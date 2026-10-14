                                        AccelSync: Verifying Synchronization Coverage in
                                        Accelerator Pipeline Programs
                                        HANGCHENG AN, Beihang University, China
                                        RUI WANG, Beihang University, China
                                        DEPEI QIAN, Beihang University, China
                                        AI accelerator operators are compiled into multi-stage pipeline programs where DMA, vector, matrix, and
                                        scalar units execute concurrently on shared on-chip buffers. A missing or misplaced synchronization primitive
arXiv:2605.07881v1 [cs.AR] 8 May 2026




                                        introduces hardware-visible data races that escape both simulation and golden testing, because neither models
                                        the accelerator’s cross-unit visibility semantics. We formalize accelerator pipeline programs as a restricted
                                        concurrent language, define a parameterized hardware event semantics with three ordering relations—program
                                        order, synchronization order, and barrier order—and reduce the correctness question to barrier sufficiency—
                                        equivalently, synchronization coverage—whether every cross-unit write-read pair on the same buffer is ordered
                                        by happens-before. Here “barrier” denotes an abstract ordering primitive in the model, covering vendor
                                        pipe barriers, hard-event synchronization, and equivalent frontend-normalized synchronization points. We
                                        prove that synchronization coverage is decidable in 𝑂 (|𝐸| 2 ) time and that our checker is both sound and
                                        complete under the modeled semantics. We implement AccelSync, a static verification tool instantiated for
                                        Ascend 910B2 and Cambricon MLU370 by changing only the hardware model. On 6,292 production kernels
                                        from the CANN operator library, AccelSync identifies 3 previously unknown synchronization hazards—one
                                        matching a hazard class for which we observed nondeterministic outputs on Ascend 910B2 under a specific
                                        toolkit/driver configuration (CANN 8.0.RC3), though this observation was not reproducible after a subsequent
                                        driver upgrade—and on 120 LLM-generated kernels it flags a 19.2% defect rate (95% CI: [13.0%, 27.4%]). A
                                        mutation study on 688 non-equivalent mutants yields 100% detection, and a head-to-head comparison shows
                                        AccelSync detects hazards that Huawei’s runtime sanitizer msSanitizer misses, at 400× lower cost per kernel.
                                        Additional Key Words and Phrases: accelerator verification, synchronization, happens-before, Ascend C, static
                                        analysis

                                        1   Introduction
                                        Modern AI accelerators—including Google TPUs [25], Graphcore IPUs [24], Huawei Ascend
                                        NPUs [21], and Cambricon MLUs [7]—organize operator execution as multi-stage pipelines where
                                        DMA engines, vector processing units, matrix engines, and scalar cores operate concurrently on
                                        shared on-chip buffers. Operator compilers such as Triton [44], TVM [11], Halide [40], AKG [46],
                                        and vendor-specific toolchains (Ascend C, BANG C) translate high-level tensor programs into this
                                        pipeline code. The translation may preserve functional correctness while still violating hardware
                                        synchronization requirements: a producer unit writes a buffer, a consumer unit reads it, and the re-
                                        quired synchronization coverage is missing. These hazards are hard to catch because x86 simulation
                                        and golden testing do not model the accelerator’s cross-unit visibility rules [3, 22].
                                          Existing verification approaches leave this gap largely unaddressed. GPU verification tools
                                        such as GPUVerify [6], WEFT [4], and GKLEE [30] target flat warp-level synchronization with
                                        __syncthreads and named barriers—a fundamentally different concurrency model from hierarchi-
                                        cal operator pipelines where distinct hardware units communicate through queues, pipe drains,
                                        and hard-event synchronization. Hardware memory model formalizations [1, 35, 45] reason about
                                        instruction-level ordering on CPUs and GPUs but do not address operator-level pipeline syn-
                                        chronization. LLM-based verification frameworks such as ProofWright [10] and FM-Agent [15]
                                        reason about sequential program semantics without awareness of implicit hardware visibility
                                        requirements. Dynamic race detectors [17, 42, 43] and vendor sanitizers [22, 38] require runtime

                                        Corresponding author: Rui Wang, wangrui@buaa.edu.cn.
2                                               An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


instrumentation and hardware access, limiting their applicability to large-scale static audits. As a
result, synchronization hazards in accelerator pipelines often remain invisible until they manifest
on real devices.
   This paper studies a narrower but practically important problem: is the synchronization present in
a structured accelerator kernel sufficient for the hardware on which it will run? We answer this question
with AccelSync, a lightweight static checker for structured accelerator pipelines. AccelSync extracts
memory events from a kernel, instantiates a parameterized hardware model describing execution
units and synchronization primitives, builds a happens-before graph following the event-based
reasoning style of Lamport [26] and Alglave et al. [1], and reports write-read pairs not covered by
the available synchronization.
   The key insight is that accelerator operator pipelines occupy a structured fragment of concurrent
programs—fixed stages, queue-mediated communication, and a small set of hardware synchro-
nization primitives—that makes synchronization-coverage checking decidable and efficient. We
formalize this class of accelerator pipeline programs and prove that barrier sufficiency—the for-
mal criterion underlying synchronization coverage—is decidable in 𝑂 (|𝐸| 2 ) with soundness and
completeness under the modeled hardware event semantics. In our model, “barrier” is an abstract
ordering primitive: on Ascend C it can represent pipe barriers, SetFlag/WaitFlag hard-event
synchronization, or equivalent frontend-normalized synchronization points. AccelSync exploits
this structure to establish a cross-layer contract: the compiler-generated pipeline topology constrains
the concurrency, and the hardware visibility model constrains the synchronization requirements.
The checker verifies that the synchronization inserted by the compiler satisfies the requirements
imposed by the hardware. This cross-layer perspective distinguishes AccelSync from GPU verifi-
cation tools (which assume flat SIMT concurrency [4, 6, 14]), sequential verification frameworks
(which ignore hardware visibility [10, 15]), and abstract-interpretation-based analyzers (which
target different program properties [13, 36]).
   In summary, this paper makes the following contributions:

     • We identify synchronization coverage in structured accelerator pipelines as a distinct
       verification problem that is not captured by simulation testing, sequential verification, or
       prior GPU-oriented barrier checkers (§2).
     • We formalize accelerator pipeline programs as a restricted concurrent language, define
       hardware event semantics with three ordering relations (po, so, bo), and prove that bar-
       rier sufficiency (synchronization coverage) is decidable in 𝑂 (|𝐸| 2 ) with soundness and
       completeness under the modeled semantics (§3).
     • We implement AccelSync with three frontends (Ascend C source-level, Ascend C IR-level,
       and BANG C source-level) and parameterized hardware models for Ascend 910B2 and
       Cambricon MLU370 (§4).
     • We evaluate AccelSync on 6,412 Ascend C kernels across two code sources—6,292 production
       CANN kernels and 120 LLM-generated kernels—finding synchronization hazards in both,
       with risk rates ranging from 0.048% (production) to 19.2% (LLM-generated). On 688 injected
       mutations, AccelSync achieves 100% detection. A head-to-head comparison with Huawei’s
       msSanitizer shows AccelSync detects hazards that runtime instrumentation misses, at
       400× lower per-kernel cost. Hardware testing of a representative VPU→scalar hazard
       class on Ascend 910B2 (CANN 8.0.RC3) observed nondeterministic outputs consistent
       with the predicted failure mode, though this was not reproducible after a driver upgrade.
       Cross-hardware instantiation on Cambricon MLU370 audits 162 BANG C kernels in 393 ms,
       confirming portability via parameter substitution (§5).
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                                 3




Fig. 1. Ascend 910B2 pipeline architecture. Three stages communicate via FIFO queues (TQue). Within the
Compute stage, the MTE2 copy pipe, VPU, Cube, and Scalar units share the unified buffer but execute
independently; cross-unit visibility requires explicit synchronization coverage such as hard events, pipe drains,
or equivalent compiler-normalized primitives (red dashed lines). The MTE2→V edge denotes copy-pipe-to-
vector coverage for data copied into UB before vector consumption, not stage-level queue synchronization.



  The full CANN corpus verifies in under 48 seconds, and the largest single kernel (274 events)
verifies in 21 ms, confirming that static synchronization-coverage auditing is practical at production
scale.
  The rest of this paper is organized as follows. §2 introduces accelerator pipeline architecture and
motivates the problem with a concrete hazard example. §3 formalizes accelerator pipeline programs
and proves decidability, soundness, and completeness. §4 describes the implementation. §5 presents
the evaluation. §6 discusses related work, and §7 concludes.

2     Background and Motivation
We describe the pipeline architecture of AI accelerators, demonstrate how synchronization hazards
arise and evade testing, and position AccelSync relative to prior verification approaches.

2.1    Accelerator Pipeline Architecture
Modern AI accelerators organize operator execution as a multi-stage pipeline to overlap data
movement with computation. On Ascend 910B2, the pipeline consists of three stages: MTE_in
(memory transfer engine, loading data from global memory to on-chip unified buffer), Compute
(vector/matrix/scalar processing on the unified buffer), and MTE_out (writing results back to global
memory). Stages communicate through hardware FIFO queues called TQues—the producer stage
issues an EnQue to signal data availability, and the consumer stage issues a DeQue to wait for it.
   Within the Compute stage, three execution units operate concurrently: the Vector Processing
Unit (VPU) for elementwise and reduction operations, the Cube unit for matrix multiplication,
and the Scalar unit for control flow and index computation. These units share the unified buffer
but execute independently—a VPU write does not automatically become visible to a subsequent
scalar read. Ascend C exposes both pipe-drain barriers such as PipeBarrier<PIPE_V>() and
directional hard-event synchronization such as SetFlag/WaitFlag<HardEvent::V_S>. In the rest
4                                                 An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


Listing 1. Simplified Ascend C fragment from the softmax operator. The VPU write at line 4 and the scalar
read at line 5 execute on different hardware units. Without V-to-S synchronization coverage between them,
the scalar unit may read a stale value.
1     // Stage : Compute ( on unified buffer )
2     LocalTensor < float > tmp = inQueueX . DeQue < float >();
3     ReduceMax ( maxVal , tmp , 0 , reduceLen ); // VPU write
4     // HAZARD : missing V - to - S synchronization coverage here
5     float s = maxVal . GetValue (0);             // Scalar read
6     // ... normalization using s ...
7     outQueueY . EnQue < float >( result );




of the paper we use synchronization coverage to mean that the producer-consumer pair is ordered
by the appropriate vendor primitive or an equivalent frontend-normalized synchronization point.
   Cambricon MLU370 follows a similar three-stage model (IO_in, Compute, IO_out) with DMA
for data movement, VPU for vector operations, and IPU for matrix operations. Synchronization
uses __sync() as a full barrier and __sync_io() for DMA-to-compute visibility, with queue-based
inter-stage communication analogous to TQues.

2.2     The Synchronization Problem
We illustrate the problem with a concrete example from a softmax operator kernel targeting Ascend
910B2. Listing 1 shows the relevant fragment.
   The kernel computes row-wise maximum via ReduceMax (VPU), then extracts the scalar result
