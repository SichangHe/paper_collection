                                                    täkōFormal: Enabling Robust Software for
                                                         Programmable Memory Hierarchies
                                                                 (Extended Version)
                                                                     Pranav Srinivasan        Manos Kapritsos      Yatin A. Manerkar
                                                                                            University of Michigan
                                                                                  {pransrin, manosk, manerkar}@umich.edu


                                           Abstract—Accelerators provide large performance and energy-                Core                 Cache                 Memory
arXiv:2605.04172v1 [cs.AR] 5 May 2026




                                        efficiency benefits, but can significantly change the hardware-                        Load                       Miss
                                        software interface. The täkō programmable memory hierarchy                                    Normal Data
                                        accelerates data movement by enabling programmers to run user-                                                    Data




                                                                                                                    App Code
                                                                                                                               Load
                                        defined callback functions triggered by cache misses, evictions,                               Phantom Data
                                        and writebacks. However, it also leads to drastically increased
                                        complexity and counterintuitive outcomes. In response, we de-
                                        velop an ISA-level memory consistency model (MCM) for täkō                                    täkō             de
                                                                                                                                        Engine          Co     OnMiss()
                                        that captures the semantics of its operation, and we show how                                               p
                                                                                                                                                  Ap
                                        it enables programmers to formally reason about their täkō
                                        programs. We also prove the soundness of this ISA-level MCM by
                                        constructing a detailed täkō implementation model and verifying   Fig. 1: Image and caption from [55] showing the organization
                                        that all executions of the implementation model are allowed         of a täkō program. An application registers an address range
                                        by our ISA-level MCM. Along the way, we discover useful             whose semantics are defined by software callbacks. These
                                        insights about microarchitectural modeling and verification that    callbacks run in-cache on programmable engines.
                                        are applicable to hardware in general.
                                           This is the extended version of the ISCA 2026 paper
                                        “täkōFormal: Enabling Robust Software for Programmable            than the accelerator-rich landscape of today. Furthermore, the
                                        Memory Hierarchies”. This version adds material on additional       accelerator design space is so rich and varied that one cannot
                                        litmus tests to Section V to further explore the programmability    create a single effective methodology for formally specifying
                                        of täkō using our ISA-level MCM.                                  and verifying all possible accelerators. Still, architects and
                                           Index Terms—memory consistency models, programmable              formal methods experts must work together to develop new
                                        memory hierarchies, formal verification, computer architecture.
                                                                                                            techniques for modeling and verifying classes of accelerators
                                                                                                            that have not been previously studied.
                                                              I. I NTRODUCTION
                                                                                                               In this work, we focus on developing a verified formal
                                           With the end of Moore’s Law, hardware innovation has             hardware-software interface for the täkō [55] programmable
                                        moved towards increasing performance via accelerator-level          memory hierarchy (PMH). Figure 1 shows täkō’s high-level
                                        parallelism [19]. Innovation in this direction involves hardware    operation: users can write callbacks that run on cache misses,
                                        and software changes that provide significant performance and       evictions, and writebacks. These callbacks give the user in-
                                        energy-efficiency gains.                                            creased control over data movement, enabling various perfor-
                                           These benefits come with new challenges. Accelerators            mance and energy-efficiency benefits.
                                        today have various shapes and sizes, and often change the              We chose to formally model and verify täkō for multiple
                                        hardware-software interface [22, 55, 61]. These changes make        reasons. Firstly, täkō fundamentally changes the hardware-
                                        it difficult for non-experts to understand, program, and verify     software interface. In addition to its callbacks triggered by
                                        such systems. Precisely defining a hardware-software interface      cache events, it supports phantom addresses which are not
                                        and verifying implementations against it is essential. In the       backed by main memory. These features lead to complicated
                                        past, a lack of careful reasoning about this interface has led      executions and counterintuitive program outcomes, requiring
                                        to critical vulnerabilities, unintuitive program outcomes, and      programmers to understand the intricacies of the memory
                                        design specification ambiguities [7, 24, 28, 41, 60].               hierarchy (e.g., details of prefetching and replacement policies)
                                           Formal methods have been used to define hardware-software        to understand how their programs will behave. This complexity
                                        interface specifications for traditional architectures for many     makes täkō a challenging and worthwhile case study for formal
                                        years [5, 49, 52, 53], as well as to verify hardware implementa-    methods. Secondly, täkō is intended to be a general-purpose
                                        tions against such specifications [10, 11, 39]. However, barring    accelerator. The täkō paper shows how täkō can be used to
                                        a few exceptions (e.g., [6, 57, 58]), most formal methods work      improve the performance and energy efficiency of a diverse
                                        still assumes a traditional view of the computing stack rather      set of workloads, including graph traversals, scatter-updates,
                     Core 0          [x].OnMiss                      MCM for an architecture also enables proving correctness of
                 (i1) [x] ← 1        (i3) [x] ← 2                    compilation to that architecture, as well as program synthe-
                 (i2) r1 ← [x]                                       sis [16] (code generation with correctness guarantees) for that
                                                                     architecture. Defining the MCM of an architecture like täkō
                               (a)
                                                                     requires reasoning beyond what is used in traditional systems,
                 Core 0                  [x].OnMiss                  because conventional MCMs have no notion of phantom
         (1) [x] misses in cache                                     addresses or cache-event-triggered callbacks.
                                       (2) (i3)1 [x] ← 2                In this work, we develop new formalisms for reasoning
         (3) (i1) [x] ← 1                                            about cache events, callbacks, and phantom addresses to create
         (4) [x] evicted                                             a new ISA-level MCM for täkō (§IV). This MCM is axiomatic,
         (5) [x] misses in cache                                     i.e., executions must obey a set of axioms (properties) to be
                                       (6) (i3)2 [x] ← 2             correct under the MCM. In §V, we show how programmers
         (7) (i2) r1 ← [x]                                           can use our MCM to reason about realistic täkō programs.
                               (b)                                      To verify that our MCM accurately captures täkō function-
                                                                     ality, we create a detailed operational (state machine-based)
Fig. 2: (a) A sample täkō program. (b) A possible execution
                                                                     model of a täkō implementation (§VI). We then formally prove
of said program. The evictions and misses from the cache,
                                                                     (§VII) that for all programs, any execution possible on the
which were previously hidden hardware details, now impact
                                                                     operational model is also allowed by our ISA-level MCM.
the outcome of the program.
                                                                     This proof is machine-checked, which means that a verification
                                                                     engine ensures that the steps we write in our proof do indeed
and non-volatile memory transactions. Thus, insights gained          prove all required theorems.
from modeling and verifying täkō are likely to be more broadly        In the course of our formalization, we come to the realiza-
applicable than those gained from modeling a more specialized        tion that architects and formal methods experts have different
accelerator. Finally, no implementation of täkō currently exists   needs from formal models – not just for täkō, but in general.
beyond the closed-source simulator used for the täkō paper.        While formal methods experts are concerned with verifiability,
Thus, there is no way for researchers other than the authors         architects desire the flexibility to change design features that
of täkō to validate whether a täkō implementation is correct.    may improve performance or energy efficiency.
A formal hardware-software interface for täkō would enable            Our work serves the needs of both camps. For täkō, our for-
such verification, and we create such an interface in this paper.    malisms must account for prefetching and cache replacement
   As an example of how täkō programs can execute in coun-         policies because they can affect täkō correctness. However, the
terintuitive ways, consider the program in Figure 2a, in which a     best prefetching and replacement policies for a desired level
program thread writes to an address [x] and subsequently reads       of performance and energy efficiency may not be known until
from it. In this case, [x] is a phantom address with an OnMiss       late-stage implementation. Thus, we parameterize our oper-
callback registered for it. When an access to [x] misses in the      ational model across prefetching policies, cache replacement
cache, the callback runs, populating the cache with a value          policies, and network-on-chip specifics so that architects can
of 2 for [x]. In an execution where [x] is brought into the          change them in a täkō implementation without compromising
cache to execute (i1) and remains there for the execution of         their conformance with our MCM. On the formal methods
(i2), the value of 2 would be overwritten to 1 by (i1), and          side, we formulate our axioms to be prefix-closed [25, 47], a
thus (i2) would read the value of 1 into r1. However, if an          property which enables inductive proofs of implementations
eviction occurs between these instructions, (i2) would miss          against these axioms across all programs.
in the cache, causing the OnMiss to be invoked again. In                This work makes the following contributions:
this case, the previously written value is dropped entirely,            • First Cache-Aware ISA-level MCM. We develop the
since phantom addresses are not backed by main memory. An                  first MCM capable of reasoning about the semantics
execution illustrating this counterintuitive behavior is shown             of cache misses, evictions, writebacks, callbacks, and
in Figure 2b. In this case, the intervening cache eviction and             phantom addresses at an ISA level.
subsequent OnMiss cause the value that is loaded by (i2)                • Parameterized Formal Implementation Model of täkō.
to completely forget the occurrence of the previous write. In              We construct a detailed microarchitectural model of täkō
such a system, the previously hidden details of cache features,            in Dafny [31]. This model parameterizes over täkō-
such as a prefetching or cache replacement policy, now have                adjacent properties that can impact performance (cache
a direct impact on the functional results of the program.                  replacement policy, prefetching policy, network-on-chip
   täkō’s linkage of cache features to program results funda-            specifics), ensuring that proofs about this model are valid
mentally changes the memory consistency model (MCM) of an                  for all choices of these parameters.
ISA that may implement täkō. MCMs constrain the values that           • Machine-Checked Soundness Proof of our MCM. We
can be read by load instructions in parallel programs, so pre-             formally prove that for all programs, any execution of our
cisely specifying MCMs and verifying their implementations                 operational model is also allowed by our ISA-level MCM,
is critical to parallel system correctness. A formally specified           ensuring that our ISA-level MCM accurately represents
                                                                                Core 0     [x].OnMiss              [x].OnWB
                                                                            (i1) [x] ← 1   (i3) [x] ← 2 (i5) [y] ← 1
                                                                            (i2) r1 ← [x]
                                                                            (i4) r2 ← [y]
                                                                            r1=2, r2=0 impossible on täkō (if [y] is initially 0)
                                                                                                       (a)


                                                                              OnMiss                   OnWB       OnMiss


                                                                                                                                      time
Fig. 3: Image from [55] showing the order of events in täkō
when an OnMiss occurs for an L3 phantom address.                          Start Of          Start Of          Start Of
                                                                          OnMiss            Eviction          OnMiss

    täkō functionality. To our knowledge, this is the first
    end-to-end machine checked proof of an operational                                                 (b)
    implementation against an axiomatic ISA-level MCM.
                                                                       Fig. 4: (a) An extended version of Figure 2a’s program (origi-
  • General Formal Modeling and Verification Insights.
                                                                       nal program in gray) that depicts the interactions of callbacks
    We discover that architects and formal methods experts
                                                                       and regular address [y]. The outcome r1=2, r2=0 is impossible
    have different needs from a formal model, and that a
                                                                       on täkō. (b) A timeline that explains why the outcome is
    model must serve both communities to be truly effective.
                                                                       impossible, as r1=2 implies the OnWB has completed and
    We also discover that enforcing prefix-closure [25, 47] for
                                                                       written 1 to [y], forbidding r2=0.
    axioms is extremely useful for enabling inductive proofs
    of microarchitectural implementations against axiomatic
                                                                       be interleaved rather arbitrarily with core thread instructions.
    ISA-level MCMs.
                                                                       While a load reading from an OnMiss cannot commit before
                       II. BACKGROUND                                  the OnMiss completes, OnEvict and OnWB callbacks can
                                                                       execute anytime after their address is brought into the cache
A. täkō Hardware Overview                                            or written to in the cache respectively. täkō thus offers a
    As Figure 3 shows, täkō is a tiled chip. Each tile has a core,   FlushRange synchronization primitive. A FlushRange
an L1, a private L2, and a shard of an L3 bank which is shared         causes all cache lines with addresses in the mentioned range to
across tiles. Each tile also has an engine that runs callbacks.        be evicted from the cache, invoking their OnEvict or OnWB
    täkō allows programmers to register OnMiss, OnEvict,             and blocking the FlushRange till they complete.
and OnWriteback (henceforth OnWB) callbacks for virtual                   täkō engines serialize all callbacks to the same address
address ranges. These callbacks run on the tile’s engine during        in FIFO order to reduce the possibility of races on those
the corresponding cache events. Figure 3 depicts an OnMiss             addresses [55]. However, täkō executions can still easily lead
workflow. When an address with a registered OnMiss misses              to races and counterintuitive outcomes, as we discuss next.
in the cache, a hardware thread runs the OnMiss on the
corresponding engine to calculate the cache line’s contents.                         III. T HE N EED FOR F ORMALIZATION
    Similarly, when a line in the address range is evicted from        A. High Complexity
a cache, an OnEvict or OnWB is invoked to run, depending                 In täkō, accesses performed during callbacks can interleave
on whether the data is clean or dirty respectively. Together,          with accesses on core threads, increasing system complexity
täkō’s three callback types allow for custom calculations and        and counterintuitive outcomes. The confusion is exacerbated
behavior to run as part of the cache’s handling of these address       by the fact that callbacks can also access regular addresses.
ranges. This functionality allows data transformation to occur         Programmers thus have to reckon not only with phantom
as part of data movement instead of occurring once the data            address semantics, but also with how cache events for phan-
has been loaded, and for any clean-up to happen as part of             tom addresses can trigger changes in the values of regular
data eviction. Moreover, as the computation results are cached,        addresses. Next, we provide an example of this complexity.
redundant work is avoided if the same transformation needs
to be run again, improving performance on certain workloads.           B. Reasoning About Callbacks
For addresses with no callbacks registered, the semantics of               Consider Figure 4a, the example from §I augmented with an
the conventional load/store interface are preserved.                   additional OnWB callback that writes the value 1 to address [y]
                                                                       (a regular address with no callbacks registered). If Figure 4a
