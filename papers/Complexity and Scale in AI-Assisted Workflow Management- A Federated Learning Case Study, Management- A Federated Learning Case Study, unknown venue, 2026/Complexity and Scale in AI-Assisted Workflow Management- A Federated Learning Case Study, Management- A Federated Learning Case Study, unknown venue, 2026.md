                                             Complexity and Scale in AI-Assisted Workflow
                                             Management: A Federated Learning Case Study
                                                            Komal Thareja∗ , Hamza Safri† , Rajiv Mayani† , Anirban Mandal∗ , Ewa Deelman†
                                                                          ∗ RENCI, University of North Carolina at Chapel Hill, NC, USA
                                                          † Information Sciences Institute, University of Southern California, Marina del Rey, CA, USA



                                           Abstract—Federated learning over medical images is a de-          and data staging. A comparable Pegasus FL workflow devel-
                                        manding workflow application. Each round fans out across             oped manually required an estimated 3 to 4 months, with most
                                        parallel client jobs and converges on an aggregation step that       of the effort devoted to workflow mechanics [5].
                                        feeds the next round. At scale this yields 101 sub-workflows and
                                        2,679 jobs on GPUs at four sites, which takes an expert months to       Automating workflow authoring is therefore attractive.
arXiv:2606.18425v2 [cs.SE] 8 Sep 2026




                                        build, mostly on workflow mechanics rather than science. We ask      Prior approaches include semantic planning systems such
                                        how far AI assistance can automate such workflows. An LLM            as Wings [6], which provide correctness guarantees but re-
                                        agent, grounded in a released plugin of Pegasus-specific skills,     quire manually engineered representations, and more recent
                                        first produces a reviewable specification of checkable constraints   LLM-based approaches that generate workflows from natural-
                                        and acceptance criteria, then generates the executable workflow.
                                        A validation loop repairs runtime failures, checks code against      language descriptions [7], [8]. These approaches show that
                                        those constraints, and regenerates the implementation from the       user intent can be translated into executable pipelines, but
                                        specification alone. We evaluate three LLM agents, report end-       direct code generation leaves the intended design implicit
                                        to-end runs on the FABRIC testbed, and show how conformance          in the implementation, so it is hard to review the design
                                        checking against the specification caught three silent errors that   before execution, check the code against its requirements, or
                                        failure-driven debugging missed, including one that trained 1,700
                                        jobs on random tensors.                                              regenerate the implementation independently of the original
                                           Index Terms—scientific workflows, workflow management,            interaction.
                                        large language models, medical imaging, federated learning              In this work, we investigate a specification-driven ap-
                                                                                                             proach to AI-assisted scientific workflow management, and
                                                                I. I NTRODUCTION                             demonstrate how AI assistance can automate the construction,
                                           Scientific workflows provide a structured means of coordi-        execution and debugging of complex hierarchical workflows
                                        nating computational tasks, data dependencies, and execution         (e.g. federated learning). The LLM first translates user intent
                                        resources in complex scientific applications. As applications        into a structured, reviewable specification containing workflow
                                        become increasingly distributed and data intensive, translating      constraints and acceptance criteria and then generates the ex-
                                        scientific requirements into executable workflows requires ex-       ecutable workflow. Workflow-specific knowledge is provided
                                        pertise beyond the application itself, including task decomposi-     through pegasus-ai, a reusable plugin of Pegasus-specific
                                        tion, data movement, dependency management, and execution            skills [9]. The specification remains an independent artifact
                                        across heterogeneous resources.                                      that can subsequently be used for conformance checking and
                                           These challenges arise naturally in federated learning (FL),      regeneration, while a validation loop combines these checks
                                        where distributed computation must be coordinated across             with failure-driven debugging during execution.
                                        multiple data holders and successive training rounds. FL                The paper makes three contributions: (1) an end-to-end
                                        trains a shared model without centralizing data [1], making          study of AI-assisted composition and management of a com-
                                        it particularly relevant to domains such as medical imaging.         plex scientific workflow, from natural-language intent through
                                        Its computation is both parallel and iterative: clients train        specification, code generation, debugging, validation, and ex-
                                        locally within each round, their updates are aggregated, and         ecution at scale, (2) an evaluation of multiple LLM coding
                                        the resulting global model becomes the input to the next round.      agents for workflow construction and debugging, compared
                                        Repeating this process across clients, datasets, and execution       with a previously reported expert implementation and (3)
                                        sites creates a hierarchical workflow with dependencies that         an analysis of defects encountered during development that
                                        extend across rounds.                                                distinguishes failures accessible to runtime debugging from
                                           Workflow management systems (WMSs) such as Pega-                  silent correctness violations, motivating the combination of
                                        sus [2], Nextflow [3], and Galaxy [4] provide planning, data         failure-driven debugging and specification-based conformance
                                        staging, orchestration, provenance, and fault recovery, but          checking for complex workflows.
                                        constructing such workflows still requires substantial system-
                                        specific expertise. For this application, the complexity lies less     II. F EDERATED L EARNING W ORKFLOW C OMPLEXITY
                                        in the learning algorithm than in workflow mechanics, includ-          Federated learning combines distributed model training with
                                        ing sub-workflow composition, cross-round data dependencies,         an iterative computational structure that becomes increasingly
                                        catalog propagation, cleanup policies, container management,         complex as the number of clients and training rounds grows.



                                        SC26 Workshops, November 15-20, 2026, Chicago, Illinois, USA
                                        979-8-3195-1221-5/26/$31.00 ©2026 IEEE
                                                                       that separate user intent from implementation (Fig. 2). A
                                                                       prompt and dataset description captures high-level intent,
                                                                       constraints, and experimental objectives without requiring
                                                                       knowledge of the underlying workflow system. From it the
                                                                       system generates a structured specification that formalizes
                                                                       the design as a human-readable artifact the user validates and
                                                                       refines before anything is executed. Once the specification
                                                                       is approved, code generation produces directly deployable
                                                                       artifacts: workflow definitions, wrapper scripts, configuration
                                                                       files, and container specifications. Workflow-specific skills
                                                                       ground the model in reusable workflow knowledge and tem-
