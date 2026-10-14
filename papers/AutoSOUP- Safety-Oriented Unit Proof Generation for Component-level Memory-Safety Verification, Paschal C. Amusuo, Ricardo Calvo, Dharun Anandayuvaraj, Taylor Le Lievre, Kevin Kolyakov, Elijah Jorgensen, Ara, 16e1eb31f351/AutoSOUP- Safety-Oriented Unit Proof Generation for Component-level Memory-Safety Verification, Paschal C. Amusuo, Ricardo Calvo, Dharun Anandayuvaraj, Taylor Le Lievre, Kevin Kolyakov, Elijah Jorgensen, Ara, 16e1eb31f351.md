                                                        AutoSOUP: Safety-Oriented Unit Proof Generation for
                                                            Component-level Memory-Safety Verification
                                                           Paschal Amusuo                                                    Ricardo Calvo                           Dharun Anandayuvaraj
                                                          Purdue University                                               Purdue University                               Purdue University
                                                                USA                                                             USA                                             USA
                                                        cpamusuo@purdue.edu                                             rcalvome@purdue.edu                             dananday@purdue.edu

                                                           Taylor Le Lievre                                                Kevin Kolyakov                                  Elijah Jorgensen
                                                          Columbia University                                          University of Waterloo                              Purdue University
                                                                 USA                                                          Canada                                             USA
arXiv:2605.10712v1 [cs.SE] 11 May 2026




                                                         tjl2152@columbia.edu                                         kkolyakov@uwaterloo.ca                             jorgene1@purdue.edu

                                                                                          Aravind Machiry                                          James C. Davis
                                                                                          Purdue University                                       Purdue University
                                                                                                USA                                                     USA
                                                                                        amachiry@purdue.edu                                     davisjam@purdue.edu

                                         Abstract                                                                                        Keywords
                                         Memory-safety errors remain a persistent source of zero-day vul-                                Memory-safety verification, Bounded Model Checking, Unit Proofs
                                         nerabilities in low-level software. The problem is especially acute in
                                                                                                                                         ACM Reference Format:
                                         embedded systems, where hardware protections are often limited
                                                                                                                                         Paschal Amusuo, Ricardo Calvo, Dharun Anandayuvaraj, Taylor Le Lievre,
                                         and dynamic analysis is difficult to apply effectively. Memory-safety                           Kevin Kolyakov, Elijah Jorgensen, Aravind Machiry, and James C. Davis.
                                         verification can provide stronger assurance by proving the absence                              2018. AutoSOUP: Safety-Oriented Unit Proof Generation for Component-
                                         of such errors or exposing violations when they exist. However,                                 level Memory-Safety Verification. In Proceedings of ACM Conference on XXX
                                         current verification workflows remain largely manual and require                                (XXX ’26). ACM, New York, NY, USA, 24 pages. https://doi.org/XXXXXXX.
                                         substantial specialized expertise, limiting their adoption in practice.                         XXXXXXX
                                            We present AutoSOUP, a system for automating component-level
                                         memory-safety verification through Safety-Oriented Unit Proofs.
                                         We formalize these unit proofs as artifacts that encode verification
                                                                                                                                         1    Introduction
                                         choices (scope, loop bounds, and environment models) for verifying                              Memory-safety errors remain a persistent source of zero-day ex-
                                         safety properties, and introduce three techniques for deriving them                             ploits in low-level software [11, 56]. These errors enable denial-of-
                                         automatically. To overcome the limitations of existing automation                               service, data-theft, and remote-code-execution attacks [63]. Their
                                         approaches, we further introduce LLM-As-Function-Call, a hybrid                                 risk is especially acute in embedded systems, which often lack stan-
                                         architecture that combines deterministic program synthesis with                                 dard hardware protections [9] and are difficult to analyze effectively
                                         LLMs to automate these techniques and produce justifiable unit                                  with techniques such as fuzzing [57, 61]. After decades of recurring
                                         proofs. We evaluate AutoSOUP by assessing its ability to automate                               exploits and failures [27, 55, 56, 63], government agencies and in-
                                         memory-safety verification and expose vulnerabilities in verified                               dustry organizations increasingly advocate or mandate methods
                                         components, and we characterize the assumptions and guarantees                                  that provide stronger memory-safety guarantees [7, 10, 19, 47].
                                         of the resulting proofs.                                                                           Formal memory-safety verification can provide such guarantees,
                                                                                                                                         but existing techniques remain difficult to apply at scale. Deductive
                                         CCS Concepts                                                                                    verification [34] can prove memory safety [45, 50], but it often re-
                                                                                                                                         quires specialized verification expertise, domain knowledge, and
                                         • Software and its engineering → Formal software verifica-                                      manual proof guidance [36, 39]. Bounded model checking (BMC) [5,
                                         tion; • Security and privacy → Software security engineering.                                   25] offers a more automated alternative, but whole-program BMC
                                                                                                                                         does not scale to large software systems. Recent industry case stud-
                                                                                                                                         ies [24, 68, 70] favor a decomposition approach, wherein engineers
                                         Permission to make digital or hard copies of all or part of this work for personal or
                                         classroom use is granted without fee provided that copies are not made or distributed           verify components in isolation using “unit proofs” [15] that specify
                                         for profit or commercial advantage and that copies bear this notice and the full citation       a component’s verification scope, loop bounds, and environment
                                         on the first page. Copyrights for components of this work owned by others than the              models. However, constructing these unit proofs remains challeng-
                                         author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
                                         republish, to post on servers or to redistribute to lists, requires prior specific permission   ing and error-prone: engineers must choose scopes, bounds, and
                                         and/or a fee. Request permissions from permissions@acm.org.                                     models that are strong enough to expose genuine memory-safety
                                         XXX ’26, United States                                                                          errors, but constrained enough to keep verification tractable. AWS’s
                                         © 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM ISBN 978-1-4503-XXXX-X/2018/06                                                              report [24] suggests a substantial engineering cost, with a verifi-
                                         https://doi.org/XXXXXXX.XXXXXXX                                                                 cation rate of 1500 lines of code in one person-month. No existing
