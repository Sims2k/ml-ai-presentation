"""Day 2 — Agentic AI Architecture. Topic-led, no running example.

Each slide: a big figure on the left and a key-concepts column on the right.
`cues` are up to four short key points the audience reads (max 4); `takeaway` is
the one sentence to keep. The column is shown to everyone, so cues state ideas;
directions for the presenter live in the speaker notes.
Real systems appear as evidence: Pi, Pi Durable and Hermes, plus the eleven
harnesses of the source-code study. Paper numbers come from the cited sections.
"""
from day2_visuals import *

HARNESS='Barbaste et al. (2026), Harness Engineering, arXiv:2609.00006'
CATALOGUE='Liu et al. (2025), Agent Design Pattern Catalogue, JSS 220'
ARCEVAL='Lu et al. (2026), AgentArcEval, JSS 232'
CONTEXT='Mohsenimofidi et al. (2026), Context Engineering for AI Agents in OSS, MSR ’26'
PI='Zechner (2025); Pi docs, github.com/earendil-works/pi'
DURABLE='Earendil (2026), Pi Durable, earendil.com/posts/pi-durable'
HERMES='Nous Research, Hermes Agent docs; Alejandro AO (2026), Hermes architecture'

O='Opening';H='Topic 1 / Harness engineering';P='Topic 2 / Design patterns';E='Topic 3 / Architecture evaluation'
C='Topic 4 / Context engineering';F='Topic 5 / From sessions to always-on agents';D='Discussion'

