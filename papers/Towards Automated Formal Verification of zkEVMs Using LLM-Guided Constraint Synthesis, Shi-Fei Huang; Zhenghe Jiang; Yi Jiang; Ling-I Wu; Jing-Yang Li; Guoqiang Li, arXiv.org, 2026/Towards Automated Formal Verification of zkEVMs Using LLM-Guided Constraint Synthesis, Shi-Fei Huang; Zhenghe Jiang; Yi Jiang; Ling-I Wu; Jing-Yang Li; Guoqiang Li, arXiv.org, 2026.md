                                         Towards Automated Formal Verification of zkEVMs
                                              Using LLM-Guided Constraint Synthesis
                                                         Shichen Huang∗ , Zhenghe Jiang∗ , Yi Jiang† , Ling-I Wu‡ , Jingyang Li‡ Guoqiang Li‡ B
                                                                                          ∗ Shanghai Polytechnic University
                                                                                   † Nanjing University of Science and Technology
                                                                                           ‡ Shanghai Jiao Tong University



                                            Abstract—Zero-Knowledge Ethereum Virtual Machines                  a critical need for automated, solver-backed formal verification
                                         (zkEVMs) secure Ethereum rollups by generating zero-                  of the source-level zkEVM code [3]–[6].
                                         knowledge proofs that guarantee off-chain execution correctness.         Addressing this challenge involves two distinct layers: au-
                                         However, subtle implementation bugs (e.g., incorrect gas
                                         accounting) can lead to valid proofs certifying semantically          tomated reasoning and verification model synthesis. At the
                                         faulty states, thereby silently defeating cryptographic guarantees.   reasoning layer, modern SMT solvers and symbolic reasoning
                                         Formal verification via SMT solvers can prevent this, but is          engines already provide mature backends for checking logical
                                         bottlenecked by specification: current zkEVM development              constraints over bit-vectors, arrays, and state-transition rela-
                                         practice lacks automated methods to translate Rust opcode             tions [7]–[10]. At the synthesis layer, however, the situation
                                         handlers into verification models. Current practices rely
                                         on unsustainable manual specifications, while LLM-based               is different: solvers can only reason about the constraints they
arXiv:2607.19795v1 [cs.SE] 22 Jul 2026




                                         approaches suffer from hallucination and lack formal                  are given; they do not automatically infer specifications or
                                         guarantees. To address this, we propose VeriSynth, a framework        verification conditions from an implementation [11]–[13]. This
                                         that synthesizes executable Python/Z3 verification models from        semantic gap is especially pronounced in zkEVM implementa-
                                         Rust zkEVM code. VeriSynth enforces a hybrid paradigm:                tions, where complex execution behaviors are implicit in low-
                                         an LLM acts strictly as a formalization frontend to translate
                                         code into symbolic constraints, while an SMT solver serves as         level Rust source code. Consequently, the central bottleneck
                                         the correctness arbiter. To handle complex multi-component            in zkEVM verification is not the capability of the reasoning
                                         state transitions, VeriSynth integrates semantic decomposition,       backend, but the lack of automated, practical tooling for
                                         retrieval-grounded prompting, and verification-guided auto-           translating implicit, source-level Rust semantics into accurate,
                                         repair into a closed-loop pipeline. We evaluate VeriSynth on the      solver-ready verification models at the opcode level.
                                         first source-level zkEVM verification benchmark, encompassing
                                         both correct and faulty opcode implementations. VeriSynth                Current software engineering workflows do not close this
                                         achieves a bug detection rate of over 90%, substantially              synthesis gap, because they leave the constraint-modeling
                                         outperforming direct and conversational LLM baselines, as             burden on human developers. Leading zkEVM projects such
                                         well as a production-grade handwritten mutation-testing suite.        as Scroll rely on manually written specifications and hand-
                                         Ablation studies confirm that each pipeline component is critical     crafted mutation tests to detect semantic bugs [14]. However,
                                         to the framework’s overall effectiveness.
                                            Index Terms—formal verification, specification inference, con-
                                                                                                               maintaining these manual artifacts does not scale as low-
                                         straint synthesis, large language models, SMT solving, zkEVM          level implementations undergo frequent optimization, and tests
                                                                                                               are bounded by the behaviors that developers explicitly an-
                                                                                                               ticipate. Furthermore, while the community has constructed
                                                                I. I NTRODUCTION                               benchmarks for smart contract and EVM bytecode vulnerabil-
                                                                                                               ities [15], there is no standardized, source-level bug benchmark
                                            The massive growth of decentralized software systems has           for zkEVM Rust implementations. As a result, developers
                                         led Ethereum to increasingly offload execution to Layer-              shoulder the modeling effort, and researchers lack a concrete
                                         2 infrastructures called rollups, which scale throughput by           baseline for evaluating automated verification model synthesis
                                         processing transactions off-chain [1]. To ensure the integrity        at the infrastructure layer.
                                         of these decoupled states, the underlying blockchain employs             LLM-based methods offer a potential path to reduce this
                                         a Zero-Knowledge Ethereum Virtual Machine (zkEVM) to                  manual burden, but they are not reliable enough on their
                                         construct mathematical validity proofs that verify off-chain          own. Existing LLM-based specification generators primarily
                                         transitions [2]. However, this verification pipeline relies on        produce high-level declarative properties [16], [17], whereas
                                         a fundamental software engineering assumption: the zkEVM              verifying zkEVM opcode transitions requires detailed exe-
                                         implementation must faithfully realize the intended virtual           cutable models that capture multi-component state updates
                                         machine semantics. If this implementation contains subtle             across stack, memory, storage, gas, and execution context [18],
                                         bugs—such as incorrect gas accounting, missing state updates,         [19]. More critically, direct LLM bug-finding suffers from
                                         or wrong boundary checks—the system can generate valid                code hallucination and provides no formal guarantees. To scale
                                         cryptographic proofs for semantically faulty execution states.        verification to complex systems, a hybrid paradigm is needed:
                                         These silent semantic errors bypass proof verification, creating      the LLM acts strictly as a formalization frontend that translates
Fig. 1. Motivation of LLM-guided verification model synthesis. Existing approaches fail to translate Rust implementations into formal verification models
due to implicit semantics and complex opcode behaviors. Our approach bridges this gap by synthesizing executable SMT constraints that can be directly
validated by a solver.



code into candidate executable SMT constraints, while an                      the detection rate from 91.6% to 66.3%, as many initially
SMT solver serves as the correctness arbiter. No existing                     generated models fail on local syntax or sort errors rather than
automated framework realizes this paradigm for source-level                   semantic misunderstandings. Retrieval grounding and semantic
Rust zkEVM implementations.                                                   decomposition each provide further gains.
   To address these gaps, we introduce VeriSynth, a framework                    To demonstrate practical engineering value, we compare
