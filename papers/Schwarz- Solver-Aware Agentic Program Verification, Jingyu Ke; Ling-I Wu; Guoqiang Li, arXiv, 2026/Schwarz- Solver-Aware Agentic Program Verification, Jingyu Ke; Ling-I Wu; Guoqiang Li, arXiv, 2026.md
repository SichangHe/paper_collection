                                                     S CHWARZ: Solver-Aware Agentic Program
                                                                   Verification
                                                             Jingyu Ke                                  Ling-I Wu                                Guoqiang Li
                                                  Shanghai Jiao Tong University              Shanghai Jiao Tong University              Shanghai Jiao Tong University
                                                    windocotber@sjtu.edu.cn                     edithwuly@sjtu.edu.cn                         li.g@sjtu.edu.cn



                                            Abstract—Agentic verification systems can often generate
                                         source-level specifications that look plausible, but plausibility is
                                         not enough: the verifier must still turn those specifications into
arXiv:2608.30803v1 [cs.LO] 31 Aug 2026




                                         SMT obligations that the solver can prove. When this step fails,
                                         current LLM-driven loops usually expose only a coarse verifier
                                         error, timeout, or unknown solver result. The model cannot tell
                                         whether the specification is wrong, a helper lemma is missing,
                                         the proof context contains irrelevant facts, or the obligation
                                         needs a different theory view. This paper presents S CHWARZ,
                                         an agentic verification harness that makes SMT-backed proof
                                         failure local, checkable, and repairable. S CHWARZ turns failed
                                         verification into obligation-local repair tasks: program-point
                                         snapshots expose checked facts at a boundary, local lemmas let
                                         the agent propose missing proof steps, and theory-aware solver
                                         policies guide the agent toward solver-friendly formulations for
                                         numeric, quantified, memory, and floating-point obligations. We            Fig. 1. A C ReachSafety code fragment adapted from SV-COMP.
                                         implement S CHWARZ for C and Rust/Verus and evaluate it on
                                         1,475 tasks. On 475 benchmarks from recent agentic verification
                                         tools, S CHWARZ solves 95.2% of the tasks. On 1,000 tasks from         or floating-point formulation. We call this property solver
                                         the SV-COMP 2026 ReachSafety track, averaging 1,427 LOC,               dischargeability: a program fact is not only intended to be
                                         S CHWARZ solves 91.5% of the tasks, compared with 60.1%                true, but is also expressed with the local facts, decomposition,
                                         for CPAchecker. Ablations and comparison with a pure-agent
                                         baseline show that solver-aware repair is effective and scalable.      and theory encoding needed for the configured SMT backend
                                                                                                                to prove it.
                                                                  I. I NTRODUCTION                                 An example from the SV-COMP ReachSafety suite illus-
                                            Large software projects continue to ship security-critical          trates the gap. As shown in Figure 1, the loop summary
                                         defects even after extensive testing, review, and deployment.          establishes x = n3 , z = 6n + 6, and the final position of n,
                                         Empirical studies of mature open-source systems show that              from which the algebraic fact A follows. The final assertion
                                         vulnerabilities are distributed across real project histories and      is a different SMT target Gc : since a is a short, the C
                                         related code regions, not merely isolated toy examples [1].            expression 6 ∗ a is first evaluated under integer-promotion
                                         Formal verification can provide stronger assurance by proving          semantics, and the verifier must also prove that the promoted
                                         program properties over all executions, but applying it to             multiplication and surrounding 64-bit arithmetic are defined.
                                         realistic software still requires substantial proof engineering. In    The unrepaired query asks the old bit-vector context and A to
                                         deductive and SMT-backed verification workflows, the checker           prove Gc , and all configured solvers time out. The accepted
                                         reduces programs equipped with source-level specifications             S CHWARZ proof introduces a local bridge Bc for the C-
                                         and auxiliary proof artifacts to verification conditions (VCs).        evaluation step: it checks that the promoted term agrees with
                                         Proof engineers must supply loop invariants, ghost state, inter-       the 64-bit algebraic term and that the relevant multiplications
                                         mediate assertions, and lemmas that expose enough semantic             and additions do not overflow. With this bridge available, the
                                         structure for automated checkers to prove those VCs [2], [3].          final assertion is discharged without forcing the top-level bit-
                                            A common failure mode in this workflow is deceptively               vector query to rediscover the C promotion and definedness
                                         simple. A user, or an LLM agent, adds a source-level spec-             reasoning.
                                         ification that matches the intended safety argument, yet the              Recent agentic-assisted verification systems seek to reduce
                                         verifier still rejects the program. The reported failure may be        the manual burden of generating source-level specifications
                                         only a failed assertion, a timeout, or an unknown SMT result.          and auxiliary proof artifacts by placing a large language
                                         From this signal alone, it is unclear whether the specification        model inside a checked repair loop. Systems built around
                                         is wrong, whether an intermediate lemma is missing, whether            interactive theorem provers such as Rocq and Lean expose
                                         the solver is distracted by irrelevant context, or whether the         explicit goals, hypotheses, tactics, and proof states checked
                                         obligation needs a different arithmetic, bit-vector, quantified,       by a trusted kernel [4], [5]. This gives the model feedback for
proof search, but it also mixes the program’s semantic intent            level specifications fail because the repair loop does
with theorem-prover context, tactic structure, and low-level             not expose missing local lemmas, irrelevant context, or
axiomatic details. SMT-backed loops offer a complementary                unsuitable theory formulations.
route by reusing mature solvers and keeping the model closer           • It presents S CHWARZ , a language-independent verifica-
to source-level specifications, but current interfaces usually ex-       tion system that turns failed verifier runs into checked,
pose only coarse verifier errors, timeouts, or unknown results           obligation-local repair tasks through program-point snap-
[6], [7]. They therefore hide the local proof context, missing           shots, local lemmas, and a set of theory-aware solver
helper facts, and theory-level choices that often determine              policies.
whether an SMT obligation can be discharged [8]–[12].                  • It evaluates S CHWARZ across 475 recent agentic-
   The key idea is to treat a failed proof not as a single request       verification benchmarks and a curated 1,000-task SV-
to rewrite the whole specification, but as a diagnostic question:        COMP 2026 C ReachSafety suite, showing that solver-
which local obligation failed, what facts were visible there,            aware repair is effective and scalable beyond small bench-
and what checked helper fact or theory view would make                   marks.
the obligation dischargeable? S CHWARZ realizes this idea with
three solver-facing optimization mechanisms. When the agent                                 II. BACKGROUND
does not know where the proof failed, checked snapshots              A. Deductive Verification
expose the symbolic facts available at selected program points.
When the proof is too large for one solver step, obligation-            Deductive verification proves program properties by reduc-
local lemmas let the agent propose a missing intermediate fact,      ing source programs and their specifications to logical proof
which must itself be proved before it can be used. When the          obligations. The classical foundation is Hoare-style reasoning:
solver is reasoning in an unsuitable representation, theory-         a triple {P } C {Q} states that command C, started in a state
aware solver policies guide the agent toward solver-friendly         satisfying precondition P , terminates only in states satisfying
formulations for numeric, quantified, memory, and floating-          postcondition Q if it terminates at all [13], [14]. Weakest-
point obligations.                                                   precondition calculi and predicate transformers provide an al-
   S CHWARZ does not ask the model to certify correctness. The       gorithmic way to compute sufficient preconditions for program
model owns search: it proposes source-level specifications,          constructs and are the basis of many modern verification-
proof decompositions, local lemmas, theory-aware solver poli-        condition generators [2], [15].
cies, and counterexample inputs. The checker owns authority:            In practical tools, source-level specifications are the artifacts
it preserves executable source code, regenerates proof obliga-       that instantiate these Hoare-style predicates. Verification engi-
tions from trusted front ends, checks SMT obligations with           neers write preconditions and postconditions to state procedure
configured solvers, and accepts unsafe claims only through           contracts, assertions to name intermediate predicates, loop
concrete replay. Thus, every accepted safe or unsafe outcome         invariants to summarize unbounded iteration, frame conditions
is grounded in deterministic checking rather than model ratio-       to bound side effects, and sometimes ghost state to expose
nale.                                                                proof-only quantities. These specifications are not trusted
   Our evaluation separates three questions that are often con-      as claims by themselves. The verifier combines them with
