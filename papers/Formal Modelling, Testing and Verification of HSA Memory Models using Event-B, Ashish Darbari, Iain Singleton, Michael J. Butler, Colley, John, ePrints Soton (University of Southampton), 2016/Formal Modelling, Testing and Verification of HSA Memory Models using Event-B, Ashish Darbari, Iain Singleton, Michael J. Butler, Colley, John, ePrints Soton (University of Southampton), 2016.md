                                         Formal Modelling, Testing and Verification of HSA
                                                 Memory Models using Event-B
                                                                        Ashish Darbari                                          Michael Butler
                                                                       and Iain Singleton                                      and John Colley
                                                                   Imagination Technologies                               University of Southampton
                                                                         Kings Langley                                          Southampton
                                                                  Hertfordshire WD4 8LZ, UK                               Hampshire SO17 1BJ, UK
arXiv:1605.04744v1 [cs.LO] 16 May 2016




                                            Abstract—The Heterogeneous System Architecture (HSA)                  The Heterogeneous System Architecture (HSA) Foundation
                                         Foundation has produced the HSA Platform System Architecture          is a not-for-profit industry standards body which has produced
                                         Specification that goes a long way towards addressing the need        the HSA Platform System Architecture Specification [2] that
                                         for a clear and consistent method for specifying weakly consistent
                                         memory. A weakly-consistent memory model is one of the funda-         goes a long way towards addressing the need for a clear and
                                         mental cornerstones for achieving high performance concurrency        consistent method for specifying weakly consistent memory,
                                         with low power on mobile platforms. HSA is specified using a          but since it is still in natural language there is still a need
                                         natural language which makes it open to multiple ambiguous            for a more formal representation. In this paper, we describe
                                         interpretations and could thereby render bugs in implementations      how the HSA specification and the well-founded terminology
                                         of it in hardware and software. In this paper, we present a
                                         formal model of HSA which can be used in the development and          and concepts it describes, is used to develop a formal model
                                         verification of both concurrent software applications as well as in   in Event-B [3] which can be used in the development and
                                         the development and verification of the HSA-compliant platform        verification of both concurrent software applications as well
                                         itself. We use the Event-B language to build a provably correct       as in the development and verification of the HSA-compliant
                                         hierarchy of models from the most abstract to a detailed refine-      platform itself, the specific configuration of masters, slaves
                                         ment of HSA that is close to implementation level. Our memory
                                         models are general in the sense that they represent arbitrary         and interconnect.
                                         numbers of masters, programs and instruction interleavings and
                                         we reason about such general models using theorem proving. By
                                         using the Rodin tool for Event-B we are able to seamlessly model         We use the Event-B [3] language to build a provably correct
                                         and verify the entire hierarchy of models using proofs to establish   hierarchy of models from the most abstract to a detailed
                                         that each refinement is correct. We also define an automated
                                         validation method that allows us to check baseline compliance of      refinement of HSA that is close to implementation level. Our
                                         the model against a suite of published HSA litmus test cases. Once    memory models are general in the sense that they represent
                                         we have completed the model validation we develop a coverage          arbitrary numbers of masters, programs and instruction in-
                                         driven method to extract a richer set of test cases from the          terleavings and we reason about such general models using
                                         formal Event-B model and a user specified coverage model. These       theorem proving. By using the Rodin tool for Event-B we
                                         tests are then used for extensive regression testing of hardware
                                         and software systems. We believe our methodology of refinement        are able to seamlessly model and verify the entire hierarchy
                                         based formal modelling, baseline compliance testing of the formal     of models using proofs to establish that each refinement is
                                         model and coverage driven test extraction using a single language     correct. We also define an automated validation method that al-
                                         of Event-B language and the Rodin tool is a completely new way        lows us check baseline compliance of the model against a suite
                                         of addressing a profoundly important challenge facing the design      of published HSA litmus test cases. The validation method
                                         and verification of low-power of multi-core systems.
                                                                                                               involves refining the general models to represent litmus tests
                                                                                                               and uses model checking to verify that all possible interleaving
                                                                I. I NTRODUCTION                               of a litmus test achieve the expected outcome. Once we
                                                                                                               have completed the model validation we develop a coverage
                                            Weakly-consistent memory [1] is one of the fundamental             driven method to extract a richer set of test cases from the
                                         cornerstones for achieving high performance concurrency with          formal Event-B model and a user specified coverage model.
                                         low power on mobile platforms. Although the buffering mech-           These tests are then used for extensive regression testing of
                                         anisms that underly weakly consistent memory models are rel-          hardware and software systems. We believe our methodology
                                         atively straightforward to understand, developing a high-level,       of refinement based formal modelling, baseline compliance
                                         natural language specification that represents the behaviours of      testing of the formal model and coverage driven test extraction
                                         all implementations is very difficult. This presents a challenge      using a single language of Event-B language and the Rodin
                                         to both software engineers, who wish to develop efficient, race-      tool is a completely new way of addressing a profoundly
                                         free concurrent programs and for platform engineers who wish          important challenge facing the design and verification of low-
                                         to develop systems that conform to a particular memory model.         power of multi-core systems.
   II. E VENT-B BASED F ORMAL M ODELLING OF HSA
                                                                                                                GM1	  
                                                                                                   Abstract Issue and Observe
   Event-B is a proof-based modelling language and method
that enables the systematic development of specifications using                                              GM2	  
a formal notion of refinement. The Rodin platform [3] is the                                            LOAD and STORE

Eclipse-based IDE that provides automated support for Event-
B modelling, refinement and mathematical proof, model-                                                        GM3	  
                                                                                                        Observed Values
