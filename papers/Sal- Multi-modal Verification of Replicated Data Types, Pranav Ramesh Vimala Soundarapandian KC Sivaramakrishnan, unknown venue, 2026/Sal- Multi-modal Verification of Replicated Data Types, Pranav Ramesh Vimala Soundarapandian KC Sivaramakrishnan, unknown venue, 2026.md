                                         Sal: Multi-modal Verification of Replicated Data Types
                                                     Pranav Ramesh                       Vimala Soundarapandian                           KC Sivaramakrishnan
                                               Indian Institute of Technology,           Indian Institute of Technology,                Indian Institute of Technology,
                                                           Madras                                    Madras                                         Madras
                                                       Chennai, India                            Chennai, India                                 Chennai, India
                                                 cs22b015@smail.iitm.ac.in                 cs19d750@smail.iitm.ac.in                         kcsrk@cse.iitm.ac.in
                                         Abstract                                                             and Mergeable Replicated Data Types (MRDTs) [9] are widely
                                         Designing correct replicated data types (RDTs) is challenging        used to implement such replicated state. However, designing
                                         because replicas evolve independently and must be merged             correct RDTs is subtle. Even well-known designs such as
                                         while preserving application intent. A promising approach            Replicated Growable Arrays (RGA) [10] have had serious
                                                                                                              anomalies discovered after publication1 .
arXiv:2603.27202v1 [cs.PL] 28 Mar 2026




                                         is correct-by-construction development in a proof-oriented
                                         programming language such as F★, Dafny and Lean, where                  Replication-aware (RA) linearizability [21] provides a prin-
                                         desired correctness guarantees are specified and checked as          cipled correctness condition for CRDTs, relating replica exe-
                                         the RDTs are implemented. Recent work Neem [20] proposes             cutions to a sequential explanation of updates. Prior work,
                                         the use of replication-aware linearizability (RA linearizabil-       Neem [20], showed that RA linearizability can be extended to
                                         ity) [21] as the correctness condition for state-based CRDTs         MRDTs and also be reduced to a set of 24 verification condi-
                                         and mergeable replicated data types (MRDTs), with automa-            tions (VCs) amenable to automation. Neem implements this
                                         tion in the SMT-aided, proof-oriented programming lan-               approach in F★, an SMT-aided, proof-oriented programming
                                         guage F★. However, SMT-centric workflows can be opaque               language. Developers implement RDTs in F★ and leverage
                                         when automation fails to discharge a verification condition          SMT automation to discharge the RA-linearizability VCs au-
                                         (VC), and they enlarge the trusted computing base (TCB).             tomatically. In practice, however, SMT-centric verification
                                            We present Sal, a multi-modal workflow to design and              workflows can be difficult to iterate on. When automation
                                         verify state-based CRDTs and MRDTs in Lean. Sal com-                 fails, developers often get little actionable information be-
                                         bines (i) kernel-checkable automation with proof reconstruc-         yond an unproved VC, and debugging incorrect implemen-
                                         tion, (ii) SMT-aided automation when needed, and (iii) AI-           tations remains manual and time-consuming.
                                         assisted interactive theorem proving for remaining proof                This debugging experience contrasts sharply with ev-
                                         obligations. When a verification condition is shown to be            eryday software development, where programmers iterate
                                         invalid, we leverage Lean’s property-based testing to au-            quickly by writing code, running tests, inspecting failing
                                         tomatically generate and visualize counterexamples, help-            traces, and refining implementations. Understanding why
                                         ing developers debug incorrect specifications or implemen-           a particular VC fails requires a laborious “proof-debugging”
                                         tations. We report on our experience verifying a suite of            workflow: developers add intermediate assertions (assert)
                                         13 CRDTs and MRDTs with Sal: 69% of verification con-                or assumptions (admit) and progressively push them deeper
                                         ditions are discharged by kernel-verified automation with-           to localize the failing reasoning step. When the root cause
                                         out SMT, and counterexamples automatically expose sub-               is an unexpected interaction between definitions and the
                                         tle bugs such as the well-known enable-wins flag anomaly.            SMT encoding, additional tuning (e.g., controlling unfold-
                                         The codebase for Sal is open-sourced, and is available at            ing or solver limits) may be needed. Moreover, SMT-aided
                                         https://github.com/fplaunchpad/sal.                                  proofs can be brittle: small changes may cause previously
                                                                                                              discharged VCs to fail. Relying on an external SMT solver
                                         CCS Concepts: • Software and its engineering → Soft-                 also increases the trusted computing base.
                                         ware verification and validation; • Computing method-                   We present Sal, a verification workflow for RA-linearizability
                                         ologies → Distributed algorithms.                                    in Lean that addresses these issues by making failures ac-
                                         Keywords: CRDT, Verification, Lean, Multi-Modal Proofs,              tionable. At the core of Sal is a staged Lean tactic that pri-
                                         Counterexample Generation                                            oritizes proof reconstruction (e.g., simplifying goals and in-
                                                                                                              voking grind [13]) and falls back to SMT-aided automation
                                                                                                              (lean-blaster [8]) only when necessary. When a VC is false,
                                         1   Introduction                                                     Sal uses property-based testing (Plausible [14]) to automat-
                                         Local-first collaboration tools allow users to continue work-        ically synthesize small counterexamples and a ProofWid-
                                         ing while offline, synchronizing in the background when              gets [2]-based visualizer to render the corresponding exe-
                                         connectivity returns [11]. This programming model requires           cution trace, enabling a test-like debugging loop for RDT
                                         replicated data types whose states can evolve independently
                                         at each replica and later be merged without violating applica-       1 https://martin.kleppmann.com/2019/03/25/papoc-interleaving-

                                         tion intent. Conflict-Free Replicated Data Types (CRDTs) [19]        anomalies.html#errata
                                                                                                          1
