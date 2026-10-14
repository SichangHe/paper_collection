                                               Recomposition: A New Technique for Efficient
                                                       Compositional Verification
                                                          Ian Dardik                                    April Porter                              Eunsuk Kang
                                                 Carnegie Mellon University              University of Maryland, College Park             Carnegie Mellon University
                                                    Pittsburgh, PA, USA                        College Park, MD, USA                         Pittsburgh, PA, USA
                                                  idardik@andrew.cmu.edu                      aporter3@terpmail.umd.edu                    eunsukk@andrew.cmu.edu



                                            Abstract—Compositional verification algorithms are well-             the entire (monolithic) system directly without compositional
arXiv:2408.03488v2 [cs.FL] 15 Aug 2024




                                         studied in the context of model checking. Properly selecting            techniques. Our key insight that addresses this shortcom-
                                         components for verification is important for efficiency, yet has        ing is to recompose the components into new components
                                         received comparatively less attention. In this paper, we address
                                         this gap with a novel compositional verification framework that         D1 , . . . , Dm that we verify instead. For example, Fig. 1b
                                         focuses on component selection as an explicit, first-class concept.     shows D1 composed of C1 and C3 while D2 is composed
                                         The framework decomposes a system into components, which we             of C2 .
                                         then recompose into new components for efficient verification.             The choice of how to recompose is determined by a
                                         At the heart of our technique is the recomposition map that             recomposition map that maps Ci ’s to Dj ’s. Recomposition
                                         determines how recomposition is performed; the component
                                         selection problem thus reduces to finding a good recomposition          maps make component selection an explicit, first-class concept
                                         map. However, the space of possible recomposition maps can be           and lie at the heart of our technique. We will show that, in
                                         large. We therefore propose heuristics to find a small portfolio        practice, there often exists a recomposition map that results
                                         of recomposition maps, which we then run in parallel. We have           in a compositional verification problem that is more efficient
                                         implemented our techniques in a model checker for the TLA+              than verifying the monolithic specification directly.
                                         language. In our experiments, we show that our tool achieves
                                         competitive performance with TLC–a well-known model checker                Additionally, we will show that our method is conducive
                                         for TLA+ –on a benchmark suite of distributed protocols.                to specification reduction. Specification reduction techniques,
                                                                                                                 e.g. program slicing [20], [21], are generally considered sepa-
                                                                I. I NTRODUCTION                                 rately from compositional verification. However, model check-
                                            Model checking is an important tool for software, protocol,          ing with recomposition unites these two techniques under a
                                         and algorithm development. Compositional verification is a              single framework. For example, Fig. 1c shows a situation
                                         paradigm in which a system is decomposed into components,               in which a partial recomposition map is used to reduce a
                                         which are then verified using a divide-and-conquer algorithm.           specification with four-components to just the first three.
                                         To help model checking scale to large programs and specifi-                Ultimately, selecting components for efficient verification
                                         cations, compositional verification remains an important type           reduces to finding a suitable recomposition map. Therefore, we
                                         of technique for combating the state explosion problem [1].             propose a technique for automatically selecting recomposition
                                            Most research papers on compositional verification assume            maps. We use heuristics to prune the large space of possible
                                         that the components are pre-determined and focus solely on              recomposition maps, which results in a small portfolio of maps
                                         verification algorithms [2], [3], [4], [5], [6], [7], [8], [9], [10],   that we run in parallel.
                                         [11], [12], [13], [14], [15], [16]. However, component selec-              We have implemented our techniques in a model checker
                                         tion–that is, determining the set of decomposed components              called “Recomp-Verify” for the TLA+ language [22]. In order
                                         and the order in which they are verified–can greatly impact             to bring compositional verification to TLA+ , we additionally
                                         performance, in terms of both run time and state space size.            propose a novel parallel composition operator for the language.
                                         Yet there are comparatively fewer model checking frame-                 We evaluate our techniques by comparing Recomp-Verify to
                                         works that investigate component selection, e.g. by automating          TLC [23], a well-known model checker for TLA+ . We show
                                         decomposition [17], [18], [19]. Unfortunately, research into            that recomposition can lead to large savings in terms of
                                         automated decomposition has seen limited success thus far; as           verification time and the size of the explored state space.
                                         Cobleigh et al. lament, decomposing a system is tough [17].                In summary, we make the following contributions: (1) our
                                            In this paper, we propose a new safety verification approach         main contribution, recomposition, which is a technique for
                                         for symbolic specifications that is centered around component           efficient compositional verification, (2) an automated method
                                         selection. In our approach, we begin by decomposing a system            for finding efficient recomposition maps using paralleliza-
                                         S into components C1 , . . . , Cn . Traditionally, a compositional      tion and heuristics, (3) a definition for parallel composition
                                         verification algorithm is applied to these components to verify         for TLA+ specifications, and (4) a prototype model checker
                                         a system level property P , as shown in Fig. 1a. However,               Recomp-Verify that implements our algorithm, along with an
                                         verifying these components may be less efficient than verifying         evaluation of Recomp-Verify against TLC on a benchmark of
                                                                                                MODULE TwoPhase
                                                                         1     CONSTANT RMs
                                                                         2     VARIABLES msgs, rmState, tmState, tmPrepared
                                                                                     ∆
                                                                         3     vars = ⟨msgs, rmState, tmState, tmPrepared ⟩
                                                                                     ∆
                                                                         4     Init =
            (a) Traditional compositional verification.                  5        ∧ msgs = {}
                                                                         6        ∧ rmState = [rm ∈ RMs ↦→ “working”]
                                                                         7        ∧ tmState = “init”
                                                                         8        ∧ tmPrepared = {}
                                                                                                ∆
                                                                         9     RcvPrepare(rm) =
                                                                         10      ∧ [type ↦→ “Prepared”, theRM ↦→ rm] ∈ msgs
                                                                         11      ∧ tmState = “init”
                                                                         12      ∧ tmPrepared ′ = tmPrepared ∪ {rm}
                                                                         13      ∧ UNCHANGED ⟨msgs, tmState, rmState⟩
        (b) Compositional verification with recomposition.               14    SndPrepare(rm) =
                                                                                                ∆


                                                                         15      ∧ rmState[rm] = “working”
                                                                         16      ∧ msgs ′ = msgs ∪ {[type ↦→ “Prepared”, theRM ↦→ rm]}
                                                                         17      ∧ rmState ′ = [rmState EXCEPT ! [rm] = “prepared”]
                                                                         18      ∧ UNCHANGED ⟨tmState, tmPrepared ⟩
                                                                                     ∆
                                                                         19    Next =
                                                                         20       ∃ rm ∈ RMs :
                                                                         21          ∨ SndPrepare(rm)
                                                                         22          ∨ RcvPrepare(rm)
                                                                                          ..
     (c) Specification reduction in the recomposition method.            23                .
                                                                                     ∆
Fig. 1: Comparing traditional compositional verification                 24    Spec = Init ∧ □[Next]vars
against our recomposition method.
                                                                          Fig. 2: A monolithic encoding of the Two Phase Commit
                                                                          Protocol.
distributed protocols.
                 II. M OTIVATING E XAMPLE
                                                                          24 formally declares the STS with initial predicate Init and
   In this section, we describe the Two Phase Commit Protocol
                                                                          transition relation Next. We show two actions, SndPrepare
[24] to motivate our work and serve as a running example
                                                                          and RcvPrepare, on lines 14 and 9 respectively. In TLA+ ,
throughout the paper.
                                                                          actions are typically conjunctions of guards that specify when
   1) Protocol Description: In the Two Phase Commit Pro-
                                                                          an action is enabled (lines 10-11 and 15) as well as primed
tocol, a transaction manager (TM) attempts to commit a
                                                                          variable expressions that specify transitions (lines 12 and 16-
transaction onto a pool of resource managers (RMs) in two
                                                                          17). The UNCHANGED keyword on lines 13 and 18 indicate
phases. In the first phase, each RM starts in the working state
                                                                          the frame conditions.
as it attempts to commit the transaction. Any RM that can
commit a transaction sends a prepared message to the TM.                     The key safety property for the Two Phase Commit Protocol
In the second phase, if every RM is prepared, the TM will                 is the invariant Consistent. We can encode this invariant as
issue a commit message to each RM; otherwise the TM will                  the following TLA+ formula:
issue an abort message. The protocol assumes that the network                 ∀ rm1, rm2 ∈ RMs :
can reorder, but not lose, messages. The key safety property                  ¬(rmState[rm1] = “aborted” ∧ rmState[rm2] = “committed”)
is for each RM to remain consistent; i.e. no two RMs should
disagree as to whether a transaction was committed or aborted.               3) Model Checking TwoPhase: The TLC model checker
   2) TLA+ Encoding: In Fig. 2, we show only the first                    can prove that a given finite instance of TP satisfies the
(prepare) phase of the TwoPhase specification, which we will              property Consistent. A finite instance of a protocol substitutes
refer to as TP for brevity. TP is a parameterized protocol,               a finite value for each parameter, e.g. a finite set of resource
meaning that the set of RMs in the protocol is given as input.            managers for RMs in TP . TLC performs explicit state model
In the TP specification, the parameter is indicated on line 1             checking, meaning that it enumerates every possible state in
using the keyword CONSTANT.                                               the transition system. For nine resource managers, TLC is able
   TP defines a symbolic transition system (STS) over four                to prove TP is safe after generating over 10 million states
state variables, which are declared on line 2 in Fig. 2. The vari-        in nearly ten minutes. However, for ten resource managers,
able rmState is the state of each RM, the variables tmState               TLC fails to terminate in an hour after checking over 48
and tmPrepared hold the state of the TM, and msgs is the                  million states. In the following section, we will show how
set of messages each machine sends over the network. Line                 our approach can scale model checking TP to ten resource



                                                                     2
                                                                                      ∆
       MODULE RM                        MODULE Env              spec ::=Spec = Init ∧ □[Next]vars conj ::= ∧ expr | ∧ expr
VARIABLES rmState                VARIABLES msgs                                ∆                                     conj
                                                                 init ::=Init = conj
     ∆
Init =
                                       ∆
                                 Init = msgs = {}                               ∆                  disj ::= ∨ expr | ∨ expr
                                                                next ::=Next = ∃ x ∈ D : d isj                       disj
   ∧ rmState =                                     ∆
                                 SndPrepare(rm) =                          arbitrary TLA+                         ∆
                                                                                                    op ::=id (p) = conj
    [rm ∈ RMs ↦→ “working”]         ∧ msgs ′ = msgs ∪ {[type ↦→ expr ::=
                  ∆
                                                                             expression
SndPrepare(rm) =                     “Prepared”, theRM ↦→ rm]}
  ∧ rmState[rm] = “working”      RcvPrepare(rm) =
                                                   ∆

  ∧ rmState ′ =                                                               Fig. 4: Restricted TLA+ grammar for this paper.
                                   ∧ [type ↦→ “Prepared”,
   [rmState EXCEPT ! [rm] =           theRM ↦→ rm] ∈ msgs
    “prepared”]                    ∧ UNCHANGED ⟨msgs⟩
                                                                       be the set of reachable states in D. We define the parallel
       MODULE TM1                       MODULE TM2                     composition (∥) over LTSs in the usual way by synchronizing
VARIABLES tmState                VARIABLES tmPrepared                  on actions common to both alphabets and interleaving on all
     ∆                                 ∆
Init = tmState = “init”          Init = tmPrepared = {}                other actions [26].
                  ∆                                ∆
