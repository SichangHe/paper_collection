                                             Test-Driven Approaches to Software Engineering
                                                      with Large Language Models:
                                               A Survey of Phases, Tasks, and Agent Skills
                                                      Yunhao Liang1,2 , Chengguang Gan3 , Ruixuan Ying4 , Hanjun Wei2 , Zhe Cui1,2 , Shiwen Ni5
                                                               1
                                                                  Chengdu Institute of Computer Applications, Chinese Academy of Sciences, China
                                                                                   2
                                                                                     University of Chinese Academy of Sciences, China
                                                                                              3
                                                                                                Independent Researcher, Japan
                                                      4
                                                        Institute of Multidisciplinary Research for Advanced Materials (IMRAM), Tohoku University, Japan
                                                          5
                                                            Artificial Intelligence Research Institute, Shenzhen University of Advanced Technology, China
arXiv:2609.12012v1 [cs.SE] 10 Sep 2026




                                            Abstract—Tests increasingly participate in the decisions made      measures. Research on test-conditioned generation, generated-
                                         by large language models and software engineering agents.             test selection, self-debugging, and stronger evaluation suites
                                         They specify intended behavior, guide program construction and        illustrates these distinct roles [1]–[4]. Figure 1 organizes the
                                         repair, select candidates, constrain transformations, and provide
                                         execution evidence for software analysis. These uses draw on          survey around phases and mechanisms, software engineering
                                         test-driven development, yet differ substantially in test order,      tasks, agent workflows and skills, and evaluation evidence,
                                         oracle availability, editable artifacts, and the role of execution.   with the full TDD cycle as a process reference.
                                         We present a structured scoping survey organized around the              Test-driven development (TDD) offers a process-oriented
                                         question of what decision a test changes. The review integrates       way to connect requirements, implementation, and behavioral
                                         87 research and supporting records, with method- or protocol-
                                         level extraction for 83 records, alongside a separate collec-         preservation. In its Red–Green–Refactor cycle, a developer
                                         tion of five practice resources. We distinguish the Red–Green–        establishes a relevant failing test, implements enough behavior
                                         Refactor cycle from test-conditioned generation, execution-guided     to satisfy it, and improves the design while retaining passing
                                         refinement, test-mediated analysis, and evaluation-only testing.      tests [5]. LLM-based work applies parts of this reasoning at
                                         We then compare code generation, repair, translation, refac-          several scales. LLM4TDD organizes incremental generation
                                         toring, clone detection, code search, localization, training-data
                                         construction, and formal-specification validation. A dedicated        around tests; TENET prepares executable test infrastructure
                                         analysis examines how agent workflows and reusable skills encode      for repository-level generation; class-level TDD introduces
                                         testing procedures and how their effects are evaluated. Across        dependency-aware method scheduling; and TDD-Agent allows
                                         these tasks, the evidence supports treating test availability, test   tests and implementations to evolve during reasoning [6]–[9].
                                         validity, feedback use, and evaluation independence as separate       Their shared use of tests does not make their execution order
                                         properties. Test passing alone does not establish behavioral
                                         equivalence, effective feedback, or process adherence; aggregate      or oracle assumptions identical.
                                         improvements can also conceal different outcomes across models,          The connection extends beyond generating and repairing
                                         tasks, and denominators. We synthesize these distinctions into a      code. Translation can use source execution as a behavioral
                                         mechanism taxonomy, a cross-task comparison, and a protocol-          reference, as illustrated by UniTrans and TransAgent [10],
                                         sensitive evidence analysis, and identify research directions in      [11]. HyClone uses dynamic behavior to support semantic
                                         oracle validation, causal evaluation, long-horizon maintenance,
                                         and reusable test-driven agent capabilities.                          clone classification, whereas IssueExec uses test traces to
                                            Index Terms—test-driven development, large language models,        locate code relevant to an issue [12], [13]. In these analysis
                                         software engineering, code generation, program repair, agent          tasks, the immediate output may be a label or a ranked location
                                         skills, scoping survey                                                rather than a program revision. A survey restricted to whether
                                                                                                               a system writes tests before code would miss this broader role
                                                                I. I NTRODUCTION                               of executable evidence.
                                                                                                                  Reusable agent skills add another dimension. A skill may
                                           A software test can influence an LLM-generated program              instruct an agent to establish a failure, make a small edit,
                                         before the program exists, during its revision, or only after         rerun tests, and inspect regressions. The presence of those
                                         development has finished. These placements have different             instructions, however, is a different observation from their
                                         consequences. A visible input–output example can resolve              execution or their contribution to task success. SWE-Skills-
                                         an ambiguous requirement. A failing assertion can identify            Bench evaluates the marginal utility of injected skill docu-
                                         a behavior that a candidate implementation must change.               ments, while work on repository context files investigates how
                                         A regression test can reject a transformation that damages            persistent guidance changes agent behavior [14], [15]. These
                                         existing functionality. When tests are hidden and run only by         studies motivate separating the contents of a procedure from
                                         an evaluator, they instead determine what the reported score          the mechanism that executes it.
  Process reference                                     Red                                   Green                                Refactor
                                               Observe a relevant                        Implement until                       Improve structure
  Full TDD · Section II                           failing test                             tests pass                          preserve behavior

                                                                                         Next increment


                                                                    Test design / Red: intent, oracles, relevant failures
                                      Phases &                      Green: conditioning, feedback, candidate selection
                                     mechanisms                     Refactor: structural change with tested behavior retained
                                      Section III                   Cross-cycle: increments, dependencies, coevolution
                                                                    Analysis: outputs, traces, execution relationships


                                                                    Construction: generation, repair, security, optimization
                                    Software                        Transformation: translation, migration, refactoring
   TDD + LLM                    engineering tasks
     Test-driven                                                    Analysis: clone detection, code search, localization
                                    Section IV
      software                                                      Assets: training data, development tasks, formal tests
     engineering
                                 Agent workflows                    Control: prompts, workflows, agents, human collaboration
                                     & skills                       TDD Skills: content, invocation, enforcement
                                    Section V                       Agent / skill artifacts: test-driven development


                                      Evidence &                    Oracles: provenance, validity, test-edit authority
                                      evaluation                    Evaluation: test visibility, benchmarks, configurations
                                       Section VI                   Outcomes: correctness, preservation, cost, human effects


  Research agenda · Section VII
  Causal comparisons · Oracle quality · Test maintenance · Skill adherence · Long-horizon transfer

Fig. 1. Survey taxonomy and reading map. Four complementary dimensions organize the synthesis: TDD phases and test-driven mechanisms (Section III),
software engineering tasks (Section IV), agent workflows and skills (Section V), and evaluation evidence (Section VI). Tree branches denote topic membership;
individual studies can span multiple dimensions. The process reference above shows the full Red–Green–Refactor cycle defined in Section II. Section VII
brings these dimensions together in the research agenda.



   Existing surveys provide substantial foundations. Software-                  Third, it synthesizes evaluation evidence for both software
testing and test-generation reviews organize testing activities,                outcomes and agent procedures, including reusable skills. This
generation techniques, and integration strategies [16], [17].                   organization explains why a generated test can be useful for
Program-repair surveys classify repair mechanisms and test-                     one purpose yet insufficient for another, and why evidence
feedback pipelines [18], [19]. The Vibe Coding survey dis-                      of successful execution must be interpreted together with the
cusses development modes, and skill surveys organize repre-                     underlying protocol.
sentation, acquisition, retrieval, evaluation, and evolution [20]–                 Section II defines the scope and review procedure. Sec-
[22]. A critical survey of self-correction further emphasizes                   tion III develops the mechanism taxonomy, and Section IV
the source and reliability of feedback [23]. Table I compares                   compares task applications. Section V examines workflows
their organizing frameworks with the questions pursued here.                    and skills. Section VI synthesizes evaluation evidence, fol-
Our contribution is a common extraction unit across these                       lowed by the research agenda and conclusions.
perspectives: the decision changed by a test, together with
the oracle, editable artifact, and evidence of its use. This unit                     II. BACKGROUND , S COPE , AND R EVIEW M ETHOD
lets us compare a translation reference, a clone-classification
observation, and a skill-validation test without assigning them                 A. Operational Meaning of Test-Driven
the same development phase.                                                       We use test-driven approaches as an umbrella term for
   Our review makes three contributions. First, it provides                     methods in which tests influence an engineering decision.
an operational taxonomy that connects TDD phases to test-                       Within that scope, full TDD retains its narrower process
conditioned construction, feedback-guided revision, candidate                   meaning: a relevant failure precedes implementation, passing
selection, and test-mediated analysis. Second, it compares                      behavior is established, and structural improvement is checked
tasks through the artifact being changed, the origin of the                     against preserved behavior [5]. Test-first preparation is evi-
expected behavior, and the permissions available to the model.                  dence about ordering; it does not by itself establish that a
                                                              TABLE I
 P OSITIONING AGAINST EIGHT RELATED SURVEYS . E NTRIES SUMMARIZE THE INSPECTED ORGANIZING FRAMEWORKS AND POSITIVE COVERAGE . T HE
                                FINAL COLUMN IDENTIFIES THE COMPLEMENTARY QUESTION PURSUED HERE .


Related survey          Organizing framework                     Treatment of tests or feedback          Complementary question in this
                                                                                                         survey
Software testing        Testing activities and LLM               Test generation, bug analysis, repair   Which engineering decision does a
[16]                    techniques.                              and testing workflows.                  test change across tasks?
Test generation [17]    Generation pipeline, data, metrics       Quality and workflow integration of     Who supplies inputs, determines
                        and integration.                         generated tests.                        expected outputs, and may revise
                                                                                                         tests?
Program repair SLR      Models, repair scenarios, inputs and     Tests as repair inputs, feedback and    How do reproduction, patching and
[18]                    evaluation.                              correctness checks.                     non-repair uses of execution differ?
Software repair         Fine-tuning, prompting, procedural       Explicit test-feedback pipelines and    Which phase evidence and oracle
taxonomy [19]           and agentic approaches.                  benchmark protocol profiles.            assumptions transfer beyond repair?
Vibe coding [20]        Development modes and                    An explicit test-driven model and       Which Red/Green/Refactor
                        human–agent interaction.                 iterative feedback.                     activities are described and actually
                                                                                                         measured?
Agent skills            Representation, acquisition, retrieval   Skill validation, feedback and          How do TDD content, invocation,
taxonomy [21]           and evolution.                           runtime governance.                     adherence and enforcement interact?
Skill evaluation [22]   Evolution methods and benchmark          Execution feedback and task/skill       How does using a TDD skill differ
                        families.                                evaluation.                             from testing the skill artifact?
Self-correction [23]    Feedback sources and correction          External feedback, including            How do oracle reliability and
                        assumptions.                             execution, versus intrinsic             editable artifacts change the
                                                                 correction.                             interpretation of feedback?



relevant failure was observed. Likewise, repeated code refine-             3) How do tests change generation, repair, selection, stop-
ment does not establish that refactoring occurred. Refactoring                 ping, classification, retrieval, localization, annotation,
requires a structural objective in addition to a behavioral-                   and data-construction decisions?
preservation objective.                                                    4) How are testing procedures implemented as agent work-
   Several neighboring practices require separate treatment.                   flows or reusable skills, and what evidence establishes
Test-conditioned generation places examples or assertions in                   their execution and utility?
the prompt. Test-guided repair uses execution feedback after               5) Which conclusions about correctness, behavioral preser-
a candidate exists. Test-based selection ranks or rejects candi-               vation, analysis accuracy, and engineering cost are sup-
dates without necessarily editing them. Test-mediated analysis                 ported under the reported evaluation protocols?
uses outputs, coverage, or traces to decide whether programs               The extraction schema contains 33 fields covering biblio-
are related or where a change should occur. Evaluation-only             graphic identity, task, artifact granularity, phase, integration
testing assigns scores after the agent has completed its work.          mechanism, test role, test source, oracle origin, test mutability,
The same paper can contain several such configurations; the             ordering, phase evidence, evaluation isolation, experimental
classification therefore follows the experimental setting rather        setting, outcomes, human participation, and evidence location.
than the title alone.                                                   Test source and oracle origin are separate fields. An LLM
   Behavior-driven development (BDD) is relevant when be-               can generate inputs while a reference implementation supplies
havioral scenarios connect requirements to executable checks.           their expected outputs. A repository test can also be an
Exploring Behavior-Driven Development for Code Generation               inherited specification whose adequacy differs from that of
distinguishes a natural-language validation variant from a              the hidden evaluation suite.
variant that translates scenarios into tests [24]. We retain that          For phase coding, we use test design, Red, Green, Refactor,
difference: model evaluation of a scenario and execution of a           and cross-cycle activity. Test design and cross-cycle activity
corresponding test supply different kinds of evidence. Simi-            are analytical descriptors around the standard cycle. A non-
larly, compiler output is execution feedback, but a successful          development analysis task may have no direct phase assign-
compilation alone does not establish the behavioral property            ment. Unknown extraction values are distinguished from an
represented by a test.                                                  inapplicable concept and from evidence that a capability is
B. Research Questions and Coding Dimensions                             absent.
  The review addresses five questions:                                  C. Search and Source Selection
  1) Which TDD phases and neighboring test-driven mecha-                   We conducted an iterative, structured scoping review with
     nisms are operationalized in LLM software engineering?             a cutoff of September 9, 2026. Search combined public topic
  2) How do tests express expected behavior, and who gen-               queries, named-method searches, author-provided publication
     erates, validates, and modifies them?                              leads, and targeted reference tracing. Query families paired
