                                           C ON V ER: Using Contracts and Loop Invariant
                                         Synthesis for Scalable Formal Software Verification
                                                   Muhammad A. A. Pirzada*                            Weiqi Wang*                       Yiannis Charalambous*
                                                    The University of Manchester               The University of Manchester           The University of Manchester
                                                         Manchester, UK                             Manchester, UK                         Manchester, UK
                                                       0009-0005-2440-7547                        0009-0005-8247-5994                    0009-0000-5755-5099

                                                                         Konstantin Korovin                                   Lucas C. Cordeiro
                                                                    The University of Manchester                        The University of Manchester
                                                                          Manchester, UK                                     Manchester, UK
arXiv:2605.27051v1 [cs.SE] 26 May 2026




                                                                       0000-0002-0740-621X                                 0000-0002-6235-4272



                                            Abstract—Formal verification of large C programs is impeded       function contracts by hand is expert-intensive and poorly
                                         by state-space explosion: Bounded Model Checking (BMC) tools         adopted in practice; even well-resourced projects such as
                                         must encode the entire state space up to the predetermined           AWS’s s2n-tls [2] require dedicated annotation effort from
                                         bound by unrolling all nested constructs. We present C ON V ER,
                                         a top-down compositional verification tool. Given a C program        verification engineers. The result is that formal verification
                                         with a top-level assertion, C ON V ER decomposes verification top-   remains largely inaccessible for programs exceeding a few
                                         down: it uses a large language model (LLM) to synthesise             hundred lines.
                                         function contracts from the system property, then alternates            C ON V ER addresses this gap by combining two complemen-
                                         system-level and function-level checks in a CEGAR-CEGIS loop,        tary ideas. First, it adopts a top-down property decomposition
                                         refining contracts whenever a check fails via SMART ICE
                                         learning. We evaluate C ON V ER on four benchmark suites of          strategy: rather than starting from individual function specifi-
                                         increasing difficulty and against other state-of-the-art (SOTA)      cations and building upward, it begins with an abstract system-
                                         tools. On the Frama-C benchmark of 45 simple C programs,             level assertion in main() and derives function contracts suf-
                                         C ON V ER achieves 82–96% verification success across three LLM      ficient to prove that property. This top-down view minimises
                                         backends, with 93–95% of converged programs requiring only a         the specification burden as contracts need to only capture what
                                         single CEGAR-CEGIS iteration. On the X.509 parser benchmark
                                         (6 programs) and LF2C-Simple suite (17 programs), C ON V ER          the system property requires, not every semantic property of
                                         achieves 33–50% and 82–88% success respectively. On the              the underlying function. Second, C ON V ER automates con-
                                         VerifyThis suite of 11 recursive and loop-intensive programs, the    tract synthesis and refinement with Large Language Models
                                         Pre-Abstraction strategy achieves 55–64% success. In addition,       (LLMs). An LLM proposes initial contracts; a software verifi-
                                         we present ESBMC-LF a preprocessor tool that converts LF             cation tool then checks them at the system level (by replacing
                                         models to C while preserving the properties of the LF files,
                                         enabling C ON V ER to verify them. We transpile the LF Verifier      calls with contract stubs) and at the function level (by verifying
                                         Benchmarks using ESBMC-LF to C; we denote those LF-Hard.             each implementation against its contract). Failures are then
                                         We show that C ON V ER successfully verifies 67% of LF-Hard          fed back to the LLM as structured counterexamples through a
                                         benchmarks overall.                                                  Counterexample Guided Abstraction Refinement (CEGAR) [4]
                                            Index Terms—Formal Verification, Compositional Verification,      loop augmented with SMART Implication Counterexamples
                                         Contract Synthesis, Large Language Models, CEGAR, CEGIS
                                                                                                              (ICE) learning [5], which classifies each counterexample into
                                                               I. I NTRODUCTION                               positive, negative, and implication examples to guide targeted
                                                                                                              refinement. C ON V ER uses ESBMC for software verification.
                                            Verifying the correctness of large C programs is one of the
                                                                                                                    a) Contributions.: The main contributions of this paper
                                         central challenges in software engineering and formal verifi-
                                                                                                              are:
                                         cation. BMC tools such as the Efficient SMT-based Context-
                                                                                                                 1) Top-down contract derivation. A methodology that
                                         Bounded Model Checker (ESBMC) [1] and C Bounded Model
                                                                                                                     derives function contracts directly from a system-level
                                         Checker (CBMC) [2] are highly effective on self-contained
                                                                                                                     assertion, minimising manual specification effort.
                                         functions and small-scale models, but their complexity grows
                                                                                                                 2) CEGAR with SMART ICE learning. An iterative
                                         rapidly with program size: every function call adds to the
                                                                                                                     refinement loop that classifies ESBMC counterexamples
                                         state space that the underlying SMT solver must explore,
                                                                                                                     into positive, negative, and implication examples to
                                         and every loop requires unrolling up to a max bound. These
                                                                                                                     guide targeted LLM re-synthesis.
                                         contribute to the well-known state explosion problem in soft-
                                                                                                                 3) Loop invariant synthesis. An on-demand inductive
                                         ware model checking [3]. The standard method of writing
                                                                                                                     invariant generation step for functions where bounded
                                           * These authors contributed equally to this work.                         checking is insufficient, integrated seamlessly into the
                                                                                simplifies the SMT equation and focuses on encoding
                                                                                only the model to be verified. Making the verification
                                                                                process simpler. Used as a Preprocessor tool to enable
                                                                                C ON V ER to verify LF benchmarks.
                                                                             We investigate three research questions throughout the pa-
                                                                           per.

                                                                             RQ1

                                                                           How effectively does C ON V ER verify programs across
                                                                           diverse benchmarks, and how does performance compare
                                                                           across three LLM backends?


                                                                             RQ2

                                                                           Under what conditions does SMART ICE learning im-
                                                                           prove convergence, and how does the quality of coun-
                                                                           terexample feedback interact with LLM capability?



                                                                             RQ3

                                                                           How does C ON V ER scale to larger, structurally complex
                                                                           programs?

                                                                              The remainder of the paper is organised as follows. Sec-
                                                                           tion II covers background and Section III covers similar re-
                                                                           search to C ON V ER. Section IV presents the C ON V ER method-
                                                                           ology. Section V presents the benchmarks that C ON V ER
                                                                           will be tested on, along with the ESBMC-LF preprocessor.
                                                                           Section VI reports experimental results. Section VII discusses
                                                                           findings and threats to validity. Section VIII discusses conclu-
Fig. 1. The C ON V ER verification pipeline. The LLM derives function
contracts top-down from the system property; the CEGAR loop alternates
                                                                           sions from the research.
system-level and function-level ESBMC checks, refining contracts via ICE
learning until both levels pass.                                                                 II. BACKGROUND
                                                                                 a) Bounded Model Checking (BMC): [6], [7] verifies
                                                                           program correctness by unrolling loops up to a bound k and
     Counterexample Guided Inductive Synthesis (CEGIS)                     encoding the resulting acyclic program as an SMT formula: a
     loop.                                                                 satisfying assignment corresponds to a counterexample, while
  4) End-to-end evaluation. An empirical study across four                 unsatisfiability proves correctness up to bound k. ESBMC [1],
     benchmarks: the Frama-C benchmark (45 programs, 82–                   [8]–[10] is a mature BMC tool that supports C/C++ with rich
     96% success), LF2C-Simple (17 programs, 82–88%),                      arithmetic and pointer reasoning. The fundamental limitation
     X.509 parser programs (6 programs, 33–50%), and Ver-                  of BMC is state space explosion: for large programs with many
     ifyThis recursive/loop-intensive programs (11 programs,               functions and deep call stacks, the SMT instance grows rapidly
     55–64%), covering diverse program structures and ver-                 and solver time increases rapidly. Function contracts are the
     ification challenges.                                                 standard mitigation technique. Once a function is verified
  5) ESBMC-LF. A prototype preprocessor transpilation tool                 against its contract, the contract replaces the implementation
     used to convert Lingua Franca (LF) benchmarks to C-                   in all calling contexts, preventing the solver from re-exploring
     based models, for verification with tools that work on                the function’s internals.
     the C programming language. Created for LF-Hard,                            b) Large Language Models.: Recent work demonstrates
     comprising 24 LF Benchmarks that are converted into a                 that LLMs can reason effectively about code structure and
     monolithic C version. With the operational models of the              semantics [11]–[16]. LLMs have been applied to test gener-
     LF Reactor replacing the implementation, this therefore               ation, bug finding, and program synthesis, and more recently
