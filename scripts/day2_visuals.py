"""Day 2 figures: agentic AI architecture, drawn in the Day 1 diagram vocabulary.

Same lanes, node roles, orthogonal connectors and keyboard builds as Day 1.
Roles keep one meaning across the deck:
  model    (crimson) — the foundation model and the loop that drives it
  data     (blue)    — harness components, state, evidence
  business (green)   — people, governance, triggers outside the harness
Paper numbers come from the cited papers; Pi, Pi Durable and Hermes details from
their own documentation and the harness study.
"""
from html import escape
from deck_common import text, arrow, svg, group
from lecture_full_visuals import edge, zone
from visual_marks import svg_icon, logo

ICON_COLOR={'data':'#526a76','model':'#a62c40','business':'#53674c','plain':'#62645f'}

def node(x,y,w,h,title,lines=(),role='data',tag='',icon=None):
    """Tall nodes (h>=112) carry a tag row with an icon; compact nodes use two lines."""
    out=f'<g data-node="{escape(title)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" class="node {role}"/>'
    if h>=112:
        if icon:out+=svg_icon(icon,x+w-40,y+10,24,ICON_COLOR[role])
        if tag:out+=text(x+16,y+28,tag,'node-tag')
        out+=text(x+16,y+64,title)
        for i,line in enumerate(lines):out+=text(x+16,y+100+i*32,line,'node-sub')
    else:
        if icon:out+=svg_icon(icon,x+w-40,y+(h-24)//2,24,ICON_COLOR[role])
        out+=text(x+16,y+36,title)
        for i,line in enumerate(lines):out+=text(x+16,y+68+i*30,line,'node-sub')
    return out+'</g>'

def side_label(x,y,value,anchor='start'):
    """Arrow label on an opaque mask, 8px clear of its connector."""
    w=len(value)*10+16
    rx=x+8 if anchor=='start' else x-8-w if anchor=='end' else x-w/2
    return f'<rect x="{rx}" y="{y-21}" width="{w}" height="28" fill="#faf9f7"/>'+text(rx+8,y,value,'edge-label')

def note(y,value):
    return text(28,y,value,'diagram-note')

# === OPENING ===

def one_layer_up():
    s='one-layer-up'
    top=zone(16,'DAY 1 · A MODEL INSIDE AN ML SYSTEM',272)
    for a,b in [(216,244),(436,464),(656,684),(876,904)]:top+=arrow(s,a,172,b,172)
    for x,(t,l,r,tag,ic) in zip([24,244,464,684,904],[
        ('Records',['CRM + app data'],'data','INPUT','database'),('Features',['Validated inputs'],'data','PREPARE','list-filter'),
        ('Model M1',['Risk score'],'model','PREDICT','brain-circuit'),('Score store',['With versions'],'data','STORE','archive'),
        ('Policy',['Rules decide'],'business','ACT','sliders-horizontal')]):
        top+=node(x,96,192,152,t,l,r,tag,ic)
    body=group(top,1,'Day 1: records, features, model, stored score, business policy')
    low=zone(328,'DAY 2 · A MODEL INSIDE A HARNESS THAT ACTS',300)
    for a,b in [(216,244),(436,464),(656,684),(876,904)]:low+=arrow(s,a,484,b,484)
    for x,(t,l,r,tag,ic) in zip([24,244,464,684,904],[
        ('Request',['Goal in words'],'business','INPUT','message-square'),('Context',['Window built'],'data','PREPARE','layers'),
        ('Model',['Picks an action'],'model','DECIDE','brain-circuit'),('Tool',['Runs in sandbox'],'data','ACT','wrench'),
        ('Observation',['Result fed back'],'data','OBSERVE','eye')]):
        low+=node(x,408,192,152,t,l,r,tag,ic)
    body+=group(low,2,'Day 2: request, context, model, tool, observation')
    back=edge(s,'M1000 560 V588 Q1000 596 992 596 H568 Q560 596 560 588 V564')+side_label(780,586,'REPEAT UNTIL DONE','middle')
    body+=group(back,3,'The observation returns to the context window until the goal is reached')
    return svg(s,'From an ML system to an agent harness','Day 1 scored customers in a one-way pipeline; Day 2 places the model in a loop that chooses tools, observes results, and repeats.',body),3

# === TOPIC 1 · HARNESS ===

def harness_anatomy():
    s='harness-anatomy'
    ui=zone(8,'INTERFACE LAYER · HOW PEOPLE AND PROGRAMS REACH THE AGENT',148)
    for x,(t,l,ic) in zip([24,384,744],[('Terminal',['TUI · print / JSON mode'],'terminal'),('Editors and apps',['IDE · SDK · ACP server'],'file-code'),('Chat gateways',['Slack · Telegram · email'],'message-square')]):
        ui+=node(x,60,352,84,t,l,'business',icon=ic)
    ui+=arrow(s,200,144,200,172)
    core=zone(176,'HARNESS · SEVEN SUBSYSTEMS AROUND THE MODEL',360)
    core+=node(24,232,272,288,'Agent loop',['model → tool →','observation, until','the model answers','in text'],'model','SUBSYSTEM 1','repeat-2')
    mods=''
    for i,(t,l,r,ic) in enumerate([('LLM access',['providers · retries'],'data','cpu'),('Tools',['read · edit · bash'],'data','wrench'),
        ('Safety',['approval · sandbox'],'business','shield-check'),('Memory',['context · compaction'],'data','layers'),
        ('Orchestration',['sub-agents'],'data','bot'),('Extensions',['skills · MCP · hooks'],'data','puzzle')]):
        x=320+(i%3)*264;y=232 if i<3 else 388;h=140 if i<3 else 132
        mods+=node(x,y,248,h,t,l,r,f'SUBSYSTEM {i+2}',ic)
    ev=zone(556,'SIZE IS NOT THE POINT',76)+logo('mini-swe-agent.png',320,574,40)+text(372,602,'Mini-SWE-Agent: all seven in ~100 lines','aside-sub')+logo('hermes.png',780,574,40)+text(832,602,'Hermes: ~642,000 lines','aside-sub')
    body=group(core,1,'The agent loop at the centre')+group(mods,2,'Six further subsystems')+group(ui+ev,3,'Interfaces above; the same seven at every size')
    return svg(s,'Agent = model + harness','A harness wraps the model in seven subsystems: the agent loop, LLM access, tools, safety, memory, orchestration and extensions, reached through terminal, editor and chat interfaces.',body),3

def _ring_exit(cx,cy,R,box,theta,direction):
    """Angle where the station circle leaves a station box, walking from its centre angle."""
    import math
    x0,y0,w,h=box;inside=lambda a:x0<=cx+R*math.cos(a)<=x0+w and y0<=cy+R*math.sin(a)<=y0+h
    lo,hi=theta,theta+direction*1.2
    for _ in range(60):
        mid=(lo+hi)/2
        lo,hi=(mid,hi) if inside(mid) else (lo,mid)
    return hi

def agent_loop():
    """Loop type: the context window accumulates state; stations run clockwise."""
    import math
    s='agent-loop';cx,cy,R=560,320,268;sw,sh=236,92;N=5
    stations=[('Model','picks a tool call','model','brain-circuit','TOOL CALL'),
              ('Permission gate','allow · ask · deny','business','shield-check',None),
              ('Tool in sandbox','read · edit · bash …','data','box',None),
              ('Observation','result or error','data','eye','RESULT'),
              ('Safe boundary','queued input enters','data','message-square','')]
    boxes=[];P=[]
    for k in range(N):
        t=-math.pi/2+k*2*math.pi/N;px,py=cx+R*math.cos(t),cy+R*math.sin(t)
        P.append((t,px,py));boxes.append((round((px-sw/2)/4)*4,round((py-sh/2)/4)*4,sw,sh))
    groups=['','','']
    step_of=[0,1,1,2,2]
    for k in range(N):
        j=(k+1)%N;tk,tj=P[k][0],P[j][0]+(2*math.pi if j==0 else 0)
        a0=_ring_exit(cx,cy,R,boxes[k],tk,1);a1=_ring_exit(cx,cy,R,boxes[j],tj,-1)-1.2/R
        x0,y0=cx+R*math.cos(a0),cy+R*math.sin(a0);x1,y1=cx+R*math.cos(a1),cy+R*math.sin(a1)
        groups[step_of[j]]+=f'<path d="M{x0:.2f} {y0:.2f} A{R} {R} 0 0 1 {x1:.2f} {y1:.2f}" class="ring" marker-end="url(#{s}-arrow)"/>'
    hw,hh=216,120
    for k,(name,sub,role,ic,spoke) in enumerate(stations):
        if not spoke:continue
        t,px,py=P[k];ux,uy=math.cos(t),math.sin(t)
        d=lambda v,a,b:min(a/abs(v[0]) if v[0] else 1e9,b/abs(v[1]) if v[1] else 1e9)
        ds=d((ux,uy),sw/2,sh/2);dh=d((ux,uy),hw/2,hh/2)+8
        sx,sy=px-ds*ux,py-ds*uy;ex,ey=cx+dh*ux,cy+dh*uy
        mx,my=(sx+ex)/2,(sy+ey)/2
        lab=side_label(mx,my+6,spoke) if k==0 else side_label(mx,my-14,spoke,'middle') if abs(uy)<.5 else side_label(mx,my+6,spoke,'start' if ux>=0 else 'end')
        groups[step_of[k]]+=f'<path d="M{sx:.2f} {sy:.2f} L{ex:.2f} {ey:.2f}" class="spoke" marker-end="url(#{s}-arrow)"/>'+lab
    for k,(name,sub,role,ic,_) in enumerate(stations):
        x,y,w,h=boxes[k];groups[step_of[k]]+=node(x,y,w,h,name,[sub],role,icon=ic)
    hub=f'<g data-node="Context window"><rect x="{cx-hw/2}" y="{cy-hh/2}" width="{hw}" height="{hh}" rx="6" class="hub"/>'
    hub+=text(cx,cy-14,'Context window','hub-title','middle')+text(cx,cy+18,'prompt + history','hub-sub','middle')+text(cx,cy+46,'grows each pass','hub-sub','middle')+'</g>'
    groups[0]=hub+groups[0]
    groups[0]+=text(28,60,'Your request enters','annotation')+text(28,92,'the window first.','annotation')
    groups[2]+=text(1092,60,'No tool call →','annotation','end')+text(1092,92,'final answer, loop ends.','annotation','end')
    groups[2]+=note(628,'Stop conditions differ: Pi has no turn cap; Hermes budgets 90 iterations and adds stop-guards.')
    body=''.join(group(g,i+1,lab) for i,(g,lab) in enumerate(zip(groups,['The model reads the window and picks a tool call','The gate allows it and the tool runs in the sandbox','The observation and any steering input return to the window'])))
    return svg(s,'The agent loop','The model reads the context window and picks a tool call, the permission gate allows it, the tool runs in a sandbox, and the observation and any queued steering input are written back to the window until the model answers in text.',body),3

def pi_architecture():
    s='pi-architecture'
    layers=''
    for (a,b) in [(136,168),(280,312),(424,456)]:layers+=arrow(s,392,a,392,b)
    for y,(t,l,r,tag,ic) in zip([24,168,312,456],[
        ('Interfaces',['Interactive TUI · print / JSON · RPC · SDK'],'business','SURFACES','terminal'),
        ('pi-coding-agent',['Sessions · 4 tools: read, write, edit, bash · skills'],'data','PRODUCT','package'),
        ('pi-agent-core',['Agent loop + event stream that extensions hook into'],'model','LOOP','repeat-2'),
        ('pi-ai',['One API over many providers · per-model quirk flags'],'data','MODELS','cpu')]):
        layers+=node(24,y,736,112,t,l,r,tag,ic)
    side=arrow(s,760,224,792,224)+arrow(s,792,368,760,368)
    side+=node(792,168,304,112,'Session tree',['JSONL · fork · rewind'],'data','STATE','git-fork')
    side+=node(792,312,304,256,'Extension host',['Sub-agents','Plan mode','Permissions','Custom tools'],'business','EXTENSIONS','puzzle')
    side+=text(28,616,'Safety is a documented absence in the core: permissions arrive as extensions.','aside-title')
    body=group(layers,1,'Four layers from interface to model gateway')+group(side,2,'Session tree and extension host')
    return svg(s,'Pi: a minimal core with an extension host','Pi layers interfaces over pi-coding-agent, pi-agent-core and the pi-ai model gateway; sessions are a JSONL tree and sub-agents, plan mode and permissions arrive as extensions.',body),2

def harness_absences():
    s='harness-absences'
    x0=448;step=52
    rows=[('Skills (SKILL.md bundles)',9),('LLM summarization of history',9),('Hierarchical Markdown context',8),('MCP integration',8),
          ('Agentic framework in the loop',0),('Embedding retrieval over code',0)]
    def row(i,name,n):
        y=84+i*84;out=text(28,y+8,name,'plot-title')
        for k in range(11):
            cls='dot-on' if k<n else 'dot-zero' if n==0 else 'dot-off'
            out+=f'<circle cx="{x0+k*step}" cy="{y}" r="17" class="{cls}"/>'
        out+=text(x0+10*step+40,y+8,f'{n} / 11','bar-zero' if n==0 else 'bar-value')
        return out
    head=text(x0-8,40,'one dot per harness · filled = implements the pattern','axis-label')
    body=group(head+''.join(row(i,*r) for i,r in enumerate(rows[:4])),1,'What most harnesses share')
    body+=group(''.join(row(i+4,*r) for i,r in enumerate(rows[4:]))+text(28,556,'None of the eleven: hand-written loops and grep-style search instead.','annotation'),2,'The twin absences')
    body+=note(624,'Eleven production harnesses at July 2026 pins · source-level audit')
    return svg(s,'What eleven harnesses share and lack','Skills and history summarization appear in nine of eleven harnesses, hierarchical context files and MCP in eight; none uses an agentic framework or embedding retrieval over code.',body),2

HARNESSES=[('Mini-SWE','Agent',1,'mini-swe-agent.png'),('Pi','',7,'pi.svg'),('Mistral','Vibe',12,'mistral.svg'),('Aider','',13,'aider.svg'),
           ('Open','Code',17,'opencode.svg'),('Open','Hands',25,'openhands.svg'),('Codex','',27,'codex.svg'),('Gemini','CLI',35,'gemini-cli.svg'),
           ('Claude','Code',43,'claude-code.svg'),('Hermes','',69,'hermes.png'),('Open','Claw',109,'openclaw.svg')]


def tool_spectrum():
    """Number line: cards evenly spaced in rank order, elbows down to each harness's true log position."""
    import math
    s='tool-spectrum';X0,X1,AY,CB=72,1048,528,240
    px=lambda n:round(X0+math.log2(n)/math.log2(109)*(X1-X0))
    axis=f'<path d="M{X0-24} {AY} H{X1+40}" class="axis-strong"/>'
    for n in (1,10,100):axis+=f'<path d="M{px(n)} {AY} V{AY+12}" class="axis"/>'+text(px(n),AY+40,str(n),'bar-value','middle')
    axis+=text(X0-24,AY+76,'Built-in tools per harness · logarithmic scale','axis-label')
    groups=[axis,'','']
    for i,(a,b,n,mark) in enumerate(HARNESSES):
        c=round(X0+i*(X1-X0)/10);x=px(n);focus=mark in ('pi.svg','hermes.png')
        g=f'<g data-node="{escape((a+" "+b).strip())}"><rect x="{c-44}" y="24" width="88" height="{CB-24}" rx="6" class="node {"model" if focus else "plain"}"/>'
        g+=logo(mark,c-24,40,48)+text(c,124,a,'card-name','middle')+(text(c,152,b,'card-name','middle') if b else '')
        g+=text(c,214,str(n),'count-num','middle')+'</g>'
        if abs(x-c)<6:g=f'<path d="M{x} {CB} V{AY-9}" class="leader"/>'+g
        else:
            y=264+(7-i)*36
            g=f'<path d="M{c} {CB} V{y-8} Q{c} {y} {c+8} {y} H{x-8} Q{x} {y} {x} {y+8} V{AY-9}" class="leader"/>'+g
        g+=f'<circle cx="{x}" cy="{AY}" r="8" class="{"dot-focus" if focus else "dot-ink"}"/>'
        groups[0 if i<2 else 1 if i<9 else 2]+=g
    labels=['The minimal end: one bash tool, or four by default','The middle: twelve to forty-three tools','The maximal end: sixty-nine and more than a hundred']
    body=''.join(group(g,k+1,l) for k,(g,l) in enumerate(zip(groups,labels)))
    body+=note(628,'Distinct built-in tools or edit formats, July 2026. Pi builds 7 and exposes 4 by default; Hermes scopes its 69 per platform.')
    return svg(s,'Eleven harnesses, from one tool to 109','The eleven harnesses of the study placed on a logarithmic scale of built-in tools: Mini-SWE-Agent 1, Pi 7, Mistral Vibe 12, Aider 13, OpenCode 17, OpenHands 25, Codex 27, Gemini CLI 35, Claude Code 43, Hermes 69 and OpenClaw 109.',body),3

# === TOPIC 2 · PATTERNS ===

def pattern_families():
    s='pattern-families'
    fams=[('Goal creation',[('Passive goal creator',0),('Proactive goal creator',0)]),
          ('Prompts & knowledge',[('Prompt/response optimiser',0),('RAG (retrieval)',0)]),
          ('Model querying',[('Incremental model querying',0),('One-shot model querying',0)]),
          ('Plan generation',[('Single-path plan generator',1),('Multi-path plan generator',1)]),
          ('Reflection',[('Self-reflection',1),('Cross-reflection',1),('Human reflection',1)]),
          ('Cooperation',[('Role-based cooperation',0),('Voting-based cooperation',0),('Debate-based cooperation',0)]),
          ('Guardrails & tools',[('Tool/agent registry',1),('Agent adapter',1),('Multimodal guardrails',0)]),
          ('Evaluation',[('Agent evaluator',0)])]
    def card(i,name,items):
        x=24+(i%2)*548;y=12+(i//2)*148
        out=f'<g data-node="{escape(name)}"><rect x="{x}" y="{y}" width="528" height="136" rx="6" class="node family"/>'+text(x+20,y+38,name,'family-title')
        for k,(p,used) in enumerate(items):
            px=x+24+(k%2)*268;py=y+80+(k//2)*34
            out+=f'<circle cx="{px+6}" cy="{py-6}" r="6" class="{"used" if used else "unused"}"/>'+text(px+20,py,p,'pattern-item')
        return out+'</g>'
    body=group(''.join(card(i,*f) for i,f in enumerate(fams[:4])),1,'Goal, prompt, querying and planning patterns')
    body+=group(''.join(card(i+4,*f) for i,f in enumerate(fams[4:])),2,'Reflection, cooperation, tool and evaluation patterns')
    body+='<circle cx="34" cy="618" r="6" class="used"/>'+text(48,624,'covered on the next three slides','legend')+'<circle cx="374" cy="618" r="6" class="unused"/>'+text(428,624,'see the catalogue for details','legend')
    return svg(s,'Eighteen patterns in eight families','The catalogue’s eighteen patterns grouped into goal creation, prompts and knowledge, model querying, plan generation, reflection, cooperation, guardrails and tools, and evaluation, with planning, reflection and registry patterns marked for the next slides.',body),2

def planning():
    s='planning'
    top=zone(8,'SINGLE-PATH PLAN GENERATOR · ONE ORDERED LIST',292)
    for a,b in [(264,288),(528,552),(792,816)]:top+=arrow(s,a,136,b,136)
    for x,(t,l) in zip([24,288,552,816],[('Explore',['read the failing test']),('Locate',['find the faulty line']),('Edit',['apply one fix']),('Verify',['run the tests'])]):
        top+=node(x,88,240,96,t,l,'data')
    top+=text(28,240,'Coding agents often keep this list visible as a todo tool;','aside-sub')+text(28,272,'a plan mode can draft it with read-only tools before any edit.','aside-sub')
    low=zone(320,'MULTI-PATH PLAN GENERATOR · OPTIONS AT EACH STEP',304)
    low+=edge(s,'M232 476 H256 Q264 476 264 468 V428 Q264 420 272 420 H296')+edge(s,'M232 500 H256 Q264 500 264 508 V556 Q264 564 272 564 H296')
    low+=edge(s,'M552 420 H576 Q584 420 584 428 V468 Q584 476 592 476 H616')+edge(s,'M552 564 H576 Q584 564 584 556 V508 Q584 500 592 500 H616')
    low+=arrow(s,840,488,904,488)
    low+=node(24,440,208,96,'Goal',['fix the bug'],'business')+node(296,372,256,96,'Option A',['patch the parser'])+node(296,516,256,96,'Option B',['rewrite module'])
    low+=node(616,440,224,96,'Compare',['tests, cost, risk'])+node(904,440,192,96,'Choose',['best path'],'model')
    body=group(top,1,'Single-path plan')+group(low,2,'Multi-path plan')
    return svg(s,'Planning: one path or many','A single-path generator orders one list of steps; a multi-path generator keeps options at each step and compares them before choosing.',body),2

def reflection():
    """Nested loops: the further out the checker sits, the slower and more independent the check."""
    s='reflection';cy=320
    agent=f'<g data-node="Agent"><rect x="24" y="48" width="200" height="544" rx="6" class="node model"/>'
    agent+=svg_icon('bot',100,250,40,ICON_COLOR['model'])+text(124,326,'Agent','node-title','middle')+text(124,358,'proposes','node-sub','middle')+text(124,388,'an action','node-sub','middle')+'</g>'
    loops=[(120,400,'SELF','Own checks','tests · linter','Hermes: verify on stop','data','search'),
           (192,680,'CROSS','Reviewer agent','a second model','Pi Durable: read-only','data','bot'),
           (264,960,'HUMAN','Person','approves or denies','Hermes: risky commands','business','hand')]
    groups=[]
    for k,(h,x,tag,title,sub,ex,role,ic) in enumerate(loops):
        top,bot=cy-h,cy+h
        g=edge(s,f'M224 {top} H{x-8} Q{x} {top} {x} {top+8} V{cy-84}')
        g+=edge(s,f'M{x} {cy+84} V{bot-8} Q{x} {bot} {x-8} {bot} H226')
        if k==0:g+=side_label(240,top-12,'OUTPUT')+side_label(240,bot+28,'FEEDBACK')
        g+=f'<g data-node="{title}"><rect x="{x-120}" y="{cy-84}" width="240" height="168" rx="6" class="node {role}"/>'
        g+=svg_icon(ic,x+80,cy-74,24,ICON_COLOR[role])+text(x-104,cy-56,tag,'node-tag')+text(x-104,cy-20,title)+text(x-104,cy+16,sub,'node-sub')+text(x-104,cy+60,ex,'diagram-note')+'</g>'
        groups.append(g)
    groups[0]=agent+groups[0]
    groups[2]+=text(1092,36,'Further out: slower, but more independent.','annotation','end')
    body=''.join(group(g,i+1,l) for i,(g,l) in enumerate(zip(groups,['Self-reflection: the agent checks its own work','Cross-reflection: a second agent reviews','Human reflection: a person approves or denies'])))
    body+=note(628,'Liu et al. (2025): self-, cross- and human reflection. Examples from the Hermes and Pi Durable documentation.')
    return svg(s,'Reflection: who checks the work','Three nested feedback loops around one agent: its own checks, a reviewer agent, and a person; the further out the checker, the slower but more independent the check.',body),3

def registry():
    s='registry'
    a=arrow(s,264,308,336,308)
    a+=node(24,232,240,152,'Agent loop',['needs a capability'],'model','CALLER','repeat-2')
    a+=node(336,200,280,216,'Registry',['Tool schemas','Skills catalog','Agent personas'],'data','TOOL/AGENT REGISTRY','list-checks')
    b=edge(s,'M616 254 H632 Q640 254 640 246 V92 Q640 84 648 84 H688')+edge(s,'M616 308 H656 Q664 308 664 300 V244 Q664 236 672 236 H688')+edge(s,'M616 362 H648 Q656 362 656 370 V380 Q656 388 664 388 H688')
    b+=node(688,16,408,136,'Built-in tools',['read · edit · bash · grep …'],'data','TOOLS','wrench')
    b+=node(688,168,408,136,'Skills',['SKILL.md body loads on use'],'data','WORKFLOWS','puzzle')
    b+=node(688,320,408,136,'Subagents',['explore · plan · review'],'data','AGENTS','bot')
    c=edge(s,'M144 384 V540 Q144 548 152 548 H336')+arrow(s,616,548,688,548)
    c+=node(336,480,280,136,'Agent adapter',['MCP · JSON-RPC'],'business','ADAPTER')+logo('mcp.svg',572,490,32)
    c+=node(688,480,408,136,'External systems',['MCP servers · LSP · sandbox'],'data','OUTSIDE THE LOOP','server')
    c+=note(628,'Hermes registers 69 tools but exposes them per platform through toolsets; Pi exposes 4 by default.')
    body=group(a,1,'Agent loop and registry')+group(b,2,'Tools, skills and subagents')+group(c,3,'Adapter to external systems')
    return svg(s,'Registries and adapters','A registry turns tool schemas, skills and agent personas into discoverable capabilities; an adapter connects the loop to external systems such as MCP servers, a language server and a sandbox.',body),3

# === TOPIC 3 · EVALUATION ===

def evaluation_shift():
    s='evaluation-shift'
    body=text(28,44,'CLASSIC ATAM ASSUMES','lane-title')+text(628,44,'A FOUNDATION-MODEL AGENT','lane-title')
    rows=[(('Fixed requirements',['Specified before design']),('Goals, decomposed live',['Sub-tasks planned at runtime'])),
          (('Designers trade off',['Decided at design time']),('Agent trades off',['Within guardrails you design'])),
          (('Stable risks',['Assessed once, stay valid']),('Continuous evolution',['Model, prompts, tools change'])),
          (('Generic scenarios',['Quality attribute templates']),('Agent-specific scenarios',['Memory, tools, guardrails']))]
    for i,(l,r) in enumerate(rows):
        y=72+i*128
        g=arrow(s,496,y+56,624,y+56)+node(24,y,472,112,l[0],l[1],'plain',icon='file-text')+node(624,y,472,112,r[0],r[1],'data',icon='bot')
        body+=group(g,i+1,r[0])
    body+=text(28,616,'Guardrail design becomes the principal architectural control point.','annotation')
    return svg(s,'Why agent architecture evaluation must change','Four assumptions of classic scenario-based evaluation and how a foundation-model agent breaks each one.',body),4

def scenario_template():
    s='scenario-template'
    body=text(28,52,'An accuracy scenario from the Luna tax-copilot case','plot-title')+text(28,88,'Each part is checkable: the measure says what “good” looks like.','aside-sub')
    a=arrow(s,216,236,244,236)
    a+=node(24,120,192,232,'Tax expert',['a tax','professional'],'business','SOURCE','users-round')
    a+=node(244,120,192,232,'Query',['capital gains','tax on a rental','property sale'],'data','STIMULUS','message-square')
    b=arrow(s,436,236,464,236)+node(464,120,192,232,'Pipeline',['context engine','planner','retriever'],'data','ARTEFACT','layers')
    b+=node(24,400,1072,96,'Environment',['Tax season: accurate recommendations are key'],'data')
    c=arrow(s,656,236,684,236)+arrow(s,876,236,904,236)
    c+=node(684,120,192,232,'Answer',['latest rules,','advice in','context'],'data','RESPONSE','circle-check')
    c+=node(904,120,192,232,'≥ 95%',['accurate answers','and correct','references'],'business','MEASURE','gauge')
    c+=note(560,'Template: source → stimulus → environment → artefact → response → response measure (Lu et al., §5).')+note(590,'Values: the Luna accuracy context scenario (Lu et al., §6.4), shortened.')
    body+=group(a,1,'Source and stimulus')+group(b,2,'Artefact and environment')+group(c,3,'Response and measure')
    return svg(s,'A quality scenario in six parts','The Luna tax copilot’s accuracy scenario: a tax professional asks about capital gains tax, the copilot pipeline retrieves the latest regulations and answers, measured at 95% accuracy and correct references.',body),3

def eleven_scenarios():
    """Polar wheel: eleven attribute sectors; the Luna case lights up seven of them."""
    import math
    s='eleven-scenarios';cx,cy,r0,r1=560,312,96,176
    attrs=[('Accuracy','result vs expectation','target',1),('Adaptability','successful adaptations','notebook-pen',1),
           ('Efficiency','response time and cost','gauge',1),('Privacy','sensitive data protected','lock-keyhole',1),
           ('Security','time to detect, recover','shield-check',0),('Fairness','bias mitigation rate','scale',0),
           ('Availability','recovery time, uptime','server',0),('Observability','log completeness','eye',1),
           ('Transparency','users who understand why','file-text',1),('Safety','unsafe events avoided','shield-alert',0),
           ('Contestability','time to resolve a challenge','hand',1)]
    N=len(attrs);step=2*math.pi/N;gap=.022
    pt=lambda r,a:f'{cx+r*math.cos(a):.1f} {cy+r*math.sin(a):.1f}'
    def sector(k,cls):
        a0=-math.pi/2+k*step-step/2+gap;a1=a0+step-2*gap
        return f'<path d="M{pt(r0,a0)} L{pt(r1,a0)} A{r1} {r1} 0 0 1 {pt(r1,a1)} L{pt(r0,a1)} A{r0} {r0} 0 0 0 {pt(r0,a0)} Z" class="sector {cls}"/>'
    def icon(k,color):
        a=-math.pi/2+k*step;return svg_icon(attrs[k][2],round(cx+136*math.cos(a)-13),round(cy+136*math.sin(a)-13),26,color)
    base='';on=''
    for k,(name,measure,ic,chosen) in enumerate(attrs):
        a=-math.pi/2+k*step;c,sn=math.cos(a),math.sin(a)
        x,y=cx+250*c,cy+214*sn;anchor='start' if c>.2 else 'end' if c<-.2 else 'middle'
        ny,my=(y-36,y-2) if sn<-.5 else (y+22,y+56) if sn>.5 else (y-12,y+22)
        base+=sector(k,'off')+icon(k,'#7d8a90')+text(round(x),round(ny),name,'wheel-name',anchor)+text(round(x),round(my),measure,'node-sub',anchor)
        if chosen:on+=sector(k,'on')+icon(k,'#a62c40')
    base+=f'<circle cx="{cx}" cy="{cy}" r="84" class="hub-ring"/>'
    on+=f'<circle cx="{cx}" cy="{cy}" r="84" class="hub"/>'+text(cx,cy-10,'Luna chose','hub-sub','middle')+text(cx,cy+26,'7 of 11','hub-title','middle')
    body=group(base,1,'Eleven quality attributes with their response measures')+group(on,2,'The seven the Luna tax copilot selected')
    body+=f'<rect x="28" y="606" width="22" height="22" class="sector on"/>'+text(62,624,'chosen for the Luna tax copilot (§6.3) · measures from the general scenarios (§5)','diagram-note')
    return svg(s,'Eleven general scenarios and their measures','A wheel of the eleven quality attributes in AgentArcEval’s scenario catalogue, each with its general response measure; the Luna tax copilot selected accuracy, adaptability, efficiency, privacy, observability, transparency and contestability.',body),2

# === TOPIC 4 · CONTEXT ENGINEERING ===

def context_budget():
    s='context-budget'
    x0=200;W=880
    def bar(y,segs):
        out='';x=x0
        for frac,cls,lab in segs:
            w=round(W*frac);out+=f'<rect x="{x}" y="{y}" width="{w}" height="64" class="seg {cls}"/>'
            if lab:out+=text(x+14,y+40,lab,'seg-label')
            x+=w
        return out
    a=text(28,140,'Session start','plot-title')+bar(100,[(.12,'prefix','Prefix'),(.88,'free','Free budget')])
    a+=text(28,244,'Mid-task','plot-title')+bar(204,[(.12,'prefix','Prefix'),(.66,'history','Conversation + tool outputs'),(.22,'free','Free')])
    a+=text(200,300,'Prefix = system prompt, tool schemas, AGENTS.md, memory files, skill catalog','axis-label')
    b=f'<path d="M{x0+.5*W} 76 V284" class="threshold"/><path d="M{x0+.92*W} 76 V284" class="threshold"/>'
    b+=text(x0+.5*W-10,64,'Hermes · 50%','threshold-label','end')+text(x0+.92*W-10,64,'Pi · window − 16k','threshold-label','end')
    rows=[('Summarise in place',['Pi: older turns become a structured checkpoint; the full history stays on disk']),
          ('Summarise in the background',['Pi Durable: the summary is built while the conversation keeps going']),
          ('Rotate the session',['Hermes: compaction closes the session and opens a child; nothing is deleted'])]
    for i,(t,l) in enumerate(rows):b+=node(24,332+i*92,1072,84,t,l,'data' if i<2 else 'business',icon='scissors' if i<2 else 'git-fork')
    b+=note(628,'Proportions illustrative for a 200k-token window. Pi reserves 16,384 tokens by default; Hermes triggers at 50%.')
    body=group(a,1,'The window fills during a task')+group(b,2,'Two thresholds and three ways to free space')
    return svg(s,'Context is a budget','A fixed prefix plus a growing conversation fill the window; Hermes compacts at 50%, Pi when only a 16k reserve is left, and three harnesses free space in three different ways.',body),2

def agents_md_categories():
    s='agents-md-categories'
    cats=[('Conventions',50),('Contribution guidelines',48),('Architecture / structure',47),('Build commands',40),('Goals / purposes',32),('Test execution',32),
          ('Metadata',29),('Test strategy',24),('Tech stack',15),('Setup',11),('References',9),('Troubleshooting',8),('Patterns / examples',8),('Security',6)]
    x0=352;unit=11
    body=text(28,32,'Level-1 and level-2 headings per category · 155 AGENTS.md files','plot-title')+f'<path d="M{x0} 52 V612" class="axis"/>'
    a='';b=''
    for i,(c,n) in enumerate(cats):
        y=56+i*40;focus=c in ('Conventions','Security')
        row=text(x0-14,y+22,c,'axis-label','end')+f'<rect x="{x0}" y="{y+2}" width="{n*unit}" height="26" class="bar{" focus" if focus else ""}"/>'+text(x0+n*unit+10,y+23,str(n),'bar-value')
        if i<7:a+=row
        else:b+=row
    b+=text(x0+360,500,'Security and troubleshooting are rare.','annotation')
    body+=group(a,1,'Most frequent categories')+group(b,2,'Rare categories')
    return svg(s,'What goes into AGENTS.md','Conventions, contribution guidelines and architecture headings are most frequent across 155 AGENTS.md files; troubleshooting and security are rare.',body),2

def instruction_styles():
    s='instruction-styles'
    rows=[('Descriptive','states a fact','This project uses the Linux Kernel Style Guideline.'),
          ('Prescriptive','gives an order','Follow the existing code style and conventions.'),
          ('Prohibitive','sets a boundary','Never commit directly to the main branch.'),
          ('Explanatory','adds the reason','Avoid hard-coded waits to prevent timing issues in CI environments.'),
          ('Conditional','encodes a situation','If you need to use reflection, use ReflectionUtils APIs.')]
    body=''
    for i,(st,what,q) in enumerate(rows):
        y=16+i*118
        g=node(24,y,264,112,st,[what],'data',f'STYLE {i+1}','file-text')+text(320,y+52,'“'+q+'”','quote')
        body+=group(g,1 if i<2 else 2,st)
    body+=note(630,'Examples quoted from the Conventions sections studied by Mohsenimofidi et al. (§4.2); styles are often mixed in one file.')
    return svg(s,'Five ways to phrase an instruction','Descriptive, prescriptive, prohibitive, explanatory and conditional instructions, each with an example quoted from real AGENTS.md files.',body),2

def context_evolution():
    s='context-evolution'
    a=text(28,40,'How often was each file changed?','plot-title')+text(28,70,'one square per AGENTS.md file · 155 files','axis-label')
    cats=[('Never',77,'50%','w0'),('Once',36,'23%','w1'),('2–7 times',32,'21%','w2'),('10+ times',10,'6%','w3')]
    cells=[cls for _,n,_,cls in cats for _ in range(n)]
    for i,cls in enumerate(cells):a+=f'<rect x="{28+(i%13)*28}" y="{96+(i//13)*28}" width="24" height="24" rx="3" class="waffle {cls}"/>'
    for i,(lab,n,pct,cls) in enumerate(cats):
        y=468+i*34;a+=f'<rect x="28" y="{y}" width="22" height="22" rx="3" class="waffle {cls}"/>'+text(62,y+19,lab,'axis-label')+text(392,y+19,f'{n} · {pct}','bar-value','end')
    b=text(600,40,'What changed? (169 commits)','plot-title')+text(600,70,'the 10 files with ≥10 commits','axis-label')
    x1=852;u2=3
    for i,(lab,n) in enumerate([('Add instruction',78),('Modify instruction',59),('Add section',26),('Remove instruction',23),('Modify heading',23),('Modify text',19),('Reformat style',10)]):
        y=96+i*56;b+=text(x1-14,y+28,lab,'axis-label','end')+f'<rect x="{x1}" y="{y+6}" width="{n*u2}" height="30" class="bar{" focus" if i==0 else ""}"/>'+text(x1+n*u2+10,y+29,str(n),'bar-value')
    b+=f'<path d="M{x1} 88 V492" class="axis"/>'
    b+=text(600,560,'Mostly fine-tuning: instructions are added','annotation')+text(600,590,'and reworded, sections rarely removed.','annotation')
    body=group(a,1,'Change frequency')+group(b,2,'Change categories')
    body+=note(628,'Mohsenimofidi et al. (2026), §4.3, Table 2. A commit can belong to more than one category.')
    return svg(s,'Context files are maintained artifacts','Half of the 155 AGENTS.md files never changed; in the ten most active files, adding and modifying instructions dominate.',body),2

def context_tiers():
    """Iceberg: only the tip sits in the window; the rest waits below the waterline."""
    s='context-tiers';W=196
    tip='<path d="M250 52 L296 92 L322 140 L352 196 L144 196 L176 138 L214 86 Z" class="ice-top"/>'
    under='<path d="M352 196 L420 252 L462 352 L448 456 L398 548 L300 592 L184 584 L104 512 L68 404 L92 292 L144 196 Z" class="ice-under"/>'
    water=f'<rect x="8" y="{W}" width="1104" height="{632-W}" class="water"/><path d="M8 {W} H1112" class="waterline"/>'
    water+=text(1092,W-12,'IN THE CONTEXT WINDOW','lane-title','end')+text(1092,W+30,'OUTSIDE · BEHIND A TOOL CALL','lane-title','end')
    def tier(y,gx,tag,title,lines):
        out=f'<path d="M{gx} {y} H508" class="leader"/>'+text(528,y-36,tag,'node-tag')+text(528,y-6,title)
        for i,(marks,line) in enumerate(lines):
            lx=528
            for m in marks:out+=logo(m,lx,y+10+i*34,26);lx+=34
            out+=text(lx+(6 if marks else 0),y+30+i*34,line,'node-sub')
        return out
    t1=tier(92,330,'EVERY REQUEST','Always in context',[((),'System prompt · AGENTS.md · tool schemas · skill catalog'),(('hermes.png',),'MEMORY.md ≤ 2,200 and USER.md ≤ 1,375 characters')])
    t2=tier(300,468,'WHEN NEEDED','Loaded on demand',[((),'A skill’s full SKILL.md is read only when it is used'),(('pi.svg','hermes.png'),'Pi and Hermes both disclose skills progressively')])
    t3=tier(476,454,'NEVER DELETED','On disk, searchable',[(('pi.svg',),'Pi: JSONL session tree · Pi Durable: SQLite'),(('hermes.png','sqlite.svg'),'Hermes: SQLite sessions with full-text search')])
    body=group(water+tip+t1,1,'The tip: what every request carries')+group(under+t2,2,'Below the waterline: loaded when used')+group(t3,3,'The deep part: stored and searchable')
    return svg(s,'What stays in context, what waits on disk','An iceberg: only the always-loaded prefix sits in the context window; skills load on demand and session history stays on disk but searchable, with examples from Pi, Pi Durable and Hermes.',body),3

def subagents():
    s='subagents'
    a=arrow(s,264,320,328,320)
    a+=node(24,232,240,176,'Orchestrator',['delegates with','N prompts'],'model','PARENT','bot')
    a+=node(328,232,224,176,'Fan-out',['bounded','parallelism'],'data','HARNESS','split')
    b=edge(s,'M552 268 H572 Q580 268 580 260 V84 Q580 76 588 76 H616')+edge(s,'M552 300 H588 Q596 300 596 292 V232 Q596 224 604 224 H616')
    b+=edge(s,'M552 340 H588 Q596 340 596 348 V364 Q596 372 604 372 H616')+edge(s,'M552 372 H572 Q580 372 580 380 V512 Q580 520 588 520 H616')
    for i,y in enumerate([8,156,304,452]):b+=node(616,y,224,136,f'Worker {i+1}',['own context'],'data','FRESH CONTEXT','search')
    c=edge(s,'M840 76 H876 Q884 76 884 84 V260 Q884 268 892 268 H904')+edge(s,'M840 224 H860 Q868 224 868 232 V292 Q868 300 876 300 H904')
    c+=edge(s,'M840 372 H860 Q868 372 868 364 V348 Q868 340 876 340 H904')+edge(s,'M840 520 H876 Q884 520 884 512 V380 Q884 372 892 372 H904')
    c+=node(904,232,192,176,'Reports',['short','summaries'],'data','RESULT','file-text')
    c+=edge(s,'M1000 408 V608 Q1000 616 992 616 H152 Q144 616 144 608 V408')+side_label(360,604,'ONE TOOL RESULT','middle')
    body=group(a,1,'Orchestrator and bounded fan-out')+group(b,2,'Workers with their own context')+group(c,3,'Compressed reports return as one tool result')
    return svg(s,'Subagents are context engineering','The orchestrator delegates several prompts; a bounded number of workers run with fresh contexts, and each returns a short report folded into one tool result.',body),3

# === TOPIC 5 · OUTLOOK ===

def runtime_spectrum():
    """Staircase: each step keeps the loop and adds state, triggers and reach."""
    s='runtime-spectrum'
    steps=[(24,400,'Pi coding agent','SESSION AGENT',('pi.svg',),'',['a person starts it','state: JSONL session tree','crash: ask it to continue','reached from a terminal'],'data'),
           (392,272,'Pi Durable','DURABLE HARNESS · LIBRARY',('pi.svg',),'+ crash-safe state',['your application submits work','state: a checkpoint per step','crash: resume() continues','experimental, beside Pi 1.0'],'data'),
           (760,144,'Hermes Agent','ALWAYS-ON AGENT',('hermes.png',),'+ triggers and memory',['chats and schedules start it','state: SQLite + Markdown memory','writes and patches its skills','reached from chat apps:'],'model')]
    body=text(28,52,'Same loop at the core.','annotation')+text(28,84,'What grows: state, triggers and reach.','annotation')
    for i,(x,top,name,tag,marks,add,lines,role) in enumerate(steps):
        g=logo(marks[0],x+4,top-68,52)+text(x+68,top-44,tag,'node-tag')+text(x+68,top-14,name)
        g+=f'<g data-node="{name}"><rect x="{x}" y="{top}" width="336" height="{600-top}" rx="6" class="node {role}"/>'
        y=top+40
        if add:g+=text(x+20,y,add,'step-add');y+=40
        for line in lines:g+=text(x+20,y,line,'node-sub');y+=32
        if role=='model':
            for k,m in enumerate(('telegram.svg','discord.svg','slack.svg','whatsapp.svg','signal.svg')):g+=logo(m,x+20+k*44,y-6,30)
        body+=group(g+'</g>',i+1,name)
    body+=note(628,'Our framing of three points on a spectrum. Hermes (Nous Research) is a separate project, not built on Pi.')
    return svg(s,'From session agent to always-on agent','A staircase of three runtimes: the Pi coding agent run per session, Pi Durable adding crash-safe state, and Hermes adding triggers, memory and chat-app reach.',body),3

def durable_recovery():
    s='durable-recovery'
    l1=zone(8,'BEFORE THE CRASH',224)
    for i,(t,l,r,ic) in enumerate([('Submit',['job + requestId'],'business','send'),('Model step',['checkpoint stored'],'model','brain-circuit'),
        ('Tool step',['intent stored first'],'data','wrench'),('Process dies',['mid tool call'],'plain','circle-alert')]):
        x=24+i*272;l1+=node(x,64,248,128,t,l,r,icon=ic)
        if i:l1+=arrow(s,x-24,128,x,128)
    l2=edge(s,'M916 192 V236 Q916 244 908 244 H248 Q240 244 240 252 V312')
    l2+=zone(256,'AFTER A RESTART',224).replace('x="8" y="256" width="1104"','x="8" y="256" width="1104"')
    for i,(t,l,r,ic) in enumerate([('New process',['opens storage','calls resume()'],'business','rocket'),('Model step',['sent again; partial','answer kept, aborted'],'model','brain-circuit'),
        ('Tool step',['reruns if “safe”;','else model is told'],'data','wrench'),('Same answer',['retried submit gets','the original result'],'data','circle-check')]):
        x=24+i*272;l2+=node(x,312,248,148,t,l,r,icon=ic)
        if i:l2+=arrow(s,x-24,386,x,386)
    st=node(24,512,1072,104,'Storage',['memory · JSONL · SQLite — one process owns it at a time; every step commits before it moves on'],'data',icon='database')
    body=group(l1,1,'A run is interrupted')+group(st,2,'Every step is checkpointed')+group(l2,3,'A new process resumes from the last checkpoint')
    return svg(s,'Pi Durable: surviving a crash','Every model and tool step is a task that checkpoints before it moves on; after a crash a new process opens the same storage, resumes open tasks, reruns only safe tools and answers a retried submission once.',body),3

def hermes_architecture():
    s='hermes-architecture'
    a=''
    for y,h,(t,l,ic) in [(16,112,('CLI',['terminal'],'terminal')),(152,152,('Gateway',['chat apps + email'],'message-square')),(328,112,('ACP',['editor clients'],'file-code'))]:
        a+=node(24,y,224,h,t,l,'business','ENTRY',ic)
    a+=''.join(logo(m,40+k*38,264,28) for k,m in enumerate(('telegram.svg','discord.svg','slack.svg','whatsapp.svg','signal.svg')))
    a+=edge(s,'M248 72 H264 Q272 72 272 80 V216 Q272 224 280 224 H312')+arrow(s,248,280,312,280)+edge(s,'M248 384 H280 Q288 384 288 376 V344 Q288 336 296 336 H312')
    a+=node(312,168,288,280,'Agent core',['one loop per turn','budget: 90 steps','verify-on-stop','guard'],'model','AIAGENT')+logo('hermes.png',540,180,48)
    b=node(24,464,224,152,'Cron',['ticks, reads','jobs.json'],'business','SCHEDULE','clock')
    b+=edge(s,'M248 540 H264 Q272 540 272 532 V400 Q272 392 280 392 H312')
    b+=text(312,500,'Compaction at 50%','annotation')+text(312,532,'rotates the session.','annotation')
    c=edge(s,'M600 224 H624 Q632 224 632 216 V92 Q632 84 640 84 H664')+edge(s,'M600 280 H636 Q644 280 644 272 V252 Q644 244 652 244 H664')
    c+=edge(s,'M600 336 H636 Q644 336 644 344 V396 Q644 404 652 404 H664')+edge(s,'M600 392 H624 Q632 392 632 400 V548 Q632 556 640 556 H664')
    for y,h,(t,l,tag,ic) in [(16,136,('Memory files',['soul.md · USER.md · MEMORY.md'],'ALWAYS IN CONTEXT','file-text')),(176,136,('Session store',['SQLite · full-text search'],'HISTORY',None)),
        (336,136,('Skills',['written and patched by the agent'],'SELF-IMPROVING','puzzle')),(496,120,('Tools',['69 built in, scoped per platform'],'ACT','wrench'))]:
        c+=node(664,y,432,h,t,l,'data',tag,ic)+(logo('sqlite.svg',1052,186,32) if ic is None else '')
    body=group(a,1,'Three entry points into one agent core')+group(b,2,'A scheduler starts work without a person')+group(c,3,'Memory, sessions, skills and tools')
    return svg(s,'Hermes: an always-on agent','CLI, messaging gateway and ACP clients feed one agent core; a cron scheduler starts work on its own; memory files, an SQLite session store, self-written skills and 69 tools surround the loop.',body),3

def platform_turn():
    """Exploded stack: four plates pulled apart, each labelled with the systems that live there."""
    s='platform-turn';x0,W,H,S,T=110,380,64,72,16
    layers=[('Meta-harness','business','META-HARNESS · ORCHESTRATES HARNESSES',['Omnigent: adapters for 23 harnesses,','one API, sandbox and policy above them'],('claude-code.svg','codex.svg','opencode.svg','hermes.png','pi.svg')),
            ('Harness as platform','data','DISTRIBUTION',['SDKs · libraries like Pi Durable','ACP servers · skill marketplaces'],('pi.svg','mcp.svg')),
            ('Harness','data','RUNTIME · LOOP + SEVEN SUBSYSTEMS',['The eleven harnesses of the study,','for example:'],('pi.svg','hermes.png','claude-code.svg','codex.svg','gemini-cli.svg','opencode.svg')),
            ('Foundation model','model','CAPABILITY',['Co-evolves with its harness:','prompts, tools, caching per model'],('anthropic.svg','openai.svg','gemini.svg','mistral.svg'))]
    groups=['','']
    for i,(name,role,tag,lines,marks) in enumerate(layers):
        y=24+i*148
        g=f'<g data-plate="{name}"><path d="M{x0+S} {y} H{x0+S+W} L{x0+W} {y+H} H{x0} Z" class="node {role}"/>'
        g+=f'<rect x="{x0}" y="{y+H}" width="{W}" height="{T}" class="plate-edge {role}"/>'
        g+=text(x0+S/2+W/2,y+H/2+9,name,'node-title','middle')+'</g>'
        if i<3:g+=''.join(f'<path d="M{px} {y+H+T} V{y+148}" class="leader"/>' for px in (x0+S+24,x0+W-24))
        g+=f'<path d="M{x0+W+S//2} {y+H//2} H588" class="leader"/>'
        g+=text(604,y+8,tag,'node-tag')+text(604,y+38,lines[0],'node-sub')+text(604,y+70,lines[1],'node-sub')
        g+=''.join(logo(m,604+k*48,y+88,32) for k,m in enumerate(marks))
        groups[0 if i>=2 else 1]+=g
    body=group(groups[0],1,'Foundation model and harness')+group(groups[1],2,'Harness as platform and meta-harness')
    body+=text(28,630,'Harnesses ship as SDKs while framework vendors ship harnesses: the two categories are merging.','aside-title')
    return svg(s,'The platform turn','An exploded stack of four layers: the foundation model, the harness, the harness as a platform with SDKs and marketplaces, and a meta-harness that orchestrates other harnesses.',body),2

# === PAPER FIGURES, TABLES AND PANELS ===

def table_figure(headers,rows,widths,cls=''):
    cols='<colgroup>'+''.join(f'<col style="width:{w}%">' for w in widths)+'</colgroup>'
    body=''.join('<tr>'+''.join(f'<td>{c}</td>' for c in row)+'</tr>' for row in rows)
    return f'<div class="lecture-table {cls}"><table>{cols}<thead><tr>'+''.join(f'<th>{escape(h)}</th>' for h in headers)+f'</tr></thead><tbody>{body}</tbody></table></div>',0

def agent_ecosystem():
    s='agent-ecosystem'
    a=node(24,72,224,128,'User',['states a goal'],'business','INPUT','message-square')+arrow(s,248,136,304,136)
    ag=zone(8,'AGENT · PATTERNS INSIDE',560).replace('x="8" y="8" width="1104"','x="272" y="8" width="456"').replace('x="28" y="44"','x="292" y="44"')
    a=ag+a+node(304,72,400,128,'Goal creator',['passive or proactive'],'data','GOALS','target')
    b=arrow(s,504,200,504,232)+node(304,232,400,152,'Plan generator',['single- or multi-path','incremental querying'],'data','PLANNING','list-checks')
    b+=arrow(s,504,384,504,416)+node(304,416,400,128,'Reflection',['self · cross · human'],'data','CHECKS','circle-check')
    b+=edge(s,'M304 480 H296 Q288 480 288 472 V316 Q288 308 296 308 H304')
    c=edge(s,'M704 262 H736 Q744 262 744 254 V88 Q744 80 752 80 H784')+edge(s,'M704 293 H752 Q760 293 760 285 V240 Q760 232 768 232 H784')
    c+=edge(s,'M704 323 H752 Q760 323 760 331 V376 Q760 384 768 384 H784')+edge(s,'M704 354 H736 Q744 354 744 362 V528 Q744 536 752 536 H784')
    for y,(t,l,r,tag,ic) in zip([16,168,320,472],[('Foundation model',['queried each step'],'model','MODEL','brain-circuit'),('Knowledge',['memory · retrieval'],'data','RAG','database'),
        ('Registry',['finds tools, agents'],'data','REGISTRY','list-checks'),('Tools, workers',['via adapters'],'data','ACT','wrench')]):
        c+=node(784,y,312,128,t,l,r,tag,ic)
    body=group(a,1,'A user goal enters the agent')+group(b,2,'Planning and reflection inside the agent')+group(c,3,'Model, knowledge, registry and tools outside it')
    body+=note(612,'Simplified from Liu et al. (2025), Fig. 2: the catalogue’s pattern labels become the boxes.')
    return svg(s,'A shared vocabulary for agent design','A user goal enters an agent whose goal creator, plan generator and reflection patterns call a foundation model, a knowledge store, a registry and tools through adapters.',body),3

def arceval_process():
    s='arceval-process'
    a=node(24,176,256,248,'Understand',['agent goals','governance needs','quality + guardrails','the architecture'],'business','STEP 1','compass')
    d=zone(8,'DESIGN TIME',280).replace('x="8" y="8" width="1104"','x="312" y="8" width="528"').replace('x="28" y="44"','x="332" y="44"')
    d+=edge(s,'M280 238 H288 Q296 238 296 230 V156 Q296 148 304 148 H336')
    d+=node(336,88,224,120,'Define',['context scenarios'],'data',icon='clipboard-check')+arrow(s,560,148,592,148)+node(592,88,224,120,'Prioritise',['by impact + risk'],'data',icon='list-checks')
    d+=edge(s,'M816 148 H836 Q844 148 844 156 V250 Q844 258 852 258 H872')
    d+=node(872,176,224,248,'Analyse',['trade-offs','risks','improvements'],'model','RESULT','scale')
    r=zone(312,'RUNTIME',280).replace('x="8" y="312" width="1104"','x="312" y="312" width="528"').replace('x="28" y="348"','x="332" y="348"')
    r+=edge(s,'M280 362 H288 Q296 362 296 370 V444 Q296 452 304 452 H336')
    r+=node(336,392,224,120,'Monitor',['risks while running'],'data',icon='eye')+arrow(s,560,452,592,452)+node(592,392,224,120,'Reprioritise',['update scenarios'],'data',icon='repeat-2')
    r+=edge(s,'M816 452 H836 Q844 452 844 444 V350 Q844 342 852 342 H872')
    r+=edge(s,'M984 424 V600 Q984 608 976 608 H456 Q448 608 448 600 V512')+side_label(716,594,'AFTER EACH CHANGE','middle')
    body=group(a,1,'Understand goals, governance, requirements and architecture')+group(d,2,'Design time: define and prioritise scenarios, then analyse')+group(r,3,'Runtime: monitor, reprioritise and analyse again')
    return svg(s,'AgentArcEval: the process','After understanding goals, governance, requirements and the architecture, evaluation splits into a design-time path of defining and prioritising scenarios and a runtime path of monitoring and reprioritising, both feeding analysis and improvement.',body),3

def context_funnel():
    """Area-true circles: the population shrinks from 10,000 to 155."""
    import math
    s='context-funnel';cx,base=300,604
    rows=[(10000,'10,000',('popular GitHub','repositories scanned'),'plain',140),(466,'466',('had an AI context','file · about 5%'),'data',506),(155,'155',('AGENTS.md files','analysed in depth'),'model',584)]
    groups=[]
    for n,num,(d1,d2),role,ly in rows:
        r=260*math.sqrt(n/10000);c=base-r;dx=math.sqrt(max(r*r-(ly-c)**2,0))
        g=f'<circle cx="{cx}" cy="{c:.1f}" r="{r:.1f}" class="node {role}"/>'
        g+=f'<path d="M{cx+dx:.1f} {ly} H636" class="leader"/><circle cx="{cx+dx:.1f}" cy="{ly}" r="4" class="dot-ink"/>'
        g+=text(656,ly+16,num,'funnel-num')+text(856,ly-6,d1,'aside-sub')+text(856,ly+28,d2,'aside-sub')
        groups.append(g)
    fm=text(656,258,'FORMATS FOUND','lane-title')
    for i,(m,lab) in enumerate([('copilot.svg','Copilot instructions'),('claude-code.svg','CLAUDE.md'),('agentsmd.png','AGENTS.md'),('gemini.svg','GEMINI.md')]):
        x=656+(i%2)*270;y=278+(i//2)*48;fm+=logo(m,x,y,30)+text(x+42,y+24,lab,'aside-sub')
    groups[1]+=fm
    groups[2]+=text(656,416,'453 commits to these 155 files','aside-sub')+text(656,450,'show how they change over time.','aside-sub')
    body=''.join(group(g,i+1,l) for i,(g,l) in enumerate(zip(groups,['10,000 repositories scanned','466 with an AI context file','155 AGENTS.md files analysed'])))
    body+=text(28,630,'Circle areas to scale · Mohsenimofidi et al. (2026), §3','diagram-note')
    return svg(s,'Who actually writes context files','Area-proportional circles: 10,000 popular repositories, 466 of them with an AI context file, and 155 AGENTS.md files analysed in depth.',body),3

CODE='''<span class="c"># Condensed from the paper's ~90-line minimum viable harness</span>
<b>class</b> Agent:
    <b>async def</b> run(self, task):
        self.messages = [system(discover_context()),  <span class="c"># AGENTS.md, root → leaf</span>
                         user(task)]
        <em>while True:</em>
            self._check_limits()           <span class="c"># max turns, max cost</span>
            <b>await</b> self._maybe_compact()    <span class="c"># summary + last 30% verbatim</span>
            resp = <b>await</b> self.model.complete(self.messages, tools=SCHEMAS)
            self.messages.append(resp)
            <em>if not resp.get("tool_calls"):</em>
                <em>return resp["content"]</em>     <span class="c"># no tool call → done</span>
            <b>for</b> call <b>in</b> resp["tool_calls"]:  <span class="c"># serial execution</span>
                out = TOOLS[call["name"]](**call["args"])
                self.messages.append(tool_result(call, out))

TOOLS = {"bash": ..., "read_file": ...,
         "write_file": ..., "search_replace": ...}   <span class="c"># 4 tools</span>'''

def code_panel():
    return f'<div class="code-panel"><div class="code-bar"><span></span><span></span><span></span><b>minimum_viable_harness.py</b></div><pre>{CODE}</pre><p class="figure-credit">Condensed from Barbaste et al. (2026), Listing 3. Illustrative scaffold, not production code.</p></div>',0
