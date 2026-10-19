"""Small, locally embedded official marks and consistent Lucide visual cues."""
from pathlib import Path
from base64 import b64encode
from html import escape

ASSETS=Path(__file__).resolve().parents[1]/'assets/marks'

def image(name,alt='',cls='concept-icon'):
    data=(ASSETS/name).read_bytes()
    # Standalone SVGs retain their own coordinate system and cannot affect
    # the authored diagram geometry, CSS, IDs or motion groups.
    if name not in ('airflow.svg','mlflow.svg'):
        data=data.replace(b'currentColor',b'#a62c40')
    return f'<img class="{cls}" alt="{escape(alt)}" src="data:image/svg+xml;base64,{b64encode(data).decode()}"/>'

def tool_mark(slide):
    if slide['title'].startswith('Airflow:'):return image('airflow.svg','Apache Airflow','brandmark')
    if slide['title'].startswith('MLflow:'):return image('mlflow.svg','MLflow','brandmark')
    return ''

def concept_mark(slide):
    title=slide['title'];section=slide['section']
    if title.startswith('Validation and drift reports'):return image('clipboard-check.svg')
    if title.startswith('Version the system'):return image('git-branch.svg')
    if title.startswith('Monitoring:') or title.startswith('Drift detection:'):return image('chart-no-axes-combined.svg')
    if title.startswith('CI, CD'):return image('workflow.svg')
    if 'Privacy:' in title or title.startswith('Least privilege'):return image('lock-keyhole.svg')
    if title.startswith('Enforce access') or title.startswith('Security threats'):return image('shield-check.svg')
    return ''

MARK_CSS='''
/* === SMALL TOOL IDENTITIES AND VISUAL CUES === */
.course{display:flex;align-items:center;gap:28px}
.brandmark{display:block;width:128px;height:38px;object-fit:contain;object-position:left center}
.explanation h2{display:flex;align-items:center;gap:12px}
.concept-icon{display:block;flex:none;width:28px;height:28px}
'''