to formal specification tasks such as precondition and post-       verifiers due to state explosion. The verification happens at the
condition derivation [17], [18] C ON V ER uses LLMs solely for     following levels:
contract and invariant synthesis for proposing candidate formal       • At the system level (Step 3), every function call is
annotations, but delegates verification decisions to ESBMC,              replaced by a contract: ESBMC checks whether the
making the verification sound. This separation ensures that              system assertion holds assuming each function satisfies its
soundness depends only on the model checker, not on the                  postcondition, without exploring any function internals.
LLM’s output.                                                         • At the function level (Step 4), each implementation is
                                                                         checked against its own contract in isolation: ESBMC
                    III. R ELATED W ORK                                  assumes the precondition holds and asserts the postcon-
      a) PolyVer: Many real-world software systems are poly-             dition after execution, verifying the actual source code of
glot: their components are implemented in different pro-                 that function.
gramming languages, yet traditional verifiers target a sin-        Algorithm 1 Overview of C ON V ER
gle language, making whole-system verification challenging.
                                                                   Require: Program P , complexity threshold τ , max iterations
PolyVer [17] addresses this by combining abstraction, com-
                                                                       K
positional reasoning, and contract synthesis to verify poly-
                                                                   Ensure: Verified ⊤ or Falsified ⊥
glot systems. The system is modelled as a transition system
                                                                    1: Step 1 — Derive Sets
whose components may be coded in different languages (e.g.,
                                                                    2: φ ← E XTRACT P ROPERTY(P )
C or Rust); PolyVer connects a top-level model checker
                                                                    3: F ← E XTRACT F UNCTIONS(P ) \ { MAIN}
(UCLID5 [19]) with language-specific back-ends (CBMC for
                                                                    4: FL = {f ∈ F | σ(f ) < τ }      ▷ Low complexity functions
C, Kani for Rust) via automatically synthesised precondition/-
                                                                       FH = {f ∈ F | σ(f ) ≥ τ } ▷ High complexity functions
postcondition contracts at each language boundary. C ON V ER
                                                                    5: Step 2 — Preprocessing         ▷ Run if Pre-Abstraction is
is thematically related: both tools decompose cross-component
                                                                       enabled
verification through contracts, but C ON V ER operates within
                                                                    6: CL ← S YNTHESIZE (FL , φ) ▷ Simple; can verify directly
a single language (C) and automates contract synthesis via
                                                                    7: CH ← OVERAPPROXIMATE(FH , φ)            ▷ State explosion;
LLMs rather than requiring manual annotation. Additionally,
                                                                       too complex to verify directly
C ON V ER uses ESBMC-LF to create C-based models of LF
                                                                    8: C ← CL ∪ CH
benchmarks to automatically verify them.
                                                                    9: Step 3 — System-Level Verification
      b) ACSE:       Array-Carrying     Symbolic     Execution     10: VS ← V ERIFY S YSTEM (P, C)
(ACSE) [20] automates function contract generation for             11: Step 4 — Function-Level Verification
array-manipulating C programs via a symbolic execution             12: Vf ← V ERIFY F UNCTION (P, C, f )         ▷ For all f ∈ F
framework that carries invariants and contiguous array             13: if PASS(VS ) ∧ ∀f ∈ F : PASS(Vf ) then
segments along execution paths. ACSE propagates loop               14:    return ⊤         ▷ Contracts correct without refinement
invariants from external generators, handles disjunctive loop      15: end if
exits, and merges or splits array segments to synthesise           16: Step 5 — Contract Replacement and System Verifica-
precise ACSL pre/postconditions and assigns clauses, which             tion
are then discharged by Frama-C’s WP plugin. C ON V ER              17: C ← {Cf ∈ C | PASS(Vf )} ▷ Drop contracts that failed
is complementary: both tools target automated contract                 function-level verification
synthesis, but ACSE derives contracts analytically in a            18: VS ← V ERIFY S YSTEM (P, C)       ▷ Verify using surviving
single symbolic pass and crucially supports quantified                 contracts
array invariants (e.g., ∀i. a[i] ≥ 0) that ESBMC’s contract        19: Step 6 — CEGAR Refinement
mechanism cannot express. C ON V ER instead synthesises            20: ⟨C, VS , VF ⟩ ← CEGAR(C, VS , VF , K)         ▷ See Alg. 2
contracts via LLMs and iteratively refines them against            21: if PASS(VS ) ∧ ∀v ∈ VF : PASS(v) then
formal counterexamples in a CEGAR/CEGIS loop, handling             22:    return ⊤
cases where symbolic invariant inference is imprecise or the       23: end if
program is too large for exhaustive symbolic exploration.          24: Step 7 — CEGIS Escalation
                                                                   25: ⟨C, VS , VF ⟩ ← CEGIS(C, VS , VF , K)         ▷ See Alg. 3
                    IV. M ETHODOLOGY                               26: if PASS(VS ) ∧ ∀v ∈ VF : PASS(v) then
   This Section will describe the functionality behind C ON V ER   27:    return ⊤
and provide an overview of the function contract and loop          28: end if
invariant integration. Algorithm 1 covers how C ON V ER works.     29: return ⊥
C ON V ER verifies a C program compositionally by decompos-
ing its top-level system property into per-function contracts         ConVer uses a two-stage refinement strategy. Both stages
that are independently checkable by a formal verification tool.    verify contracts at the system level (proving the property
This abstraction of the state space enables verification of        holds assuming contracts — Step 3) and the function level
programs larger than would be possible with traditional formal     (proving each implementation satisfies its contract — Step
    4). The CEGAR loop first attempts to refine contracts using         reduces to the standard Hoare triple {P } f {Q}, which is
    LLM-guided counterexample analysis (Step 5). If CEGAR               precisely what ESBMC discharges during Enforce mode. A
    stagnates, a variant of Delta Debugging [21], [22] is used as a     function that passes this check is contract-conformant. When
    stagnation breaker by incrementally removing post-condition         both checks pass, soundness follows by substitution: because
    clauses from stagnating functions, reverifies said function until   the real implementation satisfies (2), any property ϕ proved
    the verification passes, then pipeline escalates to CEGIS (Step     against the stub in Replace mode holds for the real code as
    7). CEGIS performs constraint-based synthesis against accu-         well, and the composed result is end-to-end sound.
    mulated positive and negative examples. LLMs are integrated               b) Loop Invariants.: For programs containing loops,
    into both loops to facilitate contract generation.                  ESBMC supports the annotation of loop invariants via
                                                                        __ESBMC_loop_invariant() [23]. Unlike function con-
    A. ESBMC Function Contract and Loop Invariant Checker
                                                                        tracts, which rely on deduction, loop invariants establish
       ESBMC [1] supports modular verification through two              correctness through induction: a predicate is shown to hold
    complementary mechanisms: function contracts and loop               before the loop begins, to be preserved by each iteration, and
    invariants. Function contracts support deductive reasoning          to imply the desired postcondition upon termination. Consider
    —deriving postconditions from preconditions without re-             the following example:
    examining the function body—while loop invariants support
    inductive reasoning, establishing correctness for unbounded1        int sum = 0;
    loops through a fixed base case and preservation argument.2         for (int i = 0; i < n; i++) {
    Together, they form the verification backbone of C ON V ER,3            __ESBMC_loop_invariant(sum == i * (i
    enabling large-scale verification tasks to be decomposed into              - 1) / 2);
    independently checkable units.                                4         sum += i;
          a) Function Contracts.: A function contract for a func-5      }
    tion f is a triple (P, Q, S), where P : State → B is the
                                                                                                    i(i−1)
    precondition, Q : State × State → B is the postcondition              The invariant sum =          2     is verified inductively by
    relating pre- and post-states, and S ⊆ Vars is the assigns set      ESBMC in three steps:
    of locations f is permitted to modify. In ESBMC these are             1) Base case: the invariant holds at i = 0, since sum =
    expressed via __ESBMC_requires, __ESBMC_ensures,                         0 = 0·(−1)  .
                                                                                     2
    and __ESBMC_assigns. A simple example is shown below:                 2) Inductive step: assuming the invariant holds at iteration i,
