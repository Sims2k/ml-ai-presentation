# Contributing

1. Create a branch (or fork) and edit your presenter JSON file under `slides/`.
2. Keep slide IDs and the shared bank vocabulary consistent. M1 is approved;
   M2 is a candidate. Prediction is separate from campaign policy.
3. For visual changes, edit the diagram functions rather than generated HTML.
   The full-width drift figures live in `scripts/drift_visuals.py`.
4. Run `npm run build && npm test && npm run site`. Review screenshots in
   `previews/lecture-full/` at 1280×720, including any new labels and connectors.
5. Submit a pull request explaining the changed teaching point and checks run.

The stage is fixed at 1920×1080. Preserve font sizes and split a crowded slide
instead of shrinking all its text. Keep presenter names and reading anchors.
SVG charts use accessible titles/descriptions and complete static frames.
Animations must not be necessary to understand the printed diagram.

Right/Left advances/reverses builds, then slides. Page Down/Page Up skips builds.
The keyboard regression must traverse cover slides, tables, figures, and both
ends of the deck. Do not restore the previous null-motion-root bug.

One section file per owner and lecture limits merge conflicts. Avoid reformatting unrelated
sections. Adding/reordering a slide currently requires a change to the Python
sequence as well as its JSON content. The guide numbering is regenerated.

The temporary public review endpoints are retired. GitHub Actions builds a
portable archive artifact; use `npm run serve` for a loopback-only local preview.
Both lecture builds and checks run through the default npm commands. Do not
reintroduce the old endpoint verification or automatic public deployment.

## Speaker notes and citations

Preserve the authored prose in `scripts/speaker_scripts.py` and
`scripts/day2_speaker_scripts.py`; keep explanations
aligned when editing a slide. Paragraph breaks are respected by the notes
builder. Use short `<b>...</b>` cues where they aid reading. Cite the original
book, paper or official technical documentation in `source`; personal study
notes are preparation material and must not appear as slide reading anchors.
M1 identifies the current approved artifact and M2 the candidate artifact; use
plain model roles alongside these identifiers when introducing them.

Official tool logos and Lucide icons live in `assets/marks/`. Preserve the
sources manifest and license notices. The HTML embeds assets for offline use.

Generated speaker-note LaTeX belongs in `outputs/`; only authored preparation
LaTeX belongs in `preparation/`. Notes must use repository-relative image paths.
Rebuild and verify the decks before regenerating notes, then run
`python3 scripts/verify_speaker_notes.py` and `npm run site`.
