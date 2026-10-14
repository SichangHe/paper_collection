                                                  A HUMAN-AI COLLABORATIVE WORKFLOW FOR
                                                  MATHEMATICAL DISCOVERY: A CASE STUDY IN
                                                 GROVER-COMPATIBLE RIEMANNIAN OPTIMIZATION
                                                CHENYI LI∗ , ZHIJIAN LAI∗ , DONG AN∗ , JIANG HU† , AND ZAIWEN WEN∗

                                              Abstract. We investigate how large language models can be used as research tools in scien-
                                         tific computing while preserving mathematical rigor. We propose a human-in-the-loop workflow for
                                         interactive theorem proving and discovery with LLMs. Human experts retain control over problem
                                         formulation and assumptions, while the model searches for proofs or contradictions, proposes can-
                                         didate properties and theorems, and helps construct structures and parameters that satisfy explicit
arXiv:2512.09443v3 [cs.HC] 21 Sep 2026




                                         constraints, supported by numerical experiments and simple verification checks. Experts treat these
                                         outputs as raw material, further refine them, and organize the results into precise statements and
                                         rigorous proofs. We instantiate this workflow in a main case study on the connection between man-
                                         ifold optimization and Grover’s quantum search algorithm, where the pipeline identifies invariant
                                         subspaces and explores Grover-compatible retractions. The √ main case study uses the corresponding
                                         Grover-compatible convergence analysis, including an O( N log(1/ε)) PL-based bound established
                                         in the companion mathematical work, to illustrate the refinement stage of the workflow. Prompt
                                         records and reusable templates for implementing the workflow are provided. We further include a
                                         multi-oracle case study, document representative failed and corrected routes arising from this setting,
                                         and provide a structured failure-mode analysis.

                                             Key words. LLM, theorem proving, Grover’s algorithm, Riemannian optimization

                                             MSC codes. 81P68, 90C26, 68V15, 68T50


                                              1. Introduction. Recent advances in artificial intelligence, especially large lan-
                                         guage models, show strong capabilities in analyzing long text [49], consolidating do-
                                         main knowledge [22], and supporting literature-grounded querying through retrieval-
                                         augmented pipelines [23]. They also achieve steady gains in stepwise mathematical
                                         reasoning [24, 45]. At the same time, mathematical research remains a demanding
                                         enterprise that requires sustained abstraction, coherence over long arguments, and
                                         verifiable correctness [39, 38]. In practice, the process is conducted by human experts
                                         and often iterative. Human experts pose questions, build candidate structures, test
                                         them on examples or with tools, and keep what survives as statements with reusable
                                         arguments [21, 32]. Motivated by these developments, we study how LLMs can sup-
                                         port nontrivial mathematical research while keeping human expertise central. We
                                         discuss several examples of human-AI interaction in mathematical theorem proving
                                         and theorem discovery. Model outputs are tested by calculations or numerical exper-
                                         iments. Failed routes are rejected, and repaired and verified ideas are promoted to
                                         theorem statements and proofs.
                                              A growing body of literature utilizes machine learning to assist mathematical re-
                                         search and to tackle difficult problems across algebra, geometry, and related areas. In
                                         algebra, collaborations between mathematicians and AI reveal useful relations in rep-
                                         resentation theory and guide the formulation and proof of new results [8]. Recent stud-
                                         ies use data-driven methods to rediscover classical algebraic inequalities [10]. In alge-
                                         braic combinatorics, curated datasets focus on the conjecturing process and support
                                         machine-assisted exploration of patterns that lead to precise and testable statements
                                           ∗ Beijing International Center for Mathematical Research, Peking University, Beijing, 100871,

                                         People’s Republic of China (lichenyi@stu.pku.edu.cn, lai zhijian@pku.edu.cn, dongan@pku.edu.cn,
                                         wenzw@pku.edu.cn).
                                           † Yau Mathematical Sciences Center, Tsinghua University, Beijing, 100190, People’s Republic of

                                         China (jianghu@tsinghua.edu.cn).

                                                                                           1
2                       C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


[6]. In geometry, AI systems have produced human-readable proofs for challenging
Euclidean problems and strong performance on Olympiad-style benchmarks by com-
bining search, deduction, and verification [40, 7]. Data-driven analyses of Calabi-Yau
spaces reveal structural regularities in algebraic geometry and motivate conjectures
that can be vetted by experts [14]. Beyond individual domains, Ramanujan Machine
procedures generate candidate identities for fundamental constants and invite human
checks and proof [33]. Symbolic regression and equation discovery pipelines recover
concise laws from data and suggest invariants and lemmas for further study [42, 4].
Most recently, OpenAI reported ten advances on long-standing problems in mathe-
matics and theoretical computer science through an AI–human workflow in which an
AI model generated candidate arguments and humans helped prepare them as math-
ematical manuscripts [30]. These works promote automatic workflows for theorem
discovery and proving, in which models propose, rank, and test candidate statements,
while human researchers shape definitions, control scope, and turn promising leads
into theorems.
      A separate line of research targets solutions to mathematical competitions, espe-
cially IMO problems. Specialized domain models such as DeepSeekMath-V2 achieve
gold-medal performance on IMO tasks via purely natural-language proofs with sub-
stantial test-time computation and dedicated self-verification [35]. In parallel, fron-
tier general-purpose reasoning models from Google reach comparable scores on IMO
2025 style problems. Building on these backbones, Huang and Yang design a model-
agnostic verification and refinement pipeline that attains gold-medal performance at
IMO 2025 by systematically generating, checking, and refining candidate solutions
[16]. Complementing this natural-language line, DeepMind’s AlphaProof system com-
bines reinforcement learning with formal proof search in Lean and achieves silver-
medal performance on IMO 2024 problems under fully formal verification [18]. These
advances suggest that natural language and formal pipelines can both approach top
human performance on Olympiad benchmarks. Formal verification provides a dif-
ferent reliability standard. Lean, Coq, and Isabelle encode definitions and proofs in
machine-checkable languages [9, 1, 29], and recent LLM integrations improve proof-
script search [47, 31, 34].
      Beyond theorem proving, many recent efforts use AI to assist scientific research,
with most systems targeting applied areas such as biomedicine [15], the natural sci-
ences [48], and machine learning [25]. Deep research systems [17, 46] go further by
producing end-to-end reports and maintaining plans over long horizons, while sus-
tained human supervision remains important for strong conclusions. A parallel line
builds agentic systems for automating parts of the research workflow, ranging from
specific agents to AI scientist frameworks and research copilots, showing feasibility in
structured settings [28, 12]. Automated survey methods can review the relevant back-
ground literature [44, 26]. For methodology implementation, recent systems pursue
automated code generation for research, including project-level context refinement
with compiler feedback [2]. In parallel, automated academic-writing tools target ref-
erence handling, citation integrity, and drafting support [36, 11]. Finally, automated
review systems focus on argumentation quality and fairness, while mathematical rigor
still requires expert verification [27, 43, 19].
      These observations motivate our interactive workflow, which inserts human over-
sight at intermediate stages and uses computationally reproducible checks and explicit
proof obligations to support the conclusions. We document how this workflow con-
verts model interactions into candidate definitions, lemmas, proof drafts, and failure
records that experts can check across three case-study threads. Our human-AI work-
               HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                                  3




      Fig. 1. Human-AI interactive theorem proving pipeline. Model proposals, human checks, and
distilled theorem statements are organized across the three workflow stages.


flow centers on three modes of human–AI interaction, namely conceptualizing research
topics, theorem proving for fixed targets, and theorem discovery while the conclusion
remains open. As the main case study, we study Grover’s quantum search algorithm
through Riemannian optimization. We explicitly present the prompts that instantiate
the workflow in this setting. The human-AI interactive proving pipeline is shown in
Figure 1. Our main contributions are listed as follows.
      1. Topic conceptualization with AI. We design an AI-assisted routine for
         early stage problem formulation. Starting from preliminary human ideas
         about research topics, the LLM proposes candidate objects, assumptions,
         and questions with brief notes on novelty and feasibility. Researchers, guided
         by both their own expertise and the model’s feedback, test these candidates
         on minimal examples. The surviving ideas are turned into precise statements
         and an initial paper outline.
      2. Goal-guided proving. For clearly specified proof targets, researchers com-
         municate their preliminary proof ideas and directions to the model via care-
         fully designed prompts. The LLM suggests reductions, proof sketches, and
         possible counterexamples along these directions. After human checks, we ex-
         tract clear theorem statements, proofs, and auxiliary lemmas, and consolidate
         them into rigorous, human-readable theorems.
      3. Open-ended theorem discovery. When target conclusions remain open,
         we use the LLM to propose candidate statements with lightweight evidence,
         such as numerical experiments and mathematical reasoning. Human experts
         filter and refine these candidates into theorem templates and reusable proof
         schemas for related problems. When suitable constructions are unknown, a
         loop of property-constrained generation and testing searches for simple can-
         didates that satisfy the desired conditions and admit clean proofs.
      4. Documented case studies in mathematical optimization. We use two
         related Grover-compatible threads and a third composite convex-optimization
         case to record how the workflow operated on concrete proving and discovery
4                       C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


         tasks. The model proposes proof routes, structural observations, or candidate
         updates. The human experts test these suggestions by calculation, compati-
         bility with the surrounding theory, and proof reconstruction.
    Table 1 gives statement-level provenance for the mathematical results used in the
case-study sections. Results marked as reproduced or adapted originate in the com-
panion Grover-compatible optimization article [20] and are included here as math-
ematical material for documenting the corresponding human–AI research process.
Statements marked as new to this manuscript are introduced in the present work-
flow exposition. The workflow’s generalizability beyond the documented case studies
remains untested.
    We organize this paper according to different modes of AI-assisted mathematical
practice. We briefly review elements of mathematical research in Section 2. Topic
conceptualization with AI support is discussed in Section 3. We present AI-assisted
theorem proving for fixed targets and document the associated records that human
experts can check in Section 4. AI-assisted theorem discovery, including proposal,
numerical test, and proof, together with transfer to similar settings, is explored in
Section 5. We clarify the respective roles of human experts and AI systems in Section
6. Finally, the paper is concluded with Section 7. Appendix A supplements the main
case study with a related multi-oracle case, representative failed and corrected routes,
and the Grover-compatible prompt records. Appendix B contains another separate
composite-optimization case study.
     2. Preliminaries for mathematical research. In practice, mathematicians
often view research as passing through five connected phases, namely topic conceptu-
alization, conjecturing, validation, proof development, and writing. Each phase has
its own goals, typical outputs, and methods. We briefly review the role of each phase
and indicate how new advances can be categorized.
     We use the following notation consistently in the case study. The unitary group is
denoted by U(N ). A ket |ψk ⟩ denotes a unit vector, whereas ψk := |ψk ⟩⟨ψk | denotes
the associated rank-one projector. Success probabilities are written as qk = Tr(Hψk ),
equivalently qk = ⟨ψk |H|ψk ⟩ when the ket notation is used explicitly. Gradients are
Riemannian gradients on U(N ) unless the text explicitly refers to the skew-Hermitian
representative of the gradient.
     Topic conceptualization. The first task is topic conceptualization. Good topics
balance depth, tractability, and potential for broader impact [38]. The conceptualiza-
tion process specifies the scope, modeling decisions, and targets for correctness and
clarity. Researchers begin by specifying the object, the assumptions, and the claim.
The object identifies the mathematical structure under study, such as a class of func-
tions, graphs, or manifolds. The assumptions collect the standing hypotheses, for
example, the regularity conditions, dimensional regimes, or model constraints. The
claim formulates the intended conclusion in precise terms, such as an error bound, a
convergence rate, or a stability guarantee. In practice, this stage includes surveying
prior work, reviewing both methods and known limitations, and choosing the working
setting, such as toy models for quick feedback or general frameworks for the final
theorem.
     Conjecturing. Once the main topic is relatively fixed, human experts study
the related literature and learn the relevant concepts. They ask what existing results
already cover, where the assumptions are too strong, which regimes or examples
are missing, and how known methods might be modified. They also look for ideas
from neighboring areas that could be imported into the current setting. From this
              HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                             5

perspective, conjectures often come from extending an existing theorem to a new
regime, weakening assumptions while trying to keep the same type of conclusion, or
combining mechanisms that have been used separately [32]. AI can generate many
candidate conjectures and variations, especially when broad background knowledge
or cross-domain analogies are useful. The central difficulty is to select candidates
that are mathematically important, feasible, and worth developing. This selection
still depends on expert judgment.
      Innovation types in conjecturing. We now distinguish several common inno-
vation routes at the conjecturing stage and, for each route, explain how conjectures
arise and provide representative examples.
       1. Fix bug. Make existing methods verifiable or stable under realistic assump-
          tions. Typical examples include robustness to nonsmooth terms and con-
          vergence proofs under perturbations, such as proximal steps and operator
          splitting for nonsmooth objectives.
       2. Weaken assumptions. Replace strong regularity or noise free models with
          weaker, more realistic conditions while preserving guarantees. For instance,
          establish convergence or rates under weak convexity, stochastic perturbations,
          or inexact oracles.
       3. Combination fusion. Merge complementary mechanisms to improve per-
          formance. For example, combine acceleration with variance reduction to ob-
          tain provable improvements over either component alone.
       4. Cross domain lifts. Recast the problem in a different domain, then use the
          new viewpoint to propose related questions. Typical cases include passing
          from the discrete to the continuous setting, and from a Euclidean setting to
          a manifold one. A standard example outside the present case study is to
          model an accelerated optimization method by a continuous-time ODE, and
          then use Lyapunov or energy functions from ODE stability theory to prove
          convergence properties of the corresponding discrete method.
       5. Unifying viewpoints. Place several related methods in a single frame-
          work to explain their similarities and differences. For example, viewing first-
          order methods through a parameterized ODE can unify different acceleration
          schemes, which can then be analyzed within a Lyapunov framework.
       6. Boundary and negative results. Identify the limits of what is achiev-
          able under a given set of assumptions. Common goals include proving lower
          bounds and constructing sharp counterexamples that expose boundary cases.
      Validation. Before investing effort in proofs, human experts test candidate con-
