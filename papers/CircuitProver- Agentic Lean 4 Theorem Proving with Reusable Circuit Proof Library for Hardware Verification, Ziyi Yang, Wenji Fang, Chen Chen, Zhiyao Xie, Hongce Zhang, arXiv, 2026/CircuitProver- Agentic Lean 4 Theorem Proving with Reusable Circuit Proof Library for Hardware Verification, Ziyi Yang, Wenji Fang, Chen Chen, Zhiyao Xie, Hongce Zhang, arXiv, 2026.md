                                                          CircuitProver: Agentic Lean 4 Theorem Proving with Reusable
                                                                 Circuit Proof Library for Hardware Verification
                                                              Ziyi Yang1∗ , Wenji Fang2∗ , Chen Chen1 , Zhiyao Xie2 , Hongce Zhang1,2†
                                                                             1
                                                                                 Hong Kong University of Science and Technology(Guangzhou)
                                                                                     2
                                                                                       Hong Kong University of Science and Technology



                                                                      Abstract                                    Input        Natural Language                            Parameterized Hardware
                                                                                                                                 Specification               Goal:             Implementation
                                           Modern integrated circuits (ICs) are becoming increasingly                                   A counter               ?
                                                                                                                                     increases every       Spec ≡ Impl              Module
                                           complex, making functional verification a major bottleneck.
                                                                                                                                    cycle, and reset …                    in     (parameter n)     out
                                           The dominant hardware formal verification methodology,
                                           model checking, verifies each design instance separately and                    Existing Method:                              Proposed CircuitProver:
                                           exposes only pass/fail results, so the reasoning behind a proof             Hardware Model Checking                      Agentic Hardware Theroem Proving
                                           stays locked inside solver heuristics and is repeatedly recon-                                                            1. Formalizing Hardware as Lean
                                                                                                                                           …
arXiv:2607.27259v1 [cs.LO] 29 Jul 2026




                                           structed across related designs. Interactive theorem proving            n=8         n = 16               n=x
                                                                                                                                                                         (Symbolic parameter: n)
                                           instead yields explicit, reusable proof artifacts, but applying it
                                           to hardware remains largely manual, demanding expert effort             1. Formalization (e.g., AIGER, BTOR)
                                                                                                                                                                       2. Agentic Theorem Proving
                                           for formalization, invariant discovery, and proof development.
                                           In this paper, we present CircuitProver, an agentic Lean 4-             2. Model Checker (e.g., BMC, PDR)                     Theorem (Parameterized
                                           based verification framework supporting proof-accumulation                                                                         Correctness)
                                           and parameterized verification. CircuitProver automatically                                                                      ∀ n, Spec ≡ Impl
                                                                                                                   Pass         Pass       …        Pass
                                           translates parameterized hardware designs and their natural
                                                                                                                                                                       3. Reusable Proof Knowledge
                                           language specifications into executable Lean 4 models. It then
                                           iteratively constructs machine-checked proofs through Lean                Verify each instance separately                   Directly verify all parameters
                                           feedback to establish that the hardware code complies with                      No knowledge reuse                           Reusable proof knowledge
                                           the specification. The proving traces and verified theorems
                                           are distilled into reusable libraries, where proving strategies      Figure 1: Comparison between existing model checking and
                                           guide future agent reasoning and verified lemmas support             our CircuitProver for parameterized hardware verification.
                                           formal proof reuse across related hardware verification tasks.       CircuitProver proves parameterized correctness in Lean 4
                                           We further introduce the first benchmark suite for evaluating        and accumulates reusable proof knowledge, while traditional
                                           agentic hardware theorem proving, covering diverse parame-           model checking verifies instantiated designs independently.
                                           terized hardware designs, specifications, proof tasks, and eval-
                                           uation metrics. Across 63 tasks, CircuitProver successfully
                                           proves all benchmarks, while a vanilla agent solves 92.1% of
                                           them and requires twice as many proof rounds on average.             with autonomous design agents emerging as a promising
                                           Ablation studies show that accumulated proof knowledge re-           paradigm for improving productivity. As autonomous agents
                                           duces redundant proof construction across related verification       begin to participate in hardware generation (Yu et al.
                                           tasks, reducing proof length by 16.3% and verification time          2026), optimization (Fang et al. 2026), and debugging (Bai
                                           by 23.2%. These results show that reusable proof knowledge           et al. 2025), automated verification becomes increasingly
                                           can significantly reduce redundant proof efforts on related          important for validating their outputs and providing reliable
                                           verification tasks.                                                  feedback. However, ensuring functional correctness remains
                                                                                                                a major bottleneck (Yang et al. 2026). While simulation
                                                                                                                can detect many bugs, it cannot exhaustively cover all
                                                                  Introduction                                  possible execution behaviors, making formal verification
                                         The rapid growth of artificial intelligence is creating                indispensable for modern hardware development.
                                         unprecedented demand for new integrated circuits (ICs).                   Existing verification tools provide automation but lack
                                         To meet this demand, hardware designers need to develop                reusable knowledge. Model checking (Clarke, Emerson, and
                                         increasingly complex designs within ever shorter devel-                Sifakis 2009; Eén, Mishchenko, and Brayton 2011; Biere
                                         opment cycles. Modern IC design therefore increasingly                 et al. 2009; Mann et al. 2021) has become the dominant
                                         relies on reusable IPs and AI-assisted methodologies,                  industrial formal verification methodology. As shown in Fig-
                                           ∗                                                                    ure 1, it translates hardware designs into solver-friendly
                                               These authors contributed equally.
                                           †                                                                    transition-system representations, such as AIGER (Brum-
                                               Corresponding author.
                                                                                                                mayer et al. 2007), BTOR (Niemetz et al. 2018), or SMT-
