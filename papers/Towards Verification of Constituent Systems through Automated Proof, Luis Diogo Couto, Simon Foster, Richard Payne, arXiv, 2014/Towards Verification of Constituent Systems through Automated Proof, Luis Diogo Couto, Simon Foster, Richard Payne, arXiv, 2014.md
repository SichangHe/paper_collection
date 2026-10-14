                                                   Towards Verification of Constituent Systems
                                                           through Automated Proof

                                                  Luı́s Diogo Couto                               Simon Foster                                 Richard Payne
                                             Aarhus University, Denmark              University of York, United Kingdom           Newcastle University, United Kingdom
                                                   ldc@eng.au.dk                          simon.foster@york.ac.uk                       richard.payne@ncl.ac.uk


                                           Abstract—This paper explores verification of constituent sys-         Obligation Generator (POG). A theorem prover can be applied
                                       tems within the context of the Symphony tool platform for Systems         to verify a software system, that is mathematically demonstrate
arXiv:1404.7792v2 [cs.SE] 7 May 2014




                                       of Systems (SoS). Our SoS modelling language, CML, supports               that required properties are met through mechanically verified
                                       various contractual specification elements, such as state invariants      proof. In the case of CSs, we need to verify that the internal
                                       and operation preconditions, which can be used to specify                 functionality and pattern of interaction is guaranteed to fulfil
                                       contractual obligations on the constituent systems of a SoS. To
                                       support verification of these obligations we have developed a proof
                                                                                                                 the contract. In Symphony this verification can be facilitated
                                       obligation generator and theorem prover plugin for Symphony.              through the POG which generates proof goals upon which the
                                       The latter uses the Isabelle/HOL theorem prover to automatically          correctness of the CS model depends. CML has a number of
                                       discharge the proof obligations arising from a CML model. Our             facilities for specifying contractual obligations, such as type
                                       hope is that the resulting proofs can then be used to formally            invariants, pre- and post-conditions for functions and opera-
                                       verify the conformance of each constituent system, which is turn          tions, and system state invariants. These can then variously be
                                       would result in a dependable SoS.                                         used to specify contractual obligations for a CS model, and the
                                                                                                                 application of the POG in concert with the TPP can be used to
                                                              I.   I NTRODUCTION                                 verify that the system satisfies those obligations. Our thesis is,
                                                                                                                 therefore, that these technologies provide a way forward for
                                           A System of Systems (SoS) [1] is a collection of seman-               mechanically verifying that a CS model fulfils its contractual
                                       tically heterogeneous, independent, and distributed constituent           obligations to the wider SoS.
                                       systems (CSs) which are co-ordinated to achieve an overall
                                       goal. Independence means that no CS can exert control on                      In the remainder we outline our contributions. Section II
                                       another CS, only influence its behaviour by offering potential            gives more background to our baseline technology. Section III
                                       opportunities should synergy be reached. Since CSs are dy-                discusses related work. Section IV discusses the combined
                                       namic and heterogeneous, often changing their capabilities and            POG and TPP framework, and how it can be used to verify a
                                       services, such synergy is achieved by negotiation of contracts            CS model. Section V demonstrates an example CS, and how
                                       between a set of CSs, which impose binding conditions on                  we envisage verifying it for a wider SoS. Finally in Section VI
                                       the behaviour of each CS. Since failure of such an agreement              we conclude and outline future work.
                                       will result in degradation of the SoS, it is important that each
                                       CS has some measure of certainty in its ability to fulfil its                                   II.   BACKGROUND
                                       requirements, which in turn will lead to a dependable SoS.                    CML is a language for modelling constituent systems and
                                           System of Systems Engineering (SoSE) therefore requires               their composition in an SoS. Systems are modelled using
                                       languages with which we can accurately model CSs to predict               CML processes, which are stateful reactive entities that can be
                                       their behaviour, and tools which enable their verification.               executed concurrently, and exchange messages over channels
                                       Such languages should have a sound theoretical background                 in the style of the CSP process calculus [4]. A CML model
                                       to ensure that they can be assigned a consistent behaviour,               consists of a collection of user defined types, functions, chan-
                                       and the ability to handle the composition of heterogeneous                nels, and processes. A process, in turn, consists of private state
                                       constituents. To this end the COMPASS Modelling Language                  variables, operations that act on these variables, and actions
                                       (CML) [2] has been developed, a formal modelling language                 that specify reactive behaviour using operators from CSP. CML
                                       for SoSs. CML reproduces the style of the VDM-SL [3] formal               processes can be parallel composed to represent concurrent
                                       specification language, whilst integrating CSP [4] process                execution, enabling description of a complete SoS.
                                       modelling constructs from the Circus [5] language. CML has a                  CML has a formal mathematical foundation [7] based in
                                       formal semantics based in Hoare and He’s Unifying Theories                the UTP semantic framework [6], which allows processes
                                       of Programming (UTP) [6], in its denotational, operational, and           to be given a precise semantics. UTP allows us to tackle
                                       axiomatic flavours. Along with the associated Symphony1 tool              semantic heterogeneity in SoSE by decomposing a modelling
                                       platform, CML allows SoSs and CSs to be formally modelled,                language semantics into its theoretical building blocks, such as
                                       tested, and verified in a controlled environment.                         state, concurrency, discrete time, and mobility, which can then
                                          This paper focuses on two closely related components                   be formalised as “UTP theories”. UTP theories then act as
                                       of Symphony, the Theorem Prover Plugin (TPP) and Proof                    components with which we can construct semantic models for
                                                                                                                 languages and provide links between similar languages based
                                         1 Symphony can be downloaded from http://symphonytool.org/              on common theoretical factors.
                                                                  currently working towards a formal axiomatic semantics for
                                                                  these proof obligations based on the current implementation,
                                                                  which will allow the integration of these proof objects with
                                                                  other evidences in the tool-chain.

                                                                                             III.    R ELATED W ORK
                                                                      The Symphony tool platform is an extension of the open
                                                                  source Overture IDE [11] for VDM based modelling. The
                                                                  Symphony POG is an adaptation of the POG for Overture [12]
                                                                  to also handle CML proof obligations. Previous efforts to
                                                                  generate and discharge Proof Obligations (POs) for VDM
   Fig. 1: Semantically supported Symphony tool platform          include [13] and [14], which connect VDMTools and Overture
                                                                  POs respectively to the HOL4 theorem prover [15]. These at-
    Development of CML models is aided through the as-            tempts were limited to the functional subset of VDM. We use a