RcvPrepare(rm) =                 RcvPrepare(rm) =                         We define an action-based behavior σ as an infinite sequence
  ∧ tmState = “init”               ∧ tmPrepared ′ =                    of actions, i.e. σ ∈ Aω , and we let σi denote the i th action
  ∧ UNCHANGED ⟨tmState⟩             tmPrepared ∪ {rm}                  in σ. We denote the action-based semantics of an LTS D as
                                                                       a set of action-based behaviors JDKα ⊆ Aω . It is the case
                                                                       that σ ∈ JDKα if and only if there exists a sequence of states
Fig. 3: A decomposition of TP . Standard operators such as             q0 , q1 , . . . ∈ Q ω such that q0 ∈ I and, for each nonnegative
Spec, Next, vars, etc. are omitted for brevity.                        index i , either (1) σi ∈ αD and (qi , σi , qi+1 ) ∈ δ, or (2)
                                                                       σi ∈ / αD and qi = qi+1 . Condition (2) allows for stuttering,
                                                                       a concept which we will introduce in Sec. III-B.
managers.                                                                 There are two methods for encoding a safety property as an
   4) Compositional Verification and Recomposition: Con-               LTS. The first method is creating an error LTS that includes
sider the specifications RM , Env , TM1 , and TM2 shown in             an error state–which we refer to as the π state–that acts as a
Fig. 3. These specifications represent a decomposition of TP ;         sink for any action that causes a safety violation. The second
that is, TP is semantically equal to the parallel composition          method is creating a property LTS whose language defines
of the four specifications. We can generate a labeled transition       the safe behaviors; property LTSs must be deterministic and
system (LTS) for each of the four specifications in Fig. 3 and         must not include a π state. Any error LTS can be converted
then use compositional verification techniques to answer the           to a property LTS using steps two and three for assumption
original model checking problem. For ten resource managers,            generation (Sec. 3) in [25]. We define property satisfaction
this strategy enumerates a maximum of 261,002 states and               over property LTSs as follows: an LTS D satisfies a property
terminates in 1 minute and 32 seconds.                                 LTS P (D |= P) exactly when JDKα ⊆ JPKα . Note that
   Compositionally verifying the components above is more              our LTS semantics (with stuttering) properly handles alphabet
efficient than TLC, but we can use recomposition to do even            refinement, and therefore it is unnecessary to consider alphabet
better. Later, in example Ex. 2, we use recomposition to               restriction [26] in our definition of property satisfaction.
identify new components that are optimal in terms of minimum
run time for verification. In general, recomposition can provide       B. TLA+
large savings in terms of run time and state space. In Sec. VII,
                                                                          In this paper we will refer to a TLA+ specification S as
we show experimentally that recomposition can reduce a
                                                                       a syntactic entity that consists of constants, variables and
model checking problem by millions of states.
                                                                       operator definitions, etc. in the format shown in Fig. 2.
                      III. P RELIMINARIES                                 The initial state predicate, transition relation, and specifica-
   In this section we formally introduce labeled transition            tion declaration are named Init, Next, and Spec respectively.
systems (LTSs), the TLA+ language, and the compositional               In this paper, Init, Next, and Spec are restricted to the syntax
verification technique that we consider in this paper. Through-        of init, next, and spec given by the grammar in Fig. 4. In
out this paper, we will use calligraphic font when referring           next, the domain D does not contain state variables. We also
to LTS variables (e.g. D) and normal font when referring to            restrict action definitions to the syntax of op, and no actions
TLA+ specifications (e.g. S ).                                         are referenced in the body of another action. In the grammar,
                                                                       □ is the always temporal operator. Expression [Next]vars is
A. Labeled Transition Systems                                          equal to Next ∨(vars ′ = vars) and allows for stuttering states,
   A labeled transition system (LTS) D is a tuple (Q, αD, δ, I )       i.e. consecutive states whose variables in vars do not change.
where Q is the set of states, αD is the alphabet of D, δ ⊆                We define several operators over a TLA+ specification
Q × αD × Q is the transition relation, and I is a set of initial       S . The scoping operator ! references definitions in S , e.g.
states. αD must be a subset of A, where A is the universe of           TP !SndPrepare refers to the SndPrepare action of TP
all possible actions across all possible LTSs. We let Reach(D)         in Fig. 2. The operators α̂ and α denote symbolic actions



                                                                   3
and concrete actions respectively. Symbolic actions are the                      MODULE T1                   ∧ tmPrepared ′ =
action names in a specification, while concrete actions are              VARIABLES                            tmPrepared ∪ {rm}
the actions that may occur in a finite instance. For exam-                 msgs, tmState, tmPrepared         ∧ UNCHANGED
ple, let TP1 be the finite instance of TP with RM =                           ∆
                                                                         Init =                               ⟨msgs, tmState⟩
{“rm1”}, then α̂TP1 = α̂TP = {SndPrepare, RcvPrepare}                       ∧ msgs = {}
                                                                                                                  MODULE T2
and αTP1 = {SndPrepare(“rm1”), RcvPrepare(“rm1”)}.                          ∧ tmState = “init”
                                                                                                          VARIABLES
Additionally, we let β S denote the set of state vari-                      ∧ tmPrepared = {}
                                                                                           ∆
                                                                                                            tmState, tmPrepared
ables in a specification or an expression, e.g. β TP =                   SndPrepare(rm) =                       ∆
                                                                           ∧ msgs ′ = msgs ∪              Init =
{msgs, rmState, tmState, tmPrepared }. For an operator                                                       ∧ tmState = “init”
                                                                            {[type ↦→ “Prepared”,
∗ ∈ {α̂, α, β } and a set of specifications Z , the notation ∗Z is            theRM ↦→ rm]}                  ∧ tmPrepared = {}
short-hand for the union of ∗z , for each specification z ∈ Z .            ∧ UNCHANGED                    RcvPrepare(rm) =
                                                                                                                            ∆


   To define the semantics of a TLA+ formula, we first define               ⟨tmState, tmPrepared ⟩          ∧ tmState = “init”
a state as an assignment to all state variables. Then, the               RcvPrepare(rm) =
                                                                                           ∆                ∧ tmPrepared ′ =
                                                                                                             tmPrepared ∪ {rm}
semantics of a TLA+ formula is a set of behaviors, where                   ∧ [type ↦→ “Prepared”,
                                                                            theRM ↦→ rm] ∈ msgs             ∧ UNCHANGED ⟨tmState⟩
a behavior is an infinite sequence of states. We indicate state-
                                                                           ∧ tmState = “init”
based semantics of a TLA+ formula F as JF Kβ , the set of
behaviors that satisfy F . For a TLA+ specification S , we will
often abbreviate JS !SpecKβ to simply JS Kβ . Given a TLA+               Fig. 5: Intermediate decomposed specifications T1 and T2 in
property P , we say S satisfies P (S |= P ) exactly when                 the TP example.
JS Kβ ⊆ JP Kβ .
   We define the operator LTS(S ), which converts a TLA+
specification S into an LTS D. LTS(S ) can be realized by                concepts such as decomposition and recomposition in Sec. V.
generating the full state graph for S and then labeling its              The new operator is syntactic; in other words, the definition is
edges with the concrete actions αS such that αD = αS .                   entirely in terms of TLA+ syntax, and does not involve explic-
Additionally, we define two operators for converting TLA+                itly enumerating the state space. To avoid confusion between
properties to an LTS. The first operator, ERR(S , P ), constructs        the parallel composition operator ∥ over LTSs (Sec. III-A), we
an error LTS for S where violations of P lead to a π state.              will denote the TLA+ parallel composition operator using //.
The second operator, PROP(S , P ), builds a property LTS for             We will use the notation //Z to denote the composition over
S where no violation of P is possible. PROP(S , P ) can be               a set of specifications Z . We now define // in the usual way,
constructed from ERR(S , P ), as pointed out in Sec. III-A.              by synchronizing common actions between specifications and
                                                                         interleaving all others actions [26].
C. CRA-Style Compositional Verification
                                                                         Definition 1 (Parallel Composition). Let S and T be TLA+
   In this paper, we consider a style of compositional verifica-         specifications with distinct state variables. We define S //T as
tion called compositional reachability analysis (CRA) [4], [8],          follows. First, S //T contains exactly the constants and state
[27]. Our recomposition framework requires a compositional               variables in S and T . Second, in S // T , we define vars ≜
verification algorithm that works for multiple components,               (S !vars) ◦ (T !vars), where ◦ is the sequence concatenation
and CRA-style techniques have reported success for verifying             operator. Finally, in S//T , we define Spec ≜ Init ∧ [Next]vars
safety properties of multi-component systems [6].                        where Init ≜ S !Init ∧ T !Init and Next is defined as follows:
   CRA is used to check safety by composing the LTS for                                ⎧
                                                                                           ∃d ∈ D : S !A(d ) ∧ T !A(d )
each component together in a hierarchical fashion; safety                              ⎪
                                                                                       ⎪
                                                                                              if A ∈ α̂S and A ∈ α̂T
                                                                                       ⎪
                                                                                       ⎪
is proved if and only if the π state is unreachable in the                             ⎪
                                                                                           ∃d ∈ D : S !A(d ) ∧ T !vars ′ = T !vars
                                                                                       ⎪
                                                                                       ⎨
                                                                               ⋁︂
overall system. Such algorithms generally derive their divide-
                                                                                              if A ∈ α̂S and A ∈  / α̂T
and-conquer efficiency from two optimizations: intermediate               A ∈ α̂S ∪α̂T ⎪
                                                                                       ⎪
                                                                                           ∃d   ∈ D   : T !A(d )  ∧ S !vars ′ = S !vars
                                                                                       ⎪
                                                                                       ⎪
minimization and short-circuiting. The former involves mini-                           ⎪
                                                                                       ⎪
                                                                                              if A ∈
                                                                                                   / α̂S and A ∈ α̂T
                                                                                       ⎩
mizing the state space of the intermediate LTSs with respect to
observational equivalence [28] during composition. The latter               Notice that Def. 1 defines parallel composition in terms of
optimization, short-circuiting, occurs when a strict subset of           TLA+ syntax, and hence does not increase the expressivity of
components are needed for verification to succeed. In this case,         the language. While the operator itself is novel, this technique
the remaining components (outside the strict subset) can be              is briefly discussed by Lamport [22].
skipped, and hence short-circuiting provides a dynamic form
                                                                         Example 1. By Def. 1, TP = RM // Env // TM1 // TM2 .
of specification reduction.
                                                                         Furthermore, consider specifications T1 and T2 from Fig. 5.
           IV. PARALLEL C OMPOSITION IN TLA +                            Notice that TP = RM // T1 , T1 = Env // T2 , and T2 =
                                                                         TM1 //TM2 .
  In this section, we introduce a new parallel composition
operator over TLA+ specifications. The operator is central                 The following theorem shows that parallel composition
to our recomposition algorithm and will allow us to define               behaves exactly as we expect if we convert a TLA+ speci-



                                                                     4
fication to an LTS. We prove this theorem using more general                 Algorithm 1 R ECOMP -V ERIFY
semantics for TLA+ specifications, namely action-state-based                 Input: Specification S , property P , recomposition strategy ρ
semantics. We include a proof in Appendix A.                                 Output: If S |= P
                                                                              1: C1 , . . . , Cn = D ECOMPOSE (S , P )
