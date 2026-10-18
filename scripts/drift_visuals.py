"""Large lecture figures: time patterns, input change, and changed relationships.

The temporal-pattern figure is a redrawn schematic after Krawczyk & Cano (2018),
Fig. 2 — not a reproduction of their artwork. All plotted bank examples are invented.
"""
from pathlib import Path
from html import escape
from build_lecture_samples import group

ROOT=Path(__file__).resolve().parents[1]
POINTS=[(1,1),(2,2),(2,5),(4,1),(4,4),(5,2),(5,5),(7,1),(7,3),(8,5),(9,2),(10,4),(11,1),(12,3),(13,5)]
OLD=lambda x,y:x+2*y<11
NEW=lambda x,y:x+2*y<17

def tx(x,y,s,cls='wide-label',anchor='start'):
    from html import escape
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{escape(str(s))}</text>'

def frame(slug,title,desc,body):
    from html import escape
    return f'<svg viewBox="0 0 1776 640" role="img" aria-labelledby="{slug}-title {slug}-desc"><title id="{slug}-title">{escape(title)}</title><desc id="{slug}-desc">{escape(desc)}</desc>{body}</svg>'

TEMPORAL_ROWS=[
    ('SUDDEN','The old regime switches abruptly.','aaaaaaaabbbbbbbb'),
    ('GRADUAL','Old and new regimes overlap briefly.','aaaabaaaabbabbbb'),
    ('INCREMENTAL','The regime shifts through in-between states.','aaaaammmmmbbbbbb'),
    ('RECURRING','An earlier regime returns, then yields again.','aaaaaabbbaaabbbb'),
    ('BLIPS','Brief noise, not a lasting change.','aaaaaxaaaaaaxaaa'),
]

def temporal_reference():
    row_h,gap,top=84,12,28
    lx,tx0,tx1,dx0,dx1=32,200,1080,1116,1744
    step=(tx1-tx0)/16
    body=''
    for i,(label,desc,seq) in enumerate(TEMPORAL_ROWS):
        ry=top+i*(row_h+gap);base=ry+50
        body+=tx(lx,base,label,'wide-panel-title')
        runs=[];start=0
        for k in range(1,len(seq)+1):
            if k==len(seq) or seq[k]!=seq[start]:
                runs.append((seq[start],start,k));start=k
        for sym,s,e in runs:
            if sym=='x':continue
            bx0=tx0+s*step-step*0.3;bw=(e-s)*step-step*0.4
            cls={'a':'regime-band-a','b':'regime-band-b','m':'regime-band-m'}[sym]
            body+=f'<rect x="{bx0:.1f}" y="{base-24}" width="{bw:.1f}" height="48" rx="10" class="{cls}"/>'
        for k,sym in enumerate(seq):
            cx=tx0+(k+0.5)*step
            if sym=='a':
                body+=f'<circle cx="{cx:.1f}" cy="{base}" r="9" class="regime-a"/>'
            elif sym=='b':
                body+=f'<path d="M{cx:.1f} {base-11:.1f} L{cx+10:.1f} {base+8:.1f} L{cx-10:.1f} {base+8:.1f} Z" class="regime-b"/>'
            elif sym=='m':
                body+=f'<rect x="{cx-8:.1f}" y="{base-8:.1f}" width="16" height="16" class="regime-m"/>'
            else:
                body+=f'<path d="M{cx:.1f} {base-13:.1f} L{cx+13:.1f} {base:.1f} L{cx:.1f} {base+13:.1f} L{cx-13:.1f} {base:.1f} Z" class="regime-blip"/>'
        body+=tx(dx0,base,desc,'row-desc')
    legend_y=526
    body+=f'<circle cx="{lx+10}" cy="{legend_y}" r="9" class="regime-a"/>'+tx(lx+32,legend_y+6,'Earlier regime','wide-legend')
    body+=f'<path d="M{lx+270} {legend_y-11} L{lx+280} {legend_y+8} L{lx+260} {legend_y+8} Z" class="regime-b"/>'+tx(lx+296,legend_y+6,'Current regime','wide-legend')
    body+=f'<rect x="{lx+550}" y="{legend_y-8}" width="16" height="16" class="regime-m"/>'+tx(lx+578,legend_y+6,'Intermediate state','wide-legend')
    body+=f'<path d="M{lx+820} {legend_y-13} L{lx+833} {legend_y} L{lx+820} {legend_y+13} L{lx+807} {legend_y} Z" class="regime-blip"/>'+tx(lx+846,legend_y+6,'Isolated blip','wide-legend')
    body+=tx(32,566,'Bank illustrations: a pricing change can be sudden; staggered adoption gradual; evolving habits incremental; seasonal activity recurring.','wide-note')
    body+=tx(32,604,'Schematic redraw after Krawczyk and Cano (2018), Fig. 2. Shapes mark a pattern in time, not a specific feature or dataset.','wide-note')
    return frame('temporal-patterns','How the world changes over time','Five schematic time patterns of change: sudden, gradual, incremental, recurring, and isolated blips.',body),0

