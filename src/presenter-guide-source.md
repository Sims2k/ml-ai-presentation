# ML Architecture

A bank customer-churn case

## Presenter guide — content draft

20 October 2026 · English · approximately 60 minutes · five presenters

This guide follows the 38-slide storyboard. The final deck has not yet been built: its visual style is awaiting selection. Match slide numbers again after any later splits. The wording below is a speaking aid rather than a script that must be read verbatim. Source locations refer to PDF file pages, not necessarily printed book pages.

### The shared teaching contract

Keep the following facts identical across all sections. Ana is fictional, identified as C042. Her weekly app logins fall from seven to one and an illustrative original model output is 0.70. These details do not establish why she might leave. Her outcome is unknown when scored. The bank prepares monthly batches targeting churn during the following 30 days; these precise choices are our simplified teaching design. Bass's case supplies the bank setting and workflow.

M1 names the approved model. M2 is an optional candidate, not a replacement that has already been released. B017 is a failed batch attempt: a CRM migration leaves engagement values missing and the entire batch is held before publication. B017-R1 identifies the separate repaired execution. The repair may preserve M1. No post-repair score, customer outcome, completed offer, or measured retention improvement has been established.

A missing feature is not zero activity. A failed input contract is not automatically concept drift. A drift alert does not prove accuracy loss; completed training does not approve release; a successful software run does not prove predictive quality. Campaign policy remains separate from prediction. An alarm, a publication gate, an investigation, a source repair, a fallback, a rollback and candidate training each have different responsibilities.

### Timing and handoffs

| Slides | Owner | Section | Time |
|---|---|---|---|
| 1–6 | Ricardo | Foundations | 0–8 minutes |
| 7–12 | Tomás | Serving | 8–17 minutes |
| 13–18 | Simon | Monitoring and diagnosis | 17–26 minutes |
| 19–23 | Luca | Design and dependencies | 26–35 minutes |
| 24–28 | Matheus | Controlled change | 35–44 minutes |
| 29–32 | Simon + Matheus | Security and privacy | 44–51 minutes |
| 33–35 | TBD | Quality review | 51–56 minutes |
| 36–38 | TBD / all | Tools and close | 56–60 minutes |

These durations include builds and speaker changes. Keep statistical derivations, detailed privacy mechanisms and tool tours out of the main talk. If running late, shorten a comparison's explanation; preserve the transitions connecting fault, diagnosis and repair.

## Ricardo — foundations

### 1. ML Architecture

**Time:** 0:00–0:30. **Purpose:** establish the question that unifies the presentation.

Open with the bank's practical need: identify customers at risk early enough to consider useful retention action. The audience will follow a prediction into use, encounter a broken input, and see how architecture supports diagnosis and controlled recovery. The talk's subject is the system around that prediction, including the decisions people make.

**Visual/build:** let the topic-led title settle before explaining the case. The cover contains no Ana record or numerical risk score; those are introduced on the next slide. Avoid reading the title, names and subtitle aloud in sequence. **Transition:** “Let's meet one customer before opening the architecture.” **Anchor:** group handoff §§1–2; Bass Chapter 14, PDF 430–434.

### 2. Meet Ana. Her outcome is still unknown.

**Time:** 0:30–2:00. **Purpose:** establish essential ML vocabulary through a concrete record.

Ana's app logs are data. A consistent count of logins during the seven days ending at the scoring cutoff is a feature. A trained model turns prepared features into a risk estimate; in our invented example its output is 0.70. A label is the later observed churn outcome, defined consistently for learning and evaluation. Churn means ending the banking relationship, not simply opening the app less often.

**Visual/build:** reveal records, prepared input, score and unknown outcome separately. Explain that training learns from earlier labeled examples, while this current prediction is temporarily unlabeled. Do not describe the falling login count as proof of intention. **Transition:** “Even with that score, the bank still has a separate decision to make.” **Anchor:** handoff §1; personal notes §1; Bass PDF 430–433.

### 3. The model estimates. The campaign decides.

**Time:** 2:00–3:30. **Purpose:** make the prediction-to-action boundary explicit.

The score supports a retention process. The campaign must still consider contact preferences, eligibility, previous contacts and budget. A high-risk estimate does not mean the customer automatically receives an offer. No contact is also a possible policy outcome. Changing a contact-frequency rule should not require relearning the churn model.

**Visual/build:** follow the score into a distinct policy component and reveal the possible action or no-action outcome. Label this boundary by responsibility rather than by a particular product. The benefit of an offer is a separate question from how accurately the model predicts churn.