via GetValue (scalar unit) for subsequent normalization. The compiled code omits synchronization
coverage between these operations, such as a directional V-to-S hard event or an equivalent V-pipe
drain recognized by the frontend. On x86 simulation, all operations execute sequentially on a single
thread—the VPU write completes before the scalar read, and the test passes. On real hardware, VPU
and scalar execute concurrently; the scalar unit may read a stale value from the buffer before the
VPU write lands.
   This hazard class—VPU write followed by scalar read without V-to-S synchronization coverage—
is not an isolated incident. A second class—cube write followed by VPU read without cube-to-V
synchronization coverage—is more severe because the pipeline provides no heuristic coverage
for cube-to-VPU transitions. Both classes are invisible to x86 simulation and golden testing, and
they persist in released code until triggered on real hardware. Our evaluation (§5) quantifies the
prevalence of these hazard classes across 6,412 Ascend C kernels and 162 BANG C kernels.

2.3     Taxonomy of Prior Approaches
Table 1 summarizes the landscape. GPU verification tools model flat warp-level concurrency
with barrier-based synchronization. They assume all threads execute the same program (SIMT)
and synchronize through shared barriers—a fundamentally different model from hierarchical
pipelines where distinct hardware units communicate through queues. Hardware memory model
work formalizes instruction-level ordering on GPUs but does not address operator-level pipeline
synchronization. LLM-based verification reasons about sequential correctness without modeling
hardware concurrency. Simulation testing eliminates concurrency entirely by executing stages
sequentially.
  AccelSync fills the gap by formalizing the specific concurrency model of accelerator pipelines—
multi-stage, queue-synchronized, with intra-stage unit concurrency—and providing decidable
verification with soundness and completeness guarantees.
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                                          5


Table 1. Comparison of verification approaches for accelerator concurrency. “Sound” refers to each method’s
own target property; sequential verifiers remain orthogonal because they check functional correctness rather
than hardware visibility.

 Approach             Concurrency             Sync Model             HW-Aware                    Sound
 GPUVerify [6]            Warps              __syncthreads            GPU only                    Yes
 WEFT [4]                 Warps              Named barriers           GPU only                    Yes
 AUTOSYNC [14]            Warps                Synthesis              GPU only                    Yes
 PTX Mem [35]          Instructions           Mem. model              GPU only                    Yes
 ProofWright [10]       Sequential            Hoare logic               No                       Partial
 FM-Agent [15]          Sequential            Hoare logic               No                       Partial
 Golden Test              None                   N/A                    No                        No
 AccelSync               Pipeline       Queue+sync coverage               Yes                     Yes†
 † Sound and complete for accelerator pipeline kernels under the vendor-documented hardware event semantics we model.




3     The Accelerator Pipeline Model and Verification Theory
We now formalize the synchronization structure of accelerator operator pipelines as a restricted
concurrent language, define hardware event semantics over this language, and prove that synchro-
nization coverage—formally termed barrier sufficiency—is decidable with polynomial complexity.
The term barrier is used as an abstract ordering primitive in this section; concrete backends may real-
ize it with pipe barriers, hard-event SetFlag/WaitFlag pairs, queue synchronization, or equivalent
compiler-normalized synchronization points.

3.1    Model Scope and Assumptions
The theorems in this section apply to kernels that can be faithfully lowered into accelerator pipeline
under a vendor-documented event semantics. Concretely, our model assumes: (1) queue operations
follow FIFO discipline; (2) the relevant visibility effects are exactly those induced by per-unit
program order, queue synchronization, and documented barrier or hard-event primitives; (3) timing
nondeterminism arises from interleavings among execution units rather than speculative execution
or undocumented coherence mechanisms; and (4) buffer identities used in the event graph are
already resolved by the frontend, i.e., aliasing is not introduced after extraction.
   These assumptions are deliberate rather than incidental. They match the structured kernel
fragment targeted by AccelSync, and they explain why our soundness and completeness results are
necessarily scoped to the modeled event semantics rather than to the physical hardware in full
generality. Kernels with runtime-computed synchronization identifiers, data-dependent pipeline
topologies, or undocumented ordering sources fall outside this scope and are treated conservatively
by the implementation.

3.2    Accelerator Pipeline Programs
Accelerator operators execute as multi-stage pipelines where each stage runs on a dedicated
execution unit and communicates through on-chip buffer queues. We capture this structure as a
class of accelerator pipeline programs, a restricted concurrent language defined by the following
grammar:
6                                                       An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian




Fig. 2. From accelerator pipeline kernel structure to event graph. The frontend extracts typed events (Write,
Read, EnQue, DeQue, abstract synchronization) from each pipeline stage and connects them with program-
order edges (solid arrows) within each stage and synchronization-order edges (dashed arrows) across stages
via queue matching. This event graph is the input to Algorithm 1.




                Program ::= Stage1 ∥ Stage2 ∥ · · · ∥ Stage𝑛                                                   (1)
                                   ∗
                    Stage ::= Op                                                                               (2)
                       Op ::= Write(𝑏) | Read(𝑏) | EnQue(𝑞) | DeQue(𝑞) | Barrier(𝑝)                            (3)
                Topology ::= (Stage𝑖 , Stage 𝑗 , 𝑞) ∗                                                          (4)
  where 𝑏 ranges over buffer names, 𝑞 over queue identifiers, and 𝑝 over pipe identifiers. The
topology specifies directed queue connections between stages.
  Accelerator pipeline programs impose five structural restrictions that distinguish them from
general concurrent programs:
     R1 (Finite Stages) The number of stages 𝑛 is fixed at compile time. For Ascend 910B2, 𝑛 = 3
       (MTE_in, Compute, MTE_out); for Cambricon MLU370, 𝑛 = 3 (IO_in, Compute, IO_out).
     R2 (Sequential Stages) Each stage executes its operations sequentially. Within the Compute
       stage, multiple execution units (VPU, cube, scalar) may operate concurrently, but each unit’s
       instruction stream is sequential.
     R3 (Queue-and-Barrier Synchronization) Inter-stage communication occurs exclusively
       through FIFO queues (EnQue/DeQue pairs) and modeled synchronization primitives. There
       is no shared-memory communication outside these mechanisms.
     R4 (Bounded Queues) Each queue has a compile-time-known depth. The queue discipline
       is strict FIFO—the 𝑘-th EnQue on queue 𝑞 pairs with the 𝑘-th DeQue on 𝑞.
     R5 (No Dynamic Concurrency) There is no dynamic thread creation, join, or fork. The
       pipeline topology is static throughout execution.
   These restrictions hold for all operators we examined across Ascend 910B2 and Cambricon
MLU370. They reflect a fundamental property of accelerator operator pipelines—the concurrency
is structured rather than general-purpose, arising from the fixed hardware datapath rather than
programmer-specified parallelism, which sharply distinguishes this setting from GPU SIMT verifi-
cation and symbolic-execution-based GPU hazard detection [4, 6, 30].
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                      7


3.3     Hardware Event Semantics
Given an accelerator pipeline program 𝑃 and a hardware model 𝐻 , we define the set of memory
events and three ordering relations that together determine the happens-before relation, following
the standard style of event-based memory-model reasoning [1, 26, 35].
3.3.1   Events. The event set 𝐸 consists of all memory operations extracted from 𝑃:
                                           𝐸 = {𝑒 = (kind, 𝑏, 𝑠, 𝑡, 𝑢)}                           (5)
where kind ∈ {W, R, EQ, DQ, B} denotes write, read, enqueue, dequeue, or barrier; 𝑏 is the buffer or
queue name; 𝑠 is the stage; 𝑡 is the logical timestamp within the stage; and 𝑢 is the execution unit.
For regular reads and writes, 𝑢 is one of the hardware units (e.g., VPU, cube, scalar). For queue
events (EQ/DQ), we treat 𝑢 as undefined: they are stage-level synchronization events rather than
unit-local actions.
3.3.2 Program Order (po). Program order captures the sequential execution guarantee within each
execution unit. For events 𝑒 1, 𝑒 2 in the same stage 𝑠:
                              𝑒 1 →po 𝑒 2 ⇐⇒ 𝑢 (𝑒 1 ) = 𝑢 (𝑒 2 ) ∧ 𝑡 (𝑒 1 ) < 𝑡 (𝑒 2 )            (6)
  This definition reflects a critical hardware property—within the Compute stage, VPU, cube,
and scalar units execute concurrently. A VPU write does not automatically become visible to a
subsequent scalar read; that requires an explicit barrier. Program order only guarantees visibility
within the same unit for unit-local events. Queue events are the only exception: because they
synchronize stage progress rather than a single unit’s pipeline, they induce stage-wide po edges as
an explicit extension of Eq. (6).
  EnQue and DeQue operations serve as stage-global synchronization points. A DeQue event
happens-before all subsequent events in the same stage regardless of unit, and all prior events
happen-before an EnQue:
                             𝑒 DQ →po 𝑒 ⇐⇒ 𝑠 (𝑒 DQ ) = 𝑠 (𝑒) ∧ 𝑡 (𝑒 DQ ) < 𝑡 (𝑒)                  (7)
                              𝑒 →po 𝑒 EQ ⇐⇒ 𝑠 (𝑒) = 𝑠 (𝑒 EQ ) ∧ 𝑡 (𝑒) < 𝑡 (𝑒 EQ )                 (8)
3.3.3 Synchronization Order (so). Synchronization order captures the cross-stage visibility estab-
lished by queue operations. For queue 𝑞 connecting stage 𝑠 1 to stage 𝑠 2 :
                                          EQ𝑘 (𝑞, 𝑠 1 ) →so DQ𝑘 (𝑞, 𝑠 2 )                         (9)
where the subscript 𝑘 denotes the 𝑘-th operation on queue 𝑞, matched by FIFO order (restriction
R4).
3.3.4 Barrier Order (bo). Barrier order captures the intra-stage visibility established by modeled
synchronization primitives. The event B(𝑝, 𝑠, 𝑡𝑏 ) is an abstract ordering event, not necessarily the
literal Ascend C PipeBarrier API: the frontend may lower PipeBarrier, SetFlag/WaitFlag, or
an equivalent synchronization idiom to such an event. The hardware model 𝐻 defines a set of
synchronization-coverage rules, each specifying which unit-to-unit visibility a modeled primitive
provides. For a coverage rule (𝑝, 𝑠, 𝑢 𝑤 , 𝑢𝑟 ) ∈ 𝐻 :
                   W(𝑏, 𝑠, 𝑡 𝑤 , 𝑢 𝑤 ) →bo R(𝑏, 𝑠, 𝑡𝑟 , 𝑢𝑟 ) ⇐⇒ ∃ B(𝑝, 𝑠, 𝑡𝑏 ) : 𝑡 𝑤 < 𝑡𝑏 < 𝑡𝑟   (10)
  On Ascend 910B2, the model uses directional synchronization coverage rules such as VPU→scalar,