B. Callback Synchronization                                            were a regular 3-thread program, the outcome r1=2, r2=0
   In täkō, the microarchitecture’s prefetching and cache re-        would be possible. This outcome is actually impossible on
placement policies still control when a cache line is moved in         täkō, but understanding why this is the case requires reasoning
and out of the cache, as Figure 2 showed. Thus, callbacks can          about the semantics of caches and callbacks.
                   Core 0         Core 1                            represent instructions and labeled edges encode relations be-
                (i1) [a] ← 1 (i3) r1 ← [b]                          tween instructions. The allowable executions of the program
                (i2) [b] ← 1 (i4) r2 ← [a]                          are given by axioms that enforce constraints on these defined
                    SC forbids r1=1, r2=0                           relations. Various memory consistency models have been
                                                                    encoded using this approach [2, 4, 5, 29, 49, 65, 68].
                               (a)
                                                                        As an example, consider Figure 5a’s (non-täkō) program.
                                                                    Under sequential consistency (SC) [29], the allowed exe-
                                                                    cutions are those corresponding to an interleaving of each
                                                                    core’s instructions in program order. As such, the outcome
                               (b)
                                                                    of r1=1, r2=0 here is outlawed, as r1=1 would indicate (i2)
                                                                    has completed and r2=0 would indicate (i1) has not completed,
Fig. 5: (a) The mp (message passing) litmus test. All addresses     violating program order on either core 0 or core 1.
are assumed to be 0 initially. (b) An execution graph of mp             Figure 5b shows an execution graph for the r1=1, r2=0
that is outlawed under sequential consistency (SC).                 outcome of Figure 5a. All addresses are assumed to initially
                                                                    be 0, as enforced by the initialization writes (W ) of 0 to [a]
   Figure 4b explains this reasoning. If r1=2, the value for (i2)
                                                                    and [b]. The other W nodes are the write events ((i1) and (i2)),
must have been generated as the result of an OnMiss A
                                                                    while the R nodes are the read events. Each node is annotated
instead of by (i1). Thus, an interspersed OnMiss must have
                                                                    with its address and value read or written. The sb (sequenced-
run between (i1) and (i2). However, since (i1) would have
                                                                    before) edges connect a given instruction to instructions after
brought the data for [x] into the cache, that data must also
                                                                    it in program order. The rf (reads-from) edge denotes that the
have been evicted B before the execution of the OnMiss that
                                                                    read at the target reads from the write at the source. The f r
(i2) read r1=2 from. This eviction must have been an OnWB,
                                                                    (from-reads) edge denotes that the write at the target occurs
as the data has been modified by (i1) and is dirty C . Due to
                                                                    after the read at the source. The mo (modification order)
the serialization of callbacks ensured by the cache controller
                                                                    relation establishes a total order on all writes to an address1 .
 D , we can guarantee that (i5) (the write to [y]) has already
                                                                        The axiomatization of SC [5] forbids cycles comprised of
completed by the time (i4) runs. Thus, the load of [y] in (i4)
                                                                    the rf , f r, sb and mo relations. Formally, this is stated as
must read a value of r2=1 for [y] in this execution, making
                                                                    acyclic(rf ∪ f r ∪ sb ∪ mo). Figure 5b’s execution graph has a
the outcome r1=2, r2=0 impossible.
                                                                    cycle comprised of these relations. Thus, it is forbidden under
C. Formalization To The Rescue                                      SC, as we would expect for the outcome of r1=1, r2=0.
    To enable programmers to rigorously reason about täkō         B. Cache Events And Relations
programs, we develop an ISA-level MCM for täkō (§IV).
                                                                       Our ISA-level MCM for täkō introduces new events and
This ISA MCM captures the semantics of cache events
                                                                    relations to enable reasoning about caches and callbacks. Since
and callbacks, but does not require programmers to fully
                                                                    the semantics of phantom reads and writes require reasoning
understand täkō’s microarchitectural details, thus enhancing
                                                                    about callbacks (e.g., Figure 2), we denote phantom reads and
täkō’s programmability, which we demonstrate with illustrative
                                                                    writes using Rcb and Wcb events (cb for callback). Regular
litmus tests (§V). We ensure that our ISA MCM accurately
                                                                    reads and writes are denoted using R and W . For both ad-
reflects täkō by first constructing a detailed implementation
                                                                    dress types, we denote an atomic read-modify-write operation
model of täkō (§VI), and then proving that all executions
                                                                    with RM Wcb and RM W respectively. We add F l events to
of the implementation model are allowed by our ISA MCM
                                                                    represent the flushing of an address by FlushRange.
(§VII). Along the way, we discover insights about how to
                                                                       We add events for the beginning and end of each callback,
construct microarchitectural models that are useful for both
                                                                    denoted Ms and Me (OnMiss start and end respectively) and
architects and formal methods experts. We also discover a best
                                                                    Es and Ee (OnEvict or OnWB start and end respectively).
practice for ISA-level MCM design to enable effective proofs
                                                                    We differentiate between OnEvict and OnWB events using
of hardware implementations against such MCMs.
                                                                    a dirty bit for each Es or Ee event. The dirty bit is false for
   IV. C ACHE -AWARE R EASONING AT THE ISA L EVEL                   OnEvict events and true for OnWB events.
  We now explain our ISA-level MCM for täkō. We begin                We add a new relation called cbo (callback order) to enforce
with background on ISA MCMs (§IV-A), and then describe              orderings on these new events. cbo establishes a total order
our MCM’s new events and relations (§IV-B). The rest of the         on all callback events (Rcb , Wcb , RM Wcb , Ms , Me , Es , Ee )
section discusses key axioms in our MCM in the context of           for a single address, and reflects täkō’s serialization of all
outlawing a forbidden outcome of Figure 4a’s program.               callbacks to a given address [55].
                                                                       Next, we describe how the axioms we develop on these re-
A. Axiomatic Memory Consistency Models                              lations forbid the r1=2, r2=0 outcome for Figure 4a’s program.
  An axiomatic memory model is a formalization used to                 1 In the literature (e.g., [5]), the relation denoting program order is some-
define the allowable executions of a program. A program             times labeled po and the relation denoting modification order is sometimes
execution is represented as a directed graph, where nodes           labeled co (coherence order).
 ∀R.∃!W.(W, R) ∈ rf               RfWf1 empty([Ms ]; cbo; cbo; [Me ] ∩ thd)                                    CboM
 rf ⊆ val ∩ addr                  RfWf2 empty([Es ]; cbo; cbo; [Ee ] ∩ thd)                                    CboE
 ∀A.to(mo, WA )                  MoWf1 empty([Wcb ]; viscb; [Es (.., .., f alse)])                           EvDirty
 mo ⊆ addr                       MoWf2 empty(viscb; [Es (.., .., true)] \ [Wcb ]; viscb)                     WbDirty
                   A       A
 ∀A.to(cbo, CBse ∪ CBme )        CboWf1 empty([Me ]; cbo; [Ms ] \ [Me ]; cbo; [Es ]; thd; [Ee ]; cbo; [Ms ])   OEInt
 cbo ⊆ addr                      CboWf2 empty([Ee ]; cbo; [Es ] \ [Ee ]; cbo; [Ms ]; thd; [Me ]; cbo; [Es ])  OMInt
 viscb ⊆ val                      CboVal ∀Me .∃!Ms .(Ms , Me ) ∈ thd                                         OMThd
 [Ms ]; thd; [Me ] ⊆ cbo           ThdM ∀Ee .∃!Es .(Es , Ee ) ∈ thd                                           OEThd
 [Es ]; thd; [Ee ] ⊆ cbo           ThdE empty([Ms ]; cbo; [Ms ] \ [Ms ]; thd; [Me ]; cbo; [Ms ])               MeInt
 [Es ]; thd; [Ee ] ⊆ dirty       DirtyWf empty([Es ]; cbo; [Es ] \ [Es ]; thd; [Ee ]; cbo; [Es ])              EeInt
 irref lexive(hb)                     Hb ∀CBme .∃!Me .(Me , CBme ) ∈ vf                                        VfWf
 irref lexive(eco; hb)                Vis ∀Es .∃!Me .(Me , Es ) ∈ ef                                            EfWf
 irref lexive(rf ∪                        ∀F l.(∀Ms .(F l, Ms ) ∈ addr ⇒ (F l, Ms ) ∈ cbo)) ∨
                                   RMW                                                                         EbWf
   (mo; mo; rf −1 ) ∪ (mo; rf ))            (∃!Ee .(Ee , F l) ∈ eb)
 irref lexive(cbo; hb)             VisCb
where
 R = {R, RM W }                   W = {W, RM W }                vf = ([Me ]; cbo; [CBme ]) \ ([Me ]; cbo; [CBse ]; cbo; [CBme ])
 Rcb = {Rcb , RM Wcb }            Wcb = {Wcb , RM Wcb }         ef = ([Me ]; cbo; [Es ]) \ ([Me ]; cbo; [CBse ]; cbo; [Es ])
 CBme = {Rcb , Wcb , RM Wcb } CBse = {Ms , Me , Es , Ee } eb = ([Ee ]; cbo; [F l]) \ ([Ee ]; cbo; [CBse ]; cbo; [F l])
 f r = rf −1 ; mo                 eco = (rf ∪ mo ∪ f r)+        sw = ([RM W ]; rf ; [RM W ]) ∪ ([RM Wcb ]; cbo; [RM Wcb ])
 hb = ((I × ¬I) ∪ sb ∪ sw ∪ vf ∪ eb ∪ ([Me ]; cbo; [Es ]) ∪ ([Ee ]; cbo; [Ms ]))+
 viscb = ([Wcb ∪ Me ]; cbo; [Rcb ∪ Es ]) \ ([Wcb ∪ Me ]; cbo; [CBse ∪ Wcb ]; cbo; [Rcb ∪ Es ])
 to(R, S) = irref lexive(R) ∧ transitive(R) ∧ (∀s1 , s2 ∈ S.R(s1 , s2 ) ∨ R(s2 , s1 ))
 race = ((((W ∪ R ∪ Wcb ∪ Rcb ) × (W ∪ R ∪ Wcb ∪ Rcb )) \ ((R × R) ∪ (Rcb × Rcb ))) ∩ addr) \ (id ∪ hb ∪ hb−1 )
 addr, val, dirty denote pairs of events with matching addresses, values, and dirty bits respectively.
 Each address is of type Synch or Data. RM W /RM Wcb run on Synch addresses; R/W/Rcb /Wcb run on Data.
 X A is all X events with address A. I denotes initialization events. id is the identity relation, i.e. pairs of identical events.
Fig. 6: All axioms for our täkō MCM. Executions must satisfy all axioms to be allowed. [A] is the elements of type A in
relation form [59]. A × B are pairs of an element of type A and an element of type B. A \ B is the elements of A that are
not in B. Semicolons (;) denote relational composition, e.g., e1; e2 is two relations e1 and e2 where the destination node of
e1 is the source node of e2. R−1 is the inverse of R. ∃! specifies existence of a unique element with the specified property.

Figure 6 contains all our axioms and their names. We refer to      executions in which reads or writes of phantom addresses like
axioms using these names throughout the rest of the paper.         [x] are not preceded by the execution of an OnMiss for them.
                                                                      To this end, we add axioms (VfWf in Figure 6) to ensure
C. Ensuring Phantom Address Sources                                that any Rcb or Wcb must be preceded in cbo by an Me .
    Figure 7 depicts execution graphs for the r1=2, r2=0 out-      Analogously, a F l must be preceded by an Ee , denoting that an
come of Figure 4a’s program. This outcome is impossible on         eviction has completed for the address being flushed (EbWf).
täkō due to cache and callback semantics (§III-B). Figure 7a     An F l may also occur before its address is ever brought into
depicts an execution graph for this outcome without täkō-        the cache (i.e., before there is anything to flush). These axioms
specific axioms. Traditional MCM axioms cannot reason about        are sufficient to outlaw Figure 7a’s execution. Adding the
cache events and callbacks, so täkō-specific axioms are needed   required OnMiss gives us Figure 7b, which we discuss next.
to forbid this execution. Graphs (b)-(e) depict execution graphs
after the addition of one or more täkō-specific axioms and/or    D. Ensuring Callback Value Correspondence
relations that outlaw the previous flawed execution graph but         Figure 7b includes an OnMiss to generate a value for [x].
not the forbidden outcome of r1=2, r2=0. Graph (f) depicts         However, note that the OnMiss generates a value of 2 for [x]
the execution graph after enough axioms and relations have         (the Me ([x], 2) node). This is then overwritten by the write of
been added to forbid the r1=2, r2=0 outcome.                       1 to [x] (the Wcb node). The subsequent read of [x] (i.e., the
    First, consider Figure 7a’s execution, in which no callbacks   Rcb node) runs after the write to [x], and so should see the
execute. The regular read of [y] can read its initial value of 0   updated value of 1. However, it currently reads a 2.
from memory, but [x] is a phantom address that does not live          To fix this problem, we need to add an axiom to ensure that
outside the cache. Since the caches are initially empty, for [x]   reads of phantom addresses (and eviction callbacks) do not
to be read, a value for it must first be created in the cache by   read values that have been overwritten. Specifically, we must
running an OnMiss callback for [x]. Thus, we must outlaw           ensure that for a given address a, if there is no intervening
 (a) Problem: No callbacks. (b) Problem: Value mismatch. (c) Problem: No intervening eviction. (d) Problem: OnEvict for dirty data.
 Solution: §IV-C.           Solution: §IV-D.             Solution: §IV-E.                      Solution: §IV-E.




