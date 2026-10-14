Logical Methods in Computer Science
Vol. 4 (4:1) 2008, pp. 1–31                                                           Submitted      Feb. 11, 2007
www.lmcs-online.org                                                                   Published      Oct. 17, 2008




              INTERPOLATION IN LOCAL THEORY EXTENSIONS

                                  VIORICA SOFRONIE-STOKKERMANS

     Max-Planck-Institut für Informatik, Campus E1.4, Saarbrücken, Germany
     e-mail address: sofronie@mpi-inf.mpg.de


         Abstract. In this paper we study interpolation in local extensions of a base theory. We
         identify situations in which it is possible to obtain interpolants in a hierarchical manner,
         by using a prover and a procedure for generating interpolants in the base theory as black-
         boxes. We present several examples of theory extensions in which interpolants can be
         computed this way, and discuss applications in verification, knowledge representation, and
         modular reasoning in combinations of local theories.




                                           1. Introduction
Many problems in mathematics and computer science can be reduced to proving satisfiability
of conjunctions of (ground) literals modulo a background theory. This theory can be a
standard theory, the extension of a base theory with additional functions, or a combination
of theories. It is therefore very important to find efficient methods for reasoning in standard
as well as complex theories. However, it is often equally important to find local causes for
inconsistency. In distributed databases, for instance, finding local causes of inconsistency
can help in locating errors. Similarly, in abstraction-based verification, finding the cause of
inconsistency in a counterexample at the concrete level helps to rule out certain spurious
counterexamples in the abstraction.
     The problem we address in this paper can be described as follows: Let T be a theory
and A and B be sets of ground clauses in the signature of T , possibly with additional
constants. Assume that A ∧ B is inconsistent with respect to T . Can we find a ground
formula I, containing only constants and function symbols common to A and B, such that
I is a consequence of A with respect to T , and B ∧ I is inconsistent modulo T ? If so, I
is a (Craig) interpolant of A and B, and can be regarded as a “local” explanation for the
inconsistency of A ∧ B.
    In this paper we study possibilities of obtaining ground interpolants in theory exten-
sions. We identify situations in which it is possible to do this in a hierarchical manner, by
using a prover and a procedure for generating interpolants in the base theory as “black-
boxes”.
   1998 ACM Subject Classification: F.4.1, I.2.3, D.2.4, F.3.1, I.2.4.
   Key words and phrases: Logic, Interpolation, Complex theories, Verification, Knowledge representation.



l    LOGICAL METHODS
     IN COMPUTER SCIENCE                     DOI:10.2168/LMCS-4 (4:1) 2008
                                                                                          c
                                                                                          CC
                                                                                               V. Sofronie-Stokkermans
                                                                                               Creative Commons
2                                 V. SOFRONIE-STOKKERMANS




    We consider a special type of extensions of a base theory – namely local theory ex-
tensions – which we studied in [15]. We showed that in this case hierarchical reasoning is
possible. i.e. proof tasks in the extension can be reduced to proof tasks in the base theory.
Here we study possibilities of hierarchical interpolant generation in local theory extensions.
      The main contributions of the paper are summarized below:
• First, we identify new examples of local theory extensions.
• Second, we present a method for generating interpolants in local extensions of a base
   theory. The method is general, in the sense that it can be applied to an extension T1 of
   a theory T0 provided that:
      (i) T0 is convex;
     (ii) T0 is P -interpolating for a specified set P of predicates (cf. the definition in Sec-
          tion 5.2);
    (iii) in T0 every inconsistent conjunction of ground clauses A ∧ B allows a ground inter-
          polant;
    (iv) the extension is defined by clauses of a special form (type (5.1) in Section 5.2).
   The method is hierarchical: the problem of finding interpolants in T1 is reduced to that
   of finding interpolants in the base theory T0 . We can use the properties of T0 to control
   the form of interpolants in the extension T1 .
• Third, we identify examples of theory extensions with properties (i)–(iv).
• Fourth, we discuss application domains such as: modular reasoning in combinations of
   local theories (characterization of the type of information which needs to be exchanged),
   reasoning in distributed databases, and verification.
The existence of ground interpolants has been studied in several recent papers, mainly
motivated by abstraction-refinement based verification [7, 8, 9, 19, 6]. In [8] McMillan
presents a method for generating ground interpolants from proofs in an extension of linear
rational arithmetic with uninterpreted function symbols. The use of free function symbols is
sometimes too coarse (cf. the example in Section 2.2). Here, we show that similar results also
hold for other types of extensions of a base theory, provided that the base theory has some of
the properties of linear rational arithmetic. Another method for generating interpolants for
combinations of theories over disjoint signatures from Nelson-Oppen-style unsatisfiability
proofs was proposed by Yorsh and Musuvathi in [19]. Although we impose similar conditions
on T0 , our method is orthogonal to theirs, as it can also handle combinations of theories
over non-disjoint signatures. In [6] a different interpolation property – stronger than the
property under consideration in this paper – is studied, namely the existence of ground
interpolants for arbitrary formulae – which is proved to be equivalent to the theory having
quantifier elimination. This limits the applicability of the results in [6] to situations in which
the involved theories allow quantifier elimination. If the theory considered has quantifier
elimination then we can use this for obtaining ground interpolants for arbitrary formulae.
The goal of our paper is to identify theories – possibly without quantifier elimination – in
which, nevertheless, ground interpolants for ground formulae exist.
Structure of the paper: We start by providing motivation for the study in Section 2. In
Section 3 the basic notions needed in the paper are introduced. Section 4 contains results
on local theory extensions. In Section 5 local extensions allowing hierarchical interpola-
tion are identified, and based on this, in Section 6 a procedure for computing interpolants
hierarchically is given. In Section 7 applications to modular reasoning in combinations of
                        INTERPOLATION IN LOCAL THEORY EXTENSIONS                              3




theories, reasoning in complex databases, and verification are presented. In Section 8 we
draw conclusions, discuss the relationship with existing work, and sketch some plans for
future work. For the sake of clarity in presentation, all the proofs that are not directly re-
lated to the main thread of the paper can be found in the appendix. (These results concern
illustrations of the fact that certain theory extensions are local, or satisfy assumptions that
guarantee that interpolants can be computed hierarchically.)

                                       2. Motivation
In this section we present two fields of applications in which it is important to efficiently
compute interpolants: knowledge representation and verification.

2.1. Knowledge representation. Consider a simple (and faulty) terminological data-
base for chemistry, consisting of two extensions of a common kernel Chem (basic chem-
istry): AChem (inorganic (anorganic) chemistry) and BioChem (biochemistry). Assume
that Chem contains a set C0 = {process, reaction, substance, organic, inorganic} of concepts
and a set Γ0 of constraints:
       Γ0 = {organic ∧ inorganic = ∅, organic ⊆ substance, inorganic ⊆ substance} .
Let AChem be an extension of Chem with concepts C1 = {cat-oxydation, oxydation}, a rôle
R1 = {catalyzes}, terminology T1 and constraints Γ1 :
        T1 = {cat-oxydation = substance ∧ ∃ catalyzes(oxydation)}
        Γ1 = {reaction ⊆ oxydation, cat-oxydation ⊆ inorganic, cat-oxydation 6= ∅} .
Let BioChem be an extension of Chem with the concept C2 = {enzyme}, the rôles R2 =
{produces, catalyzes}, terminology T2 and constraints Γ2 :
 T2 = {reaction=process ∧ ∃ produces(substance), enzyme = organic ∧ ∃ catalyzes(reaction)}
 Γ2 = {enzyme 6= ∅} .
The combination of Chem, AChem and BioChem is inconsistent (we wrongly added to Γ1
the constraint reaction ⊆ oxydation instead of oxydation ⊆ reaction). This can be proved
as follows: By results in [14] (p.156 and p.166) the combination of Chem, AChem and
BioChem is inconsistent if and only if
                            Γ0 ∧ (T1 ∧ Γ1 ) ∧ (T2 ∧ Γ2 ) |=T ⊥                          (2.1)
                                 S
where T is the extension SLat ∧ f ∈R1 ∪R2 Mon(f ) of the theory of semilattices with smallest
element 0 and monotone function symbols corresponding to ∃r for each rôle r ∈ R1 ∪ R2 .
Using, for instance, the hierarchical calculus presented in [15] (see also Section 4), the
contradiction can be found in polynomial time. In order to find the mistake we look for
an explanation for the inconsistency in the common language of AChem and BioChem.
(Common to AChem and BioChem are the concepts substance, organic, inorganic, reaction and
the rôle catalyzes.) This can be found by computing an interpolant for the conjunction
in (2.1) in the theory of semilattices with monotone operators. In this paper we show how
such interpolants can be found in an efficient way. The method is illustrated on the example
above in Section 7.2.
4                                        V. SOFRONIE-STOKKERMANS




2.2. Verification. In [8], McMillan proposed a method for abstraction-based verification
in which interpolation (e.g. for linear arithmetic + free functions) is used for abstraction
refinement. The idea is the following: Starting from a concrete, precise description of a
(possibly infinite-state) system one can obtain a finite abstraction, by merging the states
into equivalence classes. A transition exists between two abstract states if there exists a
transition in the concrete systems between representatives in the corresponding equivalence
classes. Literals describing the relationships between the state variables at the concrete level
are represented – at the abstract level – by predicates on the abstract states (equivalence
classes of concrete states). Classical methods (e.g. BDD-based methods) can be used for
checking whether there is a path in the abstract model from an initial state to an unsafe
state. We distinguish the following cases:
(1) No unsafe state is reachable from an initial state in the abstract model. Then, due to
     the way transitions are defined in the abstraction, this is the case also at the concrete
     level. Hence, the concrete system is guaranteed to be safe.
(2) There exists a path in the abstract model from an initial state to an unsafe state. This
     path may or may not have a correspondent at the concrete level. In order to check this,
     we analyse the counterpart of the counterexample in the concrete model. This can be
     reduced to testing the satisfiability of a set of constraints:
                           Init(s0 ) ∧ Tr(s0 , s1 ) ∧ · · · ∧ Tr(sn−1 , sn ) ∧ ¬Safe(sn )
    (2.1) If the set of constraints is satisfiable then an unsafe state is reached from the
          initial state also in the concrete system. Thus, the concrete system is not safe.
    (2.2) If the set of constraints is unsatisfiable, then the counterexample obtained due to
          the abstraction was spurious. This means that the abstraction was too coarse.
          In order to refine it we need to take into account new predicates or relationships
          between the existing predicates. Interpolants provide information about which
          new predicates need to be used for refining the abstraction.
We illustrate these ideas below. Consider a water level controller modeled as follows:
Changes in the water level by inflow/outflow are represented as functions in, out, depend-
ing on time t and water level L. Alarm and overflow levels Lalarm <Loverflow , as well as
upper/lower bounds for mode durations 0 ≤ δt ≤ ∆t are parameters of the systems.

                                           • If L ≥ Lalarm then a valve is opened until time g(t),
      t:= h(t)
                                             time changes to t′ := h(t) and the water level to
      L:= in(out(L, g(t)−t), h(t)−t)         L′ := in(out(L, g(t) − t), h(t) − t).

             L > Lalarm
                                           • If L < Lalarm then the valve is closed; time changes to
                                              t′ := k(t), and the water level to L′ := in(L, k(t) − t).
                  valve := 1
                  valve := 0
                                           We impose restrictions K on h, g, k and on in and out:
             L>L
                   alarm
                                              ∀t (0 ≤ δt ≤ g(t) − t ≤ h(t) − t ≤ ∆t)
                                              ∀t (0 ≤ k(t) − t ≤ ∆t)
                                              ∀L, t (L < Lalarm ∧ 0 ≤ t ≤ ∆t → in(L, t) < Loverflow )
       L:= in(L, k(t)−t)
                                              ∀L, t (L < Loverflow ∧ t ≥ δt → out(L, t) < Lalarm ).
       t:= k(t)
                                           We want to show that if initially L < Lalarm then the
                                           water level always remains below Loverflow .
                          INTERPOLATION IN LOCAL THEORY EXTENSIONS                                         5




We start with an abstraction in which the predicates are:
       p:     L < Lalarm
       r1 :   t′ ≈ k(t)          r2 : t′′1 ≈ g(t′ ) r3 : t′′2 ≈ h(t′ )
       p1 :   L′ ≈ in(L, t′ − t) p2 : L′ ≥ Lalarm p3 : L′′ ≈ in(out(L′ , t′′1 − t′ ), t′′2 − t′ )
       q:     ¬L′′ < Loverflow
and no other relations between these predicates are specified. We can, for instance, use
finite model checking for the finite abstraction obtained this way. Note for instance that
                                  p ∧ p1 ∧ p2 ∧ p3 ∧ r1 ∧ r2 ∧ r3 ∧ q
is satisfiable, i.e. in the abstract model there exists a path (of length 2) from the initial state
to an unsafe state. We analyze the corresponding path in the concrete model to see if this
counterexample to safety is spurious, i.e. we check whether there exist l, l′ , l′′ , t, t′ , t′′1 , t′′2 ∈ R
such that the conjunction:
     G = l<Lalarm ∧ l′ ≈ in(l, t′ − t) ∧ t′ ≈ k(t) ∧ l′ ≥ Lalarm ∧
         l′′ ≈ in(out(l′ , t′′1 − t′ ), t′′2 − t′ ) ∧ t′′1 ≈ g(t′ ) ∧ t′′2 ≈ h(t′ ) ∧ ¬l′′ < Loverflow
is true. If h, g, k, in, out are regarded as free function symbols this conjunction is satisfiable,
so the spuriousness of the counterexample cannot be detected. G can however be proved
to be unsatisfiable if we take into account the additional conditions K on the functions
in, out, g, h and k. Interpolants can be used for determining the cause of inconsistency,
and can therefore help in refining the abstraction. The hierarchical interpolation method
we present here allows us to efficiently generate ground interpolants for extensions with
functions satisfying axioms of the type considered here and also for a whole class of more
general axioms. An illustration of this method on the formulae in the example presented
here is given in Section 7.3.
     Besides the application to verification by abstraction-refinement, computation of Craig
interpolants has other potential applications (e.g. to goal-directed overapproximation for
achieving faster termination, or to automatic invariant generation).

                                           3. Preliminaries
In this section we introduce the main notions and definitions concerning theories, models
and interpolants needed in the paper.

