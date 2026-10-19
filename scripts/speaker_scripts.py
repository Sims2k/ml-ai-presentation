"""Hand-written spoken-example scripts for the speaker-notes booklet, keyed by slide title.

These are real lecture prose, not generated from the deck's structured fields --
written to read naturally aloud, stay in easy language, and keep returning to
the running Ana / bank-churn example for continuity. Edit this file directly
when slide content changes; there is no mechanical regeneration from here.
"""

SCRIPTS = {
"ML Architecture": "Today we're looking at what it takes to turn a trained model into a system you can actually trust and run in production. We'll use one running example throughout: a bank trying to predict which customers might leave, or “churn.” You'll see that building the model is really just the first step — the real engineering work is everything that happens around it: serving predictions reliably, watching for problems, and keeping the whole system accountable. Five of us will walk through this together, in two parts: first the foundations, then architecture and quality.",

"Two blocks, one shared bank case": "We've split today's talk into two blocks. The first covers the lifecycle of a model — how it's served, monitored, and designed. The second moves into tactics, operations, security, and quality. Rather than jumping between abstract ideas, we'll always ground each concept in the same story: a bank scoring customers for churn risk. So whenever we introduce a new idea, ask yourself: what does this actually mean for that one bank and that one model?",

"The bank case: features, labels, and predictions": "Let's meet the example that will follow us through the whole talk. Ana is a fictional customer, customer number C042. Over the last week, her app logins dropped from seven down to just one — that's a feature, a piece of prepared input data. Based on that and other signals, our model estimates her churn risk at 0.70. That's a prediction — a guess made before we know what actually happens. Only later, once we observe whether she actually leaves, do we get the label. It's really important to say clearly: a lower login count is evidence, not proof. Ana hasn't left the bank — not yet, maybe not ever.",

"From a trained model to an ML system": "So how does a model like the one that scored Ana actually become part of a real system? There's a training side, where we learn from historical data, and a production side, where we apply an already-approved model to current customers. Every score we produce gets stored together with who it was for, when it happened, and which model version made it. And crucially, the business policy — who actually gets contacted — sits completely separate from that score. At our bank, that means the churn score is computed once a month, in a batch, and only afterward does the campaign team apply its own eligibility rules.",

"Two lifecycles, one compatible system": "Here's something that trips a lot of teams up: code and models don't change on the same clock. You can test a code change quickly — does it compile, does it pass its tests. But testing whether a model is still predictively useful takes much longer, because you need real labels, and those arrive late. Imagine our bank's CRM connector changes today. The code deploys fine, the tests pass — but the current approved model, which we call M1, hasn't changed at all. Yet its inputs have, and that alone can shift what it predicts. So a green test suite is not a guarantee that your predictions are still good.",

"Prediction and business action are separate": "A model's score is just an estimate — never a guaranteed outcome. What happens next is governed by business policy: contact preferences, who's eligible, how many times someone can be contacted, and the campaign's budget. So picture Ana again. Even with a high churn-risk score, she might receive no offer at all, simply because policy says no. That separation matters a lot in practice — it means if the bank wants to change its contact rules tomorrow, nobody needs to retrain the model to do it.",

"Serving patterns: when is a prediction needed?": "Now Tomás is going to walk us through how predictions actually get delivered. The first question to ask is timing: does someone need this answer right now, or can it wait? For our churn case, a batch works fine — scores get computed overnight and read later by the campaign. But imagine a fraud check instead: that needs an answer synchronously, while the customer is still mid-transaction. And there's a third option, asynchronous, where producer and consumer are decoupled through messaging. Notice that where the model physically runs — centrally or at the edge — is a completely separate decision from any of this.",

"Batch serving: validate, score, publish": "Batch serving means computing lots of predictions at once, ahead of when they're needed. For the bank, that means defining a clear snapshot: which customers, as of when, using which sources. Before scoring anyone, we validate the inputs and reject anything that doesn't meet the contract. We reconcile what got written, what got rejected, and what had to be withheld. Only then do we publish — expose a complete, validated batch under a contract the campaign team can rely on. The real goal isn't making any single prediction fast; it's hitting the deadline for the whole batch.",

"Synchronous serving: the caller waits": "Synchronous serving puts the model directly on the critical path of a user's request — they're waiting right now for an answer. That means your response time now has to include looking things up, preparing features, running inference, and the network round-trip. And since the caller is blocked, you need explicit policies for what happens on a timeout or an error. A real-time fraud check is a good candidate for this pattern. Our monthly churn campaign is not — there's no customer sitting there waiting for that score.",

"Asynchronous serving: decouple the work": "Asynchronous serving uses messages to separate who produces a prediction from who eventually consumes it. That buffering is useful — it smooths out bursts of work. But it brings its own concerns: how far behind is the queue, and what happens if a message gets retried? If our bank ever built a campaign that reacted to prediction events in real time, a retried message must never cause the same customer to be contacted twice. Decoupling doesn't remove your timing obligations — it just moves them into a messaging contract.",

"Deployment location is a separate decision": "Where a model physically runs is its own decision, independent of everything else we've covered. Centrally hosted models are easier to govern as one shared system. Embedded models ship inside their host application. And edge deployments have to deal with limited hardware and patchy connectivity. For our churn model, we keep everything centrally governed — there's no reason to push it onto a customer's device. The point is: location, timing, and release strategy are three separate knobs, not one.",

"Package the whole compatible set": "When you deploy a model, the model file itself is really the smallest part of what you're shipping. You also need the runtime it depends on, the code that prepares its features, and a contract describing exactly what each feature means, including how missing values are handled. For the bank, that means M1 is packaged together with the precise definition of its features — not just the model weights. Even when a package installs and loads without errors, that still tells you nothing about whether it's actually ready for release.",

"Shadow deployment: observe without acting": "Shadow deployment lets a new candidate model quietly score the same real inputs as the approved model, without ever influencing a real decision. We run both in parallel, and we're careful to record which output came from which model — M1 or the candidate, M2. At this stage we're only comparing operational behavior and how the scores differ; we still need to wait for actual outcomes to judge predictive quality. At our bank, only M1's record is ever eligible to trigger a campaign offer — M2 running in the shadows can never create a second, invisible offer.",

"Canary deployment: limit exposure": "A canary release lets a small, defined group of customers actually experience the new model, while everyone else stays on the one we trust. We watch execution, compatibility, and how it behaves under real policy — and critically, we define ahead of time what would make us stop, and how we'd roll back. Say the bank authorizes M2 for just a small cohort while keeping M1 everywhere else. One thing to be careful about: a canary running smoothly for a few days tells you the system didn't break. It does not, by itself, prove the new model is better over a full 30-day churn window.",

"A/B testing: define the intervention": "A proper A/B test starts by naming exactly what's changing — is it the model, the decision policy, or the retention offer itself? Then you assign genuinely comparable groups, and you decide upfront what outcome you're measuring and over what window. The trap to avoid is confounding: if you change both the model and the offer at the same time, you'll never know which one caused the result. So we'd test two offer policies in one experiment, and separately test whether M2 actually ranks churn risk better than M1 — never both questions in the same test.",

"How the world changes over time": "Before we talk about what can go wrong with a model over time, it helps to separate out how change happens, in time, from what actually changed. A sudden change flips overnight — think of a bank changing its fees overnight. A gradual change has the old and new situations overlapping for a while, like customers slowly adopting a new app. An incremental change drifts through in-between states, the way average balances creep up over months. A recurring change comes back on a schedule, like holiday shopping every December. And a blip is just one unusual day, like Christmas Eve — noise, not a lasting shift. Keep these patterns separate in your head from the next question, which is what actually changed: the data coming in, the relationship to the outcome, or just plain broken data.",

"Monitoring: observe more than model accuracy": "It's tempting to think monitoring a model just means watching its accuracy. It's really watching four different things. Are the inputs actually there and meaningful? Did the pipeline that produces them run correctly and on time? Are the predictions still useful for today's customers? And are the actions the business takes with those predictions actually being tracked? Here's the trap: a churn job can run perfectly, every record present and on time, and still be scoring a population that's shifted. And a perfectly good score can still lead to a contact that shouldn't have happened. A dashboard full of green checkmarks doesn't decide what to do next — it just tells you where to look.",

"Monitoring architecture: from signal to response": "Good monitoring isn't just collecting numbers — it's getting the right evidence to the right person. Different signals — about inputs, about execution, about predictions — show up on different timelines, so we need to link them back to a specific run, feature version, model, and customer cohort. And every alert needs somewhere to go: a defined recipient and a defined response. Picture a missing-data alert from the CRM migration — it links to the failed batch we'll call B017, and it goes to the data and operations owners. It does not, on its own, promote a new model. Investigating a problem and approving a release are always kept as separate authorities.",

"Data drift: a different customer mix": "Data drift means the mix of customers coming in has changed, even though the feature definition stayed exactly the same. Say a marketing campaign suddenly attracts a lot more low-activity customers than usual — that's a shift we can actually see right away, just by comparing input distributions, without waiting weeks for churn labels to come in. In our illustration, both cohorts are 100 fictional customers using identical seven-day login bins — only the mix across those bins has moved. But here's the limit to keep in mind: seeing that shift alone doesn't prove the model's gotten any less accurate. It's a prompt to look closer, not a verdict.",

"Concept drift: a different relationship": "Concept drift is a different animal: the inputs look exactly the same, but the relationship between those inputs and the outcome has shifted. Say the bank introduces a new fee, and now active customers start leaving at a higher rate than before — same engagement pattern, different result. We can only really see this once we have mature, trustworthy churn outcomes to compare against — not right away. And through all of this, M1 itself hasn't changed; it keeps using its old decision boundary until a properly evaluated new release replaces it. One thing concept drift is not: a single missing field, and it's definitely not an automatic green light to retrain.",

"Concept drift: how M1 starts making errors": "Let's make concept drift concrete. Picture two customers with exactly the same inputs as before — say, five logins and five products used — but now, where they used to stay, they churn. The inputs haven't moved. M1 hasn't moved either; it's still using the boundary it learned originally. What's moved is the real-world relationship between those inputs and what customers actually do. That mismatch is exactly where a fixed model starts quietly making mistakes — not because anything crashed, but because the world underneath it kept moving. Once we see this kind of evidence in mature labels, the next step is to investigate the cause, properly evaluate a candidate fix, and release it through a controlled process — never promote something automatically.",

"Input checks now; quality checks later": "There's an unavoidable delay baked into how we evaluate churn predictions: we define a target window, so by definition the full outcome isn't known yet when we score someone. At scoring time, all we can check is whether the inputs were fresh, complete, and the pipeline ran correctly. Only once that window closes and the real labels arrive can we join them back to the original score and properly evaluate precision, recall, and calibration by cohort. Think of Ana's score on day zero: it's saved with its full context, but we genuinely cannot evaluate it properly until 30 days later. And a missing label at that point does not mean she stayed — it might just mean the data hasn't arrived yet.",

"Drift detection: methods and their purpose": "Drift-detection methods are good at one narrow thing: comparing input distributions. They don't, on their own, tell you anything about business value or whether the model itself is still correct. To use them well, you need to name your reference population and time period clearly, calibrate your thresholds for your own situation rather than copying someone else's rule of thumb, and look at specific affected segments rather than trusting a single aggregate number. If we compare the same seven-day login feature before and after a marketing campaign and see a shift, the right next move is to go find out why the customer mix actually changed — the statistic alone won't tell you.",

"Data-quality faults and training-serving skew": "It's worth drawing a sharp line between two things that often get lumped together. A data-quality fault is something simply broken — missing, stale, or corrupted records. Training-serving skew is subtler: training and production are preparing the exact same feature in two different ways. A missing engagement value after a CRM migration is a quality fault, plain and simple. Using a 30-day activity count in production when training used seven days — that's skew. In both cases, the fix is to repair the actual cause. If you retrain on data that's still broken, you just teach the model to be wrong in a new, more confident way. Don't let ‘drift’ become the catch-all word you reach for every time an alarm fires.",

"A publication gate contains a bad batch": "Let's walk through our fictional teaching incident. After the CRM migration, some records come in with engagement missing — not zero, genuinely missing — and that violates our agreed input contract. The detection is automatic. What happens next is containment: we hold the entire batch, which we'll call B017, before it ever reaches the campaign. Then we investigate — how does this cohort, this source change, and this feature definition actually connect? And importantly, we keep M1 exactly as it is. A broken input source, on its own, is never a reason to reach for a new model. The gate's job is to block unsafe use; the alert's job is to get the evidence to someone who can actually dig in.",

"Respond: investigate, contain, repair, verify": "A monitoring signal is the start of a decision process — it never makes the decision for you. The first step is always to diagnose before reaching for a fix, whether that's a repair, a rollback, a fallback, or retraining. Along the way, we preserve the evidence of exactly what failed and how. Once we've chosen a repair, we validate the whole path end to end, not just the piece we touched. And a model change only gets requested when the evidence actually supports one. In our incident, that means: repair the CRM path, validate a brand-new execution we'll call B017-R1, and keep M1 unless there's a separate, justified reason to change it. From here, Luca's going to pick up the question of what let this failure happen in the first place.",

"Hidden dependencies create technical debt": "Here's an uncomfortable truth: a completely innocent change upstream can quietly change how your model behaves, without anyone touching the model at all. Features often depend on data sources owned by other teams entirely. Parallel preparation paths — one for training, one for production — can drift apart from each other over time. And a model artifact on its own can't reproduce a past decision if you don't also know exactly which version of everything else was involved. In our story, the CRM team changes its engagement export for reasons that have nothing to do with the churn model — and both training and production inherit that change anyway. The lesson is simple: treat your data dependencies with the same seriousness you'd treat a code dependency.",

"Make the feature contract explicit": "A good feature contract records more than just a data type — it records meaning. What does this feature actually measure? Over what time window, with what cutoff? What counts as valid, and what should happen when a value is missing? And who do you talk to before that upstream source changes? Take our feature, engagement_7d: it means app logins over the seven days ending at the scoring cutoff — and a missing value must never silently become a zero, because that's a completely different claim about the customer. A schema check alone would never have caught a change in what the feature actually means.",

"Separate responsibilities where change happens": "Clean interfaces let different parts of a system evolve on their own schedules, without forcing everything else to change along with them. Each module should have one clear reason to change, and the data and behavior crossing each boundary should be explicitly specified. Think about three very different kinds of change at our bank: fixing a connector changes how data gets prepared; changing a contact-frequency rule changes campaign policy; releasing a new M2 changes inference. None of those three should force the other two to change. And just because you've separated these concerns logically doesn't mean you're obligated to deploy them as three separate services — that's a different decision, made on its own merits.",

"Pipeline pattern: order the responsibilities": "Structuring your pipeline as explicit stages makes the transformations and their dependencies visible, instead of hidden inside one tangled script. Each stage should have a contract so the data passing between them stays understandable, and you want tests both at the stage level and across the whole pipeline. Failure handling matters too — you never want a partial result quietly passing itself off as a complete batch. Concretely: CRM records get validated before we ever compute engagement_7d or hand anything to M1. The goal of this structure isn't to hide the dependency on upstream data — it's to make it visible enough that you can actually reason about it.",

"Strategy pattern: replace one implementation": "The Strategy pattern lets a client code against a stable interface, while the actual implementation behind that interface can be swapped out. So you might replace how a feature gets prepared, behind an interface the rest of the system never has to know changed. But here's the catch for ML specifically: compatibility has to include meaning, not just matching types. Two implementations can both compile and both return a float, and still mean something subtly different. So even when you swap an implementation this way, evaluation and release approval still apply — being interchangeable in code is not the same as being equivalent in predictive behavior.",

"Observer pattern: notify, then investigate": "The Observer pattern decouples whoever notices a problem from whoever needs to act on it. A subject emits a meaningful event when something changes; subscribers receive that notification without being tightly wired to whoever produced it. The notification should carry real context — which cohort, which reference, what evidence backs it up. And here's the important boundary: receiving a notification is not the same as having authority to act on it. A missingness event tells the data and operations owners something's wrong; it does not, by itself, instruct anything to promote M2 into production. A good notification asks for attention — it doesn't quietly grant permission.",

"Version the system, not only the model": "A single prediction actually depends on a whole compatible set of things: what the data meant at the time, which code prepared it, which model scored it, and what configuration was active. Versioning the model alone misses most of that picture. If a CRM migration quietly changed what ‘engagement’ means, then knowing it was M1 that produced Ana's score tells you almost nothing useful on its own — you need the data definition that went with it too. Co-versioning is what actually connects your system's lifecycle to your model's lifecycle, instead of treating them as two separate stories.",

"Modules or services? Make the trade-off": "Splitting something into an independently deployable service is only worth it when that independence actually pays for its own operational cost. Modules give you strong logical boundaries with much simpler operations. Services let you scale and change pieces independently — but distribution brings its own failure modes and the headache of keeping versions coordinated across the boundary. At the bank, we'd separate feature preparation from policy logic cleanly as modules first, and only turn either into a separate service once there's real evidence it's worth the operational cost. There's no single best architecture for every ML system — the right answer depends on your actual constraints.",

"Architectural tactics connect concerns to controls": "Let's name the tactics we've actually been using throughout, now that Block 2 starts. Separation keeps data preparation, model execution, and business policy from tangling together. Observation is what makes both operational and predictive behavior something you can actually review. Recovery means restoring a whole compatible path, not just swapping back one file. And governance ties evidence, approval, access, and responsibility together into something accountable. In our CRM incident, a validation boundary is what contained the bad batch, and version links plus approvals are what made the repair trustworthy. A tactic earns its keep when you can point to its mechanism, its owner, and its evidence — not just gesture at a diagram.",

"CI, CD, and CT need different evidence": "CI, CD, and CT sound like one pipeline, but they automate genuinely different responsibilities. Continuous integration runs your code, contract, and path checks whenever something changes. Continuous delivery keeps a compatible change ready, waiting on an actual approval decision. Continuous deployment automatically releases anything that passes a defined policy. And continuous training trains and evaluates candidate models — but finishing that training run is not the same thing as being approved for production. A connector repair, for instance, can go through CI/CD perfectly well while M1 stays exactly as it is — fixing the pipeline doesn't require retraining the model.",

"Candidate training ends before promotion": "A model registry's job is to preserve candidate evidence — it is not, by itself, the approval. You need reproducibility: the exact data, code, configuration, and artifacts that produced a candidate. You evaluate it against both the current baseline and the cohorts that actually matter. Registration preserves identity and lineage so it can be properly reviewed. And promotion is a distinct act — authorizing a specific, compatible set of things for production, with a recovery plan already in place. Concretely: M2 sits in the registry as a candidate until it's actually reviewed, while M1 stays the one approved artifact scoring customers throughout the CRM repair.",

"Repair the input path; retain M1 when appropriate": "When the CRM incident needs fixing, what's actually required is a verified repair to the input path — not a reflexive jump to training a new model. First you repair the actual source or preparation defect. Then you version the reviewed fix together with its compatible configuration. You re-run it under a brand-new execution identity, and you validate the complete path end to end. Only then do you publish, and only once the evidence and approval requirements you've already defined are satisfied. B017 is the batch we held back; B017-R1 is the new execution that links the reviewed fix, the still-compatible M1, real validation evidence, and an actual publication approval. A passing connector test on its own was never going to be enough evidence.",

"Trace the prediction and the decision": "Lineage is what lets you connect input evidence, execution, approval, and whatever action followed — all the way through. A prediction's identity links it to a specific customer, a specific time, and a specific target window. Execution evidence tells you exactly which code, features, model, and configuration were compatible and in play. Decision evidence records which policy version applied and what action resulted. And because this evidence is sensitive, access to it needs its own controls. With this in place, an investigator really can trace back Ana's original score and, separately, the campaign's decision to contact her or not. A model version number alone was never going to reconstruct that whole story.",

"Recovery restores a compatible path": "Recovery means restoring a compatible path — and you should never be testing that path for the first time during an actual incident. First, know your target: what's the last compatible release, or a validated fallback you can trust? Rehearse the actual recovery procedure before you ever need it for real. When you restore, restore the whole set — data meaning, runtime, and configuration together, not just one piece. And afterward, verify by checking real stored scores and real consumer behavior, not just that a command ran successfully. Here's the trap in our incident: rolling M1 back does absolutely nothing to fix a CRM field that's still missing. The input path itself is what needs restoring. From here, we hand off to security — who's actually allowed to read, change, approve, or operate any of these paths?",

"Security threats depend on attacker access": "Before naming an attack by its textbook mechanism, locate exactly what the attacker can actually touch. Poisoning means altered inputs make it into training and corrupt the model that gets learned. Inference manipulation means altered inputs affect an already-trained model's output, at prediction time. Privacy inference means access to outputs or behavior reveals something sensitive about who's in the data. Each of these rests on different assumptions about access, knowledge, and goals. Picture a compromised CRM writer: it could affect current production inputs right away — but it only becomes a poisoning attack if those same altered records later get used to train a future model. And to be clear, our earlier CRM migration incident was accidental, not an attack at all — a genuinely different scenario.",

"Enforce access at the resource boundary": "A trust boundary only matters if it's actually enforced — not just drawn as a box on a diagram. Authentication establishes who's calling. Authorization checks whether that caller can do this specific operation on this specific resource. Validation enforces the input contract completely independently of who's asking. And audit preserves a real trail of access and change. Concretely: the scoring service should be allowed to read the approved M1 artifact — but reaching the model registry should never, by itself, grant it permission to promote M2 into production. Those are different operations and need different permissions.",

"Least privilege follows responsibilities": "Least privilege means scoping every identity to exactly the operations and resources it actually needs — nothing more. Separate the duties clearly: training a candidate model should never, on its own, carry the authority to release it. Protect credentials properly, and keep secrets out of code and out of broad-access logs. And connect access changes, source updates, and approvals so they're reviewable together. A campaign user, for example, should only be able to read an approved score view — not raw training data, and definitely not production deployment credentials. This simplified matrix is meant as a starting point for thinking it through, not a complete real-world permission design for an actual bank.",

"Privacy: expose what each role needs": "Campaign work and incident investigation genuinely need different views into the same customer data. Minimize what you collect and what ends up exposed in any output. Keep those views separate by purpose — what a campaign team needs is not what an investigator needs. Protect logs with clear retention and access rules. And preserve accountability without making raw evidence broadly available to everyone. Campaign staff might reasonably need Ana's approved score and her eligibility status; an investigator looking into an incident might need much more restricted, fully versioned evidence. Privacy, in this sense, is a design decision about access and data use — not a label you attach after the fact because you used some particular technique.",

"Privacy techniques have specific limits": "Before reaching for a specific privacy technique, name exactly what you're trying to protect, and from whom. Tokenizing an identifier or generating synthetic data doesn't automatically mean you've achieved anonymity — those are separate claims that need their own evidence. Federation changes where data physically lives; it doesn't eliminate every way information could leak. And differential privacy needs a clearly defined protected unit and careful accounting across every release — we won't derive the mathematics here, but the idea matters: protecting one single transaction is a very different problem from protecting everything one customer ever contributed. Never announce a privacy guarantee without naming its actual assumptions and the evidence behind it.",

"Use the quality checklist as a review tool": "Think of a quality checklist as a tool for structured review, not a certificate you can wave around. Both system concerns and process concerns matter for ML-heavy systems. Pick the checks that are actually relevant to you, rather than treating a short published list as the entire checklist. And for each concern you do pick, map it to a real control, a real owner, and real evidence. As one example: completeness validation is genuinely good evidence about input quality — but it says nothing at all, by itself, about defense against a sophisticated cyberattack. Be honest about what a checklist item actually proves, and keep its limits visible.",

"Predictive quality and system performance": "Choosing an acceptable model means weighing several different kinds of quality against each other, not just picking the most accurate one. Accuracy alone is a weak objective, especially when churners are a small minority of customers. Performance has to include the real end-to-end deadline and the resources you're spending. Complexity needs to earn its cost, both in training and in ongoing operation. What counts as acceptable genuinely depends on the task and on what an error actually costs. A heavier, fancier churn model is only worth it if its quality gain actually justifies the cost — and it still has to hit the campaign's deadline. Decide what ‘good enough’ means before you go looking for a fancier model.",

"Robustness: invalid, unfamiliar, or ordinary?": "Not every unusual input deserves the same response, and it's worth telling three cases apart. Contract validity and whether the model actually applies well to this case are two separate questions. An out-of-distribution input might be perfectly valid by the contract, just poorly represented in what the model was trained on. And high confidence from the model is not, on its own, a reliable sign that an input is actually familiar to it. A missing activity value is simply invalid — that's a contract failure. A genuinely new customer population might be entirely valid data, yet still sit outside where the model is reliable. Your architecture needs an explicit, deliberate response for the moment the model probably shouldn't be trusted.",

"Explainability and auditability differ": "Explaining why a model produced a particular output, and reconstructing exactly how a historical decision was made, are related but genuinely different jobs. An explanation helps you interpret the model's behavior in context. Auditability needs real historical evidence and versions you can actually trace. And reviewing a decision properly includes the business policy and the action taken — not just what the model output. It's worth saying plainly: tools like SHAP or LIME do not prove causality, and they do not prove fairness. An engagement feature's contribution might help explain why Ana's score came out the way it did — it cannot tell you why she would actually choose to leave the bank. The real test of auditability is whether an authorized reviewer can actually retrieve the evidence when it matters, not whether you drew a nice diagram of the process.",

"Fairness: prediction versus treatment": "Before picking a fairness metric, be precise about what you're actually comparing. Prediction fairness looks at whether errors or calibration differ across relevant groups. Treatment fairness looks at something different — who actually gets access to an offer, and what the policy's real effects are. Which target matters depends on context — on the actual harms at stake and what's required of you. And no single metric settles every fairness question on its own; there are real trade-offs between them. Equal error rates in churn prediction do not automatically mean equal access to retention offers once the campaign's own allocation rules are applied. Keep predictive quality and the real-world consequences of intervening cleanly separate in how you think about this.",

"Airflow: make workflow dependencies visible": "A tool like Airflow earns its place by making task order, failure handling, and execution evidence visible — it orders the dependent pieces of your pipeline. The evidence it gives you is task state, timing, and the context each run executed in. When something fails, operators and source owners can actually see and inspect that failed dependency. For us, the required CRM validation step has to sit upstream of scoring and export, specifically so that its failure blocks everything downstream from running on bad data. One honest limit, though: orchestration on its own gives you none of the evidence you need to judge predictive quality or approve a release — that's a different job entirely.",

"MLflow: connect experiments and artifacts": "A tracking tool like MLflow supports reproducibility and review — but only if you actually design the evidence links deliberately. It connects your training evidence to your model artifacts. What it gives you is the run, the configuration, the metrics, and the artifact's identity. Reviewers use that to compare candidates and verify what's actually compatible before releasing. In our story, the approved M1 stays linked to its own evidence, while B017-R1 gets recorded separately, with its own distinct input and execution context. No single tracking tool hands you every governance control you need — it supports the release decision, it doesn't replace the policy behind it.",

"Validation and drift reports support diagnosis": "A validation or drift report earns its usefulness from four things being clear: its reference, what the feature actually means, which cohort it covers, and who's supposed to respond to it. Validation tests the expectations you've actually declared, before anything gets used downstream. Drift comparison checks change against a reference you've explicitly named. Tools can genuinely help with both of these roles — just keep the actual policy decisions out of the screenshot itself. And always, preserve the evidence and assign someone to respond to it. A missing CRM feature needs a contract-failure response; a population that's shifted but still valid needs a completely different kind of investigation. Tools make evidence easier to gather — the architecture is what decides what that evidence actually means.",

"ML architecture connects five responsibilities": "Let's step back and look at the whole system one more time, and what actually makes a prediction usable. Data has to preserve its meaning, its validity, and consistency over time. Models need their uncertainty evaluated and their approved, compatible versions carefully managed. Operations means observing, diagnosing, releasing, and recovering — all as an ongoing discipline, not a one-time setup. And decisions means protecting access and properly governing whatever business action follows. Trace it back to Ana: her score only becomes genuinely usable through validated inputs, execution you can actually trace, a model release that went through approval, and a campaign policy that's kept entirely separate from the prediction itself. Tomorrow, on Day 2, we'll see that foundation models and agents keep needing exactly these same controls — even as the components and the ways things fail change underneath them.",

"Sources and adaptation boundaries": "One last thing before we close. Our bibliography is where the real concepts come from; the bank diagrams and the incidents you've seen today are our own invented teaching applications of those concepts, built to make them concrete. The core readings cover architectural decisions, serving, maintenance, and quality; the supporting readings extend into monitoring, governance, and security. To be completely clear: Ana, her scores, the dates, the batches, the incident — all of it is invented for this lecture. No real churn outcome, no real repaired score, no real retention benefit, and no real bank tool execution is being claimed anywhere in this talk. A separate guide records exactly where each idea in this lecture actually comes from, and the limits of how we've adapted it.",
}