checking and model-based test generation.
   Our approach starts at the abstract level, focusing on issue
                                                                                                          HSAM4	  
and observation of memory instructions. In subsequent refine-
                                                                                               Load/Store Atomics, FENCEs
ments, we introduce set-theoretic relations on the memory
accesses which constrain the order in which they can be issued
                                                                                                             HSAM5	  
or observed. At each refinement level we are able to verify                                                 Registers
properties formally at their appropriate level of abstraction
and detailed instruction sets are introduced in correctness-
                                                                                     HSAM6_1	               HSAM6_2	              HSAM6_m	  
preserving refinement steps. This refinement-based approach                       Litmus Test 1           Litmus Test 2          Litmus Test m
helps to manage complexity of the modelling and verification.
   Using this modelling approach, we build a formal memory
                                                                                    HSAM7_1	              HSAM7_2	               HSAM7_m	  
model that represents an arbitrary set of masters running an                 TestGen/Coverage 1       TestGen/Coverage 2        TestGen/Coverage m

arbitrary set of program threads. We then use further Event-
B refinements to constrain the model to represent a fixed set                        Fig. 1. Model Refinement Hierarchy
of masters, each executing a specific program thread. In this
way, we can represent a published HSA litmus test, together
with a property or set of properties which specify the desired    each representing a single, fixed concurrent program, each
outcome of the test. We then use a combination of automatic       model represents a class of concurrent, synchronised pro-
theorem proving, model checking and simulation to verify and      grams, based on the litmus test, from which we can generate
validate the formalised memory models against the formalised      tests automatically that can be used in the development and
litmus tests. Once we have completed the model validation we      verification of the HSA-compliant platform itself.
develop a coverage driven method to extract a richer set of          In summary, the contributions of this paper are:
test cases from the formal Event-B model and a user specified        • a hierarchy of formalised and verified memory models

coverage model. These tests can then be used for extensive              with varying ordering constraints
regression testing of hardware and software systems.                 • a method for validating models against known litmus tests

   In Figure 1 below we show the Event-B model refinement               through model-checking
hierarchy. The abstract generic models are denoted by GMn,           • a method for automatic generation of tests from a

where n ranges from 1 to 3 whilst the HSA-specific models               constrained model for regression testing of an HSA-
are denoted by HSAMn[ m] where n ranges from 4 upwards                  compliant platform.
and m represents a litmus test at the concrete level. The                    III. U NDERSTANDING HSA O RDERING
abstract models, GM1 to GM3, are generic and can form the
foundation for modelling, for instance, Sequential Consistency       We develop a generalised approach to weakly consistent
(SC) [4], Total Store Order (TSO) [5] or ARM [6] memory           memory modelling, based on HSA terminology, which pro-
models. In GM1 we define the fundamental memory accesses          vides the building blocks with which we can model weak
with the events Issue and Observe, in GM2 we differentiate        memory semantics with a single, consistent modelling frame-
between LOAD and STORE memory accesses and in GM3                 work. We also provide at the concrete level a generalised nota-
we model the observation of the LOAD and STORE values.            tion for representing litmus tests and the invariants associated
In the next refinement, HSAM4, we model the ordering rules        with those tests.
for HSA atomics and FENCEs and in refinement HSAM5 we                We begin with a definition of load and store from the HSA
model the registers generically. We then introduce a series of    reference manual [2]. We focus our modelling around LOAD
refinements, HSAM6[1 .. m] to model a series of m concurrent      and STORE operations that may be issued and observed by
programs, the litmus tests, each running on a fixed set of        different units of execution.
masters and use the ProB model checker [7] to validate the           • For primitives of type store, visibility to unit of execution
model. Each of these models is then further refined, HSAM7[1           A of a store operation X is when the data of store X is
.. m] to introduce the functional coverage metric for coverage         available to loads from unit of execution A.
measurement and test generation.                                     • For primitives of type load, visibility is when a load gets

   Once we have completed the model validation and have a set          the data that the unit of execution will put in the register.
of litmus tests which cover the model, we relax the constraints      We shall use the HSA definition as the basis for formalising
on the litmus test models HSAM7[1 .. m] so that instead of        the specification of loads and stores.
   P1	                                                  P2	                                                      P3	                                                        labelled arrow in Figure 5. P2 observes the STORE p1i2
   p1i1:	  	  	  	  S	  	  1,	  	  	  a1	      p2i1:	  	  	  	  L	  	  	  R1,	  	  	  a2	     p3i1:	  	  	  L	  	  	  R1,	  	  	  a1	           before it observes the LOAD p2i1.
   p1i2:	  	  	  	  S	  	  1,	  	  	  a2	      p2i2:	  	  	  	  L	  	  	  R2,	  	  	  a1	     p3i2:	  	  	  L	  	  	  R2,	  	  	  a2	  
                                                                                                                                                                            P1	                                                  P2	                                                      P3	  
                                                           Fig. 2. Litmus test                                                                                              p1i1:	  	  	  	  S	  	  1,	  	  	  a1	     p2i1:	  	  	  	  L	  	  	  R1,	  	  	  a2	      p3i1:	  	  	  L	  	  	  R1,	  	  	  a1	  
                                                                                                                                                                            p1i2:	  	  	  	  S	  	  1,	  	  	  a2	     p2
                                                                                                                                                                                                                                  p2i2:	  	  	  	  L	  	  	  R2,	  	  	  a1	     p3i2:	  	  	  L	  	  	  R2,	  	  	  a2	  
A. Observation Ordering
                                                                                                                                                                            Fig. 5. Ordering between STOREs and LOADs on different masters
   Without considering synchronisation, based on the HSA
