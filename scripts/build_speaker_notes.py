"""Builds a per-slide speaker-notes LaTeX booklet: screenshot, spoken script, delivery cues.

Source of truth is lecture_content.build_lecture() — the same data that drives the
deck itself — paired with fresh screenshots of outputs/ml-architecture-lecture.html.
Run scripts/build_lecture_deck.py and the screenshot step below before this script
whenever slide content changes, so the notes stay in sync with the deck.
"""
import re
from pathlib import Path
from html import unescape
from lecture_content import build_lecture
from speaker_scripts import SCRIPTS

ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/'previews/lecture-full'
OUT_TEX=ROOT/'outputs/speaker-notes.tex'
OUT_DIR=ROOT/'outputs'

TAG=re.compile(r'<(/?)b>')
def strip_bold(s):
    # '<b>X</b>' -> ('\\textbf{X}') while leaving the rest of the sentence plain.
    return TAG.sub(lambda m:'}' if m.group(1) else '\\textbf{',s)

SPECIAL={'&':r'\&','%':r'\%','#':r'\#','_':r'\_','$':r'\$'}
def esc(s):
    s=unescape(s)
    out=[]
    i=0
    while i<len(s):
        c=s[i]
        if c=='\\' and s[i:i+7]=='\\textbf':
            out.append(c);i+=1;continue
        if c in '{}' :
            out.append(c);i+=1;continue
        if c in SPECIAL:
            out.append(SPECIAL[c])
        else:
            out.append(c)
        i+=1
    return ''.join(out)

def escape_keep_bold(s):
    s=strip_bold(s)
    # Escape everything except the \textbf{ / } markers we just inserted.
    parts=re.split(r'(\\textbf\{|\})',s)
    return ''.join(p if p in ('\\textbf{','}') else esc(p) for p in parts)

def cues_for(slide,n,steps,prev_section):
    lines=[]
    if slide['section']!=prev_section:
        lines.append(f"New block: \\textbf{{{esc(slide['section'])}}}.")
    if steps and steps>1:
        lines.append(f"\u200bBuild: press Right {steps} times to reveal the complete figure; press once more to advance.")
    elif steps==1:
        lines.append("Build: press Right once to reveal the figure, then again to advance.")
    visual=slide['visual']
    if callable(visual): visual,_=visual()
    if isinstance(visual,str) and '<table' in visual:
        headers=[unescape(re.sub('<[^>]+>','',x)) for x in re.findall(r'<th>(.*?)</th>',visual)]
        lines.append('Table cue: introduce the columns, then explain the relevant rows using the spoken points below.')
    elif isinstance(visual,str) and '<svg' in visual:
        if slide.get('layout')=='wide':
            lines.append('Point to the graphic: identify the axes or time direction and the legend before comparing the panels.')
        else:
            names=[unescape(x) for x in re.findall(r'data-node="([^"]+)"',visual)]
            if names:lines.append('Diagram cue: follow '+esc(' → '.join(names[:3]))+'.')
    elif isinstance(visual,str) and '<img' in visual:
        lines.append('Graphic cue: follow time from left to right; distinguish the five rows before using the bank illustrations.')
    if slide['title']=='What a test can’t tell us today':
        lines.append('Handoff cue: this is the brief foundation; Simon revisits the monitoring timeline and delayed labels later.')
    if slide['title']=='Input checks now; quality checks later':
        lines.append('Callback: connect this monitoring timeline to Ricardo’s earlier test-versus-outcome distinction.')
    if slide['title'].startswith('Release plan:'):
        lines.append('Handoff to Simon: a successful release still needs ongoing input, execution and outcome evidence.')
    if slide.get('extra'):
        lines.append("Adaptation note on file for this slide; do not read aloud unless asked.")
    return lines

def clause(b):
    # '<b>Label:</b> rest.' or '<b>Label</b> rest.' -> a spoken clause, label kept bold.
    m=re.match(r'^<b>([^<]*?)(:?)</b>\s*(.*)$',b)
    if not m:
        return escape_keep_bold(b)
    label,colon,rest=m.groups()
    rest=rest[0:1].lower()+rest[1:] if rest and not colon else rest
    sep=': ' if colon else ' '
    return '\\textbf{'+esc(label)+'}'+sep+esc(rest)

def bullets_for(slide):
    items=[]
    if slide['lead']:
        items.append(escape_keep_bold(slide['lead']))
    for b in slide['bullets']:
        items.append(clause(b))
    if slide['example']:
        ex=slide['example']
        if slide.get('example_label','').startswith('Next') or ex.lower().startswith('bank') or ex.startswith('Ana'):
            items.append(escape_keep_bold(ex))
        else:
            ex=ex[0:1].lower()+ex[1:]
            items.append('\\textit{At our bank,} '+esc(ex))
    if slide['takeaway']:
        items.append('\\textit{'+escape_keep_bold(slide['takeaway'])+'}')
    return items

def paragraph_for(slide):
    # Hand-written lecture prose, keyed by title -- see speaker_scripts.py.
    script=SCRIPTS.get(slide['title'])
    if script is None:
        raise KeyError(f"No hand-written spoken script for slide {slide['title']!r} -- add one to speaker_scripts.py")
    # Keep the authored prose. Short, bulleted paragraphs are reading aids,
    # not a new, compressed script. Explicit blank lines define authored blocks.
    if '\n\n' in script:
        blocks=script.split('\n\n')
    else:
        sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z“])',script)
        blocks=[' '.join(sentences[i:i+2]) for i in range(0,len(sentences),2)]
    return '\\begin{itemize}\n'+'\n'.join('\\item '+escape_keep_bold(b) for b in blocks)+'\n\\end{itemize}'

