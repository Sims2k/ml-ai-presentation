"""Detailed, bounded lecture figures. Coordinates and connections are authored.

Brand typography follows approved A. Semantic colors repeat across all figures.
All complete static frames remain readable without the keyboard enhancement.
"""
from html import escape
from build_lecture_samples import text, node, arrow, svg, group, architecture
from visual_marks import svg_icon

PAPER='#faf9f7'

def edge(slug, path, dashed=False):
    return f'<path d="{path}" class="edge" marker-end="url(#{slug}-arrow)"'+(' stroke-dasharray="6 5"' if dashed else '')+'/>'

def label(x,y,value):
    w=max(64,len(value)*10+20)
    return f'<rect x="{x-w/2}" y="{y-23}" width="{w}" height="30" fill="{PAPER}"/>'+text(x,y,value,'edge-label','middle')

def zone(y,title,h=272):
    return f'<rect x="8" y="{y}" width="1104" height="{h}" rx="6" class="zone"/>'+text(28,y+36,title,'lane-title')

def banner(y,title,lines):
    out=f'<rect x="24" y="{y}" width="1072" height="{64+len(lines)*32}" rx="6" fill="#f1f0eb" stroke="#d4d4cc"/>'
    out+=text(44,y+32,title,'lane-title')
    for i,line in enumerate(lines):out+=text(44,y+70+i*32,line,'aside-sub')
    return out

def sequence(slug,title,items,details,heading='ARCHITECTURE PATH',footer=''):
    """Three responsibilities, with exact operational detail under each one."""
    assert len(items)==3 and len(details)==3
    body=zone(16,heading,584)
    body+=arrow(slug,304,216,420,216)+arrow(slug,700,216,816,216)
    for i,(name,lines,role) in enumerate(items):
        x=24+i*396
        content=node(x,136,280,160,name,lines,role,['INPUT','PROCESS','OUTPUT'][i])
        body+=group(content,i+1,name)
        body+=text(x+12,354,details[i][0],'aside-title')
        for j,line in enumerate(details[i][1:]):body+=text(x+12,394+j*34,line,'aside-sub')
    if footer:body+=text(28,630,footer,'diagram-note')
    return svg(slug,title,title,body),3