(e) Problem: Violates happens-before visibility for [y].                    (f) Final execution graph for outcome r1=2, r2=0
Solution: §IV-F.
Fig. 7: (a-e) Faulty candidate execution graphs for Figure 4a’s täkō program with an outcome of r1=2, r2=0. (f) The final
execution graph for the outcome r1=2, r2=0 once all relevant events, relations, and axioms are added. §IV explains how we
encode the semantics of caches and callbacks into axioms to enforce that impossible outcomes like r1=2, r2=0 are forbidden.

write (e.g., a Wcb ) to a in cbo order between the end of an       could get a value of 2 in our program is if another OnMiss
OnMiss (i.e., an Me ) for a and a read (e.g., an Rcb ) of a,       ran and generated that value of 2, which was then read by the
then the value of the read must match the value of the Me .        Rcb node. Adding this extra OnMiss to the graph gives us
On the other hand, if there is an intervening write to a in cbo    Figure 7c, which we discuss in the next section.
order between the Me and the Rcb to a, then the value of the
Rcb must match the value of the most recent such write in cbo.
The latter case occurs when a phantom address is brought into      E. Ensuring Correct Callback Correspondences
the cache and then written to. Both cases are depicted below:
                                                                      As Figure 7c shows, we have now ensured correct values
                                                                   for the phantom reads in our execution. However, note that
                                                                   Figure 7c contains two OnMiss callbacks for [x] without [x]
                                                                   being evicted from the cache in between. This is impossible,
                                                                   and so an eviction callback (OnEvict or OnWB) for [x] must
                                                                   run in between the two OnMiss callbacks.
                                                                      To enforce this constraint, we require that there must be
   To express this constraint formally, we first define a viscb
                                                                   an OnEvict or OnWB (i.e. an Es /Ee pair) between the end
relation to denote phantom writes and OnMiss results that
                                                                   of an OnMiss and the beginning of another OnMiss to that
are visible to phantom reads and eviction callbacks. We then
                                                                   same address. Graphically, this constraint requires the dotted
require that viscb ⊆ val (CboVal in Figure 6). The val
                                                                   events in the diagram below to exist between the Ms and Me
relation links elements with the same value, so this constraint
                                                                   (thd refers to events on the same thread):
requires that elements linked by viscb must have the same
value. This constraint ensures that phantom reads and eviction
callbacks must have values that are actually visible to them.
   Returning to Figure 7b, now the only way the read of [x]
                                                                   which writes are visible to a read. The hb relation enables
                                                                   capturing orderings enforced by inter-thread synchronization
                                                                   such as release-acquire [14]. Stated formally, the hb relation is
                                                                   typically defined as (sb∪sw)+ , or the transitive closure (+) of
                                                                   sb and sw (synchronizes with) edges [2, 9]. hb also connects
Fig. 8: A pattern forbidden by traditional happens-before (hb).    initialization events to non-initialization events (I × ¬I).
                                                                      Consider Figure 8’s relational pattern. Here, the read R of
   Formally, this axiom is OEInt in Figure 6. We also add a        [x] reads from the write of v to [x], but a later write of v ′ to
similar axiom for the existence of an OnMiss between two           [x] happens-before the read. The read should not observe the
eviction callbacks of the same phantom address (OMInt).            older write of v and should instead read the write of v ′ . Thus,
   The OEInt axiom only ensures that an eviction callback          this pattern and other similar ones should be forbidden. We,
runs in between two OnMisses. It does not enforce whether          like prior work, do so using Figure 6’s Vis axiom.
said callback is an OnEvict or OnWB for the appropriate               2) Adding Callback Ordering to hb: Now consider Fig-
cases. With OEInt, an execution graph like Figure 7d is            ure 7e’s execution graph. In täkō, the write of [y] happens
possible. Here, we have an OnEvict for [x] in between the          before the read of [y], as §IV-E covers. However, there is no
two OnMisses (the dirty bits of the Es and Ee are false).          hb edge from the write of [y] to the read of [y] in Figure 7e,
Since [x] is written to by the Wcb node in the graph before its    because the traditional hb relation does not take callback
eviction, an OnWB for [x] should run instead of the OnEvict.       orderings into account. Thus, Figure 8’s pattern does not show
The OnEvict should only have run if [x] had not been written       up in the graph, and the execution is not forbidden by the Vis
to in the cache before its eviction.                               axiom. For our hb relation to be accurate, we need to augment
   To this end, we establish a correspondence between the dirty    it with callback-related orderings.
bits of Es and Ee events and the existence of a write to a            There are four additions that we make to the traditional hb
phantom address after it is brought into the cache. If the dirty   relation of (sb ∪ sw)+ in our täkō MCM (Figure 6). Our first
bit of an Es is false (OnEvict case), we outlaw the existence      two additions to hb are vf (value-from) and eb (evicts-before)
of a callback write event in cbo order occurring between the       edges. vf edges connect Me events to the Rcb or Wcb that
previous Me (i.e., the end of the most recent OnMiss) and          they populate the cache for, while eb connects Ee events to
this Es . Conversely, if the dirty bit of the Es is true (OnWB     the next F l for the corresponding address. Intuitively, these
case), we necessitate the existence of a write event in between    orderings are part of hb because an OnMiss for a phantom
the previous Me and the Es . Both cases are depicted below:        address must finish before a read or write to that phantom
                                                                   address, and an eviction of a phantom address must complete
                                                                   before the next FlushRange for that address completes.
                                                                      The remaining two additions to hb come from täkō’s serial-
                                                                   ization of callbacks to the same address. Specifically, we add
                                                                   any cbo edges from Me to Es nodes (i.e., from the end of an
   To express this formally (Figure 6), we enforce EvDirty for     OnMiss to the start of an eviction for the same address) and
the OnEvict and WbDirty for the OnWB cases.                        from Ee to Ms nodes (i.e., from the end of an eviction to the
   Once we enforce the correct type for each eviction callback,    start of an OnMiss for the same address).
Figure 7d can no longer be generated. Figure 7e shows the             Figure 7f shows the execution graph from Figure 7e with
execution of our running example with an OnWB between the          edges added from our updated hb relation. Our updated hb
two OnMiss callbacks for [x], as required.                         relation correctly enforces the hb edge we know should exist
   While we have now enforced correct values for the call-         from the write of [y] to the read of [y]. The graph now contains
backs and phantom addresses, the effects of these callbacks        an instance of Figure 8’s forbidden pattern, which is forbidden
and phantom addresses on regular addresses have not been           by the Vis axiom (§IV-F1). Thus, Figure 7f’s execution is now
enforced. Specifically, Figure 7e shows that the write of 1 to     forbidden by our axioms. There is no additional execution that
[y] in the OnWB of [x] runs before the Rcb of [x], which in        allows the outcome of r1=2, r2=0, so the axioms we have
turn runs before the read of [y]. (We assume no load-load          discussed suffice to forbid that outcome.
reordering in our system; the täkō paper [55] uses the x86
                                                                   G. Summary
ISA which forbids load-load reordering [49].) Thus, the read
of [y] should see the write of 1 to [y], but there is currently        In this section, we showed how we encoded reasoning about
no axiom enforcing this. To enforce this ordering, we need to      täkō’s callbacks and cache events into our ISA-level MCM for
augment the happens-before reasoning from traditional MCMs         täkō. We could not discuss all our MCM axioms from Figure 6
with callback-related orderings, which we do next.                 due to space constraints, but we discussed many important
                                                                   ones. We have encoded all of our axioms as well as our täkō
F. Augmenting Happens-Before With Callback Ordering                litmus tests in Alloy [21] to support use of our MCM. A
  1) Traditional Happens-Before Ordering: In conventional          programmer can now simply use our MCM to check whether
consistency models, the hb (happens-before) relation governs       a given outcome is possible for their täkō program, without
         Core 0               Core 1          [b].OnMiss            of [b] in Figure 5b to RMW operations, inducing an sw edge
  (i1) [a] ← 1          (i3) RMW([b], r1, 1) (i5) [b] ← 0           from the write of [b] to the read of [b], as shown in Figure 9b.
  (i2) RMW([b], , 1) (i4) r2 ← [a]                                  The Vis axiom then enforces that the read of [a] is required to
        mprmw ([b] is a regular address, no OnMiss):                see the write of 1 to [a], forbidding the outcome of r1=1,r2=0.
           r1 = 1, r2 = 0 forbidden by our MCM                      Vis also enforces per-address SC for regular addresses.
    mpcb ([b] is a phantom address, OnMiss included):                  Both regular and phantom conflicting accesses (i.e., a pair
           r1 = 1, r2 = 0 forbidden by our MCM                      of accesses to the same address in different threads not ordered
                                                                    by hb where at least one is a write) constitute a race if they
                               (a)
                                                                    are to a data address, e.g., Figure 5b’s read of [a] and write of
                                                                    1 to [a] constitute a race. Figure 6 defines our race relation.
                                                                    B. Synchronizing With RMWs To Phantom Addresses
                                                                       RMWs to phantom addresses (i.e., RM Wcb events (§IV-B))
                               (b)                                  can also be used to enforce ordering constraints, similar to how
                                                                    regular address RMWs can be used on conventional programs
                                                                    (§V-A). This is illustrated in the mpcb litmus test (Figure 9a),
                                                                    where the address [b] is a phantom address with an OnMiss
                                                                    that returns 0. Similar to mprmw, the outcome of r1=1,r2=0
                               (c)                                  is forbidden by our täkō MCM.
                                                                       Figure 9c demonstrates a forbidden execution graph that
Fig. 9: (a) The mprmw (no callback) and mpcb (OnMiss for            shows the happens-before reasoning in mpcb, which is analo-
[b]) litmus tests. (b) A forbidden execution of mprmw where         gous to that presented in §V-A for mprmw. In this case, as the
the RM W s augment the hb relation to outlaw the reading            cbo relation between the two RM Wcb events is also added to
of 0 for [a]. (c) An analogous forbidden execution of mpcb          the sw relation, the same hb edge is constructed between the
showing the same pattern when [b] is a phantom address.             write and read of [a]. The Vis axiom then forbids the outcome
                                                                    of r1=1,r2=0 for this test, very similar to how it forbids this
                                                                    outcome in mprmw.
needing to understand the intricacies of a täkō implementation.      Of course, with the use of a phantom address, one must
§V shows how to use our MCM to analyze täkō programs.             reason about intervening evictions that could occur between
                                                                    the RM Wcb accesses. In mpcb, the VisCb axiom ensures that
        V. P ROGRAMMING T ÄK Ō U SING O UR MCM
                                                                    if (i3) reads a value of 1, it must get this value from (i2) (as
    We now show how programmers can use litmus tests to             the OnMiss can only produce the value 0), ensuring that no
write and analyze täkō programs using our MCM (§V-A-              eviction occurs in between.
V-E). We also analyze a real täkō application (§V-F) using
our MCM, and highlight the insights we discover about writing       C. Instruction Ordering Within Callbacks
täkō programs that are both correct and performant.                   Our MCM does not require the preservation of program
                                                                    order between instructions to different addresses in callbacks,
A. Programs Without Callbacks                                       similar to how we do not require such ordering in non-
    Our MCM imposes minimal restrictions on programs with-          täkō programs (§V-A). We demonstrate this using the icbsb
out callbacks to avoid adding ordering requirements to non-         litmus test in Figure 10a. In this test, two cores perform writes
täkō programs. We do not require preservation of program or-      (i1) and (i2) to phantom addresses [x] and [y] respectively. As
der between different addresses, so for instance, the execution     there are no restrictions in täkō that prevent running callbacks
of mp in Figure 5b is allowed under our model.                      for different addresses concurrently, the two OnWBs can run at
    Similar to release consistency [14] and C11 [8], we classify    any time with respect to each other, and perform writes and
addresses as data or synchronization addresses, and enforce         reads to addresses [a] and [b].
that if one thread performs a synchronization write that is             The OnWBs for [x] and [y] recreate the well-known sb
read by a synchronization read on another thread, accesses          (store buffering) litmus test [53]. As in the sb test, for
after the synchronization read are required to observe accesses     both loads in the callbacks to return 0 (i.e., the outcome
before the synchronization write. In our model’s parlance, this     r1=0, r2=0), the instructions in at least one callback must be
synchronization read-write pair induces an sw edge between          reordered. Figure 10b shows an execution with the outcome
the two accesses. We chose RMW operations to implement              r1=0,r2=0 that is allowed under our model, thus showing that
all accesses to synchronization addresses [1] for simplicity.       our model does not require the preservation of program order
(Additional constructs like C11 low-level atomics [9] could         in callbacks. More specifically, the axioms in our MCM allow
be added in the future.) For instance, consider the mprmw           the f r∪sb cycle among the callback instructions in Figure 10b.
litmus test in Figure 9a (where [b] is a regular address and its        By not requiring program order to be preserved in callbacks,
OnMiss is thus omitted). This test changes the read and write       our MCM gives computer architects significant freedom when
           Core 0       [x].OnMiss      [x].OnWB                             Core 0          [x].OnMiss         [x].OnWB
        (i1) [x] ← 1    (i3) [x] ← 0 (i5) [a] ← 1                     (i1) [x] ← 1           (i4) [x] ← 0 (i5) [y] ← 1
                                     (i6) r1 ← [b]                    (i2) FlushRange[x]
           Core 1     [y].OnMiss        [y].OnWB                      (i3) r1 ← [y]
        (i2) [y] ← 1 (i4) [y] ← 0 (i7) [b] ← 1                         wbr (without (i2)): program racy under our täkō MCM
                                     (i8) r2 ← [a]                    wbf (with (i2)): no race, r1 = 0 forbidden by our MCM
        icbsb: r1 = 0, r2 = 0 allowed by our MCM                                                  (a)
                               (a)




                                                                                                  (b)




                               (b)