1   int increment(int x) {                                                   after executing sum += i, we obtain sum′ = i(i−1)    2   +
                                                                                  i(i+1)                                   ′
2       __ESBMC_requires(x > 0);                                             i = 2 , which matches the invariant at i = i + 1.
3       __ESBMC_assigns(x);                                               3) Conclusion: when the loop exits at i = n, the invariant
4       __ESBMC_ensures(__ESBMC_return_value                                 yields sum = n(n−1)2  .
           > x);
5       return x + 1;
6   }                                                                   This reduces an otherwise unbounded verification problem
                                                                        to a fixed inductive argument, avoiding loop unrolling
    Given that P holds at a call site, ESBMC deduces that Q             entirely and sidestepping the state space explosion that
    holds upon return without re-examining the body; verification       would otherwise arise for large or non-terminating loops
    proceeds as assume(P ) → execute(f ) → assert(Q).                   [24].
    Once f is verified to satisfy (P, Q, S), the contract replaces
    the implementation in any calling context.
       Function contracts serve two distinct roles in C ON V ER. In     B. CEGAR+CEGIS
    system-level verification (Replace mode), each call to f is               a) Counterexample-Guided Abstraction Refinement (CE-
    substituted with an abstract stub                                   GAR): [4] drives the primary refinement loop in C ON V ER.
                                                                        Starting from LLM-derived contracts, each iteration runs two
              abs(P, Q, s0 ) = { s | P (s0 ) ∧ Q(s0 , s) },      (1)
                                                                        ESBMC checks: System-Level verification (function calls re-
    which havocs only the declared assigns targets and assumes          placed by abstract contract stubs) and Function-Level veri-
    Q; the internal state space is never explored. In function-         fication (each implementation checked against its contract).
    level verification (Enforce mode), the real implementation is       If both pass, verification is sound by the assume-guarantee
    checked against (P, Q, S) by assuming P and asserting Q after       rule [25]. Otherwise, the counterexample is fed back to the
    execution. Enforce mode establishes the contract-conformance        LLM for contract refinement. Function-level failures direct
    condition                                                           the LLM to relax contracts; system-level failures direct it to
                                                                        strengthen them — reflecting that the two levels pull contracts
              ∀s0 . P (s0 ) ⇒ Jf K(s0 ) ∈ abs(P, Q, s0 ),        (2)
                                                                        in opposite directions. CEGAR runs for up to five iterations
    i.e., the concrete execution trace of f is a witness in the         before escalating. An overview of CEGAR used in C ON V ER
    abstract state set defined by the stub. Expanding (1) into (2)      can be seen in Algorithm 2.
Algorithm 2 CEGAR Refinement in C ON V ER                         states that must be excluded, and implication examples encod-
Require: Contracts C, results VS , VF , max iterations K          ing inductive relationships between states. Conflict detection
Ensure: Refined ⟨C, VS , VF ⟩                                     identifies when a counterexample contradicts existing positive
 1: for k = 1 to K do                                             examples, keeping the database consistent. When ESBMC
 2:   C ← C OUNTEREXAMPLE R EFINE(C, VS , VF )                    reports a failure, the raw output is parsed to extract the violated
 3:   VS ← V ERIFY S YSTEM(P, C)                                  property and execution trace; tool-level failures are separated
 4:   Vf ← V ERIFY F UNCTION(P, C, f ) for all f ∈ F              from semantic counterexamples, which are further classified
 5:   if PASS(VS ) ∧ ∀v ∈ VF : PASS(v) then                       into five categories — only unconstrained and semantic vi-
 6:      return ⟨C, VS , VF ⟩                                     olations are admitted into E − , keeping the database free of
 7:   end if                                                      noise.
 8:   if S TAGNANT(k) then
 9:      C ← D ELTA D EBUG(C)                                     Algorithm 4 Counterexample Handling Pipeline - SMART
10:      break                ▷ Escalate to CEGIS — Step 7        ICE
11:   end if                                                      Require: Raw ESBMC output, current contracts, ICE
12: end for                                                            database
13: return ⟨C, VS , VF ⟩                                          Ensure: Updated E + /E − /implications, weakest-link function
                                                                    1: Parse output: extract violated property, trace, key variables
                                                                    2: if tool-level failure (timeout / internal error / parse rejec-
                                                                       tion) then
     b) Counterexample-Guided Inductive Synthesis (CEGIS):
                                                                    3:    Record separately; exit
 [26] serves as a second-stage fallback when CEGAR exhausts
                                                                    4: end if
its budget. Counterexamples are classified and accumulated
                                                                    5: Classify into: syntax error, unparsed, tool error, uncon-
in a constraint database tracking positive examples (passing
                                                                       strained init, semantic
configurations), negative examples (states that must not sat-
                                                                    6: if semantic or unconstrained initialisation then
isfy the contract), and implication examples (inferred from
                                                                    7:    Admit into E −
observed program behaviour and structural patterns in the
                                                                    8: end if
function body). Each synthesis call is conditioned on the full,
                                                                    9: if system-level failure then
accumulated constraint set, guiding the LLM toward contracts
                                                                   10:    Map variables → responsible functions
that are consistent with all observed behaviour. This loop
                                                                   11:    Compute gap score per function
also runs for up to five iterations; if the combined budget
                                                                   12:    Flag the highest-gap function as the weakest link
of up to ten iterations across both stages is exhausted without
                                                                   13: end if
convergence, verification is declared inconclusive. Algorithm 3
                                                                   14: Render structured diagnostic block (trace + E + /E − anal-
describes how C ON V ER uses CEGIS.
                                                                       ysis) for LLM prompt
Algorithm 3 CEGIS Escalation in C ON V ER
Require: Contracts C, results VS , VF , max iterations K
Ensure: Refined ⟨C, VS , VF ⟩                                     D. Pre-abstraction
 1: D ← CEGISDATABASE(VF )                          ▷ Migrate        The pre-abstraction phase addresses the scalability limita-
    counterexamples from CEGAR                                    tion of compositional verification: certain functions exhibit
 2: for k = 1 to K do                                             structural complexity sufficient to trigger state explosion even
 3:   C ← E XAMPLE S YNTHESIZE(C, D)          ▷ Using Oracle      at the function level. C ON V ER assigns each domain function
 4:   VS ← V ERIFY S YSTEM(P, C)                                  a complexity score which is a weighted sum of static metrics
 5:   Vf ← V ERIFY F UNCTION(P, C, f ) for all f ∈ F              extracted by regex analysis of the function body following es-
 6:   if PASS(VS ) ∧ ∀v ∈ VF : PASS(v) then                       tablished complexity metrics [27]. The weights reflect the cost
 7:      return ⟨C, VS , VF ⟩                                     model of BMC: loop count and nesting depth carry the highest
 8:   end if                                                      per-occurrence weights because each iteration multiplies the
 9:   Update D with new E + , E − from VF                         path count. Recursion and unbounded loops incur large flat
10: end for                                                       penalties, as a single occurrence renders the state space po-
11: return ⟨C, VS , VF ⟩                                          tentially infinite. Dynamic allocation is penalised moderately
                                                                  (bounded by calling context); branching and pointer operations
                                                                  contribute smaller per-occurrence costs.
                                                                     The score maps each function to one of four explosion-risk