LIB (Cok et al. 2011), and automatically proves properties        constructs general correctness theorems over symbolic de-
or generates counterexamples. This makes model checking           sign parameters, enabling a single proof to establish correct-
highly effective for RTL property checking and bug find-          ness for an entire family of hardware instances.
ing. However, the reasoning behind correctness decisions is          We summarize the contributions of this work as follows:
largely hidden inside the verification engine and exposed          • Agent-native hardware verification. We present Cir-
mainly through final pass/fail results or counterexamples.           cuitProver, a Lean 4-based framework that integrates
Consequently, verification knowledge is rarely captured as           hardware auto-formalization, agentic theorem proving,
explicit and reusable artifacts, requiring similar reasoning to      and reusable proof libraries for automated hardware the-
be reconstructed across related verification tasks.                  orem proving.
   Interactive theorem proving provides reusable hard-
                                                                   • Hardware auto-formalization. We develop an automatic
ware knowledge but lacks automation. Beyond automated
                                                                     formalization pipeline that translates hardware imple-
model checking, interactive theorem proving explicitly rep-
                                                                     mentations and specifications into a unified Lean 4 rep-
resents verification reasoning as machine-checked formal ar-
                                                                     resentation with machine-checkable semantics.
tifacts. Existing frameworks such as Kami (Choi et al. 2017)
and Coquet (Braibant 2011) in Coq/Rocq, together with              • Agentic hardware theorem proving. We propose an
ACL2- (Kaufmann and Moore 1997) and HOL-based (Gor-                  interactive theorem-proving workflow where reasoning
don 1988) systems, have demonstrated this approach for               agents iteratively construct and repair proofs through
arithmetic circuits, processors, and parameterized hardware          feedback from the theorem prover.
designs. These artifacts provide strong correctness guaran-        • Reusable proof library. We build a reusable proof li-
tees and can be composed and reused across related verifi-           brary that distills proof traces into natural-language proof
cation tasks. However, current frameworks still rely heavily         strategies and their corresponding formal artifacts, en-
on experts for hardware formalization, specification devel-          abling proof reuse across related verification tasks.
opment, invariant discovery, and proof construction.               • Benchmark and evaluation. We introduce a benchmark
   What should new hardware verification tools look like             suite for agentic hardware theorem proving and demon-
in the agent era? In the agent era, verification tools should        strate the effectiveness of CircuitProver and the benefits
not only check correctness, but also preserve and accumu-            of reusable proof knowledge.
late explicit proof artifacts and reasoning strategies for fu-
ture agent reasoning. We refer to this paradigm as proof-                               Preliminaries
accumulating hardware verification. In this setting, suc-
cessful proofs are no longer treated as isolated and implicit     Theorem Proving for Hardware Verification
outputs. Instead, proof strategies, lemmas, and invariants        Hardware theorem proving verifies circuit correctness by en-
are distilled from proof trajectories, linked to their explicit   coding hardware implementations and their specifications in
machine-checked formal artifacts, and reused by agents in         an interactive theorem prover and establishing correctness
new verification tasks.                                           through machine-checked proofs. Early HOL-based verifi-
   CircuitProver: agentic hardware theorem proving with           cation systems (Gordon 1988) demonstrated mechanically
reusable proof libraries. To this end, we present Circuit-        verified hardware using higher-order logic, while ACL2-
Prover, an agent-native hardware verification framework           based approaches (Kaufmann and Moore 1997) explored
built upon Lean 4. As shown in Figure 1, CircuitProver com-       automated theorem proving for hardware reasoning. More re-
bines hardware formalization, agentic theorem proving, and        cent Coq/Rocq-based frameworks, such as Coquet (Braibant
reusable proof knowledge accumulation. Through proof tra-         2011) and Kami (Choi et al. 2017), enabled embedded hard-
jectory distillation, the reasoning processes are transformed     ware modeling and refinement-based verification for param-
into reusable symbolic artifacts that guide future hardware       eterized designs. Despite different proof environments, these
agents. First, CircuitProver automatically formalizes hard-       frameworks share a common workflow of formalizing hard-
ware implementations and specifications into a unified Lean       ware behavior, specifying correctness properties, and prov-
representation for machine-checked reasoning. Second, the         ing corresponding theorems. However, proof development
reasoning agent iteratively constructs and repairs formal         still requires substantial human effort in formalization, in-
proofs through interaction with the theorem prover and            variant discovery, lemma construction, and proof guidance.
its feedback. Finally, proving traces and verified theorems
are distilled into reusable proof libraries, including natural-   Lean 4 and Reusable Proof Libraries
language proof strategies and their corresponding machine-        Lean 4 is a modern interactive theorem prover widely used
checked formal artifacts, and stored in a persistent proof        in mathematics, software verification, and AI-assisted the-
library for future verification tasks.                            orem proving (Moura and Ullrich 2021; Wu et al. 2022;
   We study parameterized hardware verification as a rep-         Azerbayev et al. 2023; Song, Yang, and Anandkumar 2024;
resentative task for this framework, where a single design        Xin et al. 2024; Wang et al. 2024; Li et al. 2024; Chen
generator describes a family of hardware instances with dif-      et al. 2025; Kumarappan et al. 2025; Ospanov, Farnia, and
ferent parameters. Existing formal verification methods, such     Mohit 2026). It provides expressive dependent types, pro-
as model checking, often verify individual instantiated de-       grammable proof automation, and a library-based ecosys-
signs and may repeatedly encounter similar reasoning pat-         tem; in particular, Mathlib (mathlib Community 2020)
terns across different configurations. CircuitProver instead      enables proofs to build upon reusable definitions, lemmas,
 Phase I. Transforming hardware                                      Phase II. Agentic Hardware Theorem Proving Workflow
         design to Lean 4                      2.1 Specification                   2.2 Proof Planning and                 2.3 Iterative Theorem
                                                Formalization                       Scaffold Construction                         Proving
   Hardware in Chisel (𝐷)
                                       Natural Language Spec (𝑆)                           Target Proof:
    class Counter(n: Int) extends
    Module {                                 For any width n > 0, the                      Spec vs. Impl                         Generate /
      require（ n > 0 ）                       counter increments every                          ℱplan                            Refine Proof
      val en = IO(Input(Bool()))             cycle and wraps around at
      val q = IO(Output(UInt(n.W)))
      val cnt = RegInit(0.U(n.W))            2n. When ‘reset’ is high,                                                                 ℱproof
      when (en) { cnt := cnt + 1.U }         the counter is reset to 0.              Comb.              Seq.
      q := cnt                                                                                                           Diagnosis &            Lean
    }                                                       ℱspec                                                         Feedback              Check
                                       Lean 4 Spec (𝐿𝑆 )                          1. single-step    1. single-step
     Chisel-to-Lean Parser (𝒯impl )     def counterSpec (p : Params)
                                            (rst en : Nat → Bool)                                    2. invariant
                                            (q : Nat → BitVec p.n) :
    Lean 4 Impl.      (𝐿𝐷 )             Prop := q 0 = 0 ∧
   structure Params where
      n: Nat
                                          ∀ t, q (t + 1) =                                                             accumulate
                                            if rst t then 0
      require: n > 0                        else if en t then q t + 1              How to Prove/Fix?                        Machine-Checked
   structure State (p: Params)
      where cnt : BitVec p.n
                                            else q t
                                                                                   Which Lemma to Use? reuse                Correctness Proof
   def init (p : Params) :
      State p := ⟨0⟩                                                                                                 theorem counter_correct {n : Nat} :
                                               Proof Guidance Library          Lean-Checked Theorem Library             ∀ t, (run n t).cnt = spec n t :=
   def step {p: Params}
      (en : Bool)(s:State p) :                                                                                          by induction t <;> simp [run,
                                         •      Reusable instructions      •    Bit-width operations & modulo           step, spec]
      State p := ⟨if en then s.cnt
      + 1 else s.cnt⟩                    •      Modular proof path         •    Datapath arithmetic
   def output {p: Params} (s :           •      Repeated behavior          •    State Transitions                    Phase III. Reusable Hardware
   State p): Bitvec p.n := s.cnt         •      Concrete repaire steps     •    Invariants & Composition
                                                                                                                              Proof Library