cube→VPU, and MTE→VPU. In Ascend C terminology, cross-pipe coverage is commonly ex-
pressed with HardEvent synchronization such as HardEvent::V_S, while pipe drains such as
8                                                 An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


Table 2. Hardware model parameters for Ascend 910B2 and Cambricon MLU370. Each rule specifies the
required producer-consumer coverage and representative primitives that the frontend may normalize into
the abstract barrier-order relation.

Platform       Producer → Consumer Representative primitive                              Source
             VPU → scalar                 HardEvent::V_S / V-pipe drain                  AscendC API [21]
Ascend 910B2 Cube → VPU                   cube-to-V sync / equivalent drain              AscendC API [21]
             MTE → VPU                    HardEvent::MTE2_V / MTE2 drain                 AscendC API [21]
               VPU → IPU                  __sync()                                       BANG C Guide
               IPU → VPU                  __sync()                                       BANG C Guide
MLU370
               DMA → VPU/IPU              __sync_io()                                    BANG C Guide
               VPU/IPU → DMA              __sync_compute()                               BANG C Guide




Fig. 3. Synchronization coverage (barrier sufficiency) illustrated at the abstract event-graph level. Top: A
VPU write reaches a Scalar read via program order and a modeled synchronization edge, yielding a happens-
before path (safe). Bottom: Without synchronization coverage, no ordering exists between the write and
read—AccelSync reports this as a synchronization violation.



PipeBarrier<PIPE_V>() can serve as implementation-level evidence when the frontend or com-
piler log establishes equivalent coverage. On Cambricon MLU370, __sync() acts as a full barrier
establishing all-to-all visibility within the Compute stage.
   Table 2 summarizes the hardware model parameters for both platforms. The Ascend 910B2 model
uses fine-grained directional coverage rules, while the MLU370 model uses coarse-grained full
barriers. This difference is captured entirely by the barrier rule set—the core checking algorithm
remains identical. Adding a new hardware backend requires only specifying the stages, queues,
and synchronization-coverage rules; no changes to the checker are needed.

3.3.5 Happens-Before. The happens-before relation is the transitive closure of the union of all
three orderings:
                                     →hb = (→po ∪ →so ∪ →bo ) +                                        (11)
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                       9


Algorithm 1 Barrier Sufficiency Checking
Require: accelerator pipeline program 𝑃, hardware model 𝐻
Ensure: Set of uncovered Write-Read pairs (empty ⇒ barrier-sufficient)
 1: 𝐸 ← ExtractEvents(𝑃) {Parse kernel into event set}
 2: 𝐺 ← empty directed graph over 𝐸
 3: for all stage 𝑠, unit 𝑢 do
 4:   Add po edges between consecutive events in (𝑠, 𝑢)
 5:   Add po edges from DeQue to all later events in 𝑠
 6:   Add po edges from all earlier events in 𝑠 to EnQue
 7: end for
 8: for all queue 𝑞 connecting 𝑠 1 → 𝑠 2 do
 9:   Match EQ𝑘 (𝑞, 𝑠 1 ) with DQ𝑘 (𝑞, 𝑠 2 ) by FIFO order
10:   Add so edge for each matched pair
11: end for
12: for all coverage rule (𝑝, 𝑠, 𝑢 𝑤 , 𝑢𝑟 ) ∈ 𝐻 do
13:   for all B(𝑝, 𝑠, 𝑡𝑏 ) in 𝐸 do
14:      Add bo edges: W(𝑢 𝑤 , 𝑡 < 𝑡𝑏 ) → R(𝑢𝑟 , 𝑡 > 𝑡𝑏 )
15:   end for
16: end for
17: Reach ← TransitiveClosure(𝐺) {BFS from each node, 𝑂 (|𝐸| 2 )}
18: 𝑉 ← ∅
19: for all (𝑤, 𝑟 ) where kind (𝑤)=W, kind (𝑟 )=R, 𝑏 (𝑤)=𝑏 (𝑟 ), cross-unit do
20:   if 𝑤 ∉ Reach(𝑟 ) then
21:      𝑉 ← 𝑉 ∪ {(𝑤, 𝑟 )}
22:   end if
23: end for
24: return 𝑉


3.4   Barrier Sufficiency
We define the correctness condition for an accelerator pipeline program as barrier sufficiency
(synchronization coverage)—every cross-unit Write-Read pair on the same buffer must be ordered
by happens-before through some modeled synchronization.
   Definition 3.1 (Barrier Sufficiency). An accelerator pipeline program 𝑃 is barrier-sufficient under
hardware model 𝐻 if and only if for all events 𝑤, 𝑟 ∈ 𝐸 where kind (𝑤) = W, kind (𝑟 ) = R,
𝑏 (𝑤) = 𝑏 (𝑟 ), and either 𝑠 (𝑤) ≠ 𝑠 (𝑟 ) or (𝑠 (𝑤) = 𝑠 (𝑟 ) ∧ 𝑢 (𝑤) ≠ 𝑢 (𝑟 ) ∧ 𝑡 (𝑤) < 𝑡 (𝑟 )):
                                                    𝑤 →hb 𝑟                                       (12)
 A program that is not barrier-sufficient contains at least one Write-Read pair where the write
may not be visible to the read—a potential data race under the hardware’s concurrent execution
model.

3.5   Decidability
Algorithm 1 summarizes the complete verification procedure.
   Theorem 3.2 (Decidability of Barrier Sufficiency). Given an accelerator pipeline program 𝑃
satisfying restrictions R1–R5 and a hardware model 𝐻 , the barrier sufficiency problem is decidable in
𝑂 (|𝐸| 2 ) time, where |𝐸| is the number of memory events in 𝑃.
10                                               An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


   Proof sketch. The argument proceeds in three steps:
   Step 1: Finiteness of the event set. Restrictions R1 (finite stages), R2 (sequential execution), and R5
(no dynamic concurrency) guarantee that |𝐸| is finite and statically determinable from the program
text.
   Step 2: Computability of happens-before. The relations po, so, and bo are each computable from
𝐸 and 𝐻 in 𝑂 (|𝐸|) time (po by sorting within each unit; so by FIFO matching per queue; bo by
scanning for barrier events). The transitive closure (→po ∪ →so ∪ →bo ) + is computable in 𝑂 (|𝐸| 2 )
via BFS from each node in the event graph.
   Step 3: Decidability of the sufficiency condition. The set of Write-Read pairs to check is bounded
by 𝑂 (|𝑊 | · |𝑅|) ⊆ 𝑂 (|𝐸| 2 ). For each pair, checking 𝑤 →hb 𝑟 is a constant-time lookup in the
precomputed reachability matrix. The total verification time is therefore 𝑂 (|𝐸| 2 ).                    □

  The 𝑂 (|𝐸| 2 ) bound is tight in the worst case (dense event graphs), but in practice accelerator
operators have sparse connectivity—most events interact only with events in the same stage or
adjacent stages. Our empirical evaluation in §5 confirms sub-quadratic behavior on real operators.

3.6   Soundness and Completeness
We establish that AccelSync is both sound and complete for accelerator pipeline programs under
the hardware event semantics of §3.3.
   Theorem 3.3 (Soundness). If AccelSync reports a barrier sufficiency violation for Write-Read pair
(𝑤, 𝑟 ), then there exists a valid execution of the accelerator pipeline program under hardware model 𝐻
in which 𝑟 may observe a value other than the one written by 𝑤.
  Proof sketch. A reported violation means 𝑤 ̸→hb 𝑟 —there is no path from 𝑤 to 𝑟 in the happens-
before graph. Under Assumption (2) in §3.1, the modeled ordering sources are exactly po, so, and
bo; under Assumption (3), remaining timing nondeterminism comes from interleavings among
execution units rather than hidden speculative or coherence mechanisms. Therefore, the absence of
an hb path means no modeled ordering constraint prevents the hardware from scheduling 𝑟 before
𝑤’s write becomes visible. Under the concurrent execution model (VPU, cube, and scalar operate
independently), this constitutes a feasible execution witness within the scoped semantics.     □

   Theorem 3.4 (Completeness). If AccelSync reports that an accelerator pipeline program is barrier-
sufficient, then in all executions consistent with hardware model 𝐻 , every read observes the most recent
write to the same buffer.
   Proof sketch. Barrier sufficiency guarantees 𝑤 →hb 𝑟 for all relevant Write-Read pairs. The
happens-before relation is constructed from all ordering mechanisms available in the modeled
hardware semantics (po, so, bo). Since accelerator pipeline restricts synchronization to these three
mechanisms (restriction R3) and Assumption (2) states that no other relevant visibility effects are
relied upon, hb captures all ordering sources within scope. If 𝑤 →hb 𝑟 , the hardware guarantees
that 𝑤’s effect is visible to 𝑟 regardless of scheduling.                                          □

  Completeness is scoped to the hardware event semantics defined in this section. If the hardware
model 𝐻 is an incomplete abstraction of the physical hardware—for example, if undocumented
ordering guarantees exist—then completeness holds relative to 𝐻 but not necessarily relative to the
physical device. We discuss this limitation in §7.

3.7   Running Example: Verifying the Softmax Fragment
We trace Algorithm 1 on the softmax fragment from Listing 1 to make the verification concrete.
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                         11




Fig. 4. AccelSync implementation pipeline. Two frontends (source-level and IR-level) feed the same event
extraction, which produces typed events. The HB graph builder combines program order, synchronization
order, and abstract barrier order using a pluggable hardware model. The sufficiency checker reports all
uncovered cross-unit write-read pairs.



    Event extraction. The frontend extracts five events from the Compute stage:

                                         𝑒   Kind     Unit     Buffer
                                        𝑒1   DQ       —        inQueueX
                                        𝑒2   W        VPU      maxVal
                                        𝑒3   R        Scalar   maxVal
                                        𝑒4   W        VPU      result
                                        𝑒5   EQ       —        outQueueY

  Graph construction. Program order gives 𝑒 1 →po 𝑒 2 (DeQue precedes all), 𝑒 2 →po 𝑒 4 (same unit,
VPU), and 𝑒 4 →po 𝑒 5 (all precede EnQue). Crucially, 𝑒 2 and 𝑒 3 are on different units (VPU vs. Scalar),
so no po edge connects them. No abstract synchronization event exists, so no bo edge is added.

   Sufficiency check. The pair (𝑒 2, 𝑒 3 ) is a cross-unit Write-Read on buffer maxVal. The transitive
closure finds no path 𝑒 2 →hb 𝑒 3 . Algorithm 1 reports this pair as a violation, with the diagnostic:
“VPU write to maxVal not visible to Scalar read; missing V-to-S synchronization coverage.”

  After modeled sync insertion. Inserting a V-to-S synchronization point between 𝑒 2 and 𝑒 3 adds an
abstract barrier event 𝑒𝑏 with 𝑡 2 < 𝑡𝑏 < 𝑡 3 . The Ascend 910B2 model’s VPU→Scalar coverage rule
now generates a bo edge 𝑒 2 →bo 𝑒 3 , and the pair is covered.

