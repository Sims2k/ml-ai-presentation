"""Build the Day 2 lecture (Agentic AI Architecture) with the Day 1 deck system.

Reuses Day 1's fonts, fixed 16:9 stage, keyboard builds, contents overlay and
local editing. Day 2 changes the slide grid: a larger figure on the left and a
key-concepts column on the right; the bottom example bar is gone.
Presenter-owned text lives in slides/day2/*.json and overrides day2_content.py.
"""
from pathlib import Path
from html import escape
import re,json,subprocess
from deck_common import FONTS,BASE,MOTION,CSS,JS,controls
from day2_content import build_day2
from day2_speaker_scripts import DIRECTIONS
from visual_marks import image

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/day2';OUT.mkdir(parents=True,exist_ok=True)
DIAGRAMS=ROOT/'assets/diagrams/day2';DIAGRAMS.mkdir(parents=True,exist_ok=True)
from day2_overrides import apply_overrides

slides=apply_overrides(build_day2())
TOTAL=len(slides)

EXTRA=r'''
/* === DAY 2 GRID: LARGER FIGURE, KEY CONCEPTS, NO BOTTOM BAR === */
.body-grid{top:298px;height:708px;grid-template-columns:1160px 1fr;gap:44px}
.diagram-column{width:1160px;height:708px}
figure{transform:scale(1.03);height:659px}
.explanation{height:708px;margin-left:-22px;padding-left:28px;display:flex;flex-direction:column}
.explanation h2{display:flex;align-items:center;gap:12px;font-size:23px;letter-spacing:.06em;text-transform:uppercase;color:#454943;margin:0 0 16px}
.explanation ul{font-size:25px;line-height:1.3;padding-left:24px}.explanation li{margin:0 0 13px}
.takeaway{margin-top:auto;font:italic 600 29px/1.2 'Cormorant Garamond',serif;color:#242421;border-top:1px solid var(--rule);padding-top:14px}
.heading h1{white-space:nowrap}
code{font:500 .86em 'IBM Plex Mono',monospace;background:#efece5;padding:1px 6px;border-radius:3px}
/* === FIGURE TYPES === */
.lecture-table{width:1160px;height:708px;padding:6px 0;overflow:visible}
.lecture-table table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:24px;line-height:1.28}
.lecture-table th{font-size:20px;letter-spacing:.04em;text-transform:uppercase;text-align:left;font-weight:600;color:#a62c40;background:#f0ede7;padding:15px 14px;border-bottom:2px solid #c5bdb0}
.lecture-table td{padding:14px;border-bottom:1px solid #d5d3cc;vertical-align:top}
.lecture-table tbody tr:nth-child(even){background:#f4f3ef}.lecture-table td:first-child{font-weight:600}
.lecture-table.decision td:last-child{color:#a62c40;font-weight:600}
.ok{color:#53674c;font-weight:600}.no{color:#a62c40;font-weight:600}
.figure-credit{align-self:flex-start;margin:0;font-size:18px;line-height:1.35;color:#60635e}
.lecture-table.dense table{font-size:21px;line-height:1.25}.lecture-table.dense td{padding:11px 12px}
.funnel-num{font:600 46px 'IBM Plex Mono',monospace;fill:#242421}
.axis-strong{fill:none;stroke:#454943;stroke-width:2}.leader{fill:none;stroke:#9a9c96;stroke-width:1.4;stroke-dasharray:5 4}
.card-name{font:600 19px 'Source Sans 3';fill:#242421}.count-num{font:600 32px 'IBM Plex Mono',monospace;fill:#242421}
.dot-ink{fill:#454943}.dot-focus{fill:#a62c40}.dot-on{fill:#718895;stroke:#526a76;stroke-width:1.2}.dot-off{fill:#faf9f7;stroke:#b9bdb6;stroke-width:1.2}.dot-zero{fill:#faf9f7;stroke:#a62c40;stroke-width:1.4;stroke-dasharray:4 3}
.sector{stroke-width:1.4}.sector.off{fill:#eef1f2;stroke:#a9b6bc}.sector.on{fill:#f3dfe3;stroke:#a62c40;stroke-width:1.8}
.hub-ring{fill:#faf9f7;stroke:#cfccc3;stroke-width:1.4}.wheel-name{font:600 24px 'Source Sans 3';fill:#242421}
.waffle{stroke-width:1}.waffle.w0{fill:#f3dfe3;stroke:#a62c40}.waffle.w1{fill:#d5dfe3;stroke:#8fa2ab}.waffle.w2{fill:#9fb3bc;stroke:#718895}.waffle.w3{fill:#526a76;stroke:#3d525c}
.water{fill:#eaf0f2;opacity:.75}.waterline{stroke:#718895;stroke-width:2}
.ice-top{fill:#faf9f7;stroke:#454943;stroke-width:1.8}.ice-under{fill:#f6f8f8;stroke:#718895;stroke-width:1.6;stroke-dasharray:7 5}
.step-add{font:600 21px 'IBM Plex Mono',monospace;fill:#a62c40}
.plate-edge{stroke-width:1.5}.plate-edge.model{fill:#e9cdd3;stroke:#a62c40}.plate-edge.data{fill:#d3dee2;stroke:#718895}.plate-edge.business{fill:#d9e1d2;stroke:#71816a}
.masthead .brand-row{display:inline-flex;align-items:center;gap:12px;margin-left:24px;vertical-align:middle}.masthead .brand-row img{height:30px;width:auto;display:block}
.code-panel{width:1160px;height:708px;background:#242421;border-radius:8px;padding:0 0 22px;display:flex;flex-direction:column}
.code-bar{display:flex;align-items:center;gap:9px;padding:16px 22px;border-bottom:1px solid #3a3b37}.code-bar span{width:13px;height:13px;border-radius:50%;background:#55564f}
.code-bar b{margin-left:14px;font:500 18px 'IBM Plex Mono',monospace;color:#c8c5bc}
.code-panel pre{margin:0;padding:26px 32px 10px;font:400 23px/1.5 'IBM Plex Mono',monospace;color:#e9e6dd;white-space:pre;flex:1}
.code-panel pre b{color:#e8a6b2;font-weight:500}.code-panel pre em{font-style:normal;color:#fff;background:rgba(166,44,64,.45);border-radius:3px}.code-panel pre .c{color:#9c9a90}
.code-panel .figure-credit{color:#b5b2a8;padding:0 32px}
/* === SVG ADDITIONS (same palette as Day 1) === */
.node.plain{fill:#faf9f7;stroke:#9a9c96}.node.family{fill:#faf9f7;stroke:#cfccc3}
.family-title{font:600 23px 'Source Sans 3';fill:#242421}.pattern-item{font:400 18px 'Source Sans 3';fill:#3d423c}
circle.used{fill:#242421}circle.unused{fill:#faf9f7;stroke:#8d918a;stroke-width:1.5}
.ring{fill:none;stroke:#696b68;stroke-width:1.7}.spoke{fill:none;stroke:#9a9c96;stroke-width:1.4;stroke-dasharray:5 4}
.hub{fill:#242421}.hub-title{font:600 25px 'Source Sans 3';fill:#faf9f7}.hub-sub{font:400 20px 'Source Sans 3';fill:#d9d6cd}
.bar{fill:#e4e6e2;stroke:#7d837b;stroke-width:1}.bar.focus{fill:#f3dfe3;stroke:#a62c40}.bar-zero{font:600 23px 'Source Sans 3';fill:#a62c40}.bar-value{font:500 19px 'IBM Plex Mono';fill:#454943}
.seg{stroke:#faf9f7;stroke-width:2}.seg.prefix{fill:#c9d4d9}.seg.history{fill:#dfe4e0}.seg.free{fill:#f4f3ef;stroke:#d4d4cc;stroke-dasharray:4 4}
.seg-label{font:600 19px 'Source Sans 3';fill:#2f362f}.threshold{stroke:#a62c40;stroke-width:2;stroke-dasharray:6 5}.threshold-label{font:500 17px 'IBM Plex Mono';fill:#a62c40}
.quote{font:italic 600 30px 'Cormorant Garamond';fill:#242421}
/* === COVER, STATEMENT, CONTENTS === */
.cover .heading{top:214px;right:560px}.cover h1{font:500 136px/1.04 'Cormorant Garamond';letter-spacing:-.04em;white-space:normal}
.cover .subtitle{font-size:36px;line-height:1.4;max-width:1050px;margin-top:30px}
.cover .cover-side{position:absolute;top:286px;right:82px;width:374px;border-left:1px solid #c9c5ba;padding-left:36px;font:500 46px/1.2 'Cormorant Garamond'}
.cover .cover-side p{font:28px/1.5 'Source Sans 3';margin-top:32px}
.cover .cover-speakers{position:absolute;left:72px;top:850px;font-size:29px;line-height:1.5}
.cover .cover-speakers small{display:block;color:#a62c40;font-size:22px;letter-spacing:.06em;margin-bottom:12px}
.statement-body{position:absolute;left:72px;right:72px;top:220px}
.statement-body .statement-q{margin:0;font:500 92px/1.08 'Cormorant Garamond';letter-spacing:-.02em;max-width:1500px}
.statement-body .topics{margin-top:44px;font:500 24px 'IBM Plex Mono';letter-spacing:.06em;text-transform:uppercase;color:#a62c40}
.reading{position:absolute;left:72px;right:72px;top:640px;display:grid;grid-template-columns:repeat(4,1fr);gap:28px;border-top:1px solid var(--rule);padding-top:26px}
.reading h3{grid-column:1/-1;margin:0;font:600 21px 'Source Sans 3';letter-spacing:.07em;text-transform:uppercase;color:#454943}
.reading p{margin:0;font-size:23px;line-height:1.35}.reading p b{display:block;font-weight:600}
#contents{position:fixed;inset:0;z-index:20000;background:#faf9f7;overflow:auto;padding:36px 5vw;font-family:'Source Sans 3'}
#contents[hidden]{display:none}#contents h2{font:48px 'Cormorant Garamond';margin:0 0 8px}#contents p{font-size:18px}
.contents-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:8px;margin-top:24px}.contents-grid button{cursor:pointer;font:19px/1.3 'Source Sans 3';text-align:left;background:transparent;border:1px solid #d5d3cc;padding:12px 16px;color:#242421}.contents-grid button small{display:block;color:#a62c40;font-size:14px;margin-bottom:5px}
button:focus-visible{outline:3px solid #a62c40;outline-offset:2px}
.course{display:flex;align-items:center;gap:28px}.concept-icon{display:block;flex:none;width:28px;height:28px}
@media print{#contents{display:none!important}}
'''