TDD, test-first, test-guided, execution feedback, or executable     a source and reading it are tracked separately. Method-level
specifications with LLMs and individual software engineering        extraction supports claims about the reported procedure but
tasks. Task expansion included translation, migration, clone        does not imply independent reproduction or a complete audit
detection, code search, localization, optimization, specification   of every result. Abstract-level records are used for narrowly
validation, and training-data construction. Search results were     stated scope and mechanism descriptions.
followed to inspectable primary sources, including archival            For the coverage map, we recode 56 method/protocol-level
preprints, publisher pages, proceedings, and author-hosted          records with an operational or phase-specific test role. Each
papers.                                                             receives one primary task and multiple supported roles, pre-
   The retained collection contains 87 research and supporting      serving secondary tasks in the full extraction matrix. Surveys,
records. A supplemental search on September 10 used the             skill/context studies without an assigned operational test role,
same publication cutoff and added four studies on execution-        evaluator-only support, and abstract- or documentation-only
informed clone representations and skill development or rep-        records are omitted from this count. Verifier-driven revision of
resentation [25]–[28]. Its 16 query strings, domain filters, and    skill artifacts is included when explicitly described, separately
examined-candidate decisions are preserved with the earlier         from production-code phase evidence. Two test-maintenance
query logs. Retrieval used ranked web results followed by           studies remain in the review but are not counted because the
primary-source inspection; it did not produce a complete            current extraction does not establish a role within the map’s
bibliographic-database export. Consequently, retained-record        seven categories. A paper-level ledger records every inclusion,
totals describe this collection and do not estimate database re-    exclusion, and role assignment; blank cells denote unassigned
call. Five practice resources remain separate from the research     coverage rather than demonstrated absence.
records.                                                               Synthesis proceeds in three steps. We first identify the test-
   Eligibility depends on a test-to-decision relationship. Direct   to-decision relationship, then compare this relationship across
methods use tests or executable observations to influence           tasks, and finally inspect representative empirical contrasts un-
construction, modification, selection, analysis, or learning.       der their original models, datasets, and denominators. The unit
Phase-specific studies and evaluation benchmarks are retained       of quantitative comparison is an experimental configuration,
when they establish how to interpret those mechanisms, while        not a paper-wide headline. We do not pool heterogeneous pass
related surveys and skill studies provide separately coded          rates into an overall TDD effect. The accompanying artifacts
context. The working collection uses English-readable pri-          contain the consolidated review protocol, exact preserved
mary sources. Earlier code models are retained when they            query logs, candidate dispositions, extraction matrix, con-
instantiate a relevant mechanism, with their model class made       figuration notes, and claim-to-source ledger. Twelve focused
explicit. For example, FuzzTuning’s CodeBERT/UniXcoder              source checks revisit phase order, oracle access, skill inter-
experiments inform execution-based representation learning          vention and evaluation denominators; a separate comparison
rather than autonomous-agent TDD [25]. Historical non-LLM           records the inspected organizing frameworks of eight surveys.
search, unrelated skill benchmarks, and proposal-only material      These checks strengthen traceability within the existing work-
not selected for the operational comparison are excluded or         flow.
deferred in the screening ledger. The accompanying protocol            The review was conducted through a single AI-assisted
records source restrictions and unresolved candidates.              extraction workflow with iterative source checks; it has not un-
   Version handling uses stable paper identifiers and linked        dergone independent duplicate screening or coder-agreement
publication records. An updated title or publication year does      measurement. Its retrieval coverage is therefore scoped rather
not create another study. Conversely, shared abbreviations are      than exhaustive. Author-supplied leads improve recall for a
insufficient for merging: the two TDAD papers concern differ-       research line but can also concentrate attention; we apply
ent artifacts and mechanisms [29], [30]. Preprint metadata is       the same mechanism and evidence criteria to those papers
cited as archival metadata when a formal venue has not been         as to other records. These properties constrain claims about
established. Records that contain placeholder conference fields     prevalence and completeness while still permitting a traceable
are not treated as evidence of publication at that venue.           mechanism-level synthesis.
D. Extraction and Synthesis                                            III. TDD P HASES AND T EST-D RIVEN M ECHANISMS
   We assign one primary corpus role per record. The collec-
tion contains 43 records on code-construction or modification       A. Test Design and Red: Establishing the Behavioral Target
decisions, six on analysis or data-construction decisions, nine        The first question is how an intended behavior becomes
providing phase or test-asset support, ten evaluation-support       an executable obligation. In interactive generation, users can
records, 11 skill-related records, and eight surveys. These         accept, reject, or refine examples, giving the system infor-
categories organize the synthesis; they are not counts of           mation that the original description omitted. The interactive
complete TDD implementations.                                       test-driven generation study separates actual user participation
   Method- or protocol-focused passages were inspected for 83       from experiments that simulate responses using a reference
records. Three records remain supported at abstract level, and      implementation [31]. This distinction matters because refer-
one tool record relies on primary documentation. Downloading        ence access resolves questions that a user may find ambiguous
or costly to answer. BDD-style scenarios offer another rep-           role that interprets errors [43], [44]. Their common structure
resentation of intent, while security tests add properties that       is a feedback channel, but the content and recipient of that
ordinary functional examples may not expose [24], [32].               channel differ.
   Existing tests reduce the cost of constructing a target but           Feedback granularity is one source of variation. A Boolean
do not determine execution order. TENET uses a test harness           failure says that a candidate violates an obligation. An as-
around a missing repository implementation, whereas TDD-              sertion message can reveal the observed and expected values.
Agent permits generation and revision of both tests and code          A stack trace points to execution context. Basic-block states
within its workflow [7], [9]. The relevant extraction questions       and aligned source/target traces can narrow where behavior
are whether tests existed first, whether they were executable         diverged, as in RECODE and TransAgent [11], [38]. Richer
in the initial environment, and whether the observed failure          feedback can also be longer, noisier, or more expensive. Its
concerned the intended missing behavior. These questions              value must therefore be compared with the action it enables,
distinguish a declared test-first protocol from an executed Red       rather than inferred from the quantity of information returned.
step.                                                                    Candidate selection is a separate alternative to editing.
   Bug reproduction makes the validity of a failure particu-          CodeT executes generated solutions against generated tests and
larly important. LIBRO generates tests from bug reports and           uses agreement to select candidates [2]. Agentless uses vali-
integrates them into the surrounding project before ranking           dation signals within a larger localization-and-repair pipeline
candidate reproductions [33]. TDD-Bench Verified and SWT-             [45]. Search-oriented methods such as LATS and S* place ex-
Bench provide task protocols for evaluating issue-oriented            ecution into exploration, verification, or discrimination among
tests and their relationship to fixes [34], [35]. AssertFlip begins   candidates [46], [47]. Work on the exploration–exploitation
with generated passing tests and inverts their assertions to          tradeoff shows why repeatedly repairing one candidate and
construct a reproduction target [36]. Heterogeneous prompt-           sampling new candidates consume the same finite resource
ing and execution-feedback selection provide further support          in different ways [48]. A fair comparison must account for
for issue-test construction [37]. Across these approaches, an         those resources and for whether a method can recover from
uncompilable test, an environmental failure, and a failure            an initially poor search direction.
exposing the reported defect are different outcomes.                     Tests can also influence training. CodeRL learns from
   Self-generated tests introduce an additional dependency:           code-execution outcomes, Repair-R1 incorporates test and
the model may be wrong about the expected answer. RE-                 repair signals, and TransCoder-ST uses automated tests in
CODE uses agreement among generated candidates to improve             unsupervised translation training [49]–[51]. PerfRL combines
test reliability and couples this with fine-grained execution         correctness and performance signals in a small-code-model
feedback [38]. Agreement is useful selection evidence, yet            optimization setting and also filters candidates during in-
correlated candidates may share the same misconception. This          ference [52]. Training-time reference information must be
yields a general extraction rule: record who proposes the             distinguished from information exposed to a deployed agent. A
input, who determines the expected output, and what validates         model benefiting from reference-based training does not imply
that expectation. A single label such as “LLM-generated test”         that the same oracle is available when it solves a new task.
obscures these separate responsibilities.
                                                                      C. Refactor: Preserving Behavior While Changing Structure
B. Green: Conditioning, Feedback, and Selection                          Refactor introduces an objective that is not captured by
   Tests affect implementation through several mechanisms.            getting a new test to pass. A transformation should improve
In test-conditioned generation, examples constrain a model            a structural property while retaining the relevant existing
before it emits its candidate. The TGen study explicitly              behavior. RefactorAssist explicitly connects agentic refinement
separates generation without tests, generation with public            to refactoring, while SWE-Refactor and CodeTaste combine
tests, and remediation using failed tests [1]. Tests as Prompt        execution checks with structural criteria [53]–[55]. The latter
studies a setting in which executable tests themselves serve          combination is essential: leaving the program unchanged may
as generation input [39]. These configurations change the             preserve behavior but fail to perform the requested transfor-
information available to the model; an improvement does not           mation.
by itself identify whether the benefit comes from a test-first           Behavioral preservation remains conditional on the ob-
process or from a more informative specification.                     servations made. Differential fuzzing compares original and
   Execution-guided revision begins after a candidate exists.         transformed programs on additional inputs and exposes dis-
Self-Debugging studies feedback and explanation configura-            crepancies missed by existing suites [56]. These discrepancies
tions, while conversational repair repeatedly exposes failures        refute equivalence for the observed cases; the absence of a
to a model [3], [40]. Self-Edit makes this relationship explicit      discrepancy over a finite run has a weaker meaning. Conse-
through generation, execution on example tests, and a fault-          quently, a review should describe test passing as evidence of
aware editor [41]. ContrastRepair instead constructs contrast-        tested behavior, rather than silently replacing it with universal
ing test-case pairs to make the relevant behavioral distinction       equivalence.
more informative [42]. RePair uses process-based feedback,               The object of refactoring also matters. Automated Unit Test
and INTERVENOR separates a coding role from a teaching                Refactoring changes test code, and Testing Framework Migra-
tion changes the infrastructure in which tests are expressed and   places behavior-informed learning alongside direct execution-
executed [57], [58]. These tasks improve verification assets but   based analysis, while keeping both separate from the Red–
do not directly establish that a production-code agent performs    Green–Refactor process.
the Refactor phase after each Green step. Their relevant             LLM4CBI generates and validates witness programs whose
invariants may concern assertion meaning, setup behavior,          execution spectra support compiler-bug localization [71].
or framework semantics rather than application functionality       SWE-Flow instead uses runtime dependency information to
alone.                                                             construct development tasks and training examples [72]. These
                                                                   examples broaden the interpretation of a test beyond an
D. Cross-Cycle Organization and Coevolution
                                                                   assertion returning pass or fail. The useful evidence can
   A test-driven process must choose an increment. Function-       be an output relationship, a coverage set, a trace hierarchy,
level methods can often consider a compact interface, whereas      or a dependency relation. Their shared contribution is to
class-level generation must schedule methods whose depen-          connect language-based reasoning to an observable property
dencies affect one another [6], [8]. AgentCoder divides pro-       of software execution.
gramming, test design, and execution into roles. AlphaCodium
organizes code generation into a flow, and Reflexion carries          IV. C ROSS -TASK A PPLICATIONS AND C OMPARISON
verbal feedback across attempts [59]–[61]. These designs
differ in where state is retained and how failed attempts affect   A. Code Generation, Requirements, and Security
subsequent actions.
   Agentic repair provides more flexible control. ThinkRepair,        Generation begins with an incomplete behavioral descrip-
RepairAgent, and AutoCodeRover use different combinations          tion and produces an implementation. The main uncertainty is
of reasoning, tools, and execution within repair workflows         which program the description permits. Function-level studies
[62]–[64]. TDFlow further studies workflows for test-driven        provide controlled settings for examining the contribution of
development [65]. Such flexibility increases the importance of     examples, while class and repository settings add dependen-
observing the actual sequence of actions: access to a test tool    cies, state, and environmental constraints [1], [7], [8], [39].
does not reveal whether it was used before an edit, after it, or   The unit of generation therefore affects both what a test can
only at the end.                                                   express and what must already exist for that test to execute.
   Dynamic cogeneration makes both the reproduction test              Interactive generation allows a user to clarify the intended