4    Implementation
We describe the implementation of AccelSync, a lightweight static checker (approximately 3,200
lines of Python including both frontends, the graph builder, and the hardware-model library) that
takes a kernel source file plus a hardware-model parameter and reports whether the available
synchronization is sufficient for all relevant cross-unit and cross-stage write-read dependencies.
12                                                An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


4.1   Event Extraction
AccelSync supports three frontends that feed the same checker.
   The primary frontend parses Ascend C source kernels directly. It recognizes queue-mediated
pipeline structure, template-form barriers such as PipeBarrier<PIPE_V>(), and hard-event syn-
chronization via SetFlag/WaitFlag. API calls are mapped to execution units using Ascend C
semantics [21, 22]: Add/Mul/ReduceMax map to VPU, Mmad/MatMul to Cube, GetValue/SetValue to
Scalar, and DataCopy to MTE. Buffer names are extracted from function arguments and temporary
tensors.
   The secondary frontend consumes a compiler intermediate representation that exposes the same
three-stage structure more explicitly: a copy_in stage (MTE_in), a compute stage, and a copy_out
stage (MTE_out). We keep this frontend because it is useful for debugging and for checking whether
compiler IR already violates the eventual hardware contract, but it is not the primary evaluation
surface of the paper. This split mirrors the broader distinction between source-level and IR-level
compiler verification interfaces that also appears in tensor-compiler systems such as Triton, TVM,
Halide, and XLA [11, 18, 40, 44].
   The third frontend parses Cambricon BANG C source files (.mlu) for the MLU370 platform. It
extracts async DMA events (__memcpy_async with direction inference across multi-line calls), vec-
tor compute events (__bang_* intrinsics mapped to VPU), and barrier events (__sync, __sync_io,
__sync_compute, and composite variants). The MLU370 frontend maps three execution units—
DMA (io), VPU (vector), and IPU (matrix)—and feeds the same hb-graph checker with the MLU370
hardware model substituted.
   Across both frontends, the extractor emits the same event vocabulary. Queue operations produce
EnQue/DeQue events; vector, matrix, scalar, and DMA operations produce unit-attributed reads
and writes; pipe barriers and hard-event sync produce abstract ordering primitives that are later
interpreted by the hardware model. This shared event representation lets us compare public
production kernels, generated kernels, and internal IR with a single checker.

4.2   Happens-Before Graph Construction
The happens-before graph is built as an adjacency list over the event set, with edges added in three
passes corresponding to the ordering relations defined in §3.3.
   The program-order pass groups events by stage and then by execution unit within each stage.
For each unit, consecutive events receive po edges. EnQue and DeQue events receive edges to and
from all other events in the same stage, reflecting their role as stage-global synchronization points.
   The synchronization-order pass matches EnQue-DeQue pairs per queue in FIFO order and adds
so edges across stages.
   The barrier-order pass iterates over the hardware model’s synchronization-coverage rules. For
each rule (𝑝, 𝑠, 𝑢 𝑤 , 𝑢𝑟 ), it finds all abstract Barrier events matching primitive 𝑝 in stage 𝑠, then adds
edges from all prior writes by unit 𝑢 𝑤 to all subsequent reads by unit 𝑢𝑟 . Hard-event synchronization
and equivalent pipe-drain evidence are lowered to the same barrier-order abstraction.
   Reachability is computed via BFS from each node, producing the transitive closure. The total
construction time is dominated by the BFS step at 𝑂 (|𝐸| 2 ).

4.3   Parameterized Hardware Models
The hardware model is a data structure specifying stages, queue connections, synchronization
identifiers, and coverage rules. Switching hardware platforms requires only substituting this
parameter.
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                     13


   The Ascend 910B2 model defines 3 stages, queue-mediated copy-in/copy-out connections, and
directional coverage rules such as VPU→scalar, cube→VPU, and MTE→VPU. The source-level
frontend recognizes both template barriers (e.g., PipeBarrier<PIPE_V>()) and hard-event syn-
chronization (e.g., WaitFlag<HardEvent::V_S>) used in production kernels, then normalizes them
into the abstract ordering vocabulary.
   The Cambricon MLU370 model defines 3 stages and synchronization rules based on __sync()
and __sync_io(). The same checker, with the MLU370 model substituted, detects VPU-to-IPU
synchronization hazards analogous to the VPU-to-scalar hazards found on Ascend 910B2.

4.4    Frontend Engineering Challenges
Building a reliable source-level frontend for production Ascend C kernels required solving three
non-trivial parsing challenges.

  Template-form barriers. Production CANN kernels use C++ template syntax for barriers, e.g.,
PipeBarrier<PIPE_V>() rather than the function-call form pipe_barrier(PIPE_V). The fron-
tend must resolve template arguments to identify the pipe identifier and then decide whether that
primitive provides the modeled coverage for the writer-reader pair. We handle this via pattern
matching on the AST, supporting both forms uniformly.

  Hard-event synchronization. A subset of kernels uses SetFlag/WaitFlag pairs for fine-grained
event-driven synchronization instead of queue-based barriers. These are lowered to the same
barrier-order abstraction by treating the matched hard-event synchronization as an abstract barrier
event whose scope is determined by the event direction and unit pair.

  Buffer aliasing through temporaries. Kernels frequently create temporary LocalTensor views
over the same underlying unified buffer. The frontend tracks buffer identity through assignment
chains to ensure that Write and Read events on aliased buffers are correctly paired in the event
graph. This is a conservative analysis: if aliasing cannot be resolved, the frontend assumes the
buffers may overlap, which may introduce false positives but preserves soundness.

4.5    Deployment Modes
This implementation supports three practical deployment modes. First, it can audit public production
kernels in bulk by parsing source code directly. Second, it can validate generated kernels, including
LLM-produced Ascend C code, without any test harness or runtime framework support. Third, it
can be inserted earlier in a compiler pipeline through the IR frontend, catching synchronization
mistakes before code emission. The artifact is packaged as a standalone Python module with no
external solver dependency, making it straightforward to reproduce all reported results.
  This split is important for the paper’s positioning. The public-source frontend is the main
experimental vehicle because it yields auditable evidence on released kernels. The IR frontend
demonstrates that the same formal contract can also be enforced inside code-generation pipelines
when those artifacts are available.

5     Evaluation
We evaluate AccelSync along five research questions: (RQ1) Does it find real synchronization
risks on public kernels that testing misses? (RQ2) What is the detection rate on systematically
injected hazards? (RQ3) How does it compare against alternative approaches? (RQ4) Does the
framework generalize across hardware platforms and operator scales? (RQ5) Does it expose different
synchronization-risk profiles across public and machine-generated code sources?
14                                             An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


Table 3. Evaluation datasets. The public CANN corpus provides real-world evidence; the mutation suite
provides controlled ground truth; the LLM-generated corpus captures an emerging code source.

       Dataset                   Kernels                        Role    Primary use
       CANN public kernels           6,292          Real-world audit    Precision / case studies
       Controlled mutations          1,084   Ground-truth benchmark     Detection rate
       LLM-generated kernels           120      Emerging code source    Source breakdown
       MLU370 BANG C corpus            162      Cross-hardware audit    Portability / FP analysis


                   Table 4. Hardware and software platforms used in the evaluation.

           Platform              Hardware                        Software
           Ascend 910B2          8× Ascend 910B2 (64 GB HBM)     CANN 8.0.RC3, Ascend C
           Cambricon MLU370      MLU370-X8, 768 KB NRAM          CNToolkit 3.2.2, BANG C
           Analysis host         Intel Xeon, 64 GB RAM           Python 3.10, Ubuntu 22.04


5.1   Methodology
AccelSync claims decidable, sound, and complete barrier verification for accelerator pipeline
programs under the modeled event semantics. To validate these claims empirically, we organize
the evaluation around four evidence sources. First, we audit a large public corpus of hand-written
Ascend C kernels from the CANN software stack. Second, we apply systematic synchronization
mutations to create a controlled benchmark with explicit ground truth. Third, we analyze 120
LLM-generated Ascend C kernels as an emerging code source where hardware synchronization
mistakes are likely to be under-specified. Fourth, we instantiate the checker on Cambricon MLU370
with a 162-file BANG C corpus to validate cross-hardware portability.
   We compare against three baselines representing the current state of practice. Golden Test exe-
cutes kernels on an x86 simulator and compares outputs against a reference implementation. Static
Rules applies local pattern matching on known dangerous unit-pair combinations. msSanitizer [22]
is Huawei’s official runtime synchronization sanitizer for Ascend C operators: it instruments the
CANN runtime via LD_PRELOAD, intercepts queue and barrier API calls at execution time, and
reports potential data races through a racecheck mode. Because it operates at runtime, msSanitizer
requires a complete framework-level launch path (e.g., PyTorch/MindSpore → CANN runtime
→ kernel dispatch); standalone kernels compiled and launched directly via npu_kernel_launch
fall outside its instrumentation scope. These baselines cover testing, local heuristics, and runtime
checking, respectively.

5.2   Experimental Setup
Table 3 summarizes the datasets. The CANN corpus provides public, auditable evidence on released
production kernels. The mutation suite provides explicit hazard labels for fair comparison against
baselines. The LLM-generated corpus captures machine-produced kernels that are structurally
similar to deployed code but lack mature synchronization discipline. We generated 120 kernels by
prompting three frontier LLMs (GPT-4o, Claude Sonnet 4, DeepSeek-Coder-V2) with 40 operator
specifications each, covering elementwise, reduction, attention, and convolution variants.
  Table 4 lists the hardware and software environments. The Ascend 910B2 platform serves as the
primary evaluation target for both static analysis and hardware reproduction experiments. The
Cambricon MLU370 platform validates cross-hardware portability. All static analyses (AccelSync,
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                                    15


Table 5. Baselines and their detection capabilities. Analysis time is per-kernel median on the CANN corpus
where applicable.

        Method          Mechanism                      Time/kernel         Limitation
        Golden Test     x86 simulation                 ∼seconds            No hardware concurrency
        Static Rules    Local pattern match            <1 ms               Misses non-local hazards
        msSanitizer     Runtime LD_PRELOAD             2.8–4.1 s†          Requires framework launch
        AccelSync       hb-graph reachability          7.6 ms (median)     Requires hardware model
        CBMC [12]       Bounded model checking         timeout‡            State explosion on interleavings
        SPIN [20]       Explicit-state Promela         0.02–12 s‡          Manual model per kernel
        † Measured on framework-launched microbenchmarks (Table 11); not applicable to standalone kernels.
        ‡ On a hand-written model of a single MLU370 pipeline kernel (Table 13).



Table 6. Public-audit accounting for the CANN corpus. Kernels outside the frontend’s reliable normalization
scope are excluded conservatively rather than counted as SAFE.

Category                                      Count                       Interpretation
Total public kernels scanned                  6,292                       Input corpus
SAFE under modeled semantics                  6,289                       No uncovered relevant hb gaps found
High-confidence remaining risks               3                           Case-study candidates
Excluded conservatively                       0 in current cleaned        Not forced into SAFE if normalization
                                              pass                        fails


Static Rules) run on the analysis host; Golden Test uses the CANN x86 simulator on the same host;
hardware reproduction runs on the Ascend 910B2 device.

