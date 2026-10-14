                                            UCLID5: Multi-Modal Formal Modeling, Verification,
                                                            and Synthesis

                                            Elizabeth Polgreen1,2[0000−0001−9032−7661] , Kevin Cheang1[0000−0002−5717−0575] ,
                                                 Pranav Gaddamadugu1 , Adwait Godbole1[0000−0001−7704−304X] , Kevin
                                                Laeufer1[0000−0003−0942−7070] , Shaokai Lin1[0000−0001−6885−5572] , Yatin
                                                     A. Manerkar3 , Federico Mora1[0000−0002−0725−9213] , and Sanjit
arXiv:2208.03699v1 [cs.LO] 7 Aug 2022




                                                                     A. Seshia1[0000−0001−6190−8707]
                                             CAV                                 1
                                                                                                                                CAV
                                          Artifact                                UC Berkeley                                  Artifact
                                         Evaluation                        2
                                                                             University of Edinburgh                          Evaluation
                                                                           3
                                                                             University of Michigan
                                         Available                                                                            Reusable



                                                Abstract. UCLID5 is a tool for the multi-modal formal modeling, verification,
                                                and synthesis of systems. It enables one to tackle verification problems for het-
                                                erogeneous systems such as combinations of hardware and software, or those
                                                that have multiple, varied specifications, or systems that require hybrid modes of
                                                modeling. A novel aspect of UCLID5 is an emphasis on the use of syntax-guided
                                                and inductive synthesis to automate steps in modeling and verification. This tool
                                                paper presents new developments in the UCLID5 tool including new language
                                                features, integration with new techniques for syntax-guided synthesis and satis-
                                                fiability solving, support for hyperproperties and combinations of axiomatic and
                                                operational modeling, demonstrations on new problem classes, and a robust im-
                                                plementation.


                                        1     Overview

                                        Tools for formal modeling and verification are typically specialized for particular do-
                                        mains and for particular methods. For instance, software verification tools like Boo-
                                        gie [5] focuses on modeling sequential software and Floyd-Hoare style reasoning, while
                                        hardware verifiers like ABC [6] are specialized for sequential circuits and SAT-based
                                        equivalence and model checking. Specialization makes sense when the problems fit
                                        well within a homogeneous problem domain with specific verification needs. However,
                                        there is an emerging class of problems, such as in security and cyber-physical systems
                                        (CPS), where the systems under verification are heterogeneous, or the types of specifi-
                                        cations to be verified are varied, or there is not a single type of model that is effective
                                        for verification. An example of such a problem is the verification of trusted computing
                                        platforms [42] that involve hardware and software components working in tandem, and
                                        where the properties to be checked include invariants, refinement checks, and hyper-
                                        properties. There is a need for automated formal methods and tools to handle this class
                                        of problems.
                                            UCLID5 is a system for multi-modal formal modeling, verification, and synthe-
                                        sis that addresses the above need. UCLID5 is multi-modal in three important ways.
2       Polgreen et al

First, it permits different modes of modeling, using axiomatic and operational seman-
tics, or as combinations of concurrent transition systems and procedural code. This
enables modeling systems with multiple characteristics. Second, it offers a varied suite
of specification modes, including first-order formulas in a combination of logical theo-
ries, temporal logic, inline assertions, pre- and post-conditions, system invariants, and
hyperproperties. Third, it supports the first two capabilities with a varied suite of verifi-
cation techniques, including Floyd-Hoare style proofs, k-induction and bounded model
checking (BMC), verifying hyperproperties, or using syntax-guided and inductive syn-
thesis to provide more automation in tedious steps of verification, or to automate the
modeling process (as proposed in [39]).
    The UCLID5 framework was first proposed in 2018 [40], itself a major evolution of
the much older UCLID system [7], one of the first satisfiability modulo theories (SMT)
based modeling and verification tools. Since that publication [40], which laid out the
vision for the tool and described a preliminary implementation, the utility of the tool
has been demonstrated on several problem classes (e.g., [9,30,8]), such as for verify-
ing security across the hardware-software interface. The syntax has been extended and
state-of-the-art methods for syntax-guided synthesis (SyGuS) have also been integrated
into the tool [33], including new capabilities for satisfiability and synthesis modulo or-
acles [37]. This tool paper presents an overview of the latest version of UCLID5, high-
lighting novel multi-modal aspects of the tool, as well as the new features supported
since 2018 [40]. The paper is structured as follows: in Section 2 we give an overview
of the UCLID5 tool; in Section 3 we detail different multi-modal aspects of the tool,
as well as high-lighting new features; and in Section 4 we present a case study using
UCLID5 to verify a Trusted Abstract Platform. We cover related work in Section 5. The
new features we highlight are:

 1. Fully integrated support for synthesis across all verification modes
 2. Support for modeling with external oracles, via satisfiability and synthesis modulo
    oracles [37]
 3. New language features to support combining axiomatic and operational modeling
 4. Direct support for hyperproperties
 5. Front-end translations from Chisel/FIRRTL to UCLID5, and from RISC-V binaries
    to UCLID5, referenced in Section 6.
 6. New case studies: covering models for distributed CPS in Lingua Franca [26], and
    encodings of µhb specifications and verification of a Trusted Abstract Platform
    described in Sections 3.2 and 4 and in the corresponding artifact [36].


2   Overview of UCLID5

In verification mode, UCLID5 reduces the question of whether a model satisfies a given
specification to a set of constraints that can be solved by an off-the-shelf SMT solver.
In synthesis mode, UCLID5 reduces the problem of finding an interpretation for an
uninterpreted function such that the specification is satisfied into a SyGuS problem that
can be solved by an off-the-shelf SyGuS solver. In order to do so, UCLID5 performs
the following main tasks, as shown in Figure 1:
                                                                               UCLID5           3

Front end: UCLID5 takes models written in the UCLID5 language as input. The
command-line front-end allows user configuration, including specifying the external
SMT-solver/SyGuS-solver to be used, as well as enabling certain utilities such as au-
tomatically converting uninterpreted functions to arrays. The parser builds an abstract
syntax tree from the model.

AST passes: UCLID5 performs a number of transformations and checks on the abstract
syntax tree, including type-checking and inlining of procedures. This intermediate rep-
resentation supports limited control flow such as if-statements and switch-cases, but
loops are not permitted in procedural code and are removed via unrolling (bounded for-
loops) or replacement with user-provided invariants (while loops). However, unbounded
control flow can be handled by representation as transition systems (where each module
consists of a transition system with an initial and a next block, each represented as a
separate AST).

