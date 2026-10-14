                                                       Foundations for Entailment Checking
                                                         in Quantitative Separation Logic
arXiv:2201.11464v1 [cs.LO] 27 Jan 2022


                                                               (extended version)⋆

                                                 Kevin Batz1 , Ira Fesefeldt1 , Marvin Jansen1 , Joost-Pieter Katoen1 ,
                                                      Florian Keßler1 , Christoph Matheja2,3 , and Thomas Noll1
                                             1
                                                 Software Modeling and Verification Group, RWTH Aachen University, Germany
                                                          {kevin.batz,fesefeldt,katoen,noll}@cs.rwth-aachen.de
                                                        2
                                                           Programming Methodology Group, ETH Zürich, Switzerland
                                                               3
                                                                 Technical University of Denmark, chmat@dtu.dk



                                                    Abstract. Quantitative separation logic (QSL) is an extension of sep-
                                                    aration logic (SL) for the verification of probabilistic pointer programs.
                                                    In QSL, formulae evaluate to real numbers instead of truth values, e.g.,
                                                    the probability of memory-safe termination in a given symbolic heap. As
                                                    with SL, one of the key problems when reasoning with QSL is entailment:
                                                    does a formula f entail another formula g?
                                                    We give a generic reduction from entailment checking in QSL to entail-
                                                    ment checking in SL. This allows to leverage the large body of SL research
                                                    for the automated verification of probabilistic pointer programs. We an-
                                                    alyze the complexity of our approach and demonstrate its applicability.
                                                    In particular, we obtain the first decidability results for the verification
                                                    of such programs by applying our reduction to a quantitative extension
                                                    of the well-known symbolic-heap fragment of separation logic.


                                         1        Introduction

                                         Separation logic [28] (SL) is a popular formalism for Hoare-style verification of
                                         imperative, heap-manipulating and, possibly, concurrent programs. Its assertion
                                         language extends first-order logic with two connectives—the separating conjunc-
                                         tion ⋆ and the magic wand −−⋆ —that enable concise specifications of how pro-
                                         gram memory, or other resources, can be split-up and combined. SL builds upon
                                         these connectives to champion local reasoning about the resources employed
                                         by programs. Consequently, program parts can be verified by considering only
                                         those resources they actually access—a crucial property for building scalable
                                         tools including automated verifiers [45,11,15,43,30], static analyzers [9,23,13],
                                         and interactive theorem provers [31]. At the foundation of almost any automated
                                         approach based on SL, lies the entailment problem ϕ |= ψ: are all models of SL
                                         formula ϕ also models of SL formula ψ? For example, Hoare-style verifiers need
                                         to solve entailments whenever they invoke the rule of consequence, and static
                                         ⋆
                                             This work is partially supported by the ERC AdG project 787914 FRAPPANT.
2         Batz et al.

analyzers ultimately solve entailments to perform abstraction. While undecid-
able in general [1], the wide adoption of SL and the central role of the entailment
problem have triggered a massive research effort to identify SL fragments with
a decidable entailment problem [10,16,20,21,26,27,34,39,46,17,19], and to build
practical entailment solvers [45,11,15,49].
    Probabilistic programs, that is, programs with the ability to sample from prob-
ability distributions, are an increasingly popular formalism for, amongst others,
designing efficient randomized algorithms [41] and describing uncertainty in sys-
tems [22,14]. While formal reasoning techniques for probabilistic programs exist
since the 80s (cf., [36,37,48]), they are rarely automated and typically target only
simplistic programming languages. For example, verification techniques that sup-
port reasoning about both randomization and data structures are, with notable
exceptions [50,8], rare—a surprising situation given that randomized algorithms
typically rely on dynamic data structures.
    Quantitative separation logic (QSL) is a weakest-precondition-style verifica-
tion technique that targets randomized algorithms manipulating complex data
structures; it marries SL and weakest preexpectations [42]—a well-established
calculus for reasoning about probabilistic programs. In contrast to classical
SL, QSL’s assertion language does not consist of predicates, which evaluate to
Boolean values, but expectations (or: random variables), which evaluate to real
numbers. QSL has been successfully applied to the verification of randomized
algorithms, and QSL expectations have been formalized in Isabelle/HOL [25].
However, reasoning is far from automated—mainly due to the lack of decision
procedures or solvers for entailments between expectations in QSL.
    This paper presents, to the best of our knowledge, the first technique for
automatically deciding QSL entailments. More precisely, we reduce QSL quanti-
tative entailments to classical entailments between SL formulas. Hence, we can
leverage two decades of separation logic research to advance QSL entailment
checking, and thus also automated reasoning about probabilistic programs.

Contributions. We make the following technical contributions:
    – We present a generic construction that reduces the entailment problem for
      quantitative separation logic to solving multiple entailments in fragments
      of SL; if we reduce to an SL fragment where entailment is decidable, our
      construction yields a QSL fragment with a decidable entailment problem.
    – We provide simple criteria for whether one can leverage a decision procedure
      or a practical entailment solver for SL to build an entailment solver for QSL.
    – We analyze the complexity of our approach parameterized in the complexity
      of solving entailments in a given SL fragment; whenever we identify a decid-
      able QSL fragment, it is thus accompanied by upper complexity bounds.
    – We use our construction to derive the QSL fragment of quantitative symbolic
      heaps for which entailment is decidable via a reduction to the Bernays-
      Schönfinkel-Ramsey fragment of SL [19].

Outline. Section 2 introduces (quantitative) separation logic. Section 3 motivates
our approach by providing the foundations for probabilistic pointer program
      Foundations for Entailment Checking in Quantitative Separation Logic        3

verification with QSL together with several examples. We present the key ideas
and our main contribution of reducing QSL entailment checking to SL entailment
checking in Section 4. We analyse the complexity of our approach in Section 5.
In Section 6, we apply our approach to obtain the first decidability results for
probabilistic pointer verification. Finally, Section 7 discusses related work and
Section 8 concludes.

                  Table 1. Metavariables used throughout this paper.

         Entities                       Metavariables          Domain
         Natural numbers                n, i, j, k             N
         Rational probabilities         p, q, α, β, γ, δ       P


         Programs                       C                      hpGCL
         Stacks                         s                      Stacks
         Heaps                          h                      Heapsk


         Variables                      x, y, z                Vars
         Values                         v, w                   Vals
         Locations                      ℓ                      Locs


         Predicates                     Φ                      P (States)
         one-bounded expectations       X                      E≤1


         SL formulae                    ϕ, ψ, ϑ                SL [·]
         Pure formulae                  π
         QSL formulae                   f, g, u, I             QSL [·]




2     (Quantitative) Separation Logic

2.1   Program States

Let Vals be a countably infinite set of values, and let Vars be a countably infinite
set of variables with domain Vals. The set of stacks is given by

                          Stacks = { s | s : Vars → Vals } .

Let Locs ⊂ Vals be an infinite set of locations. We denote locations by ℓ and
variations thereof. We fix a natural number k ≥ 1 and a heap model where finite
sets of locations are mapped to fixed-size records over Vals of size k. Put more
4        Batz et al.

                        Table 2. Semantics of SL [A] formulae.

           ϕ            (s, h) |= ϕ iff
           ϑ            (s, h) ∈ JϑK
           ¬ψ           (s, h) 6|= ψ
           ψ∧ϑ          (s, h) |= ψ and (s, h) |= ϑ
           ψ∨ϑ          (s, h) |= ψ or (s, h) |= ϑ
           ∃x : ψ       (s [x:=v] , h) |= ψ for some v ∈ Vals
           ∀x : ψ       (s [x:=v] , h) |= ψ for all v ∈ Vals
           ψ⋆ϑ          (s, h1 ) |= ψ and (s, h2 ) |= ϑ for some h1 ⋆ h2 = h
           ψ −−⋆ ϑ      (s, h ⋆ h′ ) |= ϑ for all h′ ⊥ h with (s, h′ ) |= ψ



formally, the set of heaps is given by
                          n                                    o
             Heapsk =       h h : L → Valsk , L ⊆ Locs, |L| < ∞ .

The set of program states is then given by

                    States = { (s, h) | s ∈ Stacks, h ∈ Heapsk } .