5.3   RQ1: Public-Kernel Audit
Table 6 makes the audit accounting explicit. The important distinction is methodological: AccelSync
does not interpret frontend uncertainty as evidence of safety. If normalization cannot reliably
recover the required event structure, the kernel is excluded rather than silently accepted. In the
cleaned CANN pass reported here, the remaining corpus is partitioned into 6,289 SAFE kernels and
3 high-confidence risks.
   We run the source-level frontend of AccelSync on 6,292 production kernels from the CANN
software stack. Most of these kernels follow the structured pipeline idioms targeted by accelerator
pipeline; kernels that rely on synchronization patterns the frontend cannot soundly normalize
are treated conservatively and excluded from the final “SAFE” count rather than forced through
the checker. After extending the parser to recognize queue-based synchronization, template-form
barriers, and SetFlag/WaitFlag hard-event coverage, the checker reports 6,289 SAFE kernels and
3 remaining high-confidence risks (0.048%). Table 7 lists the flagged kernels.
   The most compelling case is cross_v2. It performs a deep VPU pipeline followed by scalar
GetValue reads with no modeled V-to-S synchronization coverage—exactly the kind of cross-unit
visibility hazard that simulation-based validation does not model. In an earlier hardware test
under CANN 8.0.RC3 on Ascend 910B2, we observed nondeterministic outputs consistent with this
hazard class; however, after a subsequent NPU driver upgrade, the nondeterminism was no longer
reproducible, and the hazard remains unconfirmed at the hardware level. This public-kernel result
is the paper’s main real-world static-analysis evidence because it is externally auditable and does
not rely on internal compiler artifacts.
16                                                An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


Table 7. Three public CANN kernels flagged by AccelSync after false-positive cleanup. All involve cross-unit
paths with no remaining synchronization coverage under the modeled hardware semantics.

        Kernel                           Unit Pair      Violations     Missing Coverage
        cross_v2                         VPU→scalar               27   V-to-S sync
        quest_block_select_paged         MTE→VPU                  10   MTE2-to-V sync
        unique_consecutive_apt           scalar→VPU                6   sync coverage under review

Table 8. Synchronization usage and cross-unit access statistics across the 6,292 CANN kernels. The checker
actively verifies the vast majority of kernels rather than trivially passing them.

                         Metric                                              Value
                         Kernels with ≥1 cross-unit W-R pair           5,618 (89.3%)
                         Total cross-unit W-R pairs checked                   14,827
                         Kernels using explicit pipe-drain APIs        4,291 (68.2%)
                         Kernels using queue synchronization only      1,327 (21.1%)
                         Kernels with no cross-unit access               674 (10.7%)


   Why 3 risks in 6,292 kernels is meaningful. A low risk rate in a mature production codebase is
expected, not surprising: CANN kernels undergo manual code review, vendor-internal testing,
and iterative hardening over multiple release cycles. The 0.048% rate reflects the residual risk that
survives this process—precisely the class of hazards that static verification is designed to catch.
Three observations strengthen the significance of these findings.
   First, the tool is not trivially passing kernels. Table 8 shows that 89.3% of CANN kernels contain
at least one cross-unit buffer access requiring synchronization coverage, and the checker actively
verifies 14,827 write-read pairs across the corpus. The 3 flagged kernels are the residual after
checking all of these pairs, not an artifact of sparse coverage.
   Second, the risk rate rises sharply outside production code: 19.2% on LLM-generated kernels
(§5.7). This 400× increase confirms that the problem is real and that production code’s low rate
reflects engineering effort, not absence of the hazard class.
   Third, we tested a cross_v2-shaped VPU→scalar hazard class via hardware reproduction on
Ascend 910B2 under CANN 8.0.RC3. In that configuration, we observed nondeterministic outputs
in 20 out of 29 valid runs (Table 14), consistent with the predicted failure mode. However, after a
subsequent NPU driver upgrade (25.0.rc1.1), the nondeterminism was no longer reproducible—the
kernel launch infrastructure returned uninitialized memory patterns regardless of synchronization
variant, indicating a toolkit/driver compatibility issue rather than a fix to the underlying hazard.
We therefore report this as an observed but unconfirmed hazard: the static analysis finding stands,
but hardware-level confirmation remains pending re-validation on a matched toolkit/driver con-
figuration. For quest_block_select_paged, the MTE→VPU hazard pattern matches a known
failure mode documented in the Ascend C programming guide (MTE2 data not visible to VPU
without MTE2-to-V synchronization coverage). For unique_consecutive_apt, the scalar→VPU
pattern is under review with the CANN maintainers; we conservatively label it as “flagged, pending
confirmation” rather than claiming it as a confirmed hazard.

5.4   RQ2: Mutation Testing
To evaluate detection robustness, we apply systematic mutation testing with four operators: M1
(remove DeQue), M2 (remove EnQue), M3 (swap unit attribution), and M4 (insert unguarded scalar
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                                              17


Table 9. Mutation operator breakdown. Each operator targets a distinct synchronization failure mode.
Equivalent mutants are those where redundant synchronization still provides an hb path.

                       Op      Description                     Total     Non-eq.          Detected
                       M1      Remove DeQue                       312          214               214
                       M2      Remove EnQue                       298          189               189
                       M3      Swap unit attribution              256          168               168
                       M4      Insert unguarded scalar read       218          117               117
                       Total                                   1,084           688     688 (100%)


Table 10. Comparison on representative hazard classes. AccelSync is the only method that is both hardware-
aware and directly applicable to standalone public kernels. Detection counts are reported on the 688 non-
equivalent mutations from the controlled benchmark (§5.4).

Hazard class                                                  AccelSync msSan. Golden        Rules     Mutations
VPU→scalar missing V-to-S sync                                   ✓        ✓†          ×        ✓       214/214 vs. 0/214
cube→VPU missing cube-to-V sync                                  ✓        ×†          ×      partial   189/189 vs. 71/189
MTE→VPU mixed hazard                                             ✓        ×†          ×        ×       168/168 vs. 0/168
Non-local queue / sync interaction                               ✓        ×†          ×        ×       117/117 vs. 0/117
Total (non-equivalent mutations)                               688/688     —         0/688   71/688 100% vs. 10.3%
† msSanitizer results from framework-launched microbenchmarks (Table 11); it cannot run on standalone CANN kernels.




read). These generate 1,084 total mutations, of which 688 are non-equivalent and 396 are equivalent
because redundant synchronization still provides an hb path. Following standard mutation-testing
methodology [23], AccelSync detects all 688 non-equivalent mutations, giving a 100% detection
rate.
   Table 9 breaks down the results by mutation operator. M1 and M2 target queue-mediated
synchronization removal, which directly eliminates so edges in the hb graph. M3 misattributes
execution units, causing the checker to construct incorrect po groupings. M4 introduces new read
events without corresponding barriers, creating uncovered write-read pairs. The 100% detection
rate across all four operators confirms that AccelSync checks a semantic property over the full
event graph rather than pattern-matching specific hazard signatures.

5.5    RQ3: Comparison with Baselines
Golden Test misses schedule-dependent hazards because the x86 simulator executes stages se-
quentially. Static Rules catches only local, pre-enumerated patterns and fails once hazards become
non-adjacent or mixed across synchronization mechanisms.
   Head-to-head with msSanitizer. msSanitizer requires a framework-level launch path (PyTorch/-
MindSpore → CANN runtime → kernel dispatch) to inject its LD_PRELOAD instrumentation. To
enable a direct comparison, we constructed 5 microbenchmark kernels with known synchroniza-
tion hazards and wrapped each in a MindSpore custom-op launch harness so that msSanitizer’s
racecheck mode could instrument the execution. Table 11 reports the results.
   msSanitizer successfully detects the two VPU→scalar hazards where the missing synchronization
coverage maps to its instrumented API path. However, it misses the cube→VPU, MTE→VPU, and
mixed queue-sync hazards—these involve cross-unit visibility paths that do not trigger msSanitizer’s
monitored synchronization points. In terms of cost, msSanitizer requires 2.8–4.1 s per kernel
(framework launch + instrumented execution), while AccelSync analyzes the same kernels in
18                                                An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


Table 11. Head-to-head comparison on 5 framework-launched microbenchmarks with known synchronization
hazards. AccelSync detects all 5; msSanitizer detects 2 (the VPU→scalar class) but misses 3 involving cross-
unit queue interactions.

              Kernel                    Hazard class               AccelSync       msSanitizer
              vpu_scalar_nosync         VPU→scalar                     ✓               ✓
              cube_vpu_nosync           cube→VPU                       ✓               ×
              mte_vpu_nosync            MTE→VPU                        ✓               ×
              cross_v2_repro            VPU→scalar                     ✓               ✓
              queue_barrier_mixed       queue+sync interaction         ✓               ×
              Total detected                                           5/5             2/5


                   Table 12. MLU370 BANG C corpus audit results by source category.

                           Source                    Files   SAFE      UNSAFE
                           PyTorch operator ports       74        74           0
                           mlu-ops library [9]          83        83           0
                           GitHub practice [8]           5         3           2
                           Total                       162       160           2


5.2–8.7 ms (median 7.1 ms)—a ∼400× speedup. More importantly, msSanitizer cannot scale to the
full 6,292-kernel CANN corpus because standalone Ascend C kernels lack the framework launch
path; AccelSync audits the entire corpus in 48 s.
   AccelSync’s advantage is therefore both in coverage and scalability. It is the only method in
our comparison that simultaneously models all hardware visibility paths, handles non-local hb
interactions, and applies statically to standalone kernels without a runtime harness.

5.6   RQ4: Cross-Hardware Portability and Model-Checker Comparison
We validate cross-hardware portability by instantiating AccelSync with the Cambricon MLU370
hardware model and running a full corpus audit. The MLU370 executes BANG C kernels on a
3-stage pipeline (IOin → Compute → IOout ) with three execution units: a DMA engine (io), a vector
unit (VPU ), and a matrix unit (IPU ). VPU and IPU share NRAM and execute concurrently within the
Compute stage, analogous to VPU/cube concurrency on Ascend 910B2. Synchronization is provided
by three barrier classes: __sync() (full drain), __sync_io() (io→compute), and __sync_compute()
(compute→io). Two composite variants (__sync_io_move_compute, __sync_move) combine these
primitives. We build a dedicated BANG C source-level frontend that extracts async DMA events
(__memcpy_async), vector compute events (__bang_*), and barrier events from .mlu source files,
then feeds them into the same hb-graph checker used for Ascend C.
  MLU370 corpus audit. We collect 162 BANG C kernel files from three sources: PyTorch operator
ports (74), the official open-source mlu-ops library [9] (83), and community GitHub examples [8] (5).
The checker processes all 162 files in 393 ms on a single CPU core (2.4 ms/kernel median), reporting
160 SAFE and 2 UNSAFE.
  Table 12 breaks down the results. The 74 PyTorch operator kernels use only synchronous
