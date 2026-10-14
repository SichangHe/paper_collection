                                            VALG: An Agentic System for ML Theory Research
                                                         and Demonstrations on COLT 2026 Open Problems

                                                                        Dechen Zhang1,2       Xuan Tang1 Xinxiang Yin1
                                                                          Xingwu Chen1        Jian Qian1 Difan Zou1,2
                                                                  1                                     2
                                                                      The University of Hong Kong           Shenzhen Loop Area Institute
arXiv:2608.13060v2 [cs.AI] 10 Sep 2026




                                                                                    Correspondence: dzou@hku.hk

                                                                                         September 11, 2026



                                                                                             Abstract
                                                  Machine learning theory studies learning procedures through mathematical setups in which the
                                              data model, training protocol, oracle access, loss, metric, and randomness define the phenomenon
                                              that a theorem is meant to explain. Solving an open problem therefore requires the problem
                                              formulation, theorem target, and proof mechanism to be developed in concert. Researchers
                                              formulate hypotheses, test them through preliminary theoretical or empirical analysis, and refine
                                              both assumptions and proofs. We investigate whether this process can be organized as an
                                              autonomous agentic workflow for ML theory research.
                                                  We develop VALG, an agentic system that combines multi-level Verification, Adaptive
                                              formulation of Learning-theory problems, and Graph-structured proof development. Within
                                              each source-relative theorem branch, VALG maintains a fixed mathematical specification, checks
                                              the theorem-level composition of a typed proof-dependency graph, and constructs and reviews
                                              local proofs in dependency order. When a proof attempt fails, VALG identifies whether the
                                              obstruction lies in a derivation, the proof structure, or the theorem formulation and routes the
                                              next attempt accordingly. Formulation-level obstructions initiate an explicitly related variant or
                                              relaxation, preserving the mathematical relation between the resulting theorem and the source
                                              problem.
                                                  We evaluate VALG on nine subproblems from five COLT 2026 open problems spanning
                                              tensor decomposition, learning complexity, one-bit mean estimation, differential privacy, and
                                              online optimization. Two runs produce internally finalized theorem candidates that match the
                                              scope of their source briefs and address the original subproblems; the remaining seven yield
                                              restricted-method results, special cases, or conditional theorems. For each candidate, we report
                                              the problem setup, theorem statement, and progress relative to the source problem. These case
                                              studies show how VALG keeps source-scope matches, relaxations, conditional results, and blocked
                                              attempts mathematically distinct. VALG is open source.
                                                VALG: https://github.com/DechenZhang/VALG-ML-Theory-Agent/tree/main/skills
                                                COLT Problem Solutions: https://github.com/DechenZhang/VALG-ML-Theory-Agent/tree/main/case-studies



                                         1 Introduction
                                         Machine learning theory studies learning procedures through mathematical setups that specify how
                                         data are generated, what information an algorithm can use, which loss or risk is measured, and how
                                         performance scales with problem parameters. This viewpoint is already present in classical PAC
                                         learning and statistical learning theory, where the hypothesis class, distributional model, sample
                                         size, loss, and success probability are part of the statement being studied (Valiant, 1984; Vapnik,

                                                                                                    1
VALG                                                                                     ML Theory Research Agent




1998; Shalev-Shwartz and Ben-David, 2014; Wainwright, 2019). Modern learning-theory papers
often make the same structure more explicit: a result may depend on the training protocol, oracle
model, randomness model, tail condition, approximation notion, or asymptotic regime. In this
literature, such choices usually appear in the theorem statement itself, because they specify the
learning phenomenon under study.
    Consequently, ML-theoretic research often proceeds as a concurrent process in which the problem
setup, theorem formulation, and proof technique are discovered and refined together. This flexibility
can yield scientifically useful outcomes: a well-stated relaxation, a conditional theorem, or a restricted
setting can illuminate why the original problem is hard and which assumptions are essential. It
also creates a risk. Once the protocol becomes adaptive, the representation approximate, the claim
distribution-dependent, or the target property assumed, the resulting theorem may no longer address
the original problem.
    This observation points to a need for systematic support: when the setup, theorem formulation,
and proof technique co-evolve, a reasoning system for ML theory must track that evolution explicitly.
Recent language-model systems have made substantial progress on extended reasoning. General-
purpose agents combine generation, tool use, feedback, and refinement across multiple steps (Yao
et al., 2023; Shinn et al., 2023; Madaan et al., 2023). Scientific-agent systems organize research into
literature search, hypothesis generation, experimentation, critique, and paper writing (Lu et al., 2024;
Schmidgall et al., 2025; Gottweis et al., 2026), while research-agent benchmarks evaluate extended
machine-learning tasks rather than single responses (Huang et al., 2023; Chan et al., 2025; Wijk
et al., 2024; Starace et al., 2025). Mathematical research agents coordinate conjecture generation,
long-horizon proof search, criticism, and revision in natural language, while AI4Theory systems also
connect literature synthesis, theorem proving, algorithm design, and numerical experiments (Feng
et al., 2026; Liu et al., 2026b; Zheng et al., 2026; He et al., 2026). In parallel, formal-mathematics
agents use proof assistants, retrieval, and repair loops to prove or formalize fixed statements,
including complete research-paper developments and statistical learning theory libraries (Yang
et al., 2023; Kripner and Straka, 2026; Zhang et al., 2026c,a). Together, these advances leave an
ML-theory-specific pre-formalization question: how should an agentic system manage informal
theorem development when both the proof and the problem formulation may require revision?
    To this end, we develop VALG1 , an agentic system that combines multi-level Verification,
Adaptive formulation of Learning-theory problems, and Graph-structured proof development within
source-relative theorem branches. The task requires generating a plausible proof while tracking
the theorem under consideration, every added assumption, the cause of each failed attempt, and
the relation of any revised formulation to the source problem. Each branch in VALG fixes one
mathematical specification and represents its proof as a typed dependency graph from primitive
assumptions, through intermediate lemmas, to the target theorem. Before local proof work begins, a
mechanism-aware global analysis checks the mathematical source of each hard claim, the compatibility
of lemma interfaces, and the closure of recursive or limiting arguments. Proof development then
proceeds from global structure to local derivations. We localize failures to a derivation, the proof
graph, or the theorem formulation; only formulation-level obstructions create a new variant or
relaxation. Specialized reviewers separately examine structure, rigor, citation use, and adversarial
boundary cases before assigning a source-relative outcome.
    We evaluate VALG on nine subproblems drawn from five COLT 2026 open-problem papers:
tensor ALS/GD overparameterization (Arvanitakis et al., 2026), distribution-independent deep or
   1
    The name also honors four pioneers of learning theory: Leslie Valiant, whose PAC framework formalized efficient
learnability (Valiant, 1984); Dana Angluin, whose L∗ algorithm established polynomial-time exact learning of regular
languages from membership and equivalence queries (Angluin, 1987); Nick Littlestone, whose mistake-bound analysis
and Winnow algorithm shaped online learning (Littlestone, 1988); and E. Mark Gold, whose identification-in-the-limit
framework provided an early mathematical model of language learning (Gold, 1967).


                                                         2
VALG                                                                         ML Theory Research Agent




statistical-query learning versus linear dimension complexity (Feldman et al., 2026), non-adaptive
one-bit mean estimation (Lau and Scarlett, 2026a), differential privacy PAC learning (Nissim
et al., 2026) and online optimization of Piecewise-Lipschitz functions (Balcan et al., 2026). These
questions remain unresolved in the source works and provide a substantive testbed beyond synthetic
proof-generation tasks. Across nine runs, VALG produces 22 internally finalized theorem candidates.
Two runs produce finalized theorem candidates that fully match the scope of their
source subproblems; the remaining seven yield restricted-method results, special cases,
or conditional theorems. For each run, we report the problem setup and finalized theorem
for selected representative candidates, together with an assessment of their progress toward the
corresponding open problem.
Contributions. Our contributions are highlighted as follows:
1. We formulate informal ML-theory research as an agentic theorem-development problem, in
   which the learning setup, assumptions, theorem target, proof dependencies, and relation to the
   originating research question must be developed and tracked together. This formulation reflects
   the fact that ML theory often requires refinement of both the mathematical assumptions and the
   object being proved.
2. We develop VALG, which organizes this process through source-relative perspective–idea branches,
   fixed theorem contracts, typed proof-dependency graphs, and a sketch–global–step–assembly
   proof pipeline. The architecture separates open-ended problem design from contract-based proof
   development and assigns different review mechanisms to the two stages.
3. We introduce a hierarchical diagnosis and revision mechanism that localizes failures to the
   derivation, proof graph, or theorem formulation. Local failures trigger local repairs, structural
   failures trigger proof-architecture revisions, and only formulation-level obstructions create an
   explicitly source-related variant or relaxation. This allows VALG to retain the mathematical
   relationship between a revised theorem and the original ML-theory problem rather than silently
   replacing the target.
4. We apply VALG to nine subproblems drawn from five COLT 2026 open-problem papers and
   obtain 22 internally finalized theorem candidates. Two runs produce candidates that match the
   scope of their source subproblems, while the remaining seven produce restricted-method results,
   special cases, or conditional theorems. The case studies illustrate how an agentic system can
   distinguish source-scope matches from related but weaker results and unsuccessful branches when
   developing theory for unresolved ML problems.
   The retrospective focuses on branch records and their mathematical outcomes.
Organization. Section 2 positions the work relative to informal mathematical-reasoning agent,
formal theorem proving and research-agent benchmarks. Section 3 presents the theorem-development
method, and section 4 then examines the COLT open problems and the resulting theorem candidates.
The paper closes with limitations and open directions.

2 Related Work
2.1 Mathematical discovery and research agents
AI for mathematics includes neural–symbolic systems for conjecture formation, geometry, and
executable program search (Davies et al., 2021; Trinh et al., 2024; Romera-Paredes et al., 2024;
Novikov et al., 2025), as well as more open-ended systems that combine conjecturing, computation,
and symbolic solving (Chen and Jiang, 2026; Chen et al., 2026; Xia et al., 2026). General scientific
research agents extend this pattern across ideas, experiments, literature, and writing (Lu et al.,

                                                 3
VALG                                                                              ML Theory Research Agent




2024; Schmidgall et al., 2025; Gottweis et al., 2026; Yang et al., 2026); mathematical research places
additional weight on constructing and checking long derivations.
    Research-level proof agents organize natural-language mathematics around generation, criticism,
and revision. Aletheia scales a generator–verifier–reviser loop across pure mathematics, while
ProofCouncil and RMA distribute analysis, literature use, proof construction, criticism, and
computation across specialized roles (Feng et al., 2026; Schmitt et al., 2026; Zhao et al., 2026).
Rethlas, QED, and the MechMath Agent Team connect informal exploration with formal checking
through theorem retrieval, decomposition, and natural- or formal-language provers (Ju et al., 2026;
An et al., 2026; Cao et al., 2026); the AI Co-Mathematician instead supports interactive refinement
of definitions, questions, conjectures, computations, and proof directions (Zheng et al., 2026).
    Danus addresses long-horizon coordination through parallel proof search and a shared fact
graph (Liu et al., 2026b). A main agent redirects workers across lines of attack, while a stateless
verifier checks each natural-language claim before the claim, its proof, and its logical dependencies
enter the graph. This structure lets many local contributions accumulate into a long argument
and supports transitive removal when an accepted fact is later rejected. Its fact graph is close to
our typed proof dependencies, although Danus terminates when a supplied target or its refutation
becomes a verified fact. VALG additionally separates a proposed proof architecture from theorem-
level feasibility and local derivations, and it treats a formulation-level obstruction as a reason to
create an explicitly source-related theorem branch rather than to edit the target in place.
    The closest AI4Theory systems extend agentic research beyond pure proof: ReasFlow integrates
literature synthesis, algorithm design, theorem proving, numerical experiments, and manuscript
preparation, while Iteris combines proof drafts with numerical and adversarial exploration (He et al.,
2026; Chen et al., 2026). VALG focuses more specifically on ML-theory questions whose learning
setup, assumptions, and theorem target may co-evolve. It records whether a result addresses the
source question itself, a restricted method, a special case, or a conditional variant; this source-relative
distinction guides both failure routing and case-study evaluation.

2.2 Formal theorem proving agents
Formal theorem proving begins after a mathematical statement and its assumptions have been
encoded in a proof assistant. The kernel then supplies an exact acceptance criterion for a completed
proof. LeanDojo provides a programmatic Lean environment, premise annotations, and retrieval-
augmented proving benchmarks, while HyperTree Proof Search combines learned proof-step proposals
with structured search (Yang et al., 2023; Lample et al., 2022). COPRA wraps a general-purpose
language model in stateful backtracking search and uses proof assistant errors and retrieved lemmas
as feedback (Thakur et al., 2024).
    Subsequent systems improve formal proof search through synthetic data, proof-assistant feedback,
informal planning, and reusable lemma libraries. DeepSeek-Prover and its later versions combine
large-scale Lean data, reinforcement learning, tree search, and subgoal decomposition; Lean-STaR
interleaves informal thoughts with tactic generation; and LEGO-Prover and DreamProver grow
transferable libraries of verified lemmas across problems (Xin et al., 2024; Ren et al., 2025; Lin
et al., 2025; Wang et al., 2024; Zhang et al., 2026b). OpenProver, OProver, Numina-Lean-Agent,
and LAMP expose agentic interaction, verifier-guided repair, and tool use in Lean, while Discover
and Prove separates answer discovery from formal proof for hard-mode statements (Kripner and
Straka, 2026; Ma et al., 2026; Liu et al., 2026c; Srinivasan R and Patawar, 2026; Liu et al., 2026a).
These methods can provide kernel-checked correctness for the encoded theorem, but they generally
take the formal target as fixed; they do not decide whether a revised learning-theory formulation
remains a meaningful answer to an originating research question.
    AI4SLT brings this formal perspective directly to machine learning theory. It combines human-
designed proof strategies with AI-assisted Lean construction to develop an empirical-process library

                                                    4
VALG                                                                            ML Theory Research Agent




containing Gaussian concentration, Dudley’s entropy integral, and sharp least-squares regression
rates (Zhang et al., 2026a). The formalization reveals implicit assumptions and omitted steps in
standard presentations, demonstrating the value of machine-checked ML theory. Its objective is
to formalize an established mathematical development; VALG instead operates earlier, when the
learning setup and theorem target are still under construction, and can pass a finalized branch to
such a formal verification workflow.

2.3 Autoformalization
Autoformalization addresses a different interface: translating natural-language mathematics into
a formal statement or proof. Early LLM-based work demonstrated statement translation into
Isabelle, ProofNet paired informal undergraduate problems with Lean statements and proofs, and
MMA expanded training through large-scale multilingual informal–formal pairs (Wu et al., 2022;
Azerbayev et al., 2023; Jiang et al., 2023). A recent survey organizes this rapidly growing area by
mathematical domain, model, data, and evaluation strategy (Weng et al., 2025).
    Recent work moves from isolated statements toward complete proofs and research libraries.
ProofFlow first recovers a directed dependency graph from an informal proof and formalizes its
steps as intermediate lemmas, explicitly measuring semantic and structural fidelity (Cabral et al.,
2026). Beyond the Library introduces an agentic pipeline that can add definitions and auxiliary
lemmas missing from Mathlib when formalizing research papers, and TOMAP concentrates test-time
refinement on the decomposition that supplies claims, assumptions, and dependencies to downstream
formalizer and prover agents (Moakhar et al., 2026; Liu et al., 2026d). FormalRx diagnoses semantic
misalignment by error type and location rather than returning only a binary translation score, while
theory-level autoformalization argues that useful formalization must ultimately construct coherent
libraries of definitions, lemmas, theorems, and their interdependencies (Wang et al., 2026; Min et al.,
2026). LeanMarathon addresses long-horizon research-paper formalization through an evolving Lean
blueprint that serves as both proof skeleton and natural-language proof graph. Four specialized
agents stabilize target fidelity and discharge the resulting dependency graph from its leaves in
parallel, producing complete Lean formalizations of seven target theorems from recent research
papers (Zhang et al., 2026c). These graph- and theory-level perspectives are close to VALG’s
emphasis on compositional structure. Their input, however, is an existing informal statement or
proof to be translated faithfully; VALG uses a dependency graph earlier, while constructing and
revising the theorem itself, and leaves proof-assistant formalization as a separate verification layer.

2.4 Benchmarks for mathematical and research agents
Formal benchmarks such as miniF2F, ProofNet, and PutnamBench evaluate proving or formalizing
fixed competition and undergraduate problems (Zheng et al., 2021; Azerbayev et al., 2023; Tsoukalas
et al., 2024). Research-level evaluations instead use expert-proposed open problems, as in Aletheia’s
FirstProof benchmark (Feng et al., 2026), or extract larger problem collections from the mathematical
literature. RMA evaluates an agentic system on research-level problems, while ResearchMath-14K
collects 14,056 questions and documents recurrent failures including fabricated references, non-
attempts, and substitution of a narrower problem (Zhao et al., 2026; Son et al., 2026). These failures
motivate evaluating both mathematical validity and fidelity to the supplied research question.
    Research-agent benchmarks cover a broader executable workflow. MLAgentBench evaluates
iterative model training, debugging, and experimental improvement; MLE-bench expands this
setting to 75 offline Kaggle competitions; and RE-Bench compares agents with human experts
under different time budgets (Huang et al., 2023; Chan et al., 2025; Wijk et al., 2024). Other suites
begin from published scientific work: CORE-Bench tests computational reproducibility, PaperBench
asks agents to replicate complete AI papers, and ScienceAgentBench isolates expert-validated
scientific coding tasks (Siegel et al., 2024; Starace et al., 2025; Chen et al., 2025). These benchmarks

                                                   5
VALG                                                                          ML Theory Research Agent




measure experimentation, research engineering, reproducibility, and data analysis under fixed task
specifications. Our case studies address a complementary question: whether an agent can develop a
theorem and, when necessary, a related formulation while keeping each outcome mathematically
tied to the original ML-theory problem.

