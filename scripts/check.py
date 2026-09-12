"""Check generated pages, local assets and optional PDF publication links."""
import argparse
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from common import ROOT, load_data, publication_link, validate


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.titles = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))
        if tag == 'h4':
            self.in_title = True
            self.titles.append('')

    def handle_endtag(self, tag):
        if tag == 'h4':
            self.in_title = False

    def handle_data(self, text):
        if self.in_title:
            self.titles[-1] += text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', action='store_true')
    args = parser.parse_args()
    data = load_data()
    validate(data)
    for rel, lang in [('index.html', 'en'), ('zh/index.html', 'zh-CN')]:
        path = ROOT / rel
        page = Page()
        page.feed(path.read_text(encoding='utf-8'))
        assert next(a['lang'] for t, a in page.nodes if t == 'html') == lang
        assert sorted(page.titles) == sorted(p['title'] for p in data['publications'])
        ids = [a['id'] for _, a in page.nodes if 'id' in a]
        assert len(ids) == len(set(ids)), f'{rel}: duplicate IDs'
        hrefs = [a['href'] for t, a in page.nodes if t == 'a']
        for paper in data['publications']:
            link = publication_link(paper, data)
            if paper.get('pdf') and lang == 'zh-CN':
                link = '../' + link
            assert link in hrefs, f'{rel}: missing publication {paper["id"]}'
        for _, node in page.nodes:
            value = node.get('href', node.get('src', ''))
            url = urlsplit(value)
            if not url.scheme and url.path:
                assert (path.parent / unquote(url.path)).is_file(), f'{rel}: missing asset {value}'
            if value.startswith('#'):
                assert value[1:] in ids, f'{rel}: broken section link {value}'
        print(f'PASS {rel}: all titles, language, links and local assets')
    if args.pdf:
        from pypdf import PdfReader
        wanted = {publication_link(p, data, absolute=True) for p in data['publications']}
        for stem in ['Shiyu_Shen_Academic_CV', 'Shiyu_Shen_Academic_CV_CN']:
            pdf = PdfReader(ROOT / 'cv' / (stem + '.pdf'))
            links = set()
            for page in pdf.pages:
                for ref in page.get('/Annots', []):
                    action = ref.get_object().get('/A', {})
                    if action.get('/S') == '/URI':
                        links.add(str(action['/URI']))
            assert wanted <= links, f'{stem}: missing publication links: {wanted - links}'
            assert (ROOT / 'cv' / (stem + '.tex')).is_file()
            print(f'PASS {stem}.pdf: {len(pdf.pages)} pages; all publication URLs clickable')


if __name__ == '__main__':
    main()
