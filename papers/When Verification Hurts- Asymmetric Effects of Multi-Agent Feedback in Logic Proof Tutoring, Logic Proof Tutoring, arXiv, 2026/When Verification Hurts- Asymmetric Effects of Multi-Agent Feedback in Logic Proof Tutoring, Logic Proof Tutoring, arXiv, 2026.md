                                              When Verification Hurts: Asymmetric Effects of Multi-Agent Feedback in
                                                                       Logic Proof Tutoring
                                                 Tahreem Yasir, Sutapa Dey Tithi, Benyamin Tabarsi, Dmitri Droujkov, Sam Gilson
                                                        Yasitha Rajapaksha, Xiaoyi Tian, DongKuan (DK) Xu, Tiffany Barnes
                                                                          North Carolina State University
                                                                                Raleigh, NC, USA
                                         {tyasir, stithi, btaghiz, ddroujk, sagilson, yrajapa, xtian9, dxu27, tmbarnes}@ncsu.edu

                                                                                           Arun Ramesh
                                                                                    rarunkumar15112k@gmail.com
                                                                    Abstract                         than evaluating only final answers (VanLehn, 2011).
                                                                                                     However, traditional ITS relies on template-based
                                                  Large language models (LLMs) are increas-
arXiv:2603.27076v1 [cs.AI] 28 Mar 2026




                                                  ingly used for automated tutoring, but their       feedback that poorly adapts to diverse miscon-
                                                  reliability in structured symbolic domains re-     ceptions (Zerkouk and Chikhaoui, 2025). Large
                                                  mains unclear. We study step-level feedback        language models (LLMs) offer scalable alterna-
                                                  for propositional logic proofs, which require      tives, yet their tendency to hallucinate risks incor-
                                                  precise symbolic reasoning aligned with a          rect feedback undermining learning (Macina et al.,
                                                  learner’s current proof state. We introduce        2023).
                                                  a knowledge-graph–grounded benchmark of
                                                                                                        Effective step-level tutoring requires more than
                                                  516 unique proof states with step-level anno-
                                                  tations and difficulty metrics. Unlike prior
                                                                                                     surface correctness: feedback that is partially cor-
                                                  tutoring evaluations that rely on model self-      rect or misaligned with a student’s proof state can
                                                  assessment or binary correctness, our frame-       reinforce misconceptions and anchor flawed rea-
                                                  work enables fine-grained analysis of feedback     soning even when not strictly wrong (VanLehn,
                                                  quality against verified solution paths. We        2011). Without external grounding, even capable
                                                  evaluate three role-specialized pipelines with     LLMs risk generating feedback that appears cor-
                                                  varying solution access: Tutor (partial solution   rect but misguides student reasoning, motivating
                                                  access), Teacher (full derivation access), and
                                                                                                     the need for verification mechanisms (Dhuliawala
                                                  Judge (verification of Tutor feedback). Our re-
                                                  sults reveal a striking asymmetry: verification    et al., 2024).
                                                  improves outcomes when upstream feedback is           Role-specialized feedback pipelines, where a
                                                  error-prone (<70% accuracy), but degrades per-     dedicated verifier agent evaluates another agent’s
                                                  formance by 4–6pp through over-specification       output, offer a potential safeguard distinct from
                                                  when feedback is already reliable (>85%). Crit-    self-correction (Huang et al., 2024). Yet the condi-
                                                  ically, we identify a shared complexity ceil-      tions under which verification helps, or hurts, is not
                                                  ing; no model or pipeline reliably succeeds on
                                                                                                     well studied. A key factor also overlooked in prior
                                                  proof states exceeding complexity 4–5. These
                                                  findings challenge the assumption that adding
                                                                                                     work is the degree of solution information access
                                                  verifiers or richer context universally improves   for the feedback agent. Greater access may enable
                                                  tutoring, motivating adaptive, difficulty-aware    more precise verification, but risks prematurely re-
                                                  architectures that route problems by estimated     vealing answers and undermining scaffolding (Da-
                                                  complexity and upstream reliability.               heim et al., 2024). Moreover, how information ac-
                                                                                                     cess shapes verification effectiveness, what failure
                                              1   Introduction
                                                                                                     modes emerge, and whether automated accuracy
                                              Propositional logic is foundational to computer        metrics capture the underlying pedagogical char-
                                              science education, underpinning formal reasoning       acteristics remain largely unexplored. We address
                                              in programming, algorithms, and digital systems        these gap in our work with the following research
                                              (Mayer and Baraniuk, 2025). Yet mastering opti-        questions:
                                              mal proof strategies remains challenging for stu-      RQ1: How does the degree of solution information
                                              dents due to limited access to timely and personal-    access shape step-level tutoring feedback effective-
                                              ized tutoring (Inamdar et al., 2025).                  ness across models of varying capability?
                                                 Intelligent tutoring systems (ITS) achieve learn-   RQ2: Under what conditions does role-specialized
                                              ing gains comparable to human tutoring through         verification improve tutoring feedback, and when
                                              step-level feedback, guiding each inference rather     does it degrade performance?
Figure 1: Multi-agent Tutoring with KG-grounded varying hints (a) Student solution is partially correct (using
incorrect rule) Tutor echoes student’s incorrect rule, validates partial correctness (b)Teacher reveals solutions
prematurely and students anchors (c) Judge correctly identifies the error in students reasoning (using incorrect rules
and statements for derivations)


RQ3: What systematic failure modes emerge                    with a KG-encoded multi-path solution space and
across feedbacks in each pipelines, and whether              instance-level difficulty metrics, enabling step-
automated metrics alone capture their pedagogical            level evaluation beyond binary correctness and sup-
impact?                                                      porting the first controlled study to the best of our
                                                             knowledge on information access effects in logic
   We answer these RQs through step-level feed-
                                                             proof tutoring.
back for propositional logic proofs, where students
                                                             Asymmetric Verification Effect: Empirical evi-
apply inference rules (e.g., Modus Ponens, Dis-
                                                             dence that the verification benefit is conditional on
junctive Syllogism) to a set of premises (logical
                                                             upstream feedback reliability, improving outcomes
statements assumed to hold) to derive a target con-
                                                             when feedback is error-prone, but degrading perfor-
clusion through intermediate derivations or steps.
                                                             mance through over-specification when feedback
At each proposed step a tutoring agent must as-
                                                             is already reliable.
sess the derivation and provide scaffolded guidance
without revealing the answer. For our investigation,         Failure Mode Taxonomy: Four systematic fail-
we developed three role-specialized agents (Fig. 1):         ure modes, echo effects, partial correctness val-
Tutor (access only to the correct next step), Teacher        idation, premature revelation, and verification
(full solution access), and Judge (verification of           over-specification, confirmed by human evaluation
Tutor feedback along with full solution access), op-         across four pedagogical dimensions, demonstrat-
erationalizing solution information access as a con-         ing that automated accuracy metrics systematically
trolled variable. Unlike prior evaluations relying on        overestimate feedback quality.
binary correctness, we perform a fine-grained eval-
                                                             2     Related Work
uation against a knowledge graph (KG), encoding
the complete derivation space, enabling analysis of          2.1    LLM-based scaffolding for tutoring
how steps are derived, not only whether they are                    systems
valid. Our contributions are as follows:
                                                             Scaffolding theory (Vygotsky and Cole, 1978) un-
Logic Tutoring Benchmark: A novel dataset of                 derlies intelligent tutoring systems (ITS), where
516 real student propositional logic proof states            step-by-step hints must be specific enough to ad-
                                                         Dataset                               Task       Step Branching Student Difficulty
vance reasoning yet scaffolded enough to pre-
                                                         ProofWriter (Tafjord et al., 2021)  Proof Gen.    ✗       ✗         ✗        ✗
serve productive struggle (Wood et al., 1976; Bel-       FOLIO (Han et al., 2024)               NLI        ✗       ✗         ✗        ✗
                                                         ProntoQA (Saparov and He, 2022)        CoT        ✓       ✗         ✗        ✗
land, 2017). This balance is especially difficult to     LogicLearner (Inamdar et al., 2025) Proof Gen.    ✗       ✗         ✗        ✗
achieve in structured symbolic domains where each        Ours                               Next-Step      ✓       ✓        ✓        ✓

inference step constrains all subsequent reasoning.
   LLMs show promise for generating adaptive             Table 1: Comparison of existing reasoning benchmarks. Step:
                                                         step-level evaluation. Branching: annotated solution space
feedback across diverse educational contexts, with       at multiple branches. Student: real learner data. Difficulty:
prior work demonstrating gains in diagnosing stu-        instance-level complexity metrics.
dent errors, and generating pedagogical feedback
in college algebra tutors (Reddig et al., 2025), fos-    verification effect may help weak generators while
tering active reasoning and self-reflection in ad-       offering limited or negative gains for strong ones in
vanced computer science courses (Kumar et al.,           general reasoning tasks (Zhang et al., 2024). How-
2024), and supporting adaptive scaffolding in pro-       ever, these findings are largely confined to general
gramming contexts (Scholz et al., 2025). However,        reasoning tasks, and whether these patterns hold in
two persistent challenges limit their effectiveness      step-level tutoring contexts remains an open ques-
in intelligent tutoring systems: LLMs often reveal       tion.
answers instead of scaffolded guidance (Macina
et al., 2023, 2025), and their feedback frequently       2.3       Logic Reasoning Benchmarks
hallucinates without external grounding (Liu et al.,     Existing benchmarks for symbolic or logical rea-
2025; Jia et al., 2024). Moreover, LLMs cannot           soning primarily evaluate end-to-end proof genera-
reliably locate reasoning errors in student solutions    tion using single-reference solutions, with limited
even with access to reference solutions (Srivatsa        or no annotations for intermediate reasoning steps
et al., 2025; Tyen et al., 2024; Estévez-Ayres et al.,   (Saparov and He, 2022). ProofWriter (Tafjord et al.,
2025). Yet these limitations remain unaddressed          2021) assesses only final proof validity, obscur-
in structured symbolic domains where step-level          ing whether models apply inference rules correctly
feedback alignment is especially consequential.          at each step. FOLIO (Han et al., 2024) provides
2.2   Role-specialized Feedback Pipelines                expert-authored first-order logic problems but pe-
                                                         nalizes semantically valid alternative derivations,