flated in agentic verification. First, can S CHWARZ reproduce        the program semantics and generates checked verification
or exceed the results of recent agentic-verification systems         conditions that justify each use of a specification: assertions
on their own benchmark settings? Second, how much do                 and postconditions must follow from the paths that reach
solver-facing lemmas and theory-aware policies contribute be-        them, loop invariants generate initialization, preservation, and
yond source-level specification generation alone? Third, what        exit-use obligations, and procedure calls are checked against
capability profile does S CHWARZ exhibit on feature-rich C           their contracts and frame conditions. The concrete encoding
verification tasks? We evaluate S CHWARZ on 1,475 tasks: 475         may use weakest preconditions, symbolic execution, SSA-like
benchmarks from AutoRocq and KVerus, and a curated 1,000-            intermediate forms, or a combination of these mechanisms, but
task SV-COMP 2026 C ReachSafety suite averaging 1,427                the common interface is a set of proof obligations that must
LOC. S CHWARZ solves 95.2% of the 475 existing agentic-              be discharged before the annotated program is accepted. Sys-
verification tasks and 91.5% of the SV-COMP tasks, with              tems such as Frama-C/WP for ACSL-annotated C [16], [17],
no incorrect S CHWARZ-accepted verdicts. Comparisons with a          Why3 [18], and Dafny [3] follow this contract-to-obligation
pure-agent baseline and CPAchecker, the ReachSafety cham-            pattern.
pion, show that S CHWARZ improves the SV-COMP score from
72.5% to 90.7% over the pure-agent baseline and achieves             B. SMT-backed Proof Discharge
a higher accepted pass rate than CPAchecker, 91.5% versus               Many deductive verifiers discharge generated obligations
60.1%. Ablations show that local proof repair and theory-            with SMT solvers rather than interactive proof. The front end
aware solver policies improve agentic verification.                  encodes each obligation as a formula over theories such as
   The paper makes three contributions.                              linear or nonlinear arithmetic, arrays, bit-vectors, uninterpreted
   • It identifies solver dischargeability as a bottleneck in        functions, and heap models. SMT-LIB provides a common
      SMT-backed agentic verification, where plausible source-       language for these formulas [19], and solvers such as Z3
Fig. 2. Overview of S CHWARZ. The untrusted agent works above the trusted boundary, where it plans, generates specifications or counterexamples, repairs
lemmas, and reviews failures under theory-aware policies. The trusted harness keeps hidden metadata and accepts only results validated by deterministic
obligation checking, SMT solving, or concrete replay.



implement decision procedures and heuristics for their combi-                management, lifecycle and orchestration, observability, ver-
nations [20]. To prove an obligation, the checker usually asks               ification, and governance [28]. We use this terminology in
whether the negation of the desired fact is unsatisfiable. If the            a verification-specific sense. In S CHWARZ, the execution en-
solver returns unsat, the proof step is accepted; if it returns              vironment is the isolated task workspace; the tool interface
sat, unknown, times out, or the front end cannot translate                   contains compilers, verifiers, SMT solvers, and replay com-
the relevant source-language subset, the proof step is rejected.             mands; context management consists of public task files,
   SMT automation is powerful, but its success depends on the                snapshots, and diagnostic reports; lifecycle logic runs the
chosen theory, encoding, and query context. Quantified sum-                  checked repair loop; observability records logs, SMT reports,
maries rely on heuristic instantiation, where trigger choices                and progress frontiers; verification is the deterministic proof
can create matching loops or unstable verification times [8].                or counterexample checker; and governance is the workspace
Arithmetic theories expose different limitations. Linear real                access policy and acceptance rules.
arithmetic has efficient simplex-style procedures, but linear
                                                                                                         III. OVERVIEW
integer arithmetic must also enforce integrality and is often
handled with cuts, branch-and-bound, and layered heuris-                        Figure 2 shows the S CHWARZ workflow and its trust
tics [21]–[23]. Nonlinear integer arithmetic requires still more             boundary. A benchmark exposes only the anonymized source
specialized procedures [11], while precise machine-integer                   program, target specification, and compilation environment to
reasoning is often encoded with fixed-size bit-vectors [10].                 the untrusted agent. Source-level metadata such as original
For bit-vectors, the dominant bit-blasting strategy can scale                comments, ground-truth labels, and verifier-side acceptance
poorly as bit-widths grow and arithmetic operators such as                   logic remain below the boundary inside the harness.
multiplication, division, and remainder appear [24]–[27]. In-                   The agent side is organized as a repair loop rather than
dependently, irrelevant assertions and assumptions in the query              a one-shot generator. The lead agent first makes a logical
can make otherwise similar obligations less stable or slower                 plan for the current proof attempt. It then generates or refines
to discharge [9].                                                            source-level specifications, proposes a concrete counterexam-
                                                                             ple when the task appears unsafe, and invokes lemma repair
                                                                             when the current proof attempt lacks an intermediate fact.
C. Agent Harnesses
                                                                             A reviewer step inspects failed attempts and routes the next
   Recent work defines an agent execution harness as the                     iteration back to planning or repair. The loop is guided by
infrastructure around an LLM agent and organizes it into                     theory-aware policies, which tell the agent when an obligation
seven layers: execution environment, tool interface, context                 is likely to require a different arithmetic, bit-vector, memory,
or quantifier view, while leaving the soundness decision to the   checker reports Ol and the generated SMT file, so the agent
checker.                                                          can inspect the formula at the level where the solver actually
   The checker side turns proposed artifacts into authorita-      failed.
tive outcomes. For a safe proof, the deterministic checker           This feedback changes the shape of repair. The agent must
regenerates the relevant obligations from the trusted source      decide whether the SMT file is missing source semantics,
view and asks the configured SMT solver to discharge them;        carrying too much irrelevant context, or using a theory view
an unsat result certifies that the checked obligation has no      that does not match the intended fact. To test such hypotheses,
violating model. For an unsafe answer, the harness accepts        the agent may edit the local SMT file and invoke the solver
only a witness validated by concrete replay. If the solver        directly. It may also propose candidate lemmas m1 , . . . , mk .
returns unknown, times out, or rejects a proposed lemma           The diagnostic check first asks whether the strengthened local
or specification, the attempt is not accepted. Instead, the       context is enough for the target:
checker returns diagnostics that identify the failed obligation
or artifact. Timeout and unknown SMT outcomes are routed                           Γl ∧ m1 ∧ · · · ∧ mk |=τl φl .
to the lemma-repair stage, where the lead agent receives          If this query still fails, the proposed decomposition is insuffi-
localized access to the bottleneck SMT file and may edit          cient. If it succeeds, the checker turns back to the candidate
it directly before the checker replays the attempt. We next       lemmas and requires them to be justified by the already
describe the technical design and core ideas behind these key     checked context, for example by proving
components.
                                                                           Γl ∧ m1 ∧ · · · ∧ mi−1 |=τl mi     for each i.
                      IV. T ECHNIQUE
                                                                  Thus, an SMT-local lemma is a checked decomposition of
   A key intuition behind S CHWARZ is that a verification
                                                                  the original obligation, not an unchecked assumption. This
harness should minimize two kinds of redundant context at the
                                                                  whole hypothesis-testing loop runs directly at the SMT level,
same time: redundant context presented to the SMT solver, and
                                                                  avoiding repeated calls to the deterministic checker that would
redundant exploration performed by the LLM. If the harness
                                                                  regenerate and revalidate the proof attempt from the beginning.
hides backend details behind high-level abstractions, the model
                                                                  Direct SMT edits are diagnostic rather than trusted proof
sees only that verification failed. It cannot tell whether the
                                                                  evidence: a successful experiment must be turned back into
failure comes from a wrong specification, missing context,
                                                                  a source-level annotation that the checker can regenerate and
or a solver-hostile encoding. In that setting, repair often
                                                                  validate from the original program.