C. SMART ICE
                                                                  tiers: minimal (< 5.0), low (≥ 5.0), medium (≥ 10.0), and high
     a) ICE Learning.: C ON V ER structures verification feed-    (≥ 20.0). Functions in the medium or high tier (score ≥ 10.0,
back using the ICE framework [5], which classifies examples       configurable) are designated for over-approximate abstraction;
into three categories: positive examples (E + ) of states that    the rest undergo standard precise-contract synthesis. The LLM
must be included in the contract, negative examples (E − ) of     prompt for abstraction instructs the model to produce sound
but loose contracts: weaker postconditions (null-safety, range      as ESBMC verification constructs (__ESBMC_assert,
bounds) rather than full behavioural specifications, and an         __ESBMC_assume, and tracking variables) in the combined
over-approximate assigns clause covering all globals that           C file. Each MTL formula is pattern-matched to one of nine
might be modified. A heuristic fallback generates tautological      instrumentation templates that determine where assertions are
ensures clauses and a body-scan-derived assigns list                placed and whether tracking variables are needed.
when the LLM fails or produces unparseable output.                     Steps 6–7 generate a direct execution model that replaces
   The pipeline then proceeds through five phases:                  the reactor-c scheduler. The pipeline parses the output topol-
   • Phase 1a: Generate over-approximate abstractions for           ogy to build a cascade graph; a static map from each reaction’s
     high-complexity functions.                                     output port to its downstream reactions and emits direct
   • Phase 1b: Concurrently synthesise precise contracts for        function calls with is_present guards instead of runtime
     low-complexity functions via coverage-validated LLM            dispatch through trigger arrays. Loop bounds are derived from
     derivation.                                                    timer periods and property time horizons, yielding a finite,
   • Phase 2: Run an initial ESBMC system-level check using         fully unrollable execution loop. Dead runtime infrastructure is
     the abstractions as function summaries, yielding a fast        then stripped to reduce the symbolic state space.
     over-approximate verification result.
   • Phase 3: Verify each function atomically against its own
                                                                    Algorithm 5 ESBMC-LF: Converts LF files to C with verifi-
     contract (proceeds unconditionally, regardless of Phase 2      cation property preservation
     outcome).                                                      Require: LF Benchmark B
   • Phase 4: Replace each successfully verified abstraction        Ensure: C Program c file with property set Φ
     with its precise contract; unverified functions retain their    1: Step 1: Semantic LF-to-C translation
     conservative abstraction.                                       2: P ← C OMPILE LF(B)                                       ▷P
   • Phase 5: Escalate to CEGAR/CEGIS refinement if the                  is a C project semantically equivalent to B without MTL
     substituted contracts still fail to establish the system            properties assuming LFC tool performs sound conversion
     property.                                                       3: Step 2: Platform normalization
                                                                     4: P ′ ← N ORMALIZE P ROJECT (P )                     ▷ Resolve
   This stratified strategy — abstract first, verify atomically,
then refine — allows C ON V ER to handle programs that would             platform-dependent paths, headers, and definitions
                                                                     5: Step 3: Single translation unit construction
otherwise be intractable under a single-phase compositional
                                                                     6: C ← F LATTEN P ROJECT(P ′ , OM )          ▷ Replace runtime
approach.
                                                                         library with operational model OM , preprocess into one
                      V. B ENCHMARKS                                     translation unit, filter system headers
   This Section describes the benchmarks that C ON V ER veri-        7: Step 4: Property extraction
fies.                                                                8: Φ ← E XTRACT MTL(B, C)             ▷ Parse MTL annotations
                                                                         from B, map symbols to locations in C
A. ESBMC-LF and LF-Hard                                              9: Step 5: Property instrumentation
    To directly compare ConVer with tools that consume LF           10: C ′ ← I NSTRUMENT MTL(Φ, C)              ▷ Insert assertions,
files, such as work from [17] which uses the LF Ver-                     assumptions, and tracking variables per Φ
fifier Benchmarks [28], a purpose-built preprocessor tool           11: Step 6: Execution model generation
ESBMC-LF was created to convert the LF file benchmarks              12: C ′′ ← G EN E XEC M ODEL(C ′ )              ▷ Build cascade
to C. ESBMC-LF translates the LF files into C with the                   graph from output topology, replace scheduler dispatch
verification conditions included, described in Algorithm 5.              with direct calls, derive loop bounds
The purpose of the pipeline is to preserve the verification         13: Step 7: Post-processing
constructs of the LF benchmarks, which the LFC compiler             14: c file ← P OST P ROCESS(C ′′ )         ▷ Strip dead runtime
strips from the converted code to ensure the compiled program            code, fix preprocessor-baked constants, propagate action
runs efficiently. The resulting LF-Hard suite comprises 24 C             values, remove line directives
programs converted from the LF Verifier Benchmarks [28];            15: return c file
further discussed in Section V-B. The remainder of Sec-
tion V-A describes in further detail Algorithm 5.
    Steps 1–3 compile each LF benchmark to C via the LFC            B. Benchmark Suites
transpiler, normalize platform-dependent paths and compiler            We evaluate C ON V ER on four alternative benchmark suites
options, and combine all source files into a single translation     totalling 79 C programs, spanning algorithmic code, loop
unit. During combination, the reactor-c runtime library is          and recursion intensive verification challenges, and real-world
replaced with a verification-friendly operational model that        parsing routines.
stubs the scheduler, event queue, and token lifecycle, so that            a) LF2C-Simple (17 Programs).: These LF2C-Simple
ESBMC reasons only about the benchmark’s reaction logic.            Benchmarks were synthesised using Claude 3.5 Sonnet [29].
    Steps 4–5 extract the Metric Temporal Logic (MTL)               Where the LLM was prompted with the original LF Bench-
properties from the original LF source and encode them              mark with the explicit instruction to generate a semantically
equivalent C Program version with the system property in-                                        TABLE I
serted at the correct position inside the code. We successfully                            E XPERIMENTAL SETUP.
obtained 17 of the 24 benchmarks; the remainder contained
                                                                    Parameter                                     Value
buggy cases that led to Verification Failed due to a logic error
                                                                    ESBMC version                                 8.1.0
injected by the LLM, and we were unable to verify the system        LLM backends                                  Qwen3.5-Plus;
property.                                                                                                         Haiku    4.5;   GPT-
      b) Frama-C (45 programs).: Drawn from a Frama-                                                              OSS 120b
                                                                    Max iterations                                5
C/ACSL exercise set used to evaluate deductive verification         Timeout (Frama-C / Simple / X.509)            600 s
tools at FM 2026-AE [20], the suite covers numerical com-           Timeout (VerifyThis)                          900 s
putations, array operations, sorting, and searching (e.g., add,     Workers (cloud / local)                       3/1
sort, binary_search). Original ACSL annotations (//@
requires/ensures) are removed, and the same property
is re-expressed as a single top-level assert() in main().           u32 idx;
Programs are typically under 100 LOC, making this suite             __ESBMC_assume(idx < len);
                                                                    if (ret == 0) assert(buf[idx] <= 0x7f);
well-suited for evaluating the core CEGAR plus ICE contract
synthesis pipeline on well-structured algorithmic code without         ESBMC’s BMC engine explores all nondet values of idx,
structural interference.                                            making this encoding semantically equivalent to the universal
      c) VerifyThis        (11        programs).:        Drawn      quantifier within the bounded path. Ranging from single-
from      three    SV-COMP       [30]    categories    —      six   function leaf parsers to three-level call chains with pointer
from      the    VerifyThis    track    (lcp,     prefixsum,        arithmetic, this suite is substantially harder than the Frama-C
prefixsum_rec, duplets, elimination_max_rec,                        benchmark and probes whether C ON V ER’s CEGAR+ICE loop
elimination_max_rec_onepoint),                    two      from     can synthesise sound pointer contracts for low-level code.
recursive-simple (fibo, sum), and three from recursive
                                                                                           VI. E XPERIMENTS
