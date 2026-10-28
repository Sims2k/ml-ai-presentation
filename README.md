# ML and agentic AI architecture — presentation archive

Two English lectures for a software engineering master's class, presented on
20 and 27 October 2026 by Ricardo, Tomás, Simon, Luca and Matheus.
The temporary Tailscale public review endpoints were closed on 28 October 2026.
The repository retains the finished materials and the sources needed to rebuild them.

| Lecture | Slides | Materials |
| --- | --- | --- |
| Day 1 — ML Architecture | 54; a bank customer-churn case | [HTML](docs/presentation.html), [PDF](docs/presentation.pdf), [presenter guide](docs/presenter-guide.pdf), [speaker notes](docs/speaker-notes.pdf), [group handoff](docs/group-handoff.pdf) |
| Day 2 — Agentic AI Architecture | 34; 40 minutes including discussion | [HTML](docs/day2/presentation.html), [PDF](docs/day2/presentation.pdf), [presenter guide](docs/day2/presenter-guide.pdf), [speaker notes](docs/day2/speaker-notes.pdf), [group handoff](docs/day2/group-handoff.pdf), [Simon's evaluation brief](docs/day2/evaluation-brief.pdf) |

Download the HTML decks to present offline, or use the local server below.
The HTML embeds fonts and graphics; presentation navigation needs JavaScript.
Printed PDFs and the static diagrams remain readable without animation.

## Repository structure

- `slides/`: presenter-owned Day 1 JSON; `slides/day2/`: Day 2 JSON.
- `scripts/`: deck builders, authored speaker scripts, diagram functions and verification.
  `deck_common.py` holds shared styles, SVG helpers and the browser controller.
- `theme/`, `assets/`, `licenses/`: shared rendering assets and attribution.
- `preparation/`: authored LaTeX handoffs and Simon's Day 2 study brief.
- `docs/`: final portable archive, including rendered PDFs and Markdown guides.
- `src/`: Day 1 guide context and colleague-review provenance still used by the build.
- `outputs/`, `previews/`, `assets/diagrams/`: ignored generated files.
  Generated speaker-note LaTeX also stays in `outputs/`.

## Build and verify

Requires Python 3.11+, Node 22+, Pandoc and Playwright Chromium.
On Ubuntu, install Pandoc with `sudo apt-get install pandoc`.

```sh
npm ci
npx playwright install chromium
npm run build
npm test
npm run site
npm run serve
```

Open `http://localhost:8000`. The preview server binds to loopback.
On Linux, Playwright may need `npx playwright install --with-deps chromium`.

The default build and test commands cover **both** lectures. Tests first build
both decks in a fresh temporary source directory to catch dependencies on cached
outputs. Checks also cover slide
geometry, keyboard traversal, diagrams, local editing and static/reduced-motion
behaviour, and export the slide/guide PDFs and screenshots.
For one lecture, use `npm run build:day1` / `npm run test:day1` or their `:day2`
equivalents. Run `npm run site` after verification to refresh `docs/`.

GitHub Actions runs both builds and their checks, then uploads a
`presentation-archive` artifact. It does not deploy a public site or check the
retired review endpoint. The repository itself remains public.

## Speaker notes

The authored prose lives in `scripts/speaker_scripts.py` and
`scripts/day2_speaker_scripts.py`. Day 2 includes optional preparation examples
and definitions, separate from the spoken scripts. Simon's five scripts fit the
six-minute allocation; the preparation boxes are material to keep in reserve.

To rebuild notes after building and verifying the decks, install XeLaTeX,
DejaVu Sans, the required TeX packages (including tcolorbox and xurl) and Poppler:

```sh
npm run notes
npm run site
```

Use `npm run notes:day1` or `npm run notes:day2` for one booklet, then
`python3 scripts/verify_speaker_notes.py --day 1` (or `--day 2`).
The generators use fresh screenshots from the deck checks. They write LaTeX to
`outputs/` with paths relative to the repository, so no AgentBox-specific paths
are needed. CI preserves the checked-in note PDFs; it does not install LaTeX.
See [preparation/README.md](preparation/README.md) for handoff and brief sources.

## Editing

Each presenter edits their JSON file, keeping `id` values stable. Day 1 uses
`title`, `lead`, `bullets`, `example`, `takeaway`, `source`, and `owner`; Day 2
uses `title`, `lead`, `cues`, `takeaway`, `source`, and `owner`. `<b>...</b>` marks
short emphasis. Edit authored scripts when changing a slide's explanation.

Day 1 order and figures live in `lecture_content.py`, `lecture_full_visuals.py`
and `drift_visuals.py`; Day 2 uses `day2_content.py` and `day2_visuals.py`.
Day 1 filenames containing `tbd` are retained for stable colleague links;
assignments within the files are current. `src/colleague-review.json` records
review provenance, rather than providing a second editable content source.

Keys: Right/Space reveals builds, then advances; Left reverses; Page Up/Down
skips between slides; G opens contents; F toggles fullscreen; E enables local
text editing. Escape finishes editing; Ctrl/Cmd+S downloads the edited HTML.
Browser edits do not update repository sources. Add `?motion=static` to view
complete diagrams. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Sources and teaching boundaries

See [SOURCES.md](SOURCES.md) and [THIRD_PARTY.md](THIRD_PARTY.md).
Banking records, outcomes and tool runs are teaching illustrations. Day 2's
system comparison is an architectural synthesis, not a comparative benchmark;
Luna's numerical acceptance targets are requirements, not reported results.
No library PDFs, credentials, connector configuration or session exports are included.