Role-specialized pipelines have shown promise in         while ProntoQA (Saparov and He, 2022) enables
educational AI, where role separation ensures feed-      controlled evaluation through synthetic reasoning
back meets both accuracy and pedagogical stan-           chains but cannot capture branching decision points
dards (Daheim et al., 2024; Phung et al., 2024),         where multiple inference rules may apply.
addressing over-praise and over-inference errors            In contrast, step-level logic tutoring requires dis-
(dos Santos and Cury, 2025; Chudziak and Kostka,         tinguishing incorrect rule use, suboptimal strate-
2025). Prior work shows that role-specialized            gies, and state misalignment (steps inconsistent
multi-agent systems improve instructional design         with the current proof state), that existing bench-
(Zhang et al., 2025), and that educational evalua-       marks collapse into binary outcomes obscuring in-
tion benefits from incorporating multiple pedagog-       termediate reasoning errors (Saparov and He, 2022;
ical roles (Chen et al., 2025). EducationQ further       Tafjord et al., 2021; Chi and Wylie, 2014). These
demonstrates that student–teacher–evaluator triads       limitations motivate our KG-grounded framework
promote effective scaffolding and align with human       (Section 3), which encodes not only whether a step
pedagogical judgment (Shi et al., 2025). Yet these       is derivable but how; capturing the inference rule
limitations remain unaddressed in structured sym-        and parent statements justifying each derivation,
bolic domains where step-level feedback alignment        enabling evaluation that existing single-reference
is especially consequential.                             benchmarks cannot support.
   Beyond educational context, prior work shows
that self-correction without external grounding          3      Task and Dataset
can degrade reasoning performance (Huang et al.,
2024). Intrinsic self-correction sometimes wors-         3.1       Task Formulation
ens performance across diverse reasoning tasks, in-      A propositional proof problem is a tuple (P, C),
cluding arithmetic reasoning, code generation, and       where P = {p1 , . . . , pn } is a set of premises which
question answering (Kamoi et al., 2024), and that        are logical statements assumed to hold, and C is
the target conclusion. A proof state σ = (P, I, C)        parent statements from P ∪ Ii , such that Ij = Ii ∪
represents a student’s progress, where I is the or-       {d}. The graph is rooted at the initial state σ0 =
dered set of intermediate statements derived so far       (P, ∅, C), in which no intermediates have yet been
by applying inference rules r ∈ R (e.g., Modus Po-        derived, and terminates at the state σ ∗ in which C
nens, Disjunctive Syllogism; complete rule set in         has been successfully derived i.e., C ∈ I ∗ . Each
Appendix A). Each r derives a new statement from          edge is annotated with the inference rule and the
parent statements in P ∪ I, with I = ∅ initially.         parent statements used in the derivation.
   Given σ = (P, I, C), the task is to predict the        Next-step classification: For any state σ ∈
optimal next step s, a statement derivable in exactly     Σ, its distance from conclusion is d(σ) =
one rule application from P ∪ I, that minimises re-       minπ: σ⇝σ∗ |π|, computed via breadth-first search.
maining derivation distance to C, preferring shorter      A predicted step ŝ from state σt yields successor
proofs that reflect more direct reasoning paths. We       σ̂t+1 and is classified as:
focus on single-step prediction, as each feedback         1. Optimal: (σt , σ̂t+1 ) ∈ E and d(σ̂t+1 ) =
round targets exactly one student decision point. A           d(σt ) − 1, i.e., a valid single-step inference that
representative proof instance is in Appendix B.               strictly reduces distance to the goal.
                                                          2. Invalid: (σt , σ̂t+1 ) ∈/ E, i.e., the predicted step
3.2   Dataset Construction
                                                              is not a valid single-step inference from the cur-
We draw on interaction logs from a propositional              rent state, a subtle failure we illustrate below.
logic tutoring system used in an undergraduate dis-       A predicted step ŝ may be symbolically valid, yet
crete mathematics course, at a large public U.S. uni-     inferentially unjustified if it is attributed to an incor-
versity. Further details and illustrations of the tutor   rect rule or unsupported parent statements. For ex-
are present in Appendix C. The tutoring system            ample, a model predicting statement C via Modus
comprises seven levels: a diagnostic assessment           Ponens must correctly identify both (A → C) and
level (pre-test), five practice levels, which include     A as parents; a prediction that produces a valid
on-demand context-specific hints along with im-           statement but misattributes the rule or parents is
mediate feedback on correctness, and a summative          flagged as unjustified regardless of symbolic valid-
assessment level (post-test).                             ity.
   Our dataset comprises 516 unique proof states,            This distinction is pedagogically consequential:
defined at the (P, I, C) triple level, from 32 prob-      tutoring feedback that validates a correct step ar-
lems across five practice levels of varying difficulty    rived at via flawed reasoning reinforces the miscon-
from Spring 2023. Each proof state instance repre-        ception rather than correcting it. We call it partial
sents a distinct student proof state, from minimal        correctness validation failure mode we identify in
configurations with only three premises to complex        Section 6.4.
states with up to 12 intermediate statements. Ta-
ble 4 provides the complete distribution of proof         4    Role-Specialized Tutoring Pipelines
states in the dataset, where unequal instance counts
across levels reflect natural student activity.           We distinguish three role-specialized pipelines that
                                                          vary in solution information access: Student-Tutor,
3.3   Knowledge Graph Construction                        Student-Teacher, and Student-Tutor-Judge. In each
We encode the complete solution space for each            pipeline, agents operate sequentially in a fixed or-
of the 32 problems as a knowledge graph K cap-            der with no bidirectional communication as illus-
turing all valid inference paths from P to C. This        trated in Fig 1.
encoding is exhaustive by construction: given a fi-          We operationalize solution information access
nite premise set and closed rule set R, all reachable     as a controlled variable across three agents:
derivations are enumerable via forward chaining           • Tutor: receives only correct next step s.
(Barnes and Stamper, 2008).                               • Teacher: receives correct next step s with com-
   Let Σ be the set of all reachable proof states for       plete derivation context (inference rule, parents).
each problem. The knowledge graph K = (Σ, E)              • Judge: receives complete derivation context as
has nodes σ ∈ Σ and directed edges (σi , σj ) ∈ E           the Teacher along with Tutor feedback.
representing valid single-step inferences. Each σj        This asymmetric grounding isolates (i) information
is obtained from σi by deriving a new intermediate        access (Tutor vs. Teacher) and (ii) verification ef-
statement s via rule r ∈ R applied to one or two          fects (Tutor vs. Judge) as independent variables
controlling for task difficulty.                         Teacher prompt and sample responses are shown
                                                         in Fig 9 and Fig 13.
4.1   Student
                                                         4.4    Judge
The Student agent simulates an undergraduate
learner with no solution access following (Shi et al.,   The Judge models a quality-assurance reviewer, fol-
2025). Given a proof state σt the agent predicts the     lowing verifier-in-the-loop designs in educational
next state σt+1 . To this end, it generates (i) 2–3      AI (Phung et al., 2024; Shi et al., 2025). It re-
candidates with rationales, (ii) select the optimal      ceives full derivation context σt+1 and Tutor feed-
σt+1 along reasoning, (iii) next step s, (iv) infer-     back, to evaluate both the student’s step and the
ence rule, and (v) parent statements. This multi-        Tutor’s feedback for correctness and answer leak-
candidate approach reflects least-to-most prompt-        age. Based on this, it either enhances or overrides
ing (Zhou et al., 2022) and pedagogical chain-of-        the tutor’s feedback, addressing over-praise and
thought (Jiang et al., 2024), externalizing reasoning    answer-leakage failures common in single-agent
that tutoring agents can reference when scaffolding.     systems (Gonnermann-Müller et al., 2025; Zhang
   After feedback, the Student agent revises their       et al., 2025). Judge prompt and sample responses
response only if errors are identified ensuring mea-     are given in Fig 10, Fig 16, and 15.
sured improvements reflect genuine feedback ef-
                                                         4.5    Shared Constraints
fects rather than forced changes. Student agent
prompts and a sample student response are shown          All feedback agents adhere to scaffolding princi-
in Figs 6, 7, and 11.                                    ples from learning science, guide discovery without
   The Student agent revises only when errors are        revealing answers (Belland, 2017; Van de Pol et al.,
identified, ensuring measured improvements re-           2010), employ Socratic questioning over directives
flect genuine feedback effects rather than forced        (Chen, 2023), reference student candidates for rele-
changes.                                                 vance (Serban et al., 2020), and acknowledge cor-
                                                         rect reasoning before addressing errors (Shi et al.,
4.2   Tutor                                              2025). Feedback is limited to 2-3 sentences.

The Tutor models a teaching assistant (TA) who           4.6    Interaction Protocol
knows the correct answer but not the derivation, a
                                                         Each interaction consists of a single feedback round
more constrained setting than the restricted-teacher
                                                         to isolate pipeline effects. To ensure fair compari-
condition in Shi et al. (2025). Tutor receives only
                                                         son, initial Student responses were generated once
the optimal next step s without derivation context
                                                         and reused across all pipelines; Tutor feedback
(rule, parent statements), requiring inference of
                                                         from the Student-Tutor pipeline was reused in the
both the applicable rule and reasoning (Kochmar
                                                         Student-Tutor-Judge pipeline. All agents communi-
et al., 2022). It classifies student responses as op-
                                                         cate via structured JSON format, where fewer than
timal or invalid and provides scaffolded feedback
                                                         3% of instances required a retry due to malformed
guided by the shared scaffolding constraints (§4.5).
                                                         JSON output. Implementation details and quality
This tests whether correctness-only grounding suf-
                                                         validation constraints across dialogue generation
fices for effective tutoring. Tutor prompt and a
                                                         appear in Appendix H.
sample response are shown in Fig 8 and Fig 12.
                                                         5     Experimental Setup and Evaluation