Fig. 10: (a) The icbsb litmus test. (b) An execution of
icbsb that demonstrates the intra-callback instruction re-
ordering that is allowed by our MCM.

                                                                                                  (c)
designing the callback engine. In particular, täkō designs that   Fig. 11: (a) The wbr (Writeback Race) and wbf (Writeback
buffer and reorder memory operations in the engine can still        Flush) litmus tests. (b) wbr execution where the accesses to
use our MCM.                                                        [y] race because the OnWB is non-blocking. (c) wbf eliminates
D. FlushRange as a Synchronization Primitive                        the race using a FlushRange, and forbids r1=0.

   While the use of an OnMiss-generated value (Me ) by a            the Ee and the F l as per Figure 6’s definitions of eb and
Rcb or Wcb induces an hb edge between the events (§IV-F2),          hb. Combining this edge transitively with the two yellow sb
an OnEvict or OnWB for a phantom address can execute                edges gives us an hb edge between (i5) and (i3), eliminating
anytime after the address is brought into the cache (for            the race. We now also have a cycle in hb and f r between
OnEvict) or after the address is written to in the cache (for       (i3) and (i5), which violates the Vis axiom, forbidding this
OnWB). This freedom allows races between accesses in these          execution’s outcome of r1=0. Our MCM thus formalizes how
eviction callbacks and those in core program threads.               FlushRange synchronization can be used to eliminate races.
   Consider the wbr litmus test from Figure 11a, where the              The race in wbr illustrates a key difference between täkō
bolded FlushRange (i2) is omitted. This program distills            and prior works like IMO [20] and EcMon [45] that allow user-
a use case of phantom memory as a write-combining buffer            space traps for cache events. In these works, traps effectively
for scatter-updates [55], which are published back to regular       have function call semantics: they interrupt a core thread
memory via OnWBs. In this test, Core 0 updates the buffer at        (either immediately after a cache event or at a predetermined
phantom address [x] in (i1), and (i5) publishes the update to       execution point), execute a handler, and then return control.
address [y] in regular memory on a writeback. Core 0 also           Thus, the ability of traps to concurrently execute with core
reads the published update in (i3).                                 threads is greatly reduced if not eliminated. In contrast, in
   Figure 11b shows that since the OnWB of [x] can execute          täkō, callbacks have thread semantics [55]: they execute on
anytime after (i1), (i5) and (i3) are unordered by hb, causing      dedicated engines in parallel with core program threads. As
a race. If we add the FlushRange (i2) from Figure 11a to            a result, conflicting accesses across täkō callbacks and core
the wbr test to give us the wbf test, the race is eliminated.       program threads can be races. This would not be the case in
Specifically, this FlushRange must either commit before             IMO and EcMon where callbacks are not separate threads.
the OnMiss of [x] or after the OnWB of [x], as enforced
by EbWf (Figure 6). Committing the FlushRange before                E. FlushRange Utility in Multicore Programs
the OnMiss causes a forbidden cycle in cbo (CboWf1).                   We now explore the utility of the FlushRange primitive
Meanwhile, Figure 11c depicts the execution where it commits        in a multicore setting by considering a multicore version of the
after the OnWB of [x]. Here, an hb edge is added between            wbf litmus test (§V-D). Figure 12 contains 2 implementations
        Core 0                 Core 1           [x].OnMiss          updates in the line at eviction to determine whether to apply
 (i1) RMW([x], , 1)     (i4) RMW([x], , 2)     (i7) [x] ← 0         the updates in place or log them [55]. We additionally use
 (i2) FlushRange[x]     (i5) FlushRange[x]                          RMW instructions ((i1) and (i4)) to update [x] in both tests
 (i3) r1 ← [y]          (i6) r2 ← [z]                               because using stores for (i1) and (i4) would result in a race
         [x].OnWB (1)                  [x].OnWB (2)                 between those two accesses.
 (i8)    r3 ← [y]               (i12) if x = 1:                        In phiR, the program runs with the OnWB (1) implemen-
 (i9)    if r3 = 0:             (i13)      [y] ← 1                  tation of the OnWB for [x]. In this OnWB implementation, (i8)
 (i10)      [y] ← 1                    else:                        first reads [y]. If [y] has a value of 0 (i.e., if [y] has not yet
         else:                  (i14)      [z] ← 2                  been written to), (i10) writes 1 to [y]. If [y] has already been
 (i11)      [z] ← 2                                                 written to by a prior OnWB for [x], (i11) writes 2 to [z] instead.
                    phiR (with OnWB (1)):                           Thus, the first time the OnWB runs, it will write to [y], and if
             program racy under our täkō MCM                      it runs a second time, it will write to [z].
                  phiNR (with OnWB (2)):                               The phiR litmus test is racy, as demonstrated by the
    no race, r1 = 0, r2 = 0 forbidden by our täkō MCM             execution snippet in Figure 12b. The core cause of the race is
                                                                    that the RMWs (i1) and (i4) can occur in either order, but the
                               (a)
                                                                    OnWB will always write to [y] in its first iteration and [z] if
                                                                    it runs a second time. Consider the case where (i4) runs first
                                                                    (not shown in Figure 12b) and then (i5) invokes the OnWB and
                                                                    causes [y] to be updated to 1 (this OnWB is also not shown).
                                                                    Figure 12b shows that when (i1) subsequently writes to [x]
                                                                    and (i2) then invokes the OnWB, this will trigger the write to
                                                                    [z] in (i11). However, nothing stops this write from racing
                                                                    with the read of [z] in (i6) on core 1, giving us a race.
                                                                       This execution demonstrates a key requirement when using
                                                                    FlushRange for synchronization: for FlushRange to be
                                                                    able to eliminate a race, callbacks should not be able to
                                                                    run accesses that cause the race after the FlushRange in
                                                                    question has committed. Here, it is possible for the OnWB to
                               (b)                                  be triggered and run (i11) after (i5) has committed, so (i5) is
                                                                    unable to prevent (i11) from racing with (i6).
                                                                       The above requirement is fulfilled by the phiNR litmus test
                                                                    from Figure 12a that uses OnWB (2) as the OnWB for [x]. Here,
                                                                    the OnWB uses the evicted value to determine which value to
                                                                    write. (i12) checks the evicted value. If it is 1 (i.e., the last
                                                                    update was from Core 0), then (i13) writes 1 to [y]. If it is 2
                                                                    (i.e., the last update was from Core 1), then (i14) writes 2 to
                                                                    [z]. Thus, once (i5) commits, any write to [z] is guaranteed to
                                                                    have completed – the OnWB only writes 2 to [z] if [x] is 2, and
                                                                    that can only happen after (i4) and before (i5) commits. Thus,
                               (c)                                  there is no write to [z] that can race with (i6) in any execution.
Fig. 12: (a) The phiR (with OnWB (1)) and phiNR (with               (Similarly, once (i2) commits, there is no write to [y] left that
OnWB (2)) litmus tests. (b) Execution snippet showing phiR          can race with (i3), eliminating races on [y] as well.) Figure 12c
race due to OnWB from core 0’s write occurring after                shows how there is no write to [z] in an OnWB triggered by
FlushRange on core 1. (c) Execution snippet showing how             (i1) and (i2), thus eliminating the race seen in Figure 12b.
phiNR avoids the race by branching on evicted value in the             In phiNR, the outcome r1=0,r2=0 is forbidden by our
OnWB.                                                               MCM, because neither (i3) nor (i6) can run before at least one
                                                                    FlushRange instruction (i.e., (i2) or (i5)) commits. Since the
                                                                    FlushRange instructions are each after RMW instructions
                                                                    that write to [x] in program order, the first FlushRange to
of a program (named phiR and phiNR) in which multiple               commit will cause the OnWB to run, which will update one
cores concurrently write updates to a phantom address [x]           of [y] or [z]. Thus, at least one of [y] or [z] will have been
and the OnWB of [x] publishes the results back to different         written to before (i3) or (i6) run, preventing them both from
locations ([y] and/or [z]), depending on how many updates           returning 0 and forbidding the outcome of r1=0,r2=0.
have previously been published (for phiR) and which update             In phiR and phiNR, the OnWB callback runs a maximum
was written last (for phiNR). This logic is inspired by how the     of two times, so the complexity is relatively easy to manage.
täkō paper’s acceleration of scatter-updates uses the number of   Next, we investigate täkō’s implementation of accelerated
       Core 0           [e].OnMiss          [e].OnEvict            Eviction callbacks therefore log edges that are evicted too
 (i1) RMW([e], r1, 1) (i4) r3 ← [g]      (i9) if [e] ̸= 1:         early to regular memory. The main thread processes the log
 (i2) FlushRange[e] (i5) if r3 ̸= 1: (i10)        [ℓ] ← 1          after iterating through the phantom addresses [55].
 (i3) r2 ← [ℓ]        (i6)     [g] ← 1
                      (i7)     [e] ← 0                                The hatsR litmus test (Figure 13a, without (i9)) contains
                            else:                                  the core logic of a naive täkō HATS implementation. The
                      (i8)     [e] ← 1                             phantom address [e] represents a graph edge, with 0 being
 hatsR (without (i9)): program racy under our täkō MCM           a valid edge and 1 an invalid one. Core 0 reads [e] to process
 hatsNR (with (i9)): no race, r1 ̸= r2 forbidden by MCM            it using an RMW, atomically reading [e] and writing 1 to [e]
                                                                   to mark it as processed. This ensures that an eviction cannot
                              (a)
                                                                   occur between reading the edge and marking it processed,
  ...                                                              which would cause the edge to be processed twice. Core 0
                                                                   then flushes [e] to ensure that any in-progress OnEvicts for
                                                                   it are completed. It then processes the log (represented by
                                                                   reading address [ℓ]). The OnMiss maintains an engine-local
                                                                   view of the graph (address [g]), and populates [e] with a valid
                                                                   edge if traversing the graph (i.e., if [g] = 0) or an invalid edge
                              (b)                                  if the graph has already been traversed (i.e, if [g] = 1). The
                                                                   OnEvict writes the edge to the log ([ℓ]). The OnWB is empty.
  ...
                                                                   The intuition here is that if the edge is evicted before being
                                                                   written to, it has not yet been processed.

                                                                      This hatsR program is racy, as Figure 13b’s graph snippet
                                                                   shows. The specific problem is that an OnMiss-OnEvict
                                                                   sequence for a phantom address can run as many times as the
                              (c)
                                                                   cache wants, without action from the core. For instance, the
Fig. 13: (a) hatsR and hatsNR litmus tests. (b) Execution          cache’s prefetcher may load [e], the cache may then evict it,
snippet showing hatsR race due to OnEvict writing to the           and this sequence may then repeat. Here, [e] is first loaded
log post-traversal. (c) Snippet showing how hatsNR elimi-          in and processed (or not) by the core, and evicted or written
nates the race by only logging valid edges in the OnEvict.         back (depending on whether or not it was processed) before
                                                                   (i2)’s FlushRange. However, nothing stops the cache from
graph traversal, which is more difficult to write correctly        then reloading [e] (triggering a second OnMiss) and then
because it has writes in OnEvict callbacks that can run an         evicting it (triggering an OnEvict). This second OnMiss-
arbitrary number of times.                                         OnEvict sequence is shown in Figure 13b. The write in the
                                                                   OnEvict races with the read of the log in (i3). While this
F. A täkō Application Case Study: HATS                           write may not change the value of [ℓ] in the test (if [e] was
   We now analyze täkō’s implementation of HATS                  not processed by the core, [ℓ] will already be 1), recall that
(Hardware-Accelerated Traversal Scheduling) [43], which            each such write to [ℓ] corresponds to updating the log in the
accelerates graph processing. The täkō paper [55] states that    real HATS application, and would cause spurious edges to be
OnMiss and OnEvict should be side-effect-free because              added to the log, impacting correctness.
they can occur at any time, but does not formalize why. täkō’s
HATS implementation ignores this guideline, making it an              Fixing this issue is tricky as the cache cannot be prevented
interesting case study. We use our MCM to analyze HATS             from loading or evicting phantom addresses after the graph
and identify when OnEvict side effects are acceptable.             traversal completes. The solution is to ensure that once the
   täkō’s HATS implementation creates a phantom address          traversal completes, (i) the OnMiss does not provide spurious
range to store all graph edges sequentially. It then uses          data for [e] and (ii) neither the OnMiss or OnEvict access
OnMiss callbacks to traverse the graph and place edges in          addresses besides their registered address [e] and engine-local
this range as the main program thread accesses the phantom         addresses like [g]. This solution is presented in the hatsNR
addresses. Thus, the main thread can iterate over the edges        test (Figure 13a including (i9)), where the OnEvict only
sequentially (an easy-to-predict pattern with good locality),      logs valid edges, and the OnMiss (as before) returns invalid
while the engine handles the hard-to-predict graph traversal.      edges once the graph has been traversed. Figure 13c shows
   Each time the OnMiss runs, it provides the next edge from       how this eliminates the race: post-traversal OnEvicts will