(MultCommutative, EvenOdd, Addition) — the
programs are adapted by replacing dynamic memory allocation              a) Tool and hardware configuration.: All experiments
with fixed-size stack arrays and reducing verification bounds       use ESBMC 8.1.0 as the backend verifier and perform at
(e.g., n ≤ 8 for prefix sum, n ≤ 6 for elimination max)             most 5 CEGAR iterations per program. We evaluate three
to prevent state-space explosion. Four programs were                LLM backends: Qwen-Plus (DashScope cloud API), Claude
excluded: elimination_max has a monolithic main()                   Haiku 4.5 (Anthropic cloud API), and GPT-OSS 120b served
with no callee, and three tree-manipulation programs                locally via Ollama on a server with four NVIDIA RTX A6000
(tree_del_iter, tree_del_rec, tree_max) require                     GPUs (48 GB each). Table I summarises the parameters. For
heap-allocated structures with ∀-quantified postconditions          the Frama-C benchmark, LF2C-Simple, and X.509 we set a
unsupported by                                                      per-program timeout of 600 s and run three workers in parallel
__ESBMC_ensures. The suite is evaluated exclusively                 for cloud models (one for GPT-OSS 120b). For VerifyThis, we
with the Pre-Abstraction strategy, as loop-intensive programs       extend the timeout to 900 s to accommodate deeper recursion
cause state-space explosion under direct synthesis and              and loop complexity.
recursive programs exceed SmartICE’s capacity without prior              b) Strategies.: We compare two verification strategies:
abstraction.                                                        SmartICE applies the full CEGAR+SMART ICE pipeline with
      d) X.509 (6 programs).: Extracted from the ANSSI-FR           structured counterexample feedback, while No-ICE disables
x509-parser project and included in the same FM 2026                ICE learning and serves as an ablation baseline. Both strategies
artifact [20] as the Frama-C suite, these programs implement        are applicable to the Frama-C benchmark, LF2C-Simple, and
real-world ASN.1/X.509 routines: buffer comparison                  X.509, which consist of short programs with explicit function-
(bufs_differ), IA5 string validation                                call structure. For VerifyThis — programs with deep or
(check_ia5_string),               ASN.1       type      parsers     unbounded recursion that cause state explosion under direct
(parse_null,                                                        synthesis — we apply the Pre-Abstraction strategy exclusively.
parse_algoid_params_none), time-field encoding
                                                                    A. Results on Function-Contract Benchmarks (RQ1)
(time_components_to_comparable_u64),                         and
time field checking (verify_correct_time_use).                         Table II shows verification outcomes on Frama-C bench-
Three adaptations are applied for ESBMC compatibility:              mark (45 programs), LF2C-Simple (17 programs), and X509
(1) static qualifiers are removed (required for                     (6 programs) using the SmartICE strategy. Figure 3 provides
--enforce-contract to locate functions by name);                    a visual overview across all four benchmarks.
(2) ACSL assertions are replaced with C assert();                      C ON V ER achieves strong results on the Frama-C bench-
and (3) universal quantifiers are encoded via a nondet              mark: GPT-OSS 120b converges on 43 of 45 programs (96%),
index—e.g.,       \forall integer i; 0<=i<len ==>                   Qwen-Plus on 40 (89%), and Claude Haiku 4.5 on 37 (82%).
buf[i]<=0x7f becomes:                                               Across LF2C-Simple, which compiles the same LF programs
                                                                    into C and runs them through the same pipeline, results
                                  TABLE II                                                                                 Qwen-Plus benefits similarly (+1 program, 89% vs. 87%).
         V ERIFIED PROGRAMS (S MART ICE STRATEGY ) ON THE F RAMA -C                                                        Claude Haiku 4.5 tells a different story: it converges on
            BENCHMARK , LF2C-S IMPLE , AND X509. N UMBERS SHOW
       CONVERGED / TOTAL (%). Q WEN = Q WEN -P LUS ; C LAUDE = H AIKU 4.5;                                                 two fewer programs under SmartICE (37/45) than without it
                           GPT = GPT-OSS 120 B .                                                                           (39/45).
                                                                                                                              The divergence has a traceable cause. The value of an ICE
                            Benchmark                         Qwen           Claude          GPT-OSS                       database depends entirely on the informational quality of its
                            Frama-C (45)                    40 (89%)       37 (82%)          43 (96%)                      entries: a negative example is useful only if it captures a
                            LF2C-Simple (17)                14 (82%)       14 (82%)          15 (88%)                      genuine semantic property of the failed contract, not a surface
                            X509 (6)                         3 (50%)       3 (50%)            2 (33%)                      artefact of how the contract was written. For Claude Haiku 4.5,
                                                                                                                           two failure modes corrupt this signal. First, when the model
                                            FM2026 Benchmark Results 3 Models × 2 Strategies                               produces a syntactically ill-formed contract—such as using a
                       50
                                89%             87%            82%         87%         96%                91%              boolean literal in a context where ESBMC expects a C integer
                       40                                                                                                  expression—the resulting parse error is stored as a negative
                                                                                                                           example, and the ICE loop constrains subsequent refinement
Programs (out of 45)




                       30                                                                                                  away from that surface pattern. The model responds by pro-
                                                                                                                           ducing other malformed expressions rather than resolving the
                       20                                                                                                  underlying cause, trapping the loop until the iteration budget
                                                                                                                           expires. Second, when ESBMC emits counterexamples in a
                                                                                                 Converged (both levels)
                       10                                                                        System-only               format that ConVer’s parser cannot decode, those semantically
                                                                                                 Failed
                                                                                                 Timeout
                                                                                                 No-ICE (hatched)
                                                                                                                           empty entries populate the E− database and are presented
                       0                                                                                                   back to the model as though they carried structural meaning—
                             Qwen3.5-Plus    Qwen3.5-Plus    Haiku 4.5   Haiku 4.5    GPT-OSS           GPT-OSS
                              SmartICE         No-ICE        SmartICE     No-ICE      SmartICE           No-ICE
                                                                                                                           noise wearing the appearance of signal. Larger backends, by
Fig. 2. Outcome breakdown on Frama-C benchmark (45 programs) for three
                                                                                                                           contrast, generate syntactically well-formed contracts more
LLM backends and two strategies. Stacked bars show counts for converged                                                    reliably and elicit richer, more structured ESBMC witnesses,
(green), system-only (orange), failed (red), and timeout (grey).                                                           keeping their counterexample databases clean and the feedback
                                                                                                                           loop genuinely informative. ICE, in this light, functions as a
                                                                                                                           capability amplifier: it sharpens refinement precisely where
are consistent at 82–88%. The X509 benchmark is markedly
                                                                                                                           the LLM already generates high-quality artefacts, and offers
harder: these programs contain pointer-heavy certificate pars-
                                                                                                                           diminishing—or in the extreme, negative—returns where those
ing code, and the 33–50% convergence rate reflects the dif-
                                                                                                                           artefacts are noisier.
ficulty of generating sound pointer contracts for low-level
memory operations with current LLMs. Figure 2 breaks down                                                                  a) RQ2 — ICE learning contribution.: SMART ICE
outcomes (converged, system-only, failed, timeout) by model                                                                learning yields its strongest gains for the highest-
and strategy on the Frama-C benchmark.                                                                                     capability backend, lifting GPT-OSS 120b by five percent-
   The Frama-C benchmark results reveal a clear dominance of
                                                                                                                           age points (96% vs. 91%) and Qwen-Plus by two (89%
first-iteration convergence across all three models. For GPT-
                                                                                                                           vs. 87%). Claude Haiku 4.5, whose smaller capacity leads
OSS 120b, 40 of the 43 converged programs (93%) require
                                                                                                                           to more frequent contract syntax errors and less structured
only a single CEGAR iteration; the remaining three converge
                                                                                                                           ESBMC witnesses, does not benefit: its ICE database