4.3   Teacher
The Teacher models an instructor with full solution      5.1    Evaluation Metrics
access, the standard assumption in ITS (Corbett,         Building on the KG evaluation framework, we de-
2001; Barnes and Stamper, 2008) representing the         fine six metrics that operationalize pipeline perfor-
upper bound on information availability. It receives     mance at the proof-state level.
the complete derivation σt+1 (rule, parents, optimal     Task Performance: We report Pre (student-only)
next step s), enabling precise evaluation and feed-      and Post (after feedback) accuracy, each evaluated
back, which may risk answer revelation (Daheim           over all N =516 proof states. It is computed as
et al., 2024), a limitation that we discuss in sec-      the proportion of Optimal predictions by classi-
tion 6.4. Comparing with Tutor, Teacher isolates         fying predicted next steps as Optimal or Invalid
the effect of solution access on feedback quality.       per next-step classification described in (Sec 3.3).
The Learning gain ∆ = Post − Pre is reported in          6     Results
percentage points (pp).
Tutor Rule Accuracy: measures how often the              We organize our findings around three RQs: how
Tutor correctly predicts the inference rule for the      information access shapes feedback (RQ1), when
optimal step, given only s as input, serving as a        does role-specialized verification improves or de-
proxy for upstream feedback reliability.                 grades the feedback (RQ2), what failure modes
Reasoning Difficulty Analysis: Step Complexity           emerge in feedback across pipelines and whether
quantifies the symbolic difficulty of a proof step       automated metrics capture the pedagogical impact
as a weighted function of logical operators and          (RQ3). We begin with baseline performance, then
nesting depth (Appendix E), providing a model-           address each RQ in turn, complimenting the eval-
independent characterization of instance difficulty.     uation metrics with expert human evaluation of
We report Mean Complexity, the average Step Com-         feedback, and discussing the pedagogical aspects.
plexity of proof states where each pipeline im-
                                                         6.1    Baseline (Student Reasoning
proves student performance, to characterize which
                                                                Performance)
difficulty regimes benefit from each condition.
Verification Effects: To isolate verification’s ef-      As shown in Table 2, baseline performance varies
fects beyond full solution access, we compute the        markedly across models. DeepSeek and Gemini
Unique Improvement Count (UIC), the number of            achieve the highest pre-feedback accuracy (56%
proof states where only the Judge pipeline succeeds      and 54.5%), followed by Qwen (46%), while
and the Teacher pipeline fails on identical student      GPT variants and Mistral perform more modestly
inputs. Since both pipelines share full derivation       (20–25%) and LLaMA performs weakest (17%).
access, any Judge improvement over Teacher is            Examining baseline accuracy alongside Tutor rule
attributable solely to verification rather than infor-   accuracy reveals two model groups. We refer to
mation access.                                           Gemini and DeepSeek, which consistently exhibit
Feedback Quality (Human Annotation): To iden-            high performance on both measures, as strong
tify failure mechanisms that automated metrics can-      models. In contrast, GPT models, Mistral, Qwen,
not capture, three domain experts with at least two      LLaMA show lower performance on both dimen-
years of undergraduate Discrete Structures teach-        sions and are referred to as weak models in this
ing experience independently annotated feedback          paper.
responses across all pipelines on four dimensions:
                                                         6.2 Effect of Information Access on Feedback
Mistake Identification, Correctness, Answer Reve-
                                                             Quality (RQ1)
lation, and Actionability (Krippendorff’s α ≥ 0.65;
full protocol in Appendix J). Three systematic fail-     Tutor: Tutor agents receive only the correct next
ure modes emerge.                                        step without rule or parent statements, requiring
                                                         inference of the full derivation before generating
5.2   Experimental Setup                                 feedback. Despite this, Tutor post-feedback accu-
We evaluate seven LLMs spanning reasoning-               racy reaches 24 − 77% across models, with models
augmented models (GPT-o3, Gemini-1.5-Pro,                referred to as weak improved modestly over base-
DeepSeek-R1), standard instruction-tuned models          line (GPT-4.1: 21% → 43%, Mistral: 24% → 38%,
(GPT-4.1, Qwen-3-32B), and open-source models            LLaMA: 18% → 24%) and strong models im-
(Mistral-Large, LLaMA-3.3-70B). This selection           proving more substantially (Gemini: 53% → 74%,
covers diverse capability levels and architectural       DeepSeek: 56% → 77%). However, these accuracy
families, enabling analysis of whether pipeline ef-      gains mask a systematic limitation: without deriva-
fects are capability-dependent (Sec 6).                  tional context, Tutor feedback is often directionally
   Each model serves as both a student and a             correct but insufficiently specific to repair student
feedback agent (Tutor, Teacher, Judge) across all        reasoning at the rule level. Human evaluation fur-
pipelines, generating 516 × 7 × 3 = 10,836 dia-          ther confirms this limitation, as discussed in Sec
logues (516 proof states × 7 models × 3 pipelines).      6.4.
All experiments use temperature 0.0 via APIs listed      Teacher: Full derivation access (Teacher) im-
in Appendix I for reproducibility. Model specifica-      proves feedback on harder instances for some mod-
tions and sample dialogues are presented in Appen-       els, but not uniformly. Among improved cases,
dices I and G.                                           Teacher mean complexity (1.85-3.17; Table 2) ex-
Table 2: Pipeline performance across seven LLMs (N = 516), bold values indicate best Post accuracy per model.

 Model            Pre (%) Rule Acc.              Post (%)            ∆        Mean Complexity        UIC over Teacher
                  Student Tutor (%) Tutor Teacher Judge              pp    Tutor Teacher Judge UIC              Gap

 GPT-4.1             21.31       58.30     42.82     61.24   75.38 54.07 1.8          2.21        2.7   89        1.63
 GPT-o3              24.80       60.10     48.25     61.24   75.58 50.78 2.04         2.26       2.65   84         1.4
 Gemini-1.5-pro 52.52             85.8     73.92     78.79   72.95 20.43 3.73         3.17       3.65   23        2.22
 Deepseek-R1           56        84.9      76.55     84.30   79.84 23.84 3.49         3.06       3.37   17        3.19
 Mistral-Large       23.74       54.80     38.41     41.69   56.37 32.63 1.86         1.85       2.43 103         0.95
 Qwen-3-32B            46        70.20     60.36     63.63   66.90 20.9 2.29          2.19        2.6   39        1.59
 Llama-3.3-70B       17.98       24.70     24.30     34.38   39.32 21.34 2.06         2.06       2.33   55        0.41
Pre/Post: student accuracy before and after feedback; ∆: learning gain in percentage points (pp); Rule Acc.: Tutor rule
prediction accuracy, proxy for upstream reliability; Mean Complexity: average proof-state complexity of pipeline-improved
instances; UIC: instances where Judge succeeds after Teacher fails; Gap: difference between predicted and optimal step
complexity (0 is ideal).


ceeds Tutor primarily for GPT-based models, while             the same Judge agent to Teacher feedback to test
Tutor reaches comparable or higher complexity for             whether verification can mitigate premature revela-
others. Logistic regression confirms that Teacher             tion. This yields no consistent benefit: performance
× Complexity interactions are significant mainly              improves only for DeepSeek (+4pp) and is neutral
for strong models (Gemini: β = +0.65, DeepSeek:               or harmful for all other models.
β = +0.36, p < .001; Table 6), indicating that full              These results confirm that verification effective-
access benefits only models able to utilize deriva-           ness depends on upstream error rate, not informa-
tional context.                                               tion access: the Judge corrects erroneous guidance
                                                              but cannot enhance already reliable feedback, and
6.3   Conditional Effects of Verification (RQ2)               cannot undo premature revelation once disclosed.
Table 2 shows that verification yields large gains            Human evaluation is consistent with this: Judge
for weak Tutor agents (Rule Acc. <70%: GPT-                   feedback scores higher on Correctness and Action-
4.1, GPT-o3, Mistral, LLaMA), averaging +35pp,                ability than Tutor for weak models. mention the
but degrades performance for strong Tutor agents              radar plot
(Gemini, DeepSeek; Rule Acc. >84%) by approx-                    Universal Complexity Ceiling Across all mod-
imately −5pp as compare to the Teacher. This                  els and pipelines, performance degrades sharply
asymmetry correlates with complexity: weak Tutor              once proof-state complexity exceeds 4–5 (Table 7
agents improve only on low-complexity problems                in Appendix). This ceiling is independent of verifi-
(mean 1.8–2.1), while Judge agents extend gains               cation or information access: simple states (com-
to harder problems (mean 2.4–2.7). Strong Tutor               plexity <2.5) require minimal intervention, mid-
agents already succeed at high complexity (mean               complexity states (2.5–4.0) benefit most from veri-
3.5–3.7), leaving limited scope for verification.             fication, and high-complexity states (>4.5) remain
    Unique Improvement Count The UIC quan-                    challenging for all approaches, suggesting that the
tifies verification’s marginal contribution beyond            bottleneck at high complexity is symbolic reason-
Teacher: weak models show n ∈ [84, 103] unique                ing capacity rather than feedback pipeline design.
Judge successes after Teacher failure, vs. 17–23 for
strong models (Table 2). The Complexity Gap (0.4–             6.4    Human Evaluation - Failure Mode
1.6 for weak, 2.2–3.2 for strong models) confirms                    Analysis (RQ3)
that verification addresses high-complexity edge              Automated accuracy metrics reward correct out-
cases where weak Tutor feedback fails. Regression             comes but cannot penalize pedagogically flawed
analysis confirms this pattern: Judge × Complex-              reasoning paths. Human evaluation across four
ity interactions are positive and significant across          dimensions (§5.1) reveals four systematic fail-
nearly all models (GPT-4.1: β = +0.22, Gemini:                ure modes. Echo Effect (Tutor). Weak Tutor
β = +0.61, DeepSeek: β = +0.56; all p < .001;                 agents, lacking derivational context, anchor on the
Table 6).                                                     student’s incorrect rule rather than correcting it
    Ablation: Verifier on Teacher Feedback. To                (Fig 15). Human evaluation confirms this system-
