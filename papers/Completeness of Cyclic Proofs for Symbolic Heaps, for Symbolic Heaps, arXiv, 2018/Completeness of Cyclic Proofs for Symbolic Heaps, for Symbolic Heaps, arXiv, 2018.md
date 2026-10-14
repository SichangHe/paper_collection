                                                                       Completeness of Cyclic Proofs
                                                                           for Symbolic Heaps
                                                 Makoto Tatsuta                       Koji Nakazawa                          Daisuke Kimura
                                             National Institute of In-            Nagoya University, Japan                Toho University, Japan
arXiv:1804.03938v2 [cs.LO] 28 May 2018




                                             formatics / Sokendai,                 knak@i.nagoya-u.ac.jp                  kmr@is.sci.toho-u.ac.jp
                                             Japan
                                                 tatsuta@nii.ac.jp


                                                                                            Abstract
                                                  Separation logic is successful for software verification in both theory and practice. Decision pro-
                                               cedure for symbolic heaps is one of the key issues. This paper proposes a cyclic proof system for
                                               symbolic heaps with general form of inductive definitions, and shows its soundness and completeness.
                                               The decision procedure for entailments of symbolic heaps with inductive definitions is also given.
                                               Decidability for entailments of symbolic heaps with inductive definitions is an important question.
                                               Completeness of cyclic proof systems is also an important question. The results of this paper answer
                                               both questions. The decision procedure is feasible since it is nondeterministic double-exponential
                                               time complexity.


                                         1     Introduction
                                         Separation logic is successful for software verification [22, 4, 5]. Several systems based on this idea have
                                         been actively investigated and implemented. One of the keys in these systems is the entailment checker
                                         that decides the validity for a given entailment of symbolic heaps.
                                             The paper [17] proposed the system SLRDbtw , which is the first decidable system for entailment of
                                         symbolic heaps with general form of inductive definitions. We call the conditions imposed in [17] for
                                         restricting the class of inductive definitions by a bounded treewidth condition. The inductive definitions
                                         without any restriction cause undecidability [1]. The bounded treewidth condition is one of the most
                                         flexible conditions for a decidable system.
                                             A cyclic proof system [7] can give us efficient implementation of theorem provers. On the other hand,
                                         the completeness and the decidability of provability are not known for any cyclic proof system. Hence
                                         it is a challenging problem to find some complete cyclic proof system and some decidable system for
                                         symbolic heaps with general form of inductive definitions.
                                             Our contribution is to solve these problems, namely, to propose a cyclic proof system CSLIDω for
                                         symbolic heaps with inductive definitions, to prove its soundness theorem and its completeness theorem,
                                         and to give its decision procedure.
                                             Our first ideas are as follows: (1) We define inductive definition clauses so that the unfolding de-
                                         termines the root cells of children. (2) We use unfold-match and split, namely, first unfold inductive
                                         predicates on both sides (antecedent and succedent), next remove the same x 7→ ( ) on both sides, then
                                         split the entailment by separating conjunction. (3) We do proof-search by going up from the conclusion to
                                         the assumption in an inference rule. We will show the termination by defining normal forms and showing
                                         the set of those possibly used during computation is finite. This shows the termination since (a) every
                                         path of potentially infinite length contains infinite number of normal forms, (b) the set of normal forms is
                                         finite, (c) hence there is some repetition of normal forms in the path, (d) hence in the path some subgoal
                                         of the repetition is eventually discharged by cyclic proof mechanism. (4) We also show (selective) local
                                         completeness of each application of rules used in each step. By this and termination, we will show the
                                         completeness.
                                             Our main ideas are as follows. Each of them is new. All of these techniques together make an
                                         algorithm based on those first ideas a real algorithm. (1) We will introduce atomic formulas t ↓ and t ↑


                                                                                                 1
which mean t is in the heap and t is not in the heap respectively, and put ↓ or ↑ for each variable in
both antecedent and succedent. (2) When we unfold the succedent, to keep validity, we need disjunction
in the succedent. So we will introduce disjunction in the succedent. (3) We will propose a new (∗)-split
rule for disjunction. As far as we know, no (∗)-split rule has not been proposed for disjunction. (4) We
will introduce a factor rule. Roughly speaking, if the candidate of a common root is x but it does not
appear in some disjunct P (y), we transform this disjunct into (Q(x)—∗P (y)) ∗ Q(x) so that the disjunct
has the root x. (5) For splitting existential scopes, we transform ∃w((P (x, w) ∧ w ↓) ∗ Q(y, w)) into
∃w((P (x, w) ∧ w ↓) ∗ (Q(y, w) ∧ w ⇑)) and it into ∃w((P (x, w) ∧ w ↓)) ∗ ∃w((Q(y, w) ∧ w ⇑)). We will
show these transformations keep equivalence. (6) We eliminate a disjunct that is a renaming of another
disjunct, and moreover we will show that this elimination keeps validity.
    For unfold-match and removing 7→, we need some conditions (strong connectivity, decisiveness) to the
class of inductive definitions besides the bounded treewidth condition. The establishment condition in the
bounded treewidth condition is checked by considering the set of inductive definitions, and it is not locally
checked by the shape of each definition clause. Our condition is a local version of the bounded treewidth
condition. These additional conditions are not so restrictive and our class of inductive definitions is still
quite large, since our class contains doubly-linked lists, skip lists, and nested lists.
    The decision procedure is feasible since it is double-exponential time complexity.
    Several entailment checkers for symbolic heaps with inductive definitions have been discussed. Most
of them do not have general form of inductive definitions and have only hard-coded inductive predicates
[19, 20, 21, 4, 5, 14, 15, 16]. The entailment checkers for general form of inductive definitions are studied
in [12, 13, 17, 18, 24, 8, 9]. The engines of the system SLRDbtw [17, 18] and the system in [24] are both
model theoretic, and they are decidable systems. The systems in [13, 8, 9] use cyclic proofs, but neither
of them is a complete system. [12] is based on ordinary sequent calculus and is not complete.
    The cyclic proofs have been intensively investigated for the first-order predicate logic [7, 9, 2, 23, 3],
a bunched implication system [6], and a symbolic heap system [8, 9].
    Section 2 defines separation logic with inductive definitions. In Section 3, we extend our language,
in particular, we give definition clauses for the strong wand. Section 4 defines the system CSLIDω .
Section 5 shows soundness of the factor rule. Section 6 proves soundness of the existential amalgamation
rules. Section 7 proves soundness of the (∗)-split rule. Section 8 proves the soundness of the system.
Section 9 gives a satisfiability checker. In Section 10, we define normal forms and groups, give the decision
algorithm of validity, and shows its partial correctness, loop invariants and termination. Section 11 proves
a property for constant store validity. Section 12 explains cones. Section 13 proves local completeness
of the factor rule. Section 14 shows local completeness of the unrelated introduction. Section 15 shows
selective local completeness of the rule (∗)-split. Section 16 shows properties for elimination of fresh
variables in the succedent. Section 17 proves completeness of CSLIDω . We conclude in Section 18.


2     Symbolic Heaps with Inductive Definitions
This section defines symbolic heaps, inductive definitions, and their semantics.
    We will use vector notation −
                                →x to denote a sequence x1 , . . . , xk for simplicity. |−
                                                                                         →
                                                                                         x | denotes the length
of the sequence. Sometimes we will also use a notation of a sequence to denote a set for simplicity. We
write ≡ for the syntactical equivalence.

2.1    Language
Our language is a first order logic with a new connective ∗ and inductive predicates, and defined as
follows.
    First-order variables Vars ::= x, y, z, w, v, . . ..        Terms t, u, p, q, r ::= x | nil.
    Inductive Predicate Symbols P, Q, R.
    We define formulas F, G of separation logic as those of the first-order language generated by the
constant nil, the propositional constant emp, predicate symbols =, 7→, P ,Q,. . ., and an additional logical
connective ∗. We write t 6= u for ¬t = u. We assume some number ncell for the number of elements in a
cell.
    Pure formulas Π ::= t = t | t 6= t | Π ∧ Π.
                                                                  →
                                                                  −
    Spatial formulas Σ ::= emp | t 7→ (t1 , . . . , tncell ) | P ( t ) | Σ ∗ Σ.


                                                      2
                                                                                                   →
                                                                                                   −
    We suppose ∗ binds more tightly than ∧. We will sometimes write P (t) for P (t, t ). We write
∗i∈[1,n] Pi (xi ) for P1 (x1 ) ∗ . . . ∗ Pn (xn ). Similarly we write ∗i∈I Pi (xi ). We write Π ⊆ Π′ when all the
conjuncts of Π are contained in those of Π′ .
    qf-Symbolic Heaps A, B ::= Π ∧ Σ | Σ.                  Symbolic Heaps φ ::= ∃−  →x A.
    Entailments A ⊢ B1 , . . . , Bn .             _
    Inductive Definitions P (x, −      →y ) =def    φi (x, −
                                                           →
                                                           y ) where φi is a definition clause.
                                                i
                                                                  →
                                                                  −
   Definition Clauses φ(x, −
                           →
                           y ) ≡ ∃−
                                  →
                                  z (Π ∧ x 7→ (−
                                               →
                                               u ) ∗ ∗i∈I Pi (zi , t i )), where
   • {zi | i ∈ I} = −
                    →z (strong connectivity),
   • −
     →
     z ⊆−  →u (decisiveness).
    We call the first argument of a spatial atomic formula except emp a root.
    The strong connectivity implies the bounded treewidth condition. The decisive condition is that in
every definition clause, all existential variables must occur in −    →u where the definition clause has x 7→ (−
                                                                                                               →
                                                                                                               u ).
It is similar to the constructively valued condition in [11]. This condition guarantees that the cell at
address x decides the content of every existential variable.
    We give some examples of the inductive definitions in the following.
    The list segment is definable: ls(x, y) =def x 7→ y ∨ ∃z(x 7→ (z) ∗ ls(z, y)).
    The doubly-linked list is definable:
    dll(h, p, n, t) =def h = t ∧ h 7→ (p, n) ∨ ∃z(h 7→ (p, z) ∗ dll(z, h, n, t)).
    The nested list is definable:
    listnest(x) =def ∃z.x 7→ (z, nil) ∗ ls(z, nil) ∨ ∃z1 z2 (x 7→ (z1 , z2 ) ∗ ls(z1 , nil) ∗ listnest(z2 )).
    The following nested list segment is also definable.
    lsnest(x, y) =def ∃z(x 7→ (z, nil) ∗ ls(z, y)) ∨ ∃z1 z2 (x 7→ (z1 , z2 ) ∗ ls(z1 , y) ∗ lsnest(z2 , y)).
    The skip list is definable:
    skl1(x, y) =def x 7→ (nil, y) ∨ ∃z(x 7→ (nil, z) ∗ skl1(z, y)),
    skl2(x, y) =def ∃z(x 7→ (y, z) ∗ skl1(z, y)) ∨ ∃z1 z2 (x 7→ (z1 , z2 ) ∗ skl1(z2 , z1 ) ∗ skl2(z1 , y)).
    The examples in [8] are definable in our system as follows: List, ListE, ListO are definable, RList is
not definable. DLL, PeList, SLL, BSLL, BinTree, BinTreeSeg, BinListFirst, BinListSecond, BinPath are
not definable but will be definable in a straightforward extension of our system by handling emp in the
base cases.
    We prepare some notions. We define P (m) by
       P (0) (−
              →
              x ) ≡ (nil_
                        6= nil),
         (m+1) − →
       P        (x)≡      φi [P := P (m) ],
                         i
                    _
where P (−
         →
         x ) =def        φi . P (m) is m-time unfold of P . We define F (m) as obtained from a formula F by
                     i
                                    P by P (m) .
replacing every inductive predicate ^
   We define (6= (T1 , T2 )) as              t1 6= t2 . We write x 6= T for (6= ({x}, T )).
                                t1 ∈T1 ,t2 ∈T2 ,t1 6≡t2
   We define (6= (T )) as (6= (T ∪ {nil}, T ∪ {nil})).

2.2    Semantics
This subsection gives semantics of the language.
    We define the following structure: Val = N , Locs = {x ∈ N |x > 0}, Heaps = Locs →f in Valncell ,
Stores = Vars → Val. Each s ∈ Stores is called a store. Each h ∈ Heaps is called a heap, and Dom(h) is
the domain of h, and Range(h) is the range of h. We write h = h1 + h2 when Dom(h1 ) and Dom(h2 ) are
disjoint and the graph of h is the union of those of h1 and h2 . A pair (s, h) is called a heap model, which
means a memory state. The value s(x) means the value of the variable x in the model (s, h). Each value
a ∈ Dom(h) means an address, and the value of h(a) is the content of the memory cell at address a in
the heap h. We suppose each memory cell has ncell elements as its content.
    The interpretation s(t) for any term t is defined as 0 for nil and s(x) for the variable x.
    For a formula F we define the interpretation s, h |= F as follows.


                                                          3
    s, h |= t1 = t2 if s(t1 ) = s(t2 ),
    s, h |= F1 ∧ F2 if s, h |= F1 and s, h |= F2 ,
    s, h |= F1 ∨ F2 if s, h |= F1 or s, h |= F2 ,
    s, h |= ¬F if s, h 6|= F .
    s, h |= emp if Dom(h) = ∅,
    s, h |= t 7→ (t1 , . . . , tncell ) if Dom(h) = {s(t)} and h(s(t)) = (s(t1 ), . . . , s(tncell )),
    s, h |= F1 ∗ F2 if s, h1 |= F1 and s, h2 |= F2 for some h1 + h2 = h,
                 →
                 −                         →
                                           −
    s, h |= P ( t ) if s, h |= P (m) ( t ) for some m,
    s, h |= ∃zF if s[z := b], h |= F for some b ∈ Val.
    We write A |= B1 , . . . , Bn for ∀sh(s, h |= A → ((s, h |= B1 ) ∨ . . . ∨ (s, h |= Bn ))). The entailment
A ⊢ B1 , . . . , Bn is said to be valid if A |= B1 , . . . , Bn holds. Our goal in this paper is to decide the validity
of a given entailment.
    For saving space, we identify some syntactical objects that have the same meaning, namely, we use
implicit transformation of formulas by using the following properties: ∧ is commutative, associative, and
idempotent; ∗ is commutative, associative, and has the unit emp; = is symmetric; Π∧(F ∗G) ↔ (Π∧F )∗G;
∃xG ↔ G, ∃x(F ∧ G) ↔ ∃xF ∧ G, and ∃x(F ∗ G) ↔ ∃xF ∗ G, when F, G are formulas and x ∈                        / FV(G);
∃xyF ↔ ∃yxF . We also identify the succedent of an entailment with a set of disjuncts instead of a
sequence of disjuncts.


3     Language Extension
3.1     Extended Language
In this section, we extend our language from symbolic heaps by ↓ and L and —∗s , which is necessary to
show the completeness.
    We extend inductive predicate symbols with Q1 —∗s . . . —∗s Qm —∗s P where Q1 , . . . , Qm , P
are original inductive predicate symbols.                 We call m the depth of wands.                      We write
    →
    −                        →
                             −           →
                                         −                                       → −
                                                                                 −  →            →
                                                                                                 −
Q1 ( t 1 )—∗s . . . —∗s Qm ( t m )—∗s P ( t ) for (Q1 —∗s . . . —∗s Qm —∗s P )( t , t 1 , . . . , t m ). For a sequence
R~ = R1 , · · · , Rn of predicates, we write R—∗P
                                             ~         for R1 —∗ · · · —∗Rn —∗P .
    We extend our first-order language with the extended inductive predicate symbols and unary predicate
symbols ↓ and L. t ↓ means that t is in Dom(h) and L(t) means that t is in Range(h) − Dom(h) (the
leaves of h). We write t ↑ for ¬t ↓. We write t ⇑ for t ↑ ∧¬Lt.
    We write Σ, A, B, φ for the same syntactical objects with ^        the extended inductive predicate symbols.
    We use X, Y for a finite set of variables and write X ↑ for {t ↑ | t ∈ X}. X ↓ and X ⇑ are similarly
defined. We write ∃−     →
                         x ↓ for ∃−→
                                   x (−
                                      →
                                      x ↓ ∧ . . .). Similarly we write ∃− →x ⇑.
    We define:
    P ::= 7→ | P where P varies in inductive predicate symbols,
                 →
                 −
    ∆ ::= P( t ) ∧ X ↓, and Γ ::= ∆ | Γ ∗ Γ, and ψ ::= Y ↑ ∧Π ∧ Γ, and Φ ::= ∃−           →x ∃−  →
                                                                                                 y ⇑ (Π ∧ Γ),
    F, G a separation logic formula with ↓, L.
    We define entailments as ψ ⊢ Φ1 , . . . , Φn .
    We write J for an entailment. In ψ, Φ, we call Γ a spatial part and Π a pure part.
                                                       →
                                                       −
    We define Roots(X ⇑ ∧Y ↑ ∧Π ∧ ∗i∈I (Pi (xi , t i ) ∧ Xi ↓)) = {xi |i ∈ I}. Then we define Roots(∃xΦ) =
     S if x ∈
Roots(Φ)           / Roots(Φ), and undefined otherwise. We define Cells(X ⇑ ∧Y ↑ ∧Π ∧ ∗i∈I (Pi (xi ) ∧ Xi ↓
)) = i∈I Xi . Then we define Cells(∃xΦ) = Cells(Φ) − {x}.
    We write (Roots + Cells)(F ) for Roots(F ) + Cells(F ) and call them address variables of F .
    We define a substitution as a map from the set of variables to the set of terms. For a substitution θ,
we define Dom(θ) = {x|θ(x) 6≡ x} and Range(θ) = {θ(x)|x ∈ Dom(θ)}. We define a variable renaming
as a substitution that is a bijection among variables with a finite domain.

Definition 3.1 s, h |= t ↓ iff s(t) ∈ Dom(h).
  s, h |= L(t) iff s(t) ∈ Range(h) − Dom(h).

   For saving space, we identify some syntactical objects that have the same meaning, namely, we use
implicit transformation of formulas by using the following properties: (F ∗G)∧X ↑↔ (F ∧X ↑)∗(G∧X ↑);
(F ∗ G) ∧ X ⇑↔ (F ∧ X ⇑) ∗ (G ∧ X ⇑).


                                                          4
3.2     Strong Wand
This section gives the definition clauses for inductive predicates that contain the strong wand.

Definition 3.2 The definition clauses of Q(y, −                →
                                                               w )—∗s P (x, −→
                                                                             y ) are as follows:
                                     →
                                     −                                      →
                                                                            −
    Case 1. ∃( z − zi )(( w = t i ∧ Π ∧ x 7→ ( u ) ∗ ∗l6=i Pl (zl , t l ))[zi := y]) where Q = Pi and ∃−
                   →
                   −           →
                               −                          →
                                                          −                                                       →
                                                                                                                  z (Π ∧ x 7→
 →
 −                 →
                   −                                             −
                                                                 →
( u ) ∗ ∗l Pl (zl , t l )) is a definition clause of P (x, y ).
                                                          →
                                                          −                             →
                                                                                        −
    Case 2. ∃−   → z (Π ∧ x 7→ (− →
                                  u ) ∗ ∗l6=i,l∈L Pl (zl , t l ) ∗ (Q(y, −
                                                                         →
                                                                         w )—∗s Pi (zi , t i ))) where i ∈ L and ∃−
                                                                                                                  →
                                                                                                                  z (Π ∧ x 7→
 →
 −                    →
                      −                                             →
                                                                    −
( u ) ∗ ∗l∈L Pl (zl , t l )) is a definition clause of P (x, y ).

Q(y)—∗s P (x) is inductively defined by the definition clauses obtained by removing Q(y) from the defini-
tion clauses of P (x). Q(y)—∗s P (x) plays a similar role to the ordinary magic wand Q(y)—∗P (x), but it
is stronger than the ordinary magic wand and it is defined syntactically. Roughly speaking, it is defined
to be false if it cannot be defined syntactically.