Fig. 1: One federated learning round: parallel client training,        plates throughout, so that outputs conform to the requirements
followed by aggregation into the global model for the next             of the target execution environment.
round.                                                                    Each participant has an explicit role. The user provides
                                                                       the prompt and dataset description, reviews and approves the
Within each round (Fig. 1), a selection step determines the par-
                                                                       specification, and decides among design alternatives that the
ticipating clients, which train locally in parallel on their private
                                                                       system surfaces, such as the orchestration strategies of Sec-
data shards. An aggregation job then combines the resulting
                                                                       tion V-A. The LLM interprets the prompt, synthesizes the spec-
model updates using Federated Averaging (FedAvg) [1], and
                                                                       ification, and generates the artifacts. The skills are authored by
an evaluation job assesses the new global model. A complete
                                                                       workflow-system developers and supply the Pegasus-specific
study repeats this process for T rounds over each dataset,
                                                                       knowledge that grounds the model. Pegasus plans and orches-
with data preparation at the beginning and centralized baseline
                                                                       trates the workflow and HTCondor executes its jobs, and the
training and figure generation at the end.
                                                                       LLM modifies neither.
   Three properties make this application challenging to ex-
                                                                          The methodology is tool-agnostic, assuming only an LLM
press as a scientific workflow. First, the graph is iterative: its
                                                                       agent capable of invoking structured skills. Claude Code with
size grows with the number of rounds, while the same round
                                                                       the pegasus-ai plugin is the reference implementation
structure is repeatedly instantiated. Second, it is hierarchical,
                                                                       here, and Section V evaluates it against agents that receive
because a round is itself a natural unit of composition rather
                                                                       the same workflow knowledge as unstructured context.
than an individual job. Third, it is dependency-intensive across
these levels, since the global model produced within one
round is consumed by the next. In Pegasus, this structure
maps naturally to the SubWorkflow construct (sub-workflow
hereafter), where each round is represented as a self-contained
workflow composed into a parent graph and planned when
the parent reaches it. This organization provides per-round
fault tolerance, provenance, and cleanup, but relies on ad-
vanced workflow-management mechanisms that non-expert
users rarely employ.
   The difficulty of constructing this workflow lies largely
in the mechanics surrounding this structure rather than in
the learning algorithm itself. A sub-workflow planned at
runtime requires its replica, transformation, and site catalogs
to be propagated correctly. Cleanup policies must preserve the                   Fig. 2: AI-assisted workflow management.
global model checkpoint required by the subsequent round,
and client shards must remain registered so that they are              B. Workflow-Specific Plugins and Skills
available when the next round is planned. Large training
                                                                          We organize workflow knowledge into plugins, packaged
containers must be reused rather than repeatedly staged, while
                                                                       extensions that supply the language model with workflow-
concurrent experimental configurations must be namespaced to
                                                                       specific material, and within each plugin into skills, each
prevent results from being overwritten. Each of these issues
                                                                       implementing one workflow-oriented operation. A skill is a
occurred during the development of the workflow and is
                                                                       self-contained, agent-agnostic slash command bundling in-
examined further in Section V-D.
                                                                       structions with the reference material that grounds them:
       III. AI-A SSISTED W ORKFLOW M ANAGEMENT                         documentation, example workflows, validation checklists, and
                                                                       reusable templates. The model invokes only the skill the
A. Overview of AI-Assisted Workflow Generation                         current step needs, which holds generation to Pegasus-specific
  We propose a specification-driven approach to AI-assisted            requirements such as correct API usage, data staging patterns,
workflow generation, decomposed into three explicit stages             and container configuration.
   The plugin we built for this work is pegasus-ai [9],              To make the specification checkable rather than purely
published in a marketplace of such plugins for scientific work-   descriptive, it distinguishes three kinds of validation content.
flow development. Its eight skills group into three functional    Constraints state properties the implementation must satisfy,
categories: workflow construction, validation & recovery, and     such as the round structure of the DAG, the staging of the
reuse & support. Any agentic coding tool supporting the           global model between rounds, and the resource limits of
skill and plugin interface, such as Claude Code, Codex, or        the target execution sites. Non-constraints record degrees of
opencode, can load it and invoke the same skills.                 freedom deliberately left to the implementation, such as the
      a) Workflow construction: The /pegasus-scaffold             naming of intermediate files or the internal structure of wrap-
skill generates a complete workflow project from a high-          per scripts, so that the review focuses on decisions that matter
level pipeline description, including the workflow gener-         and later changes to these aspects do not require re-approval.
ator, wrapper scripts, Dockerfile, and site catalogs. The         Expected outcomes define acceptance criteria for the generated
/pegasus-wrapper skill creates wrapper scripts that in-           code, including the artifacts each stage must produce, the
terface Pegasus job execution with computational tools. The       smoke-test configuration exercised before full-scale runs, and
/pegasus-dockerfile skill generates container defini-             the metrics and figures anticipated by the experiment plan.
tions with the required software dependencies for reproducible    User review therefore evaluates concrete, testable statements
execution.                                                        rather than prose intent, and the same statements later serve
      b) Validation and recovery: The /pegasus-debug              as the reference for automated debugging (Section V-D).