3 VALG: ML Theory Research Agent
VALG develops theorem candidates from an ML-theory research direction or question. Starting
from a source problem, it maps the relevant literature, identifies distinct perspectives, develops
mechanism-level ideas, formalizes each viable idea as a precise setting and goal, constructs and
reviews a proof from global structure to local derivations, and reports every accepted theorem
relative to the source problem. A run may return zero, one, or several accepted theorem candidates.
    VALG divides theorem development into a pre-proof stage for formalizing the problem setup
and a proof-review stage for constructing and checking the proof. Dedicated revision loops operate
at both stages because local derivations, proof structure, and theorem formulation require different
repairs. Figure 1 summarizes the complete workflow.

3.1 Workflow 1: Pre-Proof Stage
Theorem proving in pure mathematics often begins with well-defined problem setup, including
formalized assumptions, mathematical objects and targets. However, an ML-theory research question
is often less settled. It may specify a learning phenomenon but leave open which model subclass, data
distribution, algorithmic mechanism, performance metric, or asymptotic regime makes a theorem
both true and informative. Workflow 1 therefore treats problem formulation as an explicit research
task rather than an implicit prerequisite for proof search.
    The workflow begins with a source question and, when available, an accompanying research
brief. Guided by the literature survey, it organizes exploration around a two-level perspective-idea
hierarchy. A perspective provides a broad research lens, whereas an idea fully specifies a concrete
problem setup sufficient for downstream formalization and theorem proving. Steps of Workflow 1
are summarized as follows.
1. Literature survey. The literature worker maps the relevant settings, results, proof techniques,
   and evidence-supported gaps. Different from conventional literature survey in auto research,
   ML-theory research
     • should separate empirical evidence from theoretical foundations to discover research gaps
       in explaining empirical phenomenon;
     • should determine applicable theoretical testbeds to study theoretical research question.
   We therefore separate existing literature into direct theoretical sources, foundational theoretical
   frameworks and empirical practice, while preserving the constraints that define the source
   direction.
2. Two-level perspective-idea structure.
     • Breadth-focus perspective selection. The perspective selector to select a small set of
       distinct, gap-grounded perspectives and launches them as parallel research branches, where
       a perspective is defined as a coherent, literature-supported research lens, represented by
       the normalized tuple

                  (analysis target, model class, data assumption, regime, algorithm).

       Such characterization for perspective distinguishes a meaningful research direction, such as


                                                  6
VALG                                                                                                                                                    ML Theory Research Agent




                                                                          WORKFLOW 1 · IDEA DISCOVERY                                                                ✓    interactive checkpoint



                         INPUT                                                                                                                       STAGE 02
                                                                                          STAGE 01
              Research direction                                                                                                             Perspective selection
               source question +                                                Literature survey                           ✓
                                                                                                                                                   distinct,                      ✓    M ≤3
                                                                             constraints, results, gaps
             optional research brief                                                                                                         gap-grounded lenses
                                                                                                                                                                                                 active
                                                                                                                                                                                                branches

                                                                                          STAGE 04                                                   STAGE 03
                   theorem contract                                               Formalization                                               Idea generation
                                                          ✓                                                                 ✓
                     for branch m                                              objects, assumptions,                                         mechanism, support,
                                                                                 exactly one goal                                              duplicate gate




                                          WORKFLOW 2 · SPLIT THEORY PROOF · repeated for every active branch

                                                                                                                                                                 REVIEW · STAGE 04
               PRODUCE · STAGE 01                                                                                  PRODUCE · STAGE 03
                                                                   REVIEW · STAGE 02                                                                                Global review
                   Proof sketch                                                                                        Global proof
                      typed                                         Sketch review                                     whole-theorem                                   viability +
                                                                  early viability gate                                                                               obstruction
                 dependency DAG                                                                                         diagnostic
                                                                                                                                                                     localization
                                                                    retry: sketch / idea
                                                                                                                                                              retry: global / sketch / idea

               PRODUCE · STAGE 07
                                                                                             REVIEW · STAGE 06                                                  PRODUCE · STAGE 05
                 Proof assembly
                accepted steps →                                                                Step reviews                                                       Step proofs
                                                                                             fresh independent                                                     S1 , . . . , Sk in
                  self-contained
                                                                                            review for every Si                                                  dependency order
                   manuscript
                                                                                        retry: step / dependency / sketch


                REVIEW · STAGE 08                                                            REVIEW · STAGE 09                                              ACCEPT · STAGE 10
           Specialized final reviews                                                                                        score ≥ 7, no blockers    Finalize accepted branch
                                                                                         Aggregate final review
              structural | rigor |                                                        sole controller-facing                                      verify gates; copy setting,
             citation | adversarial                                                              verdict                                             manuscript, and final review

                                                                                   retry: assembly / step / sketch / idea



        FAILURE-LOCALIZED ROUTING                                                                                                         CONTROLLER INVARIANTS
        Reviewers diagnose; the controller selects the smallest valid producer retry.
                                                                                                                                         GATES         validate artifacts before use
                                                                    PROOF STRUCTURE
       ASSEMBLY                      LOCAL STEP                     diagnostic → 03               THEOREM CONTRACT
       flaw → 07                     step/dependency → 05                                         failure → new idea                     WORKERS       2 run-scoped; 12 + 2k per branch
                                                                    graph/interface → 01
                                                                                                                                         RUN MODE      interactive pauses; autopilot proceeds
        Budget escalation:    local unit → sketch → new idea → branch failure                                                             Both modes enforce coverage, budgets,
                                                                                                                                          and accepted-copy verification.



Figure 1: The VALG workflow. Workflow 1 creates active perspective branches; Workflow 2 is shown
for one branch. Teal, amber, and green denote producers, independent reviewers, and accepted
output, respectively. Solid arrows show validated forward flow. A finalized branch does not stop the
remaining branches.


       the desired theoretical guarantee, model and data setting, learning regime, or algorithmic
       family. It needs not fix every aspect of the eventual theorem; rather, it defines a broad
       search region and leaves appropriate choices open for refinement during idea generation.

    • Depth-focus idea generator. Within each perspective branch, an distinct idea generator
      proposes a concrete mechanism and candidate result using the upstream perspective
      as an explicit anchor. Ideas that are unsupported by the literature or duplicate ideas
      already proposed in another branch are rejected. Each generated idea must be a
      field-wise specialization of its upstream perspective: it may make the analysis
      target, model class, data assumption, regime, or algorithm more specific, but it may not
      broaden any of these choices or contradict the perspective.

    This separation keeps exploration broad without spending all proof effort on a single interpre-


                                                                                                  7
VALG                                                                            ML Theory Research Agent




     tation, while giving each surviving branch a focused mechanism and theorem target.

3. Formalization. For each viable, nonduplicate idea, the formalizer fixes the notation, primitive
   assumptions, quantifiers, regime, and exactly one mathematical goal. The resulting setting is the
   theorem contract passed to Workflow 2.

Human-expert interactive mode. We remark that early failures are expected:
   • research gaps from literature survey may not be valuable in research level;
   • perspectives may be too narrow, too broad, or redundant;
   • ideas may depend on assumptions that make the resulting theorem unacceptable.
Because these decisions are scientific as well as formal, Workflow 1 places a human-expert checkpoint
after each stage. In interactive mode, the expert may approve the artifact, edit it, or request a
new search or generation with human-expert feedback. Autopilot mode proceeds with approval by
default, but retains the same source-direction fidelity and branch-coverage constraints. In either
mode, only a checked and formalized branch enters proof development.

3.2 Workflow 2: Proof-Review Stage
Following Workflow 1, Workflow 2 develops mathematical proofs based on the provided formalized
setting and goal. Our initial approach relied on monolithic proof generation, which entangles
theorem-level architecture, local derivations, and final exposition. This method suffered from one
severe limitation: the resulting proofs were too compact to effectively review or understand.
    Drawing on recent progress in natural-language mathematical reasoning, where systems typically
generate a proof plan, tackle each step individually, and then assemble the final proof (An et al., 2026;
Ju et al., 2026; Feng et al., 2026), we introduced a similar sketch-step-assembly decomposition
to make local claims individually addressable. This decomposition, however, revealed a second
gap: a structurally coherent dependency graph does not guarantee that every node is derivable
from its assigned inputs, nor does it ensure that its conclusion possesses the precise form and
quantitative strength required downstream. To resolve this, we inserted a theorem-level global
diagnostic between the sketching and local proof phases, ultimately structuring Workflow 2 as a
four-stage sketch-global-step-assembly pipeline.
3.2.1 Proof Stage
1. Proof sketch. The sketch worker represents the proposed argument as a directed acyclic
   dependency graph. Source nodes encode primitive assumptions, internal nodes encode lemma-
   sized claims, and the unique sink is the target theorem. Each node records its exact claim,
   dependencies, permitted assumptions, intended proof tool, and required output interface.
2. Global proof. The global-proof worker expands the accepted graph into a whole-theorem
   diagnostic. For every node, it traces the available inputs, identifies the mechanism or cited
   result that could establish the claim, and checks whether the output has the form and strength
   required by downstream nodes. At theorem level, it audits quantitative dependence, probability
   and convergence modes, object compatibility, closure arguments, boundary behavior, and the
   composition of local interfaces.
     Global proof is crucial as proof dependency graph consistency does not ensure theorem-level
     composability and local-derivation feasibility. For example, an upstream guarantee for a
     surrogate object may not imply the guarantee required for the original target downstream.
     The global diagnostic identifies these cross-step mismatches, specifies each step’s admissible


                                                   8
VALG                                                                            ML Theory Research Agent




    inputs and required output, and guides step workers for full local derivations.

3. Proof step. A dedicated step worker converts one graph obligation into proof evidence using
   the formal setting, accepted dependency results, and the global diagnostic as context. It may
   introduce local lemmas, but must state and prove them before deriving the exact assigned claim,
   without strengthening assumptions or weakening the required output.

4. Proof assembly. Once all required steps are accepted, the assembler reconciles notation and
   composes their claims into a self-contained LATEX theorem manuscript. This stage verifies that
   the accepted local interfaces yield the stated theorem in one coherent presentation.

3.2.2 Review Stage
We would like to highlight a key difference between Workflow 1 and Workflow 2 in review mechanisms
because they govern different kinds of decisions.
 Human-expert checkpoints versus agent reviewers

 • Workflow 1 uses human-expert checkpoints because evaluating literature gaps and selecting
   research perspectives and theorem formulations require open-ended judgments about
   research value that depend strongly on human expertise.

 • Workflow 2 begins from a fixed theorem contract. This contract allows reviewers distinct
   from the producers to assess each proof artifact against explicit, stage-specific obligations
   of goal alignment, assumption fidelity, logical soundness, and derivational rigor before the
   controller authorizes its downstream use. Because both the target and the evaluation criteria
   are fixed, this contract-based review is better suited to specialized agent reviewers than the
   open-ended decisions in Workflow 1.
    Hence, within Workflow 2, we place a distinct sketch reviewer checks proof architecture after the
sketch worker, a distinct global reviewer checks theorem-level feasibility after the global proof worker
and a distinct step reviewer checks local derivations after the proof step worker. This separation
prevents producer self-validation and exposes defects at the same level of abstraction at which they
arise. Below we show the key rubrics of both sketch and step reviewers.
 Key rubrics

 • Proof-sketch review (/proof-sketch-review).
    1. Goal fidelity. Check exact-goal or target-spec alignment, including quantifiers, regimes,
       probability or convergence modes, normalization, and exposed rate dependence.
    2. Graph and coverage. Verify an acyclic graph of stable, lemma-sized steps with legal
       earlier dependencies, allowed assumptions, intended proof tools, output targets, and explicit
       blockers for unresolved high-risk obligations.
    3. Provenance and interfaces. Trace assumptions, derived invariants, and cited tools to
       legal sources; trace every generated output from producer to consumers and through any
       required current-notation or residual-to-target bridge.
    4. Viability gates. Check mechanism witnesses, baseline and entry behavior.

 • Proof-step review (/proof-step-review).
    1. Local-unit audit. Check every local lemma statement and derivation against the exact
       sketch-row claim, allowed assumptions, and accepted dependencies.


                                                   9
VALG                                                                            ML Theory Research Agent




    2. Hidden-claim and provenance audit. Scan for independent subclaims; trace assump-
       tions, constants, rates, events, and notation; restate cited results in current notation with
       all hypotheses discharged; stress quantifiers, modes, and boundary cases.
    3. Target assembly. Verify that named local results, checked citations, and accepted
       dependencies jointly establish the exact target claim without strengthening assumptions or
       weakening the required output.
    For assembly worker, which is the first stage where all accepted components, notation,
citations, and connecting implications must jointly establish the exact theorem, however,
the substantial review task motivates us to separate review into independent, multi-angle reviews
(An et al., 2026): dependency and coverage errors (structural), invalid derivations (rigor), misapplied
external results (citation), and hidden boundary-case failures (adversarial). Each reviewer is therefore
tied to a specific assembly-level risk, rather than being an arbitrary addition. Finally, an aggregate
reviewer reconciles them into the sole controller-facing final-review verdict and identifies the smallest
admissible repair target.
  Key rubrics

  • Structural review (/proof-review-structural).
    1. Check the assembled claim against the setting, close every dependency, trace every required
       sketch step into an accepted proof and the public appendix.
    2. Reject independent mathematics introduced during assembly.
    3. The public LATEX must remain self-contained, paper-ready, and explicit about its assump-
       tions and theorem-style references.

  • Rigor review (/proof-review-rigor).
    1. Inspect the actual derivations rather than labels or environment counts.
    2. Audit quantifier order, constants and parameter dependence, probability and convergence
       modes, assumption provenance, explicit-rate specialization bridges, interchanges, and
       boundary cases.
    3. Compare every used step’s proof obligations with its appendix proof body.

  • Citation review (/proof-review-citation).
    1. Verify that each cited or internal result exists and supports the exact conclusion used,
       translate its objects and notation into the current setting, and discharge every hypothesis
       in the claimed regime.
    2. Check BibTeX keys and internal label–reference pairs.

  • Adversarial review (/proof-review-adversarial).
    1. Attack the weakest claims with concrete assumption-minimal, boundary, degenerate, and
       extreme regimes.
    2. Test hidden assumption strengthening, unsupported scope or convergence-mode upgrades,
       unproved derived invariants, and failed baseline reductions.
    3. Treat verified breaks and unresolved high-risk candidate counterexamples as blocking.

3.3 Revision Loops
A failed proof attempt may expose a defect in a local derivation, a dependency interface, the proof
architecture, or the theorem formulation itself. In ML-theory research, it may also show that the
initial problem setup requires an additional condition or a revised assumption before a valid theorem

                                                   10
VALG                                                                                            ML Theory Research Agent




                                                2 INDEPENDENT                             3 CONTROLLER
        1   CURRENT ATTEMPT
                                                REVIEW                                    ROUTING
        Attempt a
                                                Diagnose the failure                      Select the repair level
        Evaluate one stage result
                                                Identify the failure type and             Validate the diagnosis and
        against its stated target and
                                                the smallest mathematical                 route one scoped retry to
        accepted inputs.
                                                object that must change.                  the responsible stage.

                                                5   FRESH REVIEW
                                                Check the revision                        4   SELECTED PRODUCER
                 Accepted
                                                Repeat the required                       Construct Attempt a + 1
            Advance the revised
                                                independent review or                     Revise only the implicated
             result downstream
                                                human checkpoint before                   mathematical component.
                                                downstream use.


                                                                                blocking: return to Step 3

Figure 2: Controlled revision in VALG. An independent review identifies the smallest repair target,
the controller routes the diagnosis to the responsible stage, and the selected producer revises only
the implicated part. The revised attempt must pass a fresh independent review or human checkpoint
before downstream use.


is possible. VALG therefore uses a hierarchy of revision loops that routes each diagnosis to
the smallest stage capable of repairing it. This hierarchical structure, along with its corresponding
review routing mechanisms, is organized as follows:

                              proof assembly → proof step → proof sketch → idea
                                              global proof ↗

• proof-sketch review: ACCEPTED, REVISE SKETCH, or IDEA FAIL;

• global-proof review: ACCEPTED, REVISE GLOBAL, REVISE SKETCH, or IDEA FAIL;

• proof-step review: ACCEPTED, REVISE STEP, BLOCKED BY DEPENDENCY, or REVISE SKETCH;

• aggregate final review: ACCEPTED, PROOF ASSEMBLY FLAW, PROOF STEP FLAW, PROOF SKETCH FLAW,
  or IDEA FAIL.

In every case, the failed review identifies the smallest repair target, the controller selects the
responsible stage subject to its retry budget 2 , and the selected producer uses the accepted upstream
context, the failed attempt, and the validated diagnosis to change only the implicated part. Figure 2
summarizes this controlled revision cycle.




   2
      If a stage’s retry budget is exhausted, the controller escalates the issue by routing it to a higher-level stage that
still has remaining budget.


                                                             11
VALG                                                                                           ML Theory Research Agent




4 COLT 2026 Case Studies
We evaluate VALG on nine subproblems drawn from five COLT 2026 open-problem papers (Lau
and Scarlett, 2026a; Arvanitakis et al., 2026; Balcan et al., 2026; Nissim et al., 2026; Feldman
et al., 2026). Each subproblem is run independently from a research brief extracted from its source
description, using GPT-5.6-sol at maximum reasoning effort. Finalized theory candidates have been
checked through independent multi-perspective LLM reviewing and roughly audited by human3 .
    Table 1 reports every perspective branch represented in the archived runs. Within a run, VALG
may develop several perspective branches (with maximum budget 3) in parallel. For each perspective
branch, the idea generator prioritizes a source-faithful candidate aimed at fully resolving the
subproblem. If no such ideas are viable, it will then attempt to propose an idea with partial-progress
type, i.e., a relaxed problem setup. After the first idea is proposed, subsequent idea variants are
opened only after explicit controller routing, such as an idea-level review failure, or escalation after
lower-level retry budgets are exhausted. See Section 3.3 for illustration of the revision rules.
    We would like to remark that progress is computed as P = min{C +B+H, applicable cap}, where
