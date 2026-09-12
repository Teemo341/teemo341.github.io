"""Guard user-uploaded PDF selection and portable CV destinations."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import common
import build
import render_cv


class PaperLinkTests(unittest.TestCase):
    def setUp(self):
        self.data = common.load_data()
        self.paper = copy.deepcopy(self.data['publications'][-1])
        self.paper.update(url='https://arxiv.org/abs/1234.56789', pdf='')

    def test_exact_title_search_fallback(self):
        self.paper['url'] = ''
        query = parse_qs(urlsplit(common.publication_link(self.paper, self.data)).query)
        self.assertEqual(query['q'], ['"' + self.paper['title'] + '"'])

    def test_chosen_pdf_overrides_url_and_cv_uses_public_address(self):
        with tempfile.TemporaryDirectory() as d, patch.object(common, 'ROOT', Path(d)):
            path = Path(d) / 'papers' / 'new-paper.pdf'
            path.parent.mkdir()
            path.write_bytes(b'%PDF-1.7\n')
            self.paper['pdf'] = 'papers/new-paper.pdf'
            self.assertEqual(common.publication_link(self.paper, self.data), 'papers/new-paper.pdf')
            self.assertEqual(common.publication_link(self.paper, self.data, absolute=True), self.data['site']['base_url'] + 'papers/new-paper.pdf')
            self.paper['pdf'] = ''
            self.assertEqual(common.publication_link(self.paper, self.data), self.paper['url'])

    def test_missing_pdf_does_not_publish_dead_link(self):
        self.paper['pdf'] = 'papers/not-uploaded.pdf'
        with self.assertRaises(ValueError):
            common.publication_link(self.paper, self.data)

    def test_local_pdf_reaches_both_pages_and_both_latex_sources(self):
        with tempfile.TemporaryDirectory() as d, patch.object(common, 'ROOT', Path(d)):
            path = Path(d) / 'papers' / 'new-paper.pdf'
            path.parent.mkdir()
            path.write_bytes(b'%PDF-1.7\n')
            data = copy.deepcopy(self.data)
            data['publications'][-1]['pdf'] = 'papers/new-paper.pdf'
            with patch.object(build, 'DATA', data):
                self.assertIn('href="papers/new-paper.pdf"', build.render('en'))
                self.assertIn('href="../papers/new-paper.pdf"', build.render('zh'))
            absolute = data['site']['base_url'] + 'papers/new-paper.pdf'
            for lang in ['en', 'zh']:
                self.assertIn('\\papertitle{' + absolute + '}', render_cv.render_language(data, lang))

    def test_pdf_path_stays_in_papers(self):
        for value in ['../cv/private.pdf', '/papers/paper.pdf', 'papers/../cv/paper.pdf']:
            self.paper['pdf'] = value
            with self.assertRaises(ValueError):
                common.publication_link(self.paper, self.data)


if __name__ == '__main__':
    unittest.main()