sociated Symphony tool platform. Symphony is an Eclipse-          similar mapping for CML types and expressions, whilst adding
based development environment that provides a parser, syn-        support for CML’s imperative and concurrent constructs.
tax highlighting, a type checker, simulator, model checker,           The area of theorem proving tools includes a number of
and a variety of other tools for variously constructing and       options including Isabelle/HOL [9] (which we use); PVS2
verifying CML models. Though consisting of independently          combining a specification language with a theorem prover;
developed components, the different tools share a common          Coq [16], a proof assistant based on intuitionistic logic;
semantic foundation given by the UTP denotational model.          specialised verification systems such as Spec], which is based
This “semantic stack” is shown in Figure 1, with the Symphony     on the Boogie verification language [17] and supported by the
platform and associated components positioned on top. Within      Z3 SMT solver [18]; and the Rodin3 tool for Event-B which
the UTP relational calculus several computational paradigms       includes an automated theorem prover.
have been formalised as UTP theories (Contracts, Processes,
etc.), and these have been in turn composed to produce                We choose Isabelle for several reasons. It is based on
the CML denotational semantics. Finally, reference semantics      Higher Order Logic which is ideal for embedding a language
have been produced that underlie the various tools, including     like CML. The LCF architecture ensures proofs are correct
the operational semantics, which underlies the simulator and      with respect to a secure logical core. It has a large library
model checker, and various axiomatic semantics, such as a         of mathematical structures related to program verification,
Hoare calculus [8]. Since this formal link exists from each       such as relational calculus and lattice theory. It integrates
tool down into the unified semantic basis we can have a           powerful proof facilities, such as the auto tactic for automated
degree of certainty that the various evidences produced can       deduction, integration of first-order automated theorem provers
be consistently composed to verify a CS model.                    (like Z3) in the sledgehammer tool [19], and counterexample
                                                                  generators like nitpick. We can directly harness many of these
    To support such verifications we have created a theo-         proof facilities by our transfer based proof tactics. Finally,