that synthesizes executable Python/Z3 verification models                     VeriSynth directly with Scroll’s handwritten Rust mutation-
from zkEVM Rust source code. Its core design separates                        test workflow. Scroll’s production-grade tests expose 55 out of
responsibilities: an LLM serves as a formalization frontend                   95 injected bugs, while VeriSynth detects 87—32 additional
that translates source-level code into candidate symbolic con-                bugs that escaped manually written assertions. This gap is con-
straints, while an SMT solver acts as the correctness arbiter:                sistent across both semantic errors and execution-path errors,
the LLM proposes, the solver decides. VeriSynth targets the                   indicating that automated constraint synthesis complements,
full zkEVM execution state, guiding the LLM to extract                        rather than replaces, manual testing pipelines.
semantics that are otherwise implicit in Rust control flow and
encoding them as symbolic variables and constraints covering                     The main contributions of this paper are as follows:
stack manipulations, memory layouts, persistent storage up-
dates, dynamic gas and refund accounting, and execution con-                     • We propose VeriSynth, an LLM-guided verification
text registers. To make these interacting components tractable,                    framework that synthesizes executable Python/Z3 models
the framework integrates three mechanisms into a closed-                           directly from zkEVM Rust source. VeriSynth treats LLMs
loop pipeline: semantic decomposition isolates state transitions                   as formalization frontends and SMT solvers as final
into modular verification units; retrieval-grounded prompting                      validators, integrating semantic decomposition, retrieval-
anchors variable types and solver APIs against previously vali-                    grounded prompting, and verification-guided auto-repair
dated examples; and verification-guided auto-repair iteratively                    into a closed-loop pipeline.
refines generated models using compiler diagnostics and solver                   • We construct the first source-level benchmark for Rust
counterexamples until they compile and verify.                                     opcode implementation verification in zkEVM systems,
   We evaluate VeriSynth on our self-constructed source-level                      spanning five semantic families of injection faults in
zkEVM verification benchmark of 95 injected faulty samples                         control flow, state updates, and resource accounting. This
across five opcode semantic families. VeriSynth detects 87                         benchmark targets implementation-level faults, a cate-
out of 95 bugs, achieving a detection rate of 91.6%, sub-                          gory distinct from existing contract- and bytecode-level
stantially outperforming the LLM-only baseline (46.3%) and                         datasets.
the conversational LLM baseline (61.1%). The framework                           • We conduct a systematic empirical evaluation showing
remains effective across diverse opcode families, with per-                        VeriSynth substantially outperforms direct LLM baselines
family detection rates ranging from 95.5% (arithmetic/bitwise)                     and industrial mutation-testing workflows. Ablation stud-
to 85.7% (call/create paths). Ablation confirms that auto-                         ies confirm that auto-repair and retrieval grounding are
repair is the single largest contributor: removing it drops                        critical for solver compatibility and model executability.
                       II. PRELIMINARY                              under which the implementation violates the property. If it is
A. Zero-Knowledge Ethereum Virtual Machines                         unsatisfiable, the property holds for all executions captured
                                                                    by the encoded model and its assumptions. Although SMT
   A zero-knowledge Ethereum Virtual Machine (zkEVM)
                                                                    solvers provide reliable reasoning backends, they require ex-
executes Ethereum-compatible programs and generates zero-
                                                                    plicit, complete, and correctly typed constraints. Constructing
knowledge proofs showing that the resulting state transitions
                                                                    such verification models from low-level source code therefore
satisfy a predefined constraint system. In rollup systems, trans-
                                                                    remains a major bottleneck. VeriSynth addresses this problem
actions are executed off-chain, while the corresponding proofs
                                                                    by using an LLM to synthesize executable Python/Z3 models
are verified on-chain, allowing a large batch of executions to
                                                                    while retaining the SMT solver as the final correctness arbiter.
be validated without re-executing every instruction.
   An EVM execution state can be abstracted as                      C. Large Language Models
              σ = ⟨pc, stk, mem, sto, gas, env⟩,                       Large language models (LLMs) have demonstrated strong
                                                                    capabilities in source-code understanding, generation, and pro-
where pc denotes the program counter, stk the operand stack,
                                                                    gram repair [18], [21], [22]. Through pretraining on large code
mem the transient memory, sto the persistent storage, gas the
                                                                    corpora and in-context learning, LLMs can infer relationships
remaining gas, and env the execution context. Each opcode o
                                                                    between variables, control-flow branches, function calls, and
defines a transition relation
                                                                    state updates. These capabilities make them useful for trans-
                           To (σ, σ ′ ),                            lating implementation-level program behavior into executable
                                                                    verification scripts.
which specifies how a valid pre-state σ is transformed into
a post-state σ ′ according to the EVM semantics [2], [6].              Recent studies have explored LLMs for formal specifi-
Depending on the opcode, the transition may involve 256-            cation generation, property inference, and feedback-driven
bit arithmetic, stack manipulation, memory expansion, storage       program repair [16], [17], [23]. Nevertheless, generating an
modification, gas accounting, or exceptional control flow.          executable verification model is more demanding than pro-
   A valid zero-knowledge proof guarantees that a witness           ducing a natural-language explanation or a high-level property.
satisfies the constraints encoded in the proving circuit. How-      The model must correctly represent path conditions, symbolic
ever, it does not independently guarantee that the source-          types, state updates, resource accounting, and solver-specific
level executor or witness generator faithfully implements the       APIs. Small mistakes, such as using inconsistent bit-vector
intended EVM semantics. Bugs such as incorrect gas charging,        widths or omitting a branch condition, can make the generated
missing state updates, improper boundary checks, or faulty          model either non-executable or semantically unsound.
control-flow handling may therefore produce valid proofs for           Therefore, LLM-generated artifacts cannot provide formal
semantically incorrect state transitions [20]. This work focuses    correctness guarantees by themselves. VeriSynth uses the
on verifying such implementation-level opcode semantics be-         LLM only as a formalization frontend that translates zkEVM
fore they are incorporated into the proving process.                source code into candidate Python/Z3 models. Compilation
                                                                    diagnostics, type and sort errors, solver exceptions, and coun-
B. Formal Verification                                              terexamples are then used as structured feedback to repair
   Formal verification establishes program correctness by ex-       incomplete or inconsistent models. The LLM proposes the
pressing implementation behavior and required properties as         symbolic model, while the SMT solver determines whether
mathematical constraints. Symbolic execution replaces con-          the encoded correctness properties hold.
crete inputs with symbolic variables and accumulates path
                                                                                           III. A PPROACH
conditions and state-transition constraints, thereby represent-
ing multiple program executions within a single logical                This section presents VeriSynth, an LLM-guided framework
model [11]. This approach is particularly suitable for opcode       for synthesizing executable verification models from source-
implementations whose behavior depends on stack values,             level implementations. The key design principle is to use
storage contents, gas conditions, and execution branches.           LLMs for semantic model construction while leaving correct-
   Satisfiability Modulo Theories (SMT) solvers support log-        ness checking to an SMT solver. Given an input implemen-
