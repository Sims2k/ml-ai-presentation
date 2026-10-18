"""Three review slides for the agreed lecture redesign, separate from the full deck.

Diagram Design: authored SVG geometry, semantic lanes, orthogonal paths, accessible
figures, canonical motion controller. Frontend Slides: embedded fixed-stage deck.
The user explicitly requests keyboard-only presentation: playback UI is hidden.
"""
from pathlib import Path
from html import escape as esc
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
OUT.mkdir(parents=True, exist_ok=True)
FONTS = (ROOT / 'assets/fonts/embedded.css').read_text().replace('data:font/woff2', 'data:font/ttf')
BASE = (ROOT / 'theme/viewport-base.css').read_text()
MOTION = (ROOT / 'theme/diagram-motion.js').read_text()

def text(x, y, value, cls='node-title', anchor='start'):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>'

def group(body, step, label):
    return f'<g data-motion-item data-step="{step}" aria-label="{esc(label)}">{body}</g>'

def node(x, y, w, h, title, lines, role='data', tag=''):
    body = f'<g data-node="{esc(title)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" class="node {role}"/>'
    if tag:
        body += text(x + 16, y + 26, tag, 'node-tag')
    body += text(x + 16, y + (36 if h == 92 else 62), title)
    for i, line in enumerate(lines):
        body += text(x + 16, y + (68 if h == 92 else 102) + i * 32, line, 'node-sub')
    return body + '</g>'

def arrow(slug, x1, y1, x2, y2, dashed=False):
    assert x1 == x2 or y1 == y2
    return f'<path d="M{x1} {y1} L{x2} {y2}" class="edge" marker-end="url(#{slug}-arrow)"'+(' stroke-dasharray="6 5"' if dashed else '')+'/>'

def svg(slug, title, desc, body):
    return f'<svg viewBox="0 0 1120 640" role="img" aria-labelledby="{slug}-title {slug}-desc"><title id="{slug}-title">{esc(title)}</title><desc id="{slug}-desc">{esc(desc)}</desc><defs><marker id="{slug}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M1 1 L9 5 L1 9" fill="none" stroke="#696b68" stroke-width="1.5"/></marker></defs>{body}</svg>'

def architecture():
    s='architecture'
    body='<rect x="8" y="12" width="1104" height="268" rx="6" class="zone"/>'
    body+=text(28,48,'TRAINING · LEARN AND APPROVE A MODEL','lane-title')
    body+='<rect x="8" y="340" width="1104" height="244" rx="6" class="zone production"/>'
    body+=text(28,376,'PRODUCTION · APPLY THE APPROVED MODEL','lane-title')
    # All connectors precede nodes; there are no crossing paths or off-axis ports.
    body+=arrow(s,216,172,248,172)+arrow(s,440,172,472,172)
    body+=arrow(s,568,248,568,420,True)
    body+='<rect x="584" y="296" width="184" height="30" fill="#faf9f7"/>'+text(592,318,'APPROVED M1','edge-label')
    for a,b in [(216,248),(440,472),(664,696),(888,920)]:
        body+=arrow(s,a,492,b,492)
    body+=group(node(24,96,192,152,'History',['Past features','+ churn labels'],'data','INPUT'),1,'Historical features and observed labels')
    body+=group(node(248,96,192,152,'Train / test',['Learn a model','Evaluate quality'],'model','LEARNING'),1,'Train and evaluate a candidate')
    body+=group(node(472,96,192,152,'Registry',['Version + lineage','Approval status'],'model','ARTIFACT'),2,'Approve and register a model')
    body+=text(708,142,'Labels describe what happened.','aside-title')
    body+=text(708,178,'Features describe the customer','aside-sub')
    body+=text(708,212,'at the scoring cutoff.','aside-sub')
    body+=group(node(24,420,192,144,'Sources',['Bank / CRM / app'],'data','RECORDS'),3,'Read current bank records')
    body+=group(node(248,420,192,144,'Features',['Validate + prepare'],'data','INPUTS'),3,'Validate and compute features')
    body+=group(node(472,420,192,144,'Score',['Run approved M1'],'model','INFERENCE'),4,'Run the approved model')
    body+=group(node(696,420,192,144,'Score store',['Risk + version links'],'data','RESULTS'),4,'Store predictions and their versions')
    body+=group(node(920,420,176,144,'Policy',['Choose action'],'business','BUSINESS'),5,'Choose an eligible business action')
    body+=text(28,620,'DATA / RECORDS','legend data-text')+text(324,620,'MODEL / EXECUTION','legend model-text')+text(692,620,'BUSINESS RULES / ACTION','legend business-text')
    return svg(s,'From a trained model to an ML system','Historical features and churn labels support training and approval; production validates current features, scores with the approved model, stores results, and applies a separate business policy.',body),5