**Transition:** “Now place those responsibilities inside the complete system.” **Anchor:** handoff §§1–2; personal notes §1; Bass PDF 433–434. The specific policy gate is our teaching design.

### 4. One architecture, two paths.

**Time:** 3:30–5:00. **Purpose:** establish the map that later speakers reuse.

Read the production path from left to right: source records, preparation and validation, scoring with M1, saved scores, then campaign policy. Below it, historical features and mature labels support candidate training and evaluation. Only a compatible approved model enters production. Later bank outcomes can be joined to saved scores to assess quality; campaign action history helps interpret what happened.

**Visual/build:** introduce production first, then the learning and review responsibilities. The dashed return requests review; it does not automatically replace M1. Current input checks will receive more attention in Simon's section. Keep each node's location and meaning consistent when returning to this map.

**Transition:** “These paths evolve at different rates.” **Anchor:** handoff §2; personal notes §1; Bass Chapter 14; Kalinowski §§13.2–13.3. The combined map is a teaching synthesis.

### 5. Software and models change on different clocks.

**Time:** 5:00–7:00. **Purpose:** connect familiar software maintenance to ML dependencies.

Software engineers can change a connector or business rule, integrate the code, run tests and release it. Model development also needs suitable examples, feature definitions, learning and evaluation. Its feedback may arrive weeks after a prediction. The two activities depend on each other: changing input meaning can alter a prediction even when model bytes remain unchanged.

**Visual/build:** show two lanes converging on a compatible release. A code test can establish that the job processes a record and writes the expected schema. It cannot establish Ana's future label today. A fixed model's prediction can be deterministic while its estimate remains uncertain; avoid calling all ML execution random.

**Transition:** “The rest of the presentation follows the decisions at those boundaries.” **Anchor:** handoff §4; Kalinowski §13.2, PDF 403–406; personal notes §§1, 3.

### 6. Six questions will guide the story.

**Time:** 7:00–8:00. **Purpose:** orient the audience without reciting a source bibliography.

Use the six existing questions: what is needed beyond a model, how scores reach campaigns, how problems are detected, how dependencies are controlled, how a repair is released, and how the system's quality and safeguards are evaluated. Security, privacy and tools support these same responsibilities. Each presenter advances the bank story rather than starting a new example.

**Visual/build:** keep the overview sparse. Highlight the next question rather than explaining every later slide. **Handoff to Tomás:** “We know what the bank wants and what the surrounding system must do. How does an approved model actually deliver usable scores?” **Anchor:** reference deck presentation map; handoff §§3–5.

## Tomás — serving

### 7. Finish the batch before the campaign needs it.

**Time:** 8:00–9:30. **Purpose:** choose a service objective from the use case.

Walk one normal batch: required sources arrive, records are checked, features are computed, the compatible M1 package is loaded, scores are stored and expected coverage is reconciled. The objective is a complete validated batch in time for its campaign. The team has not specified a real numerical deadline or availability target, so do not invent one.

**Visual/build:** reveal the normal path once, emphasizing that consumers use saved scores. Completion means accounting for the intended customer population, not merely reporting that the last task exited successfully. Rejected or missing records must be visible in that accounting.

**Transition:** “This works because the campaign can use precomputed results. Other timing needs imply different flows.” **Anchor:** handoff §5; Bass PDF 433–434; Kalinowski §13.3, PDF 407–408.

### 8. Batch, synchronous, and asynchronous answer different timing needs.

**Time:** 9:30–11:00. **Purpose:** compare serving interactions precisely.

Batch processes many records and stores results for later consumption. In a synchronous interaction a caller waits for the response before continuing. In an asynchronous design, messages separate request or event production from processing and result delivery. The prediction may still need to arrive quickly even though the original caller does not wait on one direct request-response call.

**Visual/build:** step through three small flows. For asynchronous inference, identify event producer, message transport, processing and prediction consumption. Fraud detection is a brief example from the reading; do not turn it into a second bank subsystem to explain.

**Transition:** “When a prediction arrives and where it runs are separate choices.” **Anchor:** Kalinowski §13.3, PDF 407–411; handoff §5.

### 9. Timing and location are separate choices.

**Time:** 11:00–12:00. **Purpose:** prevent a common conflation in deployment terminology.

A model can run centrally, embedded in an application, or near a device. Those locations do not by themselves specify batch, synchronous or asynchronous behavior. An edge deployment can respond locally; a central service can participate in a message-based architecture. Choose the location using resource, connectivity, ownership and operational requirements.