BRANDS={'Pi: a minimal core, everything else an extension':[('logo-pi.svg','Pi')],
        'Registries and adapters: finding capabilities':[('logo-mcp.svg','Model Context Protocol')],
        'Who actually writes context files?':[('logo-agentsmd.png','AGENTS.md')],'What goes into AGENTS.md':[('logo-agentsmd.png','AGENTS.md')],
        'Five ways to phrase an instruction':[('logo-agentsmd.png','AGENTS.md')],'Context files are maintained artifacts':[('logo-agentsmd.png','AGENTS.md')],
        'From session agent to always-on agent':[('logo-pi.svg','Pi'),('logo-hermes.png','Hermes Agent')],
        'Pi Durable: surviving a crash':[('logo-pi.svg','Pi')],'Hermes: an always-on agent':[('logo-hermes.png','Hermes Agent')],
        'What always-on costs':[('logo-pi.svg','Pi'),('logo-hermes.png','Hermes Agent')]}

def masthead(owner,title=''):
    marks=''.join(image(f,alt,'') for f,alt in BRANDS.get(title,[]))
    brand=f'<span class="brand-row">{marks}</span>' if marks else ''
    return f'<header class="masthead"><span class="course">AGENTIC AI ARCHITECTURE{brand}</span><span class="speaker">Presenter: <b>{escape(owner)}</b></span></header>'

