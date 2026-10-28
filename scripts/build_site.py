"""Assemble both reviewed lectures into a portable presentation archive."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs';DOCS=ROOT/'docs'
DOCS.mkdir(exist_ok=True)
for source,dest in [('ml-architecture-lecture.html','presentation.html'),('ml-architecture-lecture.pdf','presentation.pdf'),('lecture-presenter-guide.pdf','presenter-guide.pdf'),('lecture-presenter-guide.md','presenter-guide.md'),('lecture-manifest.json','slides.json')]:
    shutil.copy2(OUT/source,DOCS/dest)
# speaker-notes.pdf requires a LaTeX toolchain (scripts/build_speaker_notes.py + xelatex),
# which CI does not install; copy it in only when a local build produced one, and otherwise
# keep whatever copy is already checked into docs/.
if (OUT/'speaker-notes.pdf').exists():
    shutil.copy2(OUT/'speaker-notes.pdf',DOCS/'speaker-notes.pdf')
manifest=json.loads((OUT/'lecture-manifest.json').read_text())
find=lambda title:next(s['number'] for s in manifest if s['title']==title)
links=''.join(f'<li><a href="presentation.html#{find(title)}">{title}</a></li>' for title in ['How the world changes over time','Data drift: a different customer mix','Concept drift: a different relationship','Concept drift: how M1 starts making errors'])
# === DAY 2: AGENTIC AI ARCHITECTURE ===
D2=OUT/'day2';DOCS2=DOCS/'day2';DOCS2.mkdir(exist_ok=True)
for source,dest in [('agentic-architecture-lecture.html','presentation.html'),('agentic-architecture-lecture.pdf','presentation.pdf'),('day2-presenter-guide.pdf','presenter-guide.pdf'),('day2-presenter-guide.md','presenter-guide.md'),('day2-manifest.json','slides.json'),('day2-speaker-notes.pdf','speaker-notes.pdf')]:
    if (D2/source).exists():shutil.copy2(D2/source,DOCS2/dest)
# Preparation PDFs are preserved in docs; fresh local builds can replace them.
for source,dest in [('day1-group-handoff.pdf',DOCS/'group-handoff.pdf'),('day2-group-handoff.pdf',DOCS2/'group-handoff.pdf'),('simon-evaluation-brief.pdf',DOCS2/'evaluation-brief.pdf')]:
    candidate=OUT/'preparation'/source
    if candidate.exists():shutil.copy2(candidate,dest)
day2=json.loads((DOCS2/'slides.json').read_text())

def deck(date,title,blurb,base,extra=''):
    files=[('presentation.pdf','Slides · PDF'),('presenter-guide.pdf','Presenter guide · PDF'),('speaker-notes.pdf','Speaker notes · PDF'),('group-handoff.pdf','Group handoff · PDF'),('presenter-guide.md','Presenter guide · Markdown'),('evaluation-brief.pdf','Evaluation brief · PDF')]
    links=''.join(f'<a class="secondary" href="{base}{f}">{label}</a>' for f,label in files if (DOCS/base/f).exists())
    return f'<section class="deck"><span class="badge">{date}</span><h2>{title}</h2><p class="sub">{blurb}</p><div class="links"><a class="primary" href="{base}presentation.html">Open the slides →</a>{links}</div>{extra}</section>'

drift='<details><summary>Day 1 · expanded drift section</summary><ul>'+links+'</ul></details>'
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Arquitetura de Sistemas de IA · Presentations</title><style>*{box-sizing:border-box}body{margin:0;background:#faf9f7;color:#242421;font:19px/1.55 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:56px 5vw}small{color:#a62c40;letter-spacing:.05em}h1{font:64px/1.04 Georgia,serif;margin:18px 0 12px}h2{font:32px/1.15 Georgia,serif;margin:6px 0 6px}.lede{color:#454943;max-width:780px}a{color:#a62c40;text-underline-offset:4px}.deck{border:1px solid #d7d4cc;border-radius:6px;padding:32px;margin:26px 0;background:#fcfbf9}.badge{display:inline-block;font-size:14px;letter-spacing:.06em;text-transform:uppercase;color:#a62c40;border:1px solid #e0c3ca;border-radius:999px;padding:3px 12px}.sub{color:#60635e;font-size:17px;margin:0 0 18px}.links{display:flex;gap:10px;flex-wrap:wrap}.primary{display:inline-block;background:#242421;color:#fff;padding:12px 18px;text-decoration:none}.secondary{display:inline-block;border:1px solid #b9b6ae;padding:12px 16px;text-decoration:none;color:#242421;font-size:17px}details{margin-top:18px;font-size:17px}summary{cursor:pointer;color:#454943}li{margin:6px 0}footer{margin-top:36px;border-top:1px solid #d7d4cc;padding-top:18px;font-size:16px;color:#60635e}</style><main><small>ARQUITETURA DE SISTEMAS DE IA · GROUP WORK</small><h1>Presentations</h1><p class="lede">Both lectures, their PDFs, presenter guides, speaker notes and handoffs — one page for the whole group. Archived after the October 2026 presentations. The temporary public review endpoint is closed; the decks work offline or through the local preview server.</p>'''
html+=deck('27 October 2026','Day 2 — Agentic AI Architecture',str(len(day2))+' slides, 40 minutes. Harness engineering, design patterns, architecture evaluation, context engineering, and what changes when agents run always-on (Pi, Pi Durable, Hermes).','day2/')
html+=deck('20 October 2026','Day 1 — ML Architecture',str(len(manifest))+' slides following one bank customer-churn case through serving, monitoring, design, MLOps, security and quality.','',drift)
html+='''<footer><strong>Keys:</strong> Right / Space next build, then next slide · Left back · Page Up / Down jump · G contents · F fullscreen · E edit text locally (Ctrl/Cmd+S downloads a copy). Add <code>?motion=static</code> to a deck URL to see complete diagrams. Presenter text lives in <a href="https://github.com/Sims2k/ml-ai-presentation">the repository</a>: <code>slides/</code> for Day 1, <code>slides/day2/</code> for Day 2. Third-party figure, icon and font credits are in THIRD_PARTY.md.</footer></main></html>'''
(DOCS/'index.html').write_text(html)
(DOCS2/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=../"><title>Agentic AI Architecture</title><a href="../">Presentations</a>')
(DOCS/'.nojekyll').write_text('')
print('Presentation archive:',DOCS)
