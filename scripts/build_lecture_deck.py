"""Build the full topic-led lecture from the approved three-slide direction."""
from pathlib import Path
from html import escape
import re,json,subprocess
from deck_common import FONTS,BASE,MOTION,CSS,JS,controls
from lecture_content import build_lecture
from drift_visuals import DRIFT_CSS
from visual_marks import tool_mark,concept_mark,MARK_CSS

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs'
DIAGRAMS=ROOT/'assets/diagrams/lecture-full';DIAGRAMS.mkdir(parents=True,exist_ok=True)
slides=build_lecture()
EXTRA=r'''
/* === LECTURE COMPARISONS, COVER, AND KEYBOARD CONTENTS === */
.lecture-table{width:1052px;height:602px;padding:12px 0;overflow:visible}
.lecture-table table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:25px;line-height:1.25}
.lecture-table th{font-size:22px;text-align:left;font-weight:600;color:#a62c40;background:#f0ede7;padding:16px 13px;border-bottom:2px solid #c5bdb0}
.lecture-table td{padding:15px 13px;border-bottom:1px solid #d5d3cc;vertical-align:top;overflow-wrap:break-word}
.lecture-table tbody tr:nth-child(even){background:#f4f3ef}.lecture-table td:first-child{font-weight:600}
.agenda .lecture-table table{font-size:24px}.agenda .lecture-table td{padding:11px 13px}
.long-title h1{font-size:66px}.heading h1{white-space:nowrap}
.cover .heading{top:214px;right:560px}.cover h1{font:500 144px/1.04 'Cormorant Garamond';letter-spacing:-.04em;white-space:normal}
.cover .subtitle{font-size:36px;line-height:1.4;max-width:1050px;margin-top:30px}
.cover .cover-side{position:absolute;top:286px;right:82px;width:374px;border-left:1px solid #c9c5ba;padding-left:36px;font:500 46px/1.2 'Cormorant Garamond'}
.cover .cover-side p{font:28px/1.5 'Source Sans 3';margin-top:32px}
.cover .cover-speakers{position:absolute;left:72px;top:850px;font-size:29px;line-height:1.5}
.cover .cover-speakers small{display:block;color:#a62c40;font-size:22px;letter-spacing:.06em;margin-bottom:12px}
#contents{position:fixed;inset:0;z-index:20000;background:#faf9f7;overflow:auto;padding:36px 5vw;font-family:'Source Sans 3'}
#contents[hidden]{display:none}#contents h2{font:48px 'Cormorant Garamond';margin:0 0 8px}#contents p{font-size:18px}
.contents-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:8px;margin-top:24px}.contents-grid button{cursor:pointer;font:19px/1.3 'Source Sans 3';text-align:left;background:transparent;border:1px solid #d5d3cc;padding:12px 16px;color:#242421}.contents-grid button small{display:block;color:#a62c40;font-size:14px;margin-bottom:5px}
button:focus-visible{outline:3px solid #a62c40;outline-offset:2px}
@media print{#contents{display:none!important}}
'''
EXTRA+=DRIFT_CSS
EXTRA+=MARK_CSS
pages=[];manifest=[];guide=[]
old=(ROOT/'src/presenter-guide-source.md').read_text();pieces=re.split(r'^### (\d+)\. (.+)$',old,flags=re.M)
notes={int(pieces[i]):pieces[i+2].strip().split('\n## ')[0] for i in range(1,len(pieces),3)}

guide.append('''# ML Architecture — Presenter Guide

English, topic-led lecture for a software engineering master's class. This guide
matches the revised slide numbering. It supersedes the earlier incident-led
speaking sequence. Slide count supports explanation; no fixed one-hour total is
imposed. Coordinate actual speaking time with the group before delivery.

## Shared example and boundaries

Bass Chapter 14 supplies the bank customer-churn setting. Monthly scoring, the
next-30-day target, Ana/C042, login counts, the illustrative 0.70 score, M1/M2,
the CRM migration and B017/B017-R1 are teaching choices. No actual customer
outcome, repaired score, retention benefit, or executed tool run is reported.

The missing CRM feature is a data-quality fault, not automatically concept drift.
The complete failed B017 batch is held before publication. A separately validated
repaired execution B017-R1 can retain M1. Training and production promotion are
separate decisions. Prediction and business action remain separate responsibilities.
M1 identifies the current approved model; M2 identifies a candidate replacement.
The identifiers stay attached to those artifacts even if their approval status changes.

## Presenting and editing

Arrow Right/Space advances a diagram build, then the slide; Arrow Left reverses.
Page Down/Page Up changes slides directly. G opens contents; Escape closes it.
F toggles fullscreen. E toggles local text editing; Escape finishes editing;
Ctrl/Cmd+S downloads the edited HTML. Browser edits are not synchronized to other
laptops. The PDF and `?motion=static` show complete figures. Reduced motion also
uses complete diagrams. No visible animation-playback controls are shown.

## Section ownership

| Section | Presenter |
| --- | --- |
| Foundations | Ricardo |
| Deployment and serving | Tomás |
| Monitoring and degradation | Simon |
| Design decisions | Luca |
| Architectural tactics | Matheus |
| DevOps/MLOps | Matheus |
| Security and privacy | Simon + Matheus |
| Quality checklist | Matheus |
| Practical tools | Matheus |

Assignments follow the colleagues’ reviewed Google deck. Statistical derivations
are outside the scope of this lecture.
''')