ical theories such as fixed-width bit-vectors, integers, arrays,    tation, VeriSynth decomposes the program into verification-
and uninterpreted functions. These theories naturally model         relevant semantic units, retrieves previously validated exam-
EVM word arithmetic, memory and storage structures, con-            ples as semantic anchors, synthesizes executable SMT con-
ditional transitions, and resource constraints [7], [8]. Let        straints, and repairs failed models using compiler and solver
CP (σ, σ ′ ) encode the behavior of an implementation P , and       feedback.
let Φ(σ, σ ′ ) denote an intended semantic or safety property.         Following the generate-and-verify paradigm used in recent
Verification checks the satisfiability of                           LLM-assisted specification generation and repair work [16],
                                                                    [23], VeriSynth adopts an iterative workflow in which can-
                    CP (σ, σ ′ ) ∧ ¬Φ(σ, σ ′ ).
                                                                    didate verification models are generated, checked, and re-
   If the formula is satisfiable, the solver returns a model        fined. However, unlike approaches that generate declarative
that serves as a counterexample, demonstrating an execution         specifications such as JML annotations, VeriSynth generates
executable verification models that can be directly checked by    prevents an incorrect but internally consistent implementation
Z3. This distinction is important for zkEVM implementations,      model from being accepted solely because the generated
where execution semantics such as opcode dispatch, storage        constraints reproduce the same faulty logic.
updates, gas accounting, and environment-dependent behavior
are often implicit in source code rather than written as formal   B. Semantic Decomposition and Retrieval
specifications.                                                      The formulation above assumes a semantic unit u is already
                                                                  isolated. In practice, raw zkEVM source files intermix opcode
A. Overview and Problem Formulation                               handlers, helper routines, and state objects. Directly applying
   The input of VeriSynth is a source program P written           LLMs to such files is unreliable because the relevant semantics
in a supported language. The language-specific front end          are scattered across these components. Therefore, VeriSynth
parses P and normalizes it into an intermediate representation    first decomposes the input into semantically coherent units.
from which verification-relevant semantic units are extracted.    The purpose of decomposition is not merely to reduce prompt
A semantic unit may correspond to an opcode handler, a            length, but to expose state effects that can be modeled inde-
state transition routine, a memory or storage update, or          pendently while preserving explicit dependencies through unit
a helper function that participates in execution semantics.       interfaces.
In the zkEVM context, we classify units into five seman-             For each code fragment, VeriSynth identifies which state
tic families: arithmetic/bitwise, memory/storage, gas/refund,     components it reads and writes, and assigns it to a semantic
call/create paths, and environment/context-dependent behavior.    family. Fragments contributing to the same state transition are
   For each semantic unit u, VeriSynth aims to synthesize an      grouped into one unit. For example, an SSTORE-like unit may
executable verification model:                                    include reading the current storage value, detecting the no-
                     Mu = ⟨Vu , Cu , Φu ⟩,                  (1)   op case, updating the warm-access state, computing gas cost,
                                                                  and writing the new storage value. Although these operations
where Vu is the set of symbolic variables, Cu is the set of       appear as separate statements in Rust, they jointly define one
solver constraints encoding the behavior of u, and Φu is          semantic transition and should be modeled together. Figure 2
the property or consistency obligation to be checked. The         illustrates this mapping for an SSTORE unit.
symbolic state of zkEVM-style code typically contains stack,         Retrieval-augmented prompting has been used to provide
memory, storage, gas, refund, warm-access information, and        LLMs with task-specific context in code and specification
environment variables, following the stateful execution model     generation tasks [17], [19]. In VeriSynth, retrieval is used
of the EVM [2], [6]. The generated constraints describe how       differently: the retrieved examples serve as semantic an-
such a state is transformed by the target unit.                   chors for executable model construction. After decomposition,
   The verification task is to check whether the synthesized      VeriSynth retrieves similar verified examples from a reference
model admits a counterexample under the chosen abstraction.       database:
Given the model in Eq. 1, if Cu ∧ ¬Φu is unsatisfiable, the                           D = {(ur , M r , metar )},
model is accepted with respect to Φu ; otherwise, the solver-
produced counterexample is treated as feedback for repair,        where ur is a reference unit, M r is its verified executable
indicating a potential semantic inconsistency in the original     model, and metar records metadata such as opcode family,
implementation.                                                   state components, and modeling patterns.
   This formulation makes the goal of VeriSynth different            Given a target unit u and a reference unit d, their similarity
from test generation or natural-language explanation. The         is computed as:
framework does not ask the LLM to decide whether a program                            E MB(u) · E MB(d)
is correct. Instead, the LLM proposes an executable model, and    S IM(u, d) = α ·                         + (1 − α) · FAM(u, d),
                                                                                    ∥E MB(u)∥∥E MB(d)∥
the solver validates whether the proposed model satisfies the                                                                  (3)
intended constraints.                                             where E MB(·) denotes the code embedding and FAM(u, d)
   VeriSynth separates the model extracted from the target        rewards matches in opcode family or semantic category. Based
implementation from the obligations used to evaluate it. For      on this similarity measure (Eq. 3), the top-k examples are used
a semantic unit u, Cuimpl (σ, σ ′ ) encodes the behavior of the   as semantic anchors for synthesis.
source implementation, while Φu is constructed from validated        The retrieved examples are not copied as templates. Instead,
opcode semantics and family-specific consistency rules rather     they serve as a modeling prior: they stabilize the symbolic
than from the target code alone. The verification query is        vocabulary, state schema, and transition structure by grounding
                                                                  generation in previously validated modeling decisions. Each
                 Cuimpl (σ, σ ′ ) ∧ ¬Φu (σ, σ ′ ).          (2)
                                                                  reference entry is added to the retrieval database only after its
Typical obligations include arithmetic equivalence, stack-        executable model passes syntax checking, sort checking, solver
height preservation, storage-update consistency, gas and refund   execution, and the associated semantic obligations. During
bounds, and correct failure or return-value propagation. A        retrieval, VeriSynth prioritizes examples with compatible op-
satisfiable query yields an input state under which the im-       code families, accessed state components, and symbolic types.
plementation violates the expected behavior. This separation      The retrieved models guide symbolic declarations, transition
Fig. 2. Example of semantic-to-SMT synthesis. Given a Rust implementation of the SSTORE opcode, VeriSynth maps key semantic operations to precise
state-transition constraints and safety properties, producing an executable verification model ready for SMT solving.



structures, and solver usage rather than being directly copied.              constraints such as gas and refund behavior, and assertions or
To prevent evaluation leakage, examples sharing the same                     safety obligations.
source-file identity or opcode unit with the target are excluded                To illustrate the intended mapping from code to constraints,
from the candidate set.                                                      consider a simplified SSTORE unit (illustrative example):

C. LLM-Guided Constraint Synthesis                                                   no op := (cur = val),
   VeriSynth uses a typed symbolic state shared across gener-                        warm′ := true,