skill drives the diagnose, fix, and re-run loop described in         For the federated learning case study in this paper, the
Section III-D, while the /pegasus-review skill inspects           generated specification is a fourteen-section, ∼7,000-word
workflow code for common anti-patterns and correctness is-        document (Table I). Validation is performed through user
sues.                                                             review before any code is generated: the user checks the
      c) Reuse and support: The /pegasus-convert                  stated constraints and expected outcomes, confirms the DAG
skill converts workflows between supported formats. The           structure, selects among the surfaced orchestration options,
/pegasus-help skill provides context-aware Pegasus doc-           and approves the experiment plan. The specification remains
umentation and guidance. The /kiso skill generates experi-        a living artifact: its final two sections record implementation
ment configurations for the Kiso [10] experiment management       status and the fixes applied during debugging (Section V-D),
platform.                                                         so the persisted document reflects the workflow as executed.
      d) How the plugin was developed: The pegasus-ai                TABLE I: Section outline of the generated specification.
plugin was distilled from building fourteen real Pegasus work-    1. Project Overview                     8. Experiment Plan
flows [11], [12] across varied workflows and input modalities,    2. Datasets                             9. Directory Structure
                                                                  3. Federated Learning Design            10. References
taking roughly 190 prompts over about 15 developer-days.          4. Pegasus Workflow Architecture        11. Design Decisions (Resolved)
                                                                  5. Software Stack & Containers          12. Setup & Dependencies
Whenever a prompt recurred or a Pegasus-specific pitfall          6. Catalogs                             13. Implementation Status
reappeared, it became a reusable skill carrying the documen-      7. Execution Environment                14. Key Fixes Applied
tation, examples, and validation checklists needed to avoid it       The specification is intentionally a design-level artifact
next time. That authoring cost is amortized over every later      rather than a formal workflow language. Only after validation
workflow and is separate from the per-workflow effort reported    does the system generate the executable artifacts. Where direct
in Section V. Because the skills capture Pegasus mechanics        LLM interaction leaves the design implicit in whatever code
rather than domain logic, new scientific domains are usually      the last prompt happened to produce, this separation makes
handled by existing skills, and only a new capability such as     the design explicit, reviewable, and auditable.
targeting a different workflow system would require a new
one.                                                              D. Execution, Debugging, and Validation
                                                                     Generated artifacts are submitted to Pegasus, which con-
C. Specification-Driven Development
                                                                  structs the workflow DAG, manages data staging, coordinates
   Our approach uses a specification-driven development           job execution, and monitors progress. Execution is delegated
methodology [13] for workflow generation. Rather than di-         to HTCondor [14], which handles resource allocation, job
rectly synthesizing executable code from user input, the system   scheduling, and distributed execution with built-in fault tol-
first produces a structured, human-readable specification that    erance. Both run on the submit node alongside the coding
captures the workflow design (data dependencies, execution        agent, and neither is modified by it (Fig. 2).
stages, and configuration parameters), together with a vali-         The system includes an AI debugging capability, delivered
dation plan (experiments, metrics, and expected figures), the     by the /pegasus-debug skill and executed by the host
design decisions resolved with their trade-offs, and an im-       coding agent, that handles failure diagnosis and recovery
plementation roadmap. This intermediate artifact is reviewed      during workflow execution. Pegasus and HTCondor generate
before implementation, and its experiment plan and smoke-         logs and runtime metadata as workflows execute. The skill
test configuration serve as acceptance checks for the generated   interprets those traces and matches them to known failure
code.                                                             patterns such as file staging errors, container issues, resource
misconfiguration, dependency conflicts, and incorrect wrapper                  TABLE II: Experimental configurations.
scripts. It then acts on its own diagnosis: the host agent          Exp        Alg.         R         K         E        Focus
edits the affected workflow definitions, wrapper scripts, and       E1         FedAvg       50        10        2        Baseline
                                                                    E3         FedAvg       50         5        2        Scalability
configuration files and re-submits the affected jobs or sub-        E4         FedAvg       10        10        5        Communication
workflows, forming a closed-loop recovery mechanism in
which failures are detected, diagnosed, and corrected during        bytes transferred scale with K × T and E4 moves one fifth of
execution.                                                          E1’s bytes. Communication efficiency is the accuracy reached
   Debugging alone is reactive, so it sits inside a wider           for that cost. Numbering follows the released artifact [17],
validation loop that plays the role continuous integration plays    which defines further configurations outside the scope of this
in software development, adapted to an artifact that cannot         evaluation.
simply be unit tested because one run of it occupies nine GPUs         Experiments ran on a distributed HTCondor pool on the
for a day. The loop has three parts, applied at different points    FABRIC testbed [18] with four GPU-equipped worker nodes
in the lifecycle. The debugging skill acts during execution and     across sites, HAWI (3 GPUs), MAX-1 (2), MAX-2 (2), and
repairs what fails. A conformance pass acts on the code before      NCSA (2), totaling 9 GPUs. Jobs ran in Docker containers
submission and checks it against the constraints the specifica-     using CondorIO for data staging, each training job requesting
tion states, which requires no execution at all. A regeneration     1 GPU, 4 CPU cores, and 15 GB memory.
test acts on the specification and rebuilds the implementation
from it alone, which is what keeps the specification honest as      C. Evaluation Metrics
the code changes underneath it. Section V reports all three.           Workflow generation is assessed along four dimensions.
Only the first is driven by failure, and Section V-D shows that     Execution success measures completion without runtime er-
this distinction, rather than the sophistication of any one part,   rors. Structural quality measures whether the generated code
determines which defects are reachable at all.                      satisfies the constraints stated in the specification. Repro-
                   IV. E VALUATION S ETUP                           ducibility measures whether the workflow can be regenerated
                                                                    from the persisted specification alone. Development effort