Figure 2: Workflow of CircuitProver for agentic hardware theorem proving. The framework translates hardware designs into
Lean 4 models, performs specification formulation, hardware-aware proof planning, and iterative theorem proving, and accu-
mulates reusable proof knowledge.


and automation. Recent LLM-based theorem proving frame-                         the XiangShan (Wang et al. 2025) and Rocket (Asanović
works, such as DeepSeek-Prover (Xin et al. 2024) and Lean-                      et al. 2016) multipliers and dividers—to examine behavior
Agent (Kumarappan et al. 2025), enable agents to interact                       on larger designs.
with Lean and synthesize proofs for formal statements. How-                        Proof tasks. Given the hardware design in code format
ever, they mainly target mathematical problems and do not                       and specification in natural language, the proof agent must
address hardware-specific reasoning, which requires circuit-                    construct a complete Lean 4 proof. The target theorem ex-
aware proof strategies for fixed-width operations, parameter-                   presses input-output equivalence for combinational designs
ized structures, and inductive invariants over clocked state                    or state-transition and invariant properties for sequential de-
transitions. Recent work such as CktFormalizer (Xiong et al.                    signs. A task is solved only when the final Lean file compiles
2026) explores Lean-based hardware formalization by gen-                        and contains no sorry, admit, axiom, or unsafe.
erating type-checkable circuit representations, while auto-                        Evaluation metrics. The benchmark evaluates hardware
mated proof construction and reusable hardware proof li-                        theorem-proving systems along four dimensions. Proof suc-
braries remain largely unexplored.                                              cess is measured by the number and percentage of tasks
                                                                                solved under the acceptance criterion above. End-to-end ef-
   A Benchmark Suite for Agentic Hardware                                       ficiency is measured by wall-clock verification time and, for
             Theorem Proving                                                    agentic systems, output tokens and effective proof rounds.
                                                                                Proof LoC measures the size and auditability of the resulting
Before introduing the whole framework, we first introduce                       machine-checked proof artifact, while Chisel and specifica-
a new benchmark suite for evaluating agentic theorem prov-                      tion LoC characterize the scale of each task. Cost metrics are
ing on hardware verification. This benchmark is designed to                     averaged over the tasks successfully solved by each system,
evaluate whether a theorem-proving workflow can construct                       with solved-task counts reported alongside them to make
checked Lean 4 proofs, and reuse proof knowledge across                         differences in proof success explicit.
related verification tasks. Although the current suite is based
on parameterized Chisel designs, its evaluation interface is
defined at the Lean level and is therefore independent of a
                                                                                                                Methodology
circuit’s source language or design style.                                      Overview of CircuitProver
   Benchmark data. The main benchmark contains 63 pa-                           Given a hardware design D and its specification S, Circuit-
rameterized Chisel verification tasks: 34 arithmetic, 9 con-                    Prover translates them into Lean 4 representations LD and
trol, 9 memory, and 11 miscellaneous. Each task contains the                    LS , and aims to prove a correctness theorem:
Chisel implementation, its generated Lean 4 model, a natural-
                                                                                                            ⊢Lean Φ(LD , LS ),                             (1)
language specification, and a theorem scaffold. The suite
covers bit-vector and modular arithmetic, combinational dat-                    where Φ specifies that the implementation satisfies the in-
apaths, state transitions, and multi-cycle invariants. We ad-                   tended behavior. The proof is constructed through auxiliary
ditionally isolate four processor-level arithmetic modules—                     lemmas, invariants, and intermediate theorems.
   As shown in Figure 2, CircuitProver consists of three com-     general theorem proving tasks, hardware verification re-
