"""Presenter overrides shared by the Day 2 deck and notes builders."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
SLIDES_DIR=ROOT/'slides/day2'
FIELDS=('title','lead','owner','cues','takeaway','source')

def slide_id(title):
    return re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-')

def apply_overrides(slides):
    """Apply committed presenter JSON without writing new source files."""
    by_id={slide_id(s['title']):s for s in slides};seen=set()
    for path in sorted(SLIDES_DIR.glob('*.json')):
        for entry in json.loads(path.read_text()):
            key=entry['id']
            if key not in by_id:raise ValueError(f'Unknown slide {key} in {path.name}')
            if key in seen:raise ValueError(f'Duplicate slide {key}')
            seen.add(key)
            for field in FIELDS:
                if field in entry:by_id[key][field]=entry[field]
            if by_id[key]['layout']=='standard' and not 1<=len(by_id[key]['cues'])<=4:raise ValueError(f'Use 1–4 cues for {key}')
    return slides