rem prover plugin, based on the Isabelle/HOL [9] interac-         Isabelle has been integrated into Eclipse in the form of
tive theorem prover. Isabelle/HOL is ideal for this kind of       Isabelle/Eclipse4 , an IDE which we reuse in Symphony.
verification since proofs can be independently checked with
respect to a secure axiomatic core; a facet of the “LCF               IV.     PO G ENERATION AND D ISCHARGE IN S YMPHONY
architecture”. Our theorem prover is based in a mechanised
semantic framework for UTP called Isabelle/UTP [10] that              The Symphony POG is an extension of the Overture
provides a strong theoretical grounding for CML, ensuring its     POG for the Vienna Development Method (VDM) [12], and
consistency. We have mechanised a partial semantic model          therefore many proof goals generated are derived from VDM.
for CML in Isabelle/UTP, a collection of associated proof         However, the POG has been developed with an extensible
tactics, and a visitor that translates the CML Abstract Syntax    visitor [20] based architecture that will enable the addition of
Tree (AST) into Isabelle definitions that can then be used to     further goals as they are researched. The current proof goals
support proof. Our current approach to proof in CML is to,        fall broadly into the following categories: safe usage of partial
where possible, convert CML to equivalent HOL formulae, and       operators; safe usage of functions with pre-conditions; type
perform the proof using Isabelle’s variety of existing tactics    compatibility due to union types, type invariants and subtypes;
and laws, effectively transferring results from HOL to UTP.       and satisfiability of implicitly defined functions and operations.
In line with the UTP framework, the theorem prover is fully           To illustrate the use of POs in Symphony, we present a
extensible: we can add support for additional programming         simple example based on a well known partial operator case:
concepts, and associated tactics as required in the future.       division by zero. Consider the following CML function:
    Alongside the theorem prover, Symphony contains a POG                                                                    
that generates, for a given CML document, a collection of         division : int * int → real
proof goals that must be satisfied to prove certain high level    division (x,y) == x / y
                                                                                                                                      
properties of the model, such as internal consistency, contrac-
tual correctness of operations, and termination. The TPP can          2 http://pvs.cdl.sri.com
then be used to attempt discharge of these proof obligations,         3 http://event-b.org

resulting in concrete proof objects for the properties. We are        4 http://andriusvelykis.github.io/isabelle-eclipse/
                 Fig. 2: Failed PO discharge.

For this function, the POG generates an obligation stating that,
for all inputs to the function, the value of the divisor (y) will
not be 0, thus ensuring the function executes successfully. This
is represented in the logical formula below:
                                                                 
PO1: forall x:int, y:int & (y <> 0)                                                Fig. 4: Auto-generated theory files.
                                                                
This states that for all variables x and y of type int, y is
                                                                     While the example shown was very simple, pre-conditions
not equal to 0. This is not satisfiable, and so an attempt to
                                                                 (and invariants) can be as complex as necessary. They are
discharge this PO will fail as shown in Figure 2. The function
                                                                 expressed in the functional subset CML and thus have the
must be enriched with a pre-condition, using the pre keyword,
                                                                 full expressive power of CML’s first-order logic. In addition
in order for the discharge to be possible:
                                                               to helping ensure consistency of the model, pre-conditions and
 division : int      int → real                                  invariants are also used to specify additional properties
               *
division (x,y) == x / y                                                   In fact, the methodology we propose is based precisely
pre y <> 0
                                                                    on specifying desired properties and requirements of a model
                                                                      through pre- and post-conditions as well as invariants. The
The additional information offered by the pre-condition alters
                                                                      POs, once generated and discharged, stand as proof that the
