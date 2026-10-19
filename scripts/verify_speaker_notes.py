"""Check the rendered PDF, including the previously printed spacing literal."""
from pathlib import Path
import json,re,subprocess

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'outputs/lecture-manifest.json').read_text())
text=subprocess.check_output(['pdftotext','-layout',str(ROOT/'outputs/speaker-notes.pdf'),'-'],text=True)
assert '0.4em' not in text, 'LaTeX spacing value leaked into rendered script boxes'
assert text.count('SPOKEN SCRIPT')>=len(manifest), 'A spoken-script box is missing'
headers={int(x) for x in re.findall(r'(?m)^\s*(\d+)\s*/\s*'+str(len(manifest))+r'\b',text)}
assert headers==set(range(1,len(manifest)+1)), 'PDF slide headings are missing or stale'
assert not re.search(r'Simon[’\x27]s\s+(?:notes|notations|technical atlas)',text,re.I), 'Personal notes appear as citations'
print(f'{len(manifest)} slides have rendered notes; no stray spacing text or personal-note citations.')