pages=[];manifest=[]
for n,s in enumerate(slides,1):
    title=escape(s['title']);owner=s['owner'];folio=f'<span class="folio">{n:02d} / {TOTAL:02d}</span>'
    count=0
    if s['layout']=='cover':
        inner=f'''<header class="masthead"><span class="course">SOFTWARE ENGINEERING MASTERCLASS</span><span>27 October 2026</span></header><div class="heading"><p class="eyebrow">Architecture of AI systems · Day 2</p><h1 data-edit>Agentic AI<br>Architecture.</h1><p class="subtitle" data-edit>From a model in a pipeline to a model that acts.<br>Harnesses, patterns, evaluation, context.</p></div><aside class="cover-side">An agent is a model plus a harness.<p>Harness engineering.<br>Design patterns.<br>Architecture evaluation.<br>Context engineering.<br>Always-on agents.</p></aside><div class="cover-speakers"><small>PRESENTERS</small>Ricardo · Tomás · Simon · Luca · Matheus</div><footer><span>Day 1 put a model inside a system. Day 2 puts it inside a loop that acts.</span>{folio}</footer>'''
    elif s['layout']=='statement':
        reading=''.join(f'<p><b>{a}</b>{b}</p>' for a,b in [('Koenigstein (2026)','Harness Engineering for AI Agents — the practitioner view'),('Grootendorst & Alammar','An Illustrated Guide to AI Agents'),('Earendil (2026)','Pi Durable — earendil.com/posts/pi-durable'),('Alejandro AO (2026)','Pi and Hermes architecture explained — alejandro-ao.com')])
        inner=f'''{masthead(owner)}<div class="statement-body"><p class="eyebrow">{escape(s['section'])}</p><h1 class="statement-q" data-edit>{escape(s["lead"])}</h1><p class="topics" data-edit>{escape(s['cues'][0])}</p></div><div class="reading"><h3>Further reading</h3>{reading}</div><footer><span>Thank you · Ricardo, Tomás, Simon, Luca and Matheus</span>{folio}</footer>'''
    else:
        visual=s['visual'];visual,count=visual()
        if visual.startswith('<svg'):
            visual=f'<figure data-motion-root data-motion-mode="step" data-step-count="{count}" data-step-current="{count}" data-frame="static" data-static-frame="complete">{visual}{controls(count)}</figure>'
            slug=re.search(r'<title id="([^"]+)-title"',visual).group(1)
            (DIAGRAMS/f'{slug}.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{FONTS}{CSS}{EXTRA} body{{background:#faf9f7;margin:24px;overflow:auto}}main{{max-width:1120px;margin:auto}}h1{{font-size:48px}}figure{{transform:none;height:auto}}.diagram-container{{overflow-x:auto}}svg{{min-width:1120px}}</style></head><body><main><h1>{title}</h1><div class="diagram-container">{visual}</div><p>{escape(s["source"])}</p></main><script data-diagram-controls>{MOTION}</script></body></html>')
        cues=''.join(f'<li data-edit>{c}</li>' for c in s['cues'])
        inner=f'''{masthead(owner,s['title'])}<div class="heading"><p class="eyebrow">{escape(s['section'])}</p><h1 data-edit>{title}</h1><p class="subtitle" data-edit>{escape(s['lead'])}</p></div><div class="body-grid"><div class="diagram-column">{visual}</div><aside class="explanation"><h2>{image(s['icon']+'.svg')}Key concepts</h2><ul>{cues}</ul><p class="takeaway" data-edit>{escape(s['takeaway'])}</p></aside></div><footer><span>{escape(s['source'])}</span>{folio}</footer>'''
    classes=('cover ' if s['layout']=='cover' else '')+('statement ' if s['layout']=='statement' else '')+('active visible' if n==1 else '')
    idx=iter(range(100))
    inner=re.sub(r' data-edit(?=[ >])',lambda _:f' id="day2-edit-{n}-{next(idx)}" data-edit',inner)
    pages.append(f'<section class="slide {classes}" id="day2-{n}" aria-label="{n}. {title}">{inner}</section>')
    manifest.append(dict(number=n,title=s['title'],section=s['section'],owner=owner,steps=count,
        kind=s['layout'] if s['layout']!='standard' else ('diagram' if count else 'figure'),source=s['source']))