Example 3.3 ls(y, v)—∗s ls(x, w) =def w = v ∧ x 7→ (y) ∨ ∃z(x 7→ (z) ∗ (ls(y, v)—∗s ls(z, w))).
                  →
                  −             →
                                −            →
                                             −            →
                                                          −             →
                                                                        −            →
                                                                                     −
    Note that Q1 ( t 1 )—∗s Q2 ( t 2 )—∗s P ( t ) and Q2 ( t 2 )—∗s Q1 ( t 1 )—∗s P ( t ) are equivalent, which
will be shown by Lemma 5.1.


4     System CSLIDω
This section defines our logical system CSLIDω .

4.1     Inference Rules
This subsection gives the set of inference rules.
    We define Dep(P ) as the set of inductive predicates symbols that appear in the unfolding of P . We
write F [F ′ ] to explicitly display the subformula F ′ in F . We write T for a finite set of terms. We say Φ
is equality-full when Π contains (6= (−   →
                                          y ,V ∪ −
                                                 →
                                                 y ∪ {nil})) where Φ is ∃−  →
                                                                            x ∃−
                                                                               →
                                                                               y ⇑ (Π ∧ Γ) and V = FV(Φ).
              ′    →
                   −   →
                       −                     ′
We write Π ⊆ ∃ x ∃ y ⇑ (Π ∧ Γ) when Π ⊆ Π. We call a context F [ ] positive when the number of ¬( )
and ( ) → F ′ that contain [ ] is even. We call a context F [ ] existential when it is of the form ∃−
                                                                                                    →
                                                                                                    x ([ ] ∗ F ′ ).
    We assume a number dwand for the maximum depth of wands.
    The inference rules are given in the figure 1.
    The rule (Factor) derives P (t) from (Q(y)—∗s P (t)) ∗ Q(y) where we list up all the cases for Q(y)
in the disjunction. The rules (∃ Amalg1, 2) amalgamate ∃x’s under some condition, which guarantees
that existentials have the same values. The rule (∗) is a new split rule since it handles disjunction in the
succedent. The other rules are standard.

4.2     Proofs in CSLIDω
This subsection defines a proof in CSLIDω .

Definition 4.1 We define a bud and a companion in the same way as [7]. For CSLIDω , we define a
cyclic proof to be a proof figure by the inference rules without any open assumptions where each bud has
a companion below it and there is some rule (∗ 7→) between them.

    Instead of the global trace condition in ordinary cyclic proof systems [7], CSLIDω requires some (∗ 7→)
rule between a bud and its companion.

4.3     Preparation for Soundness Proof
The following is a key notion for simple soundness proof.
                                  →
                                  −                                                                 →
                                                                                                    −
Definition 4.2 We write F |=m G when for all s, h, |Dom(h)| ≤ m and s, h |= F imply s, h |= G . We
         →
         −                                →
                                          −                 →
                                                            −
say F ⊢ G is m-valid and write |=m F ⊢ G when F |=m G .
    We call a rule m-sound when the following holds: if all the assumptions are m-valid then the conclusion
is m-valid.

                                                             5
     →
     −
 F ⊢ G
     → (Subst)
     −                               (emp)        → (Unsat)
                                                  −
Fθ ⊢ Gθ                  emp ⊢ emp            F ⊢G          (F unsatisfiable)
       →
       −                     → −
                             −                             →
                                                           −
  F ⊢ G                  F ⊢ G , ∃→        ′
                                  x (G ∧ G )          F ⊢ G , ∃−
                                                               →
                                                               x (G ∧ ¬G)
  ′       → (∧L)
          −                      → −
                                 −   →
                                             (∧Elim)             →
                                                                 −          (∨Elim)
F ∧F ⊢ G                    F ⊢ G, ∃ x G                     F ⊢G
             →
             −                                        →
                                                      −
  F ∧ F′ ⊢ G, G                    (x ↑ ∗F1 ) ∗ F2 ⊢ G
          →
          −            (∧R)                       →
                                                  −       (↑ Elim)
F ∧ F′ ⊢ G, G ∧ F′                     F1 ∗ F2 ⊢ G                  (x ∈ (Roots + Cells)(F2 ))
      →
      −                     →
                            −                                       →
                                                                    −                               −
                                                                                                    →
 F ⊢G                 F ⊢ G , G[w := t]                F [x := t] ⊢ G [x := t]                 F ⊢ G, G
     →
     −     (∨R)                →
                               −             (∃R)                       →
                                                                        −       (=  L)          −
                                                                                                →             (= R)
F ⊢ G, G                 F ⊢ G , ∃wG                       x=t∧F ⊢ G                       F ⊢ G, G ∧ t = t
                       →
                       −                              →
                                                      −                                −
                                                                                       →
F ∗ (F1 ∧ x ↓) ∗ F2 ⊢ G F ∗ F1 ∗ (F2 ∧ x ↓) ⊢ G                                    F ⊢ G, G
                                         →
                                         −                (↓ Out  L)           →
                                                                               −                      (⇑ R)
             F ∗ ((F1 ∗ F2 ) ∧ x ↓) ⊢ G                                   F ⊢ G , ∃y ⇑ (y 6= T ∧ G)
     →
     − →                                                                                      −
                                                                                              →      −
                                                                                                     →
F ⊢ G , ∃−x (G ∗ (G1 ∧ t ↓) ∗ G2 ), ∃− →x (G ∗ G1 ∗ (G2 ∧ t ↓))                       F ∗ P(t, t ) ⊢ G , G
                 → →
                 −                                                (↓ Out  R)                      −
                                                                                                  →           (↓ R)
            F ⊢ G , ∃− x (G ∗ ((G1 ∗ G2 ) ∧ t ↓))                                  F ∗ P(t, −
                                                                                            →
                                                                                            t ) ⊢ G, G ∧ t ↓
          →
          −                  →
                             −
F ∧ F ′ ⊢ G F ∧ ¬F ′ ⊢ G
                →
                −               (Case L)
           F ⊢G
     →
     −            −−−−→
                      − −→                     →
                                               −       −−−−→
                                                           − −→
F ⊢ G , {G[∃− →
              w ((Q1 ( t 1 ), Q(y, −
                                   →w )—∗s P ( t )) ∗ (Q2 ( t 2 )—∗s Q(y, −
                                                                          →
                                                                          w )))] |
              →
              −                 →
                                −
Q ∈ Dep(P ), Q 2 ⊆ Dep(Q), w fresh}
                                 −−−−   −→ −−−−  −→                                     (Factor)
                           →
                           −           →
                                       −        →
                                                −             →
                                                              −
                    F ⊢ G , G[Q1 ( t 1 ), Q2 ( t 2 )—∗s P ( t )]                                  (G[ ] existential)
     → −
     −   →         →
                   −                                       →
                                                           −       → −
                                                                   −  →             →
                                                                                    −
A(x, t , z ) ∗ F ⊢ G (for every definition clause ∃ z A(x, t , z ) of P (x, t ))
                                                   →
                                                   −                                     (Pred L)
                                  P (x, −→t )∗F ⊢ G
     →
     −
F ⊢ G , {G[φ] | φ is a definition clause of P (x, −  →t )}
                      →
                      −             →
                                    −                       (Pred R)
                 F ⊢ G , G[P (x, t )]                                 (G[ ] existential)
         x ↑ ∧F ⊢ {Gi | i ∈ I}
                                          (∗ 7→)
F ∗ x 7→ (−
          →u ) ⊢ {Gi ∗ x 7→ (−
                             →
                             u ) | i ∈ I}
    →
    −
F ⊢ G , G[∃x ⇑ Φ1 ∗ ∃x ⇑ Φ2 ]
       →
       −                        (∃ Amalg1)
 F ⊢ G , G[∃x ⇑ (Φ1 ∗ Φ2 )]                 (∃x ⇑ Φ1 , ∃x ⇑ Φ2 equality-full, G[ ] positive)
       →
       −
  F ⊢ G , G[∃xΦ1 ∗ ∃x ⇑ Φ2 ]
                                 (∃ Amalg2) x ∈ Cells(Φ1 ), (x 6= FV(∃x ⇑ Φ2 )) ⊆ Φ1 ,
                                                                                          !
    →
    −
F ⊢ G , G[∃x(Φ1 ∗ (x ⇑ ∧Φ2 ))]                 ∃x ⇑ Φ2 equality-full, G[ ] positive

F1 ⊢ {Gi1 | i ∈ I ′ } or F2 ⊢ {Gi2 | i ∈ I − I ′ }   (∀I ′ ⊆ I)
                                                                  (∗)
                F1 ∗ F2 ⊢ {Gi1 ∗ Gi2 | i ∈ I}



                                        Figure 1: Inference Rules




                                                       6
Lemma 4.3 If x ∈
               / T , then
        F → ∃x ⇑ ((x 6= T ) ∧ F ).

    Proof. Assume
        s, h |= F.

There is a such that a 6= s(T ) and ∈
                                    / Dom(h) ∪ Range(h) since the set of addresses is infinite. Then
        s[x := a], h |= x ⇑ ∧(x 6= T ).

Hence
        s, h |= ∃x ⇑ ((x 6= T ) ∧ F ).

✷

Definition 4.4 For a heap h, Leaves(h) is defined as Range(h) − Dom(h).

Lemma 4.5 If
        s, h |= Γ
                     S − →                  −
                                            →
then Leaves(h) ⊆      {s( t ∪ {nil}) | P (x, t ) ∈ Γ}.

   Proof. By induction on |h|.
   Let Γ be ∗i ∆i . Assume a ∈ Leaves(h). We have h = Σi hi such that s, hi |= ∆i . We have i such that
                                  −
                                  →
a ∈ Leaves(hi ). Let ∆i be P (x, t ) ∧ X ↓. Let
                                                     →
                                                     −
      s[−
        →
        z := − →r ], h |= Π ∧ x 7→ (−
                                    →
                                    u ) ∗ ∗l Pl (zl , t l ).
                    →
                    −                                                   →
                                                                        −
ui is included in x, t , nil, −
                              →
                              z . Hence s(−
                                          →
                                          u ) − Dom(h) is included in s( t , nil).
    Let s′ be s[−
                →
                z := −→r ] and hi = h′ + h′′ such that
       s′ , h′ |= x 7→ (− →u ),
                              →
                              −
       s′ , h′′ |= ∗l Pl (zl , t l ).
                            S        →
                                     −               →
                                                     −                     →
                                                                           −                 →
                                                                                             −
By IH, Leaves(h′′ ) ⊆ {s′ ( t l ∪ {nil}) | l}. Since t l are included in x, t , nil, →
                                                                                     −
                                                                                     z , s′ ( t l ) − Dom(h) are
                 →
                 −
included in s( t , nil).                                   S −
                                      →
                                      −                         →                   −
                                                                                    →
    Hence a is included in s( t , nil). Hence Leaves(h) ⊆ {s( t ∪ {nil}) | P (x, t ) ∈ Γ}. ✷


5     Soundness of Rule (Factor) and Properties for Strong Wands
We prove some properties for strong wands.
                  →
                  −                     →
                                        −                 →
                                                          −                →′
                                                                           −                                  −
                                                                                                              →′
   The order in R is not important in R —∗s P , since R —∗s P and R —∗s P are equivalent when R is
                   →
                   −
a permutation of R . This is shown in the next lemma.
                                        −−−−−  →
