"""Generate the English and Chinese LaTeX CVs from the shared content file.

Run ``python scripts/render_cv.py`` from the repository root, then compile the
generated sources with XeLaTeX from the ``cv`` directory. Publication titles
share the website's URL/PDF fallback rules, using absolute HTTPS URLs so that
downloaded CVs keep working outside the repository.
"""
from common import ROOT, load_data, publication_link, validate


def tex(value):
    """Escape plain content without allowing it to become LaTeX commands."""
    escapes = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
        "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
        "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return ''.join(escapes.get(char, char) for char in str(value))


def url_tex(value):
    # hyperref correctly restores these escaped URL characters in PDF actions.
    return ''.join({'%': r'\%', '#': r'\#', '&': r'\&', '_': r'\_'}.get(c, c)
                   for c in value)


def publication_entry(paper, data):
    name = tex(data['person']['name'])
    authors = tex(paper['authors']).replace(name, r'\me')
    title = tex(paper['title'])
    link = url_tex(publication_link(paper, data, absolute=True))
    entry = rf'  \item {authors} ``\papertitle{{{link}}}{{{title}.}}'''
    entry += "'' "
    if paper.get('venue'):
        entry += rf"\textit{{{tex(paper['venue'])}}}, "
    elif paper.get('arxiv'):
        entry += rf"\textit{{arXiv preprint arXiv:{tex(paper['arxiv'])}}}, "
    entry += f"{tex(paper['year'])}."
    if paper.get('review'):
        entry += rf" \status{{Under review at {tex(paper['review'])}.}}"
    return entry


def render_language(data, language):
    localized = data[language]
    person = data['person']
    lines = []
    lines.append(r'\section{' + tex(localized['research_heading']) + '}')
    lines.append(r'\begin{itemize}')
    for key in ['interests_sentence', 'foundations', 'tooling', 'engineering']:
        lines.append(r'  \item ' + tex(localized['research'][key]))
    lines.append(r'\end{itemize}')

    lines.append(r'\section{' + tex(localized['nav']['education']) + '}')
    for education in sorted(localized['education'], key=lambda item: item['years']):
        separator = '；' if language == 'zh' else '; '
        award_separator = '、' if language == 'zh' else ', '
        detail = education['degree'] + separator + education['awards'].replace(' · ', award_separator)
        lines.append(r'\cvrow{' + tex(localized['university']) + '}{' + tex(detail)
                     + '}{' + tex(education['years']) + '}')

    lines.append(r'\section{' + tex(localized['publication_heading']) + '}')
    lines.append(r'\begin{enumerate}')
    lines.extend(publication_entry(paper, data) for paper in data['publications'])
    lines.append(r'\end{enumerate}')

    lines.append(r'\section{' + tex(localized['project_heading']) + '}')
    for project in sorted(localized['projects'], key=lambda item: item['year']):
        lines.append(r'\projectline{' + tex(project['title']) + '}{' + tex(project['role'])
                     + '}{' + tex(project['year']) + '}')

    lines.append(r'\section{' + tex(localized['experience_heading']) + '}')
    for experience in sorted(localized['experience'], key=lambda item: item['years']):
        title = experience['organization'] + ' — ' + experience['project']
        lines.append(r'\projectline{' + tex(title) + '}{' + tex(experience['role'])
                     + '}{' + tex(experience['years']) + '}')

    template = (ROOT / 'templates' / 'cv.tex.template').read_text(encoding='utf-8')
    replacements = {
        'CJK_SETUP': (
            r'\usepackage{xeCJK}' + '\n'
            r'\IfFontExistsTF{Noto Sans SC}' + '\n'
            r'  {\setCJKmainfont{Noto Sans SC}}' + '\n'
            r'  {\IfFontExistsTF{Noto Sans CJK SC}' + '\n'
            r'    {\setCJKmainfont{Noto Sans CJK SC}}' + '\n'
            r'    {\setCJKmainfont[BoldFont=FandolHei-Bold]{FandolHei-Regular}}}'
        ) if language == 'zh' else '',
        'NAME': tex(localized['name']),
        'AUTHOR': tex(person['name']),
        'AFFILIATION': tex(localized['university'] + ('，' if language == 'zh' else ', ')
                           + localized['location']),
        'EMAIL_URI': url_tex('mailto:' + person['email']),
        'EMAIL': tex(person['email']),
        'PHONE': tex(person['phone']),
        'GITHUB': url_tex(person['github']),
        'SCHOLAR': url_tex(person['scholar']),
        'BODY': '\n'.join(lines),
    }
    for key, value in replacements.items():
        template = template.replace('@@' + key + '@@', value)
    return template


def render_all(data):
    validate(data)
    destination = ROOT / 'cv'
    destination.mkdir(exist_ok=True)
    outputs = []
    for language, suffix in [('en', ''), ('zh', '_CN')]:
        path = destination / f'Shiyu_Shen_Academic_CV{suffix}.tex'
        path.write_text(render_language(data, language), encoding='utf-8')
        outputs.append(path)
    return outputs


if __name__ == '__main__':
    for output in render_all(load_data()):
        print(output.relative_to(ROOT))