**Visual/build:** use a compact comparison of the two design dimensions. Mark the selected teaching configuration: centrally governed batch scoring for churn. Edge remains an alternative, not another required component. **Transition:** “Whichever location we choose, the artifact must carry compatible assumptions.” **Anchor:** handoff §5; Kalinowski Chapter 12 as supporting reading and §13.4, PDF 411–414. Full Chapter 12 was not freshly reread for this draft.

### 10. Package a compatible set.

**Time:** 12:00–13:00. **Purpose:** distinguish executable packaging from release authorization.

The learned model needs its dependencies, expected input schema, feature semantics and scoring configuration. Check that the intended runtime can load it and perform inference. A column with the same name but a different time window is not necessarily compatible. Containerization can standardize a runtime; it does not establish that the inputs represent the right business meaning.

**Visual/build:** group the compatible pieces into one package. Keep the approval or rollout decision outside that grouping. **Transition:** “A package can run successfully and still need a controlled introduction.” **Anchor:** Bass §14.1.4, PDF 442–443; handoff §5; preparation semantics are our bank-specific application.

### 11. Shadow observes; canary limits exposure.

**Time:** 13:00–15:00. **Purpose:** make the action path visible during a rollout.

In shadow mode, M1 and candidate M2 may score the same batch, but only the approved action path can influence the campaign. Candidate outputs are comparison records. A canary lets a limited approved cohort use the new version while the remainder retains the old one. In both cases, customer eligibility must prevent duplicate offers.

**Visual/build:** reveal which score path is enabled for action. Separate early execution, compatibility and coverage evidence from predictive quality, which requires mature churn outcomes. A short clean canary cannot settle a 30-day quality question.

**Transition:** “Exposure control is different from an experiment about an outcome.” **Anchor:** handoff §5; personal notes §§3–4; Breck infrastructure tests 6–7 as recorded in the source ledger. The specific batch routing is our teaching application.

### 12. An A/B test needs a stated intervention and outcome.

**Time:** 15:00–17:00. **Purpose:** separate model comparison from retention-treatment evaluation.

An experiment needs a clear question, appropriate group assignment and a measured outcome. State whether the alternative is the risk model, the campaign treatment, or another controlled change. If model selection and treatment change together, interpreting an observed retention difference becomes harder. Comparing people who received an offer with everyone else is not automatically a valid estimate of the offer's effect.

**Visual/build:** follow assigned groups through one defined alternative to a later outcome; avoid unsupported numerical lift. Record which model and policy each group used.

**Handoff to Simon:** “The first scoring run worked. What evidence tells us it remains reliable when sources and customer behavior change?” **Anchor:** handoff §5 and personal notes §3; experimental framing is a teaching synthesis.

## Simon — monitoring and diagnosis

### 13. The CRM changed. The model did not.

**Time:** 17:00–18:30. **Purpose:** introduce the recurring incident before the terminology.

A CRM migration makes engagement values unavailable for part of B017. M1 is unchanged. Missing values are not evidence of zero app activity; replacing them with zero would create a new unvalidated interpretation. The input gate holds the entire batch before publication, so no new B017 scores are released for campaign use.

**Visual/build:** reveal the upstream change, the failed feature boundary and the publication hold in that order. Distinguish the gate that blocks use from the alert that tells someone to investigate. Ana's 0.70 belongs to the earlier valid illustrative record; do not invent a new score for the defective input.

**Transition:** “We have evidence of a fault. We still need to distinguish what kind of change occurred.” **Anchor:** personal notes §4; handoff §6; source-change risk in Bass §14.1.1. The incident and whole-batch hold are our choices.

### 14. Locate the change before naming the remedy.

**Time:** 18:30–20:00. **Purpose:** distinguish diagnostic possibilities.

Ask whether the inputs are valid, whether training and production compute them consistently, whether the population changed, and whether the relationship to churn changed. A source-quality fault concerns absent, stale or incompatible records. Training-serving skew concerns inconsistent preparation. Input drift concerns the distribution of valid features. Concept drift concerns the relationship between valid inputs and the outcome.

**Visual/build:** reveal one diagnostic question at a time, anchored to its place in the shared map. These conditions can coexist; the diagram is not a claim that they are mutually exclusive. A missingness alarm alone identifies neither an attacker nor concept drift.