Conference’17, July 2017, Washington, DC, USA                                                                                   Ramesh et al.


verification. In our evaluation over a suite of CRDTs and                 An observed-removed set (OR-set) MRDT [9] is defined as
MRDTs, Sal discharges most VCs without SMT and auto-                      follows:
matically rediscovers subtle bugs such as the well-known                      • Σ = P (T × 𝐸) where 𝐸 is the set of elements with
enable-wins flag anomaly (Table 2).                                              𝜎0 = ∅
  This paper makes the following contributions:                               • 𝑂 = {add𝑒 , rem𝑒 |𝑒 ∈ 𝐸}
   1. A Lean formalization of RA-linearizability VCs for a                    • do(𝜎, 𝑡, _, add𝑒 ) = 𝜎 ∪ {(𝑒, 𝑡)}
       suite of state-based CRDTs and MRDTs.                                  • do(𝜎, _, _, rem𝑒 ) = 𝜎 \ {(𝑒, 𝑖)|(𝑒, 𝑖) ∈ 𝜎 }
   2. A counterexample-generation and visualization work-                     • merge(𝜎𝑙𝑐𝑎 , 𝜎1, 𝜎2 ) = (𝜎𝑙𝑐𝑎 ∩𝜎1 ∩𝜎2 ) ∪ (𝜎1 \𝜎𝑙𝑐𝑎 ) ∪ (𝜎2 \
       flow for failing VCs, based on property-based testing                     𝜎𝑙𝑐𝑎 ) – the merged state contains elements common to
       in Lean.                                                                  all three versions (unchanged elements remain; deleted
   3. Sal, a custom tactic that attempts proof reconstruction-                   elements are not included), as well as elements added
       based automation first, falls back to SMT-aided automa-                   in either version since the LCA.
       tion, and uses AI-assisted interactive theorem proving                 • rc = {(rem𝑒 , add𝑒 )|𝑒 ∈ 𝐸} – remove is ordered before
       as a last resort.                                                         add for the same element, and hence, adds win over
   4. An evaluation across a suite of CRDTs and MRDTs,                           concurrent removes.
       including cases where counterexamples expose subtle                   We verify RDT correctness using replication-aware (RA)
       bugs (Table 2).                                                    linearizability [21], which makes merge semantics explicit
                                                                          while retaining a linearizability-style reading. Neem [20]
2    Background                                                           reduces RA linearizability for MRDTs and state-based CRDTs
We assume familiarity with replicated data types and focus                to a finite set of verification conditions (VCs) over do, merge,
on the specific models and specifications used in this paper.             and rc. Sal focuses on discharging these VCs effectively and
State-based CRDTs reconcile replicas via a deterministic                  on producing actionable feedback when automation fails.
two-way merge 𝜇 (𝑣 1, 𝑣 2 ); a common sufficient condition for               Lean 4 [17] is a theorem prover and functional program-
convergence is that the merge function 𝜇 is the join of a                 ming language with a small trusted kernel; proofs can be
semilattice.                                                              checked as proof terms by the kernel. Lean’s metaprogram-
   Mergeable Replicated Data Types (MRDTs) [9] avoid em-                  ming support enables custom tactics and domain-specific
bedding causal metadata in the state of the RDT. Instead,                 automation, which is useful for VC-heavy developments like
they assume a versioned storage model (e.g., Git-like histo-              ours.
ries) that can provide the lowest common ancestor (LCA)                      Lean offers several automation techniques with different
for a three-way merge. This interface often yields compact                tradeoffs. We rely on the following:
implementations: for example, a counter MRDT can be 𝑂 (1),                    • dsimp and aesop: simplification and proof search for
whereas state-based counter CRDTs require Ω(𝑛) space in                          routine goals.
the number of replicas [3].                                                   • grind [13]: SMT-style automation with proof recon-
   Formally, an MRDT implementation for a data type 𝜏 [20]                       struction, producing kernel-checkable proof terms.
