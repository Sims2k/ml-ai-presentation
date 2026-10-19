"""Small, locally embedded official marks and consistent Lucide visual cues."""
from pathlib import Path
from base64 import b64encode
from html import escape
from functools import lru_cache
import re

ASSETS=Path(__file__).resolve().parents[1]/'assets/marks'

def image(name,alt='',cls='concept-icon'):
    data=(ASSETS/name).read_bytes()
    # Standalone SVGs retain their own coordinate system and cannot affect
    # the authored diagram geometry, CSS, IDs or motion groups.
    if name not in ('airflow.svg','mlflow.svg','nist.svg','shap.png'):
        data=data.replace(b'currentColor',b'#a62c40')
    mime='image/png' if name.endswith('.png') else 'image/svg+xml'
    return f'<img class="{cls}" alt="{escape(alt)}" src="data:{mime};base64,{b64encode(data).decode()}"/>'

def tool_mark(slide):
    if slide['title'].startswith('Airflow:'):return image('airflow.svg','Apache Airflow','brandmark')
    if slide['title'].startswith('MLflow:'):return image('mlflow.svg','MLflow','brandmark')
    if 'NIST ' in slide['source']:return image('nist.svg','NIST — National Institute of Standards and Technology','brandmark brandmark-nist')
    if slide['title']=='Explainability and auditability differ':return image('shap.png','SHAP','brandmark brandmark-shap')
    return ''

def concept_mark(slide):
    title=slide['title'];section=slide['section']
    subjects=[
        ('The bank case','landmark'),('Two lifecycles','split'),('What a test','flask-conical'),
        ('Prediction and business','split'),('Batch path','database'),('Online serving','network'),
        ('Package the','package'),('Shadow deployment','eye'),('Release strategies','split'),
        ('Release plan','package'),('Monitoring architecture','bell'),
        ('Input checks now','clock'),('Data-quality faults','circle-alert'),
        ('A publication gate','circle-check'),('Respond:','wrench'),
        ('Hidden dependencies','plug'),('Make the feature','list-filter'),
        ('Pipeline pattern','workflow'),('Strategy pattern','settings-2'),('Observer pattern','bell'),
        ('Candidate training','flask-conical'),('Repair the input','wrench'),
        ('Trace the prediction','git-branch'),('Recovery restores','undo-2'),
        ('Airflow:','workflow'),('MLflow:','brain-circuit'),
    ]
    for prefix,name in subjects:
        if title.startswith(prefix):return image(name+'.svg')
    if title.startswith('Validation and drift reports'):return image('clipboard-check.svg')
    if title.startswith('Version the system'):return image('git-branch.svg')
    if title.startswith('Monitoring:') or title.startswith('Drift detection:'):return image('chart-no-axes-combined.svg')
    if title.startswith('CI, CD'):return image('workflow.svg')
    if 'Privacy:' in title or title.startswith('Least privilege'):return image('lock-keyhole.svg')
    if title.startswith('Enforce access') or title.startswith('Security threats'):return image('shield-check.svg')
    sections={
        'Foundations':'book-open.svg','Deployment & serving':'network.svg',
        'Monitoring & degradation':'chart-no-axes-combined.svg',
        'Design decisions':'blocks.svg','Architectural tactics':'layers.svg',
        'DevOps & MLOps':'workflow.svg','Security & privacy':'shield-check.svg',
        'Quality concerns':'badge-check.svg','Practical tools':'wrench.svg',
    }
    name=sections.get(section.split(' / ')[-1])
    return image(name) if name else ''

@lru_cache(maxsize=None)
def icon_paths(name):
    """Local Lucide primitives; inherited SVG geometry and motion stay intact."""
    data=(ASSETS/(name+'.svg')).read_text()
    return re.search(r'<svg\b[^>]*>(.*)</svg>',data,re.S).group(1)

def svg_icon(name,x,y,size=26,color='#62645f'):
    return (f'<g data-component-icon="{name}" aria-hidden="true" '
            f'transform="translate({x} {y}) scale({size/24})" '
            f'fill="none" stroke="{color}" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round">{icon_paths(name)}</g>')

def component_mark(title,role,x,y,w,h):
    """Use the spare tag-row corner, never the component's text area."""
    if h<128:return ''
    t=title.lower()
    rules=[
        (('fails','invalid','missing','bad batch'),'circle-alert'),
        (('hold publication','publication hold','withhold'),'lock-keyhole'),
        (('customer records','bank data'),'landmark'),
        (('history','snapshot','source','record','evidence store'),'database'),
        (('feature','prepared input','input contract'),'list-filter'),
        (('train','learn','test'),'flask-conical'),
        (('registry','artifact','register'),'archive'),
        (('score store','persist','saved score','prediction id'),'database'),
        (('model','risk','prediction','score','inference','implementation'),'brain-circuit'),
        (('policy','rule','strategy','configuration','config'),'sliders-horizontal'),
        (('alert','notification','notify','subject','subscriber'),'bell'),
        (('repair','restore','recovery'),'wrench'),
        (('review','evaluate','validate','gate','approve','check','verify','enforcement'),'circle-check'),
        (('version','lineage','execution context'),'git-branch'),
        (('campaign','contact','offer','customer','cohort'),'users-round'),
        (('identity','caller','request','resource','protected'),'shield-check'),
        (('runtime','package','release'),'package'),
        (('adapter','connector','interface'),'plug'),
        (('window','label','cutoff'),'clock'),
        (('decision','result','output'),'file-text'),
    ]
    name=next((name for words,name in rules if any(word in t for word in words)),
              {'data':'database','model':'brain-circuit','business':'sliders-horizontal'}.get(role,'blocks'))
    size=20 if title in ('Approved M1','Candidate M2') or len(title)>18 else 22 if w<220 else 28
    color={'data':'#526a76','model':'#a62c40','business':'#53674c'}.get(role,'#62645f')
    return svg_icon(name,x+w-size-16,y+(6 if size==20 else 10),size,color)

MARK_CSS='''
/* === SMALL TOOL IDENTITIES AND VISUAL CUES === */
.course{display:flex;align-items:center;gap:28px}
.brandmark{display:block;width:128px;height:38px;object-fit:contain;object-position:left center}
.brandmark-nist{width:140px;background:#242421;padding:6px 14px;object-position:center}
.brandmark-shap{width:36px;object-position:center}
.explanation h2{display:flex;align-items:center;gap:12px}
.concept-icon{display:block;flex:none;width:28px;height:28px}
'''
