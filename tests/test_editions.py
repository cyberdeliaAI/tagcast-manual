"""Version selection, source preservation and the 1.9.0 editorial snapshot."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject

from tagcast_manual.content import load_chapter
from tagcast_manual.provenance import edition_directory, load_edition, sha256, verify_assets
from tagcast_manual.render import build
from tagcast_manual.validate import validate

ROOT = Path(__file__).resolve().parents[1]


class EditionTests(unittest.TestCase):
    def test_editions_keep_stable_ids_and_separate_assets(self):
        chapters = {}
        for edition in ('1.7.0', '1.9.0'):
            base = edition_directory(ROOT, edition)
            chapters[edition] = [load_chapter(base / name) for name in
                                 json.loads((base / 'chapters.json').read_text())]
        old = {item['id'] for item in chapters['1.7.0']}
        new = {item['id'] for item in chapters['1.9.0']}
        self.assertEqual(54, len(chapters['1.9.0']))
        self.assertEqual({'first-setup', 'download-and-install-updates', 'playlist-and-details',
                          'compare-track-lists'}, new - old)
        self.assertTrue(old <= new)
        before, _, old_figures = verify_assets(ROOT)
        after, _, new_figures = verify_assets(ROOT, '1.9.0')
        self.assertEqual(11, len(after.keys() - before.keys()))
        self.assertNotEqual(old_figures['figure-003']['asset'], new_figures['figure-003']['asset'])
        self.assertEqual(old_figures['figure-040'], new_figures['figure-040'])
        self.assertIn('version numbers are examples', str(chapters['1.9.0']))
        self.assertIn('Earlier 1.6.5 capture', str(chapters['1.9.0']))

    def test_version_selection_rejects_paths_and_unknown_versions(self):
        for edition in ('../1.7.0', '/tmp', '1.9.0/../../1.7.0', '1.9.0-rc1', '9.9.9'):
            with self.subTest(edition=edition), self.assertRaises(ValueError):
                load_edition(ROOT, edition)

    def test_metadata_cannot_select_another_edition_or_output_path(self):
        metadata = load_edition(ROOT, '1.9.0')
        for changed in (dict(metadata, app_version='1.8.0'),
                        dict(metadata, filename='../outside.pdf')):
            with patch('tagcast_manual.provenance.read_json', return_value=changed):
                with self.assertRaises(ValueError):
                    load_edition(ROOT, '1.9.0')


class EditionPDFTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name)
        cls.pdf, cls.manifest = build(ROOT, cls.output, '1.9.0')

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_new_edition_content_navigation_and_layout(self):
        report = validate(ROOT, self.pdf, self.output, visual=False, edition='1.9.0')
        self.assertEqual((56, 55, 108, 47), (report['pages'], report['bookmarks'],
                                            report['internal_links'], report['image_placements']))
        self.assertEqual([], report['errors'])
        self.assertEqual('440199a359fd2df2fd615e3222fb36afbc13427c',
                         self.manifest['edition']['release_commit'])
        self.assertEqual(sha256(self.pdf), self.manifest['pdf']['sha256'])
        reader = PdfReader(self.pdf, strict=True)
        self.assertTrue(reader.metadata['/CreationDate'].startswith('D:20261113000000'))

    def test_wrong_edition_is_rejected(self):
        with self.assertRaisesRegex(ValueError, '1.7.0 edition must have 52 pages'):
            validate(ROOT, self.pdf, self.output, visual=False)

    def test_changed_wiki_link_is_rejected(self):
        reader = PdfReader(self.pdf)
        writer = PdfWriter()
        writer.clone_document_from_reader(reader)
        for ref in writer.pages[2].get('/Annots', []):
            action = ref.get_object().get('/A', {})
            if '/URI' in action and 'Getting-started' in str(action['/URI']):
                action[NameObject('/URI')] = TextStringObject('https://example.invalid/changed')
        target = self.output / 'changed-wiki.pdf'
        writer.write(target)
        with self.assertRaisesRegex(ValueError, 'Missing canonical Wiki link|regression'):
            validate(ROOT, target, self.output, visual=False, edition='1.9.0')