def serving():
    s='serving';body=''
    rows=[(12,'01  BATCH','Precompute many predictions','Scheduled job',['Customer snapshot'],'Score + save',['Many customers'],'Campaign',['Read saved scores'],'Fits monthly churn'),
          (216,'02  SYNCHRONOUS','Caller waits for a prediction','Application',['Send request'],'Prediction API',['Score this request'],'Application',['Use response'],'Latency in request path'),
          (420,'03  ASYNCHRONOUS','Producer does not wait for the score','Producer',['Publish an event'],'Queue + worker',['Process later'],'Consumer',['Use result event'],'Buffer and retry work')]
    # Each row is its own legible three-node architecture, nine nodes total.
    for step,(y,heading,sub,a,al,b,bl,c,cl,note) in enumerate(rows,1):
        content=f'<rect x="8" y="{y}" width="1104" height="188" rx="6" class="zone"/>'
        content+=text(28,y+32,heading,'lane-title')+text(28,y+62,sub,'row-description')
        cy=y+128
        content+=arrow(s,312,cy,432,cy,step==3)+arrow(s,712,cy,832,cy,step==3)
        for xx,label in [(372,'SCORE' if step==1 else 'REQUEST' if step==2 else 'EVENT'),(772,'READ' if step==1 else 'RESPONSE' if step==2 else 'RESULT')]:
            content+=f'<rect x="{xx-54}" y="{cy-48}" width="108" height="28" fill="#faf9f7"/>'+text(xx,cy-28,label,'edge-label','middle')
        content+=node(28,y+80,284,92,a,al,'data')
        content+=node(432,y+80,280,92,b,bl,'model')
        content+=node(832,y+80,260,92,c,cl,'business')
        # Compact nodes use an explicit two-line type treatment.
        content=content.replace(f'y="{y+138}" class="node-title"',f'y="{y+116}" class="node-title"').replace(f'y="{y+168}" class="node-sub"',f'y="{y+148}" class="node-sub"')
        body+=group(content,step,heading[4:]+': '+sub)
    return svg(s,'Batch, synchronous, and asynchronous serving','Batch stores scores for later use; synchronous serving returns a prediction to a waiting caller; asynchronous serving separates event production, processing, and consumption.',body),3

def drift():
    s='drift';body=''
    # Two separate comparisons; every numeric shape is schematic, not bank data.
    body+='<rect x="8" y="12" width="1104" height="288" rx="6" class="zone"/>'
    body+=text(28,46,'DATA DRIFT · THE INPUT MIX CHANGES','lane-title')
    top=''
    for off,title,values in [(0,'Reference customers',[2,4,7,9]),(556,'Current customers',[9,7,4,2])]:
        top+=text(off+60,86,title,'plot-title')
        top+=f'<path d="M{off+60} 108 V228 H{off+492}" class="axis"/>'
        top+=text(off+60,120,'Customers','axis-label')+text(off+60,272,'Weekly app activity: low → high','axis-label')
        for i,v in enumerate(values):
            x=off+116+i*84;h=v*11
            top+=f'<rect x="{x}" y="{228-h}" width="48" height="{h}" class="hist {"current" if off else "reference"}"/>'
    body+=group(top,1,'Valid customers now include more low-activity customers')
    body+='<rect x="8" y="320" width="1104" height="292" rx="6" class="zone"/>'
    body+=text(28,354,'CONCEPT DRIFT · THE INPUT–OUTCOME RELATIONSHIP CHANGES','lane-title')
    bottom=''
    for off,title in [(0,'Before a pricing change'),(556,'After a pricing change')]:
        bottom+=text(off+60,394,title,'plot-title')
        bottom+=f'<path d="M{off+60} 420 V548 H{off+492}" class="axis"/>'
        bottom+=text(off+68,442,'Higher churn risk','axis-label')
        bottom+=text(off+60,592,'Weekly app activity: low → high','axis-label')
        bottom+=f'<path d="M{off+120} 452 C{off+200} 460 {off+300} 524 {off+464} 536" class="risk reference"/>'
        if off:
            bottom+=f'<path d="M{off+120} 452 C{off+220} 450 {off+340} 466 {off+464} 476" class="risk current"/>'
            bottom+=text(off+302,514,'New relationship','annotation')
    body+=group(bottom,2,'The same app activity can now imply a different churn risk')
    body+=text(28,630,'SCHEMATIC ONLY · Dashed: reference relationship. Solid: changed relationship. No measured results.','diagram-note')
    return svg(s,'Data drift versus concept drift','The upper comparison changes the customer activity distribution; the lower comparison changes churn risk for the same activity, with a dashed old relationship and solid new relationship.',body),2