**Transition:** “The two statistical changes are easier to distinguish with pictures.” **Anchor:** personal notes §§2–4; handoff §6; Bass §14.1.5. The precise distinctions follow the study notes' technical treatment.

### 15. Feature drift and concept drift change different things.

**Time:** 20:00–21:30. **Purpose:** teach the difference using the paired plots.

First explain the axes and points: each fictional customer has two scaled activity features. In the feature-drift comparison the input population changes while the illustrative input-to-outcome relationship is held fixed. In the concept-drift comparison the positions are held fixed while the assumed relationship changes. The old deployed boundary remains visible; it has not automatically learned the new relationship.

**Visual/build:** show reference, then current, then the explanatory highlight. Actual stay/leave colors represent later known outcomes in these thought experiments. They are not immediately observable labels for the latest batch. An input shift can be detected before labels; concluding how prediction quality changed needs further evidence.

**Transition:** “A monitoring calculation also needs a specified reference.” **Anchor:** personal notes §2; visual-sources.md records the Fiddler-inspired adaptations. All plotted bank coordinates are invented.

### 16. Compare populations against a defined reference.

**Time:** 21:30–22:30. **Purpose:** introduce drift statistics without a mathematical detour.

The notes compare activity groups changing from 60/30/10% to 30/40/30%. No churn labels are needed for that comparison. PSI summarizes changes in common bins, KL compares distributions directionally, and JS provides a symmetric comparison. They have different properties and scales. KS instead uses the largest cumulative-distribution gap, with test assumptions that must fit the input type.

**Visual/build:** read the changed bars, then name the methods briefly. State that feature definition, population, reference period, binning and sample size affect interpretation. No universal threshold turns these statistics into model accuracy or a command to retrain.

**Transition:** “Some evidence is available now; other evidence must wait.” **Anchor:** personal notes §3 and optional atlas; Bass PDF 444 names stability/divergence techniques; formula derivations stay in backup material.

### 17. Check inputs now; evaluate prediction quality later.

**Time:** 22:30–24:00. **Purpose:** make feedback delay visible.

At scoring time, check freshness, completeness, coverage, valid features, job completion and score distributions. Ana's 30-day outcome is still pending. After the defined window closes and labels arrive reliably, join outcomes to the original saved predictions. Record prediction time, target window and label definition so that next month's outcome is not attached to this month's score.

**Visual/build:** walk the upper immediate-check lane, then the later-label lane. A missing outcome during ingestion is not evidence that the customer stayed. If illustrating two extra ingestion days from the notes, label them invented. The bank need not wait for labels to stop an incompatible input batch.

**Transition:** “The alert needs enough connected evidence for someone to choose a response.” **Anchor:** personal notes §3; handoff §6; visual-sources.md for the delayed-feedback adaptation.

### 18. An alert starts an investigation.

**Time:** 24:00–26:00. **Purpose:** connect monitoring to operational diagnosis and a justified remedy.

Use B017 to locate the CRM export, feature definition, code and last healthy run. The notes' optional example has 170 missing values among 1,000 expected rows, compared with a 0.5% reference and an invented 2% hold threshold. The denominator includes the expected population; counting only received rows could conceal missing records. The gate holds publication; an assigned owner investigates the change.

**Visual/build:** move from alert to protected evidence, affected scope, source-change timing and selected response. Repairing the mapping may be sufficient. Fallback, rollback or candidate training are considered for different evidence; they are not synonyms. Leave detailed release mechanics to Matheus.

**Handoff to Luca:** “We found the broken data path. Which dependencies allowed another team's CRM change to reach our predictions?” **Anchor:** personal notes §4; handoff §6. All alert values and policies are illustrative.

## Luca — design and dependencies

### 19. An implicit arrow hides a contract.

**Time:** 26:00–27:30. **Purpose:** turn the incident into a design decision.

The phrase “CRM feeds the model” hides assumptions about identity, timestamps, feature meaning and ownership. Define engagement_7d as the count of logins during the seven days ending at the scoring cutoff. Include type, missingness policy, compatible preparation and the team responsible for source changes. The migration must preserve those meanings or initiate coordinated review.

**Visual/build:** compare the implicit dependency with an explicit source contract and feature-validation boundary. For our case, missing engagement fails the contract and holds the batch. This is a proposed control rather than a statement that the book describes our exact gate.

**Transition:** “That boundary gives us a place to assign responsibility.” **Anchor:** handoff §7; Bass §14.1.1, PDF 434–436; Nazir §§5–6 for context-sensitive decisions.

### 20. Separate responsibilities where change happens.