and the patch part of the evolving state [66]. This permits        behavior. Automated application generation instead distributes
adaptation when an initial test is inadequate, but also changes    requirements, test construction, and implementation across
the meaning of eventual success. A passing result after editing    agent roles [31], [74]. GAI4-TDD provides a tool-oriented
the test can reflect an improved specification or a weakened       integration of generative AI with TDD [75]. These forms
obligation. The distinction requires tracking what changed in      of integration expose different costs: obtaining a trustworthy
the test, why it changed, and whether independent evidence         specification may require user effort, reference access, role
still supports the original requirement.                           coordination, or additional model calls. Treating all tests as
   Long-horizon benchmarks extend this issue across releases       a free input removes an important part of the engineering
and repeated requirements. SWE-CI, SWE-EVO, and Slop-              problem.
CodeBench study maintenance or iterative evolution in which a         Behavioral specifications can add requirements that are
sequence of locally plausible changes can accumulate broader       difficult to infer from a prose prompt alone. BDDCoder
degradation [67]–[69]. They motivate evaluating a growing set      distinguishes natural-language scenarios from executable-test
of behavioral obligations, rather than treating each successful    validation, and security-specification work distinguishes func-
episode as independent of previous work.                           tional obligations from security obligations [24], [32]. The
                                                                   distinction between a model understanding a test and following
E. Executable Evidence for Analysis and Data Construction          its rule is equally important. The paired-intervention study
   Not every test-mediated decision belongs to a development       holds inputs fixed while changing expected outputs between
cycle. HyClone uses outputs from shared inputs to inform           two compatible specifications, then checks generated behavior
clone classification, CoSQA+ uses execution to support query–      on unseen inputs [76]. This supplies a direct test of specifica-
code annotation, and IssueExec uses traces from relevant tests     tion use, rather than relying solely on an aggregate benchmark
to locate code [12], [13], [70]. Here the test provides evidence   score.
for a judgment. A negative classification is not a Red step, and      The relevant success criteria consequently include more than
a completed ranking is not a Green implementation.                 visible pass rate. They include behavior on unexposed inputs,
   A further distinction is whether the observation changes        joint satisfaction of functional and security requirements, and
a current judgment or the representation used for future           sensitivity to intended changes in the specification. These
judgments. FuzzTuning uses fuzzed input/output examples to         outcomes answer different questions. An agent may pass
enrich code-model inputs and learning for clone retrieval and      supplied examples without implementing the intended general
classification [25]. Its execution signal is informative without   rule, or implement the general rule while failing because the
a missing implementation or a failing requirement test. This       execution environment is incomplete.
                                                           TABLE II
    M ECHANISM TAXONOMY. E XAMPLES INSTANTIATE THE LISTED RELATIONSHIP ; INCLUSION DOES NOT ESTABLISH A COMPLETE TDD CYCLE .

Mechanism           Test-to-decision relationship           Evidence required                         Illustrative records
Red–Green–          A relevant failure precedes             Ordered observations of all three         TDD provides the reference process
Refactor            implementation; passing behavior        activities, including the reason for      [5]; phase coverage is coded
                    constrains structural improvement.      failure and the refactoring objective.    separately for each study.
Test-conditioned    Assertions or examples constrain the    Tests visible before generation;          TGen; Tests as Prompt; TENET [1],
generation          initial candidate.                      source of expected outputs.               [7], [39].
Execution-guided    A candidate’s execution result guides   Feedback channel, revised artifact,       Self-Debugging; RepairAgent;
refinement          a subsequent revision.                  stopping rule, and budget.                UniTrans [3], [10], [63].
Test-based          Executions determine which              Candidate population, selection           CodeT; interactive code generation
selection           candidate is retained.                  criterion, and oracle assumptions.        [2], [31].
Test-mediated       Outputs, coverage, or traces drive a    Mapping from execution evidence to        HyClone; CoSQA+; Issue-Exec [12],
analysis            relation, relevance, localization, or   the analysis output and its evaluation.   [13], [70].
                    annotation decision.
Evaluation-only     Tests assign a score after the agent    Test access boundary; absence of an       RepoMod-Bench; stronger functional
testing             finishes.                               iterative feedback channel in the         evaluation [4], [73].
                                                            evaluated setting.



B. Bug Reproduction, Repair, and Performance Optimization             gression.
   Repair starts from existing behavior and a request to change       C. Translation, Migration, Refactoring, and Maintenance
part of it. Tests can establish the defect, help locate relevant         Translation has a particularly useful oracle: an executable
code, guide a patch, or screen candidate fixes. LIBRO and             source program. UniTrans generates test inputs, obtains ex-
AssertFlip focus on constructing useful reproductions; SWT-           pected behavior from source execution, and uses tests in
Bench connects issue tests with fix validation [33], [35],            translation and repair [10]. TransAgent augments final-output
[36]. The reproduction itself is an engineering artifact whose        checking with fine-grained execution alignment [11]. These
executability and relevance determine the feedback available          methods can use the source to expose differences that are
to the repair process.                                                difficult to infer from target-language syntax alone. Their
   Conversational and autonomous repair differ in how they            assurance is nevertheless relative to the source behavior rep-
act on that feedback. A conversational loop can return failure        resented by the chosen inputs.
information after each proposed patch, while agentic sys-                SpecTra validates multiple specification modalities before
tems may interleave code inspection, localization, editing,           using them for translation. Static specifications and de-
and execution [40], [63], [64]. ContrastRepair changes the            scriptions can be checked by regenerating source-language
test evidence supplied to the conversation, whereas Agent-            code and executing existing tests; dynamic specifications
less emphasizes a structured pipeline and patch validation            are checked against source execution [77]. This provides
[42], [45]. Comparing these approaches requires distinguishing        an intermediate point between raw source prompting and
improvements in locating the defect from improvements in              repeated target-code repair. The tests first influence which
editing or selecting the patch.                                       specification is trusted, and that specification subsequently
   Performance optimization adds a second objective to func-          conditions translation. TransCoder-ST provides a historical
tional preservation. PerfRL uses execution-based correctness          training-oriented counterpart through test-based filtering in
and timing signals to rank optimized code [52]. A faster              unsupervised translation [51].
candidate that violates required behavior is unacceptable,               Repository migration introduces dependencies between
while an unchanged correct candidate may make no optimiza-            translation units. DepWareTrans orders batches using depen-
tion progress. This resembles refactoring in its preservation         dency information and checks the mixed-language repository
requirement but differs in its explicit performance objective.        after each translated batch [78]. Its setting relies on languages
The review therefore records the optimized property rather            that can coexist during migration. The resulting feedback can
than classifying every semantics-preserving edit as the same          identify integration failures that would be invisible when eval-
task.                                                                 uating isolated functions. Test-framework migration presents a
   The scope of regression checks is another important axis. A        different problem because the verification infrastructure itself
patch can satisfy the newly introduced failure while breaking         changes [58].
unrelated behavior. Graph-based TDAD attempts to provide                 Refactoring evaluations need both behavioral and structural
relevant regression-test context [29]. Its evaluation illustrates     criteria. SWE-Refactor checks developer-derived transforma-
why severity, incidence, and issue resolution should all be           tions, while CodeTaste combines repository tests with checks
measured: a method can reduce the number of failing tests             for requested code-pattern changes [54], [55]. Differential
without reducing the fraction of patches that cause any re-           fuzzing offers an additional observation channel when existing
suites fail to expose a semantic discrepancy [56]. These evalua-     Its pipeline distinguishes straightforward cases from cases
tions address whether a requested transformation occurred and        requiring executable validation. Tests help assess whether a
whether the observed behavior was retained; neither criterion        candidate satisfies the query, and the pipeline can repair the
subsumes the other.                                                  generated test program before making an annotation decision.
   Maintenance extends these obligations through time. SWE-             The main test-driven artifact is the relevance label. This
CI studies continuous-integration settings, SWE-EVO uses             is different from an online retrieval system executing every
release-sized changes, and SlopCodeBench examines long-              candidate for every query. Accordingly, annotation accuracy,
horizon iterative tasks [67]–[69]. In these settings, a test suite   agreement with human verification, and downstream retrieval
is both an accumulated specification and an asset that must          quality should be evaluated separately. The example also
itself be maintained. A process that succeeds on a single issue      reveals a distinct oracle problem: the test must operationalize
can still incur growing costs through redundant tests, fragile       the query correctly before it can provide evidence about the
fixtures, or changes that make subsequent tasks harder.              candidate code.
   RepoMod-Bench supplies an important evaluation bound-
ary. It uses implementation-agnostic tests through standardized      F. Issue and Compiler-Bug Localization
interfaces and hides the test suites from the agents [73]. The          IssueExec connects issue descriptions to existing tests and
tests measure modernization outcomes; their existence does           then uses their execution traces to identify relevant code [13].
not establish that they guided the agent. This contrast helps        Its motivating setting lacks failing tests: the existing tests pass
separate the quality of the evaluation from the presence of a        before the issue is resolved. Passing executions remain useful
test-driven method.                                                  because they reveal which code implements related behavior
                                                                     and how application-level operations traverse infrastructure.
D. Semantic Code Clone Detection                                        LLM4CBI uses a different signal. It generates witness-
   Clone detection asks whether two implementations represent        program variants, validates them, and collects passing/failing
related or equivalent functionality. HyClone combines an LLM         execution information for compiler-bug isolation [71]. The
judgment with dynamic comparison using generated inputs              mutated artifact is the test program; the compiler is the
[12]. Rather than requiring the model to infer equivalence           localization target. These two methods demonstrate why “test-
solely from code text, execution provides behavioral obser-          driven localization” is not one uniform protocol. They differ
vations that can confirm or challenge its initial interpretation.    in whether a failure is available, how tests are obtained, and
   The immediate decision is a code-pair label. Test gen-            which execution relationship supports the ranking.
eration must produce inputs that are meaningful for both                Localization should be evaluated at the reported granularity
programs, and the evidence depends on which behaviors                and separately from downstream repair. A better file ranking
those inputs expose. Divergent outputs can supply a concrete         may reduce search effort without guaranteeing a correct patch.
counterexample, whereas agreement on sampled inputs leaves           Conversely, an agent may repair a bug despite an imperfect
unobserved behavior unresolved. Classification precision and         ranking. Keeping these outcomes separate makes the contri-
recall therefore capture a different objective from the pass rate    bution of executable evidence easier to assess.
of a generated implementation. This task motivates retaining
software-analysis methods within the review while assigning          G. Training-Data and Development-Task Construction
them no artificial Red or Green phase.                                  SWE-Flow uses test execution to recover runtime dependen-
   Execution can also enter clone detection through the learned      cies and construct software engineering tasks [72]. Existing
representation rather than an explicit comparison of two             implementations and tests provide a basis for selecting devel-
programs’ outputs. FuzzTuning concatenates fuzz-generated            opment units, removing implementations, and creating target
input/output examples with source code when adapting Code-           changes. The resulting dataset supports model training and
BERT and UniXcoder [25]. On POJ104, the reported clone-              evaluation.
retrieval MAP@R changes from 84.29 to 92.01 for CodeBERT                This is a data-construction use of test-driven reasoning. The
and from 90.52 to 93.40 for UniXcoder. The protocol splits           recovered sequence is a synthesized development arrangement,
programming problems across training, validation, and test           rather than an observation that the original developers followed
sets. This differs from HyClone in both intervention and             TDD. Evaluation should therefore examine both the fidelity of
outcome: one learns a behavior-enriched representation for           the constructed tasks and the performance of models trained on
retrieval, while the other uses execution evidence in a pair-        them. The method also differs from rewarding a model during
wise classification procedure. Their scores therefore cannot         training or returning failed tests during inference: execution
establish which approach is more effective without a shared          information shapes the learning problem itself.
task and evaluation protocol.
                                                                     H. Formal-Specification Validation
E. Code Search and Relevance Annotation                                Tests can validate artifacts more abstract than executable
   Code search links a natural-language request to one or more       application code. Work on LLM-generated tests for Alloy
relevant implementations. CoSQA+ uses test-driven agents to          specifications examines whether generated cases expose in-
help construct a multi-choice code-search benchmark [70].            correct formalizations of natural-language requirements [79].
Its immediate contribution is a verification asset supporting       that it selected and used the testing capability. In a multi-
test-driven modeling.                                               agent system, separate role names do not establish independent
   The relevant questions concern whether a test is syn-            reasoning: roles may share a model, context, or an incorrect
tactically valid, whether it represents the requirement, and        specification.
whether it distinguishes correct from incorrect specifications.        Agent skills externalize reusable procedural knowledge. The
This places formal-specification validation close to test design    skill-authoring literature treats the skill as an artifact with an
while preserving the identity of the artifact under examination.    interface, supporting resources, and a behavioral evaluation
Evidence that an LLM generates useful tests does not auto-          process [81]. Surveys distinguish representation, acquisition,
matically establish an end-to-end process that repairs formal       retrieval, evaluation, and evolution, which operate at different
models.                                                             points in the lifecycle [21], [22]. A TDD skill can therefore be
                                                                    analyzed both as a representation of a development procedure
