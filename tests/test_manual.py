import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pypdf import PdfReader, PdfWriter

from tagcast_manual.content import inline, load_chapter, parse_blocks
from tagcast_manual.provenance import local_path, sha256, verify_assets
from tagcast_manual.render import Design, DeterministicCanvas, GuideDoc, build
from tagcast_manual.validate import validate

ROOT = Path(__file__).resolve().parents[1]


class ContentTests(unittest.TestCase):
    def test_all_effective_chapters_parse_and_keep_historical_labels(self):
        base = ROOT / 'content/editions/1.7.0/en'
        names = json.loads((base / 'chapters.json').read_text())
        chapters = [load_chapter(base / name) for name in names]
        self.assertEqual(50, len(chapters))
        self.assertEqual(50, len({chapter['id'] for chapter in chapters}))
        queue = next(chapter for chapter in chapters if chapter['id'] == 'play-music-and-manage-the-queue')
        self.assertIn('The local queue is remembered', str(queue))
        self.assertNotIn('The ordinary queue is temporary', str(queue))
        self.assertIn('Earlier 1.6.5 capture', str(chapters))

    def test_unknown_or_unclosed_directives_do_not_silently_drop_content(self):
        for text in ['::: unknown\nhello\n:::', '::: small\nhello',
                     '::: gallery\nhello\n:::', '::: column',
                     '::: figure\ncaption\n:::']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_blocks(text)

    def test_table_proportions_are_validated(self):
        with self.assertRaises(ValueError):
            parse_blocks('::: table {"widths":[0.2,0.2],"headers":true}\n| A | B |\n|---|---|\n:::')

    def test_plain_markup_and_entities_cannot_become_reportlab_commands(self):
        self.assertEqual('&lt;b&gt;literal&lt;/b&gt; &amp; <b>bold</b>', inline('<b>literal</b> & **bold**'))

    def test_links_and_line_breaks_remain_explicit(self):
        result = inline('[Wiki](https://github.com/cyberdeliaAI/tagcast/wiki)  \nNext')
        self.assertIn('href="https://github.com/cyberdeliaAI/tagcast/wiki"', result)
        self.assertIn('<br/>Next', result)


class ProvenanceTests(unittest.TestCase):
    def test_original_assets_and_legacy_sources_match_hashes(self):
        screenshots, fonts, figures = verify_assets(ROOT)
        self.assertEqual((43, 4, 44), (len(screenshots), len(fonts), len(figures)))

    def test_assets_cannot_escape_checkout(self):
        with self.assertRaises(ValueError):
            local_path(ROOT, '../outside.png')

    def test_wrong_hash_stops_build(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'manifests').mkdir()
            (root / 'asset.png').write_bytes(b'changed screenshot')
            (root / 'manifests/screenshots.json').write_text(json.dumps({
                'test': {'path': 'asset.png', 'sha256': '0' * 64}}))
            (root / 'manifests/fonts.json').write_text('{"fonts":{}}')
            (root / 'manifests/legacy.json').write_text('[]')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                verify_assets(root)


class PDFTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name)
        cls.pdf, cls.manifest = build(ROOT, cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_historical_text_images_links_and_layout_are_preserved(self):
        report = validate(ROOT, self.pdf, self.output, visual=False)
        self.assertEqual((52, 51, 100, 110), (report['pages'], report['bookmarks'],
                                            report['internal_links'], report['external_links']))
        self.assertLessEqual(report['max_text_position_delta_pt'], .002)

    def test_metadata_and_edition_date_are_explicit(self):
        reader = PdfReader(self.pdf, strict=True)
        self.assertEqual('Tagcast Manual 0.1.0', reader.metadata.creator)
        self.assertTrue(reader.metadata['/CreationDate'].startswith('D:20261111000000'))
        self.assertEqual('en', reader.trailer['/Root']['/Lang'])
        self.assertEqual(44, len(self.manifest['image_uses']))

    def test_reference_pdf_bytes_remain_unchanged(self):
        self.assertEqual('7b0a384006e6f71f114ee3424f75b286a81f3b7fd83ae30a06c458a4e29a8bce',
                         sha256(self.pdf))

    def test_a_changed_external_link_fails_validation(self):
        reader = PdfReader(self.pdf)
        writer = PdfWriter()
        writer.clone_document_from_reader(reader)
        from pypdf.generic import NameObject, TextStringObject
        for page in writer.pages:
            changed = False
            for ref in page.get('/Annots', []):
                action = ref.get_object().get('/A', {})
                if '/URI' in action:
                    action[NameObject('/URI')] = TextStringObject('https://example.invalid/changed')
                    changed = True
                    break
            if changed:
                break
        target = self.output / 'changed-link.pdf'
        writer.write(target)
        with self.assertRaisesRegex(ValueError, 'link targets changed'):
            validate(ROOT, target, self.output, visual=False)

    def test_contents_uses_actual_pages_when_a_chapter_overflows(self):
        design = Design(ROOT, self.output)
        design.chapters = design.chapters[:2]
        design.chapters[0]['blocks'] = [dict(type='text', kind='body',
                                           text='A long reference paragraph. ' * 30)] * 14
        destinations = {}
        for _ in range(3):
            stream = io.BytesIO()
            document = GuideDoc(stream, design)
            document.build(design.story(destinations), canvasmaker=lambda *a, **kw:
                           DeterministicCanvas(*a, source_epoch=1794355200, **kw))
            if destinations == document.seen:
                break
            destinations = document.seen
        self.assertGreater(destinations[design.chapters[1]['id']], 4)
        reader = PdfReader(stream)
        self.assertEqual(destinations[design.chapters[1]['id']],
                         reader.get_destination_page_number(reader.outline[2]) + 1)

    def test_ambient_epoch_is_restored(self):
        with patch.dict('os.environ', {'SOURCE_DATE_EPOCH': '321'}):
            import os
            canvas = DeterministicCanvas(io.BytesIO(), invariant=1, source_epoch=1794355200)
            self.assertEqual(1794355200, canvas._doc._timeStamp.t)
            self.assertEqual('321', os.environ['SOURCE_DATE_EPOCH'])


if __name__ == '__main__':
    unittest.main()