the traversal. The OnMiss only returns each edge once. Even        never log edges in hatsNR, thus eliminating the write of the
if the same phantom address misses twice, the two OnMisses         race. We encoded hatsNR in our Alloy model of our MCM
will return different edges. Thus, edges that are evicted before   and searched for races with a large bound. None were found,
being processed would be lost without additional handling.         giving us confidence that hatsNR is indeed race-free.
                                                                          The overall N ext predicate for the system is a transition
     Core        Engine                        Core         Engine
     + L1         + L1    ...        ...       + L1          + L1
                                                                       of a single component state machine alongside a transition of
            L2                                         L2              the Network to capture a potential message the component
            L3            Tile1     Tile0              L3              transition might send and/or receive. Figure 14 illustrates tran-
  Tile0                                     Tile1                      sitions in greater detail, depicting how the transition system
   Network GetS                     Network GetS        Data
                                                                       represents the behavior of the L2 requesting data from the
                                                                       L3. In this case, the L2.Next predicate adds a GetS to the
             Memory                           Memory
                                                                       Network, and a subsequent transition in the L3 state machine
                 täkō                           täkō                   receives this message from the Network and replies with
   System.Next (s     s')  System.Next (s'    s'')                     the requested data. Thus, an execution trace for a program in
  Tile0.Next Network.Next Network.Next Tile1.Next                      the full state machine is decomposed into individual atomic
                (+ GetS
                   GetS)    (- GetS
                               GetS)     L3.Next                       steps that are taken by its component state machines, alongside
    L2.Next
                            (+ Data
                               Data)   (Read GetS
                                             GetS)
  (Send GetS
        GetS) Others.NoOp                                              Network steps for communication.
                          Others.NoOp (Send Data
                                             Data)
                                                                          Our model currently supports programs with Load, Store,
Fig. 14: Our hierarchical transition system instantiated with          RMW, Flush, and Branch instructions. The execution of
two tiles, executing two transitions (s → s′ and s′ → s′′ ). In        an instruction potentially corresponds to several transitions
the first transition, Tile0’s L2 cache sends a GetS request            that occur in the system (e.g., to request its value from the
into the Network. In the second, Tile1’s L3 cache receives             memory hierarchy). Each instruction is committed using a
said request and responds with a Data message. All other               PerformInst transition in either the Core or Engine
state machines perform a NoOp transition (colored      ).              component state machines, depending on if the instruction is
                                                                       in a program thread or a callback.
                                                                          Our caches are inclusive (enforced by täkō [55]), and kept
          VI. A PARAMETERIZED M ODEL OF T ÄK Ō
                                                                       coherent through a hierarchical directory-based MSI proto-
A. Operational Models                                                  col [46]. The higher protocol has the L2 as a directory and the
                                                                       Core and Engine L1s as children, while the lower protocol
  An operational model is a transition system, which consists
                                                                       has L3 shards as a directory and L2 caches as children.
of a set of states S, as well as two predicates over elements
                                                                       We use the HieraGen [48] approach of a proxy L2 cache to
of this set: an initial state predicate Init(s) that is true when
                                                                       communicate between the two protocols. Our protocols do not
s ∈ S represents a valid initial state, and a transition predicate
                                                                       require point-to-point ordering, as our Network model does
N ext(s, s′ ) that is true for a pair of states s, s′ ∈ S when they
                                                                       not enforce point-to-point ordering for coherence messages.
represent a valid transition from s to s′ .
  We implement our transition system in Dafny [31], a                  C. Model Parameterization
verification-aware language that enables proving properties
                                                                          Our model is parameterized over the size of all caches, the
about programs and abstract models in a partially automated
                                                                       executing program, the number of cores, and the mapping of
way. Dafny converts properties into Satisfiability Modulo
                                                                       addresses to L3 banks. By making these parameters generic
Theories (SMT) queries and then uses Z3 [12] to verify them.
                                                                       instead of concrete values, we ensure that when we prove facts
                                                                       about the transition system (§VII-A), we in fact prove them for
B. täkō State Machine Overview
                                                                       any configuration of these values. This parameterization makes
   Figure 14 depicts the components in our täkō transition           our proof notably harder, as we now cover a wider range of
system, instantiated with two tiles, as well as two example            possibilities. However, our proof becomes much more useful,
transitions. The model is hierarchical: each tile of the täkō chip   as it applies to all configurations of these parameters.
(Figure 3) is its own transition system, consisting of individual
transition systems representing each major component of said           D. Environmental Transitions
tile (the Core + L1, Engine + L1, L2, and L3 slice). A                    In systems like täkō, callback code can execute due to
single Memory state machine represents main memory.                    events like evictions or prefetches. Hardware controls when
   To enable communication between the individual compo-               these events happen, so they may interleave arbitrarily with
nents, we add a state machine called Network to the design,            main program threads. To model such variable timing, we use
which contains all in-flight messages between components.              environmental transitions (transitions that are not dependent
During any individual component transition, a single message           on instructions) [64] to overapproximate cache behavior. Envi-
may be read from or written into the Network (potentially              ronmental transitions decouple memory hierarchy transitions
both). The Network’s internal structure determines which               from the instructions on cores and engines, enabling us to
messages can be delivered during a transition: for coherence           model cases where an instruction triggered a memory request,
messages, this is an unordered set, allowing arbitrary reorder-        as well as cases where the same request was triggered by
ing to overapproximate various network-on-chip designs. For            a prefetch or eviction. Using environmental transitions thus
engine requests, the Network is stricter, enforcing FIFO or-           ensures that our proof of consistency (§VII) is sound even
dering per address on callback requests, as täkō requires [55].      under varied prefetching and cache replacement policies.
   Core + L1                                                                                                             s
     Program
                    Engine                                                                Init(s)
    Load [x]                   Load                   Load
                     + L1                                                                 Reachable(s)
    Load [y]                  needs                   needs
                                                                                                 Inv(s)
                               Data                   Data
                                                                                                    P(s)
                                        Load-Load
 GetS [x] GetS [y]       L2              Ordering                    Fig. 16: A Venn diagram motivating inductive invariants.
   OnEvict [z]           L3                                          Non-reachable states can leave the P (s) set by transitioning
      Network                 No ordering between                    ( X ), so a strengthening Inv(s) is constructed such that any
 Tile0                                                               transition of a state in Inv(s) ( Y ) remains in Inv(s).

Fig. 15: Environmental transitions in action. For the five              Given a state machine and a property P (s), induction
pictured potential transitions, 3 , 4 , and 5 can occur at           requires us to prove two things: a) that the initial state satisfies
any time without any dependencies on each other. The Loads           P (s), and b) that all transitions preserve P (s). This proves that
( 1 , 2 ) are dependent on the Data being in their cache.            P (s) is maintained throughout the execution.
                                                                        Formally, the second obligation is P (s) ∧ N ext(s, s′ ) =⇒
   Figure 15 illustrates environmental transitions in the context    P (s′ )), i.e., if we are in a state satisfying P , any transition
of two loads. Consider modeling a load’s execution if its data is    from that state should lead to another state that satisfies P .
not present in the L1, e.g., the load of [x] in Figure 15. Instead   Alas, this proposition simply does not hold for most systems.
of making the load send a GetS to the L2 state machine, we
                                                                        To understand why, consider Figure 16’s Venn diagram. The
decompose this transition into two independent ones ( 1 and
                                                                     outer rectangle represents all possible states in the system,
 3 in Figure 15). 1 is a PerformLoad step that can only
                                                                     including states not reachable by the state machine. The outer
execute if the data is in the L1, and 3 is a SendGetS step
                                                                     circle represents P (s); i.e., all states s for which P holds. It
that can execute whenever the data is not in the cache. We
                                                                     is possible that a transition like X exists, such that the above
thus capture executions in which a GetS is triggered without
                                                                     implication is violated. This does not mean that our system
a specific load causing it (e.g., on a prefetch), as well as
                                                                     is incorrect, as X originates in an unreachable state and is
executions where the events are causally linked. Thus, even
                                                                     thus a spurious counterexample. But it does mean we cannot
though Figure 15 has the load of [x] ( 1 ) before the load of [y]
                                                                     directly use P in our inductive proof.
( 2 ) in program order, their requests to the memory hierarchy
                                                                        Instead, we use an inductive invariant (Inv(s) in Figure 16),
( 3 and 4 ) are not ordered with respect to each other due to
                                                                     a strengthening of P (s) (i.e., Inv(s) =⇒ P (s)) which is
environmental transitions, as they could be prefetched out of
                                                                     always preserved under N ext (as exemplified by Y ). Our
order. Callback scheduling and running are also environmental
                                                                     proof obligation is then to show that Inv(s)∧N ext(s, s′ ) =⇒
transitions, since misses, evictions, and writebacks can occur
                                                                     Inv(s′ ) and Init(s) =⇒ Inv(s). This ensures that P (s)
arbitrarily. Thus, the eviction of [z] ( 5 ) in Figure 15 can also
                                                                     holds throughout the execution, because Inv(s) =⇒ P (s).
be interleaved with other transitions arbitrarily.
                                                                     Finding an inductive invariant for a system is a key challenge
   We allow callback environmental transitions to repeat if
                                                                     when verifying a system inductively [36, 50, 70].
their preconditions are met. For instance, our model can exe-
cute repeated OnMiss-OnEvict sequences for an address [x]            B. Intermediate State Machine
without a core ever requesting [x]. This is because a prefetch
could bring [x] in and the cache could then evict it at any time.       We wish to demonstrate via induction that each axiom in
Allowing such loops enables our model to overapproximate             our MCM holds for all executions. However, recall that axioms
replacement policy or prefetcher-based triggering of callbacks       are properties of execution graphs, meaning they hold for a full
that might cause unexpected outcomes. Our proof in §VII is           execution of a program. In contrast, our operational model is a
valid across all such callback combinations.                         transition system that incrementally builds the execution with
                                                                     each transition. Inductive proofs (§VII-A) require a property
    VII. A M ACHINE -C HECKED C ONSISTENCY P ROOF                    to hold during these intermittent stages as well. Thus, we first
  Here, we describe how we produce a machine-checked, all-           need a notion of a partial execution graph which represents
program proof that our täkō ISA-level MCM (§IV) is sound           the execution graph of a program that has not yet completed
with respect to our model of the täkō hardware (§VI).              running. To that end, we first build an intermediate state
                                                                     machine (henceforth ISM for short) that is much simpler than
A. Proof by Induction                                                the operational model in §VI. The state of this ISM includes
   Induction is a powerful proof technique that can prove            a partial execution graph for a program, and its transitions
properties about infinite executions of a state machine while        represent how running a program updates this graph. We then
only reasoning about one transition at a time. In the realm of       require that each axiom, when strengthened with an inductive
hardware, where many designs are modeled as state machines,          invariant (§VII-A), is true for the partial graph at Init(s), and
this approach is broadly applicable [13, 51, 56, 63].                is preserved by N ext’s additions to these partial graphs.
                                          Axiom1: "Every       has a          and remains consistent as it produces a complete execution
                                             corresponding      "             trace. We leverage this same property in a new way: to ensure
                                           (not prefix-closed)
                                                                              axioms about our system, when true about full executions,
                                           Axiom2: "Between every pair of     are always provable on a state machine representation of the
                                                    there is an  "
Partial Execution        Partial Execution       (prefix-closed)              hardware using inductive verification. This approach can be
  Graph at s1              Graph at s2                                        applied for general proofs of hardware correctness against
  End       No    for the s              End                      s           prefix-closed MCM axioms. As such, future designers of
 OnMiss       new     !                 OnMiss
                                                                              MCMs should strive for axioms that respect this property to
                                                             s1               unlock this method of MCM verification.
   Reachable(s)           s1
                                                      s2
                    s2                                     s0
                         s0                   Reachable(s)                    D. Proof Architecture: Dividing the Proof Obligation
           Axiom1(s)            Start                              Start
                               OnMiss
                                                 Axiom2(s)
                                                                  OnMiss
                                                                                 Figure 18 illustrates the two forms of reasoning in our end-
                                                                              to-end proof. First, one must reason ( I ) about the ISM itself
Fig. 17: Two formulations of an axiom restricting the number                  (§VII-B) to determine if it satisfies the axiom we are verifying
of Ms and Me events in an execution graph. While both are                     using induction (§VII-A). Second, one must connect ( R ) the
true about full executions of our operational model, Axiom1                   ISM with the operational model to ensure that the ISM is a
is not provable using induction, because there are transitions                faithful representation of the hardware.
from reachable states (e.g., s0 → s1) where Axiom1 tem-                          Previous work has separated these two forms of reasoning
porarily fails to hold. Axiom2 (MeInt in our MCM), phrased                    by introducing an intermediate state machine that builds partial
in a prefix-closed manner, avoids this issue by ensuring that                 execution graphs [5, 25, 47, 64], and demonstrating that the
the axiom holds for all reachable partial executions as well.                 axioms hold for each generated partial execution. Some of
                                                                              these works [5] performed a machine-checked proof of I
C. Using Prefix-Closure To Ensure Provable Axioms                             by showing that the ISM produces exactly the set of all
   A key potential pitfall with this inductive approach is that               axiomatically consistent outcomes. However, the proof that
certain axioms can be true about the final, full execution graph,             the executions of the operational model correspond to those
but fail to hold for partial graphs along the way. For example,               of the ISM ( R ) was done by hand, an error-prone approach
an axiom we originally added to our model expressed the                       that has historically missed bugs [28, 41, 65].
property that for each Ms node in the graph, there was a                         In contrast, we machine-check both parts, constructing an
corresponding Me that belonged to the same thread. An axiom                   end-to-end machine-checked proof of axiomatic consistency.
like this was needed to outlaw full executions where there                    The feasibility of machine-checking the entire proof is facili-
were more Ms events than Me events; such executions are                       tated by the decoupling of concerns that allows the two proofs
impossible, as an OnMiss requires both an Ms and an Me .                      to focus on different aspects of correctness in a modular way:
   Figure 17 illustrates why this axiom (Axiom1) cannot be                    the refinement proof (§VII-E) focuses solely on abstracting
verified despite being true. Consider the transition which adds               away the internals of data movement through layers of the
an Ms to the ISM’s partial execution graph, representing                      caches and the engine running in the operational model, while
an OnMiss starting in the engine. As this callback has not                    the proof of axiomatic consistency only reasons about how
completed, its associated Me has not yet been added. As such,                 adding events to the execution graph changes its structure.
while Axiom1 is valid for full executions, it cannot be proven
by standard induction as it fails to hold for a partial execution             E. Connecting the ISM and Operational Model via Refinement
graph after a transition from a reachable state (s0 → s1).                       The goal of the refinement proof is to demonstrate that any
   To remedy this, a key feature of the axiom set we design in                execution trace of the operational model (§VI) corresponds to