definition above, we define observation ordering, using the                                                                                                                 With these three orderings in place, the following outcome
litmus test of Figure 2 to illustrate the definitions. We assume                                                                                                         is not possible:-
that the values at addresses a1 and a2 are initially set to 0                                                                                                               (p2:R1 = 1 and p2:R2 = 0 and p3:R1 = 1 and p3:R2 = 0)
   • A STORE is observed by any master when a subsequent                                                                                                                    For this outcome to occur would mean that
      LOAD issued by that master would result in the LOAD                                                                                                                   • p2i1 and p2i2 are observed in program order
      returning the value associated with the STORE                                                                                                                         • P2 must observe the LOAD p2i2 before P3 observes the
      – The STOREs p1i1 and p1i2 are observed by masters                                                                                                                      LOAD p3i1
         P1, P2, P3 in some order and these STORE observa-                                                                                                                  • P3 must observe the LOAD p3i2 before P2 observes the
         tions with respect to the LOAD observations determine                                                                                                                LOAD p2i1
         the value which the LOADs observe.                                                                                                                                 • This ordering is invalid (cyclic), therefore the assumed

   • A LOAD is observed by the master issuing the LOAD
                                                                                                                                                                              outcome is not possible, as shown in Figure 6.
      when the LOAD returns the value associated with the last
                                                                                                                                                                            P1	                                                  P2	                                                      P3	  
      observed STORE to the LOAD’s address
                                                                                                                                                                            p1i1:	  	  	  	  S	  	  1,	  	  	  a1	      p2i1:	  	  	  	  L	  	  	  R1,	  	  	  a2	     p3i1:	  	  	  L	  	  	  R1,	  	  	  a1	  
      – The LOADs p2i1 and p2i2 are observed by P2 in some                                                                                                                  p1i2:	  	  	  	  S	  	  1,	  	  	  a2	  
         order; similary for the P3 LOADS.                                                                                                                                                                                        p2i2:	  	  	  	  L	  	  	  R2,	  	  	  a1	     p3i2:	  	  	  L	  	  	  R2,	  	  	  a2	  
   Note that this definition of observation ordering does not
refer to values in registers. We use, instead, the more abstract                                                                                                                                                                 Fig. 6. Invalid ordering
concept of a LOAD returning a value. We also use the term
                                                                                                                                                                            We now describe these three synchronisation orderings,
observe [8] rather than the HSA visibility.
                                                                                                                                                                         using the definitions of Program Order (po), Coherent Order
   For Synchronisation, the ordering of STORE and LOAD
                                                                                                                                                                         (co) and Happens Before Order (hb), as defined in the HSA
observations is constrained
                                                                                                                                                                         specification. For po, there is a total sequential order on
  1) An ordering is established between LOAD and STORE                                                                                                                   operations within a single unit of execution, for co, there
      observations when those LOADs and STOREs are issued                                                                                                                is a total apparent order on all synchronisation operations
      by a single master (e.g., program order). In Figure 3, the                                                                                                         consistent with po and hb must be consistent with each co
      arrow indicates the ordering of the LOADs on P2 and P3.                                                                                                            and with all SC orders.
                                                                                                                                                                            We illustrate these orderings using the same litmus test.
    P1	                                                 P2	                                                      P3	  
    p1i1:	  	  	  	  S	  	  1,	  	  	  a1	     p2i1:	  	  	  	  L	  	  	  R1,	  	  	  a2	     p3i1:	  	  	  L	  	  	  R1,	  	  	  a1	  
                                                                                                                                                                         B. LOADs and STOREs Observed in Program Order (po)
    p1i2:	  	  	  	  S	  	  1,	  	  	  a2	                                                                                                                       Memory accesses from the same master are observed in
                                                         p2i2:	  	  	  	  L	  	  	  R2,	  	  	  a1	     p3i2:	  	  	  L	  	  	  R2,	  	  	  a2	     the order they are issued by all masters.

                Fig. 3. Ordering between LOADs on the the same master                                                                                                    Figure 3 illustrates po on masters P2 and P3.
 2) An ordering is established between LOAD observations                                                                                                                 C. Coherent Observation of LOADs/STOREs per Master (co)
    on different masters to the same address as shown in                                                                                                                    If a master observes a STORE followed by a LOAD for the
    Figure 4.                                                                                                                                                            same memory address, then the value it reads in the LOAD
                                                                                                                                                                         is the value defined in the STORE.
    P1	                                                 P2	                                                      P3	  
    p1i1:	  	  	  	  S	  	  1,	  	  	  a1	     p2i1:	  	  	  	  L	  	  	  R1,	  	  	  a2	     p3i1:	  	  	  L	  	  	  R1,	  	  	  a1	     Figure 4 illustrates co between masters P2 and P3.
    p1i2:	  	  	  	  S	  	  1,	  	  	  a2	  
                                                                                                                                                                         D. Happens Before ordering of Load observations (hb)
                                                         p2i2:	  	  	  	  L	  	  	  R2,	  	  	  a1	     p3i2:	  	  	  L	  	  	  R2,	  	  	  a2	  
                                                                                                                                                                            Finally, we introduce the Happens Before ordering. This
                     Fig. 4. Ordering between LOADs on different masters                                                                                                 is an ordering between loads defined by a combination of
                                                                                                                                                                         coherent orderings on loads and stores to the same address,
 3) An ordering is established between a STORE observation                                                                                                               i.e., if a load L1 from an address A is observed before a store
    by a given master and an observation of a LOAD by a                                                                                                                  S1 to A and load L2 is observed after S1 by some master, then
    different master for the same address as shown by the                                                                                                                L1 is observed before L2 by all masters. (See 7.)
    P1	                                                      P2	                                                       P3	                                                   observed some time after they are issued. Key to defining weak
    p1i1:	  	  	  	  S	  	  1,	  	  	  a1	         p2i1:	  	  	  	  L	  	  	  R1,	  	  	  a2	       p3i1:	  	  	  L	  	  	  R1,	  	  	  a1	      memory models is the relative ordering, locally and globally,
    p1i2:	  	  	  	  S	  	  1,	  	  	  a2	         p2
                                                                                               p3                                                                               of transaction issues and observations. For this reason, we start
                                                             p2i2:	  	  	  	  L	  	  	  R2,	  	  	  a1	       p3i2:	  	  	  L	  	  	  R2,	  	  	  a2	      our modelling with the key events in weak memory systems,
                                                                                                                                                                                Issue transaction and Observe transaction.
                                                         Fig. 7. Happens Before (hb)
                                                                                                                                                                                   We therefore define an abstract Event-B machine, GM1,
                                                                                                                                                                                with two events, Issue and Observe, which operate on memory