Theorem 1. JLTS(S //T )Kα = JLTS(S ) ∥ LTS(T )Kα .
                                                                              2: f , m ← ρ(C1 , . . . , Cn )
       V. M ODEL C HECKING WITH R ECOMPOSITION                                3: f , m ← S TATIC -R EDUCE(f , m)
   In this section, we propose our algorithm for verifying sym-               4: DP ← //f −1 (dP )              ▷ f −1 (dP ) ⊆ {C1 , . . . , Cn }
bolic specifications. We begin by introducing the algorithm in                5: for j ∈ {1, . . . , m} do
Sec. V-A. Subsequently, we provide details for decomposition                  6:      Dj ← //f −1 (dj )          ▷ f −1 (dj ) ⊆ {C2 , . . . , Cn }
(Sec. V-B), static specification reduction (Sec. V-C), and                    7: return C OMP -V ERIFY (D1 , . . . , Dm , DP , P )
compositional verification (Sec. V-D). Finally, we conclude
this section with a correctness analysis of the algorithm in
Sec. V-E.                                                                       Alg. 1 begins by decomposing S into components on line
A. The Recomp-Verify Algorithm                                               1. The strategy ρ selects a recomposition map on line 2, which
                                                                             is possibly statically reduced on line 3. We provide more
   1) Algorithm Overview: Our algorithm solves a model
                                                                             detail for decomposition and static specification reduction in
checking problem S |= P , where S and P are both writ-
                                                                             Sec. V-B and Sec. V-C respectively. Next, on lines 4-6, we
ten in TLA+ . The algorithm begins by decomposing S into
                                                                             perform recomposition using the recomposition map f . On
n components C1 , . . . , Cn , each of which is also a TLA+
                                                                             line 4, we define DP to be the parallel composition of each
specification. The decomposition algorithm ensures two key
                                                                             Ci component in the pre-image f −1 (dP ). Similarly, on line
properties upon termination: (P1) S = C1 // · · · // Cn and
                                                                             6, we define each Dj to be the parallel composition of each
(P2) the first component, C1 , contains all state variables that
                                                                             Ci component in the pre-image f −1 (dj ). Finally, on line
occur syntactically in P . Property (P1) ensures soundness of
                                                                             7, we solve the compositional verification problem for the
the decomposition, while property (P2) allows us to build the
                                                                             recomposed components (Dj ’s); we provide more detail for
safety property P described in the following paragraph.
                                                                             this step in Sec. V-D.
   After decomposition, the algorithm recomposes the Ci com-
ponents into new components DP and D1 , . . . , Dm . These new               Example 2. In this example we analyze Alg. 1 given the input
components define the following compositional verification                   TP , Consistent, and a hand-crafted optimal recomposition
problem that is equivalent to the original: LTS(D1 ) ∥ . . . ∥               strategy ρopt . Line 1 of Alg. 1 produces the components
LTS (Dm ) |= P, where P = PROP (DP , P ). For PROP (DP , P )                 RM , Env , TM1 , and TM2 from Fig. 3. On line 2, ρopt
to be well-formed, DP must contain every state variable that                 chooses m = 2 and f such that f (RM ) = dP , f (Env ) =
occurs in P . Therefore, we require DP to be composed of (at                 f (TM1 ) = d1 , and f (TM2 ) = d2 . Static specification
least) C1 , as C1 must contain every state variable that occurs              reduction on line 3 has no effect on f and m. Recomposition
in P by property (P2) of decomposition. We formally capture                  (lines 4-6) reduces the original model checking problem to
this requirement, as well as the choice of how to perform                    LTS (Env // TM1 ) ∥ LTS (TM2 ) |= PROP (RM , Consistent),
recomposition, in the following definition.                                  which we solve on line 7. Whereas the example in Sec. II
                                                                             verifies four specifications (for RM , Env , TM1 , TM2 ), this
Definition 2 (Recomposition Map). A recomposition map is
                                                                             example verifies three (for RM , Env // TM1 , TM2 ). The
a surjective function f : {C1 , . . . , Cn } → {dP , d1 , . . . , dm }
                                                                             strategy ρopt in this example reduces the maximum state space
such that f (C1 ) = dP .
                                                                             by 1,027 states and improves the model checking time from
   In Def. 2, the dj ’s in the co-domain are intended as a place-            1 minute 32 seconds to 51 seconds.
holder for constructing each Dj . In particular, we will define
each recomposed component as Dj = //f −1 (dj ), the parallel                 B. Decomposition
composition of one or more Ci components. Therefore, the                        In this section, we present an algorithm for decomposing a
restriction f (C1 ) = dP implies that DP will be composed of                 symbolic specification S into n components C1 . . . Cn . Our
C1 as intended. Finally, once each Dj is constructed, we solve               algorithm guarantees the following two properties: (P1) S =
the compositional verification problem.                                      C1 //· · ·//Cn and (P2) β P ⊆ β C1 . We provide a correctness
   2) Algorithm Details: We present our model checking                       argument for these two properties in Sec. V-E.
algorithm in Alg. 1. The algorithm accepts several inputs,                      1) Decomposition Algorithm: Each step of the algorithm
including a recomposition strategy. A recomposition strategy                 splits a specification Ti into two specifications Ci+1 and Ti+1
ρ is a function that maps Ci components to a pair (f , m),                   such that Ti = Ci+1 // Ti+1 . We note the following two
where f is a total recomposition map and m is the number                     corner cases: T0 = S and Cn = Tn−1 . The algorithm splits a
of Dj components. In other words, the recomposition strategy                 specification across two phases: state variable partitioning and
determines which recomposition map is used. In the remainder                 specification slicing. The former partitions the state variables
of this section we assume ρ is given; we discuss recomposition               of Ti into two sets VC and VT , while the latter slices Ti
strategy selection in Sec. VI.                                               into Ci+1 and Ti+1 that contain the variables VC and VT



                                                                         5
respectively. We present the algorithm in Alg. 2. We now               state variables in each partition will constitute a well-formed
explain state variable partitioning and specification slicing in       slice according to the grammar in Fig. 4. For example, if
detail across the following two sections.                              a specification contains the expression a = b + 1, then a
                                                                       and b should be grouped together into the same partition.
Example 3. We explain Alg. 2 given TP and Consistent.
                                                                       To accomplish this, we let VC be V plus any variables that
The algorithm begins with the partition VC = {rmState} and
                                                                       occur within the same expression, repeated until fix-point.
VT = {msgs, rmState, rmPrepared } on line 1; we explain
                                                                       More formally, we let VC = F IX(O CCURSS , V ) (line 14),
partitioning in Sec. V-B2. Next, on lines 6-7, the algorithm
                                                                       where F IX invokes the O CCURSS procedure, initially on V ,
slices TP into RM (Fig. 3) and T1 (Fig. 5). The state variables
                                                                       until a fix-point is reached. Finally, we choose VT to be the
of T1 are subsequently partitioned into VC = {msgs} and
                                                                       remainder of the state variables in Ti (line 15).
VT = {rmState, rmPrepared } on line 9. The algorithm
continues in this fashion until VT = ∅, i.e. no partition is           Example 4. Notice that β Consistent = {rmState} and
possible. The algorithm will then exit the loop and return the         F IX(O CCURSTP , {rmState}) = {rmState}. Therefore, the
components RM , Env , TM1 , TM2 on line 12.                            first partition (line 1) will be VC = {rmState} and VT =
                                                                       {msgs, tmState, tmPrepared }. In the second partition (lines
                                                                       8-9), we arbitrarily choose v = msgs, which results in
Algorithm 2 D ECOMPOSE
                                                                       VC = {msgs} and VT = {tmState, tmPrepared }.
Input: Specification S , Safety Property P
Output: C1 , . . . , Cn with properties (P1) and (P2)                     3) Specification Slicing: The specification slicing phase
 1: VC , VT ← PARTITION (S , β P )                                     restricts a specification Ti to a given subset of its variables
 2: if VT = ∅ then                                                     V . Slicing can be seen as the inverse of parallel composition.
 3:     return S                                                       For example, consider a system specification M with action
 4: T0 ← S , i ← 0                                                     Action and state variables var1 and var2 :
                                                                                                 ∆
 5: while VT ̸= ∅ do                                                                    Action = ∧ var1 ′ = “val1”
 6:     Ci+1 ← S LICE(Ti , VC )                                                                  ∧ var2 ′ = “val2”
 7:     Ti+1 ← S LICE(Ti , VT )
                                                                       Given the variable partition {var1 }, {var2 }, we can
 8:     v ∈ β Ti+1 ▷ Nondeterministically choose a variable
                                                                       view M as the composition of two components M1 and
 9:     VC , VT ← PARTITION(Ti+1 , {v })                                                                         ∆
                                                                       M2 that respectively define: Action = var1 ′ = “val1” and
10:     i ←i +1                                                                  ∆      ′
                                                                       Action = var2 = “val2”. In particular, we have M1 =
11: n ← i + 1, Cn ← Ti
                                                                       S LICE(M , {var1 }), M2 = S LICE(M , {var2 }), and M = M1//
12: return C1 , . . . , Cn
                                                                       M2 . In the TP example, this corresponds to TP = RM //T1
13: procedure PARTITION (T , V )
                                                                       in Ex. 3. We include more details on slicing, including the
14:     VC ← F IX(O CCURST , V )
                                                                       definition for the slicing procedure, in Appendix B.
15:     VT ← β S − VC
16:     return VC , VT                                                 C. Static Specification Reduction
17: procedure O CCURS S (V )                                              In Sec. V-A, we require recomposition strategies to produce
                     ⋃︁
18:     return            {β c | c ∈ Conj(A) and β c ∩ V ̸= ∅}         a total recomposition map. Total recomposition maps apply
                A ∈ α̂S                                                verification to every component; however, in some cases, not
19: procedure F IX (op, X )                                            every component is necessary for verification. Therefore, in
20:     Y ← X ∪ op(X )                                                 the following paragraph, we introduce a technique for stati-
21:     if X = Y then return X                                         cally detecting a subset of components that are necessary for
22:     return Y ∪ F IX(op, Y )                                        verification. In Alg. 1, the procedure S TATIC -R EDUCE(f , m)
                                                                       on line 3 restricts the domain of f to this subset and reduces
                                                                       the codomain and m accordingly so f remains surjective.
   2) State Variable Partitioning: Given a specification Ti ,
                                                                          The subset of necessary components is those whose alpha-
the partitioning phase partitions the variables β Ti into two
                                                                       bets may affect–either directly or indirectly–the actions of C1 ,
sets VC and VT . The partition procedure appears twice in
                                                                       and therefore may prevent the entire system from reaching
Alg. 2. The first occurrence, on line 1, determines the state                                                                   ⋃︁
                                                                       an error. More formally, the subset of components is i Xi ,
variables that will appear in C1 ; therefore, to uphold property
                                                                       where X0 = {C1 } and Xi+1 = {Cj | α̂Cj ∩ α̂Xi ̸= ∅}. In
(P2), we partition on β P . In the second appearance, on line 9,
                                                                       Appendix C, we show that it is only necessary to consider the
we choose just one variable in attempt to produce as many
                                                                       first n + 1 terms–where n is the number of Ci components–
components as possible (ideally, one component per state
                                                                       when computing the union of the Xi ’s. Intuitively, X1 is the
variable). We are free to choose the one variable nondeter-
                                                                       set of components that may directly prevent C1 from reaching
ministically because the order of decomposed components is
                                                                       an error, while X2 , X3 , etc. may indirectly prevent an error.