“applicable cap” is a hard ceiling triggered by a fundamental mismatch with the original problem.
For example, P ≤ 3 if the theorem assumes a central unresolved property, P ≤ 7 if it proves only
one direction of a characterization or omits a central quantifier, regime, or rate. C ∈ [0, 4] measures
closure of the paper-level target contract, B ∈ [0, 3] measures improvement over the paper’s baseline,
and H ∈ [0, 3] measures how much of the central open burden is discharged. A score of P = 10
denotes exact target coverage. Regarding mathematical soundness, S = min{M, D, A} is a weakest-
link assessment of intrinsic mathematical validity, verification of theorem-critical dependencies, and
audit completeness. For technical novelty, N measures the originality and proof-critical role of the
technical mechanism relative to prior work.
    Results show that two of nine subproblems are fully solved while the remaining seven subproblems
are partially solved. For each subproblem, we report the most informative branches and state
their progress relative to the corresponding source problem. Proof details are available at https:
//github.com/DechenZhang/VALG-ML-Theory-Agent/tree/main/case-studies/colt-2026.

4.1 How much overparametrization is needed for ALS in tensor decomposition?

  Open question. Let
                                              r
                                              X
                                       T =           aj ⊗ bj ⊗ cj ∈ Rn×n×n
                                               j=1

  where aj , bj and cj are obtained by adding mutually independent N (0, ρ2 In /n) perturbations,
  with ρ = 1/ poly(r), to deterministic factor columns. Consider an optimization problem
  minimizing the least-squares objective

                                                               k                       2
                                                               X
                                         min              T−          xi ⊗ y i ⊗ z i       .
                                 xi ,yi ,zi ∈Rn , i∈[k]
                                                                i=1                    F

  The open question of Arvanitakis et al. (2026) asks what is the smallest value of k = k(r) so
  that alternating least squares (ALS) or another iterative algorithm such as GD converges from
  random initialization to the global optimum with high probability.

   3
     The correctness of the proof may also need to be verified by more experts, especially the authors of these
open-problem papers.




                                                           12
VALG                                                                                           ML Theory Research Agent




Table 1: Perspective-level search and evaluation summary.

                                                                       Ideas     Branch      Elapsed
Problem                              Subproblem           Persp.       tried    outcome        (h)   Progress Rank
                                                             1          7       Idea 7         76       6.50         1
                                     Upper bound
                                                             2          14     Exhausted        –       0.00         2
P1: Tensor ALS                                               1          2       Idea 2         8        2.25         2
                                     Lower bound             2          2       Idea 2         11       3.00         1
                                                             3          3       Idea 3         38       3.00         3
                                                             1             1     Idea 1        13      10.00         2
P2: 1-bit mean estimation            Non-adaptive            2             2   Interrupted     –        0.00         3
                                                             3             1     Idea 1        9       10.00         1
                                                             1             3     Idea 3        12       2.75         2
                                     SGD                     2             2     Idea 2        10       2.25         3
                                                             3             2     Idea 2        12       5.25         1
P3: Deep vs. linear learning
                                                             1             3     Idea 3        15       2.75         2
                                     SQ                      2             2     Idea 2        8        3.00         1
                                                             3             2     Idea 2        9        2.25         3
                                                             1             3    Idea 3         48       6.50         1
                                     Sample
                                                             2             4    Idea 4         91       6.25         2
                                     complexity
                                                             3             1    Idea 1         28       5.25         3
P4: Private PAC learning
                                                             1             5    Idea 5         28       3.00         2
                                     Class
                                                             2             2    Idea 2         25       5.50         1
                                     existence
                                                             3             6   Exhausted        –       0.00         3
                                                             1             1     Idea 1        12       5.75         2
                                     Polynomial
                                                             2             1     Idea 1        24       7.00         1
P5: Online optimization                                      1             1     Idea 1        30      10.00         1
                                     Pfaffian                2             1     Idea 1        40      10.00         2
                                                             3             1     Idea 1        31       6.75         3
Progress P ∈ [0, 10] is evaluated against the original paper’s subproblem by a distinct agent. Rank is computed within
each subproblem from 0.40 × progress, 0.40 × mathematical soundness, and 0.20 × technical novelty by a distinct
agent. Exhausted indicates that the branch consumed its configured idea-variant budget without finalizing a theory,
whereas Interrupted indicates that execution ended before finalization by human. A dash denotes unavailable elapsed
time.


4.1.1 Subproblem 1: Upper Bound

  Open question. Does some iterative method, with r < k = o(r2 ) components, return in
  poly(n, r, log(1/ϵ)) time a decomposition satisfying
                                              k
                                              X
                                        T−            xi ⊗ y i ⊗ z i       ≤ ϵ∥T ∥F
                                                i=1                    F

  with high probability over the smoothed instance?

Perspective 1.
Formalized setting and preliminaries. Fix integers r ≥ 3, n and let q∗ = 1/4096. For deterministic
Ā, B̄, C̄ ∈ Rn×r with nonzero columns, define ūj = āj /∥āj ∥2 and cyclically v̄j , w̄j ; write Ū = [ūj ],

                                                             13
VALG                                                                                       ML Theory Research Agent




V̄ = [v̄j ], W̄ = [w̄j ] and λ̄j = ∥āj ∥2 ∥b̄j ∥2 ∥c̄j ∥2 . For a unit-column matrix M = [mj ], write
                                            X
                           q(M ) = max           |⟨mj , mℓ ⟩|,      q̄ =    max   q(M ).
                                      j                                M ∈{Ū ,V̄ ,W̄ }
                                          ℓ̸=j

                                                        (A)    (B)     (C)                                          (A)
Independently over columns and modes, draw gj , gj , gj                      ∼ N (0, ρ2 In /n), set aj = āj + gj
and cyclically bj , cj , and form
                                      r
                                      X                      r
                                                             X
                                T =         aj ⊗ bj ⊗ cj =         λj uj ⊗ vj ⊗ wj ,
                                      j=1                    j=1

where U = [uj ], V = [vj ], W = [wj ] are the normalized realized factors and λj = ∥aj ∥2 ∥bj ∥2 ∥cj ∥2 .
Put qreal = max{q(U ), q(V ), q(W )} and Γ = maxj λj / minj λj .
   The proposed procedure uses
          l                     m                                                                          q∗2
       k = Crank r5/3 (log r)5/2 ,        Lburn = ⌈Cburn log r⌉,       Lcert = ⌈Ccert log r⌉,    τr =           .
                                                                                                          104 r
                                                                                                   (M )
For each slot i and mode M ∈ {U, V, W }, draw mutually independent raw vectors ξi           ∼ N (0, In ),
independently of the smoothing, and initialize (p0i , qi0 , s0i ) by normalizing the corresponding raw
triple. For h = (p, q, s), it repeatedly makes the simultaneous old-state Jacobi commit
                                                                                 
                                       T (·, q, s)   T (p, ·, s)    T (p, q, ·)
                           J (h) =                 ,              ,                 .
                                     ∥T (·, q, s)∥2 ∥T (p, ·, s)∥2 ∥T (p, q, ·)∥2

After Lburn commits it inspects the states through t = Lburn + Lcert and stores the first one for
which maxM minσ∈{±1} ∥hM − σJM (h)∥2 ≤ τr . Only states with nonzero contractions and a valid
certificate proceed. Certified triples are filtered at 0.85 of the largest score |⟨T, p ⊗ q ⊗ s⟩|. Form a
graph on the remaining triples, joining two vertices when their modewise absolute correlations are
all at least 1 − 64q∗ . The proposal is accepted only if this graph has exactly r connected components.
The minimum-displacement representative of each component, with score as tie-break, gives an
equal-norm best-scalar seed. For representative (pa , qa , sa ) with θa = ⟨T, pa ⊗ qa ⊗ sa ⟩ =
                                                                                             ̸ 0, this seed
is
                       x0a = |θa |1/3 pa , ya0 = |θa |1/3 qa ,  za0 = sgn(θa )|θa |1/3 sa .
A zero score aborts the run.
    Here ⊙ denotes the columnwise Khatri–Rao product. The three designs Z 0 ⊙ Y 0 , Z 0 ⊙ X 0 , and
Y ⊙ X 0 are frozen before any solve. Three Moore–Penrose least-squares landing proposals are
  0

computed from that same seed and committed synchronously. The run aborts if any committed
active column is zero; otherwise the proposals are rebalanced once without changing their rank-one
products. Cyclic U/V /W ALS then updates the r active columns; the other k − r columns stay
zero. Each run stops at relative residual ϵ or after ⌈Cstop log(8κ20 /ϵ)⌉ sweeps.
                               (M )                                                 (M )       (M )
    For raw proposal vectors ξi , set mU,j = uj , mV,j = vj , mW,j = wj and Zij = ⟨mM,j , ξi ⟩
          p
and tr = (10/9) log r. The analysis uses the target-slot event
                    \          (M )
                                                   \ \  (M ) (N )            19
                                                                                       
                                            −1
              Eij = {tr ≤ |Zij | ≤ tr + tr } ∩                 |Ziℓ Ziℓ | ≤       log r ,
                                                                              18
                      M                                 ℓ̸=j {M,N }

where M, N range over distinct pairs from {U, V, W }.



                                                       14
   VALG                                                                                 ML Theory Research Agent




   Technical assumptions.

   Assumption 4.1 (Bounded deterministic base scales). Every base-column norm lies in [κ−1
                                                                                        0 , κ0 ],
   where 1 ≤ κ0 ≤ rdκ for a fixed finite dκ .

   Assumption 4.2 (Cumulative Gram interference). q̄ ≤ q∗ /4.

   Assumption 4.3 (Near-balanced deterministic weights). maxj λ̄j / minj λ̄j ≤ 1 + 1/800.

   Assumption 4.4 (Independent Gaussian smoothing). The 3r perturbations have the independent
   laws above, with 0 < ρ ≤ 1 and ρ−1 ≤ rdρ for a fixed finite dρ .

   Assumption 4.5 (Scale-aware smoothing and dimension margin). For δsm ∈ (0, 1),
                                                    r
                              q∗               2 2    log(9r2 /δsm )  q∗
                      κ0 ρ ≤     ,   r(κ0 ρ + κ0 ρ )                 ≤ .
                             128                           n          32
   Assumption 4.6 (Strictly subquadratic proposal rank). The displayed k satisfies r < k ≤ n.

   Assumption 4.7 (Independent proposal and restart randomness). Conditional on the once-drawn
   tensor, proposal triples are independent across slots, modes, and completed runs, and independent
   of smoothing; restarts reuse the tensor but not proposal randomness.

   Assumption 4.8 (Accuracy and separate confidence levels). 0 < ϵ, δsm , δinit < 1, with the latter
   two controlling the smoothed instance and conditional restarts, respectively.

Main theory.
     Theorem 4.1 (Conditional strictly subquadratic recovery). Universal positive choices of
     Crank , Cburn , Ccert , Cstop , Crep make the following true under Assumptions 4.1–4.8. There is a
     smoothing event Esm of probability at least 1 − δsm on which every realized column has norm at
     least (2κ0 )−1 ,

                                       qreal ≤ q∗ ,                                   Γ ≤ 1.01,
                               ⊤                                            ⊤
                λmin ((V ⊙ W ) (V ⊙ W )) ≥ 1 − q∗2 ,          λmin ((U ⊙ W ) (U ⊙ W )) ≥ 1 − q∗2 ,
                 λmin ((U ⊙ V )⊤ (U ⊙ V )) ≥ 1 − q∗2 .

    Conditional on any fixed instance in Esm , uniformly in i, j,
                                                                 
                                   Pr (Eij ) = Θ r−5/3 (log r)−3/2 ,
                                     prop

    with universal comparison constants. Hence the displayed k = o(r2 ) gives one-run simultaneous
    target coverage with probability at least 26/27.
    On coverage, certification, unlabeled clustering, synchronized landing, and cyclic refinement
    return at most k terms with relative Frobenius residual at most ϵ. With

                                      J = max {1, ⌈Crep log(1/δinit )⌉}

    independent completed runs, conditional success is at least 1 − δinit , so joint success is at least
    (1 − δsm )(1 − δinit ). Every tape terminates, and the dense arithmetic work is polynomial in
    n, r, κ0 , ρ−1 , log(1/ϵ), log(1/δinit ).



                                                         15
VALG                                                                             ML Theory Research Agent




Discussion. This is partial progress. It preserves the smoothed CP model, the strictly subquadratic
rank k = Θ(r5/3 (log r)5/2 ), arbitrary relative accuracy, polynomial time, and nested high-probability
success. Its partiality comes from added bounded-scale, weak-interference, weight-balance, and
smoothing/dimension assumptions. The chosen mechanism is a certified proposal, synchronized-
landing, and cyclic-ALS pipeline with independent restarts.
Technical role and remaining barrier. The source setting leaves two technical barriers. First,
arbitrary base geometry can make the smoothed components indistinguishable and prevent the
proposal estimates from remaining uniform across components. Second, independently proposed
mode estimates do not automatically enter compatible target spans. Bounded scales and near-
balanced weights control component magnitudes, weak interference separates components, and the
smoothing/dimension margin preserves these properties after perturbation; together they close the
proposal recurrences. Certification and synchronized landing then align the three modes before
cyclic ALS refinement. The remaining problem is to prove the same rank, accuracy, running-time,
and probability guarantees for arbitrary source-admissible base triples without the added structural
assumptions.
4.1.2 Subproblem 2: Lower Bound

 Open question. Is there a universal c > 0 such that, for r < k ≤ r1+c , ALS, gradient descent,
 or another iterative method converges with constant probability to a strictly positive objective
 value?
Perspective 1.
Formalized setting and preliminaries. Let r, n, k be positive integers, let q > 0, and set ρ = r−q .
For arbitrary deterministic Ā, B̄, C̄ ∈ Rn×r , independently smooth their columns by N (0, ρ2 In /n)
to obtain
                                               Xr
                                         T =       aj ⊗ b j ⊗ c j .
                                                 j=1

For X, Y, Z ∈ Rn×k , set S(X, Y, Z) = i xi ⊗ yi ⊗ zi and F (X, Y, Z) = 12 ∥T − S(X, Y, Z)∥2F . Here
                                          P
T(m) is the mode-m matricization and ⊙ is the Khatri–Rao product.
   For each M ∈ {cALS, cGD}, draw an independent Gaussian triple GM               M    M
                                                                             x , Gy , Gz with iid
N (0, 1/n) entries. Let QM = orth(GM x ), where orth is a fixed measurable choice of orthonormal
basis for the column space, SM = range(GM x ), and

                      HM = SM ⊗ Rn ⊗ Rn ,              PHM = (QM Q⊤
                                                                  M ) ⊗ I n ⊗ In .

The methods share T but have independent starts. The constrained sequential ALS method
initializes at its Gaussian triple and, in X, Y, Z order, uses

                   Xt+1 = QcALS Q⊤          x    x ⊤ x †     x
                                 cALS T(1) Kt ((Kt ) Kt ) , Kt = Zt ⊙ Yt ,
                   Yt+1 = T(2) Kty ((Kty )⊤ Kty )† ,              Kty = Zt ⊙ Xt+1 ,
                   Zt+1 = T(3) Ktz ((Ktz )⊤ Ktz )† ,              Ktz = Yt+1 ⊙ Xt+1 .

Thus only Xt is constrained to its fixed initialization span. All three displayed updates are
Moore–Penrose minimum-norm solves, including when a design Gram is singular.
    The constrained GD method writes Xt = QcGD Ct and fQ (C, Y, Z) = F (QcGD C, Y, Z).
Initialize at
                          (C0 , Y0 , Z0 ) = (Q⊤    cGD
                                              cGD Gx   , GcGD
                                                          y   , GcGD
                                                                 z   ),



                                                       16
   VALG                                                                           ML Theory Research Agent




   and, testing j = 0, 1, 2, . . . in increasing order, choose the first dyadic ηt = 2−j satisfying, for
   ut = (Ct , Yt , Zt ),
                                                                  ηt
                               fQ (ut − ηt ∇fQ (ut )) ≤ fQ (ut ) − ∥∇fQ (ut )∥2F ,
                                                                  2
   and take that step. Both methods iterate the displayed updates from their specified starts. Write
   StM = S(XtM , YtM , ZtM ) and FM (t) = F (XtM , YtM , ZtM ). The gradient norm is the combined
   Frobenius norm of the C, Y, Z blocks.
   Technical assumptions.
   Assumption 4.9 (Fixed ambient dimension). n ≥ 8r5/4 .
   Assumption 4.10 (Superlinear algorithmic rank). r < k ≤ r5/4 ; equivalently, the exponent is
   α = 1/4.
   Assumption 4.11 (Uniform arbitrary deterministic bases). The deterministic base triple is unre-
   stricted, and the claim is pointwise uniform over all such triples.
   Assumption 4.12 (Independent Gaussian smoothing). q > 0 is fixed, ρ = r−q , and the 3r
   smoothing vectors are mutually independent with covariance (ρ2 /n)In .
   Assumption 4.13 (Shared target and independent starts). The two initialization triples are
   mutually independent and independent of smoothing, while both methods use the same realized T .

Main theory.
     Theorem 4.2 (Fixed-span positive limiting objective). Under Assumptions 4.9–4.13, with
     probability at least 1/4 over smoothing and both starts, simultaneously for M ∈ {cALS, cGD},
                                      3                        3
                    ∥(I − PHM )T ∥2F ≥ ∥T ∥2F ,        FM (t) ≥ ∥T ∥2F   for every t ≥ 0,
                                      4                        8
     and FM (t) has a finite scalar limit satisfying
                                                       3
                                           lim FM (t) ≥ ∥T ∥2F .
                                           t→∞         8
    The statement holds for every admissible r, n, k and is pointwise uniform in the deterministic
    base triple.

   Discussion. This is partial progress. It preserves arbitrary base factors, the smoothed tensor
   model, Gaussian initialization, every r < k ≤ r5/4 , and the goal of a strictly positive limiting loss
   with constant probability. The main change is algorithmic: cALS and cGD constrain one factor to
   its initialization span. The result also assumes n ≥ 8r5/4 and uses specified minimum-norm ALS
   and Armijo-GD updates.
   Technical role and remaining barrier. The source algorithms present a trajectory-control
   barrier: an unconstrained update can leave the initialization span, so the proof loses the fixed
   subspace used to obstruct exact recovery. Constraining the X factor keeps every represented tensor
   in the fixed space SM ⊗ Rn ⊗ Rn . With constant probability, the target has a nonzero component
   orthogonal to this space, which forces positive loss. The dimension condition gives k/n ≤ 1/8 and
   hence a constant-probability orthogonal-residual witness, while the specified descent rules ensure
   that the loss converges. The remaining problem is to prove, under the same smoothed model,
   dimension condition, and rank window, the corresponding constant-probability positive-limit result
   for unconstrained sequential minimum-norm ALS and full-variable Armijo GD. Returning to the
   full source contract additionally requires removing or justifying the dimension restriction n ≥ 8r5/4 .

                                                       17