A. Datasets                                                         measures the iterations and manual interventions needed to
   TCIA [15] provides 4,144 3D CT/MRI lung volumes across           obtain a working workflow. Structural quality is measured
multiple collections. One representative slice per imaging          by a conformance pass in which ten independent reviewer
series is extracted, resized to 224 × 224, and distributed across   sessions each receive one copy of the workflow together with
K clients. The task is binary classification for lung pathology     the specification, with no access to the development history
present or absent. Labels are assigned at the collection level      and no pointer to any particular constraint, and return a
from collection metadata, and the train/test split is performed     verdict of pass, fail or unclear for each of the eleven stated
at the series level after pooling all collections.                  constraints along with the file and line supporting it. A verdict
   NIH ChestX-ray [16] consists of 50,000 2D chest X-rays           of fail counts as a false positive unless the violation can be
resized to 224×224, partitioned by patient ID across K clients,     independently confirmed in the code.
with binary classification (“No Finding” vs. pathology). The           Federated learning performance is assessed with accuracy
held-out test set is reserved at the patient level, so no patient   and F1 score, only to confirm that the workflows produce
contributes to both training and evaluation.                        interpretable machine learning results.
B. Experimental Setup
                                                                                             V. R ESULTS
   The experimental workflows are generated using the ap-
proach described in Section III-D. All experiments use a            A. Workflow Design and Generation
ResNet-18 model with an ImageNet-pretrained backbone,                  During the specification phase, the LLM presented two
batch size 32, learning rate 0.001, and stochastic gradient         orchestration strategies for the iterative FL rounds: (1) an
descent with momentum 0.9 and weight decay 10−4 .                   ensemble-manager pattern, in which a single top-level work-
   We report three configurations that explore scalability and      flow re-invokes itself across rounds using an external co-
communication efficiency (Table II). All K clients participate      ordinator, and (2) a sub-workflow pattern, in which each
in every round (client fraction C = 1). The per-round selection     round is encapsulated as a Pegasus sub-workflow with explicit
step is seeded by the round number, so a re-planned or rescued      data dependencies between rounds. The ensemble-manager ap-
round selects the same clients.                                     proach offers lower scheduling overhead and supports dynamic
   E1 is the FedAvg reference against which the others vary a       runtime decisions such as early stopping, but introduces a
single factor. E3 halves the client count, which increases the      single point of failure and coarsens fault tolerance and prove-
data each client holds while reducing aggregation diversity.        nance. The sub-workflow approach costs additional per-round
E4 trades rounds for local epochs. Communication cost here          scheduling latency and buys back the per-round guarantees
is the number of full-model exchanges between clients and           of Section II. The user selected the sub-workflow approach,
aggregator. With full participation each round moves the global     as these benefits outweigh the overhead for long-running FL
model to and from every client (about 45 MB per direction), so      workflows where GPU computation dominates execution time.
           TABLE III: Workflow generation comparison.                         TABLE IV: Development effort comparison. Manual figures
                            Claude Code                Kimi
                                                                              are estimates.
Metric                                     Codex                   Manual
                            + pegasus-ai             (Opencode)
                                                                                                        Claude Code                  Kimi
                                                                              Metric                                    Codex                     Manual
Files generated                 22           33         15           n/a                                + pegasus-ai               (Opencode)
Specification                   Yes          Yes        Yes          No
Design guidance                  5            0          0           n/a      Sessions                       2             9           4              n/a
Orchestration opts.             Yes          No         No           Yes      Prompts, construction          7             7          12              n/a
                                                                              Prompts, refine & debug       45            42          51              n/a
Orchestration                 Sub-wf       Sub-wf†    Sub-wf‡     Ensemble∗   Output tokens               ∼109K         ∼237K       ∼178K             n/a
Sub-workflow support          Initial       Later†     Later‡        Yes      Estimated cost (USD)       $10 to 15     $15 to 20     n/r‡             n/a
CondorIO staging              Initial       Later†     Later‡        Yes      Development time            2 days        3 weeks     7 days      3 to 4 months
Parallel datasets             Initial       Later†     Initial       Yes      Production-ready              Yes           Yes       Partial†         Yes
GPU containers                Initial       Later†    Initial§       Yes      † Generates a valid DAG but not yet executed on distributed infrastructure.
PyTorch models                Initial       Later†     Initial       Yes      ‡ Not recorded. Kimi ran through a gateway that reports no per-call cost.
FedProx support               Initial       Later†     Initial       Yes
Staging resolved               Yes           Yes        No‡          Yes      surface design alternatives and enforce consistent patterns.
Reproducibility                High         Low         Low        Manual     Codex produced a simplified initial workflow [20] and needed
Sub-wf: sub-workflow. † Follow-up prompts required. ‡ Staging unresolved.     repeated follow-ups to add sub-workflows, data staging, par-
§ Fixed in later sessions. ∗ Preferred for large-scale workflows.
                                                                              allel dataset execution, and realistic models. Kimi, given the
   Figure 3 shows the resulting top-level workflow DAG for                    same documentation, required the most refinement [21] and