at iteration 2. Figure 4 shows the full iteration distribution.
                                                                                                                           accumulates noise rather than signal, and the feedback
                                                                                                                           loop becomes counterproductive. The finding reframes the
        a) RQ1 — Verification effectiveness.: C ON V ER achieves                                                           role of ICE: rather than a uniform improvement over
        82–96% on Frama-C benchmark and LF2C-Simple, with                                                                  pure CEGAR, it is a capability-conditioned amplifier—
        a narrow spread across three backends, suggesting the                                                              most valuable precisely where the LLM is already strong
        CEGAR+ICE loop is largely model-agnostic for well-                                                                 enough to generate artefacts from which structured feed-
        structured algorithmic programs. X509 (33–50%) is the                                                              back can be meaningfully extracted.
        outlier: pointer-heavy certificate parsing exposes a gap
        in current LLM contract synthesis for low-level memory
        code that no backend closes.                                                                                       C. Results on Complex Programs (RQ3)
                                                                                                                              LF-Hard Benchmarks (24 programs): Table III shows re-
B. ICE Learning Ablation (RQ2)                                                                                             sults on the 24 LF-Hard benchmarks (1,998–4,328 LOC each)
   To isolate the contribution of SMART ICE learning, we                                                                   under the Pre-Abstraction strategy with a 600 s budget. Fig-
compare SmartICE and No-ICE on the Frama-C benchmark                                                                       ure 6 visualises the outcome breakdown.
for all three backends. Figure 5 visualises the comparison.                                                                   Direct ESBMC without contracts verifies 10 of 24 programs
   The ablation reveals a picture more nuanced than a simple                                                               within budget, providing a baseline: these are already simpli-
verdict on ICE. GPT-OSS 120b gains the most from structured                                                                fied C translations of LF reactor models that ESBMC can
counterexample feedback (+2 programs, 96% vs. 91%), and                                                                    handle monolithically. C ON V ER improves on this across all
                                                                                 ConVer Benchmark Overview (best strategy per benchmark type)
                                                                                                                                                                                                               100
                      Qwen3.5-Plus                                   40/45                          14/17                      3/6                               6/11                      11/24
                                                                    SmartICE                       SmartICE                  SmartICE                           Preabs                    Preabs               80




                                                                                                                                                                                                                    Convergence rate (%)
                                                                                                                                                                                                               60
                                      Haiku 4.5                      37/45                          14/17                      3/6                               7/11                      12/24
                                                                    SmartICE                       SmartICE                  SmartICE                           Preabs                    Preabs
                                                                                                                                                                                                               40

               GPT-OSS 120b                                          43/45                          15/17                      2/6                               6/11                      15/24               20
                                                                    SmartICE                       SmartICE                  SmartICE                           Preabs                    Preabs

                                                                                                                                                                                                               0
                                                                    Frama-C                      LF2C-Simple                      X.509                        VerifyThis                 LF-Hard
                                                                      (45)                            (17)strategy
                                                                                                SmartICE                           (6)                           (11)     Preabs strategy   (24)

Fig. 3. Verification success rate (%) across all four benchmarks and three LLM backends. Each cell shows the convergence percentage under the best
applicable strategy for that benchmark.

                                                                         CEGAR Iteration Distribution FM2026, SmartICE
                                                 Qwen3.5-Plus                                         Haiku 4.5                              GPT-OSS 120b
                                               (40/45 converged)                                  (37/45 converged)                        (43/45 converged)
                                        95%                                          35     92%                                               49%
                                 35                                                                                          20
                                                                                     30
                                 30
                                                                                     25                                      15
                                 25                                                                                                  30%
                                                                                     20
 Programs




                                 20
                                                                                     15                                      10
                                 15
                                                                                     10                                                                14%
                                 10                                                                                          5
                                                                                     5                                                                           7%
                                  5                                                                                    8%
                                                     2%                  2%
                                  0                                                  0                                       0
                                         1            2         3        4                  1          2        3      4              1        2        3         4
                                                    CEGAR Iteration                                  CEGAR Iteration                         CEGAR Iteration


Fig. 4. CEGAR iteration distribution on Frama-C benchmark (SmartICE) for three LLM backends. Nearly all converged programs require only a single
iteration.


                                                            SmartICE vs No-ICE Ablation FM2026                                                                     TABLE III
                                 50
                                             SmartICE (solid)                                                                            P RE -A BSTRACTION RESULTS ON LF-H ARD BENCHMARKS (24
                                             No-ICE (hatched)                                                95%                       PROGRAMS , 600 S BUDGET ). “D IRECT ESBMC” VERIFIES WITHOUT
                                              88%                                                                      91%
                                 40                       86%                             86%
Converged programs (out of 45)




                                                                                                                                           CONTRACTS ; C ON V ER COLUMNS USE P RE -A BSTRACTION .
                                                                               82%
                                                                                                                                      Q WEN = Q WEN -P LUS ; C LAUDE = H AIKU 4.5; GPT = GPT-OSS 120 B .

                                 30
                                                                                                                                                         Direct ESBMC           Qwen3.5-Plus        Haiku4.5        GPT-OSS
                                 20                                                                                                   Converged                10 (42%)            11 (46%)         12 (50%)        15 (62%)
                                                                                                                                      Timeout                     14                  12               11               8
                                                                                                                                      Failed                       0                   1                1               1
                                 10

                                  0
                                              Qwen3.5-Plus                      Haiku 4.5                     GPT-OSS 120b
                                                                                                                                    GPT-OSS 120b additionally converges on Fibonacci and
Fig. 5. SmartICE vs. No-ICE on the Frama-C benchmark for three LLM
                                                                                                                                    TrainDoorFeedback where the smaller models time out,
backends. Each pair of bars shows converged program counts with and without                                                         reflecting higher contract synthesis quality from the larger
ICE learning.                                                                                                                       model. The ordering of results mirrors the model’s capability,
                                                                                                                                    confirming that contract synthesis quality, not ESBMC’s solv-
                                                                                                                                    ing capacity, is the binding constraint on these benchmarks.
three backends: GPT-OSS 120b leads at 15/24 (62%), followed                                                                            Most converged programs require no CEGAR refinement
by Claude Haiku 4.5 at 12/24 (50%) and Qwen-Plus at 11/24                                                                           (iteration 0); the few that do (e.g., Election at iter=1,
(46%). The gains stem from programs such as Election,                                                                               Fibonacci at iter=2 for GPT-OSS 120b) converge quickly,
ADASModel, and ProcessMsg where monolithic ESBMC                                                                                    indicating the refinement loop is effective when initial con-
exploration times out, but contract-based decomposition re-                                                                         tracts are close to correct.
duces each function-level SMT instance to a tractable size.                                                                            ProcessSync is the single FAILED program across all
                                LF-Hard Benchmarks (24 programs, 600 s budget)
                                                                                         contract synthesis in a CEGIS–CEGAR loop to verify Lingua
                                                                                         Franca programs. The two systems are complementary rather
                                 42%            46%            50%            62%
                        24                       1              1               1        than directly competing. P OLY V ER operates at the LF source
 Programs (out of 24)



                                                                                         level: each benchmark comprises 18–206 LOC of LF source
                                                                                8
                        18
                                 14              12             11                       and 2–64 LOC of C reaction code, and UCLID5 is used
                                                                                         as the system-level model checker, enabling verification of
                        12                                                               temporal properties expressed as extended state machines and
                                                                                         support for polyglot (C and Rust) reactions. C ON V ER operates
                                                                               15
                         6                       11             12                       on the fully translated C output of ESBMC-LF, where the
                                 10
                                                                                         same benchmarks expand to 1 998–4 328 LOC monolithic C
                                              Converged         Timeout         Failed
                         0
                                                                                         files including the complete LF runtime. This makes C ON -
                                Direct       Qwen-Plus     Claude Haiku     GPT-OSS      V ER’s verification task substantially harder—state explosion
                                ESBMC         (ours)          (ours)         120b
                                                                                         in the translated code is why direct ESBMC fails on 14 of
                                                                                         24 benchmarks—but it also makes C ON V ER independent of