the PO and now the theorem prover plug-in is able to discharge
                                                                      model respects the specified properties.
the revised PO as shown in Figure 3. It is of course not possible
to prove that an arbitrary integer is different from zero, but it         Discharging POs is the task of the TPP. At its core, the
is trivial to prove that a non-zero integer is different from zero.   TPP consists of a mechanised semantic model for CML within
                                                                      Isabelle/UTP. It is essentially a deep embedding of CML, in
                                                                      that we give an explicit semantics to each of the operators of
                                                                      CML processes within Isabelle.
                                                                          The TPP will process a CML model and its associated POs
                                                                      and automatically generate Isabelle theory files for them (see
                                                                      Figure 4). These theory files can then be submitted to Isabelle
                                                                      for discharging through various automated proof tactics such
                                                                      as auto and sledgehammer, or the cml tac tactic that maps
               Fig. 3: Successful PO discharge.                       a CML formula onto a HOL formula.
                                                                          Because the TPP connects to the Isabelle/Eclipse plug-in,
The aforementioned example was trivial but, in general, it is
                                                                      the full functionality of that plug-in and, by extension, Isabelle
quite important to ensure that, when adding a pre-condition,
                                                                      is available to the user . This includes the ability to write and
said pre-condition is sufficient to allow the discharge of any
                                                                      discharge model-specific conjectures directly in the Isabelle
POs generated for the function.
                                                                      encoding of the model. However, to perform this kind of work
    The addition of the pre-condition has another effect. One         requires significant knowledge of Isabelle and its syntax.
must now ensure that, whenever the function is called its                 Therefore, the POG will be the primary source of goals
pre-condition is respected. Therefore, a new kind of PO is            to discharge. Furthermore, the TPP offers a fully automated
generated. Consider the following function and PO:                    mode of interaction with Isabelle where users simply choose
                                                                    which PO to discharge and all inner workings (such as tactic
divby2: int → real                                                    selection and result collection) are hidden from them.
divby2 (x) == division(x,2)
                                                                We envisage two main functionalities for the plug-ins Quick
                                                            check and Proof Session. Quick check will be a fully automated
PO2: forall x : int & pre_division(x,2)                       process, simply presenting a list of Proof Obligations (POs)
                                                            (including their predicates) in CML and linked to the relevant
                                                              model elements. The process of generating POs is quick,
Since divby2 calls division, a PO is generated to
                                                              therefore this may be performed frequently during initial model
ensure that the pre-condition of division, given by
                                                              development, to gain useful feedback about the model.
pre_division, is satisfied. This kind of obligation, called
pre-condition obligation is generated at all points               The Proof Session will be the main functionality of the
in the model where the function is called.                    plug-ins. It creates a snapshot of the model (a timestamped,
read-only copy of the model’s CML sources), generates POs
and translates the model and POs into Isabelle theories. The
POs are displayed in a similar manner to the quick check
version but can now be submitted to the TPP for discharge.
At the moment only cml tac is available, though we hope to
enable automated use of additional tactics when attempting to
discharge POs. Regardless, the output of a proof attempt will
be captured from Isabelle and displayed to the user. Also, the
results of a proof session will be stored along with the model
snapshot, thus verifying the model’s correctness.
   These two functionalities combine to form the following
work-flow: as a user works on a model, he can quick check for
POs as a way to gain early insights into the of the model. Each         Fig. 5: Picture of railway signal, with lamps indicated
PO can be seen of as a possible inconsistency and merely by
manual inspection they can guide the user in terms of adding
necessary pre-conditions or guards to the model.
    Once a set of changes has been completed, the user                The Dwarf Signal model is defined in CML with several