further isolate the role of verification, we applied          atically: Tutor feedback scores lowest on Mistake
Identification among weak models, indicating in-       try is governed by the proof-state Complexity. Ver-
sufficient derivational grounding rather than ran-     ification helps in intermediate regimes but cannot
dom noise. Verification mitigates this through KG-     overcome a shared reasoning ceiling (complexity
grounded override (§6.3).                              >4–5) beyond which no pipeline reliably succeeds.
   Partial Correctness Validation (Tutor). When        We identify three systematic failure modes: echo
students predict the correct step via flawed rea-      effects, partial correctness validation, and prema-
soning, Tutor agents validate the faulty logic, re-    ture revelation that verification mitigates only under
inforcing misconceptions. Correctness scores re-       limited conditions. These findings challenge the
main moderate even when post-feedback accuracy         assumption that adding verifiers or solution access
improves, confirming that accuracy overestimates       improves tutoring. Instead, effective LLM tutoring
genuine reasoning repair (Kamoi et al., 2024; Tyen     requires adaptive pipelines that estimate upstream
et al., 2024).                                         reliability and route problems by complexity, rather
   Premature Revelation. Teacher feedback fre-         than defaulting to more agents or richer context.
quently discloses the correct step or over-specifies
derivational hints (Fig 14), leading student agents    Limitations
to anchor on the disclosed answer without inte-        This study has several limitations. First, our evalu-
grating it into their reasoning. Human evaluation      ation is restricted to propositional logic proof tutor-
confirms that Teacher feedback scores highest on       ing, and the findings may not directly generalize to
Answer Revelation while Actionability scores re-       domains with weaker symbolic constraints or richer
main moderate, indicating that disclosed answers       semantic structure. While our primary metrics as-
produce surface-level correctness rather than trans-   sess the intrinsic properties of feedback indepen-
ferable reasoning improvement.                         dently of the receiver, LLM students may respond
   Verification Over-Specification. Although           differently from human learners; therefore, human-
Judge feedback improves Correctness and Mistake        in-the-loop validation would be necessary to sub-
Identification for weak models, human evaluation       stantiate claims about learning outcomes. Second,
reveals a distinct failure mode for strong models:     while our knowledge-graph-based metrics enable
when the Judge overrides already reliable Tutor        fine-grained analysis of step-level reasoning, they
feedback, the resulting guidance becomes overly        rely on a predefined solution space and do not cap-
abstract, reducing Actionability scores below those    ture open-ended or creative reasoning strategies.
of the original Tutor feedback. This pattern mirrors   Third, our experiments focus on single-step feed-
the quantitative degradation observed for Gemini       back and do not model long-horizon student–tutor
and DeepSeek (−5pp) and suggests that verifica-        interactions or learning gains over time. Moreover,
tion introduces a specificity cost when upstream       our qualitative analysis is limited to a small expert-
feedback is already well-grounded: the Judge im-       reviewed sample (10 responses per model), and
poses derivational constraints that narrow rather      broader manual analysis could reveal additional
than scaffold the student’s reasoning space.           failure modes. Finally, although we analyze multi-
   Human evaluation confirms the four failure          ple large language models, results may vary with
modes, demonstrating that automated metrics over-      future architectures or training regimes.
estimate feedback quality by rewarding correct out-
comes without penalizing flawed reasoning paths        Ethics Statement
or answer leakage.                                     Student interaction data was collected under IRB
                                                       approval with informed consent. All data was
7   Conclusion                                         anonymized before analysis. Our LLM-based Eval-
We present a controlled study of multi-agent LLM       uation does not involve human subjects beyond
tutoring for propositional logic using a knowledge-    annotators, who serve as researchers for the tutor-
graph–grounded benchmark of 516 proof states.          ing system used for data generation in this study,
Our central finding is that verification benefit is    as well as co-authors of this study.
asymmetric: it improves outcomes by +10–14pp
                                                       Reproducibility
when upstream feedback is error-prone (<70% ac-
curacy), but degrades performance by 4–6pp when        Code and data will be released upon publication.
feedback is already reliable (>85%). This asymme-      All experiments use temperature 0.0 to ensure de-
terministic, reproducible results, prioritizing con-        Jarosław A Chudziak and Adam Kostka. 2025. Ai-
trolled comparison over response diversity. While              powered math tutoring: Platform for personalized
                                                               and adaptive education. In International Conference
real-world tutoring systems might benefit from non-
                                                               on Artificial Intelligence in Education, pages 462–
zero temperature, our evaluation focuses on mea-               469. Springer.
suring the systematic effects of multi-agent archi-
                                                            Albert Corbett. 2001. Cognitive computer tutors: Solv-
tectures under controlled conditions. Model speci-
                                                              ing the two-sigma problem. In International Confer-
fications and prompts appear in Appendices I and              ence on User Modeling, pages 137–147. Springer.
F.
                                                            Nico Daheim, Jakub Macina, Manu Kapur, Iryna
                                                              Gurevych, and Mrinmaya Sachan. 2024. Stepwise
AI Usage Disclosure                                           verification and remediation of student reasoning er-
                                                              rors with large language model tutors. In Proceed-
This work studies and evaluates large language
                                                              ings of the 2024 Conference on Empirical Methods
models as research objects. We utilized large lan-            in Natural Language Processing, pages 8386–8411.
guage models as assistive tools during manuscript
                                                            Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu,
preparation, including formatting guidelines and
                                                              Roberta Raileanu, Xian Li, Asli Celikyilmaz, and Ja-
brainstorming organization, mainly, and paraphras-            son Weston. 2024. Chain-of-verification reduces hal-
ing on a need basis only. We did not use any AI               lucination in large language models. In Findings of
tools for designing, implementing, or executing this          the Association for Computational Linguistics: ACL
research study. All the claims, analyses, hypothe-            2024, pages 3563–3578.
ses, and conclusions are developed, verified, and           O Lube dos Santos and D Cury. 2025. Intelligent multi-
reviewed by the authors. Moreover, no AI tool was             agent systems with generative ai in education: A sys-
used for generating or labeling data, making judg-            tematic literature mapping. ICERI2025 Proceedings,
                                                              pages 9037–9046.
ments about data, or making any scientific claims.
All implementations were reviewed, validated, and           Iria Estévez-Ayres, Patricia Callejo, Miguel Ángel
finalized by the authors. The authors take full re-            Hombrados-Herrera, Carlos Alario-Hoyos, and Car-
                                                               los Delgado Kloos. 2025. Evaluation of llm tools
sponsibility for the correctness, originality, and             for feedback generation in a course on concurrent
integrity of the work.                                         programming. International journal of artificial in-
                                                               telligence in education, 35(2):774–790.
                                                            Jana Gonnermann-Müller, Jennifer Haase, Konstantin
References                                                    Fackeldey, and Sebastian Pokutta. 2025. Facet:
Tiffany Barnes and John Stamper. 2008. Toward au-             Teacher-centred llm-based multi-agent systems-
   tomatic hint generation for logic proof tutoring us-       towards personalized educational worksheets. arXiv
   ing historical student data. In International confer-      preprint arXiv:2508.11401.
   ence on intelligent tutoring systems, pages 373–382.
                                                            Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhent-
   Springer.
                                                              ing Qi, Martin Riddell, Wenfei Zhou, James Coady,
Brian R Belland. 2017. Instructional scaffolding in stem      David Peng, Yujie Qiao, Luke Benson, and 1 oth-
  education: Strategies and efficacy evidence. Springer       ers. 2024. Folio: Natural language reasoning with
  Nature. Comprehensive review of scaffolding strate-         first-order logic. In Proceedings of the 2024 Con-
  gies in STEM.                                               ference on Empirical Methods in Natural Language
                                                              Processing, pages 22017–22031.
Jiaju Chen, Yuxuan Lu, Xiaojie Wang, Huimin Zeng,           Jie Huang and 1 others. 2024. Large language models
   Jing Huang, Jiri Gesi, Ying Xu, Bingsheng Yao,              cannot self-correct reasoning yet. In International
   and Dakuo Wang. 2025. Multi-agent-as-judge:                 Conference on Learning Representations (ICLR).
   Aligning llm-agent-based automated evaluation with
   multi-dimensional human evaluation. arXiv preprint       Amogh Inamdar, Uzay Macar, Michel Vazirani, Michael
   arXiv:2507.21028.                                         Tarnow, Zarina Mustapha, Natalia Dittren, Sam
                                                              Sadeh, Nakul Verma, and Ansaf Salleb-Aouissi.
others Chen. 2023. Artificial intelligence in intelligent     2025. Logiclearner: A tool for the guided prac-
   tutoring systems toward sustainable education: A           tice of propositional logic proofs. arXiv preprint
   systematic review. Smart Learning Environments,            arXiv:2503.19280.
  10:41. ITS monitor progress, provide feedback, hints,
   and scaffolding.                                         Qinjin Jia, Jialin Cui, Ruijie Xi, Chengyuan Liu, Parvez
                                                              Rashid, Ruochi Li, and Edward Gehringer. 2024. On
Michelene TH Chi and Ruth Wylie. 2014. The icap               assessing the faithfulness of llm-generated feedback
  framework: Linking cognitive engagement to ac-              on student assignments. In Proceedings of the 17th
  tive learning outcomes. Educational psychologist,           International Conference on Educational Data Min-
  49(4):219–243.                                              ing, pages 491–499.
Zhuoxuan Jiang, Haoyuan Peng, Shanshan Feng, Fan            Abulhair Saparov and He He. 2022. Language models
  Li, and Dongsheng Li. 2024. Llms can find mathe-            are greedy reasoners: A systematic formal analysis of
  matical reasoning mistakes by pedagogical chain-of-         chain-of-thought. arXiv preprint arXiv:2210.01240.
  thought. arXiv preprint arXiv:2405.06705.
                                                            Niklas Scholz, Manh Hung Nguyen, Adish Singla, and
Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han,                Tomohiro Nagashima. 2025. Partnering with ai: A
  and Rui Zhang. 2024. When can llms actually cor-            pedagogical feedback system for llm integration into
  rect their own mistakes? a critical survey of self-         programming education. In European Conference
  correction of llms. Transactions of the Association         on Technology Enhanced Learning, pages 243–248.
  for Computational Linguistics, 12:1417–1440.                Springer.