inconsequential; this is due to the fact that the ordering is
ultimately determined by a recomposition map in Alg. 1.                Example 5. We now introduce TPCounter , an extension to
   The partition procedure in Alg. 2 also guarantees that the          TP . TPCounter is identical to TP , except it includes one



                                                                   6
more state variable counter and one more action Increment.             Algorithm 3 C OMP -V ERIFY
In the initial state, counter is equal to zero. Each original          Input: D1 , . . . , Dm , DP , P
action from TP leaves counter unchanged, while Increment               Output: If LTS(D1 ) ∥ . . . ∥ LTS(Dm ) |= P
increments counter by one and leaves all other state variables          1: D ← Min( ERR (DP , P ))               ▷ P = ERR(DP , P )
unchanged. The Increment action is always enabled, and                  2: if π ∈/ Reach(D) then
therefore TPCounter is an infinite-state protocol.                      3:     return true
   Consider model checking TPCounter |= Consistent with                 4: for j ∈ {1, . . . , m} do
Alg. 1. Decomposition (line 1) produces five components:                5:     D ← D ∥ Min(LTS(Dj ))
RM , Env , TM1 , TM2 , and Counter , where Counter has one              6:     if π ∈
                                                                                    / Reach(D) then
state variable counter and one action Increment. Counter                7:         return true
is the only specification with the action Increment and,                8: return false
therefore, does not synchronize with the actions in the other
four specifications. Therefore, Counter cannot affect the
safety of C1 . Formally, X0 = {RM }, X1 = {RM , Env },                 problem to compositional verification is correct (Lem. 4).
X2 = {RM , Env , TM1 , TM2 }, X3 = X2 , etc. so Counter is             Finally, we present Thm. 2 that shows that Alg. 1 is sound.
not a necessary component. S TATIC -R EDUCE will therefore
omit Counter from the domain of any given recomposition                Lemma 1. Algorithm 2 ensures (P1) S = C1 //· · ·//Cn and
map, causing Alg. 1 to successfully terminate.                         (P2) β C1 ⊆ β P upon termination.
                                                                       Proof. Sketch. We prove property (P1) by establishing the fol-
D. Compositional Verification                                          lowing loop invariant in Alg. 2 on line 5: S = C1//· · ·//Ci//Ti .
   We present a CRA-style compositional verification algo-             The proof for property (P2) follows in two steps. First,
rithm in Alg. 3. The algorithm works by iteratively composing          β P ⊆ VC because VC (in the first partition) is defined by
the LTS for each component Dj together (line 5) until the π            a monotonically increasing operation (F IX) on β P . Second,
state becomes unreachable, in which case verification succeeds         β P ⊆ β C1 because C1 = S LICE (S , VC ) will contain exactly
(lines 3 and 7). If the π state remains reachable by the end           the state variables in VC .
of the algorithm, however, then we report a failure (line                                                    ⋃︁
                                                                       Lemma 2. S |= P if and only if //( i Xi ) |= P .
8). The algorithm performs intermediate minimization on
lines 1 and 5. In general, there are many options for which            Proof. We prove this theorem in Appendix C.
components–or composition of components–to minimize [12].
                                                                       Lemma 3. LTS(D1 ) ∥ . . . ∥ LTS(Dm ) |= P if and only if there
We choose to only minimize components because we observed
                                                                       exists a k ∈ {0 . . . m} such that π ∈
                                                                                                            / Reach(ERR(DP , P ) ∥
that minimizing the composition of components was generally
                                                                       LTS(D1 ) ∥ . . . ∥ LTS (Dk )).
slow. In essence, this algorithm is an abstraction-refinement
loop where each new component lowers the abstraction by                Proof. Sketch. The forwards case (⇒) follows by choosing
introducing more state variables.                                      k = m. For the backwards case (⇐), we assume that k is
                                                                       given such that 0 ≤ k ≤ m and π ∈     / Reach(ERR(DP , P ) ∥
Example 6. Consider TP with ten resource managers and the
                                                                       LTS(D1 ) ∥ . . . ∥ LTS (Dk )). Notice that, by construction,
optimal mapping f from Ex. 2, where DP = RM , D1 = Env//
                                                                       none of LTS(Dk +1 ), . . . , LTS(Dm ) contains a π state, and
TM1 , and D2 = TM2 . Line 1 of Alg. 3 will generate an LTS
                                                                       therefore neither will Reach(ERR(DP , P ) ∥ LTS(D1 ) ∥ . . . ∥
for DP with 477,454 states, including a π state. Minimization
                                                                       LTS(Dm )).
reduces DP to 13,291 states. Due to a reachable π state, the
algorithm proceeds into the loop on line 4. Next, on line 5, the       Lemma 4. S |= P ⇐⇒ LTS(D1 ) ∥ . . . ∥ LTS(Dm ) |= P.
algorithm generates an LTS for D1 with 3,072 states, which
reduces to 1,026 states after minimization. Composing this             Proof.
LTS with D (line 5) retains the π state (line 6) so we loop                     S |= P                                               (1)
again. The algorithm continues in this fashion until a π state            ⇐⇒ π ∈ Reach(ERR(S , P ))                                  (2)
is no longer reachable, and we return a positive answer (line 6           ⇐⇒ π ∈ Reach(ERR(C1 //· · ·//Cn , P ))                     (3)
and 7). A maximum of 481,550 states are needed in memory
                                                                          ⇐⇒ π ∈ Reach(ERR(DP //D1 //· · ·//Dm , P ))                (4)
at once.
                                                                          ⇐⇒ π ∈ Reach(ERR(DP , P ) ∥ . . . ∥ ERR(Dm , P ))          (5)
                                                                          ⇐⇒ π ∈ Reach(ERR(DP , P ) ∥ . . . ∥ LTS(Dm ))              (6)
E. Correctness Analysis
                                                                          ⇐⇒ LTS(D1 ) ∥ . . . ∥ LTS(Dm ) |= PROP(DP , P )            (7)
   In this section, we show that Alg. 1 is sound but not
complete. To establish this result, we first provide lemmas for        Biconditional (2) holds because P is a safety property, (3)
the correctness of decomposition (Lem. 1), static specification        by Lem. 1 property (P1), (4) by the definition for each Dj
reduction (Lem. 2), and compositional verification (Lem. 3).           (and Lem. 2 in the case that f is partial), (5) by Thm. 1, (6)
Next, we show that reducing the monolithic model checking              by Lem. 1 property (P2) and Def. 2 (f (C1 ) = dP ), and (7)



                                                                   7
                                                                                           ⋃︁
because P is a safety property. Finally, the theorem follows             Finally, let F = i Fi ; we define the data flow partial order
because P = PROP(DP , P ).                                               ≼ to be the reflexive transitive closure of F . In Appendix D,
                                                                         we show formally that the partial order refines the static
Theorem 2. If Alg 1 terminates, then it returns true (model
                                                                         specification reduction scheme from Sec. V-C.
checking succeeds) if and only if S |= P .
                                                                         Example 7. For TP and Consistent, E0 = {RM },
Proof. The result follows from Lem. 3 and Lem. 4.
                                                                         E1 = {Env }, and E2 = {TM1 , TM2 }. Moreover, F =
   While Thm. 2 shows that Alg. 1 is sound, the algorithm                {(RM , Env ), (Env , TM1 ), (Env , TM2 )} and the data flow
is not complete, even if we limit S to be a finite-state                 partial order is the reflexive transitive closure of this set.
specification. This is because a given component Dj may                  Intuitively, the partial order shows that TM1 and TM2 can
be infinite-state, in which case LTS construction will fail to           only affect the variables in RM –i.e. the variables β Consistent
terminate on line 1 or 5 in Alg. 3. We address this limitation           needed for verification–indirectly by interacting with the Env
in Sec. VI-B by using a portfolio of strategies that includes            component.
the monolithic strategy.
                                                                            To further reduce the search space of maps, we extend the
     VI. C HOOSING E FFICIENT R ECOMPOSITION M APS                       data flow partial order to a total order ⩽ , i.e. ≼⊆⩽ . We
   In this section, we address the problem of designing re-              build the total order by breaking ties between incomparable
composition strategies, i.e. choosing efficient recomposition            components Ci and Cj by requiring Ci ⩽ Cj if and only if
maps. Rather than finding a single recomposition strategy, we            Ci ’s state variables have fewer syntactic appearances than Cj ’s
propose running Alg. 1 with a portfolio of strategies in parallel.       in the original specification S . In the case that the variables
The primary challenge is determining which strategies to use,            of Ci and Cj have the same number of appearances in S , we
since the number of possible recomposition maps grows large              break the tie arbitrarily.
as the number of components increases. We therefore propose
                                                                         B. Choosing a Portfolio of Strategies
a heuristic for pruning the search space of recomposition maps
in Sec. VI-A. We then choose a small portfolio of strategies                In this section, we describe four recomposition strategies
based on this heuristic in Sec. VI-B.                                    that comprise our portfolio. For simplicity, we describe the
                                                                         strategies assuming that the components C1 , . . . , Cn have
A. Recomposition Map Reduction Heuristic
                                                                         been reordered according to the total order ⩽ described in
   Any heuristic for pruning the search space of recomposition           Sec. VI-A. The four strategies are (S1) the identity strategy,
maps should be tailored to the compositional verification                in which m = n − 1 and f (Ci ) = di for all i , (S2) a “bottom
algorithm being used. Since we use a CRA-style verification              heavy” strategy in which we choose m = 1 and f such that
algorithm, we design our heuristic to find component orderings           f (C1 ) = dP and f (Ci ) = d1 for all i > 1, (S3) a “top
that can take advantage of short-circuiting. In particular, the          heavy” strategy in which we choose m = 1 and f such that
heuristic identifies recomposition maps that order Dj compo-             f (Cn ) = d1 and f (Ci ) = dP for all i < n, and (S4) the
nents that are least likely to be necessary for verification last.       monolithic strategy, where m = 0 and f (Ci ) = dP for all i .
   Our heuristic is to choose recomposition maps that respect
the data flow partial order ≼ over the Ci components. This is a          Example 8. In TP , the state variables of TM2 occur fewer
novel partial order that attempts to find dynamic specification          times than the variables of TM1 . Therefore, the total ordering
reduction–i.e. short-circuiting–by refining our static specifica-        from Sec. VI-A is: RM , Env , TM2 , TM1 . Then:
tion reduction scheme. Intuitively, the partial order will order            1) In the identity strategy, m = 3, f (RM ) = dP ,
the components based on how far removed their state variables                  f (Env ) = d1 , f (TM2 ) = d2 , and f (TM1 ) = d3 .
are from impacting verification.                                            2) In the bottom heavy strategy, m = 1, f (RM ) = dP ,
   More formally, we compute the data flow partial order based                 and f (Env ) = f (TM2 ) = f (TM1 ) = d1 .
on the indexed sets Xi introduced in Sec. V-C. These sets                   3) In the top heavy strategy, m = 1, f (RM ) = f (Env ) =
cumulatively capture the components that may interact–either                   f (TM2 ) = dP , and f (TM1 ) = d1 .
directly or indirectly–with the actions of C1 . First, we build             4) In the monolithic strategy, m = 0 and f (RM ) =
new indexed sets Ei defined as E0 = X0 and Ei+1 = Xi+1 \                       f (Env ) = f (TM2 ) = f (TM1 ) = dP .
Xi . While the Xi ’s are cumulative, each Ei captures only the
                                                                            As a note regarding the correctness analysis from Sec. V-E,