Lemma 5.1 The definition clauses of R(v, −   →u )—∗s P (x, − →
                                                             z ) are
                      V −−−−−− →           →
                                           −            −−−−−−−→   −−→
      ∃(−
        →
        w 1i )i∈I (Π ∧ −→
                        u2 = − →
                               s 2 ∧ x 7→ ( t ) ∗ ∗i∈I (R1i (v1i , −
                                                                   u 1i )—∗s Q1i (w1i , −
                                                                                        →
                                                                                        s 1i )))[−
                                                                                                 →
                                                                                                 w 2 := −
                                                                                                        →
                                                                                                        v 2 ] (#)
                                                      →
                                                      −     −−−−− →                                       −−−−−→
for each definition clause ∃−          →
                                       w (Π ∧ x 7→ ( t ) ∗ Q(w, −→s )) of P (x, −
                                                                                →
                                                                                z ), and divisions R(v, −      →
                                                                                                               u) =
 −−−−−−−→   −−→          −−−−−−   −→                                 −−−−− →                              −−−−−−−   −→
(R1i (v1i , −
            u 1i ))i∈I , R2 (v2 , −
                                  →
                                  u 2 ) (with some permutation) and Q(w, − →
                                                                           s ) = (Q1i (w1i , −
                                                                                             →
                                                                                             s 1i ))i∈I , Q2 (w2 , −
                                                                                                                   →
                                                                                                                   s 2)
            →
            −        →
                     −                  →
                                        − ′                   →
                                                              −        →
                                                                       − ′                           →
                                                                                                     −
such that R 2 = Q 2 . Hence, if R is a permutation of R , then R —∗s P is equivalent to R —∗s P . Note
            →
            −
that each R 1i can be empty.




                                                          7
                                              →
                                              −
     Proof. By induction on the length of R .
                             →
                             −                          →
                                                        −              →
                                                                       −
     Case 0. In this case, Q = (Q1i )i and all of ( R 1i )i and R 2 are empty. Hence, (#) is the same as
                  →
                  −     −−−−− →
∃−→w (Π ∧ x 7→ ( t ) ∗ Q(w, −
                            →s )).
             ′ −
               → s                  →
                                    −                                                                          →
                                                                                                               −
     Case R , R —∗ P (= R′ —∗s ( R —∗s P )). By the induction hypothesis, a definition clause of R —∗s P
is
                          V− −−−−− →           →
                                               −            −−−−−−−→   −−→
        ∃(−
          →w 1i )i∈I (Π ∧ − →
                            u2 = − →
                                   s 2 ∧ x 7→ ( t ) ∗ ∗i∈I (R1i (v1i , −
                                                                       u 1i )—∗s Q1i (w1i , −
                                                                                            →
                                                                                            s 1i )))[−
                                                                                                     →
                                                                                                     w 2 := −
                                                                                                            →
                                                                                                            v 2]
                                                        →
                                                        −       −−−−−  →                                         −−−−− →
for a definition clause ∃−          →
                                    w (Π ∧ x 7→ ( t ) ∗ Q(w, −       →s )) of P , and some divisions R(v, −          →u) =
 −−−−−−−−   −−→          −−− −−  − −→        −− −−−→                               −
                                                                                   − − −−− −  −
                                                                                              →              →
                                                                                                             −     →
                                                                                                                   −
(R1i (v1i , →
            u 1i ))i∈I , R2 (v2 , −
                                  →
                                  u 2 ) and Q(w, − →
                                                   s ) = (Q1i (w1i , −
                                                                     →s 1i ))i∈I , Q2 (w2 , →
                                                                                            −s 2 ) such that R 2 = Q 2 .
                                                                                                                   →
                                                                                                                   −
   By the definition of the strong wand, we have two cases for the definition clauses of R′ —∗s ( R —∗s P ).
                      ′   →
                          −         s                             →
                                                                  −                         ′
   Subcase 1. R = R 1j —∗ Q1j for some j, that is, R 1j is empty and R = Q1j , and the clause is
                             V−   −−−−−  →                         →
                                                                   −
        ∃(− →
            w 1i )i6=j (Π ∧ −  → u2 = − →s 2 ∧ u1j = s1j ∧ x 7→ ( t )∗
                      −−−−−−−−   − −→
              ∗i6=j (R1i (v1i , →u 1i )—∗s Q1i (w1i , −
                                                      →
                                                      s 1i )))[−
                                                               →
                                                               w 2 := −
                                                                      →v 2 , w1j := v1j ].
                                      →
                                      −      →
                                             −                →
                                                              −
This is (#) for the division R′ , R = (( R 1i )i6=j , (R′ , R 2 )).
   Subcase 2. The clause is
                      V→−−−−−−     →           →
                                               −
       ∃(−
         →
         w 1i )i (Π ∧ −  u2 =−   → s 2 ∧ x 7→ ( t )∗
                   −−−−−−−−  −−→                                   →
                                                                   −
           ∗i6=j (R1i (v1i , →
                             u 1i )—∗s Q1i (w1i , −
                                                  →s 1i )) ∗ (R′ , R 1j —∗s Q1j ))[−
                                                                                   →
                                                                                   w 2 := −
                                                                                          →
                                                                                          v 2 , w1j := v1j ].
                                  →
                                  −     →′
                                        −          →
                                                   −            →′
                                                                −      →
                                                                       −                    →′
                                                                                            −           →
                                                                                                        −
This is (#) for the division R′ , R = (( R 1i )i , R 2 ), where R 1i = R 1i for i 6= j, and R 1i = R′ , R 1i for
i = j. ✷
   The following shows what is derived from the strong wand.
                                                                                          −−−−− →
Lemma 5.2 (Strong Wand Elimination) (Q(y, −
                                          →
                                          w )—∗s P (x, −
                                                       →
                                                       z ))                          ∗   (R(v, −
                                                                                               →
                                                                                               u )—∗s Q(y, →
                                                                                                           −
                                                                                                           w ))        |=
−−−−−
    →
    −→    s     →
                −
R(v, u )—∗ P (x, z ).

    Proof. We prove s, h |= LHS implies s, h |= RHS by induction on the size of h.
    Suppose s, h |= LHS, then we have some h1 + h2 = h such that
        s, h1 |= Q(y, −
                      →
                      w )—∗s P (x, −
                                   →
                                   z)
                 −−−−−→
                      −→ s         →
                                   −
        s, h2 |= R(v, u )—∗ Q(y, w ).
By the definition of the strong wand, we have the following two cases.
   Case 1. We have
                                                             →
                                                             −
      s, h1 |= ∃(−
                 →r )(−
                      →
                      w =− →s Q ∧ Π ∧ x 7→ (−
                                            →
                                            u ) ∗ ∗l Sl (rl , t l ))[rQ := y]
                                           →
                                           −
for a definition clause ∃(−
                          →
                          r rQ )(Π ∧ x 7→ ( t ) ∗ Q(rQ , −
                                                         →
                                                         s Q ) ∗ ∗l Sl (rl , −
                                                                             →
                                                                             s l )) of P (x, −
                                                                                             →
                                                                                             z ). Then, we have some
→
−
 b such that
                →
                −                                                                 →
                                                                                  −
       s[−→
          r := b , rQ := s(y)], h1 |= −
                                      →
                                      w =− →s Q ∧ Π ∧ x 7→ (−  →
                                                               u ) ∗ ∗l Sl (rl , t l ).
                →
                −
Let s′ = s[−
           →
           r := b , rQ := s(y)]. We also have
                   −−−−− →
        s′ , h2 |= R(v, −
                        →
                        u )—∗s Q(y, →
                                    −
                                    w ),
                               −−−−−→
since none of −
              →
              r , rQ occurs in R(v, −
                                    →
                                    u )—∗s Q(y, −
                                                →
                                                w ). Hence we have
                            →
                            −       −−−−− →                            →
                                                                       −
        s′ , h |= Π ∧ x 7→ ( t ) ∗ (R(v, −
                                         →
                                         u )—∗s Q(y, −
                                                     →
                                                     w )) ∗ ∗l Sl (rl , t l ).
Since s′ , h |= −
                →
                w =−
                   →
                   s Q and s′ (rQ ) = s(y), we have
                            →
                            −       −−−−− →                                →
                                                                           −
        s′ , h |= Π ∧ x 7→ ( t ) ∗ (R(v, −
                                         →
                                         u )—∗s Q(rQ , −
                                                       →
                                                       s Q )) ∗ ∗l Sl (rl , t l ),
and hence,
                                   →
                                   −       −−−−− →                                →
                                                                                  −
        s, h |= ∃(−
                  →
                  r rQ )(Π ∧ x 7→ ( t ) ∗ (R(v, −
                                                →
                                                u )—∗s Q(rQ , −
                                                              →
                                                              s Q )) ∗ ∗l Sl (rl , t l )),

                                                             8
                                −−−−−→
which is a definition clause of R(v, −
                                     →
                                     u )—∗s P (x, −
                                                  →
                                                  z ) by Lemma 5.1.
   Case 2. We have
                                                                         →
                                                                         −
       s, h1 |= ∃(−
                  →
                  r r)(Π ∧ x 7→ (−
                                 →
                                 u ) ∗ (Q(y, −
                                             →
                                             w )—∗s S(r, −
                                                         →
                                                         s )) ∗l Sl (rl , t l ))
                                           →
                                           −                                                                       →
                                                                                                                   −
for a definition clause ∃(−
                          → r r)(Π ∧ x 7→ ( t ) ∗ S(r, −
                                                       →
                                                       s ) ∗ ∗l Sl (rl , −
                                                                         →
                                                                         s l )) of P (x, −→z ). Then, we have some b
and b such that
                →
                −                                                                          →
                                                                                           −
       s[−
         →r := b , r := b], h1 |= Π ∧ x 7→ (−
                                            →u ) ∗ (Q(y, −
                                                         →
                                                         w )—∗s S(r, −    →s )) ∗l Sl (rl , t l ).
                →
                −
Let s′ = s[−
           →
           r := b , r := b], and we have some h1 = hx + hS + Σl hl such that
                          →
                          −
       s′ , hx |= x 7→ ( t )
       s , hS |= Q(y, w )—∗s S(r, −
        ′                →
                         −            →s)
        ′                →
                         −
       s , hl |= Sl (rl , s l ) (for each l).
We also have
                  −−−−− →
                       u )—∗s Q(y, →
       s′ , h2 |= R(v, −
                       →           −
                                   w ),
                                −−−−− →
since none of − r , r occurs in R(v, −
                →                    →
                                     u )—∗s Q(y, →
                                                 −
                                                 w ). Therefore, we have
                        −−−−− →
       s′ , hS + h2 |= R(v, −
                            →u )—∗s S(r, −
                                         →
                                         s)
by IH. Hence, we have
                           →
                           −       −−−−− →
       s′ , h |= Π ∧ x 7→ ( t ) ∗ (R(v, −
                                        →
                                        u )—∗s S(r, −
                                                    →
                                                    s )) ∗ ∗l Sl (rl , −
                                                                       →
                                                                       s l ),
and then
                                →
                                −       −−−−−→
                 r r)(Π ∧ x 7→ ( t ) ∗ (R(v, −
       s, h |= ∃(−
                 →                           →
                                             u )—∗s S(r, −
                                                         →
                                                         s )) ∗ ∗l Sl (rl , −
                                                                            →
                                                                            s l )),
                                −−−−−→
which is a definition clause of R(v, −
                                     →
                                     u )—∗s P (x, −   →
                                                      z ) by Lemma 5.1. ✷
   By the previous two lemmas, we have
                  −−−−− →                   −−−−−−    −→                    −−−−−→ −−−−−−       −→
      (Q(y, −w ), R(v, −
             →         →
                       u )—∗s P (x, −
                                    →
                                    z )) ∗ (R′ (v ′ , −
                                                      →
                                                      u ′ )—∗s Q(y, →
                                                                    −
                                                                    w )) |= R(v, −
                                                                                 →
                                                                                 u ), R′ (v ′ , −
                                                                                                →
                                                                                                u ′ )—∗s P (x, −
                                                                                                               →
                                                                                                               z ).
   The following shows what derives the strong wand.
                                                                                  −−−−−   →
Lemma 5.3 (Strong Wand Introduction) x                    6=    y ∧ y       ↓  ∧(R(v, −  →u )—∗s P (x, −
                                                                                                       →
                                                                                                       z ))     |=
                −−− −−  −− →                   −−− −−  −− →                 →
                                                                            −    →
                                                                                 −      →
                                                                                        −                   →
                                                                                                            −
{∃−
  →
  w ((Q(y, −
           →
           w ), R1 (v1 , −
                         →
                         u 1 )—∗ P (x, −
                                s      →
                                       z )) ∗ (R2 (v2 , −
                                                        →
                                                        u 2 )—∗ Q(y, −
                                                               s     →
                                                                     w )) | R = ( R 1 , R 2 ), Q ∈ Dep(P ), R 2 ⊆
Dep(Q)}
   Proof. We prove s, h |= LHS implies s, h |= RHS by induction on the size of h.
                                      −−−−− →
   Suppose s, h |= LHS. Since s, h |= R(v, −
                                           →
                                           u )—∗s P (x, − →
                                                          z ), we have
                           V−−−−−−− →         →
                                              −          −−−−−−−−   −−→
      s, h |= ∃(rAi )i (Π ∧ −
                            →
                            uB = −→                                 u Ai )—∗s SAi (rAi , −
                                  s B ∧ x 7→ ( t ) ∗ ∗i (RAi (vAi , −
                                                                    →                    →
                                                                                         s Ai )))[−
                                                                                                  →
                                                                                                  r B := −
                                                                                                         →
                                                                                                         v B]
for some definition clause
                               →
                               −                             −−−−−−→  −−→
       ∃(rAi )i −
                →
                r B (Π ∧ x 7→ ( t ) ∗ ∗i SAi (rAi , −
                                                    →
                                                    s Ai ) ∗ SB (rB , −
                                                                      s B ))
                          −−−−− →       −−−−−−−−    −−→ −−−−−−−−       −−→             →
                                                                                       −     →
                                                                                             −
of P and some division R(v, −  →u ) = (RAi (vAi , −→
                                                   u Ai ))i , RB (vB , →
                                                                       u B ) such that R B = S B .
    Then, we have some (bAi )i such that
                                                     V−  −−−−−→   −→
      s[(rAi := bAi )i , →
                         −
                         r B := s(−→v B )], h |= Π ∧ −  →uB = −   s B∧
                 →
                 −          −−−−−−−−   −−→
           x 7→ ( t ) ∗ ∗i (RAi (vAi , −
                                       →
                                       u Ai )—∗s SAi (rAi , − →
                                                              s Ai )).

Let s′ = s[(rAi := bAi )i , −
                            →
                            r B := s(−
                                     →
                                     v B )]. We have h = hx + Σi hAi such that
                        →
                        −
       s′ , hx |= x 7→ ( t )
                   −− −−− −−− −−→
       s′ , hAi |= RAi (vAi , −
                              →
                              u Ai )—∗s SAi (rAi , −
                                                   →
                                                   s Ai ).


                                                             9
Since s′ |= x 6= y, we have y ∈ dom(hAk ) for some k, and hence we have
                        −−−−−−−−−   −−→
       s′ , hAk |= y ↓ ∧RAk (vAk , −
                                   →
                                   u Ak )—∗s SAk (rAk , −
                                                        →
                                                        s Ak ).
                                                  →
                                                  −     → −
                                                        −   →          →
                                                                       −     →
                                                                             −
   Case s′ (y) = bAk (= s′ (rAk )). Let Q = SAk , R 1 = R − R Ak , and R 2 = R Ak . Note that Q ∈ Dep(P )
    →
    −
and R 2 ⊆ Dep(Q). Then, we have
                  −−−−−−   −→
      s′ , hAk |= R2 (v2 , −
                           →
                           u 2 )—∗s Q(y, →
                                         −
                                         s Ak ).
   We show
                                           −−−−−−   −→
       s′ , Σi6=k hAi + hx |= Q(y, −
                                   →
                                   s Ak ), R1 (v1 , −
                                                    →
                                                    u 1 )—∗s P (x, −
                                                                   →
                                                                   z ).
Now,
                               →
                               −                                                 −−−−−−−  −−→
       ∃(rAi )i −
                →
                r B (Π ∧ x 7→ ( t ) ∗ ∗i6=k SAi (rAi , −
                                                       →
                                                       s Ai ) ∗ Q(rAk , −
                                                                        →
                                                                        s Ak ) ∗ SB (rB , →
                                                                                          s B ))
                                                        →
                                                        −         →
                                                                  −                →
                                                                                   −
is a definition clause of P . Consider the division R = (( R Ai )i6=k ), (Q, R B ), and it is sufficient to show
that
                                                V→ −−−−−−−−→ −
       s′ , Σi6=k hAi + hx |= ∃(rAi )i6=k (Π ∧ −   uB = → sB ∧→   s Ak = − →s Ak ∧
                    →
                    −            −−−−−−−−   − −→
             x 7→ ( t ) ∗ ∗i6=k (RAi (vAi , u Ai )—∗ SAi (rAi , s Ai )))[ r B := −
                                           →
                                           −         s         →
                                                               −         →
                                                                         −        →v B , rAk := y],
which follows from
            −−−−−−→−→
            uB =−
      s′ |= −
            →      sB
       s′ (rAk ) = s′ (y)
                        →
                        −
       s′ , hx |= x 7→ ( t )
                  −−− −−− −− −−→
       s′ , hi |= RAi (vAi , →
                             −
                             u Ai )—∗s SAi (rAi , −
                                                  →
                                                  s Ai )    (for i 6= k).
Therefore, we have
                               →
                               −                     −−−−−−−→ −−→
       s′ , h |= (Q(y, −
                       →
                       s Ak ), R A —∗s P (x, −
                                             →                u B )—∗s Q(y, −
                                             z )) ∗ (RB (vB , −             →
                                                                            s Ak )),
so we have
                               →
                               −                     −−−−−−−→ −−→
                  w (Q(y, −
       s′ , h |= ∃−
                  →       →
                          w ), R A —∗s P (x, −
                                             →                u B )—∗s Q(y, −
                                             z )) ∗ (RB (vB , −             →
                                                                            w )),
and hence
                             →
                             −                     −−−−−−−→ −−→
                w (Q(y, −
       s, h |= ∃−
                →       →
                        w ), R A —∗s P (x, −                u B )—∗s Q(y, −
                                           z )) ∗ (RB (vB , −
                                           →                              →
                                                                          w )),
since (rAi )i , −
                →
                r B 6∈ RHS.
    Case s′ (y) 6= bAk . In this case, we have
                                    −−−−−−−−−  −−→
                                              u Ak )—∗s SAk (rAk , −
       s′ , hAk |= rAk 6= y ∧ y ↓ ∧RAk (vAk , −
                                              →                    →
                                                                   s Ak ).
                                                             →
                                                             −         →
                                                                       −       →
                                                                               −                →
                                                                                                −
By IH, there exist Q ∈ Dep(SAk ) ⊆ Dep(P ) and a division R Ak = R 1Ak , R 2Ak such that R 2Ak ⊆ Dep(Q)
and
                                  −−−−−−−−−−   −−−→                             −−−−−−−−−−   −−−→
       s′ , hAk |= ∃−
                    →
                    w ((Q(y, −
                             →
                             w ), R1Ak (v1Ak , −
                                               →
                                               u 1Ak )—∗s SAk (rAk , −
                                                                     →
                                                                     s Ak )) ∗ (R2Ak (v2Ak , −
                                                                                             →
                                                                                             u 2Ak )—∗s Q(y, −
                                                                                                             →
                                                                                                             w ))).
There exists −
             →
             c such that
                                        −−−−−−−−−−   −−−→
       s ′ [−
            →
            w := −
                 →
                 c ], h1Ak |= Q(y, −
                                   →
                                   w ), R1Ak (v1Ak , −
                                                     →
                                                     u 1Ak )—∗s SAk (rAk , −
                                                                           →
                                                                           s Ak )
         ′ −→    →
                 −            −−−− −−− − −−
                                          →
                                          −−− −→      s     →
                                                            −
       s [ w := c ], h2Ak |= R2Ak (v2Ak , u 2Ak )—∗ Q(y, w ),
and then we have
                                                      V→
                                                       −−−−−−−  −→
      s ′ [−
           →
           w := −→
                 c ], hx + Σi6=k hi + h1Ak |= Π ∧ −    uB = →   s B∧
                   →
                   −             −−−−−−−−   − −→                                     −−−−−−−−−−   −−−→
             x 7→ ( t ) ∗ ∗i6=k (RAi (vAi , u Ai )—∗ SAi (rAi , s Ai )) ∗ (Q(y, −
                                           →
                                           −        s          →
                                                               −                →
                                                                                w ), R1Ak (v1Ak , −
                                                                                                  →
                                                                                                  u 1Ak )—∗s SAk (rAk , −
                                                                                                                        →
                                                                                                                        s Ak )).
    →
    −         −
              →          →
                         −           →
                                     −     →
                                           −
Let R 1 = ( R Ai )i6=k , R 1Ak , and R 2 = R 2Ak (⊆ Dep(Q)), and then we have
                                                        →
                                                        −
       s ′ [−
            →
            w := −
                 →
                 c ], hx + Σi6=k hi + h1Ak |= Q(y, −
                                                   →
                                                   w ), R 1 —∗s P

                                                           10
and hence
                                       →
                                       −              →
                                                      −
        s ′ [−
             →
             w := −
                  →
                  c ], h |= (Q(y, −
                                  →
                                  w ), R 1 —∗s P ) ∗ ( R 2 —∗s Q(y, →
                                                                    −
                                                                    w )).
Therefore, we have
                               →
                               −              →
                                              −
                 w ((Q(y, −
        s, h |= ∃−
                 →        →
                          w ), R 1 —∗s P ) ∗ ( R 2 —∗s Q(y, →
                                                            −
                                                            w ))).
✷

Lemma 5.4 (Soundness of Rule (Factor)) The rule (Factor) is m-sound.

   Proof. Assume the antecedent of the conclusion is true at (s, h) and |Dom(h)| ≤ m in order to show
the succedent of the conclusion is true at (s, h). Then the antecedent of the assumption is true at (s, h).
Then the succedent of the assumption is true at (s, h). By Lemma 5.2 the succedent of the conclusion is
true at (s, h). ✷


6      Soundness of Rules (∃ Amalg1, 2)
Lemma 6.1 (1) If F is a formula constructed from =, 6=, emp, 7→, ∧, ∨, ∗, ∃x ↓, and T = FV(F ) ∪ {nil} −
−
→
y , and −
        → / s(T ) ∪ Dom(h) ∪ Range(h), and −
        a ∈                                →a are different from each other, and
        s, h |= −
                →
                y ⇑ ∧(6= (−
                          →
                          y ,T ∪ −
                                 →
                                 y )) ∧ F
then
        s[−
          →
          y := −
               →
               a ], h |= F.
    (2) If ∃y ⇑ Φ is equality-full, and a ∈
                                          / s(FV(∃y ⇑ Φ) ∪ {nil}) ∪ Dom(h) ∪ Range(h) and
        s, h |= ∃y ⇑ Φ,
then
        s[y := a], h |= Φ.
   (3) If ∃x ⇑ Φ1 and ∃x ⇑ Φ2 are equality-full, then ∃x ⇑ Φ1 ∗ ∃x ⇑ Φ2 → ∃x ⇑ (Φ1 ∗ Φ2 ).
   (4) If x ∈ Cells(Φ1 ), and (x 6= FV(∃x ⇑ Φ2 )) ⊆ Φ1 , and ∃x ⇑ Φ2 is equality-full, then ∃xΦ1 ∗ ∃x ⇑
Φ2 → ∃x(Φ1 ∗ (x ⇑ ∧Φ2 )).

    Proof. (1) We show the claim by induction on F .
    If F is F1 ∗ F2 or F1 ∧ F2 or F1 ∨ F2 , the claim immediately follows from IH.
    Case 1. ∃x ↓ F1 ,
    We have b ∈ Dom(h) such that
        s[x := b], h |= F1 .
Since −
      → / Dom(h), we have −
      a ∈                 →
                          a 6= b and s(−
                                       →
                                       y ) 6= b. From
        s[x := b], h |= −
                        →
                        y ⇑ ∧(6= (−
                                  →
                                  y , T ∪ {x} ∪ −
                                                →
                                                y )) ∧ F1 ,
by IH
        s[x := b, →
                  −
                  y := −
                       →
                       a ], h |= F1 .
Hence
        s[−
          →
          y := −
               →
               a ], h |= ∃x ↓ F1 .
   Case 2. emp. The claim immediately follows.
   Case 3. t 7→ (−
                 →
                 u ).
   t∈/ y since s(t) ∈ Dom(h). −
       →
       −                      →
                              u 6∋ −
                                   →
                                   y since s(−
                                             →
                                             u ) ⊆ Range(h). Since F does not contain −
                                                                                      →
                                                                                      y , the claim
holds.
   Case 4. t ↓.

                                                         11
    t∈/−→y since s(t) ∈ Dom(h). Since F does not contain −   →y , the claim holds.
    Case 5. u = t.
            /−
    If u, t ∈ →
              y , the claim immediately follows. If u ≡ t, the claim immediately follows. If u, t ∈ −   →
                                                                                                        y and
                                 →
                                 −        →
                                          −            →
                                                       −
u 6≡ t, it contradicts with (6= ( y , T ∪ y )). If u ∈ y and t ∈  →
                                                                  −
                                                                / y , then t ∈ T , which contradicts with the
assumption −  →
              y 6= T .
    Case 6. u 6= t.
            /−
    If u, t ∈ →
              y , the claim immediately follows. If u ≡ t, it contradicts with u 6= t. If u, t ∈ −
                                                                                                 →
                                                                                                 y and u 6≡ t,
  →
  −      →
         −                  →
                            −                         →
                                                      −
s[ y := a ] |= u 6= t since a are different. If u ∈ y and t ∈    →
                                                                 −                    →
                                                                                      −      →
                                                                                             −
                                                              / y , then t ∈ T , so s[ y := a ] |= u 6= t since
→
−a ∈/ s(T ).
    (2) Let T be FV(∃y ⇑ Φ) ∪ {nil}. Let Φ be ∃−      →
                                                      x ∃−
                                                         →
                                                         y ⇑ (Π ∧ Γ). Note that −  →x ∈ Cells(Γ). We have m
such that
        s, h |= ∃y ⇑ Φ(m) .
                         →
                         −
We have −
        →a ∈ Dom(h) and b , c such that
                     →
                     −
     s[−
       →x := −
             →
             a ,−
                →
                y := b , y := c], h |= −
                                       →
                                       y y ⇑ ∧Π ∧ Γ(m) .
Since −
      →
      a ∈ Dom(h), we have a 6= −
                               →a . From the equality-fullness,
                     →
                     −
      s[−
        →
        x := −
             →
             a ,−
                →
                y := b , y := c] |= (6= (y −
                                           →
                                           y , T ∪ {−
                                                    →
                                                    x , y−
                                                         →
                                                         y })).
       →′
       −            →′
                    −                                  →′
                                                       −            →′
                                                                    −
Choose b such that b ∈ / s(T ) ∪ Dom(h) ∪ Range(h), and b 6= a, and b are different from each other.
                                  →
                                  − ′                           →
                                                                −
By taking −
          →
          y to be y −
                    →
                    y,−→
                       a to be a b and s to be s[−
                                                 →x := −
                                                       →
                                                       a ,→
                                                          −
                                                          y := b , y := c] in (1),
                      →′
                      −
        s[−
          →
          x := −
               →
               a ,−
                  →
                  y := b , y := a], h |= Π ∧ Γ(m) .
Hence
        s[y := a], h |= ∃−
                         →
                         x ∃−
                            →
                            y ⇑ (Π ∧ Γ(m) ).
Hence
        s[y := a], h |= Φ.
   (3) Assume
        s, h |= ∃x ⇑ Φ1 ∗ ∃x ⇑ Φ2 .
We have h1 + h2 = h such that
        s, h1 |= ∃x ⇑ Φ1 ,
        s, h2 |= ∃x ⇑ Φ2 .
There is a such that a ∈
                       / s(FV(Φ1 , Φ2 ) ∪ {nil} − {x}) ∪ Dom(h) ∪ Range(h). By (2),
        s[x := a], h1 |= Φ1 ,
        s[x := a], h2 |= Φ2 .
Hence
        s[x := a], h1 + h2 |= Φ1 ∗ Φ2 .
Hence
        s, h |= ∃x ⇑ (Φ1 ∗ Φ2 ).
   (4) Assume
        s, h |= ∃xΦ1 ∗ ∃x ⇑ Φ2 .
Then we have h1 + h2 = h such that
        s, h1 |= ∃xΦ1 ,
        s, h2 |= ∃x ⇑ Φ2 .

                                                      12
Then we have a ∈ Dom(h1 ), b such that
        s[x := a], h1 |= Φ1 ,
        s[x := b], h2 |= x ⇑ ∧Φ2 .
                                                                   →
                                                                   −
Let Φ2 be ∃− →
             x 2 ∃−
                  →
                  y 2 ⇑ (Π2 ∧ Γ2 ). Then we have −→
                                                  a ∈ Dom(h2 ) and b ∈
                                                                     / Dom(h2 ) ∪ Range(h2 ) such that
                                            →
                                            −
by letting s′ be s[x := b, →
                           −
                           x 2 := −
                                  →a ,−
                                      →
                                      y 2 := b ],
        s′ , h2 |= Π2 ∧ Γ2 .

    We will show
    Claim 1: s[x := a], h2 |= x ⇑ ∧Φ2 .
    If a = b, the claim immediately follows. Assume a 6= b.
    We can show a ∈   / Range(h2 ) as follows. Assume a ∈ Range(h2 ) in order to show contradiction.
                                     →
                                     −       →
                                             −
a 6= −
     →a nil since a ∈ Dom(h1 ). a 6= b since b ∈ / Range(h2 ). a 6= s(FV(∃x ⇑ Φ2 )) since (x 6= FV(∃x ⇑
                                                 →
                                                 −
Φ2 )) ⊆ Φ1 . Hence a ∈  / s(FV(∃x ⇑ Φ2 )) ∪ {−
                                             →a , b , nil}. By Lemma 4.5, a ∈ s′ (FV(Γ2 ) ∪ {nil}), which
contradicts.
    We have shown a ∈  / Range(h2 ). Hence a ∈
                                             / s(FV(∃x ⇑ Φ2 ) ∪ {nil}) ∪ Dom(h2 ) ∪ Range(h2 ). By (2),
        s[x := a], h2 |= x ⇑ ∧Φ2 .

Hence we have shown the claim 1.
   Hence
        s[x := a], h |= Φ1 ∗ (x ⇑ ∧Φ2 ).

Hence
        s, h |= ∃x(Φ1 ∗ (x ⇑ ∧Φ2 )).

✷

Lemma 6.2 (Soundness of Rules (∃ Amalg1, 2)) The rules (∃Amalg1) and (∃Amalg2) are m-sound.

    Proof. We consider both rules simultaneously. Assume the antecedent of the conclusion is true at
(s, h) and |Dom(h)| ≤ m in order to show the succedent of the conclusion is true at (s, h). Then the
antecedent of the assumption is true at (s, h). Then the succedent of the assumption is true at (s, h). By
Lemma 6.1 (3) and (4) for (∃Amalg1) (∃Amalg2) respectively, the succedent of the conclusion is true at
(s, h). ✷


7     Soundness of Rule (∗)
We will show the soundness of the rule (∗). It is short but one of the most interesting parts in our
contribution.

Lemma 7.1 For propositional variables Aik (k = 1, 2, i ∈ I), the following is true in the propositional
logic:
       ^     _           _          _
          ((   Ai1 ) ∨ (   Ai2 )) ↔   (Ai1 ∧ Ai2 ).
        I1 +I2 =I   i∈I1       i∈I2        i∈I

    Proof. =⇒: Assume the negation of the right-hand side
         _
       ¬ (Ai1 ∧ Ai2 )
          i∈I

in order to show the negation of the left-hand side. It is
       ^
          (¬Ai1 ∨ ¬Ai2 )
        i∈I




                                                    13
Take I1 to be {i | ¬Ai1 } and I2 be I − I1 . Then
        ^             ^
      (    ¬Ai1 ) ∧ (     ¬Ai2 ).
         i∈I1              i∈I2

Hence
              _               _
        ¬((       Ai1 ) ∨ (        Ai2 )).
           i∈I1             i∈I2

Hence the negation of the left-hand side is true.
    ⇐=: Assume the i-th disjunct is true. For any I = I1 + I2 , i ∈ I1 or i ∈ I2 , so the conjunct of the
left-hand side is true. ✷

Lemma 7.2 (Split Lemma) The rule
        F1 ⊢ {Gi1 | i ∈ I ′ } or F2 ⊢ {Gi2 | i ∈ I − I ′ }              (∀I ′ ⊆ I)
                                                                                       (∗)
                            F1 ∗ F2 ⊢ {Gi1 ∗ Gi2 | i ∈ I}
is m-sound.

     Proof. For each I ′ ⊆ I, assume
        F1 |=m {Gi1 |i ∈ I ′ }
or
        F2 |=m {Gi2 |i ∈ I − I ′ }.
We will show F1 ∗ F2 |=m {Gi1 ∗ Gi2 |i ∈ I}.
  Assume s, h |= F1 ∗ F2 and |Dom(h)| ≤ m.
  We have h = h1 + h2 such that s, hi |= Γi (i = 1, 2). Then
        s, h1 |= F1 ,
        s, h2 |= F2 .
                                             _                           _
Since |Dom(h1 )|, |Dom(h2 )| ≤ m,                    s, h1 |= Gi1 or             s, h2 |= Gi2 . Since this holds for each I ′ ⊆ I, by
                                             i∈I ′                     i∈I−I ′
letting I1 = I ′ and I2 = I − I ′ ,
          ^       _                   _
                (   (s, h1 |= Gi1 ) ∨   (s, h2 |= Gi2 )).
        I1 +I2 =I i∈I1                       i∈I2
                    _
By Lemma 7.1,             (s, h1 |= Gi1 ∧ s, h2 |= Gi2 ). Therefore s, h |= Gi1 ∗ Gi2 for some i ∈ I. ✷
                    i∈I


8      Soundness of CSLIDω
This section proves the soundness theorem of CSLIDω . The soundness proof uses the fact that |Dom(h)|
decreases upwardly by the rule (∗ 7→).

Lemma 8.1 (1) For the rule (∗ 7→), if the assumptions are m-valid then the conclusion is (m + 1)-valid.
  (2) Every rule except (∗ 7→) is m-sound.

    Proof. (1) Assume the antecedent of the conclusion is true at (s, h) and |Dom(h)| ≤ m + 1 in order to
show the succedent of the conclusion is true at (s, h). We have h1 + h2 = h such that the first conjunct is
true at (s, h1 ) and the second conjunct is true at (s, h2 ). Then the antecedent of the assumption is true
at (s, h1 ). Since |Dom(h1 )| ≤ m, the succedent of the assumption is true at (s, h1 ). Hence the succedent
of the conclusion is true at (s, h).
    (2) Lemmas 5.4, 6.2 and 7.2 show m-soundness of (Factor), (∃Amalg) and (∗) respectively. (⇑ R) is
m-sound by Lemma 4.3. The claim for the other rules apparently holds. ✷
    When we allow open assumptions in a proof, we call it an open proof.

                                                                       14
Lemma 8.2 (1) For any bud J in a given proof, |=m J.
             →
             −                        →
                                      −
  (2) If F ⊢ G has a proof then F |=m G for any m.

    Proof. (1) Assume D is a proof. For a bud J in D, we define the height |J| as the number of judgments
in the path from the conclusion to its companion in D. Note that the path is not to the bud. For a bud
J in D, we will show |=m J by induction on (m, |J|).
    Let J ′ be the companion of J. Consider the open subproof πJ of J ′ in D.
    For a bud J1 in πJ such that |J1 | ≥ |J|, the companion of J1 is between J ′ and J1 . Hence there is a
rule application (∗ 7→) between J ′ and J1 . We remove the path from the assumption of the rule to J1 .
We do this for every such bud to obtain an open proof of πJ′ where the open assumptions are buds of
smaller heights or the conclusions of rule applications (∗ 7→). For an open assumption J2 of a bud in πJ′ ,
by IH for |J2 | < |J|, |=m J2 . Let J3 be an open assumption of the conclusion of the rule (∗ 7→) in πJ′ . By
case analysis of m, we show |=m J3 .
    Case m = 0. Since the antecedent of J3 is false with the empty heap, |=m J3 .
    Case m > 0. By IH for m − 1, the assumption of the rule (∗ 7→) is (m − 1)-valid. By Lemma 8.1 (1),
J3 is m-valid.
    Hence, in both cases,|=m J3 . Since J3 is arbitrary, all the open assumptions of πJ′ are m-valid. By
Lemma 8.1 (1)(2), |=m J ′ so |=m J.
                                    →
                                    −                                                                      →
                                                                                                           −
    (2) Assume a proof D of F ⊢ G . By (1), every bud of D is m-valid. By Lemma 8.1 (1)(2), F |=m G .
✷

Theorem 8.3 (Soundness) If J is provable in CSLIDω , then J is valid.
                        →
                        −                                                                 →
                                                                                          −
    Proof. Let J be F ⊢ G . Assume s, h |= F . Let m be |Dom(h)|. By Lemma 8.2 (2), F |=m G . Hence
        →
        −
s, h |= G . ✷


9     Satisfiability Checking
This section gives a satisfiability checking procedure for ψ.
    For each inductive predicate symbol P of arity m and each n ≥ 0, we add an inductive predicate
symbol P̂ n of arity m + n. For simplicity, we write P̂ for every P̂ n , since n is determined by the number
of arguments.
    We define the definition clauses for P̂ (x, −→
                                                 x,−
                                                   →y ) as the following (1) and (2) for each definition clause
        →
        −                                        →
                                                 −
of P (x, x ). Let the definition clause of P (x, x ) be
                                        →
                                        −
       ∃−→
         z (Π ∧ x 7→ (−→
                       u ) ∗ ∗i Pi (ti , t i )).
   (1) For each y, (−→
                     y i )i such that the sequence y(−
                                                     →y i )i is a permutation of the sequence− →y and the
sequence y i are in the same order as the sequence y , we define the definition clause of P̂ (x, −
         →
         −                                          →
                                                    −                                            →
                                                                                                 x,−
                                                                                                   →
                                                                                                   y ) by
                                               → −
                                               −
       ∃−
        →                    u ) ∗ ∗i P̂i (ti , t i , →
        z (Π ∧ x = y ∧ x 7→ (−
                             →                        y i )).
    (2) For each (−
                  →
                  y i )i such that the sequence (−
                                                 →
                                                 y i )i is a permutation of the sequence −
                                                                                         →
                                                                                         y and the sequence
−
→
y i are in the same order as the sequence y , we define the definition clause of P̂ (x, x , −
                                             →
                                             −                                           −
                                                                                         →  →
                                                                                            y ) by
                                       → →
                                       −
       ∃−
        →            u ) ∗ ∗i P̂i (ti , t i , −
        z (Π ∧ x 7→ (−
                     →                        y i )).

Lemma 9.1 We have P (x, −
                        →
                        x)∧−
                           →
                           y ↓↔ P̂ (x, −
                                       →
                                       x,−
                                         →
                                         y ).

    Proof. →:
    It is sufficient to show the following claim for all m.
    Claim 1: P (m) (x, − →
                         x)∧− →
                              y ↓ →P̂ (m) (x, −
                                              →
                                              x,−
                                                →y ).
    We show this claim by induction on m.
    Assume

       s, h |= P (m) (x, −
                         →
                         x)∧−
                            →
                            y ↓

in order to show s, h |= P̂ (m) (x, −
                                    →
                                    x ,→
                                       −
                                       y ).

                                                           15
   If m = 0, the immediately holds. Assume m > 0.
   We have a definition clause of P (x, −    →x)
                                      →
                                      −
       ∃−
        →
        z (Π ∧ x 7→ (−
                     →
                     u ) ∗ ∗i Pi (ti , t i ))
such that
                                                     →
                                                     −
         s, h |= ∃−
                  →
                  z (Π ∧ x 7→ (−
                               →          (m−1)
                               u ) ∗ ∗i Pi      (ti , t i )).

   Consider cases according to s(x) ∈ s(−   →
                                            y ).
                   →
                   −
   Case s(x) ∈ s( y ).
   Let y ∈ −
           →
           y such that s(x) = s(y).
   We have (−→
             y i )i such that y(−
                                →
                                y i )i is a permutation of −
                                                           →
                                                           y,−
                                                             →
                                                             y i are in the same order as −
                                                                                          →
                                                                                          y and
                                                              →
                                                              −
         s, h |= ∃−
                  →
                  z (Π ∧ x = y ∧ x 7→ (−
                                       →                 (ti , t i ) ∧ −
                                                                       →
                                                   (m−1)
                                       u ) ∗ ∗i (Pi                    y i ↓)).
By IH,
                                                              → →
                                                              −
         s, h |= ∃−
                  →
                  z (Π ∧ x = y ∧ x 7→ (−
                                       →                 (ti , t i , −
                                                   (m−1)
                                       u ) ∗ ∗i P̂i                  y i )).

Hence s, h |= P̂ (m) (x, −
                         →
                         x,−→
                            y ).
   Case s(x) ∈       →
                     −
               / s( y ).
   We have (− →y i )i such that (−
                                 →
                                 y i )i is a permutation of −
                                                            →
                                                            y,−
                                                              →
                                                              y i are in the same order as −
                                                                                           →
                                                                                           y , and
                                                      →
                                                      −
         s, h |= ∃−
                  →
                  z (Π ∧ x 7→ (−
                               →                 (ti , t i ) ∧ −
                                                               →
                                           (m−1)
                               u ) ∗ ∗i (Pi                    y i ↓)).
By IH,
                                                          → →
                                                          −
         s, h |= ∃−
                  →
                  z (Π ∧ x 7→ (−
                               →                     (ti , t i , −
                                             (m−1)
                               u ) ∗ ∗i P̂i                      y i )).

Hence s, h |= P̂ (m) (x, −
                         →
                         x,−
                           →y ).
   We have shown the claim 1.
   ←:
   It is sufficient to show the following claim.
   Claim 2: P̂ (m) (x, −→x,−
                           →
                           y ) → P (m) (x, −
                                           →
                                           x)∧−→
                                               y ↓.
   By induction on m we show this claim.
   If m = 0, the immediately holds. Assume m > 0.
   Assume s, h satisfies the antecedent.
   We have cases according to the definition clause (1) or (2) of P̂ (x, −
                                                                         →
                                                                         x,−
                                                                           →
                                                                           y ).
   Case (1). Let the definition clause be
                                                 → −
                                                 −
                               u ) ∗ ∗i P̂i (ti , t i , →
          z (Π ∧ x = y ∧ x 7→ (−
         ∃−
          →                    →                        y i ))
and
                                                              → →
                                                              −
                  z (Π ∧ x = y ∧ x 7→ (−
         s, h |= ∃−
                  →                    →                 (ti , t i , −
                                                   (m−1)
                                       u ) ∗ ∗i P̂i                  y i )).
By IH,
                                                              →
                                                              −
         s, h |= ∃−
                  →
                  z (Π ∧ x = y ∧ x 7→ (−
                                       →                 (ti , t i ) ∧ −
                                                                       →
                                                   (m−1)
                                       u ) ∗ ∗i (Pi                    y i ↓)).

Hence s, h |= P (m) (x, −
                        →
                        x)∧−→y ↓.
   Case (2) is similar to the case (1). We have shown the claim 2. ✷
   We check the satisfiability of ψ by extending the decision procedure for the satisfiability of a symbolic
heap given in [10].

Theorem 9.2 ([10]) For a given symbolic heap φ, we can effectively compute the set [[φ]] of its base
pairs such that φ is satisfiable iff for some (V, Π) ∈ [[φ]], Π is satisfiable.




                                                                 16
Definition 9.3 We give a decision algorithm to check the satisfiability of given
                               →
                               −
      Y ↑ ∧Π ∧ ∗i∈I (Xi ↓ ∧Pi ( t i )).
   Step 1. By using the Lemma 9.1 to eliminate ↓ keeping equivalence, we transform the goal into
                         → →
                         −
      Y ↑ ∧Π ∧ ∗i∈I P̂i ( t i , −
                                x i)
where −→
       x i is a sequence of elements in Xi .
                                             → →
                                             −
   Step 2. For each i ∈ I, we compute [[P̂i ( t i , −
                                                    x i )]] by using the algorithm by [10], and let it be Bi .
   Step 3. Try to find some (Vi , Πi^ ) in Bi for each i ∈ I such that Vi and Y are disjoint under the
                      U
equality of Π, and ⊗( i∈I Vi ) ∧ Π ∧     Πi is satisfiable.
                                       i∈I
    Step 4. If there are such (Vi , Πi ) (i ∈ I), answer with ”satisfiable”. Otherwise, answer with ”unsatis-
fiable”.


10      Decision Algorithm
This section gives the algorithm to decide the validity of a given entailment. First define normal forms
and groups, then define the algorithm, finally we will show the partial correctness, loop invariants, and
the termination of the algorithm.

10.1     Normal Form and Group
This section defines a normal form and a group. In our proof search algorithm, a normal form is used as
a bud in cyclic proofs and the termination will be proved by counting normal forms. Groups are used for
the (∗) rules to keep validity.
Definition 10.1 (Groups) A variable group of ψ is defined to be the set (Roots+ Cells)(∆) of variables
for some ∆ in ψ. A variable group of an entailment J is defined to be a variable group of the antecedent
in J. A formula F in an entailment J is called a group when (Roots + Cells)(F ) is a variable group of J.
In particular, the ∗-conjunct P (x) ∧ y1 ↓ ∧ . . . ∧ yn ↓ in the antecedent is a group. A formula ∗i Fi in an
entailment J is called grouping when each Fi is a group of J.
    (Γ1 , Γ2 ) is called group-disjoint if (Roots + Cells)(Γ1 ) ∩ (Roots + Cells)(Γ2 ) = ∅.
    (Φ1 , Φ2 ) is called a group split by (Γ1 , Γ2 ) if (Roots + Cells)(Γi ) = (Roots + Cells)(Φi ) for i = 1, 2.
A variable group is the set of address variables that belong to some single ∆ in the antecedent. A group
is a ∗-conjunction of formulas whose address variables are in a single group. (Γ1 , Γ2 ) is group-disjoint
when their address variables are disjoint. (Φ1 , Φ2 ) is a group split by (Γ1 , Γ2 ) when they are split by their
address variables according to variable groups of Γ1 , Γ2 .
                                                 →
                                                 −                       →
                                                                         −
    For a set V of variables, we define |P1 (t1 , t 1 ), . . . , Pn (tn , t n )|V as |{t1 , . . . , tn } − V |.
Definition 10.2 (Normal Form) For a given set V0 of variables and a given number d, an entailment
J is called normal with (V0 , d) if J is of the form Y ↑ ∧Π ∧ Γ ⊢ {Φi | i ∈ I} and Φi is of the form
∃−
 →
 x i ∃−
      →
      y i ⇑ (Πi ∧ Γi ) and by letting V be FV(J),
  1. Γ is a single group (single group condition),
  2. Y + (Roots + Cells)(Γ) = V (variable condition),
  3. Roots(Φi ) is defined (disjunct root condition),
  4. (Roots + Cells)(Γ) = (Roots + Cells)(Φi ) for every i ∈ I (group condition),
              →
              −                              →
                                             −
  5. if P (x, t ) ∧ y ↓ in Φi , then y ∈ t (disjunct definedness condition),
  6. −
     →x i ⊆ Cells(Γi ) (disjunct existential condition),
     →
     −
  7. y i ⊆ FV(Γi ) (unrelated existential condition),
  8. Π is (6= (V )) (equality condition),
  9. Πi is (6= (− x i−
                  →  →          x i−
                     y i , V + {−
                                →  →y i , nil})) (disjunct equality condition),
 10. if i 6= j, then Φi 6≡ Φj θ for all variable renaming θ such that Dom(θ)∩FV(Γ) = ∅ (disjunct renaming
     condition),
 11. FV(Y, Π) ⊆ FV(Γ, (Φi )i ) (antecedent variable condition),
      →
      −                                            →
                                                   −
 12. | Q |V0 ≤ d for every predicate symbol Q —∗s P in J (wand condition).

                                                       17
10.2     Definition of Algorithm
                                →
                                −                                                  →
                                                                                   −                         →
                                                                                                             −
For a given entailment A ⊢ B , our algorithm calls the function Main(A ⊢ B ) to decide whether A ⊢ B
                                                  →
                                                  −                                        →
                                                                                           −
is valid or not. If it returns Yes, then A ⊢ B is valid. If it return No, then A ⊢ B is not valid. The
function Main calls MainLoop, which may fork, namely, it copies itself and produces new processes. The
function Main waits all these processes to terminate or fail.
    Let kmax be the maximum arity for predicate symbols in the original language.
    For sets T, T ′ of terms, we define (=6= (T, T ′ )) as the set of conjunctions of all combinations of t = u
or t 6= u for t ∈ T, u ∈ T ′ . We define (=6= (T )) as (=6= (T ∪ {nil}, T ∪ {nil})). We write (Dom ∪ Range)(f )
for Dom(f ) ∪ Range(f ).
    We say we apply a rule to a computation step when the input to the step is the conclusion of the rule
and the output of the step are the assumptions of the rule.
    All the functions are defined below. We describe functions in codes and then describe the same
functions again in English for explanation. The algorithm of satisfiability check is given in Section 9.
                        →
                        −
function Main(A ⊢ B )
                   →
                   −
   let J be A ⊢ B .
   let V be FV(J).
                      →
                      −
   let Π ∧ ∗i Pi (xi , t i ) be A.
   K := {(Y, (Xi )i ) | Y + Σi Xi + {xi }i = V }.
   for each (Y, (Xi )i ) in K do
                                    →
                                    −                 →
                                                      −
      J := (Y ↑ ∧Π ∧ ∗i (Pi (xi , t i ) ∧ Xi ↓) ⊢ B ).
                           →
                           −
      let (Bj )j∈J ′ be B .
      let X be Roots(A) + Σi Xi .
      K ′′ := {((Xj,x )x∈Roots(Bj ) )j∈J ′ | j ∈ J ′ , Roots(Bj ) + Σx∈Roots(Bj ) Xj,x = X}.
      for each ((Xj,x )x∈Roots(Bj ) )j∈J ′ in K ′′ do
                                     →
                                     −
          let ψ ⊢ (Πj ∗ ∗i Pji (xji , t ji ))j∈J ′ be J.
          J := (ψ ⊢ (Πj ∗ ∗i (Pji (xji , −
                                         → t ji ) ∧ Xj,xji ↓))j∈J ′ ).
            ′
          K := (=6= (V )).
          for each Π1 in K ′ do
                        →
                        −
              let ψ ⊢ ψ be J.
                                 →
                                 −
              J := Π1 ∧ ψ ⊢ ψ .
                        →
                        −
              let ψ ⊢ ψ be J.
              if ψ unsat then continue
              if ψ is V ↑_   ∧Π ∧ emp then
                                                   −
                                                   →
                  if Π → {Π′ | Π′ ∧ emp ∈ ψ } is true then continue
                  else fail
              end if S
              let V be           → Cells(ψi ).
                                 −
                             ψi ∈ ψ
              let dwand be kmax .
              MainLoop({J, V, dwand ) /* MainLoop will produce some processes */
              Wait either of the following cases happens.
              if some process produced by MainLoop terminates without fail then continue
              if every process produced by MainLoop fails then return No
          end for
      end for
   end for
   return Yes
end function
function MainLoop(J, V, d)
 /* J an entailment to prove, d the maximum depth of wands. V the set of cell variables. */
   S := {(J, ∅)}.
   while S 6= ∅ do
      /* S a set of pairs of a subgoal J and a history H.
      J and elements in H are normal forms except the initial entailment. */
      For each (J, H) ∈ S, copy the current process and continue the computation
      (namely, the current process becomes |S| processes by fork).
      S := S − {(J, H)}.
      if there are some J ′ ∈ H and θ such that J ′ θ ≡ J then continue



                                                      18
      H := H + {J}
                 →
                 −
      let ψ ⊢ Φ be T    J.
      if Roots(ψ) ∩ i Roots(Φi ) = ∅ then
           Choose y ∈ Roots(ψ). /* There may be choices only for the first loop */
                     →
                     −        →
                              −
           let ψ ⊢ Φ , Φ[P ( t ) ∧ y ↓] be J.
                                      →
                                      −
           J := Factor(V, d, (ψ ⊢ Φ , Φ[ ]), P (−
                                                →t ), y).
      end if
      S ′ := Unfold(J).
      for each J in S ′ do
                                            →
                                            −                      →
                                                                   −
           /* Case analysis */ let ψ ⊢ F be J. S ′′ := {Π ∧ ψ ⊢ F | Π ∈ (=6= (FV(J)))}.
                              ′′
           for each J in S do
                                              →
                                              −
               /* Unsat check */ let ψ ⊢ F be J. if ψ unsat then continue
               J := Match(J)
               /* In emp case. Termination Check */
               if ψ ≡ Y ↑ ∧Π ∧ emp then
                                                 →
                                                 −
                   if some ∃− →
                              w ⇑ (Π′ ∧ emp) ∈ F then continue /* Π′ has only w 6= t */
                   fail
               end if
               G := Split(J, V, d)
               For each S ′′′ ∈ G, copy the current process and continue the computation
               (namely, the current process becomes |G| processes by fork).
               for each J in S ′′′ do
                   J := Normalize(J)
                   S := S ∪ {(J, H)}.
               end for
           end for
      end for
   end while
end function
function Factor(V, d, J[ ], P ′ (− →t ), y)
            ′ −
              →             ′
   /* J[P ( t ) ∧ y ↓]. P is in the extended language. */
   /* (1) Factor */
              →
              −
   let F ⊢ G , G[ ] be J[ ].
       −−−   →                                                       →
                                                                     −
   let Q(− →t )—∗s P (− →
                        t ) be P ′ (−
                                    →t ) where the predicate symbols Q , P are in the original language.
   Apply the following rule (BoundedFactor) to J.
                        →
                        −              −−−−  −→                              −−−− −→
         x 6= y ∧ F ⊢ G , {G[∃−   →w ((Q1 (−→
                                            t 1 ), Q(y, −
                                                        →            t )) ∗ (Q2 (−
                                                        w )—∗s P (x, −
                                                                     →           →
                                                                                 t 2 )—∗s Q(y, −
                                                                                               →
                                                                                               w )))] |
           −−−−−−→ −−−−
               →          →
                          −−→        → −
                                     −   →                    →
                                                              −
         {Q1 ( t 1 ), Q2 ( t 2 )} = { Q ( t )}, Q ∈ Dep(P ), Q 2 ⊆ Dep(Q),
          −−−−→
              −−→                       −−−− →
                                             −−→
         |Q1 ( t 1 ), Q(y, −
                           →
                           w )|V ≤ d, |Q2 ( t 2 )|V ≤ d, −→w fresh}
                                                    −−− →                                        (BoundedFactor)
                                            →
                                            −         →
                                                      −             →
                                                                    −
                             x 6= y ∧ F ⊢ G , G[(Q( t )—∗s P (x, t )) ∧ y ↓]

   /* (2) Name Case Analysis */
                          −−−−  →
                                −−→                             →
                                                                −       −−−−→
                                                                            −−→                               −
                                                                                                              →
   let ψ ⊢ F ′ [∃w−   →
                      w ((Q1 ( t 1 ), Q(y, − →
                                             u 1 w−
                                                  →u 2 )—∗s P ( t )) ∗ (Q2 ( t 2 )—∗s Q(y, −  →
                                                                                              u 1 w−→
                                                                                                    u 2 )))], F be J.
   let V be FV(J).
                   −−−−  −→
   let F [ ] be (Q1 (−  →t 1 ), Q(y, −
                                     →       u 2 )—∗s P (−
                                      u 1 [ ]−
                                             →           →t )).
                   −−−− →
                        −−→        s      →
                                          −      →
                                                 −
   let G[ ] be (Q2 ( t 2 )—∗ Q(y, u 1 [ ] u 2 )).
                                                                                                                           −
                                                                                                                           →
   J := (ψ ⊢ F ′ [∃w−   →
                        w (w 6= V ∪ {nil} ∧ (F [w] ∧ w ↓) ∗ G[w])], {F ′ [∃−       →
                                                                                   w (F [t] ∗ G[t])] | t ∈ V ∪ {nil}}, F ).
   Do this for each ∃w produced by the previous step.
   return J
end function
function Unfold(J)
   /* (1) Unfold L and R */
              →
              −
   let ψ ⊢ F be J.                T
   Choose x ∈ Roots(ψ) ∩ i Roots(Fi ).
                         → →
                         −                               →
                                                         −
   S ′ := {ψ ′ ∗ (A(x, t , −   z ) ∧ X ↓) ⊢ {Fi [φi (x, t i )] |
                       →
                       −
   Fi [Pi (x, t i )] ∈ F , φi (x, t i ) is a definition clause of Pi (x, −
              →
              −                    →
                                   −                                       →t i ) if P is Pi , φi (x, −
                                                                                                      →
                                                                                                      t i ) is Pi (x, −
                                                                                                                      →
                                                                                                                      t i ) if Pi is 7→}
                    ′           →
                                −
          | ψ ≡ ψ ∗ (P(x, t ) ∧ X ↓),
                    → →
                    −                                           →
                                                                −                      → →
                                                                                       −                  −
                                                                                                          →
         ∃−→z A(x, t , − z ) is a definition clause of P (x, t ) if P is P , A(x, t , −      z ) is P(x, t ) if P is 7→, −   →z fresh}.
   /* (2) Left Definedness Distribution */


                                                                   19
                                                →
                                                −
   while ψ ∗ ((Π ∧ ∗i∈I Pi (xi )) ∧ X ↓) ⊢ F is in S ′ and |I| > 1 and X 6= ∅ do
         ′      ′                                         →
                                                          −                                     −
                                                                                                →
       S := S − {ψ ∗ ((Π ∧ ∗i∈I Pi (xi )) ∧ X ↓) ⊢ F } + {ψ ∧ Π ∗ ∗i (Pi (xi ) ∧ Xi ↓) ⊢ F | Σi (Xi + {xi }) = X}.
   end while
   return S ′
end function
function Match(J)
   /* (1) Equality Elimination */
                                    →
                                    −
   let x = t ∧ X ↑ ∧Π ∧ Γ ⊢ F be J.
   J := ((X[x := t] − {nil}) ↑ ∧Π[x := t] ∧ Γ[x := t]
           →
           −
         ⊢ F [x := t])
   Repeat this until the antecedent does not contain =.
   /* (2) Match */
                           → →
                           −
   let ψ ∗ x 7→ (−  →u ) ⊢ F , ∃−z (F ∗ x 7→ (−→
                                               v )) be J.
                              → →
                              −
   J := (ψ ∗ x 7→ ( u ) ⊢ F , ∃−
                       →
                       −            z (F ∗ x 7→ (−
                                                 →v)∧−  →
                                                        u =−   →v )).
                               →
                               −
   Do this for each x 7→ ( v ) in the succedent.
   /* (3) Existential Instantiation */
            → →
            −
   let ψ ⊢ F , ∃−   z z(z = t ∧ F ) be J.
               → →
               −
   J := (ψ ⊢ F , ∃−    z F [z := t]).
   Repeat this until this cannot apply anymore.
   /* (4) Unmatch Disjunct Elimination */
            →
            −
   let ψ ⊢ F , t = u ∧ F be J.
                                  →
                                  −
   if t ≡ u then J := (ψ ⊢ F , F )
                      →
                      −
   else J := (ψ ⊢ F )
   Do this for each = in the succedent.
   /* (5) Disequality Elimination */
            →
            −
   let ψ ⊢ F , t 6= u ∧ F be J.
                                  →
                                  −
   if t ≡ u then J := (ψ ⊢ F )
                      →
                      −
   else J := (ψ ⊢ F , F )
   /* (6) Emp Disjunct Elimination */
            →
            −
   let ψ ⊢ F , F be J.
                                                                             →
                                                                             −
   if F is ∃→−x ∃−→y ⇑ (Π ∧ emp ∧ X ↓) and X 6= ∅ then J := (ψ ⊢ F )
   Do this for each disjunct.
   /* (7) Unleaf Elimination */
             →
             −
   let G ⊢ F , F be J.
                                                                             →
                                                                             −
   if F contains x 7→ (−    →
                            u ) ∧ w ⇑ and w ∈ −  →u then J := (G ∧ Γ ⊢ F )
   Do this for each disjunct.
   /* (8) 7→ Removal */
   let ψ ∗ x 7→ (−  →u ) ⊢ (∃−→
                              w i (Fi ∗ x 7→ (−
                                              →
                                              v )))i be J.
                         →
                         −
   J := (x ↑ ∧ψ ⊢ (∃ w i Fi )i ).
   return J
end function
function Split(J, V, d)
   /* (1) Extra Definedness */
            →
            −
   let ψ ⊢ F , F be J.
                                                                     →
                                                                     −
   if z ∈ Roots(ψ) − (Roots + Cells)(F ) then J := (ψ ⊢ F , F ∧ z ↓).
   Repeat this until there is not z ∈ Roots(ψ) − (Roots + Cells)(F ).
   while true do
       /* (2) Right Definedness Distribution */
                  →
                  −                                     →
                                                        −
       let ψ ⊢ F , F [∃−  →
                          x ∃− →
                               y ⇑ (Π ∧ F ∗ (∗i Pi (xi , t i ) ∧ X ↓))] be J.
                    →
                    −
       J := (ψ ⊢ F , {F [∃−   →x ∃−y ⇑ (Π ∧ F ∗ ∗i (Pi (xi , −
                                   →                         →t i ) ∧ Xi ↓))] | X = Σi Xi }).
                                                        →
                                                        −
       Repeat this until the succedent becomes Φ .
       /* (3) Disjunct Grouping */
                     →
                     −             →
                                   −
       if J is ψ ⊢ Φ , Φ[P (x, t ) ∧ y ↓] and x and y are in different groups then
                                       →
                                       −
           J := Factor(V, d, (ψ ⊢ Φ , Φ[ ]), P (x, − →t ), y).
       else break
       end if
   end while
   /* (4) Existential Disequality */
   /* We have 6= for every variable except −       →z. −
                                                       →x 6= − →
                                                               z from the antecedent. −   →
                                                                                          y 6= −
                                                                                               →
                                                                                               z from −
                                                                                                      →
                                                                                                      y ↑ and −
                                                                                                              →
                                                                                                              z ↓. */
            → −
            −      →    →
                        −
   let ψ ⊢ Φ , ∃ x ∃ y ⇑ (Π ∧ ∗i Γi ) be J where ∗i Γi is grouping.



                                                          20
              → → −
              −
   J := (ψ ⊢ Φ , ∃−x ∃→ y ⇑ ((6= (−
                                  →
                                  x−→y , FV(∗i Φi ) ∪ {nil})) ∧ Π ∧ ∗i Γi )).
   /* (5) Unrelatedness Introduction */
           →
           − → −
   let ψ ⊢ Φ , ∃−
                x ∃→ y ⇑ (Π ∧ (∆ ∧ x ↓) ∗ ∗i Γi ) be J where (∆ ∧ x ↓) ∗ ∗i Γi is grouping.
              → → −
              −
   J := (ψ ⊢ Φ , ∃−x ∃→ y ⇑ (Π ∧ (∆ ∧ x ↓) ∗ ∗i (Γi ∧ x ⇑))).
   Do this for each x ↓.
   /* (6) Existential Split */
           → → −
           −
   let ψ ⊢ Φ , ∃−
                x ∃→ y ⇑ (Π ∧ ∗i Γi ) be J where ∗i Γi is grouping.
              →
              −
   J := (ψ ⊢ Φ , ∗i ∃−
                     →x ∃−
                         →y ⇑ (Π ∧ Γi )).
   /* (7) (∗)-Split */
   Repeatedly apply the following rule (Split) to J until the antecedent becomes a single group in order to
generate a set G of sets of subgoals.
       (Y ∪ Y1 ) ↑ ∧Π ∧ Γ2 ⊢ {Φ2i |i ∈ I − I ′ } or (Y ∪ Y2 ) ↑ ∧Π ∧ Γ1 ⊢ {Φ1i |i ∈ I ′ }   (∀I ′ ⊆ I)
                                                                                                         (Split)
                               Y ↑ ∧Π ∧ Γ1 ∗ Γ2 ⊢ {Φ1i ∗ Φ2i |i ∈ I}

   where
       V = FV(Y ↑ ∧Π ∧ Γ1 ∗ Γ2 ⊢ {Φ1i ∗ Φ2i |i ∈ I}),
       Yi = (Roots + Cells)(Γi ) (i = 1, 2),
       Π ≡ (6= (V )),
       (Roots + Cells)(Γ1 ∗ Γ2 ) + Y = V,

   (Γ1 , Γ2 ) is group-disjoint, and (Φ1i , Φ2i ) (i ∈ I)) is group split by (Γ1 , Γ2 ).
   return G
end function
function Normalize(J)
   /* (1) Fresh Variable Disjunct Elimination */
                        →
                        −
   let X ↑ ∧Π ∧ Γ ⊢ Φ , Φ, Φ′ be J.
   if θ is a variable renaming, Φ′ ≡ Φθ, (Dom ∪ Range)(θ) ⊆ X, (Dom ∪ Range)(θ) ∩ FV(Γ) = ∅ then
                              →
                              −
       J := (X ↑ ∧Π ∧ Γ ⊢ Φ , Φ)
   end if
   Repeat this until it cannot apply.
   /* (2) Unnecessary Disequality Elimination */
                                 →
                                 −
   let X ↑ ∧x 6= t ∧ Π ∧ Γ ⊢ Φ be J.
                   →
                   −                                 →
                                                     −
   if x ∈/ FV(Γ, Φ ) then J := (X ↑ ∧Π ∧ Γ ⊢ Φ )
   Repeat this until it cannot apply.
   /* (3) Unnecessary Variable Elimination */
                              →
                              −
   let x ↑ ∧X ↑ ∧Π ∧ Γ ⊢ Φ be J.
                   →
                   −                                  →
                                                      −
   if x ∈/ FV(Γ, Φ ) then J := (X ↑ ∧Π ∧ Γ ⊢ Φ )
   Repeat this until it cannot apply.
   /* (4) Unnecessary Unrelated Existential Elimination */
             → → −
             −
   let ψ ⊢ Φ , ∃−  x ∃y →
                        y ⇑ (Π ∧ Γ) be J.
   if y ∈/ FV(Γ) then
       Remove y 6= t in Π to obtain Π′ .
                    → → −
                    −
       J := (ψ ⊢ Φ , ∃−  x ∃→
                            y ⇑ (Π′ ∧ Γ))
   end if
   Repeat this until it cannot apply.
   return J
end function
    For explanations of these functions we give their English descriptions except Mainloop below.
                       →
                       −
function Main(A ⊢ B )
    1. In the antecedent A, consider cases by classifying all the free variables except the roots into Y ↑ and
Xi ↓ for each atomic spatial formula Pi (xi ), and in each case, add Y ↑ ∧ and Xi ↓ ∧ to the ∗-conjunct
Pi (xi ), and do the following.
                                              →
                                              −
    2. In each disjunct of the succedent B , consider cases by classifying the address variables of the
antecedent into Xi and xi for each atomic spatial formula Qi (xi ), and in each case, generate a new
disjunct by adding Xi ↓ ∧ to the ∗-conjunct Qi (xi ), and do the following.
    3. Consider cases by = and 6= for all the variables and nil, and in each case, add Π1 ∧ to the antecedent
where Π1 is the conjunction of these = and 6=, and do the following.
    4. If the antecedent is unsatisfiable, finish this case.


                                                           21
    5. If the spatial part of the antecedent is emp, do the following. If there is some disjunction whose
spatial part is emp and pure part is included in the pure part of the antecedent, finish this case. Otherwise
stop with fail.
    6. Let J be the entailment. Let V be the union of Cells for each disjunct in the succedent. Let dwand
be kmax . Call MainLoop({J, V, dwand ). MainLoop may fork and process several processes. Wait either
of the following cases happens: If some process terminates without fail, finish this case; If every process
fails, stop with No.
    7. If all the cases are finished, stop with Yes.
end function
                                  →
                                  −
function Factor(V, d, J[ ], P ′ ( t ), y)
                                  →
                                  −               →
                                                  −       −−−
                                                            →
                                                            −→         →
                                                                       −                                −
                                                                                                        →
    1. Factor. Let J[ ] be F ⊢ G , G[ ]. Let P ′ ( t ) be Q( t )—∗s P ( t ) where the predicate symbols Q , P
are in the original language. Apply the following rule (BoundedFactor) to J.
                      →
                      −              −−−− →
                                          −−→                     −
                                                                  →        −−−−→
                                                                               −−→
       x 6= y ∧ F ⊢ G , {G[∃−    →
                                 w ((Q1 ( t 1 ), Q(y, −
                                                      →
                                                      w )—∗s P (x, t )) ∗ (Q2 ( t 2 )—∗s Q(y, →
                                                                                              −
                                                                                              w )))] |
         −−−−→
             −−→    −−− −
                        →
                        −−→        →−
                                   −   →                    →
                                                            −
       {Q1 ( t 1 ), Q2 ( t 2 )} = { Q ( t )}, Q ∈ Dep(P ), Q 2 ⊆ Dep(Q),
        −−−−−
            →−→                       −−−− →
                                           −−→
       |Q1 ( t 1 ), Q(y, −
                         →
                         w )|V ≤ d, |Q2 ( t 2 )|V ≤ d, −→w fresh}
                                                   −− −→                                          (BoundedFactor)
                                           →
                                           −          →
                                                      −            →
                                                                   −
                            x 6= y ∧ F ⊢ G , G[(Q( t )—∗s P (x, t )) ∧ y ↓]

   2. Name Case Analysis. For each ∃w generated in the step 1, do the following. Let V1 be the union
of the set of free variables in J and the set of bound variables whose scopes include this ∃w. Generate
disjuncts by classifying cases by = and 6= between each element in V1 ∪ {nil} and w. If a disjunct has
w = t, eliminate ∃w by substituting w := t in the disjunct. If a disjunct has w 6= V1 ∪ {nil}, add w ↓ ∧
   −−−− →
        −−→                   →
                              −
to Q1 ( t 1 ), Q(y, −
                    →
                    w )—∗s P ( t ) in the disjunct.
   3. Return the entailment.
end function
function Unfold(J)
   1. Unfold L and R. In the entailment J, choose a common root x among the antecedent and all
disjuncts of the succedent.
   Generate a set of subgoals by replacing P (x) in the antecedent by formulas obtained from the definition
clauses of P (x) by removing ∃−   →
                                  z and replacing − →
                                                    z by fresh variables, if P (x) is in the antecedent. In each
entailment in the subgoal set, replace Q(x) by each definition clause of Q(x) to generate new disjuncts,
if Q(x) in the disjunct.
   2. Left Definedness Distribution. In the antecedent of each subgoal entailment J in the subgoal set,
consider cases of distributing ∧x ↓ to spatial atomic formulas, and replace J by new subgoals generated
from these cases.
   3. Return the subgoal set.
end function
function Match(J)
   1. Equality Elimination. In the entailment J, if the antecedent has x = t, eliminate it by substitution
x := t.
   2. Match. If the antecedent has x 7→ (−    →
                                              u ) and a disjunct in the succedent has x 7→ (− →
                                                                                              v ), add −
                                                                                                       →u =−→
                                                                                                            v∧
          →
          −
to x 7→ ( v ).
   3. Existential Instantiation. If the succedent has ∃z(z = t ∧ . . .), eliminate ∃z by substitution z := t.
   4. Unmatch Disjunct Elimination. If the succedent has t = t, remove it. If a disjunct of the succedent
has t = u and t 6≡ u, remove the disjunct.
   5. Disequality Elimination. If a disjunct of the succedent has t 6= t, remove the disjunct. If the
succedent has t 6= u and t 6≡ u, remove t 6= u.
   6. Emp Disjunct Elimination. If a disjunct of the succedent has emp ∧ t ↓, remove this disjunct.
   7. Unleaf Elimination. If a disjunct of the succedent has x 7→ (−      →u ) ∧ ui ⇑ and ui ∈ −  →
                                                                                                  u , remove the
disjunct.
   8. 7→ Removal. If the antecedent and all the disjuncts of the succedent have x 7→ ( ), remove these
x 7→ ( ) and add x ↑ ∧ to the antecedent.
   9. Return the entailment.
end function


                                                       22
function Split(J, V, d)
    1. Extra Definedness. For each root z of the antecedent and each disjunct F of the succedent, if
z∈ / (Roots + Cells)(F ), add z ↓ ∧ to F . Repeat this until there are not such z and F .
    2. Right Definedness Distribution. In each disjunct in the succedent of the entailment J, consider
cases of distributing ∧x ↓ to spatial atomic formulas, and replace the original disjunct by all the disjuncts
generated from these cases.
                                                          →
                                                          −
    3. Disjunct Grouping. If some disjunct has P (x, t ) ∧ y ↓ and x and y are in different groups, by
                                →
                                −          −
                                           →                            →
                                                                        −              →
                                                                                       −
letting the entailment be ψ ⊢ Φ , Φ[P (x, t )], call Factor(V, d, (ψ ⊢ Φ , Φ[ ]), P (x, t ), y). Then go to the
step 2.
    4. Existential Disequality. In each disjunct, add w 6= z∧ to the ∃-body for each w, z such that the
disjunct has ∃w and z is a fresh variable introduced by the function Unfold.
    5. Unrelatedness Introduction. Replace each disjunct ∃−    →
                                                               x (Π∧(Φ∧x ↓)∗∗i Φi ∧Y ⇑) by ∃−    →x (Π∧(Φ∧x ↓
) ∗ ∗i (Φi ∧ x ⇑)) ∧ Y ⇑, where (Φ ∧ x ↓) ∗ ∗i Φi is grouping.
    6. Existential Split. Replace each disjunct ∃− →x (Π ∧ ∗i Φi ∧ Y ⇑) by ∗i ∃−
                                                                               →
                                                                               x (Π ∧ Φi ∧ Y ⇑).
    7. (∗)-Split. Apply the following rule (Split) repeatedly to generate the subgoal set G until the spatial
part of the antecedent in every entailment becomes atomic.
        (Y ∪ Y1 ) ↑ ∧Π ∧ Γ2 ⊢ {Φ2i |i ∈ I − I ′ } or (Y ∪ Y2 ) ↑ ∧Π ∧ Γ1 ⊢ {Φ1i |i ∈ I ′ } (∀I ′ ⊆ I)
                                                                                                      (Split)
                                Y ↑ ∧Π ∧ Γ1 ∗ Γ2 ⊢ {Φ1i ∗ Φ2i |i ∈ I}
where
        V = FV(Y ↑ ∧Π ∧ Γ1 ∗ Γ2 ⊢ {Φ1i ∗ Φ2i |i ∈ I}),
        Yi = (Roots + Cells)(Γi ) (i = 1, 2),
        Π ≡ (6= (V )),
        (Roots + Cells)(Γ1 ∗ Γ2 ) + Y = V,

(Γ1 , Γ2 ) is group-disjoint, and (Φ1i , Φ2i ) (i ∈ I)) is group split by (Γ1 , Γ2 ).
   8. Return G.
end function
function Normalize(J)
                                                                                               →
                                                                                               −
   1. Fresh Variable Disjunct Elimination. If the entailment J has the form X ↑ ∧Π ∧ Γ ⊢ Φ , Φ, Φ′ and
                                               ′
there is a variable renaming θ such that Φ ≡ Φθ, (Dom∪Range)(θ) ⊆ X, and (Dom∪Range)(θ)∩FV(Γ) =
∅, then remove Φ′ .
   2. Unnecessary Disequality Elimination. If x does not occur in neither the spatial part and ↓ of the
antecedent or the succedent, then remove x 6= t in the antecedent.
   3. Unnecessary Variable Elimination. If x does not occur in neither the spatial part and ↓ of the
antecedent or the succedent, then remove x ↑ in the antecedent.
   4. Unnecessary Unrelated Existential Elimination. If y does not occur in the spatial part in a disjunct
with ∃y ⇑, remove ∃y ⇑ and y 6= t in the disjunct.
   5. Return the entailment.
end function
                                →
                                −
    When an entailment A ⊢ B is given to Main, we generate subgoals by putting ↓ and ↑ of all the free
variables to the antecedent with all the cases, putting ↓ of all the address variables in the antecedent to
the succedent with all the cases, putting = and 6= of all the variables with nil to the antecedent with all
cases, check satisfiability, and send the subgoal set to the function MainLoop. MainLoop may fork and
produce several processes. If for some subgoal every process of MainLoop fails, the function Main returns
No. If for all subgoals some process of MainLoop terminates without fail, the function Main returns Yes.
    MainLoop first checks whether the current subgoal appeared already. If so, we finish this subgoal and
go to the next subgoal. Secondly MainLoop calls Factor to create common roots on both sides when there
is no common root. In order to find a common root such that the bounded factor rule for it is locally
complete, the function MainLoop forks and produces new processes with each common root. When there
is a common root x, MainLoop first unfolds the predicate of form P (x) on both sides (the function
Unfold). Next it forces match of them on both sides by putting equalities on the succedent and removes
x 7→ ( ) on both sides (the function Match). Then MainLoop checks termination condition when the
antecedent is emp. Then MainLoop splits ∃-scopes. Then we split separating conjunctions until every
entailment become a single group (the function Split). For each rule instance of (Split), MainLoop forks

                                                       23
and produces new processes to compute this case, and executes these processes nondeterministically. Then
MainLoop transforms subgoals into normal forms and goes to the first step of the function MainLoop.
The function MainLoop does this loop until the subgoal set becomes empty.

10.3    Partial Correctness of Algorithm
We can show the correctness of the algorithm when it terminates with Yes. We will show the case with
No in the completeness proof later.

Lemma 10.3 (Partial Correctness) If the algorithm terminates with Yes, then the input entailment
is provable.

    Proof. When the algorithm terminates with Yes, for each subgoal there is some process that terminates
without fail.
    For the input goal, the function Main generates subgoals for it. For each subgoal, the function Main-
Loop constructs its proof when it terminates without fail. In the while loop of the function MainLoop,
for each subgoal (J, H) ∈ S, the function MainLoop proves J by using H as companions.
    We can show that each step of the algorithm consists of applications of inference rules as follows. We
consider each step of each function.
    Function Main.
    Case analysis by (Y, (Xi )i ). By the rules (Case L) and (↓ Out L).
    Case analysis by K ′′ . By (∧Elim) and (↓ Out).
    Case analysis by K ′ : By rule (Case L).
    Unsatisfiability check. By (Unsat).
    Termination check: By (emp), (∧L), (∧R), (∨R).
    By MainLoop, each subgoal J is provable.
    Function MainLoop.
    If MainLoop terminates without fail for the input {(J, H)}, J is provable by using H as companions.
    We use rule (Subst) from J ′ to J and discharge J as a bud with the companion J ′ ∈ H. Since H is
the set of judgments from the root to the previous subgoal, the step for J ′ ∈ H and J ′ θ = J in MainLoop
gives a bud-companion relation.
    Case Analysis: By rules (Case L).
    Unsat Check: By rule (Unsat).
    Termination Check: By (emp), (⇑ R), (∧L), (∨R).
    Function Factor. We show the input formula is derived from the output formula.
    (1) Factor. By Lemma 5.2.
    (2) Name Case Analysis. By the rules (∧Elim) and (∃R).
    Function Unfold. We show that J is derivable from S ′ .
    (1) Unfold L and R. By the rules (Pred L) and (Pred R).
    (2) Left Definedness Distribution. By (↓ Out L).
    Function Match. We show the input formula is derived from the output formula.
    (1) Equality Elimination. By the rule (= L).
    (2) Match. By the rule (∧Elim).
    (3) Existential Instantiation. By the rules (= R) and (∃R).
    (4) Unmatch Disjunct Elimination. By the rules (= R) and (∨R).
    (5) Disequality Elimination. By (∧R), (∨R).
    (6) Emp Disjunct Elimination. By the rule (∨R).
    (7) Unleaf Elimination. By the rule (∨R).
    (8) 7→ Removal. By the rule (∗ 7→).
    Function Split. We show that J is derived from any subgoal set in S.
    (1) Extra Definedness. By (↓ R).
    (2) Right Definedness Distribution. By the rule (↓ Out R).
    (3) Disjunct Grouping. By Factor.
    (4) Existential Disequality. By the rule (∧Elim).
    (5) Unrelatedness Introduction. By the rule (∧Elim).
    (6) Existential Split. Use (∃Amalg2) for − →x and (∃Amalg1) for −→
                                                                     y ⇑.


                                                   24
   (7) (∗)-Split. The rule (Split) is derivable from the rule (∗) and (↑ Elim).
   Function Normalization. We show that the input formula is derived from the output formula.
   (1) Fresh Variable Disjunct Elimination. By the rule (∨R).
   (2) Unnecessary Disequality Elimination. By the rule (∧L).
   (3) Unnecessary Variable Elimination. By the rule (∨L).
   (4) Unnecessary Unrelated Existential Elimination. By (⇑ R).
   We have shown that each step of the algorithm consists of applications of inference rules. Hence the
process produces a proof of the input entailment, when it terminates without fail. Hence the function
Main produces the proof when it returns Yes. ✷

10.4    Loop Invariant
We will use the following loop invariants of the function MainLoop.

Lemma 10.4 Let V, dwand be those in the call of the function MainLoop. At the beginning of the while
loop in the function MainLoop, every entailment (J, H) ∈ S satisfies the following.

  1. J is a normal form with (V, dwand ) except the single group condition, the disjunct equality condition,
     and the disjunct renaming condition.
  2. J is a normal form with (V, dwand ) after the first loop.
  3. the antecedent of J is satisfiable.
  4. Cells(Γ) ⊆ Cells(Γ′ ) where Γ is the spatial part of antecedent in J and Γ′ is that in the initial goal
     given to the function MainLoop.

   Proof.
   1 and 2.
   The single group condition. By the function Split.
   The variable condition. This holds for the initial entailment. New variables are −→z in the function
Unfold, and they are in the roots.
   The disjunct root condition is trivial.
   The group condition. J sent to MainLoop satisfies this condition. New variables −   →z introduced by
Unfold is added to the succedent by the extra definedness step in Split.
   The disjunct definedness condition. By the name case analysis step of Factor.
   The disjunct existential condition. By the name case analysis step of Factor.
   The unrelated existential condition. By the unrelatedness introduction step of Split.
   The equality condition. By case analysis in the function Main.
   The disjunct equality condition. By the existential disequality step of Split.
   The disjunct renaming condition and the antecedent variable condition. By the function Normalize.
   The wand condition. By the function Factor.
   3. By the unsatisfiability check in the functions Main and MainLoop.
   4. The algorithm does not increase Cells(Γ). ✷

10.5    Termination
This subsection shows the termination of the algorithm. First we show the finiteness of the set of normal
forms possibly used in the algorithm. Then we show the termination by using the finiteness.
   Since a normal form during the loop consists of a single group, the number of normal forms up to
variable renaming is proved to be finite.

Lemma 10.5 The set of normal forms with (V0 , d) up to variable renaming is finite.

   Proof.
   d is the maximum depth of wands. Let J be the entailment sent to MainLoop from Main, V be
FV(J), Y ↑ ∧Π ∧ Γ be the antecedent of J, (Φi )i∈I be the succedent of J, c1 be |Cells(Γ)|, kmax be
the maximum arity of original inductive predicates and the 7→ predicate, c4 be the number of original
inductive predicates and the 7→ predicate.


                                                    25
    We will count numbers of normal forms up to variable renaming. We count ⇑ as a single predicate
symbol.
    First the maximum number k1 of arguments for extended inductive predicates and the 7→ predicate
is ≤ kmax (d + 1).
    The number k2 of extended inductive predicates and the 7→ predicate is ≤ cd+1 4   .
    The number k3 of ∗-conjuncts in Γ is 1 by the single group condition.
    The number k4 of arguments in Γ is ≤ k3 k1 + c1 , since the number of arguments for inductive or 7→
predicates is ≤ k3 k1 and the number of arguments for ↓ is ≤ c1 .
    The number k5 of variables in Γ is ≤ k4 .
    The number k6 of ∗-conjuncts in Φi is ≤ k3 + c1 , since P (x) in Φi implies x ∈ (Roots + Cells)(Γ).
    The number k7 of arguments for inductive predicates and 7→ in Φi is ≤ k1 k6 , since the number of
arguments for inductive or 7→ predicates is ≤ k1 and the number of the predicate symbols is ≤ k6 .
    The number k8 of variables in ∃-body of Φi is ≤ k7 .
    The number k9 of disjuncts in the antecedent (namely |I|) is ≤ k2k6 (k8 + 1)k7 22k7 since the number of
combination for inductive predicates and 7→ is ≤ k2k6 , the number of combination for their arguments is
≤ (k8 + 1)k7 (note that +1 for nil), and the number of choice for existentials is ≤ 2k7 for each of −→x and
→
−y ⇑.
    The number k10 of Γ is ≤ k2k3 (k5 + 1)k4 , since the number of combination for predicates is ≤ k2k3 , and
the number of combination for arguments is ≤ (k5 + 1)k4 . (note that +1 for nil.)
    The number k11 of Γ ⊢ (Φ)i∈I is ≤ k10 2k9 , since Y ↑ and Π are determined uniquely by Γ, the number
of the antecedent is ≤ k10 and the number of succedents is ≤ 2k9 . ✷

Lemma 10.6 (Termination) (1) Every process produced by the function MainLoop terminates or fails.
  (2) The algorithm always terminates.

    Proof. (1) Assume some process does not terminate or fail in order to show contradiction. By Lemma
10.5, we have some upper bound n for the number of normal forms. The step H := H + {J} in MainLoop
increases |H|. After the (n + 2)-th execution of the while loop in MainLoop of the process, |H| = n + 2.
Since every element in H except one element is a normal form and they are not equal by variable renaming,
it contradicts.
    (2) By (1). ✷

Proposition 10.7 The algorithm is nondeterministic double exponential time.

   Proof. By the upper bound given by the proof of Lemma 10.5. ✷


11     Constant Store Validity
Definition 11.1 For a bijection β : Locs → Locs, we define
       β(s) = β ◦ s,
       β(h) = β ◦ h ◦ β −1 .

Lemma 11.2 For a formula F in the extended language,
       s, h |= F

and β : Locs → Locs is a bijection, then
       β(s), β(h) |= F.

  Proof.
  First we show:
  Claim 1: the claim holds when F does not contain inductive predicates.
  We can show the claim 1 by induction on F . Every case is straightforward. We show only the case
¬G.
  Case ¬G.



                                                     26
   Assume s, h |= ¬G in order to show β(s), β(h) |= ¬G. Then s, h 6|= G. Hence β −1 (β(s)), β −1 (β(h)) 6|=
G. By IH, β(s), β(h) 6|= G. Hence β(s), β(h) |= ¬G.
   We have proved the claim 1.
   Next we show the claim of the lemma by induction on F . We show only the case of an inductive
predicate. The other cases are proved straightforwardly.
           −
           →
   Case P ( t ).
                     →
                     −                                        →
                                                              −                                            →
                                                                                                           −
   Assume s, h |= P ( t ). We have m such that s, h |= P (m) ( t ). By the claim (1), β(s), β(h) |= P (m) ( t ).
                        →
                        −
Hence β(s), β(h) |= P ( t ). ✷
Definition 11.3 A |=s {Bi |i ∈ I} is defined by
                     _
      ∀h(s, h |= A →   s, h |= Bi ).
                            i∈I

Lemma 11.4 Let Fi , Gji be formulas. If
        Π ⊇ (6= FV(Π, (Fj , Gij )i∈Ij ,j=1,2 )),
        ∀s((Π ∧ F1 |=s {Gi1 |i ∈ I1 }) ∨ (Π ∧ F2 |=s {Gi2 |i ∈ I2 }))
then
        (Π ∧ F1 |= {Gi1 |i ∈ I1 }) ∨ (Π ∧ F2 |= {Gi2 |i ∈ I2 }).
    Proof. Let −
               →
               y = FV((Fj , Gij )i∈Ij ,j=1,2 ).
    Assume
        (Π ∧ F1 |= {Gi1 |i ∈ I1 }) ∨ (Π ∧ F2 |= {Gi2 |i ∈ I2 })
does not hold. Then we have s1 , h1 , s2 , h2 such that
        s1 , h1 |= Π ∧ F1 ,
        s1 , h1 6|= {Gi1 |i ∈ I1 },
        s2 , h2 |= Π ∧ F2 ,
        s2 , h2 6|= {Gi2 |i ∈ I2 }.
                                →
                                −                                                     →
                                                                                      −
Let s1 (−
        →
        y) = −
             →a and s2 (−→
                         y ) = b . Since s1 |= Π and s2 |= Π, we have − →a 6= nil and b 6= nil, −
                                                                                                →
                                                                                                a are
                                         →
                                         −
in Locs and distinct to each other, and b are in Locs and distinct to each other. Take some bijection
β : Locs → Locs such that β(ai ) = bi . Then s2 =−
                                                 y β(s1 ). By Lemma 11.2,
                                                 →

        β −1 (s2 ), β −1 (h2 ) |= Π ∧ F2 ,
        β −1 (s2 ), β −1 (h2 ) 6|= {Gi2 |i ∈ I2 }.
Hence
        s1 , β −1 (h2 ) |= Π ∧ F2 ,
        s1 , β −1 (h2 ) 6|= {Gi2 |i ∈ I2 }.
By taking s to be s1 in the assumption,
        (Π ∧ F1 |=s1 {Gi1 |i ∈ I1 }) ∨ (Π ∧ F2 |=s1 {Gi2 |i ∈ I2 })
    Case 1. Π ∧ F1 |=s1 {Gi1 |i ∈ I1 }. Since
        s1 , h1 |= Π ∧ F1 ,
        s1 , h1 6|= {Gi1 |i ∈ I1 }
we have contradiction.
   Case 2. Π ∧ F2 |=s1 {Gi2 |i ∈ I2 }. Since
        s1 , β −1 (h2 ) |= Π ∧ F2 ,
        s1 , β −1 (h2 ) 6|= {Gi2 |i ∈ I2 }.
we have contradiction.
   Since every case leads to contradiction, we have
        (Π ∧ F1 |= {Gi1 |i ∈ I1 }) ∨ (Π ∧ F2 |= {Gi2 |i ∈ I2 })
✷

                                                         27
12      Cone
Definition 12.1 For a heap h and a ∈ Val, the heap h ⇓ a is defined as h|X where X is the least fixed
point of
        F (X) = ({a} ∩ Dom(h)) ∪ {c ∈ Dom(h)|b ∈ X, b ❀ c}.
b ❀ c denotes (h(b))k = c for some k. We call h ⇓ a a cone of root a in the heap h. For b ∈ h ⇓ a, the
depth of b in h ⇓ a is defined as the least number d such that F d+1 (∅) ∋ b. We write b → c when b ❀ c
and c ∈ Dom(h). We write ։ to the reflexive and transitive closure of →. We write b →tr c ∈ h ⇓ a
when b → c, F d (∅) ∋ b and F d (∅) 6∋ c for some d. We write b →bk c ∈ h ⇓ a when b → c holds and
b →tr c ∈ h ⇓ a does not hold.
    For a heap h, a ∈ Val and S ⊆ Val, the heap h ⇓S a is defined as (h|Dom(h)−(S−{a}) ) ⇓ a, and we call
it a cone of root a with guard S in the heap h.

   We write a ∈ h for a ∈ Dom(h), and h ⊆ h′ for h = h′ |Dom(h) .

Lemma 12.2 (1) If
        s, h |= Γ,
then
             S
        h=     x∈Roots(Γ) h ⇓ s(x).

   (2) If h = h1 + h2 and Γ is Γ1 ∗ Γ2 and for i = 1, 2
        s, hi |= Γi ∧ (FV(Γ) − (Roots + Cells)(Γi )) ↑,
then
               S
        hi =     x∈(Roots+Cells)(Γi ) h ⇓s((Roots+Cells)(Γ)) s(x).

                                       →
                                       −
   Proof. (1) Let Γ be ∗i (Pi (xi , t i ) ∧ Xi ↓). Then we have hi such that h = Σi hi and
                         →
                         −
      s′ , hi |= Pi (xi , t i ) ∧ Xi ↓ .
Hence
        hi ⊆ h ⇓ s(xi ).
Hence
             S
        h⊆     i (h ⇓ s(xi )).

Hence
             S
        h=     x∈Roots(Γ) h ⇓ s(x).

   (2) We write RC for (Roots + Cells) for simplicity.
   By (1),
           S
       h = x∈Roots(Γ) h ⇓ s(x).

Hence
             S
        h=     x∈RC(Γ) h ⇓s(RC(Γ)) s(x).

   We can show
           S
     h1 ⊇ x∈RC(Γ1 ) h ⇓s(RC(Γ)) s(x)

as follows. Assume 6⊇ in order to show contradiction. Then there is a ∈ / h1 and a in the right-hand
side. Hence a ∈ h2 . Hence there is x ∈ RC(Γ1 ) such that a ∈ h ⇓RC(Γ) s(x). Hence there is the path
s(x) ։ a. By going from s(x) to a, take the first h2 -element to be c. Let the previous element be b.

                                                           28
Then s(x) ։ b → c ։ a and s(x) ։ b is in h1 . From s, h1 |= Γ1 and s, h2 |= Γ2 , since b → c is from one
cone to another cone, we have y ∈ FV(Γ) such that c = s(y). Since c ∈ h2 , we have y ∈ RC(Γ2 ), which
contradicts with the path s(x) ։ b → s(y) ։ a in h ⇓s(RC(Γ)) s(x) since y ∈ RC(Γ).
   Similarly we have
            S
       h2 ⊇ x∈RC(Γ2 ) h ⇓s(RC(Γ)) s(x).

Since
                    S
        h1 + h2 =       x∈RC(Γ1 )∪RC(Γ2 ) h ⇓s(RC(Γ)) s(x),

we have
               S
        hi =    x∈RC(Γi ) h ⇓s(RC(Γ)) s(x).

✷

Lemma 12.3 (1) If Γ is Γ1 ∗ Γ2 , and Γ′ is Γ′1 ∗ Γ′2 , and
        h1 + h2 = h′1 + h′2 ,

and for i = 1, 2,
        s, hi |= Γi ∧ (FV(Γ) − (Roots + Cells)(Γi )) ↑,
        s′ , h′i |= Γ′i ∧ (FV(Γ′ ) − (Roots + Cells)(Γ′i )) ↑,
        Roots(Γ′i ) ⊆ (Roots + Cells)(Γi ) ⊆ (Roots + Cells)(Γ′i ),

then hi = h′i for i = 1, 2.
   (2) If
        s, hi |= Γi (i = 1, 2),
        s, h1 + h2 |= Φ1 ∗ Φ2 ,

and (Γ1 , Γ2 ) is group-disjoint, (Φ1 , Φ2 ) is a group split by (Γ1 , Γ2 ), then
        s, hi |= Φi (i = 1, 2).

   Proof. (1) Let Vi be (Roots + Cells)(Γi ) and Vi′ be (Roots + Cells)(Γ′i ) for i = 1, 2. Let V be V1 ∪ V2
and V ′ be V1′ ∪ V2′ . Let h be h1 + h2 .
   By Lemma 12.2 (2),
            S
       h′i = x∈V ′ h ⇓s′ (V ′ ) s′ (x).
                    i


    We can show
    Claim 1: x ∈ V1′ − V1 implies s(x) ∈ h1
    as follows. Assume x ∈ V1′ − V1 . Then x ∈ Cells(Γ′1 ). Then s(x) ∈   / s(V ) since s(x) ∈ s(V2 ) implies
s(x) ∈ s(V2′ ), which contradicts with x ∈ V1′ . Moreover there is y ∈ Roots(Γ′1 ) such that P (y) ∧ x ↓ is
in Γ′1 . Hence there is a path s(y) ։ s(x) in h′1 . By going from s(y) to s(x), take s(z) to be the last
s(V )-element. Then z ∈ V and s(y) ։ s(z) → a ։ s(x) and a ։ s(x) are not in s(V ). Then z ∈ V1
since z ∈ / V1 implies z ∈ V2 and z ∈ V2′ from V2 ⊆ V2′ , so s(z) ∈ h′2 , which contradicts with s(z) ∈ h′1 .
Hence s(x) ∈ h ⇓s(V ) s(z). By Lemma 12.2 (3),
              S
         h1 = x∈V1 h ⇓s(V ) s(x).

Hence h1 ∋ s(x). We have shown the claim 1.
   We will show
   Claim 2: h ⇓s(V ′ ) s(x) ⊆ h1 for any x ∈ V1′
   as follows. If x ∈ V1 , then h ⇓s(V ′ ) s(x) ⊆ h ⇓s(V ) s(x) ⊆ h1 . Assume x ∈ V1′ − V1 . By the claim 1,
s(x) ∈ h1 . Hence there is y ∈ V1 such that s(x) ∈ h ⇓s(V ) s(y). Hence h ⇓s(V ′ ) s(x) ⊆ h ⇓s(V ) s(x) ⊆
h ⇓s(V ) s(y) ⊆ h1 . We have shown the claim 2.
   By the claim 2, h1 ⊇ h′1 . Similarly we have h2 ⊇ h′2 . Hence hi = h′i for i = 1, 2.
   (2) Note that the roots are not bound in Φi for i = 1, 2 by the group split.


                                                         29
      We have h′1 + h′2 = h1 + h2 such that
         s, h′i |= Φi .
                                                        →
                                                        −
Let Φi be ∃− →x i ∃−
                   →
                   y i ⇑ (Πi ∧ Γ′i ). Then we have −
                                                   →
                                                   a i , b i such that by letting s′ be s[−
                                                                                          →
                                                                                          x i := −
                                                                                                 →
                                                                                                 a i, −
                                                                                                      →
                                                                                                      y i :=
→
−
b i (i = 1, 2)], we have
         s′ , h′i |= Γ′i .
By (1), hi = h′i . ✷


13       Local Completeness of Rule (BoundedF actor) in Algorithm
A rule is defined to be locally complete if all its assumptions are valid when its conclusion is valid.

Lemma 13.1 Let V, d be the arguments sent to MainLoop from Main. Then, among processes produced
by MainLoop, there is some process in which every use of the rule
                     →
                     −              −−−− →
                                         −−→                     →
                                                                 −        −−−−→
                                                                              −−→
      x 6= y ∧ F ⊢ G , {G[∃−    →
                                w ((Q1 ( t 1 ), Q(y, −
                                                     →
                                                     w )—∗s P (x, t )) ∗ (Q2 ( t 2 )—∗s Q(y, −
                                                                                             →
                                                                                             w )))] |
        −−−−→
            −−→    −−− −
                       →
                       −−→        →−
                                  −   →                    →
                                                           −
      {Q1 ( t 1 ), Q2 ( t 2 )} = { Q ( t )}, Q ∈ Dep(P ), Q 2 ⊆ Dep(Q),
       −−−−−
           →−→                       −−−− →
                                          −−→
      |Q1 ( t 1 ), Q(y, −
                        →
                        w )|V ≤ d, |Q2 ( t 2 )|V ≤ d, −→w fresh}
                                                  −−− →                                          (BoundedFactor)
                                          →
                                          −          →
                                                     −            →
                                                                  −
                           x 6= y ∧ F ⊢ G , G[(Q( t )—∗s P (x, t )) ∧ y ↓]
is locally complete.

    Proof. Assume all the processes use some locally incomplete application of (BoundedFactor), in order
for contradiction.
    Consider the tree of processes where each path represents a process, the nodes are factor nodes and
fork nodes, which represent the application of the bounded factor rule and fork with new processes
respectively, and any process is represented by some path. We cut each path by the first application
of locally incomplete application of the bounded factor rule. By the assumption, each path is cut. By
König’s Lemma, there is the maximum depth of the cut tree. Take a path of the maximum depth and
consider the process represented by this path. Then for every choice for the application of the bounded
factor rule by the process at the cut node is locally incomplete. (Otherwise, by choosing some application
that is locally complete, the path can extend more than the maximum depth, which contradicts.)
    For simplicity, we write v—∗s v ′ for P ′ (v)—∗s P ′′ (v ′ ) for some P ′ , P ′′ . We also write {v1 , . . . , vn }—∗s v
for P1 (v1 )—∗s . . . —∗s Pn (vn )—∗s P (v) for some P, P1 , . . . , Pn . Note that any order of {v1 , . . . , vn } gives
the equivalent inductive predicate by Lemma 5.1.
    Consider this process at the cut node. We write p for this process at the cut node.
    Fix an application of the bounded factor rule in p.
    Since the rule (Factor) without the restriction on depth of wands is locally complete by Lemma 5.3,
                →
                −        →′
                         −                                                                                          →
                                                                                                                    −
we have some Φ , Φ, Φ , Φ′′ , such that the entailment of the cut note is the conclusion ψ ⊢ Φ , Φ of
                                     → −
                                     −   →′
the rule (Factor) and valid, ψ ⊢ Φ , Φ is the assumption of the rule with the restriction d and invalid,
     → −
     −   →′ −→′′
ψ ⊢ Φ , Φ , Φ is the assumption of the rule without the restriction and valid and contains some wand
of depth d + 1. Then there are s′ , h′ such that
         s′ , h′ |= ψ,
                     → →
                     −   −′
         s′ , h′ 6|= Φ , Φ
                    →′′
                    −
Then there is Φ′′ ∈ Φ such that
         s′ , h′ |= Φ′′ .
Let
         Φ′′ ≡ F [∃−
                   →
                   w (S—∗s x) ∗ y)]
where S is a set of variables and y ∈ S and |S − V | = d + 1.

                                                            30
   Define s from s′ by adding assignments for existential variables in Φ′′ . Then we have some h′′ ⊆ h′
such that
       s, h′′ |= S—∗s x.
We obtain some initial heap h by going back along the computation from h′ to the beginning in reverse
order.                                                                       T
   We call a variable w an extra in an entailment J when w ∈ Roots(ψ) − i (Roots(Φi )) where J be
ψ ⊢ (Φi )i∈I . Assume w ∈/ V . The wand P (w)—∗s . . . appears in the computation only when w is an
extra at some step. w is an extra at the step only when at the previous steps we unfold some predicate
with some root in the antecedent and unfold another predicate with the same root in the succedent, and
we match some ∃z in the antecedent and the corresponding ∃w in the succedent.
   By this observation, we make a sequence as follows: We start with some y ∈ V for ∃−    →
                                                                                          w (y—∗s . . .).
Then we take the next w ∈ w for ∃ w (w—∗ . . .). Then we similarly take the next w′ ∈ −
                                →
                                −           →
                                            −  ′      s                                         →
                                                                                                w ′ for
 →
 − ′′  ′    s
∃ w (w —∗ . . .). We repeat this. Finally we collect all of such w to make a sequence starting from y.
Note that there is not any y ′ ∈ V such that y ′ = w since w 6= FV by the algorithm. Then in h for the
succedent, we have a sequence y, z1 , . . . , zd+1 such that
       y ∈ V,
       zi ∈/ V,
       y ։→bk z1 ,
       zi ։tr →bk zi+1 (1 ≤ i ≤ d),
       zi′ →tr zi (1 ≤ j ≤ d + 1),
         ′
       zd+1  ։tr . . . ։tr z1′ ։tr y.
Here zi ’s are different. zi′ ’s may be the same. zi 6= zi′ for all i. zi′ may be in V .
    Since an application of the bounded factor rule in p is arbitrary, we have these for each application
of the bounded factor rule in p. We index these applications by I. Then in h for the succedent, for all
i ∈ I, we have sequences yi , zi1 , . . . , zi(d+1) such that
       yi ∈ V,
       zij ∈
           / V,
       yi ։→bk zi1 ,
       zij ։tr →bk zi(j+1) (1 ≤ j ≤ d),
        ′
       zij →tr zij (1 ≤ j ≤ d + 1),
        ′                     ′
       zi(d+1) ։tr . . . ։tr zi1 ։tr yi .
 ′                                 ′                   ′
zij ’s may be the same. zij 6= zij   for all i, j. zij    may be in V .
     Claim 1. zij ’s are different.
     It is because: It is clear that zij ’s are different for a fixed i. For i 6= k, zij and zkl are different since
they belong to different heaps after some split step.
     Claim 2. In h for the antecedent, zij (1 ≤ j ≤ d) is not below zk(d+1) .
     It is because zij is unfolded before zk(d+1) is unfolded.
                            ′                      ′
     Claim 3. The path zi(d+1)    ։tr . . . ։tr zi1      ։tr yi does not contain any zkj .
     We can show it as follows. Assume the path contains some zkj in order for contradiction. Consider
some process q such that q unfolds the same variables as p, and q unfolds zkj before q does the application
of bounded factor indexed by i. Then this application by q is locally complete with depth d, so the path
of q is longer than that of p, which contradicts with the maximum length for p. Hence we have shown
the claim 3.
                                                     ′
     Claim 4. In h for the antecedent, every zij         is below some zk(d+1) .
                                                     ′
     We can show it as follows. Assume some zij is not below zk(d+1) for all k ∈ I, in order for contradiction.
          ′
Then zij    is above or equals every z such that the bounded factor for z is locally incomplete. Consider
                                                                                    ′
some process q such that q unfolds the same variables as p, and q unfolds zij         before q does the application
of bounded factor indexed by i. Then this application by q is locally complete with depth d, so the path
of q is longer than that of p, which contradicts with the maximum length for p. Hence we have shown
the claim 4.
     By the claim 1, the number of zij ’s is |I|(d + 1). Since the number of zi(d+1) ’s is |I|, by the claims 2
                                                                                               ′
and 4, there is some k ∈ I such that |S| ≥ d + 1 where S is the set of zij such that zij         below zk(d+1) in h
for the antecedent.

                                                        31
   By the claims 2 and 4, the paths zi′ → zi (1 ≤ i ≤ k + 1) are back edges in h for the antecedent. Hence
we have every element of S in the arguments of the predicate for zk(d+1) . But |S| ≥ d + 1 = kmax + 1
and the number of the arguments at zk(d+1) is ≤ kmax , which contradicts. ✷


14     Local Completeness of Step Unrelatedness Introduction
Lemma 14.1 If
                                → → ′
                                −
       Y ↑ ∧Π ∧ Γ ∗ ∆1 ∗ ∆2 |= Φ , ∃−
                                    w (Y ⇑ ∧Π′ ∧ Γ′ ∗ (Γ1 ∗ (∆ ∧ w ↓)) ∗ Γ2 ),
           −
           →
       w ∈ w,
       (Roots + Cells)(Γ) = (Roots + Cells)(Γ′ ) − −
                                                   →
                                                   w,
       (Roots + Cells)(∆1 ) = (Roots + Cells)(Γ1 ∗ (∆ ∧ w ↓)) − −
                                                                →
                                                                w,
                                                     →
                                                     −
       (Roots + Cells)(∆2 ) = (Roots + Cells)(Γ2 ) − w ,

and ∃−
     →
     w (Y ′ ⇑ ∧Π′ ∧ Γ′ ∗ (Γ1 ∗ (∆ ∧ w ↓)) ∗ Γ2 ) is equality-full, then
                                → → ′
                                −
      Y ↑ ∧Π ∧ Γ ∗ ∆1 ∗ ∆2 |= Φ , ∃− w (Y ⇑ ∧Π′ ∧ Γ′ ∗ (Γ1 ∗ (∆ ∧ w ↓)) ∗ (Γ2 ∧ w ⇑)).

    Proof. Assume s, h satisfies the antecedent. Then we have h0 + h1 + h2 = h such that
       s, h0 |= Γ,
       s, h1 |= ∆1 ,
       s, h2 |= ∆2 .
           →
           −
If s, h |= Φ , the claim immediately holds. Assume
       s, h |= ∃−
                →
                w (Y ′ ⇑ ∧Π′ ∧ Γ′ ∗ (Γ1 ∗ (∆ ∧ w ↓)) ∗ Γ2 ).

Then we have −
             →
             a , h′0 + h′1 + h′2 = h such that by letting s′ be s[−
                                                                  →
                                                                  w := −
                                                                       →
                                                                       a ],
       s′ , h′0 |= Γ′ ,
       s′ , h′1 |= Γ1 ∗ (∆ ∧ w ↓),
       s′ , h′2 |= Γ2 .

By Lemma 12.3 (1),
       h0 = h′0 ,
       h1 = h′1 ,
       h2 = h′2 .

Hence we have w ↑ for h′2 . By Lemma 4.5 and the equality-fullness, s′ (w) ∈
                                                                           / Leaves(h2 ). Hence
       s′ , h′2 |= w ⇑ .

✷

Lemma 14.2 At the Unrelatedness Introduction step, the rule
        −
        → → −
    ψ ⊢ Φ , ∃−
             x ∃→y ⇑ (Π ∧ Γ ∗ (∆ ∧ x ↓) ∗ ∗i (Γi ∧ x ⇑))
            → −
            −                                            (UnrelatednessIntroduction)
       ψ ⊢ Φ , ∃ x ∃−
                →   →
                    y ⇑ (Π ∧ Γ ∗ (∆ ∧ x ↓) ∗ ∗i Γi )
is locally complete.

   Proof. Since Π ∧ Γ ∗ (∆ ∧ x ↓) ∗ ∗i Γi ) is grouping and equality-full at the step, there are ∆1 , ∆2 such
that the conditions of Lemma 14.1 hold. By Lemma 14.1, the claim holds. ✷




                                                      32
15       Selective Local Completeness of Rule (∗)
A set of rules of the same conclusion is defined to be selectively locally complete if for every valid
conclusion of the rules there is a locally complete rule in the set.

Proposition 15.1 Let S be the set of
         (Y ∪ Y1 ) ↑ ∧Π ∧ Γ2 ⊢ {Φ2i |i ∈ I − I ′ } or (Y ∪ Y2 ) ↑ ∧Π ∧ Γ1 ⊢ {Φ1i |i ∈ I ′ }   (∀I ′ ⊆ I)
                                                                                                           (Split)
                                 Y ↑ ∧Π ∧ Γ1 ∗ Γ2 ⊢ {Φ1i ∗ Φ2i |i ∈ I}
where
         V = FV(Y ↑ ∧Π ∧ Γ1 ∗ Γ2 ⊢ {Φ1i ∗ Φ2i |i ∈ I}),
         Yi = (Roots + Cells)(Γi ) (i = 1, 2),
         Π ≡ (6= (V )),
         (Roots + Cells)(Γ1 ∗ Γ2 ) + Y = V,
(Γ1 , Γ2 ) is group-disjoint, and (Φ1i , Φ2i ) (i ∈ I)) is group split by (Γ1 , Γ2 ). Then S is selectively locally
complete, namely, if Y ↑ ∧Π ∧ Γ1 ∗ Γ2 ⊢ {Φ1i ∗ Φ2i |i ∈ I} is valid, then there is some rule in S such that
all assumptions of the rule are valid.

   Proof. Assume
         Y ↑ ∧Π ∧ Γ1 ∗ Γ2 |= {Φ1i ∗ Φ2i |i ∈ I}.
   Let
         ψ1 = (Y ∪ Y2 ) ↑ ∧Π ∧ Γ1 ,
         ψ2 = (Y ∪ Y1 ) ↑ ∧Π ∧ Γ2 .
   Fix s, h1 , h2 and assume
         s, h1 |= ψ1 ,
         s, h2 |= ψ2 .
Let h = h1 + h2 . Then
         s, h |= Y ↑ ∧Π ∧ Γ1 ∗ Γ2 .
   Then we have
      _
        s, h1 + h2 |= Φ1i ∗ Φ2i .
         i∈I

   By Lemma 12.3 (2),
      _
        (s, h1 |= Φ1i ∧ s, h2 |= Φ2i ).
         i∈I

By Lemma 7.1
       ^      _                    _
           ((   s, h1 |= Φ1i ) ∨ (   s, h2 |= Φ2i )).
         I=I1 +I2   i∈I1                i∈I2

Since s, h1 , h2 are arbitrary,
         ∀sh1 h2^
                (s, h1 |=_ψ1 ∧ s, h2 |= ψ2 → _
                     ((    s, h1 |= Φ1i ) ∨ (  s, h2 |= Φ2i ))).
               I=I1 +I2    i∈I1                i∈I2

Fix I1 + I2 = I. Then
         ∀sh1 h2_
                (s, h1 |= ψ1 ∧ s, h2 |=_ψ2 →
             ((     s, h1 |= Φ1i ) ∨ (   s, h2 |= Φ2i ))).
                 i∈I1                 i∈I2


                                                             33
Hence
                                                      _
        ∀sh1 h2 ((s, h1 |= ψ1 ∧ s, h2 |= ψ2 → (           s, h1 |= Φ1i ))∨
                                                _ i∈I1
               (s, h1 |= ψ1 ∧ s, h2 |= ψ2 → (         s, h2 |= Φ2i ))).
                                               i∈I2
                                             _                          _
   If s, h1 |= ψ1 ∧ s, h2 |= ψ2 , then              (s, h1 |= Φ1i ) ∨          (s, h2 |= Φ2i ). If s, h1 6|= ψ1 , then s, h1 |=
        _                                    i∈I1
                                                                    _   i∈I2
ψ1 →          s, h1 |= Φ1i . If s, h2 6|= ψ1 , then s, h2 |= ψ2 →          s, h2 |= Φ2i . Hence
       i∈I1                                                         i∈I2
                                 _
        ∀sh1 h2 ((s, h1 |= ψ1 →       s, h1 |= Φ1i )∨
                              _ i∈I 1

            (s, h2 |= ψ2 →       s, h2 |= Φ2i )).
                                i∈I2

Hence
        ∀s(ψ1 |=s {Φ1i |i ∈ I1 } ∨ ψ2 |=s {Φ2i |i ∈ I2 }).

By Lemma 11.4
        ψ1 |= {Φ1i |i ∈ I1 } ∨ ψ2 |= {Φ2i |i ∈ I2 }.

Since I1 + I2 = I are arbitrary, we have
        ψ1 |= {Φ1i |i ∈ I1 } ∨ ψ2 |= {Φ2i |i ∈ I2 }

for all I1 + I2 = I.
    Consider the rule in S such that for each I ′ , by taking I1 to be I ′ and I2 to be I − I ′ , the assumption
for I ′ is taken to be the first disjunct when
        ψ2 |= {Φ2i |i ∈ I2 }

and is taken to be the second disjunct when
        ψ1 |= {Φ1i |i ∈ I1 }.

Then all the assumptions of this rule are valid. ✷


16      Fresh Variable in Succedent
Lemma 16.1 If θ is a variable renaming, (Dom ∪ Range)(θ) ⊆ X, and (Dom ∪ Range)(θ) ∩ FV(Γ) = ∅,
                             →
                             −
and Π ⊇ (6= (FV(X ↑ ∧Π ∧ Γ ⊢ Φ , Φ, Φθ))) and Φ is equality-full, then the rule
                       →
                       −
         X ↑ ∧Π ∧ Γ ⊢ Φ , Φ
                     →
                     −         (FreshVariableDisjunctElim)
        X ↑ ∧Π ∧ Γ ⊢ Φ , Φ, Φθ

   is locally complete.

    Proof. Let −
               →x 1 be FV(Φ) ∩ Dom(θ) and −   →
                                              x 2 be θ(−→x 1 ).
    Assume the conclusion of the rule is valid in order to show the assumption of the rule is valid. Assume
                                        →
                                        −                       →
                                                                −
s, h |= X ↑ ∧Π ∧ Γ in order to show Φ , Φ. Then s, h |= Φ , Φ, Φθ. Assume s, h |= Φθ. We will show
s, h |= Φ.
    By Lemma 4.5, Leaves(h) ⊆ s(FV(Γ) ∪ {nil}). Hence s(−        →
                                                                 x 1−
                                                                    →    / Leaves(h), since −
                                                                    x 2) ∈                  →
                                                                                            x 1−
                                                                                               →
                                                                                               x2 ∈/ FV(Γ).
          →
          − →
            −                                  →
                                               −  →
                                                  −
                   / (Dom ∪ Range)(h), since x 1 x 2 ⊆ X.
Hence s( x 1 x 2 ) ∈
    Let T be FV(Φ1 ) ∪ {nil} − −
                               →
                               x 1 . Then
        s, h |= ∃−
                 →
                 x 2 ⇑ (Φθ ∧ (6= (−
                                  →
                                  x 2, T ∪ −
                                           →
                                           x 2 ))).



                                                              34
By variable renaming,
        s, h |= ∃−
                 →
                 x 1 ⇑ (Φ ∧ (6= (−
                                 →
                                 x 1, T ∪ −
                                          →
                                          x 1 )).

Here ∃−
      →
      x 1 ⇑ (Φ ∧ (6= (−
                      →
                      x 1, T ∪ −
                               →
                               x 1 )) is equality-full. By Lemma 6.1 (2),
        s[−
          →
          x 1 := s(−
                   →
                   x 1 )], h |= Φ ∧ (6= (−
                                         →
                                         x 1, T ∪ −
                                                  →
                                                  x 1 )).

Hence
        s, h |= Φ.

✷


17      Completeness of CSLIDω
This section shows the completeness of CSLIDω by using the algorithm, the local completeness, and the
termination.
   By the lemmas in previous sections, we can show some process does not fail for a valid input.

Lemma 17.1 (1) In the algorithm, each step except the rules (BoundedFactor) and (Split) in each
function except Main and MainLoop transforms a valid entailment into subgoals consisting of valid en-
tailments.
    (2) If a valid entailment is given to the algorithm, for each call of the function MainLoop, there is
some process such that all applications of the rules (BoundedFactor) and (Split) are locally complete.
    (3) If a valid entailment is given to the algorithm, for each call of the function MainLoop, some process
does not fail.

      Proof. (1) We only discuss interesting cases.
      - The function Split.
      Step 4. Existential Disequality. We have 6= for every variable except −→
                                                                             z. −→
                                                                                 x 6= −
                                                                                      →
                                                                                      z from the antecedent.
→
−y 6= − →z from −→y ↑ and −→
                           z ↓.
      Step 5. Unrelatedness Introduction. By Lemma 14.2.
      - Normalize
      Step 1. Fresh Variable Disjunct Elimination. By Lemma 16.1.
      Step 2. Unnecessary Disequality Elimination. Assume the antecedent of the assumption is true at
(s, h) in order to show the succedent of the assumption is true at (s, h). Choose a ∈ Val − Dom(h) such
                        −
                        →
that a ∈  / s(FV(Π, Γ, Φ ) ∪ {nil}). Let s′ be s[x := a]. Then the antecedent of the conclusion is true at
(s′ , h). Then the succedent of the conclusion is true at (s′ , h). Then the succedent of the assumption is
true at (s′ , h). Since y does not appear in the succedent, the succedent of the assumption is true at (s, h).
      Step 3. Unnecessary Variable Elimination. It is similar to Unnecessary Disequality Elimination by
choosing a ∈  / Dom(h).
      Step 4. Unnecessary Unrelated Existential Elimination. By Lemma 4.3.
      (2) By Proposition 15.1 and Lemma 13.1.
      (3) From (2), we have some process such that all applications of the rules (BoundedFactor) and (Split)
are locally complete. Since Main does case analysis and MainLoop does case analysis and discharges by
bud-companion relation. By (1), in this process, applications of each rule are locally complete. Hence
all the entailments handled by this process are valid. We show this process does not fail. Assume it
fails in order to show contradiction. When the process fails, there is either some Termination Check
step in the function MainLoop or the step for checking emp in the function Main. In both cases we
have _  contradiction since the entailment is shown to be^  invalid as follows: For the function Main. Since
Π→         Π′ is not true, we have s that satisfies Π and     ¬Π′ . Take h to be the empty heap. (s, h) is a
counterexample since for every disjunct either emp is not in it or Π′ in it is false. For MainLoop. Since
ψ is satisfiable by the Unsat check step, we have s that satisfies Π. Take h to be the empty heap. Then
(s, h) is a counterexample since emp is not in the succedent. ✷
      Finally we can prove the completeness of CSLIDω .



                                                            35
Theorem 17.2 (Completeness) (1) The system CSLIDω is complete. Namely, if a given entailment
J is valid, then it is provable in CSLIDω .
    (2) The algorithm decides the validity of a given entailment. Namely, For a given input J, the
algorithm returns Yes when the input is valid, and it returns No when the input is invalid.

    Proof. (1) Assume J is valid in order to show J is provable in CSLIDω . When we input J to the
algorithm, by Lemma 17.1 (3), for each call of MainLoop, some process does not fail. By Lemma 10.6
(2), for each call of MainLoop, the process terminates without fail. Hence the algorithm terminates with
Yes. By Lemma 10.3, J is provable.
    (2) Assume J is valid, in order to show the algorithm with input J terminates with Yes. By Lemma
17.1 (3), for each call of MainLoop, some process does not fail. By Lemma 10.6 (2), the algorithm
terminates with Yes.
    Assume J is invalid, in order to show the algorithm with input J terminates with No. By Lemma
10.6 (2), the algorithm terminates. Assume the algorithm with input J terminates with Yes, in order to
show contradiction. By Lemma 10.3, J is provable. By Theorem 8.3, |= J, which contradicts. Hence the
algorithm with input J terminates with No. ✷


18     Conclusion
We have proposed the cyclic proof system CSLIDω for symbolic heaps with inductive definitions, and
have proved its soundness theorem and its completeness theorem, and have given the decision procedure
for the validity of a given entailment.
    Future work would be to apply ideas in this paper to other systems, in particular, the strong wand
and the selective local completeness of the rule (∗).


References
 [1] T. Antonopoulos, N. Gorogiannis, C. Haase, M. Kanovich, and J. Ouaknine, Foundations for Decision
     Problems in Separation Logic with General Inductive Predicates, In: Proceedings of FoSSaCS 2014,
     LNCS 8412 (2014) 411–425.
 [2] S. Berardi and M. Tatsuta, Classical System of Martin-Lof’s Inductive Definitions is not Equivalent
     to Cyclic Proof System, In: Proceeding of FoSSaCS 2017, LNCS 10203 (2017) 301–317.
 [3] S. Berardi and M. Tatsuta, Equivalence of Inductive Definitions and Cyclic Proofs under Arithmetic,
     In: Proceedings of LICS2017 (2017) 1–12.
 [4] J. Berdine, C. Calcagno, P. W. O’Hearn, A Decidable Fragment of Separation Logic, In: Proceedings
     of FSTTCS 2004, LNCS 3328 (2004) 97–109.
 [5] J. Berdine, C. Calcagno, and P. W. O’Hearn, Symbolic Execution with Separation Logic, In: Pro-
     ceedings of APLAS 2005, LNCS 3780 (2005) 52–68.
 [6] J. Brotherston, Formalised Inductive Reasoning in the Logic of Bunched Implications, In: Proceed-
     ings of SAS 2007, LNCS 4634 (2007), 87–103.
 [7] J. Brotherston, A Simpson, Sequent calculi for induction and infinite descent, Journal of Logic and
     Computation 21 (6) (2011) 1177–1216.
 [8] J. Brotherston, D. Distefano, and R. L. Petersen, Automated cyclic entailment proofs in separation
     logic, In: Proceedings of CADE-23 (2011) 131–146.
 [9] J. Brotherston, N. Gorogiannis, and R. L. Petersen, A Generic Cyclic Theorem Prover, In: Proceed-
     ings of APLAS 2012, LNCS 7705 (2012) 350–367.
[10] J. Brotherston, C. Fuhs, N. Gorogiannis, and J. Navarro Pérez, A Decision Procedure for Satisfiability
     in Separation Logic with Inductive Predicates, In: Proceedings of CSL-LICS’14 (2014) Article 25.
[11] J. Brotherston, N. Gorogiannis, M. Kanovich, and R. Rowe, Model checking for symbolic-heap
     separation logic with inductive predicates, In: Proceedings of POPL 2016 (2016) 84-96.
[12] W. Chin, C. David, H. Nguyen, and S. Qin, Automated Verification of Shape, Size and Bag Properties
     via User-Defined Predicates in Separation Logic, In Science of Computer Programming 77 (9) (2012)
     1006–1036.


                                                    36
[13] D. Chu, J. Jaffar, and M. Trinh, Automatic Induction Proofs of Data-Structures in Imperative
     Programs, In: Proceedings of PLDI 2015 (2015) 457–466.
[14] B. Cook, C. Haase, J. Ouaknine, M. J. Parkinson, J. Worrell, Tractable reasoning in a fragment of
     Separation Logic, In: Proceedings of CONCUR’11, LNCS 6901 (2011) 235–249.
[15] C. Enea, V. Saveluc, M. Sighireanu, Compositional invariant checking for overlaid and nested linked
     lists, In: Proceeding of ESOP 2013, LNCS 7792 (2013) 129–148.
[16] C. Enea, O. Lengál, M. Sighireanu, T. Vojnar, Compositional Entailment Checking for a Fragment
     of Separation Logic, In: Proceedings of APLAS 2014, LNCS 8858 (2014) 314–333.
[17] R. Iosif, A. Rogalewicz, and J. Simacek, The Tree Width of Separation Logic with Recursive Defi-
     nitions, In: Proceedings of CADE-24, LNCS 7898 (2013) 21–38.
[18] R. Iosif, A. Rogalewicz, and T. Vojnar, Deciding Entailments in Inductive Separation Logic with
     Tree Automata, In: Proceedings of ATVA 2014, LNCS 8837 (2014) 201–218.
[19] J. Navarro Pérez and A. Rybalchenko, Separation logic modulo theories, In: Proceedings of APLAS
     2013, LNCS 8301 (2013) 90-106.
[20] R. Piskac, T. Wies, and D. Zufferey, Automating Separation Logic Using SMT, In: Proceedings of
     CAV 2013, LNCS 8044 (2013) 773-789.
[21] R. Piskac, T. Wies, and D. Zufferey, Automating separation logic with trees and data, In: Proceed-
     ings of CAV 2014, LNCS 8559 (2014) 711–728.
[22] J.C. Reynolds, Separation Logic: A Logic for Shared Mutable Data Structures, In: Proceedings of
     Seventeenth Annual IEEE Symposium on Logic in Computer Science (LICS2002) (2002) 55–74.
[23] A. Simpson, Cyclic Arithmetic is Equivalent to Peano Arithmetic, In: Proceedings of FoSSaCS 2017
     (2017) 283–300.
[24] M. Tatsuta and D. Kimura, Separation Logic with Monadic Inductive Definitions and Implicit Ex-
     istentials, In: Proceedings of APLAS 2015, LNCS 9458 (2015) 69–89.
[25] M. Tatsuta, K. Nakazawa and D. Kimura, Completeness of Cyclic Proofs for Symbolic Heaps,
     arXiv:1804.03938, 2018.




                                                  37