Fig. 6. Outcome breakdown on LF-Hard benchmarks (24 programs, 600 s                      any LF-specific toolchain: it verifies standard C programs
budget). Direct ESBMC (42%) is the no-contract baseline. GPT-OSS 120b
leads at 62%, with Claude Haiku 4.5 at 50% and Qwen-Plus at 46%,                         without requiring a separate model-checking frontend. Where
confirming that stronger contract synthesis yields higher convergence.                   P OLY V ER achieves 22/22 on its benchmark set at the source
                                                                                         level, C ON V ER achieves 15/24 (GPT-OSS 120b) on the
                                                 TABLE IV                                translated-C versions of the same programs, overall 16/24
                        P RE -A BSTRACTION STRATEGY RESULTS ON V ERIFY T HIS (900 S      across all run-throughs, a result that is not directly comparable
                        TIMEOUT ). Q WEN = Q WEN -P LUS ; C LAUDE = H AIKU 4.5; GPT =
                                              GPT-OSS 120 B .                            but highlights the additional challenge of verifying runtime-
                                                                                         inclusive translations.
                         Benchmark          Qwen3.5-Plus      Haiku4.5      GPT             ACSE [20] is evaluated on the same Frama-C and X.509
                         VerifyThis (11)       6 (55%)        7 (64%)     6 (55%)        benchmarks used in this paper, making it a direct point of
                                                                                         comparison. ACSE generates ACSL pre/post-conditions and
                                                                                         assigns clauses via array-carrying symbolic execution, and
LLM backends; ESBMC rejects its structure at the system-                                 crucially supports quantified loop invariants (e.g., ∀i. a[i] ≥ 0)
level check before contract synthesis begins, so it is excluded                          through its symbolic segment abstraction. C ON V ER does
from the convergence count.                                                              not generate quantified invariants: ESBMC’s function con-
   VerifyThis Benchmarks (11 programs): For VerifyThis (11                               tract mechanism does not support first-order quantifiers in
recursive and loop-invariant programs), we apply the Pre-                                requires/ensures clauses, so the Frama-C benchmark
Abstraction strategy. Table IV summarises the outcomes.                                  is restricted to the 45 programs whose properties can be
   On VerifyThis, Claude Haiku 4.5 achieves 7/11 (64%),                                  expressed without quantification. Programs that require quanti-
matching the reference result produced by the pipeline authors                           fied array invariants are outside C ON V ER’s current scope, and
under manual configuration. Qwen-Plus and GPT-OSS 120b                                   ACSE handles these cases where C ON V ER cannot. Within
both reach 6/11 (55%). The four programs that fail across all                            the quantifier-free subset, C ON V ER’s CEGAR loop provides
backends — MultCommutative, duplets, prefixsum,                                          a complementary advantage: rather than inferring contracts
and prefixsum_rec — involve complex inter-procedural                                     analytically in a single pass, it iteratively refines contracts
invariants that exceed the current contract synthesis capability                         against formal counterexamples, which handles cases where
within the iteration budget.                                                             symbolic invariant inference is imprecise or the program is
                                                                                         too large for exhaustive symbolic exploration.
a) RQ3 — Performance on complex programs.: On                                                  b) Persistent system-only cases.: Across all four config-
LF-Hard (24 programs), Pre-Abstraction lifts convergence                                 urations, 4–5 programs reach the system-only outcome: the
from 42% (direct ESBMC) to 62% (GPT-OSS 120b),                                           system-level ESBMC check passes, but at least one function-
with results ordering by model capability (GPT-OSS 120b                                  level check fails within the iteration limit. Inspection reveals
> Claude > Qwen), confirming that contract synthesis                                     that these programs contain loop-heavy functions for which
quality is the binding constraint. On VerifyThis (11 pro-                                the LLM consistently produces contracts that are too strong
grams), Pre-Abstraction achieves 55–64%, with Claude                                     for the implementation to satisfy, and the 5-iteration budget is
Haiku 4.5 matching the expert reference at 7/11; the                                     insufficient to relax them to a valid specification. Increasing
four failing programs involve complex inter-procedural                                   the iteration limit or adding an automatic loop invariant
invariants beyond current synthesis capability.                                          synthesis step for these functions are promising remedies.
                                                                                               c) Threats to validity.: Three threats apply. First, the
                                                                                         Frama-C benchmark consists entirely of relatively simple
                                           VII. D ISCUSSION                              single-assertion programs; generalisation to multi-property,
      a) Comparison with state of the art.: The most closely                             multi-function programs remains to be demonstrated. Sec-
related tool is P OLY V ER [17], which also applies LLM-based                            ond, LLM outputs are stochastic, so results may vary across
runs; we ran each configuration once and have not yet                                             R EFERENCES
conducted repeated-trial experiments. Third, the one known
                                                                     [1] T. Wu, X. Li, E. Manino, R. S. Menezes, M. R. Gadelha, S. Xiong,
soundness caveat is specific to ESBMC’s assigns clause                   N. Tihanyi, P. Petoumenos, and L. C. Cordeiro, “Esbmc v7. 7: Efficient
implementation: pointer-dereference targets (e.g., assigns               concurrent software verification with scheduling, incremental smt and
                                                                         partial order reduction: (competition contribution),” in International
*instance_args) are not currently supported by ESBMC                     Conference on Tools and Algorithms for the Construction and Analysis
and are stripped from contracts before invocation, so frame              of Systems. Springer, 2025, pp. 223–228.
conditions for state modified through pointer parameters are         [2] N. Chong, B. Cook, J. Eidelman, K. Kallas, K. Khazem, F. R. Monteiro,
not mechanically verified. This is a limitation of the ESBMC             D. Schwartz-Narbonne, S. Tasiran, M. Tautschnig, and M. R. Tuttle,
                                                                         “Code-level model checking in the software development workflow at
backend, not of the compositional method: all requires,                  amazon web services,” Software: Practice and Experience, vol. 51, no. 4,
ensures, and scalar assigns clauses are verified normally,               pp. 772–797, 2021.
and the method’s soundness argument holds for the verified           [3] E. M. Clarke, W. Klieber, M. Nováček, and P. Zuliani, “Model checking
                                                                         and the state explosion problem,” in LASER Summer School on Software
portion of each contract. All results reported in the tables are         Engineering. Springer, 2011, pp. 1–30.
valid under these conditions.                                        [4] E. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith, “Counterexample-
                                                                         guided abstraction refinement,” in International Conference on Com-
                     VIII. C ONCLUSION                                   puter Aided Verification. Springer, 2000, pp. 154–169.
                                                                     [5] P. Garg, C. Löding, P. Madhusudan, and D. Neider, “Ice: A robust
   We have presented C ON V ER, a tool for LLM-guided top-               framework for learning invariants,” in International Conference on
down compositional verification of C programs using ESBMC                Computer Aided Verification. Springer, 2014, pp. 69–87.
function contracts. On the Frama-C benchmark of 45 C pro-            [6] A. Biere, A. Cimatti, E. Clarke, and Y. Zhu, “Symbolic model checking
                                                                         without bdds,” in International conference on tools and algorithms for
grams, C ON V ER achieves 82–96% verification success across             the construction and analysis of systems. Springer, 1999, pp. 193–207.
three LLM backends (GPT-OSS 120b 96%, Qwen-Plus 89%,                 [7] A. Biere, A. Cimatti, E. M. Clarke, O. Strichman, and Y. Zhu, “Bounded
Claude Haiku 4.5 82%), with over 93% of converged programs               model checking.” Handbook of satisfiability, vol. 185, no. 99, pp. 457–
                                                                         481, 2009.
requiring only a single CEGAR iteration. On LF2C-Simple              [8] L. Cordeiro and B. Fischer, “Bounded model checking of multi-threaded
(17 programs) results are consistent at 82–88%, confirming               software using smt solvers,” arXiv preprint arXiv:1003.3830, 2010.
that the pipeline generalises beyond its primary benchmark.          [9] M. R. Gadelha, F. R. Monteiro, J. Morse, L. C. Cordeiro, B. Fischer,
                                                                         and D. A. Nicole, “Esbmc 5.0: an industrial-strength c model checker,”