I. What Transfers Across Tasks?                                     and as a component selected and executed by an agent.
   Across these applications, the transferable abstraction is a
relationship between an executable observation and a decision.      B. Content, Invocation, and Enforcement
What varies is the behavioral authority behind the observation.
                                                                       A useful description of a TDD skill should identify the
Generation may rely on user examples, translation on source
                                                                    trigger, behavioral target, required ordering, allowed edits,
execution, clone detection on differential behavior, localization
                                                                    test commands or discovery process, refactoring objective,
on coverage or spectra, and formal modeling on requirements
                                                                    and stopping condition. These elements establish what the
and model checking. The authority also determines the in-
                                                                    procedure asks the agent to do. They do not alone establish
terpretation of failure: it can be a violated requirement, a
                                                                    that the environment prevents deviations. A natural-language
source/target discrepancy, an irrelevant candidate, or a useful
                                                                    instruction to observe a failure and an external check that
witness.
                                                                    blocks an edit have different operational consequences.
   Table III summarizes these differences. A workflow trans-
                                                                       The five practice resources illustrate substantive differences
fers successfully only when it preserves the meaning of the test
                                                                    in what a TDD skill prescribes. The Superpowers and Addy
and the decision it informs. Reusing the same prompt sequence
                                                                    Osmani documents include an explicit Red–Green–Refactor
across tasks without adapting the oracle can preserve the
                                                                    sequence [82], [83]. The inspected Matt Pocock document
appearance of TDD while changing its substantive guarantee.
                                                                    instead assigns refactoring to a separate review stage and uses
   Figure 2 summarizes the resulting coverage by primary task
                                                                    a Red–Green loop with one behavioral slice at a time [84]. The
and test role. Of the 56 mapped records, 24 primarily address
                                                                    label TDD thus does not uniquely determine phase coverage
generation and 15 address repair or reproduction. Feedback-
                                                                    even among written skill protocols.
guided revision is prominent in these groups, whereas the
                                                                       Superpowers’ skill-authoring guide applies test-driven rea-
analysis rows concentrate on execution-supported judgments.
                                                                    soning to instruction development: observe undesired agent be-
The small analysis groups describe the composition of this
                                                                    havior without the skill, write the skill, and assess the changed
collection; they do not establish exhaustive coverage or the
                                                                    behavior [85]. Probity describes operation-level checks that
size of an unexplored field. Training and data construction
                                                                    can block actions, placing enforcement outside the skill text
form a separate column because an execution-derived learning
                                                                    [86]. These are design descriptions, not independently re-
signal need not be available as feedback during deployment.
                                                                    produced effectiveness results. The inspected documents are
        V. AGENT W ORKFLOWS AND TDD S KILLS                         dated snapshots of mutable repository content; their procedural
                                                                    claims should not be generalized to every version.
A. Who Controls the Procedure?                                         Repository context files provide relevant comparative ev-
   The integration mechanism determines whether testing is          idence. Evaluating AGENTS.md studies conditions with no
optional, prescribed, or enforced. A prompt can request a           context file, model-generated context, and developer-provided
sequence of actions. A fixed workflow can schedule those            context, together with traces of testing and exploration [15].
actions externally. An autonomous agent can choose tools and        Its results show why behavior and utility need separate mea-
decide when to stop. A multi-agent design can assign test           surement: instructions can increase test execution and tool use
generation and implementation to different roles. Human col-        without a corresponding improvement in issue resolution. Skill
laboration adds another source of decisions about requirements      presence, invocation, adherence, and benefit are successive
and acceptable changes. Application-generation, repair, and         properties to observe, rather than interchangeable descriptions
workflow studies instantiate different combinations of these        of the same event.
choices [59], [63], [65], [74], [80].                                  Graph-based TDAD demonstrates a more specific interven-
   This distinction affects how a test-driven method should         tion. It combines test-oriented guidance with information about
be evaluated. For a fixed orchestrator, the relevant questions      impacted tests and code relationships [29]. The design question
include whether the scheduled test is executable and whether        is consequently broader than whether the instruction says “use
the returned feedback changes the next candidate. For an            TDD”: it also concerns whether the agent receives the test
autonomous agent, the evaluation must additionally establish        context needed to act on that instruction. Comparing text-only
    Coded test roles across primary tasks
    56 records · One primary task per record · Multiple roles permitted

           Primary task (records)                Specify Reproduce Feedback Candidate Preserve Analysis Training /
                                                behavior   failure  revision filtering behavior judgment  data

                       Generation (24)               12             1             20               6             —              —               1

          Repair / reproduction (15)                 1              8              7               4              3              1              2

          Translation / migration (5)                2              —              3               2              4              1              1

      Refactoring / optimization (2)                 —              —              1               1              2             —               1

                   Clone detection (2)               —              —              —              —              —               2              1

                Search annotation (1)                —              —              1              —              —               1              —

                        Localization (2)             —              —              —              —              —               2              —

            Data / specs / agents (5)                2              —              3               1             —               2              1

    Recorded papers                 1            5            10          20

    — No assigned role in this extraction; counts do not measure effectiveness or complete TDD adherence.


Fig. 2. Coverage of coded test roles across primary tasks in 56 method/protocol-level records. Each record has one primary task and may contribute to several
columns; row totals therefore cannot be recovered by summing cells. Counts include only roles supported by the current extraction, with per-cell paper IDs
supplied in the accompanying data. Dashes indicate no assigned role, not absence in the field. Training/data signals are distinguished from execution feedback
used during revision. The map describes the retained collection rather than effectiveness or complete TDD adherence.



guidance with guidance plus retrieved execution context can                     the tdd-workflow row reports one, one, and four solved
isolate this difference.                                                        tasks out of ten for no skill, full skill text, and the adapter,
                                                                                respectively. The ten-task subset differs from the 14-task
C. Effectiveness, Cost, and Optimization
                                                                                Haiku 4.5 comparison above, and the runtime cost measure is
   SWE-Skills-Bench reports different outcomes for two                          per-step tokens with offline synthesis and training excluded.
TDD-related skills. With Claude Code and Haiku 4.5, the                         This result concerns how a given procedure is represented
tdd-workflow condition changes pass rate from 21.4% to                          and activated; the experiment supplies the skill identity and
28.6% on 14 tasks and increases average token cost from 83K                     does not establish retrieval accuracy or Red–Green–Refactor
to 148K. The springboot-tdd condition changes pass rate                         adherence.
from 80.0% to 70.0% on ten tasks while reducing tokens from                        Guardrails Beat Guidance supplies another relevant distinc-
374K to 236K [14]. These are small, setting-specific contrasts.                 tion: the content of an instruction and the effect of adding
They establish neither a universal benefit nor a universal cost                 instructional context need not coincide [90]. Its controlled
penalty for TDD skills.                                                         analysis uses a selected discriminative task subset and rule-
   SkillsBench provides broader task coverage, and SkillMOO
                                                                                content comparisons. Such findings motivate matched controls,
examines multi-objective optimization of skills [87], [88].
                                                                                but their scope should remain tied to the evaluated selection
These studies support evaluating multiple outcomes but cannot
                                                                                and agent configuration. A generic rule-file benefit cannot
be directly substituted for a TDD-specific treatment compari-
                                                                                identify which part of a TDD procedure caused an improve-
son. Inside the Skill Market characterizes the activities repre-
                                                                                ment.
sented in skill collections rather than testing the effectiveness
of every skill it observes [89]. Corpus prevalence, benchmark
                                                                                D. Developing Agent and Skill Artifacts with Tests
utility, and optimization results therefore belong to different
evidence categories.                                                               Testing can also be used to construct the agent artifact itself.
   Skill representation is another intervention variable. Skill-                Test-Driven AI Agent Definition introduces roles for deriving
to-LoRA replaces the runtime body of a selected skill with a                    behavioral tests, revising system prompts, and assessing tests
skill-specific adapter trained from synthetic, skill-conditioned                through behavioral mutations [30]. Its evaluation separates vis-
demonstrations [26]. In its Qwen3.6-27B/OpenCode setting,                       ible and hidden behavior and includes specification evolution.
                                                               TABLE III
       C ROSS - TASK COMPARISON OF THE DECISION CHANGED BY TESTS . O RACLE AVAILABILITY AND THE EDITED OBJECT DIFFER ACROSS TASKS .

Task               Decision and object                     Typical oracle or observation             Central distinction
Code               Construct, revise, or select a          Supplied assertions, generated tests,     Test-first access versus observed Red;
generation         candidate implementation.               or human-confirmed outputs.               visible satisfaction versus hidden
                                                                                                     correctness [1], [6], [8], [31].
Program repair     Reproduce an issue, localize a          Issue text, repository tests, generated   Test relevance versus patch
                   change, revise a patch, or stop.        reproduction tests.                       correctness; product edits versus test
                                                                                                     edits [33]–[35], [63], [65].
Translation and    Accept or repair a target program or    Source execution, shared inputs,          Source-derived behavior versus
migration          migrated test.                          compilation, specifications.              platform-dependent semantics [10],
                                                                                                     [11], [51], [58], [77].
Refactoring        Accept a structural change or improve   Regression suite and differential         Passing existing tests versus
                   test assets.                            execution.                                behavioral preservation; product
                                                                                                     versus test refactoring [53], [54],
                                                                                                     [56], [57].
Clone              Decide whether programs exhibit         Shared-input output comparison or         Pairwise judgment versus learned
detection          sufficiently similar behavior.          fuzz-enriched code representations.       retrieval; neither establishes universal
                                                                                                     equivalence [12], [25].
Search and         Validate code–query relevance or        Tests that operationalize a query.        Offline annotation versus an online
annotation         construct labels.                                                                 retrieval mechanism [70].
Localization       Rank issue-related locations or         Coverage, execution traces, or            Localization evidence versus a
                   compiler behaviors.                     compiler test behavior.                   subsequent repair loop [13], [71].
Data and           Retain training examples, optimize      Execution filters, rewards, solvers,      Retrospective task construction versus
specification      programs, or revise formal artifacts.   and behavioral properties.                observed TDD; solver validity versus
                                                                                                     requirement validity [52], [72], [79].



The object undergoing revision is the system prompt, not the           qualitative case demonstrates what changes in a skill, but
production-code implementation.                                        does not provide a separate average effect for that skill.
   This reverses the usual relationship: a test-driven procedure       Moreover, the optimizer can access a reference trajectory and
is used to improve the definition of an agent that will later          benchmark feedback. On the skill benchmarks, one instance
execute tasks. The approach is relevant to skill engineer-             is used to construct the skill before evaluation across that
ing because both concern reusable behavioral instructions.             task’s instances; the separately reported held-out GAIA and
However, transfer to a specific SKILL.md package requires              EarthBench splits answer a different transfer question.
an evaluation of that artifact’s invocation and use. The two              Together, these approaches expose two levels of testing:
TDAD studies in this review accordingly remain distinct: one           tests can govern the code-producing agent’s behavior, or
addresses regression control in code editing, while the other          evaluate the reusable artifact that conditions that behavior.
addresses construction of tool-using agent definitions.                A successful package test, a useful instruction rewrite, and a
   Test-driven skill development now includes edits to pack-           correctly repaired repository are outcomes at different levels.
aged instructions and helper code. MUSE-Autoskill describes            Reporting the link between them requires both artifact-level
creating a skill package, running its local tests, revising it on      validation and task-level evidence.
failure, and registering it for reuse [28]. Its package audit
                                                                               VI. E VIDENCE , E VALUATION , AND VALIDITY
reports a tests/ directory in 9% of generated packages,
so the described gate and observed package coverage must               A. What Does Each Benchmark Establish?
remain separate. The generation experiment also distinguishes             Benchmarks observe different parts of the proposed process.
35 tasks that yield a skill from the full 51-task population: the      HumanEval, MBPP, and their expanded tests primarily assess
reported conditional score is 87.94%, while the full-population        the behavior of generated functions. EvalPlus demonstrates
score is 60.35%. Skills are created from successful runs and           how strengthening the evaluation suite can expose failures that
re-evaluated on the same tasks. These measurements charac-             the original tests miss [4]. A passing candidate is consequently
terize generation coverage and reuse; new-task generalization          evidence relative to an oracle and input set. It is not a direct
requires a different evaluation.                                       measure of the procedure that produced the candidate.
   SKILLER optimizes textual skill bundles through verifier-              Issue-level test benchmarks ask a different question. TDD-
grounded feedback while keeping the executor model fixed               Bench Verified and SWT-bench evaluate whether a generated
[27]. A critic interprets trajectories and verifier diagnostics,       test distinguishes an unresolved issue from a repaired version
and an actor changes instructions or task-local helpers. Its           [34], [35]. They can establish the relevance of a reproduction
selected springboot-tdd example illustrates successive                 test without establishing that an agent subsequently repaired
edits to exploration budgets and artifact consistency. This            the issue. Conversely, a repair benchmark can establish issue
resolution without showing that the agent first constructed          on SALLM, but from 15.6% to 40.0% on CWEval [32]. The
a failing test. A study must observe both transitions before         SALLM and CWEval conditions contain 11 and nine tasks,
attributing the result to a complete test-first repair cycle.        respectively, each repeated with five seeds. The direction of the
   Tests as Prompt, CodeTaste, and RepoMod-Bench further             contrast therefore depends on the benchmark. Joint correctness