def build_day2():
    slides=[]
    def add(title,section,owner,lead,visual,cues,takeaway,source,icon='book-open',layout='standard'):
        assert layout!='standard' or 1<=len(cues)<=4,title
        slides.append(dict(title=title,section=section,owner=owner,lead=lead,visual=visual,cues=cues,
                           takeaway=takeaway,source=source,icon=icon,layout=layout))

    add('Agentic AI Architecture',O,'All presenters','From a model in a pipeline to a model that acts.',None,[],'','',layout='cover')
    add('Five questions in forty minutes',O,'All presenters','Each presenter answers one question, grounded in one paper.',
        lambda:table_figure(['Time','Presenter','Question','Main source'],[
            ['0–2','All','Why go one layer up from Day 1?','—'],
            ['2–9','Ricardo','What is a harness?','Barbaste et al. (2026)'],
            ['9–15','Tomás','Which patterns describe an agent?','Liu et al. (2025)'],
            ['15–21','Simon','How do we evaluate its architecture?','Lu et al. (2026)'],
            ['21–29','Luca','What does context engineering look like?','Mohsenimofidi et al. (2026)'],
            ['29–37','Matheus','What changes when agents run always-on?','Pi Durable · Hermes'],
            ['37–40','All','Discussion','—']],[9,15,44,32]),
        ['<b>Five topics</b>, each self-contained: one question, one main source.','<b>Real systems as evidence:</b> Pi, Pi Durable, Hermes and the eleven harnesses of one source-code study.',
         '<b>Topic-led:</b> no single running example this time.','<b>Discussion</b> reserved for the last three minutes.'],
        'Same question as Day 1, one layer up: what must surround the model?','Group handoff · Day 2 outline',icon='list-checks')
    add('One layer up from Day 1',O,'Ricardo','Day 1 put a model inside a system. Day 2 puts it inside a loop that acts.',one_layer_up,
        ['<b>Day 1:</b> a one-way path from records to a business decision.','<b>Day 2:</b> the model chooses an action, not just a score.',
         '<b>The return arrow</b> is new: results flow back as context.','<b>Same engineering question:</b> what must surround the model?'],
        'An agent is still a model inside an architecture — now one that loops.','Day 1 lecture · '+HARNESS+', §1',icon='layers')

    add('Agent = model + harness',H,'Ricardo','The harness is everything except the model. A source-code study of eleven harnesses found the same seven subsystems in all of them.',harness_anatomy,
        ['<b>Agent loop</b> at the centre: model → tool → observation.','<b>Six more subsystems:</b> LLM access, tools, safety, memory, orchestration, extensions.',
         '<b>Every harness takes a position</b> on all seven, even if it is “none”.','<b>Interfaces</b> sit on top: terminal, editors, chat gateways.'],
        'The harness is the part you can engineer.',HARNESS+', §2.3, Table 1',icon='blocks')
    add('Eleven harnesses, from one tool to 109',H,'Ricardo','The same seven subsystems, built with tool surfaces that differ by two orders of magnitude.',tool_spectrum,
        ['<b>Minimal end:</b> Mini-SWE-Agent works through one bash tool; Pi exposes four by default.','<b>Maximal end:</b> Hermes registers 69 tools and scopes them per platform; OpenClaw ships 109.',
         '<b>More code is not better results:</b> loop sophistication does not predict benchmark performance.','<b>Most code goes elsewhere:</b> safety, user experience, extensibility and clients.'],
        'Tool count is a design philosophy, not a quality score.',HARNESS+', §5 Table 4, §8.1 Fig. 3',icon='wrench')
    add('The agent loop: decide, act, observe',H,'Ricardo','One cycle repeats until the model answers in text instead of calling a tool.',agent_loop,
        ['<b>The context window accumulates state:</b> every pass writes into it.','<b>Clockwise:</b> model → permission gate → tool → observation.',
         '<b>Steering input</b> waits for a safe boundary, never mid-tool-call.','<b>Stop conditions differ:</b> no cap in Pi, a 90-step budget in Hermes.'],
        'A loop with a growing context — everything else manages that loop.',HARNESS+', §6',icon='repeat-2')
    add('Pi: a minimal core, everything else an extension',H,'Ricardo','Pi keeps the core small and moves safety, sub-agents and plan mode into extensions.',pi_architecture,
        ['<b>Four layers:</b> interfaces → product → loop → model gateway.','<b>Session tree:</b> JSONL entries you can fork and rewind.',
         '<b>Extension host:</b> sub-agents, plan mode and permissions hook into the event stream.','<b>Trade-off:</b> a small core, but safety depends on what you install.'],
        'Minimal core plus extensions is one coherent harness architecture.',HARNESS+', §10–12 · '+PI,icon='package')
    add('What eleven harnesses share — and lack',H,'Ricardo','Production harnesses converge on skills and context files, and all skip two popular technologies.',harness_absences,
        ['<b>Shared:</b> skills, summarised history, Markdown context files, MCP.','<b>Absent everywhere:</b> agentic frameworks and embedding search over code.',
         '<b>Instead:</b> hand-rolled async loops and deterministic search (grep, LSP).','<b>Next:</b> a vocabulary for the agent inside the loop.'],
        'The field runs on simple loops and deterministic retrieval.',HARNESS+', §13.2, Observation 8–9',icon='chart-no-axes-combined')

    add('A shared vocabulary for agent design',P,'Tomás','A systematic review of 57 studies distilled 18 architectural patterns for foundation-model agents.',agent_ecosystem,
        ['<b>Inside the agent:</b> goal creation, planning, reflection.','<b>Outside it:</b> the model, knowledge, a registry, tools and workers.',
         '<b>Each pattern</b> documents context, forces, solution, consequences, known uses.','<b>Why it matters:</b> two teams can compare designs precisely.'],
        'Patterns let us name a design choice and its trade-off.',CATALOGUE+', §2–4, Fig. 2',icon='book-open')
    add('Eighteen patterns in eight families',P,'Tomás','Group the catalogue by the question each pattern answers.',pattern_families,
        ['<b>Eight families</b>, from goal creation to evaluation.','<b>Most agents combine</b> several small patterns.',
         '<b>Deep dive on three:</b> planning, reflection, registry.','<b>Coding harnesses skip RAG</b> and use grep and the language server instead.'],
        'Most agents combine many small patterns, not one big one.',CATALOGUE+', Table 1 · '+HARNESS+', §13.2',icon='blocks')
    add('Planning: one path or many?',P,'Tomás','A plan generator decomposes a goal; the choice is how many options it keeps open.',planning,
        ['<b>Single path:</b> one ordered list — cheap, simple, explainable.','<b>Multi-path:</b> options per step, compared before choosing.',
         '<b>Trade-off:</b> multi-path improves certainty but costs more model calls.','<b>A visible plan</b> lets people correct it early.'],
        'Most coding agents choose a single, visible plan.',CATALOGUE+', §4.7–4.8',icon='list-checks')
    add('Reflection: who checks the work?',P,'Tomás','Reflection patterns differ by who gives the feedback: the agent, another agent, or a person.',reflection,
        ['<b>Self:</b> cheap and fast, limited by the agent’s own blind spots.','<b>Cross:</b> a second agent adds a perspective, and cost.',
         '<b>Human:</b> aligns with preferences, adds latency and contestability.','<b>Real harnesses mix all three</b> at different moments.'],
        'Choose the reviewer by the cost of a wrong action.',CATALOGUE+', §4.9–4.11 · '+HARNESS+', §6',icon='circle-check')
    add('Registries and adapters: finding capabilities',P,'Tomás','A registry makes tools and agents discoverable; an adapter connects the loop to outside systems.',registry,
        ['<b>Registry:</b> tool schemas, skills and agent personas in one place.','<b>Load on use:</b> skills and agents enter the context only when needed.',
         '<b>Adapter:</b> MCP or JSON-RPC to servers, language servers and sandboxes.','<b>Scale:</b> Hermes registers 69 tools but shows each platform a subset.'],
        'Registries keep the loop small while capabilities grow.',CATALOGUE+', §4.16–4.17 · '+HARNESS+', §8',icon='plug')
    add('Choosing patterns: the decision model',P,'Tomás','The catalogue’s decision model asks one question per design problem.',
        lambda:table_figure(['Decision','Yes →','No →'],[
            ['Capture the user’s environment?','Proactive goal creator','Passive goal creator'],
            ['Use an external data store?','Retrieval-augmented generation','Model + tools only'],
            ['Query the model several times?','Incremental model querying','One-shot model querying'],
            ['Several options per plan step?','Multi-path plan generator','Single-path plan generator'],
            ['Multiple agents collaborate?','Cross-reflection, cooperation','Self- or human reflection'],
            ['Use external tools or agents?','Tool/agent registry, adapter','—'],
            ['Assess agent performance?','Agent evaluator','—']],[40,32,28]),
        ['<b>One question per row</b>, two answers.','<b>Each answer has consequences</b> — benefits and costs.',
         '<b>A design</b> is a coherent set of answers.','<b>Next:</b> how do we judge whether the choices are good?'],
        'A pattern is chosen by a question, not by fashion.',CATALOGUE+', §5.1, Fig. 19',icon='split')

    add('Why architecture evaluation must change',E,'Simon','Classic scenario-based methods assume fixed requirements; agents decide much of their architecture at runtime.',evaluation_shift,
        ['<b>Goals</b> are decomposed into sub-tasks while the agent runs.','<b>The agent makes trade-offs</b> — inside guardrails we design.',
         '<b>Model, prompts and tools</b> change after evaluation.','<b>New scenarios</b> are needed for memory, tools and guardrails.'],
        'Guardrails become the main architectural control point.',ARCEVAL+', §1',icon='scale')
    add('AgentArcEval: the process',E,'Simon','An ATAM-based method that evaluates agent architecture at design time and keeps re-evaluating at runtime.',arceval_process,
        ['<b>Understand first:</b> goals, governance, quality and guardrail requirements, the architecture.','<b>Design time:</b> define and prioritise context scenarios.',
         '<b>Runtime:</b> monitor risks and reprioritise scenarios.','<b>Output:</b> trade-offs, risks, improvements.'],
        'Agent architecture evaluation never really ends.',ARCEVAL+', §4, Fig. 2',icon='workflow')
    add('A quality scenario in six parts',E,'Simon','Each scenario follows source → stimulus → environment → artefact → response → measure.',scenario_template,
        ['<b>Source and stimulus:</b> who triggers what.','<b>Artefact:</b> the part of the architecture under test.',
         '<b>Environment:</b> the conditions that make it hard.','<b>Measure</b> makes the scenario checkable.'],
        'A scenario is only useful if its measure can fail.',ARCEVAL+', §5, §6.4',icon='clipboard-check')
    add('Eleven general scenarios and their measures',E,'Simon','The catalogue gives one starter scenario per quality attribute; teams adapt and prioritise them.',eleven_scenarios,
        ['<b>Eleven attributes</b>, from accuracy to contestability.','<b>Each comes with a measure</b> a team can track.',
         '<b>Prioritising</b> is where the domain enters.','<b>Luna tax copilot</b> chose 7 of the 11.'],
        'Prioritising scenarios is where the domain enters the evaluation.',ARCEVAL+', §5–6',icon='badge-check')
    add('Scenarios as a lens on real harnesses',E,'Simon','The same scenario catalogue exposes where real harnesses put their architectural effort.',
        lambda:table_figure(['Scenario','Pi','Pi Durable','Hermes'],[
            ['Safety','None in the core, by design; extensions add it','Hooks can block a tool call; approvals stored as memos','Approval module; a hard floor of blocked commands'],
            ['Availability','You restart and ask it to continue','resume() continues open tasks after a crash','Long-running gateway process'],
            ['Observability','Full JSONL session tree on disk','Every step committed; clients watch live','SQLite sessions with full-text search'],
            ['Efficiency','Compacts when only a 16k reserve is left','Compacts in the background','Compacts at 50%; rotates the session'],
            ['Adaptability','Extensions reload without a build step','Extensions replaced while running','Agent writes and patches its own skills']],[16,28,28,28]),
        ['<b>Rows</b> are AgentArcEval attributes; cells are architectural mechanisms.','<b>Pi</b> optimises for a person at a terminal.',
         '<b>Pi Durable</b> optimises for availability.','<b>Hermes</b> invests in safety policy and self-improvement.'],
        'A scenario catalogue makes the trade-offs between harnesses visible.',ARCEVAL+' · our mapping from '+HARNESS+', '+DURABLE,icon='scale')

    add('Context is a budget',C,'Luca','Context engineering decides what task-relevant information the model has — and what it does not.',context_budget,
        ['<b>Prompt engineering:</b> how a task is described.','<b>Context engineering:</b> what information the model can access.',
         '<b>The window fills</b> with every tool output.','<b>Compaction</b> frees space — at different thresholds and in different ways.'],
        'Every token in the window competes for the model’s attention.',CONTEXT+', §1 · '+HARNESS+', §7',icon='gauge')
    add('Who actually writes context files?',C,'Luca','An empirical study scanned 10,000 popular GitHub projects for AI context files.',context_funnel,
        ['<b>Formats:</b> Copilot instructions, CLAUDE.md, AGENTS.md, GEMINI.md.','<b>Adoption is early:</b> only 5% of mature projects.',
         '<b>AGENTS.md</b> is the tool-agnostic convention, so it is studied in depth.','<b>Most common pair:</b> AGENTS.md with CLAUDE.md.'],
        'Context engineering is real practice, but still early.',CONTEXT+', §3–4.1',icon='database')
    add('What goes into AGENTS.md',C,'Luca','Projects describe conventions, contribution rules and architecture — rarely security.',agents_md_categories,
        ['<b>Top three:</b> conventions, contribution guidelines, architecture.','<b>Then:</b> build and test commands — what an agent must run.',
         '<b>Rare:</b> troubleshooting and security.','<b>No shared structure</b> yet across projects.'],
        'Teams document how to work here, not how to stay safe.',CONTEXT+', §4.2, Table 1',icon='file-text')
    add('Five ways to phrase an instruction',C,'Luca','The same convention can describe, order, forbid, explain or set a condition.',instruction_styles,
        ['<b>Descriptive</b> states facts; <b>prescriptive</b> gives orders.','<b>Prohibitive</b> sets boundaries — “never …”.',
         '<b>Explanatory</b> adds the reason; <b>conditional</b> a situation.','<b>Open question:</b> which style changes agent behaviour most?'],
        'How you phrase context is a design choice, not a detail.',CONTEXT+', §4.2',icon='message-square')
    add('Context files are maintained artifacts',C,'Luca','Half the files never change; active ones are tuned instruction by instruction.',context_evolution,
        ['<b>50% unchanged</b> since they were added.','<b>Active files:</b> mostly add or reword instructions.',
         '<b>Few removals:</b> files tend to grow.','<b>Treat them like code:</b> versioned, reviewed, tested.'],
        'Context files co-evolve with the code they describe.',CONTEXT+', §4.3, Table 2',icon='git-branch')
    add('What stays in context, what waits on disk',C,'Luca','Harnesses keep the always-loaded context small and move the rest behind a tool call.',context_tiers,
        ['<b>Always loaded:</b> instructions, schemas, a skill catalog, small memory files.','<b>On demand:</b> a skill’s full text only when it is used.',
         '<b>On disk:</b> full history, searchable but out of the window.','<b>Hermes caps memory</b> at a few thousand characters on purpose.'],
        'Load context just in time, not just in case.',HARNESS+', §7, §15 · '+HERMES,icon='notebook-pen')
    add('Subagents are context engineering',C,'Luca','A subagent spends tokens exploring in its own context and returns one short report.',subagents,
        ['<b>The orchestrator</b> delegates several prompts at once.','<b>Workers</b> start with a fresh context and keep their search noise.',
         '<b>The parent keeps</b> only the call and the reports.','<b>Hermes</b> runs one child by default; in Pi Durable a subagent is a conversation owned by a tool call.'],
        'The harness decides what the orchestrator never sees.',HARNESS+', §11, Rec. 12 · '+DURABLE,icon='bot')

    add('From session agent to always-on agent',F,'Matheus','The same loop can run per session, survive crashes, or run all the time — each step adds state and responsibility.',runtime_spectrum,
        ['<b>Pi:</b> a person at a terminal starts and supervises each run.','<b>Pi Durable:</b> a library for apps whose agents must survive restarts.',
         '<b>Hermes:</b> started by chats and schedules, not only by people.','<b>What grows:</b> state, triggers and the surfaces that reach the agent.'],
        'Always-on is an architectural decision, not a feature flag.',PI+' · '+DURABLE+' · '+HERMES,icon='route')
    add('Pi Durable: surviving a crash',F,'Matheus','Every step is a task that stores a checkpoint before it moves on.',durable_recovery,
        ['<b>Checkpoint first:</b> a tool call’s intent is stored before it runs.','<b>After a restart</b>, a new process resumes open tasks.',
         '<b>Replay rule:</b> only tools marked safe rerun; otherwise the model is told.','<b>requestId</b> makes a submission exactly-once.'],
        'Durability means deciding, per tool, what may happen twice.',DURABLE,icon='database')
    add('Hermes: an always-on agent',F,'Matheus','One agent core, reached through a CLI, chat gateways and editors, and started by a scheduler.',hermes_architecture,
        ['<b>Entry points:</b> CLI, a long-running gateway, ACP clients.','<b>Cron</b> starts work without a person in the loop.',
         '<b>Memory files</b> are always in context; sessions live in SQLite.','<b>Self-improving:</b> the agent writes and patches its own skills.'],
        'An always-on agent is a service, with a service’s responsibilities.',HERMES+' · '+HARNESS+', §7–10',icon='clock')
    add('What always-on costs',F,'Matheus','More autonomy moves risk from the person at the terminal into the architecture.',
        lambda:table_figure(['','Pi','Pi Durable','Hermes'],[
            ['Started by','A person, per session','Your application','People, chats and schedules'],
            ['State','JSONL session tree','Checkpoints in SQLite, JSONL or memory','SQLite sessions + Markdown memory'],
            ['After a crash','You ask it to continue','resume() picks up open tasks','History persists in SQLite'],
            ['Isolation','None by design','Pluggable execution environments','Six pluggable execution backends'],
            ['Watch out for','Safety depends on installed extensions','Experimental API; one process owns the storage','One user lost 69% of a 12-hour session’s tokens to replayed history']],[16,26,29,29]),
        ['<b>Each step right</b> adds state that must stay consistent.','<b>Unattended runs</b> need durable checkpoints and replay rules.',
         '<b>Long-running processes</b> fail in new ways: leaks, replays, fragmentation.','<b>Field reports</b> are evidence too: read the issue tracker.'],
        'Every hour an agent runs unattended is an hour of architecture to own.',PI+' · '+DURABLE+' · Hermes issue #5563',icon='shield-alert')
    add('The platform turn',F,'Matheus','Harnesses are becoming platforms, and frameworks are becoming harnesses.',platform_turn,
        ['<b>Bottom up:</b> model, harness, platform, meta-harness.','<b>Platform:</b> SDKs, durable libraries, ACP servers, skill marketplaces.',
         '<b>Meta-harness:</b> Omnigent ships adapters for 23 harnesses.','<b>Implication:</b> extensions are a supply chain to secure.'],
        'The developer increasingly programs inside the harness.',HARNESS+', §14 · '+DURABLE,icon='boxes')
    add('Recommendations from eleven harnesses',F,'Matheus','The study ends with 18 recommendations; seven connect directly to today’s topics.',
        lambda:table_figure(['#','Recommendation','Topic','Evidence today'],[
            ['R1','Start with a linear loop','Harness','Pi: a ~790-line loop, no planner'],
            ['R6','Auto-discover hierarchical Markdown context','Context','8 of 11 harnesses'],
            ['R7','Compact at a threshold; keep a verbatim tail','Context','Hermes at 50%; Pi at window − 16k'],
            ['R8','Do not build RAG over code','Patterns','0 of 11 use embedding search'],
            ['R12','Stay single-agent until exploration needs parallelism','Patterns','Hermes: one child by default'],
            ['R15','Do not use an agentic framework for the runtime','Harness','0 of 11 import one'],
            ['R18','Ship cheap caps against stuck loops','Evaluation','Hermes: 90-step budget; Pi: none']],[7,44,15,34]),
        ['<b>Recommendations</b> come from what eleven systems converged on.','<b>Evidence column:</b> where today’s systems follow or diverge.',
         '<b>R18 splits the field:</b> budgets versus trusting the model to stop.','<b>Use them as defaults</b>, and know when you diverge.'],
        'Recommendations are evidence, not rules — know when you diverge.',HARNESS+', §16',icon='clipboard-check')
    add('A minimum viable harness in ~90 lines',F,'Matheus','The study closes with a scaffold that implements ten of its recommendations.',code_panel,
        ['<b>The while loop</b> is the whole agent.','<b>Limits and compaction</b> run before every model call.',
         '<b>Return when</b> the model stops calling tools.','<b>Left out on purpose:</b> sandbox, multi-agent, MCP, skills.'],
        'Start minimal; add what your observed failures demand.',HARNESS+', §16.10, Listing 3',icon='file-code')
    add('Discussion',D,'All presenters','Which of today’s five questions can our own project already answer?',None,
        ['Harness · patterns · evaluation · context · always-on'],'','',layout='statement')
    return slides