ated models. EVM words are represented as fixed-width bit-                        gas cost := ite(no op, 0, sstore cost(cur, val)),
vectors, control flags as Boolean expressions, and memory and                         gas′ := gas − gas cost,
storage as symbolic arrays. The state is divided into pre-state                      store′ := ite(no op, cur, val).
and post-state variables:
                                                                             The corresponding safety obligations can be written as:
              σ = ⟨stk, mem, sto, gas, ref, ctx, status⟩,
                                                                       (4)                         gas′ ≥ 0,
       σ ′ = ⟨stk ′ , mem′ , sto′ , gas′ , ref ′ , ctx′ , status′ ⟩.
                                                                                                no op ⇒ store′ = cur,
Source-level branches are translated into guarded constraints
                                                                                               ¬no op ⇒ store′ = val.
or Z3 If expressions, while Rust assignments define equalities
over post-state variables. Each state component must either                  D. Executable Verification and Auto-Repair
be explicitly updated or connected to its pre-state through                     The generated model may still fail verification. Common
a frame condition. For example, an opcode that does not                      failures include missing declarations, invalid Python or Z3 API
modify memory introduces mem′ = mem. These frame                             usage, bit-vector sort mismatches, incomplete state updates, or
conditions prevent omitted updates from leaving post-state                   semantic inconsistencies exposed by counterexamples. Instead
variables unconstrained. The encoding also enforces consistent               of discarding failed models, VeriSynth repairs them using
bit-vector widths and explicit status variables for exceptional              structured feedback from the compiler and solver, following
exits, reducing ambiguity during constraint synthesis and pro-               the broader idea of feedback-driven LLM repair [23].
viding structured targets for solver-guided repair.                             As formalized in Eq. 5, given a candidate model M    cu , the
   LLMs have shown strong capabilities in code generation                    verifier returns:
and code understanding [21], [24]. In VeriSynth, we use this                                          cu ) = ⟨ok, e, w⟩,
                                                                                              V ERIFY(M                                      (5)
capability to translate each semantic unit into an executable
SMT model rather than a natural-language description. For a                  where ok indicates whether the model passes verification, e is
target unit u, the prompt contains four parts: the source code               the error class, and w is an optional witness such as a compiler
of u, the retrieved semantic anchors, opcode-aware modeling                  trace or solver counterexample.
instructions, and the required output format. The opcode-aware                  Verification proceeds in four stages. VeriSynth first parses
instructions specify the relevant symbolic state schema (stack,              and imports the generated Python script, then constructs
memory, storage, gas, environment variables) and modeling                    the symbolic expressions to detect missing declarations and
obligations for the semantic family of u, guiding the LLM to                 sort mismatches. Next, it executes the solver query under a
encode the appropriate variable types, transition structure, and             bounded timeout and finally checks the semantic obligations.
safety assertions. When repair is needed, compiler diagnostics               When a stage fails, only the corresponding diagnostic and the
or solver feedback are additionally appended to the prompt.                  relevant model fragment are returned to the LLM, enabling
   The synthesized constraint set falls into four categories:                localized repair while preserving constraints that have already
guard and path conditions, state-transition constraints, resource            passed earlier checks.
                              TABLE I                                            must pass syntax, sort, execution, and semantic checks. Thus,
                  LLM- GUIDED SYNTHESIS AND REPAIR .                             an unsatisfiable query establishes correctness only within the
                                                                                 modeled state and assumptions, rather than for the entire
 Input             P (source program), D (reference database), R
                   (repair action set), k (retrieval count), Tmax (repair        zkEVM implementation.
                   budget).
 Output            Verified executable models for all accepted units.                              IV. E XPERIMENTAL S ETUP
 Procedure         1) Parse and normalize P .                                      In this section, we introduce the experimental design,
                   2) Decompose P into semantic units.
                   3) Initialize Mfinal ← ∅.
                                                                                 dataset, baselines, and evaluation metrics used to evaluate
                   4) For each unit u:                                           VeriSynth. Our experiments are organized around the follow-
                       a) Identify semantic family f (u).                        ing research questions:
                       b) Retrieve top-k anchors from D.
                                                                                   • RQ1: Effectiveness. How accurately can VeriSynth de-
                       c) Synthesize candidate model M   cu .
                       d) Verify Mcu .                                               tect opcode-related semantic bugs?
                       e) If verification fails, repair the model using            • RQ2: Opcode-Family Generalization. Does VeriSynth
                           compiler/solver feedback.                                 remain effective across different opcode semantic fami-
                       f) Repeat until accepted or Tmax is reached.                  lies?
                                                                                   • RQ3: Ablation. How much do semantic decomposition,
                            TABLE II                                                 retrieval grounding, opcode-aware prompting, auto-repair,
       E RROR CATEGORIES AND REPAIR ACTIONS IN V ERI S YNTH .                        and solver-backed validation contribute to the final per-
   Error       Source           Repair Action                                        formance?
   Parse       Compiler         Fix syntax, imports, and missing declarations.     • RQ4: Token Cost. What is the token cost of the full
   Sort        Z3 exception     Align bit-vector widths and symbolic sorts.
                                                                                     verification pipeline?
   Execution   Traceback        Repair invalid APIs and solver construction.
   Semantic    Counterexample   Refine guards, transitions, and constraints.       • RQ5: Practical Value. Compared with Scroll’s hand-
                                                                                     written Rust mutation-test workflow, what additional bug-
                                                                                     detection value does VeriSynth provide?
  We classify repair-relevant failures into four categories:
                   E = {Eparse , Esort , Eexec , Esem }.                         A. Implementation

Here, Eparse denotes syntax or missing-declaration errors,                          We implement VeriSynth as a prototype framework that in-
Esort denotes type or sort mismatches, Eexec denotes solver                      tegrates language-specific front ends, retrieval-guided prompt-
execution failures or timeouts, and Esem denotes semantic                        ing, executable Python/Z3 model synthesis, and verification-
inconsistencies exposed by solver witnesses.                                     guided repair. The current prototype supports source-level
   For each error class e, VeriSynth maintains a candidate                       analysis of Rust programs and generates Python/Z3 verifica-
repair set R(e). A repair action may complete missing dec-                       tion scripts. For each target program, VeriSynth first extracts
larations, correct bit-vector widths, replace invalid operators,                 verification-relevant semantic units, retrieves similar verified
refine guard constraints, patch state updates, or regenerate a                   examples from a reference database, generates executable
localized fragment of the model. Repair actions are applied in                   SMT models, and invokes Z3 to check the synthesized con-
a fixed priority per error class (Table II), favoring actions with               straints.
minimal structural modification.                                                    We use GPT-4o as the backend LLM in the current evalua-
   Table I summarizes the overall procedure. The loop termi-                     tion. The maximum number of repair iterations is set to 3. For
nates when the model passes all verification phases or the                       each sample, we record the final detection result, executability
repair budget is exhausted. This bounded process prevents                        status, repair behavior, and token usage. Since the current
unbounded regeneration and makes the system behavior mea-                        prototype is intended for offline verification of security-critical
surable.                                                                         implementation logic, our cost analysis focuses on token
   Finally, VeriSynth is verification-guided rather than LLM-                    consumption rather than online runtime overhead.