illustrate differences in test access [39], [55], [73]. When tests   should remain separate from functional correctness and from
are supplied to the model, performance measures its ability          a security-only score, especially when repair can improve one
to satisfy an available executable specification. Hidden tests       dimension while damaging another.
instead assess generalization beyond the checks available dur-          Table V applies a common schema to 16 studies selected for
ing construction. RepoMod-Bench evaluates modification with          task and mechanism diversity. It makes visible two distinctions
tests that do not supply an iterative agent feedback channel. Its    that aggregate performance tables can obscure: a test’s source
results therefore inform task difficulty and evaluation design,      can differ from the authority behind its expected output,
rather than the effectiveness of an execution-guided loop.           and the ability to revise tests can differ from the ability to
   InterCode makes interactive execution an explicit part of         revise code. The phase column preserves evaluator-only and
the coding environment, allowing evaluations to observe ex-          configuration-dependent evidence and leaves unestablished
changes between an agent and executable feedback [91]. This          properties open. In particular, generated-test selection, code
setting complements terminal correctness scores by exposing          repair, and system-prompt revision should not acquire identical
the interaction that produced the result.                            phase labels merely because all three use execution.
   Long-horizon settings add another dimension. SWE-
CI, SWE-EVO, and SlopCodeBench evaluate sequences of                 C. Test Availability, Validity, and Use
changes in which existing behavior and later requirements
can interact [67]–[69]. Their contribution to this survey is            Three questions recur across these evaluations. First, are
the opportunity to observe accumulated regressions and main-         the relevant tests available to the model? Second, are their
tenance behavior. Success on a single isolated change does           expected outcomes trustworthy and discriminative for the
not determine how test assets, dependencies, or earlier design       intended behavior? Third, does the model use their information
decisions affect the next change.                                    when making a decision? Better scores after adding tests can
                                                                     combine effects from additional specification content, addi-
B. Comparisons Depend on the Experimental Configuration              tional computation, candidate selection, and feedback-driven
   Table IV retains representative comparisons at the configu-       revision. A test/no-test comparison alone cannot separate these
ration level. The rows illustrate different evidential questions;    mechanisms.
their metrics are not pooled. A change in pass rate, the fraction       Do LLMs Really Follow Tests? studies test use through
of affected tests that fail, and success in following a changed      paired behavioral rules [76]. Its revised protocol uses 20 task
test rule have different denominators and meanings.                  families with six realizations per family, repeated under several
   Graph-based TDAD provides a particularly instructive con-         checkpoints. Qwen3.6-27B follows an explicit description of
trast [29]. On its 100-task Phase 1 subset with Qwen3-Coder-         each rule at 100% in the reported control conditions, while
30B, the baseline, TDD guidance, and graph-augmented TDD             its paired test-driven switching rate is 60.6%, with a family-
conditions resolve 31%, 31%, and 29% of tasks. Their test-           bootstrap interval of [43.1, 76.7]. This contrast distinguishes
level regression rates are 6.08%, 9.94%, and 1.82%, respec-          competence to implement a rule from reliably inferring and
tively. The corresponding evaluated test counts differ: 9,245,       switching to that rule from tests. The family structure and un-
8,040, and 8,536. The study’s instance-level regression rates        certainty also matter: repeated realizations are not independent
do not exhibit the same reduction. The evidence thus supports        evidence for hundreds of unrelated task families.
a reduction in the reported test-level failure proportion under         The same separation applies to repair. A failure report can
the graph-augmented condition, not a general increase in issue       be informative while still being ignored, misinterpreted, or
resolution or a corresponding reduction in the fraction of           overfit. Self-Repair, Self-Edit, INTERVENOR, and work on
regressing instances.                                                LLM self-correction examine different forms of revision and
   SpecTra supplies a second contrast at a smaller scale [77].       external evidence [23], [41], [44], [92]. These studies should
In its GPT-4o case study on 24 functions from GNU coreutils          be compared through their feedback channels and budget
cat, the baseline, simultaneous use of all specification modal-      controls. An apparent repair gain may partly reflect another
ities, and staged SpecTra procedure produce 10, eight, and           sampling opportunity; conversely, an ineffective loop may
11 accepted first-candidate translations, respectively. These        reflect a weak oracle rather than a general inability to revise
counts describe one project case with a bounded compiler-            code.
repair procedure. They suggest that the arrangement of speci-           Oracle validation becomes especially important when both
fication information matters, while providing limited grounds        programs and tests are generated by related models. Agree-
for predicting effects across repositories or language pairs.        ment can reflect a shared interpretation error. Reference ex-
   Security-oriented tests can also have setting-dependent ef-       ecution, human confirmation, behavioral mutation, and inde-
fects. In SecTDD’s Qwen2.5-Coder-7B results, providing all           pendently constructed evaluation tests provide different checks
tests changes hidden joint correctness from 45.5% to 41.8%           on that agreement [2], [30], [31]. None is interchangeable with
                                                             TABLE IV
 S ELECTED CONFIGURATION - LEVEL CONTRASTS . VALUES ARE REPORTED WITHIN THEIR ORIGINAL SETTINGS ; PERCENTAGES ACROSS ROWS ARE NOT
                                                      COMPARABLE EFFECT SIZES .


Study            Setting and comparison         Reported outcome                                Scope of inference
SWE-Skills-      Claude Code / Haiku 4.5;       Pass rate: 21.4% → 28.6%; tokens: 83K →         Small skill-specific sample; increased pass
Bench [14]       tdd-workflow; 14               148K.                                           rate accompanies increased cost.
                 tasks; no skill → skill.
SWE-Skills-      Same agent/model;              Pass rate: 80% → 70%; tokens: 374K →            A distinct task subset; not a repeated
Bench [14]       springboot-tdd; 10             236K.                                           estimate of the preceding skill’s effect.
                 tasks; no skill → skill.
Skill-to-LoRA    Qwen3.6-27B/OpenCode;          Solved tasks: 1 / 1 / 4 of 10.                  Selected subset; runtime per-step token cost
[26]             tdd-workflow; no                                                               excludes offline synthesis/training. No
                 skill / full text / adapter.                                                   phase-adherence outcome.
Graph-based      Qwen3-Coder-30B; 100           Resolution: 31 / 31 / 29%; test regression:     Evaluated test totals differ; test-level and
TDAD [29]        tasks; baseline / TDD /        6.08 / 9.94 / 1.82%.                            instance-level regression have different
                 graph + TDD.                                                                   behavior.
SpecTra [77]     GPT-4o; 24 cat                 Accepted first-candidate translations: 10 / 8   One project case; includes the study’s
                 functions, C → Rust;           / 11 of 24.                                     bounded compiler-repair procedure.
                 baseline / all modalities /
                 staged method.
SecTDD [32]      Qwen2.5-Coder-7B;              Hidden joint correctness: 45.5% → 41.8%.        Joint functional/security outcome in this
                 SALLM (11 tasks, five                                                          benchmark and configuration.
                 seeds); B0 (no tests) →
                 B3 (all tests).
SecTDD [32]      Same model; CWEval             Hidden joint correctness: 15.6% → 40.0%.        Direction differs from SALLM; task/model
                 (nine tasks, five seeds);                                                      strata must remain visible.
                 B0 → B3.
Follow Tests     Qwen3.6-27B; 20                Explicit A/B: 100% each; paired switch:         Different measures diagnose capability
[76]             families, 120 paired           60.6%, interval [43.1, 76.7].                   versus test use; uncertainty is bootstrapped
                 realizations; explicit-rule                                                    by family.
                 controls versus
                 test-driven switching.



a larger number of generated assertions: more assertions can               These distinctions suggest a common reporting core: the
repeat the same missing assumption.                                     editable artifacts; test and oracle origins; observed phase tran-
                                                                        sitions; visible and hidden evaluation access; task, attempt, and
D. Behavioral Preservation and Human Outcomes                           test denominators; execution and token budgets; unsuccessful
   Behavioral preservation calls for measurements beyond                or excluded attempts; and the uncertainty attached to the
passing the existing suite. Differential fuzzing of LLM refac-          comparison. Studies can then add task-specific outcomes, such
toring examines a filtered set of 3,538 refactorings from 4,368         as classification quality for clone detection or semantic preser-
generated candidates and reports non-equivalent transforma-             vation for translation. Such reporting makes an intervention
tions missed by existing tests [56]. The filtering step defines         interpretable without imposing one success metric on every
the evaluated population. Results for compilable, executable            software engineering task.
candidates should not be silently presented as results for every
generated attempt. The conditional fraction of non-equivalent           E. Cross-Study Findings and Their Implications
cases missed by tests likewise differs from a failure rate over
all transformations.                                                         a) Test order, information and feedback are distinct in-
   For human collaboration, correctness, effort, and experience         terventions: TGen separates supplying tests from remediation,
should be reported separately. Interactive code generation              CodeT uses execution for selection, and the paired-rule study
includes both a real-user study and larger evaluations with a           measures whether a model changes its program when the
reference-based user proxy [31]. The proxy supplies useful              behavior specified by tests changes [1], [2], [76]. Together
controlled answers but does not model all the uncertainty,              they show why a test/no-test score difference cannot identify a
effort, or misunderstanding of a developer. GAI4TDD and                 complete TDD mechanism: the difference may reflect a clearer
the exploratory TDD interaction studies add tool and human-             target, selection among more candidates, or revision after
workflow perspectives [75], [80], [93]. The latter compare              a failure. Conversely, a method can obtain useful execution
small groups and distinct interaction arrangements; their find-         evidence without observing Red, as in passing-test localization
ings motivate further study without establishing a population-          [13]. The practical consequence is to evaluate test availability,
wide productivity effect.                                               action order, feedback use and final correctness separately. The
                                                               TABLE V
R EPRESENTATIVE STUDIES UNDER A SHARED EXTRACTION SCHEMA . S IXTEEN RECORDS WERE SELECTED FOR MECHANISM AND TASK DIVERSITY, NOT
  AS A RANKING . P HASE CODES DESCRIBE PRODUCTION - CODE R/G/F EVIDENCE ; ANALYSIS AND AGENT- DEFINITION ACTIVITIES RETAIN THEIR OWN
                                                           ARTIFACT TYPES .


Study / primary task Tests and expected-output authority              Test modification        R/G/F                Evaluation boundary
TGen [1]                  Public benchmark tests; supplied            Supplied tests fixed U / M / U                Public/private check in the
Generation                expected outputs                                                                          designated configuration
TENET [7]                 Repository tests; repository oracle         Selected subset;         M/M/U                Agent subset; harness sees full suite
Repository                                                            edit rights U
generation
Class-level TDD [8]       Public class tests; benchmark oracle        Public tests fixed       U / M / NA           Private tests assess generated classes
Class generation
TDD-Agent [9]             Generated tests; model-inferred             Code and tests           U/M/U                Self-tests during reasoning; final
Generation                outputs                                     mutable                                       project tests
CodeT [2]                 Generated tests; execution consensus        Separate generated       NA / NA / NA         Development selection and
Candidate selection                                                   test pool                                     benchmark scoring separated
TDD-Bench Verified        Generated issue tests; buggy/fixed          Test generation; no      E / NA / NA          Gold patch hidden in main condition
[34]                      comparison                                  code repair
Bug reproduction
Dynamic                   Generated reproductions;                    Workflow-                C / M / NA           Joint correctness separated from
cogeneration [66]         independent fix/test assessment             dependent                                     self-consistency
Repair
TDFlow [65]               Human/generated reproductions;              Reproductions            M / M / NA           Human-gold and generated-test
Repair                    repository regression tests                 locked after                                  conditions differ
                                                                      creation