degenerates into unfocused exploration. A second source of
                                                                     S CHWARZ also uses deliberately short default solver time-
repetition is the lack of prior knowledge about solver-friendly
                                                                  outs. In practice, when the context is compact and the formula
reductions: the model may repeatedly generate formulations
                                                                  matches the intended theory, many entailment steps that are
that are semantically equivalent to the desired proof fact but
                                                                  obvious under a human mental model are discharged by
inefficient for the theory combination being used.
                                                                  modern SMT solvers in milliseconds. Long default timeouts
   S CHWARZ addresses these two issues by making solver
                                                                  are therefore a poor diagnostic signal: they delay the feedback
feedback local and by making recurring theory choices ex-
                                                                  loop and make it harder to tell whether the issue is context
plicit. SMT-local lemmas expose failed solver obligations as
                                                                  size, theory choice, or a missing lemma. S CHWARZ normally
inspectable repair targets, while theory-aware policies encode
                                                                  checks local obligations with aggressive timeouts, often in the
checked guidance about which annotation forms to use under
                                                                  10–20 second range. The agent may selectively extend the
different theory scenarios. A snapshot mechanism then keeps
                                                                  timeout for an obligation it believes is intrinsically harder, but
long proof attempts from accumulating irrelevant state. The
                                                                  the default behavior favors fast failure and rapid hypothesis
rest of this section describes these three components.
                                                                  testing.
A. SMT-Local Lemmas
                                                                   Key Intuition. LLMs often fail at specification design
  The smallest repair unit in S CHWARZ is an SMT-local             because they cannot see how a source-level specification
lemma. For a source location l, the checker exposes a local        is lowered into solver obligations. Exposing and repairing
obligation                                                         SMT-local obligations removes the abstraction layers that
                   Ol = ⟨l, Γl , φl , τl ⟩,                        would otherwise cause repeated blind repair.
where Γl is the symbolic context visible at l, φl is the target
fact, and τl is the active theory view and proof policy. The      B. Theory-Aware Policies
obligation is discharged when the solver can prove                   SMT-local feedback tells the agent where a proof attempt
                          Γl |=τl φl ,                            failed; theory-aware policies tell it which formulation is likely
                                                                  to be efficient and sound for that failure. These policies are
implemented as the unsatisfiability check unsatτl (Γl ∧ ¬φl ).    not unchecked hints to the solver. They are scoped proof
When this query returns unknown or times out, the agent           directives exposed to the LLM as auxiliary context. Each
is not asked to rewrite the entire proof attempt. Instead, the    policy specifies when a source-level fact may be encoded in
a particular SMT theory, which bridge obligations must be          summaries. The policy library captures these recurring solver-
generated, and when the front end must fall back to a more         theory priors and turns them into checked choices in the proof
precise theory. We illustrate this idea through the concrete       artifact.
structure of two policies.
                                                                    Key Intuition. Introducing prior knowledge about SMT
   One policy concerns aggregate proofs over arrays and loops.      solver theories reduces redundant exploration caused by
A direct specification may ask the agent to prove a final fact      specifications that are semantically equivalent but inefficient
such as                      X                                      for the backend.
                        s=        A[k]
                            0≤k<n
                                                                   C. Snapshot Mechanism
or to show that one loop’s accumulated elements are exactly
                                                                      Snapshots keep the local repair loop from becoming global
canceled by a later loop. Stating this as one global quantified
                                                                   again. A snapshot is a named boundary in the proof state:
formula mixes several theories and program facts in a single
                                                                   it records the program point, the checked facts that remain in
obligation. Such a formula is often close to the human proof
                                                                   scope, the active proof policy, and any ghost or summary state
idea but poor as a solver target and difficult for the LLM to
                                                                   that has already been validated. Later proof steps can resume
repair locally.
                                                                   from this boundary without replaying the entire exploration
   The aggregate policy instead tells the LLM to introduce
                                                                   history or reintroducing facts that are no longer relevant.
proof-only ghost state that advances with the program. For a
                                                                      This mechanism is especially important for long programs
prefix sum, the agent may maintain a ghost prefix array P :
                                                                   and project-level code. The path from the entry point to the
        Pi+1 = store(Pi , i + 1, select(Pi , i) + A[i]).           current proof location may contain substantial control flow and
                                                                   many already-checked proof steps. If every repair attempt must
The proof is then phrased as an inductive argument over            replay that prefix, the feedback loop becomes dominated by
local ghost updates, with loop invariants or recursive-function    revalidation rather than by the local proof problem. Snapshots
summaries connecting each step to the next. This form is           let the agent stop at a previously checked point, keep only
usually closer to what SMT solvers can discharge than a single     the compact state needed for the next transition, and continue
aggregate formula, and it gives the LLM smaller obligations        repair from there.
to inspect and repair.                                                Snapshots are therefore an incremental engineering device,
   A second policy chooses between mathematical arithmetic         not the final acceptance condition. After the proof pipeline
and machine-integer bit-vectors. S CHWARZ exposes theory           reaches the end, S CHWARZ runs a clean-gate check from
selection as a first-class interface: the LLM may choose the       the original source program. In that final pass, snapshots are
proof theory for each annotation, and the deterministic checker    ignored as cached state, and all obligations are regenerated
ensures that the current formula can be lowered in that theory     and checked end to end.
while preserving the C semantics of the source program. This
lets the agent use the theory that matches the proof obligation                        V. I MPLEMENTATION
instead of inheriting one global encoding.                            We implemented S CHWARZ for C and Rust in about 220K
   Encoding every scalar obligation as BitVec preserves C inte-    lines of non-test Rust code. The implementation has three main
ger semantics, but BitVec performs poorly on complex arith-        components. First, language-specific trusted front ends define
metic, especially nonlinear products, division, and modulo-        how source-language semantics and source-level annotations
style reasoning. For example, a simple interpolation proof may     are lowered into verification conditions. Second, a shared
need the arithmetic step                                           verification core checks formulas across several SMT theories
0 ≤ t ≤ d ∧ 0 ≤ y1 − y0 ⇒ 0 ≤ t · (y1 − y0 ) ≤ d · (y1 − y0 ).     and solvers. Third, the harness layer provides the execution en-
                                                                   vironment, including Docker images and deterministic scripts
In an integer arithmetic view this is a small nonlinear fact; in   for running the agent/checker loop.
BitVec it is a bit-level statement about finite-width multipli-       Each language front end lowers the corresponding source
cation and wraparound, and the solver often has little useful      semantics into formulas over the shared verification core.
structure to exploit. Conversely, using mathematical integers      The core then discharges the generated proof obliga-
globally would be unsound when the program actually depends        tions with an SMT solver bundle. Our evaluation environ-
on low-level machine behavior. The policy therefore tells the      ment uses CVC 5 1.3.1-dev.12.58cda4cdc, Bitwuzla 0.7.0-dev-
agent to use LIA/NIA or their C-aware variants for value-level     main@d1f1bc2a, and Z3 4.16.0. For short-timeout checks,
arithmetic, and to reserve BitVec for facts whose truth depends    S CHWARZ dispatches the obligation to the configured solvers
on truncation, wraparound, or raw bit layout.                      in parallel and uses their results to classify the obligation as
   These examples illustrate the role of the policy library.       proved, refuted, unknown, or timed out.
The LLM does not need to rediscover, for every benchmark,             For C, the trusted front end translates LLM-generated
that array aggregates should be represented as scoped ghost        annotations together with C semantic requirements into proof
summaries rather than monolithic quantified formulas, or           obligations. These requirements include, for example, valid-
that BitVec is often the wrong default for scalar induction        ity of array and pointer accesses and safety conditions for
dynamic malloc/free usage. Each obligation is checked                                            TABLE I
under the symbolic context available at the corresponding                        B ENCHMARK SUITES USED IN THE EVALUATION .
program point, typically as an implication query encoded by
                                                                     Suite                         Language            Tasks Avg. LOC
asking whether the premises together with the negated target
                                                                     AutoRocq-ReachSafety          C/Rocq              112          57