for n,s in enumerate(slides,1):
    visual=s['visual'];count=0
    if callable(visual):visual,count=visual()
    title=escape(s['title']);owner=escape(s['owner']);section=escape(s['section'])
    mark=tool_mark(s);icon=concept_mark(s)
    if n==1:
        inner=f'''<header class="masthead"><span class="course">SOFTWARE ENGINEERING MASTERCLASS</span><span>20 October 2026</span></header><div class="heading"><p class="eyebrow">Architecture of ML-enabled systems</p><h1>ML<br>Architecture.</h1><p class="subtitle">From prediction to production.<br>A bank customer-churn case.</p></div><aside class="cover-side">A model becomes useful<br>inside a system.<p>Data and feature pipelines.<br>Serving and monitoring.<br>Controlled change and quality.</p></aside><div class="cover-speakers"><small>PRESENTERS</small>Ricardo · Tomás · Simon · Luca · Matheus</div><footer><span>Based on the assigned readings and the bank customer-churn case.</span><span class="folio">01 / {len(slides):02d}</span></footer>'''
    else:
        is_svg=visual.startswith('<svg')
        if is_svg:
            visual=f'<figure data-motion-root data-motion-mode="step" data-step-count="{count}" data-step-current="{count}" data-frame="static" data-static-frame="complete">{visual}{controls(count)}</figure>'
            slug=re.search(r'<title id="([^"]+)-title"',visual).group(1)
            standalone=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,600&amp;family=Source+Sans+3:wght@400;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap"><style>{CSS}{DRIFT_CSS} body{{background:#faf9f7;margin:24px;overflow:auto}}main{{max-width:1776px;margin:auto}}h1{{font-size:48px}}figure{{transform:none;height:auto}}.diagram-container{{overflow-x:auto}}svg{{min-width:{1776 if s.get('layout')=='wide' else 1120}px;width:{1776 if s.get('layout')=='wide' else 1120}px}}figure{{width:{1776 if s.get('layout')=='wide' else 1120}px}}</style></head><body><main><h1>{title}</h1><div class="diagram-container">{visual}</div><noscript><p>The complete static diagram is shown without JavaScript.</p></noscript><p>{escape(s["source"])}</p></main><script data-diagram-controls>{MOTION}</script></body></html>'
            (DIAGRAMS/f'{slug}.html').write_text(standalone)
        bullets=''.join(f'<li data-edit>{v}</li>' for v in s['bullets'])
        inner=f'''<header class="masthead"><span class="course">ML ARCHITECTURE{mark}</span><span class="speaker">Presenter: <b>{owner}</b></span></header><div class="heading"><p class="eyebrow">{section}</p><h1 data-edit>{title}</h1><p class="subtitle" data-edit>{escape(s['lead'])}</p></div><div class="body-grid"><div class="diagram-column">{visual}</div><aside class="explanation"><h2>{icon}Key concepts</h2><ul>{bullets}</ul><p class="takeaway" data-edit>{escape(s['takeaway'])}</p></aside></div><div class="example"><span class="example-label">{escape(s.get("example_label","Bank example"))}</span><p data-edit>{escape(s['example'])}</p></div><footer><span>{escape(s['source'])}</span><span class="folio">{n:02d} / {len(slides):02d}</span></footer>'''
    if s.get('layout')=='wide':
        inner=re.sub(r'<aside class="explanation">.*?</aside>', '', inner, flags=re.S)
    classes=('wide ' if s.get('layout')=='wide' else '')+('cover ' if n==1 else '')+('agenda ' if n==2 else '')+('long-title ' if len(s['title'])>48 else '')+('active visible' if n==1 else '')
    edit_index=iter(range(100))
    inner=re.sub(r' data-edit(?=[ >])',lambda _:f' id="lecture-edit-{n}-{next(edit_index)}" data-edit',inner)
    pages.append(f'<section class="slide {classes}" id="lecture-{n}" aria-label="{n}. {title}">{inner}</section>')
    manifest.append(dict(number=n,title=s['title'],section=s['section'],owner=s['owner'],steps=count,kind='cover' if n==1 else 'diagram' if count else 'image' if s.get('layout')=='wide' else 'table',layout=s.get('layout','standard'),source=s['source']))
    guide.append(f'\n## {n}. {s["title"]}\n\n**Section:** {s["section"]}. **Presenter:** {s["owner"]}.\n\n{s["lead"]}\n')
    for b in s['bullets']:guide.append('\n- '+re.sub(r'</?b>','**',b))
    if s.get('extra'):guide.append('\n\n**Figure explanation:** '+s['extra']+'\n')
    guide.append(f'\n\n**Bank example:** {s["example"]}\n\n**Teaching point:** {s["takeaway"]}\n')
    # Preserve explanatory source context, not obsolete timings/diagram directions.
    custom_context={
        'Data drift: a different customer mix': 'Read the bin labels first: 0, 1–2, 3–5, and 6+ app logins in the same seven-day window. Each bar is a count within a fictional 100-customer cohort; this is a categorical proportion comparison, not a measured bank distribution. The current cohort contains more low-activity customers. Input evidence alone can establish this change, without knowing whether those customers later churned. It does not establish whether model errors increased. Reference selection and cohort comparability matter as much as the comparison method.',
        'Concept drift: a different relationship': 'Explain both axes and the legend first: app logins and products used are inputs; circles and triangles are mature observed outcomes. The same 15 positions are used twice to isolate a changed relationship. The gray dashed M1 boundary stays fixed in both panels. The solid line illustrates the changed outcome relationship, not an automatically deployed replacement. These deliberately simplified examples are invented and do not claim measured bank performance.',
        'Monitoring architecture: from signal to response': 'Start with the three evidence sources. Input quality and run health can be assessed immediately; predictive quality requires outcomes linked back to the original prediction context. The evidence store represents linked logs, metrics and reports, not a required single product. Alert routing brings a defined condition to a named owner. That owner reviews the supporting evidence and selects a controlled response. Review authority does not bypass the separate release policy.',
        'Predictive quality and system performance': 'Precision asks how many flagged customers actually churned; recall asks how many actual churners were found. Calibration asks whether predicted risks agree with observed outcome rates in an appropriate evaluation. These measures answer different questions and need reliable mature labels. The batch deadline and operating cost are system measures, so they can be assessed separately from future churn quality. Do not invent numerical thresholds or claim an evaluated winner between models.',
    }
    if s['title'] in custom_context:
        guide.append('\n**Additional speaking context:**\n\n'+custom_context[s['title']])
    elif s['ref'] in notes and s['ref'] not in (1,6):
        pars=notes[s['ref']].split('\n\n')
        selected=[p for p in pars if p and not p.startswith('**') and not p.startswith('#') and 'Visual/build' not in p and 'Transition:' not in p and 'Handoff' not in p]
        if selected:guide.append('\n**Additional speaking context:**\n\n'+'\n\n'.join(selected[:2]))
    guide.append(f'\n\n**Reading anchor:** {s["source"]}.\n')
    if n<len(slides):guide.append(f'\n**Next:** {slides[n]["title"]} — {slides[n]["owner"]}.\n')