def input_distribution():
    body=''
    for j,(title,vals) in enumerate([('REFERENCE COHORT',[10,20,30,40]),('CURRENT COHORT',[40,30,20,10])]):
        off=j*896;layer=f'<rect x="{off+8}" y="8" width="872" height="540" rx="6" class="wide-panel"/>'
        layer+=tx(off+48,52,title,'wide-panel-title')+tx(off+48,98,'Customers per 100','wide-muted')
        for v in range(0,41,10):
            y=442-v*7;layer+=f'<path d="M{off+96} {y} H{off+816}" class="wide-grid"/>'+tx(off+76,y+8,v,'wide-tick','end')
        layer+=f'<path d="M{off+96} 146 V442 H{off+816}" class="wide-axis"/>'
        for k,v in enumerate(vals):
            x=off+140+k*172;h=v*7
            layer+=f'<rect x="{x}" y="{442-h}" width="100" height="{h}" class="hist {"current" if j else "reference"}"/>'
            layer+=tx(x+50,442-h-14,v,'wide-panel-title','middle')
            layer+=tx(x+50,470,['0','1–2','3–5','6+'][k],'wide-label','middle')
        layer+=tx(off+96,516,'App logins in the same seven-day window','wide-muted')
        body+=group(layer,j+1,title)
    body+=tx(36,598,'WHAT CHANGED','wide-accent')+tx(320,598,'The mix of customer inputs. Churn labels are not needed to see this shift.','wide-label')
    body+=tx(36,632,'Invented cohorts: 100 customers each. Identical bins and feature meaning. Input drift alone does not establish accuracy loss.','wide-note')
    return frame('drift-input-wide','Data drift: different customer inputs','Two 100-customer cohorts have different activity counts under identical feature definitions and bins.',body),2

def point(x,y,churned,highlight=False):
    shape=(f'<path d="M{x} {y-11} L{x+11} {y+9} L{x-11} {y+9} Z" class="churn-point"/>' if churned else f'<circle cx="{x}" cy="{y}" r="10" class="stay-point"/>')
    if highlight:shape=f'<circle cx="{x}" cy="{y}" r="20" class="changed-point"/>'+shape
    return shape

def point_label(x,y,text,dx=0):
    lx,ly=x+dx,y-34
    return f'<rect x="{lx-20:.1f}" y="{ly-14:.1f}" width="40" height="19" fill="#f2f1ec" rx="3"/>'+tx(lx,ly,text,'wide-tick','middle')

def scatter(off,current=False,errors=False):
    # Data coordinates map directly to linear, identical axes in both cohorts.
    xx=lambda v:off+112+v*44
    yy=lambda v:484-v*54
    body=f'<rect x="{off+8}" y="8" width="872" height="522" rx="6" class="wide-panel"/>'
    body+=tx(off+48,52,'AFTER: MATURE OUTCOMES' if current else 'BEFORE: MATURE OUTCOMES','wide-panel-title')
    body+=tx(off+48,96,'Products used','wide-muted')
    for v in [0,2,4,6]:
        y=yy(v);body+=f'<path d="M{xx(0)} {y} H{xx(14)}" class="wide-grid"/>'+tx(xx(0)-20,y+8,v,'wide-tick','end')
    for v in [0,4,8,12,14]:body+=tx(xx(v),486,v,'wide-tick','middle')
    body+=f'<path d="M{xx(0)} {yy(6)} V{yy(0)} H{xx(14)}" class="wide-axis"/>'
    body+=tx(xx(0),520,'Seven-day app logins','wide-muted')
    # Chart boundaries are data-space marks, not architecture connectors.
    if errors:
        body+=f'<path d="M{xx(0)} {yy(5.5)} L{xx(0)} {yy(6)} L{xx(5)} {yy(6)} L{xx(14)} {yy(1.5)} L{xx(14)} {yy(0)} L{xx(11)} {yy(0)} Z" class="error-region"/>'
    body+=f'<path d="M{xx(0)} {yy(5.5)} L{xx(11)} {yy(0)}" class="fixed-boundary"/>'
    if current:body+=f'<path d="M{xx(5)} {yy(6)} L{xx(14)} {yy(1.5)}" class="new-boundary"/>'
    for i,(x,y) in enumerate(POINTS):
        changed=OLD(x,y)!=NEW(x,y)
        body+=point(xx(x),yy(y),(NEW if current else OLD)(x,y),current and changed and errors)
        if i==6:body+=point_label(xx(x),yy(y),'C1',dx=-34)
        if i==12:body+=point_label(xx(x),yy(y),'C2')
    return body