Ekaterina Kochmar, Dung Do Vu, Robert Belfer, Varun         Iulian Vlad Serban and 1 others. 2020. Automated per-
  Gupta, Iulian Vlad Serban, and Joelle Pineau. 2022.          sonalized feedback improves learning gains in an
  Automated data-driven generation of personalized             intelligent tutoring system. In International Confer-
  pedagogical interventions in intelligent tutoring sys-       ence on Artificial Intelligence in Education, pages
  tems. International Journal of Artificial Intelligence       140–146. Springer. Personalized hints improve learn-
  in Education, 32(2):323–349.                                 ing gains; feedback from ZPD.
Harsh Kumar, Ruiwei Xiao, Benjamin Lawson, Ilya             Yao Shi, Rongkeng Liang, and Yong Xu. 2025. Ed-
  Musabirov, Jiakai Shi, Xinyuan Wang, Huayin Luo,            ucationQ: Evaluating LLMs’ teaching capabilities
  J. Williams, Anna N. Rafferty, John Stamper, and            through multi-agent dialogue framework. In Pro-
  Michael Liut. 2024. Supporting self-reflection at           ceedings of the 63rd Annual Meeting of the Associa-
  scale with large language models: Insights from ran-        tion for Computational Linguistics (Volume 1: Long
  domized field experiments in classrooms. Proceed-           Papers), pages 32799–32828, Vienna, Austria. Asso-
  ings of the Eleventh ACM Conference on Learning @           ciation for Computational Linguistics.
  Scale.
                                                            Kv Aditya Srivatsa, Kaushal Kumar Maurya, and Eka-
Rongxin Liu, Julianna Zhao, Benjamin Xu, Christopher
                                                              terina Kochmar. 2025. LLMs cannot spot math er-
  Perez, Yuliia Zhukovets, and David J Malan. 2025.
                                                              rors, even when allowed to peek into the solution.
  Improving ai in cs50: Leveraging human feedback
                                                              In Proceedings of the 2025 Conference on Empiri-
  for better learning. In Proceedings of the 56th ACM
                                                              cal Methods in Natural Language Processing, pages
  Technical Symposium on Computer Science Educa-
                                                              10914–10928, Suzhou, China. Association for Com-
  tion V. 1, pages 715–721.
                                                              putational Linguistics.
Jakub Macina, Nico Daheim, Sankalan Chowdhury, Tan-
   may Sinha, Manu Kapur, Iryna Gurevych, and Mrin-         Oyvind Tafjord, Bhavana Dalvi, and Peter Clark. 2021.
   maya Sachan. 2023. Mathdial: A dialogue tutoring           Proofwriter: Generating implications, proofs, and
   dataset with rich pedagogical properties grounded in       abductive statements over natural language. In Find-
   math reasoning problems. In Findings of the Associ-        ings of the Association for Computational Linguistics:
   ation for Computational Linguistics: EMNLP 2023,           ACL-IJCNLP 2021, pages 3621–3634.
   pages 5602–5621.
                                                            Gladys Tyen, Hassan Mansoor, Victor Cărbune, Peter
Jakub Macina, Nico Daheim, Ido Hakimi, Manu Kapur,            Chen, and Tony Mak. 2024. Llms cannot find rea-
   Iryna Gurevych, and Mrinmaya Sachan. 2025. Math-           soning errors, but can correct them given the error
   tutorbench: A benchmark for measuring open-ended           location. Preprint, arXiv:2311.08516.
   pedagogical capabilities of llm tutors. arXiv preprint
   arXiv:2502.18940.                                        Janneke Van de Pol, Monique Volman, and Jos
                                                              Beishuizen. 2010. Scaffolding in teacher–student
Paul Mayer and Rich Baraniuk. 2025. The importance            interaction: A decade of research. Educational Psy-
  of teaching logic to computer scientists and electrical     chology Review, 22(3):271–296. Comprehensive re-
  engineers. ACM Transactions on Computing Educa-             view of scaffolding in teacher-student interactions.
  tion, 25(2):1–12.
                                                            Kurt VanLehn. 2011. The relative effectiveness of
Tung Phung, Victor-Alexandru Pădurean, Anjali Singh,         human tutoring, intelligent tutoring systems, and
  Christopher Brooks, José Cambronero, Sumit Gul-             other tutoring systems. Educational Psychologist,
  wani, Adish Singla, and Gustavo Soares. 2024. Au-           46(4):197–221. Step-based ITS achieve effect sizes
  tomating human tutor-style programming feedback:            of 0.75-0.80, comparable to human tutoring (0.79).
  Leveraging gpt-4 tutor model for hint generation and
  gpt-3.5 student model for hint validation. In Proceed-    Lev Semenovich Vygotsky and Michael Cole. 1978.
  ings of the 14th learning analytics and knowledge           Mind in society: Development of higher psychologi-
  conference, pages 12–23.                                    cal processes. Harvard university press.
Jennifer M Reddig, Arav Arora, and Christopher J            David Wood, Jerome S Bruner, and Gail Ross. 1976.
  MacLellan. 2025. Generating in-context, person-             The role of tutoring in problem solving. Journal
  alized feedback for intelligent tutors with large lan-      of Child Psychology and Psychiatry, 17(2):89–100.
  guage models. International Journal of Artificial           Foundational work on scaffolding and just-in-time
  Intelligence in Education, pages 1–42.                      interventions.
Mohamed Zerkouk and Belkacem Chikhaoui. 2025. A                 Representative proof Instance
 comprehensive review of ai-based intelligent tutor-
 ing systems: Applications and challenges. arXiv                Givens
 preprint arXiv:2507.18882. ITS can improve student             • (1) ((S → Y ) ∨ (I ∗ Q))
 performance; CLT informs stepwise hint design.
                                                                • (2) ((I ∧ Q) → D)
Xueqiao Zhang, Chao Zhang, Jianwen Sun, Jun Xiao,
  Yi Yang, and Yawei Luo. 2025. Eduplanner: Llm-                • (3) ¬D
  based multi-agent systems for customized and intel-
  ligent instructional design. IEEE Transactions on             • (4) ((S → Y ) → D)
  Learning Technologies.                                        Intermediate Steps
Yifan Zhang and 1 others. 2024. Small language mod-             • (5) ¬(S → Y )                    [MT: (3), (4)]
  els need strong verifiers to self-correct reasoning. In
  Findings of the Association for Computational Lin-            • (6) ¬(I ∧ Q)                     [MT: (3), (2)]
  guistics (ACL).                                               • (7) (S → Y )                     [DS: (6), (1)]
Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei,               Conclusion: Y
  Nathan Scales, Xuezhi Wang, Dale Schuurmans,
  Claire Cui, Olivier Bousquet, Quoc Le, and 1 oth-             Tutor Hint
  ers. 2022. Least-to-most prompting enables complex            ¬(¬S ∨ Y )
  reasoning in large language models. arXiv preprint
  arXiv:2205.10625.                                             Teacher & Judge Hint
A      Inference Rule List                                      Derive ¬(¬S ∨ Y ) from ¬(S → Y ) using the
We employ a fixed set of propositional inference                Implication rule.
rules used in Logic Tutor for the dataset. The short
names were used for consistent response genera-
                                                            Figure 2: Illustrative proof instance showing intermedi-
tion and evaluation. The complete list of inference
                                                            ate derivations and differential hint access for Tutor and
rules, along with short names and derivations are           Teacher agents.
provided below in Table 3.
Table 3: Propositional inference rules used in this work.   with each step indexed and linked to its parent state-
                                                            ments and rule application. This explicit structure
Abbrev. Rule Name               Form
                                                            exposes the shortest derivation path toward the con-
MP        Modus Ponens           P → Q, P ⇒ Q               clusion while preserving alternative valid reasoning
MT        Modus Tollens          P → Q, ¬Q ⇒ ¬P
Conj      Conjunction            P, Q ⇒ P ∧ Q               trajectories.
Simp      Simplification         P ∧ Q ⇒ P (or Q)              The Tutor is provided only with the KG-verified
Add       Addition               P ⇒P ∨Q
DS        Disjunctive Syllogism P ∨ Q, ¬P ⇒ Q
                                                            optimal next symbolic step, enabling guidance that
HS        Hypothetical Syllogism P → Q, Q → R               focuses on local progression without access to
                                 ⇒P →R                      derivational context. In contrast, the Teacher ad-
Impl      Implication            P → Q ≡ ¬P ∨ Q
DN        Double Negation        P ≡ ¬¬P
                                                            ditionally receives the rule and parent statements
CP        Contraposition         P → Q ≡ ¬Q → ¬P            used to derive this step, allowing feedback to ref-
Com       Commutation            P ∨Q≡Q∨P                   erence structural reasoning without revealing the
Assoc     Associativity          (P ∨ Q) ∨ R
                                 ≡ P ∨ (Q ∨ R)              answer directly. This distinction isolates the effect
Dist      Distribution           P ∧ (Q ∨ R)                of solution access: the Tutor operates under min-
                                 ≡ (P ∧ Q) ∨ (P ∧ R)        imal grounding, while the Teacher leverages full
CD        Constructive Dilemma (P → Q), (R → S), P ∨ R
                                 ⇒Q∨S                       derivational context to support more informed inter-
Equiv     Equivalence            P ↔Q                       vention. The representative proof state is available
                                 ≡ (P → Q) ∧ (Q → P )       in Fig 2.

B      Representative Proof State                           C     Illustrative Logic Tutor Proof
                                                                  Interaction
This appendix presents an illustrative propositional
logic proof instance Fig 2 annotated with inter-            Figure 3–5 illustrates a representative student in-
mediate derivations and agent-specific hints. In-           teraction in the propositional logic tutor. These
termediate steps are derived by applying valid in-          screenshots demonstrate forward chaining, rule ap-
ference rules to previously established statements,         plication, and goal completion within the tutor in-
terface.




                                                                  Figure 5: Successful proof completion. The student
                                                                  derives J via Disjunctive Syllogism and applies the