jectures in straightforward ways. They may compare them with known results and
basic intuition, and examine their behavior on both simple examples and complicated
cases. Feedback from these checks is then used to revise the statement, adjust the
assumptions, and decide which directions are worth pursuing.
      In practice, human experts combine careful manual calculations with small nu-
merical experiments. Examples that cover boundary cases and important special
situations may also be explored. These checks can be implemented with lightweight
tools such as Python with the NumPy and SciPy libraries, or MATLAB, depending
on the surrounding code base. In the present work, they serve as diagnostic evidence
that guides proof attempts. Among the five phases, validation is one of the most dif-
ficult to delegate to AI. A model can propose tests, generate executable calculations,
or point to apparent patterns, but human experts must execute and assess the checks,
determine whether hidden assumptions remain, and decide whether the statement is
ready for proof. It is often helpful to keep a record of each conjecture, which contains
6                       C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


the tests it has passed or failed, and the exact assumptions under which it seems
to hold. The goal is to discard weak ideas early, focus on a clear formulation, and
identify proof directions.
     Proof development. When the statement is stable, human experts try to figure
out a proof plan. Several basic proof approaches are useful in many parts of mathe-
matics. First, human experts use plain step-by-step reasoning. They write down the
definitions, expand them carefully, and follow the logical implications until the claim
is reached. Second, they adapt standard methods from previous work or neighboring
areas. Typical transfers take techniques developed in other domains and apply them
in the current setting. Decomposing the current problem into simpler subproblems
can reveal structures that also appear in related work. Third, they look for innova-
tive structure or ideas that can guide the proof. This may involve defining a quantity
with carefully chosen properties. At this stage, new proof techniques may also be
developed to handle more sophisticated problems.
     Writing. In the final stage, human experts organize the statements, standardize
the notation, and polish the proofs. Results are arranged into a coherent hierarchy
of definitions, lemmas, and theorems, and symbols are introduced explicitly and used
consistently. Proofs are streamlined where possible, with the main idea stated before
technical details. The final writeup gathers the work from conjecturing, testing, and
proving into a presentation that is clear, checkable, and easy to build on. In the case
study, the writing-phase outputs are the human-curated theorem hierarchy, standard-
ized notation, polished proofs, and final manuscript. The main case-study analysis
centers on AI-assisted theorem proving and theorem discovery.
    3. Conceptualizing research topics with AI.
     3.1. Early stage exploration with domain sketches and candidate ques-
tions. Early exploration moves from broad themes to specific mathematical targets.
We begin by using AI to map the structure of the domain. This includes identifying
the main objects under study, including core algorithms, key operators, and typi-
cal function classes. We also identify the assumptions that usually govern behavior,
namely properties of functions, or curvature conditions, and the standard objectives
like rates, bounds, stability, and existence results. By aligning terminology across
different areas and highlighting analogies, AI helps construct a coherent picture of
the field and locate promising candidate problems. A typical example is transferring
properties established in Euclidean space to their counterparts on manifolds.
     With this guidance, we encourage AI to propose concrete research questions along
principled axes of variation. These include weakening or strengthening hypotheses,
transferring known results to new regimes, seeking converses, or isolating thresholds.
Each proposal is paired with a precise claim sketch with minimal hypotheses, the
nearest classical results with their gaps, and a plausible method class. To avoid
vacuous or ill-posed targets, we run quick feasibility checks. AI is asked to generate
instances, and to perform scaling and invariance sanity checks. These steps reveal
hidden necessary conditions or point to underlying patterns. Proposals that survive
are ranked by novelty and tractability, with preference given to those promising a
unifying principle. The output of this stage is a compact domain sketch and a curated
set of viable questions ready to be sharpened.
     Example. Building on the perspective of [37], which analyzes classical quan-
tum algorithms through imaginary time evolution, we begin with an initial idea of
combining quantum algorithms with manifold optimization. We phrase this idea as
a concrete prompt, given in Appendix A.3.1. The model returns a concise conclusion
             HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                            7

that lists candidate directions and prerequisite concepts on both sides, such as al-
gorithmic primitives, target objectives, and possible correspondences between them,
together with preliminary feasibility explanations. We treat this response as a rough
map. It guides our literature reading and internal discussion, and helps us prune
ideas that are ill-posed or unlikely to admit clean analysis. After several rounds of
interaction with language models, our main idea converges on two anchors, Grover’s
search and Riemannian gradient methods.
     3.2. Concrete idea phase for sharpened claims and validation planning.
Once the topic and basic directions are in place, the next step is to turn promising
ideas into precise and checkable statements. Human experts usually begin by fixing
notation and writing down assumptions as explicit structural properties of the objects
under study. This separates the object of analysis from background motivation. At
the same time, AI can be asked to propose decompositions, identify plausible proof
routes, and point out where known techniques are likely to apply. The goal is to
expose the core difficulty of the problem and to identify a small number of central
conjectures and theorems that capture it.
     With candidate statements in hand, we organize the reasoning into a hierarchy
of proof tasks. This hierarchy includes main theorems, key reductions, comparison
steps, and delicate lemmas where constants, parameter ranges, or limiting regimes
matter most. For each task, AI can list possible proof strategies and propose simple
numerical tests. These tests help diagnose which parts are routine and which are
genuine bottlenecks. On this basis, we design a validation plan that separates target
claims from structurally suggested conjectures.
     Finally, we start to shape the final paper around this structure. Definitions and
notation are organized in the form most convenient for the subsequent arguments.
Intermediate claims are grouped into coherent subsections. Prospective figures and
tables are tied directly to specific arguments or comparisons. By the end of this
phase, a vague direction has been converted into a disciplined roadmap with clear
scope, proof avenues, and validation checks.
     Example. Continuing the example from the previous subsection, suppose we
have fixed the topic at the intersection of Riemannian optimization and Grover’s
algorithm. The guiding theme is to interpret Grover’s procedure from a manifold
optimization viewpoint. With this topic in place, we ask the model for a theoretical
framing. It produces a structured note that lists the relevant objects on both sides.
These include the manifold of quantum states and the standard Riemannian gradient
updates. It also recalls the basic properties of Grover iterations, namely their symme-
try and complexity guarantees. It suggests natural submanifolds on which to restrict
the dynamics and identifies candidate correspondences between gradient dynamics
and Grover iterations. The prompts used in this example are given in Appendix
A.3.2.
     We then request a more explicit manifold-optimization treatment. The model
proposes viewing the state evolution as gradient-type updates on a suitable manifold of
quantum states and outlines checks that distinguish genuine geometric structure from
artifacts of a particular parameterization. It suggests candidate statements that aim
to recover the classical complexity of Grover’s algorithm within this manifold-gradient
framework. Human authors then refine these suggestions into precise assumptions,
theorem statements, and a short list of claims that still need proof.
    4. AI-assisted theorem proving. This section considers three fixed-target
proving scenarios. Human experts specify the goals, choose and verify proof routes,
8                          C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


and integrate accepted arguments, while the model proposes local lemmas, alternative
approaches, and computational checks. Several substantive Grover-compatible math-
ematical results used in the following case-study sections, including the retraction,
invariant-structure results, and convergence analysis, originate in or are adapted from
the companion mathematical article [20]. Their role here is to provide mathematical
material for documenting the corresponding human–AI research process.

    Table 1. Statement-level provenance. Reproduced: the same statement appears in [20].
    Adapted: based on material in [20] but reorganized, combined for the present exposition.
                 New: introduced here, with the label indicating provenance.
    Statement              Status        Provenance and role
    Theorem 4.1            Reproduced    The corresponding global-optimality statement and gradi-
                                         ent characterization appear as Theorem 2 in [20]. Notation
                                         is harmonized here.
    Proposition 1          New to this   This commutator characterization is introduced as a prove-
                           manuscript    or-disprove example. It is a standard matrix/Lie-algebra
                                         fact and is not claimed as a new mathematical research
                                         contribution.
    Theorem 4.2            Adapted       Based on the classical-simulability result, Theorem 13 in
                                         [20], and reorganized around the scalar process (xk , yk , qk ).
    Proposition 2          Adapted       The exact exponential-step statement combines the
                                         commutator-norm identity and invariant two-dimensional
                                         dynamics in [20] with the one-step formulation used here.
    Theorem 5.1            Reproduced    The invariant-2D-subspace and gradient-subspace state-
                                         ments appear as Theorem 6 in [20].
    Theorem 5.2            Reproduced    The 5-factor Grover-compatible retraction and its parame-
                                         terization appear in Proposition 10 of [20].
    Theorem 5.3            Reproduced    The baseline smoothness-based Riemannian-gradient com-
                                         plexity statement appears as Theorem 17 in [20].
    Theorem 5.4            Reproduced    The tight first- and second-order bounds and constants ap-
                                         pear as Lemma 15 in [20].
    Theorem 5.5            Adapted       The PL-based complexity statement is based on Proposi-
                                         tion 18 and Theorem 19 in [20].



     4.1. Direct proofs when the statements are trusted. The easiest case be-
gins with a statement human experts believe to be correct and a concrete proof plan.
The simplest way to use an AI prover in this setting is to ask it directly for a proof
of the target statement, then query the model for standard reductions and a stepwise
derivation. Because the model may skip justifications, misapply lemmas, or mishandle
quantifiers and constants, human experts use targeted prompts. For example, they
explicitly state assumptions and variable domains, require line-by-line reasoning, and
ask for citations, adversarial checks, and quick numerical spot tests. Human experts
then verify every claim produced by the AI, checking edge cases and reproducing key
calculations.
     This setup typically arises when human experts already have a deep understand-
ing of what needs to be proved and only some local details remain to be filled in.
After reviewing the draft, they identify gaps, remove redundancy, and reorganize the
argument so that the key steps are transparent. In this setting, AI is useful primarily
as a generator of local proof variants and checks. Human experts provide validation,
judgment, and final integration into a clear and fully rigorous proof.
     Example. We illustrate our human-AI workflow with the following claim, which
ties stationarity to global optimality on the unitary manifold. Let H = H † = H 2 be
an orthogonal projector on a Hilbert space. U ∈ U(N ) denotes the quantum circuit
we want to design. Our cost function is f (U ) = Tr(HU ψ0 U † ), where |ψ0 ⟩ is the
initial state. Intuitively, the skew-Hermitian component of the Riemannian gradient
gradf
 g (U ) = [H, ψU ] shows that stationarity is equivalent to the output state ψU
              HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                             9

commuting with H. In this case ψU is an eigenstate of H, and since the spectrum of
H is {0, 1}, the expectation f (U ) = Tr(HψU ) is forced to take an extremal value 0
or 1. This intuition gives the following theorem on global optimality.
    Theorem 4.1 (Global optimality). Let f (U ) = Tr(HU ψ0 U † ) on the unitary
group U(N ), and write ψU := U ψ0 U † for the output state of the circuit U . The
skew-Hermitian part of the Riemannian gradient of f on U(N ) is

                                 gradf
                                  g (U ) = [H, ψU ].

Moreover, gradf
             g (U ) = 0 if and only if U is a global optimizer of f over U(N ). In
that case f (U ) ∈ {0, 1}, corresponding respectively to the global minimum 0 and global
maximum 1.
    To turn the intuition into a rigorous argument, we use a structured prompt that
asks the model to restate assumptions, notation, and domains, give a stepwise deriva-
tion, and justify nontrivial inferences. Reference verification is a key methodological
safeguard: the model may invoke standard named results by their usual names, while
human experts verify any bibliographic support before it enters the proof. Human
experts also verify the derivation line by line, reproduce key calculations, check bound-
ary cases, determine citation status, and streamline the final proof. The prompts used
in this example are listed in Appendix A.3.3.
    For Theorem 4.1, one concrete adversarial check uses the two-dimensional pro-
jector H = diag(1, 0). For the pure states ψ = e1 e†1 and ψ = e2 e†2 , one has [H, ψ] = 0
and Tr(Hψ) = 1 or 0, respectively, so the stationary cases    √ are exactly extremal in
this test. For the nonextremal pure state v = (e1 + e2 )/ 2 and ψ = vv † , one has
Tr(Hψ) = 1/2 and [H, ψ] ̸= 0. This confirms that the stationary classification selects
the two extremal states in this test.
     4.2. Clear target, uncertain truth. In many cases, the truth of a proposed
theorem remains uncertain, so we adopt a systematic prove-or-disprove protocol. We
delegate to AI along two coordinated branches. One explores plausible avenues toward
a proof, and the other actively searches for failure. Both outcomes are informative.
A successful argument consolidates the scope of the claim, while a counterexample
clarifies its limits and may suggest a sharper statement.
     On the proof side, the AI proposes feasible directions, candidate lemmas, de-
composition strategies, and intermediate claims, around which the human expert
can organize a coherent argument. On the disproof side, the AI generates tentative
constructions, stress tests, and diagnostic patterns that focus the search for coun-
terexamples on promising regions of the space. By jointly assessing the evidence
produced by both branches, the human expert avoids one-sided reasoning and moves
more systematically from an initial conjecture to a stable, well-justified conclusion.
     Example. We illustrate the prove or disprove workflow on a basic structural
question from matrix theory related to the retraction on the Riemannian manifold.
Consider the following proposition about commutators of Hermitian matrices and the
Lie algebra su(n). It is straightforward to check that any commutator [A, B] with
A† = A and B † = B is skew-Hermitian. The converse direction is less obvious. Every
skew-Hermitian matrix with zero trace must be represented in this way. This makes
the statement a natural candidate for a two branch search. The proof branch looks
for a constructive representation of arbitrary elements of su(n) as commutators, while
the disproof branch asks the model to search for counterexamples or obstructions.
10                      C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


     Proposition 1. The set of commutators of Hermitian matrices

                           C = {[A, B] : A† = A, B † = B}

