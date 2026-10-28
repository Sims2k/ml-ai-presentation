"""Build both lectures without cached outputs or generated diagrams."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

with tempfile.TemporaryDirectory(prefix='presentation-clean-build-') as directory:
    checkout = Path(directory)
    for name in ['scripts', 'slides', 'theme', 'assets', 'src']:
        shutil.copytree(ROOT / name, checkout / name,
                        ignore=shutil.ignore_patterns('__pycache__', 'diagrams'))
    for script in ['build_lecture_deck.py', 'build_day2_deck.py']:
        subprocess.run([sys.executable, str(checkout / 'scripts' / script)],
                       cwd=checkout, check=True)
    for name, count in [('lecture-manifest.json', 54), ('day2/day2-manifest.json', 34)]:
        assert len(json.loads((checkout / 'outputs' / name).read_text())) == count
    assert not (checkout / 'outputs/lecture-redesign.html').exists()
    print('Both lectures build from clean source directories without prototype outputs.')
