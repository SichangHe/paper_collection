                                             MathCoPilot: An Interactive System for Human–AI
                                              Symbiotic Paradigm of Mathematical Research

                                             Junjie Zhang1* Jiayu Liu1* Wenbin Liu1* Zhenya Huang1† Doudou Wang1,2 Yan Jiang1,2
                                             Leiye Xu1,2 Tao Xiong1,2 Wen Huang1,2 Qi Liu1 Guoping Hu1 Enhong Chen1 Mengping
                                                                          Zhang1,2† Xiangdong Ye1,2
                                             1
                                                 State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China
                                                       2
                                                         School of Mathematical Sciences, University of Science and Technology of China
                                                                           *                        †
                                                                               Equal contribution       Corresponding authors
                                                                               Webpage: https://mathcopilot.cn



                                                                                            Abstract
arXiv:2607.14582v1 [cs.AI] 16 Jul 2026




                                                     Existing LLM-based theorem provers have achieved impressive results on formal
                                                     mathematics benchmarks, yet they remain confined to acting as autonomous agents
                                                     that prove a stated proposition. In this paper, we propose M ATH C O P ILOT, a
                                                     human-in-the-loop system that embodies a new human–AI symbiotic paradigm for
                                                     mathematical research, in which the mathematician steers the high-level mathemat-
                                                     ical direction while AI agents carry out the detailed formalization and proof work
                                                     under continuous human guidance. M ATH C O P ILOT unifies three core capabilities:
                                                     (1) an interactive workbench where the mathematician and AI agents collaborate
                                                     through a living proof blueprint that decomposes a proof into navigable steps the
                                                     human can directly inspect, direct, and refine; (2) automated proving skill orchestra-
                                                     tion with adaptive knowledge base search and Lean-integrated iterative verification;
                                                     and (3) topic-driven paper retrieval and automated formalization into a verified
                                                     Lean knowledge base. Using M ATH C O P ILOT, we systematically compare four
                                                     state-of-the-art LLMs, including Gemini 3.1 Pro, GPT-5.4, and Claude Opus 4.7,
                                                     on a FormalMATH subset and on two real PDE theorems requiring deep domain
                                                     expertise, evaluating their ability to produce verified Lean 4 proofs and to identify
                                                     errors in deliberately incorrect proofs. Our results show that while current models
                                                     can handle undergraduate-level problems with high success rates under favorable
                                                     autoformalization conditions, substantial challenges remain for domain-specific
                                                     theorems requiring genuine mathematical understanding.


                                         1       Introduction
                                         Mathematical research is undergoing a paradigm shift [Davies et al., 2021, Tao, 2025, Sothanaphan,
                                         2026]. For most of its history, the machine has been at most a tool, a calculator, a search engine,
                                         or a proof checker, while the mathematician alone poses the questions, devises the arguments, and
                                         judges their correctness. The rise of capable AI agents is now challenging this division of labor and
                                         pointing toward a new paradigm in which AI and mathematician work as collaborators, the human
                                         steering the high-level direction and creation while the machine carries out ever larger parts of the
                                         reasoning. The dream of such assistance dates back to the origins of automated theorem proving
                                         [Irving et al., 2016], and the emergence of large language models (LLMs) has accelerated it, with
                                         systems such as AlphaProof [Hubert et al., 2025], DeepSeek-Prover [Xin et al., 2024], and various
                                         Lean-based agents [Jiang et al., 2023, Polu et al., 2023, Liu et al., 2026, Ju et al., 2026] achieving
                                         impressive results. However, these systems are inherently task-centered, concentrating on how an
                                         agent (or multi agents) can best carry out one concrete step such as proving a given theorem, while
                                         overlooking the mathematician’s role in research and failing to support their broader workflow.

                                         Preprint.
The workflow of a working mathematician is far more complex than “prove a given theorem.” It
involves several interconnected activities: Reading and digesting existing work. Mathematicians
spend a substantial fraction of their time understanding papers, proofs, and constructions produced
by others. Long-term knowledge accumulation. Each researcher maintains a personal repository of
lemmas, notation conventions, and proof techniques built over years of study. Interactive human-
machine collaboration. Researchers need to ask questions, discuss approaches, request explanations,
and have their informal sketches formalized by an assistant that adapts to their style. Diverse proof
strategies. Mathematicians think in heterogeneous ways: some begin with natural language sketches,
while others prefer to formalize first and then reason, so a useful assistant must support multiple
strategies rather than committing to a single approach.
Current LLM-based formal mathematics systems primarily operate under a question-and-answer
(Q&A) paradigm [Liu et al., 2026, Baba et al., 2025, Lin et al., 2025, Kim and Yun, 2025]. While they
are capable of generating complete proof processes, this black-box approach falls short of genuinely
assisting mathematicians in active research. First, because these systems directly output complete,
end-to-end proofs in a single pass, the generated content is often overwhelming. Mathematicians are
forced to parse a massive volume of unsegmented steps, making it difficult to read through the proof,
comprehend the underlying logic, or verify its correctness. Second, these systems lack interactivity
across levels of granularity. Whether a mathematician wants to propose a high-level proof sketch
or intervene at a specific logical step, the Q&A format prevents them from injecting insights or
steering the model’s direction mid-generation. Due to these rigidities, practical research tasks remain
fundamentally unsupported. A mathematician who wants to formalize a proof from a newly published
paper, explore whether a lemma from an earlier result applies, or discuss a proof strategy with an AI
collaborator currently has no unified tool to turn to. Moreover, the rapid proliferation of LLM-based
provers has made it difficult to understand the relative strengths of different models and strategies.
Existing evaluations typically report a single pass-rate number per system, obscuring important
questions: how does performance vary across proving strategies? How sensitive are results to the
choice of autoformalization pipeline? Can current models detect subtle logical errors in proofs?
To address these gaps, we present M ATH C O P ILOT, a human-in-the-loop system that embodies a
new human–AI symbiotic paradigm for mathematical research. Rather than treating proving as an
autonomous task, M ATH C O P ILOT casts it as a collaboration in which the mathematician steers the
high-level mathematical direction while AI agents carry out the detailed implementation. Given a
research topic, the system supports paper retrieval and automatically transforms the retrieved content
into verified Lean code stored in a local knowledge base. When proving theorems, it orchestrates
multiple proving skills, dynamically switching between them based on intermediate progress, and
automatically verifies each candidate proof in Lean. Crucially, instead of having AI agents converse
among themselves, M ATH C O P ILOT keeps the mathematician in control through a living proof
blueprint, a flowchart of proof steps in which the human provides direction by pointing at any
step, while the AI handles the detailed work of brainstorming strategies, decomposing the proof,
discharging steps, and formalizing them in Lean.
To understand how different design choices affect proving performance, we conduct a systematic
evaluation of the key components within M ATH C O P ILOT across different proving skills and aut-
oformalization routes. We carry out two complementary studies. The first is an evaluation on a
FormalMATH subset comparing the NL-first and formalization-first skills, in which we evaluate
Gemini 3.1 Pro, GPT-5.4, and Claude Opus 4.7. The second is a focused study on two real PDE
theorems, the L2 error estimate for the semi-discrete upwind DG method and the Gauss–Radau
projection reference-cell estimate, evaluated across three autoformalization routes, in which we test
Gemini 3.1 Pro, GPT-5.4, Claude Opus 4.7, and Claude Sonnet 4 on their ability to produce fully
verified Lean 4 proofs and to identify errors in deliberately incorrect proofs.
Our experiments reveal that current models can solve undergraduate-level problems at moderate
success rates, and that writing a natural-language proof before formalization roughly doubles the strict
pass rate. On the real PDE tasks, performance is highly sensitive to how the statement is formalized:
given a well-formed Lean formalization, Claude Opus 4.7 produces verified Lean 4 certificates on
every attempt and GPT-5.4 follows closely, whereas the same models fail on version-incompatible
formalizations. Performance also varies sharply across proving skills and error-detection capabilities.
These findings suggest that while LLMs have made substantial progress on formal mathematics,
bridging the gap to research-level mathematical reasoning remains an open challenge.



                                                   2
2     Related Work

2.1   LLM-Based Theorem Proving

The integration of AI-driven methods into formal proof has fostered a rich and rapidly evolving line
of work. Early approaches primarily used language models for premise selection [Irving et al., 2016,
Wang et al., 2017], while subsequent work explored direct proof generation via sequence-to-sequence
models [Polu et al., 2023]. More recently, large language models (LLMs) have demonstrated
unprecedented capabilities in mathematical reasoning. However, because verifying pure natural
language proofs is inherently difficult, the mainstream paradigm has shifted toward integrating LLMs
with formal languages, such as Lean [de Moura and Ullrich, 2021] and Isabelle [Eberl et al., 2024].
Despite this shift, directly generating formal code remains a severe bottleneck for current LLMs due
to the scarcity of formal training data. Consequently, recent advancements in this domain broadly
bifurcate into two distinct categories.
The first category leverages natural language (informal mathematics) as an intermediate bridge.
These approaches first generate a natural language proof and subsequently translate it into a formal
language for verification. For instance, Draft-Sketch-Prove [Jiang et al., 2023] demonstrated that
drafting an informal mathematical sketch to outline the high-level logical structure before attempting
formalization significantly improves the model’s success rate. Hilbert [Varambally et al., 2025]
further introduced a recursive refinement strategy that first attempts a direct formal proof and,
upon verification failure, reverts to natural language to decompose the complex target into smaller,
manageable sub-goals before recursively repeating this formalization-decomposition cycle.
The second category confronts the generation challenge head-on by utilizing finetuning [Wang et al.,
2024, Wu et al., 2022, Hubert et al., 2025], data synthesis [Lin et al., 2025], and advanced inference
strategy [Thakur et al., 2023, Xin et al., 2025, Chen et al., 2025] to directly enhance the model’s
capacity to produce formal tactics. For example, DeepSeek-Prover-V2 [Xin et al., 2025] utilizes
Monte Carlo Tree Search (MCTS) guided by Lean’s state feedback to explore complex proof trees.
AlphaProof [Hubert et al., 2025] combined Gemini-based models with RL to solve competition-level
geometry and algebra problems. Goedel-Prover-V2 [Lin et al., 2025] further trains a prover capable
of generation, correction, and expansion, rather than relying on pure single-pass generation.

2.2   AI-Assisted Mathematical Research Systems