a single dataset branch. Data is downloaded and partitioned                   never resolved the sub-workflow staging conflict, oscillating
into client shards, after which T federated learning rounds                   between flat DAG and sub-workflow approaches across several
execute as sub-workflows, each implementing the fan-out/fan-                  debugging sessions.
in pattern shown in Fig. 1. A centralized baseline and result                    Claude also exposes orchestration alternatives before any
visualization complete the pipeline. The full workflow repli-                 code exists, which neither of the others does, and its speci-
cates this branch for each dataset, enabling parallel execution.              fication supports regeneration from a persisted artifact where
                                                                              they depend on replaying an interaction history (Table III).
                                                                                 We tested that regeneration claim rather than asserting it.
                                                                              The persisted specification alone was given to a fresh session
                                                                              with the plugin, in a working directory containing no file from
                                                                              the original implementation, and the criteria for equivalence
                                                                              were fixed before comparing. The regenerated workflow is
                                                                              structurally identical for the same configuration, with 15 top-
Fig. 3: Generated top-level DAG for one dataset branch. Each
                                                                              level jobs, 4 round sub-workflows, and 5 jobs per round in
round is a sub-workflow of the form in Fig. 1.
                                                                              the same fan-out and fan-in arrangement, differing only in
                                                                              generated file names, which the specification lists as free.
B. Workflow Generation Comparison                                             It satisfies the eleven stated constraints, cites seven of them
   To evaluate the effectiveness of AI-assisted workflow gen-                 by identifier in its own source, plans without error, and
eration, we compare four approaches: Claude Code with the                     reintroduces none of the nine defects recorded during the
pegasus-ai plugin, OpenAI Codex, Kimi K2.6 running                            original development. Seven passages cite the originating fix
under Opencode [19], and a manually implemented work-                         by number, so the sections recording status and applied fixes
flow by an expert in federated learning and Pegasus WMS                       are read rather than merely persisted.
(Table III). All three LLM systems had access to identical
documentation. Claude integrates it as structured skills invoked              C. Cost of AI-Assisted Development
during generation, whereas Codex and Kimi receive it as static                   Claude Code sessions used Claude Opus 4 ($15/M input,
context in the working directory.                                             $75/M output tokens), Codex sessions used OpenAI’s GPT-5.4
   The comparison metrics are defined as follows. Design guid-                model, and Kimi sessions used Kimi K2.6 via Opencode.
ance counts the design decisions explicitly surfaced for user                    Construction is the cheaper half for every agent, and the
approval before code generation, and orchestration options                    totals differ in where the remaining effort went rather than in
indicates whether alternative round-orchestration strategies                  its size. Codex spent its sessions incrementally adding features
were presented to the user. Staging resolved indicates whether                that Claude produced in its first, and at a comparable prompt
the tool produced a working data-staging configuration for                    count consumed more than twice Claude’s output tokens,
nested sub-workflows. Reproducibility is rated high when the                  because it repeatedly regenerated its monolithic workflow
workflow can be regenerated from persisted artifacts (the                     generator. Kimi’s effort was concentrated rather than spread,
specification) and low when regeneration depends on replaying                 with a single later session consuming 51 of its 63 prompts on
a prompt history.                                                             Pegasus-specific issues such as sub-workflow file registration
   All three produced functional Pegasus workflows but differ                 and staging policy conflicts, which it never resolved. Refine-
in design completeness, interaction effort, and reproducibility.              ment and debugging dominated Claude’s effort as well, at 45
Claude Code produced a modular, feature-complete work-                        of 52 prompts, though from a far lower base and against a
flow [17] in a single session, guided by structured skills that               workflow that already ran.
   Every LLM-assisted approach costs negligibly little against       TABLE V: The nine defects by runtime evidence. Statically
the GPU resources the experiments required, nine GPUs for            visible counts evidence in the generated source before submis-
multiple days. In Table IV, production-ready means the gener-        sion.
ated workflow executed end to end on the pool of Section IV,         Runtime evidence     Defects       Debug loop       Statically visible
and the manual figure is the prior-work estimate cited in the        A job failed            6            reaches         4 full, 2 partial
                                                                     Nothing failed          3          cannot reach      3 full, 0 partial
introduction.
                                                                     Total                   9                            7 full, 2 partial

D. AI Debugging Skill                                                      b) Worked example: disk exhaustion: One of the six
   Across the runs the /pegasus-debug skill resolved fail-           failures shows the debugging loop end to end, and it also
ures spanning Pegasus configuration, HTCondor scheduling,            shows why a workflow failure is not the same problem as
Docker containerization, and filesystem capacity. The loop of        a program failure. Midway through a fifty round run, training
Section III-D ran autonomously throughout, without per-fix           jobs began failing on workers whose scratch space had filled.
human approval, and human involvement was limited to post-           No single layer of the system explains this. The job logs say
hoc review of the applied changes.                                   only that training died. The cause lies in how the planner
   What it resolved ranged across all four of those layers. Miss-    staged each round, not in anything a job did. The symptom
ing cleanup let intermediate files accumulate across rounds          appears on a worker machine that neither the logs nor the
until in-place cleanup was enabled. Experiment collisions oc-        planner names. The agent read across all three layers and
curred when concurrent experiments overwrote shared output           found the mechanism: every round’s sub-workflow was staging
paths, fixed by per-experiment namespacing. A model config-          its own copy of the multi-gigabyte training container, so disk
uration error, a mismatch between model output dimensions            use on each worker grew with the round count and crossed
and class-weight computation, failed training jobs until the loss    the limit partway through the run. The correction is a single
configuration was corrected. Missing dependencies, undeclared        property on the container definition, which tells workers to pull
script inputs, were added to the workflow definition.                the image once and reuse their local cache. The agent applied
                                                                     it to the workflow generator, re-planned, and re-submitted
     a) What the errors have in common: Rather than count
                                                                     the affected sub-workflows, which then completed. No human