CSS=r'''
/* === PAPER & INK: LECTURE TYPOGRAPHY AND SEMANTIC COLORS === */
:root{--slide-bg:#faf9f7;--stage-bg:#dedbd5;--ink:#242421;--muted:#62645f;--accent:#a62c40;--rule:#d5d3cc;--motion-fast:160ms;--motion-step:480ms;--motion-hold:720ms;--motion-total:3600ms}
*{box-sizing:border-box}body{font-family:'Source Sans 3',sans-serif;color:var(--ink)}
.masthead{position:absolute;top:46px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--rule);padding-bottom:18px;font-size:24px}
.course{font-weight:600;letter-spacing:.035em}.speaker{font-size:24px}.speaker b{color:var(--accent)}
.heading{position:absolute;top:112px;left:72px;right:72px}.eyebrow{font-size:21px;letter-spacing:.07em;text-transform:uppercase;color:var(--accent);margin:0 0 8px;font-weight:600}
h1{font:600 76px/1.06 'Cormorant Garamond',serif;margin:0 0 12px;letter-spacing:-.018em}.subtitle{font-size:29px;line-height:1.3;margin:0;color:#565953}
.body-grid{position:absolute;left:72px;right:72px;top:298px;height:602px;display:grid;grid-template-columns:1120px 1fr;gap:48px}
figure{margin:0;width:1120px;height:640px;transform-origin:top left;transform:scale(.94);overflow:visible}
svg{width:1120px;height:640px;max-width:none;max-height:none;overflow:visible;display:block}
.diagram-column{width:1080px;height:602px}.explanation{border-left:1px solid var(--rule);padding-left:32px;height:602px;position:relative;margin-left:-32px}
.explanation h2{font-size:25px;letter-spacing:.025em;margin:0 0 14px;font-weight:600}
.explanation ul{margin:0;padding-left:25px;font-size:28px;line-height:1.32}.explanation li{padding-left:3px;margin:0 0 16px}.explanation li::marker{color:var(--accent);font-size:19px}.explanation b{font-weight:600}
.takeaway{margin-top:16px;padding-top:14px;border-top:1px solid var(--rule);font-size:25px;line-height:1.3;color:#454943}
.example{position:absolute;left:72px;right:72px;top:926px;height:90px;display:grid;grid-template-columns:190px 1fr;gap:22px;align-items:center;border-top:2px solid #a62c40;border-bottom:1px solid var(--rule);background:#f3f0ea;padding:12px 20px}
.example-label{font-size:21px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:.04em}.example p{font-size:27px;line-height:1.25;margin:0}.example strong{font-weight:600}
footer{position:absolute;bottom:25px;left:72px;right:72px;display:flex;justify-content:space-between;gap:20px;font-size:19px;color:#60635e}.folio{white-space:nowrap;color:#242421}
/* === DIAGRAM DESIGN: LANES, TYPES, PORTS AND LABELS === */
.zone{fill:#f1f0eb;stroke:#d4d4cc;stroke-width:1.4}.zone.production{fill:#f6f5f0}.lane-title{font:600 20px 'Source Sans 3';letter-spacing:.8px;fill:#454a43}
.node{stroke-width:1.5;fill:#faf9f7}.node.data{fill:#eaf0f2;stroke:#718895}.node.model{fill:#f7edef;stroke:#a62c40}.node.business{fill:#eef2e9;stroke:#71816a}
.node-title{font:600 26px 'Source Sans 3';fill:#242421}.node-sub{font:400 21px 'Source Sans 3';fill:#50574f}.node-tag{font:500 15px 'IBM Plex Mono';fill:#5a6159;letter-spacing:.4px}
.edge{fill:none;stroke:#696b68;stroke-width:1.7}.edge-label{font:500 17px 'IBM Plex Mono';fill:#525a51}
.aside-title{font:600 23px 'Source Sans 3';fill:#3b413a}.aside-sub{font:400 23px 'Source Sans 3';fill:#5d635a}.legend{font:600 17px 'Source Sans 3';letter-spacing:.5px}
.data-text{fill:#526a76}.model-text{fill:#a62c40}.business-text{fill:#53674c}.row-description{font:400 22px 'Source Sans 3';fill:#62665f}
.axis{fill:none;stroke:#969c93;stroke-width:1.2}.plot-title{font:600 23px 'Source Sans 3';fill:#363d35}.axis-label{font:400 20px 'Source Sans 3';fill:#5a6257}
.hist.reference{fill:#87999e;stroke:#536b74;stroke-width:1.2}.hist.current{fill:#d4a4ae;stroke:#a62c40;stroke-width:1.2}
.risk{fill:none;stroke-width:3.2}.risk.reference{stroke:#77858a;stroke-dasharray:8 5}.risk.current{stroke:#a62c40}.annotation{font:italic 600 23px 'Cormorant Garamond';fill:#a62c40}.diagram-note{font:400 17px 'Source Sans 3';fill:#5d645b}
/* === KEYBOARD BUILDS: COMPLETE STATIC SOURCE, NO VISIBLE PLAYBACK UI === */
[data-motion-controls]{display:none!important}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.motion-ready [data-motion-item]{opacity:.12;transform:translateY(6px);transition:opacity var(--motion-step) ease,transform var(--motion-step) ease}
.motion-ready [data-motion-item].is-visible,.motion-ready[data-frame="end"] [data-motion-item],.motion-ready[data-frame="static"] [data-motion-item]{opacity:1;transform:none}
.editing [data-edit]{outline:1px dashed #a62c40;outline-offset:3px}.edit-notice{display:none;position:fixed;top:8px;left:8px;padding:8px 14px;background:#242421;color:#fff;z-index:10000;font:16px 'Source Sans 3'}.editing .edit-notice{display:block}
@media(prefers-reduced-motion:reduce){[data-motion-item]{opacity:1!important;transform:none!important;transition:none!important}}
@page{size:1920px 1080px;margin:0}@media print{[data-motion-item]{opacity:1!important;transform:none!important}.edit-notice{display:none!important}}
'''