def lanes(slug,title,rows,link=None,footer=''):
    """Two labeled lanes, three components each, and an optional vertical handoff."""
    assert len(rows)==2
    body=''
    for r,(heading,items) in enumerate(rows):
        y=16+r*304
        body+=zone(y,heading,280)
        body+=arrow(slug,304,y+160,420,y+160)+arrow(slug,700,y+160,816,y+160)
    if link:
        col,txt=link;x=164+col*396
        body+=arrow(slug,x,256,x,400,True)+label(x+114,328,txt)
    for r,(heading,items) in enumerate(rows):
        y=96+r*304
        for i,(name,lines,role) in enumerate(items):
            body+=group(node(24+i*396,y,280,160,name,lines,role),r*2+i//2+1,name)
    if footer:body+=text(28,630,footer,'diagram-note')
    return svg(slug,title,title,body),4

def fork(slug,title,source,upper,lower,right,toplabel='PATH A',bottomlabel='PATH B',foot=''):
    """One input, two routes, one downstream owner. Five nodes, six paths."""
    body=zone(16,'SEPARATE THE PATHS AND THEIR AUTHORITY',584)
    # Separate ports and elbows, no shared segments or crossings.
    body+=edge(slug,'M304 276 H352 Q360 276 360 268 V184 Q360 176 368 176 H420')
    body+=edge(slug,'M304 316 H344 Q352 316 352 324 V424 Q352 432 360 432 H420')
    body+=edge(slug,'M700 176 H752 Q760 176 760 184 V268 Q760 276 768 276 H816')
    body+=edge(slug,'M700 432 H760 Q768 432 768 424 V324 Q768 316 776 316 H816',True)
    body+=label(560,76,toplabel)+label(560,332,bottomlabel)
    for step,(x,y,item) in enumerate([(24,216,source),(420,96,upper),(420,352,lower),(816,216,right)],1):
        n,ls,role=item;body+=group(node(x,y,280,160,n,ls,role),step,n)
    if foot:body+=text(28,630,foot,'diagram-note')
    return svg(slug,title,title,body),4

def table_figure(slug,title,headers,rows,widths=None):
    # HTML tables are intentional where a diagram adds no semantic value.
    cols='<colgroup>'+''.join(f'<col style="width:{w}%">' for w in widths)+'</colgroup>' if widths else ''
    return '<div class="lecture-table"><table>'+cols+'<thead><tr>'+''.join('<th>'+escape(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+escape(str(c))+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>',0

def distribution(slug='input-drift'):
    body=zone(12,'SAME FEATURE DEFINITION · SAME BIN BOUNDARIES · TWO COMPARABLE COHORTS',560)
    for i,(name,vals) in enumerate([('Reference: earlier customers',[10,20,30,40]),('Current: newer customers',[40,30,20,10])]):
        off=i*552
        layer=text(off+52,108,name,'plot-title')
        layer+=text(off+52,150,'Customers per 100','axis-label')
        layer+=f'<path d="M{off+52} 176 V424 H{off+516}" class="axis"/>'
        for k,v in enumerate(vals):
            x=off+100+k*104;h=v*5
            layer+=f'<rect x="{x}" y="{424-h}" width="60" height="{h}" class="hist {"current" if i else "reference"}"/>'
            layer+=text(x+30,424-h-16,str(v),'plot-title','middle')
            layer+=text(x+30,466,['0','1–2','3–5','6+'][k],'axis-label','middle')
        layer+=text(off+52,514,'App logins in the last seven days','axis-label')
        body+=group(layer,i+1,name)
    body+=text(28,600,'What changed: the input distribution. What this does not establish: predictive accuracy loss.','aside-title')
    body+=text(28,630,'Invented counts: two 100-customer cohorts. No churn labels are needed for this comparison.','diagram-note')
    return svg(slug,'Data drift: the customer mix changes','Two invented cohorts use identical app-activity bins; the current cohort contains more low-activity customers, without establishing any change in churn risk given those inputs.',body),2

def concept(slug='concept-drift'):
    body=zone(12,'HOLD THE INPUT MEANING FIXED · CHANGE ITS RELATIONSHIP TO THE OUTCOME',560)
    for i,name in enumerate(['Reference relationship','Changed relationship']):
        off=i*552;layer=text(off+52,108,name,'plot-title')
        layer+=text(off+52,154,'Illustrative churn risk','axis-label')
        layer+=f'<path d="M{off+52} 184 V440 H{off+516}" class="axis"/>'
        layer+=text(off+60,216,'Higher','axis-label')+text(off+60,422,'Lower','axis-label')
        layer+=f'<path d="M{off+144} 224 C{off+236} 240 {off+304} 388 {off+484} 412" class="risk reference"/>'
        if i:
            layer+=f'<path d="M{off+144} 224 C{off+244} 234 {off+340} 256 {off+484} 280" class="risk current"/>'
            layer+=text(off+254,338,'Same activity, higher risk','annotation')
        layer+=text(off+120,482,'Low activity','axis-label')+text(off+408,482,'High activity','axis-label')
        layer+=text(off+52,528,'Same feature: seven-day app logins','axis-label')
        body+=group(layer,i+1,name)
    body+=text(28,600,'Dashed: earlier relationship. Solid: later relationship. The deployed M1 has not changed.','aside-title')
    body+=text(28,630,'Schematic relationships, not measurements or fitted models. Assess with valid inputs and mature outcomes.','diagram-note')
    return svg(slug,'Concept drift: the same behavior means something different','After a hypothetical pricing change, active customers have higher churn risk than before, while the input definition and deployed model are held fixed.',body),2

def label_timeline():
    s='delayed-labels';body=zone(16,'LINK EVIDENCE TO THE ORIGINAL PREDICTION DATE AND TARGET WINDOW',572)
    body+=arrow(s,100,200,1048,200)
    for x,title,sub in [(100,'D0','Score saved'),(700,'D30','Window closes'),(1040,'Later','Labels ingested')]:
        body+=f'<path d="M{x} 186 V218" class="axis"/>'+text(x,160,title,'plot-title','middle')+text(x,258,sub,'axis-label','middle')
    body+=group(node(24,336,312,168,'Operational checks',['Freshness + missingness','Coverage + completion'],'data','AVAILABLE AT D0'),1,'Inspect operation immediately')
    body+=group(node(420,336,312,168,'Unknown outcomes',['No full 30-day label','Absence ≠ stayed'],'model','WAIT FOR EVIDENCE'),2,'The outcome window must close')
    body+=group(node(816,336,280,168,'Quality review',['Join scores to labels','Evaluate by cohort'],'business','MATURE LABELS'),3,'Evaluate with mature outcome evidence')
    body+=text(28,554,'Save customer, cutoff, target window, features, M1 version, and campaign action context.','aside-title')
    body+=text(28,630,'The 30-day window and dates are teaching choices. Ingestion can delay evaluation further.','diagram-note')
    return svg(s,'Operational evidence now; quality evidence later','A saved prediction precedes a 30-day outcome window and label ingestion; immediate input and execution checks remain distinct from later predictive evaluation.',body),3

def permissions():
    return table_figure('permissions','Least privilege by role',
        ['Identity','Read','Write / decide','Excluded authority'],[
        ('Feature job','Approved source','Prepared features','Promote a model'),
        ('Trainer','Training features','Candidate artifact','Release to production'),
        ('Release reviewer','Candidate + checks','Approve a version set','Rewrite training data'),
        ('Batch scorer','Approved M1 + inputs','Versioned scores','Change campaign policy'),
        ('Campaign user','Approved score view','Eligible contact action','Read unrestricted history')],[24,22,27,27])

def cover_map():
    return table_figure('agenda','Two blocks and topic owners',['Block','Topics','Presenter'],[
        ('1 · Model to system','Foundations and dual lifecycle','Ricardo'),
        ('','Deployment and serving','Tomás'),
        ('','Monitoring and degradation','Simon'),
        ('','Design decisions and technical debt','Luca'),
        ('2 · Architecture & quality','Architectural tactics','Matheus'),
        ('','DevOps / MLOps','Matheus'),
        ('','Security and privacy','Simon + Matheus'),
        ('','Quality checklist and tools','Matheus')],[25,49,26])

def serving_comparison(online=False):
    """Colleague content in the existing three-lane, keyboard-build grammar."""
    slug='online-contrast' if online else 'serving-overview'
    rows=(
        [('01 SYNCHRONOUS · BLOCK A PAYMENT','Authorization waits for the score',
          ('Card payment','Authorization request'),('Fraud API','Scores in milliseconds'),('Authorizer','Approves or blocks'),'REQUEST','RESPONSE'),
         ('02 ASYNCHRONOUS · NOTIFY','Other systems act after the event',
          ('Online app','Publishes transaction'),('Stream processor','Invokes the model'),('Pub/sub output','Alert to the app'),'EVENT','PUSH'),
         ('03 HYBRID · PRECOMPUTE + CACHE','Computed in batch, read with low latency',
          ('Monthly batch','Churn scores'),('Low-latency store','Keyed by customer'),('CRM screen','Shows C042: 0.70'),'WRITE','READ')]
        if online else
        [('01 OFFLINE · BATCH','Precompute many predictions on a schedule',
          ('Monthly job','Customer snapshot'),('Score + save','All active customers'),('Campaign','Reads saved scores'),'SCORE','READ'),
         ('02 REAL-TIME · SYNCHRONOUS','The caller waits for the prediction',
          ('Application','Sends request'),('Prediction API','REST microservice'),('Application','Uses the response'),'REQUEST','RESPONSE'),
         ('03 REAL-TIME · ASYNCHRONOUS','Events and predictions travel through pub/sub',
          ('Online app','Publishes an event'),('Stream processor','Invokes the model'),('Pub/sub output','Notifies the app'),'EVENT','PUSH')])
    body=''
    for step,(heading,sub,a,b,c,left,right) in enumerate(rows,1):
        y=12+(step-1)*204;cy=y+128
        layer=f'<rect x="8" y="{y}" width="1104" height="188" rx="6" class="zone"/>'
        layer+=text(28,y+32,heading,'lane-title')+text(28,y+62,sub,'row-description')
        mark=('network','bell','database')[step-1] if online else ('database','network','send')[step-1]
        layer+=svg_icon(mark,1060,y+16,28)
        layer+=arrow(slug,312,cy,432,cy,step==2 if online else step==3)
        layer+=arrow(slug,712,cy,832,cy,step==2 if online else step==3)
        for x,value in [(372,left),(772,right)]:
            layer+=f'<rect x="{x-54}" y="{cy-48}" width="108" height="28" fill="{PAPER}"/>'
            layer+=text(x,cy-28,value,'edge-label','middle')
        for x,w,(name,subline),role in [(28,284,a,'data'),(432,280,b,'model'),(832,260,c,'business')]:
            layer+=node(x,y+80,w,92,name,[subline],role)
        body+=group(layer,step,heading)
    return svg(slug,'Online serving contrasts' if online else 'Prediction serving patterns',
        'Three timing patterns connect the producer, model execution, and consumer; the monthly churn case remains batch.',body),3

def strategy_dispatch():
    s='strategy-pattern';body=zone(16,'ONE CLIENT CONTRACT · TWO POSSIBLE IMPLEMENTATIONS',584)
    body+=arrow(s,304,296,420,296)
    body+=edge(s,'M700 276 H752 Q760 276 760 268 V184 Q760 176 768 176 H816')
    body+=edge(s,'M700 316 H744 Q752 316 752 324 V424 Q752 432 760 432 H816',True)
    body+=group(node(24,216,280,160,'Scoring client',['Uses an abstraction','No concrete dependency'],'data','CLIENT'),1,'Client calls the stable interface')
    body+=group(node(420,216,280,160,'Stable interface',['Input + output contract','Inject implementation'],'business','CONTRACT'),2,'Stable strategy interface')
    body+=group(node(816,96,280,160,'Strategy A',['Current implementation','Contract is tested'],'model','CURRENT'),3,'Current implementation')
    body+=group(node(816,352,280,160,'Strategy B',['Alternative candidate','Evaluate compatibility'],'model','ALTERNATIVE'),4,'Alternative implementation')
    body+=text(28,554,'Bind the selected implementation; the diagram does not imply both execute for every call.','aside-title')
    body+=text(28,630,'Substitution in code still requires semantic compatibility, predictive evaluation, and release approval.','diagram-note')
    return svg(s,'Strategy: implementation behind a stable interface','A scoring client depends on a stable interface, to which a selected current or alternative implementation can be bound.',body),4

def shadow_paths():
    s='shadow-detail';body=zone(16,'SAME INPUTS · DISTINCT OUTPUT PURPOSES · ONE ACTION PATH',584)
    body+=edge(s,'M304 276 H352 Q360 276 360 268 V184 Q360 176 368 176 H420')
    body+=edge(s,'M304 316 H344 Q352 316 352 324 V424 Q352 432 360 432 H420')
    body+=arrow(s,700,176,816,176)
    body+=arrow(s,700,432,816,432,True)
    body+=edge(s,'M700 216 H740 Q748 216 748 224 V392 Q748 400 756 400 H816',True)
    for step,(x,y,name,ls,role,tag) in enumerate([
        (24,216,'Validated batch',['Same D0 snapshot','C042 in both runs'],'data','INPUT'),
        (420,96,'Approved M1',['C042: 0.70','Action path enabled'],'model','INCUMBENT'),
        (420,352,'Candidate M2',['C042 scored, logged','No action authority'],'model','SHADOW'),
        (816,96,'Campaign policy',['Only approved result','One permitted action'],'business','ACTION'),
        (816,352,'Evidence review',['Compare M1 and M2','Quality after labels'],'data','OBSERVATION')],1):
        body+=group(node(x,y,280,160,name,ls,role,tag),step,name)
    body+=text(28,630,'The candidate has no path to campaign action. Comparison records preserve model and input identities.','diagram-note')
    return svg(s,'Shadow deployment: observe without acting','A validated batch feeds approved M1 and shadow M2; only M1 feeds campaign policy, while both outputs can support evidence review.',body),5

def policy_decision():
    s='prediction-policy';body=zone(16,'RISK ESTIMATION AND CONTACT AUTHORITY ARE SEPARATE',584)
    body+=arrow(s,304,296,420,296)
    body+=edge(s,'M700 276 H752 Q760 276 760 268 V184 Q760 176 768 176 H816')
    body+=edge(s,'M700 316 H744 Q752 316 752 324 V424 Q752 432 760 432 H816')
    body+=label(760,128,'ALLOW')+label(752,492,'BLOCK')
    for step,(x,y,name,ls,role,tag) in enumerate([
        (24,216,'Risk estimate',['Illustrative score: 0.70','Outcome still unknown'],'model','PREDICTION'),
        (420,216,'Campaign policy',['Eligibility + contact limits','Preferences + budget'],'business','DECISION'),
        (816,96,'Permitted contact',['Record offer / action','Link policy version'],'business','ACTION'),
        (816,352,'No contact',['Record the reason','Preserve decision link'],'data','ALTERNATIVE')],1):
        body+=group(node(x,y,280,160,name,ls,role,tag),step,name)
    body+=text(28,630,'A high risk estimate does not bypass the policy. No completed contact or outcome is asserted here.','diagram-note')
    return svg(s,'A prediction reaches a separate policy decision','A churn score feeds campaign policy, which either permits contact or records a no-contact decision under separate business rules.',body),4

def monitoring_architecture():
    s='monitoring-architecture';body=zone(16,'CONNECT OPERATIONAL SIGNALS TO EVIDENCE AND RESPONSIBLE RESPONSE',584)
    body+=edge(s,'M304 160 H352 Q360 160 360 168 V288 Q360 296 368 296 H420')
    body+=arrow(s,304,336,420,336)
    body+=edge(s,'M304 512 H344 Q352 512 352 504 V384 Q352 376 360 376 H420')
    body+=edge(s,'M700 296 H744 Q752 296 752 288 V168 Q752 160 760 160 H816')
    body+=edge(s,'M700 376 H736 Q744 376 744 384 V504 Q744 512 752 512 H816',True)
    body+=arrow(s,956,240,956,432,True)+label(1040,336,'NOTIFY')
    for step,(x,y,name,ls,role,tag) in enumerate([
        (24,80,'Input checks',['Validity + freshness','Reference comparisons'],'data','AT SCORING'),
        (24,256,'System signals',['Errors + duration','Coverage + completion'],'data','AT EXECUTION'),
        (24,432,'Model quality',['Linked mature labels','Cohort error measures'],'model','AFTER LABELS'),
        (420,256,'Evidence store',['Run + feature + version','Logs / metrics / reports'],'data','SHARED CONTEXT'),
        (816,80,'Alert routing',['Defined threshold','Named response owner'],'business','ATTENTION'),
        (816,432,'Review + respond',['Investigate the cause','Select controlled remedy'],'business','AUTHORITY')],1):
        body+=group(node(x,y,280,160,name,ls,role,tag),(step+1)//2,name)
    body+=text(28,630,'Monitoring can request a review. It cannot approve a candidate or silently promote a replacement.','diagram-note')
    return svg(s,'Monitoring architecture: signals, evidence and response','Input, execution and mature-label evidence is linked in shared run context, routed to an owner, and used for investigation rather than automatic model promotion.',body),3