§IV is that each axiom is prefix-closed: that is, if it holds for             an ISM execution trace that produces partial execution graphs.
the full execution, it will hold for all partial executions along                What complicates this is the detail in the operational model:
its construction (its prefixes)2 . This property has a remarkable             most transitions do not update the execution graph but still
consequence for inductive verification: if an axiom is prefix-                meaningfully impact the state for transitions that do. Figure 18
closed and true about the system, one can always find an                      shows this disconnect in an execution snippet of Figure 4a’s
inductive invariant to prove it. For our system, we changed                   program. While the operational model performs four transi-
Axiom1 to Axiom2, which states that for every pair of Ms ,                    tions (s1 → s5), only two of them (ending an OnWB (s1 → s2)
there exists an Me in between them (MeInt in Figure 6). This                  and starting an OnMiss (s4 → s5)) update the execution
accomplishes the same goal, but is also true when an OnMiss                   graph. In contrast, when the L3 sends an OnMiss request
is partially complete, and thus can be verified inductively.                  to the Network (s2 → s3) and the Engine receives it
   Prior work [25, 47] has used prefix-closure for its axiom sets             (s3 → s4), the graph is not updated (as our MCM is at ISA
to ensure that its construction of partial execution graphs starts            level and does not model unnecessary hardware details).
  2 Prefix-closure in the literature is typically defined with respect to a
                                                                                 However, these internal steps are still pivotal to correctness:
commitment order: our commitment order respects cbo, meaning we never         when the Engine later starts an OnMiss (s4 → s5), the
add callback events to the graph in an order that violates cbo.               address for which it runs and the cache line it populates are
     Inv(abs(s1))                 Inv(abs(s2))                                                      Inv(abs(s5))

                     Add                                                                  Add
                                                                                                                        Axioms hold
                     to Execution Graph             NoOp              NoOp             to Execution Graph                inductively
          abs(s1)                         abs(s2)          abs(s2)           abs(s2)                        abs(s5)        §

Abstraction
 Function                                        Send OnMiss     Receive OnMiss
  (abs)                End OnWB [x]                (internal)       (internal)         Start OnMiss [x]                 Refinement
              s1                            s2                  s3             s4                             s5
                                                                                                                         §
Fig. 18: The two components of our soundness proof. R The refinement proof (§VII-E) proves that each operational model
execution (e.g., s1 → s5), abstracted at each state, maps to an intermediate state machine execution (e.g., abs(s1) → abs(s5)).
Operational model transitions either add nodes to the partial execution graph (e.g., s1 → s2) or are internal steps that abstract
up to NoOps (e.g., s2 → s3). I The inductive proof that the axioms hold as the partial execution graph grows (§VII-B).

determined by the message it receives from the Network,              verification of hardware implementations includes bounded
which in turn is determined by the previous internal steps.          proofs [33, 35, 39, 40, 69] and complete (all-program) [10, 11,
   Figure 18 shows how refinement reasons about correctness          30, 38, 62, 64] proofs. Some prior hardware verification work
in the presence of internal steps. We first define an abstraction    uses an intermediate state machine to decompose the proof [5,
function abs that, for any s of the täkō operational model         64]. However, none of these prior decomposed proofs are
produces an equivalent state in the ISM. Then we show via            completely machine-checked like ours. Refinement has been
induction that for any transition s → s′ of the operational          used to verify hardware [10, 11, 30] as well as distributed and
model, abs(s) → abs(s′ ) is either a valid ISM transition (e.g.,     operating systems [15, 17, 18, 23, 26, 32, 66]. Pensieve [67]
s1 → s2), or makes no change to the graph (e.g., s2 → s3).           uses uninterpreted functions to overapproximate microarchi-
   As we prove refinement through induction, this involves           tectural security behavior, similar to how we overapproximate
proving an inductive invariant which shows that the added            cache behavior using environmental transitions (§VI-D). Our
complexity of caches and Network communication does not              environmental transitions are inspired by Wickerson et al. [64].
change the underlying behavior of the system.                           Programmable Memory Hierarchies: Programmable
   Our proof assumes certain basic properties about our coher-       memory hierarchies give software greater control over data
ence protocol to avoid having to prove coherence in addition         movement through the memory hierarchy [27, 43, 44, 54, 55],
to correspondence between our täkō implementation model            and can improve performance and energy efficiency.
and our ISA-level MCM. We do so because the coherence
protocol we use is well-studied and is known to provide                                    IX. C ONCLUSION
coherence [46, 48]. Additionally, the coherence protocol in              We develop a MCM for the täkō PMH, enabling program-
a täkō system is tangential to täkō’s novel features: after      mers to reason about täkō programs without understanding
phantom data is received from the engine and populates an            täkō’s implementation details. We also construct a microar-
entry in the directory-level cache, the data is indistinguishable    chitectural täkō model that is parameterized over prefetch-
from data fetched from memory to the coherence protocol.             ing policies, cache replacement policies, and network-on-
   We explicitly model all protocol transient states and their       chip specifics. This model enables architects to change these
interaction with täkō, thus verifying any coherence-consistency    features in their täkō design to improve performance without
interface [40] issues that might arise. For example, we verify       compromising correctness. Finally, we prove our MCM sound
that the dirty bit at directory level is accurately preserved by     against our microarchitectural model across all programs, thus
the coherence protocol, to ensure that OnEvict and OnWB              verifying that our MCM accurately represents täkō.
are invoked appropriately. Even assuming coherence, our proof            Our formalization also discovers two more general insights.
still required adding 119 clauses to our inductive invariant and     First, when creating an ISA-level MCM, ensuring prefix-
61K LoC of proof annotations.                                        closure for its axioms makes the MCM amenable to inductive
                                                                     correctness proofs. Second, microarchitectural models should
                   VIII. R ELATED W ORK                              (and can) serve the needs of both architects and formal
   High-Level Language (HLL) and ISA MCMs: There is a                methods experts, as our microarchitectural model of täkō does.
long line of work that models various ISA and HLL MCMs [2,
3, 5, 9, 34, 37, 42, 49, 52, 53]. Prior work on such models                              ACKNOWLEDGMENTS
highlighted prefix-closure as a useful property [25, 47]. There         We thank the anonymous reviewers and our shepherd
have been a few papers on MCMs and coherence for novel               for their helpful feedback. We thank Brian Schwedock and
hardware [6, 58, 68], but more research in this area is needed.      Nathan Beckmann for clarifying certain täkō implementation
   Hardware Models and Proofs: There has also been much              details. This work was supported in part by National Science
work on formally modeling hardware designs using a variety           Foundation grant CCF-2318954. GitHub Copilot was used
of representations [10, 11, 33, 35, 57, 64, 68]. Work on formal      for mundane code autocomplete and generation (e.g., find &
replace) in our Dafny proofs. (We handwrote the vast majority                3) Software dependencies: Installations of Dafny 4.11.0
of our proofs.)                                                           and Alloy 6.2.0 are required to run the verification scripts.
                                                                          The README contains detailed instructions and links for
                      A RTIFACT A PPENDIX                                 installation instructions.

A. Abstract                                                               D. Installation
  This artifact contains two major components:                               Other than software dependencies mentioned above, no
  1) A Dafny end-to-end machine checked proof of axiomatic                installation is necessary. The files in the repository can be
     consistency for a state machine representation of the täkō         verified using the included bash scripts.
     hardware (§VII), which can be explicitly verified.
  2) An Alloy encoding of the axioms (Figure 6) along with                E. Evaluation and expected results
     the täkō litmus tests presented in the paper, which can
                                                                             The two provided scripts correspond to the 2 components of
     be run to confirm the results presented in the paper are
                                                                          the artifact. Running the run_alloy_tests.sh script will
     consistent with our axioms.
                                                                          iterate through the litmus tests in the repository and confirm
                                                                          the expected outcomes claimed for these tests in the paper.
B. Artifact check-list (meta-information)
                                                                          A full table of these is included below, as well as in the
  • Run-time environment: Tested on Windows 11 Enterprise                 README.
    23H2, with Dafny 4.11.0 and Alloy 6.2.0. Dafny on Windows
    requires .NET installation. Alloy requires Java (JVM 17+, tested             Figure       Claimed Result          File (.als)
    with JVM 24.0.1).                                                                         r1 = 2, r2 = 0
  • Hardware: Tested on 12th Gen Intel(R) Core i7-1280P Win-
                                                                                Figure 4a                         test_paper_ex
                                                                                                 forbidden
    dows Laptop with 32 GB RAM.
  • Metrics: Machine-Checked Proof Verification; confirming Lit-
                                                                                              r1 = 1, r2 = 0
                                                                                Figure 5a                              test_mp
    mus Test outcomes for Axiomatic Model.                                                    allowed (§V-A)
  • Output:      Scripts will output results to the console. Dafny            Figure 9a       r1 = 1, r2 = 0
    proof expected result: verification script succeeds. Alloy model                                                test_mp_rmw
                                                                           (w/o OnMiss)          forbidden
    expected result: Alloy execution matches expected result printed          Figure 9a       r1 = 1, r2 = 0
    by script.                                                                                                    test_mp_rmwcb
  • Experiments:        Experiment setup and listing included in            (w/ OnMiss)          forbidden
    README file.                                                                              r1 = 0, r2 = 0
                                                                                Figure 10a                          test_icb_sb
  • How much disk space required (approximately)?: With a                                         allowed
    Dafny installation and Alloy Installation, the full repository size         Figure 11a
    is ∼180 MB.                                                                                     racy            test_wbrace
                                                                                 (w/o i2))
  • How much time is needed to prepare workflow (approxi-
    mately)?: Around 15 minutes. (installing Dafny + Alloy, Java                               a) no race
                                                                                Figure 11a
    and potentially .NET).                                                                     b) r1 = 0           test_wbflush
  • How much time is needed to complete experiments (approx-
                                                                                 (w/ i2))
                                                                                                  forbidden
    imately)?: Around 1.5 hours.                                             Figure 12a
  • Publicly available?: Yes, on GitHub.                                                            racy             test_phir
  • Code licenses (if publicly available)?: MIT License (included
                                                                            (w/ OnWB 1))
    in repository).                                                                           a) no race
                                                                             Figure 12a
  • Workflow automation framework used?: Bash Scripts.                                        b) r1 = 0, r2 = 0      test_phinr
  • Archived (provide DOI)?:            Version 1.1.1 uploaded to           (w/ OnWB 2))
                                                                                                 forbidden
    https://doi.org/10.5281/zenodo.19444275                                     Figure 13a
                                                                                                    racy             test_hatsr
                                                                                 (w/o i9))
C. Description                                                                                 a) no race
                                                                                Figure 13a
   1) How       to    access:     The     artifact    can     be                               b) r1 ̸= r2          test_hatsnr
                                                                                 (w/ i9))
cloned       from       the     GitHub        Repository      at                                  forbidden
https://github.com/GenericMonkey/takoFormal. The following                Running the run_dafny_verification.sh script will
instructions are all found in the README of this repository               verify all the Dafny files that make up the end-to-end proof
as well.                                                                  discussed in §VII. The translation of each axiom presented in
   2) Hardware dependencies: The submitted artifact has been              Figure 6 to its corresponding file is included in the README.