equals {X ∈ Mn (C) : X † = −X, tr X = 0} = su(n).
    To analyze this proposition, we use a prove-or-disprove prompt with two branches.
The proof branch asks for a construction of arbitrary elements of su(n) as commutators
[A, B]. The disproof branch searches for obstructions, counterexamples, and invariant-
based failures. Each branch must give explicit reasoning and use only standard results.
The output is a verdict together with adversarial checks that human experts inspect
before accepting the conclusion. Concrete prompts are given in Appendix A.3.4.
     4.3. Rich proofs and the “Aha” moment. A model response may contain
candidate invariants, reductions, or alternative formulations beyond the requested
proof. We document their provenance by using prompt records to identify the initial
observation and the manuscript to record the human work of selecting, formalizing,
verifying, and integrating it.
     Example. In the synthesis example, the model’s reply included a secondary
observation about the update dynamics. The AI-generated seed is identifiable in Ap-
pendix A.3.5, where the model pointed to confinement in a two-dimensional working
subspace. The human contribution lies in reworking that seed into a mathemati-
cal result. Human authors recognized that the high-dimensional unitary evolution
could be tracked through a small number of scalar variables once the dynamics was
restricted to the Grover plane. They then formulated a theorem that records the
associated classically computable scalar process and resolves the matrix product into
a low-dimensional update.
    Theorem 4.2. Let H be a projector and ψ0 a rank-one projector. Assume 0 <
Tr(Hψ0 ) < 1. Fix the five-factor gate-product curve V (t; x, y) of Theorem 5.2, with
parameters prescribed by (5.4) and V (t; 0, 0) = I. Define U0 = I, ψk = Uk ψ0 Uk† , and

                                [H, ψk ] = xk X0 + yk Y0 ,
                        Vk = V (tk ; xk , yk ),      Uk+1 = Vk Uk ,

where X0 = [H, ψ0 ] and Y0 = i[H, X0 ]. Then there exists an explicit, classically
computable process

(4.1)                    Ftk (xk , yk , qk ) = (xk+1 , yk+1 , qk+1 ),

where (xk , yk ) ∈ R2 are the real coordinates of the commutator [H, ψk ] in the fixed
basis (X0 , Y0 ) of the two-dimensional gradient plane, qk = Tr(Hψk ) ∈ [0, 1] is the
scalar success probability, and tk ∈ R≥0 is the stepsize. For this fixed product and
parameter rule, F is a three-dimensional real scalar update on R2 ×[0, 1], parametrized
by tk and obtained by restricting the full N × N matrix dynamics to the Grover plane.
This scalar process keeps all iterates within U(N ), preserves the Grover plane S, and
admits closed-form scalar recursions.
     5. AI-assisted theorem discovery. Theorem discovery is often harder than
fixed-target proving because the final statement remains open during the search. AI
can help by proposing candidate statements, patterns, invariants, normal forms, and
boundary tests. Human experts still fix the assumptions, judge the evidence, and
decide which byproducts are promoted to named results.
              HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                             11

      5.1. From assumptions to conclusions through AI-guided discovery.
    5.1.1. AI-guided proposal of candidate conclusions. Human experts begin
with a fixed setting, assumptions, class of objects, and admissible ambient space, while
the precise conclusion remains open. In this situation, they prompt the AI to propose
candidate consequences of the assumptions, such as plausible properties, equivalent
formulations, reductions, and statements about extreme or boundary regimes. To
encourage diversity, they ask for multiple variants with short explanations and, when
appropriate, suggested counterexamples. Since the model can make mistakes or over-
state what is true, each proposal must provide light supporting evidence, such as
tests on simple and edge cases, quick numerical checks, and references to comparable
results. The returned suggestions are then filtered by explicit criteria, and for each
candidate we record whether it passes or fails and why.
    Human experts then analyze and select. They test validity more thoroughly, eval-
uate whether a candidate improves interpretability or tightens bounds, and keep the
statements that clarify mechanisms or simplify later analysis. From these surviving
candidates, they distill a clean, testable theorem shape, including assumptions and
theorems. AI is used to expand it into a coherent, step-by-step argument. Discarded
claims are recorded as negative evidence and inform the next round of prompts.
    Example. We illustrate the discovery workflow on the Grover-type iteration.
Our goal is to explore the properties of a simple projector-driven dynamics underlying
the Grover search operator. We use the AI interaction to surface candidate structural
statements. At a high level, we study the evolution of pure states under repeated
updates driven by a fixed projector and ask for invariants, norm identities, and scalar
recursions that describe this process.
    First, we consider the general exponential update. Concretely, fix a projector
H = H † =pH 2 and consider pure states ψk = |ψk ⟩⟨ψk |. Define qk = Tr(Hψk ) ∈ [0, 1]
and γk = qk (1 − qk ). We study the following exact exponential step
                                                                        †
(5.1)     Vk = exp tk [H, ψk ] ,     Uk+1 = Vk Uk ,      ψk+1 = Uk+1 ψ0 Uk+1 .

At this stage, the structurally decisive properties of this update are still being iden-
tified, so the final theorem is left open. We ask the model to surface plausible con-
sequences of the dynamics, such as invariance properties, norm identities, scalar re-
cursions, or one step convergence conditions. These suggestions are then checked for
internal consistency and usefulness for the later analysis, retaining only statements
that clarify the mechanism or simplify the argument. This leads to the following
precise statement.
     Proposition 2 (Exact step via exponentialp        (“Exp update”)). Let H = H † =
  2
H and define qk = Tr(Hψk ) and γk = qk (1 − qk ). The following properties hold
for (5.1).                                             √
     (i) The gradient norm identity ∥[H, ψk ]∥F = 2 γk .
    (ii) The state |ψk ⟩ remains in the real two dimensional Grover plane spanned by
         {|ψ0 ⟩, H|ψ0 ⟩}.
   (iii) The quantity qk+1 has a closed form recursion obtained by viewing the update
         as a rotation on this plane.                                         √
                                                                       arccos q0
    (iv) If 0 < q0 < 1, there exists a positive one-shot step t∗0 =        γ0    such that
           t∗ [H,ψ0 ]           ∗
         e  0         |ψ0 ⟩ = |ψ ⟩ and max f (U ) = 1 are attained in a single update. At
         q0 = 0 or q0 = 1, [H, ψ0 ] = 0, so every finite exponential step leaves the state
         unchanged. The case q0 = 1 is already optimal, whereas q0 = 0 cannot reach
12                       C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


        f = 1 by this update.
    We used the assumption-driven prompt in Appendix A.3.6 to generate candidate
structural properties. Human authors retained only statements that passed the end-
point checks qk = 0, 1, low-dimensional comparisons between the full matrix update
and scalar recursion, and tests outside the stated product-generated Grover plane.
These surviving claims form Proposition 2.
     5.1.2. Human abstraction and cross-setting transfer. After one iteration
of the discovery loop, human experts extract patterns such as recurring steps, reusable
lemmas, and canonical normalizations. These ingredients are summarized into a por-
table proof schema that records what to assume, what to try first, which invariants to
test, and which failure modes to monitor. The schema is then transferred to nearby
settings, such as related function spaces, modified boundary conditions, or perturbed
parameter ranges. Human experts prompt the AI to adapt earlier lemmas, inequali-
ties, and constants to generate variants on similar cases.
     In summary, the working loop for exploring conclusions of fixed assumptions is as
                  propose → check → distill → prove → transfer,
with the AI broadening the search and providing evidence-backed suggestions, and
human experts supplying direction, skepticism, selection, and cross-setting reuse. The
outcome combines a theorem for the initial setting with a transferable pattern that
can be tested in related regimes.
     Example. We treat the projector-driven in-
stance in Section 5.1.1 as an exemplar for transfer.
From the prior round, the AI returned several prop-      (I-H)|ψ₀⟩
erties that survived lightweight checks by human ex-
perts, including an invariant working subspace, a sta-
ble two-direction gradient plane, a scalar progress
statistic with a simple recursion, and a local sur-
rogate update that preserves structure within con-
                                                                              …


trolled error. We abstract these survivors into a por-
table schema and use them to organize proofs in sim-
ilar settings. Concretely, we keep the invariance and                Grover plane

closure statements as the core of the schema, and ask           𝒮 = span{|ψ₀⟩, H|ψ₀⟩} H|ψ₀⟩

the model to instantiate them under new assump-
tions while providing the same evidence pack, con-
                                                             Fig. 2. Invariant Grover plane
sisting of toy and edge-case numerics, minimal coun- shown using the orthogonal compo-
terexamples, and references to comparable mecha- nents H|ψ0 ⟩ and (I − H)|ψ0 ⟩. Prod-
nisms. The central lemma we retain is as follows.      uct updates preserve the same sub-
                                                            space S.
    Theorem 5.1 (Invariant 2D subspace lemma).
Let H be a projector, ψ0 a rank-one projector, and define iterates as follows. Let Vk
be any finite product of factors of the form eiθH and eiθψ0 , set Uk+1 := Vk Uk with
U0 = I, and let ψk := Uk ψ0 Uk† . Let

                                 qk := Tr(Hψk ) ∈ [0, 1],

and define X0 := [H, ψ0 ], Y0 := i[H, X0 ]. Then the following properties hold
     • The state |ψk ⟩ remains in the fixed two dimensional subspace (the Grover
        plane)
        S := spanC {|ψ0 ⟩, H|ψ0 ⟩} = spanC {(I − H)|ψ0 ⟩, H|ψ0 ⟩} for all k.
     • The skew-Hermitian representation of each gradient satisfies gradf  g (Uk ) =
              HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                                13

         [H, ψk ] ∈ W, where W := spanR {X0 , Y0 }. Equivalently, the tangent gradient
         is grad f (Uk ) = [H, ψk ]Uk , which belongs to WUk for all k.
    Figure 2 illustrates this invariant plane using the orthogonal decomposition |ψ0 ⟩ =
(I − H)|ψ0 ⟩ + H|ψ0 ⟩.
    The prompt is given in Appendix A.3.7. For cross-setting transfer, Proposition 2 is
used as a base lemma. The model is asked to identify an invariant working subspace,
a scalar progress statistic, and a local surrogate update. Possible transfer settings
include variational quantum eigensolver dynamics, QAOA-style product ansatzes, and
amplitude-amplification variants with different projectors. We treat these as proposed
directions for future validation. The proof of Theorem 5.1 was then written and
checked under the same human-verified workflow.
     5.2. Property constrained synthesis. Human experts specify the required
properties, admissible space, and edge cases. The model proposes parameterized can-
didates together with executable tests. Human authors run the tests locally, compare
candidates by correctness and simplicity, and send only surviving forms to symbolic
proof. Failed candidates lead to tighter assumptions or a revised search.
     Example. We treat the design of the retraction in our update rule as a property-
constrained search guided by the AI. The target properties are fixed in advance.
   (P1) V (t; x, y) is a product of factors of the form eiθH or eiθψ0 .
   (P2) V (0; x, y) = I.
   (P3) for any target tangent Z ∈ W := spanR {X0 , Y0 } with Z = xX0 + yY0 (where
          X0 := [H, ψ0 ], Y0 := i[H, X0 ]), the initial velocity satisfies V ′ (0; x, y) = Z.
     We ask the model to propose product forms and parameter couplings of different
lengths and to supply executable checks for each candidate on a seed set S ⊂ R2 .
The supplied tests check (i) (P1) syntactically, (ii) (P2) exactly, and (iii) (P3) by the
finite-difference criterion
                           V (h; x, y) − I
(5.2)                                      − (xX0 + yY0 ) ≤ ε,
                                  h                      F

for a small step size h and each (x, y) ∈ S. Human authors execute these tests locally,
including the edge cases x = 0 and y = 0. Only the shortest product that passes this
screening is sent to detailed proof.
     The following summary records the candidate screening stage. The search objec-
tive was to find a product retraction with as few factors as possible while preserving
(P1)-(P3) and admitting a clean proof. The length-3 and length-4 candidates were
rejected by the checks. The length-5 product was the shortest construction that
passed numerical screening and was then verified symbolically. Longer length-6 and
length-8 block constructions can also be written down, but they add factors while
leaving the present proof unchanged. Table 2 summarizes these candidates, where
Ca,b := eiaH eibψ0 e−iaH .
14                              C. LI, Z. LAI, D. AN, J. HU AND Z. WEN

                  Table 2. Candidate product retractions in the synthesis loop.

     Factors Representative product                                       Conclusion
       3–4   Short alternating products in H and ψ0 .                     Rejected by the checks.
        5    eia1 H eib1 ψ0 ei(a2 −a1 )H eib2 ψ0 e−ia2 H U                Shortest validated candidate
                                                                          used in the proof.
        6     Cπ/2,c1 C−π/2,c2 C0,y U .                                   Valid longer construction
                                                                          with the same proof role.
        8     C0,y/2 Cπ/2,−x/2 C−π/2,x/2 C−π,−y/2 U                       Valid longer construction
                                                                          with the same proof role.


    Theorem 5.2. For U ∈ U(N ) and η = ZU ∈ WU , with Z = xX0 + yY0 , define
the following length-5 product retraction
                          (5)
(5.3)                   RU (η) := eia1 H eib1 ψ0 ei(a2 −a1 )H eib2 ψ0 e−ia2 H U,

where the real parameters (a1 , a2 , b1 , b2 ) are defined as
                                                         p                           π
                      A := atan2(y, x),        R :=          x2 + y 2 ,   a1 = A +     ,
                                                                                     2
(5.4)
                                   π               R               R
                     a2 = A −        ,    b1 = −     ,   b2 =        .
                                   2               2               2
                                    (5)