additional components in each Xi . Intuitively, the components
                                                                         including the monolithic strategy in the portfolio ensures
in Ei are i steps removed from affecting the variables in C1 ,
                                                                         termination. Therefore, our parallel approach is complete for
and hence i steps removed from impacting verification (by
                                                                         finite state specifications S .
property (P2) of decomposition).
   Second, we build indexed sets Fi that capture the data flow                          VII. E XPERIMENTAL R ESULTS
from each component in Ei to the components in Ei+1 . We                 A. Implementation
define F0 = ∅ and:
                {︃          ⃓                           }︃                  We have created a model checker called Recomp-Verify that
                            ⃓ Cj ∈ Ei and Ck ∈ Ei+1
        Fi+1 = (Cj , Ck ) ⃓⃓                                             can verify safety for TLA+ specifications. The model checker
                                and α̂Cj ∩ α̂Ck ̸= ∅                     is a prototype research tool that implements Alg. 1 in the



                                                                     8
Python, Java, and Kotlin programming languages. The model                   In terms of verification speed, Recomp-Verify1 and TLC1
checker also supports running multiple instances of Alg. 1               both outperform each other in fourteen benchmarks, and
in parallel, and returns the first result to finish. Our tool is         tie in five cases. However, Recomp-Verify1 completes more
available in a public repository [29].                                   benchmarks, verifying twenty-nine benchmarks while TLC1
                                                                         verifies twenty-four. Generally speaking, Recomp-Verify1 is
B. Experiments                                                           more performant on larger benchmarks; on benchmarks with
   We evaluate Recomp-Verify against TLC on a benchmark                  over a million states, TLC1 is faster in two cases while
of distributed protocols [30], plus the tla-twophase-counter             Recomp-Verify1 is faster in at least six cases. We therefore
protocol that we introduce in Ex. 5. Our evaluation is driven            answer RQ1 by concluding that hand-crafted maps can provide
by two research questions. First, (RQ1) can hand-written                 more efficiency than TLC.
recomposition maps provide more efficient verification than                 2) RQ2: The results for TLC4 and Recomp-Verify4 are
TLC? If this is the case, we then ask whether our technique is           similar to the single threaded versions. In terms of state space,
still performant when automating the search for recomposition            Recomp-Verify4 always enumerates the same number of (or
maps. More precisely, (RQ2) is the performance of Recomp-                fewer) states than TLC4 , and also exhibits large savings in
Verify (using a parallel, portfolio strategy) competitive with           the millions for six benchmarks. We note that Recomp-Verify4
TLC when each tool is allotted four threads?                             short-circuited every time that Recomp-Verify1 short-circuited,
   In our experiments, we use TLC1 and TLC4 to respectively              which showcases the effectiveness of the data flow heuristic
denote TLC run with one and four parallel threads; this is               from Sec. VI-A.
a built-in option for the tool. Recomp-Verify1 is the version               In terms of verification speed, Recomp-Verify4 is faster
of our tool with one thread and hand-crafted maps, while                 for eleven benchmarks, TLC4 is faster for fourteen, and the
Recomp-Verify4 denotes the version that uses four threads                tools tie for eight benchmarks. However, Recomp-Verify4
to run the portfolio of recomposition strategies (S1-4) from             verifies more benchmarks, completing thirty-two, while TLC4
Sec. VI in parallel. We report the fastest strategy for Recomp-          completes twenty-four. While threading made TLC faster for
Verify4 in the “Strat.” column in Fig. 6. Additionally, in the im-       the smaller benchmarks, it did not help the tool verify more
plementation of Recomp-Verify4 , we use TLC1 for running the             benchmarks. On the other hand, threading helped Recomp-
monolithic strategy (S4), since TLC is far more efficient than           Verify to verify three more benchmarks. Generally speaking,
our research prototype for monolithic model checking. For                Recomp-Verify4 outperforms TLC4 for large benchmarks and
example, in ex-quorum-leader-election-6 in Fig. 6, Recomp-               is competitive with TLC4 for smaller ones, and therefore we
Verify1 uses an optimal single-threaded strategy, yet is slower          answer RQ2 in the affirmative.
than TLC1 –and therefore Recomp-Verify4 too.                                3) Discussion: In Fig. 6, the Strat. column shows that the
   Every experiment in this paper was run on an Apple                    winning strategy for Recomp-Verify4 varies depending on the
MacBook Pro with 32GB of memory and an M1 processor. For                 given benchmark. This observation suggests that using a port-
each benchmark, we report the total run time using the Unix              folio of strategies may be necessary for efficient verification.
time utility as well as the maximum number of states checked.            Notably, among the benchmark problems, we found that the
We use TO to indicate a timeout after ten minutes and OM                 bottom heavy strategy (S2) did not perform well. Most likely,
to indicate a program crash due to reaching the memory limit             this is because the second component in this strategy is too
given a 25GB allotment. For TLC’s maximum state count,                   large, and therefore misses opportunities for short-circuiting.
we use the number of unique states that the tool reports. For               Ultimately, Recomp-Verify tends to be faster than TLC on
Recomp-Verify, we use the maximum between (1) the number                 benchmarks that have more opportunity for recomposition. We
of unique states generated for each component and, for each              point out that Recomp-Verify1 is faster than TLC1 in every
iteration, (2) the number of states that results from composition        case where decomposition produced at least four components
in Alg. 3 on line 5. For Recomp-Verify1 , we also report the             (n ≥ 4). The same is true for Recomp-Verify4 and TLC4 in all
number of components that result from decomposition (n), the             but one case. This observation suggests that the potential ben-
number of recomposed components (m), and the number of                   efits of recomposition increase with the number of available
recomposed components that were checked (k ).                            components (n).
C. Results and Discussion                                                                   VIII. R ELATED W ORK
   1) RQ1: We show our results in Fig. 6. In terms of state                Compositional verification is a well studied research area.
space, TLC1 enumerates at least as many states as Recomp-                Two widely studied styles of compositional verification are
Verify1 in every case. For six of the benchmarks that both               CRA [4], [5], [6], [8], [31], [12], [13], [14], [15], [16] and
tools verified, recomposition reduced the state size by millions         assume-guarantee reasoning [2], [3], [7], [17], [9], [32], [18],
of states. Moreover, Recomp-Verify1 short-circuits (k < m)               [19], [10], [11], [33], although other styles exist as well [34],
for eight benchmarks, each of which has a significantly                  [35]. Of these works, the ones most closely related to this
smaller state space than TLC1 . Finally, Recomp-Verify1 –but             paper automate decomposition for verification. Metzler et a.
not TLC1 –was able to verify the one infinite state benchmark            [18] and Cobleigh et al. [17] decompose systems into two
(tla-twophase-counter) via static specification reduction.               components, after which they apply L∗ style learning [36] to



                                                                     9
                                             Recomp-Verify1                  TLC1                Recomp-Verify4              TLC4
 Name                                n   m    k     States   Time         States   Time        States   Time Strat.        States  Time
 tla-consensus-3                     1   0    0          4      1s             4      1s            4      1s   S4              4     1s
 tla-tcommit-3                       1   0    0        34       1s            34      1s          34       1s   S4            34      1s
 i4-lock-server-2-2                  1   0    0          9      1s             9      1s            9      1s   S4              9     1s
 ex-quorum-leader-election-6         2   1    1 117,671       39s       121,111       4s     121,111       5s   S4       121,111      2s
 pyv-toy-consensus-forall-6-6        3   1    1 117,671       33s       121,111       4s     121,111       5s   S4       121,111      2s
 tla-simple-5                        1   0    0       723       1s          723       1s         723       1s   S4           723      1s
 ex-lockserv-automaton-20            5   1    0        61       2s             -     TO           61       3s   S3              -    TO
 tla-simpleregular-5                 1   0    0     2,524       2s        2,524       1s       2,524       1s   S4         2,524      1s
 pyv-sharded-kv-3-3-3                3   0    0    10,648       5s       10,648       2s      10,648       2s   S4        10,648      1s
 pyv-lockserv-20                     5   1    0        61       1s             -     TO           61       2s   S3              -    TO
 tla-twophase-9                      4   2    2 145,176       19s    10,340,352   9m41s      145,691     31s    S1    10,340,352  2m36s
 tla-twophase-10                     4   2    2 481,550      1m8s              -     TO      482,577  1m36s     S1              -    TO
 tla-twophase-counter-9              5   2    2 145,176       19s              -     TO      145,691     31s    S1              -    TO
 i4-learning-switch-4-3              1   0    -          -     TO     1,344,192   5m55s    1,344,192  5m55s     S4     1,344,192 1m37s
 ex-simple-decentralized-lock-4      2   0    0        20       2s            20      1s          20       1s   S4            20      1s
 i4-two-phase-commit-7               4   2    2 151,348       26s    10,016,384   3m38s      184,112     27s    S3    10,016,384    53s
 pyv-consensus-wo-decide-4           5   2    1    32,816       9s             -     TO       32,953     10s    S3              -    TO
 pyv-consensus-forall-4-4            6   1    0    33,545       8s             -     TO       33,545       9s   S3              -    TO
 pyv-learning-switch-trans-3         2   1    0       729       5s             -     TO          729       6s   S1              -    TO
 pyv-learning-switch-sym-2           2   1    0          4      2s        1,344       1s       1,344       1s   S4         1,344      1s
 pyv-sharded-kv-no-lost-keys-3-3-3   2   0    0     9,261       4s            27      1s       9,261       2s   S4         9,261      1s
 ex-naive-consensus-4-4              3   1    1       824       2s        1,001       1s       1,001       2s   S4         1,001      1s
 pyv-client-server-ae-4-2-2          2   1    1 352,145       42s     2,039,392   1m36s      352,145     49s    S1     2,039,392    28s
 pyv-client-server-ae-2-4-2          2   1    1 894,437     2m18s     2,387,032   1m16s    2,387,032  1m26s     S4     2,387,032    22s
 ex-simple-election-6-7              3   1    0 267,590     1m20s     2,900,256    3m7s      267,590  1m22s     S3     2,900,256    54s
 pyv-toy-consensus-epr-8-3           3   1    1    65,543    1m1s        70,903       6s      70,903       7s   S4        70,903      2s
 ex-toy-consensus-8-3                2   1    1    65,543     57s        70,903       5s      70,903       6s   S4        70,903      2s
 pyv-client-server-db-ae-2-3-2       5   4    4 188,158       12s     1,394,368    1m1s      188,799     15s    S1     1,394,368    18s
 pyv-client-server-db-ae-4-2-2       5   1    1 356,706     1m23s     3,624,960   2m48s      356,706  1m40s     S1     3,624,960    44s
 pyv-firewall-5                      2   0    0    56,072       9s       56,072       2s      56,072       3s   S4        56,072      1s
 ex-majorityset-leader-election-5    3   1    -          -     TO       166,306     15s      166,306     17s    S4       166,306      5s
 pyv-consensus-epr-4-4               6   2    1     7,018       3s             -     TO        7,221       5s   S3              -    TO
 mldr-2                              1   0    -          -     TO              -     TO             -     TO      -             -    TO

Fig. 6: Run time comparison between Recomp-Verify and TLC. The superscripts for each tool indicates how many threads are
allocated to a trial. The fastest times for each experiment are bolded. The “Strat.” column denotes the fastest strategy.