SLIDES = [
dict(title='From a trained model to an ML system', section='Block 1 / Foundations', speaker='Ricardo', figure=architecture,
 lead='Training creates an artifact. Architecture connects it to data, operation, and business decisions.',
 bullets=['<b>Features</b> are model inputs; <b>labels</b> describe observed outcomes used for learning.',
          '<b>Training</b> learns and evaluates a candidate. <b>Inference</b> applies an approved model to new inputs.',
          '<b>Two lifecycles:</b> software can change independently of data and model quality.',
          '<b>Separate prediction from action:</b> a risk score does not decide whom the bank contacts.'],
 takeaway='Architecture must preserve compatible inputs, traceable versions, and clear responsibilities.',
 example='<strong>Bank churn:</strong> monthly scoring estimates each customer’s risk of leaving in the next 30 days. Campaign rules decide whether an eligible customer receives an offer.',
 source='Bass, Ch. 14 · Kalinowski, §13.2–13.3 · Diagram adapted for teaching; schedule and horizon are illustrative.'),
dict(title='Serving patterns: when is a prediction needed?', section='Block 1 / Deployment & serving', speaker='Tomás', figure=serving,
 lead='Choose the interaction pattern from the decision’s timing, volume, and failure behavior.',
 bullets=['<b>Batch:</b> compute many predictions on a schedule; consumers use stored results later.',
          '<b>Synchronous:</b> the caller waits, making response time and availability part of its request.',
          '<b>Asynchronous:</b> events decouple producer and consumer; handle retries, lag, and duplicates.',
          '<b>Edge is a location choice.</b> It can use different interaction patterns; it is not a fourth timing mode.'],
 takeaway='Serving pattern, deployment location, and release strategy are separate architecture decisions.',
 example='<strong>Bank churn uses batch:</strong> prepare validated scores before a campaign. A fraud check may need an immediate response—a brief comparison, not a second running case.',
 source='Kalinowski, §13.3–13.4; supporting Ch. 12 · Bank application and diagrams are teaching adaptations.'),
dict(title='Data drift vs. concept drift', section='Block 1 / Monitoring & degradation', speaker='Simon', figure=drift,
 lead='A changing input population and a changing predictive relationship require different evidence.',
 bullets=['<b>Data drift:</b> the mix of valid inputs changes. Compare current data with a reference.',
          '<b>Concept drift:</b> the same inputs imply different churn risk. Check observed outcomes.',
          '<b>Labels arrive later:</b> check inputs now; evaluate quality after the churn window closes.',
          '<b>Diagnose first:</b> missing CRM fields are data-quality faults. An alert does not authorize retraining.'],
 takeaway='Input shift alone does not prove degraded accuracy or concept drift.',
 example='<strong>Bank examples:</strong> a campaign attracts more low-activity customers → data drift. New fees make active customers leave more often → possible concept drift.',
 source='Simon’s study notes, §2–3 · Bass, Ch. 11 / §14.1.5 · Kalinowski, §13.2 · Schematic examples; no measured results.'),
]

