from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def slide_id(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
def apply_overrides(slides):
    by_id={slide_id(s['title']):s for s in slides}
    seen=set()
    for path in sorted((ROOT/'slides').glob('*.json')):
        for entry in json.loads(path.read_text()):
            key=entry['id']
            if key not in by_id: raise ValueError(f"Unknown slide {key} in {path.name}")
            if key in seen: raise ValueError(f"Duplicate slide {key}")
            seen.add(key)
            for field in ('title','lead','owner','bullets','example','takeaway','extra'):
                if field in entry:by_id[key][field]=entry[field]
            if not 1<=len(by_id[key]['bullets'])<=5:raise ValueError(f"Use 1–5 bullets for {key}")
    return slides