**Time:** 27:30–29:30. **Purpose:** connect familiar modularity to the bank's maintenance problems.

Ingestion obtains source records. Preparation checks and computes features. Scoring applies the approved learned rule. Storage preserves results and version links. Campaign policy decides appropriate action. A connector repair belongs near preparation; a contact-limit change belongs to campaign policy. Those different reasons for change should remain understandable and testable.

**Visual/build:** highlight each change on the same map rather than drawing a new architecture. A clean interface can exist between modules in one process. Distributing those modules creates additional network and operating obligations; separation of concerns does not itself select microservices.

**Transition:** “Patterns can make one of those boundaries easier to implement.” **Anchor:** handoff §7; personal notes §1; Kalinowski Chapter 14; Nazir PDF 10–13.

### 21. Patterns clarify a boundary.

**Time:** 29:30–31:30. **Purpose:** explain pattern benefits through concrete interactions.

Pipeline divides processing into steps, placing required validation before scoring. Strategy provides a stable interface behind which a preparation or algorithm implementation can change. Observer notifies interested components of an event, such as a monitoring result. These solve different design problems. An interface-compatible replacement still needs behavioral validation, and a notification does not authorize promotion.

**Visual/build:** three small views should each show the problem and the boundary clarified. Avoid reading a catalogue of patterns or presenting a full code lesson. Dependency injection can be mentioned as supplying replaceable dependencies without hard-wiring unrelated configuration into business logic.

**Transition:** “Replaceability also requires knowing which versions are compatible.” **Anchor:** Kalinowski §14.3, PDF 433–437; handoff §7. The bank mappings are teaching applications.

### 22. Version the system, not only M1.

**Time:** 31:30–33:00. **Purpose:** show why model identity cannot reconstruct an output alone.

The same M1 artifact can receive features computed differently or run with different configuration. A score record therefore needs links to the relevant source/feature definition, preparation code, dependencies, model, scoring configuration and time. These links let the team identify which compatible set actually produced a batch.

**Visual/build:** reveal the supporting version references around one model or prediction record. Avoid turning this into a requirement to duplicate every raw customer transaction in logs. Sensitive evidence can remain behind controlled references, subject to retention and reproducibility needs.

**Transition:** “How much physical separation is useful for those responsibilities?” **Anchor:** Kalinowski §13.2 co-versioning, PDF 403–406; Bass registry discussion, PDF 442–443; handoff §7.

### 23. Independence has an operating cost.

**Time:** 33:00–35:00. **Purpose:** make architecture selection a trade-off rather than a slogan.

Modules can give a clear separation of responsibilities with simpler operation. Services may support independent ownership, deployment and scaling, but they introduce communication failures, interface evolution, release coordination and distributed recovery. Evaluate those benefits against the actual bank team's needs and capacity.

**Visual/build:** compare a few parallel concerns. Do not claim that Nazir proves microservices always win—or always fail with changing data. The paper reports context-dependent recommendations and remaining evidence gaps. Our contract and modularity decisions are a reasoned response to this particular teaching incident.

**Handoff to Matheus:** “The responsibilities and compatibility rules are clear. How do we make the checks repeatable and traceable?” **Anchor:** Nazir §§5–6, PDF 10–13; Kalinowski §§14.3–14.4; handoff §7.

## Matheus — controlled change

### 24. Repair the data path; retain M1.

**Time:** 35:00–37:00. **Purpose:** resolve the same incident through a concrete change process.

B017 failed before publication. Review the connector or mapping correction, restore complete source inputs, recompute features and identify the new execution as B017-R1. Check row coverage, feature meaning, required fields, compatibility with M1, stored outputs and campaign consumption. The approved learned rule can remain M1 because the demonstrated fault was in the input path.

**Visual/build:** follow the repair path to validated release. Show candidate training as conditional on separate evidence, not as the inevitable next stage. Record authorization to resume; do not claim that we executed these checks on a real bank or that a particular corrected score resulted.

**Transition:** “Different kinds of change need different checks.” **Anchor:** personal notes §4; handoff §8; Bass bank workflow as context. Exact incident, identifiers and gates are our synthesis.

### 25. CI, CD, and CT need different evidence.

**Time:** 37:00–39:00. **Purpose:** distinguish automation responsibilities.

Continuous integration checks combined code changes, including the connector and preparation path. Continuous delivery keeps validated changes ready for a release decision; continuous deployment automatically releases changes satisfying configured gates. Continuous training repeatedly prepares and evaluates model candidates from suitable data. These activities can be connected without being identical.