Multi-agent reasoning systems [Du et al., 2023, Wu et al., 2023, Zhang and Xiong, 2025] have
demonstrated that collaborative debate among agents can improve reasoning quality, and interactive
frameworks like ReAct [Yao et al., 2023] enable iterative reasoning with tool use. Existing mathe-
matical tool bases such as Mathlib [Ulirsch et al., 2022] provide extensive community-maintained
libraries, which are supported by rigorous verification environments like Lean. Building upon
these environments, interactive proof systems such as LeanDojo [Yang et al., 2023] provides an
open-source playground that enables fine-grained premise extraction, hard negative mining, and
retrieval-augmented theorem proving, while Lean Copilot [Song et al., 2025] assists humans by
integrating LLM inference into Lean to suggest proof steps, complete sub-goals, and select premises.
Two systems are particularly relevant to our work. Numina-Lean-Agent [Liu et al., 2026] leverages
the capabilities of Claude Code to autonomously orchestrate natural language proving and Lean
verification. Rethlas & Archon [Ju et al., 2026] is a dual-agent system: Rethlas handles literature
retrieval, proof planning, and heuristic refinement via natural language, while Archon compiles these
informal plans into Lean and fills in the formal gaps. This framework successfully resolved an open
Anderson conjecture in commutative algebra.
These systems share a common focus: given a statement, they aim to autonomously generate a
complete formal proof. While the vision of fully automated, end-to-end theorem proving is ambitious
and has driven significant progress, we argue that the ideal human-AI interaction paradigm should
not seek to entirely replace human researchers. Instead, human experts are best suited for high-level
directional design, leaving the tedious, low-level formalization tasks to AI. Consequently, our system,
M ATH C O P ILOT, heavily emphasizes active mathematician involvement. Within our system, humans
supervise and continuously refine the overarching proof sketches, while delegating the fine-grained,
step-level detail completion to AI. This division of labor ensures that the overall proving workflow
remains highly controllable, mathematically intuitive, and ultimately more efficient.


                                                  3
       Data Sources
                                        Knowledge Base Construction and Maintenance
              arXiv
                                                                                                                           Verified
      𝑓(𝑥) mathscidoc               Retrieve         Extract               Autoformalize
                                                                                                                        Knowledge Base
                                                                                           Lean4+Mathlib
             Mathlib                                                                          Verifier


            Interactive Human–AI Proof Co-Construction                                        Proving Skill Orchestration
                                        Blueprint


                                                                                                           Knowledge
                                                                                                           Grounded

                                                     Ask
        Brainstorm                                                       Prover
                                                     Guide
                          Collaborate                Approve                                                  Skill
                                                                                                           Orchestrator
                                    Mathematician
                      recursion                                no
                                                                         success?
            Aggregation                 Formalizer             yes
                                                                                              Formalize
                                                                                                              Iterate       NL-First
                                                                                                First


Figure 1: Architecture of M ATH C O P ILOT. The mathematician interacts with three core capabilities,
all connected to the Lean 4 verifier and a personal verified knowledge base.



3     M ATH C O P ILOT

M ATH C O P ILOT is designed around a simple principle: the system should serve the mathematician,
not the benchmark. This means supporting the full breadth of research activities within a single
platform, with the mathematician retaining control over the process at every stage. We organize
the system around three core capabilities: an interactive human–AI workbench that turns proof
construction into a human-in-the-loop process centered on an editable proof blueprint; automated
proving skill orchestration; and automated knowledge base construction and maintenance. Figure 1
illustrates the overall architecture.


3.1   Interactive Human–AI Proof Co-Construction

The core capability of M ATH C O P ILOT is an interactive workbench where a mathematician and AI
agents co-construct a proof. Rather than delivering a single end-to-end proof, the system organizes
the work as a human-in-the-loop pipeline of specialized agents centered on a shared, editable proof
blueprint. This keeps the mathematician in control of the high-level direction while the detailed
sub-tasks are delegated to the agents. The workflow begins when the mathematician states a target
proposition and proceeds through five agents.
Brainstorm Agent. Given the target, the Brainstorm Agent proposes several candidate proof strate-
gies, each a high-level natural-language sketch of a possible route to the result. The mathematician
can edit these suggestions directly, merge or discard them, and ultimately selects one strategy to
develop. This keeps the choice of overall approach, the step that most depends on mathematical taste,
in human hands.
Blueprint Agent. From the selected strategy, the Blueprint Agent generates a proof blueprint by
decomposing the sketch into a graph of nodes, where each node is a self-contained sub-step, such as a
lemma, a case, or an intermediate claim, and the edges encode logical dependencies. The blueprint is
rendered as a flowchart annotated with each node’s natural-language intent and current status (open,
in progress, or verified), so that the mathematician can see at a glance which parts of the argument
are settled and which remain open. Crucially, interaction is node-local and pointing-based: instead
of locating a step through back-and-forth dialogue, the mathematician clicks directly into a node to
inspect, edit, or act on that specific step. This makes large proofs navigable and gives the human and
the agents a concrete shared workspace.


                                                                     4
Prover Agent. The Prover Agent is the discussion-time interface to the automated skill orchestration
that will be introduced in Section 3.2. For any node, the mathematician can designate the claim and
ask the Prover Agent to discharge it fully automatically. When a step is too hard to close directly,
the mathematician can instead recurse: the entire workflow is re-applied to that single node, asking
the Brainstorm Agent for sub-strategies, generating a sub-blueprint, and proving the resulting finer
sub-steps. This recursion can be repeated to arbitrary depth, letting a difficult proof be broken down
until each leaf is automatically provable.
Formalizer Agent. The Formalizer Agent maintains the correspondence between the informal
blueprint and Lean 4. When the blueprint is first created, it emits a Lean sketch that mirrors the node
structure, namely a skeleton of have statements whose unproven steps are filled with sorry. As
each node is completed, it automatically translates that node’s natural-language argument into Lean
and validates it against the Lean 4 verifier, so that formal progress accumulates in lockstep with the
informal proof.
Aggregation Agent. Once the blueprint is fully discharged, the Aggregation Agent collects the
per-node results and synthesizes them into a single coherent natural-language proof of the original
target, suitable for inclusion in a paper. It linearizes the dependency graph, stitches the node-level
arguments into connected prose, and pairs the exposition with the assembled Lean proof.
Throughout this pipeline, the system provides on-demand explanation: given any node or Lean
fragment, it generates natural-language explanations at multiple granularities, from high-level strategy
overviews to individual tactic justifications. A mathematician can, for example, ask “why did you
apply induction here?” and receive both a formal account of the tactic’s effect and an informal
description of the underlying mathematical intuition.

3.2   Proving Skill Orchestration

A central feature of M ATH C O P ILOT is that proving is not a fixed sequential pipeline but rather an
automated orchestration of skills that adapt based on the current proof state, Lean feedback, and
knowledge base content. The system maintains a pool of proving skills, such as NL-first (generate an
informal sketch, then incrementally formalize), formalization-first (fully formalize the statement, then
search for tactics via Lean’s own proof state), and knowledge-grounded proving (retrieve analogous
theorems and reusable lemmas from the user’s knowledge base before and during proof construction).
Rather than executing these skills in a predetermined order, an orchestrator dynamically selects and
composes skills at each step. The proving process typically proceeds as follows: the system begins
by analyzing the formal statement and searching the knowledge base for relevant prior results. Based
on this analysis, it selects an initial proving skill and generates a proof attempt. This attempt is
then submitted to the Lean 4 environment, which returns either a success signal or detailed error
information (e.g., type mismatches, missing hypotheses, incomplete tactics, unsolved goals). The
orchestrator parses this feedback, diagnoses the failure mode, and decides on the next action, which
may include retrying with a different skill, refining the current approach based on the specific error,
searching for additional lemmas in the knowledge base, or requesting human intervention.
The key insight is that this is not a fixed workflow but a flexible, feedback-driven orchestration. In
some cases, the NL-first skill may produce a clean proof on the first attempt. In others, the system
may switch between multiple skills, incorporate knowledge base results mid-proof, and iteratively
refine based on Lean feedback several times before arriving at a correct proof. The orchestrator learns
from historical proof attempts which skills tend to succeed for which types of problems, improving
its selection over time.

3.3   Automated Knowledge Base Construction and Maintenance

Given a research topic specified by the user, M ATH C O P ILOT can retrieve relevant papers from
multiple sources including Semantic Scholar, arXiv, and the Lean Mathlib, ranking them by relevance
score, citation count, and formalization potential. For each retrieved paper, an extraction agent
identifies formal definitions and their dependencies, theorem statements including all hypotheses
and conclusions, proof sketches and lemma chains, and the notation conventions used by the authors.
The extracted content is then translated into Lean 4 code using LLM prompting with access to the
Mathlib library as context, following a dependency-aware ordering where definitions are formalized


                                                   5
first, then auxiliary lemmas, then main theorems. Each formalized Lean file is compiled and verified
against the Lean 4 type checker, and only content that passes compilation enters the knowledge base.
Crucially, each knowledge base entry stores both the verified Lean 4 code and the natural language
proof process that led to it, including the informal reasoning chain, key insights at each step, and the
correspondence between natural language arguments and formal tactics. This dual representation
serves two purposes: it enables the system to provide natural language explanations when a mathe-
matician retrieves a lemma, and it allows the agents in Section 3.1 to reason about proofs in both
informal and formal terms.
Verified entries are indexed by topic tags, theorem names, dependency graphs, and natural language
summaries to support flexible retrieval. The knowledge base is personal: it grows organically as the
mathematician processes papers and proves theorems, accumulating a reusable repository tailored to
their research interests. The system also supports incremental maintenance: when the underlying
Lean environment (e.g., Mathlib) is updated, existing entries are automatically re-verified, and any
incompatibilities are flagged for the user.


4     FormalMATH Benchmark Experiments

We first evaluate M ATH C O P ILOT in a controlled benchmark setting using a sampled subset of
FormalMATH. This section isolates the effect of proving skill choice on undergraduate-level formal
mathematics, and then studies whether the full interactive proof-blueprint workflow can recover hard
cases unsolved by GPT-5.4 through recursive refinement of unresolved local proof obligations.

4.1   FormalMATH Experimental Setup

Models and routes. The FormalMATH study evaluates Gemini 3.1 Pro, GPT-5.4, and
Claude Opus 4.7. Each model is tested under two proving skills from Section 3.2: formalization-first
(FF), where the model works from the formal statement directly, and NL-first (NL), where it first
produces a natural-language proof sketch and then translates the argument into Lean.
FormalMATH subset. We sample 21 problems from FormalMATH to compare the proving skills,
with exactly three problems from each of seven domains: Algebra, Differentiation, Integral, Multi-
variable Calculus, Other, Precalculus, and Sequences and Series. Each problem contains a natural-
language statement, a formalized Lean statement, and a reference solution. The sampled problems
are listed in Appendix A.1. This gives 21 × 3 × 2 = 126 proof attempts.
GPT-unsolved subset. To evaluate the full our interactive system beyond a single baseline
prompting route, we select 12 cases that GPT-5.4 failed to solve: u-math_862, u-math_645,
u-math_166, u-math_839, u-math_93, u-math_237, hardmath_162, DEMIMathAnalysis_86,
DEMIMathAnalysis_26,            DEMIMathAnalysis_37,              DEMIMathAnalysis_19,           and
DEMIMathAnalysis_75. In this setting the system is allowed to use the interactive proof-
blueprint workflow: when a first formalization fails, the unresolved proof obligations are exposed as
local nodes, searched against standard mathematical facts, and recursively formalized until either
Lean verifies the node or the node remains open.
Verification protocol. We verify FormalMATH proofs with Lean 4.30.0-rc2 and Mathlib v4.30.0-rc2
under a 1200-second timeout. We report a strict pass rate: a proof passes only if lake env lean
accepts the file, the final proof is nonempty, and the file contains no sorry/placeholder proof. This
strict rule matters: Claude Opus 4.7 has 6/21 raw verifier passes under Formalization-First, but three
are empty formal-proof outputs and are therefore counted as failures.

4.2   FormalMATH Results