E. Synchronisation Mechanisms for Weakly Consistent Mem-                                                                                                                        accesses.
ory
                                                                                                                                                                                  inv1 : issued ⊆ M EM ACCESS
   Using these notions of observation ordering, po, co, and hb,                                                                                                                   inv2 : observed ⊆ issued
we can now define the mechanisms by which synchronisation                                                                                                                       Event Issue =
                                                                                                                                                                                            b
can be achieved. First, we look at the case of No Synchroni-                                                                                                                        any
sation for weakly consistent memory
   1) No Synchronisation: If no fences or specific synchro-                                                                                                                             ma
                                                                                                                                                                                     where
nising instructions are used, then the only ordering is co, as
shown in Figure 2. No synchronisation means that stores are                                                                                                                                 grd1 : ma ∈ M EM ACCESS
observed by different masters in different order.                                                                                                                                           grd2 : ma ∈
                                                                                                                                                                                                      / issued
   2) Synchronising Memory Accesses (Single Memory Loca-                                                                                                                             then
tion): HSA supports atomic synchronizing operations with ac-                                                                                                                            act1 : issued := issued ∪ {ma}
quire and release semantics and are, by definition, Sequentially                                                                                                                    end
Consistent. The operations apply to a single memory location.                                                                                                                   Event Observe =
                                                                                                                                                                                              b
These synchronising LOADs and STOREs, represented as                                                                                                                                any
SL and SS in Figure 8, result in po, co and hb observation
                                                                                                                                                                                        ma
orderings. SL and SS instructions impose po and hb ordering.                                                                                                                         where

   P1	                                                       P2	                                                       P3	  
                                                                                                                                                                                            grd1 : ma ∈ issued
                                                                                                                                                                                     then
   p1i1:	  	  	  	  SS	  	  1,	  	  	  a1	          p2i1:	  	  	  	  SL	  	  	  R1,	  	  	  a2	     p3i1:	  	  	  SL	  	  	  R1,	  	  	  a1	  
   p1i2:	  	  	  	  SS	  	  1,	  	  	  a2	          p2i2:	  	  	  	  SL	  	  	  R2,	  	  	  a1	     p3i2:	  	  	  SL	  	  	  R2,	  	  	  a2	                 act1 : observed := observed ∪ {ma}
                                                                                                                                                                                      end
                                          Fig. 8. Synchronising Memory Accesses                                                                                                    The variable issued, invariant inv1, initialised to the empty
                                                                                                                                                                                set, records the issuing of each memory access by the event
   3) Fences (Multiple Memory Locations in the same Scope):                                                                                                                     Issue. The parameter ma of the event Issue represents a
Instead of using synchronising memory accesses, we can                                                                                                                          memory access, the first guard, grd1, ensures that the memory
introduce a FENCE instruction between the LOADs on P3                                                                                                                           access cannot be re-issued if it has already been issued and
and P4 as shown in Figure 9. The introduction of the FENCE                                                                                                                      ma is added to the issued set by the action act1.
also results in po, co and hb observation orderings. Whereas                                                                                                                       The variable observed, invariant inv2 is defined as a subset
the LOAD and STORE atomics only apply to a single memory                                                                                                                        of the memory accesses that have been issued. If the set issued
location, the FENCE applies to all memory locations within                                                                                                                      is not empty, the event Observe chooses an issued memory
the same defined scope, as described in the HSA specification.                                                                                                                  access non-deterministically from the set and the action act1
                                                                                                                                                                                adds it to the set observed. At this early stage there is no notion
   P1	                                                       P2	                                                       P3	  
                                                                                                                                                                                of a program. Memory accesses are issued in some arbitrary
   p1i1:	  	  	  	  S	  	  1,	  	  	  a1	           p2i1:	  	  	  	  L	  	  	  R1,	  	  	  a2	      p3i1:	  	  	  L	  	  	  R1,	  	  	  a1	  
                                                                                                                                                                                order, and once issued they can be observed repeatedly in some
   p1i2:	  	  	  	  S	  	  1,	  	  	  a2	           P2i2:	  	  	  	  FENCE	                               P3i2:	  	  	  FENCE	  
                                                                                                                                                                                arbitrary order.
                                                              p2i3:	  	  	  	  L	  	  	  R2,	  	  	  a1	      p3i3:	  	  	  L	  	  	  R2,	  	  	  a2	  
                                                                                                                                                                                   We then refine the abstract model to differentiate between
                                                         Fig. 9. Fence Synchronisation                                                                                          LOAD and STORE accesses,

                                                                                                                                                                                   axm2 : partition(M EM ACCESS, ST ORE, LOAD)
       IV. M ODELLING W EAK M EMORY WITH E VENT-B                                                                                                                                 and refine the abstract events Issue and Observe.
   We begin with an abstract, highly nondeterministic model                                                                                                                        • New events IssueLoad and IssueStore refine Issue