infer assumptions for assume-guarantee style compositional                          IX. L IMITATIONS AND F UTURE W ORK
verification. Nam et al. [19] use a similar strategy, but consider
multi-way decomposition and verification. While these works                  In Sec. VII-C, we show that the effectiveness of our ap-
report limited success, we are able to find efficient verification        proach is tied to the number of Ci components. In future work,
problems via recomposition.                                               we plan to investigate methods to make decomposition more
                                                                          granular, as well as decomposing properties. As the number
   Our work also relates to program slicing [20], [21] and cone           of components increase, we also plan to improve our methods
of influence reduction [37], both of which are techniques for             for finding efficient recomposition maps. For example, we plan
static specification reduction. These two techniques soundly              to improve our parallel technique so that different threads can
reduce the state variables needed for model checking by                   share intermediate work to save time and memory.
analyzing a variable dependency graph. Our work includes                     In this paper, we focus on using recomposition for explicit-
static specification reduction by allowing partial recomposition          state model checking. However, recomposition may also be
maps, as described in Sec. V.                                             effective for other compositional verification tasks. For exam-
   In the TLA+ ecosystem, TLC [23] is the most well-known                 ple, we plan to investigate whether recomposition can be used
model checker. Apalache [38], [39] is an alternate model                  in combination with non-explicit verification techniques, e.g.
checker that internally relies on SMT solvers. Apalache sup-              using SMT solvers or inductive invariants. We also plan to
ports bounded model checking and verification with induc-                 investigate whether recomposition can be used for efficient
tive invariants–two techniques that are outside the scope of              counter-example detection.
comparison for our tool. The TLA+ Proof System (TLAPS)
[40] provides an alternative to model checking TLA+ . TLAPS                                  ACKNOWLEDGEMENTS
proofs are manually constructed, but automatically verified by
dispatching proof obligations to SMT solvers. Endive [30] is                The authors are most grateful to Changjian Zhang, Andy
a tool that automatically infers inductive invariants for TLA+            Hammer, and the anonymous reviewers for their helpful
specifications, which then may be checked using a TLAPS                   comments on earlier versions of this paper. This project was
proof.                                                                    supported by the U.S. NSF Award #2144860.



                                                                     10
                             R EFERENCES                                                  S. Liu, T. Maibaum, and K. Araki, Eds. Berlin, Heidelberg: Springer
                                                                                          Berlin Heidelberg, 2008, pp. 105–125.
 [1] D. Giannakopoulou, K. S. Namjoshi, and C. S. Păsăreanu,                       [19] W. Nam, P. Madhusudan, and R. Alur, “Automatic symbolic
     Compositional Reasoning. Cham: Springer International Publishing,                    compositional verification by learning assumptions,” Form. Methods
     2018, pp. 345–383. [Online]. Available: https://doi.org/10.1007/978-3-               Syst. Des., vol. 32, no. 3, p. 207–234, jun 2008. [Online]. Available:
     319-10575-8 12                                                                       https://doi.org/10.1007/s10703-008-0055-8
 [2] R. Alur, P. Madhusudan, and W. Nam, “Symbolic compositional ver-                [20] I. Brückner and H. Wehrheim, “Slicing an integrated formal method for
     ification by learning assumptions,” in Computer Aided Verification,                  verification,” in Formal Methods and Software Engineering, K.-K. Lau
     K. Etessami and S. K. Rajamani, Eds. Berlin, Heidelberg: Springer                    and R. Banach, Eds. Berlin, Heidelberg: Springer Berlin Heidelberg,
     Berlin Heidelberg, 2005, pp. 548–562.                                                2005, pp. 360–374.
 [3] Y.-F. Chen, A. Farzan, E. M. Clarke, Y.-K. Tsay, and B.-Y. Wang,                [21] M. Weiser, “Programmers use slices when debugging,” Commun.
     “Learning minimal separating dfa’s for compositional verification,” in               ACM, vol. 25, no. 7, p. 446–452, jul 1982. [Online]. Available:
     Tools and Algorithms for the Construction and Analysis of Systems,                   https://doi.org/10.1145/358557.358577
     S. Kowalewski and A. Philippou, Eds. Berlin, Heidelberg: Springer               [22] L.     Lamport,     Specifying    Systems:     The    TLA+      Language
     Berlin Heidelberg, 2009, pp. 31–45.                                                  and      Tools     for      Hardware      and     Software     Engineers.
 [4] S. C. Cheung and J. Kramer, “Compositional reachability analysis                     Addison-Wesley,        June    2002.     [Online].    Available:   https:
     of finite-state distributed systems with user-specified constraints,” in             //www.microsoft.com/en-us/research/publication/specifying-systems-
     Proceedings of the 3rd ACM SIGSOFT Symposium on Foundations                          the-tla-language-and-tools-for-hardware-and-software-engineers/
     of Software Engineering, ser. SIGSOFT ’95. New York, NY, USA:                   [23] Y. Yu, P. Manolios, and L. Lamport, “Model checking tla+ specifica-
     Association for Computing Machinery, 1995, p. 140–150. [Online].                     tions,” in Correct Hardware Design and Verification Methods, L. Pierre
     Available: https://doi.org/10.1145/222124.222149                                     and T. Kropf, Eds. Berlin, Heidelberg: Springer Berlin Heidelberg,
                                                                                          1999, pp. 54–66.
 [5] ——, “Context constraints for compositional reachability analysis,”
                                                                                     [24] J. Gray and L. Lamport, “Consensus on transaction commit,” ACM
     ACM Trans. Softw. Eng. Methodol., vol. 5, no. 4, p. 334–377, oct 1996.
                                                                                          Trans. Database Syst., vol. 31, no. 1, p. 133–160, mar 2006. [Online].
     [Online]. Available: https://doi.org/10.1145/235321.235323
                                                                                          Available: https://doi.org/10.1145/1132863.1132867
 [6] ——, “Checking safety properties using compositional reachability
                                                                                     [25] D. Giannakopoulou, C. Pasareanu, and H. Barringer, “Assumption
     analysis,” ACM Trans. Softw. Eng. Methodol., vol. 8, no. 1, p. 49–78,
                                                                                          generation for software component verification,” in Proceedings 17th
     jan 1999. [Online]. Available: https://doi.org/10.1145/295558.295570
                                                                                          IEEE International Conference on Automated Software Engineering,,
 [7] J. M. Cobleigh, D. Giannakopoulou, and C. S. PĂsĂreanu, “Learning
                                                                                          2002, pp. 3–12.
     assumptions for compositional verification,” in Tools and Algorithms for
                                                                                     [26] C. A. R. Hoare, “Communicating sequential processes,” Commun.
     the Construction and Analysis of Systems, H. Garavel and J. Hatcliff,
                                                                                          ACM, vol. 21, no. 8, p. 666–677, aug 1978. [Online]. Available:
     Eds. Berlin, Heidelberg: Springer Berlin Heidelberg, 2003, pp. 331–
                                                                                          https://doi.org/10.1145/359576.359585
     346.
                                                                                     [27] W. J. Yeh and M. Young, “Compositional reachability analysis using
 [8] S. Graf and B. Steffen, “Compositional minimization of finite state sys-             process algebra,” in Proceedings of the Symposium on Testing, Analysis,
     tems,” in Proceedings of the 2nd International Workshop on Computer                  and Verification, ser. TAV4. New York, NY, USA: Association
     Aided Verification, ser. CAV ’90. Berlin, Heidelberg: Springer-Verlag,               for Computing Machinery, 1991, p. 49–59. [Online]. Available:
     1990, p. 186–196.                                                                    https://doi.org/10.1145/120807.120812
 [9] A. Gupta, K. L. McMillan, and Z. Fu, “Automated assumption gen-                 [28] R. Milner, Communication and Concurrency, ser. Ph/AMA Series
     eration for compositional verification,” in Proceedings of the 19th                  in Marketing. Prentice Hall, 1989. [Online]. Available: https:
     International Conference on Computer Aided Verification, ser. CAV’07.                //books.google.com/books?id=S5UZAQAAIAAJ
     Berlin, Heidelberg: Springer-Verlag, 2007, p. 420–432.                          [29] “Recomp-verify research prototype model checker for tla+,” https:
[10] C. Păsăreanu, D. Giannakopoulou, M. Bobaru, J. Cobleigh, and H. Bar-               //github.com/cmu-soda/recomp-verify/tree/FMCAD24, accessed: 2024-
     ringer, “Learning to divide and conquer: Applying the l*algorithm                    08-16.
     to automate assume-guarantee reasoning,” Formal Methods in System               [30] W. Schultz, I. Dardik, and S. Tripakis, “Plain and simple inductive
     Design, vol. 32, pp. 175–205, 06 2008.                                               invariant inference for distributed protocols in tla+,” in 2022 Formal
[11] C. S. Păsăreanu and D. Giannakopoulou, “Towards a compositional                    Methods in Computer-Aided Design (FMCAD). IEEE, 2022, pp. 273–
     spin,” in Model Checking Software, A. Valmari, Ed. Berlin, Heidelberg:               283.
     Springer Berlin Heidelberg, 2006, pp. 234–251.                                  [31] J. Malhotra, S. A. Smolka, A. Giacalone, and R. Shapiro, “Winston:
[12] K. Sabnani, A. Lapone, and M. Uyar, “An algorithmic procedure                        A tool for hierarchical design and simulation of concurrent systems,”
     for checking safety properties of protocols,” IEEE Transactions on                   in Specification and Verification of Concurrent Systems, C. Rattray, Ed.
     Communications, vol. 37, no. 9, pp. 940–948, 1989.                                   London: Springer London, 1990, pp. 140–152.
[13] K.-C. Tai and P. Koppol, “Hierarchy-based incremental analysis of               [32] C. Jones, “Specification and design of (parallel) programs.” vol. 83, 01
     communication protocols,” in 1993 International Conference on Network                1983, pp. 321–332.
     Protocols, 1993, pp. 318–325.                                                   [33] A. Pnueli, “In transition from global to modular temporal reasoning
[14] H. Zheng, “Compositional reachability analysis for efficient modular                 about programs,” in Logics and Models of Concurrent Systems, K. R.
     verification of asynchronous designs,” IEEE Transactions on Computer-                Apt, Ed. Berlin, Heidelberg: Springer Berlin Heidelberg, 1985, pp.
     Aided Design of Integrated Circuits and Systems, vol. 29, no. 3, pp.                 123–144.
     329–340, 2010.                                                                  [34] H. Barringer, D. Giannakopoulou, and C. Pasareanu, “Proof rules for
[15] ——, “Local state space construction for compositional verification of                automated compositional verification through learning,” 02 2003.
     concurrent systems,” in Proceedings of the 2014 International SPIN              [35] S. Bensalem, M. Bozga, J. Sifakis, and T.-H. Nguyen, “Compositional
     Symposium on Model Checking of Software, ser. SPIN 2014. New                         verification for component-based systems and application,” in Automated
     York, NY, USA: Association for Computing Machinery, 2014, p.                         Technology for Verification and Analysis, S. S. Cha, J.-Y. Choi, M. Kim,
     11–19. [Online]. Available: https://doi.org/10.1145/2632362.2632366                  I. Lee, and M. Viswanathan, Eds. Berlin, Heidelberg: Springer Berlin
[16] H. Zheng, Z. Zhang, C. J. Myers, E. Rodriguez, and Y. Zhang, “Com-                   Heidelberg, 2008, pp. 64–79.
     positional model checking of concurrent systems,” IEEE Transactions             [36] D. Angluin, “Learning regular sets from queries and counterexamples,”
     on Computers, vol. 64, no. 6, pp. 1607–1621, 2015.                                   Inf. Comput., vol. 75, no. 2, p. 87–106, nov 1987. [Online]. Available:
[17] J. M. Cobleigh, G. S. Avrunin, and L. A. Clarke, “Breaking up is                     https://doi.org/10.1016/0890-5401(87)90052-6
     hard to do: an investigation of decomposition for assume-guarantee              [37] E. Clarke, O. Grumberg, D. Kroening, D. Peled, and H. Veith, Model
     reasoning,” in Proceedings of the 2006 International Symposium on                    Checking, second edition, ser. Cyber Physical Systems Series. MIT
     Software Testing and Analysis, ser. ISSTA ’06. New York, NY, USA:                    Press, 2018. [Online]. Available: https://books.google.com/books?id=
     Association for Computing Machinery, 2006, p. 97–108. [Online].                      qJl8DwAAQBAJ
     Available: https://doi.org/10.1145/1146238.1146250                              [38] I. Konnov, J. Kukovec, and T.-H. Tran, “Tla+ model checking made
[18] B. Metzler, H. Wehrheim, and D. Wonisch, “Decomposition for com-                     symbolic,” Proc. ACM Program. Lang., vol. 3, no. OOPSLA, oct 2019.
     positional verification,” in Formal Methods and Software Engineering,                [Online]. Available: https://doi.org/10.1145/3360549




                                                                                11
[39] R. Otoni, I. Konnov, J. Kukovec, P. Eugster, and N. Sharygina, “Sym-          We will prove equation (8)–for both S and T –by considering
     bolic model checking for tla+ made faster,” in Tools and Algorithms           the following four cases for an arbitrary choice of i :
     for the Construction and Analysis of Systems, S. Sankaranarayanan and
     N. Sharygina, Eds. Cham: Springer Nature Switzerland, 2023, pp.                  1) Case 1: ai+1 ∈ αS and ai+1 ∈ αT .
     126–144.                                                                            In this case, the symbolic action for ai+1 must be in