XXX ’26, 2026, United States                                                                                                                     Amusuo et al.



                                                                          1    size_t get_record_count() {           1     Scope = {process_record,
                                                                          2       // Complex logic returning              ↩→   handle_record}.
                                                                                 ↩→ [0,10]                           2     Loop bound: {process_record.0:
                                                                           3      return count;                           ↩→ 11}
                                                                           4   }                                      3
                                                                           5                                          4   size_t get_record_count_m1() {
                                                                           6   int handle_record(size_t i) {          5     uint8_t ret = nondet_int();
                                                                           7     ...                                  6     assume(ret < 10);
                                                                           8   }                                      7     return ret;
                                                                           9                                          8   }
                                                                          10   void process_record(uint8_t            9
                                                                               ↩→ *dst) {                            10   size_t get_record_count_m2() {
                                                                          11       size_t n = get_record_count();    11     uint8_t ret = nondet_int();
                                                                          12        // Bug!! should be i < n         12     assume(ret <= 10);
Figure 1: AutoSOUP automatically identifies the functions                 13        for (size_t i = 0; i <= n;       13     return ret;
to include in the verification scope, loop bounds, and en-                         ↩→ ++i) {                         14   }
                                                                          14          dst[i] = handle_record(i);     15
vironment model for which the resulting component-level                   15          assert(isValidObject(dst));    16   void harness(void) {
memory-safety verification completes and provides useful                  16          assert(ObjectSize(dst) > i);   17      uint8_t dst_size =
                                                                          17        }                                       ↩→ nondet_int();
guarantees of memory safety.                                              18   }                                     18      uint8_t *dst =
                                                                          19                                                ↩→ malloc(dst_size);
                                                                          20   void caller() {                       19      assume(dst != NULL);
                                                                          21     int dst[10];                        20      process_record(dst);
                                                                          22     process_record(dst);                21   }
                                                                          23   }
work automates these choices in a way that supports practical
component-level memory-safety verification for real C software.
    To address this gap, this paper introduces AutoSOUP (Figure 1),      Listing 1: Left: Program instrumented with memory-safety
a hybrid system for constructing unit proofs that enable useful          properties and its calling context. Right: Unit proof with
memory-safety verification for embedded software. The key idea           verification choices for the process_record component.
is the notion of memory-safety-oriented unit proofs: reusable verifi-
cation artifacts that prioritize the scope, bounds, and environment
models needed to preserve safety-relevant memory behavior, rather         Significance: AutoSOUP is the first system to automate memory-
than faithfully model all execution behavior. AutoSOUP derives           safety verification through the construction of unit proofs that en-
these choices using three techniques: resource-aware scope widen-        able component-level bounded model checking. Our results show
ing, property-guided loop-bound selection, and context-aware en-         that AutoSOUP applies to substantial real-world codebases, pro-
vironment refinement. To make this automation reliable and gen-          vides useful memory-safety assurance, and exposes real security
eralizable, AutoSOUP uses a hybrid LLM-as-function-call archi-           vulnerabilities. Automated memory-safety verification can be prac-
tecture [42, 51]. Rather than asking an LLM to synthesize an en-         tical enough to integrate into software-development workflows and
tire proof artifact, AutoSOUP uses deterministic program-analysis        help prevent memory-safety vulnerabilities before deployment.
workflows to drive the construction process and invokes LLMs
for controlled tasks with explicit validation criteria. As a result,     2 Background
each verification choice incorporated into the unit proof is tied to a   2.1 Memory-Safety and Verification
specific algorithmic objective and validated before use.
                                                                         Memory safety means that all memory accesses performed by a pro-
    We evaluate AutoSOUP on four embedded real-time operat-
                                                                         gram are valid under the semantics of the language [63]. Accesses
ing systems. AutoSOUP successfully produces valid unit proofs
                                                                         must refer to memory that has been properly allocated, remain
and verifies 93% of candidate targets, exposing 66.7% of evalu-
                                                                         within the bounds of the target object, and occur during that object’s
ated vulnerabilities—38.7% and 28.5% more than the next best-
                                                                         lifetime [16, 38, 58]. A memory safety error violates these condi-
performing baselines. Each of our techniques contributes to the
                                                                         tions [58, 67], either spatially or temporally [63]. Violations of these
final verification results by improving the derived bounds and en-
                                                                         conditions cause memory corruption and remain a major source of
vironment models. Moreover, AutoSOUP’s unit proofs use simpler
                                                                         software failures, security vulnerabilities, and exploits [6, 8, 56, 69].
and more general environment assumptions than fidelity-oriented
                                                                             Memory-safety verification uses formal methods to establish that
expert-written counterparts while achieving comparable verifica-
                                                                         a program cannot perform invalid memory accesses, subject to
tion outcomes.
                                                                         explicit modeling assumptions. Compared with testing and bug-
    In summary, this paper makes the following contribution:
                                                                         finding techniques, its goal is not only to expose errors, but also to
     • We propose safety-oriented unit proofs, a formulation of          provide assurance that specified classes of memory violations are
       component-level memory-safety verification artifacts; and         absent within the verified program.
       techniques for scope, bounds, and environment models.                 Two approaches have been especially important for memory-
     • We operationalize the LLM-as-function-call architecture for       safety verification. Deductive verification proves memory safety
       automating auditable and justifiable unit-proof construction.     by reasoning over program behavior using specifications of pro-
     • We design and implement AutoSOUP to automatically con-            gram state, memory, and invariants [21, 45]. It can provide strong
       struct safety-oriented unit proofs for C-language software.       guarantees over all executions, but it requires substantial exper-
     • We evaluate AutoSOUP on 177 components from four widely           tise and manual proof effort. In contrast, Bounded Model Checking
       used embedded operating systems and report its utility, ef-       (BMC) [41] checks memory-safety properties automatically by ex-
       fectiveness, and cost for memory-safety verification.             ploring executions within explicit bounds.
AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification                                      XXX ’26, 2026, United States


2.2     Bounded Model Checking and Unit Proofing                                     them in real software. This gap motivates methods that derive veri-
Tools for Bounded Model Checking (BMC) [43, 46] specify program                      fication choices automatically while preserving the safety-relevant
properties as Boolean assertions over variable states, automatically                 behavior needed for useful memory-safety verification guarantees.
check these assertions using constraint-solving tools, and report
counterexample traces [53]. For memory-safety verification, BMC                      3     Problem Statement
instruments the program with memory-safety assertions, unrolls                       Our goal is to automate component-level memory-safety verifica-
loops and recursion, translates the resulting bounded program into                   tion through the creation of unit proofs. This requires identifying
a satisfiability formula, and applies constraint solvers. If no violating            verification choices that provide meaningful memory-safety guar-
trace exists, BMC proves that the instrumented properties hold. If                   antees while keeping verification tractable.
a violation exists, BMC returns a counterexample.                                       We formalize the problem as follows. Given a software system 𝑆,
   Listing 1 illustrates how BMC can be used to verify a compo-                      a component entry point 𝐶𝑒 , a set of memory-safety properties 𝑄,
nent’s memory safety. An engineer verifies a connected subset of a                   and a resource budget 𝑅, automatically construct a unit proof 𝑈 (𝑉 )
program to keep verification tractable (verification scope); for exam-               that encodes the verification choices
ple, they may verify process_record and handle_record while
excluding the get_record_count callee. The engineer must also                                                    𝑉 = (𝑆𝑐 , 𝐵, 𝐸),
choose the maximum number of times to unroll loops (loop bounds),
because BMC operates only on loop-free programs, and provide                         where 𝑆𝑐 ⊆ 𝑆 is a connected set of functions rooted in 𝐶𝑒 , 𝐵 maps
assumptions about the behavior of callers and callees outside the                    each loop reachable in 𝑆𝑐 to a maximum unrolling bound, and 𝐸 is an
chosen scope (environment model).                                                    environment model that defines assumptions for functions outside
   These choices—verification scope, loop bounds, and environ-                       𝑆𝑐 . The resulting proof should allow BMC to verify 𝑄 conclusively
ment model—are encoded in a unit proof, shown on the right of                        within 𝑅, while ensuring the result reflects the memory safety of
Listing 1. For example, Program Lines 15–16 assert that dst points                   the verified functions 𝑆𝑐 in the original system 𝑆. In Listing 1, this
to a valid allocated object and that the object is large enough for the              means constructing the unit proof on the right so that BMC exposes
indexed write; the unit proof then determines the scope, bounds,                     the memory-safety error on the left.
and assumptions under which BMC checks those assertions.                                 No existing work solves this problem automatically. Prior work
                                                                                     on memory-safety verification either requires experts to define
                                                                                     these choices [24, 68, 70], or uses fixed scope, loop bounds and
                                                                                     program-analysis-inferred environment models [21, 23, 40] that
2.3     Verification Choice Fidelity                                                 require expert adaptation to real software. In this work, we auto-
The guarantees afforded by BMC depend on the choices encoded in                      matically derive verification choices and construct executable unit
a unit proof. For example, on Line 13 of Listing 1, setting the bound                proofs for real C software.
for the program loop to 1 may suffice to check that dst is valid,
but not that all indexed accesses are valid. Similarly, the overly-                  3.1         Success Criteria
constrained model get_record_count_m1 (Unit Proof Lines 4–8)
masks the violation, whereas get_record_count_m2 exposes it.                         A unit proof should support useful memory-safety guarantees.
   We define verification choice fidelity (VCF) as the degree to which               Building on [12], we distinguish five requirements:
these choices reflect the behavior of the real system. Formally, we                   (1) Structural validity: It should compile and verify the intended
characterize fidelity as 𝑉𝐶𝐹 = ⟨𝑆𝑐 𝑓 , 𝐵 𝑓 , 𝐸 𝑓 ⟩, where 𝑆𝑐 𝑓 denotes               component identified by the entry point 𝐶𝑒 . For example, the unit
verification-scope fidelity, 𝐵 𝑓 denotes loop-bound fidelity, and 𝐸 𝑓                proof in Listing 1 must verify process_record.
denotes environment-model fidelity. This notion is related to model                   (2) Conclusiveness [12]: It should produce a verification result within
fidelity in systems modeling [54] and execution fidelity in firmware                 the resource budget 𝑅. The result may be either a proof that the tar-
rehosting [33, 61] but focuses on choices that affect bounded model                  get memory-safety properties 𝑄 hold, or a counterexample showing
checking. Higher-fidelity choices preserve implementation behav-                     the states and execution trace that violate them.
ior and can support stronger guarantees. Lower-fidelity choices                       (3) Verification coverage [12]: It should verify as much reachable
simplify semantics, reducing development cost.
                                                                                     code in its verification scope as possible. We define verification
   Many existing approaches to component-level BMC are fidelity-
                                                                                     coverage as the proportion of included lines that are exercised and
oriented. They rely on experts to encode detailed knowledge of the
                                                                                     checked by the unit proof. This metric is analogous to line coverage
system [24], infer artifacts from specifications [70] or unit tests [68],
                                                                                     in unit testing and fuzzing.
or refine artifacts manually using verification results [12]. Such
proofs can provide strong guarantees, but require deep knowledge                      (4) Result validity: It should make verification choices that neither
of the component and its role in the surrounding program. It is                      encode spurious violations nor mask feasible memory-safety viola-
therefore hard to create them automatically.                                         tions within the checked scope, bounds, and assumptions. Reported
   Other approaches rely on automatable choices, such as fixed                       violations should correspond to real memory-safety errors.
function-level scopes [23, 40], uniform loop bounds [64], or envi-                    (5) Maintainability: Unit proofs are reusable and auditable artifacts.
ronment models inferred by program analysis [21, 40]. However,                       As a result, their format should be familiar to software engineers
these methods focus on restricted property sets, limiting their use                  so that the verification choices can be inspected and refined and
for memory-safety verification; or require expert guidance to apply                  the unit proofs maintained as the code evolves.
XXX ’26, 2026, United States                                                                                                       Amusuo et al.


Automatically generating unit proofs that satisfy these require-          widens 𝑆𝑐 incrementally, using simple models for functions that re-
ments is non-trivial because the requirements can conflict. For ex-       main outside the current scope. This lets the verifier check memory-
ample, a system may improve conclusiveness with shallow bounds            safety properties in the included code without requiring precise
or simple models, but reduce verification coverage or result validity.    models for every external callee. A widened scope is useful only
Conversely, techniques optimized for result validity may compro-          if it increases the code and properties checked while remaining
mise coverage and tractability, or yield unit proofs too complex for      within the resource budget 𝑅. This reframing avoids the need to
engineering teams. Prior work [12] introduced conclusiveness and          predict the globally best scope in advance: AutoSOUP starts with a
verification coverage to assess unit proof completeness. We add           small, tractable scope and expands only as needed.
structural validity, result validity, and maintainability to capture       2. Property-guided loop-bound refinement: Prior fidelity-oriented ap-
risks introduced by automation: a generated unit proof may verify         proaches rely on experts to define loop bounds [24] or loop invari-
the wrong entry point, encode choices that produce invalid results,       ants [37]. Other approaches use uniform bounds for all loops [64],
or become too complex for maintainers to inspect and refine.              which can be expensive and still miss memory-safety-relevant be-
                                                                          havior. We instead treat loop-bound selection as a property-guided
3.2     System and Threat Model                                           refinement problem. The intuition is that many memory-safety
 System model: We consider software systems 𝑆 written in the C            properties depend on local program states and are affected most
language, which is often used for embedded software development.          directly by nearby loops. Thus, AutoSOUP refines 𝐵 only for loops
We focus on components that process untrusted inputs from exter-          whose iterations affect the reachability or violation of instrumented
nal interfaces, e.g., network channels, since these interfaces form       memory-safety properties (e.g., the loop on Line 13 of Listing 1).
primary attack surfaces. We exclude programs in which memory               3. Context-aware environment refinement: Environment models cre-
references can be shared across processes (threads or tasks) and          ate a different tension: permissive models expose possible memory-
that are prone to race conditions, because they violate the linear        safety violations, but can also produce infeasible counterexamples;
execution assumptions of standard bounded model checking tools.           overly constrained models avoid spurious reports, but can mask
 Threat model: We consider attackers who can supply inputs through        real violations. We therefore extend counterexample-guided envi-
external interfaces and thereby trigger violations of the target          ronment refinement [40] with context validation. AutoSOUP starts
memory-safety properties 𝑄. Such inputs may flow directly to              with permissive models that expose possible violations, infers pre-
memory-safety sinks or indirectly influence control/data flow so          conditions that suppress infeasible violations, and then validates
that the component reaches an unsafe memory state.                        those preconditions against calling contexts in the original program.
                                                                          Preconditions satisfied by the surrounding program become explicit
4     AutoSOUP Design and Implementation                                  assumptions in 𝐸; violated preconditions identify feasible memory-
We designed AutoSOUP to automate component-level memory-                  safety errors. In Listing 1, this process distinguishes assumptions
safety verification through the creation of unit proofs (Figure 2).       needed for process_record to be memory safe from assumptions
                                                                          violated by the actual implementation of get_record_count().
4.1     Key Ideas                                                            Together, these techniques derive 𝑆𝑐 , 𝐵, and 𝐸 in a property-
AutoSOUP explores two ideas: safety-oriented derivation of verifica-      directed way. The resulting unit proofs 𝑈 (𝑉 ) are safety-oriented
tion choices (§4.1.1) and LLM-as-function-call automation (§4.1.2).       because they preserve behavior relevant to the target safety prop-
                                                                          erties rather than all program behavior. Although we focus on
4.1.1 Memory-Safety-Oriented Unit Proofs. We introduce memory-            memory safety, the same formulation applies to safety properties
safety-oriented unit proofs: unit proofs whose verification choices       expressible as Boolean predicates over program states.
𝑉 = (𝑆𝑐 , 𝐵, 𝐸) are tailored to the instrumented memory-safety prop-
erties 𝑄. Unlike fidelity-oriented unit proofs, which choose 𝑉 to
approximate the program’s behavior, memory-safety-oriented unit
proofs choose 𝑉 to preserve the behavior needed to prove or refute        4.1.2 Automating Safety-Oriented Unit Proofs. Automating safety-
𝑄 within the resource budget 𝑅. This gives a safety-oriented inter-       oriented unit proofs requires both project-specific reasoning and
pretation of each choice: 𝑆𝑐 should include code that contributes         auditable verification choices. Program analysis can enforce syntac-
checkable memory-safety behavior; 𝐵 should be large enough to             tic and semantic constraints, but struggles with build configuration,
cover or expose property-relevant loop behavior; and 𝐸 should             local code idioms, and scalable semantic inference. LLMs can handle
expose possible violations while excluding infeasible ones.               such project-specific reasoning, but unconstrained generation is
    AutoSOUP realizes this interpretation through three techniques.       unsuitable because invalid scopes, bounds, or environment assump-
 1. Resource-aware scope widening: Prior fidelity-oriented approaches     tions can invalidate the resulting verification guarantees.
rely on experts to select verification scopes [24, 64]. Automating this       AutoSOUP balances reliability and generalizability with an LLM-
selection is difficult because it requires reasoning about both inter-    as-function-call architecture. Deterministic algorithms control the
function semantics and verification cost. However, prior work [12]        proof-construction workflow and define the objective of each step.
suggests that memory-safety verification often does not require           When a step requires semantic code understanding or project-
preserving all inter-function behavior.                                   specific adaptation, AutoSOUP delegates a bounded task to a tool-
    We therefore treat scope selection as a resource-aware coverage       equipped LLM agent. Program-analysis modules then validate the
problem rather than a full semantic-modeling problem. AutoSOUP            returned artifact before it is incorporated into the unit proof.
AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification                                        XXX ’26, 2026, United States




Figure 2: AutoSOUP system diagram. AutoSOUP connects safety-oriented unit-proof construction with LLM-as-function-call
automation. Across all stages, deterministic workflows derive the verification choices 𝑉 = (𝑆𝑐 , 𝐵, 𝐸), delegate bounded semantic
tasks to LLM agents, and validate returned artifacts before incorporating them into the unit proof.


4.2     Resource-Aware Scope Widening                                                by longest common path prefix to the in-scope caller. An LLM agent
Resource-aware scope widening derives 𝑆𝑐 by incrementally adding                     recovers build configuration for newly added files, and AutoSOUP
semantically related code that may contain checkable memory-                         repeats external-call modeling and scope widening until verification
safety properties, retaining expansions only while verification re-                  exceeds 𝑅 or no additional files can be added.
mains within the resource budget 𝑅. We use source files as the unit
of expansion because related functions are often colocated, making                     Algorithm 1: Property-guided loop-bound and model re-
file-level widening a coarse but useful approximation of semantic                      finement. Given a verification instance with initial loop
locality. The algorithm proceeds in three steps (cf. §C.1).                            bounds, refine the bounds, build configuration, and envi-
 Step 1: Initialize the scope, bounds, and input model: AutoSOUP ini-                  ronment models to cover property-relevant code and expose
tializes 𝑆𝑐 with the file containing 𝐶𝑒 , sets all loop bounds to 1, and               loop-dependent memory-safety violations.
constructs a type-directed input model for 𝐶𝑒 : primitive arguments                     Input: Verification scope 𝑆𝑐 , properties 𝑄, loop bounds 𝐵,
receive unconstrained symbolic values, while pointer arguments                                 environment model 𝐸, resource budget 𝑅
receive valid allocated objects containing unconstrained values. An                     Output: Refined loop-bound map 𝐵, refined environment model 𝐸
                                                                                      1 Function PropertyGuidedRefinement(𝑆𝑐 , 𝑄, 𝐵, 𝐸, 𝑅)
LLM agent synthesizes this input model and recovers the build
                                                                                           // Step 1: Cover property-relevant code
configuration needed to compile the entry point’s parent file, in-
                                                                                      2    𝐺 ← UncoveredPropertyBlocks(𝑆𝑐 , 𝑄, 𝐵, 𝐸 )
cluding headers, include paths, macros, and mandatory project
                                                                                      3    foreach 𝑔 ∈ 𝐺 do
configurations. AutoSOUP accepts the result only if deterministic
                                                                                      4         𝜌 ← ClassifyCoverageGap(𝑔, 𝑆𝑐 , 𝐵, 𝐸 )
checks confirm that the proof compiles, calls 𝐶𝑒 , and introduces no
                                                                                      5         (𝐵 ′ , 𝐸 ′ ) ← RepairCoverageGap(𝑔, 𝜌, 𝐵, 𝐸 )
preconditions beyond the intended type-directed initialization.
                                                                                      6         if ValidCoverageRefinement(𝑆𝑐 , 𝑄, 𝐵 ′ , 𝐸 ′ , 𝑅) then
 Step 2: Model external calls: AutoSOUP identifies call edges that                    7                (𝐵, 𝐸 ) ← (𝐵 ′ , 𝐸 ′ )
cross the current scope boundary and replaces their targets with
                                                                                             // Step 2: Expose loop-dependent property
simple type-based models. Primitive returns are modeled as un-
                                                                                                violations
constrained symbolic values, while pointer returns are modeled
                                                                                       8     𝐿 ← LoopsWithIncompleteUnwinding(𝑆𝑐 , 𝐵, 𝐸 )
as valid allocated objects to avoid irrelevant invalid-pointer states
                                                                                       9     foreach ℓ ∈ 𝐿 do
that inflate the solver state space. An LLM agent synthesizes and
                                                                                      10         𝑃ℓ ← LoopDependentProperties(ℓ, 𝑄 )
integrates these models from the recovered call graph and return
                                                                                      11         if 𝑃ℓ ≠ ∅ then
types; deterministic checks confirm that the resulting unit proof
                                                                                      12             𝑛 ← MinBoundToViolate(ℓ, 𝑃ℓ )
remains structurally valid.
                                                                                      13              𝐵 ′ ← 𝐵; 𝐵 ′ [ℓ ] ← max(𝐵 [ℓ ], 𝑛)
 Step 3: Widen the scope: AutoSOUP checks the provisional unit proof                  14              if ValidBoundRefinement(𝑆𝑐 , 𝑄, 𝐵 ′ , 𝐸, 𝑅) then
against the configured time, memory, and file-depth budgets. If ver-                  15                  𝐵 ← 𝐵′
ification remains within 𝑅, it widens 𝑆𝑐 by adding files that define
previously modeled callees, selecting among ambiguous definitions                     16     return (𝐵, 𝐸 )
XXX ’26, 2026, United States                                                                                                        Amusuo et al.


4.3     Property-Guided Loop & Model Refinement                           Algorithm 2: Context-aware environment model refine-
Property-guided refinement derives the bounds 𝐵 and model re-             ment. The algorithm infers approximate preconditions for
finements 𝐸 to exercise memory-safety-relevant behavior in 𝑆𝑐 . It        violated memory-safety properties, validates them against
uses the instrumented properties 𝑄 as the oracle for deciding which       calling contexts, and reports caller-feasible violations as
refinements matter. It honors the resource budget 𝑅 by increasing         memory-safety errors.
bounds or refining models only to cover property-relevant code or           Input: Software system 𝑆, component entry point 𝐶𝑒 , Environment
expose violations. Our technique has two steps (Algorithm 1).                      model 𝐸, Property violations 𝑄 𝑣
                                                                            Output: Refined environment model 𝐸, memory-safety error set M
 Step 1: Cover property-relevant code: A violation of 𝑞 ∈ 𝑄 can be
                                                                          1 Function ContextAwareEnvRefinement(𝑆, 𝐶𝑒 , 𝐸, 𝑄 𝑣 )
exposed only if the line containing 𝑞 is reached and checked. Cov-        2    M←∅
erage can be blocked by three factors: insufficient loop bounds,          3    W ← ParseViolationReport(𝑄 𝑣 )
missing compile-time configuration, or external-call side effects              // W contains tuples (𝑞, 𝑤 (𝑞) )
not captured by return-value-only models.                                 4    foreach (𝑞, 𝑤 (𝑞) ) ∈ W do
   AutoSOUP runs BMC in coverage mode, identifies uncovered               5         𝜙 ← InferApproxPrecondition(𝐸, 𝑞, 𝑤 (𝑞) )
property blocks, and uses an LLM agent to classify the blocking           6         (𝜙 ′ , B ) ← ValidatePrecondition(𝑆, 𝐶𝑒 , 𝑞, 𝜙 )
factor. It then applies the corresponding local repair: increase the      7         𝐸 ← 𝐸 ∪ {𝜙 ′ }
relevant loop bound, adjust the configuration, or refine the external     8         M←M∪B
model to write unconstrained symbolic values through affected
                                                                          9     return (𝐸, M )
pointer arguments. The taxonomy and repair rules constrain the
agent so that refinements remain local and aligned with the tech-        10 Function ValidatePrecondition(𝑆, 𝐶𝑒 , 𝑞, 𝜙 )
nique. A refinement is accepted only if the unit proof remains           11    B ← ∅; 𝜙 ′ ← 𝜙
semantically valid, the target block becomes covered, and overall        12    C ← CallsitesOf(𝐶𝑒 , 𝑆 )
verification coverage does not decrease.                                 13    foreach 𝑐 ∈ C do
                                                                         14        𝜓𝑐 ← PathConstraints(𝑐, 𝑆 )
 Step 2: Expose loop-dependent property violations: Covering a prop-
                                                                         15        if 𝜓𝑐 ̸ |= 𝜙 ′ then
erty does not imply that the current loop bounds can expose its
                                                                         16            𝜙ˆ ← WeakenPrecondition(𝜙 ′ ,𝜓𝑐 )
violation. AutoSOUP inspects loops from the coverage report whose                                            ˆ 𝑞) then
                                                                         17            if SatisfiesProperty(𝜙,
current bounds were insufficient for complete unwinding. For each
                                                                         18                   𝜙 ′ ← 𝜙ˆ
such loop, it uses an LLM agent to determine whether the loop
                                                                         19              else
can affect violation of a nearby memory-safety property and, if so,
                                                                         20                     B ← B ∪ { (𝑞,𝜓𝑐 , 𝜙 ′ ) }
to estimate the minimum bound likely to expose a violation. The
prompt constrains this estimation using local program semantics,         21     return (𝜙 ′ , B )
such as memory-region size, access stride, allocation constraints,
and loop guards. A proposed bound is accepted only if it modifies
the intended loop bound and preserves structural validity, conclu-
siveness, and verification coverage. If the bound causes verification    𝑤 (𝑞). For each tuple (𝑞, loc(𝑞), 𝑤 (𝑞)), an LLM agent infers a pre-
to exceed 𝑅, AutoSOUP reports the bound but does not apply it.           condition that keeps loc(𝑞) covered but suppresses the violation of
                                                                         𝑞. The prompt guides the agent to identify the violated condition,
                                                                         propagate it backward through local dataflow and path constraints,
4.4     Context-Aware Env. Model Refinement                              and stop at the external model or input responsible for the value.
Property-guided refinement in §4.3 maximizes exposure of viola-          The agent can inspect witnesses, navigate code, and test candidate
tions of 𝑄 using permissive models 𝐸. However, violations found          preconditions. A candidate is accepted only if it suppresses the tar-
under permissive models may be infeasible in the broader system 𝑆.       get violation without reducing structural validity, conclusiveness,
For example, the assertion on Program Line 15 in Listing 1 is violated   coverage, or the number of checked properties.
if the input model provides a null pointer, even if the actual caller     Step 2: Validate and refine against calling contexts: An inferred pre-
provides a statically allocated array. Our context-aware environ-        condition may exclude feasible caller states that would not violate
ment refinement separates infeasible violations (caused by overly        𝑞, or it may reveal that the surrounding program can trigger the
permissive environment assumptions) from genuine memory-safety           violation. AutoSOUP therefore validates each accepted precondi-
errors. This technique operates in two steps (Algorithm 2).              tion against calling contexts in 𝑆. Using a pre-indexed call graph,
 Step 1: Infer approximate weakest preconditions: Following counter-     it identifies callsites of 𝐶𝑒 and implementations of modeled func-
example-guided environment refinement, AutoSOUP infers precon-           tions. For each context, an LLM agent identifies path constraints
ditions that suppress reported violations of memory-safety prop-         reaching the callsite or implementation and checks whether those
erties. These preconditions need not be logically weakest, since         constraints imply the inferred precondition.
weakest-precondition inference is often computationally expen-               Validation has three outcomes. If a calling path violates the pre-
sive [23]. Instead, they should be weak enough to preserve safe          condition but still satisfies 𝑞, the agent weakens and revalidates the
states while strong enough to suppress the target violation.             precondition. If the precondition holds across the checked contexts,
    AutoSOUP parses the verification report to extract each violated     it becomes an explicit assumption in 𝐸. And of course, if a calling
property 𝑞 ∈ 𝑄, its location loc(𝑞), and its counterexample witness      path violates the precondition and triggers 𝑞, AutoSOUP reports
AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification                                     XXX ’26, 2026, United States


the path as a feasible memory-safety error in 𝑆. These assumptions                    LLM-driven modules: AutoSOUP implements its LLM-driven mod-
make the generated unit proof auditable: the component is verified                   ules using the OpenAI Python SDK [2] and LiteLLM [1]. The Ope-
only under the preconditions recorded in its environment model.                      nAI SDK provides access to the GPT-family models used in our
                                                                                     evaluation, while LiteLLM supports additional providers, including
                                                                                     open-source and self-hosted models.
4.5     Guarantees and Limitations                                                      We expose three tools to the agents: (i) a containerized termi-
We discuss the guarantees and limitations of AutoSOUP.                               nal tool lets agents inspect source files, build logs, and verification
                                                                                     reports; (ii) a cscope-based navigation tool supports code search,
4.5.1 Guarantees. Unit proofs generated by AutoSOUP provide                          definition lookup, and call-graph queries; and (iii) a unit-proof vali-
bounded formal guarantees of memory safety, backed by BMC.                           dation tool analyzes the compiled unit and verification report after
They establish that no execution from the component entry point                      each proposed change to confirm the proof compiles, calls the target
violates a verified memory-safety property, provided the execution                   entry point, satisfies the requested refinement task, and does not
stays within the scope, loop bounds, and assumptions encoded in the                  reduce line coverage or the number of covered or verified proper-
unit proof. This is the same form of guarantee provided by expert-                   ties.
written unit proofs [24]; its strength depends on the correctness
and completeness of the encoded verification choices. AutoSOUP                       5     Evaluation
strengthens these choices by expanding safety-relevant scope, in-                    We structure our evaluation with four research questions:
creasing bounds needed to expose property-relevant behavior, and
                                                                                           • RQ1: Can AutoSOUP generate useful unit proofs for memory-
making environment assumptions explicit.
                                                                                             safety verification?
                                                                                           • RQ2: Are memory-safety-oriented unit proofs effective at
4.5.2 Limitations. Three limitations constrain these guarantees.                             exposing memory-safety vulnerabilities?
First, AutoSOUP uses LLMs for project-specific reasoning. To re-                           • RQ3: How do AutoSOUP’s safety-oriented techniques con-
duce unreliable outputs, deterministic workflows issue bounded                               tribute to its performance and cost?
tasks and validate outputs before incorporating them into the unit                         • RQ4: Do AutoSOUP-generated unit proofs differ from those
proof. As program analyses improve, these modules can be replaced                            of experts?
with deterministic techniques. Second, AutoSOUP relies on static
analysis to recover call graphs for scope widening and precondi-                     5.1         Evaluation Setup
tion validation. Imprecision, especially around indirect calls, may
cause AutoSOUP to miss relevant call edges; engineers can reduce                      Subjects: Following prior works on validating embedded software [12],
this risk by providing accurate application call graphs. Third, Au-                  we evaluate AutoSOUP using four widely-used open-source em-
toSOUP widens scope at file granularity. Large files may exceed 𝑅                    bedded operating systems: Zephyr RTOS, RIOT OS, Contiki-NG and
and prevent wider scopes from being explored.                                        FreeRTOS. These operating systems are substantial (Table 7), includ-
                                                                                     ing task management, IPC, networking, and storage subsystems.
                                                                                     We considered including downstream embedded applications but
4.6     Implementation                                                               their source code is often not publicly available [61].
We implement AutoSOUP in 15463 lines of Python and 1230 lines of                      Vulnerability selection: To assess AutoSOUP’s effectiveness to ex-
prompts. Resource-aware scope widening uses 1227 lines of Python                     pose security vulnerabilities, we identify and recreate 60 known
and 292 prompt lines; property-guided loop-bound refinement uses                     CVEs in selected subjects. To ensure reliable recreation, we extract
775 lines of Python and 316 prompt lines; and context-aware en-                      CVEs affecting each software from the National Vulnerability Data-
vironment refinement uses 1091 lines of Python and 479 prompt                        base and identify the first 20 CVEs where the vulnerable function
lines.                                                                               still exists and the security advisory provided details of the vul-
 Bounded model checking: AutoSOUP uses the ANSI-C Bounded                            nerability sink and the fixing commit. The FreeRTOS CVEs in our
Model Checker (CBMC) [46] as its verification backend. AutoSOUP                      dataset did not provide the fixing commits and were excluded. We
can be used with most bounded model checkers with memory-                            re-expose each CVE by applying a patch to reverse the changes
safety instrumentation, as elaborated in §E.                                         in the identified fixing commit. For each CVE, we also record the
                                                                                     vulnerability type, affected function, and sink location, to enable
 Program-analysis modules: AutoSOUP integrates components for
                                                                                     exposure detection.
deterministic program analysis. We use CBMC’s goto-instrument
to extract call-graph and symbol information from the compiled                        Verification targets: Component-level verification require entry points
verification scope, which lets AutoSOUP check that the unit proof in-                through which the components would be verified. We identify these
vokes the target entry point and identify undefined external callees                 entry points in three steps. First, we include the 57 functions affected
during scope widening. We use libclang to locate function-pointer                    by the 60 selected CVEs 1 . Second, to assess generalizability beyond
calls in the verification scope, allowing AutoSOUP to constrain                      known vulnerable functions, we randomly select an additional 100
them to selected models or concrete targets. We use cscope to index                  functions across the four embedded OSes. First, we identify five
the software system 𝑆, recover project-level call relations, locate                  modules in each operating system that handle untrusted data, such
candidate function definitions, and identify calling contexts for
validating inferred preconditions.                                                   1 3 functions contained 2 CVEs each
XXX ’26, 2026, United States                                                                                                        Amusuo et al.


as bluetooth, network and USB modules. For each module, we per-               We also measure the cost and size of each unit proof. For cost,
form an attack surface analysis to identify sources of untrusted           we record total generation time and API cost. For size, we record
data and the functions that process them. We select 5 functions            proof size in lines of code, including both harness function and all
per module, yielding an additional 25 functions per OS. Finally,           function models. Following prior work on unit testing [28, 62], we
we select 20 FreeRTOS functions with expert-written harnesses              use unit proof size as a proxy for maintainability.
to enable head-to-head comparison in RQ4. Our component entry                 For comparison, we run Codex and Seeker on the verification
point set thus has a total of 177 entry points. Table 7 shows the          targets with recreated vulnerabilities and report the corresponding
parent modules containing the selected entry points.                       measurements when available. For Codex, we use a prompt that
 Baselines.: We compare AutoSOUP against two categories of base-           states the goal of unit proof creation and the success criteria in
lines. First, we compare against alternative methods for producing         §3.1, but gives no specific guidance on how to derive verification
unit proofs, including expert-written FreeRTOS proofs and proofs           choices. This baseline tests whether a general-purpose AI coding
generated by vanilla coding agents (GPT Codex). This comparison            agent can independently produce unit proofs that support useful
evaluates differences in verification choices and resulting outcomes.      memory-safety guarantees. For Seeker, we extract the compila-
Second, we compare against memory-safety verification techniques,          tion configurations from AutoSOUP-generated unit proofs and the
using Seeker [64], a recent open-source verifier for memory safety         scripts provided in the Seeker artifact to compile and verify the
of open programs. Seeker is the closest prior system to our setting.       target file. To validate our setup, we sampled benchmarks from the
We defer conceptual comparisons with other verification methods            Seeker codebase and confirmed that our instrumented programs
to §6.2.                                                                   matched the artifact versions and produced identical verification
 Hardware and AI models: We run experiments on dedicated servers           results.
(32 virtual CPUs, 188GB of RAM). We use gpt-5.3-codex through
their API for our evaluation, as it ranked among the best AI models        5.2.2 Result. Unit proof validity: Table 1 compares the validity,
for coding [4] at time of study. We configure with the default tem-        verification outcomes, and generation cost of unit proofs produced
perature (1.0) and reasoning effort (high). To assess generalizability     by AutoSOUP and CodexUP. AutoSOUP produced substantially
to open-source models, we compare against Minimax M2.5 and                 more valid unit proofs than Codex: 93%, 89.5% and 91.7% for scope
GLM-5, two leading open-source models for coding [4].                      levels 1 and 2 and the randomly selected targets, respectively, com-
                                                                           pared with 31.6% for CodexUP. In Seeker, of the 57 targets, 12 (21.1%)
 AutoSOUP configuration: We evaluate two AutoSOUP configura-               returned an error while 23 (40.4%) timed out.
tions that differ in the maximum scope level used by resource-aware           Most Codex proofs were structurally invalid because Codex often
scope widening (§4.2). Scope-1 (S1) widens only to scope level of          failed to compile or verify the target, due to missing compilation,
one (parent file containing entry point). Scope-2 (S2) uses depth          incomplete environment models or initially large loop bounds, and
two (parent file and all adjacent files). For each verification run,       instead created simpler copies to verify. Seeker more often returned
we use a 30-minute timeout, a practical budget under which most            errors when it could not process the source file and timed out more
component-level verification tasks complete. We use the default            often because it assigned a uniform bound of 20 to all loops and did
configurations for the baseline techniques.                                not create valid environment models that reduce the state space.
                                                                           This shows that AutoSOUP’s structured refinement and validation
                                                                           are necessary to produce unit proofs that compile, reach the target,
5.2     RQ1: Are AutoSOUP’s Results Useful?
                                                                           and complete verification.
§3.1 identifies five properties that unit proofs must satisfy to support      The lower success rate of AutoSOUP-S2 relative to AutoSOUP-S1
useful verification guarantees: structural validity, conclusiveness,       is expected. Increasing the scope level adds more adjacent code to
verification coverage, result validity and maintainability. RQ1 eval-      the verification target, which increases program size, state space,
uates the first three and last properties. We defer result validity to     and verification time.
RQ2.                                                                          Verification outcomes and assurance: Among valid unit proofs,
                                                                           AutoSOUP, at scope levels 1 and 2, covered and verified 88.2% and
5.2.1 Method. We evaluate RQ1 on the full set of selected com-             155% more lines of code compared to Codex’ 57.8 lines of code.
ponent entry points and use both AutoSOUP configurations. We               Data from Seeker is excluded as it does not provide coverage report.
run AutoSOUP-S1 on all verification targets and AutoSOUP-S2 only           Table 1 also provides the number of total and verified properties
on targets with recreated CVEs because its wider scope increases           as reported by the tool. However, because it counts the proper-
generation and verification cost. We terminate generation runs that        ties in non-covered code as verified because no violation was pro-
exceed 24 hours.                                                           duced, Codex substantially lower coverage led to a higher number
   For each generated unit proof, we measure whether generation            of reported verified properties. These results show that AutoSOUP
completes, whether the proof compiles, whether it is semantically          also outperforms frontier coding agents in generating unit proofs
valid, and how long verification takes. We then measure the verifica-      that achieves better verification coverage and provides stronger
tion outcome: the total lines of code in functions statically reachable    memory-safety assurances.
from the unit proof, the proportion of those lines covered under the          The remaining uncovered code was primarily caused by state-
proof bounds and assumptions, the total number of instrumented             ments that were not statically reachable from the generated unit
memory-safety properties, and the proportion of those properties           proof, even when their enclosing functions were reachable. This
verified.                                                                  effect becomes more pronounced as scope level increases and the
AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification                                                                                   XXX ’26, 2026, United States


Table 1: Comparison of unit proofs produced by AutoSOUP                                                                                                              3500




                                                                                          Component Coverage (loc)
                                                                                                                     500
                                                                                                                                                                     3000




                                                                                                                                             Verification Time (s)
at scope level 1 and 2 and by CodexUP. Random represents
                                                                                                                     400                                             2500
targets selected to assess generalizability. We report results                                                                                                       2000
                                                                                                                     300
from Seeker baseline in the prose. Below the double-line, we                                                                                                         1500
                                                                                                                     200
consider only the unit proofs from successful runs for each                                                                                                          1000
                                                                                                                     100                                              500
method.
                                                                                                                       0                                                0
                                                                                                                           S1   S2   Codex                                  S1            S2        Codex
 Metric                              S1        S2       Codex      Random                                    2500                                                      30




                                                                                     Generation Time (min)
                                                                                                             2000                                                      25
 Num Targets                         57        57         57           84 2




                                                                                                                                                        API Cost ($)
                                                                                                                                                                       20
 Struct. valid (%)                  93%       89.5%      31.6%        91.7%                                  1500
                                                                                                                                                                       15
 Verification completes (%)        96.5%      91.2%      70.2%        76.2%                                  1000
                                                                                                                                                                       10
 Generation succeeds (%)           93.0%      78.9%      98.2%         75%                                           500                                                5
                                                                                                                       0                                                0
 Verification time (s)              137.9     249.1       37.4         17.7                                                S1   S2   Codex                                  S1            S2        Codex
 Avg compon. size (loc)             126.1     418.9      132.5        107.7
 Avg covered size (loc)             108.8     147.4       57.8         88.8             Figure 3: Distribution of program reachable LOC, verification
 Avg num. properties (#)            382.4    1187.2      468.3        243.2             time, development time, and API cost for the RQ1 unit proofs.
 Avg prop. verified (#)             369.5    1185.3      465.1        242.7
 Avg reported errors (#)             4.7       3.2        1.6          1.2
                                                                                           Counting a vulnerability as exposed is non-trivial. During context-
 Avg gen. time (min)                129.8     363.7       10.1         45.0
                                                                                        aware environment refinement (§4.4), AutoSOUP infers underap-
 Avg API cost ($)                    3.0       5.9        0.8           1.8
                                                                                        proximate preconditions that suppress reported property violations.
 Avg proof size (loc)               34.1      40.1        50.7         27.3             A precondition inferred for one violation may also suppress other
                                                                                        violations that share the same root cause. As a result, the viola-
                                                                                        tion location recorded by AutoSOUP may differ from the CVE sink
proof includes functions from adjacent files. AutoSOUP neverthe-                        location defined in §5.1, even when both correspond to the same
less achieved higher coverage than CodexUP because its generated                        vulnerability.
proofs are designed to admit all valid reachable states. By contrast,                      We therefore count a vulnerability as exposed if any of the fol-
CodexUP often introduced restrictive assumptions in its unit proofs                     lowing holds: (i) AutoSOUP reports a memory-safety error at the
that excluded feasible states, reducing both code coverage and the                      recorded CVE sink, and the inferred precondition can be violated
corresponding number of properties checked.                                             at the component callsite; (ii) AutoSOUP reports a memory-safety
   Unit proof generation cost: Generating AutoSOUP unit proofs                          error at a different sink, the inferred precondition can be violated at
required 2.16 and 6.06 hours on average for scope levels 1 and 2,                       the callsite, and violating it would also trigger a property violation at
respectively, and cost $3 and $5.9 in API usage. These costs are                        the recorded CVE sink; or (iii) AutoSOUP reports a memory-safety
higher than CodexUP, but they produce substantially more valid                          error at the recorded CVE sink without inferring a precondition
and useful proofs. They are also modest relative to prior human-                        that suppresses the error.
driven unit proofing effort, where verifying 1,500 lines of code                           We identify the first and third cases automatically by compar-
required about one person-month of work [24].                                           ing recorded CVE sink locations with the memory-safety errors
   Figure 3 shows that the cost of AutoSOUP was distributed across                      reported by AutoSOUP. We identify the second case manually by
the unit proofs. Overall, increasing the scope level from 1 to 2                        checking whether removing the inferred precondition produces a
increased the size of verified code, together with the development                      property violation at the recorded CVE sink. Finally, we compare
costs. Our data also showed these costs correlated closely with                         the proportion of CVEs exposed by AutoSOUP, Codex, and Seeker,
component size: larger component sizes took longer to verify, which                     and manually categorize missed vulnerabilities to understand lim-
increased the iterative-refinement-based development time.                              itations of our techniques and those of the underlying bounded
                                                                                        model checker.
5.3     RQ2: Does AutoSOUP Find Vulnerabilities?                                        5.3.2 Result. Exposure of known CVEs: Table 2 reports the pro-
§3.1 requires unit proofs to produce valid memory-safety results:                       portion of recreated CVEs exposed by each method and summarizes
their verification outcomes should reflect genuine memory-safety                        the reasons for non-exposure. AutoSOUP-S1 and AutoSOUP-S2 ex-
vulnerabilities in the verified component. RQ2 evaluates whether                        posed 66.7% and 65% of CVEs, respectively. In contrast, Codex and
unit proofs generated by AutoSOUP expose known memory-safety                            Seeker exposed only 28.3% and 41.7% 3 . These results show that
vulnerabilities during verification.                                                    AutoSOUP exposes substantially more known vulnerabilities than
                                                                                        both a general-purpose coding agent and the prior verification
5.3.1 Method. We evaluate RQ2 on verification targets with recre-                       baseline.
ated vulnerabilities. We compare AutoSOUP against the baselines
using the proportion of vulnerabilities exposed and the root causes                     3 For Seeker, due to limited information it provides, we counted any violation corre-
of any missed vulnerabilities.                                                          sponding to the CVE sink line as exposure
XXX ’26, 2026, United States                                                                                                        Amusuo et al.


Table 2: Exposure rate of known vulnerabilities. S1 and S2                Table 3: New vulnerabilities discovered using AutoSOUP.
represents AutoSOUP configured at scope levels one and two                Each count is reported as Total (Contiki-NG, Zephyr, RIOT).
respectively.
                                                                                        Vulnerability Type             Count
       Metric                      S1    S2   Codex     Seeker
                                                                                        Out-of-bound write           9 (5, 1, 2)
       Number of CVEs              60    60     60        60                            Out-of-bound read            7 (2, 3, 2)
       Number exposed              40    39     17        25                            Undefined shift behavior     2 (1, 1, 0)
       Unexploitable                6     5     1          -                            Null pointer dereference     1 (1, 0, 2)
       Compilation error            3    4      6          -                            Total                        20 (9, 5, 6)
       Structural invalidity        0    0      2          -
       Resource exhaustion          1    2      17         -
       Limited scope                3    0      2          -              memory-safety violations where inferred preconditions were vio-
       Limited loop unwinding       1    3      0          -              lated. After reviewing a subset of these reports, we confirmed 20
       Inaccurate env. model        2    0      14         -              new externally triggerable vulnerabilities (Table 3). Nine of these
       Unsupported sink             2    2       1         -              are out-of-bound write vulnerabilities, with potentials to cause
       BMC field granularity        2    4       0         -              denial of service or arbitrary code execution. Another 7 are out-of-
                                                                          bound reads, which can potentially lead to information disclosure
                                                                          attacks. Details of one vulnerability is in §F. We reported all con-
   Root causes of non-exposure: We classify non-exposure into             firmed vulnerabilities to the corresponding maintainers. One has
three categories. First, some unit proofs were invalid or inconclusive,   been fixed and assigned a CVE. Another 4 were fixed without CVE
preventing verification from producing a useful result. Second, some      assignment because maintainers considered exploitation to require
proofs used insufficient verification choices, such as scopes that        prior compromise of the downstream embedded application, which
excluded vulnerability-relevant paths, loop bounds that were too          was outside their threat model. The remaining reports are still under
small, or environment assumptions that ruled out vulnerable states.       investigation.
Third, some cases were limited by the underlying bounded model               Sample out-of-bound write vulnerability in RIOT-OS: List-
checker, even when the relevant code and triggering conditions            ing 4 illustrates a vulnerability in RIOT-OS nanocoap.c discovered
were present.                                                             by AutoSOUP. AutoSOUP first generated a harness for the root func-
   For AutoSOUP-S1, missed CVEs were primarily caused by limited          tion coap_opt_put_uri_pathquery, initializing buf and string
scope, CBMC limitations, or vulnerabilities that were not triggerable     as nondeterministic pointers with unconstrained sizes. Stage 2 re-
from the project context. The scope-related misses were resolved          fined the proof bounds and models until verification reached the
by AutoSOUP-S2, showing that scope widening is important for              vulnerable memcpy on Line 33, where a memcpy write violation was
exposing vulnerabilities whose triggers cross file boundaries.            exposed. Finally, Stage 3 inferred a precondition on the input-buffer
   The CBMC limitations appeared in two forms. First, CBMC re-            length that would eliminate the violation, but the validator traced
ports a spatial memory-safety violation only when an access leaves        the constrained string back to the nanocoap_sock_post public API
the allocated object. However, for structs, AutoSOUP’s property-          and found no corresponding length check. AutoSOUP therefore
guided loop-bound analysis computes the bound needed to overflow          classified the precondition as violable in the real environment and
the destination field, not necessarily the containing object. Thus,       reported the memcpy out-of-bounds write vulnerability.
when a write overflows a struct field but remains within the same
allocated struct object, CBMC does not report a violation. Second,        5.4    RQ3: Ablation of AutoSOUP’s Techniques?
2 vulnerabilities was missed because they required semantics that         We ablate the techniques used to derive our safety-oriented unit
CBMC did not model. One was a memory-leak, missed because the             proofs: verification scope, loop bounds, and environment models.
corresponding custom deallocator is not supported. The second
required timer semantics for exposure.                                    5.4.1 Method. During the RQ1 runs, we save a unit proof snapshot
   In cases we tagged unexploitable, AutoSOUP reached the CVE             after each technique completes. For each snapshot, we also record
sink and inferred the relevant precondition, but the precondition         the technique’s execution time and API cost.
was valid in the component’s calling context, either due to upstream         We use these snapshots to measure how each technique changes
constraints or default program configurations.                            the unit proof. Specifically, we measure changes in verification
   Codex missed CVEs mainly because its unit proofs were invalid,         scope, loop bounds, and environment models. We then execute
inconclusive, or over-constrained. Its ad hoc proof generation often      each snapshot and measure the resulting verification coverage, the
produced scopes that did not support conclusive verification or           number of reachable memory-safety properties, and the proportion
assumptions that excluded vulnerable states. We could not investi-        of those properties verified. This allows us to isolate how each
gate Seeker misses because no coverage report or unit proofs were         verification choice affects verification outcomes and to estimate the
produced.                                                                 marginal cost of each technique.
   Exposure of new vulnerabilities: During unit proof genera-                Finally, we compare generalizability to open-source models. We
tion, AutoSOUP scope levels 1 and 2 reported 63 and 99 potential          execute the 37 targets in RIOT and Contiki-NG using AutoSOUP
AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification                                     XXX ’26, 2026, United States


Table 4: Stage-wise contribution of AutoSOUP’s scope, loop-                          refinement separates feasible violations from behaviors ruled out
bound, and environment-modeling stages to harness struc-                             by the component context.
ture, verification behavior, development time, and API cost.                            Generalizability to open-source models: Table 6 in §G eval-
                                                                                     uates AutoSOUP with open-source models. Across 37 test cases,
 Metric                                   Stage 1      Stage 2     Stage 3           unit proof generation succeeded for 78.4% with GLM-5 and 48.6%
                                                                                     with Minimax M2.5, compared to 93% with GPT-5.3-Codex. Their
 Harness Size (LOC)                         6.613       7.795       21.64
                                                                                     average costs were $4.9 and $0.7, respectively, compared to $3 for
 Proof Size (LOC)                           18.74       25.76       44.81
                                                                                     GPT-5.3-Codex. These results show that AutoSOUP can generalize
 # Functions In Scope                       17.78       18.84       17.34            to open-source models, but its performance depends on model ca-
 # Custom Loop Bounds                       0.004       0.909       0.842            pability. As open-source models improve, we expect corresponding
 # Variable Models                          0.044       0.068       3.424            gains in AutoSOUP’s performance with them.
 # Function Models                          1.351       1.938       2.119
 Avg Function Model Size (LOC)              2.954       3.602       5.402
 Component Size (LOC)                       209.8       220.8       196.3            5.5         RQ4: AutoSOUP vs. Expert-Written Proofs?
 Verification Coverage (LOC)                94.06       139.6       115.8            RQ4 compares unit proofs generated by AutoSOUP with existing
 Total Properties                           542.8       580.0       539.0            FreeRTOS proofs. We restrict this analysis to FreeRTOS because it
 Verified Properties                        412.3       412.8       531.6            is the only evaluation subject with unit proofs developed by project
 Generation Time (min)                      6.054       39.99       141.5            maintainers.
 API Cost ($)                               0.296       0.743       2.602
                                                                                     5.5.1 Method. We first compare verification choices and outcomes
                                                                                     quantitatively. For verification choices, we measure proof size,
                                                                                     verification-scope size, distinct loop bounds, and the number of
configured at scope level 1 and equipped with the selected open-                     variable and function models. For outcomes, we measure verifica-
source models, Minimax M2.5 and GLM-5. Similar to RQ1, we mea-                       tion time, component size, verification coverage, the number of
sure the validity of produced unit proofs, their verification outcomes               verified properties, and the number of violated properties.
and the generation cost.                                                                We then qualitatively analyze the environment models using
                                                                                     the taxonomy from prior work [12]. Variable models fall into four
5.4.2 Result. Contribution and cost of each technique: Table 4                       categories: null-pointer preconditions (p != NULL), pointer-offset
summarizes how each AutoSOUP stage changes the unit proof,                           preconditions (p2 = p1 + offset), variable-constant preconditions
affects verification outcomes, and contributes to generation cost.                   (var >= CONSTANT), and variable-variable preconditions (var1 >=
Overall, the results show that the three techniques are complemen-                   var2). Function models fall into three categories: Type 1 models
tary: each stage introduces a distinct class of verification choices                 with no preconditions, Type 2 models with preconditions only on
and improves a different aspect of the final proof.                                  return values, and Type 3 models with preconditions on inputs
   Stage 1 (resource-aware scope widening) determines the reach-                     or global variables. We classify each model and compare the as-
able functions included in the proof and introduces models for                       sumptions encoded by AutoSOUP-generated and expert-written
undefined functions. These choices remain largely unchanged in                       proofs.
later stages. This stage is also the cheapest because it is implemented                 Finally, we conduct a case study of three randomly selected
primarily using deterministic program analysis.                                      functions with varying proof sizes. We inspect their loop bounds
   Stage 2 (property-guided loop refinement) increases the number                    and environment models to explain observed differences and their
of per-loop bounds. This expands the explored behavior of the                        implications for verification.
component, which increases both verification coverage and the
number of reachable memory-safety properties. At this stage, up
to 71.04% of reachable properties on average are violated under the                  5.5.2 Result. Quantitative comparisons: Figure 4 compares the
unconstrained environment, showing that loop unwinding exposes                       verification choices and outcomes. Overall, AutoSOUP-generated
safety-relevant behaviors that must later be checked or constrained.                 unit proofs are smaller, use smaller verification scopes, include more
This stage takes 39.99 minutes and costs $0.743 on average.                          variable models and fewer function models, and achieve comparable
   Stage 3 (context-aware environment refinement) primarily re-                      verification coverage. This difference stems from two design choices.
fines the variable and function models to eliminate infeasible execu-                First, AutoSOUP uses preconditions to constrain environment vari-
tions while preserving safety-relevant behavior. This allows 98.63%                  ables, whereas FreeRTOS proofs often call project functions to
of reachable properties to be verified and produces the environment                  initialize or constrain state, such as the proof for vDHCPProcess
assumptions under which the verification holds. It is also the most                  using prvCreateDHCPSocket to initialize DHCP sockets. Second,
expensive because AutoSOUP infers and validate preconditions for                     FreeRTOS proofs often replace same-file callees with function mod-
reported property violations one by one.                                             els and reuse shared function models across proofs. In contrast,
   Together, these results explain AutoSOUP’s performance. Scope                     AutoSOUP keeps same-file callees in scope and creates models only
widening determines what code is analyzed, loop unwinding ex-                        for functions outside the entry point’s parent file, resulting in fewer
poses safety-relevant behaviors within that code, and environment                    function models.
XXX ’26, 2026, United States                                                                                                     Amusuo et al.


                                                                      at lower cost, but target narrower classes of properties than the
                                                                      bounded memory-safety guarantees studied in this paper. In con-
                                                                      trast, AutoSOUP automates these choices and makes them explicit,
                                                                      while providing bounded memory-safety guarantees. RQ2 (§5.3)
                                                                      shows that this tradeoff is useful in practice: AutoSOUP exposes
                                                                      66.7% of recreated CVEs and reports the assumptions under which
                                                                      each verified component is memory safe. It is also substantially
                                                                      cheaper than prior industry experience where expert-written proofs
                                                                      take one engineer-month to cover 1500 lines of code. Although Au-
                                                                      toSOUP does not replace stronger verification methods for safety-
                                                                      critical certification, it lowers the cost of memory-safety verification
                                                                      for broader software teams.
                                                                       Integration in developer workflow.: AutoSOUP makes component-
Figure 4: Comparing AutoSOUP’s unit proofs with expert-
                                                                      level verification more practical for low-level software projects.
written ones. Top measures verification choices. Bottom mea-
                                                                      RQ1 (§5.2) shows that it can generate unit proofs and verify com-
sures verification outcomes.
                                                                      ponents in realistic embedded software. This supports a practical
                                                                      shift-security-left workflow [60]: developers can obtain formal evi-
Table 5: Categorization of environment models from unit               dence about component memory safety during development, when
proofs. Data is aggregated from 20 unit proofs each. Top              defects are cheaper to diagnose and fix [3]. Our aeronautics indus-
section represent variable model categories, while bottom             try partners noted that this capability is especially valuable in long
section is for function models.                                       development cycles, where products may take up to seven years to
                                                                      complete. In addition, by making environment assumptions explicit
         Model category        Expert-written   AutoSOUP              in the unit proof, AutoSOUP also exposes the interface contracts
                                                                      under which a component is memory safe. This will help developers
        pointer-not-null             65            62
                                                                      identify and validate the caller-side obligations whose violation
          pointer-offset             2             1
                                                                      often leads to component-interface vulnerabilities [49].
        variable-constant            38            70
        variable-variable            3             8                   Implications and future directions.: AutoSOUP also illustrates a path
                                                                      for trustworthy AI-assisted software engineering. As developers
          Type 1 models              58            23                 increasingly use AI agents to generate and modify code, tools like
          Type 2 models              18            19                 AutoSOUP can provide machine-checkable evidence that generated
          Type 3 models              0             2                  components are memory safe under explicit assumptions. Its LLM-
                                                                      as-function-call architecture also allows model improvements to
                                                                      strengthen LLM-driven subtasks without weakening the determin-
   Qualitative comparisons: Table 5 shows the distribution of         istic orchestration and validation framework. This matters because
model categories. Although AutoSOUP introduces 90% more pre-          formal guarantees depend on the assumptions encoded in the verifi-
conditions than the expert-written proofs, most are simple: non-      cation task [36], and automatically judging the correctness of these
null pointer constraints or fixed upper and lower bounds on en-       assumptions remains an open problem [15].
vironment variables needed for memory safety. Thus, AutoSOUP-             Looking forward, extending AutoSOUP from component-level
generated environment models are comparable to expert-written         memory-safety verification to broader project-level assurance re-
models, making them auditable and maintainable. Case studies com-     quires three advances. First, loop unwinding should be combined
paring specific unit proofs are in §D. Sample AutoSOUP-generation     or replaced with loop invariant generation [59] to expose vulnera-
unit proof is in Listing 2.                                           bilities whose required bounds exceed the resource budget. Second,
                                                                      whole-project verification requires techniques that select effective
6     Discussion and Related Work                                     component entry points, reduce bound or environment refinement
We discuss implications for practitioners and researchers and com-    cost with program analysis, and compose component-level results
pare our work to related lines of research.                           into project-level guarantees [17, 23]. Third, generalizing beyond
                                                                      memory safety requires techniques that automatically infer system
6.1     Discussion                                                    and security properties that can be verified using bounded model
 Guarantees, cost, and practicality.: AutoSOUP occupies a practical   checking. Novel AI-driven techniques can help infer them from
                                                                      existing specifications, comments, and unit tests [48], then encode
middle ground in the software-verification landscape. Deductive
                                                                      them as safety properties for verification.
verification [34] can prove rich functional and memory-safety prop-
erties, but requires substantial specifications, annotations, and
proof effort. Expert-written unit proofs for bounded model check-
ing [24, 70] can provide useful memory-safety guarantees, but
require experts to define scopes, loop bounds, inputs, and envi-      6.2    Related Work
ronment models. Automated analyzers such as Infer [20] operate        We situate our work within three lines of research.
AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification                                XXX ’26, 2026, United States


 (1) Automating component-level BMC: Prior work has explored au-                     Acknowledgments
tomating bounded model checking through compositional veri-                          Davis and Machiry acknowledge funding from Rolls Royce. Amusuo
fication [23, 40]. These techniques decompose programs along                         and Anandayuvaraj acknowledge funding from the Qualcomm
call-graph or control-flow edges, infer preconditions under which                    Innovation Fellowship. All authors acknowledge API credits from
each fragment is safe, and discharge the resulting obligations us-                   OpenAI.
ing assume-guarantee reasoning [26]. However, it remains unclear
whether these techniques scale to real-world systems with large
components, diverse coding patterns, and complex inter-component
relationships. Other work targets open programs, where compo-
nents have undefined dependencies, and refines their environments
using expert-provided precondition templates [29, 64]. Our evalua-
tion shows that such templates can be imprecise and incomplete,
compromising the resulting verification guarantees. In contrast, Au-
toSOUP automates industry-adopted component-level verification
workflow and derives the scope, loop bounds, and environment
models needed for practical memory-safety verification. The de-
rived choices can also support compositional and open-program
verification methods.
 (2) LLMs and the verification-oracle problem: Large language mod-
els are increasingly used to automate software-verification tasks, in-
cluding tactic generation for deductive verification [35, 44, 72], pre-
condition and loop-invariant inference for bounded model check-
ing [59], and repair of verification failures [65]. In these settings,
the LLM usually acts as the main driver and the task has a clear
success oracle: the generated artifact is accepted if verification
succeeds. AutoSOUP addresses a harder oracle problem because
successful verification is not sufficient when unjustified choices
of scope, bounds, or environment assumptions can make verifi-
cation succeed without providing appropriate guarantees. Thus,
AutoSOUP uses LLMs as assistants inside program-analysis-driven
workflows: deterministic orchestrators issue small tasks aligned
with specific algorithms and validate each result before incorporat-
ing it into the unit proof. This architecture may also apply to other
security and software-engineering tasks, such as fuzzing, where
AI-generated harnesses can compile and achieve coverage yet still
produce false crashes or invalid results [13, 71, 74].
 (3) Security vulnerability detection: AutoSOUP complements static
analysis [22, 31] and dynamic analysis [14, 73, 75] for vulnerability
detection. Unlike these techniques, AutoSOUP produces auditable
unit proofs that specify the scope, bounds, and assumptions under
which a component is memory safe. These proofs can be rechecked
to obtain bounded formal evidence of memory safety. Because
AutoSOUP operates statically on source code, it is also well suited
to embedded software, where dynamic analysis is often limited by
emulation, rehosting, and peripheral-modeling challenges [18, 32,
33, 52, 76].

7    Conclusion
AutoSOUP makes component-level bounded model checking more
practical by automatically constructing unit proofs that verify a
component’s memory safety, while documenting the bounds and
environment assumptions for the guarantees. It combines LLMs
with a deterministic, incremental workflow to balance utility with
reliability. Our evaluation on four substantial embedded RTOSes
suggest automated harness generation as an incremental path to-
ward security guarantees for real-world embedded software.
AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification                                                        XXX ’26, 2026, United States


References                                                                                      388–400. Association for Computing Machinery, 2015. URL: https://dl.acm.org/
 [1] LiteLLM - getting started | liteLLM. URL: https://docs.litellm.ai/docs/.                   doi/10.1145/2810103.2813643, doi:10.1145/2810103.2813643.
 [2] openai/openai-python. original-date: 2020-10-25T23:23:54Z. URL: https://github.       [23] Chia Yuan Cho, Vijay D’Silva, and Dawn Song. BLITZ: Compositional bounded
     com/openai/openai-python.                                                                  model checking for real-world programs. In 2013 28th IEEE/ACM International
 [3] Software defect reduction top 10 list. URL: https://www.computer.org/csdl/                 Conference on Automated Software Engineering (ASE), pages 136–146, 2013. URL:
     magazine/co/2001/01/r1135/13rRUwgyOg9.                                                     https://ieeexplore.ieee.org/abstract/document/6693074, doi:10.1109/ASE.2013.
 [4] SWE-bench leaderboards. URL: https://www.swebench.com/index.html.                          6693074.
 [5] IEC 61508-3: Functional safety of electrical/electronic/programmable electronic       [24] Nathan Chong, Byron Cook, Konstantinos Kallas, Kareem Khazem, Felipe R.
     safety-related systems – part 3: Software requirements, 2010. Second edition.              Monteiro, Daniel Schwartz-Narbonne, Serdar Tasiran, Michael Tautschnig, and
 [6] Channel File 291 Incident RCA is Available | CrowdStrike, 2025. URL: https:                Mark R. Tuttle. Code-level model checking in the software development work-
     //www.crowdstrike.com/en-us/blog/channel-file-291-rca-available/.                          flow. In Proceedings of the ACM/IEEE 42nd International Conference on Software
 [7] DARPA Guide for Formal Methods to Deliver Resilient Systems for Proposals,                 Engineering: Software Engineering in Practice, ICSE-SEIP ’20, pages 11–20. As-
     2025. URL: https://defencescienceinstitute.com/wp-content/uploads/2025/01/                 sociation for Computing Machinery, 2020. URL: https://dl.acm.org/doi/10.1145/
     Resilient_Systems_Best_Practices_Guide_-_1-9-2025.pdf.                                     3377813.3381347, doi:10.1145/3377813.3381347.
 [8] Project Zero: 0day "In the Wild", 2025. URL: https://googleprojectzero.blogspot.      [25] Edmund Clarke, Armin Biere, Richard Raimi, and Yunshan Zhu. Bounded model
     com/p/0day.html.                                                                           checking using satisfiability solving. Formal Methods in System Design, 19(1):7–34,
 [9] Ali Abbasi, Jos Wetzels, Thorsten Holz, and Sandro Etalle. Challenges in de-               2001. doi:10.1023/A:1011276507260.
     signing exploit mitigations for deeply embedded systems. In 2019 IEEE Euro-           [26] Jamieson M. Cobleigh, Dimitra Giannakopoulou, and Corina S. PĂsĂreanu. Learn-
     pean Symposium on Security and Privacy (EuroS&P), pages 31–46, 2025. URL:                  ing assumptions for compositional verification. In Hubert Garavel and John
     https://ieeexplore.ieee.org/abstract/document/8806725, doi:10.1109/EuroSP.                 Hatcliff, editors, Tools and Algorithms for the Construction and Analysis of Systems,
     2019.00013.                                                                                pages 331–346. Springer, 2003. doi:10.1007/3-540-36577-X_24.
[10] Alex Rebert, Ben Laurie, Murali Vijayaraghavan, and Alex Richardson. Securing         [27] CrowdStrike, Inc. External technical root cause analysis — channel file
     tomorrow’s software: the need for memory safety standards, 2025. URL: https://             291. Technical report, CrowdStrike, August 2024. Accessed January 2026.
     security.googleblog.com/2025/02/securing-tomorrows-software-need-for.html.                 URL: https://www.crowdstrike.com/wp-content/uploads/2024/08/Channel-File-
[11] Alex Rebert, Chandler Carruth, Jen Engel, and Andy Qin. Safer with Google:                 291-Incident-Root-Cause-Analysis-08.06.2024.pdf.
     Advancing Memory Safety, 2024. URL: https://security.googleblog.com/2024/10/          [28] Ermira Daka, José Campos, Gordon Fraser, Jonathan Dorn, and Westley Weimer.
     safer-with-google-advancing-memory.html.                                                   Modeling readability to improve unit tests. In Proceedings of the 2015 10th Joint
[12] Paschal C. Amusuo, Owen Cochell, Taylor Le Lievre, Parth V. Patil, Aravind                 Meeting on Foundations of Software Engineering, ESEC/FSE 2015, pages 107–118.
     Machiry, and James C. Davis. Do unit proofs work? an empirical study of composi-           Association for Computing Machinery. URL: https://dl.acm.org/doi/10.1145/
     tional bounded model checking for memory safety verification. In 2026 IEEE/ACM             2786805.2786838, doi:10.1145/2786805.2786838.
     48th International Conference on Software Engineering. URL: http://arxiv.org/abs/     [29] Ankush Das, Shuvendu K. Lahiri, Akash Lal, and Yi Li. Angelic verification:
     2503.13762, arXiv:2503.13762[cs], doi:10.48550/arXiv.2503.13762.                           Precise verification modulo unknowns. In Daniel Kroening and Corina S. Păsăre-
[13] Paschal C. Amusuo, Dongge Liu, Ricardo Andres Calvo Mendez, Jonathan Met-                  anu, editors, Computer Aided Verification, pages 324–342. Springer International
     zman, Oliver Chang, and James C. Davis. FalseCrashReducer: Mitigating false                Publishing, 2015. doi:10.1007/978-3-319-21690-4_19.
     positive crashes in OSS-fuzz-gen using agentic AI. URL: http://arxiv.org/abs/         [30] James C Davis, Sophie Chen, Huiyun Peng, Paschal C Amusuo, and Kelechi G
     2510.02185, arXiv:2510.02185[cs], doi:10.48550/arXiv.2510.02185.                           Kalu. A guide to stakeholder analysis for cybersecurity researchers. arXiv preprint
[14] Paschal C. Amusuo, Ricardo Andrés Calvo Méndez, Zhongwei Xu, Aravind                       arXiv:2508.14796, 2025.
     Machiry, and James C. Davis. Systematically detecting packet validation vul-          [31] Dino Distefano, Manuel Fähndrich, Francesco Logozzo, and Peter W. O’Hearn.
     nerabilities in embedded network stacks. In 2023 38th IEEE/ACM Interna-                    Scaling static analyses at facebook. Communications of the ACM, 62(8):62–70,
     tional Conference on Automated Software Engineering (ASE), pages 926–938, 2023.            2019. URL: https://dl.acm.org/doi/10.1145/3338112, doi:10.1145/3338112.
     ISSN: 2643-1572. URL: https://ieeexplore.ieee.org/abstract/document/10298483,         [32] Andrew Fasano, Tiemoko Ballo, Marius Muench, Tim Leek, Alexander Bulekov,
     doi:10.1109/ASE56229.2023.00095.                                                           Brendan Dolan-Gavitt, Manuel Egele, Aurélien Francillon, Long Lu, Nick Gregory,
[15] Paschal C. Amusuo, Parth V. Patil, Owen Cochell, Taylor Le Lievre, and James C.            Davide Balzarotti, and William Robertson. SoK: Enabling security analyses of
     Davis. A unit proofing framework for code-level verification: A research agenda.           embedded systems via rehosting. In Proceedings of the 2021 ACM Asia Conference
     In 2025 IEEE/ACM 47th International Conference on Software Engineering: New Ideas          on Computer and Communications Security, ASIA CCS ’21, pages 687–701. Asso-
     and Emerging Results (ICSE-NIER), pages 36–40. URL: https://ieeexplore.ieee.org/           ciation for Computing Machinery. URL: https://dl.acm.org/doi/10.1145/3433210.
     abstract/document/11023946, doi:10.1109/ICSE-NIER66352.2025.00013.                         3453093, doi:10.1145/3433210.3453093.
[16] Arthur Azevedo de Amorim, Cătălin Hriţcu, and Benjamin C. Pierce. The meaning         [33] Bo Feng, Alejandro Mera, and Long Lu. {P2IM}: Scalable and hardware-
     of memory safety. In Lujo Bauer and Ralf Küsters, editors, Principles of Security          independent firmware testing via automatic peripheral interface modeling. In
     and Trust, pages 79–105. Springer International Publishing. doi:10.1007/978-               29th USENIX Security Symposium (USENIX Security 20), pages 1237–1254, 2020.
     3-319-89722-6_4.                                                                           URL: https://www.usenix.org/conference/usenixsecurity20/presentation/feng.
[17] S. Bensalem, M. Bozga, T.-H. Nguyen, and J. Sifakis. Compositional verification       [34] Jean-Christophe Filliâtre. Deductive software verification. 13(5):397–403. doi:
     for component-based systems and application. IET Software, 4(3):181–193, 2010.             10.1007/s10009-011-0211-0.
     Publisher: IET Digital Library. URL: https://digital-library.theiet.org/content/      [35] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. Baldur: Whole-
     journals/10.1049/iet-sen.2009.0011, doi:10.1049/iet-sen.2009.0011.                         proof generation and repair with large language models. In Proceedings of
[18] Moritz Bley, Tobias Scharnowski, Simon Wörner, Moritz Schloegel, and Thorsten              the 31st ACM Joint European Software Engineering Conference and Symposium
     Holz. Protocol-aware firmware rehosting for effective fuzzing of embedded                  on the Foundations of Software Engineering, ESEC/FSE 2023, pages 1229–1241.
     network stacks. In Proceedings of the 2025 ACM SIGSAC Conference on Com-                   Association for Computing Machinery, 2023. URL: https://dl.acm.org/doi/10.
     puter and Communications Security, CCS ’25, pages 4484–4498. Association for               1145/3611643.3616243, doi:10.1145/3611643.3616243.
     Computing Machinery. URL: https://dl.acm.org/doi/10.1145/3719027.3765125,             [36] Pedro Fonseca, Kaiyuan Zhang, Xi Wang, and Arvind Krishnamurthy. An em-
     doi:10.1145/3719027.3765125.                                                               pirical study on the correctness of formally verified distributed systems. In
[19] Bob Lord. The Urgent Need for Memory Safety in Software Products | CISA,                   Proceedings of the Twelfth European Conference on Computer Systems, EuroSys
     September 2025. URL: https://www.cisa.gov/news-events/news/urgent-need-                    ’17, pages 328–343. Association for Computing Machinery, 2017. URL: https:
     memory-safety-software-products.                                                           //dl.acm.org/doi/10.1145/3064176.3064183, doi:10.1145/3064176.3064183.
[20] Cristiano Calcagno and Dino Distefano. Infer: An automatic program verifier           [37] Mikhail Y. R. Gadelha, Hussama I. Ismail, and Lucas C. Cordeiro. Handling
     for memory safety of c programs. In Mihaela Bobaru, Klaus Havelund, Gerard J.              loops in bounded model checking of c programs via k-induction. 19(1):97–114.
     Holzmann, and Rajeev Joshi, editors, NASA Formal Methods, pages 459–465.                   doi:10.1007/s10009-015-0407-9.
     Springer. doi:10.1007/978-3-642-20398-5_33.                                           [38] Michael Hicks. What is memory safety? - the PL enthusiast. URL: http://www.pl-
[21] Cristiano Calcagno, Dino Distefano, Peter O’Hearn, and Hongseok Yang. Compo-               enthusiast.net/2014/07/21/memory-safety/.
     sitional shape analysis by means of bi-abduction. In Proceedings of the 36th annual   [39] Li Huang, Sophie Ebersold, Alexander Kogtenkov, Bertrand Meyer, and Yinling
     ACM SIGPLAN-SIGACT symposium on Principles of programming languages, POPL                  Liu. Lessons from Formally Verified Deployed Software. CoRR, March 2023. URL:
     ’09, pages 289–300. Association for Computing Machinery, 2025. URL: https:                 http://arxiv.org/abs/2301.02206, doi:10.48550/arXiv.2301.02206.
     //dl.acm.org/doi/10.1145/1480881.1480917, doi:10.1145/1480881.1480917.                [40] Franjo Ivančić, Gogul Balakrishnan, Aarti Gupta, Sriram Sankaranarayanan,
[22] Qi Alfred Chen, Zhiyun Qian, Yunhan Jack Jia, Yuru Shao, and Zhuoqing Morley               Naoto Maeda, Hiroki Tokuoka, Takashi Imoto, and Yoshiaki Miyazaki. DC2:
     Mao. Static detection of packet injection vulnerabilities: A case for identifying          A framework for scalable, scope-bounded software verification. In 2011 26th
     attacker-controlled implicit information leaks. In Proceedings of the 22nd ACM             IEEE/ACM International Conference on Automated Software Engineering (ASE
     SIGSAC Conference on Computer and Communications Security, CCS ’15, pages                  2011), pages 133–142. ISSN: 1938-4300. URL: https://ieeexplore.ieee.org/abstract/
                                                                                                document/6100046, doi:10.1109/ASE.2011.6100046.
XXX ’26, 2026, United States                                                                                                                                        Amusuo et al.


[41] Franjo Ivančić, Zijiang Yang, Malay K. Ganai, Aarti Gupta, and Pranav Ashar.                 Proceedings of the 39th IEEE/ACM International Conference on Automated Software
     Efficient SAT-based bounded model checking for software verification. 404(3):256–            Engineering, ASE ’24, pages 1395–1407. Association for Computing Machinery.
     274. URL: https://www.sciencedirect.com/science/article/pii/S0304397508002223,               URL: https://dl.acm.org/doi/10.1145/3691620.3695512, doi:10.1145/3691620.
     doi:10.1016/j.tcs.2008.03.013.                                                               3695512.
[42] Yuchen Ji, Ting Dai, Zhichao Zhou, Yutian Tang, and Jingzhu He. Artemis:                [60] Mark Pitchford. The ‘shift left’ principle. New Electronics, 54(14):18–21, 2021.
     Toward accurate detection of server-side request forgeries through LLM-assisted              Publisher: Mark Allen Group. URL: https://www.magonlinelibrary.com/doi/full/
     inter-procedural path-sensitive taint analysis. 9:128:1349–128:1377. URL: https:             10.12968/S0047-9624%2822%2960234-7, doi:10.12968/S0047-9624(22)60234-
     //dl.acm.org/doi/10.1145/3720488, doi:10.1145/3720488.                                       7.
[43] kani. Getting started - the kani rust verifier, 2024. URL: https://model-checking.      [61] Sai Ritvik Tanksalkar, Siddharth Muralee, Srihari Danduri, Paschal Amusuo,
     github.io/kani/.                                                                             Antonio Bianchi, James C Davis, and Aravind Kumar Machiry. Lemix: Enabling
[44] Saketh Ram Kasibatla, Arpan Agarwal, Yuriy Brun, Sorin Lerner, Talia Ringer, and             testing of embedded applications as linux applications. In [USENIX Security’25]
     Emily First. Cobblestone: A divide-and-conquer approach for automating formal                USENIX Security Symposium, 2025, pages arXiv–2503, 2025.
     verification. URL: https://arxiv.org/abs/2410.19940v4, doi:10.1145/3744916.             [62] Brian Robinson, Michael D. Ernst, Jeff H. Perkins, Vinay Augustine, and Nuo Li.
     3773178.                                                                                     Scaling up automated test generation: Automatically generating maintainable
[45] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock,                  regression unit tests for programs. In 2011 26th IEEE/ACM International Conference
     Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt, Rafal Kolanski, Michael                    on Automated Software Engineering (ASE 2011), pages 23–32. ISSN: 1938-4300.
     Norrish, Thomas Sewell, Harvey Tuch, and Simon Winwood. seL4: formal                         URL: https://ieeexplore.ieee.org/abstract/document/6100059, doi:10.1109/ASE.
     verification of an OS kernel. In Proceedings of the ACM SIGOPS 22nd symposium on             2011.6100059.
     Operating systems principles, SOSP ’09, pages 207–220. Association for Computing        [63] László Szekeres, Mathias Payer, Tao Wei, and Dawn Song. SoK: Eternal war in
     Machinery, 2009. URL: https://dl.acm.org/doi/10.1145/1629575.1629596, doi:                   memory. In 2013 IEEE Symposium on Security and Privacy, pages 48–62, 2025.
     10.1145/1629575.1629596.                                                                     ISSN: 1081-6011. URL: https://ieeexplore.ieee.org/abstract/document/6547101,
[46] Daniel Kroening and Michael Tautschnig. CBMC – c bounded model checker.                      doi:10.1109/SP.2013.13.
     In Erika Ábrahám and Klaus Havelund, editors, Tools and Algorithms for the              [64] Gourav Takhar, Baldip Bijlani, Prantik Chatterjee, Akash Lal, and Subhajit
     Construction and Analysis of Systems, pages 389–391. Springer, 2014. doi:10.                 Roy. Memory-safety verification of open programs with angelic assump-
     1007/978-3-642-54862-8_26.                                                                   tions. 9:312:1119–312:1147. URL: https://dl.acm.org/doi/10.1145/3763090, doi:
[47] Latham & Watkins LLP. New EU product liability directive comes into                          10.1145/3763090.
     force. Client alert / legal briefing, December 2024. Accessed January                   [65] Norbert Tihanyi, Yiannis Charalambous, Ridhi Jain, Mohamed Amine Ferrag,
     2026.     URL: https://www.lw.com/admin/upload/SiteAttachments/New-EU-                       and Lucas C. Cordeiro. A new era in software security: Towards self-healing
     Product-Liability-Directive-Comes-Into-Force.pdf.                                            software via large language models and formal verification. In 2025 IEEE/ACM
[48] Thanh Le-Cong, Bach Le, and Toby Murray. Can LLMs reason about program se-                   International Conference on Automation of Software Test (AST), pages 136–147.
     mantics? a comprehensive evaluation of LLMs on formal specification inference.               IEEE Press. URL: https://dl.acm.org/doi/10.1109/AST66626.2025.00020, doi:10.
     In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher                        1109/AST66626.2025.00020.
     Pilehvar, editors, Proceedings of the 63rd Annual Meeting of the Association for Com-   [66] John Toman and Dan Grossman. Taming the static analysis beast. In Ben-
     putational Linguistics (Volume 1: Long Papers), pages 21991–22014. Association for           jamin S. Lerner, Rastislav Bodík, and Shriram Krishnamurthi, editors, 2nd Sum-
     Computational Linguistics. URL: https://aclanthology.org/2025.acl-long.1068/,                mit on Advances in Programming Languages (SNAPL 2017), volume 71 of Leib-
     doi:10.18653/v1/2025.acl-long.1068.                                                          niz International Proceedings in Informatics (LIPIcs), pages 18:1–18:14. Schloss
[49] Hugo Lefeuvre, Vlad-Andrei Bădoiu, Yi Chen, Felipe Huici, Nathan Dautenhahn,                 Dagstuhl – Leibniz-Zentrum für Informatik. URL: https://drops.dagstuhl.de/
     and Pierre Olivier. Assessing the impact of interface vulnerabilities in compart-            entities/document/10.4230/LIPIcs.SNAPL.2017.18, doi:10.4230/LIPIcs.SNAPL.
     mentalized software. In Proceedings 2023 Network and Distributed System Security             2017.18.
     Symposium. Internet Society. doi:10.14722/ndss.2023.24117.                              [67] Paul C. van Oorschot. Memory errors and memory safety: C as a case study.
[50] Shaofeng Li, Lei Qiao, and Mengfei Yang. Memory state verification based on                  21(2):70–76. URL: https://ieeexplore.ieee.org/abstract/document/10102611, doi:
     inductive and deductive reasoning. 70(3):1026–1039. URL: https://ieeexplore.ieee.            10.1109/MSEC.2023.3236542.
     org/abstract/document/9435092, doi:10.1109/TR.2021.3074709.                             [68] Minghua Wang, Jingling Xue, Lin Huang, Yuan Zi, and Tao Wei. UnsafeCop:
[51] Ziyang Li, Saikat Dutta, and Mayur Naik. IRIS: LLM-assisted static analysis                  Towards memory safety for real-world unsafe rust code with practical bounded
     for detecting security vulnerabilities. In Y. Yue, A. Garg, N. Peng, F. Sha, and             model checking. In Andre Platzer, Kristin Yvonne Rozier, Matteo Pradella, and
     R. Yu, editors, International Conference on Learning Representations, volume 2025,           Matteo Rossi, editors, Formal Methods, pages 307–324. Springer Nature Switzer-
     pages 35735–35758. URL: https://proceedings.iclr.cc/paper_files/paper/2025/file/             land, 2025. doi:10.1007/978-3-031-71177-0_19.
     582d4e27fa24168f3af1f4582655034b-Paper-Conference.pdf.                                  [69] Lian Kit Wee. Here comes the wave of insurance claims for the CrowdStrike
[52] Dominik Maier, Lukas Seidel, and Shinjo Park. BaseSAFE: baseband sanitized                   outage, 2025. URL: https://www.businessinsider.com/businesses-claiming-losses-
     fuzzing through emulation. In Proceedings of the 13th ACM Conference on Security             crowdstrike-outage-insurance-billions-losses-cyber-policies-2024-7.
     and Privacy in Wireless and Mobile Networks, WiSec ’20, pages 122–132. Associ-          [70] Tong Wu, Shale Xiong, Edoardo Manino, Gareth Stockwell, and Lucas C. Cordeiro.
     ation for Computing Machinery. URL: https://dl.acm.org/doi/10.1145/3395351.                  Verifying components of arm(r) confidential computing architecture with ESBMC,
     3399360, doi:10.1145/3395351.3399360.                                                        2024. URL: https://arxiv.org/abs/2406.04375v1.
[53] Martin Brain. CBMC: goto-cc, 2024. URL: https://diffblue.github.io/cbmc/group_          [71] Hanxiang Xu, Wei Ma, Ting Zhou, Yanjie Zhao, Kai Chen, Qiang Hu, Yang
     _goto-cc.html.                                                                               Liu, and Haoyu Wang. CKGFuzzer: LLM-based fuzz driver generation en-
[54] Atif Mashkoor, Michael Leuschel, and Alexander Egyed. Validation obli-                       hanced by code knowledge graph. In 2025 IEEE/ACM 47th International Confer-
     gations: A novel approach to check compliance between requirements and                       ence on Software Engineering: Companion Proceedings (ICSE-Companion), pages
     their formal specification. In 2021 IEEE/ACM 43rd International Conference on                243–254. URL: https://ieeexplore.ieee.org/abstract/document/11024256, doi:
     Software Engineering: New Ideas and Emerging Results (ICSE-NIER), pages 1–                   10.1109/ICSE-Companion66252.2025.00079.
     5. URL: https://ieeexplore.ieee.org/abstract/document/9402243, doi:10.1109/             [72] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui,
     ICSE-NIER52604.2021.00009.                                                                   Yeyun Gong, Chris Hawblitzel, Shuvendu Lahiri, Jacob R. Lorch, Shuai Lu, Fan
[55] Barton P. Miller, Lars Fredriksen, and Bryan So. An empirical study of the                   Yang, Ziqiao Zhou, and Shan Lu. AutoVerus: Automated proof generation for
     reliability of UNIX utilities. 33(12):32–44. URL: https://dl.acm.org/doi/10.1145/            rust code, 2024. URL: https://arxiv.org/abs/2409.13082v1.
     96267.96279, doi:10.1145/96267.96279.                                                   [73] Joobeom Yun, Fayozbek Rustamov, Juhwan Kim, and Youngjoo Shin. Fuzzing of
[56] MSRC Team. A proactive approach to more secure code | MSRC Blog | Microsoft                  embedded systems: A survey. ACM Computing Surveys, 55(7):1–33, 2025. URL:
     Security Response Center, 2019. URL: https://msrc.microsoft.com/blog/2019/07/a-              https://dl.acm.org/doi/10.1145/3538644, doi:10.1145/3538644.
     proactive-approach-to-more-secure-code/.                                                [74] Cen Zhang, Yaowen Zheng, Mingqiang Bai, Yeting Li, Wei Ma, Xiaofei Xie,
[57] Marius Muench, Jan Stijohann, Frank Kargl, Aurelien Francillon, and Davide                   Yuekang Li, Limin Sun, and Yang Liu. How effective are they? exploring large
     Balzarotti. What you corrupt is not what you crash: Challenges in fuzzing em-                language model based fuzz driver generation. In Proceedings of the 33rd ACM
     bedded devices. In Network and Distributed System Security Symposium. Internet               SIGSOFT International Symposium on Software Testing and Analysis, ISSTA 2024,
     Society, 2025. URL: https://www.ndss-symposium.org/wp-content/uploads/2018/                  pages 1223–1235. Association for Computing Machinery, 2024. URL: https:
     02/ndss2018_01A-4_Muench_paper.pdf, doi:10.14722/ndss.2018.23166.                            //dl.acm.org/doi/10.1145/3650212.3680355, doi:10.1145/3650212.3680355.
[58] Santosh Nagarakatte. Full spatial and temporal memory safety for c. 22(4):30–           [75] Chi Zhang, Yu Wang, and Linzhang Wang. Firmware fuzzing: The state of the art.
     39. URL: https://ieeexplore.ieee.org/abstract/document/10439147, doi:10.1109/                In 12th Asia-Pacific Symposium on Internetware, Internetware’20, pages 110–115.
     MSEC.2024.3363142.                                                                           Association for Computing Machinery, 2020. doi:10.1145/3457913.3457934.
[59] Muhammad A. A. Pirzada, Giles Reger, Ahmed Bhayat, and Lucas C. Cordeiro.               [76] Yaowen Zheng, Yuekang Li, Cen Zhang, Hongsong Zhu, Yang Liu, and Limin Sun.
     LLM-generated invariants for bounded model checking without loop unrolling. In               Efficient greybox fuzzing of applications in linux-based IoT devices via enhanced
AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification   XXX ’26, 2026, United States


     user-mode emulation. In Proceedings of the 31st ACM SIGSOFT International Sym-
     posium on Software Testing and Analysis, ISSTA 2022, pages 417–428. Association
     for Computing Machinery. URL: https://dl.acm.org/doi/10.1145/3533767.3534414,
     doi:10.1145/3533767.3534414.
XXX ’26, 2026, United States                                                                                                        Amusuo et al.


Outline of Appendices                                                           methods. Our work is intended to shift their cost/benefit
The appendix contains the following material:                                   calculus.
     • §A Ethics analysis
     • §B Open science information                                        Potential Harms and Mitigating Factors
     • §C Extended version of AutoSOUP algorithms                             • Exploitation risk. AutoSOUP could be used by adversaries
     • §D Unit Proof Case Studies                                               to more efficiently identify exploitable vulnerabilities, includ-
     • §E Instrumented memory safety properties                                 ing zero-day vulnerabilities, before patches are developed or
     • §F: Sample vulnerability disclosed as a result of this work.             deployed.
     • §G: Additional experimental results.                                   • False positives. When used by engineers, false positives in
                                                                                AutoSOUP may waste their time. Our evaluation character-
A     Ethical Considerations                                                    ized the false positives resulting from AutoSOUP to let them
This section describes the ethical considerations of our work. Au-              make an informed adoption decision.
toSOUP’s primary ethical consideration is that it can be used to              • Operational and economic impact. Findings may require
identify defects in a software system, resulting in a standard “dual            costly remediation, downtime, or architectural changes for
use” scenario posing both harms and benefits. We followed the                   system operators and organizations.
guidance of Davis et al. in conducting our stakeholder-based ethics           • False confidence or misuse. Over-reliance on AutoSOUP ’s
analysis [30].                                                                  outputs may lead developers to overlook other vulnerability
                                                                                classes or to misinterpret partial guarantees as comprehen-
Stakeholders                                                                    sive security. To reduce the risk of overgeneralization by
                                                                                engineers, our work characterizes the class of vulnerabilities
Direct stakeholders:                                                            exposed by AutoSOUP, and the extent of false negatives.
     • Software maintainers and developers. Engineers who use                 • Risk to researchers. The research team may face legal or
       AutoSOUP to analyze their own codebases for vulnerabilities              reputational consequences if AutoSOUP is misused, miscon-
       and correctness issues. They directly interact with the tool             figured, or perceived as facilitating harm.
       and may act on its findings.
     • System operators and organizations. Teams responsi-
       ble for deploying and operating software systems evaluated         Potential Benefits
       using AutoSOUP, including embedded, infrastructure, or                 • Improved software security. AutoSOUP enables engineers
       safety-critical systems.                                                 to detect and remediate vulnerabilities earlier and more sys-
     • The research and development team. Authors and main-                     tematically, reducing the likelihood of exploitation.
       tainers of AutoSOUP, who may face legal, professional, or              • Support for higher-assurance engineering. By produc-
       reputational risks related to vulnerability discovery, disclo-           ing structured analysis artifacts (e.g., unit-level evidence or
       sure practices, or downstream misuse.                                    proofs), AutoSOUP can assist organizations in meeting regu-
     • Adversaries. Malicious actors who could use AutoSOUP, or                 latory, safety, or compliance requirements.
       techniques disclosed in the paper, to systematically discover          • Knowledge transfer and standardization. The tool and
       vulnerabilities in target software.                                      associated research disseminate best practices for systematic
                                                                                vulnerability analysis and verification. They may change the
Indirect stakeholders:                                                          standard cost/benefit analysis for the use of bounded model
     • End users of affected software. Individuals or organiza-                 checking.
       tions who rely on software analyzed using AutoSOUP and                 • Research advancement. AutoSOUP contributes to the sci-
       may be impacted by vulnerabilities or by mitigations applied             entific understanding of systematic vulnerability detection
       as a result of AutoSOUP ’s use.                                          and verification, enabling further defensive research.
     • Downstream software ecosystem. Maintainers and users
       of libraries, dependencies, or products that incorporate code
       analyzed or modified using AutoSOUP.                               Judgment
     • Vulnerable populations. Groups disproportionately harmed           In our judgment, the potential benefit to software cybersecurity
       by software exploitation, such as users of safety-critical, med-   outweighs the risks posed by our work. We understood the ethical
       ical, industrial, or civic infrastructure.                         framing of our work at the outset of our study. We did not ob-
     • Broader public. Society at large, insofar as widespread ex-        serve any new concerns during the research conduct. We therefore
       ploitation or mitigation of vulnerabilities affects trust in       proceeded with submission to USENIX.
       software systems and digital infrastructure.
     • Research and security community. Other researchers
       and practitioners who may reuse, extend, or operationalize         B    Open Science
       AutoSOUP ’s techniques.                                            An anonymized artifact for our submission is available at:
     • Policymakers and standards bodies. Government and                    https://anonymous.4open.science/r/AutoSOUP.
       industry policymakers have asked for greater use of formal           This artifact consists of:
AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification                                       XXX ’26, 2026, United States


    (1) The implementation of AutoSOUP, consisting of both the                         Algorithm 3: Resource-aware scope widening. The algo-
        conventional software and the prompts for the LLM compo-                       rithm incrementally expands the verification scope at the
        nents. We used an agentic framework that facilitates the use                   file level and returns the largest scope whose provisional
        of open-source LLMs rather than commercial ones.                               verification instance remains within the resource budget.
    (2) The organized benchmark of real-world CVE patches in open-                      Input: Software system 𝑆, component entry point 𝐶𝑒 , maximum
        source embedded operating systems, derived from the work                               scope level 𝑑 max , resource budget 𝑅
        of Amusuo et al. [12].                                                          Output: Verification scope 𝑆𝑐 , loop bounds 𝐵, env. model 𝐸
    (3) The evaluation automation that permit the replication of our                  1 Function ResourceAwareScopeWidening(𝑆, 𝐶𝑒 , 𝑑 max , 𝑅)

        results.                                                                      2    𝑆𝑐 ← AllFunctionsIn(FileOf(𝐶𝑒 ) )
    (4) The data associated with the evaluation automation that is                    3    𝐵 ← InitBounds(𝑆𝑐 , 1)
        used to create the tables and figures in this manuscript.                     4    𝐸 ← InputModel(𝐶𝑒 ) ∪ ModelExternalCallees(𝑆𝑐 )
    (5) Links to the CVEs and defect repairs resulting from this                      5    if ¬WithinBudget(𝑆𝑐 , 𝐵, 𝐸, 𝑅) then
        research, as they emerge.                                                     6         return ( ∅, ∅, ∅ )
   In short, we provide everything we used to create our work and                      7     for 𝑑 ← 1 to 𝑑 max do
collect data. We acknowledge that our use of OpenAI’s frontier                         8         𝑆𝑐′ ← WidenByOneFileLevel(𝑆𝑐 )
models complicates the replicability of this work. We spent several                    9         𝐵 ′ ← InitBounds(𝑆𝑐′ , 1)
thousand dollars to perform our experiments, and an independent                       10         𝐸 ′ ← InputModel(𝐶𝑒 ) ∪ ModelExternalCallees(𝑆𝑐′ )
replication would require a similar outlay of funds — and the results                 11         if ¬WithinBudget(𝑆𝑐′ , 𝐵 ′ , 𝐸 ′ , 𝑅) then
                                                                                      12              return (𝑆𝑐 , 𝐵, 𝐸 )
will change because of the evolving nature of frontier models.
   For more information, we refer the reviewers to the README                         13         (𝑆𝑐 , 𝐵, 𝐸 ) ← (𝑆𝑐′ , 𝐵 ′ , 𝐸 ′ )
of that artifact.                                                                     14     return (𝑆𝑐 , 𝐵, 𝐸 )

                                                                                     15  Function WidenByOneFileLevel(𝑆𝑐 )
C     Detailed AutoSOUP Algorithms                                                    16    𝐹 ← FilesOf(𝑆𝑐 )
Here we provide detailed versions of the core AutoSOUP algorithms.                    17    𝐹 adj ← FilesContainingCalleesFrom(𝑆𝑐 )
                                                                                      18    return AllFunctionsIn(𝐹 ∪ 𝐹 adj )
C.1     Resource-Aware Scope Widening
Resource-aware scope widening derives the verification scope 𝑆𝑐
by incrementally adding code that may contain checkable memory-
safety properties and are semantically related while keeping ver-                     Step 2: Model external calls: We next identify call edges that cross
ification within the resource budget 𝑅. Its goal is to increase the                  the current scope boundary and replace their targets with sim-
component behavior checked against 𝑄 without making verifica-                        ple type-based models. From the compiled unit, we recover the
tion intractable or the resulting unit proof difficult to audit.                     call graph and identify edges to undefined callees and their return
    Following prior work [64], we use source files as the unit of                    types. We use an LLM agent to synthesize models for these un-
scope expansion. This choice reflects the convention that related                    defined callees following strict guidelines, integrate them to the
functions are often colocated in the same file. File-level widening                  unit proof and ensure the resulting unit proof remains structurally
therefore preserves useful semantic context while keeping each                       valid. Primitive returns are also modeled as unconstrained symbolic
expansion step coarse enough to manage.                                              values, while pointer returns are modeled as valid allocated objects
    The technique proceeds in three steps (Algorithm 3).                             containing unconstrained values.
 Step 1: Initialize the scope, bounds, and input model: We first add the                 These unconstrained models preserve all possible states that
file containing the component entry point 𝐶𝑒 to 𝑆𝑐 , initialize all                  may be returned by the excluded functions, including values that
loop bounds in the current scope to 1, and construct an input model                  may violate 𝑄. Validly-allocated pointer returns avoid irrelevant
for 𝐶𝑒 . The input model follows the entry-point type signature.                     invalid-pointer states that cause state-space explosion and increase
Primitive arguments receive unconstrained symbolic values over                       verification cost. As in Step 1, an LLM agent generates and integrates
their full type range, while pointer arguments are initialized to valid              the models, while deterministic checks ensure that the unit proof
allocated objects containing unconstrained values. The resulting                     remains semantically valid.
unit proof 𝑈 (𝑉 ) contains this input model and a call to 𝐶𝑒 .                        Step 3: Widen the scope: After constructing the provisional instance
    We use an LLM agent to synthesize this input model and re-                       𝑉 = (𝑆𝑐 , 𝐵, 𝐸), we check it against the configured resource budgets.
cover the configurations to compile the entry point’s parent file.                   If verification remains within 𝑅, we widen 𝑆𝑐 by adding all reachable
Although the input model follows a fixed template, compiling it                      functions from files that contain definitions of previously excluded
with the target file requires project-specific headers, include paths,               and modeled callees. We use a pre-indexed database of 𝑆 to locate
macros and mandatory program configurations. These require-                          candidate files. When multiple files define functions with the same
ments are difficult to recover reliably with fixed rules across diverse              name and signature, we select the file closest to the in-scope caller
C projects [66]. Following the LLM-as-Function-Call architecture,                    by longest common path prefix. The LLM agent is finally used to
we mechanically validate the result: the proof must compile, call 𝐶𝑒 ,               recover the compilation configuration for newly added files.
and introduce no preconditions beyond the intended type-based                            We repeat external-call modeling and scope widening until ver-
initialization.                                                                      ification exceeds 𝑅 or no additional files can be added. We use
XXX ’26, 2026, United States                                                                                                   Amusuo et al.


three budgets: verification time, memory resources, and file depth.      Step 1: Infer underapproximate weakest preconditions: Following prior
The file depth budget bounds the number of files whose functions        counter-example-guided environment refinement approaches, we
can be added to the verification scope so as to keep the unit proof     infer preconditions from counterexamples that suppress violations
generation cost reasonable.                                             of memory-safety properties. These preconditions need not be logi-
                                                                        cally weakest, since weakest-precondition inference is often com-
C.2      Property-Guided Loop Bound and Model                           putationally expensive [23]. Instead, they must be weak enough to
         Refinement                                                     preserve the target property while avoiding unnecessary restric-
                                                                        tions on safe states. For example, in Listing 1, the property on
A detailed description is in the main body of the manuscript. We
                                                                        line 16 requires the loop index to remain within the size of dst.
do not expand on it here.
                                                                        The inferred precondition 𝑟𝑒𝑡 ≤ 10 constrains the value returned
                                                                        by get_record_count_m2() and therefore the number of loop it-
C.3      Context-Aware Environmental Model                              erations. Further weakening this precondition by allowing larger
         Refinement                                                     values of 𝑟𝑒𝑡 violates the property.
Property-guided refinement in §4.3 maximizes exposure of vio-              We first parse the verification report to extract each violated
lations of 𝑄 using unconstrained models 𝐸. However, violations          property 𝑞 ∈ 𝑄, its location loc(𝑞), and its counterexample wit-
found under unconstrained models may be infeasible in the broader       nesses 𝑤 (𝑞). For each tuple (𝑞, loc(𝑞), 𝑤 (𝑞)), we prompt an LLM
system 𝑆. For example, the assertion on Program Line 15 in Listing 1    agent to infer a precondition that, when added to 𝐸, keeps loc(𝑞)
will be violated by an input model that provides a null pointer, even   covered but suppresses the violation of 𝑞. The prompt guides the
though the actual caller only provides statically-defined arrays.       agent to identify the violated condition, propagate it backward
Context-aware environment refinement separates these infeasi-           through dataflow and path constraints, and stop at the external
ble property violations caused by overly permissive environment         model or input responsible for the value.
assumptions from genuine memory-safety errors.                             In Listing 1, the agent first identifies the violated condition 𝑖 <
   This technique operates in two steps, illustrated in Algorithm 2.    𝑂𝑏 𝑗𝑒𝑐𝑡𝑆𝑖𝑧𝑒 (𝑑𝑠𝑡), which simplifies to 𝑖 < 10. It then propagates this
                                                                        condition through the loop condition on program line 13 to derive
                                                                        𝑛 ≤ 10. Finally, it propagates the constraint to the get_record_count_m2()
 Algorithm 4: Context-aware environment model refine-                   model and derives 𝑟𝑒𝑡 ≤ 10. The agent can inspect witnesses, navi-
 ment. The algorithm infers underapproximate precondi-                  gate code, and test candidate preconditions. We accept a candidate
 tions for violated memory-safety properties, validates them            only if it suppresses the target violation without reducing struc-
 against calling contexts of the component entry point, and             tural validity, conclusiveness, coverage, or the number of checked
 reports caller-feasible violations as memory-safety errors.            properties.
   Input: Software system 𝑆, component entry point 𝐶𝑒 , Environment      Step 2: Validate and refine against calling contexts: The resulting pre-
          model 𝐸, Property violations 𝑄 𝑣                              condition may overgeneralize and exclude valid caller states that
   Output: Refined environment model 𝐸, memory-safety error set M
                                                                        would not violate 𝑞. As a result, we validate each accepted precon-
 1 Function ContextAwareEnvRefinement(𝑆, 𝐶𝑒 , 𝐸, 𝑄 𝑣 )
 2    M←∅
                                                                        dition against the calling contexts of 𝐶𝑒 in 𝑆. Using a pre-indexed
 3    W ← ParseViolationReport(𝑄 𝑣 )
                                                                        call graph, we identify callsites of 𝐶𝑒 or the actual implementations
      // W contains tuples (𝑞, 𝑤 (𝑞) )
                                                                        of modeled functions. For each callsite or implementation, we use
 4    foreach (𝑞, 𝑤 (𝑞) ) ∈ W do
                                                                        an LLM agent to identify the constraints along execution paths that
 5         𝜙 ← InferApproxPrecondition(𝐸, 𝑞, 𝑤 (𝑞) )                    reach the callsite and check whether those constraints can violate
 6         (𝜙 ′ , B ) ← ValidatePrecondition(𝑆, 𝐶𝑒 , 𝑞, 𝜙 )             the inferred precondition.
 7         𝐸 ← 𝐸 ∪ {𝜙 ′ }                                                  This validation produces three outcomes. If a calling path vio-
 8         M←M∪B                                                        lates the precondition but still satisfies 𝑞, the agent weakens and
                                                                        revalidates the precondition. If a calling path violates the precondi-
 9      return (𝐸, M )
                                                                        tion and triggers 𝑞, we report the path as a feasible memory-safety
10 Function ValidatePrecondition(𝑆, 𝐶𝑒 , 𝑞, 𝜙 )                         error in 𝑆. If the precondition holds, we report the property as veri-
11    B ← ∅; 𝜙 ′ ← 𝜙                                                    fied. All preconditions are added to the unit proof’s environment
12    C ← CallsitesOf(𝐶𝑒 , 𝑆 )                                          model 𝐸. They become explicit, auditable assumptions under which
13    foreach 𝑐 ∈ C do                                                  the verified component is memory safe.
14        𝜓𝑐 ← PathConstraints(𝑐, 𝑆 )
15        if 𝜓𝑐 ̸ |= 𝜙 ′ then                                           D     Unit Proof Case Studies
16            𝜙ˆ ← WeakenPrecondition(𝜙 ′ ,𝜓𝑐 )
                                    ˆ 𝑞) then
              if SatisfiesProperty(𝜙,
17                                                                      D.1    Case study 1: prvCheckOptions.
18                   𝜙 ′ ← 𝜙ˆ
                                                                        prvCheckOptions processes TCP packet options using a socket
19               else
20                      B ← B ∪ { (𝑞,𝜓𝑐 , 𝜙 ′ ) }
                                                                        pointer and a network-buffer pointer. Listing 2 shows a unit proof,
                                                                        comprising its input and function model, created by AutoSOUP.
21      return (𝜙 ′ , B )                                                Scope.: At scope level 1, AutoSOUP verified the entry point and
                                                                        two reachable same-file callees, covering 107 lines of code. The
AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification                                    XXX ’26, 2026, United States



  1   size_t uxIPHeaderSizePacket( const NetworkBufferDescriptor_t
                                                                                     the callees, creating separate unit proofs to verify them. Thus, Au-
      ↩→ * nbuf )                                                                    toSOUP maximized the number of properties verified with one unit
  2   {                                                                              proof, while FreeRTOS abstracted part of that behavior.
  3       const EthernetHeader_t * pxEth = ( const EthernetHeader_t
          ↩→ * ) nbuf->pucEthernetBuffer;                                             Loop bounds.: prvCheckOptions contains one loop that iterates
  4       if( pxEth->usFrameType == ( uint16_t ) ipIPv6_FRAME_TYPE )                 over TCP packet options. AutoSOUP kept this loop at its initial
  5       {
  6           return ipSIZE_OF_IPv6_HEADER;                                          bound of 2 because all memory-safety properties were covered and
  7       }                                                                          no in-scope memory access depended on further unwinding. FreeR-
  8       return ipSIZE_OF_IPv4_HEADER;
  9   }
                                                                                     TOS used a bound of 41. It is not clear why they used such large loop
 10                                                                                  bound even though the helper logic was already abstracted and no
 11   void harness()                                                                 memory-safety access occur in or after that loop. This shows how
 12   {
 13       size_t sock_len;                                                           property-guided refinement can avoid unnecessary unwinding.
 14       __CPROVER_assume(sock_len >= sizeof(FreeRTOS_Socket_t));
 15       FreeRTOS_Socket_t *sock = malloc(sock_len);
                                                                                      Models.: Both proofs used similar input models: valid struct point-
 16       __CPROVER_assume(sock != NULL);                                            ers for input arguments (Lines 13–28) and preconditions that specify
 17                                                                                  a lower bound on the size of received TCP packet (Lines 33–41).
 18        size_t nbuf_len;
 19        __CPROVER_assume(nbuf_len >=                                              AutoSOUP also inferred the same packet-length precondition used
           ↩→ sizeof(NetworkBufferDescriptor_t));                                    by FreeRTOS, namely that the packet must contain the Ethernet, IP,
 20        NetworkBufferDescriptor_t *nbuf = malloc(nbuf_len);                       and TCP headers. For environment modeling, both proofs modeled
 21        __CPROVER_assume(nbuf != NULL);
 22                                                                                  uxIPHeaderSizePacket by returning the IP header size implied by
 23        size_t ethbuf_len;                                                        the packet’s IP version. The main difference is that FreeRTOS also
 24        __CPROVER_assume(ethbuf_len >= ipSIZE_OF_ETH_HEADER);
 25        nbuf->pucEthernetBuffer = malloc(ethbuf_len);                             modeled the same-file helper prvSingleStepTCPHeaderOptions,
 26        __CPROVER_assume(nbuf->pucEthernetBuffer != NULL);                        while AutoSOUP included that helper directly in scope.
 27
 28        __CPROVER_assume(nbuf->xDataLength <= ethbuf_len);
                                                                                        Overall, this case shows that AutoSOUP can replicate expert-like
 29                                                                                  input and environment assumptions while checking more same-file
 30        const EthernetHeader_t *eth =                                             behavior with a smaller loop bound.
 31            (const EthernetHeader_t *) nbuf->pucEthernetBuffer;
 32
 33        __CPROVER_assume(
 34           ((eth->usFrameType == (uint16_t) ipIPv6_FRAME_TYPE) &&                 D.2         Case Study 2: vDHCPProcess
 35             (nbuf->xDataLength >=
 36                (ipSIZE_OF_ETH_HEADER + ipSIZE_OF_IPv6_HEADER +                   vDHCPProcess function processes received DHCP packets and man-
 37                 ipSIZE_OF_TCP_HEADER)))                                          ages the DHCP state machine.
 38           ((eth->usFrameType != (uint16_t) ipIPv6_FRAME_TYPE) &&
 39             (nbuf->xDataLength >=                                                 Scope.: AutoSOUP includes vDHCPProcess and all reachable func-
 40                (ipSIZE_OF_ETH_HEADER + ipSIZE_OF_IPv4_HEADER +                   tions in its parent file, covering 17 functions and 507 lines of code.
 41                 ipSIZE_OF_TCP_HEADER))));
 42                                                                                  The FreeRTOS proof includes only the 41-line entry function and
 43        __CPROVER_assume(                                                         excludes the reachable helper functions. This difference reflects
 44         ipconfigIS_VALID_PROG_ADDRESS(sock->u.xTCP.pxHandleSent)
                                                                                     the goal of AutoSOUP: rather than minimizing the proof to the
               ↩→ == pdFALSE);
 45                                                                                  entry point, it expands the scope to include code that may contain
 46        prvCheckOptions(sock, nbuf);                                              checkable memory-safety properties or may affect the entry point’s
 47   }
                                                                                     memory-safety behavior.
                                                                                      Loop bounds.: AutoSOUP reaches eight loops but does not increase
Listing 2: AutoSOUP-generated unit proof for                                         all bounds uniformly. It keeps six loops at the default bound of 2,
prvCheckOptions. The harness specifies the input model. It                           bounds memcmp’s internal loop at 7 because it compares six-byte
initializes the input socket and network buffer arguments. It                        MAC addresses, and increases the bound for vProcessHandleOption.1
also identifies conditions for memory safety: the ethernet                           only after coverage feedback shows that the loop exit is needed to
frame ethbuf_len is greater than the size of ethernet header                         reach additional code. Listing 3 shows this localized refinement. In
(Line 24), the specified length value (Line 28) and the                              contrast, the FreeRTOS proof reaches only two loops and assigns
combined size of the ethernet, IP and TCP headers (Line 33                           both a uniform bound of 4. This demonstrates the property-guided
– 41). The uxIPHeaderSizePacket function model specifies                             approach AutoSOUP follows to derive appropriate loop bounds.
the memory-safety-relevant behavior of the function: that it                          Models.: AutoSOUP initializes the primitive argument as an uncon-
returns the size of IP header corresponding to the IP version                        strained symbolic value and models the endpoint pointer as a valid
in the ethernet frame. These environment models were                                 allocated endpoint list. It also infers, from verification feedback, that
inferred through the context-aware environment refinement                            the global pxNetworkEndPoints must reference the input endpoint.
technique.                                                                           It also correctly infers, from a failed assertion in the program, that
                                                                                     its xSocketValid model should return True after socket creation.
                                                                                         The FreeRTOS proof uses a similar endpoint model by passing the
                                                                                     initialized global endpoint object directly to vDHCPProcess, but it
                                                                                     additionally calls prvCreateDHCPSocket and prvCloseDHCPSocket
FreeRTOS proof verified only the 33-line entry point and excluded                    around the target call, possibly to ensure a valid socket is available.
XXX ’26, 2026, United States                                                                                                     Amusuo et al.


  1   {                                                                            • pointer relation: dead object in 𝑝: ¬dead(𝑝)
  2     "analysis": "The uncovered block starts at line 1095,
        ↩→ immediately after the `while` loop at line 1088:
                                                                                   • pointer relation: pointer outside object bounds in 𝑝 + 𝑘:
  3   `while(uxTargetIndex < ipconfigENDPOINT_DNS_ADDRESS_COUNT)`.                   offset(𝑝) + 𝑘 ≤ object_size(𝑝)
  4
  5    Root cause: `ipconfigENDPOINT_DNS_ADDRESS_COUNT` is 5 in this
                                                                                   • pointer relation: invalid integer address in 𝑝+𝑘: object(𝑝) ≠
       ↩→ proof configuration                                                        object(NULL) ∨ 𝑝 + 𝑘 = NULL
       ↩→ (`test/unit-test/ConfigFiles/FreeRTOSIPConfig.h`), so the            (4) Pointer primitives
       ↩→ loop may require up to 5 iterations before exit...",
  6
                                                                                   • pointer invalid in 𝑃 (𝑝, 𝑛): 𝑝 = NULL ∨ valid(𝑝)
  7    "proposed_modifications": "Minimal change in Makefile only: add             • deallocated dynamic object in 𝑃 (𝑝, 𝑛): 𝑝 = NULL∨¬deallocated(𝑝)
       ↩→ a loop-specific unwind bound for `vProcessHandleOption.1`.               • dead object in 𝑃 (𝑝, 𝑛): 𝑝 = NULL ∨ ¬dead(𝑝)
  8
  9 Set:                                                                           • pointer outside object bounds in 𝑃 (𝑝, 𝑛): 𝑝 = NULL ∨
 10 `--unwindset vProcessHandleOption.1:6`                                           offset(𝑝) + 𝑛 ≤ object_size(𝑝)
 11 (5 needed iterations + 1 to allow falsifying the loop condition
                                                                               (5) Array bounds
     ↩→ and exiting).",
 12                                                                                • array lower bound in 𝑎[𝑖]: 𝑖 ≥ 0
 13    "updated_harness": ...                                                      • array upper bound in 𝑎[𝑖]: 𝑖 < |𝑎|
 14 }
                                                                                   • array dynamic object upper bound in 𝑝 [𝑖]: offset(𝑝) + 𝑖 ·
                                                                                     sizeof (𝑇 ) < object_size(𝑝)
Listing 3: Loop-unwinding refinement proposed for a loop                           • string constant lower bound in 𝑠 [𝑖]: 𝑖 ≥ 0
in vProcessHandleOption, reachable from vDHCPProcess, by                           • string constant upper bound in 𝑠 [𝑖]: 𝑖 < |𝑠 |
the property-guided loop bound refinement technique. The                       (6) Overflow
technique identified a block of code which was not being                           • arithmetic overflow on signed + in 𝑥 + 𝑦: MIN ≤ 𝑥 + 𝑦 ≤
verified, determined it resulted from insuffient loop bounds,                        MAX
and derived the minimal loop bound required for the loop                           • arithmetic overflow on signed − in 𝑥 − 𝑦: MIN ≤ 𝑥 − 𝑦 ≤
exit condition to hold and the block of code to be verified.                         MAX
                                                                                   • arithmetic overflow on signed ∗ in 𝑥 ·𝑦: MIN ≤ 𝑥 ·𝑦 ≤ MAX
                                                                                   • arithmetic overflow on signed shl in 𝑥 ≪ 𝑘: MIN ≤ 𝑥 ·2𝑘 ≤
These differences identify the distinguishing feature of fidelity-
                                                                                     MAX
oriented and safety-oriented unit proofs: fidelity-oriented proofs
                                                                                   • arithmetic overflow on signed unary minus in −𝑥: 𝑥 ≠
may use functions within the project to proactively set up valid
                                                                                     MIN
calling context, while safety-oriented proofs recover these semantic
                                                                                   • arithmetic overflow on signed division in 𝑥/𝑦: ¬(𝑥 =
knowledge as necessary and encode them as explicit assumptions
                                                                                     MIN ∧ 𝑦 = −1)
in the unit proof.
                                                                                   • result of signed mod is not representable in 𝑥 mod 𝑦: ¬(𝑥 =
                                                                                     MIN ∧ 𝑦 = −1)
E Instrumented Memory Safety Properties                                        (7) Undefined-shift
This appendix summarizes the memory-safety properties verified in                  • shift distance is negative in 𝑥 ≪ 𝑘: 𝑘 ≥ 0
this work as part of the experimental evaluation. These properties                 • shift distance too large in 𝑥 ≪ 𝑘: 𝑘 < 𝑤
are instrumented by CBMC and genuine violations can represent                      • shift operand is negative in 𝑥 ≪ 𝑘: 𝑥 ≥ 0
high-impact security vulnerabilities.                                          (8) Division-by-zero
    (1) Assertion                                                                  • division by zero in 𝑥/𝑦 or 𝑥 mod 𝑦: 𝑦 ≠ 0
        • max allocation size exceeded: malloc_size ≤ MAX_SIZE                 (9) Pointer
        • max allocation may fail: ¬should_malloc_fail                             • same object violation in pointer comparison: object(𝑝) =
    (2) Pointer dereference                                                          object(𝑞)
        • dereference failure: pointer NULL in 𝑝: 𝑝 ≠ NULL                    (10) Precondition instance
        • dereference failure: pointer invalid in 𝑝: valid(𝑝)                      • memcpy src/dst overlap: object(𝑠𝑟𝑐) ≠ object(𝑑𝑠𝑡) ∨ 𝑠𝑟𝑐 +
        • dereference failure: deallocated dynamic object in 𝑝: ¬deallocated(𝑝)      𝑛 ≤ 𝑑𝑠𝑡 ∨ 𝑑𝑠𝑡 + 𝑛 ≤ 𝑠𝑟𝑐
        • dereference failure: dead object in 𝑝: ¬dead(𝑝)                          • memcpy source region readable: R_OK(𝑠𝑟𝑐, 𝑛)
        • dereference failure: pointer outside object bounds in 𝑝:                 • memcpy destination region writeable: W_OK(𝑑𝑠𝑡, 𝑛)
           offset(𝑝) + sizeof (∗𝑝) ≤ object_size(𝑝)                                • memset destination region writeable: W_OK(𝑑𝑠𝑡, 𝑛)
        • dereference failure: invalid integer address in 𝑝: object(𝑝) ≠           • memmove source region readable: R_OK(𝑠𝑟𝑐, 𝑛)
           object(NULL) ∨ 𝑝 = NULL                                                 • memmove destination region writeable: W_OK(𝑑𝑠𝑡, 𝑛)
        • no candidates for dereferenced function pointer: false                   • strcpy/strncpy src/dst overlap: object(𝑠𝑟𝑐) ≠ object(𝑑𝑠𝑡)∨
        • dereferenced function pointer must be 𝑓 : fp = 𝑓                           𝑠𝑟𝑐 + 𝑛 ≤ 𝑑𝑠𝑡 ∨ 𝑑𝑠𝑡 + 𝑛 ≤ 𝑠𝑟𝑐
        • dereferenced function pointer must be one of {𝑓1, . . . , 𝑓𝑛 }:          • free argument must be NULL or valid pointer: 𝑝 = NULL∨
           fp ∈ {𝑓1, . . . , 𝑓𝑛 }                                                    R_OK(𝑝, 0)
    (3) Pointer arithmetic                                                         • free argument must be dynamic object: 𝑝 = NULL ∨
        • pointer relation: pointer NULL in 𝑝: 𝑝 ≠ NULL                              dynamic(𝑝)
        • pointer relation: pointer invalid in 𝑝: valid(𝑝)                         • free argument has offset zero: 𝑝 = NULL ∨ offset(𝑝) = 0
        • pointer relation: deallocated dynamic object in 𝑝: ¬deallocated(𝑝)
AutoSOUP: Safety-Oriented Unit Proof Generation for Component-level Memory-Safety Verification                                        XXX ’26, 2026, United States


 1   // Public API. path is user-controlled.                                         Table 6: Comparison AutoSOUP’s performance when using
 2   ssize_t nanocoap_sock_post(nanocoap_sock_t *sock, const char
                                                                                     open-source models
     ↩→ *path, ...)
 3   { return _sock_put_post(sock, path, ...);}
 4
 5   // nanocoap_sock_post -> _sock_put_post ->                                         Metric                               GLM-5        MiniMax M2.5
     ↩→ coap_opt_put_uri_pathquery -> coap_opt_put_string_with_len ->
     ↩→ coap_put_option
                                                                                        Num Targets                            37.0              37.0
 6
 7   size_t coap_opt_put_uri_pathquery(uint8_t *buf, uint16_t                           Compiles (%)                          97.3%             75.7%
     ↩→ *lastonum, const char *uri) {                                                   Structural validity (%)               81.1%             62.2%
 8       coap_opt_put_string_with_len(buf, ..., string, ...);                           Verification completes (%)            86.5%             73.0%
 9   }
10                                                                                      Generation succeeds (%)               78.4%             48.6%
11   // buf is a fixed size buffer from sock->hdr_buf
12   // const char *string contains user-provided string                                Verification time (s)                  98.6              56.9
13   size_t coap_opt_put_string_with_len(uint8_t *buf, ...,                             Avg component size (loc)               99.9              54.6
14                                       const char *string, ...)
15   {                                                                                  Avg covered size (loc)                 90.9              42.7
16       uint8_t *bufpos = buf;                                                         Avg coverage (%)                       96.1              81.5
17       char *uripos = (char *)string;
18                                                                                      Avg num. properties (#)               262.1              174.6
19        while (len) {                                                                 Avg num. verified properties (#)      253.0              170.3
20            uint8_t *part_start = (uint8_t *)uripos;
21            bufpos += coap_put_option(bufpos, ..., part_start, ...);                  Avg num. vulnerabilities (#)           2.1                1.2
22        }
23   }                                                                                  Avg generation time (min)             739.4              83.4
24                                                                                      Avg API cost ($)                       4.9               0.7
25   // odata is user-provided string. olen is its length.
26   size_t coap_put_option(uint8_t *buf, ..., const void *odata,                       Avg proof size (loc)                   48.4              29.6
     ↩→ size_t olen)
27   {
28       assert(lastonum <= onum);
29
                                                                                         Table 7: Summary statistics for the evaluation subjects.
30        n = _put_delta_optlen(buf, n, 0, olen);
31        if (olen) {
32            // Copy of olen bytes into fixed length buffer without                      Software        Size       Stars   Parent modules
              ↩→ validation.
33            memcpy(buf + n, odata, olen);                                               Zephyr-RTOS     2253971    15115   BT, FS, USB, Shell, 6LoWPAN
34            n += olen;                                                                  RIOT-OS         417135     5718    BT, FS, USB, Shell, 6LoWPAN
35        }                                                                               Contiki-NG      186095     1486    BT, FS, USB, Shell, 6LoWPAN
36        return (size_t)n;
37   }
                                                                                          FreeRTOS        836205     7280    Shell, FS, OTA, MQTT, JSON


Listing 4: Sample of out-of-bound write vulnerability on line
                                                                                             in line 5 of Listing 4 are covered. At this point, verification
33 discovered by AutoSOUP in RIOT-OS.
                                                                                             exposes an out-of-bounds write at line 33. Although the
                                                                                             code contains a loop at line 19, the bug manifests without
         • double free: 𝑝 = NULL ∨ ¬deallocated(𝑝)                                           increasing its unwinding limit.
         • free called for new[] object: 𝑝 = NULL ∨ ¬new_array(𝑝)                          • Precondition generation. In Stage 3, AutoSOUP analyzes
         • free called for stack-allocated object: 𝑝 = NULL∨¬stack(𝑝)                        the counterexample trace and infers a precondition that con-
    (11) Precondition                                                                        strains the input (buffer) length to eliminate the reported
         • memcmp region readable: R_OK(𝑠, 𝑛)                                                error.
         • memcpy region readable: R_OK(𝑠, 𝑛)                                              • Precondition validation. The validator performs backward
         • buffer nonnull: 𝑏𝑢 𝑓 ≠ NULL                                                       dataflow analysis to trace the constrained argument to its
         • size greater than zero: 𝑠𝑖𝑧𝑒 > 0                                                  source. It determines that the relevant string originates from
         • buffer writable: W_OK(𝑏𝑢 𝑓 , 𝑠𝑖𝑧𝑒)                                                a parameter of the public API nanocoap_sock_post. Along
         • object overlap: object(𝑝) ≠ object(𝑞)                                             this path, it finds no explicit constraint on the string length.
                                                                                             It therefore flags the inferred precondition as violable in
F        Details of Reported Vulnerabilities                                                 the real environment and reports the corresponding memcpy
   Listing 4 illustrates a vulnerability in RIOT-OS (nanocoap.c)                             out-of-bounds write as a true vulnerability.
discovered by AutoSOUP. The bug is reached along the following                         We reported this issue to the RIOT-OS maintainers, who ac-
execution flow.                                                                      knowledged receipt and began an internal investigation.
    • Initial harness. AutoSOUP first generates a harness for
       coap_opt_put_uri_pathquery, a root function in nanocoap.c.                    G      Additional Evaluation Data and Results
       The harness initializes the buf and string arguments as                       Table 7 summarizes the evaluation subjects. These are embedded
       nondeterministic buffers with unconstrained sizes.                            operating systems developed and maintained by Google (Zephyr-
    • Coverage refinement and bug exposure. Stage 2 then                             RTOS), Amazon Web Services (FreeRTOS), and the international
       resolves coverage gaps until all edges along the call path                    engineering community (RIOT-OS, Contiki-NG).
XXX ’26, 2026, United States                                             Amusuo et al.


  Table 6 compares AutoSOUP’s performance when using two
open-source models, GLM-5 and MiniMax M2.5, across 37 targets.
Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009