of memory accesses. The abstract Event-B context defines a                                                                                                                         • New events ObserveLoad and ObserveStore refine Ob-
set of transactions, TRN and a subset of the transactions which                                                                                                                      serve
are memory accesses, MEMACCESS.
                                                                                                                                                                                  In the next refinement, we introduce an abstraction of
  axm1 : M EM ACCESS ⊆ T RN                                                                                                                                                     the memory architecture, which makes reasoning about weak
  We assume a set of masters that issue transactions on a                                                                                                                       memory consistency tractable[8]. Each master keeps track in-
shared memory space and the effect of those transactions is                                                                                                                     dividually of its last observed STORE value for each memory
location. When a LOAD is observed, the last observed value                 necessary to implement fence synchronisation. We introduce
for that master is written to the master’s target register.                the variable ahead to represent the accesses that are ahead
   An observation ordering is then established between LOADs               of the fence and the variable after to represent the set of
and STOREs, depending on address, control and data depen-                  LOADs that are observed after a given STORE. Our refine-
dencies and the positioning of fences.                                     ment distinguishes multiple cases of LOAD observation, each
   The abstract architecture is shown in Figure 10, where each             of which is represented by an event that refines our abstract
Memory i represents the last observed STORE value of each                  ObserveLoad event. First, we specify the LOAD observations
memory location for each individual Master i.                              in the presence of a FENCE. There are two cases to address,
                                                                           the load happening before a store and happening after a store.
                                                                              ObserveLoadHappensBeforeWithFence: If the master that
             MASTER 1         MASTER 2                       MASTER n
                                                                           issued the LOAD has issued a FENCE and if the LOAD is not
         store             store                          store
                                                                           ahead of the FENCE in program order, then all other memory
                    load             load                           load
                                                                           accesses ahead of the FENCE in program order must have
             Memory 1         Memory 2                       Memory n
                                                                           been observed (guard grd7 below). This LOAD is observed
                                                                           before a corresponding STORE to the same location (guards
                             Abstract Memory Sub-system
                                                                           grd9, grd10) and no other LOAD has observed that STORE
                                                                           and there is therefore no LOAD after the STORE (guard
                                                                           grd11).
                  Fig. 10. Abstract Memory Architecture                       • LOADs are observed in Program Order(po)
                                                                              • LOAD is observed before a corresponding STORE
   This architecture is represented in Event-B with the variable
                                                                              • No other LOAD has been observed after the STORE
lov.
                                                                              • po + co + hb

   inv1 : lov ∈ M AST ER → (ADDR → V ALU E)                                The event is specified as follows:
   which maintains the last observed value.                                Event ObserveLoadHappensBeforeWithFence =      b
   We also introduce the variable observers, which associates              extends ObserveLoad
each memory access with the masters which have observed                         any
that access.
                                                                                  l, m, f, s
  inv2 : observers ∈ M EM ACCESS →
                                 7 P(M AST ER)                                 where
   For each LOAD or STORE that is issued, observers(s) is                           grd1 : l ∈ issued
initialised to the empty set.                                                       grd2 : l ∈ LOAD
   The refined event ObserveStore introduces a new guard,                           grd3 : m ∈ / observers(l)
grd3, to ensure that this master, m, has not already observed                       grd4 : m = issuer(l)
this store, s, an action, act2, which updates the last observed                     grd5 : f ∈ issuedf ence
value for m, using the relational override operator, and an                         grd6 : m = issuer(f )
action, act3, which adds m to the observers of s.                                   grd7 : l ∈
                                                                                             / ahead(f ) ⇒
Event ObserveStore =    b                                                         (∀a·a ∈ ahead(f ) ∧ a ∈ dom(observers) ⇒
refines ObserveStore                                                              m ∈ observers(a))
      any                                                                           grd8 : s ∈ ST ORE
        s, m                                                                        grd9 : address(s) = address(l)
     where                                                                          grd10 : m ∈/ observers(s)
                                                                                    grd11 : af ter(s) = ∅
            grd1 : s ∈ issued                                                  then
            grd2 : s ∈ ST ORE
            grd3 : m ∈/ observers(s)                                                act1 : observed := observed ∪ {l}
     then                                                                           act2 : observers(l) := observers(l) ∪ {m}
                                                                                end
            act1 : observed := observed ∪ {s}
                                                                             ObserveLoadAfterStoreWithFence: If the master that issued
            act2 : lov(m) := lov(m) C− {addr(s) 7→ val(s)}
                                                                           the LOAD has issued a FENCE and if the LOAD is not
            act3 : observers(s) := observers(s) ∪ {m}
     end                                                                   ahead of the FENCE in program order, then all other memory
                                                                           accesses ahead of the FENCE in program order must have
   We now have a generic, abstract model which can now be
                                                                           been observed (guard grd7). The master has observed a
refined to implement HSA Atomics and Fences.
                                                                           corresponding STORE to the same location (guard grd11).
A. Modelling HSA Fence Synchronisation                                        • In Program Order
  Using the definitions of po, co and hb from the HSA                         • LOAD is observed after a corresponding STORE
specification, we are able to model the observation orderings                 • po + co
The event is specified as follows:                                             V. VALIDATING THE M EMORY M ODEL
Event ObserveLoadAfterStoreWithFence =
                                     b                             A. A Notation for Representing Litmus Tests