**Visual/build:** use lanes converging on release evidence. A changed dataset, passed code test or trained model file does not by itself establish suitability for production. The policy specifies the evidence and approval needed for the actual compatible set. Predictive evaluation still requires appropriate outcomes.

**Transition:** “That evidence needs an inspectable identity.” **Anchor:** handoff §8; personal notes §4; supporting Kalinowski §§16.3–16.5; Bass §§14.1.2–14.1.5. The cited versioning, CI and deployment passages were freshly checked on PDF pages 469–474.

### 26. The release record binds evidence to a compatible set.

**Time:** 39:00–40:30. **Purpose:** make governance concrete without a product tour.

Read the illustrative release record by function: what changed, which versions belong together, which checks ran, who approved, and how to recover. Feature and code references identify preparation. M1 identifies the learned artifact. Configuration and execution time identify the scoring context. Check results and approval refer to that specific release, not to a floating “latest” model.

**Visual/build:** reveal the record fields in those groups. Protected fingerprints can help identify bytes but do not establish trust if the expected digest and approval record are themselves unprotected. No displayed identifiers are claimed as captured tool output.

**Transition:** “Follow those links from the release to Ana's prediction.” **Anchor:** personal notes §4; handoff §8; Bass registry/lineage, PDF 442–443.

### 27. Reconstruct the score and the decision.

**Time:** 40:30–42:00. **Purpose:** connect traceability, debugging and auditability.

Start with Ana's prediction identifier. Retrieve the feature definition and protected input snapshot or sufficient historical reference, M1, scoring configuration, cutoff, target window and campaign-policy version. The action record may say no contact. The later outcome reference remains pending until available. Reconstructing a score and reconstructing a policy action are related but different tasks.

**Visual/build:** reveal one protected reference at a time. Log identifiers and necessary context rather than scattering full customer histories through every component. Exercise retrieval: a broken reference can make an otherwise detailed record unusable. Do not attach an invented post-repair score to B017-R1.

**Transition:** “A release record is useful in recovery only if its recovery path works.” **Anchor:** personal notes §§4, 6; handoff §8; Bass §14.2.2.

### 28. Recovery restores a compatible path.

**Time:** 42:00–44:00. **Purpose:** close the repair loop and make rollback limits clear.

Identify what a rollback restores: preparation, configuration, model references, batch outputs and downstream handling may all matter. Reverting the unchanged M1 cannot restore the missing CRM field. A fallback is a previously defined alternative, such as pausing automation or a validated manual process; old scores are not automatically suitable simply because they are available.

**Visual/build:** before release, rehearse the compatible recovery; during release, control exposure; afterward, check the repaired operational path and later evaluate mature outcomes. Already delivered contacts cannot be undone by a deployment rollback.

**Handoff to the joint section:** “Who can make these changes, and which customer information should each participant see?” **Anchor:** handoff §8; personal notes §4; Breck recovery support in source-review.md.

## Simon + Matheus — security and privacy

### 29. What if the source change were deliberate?

**Time:** 44:00–45:45. **Suggested lead:** Simon. **Purpose:** locate threats using actual access assumptions.

Explicitly open a hypothetical branch: suppose a compromised writer alters engagement records. Manipulating records that later enter learning creates a poisoning opportunity. Manipulating features consumed by an already trained model concerns prediction-time inputs. Privacy inference concerns learning sensitive information through outputs or model access. These are different mechanisms with different prerequisites.

**Visual/build:** locate each mechanism on the same architecture. An internal batch job does not automatically expose a public query API. A missingness alert cannot establish malicious intent; combine source history and access evidence. Keep the original CRM migration as an accidental fault unless further evidence says otherwise.

**Transition:** “The first question is who can reach which resource.” **Anchor:** personal notes §5; handoff §9; Bass Chapters 9 and 14; recorded NIST predictive-ML taxonomy.

### 30. Permissions follow responsibility boundaries.

**Time:** 45:45–47:30. **Suggested lead:** Matheus. **Purpose:** make least privilege specific.

Read the matrix by identity and operation. A feature job reads authorized source data and writes prepared features. A trainer creates candidates. A release reviewer can promote an approved compatible set. The scorer reads approved artifacts and writes scores; the campaign reads a restricted approved view. Write access does not silently include promotion authority.

**Visual/build:** emphasize the permissions that would cross roles inappropriately: the trainer cannot approve itself, the campaign cannot rewrite training data, and source credentials cannot deploy a model. The matrix is abbreviated; evaluation-report access and operational exceptions would need explicit treatment in a real design.