Table 1 shows the strict pass rates. The main pattern is simple: generating a natural-language proof
before Lean translation substantially improves reliability. The NL skill reaches 20/63 overall, exactly
double FF’s 10/63. The improvement is consistent across all three models, with gains of +14.29% for
Gemini and GPT and +19.05% for Opus after the empty-proof correction.
The domain-level heatmap in Table 2 gives a more informative view. The NL skill is not uniformly
better because the benchmark mixes very different formalization burdens. It gives large gains in


                                                   6
                 Table 1: Strict pass rates on the 21-problem FormalMATH subset.
                     Model                     FF                  NL         Gain
                     Gemini 3.1 Pro      4/21 (19.05%)      7/21 (33.33%)    +14.29
                     GPT-5.4             3/21 (14.29%)      6/21 (28.57%)    +14.29
                     Claude Opus 4.7     3/21 (14.29%)      7/21 (33.33%)    +19.05
                     Overall            10/63 (15.87%)     20/63 (31.75%)    +15.87



       Table 2: Domain heatmap for FormalMATH. Darker green indicates higher pass rate.
                                FF      NL     Gemini     Gemini    GPT     GPT   Opus   Opus
         Domain
                               Total   Total    FF         NL        FF     NL     FF     NL
         Integral               0/9     0/9     0/3        0/3      0/3     0/3   0/3     0/3
         Other                  0/9     0/9     0/3        0/3      0/3     0/3   0/3     0/3
         Seq./Series            0/9     0/9     0/3        0/3      0/3     0/3   0/3     0/3
         Multivariable Calc.    2/9     3/9     1/3        1/3      1/3     1/3   0/3     1/3
         Differentiation        0/9     6/9     0/3        2/3      0/3     2/3   0/3     2/3
         Algebra                3/9     4/9     1/3        1/3      1/3     1/3   1/3     2/3
         Precalculus            5/9     7/9     2/3        3/3      1/3     2/3   2/3     2/3



Differentiation, where FF solves none of the nine attempts but NL solves six, and in Precalculus,
where the per-skill score increases from 5/9 to 7/9. In contrast, Integral, Other, and Sequences and
Series remain at 0/18 across both skills and all models. These zero rows are important: they show
that failures are not merely model-choice noise, but often reflect missing formal infrastructure, brittle
theorem statements, or proof obligations that current single-turn prompting does not bridge.
Failure analysis further supports this interpretation. The most common blocking category is residual
sorry: 19 times under FF and 23 times under NL. Thus, the models often understand enough to
state a plausible proof plan but cannot discharge the Lean proof obligations. The NL skill reduces
this problem for tractable domains by giving the Lean stage a structured proof skeleton, but it
does not solve domains whose formal statements require substantial libraries or nontrivial analytic
machinery. Appendix A.2 gives a concrete NL-skill example from the Integral domain: all three
models identify the correct endpoint Laplace-method argument for hardmath_734, yet each final
Lean file still contains sorry. This case illustrates why strict verification can disagree with a
superficially convincing natural-language derivation.


4.3   Recovering Failures with M ATH C O P ILOT

Table 3 reports the recovery experiment on the 12 difficult FormalMATH cases unsolved by GPT-
5.4. In the first system pass, nine of the twelve cases are fully formalized and accepted by Lean
under the same strict rule used above. Three cases remain open: u-math_839, u-math_237, and
hardmath_162. The failure mode of hardmath_162 is qualitatively different from the other two:
the system produces a complete natural-language proof of the endpoint Laplace asymptotic, but
the Lean attempt stalls at local analytic and numerical sublemmas. When those sublemmas are
recursively exposed as proof-blueprint nodes, the system eventually formalizes the endpoint Laplace
statement completely, yielding a verified Lean certificate in tex/lean/Main.lean. Counting this
lemma-refinement stage, M ATH C O P ILOT verifies 10/12 of the targeted GPT-unsolved cases.
Table 4 gives a closer view of the most informative recovery case, hardmath_162. In the baseline
FormalMATH experiment, all six Gemini/GPT/Opus solutions on this problem, across both FF
and NL settings, end with the same failure category: the generated Lean file contains a top-level
sorry.The natural-language behavior is more nuanced. Some attempts identify the endpoint-Laplace
route, while others correctly notice that the autoformalized target is semantically brittle: the Lean
statement uses an outer parameter x, then shadows it inside the function whose limit is being taken,
and asks for convergence to a rounded expression depending on the outer x. In either case, the
baseline attempts do not convert the Laplace argument into checkable local proof obligations.


                                                      7
Table 3: M ATH C O P ILOT’s performance on twelve GPT-unsolved FormalMATH cases. “First
pass” counts the initial full-system attempt; “after refinement” allows recursive proof-blueprint
formalization of unsolved local lemmas.
      Problem                             Domain                       First pass                After refinement
      u-math_862                          Precalculus                  Pass                      Pass
      u-math_645                          Algebra                      Pass                      Pass
      u-math_166                          Integral                     Pass                      Pass
      u-math_839                          Multivariable Calc.          Fail                      Fail
      u-math_93                           Multivariable Calc.          Pass                      Pass
      u-math_237                          Sequences/Series             Fail                      Fail
      hardmath_162                        Integral                     Fail                      Pass
      DEMIMathAnalysis_86                 Other                        Pass                      Pass
      DEMIMathAnalysis_26                 Other                        Pass                      Pass
      DEMIMathAnalysis_37                 Differentiation              Pass                      Pass
      DEMIMathAnalysis_19                 Sequences/Series             Pass                      Pass
      DEMIMathAnalysis_75                 Other                        Pass                      Pass
      Total                               –                            9/12 (75.0%)              10/12 (83.3%)



Table 4: Detailed comparison on hardmath_162. Baseline evidence comes from the prior Formal-
MATH runs in formalbench_project.
    Attempt                Mathematical behavior             Lean behavior                        Main limitation or strength
    Gemini/GPT/Opus        Often identify the endpoint- All six generated Lean files in- No decomposition of derivative
    baselines, FF and NL Laplace structure or flag the stantiate a direct Tendsto target bounds, endpoint separation,
                           rounded target as problematic.  for the rounded expression and integration-by-parts remainder, or
                                                           end with sorry; verifier category: numerical enclosures into verified
                                                           contains_sorry.                         subgoals.
    M ATH C O P ILOT first Finds the correct left-endpoint Fails strict verification because local Failure is localized to explicit
    pass                   Laplace proof strategy and analytic and numerical lemmas re- proof-blueprint nodes rather than
                           produces a coherent natural- main unresolved.                           hidden in one monolithic place-
                           language derivation.                                                    holder.
    M ATH C O P ILOT re- Recursively formalizes the unre- Produces a complete Lean certifi- Turns the informal appeal
    finement               solved endpoint-Laplace lemma, cate with no placeholder proof in to Laplace’s method into
                           including exact asymptotics and the endpoint block.                     machine-checkable           mono-
                           rounded-constant bounds.                                                tonicity,    integration-by-parts,
                                                                                                   remainder, and interval-arithmetic
                                                                                                   obligations.



The hardmath_162 refinement is particularly informative. The unsolved obligation is not a high-level
proof strategy failure but the formalization of an endpoint Laplace lemma:
              Z 0.5
     I(x) =         (−0.9t2 )exϕ(t) dt,     ϕ(t) = 1.7t4 − 0.3t − 0.6 cos t − 2 arctan t + 2.6,
                  −0.7
with the target asymptotic
                                (−0.9)(−0.7)2 exϕ(−0.7)
                                I(x) ∼                                                (x → +∞),
                                    x(−ϕ′ (−0.7))
together with the numerical bounds
                                               (−0.9)(−0.7)2
                    |ϕ(−0.7) − 3.98| ≤ 0.001,                    + 0.10 ≤ 0.002.
                                                  −ϕ′ (−0.7)
These are standard consequences of the endpoint form of Laplace’s method plus concrete interval
estimates. The system decomposes them into derivative identities, endpoint separation, integration-
by-parts, remainder bounds, and numerical inequalities, after which Lean verifies the final theorem.
Appendix A.3 gives the detailed evidence.
The refined statement is also mathematically sharper than the displayed benchmark approximation.
The proof does not assert the strict asymptotic equivalence
                                               0.10e3.98x
                                                    I(x) ∼ −
                                                           ,
                                                    x
which would be sensitive to the rounded exponent. Instead, it proves the exact endpoint formula
                                                         −0.9(−0.7)2 exϕ(−0.7)
                                              I(x) ∼                           ,
                                                          −ϕ′ (−0.7)     x

                                                                   8
and separately proves that ϕ(−0.7) is within 0.001 of 3.98 and that the leading coefficient is within
0.002 of −0.10. This separation between exact asymptotics and rounded numerical presentation is
precisely the kind of distinction that the proof-blueprint workflow makes explicit.


5     PDE Theorem Proving Experiments

We next evaluate M ATH C O P ILOT on two real theorems from numerical PDE analysis. This setting is
deliberately more demanding than the FormalMATH benchmark: the statements come from actual
domain-specific analysis, the proofs rely on numerical-method concepts that are not fully developed
in Mathlib, and success depends on choosing a suitable formalization boundary rather than merely
finding a short tactic proof. We therefore treat the PDE study as a separate real-data evaluation of
whether current models can help with research-level mathematical formalization.

5.1   PDE Experimental Setup

Theorems. We use two real theorems from numerical PDE analysis. They are drawn from the
standard discontinuous Galerkin (DG) analysis pipeline for transport-dominated PDEs. Linear
advection is the canonical scalar model for wave propagation and conservation-law transport; upwind
DG schemes trace back to finite-element discretizations of neutron-transport equations and later
became a central family of high-order methods for hyperbolic conservation laws [Lesaint and Raviart,
1974, Cockburn et al., 1989, Cockburn and Shu, 2001]. The first is the semi-discrete upwind DG
error estimate for linear advection,

                               ∥u(·, T ) − uh (·, T )∥L2 (0,1) ≤ ChK+1 ,                            (1)

proved by splitting u − uh = (u − Πh u) + (Πh u − uh ), using Galerkin orthogonality, an energy esti-
mate, and Gronwall’s inequality, following the classical error-analysis template for scalar hyperbolic
DG methods [Johnson and Pitkäranta, 1986, Zhang and Shu, 2004]. The second is the Gauss–Radau
reference-cell projection estimate,

                               ∥Π̂ŵ − ŵ∥L2 (I)
                                              ˆ ≤ C|ŵ|H k+1 (I)
                                                              ˆ ,                                   (2)
                              ∥P w − w∥L2 (Ii ) ≤ Chk+1
                                                    i   |w|H k+1 (Ii ) .                            (3)

which represents the local approximation ingredient used in those DG analyses: endpoint matching
is aligned with the one-sided upwind flux, while the L2 bounds are consequences of polynomial
approximation, Bramble–Hilbert type estimates, and affine scaling from a reference cell to a physical
mesh cell [Bramble and Hilbert, 1970, Ciarlet, 2002, Zhang and Shu, 2004]. Appendix A.4 states the
two PDE cases in more detail.
Routes and models. For these two theorems, we adopt three routes. In the GPT-Formalized
and Opus-Formalized routes, GPT-5.4 and Claude Opus 4.7 respectively formalize the statement
into a Lean stub, which is then handed to each model to prove. In the Direct route, each model
formalizes the statement and writes both the natural-language and Lean proofs on its own. We
evaluate Gemini 3.1 Pro, GPT-5.4, and Claude Opus 4.7 on all three routes, and Claude Sonnet 4 on
the GPT-Formalized route. This yields 20 Lean proof attempts.
Verification protocol and scope. We use Lean 4.30.0 and Mathlib v4.30.0 under a 600-second
timeout. Current Mathlib does not contain a full formal development of DG methods, Sobolev
estimates, or Gauss–Radau projection theory. Therefore, successful PDE files often encode the deep
analytic ingredients as opaque declarations or axioms and then verify the formal assembly step
in Lean. We count these as successful Lean certificates, not as end-to-end formalizations of PDE
analysis from first principles. Consequently, the PDE pass rates in Table 5 are not directly comparable
to the end-to-end strict pass rates in Table 1.
Wrong-proof diagnostic. Because proof review is an important part of real mathematical work,
we also test wrong-proof detection by giving Gemini 3.1 Pro and GPT-5.4 deliberately flawed
proofs of the two PDE theorems. Appendices A.5 and A.6 summarize the proof-output patterns and
wrong-proof diagnostics.


                                                  9
