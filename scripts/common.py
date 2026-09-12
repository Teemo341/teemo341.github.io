"""Shared facts and publication link rules for the website and both CVs."""
import json
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit, urljoin

ROOT = Path(__file__).resolve().parents[1]


def load_data():
    return json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))


def scholar_url(paper):
    return 'https://scholar.google.com/scholar?q=' + quote('"' + paper['title'] + '"', safe='')


def publication_link(paper, data, *, absolute=False):
    """Prefer a chosen local PDF, then a verified URL, then a title search.

    A configured missing PDF is a build error, never a published broken link.
    Local PDF links in downloadable CVs are absolute public HTTPS URLs.
    """
    if paper.get('pdf'):
        path = PurePosixPath(paper['pdf'])
        if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] != 'papers' or path.suffix.lower() != '.pdf':
            raise ValueError(f'Paper {paper["id"]}: pdf must be a relative papers/*.pdf path')
        target = (ROOT / path).resolve()
        if not target.is_relative_to((ROOT / 'papers').resolve()) or not target.is_file():
            raise ValueError(f'Paper {paper["id"]}: local PDF is missing: {path}')
        if not target.read_bytes().startswith(b'%PDF-'):
            raise ValueError(f'Paper {paper["id"]}: file is not a PDF: {path}')
        link = quote(path.as_posix(), safe='/')
        return urljoin(data['site']['base_url'], link) if absolute else link
    link = paper.get('url') or scholar_url(paper)
    parsed = urlsplit(link)
    if parsed.scheme != 'https' or not parsed.netloc:
        raise ValueError(f'Paper {paper["id"]}: expected a public HTTPS URL')
    return link


def validate(data):
    base = urlsplit(data['site']['base_url'])
    if base.scheme != 'https' or not base.netloc or not data['site']['base_url'].endswith('/'):
        raise ValueError('site.base_url must be an absolute HTTPS URL ending in /')
    ids = [p['id'] for p in data['publications']]
    if len(ids) != len(set(ids)):
        raise ValueError('Publication IDs must be unique and stable')
    for paper in data['publications']:
        publication_link(paper, data)
