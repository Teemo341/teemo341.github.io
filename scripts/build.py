"""Build both language pages and LaTeX CVs; add --pdf to compile both PDFs."""
import argparse
import shutil
import subprocess
from html import escape
from pathlib import Path
from common import ROOT, load_data, publication_link, validate

DATA = load_data()
BASE = DATA['site']['base_url']


def e(value):
    return escape(str(value), quote=True)


def render(lang):
    c = DATA[lang]
    cn = lang == 'zh'
    prefix = '../' if cn else ''
    page_url = BASE + ('zh/' if cn else '')
    sections = ['about', 'publications', 'education', 'experience', 'projects']
    nav = ''.join(f'<a href="#{key}">{e(c["nav"][key])}</a>' for key in sections)
    papers = ''
    for year in sorted({p['year'] for p in DATA['publications']}, reverse=True):
        items = ''
        for p in [x for x in DATA['publications'] if x['year'] == year]:
            title = e(p['title'])
            link = publication_link(p, DATA)
            if p.get('pdf'):
                link = prefix + link
            hint = ('在 Google Scholar 中检索此标题' if cn else 'Search this title on Google Scholar') if not p.get('pdf') and not p.get('url') else ('打开论文' if cn else 'Open paper')
            title = f'<a href="{e(link)}" title="{hint}">{title}</a>'
            authors = e(p['authors']).replace('Shiyu Shen', '<strong>Shiyu Shen</strong>')
            meta = e(p['venue'])
            if p.get('arxiv'):
                meta = f'arXiv:{e(p["arxiv"])}'
            if p.get('review'):
                status = f'{p["review"]} 审稿中' if cn else f'Under review at {p["review"]}'
                meta += (' <span aria-hidden="true">·</span> ' if meta else '') + f'<span class="review">{e(status)}</span>'
            items += f'<li class="paper" data-source-id="{p["id"]}"><h4 lang="en">{title}</h4><p class="authors" lang="en">{authors}</p>' + (f'<p class="venue">{meta}</p>' if meta else '') + '</li>'
        papers += f'<div class="year-group"><h3 class="year">{year}</h3><ol class="paper-list">{items}</ol></div>'
    education = ''.join(f'<li class="entry"><div class="entry-heading"><h3>{e(x["degree"])}</h3><span class="date">{e(x["years"])}</span></div><p class="organization">{e(c["university"])}</p><p class="detail">{e(x["awards"])}</p></li>' for x in c['education'])
    experience = ''.join(f'<li class="entry"><div class="entry-heading"><h3>{e(x["organization"])}</h3><span class="date">{e(x["years"])}</span></div><p class="organization">{e(x["project"])}</p>' + (f'<p class="detail">{e(x["role"])}</p>' if x['role'] else '') + '</li>' for x in c['experience'])
    projects = ''.join(f'<li class="entry"><div class="entry-heading"><h3>{e(x["title"])}</h3><span class="date">{e(x["year"])}</span></div><p class="detail">{e(x["role"])}</p></li>' for x in c['projects'])
    interests = ''.join(f'<li>{e(x)}</li>' for x in c['interests'])
    r = c['research']
    paragraphs = ''.join(f'<p>{e(x)}</p>' for x in [r['interests_sentence'] + ' ' + r['current_work'], r['tooling'] + ' ' + r['engineering']])
    person = DATA['person']
    publication_count = f'{len(DATA["publications"])} 篇研究工作' if cn else f'{len(DATA["publications"])} works'
    en_url = '../index.html' if cn else 'index.html'
    zh_url = 'index.html' if cn else 'zh/index.html'
    cv = 'Shiyu_Shen_Academic_CV_CN.pdf' if cn else 'Shiyu_Shen_Academic_CV.pdf'
    return f'''<!doctype html>
<html lang="{'zh-CN' if cn else 'en'}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(c['name'])} | {e(c['university'])}</title>
  <meta name="description" content="{e(c['description'])}">
  <meta name="author" content="{e(person['name'])}">
  <meta name="theme-color" content="#f8f7f3">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="{e(c['name'])} | {e(c['university'])}">
  <meta property="og:description" content="{e(c['description'])}">
  <meta property="og:url" content="{page_url}">
  <meta property="og:locale" content="{'zh_CN' if cn else 'en_US'}">
  <link rel="canonical" href="{page_url}">
  <link rel="alternate" hreflang="en" href="{BASE}">
  <link rel="alternate" hreflang="zh-CN" href="{BASE}zh/">
  <link rel="alternate" hreflang="x-default" href="{BASE}">
  <link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg">
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <script src="{prefix}assets/main.js" defer></script>
</head>
<body id="top">
<a class="skip-link" href="#main">{e(c['skip'])}</a>
<header class="site-header">
  <div class="header-inner">
    <a class="wordmark" href="#top" aria-label="{e(c['name'])}"><span class="monogram" aria-hidden="true">S.</span><span>{e(c['academic'])}</span></a>
    <nav class="language-switch" aria-label="Language / 语言">
      <a href="{en_url}" lang="en" hreflang="en" {'aria-current="page"' if not cn else ''}>EN<span class="sr-only"> — English</span></a>
      <a href="{zh_url}" lang="zh-CN" hreflang="zh-CN" {'aria-current="page"' if cn else ''}>中文</a>
    </nav>
  </div>
</header>
<div class="page-shell">
  <aside class="sidebar">
    <p class="sidebar-label">{e(c['contents'])}</p>
    <nav class="section-nav" aria-label="{e(c['contents'])}">{nav}</nav>
    <div class="sidebar-links"><a href="{e(person['scholar'])}">Google Scholar <span aria-hidden="true">↗</span></a><a href="{e(person['github'])}">GitHub <span aria-hidden="true">↗</span></a></div>
    <a class="cv-button" href="{prefix}cv/{cv}" download>{e(c['download'])}<span aria-hidden="true">↓</span></a>
  </aside>
  <main id="main">
    <section class="about-section" id="about" aria-labelledby="name">
      <div class="hero">
        <div class="hero-copy"><p class="eyebrow">{e(c['role'])}</p><h1 id="name">{e(c['name'])}</h1><p class="other-name" lang="{'en' if cn else 'zh-CN'}">{e(c['other_name'])}</p><p class="affiliation">{e(c['university'])}<br><span>{e(c['location'])}</span></p></div>
        <img class="portrait" src="{prefix}assets/portrait.jpg" alt="{e(c['portrait_alt'])}" width="144" height="192" fetchpriority="high">
      </div>
      <div class="contact"><a href="mailto:{e(person['email'])}">{e(person['email'])}</a><a href="tel:{e(person['phone_uri'])}">{e(person['phone'])}</a></div>
      <div class="research"><h2 class="sr-only">{e(c['research_heading'])}</h2><ul class="interest-list">{interests}</ul><div class="profile-copy">{paragraphs}</div></div>
    </section>
    <section id="publications" aria-labelledby="publications-heading">
      <div class="section-heading"><h2 id="publications-heading">{e(c['publication_heading'])}</h2><span>{e(publication_count)}</span></div>
      {papers}
    </section>
    <section id="education" aria-labelledby="education-heading"><div class="section-heading"><h2 id="education-heading">{e(c['nav']['education'])}</h2></div><ol class="entry-list education">{education}</ol></section>
    <section id="experience" aria-labelledby="experience-heading"><div class="section-heading"><h2 id="experience-heading">{e(c['experience_heading'])}</h2></div><ol class="entry-list">{experience}</ol></section>
    <section id="projects" aria-labelledby="projects-heading"><div class="section-heading"><h2 id="projects-heading">{e(c['project_heading'])}</h2></div><ol class="entry-list">{projects}</ol></section>
    <footer><span>© {e(DATA['site']['updated'][:4])} {e(c['name'])}</span><a href="#top">{e(c['back_top'])} <span aria-hidden="true">↑</span></a></footer>
  </main>
</div>
</body>
</html>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', action='store_true', help='Compile both generated CVs with XeLaTeX')
    args = parser.parse_args()
    validate(DATA)
    from render_cv import render_all
    render_all(DATA)
    for language, path in [('en', ROOT / 'index.html'), ('zh', ROOT / 'zh' / 'index.html')]:
        path.parent.mkdir(exist_ok=True)
        path.write_text(render(language), encoding='utf-8')
        print(f'Generated {path.relative_to(ROOT)}')
    if args.pdf:
        engine = shutil.which('xelatex')
        if not engine:
            raise SystemExit('XeLaTeX is required for --pdf. Install TeX Live with Chinese language support.')
        for stem in ['Shiyu_Shen_Academic_CV', 'Shiyu_Shen_Academic_CV_CN']:
            for run in range(2):
                result = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', stem + '.tex'], cwd=ROOT / 'cv', text=True, capture_output=True)
                if result.returncode:
                    print(result.stdout[-8000:])
                    raise SystemExit(f'CV compilation failed: {stem}. Inspect cv/{stem}.log; do not publish stale PDFs.')
            print(f'Compiled cv/{stem}.pdf')


if __name__ == '__main__':
    main()
