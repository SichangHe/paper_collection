                                         Towards Concurrent Quantitative Separation Logic
                                         Ira Fesefeldt #
                                         Software Modeling and Verification Group, RWTH Aachen University, Germany
                                         Joost-Pieter Katoen #
                                         Software Modeling and Verification Group, RWTH Aachen University, Germany
                                         Thomas Noll #
                                         Software Modeling and Verification Group, RWTH Aachen University, Germany

                                               Abstract
                                         In this paper, we develop a novel verification technique to reason about programs featuring con-
                                         currency, pointers and randomization. While the integration of concurrency and pointers is well
                                         studied, little is known about the combination of all three paradigms. To close this gap, we combine
                                         two kinds of separation logic – Quantitative Separation Logic and Concurrent Separation Logic –
arXiv:2207.02822v3 [cs.LO] 30 Sep 2024




                                         into a new separation logic that enables reasoning about lower bounds of the probability to realise
                                         a postcondition by executing such a program.

                                         2012 ACM Subject Classification Theory of computation → Program verification; Theory of compu-
                                         tation → Concurrent algorithms; Mathematics of computing → Probabilistic reasoning algorithms

                                         Keywords and phrases Randomization, Pointers, Heap-Manipulating, Separation Logic, Concur-
                                         rency


                                          1     Introduction and Related Work
                                         In this paper, we aim to provide support for formal reasoning about concurrent imperat-
                                         ive programs that are extended by two important features: dynamic data structures and
                                         randomisation. In other words, it deals with the analysis and verification of concurrent
                                         probabilistic pointer programs. This problem is of practical interest as many concurrent
                                         algorithms operating on data structures use randomisation to reduce the level of interaction
                                         between threads. For example, probabilistic skip lists [47] work well in the concurrent setting
                                         [16] because threads can independently manipulate nodes in the list without much synchron-
                                         isation. In contrast, scalability of traditional balanced tree structures is difficult to achieve,
                                         since re-balancing operations may require locking access to large parts of the data structure.
                                         Bloom filters are another example of a probabilistic data structure supporting parallel ac-
                                         cess [8]. A further aspect is that stochastic modelling naturally arises when analysing faulty
                                         behaviour of (concurrent) software systems, as we later demonstrate in Section 5.
                                             However, the combination of these features poses severe challenges when it comes to
                                         implementing and reasoning about concurrent randomised algorithms that operate on dy-
                                         namic data structures. To give a systematic overview of related approaches, we mention that
                                         a number of program logics for reasoning about concurrent software have been developed
                                         [13, 14, 17, 29, 31, 42]. Next, we will address the programming-language extensions in
                                         isolation and then consider their integration. An overview is shown in Figure 1.
                                             Pointers. Pointers constitute an essential concept in modern programming languages,
                                         and are used for implementing dynamic data structures like lists, trees etc. However, many
                                         software bugs can be traced back to the erroneous use of pointers by e.g. dereferencing null
                                         pointers or accidentally pointing to wrong parts of the heap, creating the need for computer-
                                         aided verification methods. The most popular formalism for reasoning about such programs
                                         is Separation Logic (SL) [25, 49], which supports Hoare-style verification of imperative,
                                         heap-manipulating and, possibly, concurrent programs. Its assertion language extends first-
                                         order logic with connectives that enable concise specifications of how program memory, or
2   Towards Concurrent Quantitative Separation Logic




                                             Concurrency


                                                       Prob. rel.-guar.
                                      CSL [44]
                                                          calc. [39]
                                               Polaris [50]
                                                 CQSL

                              Pointers                        Randomisation
                              SL [25, 49]        QSL [5]      Expectations [38]




       Figure 1 Overview of programming language features and formal approaches (CQSL denotes
    our concurrent extension of QSL)


    other resources, can be split-up and combined. In this way, SL supports local reasoning
    about the resources employed by programs. Consequently, program parts can be verified
    by considering only those resources they actually access – a crucial property for building
    scalable tools including automated verifiers [7, 27, 41, 46], static analysers [6, 10, 19], and
    interactive theorem provers [30].
        The notion of resources, and in particular their controlled access, becomes even more
    important in a concurrent setting. Therefore, SL has been extended to Concurrent Separ-
    ation Logic (CSL) [44] to enable reasoning about resource ownership, where the resource
    typically is dynamically allocated memory (i.e., the heap). The popularity of CSL is evident
    by the number of its extensions [9]. Of particular importance to our work is [52], which
    presents a soundness result for CSL that is formulated in an inductive manner, matching
    the ‘small-step’ operational style of semantics. Here, we will employ a similar technique that
    also takes quantitative aspects (probabilities) into account.
        Randomisation. Probabilistic programs (i.e., programs with the ability to sample from
    probability distributions) are increasingly popular for implementing efficient randomised
    algorithms [40] and describing uncertainty in systems [11, 18], among other similar tasks. In
    such applications, the purely qualitative (true vs. false) approach of classical logic is obviously
    not sufficient. The method advocated by us is based on weakest precondition reasoning as
    established in a classical setting by Dijkstra [12]. It has been extended to provide semantic
    foundations for probabilistic programs by Kozen [33, 34] and McIver & Morgan [38]. The
    latter also coined the term ‘weakest preexpectation’ for random variables that take over the
    role of logical formulae when doing quantitative reasoning about probabilistic programs –
    the quantitative analogue of weakest preconditions. Their relation to operational models is
    studied in [20]. Moreover, weakest preexpectation reasoning has been shown to be useful for
    obtaining bounds on the expected resource consumption [43] and, especially, the expected
    run-time [32] of probabilistic programs.
        However, verification techniques that support reasoning about both randomisation and
    dynamic data structures are rare – a surprising situation given that randomised algorithms
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                            3


typically rely on such data structures. One notable exception is the extension of SL to
Quantitative Separation Logic (QSL) [4, 5], which marries SL and weakest preexpectations.
QSL has successfully been applied to the verification of randomised algorithms, and QSL
expectations have been formalised in Isabelle/HOL [23]. The present work builds on these
results by additionally taking concurrency into account.
    A prior program logic designed for reasoning about programs that are both concur-
rent and randomised but do not maintain dynamic data structures is the probabilistic
rely-guarantee calculus developed by McIver et al. [39], which extends Jones’s original rely-
guarantee logic [29] by probabilistic constructs.
    Later, Tassarotti & Harper [50] address the full setting of concurrent probabilistic pointer
programs by combining CSL with probabilistic relational Hoare logic [3] to obtain Polaris,
a Concurrent Separation Logic with support for probabilistic reasoning. Verification is thus
understood as establishing a relation between a program to be analysed and a program which
is known to be well-behaved. Programs which do not almost surely terminate, however, are
outside the scope of their approach. In contrast, the goal of our method is to directly measure
quantitative program properties on source-code level using weakest liberal preexpectations
defined by a set of proof rules, including possibly non-almost surely terminating programs.
Since the weakest liberal preexpectation includes non-termination probability, we can use
invariants to bound the weakest liberal preexpectation of loops from below.
    The main contributions of this paper are:
    the definition of a concurrent heap-manipulating probabilistic guarded command lan-
    guage (chpGCL) and its operational semantics in terms of Markov Decision Processes
    (MDP);
    a formal framework for reasoning about quantitative properties of chpGCL programs,
    which is obtained by extending classical weakest liberal preexpectations by resource
    invariants;
    a sound proof system that supports backward reasoning about such preexpectations; and
    the demonstration of our verification method on a (probabilistic) producer-consumer
    example.

    The remainder of this paper is organised as follows. Section 2 introduces QSL as an
assertion language for quantitative reasoning about (both sequential and concurrent) prob-
abilistic pointer programs. In Section 3, we present the associated programming language
(chpGCL) together with an operational semantics. Next, in Section 4 we develop a calculus
for reasoning about lower bounds of weakest liberal preexpectations. Its usage is demon-
strated in Section 5, and in Section 6 we conclude and explain further research directions.
The main part of the paper is accompanied by an extensive appendix providing elaborated
proofs and additional details about the examples.


 2     Quantitative Separation Logic

To reason about probability distributions over states of a program, we use Quantitative
Separation Logic (QSL) [5, 36]. QSL is an extension of classical (or qualitative) Separation
Logic in the sense that instead of mapping stack/heap pairs to booleans in order to gain a
set characterization of states, we assign probabilities to stack/heap pairs.