are unsatisfiable. For SV-COMP ReachSafety tasks, the front          AutoRocq-NoOverflow           C/Rocq                50          79
end also generates obligations requiring the path condition for      KVerus-File                   Rust/Verus           313          59
reaching reach_error() to be unsatisfiable.                          VariousSVC-ReachSafety        C                   1000        1,427
   The C front end summarizes unbounded control flow in a            Aggregate                     Mixed               1475        987
standard deductive style. Loop invariants and loop-exit sum-
maries over-approximate the effects of loops, while function                                 TABLE II
contracts use requires and ensures clauses to over-                  LOC AND DOMINANT- FEATURE DISTRIBUTION OF THE 1,000- TASK C
approximate function behavior. Therefore, when the checker                              R EACH S AFETY SUITE .
proves a bad state unreachable in this over-approximation,
                                                                       Feature          < 100   100–1000   1000–5000   > 5000      Total
the conclusion is sound for the executions represented by
the trusted C semantics. The Rust front end follows the                Recursion          120         7           0            0    127
                                                                       Control flow        10        26          58           51    145
same overall pattern: it lowers Rust programs and annotations
                                                                       Numeric            140        81          68           18    307
into the shared verification core, while modeling Rust-specific        Floating point     114       100          22           22    258
semantic details, such as ownership, separately from the C             Array/pointer       77        83           3            0    163
memory model.                                                          Total              461       297         151           91   1000
   The harness layer wraps these trusted components in a
deterministic execution protocol. A deterministic script sched-
ules the lead agent, receives the agent-generated specification,   as part of AutoRocq’s benchmark construction; when running
invokes the backend checker, returns trusted-side diagnostics,     S CHWARZ, we remove this metadata and expose only the
and resumes the agent for the next repair iteration. The           anonymized source program, target property, and compilation
agent cannot inspect the trusted frontend lowering logic,          environment. The curated C suite is selected from the SV-
checker internals, or deterministic orchestration scripts. All     COMP 2026 ReachSafety benchmark set [29], [30]; it is
input programs are anonymized before they are shown to             stratified by feature category and LOC bucket and covers struc-
the agent, including program names, source comments, and           tured loops, arrays and pointers, floating-point and numeric
extra metadata, so the agent receives only the intended public     reasoning, bit-level operations, and recursion. Table II reports
program view.                                                      the resulting LOC-by-feature distribution for the 1,000 tasks.
                                                                   The benchmark excludes cases containing cyclic goto, which
                      VI. E VALUATION
                                                                   are outside the current frontend scope.
   The evaluation is designed to test how S CHWARZ’s frame-           The Rust/Verus portion uses 313 single-file proof tasks from
work design performs across benchmarks of different scales         the AutoVerus/KVerus setting [6], [7]. Some original tasks
and solver-theory demands. We organize the study around            include synthesis-generated proof helpers. We remove all such
three questions.                                                   helper proof material and keep only the target to be verified
RQ1: Effectiveness. How does S CHWARZ perform compared             and the generated program as the input to S CHWARZ.
with existing traditional tools and agentic verification tools?       Each task is imported into the two-view case format from
RQ2: Solver-facing interface. How much of the result comes         Section III. S CHWARZ is not given separate safe and unsafe
from obligation-local solver-facing guidance and theory-aware      modes: each input may be safe or unsafe, and the prompt
solver policies rather than from source-level specification        contains no hint favoring either outcome. We run all tools with
generation alone?                                                  a 4-hour wall-clock timeout per task. For agentic tools, we do
RQ3: Capability boundaries. On the 1,000-task C Reach-             not cap the number of model calls or repair rounds within
Safety suite, what capability profile does S CHWARZ exhibit        that timeout. Each task is limited to at most 8 CPU cores
across task features and program scales, and what limitations      and 12 GB of memory. All experiments run on a machine
remain in its current implementation?                              with an AMD Ryzen 9 5950X 16-core CPU (32 hardware
                                                                   threads) and 128 GB RAM. We use Codex CLI 0.130.0 with
A. Evaluation Setting
                                                                   GPT-5.5 xhigh as the underlying lead agent for S CHWARZ
  Table I summarizes the benchmark suites used in the              and for the pure-agent baseline. We report direct passes as the
evaluation. The evaluation uses two language settings. The C       primary metric because they correspond to outcomes accepted
portion combines AutoRocq’s SV-COMP-derived suites with            by deterministic infrastructure rather than by model judgment.
a curated 1,000-task SV-COMP 2026 C ReachSafety suite.
The AutoRocq C suites contain 112 ReachSafety programs             B. RQ1: Effectiveness
and 50 NoOverflow programs whose Rocq obligations are                S CHWARZ is compared with four representative tools:
generated by Frama-C/WP through Why3 [4], [16], [18].                • AutoRocq is an agentic verification tool for proving
The specifications used for those obligations are generated             program-verification obligations exported from Frama-
                                                                                  TABLE III
                                                                      C ROSS - BENCHMARK COMPARISON .

                                                                                                                       Direct passes (pass rate)
        Benchmark suite                   Language          Tasks
                                                                           S CHWARZ                      AutoRocq                AutoVerus                   KVerus†              CPAchecker
        AutoRocq-ReachSafety              C/Rocq            112           106 (94.6%)                45 (40.2%)                  –                        –                        25 (22.3%)
        AutoRocq-NoOverflow               C/Rocq             50           47 (94.0%)                 10 (20.0%)                  –                        –                       45 (90.0%)
        KVerus-File                       Rust/Verus         313          299 (95.5%)                     –                 217 (69.3%)              251 (80.2%)                        –
        VariousSVC-ReachSafety            C                 1000          915 (91.5%)                     –                      –                        –                       601 (60.1%)
        Aggregate                         Mixed             1475         1367 (92.7%)                             –                 –                             –                         –
Note: Result cells report direct passes, with pass rates in parentheses; a dash indicates that the tool does not target the suite or no comparable result is available. AutoRocq results
are mapped from VC-level outcomes to property-specific source-program outcomes: a source benchmark is counted solved only when all generated VCs in the corresponding
property slice are solved and rechecked. In AutoRocq-ReachSafety, the CPAchecker false-unsafe result is counted unsolved. † KVerus was not open-sourced at evaluation time, so
we report the paper’s Claude Sonnet 4.0 result.



      C/WP and Why3 into Rocq [4]. It uses Rocq proof states
      and kernel-checked proof scripts as feedback for itera-                                                            1,516
                                                                                                                                                                                            Max score (1,672)

      tively constructing proofs for the generated verification                                                1,600     90.7%


      conditions.                                                                                                                    1,212
                                                                                                                                        72.5%
   • AutoVerus targets Rust programs written for the Verus                                                     1,200                               995                986




                                                                                               SV-COMP score
      verifier and uses LLM agents to synthesize Verus specifi-                                                                                   59.5%               59.0%       860             852
                                                                                                                                                                                 51.4%            51.0%
      cations and proof code [6]. It organizes proof generation                                                 800
      into preliminary construction, verifier-guided refinement,
      and debugging from Verus errors.
                                                                                                                400
   • KVerus builds on Verus and combines dependency-
      graph analysis, semantic lemma generation and retrieval,
      toolchain knowledge, and error-driven self-refinement [7].                                                  0
                                                                                                                                                              †                             †                †
                                                                                                                        Schwarz      Baseline   CPAchecker        CPAchecker   ESBMC-kind       Symbiotic
      It uses dependency structure and reusable proof knowl-                                                                                      official                       official         official

      edge as persistent context for project-level proof repair.
   • CPAchecker is a traditional software verifier for C
                                                                                              Fig. 3. SV-COMP-style scores on the 1,000-task SV-COMP 2026 Reach-
      based on configurable program analysis, integrating mul-                                Safety suite. Daggered bars are official SV-COMP 2026 per-task results
      tiple abstract domains and model-checking strategies un-                                projected to the same local subset.
      der a common framework [31]. It ranked first in the
      C.ReachSafety category of SV-COMP 2026 [30].
   Table III is the main comparison table. AutoRocq proves                                    safe answer receives two points, a correct unsafe answer re-