ponents. (1) Hardware formalization translates hardware im-       quires reasoning about parameterized designs, fixed-width
plementations into executable Lean 4 semantic models and          bit-vector semantics, and cycle-level state evolution. There-
formalizes specifications into Lean theorems. (2) A reason-       fore, CircuitProver develops a hardware-aware proving work-
ing agent iteratively constructs proofs by decomposing proof      flow that integrates circuit analysis, proof planning, and it-
goals, generating auxiliary lemmas and invariants, and re-        erative theorem proving with Lean 4 as the trusted proof
pairing proof scripts based on Lean feedback. (3) Successful      environment.
proof trajectories are distilled into reusable proof knowl-          As shown in Figure 2, the workflow consists of three
edge, including reasoning strategies and their corresponding      stages: (1) specification formulation and circuit analysis,
machine-checked artifacts, which are stored in a hardware         where the agent analyzes the hardware model and constructs
proof library for future verification tasks.                      the target correctness theorem; (2) hardware-aware proof
                                                                  planning and scaffold construction, where the agent identifies
Phase I: Transforming Hardware Design to Lean 4                   appropriate proof structures for different hardware properties
As shown in Figure 2, CircuitProver first translates the hard-    and generates auxiliary lemmas and invariants; and (3) iter-
ware implementation into an executable Lean 4 semantic            ative theorem proving, where the agent interacts with Lean
model, providing a fixed and machine-checkable representa-        feedback to complete and refine the formal proof.
tion for subsequent theorem proving. We represent a param-           Step 1: Specification formulation. Given the transformed
eterized hardware design as a transition system:                  Lean hardware model LD and its natural-language specifica-
                                                                  tion S, the reasoning agent analyzes the circuit structure and
                    D = (P, I, O, R, T ),                  (2)    formulates the corresponding Lean 4 specification LS . Un-
                                                                  like the deterministic hardware translation in Phase I, this step
where P denotes design parameters, I and O denote input
                                                                  requires semantic reasoning to interpret the natural-language
and output interfaces, R denotes the set of registers, and T
                                                                  requirements based on the hardware context. The agent ana-
defines the state transition behavior.
                                                                  lyzes design parameters, parameter constraints, register be-
  We develop a deterministic Chisel-to-Lean translator:
                                                                  havior, reset conditions, output dependencies, and cycle-level
                      Timpl : D → LD ,                     (3)    behaviors, while preserving parameters symbolically rather
                                                                  than instantiating fixed configurations.
where LD is an executable Lean 4 semantic model of the               The specification formulation process is defined as:
hardware implementation. The generated Lean model pre-
serves the original design parameters, IO interfaces, regis-                         Fspec : (LD , S) → LS ,                   (4)
ter states, and state transition behaviors, while representing
hardware operations using Lean 4 definitions.                     where LS consists of formal correctness properties extracted
   As shown in Figure 2, the translator extracts design pa-       from the natural-language specification. Specifically, LS
rameters, IO interfaces, registers, and state transitions from    contains a set of Lean 4 properties:
the source design and maps them into corresponding Lean 4                            LS = {ϕ1 , ϕ2 , . . . , ϕk },             (5)
definitions. Parameters are represented explicitly, while hard-
ware signals and registers are modeled using width-aware          where each ϕi represents a specific correctness requirement
bit-vector types. Hardware operations and expressions are         to be verified. We validate the formalized specifications using
translated into executable Lean 4 expressions with consis-        the same exhaustive small-bit-width co-simulation procedure
tent width semantics. Intermediate signals are represented        as in Phase I.
using let bindings, conditional logic is translated into if          Step 2: Proof planning and scaffold construction. Given
expressions, and register reads and updates are mapped to         the formalized hardware model LD and specification LS ,
explicit state accesses and updates in Lean 4.                    the agent first analyzes the verification task and constructs a
   After translation, we validate the generated models            hardware-aware proof scaffold. Instead of directly searching
through exhaustive small-bit-width co-simulation: for each        for tactics on the complete theorem, the agent decomposes the
configuration, we execute the Chisel design and its Lean 4        correctness proof into structured intermediate obligations,
counterpart over the complete test space and compare their        including auxiliary lemmas and invariants.
simulation results. The matching results confirm that the            The proof planning process is formulated as:
translation preserves the behavior of the original design for
the evaluated bit-width configurations, providing additional                         Fplan : (LD , LS ) → P,                   (6)
confidence in the generated Lean 4 models before they are         where P denotes the generated proof scaffold. The scaffold
used for formal reasoning.                                        construction depends on the hardware behavior:
                                                                     For combinational designs, which do not involve state
Phase II: Agentic Hardware Theorem Proving                        evolution across cycles, the agent focuses on proving the
Workflow                                                          correctness of the underlying computation within one cy-
After the hardware implementation is translated into a Lean 4     cle. The generated proof scaffold contains auxiliary lemmas
model, CircuitProver employs a hardware-oriented reason-          for arithmetic operations, bit-vector manipulations, Boolean
ing agent to construct a machine-checked correctness proof        logic, and symbolic parameter constraints required to estab-
between the implementation and its specification. Unlike          lish functional correctness.
                                                          Trajectory Collection                 reusable proof plan that explains how the proof is decom-
                                                        Detect Proof Bottleneck
                                                                                                posed, why particular lemmas are selected, and how the plan
                                                                                                is adapted in response to Lean feedback.
                 、                       Critical
                                                         Knowledge Distillation                    Lean-Checked Theorem Library. In contrast to the first
                                         bottleneck
                                                           Library Construction
                                                                                                library, this one preserves the results established along the
    Proof task                     Final proof
                                                                                                trajectory. Before a theorem is added to the library, Circuit-
    Lean-Checked Theorem Library                      Proof Guidance library                    Prover decouples it from its originating module by removing
 Theorem                                      Proof                                             module-specific definitions, signal names, and incidental as-
     𝑠𝑘 = 𝐴𝑘 + 𝐵𝑘 + 𝑐𝑘 mod 2𝑏                 RTL signature: the fold writes carries[block+1]
               𝐴𝑘 + 𝐵𝑘 + 𝑐𝑘                   & sums[block] from carries[block], and the next   sumptions, and reformulating its reusable core over symbolic
        𝑐𝑘+1 =                                block reads that carry
                                                                                                parameters and generic interfaces. The resulting theorem is
   𝑛−1              2𝑏                        Route: Recover carries from generator state and
                                              close the block recurrence in one step.