extends ObserveLoad
                                                                      The memory model we have developed represents all the
     any
                                                                   legal interleavings of an arbitrary set of programs running on
        l, m, f, s                                                 an arbitrary set of masters. We now wish to constrain the
     where                                                         model to represent a litmus test - all possible interleavings for
          grd1 : l ∈ issued                                        a fixed set of masters each running a specific, fixed program
          grd2 : l ∈ LOAD                                          thread.
                                                                      To make it easier to verify litmus tests, we introduce a tool-
          grd3 : m ∈ / observers(l)
                                                                   supported notation with which the litmus test and the invariant
          grd4 : m = issuer(l)
          grd5 : f ∈ issuedf ence                                  can be represented and an Event-B context and invariant is
                                                                   generated automatically from this description. An example of
          grd6 : m = issuer(f )
                                                                   a litmus test in our notation as shown in Figure 11.
          grd7 : l ∈
                   / ahead(f ) ⇒
        (∀a·a ∈ ahead(f ) ∧ a ∈ dom(observers) ⇒
                                                                   p1:
        m ∈ observers(a))                                                   st 1, a1
          grd8 : s ∈ issued                                                 st 1, a2
          grd9 : s ∈ ST ORE                                        p2:
                                                                            ld r1, a1
          grd10 : address(s) = address(l)                                   fence
          grd11 : m ∈ observers(s)                                          ld r2, a2
     then                                                          p3:
                                                                            ld r1, a2
          act1 : observed := observed ∪ {l}                                 fence
                                                                            ld r2, a1
          act2 : observers(l) := observers(l) ∪ {m}
          act3 : af ter(s) := af ter(s) ∪ {l}
      end                                                          outcome: not(p2.r1 = 1 and p3.r1 = 1 and p2.r2 = 0 and p3.r2 = 0)
   Similarly, we specify the two cases of LOAD observation
without a FENCE covering loads before and after a store.                       Fig. 11. Litmus Test in Tool-supported Notation
We also specify an IssueFence event. Details of these are
straightforward and are ommited for brevity.                       B. The Litmus Test Context
B. Modelling the HSA Atomics                                         We constrain the memory model by introducing axioms
                                                                   which specify the litmus test instructions, where for instance
   Again, using the definitions of po, co and hb from the HSA
                                                                   I11 is a STORE of the value 1 to the address a1, and the
specification, we are now able to model the HSA atomics.
                                                                   program threads that will run those instructions.
   First, we define the atomic LOAD, SCACQLOAD, with
acquire semantics and the atomic STORE, SCRELSTORE with              axm10 : P 1 = {1 7→ I11, 2 7→ I12}
release semantics, and differentiate them from the ordinary          axm11 : P 2 = {1 7→ I21, 2 7→ I22, 3 7→ I23}
LOADs and STOREs.                                                    axm12 : P 3 = {1 7→ I31, 2 7→ I32, 3 7→ I33}
   As we did to model fences, above, we then refine the events       We then associate each thread with the appropriate master.
of the generic model to establish this differentiation, imposing
the ordering defined in the HSA specification in the follow-         axm19 : P ROGRAM = {M 1 7→ P 1, M 2 7→ P 2, M 3 7→ P 3}
ing, refinedIssue events, IssueAtomicSCACQLoad, IssueLoad,         C. Verifying the Litmus Test Outcome
IssueAtomicSCRELStore, IssueStore and their corresponding             An outcome statement may be associated with the Litmus
Observe events.                                                    Test, which is represented as a boolean expression in terms of
C. Introducing the Register File                                   the values in the registers of the masters. We specify outcome
                                                                   to mean the values in the registers when all litmus test loads
  We have a model which implements fences and atomics,
                                                                   have been observed. An invariant is generated that we verify
which can be refined to introduce the register file as an Event-
                                                                   using the ProB model checker. In the case of this litmus test,
B variable, rf
                                                                   the invariant is
   inv1 : rf ∈ M AST ER →   7 (REG → V ALU E)
   When a LOAD, l, is observed by a master, m, the register          inv1 : {I21, I23, I31, I33} ⊆ observed ⇒
r associated with l, rl, takes the last observed value for          ¬((rf (M 2))(R1) = V 1 ∧ (rf (M 3))(R1) = V 1 ∧
that LOAD location, addr(l). For instance, in the event Ob-         ((rf (M 2))(R2) = V 0 ∧ (rf (M 3))(R2) = V 0))
serveLoadHappensBeforewithFence described above, an extra            If the loads, I21, I23, I31, I33 issued by the masters M2 and
action, act3 is added.                                             M3 have been observed, then the registers associated with the
                                                                   masters cannot contain the prohibited outcome. The values V0
                          − {r(l) 7→ (lov(m))(addr(l))}
  act3 : rf (m) := rf (m) C                                        and V1 represent logic 0 and 1 respectively.
D. Covering the Allowable Register Value Combinations                for each of the 15 reachable combinations. Creating the tests
   The facility to specify and verify the illegal litmus test out-   manually is time consuming. ProB provides a model-checking-
comes formally is valuable, but to ensure thorough verification,     based test generation facility which can be used to generate
it is necessary to go further.                                       these tests automatically.
    • To ensure that all the legal outcomes of the litmus test          First, we specify a predicate to define the target state. For
      are reachable.                                                 instance, if we wish to show that all the registers of both
    • To ensure that the set of litmus tests cover the model         masters can take the value 0 when all the LOADs have been
      functionality.                                                 observed, then we specify.
   We introduce a further refinement of the memory model to