VALG                                                                                            ML Theory Research Agent




Perspective 2.
Formalized setting and preliminaries. Fix κ ≥ 1, q > 0, and positive integers n, r, k, and put ρ = r−q .
For deterministic Ā, B̄, C̄ ∈ Rn×r with nonzero columns, let A,    e B,e C
                                                                          e be their column-normalized
versions. Independently over j and modes, draw ξj , ξj , ξj ∼ N (0, ρ2 In /n), set aj = āj + ξja ,
                                                           a  b  c

bj = b̄j + ξjb , and cj = c̄j + ξjc , and form T = rj=1 aj ⊗ bj ⊗ cj . For X, Y, Z ∈ Rn×k , let
                                                  P

                                   k
                                   X
                  Tb(X, Y, Z) =          xi ⊗ yi ⊗ zi ,     L(X, Y, Z) = ∥T − Tb(X, Y, Z)∥2F .
                                   i=1

Write Tbt = Tb(Xt , Yt , Zt ) and use the standard mode matricizations and Khatri–Rao product below.
From an iid N (0, 1/n) initialization, compute the three minimum-norm least-squares candidates in
parallel from the old iterate:
                                 Utx = Zt ⊙ Yt ,      ls
                                                     Xt+1 = T(1) Utx ((Utx )⊤ Utx )† ,
                                 Uty = Zt ⊙ Xt ,        ls
                                                      Yt+1 = T(2) Uty ((Uty )⊤ Uty )† ,
                                 Utz = Yt ⊙ Xt ,       ls
                                                      Zt+1 = T(3) Utz ((Utz )⊤ Utz )† .
       raw , Y raw , Z raw ) to the componentwise averages of the old factors and these candidates. For