Figure 3: Initial proof state and goal specification.             Addition rule to reach the target conclusion J ∨ K. The
The student is presented with the premises (top left) and         system confirms completion, reinforcing correct rule
the target conclusion (J ∨ K) at the bottom. Available            sequencing and alignment with the goal state.
inference rules are displayed on the middle. At this
stage, no intermediate steps have been derived, and the
student must choose a productive forward step toward              to evaluate next-step reasoning quality. All metrics
the goal.                                                         are computed with respect to the knowledge graph
                                                                  (KG) constructed for each problem.

                                                                  E.1   Step Complexity
                                                                  Beyond derivational validity, Step Complexity quan-
                                                                  tifies the intrinsic symbolic difficulty of a single
                                                                  inference step based on the structural complexity of
                                                                  the derived statement. We define step complexity
                                                                  as a function
                                                                                      c : E → R+ ,
                                                                  computed directly from the syntactic structure of ϕ.
Figure 4: Rule application with guided simplifica-                Let O(ϕ) denote the set of logical operators in ϕ,
tion. After deriving an intermediate conjunction via              and let depth(o) denote the nesting depth at which
Modus Ponens, the student applies the Simplification              operator o occurs. The complexity of the step is
rule. The interface prompts the learner to select the             defined as:
appropriate resulting literal (G or ¬H), illustrating fine-
grained, step-level decision making supported by rule                                   X
                                                                          c(si , sj ) =     w(o) · αdepth(o) ,
constraints.
                                                                                       o∈O(ϕ)

                                                                  where w(o) is an operator-specific base weight
D       Dataset Distribution                                      (e.g., ¬, ∧, ∨, →, ↔) and α > 1 controls the
                                                                  penalty for nested structure. For example, c(F ) <