classes, we classified every change the specification records
                                                                     approved any step.
as applied during development, which separates nine genuine
defects from five features and design changes. We organize              The episode also shows what the specification adds to the
them not by the subsystem they belong to but by whether              repair. The property is now recorded there as a constraint, so it
the runtime produced any evidence to diagnose (Table V).             can be checked before submission, and a regenerated workflow
Six of the nine produced such evidence: a job failed, and the        carries it by construction rather than by anyone’s memory of
exit codes, logs, and held-job records that a debugging loop         the incident.
consumes were all present. The other three left no trace at all.           c) A defect that produced no failure: One of the nine de-
The workflow ran to completion, every job exited zero and            fects was found only after the experiments had been reported.
wrote its declared outputs, and the results were nonetheless         The client training script read its data shard from a directory
wrong.                                                               whose name did not match the one the partitioning job wrote.
   This division comes from the execution logs rather than           The dataset class therefore found no images and substituted
from our judgment, and it decides what any failure-driven            random tensors, so every training job trained on noise. Counted
method can reach. A debugging loop covers the first six              from the Kickstart records, this affected all 1,700 training jobs
by construction and cannot reach the other three. What the           in the three reported configurations, and 3,700 across every
three silent defects share is a common shape rather than a           configuration run during development. Evaluation and the cen-
common subsystem. In each case the workflow did exactly              tralized baselines read real data, because their paths happened
what it had been told, and what it had been told was wrong:          to match. The reported federated accuracies therefore came
a shard was read from a directory the partitioning job never         from noise-trained models evaluated on a real test set, which is
wrote, an algorithm parameter never reached the trainer, and         why they sat near the majority-class rate while the centralized
an output path was shared by concurrent configurations. The          baselines did not.
picture reverses when we ask what was visible in the generated          The metrics these jobs produced were low but unremarkable
source. All three silent defects were fully visible there before     for federated learning on heterogeneous medical images, so
submission, whereas two of the six that failed appeared only as      nothing looked wrong and the failure-driven loop had nothing
anti-patterns whose trigger depends on worker disk capacity or       to act on. The defect was found instead by a conformance
on the class distribution of a shard. Static checking is therefore   pass, in which ten independent reviewers, given only the
most reliable exactly where the runtime is blind. This result        specification and the code, judged the implementation against
bounds what a pre-submission check could reach. It does not          the constraints of Section III-C. All ten flagged the constraint
measure what a particular checker finds, because the false           forbidding synthetic-data substitution, and four of them in-
positive rate of such a pass is not evaluated here. The per-         dependently identified the directory mismatch as the reason
defect classification is released with the workflow [17].            the forbidden path was always taken. When the pass was
repeated on the fixed code, every verdict it returned could be           TABLE VII: Structure and execution of the corrected runs.
confirmed in the source, and it surfaced three further genuine           Occ. is the fraction of a median round’s wall time with a job
violations of stated constraints. On a single codebase this is           executing.
an observation rather than a measured false-positive rate.                      Configuration        FL Structure                 Execution
   Two qualifications apply. First, the constraint in question           Exp   K     T      E    Train   Agg        Eval   Jobs   Wall (h)    Occ.
names the forbidden construct explicitly, so the reviewers were          E1    10   50      2     1000   100         4     2679     24.3      12.8%
in effect told what to look for. The result is evidence that             E3     5   50      2      500   100         4     2179     30.1       8.0%
                                                                         E4    10   10      5      200    20         4      559      4.6      27.9%
checking a written constraint is what mattered, not evidence
of unaided discovery. The constraint had been written weeks                  The job-level provenance records show where the remaining
earlier and changed nothing until it was checked. Second,                time goes. Within a median E1 round of 1,601 seconds, at least
the reviewers were ten sessions of a single model, so their              one job is executing for 204 seconds and DAGMan startup and
agreement is less independent than the count suggests. Only              teardown account for 13. The remainder is dominated by data
six of the nine defects recorded during development fall under           movement rather than by orchestration. Under CondorIO every
a stated constraint at all, which bounds what this form of               job receives its inputs afresh, so a median client training job
checking can reach.                                                      executes for 17.7 seconds while a further 134 seconds of its
      d) LLM vs. user vs. expert: A non-expert user typically            slot is spent outside process execution, during which HTCon-
builds a sequential pipeline with predefined rounds and explicit         dor moves 75 MB in and 45 MB out. Jobs that receive no large
job definitions and no advanced orchestration. An expert                 inputs show no comparable gap, which is what attributes it to
judges the generated workflow structurally correct, though               transfer rather than to generic slot overhead. A median training
FL-specific refinements such as early stopping or Ensemble               job also waits 361 seconds between submission and execution,
Manager orchestration [5] are absent.                                    because a round requests ten GPUs per dataset branch from
                                                                         a pool of nine. Each round moves about 2.6 GB, and a fifty
E. Federated Learning Performance
                                                                         round experiment roughly 260 GB, largely because the same
   Model quality is not a contribution of this work, and these           client shards and global model are re-staged on every round.
results only confirm that the generated workflows execute                    Round occupancy therefore tracks the amount of computa-
correctly. They are re-runs after the one line fix for the silent        tion a round contains rather than its size. E4, with five local
data-path defect of Section V-D, which invalidated an earlier            epochs per round, reaches 27.9% against 12.8% for E1 and
version of them.                                                         8.0% for E3. Expressing each round as a sub-workflow costs
   On the corrected runs, federated learning approaches cen-             little in itself, and the case for doing so strengthens as per-
