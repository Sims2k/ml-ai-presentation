"""Day 2 speaker notes: per slide, the slide image, delivery cues, key points and a spoken script.

Same booklet format as Day 1 (scripts/build_speaker_notes.py). Run after
build_day2_deck.py and verify_day2_deck.cjs (which writes previews/day2/slide-NN.png):
    python3 scripts/build_day2_speaker_notes.py
    xelatex -output-directory=outputs/day2 outputs/day2/day2-speaker-notes.tex (twice)
"""
import json,re
from pathlib import Path
from build_speaker_notes import esc,escape_keep_bold
from day2_content import build_day2
from day2_overrides import apply_overrides
from day2_speaker_scripts import SCRIPTS,DIRECTIONS,PREPARATION

ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/'previews/day2';OUT_TEX=ROOT/'outputs/day2/day2-speaker-notes.tex'

def tex(s):
    s=re.sub(r'</?code>','',re.sub(r'</?span[^>]*>','',s)).replace('&lt;','<').replace('&gt;','>')
    parts=[]
    for part in re.split(r'(https?://[^\s]+)',s):
        if part.startswith(('https://','http://')):
            address=part.rstrip('.,;')
            parts.append('\\url{'+address+'}'+part[len(address):])
        else:
            parts.append(escape_keep_bold(part).replace('<','\\textless{}').replace('>','\\textgreater{}').replace('~','\\textasciitilde{}').replace('^','\\textasciicircum{}'))
    return ''.join(parts)

def cues_for(s,m,prev_owner):
    lines=[]
    if s['owner']!=prev_owner and prev_owner is not None:lines.append(f'Handover: \\textbf{{{esc(s["owner"])}}} takes over here.')
    if m['steps']:lines.append(f'Build: press Right {m["steps"]} times to reveal the complete figure; once more to advance.')
    elif m['kind']=='figure':lines.append('Static figure or table: no builds. If it is a paper figure, name the source aloud first.')
    if DIRECTIONS.get(s['title']):lines.append('Do: '+esc(DIRECTIONS[s['title']]))
    seconds = {'Why architecture evaluation must change': 60, 'AgentArcEval: the process': 80, 'A quality scenario in six parts': 85, 'Eleven general scenarios and their measures': 65, 'Scenarios as a lens on real harnesses': 70}.get(s['title'], 70 if s['layout']=='standard' else 60)
    lines.append(f'Timing: about {seconds} seconds spoken; preparation is optional.')
    return lines

def main():
    out=[r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=18mm,headheight=16pt]{geometry}