introduce a functional coverage metric for the litmus test.            I21, I23, I31, I33 ⊆ observed => C0 7→ C0 : coverage
   The relation coverage
                                                                     Second, we specify the event or events which we wish
  inv1 : coverage ∈ REGCOV ER ↔ REGCOV ER                            to be covered by the test. In this case, we just specify the
represents the combinations of register values that are reached      CoverRegisterValues event to guide the search.
by the litmus test, where REGCOVER is defined in extended               ProB generates the tests as an HTML file, which can be
context thus:                                                        translated to suit the tool chain. One of the tests that ProB
  axm1 : C0 = {R1 7→ V 0, R2 7→ V 0}                                 generates is shown in Figure 12 below. The test describes
  axm2 : C1 = {R1 7→ V 0, R2 7→ V 1}                                 a sequence of six Issue instructions which results in the
  axm3 : C2 = {R1 7→ V 1, R2 7→ V 0}                                 expected register value combination to be recorded by the
  axm4 : C3 = {R1 7→ V 1, R2 7→ V 1}                                 event CoverRegisterValues.
  axm5 : REGCOV ER = {C0, C1, C2, C3}
Each constant Cn represents a register combination value for a       Test_case_id = 1
master and REGCOVER is the set of all register combinations          IssueLoad(I21, P2);
for a master. The coverage relation is initialised to the empty      IssueLoad(I31, P3);
set. The refinement then introduces a new event CoverRegis-          IssueFence(I22, P2);
terValues                                                            IssueLoad(I23, P2);
Event CoverRegisterValues =   b                                      IssueFence(I32, P3);
     any                                                             IssueLoad(I33, P3);
                                                                     CoverRegisterValues(rm2(R1->0, R2->0),
        rm2, rm3                                                                         rm3(R1->0, R2->0) );
     where
            grd1 : rm2 ∈ REGCOV ER                                                         Fig. 12. Generated Test
            grd2 : rm3 ∈ REGCOV ER
            grd3 : rf (M 2) = rm2                                    F. Measuring the Coverage of a set of Litmus Tests
            grd4 : rf (M 3) = rm3
            grd5 : rm2 7→ rm3 ∈ / coverage                              Since the litmus tests each target a particular aspect of the
            grd6 : {I21, I23, I31, I33} ⊆ observed                   weak memory model, an individual litmus test will not cover
     then                                                            all of the events of the model. What we do want to know,
                                                                     however, is that all events of the model are covered by the set
           act1 : coverage := coverage ∪ {rm3 7→ rm4}                of litmus tests. In other words, that the litmus tests fully cover
     end
                                                                     the model functionality.
   This event is enabled when all the LOADs have been
                                                                        We return to the tests generated above and now, instead of
observed (guard grd6) and when this combination of the
                                                                     specifying the CoverRegisterValues event, we specify all the
master register values has not already been covered (guard
                                                                     events that we expect to be covered by the test. We want
grd5). The combination is then added to the coverage relation.
                                                                     to verify that these and only these events are covered by
   We can now re-run the model checker exhaustively to show,
                                                                     the litmus test. ProB will now generate several tests for the
not only that illegal register combinations are never reached
                                                                     required outcome which cover the events specified.
but also that all legal combinations are reachable. The ProB
model checker has a coverage option that now allows us to            G. Generating additional Litmus Tests
display the values of the relation coverage that are covered.
   Coverage point 15 represents the initial value of the cover-         Once we have completed the model validation and have a set
age relation. Note that otherwise all 15 possible combinations       of litmus tests which cover the model, we relax the constraints
have been covered and the illegal combination is not covered.        on our formalised litmus tests so that each model represents a
                                                                     class of programs with a non-deterministic mix of instructions
E. Generating a Test for each Coverage Point                         (and the same set of masters, registers and address space as the
  Now that we are sure that each legal combination of                associated litmus). Using the ProB test generator, we are able
registers is reachable, we wish to create a regression test          to generate automatically a wide range of tests, with expected
register values, which can be used for regression testing of the   in understanding and precision of formal modelling. Using
HSA-compliant platform itself.                                     the same Event B model on which we have shown that
                                                                   refinements are provably correct, we can test it for litmus test
          VI. R ELATED W ORK AND C ONCLUSION                       compliance against published HSA litmus tests. The key here
   An overview of memory ordering and barriers in modern           is that testing for compliance is embedded within the Rodin
microprocessors is presented in [9] and[10]. The release           framework where proof based refinement is done; leading to
consistency model is described in [11]. The notion of using        a very tight integration of testing and proofs. By relaxing
thread-local re-ordering and store atomicity, together with        the constraints of HSA litmus tests we are able to explore
the definition of an abstract architecture to support weakly       a much bigger space of tests and by a natural extension of
consistent memory specification is developed in [8] and [12].      the core Event B model of the HSA by a coverage event
The tutorial [13], for ARM and POWER memory models,                we are able to generate a bigger set of regression tests that
builds on the notion of an abstract machine architecture to        satisfy the coverage model. This is again done on the same
define a storage subsystem which has general applicability         core Event B model on which proof based refinements were
for weakly consistent memory specification. [14] introduces        done. The tests generated can be used in the development
the notion of modelling concurrency with partial orders. [15]      and verification of the HSA-compliant platform itself.
presents an axiomatic approach to POWER memory modelling
and [16] presents a class of relaxed memory models which
are parameterised to support different local re-orderings and                               ACKNOWLEDGMENT
store atomicity relaxation. [6] provides a clear description of       The authors would like to thank Jason Meredith, Mark
the ARM memory model and the HSA initiative to harmonise           Landers and James Aldis for several discussions during the
heterogenous computing concepts [2] has resulted in a natural      development of this work. The authors would also like to
language specification of fences and atomics which provides        thank Imagination Technologies for their time and support
considerable clarity for programmers, model and system de-         throughout this work.
velopers.
   In [17], an axiomatic approach is used where the mem-                                        R EFERENCES