def controls(count):
    # Preserve the canonical controller contract but suppress all playback chrome.
    buttons=''.join(f'<button type="button" tabindex="-1" data-motion-action="{action}">{label}</button>' for action,label in [('prev','Previous'),('play','Play'),('pause','Pause'),('next','Next'),('replay','Replay')])
    return f'<div data-motion-controls hidden aria-hidden="true">{buttons}<span data-motion-step-label>{count}</span></div><p class="sr-only" data-motion-status role="status" aria-live="polite" aria-atomic="true"></p>'

pages=[]
for number,item in enumerate(SLIDES,1):
    drawing,count=item['figure']()
    bullets=''.join(f'<li data-edit>{b}</li>' for b in item['bullets'])
    pages.append(f'''<section class="slide {'active visible' if number==1 else ''}" id="sample-{number}" aria-label="{number}. {esc(item['title'])}">
    <header class="masthead"><span class="course">ML ARCHITECTURE</span><span class="speaker">Presenter: <b>{esc(item['speaker'])}</b></span></header>
    <div class="heading"><p class="eyebrow">{esc(item['section'])}</p><h1 data-edit>{esc(item['title'])}</h1><p class="subtitle" data-edit>{esc(item['lead'])}</p></div>
    <div class="body-grid"><div class="diagram-column"><figure data-motion-root data-motion-mode="step" data-step-count="{count}" data-step-current="{count}" data-frame="static" data-static-frame="complete">{drawing}{controls(count)}</figure></div>
    <aside class="explanation"><h2>Key concepts</h2><ul>{bullets}</ul><p class="takeaway" data-edit>{esc(item['takeaway'])}</p></aside></div>
    <div class="example"><span class="example-label">Bank example</span><p data-edit>{item['example']}</p></div>
    <footer><span>{esc(item['source'])}</span><span class="folio">{number:02d} / 03</span></footer>
    </section>''')