tralized training on both datasets (Table VI). Convergence is            round computation grows relative to the fixed cost of staging
rapid, with TCIA passing 90% by round four and plateauing                its inputs. All three corrected configurations completed without
near 93% by round twenty. Reducing the client count (E3)                 job-level retries and without DAG-level rescues.
narrows the gap to under a point on TCIA and closes it on
NIH. Reducing rounds while raising local epochs (E4) matches                                    VI. R ELATED W ORK
the fifty round baseline in a fifth of the rounds and 4.6 hours
instead of 24.3, at one fifth of the model exchanges. These                 Several systems generate workflows from natural-language
numbers match the expected behaviour of FedAvg on naturally              input. Zeng et al. [7] use structured prompting and API
partitioned data rather than a heterogeneity penalty.                    grounding, and bioinformatics studies show similar applica-
TABLE VI: Final-round accuracy vs. the centralized baseline,             tions in Galaxy and Nextflow [22]. Zhang et al. [8] model
percent.                                                                 generation as a search over tool graphs, which is not tailored to
                      TCIA                      NIH ChestX-ray
                                                                         DAG-based scientific workflows and lacks WMS integration,
Exp       Federated          Centralized   Federated       Centralized
                                                                         and Balis et al. [23] combine intent extraction with determinis-
                                                                         tic DAG construction but target HyperFlow and do not address
E1          93.6                95.8         66.1                67.4
E3          95.3                95.9         66.8                66.7    distributed orchestration. None of these combines workflow
E4          94.2                95.1         67.6                66.3    synthesis with execution in a system such as Pegasus.
                                                                            On the debugging side, code-generation models such as
F. Workflow Execution Statistics                                         Codex [24], multi-agent frameworks such as AutoGen [25],
   The fifty round experiments consist of 101 sub-workflows,             and self-debugging techniques that repair code from execution
50 rounds across two datasets plus the top level, and generate           feedback [26] all operate on standalone programs, whereas
over 2,000 jobs each (Table VII). Reducing rounds (E4) cuts              diagnosing a workflow failure requires interpreting evidence
workflow complexity by 80% and execution time to 4.6 hours.              spread across the WMS, the scheduler, and the container run-
Reducing clients (E3) lowers training jobs but not the number            time. Within workflow systems, PANORAMA [27] combines
of sub-workflows, and it lengthens the run to 30.1 hours                 performance models with online monitoring to diagnose run-
because each of the five remaining clients then carries twice            time anomalies in Pegasus workflows, but leaves the corrective
the data, so halving the client count redistributes work rather          action to the operator. The debugging skill addresses both
than removing it.                                                        gaps: it reasons across system layers and applies the fix.
   Federated learning also has dedicated orchestration frame-                      [3] P. Di Tommaso, M. Chatzou, E. W. Floden et al., “Nextflow enables
works such as Flower [28] and PySyft [29], which manage                                reproducible computational workflows,” Nature Biotechnology, vol. 35,
                                                                                       no. 4, pp. 316–319, 2017.
training rounds but lack the provenance, data staging, and fault                   [4] E. Afgan, D. Baker, B. Batut et al., “The galaxy platform for accessible,
tolerance of a scientific WMS. Safri et al. [5] expressed FL as                        reproducible and collaborative biomedical analyses,” Nucleic Acids
                                                                                       Research, vol. 46, no. W1, pp. W537–W544, 2018.
manually constructed Pegasus workflows. Our work generates                         [5] H. Safri, G. Papadimitriou, F. Desprez et al., “A workflow management
such workflows automatically from natural-language intent.                             system approach to federated learning: Application to industry 4.0,” in
                                                                                       Proc. DCOSS-IoT. IEEE, 2024, pp. 259–263.
                          VII. C ONCLUSION                                         [6] Y. Gil, V. Ratnakar, E. Deelman et al., “Wings for pegasus: Creating
                                                                                       large-scale scientific workflows using semantic representations,” in Proc.
    We studied the composition and management of a federated                           SSDBM (SSDBM), 2007.
learning workflow for medical imaging under AI assistance,                         [7] H. Zeng et al., “Flowmind: Automatic workflow generation with large
following it from natural-language intent through a reviewable                         language models,” arXiv preprint arXiv:2404.13050, 2024.
                                                                                   [8] C. Zhang et al., “Aflow: Automating agentic workflow generation,” arXiv
specification, code generation, autonomous debugging, and                              preprint arXiv:2410.10762, 2024.
execution on distributed infrastructure. Separating design from                    [9] K. Thareja and R. Mayani, “Claude code plugin pegasus-ai,”
implementation made the rest possible: the specification was                           https://github.com/pegasus-isi/claude-plugin-marketplace/tree/main/
                                                                                       plugins/pegasus-ai, 2026.
reviewable while the code was still hypothetical, and it later                    [10] R. Mayani, K. Vahi, M. Rynge et al., “Kiso: A foundation for complex,
proved detailed enough both to audit that code and to rebuild                          agentic, and reproducible experiments,” Frontiers in Complex Systems,
it.                                                                                    vol. 4, p. 1800335, 2026.
                                                                                  [11] K. Thareja, A. Mandal, and E. Deelman, “From sensors to insight:
    The generated workflow reached 101 sub-workflows and                               Rapid, edge-to-core application development for sensor-driven applica-