▶ Definition 2.1 (Stack). Let Vars be a fixed set of variables. A stack s : Vars → Z is a
mapping from variable symbols to values. We denote the set of all stacks by Stacks.
4   Towards Concurrent Quantitative Separation Logic


    When evaluating an (arithmetic or boolean) expression e with respect to a stack s, we write
    e(s). In this sense, expressions are mappings from stacks to values. The stack that agrees
    with a stack s except for the value of x, which is mapped to v, is denoted as s [x := v].
    ▶ Definition 2.2 (Heaps). A heap h : L → Z is a mapping from a finite subset of locations
    L ⊂ N>0 to values. We denote the set of all heaps by Heaps.
    We furthermore write dom (h) for the domain of h, h1 ⊥ h2 if and only if dom (h1 ) ∩
    dom (h2 ) = ∅, and for disjoint heaps h1 ⊥ h2 we define the disjoint union of heaps h1 and h2 as
                            
                            h1 (ℓ) if ℓ ∈ dom (h1 )
                            
                            
       (h1 ⋆ h2 )(ℓ) =        h2 (ℓ) if ℓ ∈ dom (h2 )
                            
                            
                            undef else .

    A pair of a stack and a heap is a state of the program. The stack is used to describe the
    variables of the program. The heap describes the addressable memory of the program.
    ▶ Definition 2.3 (Program States). A program state σ ∈ Stacks × Heaps is a pair consisting
    of a stack and a heap. The set of all states is denoted by States.
    Expectations are random variables that map states to non-negative reals. In this paper, we
    only consider one-bounded expectations. These do not map states to arbitrary non-negative
    reals, but only to reals between 0 and 1. The nomenclature of calling these expectations
    rather than random variables is due to the weakest preexpectation calculus being used to
    derive expectations.
    ▶ Definition 2.4 (Expectations). A (one-bounded) expectation X : States → [0, 1] is a map-
    ping from program states to probabilities. We write E≤1 for the set of all (one-bounded)
    expectations. We call an expectation φ qualitative if for all (s, h) ∈ States we have that
    φ(s, h) ∈ {0, 1}. We define the partial order (E≤1 , ≤) as the pointwise application of less
    than or equal, i.e., X ≤ Y if and only if ∀(s, h) ∈ States X(s, h) ≤ Y (s, h).
    We use capital letters for regular (one-bounded) expectations and Greek letters for qual-
    itative expectations. As in [5], we choose to not give a specific syntax for QSL since the
    weakest liberal preexpectation of a given postexpectation – for which we provide more de-
    tail in Section 3 – may not be expressible in a given syntax. Instead, we prefer to interpret
    expectations as extensional objects that can be combined via various connectives. These
    connectives include (but are not limited to) the pointwise-applied connectives of addition,
    multiplication, exponentiation, maximum and minimum. As it is common in quantitat-
    ive logics, the maximum/minimum is the quantitative extension of disjunction/conjunction,
    respectively. However, multiplication can be chosen as the quantitative extension of conjunc-
    tion as well. We denote the substitution of a variable x by the expression e in the expectation
    X as X [x := e] and define it as X [x := e] (s, h) = X(s [x := e(s)] , h). When dealing with
    state predicates, we use Iverson brackets [26] to cast boolean values into integers:
                     (
                      1 if (s, h) ∈ b
        [b] (s, h) =
                      0 else

    Note that we could also define predicates as mappings from states to 0 or 1. We refrain from
    this, since (1) usage of Iverson brackets is standard in weakest preexpectation reasoning and
    (2) we may use QSL inside of Iverson brackets.
        For a state (s, h), the empty heap predicate emp holds if and only if dom (h) = ∅, the
    points-to predicate e 7→ e0 , . . . , en holds if and only if dom (h) = {e(s) + 0, . . . , e(s) + n}
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                             5


and ∀i ∈ {0, . . . , n} h(e(s) + i) = ei (s), the allocated predicate e 7→ − holds if and only if
dom (h) = {e(s)}, and the equality predicate e = e′ holds if and only if e(s) = e′ (s).
   We also use quantitative extensions of two separation connectives – the separating con-
junction and the magic wand. The quantitative extension of the separating conjunction,
which we call separating multiplication, maximises the value of the product of its arguments
applied to separated heaps:

     (X ⋆ Y )(s, h) = sup { X(s, h1 ) · Y (s, h2 ) | h1 ⋆ h2 = h }

The definition of separating multiplication is similar to the classical separating conjunction:
the existential quantifier is replaced by a supremum and the conjunction by a multiplication.
Note that the set over which the supremum ranges is never empty.
    The (guarded) quantitative magic wand is defined for a qualitative first argument and a
quantitative second argument. We minimise the value of the second argument applied to the
original heap joined with a heap that evaluates the first argument to 1, i.e., for qualitative
expectation φ and expectation Y we have:

     (φ −−⋆ Y )(s, h) = inf { Y (s, h′′ ) | φ(s, h′ ) = 1, h′′ = h ⋆ h′ }

If the set is empty, the infimum evaluates to the greatest element of all probabilities, which
is 1. Although it is also possible to allow expectations in both arguments (cf. [5]), we restrict
ourselves to the guarded version of the magic wand. This restriction allows us to exploit the
superdistributivity of multiplication, i.e., φ −−⋆ (X · Y ) ≥ (φ −−⋆ X) · (φ −−⋆ Y ).

▶ Example 2.5. To illustrate separating operations and lower bounding in QSL, we consider
X = [x 7→ − ] ⋆ ([x 7→ y] −−⋆ (0.5 · [x 7→ − ])), Y = 0.5 · [x 7→ − ] and Z = 0.5 · [x 7→ y]. Let
us consider the semantics of X in more detail. X is non-zero only for states that allocate
exactly x. In this case, after changing the value pointed to by x to y, 0.5 is returned if x is
still allocated (which obviously holds). Thus, the combination of separating multiplication
and magic wand realises a change of value: First a pointer is removed from the heap by
using separating multiplication, and afterwards we add it back with a different value using
the magic wand. Note that [x 7→ y] is qualitative, which is required for our version of the
magic wand. Then we have X = Y and Z ≤ X.

 3      Programming Language and Operational Semantics
Our programming language is a concurrent extension of the heap-manipulating and prob-
abilistic guarded command language [5]. Our language features both deterministic and
probabilistic control flow, atomic regions, concurrent threads operating on shared memory,
variable-based assignments, and heap manipulations. Although our language allows arbit-
rary shared memory, we will later only be able to reason about shared memory in the heap.
Conditional choice without an else branch is considered syntactic sugar. Atomic regions con-
sist of programs without memory allocation or concurrency. However, probabilistic choice
is admitted. Programs that satisfy this restriction are called tame.
    The reason to restrict the program fragment within atomic regions is that non-tame
statements introduce non-determinism (as addresses to be allocated and schedulings of con-
current programs are chosen non-deterministically), which would increase the semantics’
complexity while providing only little benefit (we refer to [1] regarding the handling of non-
tame probabilistic programs in atomic regions). If an atomic region loops with a certain
probability p, we instead transition to a non-terminating program with probability p.
6   Towards Concurrent Quantitative Separation Logic


    ▶ Definition 3.1 (Concurrent Heap-Manipulating Probabilistic Guarded Command Language).
    The concurrent heap-manipulating probabilistic guarded command language chpGCL is gen-
    erated by the grammar

       C    −→        ↓                                            (terminated program)
                  | diverge                                   (non-terminating program)
                  | x := e                                                  (assignment)
                  | { C } [ ep ] { C }                                     (prob. choice)
                  | C; C                                              (seq. composition)
                  | atomic { C }                                         (atomic region)
                  | if ( b ) { C } else { C }                        (conditional choice)
                  | while ( b ) { C }                                                  (loop)
                  |       C∥C                                              (concurrency)
                  | x := new (e0 , . . . , en )                               (allocation)
                  | free(e),                                                    (disposal)
                  | x := < e >                                                   (lookup)
                                    ′
                  | < e > := e                                                (mutation)

    where x is a variable, e, e′ , ei : Stacks → Z are arithmetic expressions, ep : Stacks → [0, 1] is
    a probabilistic arithmetic expression and b ⊆ Stacks is a guard.

    ▶ Example 3.2. We consider as running example a little program with two threads syn-
    chronizing over a randomised value:

       < r > := −1 ;
                                                   y := < r > ;
           { < r > := 0 } [ 0.5 ] { < r > := 1 }
                                                   while ( y = −1 ) { y := < r > } ;

    We first initialise our resource r with some integer that stands for an undefined value (here
    −1). The first thread now either assigns 0 or 1 with probability 0.5 to r. As soon as r has
    a new value, the second thread receives this value and terminates as r is not −1 any more.

        We define the operational semantics of our programming language chpGCL in the form
    of a Markov Decision Process (MDP for short). An MDP allows the use of both non-
    determinism, which we need for interleaving multiple threads, and probabilities, which are
    used for encoding probabilistic program commands. A transition between states is thus
    always annotated with two parameters: (1) an action that is taken non-deterministically
    and (2) a probability to transition to a state given the aforementioned action.

    ▶ Definition 3.3 (Markov Decision Process). A Markov Decision Process M = (U, Act, P)
    consists of a countable set of states U , a mapping from states to enabled actions Act : U → 2A
    for a countable set of actions A, and a transition probability function P : (U ×A) → U → [0, 1]
    where for all σ ∈ U and a ∈ Act(σ) we require σ′ ∈U P(σ, a)(σ ′ ) = 1. We also use the
                                                           P
                             p
    shorthand notation σ −   → σ ′ for P(σ, a)(σ ′ ) = p in case p > 0.
                                a

        We define the operational semantics of chpGCL as an MDP. A state in this MDP consists
    of a chpGCL program to be executed and a program state (s, h). The meaning of basic
    commands, i.e., assignments, heap mutations, heap lookups, memory allocation and disposal,
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                                                                     7



                                                                        1
                                                                                                             ASSIGN
                                                  x := e, (s, h) −−−−→ ↓ , (s [x := e(s)] , h)
                                                                   assign
                     e(s) ∈ dom (h)                                                                          e(s) ̸∈ dom (h)
                         1
                                                                     LOOKUP                                                 1
                                                                                                                                             LOOKUP-ABT
   x := < e >, (s, h) −−−−→ ↓ , (s [x := h(e(s))] , h)                                       x := < e >, (s, h) −−−−−−−→ abort
                      lookup                                                                                        lookup-abt
                       e(s) ∈ dom (h)                                                                    e(s) ̸∈ dom (h)
                             1
                                                                            MUT                                          1
                                                                                                                                              MUT-ABT
    < e > := e′ , (s, h) −−−−−−→ ↓ , (s, h [e(s) := e′ (s)])                               < e > := e′ , (s, h) −−−−−−−−→ abort
                        mutation                                                                                   mutation-abt
         e(s) ∈ dom (h)           h′ = h \ {e(s) 7→ h(e(s))}                                          e(s) ̸∈ dom (h)
                                          1
                                                                            FREE                                     1
                                                                                                                                       FREE-ABT
                 free(e), (s, h) −−→ ↓ , (s, h′ )                                           free(e), (s, h) −−−−−→ abort
                                       free                                                                       free-abt
 ℓ + 0, . . . ℓ + n ∈ N>0 \ dom (h)               e0 (s) = v0 , . . . , en (s) = vn          h′ = h ⋆ {ℓ + 0 7→ v1 } ⋆ · · · ⋆ {ℓ + n 7→ vn }
                                                                                   1
                                                                                                                                                    ALLOC
                                  x := new (e0 , . . . , en ) , (s, h) −−−−→ ↓ , (s [x := ℓ] , h′ )
                                                                               alloc-ℓ


   Figure 2 Operational semantics of basic commands in chpGCL

                                           p                                                             p
                                      → C1′ , (s′ , h′ )
                          C1 , (s, h) −                                                                → C2′ , (s′ , h′ )
                                                                                           C2 , (s, h) −
                                           a                                                             a
                                           p
                                                                        SEQ                                   p
                                                                                                                                    SEQ-END
                                     → C1′ ; C2 , (s′ , h′ )
                    C1 ; C2 , (s, h) −                                                                   → C2′ , (s′ , h′ )
                                                                                         ↓ ; C2 , (s, h) −
                                           a                                                                  a
                                       p                                                             p
                       C1 , (s, h) −
                                   → abort                                               C2 , (s, h) −
                                                                                                     → abort
                                       a                                                             a
                                              p
                                                             SEQ-ABT                                     p
                                                                                                                         SEQ-END-ABT
                     C1 ; C2 , (s, h) −
                                      → abort                                          ↓ ; C2 , (s, h) −
                                                                                                       → abort
                                              a                                                          a
                                 s∈b                                                                                 s ̸∈ b
                                                       1
                                                                            IF-T                                                                     IF-F
                                                                                                                                       1
     if ( b ) { C1 } else { C2 } , (s, h) −−→ C1 , (s, h)                                if ( b ) { C1 } else { C2 } , (s, h) −−→ C2 , (s, h)
                                                      if-t                                                                            if-f
                                                                    s∈b
                                                                    1
                                                                                                                    WHILE-T
                             while ( b ) { C1 } , (s, h) −−−−→ C1 ; while ( b ) { C1 }, (s, h)
                                                                  loop-t

                                 s ̸∈ b
                                                  1
                                                                    WHILE-F                                                                   DIV
           while ( b ) { C1 } , (s, h) −−−→ ↓ , (s, h)                                                              1
                                                                                            diverge, (s, h) −−→ diverge, (s, h)
                                               loop-f
                                                                                                                   div
                          ep (s) = p                                                                           ep (s) = p
                                              p                   PROB-L                                                     1−p
                                                                                                                                               PROB-R
        { C1 } [ ep ] { C2 } , (s, h) −−−→ C1 , (s, h)                                   { C1 } [ ep ] { C2 } , (s, h) −−−→ C2 , (s, h)
                                          prob                                                                               prob



   Figure 3 Operational semantics of non-concurrent control-flow operations in chpGCL


is defined by the inference rules shown in Figure 2. An action is enabled if and only if an
inference rule for this action exists. We use an abort keyword to indicate that a memory
access error happened and terminate at this state. We consider aborted runs as undesired
runs. The condition σ′ ∈U P(σ, a)(σ ′ ) = 1 holds for all states in a chpGCL program. States
                      P

with program ↓ or abort have no enabled actions, thus the condition holds trivially for all
enabled actions a; non-probabilistic programs only have actions with trivial distributions;
states with probabilistic choice only have a single action with a biased coin-flip distribution;
and other programs are composed of these.
    Control-flow statements include while loops, conditional choice, sequential composition
and probabilistic choice, and we define their operational semantics in Figure 3. For the sake
of brevity, we do not include a command to sample from a distribution.
    The remaining control-flow statements handle concurrency, i.e., the concurrent execution
of two threads and the atomic execution of regions. An atomic region may only terminate
                                                      p
with a certain probability. The notation C, (s, h) −  → ∗ . . . denotes that program C does
not terminate on state (s, h) with probability p. As mentioned before, we will only allow
tame programs inside atomic regions. A tame program does not require any (scheduling)
actions since its Markov model is fully probabilistic. To formally define the syntax used in
the inference rules for atomic regions, we first need to introduce schedulers, which are used
8   Towards Concurrent Quantitative Separation Logic

                    p                                                                             p
                    →∗
          C, (s, h) −        ↓ , (s′ , h′ )       C is tame                                       →∗ abort
                                                                                        C, (s, h) −                      C is tame
                                          p             ′   ′
                                                                    ATOM-END                                         p                  ATOM-ABT
           atomic { C } , (s, h) −−−−→ ↓ , (s , h )                                     atomic { C } , (s, h) −−−−→ abort
                                      atomic                                                                       atomic
                                                                p
                                                            →∗ . . .
                                                  C, (s, h) −                    C is tame
                                                                         p                       ATOM-LOOP
                                          atomic { C } , (s, h) −−−−→ diverge, (s, h)
                                                                       atomic
                                      p                                                                        p
                                    → C1′ , (s′ , h′ )
                        C1 , (s, h) −                                                                    → C2′ , (s′ , h′ )
                                                                                             C2 , (s, h) −
                                      a                                                                        a
                                      p                                CON-L                                   p                            CON-R
              C1 ∥ C2 , (s, h) −−−→ C1′              C2 , (s′ , h′ )                  C1 ∥ C2 , (s, h) −−−→ C1           C2′ , (s′ , h′ )
                                    C1,a                                                                   C2,a
                                     p                                                                p
                        C1 , (s, h) −
                                    → abort                                              C2 , (s, h) −
                                                                                                     → abort
                                      a                                                               a
                                              p             CON-L-ABT                                      p                CON-R-ABT
                 C1 ∥ C2 , (s, h) −−−→ abort                                         C1 ∥ C2 , (s, h) −−−→ abort
                                          C1,a                                                            C2,a



                                                                             1
                                                                                             CON-END
                                                    ↓ ∥ ↓ , (s, h) −−−−−→ ↓ , (s, h)
                                                                         con-end


       Figure 4 Operational semantics of concurrent control-flow operations in chpGCL


    to resolve non-determinism in an MDP. There are various classes of schedulers, and indeed
    we will later allow the use of different classes. However, we do require that all schedulers are
    deterministic and may have a history. This especially rules out any randomised scheduler,
    which would be an interesting topic, but is out of scope for the results presented here. Our
    schedulers use finite sequences of MDP states as histories.
    ▶ Definition 3.4 (Scheduler). A scheduler is a mapping s : U + → A from histories of states
    to enabled actions, i.e., s(σ1 . . . σn ) ∈ Act(σn ). We denote the set of all schedulers by S.
       For final states σ ′ (i.e., with program ↓ or abort) and an MDP (U, Act, P), we define
                                X  m−1
                                      Y
                         ′
       reach(n, σ1 , s, σ ) =              P(σi , s(σ1 . . . σi ))(σi+1 )
                                                     i=1
                                                                                         
                                                     σ1 . . . σm ∈ U m , σm = σ ′ , m ≤ n ,                                                         (1)
                    p
                 →∗ σ ′
               σ −                   iff p = lim reach(n, σ, s, σ ′ ) ,                                                                             (2)
                    s                        n→∞
              1−p                             X
          σ −−→∗ . . .               iff p =       lim reach(n, σ, s, σ ′ ) .                                                                       (3)
                s                                                   n→∞
                                                       σ ′ final

    For a function f and a predicate b, we write [f (x) | x ∈ b] for the bag consisting of the
    values f (x) with x ∈ b. We use notation (1) to calculate the probability to reach the final
    state σ ′ from σ1 in at most n steps w.r.t s. We unroll the MDP here into the Markov Chain
    induced by s after at most n steps (cf. [2, Definition 10.92]). With notation (2), we define
    the reachability probability of a final state and with notation (3), we define the probability
    of non-termination. We avoid reasoning about uncountable sets of paths in case of non-
    termination by taking the probability to not reach a final state, i.e., a state with program
    ↓ or abort. A scheduler s is unique if for every state σ ∈ U there is at most one enabled
    action s can map to, i.e., |Act(σ)| ≤ 1. In that case, we usually omit the corresponding
    transition label.
        To reason about the operational semantics using QSL, we use weakest liberal preexpect-
    ations [5, 37], which take the greatest lower bound of the expected value with respect to a
    postexpectation together with the probability of non-termination for all schedulers that we
    want to consider. We allow subsets of schedulers S ⊆ S in order to apply fairness conditions.
    Later, we only consider the complete set of schedulers. In that case, we omit the superscript
    from the function wlp, which is defined in the following.
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                   9


▶ Definition 3.5 (Weakest Liberal Preexpectation). For a program C and an expectation X,
we define the weakest liberal preexpectation with respect to a set of schedulers ∅ =   ̸ S ⊆ S as
                                  Xh                                                i
                                                                    p
   wlpS JCK (X) (s, h) = inf            p · X(s′ , h′ ) | C, (s, h) −
                                                                    →∗ ↓ , (s′ , h′ ) + pdiv
                                                                    s
                                                                      
                                                             pdiv ∗
                                    s ∈ S and C, (s, h) −−−→ . . . .
                                                                s

▶ Example 3.6. For program C in Example 3.2, we evaluate (without proof) wlpJCK ([y = 0]) =
wlpS JCK ([y = 0]) = 0.5 ⋆ [r 7→ − ]. That is, if r is allocated, then the likelihood of C termin-
ating without aborting in a state in which y equals 0 is 0.5, and zero otherwise. We will
prove that this is a lower bound in Example 4.2.

    4      Weakest Safe Liberal Preexpectations
For sequential probabilistic programs, a backwards expectation transformer can be defined
to compute wlp [5]. This is not feasible for concurrent programs due to the non-locality
of shared memory. Instead, we drop exact computation in our approach and reason about
lower bounds of wlp by using inference rules similar to Hoare triples. To support shared
memory, we furthermore introduce a modified version of wlp – the weakest resource-safe
liberal preexpectation. The general idea as inspired by [52] is to prove that the shared
memory is invariant with respect to a qualitative expectation, which we call a resource
invariant. In other words, the shared memory is proven to be safe with respect to the resource
invariant. We archive this by enforcing that at every point in the program’s execution (except
for executions in atom regions), some part of the heap is satisfied by the resource invariant.
In Example 4.2 we use the resource invariant max { [r 7→ 0], [r 7→ −1] } to prove the lower
bound from Example 3.6. We enforce that the program states do not include the shared
memory any more, the transitions however are taken with any possible shared memory.
▶ Definition 4.1 (Weakest Resource-Safe Liberal Preexpectation). We first consider the ex-
pectation after one step with respect to a mapping from programs to expectations, that is, for
a program C and a mapping t : chpGCL → E≤1 , we define
                                Xh                                                         i
                                                                         p
    stepJCK (t) (s, h) = inf           p · t(C ′ )(s′ , h′ ) | C, (s, h) −
                                                                         → C ′ , (s′ , h′ )
                                                                         a
                                                         
                                  a ∈ Act(C, (s, h)) .

We define the weakest resource-safe liberal preexpectation after n steps for a program C, a
postexpectation X and a (qualitative) resource invariant ξ as
                      
                      1
                      
                                                                          if n = 0
   wrlpn JCK (X | ξ) = X                                                   if n ̸= 0 and C = ↓
                      
                      ξ −−⋆ stepJCK λC ′ . wrlp
                      
                                                      JC ′ K (X | ξ) ⋆ ξ
                                                                         
                                                                           otherwise1 .
                                                        n−1

 Finally, we define the weakest resource-safe liberal preexpectation for arbitrarily many steps
as
        wrlpJCK (X | ξ) = lim wrlpn JCK (X | ξ) .
                         n→∞


1
    We use λC ′ . X for the function which, when applied to the argument C, reduces to X in which every
    occurrence of C ′ in X is replaced by C.
10   Towards Concurrent Quantitative Separation Logic


     An important observation is that for the special resource invariant [emp], wlp and wrlp
     coincide (cf. Theorem B.10).This enables us to reason about lower bounds for probabilities
     of qualitative preconditions (and in general lower bounds for the expected value of one-
     bounded random variables). When reasoning about such probabilities, we first express a
     property for which we aim to prove a lower bound on wlp, afterwards we can transform
     it into wrlp with the resource invariant [emp] and use special rules to enrich the resource
     invariant with more information. The resource invariant should always cover all possible
     states that the shared memory may be in at any time during the program’s execution. It is
     fine if the resource invariant is violated during executions of atomic regions, since we only
     care about safeness during executions with inferences between threads.
         We mention that wrlp is heavily inspired by [52]. We formalise the connection between
     Vafeiadis’ Concurrent Separation Logic and our weakest resource-safe liberal preexpectation
     below. In [52] a judgement is defined by a safe predicate that is similar to how we defined
     wrlp.

     ▶ Definition 4.1 (Safe Judgements [52]). The predicate safen (C, s, h, ξ, φ) holds for qualit-
     ative φ and ξ and non-probabilistic program C if and only if
     1. if n = 0, then it holds always; and
     2. if n > 0 and C = ↓ , then φ(s, h) = 1; and
     3. if n > 0 and for all hξ and hF with ξ(s, hξ ) = 1 and h ⊥ hξ ⊥ hF , then for all enabled
                                                                                          1
          actions a ∈ Act(C, (s, h ⋆ hξ ⋆ hF )) we do not have C, (s, h ⋆ hξ ⋆ hF ) −
                                                                                    → abort; and
                                                                                          a
     4. if n > 0 and for all hξ , hF , C ′ , s and h, with ξ(s, hξ ) = 1, and h ⊥ hξ ⊥ hF , and
                               1
                               → C ′ , (s′ , h′ ), then there exists h′′ and h′ξ such that h′ = h′′ ⋆ h′ξ ⋆ hF
          C, (s, h ⋆ hξ ⋆ hF ) −
                               a
        and ξ(s′ , h′ξ ) = 1 and safen−1 (C ′ , s′ , h′′ , ξ, φ).
     For qualitative φ, ψ and ξ, we say that ξ |= {ψ} C {φ} holds if and only if for all stack/heap
     pairs s, h the statement ψ(s, h) = 1 ⇒ ∀n ∈ N. safen (C, s, h, ξ, φ) holds.

        A program C is framing enabled2 if we can always extend the heap without changing
     the behaviour of C.

     ▶ Definition 4.2 (Framing Enabledness). A non-probabilistic program C is framing enabled
     if for all heaps hF with h ⊥ hF and all enabled actions a ∈ Act(C, (s, h ⋆ hF )), it holds: if
                 1                                            1
     C, (s, h) −→ C ′ , (s′ , h′ ), then also C, (s, h ⋆ hF ) −
                                                              → C ′ , (s′ , h′ ⋆ hF ).
                 a                                            a

          The next theorem states that wrlp is a conservative extension of safe.

     ▶ Theorem 4.1 (Conservative Extension of Concurrent Separation Logic). For a framing-
     enabled non-probabilistic program C and qualitative expectations φ, ψ and ξ, we have

          φ ≤ wrlpJCK (ψ | ξ)       iff   ξ |= {φ} C {ψ} .

     Proof. See Appendix B.                                                                                 ◀

     We define wrlp inductively by means of a number of inference rules. We do not use classic
     Hoare triples due to difficulties arising when interpreting a wrlp statement forward. These
     difficulties are due to Jones’s counterexample [28, p. 135]: Given the constant preexpecta-
     tion 0.5 and the program C : { x := 0 } [ 0.5 ] { x := 1 }, what is the postexpectation? Two
     possible answers are 0.5 = wlpJCK ([x = 0]) and 0.5 = wlpJCK ([x = 1]), but a combination


     2
         Indeed every non-probabilistic chpGCL program is framing enabled (cf. Theorem D.3).
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                                11


                                              term                             Y ≤ X [x := e]
                   X ≤ wrlpJ ↓ K (X | ξ)                                                              assign
                                                                         Y ≤ wrlpJx := eK (X | ξ)
    Y ≤ supv∈Z [e 7→ v] ⋆ ([e 7→ v] −−⋆ X [x := v])                   Y ≤ [e 7→ − ] ⋆ ( e 7→ e′ −−⋆ X)
                                                                                              
                                                    look
           Y ≤ wrlpJx := < e >K (X | ξ)                                                                  mut
                                                                       Y ≤ wrlpJ< e > := e′ K (X | ξ)
      Y ≤ inf v∈Z [v 7→ e1 , . . . , en ] −−⋆ X [x := v]
                                                         alloc               Y ≤ X ⋆ [x 7→ − ]
       Y ≤ wrlpJx := new (e1 , . . . , en )K (X | ξ)                                                disp
                                                                          Y ≤ wrlpJfree(x)K (X | ξ)

   Figure 5 Proof rules for wrlp for basic commands

                                   X ≤ wrlpJC1 K (Y | ξ)  Y ≤ wrlpJC2 K (Z | ξ)
                                                                                seq
                                            X ≤ wrlpJC1 ; C2 K (Z | ξ)
                                  X1 ≤ wrlpJC1 K (Y | ξ)      X2 ≤ wrlpJC2 K (Y | ξ)
                                                                                             if
                            [b] · X1 + [¬b] · X2 ≤ wrlpJif ( b ) { C1 } else { C2 }K (Y | ξ)
            I ≤ [b] · X + [¬b] · Y  X ≤ wrlpJCK (I | ξ)                                                 div
                                                        while               X ≤ wrlpJdivergeK (Y | ξ)
                  I ≤ wrlpJwhile ( b ) { C }K (Y | ξ)

    X1 ≤ wrlpJC1 K (Y | ξ)      X2 ≤ wrlpJC2 K (Y | ξ)                         X ≤ wrlpJCK (Y ⋆ ξ | [emp])
                                                               p-choice                                      atomic
 ep · X1 + (1 − ep ) · X2 ≤ wrlpJ{ C1 } [ ep ] { C2 }K (Y | ξ)                X ≤ wrlpJatomic { C }K (Y | ξ)

                                              X ≤ wrlpJCK (Y | ξ ⋆ π)
                                                                         share
                                             X ⋆ π ≤ wrlpJCK (Y ⋆ π | ξ)
 X1 ≤ wrlpJC1 K (Y1 | ξ)         X2 ≤ wrlpJC2 K (Y2 | ξ)  ∀i ∈ {1, 2} Write(Ci ) ∩ Vars (C3−i , Y3−i , ξ) = ∅
                                                                                                              concur
                                    X1 ⋆ X2 ≤ wrlpJ C1 ∥ C2 K (Y1 ⋆ Y2 | ξ)

   Figure 6 Proof rules for wrlp for control-flow commands


of both is not possible. For this reason, we highlight the backwards interpretation of our
judgements by writing them as X ≤ wrlpJCK (Y | ξ), where X is a (lower bound for the
weakest liberal) preexpectation, C is the program, Y is the postexpectation and ξ is the
resource invariant.
    For basic commands, as shown in Figure 5, we can just re-use the QSL proof rules for
weakest liberal preexpectations (wlp) of non-concurrent programs, as given in [5]. However,
for wrlp these proof rules only allow lower bounding the preexpectation since we do not want
to reason about the resource invariant if not necessary.
    For commands handling control flow, as shown in Figure 6, we use mostly standard rules.
Atomic regions regain access to the resource invariant. The share rule allows us to enrich the
resource invariant. The rule for concurrency enforces that only local variables or read-only
variables are used in each thread. One could as well allow shared variables that are owned
by the resource invariant. However, for the sake of brevity we do not include this here.
    We also introduce several proof rules that make reasoning easier, see Figure 7. A program
is almost surely terminating with respect to a set of schedulers if the program terminates
with probability one for every initial state and every scheduler in this set. Even though there
is a plethora of work on almost-sure termination for (sequential) probabilistic programs (cf.
[24] for an overview), techniques for checking almost-sure termination in a concurrent setting
are sparse [21, 22, 35, 51]. Here, interpreting probabilistic choice as non-determinism and
proving sure termination instead using techniques such as [15, 48] is an alternative.
    The first rule in Figure 7 uses superlinearity for wlp to split a given postexpectation into
a sum of smaller postexpectations, for which proving a lower bound on the preexpectation
might be easier. Here we use addition instead of maximum since addition is usually more
precise. We only allow the use of superlinearity for wlp (and not for wrlp) because we need
12   Towards Concurrent Quantitative Separation Logic


                   X ′ ≤ wlpS JCK (X)      Y ′ ≤ wlpS JCK (Y )     C is AST w.r.t. S    a ∈ R≥0
                                                                                                  superlin
                                         a · X ′ + Y ′ ≤ wlpS JCK (a · X + Y )
            X ≤ wrlpJCK (Y | [emp])                   X ≤ wrlpJCK (Y | ξ)  Write(C) ∩ Vars (Z) = ∅
                                        wlp-wrlp                                                   frame
                X ≤ wlpS JCK (Y )                             X ⋆ Z ≤ wrlpJCK (Y ⋆ Z | ξ)

                         X ⋆ ξ ≤ wrlpJCK (Y ⋆ ξ | [emp])       C is a terminating atom
                                                                                          atom
                                              X ≤ wrlpJCK (Y | ξ)
                             X ≤ X′        X ′ ≤ wrlpJCK Y ′ | ξ       Y′ ≤Y
                                                                 
                                                                                 monotonic
                                            X ≤ wrlpJCK (Y | ξ)
                                                           X ′ ≤ wrlpJCK Y ′ | ξ
                                                                                  
                                X ≤ wrlpJCK (Y | ξ)
                                                                                      max
                                 max X, X ′ ≤ wrlpJCK max Y, Y ′ | ξ
                                                                             

                                       X ′ ≤ wrlpJCK Y ′ | ξ
                                                             
             X ≤ wrlpJCK (Y | ξ)                                   ξ precise      C is not probabilistic
                                                                                                         min
                                  min X, X ′ ≤ wrlpJCK min Y, Y ′ | ξ
                                                                            

                                    X ′ ≤ wrlpJCK Y ′ | ξ
                                                          
            X ≤ wrlpJCK (Y | ξ)                                 ξ precise     Write(C) ∩ Vars (e) = ∅
                                                                                                         convex
                           e · X + (1 − e) · X ′ ≤ wrlpJCK e · Y + (1 − E) · Y ′ | ξ
                                                                                     


        Figure 7 Auxiliary proof rules for wrlp


     a restricted set of schedulers to enforce fairness conditions. Fairness conditions are required
     to reason about termination for concurrent programs with some sort of blocking behaviour.
     We are then able to transform wlp into wrlp by using the wlp-wrlp rule. Whether wrlp can
     also be defined with fairness conditions in mind and thus applying superlinearity directly
     on wrlp, is an open question. The frame rule is of central importance to the Separation
     Logic approach, as it supports local reasoning about only the relevant part of the heap [45].
     The atom rule can be used similarly to the rule for atomic regions. Monotonicity is the
     quantitative version of the rule of consequence and is used to reduce and increase the post-
     and preexpectation respectively. The max, min and convex rules eliminate max, min and
     convex sum operations, respectively. The min and convex rule require preciseness of the
     resource invariant – similarly to how [52] required preciseness for the conjunction rule. An
     expectation is precise if for any stack there is at most one heap for which the expectation is
     not zero. For the min rule, this is not surprising as the minimum behaves like conjunction
     in case of qualitative expectations. Requiring preciseness also for the convex rule is due to
     the missing superlinearity of the separating multiplication for non-precise expectations.
     ▶ Theorem 4.2 (Soundness of proof rules). For every proof rule in Figures 5–7 it holds that
     if their premises hold, the conclusion holds as well.
     Proof. See Appendix E.                                                                                       ◀

     ▶ Example 4.2. We are now able to establish the lower bound computed in Example 3.6
     using the proof rules. Instead of constructing a proof tree by composing inference rules, we
     annotate program locations with their respective pre- and postexpectations. The interpreta-
     tion is standard; for preexpectation X, postexpectation Y , resource invariant ξ and program
     C:
         ( X | ξ
        C                   iff     X ≤ wrlpJCK (Y | ξ)
         ( Y | ξ
     Proofs in this style should only be read backwards from bottom to top. They will not
     include applications of the proof rules for atomic programs and of the share rule as this
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                          13


may lead to incorrect interpretations. For our example, we use the resource invariant
ξ = max { [r 7→ 0], [r 7→ −1] }, which we guessed by collecting all possible values stored
in location r during executions yielding our postexpectation. We assume that the memory
of the initial heap h only contains a single location r with value −1. This assumption is
reflected by the resource invariant and will only allow us to reason about executions with
such an initial heap. The other possible value for the location r is 0, since the left program
may mutate the heap. Indeed, there are also executions where the value of location r is 1.
For these, the program only terminates in states violating the postexpectation [y = 0]. We
can further show:

     ( 0.5 ⋆ 1 | ξ
                                             ( 1 | ξ
     ( 0.5 | ξ                               y := < r > ;
     { < r > := 0 } [ 0.5 ] { < r > := 1 }   ( max { [y = 0], [y = −1] } | ξ
     ( 1 | ξ                                 while ( y = −1 ) { y := < r > } ;
                                             ( [y = 0] | ξ
     ( 1 ⋆ [y = 0] | ξ



To handle concurrency, we separate our postexpectation into the expectation 1 for the left
program and the expectation [y = 0] for the right program. The left program includes a
probabilistic choice, for which we use the atom rule to infer that the preexpectation is 1
in the left branch of the probabilistic choice, as the resource invariant allows mutating the
value of location r to 1 and the resource invariant can be re-established since we can lower
bound all possible values for the location r that are not −1 or 0 to zero. Moreover, we lower
bound the right branch of the probabilistic choice by zero, because zero is a lower bound of
any expectation. The right program iterates until the value of location r has been mutated.
Our resource invariant contains all possible values that the program can expect here. For
the loop invariant, we connect all possible values of y using a disjunction over 0 and −1, as
we disregard executions where y = 1. Lastly, we can apply the loop invariant to the lookup
of r and since this matches our resource invariant, the resulting preexpectation is one.
    Thus, we have established that 0.5 ≤ wrlpJCK ([y = 0] | ξ). Using the share rule we
can further infer that 0.5 ⋆ ξ ≤ wrlpJCK ([y = 0] ⋆ ξ | [emp]). Lastly, we can clean up the
statement using monotonicity and the wlp-wrlp rule to obtain 0.5 ⋆ ξ ≤ wlpJCK ([y = 0]). For
details on the probabilistic choice and the loop invariant, we refer to Appendix F.1.


 5     Example: A Producer, a Consumer and a Lossy Channel
A producer-consumer system is often used when presenting verification techniques for concur-
rent programs. We continue this tradition, extending this example by probabilistic elements,
see Figure 8. Video and audio streaming is an example for such a system, where data losses
are acceptable if they do not exceed a certain limit. Moreover, by enriching the resource
invariant with a predicate defining an appropriate data structure, this example can be used
as a template to reason about systems communicating using a shared data structure. We
consider a producer that randomly generates data (1 or 2) and stores it in an array of size
k indexed by z1 . The data has to be transferred to a consumer. However, the consumer
does not have direct access to the array maintained by the producer. Instead a third party,
14   Towards Concurrent Quantitative Separation Logic



       l := 0 ;
       y1 , y2 , y3 := k ;

                                                    while ( y2 ≥ 0 ) {
                                                        x2 := < z1 + y2 > ;           while ( y3 ≥ 0 ) {
        while ( y1 ≥ 0 ) {                              if ( x2 ̸= 0 ) {                  x3 := < z2 + y3 > ;
            { x1 := 1 } [ 0.5 ] { x1 := 2 } ;                 {< z2 + y2 > := x2 }        if ( x3 ̸= 0 ) {
            < z1 + y1 > := x1 ;                             [p]                               if ( x3 ̸= −1 ) {l := l + 1} ;
            y1 := y1 − 1                                      {< z2 + y2 > := −1} ;           y3 := y3 − 1
        }                                                   y2 := y2 − 1                  }
                                                        }                             }
                                                    }



         Figure 8 A program consisting of the tree threads: a producer (left), a consumer (right) and
     lossy channel (middle) for communication between the prior threads.


     the lossy channel, transfers data from the array maintained by the producer to a different
     k-sized array that is indexed by z2 , and that can be accessed by the consumer. However,
     the channel is not reliable. With a probability of 1 − p, it loses a value and instead stores
     invalid data (encoded as −1) at the respective array position. The consumer discards invalid
     data and counts in l how many valid elements it received until all array elements have been
     attempted to be transmitted once. For the sake of brevity, we leave out the allocation of
     the array index z1 and z2 . Instead, we assume already allocated arrays as input.
         We are interested in the probability that the data of a certain set of locations has been
     successfully transmitted. If we additionally prove that the program is almost surely termin-
     ating for some reasonable set of fair schedulers, we can use superlinearity to prove lower
     bounds of probabilities for even more complex postconditions, e.g. the probability that at
     least half of the data have been transmitted successfully. Indeed, the program is almost
     surely terminating under a fairness condition. We denote the set of locations that we want
     to be successfully transmitted as J. For the resource invariant, we use a big separating
     multiplication. Its semantics is as expected: for a stack s, we connect all choices for the
     index variable with regular separating multiplications. The resource invariant describes the
     values we want to tolerate for every entry in both arrays. We join the tolerated values
     by a disjunction (which is the maximum in our case). We now use the resource invariant,
     parametrised on the set J as
                                                                               !
        ξJ        =              ⋆         max { [z1 + i 7→ 0] , [z1 + i 7→ 1] , [z1 + i 7→ 2] }
                             i∈{0,...,k}
                                                                                                             !
                      ⋆           ⋆          max { [z2 + i 7→ 0] , [z2 + i 7→ 1] , [z2 + i 7→ 2] }
                             i∈{0,...,k}∩J
                                                                                          !
                      ⋆           ⋆          max { [z2 + i 7→ 0] , [z2 + i 7→ −1] }           .
                             i∈{0,...,k}\J


        Next, we can use the resource invariant to prove an invariant for each of the three
     concurrent programs. The corresponding calculations can be found in Appendix F.2. Let
     C1 be the producer, C2 the channel and C3 the consumer. For the producer program C1
     we can prove the invariant I1 = 1 with respect to the postexpectation 1, for the channel
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                    15


C2 we can prove the invariant I2 = [0 ≤ y2 ≤ k] · p|{0,...,y2 }∩J| · (1 − p)|{0,...,y2 }\J| + [y2 < 0]
with respect to the postexpectation 1, and for the consumer program C3 we can prove the
invariant I3 = [0 ≤ y3 ≤ k] · [l = |J ∩ {0, . . . , y3 }|] + [y3 < 0] · [l = |J|] with respect to the
postexpectation [l = |J|]. Using all three invariants, we can now lower bound the probability
that l = |J| holds after the execution of the whole program C in Figure 8:
     ( [0 ≤ k] · p|{0,...,k}∩J| · (1 − p)|{0,...,k}\J| | ξJ
     l := 0 ;
     y1 , y2 , y3 := k ;
     ( I1 ⋆ I 2 ⋆ I 3 | ξJ
     C1 ∥ C2 ∥ C3
     ( 1 ⋆ 1 ⋆ [l = |J|] | ξJ
Here, we first use the concurrency rule to place the postexpectation [l = |J|] into a separ-
ating context, thus covering all three programs. The resulting preexpectation is indeed
the separating multiplication of the respective invariants. By applying the assignment
rules to the first two rows, we finally get the result for a lower bound of the weakest
resource-safe preexpectation with respect to resource invariant ξJ . Thus, the lower bound
([0 ≤ k] · p|{0,...,k}∩J| · (1 − p)|{0,...,k}\J| ) ⋆ ξJ ≤ wlpS JCK ([l = |J|] ⋆ ξJ ) also holds. We also
show in Appendix F.2 how to prove the lower bound of more difficult postexpectations using
superlinearity.

 6       Conclusion and Future Work
Using resource invariants from Concurrent Separation Logic [52] together with quantitative
reasoning from Quantitative Separation Logic [5] allows us to reason about lower-bound
probabilities of realizing a postcondition. In our technique, probability mass is local to
the thread. This insight gave rise to only allow qualitative expectations in the model of
the environment. By this, the resource invariant only describes shared memory and lacks
semantics for global probability mass.
    However, we may favour a probabilistic model of the environment – for example, if the
environment is a black box and only statistic information about its possible behaviours is
available. More research is required for logics allowing probabilistic specifications in the en-
vironment description, especially logics allowing quantitative resource invariants. Moreover,
we are only able to verify lower bounds due to the concurrent rule. We conjecture that a
logic for upper bounds requires different, unknown separation connectives.

       References
 1     Christel Baier, Frank Ciesinski, and Markus Grosser. PROBMELA: a modeling language for
       communicating probabilistic processes. In MEMOCODE, pages 57–66. IEEE, 2004.
 2     Christel Baier and Joost-Pieter Katoen. Principles of Model Checking. The MIT Press, 2008.
 3     Gilles Barthe, Benjamin Grégoire, and Santiago Zanella Béguelin. Probabilistic relational
       Hoare logics for computer-aided security proofs. In MPC, pages 1–6. Springer, 2012.
 4     Kevin Batz, Ira Fesefeldt, Marvin Jansen, Joost-Pieter Katoen, Florian Keßler, Christoph
       Matheja, and Thomas Noll. Foundations for entailment checking in quantitative separation
       logic. In ESOP, pages 57–84. Springer, 2022.
 5     Kevin Batz, Benjamin Lucien Kaminski, Joost-Pieter Katoen, Christoph Matheja, and
       Thomas Noll. Quantitative separation logic: a logic for reasoning about probabilistic pointer
       programs. Proc. ACM Program. Lang., 3(POPL):34:1–34:29, 2019.
16   Towards Concurrent Quantitative Separation Logic


      6   Josh Berdine, Cristiano Calcagno, Byron Cook, Dino Distefano, Peter W. O’Hearn, Thomas
          Wies, and Hongseok Yang. Shape analysis for composite data structures. In CAV, pages
          178–192. Springer, 2007.
      7   Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. Smallfoot: Modular automatic
          assertion checking with separation logic. In FMCO, pages 115–137. Springer, 2005.
      8   Burton H. Bloom. Space/time trade-offs in hash coding with allowable errors. Commun.
          ACM, 13(7):422–426, 1970.
      9   Stephen Brookes and Peter W. O’Hearn. Concurrent separation logic. ACM SIGLOG News,
          3(3):47–65, 2016.
     10   Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. Compositional
          shape analysis by means of bi-abduction. J. ACM, 58(6):26:1–26:66, 2011.
     11   Michael Carbin, Sasa Misailovic, and Martin C. Rinard. Verifying quantitative reliability for
          programs that execute on unreliable hardware. Commun. ACM, 59(8):83–91, 2016.
     12   Edsger W. Dijkstra. A Discipline of Programming. Prentice-Hall, 1976.
     13   Thomas Dinsdale-Young, Lars Birkedal, Philippa Gardner, Matthew Parkinson, and Hong-
          seok Yang. Views: Compositional reasoning for concurrent programs. In POPL, pages 287–
          300. ACM, 2013.
     14   Thomas Dinsdale-Young, Mike Dodds, Philippa Gardner, Matthew J. Parkinson, and Viktor
          Vafeiadis. Concurrent abstract predicates. In ECOOP, pages 504–528. Springer, 2010.
     15   Emanuele D’Osualdo, Julian Sutherland, Azadeh Farzan, and Philippa Gardner. TaDA live:
          Compositional reasoning for termination of fine-grained concurrent programs. ACM Trans.
          Program. Lang. Syst., 43(4), 2021.
     16   Keir Fraser. Practical lock-freedom. Technical Report UCAM-CL-TR-579, University of
          Cambridge, Computer Laboratory, 2004.
     17   Ming Fu, Yong Li, Xinyu Feng, Zhong Shao, and Yu Zhang. Reasoning about optimistic
          concurrency using a program logic for history. In CONCUR, pages 388–402. Springer, 2010.
     18   Andrew D. Gordon, Thomas A. Henzinger, Aditya V. Nori, and Sriram K. Rajamani. Prob-
          abilistic programming. In FOSE, pages 167–181. ACM, 2014.
     19   Alexey Gotsman, Josh Berdine, Byron Cook, and Mooly Sagiv. Thread-modular shape ana-
          lysis. In PLDI, pages 266–277. ACM, 2007.
     20   Friedrich Gretz, Joost-Pieter Katoen, and Annabelle McIver. Operational versus weakest
          pre-expectation semantics for the probabilistic guarded command language. Performance
          Evaluation, 73:110–132, 2014.
     21   Sergiu Hart and Micha Sharir. Concurrent probabilistic programs, or: How to schedule if you
          must. SIAM J. Comput., 14(4):991–1012, 1985.
     22   Sergiu Hart, Micha Sharir, and Amir Pnueli. Termination of probabilistic concurrent programs.
          ACM Trans. Program. Lang. Syst., 5(3):356–380, 1983.
     23   Max P. L. Haslbeck. Verified Quantitative Analysis of Imperative Algorithms. PhD thesis,
          Technical University of Munich, Germany, 2021.
     24   Mingzhang Huang, Hongfei Fu, Krishnendu Chatterjee, and Amir Kafshdar Goharshady. Mod-
          ular verification for almost-sure termination of probabilistic programs. Proc. ACM Program.
          Lang., 3(OOPSLA):129:1–129:29, 2019.
     25   Samin S. Ishtiaq and Peter W. O’Hearn. BI as an assertion language for mutable data
          structures. In POPL, pages 14–26. ACM, 2001.
     26   Kenneth E. Iverson. A Programming Language. John Wiley & Sons, Inc., USA, 1962.
     27   Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank
          Piessens. Verifast: A powerful, sound, predictable, fast verifier for C and Java. In NFM,
          pages 41–55. Springer, 2011.
     28   Claire Jones. Probabilistic Non-Determinism. PhD thesis, University of Edinburgh, 1992.
     29   Cliff B. Jones. Tentative steps toward a development method for interfering programs. ACM
          Trans. Program. Lang. Syst., 5(4):596–619, 1983.
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                              17


30   Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and Derek
     Dreyer. Iris from the ground up: A modular foundation for higher-order concurrent separation
     logic. J. Funct. Program., 28:e20, 2018.
31   Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal,
     and Derek Dreyer. Iris: Monoids and invariants as an orthogonal basis for concurrent reason-
     ing. In POPL, pages 637–650. ACM, 2015.
32   Benjamin L. Kaminski, Joost-Pieter Katoen, Christoph Matheja, and Federico Olmedo. Weak-
     est precondition reasoning for expected runtimes of randomized algorithms. J. ACM, 65(5),
     2018.
33   Dexter Kozen. Semantics of probabilistic programs. In FOCS, pages 101–114. IEEE Computer
     Society, 1979.
34   Dexter Kozen. A probabilistic PDL. In STOC, pages 291–297. ACM, 1983.
35   Ondrej Lengál, Anthony Widjaja Lin, Rupak Majumdar, and Philipp Rümmer. Fair termina-
     tion for parameterized probabilistic concurrent systems. In TACAS, pages 499–517. Springer,
     2017.
36   Christoph Matheja. Automated Reasoning and Randomization in Separation Logic. PhD
     thesis, RWTH Aachen University, Germany, 2020.
37   Annabelle McIver and Carroll Morgan. Partial correctness for probabilistic demonic programs.
     Theoretical Computer Science, 266(1):513–541, 2001.
38   Annabelle McIver and Carroll Morgan. Abstraction, Refinement and Proof for Probabilistic
     Systems. Monographs in Computer Science. Springer, 2005.
39   Annabelle McIver, Tahiry Rabehaja, and Georg Struth. Probabilistic rely-guarantee calculus.
     Theoretical Computer Science, 655:120–134, 2016.
40   Michael Mitzenmacher and Eli Upfal. Probability and Computing: Randomized Algorithms
     and Probabilistic Analysis. Cambridge University Press, 2005.
41   Peter Müller, Malte Schwerhoff, and Alexander J. Summers. Viper: A verification infrastruc-
     ture for permission-based reasoning. In Dependable Software Systems Engineering, volume 50
     of NATO Science for Peace and Security Series - D: Information and Communication Secur-
     ity, pages 104–125. IOS Press, 2017.
42   Aleksandar Nanevski, Ruy Ley-Wild, Ilya Sergey, and Germán Andrés Delbianco. Communic-
     ating state transition systems for fine-grained concurrent resources. In ESOP, pages 290–310.
     Springer, 2014.
43   Van Chan Ngo, Quentin Carbonneaux, and Jan Hoffmann. Bounded expectations: Resource
     analysis for probabilistic programs. SIGPLAN Not., 53(4):496–512, 2018.
44   Peter W. O’Hearn. Resources, concurrency, and local reasoning. Theoretical Computer Sci-
     ence, 375(1):271–307, 2007.
45   Peter W. O’Hearn. Separation logic. Commun. ACM, 62(2):86–95, 2019.
46   Ruzica Piskac, Thomas Wies, and Damien Zufferey. Automating separation logic using SMT.
     In CAV, pages 773–789. Springer, 2013.
47   William Pugh. Skip lists: A probabilistic alternative to balanced trees. Commun. ACM,
     33(6):668–676, 1990.
48   Tobias Reinhard and Bart Jacobs. Ghost signals: Verifying termination of busy waiting. In
     CAV, pages 27–50. Springer, 2021.
49   John C. Reynolds. Separation logic: A logic for shared mutable data structures. In LICS,
     pages 55–74. IEEE Computer Society, 2002.
50   Joseph Tassarotti and Robert Harper. A separation logic for concurrent randomized programs.
     Proc. ACM Program. Lang., 3(POPL):64:1–64:30, 2019.
51   Michael L. Tiomkin. Probabilistic termination versus fair termination. Theor. Comput. Sci.,
     66(3):333–340, 1989.
52   Viktor Vafeiadis. Concurrent separation logic and operational semantics. Electronic Notes in
     Theoretical Computer Science, 276:335–351, 2011.
18   Towards Concurrent Quantitative Separation Logic


      A       Quantitative Separation Logic
     ▶ Lemma A.1 (Various Analysis Statements). For sets A ⊆ A′ , B ⊆ B ′ , countable set C ⊆ C ′ ,
     non-empty set D ⊆ D′ and real-valued functions f : A′ × B ′ → [0, 1], g : C ′ × D′ → [0, 1] we
     have
                                    [
         inf {inf Ab | b ∈ B} = inf   {Ab | b ∈ B}                                               (4)
          inf {inf {f (a, b) | a ∈ A} | b ∈ B} = inf {inf {f (a, b) | b ∈ B} a ∈ A}                        (5)
          sup {inf {f (a, b) | a ∈ A} | b ∈ B} ≤ inf {sup {f (a, b) | b ∈ B} | a ∈ A}                      (6)
          X                                         nX                             o
              [inf {g(c, d) | d ∈ D} | c ∈ C] ≤ inf      [g(c, d) | c ∈ C] | d ∈ D                         (7)

     Proof. Straightforward using real-valued analysis.                                                     ◀

     ▶ Lemma A.2 (Properties of Separating Multiplication). For expectations X, Y, Z and qualit-
     ative expectations φ:

          X ⋆ (Y ⋆ Z)       =       (X ⋆ Y ) ⋆ Z                            (Associativity)                (8)
          X ⋆ [emp]     =       [emp] ⋆ X = X                               (Neutrality)                   (9)
          X ⋆Y     =     Y ⋆X                                               (Commutativity)               (10)
          X≤Y      implies          X ⋆Z ≤Y ⋆Z                              (Monotonicity)                (11)
          X ⋆ max { Y, Z }          =        max { X ⋆ Y , X ⋆ Z }          (Dist. with max)              (12)
          φ ⋆ (Y · Z)   ≤       (φ ⋆ Y ) · (φ ⋆ Z)                          (Subdist. with mult.)         (13)
          X ⋆ (Y + Z)         ≤ (X ⋆ Y ) + (X ⋆ Z)                          (Subdist. with plus)          (14)

     Proof. See [36, Theorem 6.14, Theorem 6.15, Theorem 6.16].                                             ◀

     ▶ Lemma A.3 (Properties of (Guarded) Magic Wand). For expectations X, Y, Z and qualit-
     ative expectations φ:

          X ⋆φ≤Y        iff     X ≤ φ −−⋆ Y                                 (Adjointness)                 (15)
          φ ⋆ (φ −−⋆ X)         ≤        X                                  (Modus Ponens)                (16)
          X    ≤    φ −−⋆ (φ ⋆ X)                                                                         (17)
          X≤Y      implies          φ −−⋆ X ≤ φ −−⋆ Y                       (Monotonicity)                (18)
          φ −−⋆ max { X, Y }             ≥     max { φ −−⋆ X, φ −−⋆ Y }     (Superdist. with max)         (19)
          φ −−⋆ min { X, Y }             =     min { φ −−⋆ X, φ −−⋆ Y }     (Dist. with min)              (20)
          φ −−⋆ (X + Y )        ≥        (φ −−⋆ X) + (φ −−⋆ Y )             (Superdist. with plus)        (21)
          φ −−⋆ (X · Y )        ≥       (φ −−⋆ X) · (φ −−⋆ Y )              (Superdist. with mult.)       (22)
          φ −−⋆ (ψ −−⋆ X)            =       (φ ⋆ ψ) −−⋆ X                  (Combining magic wands) (23)
          φ −−⋆ (X ⋆ Y ) ≥ (φ −−⋆ X) ⋆ Y                                                                  (24)

     Proof. See [36, Theorem 6.18, Theorem 6.19, Theorem 6.20, Theorem 6.21]. Theorem 6.21
     in [36] has a small typo for Statement (22). We give a small proof for this here instead:

                   φ ⋆ (φ −−⋆ X) ≤ X               and φ ⋆ (φ −−⋆ Y ) ≤ Y                     (Statement (16))
          implies (φ ⋆ (φ −−⋆ X)) · (φ ⋆ (φ −−⋆ Y )) ≤ X · Y                (Monotoncitiy of multiplication)
          implies φ ⋆ ((φ −−⋆ X) · (φ −−⋆ Y )) ≤ X · Y                                        (Statement (13))
          implies (φ −−⋆ X) · (φ −−⋆ Y ) ≤ φ −−⋆ (X · Y )                                     (Statement (15))
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                   19


For Statement (17) we give the proof:

               X≤X
     implies X ⋆ ξ ≤ X ⋆ ξ                                                           (Statement (11))
     implies X ≤ ξ −−⋆ (X ⋆ ξ)                                                       (Statement (15))

For Statement (23) we give the proof:

        (φ −−⋆ (ψ −−⋆ X)) (s, h)
     = inf {inf {X(s, h′′ ) | ψ(s, hψ ) = 1, h′′ = h′ ⋆ hψ } | φ(s, hφ ) = 1, h′ = h ⋆ hφ }
                                                                                   (Definition of −−⋆ )
     = inf {X(s, h′′ ) | ψ(s, hψ ) = 1, φ(s, hφ ) = 1, h′′ = h ⋆ hφ ⋆ hψ }            (Statement (4))
                     ′′                                ′′
     = inf {X(s, h ) | (ψ ⋆ φ)(s, hψ ⋆ hφ ) = 1, h = h ⋆ hφ ⋆ hψ }
                                                         (Definition of separation conjunction)
     = ((φ ⋆ ψ) −−⋆ X) (s, h)                                                      (Definition of −−⋆ )

For Statement (24) we give the proof:

       φ −−⋆ (X ⋆ Y )
     = inf{sup{X(s, h1 ) · Y (s, h2 ) | h1 ⋆ h2 = h ⋆ hφ } | φ(s, hφ ) = 1, hφ ⊥ h}
                                                                          (Definition of −−⋆ and ⋆)
     ≥ inf{sup{X(s, h1 ⋆ hφ ) · Y (s, h2 ) | h1 ⋆ h2 = h, hφ ⊥ h1 } | φ(s, hφ ) = 1, hφ ⊥ h}
                                                                       (Decreasing the supremum)
     ≥ sup{inf{X(s, h1 ⋆ hφ ) · Y (s, h2 ) | φ(s, hφ ), hφ ⊥ h1 } | h1 ⋆ h2 = h}
                                                      (Statement (6) and decreasing the infimum)
     = sup{inf{X(s, h1 ⋆ hφ ) | φ(s, hφ ), hφ ⊥ h1 } · Y (s, h2 ) | h1 ⋆ h2 = h}
                                                                     (Factorisation with constants)
     = (φ −−⋆ X) ⋆ Y                                                         (Definition of −−⋆ and ⋆)

                                                                                                    ◀

▶ Definition A.4. An expectation X is precise iff

     ∀(s, h). |{h′ ∈ Heaps | ∃h′′ : h′ ⋆ h′′ = h and X(s, h′ ) > 0}| ≤ 1 .

▶ Lemma A.5 (Properties for Precise Expectations). For a precise expectation X and a precise
qualitative expectation φ:

     X ⋆ min { Y, Z }         =     min { X ⋆ Y , X ⋆ Z }           (Dist. with min)              (25)
     X ⋆ (Y + Z)          =    (X ⋆ Y ) + (X ⋆ Z)                   (Dist. with plus)             (26)
     φ ⋆ (Y · Z)     =        (φ ⋆ Y ) · (φ ⋆ Z)                    (Dist. with mult.)            (27)

Proof. See [36, Theorem 6.25]                                                                       ◀

 B       Proofs for the Weakest Safe Liberal Preexpectation
▶ Lemma B.1 (Monotonicity of step). For all programs C and t, t′ : C → E≤1 we have

     t(C) ≤ t′ (C)        implies   stepJCK (t) ≤ stepJCK (t′ ) .
20   Towards Concurrent Quantitative Separation Logic


     Proof. This follows directly by monotonicity of multiplication with probabilities, countable
     sums and infima.                                                                          ◀

     ▶ Lemma B.2 (0 − 1 Bounds on wrlp). For all programs C, expectation X and qualitative
     expectation ξ we have

        0 ≤ wrlpJCK (X | ξ) ≤ 1 .

     Proof. If 0 ≤ wrlpn JCK (X | ξ) ≤ 1, then the statement holds as well. We prove this new
     statement by induction on n.
         For the base case n = 0 we have 0 ≤ wrlp0 JCK (X | ξ) = 1.
         Now we assume an arbitrary but fixed n such that 0 ≤ wrlpn JCK (X | ξ) ≤ 1 for all C, X
     and ξ.
         For the induction step, if C = ↓ the statement holds again trivially since expectations
     are also 0 − 1 bounded. Thus, we assume that C ̸= ↓ . By the induction hypothesis
     0 ≤ wrlpn JC ′ K (X | ξ) ≤ 1, thus also 0 ≤ wrlpn JC ′ K (X | ξ) ⋆ ξ ≤ 1 for all C ′ . If t is 0 − 1
     bounded, then the step function is also 0 − 1 bounded:
                                  Xh                                                         i
                                                                             p
         stepJCK (t) (s, h) = inf      p · t(C ′ , (s′ , h′ )) | C, (s, h) −→ C ′ , (s′ , h′ )
                                                                             a
                                                          
                                   a ∈ Act(C, (s, h))
                                  Xh                                           i
                                                               p
                            ≤ inf      p · 1 | C, (s, h) −    → C ′ , (s′ , h′ )
                                                               a
                                                          
                                   a ∈ Act(C, (s, h))                                           (Lemma B.1)

                           ≤ inf {1 | a ∈ Act(C, (s, h))}                                            (MDP property)
                           =1


                                   Xh                                                           i
                                                                            p
        stepJCK (t) (s, h) = inf        p · t(C ′ , (s′ , h′ )) | C, (s, h) −
                                                                            → C ′ , (s′ , h′ )
                                                                            a
                                                           
                                    a ∈ Act(C, (s, h))
                                   Xh                                      i
                                                          p
                           ≥ inf                          → C ′ , (s′ , h′ )
                                        p · 0 | C, (s, h) −
                                                          a
                                                        
                                    a ∈ Act(C, (s, h))                                                 (Lemma B.1)

                           ≥ inf {0 | a ∈ Act(C, (s, h))}                                        (0 is zero element)
                           =0

     Lastly, the quantitative magic wand is the infimum of all applicable values for the second
     argument, thus also 0 − 1 bounded if their second argument is 0 − 1 bounded.             ◀

     ▶ Lemma B.3 (Antitonicity of wrlpn w.r.t. n). For natural numbers n ≤ m we have

        wrlpn JCK (X | ξ) ≥ wrlpm JCK (X | ξ) .
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                      21


Proof. We instead prove by induction on n the equivalent statement that

    wrlpn JCK (X | ξ) ≥ wrlpn+1 JCK (X | ξ) .

    For the base case n = 0 we have wrlp0 JCK (X | ξ) = 1, thus the statement holds trivially
by Lemma B.2.
    Now for the induction hypothesis, we assume that for some fixed but arbitrary n we have
wrlpn JCK (X | ξ) ≥ wrlpn+1 JCK (X | ξ) for all C.
    For the induction step, if C = ↓ the statement holds trivially, since wrlpn+1 J ↓ K (X | ξ) =
X = wrlpn+2 J ↓ K (X | ξ). For C ̸= ↓ we have

    wrlpn+2 JCK (X | ξ) =ξ −−⋆ stepJCK λC ′ . wrlpn+1 JC ′ K (X | ξ) ⋆ ξ
                                                                                               

                                       ≤ξ −−⋆ stepJCK (λC ′ . wrlpn JC ′ K (X | ξ) ⋆ ξ)
                                                   (Monotonicity of step, ⋆, −−⋆ and induction hypothesis)
                                       =wrlpn+1 JCK (X | ξ)

                                                                                                        ◀

▶ Lemma B.4 (Alternative description of wrlp).

    lim wrlpn JCK (X | ξ) = inf {wrlpn JCK (X | ξ) | n ∈ N}
    n→∞

Proof. This follows from Lemma B.3 and real-valued analysis.                                            ◀

▶ Definition B.5. Recall that

                                         X  m−1
                                             Y
                             ′
    reach(n, σ1 , s, σ ) =                                P(σi , s(σ1 . . . σi ))(σi+1 )
                                               i=1
                                                                                           
                                                                    m            ′
                                               σ1 . . . σm ∈ U , σm = σ , m ≤ n .

For final states σ ′
               p n
       σ −
         →            σ′         iff    p = reach(n, σ, s, σ ′ ) ,                                    (28)
          s
       1−p n                                  X
    σ −−→            ...         iff    p =       reach(n, σ, s, σ ′ ) .                              (29)
           s
                                              σ ′ final


▶ Lemma B.6. For a scheduler s, a state σ and a final state σ ′
           p                                                        qn n
       →∗ σ ′
     σ −                   iff         p = lim qn with σ −→                σ′
           s                               n→∞                       s
       p                                                            qn n
      →∗ . . .
    σ −                    iff         p = lim qn with σ −→                ...
       s                                   n→∞                       s




Proof. Both follow by using real-valued analysis.                                                       ◀

▶ Lemma B.7. For a scheduler s, a state σ and a final state σ ′′ with σ ̸= σ ′′ and where
λπ. s(σπ) behaves as s with the difference that we always append σ to its argument, we have
                               X
   reach(n + 1, σ, s, σ ′′ ) =   [ P(σ, s(σ))(σ ′ ) · reach(n, σ ′ , λπ. s(σπ), σ ′′ ) | σ ′ ∈ U ]
22   Towards Concurrent Quantitative Separation Logic


     Proof.
          reach(n + 1, σ, s, σ ′′ )
              "                                                                      #
          X m−1 Y
                                                       m                ′′
        =          P(πi , s(π1 . . . πi ))(πi+1 ) π ∈ U , π1 = σ, πm = σ , m ≤ n + 1
                  i=1
                                                                                                    (by definition)
             "                                                                                         #
            X m−1
               Y
        =               P(πi , s(π1 . . . πi ))(πi+1 ) π ∈ U m , π1 = σ, πm = σ ′′ , 2 ≤ m ≤ n + 1
                  i=1
                                                                                                    (since σ ̸= σ ′′ )
            X                      m−1
                                    Y
        =     P(π1 , s(π1 ))(π2 ) ·     P(πi , s(π1 π2 . . . πi ))(πi+1 )
                                          i=2
                                                                     
                         m                        ′′
                 π ∈ U , π1 = σ, πm = σ , 2 ≤ m ≤ n + 1                                      (by commutativity)

          X                  m−1
                              Y
        =   P(σ, s(σ))(π1 ) ·     P(πi , s(σπ1 . . . πi ))(πi+1 )
                                     i=1
                                                       
                         m           ′′
                 π ∈ U , πm = σ , 1 ≤ m ≤ n                                                             (renaming)

            X                   X  m−1
                                     Y
        =     P(σ, s(σ))(σ ′ ) ·         P(πi , s(σπ1 . . . πi ))(πi+1 )
                                            i=1

                                           π ∈ U m , π1 = σ ′ , πm = σ ′′ , 1 ≤ m ≤ n
                                                                                        
                          
                 σ′ ∈ U                                                                        (by distributivity)
            X
        =       [P(σ, s(σ))(π1 ) · reach(n, σ, λπ. s(σπ), σ ′ ) | σ ′ ∈ U ]                         (by definition)


                                                                                                                   ◀

     ▶ Definition B.8 (Weakest Liberal Preexpectation after n steps).
                             Xh
                                                                 p n
                                                                                 i
       wlpn JCK (X) = inf            p · X(s′ , h′ ) | C, (s, h) −
                                                                 → ↓ , (s′ , h′ ) + pdiv
                                                                 s
                                                                    
                                                          pdiv n
                                s ∈ S and C, (s, h) −−−→ . . .
                                                                 s

     ▶ Lemma B.9.
        wlpJCK (X)        =     lim wlpn JCK (X)
                               n→∞

     Proof. Follows directly from Lemma B.6.                                                                       ◀

     ▶ Theorem B.10 (Equality between wlp and wlp).
        wrlpJCK (X | [emp])        =       wlpJCK (X)
     Proof. We first observe, that wrlpn JCK (X | [emp]) simplifies to
                                
                                1
                                
                                                                                           if n = 0
        wrlpn JCK (X | [emp]) = X                                                           if n ̸= 0, C = ↓
                                
                                stepJCK λC ′ . wrlp
                                
                                                        JC ′ K (X | [emp])
                                                                          
                                                                                            else.
                                                              n−1
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                                                       23


We now prove by induction on n that wrlpn JCK (X | [emp]) = wlpn JCK (X), which by
Lemma B.9 also proofs the claim.
    For the induction basis, we have that n = 0, wrlpn JCK (X | [emp]) (s, h) = 1 and that
wlpn JCK (X) = 1 because of reach(0, σ, s, σ ′ ) = 0 and thus the probability of non-termination
is 1.
    Now we assume that for some fixed but arbitrary n the claim holds.
    For the induction step, we have two cases. If C = ↓ , then wrlpn+1 JCK (X | [emp]) (s, h) =
X(s, h); and reach(n + 1, (C, (s, h)), s, ( ↓ , (s, h))) = 1, thus wlpn+1 JCK (X) (s, h) = X(s, h)
as well.
    We will use lambda expressions to create anonymous functions. That is we define for a
sequence of states π and a state σ the notation (λπ ′ . s(σ.π ′ ))(π) = s(σ.π), where σ.π is the
                                                                                     p
string concatenation of σ with π. We can split the first step apart from σ −        → σ ′ due to
                                                                                     s
Lemma B.7. Thus, for C ̸=↓ we have:

    wlpn+1 JCK (X) (s, h)
         Xh
                                                        p n+1
                                                                                            i
   = inf       p · X(s′ , h′ ) | C, (s, h) −            →              ↓ , (s′ , h′ ) + pdiv
                                                         s
                                                                  
                                        pdiv n+1
           s ∈ S and C, (s, h) −−−→                          ...
                                           s
         Xh
                                                        p n+1
                                                                                            i
   = inf       p · X(s′ , h′ ) | C, (s, h) −            →              ↓ , (s′ , h′ )
                                                         s
                                                                                       
           Xh                           pdiv n+1
                                                                  i
         +      pdiv | C, (s, h) −−−→                        ...            s∈S                                            (pdiv is unique)
                                           s
                                                                                                                          n
         X                                                                                                                            
                 ′′    ′         ′   ′                            p′′           ′′        ′′     ′′              p′                ′  ′
   = inf       p · p · X(s , h ) | C, (s, h) −→ C , (s , h ) −−−−−−−−−−→ ↓ , (s , h )
                                                                   a                                   λπ. s(C,(s,h).π)
                                                      ′′                                                ′          n      
           X
                 ′′       ′                         p  div           ′′       ′′      ′′               p div
         +      pdiv · pdiv | C, (s, h) −−−→ C , (s , h ) −−−−−−−−−−→ . . .
                                                       a                                      λπ. s(C,(s,h).π)
                                                         
           s ∈ S and a ∈ Act(C, (s, h))                                                            (By Lemma B.7 and since C ̸=↓)
                                                                                                                n
         X                                                                                                                 
                 ′′
                       X
                               ′         ′      ′           ′′       ′′      ′′                   p′                   ′    ′
   = inf       p ·            p · X(s , h ) | C , (s , h ) −−−−−−−−−−→ ↓ , (s , h )
                                                                                      λπ. s(C,(s,h).π)
                       X                                                           ′                n        
                    ′′           ′           ′′       ′′      ′′                  p div
               +p ·            pdiv | C , (s , h ) −−−−−−−−−−→ . . .
                                                                       λπ. s(C,(s,h).π)
                                                                                                                     
                               p′′       ′′       ′′      ′′
                C, (s, h) −→ C , (s , h ) s ∈ S and a ∈ Act(C, (s, h))                                                    (Distributivity)
                                a
                                                                                                                     n
             X                                                                                                                  
                         ′′
                               X
                                       ′             ′      ′           ′′       ′′      ′′                p′                  ′ ′
   = inf inf           p ·          p · X(s , h ) | C , (s , h ) −−−−−−−−−−→ ↓ , (s , h )
                                                                                                 λπ. s(C,(s,h).π)
                                 X                                                            ′              n     
                            ′′            ′              ′′      ′′       ′′                 p div
                       +p ·             pdiv | C , (s , h ) −−−−−−−−−−→ . . .
                                                                                   λπ. s(C,(s,h).π)
                                                                                                                       
                                     p′′           ′′        ′′     ′′
                       C, (s, h) −→ C , (s , h ) s ∈ S a ∈ Act(C, (s, h))
                                             a
                                                                                             (Statement (4))
                                                                                           n
           X                 X                                                 ′
                                                                                                    
                                                                                 p
   = inf              inf p′′ ·   p′ · X(s′ , h′ ) | C ′′ , (s′′ , h′′ ) −−−−−−−−−−→ ↓ , (s′ , h′ )
                                                                          λπ. s(C,(s,h).π)
                                 X                                     ′         n      
                                                                       pdiv
                         + p′′ ·   p′div | C ′′ , (s′′ , h′′ ) −−−−−−     −−−−→ . . .
                                                                          λπ. s(C,(s,h).π)
24      Towards Concurrent Quantitative Separation Logic

                                                                                  
                                                 p′′ ′′   ′′  ′′
                                 s ∈ S C, (s, h) −→ C , (s , h ) a ∈ Act(C, (s, h))
                                                         a
                                                                     (Expressiveness of Schedulers, see † below)
                                                                                    n
                   X               X                                                         
                                                                                 p′
           = inf            inf p′′ ·    p′ · X(s′ , h′ ) | C ′′ , (s′′ , h′′ ) −→ ↓ , (s′ , h′ )
                                                                                 s
                                       X                                ′   n      
                                                                       p
                               + p′′ ·    p′div | C ′′ , (s′′ , h′′ ) −−div
                                                                          −→ . . .
                                                                          s
                                                      ′′
                                                                                                  
                                                     p
                                s ∈ S C, (s, h) −→ C ′′ , (s′′ , h′′ ) a ∈ Act(C, (s, h))
                                                         a
     (Set of schedulers where C, (s, h) has been taken and where it has not been taken is the same)
                                                                         n
                  X           X                                                  
                         ′′              ′       ′    ′    ′′ ′′   ′′ p′       ′   ′
            = inf       p · inf        p · X(s , h ) | C , (s , h ) −→ ↓ , (s , h )
                                                                      s
                                                               ′   n           
                                  X
                                           ′       ′′   ′′ ′′ pdiv
                                +       pdiv | C , (s , h ) −−−→ . . .       s∈S
                                                                 s
                                                                           
                                  p′′
                        C, (s, h) −→ C ′′ , (s′′ , h′′ ) a ∈ Act(C, (s, h))
                                        a
                                                                (Infimum of multiplication with constants)
                   X                                                                     
                                                                     p′′
           = inf      p′′ · wlpn JC ′′ K (X) (s′′ , h′′ ) C, (s, h) −→ C ′′ , (s′′ , h′′ )
                                                                      a
                                       
                  a ∈ Act(C, (s, h))                                                         (Rephrasing as wlp)
                 X                                                                                
                       ′′            ′′                   ′′  ′′              p′′      ′′     ′′ ′′
           = inf      p · wrlpn JC K (X | [emp]) (s , h ) C, (s, h) −→ C , (s , h )
                                                                               a
                                       
                  a ∈ Act(C, (s, h))                                                     (Induction hypothesis)

           = stepJCK (λC ′ . wrlpn JC ′ K (X | [emp])) (s, h)                            (Rephrasing as step)
           = wrlpn+1 JCK (X | [emp]) (s, h)                                             (Rephrasing as wrlp)

        The step in † is the most difficult part here. We will not go into all details and instead give
        a proof sketch. The first direction (which is the same as in Statement (7)), i.e.,
               (                    )
                 X                        X
                            ′
           inf       f (s, σ ) s ∈ S ≥        inf {f (s, σ ′ ) | s ∈ S} ,
                   σ ′ ∈A                      σ ′ ∈A

        it is easy (but technical) to proof: the value for choosing only one scheduler for all summands
        will always be at least as high as if we choose one scheduler each for every summand. The
        other direction, i.e.,
                 (                      )
                   X                       X
             inf       f (s, σ ′ ) s ∈ S ≤     inf {f (s, σ ′ ) | s ∈ S} ,
                   σ ′ ∈A                     σ ′ ∈A

        is far more difficult to prove. Let σ be the current state and σ ′ be the next state chosen
        in the sum. To prove this, one need to consider sequences of schedulers for each summand
        sσ′ ,i such that they convert to the infimum, i.e.,

           inf {f (s, σ ′ ) | s ∈ S} = lim f (sσ′ ,i , σ ′ ) .
                                        i→∞

        From these, one can show that we can always construct a sequence of schedulers si for all
        summands such that λπ. si (σ.σ ′ .π) = λπ. sσ′ ,i (σ.σ ′ .π). The expression then converges for
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                           25


the sequence si to the same value, i.e.,
        X                   X
    lim     f (si , σ ′ ) =   lim f (sσ′ ,i , σ ′ ) .
     i→∞                                     i→∞
           σ ′ ∈A                   σ ′ ∈A

From both directions, the equality then also follows.
   Thus, the claim is proven.                                                                              ◀

 C       Proofs about Framing
▶ Definition C.1. We define stacks s and s′ as equal for variables in V as
               V
     (s ∼ s′ )          iff   ∀x ∈ V s(x) = s′ (x) .

▶ Definition C.2. We define the in program C written variables Write(C) as all variables
occurring on left sides of assignments, lookups and allocation.
                                                                                         p
                                                                        → C ′ , (s′ , h′ )
▶ Lemma C.3. For a chpGCL program without atomic region C and C, (s, h) −
                                                                        a
               Vars\Write(C)
we have s ∼ s′                .

Proof. We prove this by induction on C.
   As the induction base we have that
   for the terminated program, such a transition does not exist;
   for the non-terminating program, probabilistic choice, conditional choice, loops, disposal
                                            p
                                           → C ′ , (s, h′ ), trivializing the statement; and
   and mutations, we always have C, (s, h) −
                                            a
   for assignment, allocation and lookup that the program on the left hand side is in
   Write(C) and thus does not change the value of variables in Vars \ Write(C).
                                                                                         p
   Now we establish the induction hypothesis that for C1 , C2 and Ci , (s, h) −  → Ci , (s′i , h′i )
                                                                                 a
                Vars\Write(Ci )
we have s ∼ s′i                  and prove the claim for the sequential composition and con-
currency.
   For the induction step we have that
                                                                              p
                                                                              → C1′ ; C2 , (s′1 , h′i )
   for the sequential composition, we directly have that for C1 ; C2 , (s, h) −
                                                                                     a
                                p
                         → C2′ , (s′1 , h′i ), the claim follows directly by the induction hypothesis;
     and ↓ ; C2 , (s, h) −
                                a
                                                                               p
     for concurrency, we have for both cases of i in C1 ∥ C2 , (s, h) −−−→ C1′                 C2′ (s′i , h′i )
                                                                              Ci.a
     that the claim follows in both cases directly by the induction hypothesis.
                                                                                                           ◀
                                                                                         p n
▶ Lemma C.4. For a chpGCL program C with atomic regions and C, (s, h) −
                                                                      →                         ↓ , (s′ , h′ )
                                                                      s
                  ′
                     Vars\Write(C)
we have that s ∼ s                  .

Proof. We prove the claim with nested inductions. The first induction is on the level of
atomic regions, i.e., we start with a program without any atomic region and increase the
possible nested atomic regions in the induction step. The second induction is on the number
of steps on the operational semantics n.
    Thus, we first start with a program that does not have any atomic region and prove that
              p n                             Vars\Write(C)
              → ↓ , (s′ , h′ ) we have s ∼ s′
for C, (s, h) −                                              . For n = 0 we only have C = ↓ , thus
                    s
trivially s = s′ . We establish the induction hypothesis † for n and prove the claim for n + 1.
                                        p                           Vars\Write(C)
By Lemma C.3 we have for C, (s, h) −   → C ′ , (s′ , h) that s ∼ s′                , furthermore by
                                                   a
26   Towards Concurrent Quantitative Separation Logic

                                                                   n
                                                              p′                                          Vars\Write(C)
     induction hypothesis † we have for C ′ , (s′ , h′ ) −→            ↓ , (s′′ , h′′ ) that s′ ∼ s′′                      .
                                                               s
                                                                                ′′   n+1
                                                                            p
     Together we also have by Lemma B.7 that for C, (s, h) −→          ↓ , (s′′ , h′′ ) we also have
                                                               s′
              Vars\Write(C)
      s ∼ s′′                .
        Now we assume that for a fixed but arbitrary level of nested atomic regions the claim
     holds as our induction hypothesis ♠.
                                                                                       p n
        For the induction step, we again prove by induction over n that C, (s, h) −   → ↓ , (s′ , h′ ).
                                                                                                      s
     We prove this again by induction over n. For n = 0 we have C = ↓ , thus trivially s = s′ .
     We establish the induction hypothesis †† for n and prove the claim for n + 1. The first
     part of the proof is for most cases totally analogous to Lemma                  C.3 except for the atomic
     region. Thus, we only consider the case that C = atomic C ′ Then we have the transition
                                                                             
                                       p                                                                    p m
     atomic C ′ , (s, h) −−−−→ ↓ , (s′ , h′ ) and by ♠ that for all m with C ′ , (s, h) −
                 
                                                                                                            →    ↓
                                   atomic                                                                   s
                                               ′
                                  Vars\Write(C   )                                   p
     , (s′ , h′ ) also s ∼ s′                                                        →∗
                                                   , therefore also for C ′ , (s, h) −      ↓ , (s′ , h′ ) we have
                                
                                                                                     s
                             ′
                Vars\Write(C )                                                                  p
       s ∼ s′                   by Lemma B.6 and thus also for atomic { C } , (s, h) −−−−→ ↓ , (s′ , h′ )
                                                                                              atomic
                          Vars\Write(C)                                       p
     we have s ∼ s′                       . For atomic { C } , (s, h) −−−−→ diverge, (s, h) we trivially
                                                                         atomic
                                                                                              p
     have s = s. With a similar proof as Lemma C.3, we get for C, (s, h) −             → C ′ , (s′ , h′ ) that
                                                                                       a
           ′ Vars\Write(C)
                                                ′   ′    ′        p n          ′′  ′′
      s∼s                  and from †† we get C , (s , h ) −      →       ↓ , (s , h ). Together and by
                                                                   s
                                            ′′ n+1
                                          p                 ′′    ′′                        ′′ Vars\Write(C)
                                                                                              
     Lemma B.7 we get that for C, (s, h) −→        ↓   , (s    , h   ) we  also have   s ∼ s                  .
                                           s′
                                                                                                            ◀
                                         p                                       Vars\Write(C)
                                → C ′ , (s′ , h′ ) we have s ∼ s′
     ▶ Lemma C.5. For C, (s, h) −                                                                 .
                                         a

     Proof. Follows from Lemma C.4 with n = 1.                                                                        ◀

     ▶ Definition C.6 (Free Variables). We define the free variables of an expectation X as

         Vars (X)      =    {x ∈ Vars | ∃v, v ′ ∈ Z : X [x := v] ̸= X [x := v ′ ]} .

     We define the free variables of a program Vars (C) as all variables occurring in the program
     C. We furthermore define Vars (A1 , A2 , . . . ) = Vars (A1 ) ∪ Vars (A2 ) ∪ . . . .
                                   V
     ▶ Lemma C.7. If s ∼ s′             and Vars (X) ⊆ V then X(s, h) = X(s′ , h).
                                                                 V
     Proof. Assume there are stacks s and s′ with s ∼ s′            such that X(s, h) ̸= X(s′ , h).
     Then s and s′ need to be different in at least one variable. For simplicity, we assume
     they differ in exactly one variable. Let x be this variable, such that s(x) ̸= s′ (x). Then
                           V
     x ̸∈ V since s ∼ s′       and x ̸∈ Vars (X)   since Vars (X) ⊆ V . Therefore, there exists no
         ′                                            ′                                    ′
                                              
     v, v ∈ Vars such that X [x :=  v] ̸= X
                                            x
                                                 := v . Then there can also not exist v, v ∈ Vars
     with X(s [x := v] , h) ̸= X(s x := v ′ , h) and therefore s(x) = s′ (x), which violates our as-
     sumption. It is now easy to extend this proof to s and s′ which differ in arbitrary many
     variables using a sequence of stacks that only differ in one variable with their predecessor
     and successor each.                                                                          ◀

     ▶ Lemma C.8 (Overapproximating Free Variables).

         Vars (wrlpn JCK (X | ξ)) ⊆ Vars (C, X, ξ)
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                       27


Proof. We prove this by contraposition, i.e., that for every x ∈ Vars\ Vars (C,   X, ξ) we have
for all values v, v ′ that wrlpn JCK (X | ξ) [x := v] = wrlpn JCK (X | ξ) x := v ′ . We will prove
this by induction on n.
                   base ′n = 0 holds trivially, since we have wrlp0 JCK (X | ξ) [x
    The induction                                                                     := v] = 1 =
wrlp0 JCK (X | ξ) x := v .
    We now assume that the claim holds for some arbitrary but fixed n as our induction
hypothesis.
    For the induction step, we have two cases. For              that C = ↓ we have the equality
                                                       the case
                                                             ′
                                                            v = wrlpn J ↓ K (X | ξ) x := v ′ by
                                                                                              
wrlpn+1 J ↓ K (X | ξ) [x   := v] = X [x  :=  v] = X x    :=
assumption that x ̸∈ Vars (X). For the case that C ̸= ↓ we have

      wrlpn+1 JCK (X | ξ) [x := v]
   = (ξ −−⋆ stepJCK (λC ′ . wrlpn JC ′ K (X | ξ) ⋆ ξ)) [x := v]                     (Definition of wrlp)
                           ′             ′
   = ξ −−⋆ stepJCK (λC . wrlpn JC K (X | ξ) ⋆ ξ) [x := v]                                 (x ̸∈ Vars (ξ))
                           ′                 ′
   = ξ −−⋆ stepJCK (λC . (wrlpn JC K (X | ξ) ⋆ ξ) [x := v])                                († see below)
                           ′             ′
   = ξ −−⋆ stepJCK (λC . wrlpn JC K (X | ξ) [x := v] ⋆ ξ)                                 (x ̸∈ Vars (ξ))
                           ′             ′                ′
   = ξ −−⋆ stepJCK (λC . wrlpn JC K (X | ξ) [x := v ] ⋆ ξ)                     (Induction Hypothesis)
                           ′                 ′                    ′
   = ξ −−⋆ stepJCK (λC . (wrlpn JC K (X | ξ) ⋆ ξ) [x := v ])                              (x ̸∈ Vars (ξ))
                           ′             ′                    ′
   = ξ −−⋆ stepJCK (λC . wrlpn JC K (X | ξ) ⋆ ξ) [x := v ]                                 († see below)
                               ′             ′                        ′
   = (ξ −−⋆ stepJCK (λC . wrlpn JC K (X | ξ) ⋆ ξ)) [x := v ]                              (x ̸∈ Vars (ξ))
                                    ′
   = wrlpn+1 JCK (X | ξ) [x := v ]                                                  (Definition of wrlp)

Now regarding †:

      stepJCK (t) [x := v] (s, h)
   = stepJCK (t) (s [x := v] , h)                                              (Definition of substitution)
         Xh                                                                  i
                                                            p
   = inf        p · t(C ′ )(s′ , h′ ) | C, (s [x := v] , h) −
                                                            → C ′ , (s′ , h′ )
                                                            a
                                             
           a ∈ Act(C, (s [x := v] , h))                                                (Definition of step)
         Xh                                                                                    i
                                                                     p
   = inf        p · t(C ′ )(s′ [x := v] , h′ ) | C, (s [x := v] , h) −
                                                                     → C ′ , (s′ [x := v] , h′ )
                                                                     a
                                             
           a ∈ Act(C, (s [x := v] , h))                       (Since x ̸∈ Vars (C) we have s′ (x) = v)
         Xh                                                                  i
                                                            p
   = inf        p · t(C ′ )(s′ [x := v] , h′ ) | C, (s, h) −→ C ′ , (s′ , h′ )
                                                            a
                                  
           a ∈ Act(C, (s, h))                         (Operational semantics and since x ̸∈ Vars (C))
         Xh                                                                  i
                                                            p
   = inf        p · t(C ′ ) [x := v] (s′ , h′ ) | C, (s, h) −
                                                            → C ′ , (s′ , h′ )
                                                            a
                                  
           a ∈ Act(C, (s, h))                                                  (Definition of substitution)

   = stepJCK (λC ′ . t(C ′ ) [x := v])                                              (Definition of wrlp)

Thus, the claim is proven.                                                                              ◀

▶ Lemma C.9. wrlpJdivergeK (X | ξ) = 1.
28   Towards Concurrent Quantitative Separation Logic


     Proof. We prove by induction on n that wrlpn JdivergeK (X | ξ) = 1. Then the same holds
     for the limit.
         For the induction base n = 0, we immediately have wrlp0 JdivergeK (X | ξ) = 1.
         Now we assume that the statement holds for some arbitrary but fixed n as our induction
     hypothesis.
         For the induction step, we have:

           wrlpn+1 JdivergeK (X | ξ)
        = ξ −−⋆ stepJdivergeK (λC ′ . wrlpn JC ′ K (X | ξ) ⋆ ξ)                           (Definition of wrlp)
        = ξ −−⋆ (wrlpn JdivergeK (X | ξ) ⋆ ξ)                                                   (†, see below)
        = ξ −−⋆ (1 ⋆ ξ)                                                               (Induction Hypothesis)
        ≥1                                                                                  (Statement (17))

     Now we still miss †, which we prove as:

          stepJdivergeK (t) (s, h)
              Xh                                                               i
                                                              p
        = inf         p · t(C ′ )(s′ , h′ ) | diverge, (s, h) −
                                                              → C ′ , (s′ , h′ )
                                                              a
                                                 
                a ∈ Act(diverge, (s, h))                                                  (Definition of step)
          Xh                                                  1
                                                                                  i
        =      1 · t(diverge)(s, h) | diverge, (s, h) −−→ diverge, (s, h)
                                                              div
                                                                    (Operational semantics of divergence)
        =t(diverge)(s, h)                                                                   (Set is singleton)

     Furthermore we have wrlpn+1 JdivergeK (X | ξ) ≤ 1 by Lemma B.2. Thus, the claim is
     proven.                                                                         ◀

     ▶ Lemma C.10. For an atomic region free chpGCL program C, a mapping t : C → E≤1 and
     an expectation X with Vars (X) ∩ Write(C) = ∅ we have

        stepJCK (t) ⋆ X      ≤     stepJCK (λC ′ . t(C ′ ) ⋆ X) .

     Proof. First, we notice that due to Vars (X) ∩ Write(C) = ∅ we have Vars (X) ⊆ Vars \
     Write(C). Now we prove the claim by structural induction on the program C.
        For C = ↓ we have stepJCK λC ′ . t(C ′ ) ⋆ X = 1 since Act( ↓ , (s, h)) = ∅, thus the
                                                      

     inequality holds trivially due to step being bounded by 1 above (cf. Lemma B.2).
        For C = diverge we have stepJCK λC ′ . t(C ′ ) ⋆ X = t(C) ⋆ X = stepJCK (t) ⋆ X (cf.
                                                            

     Lemma C.9)
        For C = x := e we have

          stepJCK (λC ′ . t(C ′ ) ⋆ X) (s, h)
              Xh                                                             i
                                                            p
        = inf         p · (t(C ′ ) ⋆ X)(s′ , h) | C, (s, h) −
                                                            → C ′ , (s′ , h′ )
                                                            a
                                      
                a ∈ Act(C, (s, h))                                                        (Definition of step)
          X                                          1
                                                                      
        =      (t(C ′ ) ⋆ X)(s′ , h) | C, (s, h) −−−−→ C ′ , (s′ , h)             (Act(C, (s, h)) is singleton)
                                                    assign
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                            29


     X                                             1
                                                                     
           ′   ′            ′                            ′    ′
   ≥   (t(C )(s , h1 ) · X(s , h2 ) | C, (s, h1 ) −−−−→ C , (s , h1 )
                                                         assign
                                (for any h1 ⋆ h2 = h and every heap allows the assign action)
     X                                               1
                                                                          
   =   (t(C ′ )(s′ , h1 ) · X(s, h2 ) | C, (s, h1 ) −−−−→ C ′ , (s′ , h1 )
                                                        assign
                                 (by Lemmas C.5 and C.7 and Vars (X) ⊆ Vars \ Write(C))
     X                                1
                                                        
           ′   ′                            ′    ′
   =   (t(C )(s , h1 ) | C, (s, h1 ) −−−−→ C , (s , h1 ) · X(s, h2 )
                                            assign
                                                             (Constant factors can be shifted outside)
   = stepJCK (t) (s, h1 ) · X(s, h2 )

Since the inequality holds for all h1 ⋆ h2 = h we also have

   stepJCK (λC ′ . t(C ′ ) ⋆ X) (s, h) ≥ sup{stepJCK (t) (s, h1 ) · X(s, h2 ) | h1 ⋆ h2 = h}
                                         = (stepJCK (t) ⋆ X)(s, h) .

   For C = { C1 } [ ep ] { C2 } the proof is analogous to the case C = x := e.
   For C = if ( b ) { C1 } else { C2 } the proof is analogous to the case C = x := e.
   For C = while ( b ) C ′ the proof is analogous to the case C = x := e.
   For C = x := new (e0 , . . . , en ) We now have that:

     stepJCK (λC ′ . t(C ′ ) ⋆ X) (s, h)
         Xh                                                                   o
                                                             p
   = inf        p · (t(C ′ ) ⋆ X)(s′ , h) | C, (s, h) −     → C ′ , (s′ , h′ )
                                                             a
                                   
           a ∈ Act(C, (s, h))                                                             (Definition of step)
         Xh                                                                                                 i
                                                                                           p
   = inf        p · sup{t(C ′ )(s′ , h′1 ) · X(s′ , h′2 ) | h′1 ⋆ h′2 = h′ } | C, (s, h) − → C ′ , (s′ , h′ )
                                                                                           a
                                   
           a ∈ Act(C, (s, h))                                                                 (Definition of ⋆)
         X                                                                                                   
                                                                                          1
   = inf        sup{t(C ′ )(s′ , h′1 ) · X(s′ , h′2 ) | h′1 ⋆ h′2 = h′ } | C, (s, h) −−−−→ C ′ , (s′ , h′ )
                                                                                       alloc-ℓ
                                           
           alloc-ℓ ∈ Act(C, (s, h))                                   (Operational semantics of allocation)
              nX                                                                                             o
                                                                          1
   = inf sup          [t(C ′ )(s′ , h′1 ) · X(s′ , h′2 ) | C, (s, h) −−−−→ C ′ , (s′ , h′ )] h′1 ⋆ h′2 = h′
                                                                       alloc-ℓ
                                           
           alloc-ℓ ∈ Act(C, (s, h))                                     (Sum over singleton or empty bag)
              nX
                                                                          1
   ≥ sup inf          [t(C ′ )(s′ , h′1 ) · X(s′ , h′2 ) | C, (s, h) −−−−→ C ′ , (s′ , h′ )]
                                                                       alloc-ℓ
                                               o                      
                                                        ′    ′      ′
                alloc-ℓ ∈ Act(C, (s, h)) h1 ⋆ h2 = h                                           (Statement (6))
              nX
                                                                                  1
   ≥ sup inf          [t(C ′ )(s′ , h′1 ) · X(s′ , h2 ) | C, (s, h1 ⋆ h2 ) −−−−→ C ′ , (s′ , h′1 ⋆ h2 )]
                                                                               alloc-ℓ
                                               o                    
                alloc-ℓ ∈ Act(C, (s, h)) h1 ⋆ h2 = h
                                                      (Reducing bag for sum and set for supremum)
30   Towards Concurrent Quantitative Separation Logic

                        nX
                                                                                       1
       ≥ sup       inf        [t(C ′ )(s′ , h′1 ) · X(s′ , h2 ) | C, (s, h1 ⋆ h2 ) −−−−→ C ′ , (s′ , h′1 ⋆ h2 )]
                                                                                    alloc-ℓ
                                                          o                 
                          alloc-ℓ ∈ Act(C, (s, h1 )) h1 ⋆ h2 = h
                                                                       (Since Act(C, (s, h1 )) ⊇ Act(C, (s, h)))
                      nX
                                                                                   1
       = sup       inf      [t(C ′ )(s′ , h′1 ) · X(s, h2 ) | C, (s, h1 ⋆ h2 ) −−−−→ C ′ , (s′ , h′1 ⋆ h2 )]
                                                                                alloc-ℓ
                                                       o                 
                        alloc-ℓ ∈ Act(C, (s, h1 )) h1 ⋆ h2 = h
                                                   (Lemmas C.5 and C.7 and Vars (X) ⊆ Vars \ Write(C))
                      nX
                                                                              1
       = sup       inf      [t(C ′ )(s′ , h′1 ) · X(s, h2 ) | C, (s, h1 ) −−−−→ C ′ , (s′ , h′1 )]
                                                                           alloc-ℓ
                                                       o                 
                        alloc-ℓ ∈ Act(C, (s, h1 )) h1 ⋆ h2 = h
                                                                          (Definition of operational semantics)
                        nX
                                                                  1
       = sup       inf        [t(C ′ )(s′ , h′1 ) | C, (s, h1 ) −−−−→ C ′ , (s′ , h′1 )]
                                                                 alloc-ℓ
                                                         o                              
                          alloc-ℓ ∈ Act(C, (s, h1 )) · X(s, h2 ) h1 ⋆ h2 = h
                                                        (Constant factors can be shifted outside)
                                                        
       = sup stepJCK (t) (s, h1 ) · X(s, h2 ) h1 ⋆ h2 = h                    (Definition of step)

       = (stepJCK (t) ⋆ X)(s, h)                                                                    (Definition of ⋆)


       For C = free(x) we have


         stepJCK (λC ′ . t(C ′ ) ⋆ X) (s, h)
             Xh                                                                i
                                                               p
       = inf       p · (t(C ′ ) ⋆ X)(s′ , h′ ) | C, (s, h) −  → C ′ , (s′ , h′ )
                                                               a
                                     
               a ∈ Act(C, (s, h))                                                           (Definition of step)
             Xh                                                           i
                                                           1
       = inf       (t(C ′ ) ⋆ X)(s, h′ ) | C, (s, h) −    → C ′ , (s, h′ )
                                                           a
                                     
               a ∈ Act(C, (s, h))                                      (Operational semantics of disposal)
             Xh                                                                                       i
                                                                                        1
       = inf       sup{t(C ′ )(s, h′1 ) · X(s, h′2 ) | h′1 ⋆ h′2 = h′ } | C, (s, h) −  → C ′ , (s, h′ )
                                                                                        a
                                     
               a ∈ Act(C, (s, h))                                                               (Definition of ⋆)
                 nX                                                                                   o
                                                                    1
       = inf sup         [t(C ′ )(s, h′1 ) · X(s, h′2 ) | C, (s, h) −
                                                                    → C ′ , (s, h′ )] | h′1 ⋆ h′2 = h′
                                                                    a
                                     
               a ∈ Act(C, (s, h))                                       (Sum over singleton or empty bag)
                 nX                                                                                       o
                                                                    1
       ≥ sup inf         [t(C ′ )(s, h′1 ) · X(s, h′2 ) | C, (s, h) −
                                                                    → C ′ , (s, h′ )] | a ∈ Act(C, (s, h))
                                                                         a
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                              31

                                
               h′1 ⋆ h′2 = h′                                                                  (Statement (6))
                    nX
                                                                           1
   ≥ sup       inf        [t(C ′ )(s, h′1 ) · X(s, h2 ) | C, (s, h1 ⋆ h2 ) −
                                                                           → C ′ , (s, h′1 ⋆ h2 )]
                                                                           a
                                             o                
                      a ∈ Act(C, (s, h)) h1 ⋆ h2 = h                         (Reducing the bag for sum)
                    nX
                                                                           1
   ≥ sup       inf        [t(C ′ )(s, h′1 ) · X(s, h2 ) | C, (s, h1 ⋆ h2 ) −
                                                                           → C ′ , (s, h′1 ⋆ h2 )]
                                                                           a
                                              o                
                      a ∈ Act(C, (s, h1 )) h1 ⋆ h2 = h
       (Since either {free} = Act(C, (s, h1 )), Act(C, (s, h)) or {free-abt} = Act(C, (s, h1 )))
             nX
                                                               1
   ≥ sup inf       [t(C ′ )(s, h′1 ) · X(s, h2 ) | C, (s, h1 ) −
                                                               → C ′ , (s, h′1 )]
                                                               a
                                       o                
               a ∈ Act(C, (s, h1 )) h1 ⋆ h2 = h                 (Operational semantics of disposal)
             nX
                                                    1
   = sup inf       [t(C ′ )(s, h′1 ) | C, (s, h1 ) −
                                                   → C ′ , (s, h′1 )]
                                                    a
                                       o                              
               a ∈ Act(C, (s, h1 )) · X(s, h2 ) h1 ⋆ h2 = h
                                                   (Constant factors can be shifted outside)
                                                    
   = sup stepJCK (t) (s, h1 ) ⋆ X(s, h2 ) h1 ⋆ h2 = h                   (Definition of step)

   = (stepJCK (t) ⋆ X)(s, h)                                                                  (Definition of ⋆)


   For C = x := < e > we have


     stepJCK (λC ′ . t(C ′ ) ⋆ X) (s, h)
         Xh                                                                   i
                                                              p
   = inf       p · (t(C ′ ) ⋆ X)(s′ , h′ ) | C, (s, h) −     → C ′ , (s′ , h′ )
                                                              a
                                  
           a ∈ Act(C, (s, h))                                                                (Definition of step)
         Xh                                                                 i
                                                          1
   = inf       (t(C ′ ) ⋆ X)(s′ , h′ ) | C, (s, h) −      → C ′ , (s′ , h′ )
                                                          a
                                  
           a ∈ Act(C, (s, h))                                            (Operational semantics of lookup)
         Xh                                                                                                i
                                                                                          1
   = inf       sup{t(C ′ )(s′ , h′1 ) · X(s′ , h′2 ) | h′1 ⋆ h′2 = h′ } | C, (s, h) −    → C ′ , (s′ , h′ )
                                                                                          a
                                  
           a ∈ Act(C, (s, h))                                                                    (Definition of ⋆)
             nX                                                                                          o
                                                                      1
   = inf sup         [t(C ′ )(s′ , h′1 ) · X(s′ , h′2 ) | C, (s, h) −→ C ′ , (s′ , h′ )] | h′1 ⋆ h′2 = h′
                                                                      a
                                  
           a ∈ Act(C, (s, h))                                           (Sum over singleton or empty bag)
             nX                                                                                              o
                                                                      1
   ≥ sup inf         [t(C ′ )(s′ , h′1 ) · X(s′ , h′2 ) | C, (s, h) −→ C ′ , (s′ , h′ )] | a ∈ Act(C, (s, h))
                                                                     a
32   Towards Concurrent Quantitative Separation Logic

                                    
                   h′1 ⋆ h′2 = h′                                                                     (Statement (6))
                        nX
                                                                                     1
       ≥ sup       inf        [t(C ′ )(s′ , h′1 ) · X(s′ , h2 ) | C, (s′ , h1 ⋆ h2 ) −
                                                                                     → C ′ , (s, h′1 ⋆ h2 )]
                                                                                     a
                                                  o                 
                          a ∈ Act(C, (s, h)) h1 ⋆ h2 = h                               (Reducing the bag for sum)
                        nX
                                                                                   1
       ≥ sup       inf        [t(C ′ )(s′ , h′1 ) · X(s′ , h2 ) | C, (s, h1 ⋆ h2 ) −
                                                                                   → C ′ , (s′ , h′1 ⋆ h2 )]
                                                                                   a
                                                    o                 
                          a ∈ Act(C, (s, h1 )) h1 ⋆ h2 = h
       (Since either {lookup} = Act(C, (s, h1 )), Act(C, (s, h)) or {lookup-abt} = Act(C, (s, h1 )))
                   nX
                                                                        1
        ≥ sup inf         [t(C ′ )(s, h′1 ) · X(s′ , h2 ) | C, (s, h1 ) −
                                                                        → C ′ , (s′ , h′1 )]
                                                                        a
                                                o               
                      a ∈ Act(C, (s, h1 )) h1 ⋆ h2 = h                    (Operational semantics of lookup)
                   nX
                                                                        1
        = sup inf         [t(C ′ )(s′ , h′1 ) · X(s, h2 ) | C, (s, h1 ) −
                                                                        → C ′ , (s′ , h′1 )]
                                                                        a
                                                o               
                      a ∈ Act(C, (s, h1 )) h1 ⋆ h2 = h
                                                   (Lemmas C.5 and C.7 and Vars (X) ⊆ Vars \ Write(C))
                        nX
                                                                1
       = sup       inf        [t(C ′ )(s′ , h′1 ) | C, (s, h1 ) −
                                                                → C ′ , (s′ , h′1 )]
                                                                a
                                                    o                              
                          a ∈ Act(C, (s, h1 )) · X(s, h2 ) h1 ⋆ h2 = h
                                                       (Constant factors can be shifted outside)
                                                        
       = sup stepJCK (t) (s, h1 ) ⋆ X(s, h2 ) h1 ⋆ h2 = h                   (Definition of step)

       = (stepJCK (t) ⋆ X)(s, h)                                                                      (Definition of ⋆)

       For C = < e > := e′ we have

         stepJCK (λC ′ . t(C ′ ) ⋆ X) (s, h)
             Xh                                                                i
                                                               p
       = inf       p · (t(C ′ ) ⋆ X)(s′ , h′ ) | C, (s, h) −  → C ′ , (s′ , h′ )
                                                               a
                                     
               a ∈ Act(C, (s, h))                                                           (Definition of step)
             Xh                                                           i
                                                           1
       = inf       (t(C ′ ) ⋆ X)(s, h′ ) | C, (s, h) −    → C ′ , (s, h′ )
                                                           a
                                     
               a ∈ Act(C, (s, h))                                     (Operational semantics of mutation)
             Xh                                                                                       i
                                                                                        1
       = inf       sup{t(C ′ )(s, h′1 ) · X(s, h′2 ) | h′1 ⋆ h′2 = h′ } | C, (s, h) −  → C ′ , (s, h′ )
                                                                                        a
                                     
               a ∈ Act(C, (s, h))                                                               (Definition of ⋆)
                 nX                                                                                   o
                                                                    1
       = inf sup         [t(C ′ )(s, h′1 ) · X(s, h′2 ) | C, (s, h) −
                                                                    → C ′ , (s, h′ )] | h′1 ⋆ h′2 = h′
                                                                          a
  I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                          33

                                      
                 a ∈ Act(C, (s, h))                                     (Sum over singleton or empty bag)
                    nX                                                                                      o
                                                                      1
     ≥ sup       inf       [t(C ′ )(s, h′1 ) · X(s, h′2 ) | C, (s, h) −
                                                                      → C ′ , (s, h′ )] | a ∈ Act(C, (s, h))
                                                                      a
                                
                 h′1 ⋆ h′2 = h′                                                                 (Statement (6))
                      nX
                                                                            1
     ≥ sup       inf       [t(C ′ )(s, h′1 ) · X(s, h2 ) | C, (s, h1 ⋆ h2 ) −
                                                                            → C ′ , (s, h′1 ⋆ h2 )]
                                                                            a
                                              o                
                       a ∈ Act(C, (s, h)) h1 ⋆ h2 = h                         (Reducing the bag for sum)
                      nX
                                                                            1
     ≥ sup       inf       [t(C ′ )(s, h′1 ) · X(s, h2 ) | C, (s, h1 ⋆ h2 ) −
                                                                            → C ′ , (s, h′1 ⋆ h2 )]
                                                                            a
                                               o                
                       a ∈ Act(C, (s, h1 )) h1 ⋆ h2 = h
(Since either {mutation} = Act(C, (s, h1 )), Act(C, (s, h)) or {mutation-abt} = Act(C, (s, h1 )))
                nX
                                                                   1
     ≥ sup inf        [t(C ′ )(s, h′1 ) · X(s, h2 ) | C, (s, h1 ) −
                                                                  → C ′ , (s, h′1 )]
                                                                  a
                                          o                
                  a ∈ Act(C, (s, h1 )) h1 ⋆ h2 = h                (Operational semantics of mutation)
                nX
                                                       1
     = sup inf        [t(C ′ )(s, h′1 ) | C, (s, h1 ) −
                                                      → C ′ , (s, h′1 )]
                                                       a
                                          o                              
                  a ∈ Act(C, (s, h1 )) · X(s, h2 ) h1 ⋆ h2 = h
                                                     (Constant factors can be shifted outside)
                                                      
     = sup stepJCK (t) (s, h1 ) ⋆ X(s, h2 ) h1 ⋆ h2 = h                   (Definition of step)

     = (stepJCK (t) ⋆ X)(s, h)                                                                 (Definition of ⋆)

     Now we assume as induction hypothesis that for arbitrary but fixed C1 and C2 the
  assumption already holds.
     For C = C1 ; C2 we have two cases, either C1 = ↓ or C1 ̸= ↓ . We only consider the case
  that C1 ̸= ↓ , since the case C1 = ↓ is analogous.

       stepJCK (λC ′ . t(C ′ ) ⋆ X) (s, h)
           Xh                                                               i
                                                           p
     = inf       p · (t(C ′ ) ⋆ X)(s′ , h′ ) | C, (s, h) −→ C ′ , (s′ , h′ )
                                                           a
                                  
             a ∈ Act(C, (s, h))                                                             (Definition of step)
           Xh                                                                    i
                                                                p
     = inf       p · (t(C1′ ; C2 ) ⋆ X)(s′ , h′ ) | C1 , (s, h) −
                                                                → C1′ , (s′ , h′ )
                                                                a
                                  
             a ∈ Act(C, (s, h))
              (Operational semantics of sequential composition and assumption that C1 ̸= ↓ )
     = stepJC1 K (λC ′ . t(C ′ ; C2 ) ⋆ X) (s, h)                                           (Definition of step)
     ≥ (stepJC1 K (λC ′ . t(C ′ ; C2 )) ⋆ X)(s, h)                                     (Induction Hypothesis)
     = (stepJCK (t) ⋆ X)(s, h)                               (Analogous to the previous transformation)
34   Towards Concurrent Quantitative Separation Logic


        For C = C1 ∥ C2 we have four cases, one for every case that we have for any i = 1 or
     i = 2 either Ci ̸= ↓ or Ci = ↓ . We first prove it for the case that C1 ̸= ↓ and C2 ̸= ↓ .
     Other cases are analogous.

          stepJCK (λC ′ . t(C ′ ) ⋆ X) (s, h)
              Xh                                                              i
                                                              p
        = inf       p · (t(C ′ ) ⋆ X)(s′ , h′ ) | C, (s, h) −→ C ′ , (s′ , h′ )
                                                              a
                                      
                a ∈ Act(C, (s, h))                                                         (Definition of step)
              (    Xh
                                                                             p
                                                                                               i
        = inf inf           p · (t( C1′ ∥ C2 ) ⋆ X)(s′ , h′ ) | C1 , (s, h) −
                                                                            → C1′ , (s′ , h′ )
                                                                                a
                                                
                         a ∈ Act(C1 , (s, h)) ,
                      Xh                                                                          i
                                                                               p
                inf           p · (t( C1 ∥ C2′ ) ⋆ X)(s′ , h′ ) | C2 , (s, h) −
                                                                              → C2′ , (s′ , h′ )
                                                                              a
                                               )
                         a ∈ Act(C2 , (s, h))                                                          (Statement (4))
                (                                                                                                )
                                   ′      ′                                        ′           ′
        = inf    stepJC1 K (λC . t( C ∥ C1 ) ⋆ X) (s, h), stepJC2 K (λC . t( C1 ∥ C ) ⋆ X) (s, h)

                                                                                               (Definition of step)
                (                                                                                              )
        ≥ inf    (stepJC1 K (λC ′ . t( C ′ ∥ C1 )) ⋆ X)(s, h), (stepJC2 K (λC ′ . t( C1 ∥ C ′ )) ⋆ X)(s, h)

                                                                                           (Induction Hypothesis)
                (
                    sup (stepJC1 K (λC ′ . t( C ′ ∥ C1 )) (s, h1 ) · X(s, h2 ) h1 ⋆ h2 = h ,
                       
        = inf
                                                                                                       )
                    sup (stepJC2 K (λC ′ . t( C1 ∥ C ′ )) (s, h1 ) · X(s, h2 ) h1 ⋆ h2 = h
                       


                                                                                                       (Definition of ⋆)
                (
                    inf (stepJC1 K (λC ′ . t( C ′ ∥ C1 )) (s, h1 ) · X(s, h2 ),
                       
        ≥ sup
                                                                                                       )
                                          ′            ′
                          stepJC2 K (λC . t( C1 ∥ C )) (s, h1 ) · X(s, h2 )            h1 ⋆ h2 = h}

                                                                                                       (Statement (6))
        = sup {stepJCK (t) (s, h1 ) · X(s, h2 ) | h1 ⋆ h2 = h}}
                                                              (Similar to the previos transformation)
        = (stepJCK (t) · X)(s, h)                                                                      (Definition of ⋆)

     Thus, the claim is proven.                                                                                      ◀

     ▶ Lemma C.11. For a chpGCL program C and expectations X and Y with Vars (X) ∩
     Write(C) = ∅ we have

        wlpJCK (Y ) ⋆ X        ≤       wlpJCK (Y ⋆ X) .
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                              35


Proof. We have wlpJCK (Y ) = wrlpJCK (Y | [emp]) by Theorem B.10. Furthermore, if
for all n we have wrlpn JCK (Y | [emp]) ⋆ X ≤ wrlpn JCK (X ⋆ Y | [emp]) we also have that
wrlpJCK (Y | [emp]) ⋆ X ≤ wrlpJCK (Y ⋆ X | [emp]). We prove the claim now by a nested
induction. The first induction is on the level of atomic regions.
    We now assume that C does not have any atomic regions. The second induction is on
n, For the base case n = 0, we prove now first that wrlp0 JCK (Y | [emp]) ⋆ X = 1 ⋆ X ≤ 1 =
wrlp0 JCK (Y ⋆ X | [emp]). Next, we assume that the claim holds for a fixed but arbitrary n
as our induction hypothesis †. For our induction step, we have that either C = ↓ in which
case wrlpn+1 J ↓ K (Y ⋆ X | [emp]) = Y ⋆ X = wrlpn+1 J ↓ K (Y | [emp]) ⋆ X. For the other case
that C ̸= ↓ we have:

      wrlpn+1 JCK (Y ⋆ X | [emp])
   = stepJCK (λC ′ . wrlpn JC ′ K (Y ⋆ X | [emp]))                   ([emp] is neutral element)
                   ′           ′
   ≥ stepJCK (λC . wrlpn JC K (Y | [emp]) ⋆ X)
                                        (Induction Hypothesis † and monotonicity of step)
   ≥ stepJCK (λC ′ . wrlpn JC ′ K (Y | [emp])) ⋆ X                                 (Lemma C.10)
   = wrlpn+1 JCK (Y | [emp]) ⋆ X                                     ([emp] is neutral element)

    Next we assume that the claim holds for an arbitrary but fixed level of atomic regions
in the program C ′ as our induction hypothesis ♠.
    We again prove the induction step by an induction over n. For the induction basis we
have wrlp0 JCK (Y | [emp]) ⋆ X = 1 ⋆ X ≤ 1 = wrlp0 JCK (Y ⋆ X | [emp]). Thus, we assume
that the claim holds for a fixed but arbitrary n as our induction hypothesis ††. For the
induction step we have two cases. If C = ↓ we have wrlpn+1 J ↓ K (Y ⋆ X | [emp]) = Y ⋆ X =
wrlpn+1 J ↓ K (Y | [emp]) ⋆ X and if C ̸= ↓ we have:

      wrlpn+1 JCK (Y ⋆ X | [emp])
   = stepJCK (λC ′ . wrlpn JC ′ K (Y ⋆ | [emp]))                     ([emp] is neutral element)
                   ′           ′
   ≥ stepJCK (λC . wrlpn JC K (Y | [emp])) ⋆ X                                     (Left to prove)
   = wrlpn+1 JCK (Y | [emp]) ⋆ X                                     ([emp] is neutral element)

We require a similar proof as in Lemma C.10 together with our induction hypothesis †† to
prove the left to prove
                     ′part. There we only miss the case for atomic regions. Thus, we
assume C = atomic C and prove first for n = 0 that:

      stepJCK (λC ′′ . wrlp0 JC ′′ K (Y ⋆ X | [emp]))
   = stepJatomic { C ′ }K (λC ′′ . wrlp0 JC ′′ K (Y ⋆ X | [emp]))            (Case assumption)
         Xh
   = inf       p · wrlp0 JC ′′ K (Y ⋆ X | [emp]) (s′ , h′ )
                                                      i                   
                              ′           p        ′′   ′   ′
                  atomic { C } , (s, h) −
                                        → C , (s , h ) a ∈ Act(C, (s, h))
                                          a
                                                                         (Definition of step)
     Xh                                                                  p
                                                                                              i
   =   p · wrlp0 JC K (Y ⋆ X | [emp]) (s , h ) | atomic { C } , (s, h) −−−−→ C ′′ , (s′ , h′ )
                   ′′                   ′   ′              ′
                                                                          atomic
                                                      (Operational semantics of atomic regions)
       Xh                                                                        p
                                                                                                 i
   =      p · wrlp0 J ↓ K (Y ⋆ X | [emp]) (s , h ) | atomic { C ′ } , (s, h) −−−−→ ↓ , (s′ , h′ )
                                            ′   ′
                                                                              atomic
       Xh
                                                     ′  ′
     +    p · wrlp0 JdivergeK (Y ⋆ X | [emp]) (s , h )
36   Towards Concurrent Quantitative Separation Logic


                                                p
                                                                            i
                      atomic { C ′ } , (s, h) −−−−→ diverge, (s, h)
                                              atomic
                                                      (Separating terminating and diverging pathes)
              Xh                                                                        p
                                                                                                        i
        =      p · wrlp0 J ↓ K (Y ⋆ X | [emp]) (s′ , h′ ) | atomic { C ′ } , (s, h) −−−−→ ↓ , (s′ , h′ )
                                                                                     atomic
            Xh                                    p
                                                                          i
                                    ′
          +    p · 1 atomic { C } , (s, h) −−−−→ diverge, (s, h)                       (wrlp0 is always 1)
                                               atomic
            Xh                                     p
                                                                   i
        =      p · 1 | atomic { C ′ } , (s, h) −−−−→ ↓ , (s′ , h′ )
                                                atomic
            Xh                                    p
                                                                          i
          +    p · 1 atomic { C ′ } , (s, h) −−−−→ diverge, (s, h)                     (wrlp0 is always 1)
                                               atomic
            Xh                      p
                                                     i
        =      p · 1 | C ′ , (s, h) −
                                    →∗ ↓ , (s′ , h′ )
            Xh                      p
                                             o
          +    p · 1 C ′ , (s, h) − →∗ . . .                (Operational semantics of atomic regions)
        = wlpJC ′ K (1)                                                                (Definition of wlp)
                  ′
        ≥ wlpJC K (1 ⋆ X)                                                           (Monotonicitiy of wlp)
                  ′
        ≥ wlpJC K (1) ⋆ X                                                                             (♠)
                          ′         ′
        = stepJCK (λC . wrlp0 JC K (Y | [emp])) ⋆ X                                     (Similar to above)

     and next for n > 0 that:

            stepJCK (λC ′′ . wrlpn JC ′′ K (Y ⋆ X | [emp]))
        = stepJatomic { C ′ }K (λC ′′ . wrlpn JC ′′ K (Y ⋆ X | [emp]))                 (Case assumption)
              Xh
        = inf       p · wrlpn JC ′′ K (Y ⋆ X | [emp]) (s′ , h′ )
                                                            i                   
                                    ′           p          ′′       ′   ′
                        atomic { C } , (s, h) −
                                              → C , (s , h ) a ∈ Act(C, (s, h))
                                                a
                                                                                   (Definition of step)
            Xh                                                                     p
                                                                                                         i
        =        p · wrlpn JC K (Y ⋆ X | [emp]) (s , h ) | atomic { C } , (s, h) −−−−→ C ′′ , (s′ , h′ )
                              ′′                       ′        ′               ′
                                                                                     atomic
                                                          (Operational semantics of atomic regions)
            Xh                                                                        p
                                                                                                       i
        =      p · wrlpn J ↓ K (Y ⋆ X | [emp]) (s , h ) | atomic { C ′ } , (s, h) −−−−→ ↓ , (s′ , h′ )
                                                 ′   ′
                                                                                   atomic
            Xh
                                                          ′ ′
          +    p · wrlpn JdivergeK (Y ⋆ X | [emp]) (s , h )
                                           p
                                                                  i
                 atomic { C ′ } , (s, h) −−−−→ diverge, (s, h)
                                              atomic
                                                      (Separating terminating and diverging pathes)
              Xh                                                                         p
                                                                                                          i
        =       p · wrlpn J ↓ K (Y ⋆ X | [emp]) (s′ , h′ ) | atomic { C ′ } , (s, h) −−−−→ ↓ , (s′ , h′ )
                                                                                      atomic
            Xh                                     p
                                                                          i
                                    ′
          +     p · 1 atomic { C } , (s, h) −−−−→ diverge, (s, h)                            (Lemma C.9)
                                                atomic
            X h                                                     p
                                                                                     i
        =       p · (Y ⋆ X)(s′ , h′ ) | atomic { C ′ } , (s, h) −−−−→ ↓ , (s′ , h′ )
                                                                 atomic
            Xh                                     p
                                                                          i
          +     p · 1 atomic { C ′ } , (s, h) −−−−→ diverge, (s, h)
                                                    atomic
                                                 (wrlpn of ↓ is always the postexpectation for n > 0)
            Xh                                       p
                                                                      i
        =      p · (Y ⋆ X)(s′ , h′ ) | C ′ , (s, h) −
                                                    →∗ ↓ , (s′ , h′ )
            Xh                     p
                                               i
          +    p · 1 C ′ , (s, h) −
                                  →∗ . . .                  (Operational semantics of atomic regions)
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                37


     = wlpJC ′ K (Y ⋆ X)                                                       (Definition of wlp)
               ′
     ≥ wlpJC K (Y ) ⋆ X                                                                        (♠)
                    ′          ′
     = stepJCK (λC . wrlpn JC K (Y | [emp])) ⋆ X                                (Similar to above)

Thus, the claim is proven.                                                                       ◀



▶ Theorem C.12. For an chpGCL program C, a mapping t : chpGCL → E≤1 and an expect-
ation X with Vars (X) ∩ Write(C) = ∅ we have

     stepJCK (t) ⋆ X    ≤    stepJCK (λC ′ . t(C ′ ) ⋆ X) .


Proof. Follows from Lemmas C.10 and C.11 by structural induction on the program C. ◀



 D       Proofs for Conservativity Properties

▶ Lemma D.1 (Conservativeness of qualitative wrlp). For qualitative X and non-probabilistic
program C we have

     wrlpn JCK (X | ξ) ∈ {0, 1} .


Proof. The factor p in step is always 1 due to the absence of probabilistic constructs in C.
The countable sum in step inflates to a sum of singleton or to the empty set. The sum of
an empty set is 0, the sum of a singleton is the value of its only element. From this point,
the rest is a straight forward induction on n.                                            ◀



▶ Definition D.2 (Framing Enabled Programs). A non-probabilistic program C is fram-
ing enabled if for their respective M DP semantics we have for all states C, (s, h), all
heaps hF with h ⊥ hF and all enabled actions a ∈ Act(C, (s, h ⋆ hF )) that if there exists
          1                                            1
          → C ′ , (s′ , h′ ) then also C, (s, h ⋆ hF ) −
C, (s, h) −                                            → C ′ , (s′ , h′ ⋆ hF ).
           a                                           a


▶ Theorem D.3. Every non-probabilistic chpGCL program C is framing enabled.

Proof. We prove this by induction over the structure of C.
    For the terminated program, non-terminating program, assignment, sequential com-
position, atomic region, conditional choice, loop, disposal, lookup and mutation we have
|Act(C, (s, h ⋆ hF ))| ≤ 1. If Act(C, (s, h ⋆ hF )) = ∅ the claim holds immediately. Thus we as-
                                                                                    1
sume that Act(C, (s, h⋆hF )) = {a}. Now we furthermore assume that C, (s, h) −      → C ′ , (s, h′ )
                                                                                    a
to show that the framing enabled condition holds. Then we also have for all these programs
that Act(C, (s, h)) = {a}. Now let φ(s′′ , h′′ ) = 1 iff s′′ = s′ , h′′ = h′ and ψ(s′′ , h′′ ) = 1
                                                                                 1
iff h′′ = hF . If stepJCK λC ′ . φ (s, h) = 0 then the premise that C, (s, h) −  → C ′ , (s, h′ ) is
                                   
                                                                                 a
                                                λC ′ . φ (s, h) = 1 due to Lemma
                                                        
not satisfied. Thus we have that stepJCK                                         D.1. Then we
also have that 1 = (stepJCK λC . φ ⋆ ψ)(s, h ⋆ hF ) ≤ stepJCK λC ′ . φ ⋆ ψ (s, h ⋆ hF ) due
                                     ′
                                        
38   Towards Concurrent Quantitative Separation Logic


     to Theorem C.12. Then

                stepJCK (λC ′ . φ ⋆ ψ) (s, h ⋆ hF ) = 1
                    Xh                                                                i
                                                                  1
        implies inf       (φ ⋆ ψ)(s′′ , h′′ ) | C, (s, h ⋆ hF ) − → C ′ , (s′′ , h′′ )
                                                                  a
                                                  
                      a ∈ Act(C, (s, h ⋆ hF )) = 1                          (Definition of qualitative step)
                    Xh                                                                       i
                                                                      1
        implies inf       φ(s′ , h′ ) · ψ(s′ , hF ) | C, (s, h ⋆ hF ) −
                                                                      → C ′ , (s′ , h′ ⋆ hF )
                                                                      a
                                                  
                      a ∈ Act(C, (s, h ⋆ hF )) = 1                  (Definition of qualitative ⋆, φ and ψ)



     which proves the claim, as the last equation can only be true if for (the only) action a ∈
                                                  1
                                                  → C ′ , (s′ , h′ ⋆ hF ).
     Act(C, (s, h ⋆ hF )) we have C, (s, h ⋆ hF ) −
                                                          a
        For allocation and for all a ∈ Act(x := new (e1 . . . en ) , (s, h ⋆ hF )), where we have that
                                      1
     x := new (e1 . . . en ) , (s, h) −
                                      → ↓ , (s, h ⋆ ha ), we have since the action is enabled for h ⋆ hF
                                          a
                                                         1
     also that x := new (e1 . . . en ) , (s, h ⋆ hF ) −
                                                      → ↓ , (s, h ⋆ ha ⋆ hF ), which proves the claim.
                                                         a
        Now we assume that the statement holds for arbitrary but fixed programs C1 and C2 .
                                                                                            1
                                                                                → C1′ ; C2 , (s′ , h′ )
        For sequential composition we have that if C1 ̸= ↓ and C1 ; C2 , (s, h) −
                                                                                            a
                           1                                                                1
                           → C1′ , (s′ , h′ ). By induction hypothesis C1 , (s, h⋆hF ) −
     then also C1 , (s, h) −                                                           → C1′ , (s′ , h′ ⋆hF )
                           a                                                                  a
                                                1    ′          ′   ′
     and thus also C1 ; C2 , (s, h ⋆ hF ) −
                                          →         C1 ; C2 , (s , h ⋆ hF ). The case that C1 = ↓    is analogous.
                                                a
                                                                        1
        For concurrency we have that if C1 ∥ C2 , (s, h) −−−→ C1′                   C2 , (s′ , h′ ), then we also
                                                                       C1,a
                       1                                                                         1
                      → C1′ , (s′ , h′ ) and by the induction hypothesis C1 , (s, h ⋆ hF ) −
     have C1 , (s, h) −                                                                    → C1′ , (s′ , h′ ⋆
                       a                                                                         a
                                                             1
     hF ) and thus also C1 ∥ C2 , (s, h ⋆ hF ) −−−→ C1′               C2 , (s′ , h′ ⋆ hF ). The case where we
                                                         C1,a
                                    1
     have C1 ∥ C2 , (s, h)     −−−→           C1′        ′   ′
                                                    C2 , (s , h ) is analogous and the case where we have
                                   C2,a
                           1
      ↓ ∥ ↓ , (s, h) −−−−−−→ ↓ , (s, h) holds trivially.
                       con−end
        Thus the claim is proven.                                                                              ◀

     ▶ Definition 4.1 (Safe Judgements [52]). The predicate safen (C, s, h, ξ, φ) holds for qualit-
     ative φ and ξ and non-probabilistic program C if and only if
     1. if n = 0, then it holds always; and
     2. if n > 0 and C = ↓ , then φ(s, h) = 1; and
     3. if n > 0 and for all hξ and hF with ξ(s, hξ ) = 1 and h ⊥ hξ ⊥ hF , then for all enabled
                                                                                            1
        actions a ∈ Act(C, (s, h ⋆ hξ ⋆ hF )) we do not have C, (s, h ⋆ hξ ⋆ hF ) −
                                                                                  → abort; and
                                                                                            a
     4. if n > 0 and for all hξ , hF , C ′ , s and h, with ξ(s, hξ ) = 1, and h ⊥ hξ ⊥ hF , and
                               1
                             → C ′ , (s′ , h′ ), then there exists h′′ and h′ξ such that h′ = h′′ ⋆ h′ξ ⋆ hF
        C, (s, h ⋆ hξ ⋆ hF ) −
                               a
        and ξ(s′ , h′ξ ) = 1 and safen−1 (C ′ , s′ , h′′ , ξ, φ).
     For qualitative φ, ψ and ξ, we say that ξ |= {ψ} C {φ} holds if and only if for all stack/heap
     pairs s, h the statement ψ(s, h) = 1 ⇒ ∀n ∈ N. safen (C, s, h, ξ, φ) holds.
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                       39


▶ Theorem 4.1 (Conservative Extension of Concurrent Separation Logic). For a framing-
enabled non-probabilistic program C and qualitative expectations φ, ψ and ξ, we have

   φ ≤ wrlpJCK (ψ | ξ)          iff   ξ |= {φ} C {ψ} .

Proof. Remark that step simplifies for non-probabilistic programs to
                         n                   o n                                              o
                                      1                                     1
                                      → abort ∪ t(C ′ )(s′ , h′ ) C, (s, h) −
 stepJCK (t) (s, h) = inf 0 C, (s, h) −                                     → C ′ , (s′ , h′ ) .
                                            a                                             a
                                                                                                       (30)

We will first show that wrlpn JCK (φ | ξ) (s, h) = 1 satisfies all of these criteria for non-
probabilistic and framing enabled programs:
1. For n = 0 we have wrlp0 JCK (φ | ξ) (s, h) = 1, thus this criteria is satisfied.
2. For n > 0 and C = ↓ we have wrlpn J ↓ K (φ | ξ) (s, h) = φ(s, h), thus wrlpn is 1 if and
   only if φ(s, h) = 1.
3. For n > 0 and for all hξ and hF with ξ(s, hξ ) = 1 and h ⊥ hξ ⊥ hF and that
                                                                                                  1
   wrlpn JCK (X | ξ) (s, h) = 1 then for all actions a we do not have C, (s, h ⋆ hξ ) −
                                                                                      → abort,
                                                                                                 a
   since else stepJCK (t) (s, h ⋆ hξ ) = 0 by Statement (30) and wrlpn JCK (X | ξ) (s, h) = 0,
   which contradicts our assumption. Finally since C is framing enabled we also get that
                                         1
   we do not have C, (s, h ⋆ hξ ⋆ hF ) − → abort as well.
                                             a
4. For n > 0 we have that if wrlpn JCK (φ | ξ) (s, h) = 1, then for all hξ with ξ(s, hξ ) = 1
   we have stepJCK λC ′ . wrlpn−1 JC ′ K (φ | ξ) ⋆ ξ (s, h ⋆ hξ ) = 1 by definition of wrlp and
                                                                                  1
                                                                    → C ′ , (s′ , h′ ) we have
   the magic wand. Furthermore, for all transitions C, (s, h ⋆ hξ ) −
                                                                                  a
   h′ = h′′ ⋆ h′ξ with ξ(s′ , h′ξ ) = 1 and wrlpn−1 JC ′ K (φ | ξ) (s′ , h′′ ) = 1 due to the separating
   multiplication with ξ. Finally since C is framing enabled, we also have this argument
                              1
   for C, (s, h ⋆ hξ ⋆ hF ) −→ C ′ , (s′ , h′ ⋆ hF ), finishing this direction.
                                a
Next we show that if all four criteria hold, then wrlpn JCK (φ | ξ) (s, h) = 1:
1. if n = 0 then wrlpn JCK (φ | ξ) (s, h) = 1 holds always.
2. if n > 0 and C = ↓ then φ(s, h) = 1 = wrlpn JCK (φ | ξ) (s, h).
3. if n > 0 and C ̸= ↓ then we especially have for all hξ with ξ(s, hξ ) = 1 that the
                           1                                                              1
   transition C, (s, h) −                                                  → C ′ , (s′ , h′ ⋆h′ξ );
                        → abort does not hold; but all three C, (s, h⋆hξ ) −
                           a                                                              a
   wrlpn−1 JC ′ K (φ | ξ) (s , h′ ) = 1; and ξ(s′ , h′ξ ) = 1 does hold. Then we have:
                            ′


        stepJCK λC ′ . wrlpn−1 JC ′ K (φ | ξ) ⋆ ξ (s, h ⋆ hξ )
                                                     
            n                             o
                               1
       = inf 0 C, (s, h) −     → abort
                               a
           n                                                                                      o
                                                                         1
         ∪ (wrlpn−1 JC K (φ | ξ) ⋆ ξ)(s′ , h′ ⋆ h′ξ ) C, (s, h ⋆ hξ ) −
                            ′
                                                                         → C ′ , (s′ , h′ ⋆ h′ξ )
                                                                           a
                                                                                          (Statement (30))
            n                         o
                         1
       ≥ inf 0 C, (s, h) −
                         → abort
                         a
           n                                                                        o
                                                           1
         ∪ wrlpn−1 JC K (φ | ξ) (s′ , h′ ) C, (s, h ⋆ hξ ) −
                       ′
                                                           → C ′ , (s′ , h′ ⋆ h′ξ )
                                                                a
                                                       (Simplifying the separating multiplication)
            n                                                                          o
                                                               1
       = inf wrlpn−1 JC ′ K (φ | ξ) (s′ , h′ ) C, (s, h ⋆ hξ ) −
                                                               → C ′ , (s′ , h′ ⋆ h′ξ )
                                                                    a
                                                                                (Emptyset eliminiation)
            n                                              o
                                   1
       = inf 1                     → C ′ , (s′ , h′ ⋆ h′ξ )
                   C, (s, h ⋆ hξ ) −                                                  (Criteria assumption)
                                      a
40   Towards Concurrent Quantitative Separation Logic


             =1.

          We have that for all hξ with ξ(s, hξ ) = 1 the above holds, therefore we can now combine
          it with the magic wand and receive

             wrlpn JCK (φ | ξ) (s, h) = ξ −−⋆ stepJCK λC ′ . wrlpn−1 JC ′ K (φ | ξ) ⋆ ξ
                                                                                          
                                                                                               (s, h) = 1 .

          Lastly, we can put everything together:

             ψ ≤ wrlpJCK (φ | ξ)
          iff ∀(s, h). ψ(s, h) = 1 ⇒ wrlpJCK (φ | ξ) (s, h) = 1             (Both sides are qualitative)
          iff ∀(s, h). ψ(s, h) = 1 ⇒ inf{wrlpn JCK (φ | ξ) (s, h) | n ∈ N} = 1                  (Lemma B.4)
          iff ∀(s, h). ψ(s, h) = 1 ⇒ ∀n ∈ N. wrlpn JCK (φ | ξ) (s, h) = 1                          (Analysis)
          iff ∀(s, h). ψ(s, h) = 1 ⇒ ∀n ∈ N. safen (C, s, h, ξ, φ)                                (See above)
          iff ξ |= {ψ} C {φ}                                                               (Definition 4.1)

     Thus finishing the proof.                                                                                ◀


      E       Soundness Proofs for all Proof Rules
     ▶ Lemma E.1 (Monotonicity of wrlp). If Y ≤ Z then wrlpJCK (Y | ξ) ≤ wrlpJCK (Z | ξ).

     Proof. We prove by induction on n that wrlpn JCK (Y | ξ) ≤ wrlpn JCK (Z | ξ). If this holds,
     the inequality for their limits hold as well.
        For the base case n = 0 we have wrlp0 JCK (Y | ξ) = 1 = wrlp0 JCK (Z | ξ).
        We now assume that the claim holds for some arbitrary but fixed n as our induction
     hypothesis.
        For n + 1 we have two cases. The case C = ↓ is again trivial, since wrlpn+1 J ↓ K (Y | ξ) =
     Y ≤ Z = wrlpn+1 J ↓ K (Z | ξ). Finally, for C ̸= ↓ we have:

                   Y ≤Z
          implies wrlpn JC ′ K (Y | ξ) ≤ wrlpn JC ′ K (Z | ξ)                   (Induction Hypothesis)
                            ′                         ′
          implies wrlpn JC K (Y | ξ) ⋆ ξ ≤ wrlpn JC K (Z | ξ) ⋆ ξ                      (Monotonicity of ⋆)
                                ′             ′                         ′          ′
          implies stepJCK (λC . wrlpn JC K (Y | ξ) ⋆ ξ) ≤ stepJCK (λC . wrlpn JC K (Z | ξ) ⋆ ξ)
                                                              (Monotonicity of step, see Lemma B.1)
          implies ξ −−⋆ stepJCK (λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ)
                   ≤ ξ −−⋆ stepJCK (λC ′ . wrlpn JC ′ K (Z | ξ) ⋆ ξ)             (Monotonicity of −−⋆ )
          implies wrlpn+1 JCK (Y | ξ) ≤ wrlpn+1 JCK (Z | ξ)                            (Definition of wrlp)

     This concludes the proof.                                                                                ◀

     ▶ Definition E.2. A program C is a terminating atom if for all stack heap pairs s, h, all
     enabled actions a ∈ Act(C, (s, h)) and probabilities p we have
                     p                                      p
                    → ↓ , (s′ , h′ )
          C, (s, h) −                    or       C, (s, h) −
                                                            → abort .
                     a                                      a


     ▶ Lemma E.3. For terminating atom C, if X ≤ wlpJCK (Y ) then also X ≤ wrlpJCK (Y | ξ).
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                  41


Proof. We show that the statement X ≤ wrlpn JCK (Y | ξ) holds for all n. For n = 0 we have
wrlp0 JCK (Y | ξ) = 1, thus the claim holds immediately. Since C is a terminating atom, we
have stepJCK λC ′ . Y = wlpJCK (Y ). With this, we can prove the case n = 1:

      wrlp1 JCK (Y | ξ)
   = ξ −−⋆ stepJCK (λC ′ . wrlp0 JC ′ K (Y | ξ) ⋆ ξ)                              (Definition of wrlp)
   = ξ −−⋆ stepJCK (1 ⋆ ξ)                                                        (Definition of wrlp)
   = ξ −−⋆ wlpJCK (1 ⋆ ξ)                                                   (C is a terminating atom)
   = ξ −−⋆ (wlpJCK (1) ⋆ ξ)                                                            (Lemma C.11)
   ≥ ξ −−⋆ (wlpJCK (Y ) ⋆ ξ)                                                          (Monotonicity)
   ≥ wlpJCK (Y )                                                                    (Statement (17))
   ≥X                                                                                  (Assumption)

and n > 1:

      wrlpn JCK (Y | ξ)
   = ξ −−⋆ stepJCK λC ′ . wrlpn−1 JC ′ K (Y | ξ) ⋆ ξ
                                                       
                                                                                  (Definition of wrlp)
   = ξ −−⋆ stepJCK (Y ⋆ ξ)         (Definition of wrlp, C is a terminating atom and n − 1 > 0)
   = ξ −−⋆ wlpJCK (Y ⋆ ξ)                                                   (C is a terminating atom)
   = ξ −−⋆ (wlpJCK (Y ) ⋆ ξ)                                                           (Lemma C.11)
   ≥ wlpJCK (Y )                                                                    (Statement (17))
   ≥X                                                                                  (Assumption)

Thus, the proof is finished.                                                                       ◀

▶ Lemma E.4. If X ≤ wrlpJC1 K (Y | ξ) and Y                   ≤ wrlpJC2 K (Z | ξ) then also for the
sequential composition X ≤ wrlpJC1 ; C2 K (Z | ξ).

Proof. We prove by induction on n that

   wrlpn JC1 K (wrlpn JC2 K (Y | ξ) | ξ) ≤ wrlpn JC1 ; C2 K (Z | ξ) .

If this holds, the inequality also holds for their limits. Finally, we can use monotonicity of
wrlp to prove that the claim holds.
    For the induction base with n = 0, we have wrlp0 JC1 K (wrlp0 JC2 K (Z | ξ) | ξ) = 1 =
wrlp0 JC1 ; C2 K (Z | ξ).
    We assume that the claim holds for some arbitrary but fixed n as the induction hypo-
thesis.
                                                                  p
    For the induction step, we have two cases, for C1 , (s, h) − → C1′ , (s′ , h′ ) either C1′ = ↓
                                                                        a
or C1′ ̸= ↓ . We will only consider the case C1′ ̸= ↓ , since the other is analogous. Then we
have:

      wrlpn+1 JC1 ; C2 K (Z | ξ)
   = ξ −−⋆ stepJC1 ; C2 K (λC ′ . wrlpn JC ′ K (Z | ξ) ⋆ ξ)                       (Definition of wrlp)
                           ′           ′
   ≥ ξ −−⋆ stepJC1 K (λC . wrlpn JC K (wrlpn JC2 K (Z | ξ) | ξ) ⋆ ξ)
                                                                        (Monotonicity of −−⋆ and †)
   = wrlpn+1 JC1 K (wrlpn JC2 K (Z | ξ) | ξ)                                      (Definition of wrlp)
42   Towards Concurrent Quantitative Separation Logic

                                                  
        ≥ wrlpn+1 JC1 K wrlpn+1 JC2 K (Z | ξ) | ξ
                         (Antitonicity of wrlp w.r.t. n and monotonicity w.r.t. postexpectation)

     For †, we have:

          stepJC1 ; C2 K (λC ′ . wrlpn JC ′ K (Z | ξ) ⋆ ξ) (s, h)
              Xh
        = inf        p · (wrlpn JC1′ ; C2 K (Z | ξ) ⋆ ξ)(s′ , h′ )
                                                                i                                   
                                    p
                  C1 ; C2 , (s, h) −
                                   →        C1′ ; C2 , (s′ , h′ )       a ∈ Act(C1 ; C2 , (s, h))
                                    a
                                                                                                        (Definition of step)
              Xh
        ≥ inf    p · (wrlpn JC1′ K (wrlpn JC2 K (Z | ξ) | ξ) ⋆ ξ)(s′ , h′ )
                                                                    i                               
                                    p
                                   → C1′ ; C2 , (s′ , h′ )
                  C1 ; C2 , (s, h) −                                    a ∈ Act(C1 ; C2 , (s, h))
                                    a
                                                               (Induction hypothesis and monotonicity)
              Xh
        = inf        p · (wrlpn JC1′ K (wrlpn JC2 K (Z | ξ) | ξ) ⋆ ξ)(s′ , h′ )
                                              i                       
                             p    ′     ′   ′
               C1 , (s, h) −→ C1 , (s , h ) a ∈ Act(C1 , (s, h))
                                a
                                                           (Operational semantics of sequential composition)
                          ′             ′
        = stepJC1 K (λC . wrlpn JC K (wrlpn JC2 K (Z | ξ) | ξ) ⋆ ξ) (s, h)                              (Definition of step)

     Thus, the claim is proven.                                                                                          ◀

     ▶ Lemma E.5. If X1 ≤ wrlpJC1 K (Y | ξ), X2 ≤ wrlpJC2 K (Y | ξ) and X ≤ [b]·X1 +[¬b]·X2
     then also X ≤ wrlpJif ( b ) { C1 } else { C2 }K (Y | ξ).

     Proof. We prove that for all n we have [b] · wrlpn JC1 K (Y | ξ) + [¬b] · wrlpn JC2 K (Y | ξ) ≤
     wrlpn Jif ( b ) { C1 } else { C2 }K (Y | ξ), where [b] (s, h) = 1 if s ∈ b and [¬b] (s, h) = 0
     if s ̸∈ b. Then the inequality holds also for their limits and due to monotonicity of all
     operations, we also get the claim.
         For the case n = 0, we have that wrlp0 Jif ( b ) { C1 } else { C2 }K (Y | ξ) = 1 ≥ [b] ·
     wrlp0 JC1 K (Y | ξ) + [¬b] · wrlp0 JC2 K (Y | ξ), thus the claim holds.
         For the case n + 1, we have two sub-cases. Either s ∈ b or s ̸∈ b. We will only prove the
     first, since the latter is analogous. There we have:

           wrlpn+1 Jif ( b ) { C1 } else { C2 }K (Y | ξ) (s, h)
        = ξ −−⋆ stepJif ( b ) { C1 } else { C2 }K (λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ) (Definition of wrlp)
        = ξ −−⋆ (wrlpn JC1 K (Y | ξ) ⋆ ξ)                                                                    (†, see below)
        ≥ wrlpn JC1 K (Y | ξ)                                                                             (Statement (17))
        ≥ wrlpn+1 JC1 K (Y | ξ)                                                                (Monotonicity w.r.t n)

     For †, we have:

          stepJif ( b ) { C1 } else { C2 }K (λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ) (s, h)
              Xh
        = inf        p · (wrlpn JC ′ K (Y | ξ) ⋆ ξ)(s′ , h′ )
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                      43


                                                       p
                                                                         i
                 if ( b ) { C1 } else { C2 } , (s, h) −→ C ′ , (s′ , h′ )
                                                       a
                                                           
             a ∈ Act(if ( b ) { C1 } else { C2 } , (s, h))                            (Definition of step)
       Xh
   =     1 · (wrlpn JC1 K (Y | ξ) ⋆ ξ)(s, h)
                                                                 i
                                                    1
             if ( b ) { C1 } else { C2 } , (s, h) −−→ C1 , (s, h)                                  (s ∈ b)
                                                    if-t

   = (wrlpn JC1 K (Y | ξ) ⋆ ξ)(s, h)                                                      (Singleton set)

For s ̸∈ b we similarly have

   wrlpn+1 Jif ( b ) { C1 } else { C2 }K (Y | ξ) ≥ wrlpn+1 JC2 K (Y | ξ) .

Combining them, we have the claim from above.                                                          ◀


▶ Lemma E.6. If I ≤ [b] · X + [¬b] · Y and X ≤ wrlpJCK (I | ξ) then for the loop we have
I ≤ wrlpJwhile ( b ) { C }K (Y | ξ).

Proof. We will now prove by induction on n that if I ≤ [b] · wrlpJCK (I | ξ) + [¬b] · Y then
I ≤ wrlpn Jwhile ( b ) { C }K (Y | ξ). If this holds for all n, then also for the limit.
   For the base case n = 0, we have wrlp0 JCK (Y | ξ) = 1 ≥ I.
   Now we assume that for some fixed but arbitrary n the claim holds as our induction
hypothesis.
   For the induction step, we have two cases. If s ̸∈ b then:

       wrlpn+1 Jwhile ( b ) { C }K (Y | ξ) (s, h)
   = (ξ −−⋆ stepJwhile ( b ) { C }K (λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ))(s, h)          (Definition of wrlp)
   = (ξ −−⋆ (wrlpn J ↓ K (Y | ξ) ⋆ ξ))(s, h)                                               (†, see below)
   ≥ wrlpn J ↓ K (Y | ξ) (s, h)                                                         (Statement (17))
   ≥ Y (s, h)                                                                         (Definition of wrlp)
   ≥ ([b] · wrlpJCK (I | ξ) + [¬b] · Y )(s, h)                                              (Since s ̸∈ b)
   ≥ I(s, h)                                                                               (Assumption)

For †, we have:

     stepJwhile ( b ) { C }K (λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ) (sh)
         Xh                                                                                             i
                                                                                       p
   = inf        p · (wrlpn JC ′ K (Y | ξ) ⋆ ξ)(s′ , h′ ) | while ( b ) { C } , (s, h) −
                                                                                      → C ′ , (s′ , h′ )
                                                                                       a
                                                  
           a ∈ Act(while ( b ) { C } , (s, h))                                        (Definition of step)
     X                                                                           1
                                                                                                
   =      1 · (wrlpn J ↓ K (Y | ξ) ⋆ ξ)(s, h) | while ( b ) { C } , (s, h) −−−→ ↓ , (s, h)
                                                                             loop-f
                                                           (Operational semantics of loop and s ̸∈ b)
   = wrlpn J ↓ K (Y | ξ) ⋆ ξ)(s, h)                                               (Sum over singleton)
44   Towards Concurrent Quantitative Separation Logic


     Then for s ∈ b we have:
           wrlpn+1 Jwhile ( b ) { C }K (Y | ξ) (s, h)
         = (ξ −−⋆ stepJwhile ( b ) { C }K (λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ))(s, h)       (Definition of wrlp)
         = (ξ −−⋆ (wrlpn JC ; while ( b ) { C }K (Y | ξ) ⋆ ξ))(s, h)                                       (††)
         ≥ wrlpn JC ; while ( b ) { C }K (Y | ξ) (s, h)                                     (Statement (17))
         ≥ wrlpn JCK (wrlpn Jwhile ( b ) { C }K (Y | ξ) | ξ) (s, h)                             (Lemma E.4)
         ≥ wrlpn JCK (I | ξ) (s, h)
                      (Induction hypothesis and Monotonicity of wrlpn w.r.t to postexpectation)
         ≥ wrlpJCK (I | ξ) (s, h)                                                               (Lemma B.4)
         ≥ ([b] · wrlpJCK (I | ξ) + [¬b] · Y )(s, h)                                             (Since s ∈ b)
         ≥I                                                                                    (Assumption)
     For †† we have:
           stepJwhile ( b ) { C }K (λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ) (sh)
               Xh                                                                                             i
                                                                                             p
         = inf        p · (wrlpn JC ′ K (Y | ξ) ⋆ ξ)(s′ , h′ ) | while ( b ) { C } , (s, h) −
                                                                                            → C ′ , (s′ , h′ )
                                                                                             a
                                                        
                 a ∈ Act(while ( b ) { C } , (s, h))                                        (Definition of step)
           X   h
         =      1 · (wrlpn JC ; while ( b ) { C }K (Y | ξ) ⋆ ξ)(s, h)
                                                                                       i
                                                1
                 while ( b ) { C } , (s, h) −−−−→ C ; while ( b ) { C }, (s, h)
                                              loop-t
                                                               (Operational semantics of loop and s ∈ b)
         = wrlpn JC ; while ( b ) { C }K (Y | ξ) ⋆ ξ)(s, h)                             (Sum over singleton)
     Thus, the claim is proven.                                                                                ◀

     ▶ Lemma E.7. If X1 ≤ wrlpJC1 K (Y | ξ), X2 ≤ wrlpJC2 K (Y | ξ) and X ≤ ep · X1 + (1 −
     ep ) · X2 then X ≤ wrlpJ{ C1 } [ ep ] { C2 }K (Y | ξ).
     Proof. We prove for all n that
         ep · wrlpn JC1 K (Y | ξ) + (1 − ep ) · wrlpn JC2 K (Y | ξ) ≤ wrlpn J{ C1 } [ ep ] { C2 }K (Y | ξ) .
     If this holds, then the same also holds for their limits and thus by monotonicity of all
     operations the claim is proven.
         For the case n = 0 we have wrlp0 J{ C1 } [ ep ] { C2 }K (Y | ξ) = 1 ≥ ep · wrlpn JC1 K (Y | ξ) +
     (1 − ep ) · wrlpn JC2 K (Y | ξ).
         For the case n + 1 we have
           wrlpn+1 J{ C1 } [ ep ] { C2 }K (Y | ξ)
         = ξ −−⋆ stepJ{ C1 } [ ep ] { C2 }K (λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ)            (Definition of step)
         = ξ −−⋆ (ep · wrlpn JC1 K (Y | ξ) ⋆ ξ + (1 − ep ) · wrlpn JC2 K (Y | ξ) ⋆ ξ)           (†, see below)
         ≥ ξ −−⋆ ((ep · wrlpn JC1 K (Y | ξ) + (1 − ep ) · wrlpn JC2 K (Y | ξ)) ⋆ ξ)
                                                  (Subdist. of ⋆ with plus and monotonicity of −−⋆ )
         ≥ (ep · wrlpn JC1 K (Y | ξ) + (1 − ep ) · wrlpn JC2 K (Y | ξ))                     (Statement (17))
         ≥ (ep · wrlpn+1 JC1 K (Y | ξ) + (1 − ep ) · wrlpn+1 JC2 K (Y | ξ))
                                                                          (Antitonicity of wrlpn w.r.t n)
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                          45


Now for †:

     stepJ{ C1 } [ ep ] { C2 }K (λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ) (s, h)
         Xh                                                                                                 i
                                                                                          p
   = inf        p · (wrlpn JC ′ K (Y | ξ) ⋆ ξ)(s′ , h′ ) | { C1 } [ ep ] { C2 } , (s, h) −→ C ′ , (s′ , h′ )
                                                                                          a
                                                     
           a ∈ Act({ C1 } [ ep ] { C2 } , (s, h))                                       (Definition of step)
                                                                                                       
     X
                         ′                 ′  ′                                       p      ′   ′   ′
   =      p · (wrlpn JC K (Y | ξ) ⋆ ξ)(s , h ) | { C1 } [ ep ] { C2 } , (s, h) −−−→ C , (s , h )
                                                                                   prob
                                                              (Operational semantics of prob. choice)
   = ep (s) · (wrlpn JC1 K (Y | ξ) ⋆ ξ)(s, h) + (1 − ep )(s) · (wrlpn JC2 K (Y | ξ) ⋆ ξ)(s, h)
                                                          (Operational semantics of prob. choice)
   = (ep · wrlpn JC1 K (Y | ξ) ⋆ ξ + (1 − ep ) · wrlpn JC2 K (Y | ξ) ⋆ ξ)(s, h)
                                                                               (Pointwise operations)

Thus, the claim is proven.                                                                                 ◀

▶ Lemma E.8. If X ⋆ ξ ≤ wrlpJCK (Y ⋆ ξ | [emp]) then X ≤ wrlpJatomic { C }K (Y | ξ).

Proof. We prove for all n that X ≤ wrlpn Jatomic { C }K (Y | ξ).
   For n = 0 we have wrlp0 Jatomic { C }K (Y | ξ) = 1 ≥ X.
   For n + 1 > 0 and where C is tame we have

      wrlpn+1 Jatomic { C }K (Y | ξ)
   = ξ −−⋆ stepJatomic { C }K (λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ)                       (Definition of wrlp)
   ≥ ξ −−⋆ wlpJCK (Y ⋆ ξ)                                                                    (†, see below)
   = ξ −−⋆ wrlpJCK (Y ⋆ ξ | [emp])                                                        (Theorem B.10)
   ≥ ξ −−⋆ (X ⋆ ξ)                                                                           (Assumption)
   ≥X                                                                                     (Statement (17))

For †, we have:

     ξ −−⋆ stepJatomic { C }K (λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ)
                        X
                                p · (wrlpn JC ′ K (Y | ξ) ⋆ ξ)(s′ , h′ )
                               
   = ξ −−⋆ λ(s, h). inf

                                                    p
                                                    → C ′ , (s′ , h′ )
                                                                      
                              atomic { C } , (s, h) −
                                                    a
                                            !
             a ∈ Act(atomic { C } , (s, h))                                           (Definition of step)
                           Xh
   = ξ −−⋆       λ(s, h).     p · (wrlpn JC ′ K (Y | ξ) ⋆ ξ)(s′ , h′ )

                                               p
                                                                  i
                    atomic { C } , (s, h) −−−−→ C ′ , (s′ , h′ )
                                             atomic
                                                               (Act(atomic { C } , (s, h)) is singleton)
                           Xh
   = ξ −−⋆       λ(s, h).     p · (wrlpn J ↓ K (Y | ξ) ⋆ ξ)(s′ , h′ )
                                              p
                                                                 i
                    atomic { C } , (s, h) −−−−→ ↓ , (s′ , h′ )
                                             atomic
46   Towards Concurrent Quantitative Separation Logic


              Xh                                          
          +        p · (wrlpn JdivergeK (Y | ξ) ⋆ ξ)(s, h)
                                                                                      !
                                                p
                                                                                     i
                   atomic { C } , (s, h) −−−−→ diverge, (s, h)
                                             atomic

                                                                                          (Splitting reachable programs)
                               Xh
        = ξ −−⋆     λ(s, h).        p · (wrlpn J ↓ K (Y | ξ) ⋆ ξ)(s′ , h′ )

                                                     p
                                                                                 i
                      atomic { C } , (s, h) −−−−→ ↓ , (s′ , h′ )
                                                atomic
                                                                                                                !
              Xh                                                             p
                                                                                                               i
          +        p · (1 ⋆ ξ)(s, h) atomic { C } , (s, h) −−−−→ diverge, (s, h)                                     (Lemma C.9)
                                                                           atomic

                               Xh                                                   p
                                                                                                      i
        ≥ ξ −−⋆     λ(s, h).        p · (Y ⋆ ξ)(s′ , h′ ) | atomic { C } , (s, h) −−−−→ ↓ , (s′ , h′ )
                                                                                                  atomic
                                                                                                                !
              Xh                                                             p
                                                                                                               i
          +        p · (1 ⋆ ξ)(s, h) atomic { C } , (s, h) −−−−→ diverge, (s, h)
                                                                           atomic

                                                                                                               (Definition of wrlp)
                               Xh                                                p
                                                                                                           i
        ≥ ξ −−⋆     λ(s, h).        p · (Y ⋆ ξ)(s′ , h′ ) | C, (s, h) −
                                                                      →∗                  ↓ , (s′ , h′ )
                                                                       !
              Xh                                    p ∗
                                                                   i
          +        p · (1 ⋆ ξ)(s, h) C, (s, h) −
                                               →           ...

                                                                 (Operational semantics of atomic regions)
                               Xh                                     p
                                                                                        i
        = ξ −−⋆     λ(s, h).        p · (Y ⋆ ξ)(s′ , h′ ) | C, (s, h) −
                                                                      →∗ ↓ , (s′ , h′ )
                                                               !
              Xh                              p ∗
                                                           i
          +        p · (1)(s, h) C, (s, h) −
                                           →         ...

                  (Since there exists hξ with ξ(s, hξ ) = 1 and h = hξ ⋆ h′ for some h′ due to −−⋆ )
        = ξ −−⋆ wlpJCK (Y ⋆ ξ)                                                                                 (Definition of wlp)


        The difficulty of this proof would have been far greater, if we had allowed non-tame
     programs in atomic regions. Since we block when encountering non-tame programs, we have
     wrlpn+1 Jatomic { C }K (Y | ξ) = ξ −−⋆ stepJCK λC ′ . wrlpn JC ′ K (Y | ξ) ⋆ ξ = ξ −−⋆ 1 = 1 ≥
     X.
        Thus, the claim is proven.                                                                ◀

     ▶ Lemma E.9. If X ≤ wrlpJCK (Y | ξ ⋆ π) then X ⋆ ξ ≤ wrlpJCK (Y ⋆ ξ | π).

     Proof. To prove this, we first prove by induction on n that for all programs C we have the
     inequality wrlpn JCK (Y | π ⋆ ξ) ⋆ ξ ≤ wrlpn JCK (Y ⋆ ξ | π).
         For the induction base n = 0, the claim holds trivially as wrlp0 JCK (Y ⋆ ξ | π) = 1.
        We now assume that the claim holds for some arbitrary but fixed n as our induction
     hypothesis.
         For the induction step, we have two cases. If C = ↓ then we have that the equality
     wrlpn+1 J ↓ K (Y ⋆ ξ | π) = Y ⋆ ξ = wrlpn+1 J ↓ K (Y | π ⋆ ξ) ⋆ ξ holds. Thus, we assume that
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                  47


C ̸= ↓ . There we prove now

      ξ −−⋆ wrlpn+1 JCK (Y ⋆ ξ | π)
   = ξ −−⋆ (π −−⋆ stepJCK (λC ′ . wrlpn JC ′ K (Y ⋆ ξ | π) ⋆ π))                 (Definition of wrlp)
                                 ′           ′
   = (ξ ⋆ π) −−⋆ stepJCK (λC . wrlpn JC K (Y ⋆ ξ | π) ⋆ π)                           (Statement (23))
                                 ′           ′
   ≥ (ξ ⋆ π) −−⋆ stepJCK (λC . wrlpn JC K (Y | ξ ⋆ π) ⋆ ξ ⋆ π)               (Induction Hypothesis)
   = wrlpn+1 JCK (Y | ξ ⋆ π)                                                     (Definition of wrlp)

and we have

       wrlpn+1 JCK (Y | π ⋆ ξ) ≤ ξ −−⋆ wrlpn+1 JCK (Y ⋆ ξ | π)
   iff wrlpn+1 JCK (Y | π ⋆ ξ) ⋆ ξ ≤ wrlpn+1 JCK (Y ⋆ ξ | π)

by adjointness (cf. Statement (15)).
   Lastly we now have:

      wrlpJCK (Y ⋆ ξ | π)
   = lim wrlpn JCK (Y ⋆ ξ | π)                                                   (Definition of wrlp)
      n→∞

   ≥ lim wrlpn JCK (Y | π ⋆ ξ) ⋆ ξ                                                         (See above)
      n→∞

   = wrlpJCK (Y | π ⋆ ξ) ⋆ ξ                                                     (Definition of wrlp)
   ≥ X ⋆ξ                                                                              (Assumption)

Thus, the claim is proven.                                                                          ◀

▶ Lemma E.10. If X1 ≤ wrlpJC1 K (Y1 | ξ), X2 ≤ wrlpJC2 K (Y2 | ξ) and Write(Ci ) ∩
Vars (C3−i , Y3−i , ξ) = ∅ then X1 ⋆ X2 ≤ wrlpJ( C1 ∥ C2 )K (Y1 ⋆ Y2 | ξ).

Proof. We instead prove that we have

   wrlpn JC1 K (Y1 | ξ) ⋆ wrlpn JC2 K (Y2 | ξ) ≤ wrlpn J( C1 ∥ C2 )K (Y1 ⋆ Y2 | ξ)

by induction on n. If this holds for all n, the same holds for the limit, which yields the
claim.
    For the induction base n = 0, we have

   wrlp0 J( C1 ∥ C2 )K (Y1 ⋆ Y2 | ξ) = 1 = wrlp0 JC1 K (Y1 | ξ) ⋆ wrlp0 JC2 K (Y2 | ξ) .

   We assume that the claim holds for some arbitrary but fixed n as our induction hypo-
thesis.
   For the induction step, we have four cases. If C1 = C2 = ↓ we have:

      wrlpn+1 J( ↓ ∥ ↓ )K (Y1 ⋆ Y2 | ξ)
   = ξ −−⋆ stepJ( ↓ ∥ ↓ )K (λC ′ . wrlpn JC ′ K (Y1 ⋆ Y2 | ξ) ⋆ ξ)               (Definition of wrlp)
   ≥ ξ −−⋆ (Y1 ⋆ Y2 ⋆ ξ)                                   (Monotonicity of −−⋆ and †, see below)
   ≥ Y1 ⋆ Y2                                                                         (Statement (17))
   = wrlpn+1 J ↓ K (Y1 | ξ) ⋆ wrlpn+1 J ↓ K (Y2 | ξ)                             (Definition of wrlp)

For †, we have:

      stepJ( ↓ ∥ ↓ )K (λC ′ . wrlpn JC ′ K (Y1 ⋆ Y2 | ξ) ⋆ ξ) (s, h)
48   Towards Concurrent Quantitative Separation Logic

             Xh                                                                                         i
                                                                                       p
       = inf        p · (wrlpn JC ′ K (Y1 ⋆ Y2 | ξ) ⋆ ξ)(s′ , h′ ) | ( ↓ ∥ ↓ ), (s, h) −
                                                                                       → C ′ , (s′ , h′ )
                                                                                       a
                                             
               a ∈ Act(( ↓ ∥ ↓ ), (s, h))                                              (Definition of step)
             h                                                                                 i
                                                                                1
         X
       =      wrlpn J ↓ K (Y1 ⋆ Y2 | ξ) ⋆ ξ)(s, h) | ( ↓ ∥ ↓ ), (s, h) −−−−−→ ↓ , (s, h)
                                                                            conc-end
                                                                (Operational semantics of concurrency)
       = wrlpn J ↓ K (Y1 ⋆ Y2 | ξ) ⋆ ξ)(s, h)                                            (Sum of singleton)
       ≥ (Y1 ⋆ Y2 ⋆ ξ)(s, h)                                                            (Definition of wrlp)

       For the case C1 ̸= ↓ and C2 ̸= ↓ we have:

          wrlpn+1 J( C1 ∥ C2 )K (Y1 ⋆ Y2 | ξ)
       = ξ −−⋆ stepJ( C1 ∥ C2 )K (λC ′ . wrlpn JC ′ K (Y1 ⋆ Y2 | ξ) ⋆ ξ)            (Definition of wrlp)
                   
       = ξ −−⋆ min stepJC1 K (λC1′ . wrlpn J C1′ ∥ C2 K (Y1 ⋆ Y2 | ξ) ⋆ ξ) ,
                                                                         
                                ′                    ′
                  stepJC2 K (λC2 . wrlpn J C1 ∥ C2 K (Y1 ⋆ Y2 | ξ) ⋆ ξ)                  (††, see below)
                   
       ≥ ξ −−⋆ min stepJC1 K (λC1′ . wrlpn JC1′ K (Y1 | ξ) ⋆ wrlpn JC2 K (Y2 | ξ) ⋆ ξ) ,
                                                                                    
                                ′                                    ′
                  stepJC2 K (λC2 . wrlpn JC1 K (Y1 | ξ) ⋆ wrlpn JC2 K (Y2 | ξ) ⋆ ξ)
                                                     (Induction Hypothesis and Vars (Ci′ ) ⊆ Vars (Ci ))
                  
       ≥ ξ −−⋆ min stepJC1 K (λC1′ . wrlpn JC1′ K (Y1 | ξ) ⋆ ξ) ⋆ wrlpn JC2 K (Y2 | ξ) ,
                                                                                     
                 stepJC2 K (λC2′ . wrlpn JC2′ K (Y2 | ξ) ⋆ ξ) ⋆ wrlpn JC1 K (Y1 | ξ)
                    (Theorem C.12 and Vars (wrlpn JCi K (Yi | ξ)) ⊆ Vars (Ci , Yi , ξ) by Lemma C.8)
               
       = min ξ −−⋆ stepJC1 K (λC1′ . wrlpn JC1′ K (Y1 | ξ) ⋆ ξ) ⋆ wrlpn JC2 K (Y2 | ξ) ,
                                                                                        
                                  ′            ′
                  ⋆
              ξ −− stepJC2 K (λC2 . wrlpn JC2 K (Y2 | ξ) ⋆ ξ) ⋆ wrlpn JC1 K (Y1 | ξ)
                                                                             (−−⋆ is distributiv with min)
               
       ≥ min       (ξ −−⋆ stepJC1 K (λC1′ . wrlpn JC1′ K (Y1 | ξ) ⋆ ξ)) ⋆ wrlpn JC2 K (Y2 | ξ) ,
                                                                                                
                                         ′            ′
                    (ξ −−⋆ stepJC2 K (λC2 . wrlpn JC2 K (Y2 | ξ) ⋆ ξ)) ⋆ wrlpn JC1 K (Y1 | ξ)
                                                                                           (Statement (24))
               
       = min wrlpn+1 JC1 K (Y1 | ξ) ⋆ wrlpn JC2 K (Y2 | ξ) ,
                                                            
              wrlpn+1 JC2 K (Y2 | ξ) ⋆ wrlpn JC1 K (Y1 | ξ)                             (Definition of wrlp)
            
       ≥ min wrlpn+1 JC1 K (Y1 | ξ) ⋆ wrlpn+1 JC2 K (Y2 | ξ) ,
                                                              
              wrlpn+1 JC2 K (Y2 | ξ) ⋆ wrlpn+1 JC1 K (Y1 | ξ)                  (wrlpn is antitone w.r.t. n)
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                                  49


   = wrlpn+1 JC1 K (Y1 | ξ) ⋆ wrlpn+1 JC2 K (Y2 | ξ)                                              (Set is a singleton)

For †† we prove:

     stepJ( C1 ∥ C2 )K (λC ′ . wrlpn JC ′ K (Y1 ⋆ Y2 | ξ) ⋆ ξ) (s, h ⋆ hξ )
         X
                p · (wrlpn JC ′ K (Y1 ⋆ Y2 | ξ) ⋆ ξ)(s′ , h′ )
               
   = inf
                                                                                                          
                                         p      ′   ′
                                                         ′
                                       → C , (s , h ) a ∈ Act(( C1 ∥ C2 ), (s, h ⋆ hξ ))
             ( C1 ∥ C2 ), (s, h ⋆ hξ ) −
                                         a
                                                                                                  (Definition of step)
                  nX
   = min       inf    p · (wrlpn J C1′ ∥ C2 K (Y1 ⋆ Y2 | ξ) ⋆ ξ)(s′ , h′ )
                                       p
                                                                                    o
                                      → C1′ , (s′ , h′ ) a ∈ Act(C1 , (s, h ⋆ hξ )) ,
                                                        
                    C1 , (s, h ⋆ hξ ) −
                                       a
                   nX
               inf       p · (wrlpn J C1 ∥ C2′ K (Y1 ⋆ Y2 | ξ) ⋆ ξ)(s′ , h′ )
                                       p
                                                                                    o
                                      → C2′ , (s′ , h′ ) a ∈ Act(C2 , (s, h ⋆ hξ ))
                                                        
                    C2 , (s, h ⋆ hξ ) −
                                         a
                                                                    (Operational Semantics of concurrency)
           
   = min stepJC1 K (λC1′ . wrlpn J C1′ ∥ C2 K (Y1 ⋆ Y2 | ξ) ⋆ ξ) ,
                                                                  
                        ′                  ′
          stepJC2 K (λC2 . wrlpn J C1 ∥ C2 K (Y1 ⋆ Y2 | ξ) ⋆ ξ)                                   (Definition of step)

The cases C1 ̸= ↓ , C2 = ↓ and C1 = ↓ , C2 ̸= ↓ are analogous to the previous case. We
just drop the minimum, since only one thread can be executed.
    Thus, the claim is proven.                                                       ◀

▶ Definition E.11. A program C is almost surely terminating w.r.t. S iff for all schedulers
                                                      0
                                                      →∗ . . . .
s ∈ S and all program states (s, h) we have C, (s, h) −
                                                                      s

                                  S                            S
▶ Lemma E.12. If X1 ≤ wlp JCK (Y1 ), X2 ≤ wlp JCK (Y2 ) and C ist almost surely termin-
ating w.r.t. S then a · X1 + X2 ≤ wlpS JCK (a · Y1 + Y2 ).

Proof. We have:

     wlpS JCK (a · Y1 + Y2 ) (s, h)
         Xh                                                                            i
                                                         p
   = inf        p · (a · Y1 + Y2 )(s′ , h′ ) | C, (s, h) −
                                                         →∗               ↓ , (s′ , h′ ) + pdiv
                                                         s
                                                  
                                    pdiv
           s ∈ S and C, (s, h) −−−→∗ . . .                                                        (Definition of wlp)
                                     s
         Xh                                                                            i         
                                                         p
   = inf        p · (a · Y1 + Y2 )(s′ , h′ ) | C, (s, h) −
                                                         →∗               ↓ , (s′ , h′ ) s ∈ S
                                                                s
                                                              (C is almost surely terminating w.r.t. S)
           Xh                                                                       i      
                                 ′   ′          ′   ′               p ∗        ′   ′
   = inf           p · (a · Y1 (s , h )) + Y2 (s , h ) | C, (s, h) −
                                                                   →     ↓ , (s , h ) s ∈ S
                                                                           s
                                                                                          (Pointwise application)
           Xh                                                              i
                                                    p
   = inf           p · a · Y1 (s′ , h′ ) | C, (s, h) −
                                                     →∗       ↓ , (s′ , h′ )
                                                    s
50   Towards Concurrent Quantitative Separation Logic


                   Xh                                                i      
                               ′   ′              p ∗          ′   ′
               +    p · Y2 (s , h ) | C, (s, h) − →      ↓ , (s , h ) s ∈ S              (Linearity of sum)
                                                  s
                  Xh                                                            i   
                                     ′  ′                 p ∗            ′     ′
        ≥ inf          p · a · Y1 (s , h ) | C, (s, h) − →        ↓ , (s , h ) s ∈ S
                                                          s
                 Xh                                                        i      
                                ′   ′                p ∗           ′    ′
          + inf       p · Y2 (s , h ) | C, (s, h) − →       ↓ , (s , h ) s ∈ S             (Statement (7))
                                                     s
                  Xh                                                        i     
                                  ′   ′               p ∗            ′    ′
        ≥ a · inf      p · Y1 (s , h ) | C, (s, h) − →        ↓ , (s , h ) s ∈ S
                                                      s
                  Xh                                                        i     
                                  ′   ′               p ∗            ′    ′
          + inf        p · Y2 (s , h ) | C, (s, h) − →        ↓ , (s , h ) s ∈ S
                                                     s
                                                                             (Factorisation with constant)
                   S                   S
        = a · wlp JCK (Y1 ) + wlp JCK (Y2 )

                                                                                                        ◀

     ▶ Lemma E.13. If X ≤ wrlpJCK (Y | [emp]) then X ≤ wlpS JCK (Y ).

     Proof. Since S ⊆ S we have wlpJCK (Y ) ≤ wlpS JCK (Y ). Furthermore, by Theorem B.10 we
     have wrlpJCK (Y | [emp]) = wlpJCK (Y ). Thus, we also have X ≤ wlpS JCK (Y ).         ◀

     ▶ Lemma E.14. If X ≤ wrlpJCK (Y | ξ) and Write(C) ∩ Vars (Z) = ∅ then we also have
     X ⋆ Z ≤ wrlpJCK (Y ⋆ Z | ξ).

     Proof. First, it is easy to prove that wrlpJCK (Y ⋆ Z | ξ) = wrlpJ( C ∥ ↓ )K (Y ⋆ Z | ξ). From
     this, we directly have the conclusion by Lemma E.10.                                         ◀

     ▶ Lemma E.15. If C is a terminating atom and X ⋆ ξ ≤ wrlpJCK (Y ⋆ ξ | [emp]) then
     X ≤ wrlpJCK (Y | ξ).

     Proof. Since C is a terminating atom, we have wrlpJCK (Y | ξ) = wrlpJatomic { C }K (Y | ξ)
     and by Lemma E.8 together with the assumption we have wrlpJatomic { C }K (Y | ξ) ≥ X,
     which proves the claim.                                                                 ◀

     ▶ Lemma E.16. If X1 ≤ wrlpJCK (Y1 | ξ) and X2 ≤ wrlpJCK (Y2 | ξ) then we have for the
     maximum max { X1 , X2 } ≤ wrlpJCK (max { Y1 , Y2 } | ξ).

     Proof. By monotonicity (Lemma E.1) we have for both i ∈ {1, 2} that the inequality
     wrlpJCK (Yi | ξ) ≤ wrlpJCK (max { Y1 , Y2 } | ξ) holds, thus for both i ∈ {1, 2} the inequal-
     ity Xi ≤ wrlpJCK (max { Y1 , Y2 } | ξ) also holds. Then we also have that the inequality
     max { X1 , X2 } ≤ wrlpJCK (max { Y1 , Y2 } | ξ) holds.                                    ◀

     ▶ Lemma E.17. If X1 ≤ wrlpJCK (Y1 | ξ), X2 ≤ wrlpJCK (Y2 | ξ), ξ is precise and C is
     not probabilistic then min { X1 , X2 } ≤ wrlpJCK (min { X2 , Y2 } | ξ).

     Proof. We prove instead by induction on n that the equality

        min { wrlpn JCK (Y1 | ξ), wrlpn JCK (Y2 | ξ) } = wrlpn JCK (min { Y1 , Y2 } | ξ)

     holds. If this holds, the claim also holds.
        For the induction base n = 0, we have that wrlp0 JCK (min { Y1 , Y2 } | ξ) = 1, which is
     always equal to min { wrlp0 JCK (Y1 | ξ), wrlp0 JCK (Y2 | ξ) }.
        Thus, we assume for some arbitrary but fixed n the claim holds as our induction hypo-
     thesis.
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                          51


   For the induction step, we have two cases. For C = ↓ we have

      wrlpn+1 J ↓ K (min { Y1 , Y2 } | ξ)
   = min { Y1 , Y2 }
         
   = min wrlpn+1 J ↓ K (Y1 | ξ), wrlpn+1 J ↓ K (Y2 | ξ)          .

For C ̸= ↓ we have

      wrlpn+1 JCK (min { Y1 , Y2 } | ξ)
   = ξ −−⋆ stepJCK (λC ′ . wrlpn JC ′ K (min { Y1 , Y2 } | ξ) ⋆ ξ)                        (Definition of wrlp)
   = ξ −−⋆ stepJCK (λC ′ . min { wrlpn JC ′ K (Y1 | ξ), wrlpn JC ′ K (Y2 | ξ) } ⋆ ξ)
                                                                              (Induction Hypothesis)
   = ξ −−⋆ stepJCK (λC ′ . min { wrlpn JC ′ K (Y1 | ξ) ⋆ ξ, wrlpn JC ′ K (Y2 | ξ) ⋆ ξ })
                                                                   (ξ precise and Statement (25))
   = ξ −−⋆ min{stepJCK (λC ′ . wrlpn JC ′ K (Y1 | ξ) ⋆ ξ) ,
               stepJCK (λC ′ . wrlpn JC ′ K (Y2 | ξ) ⋆ ξ)}                                     (†, see below)
        n
   = min ξ −−⋆ stepJCK (λC ′ . wrlpn JC ′ K (Y1 | ξ) ⋆ ξ) ,
                                                           o
          ξ −−⋆ stepJCK (λC ′ . wrlpn JC ′ K (Y1 | ξ) ⋆ ξ)                                  (Statement (20))
        
   = min wrlpn+1 JCK (Y1 | ξ), wrlpn+1 JCK (Y2 | ξ)                                       (Definition of wrlp)

For † we have:

     stepJCK (λC ′ . min { t(C ′ ), t′ (C ′ ) })
         Xh                                                                           i
                                                                     p
   = inf       p · min { t(C ′ ), t′ (C ′ ) } (s′ , h′ ) | C, (s, h) −
                                                                     → C ′ , (s′ , h′ )
                                                                     a
                                 
           a ∈ Act(C, (s, h))                                                            (Definition of step)
                                                                                                     
                                                                                     1
   = inf min { t(C ′ ), t′ (C ′ ) } (s′ , h′ ) | a ∈ Act(C, (s, h)) ∧ C, (s, h) −   → C ′ , (s′ , h′ )
                                                                                  a
                                                                                 (C is not probabilistic)
                    nXh                                                 i
                                                       p
   = inf       minp · t(C ′ )(s′ , h′ ) | C, (s, h) −  → C ′ , (s′ , h′ ) ,
                                                       a
               Xh                                       p
                                                                          io
                   p · t′ (C ′ )(s′ , h′ ) | C, (s, h) −
                                                       → C ′ , (s′ , h′ )
                                                        a
                            
         a ∈ Act(C, (s, h))                                                  (C is not probabilistic)
             nXh                                                        i                  o
                                                       p
   = min inf      p · t(C ′ )(s′ , h′ ) | C, (s, h) −  → C ′ , (s′ , h′ ) a ∈ Act(C, (s, h)) ,
                                                       a
              nXh                                       p
                                                                          i                  o
          inf       p · t(C ′ )(s′ , h′ ) | C, (s, h) −→ C ′ , (s′ , h′ ) a ∈ Act(C, (s, h))
                                                          a

                                                                                             (Statement (5))
                           ′           ′                                ′             ′
   = min { stepJCK (λC . wrlpn JC K (Y1 | ξ) ⋆ ξ), stepJCK (λC . wrlpn JC K (Y2 | ξ) ⋆ ξ) }
                                                                           (Definition of step)

                                                                                                           ◀
52   Towards Concurrent Quantitative Separation Logic


     ▶ Lemma E.18. If X1 ≤ wrlpJCK (Y1 | ξ), X2 ≤ wrlpJCK (Y2 | ξ), ξ is precise and
     Write(C) ∩ Vars (e) = ∅ then ep · X1 + (1 − ep ) · X2 ≤ wrlpJCK (ep · Y1 + (1 − ep ) · Y2 | ξ).

     Proof. We prove by induction on n that ep · wrlpn JCK (Y1 | ξ) + (1 − ep ) · wrlpn JCK (Y2 | ξ) ≤
     wrlpn JCK (ep · Y1 + (1 − ep ) · Y2 | ξ). If this holds, the claim also holds.
         For the induction base n = 0, we have wrlp0 JCK (ep · Y1 + (1 − ep ) · Y2 | ξ) = 1 = ep +
     (1 − ep ) = ep · wrlp0 JCK (Y1 | ξ) + (1 − ep ) · wrlp0 JCK (Y2 | ξ).
         We now assume that the claim holds for some arbitrary but fixed n as our induction
     hypothesis.
         For the induction step, we have three cases. For the case C = ↓ we have the equality
     wrlpn+1 J ↓ K (ep · Y1 + (1 − ep ) · Y2 | ξ) = ep · Y1 + (1 − ep ) · Y2 = ep · wrlpn+1 J ↓ K (Y1 | ξ) +
     (1 − ep ) · wrlpn+1 J ↓ K (Y2 | ξ). For the case C ̸= ↓ , Act(C, (s, h)) = ∅ we have:

            wrlpn+1 JCK (ep · Y1 + (1 − ep ) · Y2 | ξ) (s, h)
         = (ξ −−⋆ stepJCK (λC ′ . wrlpn JC ′ K (ep · Y1 + (1 − ep ) · Y2 | ξ) ⋆ ξ)) (s, h)
                                                                                         (Definition of wrlp)
         = (ξ −−⋆ 1)(s, h)                                                                     (Act(C, (s, h)) = ∅)
         = 1(s, h)                                                                              (Definition of −−⋆ )
         = (ep + (1 − ep )) (s, h)                                                                         (Algebra)
         = ep · wrlpn+1 J ↓ K (Y1 | ξ) + (1 − ep ) · wrlpn+1 J ↓ K (Y2 | ξ)                      (Similar to above)

     And lastly we have the case that C ̸= ↓ , Act(C, (s, h)) ̸= ∅:

            wrlpn+1 JCK (ep · Y1 + (1 − ep ) · Y2 | ξ)
         = ξ −−⋆ stepJCK (λC ′ . wrlpn JC ′ K (ep · Y1 + (1 − ep ) · Y2 | ξ) ⋆ ξ)              (Definition of wrlp)
         ≥ ξ −−⋆ stepJCK (λC ′ . (ep · wrlpn JCK (Y1 | ξ) + (1 − ep ) · wrlpn JCK (Y2 | ξ)) ⋆ ξ)
                                                                                (Induction Hypothesis)
         = ξ −−⋆ stepJCK (λC ′ . ep · (wrlpn JCK (Y1 | ξ) ⋆ ξ) + (1 − ep ) · (wrlpn JCK (Y2 | ξ) ⋆ ξ))
                                                          (ξ is precise and Statements (26) and (27))
         ≥ ξ −−⋆ ep · stepJCK (λC ′ . wrlpn JCK (Y1 | ξ) ⋆ ξ)
                + (1 − ep ) · stepJCK (λC ′ . wrlpn JCK (Y2 | ξ) ⋆ ξ)
                                                                      

                                                                (Monotoncitiy of −−⋆ and †, see below)
         ≥ ep · (ξ −−⋆ stepJCK (λC ′ . wrlpn JCK (Y1 | ξ) ⋆ ξ))
           + (1 − ep ) · (ξ −−⋆ stepJCK (λC ′ . wrlpn JCK (Y2 | ξ) ⋆ ξ))             (Statements (21) and (22))
         = ep · wrlpn+1 JCK (Y1 | ξ) + (1 − ep ) · wrlpn+1 JCK (Y2 | ξ)                        (Definition of wrlp)

     Lastly for † we have:

           stepJCK (λC ′ . ep · t(C ′ ) + (1 − ep ) · t′ (C ′ ))
               Xh                                                                                             o
                                                                                             p
         = inf         p · (ep · t(C ′ ) + (1 − ep ) · t′ (C ′ ))(s′ , h′ ) | C, (s, h) −   → C ′ , (s′ , h′ )
                                                                                             a
                                         
                 a ∈ Act(C, (s, h))                                                                 (Definition of step)
               X
                      p · (ep (s′ ) · t(C ′ )(s′ , h′ ) + (1 − ep (s′ )) · t′ (C ′ )(s′ , h′ ))
                     
         = inf
                                                                            
                              p
                             → C ′ , (s′ , h′ ) a ∈ Act(C, (s, h))
                                                 
                 C, (s, h) −                                                                    (Pointwise application)
                                a
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                            53

           X
                    p · (ep (s) · t(C ′ )(s′ , h′ ) + (1 − ep (s)) · t′ (C ′ )(s′ , h′ ))
                   
   = inf
                                                                        
                           p       ′   ′   ′
                                               
               C, (s, h) − → C , (s , h ) a ∈ Act(C, (s, h))
                             a
                                                   (Lemmas C.5 and C.7 and Write(C) ∩ Vars (ep ) = ∅)
           X
                    p · ep (s) · t(C ′ )(s′ , h′ ) + p · (1 − ep (s)) · t′ (C ′ )(s′ , h′ )
                   
   = inf
                                                                       
                            p
                           → C ′ , (s′ , h′ ) a ∈ Act(C, (s, h))
                                               
               C, (s, h) −                                                                  (Distributivity)
                             a
           X
                                                                p
                   p · ep (s) · t(C ′ )(s′ , h′ ) C, (s, h) −  → C ′ , (s′ , h′ )
                                                                                 
   = inf
                                                                a
               X
                                            ′    ′   ′    ′              p
                                                                         → C ′ , (s′ , h′ )
                                                                                           
           +         p · (1 − ep (s)) · t (C )(s , h ) C, (s, h) −
                                                                         a
                                    
             a ∈ Act(C, (s, h))                                                                (Commutativitiy)
          X
                                                                p
                   p · ep (s) · t(C ′ )(s′ , h′ ) C, (s, h) −  → C ′ , (s′ , h′ )
                                                                                 
   ≥ inf
                                                                a
                                    
             a ∈ Act(C, (s, h))
             X
                                                                          p
                      p · (1 − ep (s)) · t′ (C ′ )(s′ , h′ ) C, (s, h) −  → C ′ , (s′ , h′ )
                                                                                            
     + inf
                                                                          a
                                    
             a ∈ Act(C, (s, h))                                       (Statement (7) and Act(C, (s, h)) ̸= ∅)
                  X
                                                               p
                           p · t(C ′ )(s′ , h′ ) C, (s, h) −   → C ′ , (s′ , h′ )
                                                                                
   = ep (s) · inf
                                                               a
                                    
             a ∈ Act(C, (s, h))
                             X
                                                                          p
                                       p · t′ (C ′ )(s′ , h′ ) C, (s, h) −→ C ′ , (s′ , h′ )
                                                                                            
     + (1 − ep (s)) · inf
                                                                          a
                                    
             a ∈ Act(C, (s, h))                                   (Constant factors can be shifted outside)

   = ep (s) · stepJCK (λC ′ . t(C ′ )) (s, h) + (1 − ep (s)) · stepJCK (λC ′ . t′ (C ′ )) (s, h)
                                                                                       (Definition of step)
   = (ep · stepJCK (λC ′ . t(C ′ )) + (1 − ep · stepJCK (λC ′ . t′ (C ′ ))) (s, h)
                                                                                 (Pointwise application)
Thus, the claim is proven.                                                                                     ◀

▶ Theorem 4.2 (Soundness of proof rules). For every proof rule in Figures 5–7 it holds that
if their premises hold, the conclusion holds as well.
Proof. We prove the soundness of all inference rules.
                                             term                              Y ≤ X [x := e]
                  X ≤ wrlpJ ↓ K (X | ξ)                                                               assign
                                                                         Y ≤ wrlpJx := eK (X | ξ)
   Y ≤ supv∈Z [e 7→ v] ⋆ ([e 7→ v] −−⋆ X [x := v])                    Y ≤ [e 7→ − ] ⋆ ( e 7→ e′ −−⋆ X)
                                                                                              
                                                   look
          Y ≤ wrlpJx := < e >K (X | ξ)                                                                   mut
                                                                       Y ≤ wrlpJ< e > := e′ K (X | ξ)
     Y ≤ inf v∈Z [v 7→ e1 , . . . , en ] −−⋆ X [x := v]
                                                        alloc              Y ≤ X ⋆ [x 7→ − ]
      Y ≤ wrlpJx := new (e1 , . . . , en )K (X | ξ)                                               disp
                                                                        Y ≤ wrlpJfree(x)K (X | ξ)
54   Towards Concurrent Quantitative Separation Logic


     The proof rules term, look, alloc, assign, mut and disp are sound by Lemma E.3 and the
     proof rules for wlp from [5].

                           X ≤ wrlpJC1 K (Y | ξ)  Y ≤ wrlpJC2 K (Z | ξ)
                                                                        seq
                                    X ≤ wrlpJC1 ; C2 K (Z | ξ)
     The proof rule seq is sound by Lemma E.4.

                           X1 ≤ wrlpJC1 K (Y | ξ)      X2 ≤ wrlpJC2 K (Y | ξ)
                                                                                      if
                     [b] · X1 + [¬b] · X2 ≤ wrlpJif ( b ) { C1 } else { C2 }K (Y | ξ)
     The proof rule if is sound by Lemma E.5.

                           I ≤ [b] · X + [¬b] · Y  X ≤ wrlpJCK (I | ξ)
                                                                       while
                                 I ≤ wrlpJwhile ( b ) { C }K (Y | ξ)
     The proof rule while is sound by Lemma E.6.

                                                                               div
                                         X ≤ wrlpJdivergeK (Y | ξ)
     The proof rule div is sound by Lemma C.9.

                      X1 ≤ wrlpJC1 K (Y | ξ)      X2 ≤ wrlpJC2 K (Y | ξ)
                                                                                 p-choice
                   ep · X1 + (1 − ep ) · X2 ≤ wrlpJ{ C1 } [ ep ] { C2 }K (Y | ξ)
     The proof rule p-choice is sound by Lemma E.7.

                                      X ≤ wrlpJCK (Y ⋆ ξ | [emp])
                                                                    atomic
                                     X ≤ wrlpJatomic { C }K (Y | ξ)
     The proof rule atomic is sound by Lemma E.8.

                                         X ≤ wrlpJCK (Y | ξ ⋆ π)
                                                                    share
                                        X ⋆ π ≤ wrlpJCK (Y ⋆ π | ξ)
     The proof rule share is sound by Lemma E.9.
           X1 ≤ wrlpJC1 K (Y1 | ξ)      X2 ≤ wrlpJC2 K (Y2 | ξ)     Write(Ci ) ∩ Vars (C3−i , Y3−i , ξ) = ∅
                                                                                                            concur
                                       X1 ⋆ X2 ≤ wrlpJ C1 ∥ C2 K (Y1 ⋆ Y2 | ξ)

     The proof rule concur is sound by Lemma E.10.
                  X ′ ≤ wlpS JCK (X)       Y ′ ≤ wlpS JCK (Y )    C is AST wrt S        a ∈ R≥0
                                             ′     ′      S
                                                                                                  superlin
                                        a · X + Y ≤ wlp JCK (a · X + Y )

     The proof rule superlin is sound by Lemma E.12.

                                       X ≤ wrlpJCK (Y | [emp])
                                                                          wlp-wrlp
                                             X ≤ wlpS JCK (Y )
     The proof rule wlp-wrlp is sound by Lemma E.13.

                        X ≤ wrlpJCK (Y | ξ)  Write(C) ∩ Vars (Z) = ∅
                                                                     frame
                                X ⋆ Z ≤ wrlpJCK (Y ⋆ Z | ξ)
     The proof rule frame is sound by Lemma E.14.
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                            55


               X ⋆ ξ ≤ wrlpJCK (Y ⋆ ξ | [emp]) C is a terminating atom
                                                                       atom
                                 X ≤ wrlpJCK (Y | ξ)

The proof rule atom is sound by Lemma E.15.

                    X ≤ X′          X ′ ≤ wrlpJCK Y ′ | ξ                   Y′ ≤Y
                                                                  
                                                                                      monotonic
                                     X ≤ wrlpJCK (Y | ξ)

The proof rule monotonic is sound by Lemma E.1.

                                           X ′ ≤ wrlpJCK Y ′ | ξ
                                                                                      
                       X ≤ wrlpJCK (Y | ξ)
                                                                                          max
                        max X, X ′ ≤ wrlpJCK max Q, Q′ | ξ
                                                            

The proof rule max is sound by Lemma E.16.

                                               X ′ ≤ wrlpJCK Y ′ | ξ
                                                                     
               X ≤ wrlpJCK (Y | ξ)                                          ξ precise
                                                                                      min
                     min X, X ′                                    ′
                                                                        
                                              ≤ wrlpJCK min Y, Y       |ξ

The proof rule min is sound by Lemma E.17.

                                  X ′ ≤ wrlpJCK Y ′ | ξ
                                                          
         X ≤ wrlpJCK (Y | ξ)                                    ξ precise     Write(C) ∩ Vars (e) = ∅
                                                                                                      convex
                          e · X + (1 − e) · X ′ ≤ wrlpJCK e · Y + (1 − E) · Y ′ | ξ
                                                                                  


The proof rule convex is sound by Lemma E.18.                                                                  ◀


 F       Details on Examples

F.1      Additional Details on the Running Example
To recap, we are given the resource invariant ξ = max { [r 7→ 0], [r 7→ −1] } and have already
proven:

     ( 0.5 ⋆ 1 | ξ
                                                   ( 1 | ξ
                                                   ( 1⋆ξ
      ( 0.5 | ξ                                    y := < r > ;
      { < r > := 0 } [ 0.5 ] { < r > := 1 }        ( max { [y = 0], [y = −1] } ⋆ ξ
      ( 1 | ξ                                      ( max { [y = 0], [y = −1] } | ξ
                                                   while ( y = −1 ) { y := < r > } ;
                                                   ( [y = 0] | ξ
     ( 1 ⋆ [y = 0] | ξ


The mutation < r > := −1 together with the atom rule gives us the inequality

     0.5 ⋆ [r 7→ − ] ≤ [r 7→ − ] ⋆ ([r 7→ −1] −−⋆ 0.5 ⋆ max { [r 7→ 0], [r 7→ −1] }) .

However, it is easy to verify that ([r 7→ −1] −−⋆ 0.5 ⋆ max { [r 7→ 0], [r 7→ −1] }) simplifies to
0.5, which results in the given lower bound.
56   Towards Concurrent Quantitative Separation Logic


        For the probabilistic choice we have:

         ( 0.5 | ξ
         ( 0.5 · 1 + 0.5 · 0 | ξ
                                         
          ( 1 | ξ
                               ( 0 | ξ
                                           
           < r > := 0    [ 0.5 ] < r > := 1
                                         
           ( 1 | ξ                ( 1 | ξ
                                         

         ( 1 | ξ

     The right part is rather simple, as we can always lower bound anything by zero. The left
     part holds since with [r 7→ 0] the mutation is satisfied, however the value before mutat-
     ing r is unknown. We can lower bound the resulting preexpectation 1 ⋆ [r 7→ − ] by 1 ⋆
     max { [r 7→ −1], [r 7→ 0] } and thus realise the resource invariant again. For the loop invari-
     ant max { [y = 0], [y = −1] } we have:

         ( max { [y = 0], [y = −1] } | ξ
        y := < r >
         ( max { [y = 0], [y = −1] } | ξ

     The lookup operation here results in both [y = 0] and [y = 1] to be evaluated to 1 if [r 7→ 0]
     and [r 7→ −1], respectively. Our resource invariant guarantees this, thus we obtain the
     expectation 1 and lower bound it by max { [y = 0], [y = −1] }. Lastly we check that it is
     indeed a loop invariant:

            [y = −1] · max { [y = 0], [y = −1] } + [y ̸= −1] · [y = 0]
        = [y = −1] + [y = 0]
        = max { [y = 0], [y = −1] }

     F.2      Example: A Producer, a Consumer and a lossy Channel
     Here we have the following program C:

       l := 0 ;
       y1 , y2 , y3 := k ;

                                                while ( y2 ≥ 0 ) {
                                                    x2 := < z1 + y2 > ;           while ( y3 ≥ 0 ) {
        while ( y1 ≥ 0 ) {                          if ( x2 ̸= 0 ) {                  x3 := < z2 + y2 > ;
            { x1 := 1 } [ 0.5 ] { x1 := 2 } ;             {< z2 + y2 > := x2 }        if ( x3 ̸= 0 ) {
            < z1 + y1 > := x1 ;                         [p]                               if ( x3 ̸= −1 ) {l := l + 1} ;
            y1 := y1 − 1                                  {< z2 + y2 > := −1} ;           y3 := y3 − 1
        }                                               y2 := y2 − 1                  }
                                                    }                             }
                                                }

     We use the resource invariant ξJ for a set J. The set J encodes which locations in the array
     starting from z2 will have an error value of −1 or a valid value of 1 or 2 after the channel
     inserts data into it. We use a big separating multiplication to connect all the possible
     instantiations using separating multiplication. That is, ⋆{X} = X and ⋆({X} ∪ A) =
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                            57


X ⋆ ⋆A for a non-empty and countable set A. ξJ declares that all locations between z1 and
z1 + k have either value 0, 1 or 2 and all locations between z2 and z2 + k have values 0, 1
or 2 if the offset is in J and 0 or −1 if the offset is not in J. The value 0 is always possible
for all locations between zi and zi + k since we assume 0 to be the initial value. We connect
the predicates declaring possible values for the location zj + i using a maximum, which acts
as a qualitative disjunction here.
                                                                            !
   ξJ      =           ⋆         max { [z1 + i 7→ 0] , [z1 + i 7→ 1] , [z1 + i 7→ 2] }
                   i∈{0,...,k}
                                                                                         !
               ⋆        ⋆          max { [z2 + i 7→ 0] , [z2 + i 7→ 1] , [z2 + i 7→ 2] }
                   i∈{0,...,k}∩J
                                                                            !
               ⋆        ⋆          max { [z2 + i 7→ 0] , [z2 + i 7→ −1] }       .
                   i∈{0,...,k}\J

We will leave out computations of inequalities X ≤ Y for the sake of brevity and give an
explanation instead. Since our representation of expectations may grow in size, we use a
curly bracket after the ( symbol to denote expectations which are too long for one line. Our
goal is to prove a lower bound on the probability that l = |J| is realised after termination.
If J contains numbers outside the range between 0 and k, we may as well replace |J| with
|J ∩ {0, . . . , k}|. We now prove an invariant for each of the three subprograms.
    For the producer C1 , we prove the invariant I1 = 1 with respect to the postexpectation
1 and resource invariant ξJ . This shows indeed that the probability of safe execution of the
loop is one and that our resource invariant ξJ almost always holds.
    ( 1 | ξJ
                                                                         
    
     ( 1 | ξJ                     
                                            
                                              ( 1 | ξJ                     
                                                                            
                                                                         
     ( [1 ∈ {0, . . . , 2}] | ξ 
                                            ( [2 ∈ {0, . . . , 2}] | ξ 
                                                                           
                                J                                        J
                                     [ 0.5 ]                                  ;
     x1 := 1
    
    
                                   
                                   
                                   
                                             
                                             
                                              x1 := 2                      
                                                                            
                                                                            
                                                                         
      ( [x1 ∈ {0, . . . , 2}] | ξJ             ( [x1 ∈ {0, . . . , 2}] | ξJ
                                                                         

    ( [x1 ∈ {0, . . . , 2}] | ξJ
   < z1 + y1 > := x1 ;
    ( 1 | ξJ
   y1 := y1 − 1
    ( 1 | ξJ
The inequality
   [x1 ∈ {0, . . . , 2}] ⋆ ξJ ≤ [z1 + y1 7→ − ] ⋆ ([z1 + y1 7→ x1 ] −−⋆ (1 ⋆ ξJ ))
resulting from the mutation < z1 + y2 > := x1 together with the atom rule holds because
for [z1 + y1 7→ x1 ] −−⋆ (1 ⋆ ξJ ) to be non-zero, x1 must coincide with ξJ – thus x1 has to
be either 0, 1 or 2. Furthermore, we have that [z1 + y1 7→ i] ≤ [z1 + y1 7→ − ] holds for
every i, and obtain by this that i ∈ {0, . . . , 2}, with which we re-establish ξJ . We have
[y1 ≥ 0] · 1 + [y1 < 0] · 1 = 1 and therefore 1 is a loop invariant.
    For the channel C2 , we use the shorthand notation P (y) to denote cumulated probability
mass and define it as
   P (y)       =    p|{0,...,y}∩J| · (1 − p)|{0,...,y}\J| .
58   Towards Concurrent Quantitative Separation Logic


     This shorthand notation gives us the probability that all data with offset 0 up to y are
     transferred according to J. That is, if an element should have been transferred successfully,
     we multiply with p and if not with 1 − p for every location up to y2 . We prove for the
     invariant I2 = [0 ≤ y2 ≤ k] · P (y2 ) + [y2 < 0] with respect to the postexpectation 1 and
     resource invariant ξJ :

         ( [0 ≤ y2 ≤ k] · P (y2 ) + [y2 < 0] | ξJ
           (
         (
              [x2 ̸= 0] · [0 ≤ y2 ≤ k] · P (y2 )
              + [x2 = 0] · ([0 ≤ y2 ≤ k] · P (y2 ) + [y2 < 0])      |   ξJ

        x2 := < z1 + y2 > ;



                                                                                              |
            
             [x2 ̸= 0] · [0 ≤ y2 ≤ k] · P (y2 − 1) · (p · [y2 ∈ J] · [x2 ∈ {1, . . . , 2}]
            
        (           + (1 − p) · [y2 ̸∈ J])                                                        ξJ
            
               + [x2 = 0] · ([0 ≤ y2 ≤ k] · P (y2 ) + [y2 < 0])
            

        if ( x2 ̸= 0 ) {
            ( [0 ≤ y2 ≤ k] · P (y2 − 1) · (p · [y2 ∈ J] · [x2 ∈ {0, . . . , 2}] + (1 − p) · [y2 ̸∈ J]) | ξJ
              {
              ( ([0 ≤ y2 ≤ k] · P (y2 − 1)) · [y2 ∈ J] · [x2 ∈ {0, . . . , 2}] | ξJ
              ( ([1 ≤ y2 ≤ k] · P (y2 − 1) + [y2 = 0]) · [y2 ∈ J] · [x2 ∈ {0, . . . , 2}] | ξJ
              < z2 + y2 > := x2
              ( [1 ≤ y2 ≤ k + 1] · P (y2 − 1) + [y2 < 1] | ξJ
              }
            [p]
              {
              ( ([0 ≤ y2 ≤ k] · P (y2 − 1)) · [y2 ̸∈ J] | ξJ
              ( ([1 ≤ y2 ≤ k] · P (y2 − 1) + [y2 = 0]) · [y2 ̸∈ J] | ξJ
              < z2 + y2 > := −1 ;
              ( [1 ≤ y2 ≤ k + 1] · P (y2 − 1) + [y2 < 1] | ξJ
              }
            ( [1 ≤ y2 ≤ k + 1] · P (y2 − 1) + [y2 < 1] | ξJ
            ( [0 ≤ y2 − 1 ≤ k] · P (y2 − 1) + [y2 − 1 < 0] | ξJ
            y2 := y2 − 1
            ( [0 ≤ y2 ≤ k] · P (y2 ) + [y2 < 0] | ξJ
        }
         ( [0 ≤ y2 ≤ k] · P (y2 ) + [y2 < 0] | ξJ

     We explain some of the difficult inequalities in the previous proof. We start with the in-
     equality

            (([1 ≤ y2 ≤ k] · P (y2 − 1) + [y2 = 0]) · [y2 ̸∈ J]) ⋆ ξJ
        ≤ [z2 + y2 7→ − ] ⋆ ([z2 + y2 7→ −1] −−⋆ ([1 ≤ y2 ≤ k + 1] · P (y2 − 1) + [y2 < 1]) ⋆ ξJ

     resulting from the mutation < z2 + y2 > := −1 together with the atom rule. This inequality
     holds since for the part [z2 + y2 7→ −1] −−⋆ . . . to be non-zero, we require y2 ̸∈ J due to ξJ .
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                     59


We lower bound all evaluations where y2 < 0 by 0 as we can not infer any information about
these locations from ξJ . Afterwards, we can lower bound [z2 + y2 7→ − ] by [z2 + y2 7→ i] for
every i and thus re-establish ξJ .
   Next we have the inequality

       (([1 ≤ y2 ≤ k] · P (y2 − 1) + [y2 = 0]) · [y2 ∈ J] · [x2 ∈ {0, . . . , 2}]) ⋆ ξJ
   ≤ [z2 + y2 7→ − ] ⋆ ([z2 + y2 7→ x2 ] −−⋆ ([1 ≤ y2 ≤ k + 1] · P (y2 − 1) + [y2 < 1]) ⋆ ξJ

resulting from the mutation < z2 + y2 > := x2 together with the atom rule. Here we assume
that the location y2 is in J and obtain that x2 ∈ {0, . . . , 2}. We lower bound any outcome
of y2 not in J by 0 because we already know that we will eventually set the term to 0 due
to the previous lookup. Next we establish ξJ back from lower bounding [z2 + y2 7→ − ].
    We have the inequality

       [x2 ̸= 0] · [0 ≤ y2 ≤ k] · P (y2 ) + [x2 = 0] · ([0 ≤ y2 ≤ k] · P (y2 ) + [y2 < 0]) ⋆ ξ
   ≤ sup [z1 + y2 7→ v] ⋆ ([z1 + y2 7→ v] −−⋆
      v∈Z

      ([v ̸= 0] · [0 ≤ y2 ≤ k] · P (y2 − 1) · (p · [y2 ∈ J] · [v ∈ {1, . . . , 2}] + (1 − p) · [y2 ̸∈ J])
       + [v = 0] · ([0 ≤ y2 ≤ k] · P (y2 ) + [y2 < 0])) ⋆ ξ)

resulting from the lookup x2 := < z1 + y2 > together with the atom rule. We will consider
both cases separately. Let us assume that v is not 0. Then either y2 is in J and v is either
1 or 2 to make p · [y2 ∈ J] · [v ∈ {1, . . . , 2}] not zero, or y2 is not in J. Then, however, v
needs to be −1, because else ξJ will evaluate to zero. Both cases can then be used to turn
P (y2 −1) into P (y2 ). In both cases, we can also use [z1 + y2 7→ v] to re-establish the resource
invariant ξJ . If, on the other side, v is 0, we do not get any new information, but also do
not need to update P (y2 ), and directly re-establish the resource invariant ξJ .
    Due to

       [y2 ≥ 0] · ([0 ≤ y2 ≤ k] · P (y2 ) + [y2 < 0]) + [y2 < 0] · 1
   = [0 ≤ y2 ≤ k] · P (y2 ) + [y2 < 0]

we establish the loop invariant with respect to postexpectation 1.
    For the consumer C3 we require a loop invariant that checks if l indeed matches the size
of the set J. We prove the loop invariant I3 = [0 ≤ y3 ≤ k] · [y3 + l = |J ∩ {0, . . . , y3 }|] with
respect to the postexpectation [l = |J|] and the resource invariant ξJ :

    ( [0 ≤ y3 ≤ k] · [l = |J ∩ {y3 + 1, . . . , k}|] | ξJ
   x3 := < z2 + y3 > ;




                                                                                             |
       
       
           [x3 = −1] · [1 ≤ y3 ≤ k + 1] · [l = |J ∩ {y3 , . . . , k}|]
       
          + [x3 = −1] · [y3 < 1] · [l = |J|]
       
       
       
       
       
        + [x ̸= 0] · [x ̸= −1] · [1 ≤ y ≤ k + 1] · [l + 1 = |J ∩ {y , . . . , k}|])
       
               3            3                  3                           3
   (                                                                                             ξJ
       
       
         + [x 3 ̸
                 = 0]  · [x 3 ̸
                              =   −1] · [y3  < 1] · [l + 1 = |J|]
       
          + [x   = 0]  · [0  ≤  y  ≤  k] · [l = |J ∩ {y3 + 1, . . . , k}|]
       
               3                 3
       
       
       
       
          + [x3 = 0] · [y3 < 0] · [l = |J|]
       

   if ( x3 ̸= 0 ) {
60   Towards Concurrent Quantitative Separation Logic




                                                                                            |
                   
                   
                      [x3 = −1] · [1 ≤ y3 ≤ k + 1] · [l = |J ∩ {y3 , . . . , k}|]
                   
                    + [x = −1] · [y < 1] · [l = |J|]
                   
                          3            3
            (                                                                                   ξJ
                   
                   
                    + [x3 ̸= −1] · [1 ≤ y3 ≤ k + 1] · [l + 1 = |J ∩ {y3 , . . . , k}|]
                   
                     + [x3 ̸= −1] · [y3 < 1] · [l + 1 = |J|]
                   

            if ( x3 ̸= −1 ) {
                 ( [1 ≤ y3 ≤ k + 1] · [l + 1 = |J ∩ {y3 , . . . , k}|] + [y3 < 1] · [l + 1 = |J|] | ξJ
                 l := l + 1
                 ( [1 ≤ y3 ≤ k + 1] · [l = |J ∩ {y3 , . . . , k}|] + [y3 < 1] · [l = |J|] | ξJ
            };
            ( [1 ≤ y3 ≤ k + 1] · [l = |J ∩ {y3 , . . . , k}|] + [y3 < 1] · [l = |J|] | ξJ
            ( [0 ≤ y3 − 1 ≤ k] · [l = |J ∩ {y3 , . . . , k}|] + [y3 − 1 < 0] · [l = |J|] | ξJ
            y3 := y3 − 1
            ( [0 ≤ y3 ≤ k] · [l = |J ∩ {y3 + 1, . . . , k}|] + [y3 < 0] · [l = |J|] | ξJ
        }
         ( [0 ≤ y3 ≤ k] · [l = |J ∩ {y3 + 1, . . . , k}|] + [y3 < 0] · [l = |J|] | ξJ

     Here we will take a closer look at the inequality

            ([1 ≤ y3 ≤ k] · [l = |J ∩ {y3 + 1, . . . , k}|] + [y3 = 0] · [l = |J ∩ {1, . . . , k}|]) ⋆ ξJ
        ≤ sup [z2 + y2 7→ v] ⋆ ([z2 + y2 7→ v] −−⋆
            v∈Z

              ([v = −1] · [1 ≤ y3 ≤ k + 1] · [l = |J ∩ {y3 , . . . , k}|]
            + [v = −1] · [y3 < 1] · [l = |J|]
            + [v ̸= 0] · [v ̸= −1] · [1 ≤ y3 ≤ k + 1] · [l + 1 = |J ∩ {y3 , . . . , k}|])
            + [v ̸= 0] · [v ̸= −1] · [y3 < 1] · [l + 1 = |J|]
            + [v = 0] · [0 ≤ y3 ≤ k] · [l = |J ∩ {y3 + 1, . . . , k}|]
            + [v = 0] · [y3 < 0] · [l = |J|]) ⋆ ξJ )

     due to the lookup x3 := < z2 + y2 > together with the atom rule. We consider all cases
     separately.
        First, let v be −1
           If moreover y3 is between 1 and k + 1, then we can directly lower bound the case
           that y3 is k + 1 by zero as ξJ does not have carry information for this location.
           Because v is −1, we know that y3 is not in J due to ξJ . Thus, we also have that
           |J ∩ {y3 + 1, . . . , k}| = |J ∩ {y3 , . . . , k}|.
           If y3 is below 1, the same reasoning holds, with the difference that we lower bound
           the expectation for every value of y3 below 0 as zero and consider only the case where
           y3 is 0.
        In the case that v is neither 0 nor −1, we first observe that only 1 and 2 are valid values,
        because ξJ does not allow any other value for y3 between 0 and k.
        In the cases where v is either k + 1 or below 0, we just lower bound the formula by zero.
        However, for the latter cases we have |J ∩ {y3 + 1, . . . , k}| + 1 = |J ∩ {y3 , . . . , k}|.
        Lastly, in the case that v is 0, the expression already matches the target lower bound,
        but again, we lower bound the formula by zero if y3 has a value below 0.
I. Fesefeldt, J.-P. Katoen, and T. Noll                                                                        61


   Moreover, we have



      [y3 ≥ 0] · ([0 ≤ y3 ≤ k] · [l = |J ∩ {y3 + 1, . . . , k}|] + [y3 < 0] · [l = |J|])
   = [0 ≤ y3 ≤ k] · [l = |J ∩ {y3 + 1, . . . , k|}] + [y3 < 0] · [l = |J|]



and thus established a loop invariant with respect to postexpectation [l = |J|].

   Now we can combine all three results



    ( P (k) · [0 ≤ k] | ξJ
    ( [0 ≤ k] · P (k) + [k < 0] · [0 = |J|] | ξJ
   l := 0 ;
    ( [0 ≤ k] · [l = 0] · P (k) + [k < 0] · [l = |J|] | ξJ



                                                                               |
      
       1
      
    (   ⋆ ([0 ≤ k] · P (k) + [k < 0])                                              ξJ
      
        ⋆ ([0 ≤ k] · [l = |J ∩ {k + 1, . . . , k}|] + [k < 0] · [l = |J|])
      

   y1 , y2 , y3 := k ;



                                                                                         |
         
          1
         
   (         ⋆ ([0 ≤ y2 ≤ k] · P (y2 ) + [y2 < 0])                                           ξJ
         
             ⋆ ([0 ≤ y3 ≤ k] · [l = |J ∩ {y3 + 1, . . . , k}|] + [y3 < 0] · [l = |J|])
         

    C1 ∥ C2 ∥ C3
    ( 1 ⋆ 1 ⋆ [l = |J|] | ξJ




and we have for the whole program C and a set of schedulers S ⊆ S:



              (P (k) · [0 ≤ k]) ≤ wrlpJCK ([l = |J|] | ξJ )
   implies (P (k) · [0 ≤ k]) ⋆ ξJ ≤ wrlpJCK ([l = |J|] ⋆ ξJ | [emp])                                (share)
                                           S
   implies (P (k) · [0 ≤ k]) ⋆ ξJ ≤ wlp JCK ([l = |J|] ⋆ ξJ )                                     (wlp-wrlp)



We can use this to prove the lower bound of probabilities for even more elaborated post-
conditions if we have a set of schedulers S ⊆ S such that C is almost surely terminating
with respect to S. One of these is the probability that at least half of the messages are
sent successfully, i.e., the probability of the postexpectation k + 1 ≥ l ≥ k+1
                                                                             2  – or equival-
      P
ently k+1 ≤j≤k+1 [l = j]. For this, we use the resource invariant ξj = maxJ⊆{0,...,k},|J|=j ξJ
          2
where ξJ is defined as previous. Although we call ξj a resource invariant, we never prove
that it is a resource invariant. We only prove that ξJ is a resource invariant. We can now
62   Towards Concurrent Quantitative Separation Logic


     compute:

                wlpS JCK ([l = |J|] ⋆ ξJ ) ≥ (P (k) · [0 ≤ k]) ⋆ ξJ
                                                         
                   S
        implies wlp JCK         max         [l = |J|] ⋆ ξJ ≥        max               (P (k) · [0 ≤ k]) ⋆ ξJ
                              J⊆{0,...,k},|J|=j                   J⊆{0,...,k},|J|=j
                                                                                                          (max)
                    S                             j       k−j+1
        implies wlp JCK ([l = j] ⋆ ξj ) ≥ (p · (1 − p)            · [0 ≤ k]) ⋆ ξj             (Definition of ξj )
                                                    
                              X                                 X
        implies wlpS JCK               [l = j] ⋆ ξj  ≥                  (pj · (1 − p)k−j+1 · [0 ≤ k]) ⋆ ξj
                              k+1                             k+1
                               2 ≤j≤k+1                        2 ≤j≤k+1

                                                                                               (Superlinearity)
                                                       
                                              k+1
        implies wlpS JCK       k+1≥l ≥            ⋆ ξj
                                               2
                                                                    
                                X
                        ≥               pj · (1 − p)k−j+1 · [0 ≤ k] ⋆ ξj
                             k+1
                              2 ≤j≤k+1

                                                          (ξj is precise and k + 1 ≥ l ≥ k+1
                                                                                            
                                                                                          2    as above)

     We could drop the resource invariant ξj inside wlpS due to monotonicity of wlpS , for which
     we do not provide a proof. However, this shows that we can use superlinearity to partition
     a big problem in smaller problems and afterwards reason about these smaller problems with
     the help of easier resource invariants, as it is standard in probability theory.
