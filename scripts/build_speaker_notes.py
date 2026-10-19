"""Builds a per-slide speaker-notes LaTeX booklet: screenshot, spoken script, delivery cues.

Source of truth is lecture_content.build_lecture() — the same data that drives the
deck itself — paired with fresh screenshots of outputs/ml-architecture-lecture.html.
Run scripts/build_lecture_deck.py and the screenshot step below before this script
whenever slide content changes, so the notes stay in sync with the deck.
"""
import re,subprocess
from pathlib import Path
from html import unescape
from lecture_content import build_lecture

ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/'previews/speaker-notes'
OUT_TEX=ROOT/'src/speaker-notes.tex'
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
    lines.append(f"Presenter: \\textbf{{{esc(slide['owner'])}}}.")
    if steps and steps>1:
        lines.append(f"Animated build: click {steps-1} time{'s' if steps>2 else ''} to reveal the remaining steps before moving on.")
    elif steps==1:
        lines.append("Single reveal: one click shows the complete figure.")
    if slide['example']:
        lines.append("Pause briefly before the bank example — let the concept land first.")
    if slide['takeaway']:
        lines.append("Close on the takeaway line before advancing.")
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

def speech_for(slide):
    sentences=[]
    if slide['lead']:
        sentences.append(escape_keep_bold(slide['lead']))
    for b in slide['bullets']:
        sentences.append(clause(b))
    if slide['example']:
        ex=slide['example']
        if ex.lower().startswith('bank'):
            sentences.append(escape_keep_bold(ex))
        else:
            ex=ex[0:1].lower()+ex[1:]
            sentences.append('\\textit{At our bank,} '+esc(ex))
    if slide['takeaway']:
        sentences.append('\\textit{'+escape_keep_bold(slide['takeaway'])+'}')
    return ' '.join(sentences)

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
\setlist[itemize]{leftmargin=1.3em,itemsep=0.25em,topsep=0.2em,parsep=0.1em}
\pagestyle{fancy}
\fancyhf{}
\lhead{\small ML Architecture --- Speaker Notes}
\rhead{\small Bank customer-churn example}
\cfoot{\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\tcbset{breakable,arc=1.5mm,boxrule=0.6pt,left=3mm,right=3mm,top=2mm,bottom=2mm,before skip=6pt,after skip=6pt,fonttitle=\bfseries\small,before upper={\setlength{\parskip}{0.4em}\RaggedRight}}
\newtcolorbox{saybox}{colback=pale,colframe=teal,title={TO SAY},fontupper=\fontsize{11}{14.5}\selectfont}
\newtcolorbox{cuebox}[1][]{colback=accent!5,colframe=accent!70!black,title={CUES},#1}
\begin{document}
\thispagestyle{empty}
\begin{center}
{\Huge\bfseries ML Architecture}\\[4mm]
{\Large Speaker Notes}\\[2mm]
{\large A bank customer-churn case --- 20 October 2026}\\[8mm]
\end{center}
\noindent Each page shows one slide exactly as presenters will see it, the words to speak, and short delivery cues. The script is a speaking aid, not a transcript to read verbatim --- adapt it to your own voice. Animated builds are marked; press the arrow key the stated number of times before moving to the next slide.
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
        speech=speech_for(slide)
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
        tex.append(speech)
        tex.append('\\end{saybox}')
        if slide['source']:
            tex.append(f'\\par\\noindent{{\\scriptsize\\textcolor{{teal!60!black}}{{Reading anchor: {esc(slide["source"])}}}}}')
        tex.append('\\clearpage')
    tex.append('\\end{document}')
    OUT_TEX.write_text('\n'.join(tex))
    print('wrote',OUT_TEX)

if __name__=='__main__':
    main()