Given a program state (s, h) and an expression t over Vars, we denote by t(s)
the evaluation of expression t in s, i.e., the value that is obtained by evaluating
t after replacing any occurrence of any variable x ∈ Vars in t by the value s(x).
We write s [x:=v] to indicate that we set variable x to value v ∈ Vals in s, i.e.4 ,
                                           (
                                             v,     if y = x
                       s [x:=v] = λ y .
                                             s(y), if y 6= x.

For heap h, h [ℓ:=(v1 , . . . , vk )] is defined analogously. For a given heap h : L →
Valsk , we denote by dom (h) its domain L. Two heaps h1 , h2 are disjoint, denoted
h1 ⊥ h2 , if their domains do not overlap, i.e., dom (h1 ) ∩ dom (h2 ) = ∅. The
disjoint union of two disjoint heaps h1 : L1 → Valsk and h2 : L2 → Valsk is
                                                               (
                                            k
                                                                h1 (ℓ), if ℓ ∈ dom (h1 )
h1 ⋆ h2 : dom (h1 ) ∪˙ dom (h2 ) → Vals , h1 ⋆ h2 (ℓ) =
                                                                 h2 (ℓ), if ℓ ∈ dom (h2 ) .

2.2    Separation Logic
A predicate Φ ∈ P (States) is a set of states. A predicate Φ is called pure if it
does not depend on the heap, i.e, for every stack s and heaps h, h′ , we have
(s, h) ∈ Φ iff (s, h′ ) ∈ Φ.
4
    We use λ-expressions to denote functions: Function λX . f applied to an argument
    v evaluates to f in which every occurrence of X is replaced by v.
      Foundations for Entailment Checking in Quantitative Separation Logic                5

    We consider a separation logic SL [A] with standard semantics [47]. A distin-
guishing aspect is that SL [A] is parametrized by a set A of predicate symbols
ψ with given semantics JψK ∈ P (States). We often identify predicate symbols ψ
with their predicates JψK. Elements of A build the atoms of SL [A]. Our reduc-
tion from quantitative entailments to qualitative entailments does not depend
on the choice of these predicate symbols. We therefore take a generic approach
that allows for user-defined atoms, e.g., list or tree predicates.
Definition 1. Let A be a countable set of predicate symbols. Formulae in sepa-
ration logic SL [A] with atoms in A adhere to the grammar
  ϕ    →     ϑ | ¬ϕ | ϕ ∧ ϕ | ϕ ∨ ϕ | ∃x : ϕ | ∀x : ϕ | ϕ ⋆ ϕ | ϕ −−⋆ ϕ ,
where ϑ ∈ A, and where x ∈ Vars.                                                          △
The Boolean connectives ¬, ∧, and ∨ as well as the quantifiers ∃ and ∀ are
standard. ⋆ is the separation conjunction and −−⋆ is the magic wand.
    The semantics JϕK ∈ P (States) of a formula ϕ ∈ SL [A] is defined by induction
on the structure of ϕ as shown in Table 2. Recall that we assume the semantics
JψK of predicate symbols ψ ∈ A to be given. We often write (s, h) |= ϕ instead
of (s, h) ∈ JϕK. For ϕ, ψ ∈ SL [A], we say that ϕ entails ψ, denoted ϕ |= ψ, if
whenever (s, h) ∈ States such that (s, h) |= ϕ, also (s, h) |= ψ.
Example 1. Let Vals = Z, Locs = N>0 , and k = 1. A term t is either a variable
x ∈ Vars or the constant 0 ∈ Vals. The set A of predicate symbols is
      A = { true, emp, x 7→ t, t = t′ , t 6= t′ , ls (t, t′ ) | x ∈ Vars, t, t′ terms }
Here, apart from standard predicates for true, equalities, and disequalities,
1. emp is the empty-heap predicate, i.e.,
                                 (s, h) |= emp    iff   dom (h) = ∅ ,
2. x 7→ t is the points-to predicate, i.e.,
                 (s, h) |= x 7→ t     iff dom (h) = {s(x)} and h(s(x)) = t(s) ,
3. the list predicate ls (t, t′ ) asserts that the heap models a singly-linked list
   segment from t to t′ :
                  (s, h) |= ls (t, t′ )
           iff    dom (h) = ∅ and t(s) = t′ (s) or
                  there exist n ≥ 1 and terms t1 , . . . , tn with tn = t′ such that
                  (s, h) |= t 7→ t1 ⋆ . . . ⋆ tn−1 7→ tn .
In this setting, SL [A] contains, e.g., the well-known symbolic heap fragment of
separation logic with lists. For instance, the SL [A] formula
                             ∃y : ∃z : x 7→ y ⋆ y 7→ z ⋆ ls (z, 0) .
asserts that the heap consists of a list with head x of length at least 2.                △
6       Batz et al.

                        Table 3. Semantics of QSL [A] formulae.

       f                        Jf K (s, h)
       [ψ]                      [ψ] (s, h)
       [π] · g + [¬π] · u       [π] (s, h) · JgK (s, h) + [¬π] (s, h) · JuK (s, h)
       q · g + (1 − q) · u      q · JgK (s, h) + (1 − q) · JuK (s, h)
       g·u                      JgK (s, h) · JuK (s, h)
       1−g                      1 − JgK (s, h)
       g max u                  max{JgK (s, h), JuK (s, h)}
       g min u                  min{JgK (s, h), JuK (s, h)}
                                    
       Sx : g                   max JgK (s [x:=v] , h) | v ∈ Vals
       J x: g
                                   
                                min JgK (s [x:=v] , h) | v ∈ Vals
       g⋆u                      max {JgK (s, h1 ) · JuK (s, h2 ) | h = h1 ⋆ h2 }
       [ψ] −−⋆ g                inf {JgK (s, h ⋆ h′ ) | h′ ⊥ h and [ψ] (s, h) = 1}



2.3   Quantitative Separation Logic
In quantitative separation logic [8,38], formulae evaluate to non-negative real
numbers or infinity instead of truth values. By conservatively extending the
weakest preexpectation calculus by McIver & Morgan [40], this enables the com-
positional verification of probabilistic pointer programs by reasoning about ex-
pected list-sizes, probabilities of terminating with an empty heap, and alike.
    We consider here a fragment of quantitative separation logic suitable for rea-
soning about the likelihood of events in probabilistic pointer programs such as,
e.g., the probability of terminating in a given symbolic heap. The formulae we
consider evaluate to rational probabilities rather than arbitrary reals or infinity.
We denote the set [0, 1] ∩ Q≥0 of rational probabilities by P. Like SL [A], quanti-
tative separation logic is parameterized by a set A of predicate symbols ψ with
given semantics JψK ∈ P (States), building the atoms of QSL [A].
Definition 2. Let A be a countable set of predicate symbols. Formulae in quan-
titative separation logic QSL [A] with atoms in A adhere to the grammar

             f   →    [ψ] | [π] · f + [¬π] · f | q · f + (1 − q) · f | f · f
                      | 1 − f | f max f | f min f | Sx : f | J x : f
                      | f ⋆ f | [ψ] −−⋆ f ,

where ψ, π ∈ A with π pure, q ∈ P, and where x ∈ Vars.                               △
The semantics of a formula f ∈ QSL [A] is a (one-bounded) expectation. The set
E≤1 of one-bounded expectations is defined as

                            E≤1 = {X | X : States → [0, 1]} .
      Foundations for Entailment Checking in Quantitative Separation Logic        7

We use the Iverson bracket [29] notation [Φ] to associate with predicate Φ its
indicator function. Formally,
                                                (
                                                  1, if (s, h) ∈ Φ
           [Φ] : States → {0, 1}, [Φ] (s, h) =
                                                  0, if (s, h) 6∈ Φ .

Given a predicate symbol ψ, we often write [ψ] instead of [JψK]. The semantics
Jf K ∈ E≤1 of f ∈ QSL [A] is defined by induction on the structure of f in Table 3.
We write f ≡ g if f and g are equivalent, i.e. if Jf K = JgK. Infima and suprema are
taken over the complete lattice ([0, 1], ≤). In particular, inf ∅ = 1 and sup ∅ = 0.

Theorem 1. The semantics of QSL [A] formulae is well-defined, i.e., for all
f ∈ QSL [A], we have Jf K ∈ E≤1 .
Proof. By induction on the structure of f . For details see Appendix A.
Let us go over the individual constructs. Formulae of the form [ψ] are the atomic
formulae. [π] · g + [¬π] · u is a Boolean choice between g and u that does not
depend upon the heap since JπK is pure. q · g + (1 − q) · u is a convex combination
of g and u. g ·u is the pointwise multiplication of g and u. 1−g is the quantitative
(or probabilistic) negation of g. g max u and g min u is the pointwise maximum
and minimum of g and u, respectively.
    Sx : g is the supremum quantification that, given a state (s, h), evaluates to
the supremum of the set obtained from evaluating g in (s [x:=v] , h) for every
value v ∈ Vals. In our setting, this supremum is actually a maximum. Dually,
J x : g is the infimum quantification.
    ⋆ and −−⋆ are the quantitative analogous of the separating conjunction and
the magic wand from separation logic as defined in [8]. g ⋆ u is the quantitative
separating conjunction of g and u. Intuitively speaking, whereas the qualitative
separating conjunction maximizes a truth value under all appropriate partition-
ings of the heap, the quantitative separating conjunction maximizes a probability.
[ψ] −−⋆ u is the quantitative magic wand. Whereas the qualitative magic wand
minimizes a truth value under all appropriate extensions of the heap, the quan-
titative magic wand minimizes a probability. For an in-depth treatment of these
connectives, we refer to [8].
Example 2. Let Vals, Locs, k, and A be as in Example 1. Then QSL [A] contains,
e.g., a quantitative extension of the symbolic heap fragment of separation logic
with lists. For instance, the QSL [A] formula

           0.7 · (Sy : Sz : [x 7→ y] ⋆ [y 7→ z] ⋆ [ls(z, 0)]) + 0.3 · [emp]

expresses that with probability 0.7 the heap consists of a list with head x of
length at least 2 and that with probability 0.3 the heap is empty.          △
   Finally, given f, g ∈ QSL [A], we say that f entails g, denoted f |= g, if

                for all (s, h) ∈ States :   Jf K (s, h) ≤ JgK (s, h) .
8       Batz et al.

Quantitative entailments f |= g generalize classical entailments in the sense that
f (pointwise) lower-bounds the quantity g. For example, if g assigns to each
state the probability that some program C terminates without a memory error,
then the entailment [true] |= g means that C terminates almost-surely, i.e., with
probability one. Our problem statement now reads as follows: Reduce entailment
checking in QSL [A] to checking finitely many entailments in SL [A].


3     Entailments in Probabilistic Program Verification
Our primary motivation for studying the entailment problem for quantitative
separation logic is to provide foundations for the automated verification of proba-
bilistic pointer programs. In this section, we consider examples of such programs
written in hpGCL—an extension of McIver & Morgan’s probabilistic guarded
command language (cf., [40]) by heap-manipulating instructions— and the en-
tailments that arise from their verification. We briefly formalize reasoning about
hpGCL programs with weakest liberal preexpectations; for a thorough introduc-
tion of hpGCL programs and techniques for their verification, we refer to [8,38].

3.1   Heap-manipulating pGCL
Recall from Section 2.1 that heaps map memory locations to fixed-size records (or
tuples) of length k ≥ 1. The set of programs in heap-manipulating probabilistic
guarded command language for k = 1, Vals = Z and Locs = N>0 , denoted hpGCL,
is given by the grammar

           C   −→ skip                              (effectless program)
                  | x := E                                  (assignment)
                      | {C } [p] {C }                     (prob. choice)
                      | C; C                         (seq. composition)
                      | if ( B ) { C } else { C }   (conditional choice)
                      | while ( B ) { C }                         (loop)
                      | x := new (E)                        (allocation)
                      | free(E),                              (disposal)
                      | x := < E >                             (lookup)
                      | < E > := E ′                        (mutation)

where x ∈ Vars, p ∈ P, E, E ′ are arithmetic expressions and B is a Boolean
expression. We assume that expressions do not depend on the heap. For now,
we do not fix a specific syntax for expressions but assume evaluation mappings

                E : Stacks → Z    and B : Stacks → {true, false} .

In addition to the usual control flow structures for sequential composition, con-
ditionals, and loops, skip does nothing, x := E assigns the value E(s) obtained
       Foundations for Entailment Checking in Quantitative Separation Logic            9

Table 4. Rules for compositionally computing weakest liberal preexpectations. Here, f
is a QSL [A] formula representing the postexpectation. f [x:=E] denotes the substitution
of every free occurrence of x by E in f . [E 7→ − ] desugars to Sz : [E 7→ z].

           C                             wlpJCK (f )
           skip                          f
           x := E                        f [x:=E]
           { C1 } [ p ] { C2 }           p · wlpJC1 K (f ) + (1 − p) · wlpJC2 K (f )
                                                                 
           C1 ; C2                       wlpJC1 K wlpJC2 K (f )
           if ( B ) { C1 } else { C2 }   [B] · wlpJC1 K (f ) + [¬B] · wlpJC2 K (f )
           x := new (E)                  J y : [y 7→ E] −−⋆ f [x:=y]
           free(E)                       [E 7→ − ] ⋆ f
                                                                              
           x := < E >                    Sy : [E 7→ y] ⋆ [E 7→ y] −−⋆ f [x:=y]
           < E > := E ′                  [E 7→ − ] ⋆ E 7→ E ′ −−⋆ f
                                                                    




from evaluating expression E in the current program state (s, h) to x, and the
probabilistic choice { C1 } [ p ] { C2 } flips a coin with bias p—it executes C1 if
the coin flip yields heads, and C2 otherwise. The allocation x := new (E) non-
deterministically selects a fresh location, stores it in x, and puts a record with
value E on the heap at that location. Since we assume an infinite address space,
allocation never fails. Conversely, free(E) disposes the record at location E
from the heap; it fails if no such location exists. The mutation < E > := E ′ and
the lookup x := < E > update to E ′ resp. assign to x the value stored at location
E; both statements fail if the heap contains no such location.


3.2    Weakest Liberal Preexpectations

We formalize reasoning about hpGCL programs in terms of the weakest liberal
preexpectation transformer wlp : hpGCL → (QSL [A] → QSL [A]), where A at
least contains formulae of the form [E 7→ E ′ ]; Table 4 summarizes the rules for
computing wlp of loop-free programs on the program structure.
    Conceptually, the weakest liberal preexpectation JwlpJCK (f )K (s, h) of pro-
gram C with respect to postexpectation f ∈ QSL [A] on (s, h) is the least ex-
pected value of Jf K (measured in the final states) after successful5 termination
of C on initial state (s, h), plus the probability that C does not terminate on
(s, h). Adding the non-termination probability can be thought of as a partial cor-
rectness view: we include the non-termination probability of C on state (s, h) in
the wlp of C just as we include the state (s, h) in the weakest liberal precondition
of C in case C does not terminate on (s, h).
5
    i.e., without encountering a memory error.
10        Batz et al.

    A reader familiar with separation logic will realize the close similarity be-
tween the rules in Table 4 and the weakest preconditions for SL by Ishtiaq and
O’Hearn [28]. The main differences are (1) the use of the quantitative connec-
tives ⋆, −−⋆ , and ·, and +, and (2) the additional rule for probabilistic choice,
wlpJ{ C1 } [ p ] { C2 }K (f ), which is a convex sum that weights wlpJC1 K (f ) and
wlpJC2 K (f ) by p and (1 − p), respectively.
    The transformer wlp is well-defined in the sense that, for every loop-free
hpGCL-program and every QSL [A] formula, we obtain—under mild conditions—
again a QSL [A] formula:
Theorem 2. Let C ∈ hpGCL be loop-free and A be a set of predicate symbols. If
1. A contains the points-to predicate for all variables and all expressions occur-
   ring in allocation, disposal, lookup and mutation in C,
2. A contains all guards and their negations occurring in C, and
3. all predicates in A are closed under substitution of variables by variables and
   arithmetic expressions occurring on right-hand sides of assignments in C,
then, for every QSL [A] formula f , wlpJCK (f ) ∈ QSL [A].
Proof. By induction on loop-free C. For details see Appendix B.1.
For loops, wlpJwhile ( B ) { C }K (f ) is typically characterized as the greatest
fixed point of loop unrollings. However, we fixed an explicit syntax of formu-
lae instead of allowing arbitrary expectations; the above fixed point is in general
not expressible in our syntax.6 To deal with loops, we thus require a user-supplied
invariant I and apply the following proof rule (cf., [33]) to approximate wlp:

      I |= [¬B] · f + [B] · wlpJC ′ K (I)   implies   I |= wlpJwhile ( B ) { C ′ }K (f )

Notice that verifying that I is indeed an invariant via the above rule requires
proving an entailment between QSL [A] formulae.

3.3     Interfered Swap
Our first example concerns a program Cswap , implemented in hpGCL below, that
attempts to swap the contents of two memory locations x and y. However, since
variable x is shared with a concurrently running process, writing to x can be un-
reliable, that is, instead of the intended value, the concurrently running process
may write a corrupted value err into memory with some probability, say 0.001.
A similar situation occurs, e.g., when using the protocol described in [2].

                 Cswap :      tmp1 := < x > ;
                              tmp2 := < y > ;
                              { < x > := tmp2 } [ 0.999 ] { < x > := err } ;
                              < y > := tmp1 .
6
     It is noteworthy that a sufficiently expressive syntax for weakest preexpectation
     reasoning without heaps has been developed only recently [7].
        Foundations for Entailment Checking in Quantitative Separation Logic                11

We can use wlp to verify an upper bound on the probability that an erroneous
write operation happened by solving the QSL entailment

      wlpJCswap K ([x 7→ z2 ] ⋆ [y 7→ z1 ])
|= [z2 = err] · ([x 7→ z1 ] ⋆ [y 7→ z2 ]) + [z2 6= err] · (0.999 · ([x 7→ z1 ] ⋆ [y 7→ z2 ])) .

That is, the probability that Cswap successfully swaps the contents of x and y is
at most 0.999 if y does initially not point to the corrupt value err.
    As we will see in Section 6.1, our approach for solving QSL entailments is
capable of deciding the above entailment, where wlpJCswap K ([x 7→ z2 ] ⋆ [y 7→ z1 ])
is computed according to the rules in Table 4.

3.4     Avoiding Magic Wands
Recall from Table 4 that computing wlp introduces a magic wand (−−⋆ ) for
almost every statement that accesses the heap. This is unfortunate because many
decidable separation logic fragments as well as practical entailment solvers do
not support magic wands.
   In particular, in Section 6.1 we present a QSL fragment with a decidable
entailment problem that supports magic wands only on the left-hand side of
entailments. Hence, proving a lower bound on the probability that the program
Cswap from above successfully swapped the contents of two memory cells, e.g.,

           0.98 · ([x 7→ z2 ] ⋆ [y 7→ z1 ]) |= wlpJCswap K ([x 7→ z1 ] ⋆ [y 7→ z2 ]) ,      (†)

might still be possible with our technique but requires a different separation
logic fragment to reduce to.
    Fortunately, we can often avoid introducing magic wands by employing lo-
cal reasoning and rules for computing wlp for specific pre- and postexpecta-
tions. In particular, the wlp calculus features (1) the frame rule from sepa-
ration logic, i.e., if no free variable in g is modified by C, then wlpJCK (f ) ⋆
g |= wlpJCK (f ⋆ g), (2) super-distributivity for convex combinations and maxi-
mum, i.e., q · wlpJCK (f ) + (1 − q) · wlpJCK (g) |= wlpJCK (q · f + (1 − q) · g) and
wlpJCK (f ) max wlpJCK (g) |= wlpJCK (f max g), and (3) monotonicity, i.e., f |= g
implies wlpJCK (f ) |= wlpJCK (g). Moreover, we give four examples of specialized
rules that avoid magic wands but require specific postexpectations: if x is not a
free variable of E or f , and x and y are distinct variables, then
  (i) wlpJx := < E >K (([E 7→ y] · [x = y]) ⋆ f ) = [E 7→ y] ⋆ f [x:=y] ;
 (ii) wlpJ< E > := E ′ K ([E 7→ E ′ ] ⋆ f ) = [E 7→ − ] ⋆ f ;
(iii) wlpJx := new (x)K (Sy : [x 7→ y] ⋆ f ) = f [y:=x] ; and
(iv) wlpJx := new (y)K ([x 7→ y] ⋆ f ) = f .
Similar rules have been used successfully for symbolic execution with separation
logic in non-probabilistic settings [12]. Combining the above rules with fram-
ing, distributivity, and monotonicity often allows avoiding magic wands. In such
cases, we have a richer set of decidable SL fragments upon which to build solvers
12        Batz et al.

for QSL entailments at our disposal. Coming back to the entailment (†) from
above and writing Cswap = C1 ; C2 ; C3 ; C4 , we calculate

         wlpJCswap K ([x 7→ z1 ] ⋆ [y 7→ z2 ])
     =| wlpJCswap K ([y 7→ tmp1] ⋆ [x 7→ tmp2] · [tmp1 = z2 ] · [tmp2 = z1 ])
                                                                       (monotonicity)
     =| wlpJC1 ; C2 ; C3 K(wlpJC4 K ([y 7→ tmp1])                               (framing)
                       ⋆ ([x 7→ tmp2] · ([tmp1 = z2 ] · [tmp2 = z1 ])))
     =| wlpJC1 ; C2 ; C3 K ([y 7→ − ] ⋆ ([x 7→ tmp2] · ([tmp1 = z2 ] · [tmp2 = z1 ])))
                                                                             (Rule (ii))
     ..
      .

     =| wlpJC1 K (0.999 · ([y 7→ z1 ] ⋆ ([tmp1 = z2 ] · [x 7→ − ])) + 0.001 · [false])
                                                                                 (Rule (i))
     =| 0.999 · wlpJC1 K (([x 7→ z2 ] · [tmp1 = z2 ]) ⋆ [y 7→ z1 ]) + 0.001 · [false]
                            (super-distributivity, monotonicity and commutativity)
     =| 0.999 · ([x 7→ z2 ] ⋆ [y 7→ z1 ]) + 0.001 · [false]                     (Rule (i))


 which yields a preexpectation without magic wand. Hence, we obtain a magic
wand-free entailment in (†). We have used our technique to transform this quan-
titative entailment into several qualitative entailments and checked them success-
fully using the separation logic extension of CVC4 [46]. Detailed calculuations,
the resulting qualitative entailments, and the input for CVC4 in SMT-LIB 2
format are found in Appendix B.2.

3.5      Randomized List Population
Our second example populates a singly-linked list by flipping coins and adding
a list element until the coin flip yields heads, i.e., we consider the program

                  Cpopulate :       while ( c 6= 0 ) {
                                          { c := 0 } [ 0.5 ] { x := new (x) }
                                    },

where x is the head of a linked list. Assume we would like to determine a lower
bound on the probability that the above program does not crash and produces a
list of length at least two7 . For that, recall from Example 1 the separation logic
formula ls(x, y) for singly-linked list segments. The aforementioned probability
is then given by wlpJCpopulate K (f ) for postexpectation

                     f = Sy : Sz : [x 7→ y] ⋆ [y 7→ z] ⋆ [ls(z, 0)] .
7
     plus the probability of nontermination, which is 0.
      Foundations for Entailment Checking in Quantitative Separation Logic                 13

We propose the loop invariant I below to show that I |= wlpJCpopulate K (f ), i.e.,
I is a lower bound on the sought-after probability.
 I = Sy : [x 7→ y] ⋆ [c = 0] · Sz : [y 7→ z] ⋆ [ls(z, 0)]
                                                                                          
                        + [c 6= 0] · 1/2 · (Sz : [y 7→ z] ⋆ [ls(z, 0)] + 1/2 · [ls(z, 0)]) .
To verify that I is indeed a loop invariant (hint: it is), we need to prove that
       I |= [c = 0] · f + [c 6= 0] · wlpJ{ c := 0 } [ 0.5 ] { x := new (x) }K (I) .
As described in Section 3.4, we can compute wlp in a way such that the resulting
formula contains no magic wands. Our reduction from QSL entailments to stan-
dard SL entailments then allows us to discharge the above invariant check using
existing separation logic solvers with support for fixed list predicates, e.g., [45].

4     Quantitative Entailment Checking
We present our main contribution of reducing entailment checking in QSL [A] to
entailment checking in SL [A]. We consider the key observations leading to our
reduction in Section 4.1. We then deal with the formalization and more technical
considerations of our approach in Sections 4.2 and 4.3.

4.1   Idea and Key Observations
We reduce entailment checking in QSL [A] to entailment checking in SL [A], i.e.,
    Given f, g ∈ QSL [A], we reduce checking f |= g to checking finitely many
                entailments of the form ϕ |= ψ with ϕ, ψ ∈ SL [A].
We instantiate QSL [A] and SL [A], respectively, for the sake of concreteness. For
that, we fix the set A of predicate symbols given by
            A = { true, emp, x = y, x 6= y, x 7→ y | x, y ∈ Vars } .
Now, consider the following entailment u1 |= u2 as a running example:
u1 = 0.4 · ([x 7→ y] ⋆ [y 7→ z]) + 0.6 · [x 7→ y] |= 0.6 · ([x 7→ y] ⋆ [true]) = u2 .
            |       {z        }          | {z }
                     =g1                     =g2

Intuitively speaking, u1 expresses that with probability 0.4 the heap consists
of two cells where x points to y and separately y points to z, and that with
probability 0.6 the heap consists of a single cell where x points to y. Formula u2
expresses that with probability 0.6 the heap contains a cell where x points to y.
How can we reduce the problem of checking whether u1 |= u2 holds to checking
finitely many entailments in SL [A]? We rely on two key observations:

Observation 1. For every f ∈ QSL [A], the set
                  Eval (f ) = {Jf K (s, h) | (s, h) ∈ States} ⊂ P
is finite. Moreover, there is an effectively constructible finite and sound overap-
proximation Val [f ] of Eval (f ), i.e., Eval (f ) ⊆ Val [f ].
14      Batz et al.

Example 3. Consider the expectation u1 from our running example: We have
Eval (u1 ) = {0, 0.4, 0.6}. We construct a finite overapproximation of Eval (u1 ) as
follows: First, we observe that both subformulae g1 and g2 evaluate to a value
in {0, 1}, i.e, Val [g1 ] = Val [g2 ] = {0, 1}. From Val [g1 ] and Val [g2 ], we obtain a
finite overapproximation Val [u1 ] of Eval (u1 ) given by
 Val [u1 ] = {0.4 · α + 0.6 · β | α ∈ Val [g1 ] , β ∈ Val [g2 ]} = {0, 0.4, 0.6, 1} .
Notice that Val [u1 ] is a proper superset of Eval (u1 ) since 1 6∈ Eval (u1 ).       △
We consider the construction of Val [f ] for arbitrary f ∈ QSL [A] in Section 4.2.

Observation 2. Given f ∈ QSL [A] and a probability α ∈ P, there is an effec-
tively constructible SL [A] formula, which we denote by ⌈α  f ⌉, such that (s, h)
is a model of ⌈α  f ⌉ if and only if f evaluates at least to α on state (s, h), i.e.,
                  (s, h) |= ⌈α  f ⌉       iff     α ≤ Jf K (s, h) .
                  |        {z      }               |   {z        }
                        in SL[A]                       in QSL[A]

We can thus lower bound QSL [A] formulae in terms of SL [A] formulae.
Example 4. Continuing our running example, we construct ⌈0.5  u1 ⌉, i.e., an
SL [A] formula evaluating to true on state (s, h) if and only if u1 evaluates at
least to 0.5. We start by considering the subformulae of u1 . Since both g1 and
g2 embed SL [A] predicates, we have for every α ∈ P
                      ⌈α  g1 ⌉ = true if α = 0 else x 7→ y ⋆ y 7→ z
                and ⌈α  g2 ⌉ = true if α = 0 else x 7→ y .
The intuition is as follows: α = 0 lower bounds every probability. Conversely, if
α > 0 then α lower bounds g1 (resp. g2 ) on state (s, h) if and only if (s, h) satisfies
the predicate g1 (resp. g2 ). Now, when does u1 evaluate at least to 0.5? Given
Val [g1 ] and Val [g2 ] and the fact that the valuation of u1 is a convex combination
of the valuations of g1 and g2 , there are (at most) two cases: Either both g1 and
g2 evaluate to (at least) 1, or g2 (but not necessarily g1 ) evaluates to (at least) 1.
Given ⌈1  g1 ⌉ and ⌈1  g2 ⌉, the aforementioned informal disjunction translates
to a formal disjunction in SL [A]:
                                                      
                ⌈0.5  u1 ⌉ = ⌈1  g1 ⌉ ∧ ⌈1  g2 ⌉ ∨ ⌈1  g2 ⌉
                                                            
                              = (x 7→ y ⋆ y 7→ z) ∧ x 7→ y ∨ x 7→ y .
Notice that—as it is the case for Val [u1 ]—we construct ⌈0.5  u1 ⌉ syntactically.
In particular, we disregard that the disjunct (x 7→ y ⋆ y 7→ z) ∧ x 7→ y is
unsatisfiable and therefore equivalent to false.                                 △
We provide the construction of ⌈α  f ⌉ for arbitrary QSL [A] formulae f —
including quantitative quantifiers and the magic wand—in Section 4.3.

    Finally, Observations 1 and 2 together yield our reduction from f |= g to
finitely many entailments in SL [A]. Intuitively speaking, we formalize that
      Foundations for Entailment Checking in Quantitative Separation Logic               15

                         Table 5. Inductive definition of Val [f ].


               f ∈ QSL [A]                 Val [f ] ⊂ P
               [ψ]                         {0, 1}
               [π] · g + [¬π] · u          Val [g] ∪ Val [u]
               q · g + (1 − q) · u         p · Val [g] + (1 − p) · Val [u]
               g·u                         Val [g] · Val [u]
               1−g                         1 − Val [g]
               g max u                     Val [g] max Val [u]
               g min u                     Val [g] min Val [u]
               Sx : g                      Val [g]
               J x: g                      Val [g]
               g⋆u                         Val [g] · Val [u]
               [ψ] −−⋆ g                   Val [g]



      whenever f evaluates at least to α, then g too evaluates at least to α
equivalently in terms of finitely many SL [A] entailments. Put more formally,
since Val [f ] is finite, we have

    f |= g
iff for all (s, h) : Jf K (s, h) ≤ JgK (s, h)                                (by definition)
iff for all (s, h) and all α ∈ Val [f ]: α ≤ Jf K (s, h) implies α ≤ JgK (s, h)
                                                                  (by Observation 1)
iff for all (s, h) and all α ∈ Val [f ]: (s, h) |= ⌈α  f ⌉ implies (s, h) |= ⌈α  g⌉
                                                                  (by Observation 2)
iff for all α ∈ Val [f ] : ⌈α  f ⌉ |= ⌈α  g⌉ .                             (by definition)



Example 5. Reconsider our running example. Since |Val [u1 ] | = 4, the QSL [A]
entailment u1 |= u2 is equivalent to the four entailments

                     ⌈α  u1 ⌉ |= ⌈α  u2 ⌉ for α ∈ {0, 0.4, 0.6, 1}

in SL [A], each of which actually holds.                                                 △

4.2   Constructing Finite Overapproximations of Eval (f )
We consider the formal construction underlying Observation 1 from the previous
section, i.e., given f ∈ QSL [A], we provide a syntactic construction of a finite
16      Batz et al.

overapproximation Val [f ] of Eval (f ). This construction is by induction on the
structure of f as shown in Table 5. For that, we define some shorthands. Given
α ∈ P, V, W ⊆ P, and a binary operation ◦ : P × P → P, we define
     α · V = {α · β | β ∈ V }       and V ◦ W = {β ◦ γ | β ∈ V, γ ∈ W } .
Let us now go over the individual cases.

The case f = [ψ]. We have [ψ] (s, h) ∈ {0, 1} by definition.

The case f = [π] · g + [¬π] · u. For every (s, h), the formula f either evalu-
ates to JgK (s, h) or to JuK (s, h), depending on whether (s, h) |= π holds.

The case f = p · g + (1 − p) · u. The formula f evaluates to p · α + (1 − p) · β for
some α ∈ Val [g] and β ∈ Val [u].

The case f = g · u or f = g ⋆ u. The formula f evaluates to α · β for some
α ∈ Val [g] and β ∈ Val [u].

The case f = 1 − g. The formula f evaluates to 1 − α for some α ∈ Val [g].

The case f = g ◦ u for ◦ ∈ {max, min}. Since max and min are defined point-
wise, the formula f evaluates to some value α ◦ β for α ∈ Val [g] , β ∈ Val [u].

The case f = Sx : g or f = J x : g. Since Val [g] overapproximates the set of
all valuations of g, quantitative quantifiers do not add any valuation.

The case f = [ψ] −−⋆ g. Recall that
         Jf K (s, h) = inf {JgK (s, h ⋆ h′ ) | h′ ⊥ h and [ψ] (s, h′ ) = 1} .
If the above set is non-empty, the infimum is actually a minimum and therefore
f evaluates to some value in Val [g]. If the above set is empty, then Jf K (s, h) = 1.
It is easy to verify that 1 is necessarily an element of Val [g] (cf., Lemma 4).

Summarizing our considerations on Val [f ], we get:
Theorem 3. For every f ∈ QSL [A], the effectively constructible set Val [f ] ⊂ P
given in Table 5 satisfies
                      |Val [f ] | < ∞   and   Eval (f ) ⊆ Val [f ] .
Proof. Straightforward by induction on f .

4.3    Lower Bounding QSL [A] by SL [A] Formulae
We now consider the formal construction underlying Observation 2 from Sec-
tion 4.1. That is, given f ∈ QSL [A] and α ∈ P, we provide the syntactic con-
struction of an SL [A] formula ⌈α  f ⌉ evaluating to true on state (s, h) if and
         Foundations for Entailment Checking in Quantitative Separation Logic           17

               Table 6. Inductive definition of ⌈α  f ⌉ for a given α ∈ P.


   f ∈ QSL [A]                ⌈α  f ⌉ ∈ SL [A]
   [ψ]                        true if α = 0 else ψ
   [π] · g + [¬π] · u         (π ∧ ⌈α  g⌉) ∨ (¬π ∧ ⌈α  u⌉)
                              W
   q · g + (1 − q) · u            β∈Val[g],γ∈Val[u],p·β+(1−p)·γ≥α   ⌈β  g⌉ ∧ ⌈γ  u⌉
                              W
   g·u                            β∈Val[g],γ∈Val[u],β·γ≥α   ⌈β  g⌉ ∧ ⌈γ  u⌉
   1−g                        true if α = 0 else ¬ ⌈δ  f ⌉
                                  for δ = min { β ∈ Val [g] | β > 1 − α }
   g max u                    ⌈α  g⌉ ∨ ⌈α  u⌉
   g min u                    ⌈α  g⌉ ∧ ⌈α  u⌉
   Sx : g                     ∃x : ⌈α  g⌉
   J x: g                     ∀x : ⌈α  g⌉
                              W
   g⋆u                            β∈Val[g],γ∈Val[u],β·γ≥α   ⌈β  g⌉ ⋆ ⌈γ  u⌉
   [ψ] −−⋆ g                  ψ −−⋆ ⌈α  g⌉




only if f evaluates at least to α on (s, h). This construction relies on Val [f ] from
the previous section and is given by induction on the structure of f as shown in
Table 6. We consider the individual constructs. For that, we fix some state (s, h).

The case f = [ψ]. There are two cases. If α = 0, then α trivially lower bounds
the value of [ψ]. Conversely, if α > 0, then α lower bounds [ψ] on state (s, h) if
and only if (s, h) satisfies ψ.

For the composite cases, recall that by Theorem 3 there are effectively con-
structible finite sets Val [g] , Val [u] covering all values g and u evaluate to.

The case f = [π]·g + [¬π]·u. The formula f represents a Boolean choice between
the formulae g and u, depending on the truth value of π. Hence, there are two
cases: If (s, h) does satisfy π, then α lower bounds f iff α lower bounds g. Con-
versely, if (s, h) does not satisfy π, then α lower bounds f iff α lower bounds u.

The case f = p · g + (1 − p) · u. Since Val [g] and Val [u] cover every possible
valuation of g and u, respectively, it follows that α lower bounds the valua-
tion of f if and only if there are β ∈ Val [g] and γ ∈ Val [u] such that (1) β
lower bounds g, (2) γ lower bounds u, and (3) α lower bounds the convex sum
p · β + (1 − p) · γ.

The case f = g · u. The reasoning is analogous to the previous case.
18      Batz et al.

The case f = 1 − g. We write α ≤ J1 − gK (s, h) equivalently as ¬(1 − α <
JgK (s, h)). In order to turn the strict inequality into a non-strict one, we con-
sider the successor δ of 1 − α in Val [g], i.e., the smallest δ in Val [g] greater than
1 − α. Since Val [g] is finite, such a δ always exists if 1 − α 6= 1. We illustrate the
idea in the following picture, where all elements in Val [g] are marked by •.

                • • •        •                  •    •     • • •
                0                      1−α      δ     JgK (s, h) 1

For the successor δ, checking if δ is a lower bound of JgK (s, h) is equivalent to
checking if 1 − α is a strict lower bound - if δ is not a lower bound, then we ran
out of possible valuations that are strictly lower bounded by 1 − α.

The case f = g ◦ u for ◦ ∈ {max, min}. The probability α lower bounds the
maximum of g and u on state (s, h) if and only if α lower bounds g or α lower
bounds u. For ◦ = min, the reasoning is dual.

The case f = Sx : g. Recall that
                                 
                Jf K (s, h) = max JgK (s [x:=v] , h) | v ∈ Vals .

Now observe that α lower bounds the above maximum if and only if α lower
bounds some element of the above set, i.e., if and only if there is some v with

 α ≤ JgK (s [x:=v] , h)       which is equivalent to       (s, h) |= ∃x : ⌈α  g⌉ .

The case f = J x : g. Recall that
                                 
                Jf K (s, h) = min JgK (s [x:=v] , h) | v ∈ Vals .

Since α lower bounds the above minimum if and only if α lower bounds all ele-
ments of the above set, the reasoning is dual to the previous case.

The case f = g ⋆ u. Recall that

           Jf K (s, h) = max {JgK (s, h1 ) · JuK (s, h2 ) | h = h1 ⋆ h2 } .

Since Val [g] and Val [u] cover every possible valuation of g and u, respectively,
α lower bounds the evaluation of f on (s, h) iff there are β ∈ Val [g] , γ ∈ Val [u]
and h1 , h2 with h1 ⋆ h2 = h such that (1) β lower bounds g on (s, h1 ), (2) γ lower
bounds u on (s, h2 ), and (3) α lower bounds β · γ. Given such β andγ, we can
phrase this equivalently in SL [A] as

                           (s, h) |= ⌈β  g⌉ ⋆ ⌈γ  u⌉ .

The case f = [ψ] −−⋆ g. Recall that

         Jf K (s, h) = inf {JgK (s, h ⋆ h′ ) | h′ ⊥ h and [ψ] (s, h′ ) = 1} .
      Foundations for Entailment Checking in Quantitative Separation Logic      19

Probability α lower bounds the above infimum if and only if for every extension
h′ of the heap h such that the stack s together with h′ satisfy ψ, probability α
is a lower bound on JgK (s, h ⋆ h′ ). Put more formally, the latter statement reads

             for all h′ ⊥ h with (s, h′ ) |= ψ : (s, h ⋆ h′ ) |= ⌈α  g⌉ ,

which is equivalent to (s, h) |= ψ −−⋆ ⌈α  g⌉.

Our construction thus applies to arbitrary QSL [A] formulae and we get:
Theorem 4. For every f ∈ QSL [A] and all α ∈ P there is an effectively con-
structible SL [A] formula ⌈α  f ⌉ such that for all (s, h) ∈ States, we have

                 (s, h) |= ⌈α  f ⌉        iff    α ≤ Jf K (s, h) .

Proof. By induction on f . See Appendix C for details.

Finally, we obtain our main theorem.
Theorem 5. Entailment checking in QSL [A] reduces to entailment checking in
SL [A], i.e, for all f, g ∈ QSL [A], we have

         f |= g       iff     for all α ∈ Val [f ] : ⌈α  f ⌉ |= ⌈α  g⌉ .

Proof. Follows from Theorems 3 and 4 and the reasoning at the end of Section 4.1.

Remark 1 (Avoiding true in SL [A] entailments). Formulae of the form ⌈α 
f ⌉ ∈ SL [A] may introduce the atom true, which is not admitted by some decid-
able separation logic fragments, such as [26]. Fortunately, we can avoid true in
⌈α  f ⌉ formulae. true is only required in formulae of the form ⌈0  f ⌉, which
arise in two situations when applying Theorem 5: (1) in entailment checks of the
form ⌈0  f ⌉ |= ⌈0  g⌉, which always hold and can thus be omitted, and (2) if
f = p · g + (1 − p) · u. In the latter case, if we have α 6= 0 in
                                     _
          ⌈α  f ⌉ =                                    ⌈β  g⌉ ∧ ⌈γ  u⌉ ,
                       β∈Val[g],γ∈Val[u],p·β+(1−p)·γ≥α

then either β 6= 0 or γ 6= 0 holds for every disjunct. Hence, subformulae of the
form ⌈0  g⌉ or ⌈0  u⌉ can be omitted, as well.                              △


5   Complexity
We now analyze the complexity of our approach. Recall that Theorem 5 reduces
checking f |= g in QSL [A] to checking

                    for all α ∈ Val [f ] : ⌈α  f ⌉ |= ⌈α  g⌉

in SL [A]. We consider two aspects: (1) the number of SL [A] entailments and
(2) the size of the resulting SL [A] formulae occurring in each entailment. We
20        Batz et al.

express these quantities in terms of the size of a QSL [A] formula f and a SL [A]
formula ϕ and denote them as |f | and |ϕ| respectively. In these sizes, we count
every construct in the formula and require that the size of atoms are defined
at instantiation. Moreover, we assume that every atom in A is at least of size
1 and especially the atom true is of size 1. Additionally we count in an QSL [A]
formula f the constructs that increase the number of possible evaluation results
of f , namely q · g + (1 − q) · u, g · u and g ⋆ u, and denote it as |f |p .8
    We will see that for an entailment f |= g in QSL [A], (1) the number of SL [A]
entailments is in 2O(|f |p) in the worst case (see Theorem 6) and (2) the size of the
                                                 2                      2
resulting SL [A] formulae are in O(|f |)·2O(|f |p ) and O(|g|)·2O(|g|p ) respectively in
the worst case (see Theorem 7). Now let us assume we have an entailment checker
for SL [A] formulae that can solve entailments of the form ⌈α  f ⌉ |= ⌈α  g⌉
and which has a runtime complexity of SL-Time(n, m) where n and m are the
size of SL [A] formulae on the left and right side of an entailment respectively.
Putting the above together, checking the entailment f |= g in QSL [A] then has
a runtime complexity of
                                                   2                   2
                                                                            
               2O(|f |p) · SL-Time O(|f |) · 2O(|f |p) , O(|g|) · 2O(|g|p )
                                           2                    2
                          +O(|f |) · 2O(|f |p) + O(|g|) · 2O(|g|p) .

If we furthermore reasonably assume that SL-Time(n, m) is at least linear in both
arguments (otherwise the entailment checker can only check trivial entailments
anyway), the runtime complexity simplifies to
                                                 2                   2
                                                                         
             2O(|f |p) · SL-Time O(|f |) · 2O(|f |p) , O(|g|) · 2O(|g|p ) .

As for aspect (1), we first observe that checking f |= g by means of Theorem 5
requires checking |Val [f ] | entailments in SL [A]. However, only the constructs we
count with |f |p increase the number of possible evaluations, which in turn will
also increase the size of the overapproximation Val [f ]. Every time any of these
constructs occur, the number of possible evaluations Eval (f ) may double. Con-
sequently, also the overapproximation Val [f ] doubles in size when any of these
constructs occur. Other constructs do not increase the number of evaluations,
but instead inherit the evaluations from their subformulae.
Theorem 6. We have |Val [f ] | ≤ 2|f |p +1 . Hence, checking f |= g by means of
Theorem 5 requires checking 2O(|f |p) entailments in SL [A].

Proof. By induction on f . For details see Appendix D.

For the size of the resulting SL [A] formulae, i.e., aspect (2), recall that we con-
struct entailments of the form

                                  ⌈α  f ⌉ |= ⌈α  g⌉ .
8
     For a formal definition see Table 9 on page 37.
      Foundations for Entailment Checking in Quantitative Separation Logic          21

We thus determine an upper bound on the size of any SL [A] formula ⌈α  f ⌉.
Here we make a similar observation as in aspect (1): whenever one of the con-
structs we count with |f |p appears, the size of the formula increases by the expo-
nential factor |Val [f ] |. Such a multiplication of increasing exponential expres-
sions then results asymptotically in a squared exponent. The other constructs
increase the size by only a constant per construct. By combining both observa-
tions we can finally conclude an upper bound on the size of the formula ⌈α  f ⌉.


Theorem 7. For any formula f ∈ QSL [A] and all probabilities α ∈ P, the SL [A]
                                                       2
formula ⌈α  f ⌉ has at most size 3 · |f | · 2(|f |p+1) . Hence the size of the formula
                                2
⌈α  f ⌉ is in O(|f |) · 2O(|f |p) .

Proof. By induction on f . For details see Appendix D.

Remark 2 (Complexity of SL [A] Entailments in QSL [A]). By Theorem 6 and
Theorem 7, the number of entailments and the size of formulae ⌈α  f ⌉ is only
exponential if |f |p is not constant. However, we would assume that an entailment
f |= g in QSL [A], where neither in f nor in g the probabilistic choice p·g+(1−p)·u
appears, should have a similar runtime complexity as SL [A] entailment. While
it is easy to see that Val [f ] = {0, 1} has constant size in this setting, the size
of the formula is still exponential. In the case where no probabilistic choice is
present, we generate multiple exponentially-sized tautologies of the form ⌈0  f ⌉.
However, due to Remark 1 we can eliminate all occurrences of ⌈0  f ⌉. That
means, if f does not contain p · g + (1 − p) · u, then for α 6= 0, we can construct
an equivalent formula to ⌈α  f ⌉ in such a way that its size is in O(|f |) and
|Val [f ] | = 2.                                                                  △


6    Application: Decidable hpGCL Verification

Since entailment in full separation logic is undecidable, it is common to con-
sider fragments of separation logic with a (semi-)decidable entailment problem.
Given a QSL [A] fragment Q, we provide sufficient and easy-to-check characteri-
zations on SL [A] fragments S ensuring that entailment checking in Q reduces to
entailment checking in S. This simplifies the search for decidable fragments of
quantitative separation logic.
    We then apply our results in Section 6.1 to show the decidability of entail-
ment checking for quantitative symbolic heaps—a quantitative extension of the
well-known symbolic heap fragment of separation logic—and demonstrate the
applicability to the verification of probabilistic pointer programs.

Our reduction from entailments in QSL [A] to entailments in SL [A] relies on the
construction of the ⌈α  f ⌉ formulae from Section 4.3. This suggests to define:
Definition 3. Let Q be a QSL [A] fragment. We say that an SL [A] fragment S
is Q-admissible if ⌈α  f ⌉ ∈ S holds for all f ∈ Q and all α ∈ P.       △
22     Batz et al.

         Table 7. SL [A] requirements for entailment checking in QSL [A].

              Q fragment contains       S contains/is closed under
              [ψ]                       ψ, true
              [π] · f + [¬π] · g        π,¬π, ∧, ∨
              p · f + (1 − p) · g       ∧, ∨
              f ·g                      ∧, ∨
              1−f                       ¬, true
              f max g                   ∨
              f min g                   ∧
              Sx : f                    ∃
              J x: f                    ∀
              f ⋆g                      ⋆, ∨
              [ψ] −−⋆ f                 ψ −−⋆ ·



The syntactic nature of our construction of the S formulae ⌈α  f ⌉ allows for a
syntactic criterion on SL [A] fragments to be Q-admissible.
Lemma 1. Let Q be a QSL [A] fragment. If an SL [A] fragment S satisfies the
requirements provided in Table 7, then S is Q-admissible.
Proof. By induction on f . For details see Appendix E.
Finally, we provide a sufficient criterion for the decidability of entailment in
QSL [A] fragments given SL [A] fragments with a decidable entailment problem.
Since entailment checks ϕ |= ψ in SL [A] can often (but not always) be reduced
to unsatisfiability checks ϕ ∧ ¬ψ, we take a more fine-grained perspective and
distinguish between fragments for the left- and the right-hand side of entail-
ments, respectively. This distinction matters when, e.g., SL [A] fragments with a
decidable satisfiability problem impose restrictions on quantifiers (cf., [19]).
Theorem 8. Let Q1 , Q2 be QSL [A] fragments, and let S1 , S2 be SL [A] frag-
ments. If S1 is Q1 -admissible and S2 is Q2 -admissible, then
                             ϕ |= ψ for ϕ ∈ S1 , ψ ∈ S2 is decidable
              implies        g |= f for g ∈ Q1 , f ∈ Q2 is decidable .
Proof. This is a consequence of Theorem 5.                                     ⊓
                                                                               ⊔

6.1   Quantitative Symbolic Heaps
We now demonstrate that our approach can facilitate the automated verification
of probabilistic pointer programs by providing a sample QSL fragment with a
decidable entailment problem.
    Recall that QSL [A] is parameterized by a set A of predicate symbols. We
obtain the quantitative symbolic heap fragment of QSL by instantiating A.
       Foundations for Entailment Checking in Quantitative Separation Logic         23

Definition 4. Let A be the set of predicate symbols given by

      A = { true, emp } ∪ { x 7→ (y1 , . . . , yk ) | x, y1 , . . . , yk ∈ Vars }
           ∪ { x = y, x 6= y, x = y ∧ emp, x 6= y ∧ emp | x, y ∈ Vars } .

Then the set QSH of quantitative symbolic heaps is given by the grammar

  f     →       [ψ] | [π] · f + [¬π] · f | q · f + (1 − q) · f | Sx : f | f ⋆ f .   △

Quantitative symbolic heaps naturally extend the symbolic heap fragment of
separation logic. Intuitively speaking, a quantitative symbolic heap f specifies
probability (sub-)distributions over (symbolic) heaps. By applying Theorem 5,
we obtain the following decidability result.
Theorem 9. For loop- and allocation-free hpGCL programs C (that only per-
form pointer operations, no arithmetic, and guards from the pure fragment of A)
and f1 , f2 ∈ QSH, it is decidable whether the entailment wlpJCK (f1 ) |= f2 holds.
Hence, for loop- and allocation-free programs C as above, upper bounds (in terms
of quantitative symbolic heaps f2 ) on the probability wlpJCK (f1 ) of terminating
in a given quantitative symbolic heap f1 are decidable. We refer to Section 3.3
for an example entailment involving quantitative symbolic heaps. In the sequel,
we show how to prove the above result.


Proof of Theorem 9. The proof relies on extended quantitative symbolic heaps
eQSH, which include magic wands with points-to formulae on their left-hand side.


Definition 5. The set eQSH of extended quantitative symbolic heaps is given
by the grammar

            g    →     [ψ] | [π] · g + [¬π] · g | q · g + (1 − q) · g | g ⋆ g
                        | Sx : g | [x 7→ (y1 , . . . , yk )] −−⋆ g .                △

Notice that indeed QSH ⊆ eQSH.
Lemma 2. For every loop- and allocation-free program C ∈ hpGCL without
arithmetic and only with guards of the pure fragment of A, extended quantitative
symbolic heaps are closed under wlpJCK, i.e.,

                       for all g ∈ eQSH :    wlpJCK (g) ∈ eQSH .

In particular, since QSH ⊆ eQSH, we have

                       for all f ∈ QSH :    wlpJCK (f ) ∈ eQSH .

Proof. By induction on the structure of loop- and allocation-free program C.
See Appendix F for details.
24        Batz et al.

Hence, if g |= f is decidable for g ∈ eQSH and f ∈ QSH, Theorem 9 follows.
Lemma 3. For g ∈ eQSH and f ∈ QSH, it is decidable whether g |= f holds.

Proof. We employ Lemma 1 to determine two SL [A] fragments S1 , S2 such that
S1 is eQSH-admissible and S2 is QSH-admissible. Then, by Theorem 8, decid-
ability of g |= f follows from decidability of ϕ |= ψ for ϕ ∈ S1 and ψ ∈ S2 . For
that, we exploit the equivalence

                        ϕ |= ψ    iff    ϕ ∧ ¬ψ is unsatisfiable .

The latter is decidable by [19, Theorem 3.3] since ϕ ∧ ¬ψ is equivalent to a
formula of the form ∃∗ ∀∗ : ϑ with ϑ quantifier-free and no formula ϑ1 −−⋆ ϑ2
occurring in ϑ contains a universally quantified variable. See Appendix F for
details.


7      Related Work
Weakest preexpectations. Weakest precondition reasoning was established in a
classical setting by Dijkstra [18] and has been extended to provide semantic foun-
dations for probabilistic programs by Kozen [37,36] and McIver & Morgan [40],
who also coined the term weakest preexpectations. Their relation to operational
models is studied in [24]. Moreover, weakest preexpectation reasoning has been
shown to be useful for obtaining bounds on the expected resource consumption
[44] and, in particular, the expected run-time [32] of probabilistic programs.

Logics for probabilistic pointer programs. Although many algorithms rely on
randomized dynamic data structures, formal reasoning about programs that are
both probabilistic and heap manipulating has received scarce attention. A no-
table exception is the work by Tassarotti and Harper [50], who introduce a con-
current separation logic with support for probabilistic reasoning, called Polaris.
Their focus is on program refinement, employing a semantic model that is based
on the idea of coupling, which underlies recent work on probabilistic relational
Hoare logics [4]. However, no other decision procedures targeting entailments for
QSL or other logics targeting probabilistic pointer programs exist.

Leveraging SL research. As shown in Table 7, building QSL entailment checkers
by employing our reduction technique requires the availability of SL fragments
that support certain logical operations, and whose entailment problem is decid-
able. Since the inception of separation logic [28], the latter has been extensively
studied. In particular, the symbolic heap fragment of SL has received a lot of
attention. Table 8 gives an overview of related approaches. 9
9
     ⋆ is always covered. Supported (Boolean or separating) connectives are marked with
     “+”, unsupported ones with “–”. “∗” means that the restrictions on the connec-
     tive are more involved. “Pure” means that the connective can only appear in pure
     formulae and “flat” means that the quantifier needs to be on the outermost level.
        Foundations for Entailment Checking in Quantitative Separation Logic       25

                Table 8. SL fragments with decidable entailment problem.

    Paper        ¬    ∧    ∨ −−⋆ ∃ ∀       Ind. predicates    Complexity
    [1]         pure pure pure – flat –    user defined       ExpTime-hard
    [10] [16]    – pure –      – – –       Lists              Polynomial
    [20]         –    –    –   – + –       user defined       2-ExpTime-complete
    [21]         –    –    +   – + –       user defined       2-ExpTime-complete
    [26]         –    +    –   – flat –    user defined       ?
    [27]         – pure –      – flat –    user defined       ExpTime-complete
    [34]         –    –    –   – + –       user defined       2-ExpTime
    [39]         ∗    +    +   ∗ – –       user defined       2-ExpTime
    [46]         +    +    + + – –         –                  ?
    [17]         +    +    +   – – –       Lists              PSpace-complete
    [19]         +    +    +   ∗ ∗ ∗       –                  PSpace-complete



8     Discussion and Conclusion

We studied entailment checking in QSL by means of a reduction to entailment
checking in SL. We analyzed the complexity of our approach and demonstrated
its applicability by means of several examples. In particular, our reduction yields
the first decidability result for probabilistic pointer program verification.
    Our primary goal was to investigate the entailment problem for QSL to pave
the way for automated verification of probabilistic pointer programs. Theorem 8
provides a generic result that enables building upon the large body of work
dealing with classical SL entailments to obtain both theoretical and practical
insights. Theoretically, Theorem 8 gives sufficient criteria to derive QSL frag-
ments with a decidable entailment problem from a classical SL fragment. We
derived a QSL fragment such that reasoning about a simple probabilistic heap-
manipulating language becomes decidable. More practically, Theorem 8 allows
reusing existing (possibly incomplete) SL solvers to solve the entailments de-
rived by our construction—an empirical evaluation of how well existing solvers
can deal with these entailments is an interesting direction for future work.
    We believe that our fine-grained complexity analysis demonstrates that our
approach can be practically feasible: the exponential blow-up in Theorem 7 stems
from the number of probabilistic constructs in the given QSL formulae. We ex-
pect the number of such constructs to be small for many randomized algorithms.
We remark that existing approaches on checking quantitative entailments be-
tween heap-independent expectations encounter similar exponential blow-ups
(cf., [35,6]). There is thus some evidence that such exponential blow-ups do
not prohibit one from automatically verifying non-trivial properties. We are not
aware of work on checking quantitative entailments between expectations that
avoids such exponential blow-ups.
    Future work includes considering richer classes of QSL and applications of
entailment checking such as k-induction [6]. Another interesting direction is the
applicability of our reduction to other approaches that aim for local reasoning
about the resources employed by probabilistic programs, such as [50,3,5].
26      Batz et al.

References
 1. Antonopoulos, T., Gorogiannis, N., Haase, C., Kanovich, M.I., Ouaknine, J.: Foun-
    dations for decision problems in separation logic with general inductive predicates.
    In: FoSSaCS. Lecture Notes in Computer Science, vol. 8412, pp. 411–425. Springer
    (2014)
 2. Baier, C., Engel, B., Klüppelholz, S., Märcker, S., Tews, H., Völp, M.: A proba-
    bilistic quantitative analysis of probabilistic-write/copy-select. In: NASA Formal
    Methods. LNCS, vol. 7871, pp. 307–321. Springer (2013)
 3. Bao, J., Docherty, S., Hsu, J., Silva, A.: A bunched logic for conditional indepen-
    dence. In: LICS. pp. 1–14. IEEE (2021)
 4. Barthe, G., Grégoire, B., Hsu, J., Strub, P.Y.: Coupling proofs are probabilistic
    product programs. In: POPL. p. 161–174. ACM (2017)
 5. Barthe, G., Hsu, J., Liao, K.: A probabilistic separation logic. Proc. ACM Program.
    Lang. 4(POPL), 55:1–55:30 (2020)
 6. Batz, K., Chen, M., Kaminski, B.L., Katoen, J., Matheja, C., Schröer, P.: Latticed
    k-induction with an application to probabilistic programs. In: CAV (2). Lecture
    Notes in Computer Science, vol. 12760, pp. 524–549. Springer (2021)
 7. Batz, K., Kaminski, B.L., Katoen, J., Matheja, C.: Relatively complete verification
    of probabilistic programs: an expressive language for expectation-based reasoning.
    Proc. ACM Program. Lang. 5(POPL), 1–30 (2021)
 8. Batz, K., Kaminski, B.L., Katoen, J., Matheja, C., Noll, T.: Quantitative separa-
    tion logic: a logic for reasoning about probabilistic pointer programs. Proc. ACM
    Program. Lang. 3(POPL), 34:1–34:29 (2019)
 9. Berdine, J., Calcagno, C., Cook, B., Distefano, D., O’Hearn, P.W., Wies, T., Yang,
    H.: Shape analysis for composite data structures. In: CAV. Lecture Notes in Com-
    puter Science, vol. 4590, pp. 178–192. Springer (2007)
10. Berdine, J., Calcagno, C., O’Hearn, P.W.: A decidable fragment of separation logic.
    In: FSTTCS. Lecture Notes in Computer Science, vol. 3328, pp. 97–109. Springer
    (2004)
11. Berdine, J., Calcagno, C., O’Hearn, P.W.: Smallfoot: Modular automatic assertion
    checking with separation logic. In: FMCO. Lecture Notes in Computer Science,
    vol. 4111, pp. 115–137. Springer (2005)
12. Berdine, J., Calcagno, C., O’Hearn, P.W.: Symbolic execution with separation
    logic. In: APLAS. Lecture Notes in Computer Science, vol. 3780, pp. 52–68.
    Springer (2005)
13. Calcagno, C., Distefano, D., O’Hearn, P.W., Yang, H.: Compositional shape anal-
    ysis by means of bi-abduction. J. ACM 58(6), 26:1–26:66 (2011)
14. Carbin, M., Misailovic, S., Rinard, M.C.: Verifying quantitative reliability for pro-
    grams that execute on unreliable hardware. Commun. ACM 59(8), 83–91 (2016)
15. Chin, W., David, C., Nguyen, H.H., Qin, S.: Automated verification of shape, size
    and bag properties via user-defined predicates in separation logic. Sci. Comput.
    Program. 77(9), 1006–1036 (2012)
16. Cook, B., Haase, C., Ouaknine, J., Parkinson, M.J., Worrell, J.: Tractable reason-
    ing in a fragment of separation logic. In: CONCUR. Lecture Notes in Computer
    Science, vol. 6901, pp. 235–249. Springer (2011)
17. Demri, S., Lozes, É., Mansutti, A.: The effects of adding reachability predicates in
    propositional separation logic. In: Foundations of Software Science and Computa-
    tion Structures. LNCS, vol. 10803, pp. 476–493. Springer (2018)
18. Dijkstra, E.W.: A Discipline of Programming. Prentice-Hall (1976)
      Foundations for Entailment Checking in Quantitative Separation Logic           27

19. Echenim, M., Iosif, R., Peltier, N.: The Bernays-Schönfinkel-Ramsey class of sep-
    aration logic with uninterpreted predicates. ACM Trans. Comput. Log. 21(3),
    19:1–19:46 (2020)
20. Echenim, M., Iosif, R., Peltier, N.: Decidable entailments in separation logic with
    inductive definitions: Beyond establishment. In: CSL. LIPIcs, vol. 183, pp. 20:1–
    20:18. Schloss Dagstuhl - Leibniz-Zentrum für Informatik (2021)
21. Echenim, M., Iosif, R., Peltier, N.: Unifying decidable entailments in separation
    logic with inductive definitions. In: CADE. Lecture Notes in Computer Science,
    vol. 12699, pp. 183–199. Springer (2021)
22. Gordon, A.D., Henzinger, T.A., Nori, A.V., Rajamani, S.K.: Probabilistic pro-
    gramming. In: FOSE. pp. 167–181. ACM (2014)
23. Gotsman, A., Berdine, J., Cook, B., Sagiv, M.: Thread-modular shape analysis.
    In: PLDI. pp. 266–277. ACM (2007)
24. Gretz, F., Katoen, J.P., McIver, A.: Operational versus weakest pre-expectation se-
    mantics for the probabilistic guarded command language. Performance Evaluation
    73, 110–132 (2014)
25. Haslbeck, M.P.L.: Verified Quantitative Analysis of Imperative Algorithms. Ph.D.
    thesis, Technical University of Munich, Germany (2021)
26. Iosif, R., Rogalewicz, A., Simácek, J.: The tree width of separation logic with
    recursive definitions. In: CADE. Lecture Notes in Computer Science, vol. 7898,
    pp. 21–38. Springer (2013)
27. Iosif, R., Rogalewicz, A., Vojnar, T.: Deciding entailments in inductive separation
    logic with tree automata. In: ATVA. Lecture Notes in Computer Science, vol. 8837,
    pp. 201–218. Springer (2014)
28. Ishtiaq, S.S., O’Hearn, P.W.: BI as an assertion language for mutable data struc-
    tures. In: POPL. pp. 14–26. ACM (2001)
29. Iverson, K.E.: A Programming Language. John Wiley & Sons, Inc., USA (1962)
30. Jacobs, B., Smans, J., Philippaerts, P., Vogels, F., Penninckx, W., Piessens, F.:
    Verifast: A powerful, sound, predictable, fast verifier for C and java. In: NASA
    Formal Methods. Lecture Notes in Computer Science, vol. 6617, pp. 41–55. Springer
    (2011)
31. Jung, R., Krebbers, R., Jourdan, J., Bizjak, A., Birkedal, L., Dreyer, D.: Iris from
    the ground up: A modular foundation for higher-order concurrent separation logic.
    J. Funct. Program. 28, e20 (2018)
32. Kaminski, B.L., Katoen, J.P., Matheja, C., Olmedo, F.: Weakest precondition rea-
    soning for expected runtimes of randomized algorithms. J. ACM 65(5) (2018)
33. Kaminski, B.L.: Advanced weakest precondition calculi for probabilistic programs.
    Ph.D. thesis, RWTH Aachen University, Germany (2019)
34. Katelaan, J., Matheja, C., Zuleger, F.: Effective entailment checking for separa-
    tion logic with inductive definitions. In: TACAS (2). Lecture Notes in Computer
    Science, vol. 11428, pp. 319–336. Springer (2019)
35. Katoen, J., McIver, A., Meinicke, L., Morgan, C.C.: Linear-invariant generation
    for probabilistic programs: - automated support for proof-based methods. In: SAS.
    Lecture Notes in Computer Science, vol. 6337, pp. 390–406. Springer (2010)
36. Kozen, D.: Semantics of probabilistic programs. In: FOCS. pp. 101–114. IEEE
    Computer Society (1979)
37. Kozen, D.: A probabilistic PDL. In: STOC. pp. 291–297. ACM (1983)
38. Matheja, C.: Automated reasoning and randomization in separation logic. Ph.D.
    thesis, RWTH Aachen University, Germany (2020)
39. Matheja, C., Pagel, J., Zuleger, F.: Complete entailment checking for separation
    logic with inductive definitions. CoRR abs/2002.01202 (2020)
28      Batz et al.

40. McIver, A., Morgan, C.: Abstraction, Refinement and Proof for Probabilistic Sys-
    tems. Monographs in Computer Science, Springer (2005)
41. Mitzenmacher, M., Upfal, E.: Probability and Computing: Randomized Algorithms
    and Probabilistic Analysis. Cambridge University Press (2005)
42. Morgan, C., McIver, A., Seidel, K.: Probabilistic predicate transformers. ACM
    Trans. Program. Lang. Syst. 18(3), 325–353 (may 1996)
43. Müller, P., Schwerhoff, M., Summers, A.J.: Viper: A verification infrastructure for
    permission-based reasoning. In: Dependable Software Systems Engineering, NATO
    Science for Peace and Security Series - D: Information and Communication Secu-
    rity, vol. 50, pp. 104–125. IOS Press (2017)
44. Ngo, V.C., Carbonneaux, Q., Hoffmann, J.: Bounded expectations: Resource anal-
    ysis for probabilistic programs. SIGPLAN Not. 53(4), 496–512 (2018)
45. Piskac, R., Wies, T., Zufferey, D.: Automating separation logic using SMT. In:
    CAV. Lecture Notes in Computer Science, vol. 8044, pp. 773–789. Springer (2013)
46. Reynolds, A., Iosif, R., Serban, C., King, T.: A decision procedure for separation
    logic in SMT. In: ATVA. Lecture Notes in Computer Science, vol. 9938, pp. 244–
    261 (2016)
47. Reynolds, J.C.: Separation logic: A logic for shared mutable data structures. In:
    LICS. pp. 55–74. IEEE Computer Society (2002)
48. Saheb-Djahromi, N.: Probabilistic lcf. In: Winkowski, J. (ed.) Mathematical Foun-
    dations of Computer Science 1978. pp. 442–451. Springer, Berlin, Heidelberg (1978)
49. Ta, Q., Le, T.C., Khoo, S., Chin, W.: Automated lemma synthesis in symbolic-heap
    separation logic. Proc. ACM Program. Lang. 2(POPL), 9:1–9:29 (2018)
50. Tassarotti, J., Harper, R.: A separation logic for concurrent randomized programs.
    Proc. ACM Program. Lang. 3(POPL), 64:1–64:30 (2019)




Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
    The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
      Foundations for Entailment Checking in Quantitative Separation Logic              29

Appendix

A     Proof of Theorem 1

Theorem 1. The semantics of QSL [A] formulae is well-defined, i.e., for all
f ∈ QSL [A], we have Jf K ∈ E≤1 .

Proof. By induction on f . For the base case f = [ψ], we have J[ψ]K (s, h) ∈ {0, 1}.
For all other cases, it is straightforward to prove that Jf K (s, h) ∈ [0, 1], since [0, 1]
is closed under all operations used in Table 3 if they are defined. It is only left to
proof that JSx : gK, JJ x : gK and Jg ⋆ uK are well-defined. For that the max and
min need to be defined on the given sets, i.e. that the sets
                             
                               JgK (s [x:=v] , h) | v ∈ Vals
                       {JgK (s, h1 ) · JuK (s, h2 ) | h = h1 ⋆ h2 }

are non-empty and finite. Since Vals is non-empty and h = h ⋆ h∅ where h∅ is
the heap with dom (h∅ ) = ∅, both sets are non-empty. Lastly, from Theorem 3
it follows directly, that both sets are also finite.


B     Appendix to Section 3

B.1    Proof of Theorem 2

Theorem 2. Let C ∈ hpGCL be loop-free and A be a set of predicate symbols. If

1. A contains the points-to predicate for all variables and all expressions occur-
   ring in allocation, disposal, lookup and mutation in C,
2. A contains all guards and their negations occurring in C, and
3. all predicates in A are closed under substitution of variables by other variables
   and arithmetic expressions occurring on right-hand sides of assignments in
   C,

then, for every QSL [A] formula f , wlpJCK (f ) ∈ QSL [A].

Proof. First we remark that since A is closed under substitution of variables
by arithmetic expressions occurring on right-hand sides of assignments in C, so
is QSL [A]. For a formula f ∈ QSL [A], substitutions are always only handed
to the atoms in A. Since A is closed under substitution of variables by arith-
metic expressions occurring on right-hand sides of assignments, we have for ev-
ery such expression E on a right-hand side of an assignment and ψ ∈ A that
also ψ [x:=E] ∈ A, where the semantics Jψ [x:=E]K of ψ [x:=E] is defined as

              Jψ [x:=E]K = { (s [x:=E(s)] , h) ∈ ψ | (s, h) ∈ States } .

Now we prove the theorem by induction on C.
30      Batz et al.

For the base case C = skip, we have wlpJskipK (f ) = f ∈ QSL [A] by assump-
tion.
For the base case C = x := E, we have wlpJx := EK (f ) = f [x:=E] ∈ QSL [A]
since QSL [A] is closed under the substitution of x by E.
For the base case C = x := new (E), we have

          wlpJx := new (E)K (f ) = J y : [y 7→ E] −−⋆ f [x:=y] ∈ QSL [A]
because QSL [A] is closed under substitution of x by y and A contains the points-
to formula [y 7→ E] by assumption.
For the base case C = free(E), we have

         wlpJfree(E)K (f ) = [E 7→ − ] ⋆ f = Sx : [E 7→ x] ⋆ f ∈ QSL [A]
because A contains [E 7→ x] by assumption.
For the base case C = x := < E >, we have

     wlpJx := < E >K (f ) = Sx : [E 7→ y] ⋆ ([E 7→ xy] −−⋆ f [x:=y]) ∈ QSL [A]

because QSL [A] is closed under substitution of x by y and A contains the points-
to formulae [E 7→ y] by assumption.
For the base case C = < E > := E ′ , we have

                      wlpJ< E > := E ′ K (f )
                = [E 7→ − ] ⋆ ([E 7→ E ′ ] −−⋆ f )
                = (Sx : [E 7→ x]) ⋆ ([E 7→ E ′ ] −−⋆ f ) ∈ QSL [A]

because A contains the points-to formulae [E 7→ x] and [E 7→ E ′ ] by assumption.
For all other composite cases we assume for some fixed, but arbitrary loop-free
programs C1 , C2 ∈ hpGCL that for all g ∈ QSL [A] we have wlpJC1 K (g) ∈ QSL [A]
and for all u ∈ QSL [A] we have wlpJC2 K (u) ∈ QSL [A].
For the case C = { C1 } [ p ] { C2 }, we have

          wlpJCK (f ) = p · wlpJC1 K (f ) + (1 − p) · wlpJC2 K (f ) ∈ QSL [A]
by the induction hypothesis.
For the case C = C1 ; C2 , we have wlpJC2 K (f ) ∈ QSL [A] by the induction
hypothesis, thus we also have wlpJC1 K (wlpJC2 K (f )) ∈ QSL [A] by the induction
hypothesis.
For the case C = if ( B ) { C1 } else { C2 }, we have
          wlpJCK (f ) = [B] · wlpJC1 K (f ) + [¬B] · wlpJC2 K (f ) ∈ QSL [A]

by the induction hypothesis and since A contains B and ¬B by assumption.
This concludes the proof.
      Foundations for Entailment Checking in Quantitative Separation Logic           31

B.2   Cswap Example

Full Computation

       wlpJCswap K ([x 7→ z1 ] ⋆ [y 7→ z2 ])
=|     wlpJCswap K ([y 7→ z2 ] ⋆ ([x 7→ z1 ] · ([tmp1 = z2 ] · [tmp2 = z1 ])))
                                                                        (monotonicity)
=|     wlpJCswap K ([y 7→ tmp1] ⋆ ([x 7→ tmp2] · ([tmp1 = z2 ] · [tmp2 = z1 ])))
                                                           (variable substitution)
=|     wlpJC1 ; C2 ; C3 K(wlpJC4 K([y 7→ tmp1] ⋆ ([x 7→ tmp2]
                            · ([tmp1 = z2 ] · [tmp2 = z1 ]))))     (wlp application)
=|     wlpJC1 ; C2 ; C3 K ([y 7→ − ] ⋆ ([x 7→ tmp2] · ([tmp1 = z2 ] · [tmp2 = z1 ])))
                                                                           (Rule (ii))
=|     wlpJC1 ; C2 K(wlpJC3 K([y 7→ − ] ⋆ ([x 7→ tmp2]
                          · ([tmp1 = z2 ] · [tmp2 = z1 ]))))        (wlp application)
=|     wlpJC1 ; C2 K(0.999 · wlpJ< x > := tmp2K([y 7→ − ]
                           ⋆ ([x 7→ tmp2] · ([tmp1 = z2 ] · [tmp2 = z1 ])))
                    + 0.001 · wlpJ< x > := errK([y 7→ − ]
                          ⋆ ([x 7→ tmp2] · ([tmp1 = z2 ] · [tmp2 = z1 ]))))
                                                                 (wlp application)
=|     wlpJC1 ; C2 K(0.999 · wlpJ< x > := tmp2K([y 7→ − ]
                           ⋆ ([x 7→ tmp2] · ([tmp1 = z2 ] · [tmp2 = z1 ])))
                    + 0.001 · [false])                                (monotonicity)
=|     wlpJC1 ; C2 K(0.999 · wlpJ< x > := tmp2K([x 7→ tmp2]
                            ⋆ ([y 7→ − ] · ([tmp1 = z2 ] · [tmp2 = z1 ])))
                    + 0.001 · [false])          (commutativity and associativity)
=|     wlpJC1 ; C2 K(0.999 · ([x 7→ − ] ⋆ ([y 7→ − ]
                            · ([tmp1 = z2 ] · [tmp2 = z1 ])))
                     + 0.001 · [false])                                      (Rule (ii))
=|     wlpJC1 K(wlpJC2 K(0.999 · ([x 7→ − ] ⋆ ([y 7→ − ]
                               · ([tmp1 = z2 ] · [tmp2 = z1 ])))
                        + 0.001 · [false])                          (wlp application)
=|     wlpJC1 K(0.999 · wlpJC2 K([x 7→ − ] ⋆ ([y 7→ − ]
                                · ([tmp1 = z2 ] · [tmp2 = z1 ])))
              + 0.001 · wlpJC2 K([false]))                     (super-distributivity)
=|     wlpJC1 K(0.999 · (wlpJC2 K(([y 7→ z1 ] · [tmp2 = z1 ])
                                ⋆ ([tmp1 = z2 ] · [x 7→ − ]))
              + 0.001 · [false])                                      (monotonicity)
32      Batz et al.

 =|     wlpJC1 K (0.999 · ([y 7→ z1 ] ⋆ ([tmp1 = z2 ] · [x 7→ − ])) + 0.001 · [false])
                                                                               (Rule (i))
 =|           0.999 · wlpJC1 K ([y 7→ z1 ] ⋆ ([tmp1 = z2 ] · [x 7→ − ]))
            + 0.001 · wlpJC1 K ([false])                              (super-distributivity)
 =|          0.999 · wlpJC1 K ([y 7→ z1 ] ⋆ ([tmp1 = z2 ] · [x 7→ z2 ]))
            + 0.001 · [false]                                                  (monotonicity)
 =|          0.999 · wlpJC1 K (([x 7→ z2 ] · [tmp1 = z2 ]) ⋆ [y 7→ z1 ])
            + 0.001 · [false]                                                 (commutativity)
 =|           0.999 · ([x 7→ z2 ] ⋆ [y 7→ z1 ]) + 0.001 · [false]                     (Rule (i))



Necessary Separation Logic Entailments

                 ((([x 7→ z2 ] ⋆ [y 7→ z1 ]) ∧ false) ∨ ([x 7→ z2 ] ⋆ [y 7→ z1 ])) ∨ false
       |=        (([x 7→ z2 ] ⋆ [y 7→ z1 ]) ∧ false) ∨ ([x 7→ z2 ] ⋆ [y 7→ z1 ])

                 (([x 7→ z1 ] ⋆ [y 7→ z2 ]) ∧ false) ∨ ([x 7→ z2 ] ⋆ [y 7→ z1 ])
       |=        (([x 7→ z1 ] ⋆ [y 7→ z1 ]) ∧ false) ∨ ([x 7→ z2 ] ⋆ [y 7→ z1 ])

                 ([x 7→ z2 ] ⋆ [y 7→ z1 ]) ∧ false
       |=        ([x 7→ z2 ] ⋆ [y 7→ z1 ]) ∧ false

SMT-LIB 2 File
      (set-logic QF_ALL_SUPPORTED)
      (declare-sort Loc 0)
      (declare-heap (Loc Int))
      (declare-const x Loc)
      (declare-const y Loc)
      (declare-const z1 Int)
      (declare-const z2 Int)
      (assert (or (and (or (or (and (sep (pto x z2) (pto y z1)) false)
      (sep (pto x z2) (pto y z1))) false)
      (not (or (and (sep (pto x z2) (pto y z1)) false)
      (sep (pto x z2) (pto y z1)))))
      (or (and (or (and (sep (pto x z2) (pto y z1)) false)
      (sep (pto x z2) (pto y z1)))
      (not (or (and (sep (pto x z2) (pto y z1)) false)
      (sep (pto x z2) (pto y z1)))))
      (and (and (sep (pto x z2) (pto y z1)) false)
      (not (and (sep (pto x z2) (pto y z1)) false))))))
      (check-sat)
      Foundations for Entailment Checking in Quantitative Separation Logic           33

C    Appendix to Section 4
Lemma 4. For all formulae f ∈ QSL [A] we have 0, 1 ∈ Val [f ].

Proof. By induction on f .
For the base case f = [ψ], we have 0, 1 ∈ {0, 1} = Val [f ].
For all other composite cases we assume for some fixed, but arbitrary g, u ∈
QSL [A] that 0, 1 ∈ Val [g] and 0, 1 ∈ Val [u].
For the induction step f = [π] · g + [¬π] · u, we have by the induction hypothesis
0, 1 ∈ Val [g] ⊆ Val [f ].
For the induction step f = p · g + (1 − p) · u, we have by the induction hypothesis
0, 1 ∈ Val [g] and 0, 1 ∈ Val [u]. Thus we also have 0, p ∈ p · Val [g] and 0, (1 − p) ∈
(1 − p) · Val [u], thus with 0 = 0 + 0 and 1 = p + (1 − p) also 0, 1 ∈ Val [f ].
For the induction step f = g ·u, we have by the induction hypothesis 0, 1 ∈ Val [g]
and 0, 1 ∈ Val [u]. Thus we also have with 0 = 0·0 and 1 = 1·1 that 0, 1 ∈ Val [f ].
For the induction step f = 1 − g, we have by the induction hypothesis 0, 1 ∈
Val [g], thus with 0 = 1 − 1 and 1 = 1 − 0 we also have 0, 1 ∈ Val [f ].
For the induction step f = g max u, we have by the induction hypothesis 0, 1 ∈
Val [g] and 0, 1 ∈ Val [u] thus with 0 = max(0, 0) and 1 = max(1, 1) we also have
0, 1 ∈ Val [f ].
The induction step f = g min u is analogous to the previous case.
For the induction steps f = J x : g, we have by the induction hypothesis 0, 1 ∈
Val [g] = Val [f ].
The induction step f = Sx : g is analogous to the previous case.
The induction step f = g ⋆ u is analogous to the case g · u.
For the induction step f = [ψ] −−⋆ g, we have by the induction hypothesis
0, 1 ∈ Val [g] = Val [f ].
This concludes the proof.



Theorem 4. For every f ∈ QSL [A] and all α ∈ P there is an effectively con-
structible SL [A] formula ⌈α  f ⌉ such that for all (s, h) ∈ States, we have

                  (s, h) |= ⌈α  f ⌉       iff     α ≤ Jf K (s, h) .

Proof. By induction on f .
The case [ψ]. If α = 0 then α ≤ J[ψ]K (s, h) trivially. If 0 < α, then

        α ≤ J[ψ]K (s, h)      iff     J[ψ]K (s, h) = 1     iff    (s, h) |= ψ .
34           Batz et al.

For the composite cases, now assume that for some arbitrary, but fixed formulae
g, u ∈ QSL [A] and all probabilities β, γ ∈ P there are effectively constructible
SL [A] formulae ⌈β  g⌉ and ⌈γ  u⌉ such that for all (s, h) ∈ States,


β ≤ JgK (s, h) iff (s, h) |= ⌈β  g⌉           and      γ ≤ JuK (s, h) iff (s, h) |= ⌈γ  u⌉ .




The case f = [π] · g + [¬π] · u.


             α ≤ J[π] · g + [¬π] · uK (s, h)
 iff         α ≤ [π] (s, h) · JgK (s, h) + [¬π] (s, h) · JuK (s, h)
 iff         (s, h) |= π and α ≤ JgK (s, h) or (s, h) |= ¬π and α ≤ JuK (s, h)
 iff         (s, h) |= π and (s, h) |= ⌈α  g⌉ or (s, h) |= ¬π and (s, h) |= ⌈α  u⌉
                                                                                 (IH)
 iff         (s, h) |= (π ∧ ⌈α  g⌉) ∨ (¬π ∧ ⌈α  u⌉)




The case f = p · g + (1 − p) · u.


                α ≤ Jp · g + (1 − p) · uK (s, h)
       iff      α ≤ p · JgK (s, h) + (1 − p) · JuK (s, h)
       iff      there are β ∈ Val [g] , γ ∈ Val [u] with p · β + (1 − p) · γ ≥ α with
                β ≤ JgK (s, h) and γ ≤ JuK (s, h)                           (monotonicity)
       iff      there are β ∈ Val [g] , γ ∈ Val [u] with p · β + (1 − p) · γ ≥ α with
                (s, h) |= ⌈β  g⌉ and (s, h) |= ⌈γ  u⌉                               (IH)
                                       _
       iff      (s, h) |=                                 ⌈β  g⌉ ∧ ⌈γ  u⌉ .
                           β∈Val[g],γ∈Val[u],p·β+(1−p)·γ≥α
                                                             (Val [g] and Val [u] are finite)




The case f = g · u is analogous to the previous case.
        Foundations for Entailment Checking in Quantitative Separation Logic         35

The case f = 1 − g.

          α ≤ J1 − gK (s, h)
  iff     α ≤ 1 − JgK (s, h)
  iff     0 = α or
          0 < α and α ≤ 1 − JgK (s, h)
  iff     0 = α or
          1 > 1 − α and 1 − α ≥ JgK (s, h)
  iff     0 = α or
          1 > 1 − α and not 1 − α < JgK (s, h)
  iff     0 = α or
          1 > 1 − α and not: there exists δ ∈ Val [g] such that
                     1 − α < δ ≤ JgK (s, h)                       (JgK (s, h) ∈ Val [g])
  iff     0 = α or
          1 > 1 − α and not min { β ∈ Val [g] | β > 1 − α } ≤ JgK (s, h)
                                                                    (†, see below)
  iff     0 = α or
          0 < α and not δ ≤ JgK (s, h) for δ = min { β ∈ Val [g] | β > 1 − α }
  iff     0 = α or
          0 < α and not (s, h) |= ⌈δ  g⌉ for δ = min { β ∈ Val [g] | β > 1 − α }
  iff     0 = α or
          0 < α and (s, h) |= ¬⌈δ  g⌉ for δ = min { β ∈ Val [g] | β > 1 − α }


Regarding †: If there exists a δ ∈ Val [g] with δ ≤ JgK (s, h), then we also have
for all β ≤ δ that β ≤ JgK (s, h) by transitivity. Since furthermore Val [g] is finite,
1 − α < 1 and 1 ∈ Val [g] we can also pick the smallest β ∈ Val [g] satisfying
1 − α < β. For the other direction we have that since Val [g] is finite, 1 ∈ Val [g]
and 1 > 1 − α, the set { β ∈ Val [g] | β > 1 − α } is finite and non-empty. Thus
there also exists an δ such that 1 − α < δ ≤ JgK (s, h).
The case f = g max u.

                            α ≤ Jg max uK (s, h)
                     iff    α ≤ max(JgK (s, h), JuK (s, h))
                     iff    α ≤ JgK (s, h) or α ≤ JuK (s, h)
                     iff    (s, h) |= ⌈α  g⌉ or (s, h) |= ⌈α  u⌉                 (IH)
                     iff    (s, h) |= ⌈α  g⌉ ∨ ⌈α  u⌉


The case f = g min u is analogous to the previous case.
36          Batz et al.

The case f = Sx : g.
                 α ≤ JSx : gK (s, h)
                           
      iff        α ≤ max JgK (s [x:=v] , h) | v ∈ Vals
      iff        there is a v ∈ Vals with α ≤ JgK (s [x:=v] , h)        (Eval (g) is finite)
      iff        there is a v ∈ Vals with (s [x:=v] , h) |= ⌈α  g⌉                    (IH)
      iff        (s, h) |= ∃x : ⌈α  g⌉

The case f = J x : g is analogous to the previous case.
The case f = g ⋆ u.
                 α ≤ Jg ⋆ uK (s, h)
      iff        α ≤ max {JgK (s, h1 ) · JuK (s, h2 ) | h = h1 ⋆ h2 }
      iff        there exists h1 , h2 ∈ Heapsk with h = h1 ⋆ h2 and
                     α ≤ JgK (s, h1 ) · JuK (s, h2 )  (Eval (g) and Eval (u) are finite)
      iff        there exists h1 , h2 ∈ Heapsk with h = h1 ⋆ h2 and
                 there exists β ∈ Val [g], γ ∈ Val [u] with β · γ ≥ α and
                     β ≤ JgK (s, h1 ) and γ ≤ JuK (s, h2 )              (monotonicity)
      iff        there exists β ∈ Val [g], γ ∈ Val [u] with β · γ ≥ α and
                 there exists h1 , h2 ∈ Heapsk with h = h1 ⋆ h2 and
                     β ≤ JgK (s, h1 ) and γ ≤ JuK (s, h2 )
      iff        there exists β ∈ Val [g], γ ∈ Val [u] with β · γ ≥ ra and
                 there exists h1 , h2 ∈ Heapsk with h = h1 ⋆ h2 and
                     (s, h1 ) |= ⌈β  g⌉ and (s, h2 ) |= ⌈γ  u⌉                       (IH)
      iff        there exists β ∈ Val [g], γ ∈ Val [u] with β · γ ≥ α and
                      (s, h) |= ⌈β  g⌉ ⋆ ⌈γ  u⌉
                                    _
      iff        (s, h) |=                     ⌈β  g⌉ ⋆ ⌈γ  u⌉
                          β∈Val[g],γ∈Val[u],β·γ≥α
                                                           (Val [g] and Val [u] are finite)



The case f = [ψ] −−⋆ g.
       α ≤ J[ψ] −−⋆ gK (s, h)
iff    α ≤ inf {JgK (s, h ⋆ h′ ) | h′ ⊥ h and [ψ] (s, h′ ) = 1}
iff    for all h′ ∈ Heapsk with h′ ⊥ h and (s, h′ ) |= ψ we have α ≤ JgK (s, h ⋆ h′ )
                                                                    († see below)
iff    for all h′ ∈ Heapsk with h′ ⊥ h and (s, h′ ) |= ψ we have (s, h ⋆ h′ ) |= ⌈α  g⌉
                                                                                 (IH)
iff    (s, h) |= ψ −−⋆ ⌈α  g⌉
      Foundations for Entailment Checking in Quantitative Separation Logic                            37

      Table 9. Inductive definitions of the size of SL [A] and QSL [A] formulae.


 ϕ          |ϕ|                  f                     |f |                         |f |p
 ψ∈A        |ϕ|                  [ψ]                   |ψ|                          0
                                 [π] · g + [¬π] · u    1 + |π| + |g| + |¬π| + |u|   |g|p + |u|p
 ¬ψ         1 + |ψ|
                                 q · g + (1 − q) · u   1 + |g| + |u|                1 + |g|p + |u|p
 ψ∧ϑ        1 + |ψ| + |ϑ|
                                 g·u                   1 + |g| + |u|                1 + |g|p + |u|p
 ψ∨ϑ        1 + |ψ| + |ϑ|        1−g                   1 + |g|                      |g|p
 ∃x : ψ     1 + |ψ|              g max u               1 + |g| + |u|                |g|p + |u|p
 ∀x : ψ     1 + |ψ|              g min u               1 + |g| + |u|                |g|p + |u|p
 ψ⋆ϑ        1 + |ψ| + |ϑ|        Sx : g                1 + |g|                      |g|p
                                 J x: g                1 + |g|                      |g|p
 ψ −−⋆ ϑ    1 + |ψ| + |ϑ|
                                 g⋆u                   1 + |g| + |u|                1 + |g|p + |u|p
                                 [ψ] −−⋆ g             1 + |g| + |ψ|                |g|p



Regarding † we have the following cases: Either there is no h′ with h′ ⊥ h and
(s, h′ ) |= ψ, then both statements hold for all α ∈ P. If there is at least one
h′ with h′ ⊥ h and (s, h′ ) |= ψ, then since Eval (g) is finite, there is a h′ with
h ⊥ h′ and (s, h′ ) |= ψ that minimizes JgK (s, h ⋆ h′ ) and we let β = JgK (s, h ⋆ h′ ).
Thus α ≤ β if and only if for all h′ with h′ ⊥ h and (s, h′ ) |= ψ we have
α ≤ JgK (s, h ⋆ h′ ).

This concludes the proof.

D     Appendix to Section 5
Theorem 6. We have |Val [f ] | ≤ 2|f |p +1 . Hence, checking f |= g by means of
Theorem 5 requires checking 2O(|f |p) entailments in SL [A].
Proof. We prove this by induction of f .
For the base case for f = [ψ] we have |Val [[ψ]] | = 20+1 = 2|[ψ]|p +1 .
For the composite cases we assume that for some fixed, but arbitrary formulae
g, u ∈ QSL [A], the inequalities |Val [g] | ≤ 2|g|p +1 and |Val [u] | ≤ 2|u|p +1 hold.
For the induction steps f = [π] · g + [¬π] · u, we distinguish three cases.
 1. |g|p = 0. Then by the induction hypothesis, we have |Val [g] | ≤ 2. By
    Lemma 4, we have {0, 1} = Val [g] and 0, 1 ∈ Val [u]. However, then the union
    will not increase the set, i.e. Val [f ] = Val [u]. Finally we have |Val [f ] | =
    |Val [u] | ≤ 2|u|p +1 = 2|f |p +1 by the induction hypothesis.
 2. |u|p = 0 is analogous.
 3. 0 < |g|p , |u|p . Then the size of the set is at most the sum of each set |Val [f ] | ≤
    |Val [g] | + |Val [u] |. By the induction hypothesis we then have
        |Val [f ] | ≤ 2|g|p +1 + 2|u|p +1 ≤ 2 · 2|g|p · 2|u|p = 2|g|p +|u|p +1 = 2|f |p+1 .
                      |                 {z                  }
                               because 0<|g|p ,|u|p
38      Batz et al.

For the induction steps f = q · g + (1 − q) · u, we have that |Val [f ] | ≤ |Val [g] | ·
|Val [u] |. By the induction hypothesis we deduce the upper bound

                Val [f ] ≤ 2|g|p +1 · 2|u|p +1 = 2|g|p +|u|p +1+1 = 2|f |p +1 .

The induction step f = g · u is analogous to the previous case.
For the induction step f = 1 − g, we have that the set does not change in size
|Val [f ] | = |Val [g] | and |f |p = |g|p . Thus this follows directly from the induction
hypothesis.
The induction steps f = g min u and f = g max u are analogous to case f =
[π] · g + [¬π] · u.
The induction steps f = Sx : g and f = J x : g are analogous to the case f =
1 − g.
The induction step f = g ⋆ u is analogous to the case f = g · u.
The induction step f = [ψ] −−⋆ g is analogous to the case f = 1 − g.



Theorem 7. For any formulae f ∈ QSL [A] and all probabilities α ∈ P, the
                                                              2
SL [A] formula ⌈α  f ⌉ has at most size 3 · |f | · 2(|f |p+1) . Hence the size of the
                                        2
formula ⌈α  f ⌉ is in O(|f |) · 2O(|f |p) .
                                                                                       2
Proof. We show by induction on f that |⌈α  f ⌉| ≤ 3 · |f | · 2(|f |p +1) for all
α ∈ P.
                                                                                              2
For the base case f = [ψ] we have |⌈α  f ⌉| ≤ |ψ| = |ψ| · 21 ≤ 3 · |f | · 2(|f |p+1) .
For the composite cases we assume that for some arbitrary, but fixed formulae
g, u ∈ QSL [A] and all probabilities α ∈ P the inequalities for both formulae
                                2                                    2
|⌈α  g⌉| ≤ 3 · |g| · 2(|g|p +1) and |⌈α  u⌉| ≤ 3 · |u| · 2(|u|p +1) hold.
For the induction step f = [π] · g + [¬π] · u we have that

             |⌈α  f ⌉|
        =    |([π] ∧ ⌈α  u⌉) ∨ ([¬π] ∧ ⌈α  u⌉)|
        =    | [π] + 1 + |⌈α  u⌉| + 1 + | [¬π] | + 1 + |⌈α  u⌉||
        =    |π| + |⌈α  g⌉| + |¬π| + |⌈α  u⌉| + 3
                                          2                            2
        ≤    |π| + 3 · |g| · 2(|g|p +1) + |¬π| + 3 · |u| · 2(|u|p +1) + 3                  (IH)
                                              2                                   2
        ≤    |π| + 3 · |g| · 2(|g|p +|u|p +1) + |¬π| + 3 · |u| · 2(|g|p +|u|p +1) + 3
                                                                   2
        ≤    3 · (|π| + |g| + |¬π| + |u| + 1) · 2(|g|p +|u|p +1)
                                                             2
        =    3 · (|π| + |g| + |¬π| + |u| + 1) · 2(|f |p+1)                 (|f |p = |g|p + |u|p )
                            (|f |p +1)2
        =    3 · |f | · 2                                (|f | = |π| + |g| + |¬π| + |u| + 1)
      Foundations for Entailment Checking in Quantitative Separation Logic                            39

For the induction step f = p · g + (1 − p) · u, we have for β, γ ∈ P maximizing
|⌈β  g⌉| and |⌈γ  u⌉| that

         |⌈α  f ⌉| ≤ (|Val [g] | · |Val [u] |) · (|⌈β  g⌉| + |⌈γ  u⌉| + 2) ,

thus using the induction hypothesis and Theorem 6
                                                     2                      2
                                                                                   
 |⌈α  f ⌉| ≤ 2|g|p +1 · 2|u|p +1 · 3 · |g| · 2(|g|p +1) + 3 · |u| · 2(|u|p +1) + 2 .
                                                                     (†)
Remark that 1 ≤ |f |p by assumption. We now prove the upper bound on the
right side by distinguishing two cases on |f |p :

 1. |f |p = 1. Then |g|p = |u|p = 0 and we have:

                       |⌈α  f ⌉|
                 ≤ 2 · 2 · (3 · |g| · 2 + 3 · |u| · 2 + 2)                           ((†) and |f |p = 1)
                 = 23 · 3 · (|g| + |u| + 1/5)
                 ≤ 23 · 3 · |f |                                                   (|f | = |g| + |u| + 1)
                                                        2
                 ≤ 3 · |f | · 2(|f |p +1)                                                     (|f |p = 1)

 2. |f |p > 1. Here we require a bit more mathematical tools in form of Lemma 5.
    Then we have:

            |⌈α  f ⌉|
                                                      2                     2
                                                                                    
        ≤     2|g|p +1 · 2|u|p +1 · 3 · |g| · 2(|g|p +1) + 3 · |u| · 2(|u|p +1) + 2                  (†)
                                           2                      2
                                                                        
        =   2|f |p +1 · 3 · |g| · 2(|g|p +1) + 3 · |u| · 2(|u|p +1) + 2
                                                                                (|f |p = |g|p + |u|p + 1)
                                                        2                            2
        =   3 · |g| · 2|f |p +1 · 2(|g|p +1) + 3 · |u| · 2|f |p +1 · 2(|u|p +1) + 2|f |p +1 · 2
                                                                        2
        ≤      3 · (|g| + |u|) · 2|f |p+1 · 2(|g|p +|u|p +1)
                                                                        2
             + 3 · (|g| + |u|) · 2|f |p +1 · 2(|g|p +|u|p +1)
             + 2 · 2|f |p+1
                                                                        2
        ≤   2 · 3 · (|g| + |u|) · 2|f |p +1 · 2(|g|p +|u|p +1) + 2|f |p+2
                                                                   2
        ≤   2 · 3 · |f | · 2|f |p +1 · 2(|g|p +|u|p +1) + 2|f |p +2                (|f | = |g| + |u| + 1)
                               |f |p +1        |f |2p        |f |p +2
        =   2 · 3 · |f | · 2              ·2            +2                      (|f |p = |g|p + |u|p + 1)
                        |f |2p +|f |p +2
        =   3 · |f | · 2             + 2|f |p +2
                        2                         
        ≤   3 · |f | · 2|f |p+|f |p +2 + 2|f |p +2
                                     2
        ≤   3 · |f | · 2(|f |p +1)                                          (by 1 < |f |p and Lemma 5)

The induction steps for f = g · u is analogous to the previous case.
40     Batz et al.

For the induction step f = 1 − g we have that
                      |⌈α  f ⌉|
                ≤ |⌈α  g⌉| + 1
                                                2
                ≤ 3 · |g| · 2(|g|p +1) + 1                                                           (IH)
                                    (|f |p +1)2          (|f |p +1)2
                ≤ 3 · |g| · 2                       +2                                 (0 ≤ |g|p = |f |p )
                                                            2
                = 3 · (|g| + 1/3) · 2(|f |p +1)
                                                2
                ≤ 3 · |f | · 2(|f |p +1)                                                  (|f | = |g| + 1)

The induction steps for g max u, g min u, Sx : g and J x : g are analogous to the
previous case.
The induction steps for g ⋆ u is analogous to the case f = p · g + (1 − p) · u.
For the induction step [ψ] −−⋆ g we have that
               |⌈α  f ⌉|
           =   |⌈α  g⌉| + |ψ| + 1
                                      2
           ≤   3 · |g| · 2(|g|p +1) + |ψ| + 1                                                        (IH)
                             (|f |p +1)2                          (|f |p +1)2
           ≤   3 · |g| · 2                  + (|ψ| + 1) · 2                            (0 ≤ |g|p = |f |p )
                                                    (|f |p +1)2
           =   3 · (|g| + |ψ|/3 + 1/3) · 2
                                        2
           ≤   3 · |f | · 2(|f |p +1)                                               (|f | = |g| + |ψ| + 1)

This concludes the proof.
                                                                                2                      2
Lemma 5. For all natural numbers n > 1, we have 2n +n+2 + 2n+2 ≤ 2(n+1) .
Proof. By induction over n.
                                   2                                        2
For the base case n = 2, we have 22 +2+2 + 22+2 = 28 + 24 < 28 + 28 = 2(2+1) .
Now we assume that for some fixed, but arbitrary natural number n > 1 the
             2                     2
inequality 2n +n+2 + 2n+2 ≤ 2(n+1) holds.
For the induction step n → n + 1, we have
                                                2
                                     2(n+1) +n+1+2 + 2n+1+2
                                            2
                               = 2n +2n+1+n+1+2 + 2n+1+2
                                            2
                               = 2n +n+2 · 22n+2 + 2n+2 · 2
                                         2              
                               ≤ 22n+2 · 2n +n+2 + 2n+2
                                                            2
                               ≤ 22n+2 · 2(n+1)                                                      (IH)
                                        n2 +4n+3
                               = 2
                                            2
                               ≤ 2n +4n+4
                                                    2
                               = 2(n+1+1) .
      Foundations for Entailment Checking in Quantitative Separation Logic      41

This concludes the proof.


E    Appendix to Section 6
Lemma 1. Let Q be a QSL [A] fragment. If an SL [A] fragment S satisfies the
requirements provided in Table 7, then S is Q-admissible.

Proof. By induction on f .
For the base case f = [ψ], we have ⌈α  [ψ]⌉ = true if α = 0 otherwise [ψ], thus
true and ψ are required.
For all other composite cases we assume for some fixed, but arbitrary g, u ∈
QSL [A] that for all β, γ ∈ P the formulae ⌈β  g⌉ and ⌈γ  u⌉ satisfy the
requirements.
For the case f = [π]·g+[¬π]·u, we have ⌈α  f ⌉ = (π∧⌈α  g⌉)∨(¬π∧⌈α  u⌉),
since by the induction hypothesis ⌈α  g⌉ and ⌈α  u⌉ already satisfy all
requirements, we only require additionally π, ¬π, ∧ and ∨.
For the case f = p · g + (1 − p) · u, we have
                                   _
          ⌈α  f ⌉ =                                   ⌈β  g⌉ ∧ ⌈γ  u⌉ .
                     β∈Val[g],γ∈Val[u],p·β+(1−p)·γ≥α

Here we have two observations:
1. There are only finitely many disjunctions since Val [g] and Val [u] is finite by
   Theorem 3.
2. The disjunctions is not empty since 1 ∈ Val [g] and 1 ∈ Val [u] by Lemma 4
   and p · 1 + (1 − p) · 1 = 1 ≥ α for all α ∈ P.
Thus, for any α ∈ P, we can construct the big disjunction by only using ∧, ∨,
⌈β  g⌉ and ⌈γ  u⌉ for all β, γ ∈ P. Since ⌈β  g⌉ and ⌈γ  u⌉ satisfy all
requirements by the induction hypothesis, we only require additionally ∧ and ∨.
The case f = g · u is analogous to the previous case.
For the case f = 1 − g, we have ⌈α  f ⌉ = true if α = 0 otherwise ¬⌈δ  g⌉
where δ = min { β ∈ Val [g] | β > 1 − α }. Remark that we compute δ during the
construction of ⌈α  f ⌉ and not during the checking of (s, h) |= ⌈α  f ⌉. Since
⌈δ  g⌉ already satisfy all requirements by the induction hypothesis, we thus
only additionally require ¬ and true.
The cases f = g max u, f = g min u, f = Sx : g and f = J x : g are analogous to
the case f = [π] · g + [¬π] · u.
The case f = g ⋆ u is analogous to the case f = p · g + (1 − p) · u.
The case f = [ψ] −−⋆ g is analogous to the case f = [π] · g + [¬π] · u.
This concludes the proof.
42      Batz et al.

F     Appendix to Section 6.1
Theorem 9. For loop- and allocation-free hpGCL programs C (that only per-
form pointer operations, no arithmetic and guards of the pure fragment of A)
and f1 , f2 ∈ QSH, it is decidable whether the entailment wlpJCK (f1 ) |= f2 holds.

Proof of Theorem 9 The proof requires extended quantitative symbolic heaps:


Definition 5. The set eQSH of extended quantitative symbolic heaps is given
by the grammar

          g   →       [Φ] | [B] · g + [¬B] · g | q · g + (1 − q) · g | g ⋆ g
                       | Sx : g | [x 7→ (y1 , . . . , yk )] −−⋆ g .             △

     Notice that indeed QSH ⊆ eQSH.
Lemma 2. For every loop- and allocation-free program C ∈ hpGCL without
arithmetic and only with guards of the pure fragment of A, extended quantitative
symbolic heaps are closed under wlpJCK, i.e.,

                      for all g ∈ eQSH :    wlpJCK (g) ∈ eQSH .

In particular, since QSH ⊆ eQSH, we have

                       for all f ∈ QSH :   wlpJCK (f ) ∈ eQSH .

Proof. Since we not allow arithmetic in expressions, we only have expressions
of the form E = y. Moreover, eQSH is trivially closed under the substitution
g [x:=y] for any x, y ∈ Vars. Now we prove the lemma by induction on the
structure of loop- and allocation-free program C with k = 1, however the proof
is easy to adapt for any k.
For the base case C = skip we have wlpJskipK (g) = g ∈ eQSH.
For the base case C = x := y we have

                       wlpJx := yK (g) = g [x:=y] ∈ eQSH .

For the base case C = free(y) we have

                    wlpJfree(y)K (g) = Sz : [y 7→ z] ⋆ g ∈ eQSH

where z is fresh.
For the base case C = x := < y > we have

      wlpJx := < y >K (g) = Sz : [x 7→ z] ⋆ ([x 7→ y] −−⋆ f [x:=y]) ∈ eQSH

where z is fresh.
      Foundations for Entailment Checking in Quantitative Separation Logic      43

For the base case C = < x > := y we have
        wlpJ< x > := yK (g) = Sz : [x 7→ z] ⋆ ([x 7→ y] −−⋆ f ) ∈ eQSH
where z is fresh.
For all other composite cases we assume for some fixed, but arbitrary loop-
and allocation-free programs C1 , C2 ∈ hpGCL without arithmetic and only with
guards of the pure fragment of A such that for all g ∈ eQSH : wlpJC1 K (g) ∈
eQSH and for all u ∈ eQSH : wlpJC2 K (u) ∈ eQSH.
For the case C = { C1 } [ p ] { C2 } we have
 wlpJ{ C1 } [ p ] { C2 }K (g) = p · wlpJC1 K (g) + (1 − p) · wlpJC2 K (g) ∈ eQSH
by the induction hypothesis.
For the case C = C1 ; C2 we have
              wlpJC1 ; C2 K (g) = wlpJC1 K (wlpJC2 K (g)) ∈ eQSH
by the induction hypothesis.
For the case C = if ( B ) { C1 } else { C2 } we have either B = (x = y), then
         wlpJif ( x = y ) { C1 } else { C2 }K (g)
                    = [x = y] · wlpJC1 K (g) + [x 6= y] · wlpJC2 K (g) ∈ eQSH
by the induction hypothesis; or B = (x 6= y) which is analogous.
This concludes the proof.
Hence, if g |= f is decidable for g ∈ eQSH and f ∈ QSH, Theorem 9 follows.
Lemma 3. For g ∈ eQSH and f ∈ QSH, it is decidable whether g |= f holds.
Proof. We employ Lemma 1 to determine two SL [A] fragments S1 , S2 such that
S1 is eQSH-admissible and S2 is QSH-admissible. Then, by Theorem 8, decid-
ability of g |= f follows from decidability of ϕ |= ψ for ϕ ∈ S1 and ψ ∈ S2 . For
that, we exploit the equivalence
                    ϕ |= ψ     iff     ϕ ∧ ¬ψ is unsatisfiable .
The latter is decidable by [19, Theorem 3.3] since ϕ∧¬ψ is equivalent to a formula
of the form ∃∗ ∀∗ : ϑ with ϑ quantifier-free and such that no formula ϑ1 −−⋆ ϑ2
occurring in ϑ contains a universally quantified variable. The eQSH-admissible
SL [A] fragment S1 is given by
                      ϕ      → Φ
                                 | ϕ∧ϕ
                                 | ϕ∨ϕ
                                 | ∃x : ϕ
                                 | ϕ⋆ϕ
                                 | x 7→ (y1 , . . . , yk ) −−⋆ ϕ .
44       Batz et al.

The QSH-admissible SL [A] fragment S2 is given by

                                       ψ     → Φ
                                                    | ψ∧ψ
                                                    | ψ∨ψ
                                                    | ∃x : ψ
                                                    | ψ⋆ψ .




Lemma 6. Every ϕ ∈ S1 is equivalent to a formula ψ = ∃x1 , . . . , xn : ϑ for
some n ∈ N with ϑ ∈ S1 quantifier-free.

Proof. By induction on ϕ. For the base case ϕ = Φ we choose n = 0 and have
nothing to show. The cases ∧, ∨, ∃ are standard. For the remaining cases, we
reason as follows: As the induction hypothesis assume that for some arbitrary,
but fixed, ϕ1 , ϕ2 ∈ S1 there are ψ1 = ∃x1 , . . . , xn : ϑ1 and ψ2 = ∃y1 , . . . , ym : ϑ2
with ϑ1 , ϑ2 ∈ S1 quantifier-free and ψ1 ≡ ϕ1 and ψ2 ≡ ϕ2 . Furthermore, assume
without loss of generality that x1 , . . . , xn do not occur in ϑ2 and that y1 , . . . , ym
do not occur in ϑ1 .

The case ϕ = ϕ1 ⋆ ϕ2 . For every (s, h) ∈ States, we have

    (s, h) |= ϕ1 ⋆ ϕ2
iff there are h1 , h2 with h1 ⋆ h2 = h such that
    (s, h1 ) |= ϕ1 and (s, h2 ) |= ϕ2
iff there are h1 , h2 with h1 ⋆ h2 = h such that
     there are v1 , . . . , vn , w1 , . . . , wm such that
     (s [x1 :=v1 ] . . . [xn :=vn ] , h1 ) |= ϑ1 and (s [y1 :=w1 ] . . . [ym :=wm ] , h2 ) |= ϑ2
                                                                                       (by I.H.)
iff there are v1 , . . . , vn , w1 , . . . , wm such that
    there are h1 , h2 with h1 ⋆ h2 = h such that
     (s [x1 :=v1 ] . . . [xn :=vn ] , h1 ) |= ϑ1 and (s [y1 :=w1 ] . . . [ym :=wm ] , h2 ) |= ϑ2
iff there are v1 , . . . , vn , w1 , . . . , wm such that
    (s [x1 :=v1 ] . . . [xn :=vn ] [y1 :=w1 ] . . . [ym :=wm ] , h) |= ϑ1 ⋆ ϑ2
                                                                    (variables do not overlap)
iff (s, h) |= ∃v1 , . . . , wn , w1 , . . . , wm : ϑ1 ⋆ ϑ2 .

The case ϕ = x 7→ (z1 , . . . , zk ) −−⋆ ϕ1 . We assume without loss of generality
that x 6∈ {x1 , . . . , xn } and {x1 , . . . , xn } ∩ {z1 . . . zk } = ∅. Let (s, h) ∈ States. We
distinguish the cases s(x) ∈ dom (h) and s(x) 6∈ dom (h). If s(x) ∈ dom (h), we
       Foundations for Entailment Checking in Quantitative Separation Logic                   45

have

                       (s, h) |= x 7→ (z1 , . . . , zk ) −−⋆ ϕ1
                 iff   true
                 iff   (s, h) |= ∃x1 , . . . , xn : x 7→ (z1 , . . . , zk ) −−⋆ ϑ1 .
                                                                       (variables do not overlap)

If s(x) 6∈ dom (h), we have

              (s, h) |= x 7→ (z1 , . . . , zk ) −−⋆ ϕ1
         iff (s, h ⋆ s(x) 7→ (s(z1 ), . . . , s(zk ))) |= ϕ1
         iff (s, h ⋆ s(x) 7→ (s(z1 ), . . . , s(zk ))) |= ∃x1 , . . . , xn : ϑ1       (by I.H.)
         iff there are v1 , . . . , vn such that
             (s [x1 :=v1 ] . . . [xn :=vn ] , h ⋆ s(x) 7→ (s(z1 ), . . . , s(zk ))) |= ϑ1
                                                                    (variables do not overlap)
         iff there are v1 , . . . , vn such that
             (s [x1 :=v1 ] . . . [xn :=vn ] , h) |= x 7→ (z1 , . . . , zk ) −−⋆ ϑ1
                                                                    (variables do not overlap)
         iff (s, h) |= ∃x1 , . . . , xn : x 7→ (z1 , . . . , zk ) −−⋆ ϑ1 .

This completes the proof.

Lemma 7. Every ϕ ∈ S2 is equivalent to a formula ψ = ∃x1 , . . . , xn : ϑ for
some n ∈ N with ϑ ∈ S2 quantifier-free.

Proof. Analogous to the proof of Lemma 6.

Now let ϕ ∈ eQSH and ψ ∈ QSH. By Lemma 6 and Lemma 7 there are ϕ′ =
∃x1 , . . . , xn : ϑ1 and ψ ′ = ∃y1 , . . . , ym : ϑ2 with ϑ1 ∈ S1 ,ϑ2 ∈ S2 quantifier-free
and ϕ ≡ ϕ′ and ψ ≡ ψ ′ . Notice that ϑ2 does not contain −−⋆ . We may without
loss of generality assume that x1 , . . . , xn do not occur in ϑ2 and that y1 , . . . , ym
do not occur in ϑ1 . Hence, we get

       ϕ |= ψ
 iff   ϕ ∧ ¬ψ is unsatisfiable
 iff   ∃x1 , . . . , xn : ϑ1 ∧ ¬(∃y1 , . . . , ym : ϑ2 ) is unsatisfiable (by above reasoning)
 iff   (∃x1 , . . . , xn : ϑ1 ) ∧ (∀y1 , . . . , ym : ¬ϑ2 ) is unsatisfiable
 iff   ∃x1 , . . . , xn : ∀y1 , . . . , ym : ϑ1 ∧ ¬ϑ2 is unsatisfiable , (standard prenexing)

since ϑ1 ∧ ¬ϑ2 is quantifier free and since none of y1 , . . . , ym occur in an instance
of −−⋆ occurring in ϑ1 ∧ ¬ϑ2 , the claim follows.