is a tuple D𝜏 = ⟨Σ, 𝜎0, do, merge, rc⟩, where:                                • lean-blaster [8]: an SMT backend (Z3) that is effec-
     • Σ is the set of states, 𝜎0 ∈ Σ is the initial state.                      tive on many VCs (notably those with lambdas), but
     • do : Σ×T ×R ×𝑂𝜏 → Σ implements update operations                          without proof reconstruction; it therefore enlarges the
       parameterized by timestamp in T , replica id in R and                     trusted computing base.
       operations in 𝑂𝜏 .                                                    Sal stages automation accordingly: we first attempt re-
     • merge : Σ × Σ × Σ → Σ is a three-way merge function.               constructible automation and only fall back to SMT when
     • rc ⊆ 𝑂𝜏 × 𝑂𝜏 is the conflict resolution policy to be               needed.
       followed for concurrent conflicting update operations.
       The relation is interpreted as a partial order where               3     Sal framework
       (𝑜 1, 𝑜 2 ) ∈ rc means that 𝑜 1 is ordered before 𝑜 2 .            In this section, we describe the Sal multi-modal verification
   For example, the increment-only counter MRDT is defined                framework for RA-linearizability in Lean. We start with the
as follows:                                                               challenge of designing data structures conducive to auto-
     • Σ = N with 𝜎0 = 0                                                  mated verification in Lean.
     • 𝑂 = {inc}
     • do(𝜎, _, _, inc) = 𝜎 + 1                                           3.1   Data structures for automated verification
     • merge(𝜎𝑙𝑐𝑎 , 𝜎1, 𝜎2 ) = 𝜎𝑙𝑐𝑎 + (𝜎1 − 𝜎𝑙𝑐𝑎 ) + (𝜎2 − 𝜎𝑙𝑐𝑎 ) –       Many RDTs rely fundamentally on sets and maps. For ex-
       the merged state is the sum of the states of the LCA and           ample, the OR-set MRDT maintains a set of timestamped
       the difference between the LCA and the two versions.               elements; map-based MRDTs and CRDTs require reasoning
     • rc = ∅ – no conflicting operations.                                about extensional equality of mappings. However, Lean’s
                                                                      2
Sal : Multi-modal Verification of Replicated Data Types                                        Conference’17, July 2017, Washington, DC, USA


standard library provides data structures optimized for dif-          abbrev concrete_st := Int × Bool
ferent purposes: the mathematical Set type uses propositions          inductive app_op_t : Type where
(𝛼 → Prop) suitable for manual proofs, while computational            | Enable
maps like RBMap and HashMap emphasize efficient itera-                | Disable
tion but complicate extensional reasoning.                            abbrev op_t:= N × N × app_op_t
   For automated verification, we use decidable representa-             /-timestamp, rid, operation-/
tions that tools like grind can reason about effectively. We          def do_ (s:concrete_st) (o: op_t) : concrete_st
therefore implement custom set and map interfaces inspired            := match o with
by F★’s verification-oriented designs. Our sets use boolean-          | (_, (_, .Enable)) => (Prod.fst s + 1, true)
valued membership functions rather than propositions, since           | (_, (_, .Disable)) => (Prod.fst s, false)
they typically contain datatypes where equality is decidable.         def merge_flag (l a b: concrete_st) :=
abbrev set (a:Type) [DecidableEq a] := a → Bool                         if Prod.snd a && Prod.snd b then true
                                                                        else if not (Prod.snd a) && not (Prod.snd b) then
   This representation is decidable by construction: since                false
membership returns a boolean, automation can directly com-              else if Prod.snd a then Prod.fst a > Prod.fst l
pute and compare set operations without requiring proof                 else Prod.fst b > Prod.fst l
objects to reason about decidability. We require DecidableEq          def merge (l a b: concrete_st) : concrete_st
for element types, ensuring all operations remain computable.         := (Prod.fst a + Prod.fst b - Prod.fst l ,
This is a natural condition which is satisfied across the RDTs            merge_flag l a b)
we verify with this framework.
   Similarly, our map interface makes the domain explicit to
                                                                       Figure 1. Buggy enable-wins flag MRDT implementation