[40] D. Cousineau, D. Doligez, L. Lamport, S. Merz, D. Ricketts, and
     H. Vanzetto, “Tla+ proofs,” Proceedings of the 18th International Sym-
                                                                                         α̂S and α̂T , and therefore (S // T )!ai+1 is equal to
                                                                                                                                ′
     posium on Formal Methods (FM 2012), Dimitra Giannakopoulou and                      S !ai+1 ∧T !ai+1 . Thus we see that bi+1   |= bi ∧S !ai+1 ∧
     Dominique Mery, editors. Springer-Verlag Lecture Notes in Computer                  T !ai+1 by the action-state-based semantics of TLA+ .
     Science, vol. 7436, pp. 147–154, January 2012. [Online]. Available:
     https://www.microsoft.com/en-us/research/publication/tla-proofs/
                                                                                         This implies equation (8) for the base case for both S
                                                                                         and T .
                               A PPENDIX A                                            2) Case 2: ai+1 ∈ αS and ai+1 ∈      / αT .
                            P ROOF OF T HM . 1                                           In this case, the symbolic action for ai+1 must be in
   Before proving Thm 1, we first introduce more general                                 α̂S but not in α̂T . Therefore, (S //T )!ai+1 is equal to
semantics for TLA+ specifications, namely action-state-based                             S !ai+1 ∧ (T !vars ′ = T !vars). Thus we see that bi+1
                                                                                                                                              ′
                                                                                                                                                   |=
                                                                                                                 ′
semantics. We define an action-state-based behavior σ as an in-                          bi ∧ S !ai+1 ∧ (T !vars = T !vars) by the action-state-
finite sequence of action-state pairs: (ϵ, b0 )(a1 , b1 )(a2 , b2 ) . . . ,              based semantics of TLA+ . This implies equation (8) for
where ϵ is the empty action. We use the notation σi to access                            the base case for both S and T .
the i th pair of σ. Notice that we require the initial action                         3) Case 3: ai+1 ∈  / αS and ai+1 ∈ αT .
to be empty, hence σ0 = (ϵ, b0 ). Let ϕ be an arbitrary TLA+                             This case is identical to Case 2, except with S and T
formula, let ψ be a TLA+ formula without temporal operators,                             flipped.
and let Next be the transition relation for a specification S ,                       4) Case 4: ai+1 ∈  / αS and ai+1 ∈   / αT .
i.e. Next is a TLA+ formula with prime operators. We now                                 In this case, the symbolic action for ai+1 must not be
define the action-state-based semantics of a behavior σ on a                             in α̂S nor α̂T . Therefore, (S // T )!ai+1 is equal to
TLA+ formula in terms of the action-state-based satisfaction                             (S !vars ′ = S !vars) ∧ (T !vars ′ = T !vars). Thus we
                                                                                                    ′
operator ⊢.                                                                              see that bi+1  |= bi ∧ (S !vars ′ = S !vars) ∧ (T !vars ′ =
                                                                                         T !vars) by the action-state-based semantics of TLA+ .
   σ⊢ψ                iff      b0 |= ψ                                                   This implies equation (8) for the base case for both S
   σ ⊢ □ϕ             iff      ∀i ∈ N : σi σi+1 . . . ⊢ ϕ                                and T .
   σ ⊢ ◇ϕ             iff      ∃i ∈ N : σi σi+1 . . . ⊢ ϕ                             Conversely, we will now show that JS Kαβ ∩ JT Kαβ ⊆ JS //
   σ ⊢ [Next]v        iff
                               (︁
                                  a1 ∈ αS ∧ b1′ |= (b0 ∧ a1 ) ∨
                                                             )︁                    T Kαβ . Suppose that σ ∈ JS Kαβ ∩ JT Kαβ , then it suffices to
                                                                                   show that σ ⊢ (S // T )!Spec. Recall that Spec has the form
                                     / αS ∧ b1′ |= (b0 ∧ v ′ = v )
                               (︁                                  )︁
                                  a1 ∈
                                                                                   Init ∧ □[Next]vars . Hence, we break the proof obligation into
Note that the semantics for σ ⊢ [Next]v implicitly uses Next                       two tasks, one for each conjunct. The first task is to show
because αS is defined by Next. We now define the action-                           σ ⊢ (S//T )!Init, or equivalently σ ⊢ S !Init ∧T !Init. Because
state-based semantics of a TLA+ specification S as the set                         σ ⊢ S !Spec and σ ⊢ T !Spec, we see that σ ⊢ S !Init and
of all action-state-based behaviors that satisfy S !Spec. More                     σ ⊢ T !Init; thus the first task is proved. The second task is
formally, we define the action-state-based semantics of S to                       to show that σ ⊢ □[(S // T )!Next]vars . By the definition of
be: JS Kαβ = {σ | σ ⊢ S !Spec}. We also define actions(σ) to                       the action-state-based semantics for TLA+ , this is equivalent
denote the action-based behavior a1 a2 . . . . We overload this                    to showing:
operator on a set of action-state-based behaviors A as follows:                       ∀i ∈ N :
actions(A) = {actions(σ) | σ ∈ A}.                                                       (︁                   ′
                                                                                                                                          )︁
                                                                                      ∨ ai+1 ∈ α(S //T ) ∧ bi+1   |= (bi ∧ (S //T )!ai+1 )
Lemma 5. JS //T Kαβ = JS Kαβ ∩ JT Kαβ                                                    (︁                   ′                                  (9)
                                                                                      ∨ ai+1 ∈/ α(S //T ) ∧ bi+1  |=
Proof. We will first show that JS //T Kαβ ⊆ JS Kαβ ∩ JT Kαβ .                                                   ′
                                                                                                                                 )︁
                                                                                            (bi ∧ (S //T )!vars = (S //T )!vars)
Suppose that σ ∈ JS // T Kαβ , then it suffices to show that
                                                                                   We will prove equation (9) by considering the following four
σ ⊢ S !Spec and σ ⊢ T !Spec. Recall that Spec has the form
                                                                                   cases for an arbitrary choice of i :
Init ∧ □[Next]vars . Hence, we break the proof obligation into
two tasks, one for each conjunct. The first task is to show                          1) Case 1: ai+1 ∈ αS and ai+1 ∈ αT .
that σ ⊢ S !Init and σ ⊢ T !Init; this fact follows because                              In this case, ai+1 ∈ α(S // T ). Next, notice that the
σ ⊢ (S !Init ∧ T !Init) by the definition of //. The second task                         symbolic action for ai+1 must be in α̂S and α̂T , and
is to show that σ ⊢ □[S !Next]vars and σ ⊢ □[T !Next]vars .                              therefore (S//T )!ai+1 is equal to S !ai+1 ∧ T !ai+1 . Fur-
                                                                                                     ′                         ′
By the definition of the action-state-based semantics for TLA+ ,                         thermore, bi+1  |= bi ∧ S !ai+1 and bi+1  |= bi ∧ T !ai+1 .
                                                                                                                    ′
this is equivalent to showing (for just S ):                                             Therefore we conclude bi+1 |= bi ∧ S !ai+1 ∧ T !ai+1
              (︁               ′
                                                       )︁                                which implies equation (9) for this case.
∀i ∈ N : ∨ ai+1 ∈ αS ∧ bi+1         |= (bi ∧ S !ai+1 )                               2) Case 2: ai+1 ∈ αS and ai+1 ∈     / αT .
                               ′
                                    |= (bi ∧ S !vars ′ = S !vars)
              (︁                                                 )︁
            ∨ ai+1 ∈  / αS ∧ bi+1                                                        In this case, ai+1 ∈ α(S // T ). Next, notice that the
                                                               (8)                       symbolic action for ai+1 must be in α̂S but not in



                                                                              12
     α̂T . Therefore, (S // T )!ai+1 is equal to S !ai+1 ∧                                         (︁ (S , V )
                                                                                 1: procedure S LICE             )︁
     (T !vars ′ = T !vars). Furthermore, bi+1
                                            ′
                                                 |= bi ∧ S !ai+1                 2:    T !vars ← ϵ S !vars ∩ V
           ′                      ′
     and bi+1 |= bi ∧ (T !vars = T !vars). Therefore we                          3:    T !Init ← S LICE -R EC(S !Init, V )
                 ′
     conclude bi+1    |= bi ∧ S !ai+1 ∧ (T !vars ′ = T !vars)                    4:    acts ← {S LICE
                                                                                                    (︁⋁︁-R EC(A, V ) | A ∈ α̂S })︁
     which implies equation (9) for this case.                                   5:    T !Next ← ϵ {A ∈ acts | A ̸= DEL}
  3) Case 3: ai+1 ∈  / αS and ai+1 ∈ αT .                                        6:    return T
     This case is identical to Case 2, except with S and T                       7: procedure S LICE -R EC (e, V )
     flipped.                                                                    8:    match
                                                                                        (︁   e with)︁
  4) Case 4: ai+1 ∈  / αS and ai+1 ∈ / αT .                                      9:    ϵ op(p) ≜ e1 →
     In this case, ai+1 ∈ / α(S // T ). Next, notice that the                   10:         E ← S LICE -R EC(e1 , V )
     symbolic action for ai+1 must not be in α̂S nor                            11:         if E = DEL then
     α̂T . Therefore, (S // T )!ai+1 is equal to (S !vars ′ =                   12:             return DEL
     S !vars) ∧ (T !vars ′ = T !vars). Furthermore, bi+1  ′
                                                               |=               13:         else        (︁           )︁
     bi ∧ (S !vars = S !vars) and bi+1 |= bi ∧ (T !vars ′ =
                   ′                   ′                                        14:             return ϵ op(p) ≜ E
                                         ′
     T !vars). Therefore we conclude bi+1     |= bi ∧ ((S !vars ◦                         (︁               )︁
              ′
     T !vars) = (S !vars ◦ T !vars)). Since (S //T )!vars =                     15:     ϵ ∃x ∈ d : e1 →
     (S !vars ◦T !vars), this implies equation (9) for this case.               16:           E ← S LICE -R EC(e1 , V )
                                                                                17:           if E = DEL then
                                                                                18:                return DEL
                                                                                19:           else
   Lem. 5 shows that our notion of parallel composition is                                                 (︁           )︁
semantically an intersection in the action-state-based seman-
                                                                                20:        (︄         )︄ ϵ ∃x ∈ d : E
                                                                                                   return
tics of TLA+ . We now prove one more lemma before proving
                                                                                                ⋀︁
                                                                                21:     ϵ           ci →
Thm. 1.                                                                                      i ∈ I
                                                                                22:           C ← {cj | β cj ⊆ V }
Lemma 6. Let A and B be LTSs, then JA ∥ BKα = JAKα ∩                            23:           if C = ∅ then
JBKα .                                                                          24:                return DEL
Proof. We first prove that JA ∥ BKα ⊆ JAKα ∩ JBKα .                             25:           else            ⋀︁
Suppose that σ ∈ JA ∥ BKα . Then there exists a sequence of                     26:                return ϵ ( Cj )
state pairs (p0 , q0 ), (p1 , q1 ), . . . such that p0 ∈ IA , q0 ∈ IB                        Fig. 7: Slicing procedure definitions.
and, for each nonnegative index i , either (1) σi ∈ αA,
(pi , σi , pi+1 ) ∈ δA , σi ∈ αB, and (qi , σi , qi+1 ) ∈ δB , (2)
σi ∈ αA, (pi , σi , pi+1 ) ∈ δA , σi ∈      / αB, and qi = qi+1 , (3)           Proof.
σi ∈/ αA, pi = pi+1 , σi ∈ αB, and (qi , σi , qi+1 ) ∈ δB , or                     JLTS(S //T )Kα = actions (JS //T Kαβ )
(4) σi ∈  / αA, pi = pi+1 , σi ∈      / αB, and qi = qi+1 . In each of                              = actions (JS Kαβ ∩ JT Kαβ )
these four cases, σi is a valid action from pi to pi+1 in A and
                                                                                                    = actions (JS Kαβ ) ∩ actions (JT Kαβ )
also a valid action from qi to qi+1 in B. Given that p0 ∈ IA
and q0 ∈ IB , we have σ ∈ JAKα and σ ∈ JBKα .                                                       = JLTS(S )Kα ∩ JLTS(T )Kα
   Conversely, we will now show that JAKα ∩ JBKα ⊆                                                  = JLTS(S ) ∥ LTS(T )Kα
JA ∥ BKα . Suppose that σ ∈ JAKα ∩ JBKα . Then there
                                                                                Where the second equality is due to Lem. 5, the third equality
exists a sequence of states p0 , p1 , . . . such that p0 ∈ IA
                                                                                holds because S and T do not share state variables, and the
and, for each nonnegative index i , either (1) σi ∈ αA and
                                                                                fifth equality is due to Lem. 6.
(pi , σi , pi+1 ) ∈ δ, or (2) σi ∈    / αA and pi = pi+1 . Likewise,
there exists a sequence of state q0 , q1 , . . . with the same                                            A PPENDIX B
conditions but for B. Then we can construct a sequence of state                                      S LICING P ROCEDURE
pairs (p0 , q0 ), (p1 , q1 ), . . . such that p0 ∈ IA , q0 ∈ IB and, for           We show the procedure for slicing in Fig. 7. Slicing works
each nonnegative index i , at least one of the following four                   by creating a new specification T such that β T = V . Line
conditions holds: (1) σi ∈ αA, (pi , σi , pi+1 ) ∈ δA , σi ∈ αB,                2 in Fig. 7 defines T ’s state variables to be S !vars restricted
and (qi , σi , qi+1 ) ∈ δB , (2) σi ∈ αA, (pi , σi , pi+1 ) ∈ δA ,              to the variables in V , while line 3 defines T ’s initial state
σi ∈/ αB, and qi = qi+1 , (3) σi ∈         / αA, pi = pi+1 , σi ∈ αB,           predicate to be S !Init restricted to the variables in V . Line 4
and (qi , σi , qi+1 ) ∈ δB , or (4) σi ∈   / αA, pi = pi+1 , σi ∈/ αB,          defines acts to be the set of the actions in S restricted to the
and qi = qi+1 . Thus, by definition, σ ∈ JA ∥ BKα .                             variables in V , and line 5 defines T ’s transition relation to be
                                                                                subset of acts that are well-formed.
  Using the prior two lemmas, we now prove Thm. 1.                                 The S LICE -R EC procedure on line 7 recursively descends
                                                                                into a TLA+ formula to restrict it to a set of variables V .
Theorem 1. JLTS(S //T )Kα = JLTS(S ) ∥ LTS(T )Kα .                              The procedure matches three cases (line 8): definitions (line



                                                                           13
9), existential quantifiers (line 15), and conjunctions (line 21).                              A PPENDIX D
We use the notation ϵ(.) to denote TLA+ syntax, and e1 (lines 9               T HE DATA F LOW PARTIAL O RDER R EFINES S TATIC
and 15) and ci (line 21) both refer to arbitrary TLA+ formulas.                         S PECIFICATION R EDUCTION
In a nutshell, slicing works by removing any conjunct that                   The following theorem shows that the data flow partial
contains a variable not in V (lines 22 and 26). In the case               order refines our static specification reduction scheme by
that every conjunct of a TLA+ expression must be removed, we              providing more information. In other words, the data flow
consider the entire expression malformed and we mark it for               partial order identifies
removal. We mark an expression for removal using the DEL                                    ⋃︁ a class of components that are necessary
                                                                          for verification ( i Xi ) and provides an ordering over these
keyword on line 24, which is then bubbled to the top (lines 12            components.
and 18); the actual removal happens in the set comprehension
on line 5.                                                                Theorem 4. Let G = {Ci | ∃Cj : Ci ≼ Cj or Cj ≼ Ci }
                                                                          be the set of all specifications
                                                                                                         ⋃︁ for which the data flow partial
                         A PPENDIX C                                      order is defined. Then G = i Xi , i.e. it is exactly the set of
             S TATIC S PECIFICATION R EDUCTION                            necessary components in static specification reduction.

   We begin by showing that the sequence {Xi } converges by               Proof. Based on the definition for Xi+1 , we provide an
the n + 1st term, i.e. at Xn .                                            alternate formulation for Ei+1 :

Theorem 3. Xn = Xn+1                                                            Ei+1 = {Cj | Cj ∈
                                                                                                / Xi and α̂Cj ∩ α̂Ei ̸= ∅}
                                                                                      = {Cj | Cj ∈
                                                                                                 / Xi } ∩ {Cj | α̂Cj ∩ α̂Ei ̸= ∅}
Proof. First, we note that n + 1 > |Xn+1 | because there
are at most n components that can be in each Xi . Next, a                    We now provide a formula for the set of all first (lesser)
simple inductive argument shows that whenever Xi ̸= Xi+1 ,                elements in each pair for Fi+1 . We will refer to this set as
|Xi+1 | ≥ i + 1. Finally, for the sake of contradiction,                  proj1 (Fi+1 ) for the projection onto the first element.
suppose that Xn ̸= Xn+1 . Then it would be the case that
                                                                              proj1 (Fi+1 ) = {Cj | Cj ∈ Ei and
n + 1 > |Xn+1 | ≥ n + 1 which is a contradiction.
                                                                                                      ∃Ck ∈ Ei+1 : α̂Cj ∩ α̂Ck ̸= ∅}
   Before presenting Lem. 2, we define states(σ) on                                         = Ei ∩ {Cj | α̂Cj ∩ α̂Ei+1 ̸= ∅}
an action-state-based behavior σ to denote the state-
                                                                                            = Ei
based behavior b0 b1 . . . . We overload this operator
on a set of action-state-based behaviors B as follows:                    Where the final equality is due to the alternate formulation of
states(B ) = {states(σ) | σ ∈ B }.                                        Ei+1 .
                                  ⋃︁                                         We now provide a formula for the set of all second (greater)
Lemma 2. S |= P if and only if //( i Xi ) |= P .                          elements in each pair for Fi+1 . We will refer to this set as
                  ⋃︁                                                      proj2 (Fi+1 ) for the projection onto the second element.
Proof. Let N = //( i Xi ) be the composition of⋃︁the necessary
components and let U = //({C1 , . . . , Cn } − i Xi ) be the                 proj2 (Fi+1 ) = {Ck | Ck ∈ Ei+1 and
composition of the unnecessary components. We note that                                               ∃Cj ∈ Ei : α̂Cj ∩ α̂Ck ̸= ∅}
α̂N ∩ α̂U = ∅, which follows from the definition of Xi+1 .                                = {Ck | Ck ∈ Ei+1 and α̂Ei ∩ α̂Ck ̸= ∅}
Also, because N is composed of C1 , β P ⊆ β N by property                                 = Ei+1 ∩ {Ck | α̂Ei ∩ α̂Ck ̸= ∅}
(P2) of Lem. 1. Because β P ⊆ β N and components do
not share state variables, we can therefore conclude that                                 = Ei+1
β P ∩ β U = ∅. Now we have:                                               Where the final equality is due to the alternate formulation of
                                                                          Ei+1 . Putting it all together we see:
        S |= P ⇐⇒ N //U |= P                                                                       ⎛        ⎞ ⎛            ⎞
                ⇐⇒ states(JN //U Kαβ ) ⊆ JP Kβ                                ⋃︂         ⋃︂           ⋃︂          ⋃︂
                                                                                  Xi =       Ei = ⎝      Ei ⎠ ∪ ⎝     Ei+1 ⎠
                ⇐⇒ states(JN Kαβ ∩ JU Kαβ ) ⊆ JP Kβ                           i≥0       i≥0           i≥0                i≥0
                ⇐⇒ states(JN Kαβ ) ⊆ JP Kβ                                              ⎛                       ⎞       ⎛                    ⎞
                                                                                            ⋃︂                              ⋃︂
                ⇐⇒ N |= P                                                             =⎝         proj1 (Fi+1 )⎠ ∪ ⎝               proj2 (Fi+1 )⎠
                                                                                           i≥0                              i≥0
In the equation above, the third biconditional is due to Lem. 5.                        ⎛                   ⎞       ⎛                    ⎞
The fourth biconditional follows for two reasons. The first                                 ⋃︂                          ⋃︂
reason is that β P ∩ β U = ∅, and therefore the states in each                        =⎝         proj1 (Fi )⎠ ∪ ⎝            proj2 (Fi )⎠ = G
                                                                                           i≥0                      i≥0
behavior of JU Kαβ will not restrict the values of the variables
in β P . The second reason is that α̂N ∩ α̂U = ∅; this implies            Where the penultimate equality follows because F0 = ∅.
αN ∩ αU = ∅, so the actions in each behavior of JU Kαβ will
not restrict any behavior in JN Kαβ .



                                                                     14