may use the proof session functionality to verify the model’s     datatypes, functions, a single Dwarf process with state vari-
correctness. Each set of POs and their associated proofs are      ables, operations and actions. The main datatype, DwarfType
only valid for the particular version of the model they were      shown below, has several fields relating to the transitions
generated from so it makes little sense to attempt manual         which are to be made in the Dwarf Signal. For example,
proofs on a volatile model. Regardless of when it is attempted,   the currentstate field dictates the collection of lamps
the proof session for the average user will be fully automated.   currently lit, and the desiredproperstate field repre-
The user simply initiates a proof session and selects POs for     sents the next state the Dwarf Signal should reach. The set of
discharging either manually or in batch. Typically some POs       possible signal states that may be reached is defined by the
will be successfully discharged whereas others will fail to       ProperState datatype, which is constrained to be one of
discharge. These should indicate a problem with the model         for constant values: dark, stop, warning and drive
and action must be taken by the user (for example, by adding      – each a set of lamps.
a guard or correcting program logic) to alter the model in a
way that allows the PO to be discharged. Then, the set of
                                                                                                                                 
completed PO goals can be used as a formal proof of the           types
constituent system’s correctness.                                  LampId      = <L1> | <L2> | <L3>
                                                                   Signal      = set of LampId
   For advanced users who are comfortable interacting with         ProperState = Signal
Isabelle/Eclipse directly, the full theorem proving perspective    inv ps == ps in set {dark, stop, warning, drive}
gives them direct access to the tool so that manual proofs may
be attempted. Users can also specify and discharge additional         DwarfType :: lastproperstate    : ProperState
model-specific conjectures.                                                        turnoff            : set of LampId
                                                                                   turnon             : set of LampId
                                                                                   laststate          : Signal
 V.   V ERIFICATION OF E XAMPLE C ONSTITUENT S YSTEM                               currentstate       : Signal
                                                                                   desiredproperstate : ProperState
    We illustrate the use of the Symphony tool platform POG           inv d == NeverShowAll(d) and MaxOneLampChange(d)
and TPP with a simple example CS from a Railway Signal                    and ForbidStopToDrive(d) and DarkOnlyToStop(d)
System of Systems (SoS). The SoS in question aims to ensure               and DarkOnlyFromStop(d)
the safe and correct movement of trains on a section of
                                                                  values
railway tack. Naturally such a SoS poses several dependability     dark: Signal    = {}
concerns and the integrator of the SoS requires several safety     stop: Signal    = {<L1>, <L2>}
properties to hold throughout the life of each of the systems.     warning: Signal = {<L1>, <L3>}
                                                                   drive: Signal   = {<L2>, <L3>}
    The Railway Signal SoS comprises several constituents                                                                        
including a Route Rule Engine, several Track Actuators, Trains
and Dwarf Signal systems. In this paper, we look at one of the
constituent systems – the Dwarf Signal system – in detail and
                                                                  There are several safety properties to which the Dwarf Signal
consider the safety properties of that system.
                                                                  must adhere. These are defined in terms of functions referred
    From the perspective of the SoS integrator, there is a        to in the DwarfType invariant – including, for example,
requirement that the procured constituent systems provide a       NeverShowAll which requires that the currentstate
safe service. The constituent system designer must, therefore,    should never have all three lamps lit. The Dwarf pro-
provide evidence of this safety. Using model-based techniques,    cess, outlined below has a single state variable: dw of type
we define a formal model of the Dwarf Signal – which may be       DwarfType, and four operations: Init, which initialises
used as a contract to which the the signals must conform. The     the dw state variable; SetNewProperState, allowing the
Dwarf model used in this paper is based upon that introduced      next desired properstate to be set; and two operations for
in [21], and a typical signal may be seen in Figure 5.            changing the lamps lit in the signal – TurnOn and TurnOff.
                                                                 Symphony in the POG perspective with the POs represented
process Dwarf = begin                                              in the Isabelle syntax used by the TPP. In the figure, the list
state
  dw : DwarfType
                                                                   of POs is given in the right hand pane, with a pane showing
                                                                   the PO definition in CML below. In the figure, we see that
operations                                                         several of the POs have been discharged – these relate to the
  Init : () ==> ()                                                 Init operation above – as denoted by the green ticks.
  Init() == (...)

    SetNewProperState: (ProperState) ==> ()
    SetNewProperState(st) == (...)

    TurnOn: (LampId) ==> ()
    TurnOn(l) == (...)

     TurnOff : (LampId) ==> ()
     TurnOff(l) == (...)
    ... end
                                                              