Table 4: Dataset distribution across practice levels (2-6)        c(A + B) < c(A → (B + C), because no opera-
                                                                  tor is involved, only 1 operator is involved, and 2
      Difficulty          Proof States    Avg. Statements
                                                                  operators involved along with nesting.
      2 (Introductory)         48                5.86
      3 (Basic)                111               7.73             E.2   Distance to Conclusion
      4 (Intermediate)         148               7.94
      5 (Advanced)             85                5.64             For any proof state s ∈ S, its distance is defined
      6 (Expert)               95                6.41             as the length of the shortest derivation path to a
      Total                    516               6.72             terminal state s∗ : d(s) = minπ:s⇝s∗ |π| computed
*
    Levels 1 and 7 excluded because of unavailability of hints.   via breadth-first search over the KG. A predicted
                                                                  next step is considered optimal if it strictly reduces
E       Knowledge Graph based Evaluation
                                                                  the distance to the goal by one.
        Metrics
                                                                     Example If d(st ) = 4 and a predicted succes-
This appendix provides formal definitions and illus-              sor state ŝt+1 satisfies d(ŝt+1 ) = 3, the step is
trative examples of the graph-based metrics used                  distance-optimal. A valid step leading to a state
with d(ŝt+1 ) = 5 is considered a valid it is non-        Student Prompt
optimal.                                                   Role: You are a Student in an undergraduate
E.3    Derivational Depth                                  Discrete Structures course solving a proposi-
                                                           tional logic proof. Your task is to produce the
Derivational depth measures how many missing               single most optimal next step that advances the
intermediate inference steps separate a predicted          proof toward the conclusion.
statement from the current proof state. This met-
ric distinguishes immediately derivable steps from         Task:
those that implicitly skip required reasoning and          1. Review the givens and intermediate steps.
thus cannot be derived in one sentence. Formally, if       2. Propose 2–3 candidate next steps.
for a predicted statement ϕ not present in the imme-       3. Select the candidate that most directly ad-
diate successor states of st , we define derivational         vances toward the conclusion.
depth as the minimum number of edges required to
derive ϕ from st in the KG.                                4. Justify your choice and output the selected
   Example If ϕ can be derived from st only after             next step.
two intermediate inferences, its derivational depth        Constraints:
is 2. Predictions with depth 1 correspond to di-           • Output exactly one next step in symbolic nota-
rectly derivable steps, while higher depths indicate         tion only.
premature or unsupported jumps in reasoning.               • Use only predefined inference rules (e.g., MP,
                                                             MT, Conj, DS).
E.4    Parent Statements and Rule Justification
                                                           • Parent statements must be actual expressions,
Each edge (si , sj ) ∈ E in the KG is annotated              not line numbers.
with the inference rule applied and the minimal set        Response Format:
of parent statements used in the derivation. This          • CANDIDATES: 2–3 candidate steps with brief
enables explicit verification of whether a model-            justification
generated step is justified by the available premises.
                                                           • REASONING: Why the selected step is optimal
   Example A model predicting statement C with
rule Modus Ponens must correctly identify both             • NEXT_STEP: Symbolic expression
(A → C) and A as parent statements. Predictions            • RULE: Inference rule (short name)
that produce a valid statement but fail to align with
                                                           • PARENT_STATEMENTS: Supporting expres-
the correct parents or rule are flagged as unjustified.
                                                             sions
F     Prompt Design
                                                                Figure 6: Base System Prompt for Student
This section provides the complete prompts used
for each agent in our multi-agent tutoring system.
All prompts use structured JSON response formats          F.2   Student Update Prompt
to ensure consistent parsing.
   Our prompt design translates established peda-         After receiving feedback, the Student Update agent
gogical principles into operational constraints for       simulates a learner revising their approach. The
LLM agents. Each agent’s prompt encodes spe-              prompt requires the student to: (1) identify what
cific instructional strategies grounded in learning       aspect of the feedback addresses their error, (2) gen-
science research, ensuring that generated feedback        erate revised candidates incorporating the guidance,
aligns with effective tutoring practices. We de-          and (3) produce a corrected next step.
scribe the key design decisions below.                       Critically, if the original response was marked
                                                          “Correct,” the agent responds with “No Improve-
F.1   Student Prompt                                      ments Needed” rather than artificially generating
The base system message includes the Role and             changes. This prevents the evaluation artifact of
Task information along with instructions, whereas         forced revisions when none are warranted, ensuring
the user message includes the problem instance            that measured improvement rates reflect genuine
itself. The prompt template is provided below in          learning effects. The base system prompt is pro-
Fig 6.                                                    vided in Fig 7.
 Student Update Prompt                                  Tutor Prompt
 Role: You are a Student revising your previous         Role: You are a Tutor evaluating a student’s pro-
 next-step attempt after receiving feedback on a        posed next step in a propositional logic proof,
 propositional logic proof.                             with access to the KG-derived optimal step.
                                                        Task:
 Task:
                                                        1. Analyze how the optimal step is derived (rule
 1. Review the feedback to determine whether
                                                           and parent statements).
    errors are present.
                                                        2. Evaluate the student’s candidates, reasoning,
 2. If the prior response is correct, return No
                                                           and chosen next step.
    Improvement Needed.
                                                        3. Classify the student’s step as Correct, Subop-
 3. Otherwise, revise your reasoning and pro-
                                                           timal, or Incorrect.
    pose exactly one improved next step.
 Constraints:                                           4. Provide brief, scaffolded feedback guiding
                                                           the student toward the optimal step.
 • Revise only the immediate next step; do not          Constraints:
   extend the proof.                                    • Do not reveal the optimal step, its rule, or
 • Output symbolic expressions only; use prede-           parent statements.
   fined inference rules.                               • Acknowledge what the student did correctly
 • Do not infer or reveal the full solution.              before addressing errors.
                                                        • Use Socratic questions to guide reasoning;
 Response Format:                                         keep feedback concise (2–3 sentences).
 • REVISED_REASONING: Brief reflection or No
   Improvement Needed                                   • Use predefined inference rule short names
                                                          only.
 • IMPROVED_STEP: Symbolic expression or No             Response Format:
   Improvement Needed                                   • STUDENT_ERRORS: Brief explanation or
 • BETTER_RULE: Inference rule (short name)               Correct
 • PARENT_STATEMENTS: Supporting expres-                • NEXT_STEP_CORRECTNESS:          Correct       /
   sions or No Improvement Needed                         Suboptimal / Incorrect
                                                        • TUTOR_FEEDBACK: Scaffolded guidance with-
  Figure 7: Base system prompt for student update         out answer revelation

                                                             Figure 8: Base System prompt for Tutor

F.3   Tutor Prompt


The Tutor operates under minimal hint access: it
receives only the correct next step without knowl-
edge of the complete solution path. The prompt
enforces a critical planning-before-feedback re-
quirement: the Tutor must first generate an internal   F.4   Teacher Prompt
derivation plan explaining how the correct step is
derived (identifying the rule and parent statements)
before producing student-facing feedback. This de-
sign decision ensures the Tutor develops a genuine
understanding of the solution rather than pattern-
matching, aligning with research showing that scaf-    The Teacher agent has access to the complete next
folded feedback improves instructional quality (Ser-   step and provides scaffolded feedback without re-
ban et al., 2020). The prompt is illustrated in Fig    vealing the answer. The prompt is illustrated in Fig
8.                                                     9.
 Teacher Prompt                                         responses. Its role is to provide targeted evalua-
 Role: You are a Teacher evaluating a stu-              tions and, where necessary, concise and actionable
 dent’s proposed next step in a propositional           feedback to ensure alignment with the correct logic
 logic proof, with access to the complete solution      step. This approach ensures a robust layer of ver-
 (KNOWLEDGE_BASE_STEPS).                                ification and strengthens the overall quality and
                                                        pedagogical value of the feedback offered to the
 Task:                                                  student. The prompt is illustrated in Fig 10.
 1. Compare the student’s response against the
    knowledge-base solution.
 2. Identify errors in the student’s logic, rule us-
    age, or reasoning.
 3. Classify the student’s next step as Correct,
    Suboptimal, or Incorrect.
 4. Provide brief, scaffolded feedback guiding
    the student toward the correct solution.            G     Illustrative Agent Responses
 Constraints:
 • Do not reveal the exact next step, rule, or par-
   ent statements from the solution.
 • Acknowledge correct aspects of the student’s
   attempt before addressing errors.
 • Use Socratic questions to guide reasoning;           This appendix presents representative responses
   keep feedback concise (2–3 sentences).               generated by the Student, Tutor, Teacher, and Judge
                                                        agents to concretely illustrate how each role opera-
 • Refer to the student’s candidates when rele-         tionalizes its assigned information access and rea-
   vant.                                                soning constraints. These examples are intended to
 • Use predefined inference rule short names            complement the quantitative analysis by providing
   only.                                                qualitative insight into agent behavior across the tu-
 Response Format:                                       toring pipeline. The responses are color-coded, red
 • STUDENT_ERRORS: Brief explanation or                 represents an incorrect student response or tutor-
   Correct                                              ing agent feedback, while blue represents correct
 • NEXT_STEP_CORRECTNESS:           Correct       /     responses and feedbacks.
   Suboptimal / Incorrect
 • TEACHER_FEEDBACK: Scaffolded guidance
   without answer revelation

      Figure 9: Base System prompt for Teacher


F.5   Judge Prompt                                      G.1    Student Agent Response
The Judge agent is tasked with thoroughly evaluat-
ing both the student’s and the teacher’s responses
to the logic proof problem. While the Teacher has
access to the correct step and is therefore not asked
to verify its own guidance, the Judge is specifically   We show a representative Student agent response
instructed to examine and identify any errors or        to demonstrate candidate generation, explicit rea-
inaccuracies present in both the student’s and the      soning, and next-step generation. The example
teacher’s responses.                                    corresponds to a single proof instance and high-
   Equipped with comprehensive access to the cor-       lights how intermediate reasoning is externalized
rect derivation steps from the knowledge base, the      for downstream tutoring and verification. The sam-
Judge carefully analyzes the reasoning behind both      ple response is shown in Fig 11.
                                                     Sample Instance
                                                     Givens:
Judge (Verifier) Prompt
                                                     • ((¬K ∨ L) → (M ∧ N ))
Role: You are an expert pedagogical AI               • (K → O)
Judge for propositional logic proof prob-
lems, with access to the complete solution           • ¬O
(KNOWLEDGE_BASE_STEPS). You evaluate both            Intermediates:
the student’s proposed next step and the             1. ¬K                                  (MT: 2,3)
Teacher’s feedback. Task:                            2. (¬K ∨ L)                             (Add: 4)
1. Compare the student’s response against the        3. (M ∧ N )                            (MP: 1,5)
   knowledge-base solution.                          Conclusion: N
2. Identify errors in the student’s reasoning, if
                                                     Corresponding student Response
   any.
3. Classify the student’s next step as Correct,      Candidate Steps:
   Suboptimal, or Incorrect.                         • M : potentially useful for deriving N from
                                                       (M ∧ N ).
4. Evaluate whether the Teacher’s feedback cor-
   rectly guides the student.                        • ¬M : less direct without a clear derivation.
5. Either enhance the Teacher’s feedback or          • (M ∧ N ): already derived; insufficient alone
   override it with corrected guidance.                to reach N .
Constraints:                                         Reasoning:       Applying a rule directly to
• Do not reveal the exact next step, rule, or        (M ∧ N ) is the most efficient path to the
  parent statements from the solution.               conclusion. Since (M ∧ N ) is available,
                                                     simplification yields the target.
• Acknowledge correct aspects of the student’s
                                                     Next Step: N
  attempt before addressing errors.
                                                     Rule: Simp
• Use Socratic questions to guide reasoning;         Parent Statement: (M ∧ N )
  scaffold rather than instruct.
• Override Teacher feedback if it is incorrect,
  misleading, or reveals the solution.              Figure 11: Sample problem instance and corresponding
• Keep final feedback concise (2–3 sentences)       correct student response
  and encouraging.
• Use predefined inference rule short names         G.2       Tutor Agent Response
  only.                                             This example illustrates a Tutor agent interaction
Response Format:                                    under partial solution access. The Tutor receives
• STUDENT_ERRORS: Brief explanation or              only the next step and must provide scaffolded feed-
  Correct                                           back without access to the full derivation context
• NEXT_STEP_CORRECTNESS:          Correct       /   or rule justification. The sample response is shown
  Suboptimal / Incorrect                            in Fig 12.
• TEACHER_FEEDBACK_CORRECTNESS: Assess-
                                                      Tutor Response Interaction
  ment of Teacher feedback
• JUDGE_ACTION: Enhanced or Overridden                Problem Instance (Excerpt)
                                                      • (Z → (¬Y → X))
• FINAL_FEEDBACK:       Judge-approved      scaf-
  folded guidance                                     • (Z ∧ ¬W )
                                                      • ...
    Figure 10: Base System prompt for Judge
                                                      Derived Intermediates (Excerpt)
                                                      • ¬W                       (Simplification)
  • Z                              (Simplification)                  – (J+K) by Addition from J
  • (¬Y → X)                       (Modus Ponens)                    – ...
  • ...                                                      • Reasoning: (J+K) is optimal because it di-
  Student Response                                             rectly derives ...
                                                             • ...
  • Candidates:
                                                             Teacher Hint
      – (Y ∨ X): conjunction aiming to reach
        (X ∨ Y )...                                          Derive (J+K) from J using the Addition rule.
      – ...                                                  Teacher Response
  • Reasoning: (X ∨ Y ) is optimal because it                • Next-Step Correctness: Correct
    could be obtained via Addition from either
                                                             • Student Errors: None
    X.
                                                             • Teacher Feedback: You correctly identified
  • Predicted Step: (X ∨ Y )
                                                               that Addition on J directly achieves the con-
  • Rule: Add                                                  clusion...
  • ...
  Tutor Hint
                                                           Figure 13: Teacher feedback (complete hint) on correct
  • Hint: (Y ∨ X)                                          student response
  Tutor Feedback
                                                            Teacher Reveals Solution
  • Tutor Rule: Addition
                                                            Givens:
  • Student Assessment: incorrect
                                                            • (S > D) ∨ I
  • Feedback: “You have correctly identified
                                                            • (−S ∨ Q) > Y
    the next step...”
                                                            • ¬D
                                                            • ¬D > ¬I
Figure 12: Tutor feedback (partial hint) on correct stu-
dent response
                                                            Student Response
G.3       Teacher Agent Response                            • Reasoning: MT on ¬D > ¬I and ¬D is
This example illustrates a Teacher agent with full            needed to get ¬I to be used later with (S >
derivational access, including the correct rule and           D) ∨ I for DS
parent statements. Unlike the Tutor, the Teacher            • Next Step: ¬I
can precisely diagnose suboptimal reasoning and
                                                            • Rule Used: MT
scaffold guidance using explicit structural knowl-
edge while avoiding direct answer revelation. The           Knowledge-Graph Correct Hint:
sample response is shown in Fig 13.                         Derive ¬S from (S > D) and ¬D using Modus
  Teacher Response Interaction                              Tollens (MT).
                                                            Teacher Response
  Problem Context (Excerpt)
  • (F → (G ∧ ¬H)                                           Teacher Feedback: Great job identifying the
                                                            relevant candidates! You correctly spotted that
  • (I ∧ F )
                                                            (¬D → ¬I) and ¬D could be useful, but
  • (H ∨ J)                                                 there’s a small mix-up with the rule. Recall:
  • ...                                                     MT requires a negated *consequent*, while MP
                                                            works with a *true antecedent*. How you might
  Student Response                                          use MP on (S > D) and ¬D to get ¬D.
  • Candidates
Figure 14: Teacher (complete hint) feedback reveals
solution on incorrect student response                      careful with the rules: you can’t directly use
                                                            Simp on a conditional like (S → D), think
G.4       Judge Verification Response                       about what rule you can use on (S → D) to
This example illustrates a complete tutoring inter-         turn it into a form more suitable for Simp...
action, showing how the student’s reasoning is eval-
uated by a Tutor with partial solution access, re-
                                                       Figure 15: Juge Verification Response, correcting In-
fined by a Judge with full derivational access. The    correct Tutor feedback (anchoring on incorrect student
instance highlights how verification can override      reasoning), Judge verification overriding incorrect feed-
pedagogically suboptimal feedback when the tu-         back.
tor does not produce good feedback. The sample
response is shown in Fig 15 and Fig 16.                 Judge verification helps Tutor Ambiguous
                                                        Feedback
  Judge Verification Improves Tutor Echo                Relevant Givens (subset):
  Problem Context (Excerpt)
                                                        ((¬Q+P ) → S),          (¬T ),    ((¬T ∗S) → ¬R)
  • (S → D)
  • ((¬S ∨ Q) → Y )                                     Student Response
  • ¬D                                                  • Reasoning: DS on ((¬Q + P ) → S) and
  • (¬D → ¬I)                                             (¬Q + P ) is optimal because it directly yields
                                                          S, which can combine with ¬T to form (¬T ∗
  • ...
                                                          S) and move toward deriving ¬R.
  Student Response
                                                        • Proposed Step: S
  • Candidates:
                                                        • Applied Rule: Disjunctive Syllogism (DS)
      – Simplify S → D to get ¬S
      – ...                                             Tutor Hint

  • Reasoning: ¬S is optimal because we al-             S
    ready have (S → D) from INTERMEDIATE                Teacher Feedback
    STEPS, and simplifying it to ¬S allows us to
                                                        • Tutor Rule: Disjunctive Syllogism (DS)
    construct (¬S ∨ Q)...
                                                          (echo failure)
  • Rule: Simp
                                                        • Feedback Text: Excellent reasoning! You’ve
  Tutor Hint                                              identified the most direct path to derive a key
  ¬S                                                      component. Now, how might this newly de-
                                                          rived statement interact with the other givens
  Tutor Response
                                                          to progress toward the conclusion? (ambigu-
  • Tutor Rule: Simp - echo failure                       ous and generic feedback)
  • Student Assessment: Correct                         Judge (Verifier) Response
  • Tutor Feedback: Excellent reasoning! You
    correctly identified how simplifying (S →           • Teacher Feedback Correctness: Vague
    D) helps set up the next step toward the con-       • Judge Action: Overridden teacher’s feed-
    clusion...                                            back
  Judge Verification                                    • Judge Feedback: Great job spotting that S is
  • Tutor Feedback Correctness: Incorrect                 a key component! You’re right that deriving S
                                                          brings you closer to using ((¬T ∗ S) → ¬R).
  • Judge Action: Overridden Teacher Feed-
                                                          Now, consider: which rule actually applies to
    back
                                                          ((¬Q + P ) → S) and (¬Q + P ) to derive
  • Final Judge Feedback: Great job recogniz-             S? How might this step help you connect to
    ing that you need -S to proceed! However, be          the other givens, like ¬T ?
                                                            J.1   Annotators
Figure 16: Judge Verification Response, Tutor echoes in-    Three expert annotators participated in the study.
correct student rule and generates ambiguous and vague      All annotators had at least two years of experience
feedback - Judge with full solution access helps            as teaching assistants for undergraduate Discrete
                                                            Structures and had previously served as researchers
H    Implementation Details                                 for the logic tutoring system used to generate the
Response Constraints. We standardize infer-                 dataset. This ensured familiarity with both proposi-
ence rule references using abbreviations (MP, MT,           tional logic proof strategies and pedagogical objec-
DS, HS, DeM, Impl) for consistent evaluation. The           tives of step-level tutoring.
complete list appears in Table 3.
                                                            J.2   Sample Selection
Token Limits. Rather than hard limits, we em-               We randomly sampled 10 problem instances per
ploy soft constraints via prompts (2–3 sentences).          feedback pipeline (Tutor, Teacher, and Judge), re-
                                                            sulting in a total of 40 annotated responses per
Quality Validation. Two automated mechanisms
                                                            model. Sampling includes a mix of correct, sub-
ensure data integrity: (1) zero-token outputs trig-
                                                            optimal, and incorrect student attempts. Following
ger automatic retry, and (2) responses missing re-
                                                            best practices for qualitative analysis in educational
quired JSON fields or violating constraints trig-
                                                            NLP, we used a minimally sufficient sampling strat-
ger re-prompting. Persistent failures after three
                                                            egy, increasing the sample size until inter-annotator
attempts are flagged for manual review. Across
                                                            agreement reached a stable, moderate level, Krip-
516 instances on 7 models, fewer than 3% required
                                                            pendorff’s α ≥ 0.70 across all annotation dimen-
retry.
                                                            sions.
I   Model Specifications                                    J.3   Annotation Dimensions
                                                            Each feedback response was independently anno-
       Table 5: Models used in our experiments              tated along four pedagogically motivated dimen-
 Model                    Org.   API      Context   Param
                                                            sions:
 GPT-4.1                OpenAI  OpenAI     1M         -
 GPT-o3                 OpenAI  OpenAI     1M         -     Evaluation Rubrics. Feedback was annotated
 Gemini 1.5 Pro         Google  Vertex    128K        -     along four dimensions capturing both reasoning
 Qwen-3-32B             Alibaba  Groq      32K       32B    accuracy and pedagogical effectiveness:
 LLaMA-3.3-70B           Meta    Groq     128K       70B
 Mistral Large          Mistral Mistral   256K      675B    • Mistake Identification: Whether the feedback
 Deepseek-r1-0528 Deepseek Deepinfra      128K      671B
"-" refers to undisclosed
                                                              correctly identifies errors or suboptimality in the
                                                              student’s proposed next step, including incorrect
                                                              rule use, invalid derivations, or deviations from
J   Manual Evaluation Protocol                                the optimal reasoning path.
                                                            • Correctness: Whether the feedback itself is logi-
To complement our automated metrics and bet-
                                                              cally sound and consistent with the correct solu-
ter understand qualitative differences in feedback
                                                              tion, providing guidance that does not introduce
behavior across pipelines, we conducted a man-
                                                              new errors or misleading reasoning.
ual evaluation of a representative subset of model
responses. This analysis focuses on pedagogical             • Answer Revelation: Whether the feedback ex-
properties of feedback that are difficult to capture          plicitly or implicitly reveals the correct next step,
through accuracy-based metrics alone, such as scaf-           inference rule, or parent statements, thereby re-
folding quality and answer revelation. Three do-              ducing the need for student reasoning.
main experts independently annotated 10 problem
                                                            • Actionability: Whether the feedback provides
instances per feedback pipeline (Student, Tutor,
                                                              clear, concrete, and usable guidance that a stu-
Teacher, and Judge), resulting in a total of 40 re-
                                                              dent could plausibly act on to improve their next
sponses per model along four pedagogical dimen-
                                                              attempt.
sions. We use a minimally sufficient sampling strat-
egy until inter-rater agreement exceeded a moder-           Due to the cognitive complexity of step-level logic
ate Krippendorff’s α threshold (α ≥ 0.65).                  feedback and the time cost of expert annotation,
we adopt a coarse 3-point ordinal scale (1–3) for        beyond which no automated feedback strategy is re-
all rubrics, with 1 = poor, 2 = partial, 3 = strong.     liable, suggesting the need for escalation strategies
This scale captures meaningful distinctions while        such as human intervention or extended symbolic
maintaining annotation reliability and consistency.      reasoning support in highly complex cases.

J.4   Annotation Procedure                               L    Future Directions
Annotators were provided with the problem con-           Several directions remain for future research. First,
text (givens, intermediates, and conclusion), the        validating these findings with human learners is
student’s response, and the corresponding feedback       essential to assess learning gains, engagement, and
generated by the pipeline under evaluation. An-          transfer beyond LLM-based student simulations.
notators worked independently and were blinded           Second, extending the framework to multi-turn tu-
to model identity and quantitative performance re-       toring dialogues may reveal different verification
sults. Inter-annotator agreement was measured us-        dynamics, including delayed correction or cumu-
ing Krippendorff’s α, which is suitable for ordinal      lative anchoring effects. Third, applying our ap-
data and multiple annotators. Agreement exceeded         proach to broader formal reasoning domains, such
a moderate reliability threshold across all four di-     as first-order logic or program verification, would
mensions (α ≥ 0.65), indicating consistent inter-        test its generality. Finally, developing adaptive rout-
pretation of the rubric.                                 ing mechanisms that dynamically select tutor roles,
                                                         verification depth, and solution access based on
J.5   Analysis                                           student state and problem difficulty represents a
Although qualitative and limited in scope, this          promising direction toward robust, scalable educa-
analysis reveals consistent patterns that align with     tional AI systems.
our quantitative results. Tutor feedback is typ-
ically vague but provides scaffolding, encourag-
ing reasoning without explicit solution disclosure,
whereas Teacher feedback often encodes the cor-
rect inference more directly (e.g., naming rules
or premises). Judge feedback, when applied to
noisy or overly revealing Teacher responses, tends
to over-correct or abstract guidance, reducing in-
structional specificity, mirroring the conditional
effectiveness of verification observed in our experi-
ments.

K     Design Implications for Education
Our findings have direct implications for the design
of LLM-based tutoring systems in formal reasoning
domains. First, verification should be condition-
ally deployed, not treated as a universal safeguard.
Systems should estimate upstream tutor reliabil-
ity and invoke verification primarily when error
rates are high, rather than indiscriminately. Sec-
ond, solution information access must be adaptive.
Full derivational access expands coverage to harder
states but increases the risk of premature revelation;
lightweight access is preferable in low-complexity
settings. Third, step-level reasoning alignment
is critical: feedback that is locally valid but mis-
aligned with the learner’s current proof state can
anchor incorrect reasoning and undermine learn-
ing. Finally, our results reveal a complexity ceiling
Table 6: Effects of proof complexity on correctness and feedback pipelines (Logistic Regression Coefficients,
significance: *** p < .001, ** p < .01, * p < .05)

               Model          Main Effect                        Interaction with Pipeline
                              Complexity           Tutor × Comp.    Teacher × Comp.          Judge × Comp.
                                       ∗∗∗
               GPT-4.1         −0.35                 −0.02 ns
                                                                           +0.08ns
                                                                                               +0.22∗∗∗
               GPT-o3          −0.42∗∗∗               +0.18∗               +0.13ns             +0.24∗∗
               Gemini-1.5      −0.55∗∗∗              +0.55∗∗∗              +0.65∗∗∗            +0.61∗∗∗
               DeepSeek-R1     −0.36∗∗∗              +0.28∗∗∗              +0.36∗∗∗            +0.56∗∗∗
               Qwen-3          −0.53∗∗∗              +0.33∗∗∗              +0.37∗∗∗            +0.39∗∗∗
               Mistral         −0.42∗∗∗              +0.10ns               +0.11ns              +0.21∗
               LLaMA-3         −0.30∗∗∗              −0.03ns               −0.03ns             +0.04ns




              Table 7: Feedback hurts student performance with corresponding mean complexity

                 Model                 Tutor                     Teacher                     Judge
                             Count      Complexity       Count     Complexity        Count    Complexity
                 GPT          295            3.97         200         4.61            127           4.90
                 GPT-o3       267            4.14         200         4.64            126           5.23
                 Gemini       134            4.79         109         5.73            139           4.82
                 DeepSeek     121            4.74          81         6.12            104           5.08
                 LLaMA        383            3.44         332         3.60            307           3.60
                 Qwen         218            4.50         200         4.74            182           4.74
                 Mistral      319            3.84         302         3.94            226           4.23




    Table 8: Tutor rule inference accuracy by rule type and model (%), best values are bolded across all rows

          Rule      Actual    GPT-4.1        GPT-o3     Gemini     Mistral     Deepseek      Qwen          Llama-3.3
          Simp      90          87           86           94         73           96           76             18
          Add       61          81           77           78         62           85           92             23
          MP        61          70           77           96         45           91           75             55
          DS        53          43           45           81         60           77           90             17
          MT        40          50           55           82         70           87           77             10
          Impl      38          47           52           86         65           81           54             21
          CP        36          30           33           83         10           86           58             17
          DN        31          48           58           83         38           74           12             29
           CD       27            7          11            66          3           66          55             11
           DeM      21           47          38            95         66           85          66             14
           HS       21           47          57           100         80           92          85             61
           Conj     14           92          92            92         92           83          85              0
           Comm     12           41          33            72         14            0           8             50
           Equiv    7            0           0             33        100          100           0              0
           Distr    4           100          100          100          0            0          50             50
          Overall               58.3         60.1         85.8       54.8        84.9         70.2            24