def main():
    slides=build_lecture()
    tex=[]
    tex.append(r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=18mm,headheight=16pt]{geometry}
\usepackage{fontspec}
\setmainfont{DejaVu Sans}
\usepackage{microtype,parskip,setspace,ragged2e}
\usepackage{xcolor,graphicx,enumitem,fancyhdr}
\usepackage[most]{tcolorbox}
\usepackage[colorlinks=true,linkcolor=teal!60!black,urlcolor=teal!60!black]{hyperref}
\definecolor{teal}{HTML}{187C80}
\definecolor{pale}{HTML}{EEF6F5}
\definecolor{ink}{HTML}{203342}
\definecolor{accent}{HTML}{A62C40}
\setstretch{1.12}
\setlength{\parindent}{0pt}
\hyphenpenalty=10000
\exhyphenpenalty=10000
\setlist[itemize]{leftmargin=1.3em,itemsep=0.25em,topsep=0.2em,parsep=0.1em}
\pagestyle{fancy}
\fancyhf{}
\lhead{\small ML Architecture --- Speaker Notes}
\rhead{\small Bank customer-churn example}
\cfoot{\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\tcbset{breakable,arc=1.5mm,boxrule=0.6pt,left=3mm,right=3mm,top=2mm,bottom=2mm,before skip=6pt,after skip=6pt,fonttitle=\bfseries\small,before upper={\setlength{\parskip}{0.4em}\RaggedRight}}
\newtcolorbox{saybox}{colback=pale,colframe=teal,title={TO SAY}}
% Brace the fontupper value: its inner '=' must not be parsed as a key separator.
\newtcolorbox{examplebox}[1][]{colback=white,colframe=teal!50,title={SPOKEN SCRIPT --- short paragraphs for delivery},fontupper={\fontsize{10.5}{14}\selectfont\interlinepenalty=10000\relax},#1}
\newtcolorbox{cuebox}[1][]{colback=accent!5,colframe=accent!70!black,title={CUES},#1}
\begin{document}
\thispagestyle{empty}
\begin{center}
{\Huge\bfseries ML Architecture}\\[4mm]
{\Large Speaker Notes}\\[2mm]
{\large A bank customer-churn case --- 20 October 2026}\\[8mm]
\end{center}
\noindent Each slide has its current image, key points, visual and handoff cues, and a spoken script. The authored prose is grouped into short bulleted paragraphs so presenters can find their place easily. Read or adapt it in your own voice. Longer notes may continue to the next page. Diagram builds use the Right arrow; the stated count reveals the figure, and one more press advances the slide.
\clearpage
''')
    prev_section=None
    for n,slide in enumerate(slides,1):
        visual=slide['visual'];steps=0
        if callable(visual):
            try:
                _,steps=visual()
            except Exception:
                steps=0
        img=SHOTS/f'slide-{n:02d}.png'
        title=esc(slide['title'])
        section=esc(slide['section'])
        owner=esc(slide['owner'])
        bullets=bullets_for(slide)
        paragraph=paragraph_for(slide)
        cue_lines=cues_for(slide,n,steps,prev_section)
        prev_section=slide['section']
        tex.append(f'\\section*{{\\normalsize {n:02d} / {len(slides):02d} \\quad {title}}}')
        tex.append(f'\\noindent\\textcolor{{teal!70!black}}{{\\small {section} \\textbullet\\ {owner}}}\\par\\vspace{{2mm}}')
        tex.append('\\noindent\\begin{minipage}[t]{0.40\\textwidth}\\vspace{0pt}')
        tex.append('\\fcolorbox{teal!30}{white}{\\includegraphics[width=\\dimexpr\\linewidth-2\\fboxsep-2\\fboxrule\\relax]{'+str(img.relative_to(ROOT))+'}}')
        tex.append('\\end{minipage}\\hfill')
        tex.append('\\begin{minipage}[t]{0.57\\textwidth}\\vspace{0pt}')
        tex.append('\\begin{cuebox}')
        tex.append('\\begin{itemize}')
        for c in cue_lines:
            tex.append(f'\\item {c}')
        tex.append('\\end{itemize}')
        tex.append('\\end{cuebox}')
        tex.append('\\end{minipage}')
        tex.append('\\vspace{2mm}')
        tex.append('\\begin{saybox}')
        tex.append('\\begin{itemize}')
        for b in bullets:
            tex.append(f'\\item {b}')
        tex.append('\\end{itemize}')
        tex.append('\\end{saybox}')
        tex.append('\\begin{examplebox}[title after break={SPOKEN SCRIPT --- slide '+str(n)+' continued}]')
        tex.append(paragraph)
        tex.append('\\end{examplebox}')
        if slide['source']:
            tex.append(f'\\par\\noindent{{\\scriptsize\\textcolor{{teal!60!black}}{{Reading anchor: {esc(slide["source"])}}}}}')
        tex.append('\\clearpage')
    tex.append('\\end{document}')
    OUT_TEX.parent.mkdir(parents=True,exist_ok=True)
    OUT_TEX.write_text('\n'.join(tex))
    print('wrote',OUT_TEX)

if __name__=='__main__':
    main()