2,679 jobs on nine GPUs across four sites, a design that                               tions,” arXiv preprint arXiv:2605.02844, 2026.
an expert puts at 3 to 4 months of manual development                             [12] K. Thareja, “Pegasus workflow repositories,” https://github.com/
                                                                                       pegasus-isi, 2026.
and that was produced here in two days. Among the LLM                             [13] D. B. Piskala, “Spec-driven development: From code to contract in the
agents evaluated, the one grounded in structured skills surfaced                       age of ai coding assistants,” arXiv preprint arXiv:2602.00180, 2026.
orchestration alternatives before generating any code and re-                     [14] D. Thain, T. Tannenbaum, and M. Livny, “Distributed computing in prac-
                                                                                       tice: The condor experience,” Concurrency and Computation: Practice
solved sub-workflow staging on its first attempt, while agents                         and Experience, vol. 17, no. 2–4, pp. 323–356, 2005.
given the same documentation as unstructured context reached                      [15] K. Clark, B. Vendt, K. Smith et al., “The cancer imaging archive (tcia):
a working design only through repeated follow-up prompts, or                           maintaining and operating a public information repository,” Journal of
                                                                                       Digital Imaging, vol. 26, no. 6, pp. 1045–1057, 2013.
not at all.                                                                       [16] X. Wang, Y. Peng, L. Lu et al., “Chestx-ray8: Hospital-scale chest x-
    Six of the nine defects surfaced as job failures, the evidence                     ray database and benchmarks on weakly-supervised classification and
a debugging loop runs on. The other three produced no                                  localization of common thorax diseases,” Proc. IEEE CVPR, pp. 2097–
                                                                                       2106, 2017.
failure at all, including one that trained all 1,700 training jobs                [17] K. Thareja, “Medical imaging federated learning workflow (claude),”
on random tensors while every job exited successfully with                             https://github.com/pegasus-isi/medical-imaging-fl-workflow, 2026, gen-
well formed metrics. All three were visible in the generated                           erated with Claude Code and the pegasus-ai plugin.
                                                                                  [18] I. Baldin, A. Nikolich, J. Griffioen et al., “Fabric: A national-scale pro-
source, and checking the specification’s constraints against it                        grammable experimental network infrastructure,” IEEE Internet Com-
found them. Static checking is most reliable exactly where                             puting, vol. 23, no. 6, pp. 38–47, 2020.
the runtime is blind, so failure-driven repair and specification-                 [19] Opencode Contributors, “Opencode: An open-source ai coding agent,”
                                                                                       https://github.com/opencode-ai/opencode, 2025.
level checking reach disjoint classes of error and a validation                   [20] K. Thareja, “Fl pegasus workflow (codex),” https://github.com/kthare10/
loop for AI-generated workflows needs both rather than either                          fl-pegasus-workflow-gpt-5.4, 2026, generated with OpenAI Codex.
alone.                                                                            [21] ——, “Fl chest workflow (kimi),” https://github.com/kthare10/
                                                                                       fl-chest-workflow-kimi, 2026, generated with Opencode and Kimi K2.6.
    Our evaluation covers one application and one workflow                        [22] K. Alam and B. Roy, “From prompt to pipeline: Large language models
management system. Future work will apply the methodology                              for scientific workflow development in bioinformatics,” arXiv preprint
to other scientific workflows, workflow systems, and AI coding                         arXiv:2507.20122, 2025.
                                                                                  [23] B. Balis et al., “From research question to scientific workflow: Leverag-
agents to assess its generality.                                                       ing agentic ai for science automation,” arXiv preprint arXiv:2604.21910,
                                                                                       2026.
                        ACKNOWLEDGMENTS                                           [24] M. Chen, J. Tworek, H. Jun et al., “Evaluating large language models
   This work is supported by NSF grant #2513101 and the                                trained on code,” arXiv preprint arXiv:2107.03374, 2021.
                                                                                  [25] Q. Wu, G. Bansal, J. Zhang et al., “Autogen: Enabling next-gen llm
FABRIC Testbed (NSF #2330891). The authors used Claude                                 applications via multi-agent conversation,” in International Conference
to help with the pictures. All intellectual contributions and final                    on Learning Representations, 2024.
editorial decisions remain solely with the human authors.                         [26] X. Chen, M. Lin, N. Schärli et al., “Teaching large language models to
                                                                                       self-debug,” in Proc. ICLR, 2024.
                                                                                  [27] E. Deelman, C. Carothers, A. Mandal, B. Tierney, J. S. Vetter et al.,
                              R EFERENCES                                              “PANORAMA: An approach to performance modeling and diagnosis of
 [1] B. McMahan, E. Moore, D. Ramage et al., “Communication-efficient                  extreme-scale workflows,” Int. J. High Perform. Comput. Appl., vol. 31,
     learning of deep networks from decentralized data,” in Artificial Intelli-        no. 1, pp. 4–18, 2017.
     gence and Statistics. PMLR, 2017, pp. 1273–1282.                             [28] D. J. Beutel, T. Tober, T. Stainton et al., “Flower: A friendly federated
 [2] E. Deelman, K. Vahi, G. Juve, M. Rynge et al., “Pegasus, a workflow               learning framework,” arXiv preprint arXiv:2007.14390, 2020.
     management system for science automation,” Future Generation Com-            [29] A. Ziller, A. Trask, A. Lopardo et al., “Pysyft: A library for easy
     puter Systems, vol. 46, pp. 17–35, 2015.                                          federated learning,” Studies in Computational Intelligence, vol. 965, pp.
                                                                                       111–139, 2021.