Set (Xt+1     t+1     t+1
each positive-norm component triple, replace all three norms by their geometric mean; if a norm is
zero, replace the triple by (0, 0, 0). This gauge preserves the represented tensor. The method is
unconstrained half-relaxed parallel ALS.
   Let ΛA = (Ā⊤ Ā)−1 Ā⊤ , and define ΛB , ΛC analogously and Q = ΛA ⊗ ΛB ⊗ ΛC . Put
                                                          r
                                                          X                   k
                                                                              X
  pi,t = (ΛA xi,t ) ⊗ (ΛB yi,t ) ⊗ (ΛC zi,t ),    Dr =          e⊗3
                                                                 j ,   Ct =         pi,t ,   St = span{pi,t : i ∈ [k]},
                                                          j=1                 i=1

Pt = ProjSt , ∆0 = distF (Dr , S0 ), and Eρ = QT − Dr . These definitions give the exact identity

                                  Q(T − Tbt ) = Dr + Eρ − Ct ,             Ct ∈ St .

The spaces St evolve adaptively, and both coefficient and ambient tensor spaces use Frobenius
geometry. For LP < δ/4 and ζ < δ/4, define C2 (δ, LP , ζ, CT ) by four clauses:
                        √
   1. ∆0 ≥ δ∥Dr ∥F = δ r;
      P
   2.   t≥0 ∥Pt+1 − Pt ∥op ≤ LP ;
      P
   3.   t≥0 ∥Tt+1 − Tt ∥F < ∞;
             b      b

   4. ∥Eρ ∥F ≤ ζ∥Dr ∥F and ∥T ∥F ≤ CT ∥Dr ∥F , where CT = CT (κ, q) is independent of r, n, k and
      the base triple.
The event C2 is an outcome-dependent certificate. Its role is transparent: the projector-path
clause preserves the initial coefficient deficit at every time,

                                         distF (Dr , St ) ≥ (δ − LP )∥Dr ∥F ,

while the same-target identity, the smoothing clause, and ∥Q∥op ≤ κ6 give the all-time physical
residual bound
                                                δ − LP − ζ
                                  ∥T − Tbt ∥F ≥             ∥T ∥F .
                                                    κ6 C T
The unsquared finite-variation clause makes (Tbt )t Cauchy, so the objective has a finite limit.

                                                           18
   VALG                                                                             ML Theory Research Agent




   Technical assumptions.

   Assumption 4.14 (Ambient dimension). n ≥ Cdim (κ, q)r4 log r.

   Assumption 4.15 (Full superlinear rank window). r < k ≤ r5/4 .

   Assumption 4.16 (Well-conditioned deterministic bases). Every base-column norm and every
   singular value of each column-normalized base matrix lie in [κ−1 , κ].

   Assumption 4.17 (Independent Gaussian smoothing). ρ = r−q , and the 3r smoothing vectors have
   the independent Gaussian law above.

   Assumption 4.18 (Independent Gaussian initialization). All 3nk initial factor entries are iid
   N (0, 1/n) and independent of smoothing.

       All probabilities refer to the joint law conditional on the deterministic base triple.
Main theory.
     Theorem 4.3 (Conditional positive limiting loss). Under Assumptions 4.14–4.18, let r0 ∈ N
     and Cdim , δ, LP , ζ, CT > 0 depend only on (κ, q), with LP < δ/4 and ζ < δ/4, and define
                                                               2
                                                   δ − LP − ζ
                                          ϵ=                         > 0.
                                                      κ6 CT

     For every r ≥ r0 , admissible n, k and base triple, the displayed half-relaxed trajectory satisfies
     the deterministic event inclusion
                                         (                                               )
                                           limt→∞ L(Xt , Yt , Zt ) exists and is finite,
                   C2 (δ, LP , ζ, CT ) ⊆                                                   .
                                           limt→∞ L(Xt , Yt , Zt ) ≥ ϵ∥T ∥2F

     The inclusion is pointwise under the joint smoothing-and-initialization law conditional on the
     base triple. In the separate deterministic zero-smoothing baseline with n ≥ r and orthonormal
     base columns, QT = Dr , Eρ = 0, ∥Q∥op = 1, and ∥T ∥F = ∥Dr ∥F ; the first three applicable
     certificate clauses imply
                                    lim L(Xt , Yt , Zt ) ≥ (δ − LP )2 ∥T ∥2F .
                                    t→∞

   Discussion. This is partial progress. It preserves the smoothed CP loss, Gaussian initialization,
   every r < k ≤ r5/4 , and the target of a positive relative limiting loss. The decisive change is that
   the conclusion is conditioned on the trajectory certificate C2 (δ, LP , ζ, CT ), which requires an initial
   deficit, controlled motion of the adaptive span, controlled smoothing and scale, and finite tensor
   variation. The theorem also uses well-conditioned bases, a high-dimensional regime, and half-relaxed
   balanced parallel ALS.
   Technical role and remaining barrier. The source setting leaves two trajectory barriers: the
   adaptive coefficient span can rotate until it absorbs the initial deficit, and the represented tensor
   is not known to converge. The certificate controls projector motion to preserve the deficit, uses
   the smoothing and scale bounds to transfer that deficit to a physical residual, and imposes finite
   tensor variation to make the trajectory Cauchy. Well-conditioning controls the coefficient-to-tensor
   transfer, while the dimension regime and modified dynamics support the certificate conditions.
   These clauses yield a positive limiting loss. The immediate missing proposition is to prove that, for
   suitable constants depending only on (κ, q),

                                     Pr[C2 (δ, LP , ζ, CT )] ≥ p0 (κ, q) > 0

                                                        19
VALG                                                                                      ML Theory Research Agent




uniformly over the admitted parameters and bases. Even this would establish only the restricted
well-conditioned, high-dimensional, half-relaxed balanced parallel-ALS result. Returning to the
source problem additionally requires a constant-probability positive-limit theorem without those
geometric, dimensional, and algorithmic restrictions.
Perspective 3.
Formalized setting and preliminaries. Fix κ ≥ 1, q ≥ 4, and positive integers n, r, k, and put
ρ = r−q . For deterministic Ā, B̄, C̄ ∈ Rn×r with nonzero columns, write Ā◦ , B̄ ◦ , C̄ ◦ for their
column-normalized versions. Independently over j and modes, draw ξja , ξjb , ξjc ∼ N (0, ρ2 In /n) and
set aj = āj + ξja , bj = b̄j + ξjb , and cj = c̄j + ξjc . With A = [aj ], B = [bj ], and C = [cj ], write

      r                                                r                                     k                     2
      X                                                X                                     X
T =         aj ⊗bj ⊗cj = (A⊗B ⊗C)Dr ,           Dr =         e⊗3
                                                              j ,     F (X, Y, Z) = T −             xi ⊗ yi ⊗ zi       .
      j=1                                              j=1                                    i=1                  F

Let G balance every component with three positive norms to their geometric mean, preserving its
rank-one product, and leave a component with a zero factor unchanged. Apply G to an iid N (0, 1/n)
initialization and after every simultaneous full-batch gradient step, where θt = (Xt , Yt , Zt ):
  et+1 = Xt − η∇X F (θt ),
  X                            Yet+1 = Yt − η∇Y F (θt ),        Zet+1 = Zt − η∇Z F (θt ),           η = (nkr)−12 .

This defines balanced full-variable gradient descent.
   On the full-rank event, set αi,t = A† xi,t and define βi,t , γi,t analogously, and set ᾱi,0 = n/r αi,0 ,
                                                                                                 p

with the same convention for β̄i,0 , γ̄i,0 . Put
                                        X                                  1
                                 D
                                 b0 =         αi,0 ⊗ βi,0 ⊗ γi,0 ,     δ0 = ,
                                                                           8
                                         i

and let S0 be the span, over i ∈ [k], of

                         Rr ⊗ βi,0 ⊗ γi,0 ,    αi,0 ⊗ Rr ⊗ γi,0 ,    αi,0 ⊗ βi,0 ⊗ Rr .

Replacing the fixed coordinates by their barred versions leaves this tangent span unchanged. With
κ1 = 2κ2 , define Einit norm as the intersection of:

   1. ∥M ∥op ≤ κ1 and σmin (M ) ≥ κ−1
                                   1 for M = A, B, C;

   2. all eigenvalues of the three normalized pair Grams [β̄i,0 ⊗ γ̄i,0 ]⊤
                                                                         i [β̄i,0 ⊗ γ̄i,0 ]i and its cyclic
      analogues lie in [r−20 , r20 ];

   3. some unit W0 ⊥ S0 satisfies ⟨Dr − D
                                        b 0 , W0 ⟩F ≥ δ0 ∥Dr ∥F ;

   4. maxi,m∈{x,y,z} ∥mi,0 ∥2 ≤ 2.

The normalized pair Grams equal (n/r)2 times their raw counterparts. For θ = (X, Y, Z), define
                                                                              X
        dbal (θ, θ′ )2 = ∥X − X ′ ∥2F + ∥Y − Y ′ ∥2F + ∥Z − Z ′ ∥2F , Epath =   dbal (θt+1 , θt ),
                                                                                    t≥0

and CCP (κ, R) = κ31 (1 + 3R). The sole trajectory certificate is
                               ( s               )
                                         δ0
                     E⋆ = min 1,                   ,  Cpath = {Epath ≤ E⋆ }.
                                    16CCP (κ, 3)

                                                        20
   VALG                                                                                     ML Theory Research Agent




   Technical assumptions.

   Assumption 4.19 (Well-conditioned deterministic bases). Every base-column norm and every
   singular value of each column-normalized base matrix lie in [κ−1 , κ].

   Assumption 4.20 (Smoothed dimension regime). q ≥ 4 is fixed, r is sufficiently large, and
   n ≥ C(κ, q)r4 log r.

   Assumption 4.21 (Universal superlinear rank window). r < k ≤ ⌊r5/4 ⌋.

   Assumption 4.22 (Independent Gaussian smoothing). All smoothing vectors have the independent
   law N (0, r−2q In /n) and are independent of initialization.

   Assumption 4.23 (Gaussian initialization). Before balancing, all entries of X0raw , Y0raw , Z0raw are
   iid N (0, 1/n).

   Assumption 4.24 (Fixed balanced gradient-descent protocol). The protocol uses the simultaneous
   full-batch update, step size η = (nkr)−12 , and map G specified above.

Main theory.
     Theorem 4.4 (Conditional positive-loss certificate). Under Assumptions 4.19–4.24, there are
     r0 (κ, q) and C(κ, q) such that, uniformly over every

                         r ≥ r0 (κ, q),     n ≥ C(κ, q)r4 log r,              r < k ≤ ⌊r5/4 ⌋,

     and every admissible deterministic base triple,

                                           Pr(Einit norm ) ≥ 1 − r−10 .

    With                                                        2
                                                         15
                                          ϵ0 (κ) =          δ0        κ−12
                                                                       1   > 0,
                                                         16
     on Einit norm ∩ Cpath the balanced iterates converge in dbal to a finite θ∞ and

                                    lim F (θt ) = F (θ∞ ) ≥ ϵ0 (κ)∥T ∥2F > 0.
                                   t→∞

     Consequently, if F+ is this convergence-and-positive-limit event,

                                 Pr(F+ ) ≥ (1 − r−10 ) Pr(Cpath | Einit norm ).

     Probabilities are under the joint smoothing-and-initialization law conditional on the deterministic
     base triple.

   Discussion. This is partial progress. It preserves the smoothed CP loss, Gaussian initialization,
   every r < k ≤ ⌊r5/4 ⌋, simultaneous all-factor gradient steps, and the target of a positive relative
   limiting loss. The decisive added condition is the finite-path event Cpath . The analyzed dynamics
   additionally use well-conditioned bases, a high-dimensional regime, a tiny fixed step, and product-
   preserving balancing after every step.
   Technical role and remaining barrier. The source setting leaves a global trajectory barrier: a
   tiny step controls each update locally but does not bound the total motion, accumulated nonlinear
   error, or convergence of the iterates. The finite-path event bounds this total motion, keeps the
   balanced iterates in the region where the initial tangent-deficit witness survives, and controls the

                                                           21
VALG                                                                              ML Theory Research Agent




accumulated Taylor remainder. Well-conditioning transfers this witness to physical loss, while
product-preserving balancing controls factor scales along the finite path. This yields convergence to
a positive limiting loss. The immediate missing proposition is to prove that, for some p0 (κ, q) > 0,

                                    Pr(Cpath | Einit norm ) ≥ p0 (κ, q)

uniformly over the admitted parameters and bases. Even this would establish only the restricted
well-conditioned, high-dimensional, tiny-step balanced method. Returning to the source problem
additionally requires removing these geometric, dimensional, step-size, and balancing restrictions.

4.2 Is Interaction Necessary for Order-Optimal 1-bit Mean Estimation?

 Open question. Consider one-dimensional mean estimation over the nonparametric distribution
 family
                     n                                                        o
         D(k, λ, σ) = D : µ(D) := EX∼D [X] ∈ [−λ, λ], EX∼D |X − µ(D)|k ≤ σ k ,

 where k > 1 and λ ≥ σ > 0 are known to the learner. A 1-bit communication protocol observes
 independent samples X1 , ..., Xn ∼ D only through binary messages Yt = 1{Xt ∈ At }, where
 At ⊂ R is measurable. In a fully non-adaptive protocol, all sets A1 , ..., An are fixed before any
 messages are observed, possibly using public or private randomness. Threshold and interval
 queries correspond to At being a half-line or an interval, respectively. We say that a protocol is
 (ϵ, δ)-accurate over D(k, λ, σ) if its output µ̂ satisfies

                                      sup       P{|µ̂ − µ(D)| > ϵ} ≤ δ.
                                   D∈D(k,λ,σ)

 The adaptive 1-bit minimax sample complexity is known:
                                            2
                                             σ      1
                                            ϵ2 log δ ,        k > 2,
                                           
                                           
                                           
                                           
                                         λ    2
                    rk (λ, σ, ϵ, δ) = log + σ log σ log 1 ,    k = 2,
                                         σ 
                                            ϵ2     ϵ   δ
                                            σ k/(k−1) log 1 , 1 < k < 2.
                                           
                                               
                                           
                                               ϵ            δ
 The open question of Lau and Scarlett (2026a) asks whether fully non-adaptive arbitrary 1-bit
 quantizers can achieve the adaptive minimax rate?

4.2.1 Subproblem 1: Order-Optimal Non-Adaptive 1-Bit Mean Estimation

 Open question. Fix k > 1. Do there exist constants ck , Ck > 0 such that, for all λ ≥ σ > 0, all
 0 < ϵ ≤ ck σ, and all δ ∈ (0, 1/2), there is a fully non-adaptive 1-bit protocol that is (ϵ, δ)-accurate
 over D(k, λ, σ) using at most n ≤ Ck rk (λ, σ, ϵ, δ) samples?

Perspective 1.
Formalized setting and preliminaries. Fix k > 1, known λ ≥ σ > 0, accuracy ϵ > 0, and confidence
δ ∈ (0, 1/2). For a law D on R, define
                            n                                                  o
               D(k, λ, σ) := D : µ(D) = ED X ∈ [−λ, λ], ED |X − µ(D)|k ≤ σ k .




                                                     22
VALG                                                                                ML Theory Research Agent




This is the unrestricted central-k-moment class. The target sample complexity is
                                               2
                                                σ      1
                                              
                                              
                                                  2
                                                    log ,         k > 2,
                                                ϵ      δ
                                              
                                              
                                              
                                            λ    2
                      rk (λ, σ, ϵ, δ) := log + σ log σ log 1 ,    k = 2,
                                            σ 
                                               ϵ2     ϵ   δ
                                               σ k/(k−1) log 1 , 1 < k < 2.
                                              
                                                
                                              
                                                  ϵ            δ
    Split the indices in advance into localization and refinement blocks. Localization uses the fully
non-adaptive balanced-code construction of Lau and Scarlett (2026b, Theorem 16) at confidence δ/4:
it uses precommitted Borel union-of-cell queries and returns a center c defined for every transcript.
Write Nloc for the number of localization queries. For finite constants Lk , Cloc,k depending only on
k, its theorem-level contract is
                                                                                     
                                             δ                            λ         4
               Pr{|c − µ(D)| ≤ Lk σ} ≥ 1 − ,        Nloc ≤ Cloc,k 1 + log + log         .
                                             4                            σ         δ

The refinement bank is also fixed before communication. For k-only constants γk ∈ (0, 1)
and bk ≥ 1, set
                                   σ 1/(k−1)              
                                                          H∗
             h0 = γk ϵ, H∗ = bk σ              , J = log2      , hj = 2j h0 .
                                    ϵ                     h0

For 0 ≤ j < J, give the fine levels hj ≤ σ weights hj /σ and the coarse levels hj > σ weights
(hj /σ)2−k ; normalize within each nonempty group and give each nonempty group equal total mass.
Denote the resulting level probabilities by pj . With S = {0, 1/4, 1/2, 3/4}, define
                                                   
                                            x − ahj
                      Qj,a (x) = ahj + hj             ,  Fj,a,b = Qj,a − Qj+1,b .
                                              hj
                                                                                          iid
Independently for every refinement sample i, draw Li ∼ (p0 , . . . , pJ−1 ), Ai , Bi ∼ Unif(S), and
Ui ∼ Unif[−1, 2], all before any response, and transmit
                                                                 
                                            FLi ,Ai ,Bi (Xi )
                                    Yi = 1                    ≥ Ui .
                                                  hLi

   At decoding time, choose the unique aj (c) ∈ S such that {c/hj − aj (c)} ∈ [3/8, 5/8), and form

                                      48hLi
                           Zi (c) =         1{(Ai , Bi ) = (aLi (c), aLi +1 (c))}
                                       pLi                          
                                                 FLi ,Ai ,Bi (c)
                                      × Yi − 1                   ≥ Ui .
                                                       hLi

Choose a positive integer s and an odd positive integer q, both as functions of the public parameter
tuple, partition the refinement indices in advance into q blocks of size s, and output
                                                                  
                                                       1 X
                               µ
                               b = c + median1≤g≤q          Zi (c) .
                                                       s
                                                              i∈Gg

Localization supplies the decoder-side shift, centering, and importance weights, while all queries
remain precommitted.

                                                     23
   VALG                                                                               ML Theory Research Agent




   Technical assumptions.

   Assumption 4.25 (Parameter domain). The exponent k > 1 is fixed and known, λ ≥ σ > 0 are
   known, δ ∈ (0, 1/2), and 0 < ϵ ≤ ck σ, where ck ∈ (0, 1) depends only on k.

   Assumption 4.26 (Unrestricted central moment class). The samples have a common law D ∈
   D(k, λ, σ).

   Assumption 4.27 (Independent samples and precommitted seeds). All samples are independent
   with common law D. The sample split, median blocks, localization randomness, and every refinement
   seed are mutually independent where appropriate and fixed before the first response bit.

Main theory.
     Theorem 4.5 (Order-optimal noninteractive one-bit mean estimation). Under Assump-
     tions 4.25– 4.27, one may take ck = e−1 , γk = 1/8, choose bk as a function only of k,
     and choose s and the odd q as functions of the public tuple (k, λ, σ, ϵ, δ). The resulting Borel
     query bank is fixed before the first response, uses exactly one bit from each of n = Nloc + qs
     independent samples, and satisfies, for a finite Ck depending only on k,

                    n ≤ Ck rk (λ, σ, ϵ, δ),      sup         Pr        {|b
                                                                         µ − µ(D)| > ϵ} ≤ δ.
                                              D∈D(k,λ,σ) D, protocol

    The probability is unconditional over both sample blocks and all protocol randomness, the horizon
    is deterministic, and the loss is absolute error on R.

   Discussion. This theorem matches the source problem’s full scope over the unrestricted central-k-
   moment class. Together with the known one-bit minimax lower bound, its rate is order-optimal.
   Both query banks are precommitted, and localization is a decoder-side operation.
   Perspective 3.
   Formalized setting and preliminaries. For k > 1 and known λ ≥ σ > 0, define

                    D(k, λ, σ) = {D : µ(D) = ED X ∈ [−λ, λ], ED |X − µ(D)|k ≤ σ k }.

   This is the unrestricted central-k-moment class. Its three-regime target rate is
                                                  2
                                                   σ      1
                                                       log ,          k > 2,
                                                 
                                                 
                                                 
                                                 
                                                  ϵ2     δ
                                               λ    2
                          rk (λ, σ, ϵ, δ) = log + σ log σ log 1 ,     k = 2,
                                               σ 
                                                  ϵ2     ϵ    δ
                                                  σ              1
                                                 
                                                  k/(k−1)
                                                              log , 1 < k < 2.
                                                 
                                                     ϵ            δ
   Split the samples in advance into localization and refinement blocks. The first uses the coding-based
   fully non-adaptive localizer of Lau and Scarlett (2026b, Theorem 16) at confidence δ/4. Let Rloc
   be a public localization seed, independent of all samples and fixed before any response bit. The
   localizer uses precommitted Borel queries Bi (Rloc ) and an always-defined decoder output
                                                                            
                                c = Decloc Rloc , (1{Xi ∈ Bi (Rloc )})i∈Iloc .

   For finite constants Lk , Cloc,k depending only on k, the localizer satisfies
                                                                                           
                                            δ                                      λ      4
              Pr{|c − µ(D)| ≤ Lk σ} ≥ 1 − ,        Nloc := |Iloc | ≤ Cloc,k 1 + log + log     .
                                            4                                      σ      δ

                                                       24
VALG                                                                                        ML Theory Research Agent




   For k-only ak , bk > 0, let

                      h0 = ak σ,      H∗ = bk σ(σ/ϵ)1/(k−1) ,        S = ⌈log2 (H∗ /h0 )⌉ ,
                                                                             S
                                               h2−k
                                                s
                                                                             X
                      hs = 2s h0 ,     ps =         ,              ZS =            h2−k
                                                                                    s   .
                                                ZS
                                                                             s=0

On the dyadic grid, set Ps,j = [jhs , (j + 1)hs ), ms,j = (j + 1/2)hs , and Js,j = Ps,j−1 ∪ Ps,j ∪ Ps,j+1 .
Define the rings
                         R0,j = J0,j ,      Rs,j,b = Js,j \ Js−1,2j+b (s ≥ 1),
and color indices by Js,ℓ = {j : j ≡ ℓ (mod 4)}. Half-open cells fix all boundary ties.
   For each refinement sample i, independently precommit Li ∼ (p0 , . . . , pS ), Ci ∼
Unif{0, 1, 2, 3}, Ui ∼ Unif[−1, 1], and a countable independent Rademacher mask (ρi,s,j ). If
Li = s ≥ 1, also precommit independent Ti ∼ Unif{coord, mass} and Bi ∼ Unif{0, 1}; at s = 0,
take Ti = coord. With ψs,j,coord (x) = (x − ms,j )/(2hs ) and ψs,j,mass (x) = 1, define
                                                x − m0,j
                                X
                               
                                        ρi,0,j            1R0,j (x),    Li = 0,
                               
                                                  2h0
                                 j∈J0,Ci
                      Fi (x) =     X
                               
                               
                                        ρi,s,j ψs,j,Ti (x)1Rs,j,Bi (x), Li = s ≥ 1.
                               
                                     j∈Js,Ci


Each refinement sample transmits the single bit Yi = 1{Fi (Xi ) ≥ Ui }. The decoder computes
Yi0 = 1{0 ≥ Ui } and ∆Yi = Yi − Yi0 .
    After the complete transcript arrives, choose

                          j0 (c) = min argmin |c − m0,j |,          m0 (c) := m0,j0 (c) ,
                                           j∈Z

and set for s ≥ 1

            js = ⌊j0 (c)/2s ⌋ ,      bs = js−1 − 2js ,        ms = ms,js ,            ds = ms − m0 (c),

with κs = js mod 4. The decoder retains and reweights the precommitted bits through
            16h0
          
           p 1{Ci = κ0 }ρi,0,j0 (c) ∆Yi ,                                          Li = 0,
          
          
               0
 Wi (c) =
            16                                                              
           1{Ci = κs , Bi = bs }ρi,s,js 4hs 1{Ti = coord} + 2ds 1{Ti = mass} ∆Yi , Li = s ≥ 1.
          
          
            ps
Finally, for k-only αk , βk > 0, preassign

                                                                       σ k ZS
                                                                           
                                           8
                            Gδ = 2 αk log      + 1,           Bref = βk 2       ,
                                           δ                             ϵ

equal-size median blocks and output
                                                                                     
                                                                   1     X
                            µ
                            b = m0 (c) + median1≤g≤Gδ                          Wi (c) .
                                                                  Bref
                                                                         i∈Gg

Localization selects the reconstruction path in the decoder, while all queries remain precommitted.



                                                         25
   VALG                                                                                ML Theory Research Agent




   Technical assumptions.
   Assumption 4.28 (Parameter domain). k > 1 is fixed and known, λ ≥ σ > 0 are known,
   δ ∈ (0, 1/2), and 0 < ϵ ≤ ck σ, for a positive k-only constant ck < 1.
   Assumption 4.29 (Unrestricted central-moment class). The common law belongs to the unrestricted
   class D(k, λ, σ).
   Assumption 4.30 (Independent observations and seeds). Both sample blocks are i.i.d. from D.
   All localization and refinement seeds are mutually independent where appropriate and independent
   of the observations.
   Assumption 4.31 (Precommitted protocol). The split, all seeds and masks, and the median blocks
   are fixed before any bit is observed. Every query is Borel and independent of earlier messages. The
   localization output enters the decoder after collection of the full transcript.

Main theory.
     Theorem 4.6 (Order-optimal fully non-adaptive one-bit mean estimation). Under Assump-
     tions 4.28– 4.31, for every fixed k > 1 there are k-only constants ck , Ck , ak , bk , αk , βk > 0 such
     that the protocol above is well defined and, for all admissible public parameters, uses one bit per
     independent sample at the deterministic horizon n = Nloc + Gδ Bref with

                     n ≤ Ck rk (λ, σ, ϵ, δ),       sup        Pr        {|b
                                                                          µ − µ(D)| > ϵ} ≤ δ.
                                               D∈D(k,λ,σ) D, protocol

    The guarantee is unconditional over all observations and protocol randomness, and uses absolute
    error on R. It retains the exact three regimes displayed above, including the single log(σ/ϵ)
    factor at k = 2, with all constants depending only on k.

   Discussion. This theorem matches the source problem’s full scope over the unrestricted moment
   class. Together with the known one-bit minimax lower bound, its rate is order-optimal. The
   masked multiscale bank is fully precommitted, and localization selects the reconstruction path in
   the decoder.

   4.3 Is the Power of Deep Learning over Linear Models Inherently
       Distribution Dependent?

    Open question. Ben-David et al. (2002) defined the dimension complexity dc(H) of a binary
    hypothesis class H ⊆ {±1}X as the smallest dimension d s.t. there exists a feature map
    φ : X → Rd allowing linear representation of H (i.e. s.t. ∀h∈H ∃w∈Rd ∀x h(x) = sign(⟨w, φ(x)⟩)).
    Using dimension complexity (dc(H)) to measure the smallest shared feature dimension in which
    a hypothesis class is linearly realizable, the open question of Feldman et al. (2026) asks whether
    distribution-independent SQ learning implies low dimension complexity, and whether anything
    learnable with (S)GD on a (benign) neural network under any input distribution is also learnable
    with a linear model.

   4.3.1 Subproblem 1: Learning with SGD over Neural Networks

    Open question. Is there a constant C such that for all H ⊆ {±1}X over X = {±1}n , and
    ϵ < 1/4, if there exists a fully connected ReLU network with S parameters in total, stepsize
    η and number of steps T , such that for every input distribution D, every h∗ ∈ H, SGD yields
    expected error ELD,h∗ (ĥ) ≤ ϵ (expectation over the initialization and SGD sampling), then


                                                         26
   VALG                                                                                       ML Theory Research Agent




     dc(H) ≤ C · T S.

   Perspective 3.
   Formalized setting and preliminaries. Fix n, m, T ≥ 1, η > 0, and ε ≥ 0. Let X = {−1, +1}n ,
   H ⊆ {−1, +1}X , and fix a tie label s0 ∈ {−1, +1}. Write signs0 (z) = sign(z) for z =
                                                                                       ̸ 0 and
   signs0 (0) = s0 , and define the strict error of a score g by

                                       LD,h (g) = Pr {signs0 (g(x))h(x) < 0}.
                                                    x∼D

   Consider the coordinatewise ReLU activation σ(z) = max{0, z} and the bias-free depth-
   two ReLU network

                     fa,W (x) = a⊤ σ(W x),          W ∈ Rm×n ,           a ∈ Rm ,      S = m(n + 1),
                                                                               (0)                      (0)
   with both layers trainable. Initialize independently with Wji ∼ N (0, 1/n) and aj ∼ N (0, 1/m).
   Given fresh x(t) ∼ D, run T ≥ 1 one-sample, all-layer SGD steps with fixed stepsize η > 0 and
   logistic loss ℓ(z) = log(1 + e−z ). Fix κkink ∈ [0, 1] once and use the ReLU derivative

                                       σκ′ kink (z) = 1{z > 0} + κkink 1{z = 0}

   in every gradient, so the SGD recursion is defined also at zero preactivations:
                                                                                                  
                    (a(t+1) , W (t+1) ) = (a(t) , W (t) ) − η∇(a,W ) ℓ h(x(t) )fa(t) ,W (t) (x(t) ) .

   The returned score is
                                                          T
                                                          X
                                             Gω (x) =              fa(t) ,W (t) (x),
                                                        t=⌈T /2⌉

   where ω includes initialization and all SGD samples.
      The deterministic dimension complexity dc(H) is the least dimension of one feature map that
   exactly represents every h ∈ H by a tie-resolved homogeneous halfspace. Its confident variant
   dc1/2 (H) is the least d for which a feature-map law P, chosen before (D, h), satisfies
                                                                       
                                                                             1
                             Pr inf Pr {signs0 (⟨w, φ(x)⟩)h(x) < 0} = 0 ≥
                            φ∼P w∈R x∼D
                                     d                                       2
   for every D and h. Let φid (x) = x ∈ Rn .
   Technical assumptions.
   Assumption 4.32 (Antipodally odd target class). Every h ∈ H satisfies h(−x) = −h(x) for
   all x ∈ X .
   Assumption 4.33 (Strict high-accuracy regime). The accuracy obeys the strict inequality
   2ε < 1/(n + 1).
   Assumption 4.34 (Universal source success). The width, stepsize, and horizon are fixed before the
   distribution and target, and for every D and h ∈ H,
                                                       
                                           Eω LD,h (Gω ) ≤ ε,

   where expectation is joint over the independent Gaussian initialization and fresh one-sample SGD
   draws.
Main theory.

                                                            27
VALG                                                                               ML Theory Research Agent




  Theorem 4.7 (Exact identity representation in the odd high-accuracy regime). Under As-
  sumptions 4.32, 4.33, and 4.34, the identity map exactly represents the class:

                       ∀h ∈ H ∃wh ∈ Rn ∀x ∈ X ,           signs0 (⟨wh , x⟩) = h(x).

  Hence the distribution- and target-independent law Pid = δφid succeeds with probability one for
  every (D, h), and
                                dc1/2 (H) ≤ dc(H) ≤ n ≤ S ≤ T S.

Discussion. This is partial progress. It preserves the Boolean domain, distribution-independent
learner parameters, Gaussian initialization, and all-layer SGD. It differs from the source problem in
three essential ways:
  (i) the network is bias-free and has depth two;
 (ii) every target is antipodally odd;
 (iii) the accuracy satisfies 2ε < 1/(n + 1).
Technical role and remaining barrier. Under the source setting, the proof faces three technical
barriers. First, the antisymmetric part of a general deep ReLU score can remain nonlinear, so it does
not directly define a shared linear feature map. Second, an arbitrary target may assign incompatible
labels to antipodal inputs, blocking the antipodal reduction. Third, the source condition ε < 1/4
is too weak to make a finite infeasibility witness contradict the learner guarantee. The added
restrictions resolve these barriers one by one: the bias-free depth-two architecture and the ReLU
identity σ(z) − σ(−z) = z linearize the antisymmetric score; target oddness aligns the labels on
antipodal pairs; and 2ε < 1/(n + 1) supplies the strict finite-witness gap. Together they yield
an exact representation by the identity features. The remaining problem is to obtain an O(T S)
common linear representation under the source assumptions, without these three restrictions.
Perspective 1.
Formalized setting and preliminaries. Let n be a positive integer, set X = {−1, +1}n , and let
H ⊆ {−1, +1}X . Write N0 = {0, 1, 2, . . .} and [r] = {1, . . . , r} for every positive integer r. Fix the
source tie label s0 ∈ {−1, +1}, and define
                                                  
                                                  +1, z > 0,
                                                  
                                    signs0 (z) = −1, z < 0,
                                                  
                                                    s0 , z = 0.
                                                  

Set
                            RD,h (w, φ) := Pr {signs0 (⟨w, φ(x)⟩)h(x) < 0}.
                                           x∼D
For α ≥ 0, define
                                                                                        
            dcα (H) := min d ∈ N0 : ∃P ∀D ∀h ∈ H,           Eφ∼P        inf RD,h (w, φ) ≤ α ,
                                                                    w∈Rd

where the law P is selected before (D, h).
   Consider a bias-free, fully connected ReLU network of positive integer depth L.PIts widths
n0 = n, n1 , . . . , nL−1 , nL = 1 are positive integers, and its parameter count is S = L    ℓ=1 nℓ nℓ−1 .
With z0 = x, uℓ = θℓ zℓ−1 , zℓ = max{0, uℓ } for ℓ < L, and fθ = θL zL−1 , initialize independently with
                                          (0)
                                        (θℓ )jk ∼ N (0, 1/nℓ−1 ).

                                                    28
   VALG                                                                                              ML Theory Research Agent




   Fix a ReLU-kink selector κ ∈ [0, 1]: derivatives at positive, negative, and zero preactivations are 1,
   0, and κ, respectively. For fresh x(t) ∼ D, run the exact all-layer recursion
                                                             
                                      (κ)
                   θ(t+1) = θ(t) − η∇θ ℓ h(x(t) )fθ(t) (x(t) ) ,    ℓ(a) = log(1 + e−a ),

   and return the tie-resolved latter-half score A(x) = Tt=⌈T /2⌉ fθ(t) (x).
                                                             P

      For r ≥ 0, let B∞ (θ(0) , r) = {θ : ∥θ − θ(0) ∥∞ ≤ r}, and define
                                          
                                          +∞,
                                                                               L = 1,
                                   (0)
                            Mr (θ ) =               inf          |uℓ,j (θ, x)|, L ≥ 2,
                                          θ∈B∞ (θ(0) ,r), x∈X ,
                                          
                                                        1≤ℓ<L, j∈[nℓ ]

                                                        (κ)
               Gr (θ(0) ) =           sup             ∥∇θ ℓ(yfθ (x))∥∞ ,          Er = {Mr > 0, ηT Gr ≤ r}.
                              θ∈B∞ (θ(0) ,r), x∈X ,
                                 y∈{−1,+1}

   This event depends only on initialization               and worst-case quantities over the fixed ball.
   Finally, for paths p = (i0 , . . . , iL−1 ) ∈ L−1
                                                Q
                                                  ℓ=0 [n ℓ define
                                                          ],
                                                L−1
                                                Y                                              L−1
                                                                                               Y
                         [φθ(0) (x)]p = xi0            1{uℓ,iℓ (θ(0) , x) > 0},      dpath =         nℓ .
                                                 ℓ=1                                           ℓ=0

   Let Pgate be the unconditional law of this map under Gaussian initialization, defined on both Er
   and Erc .
   Technical assumptions.

   Assumption 4.35 (Fixed source witnesses and regime). 0 ≤ ε < 1/4, T is a positive integer, and
   η > 0. For the given (n, H, ε), the architecture, S, η, T , and the fixed tie and kink conventions are
   selected once before every (D, h).

   Assumption 4.36 (Universal expected-error SGD premise). For every distribution D on X and
   every h ∈ H, the strict classification error of the prescribed latter-half predictor satisfies
                                                                              
                            Eθ(0) ,x(0) ,...,x(T −1) Pr {signs0 (A(x))h(x) < 0} ≤ ε.
                                                          x∼D

   Assumption 4.37 (Fixed constant depth). A universal positive integer L0 , independent of all
   problem and learner parameters, satisfies 1 ≤ L ≤ L0 . Widths are arbitrary and all layers remain
   trainable.

   Assumption 4.38 (Static robust initialization tube). Deterministic r > 0 and 0 ≤ δ0 ≤ ε are
   fixed before initialization, distribution, target, and SGD samples, and

                                                         Pr (Er ) ≥ 1 − δ0 .
                                                         θ(0)

  This initialization-only event is defined by worst-case quantities over the fixed ball. Trajectory
  containment, gate stability, and the path representation are derived from Er .

Main theory.



                                                                 29
VALG                                                                             ML Theory Research Agent




  Theorem 4.8 (Conditional polynomial probabilistic dimension). Under Assumptions 4.35,
  4.36, 4.37, and 4.38, the single unconditional law Pgate , chosen before every distribution and
  target, satisfies for all D and h ∈ H
                                                          
                                Eφ∼Pgate   inf RD,h (w, φ) ≤ ε + δ0 .
                                             d
                                         w∈R path

 Consequently,
                         dcε+δ0 (H) ≤ dpath ≤ S L ≤ S L0 ,   dc2ε (H) ≤ S L0 .
 The learner premise averages over initialization and the fixed finite SGD horizon; the tube
 premise is an initialization probability; and the conclusion averages over the unconditional
 feature-map law.

Discussion. This is partial progress. It preserves one Gaussian-initialized ReLU learner, finite-
horizon all-layer SGD, and uniform expected error over distributions and targets. It differs from the
source problem in four ways:

  (i) the initialization must satisfy a robust-tube condition with high probability;

 (ii) the network depth is bounded by a constant L0 ;

 (iii) the network is bias-free;

 (iv) the target is weakened to randomized approximate dimension dcε+δ0 (H) ≤ S L0 .

Technical role and remaining barrier. The source setting leaves three technical barriers.
Instance-dependent SGD can change hidden gates, so trajectories need not share a fixed feature map;
unrestricted depth can make the number of path features too large; and bad initializations cannot
be discarded when the target is deterministic and exact. The robust tube freezes the gates, the
depth cap bounds the path-feature dimension, and the bias-free architecture supports the displayed
homogeneous path-feature map; the randomized approximate target absorbs the bad-seed event.
These devices give a polynomial feature bound, but not the source’s exact linear O(T S) bound.
The remaining problem is to construct that common representation without the tube, depth cap,
bias-free restriction, or target relaxation.
4.3.2 Subproblem 2: Statistical Query Learning
A τ −statistical query (SQ) oracle for input distribution D and target h∗ , on input query q :
X × {±1} → [−1, 1] and tolerance τ returns an arbitrary value v such that |v − Ex∼D q(x, h∗ (x))| ≤ τ.
A (randomized) (m, τ )−statistical query (SQ) algorithm operates by making a sequence of m queries
to a τ −SQ oracle where each query can depend on all previous responses and can be selected at
random, and then returns a predictor ĥ : X → {±1}.

 Open question. Is there a constant C such that for every class H ⊆ {±1}X , over any domain
 X , and any ϵ < 1/4, if there exists an (m, τ )−SQ algorithm s.t. for every input distribution D
 and every h∗ ∈ H, the algorithm returns a predictor ĥ with ELD,h∗ (ĥ) ≤ ϵ (expectation over the
 randomness of the algorithm), then dc(H) ≤ C · m/τ 2 .

Perspective 2.
Formalized setting and preliminaries. Let (X , Σ) be an arbitrary measurable space, and let H
be a class of measurable maps from X to {−1, +1}. Write N0 = {0, 1, 2, . . .}. For a probability
measure D on (X , Σ), measurable target h, and measurable binary predictor g, write LD,h (g) =

                                                    30
   VALG                                                                             ML Theory Research Agent




   Prx∼D {g(x) ̸= h(x)}. Dimension complexity is the least d ∈ N0 for which one map φ : X → Rd ,
   measurable with respect to the Borel sigma-algebra on Rd , satisfies

                            ∀h ∈ H ∃wh ∈ Rd ∀x ∈ X ,         h(x)⟨wh , φ(x)⟩ > 0.

   If no such finite d exists, set dc(H) = +∞.
       Fix a randomized learner A with hidden seed U ∼ µA . Conditional on U = u, it makes at
   most m adaptive unrestricted queries qt : X × {−1, +1} → [−1, 1], measurable with respect to the
   product sigma-algebra, each selected from the seed and the preceding public transcript, and then
   returns a measurable binary predictor. All seed-, transcript-, query-, and output-coordinate maps
   are assumed measurable.
       A deterministic complete response rule R assigns a value in [−1 − τ, 1 + τ ] to every public
   query-bearing history admitted by A, including histories not reached by a particular seed or reply
   sequence. It does not observe the seed except through the public transcript. Let Rall A contain all
   such rules, and let gu,R be the terminal predictor. A complete rule is (D, h, τ )-valid if, at every
   round reached by every seed interacting with it,

                                        |vt − Ex∼D qt (x, h(x))| ≤ τ.

   Denote the valid rules by RA,τ (D, h). Accuracy below is required pointwise for every valid response
   rule.
       For every complete rule, define the seed-averaged terminal response and the static all-rule
   space
              FR (x) = EU ∼µA [gU,R (x)],    VA = spanR {FR : R ∈ Rall
                                                                     A },     rA = dim VA .
   Thus VA spans the seed-averaged terminal responses over all complete response rules.
   Technical assumptions.

   Assumption 4.39 (Primitive parameter regime). m ∈ N0 , τ > 0, and ε ∈ [0, 1/4). Fixed numerical
   constants B ≥ 1 and k ≥ 1 are independent of the domain, class, learner instance, parameters,
   distributions, targets, response rules, and seeds.

   Assumption 4.40 (Fixed randomized adaptive unrestricted-SQ interface). The learner A is fixed
   before D, h, and the response policy. It uses at most m adaptive bounded unrestricted queries, may
   use the full preceding real-valued public transcript, and interacts measurably with every deterministic
   complete response rule.

   Assumption 4.41 (Every-valid-policy universal guarantee). For every distribution D, every h ∈ H,
   and every R ∈ RA,τ (D, h),
                                      EU ∼µA LD,h (gU,R ) ≤ ε.
  The expectation is over the learner seed, uniformly for every valid R.

   Assumption 4.42 (Static polynomial mean-response-rank certificate). The rank over all
   deterministic complete response rules is finite and obeys
                                                           k
                                           rA ≤ B 1 + m/τ 2 .

  This primitive certificate on the seed-averaged responses is fixed before the learning instance.

Main theory.



                                                     31
VALG                                                                            ML Theory Research Agent




  Theorem 4.9 (Conditional static mean-response-rank theorem). Under Assumptions 4.39–
  4.42, choose once a basis ψ1 , . . . , ψrA of VA and define φA (x) = (ψ1 (x), . . . , ψrA (x)). This
  deterministic map is independent of the distribution, target, valid response policy, and realized
  seed. For every h ∈ H, some wh ∈ RrA satisfies
                                                     1
                      h(x)⟨wh , φA (x)⟩ ≥ 1 − 2ε >     >0      for every x ∈ X .
                                                     2
  Consequently,
                                                            k
                                    dc(H) ≤ rA ≤ B 1 + m/τ 2 .
  The conclusion is deterministic and pointwise.

Discussion. This is partial progress. It preserves arbitrary domains, adaptive randomized SQ
learning, adversarial tolerance-valid replies, and uniform success over distributions and targets.
The decisive added condition is a static polynomial-rank certificate for the seed-averaged terminal
responses. The resulting dimension bound is polynomial, B(1 + m/τ 2 )k , rather than the source
target O(m/τ 2 ).
Technical role and remaining barrier. The source SQ interface leaves a finite-dimensionality
barrier: adaptive real-valued transcripts do not by themselves place the terminal predictors in a
common finite-dimensional function space. The static rank certificate supplies that common space,
so seed averaging and exactification can produce a deterministic representation. The remaining
                                                                                              0
technical problem is to derive the source-scale compression from the SQ interface itself: if FD,h is
the seed-averaged terminal predictor under the canonical exact-center policy, then
                                            0
                                  dim span{FD,h : D, h} ≤ Cm/τ 2 .

4.4 Does Differential Privacy Make PAC Learning Much Harder?

 Open question. Denote V C(C) the Vapnik-Chervonenkis dimension for a hypothesis class
 C, LD(C) (Littlestone, 1988) the Littlestone dimension which is a combinatorial parame-
 ter characterizing online learnability. A randomized algorithm A : (X × {0, 1})n → W is
 (ϵ, δ)−Differentially Private (DP) (Dwork et al., 2016) if for every pair of neighboring datasets
 S, S ′ and every event E ⊆ W it holds that Pr[A(S) ∈ E] ≤ eϵ Pr[A(S ′ ) ∈ E] + δ. A private
 learner is a PAC learner that guarantees DP w.r.t. its training data. It is well known that DP
 learning requires more samples than non-private learning for some classes. Nissim et al. (2026)
 asks the central question: How much more is needed? Is the answer close to VC(C), or could it
 be drastically larger?

4.4.1 Subproblem 1: The Sample Complexity of Private Learning

 Open question. Identify a combinatorial measure of a class that determines the sample
 complexity of privately learning it, analogously to the characterization of non-private learning in
 terms of the VC dimension.

Perspective 1.
Formalized setting and preliminaries. Let (X, Σ) be a measurable space, C ⊆ {0, 1}X , and log be
natural. A Cartesian partition makes restriction bijective onto the blockwise product; it is finest if
                                                   (0)             (r)
it refines every such partition. For t ≥ 1, let log2 t = t, let log2 denote the r-fold iterate of the
                                                                     (r)
base-two logarithm for r ≥ 1, and write log∗ t = min{r ≥ 0 : log2 t ≤ 1}. For the finite finest


                                                  32
   VALG                                                                                   ML Theory Research Agent



                                                       Fk
   Cartesian partition specified below, write X =           i=1 Xi , Ci = {c|Xi : c ∈ C}, and, for a candidate
   positive integer n, set
                                                         X                     si
   di = LD(Ci ),   si = 1 + log∗ (di + 1),    M⊕ (C) =          si ,   ωi =          ,   mn,i = max{8, ⌈4nωi ⌉}.
                                                                              M⊕ (C)
                                                            i
                                                                                               (1)
   Identify x, x′ ∈ Xi when every ci ∈ Ci agrees on them, and write Qi = Xi /≡i , κi : Xi → Qi ,
   and Σi = {A ∩ Xi : A ∈ Σ}, giving Qi the discrete sigma-field 2Qi . Every ci ∈ Ci has a unique
   representative c̄i : Qi → {0, 1} satisfying ci = c̄i ◦ κi ; set
                                                                        Y
                           C̄i = {c̄i : ci ∈ Ci }, Hi = {0, 1}Qi , H⊕ =   Hi ,
                                                                                     i

   where Hi is the product sigma-field generated by finite evaluation cylinders and H ⊕ = i Hi . A
                                                                                               N
   quotient tuple h̄ = (h̄i )i ∈ H⊕ decodes as hh̄ (x) = h̄i (κi (x)) for x ∈ Xi .
       For a probability measure D on (X, Σ) and c ∈ C, let RD (h, c) = PrD [h(x) ̸= c(x)] and let Dc
   be the law of (x, c(x)). An unrestricted learner is a Markov kernel on fixed-size replacement-adjacent
   samples, including nonrealizable ones, with arbitrary measurable output Ω and decoder hΩ ; it may
   be joint, improper, or computationally unbounded. Finite evaluations and stated risk events are
   measurable. Define SCε,δ (C) as the least positive integer n for which such a private learner satisfies,
   for every c ∈ C and probability measure D on (X, Σ),

                                       Pr        [RD (hΩ , c) ≤ 1/16] ≥ 15/16.                                 (2)
                                S∼Dcn , Ω∼An (S,·)

   Technical assumptions.

   Assumption 4.43
                Fk (Canonical finite Cartesian factorization).QThere     is a finite finest Cartesian
                                                                  k
   partition X = i=1 Xi , k ≥ 1, with Ci = {c|Xi : c ∈ C} and C ≃ i=1 Ci .

   Assumption 4.44 (VC-one factors). Every Ci is nonconstant, has VC(Ci ) = 1, and has finite
   di .

   Assumption 4.45 (Measurable countable evaluation quotients). Each Xi ∈ Σ, each Qi is
   finite or countable, and each cell κ−1                                                             Qi
                                       i ({q}) belongs to Σi . Equivalently, κi : (Xi , Σi ) → (Qi , 2 ) is
   measurable.

      Consequently, every target and decoded hypothesis is Σ-measurable, and quotient decoding
   preserves distributional zero-one risk exactly.

   Assumption 4.46 (Approximate-DP range). 0 < ε ≤ 1/10 and 0 < δ < 1.

   Assumption 4.47 (Candidate-wise lower-bound budget). At the lower-bound candidate n,
                                 (                                    )
                                         1                 cδ
                     0 < δ ≤ min               , min                    ,                                      (3)
                                   n log(n + 1) i m2n,i log(mn,i + 1)

   where cδ > 0 is universal.

Main theory.
     Theorem 4.10 (Conditional private direct sum for Cartesian VC-one products). Under As-
     sumptions 4.43–4.46, let KY be the universal constant of the quotient-first VC-one learner of


                                                       33
VALG                                                                                ML Theory Research Agent




 Yan (2025), and define
                                             
                                  KY si     2 esi
                                                                       X
                             qi =       log       ,             Q⊕ =         qi .
                                   ε          εδ
                                                                         i

 With Cup = 65536 and Cquota = max{1, KY + 1/20}, route the first qi block records with
 fixed padding, run fixed permutation-symmetrized, fully totalized factor learners for C̄i into
 (Hi , Hi ) at (ε/2, δ/2), form their tuple in (H⊕ , H ⊕ ), and decode. This is a measurable all-input
 replacement-(ε, δ)-DP learner. For n ≥ ⌈Cup Q⊕ ⌉, (2) holds and
                                                                                
                                                          M⊕ (C)      2 eM⊕ (C)
                      SCε,δ (C) ≤ ⌈Cup Q⊕ ⌉ ≤ Cup Cquota          log              .               (4)
                                                             ε             εδ

 The upper bound holds throughout 0 < δ < 1.
 Conversely, for universal clow > 0, every candidate satisfying (3) and every unrestricted
 measurable replacement-(ε, δ)-DP learner satisfying (2) obey n ≥ clow M⊕ (C). Below this
 threshold some full-product target and arbitrary-support D with D(Xi ) = ωi satisfy

                                      Pr      [RD (hΩ , c) > 1/16] > 1/16.                            (5)
                             S∼Dcn , Ω∼An (S,·)

 When (3) holds at n∗ = SCε,δ (C), the lower bound applies at the sample-complexity threshold
 and combines with (4).

Discussion. This is partial progress. It preserves realizable binary PAC learning, arbitrary targets
and data distributions, approximate privacy, and unrestricted learners in the lower bound. The main
restriction is to Cartesian products of VC-one, finite-Littlestone factors with countable evaluation
quotients. Within this subclass it gives matching bounds up to privacy and logarithmic factors; the
lower bound additionally requires the stated small-δ condition.
Technical role and remaining barrier. The source setting leaves two structural barriers: a
general finite- Littlestone class has no factorwise decomposition to which threshold bounds apply,
and arbitrary evaluation spaces can make the learner construction non-measurable. Cartesian
VC-one structure supplies the factorwise direct sum, while countable evaluation quotients provide
a measurable quotient-first learner. The small-δ condition separately makes the threshold lower
bound applicable. The remaining problem is to obtain a comparable intrinsic characterization
for every measurable class of finite Littlestone dimension, without the Cartesian, VC-one, or
countable-quotient assumptions and without the candidate-wise small-δ restriction.
4.4.2 Subproblem 2: Class Existence

 Open question. Does there exist a sequence of finite-size classes C = {Cκ }κ∈N where: (1)
 limκ→∞ |Cκ | = ∞, (2) log |Cκ | is superpolynomial in V C(Cκ ), and (3) The number of samples
 required to learn Cκ under differential privacy is Ω(log |Cκ |).

Perspective 2.
Formalized setting and preliminaries. Let (X, Σ) be a measurable space, and let C be a finite class
of Σ-measurable maps from X to {0, 1}. For t ∈ [N ], let τt (q) = 1{q ≤ t}. The class C has a (k, N )
disjoint-threshold minor if there are injections ϕj : [N ] → X with disjoint images and concepts
ct ∈ C, t ∈ [N ]k , such that

                               ct (ϕj (q)) = τtj (q)    (j ∈ [k], q ∈ [N ]).


                                                       34
   VALG                                                                               ML Theory Research Agent




   For a probability law Q on the product measurable space X ×{0, 1}, write LQ (h) = Pr(x,y)∼Q [h(x) ̸=
   y] for measurable h. Learners use exactly an integer m ≥ 1 iid examples and replacement adjacency;
   their output hypotheses and all output-coordinate evaluation maps are measurable. For a probability
   measure P on (X, Σ) and c ∈ C, let QP,c be the law of (x, c(x)) for x ∼ P , and define log∗ t =
                   (r)
   min{r ≥ 0 : log2 t ≤ 1}. Here log is natural.
   Technical assumptions.
   Assumption 4.48 (Disjoint-threshold restriction table). Integers k ≥ 1, N ≥ 2, and C admit
   the minor defined above.
   Assumption 4.49 (Unrestricted private PAC antecedent). The kernel A : (X × {0, 1})m ⇝ {0, 1}X
   is replacement-(ε0 , δm )-DP and, for every c ∈ C and distribution P on X,
                                          Pr          [LQP,c (h) > α0 ] ≤ β0 .
                                    S∼Qm
                                       P,c , h∼A(S)


  The learner may be improper and computationally unbounded.
   Assumption 4.50 (Fixed PAC and approximate-privacy scale).
                           1             1                                            cδ
                   α0 =       ,   β0 =      ,     0 < ε0 ≤ 1,          0 ≤ δm ≤    2
                                                                                            ,
                          128            32                                       m log(em)
   where the theorem fixes the universal constant cδ .

Main theory.
     Theorem 4.11 (Private direct-sum threshold-minor lower bound). There are universal constants
     c, cδ > 0 and N0 ≥ 2 such that, for every k ≥ 1, N ≥ N0 , domain X, finite class C, and
     fixed-sample learner satisfying Assumptions 4.48–4.50,

                                                m ≥ c k log∗ N,

     where log∗ is the base-two iterated logarithm.

   Discussion. This is partial progress. It preserves finite binary classes, distribution-free realizable
   PAC learning, approximate privacy, and a lower bound against unrestricted learners. It differs from
   the source problem in two essential ways:
     (i) the class must contain a (k, N ) disjoint-threshold minor, under a small-δm privacy regime;
    (ii) the conclusion is Ω(k log∗ N ) rather than the requested Ω(log |C|) existential separation.
   Technical role and remaining barrier. The source class-existence question leaves two barriers:
   an arbitrary finite class need not contain independent threshold-hard directions, and combining many
   hard directions can violate record-level privacy through record reuse or group privacy. The disjoint-
   threshold minor exposes independent hard coordinates, and the one-use hidden-arm reduction
   combines them while preserving record-level adjacency. The small-δm regime makes the component
   threshold lower bound applicable. The remaining problem is to construct finite classes with log |Cκ |
   superpolynomial in VC(Cκ ) for which every private learner requires Ω(log |Cκ |) samples without
   relying on the added small-δm regime.

   4.5 Online Optimization of Piecewise-Lipschitz Functions with Applications to
       Data-Driven Algorithm Design
   4.5.1 Subproblem 1: Polynomial Boundaries


                                                         35
VALG                                                                                          ML Theory Research Agent




  Open question. For a monic polynomial

                   ϕα (θ) = θd + αd−1 θd−1 + · · · + α0 ,              α ∈ [−R, R]d ,       θ ∈ Θ,

  for a coefficient distribution class D, the relevant constant for a coefficient-law class D is

                                                      Prα∼µ [∃θ ∈ I : ϕα (θ) = 0]
                              CD = sup         sup                                .
                                     µ∈D I⊆Θ interval            |I|
                                              |I|>0

 The first subproblem of Balcan et al. (2026) asks: under what natural necessary and sufficient
 conditions on D is CD finite, and under what conditions is it bounded by a polynomial in d and
 R?
Perspective 2.
Formalized setting and preliminaries. Let Θ ⊆ R be compact and I(Θ) its positive finite-length
intervals, with arbitrary endpoint conventions. For d ≥ 1, R ≥ 1, and α = (α0 , . . . , αd−1 ) ∈ [−R, R]d ,
set
                                   d−1
                                   X
                                d
                      ϕα (θ) = θ +     αj θj ,   Hd,I = {α : ∃θ ∈ I, ϕα (θ) = 0}.
                                        j=0
For a law µ, define the random regular conditional-density norms
            K0µ = ∥fαµ0 |α1:d−1 ( · | α1:d−1 )∥L∞ (R) ,          µ
                                                                K∞ = ∥fαµd−1 |α0:d−2 ( · | α0:d−2 )∥L∞ (R) ,
evaluated at the random conditioning coordinates (for d = 1, both are the density norm of α0 ).
For fixed finite η = (κ̄0 , κ̄∞ ), let Dd,R,η contain exactly the laws supported on [−R, R]d whose two
regular conditional densities exist almost surely and obey EK0µ ≤ κ̄0 and EK∞       µ
                                                                                      ≤ κ̄∞ . These are
mean caps, rather than almost-sure uniform caps. Thus Dd,R,η permits dependent laws specified
through endpoint regular conditional densities. Define
                                                                     µ(Hd,I )
                                       CDd,R,η =       sup       sup          .
                                                     µ∈Dd,R,η I∈I(Θ)   |I|
All interval lengths are Lebesgue lengths, and the definition assigns value zero whenever either
indexing family is empty. For I0 = I ∩ [−1, 1], I+ = I ∩ (1, ∞), and I− = I ∩ (−∞, −1), set
           Rd(d − 1)                Rd(d − 1)
 B0 = d +             , B∞ = 1 +              , Mη = max{κ̄0 B0 , κ̄∞ B∞ }, κ̄∗ = max{κ̄0 , κ̄∞ }.
                2                      2
Define a witness law by taking α0 uniform on [−R, R] when d = 1, take α0 , α1 independently
uniform when d = 2, and, for d ≥ 3, take independent uniform endpoint coefficients and set every
middle coefficient to RS for one independent Rademacher S. Call the resulting law µwit
                                                                                    d,R .
Technical assumptions.
Assumption 4.51 (Compact parameter domain). Θ ⊆ R is fixed and compact; the result is uniform
in I ∈ I(Θ) and independent of Θ.
Assumption 4.52 (Indexed regime). d ≥ 1, R ≥ 1, and finite η ∈ [0, ∞)2 is fixed independently of
(d, R).
Assumption 4.53 (Compact cube support and monicity). Every quantified law is supported on
[−R, R]d , and ϕα is exactly monic.
Assumption 4.54 (Mean endpoint conditional-density caps). The two conditional densities and
mean bounds defining Dd,R,η hold.

                                                           36
   VALG                                                                                   ML Theory Research Agent




Main theory.
     Theorem 4.12 (Endpoint conditional anti-concentration). Under Assumptions 4.51– 4.54, for
     every µ ∈ Dd,R,η and I ∈ I(Θ),

                             µ(Hd,I ) ≤ κ̄0 B0 |I0 | + κ̄∞ B∞ (|I+ | + |I− |) ≤ Mη |I|.

    Consequently,
                                                                   κ̄∗ 2
                                        CDd,R,η ≤ Mη ≤ κ̄∗ d +        Rd .
                                                                    2
                                                                                                wit       wit
     If κ̄0 , κ̄∞ ≥ 1/2, then for every d, R the witness law belongs to Dd,R,η and K0µ                   µ
                                                                                                      = K∞      =
     1/(2R) almost surely.

   Discussion. This is partial progress. It preserves monic degree-d polynomials, cube-supported
   coefficients, and the source root-hitting constant. It differs from the source problem in three ways:

     (i) the coefficient law must satisfy endpoint conditional-density bounds;

    (ii) the theorem is restricted to R ≥ 1;

    (iii) it gives a sufficient polynomial upper bound, not a necessary-and- sufficient characterization.

   Technical role and remaining barrier. The source coefficient-law problem leaves two analytic
   barriers. General laws provide no controlled one-dimensional sweep near zero or infinity, and a direct
   joint-density argument can incur exponential dependence on the ambient coefficient dimension. The
   endpoint conditional-density bounds control the two endpoint charts separately, while the outer
   pivot removes the large-root growth, yielding the bound Oη (Rd2 ). The restriction R ≥ 1 has a
   separate role: when κ̄0 , κ̄∞ ≥ 1/2, it makes the indexed family uniformly nonempty under the fixed
   caps, since the witness satisfies K0 = K∞ = 1/(2R) ≤ 1/2. The local sweep bounds themselves
   extend to R > 0 whenever the capped family is nonempty. The remaining problem is to obtain a
   natural coefficient-side condition that is necessary and sufficient, up to polynomial factors, for all
   R > 0 and general coefficient-law classes, including the cap scaling needed in the small-R regime.
   4.5.2 Subproblem 2: Pfaffian Boundaries

    Open question. Let F = (F1 , . . . , FN ) be a vector of Pfaffian functions on a compact interval
    Θ, and let
                            ϕα (θ) = ⟨α, F (θ)⟩,         α ∈ [−R, R]N .
    Suppose every law in D has a joint density bounded by κ. The second subproblem of Balcan
    et al. (2026) asks: what normalization of F , analogous to fixing the leading coefficient of a
                                        Pf is finite? Here
    polynomial to one, guarantees that CD

                               Pf                      Prα∼µ [∃θ ∈ I : ϕα (θ) = 0]
                              CD  = sup       sup                                  .
                                      µ∈D I⊆Θ interval            |I|
                                              |I|>0

   Perspective 1.
   Formalized setting and preliminaries. Let Θ = [c − h, c + h], x = (θ − c)/h ∈ [−1, 1], and use the
   one-parameter convention p = 1. Let η = (η1 , . . . , ηq ) be a triangular Pfaffian chain with polynomials
   Pj (x, y1:j ). For output polynomials Qi (x, y1:q ), define

                                 Gi (x) = Qi (x, η(x)),        Fi (θ) = Gi (x(θ)),


                                                          37
   VALG                                                                            ML Theory Research Agent




     M = max deg Pj ,    ∆ = max deg Qi ,   BP = max ∥ coeff(Pj )∥1 ,     BQ = max ∥ coeff(Qi )∥1 , (F1)
            j                  i                      j                            i

   with total degrees and M = BP = 0 if q = 0. Let DN,R,κ be all laws on [−R, R]N with full joint
   density at most κ; their coordinates may be arbitrarily correlated. Set

          D = DN,R,κ ,      A = (2R)N κ,      γF = F/∥F ∥2 ,       Γproj (F ) = ess sup ∥γF′ (θ)∥2 ,
                                                                                  θ∈Θ

            Pf (F ; Θ) be the supremum, first over positive-length intervals I ⊆ Θ and then over
   and let CD
   µ ∈ DN,R,κ , of Prµ [∃θ ∈ I : ⟨α, F (θ)⟩ = 0]/|I|.
      For an affine offset F0 ∈ C 1 (Θ) and a measurable partition I = j Ej with Fj ̸= 0 on Ej , index
                                                                      F

   β ∈ [−R, R]N −1 by i ̸= j and set

                                                   F0 (θ) X Fi (θ)
                                   Tj (θ, β) = −          − βi        .                                (F2)
                                                   Fj (θ)      Fj (θ)
                                                           i̸=j

   For N = 1, the zero-dimensional cube has Lebesgue mass one.
   Technical assumptions.

   Assumption 4.55 (Primitive parameter regime). N ≥ 1, q ≥ 0, h, R > 0, 0 < κ < ∞, the class
   DN,R,κ is nonempty, and all degrees and coefficient budgets in (F1) are finite.

   Assumption 4.56 (Balcan common-chain presentation). Each ηj ∈ C 1 ([−1, 1]) satisfies ηj′ =
   Pj (x, η1:j ), and every Gi = Qi (x, η), with the degree convention (F1).

  Assumption 4.57 (Literal anchor and unit-range certificate). |ηj (x)| ≤ 1 on [−1, 1] and Q1 ≡ 1.
  Thus F1 = G1 = 1, supplying the norm margin used below.

   Assumption 4.58 (Arbitrarily correlated capped joint laws). Every probabilistic clause quantifies
   over arbitrary µ ∈ DN,R,κ , including dependent coordinate laws.

   Assumption 4.59 (Deterministic affine offset and pivot cover). The affine clause uses precisely
   the deterministic F0 and measurable pivot partition described before (F2).

Main theory.
    Theorem 4.13 (Anchored coefficient-normalized Pfaffian sweep). Under Assumptions 4.55–
    4.57, the following five conclusions hold; the probabilistic ones also use Assumption 4.58, and
    the affine one uses Assumption 4.59.
    (R1) Projective speed. With D∗ = ∆BQ (1 + qBP ), pointwise
                                                                    √
                    ′                ′
                                          √                           N ∆BQ (1 + qBP )
                  |Gi | ≤ D∗ ,    ∥G ∥2 ≤ N D∗ ,       Γproj (F ) ≤                    .       (R1)
                                                                             h
    The literal anchor gives ∥F ∥2 , ∥G∥2 ≥ 1, so this conditioning is derived from the normalized
    presentation.
    (R2) Central sweep. For every possibly correlated µ ∈ DN,R,κ and then every positive-length
    I ⊆ Θ,
                                                r
                                                  N                 AN ∆BQ (1 + qBP )
                Pr[∃θ ∈ I : ⟨α, F (θ)⟩ = 0] ≤ A     Γproj (F )|I| ≤      √            |I|,  (R2a)
                 µ                                2                        2h



                                                     38
VALG                                                                                     ML Theory Research Agent




  and the same two coefficients bound
                                         r
                         Pf                  N              AN ∆BQ (1 + qBP )
                        CD  (F ; Θ) ≤ A        Γproj (F ) ≤      √            .                          (R2b)
                                             2                     2h
 (R3) Affine sweep. For every µ ∈ DN,R,κ , interval, and admissible pivot cover,
                                                         N Z
                                                         X          Z
            Pr[∃θ ∈ I : F0 (θ) + ⟨α, F (θ)⟩ = 0] ≤ κ                             |∂θ Tj (θ, β)| dβ dθ.    (R3)
             µ                                                 Ej   [−R,R]N −1
                                                         j=1

 The right side is interpreted in [0, +∞] and may equal +∞.
 (R4) Exact monic recovery. For every integer d ≥ 1 and bounded interval
                                                                      P J ⊂ R, choose Θ ⊇ J
 and set F0 (θ) = θd , Fk+1 (θ) = θk for 0 ≤ k < d. Thus pα (θ) = θd + k<d αk θk , with the monic
 coefficient deterministic and outside the random vector, and

                  Q0 (x) = (c + hx)d ,        Qk+1 (x) = (c + hx)k , ∆aug = d,
                       q = M = BP = 0,              N = d,                       A = (2R)d κ.

 Using E1 = J ∩ {|θ| ≤ 1} and Ed = J ∩ {|θ| > 1} (or E1 = J for d = 1) in (R3) gives, for every
 possibly correlated µ ∈ Dd,R,κ ,
                                                                     
                                                            Rd(d − 1)
                     Pr[∃θ ∈ J : pα (θ) = 0] ≤ κ(2R)d−1 d +             |J|.               (R4)
                      µ                                         2

 (R5) Counterexample scale. For 0 < δ ≤ 1, take F (θ) = (1, θ/δ) on [−1, 1] and the uniform law
 on [−1, 1]2 , so κ = 1/4 and A = 1. Then BQ = Γproj (F ) = 1/δ and, for every 0 < ϵ ≤ δ,
                                                                                  √
                                          ϵ     1       Pf                    1     2
      Pr[∃θ ∈ [0, ϵ] : α1 + α2 θ/δ = 0] = ,        ≤ CD2,1,1/4 (F ; [−1, 1]) ≤ ≤      .    (R5)
                                         4δ     4δ                            δ    δ
 When BP is fixed, the dependence on M is degree zero.

Discussion. This is full progress for the declared anchored unit-range normalization: the literal
anchor and bounded-chain presentation yield finite, explicit projective and central sweep bounds, a
general affine chart inequality, exact monic recovery, and the counterexample’s unavoidable 1/δ scale.
Whether every raw Pfaffian presentation admits this normalization with polynomial parameter
budgets remains open.

5 Conclusion and Discussions
VALG organizes informal ML-theory research around source-relative theorem branches whose
assumptions, proof dependencies, and outcomes remain tied to the originating question. Its global-
to-local proof process supports both local repair and formulation-level revision, allowing a failed
proof mechanism to produce a clearly scoped variant or relaxation. Across nine COLT 2026 case
studies, two runs produce internally finalized theorem candidates that match the scope of the
original subproblems, while the remaining runs yield restricted-method results, special cases, or
conditional theorems.
    An important next step is to make AI-generated mathematics more readable and verifiable for
researchers. Current systems tend to overuse notation and present proofs in ways that obscure the
main argument, often deviating from established human proof-writing conventions. Even when


                                                    39
VALG                                                                            ML Theory Research Agent




derivations are plausible, these stylistic issues significantly increase the cost of expert verification.
Rigorous evaluation also requires machine learning theory benchmarks that go beyond case studies
of open problems. Our findings on COLT open problems indicate that difficult questions often
benefit from multiple perspectives and evolving generation of ideas. However, to meaningfully
assess the contribution and redundancy of these components, we need controlled benchmarks with
known solutions, alternative valid formulations, explicit assumptions and relaxations, and clearly
documented proof dependencies. Finally, formalization also remains a critical challenge. ML theory
draws on probability, optimization, statistics, information theory, and learning theory, i.e., domains
for which existing general-purpose formalization pipelines are often incomplete or cumbersome.
Developing automated formalization tools tailored to the specific statements and proof patterns
of ML theory would enable natural-language agents to explore formulations and proof strategies,
while formal tools verify the mathematical core of their results. All of these further explorations
and developments require the participation and effort of the entire ML theory community.

References
An, C., Ye, Q., Pan, M. and Zhang, J. (2026). Qed: An open-source multi-agent system for
 generating mathematical proofs on open problems. arXiv preprint arXiv:2604.24021 . 4, 8, 10

Angluin, D. (1987). Learning regular sets from queries and counterexamples. Information and
 Computation 75 87–106. 2

Arvanitakis, D., Srinivas, V. and Vijayaraghavan, A. (2026). Open problem: How much
 overparametrization is needed for ALS in tensor decomposition? In Proceedings of the Thirty-
 Ninth Conference on Learning Theory, vol. 336 of Proceedings of Machine Learning Research.
 PMLR. 2, 12

Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E. W., Radev, D. and Avigad, J.
 (2023). Proofnet: Autoformalizing and formally proving undergraduate-level mathematics. arXiv
 preprint arXiv:2302.12433 . 5

Balcan, M.-F., Pegden, W. and Sharma, D. (2026). Invited open problem: Online optimization
 of piecewise-Lipschitz functions with applications to data-driven algorithm design. In Proceedings
 of the Thirty-Ninth Conference on Learning Theory, vol. 336 of Proceedings of Machine Learning
 Research. PMLR. 3, 12, 36, 37

Ben-David, S., Eiron, N. and Simon, H. U. (2002). Limitations of learning via embeddings in
 euclidean half spaces. Journal of Machine Learning Research 3 441–461. 26

Cabral, R., Manh, T., Yu, X., Tai, W. M., Feng, Z. and Xin, S. (2026). Proofflow: A
 dependency graph approach to faithful proof autoformalization. In International Conference on
 Learning Representations, vol. 2026. 5

Cao, Y., Qiu, R., Liu, J., Wang, J., Guo, D., Feng, R., Zhi, L. and Gao, X.-S. (2026). Mech-
 math agent team: Llm driven agents for mathematical research. arXiv preprint arXiv:2607.04394
 . 4

Chan, J. S., Chowdhury, N., Jaffe, O., Aung, J., Sherburn, D., Mays, E., Starace, G.,
 Liu, K., Maksin, L., Patwardhan, T. et al. (2025). Mle-bench: Evaluating machine learning
 agents on machine learning engineering. In International Conference on Learning Representations,
 vol. 2025. 2, 5



                                                   40
VALG                                                                        ML Theory Research Agent




Chen, L., Liu, Z., He, W. and Dong, B. (2026). Iteris: Agentic research loops for computational
 mathematics. arXiv preprint arXiv:2606.02484 . 3, 4

Chen, X. and Jiang, X. (2026). Moonshine: An autonomous mathematical research agent centered
 on conjecture generation. arXiv preprint arXiv:2606.10806 . 3

Chen, Z., Chen, S., Ning, Y., Zhang, Q., Wang, B., Yu, B., Li, Y., Liao, Z., Wei, C., Lu,
 Z., Dey, V., Xue, M., Baker, F. N., Burns, B., Adu-Ampratwum, D., Huang, X., Ning,
 X., Gao, S., Su, Y. and Sun, H. (2025). ScienceAgentBench: Toward rigorous assessment of
 language agents for data-driven scientific discovery. In International Conference on Learning
 Representations. 5

Davies, A., Veličković, P., Buesing, L., Blackwell, S., Zheng, D., Tomašev, N., Tanburn,
 R., Battaglia, P., Blundell, C., Juhász, A. et al. (2021). Advancing mathematics by
 guiding human intuition with AI. Nature 600 70–74. 3

Dwork, C., McSherry, F., Nissim, K. and Smith, A. (2016). Calibrating noise to sensitivity in
 private data analysis. Journal of Privacy and Confidentiality 7 17–51. 32

Feldman, V., Kamath, P. and Srebro, N. (2026). Invited open problem: Is the power of deep
  learning over linear models inherently distribution dependent? In Proceedings of the Thirty-Ninth
 Conference on Learning Theory, vol. 336 of Proceedings of Machine Learning Research. PMLR. 3,
 12, 26

Feng, T., Trinh, T. H., Bingham, G., Hwang, D., Chervonyi, Y., Jung, J., Lee, J.,
 Pagano, C., Kim, S.-h., Pasqualotto, F. et al. (2026). Towards autonomous mathematics
 research. arXiv preprint arXiv:2602.10177 . 2, 4, 5, 8

Gold, E. M. (1967). Language identification in the limit. Information and Control 10 447–474. 2

Gottweis, J., Weng, W.-H., Daryin, A. et al. (2026). Accelerating scientific discovery with
 Co-Scientist. Nature . 2, 4

He, Y., Li, D., Li, G., Geng, J., Huang, Z., Ren, C., Zhang, Z., Liu, Y., Zhu, S., Zhang, H.
 et al. (2026). Reasflow: Assisting reasoning-centric scientific discovery in applied mathematics
 via a knowledge-based multi-agent system. arXiv preprint arXiv:2607.14178 . 2, 4

Huang, Q., Vora, J., Liang, P. and Leskovec, J. (2023). Mlagentbench: Evaluating language
 agents on machine learning experimentation. arXiv preprint arXiv:2310.03302 . 2, 5

Jiang, A. Q., Li, W. and Jamnik, M. (2023). Multilingual mathematical autoformalization. arXiv
  preprint arXiv:2311.03755 . 5

Ju, H., Gao, G., Jiang, J., Wu, B., Sun, Z., Liu, S., Chen, L., Wang, Y., Wang, Y., Wang,
  Z. et al. (2026). Automated conjecture resolution with formal verification. arXiv preprint
  arXiv:2604.03789 . 4, 8

Kripner, M. and Straka, M. (2026). Openprover: Agentic and interactive theorem proving with
 lean 4. arXiv preprint arXiv:2607.09217 . 2, 4

Lample, G., Lacroix, T., Lachaux, M.-A., Rodriguez, A., Hayat, A., Lavril, T., Ebner,
  G. and Martinet, X. (2022). Hypertree proof search for neural theorem proving. Advances in
 neural information processing systems 35 26337–26349. 4


                                                41
VALG                                                                        ML Theory Research Agent




Lau, I. and Scarlett, J. (2026a). Open problem: Is interaction necessary for order-optimal 1-bit
  mean estimation? In Proceedings of the Thirty-Ninth Conference on Learning Theory, vol. 336 of
 Proceedings of Machine Learning Research. PMLR. 3, 12, 22

Lau, I. and Scarlett, J. (2026b). Order-optimal sequential 1-bit mean estimation in general tail
  regimes. arXiv preprint arXiv:2604.07796 . 23, 24

Lin, H., Sun, Z., Welleck, S. and Yang, Y. (2025). Lean-star: Learning to interleave thinking
  and proving. In International Conference on Learning Representations, vol. 2025. 4

Littlestone, N. (1988). Learning quickly when irrelevant attributes abound: A new linear-
  threshold algorithm. Machine learning 2 285–318. 2, 32

Liu, C., Yin, Y., Yuan, Y., Xie, J., Li, B., Li, S., Shen, J., Xu, Y., Shang, L. and Zhang,
  M. (2026a). Discover and prove: An open-source agentic framework for hard mode automated
  theorem proving in lean 4. In Proceedings of the 64th Annual Meeting of the Association for
  Computational Linguistics (Volume 1: Long Papers). 4

Liu, J., Gao, G., Sun, Z., Wu, B., Liu, S., Jiang, J., Ju, H., Chen, L., Cheng, R., Zhang,
  X. et al. (2026b). Danus: Orchestrating mathematical reasoning agents with fact-graph memory.
  arXiv preprint arXiv:2607.06447 . 2, 4

Liu, J., Zhou, Z., Zhu, Z., Santos, M. D., He, W., Liu, J., Wang, R., Xie, Y., Zhao, J.,
  Wang, Q. et al. (2026c). Numina-lean-agent: An open and general agentic reasoning system
  for formal mathematics. arXiv preprint arXiv:2601.14027 . 4

Liu, T.-S., Zhang, S., Geng, Z., Liu, H., Xu, R., Wang, P., Yuan, L. and Yu, Y.
  (2026d). Efficient test-time optimization for multi-agent proof autoformalization. arXiv preprint
  arXiv:2607.11307 . 5

Lu, C., Lu, C., Lange, R. T., Foerster, J., Clune, J. and Ha, D. (2024). The ai scientist:
 Towards fully automated open-ended scientific discovery. arXiv preprint arXiv:2408.06292 . 2, 3

Ma, D., Ma, K., Guo, S., Shi, Y., Zhao, E., Shi, J., Zhang, Z., Cheung, G., Liu, J. and
 Wang, Z. (2026). Oprover: A unified framework for agentic formal theorem proving. arXiv
 preprint arXiv:2605.17283 . 4

Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U.,
 Dziri, N., Prabhumoye, S., Yang, Y., Welleck, S., Majumder, B. P., Gupta, S.,
 Yazdanbakhsh, A. and Clark, P. (2023). Self-refine: Iterative refinement with self-feedback.
 In Advances in Neural Information Processing Systems, vol. 36. 2

Min, M. J., He, M., Li, Z., Yi, Z., Malik, S., Gupta, A., Si, X. and Bastani, O. (2026).
 Theory-level autoformalization: From isolated statements to unified formal knowledge bases.
 arXiv preprint arXiv:2607.13292 . 5

Moakhar, A. S., Gholami, I., Springer, M., JafariRaviz, M. and Hajiaghayi, M. (2026).
 Beyond the library: An agentic framework for autoformalizing research mathematics. arXiv
 preprint arXiv:2606.31134 . 5

Nissim, K., Stemmer, U. and Tsfadia, E. (2026). Invited open problem: Does differential privacy
  make PAC learning much harder? In Proceedings of the Thirty-Ninth Conference on Learning
 Theory, vol. 336 of Proceedings of Machine Learning Research. PMLR. 3, 12, 32


                                                42
VALG                                                                       ML Theory Research Agent




Novikov, A., Vũ, N., Eisenberger, M., Dupont, E., Huang, P.-S., Wagner, A. Z.,
 Shirobokov, S., Kozlovskii, B., Ruiz, F. J., Mehrabian, A. et al. (2025). Alphaevolve: A
 coding agent for scientific and algorithmic discovery. arXiv preprint arXiv:2506.13131 . 3

Ren, Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W., Zhang, L., Fu, Z., Zhu, Q.,
 Yang, D. et al. (2025). Deepseek-prover-v2: Advancing formal mathematical reasoning via
 reinforcement learning for subgoal decomposition. arXiv preprint arXiv:2504.21801 . 4

Romera-Paredes, B., Barekatain, M., Novikov, A., Balog, M., Kumar, M. P., Dupont,
 E., Ruiz, F. J. R., Ellenberg, J. S., Wang, P., Fawzi, O. et al. (2024). Mathematical
 discoveries from program search with large language models. Nature 625 468–475. 3

Schmidgall, S., Su, Y., Wang, Z., Sun, X., Wu, J., Yu, X., Liu, J., Moor, M., Liu, Z. and
  Barsoum, E. (2025). Agent laboratory: Using llm agents as research assistants. Findings of the
  Association for Computational Linguistics: EMNLP 2025 5977–6043. 2, 4

Schmitt, J., Gehrunger, T., Dekoninck, J., Bérczi, G., Kreitner, U., Price, L. and
  Holmes, D. (2026). Proofcouncil: An llm agent for solving open mathematical problems. arXiv
  preprint arXiv:2607.09474 . 4

Shalev-Shwartz, S. and Ben-David, S. (2014). Understanding Machine Learning: From Theory
  to Algorithms. Cambridge University Press. 2

Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K. and Yao, S. (2023). Reflexion:
  Language agents with verbal reinforcement learning. In Advances in Neural Information Processing
  Systems, vol. 36. 2

Siegel, Z. S., Kapoor, S., Nadgir, N., Stroebl, B. and Narayanan, A. (2024). Core-bench:
  Fostering the credibility of published research through a computational reproducibility agent
  benchmark. arXiv preprint arXiv:2409.11363 . 5

Son, G., Yi, S., Gwak, M., Ko, H., Jang, W. and Yu, Y. (2026). Researchmath-14k: Scaling
  research-level mathematics via agents. arXiv preprint arXiv:2605.28003 . 5

Srinivasan R, S. and Patawar, M. (2026). Lamp: Lean-based agentic framework with mcp and
  proof repair. arXiv e-prints arXiv–2606. 4

Starace, G., Jaffe, O., Sherburn, D., Aung, J., Chan, J. S., Maksin, L., Dias, R., Mays,
  E., Kinsella, B., Thompson, W. et al. (2025). Paperbench: evaluating ai’s ability to replicate
  ai research. arXiv preprint arXiv:2504.01848 . 2, 5

Thakur, A., Tsoukalas, G., Wen, Y., Xin, J. and Chaudhuri, S. (2024). An in-context
 learning agent for formal theorem-proving. In Proceedings of the 7th Conference on Artificial
 Intelligence and Theorem Proving. 4

Trinh, T. H., Wu, Y., Le, Q. V., He, H. and Luong, T. (2024). Solving olympiad geometry
 without human demonstrations. Nature 625 476–482. 3

Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M., Jennings, M., Thakur, A. and
 Chaudhuri, S. (2024). PutnamBench: Evaluating neural theorem-provers on the putnam
 mathematical competition. In Advances in Neural Information Processing Systems. 5

Valiant, L. G. (1984). A theory of the learnable. Communications of the ACM 27 1134–1142. 1,
 2

                                               43
VALG                                                                        ML Theory Research Agent




Vapnik, V. N. (1998). Statistical Learning Theory. Wiley. 1
Wainwright, M. J. (2019). High-Dimensional Statistics: A Non-Asymptotic Viewpoint. Cambridge
 University Press. 2
Wang, H., Huang, B., Wan, Y., Zhu, X., Liu, X., Huang, Y. and Guo, Z. (2026). Formalrx:
 Rectify and examine semantic failures in autoformalization. arXiv preprint arXiv:2607.04655 . 5
Wang, H., Xin, H., Zheng, C., Liu, Z., Cao, Q., Huang, Y., Xiong, J., Shi, H., Xie, E., Yin,
 J. et al. (2024). Lego-prover: Neural theorem proving with growing libraries. In International
 Conference on Learning Representations, vol. 2024. 4
Weng, K., Du, L., Li, S., Lu, W., Sun, H., Liu, H. and Zhang, T. (2025). Autoformalization
 in the era of large language models: A survey. arXiv preprint arXiv:2505.23486 . 5
Wijk, H., Lin, T., Becker, J., Jawhar, S., Parikh, N., Broadley, T., Chan, L., Chen, M.,
 Clymer, J., Dhyani, J. et al. (2024). Re-bench: Evaluating frontier ai r&d capabilities of
 language model agents against human experts. arXiv preprint arXiv:2411.15114 . 2, 5
Wu, Y., Jiang, A. Q., Li, W., Rabe, M., Staats, C., Jamnik, M. and Szegedy, C. (2022).
 Autoformalization with large language models. Advances in neural information processing systems
 35 32353–32368. 5
Xia, H., Gomes, C. P., Selman, B. and Szeider, S. (2026). Agentic neurosymbolic collaboration
  for mathematical discovery: A case study in combinatorial design. arXiv preprint arXiv:2603.08322
  . 3
Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B., Ruan, C., Li, W. and Liang, X.
 (2024). Deepseek-prover: Advancing theorem proving in llms through large-scale synthetic data.
 arXiv preprint arXiv:2405.14333 . 4
Yan, C. (2025). An Optimal
                    e       differentially private learner for concept classes with vc dimension 1.
 arXiv preprint arXiv:2505.06581 . 34
Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song, P., Yu, S., Godil, S., Prenger, R.
 and Anandkumar, A. (2023). LeanDojo: Theorem proving with retrieval-augmented language
 models. In Advances in Neural Information Processing Systems, vol. 36. 2, 4
Yang, R., Li, Y. and Li, S. (2026). Aris: Autonomous research via adversarial multi-agent
 collaboration. arXiv preprint arXiv:2605.03042 . 4
Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. and Cao, Y. (2023). ReAct:
 Synergizing reasoning and acting in language models. In International Conference on Learning
 Representations. 2
Zhang, Y., Lee, J. D. and Liu, F. (2026a). Ai4slt: Empirical processes in lean 4 for formal
  statistical learning theory. arXiv preprint arXiv:2602.02285 . 2, 5
Zhang, Y., Sun, J., Bi, H., Geng, C., Ma, W., Li, Z. and Si, X. (2026b). Dreamprover:
  Evolving transferable lemma libraries via a wake-sleep theorem-proving agent. arXiv preprint
 arXiv:2604.26311 . 4
Zhang, Y., Sun, Y., Suzuki, T., Lee, J. D. and Liu, F. (2026c). Leanmarathon: Toward reliable ai
  co-mathematicians through long-horizon lean autoformalization. arXiv preprint arXiv:2606.05400
  . 2, 5

                                                44
VALG                                                                  ML Theory Research Agent




Zhao, Z., Yuan, B., Choi, J. and Chen, Y. (2026). Rma: an agentic system for research-level
  mathematical problems. arXiv preprint arXiv:2605.22875 . 4, 5

Zheng, D., von Glehn, I., Zwols, Y., Beloshapka, I., Buesing, L., Roy, D. M., Wat-
 tenberg, M., Georgiev, B., Schmidt, T., Cowie, A. et al. (2026). Ai co-mathematician:
 Accelerating mathematicians with agentic ai. arXiv preprint arXiv:2605.06651 . 2, 4

Zheng, K., Han, J. M. and Polu, S. (2021). Minif2f: a cross-system benchmark for formal
  olympiad-level mathematics. arXiv preprint arXiv:2109.00110 . 5




                                            45