contents=''.join(f'<button type="button" data-jump="{m["number"]-1}"><small>{m["number"]:02d} · {escape(m["owner"])}</small>{escape(m["title"])}</button>' for m in manifest)
contents='<nav id="contents" aria-label="Lecture contents" hidden><h2>ML Architecture</h2><p>Choose a slide. Press G or Escape to return.</p><div class="contents-grid">'+contents+'</div></nav>'
NAV=r'''
/* === KEYBOARD CONTENTS: HIDDEN OUTSIDE REVIEW === */
const contents=document.getElementById('contents');let contentsOrigin=null;
// Text edits persist only in this browser; the download contains the edited text.
const editStorageKey='ml-architecture-lecture-v3';
try{const edits=JSON.parse(localStorage.getItem(editStorageKey)||'{}');document.querySelectorAll('[data-edit]').forEach(e=>{if(typeof edits[e.id]==='string')e.textContent=edits[e.id];});}catch{}
document.addEventListener('input',e=>{if(!e.target.matches('[data-edit]'))return;try{const edits=JSON.parse(localStorage.getItem(editStorageKey)||'{}');edits[e.target.id]=e.target.textContent;localStorage.setItem(editStorageKey,JSON.stringify(edits));}catch{}});
function toggleContents(){const open=contents.hidden;contents.hidden=!open;if(open){contentsOrigin=document.activeElement;contents.querySelector('button').focus();}else if(contentsOrigin&&contentsOrigin!==document.body){contentsOrigin.focus();}else{document.activeElement.blur();}}
document.addEventListener('keydown',e=>{if(e.target.isContentEditable)return;if(e.key.toLowerCase()==='g'){e.preventDefault();toggleContents();}if(e.key==='Escape'&&!contents.hidden){e.preventDefault();toggleContents();}});
contents.addEventListener('click',e=>{const b=e.target.closest('[data-jump]');if(b){deck.show(Number(b.dataset.jump));contentsOrigin=null;toggleContents();}});
'''
# Exported HTML must initialize from complete source and preserve all deck behavior.
deckjs=JS.replace('presentation-edited.html','ml-architecture-lecture-edited.html')
doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ML Architecture — Topic-led lecture</title><style>'+FONTS+'\n'+BASE+'\n'+CSS+'\n'+EXTRA+'</style></head><body><div class="edit-notice">Editing · Escape to finish · Ctrl/Cmd+S to download</div><div class="deck-viewport"><main class="deck-stage" id="deckStage">'+''.join(pages)+'</main></div>'+contents+'<noscript><style>html,body{overflow:auto;height:auto}.deck-viewport,.deck-stage{position:static;overflow:visible;height:auto}.slide{position:relative;visibility:visible;opacity:1;pointer-events:auto}</style><p>All complete slides are shown without JavaScript.</p></noscript><script data-diagram-controls>'+MOTION+'</script><script>'+deckjs+NAV+'</script></body></html>'
(OUT/'ml-architecture-lecture.html').write_text(doc)
(OUT/'lecture-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
guide.append('''\n## Source and adaptation notes

The inspected reading locations and limitations are recorded in SOURCES.md.
Kalinowski Chapters 13–14 supply the assigned architecture and design material;
Chapter 12 and §§16.3–16.5 are supporting reading, not silently relabeled assigned
chapters. Bass Chapters 9–11 and 14 supply security, privacy, observability and the
banking case. Nazir references are selected decision/discussion excerpts rather
than a fresh complete paper read. Published Bucaioni Table 1 was spot-checked on
PDF pages 6–7. Its separately catalogued corrigendum has not been read.

Selected checklist codes are part of a larger checklist. SMN3 concerns input
monitoring; SA1 recovery; SS5 cyberattack defense; SS6 safety/fairness; SP1 privacy
considerations. Ordinary input completeness checks alone do not establish cyber
defense. A checklist prompt, SHAP/LIME attribution, federated learning, or a token
does not by itself prove fairness, causality, compliance, or a privacy guarantee.

All architecture figures are teaching syntheses, not exact book-figure copies.
Data-drift counts and concept-drift curves are schematic invented illustrations.
Airflow and MLflow records are prepared explanations, not observed tool runs.
No new full-text source checks or new experimental results are claimed by this
visual reorganization. Mathematical detail remains in the separate personal notes.
''')
md='\n'.join(guide);(OUT/'lecture-presenter-guide.md').write_text(md)
guide_css=FONTS+"\n@page{size:A4;margin:19mm 18mm 20mm}body{font:11pt/1.45 'Source Sans 3';color:#242421;max-width:900px;margin:32px auto}h1{font:600 32pt/1.08 'Cormorant Garamond'}h2{font:600 21pt/1.15 'Cormorant Garamond';margin-top:1.2em;break-after:avoid}h3{break-after:avoid}p,li{orphans:3;widows:3}li{margin:.25em 0}table{width:100%;border-collapse:collapse;font-size:10pt}td,th{padding:5px 8px;border-bottom:1px solid #ddd;text-align:left}a{color:#a62c40}strong{font-weight:600}@media print{body{margin:0;max-width:none}}"
converted=subprocess.run(['pandoc','-f','gfm','-t','html5'],input=md,text=True,check=True,capture_output=True).stdout
(OUT/'lecture-presenter-guide.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ML Architecture — Presenter Guide</title><style>'+guide_css+'</style><body>'+converted+'</body></html>')
print(f'{len(slides)} topic-led slides; '+str(sum(bool(m['steps']) for m in manifest))+' diagrams; no fixed total time.')