contents=''.join(f'<button type="button" data-jump="{m["number"]-1}"><small>{m["number"]:02d} · {escape(m["owner"])}</small>{escape(m["title"])}</button>' for m in manifest)
contents='<nav id="contents" aria-label="Lecture contents" hidden><h2>Agentic AI Architecture</h2><p>Choose a slide. Press G or Escape to return.</p><div class="contents-grid">'+contents+'</div></nav>'
NAV=r'''
/* === KEYBOARD CONTENTS AND LOCAL EDITS === */
const contents=document.getElementById('contents');let contentsOrigin=null;
const editStorageKey='agentic-architecture-lecture-v1';
try{const edits=JSON.parse(localStorage.getItem(editStorageKey)||'{}');document.querySelectorAll('[data-edit]').forEach(e=>{if(typeof edits[e.id]==='string')e.textContent=edits[e.id];});}catch{}
document.addEventListener('input',e=>{if(!e.target.matches('[data-edit]'))return;try{const edits=JSON.parse(localStorage.getItem(editStorageKey)||'{}');edits[e.target.id]=e.target.textContent;localStorage.setItem(editStorageKey,JSON.stringify(edits));}catch{}});
function toggleContents(){const open=contents.hidden;contents.hidden=!open;if(open){contentsOrigin=document.activeElement;contents.querySelector('button').focus();}else if(contentsOrigin&&contentsOrigin!==document.body){contentsOrigin.focus();}else{document.activeElement.blur();}}
document.addEventListener('keydown',e=>{if(e.target.isContentEditable)return;if(e.key.toLowerCase()==='g'){e.preventDefault();toggleContents();}if(e.key==='Escape'&&!contents.hidden){e.preventDefault();toggleContents();}});
contents.addEventListener('click',e=>{const b=e.target.closest('[data-jump]');if(b){deck.show(Number(b.dataset.jump));contentsOrigin=null;toggleContents();}});
'''
deckjs=JS.replace('presentation-edited.html','agentic-architecture-lecture-edited.html')
doc=('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Agentic AI Architecture — Day 2 lecture</title><style>'
     +FONTS+'\n'+BASE+'\n'+CSS+'\n'+EXTRA+'</style></head><body><div class="edit-notice">Editing · Escape to finish · Ctrl/Cmd+S to download</div><div class="deck-viewport"><main class="deck-stage" id="deckStage">'
     +''.join(pages)+'</main></div>'+contents+'<noscript><style>html,body{overflow:auto;height:auto}.deck-viewport,.deck-stage{position:static;overflow:visible;height:auto}.slide{position:relative;visibility:visible;opacity:1;pointer-events:auto}</style><p>All complete slides are shown without JavaScript.</p></noscript><script data-diagram-controls>'+MOTION+'</script><script>'+deckjs+NAV+'</script></body></html>')
