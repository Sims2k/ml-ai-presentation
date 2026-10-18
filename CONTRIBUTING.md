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

One section file per owner limits merge conflicts. Avoid reformatting unrelated
sections. Adding/reordering a slide currently requires a change to the Python
sequence as well as its JSON content. The guide numbering is regenerated.

Public review updates: GitHub Pages deploys after main changes only if Pages has
been enabled by the repository owner. The existing Funnel review is a separate
server checkout and needs a pull/build/test refresh. Actions artifacts are an
alternative way to review a branch's generated site.
