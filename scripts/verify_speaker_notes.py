"""Verify rendered notes for both lectures, including slide coverage and preparation."""
from pathlib import Path
import argparse
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def verify(day):
    directory = ROOT / 'outputs' / ('day2' if day == '2' else '')
    prefix = 'day2-' if day == '2' else ''
    manifest = json.loads((directory / ('day2-manifest.json' if day == '2' else 'lecture-manifest.json')).read_text())
    text = subprocess.check_output(['pdftotext', '-layout', str(directory / f'{prefix}speaker-notes.pdf'), '-'], text=True)
    assert '0.4em' not in text and 'newline' not in text, 'LaTeX syntax leaked into rendered notes'
    assert text.count('SPOKEN SCRIPT') >= len(manifest), 'A spoken-script box is missing'
    headers = {int(x) for x in re.findall(r'(?m)^\s*(\d+)\s*/\s*' + str(len(manifest)) + r'\b', text)}
    assert headers == set(range(1, len(manifest) + 1)), 'PDF slide headings are missing or stale'
    assert not re.search(r'Simon[’\x27]s\s+(?:notes|notations|technical atlas)', text, re.I), 'Personal notes appear as citations'
    if day == '2':
        assert text.count('OPTIONAL PREPARATION') == len(manifest), 'Preparation notes missing'
        assert 'Architecture Tradeoff Analysis Method' in text, 'ATAM definition missing'
    print(f'Day {day}: {len(manifest)} slides have rendered notes and matching headings.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day', choices=['1', '2', 'all'], default='all')
    args = parser.parse_args()
    for day in (['1', '2'] if args.day == 'all' else [args.day]):
        verify(day)