Symbolic Simulator: The symbolic simulator performs a simulation of the transition
system in the model, according to the verification command provided, and produces
a set of assertions. For instance, if bounded model checking is used, UCLID5 will
symbolically execute the main module a bounded number of times. UCLID5 encodes
the violation of each independent verification condition as a separate assertion tree.

Synth-Lib interface: UCLID5 supports both synthesis and verification. The Synth-Lib
interface constructs either a verification or a synthesis problem from the assertions gen-
erated by the symbolic simulator. The verification problems are passed to the SMT-LIB
interface, which converts each assertion in UCLID5’s intermediate representation to an
assertion in SMT-LIB. Similarly, the synthesis problems are passed to the SyGuS-IF
interface, which converts each assertion to an assertion in SyGuS-IF. The verification
and synthesis problems are then passed to the appropriate provided external solver and
the result is reported back to the user.


                                                        assert
                          AST
   Front-end   AST                  AST   Symbolic       tree     Synth-Lib          Result +
                     transformation
     parser                               Simulator                interface        c-example
                         passes
                                                         synth                 synth
                                                          IR                    IR
                                                      SMT-LIB                  SyGuS-IF
                                                      interface                 interface

                                                model            query model           query

                                                   SMT solver             SyGuS solver

                            Fig. 1: Architecture of UCLID5
4       Polgreen et al

Basic UCLID5 Models A simple UCLID5 model that computes the Fibonacci se-
quence is shown in Figure 2. UCLID5 models are contained within modules which
comprise of 3 parts: a system model represented using combinations of sequential, con-
current, operational and axiomatic modeling, as described in Sections 3.2; a system
specification described in Section 3.1; and a proof script that specifies the verification
tasks UCLID5 should perform to prove that the system satisfies its specification, using
a variety of supported verification and synthesis techniques described in Section 3.1.


3   Multi-modal Language Features

3.1 Multi-modal verification and synthesis
Specification UCLID5 supports a variety of different types of specifications. The stan-
dard properties supported include inline assertions and assumptions in sequential code,
pre-conditions and post-conditions for procedures, and global axioms and invariants
(both as propositional predicates, and temporal invariants in Linear Temporal Logic
(LTL)).
     The latest version of UCLID5 further provides direct support for hyperinvariants
and hyperaxioms (for k-safety). This new support for direct hyperproperties comprises
of two new language constructs: hyperaxiom and hyperinvariant . The former places
an assumption on the behavior of the module, if n instances of the module were instan-
tiated, and the latter is an invariant over n instances of the module, which is verified
via the usual verification methods. A variable x from the nth instance of the module
is reasoned about in the predicate using x.n, and the number of modules instantiated
is determined by the maximum n in both the invariant and the axiom. For example,
hyperinvariant[2] det xy: y.1 == y.2 asserts that a 2-safety hyperprop-
erty holds.

Verification To verify these specifications, we implement multiple classic techniques.
As a result, once a model is written in UCLID5, the user can deploy a combination of
verification techniques, depending on the properties targeted. UCLID5 supports a range
of verification techniques including: Bounded Model Checking (for LTL, hyperinvari-
ants and assertion-based properties); induction and k-induction for assertion-based in-
variants and hyperinvariants; and verification of pre-and post-conditions on procedures
and hyperinvariants.
    As an exemplar of the utility of multi-modal verification, consider the hyper-property
based models verified by Sahai et al. [38]. These models use both procedure verification
and induction to verify k-trace properties.

Synthesis The latest version of UCLID5 integrates program synthesis fully across all
the verification modes previously described. Specifically, users are able to declare and
use synthesis functions anywhere in their models, and UCLID5 will seek to automat-
ically synthesize function bodies for these functions such that the user-selected veri-
fication task will pass. In this section, we give an illustrative example of synthesis in
UCLID5, we provide the necessary background on program synthesis, and then we
formulate the existing verification techniques inside of UCLID5 for synthesis.
                                                                              UCLID5          5


 1   module main {
 2
 3       // Part 1: System Description.
 4       var a, b : integer;
 5       init {
 6         a, b = 0, 1;
 7       }
 8       next {
 9         a’, b’ = b, a + b;
10       }
11
12       // Part 2: System Specification.
13       invariant a_le_b: a <= b;
14
15       // Part 3: (NEW) Synthesis Integration
16       synthesis function
17         h(x : integer, y : integer): boolean;
18       invariant hole: h(a, b);
19
20       // Part 4: Proof Script.
21       control {
22         induction;
23         check;
24         print_results;
25       }
26   }



     Fig. 2: UCLID5 Fibonacci model. Part 3 shows the new synthesis syntax, and how to
     find an auxiliary invariant.




         Consider the UCLID5 model in Fig. 2. The user wants to prove by induction that the
     invariant a le b at line 13 always holds. Unfortunately, the proof fails because the in-
     variant is not inductive. Without synthesis, the user would need to manually strengthen
     the invariant until it became inductive. However, the user can ask UCLID5 to automat-
     ically do this for them. Fig. 2 demonstrates this on lines 16, 17 and 18. Specifically, the
     user specifies a function to synthesize called h at lines 16 and 17, and then uses h at
     line 18 to strengthen the existing set of invariants. Given this input, UCLID5, using e.g.
     CVC 5 [4] as a syntax-guided synthesis engine, will automatically generate the function
     h(x, y) = x >= 0, which completes the inductive proof.

         In this example, the function to synthesize represents an inductive invariant. How-
     ever, functions to synthesize are treated exactly like any interpreted function in UCLID5:
     the user could have called h anywhere in the code. Furthermore, this example uses in-
     duction and a global invariant, however, the user could also have used a linear temporal
     logic (LTL) specification and bounded model checking (BMC). In this sense, our inte-
     gration is fully flexible and generic. Furthermore, the integration scheme allows us to
     enable synthesis for any verification procedure in UCLID5, by simply letting users de-
     clare and use functions to synthesize and relying on existing SyGuS-IF solvers to carry
     out the automated reasoning.
6       Polgreen et al

3.2   Multi-modal modeling