On the VerifyThis suite of 11 recursive and loop-intensive               in Proceedings of the 33rd ACM/IEEE International Conference on
programs, the Pre-Abstraction strategy achieves 55–64%, with             Automated Software Engineering, 2018, pp. 888–891.
Claude Haiku 4.5 matching the expert reference at 7/11. All         [10] R. S. Menezes, M. Aldughaim, B. Farias, X. Li, E. Manino, F. Shmarov,
                                                                         K. Song, F. Brauße, M. R. Gadelha, N. Tihanyi et al., “Esbmc v7.
three backends achieve competitive results on well-structured            4: Harnessing the power of intervals: (competition contribution),” in
programs, while on harder benchmarks (LF-Hard, 46–62%)                   International Conference on Tools and Algorithms for the Construction
results correlate with model capability, confirming that the             and Analysis of Systems. Springer, 2024, pp. 376–380.
                                                                    [11] H. Jelodar, S. Bai, P. Hamedi, H. Mohammadian, R. Razavi-Far, and
CEGAR+ICE loop is the primary driver of convergence on                   A. Ghorbani, “Large language model (llm) for software security: Code
tractable programs.                                                      analysis, malware analysis, reverse engineering,” Journal of Information
   Future work will target two directions: (1) extending the             Security and Applications, vol. 98, p. 104390, 2026.
                                                                    [12] C. S. Xia, Y. Wei, and L. Zhang, “Automated Program Repair in
approach to programs with multiple top-level assertions, and             the Era of Large Pre-trained Language Models,” in 2023 IEEE/ACM
(2) investigating hybrid model selection strategies that route           45th International Conference on Software Engineering (ICSE).
simple programs to fast, cheap LLMs and complex programs                 Melbourne, Australia: IEEE, May 2023, pp. 1482–1494. [Online].
                                                                         Available: https://ieeexplore.ieee.org/document/10172803/
to stronger reasoning models.                                       [13] J. Liu, S. Xie, J. Wang, Y. Wei, Y. Ding, and L. Zhang, “Evaluating
                                                                         Language Models for Efficient Code Generation,” Aug. 2024,
                 IX. ACKNOWLEDGEMENTS                                    arXiv:2408.06450. [Online]. Available: http://arxiv.org/abs/2408.06450
  The authors of this research disclose that generative AI          [14] N. Tihanyi, Y. Charalambous, R. Jain, M. A. Ferrag, and L. C. Cordeiro,
                                                                         “A new era in software security: Towards self-healing software via
was used in the development of the tooling and in the                    large language models and formal verification,” in 2025 IEEE/ACM
execution of the methodological evaluation. After using these            International Conference on Automation of Software Test (AST). IEEE,
tool(s)/service(s), the author(s) reviewed and edited the content        2025, pp. 136–147.
                                                                    [15] F. Zubair, M. Al-Hitmi, and C. Catal, “The use of large language
as needed and take(s) full responsibility for the publication’s          models for program repair,” Computer Standards & Interfaces, vol. 93,
content.                                                                 p. 103951, Apr. 2025. [Online]. Available: https://www.sciencedirect.
                                                                         com/science/article/pii/S092054892400120X
                        AVAILABILITY                                [16] M. Haque, P. Babkin, F. Farmahinifarahani, and M. Veloso, “Towards
                                                                         Effectively Leveraging Execution Traces for Program Repair with
   The C ON V ER tool, all benchmark programs, pre-computed              Code LLMs,” May 2025, arXiv:2505.04441 [cs] version: 1. [Online].
experiment results, and reproduction scripts are openly avail-           Available: http://arxiv.org/abs/2505.04441
able as a replication package on Zenodo at https://doi.org/         [17] P.-W. Chen, S. Lin, A. Godbole, R. Singh, E. Polgreen, E. Lee,
                                                                         and S. Seshia, “Polyver: A compositional approach for polyglot
10.5281/zenodo.19249204. The artifact includes the C ON V ER             system modeling and verification,” 2025. [Online]. Available: https:
source code, ESBMC v8.1 static binary, all four benchmark                //repositum.tuwien.at/handle/20.500.12708/219538
suites (Frama-C, X.509, LF2C-Simple, VerifyThis, LF-Hard),          [18] Z. Wang, T. Lin, M. Chen, H. Li, M. Yang, X. Yi, S. Qin, Y. Luo,
                                                                         X. Li, B. Gu et al., “A tale of 1001 loc: Potential runtime error-
and the figures and notebooks used to generate the results in            guided specification synthesis for verifying large-scale programs,” arXiv
this paper.                                                              preprint arXiv:2512.24594, 2025.
                                                                    [19] S. A. Seshia and P. Subramanyan, “Uclid5: integrating modeling, veri-
                                                                         fication, synthesis and learning,” in 2018 16th ACM/IEEE International
     Conference on Formal Methods and Models for System Design (MEM-
     OCODE). IEEE, 2018, pp. 1–10.
[20] W. Lu, J. Ke, H. Fu, Z. Sun, Y. Zhou, G. Li, and H. Li, “Array-carrying
     symbolic execution for function contract generation,” in Proceedings of
     the 26th International Symposium on Formal Methods (FM 2026), ser.
     Lecture Notes in Computer Science. Springer, 2026.
[21] A. Zeller, “Yesterday, my program worked. today, it does not. why?”
     ACM SIGSOFT Software engineering notes, vol. 24, no. 6, pp. 253–267,
     1999.
[22] A. Zeller and R. Hildebrandt, “Simplifying and isolating failure-inducing
     input,” IEEE Transactions on software engineering, vol. 28, no. 2, pp.
     183–200, 2002.
[23] R. Sá Menezes, M. Aldughaim, B. Farias, X. Li, E. Manino,
     F. Shmarov, K. Song, F. Brauße, M. R. Gadelha, N. Tihanyi,
     K. Korovin, and L. C. Cordeiro, “ESBMC 7.4: Harnessing the
     power of intervals,” Systems & Software Verification Laboratory,
     Software Documentation, 2024, version 7.4. Available at: https:
     //github.com/esbmc/esbmc. Accessed: 2026-03-20. [Online]. Available:
     https://esbmc.github.io/docs/#quantifiers
[24] M. A. Pirzada, G. Reger, A. Bhayat, and L. C. Cordeiro, “Llm-generated
     invariants for bounded model checking without loop unrolling,” in Pro-
     ceedings of the 39th IEEE/ACM International Conference on Automated
     Software Engineering, 2024, pp. 1395–1407.
[25] A. Komuravelli, C. S. Păsăreanu, and E. M. Clarke, “Assume-guarantee
     abstraction refinement for probabilistic systems,” in International con-
     ference on computer aided verification. Springer, 2012, pp. 310–326.
[26] A. Solar-Lezama, C. G. Jones, and R. Bodik, “Sketching concurrent
     data structures,” in Proceedings of the 29th ACM SIGPLAN Conference
     on Programming Language Design and Implementation, ser. PLDI ’08.
     New York, NY, USA: Association for Computing Machinery, 2008, p.
     136–148. [Online]. Available: https://doi.org/10.1145/1375581.1375599
[27] T. J. McCabe, “A complexity measure,” IEEE Transactions on software
     Engineering, no. 4, pp. 308–320, 1976.
[28] S. Lin, Y. A. Manerkar, M. Lohstroh, E. Polgreen, S.-J. Yu, C. Jerad,
     E. A. Lee, and S. A. Seshia, “Towards building verifiable cps using
     lingua franca,” ACM Transactions on Embedded Computing Systems,
     vol. 22, no. 5s, pp. 1–24, 2023.
[29] Anthropic, “Introducing Claude 3.5 Sonnet,” 2024, accessed:
     2026-03-27. [Online]. Available: https://www.anthropic.com/news/
     claude-3-5-sonnet
[30] D. Beyer, “State of the art in software verification and witness validation:
     Sv-comp 2024,” in International Conference on Tools and Algorithms
     for the Construction and Analysis of Systems. Springer, 2024, pp.
     299–329.