generated Rocq VCs, AutoVerus and KVerus synthesize Verus                                     ceives one point, a wrong safe answer receives −32 points, and
proof artifacts, and CPAchecker checks C reachability or over-                                a wrong unsafe answer receives −16 points. The “Baseline”
flow directly [31]. S CHWARZ is evaluated through different                                   bar is the pure-agent baseline: the same underlying agent is
language front ends and the same hidden harness across the                                    asked to classify the program’s safety property as safe or un-
suites.                                                                                       safe without any formal assistance. The base model maintains
   S CHWARZ produces 1367 direct passes across 1475 tasks                                     a high solve rate without any formal assistance, but it is still
(92.7%). On the 475 tasks drawn from recent agentic ver-                                      severely affected by hallucination: on the 1,000 tasks, it emits
ification benchmarks, it passes 452 tasks (95.2%), includ-                                    17 wrong labels, including 10 wrong safe answers and 7 wrong
ing 106/112 AutoRocq ReachSafety tasks, 47/50 AutoRocq                                        unsafe answers. Two additional expected-safe tasks receive
NoOverflow tasks, and 299/313 KVerus-File tasks. On the                                       no scored answer. Under the SV-COMP penalty rule, these
1,000-task SV-COMP 2026 ReachSafety suite, S CHWARZ                                           outcomes reduce its score to 1212/1672 (72.5%). S CHWARZ
passes 915 tasks (91.5%), compared with 601 (60.1%) for                                       scores 1516/1672 (90.7%) with 915 accepted passes: 601
CPAchecker. The largest gains appear on the AutoRocq Reach-                                   safe proofs and 314 unsafe replays. It therefore substantially
Safety and KVerus-File suites, where the existing tools operate                               improves the score over both the pure-agent baseline and
through generated Rocq or Verus proof interfaces, which                                       CPAchecker (986/1672, 59.0%), while retaining deterministic
can be affected by tool abstraction layers and large amounts                                  checking for every accepted outcome.
of redundant proof context. By contrast, S CHWARZ keeps                                       Failure Analysis. We analyze the remaining cases qualita-
repair tied to source-level annotations and local solver-facing                               tively rather than reporting a separate non-pass taxonomy.
obligations.                                                                                  The dominant source of missed passes is missing semantic
   Figure 3 compares tools on the 1,000-task SV-COMP 2026                                     coverage in the current trusted front ends and solver backends.
ReachSafety suite using the SV-COMP scoring rule: a correct                                   Examples include standard-library or libm functions whose
                                                               TABLE IV
                                                    A BLATION COMPARISON FOR RQ2.

                                                         Full                                                                 Ablation
     Benchmark suite           Language     Tasks
                                                      S CHWARZ            No Policies                          No SMT-Local Lemmas                      No Policies/Lemmas
     AutoRocq-ReachSafety      C/Rocq        112     106 (94.6%)       104 (92.9%)                                        91 (81.3%)                           82 (73.2%)
     AutoRocq-NoOverflow       C/Rocq        50       47 (94.0%)        45 (90.0%)                                        43 (86.0%)                           46 (92.0%)
     KVerus-File               Rust/Verus    313     299 (95.5%)       281 (89.8%)                                       256 (81.8%)                          230 (73.5%)
     VariousSVC-ReachSafety    C            1000     915 (91.5%)       871 (87.1%)                                       756 (75.6%)                          723 (72.3%)
     Aggregate                 Mixed        1475    1367 (92.7%)   1301 (88.2%)                                          1146 (77.7%)                         1081 (73.3%)



precise semantics are not yet modeled, such as tanf, sqrtf,                                                                                                                  1.00
                                                                                                 Recursion     119/120           6/7                   --             --
and string routines such as strncmp; C constructs that                                                          99.2%           85.7%                                        0.95

require finer bit-level layout modeling, especially union-heavy                                                                                                              0.90




                                                                   Dominant source feature
                                                                                               Control flow     9/10             26/26                50/58          50/51
                                                                                                               90.0%            100.0%                86.2%          98.0%   0.85
code; and cases where the target location requires a large




                                                                                                                                                                                    Solve rate
number of source-level specifications before the agent can                                                     138/140          78/81                 67/68          15/18   0.80
                                                                                                   Numeric      98.6%           96.3%                 98.5%          83.3%
establish a sufficient symbolic context. These implementation                                                                                                                0.75

and backend semantic gaps account for roughly 80% of                                                           89/114           80/100             22/22             12/22   0.70
                                                                                             Floating point    78.1%            80.0%             100.0%             54.5%
the unresolved cases in our logs. By contrast, plain time                                                                                                                    0.65
                                                                                             Array / pointer   75/77            77/83                  2/3            --     0.60
exhaustion is less common: in the 1,000-task SV-COMP suite,                                                    97.4%            92.8%                 66.7%
                                                                                                                                                                             0.55
only 13 tasks remain unresolved primarily because the run                                                      <100            100-1000          1000-5000          >5000
                                                                                                                                         LOC bucket
ran out of time before the needed specification route could be
generated and checked.
                                                                   Fig. 4. S CHWARZ accepted passes by dominant source feature and LOC
                                                                   bucket on the 1,000-task SV-COMP 2026 ReachSafety suite. Each cell reports
 Answer to RQ1. S CHWARZ solves 1367/1475 tasks across             accepted passes over tasks in that bucket and the corresponding pass rate.
 the evaluation suite (92.7%), including 452/475 tasks from
 recent agentic-verification benchmarks and 915/1000 SV-
 COMP ReachSafety tasks. On the SV-COMP subset, it                 ReachSafety, it decreases from 94.6% to 81.3%. These drops
 improves the score from 1212/1672 for the pure-agent              support the design premise of S CHWARZ: many failed obli-
 baseline to 1516/1672, while also exceeding CPAchecker’s          gations are not solved by simply adding more source-level
 accepted pass rate, 91.5% versus 60.1%.                           annotations. The agent often needs a way to expose a small
                                                                   missing proof step, test it directly against the generated SMT
                                                                   obligation, and then lift the successful step back into a checker-
C. RQ2: Solver-Facing Interface                                    accepted source annotation. Without this local repair loop, the
   RQ2 tests the contribution of local solver-facing optimiza-     agent must infer the solver bottleneck indirectly from a larger
tion, not merely whether the LLM can produce more source-          verifier failure, which leads to more redundant exploration.
level specifications. Table IV uses a two-factor ablation:            Theory-aware policies provide a smaller but still consistent
theory-aware solver policies are either enabled or disabled,       benefit on the larger suites. Removing policies loses 44 passes
and SMT-local lemmas are either enabled or disabled. This          on VariousSVC-ReachSafety and 18 passes on KVerus-File.
isolates whether the gains come from choosing solver-friendly      This is expected: policies do not replace proof construction,
theory views, from adding checked intermediate proof steps,        but they bias the agent toward annotation forms that fit
or from their combination.                                         the dominant theory view of the obligation. Their effect is
   Table IV shows that both components contribute to the           therefore most visible when the task mixes arrays, machine
overall result, but they do so at different magnitudes. With       integers, bit-level facts, and arithmetic summaries, where
the full solver-facing interface, S CHWARZ passes 1367/1475        several semantically equivalent annotations can produce very
tasks (92.7%). Removing theory-aware policies reduces the          different solver behavior. The AutoRocq-NoOverflow suite is
aggregate result to 1301 passes (88.2%), a loss of 66 tasks.       less diagnostic: all configurations remain within four tasks
Removing SMT-local lemmas has a larger effect: the re-             of the full system, suggesting that these short arithmetic
sult drops to 1146 passes (77.7%), losing 221 tasks. When          obligations are already close to saturation under the current
both components are disabled, the system passes 1081 tasks         harness.
(73.3%), 286 fewer than the full configuration.                       The combined ablation is worse than either single ablation
   The largest and most stable drop comes from disabling           on three of the four suites and on the aggregate. This indi-