When (x, y) = (0, 0), set RU (0) = U and V (t; 0, 0) = I. For (x, y) ̸= (0, 0), the
gate-product curve

                  V (t; x, y) = eia1 H eitb1 ψ0 ei(a2 −a1 )H eitb2 ψ0 e−ia2 H ,    t ≥ 0,

satisfies (P1)–(P3), with V (0; x, y) = I and V ′ (0; x, y) = Z. The corresponding
retraction curve through U is
                         (5)
        γU (t; x, y) := RU (tη) = V (t; x, y)U,               γU (0; x, y) = U,    γU′ (0; x, y) = η.

     The full property-constrained prompt and test specification are given in Appen-
dix A.3.8. The selected length-5 product is the shortest robust candidate in the
recorded search. Human experts replace the model’s proof sketch with a symbolic
derivation and integrate it into the main argument. The reduction uses that H is
a projector, ψ0 is rank one, and the update products are generated only by H and
ψ0 . Extensions to nonprojector observables, additional noncommuting Hamiltonian
terms, or ansatz families outside the Grover plane would require a separate analysis.
    5.3. Human-AI collaborative proof for conjectures. Proving complex con-
jectures is sensitive to the domain, geometric setting, and technical assumptions.
We organize the collaboration into four stages: (i) fix the objects, ambient space,
and assumptions, (ii) identify a literature-guided proof route, (iii) calibrate constants
through analysis and locally executed checks, and (iv) refine the stabilized argument
into a sharper theorem. The corresponding outputs are a specification checklist, proof
skeleton, tested constants and logs, and final theorem.
   5.3.1. Scoping with AI for objects, ambient spaces, and assumptions.
Human experts usually start from a rough target theorem in which several concepts
and assumptions are still vague. In the first stage, they conduct short rounds of
              HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                             15

interaction with the AI whose purpose is to make these ingredients precise. In each
round, the AI is asked to define the relevant objects, fix the ambient space (for
instance, a Euclidean space, a Riemannian manifold, or a function space), specify the
metric and the associated notion of gradient, and list all assumptions in a consistent
format. The round ends with an explicit checklist of domains of variables, regularity
or convexity requirements, boundary cases, and notation. Human experts review this
checklist, resolve inconsistencies, and repeat the cycle until the statement is internally
consistent and the AI can restate it in the agreed notation without contradictions or
hidden assumptions.
    Example. We start from an informal conjecture that gradient descent with the
5-factor retraction
               √     on the unitary group should reach a point with gradient      norm at
most ε in O( N /ε2 ) iterations, for the target function f (U ) = Tr H U ψ0 U † ,
                                                                           

defined on the unitary group U(N ) equipped with the canonical Riemannian metric
induced by the Frobenius inner product. At this point, the geometric setting is still
unresolved. The iteration can be viewed either through an ambient Euclidean lens
or through the intrinsic manifold geometry. This choice determines which notion of
Lipschitz continuity should control the complexity bound.
    After several scoping rounds with the AI, we fix the following setting. Gradients
and norms are understood in this Riemannian sense. Following standard practice in
numerical optimization, we expect that some Lipschitz constant of the (Riemannian)
gradient will enter the complexity analysis. The output of the first stage is therefore
a precise target theorem. It specifies the domain U ∈ U(N ) with its canonical metric,
the objective f , the assumption that the Riemannian gradient of f is√Lipschitz with
constant Lg , and the goal of proving an iteration bound of order O( N /ε2 ) for the
5-factor retraction gradient method.
    In this phase, the AI expands the informal conjecture into a well-posed statement
about (U(N ), canonical metric), the function f , and the constant Lg that later appears
in the complexity bound. The prompt used for this example is given in Appendix
A.3.9.
     5.3.2. Route confirmation through a literature guided plan. Once the
statement is fixed, the second stage searches for a feasible proof route. Human ex-
perts read the relevant literature and ask the AI to retrieve related results, known
inequalities, and standard proof patterns that match the scoped setting. The goal
is to construct a detailed proof skeleton, including a main strategy, a sequence of
reductions, and key lemmas and inequalities with clear logical dependencies. The AI
is used to suggest plausible decompositions of the main claim, to recall standard com-
plexity bounds under comparable assumptions, and to point to candidate references.
Human experts then check compatibility with the scoped statement and record which
external results will be instantiated and which conditions remain to be verified.
     Example. For the convergence conjecture above, experience suggests that the
iteration complexity of a gradient method is controlled by a Lipschitz constant of
the gradient. As a first attempt, we ask the AI to estimate a Euclidean Lipschitz
constant of the gradient and to combine it with standard Euclidean gradient descent
bounds. The resulting rate
                         √ has   the wrong dependence on N and is closer to O(N/ε2 )
                               2
than to the desired O( N /ε ). This shows that the Euclidean Lipschitz notion is
mismatched to the target rate in our manifold setting. For the Grover search instance,
let M := rank(H) = Tr(H) be the number of marked basis states among the N
               PN 1 ≤ M < N . The reference state is the uniform superposition
basis states, with
|ψ0 ⟩ = N −1/2 j=1 |j⟩, so Tr(Hψ0 ) = M/N .
16                         C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


    We then ask the AI to search for complexity results for Riemannian gradient
descent with retractions. The prompt is given in Appendix A.3.10. After comparing
the model’s suggestions with the optimization literature and discussion among the
authors, we identify the relevant parts of [3] as the appropriate basis for the proof.
We adopt the standard complexity result for Riemannian gradient descent with a
Lipschitz continuous Riemannian gradient. This shifts the focus from a Euclidean
Lipschitz constant to the Lipschitz constant L√   g of the pullback gradient of f on
(U(N ), canonical metric). The desired rate O( N /ε2 ) will follow if weq can prove
                                                                                           N
that the Lipschitz constant of the pullback gradient satisfies LRie ∈ O                    M   .
    We maximize f by Riemannian gradient ascent:

                   ψk := Uk ψ0 Uk† ,         Gk := [H, ψk ] = xk X0 + yk Y0 ,
                    ηk := Gk Uk = grad f (Uk ),             tk := L−1
                                                                   Rie ,
(5.5)                        (5)
                 Uk+1 := RUk (tk ηk ) = Vk Uk ,
                   Vk := eia1,k H eitk b1,k ψ0 ei(a2,k −a1,k )H eitk b2,k ψ0 e−ia2,k H .

 Here X0 = [H, ψ0 ] and Y0 = i[H, X0 ] are the fixed basis from Theorem 5.1. The
real coordinates (xk , yk ) determine (a1,k , a2,k , b1,k , b2,k ) through (5.4). If Gk = 0, set
Vk = I. The positive sign corresponds to maximizing f , equivalently minimizing −f .
     Using a constant step size t = 1/LRie , the Riemannian update achieves the tar-
geted convergence rate. The final statement is given as follows.
    Theorem 5.3 (Baseline Complexity). Suppose we run the iteration (5.5) with
the 5-factor retraction
                  p     RU defined in (5.3), and choose a fixed step size tk = 1/LRie ,
where LRie = O( N/M ) is defined as above. Then, for any ε > 0,
                              
                         2LRie
                  T ≥             =⇒       min ∥grad f (Uk )∥ ≤ ε.
                          ε2             0≤k≤T −1

Thus the second stage produces a proof plan consisting of two main tasks. The first
task is to establish a sharp estimate of LRie on U(N ) with the canonical metric and
the 5-factor retraction. The second task is to verify that the assumptions of the
Riemannian complexity theorem are satisfied by our algorithm and manifold. The
remaining work, namely the refinement of inequalities, calibration of constants, and
numerical stress tests for the bound on LRie , is carried out in the third stage.
     5.3.3. Parameter discovery: iterative estimates and numerical tests.
Along the chosen route, some lemmas or inequalities involve parameters or coefficients
that need sharp bounds. At this stage, human experts iterate with the AI on two
parallel tracks.
     (1) Parameter proposals and goal checks. Human experts state the explicit
requirements that the final theorem imposes on the parameters. For example, that
certain error terms must be bounded by a fraction of ε. The AI proposes candidate
values or bounds. Human experts test them against these requirements. Failed can-
didates are revised with short explanations (e.g. this choice violates the inequality
for large N ). Passing candidates are kept as the current best estimates. Over a few
rounds, this yields a small table of admissible constants with clear justifications.
     (2) Numerical stress tests for inequalities. For inequalities tied to the pa-
rameters, human experts ask the AI to propose simple low-dimensional checks and
executable code. They execute the checks locally and verify whether each sample
              HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                              17

satisfies the inequality. When counterexamples appear, the model helps analyze the
pattern, for instance whether violations occur near the boundary, and proposes tight-
ened assumptions for human review.
     By alternating these steps, human experts break the large problem into smaller,
verifiable pieces that the AI can help address. The AI assists with variant generation,
quick retrieval of known bounds, and parameter tuning, while human experts con-
trol the framework, proof logic, and acceptance criteria. At the end, the conjecture
is refined into a stable theorem with a clear scope, a documented proof path, and
constants checked by both analysis and targeted experiments.
     Example. Continuing the running example, to prove the Lipschitz estimate
above we first isolate the contribution of the retraction. We focus on the following
two standard inequalities for a retraction Retr(·).
               ∥Retrx (η) − x∥ ≤ α∥η∥,     ∥Retrx (η) − x − η∥ ≤ β∥η∥2 .
We ask the AI to propose candidate values for (α, β) that are valid on U(N ) for
our chosen five factor retraction RU in Theorem 5.2. The language model
                                                                     √ suggests
                                                                                2M (N −M )
αtight = 1, βtight = 4c10 , where c0 := ∥X0 ∥F = ∥Y0 ∥F = ∥[X0 , ψ0 ]∥F =     N      ,
and flags these constants as potentially tight. Human experts adopt these values after
symbolic verification. The processed theorem states as follows.
     Theorem 5.4 (Tight first and second order bounds). Consider the 5-factor
retraction RU defined in (5.3). For all U ∈ U(N ) and η ∈ WU , it holds
                                                                   1
             ∥RU (η) − U ∥F ≤ ∥η∥F ,       ∥RU (η) − U − η∥F ≤        ∥η∥2F .
                                                                  4c0
Moreover, both estimates are globally tight: as η → 0, the ratio in the first bound tends
to 1, and the ratio in the second bound tends to 1/(4c0 ).
Guided by the prompt in Appendix A.3.11, the language model is used within an
explicit propose–test–prove loop. It proposes (α, β) and executable numerical stress
tests for random unitary points and tangent vectors. Human authors run these tests
locally and revise the candidate constants if violations or unstable behavior are de-
tected. Numerical evidence identifies promising constants. The final theorem relies
on the subsequent symbolic proof and tightness argument.
     5.3.4. Refining the theorem through structural insights and improved
results. After the first successful proof, the collaboration enters a refinement stage.
In the final stage, human experts review the baseline result to identify structural prop-
erties of the problem that may have been underutilized in the initial rough analysis.
The goal here is to strengthen the theorem, including improving convergence rates,
weakening assumptions, or simplifying the final constants.
     In this phase, the interaction loop shifts from verification to discovery of struc-
ture. Human experts hypothesize stronger conditions (such as strong convexity, or the
Polyak-ojasiewicz (PL) inequality) and ask the AI to attempt to derive these condi-
tions for the scoped object. If such a bound relating the gradient norm to the function
value gap can be verified, the complexity analysis can be upgraded without changing
the underlying algorithm. This stage transforms a generic “worst-case” theorem into
a “problem-specific” sharp result.
     Example. Returning to our running example, Theorem 5.3 establishes a conver-
gence rate of O(ε−2 ). This is the standard guarantee for Riemannian gradient descent
on general nonconvex smooth functions. Human experts then examine whether the
18                            C. LI, Z. LAI, D. AN, J. HU AND Z. WEN

             Table 3. Convergence guarantees before and after the PL refinement.
     Analysis stage            Assumption used                                           Iteration guarantee
     Smoothness baseline       Riemannian pullback-gradient                              O(LRie ε−2 ) iterations for
                               smoothness with LRie                                      mink ∥ grad f (Uk )∥ ≤ ε
     PL refinement             Iterates already in and                                   O(L√Rie log(1/ε)) =
                               remaining in the local PL and                             O( N log(1/ε)) iterations for
                               smoothness √region, with                                  1 − qT ≤ ε
                               LRie = O( N )



specific objective function f (U ) = Tr(HU ψ0 U † ) has better local geometry near the
optimum, specifically a relationship between the magnitude of the gradient and the
suboptimality gap. We ask the language model to search for structural mechanisms
that could sharpen the convergence result. The concrete prompt is given in Appendix
A.3.12.
    The model identifies the PL property as a plausible route and lists the verification
steps required to test this approach. Human experts then check these steps and
formulate the refined result below.
    Theorem 5.5 (Best Complexity via PL Inequality). Consider the iteration (5.5)
under the same assumptions as in Theorem 5.3. Let qk := f (Uk ) ∈ [0, 1] be the
objective value at step k, and let qmax = 1 be the global maximum.
    Assume that the initial iterate lies in a region where the pullback-gradient smooth-
ness bound with constant LRie and the following PL inequality hold. Assume further
that all subsequent iterates Uk , for 1 ≤ k < T , remain in this region. The theorem
does not establish entry into the region from an arbitrary initialization.

                                        2     1
                           ∥grad f (Uk )∥ ≥     (1 − qk ) ,                             0 ≤ k < T.
                                              3

                           0 < ε ≤ 1− q0 , the iterates satisfy the optimality gap
Then, for any target accuracy
1 − qT ≤ ε in at most T = 6LRie log 1ε iterations.
    This final improvement illustrates the
role of the refinement stage. The baseline                                10
                                                                                0

                                                                                                             Baseline proxy O(1/√ k )
proof provided the smoothness-based guar-                                                                    PL-refined proxy O(e −ck)
antee, while the later structural analysis
                                                       Progress measure




