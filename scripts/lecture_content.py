"""Concept-first English lecture, grounded in the group outline and study notes.

Bank records, scores, release labels, incidents and diagrams are teaching designs.
No real bank result or executed tool run is claimed. Speaker TBDs stay explicit.
"""
from lecture_full_visuals import *
from drift_visuals import temporal_reference, input_distribution, concept_relationship, concept_errors

def item(name,a,b='',role='data'):
    return name,[x for x in (a,b) if x],role

def build_lecture():
    slides=[]
    def add(title,section,owner,lead,visual,bullets,example,takeaway,source,ref=None,extra=''):
        assert len(bullets)==4
        slides.append(dict(title=title,section=section,owner=owner,lead=lead,visual=visual,bullets=bullets,example=example,takeaway=takeaway,source=source,ref=ref,extra=extra))
    F='Block 1 / Foundations';S='Block 1 / Deployment & serving';M='Block 1 / Monitoring & degradation';D='Block 1 / Design decisions'
    A='Block 2 / Architectural tactics';O='Block 2 / DevOps & MLOps';SEC='Block 2 / Security & privacy';Q='Block 2 / Quality concerns';T='Block 2 / Practical tools'
    BASS='Bass, Ch. 14';K='Kalinowski, Ch. 13–14';MON='Simon’s notes, §2–4 · Bass, Ch. 11 / §14.1.5';DES='Kalinowski, Ch. 14 · Nazir, §§5–6';OPS='Bass, §14.1 · Kalinowski, §16.3–16.5 (supporting)'
    SECREF='Simon’s notes, §5–7 · Bass, Ch. 9–10 / §14.2';QUALITY='Bucaioni, published Table 1, pp. 6–7 · Bass, Ch. 14'

    add('ML Architecture',F,'All presenters','From a trained model to a maintainable, observable, governed system.',None,
        ['<b>Software engineering</b> for systems that depend on learned behavior.', '<b>One shared case:</b> bank customer-churn prediction.', '<b>Two blocks:</b> model-to-system foundations, then architecture and quality.', '<b>Five presenters:</b> Ricardo, Tomás, Simon, Luca, and Matheus.'],
        'Bank churn supplies the shared case. Examples, records, schedules, and incidents are illustrative.',
        'A useful model needs an engineered system around it.',BASS+' · '+K,1)
    add('Two blocks, one shared bank case',F,'All presenters','Follow the group’s topic outline; use the case to connect each architectural decision.',cover_map,
        ['<b>Block 1:</b> lifecycle, serving, monitoring, and design decisions.', '<b>Block 2:</b> tactics, MLOps, security, privacy, and quality.', '<b>Concept first:</b> explain the mechanism, then apply it to churn.', '<b>Named handoffs:</b> each section identifies its presenter; unassigned topics remain TBD.'],
        'The same source → feature → model → score → policy path returns throughout the lecture.',
        'Each architectural decision connects predictive behavior to a system responsibility.','Group discussion document · Agreed lecture redesign',6)
    add('The bank case: features, labels, and predictions',F,'Ricardo','A few ML terms connect familiar application data to a learned risk estimate.',
        lambda:sequence('bank-vocabulary','Features, labels and predictions',[
            item('Customer records','CRM + app activity','Known at scoring time'),item('Prepared inputs','Seven-day login count','Consistent time cutoff'),item('Risk estimate','Apply approved M1','Outcome still unknown',role='model')],
            [('DATA','Events and transactions','are source records.'),('FEATURE','A prepared input has','a precise meaning.'),('LABEL','Observed churn comes','after the target window.')],footer='Ana / C042 and all values are illustrative. A feature value does not prove intent.'),
        ['<b>Feature:</b> a prepared input, such as logins during the previous seven days.', '<b>Label:</b> the observed churn outcome used for training and later evaluation.', '<b>Prediction:</b> an estimate produced before the customer’s future outcome is known.', '<b>Training vs. inference:</b> learn from earlier examples; apply the approved model to current inputs.'],
        'Ana / C042: logins fall from 7 to 1; the illustrative score is 0.70. Her next-30-day outcome is unknown.',
        'Lower activity is evidence for a model input, not proof that a customer will leave.',BASS+' · Simon’s notes, §1',2)
    add('From a trained model to an ML system',F,'Ricardo','Architecture connects learning, production data, operational controls, and business decisions.',architecture,
        ['<b>Training</b> uses historical features and labels to build and evaluate candidates.', '<b>Production</b> validates current data and applies an approved, compatible model.', '<b>Stored scores</b> link predictions to customer, time, input evidence, and versions.', '<b>Business policy</b> determines the permitted action; it remains separate from the score.'],
        'The bank computes a monthly batch of churn scores, then applies campaign eligibility and contact rules.',
        'Keep the learning path and production path distinct, but traceable.',BASS+' · Kalinowski, §13.2–13.3',4)
    add('Two lifecycles, one compatible system',F,'Ricardo','Code correctness and predictive usefulness depend on different feedback and release cycles.',
        lambda:lanes('dual-lifecycle','Software and model lifecycles',[
            ('SOFTWARE LIFECYCLE',[item('Change code','Connector or policy'),item('Integrate + test','Behavior + contracts'),item('Deliver release','Compatible runtime',role='business')]),
            ('DATA / MODEL LIFECYCLE',[item('Curate examples','Features + labels'),item('Train + evaluate','Candidate evidence',role='model'),item('Approve candidate','Versioned artifact',role='model')])],footer='Coordinate code, data meaning, model, and configuration; neither path is sufficient alone.'),
        ['<b>Software changes</b> can be checked through code, contract, and integration tests.', '<b>Model development</b> also needs representative data, suitable labels, and evaluation.', '<b>Feedback differs:</b> execution checks may be immediate; churn labels arrive later.', '<b>Co-versioning</b> links changes across code, feature meaning, model, and configuration.'],
        'A CRM connector can change today while M1 stays fixed; its changed inputs can still alter predictions.',
        'A passing software test does not establish future predictive quality.',K+' · Bass, Ch. 11 · Simon’s notes, §1',5)
    add('Prediction and business action are separate',F,'Ricardo','A model estimates risk. Business rules decide whether and how the bank may act.',
        policy_decision,
        ['<b>Score:</b> estimated churn risk, not a guaranteed outcome.', '<b>Policy:</b> preferences, eligibility, contact limits, and campaign budget.', '<b>Action:</b> an offer, another response, or no contact at all.', '<b>Separate evaluation:</b> predictive quality and the benefit of an offer are different questions.'],
        'Ana may have a high risk score and still receive no offer because contact preferences or policy prohibit it.',
        'A policy change should not require retraining the prediction model.',BASS+' · Teaching policy decomposition',3)

    add('Serving patterns: when is a prediction needed?',S,'Tomás','Select the interaction pattern from the decision’s timing and failure behavior.',
        lambda:__import__('build_lecture_samples').serving(),
        ['<b>Batch:</b> compute many predictions; consumers read stored results later.', '<b>Synchronous:</b> the caller waits for a result during its request.', '<b>Asynchronous:</b> an event producer and consumer are decoupled through messaging.', '<b>Edge:</b> a deployment location, independent of prediction timing.'],
        'The churn campaign can use precomputed scores. An immediate fraud check motivates a different timing need.',
        'Timing, location, and release strategy are separate choices.','Kalinowski, §13.3–13.4; supporting Ch. 12',8)
    add('Batch serving: validate, score, publish',S,'Tomás','A complete validated batch must be available before its business deadline.',
        lambda:sequence('batch-detail','Batch scoring with a publication gate',[
            item('Snapshot + check','Fresh source snapshot','Population accounted'),item('Prepare + score','Compatible features','Approved M1','model'),item('Publish batch','Reconcile coverage','Campaign reads scores','business')],
            [('INPUT GATE','Schema, freshness,','completeness, cutoff.'),('EXECUTION','Runtime, dependencies,','feature compatibility.'),('OUTPUT GATE','Version links, valid scores,','publication approval.')],footer='Account for the expected population; a successful final task alone is not a complete batch.'),
        ['<b>Snapshot:</b> define population, cutoff, and required source freshness.', '<b>Validate:</b> reject incompatible inputs before scoring.', '<b>Reconcile:</b> account for written, rejected, and withheld records.', '<b>Publish:</b> expose a validated batch under a defined consumer contract.'],
        'Monthly churn scores are saved for the campaign. A real numerical deadline must be agreed with campaign owners.',
        'Optimize the whole batch deadline, not only per-record prediction speed.',BASS+' · Kalinowski, §13.3',7)
    add('Synchronous serving: the caller waits',S,'Tomás','Prediction becomes part of the application’s response path.',
        lambda:sequence('sync-detail','Synchronous request and prediction',[
            item('Application','Request + identity','Input validation'),item('Prediction API','Fetch / compute inputs','Run compatible model','model'),item('Response','Score or explicit error','Caller handles failure','business')],
            [('REQUEST','Enforce input contract','and access permissions.'),('LATENCY BUDGET','Include feature lookup,','model, and network.'),('FAILURE POLICY','Timeouts and fallbacks','must suit the action.')],footer='This is a pattern comparison, not a new online component in the monthly churn architecture.'),
        ['<b>Response time</b> includes lookup, preparation, inference, and network work.', '<b>Availability</b> now affects the waiting application’s request.', '<b>Failure behavior</b> needs explicit timeout, error, and fallback policies.', '<b>Consistency</b> still requires compatible feature meanings and model versions.'],
        'An immediate fraud check can justify this pattern. The monthly churn campaign does not require it.',
        'A fast model does not guarantee a fast end-to-end service.','Kalinowski, §13.3–13.4 · Teaching comparison',8)
    add('Asynchronous serving: decouple the work',S,'Tomás','Messages separate production, processing, and consumption of a prediction.',
        lambda:sequence('async-detail','Asynchronous event-driven prediction',[
            item('Producer','Publish customer event','Include event identity'),item('Queue + worker','Buffer and process','Compute prediction','model'),item('Consumer','Read result event','Deduplicate action','business')],
            [('MESSAGE CONTRACT','Schema, ordering needs,','event and cutoff IDs.'),('RECOVERY','Retries, lag monitoring,','failed-message handling.'),('IDEMPOTENCY','Repeated delivery must','not duplicate an offer.')],footer='Asynchronous interaction can still have a strict deadline. Delivery guarantees require an explicit design.'),
        ['<b>Buffering</b> absorbs bursts and supports independent processing.', '<b>Lag</b> and queue health become operational concerns.', '<b>Retries</b> require failure handling and idempotent processing.', '<b>Contracts</b> define message identity, timing, schema, and result interpretation.'],
        'If a future campaign consumes prediction events, a repeated message must not cause duplicate customer contacts.',
        'Decoupling adds messaging responsibilities; it does not remove timing requirements.','Kalinowski, §13.3 · Bank application is hypothetical',8)
    add('Deployment location is a separate decision',S,'Tomás','Central, embedded, and edge deployments change operations and constraints.',
        lambda:table_figure('locations','Timing and deployment location',['Location','Typical benefit','Architecture cost'],[
            ('Central service / job','Shared governance and compute','Connectivity and centralized availability'),
            ('Embedded application','Local integration and low call overhead','Coupled application/model releases'),
            ('Edge device','Local response and offline operation','Resource limits, rollout and stale versions')],[26,35,39]),
        ['<b>Central:</b> simplify shared operation and governance.', '<b>Embedded:</b> deploy the model with its host application.', '<b>Edge:</b> account for constrained hardware and intermittent connectivity.', '<b>Choose independently:</b> location does not uniquely determine batch or request timing.'],
        'Keep churn centrally governed. Device-local inference is a contrast, not an extra subsystem to implement here.',
        'Architecture follows the operational context.','Kalinowski, supporting Ch. 12; §13.3–13.4',9)
    add('Package the whole compatible set',S,'Tomás','A deployable release contains more than the learned model file.',
        lambda:sequence('package-detail','A compatible inference package',[
            item('Feature contract','Schema + semantics','Time window + units'),item('Runtime package','M1 + dependencies','Preparation code','model'),item('Execution config','Cutoff + population','Resource settings','business')],
            [('DATA MEANING','Column names alone','are insufficient.'),('REPRODUCIBILITY','Pin and track the','compatible versions.'),('RUNTIME CHECK','Load, score, and write','in the target environment.')],footer='Containerization packages execution; it does not itself establish predictive quality or release approval.'),
        ['<b>Model artifact:</b> the learned parameters and required format.', '<b>Runtime:</b> dependencies, preparation code, and execution environment.', '<b>Contract:</b> feature meaning, types, missingness, and temporal cutoff.', '<b>Configuration:</b> scoring population and execution settings.'],
        'The bank packages M1 with the exact feature interpretation needed to score the monthly customer snapshot.',
        'A package that loads successfully still needs release and quality evidence.',BASS+' · Kalinowski, §13.3–13.4',10)
    add('Shadow deployment: observe without acting',S,'Tomás','A candidate scores real inputs while the approved model remains the action source.',
        shadow_paths,
        ['<b>Run in parallel</b> against comparable production inputs.', '<b>Record identity:</b> distinguish M1 and M2 outputs explicitly.', '<b>Compare</b> operational behavior and score differences first.', '<b>Wait for labels</b> to compare future churn quality.'],
        'Only the M1 record is eligible for campaign use; M2’s shadow score cannot create a second offer.',
        'Shadow checks observation, not the business effect of acting on the candidate.','Group outline · Breck, infrastructure 6–7 · Teaching application',11)
    add('Canary deployment: limit exposure',S,'Tomás','An approved limited cohort uses the candidate before broader rollout.',
        lambda:fork('canary-detail','Canary routes controlled cohorts',item('Assigned cohorts','Stable customer split','No double assignment'),item('Majority on M1','Current production','Baseline evidence','model'),item('Canary on M2','Limited approved group','Observe + recover','model'),item('Campaign policy','One eligible result','Controlled action','business'),toplabel='INCUMBENT COHORT',bottomlabel='CANARY COHORT',foot='The exact cohort size and acceptance gates are design choices; no rollout percentage is prescribed here.'),
        ['<b>Restrict exposure</b> to a defined cohort and scope.', '<b>Observe</b> execution, compatibility, coverage, and policy behavior.', '<b>Define stop rules</b> and a rehearsed recovery path.', '<b>Separate evidence:</b> short operational success cannot prove 30-day predictive quality.'],
        'The bank may authorize a small cohort to use M2 while retaining M1 for the remainder.',
        'A canary controls risk; it is not automatically a valid business experiment.','Breck, infrastructure test 6 · Bank teaching application',11)
    add('A/B testing: define the intervention',S,'Tomás','Assigned groups and a stated outcome make the comparison interpretable.',
        lambda:fork('ab-detail','A/B comparison with a defined outcome',item('Eligible customers','Assignment procedure','Comparable groups'),item('Group A','Defined model / policy','Record action','business'),item('Group B','One stated difference','Record action','business'),item('Outcome analysis','Mature observation','Account for treatment','data'),toplabel='BASELINE',bottomlabel='STATED INTERVENTION',foot='A model comparison and a retention-treatment experiment answer different questions.'),
        ['<b>State what changes:</b> model, decision policy, or retention treatment.', '<b>Assign comparable groups</b> under an appropriate experiment design.', '<b>Define outcomes</b> and the observation window before interpreting results.', '<b>Avoid confounding:</b> changing model and offer together obscures their separate effects.'],
        'Compare two offer policies separately from asking whether M2 ranks churn risk better than M1.',
        'Prediction accuracy and the effect of contacting a customer are different targets.','Group outline · Simon’s notes, §3 · Teaching application',12)

    add('How the world changes over time',M,'Simon','Sudden, gradual, incremental, and recurring changes are different time patterns—not different input features.',temporal_reference,
        ['<b>Sudden:</b> the old regime switches abruptly.', '<b>Gradual:</b> old and new regimes coexist during a transition.', '<b>Incremental / recurring:</b> intermediate change differs from a returning regime.', '<b>Blips:</b> isolated noise is not necessarily a lasting regime change.'],
        'Bank illustrations: a pricing change can be sudden; staggered adoption gradual; evolving habits incremental; seasonal activity recurring.',
        'First ask how change unfolds over time. Then ask what changed: input data, outcome relationships, or data validity.',
        'Krawczyk & Cano (2018), Fig. 2 · Original figure; attribution and source link in guide',extra='Figure requested by the presenter: https://www.researchgate.net/figure/Four-types-of-concept-drift-according-to-severity-and-speed-of-changes-and-noisy-blips_fig2_321627304 . The identical figure was retrieved intact from the publicly posted PyConf 2019 deck at https://pyconf.hydpy.org/PyConf19Slides/talks/The-Past-and-the-dubious-Concept-Drift.pdf , page 6, because direct ResearchGate image download returned HTTP 403. Source publication: B. Krawczyk and A. Cano, Online Ensemble Learning with Abstaining Classifiers for Drifting and Noisy Data Streams, Applied Soft Computing 68, 677–692, 2018. These temporal patterns do not replace the distinction between input drift, concept drift and invalid data. Blips are shown separately from lasting drift.')
    add('Monitoring: observe more than model accuracy',M,'Simon','Inputs, system execution, predictions, and business actions need different evidence.',
        lambda:table_figure('monitor-levels','Four monitoring responsibilities',['Layer','Evidence','Response owner'],[
            ('Inputs','Freshness, missingness, distributions','Source / feature owners'),('System','Completion, latency, errors, coverage','Operations'),('Model','Scores and mature-label quality','ML reviewer'),('Action','Eligibility, contacts, outcomes','Campaign owner')],[23,48,29]),
        ['<b>Inputs:</b> are the right records available and meaningful?', '<b>System:</b> did the pipeline complete correctly and on time?', '<b>Model:</b> are predictions useful on the current population?', '<b>Business:</b> are permitted actions and outcomes being tracked?'],
        'A healthy churn job can still use a shifted population. A useful score can still lead to an inappropriate contact.',
        'Observability connects evidence to investigation; dashboards alone do not decide the remedy.',MON,14)
    add('Monitoring architecture: from signal to response',M,'Simon','Collect linked evidence and route it to an owner who can investigate and act.',monitoring_architecture,
        ['<b>Signals:</b> input, execution, and predictive evidence arrive at different times.', '<b>Context:</b> link observations to run, feature, model, and cohort identity.', '<b>Routing:</b> an alert has a defined recipient and response policy.', '<b>Authority:</b> investigation and release approval remain separate.'],
        'A CRM missingness alert links to B017 and reaches source / operations owners; it does not promote M2.',
        'A useful monitoring design connects evidence, ownership, and a controlled response.',MON+' · Teaching expansion of monitoring responsibilities',18)
    add('Data drift: a different customer mix',M,'Simon','Compare the same input definition across a reference cohort and the current cohort.',input_distribution,
        ['<b>What changes:</b> the distribution of valid model inputs.', '<b>Bank example:</b> a campaign attracts more low-activity customers.', '<b>Available now:</b> compare inputs without waiting for churn labels.', '<b>Limit:</b> a changed distribution alone does not prove lost accuracy.'],
        'Both diagrams count 100 fictional customers using the same seven-day login bins. Only the customer mix changes.',
        'Choose a meaningful reference, comparable cohorts, and a defined response.',MON+' · Invented counts',15)
    add('Concept drift: a different relationship',M,'Simon','The same inputs can have different outcomes while the deployed model keeps its earlier boundary.',concept_relationship,
        ['<b>What changes:</b> churn risk given the same valid input information.', '<b>Bank example:</b> new fees make active customers leave more often.', '<b>Evidence:</b> link predictions to mature, reliable churn outcomes.', '<b>Model status:</b> M1 stays fixed until a separately evaluated release changes it.'],
        'The two panels use the same 15 fictional feature positions. After the hypothetical change, some previously staying customers churn.',
        'A missing field is not concept drift; a statistical alarm is not a retraining approval.',MON+' · Schematic relationships',15)
    add('Concept drift: how M1 starts making errors',M,'Simon','A fixed model can miss churners because the world changed—not because its software stopped running.',concept_errors,
        ['<b>Inputs stay fixed:</b> the two cohorts use identical feature positions.', '<b>M1 stays fixed:</b> its earlier decision boundary is unchanged.', '<b>Outcomes change:</b> a different relationship creates missed churners.', '<b>Evidence:</b> the example uses mature labels, not outcomes already known on scoring day.'],
        'C1 has 5 logins and 5 products; C2 has 11 logins and 1 product. The same inputs now accompany different observed churn outcomes.',
        'Changed labels reveal the mismatch. Investigate causes, evaluate candidates, and use controlled release rather than automatic promotion.',MON+' · Invented mature cohorts and deliberately simplified decision rule',extra='Read the shaded region between the old dashed model boundary and the new solid outcome relationship. Rings mark customers who stayed in the reference scenario but churn in the changed scenario. The two labeled customer examples make the conditional change explicit. This perfect-separation construction is intentionally simple; actual populations can overlap and be noisy. The solid line describes the changed teaching relationship, not a replacement model that has already been trained or released.')
    add('Input checks now; quality checks later',M,'Simon','The target window creates a delay between a prediction and complete outcome evidence.',label_timeline,
        ['<b>At scoring time:</b> check freshness, missingness, execution, and coverage.', '<b>During the window:</b> the full churn outcome is still unknown.', '<b>After ingestion:</b> join labels to the original score and target window.', '<b>Evaluate by cohort:</b> precision, recall, and calibration answer different questions.'],
        'Ana’s D0 score is saved with its context. Complete next-30-day evaluation must wait for that window and ingestion.',
        'An absent label does not mean the customer stayed.',MON+' · Teaching 30-day window',17)
    add('Drift detection: methods and their purpose',M,'Simon','Methods compare inputs; they do not directly measure business value or model correctness.',
        lambda:table_figure('drift-methods','Input comparison methods',['Method','Useful interpretation','Key limitation'],[
            ('PSI','Compare proportions in fixed bins','Depends on binning and reference'),('KS','Compare continuous distributions','Sample size affects sensitivity'),('KL divergence','Directional distribution difference','Needs careful support handling'),('JS divergence','Symmetric distribution comparison','Still does not measure accuracy')],[24,40,36]),
        ['<b>Reference:</b> name the population, period, and feature definition.', '<b>Thresholds:</b> calibrate for the application rather than copying a universal rule.', '<b>Segments:</b> inspect affected cohorts instead of relying only on an aggregate.', '<b>Action:</b> investigate drift alongside quality, change, and business evidence.'],
        'Compare the same seven-day login feature before and after a campaign; investigate why the cohort mix changed.',
        'Interpret the signal alongside data validity, sample size, and downstream quality.',MON+' · Simon’s technical atlas',16)
    add('Data-quality faults and training-serving skew',M,'Simon','Invalid data and inconsistent preparation differ from a shifted valid population.',
        lambda:lanes('fault-skew','Separate invalid inputs from preparation mismatch',[
            ('DATA-QUALITY FAULT',[item('CRM migration','Field becomes missing'),item('Contract check','Missing is invalid'),item('Publication hold','Do not use bad scores',role='business')]),
            ('TRAINING–SERVING SKEW',[item('Training feature','Seven-day cutoff'),item('Production feature','Different join / window'),item('Compatibility test','Detect mismatch',role='model')])],footer='These are different diagnoses. Both can occur even when the model artifact is unchanged.'),
        ['<b>Data-quality fault:</b> missing, stale, corrupt, or incompatible records.', '<b>Skew:</b> training and production prepare the feature differently.', '<b>Inspect:</b> definitions, cutoffs, joins, source changes, and code versions.', '<b>Repair the cause:</b> retraining on defective inputs can preserve the defect.'],
        'A missing engagement field after CRM migration is invalid input. A 30-day production count replacing seven days is skew.',
        'Do not use the word “drift” as a diagnosis for every alarm.',MON,14)
    add('A publication gate contains a bad batch',M,'Simon','The CRM incident illustrates a concrete input fault and a controlled response.',
        lambda:sequence('incident-detail','Contain the fictional CRM incident',[
            item('Source change','CRM migration','Engagement is missing'),item('Validation fails','B017 cannot pass','M1 is unchanged','model'),item('Hold publication','Whole batch withheld','No campaign use','business')],
            [('LOCATE','Match missingness onset','to the source change.'),('PRESERVE','Keep failed run identity','and protected evidence.'),('NOTIFY','Route the evidence to','data and operations owners.')],footer='This is an invented incident. No changed score or customer outcome is claimed.'),
        ['<b>Detect:</b> invalid records violate the agreed input contract.', '<b>Contain:</b> hold the entire B017 batch before publication.', '<b>Investigate:</b> relate cohort, source change, feature definition, and execution.', '<b>Keep M1:</b> a source fault does not itself justify a new learned model.'],
        'Ana’s engagement value is missing, not zero. No new score or completed customer contact is invented.',
        'A gate blocks unsafe use; an alert sends evidence to someone who can investigate.',MON+' · Fictional B017 incident',13)
    add('Respond: investigate, contain, repair, verify',M,'Simon','A monitoring signal opens a decision process; it does not select or approve a remedy.',
        lambda:sequence('incident-response','Controlled incident response',[
            item('Investigate','Scope + source timing','Feature + version links'),item('Contain + repair','Pause unsafe use','Restore valid inputs','model'),item('Verify + release','Re-run full checks','Authorized publication','business')],
            [('EVIDENCE','Which customers, batches,','versions, and changes?'),('REMEDY','Source repair, compatible','rollback, validated fallback.'),('FOLLOW-UP','Observe operation now;','quality after labels mature.')],footer='Candidate training is optional and separately justified; promotion remains a separate release decision.'),
        ['<b>Diagnose</b> before choosing repair, rollback, fallback, or training.', '<b>Preserve evidence</b> and the identity of failed attempts.', '<b>Validate the complete path</b> after the chosen repair.', '<b>Request a model change</b> only when evidence supports one.'],
        'Repair the CRM path, validate a new execution B017-R1, and retain M1 unless a separate model change is justified.',
        'Handoff to Luca: which dependencies made this failure possible?',MON,18)

    add('Hidden dependencies create technical debt',D,'Luca','An innocent upstream change can alter ML behavior without changing the model.',
        lambda:fork('hidden-dependencies','Upstream feature dependencies',item('Shared CRM data','Owner changes schema','Meaning may change'),item('Training consumer','Historical examples','Feature definition','model'),item('Scoring consumer','Current inputs','Same feature meaning','model'),item('Contract review','Owners + versions','Notify consumers','business'),toplabel='HISTORICAL USE',bottomlabel='PRODUCTION USE',foot='A dependency needs an owner and change contract; documenting an arrow is not enough.'),
        ['<b>Hidden coupling:</b> features depend on sources owned by other teams.', '<b>Pipeline complexity:</b> parallel preparation paths can diverge.', '<b>Versioning gaps:</b> a model artifact alone cannot reproduce a decision.', '<b>Context matters:</b> architecture decisions depend on requirements and constraints.'],
        'CRM changes its engagement export for another purpose; both training and production can inherit the change.',
        'Make data dependencies as reviewable as code dependencies.',DES,19)
    add('Make the feature contract explicit',D,'Luca','A contract records meaning and ownership as well as structural schema.',
        lambda:table_figure('feature-contract-detail','engagement_7d contract',['Contract field','Teaching definition'],[
            ('Meaning','Count of app logins in the seven days ending at the scoring cutoff'),('Structure','Non-negative count; declared type and units'),('Missingness','Missing is incompatible with this normal scoring path'),('Ownership','Source and feature owners review semantic changes'),('Compatibility','Train and score with tested, linked definitions')],[29,71]),
        ['<b>Semantics:</b> define what the feature actually measures.', '<b>Time:</b> specify window, cutoff, and joins consistently.', '<b>Validity:</b> define types, ranges, freshness, and missingness.', '<b>Ownership:</b> review upstream changes with affected consumers.'],
        'engagement_7d means app logins during seven days ending at the scoring cutoff; missing must not silently become zero.',
        'Schema checks alone cannot detect every change in meaning.',BASS+' · Nazir, §§5–6 · Teaching contract',19)
    add('Separate responsibilities where change happens',D,'Luca','Clear interfaces let different concerns evolve without unnecessary relearning.',
        lambda:sequence('responsibility-detail','Data, inference and policy boundaries',[
            item('Prepare inputs','Source adapters','Feature semantics'),item('Run inference','Compatible input API','Approved model','model'),item('Apply policy','Eligibility + budget','Record decision','business')],
            [('DATA CHANGE','Repair a connector','without rewriting policy.'),('MODEL CHANGE','Evaluate a replacement','behind a stable contract.'),('RULE CHANGE','Change contact limits','without retraining M1.')],footer='Logical separation can remain inside one application. Microservices need a separate justification.'),
        ['<b>Single responsibility:</b> identify each module’s reason to change.', '<b>Interfaces:</b> specify data and behavior at each boundary.', '<b>Dependency injection:</b> provide implementations through explicit contracts.', '<b>Deployment:</b> logical modules do not automatically require separate services.'],
        'A connector fix changes preparation; a contact-frequency rule changes campaign policy; a new M2 changes inference.',
        'Separate concerns first; choose deployment units from the actual trade-offs.',DES,20)
    add('Pipeline pattern: order the responsibilities',D,'Luca','Make preparation and validation steps explicit and testable.',
        lambda:sequence('pipeline-pattern','Pipeline pattern in bank scoring',[
            item('Validate input','Check contract','Reject incompatible'),item('Prepare feature','Apply cutoff + joins','Transform consistently'),item('Score + persist','M1 inference','Versioned output','model')],
            [('STEP CONTRACT','Known input and output','for each stage.'),('LOCAL TESTS','Check transformation','behavior in isolation.'),('INTEGRATION','Check the connected path','and failed-stage behavior.')],footer='A pipeline structures work; its error and publication policies still require explicit design.'),
        ['<b>Explicit stages</b> clarify transformations and dependencies.', '<b>Stage contracts</b> make intermediate data understandable.', '<b>Tests</b> cover local behavior and end-to-end compatibility.', '<b>Failure handling</b> prevents a partial result from masquerading as a complete batch.'],
        'Validate CRM records before computing engagement_7d and invoking M1.',
        'Use structure to expose the dependency, not to hide it in orchestration code.',DES,21)
    add('Strategy pattern: replace one implementation',D,'Luca','A stable interface separates the client from a specific implementation choice.',
        strategy_dispatch,
        ['<b>Stable interface:</b> the client relies on a contract, not a specific class.', '<b>Alternative implementations</b> can be supplied through that interface.', '<b>Compatibility</b> still includes meaning, not only types.', '<b>Evaluation</b> and release approval still apply when behavior changes.'],
        'Replace a feature-preparation implementation behind a stable interface; verify equivalent semantics before scoring.',
        'Interchangeability in code is not equivalence in predictive behavior.',DES,21)
    add('Observer pattern: notify, then investigate',D,'Luca','A change notification decouples the signal producer from interested responders.',
        lambda:sequence('observer-pattern','Notification is not release authority',[
            item('Monitoring event','Source / quality signal','Named affected cohort'),item('Notification','Route subscribed event','Preserve evidence link'),item('Investigation','Owner selects response','No direct promotion','business')],
            [('SUBJECT','Produces a specific event','with useful context.'),('SUBSCRIBERS','Receive a notification','without tight coupling.'),('AUTHORITY','Investigate and request;','release policy approves.')],footer='Do not wire a generic drift alarm directly to unreviewed model promotion.'),
        ['<b>Subject:</b> emits a meaningful change event.', '<b>Subscribers:</b> receive notifications without tightly coupling the producer.', '<b>Context:</b> include cohort, reference, and evidence links.', '<b>Authority:</b> receiving a notification does not grant release privileges.'],
        'A missingness event notifies data and operations owners; it does not instruct the registry to promote M2.',
        'A useful notification requests attention and preserves the decision boundary.',DES,21)
    add('Version the system, not only the model',D,'Luca','A prediction depends on a compatible set of data meaning, code, model, and configuration.',
        lambda:sequence('coversioning','Link a score to the compatible version set',[
            item('Input evidence','Source + feature version','Preparation revision'),item('Execution context','Model M1 + runtime','Cutoff + configuration','model'),item('Prediction record','Customer + target window','Batch + version links','business')],
            [('MEANING','Identify the exact','feature interpretation.'),('REPLAY','Keep enough protected','context to reconstruct.'),('TRACEABILITY','Link approval and action','to the produced scores.')],footer='Protect sensitive evidence; a traceability link need not expose raw customer history to everyone.'),
        ['<b>Data meaning:</b> record source and feature definitions.', '<b>Code:</b> identify preparation and scoring revisions.', '<b>Model:</b> identify artifact, runtime, and configuration.', '<b>Outputs:</b> connect the compatible set to score and decision records.'],
        'M1 alone cannot explain Ana’s score if a CRM migration changed the meaning of its engagement input.',
        'Co-versioning connects system and model lifecycles.',K+' · Bass, Ch. 11 / §14.1 · Simon’s notes',22)
    add('Modules or services? Make the trade-off',D,'Luca','Independent deployment is useful only when it justifies its operating cost.',
        lambda:table_figure('module-service','Modules versus services',['Concern','Modules in one application','Separate services'],[
            ('Release','Coordinated release','Independent release where justified'),('Failure','Fewer remote dependencies','Network, protocol and partial failures'),('Operation','Simpler local observability','Distributed tracing and recovery'),('Scaling','Scale shared runtime','Scale selected capabilities'),('Choice','Useful simple starting point','Autonomy must justify complexity')],[22,39,39]),
        ['<b>Modules</b> can provide strong logical boundaries with simpler operation.', '<b>Services</b> can support independent change and scaling.', '<b>Distribution</b> adds failure modes and version coordination.', '<b>Evidence</b> and requirements should drive the choice.'],
        'Separate preparation from policy logically; deploy them independently only when the bank’s needs justify it.',
        'There is no universal best ML architecture.',DES,23)

    add('Architectural tactics connect concerns to controls',A,'TBD','Use explicit mechanisms to address uncertainty, change, recovery, and auditability.',
        lambda:table_figure('tactics','Concern, tactic and bank effect',['Concern','Architectural tactic','Bank effect'],[
            ('Data change','Contracts + validation boundary','Detect incompatible CRM inputs'),('Predictive uncertainty','Evaluation + reviewed release','Use evidence for model changes'),('Recovery','Compatible rollback / fallback','Restore the usable path'),('Auditability','Co-versioning + protected lineage','Reconstruct a score and action'),('Privacy / security','Scoped access + minimization','Limit exposure and authority')],[25,38,37]),
        ['<b>Separation</b> isolates data preparation, model execution, and business policy.', '<b>Observation</b> makes operational and predictive behavior reviewable.', '<b>Recovery</b> restores a compatible path rather than only one artifact.', '<b>Governance</b> links evidence, approval, access, and responsibility.'],
        'A validation boundary contains a bad CRM batch; version links and approvals support controlled repair.',
        'A tactic is credible when its mechanism, owner, and evidence are clear.',BASS+' · Bass, Ch. 9–11 · Group Block 2 outline',20)
    add('CI, CD, and CT need different evidence',O,'Matheus','Integration, delivery, deployment, and training automate different responsibilities.',
        lambda:lanes('cicdct','Code and model automation need separate acceptance',[
            ('CODE / SYSTEM PATH',[item('Commit + review','Source / feature code'),item('CI checks','Unit + contract tests'),item('CD release','Compatible package','Configured approval','business')]),
            ('MODEL CANDIDATE PATH',[item('Approved data','Versioned examples'),item('CT process','Train + evaluate','Candidate evidence','model'),item('Registry review','Record + approve','Separate promotion','model')])],footer='Continuous delivery keeps a change releasable; continuous deployment automatically releases gated changes.'),
        ['<b>CI:</b> integrate changes and run code, contract, and path checks.', '<b>Delivery:</b> keep a compatible change ready for an approval decision.', '<b>Deployment:</b> automatically release changes passing the defined policy.', '<b>CT:</b> train and evaluate candidates; completion is not production approval.'],
        'A connector repair can use CI/CD while retaining M1. Retraining is not required for every pipeline change.',
        'Automation executes policy; it does not make acceptance criteria identical.',OPS,25)
    add('Candidate training ends before promotion',O,'Matheus','A registry stores candidate evidence; a separate release decision controls production use.',
        lambda:sequence('candidate-promotion','From candidate evidence to approved model',[
            item('Train candidate','Versioned data + code','Recorded experiment','model'),item('Evaluate + register','Quality + compatibility','Candidate M2 evidence','model'),item('Approve + release','Specific version set','Controlled exposure','business')],
            [('REPRODUCE','Link configuration and','training data context.'),('COMPARE','Baseline, relevant cohorts,','and acceptance criteria.'),('OPERATE','Rollback reference and','post-release checks.')],footer='A drift signal may request review or training. It does not authorize release.'),
        ['<b>Reproducibility:</b> record data, code, configuration, and artifacts.', '<b>Evaluation:</b> compare candidate evidence against the baseline and relevant cohorts.', '<b>Registration:</b> preserve identity and lineage for review.', '<b>Promotion:</b> authorize a specific compatible set with recovery planned.'],
        'M2 remains a candidate until reviewed. M1 remains the approved scoring artifact during the CRM repair.',
        'The registry is part of governance, not the whole approval process.',OPS,26)
    add('Repair the input path; retain M1 when appropriate',O,'Matheus','The CRM incident requires a verified source repair, not an assumed new model.',
        lambda:sequence('repair-execution','A separate repaired execution',[
            item('Review repair','Fix source / adapter','Version the change'),item('Run B017-R1','Validate repaired input','Use compatible M1','model'),item('Verify + publish','Coverage + output checks','Authorized release','business')],
            [('FAILED ATTEMPT','B017 remains recorded','as held / failed.'),('NEW EXECUTION','The repaired run gets','a separate identity.'),('AUDIT HISTORY','Keep failed attempt and','recovery evidence linked.')],footer='Do not overwrite failed evidence. Retain M1 unless separate evidence justifies changing it.'),
        ['<b>Repair</b> the source or preparation defect.', '<b>Version</b> the reviewed fix and compatible configuration.', '<b>Re-run</b> under a new execution identity and validate the complete path.', '<b>Publish</b> only after the configured evidence and approval requirements pass.'],
        'B017 is the held attempt. B017-R1 links the reviewed fix, compatible M1, validation evidence, and publication approval.',
        'A successful fix needs evidence at the consumer boundary, not only a passing connector test.',OPS+' · Simon’s notes, §4',24)
    add('Trace the prediction and the decision',O,'Matheus','Lineage connects input evidence, execution, approval, and downstream action.',
        lambda:sequence('decision-lineage','Reconstruct a score and its use',[
            item('Protected evidence','Feature / source links','M1 + config + cutoff'),item('Prediction ID','Customer + target window','Batch + stored score','model'),item('Decision record','Policy version','Contact / no contact','business')],
            [('RECONSTRUCT','What inputs and model','produced this score?'),('LINK','Which approved run','and output record?'),('EXPLAIN USE','Which rule permitted','or blocked the action?')],footer='Protected references can support audit without exposing all customer history in campaign tools.'),
        ['<b>Prediction identity</b> links customer, time, and target window.', '<b>Execution evidence</b> identifies compatible code, features, model, and config.', '<b>Decision evidence</b> records policy version and action.', '<b>Access controls</b> protect sensitive reconstruction material.'],
        'An investigator can trace Ana’s original score and the campaign’s separate no-contact or contact decision.',
        'A model version alone cannot reconstruct the full decision.',OPS+' · Simon’s notes, §4–6',27)
    add('Recovery restores a compatible path',O,'Matheus','Rehearse restoration before release, and verify it at the consumer boundary.',
        lambda:sequence('recovery-detail','Prepare, execute and verify recovery',[
            item('Before release','Choose rollback target','Rehearse restoration'),item('During incident','Contain affected use','Restore compatible set','model'),item('After recovery','Verify inputs + outputs','Observe the consumer','business')],
            [('PREPARE','Version compatibility','and authority are known.'),('RESTORE','Model-only rollback may','leave bad features intact.'),('EVALUATE','Operation can recover now;','quality needs mature labels.')],footer='Historical customer contacts cannot be undone. Recovery of the system does not erase prior effects.'),
        ['<b>Know the target:</b> identify the last compatible release or validated fallback.', '<b>Rehearse:</b> test the recovery procedure before relying on it.', '<b>Restore the set:</b> include data meaning, runtime, and configuration.', '<b>Verify:</b> inspect stored scores and actual consumer behavior.'],
        'Rolling M1 back cannot repair a CRM field that is still missing; the input path must be restored.',
        'Handoff to security: who may read, change, approve, or operate these paths?','Breck, infrastructure tests 6–7 · Simon’s notes, §4',28)

    add('Security threats depend on attacker access',SEC,'Simon + Matheus','Locate the attacker’s control before naming the ML attack mechanism.',
        lambda:table_figure('attack-mechanisms','Attacks at different stages',['Access surface','Mechanism','What changes'],[
            ('Training records / learning inputs','Poisoning','The learned behavior'),('Production prediction inputs','Inference-time manipulation','The input to a fixed model'),('Outputs or model access','Privacy inference','Attacker knowledge of sensitive data')],[34,33,33]),
        ['<b>Poisoning:</b> altered learning inputs influence the trained model.', '<b>Inference manipulation:</b> altered production inputs affect an existing model’s output.', '<b>Privacy inference:</b> access can reveal sensitive membership or attributes.', '<b>Assumptions matter:</b> access, knowledge, and goals differ by threat.'],
        'A compromised CRM writer could affect current inputs; those records create a poisoning path only if later used for training.',
        'The accidental CRM migration remains a different scenario.',SECREF+' · NIST AI 100-2e2025',29)
    add('Enforce access at the resource boundary',SEC,'Simon + Matheus','Authentication, authorization, validation, and audit solve different parts of the problem.',
        lambda:sequence('access-enforcement','Controlled access to a protected ML resource',[
            item('Authenticated caller','Identity + credentials','Requested operation'),item('Enforcement point','Check policy + scope','Validate request','business'),item('Protected resource','Permit or deny access','Record audit evidence','data')],
            [('IDENTITY','Who is requesting','which operation?'),('AUTHORITY','May this identity act','on this resource now?'),('EVIDENCE','Record allowed and denied','operations for review.')],footer='Logical enforcement functions need not be separate microservices. Network reachability is not authorization.'),
        ['<b>Authenticate:</b> establish caller identity.', '<b>Authorize:</b> check operation, resource, and scope.', '<b>Validate:</b> enforce the input contract independently.', '<b>Audit:</b> preserve useful access and change evidence.'],
        'The scorer may read the approved M1 artifact; it must not gain permission to promote M2 merely by reaching the registry.',
        'A trust boundary needs an enforced policy, not only a box on a diagram.',SECREF+' · NIST SP 800-207, §3',31)
    add('Least privilege follows responsibilities',SEC,'Simon + Matheus','Separate source writes, candidate creation, release approval, and campaign use.',permissions,
        ['<b>Scope identities</b> to the operations and resources they need.', '<b>Separate duties:</b> training does not imply release authority.', '<b>Protect credentials</b> and avoid secrets in code or broad logs.', '<b>Review changes:</b> connect access, source updates, and approvals.'],
        'A campaign user reads an approved score view, not unrestricted training data or production deployment credentials.',
        'This abbreviated teaching matrix is a starting point, not a complete bank permission design.',SECREF+' · Proposed permissions',30)
    add('Privacy: expose what each role needs',SEC,'Simon + Matheus','Campaign use and incident investigation require different views of customer information.',
        lambda:lanes('privacy-views','Purpose-limited access to customer evidence',[
            ('CAMPAIGN VIEW',[item('Approved output','Customer token + score'),item('Policy checks','Preferences + eligibility','Contact limits','business'),item('Action record','Minimum useful context','Restricted retention','business')]),
            ('INVESTIGATION VIEW',[item('Authorized request','Scoped purpose + access'),item('Protected evidence','Relevant feature history','Version and run links'),item('Review record','Audit access and use','Limited retention','business')])],footer='A token alone does not make real customer information anonymous.'),
        ['<b>Minimize collection</b> and the information exposed in outputs.', '<b>Separate views:</b> campaigns and investigators have different purposes.', '<b>Protect logs</b> and define retention and access rules.', '<b>Preserve accountability</b> without making raw evidence broadly available.'],
        'Campaign staff may need Ana’s approved score and eligibility context; investigators may need restricted versioned evidence.',
        'Privacy is an access-and-data-use design, not a label attached to a technique.',SECREF,32)
    add('Privacy techniques have specific limits',SEC,'Simon + Matheus','Choose a mechanism for a defined objective rather than claiming privacy by technique name.',
        lambda:table_figure('privacy-techniques','Techniques and their limits',['Technique','Useful role','Limit to explain'],[
            ('Tokenization','Separate identifiers through a protected mapping','Does not establish anonymity'),('Synthetic data','Reduce direct use of original records','Can retain or leak sensitive patterns'),('Federated learning','Train without centralizing raw records','Updates and outputs can still leak'),('Differential privacy','Bound information about protected contributions','Needs unit, bounds and cumulative-loss accounting')],[27,36,37]),
        ['<b>Specify the objective:</b> what information should be protected from whom?', '<b>Tokens</b> and synthetic data do not automatically establish anonymity.', '<b>Federation</b> changes data location, not every leakage risk.', '<b>DP</b> needs a defined protected unit and accounting across releases; no derivation here.'],
        'Protecting one transaction differs from protecting all contributions of a bank customer.',
        'Do not announce a guarantee without its assumptions and evidence.',SECREF+' · NIST SP 800-226',32)

    add('Use the quality checklist as a review tool',Q,'TBD','Connect concerns to architectural controls, ownership, and observable evidence.',
        lambda:table_figure('quality-checklist','Selected quality concern checks',['Selected concern','Architecture review','Evidence example'],[
            ('SMN3 · Input monitoring','Compare appropriate input distributions','Cohort report + investigated change'),('SA1 · Recovery','Restore a compatible path','Recovery rehearsal + verified outputs'),('SS5 · Cyberattack defense','Enforce authorized operations','Rejected prohibited access / change'),('SS6 · Safety / fairness','Define harm and fairness targets','Group-specific review evidence'),('SP1 · Privacy consideration','Assess data use and privacy mechanisms','Access / retention / technique review')],[32,35,33]),
        ['<b>System and process concerns</b> both matter in ML-intensive systems.', '<b>Select relevant checks</b> rather than treating a short list as the entire checklist.', '<b>Map each concern</b> to a control, owner, and evidence.', '<b>Keep limits visible:</b> the separate corrigendum remains unread.'],
        'Completeness validation addresses input quality; it is not by itself evidence of SS5 cyberattack defense.',
        'A checklist supports structured review; it is not a certification claim.',QUALITY+' · Corrigendum contents not reviewed',33)
    add('Predictive quality and system performance',Q,'TBD','Choose an acceptable model and system from several quality objectives.',
        lambda:table_figure('quality-tradeoffs','Evaluate distinct objectives',['Objective','Evidence','Architecture consequence'],[
            ('Predictive quality','Mature-label precision / recall / calibration','Candidate and cohort evaluation'),('Timeliness','Complete scores before campaign deadline','Batch capacity and dependencies'),('Cost','Training, inference and operations effort','Model complexity and infrastructure'),('Maintainability','Reproducibility, tests, recovery work','Versioned modular design')],[28,39,33]),
        ['<b>Accuracy</b> alone is an incomplete objective, especially with imbalanced outcomes.', '<b>Performance</b> includes the end-to-end deadline and resource use.', '<b>Complexity</b> must justify training and operating costs.', '<b>Acceptance</b> depends on the task and the consequences of errors.'],
        'A heavier churn model is useful only if its quality benefit justifies cost and still meets the campaign’s deadline.',
        'Define acceptance criteria before selecting a more complex model.',QUALITY+' · Kalinowski, §13.4',34)
    add('Robustness: invalid, unfamiliar, or ordinary?',Q,'TBD','Different inputs need different responses; do not treat every unusual value as the same failure.',
        lambda:table_figure('robustness','Input categories and response choices',['Input condition','Evidence to inspect','Possible response'],[
            ('Invalid / incompatible','Contract, freshness, missingness','Reject / hold and investigate'),('Valid but unfamiliar','Population shift, coverage, OOD evidence','Review applicability; validated fallback'),('Valid and familiar','Normal input and execution checks','Score and monitor normally')],[31,39,30]),
        ['<b>Contract validity</b> and model applicability are distinct.', '<b>OOD inputs</b> may be structurally valid but poorly represented in training.', '<b>Confidence</b> alone is not a guaranteed detector of unfamiliar inputs.', '<b>Fallbacks</b> must be validated for the intended situation.'],
        'A missing activity value is invalid; a new customer population may be valid but outside the model’s reliable coverage.',
        'An architecture needs an explicit response when the model should not be trusted.',QUALITY+' · Simon’s notes, §2–4',34)
    add('Explainability and auditability differ',Q,'TBD','Explaining feature influence and reconstructing a historical decision are complementary tasks.',
        lambda:sequence('explanation-audit','From explanation to accountable reconstruction',[
            item('Model explanation','Feature contributions','SHAP / LIME context','model'),item('Protected lineage','Inputs + versions','Prediction record'),item('Decision review','Policy + action','Authorized evidence','business')],
            [('INTERPRET','Why did this model','produce this output?'),('RECONSTRUCT','Which exact context','produced this score?'),('ASSESS','Was the action permitted','and appropriately reviewed?')],footer='Feature attribution does not establish causality, fairness, or a customer’s intention.'),
        ['<b>Explanation</b> helps interpret model behavior in context.', '<b>Auditability</b> needs historical evidence and traceable versions.', '<b>Decision review</b> includes business policy and action, not only the model.', '<b>Limits:</b> SHAP and LIME do not prove causality or fairness.'],
        'An engagement contribution may help explain Ana’s score; it cannot prove why she would leave the bank.',
        'Protect evidence and test whether authorized reviewers can actually retrieve it.',BASS+' · Simon’s notes, §6–7',35)
    add('Fairness: prediction versus treatment',Q,'TBD','Name what is being compared before selecting a metric or declaring an improvement.',
        lambda:lanes('fairness-targets','Different fairness targets',[
            ('PREDICTION FAIRNESS',[item('Mature outcomes','Relevant customer groups'),item('Error comparison','False positives / negatives','Calibration where relevant','model'),item('Model review','Check trade-offs','Document limitations','business')]),
            ('TREATMENT FAIRNESS',[item('Eligible population','Preferences + policy'),item('Offer allocation','Who is contacted?','Who receives support?','business'),item('Outcome review','Observe treatment effects','Interpret with care','business')])],footer='Different fairness measures can conflict; define the objective and relevant groups in context.'),
        ['<b>Prediction fairness:</b> compare errors or calibration across relevant groups.', '<b>Treatment fairness:</b> inspect access to offers and policy effects.', '<b>Context:</b> select targets based on harms and requirements.', '<b>Trade-offs:</b> one metric does not settle every fairness concern.'],
        'Equal churn prediction errors do not imply equal access to retention offers under campaign allocation rules.',
        'Keep predictive quality and the consequences of intervention distinct.',QUALITY+' · Bass, Ch. 10 / §14.2',35)

    add('Airflow: make workflow dependencies visible',T,'TBD','Orchestration supports task order, failure handling, and execution evidence.',
        lambda:sequence('airflow-record','Illustrative orchestration dependency',[
            item('Validate input','B017: failed check','Prepared teaching record'),item('Score M1','Not run','Blocked by dependency','model'),item('Campaign export','Not run','Publication withheld','business')],
            [('TASK EVIDENCE','Status, timing, run ID,','and failure context.'),('WHO ACTS','Operations and source','owners investigate.'),('LIMIT','A green workflow is not','proof of churn accuracy.')],footer='Prepared teaching record, not a screenshot or a captured Airflow run. States are deliberately simplified.'),
        ['<b>Architecture role:</b> order dependent pipeline work.', '<b>Evidence:</b> task state, timing, and run context.', '<b>Action:</b> operators and source owners inspect failed dependencies.', '<b>Limit:</b> orchestration does not supply predictive or release approval evidence by itself.'],
        'The required CRM validation must sit upstream of scoring and export so its failure blocks dependent work.',
        'Connect each tool to a responsibility, evidence, and a response owner.',BASS+' · Illustrative Airflow role',36)
    add('MLflow: connect experiments and artifacts',T,'TBD','Model tracking supports reproducibility and review when evidence links are designed explicitly.',
        lambda:sequence('mlflow-record','Illustrative experiment and model evidence',[
            item('Training run','Code + data context','Parameters + metrics','model'),item('Model artifact','M1 / candidate M2','Artifact and lineage','model'),item('Release context','Compatible version set','Review + approval','business')],
            [('EXPERIMENT','What was trained,','with which configuration?'),('REGISTRY','Which artifact is being','evaluated or released?'),('GOVERNANCE','Connect external checks','and release authority.')],footer='Illustrative records only. No experiment, registry transition, or production release was executed here.'),
        ['<b>Architecture role:</b> connect training evidence and model artifacts.', '<b>Evidence:</b> runs, configuration, metrics, and artifact identity.', '<b>Action:</b> reviewers compare candidates and verify compatible releases.', '<b>Limit:</b> no single tracking tool provides every governance control.'],
        'Link the approved M1 to its evidence while recording B017-R1’s separate input and execution context.',
        'Tool records support the release decision; they do not replace its policy.',BASS+' · Illustrative MLflow role',37)
    add('Validation and drift reports support diagnosis',T,'TBD','A report is useful when its reference, feature meaning, cohort, and response are clear.',
        lambda:sequence('report-record','A useful validation and monitoring report',[
            item('Input context','Feature definition','Reference + current set'),item('Report evidence','Completeness + drift','Cohort + run identity'),item('Owner response','Investigate cause','Record disposition','business')],
            [('VALIDATION','Does the input meet','the declared contract?'),('MONITORING','Did valid input behavior','change relative to reference?'),('DECISION','Repair, review applicability,','or request further evidence.')],footer='Reports here are teaching illustrations, not executed tool output.'),
        ['<b>Validation:</b> test declared expectations before use.', '<b>Drift comparison:</b> inspect change against a named reference.', '<b>Tool choice:</b> reports can support these roles; keep policy outside the screenshot.', '<b>Action:</b> preserve evidence and assign a response owner.'],
        'A missing CRM feature needs a contract-failure response; a changed valid population needs a different investigation.',
        'Tools make evidence easier to collect; architecture defines what that evidence means.',MON+' · Group tool-showcase topic',37)
    add('ML architecture connects five responsibilities',T,'All presenters','Return to the full system and the choices that make a prediction usable.',architecture,
        ['<b>Data:</b> preserve meaning, validity, and temporal consistency.', '<b>Models:</b> evaluate uncertainty and manage compatible approved artifacts.', '<b>Operations:</b> observe, diagnose, release, and recover.', '<b>Decisions:</b> protect access and govern appropriate business action.'],
        'Ana’s score becomes usable through validated inputs, traceable execution, an approved release, and a separate campaign policy.',
        'Day 2: foundation models and agents retain these control needs, while components and failure modes change.',BASS+' · Group synthesis',38)
    add('Sources and adaptation boundaries',T,'All presenters','The bibliography supplies concepts; the bank diagrams and incidents are explicit teaching applications.',
        lambda:table_figure('sources','Source roles in the lecture',['Source','Role'],[
            ('Kalinowski, Ch. 13–14','Architecture, serving, design principles and patterns'),('Bass, Engineering AI Systems','Bank churn; security, privacy and observability'),('Nazir et al., JSS 2024','Challenges, practices and contextual design decisions'),('Bucaioni et al., JSS 2026','Quality checklist; published Table 1 spot-check'),('Breck / NIST supplements','Testing, release / recovery, threat and privacy framing')],[42,58]),
        ['<b>Core readings:</b> architectural decisions, serving, maintenance, and quality concerns.', '<b>Supporting readings</b> extend monitoring, governance, and security.', '<b>Illustrations:</b> Ana, scores, dates, batches, and incidents are invented.', '<b>Source limit:</b> the separately catalogued checklist corrigendum remains unread.'],
        'No new churn outcome, repaired score, retention benefit, or real bank tool execution is claimed.',
        'The separate guide records reading anchors and adaptation limits.','See source-review.md and presenter guide')
    for slide in slides:
        if slide['visual'] in (temporal_reference,input_distribution,concept_relationship,concept_errors):
            slide['layout']='wide'
    from content_overrides import apply_overrides
    return apply_overrides(slides)