3.1. Theories and models. Theories can be regarded as sets of formulae or as sets of
models. In this paper, whenever we speak about a theory T – if not otherwise specified –
we implicitly refer to the set Mod(T ) of all models of T .
Definition 3.1. Let T be a theory in a given signature Π = (Σ, Pred), where Σ is a set of
function symbols and Pred a set of predicate symbols. Let φ and ψ be formulae over the
signature Π with variables in a set X. The notion of truth of formulae and of entailment is
the usual one in logic. We say that:
• φ is true with respect to T (denoted |=T φ) if φ is true in each model M of T .
• φ is satisfiable with respect to T if there exists at least one model M of T and an
   assignment β : X → M such that (M, β) |= φ. Otherwise we say that φ is unsatisfiable.
• We say that φ entails ψ with respect to T (denoted φ |=T ψ) if for every model M of T
   and every valuation β, if (M, β) |= φ then (M, β) |= ψ.
6                                       V. SOFRONIE-STOKKERMANS




Note that φ is unsatisfiable with respect to T if and only if φ |=T ⊥ (⊥ stands for false).

3.2. Interpolation. A theory T has interpolation if, for all formulae φ and ψ in the sig-
nature of T , if φ |=T ψ then there exists a formula I containing only symbols which occur
in both φ and ψ such that φ |=T I and I |=T ψ. First order logic has interpolation but –
for an arbitrary theory T – even if φ and ψ are e.g. conjunctions of ground literals, I may
still be an arbitrary formula, containing alternations of quantifiers (cf. [6] for an example of
ground formulae φ and ψ in the language of the theory Tharrays of arrays whose conjunction
is unsatisfiable, but there is no ground interpolant over the common variables of φ and ψ).
It is often important to identify situations in which ground clauses have ground interpolants.
Definition 3.2. We say that a theory T has the ground interpolation property (or, shorter,
that T has ground interpolation) if for all ground clauses A(c, d) and B(c, e), if A(c, d) ∧
B(c, e) |=T ⊥ then there exists a ground formula I(c), containing only the constants c
occurring both in A and B, such that A(c, d) |=T I(c) and B(c, e) ∧ I(c) |=T ⊥ .
    There exist results which relate ground interpolation to amalgamation or the injection
transfer property [5, 2, 18] and thus allow us to recognize many theories with ground
interpolation. We present these results in Appendix A.
Theorem 3.3. The following theories allow ground interpolation1 :
(1) The theory of pure equality (without function symbols).
(2) Linear rational and real arithmetic.
(3) The theory of posets.
(4) The theories of (a) Boolean algebras, (b) semilattices, (c) distributive lattices.
Proof. The proof is given in Appendix A.
     Other examples of theories which allow ground interpolation are the equational classes
of (abelian) groups and lattices. In many applications one needs to consider extensions or
combinations of theories, and proving amalgamation properties can be complicated. On the
other hand, just knowing that ground interpolants exist is usually not sufficient: we would
like to construct the interpolants fast.
     In the examples considered in Theorem 3.3, methods for constructing interpolants exist.
For the theories of pure equality and of posets interpolants can be constructed for instance
from proofs [8, 19]. For linear rational or real arithmetic they can either be constructed
from proofs [8] or by constructing linear programming problems and solving these problems
using an off-the-shelf sound solver [11] 2. For the theories of Boolean algebras, distributive
lattices and semilattices they can be reconstructed from resolution proofs associated with
the translation of the satisfiability problems to propositional logic [13]; the construction is
similar to the one described in the proof of Theorem 5.4 in Appendix C.
We would like to use the advantages of modular or hierarchical reasoning for constructing
interpolants in theory extensions in an efficient way. This is why in this paper we aim at giv-
ing methods for constructing interpolants in a hierarchical way. Since in [15] we identified a
    1In fact, the theories (1) and (4) allow equational interpolation (cf. Definition A.2 in Appendix A). Similar
results were also established for (2) in [11].
   2Some off-the-shelf linear programming solvers may not be sound, so care is needed when choosing them.
                          INTERPOLATION IN LOCAL THEORY EXTENSIONS                                       7




class of theory extensions – namely, local theory extensions – in which hierarchical reasoning
was possible, in what follows we will study interpolation in local theory extensions.

                                  4. Local Theory Extensions
Let T0 be a theory with signature Π0 = (Σ0 , Pred). We consider extensions T1 = T0 ∪ K of
T0 with signature Π = (Σ, Pred), where Σ = Σ0 ∪ Σ1 (i.e. the signature is extended by new
function symbols) and T1 is obtained from T0 by adding a set K of (universally quantified)
clauses. Thus, Mod(T1 ) consists of all Π-structures M which are models of K and whose
reduct M|Π0 to Π0 is a model of T0 .
Definition 4.1. A partial Π-structure is a structure M = (M, {fM }f ∈Σ , {PM }P ∈Pred ),
where M 6= ∅ and for every f ∈ Σ with arity n, fM is a partial function from M n to M .
     Any variable assignment β : X → M extends in a natural way to terms, such that
β(f (t1 , . . . , tn )) = fM (β(t1 ), . . . , β(tn )). Thus, the notion of evaluating a term t with respect
to a variable assignment β : X → M for its variables in a partial structure M is the same
as for total algebras, except that this evaluation is undefined if t = f (t1 , . . . , tn ) and at least
one of β(ti ) is undefined, or else (β(t1 ), . . . , β(tn )) is not in the domain of fM .
Definition 4.2. Let M be a partial Π-structure, C a clause and β : X → M . Then
(M, β) |=w C if and only if either
  (i) for some term t in C, β(t) is undefined, or else
 (ii) β(t) is defined for all terms t of C, and there exists a literal L in C such that β(L) is
      true in M.
M weakly satisfies C (notation: M |=w C) if (M, β) |=w C for all assignments β. We say
that M weakly satisfies a set of clauses K or M is a weak partial model of K (notation:
M |=w K) if M |=w C for all C ∈ K.


4.1. Local theory extensions: definitions. Let T0 be a theory with signature Π0 =
(Σ0 , Pred) and let K be a set of (universally quantified) clauses in the signature Π =
(Σ, Pred), where Σ = Σ0 ∪Σ1 . In what follows, when referring to sets G of ground clauses
we assume they are in the signature Πc = (Σ∪Σc , Pred) where Σc is a set of new constants.
For the sake of simplicity, we will use the same notation for a structure and for its universe.
     A (total) model of T1 = T0 ∪ K is a Π-structure A s.t. A |= K and A|Π0 is a model of T0 .
Let PModw (Σ1 , T1 ) be the class of all weak partial models P of K, in which the Σ1 -functions
are partial and such that P|Π0 is a total model of T0 .
     An extension T0 ⊆ T0 ∪ K is local if, in order to prove unsatisfiability of a set G of
clauses with respect to T0 ∪ K, it is sufficient to use only those instances K[G] of K in which
the terms starting with extension functions are in the set st(G, K) of ground terms which
already occur in G or K.
Definition 4.3. We consider the following properties of an extension T1 =T0 ∪ K of a theory
T0 with additional function symbols satisfying a set K of clauses.
 (Loc) For every set G of ground clauses, G |=T1 ⊥ if and only if there is no partial
       Πc -structure P such that P|Π0 is a total model of T0 , all terms in st(K, G) are
       defined in P , and P weakly satisfies K[G] ∧ G.
8                                     V. SOFRONIE-STOKKERMANS




A weaker notion (Locf ) is defined by requiring that the locality condition only holds for
finite sets G of ground clauses.
  (Locf ) For every finite set G of ground clauses, G |=T1 ⊥ if and only if there is no partial
          Πc -structure P such that P|Π0 is a total model of T0 , all terms in st(K, G) are
          defined in P , and P weakly satisfies K[G] ∧ G.

Since (Locf ) is the property we are interested in, we will only refer to this form of locality in
what follows. We will say that the extension T0 ⊆ T1 is local if it satisfies condition (Locf ).

4.2. Embeddability and locality. In [15, 17] we showed that embeddability of certain
weak partial models into total models implies locality of an extension. Consider condition:
 (Embfd
      w ) Every A ∈ PModw (Σ1 , T1 ) in which all extension functions have a
          finite definition domain weakly embeds into a total model of T1 .
Definition 4.4. A non-ground clause is Σ1 -flat if function symbols (including constants) do
not occur as arguments of functions in Σ1 . A Σ1 -flat non-ground clause is called Σ1 -linear if
whenever a variable occurs in two terms in the clause which start with function symbols in
Σ1 , the two terms are identical, and if no term which starts with a function in Σ1 contains
two occurrences of the same variable.
Theorem 4.5 ([15, 17]). Let K be a set of clauses in which all terms starting with a function
symbol in Σ1 are flat and linear. If the extension T0 ⊆ T1 satisfies (Embfd
                                                                          w ) then it satisfies
(Locf ).


4.3. Examples. Using a variant of Theorem 4.5, in [15] we gave several examples of local
theory extensions: any extension of a theory with free functions; extensions with selector
functions for a constructor which is injective in the base theory; extensions of R with a
Lipschitz function in a point x0 ; extensions of partially ordered theories – in a class Ord
consisting of the theories of posets, (dense) totally-ordered sets, semilattices, (distributive)
lattices, Boolean algebras, or R – with a monotone function f , i.e. satisfying:
                              n
                              ^
               (Mon(f ))        xi ≤ yi → f (x1 , . . . , xn ) ≤ f (y1 , . . . , yn ).
                                i=1
Generalized monotonicity conditions – combinations of monotonicity in some arguments
and antitonicity in other arguments – were studied in [17]. Below, we give some additional
examples with particular relevance in verification.
Theorem 4.6. We consider the following base theories T0 : (1) P (posets), (2) T O (totally-
ordered sets), (3) SLat (semilattices), (4) DLat (distributive lattices), (5) Bool (Boolean
algebras), (6) the theory R of reals resp. LI(R) (linear arithmetic over R), or the theory Q
of rationals resp. LI(Q) (linear arithmetic over Q), or (a subtheory of ) the theory of integers
(e.g. Presburger arithmetic). The following theory extensions are local:
(a) Extensions of any theory T0 for which ≤ is reflexive with functions satisfying bounded-
     ness (Boundt (f )) or guarded boundedness (GBoundt (f )) conditions
       (Boundt (f ))     ∀x1 , . . . , xn (f (x1 , . . . , xn ) ≤ t(x1 , . . . , xn ))
       (GBoundt (f )) ∀x1 , . . . , xn (φ(x1 , . . . , xn ) → f (x1 , . . . , xn ) ≤ t(x1 , . . . , xn )),
                         INTERPOLATION IN LOCAL THEORY EXTENSIONS                                   9




    where t(x1 , . . . , xn ) is a term in the base signature Π0 and φ(x1 , . . . , xn ) a conjunction
    of literals in the signature Π0 , whose variables are in {x1 , . . . , xn }.
(b) Extensions of any theory T0 in (1)–(6) with Mon(f ) ∧ Boundt (f ), if t(x1 , . . . , xn ) is a
    term in the base signature Π0 in the variables x1 , . . . , xn such that for every model of
    T0 the associated function is monotone in the variables x1 , . . . , xn .
(c) Extensions of any theory in (1)–(6) with functions satisfying Leq(f, g) ∧ Mon(f ).
       (Leq(f, g)) ∀x1 , . . . , xn ( ni=1 xi ≤ yi → f (x1 , . . . , xn ) ≤ g(y1 , . . . , yn ))
                                      V

(d) Extensions of any totally-ordered theory above (i.e. (2) and (6)) with functions satisfying
    SGc(f, g1 , . . . , gn ) ∧ Mon(f, g1 , . . . , gn ).
       (SGc(f, g1 , . . . , gn )) ∀x1 , . . . , xn , x( ni=1 xi ≤ gi (x) → f (x1 , . . . , xn ) ≤ x)
                                                        V

(e) Extensions of any theory in (1)–(3) with functions satisfying SGc(f, g1 ) ∧ Mon(f, g1 ).
All the extensions above satisfy condition Locf .
Proof. The proof is given in Appendix B.


4.4. Hierarchic reasoning in local theory extensions. Let T0 ⊆ T1 =T0 ∪ K be a local
theory extension. To check the satisfiability of a set G of ground clauses with respect to
T1 we can use the following hierarchical procedure to reduce the problem to a satisfiability
problem in the base theory (for details cf. [15]):
Step 1: Use locality. By the locality condition, we know that G is unsatisfiable with
  respect to T1 if and only if K[G] ∧ G has no weak partial model in which all the subterms
  of K[G] ∧ G are defined, and whose restriction to Π0 is a total model of T0 .
Step 2: Flattening and purification. As in K[G] and G the functions in Σ1 have as ar-
  guments only ground terms, K[G] ∧ G can be purified and flattened by introducing new
  constants for the arguments of the extension functions as well as for the (sub)terms
  t = f (g1 , . . . , gn ) starting with extension functions f ∈ Σ1 , together with new corre-
  sponding definitions ct ≈ t. The set of clauses thus obtained has the form K0 ∧ G0 ∧ D,
  where D is a set of ground unit clauses of the form f (c1 , . . . , cn ) ≈ c, where f ∈ Σ1 and
  c1 , . . . , cn , c are constants, and K0 , G0 are clauses without function symbols in Σ1 .
Step 3: Reduction to testing satisfiability in T0 . We reduce the problem of testing satisfia-
  bility of G with respect to T1 to a satisfiability test in T0 as shown in Theorem 4.7.

Theorem 4.7 ([15]). Assume that T0 ∪ K is a local extension of T0 with a set K of clauses.
With the notation above, the following are equivalent:
(1) T0 ∧ K ∧ G has a model.
(2) T0 ∧ K[G] ∧ G has a weak partial model where all terms in st(K, G) are defined.
(3) T0 ∧ K0 ∧ G0 ∧ D has a weak partial model with all terms in st(K, G) defined.
(4) T0 ∧ K0 ∧ G0 ∧ Con[D]0 has a (total) Σ0 -model, where
                 ^ ^ n
       Con[D]0 = { ci ≈ di → c ≈ d | f (c1 , . . . , cn ) ≈ c, f (d1 , . . . , dn ) ≈ d ∈ D} .
                        i=1
    is the set of instances of the congruence axioms for the functions in Σ1 corresponding
    to the extension terms in D.