ory model is represented as a directed graph, the nodes
                                                                    [1] M. Dubois, C. Scheurich, and F. Briggs, “Memory access buffering in
representing the memory accesses and the arcs the ordering              multiprocessors,” ACM SIGARCH Computer Architecture News, vol. 14,
between those accesses. Our Event-B approach is based on                no. 2, pp. 434–442, 1986.
the computation model of guarded atomic actions. Memory             [2] H. Foundation, “HSA platform system architecture specification,” Stan-
                                                                        dard, January 2015.
access ordering is specified axiomatically as guards on events,     [3] J.-R. Abrial, M. J. Butler, S. Hallerstede, T. S. Hoang, F. Mehta, and
which model the memory accesses themselves, for instance                L. Voisin, “Rodin: an open toolset for modelling and reasoning in Event-
IssueRead, ObserveWrite. If more than one event is enabled,             B,” STTT, vol. 12, no. 6, pp. 447–466, 2010.
                                                                    [4] L. Lamport, “How to make a multiprocessor computer that correctly
then a choice is made non-deterministically, naturally repre-           executes multiprocess programs,” Computers, IEEE Transactions on,
senting the non-determinism of the memory model. The Event-             vol. 100, no. 9, pp. 690–691, 1979.
B model is operational in the sense that it is based on the         [5] P. Sewell, S. Sarkar, S. Owens, F. Z. Nardelli, and M. O. Myreen, “x86-
                                                                        tso: a rigorous and usable programmer’s model for x86 multiprocessors,”
highly abstract memory architecture described in [8]. We begin          Communications of the ACM, vol. 53, no. 7, pp. 89–97, 2010.
with a generic model to represent the ordering at a high level      [6] N. Chong and S. Ishtiaq, “Reasoning about the arm weakly consistent
of abstraction and then use formal refinement to introduce, in          memory model,” in Proceedings of the 2008 ACM SIGPLAN workshop
                                                                        on Memory systems performance and correctness: held in conjunction
steps, as much detail as is necessary to represent a concrete,          with the Thirteenth International Conference on Architectural Support
concurrent program, where the state of the registers and the            for Programming Languages and Operating Systems (ASPLOS’08).
values observed by each of the masters are updated by the               ACM, 2008, pp. 16–19.
                                                                    [7] M. Leuschel and M. Butler, “ProB: an automated analysis toolset for
event actions. The concrete model can therefore be mapped               the B method,” STTT, vol. 10, no. 2, pp. 185–203, 2008.
directly to a Transaction-Level Model (TLM) for efficient           [8] X. Shen, Arvind, X. Shen, L. Rudolph, and L. Rudolph, “Commit-
system simulation. [17] also presents a tool for simulation             reconcile fences (crf): A new memory model for architects and compiler
                                                                        writers,” in In Proceedings of the 26th International Symposium on
and testing of memory models. Using ProB we can simulate                Computer Architecture, 1999, pp. 150–161.
and test our Event-B models at each level of abstraction as         [9] P. E. McKenney, “Memory ordering in modern microprocessors, part i,”
well as generate coverage-driven tests for regression testing           Linux Journal, vol. 2005, no. 136, p. 2, 2005.
of hardware and software systems.                                  [10] ——, “Memory ordering in modern microprocessors, part ii,” Linux
                                                                        Journal, vol. 2005, no. 137, p. 5, 2005.
   We believe our methodology of refinement based formal           [11] K. Gharachorloo, D. Lenoski, J. Laudon, P. Gibbons, A. Gupta, and
modelling, baseline compliance testing of the formal model              J. Hennessy, Memory consistency and event ordering in scalable shared-
and coverage driven test extraction using a single language of          memory multiprocessors. ACM, 1990, vol. 18, no. 2SI.
                                                                   [12] A. Arvind and J.-W. Maessen, “Memory model= instruction reorder-
Event B language and the Rodin tool is a completely new way             ing+ store atomicity,” in ACM SIGARCH Computer Architecture News,
of addressing a profoundly important challenge facing the               vol. 34. IEEE Computer Society, 2006, pp. 29–40.
design and verification of low-power of multi-core systems.        [13] L. Maranget, S. Sarkar, and P. Sewell, “A tutorial introduction to the
                                                                        arm and power relaxed memory models,” 2012.
It provides a hierarchy of models where the complexity             [14] V. Pratt, “Modeling concurrency with partial orders,” International
of modelling is managed by refinement leading to clarity                Journal of Parallel Programming, vol. 15, no. 1, pp. 33–71, 1986.
[15] S. Mador-Haim, L. Maranget, S. Sarkar, K. Memarian, J. Alglave,
     S. Owens, R. Alur, M. M. Martin, P. Sewell, and D. Williams, “An
     axiomatic memory model for power multiprocessors,” in Computer
     Aided Verification. Springer, 2012, pp. 495–512.
[16] J. Alglave, L. Maranget, S. Sarkar, and P. Sewell, “Fences in weak
     memory models,” in Computer Aided Verification. Springer, 2010, pp.
     258–272.
[17] J. Alglave, L. Maranget, and M. Tautschnig, “Herding cats: Modelling,
     simulation, testing, and data mining for weak memory,” ACM Trans-
     actions on Programming Languages and Systems (TOPLAS), vol. 36,
     no. 2, p. 7, 2014.