JS=r'''
/* === FRONTEND SLIDES: STAGE, KEYBOARD, TOUCH, AND LOCAL EDITING === */
class SlidePresentation {
 constructor(){this.slides=[...document.querySelectorAll('.slide')];this.current=0;this.editing=false;this.static=new URLSearchParams(location.search).get('motion')==='static';this.scale();window.addEventListener('resize',()=>this.scale());this.bind();this.show(Math.max(0,Number(location.hash.slice(1))-1)||0);}
 scale(){const f=Math.min(innerWidth/1920,innerHeight/1080);document.querySelector('.deck-stage').style.transform=`translate(${(innerWidth-1920*f)/2}px,${(innerHeight-1080*f)/2}px) scale(${f})`;}
 show(i,complete=false){this.current=Math.max(0,Math.min(this.slides.length-1,i));this.slides.forEach((s,n)=>{s.classList.toggle('active',n===this.current);s.classList.toggle('visible',n===this.current);s.setAttribute('aria-hidden',String(n!==this.current));});const root=this.slides[this.current].querySelector('[data-motion-root]');if(root&&!root.dataset.motionState){root.querySelector('[data-motion-action="pause"]').click();const current=Number(root.dataset.stepCurrent),target=complete?Number(root.dataset.stepCount):0;for(let j=0;j<Math.abs(target-current);j++)root.querySelector(`[data-motion-action="${target>current?'next':'prev'}"]`).click();}history.replaceState(null,'','#'+(this.current+1));}
 advance(dir){const root=this.slides[this.current].querySelector('[data-motion-root]');if(root&&!this.static&&!root.dataset.motionState){const step=Number(root.dataset.stepCurrent),count=Number(root.dataset.stepCount);if((dir>0&&step<count)||(dir<0&&step>0)){root.querySelector(`[data-motion-action="${dir>0?'next':'prev'}"]`).click();return;}}this.show(this.current+dir,dir<0);}
 toggleEdit(){this.editing=!this.editing;document.body.classList.toggle('editing',this.editing);document.querySelectorAll('[data-edit]').forEach(e=>{e.contentEditable=String(this.editing);});}
 save(){const clone=document.documentElement.cloneNode(true);clone.querySelector('body').classList.remove('editing');clone.querySelectorAll('[contenteditable]').forEach(e=>e.removeAttribute('contenteditable'));clone.querySelectorAll('[data-motion-root]').forEach(r=>{r.classList.remove('motion-ready');r.dataset.frame='static';});const a=document.createElement('a');a.href=URL.createObjectURL(new Blob(['<!doctype html>'+clone.outerHTML],{type:'text/html'}));a.download='lecture-redesign-edited.html';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
 bind(){document.addEventListener('keydown',e=>{if(e.key==='Escape'&&this.editing){this.toggleEdit();return;}if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();this.save();return;}if(e.ctrlKey||e.metaKey||e.altKey||e.target.isContentEditable||e.target.closest('input,textarea,select,button,a'))return;if(e.key.toLowerCase()==='e'){this.toggleEdit();return;}if(e.key.toLowerCase()==='f'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();return;}const actions={ArrowRight:()=>this.advance(1),ArrowDown:()=>this.advance(1),' ':()=>this.advance(1),ArrowLeft:()=>this.advance(-1),ArrowUp:()=>this.advance(-1),PageDown:()=>this.show(this.current+1),PageUp:()=>this.show(this.current-1,true),Home:()=>this.show(0),End:()=>this.show(this.slides.length-1)};if(actions[e.key]){e.preventDefault();e.stopImmediatePropagation();actions[e.key]();}},true);
 let start=null;document.addEventListener('touchstart',e=>{if(!this.editing)start=e.touches[0].clientX;},{passive:true});document.addEventListener('touchend',e=>{if(start===null)return;const dx=e.changedTouches[0].clientX-start;if(Math.abs(dx)>50)this.advance(dx<0?1:-1);start=null;},{passive:true});let last=0;document.addEventListener('wheel',e=>{if(!this.editing&&Math.abs(e.deltaY)>30&&Date.now()-last>600){this.advance(e.deltaY>0?1:-1);last=Date.now();}},{passive:true});}
}
window.deck=new SlidePresentation();
'''
doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ML Architecture — Lecture redesign</title><style>'+FONTS+'\n'+BASE+'\n'+CSS+'</style></head><body><div class="edit-notice">Editing · Escape to finish · Ctrl/Cmd+S to download</div><div class="deck-viewport"><main class="deck-stage" id="deckStage">'+''.join(pages)+'</main></div><noscript><style>html,body{overflow:auto;height:auto}.deck-viewport,.deck-stage{position:static;overflow:visible;height:auto}.slide{position:relative;visibility:visible;opacity:1;pointer-events:auto}</style></noscript><script data-diagram-controls>'+MOTION+'</script><script>'+JS+'</script></body></html>'
(OUT/'lecture-redesign.html').write_text(doc)
print(OUT/'lecture-redesign.html')

# Standalone diagram sources allow the diagram-specific validator to run without
# confusing a multi-slide frontend deck with a single-figure document.
DIAGRAM_OUT = ROOT / 'assets/diagrams/lecture-redesign'
DIAGRAM_OUT.mkdir(parents=True, exist_ok=True)
for slug, build in [('architecture', architecture), ('serving', serving), ('drift', drift)]:
    drawing, count = build()
    page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+slug+'</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,600&amp;family=Source+Sans+3:wght@400;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap"><style>'+CSS+'\nbody{background:#faf9f7;margin:24px;overflow:auto}main{max-width:1120px;margin:auto}h1{font-size:48px}figure{transform:none;height:auto}.diagram-container{overflow-x:auto}svg{min-width:1120px}header{font-size:18px;margin-bottom:24px}</style></head><body><main><header>ML Architecture</header><h1>'+slug.title()+'</h1><figure data-motion-root data-motion-mode="step" data-step-count="'+str(count)+'" data-step-current="'+str(count)+'" data-frame="static" data-static-frame="complete"><div class="diagram-container">'+drawing+'</div>'+controls(count)+'</figure><noscript><p>The complete static diagram is shown without JavaScript.</p></noscript></main><script data-diagram-controls>'+MOTION+'</script></body></html>'
    (DIAGRAM_OUT / (slug+'.html')).write_text(page)