10                                V. SOFRONIE-STOKKERMANS




Example 4.8. Let T1 = SLat ∪ SGc(f, g) ∪ Mon(f, g) be the extension of the theory of
semilattices with two monotone functions f, g satisfying the semi-Galois condition SGc(f, g).
Consider the following ground formulae A, B in the signature of T1 :
                      A : d ≤ g(a) ∧ a ≤ c          B : b ≤ d ∧ f (b) 6≤ c .
where c and d are shared constants. By Theorem 4.6(e), T1 is a local extension of the theory
of semilattices. To prove that A ∧ B |=T1 ⊥ we proceed as follows:
Step 1: Use locality. By the locality condition, A ∧ B is unsatisfiable with respect to
   SLat ∧ SGc(f, g) ∧ Mon(f, g) iff SLat ∧ SGc(f, g)[A ∧ B] ∧ Mon(f, g)[A ∧ B] ∧ A ∧ B has
   no weak partial model in which all terms in A and B are defined. The extension terms
   occurring in A ∧ B are f (b) and g(a), hence:
              Mon(f, g)[A ∧ B] = {a ≤ a → g(a) ≤ g(a), b ≤ b → f (b) ≤ f (b)}
              SGc(f, g)[A ∧ B] = {b ≤ g(a) → f (b) ≤ a}
Step 2: Flattening and purification. We purify and flatten the formula SGc(f, g)∧Mon(f, g)
  by replacing the ground terms starting with f and g with new constants. The clauses are
  separated into a part containing definitions for terms starting with extension functions,
  DA ∧ DB , and a conjunction of formulae in the base signature, A0 ∧ B0 ∧ SGc0 ∧ Mon0 .
Step 3: Reduction to testing satisfiability in T0 . As the extension SLat ⊆ T1 is local, by
  Theorem 4.7 we know that

            A ∧ B |=T1 ⊥     if and only if        A0 ∧ B0 ∧ SGc0 ∧ Mon0 ∧ Con0
                                                is unsatisfiable with respect to SLat ,

     where Con0 = Con[A ∧ B]0 consists of the flattened form of those instances of the congru-
     ence axioms containing only f - and g-terms which occur in DA or DB , and SGc0 ∧ Mon0
     consists of those instances of axioms in SGc(f, g) ∧ Mon(f, g) containing only f - and
     g-terms which occur in DA or DB .

     Extension       Base
     DA ∧ DB      A0 ∧ B0 ∧ SGc0 ∧ Mon0 ∧ Con0
     a1 ≈ g(a)    A0 = d ≤ a1 ∧ a ≤ c       SGc0 = b ≤ a1 → b1 ≤ a
     b1 ≈ f (b)   B0 = b ≤ d ∧ b1 6≤ c      ConA ∧ MonA = a ✁ a → a1 ✁ a1 , ✁ ∈ {≈, ≤}
                                            ConB ∧ MonB = b ✁ b → b1 ✁ b1 , ✁ ∈ {≈, ≤}

     It is easy to see that A0 ∧ B0 ∧ SGc0 ∧ Mon0 ∧ Con0 is unsatisfiable with respect to T0 :
     A0 ∧ B0 entails b ≤ a1 , together with SGc0 this yields b1 ≤ a, which together with a ≤ c
     and b1 6≤ c leads to a contradiction.


                       5. Hierarchical Interpolant Computation
Let T0 ⊆ T1 = T0 ∪ K be a theory extension by means of a set of clauses K. Assume that
A ∧ B |=T1 ⊥, where A and B are two sets of ground clauses. Our goal is to find a ground
interpolant, that is a ground formula I containing only constants and extension functions
which are common to A and B such that
                                A |=T1 I      and   I ∧ B |=T1 ⊥.
                        INTERPOLATION IN LOCAL THEORY EXTENSIONS                                 11




Flattening and purification do not influence the existence of ground interpolants:
Lemma 5.1. Let A and B be two sets of ground clauses in the signature Πc . Let A0 ∧ DA
and B0 ∧DB be obtained from A resp. B by purification and flattening. If I is an interpolant
of (A0 ∧ DA ) ∧ (B0 ∧ DB ) then the formula I, obtained from I by replacing, recursively, all
newly introduced constants with the terms in the original signature which they represent, is
an interpolant for A ∧ B.
Proof. If I is an interpolant of (A0 ∧ DA ) ∧ (B0 ∧ DB ), then A0 ∧ DA |=T1 I and B0 ∧ DB ∧
I |=T1 ⊥. Let I be obtained from I by replacing, recursively, all newly introduced constants
with the terms in the original signature which they represent. Then:
  (i) A ∧ ¬I and A0 ∧ DA ∧ ¬I are equisatisfiable with respect to T1 , so A |=T1 I.
 (ii) B ∧ I and B0 ∧ DB ∧ I are equisatisfiable with respect to T1 , so B ∧ I |=T1 ⊥.

Therefore we can restrict without loss of generality to finding interpolants for the purified
and flattened conjunction of formulae (A0 ∧ DA ) ∧ (B0 ∧ DB ).
    We focus on interpolation in local theory extensions. Let T0 ⊆ T1 = T0 ∪ K be a local
theory extension. From Theorem 4.7 we know that in such extensions hierarchical reasoning
is possible: if A and B are sets of ground clauses in a signature Πc , and A0 ∧ DA (resp.
B0 ∧ DB ) are obtained from A (resp. B) by purification and flattening then:
(A0 ∧ DA ) ∧ (B0 ∧ DB ) |=T1 ⊥        if and only if      K0 ∧ A0 ∧ B0 ∧ Con[DA ∧ DB ]0 |=T0 ⊥,
where K0 is obtained from K[DA ∧ DB ] by replacing the Σ1 -terms with the corresponding
constants contained in the definitions DA and DB and
                  ^ ^  n
Con[DA ∧ DB ]0 = { ci ≈ di → c ≈ d | f (c1 , . . . , cn ) ≈ c, f (d1 , . . . , dn ) ≈ d ∈ DA ∪ DB }.
                        i=1
In general we cannot use Theorem 4.7 for generating a ground interpolant because:
   (i) K[DA ∧ DB ] (hence also K0 ) may contain free variables.
  (ii) If some clause in K contains two or more different extension functions, it is unlikely
       that these extension functions can be separated in the interpolants.
 (iii) The clauses in K[DA ∧ DB ] and the instances of congruence axioms (and therefore the
       clauses in K0 ∧ Con[DA ∧ DB ]0 ) may contain combinations of constants and extension
       functions from A and B.
To avoid (i), we will need to take into account only extensions with sets K of clauses in
which all variables occur below some extension term. To solve (ii), we define a relation ∼
between extension functions, where f ∼ g if f and g occur in the same clause in K. This
defines an equivalence relation ∼ on Σ1 . We henceforth consider that a function f ∈ Σ1 is
common to A and B if there exist g, h ∈ Σ1 such that f ∼ g, f ∼ h, g occurs in A and h
occurs in B.
Example 5.2. Consider the reduction to the base theory in Example 4.8. We explain the
problems mentioned above.
 Ad (ii) As SGc(f, g) contains occurrences of both f and g, it is not likely to find an
         interpolant with no occurrence of f and g, even if g only occurs in A and f only
         occurs in B. We therefore assume that f ∼ g, i.e. that both f and g are shared.
Ad (iii) The clause b ≤ a1 → b1 ≤ a of SGc0 is mixed, i.e. contains combinations of
         constants from A and B.
12                                V. SOFRONIE-STOKKERMANS




The idea for solving problem (iii) is presented below.

5.1. Main Idea. The idea of our approach is to separate mixed instances of axioms in
K0 , or of congruence axioms in Con[DA ∧ DB ]0 , into an A-part and a B-part. This is,
if A ∧ B |=T1 ⊥ we find a set T of Σ0 ∪Σ1 -terms containing only constants and extension
functions common to A and B, such that K[A ∧ B] can be separated into a part K[A, T ]
consisting of instances with extension terms occurring in A and T , and a part K[B, T ]
containing only instances with extension terms in B and T , such that:
               K[A, T ] ∧ A0 ∧ Con[DA ∧ DT ] ∧ K[B, T ] ∧ B0 ∧ Con[DB ∧ DT ]
has no weak partial model where all ground terms in K, DA , DB , T are defined.
Example 5.3. Consider the conjunction A0 ∧ DA ∧ B0 ∧ DB ∧ Con[DA ∧ DB ]0 ∧ Mon0 ∧ SGc0
in Example 4.8. The A and B-part share the constants c and d, and no function symbols.
However, as f and g occur together in SGc, f ∼ g, so they are considered to be all shared.
(Thus, the interpolant is allowed to contain both f and g.) We obtain a separation for the
clause b ≤ a1 → b1 ≤ a of SGc0 as follows:
   (i) We note that A0 ∧ B0 |= b ≤ a1 .
  (ii) We can find an SLat-term t containing only shared constants of A0 and B0 such that
       A0 ∧ B0 |= b ≤ t ∧ t ≤ a1 . (Indeed, such a term is t = d.)
 (iii) We show that, instead of the axiom b ≤ g(a) → f (b) ≤ a, whose flattened form is in
       SGc0 , we can use, without loss of unsatisfiability:
       (1) an instance of the monotonicity axiom for f : b ≤ d → f (b) ≤ f (d),
       (2) another instance of SGc, namely: d ≤ g(a) → f (d) ≤ a.
       For this, we introduce a new constant cf (d) for f (d) (its definition, cf (d) ≈ f (d), is
                                                                       A ∧ HB of the congru-
       stored in a set DT ), and the corresponding instances Hsep = Hsep        sep
       ence, monotonicity and SGc(f, g)-axioms, which are now separated into an A-part
          A :d ≤a →c                                 B
       (Hsep         1     f (d) ≤ a) and a B-part (Hsep : b ≤ d → b1 ≤ cf (d) ). We thus obtain
       a separated conjunction A0 ∧ B 0 (where A0 = Hsep   A ∧ A and B = HB ∧ B ), which
                                                                 0       0        sep  0
       can be proved to be unsatisfiable in T0 = SLat.
 (iv) To compute an interpolant in SLat for A0 ∧ B 0 note that A0 is logically equivalent
       to the conjunction of unit literals d ≤ a1 ∧ a ≤ c ∧ cf (d) ≤ a and B 0 is logically
       equivalent to b ≤ d ∧ b1 6≤c ∧ b1 ≤ cf (d) . An interpolant is I0 = cf (d) ≤ c.
  (v) By replacing the new constants with the terms they denote we obtain the interpolant
       I = f (d) ≤ c for A ∧ B.
Note that in order to be able to perform in general the succession of steps in Example 5.3
it is necessary that K0 is ground and the theory extension and the base theory have certain
properties:
   (i) it always is possible to find an axiom instance such that all its premises are entailed
       by A0 ∧ B0 ;
  (ii) we can find separating terms (in the joint signature) for the entailed literals;
 (iii) the axioms come in pairs with corresponding monotonicity axioms which are then used
       to separate mixed rules;
 (iv) we can compute ground interpolants in T0 .
                          INTERPOLATION IN LOCAL THEORY EXTENSIONS                                   13




Theory extensions satisfying these conditions appear in a natural way in a wide variety of
applications ranging from knowledge representation to verification. In what follows we will
give several examples of theories with properties (i)–(iv).

5.2. Examples of theory extensions with hierarchic interpolation. We identify a
class of theory extensions for which interpolants can be computed hierarchically (and effi-
ciently) using a procedure for generating interpolants in the base theory T0 . This allows
us to exploit specific properties of T0 for obtaining simple interpolants in T1 . We make the
following assumptions about T0 :
Assumption 1: T0 is convex with respect to the set Pred of all predicates (including
   equality ≈), i.e., for all conjunctions Γ of ground atoms, relations          R1 , . . . , Rm ∈ Pred
   and ground tuples of corresponding arity t1 , . . . , tn , if Γ |=T0 m
                                                                       W
                                                                        i=1 R i (t i ) then there exists
   j ∈ {1, . . . , m} such that Γ |=T0 Rj (tj ).
Assumption 2: T0 is P -interpolating with respect to P ⊆ Pred, i.e. for all conjunctions A
   and B of ground literals, all binary predicates R ∈ P and all constants a and b such that
   a occurs in A and b occurs in B (or vice versa), if A ∧ B |=T0 aRb then there exists a
   term t containing only constants common to A and B with A ∧ B |=T0 aRt ∧ tRb. (If we
   can always find a term t containing only constants common to A and B with A |=T0 aRt
   and B |=T0 tRb we say that T0 is strongly P -interpolating.)
Assumption 3: T0 has ground interpolation.
Some examples of theories satisfying these properties are given below.
Theorem 5.4. The following theories have ground interpolation and are convex and P -
interpolating with respect to the indicated set P of predicate symbols:
(1) The theory of EQ of pure equality without function symbols (for P = {≈}).
(2) The theory PoSet of posets (for P = {≈, ≤}).
(3) Linear rational arithmetic LI(Q) and linear real arithmetic LI(R) (convex with respect
    to P = {≈}, strongly P -interpolating for P = {≤}).
(4) The theories Bool of Boolean algebras, SLat of semilattices and DLat of distributive
    lattices (strongly P -interpolating for P = {≈, ≤}).
Proof. The proof is given in Appendix C.
    We make the following assumption about the extension T1 of T0 .
Assumption 4: T1 = T0 ∪ K is a local extension of T0 with the property that in all clauses
 in K each variable occurs also below some extension function.
For the sake of simplicity we only consider sets A, B of unit clauses, i.e. conjunctions of
ground literals. This is not a restriction, since if we can obtain interpolants for conjunctions
of ground literals then we also can construct interpolants for conjunctions of arbitrary
clauses by using standard methods3 discussed e.g. in [8] or [19].
    By Lemma 5.1, we can restrict without loss of generality to finding an interpolant for
the purified and flattened conjunction of unit clauses A0 ∧ B0 ∧ DA ∧ DB . By Theorem 4.7,
   A0 ∧ DA ∧ B0 ∧ DB |=T1 ⊥           if and only if    K0 ∧ A0 ∧ B0 ∧ Con[DA ∧ DB ]0 |=T0 ⊥,
  3E.g. in a DPLL-style procedure partial interpolants are generated for the unsatisfiable branches and
then recombined using ideas of Pudlák.
14                                       V. SOFRONIE-STOKKERMANS