Table 5: PDE theorem proving results. Each entry is Lean-checked certificates out of two. “Syntax”
denotes Lean-version/formalization incompatibility; “Logic” denotes a syntactically valid proof
attempt that fails during proof checking. These are not end-to-end formalizations of PDE analysis
from first principles.
                                 GPT             Opus
          Model                                                   Direct           Total
                              Formalized       Formalized
          Gemini 3.1 Pro      0/2 (Syntax)    2/2 (assembly)     0/2 (Logic)        2/6
          GPT-5.4             0/2 (Syntax)    2/2 (assembly)   2/2 (assembly)       4/6
          Claude Opus 4.7    2/2 (assembly)   2/2 (assembly)   2/2 (assembly)       6/6
          Claude Sonnet 4     0/2 (Syntax)           –                –             0/2
          Per-route total      2/8 (25%)       6/6 (100%)      4/6 (66.67%)     12/20 (60%)


5.2   Proof Synthesis Results

Table 5 summarizes the PDE proof synthesis results. The GPT-Formalized route performs poorly not
because the theorems are mathematically impossible, but because the GPT-produced formalizations
are associated with Lean-version and declaration-boundary incompatibilities, including generated
declarations that should instead be represented as explicit opaque or axiom assumptions in the
tested Lean 4.29 setting. This formalization/version issue causes Gemini, GPT-5.4, and Sonnet to
fail both theorems. Claude Opus 4.7 is the only model that adapts the formalization and produces
assembly certificates for both. The Opus-Formalized route yields assembly certificates for all six
tested attempts. The Direct route is intermediate: GPT-5.4 and Claude Opus 4.7 produce assembly
certificates for both theorems under their own declared assumptions, while Gemini 3.1 Pro produces
Lean files with logical/tactic-level failures.
These results reveal a different failure mode from the FormalMATH experiment. In the PDE setting,
the strongest closed models can produce mathematically coherent natural-language proofs: they
mention the correct DG error decomposition, the admissibility of the discrete error ξ = Πh u − uh as
a test function, energy stability, Gronwall’s inequality, and the Bramble–Hilbert/scaling argument for
Gauss–Radau projection. The main bottleneck is turning that understanding into a version-correct and
appropriately abstract Lean. Successful proofs typically separate the work into two layers: analytic
PDE facts are declared as explicit assumptions, while Lean verifies the algebraic combination, norm
inequality, or scaling step. Appendix A.5 summarizes representative PDE proof-output patterns and
identifies which analytic ingredients are treated as opaque declarations or axioms.
We also include an out-of-distribution diagnostic with two open-source theorem-proving models,
DeepSeek-Prover-V2 [Ren et al., 2025] and Goedel-Prover-V2 [Lin et al., 2025], on the DG theorem.
Both fail to produce valid Lean 4 code (0/2). Their outputs remain in natural-language meta-analysis
and then repeat until truncation. This suggests that specialization on competition-style formal
mathematics does not automatically transfer to PDE/numerical-analysis reasoning.

5.3   Wrong-Proof Detection

We additionally evaluate whether models can act as mathematical proof reviewers rather than proof
constructors. For each PDE theorem, we provide a polished but deliberately flawed proof and ask
Gemini 3.1 Pro and GPT-5.4 to decide whether the argument is correct and to locate the failure.
Both models correctly reject all four model-theorem pairs. The diagnostic cases in Appendix A.6
show that critique can be easier than construction: even when Lean proof generation depends on
abstracting away PDE theory with opaque declarations or axioms, the models can still recognize
invalid mathematical moves in natural-language proofs. This supports using M ATH C O P ILOT’s
Formalizer Agent as a complementary mode to proof synthesis, especially for domain-specific
arguments whose full formal library support is still incomplete.

6     Discussion
Our results highlight four key takeaways. Current models show meaningful capability on
undergraduate-level formal mathematics, but this capability is highly sensitive to the autoformal-


                                                 10
Table 6: Wrong-proof detection on the two PDE examples. “Judgment” records whether the model
correctly rejects the flawed proof; “coverage” summarizes which planted issue is explicitly identified.
    Model              DG L2 estimate                         Gauss–Radau estimate                    Judgment
    Gemini 3.1 Pro     Rejects the proof and identifies the   Rejects the proof and identifies that     Pass
                       decisive illegal test function e =     F (ŵ) = ∥Π̂ŵ − ŵ∥L2 is a norm of
                       u − uh ∈  / UhK ; it also notes that   an error, not a linear functional.
                       interface terms form a jump contri-
                       bution rather than canceling.
    GPT-5.4            Rejects the proof, explicitly states   Rejects the proof, explains the non-      Pass
                       that Galerkin orthogonality holds      linearity of F (ŵ), and proposes
                       only for φh ∈ UhK , and identifies     a corrected operator or seminorm-
                       the illegal choice φ = e.              based Bramble–Hilbert argument.


ization pipeline and to the domain’s available formal infrastructure. The NL-first skill consistently
outperforms formalization-first on the FormalMATH subset, validating the intuition that informal
reasoning provides a valuable scaffold for formalization. The recovery study further shows that an
interactive proof-blueprint loop can recover many hard cases missed by a strong baseline: among
twelve GPT-5.4-missed cases, the system produces strict Lean certificates for 9/12 immediately and
10/12 after local lemma refinement. Finally, the gap between benchmark proofs and PDE certificates,
together with the wrong-proof diagnostic, underscores that proof construction, formal certification,
and mathematical critique remain distinct skills.
These findings carry practical implications: investing in better autoformalization pipelines may yield
larger returns than scaling up model size, and evaluation of formal mathematics systems should
include domain-specific problems alongside curated benchmarks.

7      Conclusion and Future Work
We presented M ATH C O P ILOT, a human-in-the-loop system embodying a human–AI symbiotic
paradigm for mathematical research, which unifies knowledge construction, automated proving
skill orchestration, and interactive human–AI collaboration. Our experiments across four state-
of-the-art LLMs reveal that these models demonstrate strong capability on undergraduate-level
formal mathematics, that the NL-first proving skill achieves higher accuracy than formalization-first,
and that autoformalization quality has a decisive impact on proving success. At the same time,
performance on real PDE theorems and error detection tasks shows that substantial challenges remain
for domain-specific mathematical reasoning.
Several directions for future work are promising. Integrating with community resources such as
Mathlib to bootstrap larger knowledge bases would enable cross-community knowledge sharing and
reduce the cold-start problem for new users. Training the skill orchestrator to learn from historical
proof attempts could develop domain-specific skill preferences that improve with use. Supporting
collaborative knowledge bases across research groups, with access control, versioning, and merge
capabilities, would extend the system from individual to team-level use. Extending beyond Lean 4
to support Coq, Isabelle, and other proof assistants would enable cross-system knowledge transfer.
Finally, conducting rigorous user studies with larger participant pools and controlled experiments
would quantify the impact on research productivity.

References
Kaito Baba, Chaoran Liu, Shuhei Kurita, and Akiyoshi Sannai. Prover agent: An agent-based
  framework for formal mathematical proofs. In 2nd AI for Math Workshop@ ICML 2025, 2025.
J. H. Bramble and S. R. Hilbert. Estimation of linear functionals on Sobolev spaces with application
   to Fourier transforms and spline interpolation. SIAM Journal on Numerical Analysis, 7(1):112–124,
   1970. doi: 10.1137/0707006.
Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin,
  Xing Jin, Chenggang Li, Kaijing Ma, et al. Seed-prover: Deep and broad reasoning for automated
  theorem proving. arXiv preprint arXiv:2507.23726, 2025.


                                                    11
Philippe G. Ciarlet. The Finite Element Method for Elliptic Problems. Classics in Applied Mathe-
  matics. Society for Industrial and Applied Mathematics, 2002. doi: 10.1137/1.9780898719208.
  Reprint of the 1978 North-Holland edition.
Bernardo Cockburn and Chi-Wang Shu. Runge–Kutta discontinuous Galerkin methods for convection-
  dominated problems. Journal of Scientific Computing, 16(3):173–261, 2001. doi: 10.1023/A:
  1012873910884.
Bernardo Cockburn, San-Yih Lin, and Chi-Wang Shu. TVB Runge–Kutta local projection discontin-
  uous Galerkin finite element method for conservation laws III: One-dimensional systems. Journal
  of Computational Physics, 84(1):90–113, 1989. doi: 10.1016/0021-9991(89)90183-6.
Alex Davies, Petar Veličković, Lars Buesing, Sam Blackwell, Daniel Zheng, Nenad Tomašev,
  Richard Tanburn, Peter Battaglia, Charles Blundell, András Juhász, et al. Advancing mathematics
  by guiding human intuition with ai. Nature, 600(7887):70–74, 2021.
Leonardo Mendonça de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming
  language. CADE, 2021.
Yilin Du, Shengang Li, Antonio Torralba, Joshua Tenenbaum, and Igor Mordatch. Improving
  factuality and reasoning in language models through multiagent debate. In ICLR, 2023.
Manuel Eberl et al. Isabelle and LLMs – an emerging symbiosis. arXiv preprint arXiv:2405.15449,
 2024.
Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z Horváth, Goran Žužić, Eric Wieser, Aja
  Huang, Julian Schrittwieser, Yannick Schroecker, Hussain Masoom, et al. Olympiad-level formal
  mathematical reasoning with reinforcement learning. Nature, pages 1–3, 2025.
Geoffrey Irving, Christian Szegedy, Alexander A Alemi, Niklas Eén, François Chollet, and Josef
  Urban. Deepmath-deep sequence models for premise selection. Advances in neural information
  processing systems, 29, 2016.
Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou, Timothee Lacroix, Jiacheng Liu, Wenda Li,
  Mateja Jamnik, Guillaume Lample, and Yuhuai Wu. Draft, sketch, and prove: Guiding formal
  theorem provers with informal proofs. In The Eleventh International Conference on Learning
  Representations, 2023.
C. Johnson and J. Pitkäranta. An analysis of the discontinuous Galerkin method for a scalar
  hyperbolic equation. Mathematics of Computation, 46(173):1–26, 1986. doi: 10.1090/
  S0025-5718-1986-0815828-4.
Haocheng Ju, Guoxiong Gao, Jiedong Jiang, Bin Wu, Zeming Sun, Leheng Chen, Yutong Wang,
 Yuefeng Wang, Zichen Wang, Wanyi He, et al. Automated conjecture resolution with formal
  verification. arXiv preprint arXiv:2604.03789, 2026.
Minsu Kim and Se-Young Yun. Process-verified reinforcement learning for theorem proving via lean.
 In The 5th Workshop on Mathematical Reasoning and AI at NeurIPS 2025, 2025.
P. Lesaint and P. A. Raviart. On a finite element method for solving the neutron transport equation. In
   Mathematical Aspects of Finite Elements in Partial Differential Equations, pages 89–123. Elsevier,
   1974. doi: 10.1016/B978-0-12-208350-1.50008-X.
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,
  Jiawei Ge, Jingruo Sun, et al. Goedel-prover-v2: Scaling formal theorem proving with scaffolded
  data synthesis and self-correction. arXiv preprint arXiv:2508.03613, 2025.
Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos Santos, Weikun He, Jiawei Liu, Ran Wang, Yunzhou
  Xie, Junqiao Zhao, Qiufeng Wang, et al. Numina-lean-agent: An open and general agentic
  reasoning system for formal mathematics. arXiv preprint arXiv:2601.14027, 2026.
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya
  Sutskever. Formal mathematics statement curriculum learning. In The Eleventh International
  Conference on Learning Representations, 2023.


                                                  12
ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang,
  Zhe Fu, Qihao Zhu, Dejian Yang, et al. Deepseek-prover-v2: Advancing formal mathematical
  reasoning via reinforcement learning for subgoal decomposition. arXiv preprint arXiv:2504.21801,
  2025.
Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Lean copilot: Large language models as
  copilots for theorem proving in lean. In International Conference on Neuro-symbolic Systems,
  pages 144–169. PMLR, 2025.