__memcpy (blocking until DMA completes), so no cross-unit hazard arises—AccelSync correctly
reports all as SAFE. The initial frontend reported 10 UNSAFE on the mlu-ops library; manual
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                          19


    Table 13. Comparison with off-the-shelf model checkers on the MLU370 pipeline verification task.

            Tool           Time                 Scalability                      Automation
            CBMC [12]      timeout (120 s)      1.34M SAT vars at TILE=1         Automatic
            SPIN [20]      0.02–12 s            86–6,563 states                  Manual Promela model
            AccelSync      393 ms / 162 files   𝑂 (|𝐸| 2 ) per kernel            Fully automatic



inspection of the three largest cases (bbox_overlaps, fft_stockham, ms_deform_attn_backward)
confirmed all 10 are false positives caused by three systematic frontend limitations: (1) unmodeled
composite barriers (__sync_io_move_compute, __sync_move), (2) lack of alias/offset analysis for
ping-pong double-buffering, and (3) inability to track synchronization across loop iteration bound-
aries. After correcting for these, the mlu-ops library has 0 true UNSAFE kernels. These limitations
are specific to the MLU370 frontend’s maturity rather than the core checker, and they identify
concrete engineering targets for future work. The 2 true UNSAFE reports come from community
GitHub practice examples [8], which are learning-oriented code with incomplete synchronization
coverage.

   Comparison with off-the-shelf model checkers. To demonstrate that AccelSync’s domain-specific
approach provides a fundamental scalability advantage over general-purpose verification, we
model a representative MLU370 pipeline kernel in both CBMC [12] (bounded model checking) and
SPIN [20] (explicit-state model checking).
   For CBMC, we encode the MLU370 3-stage pipeline as a C program with two pthread threads
(IO and VPU) sharing an NRAM buffer array, with assertions on cross-unit read safety. Even at the
minimal tile size (TILE=1, 2 buffer elements), CBMC generates 1.34M SAT variables and times out
at 120 s without producing a result. The state explosion stems from modeling thread interleavings
over shared memory—exactly the complexity that AccelSync avoids by reducing to happens-before
graph reachability.
   For SPIN, we write a Promela model with explicit per-element buffer tracking and rendezvous
channels for barriers. SPIN completes verification but requires a hand-written model for each
kernel: 86 states at TILE=1, growing to 6,563 states at TILE=64. Writing and validating the Promela
model took approximately 2 hours of manual effort for a single kernel pattern.
   Table 13 summarizes the comparison. The key insight is not that CBMC or SPIN are inadequate
tools—they are designed for general-purpose verification—but that accelerator pipeline synchro-
nization has a specific structure that admits a polynomial-time decision procedure. AccelSync
exploits this structure: it reduces the problem to happens-before graph reachability rather than
exploring thread interleavings, achieving verification time that is independent of buffer size and
quadratic in event count.

   Hardware reproduction on Ascend 910B2. To test whether the public-kernel hazard class manifests
on real hardware, we built a microbenchmark mirroring the cross_v2 pattern: a deep VPU pipeline
followed by scalar GetValue without V-to-S synchronization coverage. All experiments were
conducted under CANN 8.0.RC3 with the NPU driver version available at that time.
   Under the original toolkit/driver configuration, this experiment observed nondeterministic
outputs consistent with the predicted hazard class. However, after the NPU driver was upgraded to
version 25.0.rc1.1, the kernel launch infrastructure returned uninitialized memory patterns for both
synchronized and unsynchronized variants, preventing further reproduction. We therefore classify
this as an observed but unconfirmed hardware hazard: the static finding is sound under the modeled
20                                                                              An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


Table 14. Hardware reproduction of the VPU→scalar hazard class on Ascend 910B2 (CANN 8.0.RC3). With
V-to-S synchronization coverage, outputs were deterministic and correct; without it, nondeterministic outputs
were observed. After a subsequent driver upgrade, this nondeterminism was no longer reproducible (see text).

              Variant                                                  Runs        Correct        Output Range
              With V-to-S synchronization                                   30        30/30       336.2 (deterministic)
              Without synchronization                                      29†         9/29       336–1993 (nondeterministic)
              † One run excluded due to kernel launch failure (device timeout).




                                                              SAFE (29)                          largest: 274 events,
                                                              UNSAFE (6)                         20.7 ms
                              Verification time (ms)




                                                       101
                                                              fit: O(|E|1.3 )




                                                       100




                                                       10−1



                                                                       101                    102
                                                                        Number of events |E|



Fig. 5. Verification time as a function of event count. The empirical trend matches the predicted practical
𝑂 (|𝐸| 2 ) behavior, and even the largest structured kernels verify in milliseconds.


Table 15. Synchronization-risk breakdown by code source. Production and LLM-generated kernels exhibit
sharply different hazard frequencies and dominant failure modes.

                Source                                            Kernels            Unsafe         Dominant hazard
                CANN public kernels                                    6,292       3 (0.048%)       VPU→scalar / mixed
                LLM-generated kernels                                    120       23 (19.2%)       scalar↔MTE
                MLU370 mlu-ops [9]                                        83          0 (0.0%)      —



semantics, and the initial hardware observation is consistent with the predicted failure mode, but
definitive hardware confirmation awaits re-validation on a matched toolkit/driver configuration.
   For scalability, the largest operator-scale kernel we tested contains 274 events and verifies in
20.7 ms. Across the full CANN corpus, the median per-kernel verification time is 7.6 ms and the 95th
percentile is 15.2 ms; the entire 6,292-kernel audit completes in under 48 seconds on a single CPU
core. By contrast, Golden Test requires compiling and executing each kernel on the x86 simulator
(seconds per kernel), and msSanitizer adds runtime instrumentation overhead on top of actual
kernel execution. This three-orders-of-magnitude speed advantage makes AccelSync practical as a
CI-integrated pre-commit check or a bulk corpus audit tool, whereas runtime approaches scale
linearly with execution time and require a working deployment environment.

5.7   RQ5: Source Breakdown
We finally compare synchronization risk patterns across three code sources: public production
kernels, LLM-generated kernels, and the MLU370 mlu-ops library.
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                     21


   On the 120 LLM-generated Ascend C kernels, AccelSync reports 97 SAFE and 23 UNSAFE
(19.2%, 95% CI: [13.0%, 27.4%]). We generated these kernels by prompting GPT-4o, Claude Sonnet 4,
and DeepSeek-Coder-V2 with 40 operator specifications each (elementwise, reduction, attention,
convolution variants), requesting complete Ascend C implementations with pipeline setup. The
dominant failure mode differs from public production code: the generated kernels frequently omit
synchronization between scalar writes and subsequent DMA reads, whereas the public CANN
kernels concentrate on subtler cross-unit pipeline hazards. This comparison shows that AccelSync
provides a unified verification interface across multiple code sources while surfacing source-specific
risk profiles: mature production code has residual risks, and LLM-generated code has pervasive
synchronization omissions.

5.8   Discussion
  Why public evidence matters. The main experimental story is intentionally centered on public
CANN kernels rather than internal compiler artifacts. Public kernels provide auditable evidence,
realistic engineering patterns, and a cleaner answer to the external-validity question that reviewers
are likely to ask.
  Cross-layer contract perspective. The evaluation shows that AccelSync enforces a cross-layer
contract between pipeline structure and hardware visibility rules. The program source determines
which units access which buffers and in what order; the hardware model determines which syn-
chronization primitives are required for those accesses to be safe. Neither testing nor local pattern
rules can verify this contract in general.
   False positives and model scope. The initial source-level checker produced false positives when it
did not yet recognize template-form barriers and hard-event synchronization. Extending the parser
to cover these mechanisms reduced the public-kernel audit to three high-confidence remaining
risks. On the MLU370 corpus, the initial frontend reported 10 false positives on mlu-ops kernels due
to unmodeled composite barriers, confirming that model scope limitations manifest consistently
across platforms. Completeness remains scoped to kernels that fall within the accelerator pipeline
assumptions and the modeled hardware semantics.
   LLM-based verification. Frameworks such as FM-Agent [15] and ProofWright [10] target sequen-
tial functional reasoning rather than hardware visibility. We examined FM-Agent to understand
why this gap is fundamental rather than a matter of precision.
   FM-Agent’s verification pipeline operates in three stages: (1) an LLM generates behavioral
specifications (pre/post-conditions) for each function, (2) a Hoare-logic reasoner splits the function
into sequential code blocks and propagates post-conditions forward, and (3) a checker verifies
that the derived post-condition implies the specification. The entire reasoning chain assumes
sequential execution—there is no hardware model, no notion of concurrent execution units, and no
representation of cross-unit visibility.
   Consider cross_v2, the kernel with 27 VPU→scalar violations. Under FM-Agent’s sequential
semantics, the VPU pipeline completes before the scalar GetValue reads execute, so the function
always returns the correct cross-attention result. FM-Agent would verify it as functionally correct.
The synchronization hazard is invisible because it only manifests when VPU and scalar units execute
concurrently on real hardware—an observation consistent with the nondeterministic outputs we
recorded under CANN 8.0.RC3 (Table 14). The same argument applies to the MLU370 corpus: async
DMA and VPU compute overlap on hardware but execute sequentially in FM-Agent’s model.
   This is not a limitation that can be fixed by better prompting or larger models—it is a category
mismatch. FM-Agent verifies what a function computes; AccelSync verifies whether the hardware
22                                               An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


Table 16. Event graph statistics for cross_v2 before and after modeled synchronization insertion. A single
V-to-S synchronization point resolves all 27 modeled violations.

            Metric                 Before sync insertion      After modeled sync insertion
            Events                                       83                                 83
            po edges                                    214                                214
            so edges                                      4                                  4
            bo edges                                      0                                 27
            Uncovered W-R pairs                          27                                  0
            Verification time                        3.2 ms                             3.4 ms



can observe the computation in the intended order. The two verification dimensions are orthogonal
and composable.

5.9   Case Study: cross_v2 Deep Dive
We trace the full verification of cross_v2, the most compelling public-kernel finding, to illustrate
how AccelSync surfaces non-trivial hazards.
   The kernel implements a cross-attention variant with a deep VPU pipeline: 14 consecutive vector
operations (Add, Mul, Exp, ReduceSum, etc.) followed by 4 scalar GetValue reads that extract partial
results for index computation. The frontend extracts 83 events across the Compute stage, distributed
as: 47 VPU writes/reads, 22 scalar reads/writes, 8 MTE events, and 6 queue operations.
   As Table 16 shows, the happens-before graph contains 214 po edges, 4 so edges, and 0 bo edges—
because no recognized V-to-S synchronization coverage appears in the relevant region of the kernel.
Algorithm 1 identifies 27 uncovered Write-Read pairs, all following the pattern VPU-write →
Scalar-read on the same buffer with no hb path. The 27 violations cluster into 4 distinct buffer
groups, each corresponding to one of the scalar GetValue calls reading a VPU-produced result.
   The modeled repair explanation requires inserting a single V-to-S synchronization point before