UniTrans [10]             Generated inputs; source-execution          Test-edit rights U       U / M / NA           Generated development and
Translation               outputs                                                                                   benchmark tests separated
SpecTra [77]              Existing/generated tests;               Test-edit rights U           U / U / NA           Specification validation uses tests;
Translation               source-execution validation                                                               holdout status varies
RefactorAssist [53]       Project tests; original tested behavior Code changes; test           NA / M / M           Independent stronger behavior
Refactoring                                                       rights U                                          checks U
HyClone [12]              Generated inputs; differential          Input generation;            NA / NA / NA         Code-pair classification; test
Clone detection           program outputs                         later edits U                                     independence U
CoSQA+ [70]               Query-derived tests; human-checked Test-program repair               NA / NA / NA         Label checking differs from retrieval
Search annotation         label subset                            allowed                                           evaluation
IssueExec [13]            Passing repository tests; execution     Test-edit rights U           NA / NA / NA         Localization output; test
Localization              traces                                                                                    independence U
Graph-based TDAD          Repository tests; impacted-test map     Code changes;                U / M / NA           F2P/P2P outcomes;
[29]                                                              static test map                                   configuration-dependent access
Regression-aware
repair
Agent-definition          Behavioral tests; execution assertions Prompt revised;               NA / NA / NA         Visible/hidden behavioral tests;
TDAD [30]                                                        test rights U                                      mutation validation
Agent definition
M: mechanism described in the method; E: established through evaluator-side comparison; C: configuration-dependent; U: not established by the current
extraction; NA: not an activity of the studied production-code process. M is not proof of universal trajectory adherence. Green denotes implementation/revision
checked against tests, not candidate selection alone. For SpecTra, validated specifications and bounded compiler repair do not by themselves establish a
behavioral test-feedback implementation loop. “Test rights U” does not imply permission to change tests. F2P/P2P denote fail-to-pass/pass-to-pass tests.



evidence supports this decomposition, rather than a universal                    of the requirement. HyClone and FuzzTuning further show that
ranking of test-first and test-after workflows.                                  behavior can support classification or representation learning
                                                                                 without proving program equivalence [12], [25]. Transfer
     b) Oracle authority determines what can transfer across                     therefore depends on the decision and source of expected
tasks: UniTrans can execute the source program to obtain a                       behavior, not just access to an execution tool.
translation reference, TiCoder can ask a user to resolve intent,
and CodeT estimates candidate quality through generated-test                           c) Outcome granularity can reverse the interpretation
agreement [2], [10], [31]. These mechanisms resolve different                    of success: Graph-based TDAD’s lower test-level regression
uncertainties. A source oracle helps preserve observed behav-                    proportion does not coincide with higher issue resolution
ior but does not supply a desired correction when that behavior                  in its Phase 1 comparison; SecTDD’s joint-correctness con-
is defective. Agreement among model-generated artifacts can                      trast changes direction across two benchmarks [29], [32].
improve selection without providing an independent account                       These are distinct outcomes and task populations, rather than
interchangeable replications of one effect. MUSE-Autoskill         [76]. Future work can connect them by measuring the be-
supplies a related selection effect: performance conditional       havioral alternatives eliminated by a test and the human or
on producing a skill has a different denominator from per-         execution cost of obtaining its expected result.
formance across all assigned tasks [28]. A review should              Oracle construction also needs to reflect task-specific asym-
retain the population and unit of each result before drawing a     metries. Translation often has an executable source program,
cross-study conclusion. Reporting task completion, behavioral      repair may have only a defect report and a partial suite,
regressions and cost together would make the engineering           and specification validation may have a solver but an un-
tradeoff more informative than any single aggregate score.         certain natural-language intention. A useful method would
     d) Skill utility depends on representation and the eval-      state which source of authority resolves disagreement. Hybrid
uation boundary: SWE-Skills-Bench exposes a written skill,         designs could use reference execution where available, ask a
Skill-to-LoRA changes its representation, SKILLER revises          human about unresolved requirements, and reserve indepen-
its contents using verifier feedback, and MUSE-Autoskill           dent checks for evaluation. This would allow test generation
validates and reuses generated packages [14], [26]–[28]. These     to express uncertainty without treating model agreement as
studies support treating skills as interventions with a con-       semantic ground truth.
struction history, not merely a present/absent feature. Their
evidence also has different access boundaries: skill identity      C. Treat Test Assets as Maintained Software
can be supplied, task feedback can guide construction, and            The corpus contains substantial work on generating tests,
a generated skill can be tested on the task that produced it.      with smaller bodies of work on test refactoring, migration,
Repeated runs, cross-agent reuse and held-out task transfer        and evolving project behavior [17], [57], [58], [67], [68].
should consequently be reported separately. For TDD, the           These activities belong to the same lifecycle. As requirements
remaining question is which representations and development        change, an inherited assertion can become obsolete, and an
procedures reliably induce the required phase transitions on       agent must distinguish an invalid test from a valid test that
new software tasks.                                                exposes a regression.
                                                                      Longitudinal evaluations could trace these decisions across
           VII. R ESEARCH G APS AND AGENDA                         successive changes. They should retain both an independent
A. Separate the Effects of Tests, Ordering, and Feedback           behavioral evaluation and a history of test edits, so that a
                                                                   passing suite can be interpreted alongside changes to its re-
   The findings in Section VI motivate decomposing interven-       quirements. Outcomes could include retained behavior, defect-
tions commonly bundled under TDD. A matched study could            revealing strength, test maintenance effort, execution cost,
hold the model, task, initial candidate, and total budget fixed    and the time spent resolving uncertain failures. The research
while varying whether tests are supplied before generation,        question is how test quality and agent behavior evolve together,
whether a relevant failure must be observed, whether execution     rather than how many tests can be generated for a fixed
feedback is returned, and whether a structural refactoring         snapshot.
objective is present. Repeated sampling with an equivalent
budget would help distinguish the contribution of feedback         D. Connect Construction and Analysis Through Execution
from that of another attempt. Such a design would estimate         Evidence
particular mechanism effects rather than an undifferentiated          Clone detection, code search, localization, and training-data
“TDD effect.”                                                      construction show that test-driven reasoning extends beyond
   Process measurement should accompany outcome measure-           modifying an implementation [12], [13], [70]–[72], [78]. This
ment. A trajectory can record when a test became available,        creates an opportunity for shared infrastructure: a validated
what failed and why, which artifact changed, and whether the       execution observation can help identify similar code, locate
accumulated suite was rerun. Failure due to an unavailable         affected behavior, choose a repair context, or construct a
dependency should be distinguished from failure that exposes       training example.
the target behavior. Refactoring should be identified through         The transfer is not automatic. A test sufficient to retrieve
its structural objective and subsequent behavioral check. These    likely examples may be too weak to establish clone equiva-
observations would make it possible to compare prescribed          lence. A compiler test useful for localizing an optimization
TDD, observed adherence, and successful completion within          issue may not express a desired source-level requirement.
the same experiment.                                               Future evaluations should therefore measure the cost and loss
                                                                   of reliability when an execution observation is reused for
B. Develop Oracles That Can Discriminate Competing Inter-          another decision. A task-spanning benchmark could expose
pretations                                                         common artifacts while maintaining distinct correctness crite-
   The test-design problem is partly an information prob-          ria for retrieval, classification, localization, and modification.
lem. A suite should distinguish plausible but incompatible
interpretations of a requirement. Interactive selection, paired-   E. Evaluate Skills as Executed Procedures
rule evaluation, and mutation-based validation already provide       TDD skills invite a layered experimental design. First,
complementary ways of investigating this property [30], [31],      validate the written artifact against its intended procedure.
Second, test whether the agent retrieves or invokes it on               The empirical evidence is configuration-dependent. Sup-
appropriate tasks. Third, inspect adherence to the required          plying tests does not ensure that a model follows them;
order and edit permissions. Finally, evaluate behavior and cost      lower test-level regression does not necessarily imply higher
on independently assessed tasks. This separates failures of skill    issue resolution; and the presence of a TDD skill does
content, selection, execution, and task competence.                  not establish adherence or utility. Future progress depends
   Matched comparisons could contrast a short prompt, a              on observing these intermediate mechanisms and evaluating
reusable skill, and an externally enforced workflow containing       them with trustworthy oracles, independent outcomes, and
the same procedural content. Additional conditions could             explicit denominators. These distinctions provide a basis for
supply relevant test context or vary the agent’s authority to edit   developing and comparing test-driven capabilities across code
tests. The mixed TDD-related results in SWE-Skills-Bench             construction, software analysis, and reusable agent procedures.
and the graph-based TDAD comparisons make these dis-
tinctions empirically relevant [14], [29]. Optimization should                                      R EFERENCES
consider correctness, regression behavior, and cost together,         [1] N. S. Mathews and M. Nagappan, “Test-Driven Development for
with evaluation tasks kept separate from those used to revise             Code Generation,” 2024, arXiv:2402.13521. [Online]. Available:
                                                                          https://arxiv.org/abs/2402.13521
the skill.                                                            [2] B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J.-G. Lou, and
   Testing the agent definition itself provides a complementary           W. Chen, “CodeT: Code Generation with Generated Tests,” 2022,
direction [30]. Behavioral tests and mutations can evaluate               arXiv:2207.10397v2. [Online]. Available: https://arxiv.org/abs/2207.103
                                                                          97v2
a prompt or skill before deployment, while task trajectories          [3] X. Chen, M. Lin, N. Schärli, and D. Zhou, “Teaching Large Language
evaluate its subsequent use. MUSE-Autoskill and SKILLER                   Models to Self-Debug,” 2023, arXiv:2304.05128. [Online]. Available:
provide concrete mechanisms for refining reusable skill arti-             https://arxiv.org/abs/2304.05128
                                                                      [4] J. Liu, C. S. Xia, Y. Wang, and L. Zhang, “Is Your Code Generated
facts, while Skill-to-LoRA changes their runtime representa-              by ChatGPT Really Correct? Rigorous Evaluation of Large Language
tion [26]–[28]. A comparison should hold procedural content               Models for Code Generation,” 2023, arXiv:2305.01210. [Online].
and executor fixed where possible, separate construction tasks            Available: https://arxiv.org/abs/2305.01210
                                                                      [5] K. Beck, Test Driven Development: By Example. Addison-Wesley
from evaluation tasks, and charge skill creation or training              Professional, 2003. [Online]. Available: https://www.informit.com/store
costs to the intended reuse horizon. This would reveal whether            /test-driven-development-by-example-9780321146533
a procedure that succeeds in its construction setting retains its     [6] S. Piya and A. Sullivan, “LLM4TDD: Best Practices for Test Driven
                                                                          Development Using Large Language Models,” 2023, arXiv:2312.04687.
benefit on new repositories.                                              [Online]. Available: https://arxiv.org/abs/2312.04687
                                                                      [7] Y. Hu, S. Liang, N. Jiang, Y. Wu, and L. Tan, “TENET:
F. Study Collaboration and Transfer Beyond Short Tasks                    One Step Toward Test-Driven Development for Repository-Level
                                                                          Code Generation,” 2025, arXiv:2509.24148v4. [Online]. Available:
   Human collaboration is central when tests clarify under-               https://arxiv.org/abs/2509.24148v4
specified requirements. Existing interaction studies establish        [8] Y. Liang, R. Ying, S. Ni, and Z. Cui, “Scaling Test-Driven Code
feasible workflows, but their task scale and participant groups           Generation from Functions to Classes: An Empirical Study,” 2026,
leave open questions about sustained adoption [31], [80],                 arXiv:2602.03557. [Online]. Available: https://arxiv.org/abs/2602.03557
                                                                      [9] H. Yu, K. Li, J. Li, H. Chai, Y. Yuan, R. He, and J. Wei, “TDD-Agent:
[93]. Longer studies should examine how developers select                 Test-Driven Reasoning for Code Generation,” 2026, arXiv:2608.16742.
tests, challenge incorrect expected outputs, review generated             [Online]. Available: https://arxiv.org/abs/2608.16742
changes, and decide when more validation is warranted. Ex-           [10] Z. Yang, F. Liu, Z. Yu, J. W. Keung, J. Li, S. Liu, Y. Hong, X. Ma, Z. Jin,
                                                                          and G. Li, “Exploring and Unleashing the Power of Large Language
perience with TDD and with AI tools may affect each activity              Models in Automated Code Translation,” 2024, arXiv:2404.14646v2.
differently.                                                              [Online]. Available: https://arxiv.org/abs/2404.14646v2
   Transfer across model families, programming languages,            [11] Z. Yuan, W. Chen, H. Wang, X. Peng, Z. Chen, and Y. Lou,
                                                                          “TransAgent: Enhancing LLM-Based Code Translation via Fine-
and repository structures should be evaluated separately from             Grained Execution Alignment,” 2024, arXiv:2409.19894v5. [Online].
within-setting optimization. A skill can depend on a test                 Available: https://arxiv.org/abs/2409.19894v5
framework or project convention that is absent in another            [12] Y. Liang, R. Ying, T. Taniguchi, G. Lyu, and Z. Cui, “HyClone:
                                                                          Bridging LLM Understanding and Dynamic Execution for Semantic
environment. A translation method can exploit a source oracle             Code Clone Detection,” 2025, arXiv:2508.01357. [Online]. Available:
that a repair task lacks. Reporting these dependencies would              https://arxiv.org/abs/2508.01357
help explain successful transfer and identify which procedural       [13] J. Liu, Y. Lin, C. Liu, Y. Qian, Y. Liu, J. Chang, W. Zhang,
                                                                          and L. Huang, “IssueExec: A Test-Driven Approach for Localizing