⟹ ෍ 𝑠𝑘 2𝑏𝑘 + 𝑐𝑛 2𝑤 = 𝐴 + 𝐵 + 𝑐0                                                                 therefore not tied to the module from which it was extracted
                                              Debug
   𝑘=0                                        Hardware symptom: motive is not type correct      and can be instantiated in other modules that exhibit the
    one-step closure for sum and carry        Fix: dsimp only [] → expose getD/toNat → rw
                                                                                                same underlying hardware semantics or structural pattern.
 Cross-Module reuse                                                                                A concrete example. Figure 3 illustrates this two-library
 REUSED LoC: 370 → 254 (-31%) agent rounds : 13 → 6 (-54%)                                      organization with concrete entries distilled from the proof
 Generalized Carry-Select Adder Booth Radix-4 Multiplier Wallace Multiplier                     of a carry-skip adder. The Lean-Checked Theorem Library
                                                                                                stores a module-independent closure theorem that lifts the
Figure 3: Proof knowledge accumulation in CircuitProver.                                        block-local sum-and-carry relation to the full-width correct-
Proof trajectories are distilled into proof guidance and                                        ness result. The corresponding Proof Guidance Library entry
reusable theorem libraries to accelerate future hardware ver-                                   records when and how to reuse this theorem: it identifies an
ification tasks.                                                                                RTL generator fold in which each iteration produces a carry
                                                                                                consumed by the next iteration, and instructs the agent to
                                                                                                recover the carry sequence and apply the closure theorem in-
   For sequential designs, the agent focuses on proving tem-                                    stead of unfolding the generator step by step. The entry also
poral correctness by reasoning about state evolution over                                       abstracts the successful fix into a reusable repair principle for
time. Instead of directly proving the complete execution be-                                    representation-level proof failures: when hidden implemen-
havior, the agent first constructs local one-step transition                                    tation definitions prevent a rewrite from matching the proof
proofs and then discovers the inductive invariants to connect                                   goal, the agent exposes only the relevant representation con-
step-wise correctness with global behavioral correctness.                                       versions before applying a targeted rewrite.
   This hardware-aware planning provides structured guid-                                          Together, the two libraries provide both a reusable route
ance for subsequent proof construction instead of relying on                                    for constructing a proof and module-independent, machine-
direct low-level tactic search.                                                                 checked facts for completing it, allowing verified knowledge
   Step 3: Iterative theorem proving. Given the hardware                                        to transfer across hardware designs.
model LD , specification LS , and generated proof scaffold
P, the agent iteratively constructs the final proof through                                          Case Study: Proving Carry-Skip Adder
interaction with Lean 4. The proof construction process is                                      This section uses the carry-skip adder module proof as a
formulated as:                                                                                  case study. This module divides two w-bit operands into
                     Fproof : (LD , LS , P) → Π,                                          (7)   n = w/b blocks of b bits. Each block computes a widened
                                                                                                sum from its two operand slices and the incoming carry. A
where Π denotes the machine-checked proof accepted by the                                       block propagates the incoming carry when the bitwise XOR
Lean kernel.                                                                                    of its two operand slices is all ones. The proof path is detailed
   In each iteration, the agent updates the proof script, in-                                   in Figure 4.
vokes Lean, and analyzes the returned proof states and error
messages. All generated proof steps are checked by the Lean                                     Four-Phase Proof Strategy
kernel, ensuring that only formally verified proofs are ac-                                     Phase 1: Setup the proof. The target theorem states that
cepted. The agent uses Lean feedback together with the hard-                                    the circuit returns the low w bits and bit w of A + B + cin.
ware context to refine its reasoning. When a proof attempt                                      The generated Lean model processes blocks from low to
fails, the agent may revise the proof plan, introduce addi-                                     high with List.foldl, passing the carry and storing
tional lemmas, strengthen invariants, or adjust assumptions.                                    each block sum. The proof agent introduces local names for
This iterative process continues until all proof obligations                                    the generated block operation, fold step, and initial state to
are successfully discharged.                                                                    simplify the proof state.
                                                                                                   Phase 2: Prove block correctness. Define Ck as the carry
Phase III: Reusable Hardware Proof Library                                                      entering block k and sk as its low b-bit sum. For D = 2b ,
As shown in Phase III of Figure 2, CircuitProver accumulates                                    both paths of the skip multiplexer satisfy sk = (Ak + Bk +
proof trajectories into two complementary libraries:                                            Ck ) mod D and Ck+1 = ⌊(Ak + Bk + Ck )/D⌋. The non-
   Proof Guidance Library. It preserves the knowledge that                                      skip path obtains the quotient from the widened addition; on
