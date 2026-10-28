"""Shared offline deck theme, browser controller and SVG primitives.

Importing this module reads local theme assets but never generates files.
"""


from pathlib import Path


from html import escape as esc


from visual_marks import component_mark


ROOT = Path(__file__).resolve().parents[1]


FONTS = (ROOT / 'assets/fonts/embedded.css').read_text().replace('data:font/woff2', 'data:font/ttf')


BASE = (ROOT / 'theme/viewport-base.css').read_text()


MOTION = (ROOT / 'theme/diagram-motion.js').read_text()


def text(x, y, value, cls='node-title', anchor='start'):
    value={'Approved M1':'Approved model (M1)', 'Candidate M2':'Candidate model (M2)'}.get(value,value)
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>'


def group(body, step, label):
    return f'<g data-motion-item data-step="{step}" aria-label="{esc(label)}">{body}</g>'


def node(x, y, w, h, title, lines, role='data', tag=''):
    body = f'<g data-node="{esc(title)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" class="node {role}"/>'
    body += component_mark(title,role,x,y,w,h)
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


def controls(count):
    # Preserve the canonical controller contract but suppress all playback chrome.
    buttons=''.join(f'<button type="button" tabindex="-1" data-motion-action="{action}">{label}</button>' for action,label in [('prev','Previous'),('play','Play'),('pause','Pause'),('next','Next'),('replay','Replay')])
    return f'<div data-motion-controls hidden aria-hidden="true">{buttons}<span data-motion-step-label>{count}</span></div><p class="sr-only" data-motion-status role="status" aria-live="polite" aria-atomic="true"></p>'


JS=r'''
/* === FRONTEND SLIDES: STAGE, KEYBOARD, TOUCH, AND LOCAL EDITING === */
class SlidePresentation {
 constructor(){this.slides=[...document.querySelectorAll('.slide')];this.current=0;this.editing=false;this.static=new URLSearchParams(location.search).get('motion')==='static';this.scale();window.addEventListener('resize',()=>this.scale());this.bind();this.show(Math.max(0,Number(location.hash.slice(1))-1)||0);}
 scale(){const f=Math.min(innerWidth/1920,innerHeight/1080);document.querySelector('.deck-stage').style.transform=`translate(${(innerWidth-1920*f)/2}px,${(innerHeight-1080*f)/2}px) scale(${f})`;}
 show(i,complete=false){this.current=Math.max(0,Math.min(this.slides.length-1,i));this.slides.forEach((s,n)=>{s.classList.toggle('active',n===this.current);s.classList.toggle('visible',n===this.current);s.setAttribute('aria-hidden',String(n!==this.current));});const root=this.slides[this.current].querySelector('[data-motion-root]');if(root&&!root.dataset.motionState){root.querySelector('[data-motion-action="pause"]').click();const current=Number(root.dataset.stepCurrent),target=complete?Number(root.dataset.stepCount):0;for(let j=0;j<Math.abs(target-current);j++)root.querySelector(`[data-motion-action="${target>current?'next':'prev'}"]`).click();}history.replaceState(null,'','#'+(this.current+1));}
 advance(dir){const root=this.slides[this.current].querySelector('[data-motion-root]');if(root&&!this.static&&!root.dataset.motionState){const step=Number(root.dataset.stepCurrent),count=Number(root.dataset.stepCount);if((dir>0&&step<count)||(dir<0&&step>0)){root.querySelector(`[data-motion-action="${dir>0?'next':'prev'}"]`).click();return;}}this.show(this.current+dir,dir<0);}
 toggleEdit(){this.editing=!this.editing;document.body.classList.toggle('editing',this.editing);document.querySelectorAll('[data-edit]').forEach(e=>{e.contentEditable=String(this.editing);});}
 save(){const clone=document.documentElement.cloneNode(true);clone.querySelector('body').classList.remove('editing');clone.querySelectorAll('[contenteditable]').forEach(e=>e.removeAttribute('contenteditable'));clone.querySelectorAll('[data-motion-root]').forEach(r=>{r.classList.remove('motion-ready');r.dataset.frame='static';});const a=document.createElement('a');a.href=URL.createObjectURL(new Blob(['<!doctype html>'+clone.outerHTML],{type:'text/html'}));a.download='presentation-edited.html';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
 bind(){document.addEventListener('keydown',e=>{if(e.key==='Escape'&&this.editing){this.toggleEdit();return;}if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();this.save();return;}if(e.ctrlKey||e.metaKey||e.altKey||e.target.isContentEditable||e.target.closest('input,textarea,select,button,a'))return;if(e.key.toLowerCase()==='e'){this.toggleEdit();return;}if(e.key.toLowerCase()==='f'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();return;}const actions={ArrowRight:()=>this.advance(1),ArrowDown:()=>this.advance(1),' ':()=>this.advance(1),ArrowLeft:()=>this.advance(-1),ArrowUp:()=>this.advance(-1),PageDown:()=>this.show(this.current+1),PageUp:()=>this.show(this.current-1,true),Home:()=>this.show(0),End:()=>this.show(this.slides.length-1)};if(actions[e.key]){e.preventDefault();e.stopImmediatePropagation();actions[e.key]();}},true);
 let start=null;document.addEventListener('touchstart',e=>{if(!this.editing)start=e.touches[0].clientX;},{passive:true});document.addEventListener('touchend',e=>{if(start===null)return;const dx=e.changedTouches[0].clientX-start;if(Math.abs(dx)>50)this.advance(dx<0?1:-1);start=null;},{passive:true});let last=0;document.addEventListener('wheel',e=>{if(!this.editing&&Math.abs(e.deltaY)>30&&Date.now()-last>600){this.advance(e.deltaY>0?1:-1);last=Date.now();}},{passive:true});}
}
window.deck=new SlidePresentation();
'''