used the specific geometry of the objective                               10
                                                                               −1                    geometric decay

to prove a local PL
                  √ inequality and combine
it with LRie = O( N ). Table 3 summarizes
the refinement. The proof is checked by hu-                               10
                                                                               −2

man experts within the workflow described
here.
                                                                                    0     10    20     30         40        50           60
     6. Roles of human and AI. In the                            Iteration number k

workflow studied here, human authors con-
trol the mathematical specification. They            Fig. 3. PL-refinement summary.
fix the objects, assumptions, admissible op-
erations, and criteria for accepting a state-
ment. The LLM works within this specification by proposing candidate proof routes,
lemmas, counterexamples, constructions, and computational checks. In the Grover
case study, human authors prune these proposals using the Grover plane, projector
identities, scalar recursions, endpoint regimes, and small matrix tests. Proposals that
conflict with these checks are repaired or rejected.
              HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                           19

     Selected prompt records and failure records make this division of labor observable.
Together, these materials show the tasks posed to the model, representative model
suggestions, the checks applied by the human authors, and the resulting acceptance,
repair, or rejection decisions. In the second, related multi-oracle case study, rejected
routes included an intersection oracle outside the stated gate model, updates that no
longer represented the average Riemannian gradient, and convention errors in matrix
products. The prompt structure supports the checking process by asking the model
to restate assumptions, separate proof attempts from counterexample searches, and
expose dependencies.
     Human authors retain full ethical and academic responsibility for the results and
for the scholarly record. The workflow is primarily a natural-language proof workflow,
supported by prompt records, the Python script for checks, and partial auxiliary for-
malization in the public repository. Proof assistants can provide stronger certification
after definitions and theorem statements stabilize. They are complementary to the
workflow studied here. An AI-generated suggestion enters the manuscript only after
human authors verify the assumptions, repair gaps, rewrite the argument, and decide
that the claim belongs in the final record. The workflow presupposes domain experts
who can identify shifted assumptions, notation drift, missing arguments, and misuse
of standard lemmas.
    7. Conclusion. We presented a human-in-the-loop workflow for mathematical
research. In this workflow, human experts set the mathematical scope, check the
model’s suggestions, and decide which statements enter the paper. The LLM is used
to explore possible proofs, counterexamples, and auxiliary claims inside this human-
defined frame. In the case study, the interaction produces checkable records and
                                                             −2
helps organize
             √the refinement from a generic smooth O(LRie ε )-type guarantee to a
PL-based O( N log(1/ε)) complexity bound for the Grover-compatible Riemannian
gradient method under the assumption that the iterates already lie in and remain in
the region where the PL inequality and pullback-gradient smoothness bound hold.
These materials provide a concrete reporting format for AI-assisted mathematical
work. They document what the model proposed, how each proposal was verified,
which routes were rejected or corrected, and which validated statements were ulti-
mately incorporated into the final paper.
     Acknowledgments. The authors used AI-based tools for English-language pol-
ishing. The authors are grateful to the (associate) editor and the anonymous referees
for their detailed and valuable comments and suggestions.
   Funding. This work was supported in part by the National Natural Science
Foundation of China under the grant numbers 12501419, 12331010 and 12288101,
and National Key Research and Development Program of China under the grant
number 2024YFA1012903.
    Availability of materials. The materials supporting this study are available in
the public GitHub repository at https://github.com/optsuite/MathResearchPrompts.
    Declarations
    Conflict of interest. The authors have no relevant financial interests to disclose.
    Appendix A. Grover-related supplementary case study and prompt
records. This appendix presents the related multi-oracle exploration, representative
rejected routes, the corresponding qualitative failure records, and selected prompts for
the main Grover-compatible case study. The versions printed here are shortened for
20                         C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


readability. The repository at https://github.com/optsuite/MathResearchPrompts
provides the prompt–response materials, reusable templates, finite-difference retrac-
tion checks, and auxiliary formalization code. The reusable templates include slots for
domain-specific assumptions, admissible operations, boundary cases, and verification
checks.
     Computational environment. The interactions used in the main case study were
conducted with GPT-5.1 through the web-based chat interface, accessed between
September 2025 and December 2025. No local LLM deployment and no local GPU
inference were used. The numerical checks reported in the main case study were small
CPU-based matrix tests which were run on a MacBook Pro with an Apple M4 chip,
a 10-core CPU, 24 GB memory, and Python 3.10.
    A.1. Multi-oracle case study. This second, related multi-oracle case study
keeps the Grover-compatible viewpoint of the main case study but replaces one or-
acle projector by several projectors. It lies outside the main theorem sequence and
examines which parts of the workflow transfer and which parts require new checks.
The starting point is the averaged objective
                                                   r
                                             1X
                               favg (U ) =         Tr(Hj U ψ0 U † ),
                                             r j=1

where H1 , . . . , Hr are oracle projectors. If a state satisfies all oracle conditions, then
each score Tr(Hj U ψ0 U † ) should be close to one. Maximizing favg is therefore a
natural way to express simultaneous progress toward all oracle conditions.
    In the commuting-projector setting, the model suggested using joint membership
patterns. A pattern b ∈ {0, 1}r records, for each j, whether a component lies in the
range of Hj . It defines a corresponding pattern projector Eb . This gives a concrete
reduction. The relevant state components lie in the span of the nonzero vectors Eb |ψ0 ⟩,
whose dimension is at most 2r . In this pattern basis, both favg and the corresponding
average-gradient direction become finite-dimensional objects that can be compared
with full matrix simulations. This reduction serves as checked exploratory material
supplementing the theorem sequence in the main case study.
    For r = 2, we additionally record a frame check in the fully active case. Let

                    G = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0)},

and, for g = (g1 , g2 ) ∈ G and ϵ ∈ {0, 1}, define
                    πi        πi       πi     πi       πi
                                                                                   †
          Wg,ϵ = e 2 g1 H1 e 2 g2 H2 e 2 ψ0 e 4 ϵH1 e 4 ϵH2 ,      Pg,ϵ = Wg,ϵ ψ0 Wg,ϵ .

 Throughout this construction, matrix products follow the standard convention that
the rightmost factor acts first. Thus the construction contains 7 × 2 = 14 projectors
generated only from the admissible phase gates associated with H1 , H2 , and ψ0 . For
a complex matrix A, define its real vectorization by
                                                      
                                             Re vec(A)
                               vecR (A) :=               .
                                            Im vec(A)

 We define Bdet as the real matrix whose columns are the vectorized deterministic
frame directions,                           
                        Bdet := vecR (iPg,ϵ ) (g,ϵ)∈G×{0,1} .
              HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                             21

 Let eb , b ∈ {00, 10, 01, 11}, denote the canonical basis vectors of the fully active
four-pattern representation, and write |b| := b1 + b2 . Order the patterns as 00 < 10 <
01 < 11. For every pair b < c with |b| ̸= |c|, define
                      (1)                            (2)
                    Dbc := eb e∗c − ec e∗b ,       Dbc := i(eb e∗c + ec e∗b ).

 These matrices form a real basis for the average-gradient subspace in the fully active
two-oracle pattern representation. We define Bavg by taking their real vectorizations
as columns,
                                      (1)        (2) 
                     Bavg := vecR (Dbc ), vecR (Dbc ) b<c, |b|̸=|c| .
 The frame condition is tested by asking whether the columns of Bavg lie in the real
column span of Bdet . In the five deterministic test configurations and 200 additional
random positive pattern-weight configurations, we obtained

                            rank(Bdet ) = rank[Bdet Bavg ] = 14,

 with the largest least-squares projection residual equal to rmax = 2.029 × 10−13 . The
reduced pattern-basis and corresponding full simulations agreed with a maximum
state-vector discrepancy of 2.091 × √ 10−15 . For N ∈ {64, 128, . .√
                                                                   . , 16384}, fitting the
observed iteration counts to TN = a N + b gave TN = 3.245224 N − 21.727607 with
R2 = 0.983305. Least-squares linear regression of log TN on log N , using the observed
iteration counts at the same values of N , gave a log–log slope of 0.542181. These
computations provide numerical diagnostics for the two-oracle construction within
the tested configurations and problem sizes.
     Several components of the workflow transfer directly: specification of admissible
operations, generation of candidate structural reductions, and numerical comparison
with full matrix dynamics. The multi-oracle setting additionally requires checks that
are absent or less prominent in the single-oracle case, including gate-model admissibil-
ity, consistency with the average Riemannian gradient, and product-order conventions.
     The second case study also supplied negative evidence. Several natural-looking
routes solved a different mathematical problem, lost the required gradient structure,
or depended on implementation conventions that the model left implicit. The next
subsection records a representative chain of such failures.
    A.2. Representative failed routes from the second multi-oracle case
study. We retain four representative failures from this case study to make the failure
record concrete: an inadmissible intersection oracle, a direction incompatible with
the average gradient, a matrix-product convention error, and overstrong numerical
convergence language. Consider again the multi-oracle objective
                                               r
                                            1X
                              favg (U ) =         Tr(Hj U ψ0 U † ),
                                            r j=1

where H1 , . . . , Hr are oracle projectors. The intended gate model permits phase gates
generated by ψ0 and by the individual Hj ’s, so admissible updates are built from
these original gates. A phase gate encoding the intersection of all marked subspaces
lies outside this model.
     A first model-generated route violated this rule. In the commuting case, the
model proposed replacing the average objective by an intersection projector such as

                                     H∩ = H1 H2 · · · Hr
22                      C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


and then optimizing
                                    Tr(H∩ U ψ0 U † ).
This is mathematically natural, but it assumes access to the phase gate e−itH∩ . That
gate already encodes the intersection and therefore changes the gate model, bypassing
the intended construction from admissible gates. Human experts rejected this route
and tightened the prompt to require that every proposed update be generated from
ψ0 , H1 , . . . , Hr themselves.
     A second failure was more subtle. Writing ρU = U ψ0 U † , and using the Hermitian-
generator convention in which the infinitesimal update is written with e−itG , the
average objective has generator
                                               r
                                            iX
                              Gavg (U ) =         [ρU , Hj ].
                                            r j=1

Some proposed updates used one component direction i[ρU , Hj ] at a time. Such an
update may be generated from admissible gates and may increase the single score
Tr(Hj ρU ). It can still fail as an update for favg , because the average-gradient di-
rection depends on all commutators in the sum above. In numerical tests, related
projected-gradient variants stalled away from the intersection after the projection re-
moved components of Gavg (U ) needed for progress. A valid proposal therefore needs
both admissible gate generation and compatibility with the Riemannian gradient of
the stated objective.
     The later frame-compatible route arose from these failures. It represents the
average-gradient direction by projectors generated from admissible gates and preserves
the original gate model. The implementation still required human correction. In one
tested frame construction, the frame condition failed when the product word was
interpreted as a left-to-right action on states. It held under the standard matrix-
product convention that the rightmost factor acts first. The same case study also led
us to weaken numerical convergence language. Experiments suggested favg (Ut ) → 1
in tested cases, while the analysis justified stationarity, for example ∥Gavg (Ut )∥ →
0, under the stated assumptions. This example shows why the workflow records
rejected routes, implementation conventions, and overstrong numerical interpretations
alongside the retained routes in this case study.
     The recovered record also shows that substantial human correction was not limited
to rejecting isolated false claims. An early formulation relied on dynamical-Lie-algebra
language that was mathematically relevant but poorly aligned with the intended op-
timization presentation, and it was later removed from the algorithmic main line.
Likewise, a frame condition that was initially supported by random constructions was
replaced by an explicit deterministic frame only after the authors required a fixed
construction and a direct span check. These episodes distinguish a discarded route
from a salvageable response whose central idea survives after a change of language,
assumptions, or verification standard.
     The table summarizes the four failure modes documented above and records
the corresponding symptom, check, and disposition. These cases were deliberately
selected to illustrate distinct failure mechanisms. They are not an exhaustive or
randomly sampled set of model outputs and therefore do not provide a base rate
for correct, salvageable, or unusable responses. We make no frequency or general-
performance inference from these four examples.
               HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                                         23

        Table 4. Failure modes documented in the second multi-oracle case study.
  Failure mode        Observable symptom      Required check                Disposition
  Gate-model drift    The intersection        Trace every proposed          Reject the intersection-
                      projector requires a    update to gates generated     oracle route and enforce
                      phase gate absent       by ψ0 , H1 , . . . , Hr .     the admissible gate list.
                      from the stated gate
                      model.
  Average-            An update follows one   Compare the proposed          Reject or revise the up-
  gradient            oracle direction or     generator with Gavg (U ).     date until it matches the
  mismatch            loses components                                      stated objective’s Rie-
                      required for average                                  mannian gradient.
                      progress.
  Convention          The frame condition     Declare that the              Correct the implemen-
  ambiguity           changes with the        rightmost factor acts first   tation and record the
                      interpretation of       and rerun the check.          failed convention.
                      product order.
  Numerical over-     Tests suggest           Separate observed             State stationarity and
  interpretation      favg (Ut ) → 1, while   convergence from the          label convergence as a
                      the analysis            proved statement.             tested observation.
                      establishes
                      stationarity.



   A.3. Prompt records for the main Grover-compatible case study. The