def concept_relationship():
    body=group(scatter(0),1,'Reference cohort and fixed model boundary')
    body+=group(scatter(896,True),2,'Same inputs, different observed outcomes')
    body+=f'<circle cx="34" cy="566" r="10" class="stay-point"/>'+tx(58,574,'Stayed','wide-legend')
    body+=f'<path d="M220 555 L231 575 L209 575 Z" class="churn-point"/>'+tx(245,574,'Churned','wide-legend')
    body+='<path d="M430 566 H490" class="fixed-boundary"/>'+tx(506,574,'M1 boundary: unchanged','wide-legend')
    body+='<path d="M960 566 H1020" class="new-boundary"/>'+tx(1036,574,'Changed outcome relationship','wide-legend')
    body+=tx(32,608,'Same 15 input positions in both panels. Shapes show invented mature outcomes; the solid line is not an automatically retrained model.','wide-note')
    return frame('drift-concept-wide','Concept drift: same inputs, changed outcomes','The same 15 fictional customer feature positions appear before and after; outcome symbols change while the deployed M1 boundary remains fixed.',body),2

def concept_errors():
    changed=sum(OLD(x,y)!=NEW(x,y) for x,y in POINTS)
    body=group(scatter(0,True,True),1,'Changed outcomes create errors for fixed M1')
    content=tx(956,60,'WHY M1 NOW MISSES CUSTOMERS','wide-panel-title')
    content+=tx(956,107,'1  The input definitions did not change.','wide-label')
    content+=tx(956,154,'2  M1 still uses its earlier boundary.','wide-label')
    content+=tx(956,201,'3  Observed churn now follows a different pattern.','wide-label')
    content+=tx(956,248,f'{changed} customers change outcome in this toy example.','wide-accent')
    content+=tx(956,292,'They sit between the old and new boundaries.','wide-muted')
    content+=tx(956,339,'C1 · 5 logins, 5 products','wide-panel-title')
    content+=tx(956,386,'Same inputs: stayed before → churned after.','wide-label')
    content+=tx(956,434,'C2 · 11 logins, 1 product','wide-panel-title')
    content+=tx(956,481,'Same inputs: stayed before → churned after.','wide-label')
    body+=group(content,2,'Explain unchanged predictions and changed outcomes')
    body+=tx(32,560,'Rings identify missed churners. Shading marks the changed region. M1 is still unchanged.','wide-note')
    body+=tx(32,598,'Invented, deliberately simplified classifier and mature cohorts. Real class boundaries overlap; no real bank performance is reported.','wide-note')
    return frame('drift-concept-errors','How concept drift creates errors','Customers whose outcomes changed now fall on the wrong side of the unchanged earlier boundary, illustrating missed churners.',body),2

DRIFT_CSS=r'''
.wide .body-grid{top:282px;height:640px;display:block}.wide .diagram-column{width:1776px;height:640px}.wide figure{width:1776px;height:640px;transform:none}.wide svg{width:1776px;height:640px}
.wide-panel{fill:#f2f1ec;stroke:#d4d4cc;stroke-width:1.3}.wide-panel-title{font:600 29px 'Source Sans 3';fill:#303a38}.wide-label{font:400 28px 'Source Sans 3';fill:#303a38}.wide-muted{font:400 25px 'Source Sans 3';fill:#5e6967}.wide-tick{font:400 23px 'Source Sans 3';fill:#505c59}.wide-accent{font:600 28px 'Source Sans 3';fill:#a62c40}.wide-note{font:400 20px 'Source Sans 3';fill:#5a635f}.wide-legend{font:400 24px 'Source Sans 3';fill:#303a38}
.wide-grid{fill:none;stroke:#dedfd8;stroke-width:1}.wide-axis{fill:none;stroke:#7c8983;stroke-width:1.5}.stay-point{fill:#56899a;stroke:#2e5360;stroke-width:2}.churn-point{fill:#c16c79;stroke:#8f263c;stroke-width:2}.fixed-boundary{fill:none;stroke:#606e71;stroke-width:3;stroke-dasharray:10 7}.new-boundary{fill:none;stroke:#a62c40;stroke-width:3}.changed-point{fill:none;stroke:#a62c40;stroke-width:2.5}.error-region{fill:#d9a6b0;fill-opacity:.27;stroke:none}
.row-desc{font:400 22px 'Source Sans 3';fill:#3b4540}
.regime-a{fill:#eef2f1;stroke:#56899a;stroke-width:2}.regime-b{fill:#f6e9ea;stroke:#a62c40;stroke-width:2}.regime-m{fill:#f2efe6;stroke:#8a7a3a;stroke-width:2}.regime-blip{fill:#e9e6df;stroke:#6b6258;stroke-width:2}
.regime-band-a{fill:#56899a;fill-opacity:.1;stroke:none}.regime-band-b{fill:#a62c40;fill-opacity:.1;stroke:none}.regime-band-m{fill:#8a7a3a;fill-opacity:.12;stroke:none}
'''
