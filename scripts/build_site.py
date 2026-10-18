"""Copy only reviewed presentation artifacts into the public site directory."""
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
(DOCS/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ML Architecture</title><style>*{box-sizing:border-box}body{margin:0;background:#faf9f7;color:#242421;font:20px/1.55 system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:60px 6vw}h1{font:76px/1 Georgia,serif;margin:25px 0}h2{font:34px Georgia,serif;margin-top:38px}small,a{color:#a62c40}a{text-underline-offset:5px}.open{display:inline-block;padding:14px 22px;background:#242421;color:#fff;text-decoration:none;margin:12px 0}li{margin:10px 0}footer{margin-top:40px;border-top:1px solid #d5d3cc;padding-top:20px;font-size:16px}</style><main><small>SOFTWARE ENGINEERING MASTERCLASS · 20 OCTOBER 2026</small><h1>ML Architecture</h1><p>'''+str(len(manifest))+''' slides following one bank customer-churn case through serving, monitoring, design, MLOps, security and quality.</p><a class="open" href="presentation.html">Open the presentation →</a><p><strong>Right / Space:</strong> next diagram build, then next slide.<br><strong>Left:</strong> previous build, then previous slide.<br><strong>Page Up / Down:</strong> move directly between slides.<br><strong>G:</strong> contents. <strong>F:</strong> fullscreen.</p><p><a href="presentation.html?motion=static">Open complete slides without builds</a></p><h2>Expanded drift section</h2><ul>'''+links+'''</ul><h2>Read and download</h2><ul><li><a href="presentation.pdf">Slide deck · PDF</a></li><li><a href="presenter-guide.pdf">Presenter guide · PDF</a></li><li><a href="presenter-guide.md">Presenter guide · Markdown</a></li><li><a href="speaker-notes.pdf">Speaker notes (script, slide, cues) · PDF</a></li><li><a href="presentation.html" download>Offline presentation · HTML</a></li></ul><h2>Edit your section</h2><p><a href="https://github.com/Sims2k/ml-ai-presentation">Source repository and collaboration instructions</a>. Presenter-owned JSON files contain the text; Python modules contain the diagrams.</p><footer>This review link is public and does not require joining a Tailnet. The banking examples are illustrative. Third-party figure and font credits are recorded in the repository.</footer></main></html>''')
(DOCS/'.nojekyll').write_text('')
print('Public site:',DOCS)