remaining appendix entries index the prompt families used in the main Grover-
compatible case study.

                               Table 5. Prompt index by intent.
   Appendix          Intent                        Main verification check
   label
   A.3.1             Scoping and topic con-        Human pruning of overbroad or ill-
                     ceptualization                posed directions
   A.3.2             Grover route framing          Alignment checks against known ob-
                                                   jects and symmetries
   A.3.3             Direct proof with fixed       Line-by-line proof verification and no
                     target                        fabricated references
   A.3.4             Prove-or-disprove             Parallel proof and counterexample
                     analysis                      branches
   A.3.6             Candidate theorem dis-        Edge cases, numerical probes, and se-
                     covery                        lection of surviving claims
   A.3.7             Cross-setting transfer        Reuse only invariant structures that
                                                   survive checks in the new setting
   A.3.8             Product retraction syn-       Finite-difference velocity tests and
                     thesis                        symbolic proof of (P1)–(P3)
   A.3.9             Statement specification       Explicit objects, ambient space, met-
                                                   ric, and assumptions
   A.3.10            Route confirmation            Literature check and replacement of
                                                   ambient Euclidean reasoning by Rie-
                                                   mannian reasoning
   A.3.11            Constant discovery            Numerical stress tests followed by
                                                   symbolic bounds
   A.3.12            Rate refinement               Verification of the PL inequality and
                                                   resulting iteration count
24                      C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


    A.3.1. Prompts for Section 3.1. You are an expert in both quantum algo-
rithms and mathematical optimization.
    I want to identify promising points of contact between quantum algorithms and
optimization that could lead to clean, analyzable research problems. You can refer to
the paper I give you. Please do the following:
1. Give a concise briefing that figures out:
 • The main quantum algorithmic primitives that are relevant here.
 • The main optimization paradigms that might interact with them.
 • Typical objectives, loss functions, and structural assumptions on each side.
2. Propose 5-8 concrete candidate research directions at this interface. For each
direction, provide:
 • A short description of the core idea.
 • The main mathematical objects and assumptions.
 • The nearest classical or existing results and what gap or limitation they leave.
 • A plausible class of analysis techniques.
3. For each direction, add 2-3 sentences of feasibility notes:
 • Why would this direction admit a clean theorem (or why it might fail).
 • Any obvious degenerate or trivial regimes to watch out for.
 • Whether you expect complexity or convergence guarantees to be within reach.
    Format your answer as a numbered list of candidate directions, each with com-
pact bullet points and feasibility notes. Avoid overly speculative ideas that are dis-
connected from existing theory.
     A.3.2. Prompts for Section 3.2. You are a theoretical mathematician special-
izing in the intersection of quantum algorithms and Riemannian optimization. Your
goal is to build connection between quantum algorithmic structures and Riemannian
optimization. We are investigating a Riemannian optimization explanation for quan-
tum search algorithm. Specifically, we hypothesize that Grover’s algorithm can be
rigorously interpreted as a form of Riemannian gradient descent. We need to identify
the underlying connection before attempting a proof.
     Task: Please provide a detailed theoretical framing for this intersection:
1. Object Identification: Define the precise mathematical objects on both sides. This
must include the manifold of quantum states and the specific Riemannian gradient
update rules that serve as the continuous analog.
2. Properties and Symmetries: Analyze the essential properties of Grover iterations,
such as unitarity and query complexity. How do these map to the oracle complexity
in Riemannian optimization?
3. Alignment Check: Identify specific regimes or limiting cases where the standard
gradient like updates and the discrete Grover iterations coincide structurally.
     A.3.3. Prompts for Section 4.1. The following direct-proof prompt already
contains the no-fabricated-references rule. This rule is highlighted here because it
functions as a methodological safeguard. The model may invoke standard named
results, but citation status and bibliographic support remain subject to human veri-
fication before any claim is incorporated into the manuscript.
     You are a careful mathematical assistant collaborating with human experts.
     When you are asked to prove a statement, you must:
1. restate all assumptions, notation, and domains of all variables.
2. give a numbered, line-by-line argument in which every nontrivial inference is ex-
plicitly justified.
3. cite standard results by their usual names (e.g. spectral theorem, Cauchy–Schwarz
              HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                               25

inequality) and never fabricate new references.
     Prove the following statement in a concise but fully rigorous way. In your proof,
you should in particular:
1. explain carefully why grad f (U ) = 0 is equivalent to [H, ψU ] = 0.
2. prove both directions of the optimality claim: that grad f (U ) = 0 implies that U
is a global optimizer with f (U ) ∈ {0, 1}, and that any global optimizer must satisfy
grad f (U ) = 0.
The statement gives as [Statement of Theorem 4.1].
     Output format. Return only:
1. a LaTeX proof environment with a numbered, step-by-step derivation.
2. a short LaTeX itemize list of adversarial checks a reader could perform.
Do not output any text outside these two parts.
     A.3.4. Prompts for Section 4.2. Content. You are a careful mathematical
assistant participating in a prove-or-disprove workflow. Your task is to analyze the
structural statement below about commutators of Hermitian matrices and the Lie
algebra su(n). When reasoning about this statement, you must:
1. Restate all assumptions, notation, and domains of the variables (including the
ambient space Mn (C), (skew-)Hermitian conditions, and the trace operator).
2. Run two explicit branches:
 • Proof branch: Try to show that every traceless skew-Hermitian matrix can be writ-
   ten as a commutator [A, B] with A† = A and B † = B. Use concrete constructions,
   basis expansions, or dimension arguments.
 • Disproof branch: In parallel, look for structural obstructions or counterexamples.
   Analyze the subspace spanned by such commutators, check invariants, and probe
   whether some elements of su(n) might fail to be commutators.
3. Within each branch, give a line-by-line argument in which every non-trivial infer-
ence is explicitly justified.
4. Cite standard facts (e.g. basic properties of commutators, spectral theorem, Lie
algebra identities) by their usual names and never fabricate new references.
5. After exploring both branches, provide a final verdict: decide whether the propo-
sition is true or false. If it is true, present a concise but fully rigorous proof. If it is
false, present an explicit counterexample and explain why it fails.
     Target statement (to prove or disprove). [Statement of Proposition 1].
     Required output format. Return only the following three parts in LaTeX:
1. A Proof branch subsection with a numbered, step-by-step derivation attempting
to prove the proposition.
2. A Disproof branch subsection with a numbered, step-by-step analysis searching for
obstructions or counterexamples.
3. A Final verdict paragraph stating clearly whether the proposition is true or false,
together with either a complete proof or a concrete counterexample, followed by a
short itemize list of adversarial checks a human reader could perform.
Do not output any commentary outside these three parts.
    A.3.5. Model reply for Section 4.3. The part of the model output that in-
spired us to obtain Theorem 4.2 is as follows.
    The Invariant “Jordan” Plane (Working Subspace). Because H is a projector
and ψ0 is rank-one, the evolution is strictly confined to the Krylov subspace K =
span{|ψ0 ⟩, H|ψ0 ⟩}.
1. Algebraic reason: The operators H and ψ0 , when restricted to the subspace con-
taining |ψ0 ⟩, form a closed 2 × 2 algebra (a single Jordan block of the pair {H, ψ0 }).
26                      C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


2. Geometric intuition: This is a “Grover plane” on the projective Hilbert space
connecting the start state ψ0 and the target state (the projection of H).
3. Subspace: The state ψk remains in the same 2D “Jordan plane” K as the baseline.
The operators H and ψ0 act as 2 × 2 matrices on this subspace (specifically, rank-1
                                                 √
projectors with overlap angle θ0 = arccos q0 ).
4. Dynamics: While the baseline flows continuously along the gradient [H, ψk ], the
two-factor product ansatz performs discrete rotations within the same 2D plane. It
acts as a “bang-bang” control to approximate the geodesic flow.
     Our observation The model identified that the system’s evolution is invariant
under a specific 2D subspace, effectively reducing the dynamics to SU(2) rotations.
We realized that this geometric confinement implies the existence of a low-dimensional
algebraic structure. Consequently, we were able to derive Theorem 4.2, which replaces
high-dimensional matrix operations with efficient, closed-form scalar recurrences in
(xk , yk , qk ) suitable for classical tracking.
     A.3.6. Prompts for Section 5.1.1. You are a careful mathematical assistant
helping with theorem discovery for a fixed dynamical setting. The assumptions and
notation are fixed. The conclusions are not.
     Setting. [Theorem setting for Proposition 2]. We study the following update rules
for Uk+1 and ψk+1 .
     Exact exponential step (“Exp update”): [exact update scheme in Proposition 2].
     Our broader goal is to surface structurally meaningful consequences of this dy-
namics. These may include (but are not limited to) invariants, norm and energy
identities, dimensional reductions, stability or monotonicity statements, convergence
and one shot optimality conditions, and useful lemmas for later analysis.
     Task. Starting from the setting above, use assumption-driven discovery to propose
candidate conclusions. Proceed as follows.
1. Restate all assumptions and domains (projector properties of H, rank-one nature
of ψk , ranges of qk and γk , and the unitary dynamics for Uk and ψk ).
2. Generate candidate statements. Propose a list of concise, LaTeX-ready candidate
claims. For each candidate:
 • assign a type label that you choose (for example, Invariant, Norm identity, Scalar
   recursion, Convergence guarantee, etc.).
 • provide a one or two sentence informal explanation of what the claim says and why
   it might be useful.
At least some candidates should reflect both local information (e.g. behavior in the
Grover plane,) and global information (e.g. long-time dynamics), but you are free to
propose additional categories of structural statements beyond these.
3. Selection. From the candidates that pass the tests, select a coherent subset (typ-
ically 3-5 items) that best captures the core structure of the Exp update. Combine
them into a single proposition with numbered parts (i), (ii), (iii).
4. Clarity and rigor. When presenting the final proposition, give short, line-by-line
derivations for each numbered item, with explicit justifications and citations of any
standard facts used (e.g. properties of projectors, commutators, unitary rotations in
a two-dimensional subspace). Avoid hand-waving and do not fabricate references.
     Required output format. Return only:
 • a numbered list of candidate statements with their type labels, informal explana-
   tions, and pass/fail/inconclusive labels from the light-weight tests.
 • a final LaTeX proposition environment collecting the selected statements into a
   single theorem-style statement, together with a concise, step-by-step proof.
              HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                           27

• a short itemize list of adversarial checks that a human reader could apply to stress-
  test the final proposition and its assumptions.
     A.3.7. Prompts for Section 5.1.2. You are a careful mathematical assistant
collaborating with human experts on theorem discovery and cross-setting transfer.
     Treat the setting below as one instance of a more general pattern rather than
as an isolated calculation. Your goals are extract a reusable schema that can be
instantiated in nearby settings and apply it on a similar setting.
     Baseline target. [Statement of Proposition 2].
     Instructions. Organize your answer into three sections.
1. Abstract schema. Extract the structural ingredients behind the baseline target
including but not limited to.
 • the working invariant subspace.
 • the associated gradient plane or tangent plane.
 • the scalar progress coordinate.
 • the structured local update
2. Transfer notes (invariant-product setting).
Transfer the above conclusion in the following setting. [Basic setting in Theorem 5.1].
In this product setting:
 • Propose candidate analogues of the baseline schema.
 • Formulate concrete transferred statements (propositions or conjectures).
 • Give me the proof of the new results you propose.
     Output format. a final LaTeX proposition environment collecting the selected
surviving statements into a single theorem-style statement, together with a concise,
step-by-step proof.
     A.3.8. Prompts for Section 5.2. Notation note. The curve notation in this
template is harmonized with Theorem 5.2: V (t; x, y) denotes the gate product, and
γU (t; x, y) = V (t; x, y)U denotes the retraction curve through U .
     Content. You are a careful mathematical assistant for mathematical discovery.
The goal is to construct a short gate product V (t; x, y) that satisfies a fixed list of
properties. The admissible building blocks and the target properties are given, but
the concrete product form is not.
     Setting. Let H = H † = H 2 be a projector and let ψ0 be a rank-one projector.
Define X0 := [H, ψ0 ], Y0 := i[H, X0 ], W := spanR {X0 , Y0 }. For each (x, y) ∈ R2 , we
consider tangent targets Z = xX0 + yY0 ∈ W, and search for gate-product curves
V (t; x, y) on the unitary group with the following properties: [Constraints (P1) -
(P3)].
     Task. Design V (t; x, y) by property-constrained synthesis. Proceed as follows.
1. Restate the constraints. Summarize the admissible factor types, the target space
W, and properties (P1)(P3) in your own words, making clear which quantities are
fixed data (H, ψ0 , X0 , Y0 ) and which are design choices (product length, coefficient
couplings, dependence on t, x, y).
2. Propose candidate product forms. Generate a small, ordered list of candidate
anstze for V (t; x, y):
 • Each candidate must be an explicit product of exponentials eiθj H or eiθj ψ0 with
   scalar parameters (aj , bj , . . . ) that may depend on t, x, y.
 • Prefer shorter products. Include candidates of different lengths, including length
   3, length 4, length 5, and longer products, so that there is a chance to find the
   shortest viable form.
 • For each candidate, give a one- or two-sentence explanation of how the chosen
28                       C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


   ordering and parameter couplings might help satisfy (P2)-(P3).
3. Numerical finite-difference tests. For each candidate, use a seed set S ⊂ R2 , a
small step size h > 0, and a tolerance ε > 0 to write concrete code (e.g. in Python)
for the following checks.
 • implements V (t; x, y) for given (x, y) and parameter values.
 • checks (P1) syntactically.
 • checks (P2) exactly at t = 0.
 • checks (P3) numerically on the seed set S via the finite-difference test [Equation
   (5.2)] and reports pass/fail outcomes for the test, including edge cases such as (x, 0)
   and (0, y).
The code must be executable, and you should run it to verify your construction.
4. Selection and refinement. Among all candidates that pass the numerical tests on
S, identify the shortest product that appears robust. For this selected candidate:
 • summarize the final parameter constraints.
 • restate the product in a clean, theorem-ready form.
 • sketch a proof plan for why (P1)-(P3) hold exactly, indicating which algebraic
   identities and expansions need to be verified.
     Required output format. Return only:
1. a numbered list of candidate product forms with their informal explanations and
symbolic viability labels.
2. the fully specified, shortest selected candidate in LaTeX, together with a brief,
step-by-step derivation of the parameter constraints ensuring (P1)-(P3).
3. executable Python code for the numerical tests on S, including the finite-difference
check above, and a short itemize list of adversarial checks a human reader could apply
to stress-test the construction.
     A.3.9. Prompts for Section 5.3.1. You are an expert mathematical research