elements remain useful across settings.                                   Software Engineering Issues,” 2026, arXiv:2607.17286. [Online].
                                                                          Available: https://arxiv.org/abs/2607.17286
                     VIII. C ONCLUSION                               [14] T. Han, Y. Zhang, W. Song, C. Fang, Z. Chen, Y. Sun, and L. Hu,
                                                                          “SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World
   Tests influence LLM software engineering through specifi-              Software Engineering?” 2026, arXiv:2603.15401. [Online]. Available:
cation, generation, refinement, selection, behavioral compar-             https://arxiv.org/abs/2603.15401
ison, analysis, and agent control. This survey organized 87          [15] T. Gloaguen, N. Mündler, M. Müller, V. Raychev, and M. Vechev,
                                                                          “Evaluating AGENTS.md: Are Repository-Level Context Files Helpful
research and supporting records around those decisions, dis-              for Coding Agents?” 2026, arXiv:2602.11988. [Online]. Available:
tinguishing the Red–Green–Refactor cycle from neighboring                 https://arxiv.org/abs/2602.11988
uses of executable evidence. The cross-task comparison shows         [16] J. Wang, Y. Huang, C. Chen, Z. Liu, S. Wang, and Q. Wang,
                                                                          “Software Testing with Large Language Models: Survey, Landscape,
that test order, oracle origin, edit permissions, and evaluation          and Vision,” 2023, arXiv:2307.07221. [Online]. Available: https:
access determine what a reported method actually establishes.             //arxiv.org/abs/2307.07221
[17] M. Tasarsu, A. V. Tokmak, and C. Catal, “Test case generation               [36] L. Khatib, N. S. Mathews, and M. Nagappan, “AssertFlip: Reproducing
     using large language models: a systematic literature review,” Cluster            Bugs via Inversion of LLM-Generated Passing Tests,” 2025,
     Computing, vol. 29, no. 4, pp. 227–, 2026. [Online]. Available:                  arXiv:2507.17542. [Online]. Available: https://arxiv.org/abs/2507.17542
     https://link.springer.com/article/10.1007/s10586-026-06021-z                [37] T. Ahmed, J. Ganhotra, A. Shinnar, and M. Hirzel, “Heterogeneous
[18] Q. Zhang, C. Fang, Y. Xie, Y. Ma, W. Sun, Y. Yang, and                           Prompting and Execution Feedback for SWE Issue Test Generation
     Z. Chen, “A Systematic Literature Review on Large Language Models                and Selection,” in ACM/IEEE International Conference on Software
     for Automated Program Repair,” 2024, arXiv:2405.01466. [Online].                 Engineering, 2026. [Online]. Available: https://research.ibm.com/publi
     Available: https://arxiv.org/abs/2405.01466                                      cations/heterogeneous-prompting-and-execution-feedback-for-swe-iss
[19] B. Yang, Z. Cai, F. Liu, B. Le, L. Zhang, T. F. Bissyandé,                       ue-test-generation-and-selection
     Y. Liu, and H. Tian, “A Survey of LLM-based Automated Program               [38] Y. Liang, R. Ying, T. Taniguchi, C. Gan, and Z. Cui, “RECODE:
     Repair: Taxonomies, Design Paradigms, and Applications,” 2025,                   Leveraging Reliable Self-generated Tests and Fine-Grained Execution
     arXiv:2506.23749v3. [Online]. Available: https://arxiv.org/abs/2506.237          Feedback to Enhance LLM-Based Code Generation,” in International
     49v3                                                                             Conference on Intelligent Computing, 2025, pp. 510–521. [Online].
[20] Y. Ge, L. Mei, Z. Duan, T. Li, Y. Zheng, Y. Wang, L. Wang, J. Yao,               Available: https://link.springer.com/chapter/10.1007/978-981-95-001
     T. Liu, Y. Cai, B. Bi, F. Guo, J. Guo, S. Liu, and X. Cheng, “A Survey of        4-7_43
     Vibe Coding with Large Language Models,” 2025, arXiv:2510.12399v2.          [39] Y. Cui, “Tests as Prompt: A Test-Driven-Development Benchmark for
     [Online]. Available: https://arxiv.org/abs/2510.12399v2                          LLM Code Generation,” 2025, arXiv:2505.09027. [Online]. Available:
[21] Y. Zhou, W. Shu, Y. Su, W. Du, Y. Fang, and X. Lin, “A                           https://arxiv.org/abs/2505.09027
     Comprehensive Survey on Agent Skills: Taxonomy, Techniques,                 [40] C. S. Xia and L. Zhang, “Keep the Conversation Going: Fixing 162 out
     and Applications,” 2026, arXiv:2605.07358. [Online]. Available:                  of 337 bugs for $0.42 each using ChatGPT,” 2023, arXiv:2304.00385.
     https://arxiv.org/abs/2605.07358                                                 [Online]. Available: https://arxiv.org/abs/2304.00385
[22] K. Ding, Y. Zhou, C. Jin, F. Tong, M. Zhou, and D. N. Metaxas, “Agent       [41] K. Zhang, Z. Li, J. Li, G. Li, and Z. Jin, “Self-Edit: Fault-Aware
     Skill Evaluation and Evolution: Frameworks and Benchmarks,” 2026,                Code Editor for Code Generation,” in Proceedings of the 61st
     arXiv:2606.11435. [Online]. Available: https://arxiv.org/abs/2606.11435          Annual Meeting of the Association for Computational Linguistics
[23] R. Kamoi, Y. Zhang, N. Zhang, J. Han, and R. Zhang, “When                        (Volume 1: Long Papers), 2023, pp. 769–787. [Online]. Available:
     Can LLMs Actually Correct Their Own Mistakes? A Critical Survey                  https://aclanthology.org/2023.acl-long.45/
     of Self-Correction of LLMs,” Transactions of the Association for            [42] J. Kong, M. Cheng, X. Xie, S. Liu, X. Du, and Q. Guo,
     Computational Linguistics, vol. 12, pp. 1417–1440, 2024. [Online].               “ContrastRepair: Enhancing Conversation-Based Automated Program
     Available: https://aclanthology.org/2024.tacl-1.78/                              Repair via Contrastive Test Case Pairs,” 2024, arXiv:2403.01971v2.
[24] Y. Liang, C. Gan, R. Ying, and Z. Cui, “Exploring Behavior-Driven                [Online]. Available: https://arxiv.org/abs/2403.01971v2
     Development for Code Generation,” in International Conference               [43] Y. Zhao, Z. Huang, Y. Ma, R. Li, K. Zhang, H. Jiang, Q. Liu,
     on Intelligent Computing, 2025, pp. 41–51. [Online]. Available:                  L. Zhu, and Y. Su, “RePair: Automated Program Repair with Process-
     https://link.springer.com/chapter/10.1007/978-981-95-0014-7_4                    based Feedback,” in Findings of the Association for Computational
[25] J. Zhao, Y. Rong, Y. Guo, Y. He, and H. Chen, “Understanding                     Linguistics: ACL 2024, 2024, pp. 16 415–16 429. [Online]. Available:
     Programs by Exploiting (Fuzzing) Test Cases,” 2023, arXiv:2305.13592.            https://aclanthology.org/2024.findings-acl.973/
     [Online]. Available: https://arxiv.org/abs/2305.13592
                                                                                 [44] H. Wang, Z. Liu, S. Wang, G. Cui, N. Ding, Z. Liu, and G. Yu,
[26] T. Zhang and Z. Qi, “Skill-to-LoRA: From Using Skills to Learning                “INTERVENOR: Prompting the Coding Ability of Large Language
     Behaviors for Token-Efficient LLM Agents,” 2026, arXiv:2606.16769v1.             Models with the Interactive Chain of Repair,” 2023, arXiv:2311.09868.
     [Online]. Available: https://arxiv.org/abs/2606.16769v1                          [Online]. Available: https://arxiv.org/abs/2311.09868
[27] C. Dang, S. Xiong, C. He, and W. Li, “SKILLER: Language-Level
                                                                                 [45] C. S. Xia, Y. Deng, S. Dunn, and L. Zhang, “Agentless: Demystifying
     Reinforcement Learning for Reusable Skill Extraction in Small
                                                                                      LLM-based Software Engineering Agents,” 2024, arXiv:2407.01489v2.
     Language Models,” 2026, arXiv:2608.10538v1. [Online]. Available:
                                                                                      [Online]. Available: https://arxiv.org/abs/2407.01489v2
     https://arxiv.org/abs/2608.10538v1
[28] H. Lin, P. Li, J. Song, F. Jiang, and T. Zhang, “MUSE-Autoskill:            [46] A. Zhou, K. Yan, M. Shlapentokh-Rothman, H. Wang, and Y.-X. Wang,
     Self-Evolving Agents via Skill Creation, Memory, Management,                     “Language Agent Tree Search Unifies Reasoning Acting and Planning
     and Evaluation,” 2026, arXiv:2605.27366v1. [Online]. Available:                  in Language Models,” 2023, arXiv:2310.04406v3. [Online]. Available:
     https://arxiv.org/abs/2605.27366v1                                               https://arxiv.org/abs/2310.04406v3
[29] P. Alonso, S. Yovine, and V. A. Braberman, “TDAD: Test-Driven               [47] D. Li, S. Cao, C. Cao, X. Li, S. Tan, K. Keutzer, J. Xing, J. E. Gonzalez,
     Agentic Development - Reducing Code Regressions in AI Coding                     and I. Stoica, “S*: Test Time Scaling for Code Generation,” 2025,
     Agents via Graph-Based Impact Analysis,” 2026, arXiv:2603.17973v2.               arXiv:2502.14382. [Online]. Available: https://arxiv.org/abs/2502.14382
     [Online]. Available: https://arxiv.org/abs/2603.17973v2                     [48] H. Tang, K. Hu, J. P. Zhou, S. Zhong, W.-L. Zheng, X. Si,
[30] T. Rehan, “Test-Driven AI Agent Definition (TDAD): Compiling                     and K. Ellis, “Code Repair with LLMs gives an Exploration-
     Tool-Using Agents from Behavioral Specifications,” 2026,                         Exploitation Tradeoff,” 2024, arXiv:2405.17503v3. [Online]. Available:
     arXiv:2603.08806v1. [Online]. Available: https://arxiv.org/abs/2603              https://arxiv.org/abs/2405.17503v3
     .08806v1                                                                    [49] H. Le, Y. Wang, A. D. Gotmare, S. Savarese, and S. C. H. Hoi,
[31] S. Fakhoury, A. Naik, G. Sakkas, S. Chakraborty, and S. K. Lahiri,               “CodeRL: Mastering Code Generation through Pretrained Models and
     “LLM-Based Test-Driven Interactive Code Generation: User Study and               Deep Reinforcement Learning,” 2022, arXiv:2207.01780v3. [Online].
     Empirical Evaluation,” 2024, arXiv:2404.10100. [Online]. Available:              Available: https://arxiv.org/abs/2207.01780v3
     https://arxiv.org/abs/2404.10100                                            [50] H. Hu, X. Xie, and Q. Zhang, “Repair-R1: Better Test Before Repair,”
[32] Y. Liang, C. Gan, R. Ying, H. Wei, Z. Cui, and S. Ni, “Security                  2025, arXiv:2507.22853. [Online]. Available: https://arxiv.org/abs/2507
     Tests as Executable Specifications for LLM Code Generation: Benefits,            .22853
     Trade-offs, and Coverage Limits,” 2026, arXiv:2608.09740v2. [Online].       [51] B. Roziere, J. M. Zhang, F. Charton, M. Harman, G. Synnaeve,
     Available: https://arxiv.org/abs/2608.09740v2                                    and G. Lample, “Leveraging Automated Unit Tests for Unsupervised
[33] S. Kang, J. Yoon, and S. Yoo, “Large Language Models are Few-shot                Code Translation,” 2021, arXiv:2110.06773v2. [Online]. Available:
     Testers: Exploring LLM-based General Bug Reproduction,” 2022,                    https://arxiv.org/abs/2110.06773v2
     arXiv:2209.11515. [Online]. Available: https://arxiv.org/abs/2209.11515     [52] S. Duan, N. Kanakaris, X. Xiao, H. Ping, C. Zhou, N. K.
[34] T. Ahmed, M. Hirzel, R. Pan, A. Shinnar, and S. Sinha, “TDD-                     Ahmed, G. Ma, M. Capota, T. L. Willke, S. Nazarian, and
     Bench Verified: Can LLMs Generate Tests for Issues Before                        P. Bogdan, “PerfRL: A Small Language Model Framework for Efficient
     They Get Resolved?” 2024, arXiv:2412.02883. [Online]. Available:                 Code Optimization,” 2023, arXiv:2312.05657v2. [Online]. Available:
     https://arxiv.org/abs/2412.02883                                                 https://arxiv.org/abs/2312.05657v2
[35] N. Mündler, M. N. Müller, J. He, and M. Vechev, “SWT-Bench:                 [53] J. Cordeiro, S. Noei, and Y. Zou, “RefactorAssist: Agentic Refinement
     Testing and Validating Real-World Bug-Fixes with Code Agents,” 2024,             for Reliable Code Refactoring,” 2026, arXiv:2608.00924. [Online].
     arXiv:2406.12952. [Online]. Available: https://arxiv.org/abs/2406.12952          Available: https://arxiv.org/abs/2608.00924