Each operation is defined in more detail in terms of pre- and
post-conditions, dictating the conditions in which the operation
may be called and the guarantees it makes if those conditions
are met. The Init operation, defined in more detail below,
has a body which initialises the dw state variable, with a post-
condition requiring that various fields of the dw variable are
updated. The operation body – an assignment to the dw state              Fig. 6: Progress on POs generated for Dwarf model
variable – must respect the safety properties of the Dwarf
Signal, in the form of the type invariant described above.             By discharging all POs for the Dwarf Signal model, we
                                                                 provide   a contractual model which is verified to be both
Init : () ==> ()                                                   internally consistent and, through encoding the safety prop-
Init() ==                                                          erties which must be met by a signal, is safe with respect
  dw := mk_DwarfType(stop, {}, {}, stop, stop, stop)               to the requirements placed on that contract. At present, whilst
post dw.lastproperstate = stop and dw.turnoff = {}                 those POs shown are successfully discharged by the Symphony
         and dw.turnon = {} and dw.laststate = stop
         and dw.currentstate = stop                                TPP, several are not. These relate to those POs which rely
         and dw.desiredproperstate = stop                          upon the value of the Dwarf process state variable dw at
                                                                 a given point of time. This may be either an issue with
                                                                   the PO expressions themselves (where the VDM-based PO
The remainder of the CML operations are defined in a similar
                                                                   expressions require further adaption to CML), or due to the
manner – with pre- and post- conditions. In addition to these
                                                                   early stage of development of the TPP proof tactics. We discuss
operation definitions, the CML model contains actions which
                                                                   these areas as future work in the next section.
dictate the ordering of internal events and operation calls. At
present, the POG does not handle these features of CML, and
thus they are omitted from this paper.                                        VI. C ONCLUSION AND F UTURE W ORK
    Executing the Symphony POG, we obtain several POs,            In this paper, we have outlined two Symphony tool plat-
which are generated by the Init, SetNewProperState,           form plugins which enable automated proof support for CML
TurnOn and TurnOff operations. The POs fall into two          POs. The Symphony POG reuses and expands upon the Over-
PO types: ensuring that the postcondition holds given the     ture POG, also resulting in improvements in the Overture Tool.
body of the operation; and ensuring subtype consistency. It   The TPP is the first attempt at tightly integrating a theorem
is the second of these which ensures that the DwarfType       prover into the VDM family of tools, providing a more useful
type invariant (and thus the safety properties of the Dwarf   tool for users wishing to discharge CML POs and general
Signal) holds when setting a new value of the dw variable.    theorems. We have also shown how both plug-ins can be used
The generated subtype POs (PO1 and PO2) and postcondition     in combination to formally verify the integrity of constituent
PO (PO3) for the Init operation are shown below.              systems of an SoS specified with CML. There are clearly many
                                                            areas of future work, both short-term improvements to the
PO1: inv_ProperState(stop)                                    two plugins, and also longer-term directions and scoping of
                                                              the work in the fields of SoS and dependability-related issues.
PO2: ((inv_DwarfType(mk_DwarfType(stop, {}, {}, stop
     , stop, stop)) and inv_ProperState(stop)) and            Below, we discuss several such directions for further work.
       inv_ProperState(stop))
                                                                  This paper demonstrated the verification of constituent
PO3: (((dw.lastproperstate) = stop) and (((dw.                system models. An interesting issue would be the verification
    turnoff) = {}) and (((dw.turnon) = {}) and (((dw          of an actual implementation, with respect to realistic system
    .laststate) = stop) and (((dw.currentstate) =             properties. Whilst clearly not in the scope of this paper,
    stop) and ((dw.desiredproperstate) = stop))))))
                                                            we would consider the work of this paper in context with
                                                              other system engineering activities. In particular; positioning
   Using the Symphony tool platform, we generate these POs,   constituent system verification with respect to the work of