would otherwise disappear once Lean accepts the final proof,                                    the skip path, the all-ones propagate condition gives Ak +
then transforms a successful interaction trajectory into a                                      Bk = D − 1, so forwarding Ck yields the same quotient.
                                                                   translation pipeline around this representation. CircuitProver
                                                                   is performed with Lean 4 v4.29.0. Our current prototype runs
                                                     Phase 1       the agent through the Claude Code command-line interface
                                               Setup the Proof
                                                                   (CLI), but the workflow itself is agent-CLI agnostic: the task
                                                                   specification and repair procedure are defined independently
                                                                   of the agent, and proof knowledge is provided through a
                                                     Phase 2
                                                                   reusable theorem library. All experiments are run on a server
                                        Prove Block Correctness    with Ubuntu 20.04.4 LTS, dual Intel Xeon Platinum 8375C
                                                                   processors, and 256GB RAM.

                                                                   Main Results: Proof-Generation Comparison
                                                     Phase 3       Table 1 compares the proof-generation efficiency and cost of
                                            Lift to Full Width
                                                                   CircuitProver with Chicala/Stainless and the vanilla agent.
                                                                   The vanilla agent is a matched baseline that uses the same
                                                                   language model, generated Lean model, specification, and
                                                                   theorem scaffold as CircuitProver, but does not have access
                                                                   to its reusable hardware theorem library or hardware-aware
                                                                   proof guidance.
                                                     Phase 4          Overall module proving results. Table 1(a) presents the
                                                                   main benchmark results across the four circuit categories.
                                     Establish Output Equality     The vanilla agent solves all miscellaneous tasks but misses
                                                                   cases in arithmetic, control, and memory, indicating limi-
 Figure 4: Detailed proof strategy for the carry-skip adder        tations in general proof search. Chicala/Stainless is limited
                                                                   earlier by front-end robustness: despite our repair of more
                                                                   than 20 implementation issues, many designs still fail during
   Phase 3: Full-width lifting. The proof agent applies a          compilation and therefore never reach Stainless verification.
fold read-back lemma to show that the final state stores Cn           Proof-generation efficiency results. Beyond improving
and every sk . It then applies the radix closure lemma to          proof success, CircuitProver turns proof generation from
compose the block recurrences into the packed low w bits           repeated trial-and-error search into a hardware-guided
and the final carry of A + B + cin. This step lifts the local      process that can reuse previously established lemmas and
block equations to the arithmetic value represented by the         proof strategies. Compared with the vanilla agent, it reduces
widened specification sum.                                         the average number of proof rounds by 50.0%, verification
   Phase 4: Establish output equality. The carry equation          time by 23.2%, and proof LoC by 16.3%. These reductions
identifies I.cout with S.cout, and a reverse-Horner lemma          indicate that the agent reaches checked proofs with fewer
rewrites the generated packing fold to identify the two sum        repair cycles and less redundant proof construction. Output
fields. Record extensionality then closes impl_eq_spec.            tokens decrease more modestly, from 66.0K to 61.7K, and
                                                                   increase for arithmetic because CircuitProver solves three
Reusable Library Knowledge                                         additional difficult arithmetic tasks; the token averages
The completed proof yields three reusable insights. First,         therefore cover different sets of solved tasks. Overall, the
when every bit in a block satisfies Ai ⊕ Bi = 1, the two           results support the central premise of proof-accumulating
operand slices sum to 2b − 1. The outgoing carry therefore         verification: reusable hardware knowledge improves both
equals the incoming carry, which justifies the carry-skip path.    proof success and proof-search efficiency.
Second, the fold accumulator records the carries C0 , . . . , Cn      Processor-level module proving results. Table 1(b) fur-
and block sums s. Third, the radix-2b equations combine            ther suggests that these benefits grow with design complex-
these block-level facts into the full-width sum and carry. The     ity. With identical coverage on the four processor-level mod-
library stores these insights as a reusable proof pattern. For     ules, CircuitProver reduces aggregate verification time, proof
another blocked adder, the agent only needs to re-establish        LoC, output tokens, and proof rounds by 56.8%, 54.4%,
the one-block semantics; the remaining steps can be reused.        55.9%, and 48.2%, respectively, relative to the vanilla agent,
                                                                   and reduces aggregate proof LoC by 57.8% relative to Chi-
                                                                   cala/Stainless. The pronounced reductions on these larger
                       Experiment                                  designs indicate that hardware-aware proof decomposition
Experiment Setup                                                   and reusable proof knowledge become increasingly valuable
We evaluate CircuitProver on the proposed benchmark suite          as it becomes more expensive to rediscover invariants and
through three studies: comparisons with Chicala (Feng et al.       auxiliary lemmas and to repair proofs.
2024) and a matched vanilla agent, component ablations,
and language-model scaling. Our translator currently sup-          Ablation Study
ports a subset of Chisel that covers the common language           To isolate the contributions of the reusable theorem library
constructs. The frontend adapts the typed-AST translation          and hardware-aware proof guidance, we conduct a controlled
pipeline introduced by Chicala and builds a new parsing and        2 × 2 ablation over the same 63 tasks. All four configurations
 Table 1: Proof-generation comparison on the full benchmark and processor-level arithmetic modules. Cost metrics are averaged
 over successfully solved tasks; time is reported in seconds and output tokens in thousands.

                                                    Design LoC            Chicala/Stainless‡                        Vanilla agent                         CircuitProver (Ours)
 Category (N)                                      Chisel Spec Solved Time                  LoC Solved            Time    LoC       Tok. Rnd. Solved        Time   LoC     Tok. Rnd.
 (a) Full benchmark; four top-level categories
 Arithmetic (34)        50.2 32.6 15/34                                            37.2     30.6     31/34        894.8 217.7       70.3   13.0   34/34    654.7 184.1     97.8      5.7
 Control (9)            45.0 63.3         7/9                                      22.9      6.4       8/9        522.9 63.9        53.2    8.9     9/9    410.7 28.8      22.8      4.3
 Memory (9)             36.2 49.4         3/9                                      58.6      8.3       8/9        343.3 15.9        95.0    6.9     9/9    302.2 12.6      48.7      2.9
 Miscellaneous (11)     27.3 27.8        6/11                                      16.8     13.2     11/11         63.8   8.5       30.6    3.1   11/11     53.7   7.8     10.1      2.4
 Summary (63)           43.4 38.6 31/63                                            32.1     21.3     58/63        658.9 129.8       66.0    9.2   63/63    506.2 108.6     61.7      4.6
 (b) Processor-level arithmetic modules
 xiangshan_mul            377 146                                            1/1     –♢ 1675               1/1   1981.3    448 278.8         9      1/1 1368.0      359   231.9      13
 xiangshan_div             73 110                                            1/1     –♢ 484                1/1   2341.1    695 310.3        40      1/1 251.6       456   236.5      16
 rocket_mul               120    46                                          1/1     –♢ 507                1/1   5264.1    616 1334.9       54      1/1 2968.0      315   252.5      45
 rocket_div               129    63                                          1/1     –♢ 451                1/1   6685.3   1126 452.6       223      1/1 2436.7      185   327.3      95
            ‡ Many designs still fail during Chicala compilation.
         ♢
              Requires substantial manual effort; the exact time cannot be reliably quantified.



                                     100                                                                            Table 2: Comparison of CircuitProver with different Claude
                                                                                                                    models on the benchmark.