trusting. The LLM proposes candidate models; the compiler
and SMT solver check their executability and internal con-                       B. Dataset
sistency. This shifts error detection from LLM judgment to
machine-checkable consistency. Thus, the framework uses                            We evaluate VeriSynth on a self-constructed benchmark
LLMs to reduce the manual burden of formal modeling                              of 95 negative samples derived from zkEVM-style opcode
while retaining solver-backed checking as the final validation                   implementation logic. Each sample contains one localized
mechanism.                                                                       opcode-related bug injected into a target semantic unit while
   The guarantees of VeriSynth are relative to the extracted                     preserving most of the surrounding code structure. The bench-
semantic unit, symbolic abstraction, and encoded obligations.                    mark is designed to evaluate whether VeriSynth can detect
The LLM is not treated as a correctness oracle; its output                       semantic inconsistencies in implementation-level opcode logic.
   1) Negative-sample Construction: To construct the bench-                                 TABLE III
mark, we inject one bug into each target unit. The injected            OVERALL BUG DETECTION EFFECTIVENESS ON THE 95- SAMPLE
                                                                                           BENCHMARK .
errors include wrong arithmetic rules, incorrect boundary han-
dling, missing state updates, wrong return-value propagation,              Approach               Detected / Total    DR
incorrect gas/refund logic, and execution-path mistakes in                 LLM-only                   44 / 95        46.3%
handlers such as CALL and CREATE. The samples cover                        Conversational LLM         58 / 95        61.1%
five opcode semantic families: arithmetic and bitwise oper-                VeriSynth                  87 / 95        91.6%
ations, memory and storage operations, gas and refund logic,
call/create paths, and environment/context-dependent behavior.
   To avoid retrieval leakage, reference examples used by the      Detection rate is reported on negative samples only; systematic
retrieval module are isolated from target samples by source-file   false-alarm estimation on positive samples is deferred to future
identity and opcode unit. Thus, the retrieved examples provide     work.
semantic anchors for modeling without directly exposing the           Executability Rate (ER). ER measures the fraction of gen-
target mutation.                                                   erated verification models that can be successfully compiled
   2) Positive Samples: In addition to negative samples, we        and executed:
                                                                                                  Nexecutable
use original non-mutated implementation units for internal                                ER =                .
sanity checking and executability analysis. The main reported                                       Ntotal
effectiveness results focus on the 95 negative samples.              Token Cost. We report the average token usage per sample
                                                                   and estimate the total token consumption for one full bench-
C. Baselines                                                       mark run. This metric reflects the cost of LLM-based synthesis
   We compare VeriSynth with the following baselines.              and repair.
   LLM-only. This baseline directly asks the LLM to identify
the bug or generate a verification script without semantic                         V. E XPERIMENTAL R ESULTS
decomposition, retrieved examples, opcode-aware prompts,              This section reports the experimental results of VeriSynth.
Z3-backed validation, or structured auto-repair. It represents     We organize the results according to the five research ques-
the simplest LLM-based setting.                                    tions introduced in Section IV. Overall, the results show that
   Conversational LLM. This baseline allows the model to           VeriSynth substantially outperforms LLM-only baselines in
revise its output using compiler or solver feedback. However,      opcode-level bug detection, remains effective across different
it does not use retrieved semantic anchors or structured repair    opcode semantic families, and benefits from each major com-
actions. This baseline is used to evaluate whether feedback        ponent in the pipeline. We further analyze the token cost of
alone is sufficient for robust verification model construction.    the framework and compare its practical value with Scroll’s
   Handwritten Rust tests. For practical comparison, we            handwritten Rust mutation-test workflow.
use Scroll’s handwritten Rust mutation-test workflow as an
engineering baseline. For each sample, the mapped Rust             A. RQ1: Overall Bug Detection Effectiveness
source file is patched, the corresponding cargo test entry            RQ1 evaluates whether VeriSynth can effectively detect in-
is executed, and the original implementation is restored after     jected opcode-level semantic bugs. We conduct the experiment
the test. We count both assertion failures and compilation fail-   on the 95-sample negative benchmark. Each sample contains
ures as successful exposures, since both prevent the mutated       one localized opcode-related bug, such as an incorrect arith-
implementation from passing the test workflow. This baseline       metic rule, missing state update, wrong boundary condition,
is used in RQ5.                                                    incorrect gas/refund logic, or execution-path error in handlers
   VeriSynth. The full system includes semantic decom-             such as CALL and CREATE.
position, retrieval-guided constraint synthesis, opcode-aware         We compare VeriSynth with the baselines described in
prompting, executable Z3 verification, and auto-repair.            Section 4.3: LLM-only, Conversational LLM, and Handwritten
                                                                   Rust tests (for RQ5).
D. Evaluation Metrics                                                 The conversational baseline is inspired by feedback-driven
  We use the following metrics to evaluate effectiveness and       LLM repair settings [23]. As shown in Table III, VeriSynth
cost.                                                              detects 87 out of 95 injected bugs, achieving a detection rate of
  Detection Rate (DR). DR measures the fraction of negative        91.6% (DR defined in Section 4.4). In contrast, the LLM-only
samples correctly identified as semantically inconsistent:         baseline detects only 44 bugs, corresponding to a detection rate
                                                                   of 46.3%. Although the conversational baseline improves over
                               Ndetected
                        DR =             .                         LLM-only generation by using feedback, it still detects only 58
                               Nnegative
                                                                   bugs. These results indicate that feedback alone is insufficient
A bug is considered detected when the synthesized verification     for reliable verification model construction. The improvement
model is executable and the SMT solver finds a counterexam-        of VeriSynth comes from the combination of semantic decom-
ple (Cu ∧¬Φu satisfiable), indicating a semantic inconsistency     position, retrieval-grounded modeling, opcode-aware prompts,
between the encoded constraints and the safety obligations.        and solver-guided repair.
                          TABLE IV                                                              TABLE V
   B UG DETECTION RESULTS ACROSS OPCODE SEMANTIC FAMILIES .         A BLATION STUDY OF V ERI S YNTH COMPONENTS ON THE 95- SAMPLE
                                                                                             BENCHMARK .
     Opcode Family              Detected / Total    DR
     Arithmetic and Bitwise         21 / 22        95.5%           Variant                      Detected / Total     DR       ER
     Memory and Storage             24 / 26        92.3%           w/o Decomposition                72 / 95         75.8%    81.1%
     Gas and Refund                 14 / 15        93.3%           w/o Retrieval                    68 / 95         71.6%    78.9%
     Call/Create Paths              18 / 21        85.7%           w/o Opcode-aware Prompt          74 / 95         77.9%    84.2%
     Environment and Context        10 / 11        90.9%           w/o Auto-Repair                  63 / 95         66.3%    66.3%
     Overall                        87 / 95        91.6%           w/o Z3 Validation                45 / 95         47.4%      –
                                                                   Full VeriSynth                   87 / 95         91.6%    93.7%


   The result also supports our central design choice: LLMs