SMT-local lemmas. On the 1,000-task C ReachSafety suite,           cates that the two mechanisms are complementary. SMT-local
the pass rate decreases from 91.5% to 75.6%; on KVerus-            lemmas give the agent a checked way to decompose a hard
File, it decreases from 95.5% to 81.8%; and on AutoRocq-           obligation; policies help it choose a decomposition that the
solver can handle efficiently. The gap between the full system      E. Threats to Validity
and the combined ablation is especially large on KVerus-
                                                                       The evaluation has two main threats. First, benchmark suites
File (299 versus 230 passes) and on VariousSVC-ReachSafety
                                                                    differ in task granularity and proof artifact: Rocq VCs, Verus
(915 versus 723 passes), where proof search often depends on
                                                                    proof artifacts, and C source programs are not interchangeable
both local intermediate facts and theory-sensitive annotation
                                                                    units. We therefore report per-suite results instead of treating
choices.
                                                                    the aggregate as a universal leaderboard. Second, the overall
 Answer to RQ2. The solver-facing interface accounts for a          results may be affected by nondeterminism in model outputs
 substantial fraction of S CHWARZ’s performance. SMT-local          and by the incomplete coverage of the current prototype.
 lemmas are the dominant contributor, and theory-aware              A specification may admit multiple proof routes and theory
 policies add further gains on feature-rich tasks; together,        choices, while some programs fall into semantic regions that
 they raise the aggregate pass rate from 73.3% to 92.7%.            S CHWARZ does not yet fully support, leading to blocked runs
                                                                    rather than accepted outcomes.


D. RQ3: Capability Boundaries                                                           VII. R ELATED W ORK

   RQ3 uses the 1,000-task C ReachSafety suite to characterize      Agentic program verification. The closest line of work
the boundary of S CHWARZ’s current capability. Figure 4             uses language-model agents to generate or repair proof arti-
breaks the 915 accepted passes down by dominant source              facts around a verifier. AutoRocq proves program-verification
feature and LOC bucket. The main observation is that the            obligations exported from Frama-C/WP and Why3 into Rocq,
pass-only metric remains high across several different kinds of     giving the agent explicit theorem prover states and a trusted
tasks, not only on short programs: S CHWARZ solves 119/120          kernel [4], [16], [18]. LemmaNet further adds source-guided
recursion cases and 138/140 numeric cases below 100 LOC,            auxiliary lemma generation at the Rocq level: it maps the se-
77/83 array-pointer cases and all 26 control-flow cases in the      mantics of source-level helper specifications into Rocq lemmas
100–1000 LOC bucket, 67/68 numeric cases in the 1000–5000           and improves the solve rate over the AutoRocq pipeline [5].
LOC bucket, and 50/51 control-flow-heavy cases above 5000              This Rocq-based route has a different cost profile from
LOC. These results are consistent with the role of local solver     SMT-backed deductive repair. As illustrated by LemmaNet’s
feedback, theory policies, and snapshots beyond the smaller         Fig. 2, the Frama-C/Why3-to-Rocq path must compile pro-
AutoRocq-derived C tasks.                                           gram semantics into Rocq formulas and often introduces
   The heatmap also exposes the current boundary. Floating-         verbose contexts and axiomatic encodings around the target
point tasks are the least stable region: S CHWARZ solves 89/114     lemma. When an early lemma in the proof route needs to be
tasks below 100 LOC, 80/100 tasks in the 100–1000 LOC               reconstructed, Rocq compilation and proof replay can become
bucket, and 12/22 tasks above 5000 LOC, even though it              a bottleneck in the agentic repair loop, especially on larger
solves all 22 floating-point tasks in the 1000–5000 LOC             programs. S CHWARZ takes the complementary design: it re-
bucket. Manual inspection indicates that many of these misses       pairs source-level annotations while using short-timeout SMT
are caused by missing built-in models for library and libm          obligations as the local feedback unit. This avoids replaying a
behavior, including functions such as sqrtf and tanf, rather        large Rocq development for each hypothesis test and lets the
than by the absence of a high-level proof strategy. A second        agent reuse mature SMT theory reasoning, lemmas, and solver
boundary appears in longer proof routes where the target            heuristics instead of reproving facts already modeled by the
location is preceded by many semantically relevant checks           solver. The interactive theorem-proving route remains valuable
and updates. Snapshots reduce the cost of replaying already         for domains where SMT support is weak, such as SQL-style
proved prefixes, but more aggressive snapshot placement and         bag reasoning with aggregation and order.
context summarization would expose a smaller checked state             AutoVerus and KVerus are agentic frameworks built on the
near the target during repair iterations. Finally, a small number   Rust Verus verifier [6], [7]. AutoVerus introduces a simple re-
of memory-layout cases still require more precise modeling of       pair loop that iteratively fixes generated proofs, while KVerus
layout-sensitive C constructs, especially unions and bit-level      targets project-level proof generation by using static program
reinterpretation.                                                   information to help the LLM understand interprocedural data
                                                                    and control dependencies. Both systems also use proof lem-
 Answer to RQ3. S CHWARZ is strongest on integer and                mas to improve the verification of complex specifications.
 numeric reasoning, recursion, and large control-flow tasks         Relative to S CHWARZ, however, their lemmas remain at the
 where source-level summaries can be checked locally and            Verus frontend level: they help the model repair Verus-facing
 reused through snapshots. Its current limitations are con-         specifications, but they do not directly explain why the SMT
 centrated in floating-point and library semantics, layout-         obligations produced after Verus lowering return unknown
 sensitive C features, and long proof routes that require           or time out. Such solver-level failures are common in larger
 many specifications before the target location.                    verification tasks, and modeling them explicitly is the core
                                                                    problem addressed by S CHWARZ.
   Earlier LLM-assisted formal-verification work is broader        agentic harness can expose enough proof interface for an LLM
than these verifier agents. One line asks LLMs to predict in-      to construct useful source-level specifications and proof facts
variants or proof hints and then checks or ranks the candidates    while leaving correctness judgments to deterministic checkers.
with symbolic tools [32]–[37]. Another line targets proof as-
sistants and formal theorem proving: DSP uses informal proof                            VIII. D ISCUSSION
drafts to guide formal proof sketches, Baldur generates and           During the development of S CHWARZ, we observed that the
repairs whole Isabelle proofs, LeanDojo/ReProver augments          plan-execute-review pattern has become a relatively standard
Lean proving with premise retrieval, and COPRA performs            outer loop for agentic systems. As this outer structure stabi-
stateful in-context tactic search for Lean and Coq [38]–[41].      lizes, the main question is no longer whether a harness can
These systems established the checked-generation pattern: the      ask an agent to plan, act, and revise, but what information
model proposes logical candidates, and a deterministic checker     and control surfaces the harness exposes inside that loop.
accepts or rejects them. S CHWARZ builds on this pattern but       The design of S CHWARZ follows this view: its purpose is
studies a deeper repair problem: how to expose local SMT           not to show the agent the front-end lowering code and ask
failures, theory choices, and replay boundaries in a source-       it to infer the verifier’s behavior. Instead, S CHWARZ exposes
level program-verification harness.                                solver-level context and the correspondence between source-
LLM-assisted SMT reasoning. Recent work has begun                  level specifications, symbolic contexts, and SMT obligations.
to use LLMs to improve SMT and constraint solving more             This makes the logical path from source annotations to SMT
directly. AquaForte uses LLM-generated semantic guidance to        queries explicit enough for the agent to diagnose local proof
instantiate quantified formulas with uninterpreted functions,      failures, while keeping the trusted lowering and checking logic
reducing the search space for traditional SMT solvers [42].        outside the agent’s control.
Another line uses LLMs to generate auxiliary lemmas for               We also found that domain knowledge is becoming an
constraints with inductive or recursive definitions, and then      essential part of harness design. Many useful verification
asks symbolic solvers to check the validity and usefulness         techniques are not simply generic reasoning patterns that a
of those lemmas [43]. These systems are close in spirit to         base model can be expected to know reliably. They include
S CHWARZ because they treat LLM output as hypotheses that          recent research results, solver-specific engineering heuristics,
must be checked by a solver.                                       and low-level improvements in verification tools, all of which
   The main difference is scope and information source.            may appear too late or too sparsely to be absorbed into the base