enable extensional reasoning:
structure map (key:Type) [DecidableEq key]                                                                    𝑣"
    (value:Type) where                                                                                       (0,F)
  mappings: key → value                                                            𝑒!: (1, r!, enable)               𝑒#: (2, r# , enable)

  domain: set key                                                                         𝑣!    (1,T)                (1,T)    𝑣#



                                                                                                         LC
   Two maps are equal when their domains and mappings                          𝑒&: (3, r!, disable)                      𝑒$: (4, r#, disable)


                                                                                                           A=
                                                                                                             (0,
agree. Since the mapping is restricted to the domain key
                                                                                                                F)
                                                                                          𝑣&    (1,F)                 (1,F)   𝑣$
which supports decidable equality, the map supports exten-                                               LC

sional equality.
                                                                                                           A=
                                                                                                             (1,
                                                                                                                T)


   Critically, we annotate all definitions and lemmas with                                                            (2,T)    𝑣'
@[simp, grind] attributes and provide grind_pattern hints.
This builds a domain-specific rewrite database: when grind
encounters goals involving set membership, union, or map                                                              (2,T)   𝑣(
selection, it automatically applies the appropriate lemmas
without manual guidance. These annotations trade the gener-           Figure 2. An enable-wins flag execution: both replicas see
ality of Lean’s standard library for automation-friendliness,         a disable at the end, yet merging produces (2, true) at 𝑣 6 ,
enabling grind to discharge most VCs involving sets and               incorrectly reporting the flag as enabled.
maps without SMT assistance (Table 2). This is analogous to
SMT patterns in F★.
                                                                         We demonstrate this approach using the enable-wins flag
3.2   Counterexample generation in Lean                               MRDT, a shared boolean flag that represents a disabled or
When a VC fails during verification, understanding why it             enabled state. The desired specification is that in the case of
failed is critical for debugging. In SMT-centric workflows            concurrent enable and disable operations, the enable wins.
                                                                                                       rc
like F★, a failed VC provides little actionable feedback: de-         This is expressed as disable −  → enable, meaning that when
velopers must manually construct execution traces, add in-            we read a replica’s state, the flag should be true if there exists
termediate assertions, and progressively narrow down the              an enable operation that is not causally preceded by a disable.
source of the failure. This process is labor-intensive and re-           Consider the enable-wins flag implementation in Figure 1,
quires significant expertise. In contrast, Sal leverages Lean’s       which tracks the number of concurrent enables using a
property-based testing framework, Plausible [14], to auto-            counter and uses this counter to determine the flag’s state
matically generate concrete counterexamples when VCs fail,            after merging. This implementation contains a subtle bug.
transforming opaque proof failures into tangible test cases           The bug manifests in executions where enable operations
that developers can inspect and debug.                                are followed by disables on each replica, yet the merged
                                                                  3
Conference’17, July 2017, Washington, DC, USA                                                                                          Ramesh et al.


state incorrectly reports the flag as enabled. Figure 2 shows
such an execution: when merging 𝑣 3 and 𝑣 5 (with LCA 𝑣 1 ),
the counter value of 𝑣 5 exceeds 𝑣 1 , causing merge_flag to
compute the new flag to be true in 𝑣 6 . However, all enable
events in this execution are subsequently disabled on their
respective replicas, violating the enable-wins specification!
When verifying the RA-linearizability VCs, one of the VCs
fails. However, finding such counterexamples manually is
challenging, particularly for more complex RDTs with larger
state spaces.
   To automate counterexample discovery, we leverage Plau-
sible [14], a property-based testing tool for Lean inspired by
QuickCheck [4]. Plausible requires that VCs be expressed
as decidable propositions – that is, properties that can be
algorithmically evaluated to true or false. Once decidability
is established, Plausible generates random test inputs and
checks whether they satisfy the VC. When a violation is
found, Plausible reports the failing input, such as:
postcondition violated for input
(disable, (enable, (enable, (disable, (0, false)))))
                                                                                                 (a)                             (b)
   While this output identifies a counterexample, diagnosing
the cause of the failure is difficult. To address this, we imple-
                                                                                  Figure 3. Visualization for the failed VC for the buggy enable-
ment an execution trace visualizer using Lean’s ProofWid-
                                                                                  wins flag in Figure 1.
gets framework [2]. The visualizer instruments the do and
merge operations to record intermediate states and opera-
tions, producing a step-by-step execution trace.                                  the bug arises from the counter-based merge logic failing
   Sal, like Neem [20], includes VCs that check whether                           to account for subsequent disables. This visualization trans-
concurrent executions can be RA-linearized to the same final                      forms the abstract VC failure into a concrete debugging sce-
state. This is achieved using bottom-up linearization, where                      nario, analogous to examining a failing unit test trace in
we peel off events in a bottom-up manner to construct a                           conventional software development.
linearization order. In the failed VC, we attempt to prove:                          The combination of automatic counterexample genera-
                                                                                  tion and interactive visualization significantly accelerates
            𝑣1                  𝑣3                         𝑣5                     the debugging workflow. Instead of manually inspecting
      z }| { z                  }|       { z               }|         {          failed VCs and constructing hypothetical execution traces,
  𝜇 𝑒 1 (0, 𝑓 𝑎𝑙𝑠𝑒), 𝑒 3 (𝑒 1 (0, 𝑓 𝑎𝑙𝑠𝑒)), 𝑒 1 (𝑒 4 (𝑒 2 (0, 𝑓 𝑎𝑙𝑠𝑒))) =         developers receive concrete, visualizable counterexamples
                                                                          
   𝑒 3 𝜇 (𝑒 1 (0, 𝑓 𝑎𝑙𝑠𝑒), 𝑒 1 (0, 𝑓 𝑎𝑙𝑠𝑒), 𝑒 1 (𝑒 4 (𝑒 2 (0, 𝑓 𝑎𝑙𝑠𝑒))) )         automatically. This approach also complements the multi-
          | {z } | {z } |                                 {z         }            modal proof strategy: when grind or lean-blaster fail to
                 𝑣1               𝑣1                       𝑣5                     discharge a VC, Plausible can quickly determine whether the
where 𝜇 is the merge operation, 𝑒 1 . . . 𝑒 4 are events, and each                failure stems from an incorrect implementation (producing a
tuple (Int × Bool) constitutes a state. The state at 𝑣 6 in Fig-                  counterexample) or requires manual interactive proof (when
ure 2 is obtained by merging 𝑣 3 and 𝑣 5 , with 𝑣 1 as LCA. This                  no counterexample exists).
corresponds to the LHS of the VC. This state should match
the state obtained by first merging 𝑣 1 and 𝑣 5 , with 𝑣 1 as LCA,                3.3   Visualizing functional sets
and then applying 𝑒 3 , through bottom-up linearization.                          While the enable-wins flag uses simple concrete types (inte-
   Figure 3 illustrates the visualization for the enable-wins                     gers and booleans), many RDTs are set-based. Our custom
flag that violates this VC. The states and operations are                         sets (Section 3.1), designed as functional predicates a → Bool
shown in blue and yellow boxes, respectively, and corre-                          for verification, pose a visualization challenge: they are ab-
spond to concrete_st and op_t, respectively, from Figure 1.                       stract, infinite by nature, and do not support iteration or
The LCA trace and state is shown at the top. In both cases,                       enumeration. Yet both counterexample debugging and gen-
the LCA state is 𝑣 1 . The left panel (a) shows the execution                     eral trace inspection require displaying actual set contents
trace for the LHS, which evaluates to (2, true), and the right                    as concrete element lists.
panel (b) shows the RHS, which evaluates to (2, false). By                           To bridge this gap, we implement a universe tracking
comparing these traces, developers can quickly identify that                      mechanism. During execution, we maintain a finite HashSet
                                                                              4
Sal : Multi-modal Verification of Replicated Data Types                                    Conference’17, July 2017, Washington, DC, USA


                                                                         2. lean-blaster (LB) – When DG fails, lean-blaster
                                                                            encodes the goal to Z3. While more powerful for VCs
                                                                            with higher-order functions and lambdas, this sacri-
                                                                            fices proof reconstruction and enlarges the TCB. We
                                                                            select it over Lean-SMT [16] and Lean-Auto [18] for
                                                                            its superior support for higher-order functions.
                                                                         3. ITP – When both DG and LB fail, we discharge the re-
                                                                            maining proof goals using Aristotle [1], an AI-assisted
                                                                            proof search tool. Aristotle generates kernel-checkable
                                                                            Lean proofs via extensive automated search. Unlike
                                                                            lean-blaster, the generated proofs are verified by Lean’s
Figure 4. OR-set execution visualized using ProofWidgets                    kernel, preserving the TCB.
                                                                        In order to prevent runaway automation, the Sal tac-
                                                                     tic incorporates a heartbeat-based timeout mechanism that
of all elements that have been added or removed. When
                                                                     bounds the execution time of the first two stages. When a
visualizing the set state, we only check membership for ele-
                                                                     timeout expires, control returns to the user, allowing them
ments in this finite universe, which suffices to characterize
                                                                     to either increase the limit or proceed directly to interactive
the set’s observable behavior. The implementation augments
                                                                     proving, either using Aristotle, or by hand using custom
our abstract sets with a concrete universe:
                                                                     tactics.
structure set_with_universe (𝛼: Type) [ToString 𝛼]
    [DecidableEq 𝛼] [Hashable 𝛼] where
                                                                     4    Evaluation
  _set : set 𝛼
  _universe : HashSet 𝛼                                              Table 1 compares F★ and Lean across several dimensions rel-
                                                                     evant to RDT verification. Lean’s rich tactic system enables
   Figure 4 demonstrates this approach on an OR-set execu-           the multi-modal workflow central to Sal, while built-in coun-
tion with concurrent add and remove operations on element            terexample generation (Plausible) and proof reconstruction
3. The visualization shows concrete set states using the nota-       support actionable debugging and reduced TCB. However,
tion #[(1, 3)]#, where the tuple contains the timestamp and          Lean’s standard library data structures are designed for math-
element. The left branch removes element 3 (resulting in the         ematical reasoning rather than automation, necessitating the
empty set #[]#), while the right branch adds element 3 (re-          custom sets and maps described in Section 3.1.
sulting in #[(1, 3)]#). Both branches converge to #[(1, 3)]#,           Table 2 shows the results of verifying 13 RDTs (311 VCs
confirming that adds win over concurrent removes as spec-            in total) using Sal. Across all benchmarks, 215 VCs (69.1%)
ified. Operations are displayed in yellow boxes, and users           are discharged by dsimp+grind, a lightweight tactic with
provide operation labels via format strings.                         proof reconstruction verified by Lean’s kernel. An additional
   This mechanism works uniformly for both correct execu-            87 VCs (28.0%) require lean-blaster (SMT-based), and only 9
tions and counterexamples, enabling developers to inspect            VCs (2.9%) fall back to interactive proving. This demonstrates
set-based RDT behavior regardless of whether they are de-            that the majority of RA-linearizability VCs can be verified
bugging a failed VC or validating a correct implementation.          without enlarging the TCB through SMT solvers.
                                                                        We observe notable differences between CRDTs and MRDTs.
3.4   Multi-modal proofs using the Sal tactic
                                                                     MRDTs generally require less SMT than CRDTs due to their
The Sal tactic orchestrates a staged proof strategy that             simpler three-way merge; for example, PN-counter MRDT
adapts to VC complexity. As described in Section 2, Lean pro-        needs no lean-blaster while PN-counter CRDT requires it for
vides multiple automation techniques with different trade-           2 VCs plus 6 interactive proofs. The 9 interactive proofs arise
offs between power, trust, and performance. The Sal tactic           predominantly in CRDTs (7 of 9), where the merge function
attempts these approaches sequentially, prioritizing proof           tends to involve more complex reasoning than three-way
reconstruction before falling back to more powerful but less         MRDT merges. Total verification times range from under
trustworthy methods.                                                 a second for simple RDTs (e.g., grows-only set) to around
   The tactic proceeds in the following stages:                      100 seconds for PN-counter CRDT, where the 6 ITP goals
    1. dsimp + grind (DG) – This combination applies sim-            discharged by Aristotle dominate the total time.
       plification followed by grind’s SMT-style automation             The enable-wins flag MRDT demonstrates the value of
       with proof reconstruction, producing kernel-checkable         counterexample generation. This implementation contains
       proof terms while maintaining the smallest TCB. We            a known bug from prior work [20]; when the correspond-
       exclude aesop [15] due to prohibitively high verifica-        ing VC fails, Plausible automatically generates a concrete
       tion times on RDT VCs.                                        counterexample, which our ProofWidgets-based visualizer
                                                                 5
Conference’17, July 2017, Washington, DC, USA                                                                            Ramesh et al.


                                  Table 1. Comparing F★ and Lean for verifying RA Linearizability

 Criterion              F★                                                      Lean
 Automation             Direct SMT solving via Z3. Automation often works       Multiple tactic-based tools (aesop, grind,
                        out of the box at scale.                                lean-blaster), less effective on large proof
                                                                                goals.
 Multi-Modal            Limited tactic system; most proofs require SMT Rich tactic system allows combining automated and
 Proofs                 solver.                                        interactive proving.
 Counterexamples No counterexample generation; reports only success             Plausible generates counterexamples for decidable
                 or failure.                                                    properties.
 Data Structures        Rich set and map libraries designed for verification.   Mathematical data structures; custom sets and maps
                                                                                needed for automation (Section 3.1).
 Trustworthiness        No proof reconstruction; relies on trusting Z3.         Proof reconstruction for most tools; kernel verifies
                                                                                proofs. Uncertified proofs marked sorry.

Table 2. Number of VCs discharged by the Sal tactic (total               CRDT verification. Several approaches verify CRDT cor-
VCs = 24 per RDT). DG refers to dsimp + grind, and LB refers          rectness. Isabelle/HOL has been used to verify strong even-
to lean − blaster. Time reports the average total wall-clock          tual consistency [7], but requires substantial manual proof
time for all stages including ITP via Aristotle. # Contains           effort. Neem [20] automates RA-linearizability verification
known bug; counterexample automatically generated (Sec-               in F★ using SMT solvers, achieving high automation but
tion 3.2).                                                            at the cost of an enlarged TCB and opaque failures. Ver-
                                                                      ifx [5] provides a specialized language for RDTs with built-in
    RDT                              DG     LB   ITP   Time (s)       verification, trading generality for domain-specific automa-
    Increment-only counter MRDT       24    0     0       0.7         tion. It also supports automated counterexample generation
    PN-counter MRDT                   24    0     0       2.7         in the context of RDT verification. Sal distinguishes itself
    OR-set MRDT                        3    21    0      17.3         through kernel-verified automation (69% of VCs discharged
    Enable-wins flag MRDT #            9    14    0      34.2         by proof reconstruction), automated counterexample gener-
    Efficient OR-set MRDT              2    22    0      14.4
                                                                      ation when verification fails, and interactive visualization of
    Grows-only set MRDT               24    0     0       0.3
    Grows-only map MRDT               22    0     2      25.8         execution traces–capabilities not present together in prior
    Replicated growable array MRDT    15    9     0       3.9         CRDT verification tools.
    Multi-valued register MRDT        24    0     0       0.3            Counterexample generation. Property-based testing
    Increment-only counter CRDT       24    0     0       1.5         tools like QuickCheck [4], QuickChick [12] (Coq), and Plau-
    PN-counter CRDT                   16    2     6      99.5
                                                                      sible (Lean) generate test inputs for executable properties.
    Multi-valued register CRDT        24    0     0       0.7
    OR-set CRDT                        4    19    1      34.7         Sal leverages Plausible for decidable VCs, but extends it
                                                                      with domain-specific visualization for RDT execution traces,
                                                                      including handling of functional set representations through
                                                                      universe tracking (Section 3.3). This bridges property test-
                                                                      ing and formal verification, transforming failed VCs into
renders for inspection (Figure 3). This workflow transforms
                                                                      debuggable counterexamples.
opaque VC failures into actionable debugging scenarios.

5    Related work
Multi-modal verification. Loom [6] is a recent work on                6   Conclusion
multi-modal verification for data structures in Lean, using           We present Sal, a multi-modal verification framework for
Dijkstra Monads to model effectful operations on mutable              replicated data types in Lean that addresses key limitations of
arrays and counters. Sal adapts this multi-modal approach             SMT-centric verification workflows. By staging automation–
to RDT verification in Lean, but leverages conventional tac-          prioritizing kernel-verified proof reconstruction via grind,
tics rather than monadic effects since RDTs are monotonic             falling back to SMT-based lean-blaster, and using AI-
and non-mutable. Unlike Loom’s focus on sequential data               assisted interactive theorem proving via Aristotle [1] for
structures, Sal targets the unique challenges of replicated           remaining obligations–Sal achieves 69% kernel-verified au-
systems with merge operations and causal reasoning.                   tomation across 13 CRDTs and MRDTs while minimizing
                                                                  6
Sal : Multi-modal Verification of Replicated Data Types                                                           Conference’17, July 2017, Washington, DC, USA


the trusted computing base. When automation fails, auto-                                    7 pages. doi:10.1145/3301419.3323972
mated counterexample generation via Plausible and interac-                             [11] Martin Kleppmann, Adam Wiggins, Peter van Hardenberg, and Mark
tive visualization through ProofWidgets transform opaque                                    McGranaghan. 2019. Local-first software: you own your data, in
                                                                                            spite of the cloud. In Proceedings of the 2019 ACM SIGPLAN Inter-
proof failures into actionable debugging scenarios, as demon-                               national Symposium on New Ideas, New Paradigms, and Reflections
strated by rediscovering the enable-wins flag bug.                                          on Programming and Software (Athens, Greece) (Onward! 2019). As-
   Our experience reveals patterns in RDT verification: MRDTs                               sociation for Computing Machinery, New York, NY, USA, 154–178.
generally require less SMT than CRDTs due to simpler three-                                 doi:10.1145/3359591.3359737
way merge, and map-based reasoning remains more challeng-                              [12] Leonidas Lampropoulos, Michael Hicks, and Benjamin C. Pierce. 2019.
                                                                                            Coverage guided, property based testing. Proc. ACM Program. Lang. 3,
ing than set-based reasoning for current Lean automation.                                   OOPSLA, Article 181 (Oct. 2019), 29 pages. doi:10.1145/3360607
Future work includes extending our custom data structure li-                           [13] Lean Community. 2024. The grind tactic. Lean 4 Reference Manual.
brary to improve map automation, developing optimizations                                   https://lean-lang.org/doc/reference/latest/The--grind--tactic/
for the staged tactic based on VC patterns, and evaluating                             [14] Lean Community. 2024. Plausible: A counterexample generator for
Sal on larger-scale RDT developments.                                                       Lean 4. Lean Reservoir. https://reservoir.lean-lang.org/@leanprover-
                                                                                            community/plausible
                                                                                       [15] Jannis Limperg and Asta Halkjær From. 2023. Aesop: White-Box Best-
References                                                                                  First Proof Search for Lean. In Proceedings of the 12th ACM SIGPLAN
                                                                                            International Conference on Certified Programs and Proofs (Boston, MA,
 [1] Tudor Achim, Alex Best, Alberto Bietti, Kevin Der, Mathïs Fédérico,                    USA) (CPP 2023). Association for Computing Machinery, New York,
     Sergei Gukov, Daniel Halpern-Leistner, Kirsten Henningsgard, Yury                      NY, USA, 253–266. doi:10.1145/3573105.3575671
     Kudryashov, Alexander Meiburg, Martin Michelsen, Riley Patter-                    [16] Abdalrhman Mohamed, Tomaz Mascarenhas, Harun Khan, Haniel
     son, Eric Rodriguez, Laura Scharff, Vikram Shanker, Vladmir Sicca,                     Barbosa, Andrew Reynolds, Yicheng Qian, Cesare Tinelli, and Clark
     Hari Sowrirajan, Aidan Swope, Matyas Tamas, Vlad Tenev, Jonathan                       Barrett. 2025. lean-smt: An SMT Tactic for Discharging Proof Goals
     Thomm, Harold Williams, and Lawrence Wu. 2025. Aristotle: IMO-                         in Lean. In Computer Aided Verification: 37th International Conference,
     level Automated Theorem Proving. arXiv:2510.01346 [cs.AI] https:                       CAV 2025, Zagreb, Croatia, July 23-25, 2025, Proceedings, Part III (Zagreb,
     //arxiv.org/abs/2510.01346                                                             Croatia). Springer-Verlag, Berlin, Heidelberg, 197–212. doi:10.1007/
 [2] Edward W. Ayers, Mateja Jamnik, and W. T. Gowers. 2021. A Graphical                    978-3-031-98682-6_11
     User Interface Framework for Formal Verification. In 12th International           [17] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 The-
     Conference on Interactive Theorem Proving (ITP 2021) (Leibniz Interna-                 orem Prover and Programming Language. In Automated Deduction
     tional Proceedings in Informatics (LIPIcs), Vol. 193), Liron Cohen and                 – CADE 28: 28th International Conference on Automated Deduction,
     Cezary Kaliszyk (Eds.). Schloss Dagstuhl – Leibniz-Zentrum für Infor-                  Virtual Event, July 12–15, 2021, Proceedings. Springer-Verlag, Berlin,
     matik, Dagstuhl, Germany, 4:1–4:16. doi:10.4230/LIPIcs.ITP.2021.4                      Heidelberg, 625–635. doi:10.1007/978-3-030-79876-5_37
 [3] Sebastian Burckhardt, Alexey Gotsman, Hongseok Yang, and Marek                    [18] Yicheng Qian, Joshua Clune, Clark Barrett, and Jeremy Avigad. 2025.
     Zawirski. 2014. Replicated data types: specification, verification, opti-              Lean-Auto: An Interface Between Lean 4 and Automated Theorem
     mality. SIGPLAN Not. 49, 1 (Jan. 2014), 271–284. doi:10.1145/2578855.                  Provers. In Computer Aided Verification, Ruzica Piskac and Zvonimir
     2535848                                                                                Rakamarić (Eds.). Springer Nature Switzerland, Cham, 175–196.
 [4] Koen Claessen and John Hughes. 2000. QuickCheck: a lightweight                    [19] Marc Shapiro, Nuno Preguiça, Carlos Baquero, and Marek Zawirski.
     tool for random testing of Haskell programs. SIGPLAN Not. 35, 9 (Sept.                 2011. Conflict-Free Replicated Data Types. In Stabilization, Safety,
     2000), 268–279. doi:10.1145/357766.351266                                              and Security of Distributed Systems, Xavier Défago, Franck Petit, and
 [5] Kevin De Porre, Carla Ferreira, and Elisa Gonzalez Boix. 2023. VeriFx:                 Vincent Villain (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,
     Correct Replicated Data Types for the Masses. In 37th European Confer-                 386–400.
     ence on Object-Oriented Programming (ECOOP 2023) (Leibniz Interna-
                                                                                       [20] Vimala Soundarapandian, Kartik Nagar, Aseem Rastogi, and KC Sivara-
     tional Proceedings in Informatics (LIPIcs), Vol. 263), Karim Ali and Guido             makrishnan. 2025. Automatically Verifying Replication-Aware Lin-
     Salvaneschi (Eds.). Schloss Dagstuhl – Leibniz-Zentrum für Informatik,                 earizability. Proc. ACM Program. Lang. 9, OOPSLA1, Article 111 (April
     Dagstuhl, Germany, 9:1–9:45. doi:10.4230/LIPIcs.ECOOP.2023.9                           2025), 27 pages. doi:10.1145/3720452
 [6] Vladimir Gladshtein, George Pîrlea, Qiyuan Zhao, Vitaly Kurin, and                [21] Chao Wang, Constantin Enea, Suha Orhun Mutluergil, and Gustavo
     Ilya Sergey. 2026. Foundational Multi-Modal Program Verifiers. Proc.                   Petri. 2019. Replication-aware linearizability. In Proceedings of the
     ACM Program. Lang. 10, POPL, Article 77 (Jan. 2026), 32 pages. doi:10.                 40th ACM SIGPLAN Conference on Programming Language Design
     1145/3776719                                                                           and Implementation (Phoenix, AZ, USA) (PLDI 2019). Association for
 [7] Victor B. F. Gomes, Martin Kleppmann, Dominic P. Mulligan, and                         Computing Machinery, New York, NY, USA, 980–993. doi:10.1145/
     Alastair R. Beresford. 2017. Verifying strong eventual consistency in                  3314221.3314617
     distributed systems. Proc. ACM Program. Lang. 1, OOPSLA, Article
     109 (Oct. 2017), 28 pages. doi:10.1145/3133933
 [8] Input Output Global. 2024. Lean-blaster: An SMT-based proof automa-
     tion tactic for Lean 4. GitHub repository. https://github.com/input-
     output-hk/Lean-blaster
 [9] Gowtham Kaki, Swarn Priya, KC Sivaramakrishnan, and Suresh Jagan-
     nathan. 2019. Mergeable replicated data types. Proc. ACM Program.
     Lang. 3, OOPSLA, Article 154 (Oct. 2019), 29 pages. doi:10.1145/3360580
[10] Martin Kleppmann, Victor B. F. Gomes, Dominic P. Mulligan, and
     Alastair R. Beresford. 2019. Interleaving anomalies in collaborative
     text editors. In Proceedings of the 6th Workshop on Principles and Practice
     of Consistency for Distributed Data (Dresden, Germany) (PaPoC ’19).
     Association for Computing Machinery, New York, NY, USA, Article 6,
                                                                                   7