where K0 is obtained from K[DA ∧ DB ] by replacing the Σ1 -terms with the corresponding
constants contained in the definitions DA ∧ DB and
                  ^ ^  n
Con[DA ∧ DB ]0 = { ci ≈ di → c ≈ d | f (c1 , . . . , cn ) ≈ c, f (d1 , . . . , dn ) ≈ d ∈ DA ∪ DB }.
                            i=1
In general, Con[DA ∧ DB ]0 = ConA           B                       A      B
                                    0 ∧ Con0 ∧ Conmix and K0 = K0 ∧ K0 ∧ Kmix , where
ConA     A                                                                       B   B
    0 , K0 only contain extension functions and constants which occur in A, Con0 , K0 only
contain extension functions and constants which occur in B, and Conmix , Kmix contain mixed
clauses with constants occurring in both A and B. Our goal is to separate Conmix and Kmix
into an A-local and a B-local part. We show that, under Assumptions 1 and 2, Conmix
can always be separated, and Kmix can be separated if K contains the following type of
combinations of clauses:
                 
                     x1 R1 s1 ∧ · · · ∧ xn Rn sn → f (x1 , . . . , xn ) R g(y1 , . . . , yn )
                                                                                                      (5.1)
                     x1 R1 y1 ∧ · · · ∧ xn Rn yn → f (x1 , . . . , xn ) R f (y1 , . . . , yn )
          where n ≥ 1, x1 , . . . , xn are variables, R1 , . . . , Rn , R are binary relations with
          R1 , . . . , Rn ∈ P and R transitive, and each si is either a variable among the
          arguments of g, or a term of the form fi (z1 , . . . , zk ), where fi ∈ Σ1 and all
          the arguments of fi are variables occurring among the arguments of g. 4
We therefore make the following additional assumption about the theory extension T1 :
Assumption 5: T1 = T0 ∪ K is an extension of T0 with a set of clauses K which only
 contains combinations of clauses of type (5.1).

Example 5.5. The following local extensions satisfy Assumptions 4 and 5:
(a) Any extension with free functions (K = ∅).
(b) Extensions of any theory in Ord (cf. Section 4.3) with monotone functions.
(c) Extensions of any totally-ordered theory in Ord with functions satisfying
                                  SGc(f, g1 , . . . , gn ) ∧ Mon(f, g1 , . . . , gn ).
(d) Extensions of theories in Ord with functions satisfying
                                           SGc(f, g1 ) ∧ Mon(f, g1 ).
(e) Extensions of theories in Ord with functions satisfying Leq(f, g) ∧ Mon(f ).
Remark 5.6. If the clauses in K are of type (5.1), then K0 = K0A ∧ K0B ∧ Kmix , where
K0A = {( ni=1 ci Ri di ) → cRd | ( ni=1 xi Ri si (y)) → f (x1 , . . . , xn ) R g(y) ∈ K,
        V                         V
                                  di ≈ si (e) ∈ DA , d ≈ g(e) ∈ DA , c ≈ f (c1 , . . . , cn ) ∈ DA }∪
      {( ni=1 ci Ri di ) → cRd | ( ni=1 xi Ri yi ) → f (x1 , . . . , xn ) R f (y1 , . . . , yn ) ∈ K,
        V                         V
                                  d ≈ f (d1 , . . . , dn ) ∈ DA , c ≈ f (c1 , . . . , cn ) ∈ DA },
     4More general types of clauses, in which instead of variables we can consider arbitrary base terms, can
be handled if T0 has a P -interpolation property for terms instead of constants. Due to space limitations,
such extensions are not discussed here.
                           INTERPOLATION IN LOCAL THEORY EXTENSIONS                                        15




similarly for K0B , and
Kmix = { ni=1 ci Ri di → cRd | ni=1 xi Ri si (y) → f (x1 , . . . , xn ) R g(y) ∈ K, di ≈ si (e) ∈ DA ,
           V                      V
                                  d ≈ g(e) ∈ DA \DB , c ≈ f (c1 , . . . , cn ) ∈ DB \DA }∪
         { i=1 ci Ri di → cRd | ni=1 xi Ri yi → f (x1 , . . . , xn ) R f (y1 , . . . , yn ) ∈ K,
           Vn                     V
                                  d ≈ f (d1 , . . . , dn ) ∈ DA \DB , c ≈ f (c1 , . . . , cn ) ∈ DB \DA }∪
         { i=1 ci Ri di → cRd | ni=1 xi Ri si (y) → f (x1 , . . . , xn ) R g(y) ∈ K, di ≈ si (e) ∈ DB ,
           Vn                     V
                                  d ≈ g(e) ∈ DB \DA , c ≈ f (c1 , . . . , cn ) ∈ DA \DB }∪
           Vn                     Vn
         { i=1 ci Ri di → cRd | i=1 xi Ri yi → f (x1 , . . . , xn ) R f (y1 , . . . , yn ) ∈ K,
                                  d ≈ f (d1 , . . . , dn ) ∈ DB \DA , c ≈ f (c1 , . . . , cn ) ∈ DA \DB }.
All clauses in K0 are of the form C = ni=1 ci Ri di →c R d, where Ri ∈ P , R is transitive,
                                              V
and ci , di , c, d are constants. Moreover, the cardinality of K0 ∪ Con[DA ∧ DB ]0 is quadratic
in the size of A ∧ B for a fixed K.

         Vn 5.7. Assume that T0 satisfies Assumptions
Proposition
                                                    c
                                                              1 and 2. Let H be a set of Horn
clauses ( i=1 ci Ri di ) → cRd in the signature Π0 (with R transitive and Ri ∈ P ) which are
instances of flattened and purified clauses of type (5.1) and of congruence axioms. Let A0
and B0 be conjunctions of ground literals in the signature Πc0 such that A0 ∧ B0 ∧ H |=T0 ⊥.
Then H can be separated into an A and a B part by replacing the set Hmix of mixed clauses
Hmix = {Vni=1 ci Ri di → cRd ∈ H | ci , c constants in A, di , d constants in B}∪
            V
           { ni=1 ci Ri di → cRd ∈ H | ci , c constants in B, di , d constants in A}
with a separated set of formulae Hsep . The following hold:
(1) There exists a set T of Σ0 ∪ Σc -terms containing only constants common to A0 and B0
    such that A0 ∧ B0 ∧ (H\Hmix ) ∧ Hsep |=T0 ⊥, where
    Hsep = {(V ni=1 ci Ri ti → cRcf (t1 ,...,tn ) ) ∧ ( ni=1 ti Ri di → cf (t1 ,...,tn ) Rd) |
                     V                                         V
                        n
                        i=1 ci Ri di → cRd ∈ Hmix , di ≈ si (e1 , . . . , en ), d ≈ g(e1 , . . . , en ) ∈ DB ,
                     c ≈ f (c1 , . . . , cn ) ∈ DA or vice versa } = Hsep  A ∧ HB
                                                                                   sep
    and cf (t1 ,...,tn ) are new constants in Σc (considered to be common) introduced for the
    corresponding terms f (t1 , . . . , tn ).
(2) A0 ∧ B0 ∧ (H\Hmix ) ∧ Hsep is logically equivalent with respect to T0 with the following
    separated conjunction of ground literals:
                                         V
    A0 ∧ B 0 = A0 ∧ B0 ∧ V{cRd | Γ→cRd ∈ H\Hmix }
                                  ∧        {cRcf (t) ∧ cf (t) Rd | (Γ → cRcf (t) ) ∧ (Γ → cf (t) Rd) ∈ Hsep }.
(3) If T0 is strongly P -interpolating then the A-part (B-part) of A0 ∧ B0 ∧ (H\Hmix ) ∧
    Hsep |=T0 ⊥ is logically equivalent with A0 (resp. B 0 ) above.
Proof. We prove (1) and (2) simultaneously by induction on the number of clauses in H.
If H = ∅ then the initial problem is already separated into an A and a B part so we are
done: we can choose T = ∅. Assume that H contains at least one clause, and that for every
H′ with fewer clauses and every conjunctions of literals A′0 , B0′ with A′0 ∧ B0′ ∧ H′ |=T0 ⊥, (1)
and (2) hold.
    Let D beVthe set of all atoms ci Ri di occurring in premises of clauses in H. As every model
of A0 ∧ B0 ∧ (cRd)∈D ¬(cRd) is also a model for H ∧ A0 ∧ B0 |=T0 ⊥ and H ∧ A0 ∧ B0 |=T0 ⊥,
A0 ∧B0 ∧ (cRd)∈D ¬(cRd) |=T0 ⊥. Let (A0 ∧B0 )+ be the conjunction of all atoms in A0 ∧B0 ,
         V
16                                        V. SOFRONIE-STOKKERMANS




and (A0 ∧ B0 )− be the set of all negative literals in A0 ∧ B0 . Then
                                          _                  _
                     (A0 ∧ B0 )+ |=T0           (cRd) ∨             L.
                                                   (cRd)∈D             ¬L∈(A0 ∧B0 )−

By Assumption 1, T0 is convex with respect to Pred. Moreover, (A0 ∧ B0 )+ is a conjunction
of positive literals. Therefore, either
  (i) (A0 ∧ B0 )+ |= L for some L ∈ (A0 ∧ B0 )− (then A0 ∧ B0 is unsatisfiable and hence
      entails any atom ci Ri di ), or
 (ii) there exists (c1 R1 d1 ) ∈ D such that (A0 ∧ B0 )+ |=T0 c1 R1 d1 .
Case 1: A0 ∧ B0 is unsatisfiable. In this case (1) and (2) hold for T = ∅.
Case 2: A0 ∧B0 is satisfiable. Then A0 ∧B0 is logically equivalent in T0 with A0 ∧B0 ∧ci Ri di .
If it is not the case that by adding ci Ri di all premises of some rule in H
                                                                           Vbecome true we repeat
the procedure for D1 = D\(c1 R1 d1 ): Again in this case A0 ∧ B0 ∧ (cRd)∈D1 ¬(cRd) |=T0 ⊥
(if it has a model then A0 ∧ B0 ∧ H has one), and as before, using convexity we infer that
either A0 ∧ B0 is unsatisfiable (which cannot be the case) or there exists c2 R2 d2 ∈ D1 with
A0 ∧ B0 |=T0 c2 R2 d2 . We can repeat the processVuntil all the premises of some clause in H
are proved to be entailed by A0 ∧ B0 . Let C = ni=1 ci Ri di → cRd be such a clause.
Case 2a. Assume that C contains only constants occurring in A or only constants occurring
in B. Then A0 ∧B0 ∧H is equivalent with respect to T0 with A0 ∧B0 ∧(H\C)∧c ≈ d. By the
induction hypothesis for A′0 ∧ B0′ = A0 ∧ B0 ∧ c ≈ d and H′ = H\{C}, we know that there
exists T ′ such that A′0 ∧ B0′ ∧ (H′ \H′ mix ) ∧ H′ sep |=⊥, and (2) holds too. Then, for T = T ′ ,
A′0 ∧ B0′ ∧ (H′ \H′ mix ) ∧ H′ sep is logically equivalent to A0 ∧ B0 ∧ (H\Hmix ) ∧ Hsep , so (1)
holds. In order to prove (2), note that, by definition, Hmix   ′               ′
                                                                 = Hmix and Hsep  = Hsep . By the
                              ′    ′    ′   ′        ′
induction hypothesis, A0 ∧ B0 ∧ (H \H mix ) ∪ H sep is logically equivalent to a corresponding
                     ′    ′
conjunction A0 ∧ B 0 containing as conjuncts all literals in A′0 and B0′ and all conclusions
of rules in H′ \H′ mix and H′ sep . On the other hand, A′0 ∧ B0′ is logically equivalent to
A0 ∧ B0 ∧ (cRd), where (cRd) is the conclusion of the rule C ∈ H\Hmix . This proves (2).
Case 2b. Assume now that C is mixed, for instance that c1 , . . . , cn , c are constants in A and
d1 , . . . , dn , d are
                    V constants in B. Assume that C is obtained from an instance of a clause
of the form ni=1 xi Ri si (y) → f (x1 , . . . , xn )Rg(y). (The case when C corresponds to an
instance of a monotonicity axiom is similar.) This means that there exist c ≈ f (c1 , . . . , cn ) ∈
DA and di ≈ si (e), d ≈ g(e) ∈ DB . C was chosen such that for each premise ci Ri di of C,
A0 ∧ B0 |=T0 ci Ri di , and – by Assumption 2 – T0 is P -interpolating. Thus, there exist terms
t1 , . . . , tn containing only constants common to A0 and B0 such that for all i ∈ {1, . . . , n}
                                      A0 ∧ B0 |=T0 ci Ri ti ∧ ti Ri di .                                               (5.2)
Let cf (t1 ,...,tn ) be a new constant, denoting the term f (t1 , . . . , tn ), and let
                    n
                    ^                                                      n
                                                                           ^
            CA =         ci Ri ti →cRcf (t1 ,...,tn )     and     CB =           ti Ri di →cf (t1 ,...,tn ) Rd.
                   i=1                                                     i=1
                                                                      n
                                                                      ^
Thus, CA corresponds to the monotonicity axiom                             ci Ri ti →f (c1 , . . . , cn )Rf (t1 , . . . , tn ),
                                                                     i=1
                                                  n
                                                  ^
whereas CB corresponds to the rule                      ti Ri si (e)→f (t1 , . . . , tn )Rg(e). As R is transitive,
                                                 i=1
                          INTERPOLATION IN LOCAL THEORY EXTENSIONS                                             17




by (5.2) the following holds:
                                                          n
                                                          ^                           n
                                                                                      ^
          A0 ∧ B0 ∧ CA ∧ CB |=|T0          A0 ∧ B0 ∧ (          ci Ri ti ∧ CA ) ∧ (       ti Ri di ∧ CB )
                                                          i=1                      i=1
                                   |=|T0   A0 ∧ B0 ∧ cRcf (t1 ,...,tn ) ∧ cf (t1 ,...,tn ) Rd
                                   |=T0    A0 ∧ B0 ∧ cRd
              (where |=|T0 stands for logical equivalence with respect to T0 ).