Existing LLM-assisted SMT systems are designed around              model during pretraining. An effective harness therefore needs
particular theory fragments, such as quantified uninterpreted      mechanisms for bringing this knowledge into the repair loop.
functions or recursive definitions. S CHWARZ instead organizes     One route is to let the harness accumulate reusable experience
solver-facing repair as part of a program-verification harness,    from prior runs as long-term context. Another is to encode
combining local lemmas, snapshots, and theory policies under       expert knowledge directly, as S CHWARZ does with theory-
a single checked workflow. Moreover, after source programs         aware policies that guide the agent toward solver-friendly
have been lowered into SMT, part of the source-level semantic      annotations. In both cases, the harness is not merely a wrapper
structure has already been abstracted away. S CHWARZ gener-        around an LLM; it becomes the place where domain expertise
ates and repairs lemmas using both the SMT obligation and the      is organized, checked, and made operational.
corresponding source-level program context, while approaches
that optimize SMT formulas alone must work without that                                  IX. C ONCLUSION
additional semantic view. These directions are therefore largely      S CHWARZ studies agentic verification as a harness problem:
orthogonal: LLM-guided SMT techniques optimize general             the model searches over annotations, decompositions, and
solver tasks, while S CHWARZ combines similar solver-facing        theory choices, while correctness remains with deterministic
repair with the source-level semantics of program verification,    front ends, SMT checking, and concrete replay. Its central
making the optimization more effective for verification tasks.     lesson is that plausible source-level specifications are not
Traditional verification tools and specification languages.        enough; the harness must expose the symbolic context, missing
S CHWARZ is complementary to mature verification tools.            proof steps, and theory choices that make SMT obligations dis-
CPAchecker provides a configurable framework for C soft-           chargeable. Across 1,475 tasks, S CHWARZ solves 1367 cases,
ware verification and a strong SV-COMP baseline [29], [31].        including 95.2% of recent agentic-verification benchmarks and
CBMC performs bit-precise bounded model checking for C             91.5% of the 1,000-task SV-COMP 2026 ReachSafety suite.
assertions [44], and KLEE uses symbolic execution to generate      The remaining failures are mostly semantic coverage gaps,
high-coverage tests for systems programs [45]. Frama-C/WP          suggesting that progress depends on harnesses that organize
generates weakest-precondition VCs from ACSL-specified C           domain knowledge and expose checked solver-facing repair
programs [16], [17], while Dafny and Verus provide SMT-            to agents.
backed specification and proof systems for high-level or Rust-     Use of Generative AI. The authors used generative AI tools
like programming models [3], [6], [46]. S CHWARZ does not          to assist in generating Figures 1 and 2; all figure content was
replace these systems with model judgment. It studies how an       manually checked.
                              R EFERENCES                                         [22] D. Jovanović and L. de Moura, “Cutting to the chase solving linear
                                                                                       integer arithmetic,” in Automated Deduction – CADE-23, ser. Lecture
                                                                                       Notes in Computer Science, vol. 6803. Springer, 2011, pp. 338–353.
 [1] B. Liu, G. Meng, W. Zou, Q. Gong, F. Li, M. Lin, D. Sun, W. Huo, and         [23] A. Griggio, “A practical approach to satisfiability modulo linear integer
     C. Zhang, “A large-scale empirical study on vulnerability distribution            arithmetic,” Journal on Satisfiability, Boolean Modeling and Computa-
     within projects and the lessons learned,” in Proceedings of the 42nd              tion, vol. 8, no. 1–2, pp. 1–27, 2012.
     International Conference on Software Engineering. ACM, 2020, pp.
                                                                                  [24] Y. Zohar, A. Irfan, M. Mann, A. Niemetz, A. Nötzli, M. Preiner, A. W.
     1547–1559.
                                                                                       Reynolds, C. Barrett, and C. Tinelli, “Bit-precise reasoning via int-
 [2] R. Hähnle and M. Huisman, “Deductive software verification: From                 blasting,” in Verification, Model Checking, and Abstract Interpretation,
     pen-and-paper proofs to industrial tools,” in Computing and Software              ser. Lecture Notes in Computer Science, vol. 13182. Springer, 2022,
     Science: State of the Art and Perspectives, ser. Lecture Notes in                 pp. 496–518.
     Computer Science. Springer, 2019, vol. 10000, pp. 345–373.                   [25] A. Niemetz, M. Preiner, and Y. Zohar, “Scalable bit-blasting with
 [3] K. R. M. Leino, “Dafny: An automatic program verifier for functional              abstractions,” in Computer Aided Verification, ser. Lecture Notes in
     correctness,” in Logic for Programming, Artificial Intelligence, and Rea-         Computer Science, vol. 14681. Springer, 2024, pp. 178–200.
     soning, ser. Lecture Notes in Computer Science, vol. 6355. Springer,         [26] S. Chakraborty, A. Gupta, and R. Jain, “Matching multiplications in
     2010, pp. 348–370.                                                                bit-vector formulas,” in Verification, Model Checking, and Abstract
 [4] H. Tu, H. Zhao, Y. Song, M. Zafar, R. Meng, and A. Roychoudhury,                  Interpretation, ser. Lecture Notes in Computer Science, vol. 10145.
     “Agentic verification of software systems,” Proceedings of the ACM on             Springer, 2017, pp. 131–150.
     Software Engineering, vol. 3, no. FSE, pp. 3558–3581, 2026.                  [27] S. Teuber, M. K. Büning, and C. Sinz, “An incremental abstraction
 [5] H. Zhao, H. Tu, Z. Liu, M. Rinard, and A. Roychoudhury,                           scheme for solving hard SMT-instances over bit-vectors,” arXiv preprint
     “Lemma discovery in agentic program verification,” arXiv preprint                 arXiv:2008.10061, 2020.
     arXiv:2603.22114, 2026.                                                      [28] J. Li, X. Xiao, Y. Zhang, C. Liu, L. Zhao, X. Liao, Y. Ji, J. Wang, J. Gu,
 [6] C. Yang, X. Li, M. R. H. Misu, J. Yao, W. Cui, Y. Gong, C. Hawblitzel,            Y. Ge, W. Xu, X. Fang, X. Xu, T. Zhao, Y. Kim, T. Wang, J. Hamm,
     S. K. Lahiri, J. R. Lorch, S. Lu, F. Yang, Z. Zhou, and S. Lu, “AutoVerus:        S. Krishnaswamy, J. Huan, and C. K. Reddy, “Agent harness engineer-
     Automated proof generation for Rust code,” Proceedings of the ACM on              ing: A survey,” https://openreview.net/pdf?id=eONq7FdiHa, 2026.
     Programming Languages, vol. 9, no. OOPSLA2, pp. 3454–3482, 2025.             [29] D. Beyer and J. Strejček, “Improvements in software verification and
 [7] Y. Liu, X. Wan, Y. Wang, M. Wang, L. Huang, and T. Wei, “KVerus:                  witness validation: SV-COMP 2025,” in Tools and Algorithms for the
     Scalable and resilient formal verification proof generation for Rust              Construction and Analysis of Systems, ser. Lecture Notes in Computer
     code,” arXiv preprint arXiv:2605.03822, 2026.                                     Science, vol. 15698. Springer, 2025, pp. 151–186.
 [8] K. R. M. Leino and C. Pit-Claudel, “Trigger selection strategies to          [30] SV-COMP 2026 Organizers, “SV-COMP 2026 results verification,”
     stabilize program verifiers,” in Computer Aided Verification, ser. Lecture        https://sv-comp.sosy-lab.org/2026/results/results-verified/, 2026.
     Notes in Computer Science, vol. 9779. Springer, 2016, pp. 361–381.           [31] D. Beyer and M. E. Keremoglu, “CPAchecker: A tool for configurable
 [9] Y. Zhou, J. Bosamiya, J. G. Li, M. J. H. Heule, and B. Parno, “Context            software verification,” in Computer Aided Verification, ser. Lecture Notes
     pruning for more robust SMT-based program verification,” in Formal                in Computer Science, vol. 6806. Springer, 2011, pp. 184–190.
     Methods in Computer-Aided Design. TU Wien Academic Press, 2024,              [32] K. Pei, D. Bieber, K. Shi, C. Sutton, and P. Yin, “Can large language
     pp. 59–69.                                                                        models reason about program invariants?” in Proceedings of the 40th