# Colleague content merge and targeted clarity improvements, 19 October 2026.
SCRIPTS.update({'What a test can’t tell us today': 'On scoring day, which we call D0, software tests can tell us '
                                    'that the job finished, the inputs matched their contract, and '
                                    'the scores were saved for the expected customers. These are '
                                    'useful checks we can perform immediately.\n'
                                    '\n'
                                    "But Ana's score of 0.70 is a risk estimate, not a statement "
                                    'that she definitely leaves. Her next-30-day outcome does not '
                                    'exist yet. Once the window closes and the labels arrive, we '
                                    'link them to the original scores and evaluate precision and '
                                    "recall across the cohort; one customer's outcome cannot "
                                    'validate a probability estimate on its own.\n'
                                    '\n'
                                    'With the same inputs and a fixed model, the score can remain '
                                    'reproducible while the prediction is still uncertain. We do '
                                    'not have to wait for labels to catch a broken input contract. '
                                    'Simon will return to this distinction when he explains what '
                                    'monitoring can check now and what must wait.',
 'How do predictions reach the business?': 'The first serving decision is when the business '
                                           'actually needs a prediction. Read the three rows from '
                                           'left to right. In the first, a scheduled job takes a '
                                           'customer snapshot, computes many scores, and saves '
                                           'them for a campaign to read later. That is offline, or '
                                           'batch, serving.\n'
                                           '\n'
                                           'In the second row, an application sends a request to a '
                                           'prediction API and waits for the response. In the '
                                           'third, the online application publishes an event; a '
                                           'stream processor invokes the model and publishes an '
                                           'output for another system to consume. Asynchronous '
                                           'does not mean there is no deadline.\n'
                                           '\n'
                                           "For our bank's monthly churn campaign, a central batch "
                                           'is sufficient. Location is a separate choice: central, '
                                           'embedded, or edge. Pushing this churn model to devices '
                                           'would add rollout work without serving an identified '
                                           'need. The architecture question comes first: does this '
                                           'decision actually require real-time inference?',
 "Batch path: Ana's score on day D0": 'Follow the same source-to-policy path from the shared '
                                      'architecture on slide 6. Here we are expanding the batch '
                                      'part of that path. First, define the scoring cutoff, D0, '
                                      'the customer population, and how fresh the source data must '
                                      'be. Ana, C042, is included in that snapshot.\n'
                                      '\n'
                                      'Next, validate the inputs and prepare the features '
                                      'consistently. Her seven-day login count has fallen from '
                                      'seven to one. The current approved model, M1, produces our '
                                      'illustrative score of 0.70. That output is saved with her '
                                      'customer identity, the scoring date, and the model and '
                                      'feature versions.\n'
                                      '\n'
                                      'Finally, reconcile written, rejected, and withheld records '
                                      'before exposing a validated batch to the campaign. Saving '
                                      'scores at scale is itself an architectural responsibility. '
                                      'A final task turning green does not establish that every '
                                      'expected customer was accounted for, or that Ana will '
                                      'actually churn; her future outcome is still unknown on D0.',
 'Online serving: the fraud contrast': 'These three rows are comparisons, not extra services we '
                                       'are adding to the churn system. For payment blocking, the '
                                       "authorization service waits for the fraud API's response. "
                                       'That is synchronous. For a fraud alert, the transaction '
                                       'can instead be published as an event, scored by a stream '
                                       'processor, and sent to another application '
                                       'asynchronously.\n'
                                       '\n'
                                       'The third row shows a hybrid: churn scores are still '
                                       "computed in batch, but a CRM screen can look up Ana's "
                                       'stored score quickly from a customer-keyed store. A fast '
                                       'lookup is not the same thing as calculating a new '
                                       'prediction during the request.\n'
                                       '\n'
                                       'End-to-end response time includes feature lookup and data '
                                       'preparation, not just the model. Smaller models, leaner '
                                       'execution, or accelerators may reduce computation, with '
                                       'cost and quality trade-offs. Asynchronous paths also need '
                                       'idempotent consumers, lag monitoring, and failed-message '
                                       "handling. The bank's monthly churn campaign continues to "
                                       'use batch inference.',
 'Release strategies: what each proves': 'Read the table across: the strategy, who is exposed, and '
                                         'what evidence it produces. In shadow deployment, '
                                         'customers are not acted on using the candidate model, '
                                         'M2. The current approved model, M1, still supplies the '
                                         "action path, while M2's results are logged. We can "
                                         'compare score differences now, but predictive quality '
                                         'still needs labels.\n'
                                         '\n'
                                         'A canary allows a limited, approved cohort to use M2. It '
                                         'reduces exposure and needs clear stop rules and a '
                                         'rollback path. Operational success over that cohort does '
                                         'not establish 30-day churn quality.\n'
                                         '\n'
                                         'An A/B test needs comparable assigned groups and one '
                                         'clearly stated intervention. Ask whether M2 ranks churn '
                                         'risk better than M1 separately from whether offer B '
                                         'retains more customers than offer A. If we change both '
                                         'the model and the offer together, we cannot cleanly '
                                         'attribute the result to either. A canary controls '
                                         'rollout risk; it is not automatically an experiment.',
 'Release plan: shadow, canary, rollback': 'This is our proposed release design for the teaching '
                                           'case, not a rollout that has already happened. In the '
                                           'first cycle, the candidate model, M2, scores the same '
                                           'batch as the current approved model, M1, but its '
                                           'outputs cannot generate offers. In a later cycle, a '
                                           'limited approved cohort can use M2 under defined stop '
                                           'rules.\n'
                                           '\n'
                                           'There are two clocks. Compatibility checks, run '
                                           'health, and score differences are available '
                                           'immediately. Churn quality requires the target window '
                                           'and reliable labels. Promotion is a separate '
                                           'evidence-and-approval decision, so one or two extra '
                                           'cycles can be an acceptable cost for limiting customer '
                                           'exposure.\n'
                                           '\n'
                                           'A rollback may return the campaign to a previously '
                                           'validated M1 batch only if its customer population, '
                                           'freshness, and eligibility are still suitable. '
                                           'Otherwise pause use or create a new validated batch '
                                           'with a compatible approved release. Changing the model '
                                           'does not repair invalid source data. Keep the model, '
                                           'features, configuration, and approval linked; Matheus '
                                           'develops that governance later. Simon now takes over: '
                                           'after the first run works, what tells us it stays '
                                           'reliable?',
 'Drift detection: methods and their purpose': 'These methods compare input distributions. They do '
                                               'not, by themselves, tell us whether predictions '
                                               'became less accurate or whether the bank lost '
                                               'business value. The table gives us a useful '
                                               'interpretation and a limitation for each method; '
                                               'we do not need the calculations here.\n'
                                               '\n'
                                               '<b>PSI:</b> compares the share of customers in '
                                               'fixed bins. It is useful for seeing a changed '
                                               'input mix, but the result depends on the bins and '
                                               'the reference we chose.\n'
                                               '\n'
                                               '<b>KS:</b> compares two continuous distributions '
                                               'and looks for their largest cumulative separation. '
                                               'Sample size affects how readily a difference is '
                                               'detected. The usual continuous-distribution test '
                                               'needs care with discrete counts such as app logins '
                                               'or many tied values; a small p-value is not a '
                                               'measure of business harm.\n'
                                               '\n'
                                               '<b>KL divergence:</b> describes a directional '
                                               'difference between distributions, so reversing '
                                               'reference and current changes the interpretation. '
                                               'Categories with zero reference probability need '
                                               'careful handling. <b>JS divergence</b> gives a '
                                               'symmetric comparison, but it still measures '
                                               'distribution difference, not model accuracy.\n'
                                               '\n'
                                               '<b>Reference</b> means the named baseline '
                                               'population and period, using the same feature '
                                               'definition. A <b>threshold</b> is the alerting '
                                               'rule we choose for the application, not a '
                                               'universal cutoff. <b>Segments</b> are customer '
                                               'subgroups we check separately, because an overall '
                                               'average can hide a local change. <b>Action</b> '
                                               'means investigate data validity, source changes, '
                                               'and any available outcome evidence; a drift '
                                               'statistic alone does not authorize retraining.',
 'Shadow deployment: observe without acting': 'Shadow deployment lets a new candidate model '
                                              'quietly score the same real inputs as the approved '
                                              'model, without ever influencing a real decision. We '
                                              "run both in parallel, and we're careful to record "
                                              'which output came from which model — the current '
                                              'approved model (M1) or the candidate model (M2). At '
                                              "this stage we're only comparing operational "
                                              'behavior and how the scores differ; we still need '
                                              'to wait for actual outcomes to judge predictive '
                                              "quality. At our bank, only M1's record is ever "
                                              'eligible to trigger a campaign offer — M2 running '
                                              'in the shadows can never create a second, invisible '
                                              'offer.',
 'Input checks now; quality checks later': "As Ricardo introduced earlier, there's an unavoidable "
                                           'delay baked into how we evaluate churn predictions: we '
                                           'define a target window, so by definition the full '
                                           "outcome isn't known yet when we score someone. At "
                                           'scoring time, all we can check is whether the inputs '
                                           'were fresh, complete, and the pipeline ran correctly. '
                                           'Only once that window closes and the real labels '
                                           'arrive can we join them back to the original score and '
                                           'properly evaluate precision, recall, and calibration '
                                           "by cohort. Think of Ana's score on day zero: it's "
                                           'saved with its full context, but we genuinely cannot '
                                           'evaluate it properly until 30 days later. And a '
                                           'missing label at that point does not mean she stayed — '
                                           "it might just mean the data hasn't arrived yet."})