tested on an 12th Gen Intel(R) Core(TM) i7-1280P Windows
Laptop (32 GB RAM) running Windows 11 Enterprise 23H2.                    F. Methodology
The tools are available for other operating systems and the
results should be portable, but there are known brittleness                 Submission, reviewing and badging methodology:
issues with Dafny in particular across different systems. If the            • https://www.acm.org/publications/policies/
scripts are used on a different architecture and certain proofs               artifact-review-and-badging-current
timeout or face internal errors, please contact.                            • https://cTuning.org/ae
                             R EFERENCES                                       [15] R. Gu, Z. Shao, H. Chen, X. Wu, J. Kim, V. Sjöberg, and D. Costanzo,
                                                                                    “CertiKOS: an extensible architecture for building certified concurrent
 [1] S. Adve and K. Gharachorloo, “Shared memory consistency models: A              OS kernels,” in Proceedings of the 12th USENIX conference on Operat-
     tutorial,” IEEE Computer, vol. 29, no. 12, pp. 66–76, 1996.                    ing Systems Design and Implementation, ser. OSDI’16. USA: USENIX
 [2] S. V. Adve and M. D. Hill, “Weak ordering—a new definition,”                   Association, Nov. 2016, pp. 653–669.
     in Proceedings of the 17th Annual International Symposium on              [16] S. Gulwani, O. Polozov, and R. Singh, “Program synthesis,” Foundations
     Computer Architecture, ser. ISCA ’90. New York, NY, USA:                       and Trends® in Programming Languages, vol. 4, no. 1-2, pp. 1–119,
     Association for Computing Machinery, 1990, p. 2–14. [Online].                  2017. [Online]. Available: http://dx.doi.org/10.1561/2500000010
     Available: https://doi.org/10.1145/325164.325100                          [17] C. Hawblitzel, J. Howell, M. Kapritsos, J. R. Lorch, B. Parno, M. L.
 [3] J. Alglave, M. Batty, A. F. Donaldson, G. Gopalakrishnan, J. Ketema,           Roberts, S. Setty, and B. Zill, “IronFleet: proving practical distributed
     D. Poetzl, T. Sorensen, and J. Wickerson, “GPU Concurrency:                    systems correct,” in Proceedings of the 25th Symposium on Operating
     Weak Behaviours and Programming Assumptions,” in Proceedings                   Systems Principles. Monterey California: ACM, Oct. 2015, pp. 1–17.
     of the Twentieth International Conference on Architectural Support             [Online]. Available: https://dl.acm.org/doi/10.1145/2815400.2815428
     for Programming Languages and Operating Systems. Istanbul                 [18] C. Hawblitzel, J. Howell, J. R. Lorch, A. Narayan, B. Parno, D. Zhang,
     Turkey: ACM, Mar. 2015, pp. 577–591. [Online]. Available: https:               and B. Zill, “Ironclad apps: end-to-end security via automated full-
     //dl.acm.org/doi/10.1145/2694344.2694391                                       system verification,” in Proceedings of the 11th USENIX conference on
 [4] J. Alglave, L. Maranget, S. Sarkar, and P. Sewell, “Fences in Weak             Operating Systems Design and Implementation, ser. OSDI’14. USA:
     Memory Models,” in Computer Aided Verification, D. Hutchison,                  USENIX Association, Oct. 2014, pp. 165–181.
     T. Kanade, J. Kittler, J. M. Kleinberg, F. Mattern, J. C. Mitchell,       [19] M. D. Hill and V. J. Reddi, “Accelerator-level parallelism,”
     M. Naor, O. Nierstrasz, C. Pandu Rangan, B. Steffen, M. Sudan,                 Communications of the ACM, vol. 64, no. 12, pp. 36–38, Dec. 2021.
     D. Terzopoulos, D. Tygar, M. Y. Vardi, G. Weikum, T. Touili,                   [Online]. Available: https://dl.acm.org/doi/10.1145/3460970
     B. Cook, and P. Jackson, Eds. Berlin, Heidelberg: Springer                [20] M. Horowitz, M. Martonosi, T. C. Mowry, and M. D. Smith, “Informing
     Berlin Heidelberg, 2010, vol. 6174, pp. 258–272, series Title:                 memory operations: providing memory performance feedback in modern
     Lecture Notes in Computer Science. [Online]. Available: http:                  processors,” in Proceedings of the 23rd annual international symposium
     //link.springer.com/10.1007/978-3-642-14295-6 25                               on Computer architecture, ser. ISCA ’96. New York, NY, USA:
 [5] J. Alglave, L. Maranget, and M. Tautschnig, “Herding Cats: Modelling,          Association for Computing Machinery, May 1996, pp. 260–270.
     Simulation, Testing, and Data Mining for Weak Memory,” ACM                     [Online]. Available: https://dl.acm.org/doi/10.1145/232973.233000
     Transactions on Programming Languages and Systems, vol. 36, no. 2,
                                                                               [21] D. Jackson, “Alloy: a lightweight object modelling notation,” ACM
     pp. 7:1–7:74, Jul. 2014. [Online]. Available: https://doi.org/10.1145/
                                                                                    Trans. Softw. Eng. Methodol., vol. 11, no. 2, pp. 256–290, Apr. 2002.
     2627752
                                                                                    [Online]. Available: https://dl.acm.org/doi/10.1145/505145.505149
 [6] G. Ambal, B. Dongol, H. Eran, V. Klimis, O. Lahav, and A. Raad,
     “Semantics of Remote Direct Memory Access: Operational and                [22] N. Jouppi, G. Kurian, S. Li, P. Ma, R. Nagarajan, L. Nai, N. Patil,
     Declarative Models of RDMA on TSO Architectures,” Proc. ACM                    S. Subramanian, A. Swing, B. Towles, C. Young, X. Zhou, Z. Zhou, and
     Program. Lang., vol. 8, no. OOPSLA2, pp. 341:1982–341:2009, Oct.               D. A. Patterson, “Tpu v4: An optically reconfigurable supercomputer
     2024. [Online]. Available: https://dl.acm.org/doi/10.1145/3689781              for machine learning with hardware support for embeddings,”
                                                                                    in Proceedings of the 50th Annual International Symposium on
 [7] ARM, “Cortex-A9 MPCore Programmer Advice Notice Read-after-
                                                                                    Computer Architecture, ser. ISCA ’23. New York, NY, USA:
     Read Hazards,” ARM, Arm Reference 761319, 2011. [Online].
                                                                                    Association for Computing Machinery, 2023. [Online]. Available:
     Available: https://developer.arm.com/documentation/uan0004/a/
                                                                                    https://doi.org/10.1145/3579371.3589350
 [8] M. Batty, A. F. Donaldson, and J. Wickerson, “Overhauling SC
     Atomics in C11 and OpenCL,” in Proceedings of the 43rd Annual             [23] G. Klein, T. Sewell, and S. Winwood, “Refinement in the Formal
     ACM SIGPLAN-SIGACT Symposium on Principles of Programming                      Verification of the seL4 Microkernel,” in Design and Verification
     Languages, Jan. 2016, pp. 634–648, arXiv:1503.07073 [cs]. [Online].            of Microprocessor Systems for High-Assurance Applications, D. S.
     Available: http://arxiv.org/abs/1503.07073                                     Hardin, Ed. Boston, MA: Springer US, 2010, pp. 323–339. [Online].
 [9] M. Batty, S. Owens, S. Sarkar, P. Sewell, and T. Weber, “Mathematizing         Available: https://doi.org/10.1007/978-1-4419-1539-9 11
     C++ concurrency,” in Proceedings of the 38th annual ACM SIGPLAN-          [24] P. Kocher, J. Horn, A. Fogh, D. Genkin, D. Gruss, W. Haas,
     SIGACT symposium on Principles of programming languages, ser.                  M. Hamburg, M. Lipp, S. Mangard, T. Prescher, M. Schwarz,
     POPL ’11. New York, NY, USA: Association for Computing                         and Y. Yarom, “Spectre Attacks: Exploiting Speculative Execution,”
     Machinery, Jan. 2011, pp. 55–66. [Online]. Available: https://doi.org/         in 2019 IEEE Symposium on Security and Privacy (SP), May
     10.1145/1926385.1926394                                                        2019, pp. 1–19, iSSN: 2375-1207. [Online]. Available: https:
[10] J. R. Burch and D. L. Dill, “Automatic verification of Pipelined Micro-        //ieeexplore.ieee.org/document/8835233
     processor Control,” in Proceedings of the 6th International Conference    [25] M. Kokologiannakis, O. Lahav, K. Sagonas, and V. Vafeiadis, “Effective
     on Computer Aided Verification, ser. CAV ’94. Berlin, Heidelberg:              stateless model checking for C/C++ concurrency,” Proceedings of the
     Springer-Verlag, Jun. 1994, pp. 68–80.                                         ACM on Programming Languages, vol. 2, no. POPL, pp. 1–32, Jan.
[11] J. Choi, M. Vijayaraghavan, B. Sherman, A. Chlipala, and Arvind,               2018. [Online]. Available: https://dl.acm.org/doi/10.1145/3158105
     “Kami: a platform for high-level parametric hardware specification and    [26] B. Kragl and S. Qadeer, “The civl verifier,” in 2021 Formal Methods in
     its modular verification,” Proceedings of the ACM on Programming               Computer Aided Design (FMCAD), 2021, pp. 143–152.
     Languages, vol. 1, no. ICFP, pp. 24:1–24:30, Aug. 2017. [Online].         [27] J. Kuskin, D. Ofelt, M. Heinrich, J. Heinlein, R. Simoni,
     Available: https://doi.org/10.1145/3110268                                     K. Gharachorloo, J. Chapin, D. Nakahira, J. Baxter, M. Horowitz,
[12] L. de Moura and N. Bjørner, “Z3: An Efficient SMT Solver,” in Tools            A. Gupta, M. Rosenblum, and J. Hennessy, “The Stanford FLASH
     and Algorithms for the Construction and Analysis of Systems, C. R.             multiprocessor,” in Proceedings of 21 International Symposium on
     Ramakrishnan and J. Rehof, Eds. Berlin, Heidelberg: Springer, 2008,            Computer Architecture, Apr. 1994, pp. 302–313. [Online]. Available:
     pp. 337–340.                                                                   https://ieeexplore.ieee.org/abstract/document/288140?casa token=
[13] M. R. Fadiheh, A. Wezel, J. Muller, J. Bormann, S. Ray, J. M.                  6LrIkfTALWcAAAAA:pMvOhg3kx7qh dYOzL g GXWtYgGmqGU
     Fung, S. Mitra, D. Stoffel, and W. Kunz, “ An Exhaustive                       XJJeGnJah1eq4Wz9M8i28LPSkZXRkdiUiIPWrQw
     Approach to Detecting Transient Execution Side Channels in                [28] O. Lahav, V. Vafeiadis, J. Kang, C.-K. Hur, and D. Dreyer, “Repairing
     RTL Designs of Processors ,” IEEE Transactions on Computers,                   sequential consistency in C/C++11,” in Proceedings of the 38th
     vol. 72, no. 01, pp. 222–235, Jan. 2023. [Online]. Available:                  ACM SIGPLAN Conference on Programming Language Design and
     https://doi.ieeecomputersociety.org/10.1109/TC.2022.3152666                    Implementation, ser. PLDI 2017. New York, NY, USA: Association
[14] K. Gharachorloo, D. Lenoski, J. Laudon, P. Gibbons, A. Gupta, and              for Computing Machinery, Jun. 2017, pp. 618–632. [Online]. Available:
     J. Hennessy, “Memory consistency and event ordering in scalable                https://doi.org/10.1145/3062341.3062352
     shared-memory multiprocessors,” in Proceedings of the 17th Annual         [29] Lamport, “How to Make a Multiprocessor Computer That Correctly
     International Symposium on Computer Architecture, ser. ISCA ’90.               Executes Multiprocess Programs,” IEEE Transactions on Computers,
     New York, NY, USA: Association for Computing Machinery, 1990, p.               vol. C-28, no. 9, pp. 690–691, Sep. 1979. [Online]. Available:
     15–26. [Online]. Available: https://doi.org/10.1145/325164.325102              https://ieeexplore.ieee.org/document/1675439
[30] S. Lau, T. Bourgeat, C. Pit-Claudel, and A. Chlipala, “Specification          Mappings,” Nov. 2016, arXiv:1611.01507 [cs]. [Online]. Available:
     and verification of strong timing isolation of hardware enclaves,” in         http://arxiv.org/abs/1611.01507
     Proceedings of the 2024 on ACM SIGSAC Conference on Computer             [42] J. Manson, W. Pugh, and S. V. Adve, “The Java memory model,”
     and Communications Security, ser. CCS ’24. New York, NY, USA:                 in Proceedings of the 32nd ACM SIGPLAN-SIGACT Symposium on
     Association for Computing Machinery, 2024, p. 1121–1135. [Online].            Principles of Programming Languages, ser. POPL ’05. New York,
     Available: https://doi.org/10.1145/3658644.3690203                            NY, USA: Association for Computing Machinery, 2005, p. 378–391.
[31] K. R. M. Leino, “Dafny: An Automatic Program Verifier for Functional          [Online]. Available: https://doi.org/10.1145/1040305.1040336
     Correctness,” in Logic for Programming, Artificial Intelligence, and     [43] A. Mukkara, N. Beckmann, M. Abeydeera, X. Ma, and D. Sanchez,
     Reasoning, E. M. Clarke and A. Voronkov, Eds. Berlin, Heidelberg:             “Exploiting Locality in Graph Analytics through Hardware-Accelerated
     Springer Berlin Heidelberg, 2010, vol. 6355, pp. 348–370, series              Traversal Scheduling,” in 2018 51st Annual IEEE/ACM International
     Title: Lecture Notes in Computer Science. [Online]. Available:                Symposium on Microarchitecture (MICRO), Oct. 2018, pp. 1–
     http://link.springer.com/10.1007/978-3-642-17511-4 20                         14. [Online]. Available: https://ieeexplore.ieee.org/abstract/document/
[32] J. R. Lorch, Y. Chen, M. Kapritsos, B. Parno, S. Qadeer, U. Sharma,           8574527
     J. R. Wilcox, and X. Zhao, “Armada: low-effort verification of           [44] A. Mukkara, N. Beckmann, and D. Sanchez, “PHI: Architectural Support
     high-performance concurrent programs,” in Proceedings of the 41st             for Synchronization- and Bandwidth-Efficient Commutative Scatter
     ACM SIGPLAN Conference on Programming Language Design and                     Updates,” in Proceedings of the 52nd Annual IEEE/ACM International
     Implementation, ser. PLDI 2020. New York, NY, USA: Association                Symposium on Microarchitecture, ser. MICRO ’52. New York, NY,
     for Computing Machinery, Jun. 2020, pp. 197–210. [Online]. Available:         USA: Association for Computing Machinery, Oct. 2019, pp. 1009–1022.
     https://doi.org/10.1145/3385412.3385971                                       [Online]. Available: https://dl.acm.org/doi/10.1145/3352460.3358254
[33] D. Lustig, M. Pellauer, and M. Martonosi, “PipeCheck: Specifying         [45] V. Nagarajan and R. Gupta, “ECMon: exposing cache events for
     and Verifying Microarchitectural Enforcement of Memory Consistency            monitoring,” SIGARCH Comput. Archit. News, vol. 37, no. 3, pp.
     Models,” in Proceedings of the 47th Annual IEEE/ACM International             349–360, Jun. 2009. [Online]. Available: https://dl.acm.org/doi/10.1145/
     Symposium on Microarchitecture, ser. MICRO-47. USA: IEEE                      1555815.1555798
     Computer Society, Dec. 2014, pp. 635–646. [Online]. Available:           [46] V. Nagarajan, D. J. Sorin, M. D. Hill, and D. A. Wood, A
     https://dl.acm.org/doi/10.1109/MICRO.2014.38                                  Primer on Memory Consistency and Cache Coherence, ser. Synthesis