**Transition:** “Those marks only matter if a mechanism enforces them.” **Anchor:** personal notes §5; handoff §9. The permission configuration is a proposed teaching design, not a bank's observed policy.

### 31. A boundary needs enforcement.

**Time:** 47:30–49:15. **Suggested lead:** Matheus. **Purpose:** distinguish identity, permission and input correctness.

The campaign presents a credential to read its approved score view. Authentication establishes the identity; authorization checks its requested operation on that resource. An allowed read returns only permitted fields. A write or unrestricted CRM read is denied without returning protected data. Record the decision and reason in restricted audit evidence without logging the secret credential.

**Visual/build:** step through allowed and denied requests, showing where the prohibited path stops. Network reachability, encryption and input validation serve different purposes. Even an authorized writer can submit bad or malicious values. A stolen campaign credential can misuse genuinely assigned reads, so field limits and investigation remain relevant.

**Transition:** “Permission also leaves a question about the purpose and scope of data use.” **Anchor:** personal notes §5; recorded NIST SP 800-207 §3. Logical access functions do not require separate microservices.

### 32. Expose what the role needs.

**Time:** 49:15–51:00. **Suggested leads:** Simon and Matheus. **Purpose:** follow privacy across the system.

The campaign needs enough information to apply its permitted action policy. An authorized investigator may need protected inputs, versions and action history. Those are different views with different retention needs. Features, model outputs, explanations and logs can remain sensitive even when direct identifiers are replaced.

**Visual/build:** contrast permitted fields for each audience. Tokens do not guarantee anonymity; synthetic records can leak; distributed training does not automatically make updates private. If mentioning differential privacy, ask what contribution is protected and how repeated releases are accounted for. Do not present it as an implemented bank guarantee.

**Handoff:** “We have proposed safeguards. What evidence would show that the design actually meets its quality concerns?” **Anchor:** personal notes §6; handoff §9; Bass §14.2.1; recorded NIST privacy guidance. Keep legal requirements out of unsupported universal claims.

## Quality review — owner TBD

### 33. Concern → control → evidence.

**Time:** 51:00–52:30. **Purpose:** use selected checklist items to review what the audience has seen.

For SMN3, connect input-distribution monitoring to a dated cohort comparison and investigation record. For SA1, connect recovery to a rehearsed compatible restoration and verified outputs. For SS5, connect cyberattack defense to enforced source/release permissions and evidence that prohibited operations are rejected. A normal data-validation check alone does not demonstrate that security defenses are effective.

**Visual/build:** reveal each concern with its bank control and evidence. These are selected prompts from a broader checklist, not certification or a claim of full checklist coverage. The published table was checked directly; its separately catalogued corrigendum remains unread.

**Transition:** “Prediction usefulness and operational performance also need distinct evidence.” **Anchor:** Bucaioni, Kazman and Pelliccione, Table 1, PDF 6–7, DOI 10.1016/j.jss.2025.112612; handoff §10.

### 34. Quality includes the prediction and the service.

**Time:** 52:30–54:15. **Purpose:** connect metrics to the bank's decisions.

Use the notes' invented mature cohort if needed: 12 of 20 flagged customers leave, giving 60% precision; 12 of 30 actual churners were flagged, giving 40% recall. Those answer different questions. Calibration asks whether probability estimates agree with observed frequencies in comparable groups; the notes' group near 0.70 with 0.40 observed churn illustrates overprediction for that group only.

**Visual/build:** separate these later model checks from the immediate batch deadline, coverage and operating cost. A more complex model should justify its practical burden. None of these metrics proves a retention offer caused someone to stay.

**Transition:** “The average can also hide which customers lose out.” **Anchor:** personal notes §3; Kalinowski §13.4; Bass PDF 432–433, with the stronger fairness claims in the book treated cautiously.

### 35. A better average can conceal a worse group outcome.

**Time:** 54:15–56:00. **Purpose:** make group evaluation and its limits tangible.

The notes' fictional comparison improves overall recall from 40% with M1 to 50% with M2, while group A falls from 40% to 30%. The tiny group counts demonstrate the arithmetic, not a statistically reliable production verdict. If using the notes' 35% per-group gate, label it an invented teaching rule. Rejecting M2 does not certify that M1 is suitable forever.

