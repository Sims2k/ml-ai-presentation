# Authored preparation materials

- `day1/group-handoff.tex`: Day 1 group handoff; final PDF in `docs/group-handoff.pdf`.
- `day2/group-handoff.tex`: Day 2 group handoff; final PDF in `docs/day2/group-handoff.pdf`.
- `day2/simon-evaluation-brief.tex`: Simon's five-page AgentArcEval preparation brief;
  final PDF in `docs/day2/evaluation-brief.pdf`.

These are authored LaTeX documents. Speaker-note LaTeX is generated from the
Python scripts and is kept under ignored `outputs/` instead.

## Rebuild

From the repository root, with pdfLaTeX and the required packages installed:

```sh
mkdir -p outputs/preparation
pdflatex -interaction=nonstopmode -halt-on-error -jobname=day1-group-handoff -output-directory=outputs/preparation preparation/day1/group-handoff.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname=day2-group-handoff -output-directory=outputs/preparation preparation/day2/group-handoff.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname=simon-evaluation-brief -output-directory=outputs/preparation preparation/day2/simon-evaluation-brief.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname=simon-evaluation-brief -output-directory=outputs/preparation preparation/day2/simon-evaluation-brief.tex
npm run site
```

## Reading behind Simon's brief

The accessible AgentArcEval manuscript was consulted in full, especially §1
(motivation), §4 and Figure 2 (process), §5 (eleven quality scenarios), and
§6.4–6.5 (Luna requirements and architectural changes):
https://arxiv.org/html/2510.21031v1 . The journal reference is JSS 232 (2026),
112656, DOI https://doi.org/10.1016/j.jss.2025.112656 . The publisher version was
not separately read.

Earendil's Pi Durable announcement was consulted for supervised operation,
checkpoints, interruption/recovery and tool replay:
https://earendil.com/posts/pi-durable/ .

The brief follows slides 15–19, the authored Day 2 scripts and the group handoff.
The Pi/Hermes comparison is existing presentation synthesis; no new code audit or
benchmark was performed. Luna's numerical targets are requirements, not reported
achieved performance. Downloaded paper copies and session transcripts are not
part of this archive.

The handoffs retain the planning context in which they were written. Any old
AgentBox review links within those historical PDFs are retired.