collaborator specializing in geometric analysis, numerical optimization, and precise
theorem formulation. I will present a rough, informal target theorem or conjecture.
Your goal is to help me make this statement precise and analyze its provability.
     Core Responsibilities:
1. Clarification: take my vague concepts and propose precise mathematical defini-
tions. Explicitly define the ambient space, the metric, and the notion of gradient.
List necessary assumptions required to make the statement well-posed.
2. Feasibility and proof strategy: analyze the logical structure of the conjectured
bound or equality. Propose feasible proof paths: Suggest specific techniques. Identify
potential bottlenecks or technical difficulties in the proof.
3. Literature and context: connect the conjecture to standard results or known the-
orems in the field. If the conjecture seems standard or trivial, point it out. If it
contradicts known counterexamples, warn me immediately.
     Format: Use LaTeX for all mathematical expressions. Your response must be
logically organized, prioritizing mathematical clarity and insight over formatting.
     A.3.10. Prompts for Section 5.3.2. You are familiar with Riemannian opti-
mization and first-order complexity theory. I am looking at a gradient method on a
Riemannian manifold. A naive Euclidean analysis treats the manifold as a subset of
a Euclidean space, takes a Lipschitz constant of the ambient gradient, and plugs this
into standard Euclidean gradient-descent bounds. This gives the wrong dependence
on the dimension. I want to understand the correct Riemannian framework and the
relevant literature. Please do the following:
1. Explain briefly why ambient Euclidean Lipschitz constants for ∇f can lead to
              HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                            29

suboptimal or dimension-misaligned complexity bounds for algorithms that are in-
trinsically Riemannian, and why the natural object is a Lipschitz constant for the
Riemannian gradient (or for the pullback gradient under a retraction).
2. List 3-6 key references (books or papers) on Riemannian gradient descent or related
first-order methods with retractions and Lipschitz-continuous Riemannian gradients.
For each reference, give a short summary (2-3 sentences) indicating:
 • the type of manifold considered,
 • the smoothness assumptions,
 • the basic complexity statement.
3. From these references, extract a generic complexity theorem for Riemannian gra-
dient descent with retractions and Lipschitz-continuous Riemannian gradient and list
the main structural assumptions on the manifold, the retraction, and the function.
      A.3.11. Prompts for Section 5.3.3. You are a mathematical assistant with
strong background in matrix manifolds and Riemannian optimization.
      Setting. Work on the unitary group U(N ) = {U ∈ CN ×N : U ∗ U = I}, equipped
with the canonical Riemannian metric induced by the Frobenius inner product. Let
∥ · ∥ denote the Frobenius norm, and Tx U(N ) the tangent space at x ∈ U(N ).
      We use the following length-5 product retraction [Equation (5.3)], where the real
parameters (a1 , a2 , b1 , b2 ) are defined by (5.4). Here H and ψ0 are fixed Hermitian
matrices, and (x, y) are scalar coefficients associated with the tangent vector η (you
may assume a reasonable linear relation). The retraction at U ∈ U(N ) in direction
η ∈ TU U(N ) is defined by RetrU (η) := γU (1; xη , yη ) for the corresponding scalars
(xη , yη ).
      Goal. Find sharp global constants α and β (ideally optimal, or close to optimal)
such that, for all U ∈ U(N ) and all tangent vectors η ∈ TU U(N ) in a suitable step-size
range, ∥ RetrU (η) − U ∥ ≤ α∥η∥, ∥ RetrU (η) − U − η∥ ≤ β∥η∥2 .
      Requirement. You must proceed in the following order :
1. propose candidate constants and simple numerical tests.
 • Propose reasonable candidate constants (α, β), with a brief explanation.
 • Then design and explicitly perform simple numerical experiments that you would
    run to test these constants.
 • Based on these tests, explain how you would confirm or adjust your candidate
    (α, β) (for example, by taking them slightly larger).
2. give a theoretical justification.
 • Using the explicit product form of γU (t; x, y), derive theoretical bounds that prove
    the two inequalities above with your final choice of constants (or with slightly
    relaxed constants if needed).
 • Keep the argument as simple and direct as possible, using standard matrix inequal-
    ities and expansions, and make the dependence on N clear if it appears.
3. comment briefly on tightness. Explain whether the constants you obtain seem tight
or near-tight, using both your reasoning and the (hypothetical) numerical evidence.
     A.3.12. Prompts for Section 5.3.4. You are an expert in both quantum al-
gorithms and mathematical optimization. We are analyzing the convergence of a Rie-
mannian gradient descent algorithm with retractions on U(N ). The objective function
is: f (U ) = Tr(HU ψ0 U † ) where H and ψ0 are Hermitian matrices. The manifold is
equipped with the canonical metric induced by the Frobenius inner product.
     Current Baseline Result We have successfully established a complexity bound.
The current theorem is as follows: [Statement of Theorem 5.3].
     Request for Deeper Theoretical Analysis The result above gives a sublinear rate
30                      C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


(O(ε−2 )), which applies to generic smooth non-convex functions. However, our objec-
tive function f (U ) has a very specific algebraic structure (a linear trace function on
the unitary group). I suspect that the baseline analysis is too conservative because it
ignores this specific structure. Please perform a deeper theoretical analysis to see if
we can improve this bound:
1. Structural Analysis: Analyze the algebraic relationship between the norm of the
Riemannian gradient, ∥ grad f (U )∥, and the function value gap. Does the specific
form of f (U ) imply a stronger geometric property than simple smoothness?
2. Improved Convergence: If such a relationship exists, does it allow us to prove a
faster convergence rate (e.g., linear convergence instead of sublinear) under the same
algorithmic settings?
3. Refined Theorem: If you find a stronger bound, please formulate a new theorem
that reflects this improved rate and the corresponding iteration count T .
     Appendix B. Separate case study: composite (L0 , L1 )-smooth convex
optimization.
     This appendix presents a third case study on composite convex optimization
under (L0 , L1 )-smoothness. The prompt–response record and the complete human-
finalized proof document are provided in the public repository at https://github.
com/optsuite/MathResearchPrompts. We organize the discussion into four research-
process subsections and summarize the final mathematical conclusion here. The LLM
makes substantive contributions to problem scoping and to the development of the
recentering, adaptive-acceleration, and hard-instance mechanisms. We determine the
final statements and oracle scope, complete the derivations, and verify the proof.
     We study the composite optimization problem minx∈Rd F (x) := f (x) + h(x),
where f is convex and differentiable, h is proper, closed, convex, and proximable,
L0 > 0, L1 ≥ 0, and ∥∇2 f (x)∥ ≤ L0 + L1 ∥∇f (x)∥. Assume that the solution
set X ⋆ is nonempty, dist(x0 , X ⋆ ) ≤ R, and there are x⋆ ∈ X ⋆ and v ⋆ ∈ ∂h(x⋆ )
satisfying ∇f (x⋆ ) + v ⋆ = 0 and ∥v ⋆ ∥ ≤ G⋆ . Set L⋆ := L0 + L1 G⋆ . The motivating
smooth results have a small-ε leading term controlled by L0 , because h ≡ 0 implies
∇f (x⋆ ) = 0 [13, 41]. In the composite problem, ∇f (x⋆ ) = −v ⋆ can be nonzero, so
the effective curvature at optimality can instead be L0 + L1 G⋆ . We consider following
three questions:                                                     p
1. Can a proximal method attain the accelerated leading order O(R L⋆ /ε) with only
lower-order warm-start terms?
2. Can one construct a matching lower bound without allowing the proximal oracle
to reveal the embedded hard smooth instance?
3. Can an accelerated proximal method attain the upper bound while using only f (x),
∇f (x), and proxλh (x)?
     The case therefore begins with a genuine theorem-discovery task. Neither the
algorithm nor the lower-bound construction is specified by the research problem.
    B.1. Problem scoping. The first request asks why the smooth and composite
problems differ at an optimum, which scale should govern the small-accuracy regime,
and what is required for matching upper and lower bounds. The model identifies the
central obstruction: in the smooth case ∇f (x⋆ ) = 0, whereas in the composite case
∇f (x⋆ ) = −v ⋆ may have norm as large as G⋆ . It therefore proposes L⋆ := L0 + L1 G⋆
as the effective curvature scale and separates the task into an accelerated upper-bound
route and an oracle-preserving lower-bound route.
    Human disposition. We verify the KKT interpretation and retain the proposed
scale and two-sided roadmap. We reformulate the target as a near-optimal upper
                HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                                         31

Table 6. Overview of the four research-process subsections in the separate, self-contained
composite-optimization case. The LLM materially assists in developing the research route
     and key mechanisms. We complete and verify the final statements and proofs.
  Subsection          AI task                      Human verification              Resulting output
  Problem scoping     Separate the composite       Check the KKT                   The          scale
                      problem from the known       interpretation, the effective   L0     +    L1 G⋆
                      smooth case and identify     scale, and which targets        and a two-sided
                      the upper- and               remain conjectural.             research roadmap.
                      lower-bound obstacles.
  Structural          Search for an equivalent     Verify the centered             Affine    recenter-
  discovery           decomposition and            smoothness and                  ing,    generalized
                      inequalities that expose     gradient-gap relations.         cocoercivity, and
                      the correct curvature.                                       a centered gradi-
                                                                                   ent bound.
  Upper-bound         Propose an executable        Check and fix the step-size     An adaptive ac-
  development         accelerated proximal         rule, warm-start condition,     celerated scheme
                      method with adaptive         Lyapunov recursion, and         with a two-phase
                      step sizes and a potential   logarithmic terms.              complexity analy-
                      argument.                                                    sis.
  Lower-bound         Embed a smooth hard          Check global smoothness,        An      orthogonal
  discovery           instance while realizing a   proximal-oracle                 absolute-value
                      G⋆ -sized optimal            independence, and the exact     lift and a span-
                      certificate.                 deterministic scope.            respecting tran-
                                                                                   script reduction.


                           p
bound with leading term R L⋆ /ε and explicitly allow lower-order logarithmic terms,
rather than assume an accuracy-independent localization cost. We also require the
lower-bound construction to maintain a nonzero smooth-gradient component at an
optimum while revealing no information about the embedded smooth hard instance
through proximal queries. These checks turn the exploratory response into precise
obligations for the remaining subsections.
    B.2. Structural discovery. The second request asks the model to search for a
decomposition that removes the obstruction ∇f (x⋆ ) ̸= 0 without changing the exe-
cutable forward–backward step, and for inequalities that connect the centered gradient
to the objective gap. The model proposes an affine recentering and a generalized-
cocoercivity route. These mechanisms are central to the final proof once we supply
and check the exact identities.
    Human disposition. Fix v ⋆ := −∇f (x⋆ ) ∈ ∂h(x⋆ ) and define

               ϕ(x) := f (x) + ⟨v ⋆ , x − x⋆ ⟩,       ψ(x) := h(x) − ⟨v ⋆ , x − x⋆ ⟩.

Then F = ϕ + ψ, ∇ϕ(x⋆ ) = 0, and x⋆ minimizes both centered components. With
L⋆ := L0 + L1 G⋆ , the smooth component ϕ is (L⋆ , L1 )-smooth. Although v ⋆ is
unknown to the algorithm, it cancels from the complete proximal-gradient step,
                                                            
                  proxλψ y − λ∇ϕ(y) = proxλh y − λ∇f (y) .

 We combine this identity with generalized cocoercivity [41] to derive a centered
gradient–gap bound. For
                                          s2
                             q(s) :=               ,
                                     2(L⋆ + 4L1 s)
the finalized argument gives ϕ(x) − ϕ(x⋆ ) ≥ q(∥∇ϕ(x)∥), and hence ∥∇ϕ(x)∥ ≤
q −1 (F (x) − F ⋆ ). This relation supplies the adaptive curvature control used in Sub-
section B.3.
32                        C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


     B.3. Upper-bound development and human proof reconstruction. The
third request asks for an executable accelerated proximal method, an invariant that
controls extrapolated iterates, and a rigorous rate. The model proposes adaptive step
sizes tied to the centered gradient scale and a Lyapunov recursion. We retain this core
route but replace the tentative localization claim in the interaction with an explicit
step-size rule and a complete two-phase analysis.
     Human disposition. Starting from y0 = u0 = x0 , a radius bound R ≥ ∥x0 −x⋆ ∥,
and a warm-start scale Γ0 > 0, the finalized method uses
                         1                          p                         Γk
        γk :=                          ,    αk :=    γk Γk ,      Γk+1 :=          .
                L⋆ + 4L1 q −1 (Γk R2 )                                      1 + αk
It combines an extrapolated proximal-gradient point with an auxiliary update defined
by a subgradient of F . The central potential is
                                                   Γk
                           Vk := F (yk ) − F ⋆ +      ∥uk − x⋆ ∥2 .
                                                   2
Under the stated warm-start condition, we prove Vk+1 ≤ Vk /(1 + αk ) and Vk ≤
Γk R2 . The large-error phase decreases Γk R2 geometrically, while the small-error
phase applies an accelerated auxiliary-sequence bound. This yields
                    r                                                  !
                                                                Γ0 R 2
                                                         
                       L⋆             Γ0
         N =O R            + log 2 +       + (L1 R + 1) log 2 +           .
                        ε             L⋆                          ε

 The first term is the accelerated leading order, and the remaining terms record
the warm-start and generalized-smoothness overhead. The displayed scheme assumes
valid bounds R and G⋆ . If they are unavailable, an additional doubling or backtracking
wrapper is required.
     B.4. Lower-bound discovery and correction. The final request asks how