should not be used as final bug judges. Instead, they are more    C. RQ3: Ablation Study
effective when used as semantic model constructors, while            RQ3 evaluates the contribution of each major component
the final validation is performed by an SMT solver. This          in VeriSynth. We consider five ablated variants. The first
distinction explains why VeriSynth outperforms direct LLM-        removes semantic decomposition and directly feeds larger
based detection.                                                  code fragments to the LLM. The second removes retrieval
  RQ1: VeriSynth detects 87 out of 95 injected opcode-level       grounding and generates verification models without semanti-
  bugs, achieving a detection rate of 91.6%. This substantially   cally similar reference examples. The third removes opcode-
  outperforms LLM-only detection and conversational LLM           aware prompting and uses a generic prompt for all opcode
  repair, showing the effectiveness of solver-backed verifica-    families. The fourth removes auto-repair and accepts only the
  tion model synthesis.                                           initially generated verification model. The fifth removes Z3
                                                                  validation, reducing the system to an LLM-only judgment
                                                                  setting.
B. RQ2: Effectiveness Across Opcode Semantic Families
                                                                     Table V shows that removing any major component reduces
   RQ2 investigates whether VeriSynth remains effective           the final performance. The largest drop occurs when auto-
across different opcode semantic families. This question is im-   repair is removed. Without auto-repair, the detection rate
portant because zkEVM implementation bugs are not limited         decreases from 91.6% to 66.3%, and the executability rate also
to simple arithmetic operations. Many difficult cases involve     drops to 66.3%. This indicates that many initially generated
storage updates, memory behavior, call/create execution paths,    Python/Z3 scripts are semantically close to the desired model
gas accounting, and environment-dependent logic. Therefore,       but fail due to local syntax errors, missing declarations, invalid
we divide the 95 negative samples into five semantic families     solver API usage, or bit-vector sort mismatches. The repair
and report the detection results for each family.                 loop is therefore essential for turning near-valid candidate
   Table IV shows that VeriSynth performs well across all         models into executable verification artifacts. Qualitatively,
semantic families. The highest detection rate is achieved on      most repair actions addressed parse and sort errors (miss-
arithmetic and bitwise operations, where the state transition     ing declarations, bit-vector width mismatches), while fewer
is relatively local and can be naturally encoded using bit-       involved semantic counterexample-guided refinement.
vector constraints. The framework also performs strongly on          Removing retrieval grounding also causes a clear perfor-
memory/storage and gas/refund cases, demonstrating that it        mance drop, reducing the detection rate to 71.6%. Without
can model nontrivial state changes beyond simple numerical        retrieved examples, the LLM is more likely to produce incon-
operations.                                                       sistent symbolic variables, incomplete transition relations, or
   The most challenging category is call/create paths, where      missing resource constraints. This confirms that retrieval acts
VeriSynth detects 18 out of 21 bugs. This lower detection         as a modeling prior rather than ordinary context augmentation.
rate is expected because call/create semantics involve multiple      Removing semantic decomposition reduces the detection
interacting components, including execution context, return       rate to 75.8%. This variant particularly struggles with complex
values, address creation, memory effects, and failure prop-       opcode handlers, where relevant state effects are scattered
agation. Even in this category, VeriSynth still achieves an       across helper routines, state objects, and conditional branches.
85.7% detection rate, suggesting that the proposed semantic       By contrast, semantic decomposition isolates verification-
decomposition and retrieval grounding are useful for complex      relevant units and makes the model synthesis task more
opcode-level behaviors.                                           tractable.
  RQ2: VeriSynth remains effective across different opcode           Removing opcode-aware prompting reduces the detection
  semantic families. While call/create paths are more chal-       rate to 77.9%. This result suggests that generic prompts are
  lenging than arithmetic operations, the framework still         insufficient for diverse opcode families. Arithmetic operations,
  detects most injected bugs in complex state-transition sce-     storage updates, gas accounting, and call/create paths require
  narios.                                                         different symbolic state schemas and modeling obligations.
                             TABLE VI                                                          TABLE VII
    T OKEN COST OF V ERI S YNTH ON THE 95- SAMPLE BENCHMARK .         P RACTICAL COMPARISON WITH S CROLL’ S HANDWRITTEN RUST TESTS .

            Metric                          Value                     Bug Group                      Total     Handwritten      VeriSynth
            Benchmark size                95 samples                  Opcode semantic errors          75           44              69
            Backend model                  GPT-4o                     Opcode execution-path           20           11              18
            Average tokens per sample       ∼100K                     errors
            Estimated total tokens          ∼9.5M                     Overall                          95           55               87
            Average repair rounds             1.8
            Maximum repair budget              3



   Finally, the variant without Z3 validation detects only 45 out
of 95 bugs. This result is close to the LLM-only baseline and
confirms that the final judgment must remain solver-backed.
The LLM can propose candidate models, but Z3 is necessary
for reliable verification.
  RQ3: All major components contribute to the effective-
  ness of VeriSynth. Auto-repair has the largest impact on
  executability, while retrieval and decomposition improve
                                                                     Fig. 3. Practical comparison between handwritten Rust tests and VeriSynth
  semantic consistency and robustness on complex opcode              by bug category on the test_neg benchmark.
  handlers.

                                                                      RQ4: Each sample consumes approximately 100K tokens
                                                                      on average, resulting in about 9.5M tokens for the 95-
D. RQ4: Token Cost Analysis                                           sample benchmark. Although the cost is nontrivial, it
                                                                      remains bounded by the repair budget and is suitable for
   RQ4 analyzes the token cost of VeriSynth. Since the cur-           offline verification of security-critical zkEVM implementa-
rent prototype relies on LLM calls for constraint synthesis           tion logic.
and repair, token usage is an important practical factor. We
therefore measure the average token consumption per sample           E. RQ5: Practical Value Compared with Handwritten Rust
and estimate the total cost for one full run over the 95-sample      Tests
benchmark.
                                                                        RQ5 evaluates whether VeriSynth provides practical value
   As shown in Table VI, each sample consumes approx-
                                                                     beyond a handwritten Rust mutation-test workflow. For this
imately 100K tokens on average. This includes the target
                                                                     comparison, we report results grouped into two high-level
semantic unit, retrieved anchors, opcode-aware modeling in-
                                                                     categories that complement the per-family breakdown in RQ2:
structions, generated Python/Z3 scripts, compiler diagnostics,
                                                                     opcode semantic errors (spanning arithmetic, memory/storage,
solver feedback, and repair prompts. For the 95-sample bench-
                                                                     gas/refund, and environment families) and opcode execution-
mark, the estimated total token usage is approximately 9.5M
                                                                     path errors (spanning call/create path and branch logic). For
tokens.
                                                                     each negative sample, the handwritten baseline temporarily
   The token cost is nontrivial. However, it is bounded by the       patches the mapped Scroll source file, runs the correspond-
