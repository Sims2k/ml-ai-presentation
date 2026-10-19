# ML / AI architecture presentation

English lecture for a software engineering master's class. The Day 1 deck uses
one bank customer-churn case. It includes 54 slides, separate full-width drift
figures, named presenters, a slide-aligned presenter guide, and keyboard builds.

- [Public review](https://agentbox.tail289ef2.ts.net:8443/ml-ai-presentation/)
- [Slides](docs/presentation.html) · [PDF](docs/presentation.pdf)
- [Presenter guide](docs/presenter-guide.pdf)
- [Speaker notes](docs/speaker-notes.pdf) — slide-aligned scripts, slide images, and delivery cues

The public review does **not** require a Tailnet connection. The HTML download is
self-contained and works offline.

## Edit your slides

| Presenter | Editable content |
| --- | --- |
| Ricardo | `slides/01-ricardo-foundations.json` |
| Tomás | `slides/02-tomas-serving.json` |
| Simon | `slides/03-simon-monitoring.json` |
| Luca | `slides/04-luca-design.json` |
| Matheus · architecture | `slides/05-tbd-architecture.json` |
| Matheus | `slides/06-matheus-mlops.json` |
| Simon + Matheus | `slides/07-simon-matheus-security.json` |
| Matheus · quality | `slides/08-tbd-quality.json` |
| Matheus · tools | `slides/09-tbd-tools.json` |

Change `title`, `lead`, `bullets`, `example`, `takeaway`, `source`, or `owner` in your file.
Keep each `id` unchanged. `<b>...</b>` marks a short emphasized phrase.
Diagram-led slides keep their bullets in the presenter guide instead of repeating
them beside the figure.

Use a branch and pull request, or fork the repository if you have read-only
access. You can edit JSON with GitHub's web editor. The Actions build checks
navigation/layout and produces a downloadable site artifact. Do not edit only a
generated HTML file: a later build will overwrite it.

For diagram geometry, edit `scripts/lecture_full_visuals.py` or
`scripts/drift_visuals.py`. To add/reorder slides, edit `scripts/lecture_content.py`
and add the corresponding JSON content. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Build locally

Requires Python 3.11+, Node 22+, and [Pandoc](https://pandoc.org/installing.html).
On Ubuntu, install Pandoc with `sudo apt-get install pandoc`.

```sh
git clone https://github.com/Sims2k/ml-ai-presentation.git
cd ml-ai-presentation
npm ci
npx playwright install chromium
npm run build
npm test
npm run site
npm run serve
```

Open `http://localhost:8000`. On Linux, Playwright may need
`npx playwright install --with-deps chromium`.

`npm run build` writes `outputs/`; `npm test` checks keyboard traversal, overlap,
SVG bounds, diagram states, and exports the slide/guide PDFs. `npm run site`
copies the reviewed results to `docs/`. Browser text edits with E are local to
that browser; Ctrl/Cmd+S downloads an edited copy, not a repository commit.

### Speaker notes

`docs/speaker-notes.pdf` is a committed artifact, not rebuilt by CI (it needs a
LaTeX toolchain CI does not install). To regenerate it after editing slide
content, install XeLaTeX (`texlive-xetex` or similar) and run:

```sh
npm run build
npm test        # verifies the deck, exports PDFs, and captures the current slide images
python3 scripts/build_speaker_notes.py
xelatex -interaction=nonstopmode -halt-on-error -output-directory=outputs src/speaker-notes.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=outputs src/speaker-notes.tex
python3 scripts/verify_speaker_notes.py  # needs pdftotext (Poppler)
npm run site
```

Slide content comes from `lecture_content.build_lecture()` and the presenter JSON
files. Spoken prose is authored separately in `scripts/speaker_scripts.py` and
must be updated when a slide changes. The notes generator groups that prose into
short bulleted paragraphs and adds visual/build/handoff cues. It uses the fresh
screenshots produced by `npm test` in `previews/lecture-full/`.

The 19 October content merge follows the 54 visible slides in the colleagues’
Google review deck. `src/colleague-review.json` records the changed content and
skipped originals; it is provenance, not a second editable content source.
Ricardo’s opening order and Tomás’s seven-slide serving section follow that
review. Matheus owns architecture tactics, quality and tools. Names containing
`tbd` in JSON filenames are retained for stable colleague links; assignments
inside those files and on slides are current.

## Publishing

The public review currently serves the curated `docs/` directory via a public
Tailscale Funnel path. It is independent of the private Tailnet review route.
A new source commit does not automatically update that server checkout.

Actions builds an updated site artifact for each change. If GitHub Pages is
configured with source **GitHub Actions**, the workflow also deploys it to Pages.
The owner can enable that in Settings → Pages. Otherwise use the artifact or
pull, build, test, and refresh the public server checkout.

## Content and attribution

See [SOURCES.md](SOURCES.md) and [THIRD_PARTY.md](THIRD_PARTY.md). The monitoring
section opens with the attributed original Krawczyk/Cano temporal-drift figure
and presenter-approved bank illustrations (`scripts/drift_visuals.py`). No library PDFs, Zotero credentials, server configuration, or
local session files are included. Banking records, outcomes, incidents and tool
records are teaching illustrations, not reported experiments.