[54] Y. Xu, J. Yang, Tse-Hsun, and Chen, “SWE-Refactor: A Repository-               Driven Development,” 2025, arXiv:2509.25297. [Online]. Available:
     Level Benchmark for Real-World LLM-Based Code Refactoring,” 2026,              https://arxiv.org/abs/2509.25297
     arXiv:2602.03712. [Online]. Available: https://arxiv.org/abs/2602.03712   [75] P. Cassieri, S. Romano, and G. Scanniello, “Generative Artificial
[55] A. Thillen, N. Mündler, V. Raychev, and M. Vechev, “CodeTaste:                 Intelligence for Test-Driven Development: GAI4- TDD,” in 2024
     Can LLMs Generate Human-Level Code Refactorings?” 2026,                        IEEE International Conference on Software Analysis, Evolution
     arXiv:2603.04177. [Online]. Available: https://arxiv.org/abs/2603.04177        and Reengineering (SANER), 2024. [Online]. Available: https:
[56] S. B. Dristi and M. B. Dwyer, “A Differential Fuzzing-Based Evaluation         //doi.org/10.1109/saner60148.2024.00098
     of Functional Equivalence in LLM-Generated Code Refactorings,” 2026,      [76] Y. Liang, C. Gan, R. Ying, H. Wei, Z. Cui, and S. Ni, “Do
     arXiv:2602.15761. [Online]. Available: https://arxiv.org/abs/2602.15761        Code Language Models Follow Tests? Paired Interventions on
[57] Y. Gao, X. Hu, X. Yang, and X. Xia, “Automated Unit Test                       Program Behavior,” 2026, arXiv:2607.26244v2. [Online]. Available:
     Refactoring,” 2024, arXiv:2409.16739v2. [Online]. Available: https:            https://arxiv.org/abs/2607.26244v2
     //arxiv.org/abs/2409.16739v2                                              [77] V. Nitin, R. Krishna, and B. Ray, “SpecTra: Enhancing the Code
[58] A. Alves, J. E. Montandon, and A. Hora, “Testing Framework                     Translation Ability of Language Models by Generating Multi-
     Migration with Large Language Models,” 2026, arXiv:2602.02964.                 Modal Specifications,” 2024, arXiv:2405.18574v3. [Online]. Available:
     [Online]. Available: https://arxiv.org/abs/2602.02964                          https://arxiv.org/abs/2405.18574v3
[59] D. Huang, J. M. Zhang, M. Luck, Q. Bu, Y. Qing, and H. Cui,               [78] S. Chand, A. Pretschner, S. Haupt, D. Zhu, and S. K. Pandey,
     “AgentCoder: Multi-Agent-based Code Generation with Iterative                  “DepWareTrans: Dependency-Aware Incremental Repository Migration
     Testing and Optimisation,” 2023, arXiv:2312.13010v3. [Online].                 across Co-executable Languages,” 2026, arXiv:2608.14128v1. [Online].
     Available: https://arxiv.org/abs/2312.13010v3                                  Available: https://arxiv.org/abs/2608.14128v1
[60] T. Ridnik, D. Kredo, and I. Friedman, “Code Generation with               [79] A. Cunha and N. Macedo, “Validating Formal Specifications with
     AlphaCodium: From Prompt Engineering to Flow Engineering,” 2024,               LLM-Generated Test Cases,” in International Symposium on Formal
     arXiv:2401.08500. [Online]. Available: https://arxiv.org/abs/2401.08500        Methods, 2026, pp. 279–297. [Online]. Available: https://link.springer.
[61] N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan,                   com/chapter/10.1007/978-3-032-26204-2_15
     and S. Yao, “Reflexion: Language Agents with Verbal Reinforcement         [80] M. Mock, J. Melegati, and B. Russo, “Generative AI for Test Driven
     Learning,” 2023, arXiv:2303.11366v4. [Online]. Available: https:               Development: Preliminary Results,” 2024, arXiv:2405.10849. [Online].
     //arxiv.org/abs/2303.11366v4                                                   Available: https://arxiv.org/abs/2405.10849
[62] X. Yin, C. Ni, S. Wang, Z. Li, L. Zeng, and X. Yang, “ThinkRepair:
                                                                               [81] G. Destefanis, “Authoring Agent Skills: A Software-Engineering
     Self-Directed Automated Program Repair,” 2024, arXiv:2407.20898.
                                                                                    Approach,” 2026, arXiv:2607.25032. [Online]. Available: https:
     [Online]. Available: https://arxiv.org/abs/2407.20898
                                                                                    //arxiv.org/abs/2607.25032
[63] I. Bouzenia, P. Devanbu, and M. Pradel, “RepairAgent: An Autonomous,
                                                                               [82] “superpowers/test-driven-development,” Repository documentation,
     LLM-Based Agent for Program Repair,” 2024, arXiv:2403.17134v2.
                                                                                    accessed September 9, 2026; mutable default-branch documentation.
     [Online]. Available: https://arxiv.org/abs/2403.17134v2
                                                                                    [Online]. Available: https://github.com/obra/superpowers/blob/main/skil
[64] Y. Zhang, H. Ruan, Z. Fan, and A. Roychoudhury, “AutoCodeRover:
                                                                                    ls/test-driven-development/SKILL.md
     Autonomous Program Improvement,” 2024, arXiv:2404.05427v3.
     [Online]. Available: https://arxiv.org/abs/2404.05427v3                   [83] “addyosmani/test-driven-development,” Repository documentation,
[65] K. Han, S. Maddikayala, T. Knappe, O. Patel, A. Liao, and                      accessed September 9, 2026; mutable default-branch documentation.
     A. B. Farimani, “TDFlow: Agentic Workflows for Test Driven                     [Online]. Available: https://github.com/addyosmani/agent-skills/blob/m
     Development,” 2025, arXiv:2510.23761v2. [Online]. Available: https:            ain/skills/test-driven-development/SKILL.md
     //arxiv.org/abs/2510.23761v2                                              [84] “mattpocock/engineering/tdd,” Repository documentation, accessed
[66] R. Cheng, M. Tufano, J. Cambronero, R. Wei, S. Shi, G. Uy, P. Rondon,          September 9, 2026; mutable default-branch documentation. [Online].
     and F. Ivančić, “Dynamic Cogeneration of Bug Reproduction Test in            Available: https://github.com/mattpocock/skills/blob/main/skills/engine
     Agentic Program Repair,” 2026, arXiv:2601.19066. [Online]. Available:          ering/tdd/SKILL.md
     https://arxiv.org/abs/2601.19066                                          [85] “superpowers/writing-skills,” Repository documentation, accessed
[67] J. Chen, X. Xu, H. Wei, C. Chen, and B. Zhao, “SWE-CI:                         September 9, 2026; mutable default-branch documentation. [Online].
     Evaluating Agent Capabilities in Maintaining Codebases via Continuous          Available: https://github.com/obra/superpowers/blob/main/skills/writing
     Integration,” 2026, arXiv:2603.03823v4. [Online]. Available: https:            -skills/SKILL.md
     //arxiv.org/abs/2603.03823v4                                              [86] “TDD Guard / Probity,” Repository documentation, accessed September
[68] T. Le, M. V. T. Thai, D. N. Manh, H. P. Nhat, and N. D. Q. Bui,                9, 2026; mutable default-branch documentation. [Online]. Available:
     “SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software                  https://github.com/nizos/probity
     Evolution Scenarios,” 2025, arXiv:2512.18470. [Online]. Available:        [87] X. Li, Y. Liu, W. Chen, B. You, Z. Di, Y. He, S. Zheng, K. W. Choe,
     https://arxiv.org/abs/2512.18470                                               J. Sun, S. Wang, C. Tao, B. Li, X. Zhao, H. Geng, X. Wu, J. Zhou,
[69] G. Orlanski, D. Roy, A. Yun, C. Shin, A. Gu, A. Ge, D. Adila,                  X. Chen, H. Xing, Y. Li, Q. Zeng, D. Wang, Y. Wang, R. B. Chaim,
     N. Roberts, F. Sala, and A. Albarghouthi, “SlopCodeBench:                      P. Jiang, H. Shen, L. Kong, X. Liu, R. Wang, X. Liu, J. Li, X. Lan,
     Benchmarking How Coding Agents Degrade Over Long-Horizon                       Y. Lin, W. Ye, J. He, S. Li, Y. Zhang, Y. Gao, Y. Li, Z. Ma, L. Jing,
     Iterative Tasks,” 2026, arXiv:2603.24755v2. [Online]. Available:               T. Wang, K. Li, Y. Xue, H. Lyu, Y. He, Y. Tian, S. Wu, B. Wang,
     https://arxiv.org/abs/2603.24755v2                                             Y. Gao, B. Chen, L. Liu, S. Cheng, J. Bao, S. Tong, S. Xu, T. Y. Zhuo,
[70] J. Gong, Y. Wu, L. Liang, Y. Wang, J. Chen, M. Liu, and Z. Zheng,              T. Ye, Q. Qi, M. Li, L. Liao, Z. Tan, C. Shi, X. Tang, S. Tankasala,
     “CoSQA+: Pioneering the Multi-Choice Code Search Benchmark with                B. Yuan, Y. Qian, J. Tu, C. Wang, Y. Sun, W. Wang, A. Taylor,
     Test-Driven Agents,” 2024, arXiv:2406.11589v7. [Online]. Available:            Z. Yang, C. Guan, Z. Dong, X. Zhang, S. Dillmann, H.-c. Lee, and
     https://arxiv.org/abs/2406.11589v7                                             D. Song, “SkillsBench: Benchmarking How Well Agent Skills Work
[71] H. Tu, Z. Zhou, H. Jiang, I. N. B. Yusuf, Y. Li, and L. Jiang,                 Across Diverse Tasks,” 2026, arXiv:2602.12670v4. [Online]. Available:
     “Isolating Compiler Bugs by Generating Effective Witness Programs              https://arxiv.org/abs/2602.12670v4
     with Large Language Models,” 2023, arXiv:2307.00593v3. [Online].          [88] J. Gong, R. Gu, Z. Fei, Y. Cao, L. Twist, A. Geiger, S. Han, D. Sobania,
     Available: https://arxiv.org/abs/2307.00593v3                                  F. Sarro, and J. M. Zhang, “SkillMOO: Multi-Objective Optimization
[72] L. Zhang, J. Yang, M. Yang, J. Yang, M. Chen, J. Zhang, Z. Cui,                of Agent Skills for Software Engineering,” 2026, arXiv:2604.09297.
     B. Hui, and J. Lin, “SWE-Flow: Synthesizing Software Engineering               [Online]. Available: https://arxiv.org/abs/2604.09297
     Data in a Test-Driven Manner,” 2025, arXiv:2506.09003. [Online].          [89] J. Cao, X. Yan, S. Chen, Y. Lu, Z. Liu, and S.-C. Cheung,
     Available: https://arxiv.org/abs/2506.09003                                    “Inside the Skill Market: From Software Engineering Activities to
[73] X. Li, N. Ben-Israel, Y. Raz, B. Ahmed, D. Serebro, and A. Raux,               Reusable Agent Skills,” 2026, arXiv:2607.09065. [Online]. Available:
     “RepoMod-Bench: A Benchmark for Code Repository Modernization                  https://arxiv.org/abs/2607.09065
     via Implementation-Agnostic Testing,” 2026, arXiv:2602.22518.             [90] X. Zhang, G. Wang, Y. Cui, W. Qiu, Z. Li, B. Zhu, and P. He,
     [Online]. Available: https://arxiv.org/abs/2602.22518                          “Guardrails Beat Guidance: A Large-Scale Study of Rules, Skills, and
[74] Y. Wan, T. Liang, J. Xu, J. Xiao, Y. Huo, and M. R. Lyu, “Automatically        Persistent Configuration for Coding Agents,” 2026, arXiv:2604.11088.
     Generating Web Applications from Requirements Via Multi-Agent Test-            [Online]. Available: https://arxiv.org/abs/2604.11088
[91] J. Yang, A. Prabhakar, K. Narasimhan, and S. Yao, “InterCode:
     Standardizing and Benchmarking Interactive Coding with Execution
     Feedback,” 2023, arXiv:2306.14898. [Online]. Available: https:
     //arxiv.org/abs/2306.14898
[92] T. X. Olausson, J. P. Inala, C. Wang, J. Gao, and A. Solar-
     Lezama, “Is Self-Repair a Silver Bullet for Code Generation?” 2023,
     arXiv:2306.09896v5. [Online]. Available: https://arxiv.org/abs/2306.098
     96v5
[93] M. Mock and B. Russo, “Vibe Coding: An Experiment with Test-
     Driven Development,” 2026, arXiv:2607.22406. [Online]. Available:
     https://arxiv.org/abs/2607.22406