Proof rate (% of benchmark proved)




                                      80                                                                              Model         Solved ↑ Time (s) ↓ LoC ↓ Tok. (K) ↓ Rnd. ↓
                                                                         58/63 = 92.1% @ 39 rounds
                                                                                                                      Haiku 4.5       31/63       845.2    174.3      301.5       17.5
                                      60                        60/63 = 95.2% @ 35 rounds                             Sonnet 4.6      47/63       834.5    139.0      480.4       11.5
                                                                                                                      Sonnet 5        60/63       642.1    113.4       88.9       11.7
                                                    63/63 = 100.0% @ 29 rounds                                        Opus 4.8        63/63       506.2    108.6       61.7        4.6
                                      40
                                                    63/63 = 100.0% @ 18 rounds
                                                                w/o proof guidance lib + w/o theorem lib
                                      20                        w/o proof guidance lib                              shortens the search needed to exploit them; their combina-
                                                                w/o theorem lib                                     tion achieves both full coverage and the fastest convergence.
                                                                CircuitProver(Ours)
                                       0
                                           0   5   10     15        20        25      30      35       40           Scaling with LLM Capability
                                                               Proof round
                                                                                                                    To assess sensitivity to language-model capability, we eval-
 Figure 5: Ablation study of CircuitProver, evaluating the im-                                                      uate CircuitProver with four Claude models under the same
 pact of proof guidance and Lean-checked theorem libraries.                                                         benchmark and workflow. Table 2 shows that proof coverage
                                                                                                                    rises from 31/63 with Haiku 4.5 to 47/63 with Sonnet 4.6,
                                                                                                                    60/63 with Sonnet 5, and 63/63 with Opus 4.8. Opus is the
 use the same language model, Lean model, specification, and                                                        only model to solve every task and also has the lowest average
 theorem scaffold. Figure 5 reports the cumulative number                                                           time, proof LoC, token usage, and proof rounds. Although
 of solved tasks under a 40-round budget, with each round                                                           these cost averages cover different solved-task subsets, the
 corresponding to one Lean compilation.                                                                             results show that stronger models improve proof coverage
    The 2 × 2 ablation exposes distinct roles for the two com-                                                      and, at the high end, proof-search efficiency.
 ponents. Holding guidance fixed, adding the library raises
 within-budget coverage from 60 to 63 tasks; without guid-                                                                                    Conclusion
 ance, the gain increases from 58 to 63. The library therefore                                                      This paper presented CircuitProver, an agentic Lean 4 frame-
 improves within-budget reachability rather than merely shift-                                                      work for proof-accumulating verification of parameterized
 ing the same solutions earlier. Holding the library fixed in-                                                      Chisel designs. Experiments demonstrate that CircuitProver
 stead, guidance advances the number of solved tasks at round                                                       is effective and efficient across diverse hardware verification
 10 from 53 to 56 and reduces the rounds required for full cov-                                                     tasks. Ablations show that reusable lemmas help solve
 erage from 29 to 18. The same acceleration appears without                                                         difficult cases, while hardware-aware guidance accelerates
 the library, where guidance increases the round-10 result                                                          search. These results show that proof accumulation benefits
 from 43 to 50 tasks, although neither configuration reaches                                                        hardware theorem proving. Future work will extend support
 full coverage. These paired contrasts show that reusable lem-                                                      to broader RTL constructs, richer properties, and industrial
 mas close difficult cases, while hardware-aware guidance                                                           designs.
                        References                                 Kumarappan, A.; Tiwari, M.; Song, P.; George, R. J.; Xiao,
Asanović, K.; Avizienis, R.; Bachrach, J.; Beamer, S.; Bian-       C.; et al. 2025. Leanagent: Lifelong learning for formal
colin, D.; Celio, C.; Cook, H.; Dabbelt, D.; Hauser, J.;           theorem proving. In International Conference on Learning
Izraelevitz, A.; et al. 2016. The rocket chip generator.           Representations, volume 2025, 73525–73564.
Azerbayev, Z.; Schoelkopf, H.; Paster, K.; Santos, M. D.;          Li, Y.; Du, D.; Song, L.; Li, C.; Wang, W.; Yang, T.; and
McAleer, S.; Jiang, A. Q.; Deng, J.; Biderman, S.; and             Mi, H. 2024. Hunyuanprover: A scalable data synthesis
Welleck, S. 2023. Llemma: An open language model for               framework and guided tree search for automated theorem
mathematics. arXiv preprint arXiv:2310.10631.                      proving. arXiv preprint arXiv:2412.20735.
Bai, Y.; Hamad, G. B.; Ho, C.-T.; Suhaib, S.; and Ren, H.          Mann, M.; Irfan, A.; Lonsing, F.; Yang, Y.; Zhang, H.;
2025. FVDebug: An LLM-Driven Debugging Assistant for               Brown, K.; Gupta, A.; and Barrett, C. 2021. Pono: a flex-
Automated Root Cause Analysis of Formal Verification Fail-         ible and extensible SMT-based model checker. In Interna-
ures. arXiv preprint arXiv:2510.15906.                             tional Conference on Computer Aided Verification, 461–474.
                                                                   Springer.