Hence, A0 ∧ V       B0 ∧ CA ∧ CB ∧ (H\C) |=T0 A0 ∧ B0 ∧ cRd ∧ (H\C). On the other hand, as
A0 ∧ B0 |=T0 ni=1 ci Ri di , A0 ∧ B0 ∧ H is logically equivalent with A0 ∧ B0 ∧ cRd ∧ (H\C), so
A0 ∧ B0 ∧ CA ∧ CB ∧ (H\C) |=T0 ⊥. By the induction hypothesis for A0 ∧ B0 ∧ cRcf (t1 ,...,tn ) ∧
cf (t1 ,...,tn ) Rd and H′ = H\C we know that there exists a set T ′ of terms such that A0 ∧ B0 ∧
                                                            ′
cRcf (t1 ,...,tn ) ∧ cf (t1 ,...,tn ) Rd ∧ (H′ \H′ mix ) ∧ Hsep |=⊥, and also (2) holds. Then (1) holds for
           ′
T = T ∪{t1 , . . . , tn }. (2) can be proved similarly using the induction hypothesis.
(3) follows from the same induction schema taking into account the fact that, by strong
interpolation, always if A0 ∧ B0 |= ci Ri di there exists ti (containing only constants common
                                                                  5
to A0 and     VnB0 ) with A0 |= ci Ri ti and B0 |= ti Ri di . Then A0 is logically equivalent (in T0 )
to A0 ∧ i=1 ci Ri ti , hence A0 ∧ CA is logically equivalent to A0 ∧ cRcf (t1 ,...,tn ) . (Similarly,
B0 is logically equivalent to B0 ∧ ni=1 ti Ri di , so B0 ∧ CB is logically equivalent to B0 ∧
                                                 V
cf (t1 ,...,tn ) Rd.) By using the induction hypothesis, (3) follows easily.

An immediate consequence of Proposition 5.7 is Proposition 5.8.
Proposition 5.8. Assume T0 satisfies Assumptions 1 and 2, the extension T0 ⊆ T0 ∪ K
satisfies Assumptions 4 and 5, and K0 ∧ A0 ∧ B0 ∧ Con[DA ∧ DB ]0 |=T0 ⊥. Then there exists
a set T of Σ0 ∪ Σc -terms containing only constants common to A0 and B0 such that (if
ConD0 = Con0
             DA
                ∧ ConDB                 D
                     0 =Con0sep and K0 = K0
                                              DA ∧ KDB =K
                                                      0     0sep ):

                 K0A ∧ K0B ∧ K0D ∧ A0 ∧ B0 ∧ ConA      B      D
                                                0 ∧ Con0 ∧ Con0 |=T0 ⊥.                                     (5.3)
As before, Σc contains the new constants cf (t1 ,...,tn ) , considered to be common to A0 and B0 ,
introduced for terms f (t1 , . . . , tn ), with t1 , . . . , tn ∈ T .
Proof. If K only contains combinations of clauses of type (5.1) then all clauses in K0 ∧
Con[DA ∧ DB ]0 satisfy the restrictions on H in Proposition 5.7. Thus Proposition 5.7 holds
for H = K0 ∧ Con[DA ∧ DB ]0 . Therefore there exists a set T of Σ0 ∪ Σc -terms containing
only constants common to A0 and B0 such that A0 ∧ B0 ∧ (H\Hmix ) ∧ Hsep . The statement
of the theorem uses the description of H\Hmix , denoted before by K0A ∧ K0B , as well as of
Hsep as K0DA ∧ K0DB ∧ ConDA
                          0   ∧ ConDB0 .

Corollary 5.9. Assume that the extension T0 ⊆ T0 ∪ K satisfies Assumptions 1–5, and that
K0 ∧ A0 ∧ B0 ∧ Con[DA ∧ DB ]0 |=T0 ⊥. With the notation in Proposition 5.8 the following
holds:
(1) There exists a Πc0 -formula I0 containing only constants common to A0 , B0 with K0A ∧
    K0DA ∧ A0 ∧ ConA         DA              B
                    0 ∧ Con0 |=T0 I0 and K0 ∧ K0
                                                   DB ∧ B ∧ ConB ∧ ConDB ∧ I |= ⊥.
                                                          0     0      0      0 T0
(2) There exists a ground Πc -formula I containing only constants and function symbols
    which occur both in A and B such that A |=T1 I and B ∧ I |=T1 ⊥ .
  5In this case we may need to separate even pure A and B clauses in H as in Case 2b, in order to
guarantee the separate entailment from A0 and B0 .
18                                V. SOFRONIE-STOKKERMANS




Proof.
(1) is a direct consequence of Proposition 5.8, since K0A , K0AD , K0B , K0BD are ground and we
    assumed that T0 has ground interpolation.
(2) Let I be obtained from I0 by recursively replacing each constant ct introduced in the
    separation process with the term t. We show that I is an interpolant of (A0 ∧ DA ) ∧
    (B0 ∧ DB ) with respect to T1 , i.e. that (i) A0 ∧ DA |=T1 I and (ii) I ∧ B0 ∧ DB |=T1 ⊥.
       (i) Let (M, v) be a T1 -model that satisfies A0 ∧ DA . Being a model of T1 , (M, v)
           satisfies all instances of the axioms in K and of the congruence axioms in K0A ∧
           K0DA ∧ConA  0 ∧Con0
                               DA
                                  (and similarly for the B part). Thus, the restriction (M|Π0 , v)
           of (M, v) to the base theory satisfies K0A ∧ K0DA ∧ A0 ∧ ConA       DA
                                                                        0 ∧ Con0 , hence also I0 .
           We thus proved that A0 ∧ DA |=T1 I0 ∧ DA . It is easy to see that I0 ∧ DA |=T1 I.
      (ii) Assume that I ∧ B0 ∧ DB has a T1 -model (M, v). Then (M, v) |= I0 ∧ B0 ∧ DB ,
           so its reduct to Π0 is a model of T0 and of K0B ∧ K0DB ∧ B0 ∧ ConB   0 ∧ Con0
                                                                                         DB
                                                                                            ∧ I0 .
           This contradicts the fact that the set of clauses above is unsatisfiable with respect
           to T0 . Thus, I ∧ B0 ∧ DB |=T1 ⊥.


                   6. A procedure for hierarchical interpolation
We obtain a procedure for computing interpolants for A ∧ B described in Figure 1.
Lemma 6.1. Assume that the cycle in Step 2 of the procedure described in Figure 1 stops
after processing all mixed clauses in Hmix and moving their separated form into the set Hsep .
The following are equivalent:
(1) A0 ∧ DA ∧ B0 ∧ DB |=T1 ⊥.
(2) A0 ∧ B0 ∧ (H\Hmix ) ∧ Hsep |=T0 ⊥.
Proof. (1)⇒(2) is a consequence of Theorems 4.7 and Proposition 5.8. As the conjunction
in (2) corresponds to a subset of instances of K ∧ A0 ∧ DA ∧ B0 ∧ DB , (2) implies (1).

Note: If K0 ∧ A0 ∧ B0 ∧ Con[DA ∧ DB ]0 |=T0 ⊥ then no matter which terms are chosen
for separating mixed clauses in Con[DA ∧ DB ]0 ∧ K0 , we obtain a separated conjunction of
clauses unsatisfiable with respect to T0 . Lemma 6.1 shows that if the set of clauses obtained
when the procedure stops is satisfiable then A ∧ B was satisfiable, and conversely, so the
procedure can be used to test satisfiability and to compute interpolants at the same time.
(However, it is more efficient to first test A ∧ B |=T1 ⊥.)
Theorem 6.2. Let T0 be a theory with the following properties:
  Assumption 1: T0 is convex with respect to the set Pred (including equality ≈);
  Assumption 2: T0 is P -interpolating with respect to a subset P ⊆ Pred and the separat-
  ing terms ti can be effectively computed; and
  Assumption 3: T0 has ground interpolation
(note that we assume, in particular, that T0 satisfies a stronger form of Assumption 2).
Assume that the extension T1 = T0 ∪ K of T0 has the following properties:
  Assumption 4: T1 is a local extension of T0 ; and
                          INTERPOLATION IN LOCAL THEORY EXTENSIONS                                        19




   Given:      Local extension T0 ⊆ T1 = T0 ∪ K which satisfies Assumptions 1–5;
               Conjunctions A and B of literals over the signature of T1 such that A ∧ B |=T1 ⊥

   Task:       Find an interpolant for A ∧ B, i.e. a formula I with A |=T1 I and I ∧ B |=T1 ⊥.

   Method:
      Step 1: Purify.
        Using locality, flattening and purification we obtain a set H ∧ A0 ∧ B0 of formulae in the
        base theory, where H = K0 ∧ Con[DA ∧ DB ]0 .
        Let ∆ := T.
      Step 2: Reduction to an interpolation problem in the base theory.
        Repeat as long as possible:
          Let C∈H whose premise is entailed by A0 ∧ B0 ∧ ∆.
          If C is mixed, compute terms ti which separate the premises in C, and separate
                         the clause into an instance C1 of monotonicity and an instance C2
                         of a clause in K as in the proof of Case 2b in Prop. 5.7.
                         Remove C from H, and add C1 , C2 to Hsep and their conclusions to ∆.
          Otherwise move C to Hsep and add its conclusion to ∆.
      Step 3: Interpolation in the base theory.
        Compute an interpolant I0 in T0 for the separated formula A0 ∧ B 0 (logically equivalent to
        A0 ∧ B0 ∧ (H\Hmix ) ∧ Hsep ) obtained this way.
      Step 4: Construct interpolant for the initial problem.
        Construct an interpolant I in T1 from I0 by recursively replacing each constant ct introduced
        in the separation process with the term t, as explained in Corollary 5.9(2).




                 Figure 1: Procedure for hierarchical interpolant computation

  Assumption 5: K consists of the following type of combinations of clauses:
          
            x1 R1 s1 ∧ · · · ∧ xn Rn sn → f (x1 , . . . , xn ) R g(y1 , . . . , yn )
            x1 R1 y1 ∧ · · · ∧ xn Rn yn → f (x1 , . . . , xn ) R f (y1 , . . . , yn )
  where n ≥ 1, x1 , . . . , xn are variables, R1 , . . . , Rn , R are binary relations, R1 , . . . , Rn ∈ P ,
  R is transitive, and each si is either a variable among the arguments of g, or a term of
  the form fi (z1 , . . . , zk ), where fi ∈ Σ1 and all the arguments of fi are variables occurring
  among the arguments of g (i.e. combinations of clauses of type (5.1)).
For every conjunction A ∧ B of ground unit clauses in the signature Πc of T1 (possibly
containing additional constants) with A∧B |=T1 ⊥ the procedure for hierarchical interpolation
terminates and it computes an interpolant I for A ∧ B.
Proof. To prove termination note that at every execution of the loop in Step 2, the number
of mixed clauses decreases. All entailment tests in Step 2 are decidable (their complexity
is discussed separately). By Assumption (2’), terms ti which separate the premises can be
computed in finite time. This shows that Step 2 terminates. Termination of Steps 1, 3 and
4 is immediate.
     We now prove correctness. We know that A ∧ B |=T1 ⊥, so A0 ∧ DA ∧ B0 ∧ DB |=T1 ⊥.
Hence, by Lemma 6.1, when the cycle in Step 2 of the procedure terminates replacing the
20                                V. SOFRONIE-STOKKERMANS




set of clauses Hmix with Hsep , then A0 ∧ B0 ∧ (H\Hmix ) ∧ Hsep |=T0 ⊥. By construction, at
termination H\Hmix ∧Hsep contains only pure (unmixed) clauses. We can use the alternative
form of H\Hmix , denoted before by K0A ∧ K0B , as well as of Hsep as K0DA ∧ K0DB ∧ ConDA  0   ∧
ConDB
    0   . In Step 3 an  interpolant  I 0 containing only constants common   to   A0 , B 0  with
K0A ∧ K0DA ∧ A0 ∧ ConA           DA               B
                       0 ∧ Con0 |=T0 I0 and K0 ∧ K0
                                                        DB ∧ B ∧ ConB ∧ ConDB ∧ I |= ⊥
                                                               0      0        0       0 T0
is computed. In Step 4, a ground Πc -formula I containing only constants and function
symbols which occur both in A and B such that A |=T1 I and B ∧ I |=T1 ⊥ is constructed
starting from I as explained in Corollary 5.9. This is the interpolant of A ∧ B.