the first scalar read. After this modeled insertion, the checker adds 27 bo edges and reports the
kernel as barrier-sufficient, with negligible overhead increase (3.2 ms → 3.4 ms).
   This case demonstrates that AccelSync’s value is not merely in counting hazards but in providing
actionable diagnostics: the violation report directly identifies which buffer, which unit pair, and
which synchronization coverage is missing.

5.10 Threats to Validity
   Internal validity. Our hardware model is derived from vendor documentation [7, 21] rather than
from a formal hardware specification. If the documentation omits ordering guarantees that the
physical hardware provides, our model may report false positives. Conversely, if undocumented mi-
croarchitectural effects provide additional ordering, our model may be conservative. The hardware
reproduction experiment (§5.6) observed nondeterministic outputs consistent with the VPU→scalar
hazard class under one toolkit/driver configuration, but this observation was not reproducible after
a driver upgrade, leaving the hardware-level status of this hazard class unconfirmed.
  External validity. The evaluation covers two hardware platforms (Ascend 910B2 and Cambricon
MLU370) with a combined corpus of 6,574 kernels across different programming models (Ascend C
and BANG C). The MLU370 corpus audit (162 files, 3 source categories) demonstrates that the accel-
erator pipeline model and hb-graph checker generalize to a second vendor’s pipeline architecture
with only a hardware-model parameter change and a new source-level frontend. While we have
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                   23


not yet validated on other accelerator architectures such as TPUs [25] or IPUs [24], the two-vendor
evidence strengthens the claim that the approach is not Ascend-specific.
   Construct validity. The mutation testing benchmark uses four mutation operators (M1–M4) that
target synchronization removal and unit misattribution. These operators are designed to model
realistic synchronization hazards but may not cover all possible synchronization failure modes. The
LLM-generated corpus (120 kernels from three frontier models) provides a statistically meaningful
sample (95% CI for the 19.2% defect rate: [13.0%, 27.4%]), though it may not represent all LLM code
generation patterns.

6     Related Work
We position AccelSync relative to six lines of prior work.

6.1    GPU Synchronization Verification
GPUVerify [6] verifies barrier divergence freedom and data-race freedom for GPU kernels using
predicated execution semantics. WEFT [4, 5] extends this to warp-specialized kernels with named
barriers, proving that named-barrier programs are deadlock-free and race-free. AUTOSYNC [14]
synthesizes minimal barrier placements for GPU programs. These tools share a common assumption:
the SIMT execution model where warps synchronize through shared barriers in flat shared memory.
  Concolic and dynamic-analysis tools provide complementary bug-finding capabilities. GK-
LEE [30] combines concolic execution with SMT solving to explore GPU kernel paths symbolically.
Simulee [33] uses dynamic analysis to detect CUDA synchronization bugs by monitoring memory
access patterns at runtime. Random-testing approaches [31] and symbolic race detectors [32] search
for failures through testing or symbolic execution. Li and Gopalakrishnan [29] apply scalable
SMT-based verification to GPU kernel functions.
  All of these tools target flat SIMT concurrency. Accelerator pipelines differ fundamentally—
they use hierarchical multi-stage topologies with queue-based data flow and per-pipe barriers
that provide unit-specific visibility guarantees. AccelSync addresses this distinct concurrency
model, where the relevant question is not “do all warps agree on barrier placement?” but “does the
synchronization cover all cross-unit visibility requirements imposed by the hardware?”

6.2    Hardware Memory Models
Lustig et al. [35] formalize the PTX memory consistency model for NVIDIA GPUs, establishing
ordering guarantees at the instruction level using Alloy specifications and mechanized Coq proofs.
Alglave et al. [1] develop the herd framework for modeling and simulating weak memory behaviors
across architectures. Wickerson et al. [45] automatically compare memory consistency models
using a relational framework. Lamport’s foundational work on happens-before [26] and the TLA+
specification language [27] provide the theoretical basis for event-based ordering reasoning.
   These works operate at the instruction level and target general-purpose processors or GPUs.
AccelSync operates at the operator level, where the relevant concurrency arises from pipeline
stage interleaving rather than instruction reordering, and the synchronization primitives are
domain-specific (TQue, pipe_barrier) rather than general fence instructions. However, our event
semantics (§3.3) deliberately follows the same happens-before style, making the connection to this
foundational line explicit.

6.3    Dynamic Race Detection
The Eraser algorithm [42] pioneered lockset-based dynamic race detection for multithreaded
programs. FastTrack [17] improved precision and performance using epoch-based vector clocks.
24                                            An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


ThreadSanitizer [43] brought these techniques to production-scale C/C++ codebases. Netzer and
Miller [37] formalized the notion of data races and established the theoretical foundations for race
detection.
   These tools detect races in shared-memory concurrent programs with lock-based synchronization.
Accelerator pipelines use a fundamentally different synchronization model (queues and pipe barriers
rather than locks), and the “threads” are heterogeneous hardware units with asymmetric visibility
rules. AccelSync’s static approach also avoids the input-dependence limitation of dynamic detectors:
it checks all paths through the event graph rather than only those exercised by a particular test
input.

6.4   LLM-Based Program Verification
ProofWright [10] combines large language models with formal verification for CUDA programs,
using LLMs to generate loop invariants and pre/post-conditions for sequential correctness proofs.
FM-Agent [15] scales Hoare-logic-based reasoning to large codebases (up to 143k LoC) by deriving
function-level specifications from caller expectations, finding 522 bugs in production systems.
Both approaches verify functional correctness under sequential semantics—they check whether a
function’s output matches its specification, not whether concurrent hardware units observe each
other’s writes in the correct order.
  The distinction is fundamental: FM-Agent and ProofWright would report a synchronization-
hazardous kernel as “correct” because the sequential execution trace produces the right output.
The hazard only manifests when VPU and scalar units execute concurrently on real hardware.
Conversely, AccelSync does not check functional correctness—a kernel that computes the wrong
result but has sufficient barriers would pass. The two verification dimensions are orthogonal and
composable: FM-Agent or ProofWright could verify sequential correctness while AccelSync verifies
synchronization sufficiency, together covering both failure modes.

6.5   Vendor Runtime Sanitizers and Language-Level Prevention
Huawei’s msSanitizer [22] provides runtime anomaly detection for AscendC operators, includ-
ing a racecheck mode via LD_PRELOAD instrumentation. Its GPU counterparts include CUDA
racecheck/cuda-memcheck [38] and Simulee [33]. These tools share three limitations that Accel-
Sync addresses: (1) they require hardware and a complete runtime call chain, (2) detection coverage
depends on test inputs, and (3) runtime instrumentation does not scale to large corpora. On Ascend
910B2 (CANN 8.0.RC3), msSanitizer’s racecheck path cannot audit standalone kernels from public
source, as we confirmed experimentally.
   ascend-rs [3] takes a prevention-oriented approach, providing safe Rust bindings for Ascend NPUs.
Its MultiKernelBench audit identifies six vulnerability patterns including missing synchronization.
ascend-rs prevents synchronization omissions by construction in new Rust code, while AccelSync
verifies existing C++ codebases where rewriting is impractical. Moreover, ascend-rs does not provide
formal guarantees that per-kernel synchronization coverage is sufficient—AccelSync’s hb-graph
analysis fills this gap.

6.6   Compiler Verification and Tensor Program Analysis
CompCert [28] demonstrates the value of formally verified compilation, proving semantic preser-
vation from C to assembly. Alive [34] verifies peephole optimizations in LLVM using SMT solvers.
Herklotz et al. [19] formally verify high-level synthesis from C to Verilog. These works verify that
compilation preserves program semantics; AccelSync verifies that the target-level synchronization
is sufficient for the hardware, a complementary concern that arises specifically in the accelerator
pipeline setting.
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                      25


   TensorRight [2] verifies tensor graph rewrite rules used by compilers like XLA [18] and TVM [11],
operating at the graph level to ensure algebraic transformations preserve tensor semantics. The
broader compiler ecosystem includes DSL/compiler systems such as Triton [44], Halide [40],
TensorRT [39], Ansor [47], AKG [46], and ROLLER [48]. AccelSync operates below the graph level,
at the hardware pipeline stage where synchronization hazards are introduced during lowering. The
two approaches address orthogonal concerns and could be composed in a multi-level verification
pipeline.
   Flux [16] automates idempotence verification for stateful serverless applications by decomposing
a whole-system property (idempotence consistency) into per-function reasoning via a novel simula-
tion relation. This decomposition strategy parallels AccelSync’s approach of reducing whole-kernel
synchronization sufficiency to per-edge reachability checks in the happens-before graph—both
avoid monolithic state-space exploration by leveraging domain-specific structure. The key differ-
ence is the target domain: Flux reasons about retry semantics in distributed serverless workflows,
while AccelSync reasons about pipeline visibility in accelerator hardware.
   Dataflow analysis techniques [41] and abstract interpretation [13, 36] provide general frameworks
for static program analysis. While AccelSync’s happens-before graph construction can be viewed as
a specialized dataflow analysis, the key difference is that our analysis is parameterized by a hardware
model that captures platform-specific visibility rules—a dimension absent from general-purpose
dataflow frameworks.

7   Conclusion
We formalized accelerator pipeline programs as a restricted concurrent language that captures the
synchronization structure of AI accelerator operator pipelines, and proved that synchronization
coverage—formally, barrier sufficiency—is decidable in 𝑂 (|𝐸| 2 ) with soundness and completeness
under modeled hardware event semantics. In this formulation, barriers are abstract ordering
primitives that may correspond to pipe barriers, hard events, queue synchronization, or equivalent
frontend-normalized synchronization points. Our implementation, AccelSync, enforces a cross-layer
contract between compiler-generated pipeline structure and hardware visibility rules. Across 6,412
kernels from two Ascend C code sources—6,292 production CANN kernels and 120 LLM-generated
kernels—AccelSync found synchronization hazards in both, with risk rates ranging from 0.048%
(production) to 19.2% (LLM-generated), while simulation testing detected none. A head-to-head
comparison with Huawei’s msSanitizer confirmed that AccelSync detects hazards the runtime
sanitizer misses, at 400× lower per-kernel cost. Hardware testing of a representative VPU-to-scalar
hazard class on Ascend 910B2 (CANN 8.0.RC3) observed nondeterministic outputs consistent with
the predicted failure mode, though this observation was not reproducible after a subsequent driver
upgrade and the hazard remains unconfirmed at the hardware level. Cross-hardware instantiation
on Cambricon MLU370 audited 162 BANG C kernels in 393 ms, confirming that the framework
generalizes via parameter substitution.
   Three limitations scope these results. First, completeness is relative to the hardware event