Nat Sothanaphan. Resolution of erd\h {o} s problem# 728: a writeup of aristotle’s lean proof. arXiv
  preprint arXiv:2601.07421, 2026.
Terence Tao. Machine-assisted proof. Notices of the American Mathematical Society, 72(1):6–13,
  2025.
Amitayush Thakur, George Tsoukalas, Yeming Wen, Jimmy Xin, and Swarat Chaudhuri. An
 in-context learning agent for formal theorem-proving. arXiv preprint arXiv:2310.04353, 2023.
Tyler Ulirsch et al. Blueprint: A retrospection on foundations of mathematics from the lean perspec-
  tive. arXiv preprint arXiv:2208.02025, 2022.
Sumanth Varambally, Thomas Voice, Yanchao Sun, Zhifeng Chen, Rose Yu, and Ke Ye. Hilbert:
  Recursively building formal proofs with informal reasoning. arXiv preprint arXiv:2509.22819,
  2025.
Mingzhe Wang, Yihe Tang, Jian Wang, and Jia Deng. Premise selection for theorem proving by deep
 graph embedding. Advances in neural information processing systems, 30, 2017.
Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe Diao, Renjie Pi, and Tong Zhang. The-
  oremllama: Transforming general-purpose llms into lean4 experts. In Proceedings of the 2024
  Conference on Empirical Methods in Natural Language Processing, pages 11953–11974, 2024.
Yiran Wu, Feiran Jia, Shaokun Zhang, Hangyu Li, Erkang Zhu, Yue Wang, Yin Tat Lee, Richard
  Peng, Qingyun Wu, and Chi Wang. Mathchat: Converse to tackle challenging math problems with
  llm agents. arXiv preprint arXiv:2306.01337, 2023.
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus Rabe, Charles Staats, Mateja Jamnik, and
  Christian Szegedy. Autoformalization with large language models. Advances in neural information
  processing systems, 35:32353–32368, 2022.
Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li,
  and Xiaodan Liang. Deepseek-prover: Advancing theorem proving in llms through large-scale
  synthetic data. arXiv preprint arXiv:2405.14333, 2024.
Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue
  Zhang, Xuan Lu, Qiushi Du, et al. Deepseek-prover-v1. 5: Harnessing proof assistant feedback
  for reinforcement learning and monte-carlo tree search. In International Conference on Learning
 Representations, volume 2025, pages 72274–72303, 2025.
Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
  Ryan Prenger, and Anima Anandkumar. Leandojo: Theorem proving with retrieval-augmented
  language models. In Advances in Neural Information Processing Systems 36 (NeurIPS), pages
  21573–21612, 2023. Oral Presentation.
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
  React: Synergizing reasoning and acting in language models. In ICLR, 2023.
Qiang Zhang and Chi-Wang Shu. Error estimates to smooth solutions of Runge–Kutta discontinuous
  Galerkin methods for scalar conservation laws. SIAM Journal on Numerical Analysis, 42(2):
  641–666, 2004. doi: 10.1137/S0036142902404182.
Shaowei Zhang and Deyi Xiong. Debate4math: Multi-agent debate for fine-grained reasoning in math.
  In Findings of the Association for Computational Linguistics: ACL 2025, pages 16810–16824,
  2025.


                                                13
A      Appendix

This appendix provides compact case-level details supporting the aggregate results. We first present
seven representative FormalMATH problems, one from each sampled domain, to make the benchmark
composition concrete. We then analyze the hardmath_734 Integral case as a representative NL-skill
failure and the hardmath_162 refinement as a representative M ATH C O P ILOT recovery case, before
turning to the two PDE diagnostics used for proof synthesis and wrong-proof detection.

A.1    Seven Representative FormalMATH Problems

To make the benchmark composition transparent, we present one representative problem from each
sampled FormalMATH domain. These examples expose the heterogeneous nature of the subset,
which ranges from algebraic simplification and elementary differentiation to asymptotic integration,
multivariable integration, functional-equation nonexistence, and sequence-space convergence.

      Problem 1: Algebra                                                                        u-math_551

    Statement.    Subtract the rational expression, then simplify:
                                                    12     6
                                                        −     .
                                                    2·q   3·p

    Target.   Prove that the simplified expression is
                                                     6·p−2·q
                                                             .
                                                       p·q


      Problem 2: Differentiation                                                    DEMIMathAnalysis_37

    Statement.    Suppose that f ∈ C 2 (0, ∞) converges to α as x → ∞, and that
                                                   f ′′ (x) + λf ′ (x)
    is bounded above for some constant λ.

    Target.   Show that
                                           f ′ (x) → 0          (x → ∞).


      Problem 3: Integral                                                                     hardmath_162

    Statement.    Consider the integral
                             Z 0.5
                                                     4
                    I(x) =         (−0.9t2 )e−x(−1.7t +0.3t+0.6 cos(t)+2.0 atan(t)−2.6) dt.
                               −0.7

    Develop an analytical formula for I(x) that is accurate as x → ∞.

    Target.   Prove the leading asymptotic form
                                                            0.10e3.98x
                                                 I(x) ≈ −              .
                                                                x


      Problem 4: Multivariable Calculus                                                         u-math_839

    Statement.    Evaluate the triple integral       ZZZ
                                                               z dV,
                                                           E




                                                          14
where E is the region                                                      
                                  
                                               −y ≤ x ≤ y,                 
                                                                            
                             E=       (x, y, z)  0 ≤ y ≤ 1,                       .
                                                    0 ≤ z ≤ 1 − x4 − y 4
                                  
                                                                           
                                                                            

Target.   Prove that                      ZZZ
                                                                113
                                                    z dV =          .
                                                E               450


Problem 5: Other                                                                      DEMIMathAnalysis_26

Statement.    Consider continuous functions
                                            f, g, h : R → R.
The claimed functional equation is
                                         h(f (x) + g(y)) = xy
                  2
for all (x, y) ∈ R .

Target.   Show that no such continuous functions f , g, and h exist.


Problem 6: Precalculus                                                                         u-math_862

Statement.    Calculate the derivative
                                               d
                                                 (logx (a))
                                              dx
under the assumptions
                              x > 0,       a > 0,           x ̸= 1,     a ̸= 1.

Target.   Prove that
                                        d                 ln(a)
                                          (logx (a)) = −          .
                                       dx                x(ln x)2


Problem 7: Sequences and Series                                                       DEMIMathAnalysis_19

Statement.    Suppose that
                                                ∞
                                                X
                                                      an bn
                                                n=1
converges for every sequence {bn } satisfying
                                              ∞
                                              X
                                                b2n < ∞.
                                              n=1


Target.   Prove that
                                                    ∞
                                                    X
                                                          a2n
                                                    n=1
also converges.




                                                     15
A.2   Case C: hardmath_734 NL-First Outputs




  Problem: hardmath_734                                                                       Domain: Integral

  Consider the integral
                Z −0.1
                                                                       5
                        2.7t5 + 1.5 sin(t) − 1.1 cos(t) + 0.5 e+x(−0.5t +4.1 cos(t)+1.9 atan(t)) dt.
                                                             
       I(x) =                                                                                                    (4)
                 −0.8

  Develop an analytical formula for I(x) that is accurate as x → ∞. Prove that the answer is:

                                                           0.32e3.89x
                                             I(x) ≈ −                 .
                                                               x


  REFERENCE SOLUTION

  The integral is of the form
                                                     Z b
                                          I(x) =           g(t)e+xf (t) dt,                                      (5)
                                                       a
  where a = −0.8, b = −0.1,
      g(t) = 2.7t5 + 1.5 sin(t) − 1.1 cos(t) + 0.5,                 f (t) = −0.5t5 + 4.1 cos(t) + 1.9 atan(t).
  This means we can use Laplace’s method to develop an analytical approximation in the limit that x → ∞.
  In this limit, the integral will be dominated by the integrand near the maximum of f (t) within the bounds
  [−0.8, −0.1]. So, to simplify the integral, we will expand the integrand around this maximum.
  However, it is impossible to compute the maximum of f (t) within these bounds analytically. We,
  therefore, find the maximum numerically with the dual annealing algorithm. Using a few iterations of
  dual annealing, we find that the maximum of f (t) occurs at t0 = [−0.1].
  Since the integral is dominated by the value of the integrand near t0 = b, we Taylor expand the integrand
  around this point:
                               Z b
                                                                                  ′
                                    g(b) + (t − b)g ′ (b) + · · · e+x(f (b)+(t−b)f (b)+··· ) dt.
                                                                 
                      I(x) =                                                                              (6)
                                a

  We can then approximate
                                             Z b
                                                                            ′
                                    I(x) ≈         g(b)e+x(f (b)+(t−b)f (b)) dt.                                 (7)
                                              a
  Pulling out the constant in the integral gives
                                                            Z b
                                                                                ′
                                    I(x) ≈ g(b)e+xf (b)             e+x(t−b)f (b) dt.                            (8)
                                                                a

  We perform the change of variables u = x(t − b)|f ′ (b)|, rewriting the integral as
                                               Z 0
                                                                    1
                           I(x) ≈ g(b)e+xf (b)                      ′
                                                                         eu du.                                  (9)
                                                x(a−b)|f ′ (b)| x|f (b)|

  Since we are interested in a solution for I(x) as x → ∞, we can simplify the integral by approximating
  the lower bound as                                            Z 0
                                                         1
                                  I(x) ≈ g(b)e+xf (b)               eu du.                          (10)
                                                      x|f ′ (b)| −∞
  Solving the integral and evaluating, we find that

                                                           0.32e3.89x
                                             I(x) ≈ −                 .                                      (11)
                                                               x




                                                           16
   NL-First Summary

   All three NL-First outputs identify the correct high-level asymptotic method: endpoint Laplace method
   near b = −0.1. However, all three Lean 4 files end with sorry. Under the strict evaluation rule, any
   proof containing sorry is marked as failed, even when Lean reports only a warning.



Gemini 3.1 Pro NL-First Natural-Language Proof

Given:    The integral
             Z −0.1
                                                                   5
                     2.7t5 + 1.5 sin(t) − 1.1 cos(t) + 0.5 ex(−0.5t +4.1 cos(t)+1.9 atan(t)) dt.
                                                          
      I(x) =
                −0.8

We are tasked with developing an analytical formula for I(x) that is accurate as x → ∞ and proving
that
                                                0.32e3.89x
                                      I(x) ≈ −             .
                                                     x

Derivation:     Let us define the amplitude function f (t) and the phase function g(t) from the
integrand such that
                                         Z −0.1
                                  I(x) =        f (t)exg(t) dt :
                                               −0.8
               5
     f (t) = 2.7t + 1.5 sin(t) − 1.1 cos(t) + 0.5,       g(t) = −0.5t5 + 4.1 cos(t) + 1.9 atan(t).
To find the asymptotic behavior of I(x) as x → ∞, we apply Laplace’s method. We first analyze the
exponent function g(t) to locate its maximum on the interval [−0.8, −0.1]. The first derivative of
g(t) with respect to t is
                                                                  1.9
                                g ′ (t) = −2.5t4 − 4.1 sin(t) +        .
                                                                1 + t2