Complexity: Assume that in T0 for a formula of length n:
(a) interpolants can be computed in time g(n),
(b) P -interpolating terms can be computed in time h(n),
(c) entailment can be checked in time k(n).
The size n of the set of clauses obtained after the preprocessing phase is quadratic in the
size of the input. Under the assumptions (a), (b), (c) above the procedure above computes
an interpolant in time of order n · (k(n)+h(n))+g(n).
Remark 6.3. If T0 satisfies Assumptions 1 and 3 at the beginning of Section 5.2. and is
strongly P -interpolating, the procedure above can be changed (according to the proof of
Proposition 5.7(3)) to separate all clauses in H and store the conclusions of the separated
clauses in ∆ = ∆A ∪ ∆B . If K0 ∧ A0 ∧ B0 ∧ Con[DA ∧ DB ]0 |=T0 ⊥ then there exists a set
T of Σ0 ∪ Σc -terms containing only constants common to A0 and B0 , and common new
constants in a set Σc such that the terms in T can be used to separate Con[DA ∧ DB ]0 ∪ K0
into Hsep = (K0DA ∧ ConDA  0 ) ∧ (K0
                                    DB ∧ ConDB ), where:
                                               0
     Hsep = {( i=1 ci Ri ti → cRcf (t1 ,...,tn ) ) ∧ ( ni=1 ti Ri di → cf (t1 ,...,tn ) Rd) |
                 Vn                                   V
                 Vn                                            DA ∧ ConDA ) ∧ (KDB ∧ ConDB )
                   i=1 ci Ri di → cRd ∈ Con0 ∪ K0 } = (K0                0               0    0
such that for each premise ci Ri di of a rule in Con[DA ∧ DB ]0 ∪ K0 , at some step in the
procedure A0 ∧ B0 ∧ ∆A ∧ ∆B |= ci Ri di and there exists ti ∈ T such that A0 ∧ ∆A |= ci Ri ti
and B0 ∧ ∆B |= ti Ri di . In this case A0 ∧ K0DA ∧ ConDA  0    is logically equivalent to A0 , and
B0 ∧K0DB ∧ConDB0   is logically equivalent to B 0 , where A 0 B 0 are the following conjunctions
                                                             ,
of literals:
   A0 = A0 ∧ {cRcf (t) | conclusion of some clause (Γ → cRcf (t) ) ∈ K0DA ∪ ConDA
                 V
                                                                                          0 }
   B 0 = B0 ∧ {cf (t) Rd | conclusion of some clause (Γ → cf (t) Rd) ∈ K0 ∪ ConDBDB
                 V
                                                                                           0 }.
Thus, if for instance in T0 interpolants for conjunctions of ground literals are always again
conjunctions of ground literals, the same is also true in the extension.
Example 6.4. The following theory extensions have ground interpolation:
(a) Extensions of any theory in Theorem 5.4(1)–(4) with free function symbols.
(b) Extensions of the theories in Theorem 5.4(2),(4) with monotone functions.
(c) Extensions of the theories in Theorem 5.4(2),(4) with Leq(f, g) ∧ Mon(f ).
(d) Extensions of the theories in Theorem 5.4(2),(4) with SGc(f, g1 ) ∧ Mon(f, g1 ).
(e) Extensions of any theory in Theorem 5.4(1)–(4) with Boundt (f ) or GBoundt (f ) (where
    t is a term and φ a set of literals in the base theory).
(f) Extensions of the theories in Theorem 5.4(2),(4) with Mon(f ) ∧ Boundt (f ), if t is mono-
    tone in its variables.
                          INTERPOLATION IN LOCAL THEORY EXTENSIONS                           21




(g) R ∪ (Lλf ), the extension of the theory of reals with a unary function which is λ-Lipschitz
    in a point x0 , where (Lλf ) is ∀x |f (x) − f (x0 )| ≤ λ · |x − x0 |.
Proof. (a)–(d) are direct consequences of Corollary 5.9, since all sets of extension clauses
are of type (5.1). For extensions of linear arithmetic note that due to the totality of ≤ we
can always assume that A and B are positive, so convexity with respect to ≈ is sufficient
(cf. proof of Proposition 5.7). Also, in [11] we show that being P -interpolating with respect
to ≤ is sufficient in this case. (e)–(g) follow from Corollary 5.9 and the fact that if each
clause in K contains only one occurrence of an extension function, no mixed instances can
be generated when computing K[A ∧ B].


                                           7. Applications

7.1. Modular reasoning in local combinations of theories. Let Ti = T0 ∪ Ki , i = 1, 2
be local extensions of a theory T0 with signature Π0 = (Σ0 , Pred), where Σ0 = Σ1 ∩ Σ2 .
Assume that (a) all variables in Ki occur below some extension function, (b) the extension
T0 ⊆ T0 ∪ K1 ∪ K2 is local6, and (c) T0 has ground interpolation.
     Let G be a set of ground clauses in the signature Πc = (Σ0 ∪ Σ1 ∪ Σ2 ∪ Σc , Pred). G
can be flattened and purified, so we assume without loss of generality that G = G1 ∧ G2 ,
where G1 , G2 are flat and linear sets of clauses in the signatures Π1 , Π2 respectively, i.e.
for i = 1, 2, Gi = G0i ∧ G0 ∧ Di , where G0i and G0 are clauses in the base theory and Di
conjunctions of unit clauses of the form f (c1 , . . . , cn ) = c, f ∈ Σi \Σ0 .
Theorem 7.1. With the notations above, assume that G1 ∧ G2 |=T1 ∪T2 ⊥. Then there exists
a ground formula I, containing only constants shared by G1 and G2 , with G1 |=T1 ∪T2 I and
I ∧ G2 |=T1 ∪T2 ⊥.
Proof. By Theorem 4.7, the following are equivalent:
(1) T0 ∪ K1 ∪ K2 ∪ (G01 ∧ G0 ∧ D1 ) ∧ (G02 ∧ G0 ∧ D2 ) |=⊥,
(2) T0 ∪ K1 [G1 ] ∧ K2 [G2 ] ∧ (G01 ∧ G0 ∧ D1 ) ∧ (G02 ∧ G0 ∧ D2 ) |=⊥,
(3) K10 ∧ K20 ∧ (G01 ∧ G0 ) ∧ (G02 ∧ G0 ) ∧ Con1 ∧ Con2 |=T0 ⊥, where, for j = 1, 2,
             ^ ^  n
    Conj = { ci ≈ di → c ≈ d | f (c1 , . . . , cn ) ≈ c, f (d1 , . . . , dn ) ≈ d ∈ Dj },
                 i=1
and Ki0 is the formula obtained from Ki [Gi ] after purification and flattening, taking into
account the definitions from Di . Let A = K10 ∧(G01 ∧G0 )∧Con1 and B = K20 ∧(G02 ∧G0 )∧Con2 .
By assumption (a), A and B are both ground. As A and B have no extension function
symbols in common and only share the constants which G1 and G2 share, there exists an
interpolant I0 in the signature Π0 , containing only Σ0 -function symbols and only constants
shared by G1 , G2 , such that A |=T0 I0 and B ∧ I0 |=T0 ⊥. An interpolant for G1 ∧ G2 with
respect to T1 can now be obtained by replacing the newly introduced constants by the terms
they replaced.
  6If T is a ∀∃ theory then (b) is implied by (a) and the locality of T , T [16].
       0                                                               1   2
22                                  V. SOFRONIE-STOKKERMANS




By Remark 6.3, if T0 is strongly P -interpolating and has equational interpolation then I is a
conjunction of literals, so for modularly proving G1 ∧ G2 |=T1 ⊥ only conjunctions of ground
literals containing constants shared by G1 , G2 need to be exchanged between specialized
provers for T1 and T2 .

7.2. Terminological Databases. Consider the combination of databases in Section 2.1.
We prove that
                         Γ0 ∧ (T1 ∧ Γ1 ) ∧ (T2 ∧ Γ2 ) |=T ⊥ .                        (7.1)
                               S
where T is the extension SLat∪ f ∈R1 ∪R2 Mon(f ) of the theory of semilattices with 0 and
monotone functions corresponding to the rôles in R1 ∪R2 , where:

Γ0 = {organic ∧ inorganic ≈ 0,       organic ≤ substance,      inorganic ≤ substance}
T1 = {cat-oxydation ≈ substance ∧ catalyzes(oxydation)}
Γ1 = {reaction ≤ oxydation, cat-oxydation ≤ inorganic, cat-oxydation6≈0}, Γ2 = {enzyme 6≈ 0}
T2 = {reaction ≈ process ∧ produces(substance),         enzyme ≈ organic ∧ catalyzes(reaction)}
In order to find the mistake we look for an explanation for the inconsistency in the joint
language of the two databases. Based on results on hierarchical reasoning in extensions of
theories in [15] we can show that if we purify the problem by introducing definitions for
the terms starting with an extension role symbol we can reduce the satisfiability test to a
satisfiability test in the base theory. Thus, (7.1) is equivalent to the unsatisfiability of a set
of clauses over the theory of semilattices, namely: CT0 ∧ CT1 ∧ CΓ1 ∧ CT2 ∧ CΓ2 ∧ N where
CTi and CΓi are as in the table below (the shared symbols are underlined):
        Extension                                                Base
      (Definitions)                 Terminology(CT )                    Constraints(CΓ )
                                                                         organic ∧ inorganic ≈ 0
 0                                                                       organic ≤ substance
                                                                         inorganic ≤ substance
                                                                         reaction ≤ oxydation
 1    co ≈ catalyzes(oxydation)      cat-oxydation ≈ substance ∧ co      cat-oxydation ≤ inorganic
                                                                         cat-oxydation 6≈ 0
      ps ≈ produces(substance)       reaction ≈ process ∧ ps
 2                                                                      enzyme 6≈ 0
      cr ≈ catalyzes(reaction)       enzyme ≈ organic ∧ cr
The following instances of the congruence or monotonicity axioms need to be considered:
                      oxydation ✄ reaction → cp ✄ cr,     where ✄ ∈ {≈, ≤, ≥}.
They are not mixed. The conjunction of formulae in the base theory is unsatisfiable in the
theory of semilattices. It can be split into a part A containing only concepts in AChem
and a part B containing only concepts in BioChem. An interpolant for A ∧ B in the
theory of semilattices with 0 is I0 = substance ∧ cr ≤ inorganic. Thus, I = substance ∧
catalyzes(reaction) ≤ inorganic is an interpolant for A ∧ B. This is an explanation for the
inconsistency of A ∧ B, and may help to find the error more easily than the initial proof
of unsatisfiability. For this we can, for instance, analyze the (shorter) proofs of A |= I and
B ∧ I |=⊥ and note that the constraint reaction ≤ oxydation is used in the proof of A |= I.
                              INTERPOLATION IN LOCAL THEORY EXTENSIONS                                                   23




7.3. Verification. Consider the verification example from Section 2.2. We illustrate our
method for generating interpolants for a formula corresponding to a path of length 2 from
an initial state to an unsafe state:
     G = l < Lalarm ∧ l′ ≈ in(l, t′ − t) ∧ t′ ≈ k(t) ∧ l′ ≥ Lalarm ∧
         l′′ ≈ in(out(l′ , t′′1 − t′ ), t′′2 − t′ ) ∧ t′′1 ≈ g(t′ ) ∧ t′′2 ≈ h(t′ ) ∧ ¬l′′ < Loverflow .
Hierarchic reasoning. The extension T1 of linear arithmetic with the clauses K in Section 2
is local, so to prove G |=T1 ⊥ it is sufficient to consider ground instances K[G] in which all
extension terms already occur in G. After flattening and purifying K[G]∧G, we separate the
problem into a definition part (Extension) and a base part G0 ∧ K0 . By Theorem 4.7 [15],
the problem can be reduced to testing the satisfiability in the base theory of the conjunction
G0 ∧ K0 ∧ Con0 . As this conjunction is unsatisfiable with respect to T0 , G is unsatisfiable.
     Extension                                                 Base
 (Definitions)          G0                               K0 ∧ Con0
 l′ ≈ in(l, e1 )        l < Lalarm                K0 :   l < Lalarm ∧ 0 ≤ e1 ≤ ∆t → l′ < Loverflow
 c12 ≈ out(l′ , e12 )   l′ ≥ Lalarm                      c12 < Lalarm ∧ 0 ≤ e22 ≤ ∆t → l′′ < Loverflow
 l′′ ≈ in(c12 , e22 )   e1 ≈ t′ − t                      l′ < Loverflow ∧ e12 ≥ δt → c12 < Lalarm
 t′ ≈ k(t)              e12 ≈ t′′1 − t′                  0 ≤ δt ≤ t′′1 − t′ ≤ t′′2 − t′ ≤ ∆t
 t′′1 ≈ g(t′ )          e22 ≈ t′′2 − t′                  0 ≤ t′ − t ≤ ∆t
 t′′2 ≈ h(t′ )          ¬l′′ ≤ Loverflow          Con0 : l ≈ c12 ∧ e1 ≈ e22 → l′ ≈ l′′

Interpolation. Let A and B be given by:
       A = l < Lalarm ∧ e1 ≈ t′ − t ∧ l′ ≈ in(l, e1 ) ∧ t′ ≈ k(l)
       B = l′ ≥ Lalarm ∧ c12 ≈ out(l′ , e12 ) ∧ l′′ ≈ in(c12 , e22 ) ∧ e12 ≈ t′′1 − t′ ∧ e22 ≈ t′′2 − t′ ∧
             t′′1 ≈ g(t′ ) ∧ t′′2 ≈ h(t′ ) ∧ ¬l′′ < Loverflow .
The set of constants which occur in A is {l, t, e1 , l′ , t′ }. In B occur {l′ , t′ , c12 , l′′ , t′′1 , t′′2 , e12 , e22 }.
The shared constants are l′ and t′ . To generate an interpolant for A ∧ B, we partition the
clauses in A0 ∧ B0 ∧ K0 ∧ Con0 = A0 ∧ B0 ∧ K0A ∧ K0B ∧ Con0 , where:
 A0 = l<Lalarm ∧ e1 ≈ t′ − t
 B0 = l′ ≥ Lalarm ∧ e12 ≈ t′′1 − t′ ∧ e22 ≈ t′′2 − t′ ∧ ¬l′′ ≤ Loverflow
K0A = (l < Lalarm ∧ 0 ≤ e1 ≤ ∆t → l′ < Loverflow ) ∧ (0 ≤ t′ − t ≤ ∆t)
K0B = (c12 < Lalarm ∧ 0 ≤ e22 ≤ ∆t → l′′ < Loverflow ) ∧ (l′ < Loverflow ∧ e12 ≥ δt → c12 < Lalarm )
         ∧ (0 ≤ δt ≤ t′′1 − t′ ≤ t′′2 − t′ ≤ ∆t) .
The clause in Con0 is mixed. Since already the conjunction of the formulae in A0 ∧ B0 ∧
K0A ∧ K0B is unsatisfiable, Con0 is not needed to prove unsatisfiability. The conjunction of
the formulae in A0 ∧ B0 ∧ K0A ∧ K0B is equivalent to A′0 ∧ B0′ , where
       A′0 = l<Lalarm ∧ e1 ≈ t′ − t ∧ (0 ≤ t′ − t ≤ ∆t) ∧ l′ < Loverflow
       B0′ = l′ > Lalarm ∧ e12 ≈ t′′1 − t′ ∧ e22 ≈ t′′2 − t′ ∧ (0 ≤ δt ≤ t′′1 − t′ ≤ t′′2 − t′ ≤ ∆t)∧
                ¬l′′ < Loverflow ∧ ¬c12 < Lalarm ∧ ¬l′ < Loverflow .
The interpolant for A′0 ∧ B0′ is l′ < Loverflow , which is also an interpolant for A ∧ B.
24                               V. SOFRONIE-STOKKERMANS




The abstraction defined in Section 2.2 can then be refined by introducing another predicate
L′ < Loverflow .

                                      8. Conclusions
We presented a method for obtaining simple interpolants in theory extensions. We identified
situations in which it is possible to do this in a hierarchical manner, by using a prover and a
procedure for generating interpolants in the base theory as “black-boxes”. This allows us to
use the properties of T0 (e.g. the form of interpolants) to control the form of interpolants in
the extension T1 . We discussed applications of interpolation in verification and knowledge
representation.
     The method we presented can be applied to a class of theories which is more general than
that considered in McMillan [8] (extension of linear rational arithmetic with uninterpreted
function symbols). Our method is orthogonal to the method for generating interpolants for
combinations of theories over disjoint signatures from Nelson-Oppen-style unsatisfiability
proofs proposed by Yorsh and Musuvathi in [19], as it allows us to consider combinations
of theories over non-disjoint signatures.
     The hierarchical interpolation method presented here was in particular used for effi-
ciently computing interpolants in the special case of the extension of linear arithmetic with
free function symbols in [11]; the algorithm we used in that paper (on which an implemen-
tation is based) differs a bit from the one presented here in being tuned to the constrained
based approach used in [11]. The implementation was integrated into the predicate dis-
covery procedure of the software verification tools Blast [4] and ARMC [10]. First tests
suggest that the performance of our method is of the same order of magnitude as the meth-
ods which construct interpolants from proofs, and considerably faster on many examples. In
addition, our method can handle systems which pose problems to other interpolation-based
provers: we can handle problems containing both strict and nonstrict inequalities, and it
allows us to verify examples that require predicates over up to four variables. Details about
the implementation and benchmarks for the special case of linear arithmetic + free function
symbols are described in [11].
     Although the method we presented here is based on a hierarchical reduction of proof
tasks in a local extension of a given theory T0 to proof tasks in T0 , the results presented
in Section 5 (in particular the separation technique described in Proposition 5.7) and in
Section 6 also hold for non-purified formulae (i.e. they also hold if we do not perform the
step of introducing new constant names cf (d) for the ground terms f (d) which occur in the
problem or during the separation process). Depending on the properties of T0 , techniques
for reasoning and interpolant generation in the extension of T0 with free function symbols
e.g. within state of the art SMT solvers can then be used. We can, therefore, use the results
in Sections 5 and 6 to extend in a natural way existing methods for interpolant computation
which take advantage of state of the art SMT technology (cf. e.g. [3]) to the more complex
types of theory extensions with sets of axioms of type (5.1) we considered here.
     An immediate application of our method is to verification by abstraction-refinement;
there are other potential applications (e.g. goal-directed overapproximation for achieving
faster termination, or automatic invariant generation) which we would like to study. We
would also like to analyze in more detail the applications to reasoning in complex knowledge
bases.
                          INTERPOLATION IN LOCAL THEORY EXTENSIONS                                      25




Acknowledgements. I thank Andrey Rybalchenko for interesting discussions. I thank
the referees for helpful comments.
This work was partly supported by the German Research Council (DFG) as part of the
Transregional Collaborative Research Center “Automatic Verification and Analysis of Com-
plex Systems” (SFB/TR 14 AVACS). See www.avacs.org for more information.

                                             References
 [1] F. Baader and S. Ghilardi. Connecting many-sorted theories. In R. Nieuwenhuis, editor, 20th Interna-
     tional Conference on Automated Deduction (CADE-20), LNAI 3632, pages 278–294. Springer, 2005.
 [2] P.D. Bacsich. Amalgamation properties and interpolation theorem for equational theories. Algebra Uni-
     versalis, 5:45–55, 1975.
 [3] A. Cimatti, A. Griggio, and R. Sebastiani. Efficient Interpolant generation in satisfiability modulo
     theories. In TACAS’2008: Tools and Algorithms for the Construction and Analysis of Systems, LNCS
     4963, pages 397–412, Springer, 2008.
 [4] T. A. Henzinger, R. Jhala, R. Majumdar, and K. L. McMillan. Abstractions from proofs. In POPL’2004:
     Principles of Programming Languages, pages 232–244. ACM Press, 2004.
 [5] B Jónsson. Extensions of relational structures. In J.W. Addison, L. Henkin, and A. Tarski, editors,
     The Theory of Models, Proc. of the 1963 Symposium at Berkeley, pages 146–157, Amsterdam, 1965.
     North-Holland.
 [6] D. Kapur, R. Majumdar, C. Zarba. Interpolation for data structures. In Proc. 14th ACM SIGSOFT
     International Symposium on Foundations of Software Engineering, pages 105–116, ACM 2006.
 [7] K.L. McMillan. Interpolation and SAT-based model checking. In CAV’2003: Computer Aided Verifica-
     tion, LNCS 2725, pages 1–13. Springer, 2003.
 [8] K.L. McMillan. An interpolating theorem prover. In TACAS’2004: Tools and Algorithms for the Con-
     struction and Analysis of Systems, LNCS 2988, pages 16–30. Springer, 2004.
 [9] K.L. McMillan. Applications of Craig interpolants in model checking. In TACAS’2005: Tools and Al-
     gorithms for the Construction and Analysis of Systems, LNCS 3440, pages 1–12. Springer, 2005.
[10] A. Podelski and A. Rybalchenko. ARMC: the logical choice for software model checking with abstraction
     refinement. In PADL’2007: Practical Aspects of Declarative Languages, LNCS 4354, pages 245–259,
     Springer, 2007.
[11] A. Rybalchenko and V. Sofronie-Stokkermans. Constraints for interpolation. Constraint solving for
     interpolation. In B. Cook and A. Podelski, editors, Proceedings of the 8th International Conference on
     Verification, Model Checking and Abstract Interpretation (VMCAI 2007), LNCS 4349, pages 346–362,
     Springer Verlag, 2007.
[12] V. Sofronie-Stokkermans. On the universal theory of varieties of distributive lattices with operators:
     Some decidability and complexity results. In H. Ganzinger, editor, Proceedings of CADE-16, LNAI
     1632, pages 157–171, Springer Verlag, 1999.
[13] V. Sofronie-Stokkermans. Resolution-based decision procedures for the universal theory of some classes
     of distributive lattices with operators. Journal of Symbolic Computation, 36(6):891–924, 2003.
[14] V. Sofronie-Stokkermans. Automated theorem proving by resolution in non-classical logics. In 4th Int.
     Conf. Journees de l’Informatique Messine: Knowledge Discovery and Discrete Mathematics (JIM-03),
     pages 151–167, 2003.
[15] V. Sofronie-Stokkermans. Hierarchic reasoning in local theory extensions. In R. Nieuwenhuis, edi-
     tor, 20th International Conference on Automated Deduction (CADE-20), LNAI 3632, pages 219–234.
     Springer, 2005.
[16] V. Sofronie-Stokkermans. Hierarchical and Modular Reasoning in Complex Theories: The Case of
     Local Theory Extensions. In B. Konev and F. Wolter, editors, Frontiers of Combining Systems, 6th
     International Symposium, (FroCoS 2007), LNCS 4720, pages 47–71, Springer, 2007.
[17] V. Sofronie-Stokkermans and C. Ihlemann. Automated reasoning in some local extensions of ordered
     structures. Proceedings of ISMVL 2007, IEEE Computer Society, 2007.
[18] A. Wroński. On a form of equational interpolation property. In Foundations of logic and linguistics
     (Salzburg, 1983), pages 23–29, New York, 1985. Plenum.
26                                       V. SOFRONIE-STOKKERMANS




[19] G. Yorsh and M. Musuvathi. A combination method for generating interpolants. In R. Nieuwenhuis,
     editor, 20th International Conference on Automated Deduction (CADE-20), LNAI 3632, pages 353–368.
     Springer, 2005.


                        Appendix A. Amalgamation and interpolation
There exist results which relate ground interpolation to amalgamation or the injection
transfer property [5, 2, 18] and thus allow us to recognize many theories with ground
interpolation.
     If Π = (Σ, Pred) is a signature and A, B are Π-structures, we say that:
• a map h : A ֒→ B is a homomorphism if it preserves the truth of positive literals, i.e.
  has the property that if fA (a1 , . . . , an ) = a then fB (h(a1 ), . . . , h(an )) = h(a), and if
  PA (a1 , . . . , an ) is true then PB (h(a1 ), . . . , h(an )) is true.
• a map i : A ֒→ B is an embedding if it preserves the truth of both positive and negative
  literals, i.e. PA (a1 , . . . , an ) is true (in A) if and only if PB (i(a1 ), . . . , i(an )) is true (in
  B) for any predicate symbol, including equality. Thus, an embedding is an injective
  homomorphism which also preserves the truth of negative literals.
Definition A.1. Let Π = (Σ, Pred) be a signature, and let M be a class of Π-structures.
(1) We say that M has the amalgamation property (AP) if for any A, B1 , B2 ∈ M and
    any embeddings i1 : A ֒→ B1 and i2 : A ֒→ B2 there exists a structure C ∈ M and
    embeddings j1 : B1 ֒→ C and j2 : B2 ֒→ C such that j1 ◦ i1 = j2 ◦ i2 .
(2) M has the injection transfer property (ITP) if for any A, B1 , B2 ∈ M, any embedding
    i1 : A ֒→ B1 and any homomorphism f2 : A → B2 there exists a structure C ∈ M, a
    homomorphism f1 : B1 → C and an embedding j2 : B2 ֒→ C such that f1 ◦ i1 = j2 ◦ f2 .
Definition A.2. An equational theory T (in signature Π = (Σ, Pred) where Pred = {≈})
has the equational interpolation property if whenever
                         ^               ^
                             Ai (a, c) ∧   Bj (c, b) ∧ ¬B(c, b) |=T ⊥,
                                 i               j

where Ai , Bj and B are ground atoms, there exists a conjunction I(c) of ground atoms
                                                      V           V
containing only the constants c occurring both in i Ai (a, c) and j Bj (c, b) ∧ ¬B(c, b),
          V                              V
such that i Ai (a, c) |=T I(c) and I(c) ∧ j Bj (c, b) |=T B(c, b)
Theorem A.3 ([5, 2, 18]). Let T be a universal theory. Then:
(1) T has ground interpolation if and only if Mod(T ) has (AP) [2]. In addition, we can
    guarantee that if φ is positive then the interpolant of φ ∧ ψ is positive if and only if
    Mod(T ) has the injection transfer property [2].
(2) If T is an equational theory, then T has the equational interpolation property if and
    only if Mod(T ) has the injection transfer property [18].
Theorem A.3 can be used to prove that many equational theories have ground interpolation:
Theorem A.4. The following theories allow ground interpolation7 :
(1) The theory of pure equality (without function symbols).
     7In fact, the theories (1) and (4) allow equational interpolation. Similar results were also established for
(2) in [11].
                          INTERPOLATION IN LOCAL THEORY EXTENSIONS                                    27




(2) Linear rational and real arithmetic.
(3) The theory of posets.
(4) The theories of (a) Boolean algebras, (b) semilattices, (c) distributive lattices.
Proof. (1), (2), (3) are well-known (for (2) we refer for instance to [8] or [19]). For proving
(4) we use the fact that if a universal theory has a positive algebraic completion then it has
the injection transfer property [1]. All theories in (4) are equational theories; by results in
[18], for equational theories the injection transfer property is equivalent to the equational
interpolation property. With these remarks, (4)(a) follows from the fact that any Gaussian
theory is its own positive algebraic completion [1], and (4)(b),(c) from the fact that the
theory of semilattices and that of distributive lattices have a positive algebraic completion
[1].
Similarly it can be proved that the equational classes of (abelian) groups and lattices have
ground interpolation.

                            Appendix B. Proof of Theorem 4.6
Theorem 4.6 We consider the following base theories T0 :
(1) P (posets),
(2) T O (totally-ordered sets),
(3) SLat (semilattices),
(4) DLat (distributive lattices),
(5) Bool (Boolean algebras).
(6) the theory R of reals resp. LI(R) (linear arithmetic over R), or the theory Q of rationals
    resp. LI(Q) (linear arithmetic over Q), or (a subtheory of ) the theory of integers (e.g.
    Presburger arithmetic).
The following theory extensions are local:
(a) Extensions of any theory T0 for which ≤ is reflexive with functions satisfying bounded-
    ness (Boundt (f )) or guarded boundedness (GBoundt (f )) conditions
       (Boundt (f ))          ∀x1 , . . . , xn (f (x1 , . . . , xn ) ≤ t(x1 , . . . , xn ))
                  t
       (GBound (f )) ∀x1 , . . . , xn (φ(x1 , . . . , xn ) → f (x1 , . . . , xn ) ≤ t(x1 , . . . , xn )),
    where t(x1 , . . . , xn ) is a term in the base signature Π0 and φ(x1 , . . . , xn ) a conjunction
    of literals in the signature Π0 , whose variables are in {x1 , . . . , xn }.
(b) Extensions of any theory T0 in (1)–(6) with Mon(f ) ∧ Boundt (f ), if t(x1 , . . . , xn ) is a
    term in the base signature Π0 in the variables x1 , . . . , xn such that for every model of
    T0 the associated function is monotone in the variables x1 , . . . , xn .
(c) Extensions of any theory in (1)–(6) with functions satisfying Leq(f, g) ∧ Mon(f ).
       (Leq(f, g)) ∀x1 , . . . , xn ( ni=1 xi ≤ yi → f (x1 , . . . , xn ) ≤ g(y1 , . . . , yn ))
                                           V

(d) Extensions of any totally-ordered theory above (i.e. (2) and (6)) with functions satisfying
    SGc(f, g1 , . . . , gn ) ∧ Mon(f, g1 , . . . , gn ).
       (SGc(f, g1 , . . . , gn )) ∀x1 , . . . , xn , x( ni=1 xi ≤ gi (x) → f (x1 , . . . , xn ) ≤ x)
                                                           V

(e) Extensions of any theory in (1)–(3) with functions satisfying SGc(f, g1 ) ∧ Mon(f, g1 ).
All the extensions above satisfy condition (Locf ).
28                                       V. SOFRONIE-STOKKERMANS




Proof. In what follows we will denote by Π0 the signature of the base theory T0 , and with
Σ1 the extension functions, namely f for cases (a) and (b), f, g for case (c), f, g1 , . . . , gn for
case (d) and f, g1 for case (e).
(a) Let (P, fP ) be a partial Π-structure which weakly satisfies Boundt (f ), such that P ∈
Mod(T0 ) and fP : P n → P is partial. Let A = (P, fA ) be a total Π-structure with the same
support as P , where:
                                       
                                         fP (x1 , . . . , xn ) if fP (x1 , . . . , xn ) defined
               fA (x1 , . . . , xn ) =
                                         t(x1 , . . . , xn )   otherwise.
Then A satisfies Boundt (f ). Let i : (P, fP ) → (A, fA ) be the identity. Obviously, i is a
Π0 -isomorphism; and if fP (x1 , . . . , xn ) is defined then i(fP (x1 , . . . , xn )) = fP (x1 , . . . , xn ) =
fA (x1 , . . . , xn ). Similar arguments also apply to GBoundt (f ).
(b) Let (P, fP ) be a partial Π-structure which weakly satisfies Boundt (f ) ∧ Mon, such that
P ∈ Mod(T0 ) and fP : P n → P is partial. In cases (1)–(3) let A = (OI(P ), f ), where
OI(P ) is the family of all order ideals of P , and
              fA (U1 , . . . , Un ) = ↓{fP (u1 , . . . , ui ) | ui ∈ Ui , fP (u1 , . . . , un ) defined}.
fA is clearly monotone. Let z ∈ fA (U1 , . . . , Un ). Then z ≤ fP (u1 , . . . , un ) for some ui ∈ Ui
with fP (u1 , . . . , un ) defined. As P |=w Boundt (f ), fP (u1 , . . . , un ) ≤ t(u1 , . . . , un ). Therefore
z ∈ t(U1 , . . . , Un ). The map i : (P, fP ) → (A, fA ) defined by i(p) =↓ p is a weak embedding.
     Since DLat and Bool are locally finite, results in [15] show that in (4) and (5) it is
sufficient to assume that P is finite. Let A = (P, fA ), where
                                   _
            fA (x1 , . . . , xn ) = {fP (u1 , . . . , un ) | ui ≤ xi , fP (u1 , . . . , un ) defined}.
fA is clearly monotone. We prove that it also satisfies the boundedness condition, i.e.
that  for all x1 , . . . , xn , fA (x1 , . . . xn ) ≤ t(x1 , . . . , xn ). By definition, fA (x1 , . . . , xn ) =
  {fP (u1 , . . . , un ) | ui ≤ xi , fP (u1 , . . . , un ) defined}. As P |=w Boundt (f ) and t is mono-
W
tone, we know that fP (u1 , . . . , un ) ≤ t(u1 , . . . , un ) ≤ t(x1 , . . . , xn ) for all ui ≤ xi with
fP (u1 , . . . , un ) defined. Therefore,
                           _
   fA (x1 , . . . , xn ) = {fP (u1 , . . . , un ) | ui ≤ xi , fP (u1 , . . . , un ) defined} ≤ t(x1 , . . . , xn ).
That the identity i is a weak embedding can be proved as before.
(c) The proof is very similar to the proof of (b). We first discuss the case (1)–(3). Let
(P, fP , gP ) be a weak partial model of T1 . Let A = (OI(P ), fA , gA ), where fA is defined as
in (b). We define g(U1 , . . . , Un ) by
                               
                                 ↓ gP (x1 , . . . , xn ) if Ui =↓ xi and gP (x1 , . . . , xn ) defined
       gA (U1 , . . . , Un ) =
                                 fA (U1 , . . . , Un )   otherwise.
Assume that U1 ⊆ V1 , . . . , Un ⊆ Vn , and let z ∈ fA (U1 , . . . , Un ). Then z ≤ fP (u1 , . . . , un ) for
some ui ∈ Ui ⊆ Vi with fP (u1 , . . . , un ) defined. If Vi =↓ xi and gP (x1 , . . . , xn ) defined, then
ui ≤ xi so, as P |=w Leq(f, g), we know that fP (u1 , . . . , un ) ≤ gP (x1 , . . . , xn ). It therefore
follows that in this case z ∈ ↓gP (x1 , . . . , xn ) = gA (V1 , . . . , Vn ). Otherwise, gA (V1 , . . . , Vn ) =
fA (V1 , . . . , Vn ), hence fA (U1 , . . . , Un ) ⊆ gA (V1 , . . . , Vn ).
                              INTERPOLATION IN LOCAL THEORY EXTENSIONS                                                 29




     For the cases (4) and (5) we again use the criterion in [15] and Theorem 4.5. Let
(P, fP , gP ) be a weak partial model of T1 . Let a0 ∈ P be such that a0 ≥ fP (p1 , . . . , pn )
whenever fP (p1 , . . . , pn ) is defined. We define A = (P, fA , gA ) as follows:
                                     (
                                       ↓ gP (x1 , . . . , xn ) if gP (x1 , . . . , xn ) defined
             gA (x1 , . . . , xn ) =
                                       a0                      otherwise
                                     _
             fA (x1 , . . . , xn ) = {fP (u1 , . . . , un ) | ui ≤ xi , fP (u1 , . . . , un ) defined} .
 f is obviously monotone. In order to prove that the second condition holds, we analyze
 two cases. Assume first that gP (y1 , . . . , yn ) is undefined. Then gA (y1 , . . . , yn ) = a0 ≥
fWP (u1 , . . . , un ) for all ui ≤ xi with fP (u1 , . . . , un ) defined, thus, gA (y1 , . . . , yn ) = a0 ≥
   {fP (u1 , . . . , un ) | ui ≤ xi , fP (u1 , . . . , un ) defined } = fA (x1 , . . . , xn ). If gP (y1 , . . . , yn ) is
 defined, then for all ui ≤ xi with fP (u1 , . . . , un ) we also have ui ≤ yi , so fP (u1 , . . . , un ) ≤
 gP (y1 , . . . , yn ) = gA (y1 , . . . , yn ). Again, it follows that gA (y1 , . . . , yn ) ≤ fA (x1 , . . . , xn ).
(d) Let T0 be the theory of totally ordered sets. Assume that (P, fP , (gPi )) is a totally ordered
weak partial model of SGc(f, g1 , . . . , gn ) ∧ Mon(f, g1 , . . . , gn ). Let A = (OI(X), fA , (gA        i )),

where fA and gA       i are extensions of f , g i defined as in the proof of (b). f , g 1 , . . . , g n are
                                                P P                                    A A               A
obviously monotone. We prove that the condition SGc(f, g1 , . . . , gn ) holds in A. Assume
that Ui ⊆ gA       i (V ) for i = 1, . . . , n, and let x ∈ f (U , . . . , U ). Then there exist u ∈
                                                             A   1           n                              i
Ui = gA  i (V ) such that f (u , . . . , u ) is defined and x ≤ f (u , . . . , u ). As u ∈ g i (V ),
                i                  1          n                             1       n        i          A
there exist vi ∈ V such that gPi (vi ) is defined and ui ≤ gPi (vi ). Let v = max(v1 , . . . , vn ).
Then ui ≤ gPi (v). Hence fP (u1 , . . . , un ) ≤ v ∈ V . Therefore, x ≤ fP (u1 , . . . , un ) ∈ V so
x ∈ V . Let i : P → A defined by i(p) =↓ p. To show that it is a weak embedding we only
have to show that if gP (x1 , . . . , xn ) is defined then i(gP (x1 , . . . , xn )) = ↓gP (x1 , . . . , xn ) =
gA (↓x1 , . . . , ↓xn ). This is true by the definition of gA .
(e) Assume that T0 is the theory of semilattices. The construction in (d) can be applied to
this case without problems. The proof is similar to that of (d) with the difference that if
n = 1 we only have one element v1 so we do not need to compute a maximum (which for
n ≥ 2 may not exist if the order is not total).
     The proof of the fact that the remaining theories satisfy (Locf ) is based on the criterion
of finite locality given in Theorem 4.5. The constructions and the proofs are similar to
those in the proof of (b) resp. (c) for the cases (4) and (5). Due toWthe fact that we
assumed that the definition domain of the extension functions is finite {fP (u1 , . . . , un ) |
ui ≤ xi , fP (u1 , . . . , un ) defined} is a finite join, and thus exists (if f is nowhere defined it is
sufficient to define it as being everywhere equal to t in case (b) or to gA in case (c)). The
fact that the definition domains are finite also ensures that in the proof of (c) an element
a0 (chosen in the definition of gA ) with the desired properties always exists.


                                 Appendix C. Proof of Theorem 5.4
Theorem 5.4. The following theories have ground interpolation and are convex and P -
interpolating with respect to the indicated set P of predicate symbols:
(1) The theory of EQ of pure equality without function symbols (for P = {≈}).
(2) The theory PoSet of posets (for P = {≈, ≤}).
30                                 V. SOFRONIE-STOKKERMANS




(3) Linear rational arithmetic LI(Q) and linear real arithmetic LI(R) (convex with respect
    to P = {≈}, strongly P -interpolating for P = {≤}).
(4) The theories Bool of Boolean algebras, SLat of semilattices and DLat of distributive
    lattices (strongly P -interpolating for P = {≈, ≤}).

Proof. Note first that if a partially-ordered theory is interpolating for ≤ it is also for ≈.
Assume that A ∧ B |=T a ≈ b. Then A ∧ B |=T a ≤ b and A ∧ B |=T b ≤ a, hence there exist
terms t1 , t2 containing only common constants of A and B such that A∧B |= a ≤ t1 ∧t1 ≤ b
and A ∧ B |= b ≤ t2 ∧ t2 ≤ a. It follows that A ∧ B |= t1 ≈ t2 , A ∧ B |= a ≈ t1 ∧ t1 ≈ b.
(1) and (2): convexity is obvious; the property of being P -interpolating can be proved by
induction on the structure of proofs. (3) is known (cf. e.g. [19]). A method for computing
interpolating terms for LI(R) and LI(Q) is presented in [11].
(4) This is a constructive proof based on ideas from [12, 13]. The results presented there
show, as an easy particular case, that one can reduce the problem of checking the satisfia-
bility of a conjunction Γ of unit clauses with respect to one of the theories above to checking
the satisfiability of a conjunction RenΓ ∧ PΓ ∧ NΓ obtained by introducing a propositional
variable Pe for each subterm e occurring in Γ, a set of renaming rules of the form
                 Pe1 op e2 ↔ Pe1 op Pe2           op binary Boolean operation
                      P¬e ↔ ¬Pe                    in the case of Bool,
and translations of the positive resp. negative part of Γ:
                                    Ps ↔ Ps′          s ≈ s′ ∈ Γ
                                  ¬(Ps ↔ Ps′ )        s 6≈ s′ ∈ Γ.

(a) The convexity of the theory of Boolean algebras with respect to ≈ follows from the fact
that this is an equational class; convexity with respect to ≤ follows from the fact that x ≤ y
if and only if x ∧ y ≈ x. We prove that the theory of Boolean algebras is ≤-interpolating,
i.e. that if A and B are two conjunctions of literals and A ∧ B |=Bool a ≤ b, where a is a
constant occurring in A and not in B and b a constant occurring in B and not in A, then
there exists a term containing only common constants in A and B such that A |=Bool a ≤ t
and B |=Bool t ≤ b. We can assume without loss of generality that A and B consist
only of atoms (otherwise one moves the negative literals to the right and uses convexity).
A ∧ B |=Bool a ≤ b if and only if the following conjunction of literals in propositional logic
is unsatisfiable:

     (Ren(∧))      Pe1 ∧e2   ↔    Pe1 ∧ Pe2                Pg1 ∧g2    ↔    Pg1 ∧ Pg2
     (Ren(∨))      Pe1 ∨e2   ↔    Pe1 ∨ Pe2                Pg1 ∨g2    ↔    Pg1 ∨ Pg2
     (Ren(¬))        P¬e     ↔    ¬Pe                        P¬g      ↔    ¬Pg
     (P)              Pe1    ↔    Pe2 e1 ≈ e2 ∈ A             Pg1     ↔    Pg2 g1 ≈ g2 ∈ B
     (N)                     Pa                                      ¬Pb

                   for all e, e1 , e2 subterms in A        for all g, g1 , g2 subterms in B
We obtain an unsatisfiable set of clauses (NA ∧ Pa ) ∧ (NB ∧ ¬Pb ) |=⊥. Propositional logic
allows interpolation, so there exists an interpolant I = f (Pe1 , . . . , Pen ), which is a Boolean
                        INTERPOLATION IN LOCAL THEORY EXTENSIONS                                                             31




combination (say in CNF) of the common propositional variables occurring in NA and NB
such that
                      (NA ∧ Pa ) |= I and (NB ∧ ¬Pb ) ∧ I |=⊥ .
But then A |=Bool a ≤ f (e1 , . . . , en ) and B |=Bool f (e1 , . . . , en ) ≤ b.
(4)(b) The proof is similar to that of (4)(a) with the difference that in the renaming rules
in the structure-preserving translation to clause form only the conjunction rules apply,
hence NA and NB are sets of non-negative Horn clauses. We can saturate NA ∪ Pa under
resolution with selection on the negative literals in linear time. The saturated set NA∗ of
clauses contains all unit clauses Pe where e is subterm of A with A |=SLat a ≤ e. Only unit
positive clauses Pe where e occurs in both A and B can enter into resolution inferences with
clauses in NB ∪ ¬Pb and lead to a contradiction. Thus we proved that
             ^
                {Pe | A |=SLat a ≤ e, e common subterm} ∧ NB ∧ ¬Pb |=⊥ .
This is equivalent to B |=SLat t ≤ b, where
                    ^
                t = {e | A |=SLat a ≤ e, e common subterm of A and B} .
Obviously, A |=SLat a ≤ t.
(4)(c) The case of distributive lattices can be treated similarly. Due to the fact that in this
case the renaming rules for ∨ and ∧ are taken into account, the sets NA and NB are not
Horn. We adopt the same negative selection strategy. When saturating NA ∪ Pa a finite
set of positive clauses is generated, namely of the form Pe1 ∨ · · · ∨ Pen where A |=DL a ≤
(e1 ∨ · · · ∨ en ). We consider a total ordering on the propositional variables where Pe is larger
than Pg if e occurs in A and not in B and g occurs in both A and in B. Then the only
inferences which can lead to a contradiction with NB ∪ ¬Pb are those between the clauses
in NA∗ which only contain common propositional variables. Thus we proved that
               ^ _                     _
                  { Pei | A |=DL a ≤      ei , ei common terms} ∧ NB ∧ ¬Pb |=⊥ .
                                                     V W                W
This is equivalent to B |=DL t ≤ b, where t = { ei | A |=DL a ≤ ei , where all ei are
common subterms of A and B}. Obviously, A |=DL a ≤ t.




                                          This work is licensed under the Creative Commons Attribution-NoDerivs License. To view
                                          a copy of this license, visit http:// reative ommons.org/li enses/by-nd/2.0/ or send a
                                          letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