repair budget and predictable in practice. In our current setting,   ing cargo test entry in the original crate environment,
the maximum number of repair iterations is limited to 3, and         and then restores the original implementation. This baseline
the average number of repair rounds is 1.8. This suggests that       reflects a realistic engineering workflow: it uses tests that are
most failed generations can be repaired within a small number        already maintained with the project, but its effectiveness is
of iterations.                                                       bounded by the assertions and execution cases that developers
   It is also important to note that VeriSynth is designed for       have manually written.
offline verification of security-critical implementation logic          Table VII and Fig. 3 report the comparison on our 95-sample
rather than online per-transaction execution. Therefore, the to-     negative benchmark, denoted as test_neg. The handwritten
ken overhead is acceptable for scenarios such as opcode imple-       Rust workflow exposes 55 injected bugs, while VeriSynth
mentation review, regression checking after code changes, and        detects 87. The gap is consistent across both groups: for
validation of high-risk state-transition logic. Compared with        opcode semantic errors, handwritten tests expose 44 out of 75
the manual effort required to construct Python/Z3 verification       cases, whereas VeriSynth detects 69; for opcode execution-
models, the LLM cost provides a practical tradeoff between           path errors, handwritten tests expose 11 out of 20 cases,
automation and verification rigor.                                   whereas VeriSynth detects 18. Overall, this corresponds to a
detection rate of 57.9% for handwritten tests and 91.6% for        of concrete executions, and their effectiveness depends on the
VeriSynth.                                                         selected inputs, assertions, and comparison oracles. Bugs in-
   Even under this counting (see Section 4.3), handwritten tests   volving uncommon storage states, gas boundaries, exceptional
leave a substantial fraction of negative samples unexposed.        branches, or interactions between execution components may
VeriSynth improves coverage by synthesizing explicit semantic      therefore remain unexposed. VeriSynth complements these
constraints and checking them with Z3, which makes it less         techniques by constructing symbolic transition models and
dependent on whether a particular behavior has already been        using SMT-generated counterexamples to reason about classes
encoded as a manual unit-test assertion.                           of executions rather than individual test inputs.
  RQ5: Compared with Scroll’s handwritten Rust mutation-
  test workflow, VeriSynth detects 87 bugs on test_neg,            C. Large Language Models for Software Engineering
  while handwritten tests expose 55. The improvement across           Large language models (LLMs) have been increasingly
  both semantic and execution-path bug groups indicates that       applied to software engineering tasks, including code under-
  VeriSynth is a practical complement to manually main-            standing, code generation, test generation, program repair, and
  tained Rust tests.                                               code summarization [18], [21], [22], [24]. Their in-context
                                                                   learning ability allows developers to provide task descriptions,
                    VI. R ELATED W ORK
                                                                   demonstrations, and feedback through prompts [18], [19].
A. Formal Semantics and Verification of EVMs                       Instruction tuning and reasoning-oriented prompting can fur-
   A substantial body of work has studied the formal semantics     ther improve the controllability and consistency of generated
and verification of Ethereum programs. KEVM provides an ex-        artifacts [26]–[28]. Recent studies have extended these capa-
ecutable formal semantics of the EVM in the K framework and        bilities to formal specification generation. SpecGen generates
enables reasoning about bytecode-level execution [6]. Tools        program specifications from source code, while PropertyGPT
such as ZEUS and Securify analyze smart contracts against          combines retrieval with LLM generation to infer properties for
predefined safety properties using abstract interpretation, sym-   smart contracts [16], [17]. These approaches mainly produce
bolic reasoning, or compliance and violation patterns [4], [5].    declarative properties or annotations, whereas zkEVM verifi-
These approaches primarily target smart contracts or EVM           cation requires executable models that encode complete state
bytecode and generally assume that the underlying virtual-         transitions across multiple execution-state components.
machine implementation correctly realizes the intended se-            LLMs have also been used to improve software artifacts
mantics.                                                           through execution feedback. Conversational automated pro-
   Recent work has also examined the soundness and com-            gram repair, for example, iteratively revises candidate patches
pleteness of zkEVM constraint systems. For example, auto-          using compiler errors, test failures, and runtime diagnos-
mated vetting techniques detect under-constrained or over-         tics [23]. However, LLM-generated verification models may
constrained behaviors in zkEVM circuits and witness gen-           contain hallucinated semantics, omitted path conditions, in-
eration [20]. Such work is complementary to VeriSynth:             consistent symbolic types, or invalid solver operations. Conse-
circuit-level verification checks whether a proving system         quently, our goal is not to use an LLM as a direct bug detector
correctly constrains its witnesses, whereas VeriSynth focuses      or correctness oracle. Instead, VeriSynth uses the LLM as a
on whether source-level Rust opcode handlers correctly im-         formalization frontend that translates implementation-level op-
plement the intended state transitions. In addition, existing      code semantics into executable SMT-based verification mod-
formal-verification approaches usually require manually writ-      els. Semantic decomposition and retrieval-grounded prompting
ten semantics or properties. VeriSynth instead synthesizes         guide model generation, while compiler diagnostics and solver
executable Python/Z3 models directly from source-level im-         feedback support bounded auto-repair. The final correctness
plementations.                                                     decision is always made by the SMT solver.

B. Testing and Validation of EVM Implementations                                        VII. C ONCLUSION
   Production EVM and zkEVM projects rely extensively                 We introduced VeriSynth, an LLM-guided framework that
on unit tests, integration tests, official Ethereum execution      synthesizes executable Python/Z3 verification models from
vectors, and regression testing. These techniques are effective    zkEVM Rust source code by combining semantic decompo-
for checking known corner cases and preventing previously          sition, retrieval-grounded prompting, and verification-guided
discovered defects from reappearing. Mutation testing can          auto-repair. On our self-constructed benchmark of 95 injected
further evaluate whether a test suite exposes deliberately         opcode-level bugs, VeriSynth detects 91.6%, outperforming
injected implementation faults.                                    direct LLM baselines (46.3–61.1%) and Scroll’s handwritten
   Differential testing provides another practical validation      mutation-test suite (57.9%).
strategy. EVMFuzz, for example, generates and mutates con-            Our framework remains effective across all five opcode se-
tract inputs and compares the resulting executions across          mantic families, including complex call/create paths (85.7%).
different EVM implementations [25]. Disagreements in return        Ablation confirms that auto-repair contributes the largest gain
values, traces, or gas consumption can reveal implementation       in executability, followed by retrieval grounding. Compared
defects. However, testing and fuzzing reason about a finite set    with Scroll’s handwritten tests, VeriSynth detects 32 additional
bugs, indicating that automated constraint synthesis comple-                     [15] F. Salzano, C. K. Antenucci, S. Scalabrino, G. Rosa, R. Oliveto, and
ments manual testing.                                                                 R. Pareschi, “An empirical analysis of vulnerability detection tools for
                                                                                      solidity smart contracts using line level manually annotated vulnerabil-
  Future work includes systematic false-alarm estimation                              ities,” Empirical Software Engineering, vol. 31, no. 5, p. 143, 2026.