[10] C. Barrett, P. Fontaine, S. Ranise, and C. Tinelli, “The                          International Conference on Machine Learning, ser. Proceedings of
     SMT-LIB theory of fixed-size bit-vectors,” https://smt-lib.org/                   Machine Learning Research, vol. 202. PMLR, 2023, pp. 27 496–27 520.
     theories-FixedSizeBitVectors.shtml, 2025.                                         [Online]. Available: https://proceedings.mlr.press/v202/pei23a.html
[11] D. Jovanović, “Solving nonlinear integer arithmetic with MCSAT,” in         [33] A. Kamath, A. Senthilnathan, S. Chakraborty, P. Deligiannis, S. K.
     Verification, Model Checking, and Abstract Interpretation, ser. Lecture           Lahiri, A. Lal, A. Rastogi, S. Roy, and R. Sharma, “Finding in-
     Notes in Computer Science, vol. 10145. Springer, 2017, pp. 330–346.               ductive loop invariants using large language models,” arXiv preprint
[12] P. Backeman, P. Rümmer, and A. Zeljić, “Interpolating bit-vector for-           arXiv:2311.07948, 2023.
     mulas using uninterpreted predicates and Presburger arithmetic,” Formal      [34] S. Chakraborty, S. K. Lahiri, S. Fakhoury, M. Musuvathi, A. Lal,
     Methods in System Design, vol. 57, no. 2, pp. 121–156, 2021.                      A. Rastogi, A. Senthilnathan, R. Sharma, and N. Swamy, “Ranking
[13] R. W. Floyd, “Assigning meanings to programs,” in Mathematical                    LLM-generated loop invariants for program verification,” in Findings
     Aspects of Computer Science, ser. Proceedings of Symposia in Applied              of the Association for Computational Linguistics: EMNLP 2023.
     Mathematics, J. T. Schwartz, Ed. American Mathematical Society,                   Singapore: Association for Computational Linguistics, Dec. 2023,
     1967, vol. 19, pp. 19–32.                                                         pp. 9164–9175. [Online]. Available: https://aclanthology.org/2023.
                                                                                       findings-emnlp.614/
[14] C. A. R. Hoare, “An axiomatic basis for computer programming,”
                                                                                  [35] G. Wu, W. Cao, Y. Yao, H. Wei, T. Chen, and X. Ma, “LLM meets
     Communications of the ACM, vol. 12, no. 10, pp. 576–580, 1969.
                                                                                       bounded model checking: Neuro-symbolic loop invariant inference,”
[15] E. W. Dijkstra, “Guarded commands, nondeterminacy and formal deriva-              in Proceedings of the 39th IEEE/ACM International Conference on
     tion of programs,” Communications of the ACM, vol. 18, no. 8, pp.                 Automated Software Engineering, ser. ASE ’24, 2024, pp. 406–417.
     453–457, 1975.
                                                                                  [36] A. Wei, T. Sun, T. Suresh, H. Wu, K. Wang, and A. Aiken, “Quokka:
[16] F. Kirchner, N. Kosmatov, V. Prevosto, J. Signoles, and B. Yakobowski,            Accelerating program verification with LLMs via invariant synthesis,”
     “Frama-C: A software analysis perspective,” Formal Aspects of Com-                arXiv preprint arXiv:2509.21629, 2025.
     puting, vol. 27, no. 3, pp. 573–609, 2015.                                   [37] P. Mukherjee and B. Delaware, “Towards automated verification of
[17] P. Baudin, J.-C. Filliâtre, C. Marché, B. Monate, Y. Moy, and V. Pre-           LLM-synthesized C programs,” arXiv preprint arXiv:2410.14835, 2024.
     vosto, ACSL: ANSI/ISO C Specification Language. Preliminary Design,          [38] A. Q. Jiang, S. Welleck, J. P. Zhou, T. Lacroix, J. Liu, W. Li,
     version 1.4, 2008, https://www.frama-c.com/html/acsl.html.                        M. Jamnik, G. Lample, and Y. Wu, “Draft, sketch, and prove:
[18] J.-C. Filliâtre and A. Paskevich, “Why3 — where programs meet                    Guiding formal theorem provers with informal proofs,” in The Eleventh
     provers,” in Programming Languages and Systems, ser. Lecture Notes                International Conference on Learning Representations, 2023. [Online].
     in Computer Science, vol. 7792. Springer, 2013, pp. 125–128.                      Available: https://openreview.net/forum?id=SMa9EAovKMC
[19] C. Barrett, A. Stump, and C. Tinelli, “The SMT-LIB standard: Version         [39] E. First, M. N. Rabe, T. Ringer, and Y. Brun, “Baldur: Whole-proof
     2.0,” Department of Computer Science, The University of Iowa,                     generation and repair with large language models,” in Proceedings of
     Tech. Rep., 2010, release: December 21, 2010. [Online]. Available:                the 31st ACM Joint European Software Engineering Conference and
     https://smt-lib.org/papers/smt-lib-reference-v2.0-r10.12.21.pdf                   Symposium on the Foundations of Software Engineering, ser. ESEC/FSE
[20] L. de Moura and N. Bjørner, “Z3: An efficient SMT solver,” in Tools and           ’23, 2023, pp. 1229–1241.
     Algorithms for the Construction and Analysis of Systems, ser. Lecture        [40] K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil,
     Notes in Computer Science, vol. 4963. Springer, 2008, pp. 337–340.                R. J. Prenger, and A. Anandkumar, “LeanDojo: Theorem proving
[21] B. Dutertre and L. de Moura, “A fast linear-arithmetic solver for                 with retrieval-augmented language models,” in Advances in Neural
     DPLL(T),” in Computer Aided Verification, ser. Lecture Notes in Com-              Information Processing Systems, vol. 36, 2023, pp. 21 573–21 612.
     puter Science, vol. 4144. Springer, 2006, pp. 81–94.                              [Online].     Available:     https://papers.nips.cc/paper files/paper/2023/
     hash/4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets and
     Benchmarks.html
[41] A. Thakur, G. Tsoukalas, Y. Wen, J. Xin, and S. Chaudhuri,
     “An in-context learning agent for formal theorem-proving,” in
     First Conference on Language Modeling, 2024. [Online]. Available:
     https://openreview.net/forum?id=V7HRrxXUhN
[42] K. Lv, Y. Dong, R. Han, F. Jia, F. Ma, and J. Zhang, “LLM-
     guided quantified SMT solving over uninterpreted functions,” in
     Proceedings of the AAAI Conference on Artificial Intelligence,
     vol. 40, no. 17, 2026, pp. 14 304–14 312. [Online]. Available:
     https://ojs.aaai.org/index.php/AAAI/article/view/38445
[43] W. Feng, S. Shen, J. Liu, T. Chen, F. Song, and Z. Wu,
     “Can LLM aid in solving constraints with inductive definitions?”
     in Formal Methods – 27th International Symposium, FM 2026,
     Tokyo, Japan, May 18–22, 2026, Proceedings, Part II, ser. Lecture
     Notes in Computer Science, A. Sampaio and M. Stoelinga, Eds.,
     vol. 16557. Springer, 2026, pp. 111–132. [Online]. Available:
     https://doi.org/10.1007/978-3-032-26220-2 6
[44] D. Kroening, P. Schrammel, and M. Tautschnig, “CBMC: The C
     bounded model checker,” 2023. [Online]. Available: https://arxiv.org/
     abs/2302.02384
[45] C. Cadar, D. Dunbar, and D. Engler, “KLEE: Unassisted and automatic
     generation of high-coverage tests for complex systems programs,” in
     Proceedings of the 8th USENIX Symposium on Operating Systems
     Design and Implementation, ser. OSDI ’08, 2008, pp. 209–224.
[46] The dafny-lang community, “Dafny reference manual,” https://dafny.org/
     dafny/DafnyRef/DafnyRef, 2026, accessed: 2026-07-01.