We must determine the sign of g ′ (t) for t ∈ [−0.8, −0.1]. Because t < 0 on this interval, sin(t) < 0,
which implies that the term −4.1 sin(t) is strictly positive. We can establish a strict lower bound for
g ′ (t) by minimizing each of its terms independently on the interval [−0.8, −0.1]:
                       1.9
 1. The rational term 1+t 2 is positive and monotonically decreasing in magnitude as |t| increases. Its

    minimum on the interval occurs at t = −0.8, yielding
                                          1.9        1.9
                                                 2
                                                   =      ≈ 1.1585.
                                      1 + (−0.8)     1.64
 2. The trigonometric term −4.1 sin(t) is positive and its minimum occurs at t = −0.1, yielding
                              −4.1 sin(−0.1) ≈ −4.1(−0.0998) ≈ 0.4093.
 3. The polynomial term −2.5t4 is negative and its minimum occurs at t = −0.8, yielding
                               −2.5(−0.8)4 = −2.5(0.4096) = −1.0240.

Summing these minimum contributions provides a lower bound for the derivative:
                           g ′ (t) ≥ −1.0240 + 0.4093 + 1.1585 = 0.5438.
Because g ′ (t) ≥ 0.5438 > 0 for all t ∈ [−0.8, −0.1], the function g(t) is strictly increasing on
the entire interval. Consequently, g(t) attains its unique absolute maximum at the right endpoint,
b = −0.1.
We now invoke the standard theorem for Laplace’s method: If f (t) and g(t) are smooth functions,
and g(t) attains its strict global maximum on [a, b] at the right endpoint b with g ′ (b) > 0, then as
x → ∞, the integral is asymptotically equivalent to
                                                   f (b) xg(b)
                                         I(x) ∼            e   .
                                                  xg ′ (b)

                                                    17
The functions f (t) and g(t) are composed of polynomials, trigonometric, and inverse trigonometric
functions, which are smooth everywhere on [−0.8, −0.1]. We have already established that the
maximum is at b = −0.1 and g ′ (−0.1) > 0. Thus, the hypotheses are fully satisfied.
Next, we evaluate f (b), g(b), and g ′ (b) at b = −0.1:
                  f (−0.1) = 2.7(−0.1)5 + 1.5 sin(−0.1) − 1.1 cos(−0.1) + 0.5,
        f (−0.1) ≈ 2.7(−0.00001) + 1.5(−0.099833) − 1.1(0.995004) + 0.5 ≈ −0.744282.
                    g(−0.1) = −0.5(−0.1)5 + 4.1 cos(−0.1) + 1.9 atan(−0.1),
          g(−0.1) ≈ −0.5(−0.00001) + 4.1(0.995004) + 1.9(−0.099669) ≈ 3.890152.
                                                                      1.9
                      g ′ (−0.1) = −2.5(−0.1)4 − 4.1 sin(−0.1) +              ,
                                                                  1 + (−0.1)2
                                                                 1.9
                g ′ (−0.1) ≈ −2.5(0.0001) − 4.1(−0.099833) +           ≈ 2.290255.
                                                                 1.01
Substituting these numerical values into the asymptotic formula gives
                            −0.744282 3.890152x       0.324978 3.890152x
                       I(x) ∼          e         ≈−           e          .
                            2.290255x                      x