and attempt to discharge them. In Figure 6 below, we show     Holt et al [22] on SoS requirements engineering and the
specification of SysML contracts and translation to CML [23]          Systems” (COMPASS, Grant Agreement 287829). For more
may provide the means to more realistic property verification.        information see http://www.compass-research.eu.
    The current CML TPP focuses on VDM-style proof obli-
                                                                                                    R EFERENCES
gations which deal with issues such as subtyping and internal
consistency. In the future we will extend this with a more             [1]   H. Kopetz, “System-of-Systems Complexity,” in Proc. 1st Workshop on
comprehensive calculus, such as a Hoare logic [8] or a                       Advances in Systems of Systems, 2013, pp. 35–39.
weakest precondition calculus, which would both expand on              [2]   J. Woodcock, A. Cavalcanti, J. Fitzgerald, P. Larsen, A. Miyazawa,
                                                                             and S. Perry, “Features of CML: a Formal Modelling Language for
the existing proof obligations. This would also allow us to                  Systems of Systems,” in Proc. 7th Intl. Conference on Systems of
reason directly about CML process and state behaviour, and                   Systems Engineering (SoSE). IEEE, July 2012.
therefore provide fuller support for reasoning about contracts.        [3]   C. B. Jones, Systematic Software Development Using VDM. Prentice-
                                                                             Hall, 1990.
    Another extension to the proof obligations relates to scaling
                                                                       [4]   T. Hoare, Communicating Sequential Processes. Prentice-Hall, 1985.
our approach from the level of constituent systems to the
                                                                       [5]   J. C. P. Woodcock and A. L. C. Cavalcanti, “A Concurrent Language
SoS-level, thus ensuring that the verified constituent systems               for Refinement,” in IWFM’01: 5th Irish Workshop in Formal Methods,
interact in a manner that ensures the desired behaviour of the               ser. BCS Electronic Workshops in Computing, July 2001.
overall SoS.                                                           [6]   T. Hoare and J. He, Unifying Theories of Programming. Prentice Hall,
                                                                             1998.
    Just as pre-conditions and invariants can be used to specify
                                                                       [7]   J. Fitzgerald, P. G. Larsen, and J. Woodcock, “Foundations for Model-
the properties that the POG and TPP verify, we need a                        based Engineering of Systems of Systems,” in Complex Systems Design
mechanism that allows these tools to reason about correctness                and Management, M. A. et al., Ed. Springer, January 2014, pp. 1–19.
at the SoS level. We see two distinct possibilities here: the first    [8]   S. Canham and J. Woodcock, “CML Definition 3 — Hoare Logic,”
is to introduce a new CML construct that allows one to specify               COMPASS Deliverable, D23.4d, Tech. Rep., September 2013.
invariants over the entire SoS, thus being able to “see” inside        [9]   T. Nipkow, M. Wenzel, and L. Paulson, Isabelle/HOL: A Proof Assistant
all constituents. The second approach is to take the existing                for Higher-Order Logic, ser. LNCS. Springer, 2002, vol. 2283.
POs that verifies a system and use them to also verify the            [10]   S. Foster, F. Zeyda, and J. Woodcock, “Isabelle/UTP: A mechanised
interface of a constituent. Afterwards, one must establish a                 theory engineering framework,” in 5th Intl. Symposium on Unifying
                                                                             Theories of Programming, 2014.
means by which these verified interfaces can be combined to
                                                                      [11]   P. G. Larsen, N. Battle, M. Ferreira, J. Fitzgerald, K. Lausdahl, and
establish global SoS properties. Of the two approaches, the                  M. Verhoef, “The Overture Initiative – Integrating Tools for VDM,”
second one seems closer to the spirit of SoS engineering, and                SIGSOFT Software Engineering Notes, vol. 35, no. 1, Jan 2010.
we believe CS refinement provides a way forward here.                 [12]   L. Couto and R. Payne, “The COMPASS Proof Obligation Generator: A
                                                                             test case of Overture Extensibility,” in Proc. 11th Overture Workshop,
    We are also currently working on a tool for CS refinement,               2013.