on positive samples, cross-project validation on additional                      [16] L. Ma, S. Liu, Y. Li, X. Xie, and L. Bu, “Specgen: Automated
zkEVM implementations, and cost reduction through smaller                             generation of formal program specifications via large language models,”
model distillation.                                                                   in Proceedings of the 47th IEEE/ACM International Conference on
                                                                                      Software Engineering, 2025.
                              R EFERENCES                                        [17] Y. Liu, Y. Li, L. Ma, and Y. Liu, “Propertygpt: Llm-driven
 [1] Ethereum           Foundation,         “Zero-knowledge          rollups,”        formal verification of smart contracts through retrieval-augmented
     https://ethereum.org/en/developers/docs/scaling/zk-rollups/, accessed:           property generation,” arXiv preprint arXiv:2405.02580, 2024. [Online].
     2026-06-27.                                                                      Available: https://arxiv.org/abs/2405.02580
 [2] G. Wood, “Ethereum: A secure decentralised generalised transaction          [18] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal,
     ledger,” Ethereum Yellow Paper, 2014. [Online]. Available:                       A. Neelakantan, P. Shyam, G. Sastry, A. Askell et al., “Language models
     https://ethereum.github.io/yellowpaper/paper.pdf                                 are few-shot learners,” Advances in Neural Information Processing
 [3] L. Luu, D.-H. Chu, H. Olickel, P. Saxena, and A. Hobor, “Making smart            Systems, vol. 33, pp. 1877–1901, 2020.
     contracts smarter,” in Proceedings of the 2016 ACM SIGSAC Conference        [19] J. White, Q. Fu, S. Hays, M. Sandborn, C. Olea, H. Gilbert, A. Elnashar,
     on Computer and Communications Security, 2016, pp. 254–269.                      J. Spencer-Smith, and D. C. Schmidt, “A prompt pattern catalog to
 [4] P. Tsankov, A. Dan, D. Drachsler-Cohen, A. Gervais, F. Buenzli, and              enhance prompt engineering with chatgpt,” in Proceedings of the 30th
     M. Vechev, “Securify: Practical security analysis of smart contracts,” in        Conference on Pattern Languages of Programs, 2023.
     Proceedings of the 2018 ACM SIGSAC Conference on Computer and
     Communications Security, 2018, pp. 67–82.                                   [20] X. Peng, Z. Sun, K. Zhao, Z. Ma, Z. Li, J. Jiang, X. Luo, and Y. Zhang,
 [5] S. Kalra, S. Goel, M. Dhawan, and S. Sharma, “Zeus: Analyzing safety             “Automated soundness and completeness vetting of polygon {zkEVM},”
     of smart contracts,” in Proceedings of the Network and Distributed               in 34th USENIX Security Symposium (USENIX Security 25), 2025, pp.
     System Security Symposium, 2018.                                                 4093–4108.
 [6] E. Hildenbrandt, M. Saxena, N. Rodrigues, X. Zhu, P. Daian, D. Guth,        [21] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan,
     B. M. Moore, D. Park, Y. Zhang, A. Stefanescu, and G. Rosu, “Kevm:               H. Edwards, Y. Burda, N. Joseph, G. Brockman et al., “Evaluating large
     A complete formal semantics of the ethereum virtual machine,” in Pro-            language models trained on code,” arXiv preprint arXiv:2107.03374,
     ceedings of the 31st IEEE Computer Security Foundations Symposium,               2021. [Online]. Available: https://arxiv.org/abs/2107.03374
     2018, pp. 204–217.
                                                                                 [22] X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li,
 [7] L. de Moura and N. Bjørner, “Z3: An efficient smt solver,” in Proceed-
                                                                                      X. Luo, D. Lo, J. Grundy, and H. Wang, “Large language
     ings of the 14th International Conference on Tools and Algorithms for
                                                                                      models for software engineering: A systematic literature review,”
     the Construction and Analysis of Systems, 2008, pp. 337–340.
                                                                                      arXiv preprint arXiv:2308.10620, 2023. [Online]. Available:
 [8] C. Barrett, A. Stump, and C. Tinelli, “The smt-lib standard: Version
                                                                                      https://arxiv.org/abs/2308.10620
     2.0,” Department of Computer Science, The University of Iowa, Tech.
     Rep., 2010. [Online]. Available: http://smtlib.cs.uiowa.edu/                [23] C. S. Xia and L. Zhang, “Conversational automated program
 [9] C. Cadar, D. Dunbar, and D. Engler, “Klee: Unassisted and automatic              repair,” arXiv preprint arXiv:2301.13246, 2023. [Online]. Available:
     generation of high-coverage tests for complex systems programs,” in              https://arxiv.org/abs/2301.13246
     Proceedings of the 8th USENIX Symposium on Operating Systems                [24] OpenAI, “Gpt-4 technical report,” arXiv preprint arXiv:2303.08774,
     Design and Implementation, 2008, pp. 209–224.                                    2023. [Online]. Available: https://arxiv.org/abs/2303.08774
[10] D. Kroening, E. Clarke, and F. Lerda, “A tool for checking ansi-c
     programs,” in Proceedings of the 10th International Conference on Tools     [25] Y. Fu, M. Ren, F. Ma, X. Yang, H. Shi, S. Li, and X. Liao, “Evm-
     and Algorithms for the Construction and Analysis of Systems, 2004, pp.           fuzz: Differential fuzz testing of ethereum virtual machine,” Journal of
     168–176.                                                                         Software: Evolution and Process, vol. 36, no. 4, p. e2556, 2024.
[11] J. C. King, “Symbolic execution and program testing,” in Communica-         [26] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin,
     tions of the ACM, vol. 19, no. 7, 1976, pp. 385–394.                             C. Zhang, S. Agarwal, K. Slama, A. Ray et al., “Training language
[12] M. D. Ernst, J. Cockrell, W. G. Griswold, and D. Notkin, “Dynamically            models to follow instructions with human feedback,” in Advances in
     discovering likely program invariants to support program evolution,”             Neural Information Processing Systems, 2022, pp. 27 730–27 744.
     IEEE Transactions on Software Engineering, vol. 27, no. 2, pp. 99–123,
     2001.                                                                       [27] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V.
[13] C. Flanagan and K. R. M. Leino, “Houdini, an annotation assistant                Le, and D. Zhou, “Chain-of-thought prompting elicits reasoning in
     for esc/java,” in Proceedings of the International Symposium of Formal           large language models,” in Advances in Neural Information Processing
     Methods Europe, 2001, pp. 500–517.                                               Systems, 2022, pp. 24 824–24 837.
[14] P. Tolmach, Y. Li, S.-W. Lin, Y. Liu, and Z. Li, “A                         [28] X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang,
     survey of smart contract formal specification and verification,”                 A. Chowdhery, and D. Zhou, “Self-consistency improves chain of
     arXiv preprint arXiv:2008.02712, 2020. [Online]. Available:                      thought reasoning in language models,” in Proceedings of the Inter-
     https://arxiv.org/abs/2008.02712                                                 national Conference on Learning Representations, 2023.