Rounding the coefficient and the exponent to two decimal places, we obtain the final analytical
formula:
                                              0.32e3.89x
                                    I(x) ≈ −             .
                                                  x
   Lean 4 formal_proof: Gemini 3.1 Pro

   import Mathlib

   open Real Filter Function
   open scoped BigOperators Topology

   theorem hardmath_734R (I : R → R)
     (hI : I = λ x =>    t in (-0.8)..(-0.1), (2.7*t^5 + 1.5*sin t - 1.1*cos t + 0.5) *
       exp (x * (-0.5*t^5 + 4.1*cos t + 1.9*arctan t))) :
     ∀ ε > 0, ∃ x_0, ∀ x > x_0, |I x + 0.32 * exp (3.89 * x) / x| < ε := by
     sorry



   Verification Failure

   Status: failed                    Category: contains_sorry                          Location: line 6
   Lean diagnostic: declaration uses sorry
   Reason: The Lean file contains sorry. Although Lean returns only a warning, this evaluation treats any
   sorry as an incomplete proof, so the model does not receive credit.
   5:
   6: theorem hardmath_734R (I : R → R)
   7:   (hI : I = λ x =>     t in (-0.8)..(-0.1), (2.7*t^5 + 1.5*sin t - 1.1*cos t + 0.5) *




GPT-5.4 NL-First Natural-Language Proof

We are given, for real x,
                                              Z −0.1
                                     I(x) =            A(t)exΦ(t) dt,
                                                −0.8
where
                              A(t) = 2.7t5 + 1.5 sin t − 1.1 cos t + 0.5
and
                              Φ(t) = −0.5t5 + 4.1 cos t + 1.9 arctan t.


                                                    18
We must find the leading asymptotic behavior of I(x) as x → +∞.
The integral is of Laplace type. Its leading contribution comes from the point in the interval
[−0.8, −0.1] where the phase function Φ is maximal. We first identify this point. Differentiating Φ
gives
                                                                 1.9
                                Φ′ (t) = −2.5t4 − 4.1 sin t +         .
                                                               1 + t2
For t ∈ [−0.8, −0.1], we have sin t < 0, so −4.1 sin t > 0. Also t4 ≤ 0.84 and 1 + t2 ≤ 1 + 0.82 =
1.64. Hence
                                                             1.9
                                     Φ′ (t) ≥ −2.5(0.8)4 +        .
                                                            1.64
Since
                                  2.5(0.8)4 = 2.5(0.4096) = 1.024
and
                                          1.9
                                              ≈ 1.158536585,
                                         1.64
we obtain
                                Φ′ (t) ≥ −1.024 + 1.158536585 > 0.
Thus Φ is strictly increasing on [−0.8, −0.1]. Therefore its maximum occurs at the right endpoint
                                               b = −0.1.

We now apply the endpoint form of Laplace’s method. The relevant standard statement is the
following: if A, Φ are continuously differentiable on [a, b], Φ′ (t) > 0 on [a, b], then as x → +∞,
                        Z b                                         xΦ(b) 
                                  xΦ(t)        A(b) xΦ(b)            e
                            A(t)e       dt =     ′ (b)
                                                       e      +O              .
                         a                    xΦ                       x2
Indeed, setting U (t) = A(t)/Φ′ (t), we have
                                                 U (t) d  xΦ(t) 
                                  A(t)exΦ(t) =            e        .
                                                  x dt
Integration by parts gives
              Z b
                                  U (b)exΦ(b)   U (a)exΦ(a)   1 b ′
                                                                Z
                  A(t)exΦ(t) dt =             −             −      U (t)exΦ(t) dt.
               a                       x             x        x  a

Since Φ is strictly increasing, Φ(a) < Φ(b), so the lower endpoint term is exponentially smaller than
exΦ(b) /x. Also, because Φ′ (t) is bounded below by a positive constant and U ′ is continuous, the
final integral is O(exΦ(b) /x). Therefore the error term is O(exΦ(b) /x2 ), proving the stated endpoint
asymptotic formula.
In our case a = −0.8 and b = −0.1. We compute the phase value at b:
                   Φ(−0.1) = −0.5(−0.1)5 + 4.1 cos(0.1) + 1.9 arctan(−0.1).
Since (−0.1)5 = −10−5 , this becomes
                      Φ(−0.1) = 0.000005 + 4.1 cos(0.1) − 1.9 arctan(0.1).
Using
                cos(0.1) ≈ 0.995004165278,          arctan(0.1) ≈ 0.099668652491,
we get
             Φ(−0.1) ≈ 0.000005 + 4.1(0.995004165278) − 1.9(0.099668652491).
Thus
                                     Φ(−0.1) ≈ 3.8901516379.
Next,
                A(−0.1) = 2.7(−0.1)5 + 1.5 sin(−0.1) − 1.1 cos(−0.1) + 0.5.
Using sin(−0.1) = − sin(0.1) and cos(−0.1) = cos(0.1), this is
                    A(−0.1) = −0.000027 − 1.5 sin(0.1) − 1.1 cos(0.1) + 0.5.


                                                  19
With
                  sin(0.1) ≈ 0.099833416647,             cos(0.1) ≈ 0.995004165278,
we find
                                     A(−0.1) ≈ −0.7442817068.
Finally,
                                                                            1.9
                    Φ′ (−0.1) = −2.5(−0.1)4 − 4.1 sin(−0.1) +                       .
                                                                        1 + (−0.1)2
Therefore
                                                                          1.9
                            Φ′ (−0.1) = −0.00025 + 4.1 sin(0.1) +             .
                                                                         1.01
Using sin(0.1) ≈ 0.099833416647, we obtain
                                      Φ′ (−0.1) ≈ 2.2902551271.
Hence
                         A(−0.1)      −0.7442817068
                                    ≈                   ≈ −0.32497764.
                        Φ′ (−0.1)      2.2902551271
Therefore Laplace’s endpoint formula gives the precise leading asymptotic behavior
                                                      3.8901516379...x 
                0.32497764 . . . 3.8901516379...x       e
       I(x) = −                 e                 +O                          (x → +∞).
                       x                                      x2
Equivalently,
                                        0.32497764 . . . 3.8901516379...x
                              I(x) ∼ −                  e                 .
                                               x
Rounding the coefficient −0.32497764 . . . to two decimal places gives −0.32, and rounding the
exponent coefficient 3.8901516379 . . . to two decimal places gives 3.89. Thus the leading asymptotic
approximation may be written as
                                                  0.32e3.89x
                                        I(x) ≈ −              ,
                                                       x
which is the claimed formula. The fully precise asymptotic form retains the constants 0.32497764 . . .
and 3.8901516379 . . . displayed above.

   Lean 4 formal_proof: GPT-5.4

   import Mathlib

   open Real Filter Function
   open scoped BigOperators Topology

   theorem hardmath_734R (I : R → R)
     (hI : I = λ x =>    t in (-0.8)..(-0.1), (2.7*t^5 + 1.5*sin t - 1.1*cos t + 0.5) *
       exp (x * (-0.5*t^5 + 4.1*cos t + 1.9*arctan t))) :
     ∀ ε > 0, ∃ x_0, ∀ x > x_0, |I x + 0.32 * exp (3.89 * x) / x| < ε := by
     sorry



   Verification Failure

   Status: failed                    Category: contains_sorry                          Location: line 6
   Lean diagnostic: declaration uses sorry
   Reason: The Lean file contains sorry. Although Lean returns only a warning, this evaluation treats any
   sorry as an incomplete proof, so the model does not receive credit.
   5:
   6: theorem hardmath_734R (I : R → R)
   7:   (hI : I = λ x =>     t in (-0.8)..(-0.1), (2.7*t^5 + 1.5*sin t - 1.1*cos t + 0.5) *



Claude Opus 4.7 NL-First Natural-Language Proof

Proof Plan:


                                                    20
1. Identify the Integral Form. The given function I(x) is an integral of the form
                                            Z b
                                    I(x) =      g(t)exf (t) dt,
                                                  a
    where
     • a = −0.8, b = −0.1;
     • g(t) = 2.7t5 + 1.5 sin t − 1.1 cos t + 0.5;
     • f (t) = −0.5t5 + 4.1 cos t + 1.9 arctan t.
2. Analyze the Phase Function f (t). To determine the asymptotic behavior of I(x) as x → ∞, we
   use Laplace’s method. We first find the maximum of f (t) on the interval [−0.8, −0.1].
   The derivative is
                                                                      1.9
                                   f ′ (t) = −2.5t4 − 4.1 sin t +           .
                                                                    1 + t2
                                                                        1.9
   For t ∈ [−0.8, −0.1], sin t < 0, so −4.1 sin t > 0. The term 1+t        2 is also positive and bounded
                1.9
   below by 1.64 ≈ 1.15. The negative term −2.5t is at most −2.5(0.8)4 ≈ −1.024. Thus,
                                                           4

   f ′ (t) > 0 strictly on the interval. Since f (t) is strictly increasing, its maximum occurs at the
   right endpoint b = −0.1.
3. Evaluate Functions at the Maximum.
    • f (−0.1) ≈ −0.5(−0.00001) + 4.1(0.995004) + 1.9(−0.099668) ≈ 3.890;
    • g(−0.1) ≈ 2.7(−0.00001) + 1.5(−0.099833) − 1.1(0.995004) + 0.5 ≈ −0.744;
    • f ′ (−0.1) ≈ −2.5(0.0001) − 4.1(−0.099833) + 1.01
                                                    1.9
                                                        ≈ 2.290.
4. Apply Laplace’s Method. For a maximum at the boundary b with f ′ (b) > 0, Laplace’s method
   gives the asymptotic expansion
                                             g(b) xf (b)
                                  I(x) ∼             e       as x → ∞.
                                            xf ′ (b)
    Substituting the evaluated constants,
                                           −0.744 3.89x         e3.89x
                                 I(x) ∼           e     ≈ −0.32        .
                                           2.290x                 x
5. Conclusion. The asymptotic equivalence implies that the difference
                                                    e3.89x
                                                          
                                    I(x) − −0.32
                                                       x
    goes to 0 (or is bounded appropriately) as x → ∞. Thus, for any ε > 0, there exists x0 such that
    for all x > x0 ,
                                                    e3.89x
                                        I(x) + 0.32        < ε.
                                                      x
Note on Formalization: Formalizing this proof requires a general version of Laplace’s method for the
asymptotic expansion of integrals, which involves deep results in real and complex analysis. Since
Mathlib currently lacks the necessary library for asymptotic expansions of integrals (like Watson’s
lemma or Laplace’s method), this theorem is genuinely impossible to complete without placeholders.
We therefore conclude the proof with sorry.

  Lean 4 formal_proof: Claude Opus 4.7

  import Mathlib

  open Real Filter Function
  open scoped BigOperators Topology

  theorem hardmath_734R (I : R → R)
    (hI : I = λ x =>    t in (-0.8)..(-0.1), (2.7*t^5 + 1.5*sin t - 1.1*cos t + 0.5) *




                                                  21
  Table 7: Proof-blueprint decomposition used to formalize the hardmath_162 endpoint lemma.
   Lean node                    Mathematical role                                         Status
   proof_step_1–3               Derivative formulae and endpoint separation showing       Pass
                                that the phase is maximized at the left endpoint.
   proof_step_4–7               Integration-by-parts reduction using the quotient         Pass
                                q(t) = f (t)/(−ϕ′ (t)).
   proof_step_8                 Boundary and remainder estimates for the endpoint         Pass
                                Laplace expansion.
   proof_step_9                 Assembly of the exact first-order asymptotic equiva-      Pass
                                lence.
   proof_step_10–12             Concrete interval estimates for ϕ(−0.7) and the lead-     Pass
                                ing coefficient.
   endpoint laplace             Final Lean-facing theorem matching the manuscript         Pass
   first order and main         statement.
   theorem



        exp (x * (-0.5*t^5 + 4.1*cos t + 1.9*arctan t))) :
      ∀ ε > 0, ∃ x_0, ∀ x > x_0, |I x + 0.32 * exp (3.89 * x) / x| < ε := by
      sorry



   Verification Failure

   Status: failed                    Category: contains_sorry                          Location: line 6
   Lean diagnostic: declaration uses sorry
   Reason: The Lean file contains sorry. Although Lean returns only a warning, this evaluation treats any
   sorry as an incomplete proof, so the model does not receive credit.
   5:
   6: theorem hardmath_734R (I : R → R)
   7:   (hI : I = λ x =>     t in (-0.8)..(-0.1), (2.7*t^5 + 1.5*sin t - 1.1*cos t + 0.5) *



A.3    hardmath_162 System Refinement Case

   Recovery setting: hardmath_162                                                       Domain: Integral

   The first-pass M ATH C O P ILOT run on hardmath_162 produced a complete natural-language proof but
   did not produce a fully verified Lean file.


The isolated lemma is:
              Z 0.5
     I(x) =         (−0.9t2 )exϕ(t) dt,       ϕ(t) = 1.7t4 − 0.3t − 0.6 cos t − 2 arctan t + 2.6,
               −0.7

                                   (−0.9)(−0.7)2 exϕ(−0.7)
                          I(x) ∼                                    (x → +∞),
                                       x(−ϕ′ (−0.7))
with the numerical estimates
                                                      (−0.9)(−0.7)2
                |ϕ(−0.7) − 3.98| ≤ 0.001,                           + 0.10 ≤ 0.002.
                                                        −ϕ′ (−0.7)

Baseline attempts and failure mode. The prior FormalMATH runs in formalbench_project
contain six baseline Lean attempts for hardmath_162: Gemini, GPT-5.4, and Claude Opus,
each under FF and NL settings. All six fail the strict verifier with the same blocking category,
contains_sorry, at the top-level theorem. The generated target also exposes a deeper issue: the
benchmark’s rounded display
                                              0.10e3.98x
                                    I(x) ≈ −
                                                    x

                                                    22
Table 8: Baseline evidence for hardmath_162 from the prior FormalMATH experiment. “FF” and
“NL” denote the two baseline routes used in Section 4.
     Model family     Routes               Verifier result             Observed behavior
     Gemini           FF, NL               Both       fail       with One output diagnoses the shadowed-
                                           contains_sorry.            variable target as impossible; another
                                                                      gives an endpoint-Laplace derivation but
                                                                      does not formalize it.
     GPT-5.4          FF, NL               Both       fail       with One output rejects the rounded Tendsto
                                           contains_sorry.            target; another gives a mathematically
                                                                      plausible Laplace proof but leaves Lean
                                                                      as sorry.
     Claude Opus      FF, NL               Both       fail       with Outputs identify the scoping problem and
                                           contains_sorry.            the danger of treating rounded constants
                                                                      as exact asymptotic parameters; Lean re-
                                                                      mains a placeholder.



  Table 9: Proof-blueprint decomposition used to formalize the hardmath_162 endpoint lemma.
   Lean node                   Mathematical role                                           Status
   proof_step_1–3              Derivative formulae and endpoint separation showing         Pass
                               that the phase is maximized at the left endpoint.
   proof_step_4–7              Integration-by-parts reduction using the quotient           Pass
                               q(t) = f (t)/(−ϕ′ (t)).
   proof_step_8                Boundary and remainder estimates for the endpoint           Pass
                               Laplace expansion.
   proof_step_9                Assembly of the exact first-order asymptotic equiva-        Pass
                               lence.
   proof_step_10–12            Concrete interval estimates for ϕ(−0.7) and the lead-       Pass
                               ing coefficient.
   endpoint laplace            Final Lean-facing theorem matching the manuscript           Pass
   first order and main        statement.
   theorem


is autoformalized as a literal Tendsto statement toward the rounded expression. Several baseline
natural-language outputs correctly notice that this formal target is not a suitable theorem: the theorem
parameter x is shadowed by the limit variable, and the target neighborhood still depends on the outer
x. Other outputs identify the endpoint-Laplace method but still leave the proof as sorry. Thus, the
baselines either diagnose the statement-level problem or outline the right method, but do not produce
a strict certificate.
  Representative baseline Lean target: direct rounded Tendsto with placeholder

  theorem hardmath_162 (x : R) :
      Tendsto   R
        (λ x =>    t in (-0.7)..0.5,
          (-0.9 * t^2) *
            exp (-x * (-1.7 * t^4 + 0.3 * t + 0.6 * cos t
              + 2.0 * arctan t - 2.6)))
        atTop
        ((-0.10 * exp (3.98 * x) / x)) := by
    sorry



Natural-language proof process.       Let a = −0.7, b = 0.5, f (t) = −0.9t2 , and
                         ϕ(t) = 1.7t4 − 0.3t − 0.6 cos t − 2 arctan t + 2.6.
The proof uses the left-endpoint form of Laplace’s method, but the Lean development does not
assume the theorem as a black box. It formalizes the following argument directly.

 1. First, compute
                                                                         2
                                ϕ′ (t) = 6.8t3 − 0.3 + 0.6 sin t −
                                                                       1 + t2

                                                     23
    and show that ϕ′ (t) ≤ −3/4 on [a, b]. Hence ϕ is strictly decreasing on the interval, so its unique
    maximum occurs at a = −0.7. This also gives the quantitative separation
                                              3
                                 ϕ(t) ≤ ϕ(a) − (t − a),                 t ∈ [a, b].
                                              4

2. Define q(t) = f (t)/(−ϕ′ (t)). Since −ϕ′ (t) is bounded away from zero on [a, b], q is differen-
   tiable and q ′ is bounded by a concrete constant.
3. Rewrite the integrand by integration by parts:
                                                          q(t) d xϕ(t)
                                       f (t)exϕ(t) = −          e      .
                                                           x dt
    Therefore
                                                                        Z b
                                 q(a)exϕ(a)   q(b)exϕ(b)   1
                        I(x) =              −            +                    q ′ (t)exϕ(t) dt.
                                     x            x        x             a

4. The endpoint separation makes the right-endpoint boundary term exponentially smaller than
   exϕ(a) /x. The same separation bounds the integral remainder by O(exϕ(a) /x2 ). Dividing by
   q(a)exϕ(a) /x therefore gives a quotient tending to 1.
5. Finally, the numerical side conditions are verified by interval estimates: the proof bounds −ϕ′ (a),
   encloses arctan(0.7) by an alternating-series argument, and derives

                                                            f (a)
                        |ϕ(a) − 3.98| ≤ 0.001,                     + 0.10 ≤ 0.002.
                                                           −ϕ′ (a)

More explicitly, the integration-by-parts identity writes
                                                                                   Z b
                 Q(a)exϕ(a)   Q(b)exϕ(b)                                  1
          I(x) =            −            + R(x),                   R(x) =                 Q′ (t)exϕ(t) dt,
                     x            x                                       x           a

where Q(t) = f (t)/(−ϕ′ (t)). The proof establishes

                                             Q(b)exϕ(b) /x
                                                           →0
                                              exϕ(a) /x

because ϕ(b) < ϕ(a). It also proves the quantitative remainder estimate

                                                          exϕ(a)
                                             |R(x)| ≤ C
                                                            x2
for all sufficiently large x. This follows by combining a bound |Q′ (t)| ≤ M with
                                                            3
                                       exϕ(t) ≤ exϕ(a) e− 4 x(t−a)

and the elementary integral estimate
                                       Z b
                                                 3                4
                                              e− 4 x(t−a) dt ≤      .
                                         a                       3x
Consequently,
                                        Q(a)exϕ(a)
                                                       xϕ(a) 
                                                       e
                                 I(x) =            +o           ,
                                            x            x
which is exactly
                                              −0.9(−0.7)2 exϕ(−0.7)
                                  I(x) ∼                            .
                                               −ϕ′ (−0.7)     x


                                                     24
Table 10: Key information extracted from the system-side theorem-search output for the
hardmath_162 Laplace subproblem.
      Item                        Extracted content
                                                                          Rb
      Retrieved theorem           Endpoint Laplace method. If I(x) = a f (t)exϕ(t) dt, ϕ has a
                                  unique maximum at the left endpoint a, and ϕ′ (a) < 0, then
                                                          f (a)exϕ(a)
                                               I(x) ∼ −                   (x → +∞).
                                                             xϕ′ (a)
                                  The symmetric right-endpoint case uses f (b)exϕ(b) /(xϕ′ (b)) when
                                  ϕ′ (b) > 0.
      Problem instantiation       a = −0.7, b = 0.5, f (t) = −0.9t2 , and ϕ(t) = 1.7t4 − 0.3t −
                                  0.6 cos t − 2 arctan t + 2.6.
      Endpoint diagnostics        The search output reports ϕ(−0.7) ≈ 3.9807, ϕ(0.5) ≈ 1.1024,
                                  and ϕ′ (−0.7) ≈ −4.3612 < 0, selecting the left-endpoint formula.
      Resulting target            The expected leading term is
                                                       (−0.9)(−0.7)2 exϕ(−0.7)
                                                                               ,
                                                           x(−ϕ′ (−0.7))
                                  matching the isolated lemma in case/lemma.md.


Exact theorem versus rounded display. The strict Lean theorem deliberately avoids treating the
rounded expression as an exact asymptotic equivalent. Let
                                                         −0.9(−0.7)2
                               λ = ϕ(−0.7),         c=               .
                                                          −ϕ′ (−0.7)
The certified result is
                                                   eλx
                                            I(x) ∼ c   ,
                                                    x
together with the numerical enclosures |λ − 3.98| ≤ 0.001 and |c + 0.10| ≤ 0.002. This distinction
matters because replacing λ by 3.98 inside the exponential is not asymptotically harmless:
                                   ceλx /x         c
                                      3.98x
                                               =       e(λ−3.98)x .
                                −0.10e      /x   −0.10
Since the endpoint value is approximately 3.9807, the rounded display
                                                  0.10e3.98x
                                        I(x) ≈ −
                                                       x
should be read as a numerical presentation of the exact endpoint parameters, not as a ratio-limit
theorem with rounded constants. This is one of the places where the proof-blueprint workflow
improves the result: it separates the mathematically correct formal target from the informal rounded
answer.

Complete Lean endpoint block. The listing below prints the full endpoint portion of the final
certificate in tex/lean/Main.lean. The preceding part of the Lean file contains the definitions
of ϕ, f , I, q, and the earlier proof-blueprint lemmas; this endpoint block contains the complete
formalization of the Laplace remainder estimates, the numerical bounds, and the final theorem
interface used by the manuscript.

   Complete endpoint Lean certificate: tex/lean/Main.lean, lines 500–1008

   Lean listing unavailable. The appendix expects the file at tex/lean/Main.lean; compile
   either from the project root or from the tex/ directory so that the listing path can be resolved.

This case explains why a strict first-pass failure should not always be interpreted as absence of
mathematical understanding, while also showing why natural-language insight alone is insufficient.


                                                  25
The baseline attempts either identify the right endpoint-Laplace route or diagnose the rounded target
as unsuitable, but their Lean certificates remain placeholders. The refined proof-blueprint workflow
converts the informal endpoint-Laplace appeal into explicit Lean obligations: monotonicity of the
phase, boundedness of the quotient derivative, exponential domination of the non-dominant endpoint,
an O(exϕ(a) /x2 ) remainder bound, and machine-checkable interval arithmetic for the constants.
Thus, the remaining gap in hardmath_162 is precisely the gap that M ATH C O P ILOT is designed to
close: turning a mathematically plausible derivation into a verified, semantically precise theorem.

A.4     Real PDE Cases

The PDE examples are designed to be qualitatively different from benchmark-style exercises. They
come from the analysis of DG methods for transport-dominated equations, where the mathematical
content is not a short symbolic manipulation but a combination of stability, projection, and mesh-
scaling arguments. They require numerical-analysis concepts not fully developed in Mathlib, so
successful Lean files verify the formal assembly under explicit assumptions rather than a from-first-
principles formalization of DG methods or Sobolev theory.

A.4.1    PDE Case 1: Upwind DG L2 Error Estimate
For the linear advection equation ut +aux = 0 on (0, 1) with a > 0 and periodic boundary conditions,
the semi-discrete upwind DG scheme seeks uh (t) ∈ UhK such that
                                  Bj (uh , φh ) = 0      ∀φh ∈ UhK .
The target theorem is the estimate
                               ∥u(·, T ) − uh (·, T )∥L2 (0,1) ≤ ChK+1 .
This is a representative smooth-solution estimate for a scalar hyperbolic problem: the upwind
numerical flux captures the one-way propagation direction, and the L2 argument measures how
stability and local polynomial approximation combine over time [Johnson and Pitkäranta, 1986,
Cockburn and Shu, 2001, Zhang and Shu, 2004]. The correct proof uses the Gauss–Radau projection
Πh u and splits
                            u − uh = (u − Πh u) + (Πh u − uh ) = η + ξ.
The essential admissibility point is that ξ = Πh u − uh ∈ UhK , so ξ may be used as a DG test function,
whereas the full error e = u − uh generally cannot. Summing the cellwise energy identity yields
                                                                  Z 1
                          1 d                 aX 2
                               ∥ξ∥2L2 (0,1) +      [[ξ]]j+1/2 = −     ηt ξ dx,
                          2 dt                2 j                   0

after the Gauss–Radau endpoint and moment conditions remove the other projection-error terms.
Cauchy–Schwarz, Young’s inequality, Gronwall’s inequality, the projected initial data ξ(·, 0) = 0,
and the projection estimate for η give the final O(hK+1 ) bound.

Planted wrong proof. The flawed proof first enlarges Galerkin orthogonality from discrete test
functions to “all test functions,” then chooses φ = e = u − uh . This is invalid because u is not
generally a piecewise polynomial, so e ∈  / UhK . The wrong proof also claims that interface terms
cancel, whereas the upwind flux produces a nonnegative jump term.

A.4.2    PDE Case 2: Gauss–Radau Reference-Cell Estimate
Let Iˆ = (0, 1) and let Π̂ : H k+1 (I)
                                    ˆ → Pk (I)
                                            ˆ be the Gauss–Radau projection defined by moment
orthogonality against Pk−1 and endpoint matching at 1. Such one-sided projections are standard
in DG analyses because the endpoint condition interacts cleanly with upwind traces at cell inter-
faces [Cockburn and Shu, 2001, Zhang and Shu, 2004]. The target reference-cell and physical-cell
estimates are
           ∥Π̂ŵ − ŵ∥L2 (I)
                          ˆ ≤ C|ŵ|H k+1 (I)
                                          ˆ ,       ∥P w − w∥L2 (Ii ) ≤ Chk+1
                                                                          i   |w|H k+1 (Ii ) .
                                                                     ˆ with ∥z∥L2 ≤ 1, define
The correct proof can be organized through duality. For each z ∈ L2 (I)
                                            Z 1
                                  Fz (ŵ) =     (Π̂ŵ − ŵ)z dx̂.
                                                0


                                                    26
Table 11: Complete PDE attempt-level status table. “Assembly” means the Lean file verifies
relative to explicit analytic assumptions or opaque/axiom declarations; it is not an end-to-end PDE
formalization.
 Route                 Model              DG estimate          Gauss–Radau estimate   Main status category
 GPT-Formalized        Gemini 3.1 Pro     Fail                 Fail                   Syntax/formalization incompat-
                                                                                      ibility.
 GPT-Formalized        GPT-5.4            Fail                 Fail                   Syntax/formalization incompat-
                                                                                      ibility.
 GPT-Formalized        Claude Opus 4.7    Assembly             Assembly               Repairs the formalization.
 GPT-Formalized        Claude Sonnet 4    Fail                 Fail                   Syntax/formalization incompat-
                                                                                      ibility.
 Opus-Formalized       Gemini 3.1 Pro     Assembly             Assembly               –
 Opus-Formalized       GPT-5.4            Assembly             Assembly               –
 Opus-Formalized       Claude Opus 4.7    Assembly             Assembly               –
 Direct                Gemini 3.1 Pro     Fail                 Fail                   Logic/tactic-level failure.
 Direct                GPT-5.4            Assembly             Assembly               –
 Direct                Claude Opus 4.7    Assembly             Assembly               –



                   Table 12: Qualitative summary of representative PDE proof outputs.
   Route             Statement formal- Representative behavior                                           Result
                     izer
   GPT-              GPT-5.4           Gemini and Sonnet fail on both PDE theorems because                   2/8
   Formalized                          they preserve the Lean-version-incompatible formaliza-
                                       tion; Opus repairs the formalization and produces assem-
                                       bly certificates.
   Opus-             Claude Opus 4.7 The formalization uses opaque/axiom boundaries for DG                   6/6
   Formalized                          stability, projection estimates, Bramble–Hilbert, and scal-
                                       ing; all tested downstream completions produce assembly
                                       certificates.
   Direct            Model-generated GPT-5.4 and Opus produce assembly certificates for both                 4/6
                     proof and formal- PDE theorems; Gemini gives mathematically plausible but
                     ization           Lean-invalid proofs.



Each Fz is a bounded linear functional that vanishes on Pk , so Bramble–Hilbert gives

                                          |Fz (ŵ)| ≤ C|ŵ|H k+1 (I)
                                                                  ˆ .


The dual characterization of the L2 norm gives the reference estimate, and the affine scaling x =
xi−1/2 + hi x̂ gives the physical-cell estimate.

Planted wrong proof.           The flawed proof instead defines

                                          F (ŵ) = ∥Π̂ŵ − ŵ∥L2 (I)
                                                                  ˆ


and calls it a bounded linear functional. This is false: it is a norm of a linear error operator, hence
nonlinear. A valid repair must use either the dual family Fz , an operator-valued Bramble–Hilbert
argument for I − Π̂, or a seminorm version of Bramble–Hilbert.

A.5      Representative PDE Proof-Synthesis Outputs

The selected PDE model outputs reveal three recurring patterns. First, GPT-Formalized failures are
mostly formalization failures: the GPT-produced formalization uses declaration forms and abstraction
boundaries that are incompatible with the tested Lean 4.29 setup, and most models do not repair them.
Second, the Opus-Formalized route succeeds because the Opus-produced formalization expresses
the missing analytic theory with modern opaque declarations or explicit axioms, leaving Lean to
verify the algebraic assembly step. Third, the Direct route shows that direct natural-language-to-Lean
generation can work when the model chooses a suitable abstraction boundary. Table 11 lists all 20
PDE attempts; Table 12 summarizes these proof-synthesis patterns by route.


                                                        27
                    Table 13: Wrong-proof detection details for the two PDE cases.
   Model                 Case                 Detected issue
   Gemini 3.1 Pro        DG estimate          Rejects the proof and identifies the illegal choice φ = e =
                                              u − uh ; also observes that the interface algebra should
                                              produce a jump term. It does not separately emphasize
                                              the earlier quantifier enlargement as strongly as GPT-5.4.
   GPT-5.4               DG estimate          Rejects the proof, explicitly states that the error equation
                                              holds only for φh ∈ UhK , and explains why the full error
                                              e is not an admissible test function.
   Gemini 3.1 Pro        Gauss–Radau          Rejects the proof because F (ŵ) = ∥Π̂ŵ − ŵ∥L2 is
                                              not linear; proposes using an operator-valued Bramble–
                                              Hilbert argument.
   GPT-5.4               Gauss–Radau          Rejects the proof, explains the failed linearity claim,
                                              and gives two repairs: a seminorm version of Bramble–
                                              Hilbert or the linear operator I − Π̂.


A.6   Wrong-Proof Diagnostic Details

Table 13 records the diagnostic behavior behind Table 6. The models are not credited for producing
a Lean proof here; the task is to reject the flawed natural-language argument and explain the
mathematical error.




                                                 28