Biere, A.; Cimatti, A.; Clarke, E. M.; Strichman, O.; and
                                                                   mathlib Community, T. 2020. The lean mathematical library.
Zhu, Y. 2009. Bounded model checking. Handbook of sat-
                                                                   In Proceedings of the 9th ACM SIGPLAN International Con-
isfiability, 185(99): 457–481.
                                                                   ference on Certified Programs and Proofs. ACM.
Braibant, T. 2011. Coquet: a coq library for verifying hard-
                                                                   Moura, L. d.; and Ullrich, S. 2021. The lean 4 theorem prover
ware. In International Conference on Certified Programs
                                                                   and programming language. In International Conference on
and Proofs, 330–345. Springer.
                                                                   Automated Deduction, 625–635. Springer.
Brummayer, R.; Cimatti, A.; Claessen, K.; Een, N.; Herb-           Niemetz, A.; Preiner, M.; Wolf, C.; and Biere, A. 2018.
stritt, M.; Kim, H.; Jussila, T.; McMillan, K.; Mishchenko,        Btor2, btormc and boolector 3.0. In International Conference
A.; Somenzi, F.; et al. 2007. The aiger and-inverter graph         on Computer Aided Verification, 587–595. Springer.
(aig) format version 20070427. The AIGER And-Inverter
Graph (AIG) Format Version, 20070427.                              Ospanov, A.; Farnia, F.; and Mohit, R. 2026. Apollo: Auto-
                                                                   mated llm and lean collaboration for advanced formal rea-
Chen, T.; Lu, S.; Lu, S.; Gong, Y.; Yang, C.; Li, X.; Misu, M.     soning. Advances in Neural Information Processing Systems,
R. H.; Yu, H.; Duan, N.; Cheng, P.; et al. 2025. Automated         38: 41599–41633.
proof generation for rust code via self-evolution. In Inter-
                                                                   Song, P.; Yang, K.; and Anandkumar, A. 2024. Towards
national Conference on Learning Representations, volume
                                                                   large language models as copilots for theorem proving in
2025, 71891–71918.
                                                                   lean. arXiv preprint arXiv:2404.12534.
Choi, J.; Vijayaraghavan, M.; Sherman, B.; Chlipala, A.; and       Wang, H.; Xin, H.; Zheng, C.; Liu, Z.; Cao, Q.; Huang, Y.;
Arvind. 2017. Kami: a platform for high-level parametric           Xiong, J.; Shi, H.; Xie, E.; Yin, J.; et al. 2024. Lego-prover:
hardware specification and its modular verification. Pro-          Neural theorem proving with growing libraries. In Inter-
ceedings of the ACM on Programming Languages, 1(ICFP):             national Conference on Learning Representations, volume
1–30.                                                              2024, 31566–31597.
Clarke, E. M.; Emerson, E. A.; and Sifakis, J. 2009. Model         Wang, K.; Chen, J.; Xu, Y.; Yu, Z.; He, W.; Tang, D.; Sun,
checking: algorithmic verification and debugging. Commu-           N.; and Bao, Y. 2025. XiangShan: An open-source project
nications of the ACM, 52(11): 74–84.                               for high-performance RISC-V processors meeting industrial-
Cok, D. R.; et al. 2011. The smt-libv2 language and tools: A       grade standards. IEEE Micro.
tutorial. Language c, 2010–2011.                                   Wu, Y.; Jiang, A. Q.; Li, W.; Rabe, M.; Staats, C.; Jamnik, M.;
Eén, N.; Mishchenko, A.; and Brayton, R. 2011. Efficient           and Szegedy, C. 2022. Autoformalization with large language
implementation of property directed reachability. In 2011          models. Advances in neural information processing systems,
Formal Methods in Computer-Aided Design (FMCAD), 125–              35: 32353–32368.
134. IEEE.                                                         Xin, H.; Guo, D.; Shao, Z.; Ren, Z.; Zhu, Q.; Liu, B.; Ruan,
Fang, W.; Lu, Y.; Liu, S.; Wang, J.; Guo, Z.; He, J.; Tu, F.;      C.; Li, W.; and Liang, X. 2024. Deepseek-prover: Advancing
and Xie, Z. 2026. Dr. RTL: Autonomous Agentic RTL Opti-            theorem proving in llms through large-scale synthetic data.
mization through Tool-Grounded Self-Improvement. arXiv             arXiv preprint arXiv:2405.14333.
preprint arXiv:2604.14989.                                         Xiong, J.; Han, Q.; Ding, C.; Xiao, H.; Su, Z.; Tao, C.; and
Feng, W.; Liu, Y.; Liu, J.; Jansen, D. N.; Zhang, L.; and Wu, Z.   Wong, N. 2026. CktFormalizer: Autoformalization of Nat-
2024. Formally Verifying Arithmetic Chisel Designs for All         ural Language into Circuit Representations. arXiv preprint
Bit Widths at Once. In Proceedings of the 61st ACM/IEEE            arXiv:2605.07782.
Design Automation Conference, 1–6.                                 Yang, Z.; Hu, G.; Zhou, X.; Miao, M.; Yu, C.; Zhang, W.; and
Gordon, M. J. 1988. HOL: A proof generating system for             Zhang, H. 2026. FORWORD: Accelerating Formal Datap-
higher-order logic. In VLSI specification, verification and        ath Verification via Word-Level Sweeping. In 2026 Design,
synthesis, 73–128. Springer.                                       Automation & Test in Europe Conference (DATE).
Kaufmann, M.; and Moore, J. S. 1997. An industrial strength        Yu, C.; Deng, C.; Pinckney, N.; and Khailany, B. 2026. Agen-
theorem prover for a logic based on Common Lisp. IEEE              tic Hardware Design as Repository-Level Code Evolution.
Transactions on Software Engineering, 23(04): 203–213.             arXiv preprint arXiv:2606.28279.