**Visual/build:** show the overall result, then the group result. Distinguish prediction errors from access to retention offers and treatment outcomes. SHAP or LIME can support investigation but cannot prove causality or fairness. **Handoff:** “What tools help retain the evidence behind these checks?” **Anchor:** personal notes §7; handoff §10; Bucaioni SS6 as a review prompt.

## Tools and close — owner TBD / all

### 36. Airflow makes execution visible.

**Time:** 56:00–57:30. **Purpose:** connect orchestration to an actual responsibility.

Introduce the display as a prepared illustrative workflow, not a captured Airflow run. Required input validation is upstream of scoring and campaign export. When validation fails, the dependent work must not proceed. The record shows execution, timing and failure context so operators and source owners can locate the affected batch.

**Visual/build:** reveal validation failure followed by dependent tasks not running. Exact Airflow state names depend on DAG configuration; simplified labels communicate the dependency outcome. Orchestration supports the configured checks. A completed run does not prove future churn accuracy, fairness or privacy.

**Transition:** “Execution evidence is useful alongside model and data evidence.” **Anchor:** Bass §14.1.2, PDF 440; handoff §11; illustrative dependencies from the team's design.

### 37. MLflow connects evidence; validation checks inputs.

**Time:** 57:30–58:45. **Purpose:** keep the showcase short and architectural.

Show a model artifact linked to its training run, data reference and evaluation metrics. A complementary validation report describes required feature checks and the affected batch. The release record links this evidence to the approved compatible versions and recovery reference. Reviewers use these links to assess a release; source owners investigate invalid inputs.

**Visual/build:** reveal model/run links, then the validation evidence, then their role in review. Every displayed identifier is illustrative. No single default tool installation supplies every data, security, release and privacy control. Keep model tracking, workflow orchestration and release authority distinguishable.

**Transition:** “Return to the customer whose prediction started the talk.” **Anchor:** Bass §§14.1.3–14.1.5, PDF 440–445; handoff §11.

### 38. Return to Ana: a usable prediction needs a system.

**Time:** 58:45–60:00. **Purpose:** finish the same story without manufacturing a result.

Ana's original illustrative score was 0.70. The CRM failure showed that usable predictions depend on compatible inputs, controlled change and appropriate action. We located an upstream fault, held B017, defined the boundaries it crossed, and explained how B017-R1 would be validated before use. We did not establish her eventual churn or the benefit of an offer.

**Visual/build:** return to the shared map and highlight those three responsibilities. Close the Day 2 bridge in one sentence: foundation models and agents still require operational controls, while their components and failure modes differ. Do not introduce the next week's architecture now.

**Closing line:** “A model supplies an estimate; architecture makes its use understandable, controlled and reviewable.” **Anchor:** group handoff §11; personal notes §§1, 4, 8; bank-case synthesis.

## Source and adaptation notes for rehearsal

The source-review and visual-source ledgers remain the detailed provenance records. Fresh checks during presentation preparation cover Bass's bank-case PDF 430–448; Kalinowski architecture/serving PDF 403–414 and design-pattern passages 433–437; selected Nazir decision passages within PDF 10–13; and the published Bucaioni Table 1 on PDF 6–7, including visual inspection of both table pages. Further passages extracted but not fully inspected should not be described as full-paper or whole-book reads.

The paired drift plots, alert numbers, policy thresholds, customer records, batch identifiers, permission matrix, rollout routing, version records and repair sequence are teaching constructions. The original chart script and visual-source ledger distinguish original coordinates from source-inspired layout. Keep those distinctions in captions and notes.

Bucaioni's separate corrigendum, DOI 10.1016/j.jss.2025.112743, has no attachment under the inspected Zotero item PR2VIDCJ and has not been read. Cite the inspected published Table 1 rather than claiming the correction has no effect.

Use the existing study notes' optional atlas for mathematical questions. If asked which statistic to use in production, explain that input type, representation, reference, sample size, seasonality, decision impact and alert policy matter; this presentation does not establish a universal monitoring threshold.

## Rehearsal protocol

Rehearse the handoffs with one person operating navigation. Let each speaker identify the same source, feature, model, batch and action names before combining sections. Ensure an arrow or build never implies automatic retraining or promotion. In the joint section, agree who speaks each sentence around the permission matrix and privacy views. Quality and tool ownership remain decisions for the group.

Use a complete static visual if motion is unavailable. An animation should let the presenter control reading order, not require racing the slide. Practice one full run against the section end times, then shorten repeated explanations before removing essential case transitions. Leave optional technical discussion until the prepared hour is complete.