Combining Concurrent and Sequential Modeling A unique feature of the UCLID5
modeling language is the ability to easily combine sequential and concurrent modeling.
This allows a user to easily express models representing sequential programs, including
standard control flow, procedure calls, sequential updates, etc, in a sequential model,
and to combine these components within a system designed for concurrent modeling
based on transition systems. The sequential program modeling is inspired by systems
such as Boogie [5] and allows the user to port Boogie models to UCLID5. The con-
current modeling is done by defining transition systems with a set of initial states and a
transition relation. Within UCLID5, each module is a transition system. A main module
can be defined that triggers when each child module is stepped. For an example of this
combination of sequential and concurrent modeling, we refer the reader to the CPU ex-
ample presented in the original UCLID5 paper [40], which uses concurrent modules to
instantiate multiple CPU modules, modeled as transition systems, with sequential code
to model the code that executes instructions, and to the case study in Section 4.


Reasoning with External Oracles New in the latest version, UCLID5 supports the
modeling with oracle function symbols [37] in both verification and synthesis. Namely,
a user can include “oracle functions” in any UCLID5 model, where an oracle function
is a function without a provided implementation, but which is associated to a user-
provided external binary that can be queried by the solver. We note that oracle func-
tions (and functions in general) can only be first-order within the UCLID5 modeling
language, i.e., functions cannot receive functions as arguments.
    This support is useful in cases where some components of the system are difficult
or impossible to model, but could be compiled into a binary that the solver can query;
or where the model of the system would be challenging for an SMT solver to reason
about (for instance, highly non-linear arithmetic), and it may be better to outsource that
reasoning to an external binary.
    UCLID5 supports oracle function symbols in verification by interfacing with a
solver that supports Satisfiability Modulo Theories and Oracles (SMTO) [37], and in
synthesis by interfacing with a solver that supports Synthesis Modulo Oracles (SyMO) [37].
    Oracle function symbols are declared like functions, with the keyword oracle,
and an annotation pointing to the binary implementation. For instance oracle function
[isprime] Prime (x: integer) : boolean would indicate to the solver
that the binary isprime takes an integer as input and returns a boolean. This is trans-
lated into the corresponding syntax in SMTO or SyMO, as detailed in [35].
    An exemplar of such reasoning in a synthesis file is available in the artifact [36],
where we use UCLID5 to synthesize a safe and stabilizing controller for a Linear Time
Invariant system, similar to Abate et al. [1].


Combining Operational and Axiomatic Modeling UCLID5 can model a system be-
ing verified using an operational (transition system-based) approach, as Figure 2 shows.
However, UCLID5 also supports modeling a system in an axiomatic manner, whereby
the system is specified as a set of properties over traces. Any execution satisfying the
                                                                        UCLID5         7

properties is allowed by the system, and any execution violating the properties is dis-
allowed. Axiomatic modeling can provide order-of-magnitude performance improve-
ments over operational models in certain cases [3], and is often well suited to systems
with large amounts of non-determinism. We provide an example of fully axiomatic
modeling in the artifact [36].

    However, uniquely, UCLID5 allows users to specify multi-modal systems using a
combination of operational and axiomatic modeling. In such models, some constraints
on the execution are enforced by the initial state and transition relation (operational
modeling), while others are enforced through axiomatic invariants (axiomatic model-
ing). This allows the user to choose the mode of modeling most appropriate to each
constraint. For example, the ILA-MCM work [45] combined operational ILA (Instruc-
tion Level Abstraction) models to describe the functional behavior of processing ele-
ments with memory consistency model (MCM) orderings that are more naturally spec-
ified axiomatically [3]. (MCM orderings constrain shared-memory communication and
synchronization between multiple processing elements.) The combined model, used
for System-on-Chip verification, worked by sharing variables (called “facets”) between
both the models. UCLID5 makes it much easier to perform such a combination.

    Fig 3 depicts parts of a UCLID5 model of microarchitectural execution that uses
both operational and axiomatic modeling (similar to that from the ILA-MCM work),
based on the µspec specifications of COATCheck [29]. In this model, the steps of in-
struction execution are driven by the init and next blocks, i.e., the operational com-
ponent of the model. Multiple instructions can step at any time (curTime denotes the
current time in the execution), but they can only take one step per timestep. Mean-
while, axioms such as the fifoFetch axiom enforce ordering between the execution
of multiple instructions. The fifoFetch axiom specifically enforces that instructions
in program order on the same core must be fetched in program order. (Enforcing this
order is tricky using operational modeling alone). The transition rules and axioms op-
erate over the same data structures, ensuring that executions of the final model abide by
both sets of constraints.

    µspec models routinely function by grounding quantifiers over a finite set of in-
structions. Thus, to fully support µspec axiomatic modeling, we introduce two new
language features —namely, groups and finite quantifiers. A group is a set of objects of
a single type. A group can have any number of elements, but it must be finite, and the
group is immutable once created. For instance, the group testInstrs in Figure 3
consists of four instructions. Finite quantifiers, meanwhile, are used to quantify over
group elements.

     This example showcases UCLID5’s highly flexible multi-modal modeling capabil-
