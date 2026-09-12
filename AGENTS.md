# Maintaining this academic homepage

This repository belongs to Shiyu Shen / 沈石禹. Conversational updates must keep the English homepage, Chinese homepage, both LaTeX CVs, and both compiled PDFs synchronized.

## Source of truth

- Read `content.json` and existing source before updating; preserve unrelated edits.
- Add only user-provided or explicitly verified facts. Never invent affiliations, paper acceptance, author roles, degrees, metrics, or dates. Do not silently replace a CV publication year with an earlier preprint submission year.
- `person` contains contact details; `en` and `zh` contain parallel research, education, projects and experience; `publications` is shared. Paper titles remain English in the Chinese CV, as in the source.
- Keep publication IDs unique and stable, author order accurate, and review statuses current only when confirmed.

## Publication links

- `url` holds a verified DOI, publisher, arXiv, OpenReview or other original paper page. Search Scholar when requested; disclose access restrictions and never invent citation IDs.
- `pdf: "papers/filename.pdf"` explicitly selects a user-provided PDF. It takes precedence over `url`. The real file must exist inside `papers/`; never add a placeholder PDF.
- If both are empty, the title links to an exact-title Scholar search. This is a search fallback, not a verified paper record.
- `scripts/common.py` owns resolution and validation. Website PDF links are relative; downloadable CV links are absolute URLs under `site.base_url`.
- Paper title text must stay black in normal, hover, focus, visited webpage states and in the PDFs.
- Record link checks and limitations in `docs/publication-link-audit.json`. Do not delete a paper merely because its public PDF is unavailable.

## Update sequence

1. Update confirmed facts in both languages of `content.json`.
2. Run `python3 scripts/build.py --pdf` to regenerate both HTML pages, both `cv/*.tex` files and both `cv/*.pdf` files. XeLaTeX with Chinese support is required. If compilation fails, report the blocker; never describe stale PDFs as updated.
3. Run `python3 scripts/check.py --pdf` (requires `pypdf`) and `python3 -m unittest discover -s tests`. After substantive CV changes, render and inspect both PDFs. Check desktop/mobile webpage display when layout changes.
4. Review the diff and commit all source and generated outputs together. Do not commit TeX logs, temporary fonts, credentials or unrelated files. Direct changes to generated HTML/TeX alone are insufficient; update the generator/template when changing formatting.
5. Push through authorized GitHub access without force-pushing. Check the deployed page if Pages is enabled; otherwise explain the remaining setting without claiming deployment succeeded.

Future updates occur when the user requests them; this project does not imply background monitoring.