(OUT/'agentic-architecture-lecture.html').write_text(doc)
(OUT/'day2-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

# === PRESENTER GUIDE (Markdown → HTML; PDF is printed by the verifier) ===
plain=lambda v:re.sub(r'</?b>','**',re.sub(r'</?code>','`',re.sub(r'</?span[^>]*>','',v))).replace('&lt;','<').replace('&gt;','>')
guide=['''# Agentic AI Architecture — Presenter Guide

Day 2 of *Arquitetura de Sistemas de IA*, 27 October 2026. English, topic-led,
40 minutes including discussion. No running example: each topic stands on its
own paper. Real systems appear as evidence — **Pi**, **Pi Durable** and
**Hermes**, plus the eleven harnesses of the source-code study.

## Timing and ownership

| Time | Presenter | Slides | Question |
| --- | --- | --- | --- |
| 0–2 min | All | 1–2 | Opening and agenda |
| 2–9 min | Ricardo | 3–8 | What is a harness? |
| 9–15 min | Tomás | 9–14 | Which patterns describe an agent? |
| 15–21 min | Simon | 15–19 | How do we evaluate its architecture? |
| 21–29 min | Luca | 20–26 | What does context engineering look like? |
| 29–37 min | Matheus | 27–33 | What changes when agents run always-on? |
| 37–40 min | All | 34 | Discussion |

About 70 seconds per slide. Each slide has a large figure, four key concepts
and a one-sentence takeaway. The right-hand column is read by the audience;
directions for the presenter are in this guide and in the speaker-notes PDF.

## Presenting and editing

Arrow Right/Space reveals the next part of a diagram, then moves to the next
slide; Arrow Left reverses. Page Down/Page Up change slides directly. G opens the
contents; F toggles fullscreen. E toggles local text editing (Escape finishes;
Ctrl/Cmd+S downloads an edited copy). Browser edits stay on that laptop. To change
slide text for everyone, edit your file in `slides/day2/` and rebuild.

## Boundaries of the evidence

- Paper numbers are quoted from the cited sections: eleven harnesses and 29
  patterns (Barbaste et al.), 18 patterns from 57 studies (Liu et al.), eleven
  general scenarios and the Luna case (Lu et al.), 466 of 10,000 repositories and
  155 AGENTS.md files (Mohsenimofidi et al.).
- Pi and Hermes details come from the harness study (July 2026 snapshot) and the
  projects' own documentation; Pi Durable from Earendil's announcement
  (1 October 2026). Pi Durable is experimental and its API may change.
- The session → durable → always-on spectrum and the scenario-to-harness table
  (slide 19) are **our synthesis**, labelled as such.
- The 69% token figure is one user's field report (Hermes issue #5563), not a
  benchmark.
''']
for n,(s,m) in enumerate(zip(slides,manifest),1):
    guide.append(f'\n## {n}. {s["title"]}\n\n**Section:** {s["section"]}. **Presenter:** {s["owner"]}.\n\n{plain(s["lead"])}\n')
    if s['layout']=='standard':
        if m['steps']:guide.append(f'\n*Builds:* press Right {m["steps"]} times to complete the figure.\n')
        if DIRECTIONS.get(s['title']):guide.append(f'\n*Do:* {DIRECTIONS[s["title"]]}\n')
        for c in s['cues']:guide.append('\n- '+plain(c))
        guide.append(f'\n\n**Takeaway:** {plain(s["takeaway"])}\n\n**Reading anchor:** {s["source"]}.\n')
    if n<TOTAL:guide.append(f'\n**Next:** {slides[n]["title"]} — {slides[n]["owner"]}.\n')
guide.append('''\n## Sources

- Barbaste, Darrigol, Vu & Wiltberger (2026). *Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents.* arXiv:2609.00006.
- Liu, Lo, Lu, Zhu et al. (2025). *Agent Design Pattern Catalogue.* Journal of Systems and Software 220. arXiv:2405.10467.
- Lu, Zhao, Liu, Zhang et al. (2026). *AgentArcEval: An Architecture Evaluation Method for Foundation Model based Agents.* Journal of Systems and Software 232. arXiv:2510.21031.
- Mohsenimofidi, Galster, Treude & Baltes (2026). *Context Engineering for AI Agents in Open-Source Software.* MSR ’26. arXiv:2510.21413 (CC BY 4.0).
- Earendil (2026). *Pi Durable.* earendil.com/posts/pi-durable (1 October 2026); Pi source: github.com/earendil-works/pi.
- Nous Research. *Hermes Agent* documentation, hermes-agent.nousresearch.com; Alejandro AO (2026), *Hermes Agent Architecture Explained*, alejandro-ao.com.
- Further reading: Koenigstein (2026), *Harness Engineering for AI Agents*; Grootendorst & Alammar, *An Illustrated Guide to AI Agents*; Zechner (2025), “What I learned building an opinionated and minimal coding agent”; Ronacher (2026), “Pi: The Minimal Agent Within OpenClaw”.

All diagrams are original drawings in the lecture's design system; where a
diagram simplifies a paper figure, the slide says so.
''')
md='\n'.join(guide);(OUT/'day2-presenter-guide.md').write_text(md)
guide_css=FONTS+"\n@page{size:A4;margin:19mm 18mm 20mm}body{font:11pt/1.45 'Source Sans 3';color:#242421;max-width:900px;margin:32px auto}h1{font:600 32pt/1.08 'Cormorant Garamond'}h2{font:600 21pt/1.15 'Cormorant Garamond';margin-top:1.2em;break-after:avoid}p,li{orphans:3;widows:3}li{margin:.25em 0}table{width:100%;border-collapse:collapse;font-size:10pt}td,th{padding:5px 8px;border-bottom:1px solid #ddd;text-align:left}a{color:#a62c40}strong{font-weight:600}code{font-family:'IBM Plex Mono';font-size:9.5pt}@media print{body{margin:0;max-width:none}}"
converted=subprocess.run(['pandoc','-f','gfm','-t','html5'],input=md,text=True,check=True,capture_output=True).stdout
(OUT/'day2-presenter-guide.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Agentic AI Architecture — Presenter Guide</title><style>'+guide_css+'</style><body>'+converted+'</body></html>')
print(f'{TOTAL} slides; {sum(bool(m["steps"]) for m in manifest)} built diagrams → {OUT}')