ity. Models can be purely operational, purely axiomatic, or a combination of the two.
Note that axiomatic modeling relies on the new language features finite forall
and groups. For a further example of axiomatic and operational multi-modal model-
ing, we refer the reader to the case study checking reachability properties in reactive
embedded systems described in the artifact [36].
     8       Polgreen et al


 1   module main {
 2       <type declarations>
 3       var i1, i2, i3, i4 : microop_t;
 4       <set i1-i4 to be the instructions of a test, like mp>
 5       group testInstrs : microop_t = {i1, i2, i3, i4};
 6
 7       //Vars to decide which instrs to step and when.
 8       var next1, next2, next3, next4 : boolean;
 9       var curTime : integer;
10
11       init {
12           i1.Fetch.nExists = false; i1.Execute.nExists = false;
13           <...>
14       }
15       //Axiom enforcing that instructions are fetched in order.
16       axiom fifoFetch :
17           finite_forall (i : microop_t) in testInstrs ::
18           finite_forall (j : microop_t) in testInstrs ::
19           (ProgramOrder(i, j) && NodeExists(j.Fetch)) ==>
20               EdgeExists(i.Fetch, j.Fetch);
21
22       procedure stepInst(index : integer)
23         returns (instr_next : microop_t)
24       {
25           //Steps instr@index, unless it has completed.
26           case
27                (index == 1) : {
28                    instr_next = i1;
29                    if(!instr_next.Fetch.nExists) {
30                        instr_next.Fetch.nExists = true;
31                        instr_next.Fetch.nTime = curTime;
32                    } else {
33                    <...>
34           esac
35       }
36       next {
37           //Increment the current timestamp and
38           //nondeterministically step instructions.
39           curTime’ = curTime + 1;
40           havoc next1, next2, next3, next4;
41
42           if (next1) { call (i1’) = stepInst(1); }
43           if (next2) { call (i2’) = stepInst(2); }
44           if (next3) { call (i3’) = stepInst(3); }
45           if (next4) { call (i4’) = stepInst(4); }
46       }
47   }


     Fig. 3: UCLID5 model that incorporates both operational modeling (through the init
     and next blocks) and axiomatic modeling (through the axiom keyword).


     4   Case Study: TAP model

     The final case study we wish to describe verifies a model of a trusted execution environ-
     ment. Trusted execution environments [22,12,11,18] often provide a software interface
     for users to execute enclaves, using hardware primitives to enforce memory isolation.
     In contrast to software which requires reasoning about sequential code, hardware mod-
     eling uses a paradigm that permits concurrent updates to a system. Moreover, verifying
     hyperproperties such as integrity requires reasoning about multiple instances of a sys-
     tem which most existing tools are not well suited for. In this section, we present the
                                                                          UCLID5          9




 1   module tap {
 2     // State variable declarations
 3     var tap_enclave_metadata_valid: tap_enclave_metadata_valid_t;
 4     var tap_enclave_metadata_addr_map: tap_enclave_metadata_addr_map_t;
 5     <...>
 6
 7       // Enclave operations
 8       procedure launch(eid: tap_enclave_id_t, <...>) { <...> }
 9       <...>
10
11       init { <...> } // initialize TAP
12
13       next { // step the system
14         case
15           (tap_current_mode == mode_untrusted) : {
16             call (<...>) = AdversarialStep(<...>);
17           }
18           (tap_current_mode == mode_enclave) : {
19             call (<...>) = EnclaveStep(<...>);
20           }
21         esac
22       }
23   }
24
25   module integrity_proof {
26     // Create two instances of the TAP model
27     instance tap_1: tap(<...>);
28     instance tap_2: tap(<...>);
29
30       // Example invariant: Memory that is mapped are equal between the two traces
31       invariant equal_mem: (forall (pa : wap_addr_t) ::
32         e_excl_map[pa] ==> (tap_1.mem[pa] == tap_2.mem[pa]));
33       <...>
34
35       init { <...> } // initialize proof
36
37       next { // step the system
38         next(tap_1); next(tap_2);
39       }
40
41       control {
42         v = induction;
43         check;
44       }
45   }



          Fig. 4: UCLID5 transition system-styled model of TAP and the integrity proof.
10         Polgreen et al

UCLID5 port 4 of the Trusted Abstract Platform (TAP) which was originally 5 written
in Boogie and introduced by Subramanyan et. al. [42] to model an abstract idealized
trusted enclave platform. We demonstrate how UCLID5’s multi-model support allevi-
ates the difficulties in modeling the TAP model in existing tools.


Modeling the TAP and Proving Integrity The UCLID5 model of TAP in Figure 4
demonstrates some of UCLID5’s key features: the enclave operations of the TAP model
(e.g. launch) are implemented as procedures, and a transition relation of the TAP
is defined using a next block that either executes an untrusted adversary operation or
the trusted enclave, which in turn executes one of the enclave operations atomically.
Proving the integrity hyperproperty on the TAP thus only requires two instantiations
of the TAP model, specifying the integrity invariants, and defining a next block which
steps each of the TAP instances as shown in the integrity proof module. The
integrity proof in UCLID5 uses inductive model checking.


Results and statistics of the TAP
modules Table 1 shows the approx- Model/Proof                       Size         Verif.
imate size of the TAP model in both                        #pr   #fn   #an  #ln  Time (s)
Boogie and UCLID5. #pr, #fn, #an,                             Boogie
and #ln refer to the number of pro- TAP                    22 25 254 1840 51
cedures, functions, annotations, and Integrity             14 11 71 835             346
lines of code respectively. Annota-                         UCLID5
tions are the number of loop invari- TAP                   53 25 87 2765 49
ants, assertions, assumptions, pre- Integrity              2     0     54 293        30
and post-conditions that were man-
ually specified. The verification time     Table 1: Boogie vs UCLID5 Model Results
includes compilation and solving.
    While the #ln for the TAP model in UCLID5 is higher than that of the model in
Boogie due to stylistic differences, the crucial difference is in the integrity proof. The
original model in Boogie implements the TAP model and integrity proof as procedures,
where the transition of the TAP model is implemented as a while loop. However, this
lack of support for modeling transition systems introduces duplicate state variables in
a hyperproperty such as integrity, requires context switching and additional procedures
for the new variables, which makes the model difficult to maintain and self composition
unwieldy. In UCLID5, the proof is no longer implemented as a procedure, but rather,
we create instances of the TAP model. We also note that the number of annotations is
less in UCLID5 compared to Boogie for the TAP model and proof. Additionally, this
model lends itself for more direct verification of hyperproperties.
    The verification results are run on a machine with 2.6GHz 6-Core Intel Core i7 and
16GB of RAM running OSX. As shown on the right of Table 1, the verification runtimes
between the Boogie and UCLID5 models and proofs are comparable.
 4
     https://github.com/uclid-org/trusted-abstract-platform/
 5
     https://github.com/0tcb/TAP
                                                                         UCLID5         11

5    Related Work

There are a multitude of verification and synthesis tools related to UCLID5. In this
brief review, we highlight prominent examples and contrast them with UCLID5 along
the key language features described in Section 3.
    UCLID5 allows users to combine sequential and concurrent modeling (see Sec-
tion 3.2). Most existing tools primarily support either sequential, e.g. [23,5,43], or con-
current computation modeling, e.g. [6,10,32,15,31]. Although users of these systems
can often overcome the tool’s modeling focus by manually including support for differ-
ent computation paradigms, for example, Dafny can be used to model concurrent sys-
tems [24], this is not always straightforward, and limited support for different paradigms
can manifest as limitations in downstream applications. For example, the Serval [34]
framework, based on Rosette, cannot reason about concurrent code. UCLID5, to the
best of our knowledge, is the only verification tool natively supporting modeling with
external oracles.
    UCLID5 supports different kinds of specifications and verification procedures (see
Section 3.1). Most existing tools[23,6,10] do not support multi-modal verification at all.
Tools that do offer multi-modal verification do not offer the same range of options as
UCLID5. For example, [31] does not support linear temporal logic, and [32,14] does
not support hyperproperty verification.
    Finally, UCLID5 supports a generic integration with program synthesis (see Sec-
tion 3.1), and so related work includes a number of synthesis engines. The SKETCH
system [41] synthesizes expressions to fill holes in programs, and has subsequently been
applied to program repair [21,17]. UCLID5 is more flexible than this work, and allows
users to declare unknown functions even in the verification annotations, as well as sup-
porting multiple verification algorithms and types of properties. Rosette [43] provides
support for synthesis and verification, but, unlike UCLID5, the synthesis is limited to
bounded specifications of sequential programs and external synthesis engines are not
supported. Synthesis algorithms have been used to assist in verification tasks, such as
safety and termination of loops [13], and generating invariants [16,46], but none of this
work to-date integrates program synthesis fully into an existing verification tool. Before
the new synthesis integration, UCLID5 supported synthesis of inductive invariants. The
key insight of this work is to generalize the synthesis support, and to unify all synthesis
tasks by re-using the verification back-end.


6    Software Project

The source code for UCLID5 is made publicly available under a BSD-license 6 . UCLID5
is maintained by the UCLID5 team 7 , and we welcome patches from the community.
Additional front-ends are available for UCLID5, including translators from Firrtl [19] 8 ,
 6
   https://github.com/uclid-org/uclid
 7
   https://github.com/uclid-org/uclid/blob/master/CONTRIBUTORS.md
 8
   https://github.com/uclid-org/chiselucl
12         Polgreen et al

and RISC-V binaries 9 to UCLID5 models. An artifact incuding the code for the case
studies in this paper is available [36].

Acknowledgments: The UCLID5 project is grateful for the significant contributions by
Pramod Subramanyan, one of the original creators of the tool. This work was supported
in part by NSF grant 1837132, the DARPA grant FA8750-20-C-0156 (LOGiCS), by the
Qualcomm Innovation Fellowship, and by Amazon and Intel.




 9
     https://github.com/uclid-org/riscverifier
                                                                                   UCLID5           13

References

 1. Abate, A., Bessa, I., Cordeiro, L.C., David, C., Kesseli, P., Kroening, D., Polgreen, E.: Au-
    tomated formal synthesis of provably safe digital controllers for continuous plants. Acta
    Informatica 57(1-2), 223–244 (2020)
 2. Adve, S., Gharachorloo, K.: Shared memory consistency models: A tutorial. IEEE Computer
    29(12), 66–76 (1996)
 3. Alglave, J., Maranget, L., Tautschnig, M.: Herding cats: Modelling, simulation, testing, and
    data-mining for weak memory. ACM Transactions on Programming Languages and Systems
    (TOPLAS) 36 (July 2014)
 4. Barbosa, H., Barrett, C.W., Brain, M., Kremer, G., Lachnitt, H., Mann, M., Mohamed, A.,
    Mohamed, M., Niemetz, A., Nötzli, A., Ozdemir, A., Preiner, M., Reynolds, A., Sheng, Y.,
    Tinelli, C., Zohar, Y.: CVC5: A versatile and industrial-strength SMT solver. In: TACAS (1).
    vol. 13243, pp. 415–442. Springer (2022)
 5. Barnett, M., Chang, B.Y.E., DeLine, R., Jacobs, B., Leino, K.R.M.: Boogie: A modular
    reusable verifier for object-oriented programs. In: International Symposium on Formal Meth-
    ods for Components and Objects. pp. 364–387. Springer (2005)
 6. Brayton, R.K., Mishchenko, A.: ABC: an academic industrial-strength verification tool. In:
    CAV. vol. 6174, pp. 24–40. Springer (2010)
 7. Bryant, R.E., Lahiri, S.K., Seshia, S.A.: Modeling and verifying systems using a logic of
    counter arithmetic with lambda expressions and uninterpreted functions. In: Brinksma, E.,
    Larsen, K.G. (eds.) CAV. pp. 78–92. LNCS 2404 (July 2002)
 8. Cheang, K., Rasmussen, C., Lee, D., Kohlbrenner, D., Asanović, K., Seshia, S.A.: Verifying
    RISC-V physical memory protection (2020)
 9. Cheang, K., Rasmussen, C., Seshia, S.A., Subramanyan, P.: A formal approach to secure
    speculation. In: Proceedings of the Computer Security Foundations Symposium (CSF) (June
    2019)
10. Cimatti, A., Roveri, M., Sheridan, D.: Bounded verification of past LTL. In: Hu, A.J., Martin,
    A.K. (eds.) FMCAD. pp. 245–259. Springer (2004)
11. Costan, V., Devadas, S.: Intel SGX explained. IACR Cryptol. ePrint Arch. 2016, 86 (2016)
12. Costan, V., Lebedev, I., Devadas, S.: Sanctum: Minimal hardware extensions for strong soft-
    ware isolation. In: 25th USENIX Security Symposium (USENIX Security 16). pp. 857–874.
    USENIX Association, Austin, TX (2016)
13. David, C., Kroening, D., Lewis, M.: Using program synthesis for program analysis. In:
    LPAR. pp. 483–498. Springer (2015)
14. Dill, D.L.: The Murphi verification system. In: CAV (1996)
15. Dutertre, B., Jovanović, D., Navas, J.A.: Verification of fault-tolerant protocols with Sally. In:
    Dutle, A., Muñoz, C., Narkawicz, A. (eds.) NASA Formal Methods. pp. 113–120. Springer,
    Cham (2018)
16. Fedyukovich, G., Bodı́k, R.: Accelerating syntax-guided invariant synthesis. In: TACAS (1).
    pp. 251–269. Springer (2018)
17. Hua, J., Zhang, M., Wang, K., Khurshid, S.: Towards practical program repair with on-
    demand candidate generation. In: ICSE. pp. 12–23. ACM (2018)
18. Intel: Intel trust domain extensions (2020), https://www.intel.com/content/www/us/en/
    developer/articles/technical/intel-trust-domain-extensions.html
19. Izraelevitz, A., Koenig, J., Li, P., Lin, R., Wang, A., Magyar, A., Kim, D., Schmidt, C.,
    Markley, C., Lawson, J., Bachrach, J.: Reusability is FIRRTL ground: Hardware construction
    languages, compiler frameworks, and transformations. In: 2017 IEEE/ACM International
    Conference on Computer-Aided Design (ICCAD). pp. 209–216 (Nov 2017)
14       Polgreen et al

20. Lamport, L.: How to make a multiprocessor computer that correctly executes multiprocess
    programs. IEEE Transactions on Computing 28(9), 690–691 (1979)
21. Le, X.D., Chu, D., Lo, D., Goues, C.L., Visser, W.: S3: syntax- and semantic-guided re-
    pair synthesis via programming by examples. In: ESEC/SIGSOFT FSE. pp. 593–604. ACM
    (2017)
22. Lee, D., Kohlbrenner, D., Shinde, S., Asanovic, K., Song, D.: Keystone: an open framework
    for architecting trusted execution environments. In: EuroSys. pp. 38:1–38:16. ACM (2020)
23. Leino, K.R.M.: Dafny: An automatic program verifier for functional correctness. In: Clarke,
    E.M., Voronkov, A. (eds.) Logic for Programming, Artificial Intelligence, and Reasoning.
    pp. 348–370. Springer (2010)
24. Leino, K.R.M.: Modeling concurrency in dafny. In: Bowen, J.P., Liu, Z., Zhang, Z. (eds.)
    Engineering Trustworthy Software Systems. pp. 115–142. Springer, Cham (2018)
25. Lohstroh, M., Íncer Romeo, Í., Goens, A., Derler, P., Castrillon, J., Lee, E.A., Sangiovanni-
    Vincentelli, A.: Reactors: A deterministic model for composable reactive systems. In: 8th
    International Workshop on Model-Based Design of Cyber Physical Systems (CyPhy’19).
    vol. LNCS 11971, p. 27. Springer-Verlag (2019)
26. Lohstroh, M., Menard, C., Bateni, S., Lee, E.A.: Toward a lingua franca for deterministic
    concurrent systems. ACM Trans. Embed. Comput. Syst. 20(4), 36:1–36:27 (2021)
27. Lohstroh, M., Menard, C., Bateni, S., Lee, E.A.: Toward a Lingua Franca for deterministic
    concurrent systems. ACM Transactions on Embedded Computing Systems (TECS) 20(4),
    Article 36 (May 2021). https://doi.org/10.1145/3448128
28. Lustig, D., Pellauer, M., Martonosi, M.: PipeCheck: Specifying and verifying microarchi-
    tectural enforcement of memory consistency models. 47th International Symposium on Mi-
    croarchitecture (MICRO) (2014)
29. Lustig, D., Sethi, G., Martonosi, M., Bhattacharjee, A.: Coatcheck: Verifying memory order-
    ing at the hardware-os interface. In: ASPLOS. pp. 233–247. ACM (2016)
30. Magyar, A., Biancolin, D., Koenig, J., Seshia, S.A., Bachrach, J., Asanovic, K.: Golden
    Gate: Bridging the resource-efficiency gap between ASICs and FPGA prototypes. In: In
    Proceedings of the International Conference on Computer-Aided Design (ICCAD). pp. 1–8
    (November 2019)
31. Mann, M., Irfan, A., Lonsing, F., Yang, Y., Zhang, H., Brown, K., Gupta, A., Barrett, C.:
    Pono: A flexible and extensible smt-based model checker. In: Silva, A., Leino, K.R.M. (eds.)
    CAV. pp. 461–474. Springer (2021)
32. McMillan, K.L., Padon, O.: Ivy: A multi-modal verification tool for distributed algorithms.
    In: Lahiri, S.K., Wang, C. (eds.) CAV. pp. 190–202. Springer, Cham (2020)
33. Mora, F., Cheang, K., Polgreen, E., Seshia, S.A.: Synthesis in UCLID5. CoRR
    abs/2007.06760 (2020)
34. Nelson, L., Bornholt, J., Gu, R., Baumann, A., Torlak, E., Wang, X.: Scaling symbolic eval-
    uation for automated verification of systems code with serval. In: SOSP. pp. 225–242. ACM
    (2019)
35. Padhi, S., Polgreen, E., Raghothaman, M., Reynolds, A., Udupa, A.: The SyGuS Language
    Standard Version 2.1. https://sygus.org/assets/pdf/SyGuS-IF.pdf (2014)
36. Polgreen, E., Cheang, K., Gaddamadugu, P., Godbole, A., Laeufer, K., Lin, S., Manerkar,
    Y.A., Mora, F., Seshia, S.A.: UCLID5 artifact. https://doi.org/10.5281/zenodo.6557711.
    https://doi.org/10.5281/zenodo.6557711
37. Polgreen, E., Reynolds, A., Seshia, S.A.: Satisfiability and synthesis modulo oracles. In:
    VMCAI. vol. 13182, pp. 263–284. Springer (2022)
38. Sahai, S., Subramanyan, P., Sinha, R.: Verification of quantitative hyperproperties using trace
    enumeration relations. In: CAV (1). vol. 12224, pp. 201–224. Springer (2020)
39. Seshia, S.A.: Combining induction, deduction, and structure for verification and synthesis.
    Proceedings of the IEEE 103(11), 2036–2051 (2015)
                                                                           UCLID5         15

40. Seshia, S.A., Subramanyan, P.: UCLID5: integrating modeling, verification, synthesis and
    learning. In: MEMOCODE. pp. 1–10. IEEE (2018)
41. Solar-Lezama, A.: The sketching approach to program synthesis. In: Asian Symposium on
    Programming Languages and Systems. pp. 4–13. Springer (2009)
42. Subramanyan, P., Sinha, R., Lebedev, I.A., Devadas, S., Seshia, S.A.: A formal foundation
    for secure remote execution of enclaves. In: CCS. pp. 2435–2450. ACM (2017)
43. Torlak, E., Bodı́k, R.: Growing solver-aided languages with rosette. In: Onward! pp. 135–
    152. ACM (2013)
44. Trippel, C., Lustig, D., Martonosi, M.: CheckMate: Automated synthesis of hardware ex-
    ploits and security litmus tests. In: 2018 51st Annual IEEE/ACM International Symposium
    on Microarchitecture (MICRO). pp. 947–960 (2018)
45. Zhang, H., Trippel, C., Manerkar, Y.A., Gupta, A., Martonosi, M., Malik, S.: ILA-MCM: In-
    tegrating memory consistency models with instruction-level abstractions for heterogeneous
    system-on-chip verification. In: FMCAD. pp. 1–10 (2018)
46. Zhang, H., Yang, W., Fedyukovich, G., Gupta, A., Malik, S.: Synthesizing environment in-
    variants for modular hardware verification. In: VMCAI. pp. 202–225. Springer (2020)


Appendix

A     Further examples

A.1   Case Study: Checking reachability properties in reactive embedded systems




                              Fig. 5: A simple train system.


    We further demonstrate the modeling flexibility of UCLID5 via a case study of
checking reachability properties in reactive embedded systems written in a coordina-
tion language called Lingua Franca (LF), which allows users to compose reactive com-
ponents called reactors [25,27]. LF adopts discrete event semantics in which events
are processed in timestamp order. Blocks of application code, named reactions (de-
noted in chevrons), can be activated by triggers, which include startup (circle), physical
action (triangle labeled by “P”), and ports (dark solid triangle). Figure 5 shows the di-
agram of a train door system with three reactors (Controller, Door, and Train).
The driver pressing a button provides the physical action, which triggers reaction 2 in
     16      Polgreen et al

     Controller. The reaction then outputs signals to close the door (by triggering the
     reaction in Door) and to move the train (by triggering the reaction in Train). Using a
     combination of axiomatic and operational modeling enabled by UCLID5, we can check
     whether the system permits an unsafe behavior where the train moves before the door
     closes.


 1   // All timestamps and microsteps are nonnegative.
 2   axiom(pi1(g(state)) >= 0 && pi2(g(state)) >= 0);
 3   // Each state can either be NULL or a specific id.
 4   axiom(id(ctrl1State) == NULL || id(ctrl1State) == controller_1);
 5   axiom(id(ctrl2State) == NULL || id(ctrl2State) == controller_2);
 6   axiom(id(trainState) == NULL || id(trainState) == train_1);
 7   axiom(id(doorState) == NULL || id(doorState) == door_1);
 8   next {
 9       havoc state; // Update state
10       case
11           (id(state) == door_1) : { doorState’ = state; doorCloses’ = true; }
12           (id(state) == train_1) : { trainState’ = state; trainMoves’ = true; }
13           (id(state) == controller_1) : { ctrl1State’ = state; }
14           (id(state) == controller_2) : { ctrl2State’ = state; }
15       esac
16       // Time tags do not decrement.
17       assume(tag_same(g(state’), g(state)) || tag_later(g(state’), g(state)));
18       // An event triggers only once in an instant.
19       assume(g(state) == g(state’) ==> id(state) != id(state’));
20       // Reaction with higher priority triggers first.
21       assume((g(state) == g(state’) && same_reactor(id(state), id(state’))) ==>
          priority(id(state)) < priority(id(state’)));
22       // Connection delay
23       assume((id(ctrl1State) != NULL && id(ctrl2State’) != NULL)
24           ==> tag_diff(g(ctrl2State’), g(ctrl1State)) == zero());
25       assume((id(ctrl2State) != NULL && id(trainState’) != NULL)
26           ==> tag_diff(g(trainState’), g(ctrl2State)) == zero());
27       assume((id(ctrl2State) != NULL && id(doorState’) != NULL)
28           ==> tag_diff(g(doorState’), g(ctrl2State)) == zero());
29       // Trigger mechanism
30       assume(id(ctrl1State) == NULL ==> id(ctrl2State’) == NULL);
31       assume(id(ctrl2State) == NULL ==> id(trainState’) == NULL);
32       assume(id(ctrl2State) == NULL ==> id(doorState’) == NULL);
33   }
34   property p: !(trainMoves && !doorCloses);
35   control {
36       v = induction;
37       check;
38       print_results;
39       v.print_cex;
40   }



                   Fig. 6: The UCLID5 model for the train system in Figure 5



         The UCLID5 snippet in Figure 6 illustrates this hybrid modeling approach. The ax-
     iomatic segment sits above the next block (line 1-7), specifying the semantics of reac-
     tors that should hold throughout the execution. Inside the next block, the havoc state-
     ment (line 9) sets the state variable in the next transition to a nondeterministic value.
     The case block (line 10-23) stores the new states in the appropriate state variables and
     sets boolean flags doorCloses and trainMoves. The assume statements (line
                                                                               UCLID5        17

24-39) constrain the next nondeterministic value of state to one that complies with
the language semantics. The operational modeling using the next block simplifies the
specification of constraints including non-decreasing time tags (line 25), unique event
per tag (line 27), reaction priority (line 29), connection delay (line 31-36), and trigger
mechanism (line 38-40). The reachability property, “the train does not move when the
door is open,” can then be checked using proof by induction (line 44).


A.2     Case Study: Fully axiomatic modeling



                                                               (i1)   (i2)   (i3)   (i4)
                                                          IF
               Core 0        Core 1
            (i1) [x] ← 1 (i3) r1 ← [y]                    EX

            (i2) [y] ← 1 (i4) r2 ← [x]
                                                         WB
              SC forbids: r1=1, r2=0
            (a) Code for litmus test mp.
                                                     (b) µhb graph for the execution of mp

Fig. 7: Left: Code for litmus test mp. The outcome r1=1,r2=0 is forbidden under
sequential consistency (SC) [20] (i.e., interleaving semantics). Right: An example µhb
graph for the execution of the mp litmus test where r1=1,r2=0 on a microarchitecture
with three-stage in-order pipelines. The graph is cyclic (as highlighted by the bolded
edges), implying that this execution is unobservable on the microarchitecture.

    In the rest of this section, we provide an example of how to encode fully axiomatic
models in UCLID5, specifically the µspec specifications of COATCheck [29].
    Program executions on microarchitectures (component-level models of hardware)
can be represented as microarchitectural happens-before (µhb) graphs [28]. Figure 7b
depicts an example µhb graph for the execution of the mp litmus test 10 on a pedagog-
ical microarchitecture with three-stage in-order pipelines of Fetch (IF), Execute (EX),
and Writeback (WB) stages. Nodes in these graphs represent sub-events in instruction
execution. For instance, the first node in the second row represents the event when in-
struction i1 from mp performs its Execute stage. Meanwhile, edges in µhb graphs rep-
resent happens-before relationships. For instance, the blue edge between the first two
nodes in the second row enforces that instruction i1’s Execute stage must occur before
the Execute stage of instruction i2, reflecting the in-order nature of this processor’s
pipelines.
    The presence or absence of nodes and edges in µhb graphs for a given microar-
chitecture are enforced by axioms in the domain-specific language µspec [29]. µspec
supports propositional logic over its built-in predicates. It also supports quantifiers over
instructions and enforces that the set of edges in µhb graphs is closed under transitivity.
10
     Litmus tests are small 4-8 instruction programs used in the verification of memory consis-
     tency [2]. µhb graphs and µspec specifications are typically used for memory consistency
     verification, but they can also be used for hardware security verification [44].
     18      Polgreen et al


 1   type uhbNode_t = record { nExists : boolean, nTime : integer };
 2
 3   type microop_t = record {
 4       globalID : integer, coreID : integer,
 5       <...>,
 6       Fetch : uhbNode_t, Execute : uhbNode_t,
 7       Writeback : uhbNode_t
 8   };
 9
10   define EdgeExists (src, dest : uhbNode_t) : boolean =
11    (src.nExists == true && dest.nExists == true && src.nTime < dest.nTime);
12   define NodeExists (n : uhbNode_t) : boolean = (n.nExists == true);
13   define ProgramOrder (i, j : microop_t) : boolean =
14    (i.globalID < j.globalID && i.coreID == j.coreID);
15
16   var i1, i2, i3, i4 : microop_t;
17   group testInstrs : microop_t = {i1, i2, i3, i4};
18
19   axiom ex_in_order :
20    finite_forall (a : microop_t) in testInstrs ::
21    finite_forall (b : microop_t) in testInstrs ::
22     EdgeExists(a.Fetch, b.Fetch) ==> EdgeExists(a.Execute, b.Execute);


     Fig. 8: Part of the embedding of µspec in UCLID5 and an example µspec axiom written
     in this embedding, illustrating UCLID5’s capability for axiomatic modeling.

          We embedded µspec into UCLID5 to showcase UCLID5’s capability for axiomatic
     modeling, as well as to enable µspec models to benefit from UCLID5’s built-in capabil-
     ities for modularity and synthesis (Section 3.1). Figure 8 shows part of this embedding
     as well as an example µspec axiom written using the embedding.
          We represent a µhb node in UCLID5 using two variables: a Boolean variable to rep-
     resent whether or not the node exists and an integer recording the execution timestamp
     at which it occurred. An instruction (microop t) consists of the nodes representing
     its sub-events as well as metadata such as its global ID (a unique identifier), core ID,
     address, and data value (some fields are not shown for brevity).
          The existence of an edge (EdgeExists) between two nodes can be modeled
     as enforcing that both the source and destination nodes exist, and constraining the
     source node’s timestamp to be less than that of the destination node. Node existence
     (NodeExists) merely checks the value of the nExists variable, while ProgramOrder
     is determined by ascending order of globalID on the same core.
          The axiom ex in order states that for every pair of instructions a and b in the
     group testInstrs, if an edge exists between their IF stages, then an edge must also
     exist between their EX stages. Thus, this axiom enforces the existence of the blue edges
     between the EX stages of i1 and i2 and between those of i3 and i4 in Figure 7b.
          Since edges in µhb graphs represent happens-before relationships, a cyclic µhb
     graph implies that an event must happen before itself. Thus, a cyclic µhb graph rep-
     resents an execution that is unobservable (i.e., impossible) on the microarchitecture be-
     ing modeled. Likewise, an acyclic µhb graph represents an execution that is observable
     on the microarchitecture. A given litmus test outcome can be verified on a microarchi-
     tecture by grounding the axioms over the instructions and outcome of that litmus test
     and asking a SMT solver to search for an acyclic µhb graph satisfying the axioms. If the
     solver returns a satisfying assignment, the test outcome is observable on the microarchi-
                                                                      UCLID5        19

tecture. If the solver returns UNSAT, the test outcome is guaranteed to be unobservable
on the microarchitecture.
    While litmus test verification of µspec specifications using SMT-based approaches
has been conducted by prior work [29], encoding such modeling in UCLID5 has the
benefit of harnessing UCLID5’s built-in capabilities for modularity and synthesis. In
fact, we are currently using UCLID5’s synthesis capability in ongoing work to synthe-
sise µspec axioms that match a set of examples.


A.3   Example: Control Synthesis with External Oracles
Consider the task of synthesising a controller for a Linear Time Invariant similar to
Abate et al. [1]. We use a state-space representation, which is discretized in time.
ẋt+1 = A~xt + B~ut , where ~x ∈ Rn , ~u ∈ Rp is the input to the system, calculated
as K~x where K is the controller to be synthesized, A ∈ Rn×n is the system matrix,
B ∈ Rn×p is the input matrix, and subscript t indicates the discrete time step.
    We aim to find a stabilizing controller K, such that absolute values of the (po-
tentially complex) eigenvalues of the closed-loop matrix A − BK are less than one,
checked by the oracle function isStable. We further require that the controller guar-
antees the states remain within a safe region of the state space up to a given number
of time steps, using the bounded model checking verification command in UCLID5, as
shown in Figure 9.
     20       Polgreen et al




 1   module main {
 2     var x0, x1: float;
 3     group stateVars : float = {x0, x1};
 4     const a00, a01, a10, a11 : float;
 5     const b0, b1 : float;
 6     const AminusBK00, AminusBK01, AminusBK10, AminusBK11 : float;
 7     oracle function [isstable] isStable(s00:float, s01:float, s10:float, s11:float)
          : boolean;
 8     synthesis function k0 (): float;
 9     synthesis function k1 (): float;
10
11       // LTI system spec
12       axiom A: (a00==0.901224922471 && a01==0.000000013429 && a10==0.000000007451 &&
            a11==0.000000000000);
13       axiom B: (b0==128.000000000000 && b1==0.000000000000);
14       axiom ax1: AminusBK00 == a00 - b0*k0() && !isNaN(AminusBK00);
15       axiom ax2: AminusBK01 == a01 - b0*k1() && !isNaN(AminusBK01);
16       axiom ax3: AminusBK10 == a10 - b1*k0() && !isNaN(AminusBK10);
17       axiom ax4: AminusBK11 == a11 - b1*k1() && !isNaN(AminusBK11);
18
19       init { // bound initial states
20         assume (finite_forall (state: float) in stateVars :: state<0.1 && state >
            -0.1);
21       }
22       next { // step the system
23         x0’ = AminusBK00*x0 + AminusBK01*x1;
24         x1’ = AminusBK10*x0 + AminusBK11*x1;
25       }
26       // the safety condition
27       invariant stability: isStable(AminusBK00, AminusBK01, AminusBK10, AminusBK11);
28       invariant safety: finite_forall (state: float) in stateVars :: state < 1.0 &&
            state > -1.0;
29       invariant isNotNaN: finite_forall (state: float) in stateVars :: state < 1.0 &&
            state > -1.0;
30
31       control {
32         unroll(10); // fix safety bound
33         check;
34       }
35   }



     Fig. 9: UCLID5 control synthesis example. The next block assigns to the state variables
     according to the standard definition of Linear Time Invariant systems. Note this model
     uses finite quantifiers, as described in Section 3.2.