[34] D. Lustig, S. Sahasrabuddhe, and O. Giroux, “A Formal Analysis                Lectures on Computer Architecture. Cham: Springer International
     of the NVIDIA PTX Memory Consistency Model,” in Proceedings                   Publishing, 2020. [Online]. Available: https://link.springer.com/10.1007/
     of the Twenty-Fourth International Conference on Architectural                978-3-031-01764-3
     Support for Programming Languages and Operating Systems, ser.            [47] K. Nienhuis, K. Memarian, and P. Sewell, “An operational semantics
     ASPLOS ’19. New York, NY, USA: Association for Computing                      for C/C++11 concurrency,” in Proceedings of the 2016 ACM SIGPLAN
     Machinery, Apr. 2019, pp. 257–270. [Online]. Available: https:                International Conference on Object-Oriented Programming, Systems,
     //dl.acm.org/doi/10.1145/3297858.3304043                                      Languages, and Applications. Amsterdam Netherlands: ACM, Oct.
                                                                                   2016, pp. 111–128. [Online]. Available: https://dl.acm.org/doi/10.1145/
[35] D. Lustig, G. Sethi, M. Martonosi, and A. Bhattacharjee, “COATCheck:
                                                                                   2983990.2983997
     Verifying Memory Ordering at the Hardware-OS Interface,” in
     Proceedings of the Twenty-First International Conference on              [48] N. Oswald, V. Nagarajan, and D. J. Sorin, “HieraGen: Automated
     Architectural Support for Programming Languages and Operating                 Generation of Concurrent, Hierarchical Cache Coherence Protocols,” in
     Systems. Atlanta Georgia USA: ACM, Mar. 2016, pp. 233–247.                    2020 ACM/IEEE 47th Annual International Symposium on Computer
     [Online]. Available: https://dl.acm.org/doi/10.1145/2872362.2872399           Architecture (ISCA). Valencia, Spain: IEEE, May 2020, pp. 888–899.
                                                                                   [Online]. Available: https://ieeexplore.ieee.org/document/9138912/
[36] H. Ma, A. Goel, J.-B. Jeannin, M. Kapritsos, B. Kasikci, and
                                                                              [49] S. Owens, S. Sarkar, and P. Sewell, “A Better x86 Memory
     K. A. Sakallah, “I4: incremental inference of inductive invariants for
                                                                                   Model: x86-TSO,” in Theorem Proving in Higher Order Logics,
     verification of distributed protocols,” in Proceedings of the 27th ACM
                                                                                   S. Berghofer, T. Nipkow, C. Urban, and M. Wenzel, Eds. Berlin,
     Symposium on Operating Systems Principles, ser. SOSP ’19. New
                                                                                   Heidelberg: Springer Berlin Heidelberg, 2009, vol. 5674, pp. 391–407,
     York, NY, USA: Association for Computing Machinery, 2019, p.
                                                                                   series Title: Lecture Notes in Computer Science. [Online]. Available:
     370–384. [Online]. Available: https://doi.org/10.1145/3341301.3359651
                                                                                   http://link.springer.com/10.1007/978-3-642-03359-9 27
[37] S. Mador-Haim, L. Maranget, S. Sarkar, K. Memarian, J. Alglave,          [50] O. Padon, K. L. McMillan, A. Panda, M. Sagiv, and S. Shoham,
     S. Owens, R. Alur, M. M. K. Martin, P. Sewell, and D. Williams,               “Ivy: safety verification by interactive generalization,” in Proceedings
     “An Axiomatic Memory Model for POWER Multiprocessors,” in                     of the 37th ACM SIGPLAN Conference on Programming Language
     Computer Aided Verification, D. Hutchison, T. Kanade, J. Kittler,             Design and Implementation, ser. PLDI ’16. New York, NY, USA:
     J. M. Kleinberg, F. Mattern, J. C. Mitchell, M. Naor, O. Nierstrasz,          Association for Computing Machinery, 2016, p. 614–630. [Online].
     C. Pandu Rangan, B. Steffen, M. Sudan, D. Terzopoulos, D. Tygar,              Available: https://doi.org/10.1145/2908080.2908118
     M. Y. Vardi, G. Weikum, P. Madhusudan, and S. A. Seshia, Eds.            [51] R. Peled, D. Kroening, M. Tautschnig, and Y. Vizel, “Large Lemma
     Berlin, Heidelberg: Springer Berlin Heidelberg, 2012, vol. 7358, pp.          Miners: Can LLMs do Induction Proofs for Hardware?” Nov. 2025,
     495–512, series Title: Lecture Notes in Computer Science. [Online].           arXiv:2511.02521 [cs]. [Online]. Available: http://arxiv.org/abs/2511.
     Available: http://link.springer.com/10.1007/978-3-642-31424-7 36              02521
[38] Y. A. Manerkar, D. Lustig, M. Martonosi, and A. Gupta, “PipeProof:       [52] C. Pulte, S. Flur, W. Deacon, J. French, S. Sarkar, and P. Sewell,
     Automated Memory Consistency Proofs for Microarchitectural Specifi-           “Simplifying ARM concurrency: multicopy-atomic axiomatic and
     cations,” in 2018 51st Annual IEEE/ACM International Symposium on             operational models for ARMv8,” Proceedings of the ACM on
     Microarchitecture (MICRO). Fukuoka: IEEE, Oct. 2018, pp. 788–801.             Programming Languages, vol. 2, no. POPL, pp. 1–29, Jan. 2018.
     [Online]. Available: https://ieeexplore.ieee.org/document/8574586/            [Online]. Available: https://dl.acm.org/doi/10.1145/3158107
[39] Y. A. Manerkar, D. Lustig, M. Martonosi, and M. Pellauer,                [53] S. Sarkar, P. Sewell, J. Alglave, L. Maranget, and D. Williams,
     “RTLcheck: verifying the memory consistency of RTL designs,” in               “Understanding POWER multiprocessors,” in Proceedings of the 32nd
     Proceedings of the 50th Annual IEEE/ACM International Symposium               ACM SIGPLAN Conference on Programming Language Design and
     on Microarchitecture, ser. MICRO-50 ’17. New York, NY, USA:                   Implementation, ser. PLDI ’11. New York, NY, USA: Association for
     Association for Computing Machinery, Oct. 2017, pp. 463–476.                  Computing Machinery, Jun. 2011, pp. 175–186. [Online]. Available:
     [Online]. Available: https://dl.acm.org/doi/10.1145/3123939.3124536           https://doi.org/10.1145/1993498.1993520
[40] Y. A. Manerkar, D. Lustig, M. Pellauer, and M. Martonosi, “CCICheck:     [54] B. C. Schwedock and N. Beckmann, “Leviathan: A Unified
     using µhb graphs to verify the coherence-consistency interface,” in           System for General-Purpose Near-Data Computing,” in 2024 57th
     Proceedings of the 48th International Symposium on Microarchitecture.         IEEE/ACM International Symposium on Microarchitecture (MICRO),
     Waikiki Hawaii: ACM, Dec. 2015, pp. 26–37. [Online]. Available:               Nov. 2024, pp. 1278–1294, iSSN: 2379-3155. [Online]. Available:
     https://dl.acm.org/doi/10.1145/2830772.2830782                                https://ieeexplore.ieee.org/document/10764520
[41] Y. A. Manerkar, C. Trippel, D. Lustig, M. Pellauer, and                  [55] B. C. Schwedock, P. Yoovidhya, J. Seibert, and N. Beckmann, “täkō:
     M. Martonosi, “Counterexamples and Proof Loophole for                         a polymorphic cache hierarchy for general-purpose optimization of
     the C/C++ to POWER and ARMv7 Trailing-Sync Compiler                           data movement,” in Proceedings of the 49th Annual International
     Symposium on Computer Architecture, ser. ISCA ’22. New York, NY,                   (FMCAD). Austin, TX, USA: IEEE, Oct. 2018, pp. 1–10. [Online].
     USA: Association for Computing Machinery, Jun. 2022, pp. 42–58.                    Available: https://ieeexplore.ieee.org/document/8603015/
     [Online]. Available: https://doi.org/10.1145/3470496.3527379                  [69] R. Zhang, C. Deutschbein, P. Huang, and C. Sturton, “End-to-end
[56] M. Sheeran, S. Singh, and G. Stålmarck, “Checking Safety Properties               automated exploit generation for validating the security of processor
     Using Induction and a SAT-Solver,” in Proceedings of the Third In-                 designs,” in 2018 51st Annual IEEE/ACM International Symposium on
     ternational Conference on Formal Methods in Computer-Aided Design,                 Microarchitecture (MICRO), 2018, pp. 815–827.
     ser. FMCAD ’00. Berlin, Heidelberg: Springer-Verlag, Nov. 2000, pp.           [70] T. N. Zhang, K. Singh, T. Chajed, M. Kapritsos, and B. Parno, “Basilisk:
     108–125.                                                                           using provenance invariants to automate proofs of undecidable proto-
[57] P. Subramanyan, Y. Vizel, S. Ray, and S. Malik, “Template-based synthe-            cols,” in Proceedings of the 19th USENIX Conference on Operating
     sis of instruction-level abstractions for SoC verification,” in Proceedings        Systems Design and Implementation, ser. OSDI ’25. USA: USENIX
     of the 15th Conference on Formal Methods in Computer-Aided Design,                 Association, 2025.
     ser. FMCAD ’15. Austin, Texas: FMCAD Inc, Sep. 2015, pp. 160–167.
[58] C. Tan, A. F. Donaldson, and J. Wickerson, “Formalising CXL
     Cache Coherence,” in Proceedings of the 30th ACM International
     Conference on Architectural Support for Programming Languages and
     Operating Systems, Volume 2. New York, NY, USA: Association for
     Computing Machinery, Mar. 2025, pp. 437–450. [Online]. Available:
     https://doi.org/10.1145/3676641.3715999
[59] A. Tarski, “On the calculus of relations,” Journal of
     Symbolic Logic, vol. 6, no. 3, pp. 73–89, Sep. 1941.
     [Online]. Available: https://www.cambridge.org/core/product/identifier/
     S0022481200106528/type/journal article
[60] C. Trippel, Y. A. Manerkar, D. Lustig, M. Pellauer, and M. Martonosi,
     “TriCheck: Memory Model Verification at the Trisection of Software,
     Hardware, and ISA,” in Proceedings of the Twenty-Second International
     Conference on Architectural Support for Programming Languages and
     Operating Systems. Xi’an China: ACM, Apr. 2017, pp. 119–133.
     [Online]. Available: https://dl.acm.org/doi/10.1145/3037697.3037719
[61] M. van der Hagen and B. Lucia, “Client-optimized algorithms and
     acceleration for encrypted compute offloading,” in Proceedings of
     the 27th ACM International Conference on Architectural Support for
     Programming Languages and Operating Systems, ser. ASPLOS ’22.
     New York, NY, USA: Association for Computing Machinery, Feb.
     2022, pp. 683–696. [Online]. Available: https://dl.acm.org/doi/10.1145/
     3503222.3507737
[62] M. Vijayaraghavan, A. Chlipala, Arvind, and N. Dave, “Modular deduc-
     tive verification of multiprocessor hardware designs,” in Computer Aided
     Verification, D. Kroening and C. S. Păsăreanu, Eds. Cham: Springer
     International Publishing, 2015, pp. 109–127.
[63] Z. Wang, G. Mohr, K. von Gleissenthall, J. Reineke, and M. Guarnieri,
     “Specification and Verification of Side-channel Security for Open-
     source Processors via Leakage Contracts,” in Proceedings of the
     2023 ACM SIGSAC Conference on Computer and Communications
     Security, ser. CCS ’23. New York, NY, USA: Association for
     Computing Machinery, Nov. 2023, pp. 2128–2142. [Online]. Available:
     https://dl.acm.org/doi/10.1145/3576915.3623192
[64] J. Wickerson, M. Batty, B. M. Beckmann, and A. F. Donaldson,
     “Remote-scope promotion: clarified, rectified, and verified,” SIGPLAN
     Not., vol. 50, no. 10, pp. 731–747, Oct. 2015. [Online]. Available:
     https://doi.org/10.1145/2858965.2814283
[65] J. Wickerson, M. Batty, T. Sorensen, and G. A. Constantinides,
     “Automatically comparing memory consistency models,” in Proceedings
     of the 44th ACM SIGPLAN Symposium on Principles of Programming
     Languages, ser. POPL ’17. New York, NY, USA: Association for
     Computing Machinery, Jan. 2017, pp. 190–204. [Online]. Available:
     https://doi.org/10.1145/3009837.3009838
[66] J. R. Wilcox, D. Woos, P. Panchekha, Z. Tatlock, X. Wang, M. D.
     Ernst, and T. Anderson, “Verdi: a framework for implementing and
     formally verifying distributed systems,” in Proceedings of the 36th
     ACM SIGPLAN Conference on Programming Language Design and
     Implementation, ser. PLDI ’15. New York, NY, USA: Association for
     Computing Machinery, Jun. 2015, pp. 357–368. [Online]. Available:
     https://dl.acm.org/doi/10.1145/2737924.2737958
[67] Y. Yang, T. Bourgeat, S. Lau, and M. Yan, “Pensieve: Microarchitectural
     Modeling for Security Evaluation,” in Proceedings of the 50th Annual
     International Symposium on Computer Architecture, ser. ISCA ’23.
     New York, NY, USA: Association for Computing Machinery, Jun.
     2023, pp. 1–15. [Online]. Available: https://dl.acm.org/doi/10.1145/
     3579371.3589094
[68] H. Zhang, C. Trippel, Y. A. Manerkar, A. Gupta, M. Martonosi,
     and S. Malik, “ILA-MCM: Integrating Memory Consistency Models
     with Instruction-Level Abstractions for Heterogeneous System-on-Chip
     Verification,” in 2018 Formal Methods in Computer Aided Design