to embed a classical L⋆ -smooth convex hard instance into the composite class while
retaining an optimal certificate of size G⋆ , without allowing the proximal oracle to
reveal the hard block. The model compares same-space and orthogonal-coordinate
embeddings and identifies the latter as the robust route. We reject a same-space
affine tilt because the hard gradient can cancel the added G⋆ -component away from
the optimum.
     Human disposition. Let g : Rd−1 → R be a classical L⋆ -smooth convex hard
instance and write x = (z, r). The finalized construction is

                       f (z, r) := g(z) − G⋆ r,      h(z, r) := G⋆ |r|.

Then F (z, r) = g(z) + G⋆ (|r| − r), ∥∇f (z, r)∥ ≥ G⋆ , and

                ∥∇2 f (z, r)∥ ≤ L⋆ = L0 + L1 G⋆ ≤ L0 + L1 ∥∇f (z, r)∥.

At x⋆ = (z ⋆ , 0), a subgradient of h cancels ∇f (x⋆ ) and has norm G⋆ . The proximal
map is the identity on the z-coordinate and soft-thresholding on the r-coordinate, so
it reveals no additional information about g. Projecting the composite transcript onto
the z-block therefore transfers the classical smooth lower bound [5]. We restrict the
finalized claim to span-respecting deterministic proximal first-order methods whose
final output is one of the queried points. No unconditional lower bound is claimed
here for unrestricted deterministic outputs or randomized methods.
               HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                                    33

    B.5. Final conclusion and detailed proof record. The four research-process
subsections above summarize the development of the research direction and core mech-
anisms. The following result records the final mathematical conclusion, which we es-
tablish and verify. We state one combined summary theorem here rather than repro-
ducing every supporting statement. The complete algorithm, five supporting lemmas,
two theorem proofs, and exact constants appear in materials/l0l1/l0l1.pdf.
    Theorem B.1 (Composite (L0 , L1 )-smooth complexity). Let F = f + h, where
L0 > 0, L1 ≥ 0, and f is convex, twice differentiable, and satisfies

                               ∥∇2 f (x)∥ ≤ L0 + L1 ∥∇f (x)∥,

and h is proper, closed, convex, and proximable. Assume G⋆ ≥ 0 and that there are
x⋆ ∈ argmin F and v ⋆ ∈ ∂h(x⋆ ) such that

                 ∇f (x⋆ ) + v ⋆ = 0,       ∥x0 − x⋆ ∥ ≤ R,         ∥v ⋆ ∥ ≤ G⋆ ,

and set L⋆ := L0 + L1 G⋆ . If R > 0 and

                                           2(F (x0 ) − F ⋆ )
                                    Γ0 ≥                     ,
                                                 R2
then the adaptive accelerated proximal-gradient method summarized in Subsection B.3
reaches F (yN ) − F ⋆ ≤ ε in
                      r                                                 !
                                                                 Γ0 R 2
                                                          
                         L⋆            Γ0
           N =O R            + log 2 +      + (L1 R + 1) log 2 +
                          ε            L⋆                          ε

iterations. Conversely, for every k ≥ 1 and d ≥ 2k + 2, there is an instance in this
class such that every span-respecting deterministic proximal first-order method whose
final output is one of its queried points and that uses at most k oracle calls returns
xk with
                                                3L⋆ R2
                              F (xk ) − F ⋆ ≥            .
                                              32(k + 1)2
        p
Thus R L⋆ /ε is the tight leading-order dependence in this oracle model, while the
upper bound retains the displayed lower-order logarithmic terms.
    Overall, in this example, the LLM is used to help formulate the composite-
optimization problem, identify the effective curvature scale L0 + L1 G⋆ , explore affine
recentering and an adaptive accelerated route for the upper bound, and develop
an oracle-preserving hard-instance construction for the lower bound. The interac-
tion illustrates how these ideas are progressively refined into a coherent route from
problem scoping to matching leading-order upper and lower bounds. Further tech-
nical details and the complete proof are provided in https://github.com/optsuite/
MathResearchPrompts.

                                        REFERENCES

 [1] Yves Bertot and Pierre Casteran. Interactive Theorem Proving and Program Development:
        Coq’Art: The Calculus of Inductive Constructions. Springer, 2004.
 [2] Zhangqian Bi, Yao Wan, Zheng Wang, et al. Iterative refinement of project-level code context
        for precise code generation with compiler feedback. arXiv preprint arXiv:2403.16792, 2024.
34                          C. LI, Z. LAI, D. AN, J. HU AND Z. WEN


 [3] Nicolas Boumal, Pierre-Antoine Absil, and Coralia Cartis. Global rates of convergence for
          nonconvex optimization on manifolds. IMA Journal of Numerical Analysis, 39(1):1–33,
          2019.
 [4] Steven L Brunton, Joshua L Proctor, and J Nathan Kutz. Discovering governing equations from
          data by sparse identification of nonlinear dynamical systems. Proceedings of the national
          academy of sciences, 113(15):3932–3937, 2016.
 [5] Sébastien Bubeck. Convex optimization: Algorithms and complexity. Foundations and Trends
          in Machine Learning, 8(3–4):231–358, 2015.
 [6] Herman Chau, Helen Jenne, Davis Brown, et al. Machine learning meets algebraic combina-
          torics: A suite of datasets capturing research-level conjecturing ability in pure mathematics.
          arXiv preprint arXiv:2503.06366, 2025.
 [7] Yuri Chervonyi, Trieu H Trinh, Miroslav Olšák, et al. Gold-medalist performance in solving
          olympiad geometry with AlphaGeometry2. arXiv preprint arXiv:2502.03544, 2025.
 [8] Alex Davies, Petar Veličković, Lars Buesing, et al. Advancing mathematics by guiding human
          intuition with AI. Nature, 600(7887):70–74, 2021.
 [9] Leonardo de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob von Raumer.
          The Lean theorem prover. In International Conference on Automated Deduction, pages
          378–388. Springer, 2015.
[10] Bin Dong, Xuhua He, Pengfei Jin, Felix Schremmer, and Qingchao Yu. Machine learning
          assisted exploration for affine Deligne–Lusztig varieties. Peking Mathematical Journal,
          pages 1–50, 2024.
[11] Kazi Ahmed Asif Fuad and Lizhong Chen. LLM-Ref: Enhancing reference handling in technical
          writing with large language models. arXiv preprint arXiv:2411.00294, 2024.
[12] Shubham Gandhi, Dhruv Shah, Manasi Patwardhan, Lovekesh Vig, and Gautam Shroff. Re-
          searchCodeAgent: An LLM multi-agent system for automated codification of research
          methodologies. In International Workshop on AI for Transportation, pages 3–37. Springer,
          2025.
[13] Eduard Gorbunov, Nazarii Tupitsa, Sayantan Choudhury, Alen Aliev, Peter Richtárik, Samuel
          Horváth, and Martin Takáč. Methods for convex (l0 , l1 )-smooth optimization: Clipping,
          acceleration, and adaptivity. arXiv preprint arXiv:2409.14989, 2024.
[14] Yang-Hui He, Zhi-Gang Yao, and Shing-Tung Yau. Distinguishing Calabi–Yau topology using
          machine learning. arXiv preprint arXiv:2408.05076, 2024.
[15] Kexin Huang, Serena Zhang, Hanchen Wang, et al. Biomni: A general-purpose biomedical AI
          agent. biorxiv, 2025.
[16] Yichen Huang and Lin F Yang. Gemini 2.5 pro capable of winning gold at IMO 2025. arXiv
          preprint arXiv:2507.15855, 7, 2025.
[17] Yuxuan Huang, Yihang Chen, Haozheng Zhang, et al. Deep research agents: A systematic
          examination and roadmap. arXiv preprint arXiv:2506.18096, 2025.
[18] Thomas Hubert, Rishi Mehta, et al. Olympiad-level formal mathematical reasoning with rein-
          forcement learning. Nature, pages 1–3, 2025.
[19] Maximilian Idahl and Zahra Ahmadi. OpenReviewer: A specialized large language model for
          generating critical scientific paper reviews. arXiv preprint arXiv:2412.11948, 2024.
[20] Zhijian Lai, Dong An, Jiang Hu, and Zaiwen Wen. A Grover-compatible manifold optimization
          algorithm for quantum search. SIAM Journal on Scientific Computing, 2026. To appear.
          arXiv:2512.08432.
[21] Imre Lakatos. Proofs and refutations: The logic of mathematical discovery. Cambridge uni-
          versity press, 2015.
[22] Mike Lewis, Yinhan Liu, Naman Goyal, et al. BART: Denoising sequence-to-sequence pre-
          training for natural language generation, translation, and comprehension. arXiv preprint
          arXiv:1910.13461, 2019.
[23] Patrick Lewis, Ethan Perez, Aleksandra Piktus, et al. Retrieval-augmented generation for
          knowledge-intensive NLP tasks. Advances in neural information processing systems,
          33:9459–9474, 2020.
[24] Aitor Lewkowycz, Anders Andreassen, David Dohan, et al. Solving quantitative reasoning prob-
          lems with language models. Advances in neural information processing systems, 35:3843–
          3857, 2022.
[25] Ruochen Li, Teerth Patel, Qingyun Wang, and Xinya Du. MLR-Copilot: Autonomous machine
          learning research based on large language models agents. arXiv preprint arXiv:2408.14033,
          2024.
[26] Xun Liang, Jiawei Yang, Yezhaohui Wang, et al. SurveyX: Academic survey automation via
          large language models. arXiv preprint arXiv:2502.14776, 2025.
[27] Ryan Liu and Nihar B Shah. ReviewerGPT? An exploratory study on using large language
               HUMAN-AI WORKFLOW FOR MATHEMATICAL DISCOVERY                                     35

          models for paper reviewing. arXiv preprint arXiv:2306.00622, 2023.
[28] Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha. The
          AI scientist: Towards fully automated open-ended scientific discovery. arXiv preprint
          arXiv:2408.06292, 2024.
[29] Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. Isabelle/HOL: A Proof Assistant
          for Higher-Order Logic. Springer, 2002.
[30] OpenAI. Ten advances in mathematics and theoretical computer science, August 2026. Updated
          August 6, 2026.
[31] Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem prov-
          ing. arXiv preprint arXiv:2009.03393, 2020.
[32] George Polya. How to solve it. Princeton Press, 1957.
[33] Gal Raayoni, Shahar Gottlieb, Yahel Manor, George Pisha, Yoav Harris, Uri Mendlovic, Doron
          Haviv, Yaron Hadad, and Ido Kaminer. Generating conjectures on fundamental constants
          with the Ramanujan Machine. Nature, 590(7844):67–73, 2021.
[34] ZZ Ren, Zhihong Shao, Junxiao Song, et al. Deepseek-prover-v2: Advancing formal mathe-
          matical reasoning via reinforcement learning for subgoal decomposition. arXiv preprint
          arXiv:2504.21801, 2025.
[35] Zhihong Shao, Yuxiang Luo, et al. DeepSeekMath-V2: Towards self-verifiable mathematical
          reasoning, 2025.
[36] Lu Sun, Stone Tao, Junjie Hu, and Steven P Dow. MetaWriter: Exploring the potential and
          perils of AI writing support in scientific peer review. Proceedings of the ACM on Human-
          Computer Interaction, 8(CSCW1):1–32, 2024.
[37] Yudai Suzuki, Marek Gluza, Jeongrak Son, Bi Hong Tiang, Nelly H. Y. Ng, and Zo Holmes.
          Grover’s algorithm is an approximation of imaginary-time evolution, 2025.
[38] Terence Tao. What is good mathematics? Bulletin of the American Mathematical Society,
          44(4):623–634, 2007.
[39] William P Thurston. On proof and progress in mathematics. In 18 Unconventional essays on
          the nature of mathematics, pages 37–55. Springer, 2006.
[40] Trieu H Trinh, Yuhuai Wu, Quoc V Le, He He, and Thang Luong. Solving Olympiad geometry
          without human demonstrations. Nature, 625(7995):476–482, 2024.
[41] Alexander Tyurin. Near-optimal convergence of accelerated gradient methods under generalized
          and (l0 , l1 )-smoothness. In Proceedings of the 43rd International Conference on Machine
          Learning, volume 306 of Proceedings of Machine Learning Research, 2026.
[42] Silviu-Marian Udrescu and Max Tegmark. AI Feynman: A physics-inspired method for sym-
          bolic regression. Science advances, 6(16):eaay2631, 2020.
[43] Qingyun Wang, Qi Zeng, Lifu Huang, Kevin Knight, Heng Ji, and Nazneen Fatema Rajani.
          ReviewRobot: Explainable paper review generation based on knowledge synthesis. arXiv
          preprint arXiv:2010.06119, 2020.
[44] Yidong Wang, Qi Guo, Wenjin Yao, Hongbo Zhang, et al. AutoSurvey: Large language mod-
          els can automatically write surveys. Advances in neural information processing systems,
          37:115119–115145, 2024.
[45] Jason Wei, Xuezhi Wang, Dale Schuurmans, et al. Chain-of-thought prompting elicits reasoning
          in large language models. Advances in neural information processing systems, 35:24824–
          24837, 2022.
[46] Renjun Xu and Jingwen Peng. A comprehensive survey of deep research: Systems, methodolo-
          gies, and applications. arXiv preprint arXiv:2506.12594, 2025.
[47] Kaiyu Yang, Aidan Swope, Alex Gu, et al. Leandojo: Theorem proving with retrieval-
          augmented language models. Advances in Neural Information Processing Systems,
          36:21573–21612, 2023.
[48] Zijie Yang, Yukai Wang, and Lijing Zhang. AI becomes a masterbrain scientist. bioRxiv, pages
          2023–04, 2023.
[49] Jingqing Zhang, Yao Zhao, Mohammad Saleh, and Peter Liu. PEGASUS: Pre-training with
          extracted gap-sentences for abstractive summarization. In International conference on
          machine learning, pages 11328–11339. PMLR, 2020.