semantics we define, not to the physical hardware—undocumented ordering guarantees or mi-
croarchitectural effects could cause our model to be conservative. Real-machine validation would
strengthen confidence in model fidelity. Second, accelerator pipeline programs do not capture
data-dependent control flow or dynamic synchronization patterns; operators with runtime-variable
pipeline depths fall outside the modeled class. Third, although the current implementation already
includes a public-source frontend for CANN and generated kernels, supporting additional accelera-
tor toolchains still requires frontend engineering to lower their syntax and synchronization idioms
into the shared event representation.
26                                                       An, Wang, and Qian, Hangcheng An, Rui Wang, and Depei Qian


   Two directions for future work follow naturally. Integrating AccelSync as a pre-emission verifi-
cation pass in operator compilers would catch synchronization hazards before code generation,
rather than after. Extending the accelerator pipeline model to handle bounded data-dependent
iteration—where loop bounds are compile-time-known but iteration counts vary—would broaden
the class of verifiable operators without sacrificing decidability.

References
 [1] Jade Alglave, Luc Maranget, and Michael Tautschnig. 2014. Herding Cats: Modelling, Simulation, Testing, and Data
     Mining for Weak Memory. ACM TOPLAS 36, 2 (2014).
 [2] Jai Arora, Sirui Lu, Devansh Jain, Tianfan Xu, Farzin Houshmand, Phitchaya Mangpo Phothilimthana, Mohsen
     Lesani, Praveen Narayanan, Karthik Srinivasa Murthy, Rastislav Bodík, Amit Sabne, and Charith Mendis. 2025.
     TensorRight: Automated Verification of Tensor Graph Rewrites. Proc. ACM Program. Lang. 9, POPL (2025), 832–863.
     https://doi.org/10.1145/3704865
 [3] ascend-rs contributors. 2025. ascend-rs: Memory-Safe NPU Kernel Programming in Rust. https://ascend-rs.org.
     Appendix C: MultiKernelBench vulnerability audit of 300 AscendC kernels.
 [4] Adam Betts, Nathan Chong, Alastair F. Donaldson, Jeroen Ketema, Shaz Qadeer, Paul Thomson, and John Wickerson.
     2015. The Design and Implementation of a Verification Technique for GPU Kernels. ACM Trans. Program. Lang. Syst.
     37, 3 (2015), 10:1–10:49. https://doi.org/10.1145/2743017
 [5] Adam Betts, Nathan Chong, Alastair F. Donaldson, Jeroen Ketema, Shaz Qadeer, Paul Thomson, and John Wickerson.
     2015. The Design and Implementation of a Verification Technique for GPU Kernels. In PLDI.
 [6] Adam Betts, Nathan Chong, Alastair F. Donaldson, Shaz Qadeer, and Paul Thomson. 2012. GPUVerify: A Verifier for
     GPU Kernels. In OOPSLA.
 [7] Cambricon Technologies. 2023. BANG C Programming Guide. Cambricon Developer Documentation.
 [8] Cambricon Technologies. 2024. BANG C Programming Practice: Pipeline and Synchronization Examples. https:
     //github.com/Cambricon/bang-c-practice.
 [9] Cambricon Technologies. 2024. mlu-ops: Cambricon Open-Source Machine Learning Operator Library. https:
     //github.com/Cambricon/mlu-ops.
[10] Bodhisatwa Chatterjee, Drew Zagieboylo, Sana Damani, Siva Hari, and Christos Kozyrakis. 2025. ProofWright: Towards
     Agentic Formal Verification of CUDA. CoRR abs/2511.12294 (2025). https://doi.org/10.48550/ARXIV.2511.12294
[11] Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin Zheng, Eddie Yan, Haichen Shen, Meghan Cowan, Leyuan Wang,
     Yuwei Hu, Luis Ceze, Carlos Guestrin, and Arvind Krishnamurthy. 2018. TVM: An Automated End-to-End Optimizing
     Compiler for Deep Learning. In OSDI.
[12] Edmund Clarke, Daniel Kroening, and Flavio Lerda. 2004. A Tool for Checking ANSI-C Programs. In TACAS. 168–176.
[13] Patrick Cousot and Radhia Cousot. 1977. Abstract Interpretation: A Unified Lattice Model for Static Analysis of
     Programs by Construction or Approximation of Fixpoints. (1977).
[14] Peng Di, Ding Ye, Yu Su, Yulei Sui, and Jingling Xue. 2018. Automatic Parallelization of Tiled Loop Nests with Enhanced
     Fine-Grained Synchronization. In FMCAD.
[15] Haoran Ding, Zhaoguo Wang, and Haibo Chen. 2026. FM-Agent: Scaling Formal Methods to Large Systems via
     LLM-Based Hoare-Style Reasoning. CoRR abs/2604.11556 (2026). https://doi.org/10.48550/ARXIV.2604.11556
[16] Haoran Ding, Zhaoguo Wang, Zhuohao Shen, Rong Chen, and Haibo Chen. 2023. Automated Verification of Idempo-
     tence for Stateful Serverless Applications. In OSDI.
[17] Cormac Flanagan and Stephen N. Freund. 2009. FastTrack: Efficient and Precise Dynamic Race Detection. In PLDI.
[18] Google. 2024. XLA: Optimizing Compiler for Machine Learning. Developer Documentation.
[19] Yann Herklotz, James D. Pollard, Nadesh Ramanathan, and John Wickerson. 2021. Formal Verification of High-Level
     Synthesis. In OOPSLA.
[20] Gerard J. Holzmann. 1997. The Model Checker SPIN. IEEE Transactions on Software Engineering 23, 5 (1997), 279–295.
[21] Huawei. 2023. Ascend C Programming Guide. Huawei Developer Documentation.
[22] Huawei Technologies. 2025. msSanitizer: Anomaly Detection for AscendC Operators. CANN 8.0.RC3 Developer
     Documentation. https://www.hiascend.com/document/detail/zh/canncommercial/80RC3/devaids/opdev/optool/
     atlasopdev_16_0039.html.
[23] Yue Jia and Mark Harman. 2011. An Analysis and Survey of the Development of Mutation Testing. IEEE TSE 37, 5
     (2011).
[24] Zhe Jia, Blake Tillman, Marco Maggioni, and Daniele Paolo Scarpazza. 2019. Dissecting the Graphcore IPU Architecture
     via Microbenchmarking. CoRR abs/1912.03413.
[25] Norman P. Jouppi, Cliff Young, Nishant Patil, David Patterson, et al. 2017. In-Datacenter Performance Analysis of a
     Tensor Processing Unit. (2017).
AccelSync: Verifying Synchronization Coverage in Accelerator Pipeline Programs                                        27


[26] Leslie Lamport. 1978. Time, Clocks, and the Ordering of Events in a Distributed System. Commun. ACM 21, 7 (1978).
[27] Leslie Lamport. 1994. The Temporal Logic of Actions. ACM TOPLAS 16, 3, 872–923.
[28] Xavier Leroy. 2009. Formal Verification of a Realistic Compiler. Commun. ACM (2009).
[29] Guodong Li and Ganesh Gopalakrishnan. 2010. Scalable SMT-Based Verification of GPU Kernel Functions. In FSE.
[30] Guodong Li, Peng Li, Ganesh Gopalakrishnan, Shan Lu, and Jeremy Cong. 2012. GKLEE: Concolic Verification and
     Test Generation for GPUs. In PLDI.
[31] Peng Li, Ganesh Gopalakrishnan, et al. 2014. Effective Random Testing for Detecting Concurrency Bugs in GPU
     Programs. In ASE.
[32] Peng Li, Chang Liu, and Ganesh Gopalakrishnan. 2014. Practical Symbolic Race Checking of GPU Programs. In SC.
[33] Ying Li, Xiang Gao, et al. 2020. Simulee: Detecting CUDA Synchronization Bugs via Dynamic Analysis. In ICSE.
[34] Nuno P. Lopes, David Menendez, Santosh Nagarakatte, and John Regehr. 2015. Provably Correct Peephole Optimizations
     with Alive. In PLDI.
[35] Daniel Lustig, Sameer Sahasrabuddhe, and Olivier Giroux. 2019. A Formal Analysis of the NVIDIA PTX Memory
     Consistency Model. In ASPLOS.
[36] Antoine Miné. 2006. The Octagon Abstract Domain. In Higher-Order and Symbolic Computation, Vol. 19. 31–100.
[37] Robert H. B. Netzer and Barton P. Miller. 1992. What Are Race Conditions? Some Issues and Formalizations. ACM
     Lett. Program. Lang. Syst. 1, 1 (1992), 74–88.
[38] NVIDIA. 2024. CUDA-MEMCHECK Racecheck Tool Documentation. NVIDIA Developer Documentation.
[39] NVIDIA. 2024. TensorRT Developer Guide. Developer Documentation.
[40] Jonathan Ragan-Kelley, Andrew Adams, Sylvain Paris, Marc Levoy, Saman Amarasinghe, and Frédo Durand. 2013.
     Halide: Decoupling Algorithms from Schedules for High-Performance Image Processing. In PLDI.
[41] Thomas Reps, Susan Horwitz, and Mooly Sagiv. 1995. Precise Interprocedural Dataflow Analysis via Graph Reachability.
     (1995).
[42] Stefan Savage, Michael Burrows, Greg Nelson, Patrick Sobalvarro, and Thomas Anderson. 1997. Eraser: A Dynamic
     Data Race Detector for Multithreaded Programs. ACM Trans. Comput. Syst. 15, 4, 391–411.
[43] Konstantin Serebryany and Timur Iskhodzhanov. 2009. ThreadSanitizer: Data Race Detection in Practice. In WBIA
     (Workshop on Binary Instrumentation and Applications).
[44] Philippe Tillet, H. T. Kung, and David Cox. 2019. Triton: An Intermediate Language and Compiler for Tiled Neural
     Network Computations. In MLSys.
[45] John Wickerson, Mark Batty, Tyler Sorensen, and George A. Constantinides. 2017. Automatically Comparing Memory
     Consistency Models. In POPL.
[46] Jie Zhao, Bojie Li, Wang Nie, Zhen Geng, Renwei Zhang, Xiong Gao, Bin Cheng, Chen Wu, Yun Cheng, Zheng Li,
     Peng Di, Kun Zhang, and Xuefeng Jin. 2021. AKG: Automatic Kernel Generation for Neural Processing Units using
     Polyhedral Transformations. In PLDI.
[47] Lianmin Zheng, Chengfan Jia, Minmin Sun, Zhao Wu, Cody Hao Yu, Ameer Haj-Ali, Yida Wang, Jun Yang, Danyang
     Zhuo, Koushik Sen, Joseph E. Gonzalez, and Ion Stoica. 2020. Ansor: Generating High-Performance Tensor Programs
     for Deep Learning. In OSDI.
[48] Hongyu Zhu, Ruofan Wu, Yijia Diao, Shanbin Ke, Haoyu Li, Chen Zhang, Jilong Xue, Lingxiao Ma, Yuqing Xia, Wei
     Cui, Fan Yang, Mao Yang, Lidong Zhou, Asaf Cidon, and Gennady Pekhimenko. 2022. ROLLER: Fast and Efficient
     Tensor Compilation for Deep Learning. In OSDI.