\usepackage{fontspec}
\setmainfont{DejaVu Sans}
\usepackage{microtype,parskip,setspace,ragged2e}
\usepackage{xcolor,graphicx,enumitem,fancyhdr}
\usepackage[most]{tcolorbox}
\usepackage{xurl}
\usepackage[colorlinks=true,linkcolor=teal!60!black,urlcolor=teal!60!black]{hyperref}
\definecolor{teal}{HTML}{187C80}
\definecolor{pale}{HTML}{EEF6F5}
\definecolor{accent}{HTML}{A62C40}
\setstretch{1.12}
\setlength{\parindent}{0pt}
\hyphenpenalty=10000
\exhyphenpenalty=10000
\setlength{\emergencystretch}{3em}
\setlist[itemize]{leftmargin=1.3em,itemsep=0.25em,topsep=0.2em,parsep=0.1em}
\pagestyle{fancy}
\fancyhf{}
\lhead{\small Agentic AI Architecture --- Speaker Notes}
\rhead{\small Day 2 \textbullet\ 27 October 2026}
\cfoot{\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\tcbset{breakable,arc=1.5mm,boxrule=0.6pt,left=3mm,right=3mm,top=2mm,bottom=2mm,before skip=6pt,after skip=6pt,fonttitle=\bfseries\small,before upper={\setlength{\parskip}{0.4em}\RaggedRight}}
\newtcolorbox{saybox}{colback=pale,colframe=teal,title={KEY CONCEPTS (as shown on the slide)},fontupper=\small}
\newtcolorbox{examplebox}[1][]{colback=white,colframe=teal!50,title={SPOKEN SCRIPT --- short paragraphs for delivery},fontupper={\fontsize{10.5}{14}\selectfont\interlinepenalty=10000\relax},#1}
\newtcolorbox{prepbox}{colback=white,colframe=teal!40,title={OPTIONAL PREPARATION --- example or clarification},fontupper={\fontsize{9.5}{12}\selectfont}}
\newtcolorbox{cuebox}[1][]{colback=accent!5,colframe=accent!70!black,title={CUES},fontupper=\small,#1}
\begin{document}
\thispagestyle{empty}
\begin{center}
{\Huge\bfseries Agentic AI Architecture}\\[4mm]
{\Large Speaker Notes}\\[2mm]
{\large Day 2 --- 27 October 2026 --- 40 minutes}\\[8mm]
\end{center}
\noindent Each slide has its current image, delivery cues, the key points shown on the slide, and a spoken script in short paragraphs. Read it or adapt it in your own voice. Optional preparation boxes explain terms, give an example to keep in reserve, and flag limits of the evidence; they are not additional text to read aloud. Examples marked optional are teaching illustrations, not reported experiments. There is no running example: each topic stands on its own paper, and real systems --- Pi, Pi Durable and Hermes --- appear as evidence. The right-hand column of each slide is read by the audience; the directions for you are in the CUES box here.

\medskip
\begin{tabular}{@{}lll@{}}
\textbf{Time} & \textbf{Presenter} & \textbf{Slides}\\
0--2 min & All & 1--2\\
2--9 min & Ricardo & 3--8\\
9--15 min & Tomás & 9--14\\
15--21 min & Simon & 15--19\\
21--29 min & Luca & 20--26\\
29--37 min & Matheus & 27--33\\
37--40 min & All & 34 (discussion)\\
\end{tabular}

\medskip
\noindent\textbf{Keys:} Right/Space reveals the next diagram part, then the next slide; Left reverses; G opens the contents; F fullscreen.
\clearpage
''']
    slides=apply_overrides(build_day2())
    manifest=json.loads((ROOT/'outputs/day2/day2-manifest.json').read_text())
    if [s['title'] for s in slides] != [m['title'] for m in manifest]:
        raise ValueError('Rebuild and verify Day 2 before generating notes.')
    OUT_TEX.parent.mkdir(parents=True,exist_ok=True)
    prev=None
    for n,(s,m) in enumerate(zip(slides,manifest),1):
        script=SCRIPTS.get(s['title'])
        if script is None:raise KeyError(f'No spoken script for {s["title"]!r} in day2_speaker_scripts.py')
        out.append(f'\\section*{{\\normalsize {n:02d} / {len(slides):02d} \\quad {esc(s["title"])}}}')
        out.append(f'\\noindent\\textcolor{{teal!70!black}}{{\\small {esc(s["section"])} \\textbullet\\ {esc(s["owner"])}}}\\par\\vspace{{2mm}}')
        out.append('\\noindent\\begin{minipage}[t]{0.42\\textwidth}\\vspace{0pt}')
        out.append('\\fcolorbox{teal!30}{white}{\\includegraphics[width=\\dimexpr\\linewidth-2\\fboxsep-2\\fboxrule\\relax]{'+str((SHOTS/f'slide-{n:02d}.png').relative_to(ROOT))+'}}')
        out.append('\\end{minipage}\\hfill\\begin{minipage}[t]{0.55\\textwidth}\\vspace{0pt}\\begin{cuebox}\\begin{itemize}')
        out+=[f'\\item {c}' for c in cues_for(s,m,prev)]
        out.append('\\end{itemize}\\end{cuebox}\\end{minipage}\\vspace{2mm}')
        prev=s['owner']
        if s['layout']=='standard':
            out.append('\\begin{saybox}\\begin{itemize}')
            out.append('\\item '+tex(s['lead']))
            out+=['\\item '+tex(c) for c in s['cues']]
            out.append('\\item \\textit{'+tex(s['takeaway'])+'}')
            out.append('\\end{itemize}\\end{saybox}')
        out.append('\\begin{examplebox}[title after break={SPOKEN SCRIPT --- slide '+str(n)+' continued}]\\begin{itemize}')
        out+=['\\item '+tex(p.strip()) for p in script.split('\n\n')]
        out.append('\\end{itemize}\\end{examplebox}')
        preparation=PREPARATION[s['title']]
        out.append('\\begin{prepbox}'+tex(preparation)+'\\end{prepbox}')
        if s['source']:
            anchors=r'\newline{}'.join(esc(part) for part in s['source'].split(' · '))
            out.append(f'\\par\\noindent{{\\scriptsize\\RaggedRight\\textcolor{{teal!60!black}}{{Reading anchor: {anchors}}}\\par}}')
        out.append('\\clearpage')
    out.append('\\end{document}')
    OUT_TEX.write_text('\n'.join(out));print('wrote',OUT_TEX)

if __name__=='__main__':main()