which combines with the theorem prover and can be used to             [13]   S. Agerholm and K. Sunesen, “Reasoning about VDM-SL Proof Obli-
formally demonstrate contractual satisfaction. This will reuse               gations in HOL,” IFAD, Tech. Rep., 1999.
the POG to enumerate and discharge refinement provisos                [14]   S. Vermolen, “Automatically Discharging VDM Proof Obligations us-
which must often be satisfied to ensure validity of a refinement             ing HOL,” Master’s thesis, Radboud University Nijmegen, Computer
step. Refinement will be principally supported by Isabelle,                  Science Dept., August 2007.
though we are also exploring the use of model generation              [15]   K. Slind and M. Norrish, “A brief overview of HOL4,” in TPHOLs, ser.
tools to aid automation. For example, the Maude rewriting                    LNCS, vol. 5170. Springer, 2008, pp. 28–32.
logic engine [24] has previously been applied to automated            [16]   Y. Bertot and P. Castéran, Coq’Art: the calculus of inductive construc-
                                                                             tions. Springer, 2004.
refinement [25], which we hope to adapt for CML. Such
                                                                      [17]   M. Barnett, B. E. Chang, R. DeLine, B. Jacobs, and K. R. M. Leino,
advances over the current technology are feasible because of                 “Boogie: A Modular Reusable Verifier for Object-Oriented Programs,”
our extensible approach to semantics provided by UTP.                        in Formal Methods for Components and Objects. Springer, 2006.
    Finally, though both plug-ins presented here are still at         [18]   L. De Moura and N. Bjørner, “Z3: an efficient SMT solver,” in TACAS,
                                                                             ser. LNCS, vol. 4963. Springer, 2008.
an early development stage, work is ongoing on various
                                                                      [19]   J. C. Blanchette, L. Bulwahn, and T. Nipkow, “Automatic proof and
improvements. While the TPP and its associated Isabelle the-                 disproof in Isabelle/HOL,” in FroCoS, ser. LNCS, vol. 6989. Springer,
ories support a significant subset of CML (types, expressions,               2011, pp. 12–27.
functions, and operations), work is ongoing on increasing the         [20]   E. Gamma, R. Helm, R. Johnson, and J. Vlissides, Design Patterns.
coverage of the plug-in. The proof tactics are also under further            Elements of Reusable Object-Oriented Software., ser. Addison-Wesley
development in order to discharge increasingly complex goals.                Professional Computing Series. Addison-Wesley, 1995.
Moreover we wish to expose more of Isabelle’s native proof            [21]   S. Foster and J. Woodcock, “A Dwarf Signal in CML,” COMPASS
facilities in the TPP, such as sledgehammer and nitpick, so                  Whitepaper WP04, Tech. Rep., September 2013.
as to bring their full weight to bear in discharging or refuting      [22]   J. Holt, “Model-based Requirements Engineering for System of Sys-
                                                                             tems,” in Proc. 7th Intl. Conference on Systems of Systems Engineering
proof obligations. Parallel to this there is work to formalise               (SoSE). IEEE, July 2012.
the proof obligations in Isabelle with respect to the CML
                                                                      [23]   J. Bryans, J. Fitzgerald, R. Payne, and K. Kristensen, “SysML Contracts
semantics. Finally, we hope to produce guidance to the user                  for Systems of Systems,” June 2014, to appear in IEEE SoSE 2014.
of how to interpret failure when a PO cannot be discharged.           [24]   M. Clavel, F. Duán, S. Eker, P. Lincoln, N. Martı́-Oliet, J. Meseguer,
                                                                             and J. Quesada, “Maude: specification and programming in rewriting
                                                                             logic,” Theor. Comp. Sci., vol. 285, no. 2, pp. 187–243, 2002.
                    ACKNOWLEDGEMENTS
                                                                      [25]   A. Griesmayer, Z. Liu, C. Morisset, and S. Wang, “A framework for
   This work is supported by EU Framework 7 Integrated                       automated and certified refinement steps,” Innovations in Systems and
Project “Comprehensive Modelling for Advanced Systems of                     Software Engineering, vol. 9, no. 1, pp. 3–16, 2013.
