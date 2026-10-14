                                                           BOUNDED REWRITING INDUCTION FOR LCSTRSs

                                                                              KASPER HAGENS     AND CYNTHIA KOP

                                              Radboud University, Nijmegen
                                              e-mail address: kasper.hagens@ru.nl, c.kop@cs.ru.nl
arXiv:2601.02803v1 [cs.LO] 6 Jan 2026




                                                    Abstract. Rewriting Induction (RI) is a method to prove inductive theorems, originating
                                                    from equational reasoning. By using Logically Constrained Simply-typed Term Rewriting
                                                    Systems (LCSTRSs) as an intermediate language, rewriting induction becomes a tool for
                                                    program verification, with inductive theorems taking the role of equivalence predicates.
                                                       Soundness of RI depends on well-founded induction, and one of the core obstacles
                                                    for obtaining a practically useful proof system is to find suitable well-founded orderings
                                                    automatically. Using naive approaches, all induction hypotheses must be oriented within
                                                    the well-founded ordering, which leads to very strong termination requirements. This, in
                                                    turn, severely limits the proof capacity of RI. Here, we introduce Bounded RI : an adaption
                                                    of RI for LCSTRSs where such termination requirements are minimized.
                                                       Traditionally, RI can be used not only to prove equivalence, but also to establish ground
                                                    confluence. Moreover, for ground confluent TRSs, RI can be extended to a system for
                                                    disproving inductive theorems. We will show that this is also possible with Bounded RI.




                                                                                      1. Introduction
                                        Rewriting Induction (RI) is a proof system for showing equations to be inductive theorems. It
                                        was introduced by Reddy [Red90] as a method to validate inductive proof procedures based on
                                        Knuth-Bendix completion. Classically, RI is used in equational reasoning to prove properties
                                        of inductively defined mathematical structures like natural numbers or lists. For example, one
                                        could use RI to prove an equation add(x, y) ≈ add(y, x), expressing commutativity of addition
                                        on the natural numbers. RI has been extended to constrained rewriting [FK12, FKN17,
                                        NNK+ 10], and recently to higher-order constrained rewriting [HK24]. These formalisms
                                        closely relate to real programming and therefore have a natural place in the larger toolbox for
                                        program verification. Programs are represented by term rewriting systems, and equivalence
                                        of two functions within a program is modeled by an equation being an inductive theorem.

                                        Why constrained rewriting? Using RI for program equivalence somewhat differs from the
                                        standard setting in equational reasoning where, for example, the Peano axioms are used to
                                        prove statements about the natural numbers. In our case, we are not so much interested in
                                        proving properties about numbers themselves, but about programs that operate on them. Of
                                        course, we can define functions like add, mul and greater, express the Peano axioms as rewrite
                                        rules and use this to define programs on natural numbers. However, doing so studying
                                        program equivalence becomes a cumbersome experience that requires both reasoning about
                                        the arithmetic and the program definition itself. Moreover, in practice, we typically want

                                        Preprint submitted to                                                                          © K. Hagens and C. Kop
                                        Logical Methods in Computer Science                                                            ⃝
                                                                                                                                       CC Creative Commons
2                                   K. HAGENS AND C. KOP




to reason about integers or even bit vectors rather than natural numbers, which requires
correspondingly harder arithmetic reasoning. Intermingling these two different kinds of
reasoning makes it hard to scale analysis. Ideally, we would want arithmetic to be given “for
free”, as it is in real life programming. With standard term rewriting this is not possible.
    Constrained term rewriting provides a solution here, as it natively supports primitive
data structures, such as integers, bit vectors and floating point numbers. This makes it
possible to distinguish between the program definition (represented by rewrite rules), and
underlying data structures with their operators (represented by distinguished terms with
pre-determined semantical interpretations). This allows us to shift some of the proof-burden
from the rewriting side to the semantical side, where dedicated SMT solvers can be used.
    In constrained rewriting, rewrite rules have a shape s → t [φ] where the boolean constraint
φ acts as a guard, in order to manage control flow over primitive data structures. Here,
we will consider Logically Constrained Simply-typed Term Rewriting Systems (LCSTRSs),
which considers applicative higher-order rewriting (without λ abstractions) and first-order
constraints [GK24]. In particular, we will build on our earlier work [HK24] where we defined
RI for LCSTRSs (but do not assume familiarity with this work or other definitions of RI).

Goals. Our goals are threefold:
▷ Redefine RI for LCSTRSs in such a way that we minimize the termination requirements.
  Our primary goal. Induction proofs in RI require induction hypotheses to be oriented in a
  well-founded ordering. This has the potential to give very strong termination requirements –
  which, as we will see, is not necessary. By adapting the definition of RI, we can significantly
  reduce these termination requirements and thereby make (automatic) proof search easier.
▷ Using RI as a method for proving ground confluence. For first-order unconstrained rewriting
  it has been shown that RI can be combined with critical pairs to obtain a method for
  proving ground confluence [AT16]. Here, we extend this result to LCSTRSs.
▷ Disproving equations. For first-order, ground confluent LCTRSs, RI can also be used
  to prove that equations are not inductive theorems [FKN17], but the higher-order proof
  system in [HK24] does not yet support this. Here, we extend this result to LCSTRSs.

Termination requirements. The name Rewriting Induction refers to the principle that
for a terminating rewrite system R, the reduction relation →+   R defines a well-founded order
on the set of all terms, and therefore can be used for proofs by well-founded induction. In
many cases, however, we will need a well-founded order ≻ which is strictly larger than →+    R.
     In particular, the role of induction hypotheses in RI is taken by equations, which, when
applied, must be oriented w.r.t. ≻. That is, we can only use an induction hypothesis s ≈ t if
s ≻ t or t ≻ s holds. Consequently, termination of R itself is not enough, since equations are
not usually orientable by →+                                                 +
                               R . Instead, we for instance might let ≻ = →R∪{s→t} , or in the
case of multiple induction hypotheses, orient them as rewrite rules, collect them into a set H,
and use ≻ = →+   R∪H . However, doing so leaves us with an obligation to show termination of
R ∪ H. Even if R is known to be terminating, it may not be easy or even possible to prove
the same for R ∪ H (think for instance of an induction hypothesis add(x, y) ≈ add(y, x),
which is not orientable in either direction). In such a situation a RI proof might get stuck.
     As already observed by Reddy [Red90], we do not necessarily need every induction
hypothesis to be oriented, so long as we guarantee that an induction rule s → t is only applied
to terms ≻-smaller than s. For this, it is not required to choose the well-founded ordering ≻
= →+  R∪H . Reddy proposed to use modulo rewriting, to build a well-founded ≻ which may not
                       BOUNDED REWRITING INDUCTION FOR LCSTRSs                                3




need to contain all induction rules. This approach was investigated by Aoto, who introduced
several extensions of RI for first-order unconstrained rewriting [Aot06, Aot08a, Aot08b].
Here, we will follow a strategy along the same idea: by redefining RI we construct a
well-founded relation ≻ during the RI process, aiming to keep it as small as possible.

Paper setup and contributions. In section 2 we recap LCSTRSs, equations and inductive
theorems. The following sections present our contributions:
▷ In section 3 we introduce Bounded RI for LCSTRSs. This system builds on the one
  introduced in [HK24] – and is thus designed for higher-order, constrained systems – but
  provides a more semantic approach and strictly contains it. Contributions include:
  – We introduce the notion of bounding pair (≻, ⪰), providing the fundamental ingredient
     by which we express the ordering requirements for induction proofs.
  – We replace equations by equation contexts, containing the extra information of two
     bounding terms which define an upper bound for applying an induction hypothesis. More
     specifically, the bounding terms provide us with a way to keep track of terms to be in used
     in the ordering requirements (along the equation we are proving) – instead of orienting
     the induction hypothesis themselves – yielding milder termination requirements.
  – In contrast to [HK24], we also include derivation rules to deduce non-equivalence
     (subsection 3.3) for ground confluent LCSTRSs. This is thus far only achieved for
     first-order definitions of RI [FKN17].
▷ In section 4, we prove soundness and completeness of Bounded RI. Apart from its necessity
  for the results of section 3 to be meaningful, there are two additional contributions:
  – We show that Bounded RI can be used to prove that equations are bounded ground
     convertible, which is strictly stronger than the property of ground convertibility that
     was used in [HK24], and which explicitly relates to the bounding pair (≻, ⪰).
  – We structure our soundness proof in a very modular way, by focusing on two properties
     that all but one of our deduction rules satisfy. This makes it possible to easily add new
     derivation rules to the existing system without having to redo the full proof.
▷ In section 5 we show that Bounded RI can be used to prove ground confluence of an LC-
  STRS. This is a known result, but only for first-order systems without constraints [AT16].
  – We recap the definition of first-order critical pairs for LCTRSs from [SM23], extend it
     to LCSTRSs and prove the Critical Peak Lemma. This is a first critical peak / pair
     definition for higher-order constrained systems.
  – We introduce the Ground Critical Peak Theorem, and show how this allows us to use
     RI for proving ground confluence. This follows the idea of [AT16], but makes important
     adaptations to work well with the new RI method.
▷ In section 6 we discuss two strategies to construct a suitable well-founded ordering. In
  particular, we can define the ordering as a reduction relation →+    R∪Q and briefly discuss
  strategies to choose the set Q. We also show that we can use a version of the dependency
  pair framework directly to obtain more liberal requirements.
▷ In section 7 we illustrate how the two soundness properties – Preserving Bounds (Defini-
  tion 4.1) and Base Soundness Property (Definition 4.9) – can be exploited to obtain new
  deduction rules, by extending Bounded RI with some practically useful deduction rules.
▷ We have implemented all methods in this work in our tool Cora, to allow for human-guided
  equivalence proofs with fully automatic termination and SMT implication checks. In
  section 8 we discuss our implementation.
    We relate our contributions to existing work in section 9, and conclude in section 10.
4                                        K. HAGENS AND C. KOP




                                           2. Preliminaries

2.1. Logically Constrained Simply Typed Rewriting Systems. We will recap LC-
STRSs [GK24], a higher-order rewriting formalism with built-in support for data structures
such as integers and booleans (or in fact any theory like bitvectors, floating point numbers or
integer arrays) as well as logical constraints to model control flow. This considers applicative
higher-order term rewriting (without λ) and first-order constraints.

Types. Assume given a set of sorts (base types) S; the set T of types is defined by the
grammar T ::= S | T → T . Here, → is right-associative, so all types may be written as
type 1 → . . . → type m → sort with m ≥ 0.
     We also assume given a subset Stheory ⊆ S of theory sorts (e.g., int and bool), and define
the theory types by the grammar Ttheory ::= Stheory | Stheory → Ttheory . Each theory sort
ι ∈ Stheory is associated with a non-empty interpretation set Iι (e.g., Iint = Z, the set of all
integers). We define Iι→σ as the set of all total functions from Iι to Iσ .

Terms. We assume given a signature Σ of function symbols and a disjoint set V of variables,
and a function typeof from Σ ∪ V to T ; we require that there are infinitely many variables
of all types. The set of terms T (Σ, V) over Σ and V are the expressions in T – defined by
the grammar T ::= Σ | V | T T – that are well-typed : a :: typeof (a) for a ∈ Σ ∪ V, and if
s :: σ → τ and t :: σ then s t :: τ . Application is left-associative, which allows all terms to
be written in a form a t1 · · · tn with a ∈ Σ ∪ V and n ≥ 0. Writing t = a t1 · · · tn , we define
head (t) = a. For a term t, let V ar(t) be the set of variables occurring in t. For multiple
terms t1 , . . . , tn , let V ar(t1 , . . . , tn ) denote V ar(t1 ) ∪ · · · ∪ V ar(tn ). A term t is ground if
V ar(t) = ∅. It is linear if no variable occurs more than once in t.
     We assume that Σ is the disjoint union Σtheory ⊎ Σterms , where typeof (f) ∈ Ttheory
for all f ∈ Σtheory . We use infix notation for the binary symbols, or use [f] for prefix or
partially applied notation (e.g., [+] x y and x + y are the same). Each f ∈ Σtheory has an
interpretation [[f]] ∈ Itypeof (f) . For example, a theory symbol ∗ :: int → int → int may be
interpreted as multiplication on Z. Symbols in Σterms do not have an interpretation. Values
are theory symbols of base type, i.e. Val = {v ∈ Σtheory | typeof (v) ∈ Stheory }. We assume
there is exactly one value for each element of Iι (ι ∈ Stheory ). Elements of T (Σtheory , V) are
called theory terms. For ground theory terms, we define [[s t]] = [[s]]([[t]]), thus mapping each
ground term of type σ to an element of Iσ . We fix a theory sort bool with Ibool = {⊤, ⊥}. A
constraint is a theory term s of type bool, such that typeof (x) ∈ Stheory for all x ∈ V ar(s).
Example 2.1. Throughout this text we will always use Stheory = {int, bool} and Σtheory =
{+, −, ∗, <, ≤, >, ≥, =, ∧, ∨, ¬, true, false} ∪ {n | n ∈ Z}, with +, −, ∗ :: int → int → int,
<, ≤, >, ≥, =:: int → int → bool, ∧, ∨ :: bool → bool → bool, ¬ :: bool → bool, true, false ::
bool and n :: int. We let Iint = Z, Ibool = {⊤, ⊥} and interpret all symbols as expected. The
values are true, false and all n. Theory terms are for instance x + 3, true and 7 ∗ 0. The
latter two are ground. We have [[7 ∗ 0]] = 0. The theory term x > 0 is a constraint, but the
theory term (f x) > 0 with f ∈ V of type int → int is not (since typeof (f ) ∈
                                                                             / Stheory ), nor is
[>] 0 :: int → bool (since constraints must have type bool).
Remark 2.2. Most programming languages have pre-defined (non-recursive) data structures
and operators, e.g. the integers with a multiplication operator ∗. This makes it, for instance,
possible to define the factorial function without first having to define multiplication. The
same is true for LCSTRSs: Σtheory contains all pre-defined operators, including constants.
                        BOUNDED REWRITING INDUCTION FOR LCSTRSs                                  5




Substitutions. A substitution is a type-preserving mapping γ : V → T (Σ, V). The
domain of a substitution is defined as dom(γ) = {x ∈ V | γ(x) ̸= x}, and its image as
im(γ) = {γ(x) | x ∈ dom(γ)}. A substitution on finite domain {x1 , . . . , xn } is often denoted
[x1 := s1 , . . . , xn := sn ]. A substitution γ is extended to a function s 7→ sγ on terms by
placewise substituting variables in the term by their image: (i) tγ = t if t ∈ Σ, (ii) tγ = γ(t)
if t ∈ V, and (iii) (t0 t1 )γ = (t0 γ) (t1 γ). If M ⊆ T (Σ, V) then γ(M ) denotes {tγ | t ∈ M }.
     A ground substitution is a substitution γ such that for all variables x in its domain, γ(x)
is a ground term. A unifier of terms s, t is a substitution γ such that sγ = tγ; a most general
unifier or mgu is a unifier γ such that all other unifiers are instances of γ. For unifiable
terms, an mgu always exists, and is unique modulo variable renaming.
     We say that a substitution γ respects a constraint φ if γ(V ar(φ)) ⊆ Val and [[φγ]] = ⊤.
We say that a constraint φ is satisfiable if there exists a substitution γ that respects φ. It is
valid if [[φγ]] = ⊤ for all substitutions γ such that γ(V ar(φ)) ⊆ Val.

Contexts and subterms. Let □1 , . . . , □n be fresh, typed constants (n ≥ 1). A context
C[□1 , . . . , □n ] (or just: C) is a term in T (Σ ∪ {□1 , . . . , □n }, V) in which each □i occurs
exactly once. (Note that □i may occur at the head of an application.) The term obtained
from C by replacing each □i by a term ti of the same type is denoted by C[t1 , . . . , tn ].
    We say that t is a subterm of s, notation s ⊵ t, if there is a context C[□] such that
s = C[t]. We say that t is a strict subterm of s, notation s ▷ t, if s ⊵ t and s ̸= t.

Rewrite rules. A rule is an expression ℓ → r [φ]. Here ℓ and r are terms of the same type, ℓ
has a form f ℓ1 · · · ℓk with f ∈ Σ and k ≥ 0, φ is a constraint and V ar(r) ⊆ V ar(ℓ) ∪ V ar(φ).
If φ = true, we may denote the rule as just ℓ → r.
     Fixing a signature Σ, we define the set of calculation rules as:
                                                                                          
                                                      f ∈ Σtheory \ Val, all xi and y ∈ V,
      Rcalc = f x1 · · · xm → y [y = f x1 · · · xm ]
                                                      typeof (f) = ι1 → . . . → ιm → κ
     We furthermore assume given a set of rules R that satisfies the following properties:
▷ for all ℓ → r [φ] ∈ R: ℓ is not a theory term (such rules are contained in Rcalc )
▷ for all f ℓ1 · · · ℓk → r [φ], g ℓ′1 · · · ℓ′n → r′ [ψ] ∈ R ∪ Rcalc : if f = g then k = n
     The latter restriction blocks us for instance from having both a rule append nil → id and a
rule append (cons x y) z → cons x (append y z). While such rules would normally be allowed
in higher-order rewriting, we need to impose this limitation for the notion of quasi-reductivity
to make sense, as discussed in [HK24]. This does not really limit expressivity, since we can
pad both sides with variables, e.g., replacing the first rule above by append nil x → id x.
     For a fixed signature and rules R as above, we define three classes of function symbols:
▷ elements of D = {f ∈ Σ | there is a rule f ℓ1 · · · ℓk → r [φ] ∈ R} are called defined symbols;
▷ elements of C = Val ∪ (Σterms \ D) are called constructors;
▷ elements of Σcalc = Σtheory \ Val are called calculation symbols.
     For every defined or calculation symbol f :: σ1 → . . . → σm → ι with ι ∈ S, we let ar (f)
be the unique number 0 ≤ k ≤ m such that for every rule of the form f ℓ1 · · · ℓk → r [φ]
in R ∪ Rcalc we have ar (f) = k. (By the restrictions above, such k always exists.) For all
constructors f ∈ C, we define ar (f) = ∞.
     We say that a substitution γ respects ℓ → r [φ] if it respects φ.
Remark 2.3. Note that it is theoretically possible for a rule to have a calculation symbol at
the head of its left-hand side, so a function symbol can be both a calculation symbol and a
6                                       K. HAGENS AND C. KOP




defined symbol. However, this would rarely occur in practice – it is allowed because methods
like rewriting induction might create “rules” of unusual forms to be used in a termination
proof, and it does not harm our method or the difficulty of the proofs to admit such rules.

Reduction relation. For a fixed signature Σ and set of rules R as discussed above, the
reduction relation →R is defined by:
                  C[lγ] →R C[rγ] if ℓ → r [φ] ∈ R ∪ Rcalc and γ respects φ
Note that by definition of context, reductions may occur at the head of an application. For
example, if append nil → id ∈ R, then we could reduce append nil s →R id s. We say that
s has normal form t if s →∗R t and t cannot be reduced. If we want to emphasize that
reduction s →R t is performed with a rule in Rcalc , we write s →Rcalc t instead.

LCSTRS. A Logically Constrained Simply-typed Term Rewriting System (LCSTRS) is a
pair (T (Σ, V), →R ) generated by (S, Stheory , Σterms , Σtheory , V, typeof , I, [[·]], R). We often
refer to an LCSTRS by L = (Σ, R), or just R, leaving the rest implicit.
Example 2.4. Let R consist of the following rules
             (R1) recdown f n i a         →   a                                [i < n]
             (R2) recdown f n i a         →   f i (recdown f n (i − 1) a)      [i ≥ n]
             (R3)   tailup f i m a        →   a                                [i > m]
             (R4)   tailup f i m a        →   tailup f (i + 1) m (f i a)       [i ≤ m]
We have S = Stheory = {int, bool}, Σterms = {recdown, tailup :: (int → int → int) → int →
int → int → int} and Σtheory the same as in Example 2.1. We have Σcalc = {+, −, ∗, <, ≤
, >, ≥, =, ∧, ∨}, D = Σterms and C = Val = {true, false} ∪ {n | n ∈ Z}. The substitution
γ = [n := 0, i := 1] respects (R2), and induces a reduction
     recdown f 0 1 a                →R f 1 (recdown f 0 (1 − 1) a)     →Rcalc
     f 1 (recdown f 0 0 a)          →R f 1 (f 0 (recdown f 0 (0−1) a)) →Rcalc
     f 1 (f 0 (recdown f 0 (−1) a)) →R f 1 (f 0 a)
It is easy to check that (tailup f n i a)γ = tailup f 0 1 a also reduces to f 1 (f 0 a).
     Intuitively, recdown and tailup define recursors which capture a class of simple programs
that compute a return value via a recursive or tail-recursive procedure. This considers
programs using a loop index i, which is decreased or increased by 1 at each recursive call,
until i is below the lower bound n or above the upper bound m. Then, the computation
terminates and returns a. With this, we can for example represent the two programs below
int factRec ( int x ) {
                                                  int factTail ( int x ) {
   if ( x >= 1)
                                                     int a = 1 , i = 1;
      return ( x * factRec (x -1) ) ;
                                                     while (i <= x ) { a = i * a ; i = i +1; }
   else
                                                     return a ; }
      return 1; }
by introducing rewrite rules factRec x → recdown [∗] 1 x 1 and factTail x → tailup [∗] 1 x 1.
Specifically, recdown [∗] n i a computes ( ik=n k)·a and tailup [∗] j m b computes ( m
                                          Q                                         Q
                                                                                      k=j k)·b.
Hence, all ground instances of recdown [∗] n i a and tailup [∗] n i a produce the same result.
In subsection 3.1 we will prove this with Bounded RI for arbitrary f :: int → int → int.
    We consider several properties an LCSTRS L = (Σ, R) can exhibit:
                        BOUNDED REWRITING INDUCTION FOR LCSTRSs                                 7




▷ L is terminating if there is no infinite reduction sequence s0 →R s1 →R s2 →R . . . for
  any s0 ∈ T (Σ, V)
▷ L is weakly normalising if every term has at least one normal form
  (note that termination implies weak normalisation, but not the other way around)
▷ L is confluent if for all s, t, q ∈ T (Σ, V): if s →∗R t and s →∗R q then there is some
  w ∈ T (Σ, V) such that t →∗R w and q →∗R w
▷ L is ground confluent if it is confluent on ground terms: for all s, t, q ∈ T (Σ, ∅): if s →∗R t
  and s →∗R q then there is some w ∈ T (Σ, ∅) such that t →∗R w and q →∗R w
▷ L has unique normal forms if for any term s there is at most one term t in normal form
  so that s →∗R t
  (note that confluence implies having unique normal forms, but not the other way around)
Viewing LCSTRSs as programs, uniqueness of ground normal forms – which is implied
by ground confluence – essentially expresses that output is produced deterministically. If,
moreover, the LCSTRS is weakly normalising, every term computes a unique result.

2.2. Rewriting induction prerequisites. Finally, we will recap the notions of equations,
inductive theorems, and the restrictions that an LCSTRS must satisfy to be able to apply
rewriting induction. For this, we follow the definitions from [HK24].

Equations and inductive theorems. An equation is a triple s ≈ t [φ] with typeof (s) =
typeof (t) and φ a constraint., If the constraint φ is true, we will simply write the equation
as s ≈ t. A substitution γ respects s ≈ t [φ] if γ respects φ and V ar(s, t) ⊆ dom(γ).
    An equation s ≈ t [φ] is an inductive theorem (aka ground convertible) if sγ ↔∗R tγ for
every ground substitution γ that respects s ≈ t [φ]. Here ↔R = →R ∪ ←R , and ↔∗R is its
transitive, reflexive closure.
    For a set of equations E, we define ↔E as follows:
              C[sγ] ↔E C[tγ] if s ≈ t [φ] ∈ E or t ≈ s [φ] ∈ E and γ respects φ
Note that E consists of inductive theorems if and only if ↔E ⊆ ↔∗R holds on ground terms
(i.e. when restricting to ground substitutions γ and ground contexts C).
Remark 2.5. In higher-order rewriting, there are multiple ways to define inductive theorems.
In particular one could choose to take into account extensionality [AYT04], which equates
two functions if they are equal on all their arguments (for example, in such a definition
[+] 0 ≈ [∗] 1 [true] would be an inductive theorem, which is not the case in our definition).
Here, we will not further motivate our choice, as this is a separate topic that we have
extensively discussed in [HK24]. One may also consider extensibility [AYC11], which limits
inductive theorems to those equations that are still ground convertible in “any reasonable
extension” of R. We will briefly discuss this in section 10.
Example 2.6. The LCSTRS from Example 2.4 admits an equation recdown f n i a
≈ tailup f n i a. Since it has constraint true, any substitution on domain ⊇ {f, n, i, a}
respects it. In subsection 3.1 we will prove that this equation is an inductive theorem,
meaning that (recdown f n i a)γ ↔∗R (tailup f n i a)γ for any ground substitution γ.
    We will limit our interest to quasi-reductive LCSTRSs (defined below), which is needed
to guarantee soundness of RI. Intuitively, this property expresses that pattern matching
on ground terms is exhaustive (i.e. there are no missing reduction cases). For example,
the rewrite system R = {(R1), (R2)} is quasi-reductive because i < n and i ≥ n together
8                                     K. HAGENS AND C. KOP




cover all ground instances of recdown f n i a. But if, for example, we replace (R2) by
recdown f n i a → f i (recdown f n (i − 1) a) [i > n] then it is not, as we are missing all
ground reduction cases for i = n (for example recdown [∗] 0 0 0 does not reduce anymore).
    For first-order LCTRSs, quasi-reductivity is achieved by requiring that there are no
other ground normal forms than the ground constructor terms T (C, ∅). For higher-order
LCSTRSs, however, this definition does not work as we can have ground normal forms
with partially applied defined symbols (for example, recdown [+]). We therefore use the
higher-order generalization of the notion of constructor terms that was introduced in [HK24].

Semi-constructor terms. Let L = (Σ, R) be some LCSTRS. The semi-constructor terms
over L, notation SCT L , are defined by (i). V ⊆ SCT L (ii). if f ∈ Σ with f :: σ1 → . . . → σm → ι,
ι ∈ S and s1 :: σ1 , . . . , sn :: σn ∈ SCT L with n ≤ m and n < ar (f), then f s1 · · · sn ∈ SCT L .
    Semi-constructor terms are always normal forms. Furthermore, as ar (f) = ∞ for every
constructor f, the constructor terms T (C, V) are contained in SCT L . However, also terms
with partial applications, such as recdown [+] 3, are included. The set SCT ∅L refers to
ground semi-constructor terms, built without (i). A ground semi-constructor substitution
(abbreviated to gsc substitution) is a substitution such that im(γ) ⊆ SCT ∅L .

Quasi-reductivity. An LCSTRS L = (Σ, R) is quasi-reductive if for every t ∈ T (Σ, ∅) we
have t ∈ SCT ∅L or t reduces with →R . Put differently, the only irreducible ground terms
are semi-constructor terms. Weak normalization and quasi-reductivity together ensure that
every ground term reduces to a semi-constructor term. Note that, if s1 , . . . , sn are ground
normal forms and f ∈ Σ, then f s1 · · · sn is a ground normal form if and only if n < ar (f).
    We say that an LCSTRS has inextensible theory sorts if the only constructors with
a type σ1 → . . . → σn → ι with ι ∈ Stheory are values (in which case n = 0). Hence, it
is not for instance allowed to have a constructor error :: int. While we do not explicitly
limit interest to LCSTRSs with inextensible theory sorts, it is satisfied in all our examples,
because in practice it is very difficult to achieve quasi-reductivity without this property.


                                   3. Rewriting Induction
RI was introduced by Reddy [Red90] in the year 1990 as a deduction system for proving
inductive theorems, using unconstrained first-order term rewriting systems. Since then, many
variations on the system have appeared (e.g., [Aot06, Aot08a, Aot08b, FK12, FKN17, HK24]).
All are based on well-founded induction, using some well-founded relation ≻. Depending on
how ≻ is being constructed these versions of RI can be categorized into two approaches
▷ The first, being used in [Red90, FK12, FKN17, HK24], employs a fixed strategy to
  construct a terminating rewrite system A ⊇ R and then chooses ≻ = →+       A.
▷ The second, used in [Aot06, Aot08a, Aot08b], employs a well-founded relation ≻ that
  satisfies certain requirements (like monotonicity and stability, but also ground totality),
  and constructs the proof in a more targeted way. This relation may either be fixed
  beforehand (e.g., the lexicographic path ordering), or constructed during or after the proof,
  as the proof process essentially accumulates termination requirements.
In practice, the former approach leads to quite heavy termination requirements because it
forces A to include all (oriented) induction hypotheses (represented by rewrite rules), while
the latter is designed to keep termination requirements as mild as possible; for example by
orienting some requirements using a relation ⪰ rather than ≻. However, the latter approach
                         BOUNDED REWRITING INDUCTION FOR LCSTRSs                                     9




imposes more bureaucracy, since derivation rules rely on several steps being done at once –
for example, by reasoning modulo the set of induction hypotheses. This makes it quite hard
to use especially when ≻ is not fixed beforehand but rather constructed on the fly.
     In subsection 3.1, we will introduce Bounded RI, which aims to combine the best of both
worlds. We reduce termination requirements by using a pair (≻, ⪰), which may either be
fixed in advance, or constructed as part of the proof process. In particular, we do not orient
induction hypotheses themselves: we only require that a particular instance of the induction
hypothesis is allowed to be applied whenever it is strictly dominated by some efficiently
chosen bounding term, being associated to the particular equation under consideration.
     Importantly, we do not impose the ground totality requirement (which would be ex-
tremely restrictive in higher-order rewriting!), and thus allow for ≻ to for instance be a
relation (→A ∪▷)+ , or built by a construction based on dependency pairs (see section 6).
     First, we will define the properties that our pair (≻, ⪰) should satisfy:
Definition 3.1 (Ordering and Bounding Pair). For a fixed set A, an ordering pair is a pair
(≻, ⪰) of a well-founded partial ordering ≻ on A (that is, ≻ is a transitive, anti-symmetric,
irreflexive and well-founded relation) and a quasi-order ⪰ (that is, ⪰ is a transitive and
reflexive relation) such that ≻ ⊆ ⪰, and both ≻ · ⪰ ⊆ ≻ and ⪰ · ≻ ⊆ ≻ (that is, for
a, b, c ∈ A, a ≻ b ⪰ c and a ⪰ b ≻ c imply a ≻ c). A bounding pair for a fixed LCSTRS with
rules R is an ordering pair (≻, ⪰) on T (Σ, ∅) such that s ⪰ t whenever s →R t or s ▷ t.
      We extend an ordering pair (≻, ⪰) to non-ground terms with a constraint as follows. A
substitution γ respects s, t, ψ if V ar(s, t) ⊆ dom(γ) and γ respects ψ. Then:
         s ≻ t [ψ] ⇐⇒ sγ ≻ tγ for all ground substitutions γ that respect s, t, ψ
         s ⪰ t [ψ] ⇐⇒ sγ ⪰ tγ for all ground substitutions γ that respect s, t, ψ


3.1. Bounded Rewriting Induction. Traditionally, RI is a deduction system on proof
states, which are pairs (E, H), where (in the existing literature), E is a set of equations,
describing all proof goals, and H is the set of induction hypotheses that have been assumed.
At the start E consists of all equations that we want to prove to be inductive theorems, and
H = ∅. With a deduction rule we may transform a proof state (E, H) into another proof
state (E ′ , H′ ), denoted (E, H) ⊢ (E ′ , H′ ). We write ⊢∗ for the reflexive-transitive closure of ⊢.
Soundness of RI is guaranteed by the following principle: “If (E, ∅) ⊢∗ (∅, H) for some set H,
then every equation in E is an inductive theorem”. Thus, we aim to make E empty.
    In bounded RI, we deviate in one respect: instead of letting E be a set of equations,
we will use a set of equation contexts. This new notion lets us avoid the bureaucracy of
combining steps by keeping track of two bounding terms, which together really dictate a
bound: we are only allowed to apply induction hypotheses below this bound.
Definition 3.2 (Equation context). Let a bounding pair (≻, ⪰) be given. Let • be a fresh
symbol, and define • ≻ s and • ⪰ s for all s ∈ T (Σ, V), and also • ⪰ •. An equation context
(ς ; s ≈ t ; τ) [ψ] is a tuple of two elements ς, τ ∈ T (Σ, V) ∪ {•}, two terms s, t and a
constraint ψ. We write (ς ; s ≃ t ; τ) [ψ] (so with ≃ instead of ≈) to denote either an
equation context (ς ; s ≈ t ; τ) [ψ] or an equation context (τ ; t ≈ s ; ς) [ψ]. A substitution
γ respects an equation context (ς ; s ≈ t ; τ) [ψ] if γ respects ψ and V ar(ς, s, t, τ) ⊆ dom(γ).
    An equation context couples an equation with a bound on the induction: we implicitly
use the induction hypothesis: “all ground instances of an equation in H that are strictly
smaller than the current instance of ς ≈ τ [ψ] are convertible”. For example, in a proof
10                                  K. HAGENS AND C. KOP




that two instances of the factorial function are equivalent, we may encounter an induction
hypothesis fact1 m ≈ fact2 m [m ≥ 0], and an equation context (fact1 n ; fact1 k ≈
fact2 k ; fact2 n) [n > 0 ∧ n = k + 1]. For an appropriately chosen ≻ we have both
fact1 n ≻ fact1 k [n > 0 ∧ n = k + 1] and fact2 n ≻ fact2 k [n > 0 ∧ n = k + 1]. We can also
see that n > 0 ∧ n = k + 1 implies k ≥ 0. Hence, we can apply the induction hypothesis.
Definition 3.3 (Proof state). A proof state is a tuple (E, H) with E a set of equation
contexts and H a set of equations.
    From Definition 3.2 we can see that • behaves as an infinity-term with respect to ≻
and ⪰. As expressed below in Theorem 3.4: when using bounded RI to prove a set of
equations, we put them into a set E of equation contexts using infinite bounds ς = τ = •.
This is not a problem, because we always start with the proof state (E, ∅), so there are no
induction hypotheses available yet. Once we add an induction hypothesis to the proof state,
the bounds will be correctly lowered, as dictated by Figure 1(Induct).
Theorem 3.4 (Soundness of Bounded RI). Let L be a weakly normalizing, quasi-reductive
LCSTRS; A a set of equations; and let E be the set of equation contexts {(• ; s ≈ t ; •) [ψ] |
s ≈ t [ψ] ∈ A}. Let (≻, ⪰) be some bounding pair, such that (E, ∅) ⊢∗ (∅, H), for some H
using the derivation rules in Figure 1. Then every equation in A is an inductive theorem.
Remark 3.5. To avoid confusion we will clarify what we mean by soundness. Those familiar
with equational reasoning may expect a statement expressing the implication
              (⋆)     RI-provability =⇒ equality in every possible model of R
This is not what Theorem 3.4 refers to. Our notion of soundness does not consider all possible
models, but rather one particular model: we fix our semantics to inductive theorems, i.e.
R-ground convertibility. Thus, soundness should be interpreted as the following implication
                         RI-provability =⇒ R-ground convertibility
Those interested in a more semantical discussion of RI – and in particular the implication
(⋆) – may consider the recent publication [ANS24], which studies this question for LCTRSs.
     Theorem 3.4 will be proved in section 4. The deduction rules for Bounded RI are
provided in Figure 1, and will be explained in detail in subsection 3.2. While they assume
a fixed bounding pair as given, in practice we can leave this pair undecided, use the proof
system to collect requirements about it, and then select a suitable bounding pair at the end.
     First, we introduce a particular notation, used by some of the deduction rules in Figure 1.
Definition 3.6 (|=δ ). Let δ be a substitution and φ, ψ be constraints. We write ψ |=δ φ if
δ(V ar(φ)) ⊆ Val ∪ V ar(ψ), and ψ =⇒ φδ is a valid constraint.
     Hence, if ψ |=δ φ and γ is a substitution that respects ψ, then γ also respects φδ. This
is for example used in the deduction rule (Simplify) to ensure that every ground instance of
an equation C[ℓδ] ≈ t [ψ] can be reduced with a rewrite rule ℓ → r [φ].
Example 3.7. Consider the equation recdown f i′ i a ≈ t [i′ = i + 1] and rewrite rule
recdown f n i a → a [i < n], and let δ = [n := i′ ]. We have (i < n)δ = i < i′ and
(i′ = i + 1) |=δ (i < n) holds, because
▷ δ(V ar(i < n)) = δ({i, n}) = {i, i′ } ⊆ V ar(i′ = i + 1) = {i, i′ }
▷ (i′ = i + 1) =⇒ (i < n)δ is valid
                         BOUNDED REWRITING INDUCTION FOR LCSTRSs                                                    11




Figure 1: Derivation rules for Bounded Rewriting Induction, given a bounding pair (≻, ⪰).
(Simplify)
               (E ⊎ {(ς ; C[ℓδ] ≃ t ; τ) [ψ]}, H)
                                                          ℓ → r [φ] ∈ R ∪ Rcalc and ψ |=δ φ
               (E ∪ {(ς ; C[rδ] ≈ t ; τ) [ψ]}, H)

(Case)
                      (E ⊎ {(ς ; s ≈ t ; τ) [ψ]}, H)                          C a cover set of s ≈ t [ψ]

           (E ∪ {(ςδ ; sδ ≈ tδ ; τδ) [ψδ ∧ φ] | (δ, φ) ∈ C}, H)               (see Definition 3.10)


(Delete)
                      (E ⊎ {(ς ; s ≈ t ; τ) [ψ]}, H)
                                                             ψ unsatisfiable, or s = t
                                  (E, H)

(Semi-constructor)
      (E ⊎ {(ς ; f s1 · · · sn ≈ f t1 · · · tn ; τ) [ψ]}, H)
                                                                      n > 0 and (f ∈ V or n < ar (f ))
        (E ∪ {(ς ; si ≈ ti ; τ) [ψ] | 1 ≤ i ≤ n} , H)

(Induct)
                                (E ⊎ {(ς ; s ≈ t ; τ) [ψ]}, H)
                         (E ∪ {(s ; s ≈ t ; t) [ψ]}, H ∪ {s ≈ t [ψ]})

(Hypothesis)
        (E ⊎ {(ς ; C[ℓδ] ≃ t ; τ) [ψ]}, H)             ℓ ≃ r [φ] ∈ H and ψ |=δ φ and
        (E ∪ {(ς ; C[rδ] ≈ t ; τ) [ψ]}, H)             ς ≻ ℓδ [ψ] and ς ≻ rδ [ψ] and ς ⪰ C[rδ] [ψ]


(H-Delete)
               (E ⊎ {(ς ; C[ℓδ] ≃ C[rδ] ; τ) [ψ]}, H)            ℓ ≃ r [φ] ∈ H and ψ |=δ φ and
                               (E, H)                            ς ≻ ℓδ [ψ] or τ ≻ rδ [ψ]


(Generalize)/(Alter)
     (E ⊎ {(ς ; s ≈ t ; τ) [ψ]}, H)           (ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ] generalizes/alters (ς ; s ≈ t ; τ) [ψ]

    (E ∪ {(ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ]}, H)   (see Definition 3.11), and ς ′ ⪰ s′ [ψ ′ ] and τ′ ⪰ t′ [ψ ′ ]


(Postulate)
                                            (E, H)
                                (E ∪ {(• ; s ≈ t ; •) [ψ]}, H)

    As we will see in subsection 4.1, the proof system in Figure 1 satisfies a property called
Preserving Bounds, meaning that it only produces a specific kind of equation contexts:
Definition 3.8 (Bounded equation context). A bounded equation context is an equation
context (ς ; s ≈ t ; τ) [ψ] such that both ς ⪰ s [ψ] and τ ⪰ t [ψ].
    This property plays an important role in the soundness proof of Bounded RI, since it
allows us to avoid ordering requirements that would otherwise need to be added to Figure 1.
    In many practical cases, we will also consider an even stronger restriction:
12                                  K. HAGENS AND C. KOP




Definition 3.9 (Strongly bounded equation context). An equation context (ς ; s ≈ t ; τ) [ψ]
is strongly bounded if either ς = s or ς ≻ s [ψ], and also either τ = t or τ ≻ t [ψ].
     Clearly, all equation contexts at the start of a RI deduction are strongly bounded, as all
initial equation contexts have ς = τ = •. At first it may not be clear why strongly bounded is
a strictly stronger property than bounded. To illustrate this, consider the following example
with a well-founded ordering ≻ whose restriction to integers is defined as
                                 n ≻ m ⇐⇒ n > m ∧ n ≥ 0
Then n ⪰ m [n ≥ m ∧ n ≥ 0] holds, but we have neither n = m nor n ≻ m [n ≥ m ∧ n ≥ 0].
     In practice, we highly benefit from strong boundedness because many of the required
inequalities in Figure 1 can be established by a straightforward syntactic check: whenever
ς ̸= s, we immediately conclude ς ≻ s [ψ]. While strong boundedness is not necessarily
preserved by the rules of Figure 1, we can maintain it by a suitable choice of reduction pair
and careful application of the (Hypothesis), (Generalize), and (Alter) rules.

3.2. Explanation by example. We will now elaborate on the rules of Figure 1, and
illustrate their use through examples. We will also introduce the definitions of cover set and
generalizing / altering, which are used in Figure 1. To start, we will consider the LCSTRS
from Example 2.4 applied on the equation recdown f n i a ≈ tailup f n i a.
     Following Theorem 3.4, we aim to show that there is a set H such that
      (E1 , ∅) ⊢∗ (∅, H) with E1 := {(• ; recdown f n i a ≈ tailup f n i a ; •) [true]}
We do not fully choose the bounding pair (≻, ⪰) in advance. Rather, we will use the proof
process to accumulate requirements on the well-founded ordering ≻ to be used. However,
we precommit to a bounding pair where ⪰ is the reflexive closure of ≻, and s ≻ t whenever
s →R t or s ▷ t. With these assumptions, it is easy to maintain the property that all equation
contexts are strongly bounded. We will ensure this invariant throughout our RI proof.

(Induct). We introduce the following way to start an induction proof.

                              (E ⊎ {(ς ; s ≈ t ; τ) [ψ]}, H)
                       (E ∪ {(s ; s ≈ t ; t) [ψ]}, H ∪ {s ≈ t [ψ]})
     Here, two things happen. First, the current equation is added to the set H of induction
hypotheses, making it available for later application of (Hypothesis) or (H-Delete). Second,
the bounding terms ς, τ are replaced by s, t. This ensures that, when an induction hypothesis
is applied, it is only on equations that are strictly smaller than s ≈ t [ψ].
     In our running example, we use (Induct) to obtain (E1 , ∅) ⊢ (E2 , H2 ) where
                E2 = {(ς2 ; recdown f n i a ≈ tailup f n i a ; τ2 ) [true]}
                H2 = {recdown f n i a ≈ tailup f n i a}
We will retain ς2 = recdown f n i a and τ2 = tailup f n i a, for later reference.

(Case). Comparing the equation in E2 to R, which of the rules should we apply? As we
will see in (Simplify), this requires information about how the variables i, n in the equation
are instantiated; in this example the reduction behavior depends on which of the two cases,
i < n or i ≥ n, holds. This is where (Case) can help us, splitting an equation into multiple
cases. Of course, we have to make sure that the cases together cover the original equation.
                       BOUNDED REWRITING INDUCTION FOR LCSTRSs                                     13




Definition 3.10 (Cover set). A cover set of an equation s ≈ t [ψ] is a set C of pairs (δ, φ),
with δ a substitution and φ a constraint, such that for every gsc substitution γ respecting
s ≈ t [ψ], there exists (δ, φ) ∈ C and a substitution σ such that γ(x) = δ(x)σ for all
x ∈ dom(γ), and σ respects ψδ ∧ φ. (Hence, sγ ≈ tγ [ψγ] is an instance of sδ ≈ tδ [ψδ ∧ φ].)
    Now, the deduction rule (Case) reads as follows:
                     (E ⊎ {(ς ; s ≈ t ; τ) [ψ]}, H)                   C a cover set of s ≈ t [ψ]

          (E ∪ {(ςδ ; sδ ≈ tδ ; τδ) [ψδ ∧ φ] | (δ, φ) ∈ C}, H)        (see Definition 3.10)

    Continuing our example, we observe the only gsc terms of type int are values (since
we have inextensible theory sorts). Hence, C = {([], i < n), ([], i ≥ n)} is a cover set of
recdown f n i a ≈ tailup f n i a. Using (Case), we obtain (E2 , H2 ) ⊢ (E3 , H2 ) with
                     (                                                       )
                       (ς2 ; recdown f n i a ≈ tailup f n i a ; τ2 ) [i < n]
               E3 =
                       (ς2 ; recdown f n i a ≈ tailup f n i a ; τ2 ) [i ≥ n]
Note that the bounding terms ς2 , τ2 are unchanged because the substitutions in the cover
set were both empty. This is, however, not true in general (and we will see an alternative
situation later in this section). Strong boundedness is still satisfied, by ς = s and τ = t.

(Simplify). Next, we can use a rule ℓ → r [φ] ∈ R∪Rcalc to rewrite an equation C[ℓδ] ≃ t [ψ].

             (E ⊎ {(ς ; C[ℓδ] ≃ t ; τ) [ψ]}, H)
                                                     ℓ → r [φ] ∈ R ∪ Rcalc and ψ |=δ φ
             (E ∪ {(ς ; C[rδ] ≈ t ; τ) [ψ]}, H)
The requirement ψ |=δ φ makes sure that the δ-instance of ℓ → r [φ] is actually applicable.
The bounding terms are not affected by the reduction.
    Continuing our example, the first equation in E3 has constraint i < n, so we apply
(Simplify) on both sides, using (R1) and (R3). For the second equation, we also apply
(Simplify) to both sides, using (R2) and (R4). We obtain (E3 , H2 ) ⊢∗ (E4 , H2 ) with
                                                                                        
                                      (ς2 ; a ≈ a ; τ2 )                         [i < n]
   E4 =
           (ς2 ; f i (recdown f n (i − 1) a) ≈ tailup f (n + 1) i (f n a) ; τ2 ) [i ≥ n]
Note that for both equations (ς2 ; s ≈ t ; τ2 ) [ψ] we now have the property: ς2 ≻ s [ψ] and
τ2 ≻ t [ψ], since →R is included in ≻. Thus, strong boundedness is preserved.

(Delete). The following deduction rule allows us to remove an equation that has an
unsatisfiable constraint, or whose two sides are syntactically equal.

                    (E ⊎ {(ς ; s ≈ t ; τ) [ψ]}, H)
                                                       ψ unsatisfiable, or s = t
                                (E, H)
    In our example, we use (Delete) we obtain (E4 , H2 ) ⊢ (E5 , H2 ) with
     E5 = {(ς2 ; f i (recdown f n (i − 1) a) ≈ tailup f (n + 1) i (f n a) ; τ2 ) [i ≥ n]}

(Alter). It is often useful to rewrite an equation context to another that might be syntacti-
cally different, but has the same ground semi-constructor instances. Indeed, this may even
be necessary, for instance to support the application of a rewrite rule through (Simplify).
This is supported by the deduction rule (Alter), which relies on the following definition:
14                                         K. HAGENS AND C. KOP




Definition 3.11. We say that an equation context (ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ]
▷ generalizes (ς ; s ≈ t ; τ) [ψ] if for every gsc substitution γ that respects (ς ; s ≈ t ; τ) [ψ]
  there is a substitution δ that respects (ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ] such that sγ = s′ δ and tγ = t′ δ,
  and ςγ ⪰ ς ′ δ and τγ ⪰ τ′ δ.
▷ alters (ς ; s ≈ t ; τ) [ψ] if both
  – (ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ] generalizes (ς ; s ≈ t ; τ) [ψ], and
  – (ς ; s ≈ t ; τ) [ψ] generalizes (ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ].
Now, (Alter) is defined as follows

               (E ⊎ {(ς ; s ≈ t ; τ) [ψ]}, H)           (ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ] alters (ς ; s ≈ t ; τ) [ψ]

              (E ∪ {(ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ]}, H)   and ς ′ ⪰ s′ [ψ] and τ′ ⪰ t′ [ψ]

    There are many ways to use this deduction rule, but following the discussion in [HK24],
we will particularly consider two ways:
      I Replacing a constraint by an equi-satisfiable one: that is, altering (ς ; s ≈ t ; τ) [ψ]
        into (ς ; s ≈ t ; τ) [ψ ′ ] if (∃⃗x.ψ) ⇐⇒ (∃⃗y .ψ ′ ) is logically valid, where {⃗x} = V ar(ψ) \
        V ar(ς, s, t, τ) and {⃗y } = V ar(ψ ′ ) \ V ar(ς, s, t, τ). (This assumes that the system has
        inextensible theory sorts; if not, we must also require that V ar(ψ)\{⃗x} = V ar(ψ ′ )\{⃗y }.)
           A particular example of this case is to replace (ς ; s ≈ t ; τ) [ψ] by (ς ; s ≈ t ; τ) [ψ ∧
        x1 = u1 ∧ · · · ∧ xn = un ], where all xi are fresh variables, with xi ∈     / V ar(uj ) for j ≤ i.
     II Replacing variables by equivalent variables or values: that is, altering (ς ; s ≈ t ; τ) [ψ]
        into (ςγ ; sγ ≈ tγ ; τγ) [ψ] if γ = [x1 := u1 , . . . , xn := un ] and ψ =⇒ x1 = u1 ∧. . . xn =
        un is valid, where x1 , . . . , xn are variables and u1 , . . . , un are each variables or values.

      Back to our example! By case I above, we can use (Alter) to obtain (E5 , H2 ) ⊢ (E6 , H2 ):
                                                                                        
              (ς2 ; f i (recdown f n (i − 1) a) ≈ tailup f (n + 1) i (f n a) ; τ2 )
      E6 =
                                                       [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
To allow this rule to be applied, we must have ς2 ⪰ f i (recdown f n (i − 1) a) [φ] and
τ2 ⪰ tailup f (n + 1) i (f n a) [φ] where φ is the constraint i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n.
But this follows immediately from the fact that our previous equation context was strongly
bounded: if ς ≻ s [i ≥ n] then also ς ≻ s [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n], and similar for
τ ≻ t [i ≥ n]. Moreover, strong boundedness is clearly still satisfied.
Remark 3.12. The preservation of strong boundedness in our example is not a coincidence:
as we will see in Lemma 4.3, most of the deduction rules of Figure 1 preserve this property
automatically if ≻ includes →R and ▷. In (Alter) and (Generalize) this is not necessarily
the case, but it is when (Alter) is used in either way I or II above (see Lemma 4.4).
     We continue the example by two successive (Simplify) steps, using calculation rules
i − 1 → i′ [i′ = i − 1] and n + 1 → n′ [n′ = n + 1], to obtain (E7 , H2 )
                 (ς2 ; f i (recdown f n i′ a) ≈ tailup f n′ i (f n a) ; τ2 )
                                                                                     
       E7 =
                                                    [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
Note that these steps were only possible because of the (Alter) step that preceded them.
   (Again, strong boundedness is preserved because ≻ includes →R .)
                        BOUNDED REWRITING INDUCTION FOR LCSTRSs                                 15




(Hypothesis). Similar to (Simplify), we can use an induction hypothesis to reduce either
side of an equation. Here, finally, the bounding terms ς, τ come into play, as we need to
make sure that we have a decrease of some kind, to apply induction.

           (E ⊎ {(ς ; C[ℓδ] ≃ t ; τ) [ψ]}, H)     ℓ ≃ r [φ] ∈ H and ψ |=δ φ and
           (E ∪ {(ς ; C[rδ] ≈ t ; τ) [ψ]}, H)     ς ≻ ℓδ [ψ] and ς ≻ rδ [ψ] and ς ⪰ C[rδ] [ψ]

     We will use (Hypothesis) to reduce the lhs of the equation in E7 with the only induction
hypothesis from H2 in the direction recdown f n i a → tailup f n i a, with substitution
[i := i′ ]. This lets us deduce (E7 , H2 ) ⊢ (E8 , H2 ) with
                    (ς2 ; f i (tailup f n i′ a) ≈ tailup f n′ i (f n a) ; τ2 )
                                                                                         
            E8 =
                                                        [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
However, to be allowed to apply this deduction rule, we must show that the ≻ requirements
are satisfied; that is, that we have:
        recdown f n i a ≻ recdown f n i′ a     [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
                                      ′
        recdown f n i a ≻ tailup f n i a       [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
        recdown f n i a ⪰ f i (tailup f n i a) [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
                                           ′

The first of these is satisfied by the strong boundedness property. The second is an immediate
consequence of the third, since f i (tailup f n i′ a) ▷ tailup f n i′ a and we have committed to
let ▷ be included in ≻. For the third, we remember that (REQ1) still needs to be satisfied:
   (REQ1) recdown f n i a ≻ f i (tailup f n i′ a) [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
Here, we have replaced the ⪰ by a ≻ to ensure that strong boundedness is preserved. Since
⪰ is the reflexive closure of ≻, this is not actually a stronger requirement.
    Let ς9 = f i (tailup f n i′ a), τ9 = tailup f n′ i (f n a), and apply (Induct) to (E8 , H2 ):
                   (ς9 ; f i (tailup f n i′ a) ≈ tailup f n′ i (f n a) ; τ9 )
                                                                                       
         E9 =
                                                     [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
                                                                                            
              recdown f n i a ≈ tailup f n i a
H9 =
          f i (tailup f n i′ a) ≈ tailup f n′ i (f n a) [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
Next, we use (Case) again to split the constraint in E9 into i = n and i > n, giving (E10 , H9 ):
                   (ς9 ; f i (tailup f n i′ a) ≈ tailup f n′ i (f n a) ; τ9 )
                                                                                       
                                                                                       
                                                      [i′ = i − 1 ∧ n′ = n + 1 ∧ i = n]
                
                                                                                       
                                                                                        
        E10 =                              ′                  ′
                  (ς9 ; f i (tailup f n i a) ≈ tailup f n i (f n a) ; τ9 )             
                                                      [i′ = i − 1 ∧ n′ = n + 1 ∧ i > n]
                
                                                                                       
                                                                                        

Observing that i′ = i − 1 ∧ n′ = n + 1 ∧ i = n implies both n > i′ and n′ > i, and that
i′ = i − 1 ∧ n′ = n + 1 ∧ i > n implies both n ≤ i′ and n′ ≤ i, we use (Simplify) on both
sides of the first equation with (R3) and on both sides of the second equation with (R4)
respectively, to deduce (E10 , H9 ) ⊢∗ (E11 , H9 ):
                                                             [i′ = i − 1 ∧ n′ = n + 1 ∧ i = n] 
                                                                                              
        (ς9 ; f i a ≈ f n a ; τ9 )
 E11 =     (ς9 ; f i (tailup f (n + 1) i′ (f n a)) ≈ tailup f (n′ + 1) i (f n′ (f n a)) ; τ9 )
                                                             [i′ = i − 1 ∧ n′ = n + 1 ∧ i > n]
                                                                                              

Note that the first equation above does not yet satisfy the requirements for (Delete), even
though the i = n part of the constraint makes it look very delete-worthy. We resolve this by
using (Alter) (case II), replacing the first equation context by (ς9 ; f n a ≈ f n a ; τ9 ) [i′ =
16                                    K. HAGENS AND C. KOP




i − 1 ∧ n′ = n + 1 ∧ i = n], after which it can immediately be deleted. Also using (Alter)
(now case I) on the second equation, and then using (Simplify) with calculation rules as we
did before, we are left with (E12 , H9 ):
               (ς9 ; f i (tailup f n′ i′ (f n a)) ≈ tailup f n′′ i (f n′ (f n a)) ; τ9 )
                                                                                        
       E12 =
                                        [i′ = i − 1 ∧ n′ = n + 1 ∧ n′′ = n′ + 1 ∧ i > n]

(H-Delete). With this deduction rule we may delete any equation that has a subequation
which is an instance of an equation in H. The rule looks very similar to (Hypothesis), but
with lighter requirements on ≻.

                 (E ⊎ {(ς ; C[ℓδ] ≃ C[rδ] ; τ) [ψ]}, H)    ℓ ≃ r [φ] ∈ H and ψ |=δ φ and
                                 (E, H)                    ς ≻ ℓδ [ψ] or τ ≻ rδ [ψ]

    Consider our example. Renaming the variables to avoid confusion, the second hypothesis
in H9 reads: g x (tailup g y x′ z) ≈ tailup g y ′ x (g y z) [x′ = x − 1 ∧ y ′ = y + 1 ∧ x ≥ y].
Let δ be the substitution [g := f, x := i, x′ := i′ , y := n′ , y ′ := n′′ , z := f n a]. We can now
deduce (E12 , H9 ) ⊢ (∅, H9 ) if one of the following ordering requirements are satisfied:
 ς9 = f i (tailup f n i′ a) ≻ f i (tailup f n′ i′ (f n a)) [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
 τ9 = tailup f n′ i (f n a) ≻ tailup f n′′ i (f n′ (f n a)) [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
In fact, both are satisfied by the strong boundedness property so there is nothing to check.
     Having used (H-Delete) to remove the last remaining equation, we have shown (E1 , ∅) ⊢∗
(∅, H9 ), so by Theorem 3.4 the equation recdown f n i a ≈ tailup f n i a is an induc-
tive theorem – provided we indeed have a suitable bounding pair that satisfies (REQ1).
But this is easily achieved: we let ≻ be (→R∪Q ∪▷)+ where Q = {recdown f n i a →
f i (tailup f n i′ a) [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]}. This is a bounding pair because →R∪Q
is terminating (which can for instance be proved using static dependency pairs [GHKV24]).
Remark 3.13. The choice to take ≻ = (→R∪Q ∪▷)+ is quite natural: in many traditional
definitions of rewriting induction [Red90, FK12, FKN17, HK24] this is the only choice for
(≻, ⪰), with Q always being a directed version of the final H (so in the case of this example,
H9 ). However, while such a choice is natural in strategies for rewriting induction, we leave
it open in the definition to allow for alternative orderings, as we will discuss in section 6.

An example with structural induction. We continue with another example, both to
introduce the remaining deduction rules and to illustrate that the method can be used
not only for induction on integers, but also for structural induction on terms. Consider
Σterms = {nil :: list, cons :: int → list → list, app :: list → list → list} with rules
        (R1) app nil ys → ys          (R2) app (cons x xs) ys → cons x (app xs ys)
        (R3) rev nil ys → ys          (R4) rev (cons x xs) ys → rev xs (cons x ys)
    Suppose we wish to show that rev (app xs ys) nil ≈ app (rev ys nil) (rev xs nil) is
an inductive theorem. We start with E1 containing this equation coupled with bullets as
bounding terms, and after an (Induct) step end up with (E2 , H2 ) where:
           E2     =   {(ς2 ; rev (app xs ys) nil ≈ app (rev ys nil) (rev xs nil) ; τ2 )}
           H2     =   {rev (app xs ys) nil ≈ app (rev ys nil) (rev xs nil)}
            ς2    =   rev (app xs ys) nil
           τ2     =   app (rev ys nil) (rev xs nil)
                        BOUNDED REWRITING INDUCTION FOR LCSTRSs                                             17




(We will omit the constraint from equation contexts when it is just [true].)
    Now we apply (Case), using the cover set ([xs := cons a as], true), ([xs := nil], true).
This is indeed a cover set because every ground semiconstructor instance of xs must be
either nil or headed by the list constructor cons. We obtain (E2 , H2 ) ⊢ (E3 , H3 ) with:
                                                                                             
           (ς3 ; rev (app (cons a as) ys) nil ≈ app (rev ys nil) (rev (cons a as) nil) ; τ3 )
  E3 =
           (ς4 ; rev (app nil ys) nil ≈ app (rev ys nil) (rev nil nil) ; τ4 )
Where:
           ς3 = rev (app (cons a as) ys) nil                  ς4 = rev (app nil ys) nil
           τ3 = app (app (cons a as) ys) zs                   τ4 = app (app nil ys) zs
Note that here the bounding terms are substituted along with the equation. This is the only
deduction rule that does so.
    After a few (Simplify) steps on both equations, we end up with (E3 , H2 ) ⊢∗ (E4 , H2 ):
                                                                                            
          (ς3 ; rev (app as ys) (cons a nil) ≈ app (rev ys nil) (rev as (cons a nil)) ; τ3 )
  E4 =
          (ς4 ; rev ys nil ≈ app (rev ys nil) nil ; τ4 )

(Generalize). Consider the latter equation context. We could try to continue with the rules
as they are, interleaving (Simplify), (Induct) and (Case), but doing so continues to yield new
equations that cannot be eliminated easily; there is no place where we can apply an induction
hypothesis. Instead, it will prove beneficial to abstract this equation by generalizing it:

          (E ⊎ {(ς ; s ≈ t ; τ) [ψ]}, H)        (ς ′ ; s′ ≈ t′ ; τ′ ) [φ] generalizes (ς ; s ≈ t ; τ) [ψ]

         (E ∪ {(ς ′ ; s′ ≈ t′ ; τ′ ) [φ]}, H)   and ς ′ ⪰ s′ [ψ] and τ′ ⪰ t′ [ψ]

     This rule is quite similar to (Alter) (and in fact, every step that can be done by (Alter)
can also be done by (Generalize)), but they are used quite differently: (Alter) is designed to
set up an equation for the use of simplification or deletion, while (Generalize) is a form of
lemma generation, very similar to (Postulate).
     In the second equation of E4 , we use (Generalize) to abstract the term rev ys nil into a
fresh variable zs, deriving (E4 , H2 ) ⊢ (E5 , H2 ) with:
                                                                                             
           (ς3 ; rev (app as ys) (cons a nil) ≈ app (rev ys nil) (rev as (cons a nil)) ; τ3 )
  E5 =
           (zs ; zs ≈ app zs nil ; app zs nil)
This is a generalization because for every gsc substitution γ that respects true we can choose
the substitution δ = [zs := rev γ(ys) nil] ∪ [γ(x) | x ∈ V \ {zs}] and have both (rev ys nil)γ =
zsδ and (app (rev ys nil) nil)γ = (app zs nil)δ, as well as ς4 γ ⪰ zsδ = (rev ys nil)γ and
τ4 γ ⪰ (app zs nil)δ because (ς4 ; rev ys nil ≈ app (rev ys nil) nil ; τ4 ) is a bounded equation
context. Moreover, the ordering requirements of the derivation rule, zs ⪰ zs [true] and
app zs nil ⪰ app zs nil [true], clearly hold.
     Next, we use (Induct) to deduce (E5 , H2 ) ⊢ (E5 , H5 ), with:
                                                                                 
                         rev (app xs ys) nil ≈ app (rev ys nil) (rev xs nil)
               H5 =
                                         zs ≈ app zs nil
We use (Case) on the second equation, to split it up into separate cases for nil and cons:
                                                                                          
       (ς3 ; rev (app as ys) (cons a nil) ≈ app (rev ys nil) (rev as (cons a nil)) ; τ3 ) 
 E5 =    (nil ; nil ≈ app nil nil ; app nil nil)
         (cons x xs ; cons x xs ≈ app (cons x xs) nil ; app (cons x xs) nil)
                                                                                          
18                                     K. HAGENS AND C. KOP




The second of these equations is quickly dispatched through applications of (Simplify),
ending in a (Delete) step. For the third equation, we use (Simplify) to arrive at (E6 , H5 ):
                                                                                            
          (ς3 ; rev (app as ys) (cons a nil) ≈ app (rev ys nil) (rev as (cons a nil)) ; τ3 )
  E6 =
          (cons x xs ; cons x xs ≈ cons x (app xs nil) ; app (cons x xs) nil)

(Semi-constructor). To deal with constructors and partially applied function symbols, we
introduce our second-to-last rule from Figure 1.

        (E ⊎ {(ς ; f s1 · · · sn ≈ f t1 · · · tn ; τ) [ψ]}, H)
                                                                 n > 0 and (f ∈ V or n < ar (f ))
          (E ∪ {(ς ; si ≈ ti ; τ) [ψ] | 1 ≤ i ≤ n} , H)
Note that ar (f ) = ∞ when f is a constructor, so certainly n < ar (f ) holds.
    In our example, we use (Semi-constructor) to deduce (E6 , H5 ) ⊢ (E7 , H5 ):
                                                                                           
        (ς3 ; rev (app as ys) (cons a nil) ≈ app (rev ys nil) (rev as (cons a nil)) ; τ3 ) 
 E7 =     (cons x xs ; x ≈ x ; app (cons x xs) nil)
          (cons x xs ; xs ≈ app xs nil ; app (cons x xs) nil)
                                                                                           

The second equation context is immediately deleted. For the third, note that the equation
is an instance of the induction hypothesis zs ≈ app zs nil ∈ H, so we can dispatch it using
(H-Delete), provided the ordering requirements are satisfied. If we again choose a bounding
pair with ▷ ⊆ ≻, we certainly have (cons x xs)γ ≻ xsγ for all γ, which suffices.

(Postulate). To introduce our final rule, we observe that it would be really useful to have
some lemmas to reason about the relation between rev and app. This leads us to introduce:
                                       (E, H)
                           (E ∪ {(• ; s ≈ t ; •) [ψ]}, H)
    In our example, we use two successive applications of (Postulate) to obtain (E8 , H5 ):
                                                                                           
        (ς3 ; rev (app as ys) (cons a nil) ≈ app (rev ys nil) (rev as (cons a nil)) ; τ3 ) 
 E8 =     (• ; rev xs ys ≈ app (rev xs nil) ys ; •)
          (• ; app (app xs ys) zs ≈ app xs (app ys zs) ; •)
                                                                                           

The last equation is easily removed through (Induct) followed by a (Case) on the instantiation
of xs, some simplifications, a (Delete) in the nil case and a use of (Semi-constructor) followed
by (H-Delete) in the cons case; doing this causes no new ordering requirements to be added
since we had already set ▷ ⊆ ≻. Hence, we obtain (E8 , H5 ) ⊢ (E9 , H9 ) where:
                                                                                            
          (ς3 ; rev (app as ys) (cons a nil) ≈ app (rev ys nil) (rev as (cons a nil)) ; τ3 )
  E9 =
          (• ; rev xs ys ≈ app (rev xs nil) ys ; •)
                                                                               
                      rev (app xs ys) nil ≈ app (rev ys nil) (rev xs nil) 
              H9 =                        zs ≈ app zs nil
                        app (app xs ys) zs ≈ app xs (app ys zs)
                                                                               
Hence, the key benefit of (Postulate) is that we are left with an additional element of H,
which can be used in the proof of the remaining equations.
    Having introduced all our rules, we do not show the rest of the proof, but leave it as
an exercise to the reader. Proving the remaining equations does cause some new ordering
requirements to be imposed, but all of these are easily satisfied for instance by choosing for
≻ the lexicographic path ordering with rev > app > cons > nil.
                        BOUNDED REWRITING INDUCTION FOR LCSTRSs                               19




3.3. Completeness. Thus far, we have used rewriting induction to prove inductive theorems.
However, we can also use it to derive that some equations are not inductive theorems.
Example 3.14. Consider Σterms = {G :: (int → int) → int → int → int, H :: (int → int) →
int → int → int → int} with rules
                   Gf nx        →    G f (n − 1) (f x)       [n > 0]
                   Gf nx        →    x                       [n ≤ 0]
                  Hf nmx        →    H f (n − 1) m (f x)     [n > 0]
                  Hf nmx        →    H f (m − 1) n (f x)     [m > 0]
                  Hf nmx        →    x                       [n ≤ 0 ∧ m ≤ 0]
Intuitively, G computes the function (f, n, x) 7→ f n (x) for all n ≥ 0, and H computes the
function (f, n, m, x) 7→ f (n+m) (x) for all n, m ≥ 0. In particular, we have an inductive
theorem G f k x ≈ H f n m x [k = n + m ∧ n ≥ 0 ∧ m ≥ 0]. The condition n, m ≥ 0 is
really necessary: the equation G f k x ≈ H f n m x [k = n + m] is not an inductive theorem.
For example, there does not even exist a single ground substitution γ = [x := t] such that
(G ([+] 1) (−1) x)γ ↔∗R (H ([+] 1) 1 (−2) x)γ.
     To prove non-equivalences, we will extend RI with a new deduction rule (Disprove).
However, we must take some care: it is entirely possible, in the course of a RI proof, to end up
with unsound equations even if the original equations are all inductive theorems. For example,
recdown [+] n 0 a ≈ recdown [+] n (−1) a is an inductive theorem, but if we use (Generalize)
in the RI proof to obtain an equation recdown [+] n i a ≈ recdown [+] n i′ a [i′ = i − 1], we
will encounter a contradiction. Hence, we must carefully consider the derivation path.
Definition 3.15 (Completeness Property). We say a deduction rule has the Completeness
Property if, whenever R is a weakly normalizing, quasi-reductive, ground confluent LCSTRS,
if we can deduce (E, H) ⊢ (E ′ , H′ ) by this rule, then
   ↔E ∪ ↔H ⊆ ↔∗R on ground terms              =⇒      ↔E ′ ∪ ↔H′ ⊆ ↔∗R on ground terms
Here, ↔E is the relation ↔A where A = {s ≈ t [ψ] | (ς ; s ≈ t ; τ) [ψ] ∈ E}.
Lemma 3.16. The derivation rules (Simplify), (Case), (Delete), (Induct), (Hypothesis),
(Alter) and (H-Delete) all have the Completeness Property, as does the limitation of (Semi-
constructor) to cases with f ∈ Σ.
    Hence, all deduction rules of Figure 1 other than (Generalize), (Postulate) and the
general case of (Semi-constructor), are complete.
Proof. Suppose that R is weakly normalizing, quasi-reductive and ground confluent, and
that ↔E ∪ ↔H ⊆ ↔∗R on ground terms. Write A = {s ≈ t [ψ] | (ς ; s ≈ t ; τ) [ψ] ∈ E}.
     For any s ≈ t [ψ] ∈ H′ we have either s ≈ t [ψ] ∈ H or, if (Induct) was used, s ≈ t [ψ] ∈ A.
Either way, a step by this equation can also be done by ↔H ∪ ↔E , so indeed ↔H′ ⊆ ↔∗R
on ground terms. To show that ↔E ′ ⊆ ↔∗R on ground terms, let γ be a ground substitution
respecting some equation context in E ′ . Note that we only need to consider equation contexts
in E ′ \ E because for an equation context (ς ; s ≈ t ; τ) [ψ] ∈ E we can immediately conclude
that sγ ↔∗R tγ by assumption. We consider every deduction rule in the lemma.
(Simplify), (Hypothesis). Then E ′ \E = {(ς ; C[rδ] ≈ t ; τ) [ψ]} while A contains C[ℓδ] ≈ t [ψ]
for either some ℓ → r [φ] ∈ R ∪ Rcalc or some ℓ ≃ r [φ] ∈ H, and δ such that ψ |=δ φ. Since
γ respects ψ we have C[ℓδ]γ ↔∗R tγ by assumption on ↔A . Furthermore, in either case we
have C[rδ]γ ↔∗R C[ℓδ]γ, whether because ←R is included in ↔∗R or by assumption on ↔H .
20                                           K. HAGENS AND C. KOP




(Case). Then the only elements of E ′ \ E have a form (ςδ ; sδ ≈ tδ ; τδ) [ψδ ∧ φ], where
s ≈ t [ψ] ∈ A. As γ respects ψδ ∧ φ, it respects ψδ. Therefore, σ = δγ respects ψ, and is a
ground substitution; dom(σ) ⊇ V ar(s, t). Hence, sδγ = sσ ↔∗R tσ = tδγ, as desired.
(Delete), (H-Delete). We have E ′ \ E = ∅ so there is nothing to prove.
(Induct). For all (ς ; s ≈ t ; τ) [ψ] ∈ E ′ we have s ≈ t [ψ] ∈ A.
(Alter). Then E ′ \ E = {(ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ]} and there is some (ς ; s ≈ t ; τ) [ψ] ∈ E
which generalizes (ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ]. Since R is weakly normalizing and quasi-reductive,
γ ↓ = [x := γ(x)↓R | x ∈ dom(γ)] is a well-defined, gsc substitution that respects (ς ′ ; s′ ≈
t′ ; τ′ ) [ψ ′ ]. By definition of generalization, there is a substitution σ that respects (ς ; s ≈
t ; τ) [ψ] with sσ = s′ γ ↓ and tσ = t′ γ ↓ . Hence, s′ γ →∗R s′ γ ↓ = sσ ↔∗R tσ = t′ γ ↓ ←∗R t′ γ.
(Semi-constructor) (with f ∈ Σ). Then E ′ \ E = {(ς ; si ≈ ti ; τ) [ψ] | 1 ≤ i ≤ n}
for some (ς ; f s1 · · · sn ≈ f t1 · · · tn ; τ) [ψ] ∈ E, with n < ar (f). By assumption,
(f s1 · · · sn )γ ↔∗R (f t1 · · · tn )γ. Now, note that R is ground confluent. So in fact there is some
u such that both (f s1 · · · sn )γ →∗R u and (f t1 · · · tn )γ →∗R u. Since n < ar (f), necessarily u
has the form f u1 · · · un with both si γ →∗R ui and ti γ →∗R ui for all 1 ≤ j ≤ n.
    With the notion of a complete deduction step, we can define the states in a derivation
path that are suitable for the new deduction rule that we wish to introduce:
Definition 3.17 (Complete proof state). Let P1 ⊢∗ Pn be some RI deduction sequence and
1 ≤ i ≤ n. Proof state Pi = (Ei , Hi ) is complete if one of the following holds
 (a). i = 1;
 (b). Pi−1 is complete and Pi−1 ⊢ Pi by a deduction rule with the Completeness Property;
 (c). there is a complete proof state Pj with j < i and Ei ⊆ Ej .
Cases (a) and (b) together ensure that deductions remain complete as long as they only use
steps with the Completeness Property. With (c) we can restore completeness, once we have
removed all equations originating from deduction steps that cause loss of completeness.
Definition 3.18 (Contradictory equation). An equation s ≈ t [ψ] is contradictory if there
exists a ground substitution δ that respects ψ, such that one of the following holds:
(1). there exist f, g ∈ Σ with f ̸= g, as well as s′1 , . . . , s′n , t′1 , . . . , t′m such that sδ = f s′1 · · · s′n
     and tδ = g t′1 · · · t′m and n < ar (f) and m < ar (g)
(2). s, t ∈ T (Σtheory , V) and [[(ψ ∧ s ̸= t)γ]] = ⊤
    Note that if s and t only have base-type variables, then the existence of a suitable
substitution γ for case (2) corresponds exactly to satisfiability of ψ ∧ (s ̸= t). However, when
s or t contains higher-order variables, then we first have to choose an instantiation for every
such variable before we can check for satisfiability. For example, if we have an equation
x ≈ f x [ψ] with x :: int and f :: int → int then ψ ∧ (x ̸= f x) is not a constraint and we first
have to instantiate f as a theory term (e.g. f := [+] 1) before we can establish satisfiability.
    Now, we formulate our deduction rule for proving non-theorems:

(Disprove). A complete proof state with a contradictory equation yields ⊥.
                  P = (E ∪ {(ς ; s ≈ t ; τ) [ψ]}, H) P is complete
                                  ⊥                  s ≈ t [ψ] is contradictory
In such a case, s ≈ t [ψ] cannot be an inductive theorem, as expressed by the following
theorem (which we will prove in subsection 4.5).
                       BOUNDED REWRITING INDUCTION FOR LCSTRSs                              21




Theorem 3.19 (Completeness of RI). Let L be a weakly normalizing, quasi-reductive,
ground confluent LCSTRS and let E be a set of equations. If (E, ∅) ⊢∗ ⊥ then there is an
equation in E which is not an inductive theorem.
     We assume weak normalization in Definition 3.15 and Theorem 3.19 because, without
this assumption, (Alter) would not have the Completeness Property. If the derivation
(E, ∅) ⊢∗ ⊥ does not use the (Alter) step, then the conclusion of Theorem 3.19 can still be
obtained without having to require weak normalization.
Example 3.20. Consider the LCSTRS from Example 3.14. The system is terminating
and in Example 5.12 we will also prove ground confluence. Let E1 = {(• ; G f k x ≈
H f n m x ; •) [k = n + m]}. We will derive (E1 , ∅) ⊢∗ ⊥. First, we apply (Case) to obtain
                                                                                 
           (E1) (• ; G f k x ≈ H f n m x ; •) [k < 0 ∧ n > 0 ∧ k = n + m]
                                                                                 
      E2 = (E2) (• ; G f k x ≈ H f n m x ; •) [k ≥ 0 ∧ k = n + m]
                                                                                 
             (E3) (• ; G f k x ≈ H f n m x ; •) [n ≤ 0 ∧ k = n + m]
                                                                                 

Equation context (E1) will bring us to ⊥, so we can forget about (E2) and (E3). After
applying some (Simplify) steps, together with (Alter), we obtain
      E3 ⊇ (• ; x ≈ H f n′ m (f x) ; •) [n′ = n − 1 ∧ k < 0 ∧ n > 0 ∧ k = n + m]
           

A new application of (Case), followed by a number of (Simplify)-steps with R yields
E4 ⊇ {(E1)’, (E2)’}, with:
 (E1)’ (• ; x ≈ f x ; •)                 [n′ ≤ 0 ∧ n′ = n − 1 ∧ k < 0 ∧ n > 0 ∧ k = n + m]
 (E2)’ (• ; x ≈ H f n′ m (f x) ; •) [n′ > 0 ∧ n′ = n − 1 ∧ k < 0 ∧ n > 0 ∧ k = n + m]
Now, (E1)’ is contradictory by Definition 3.18.(2), so with (Disprove) we obtain ⊥. By
Theorem 3.19 it follows that G f k x ≈ H f n m x [k = n + m] is not an inductive theorem.


                                         4. Proofs
In this section, we shall prove the soundness and completeness theorems of section 3, in
a form that allows for easily adding new deduction rules. In addition, we will supply the
results mentioned in Remark 3.12, which allow us to limit interest to bounded equation
contexts when using Bounded Rewriting Induction. This section is organized as follows
▷ In subsection 4.1 we show that Bounded RI – as presented in Figure 1 – restricts to a
  proof system on bounded equation contexts. This property is called Preserving Bounds.
▷ In subsection 4.2 we introduce some necessary prerequisites on multisets.
▷ In subsection 4.3 we introduce R-bounded ground convertibility; a restriction of R-ground
  convertibility which limits intermediate terms in the conversion using the bounding pair
  (≻, ⪰). We use this notion to express the Base Soundness property, and prove that every
  deduction rule except (Induct) satisfies this property. This allows us to obtain a more
  transparent and modular proof procedure towards proving Theorem 3.4.
▷ In subsection 4.4 we accumulate the results of the preceding subsections to finally conclude
  the statement of Theorem 3.4. In particular, Theorem 4.18 shows that every deduction
  rule that satisfies Preserving Bounds and the Base Soundness property is sound.
▷ In subsection 4.5 we prove the full completeness statement of Theorem 3.19 by induction
  on the length of a derivation sequence that ends in ⊥. The base case is covered by
  Proposition 4.22, after which the full proof is obtained using Lemma 3.16.
22                                  K. HAGENS AND C. KOP




4.1. Bounded equation contexts. In the following, we assume given a fixed bounding
pair (≻, ⪰) on T (Σ, V). In this subsection we will show that Bounded Rewriting Induction
can always be limited to bounded equation contexts.
Definition 4.1 (Preserving Bounds). We say that a deduction rule preserves bounds if,
whenever (E, H) ⊢ (E ′ , H′ ) and all equation contexts in E are bounded, then also all equation
contexts in E ′ are bounded.
    We say that it preserves strong bounds if, whenever (E, H) ⊢ (E ′ , H′ ) and all equation
contexts in E are strongly bounded, then also all equation contexts in E ′ are strongly bounded.
Lemma 4.2. All derivation rules in Figure 1 preserve bounds.
Proof. All elements of E ′ ∩ E are bounded equation contexts by assumption; as for the rest,
consider the rule by which (E, H) ⊢ (E ′ , H′ ):
(Simplify): E ′ \ E = {(ς ; C[rδ] ≈ t ; τ) [ψ]} with (ς ; C[ℓδ] ≈ t ; τ) [ψ] ∈ E. Because
      the original equation context is bounded, we have both τ ⪰ t [ψ] and ς ⪰ C[ℓδ] [ψ].
      Because →R ⊆ ⪰, we have C[ℓδ] ⪰ C[rδ] [ψ]. Then ς ⪰ C[rδ] [ψ] by transitivity of ⪰.
(Case): E contains a bounded equation context (ς ; s ≈ t ; τ) [ψ], and E ′ \ E contains
      equation contexts (ςδ ; sδ ≈ tδ ; τδ) [ψδ ∧ φ]. To see that these are bounded as well,
      consider a ground substitution σ that respects ψδ ∧ φ. This substitution certainly
      respects ψδ, so the composition δσ respects ψ. Since by assumption ς ⪰ s [ψ] and
      τ ⪰ t [ψ] hold, we have ς(δσ) ⪰ s(δσ) and τ(δσ) ⪰ t(δσ).
(Delete),(H-Delete): E ′ \ E = ∅
(Semi-constructor): E ′ \ E contains only equation contexts (ς ; si ≈ ti ; τ) [ψ] where
      E contains a bounded equation context (ς ; f s1 · · · sn ≈ f t1 · · · tn ; τ) [ψ]; since
      ςγ ⪰ (f s1 · · · sn )γ implies ςγ ⪰ si γ (as ⪰ is transitive and includes ▷), and we
      similarly have τγ ⪰ ti γ, all elements of E ′ \ E are bounded.
(Induct): E ′ \ E = {(s ; s ≈ t ; t) [ψ]} and s ⪰ s [ψ] and t ⪰ t [ψ] hold by reflexivity of ⪰.
(Hypothesis): E ′ \ E = {(ς ; C[r] ≈ t ; τ) [ψ]} where ς ⪰ C[r] [ψ] by definition of the
      deduction rule, and τ ⪰ t [ψ] because the input equation is bounded.
(Generalize)/(Alter): Boundedness of the result is a requirement of the deduction rule.
(Postulate): The only fresh equation context is (• ; s ≈ t ; •) [ψ], and • ≻ sγ, tγ holds.
   By almost the same proof we can see that the derivation rules – when applied in certain
ways and with a suitably restricted bounding pair – can also preserve strong bounds.
Lemma 4.3. Suppose s ≻ t whenever s →R t or s ▷ t. Let s ⪰! t [ψ] denote that either
s = t or s ≻ t [ψ]. Consider the variation of the proof system of Figure 1 where any use of
⪰ is replaced by ⪰! . All derivation rules in this variant preserve strong bounds.
     Note that ⪰ is only used in the definition of (Hypothesis), (Generalize) and (Alter), so
all other derivation rules preserve strong bounds without modification.
Proof. The proof is a straightforward adaptation of the proof of 4.2, observing that if
a ⪰! b [φ] and b ⪰! c [φ] then a ⪰! c [φ] immediately follows.
▷ For (Simplify), we use that certainly C[ℓδ] ≻ C[rδ] [ψ] because →R is included in ≻.
▷ For (Case), we observe that a ⪰! b [φ] clearly implies aδ ⪰! bδ [φδ] as well.
▷ For (Semi-constructor), we observe that f s1 · · · sn ⪰! si [ψ] for any ψ because ▷ is
  included in ≻ (as ⪰ is the reflexive closure of ≻ and a ▷ b implies a ̸= b).
▷ All other cases are immediately obvious.
                            BOUNDED REWRITING INDUCTION FOR LCSTRSs                                           23




    We also observe that, as stated in Remark 3.12, the typical ways of using (Alter) preserve
both boundedness and strong boundedness without a need for additional checks:
Lemma 4.4. Suppose (ς ; s ≈ t ; τ) [ψ] is a bounded equation context, and (ς ′ ; s′ ≈
t′ ; τ′ ) [ψ ′ ] alters it by either method I or II. Then also (ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ] is a bounded
equation context. If (ς ; s ≈ t ; τ) [ψ] is strongly bounded, then so is (ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ].
Proof. First consider case I: in this case (ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ] is (ς ; s ≈ t ; τ) [φ], where:
▷ {x1 , . . . , xn } = V ar(ψ) \ V ar(ς, s, t, τ) and {y1 , . . . , ym } = V ar(φ) \ V ar(ς, s, t, τ);
▷ {z1 , . . . , zk } = V ar(φ, ψ) ∩ V ar(ς, s, t, τ);
▷ (∃x1 . . . xn .ψ) ⇔ (∃y1 . . . ym .φ) is logically valid; that is,
   for all appropriately typed values v1 , . . . , vk ,
   there exist values u1 , . . . , un s.t. [[ψ[z1 := v1 , . . . , zk := vk , x1 := u1 , . . . , xn := un ]]] = ⊤,
   if and only if
   there exist values w1 , . . . , wm s.t. [[φ[z1 := v1 , . . . , zk := vk , y1 := w1 , . . . , ym := wm ]]] = ⊤.
      Now, let γ be a ground substitution that respects φ. From “respects”, we know
that [[φγ]] = ⊤, so for the fixed values v1 = γ(z1 ), . . . , vk = γ(zk ), if we choose w1 =
γ(y1 ), . . . , wm = γ(ym ) then the second part of the “if and only if” above is satisfied, so we
can find values u1 , . . . , un that satisfy the first part. Now, let δ be the substitution that maps
each xi to ui and all other variables a to γ(a). Then indeed [[ψδ]] = [[ψ[z1 := v1 , . . . , zk :=
vk , x1 := u1 , . . . , xn := un ]]] = ⊤, so δ respects ψ, and since δ is identical to γ on all variables
in ς, s, t, τ, we have ςγ = ςδ ⪰ sδ = sγ and τγ = τδ ⪰ tδ = tγ as required.
      As for strong boundedness: if ς = s for the original, then clearly the same holds for
the altered context. Otherwise ς ≻ s [ψ] so, as we saw above, for all γ we find δ such that
ςγ = ςδ ≻ sδ = sγ. The same holds for τ and t.
      Now consider case II: in this case (ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ] has the form (ςγ ; sγ ≈ tγ ; τγ) [ψ]
where γ = [x1 := v1 , . . . , xn := vn ] such that ψ =⇒ x1 = v1 ∧ xn = vn is valid; that is, for
every substitution δ that respects ψ we have δ(xi ) = vi δ. Hence, ςγδ = ςδ ⪰ sδ = sγδ and
τγδ = τδ ⪰ tδ = tγδ as required, and similar for strong boundedness.


4.2. Multiset orderings. The proofs in the following subsections make substantial use of
the multiset extension of an ordering pair (≻, ⪰) on A = T (Σ, V). We particularly consider
multisets containing exactly 2 elements, which allows for a much simpler representation than
the common definitions in the literature (where multisets may have infinite size). Here, we
present our version of the multiset extension of an ordering pair, as follows:
     For an ordering pair (≻, ⪰) on A, a size-2 multiset over A is an unordered pair {{a, b}}
with a, b ∈ A (it is allows to have a = b). We say that:
• {{a1 , a2 }} = {{b1 , b2 }} if either a1 = b1 and a2 = b2 , or a1 = b2 and a2 = b1
• {{a1 , a2 }} ⪰mul {{b1 , b2 }} if one of the following holds:
  – there is some i ∈ {1, 2} such that both ai ≻ b1 and ai ≻ b2
  – either a1 ⪰ b1 and a2 ⪰ b2 , or a1 ⪰ b2 and a2 ⪰ b1
• {{a1 , a2 }} ≻mul {{b1 , b2 }} if one of the following holds:
  – there is some i ∈ {1, 2} such that both ai ≻ b1 and ai ≻ b2
  – there exist i, j ∈ {1, 2} such that ai ≻ bj and a3−i ⪰ b3−j
     Note that {{a1 , a2 }} ≻mul {{b1 , b2 }} implies {{a1 , a2 }} ⪰mul {{b1 , b2 }}, because ai ≻ bj
implies ai ⪰ bj . Hence, we easily see that the multiset extension (≻mul , ⪰mul ) is itself an
ordering pair on size-2 multisets over A.
24                                        K. HAGENS AND C. KOP




4.3. Bounded ground convertibility. In principle, to prove Theorem 3.4, it suffices to
show R-ground convertibility for every equation in E. However, as we will see, bounded
rewriting induction actually proves a stronger property, called bounded ground convertibility.
Definition 4.5 (R/H/E-Bounded convertility). Let R be a set of rewrite rules, (≻, ⪰) a
bounding pair, H a set of equations, and E a set of equation contexts. For a, b ∈ T (Σ, V)∪{•}
                                    {a,b}
and u, v ∈ T (Σ, V) we define u ←−−→ v if one of the following holds:
                                    R;H;E
(A) u = C[ℓσ] and v = C[rσ] for some ℓ → r [φ] or r → ℓ [φ] in R, such that:
    ▷ σ is a ground substitution that respects the rule
    ▷ a ⪰ ℓσ or b ⪰ ℓσ, and
    ▷ a ⪰ rσ or b ⪰ rσ
(B) u = C[ℓσ] and v = C[rσ] for some ℓ ≈ r [φ] or r ≈ ℓ [φ] in H such that:
    ▷ σ is a ground substitution that respects the equation, and
    ▷ {a, b} ≻mul {ℓσ, rσ}
(C) u = C[ℓσ] and v = C[rσ] for some (d ; ℓ ≈ r ; e) [φ] ∈ E such that:
    ▷ σ is a ground substitution that respects the equation context, and
    ▷ {a, b} ⪰mul {dσ, eσ}
           {a,b} ∗                                               {a,b}
We write ←−−−→ for the reflexive, transitive closure of ←−−→.
           R;H;E                                                R;H;E

Definition 4.6 (R/H/E-Bounded ground convertibility). Assume given a fixed LCSTRS
with rules R, and a bounding pair (≻, ⪰). Let H be a set of equations and E be a set
of equation contexts. An equation context (ς ; s ≈ t ; τ) [ψ] is R/H/E-bounded ground
                      {ςγ,τγ} ∗
convertible if sγ ←−−−−→ tγ for every ground substitution γ that respects ψ.
                       R;H;E

     We will prove (in Theorem 4.21) that, if (E, ∅) ⊢∗ (∅, H), then every equation context in
E is R/H/E-bounded ground convertible. This result not only implies Theorem 3.4, but
will also be invaluable to use rewriting induction for ground confluence (Corollary 5.11).
                                                                    {a,b}        {a,b} ∗
     To start with the proof, we observe that both relations ←−−→ and ←−−−→ are symmetric.
                                                                    R;H;E        R;H;E
We will often use this property without explicitly stating it.
   We also immediately see that our relations are preserved under contexts:
Lemma 4.7. Let D be a context.
             {a,b}             {a,b}               {a,b} ∗            {a,b} ∗
   (1) If u ←−−→ v, then D[u] ←−−→ D[v]. (2) If u ←−−−→ v, then D[u] ←−−−→ D[v].
              R;H;E                  R;H;E                      R;H;E                      R;H;E

Proof. Obvious by definition of the relation: in each place where we use a context C[] we
can also use the context D[C[]] instead, without affecting the ordering requirements.
     Similarly, the relations are preserved under an increase of the bounding terms a, b:
Lemma 4.8. Suppose {c, d} ⪰mul {a, b}.
              {a,b}               {c,d}               {a,b} ∗               {c,d} ∗
     (1) If u ←−−→ v, then u ←−−→ v. (2) If u ←−−−→ v, then u ←−−−→ v.
              R;H;E               R;H;E               R;H;E                 R;H;E

Proof. The second statement follows immediately from the first. For the first, recall that
(≻mul , ⪰mul ) is an ordering pair; in particular, X ⪰mul Y ⪰mul Z implies X ⪰mul Z, and
X ⪰mul Y ≻mul Z implies X ≻mul Z. Hence, both cases (B) and (C) are preserved. If
                        BOUNDED REWRITING INDUCTION FOR LCSTRSs                               25



   {a,b}
u ←−−→ v by case (A), then there exists some e ∈ {{a, b}} such that e ⪰ ℓσ. By definition of
   R;H;E
⪰mul , there must be some f ∈ {{c, d}} such that f ≻ e or f ⪰ e; so either way, f ⪰ e ⪰ ℓσ
and f ⪰ ℓσ holds by transitivity. Similarly, some element g ∈ {{c, d}} exists with g ⪰ rσ.
       In the proof of Theorem 4.21, we will study derivation sequences (E1 , ∅) ⊢ (E2 , H2 ) ⊢
· · · ⊢ (∅, HN ), and show R/Hi /∅-bounded ground convertibility of all elements of any Ei
                                                                 {ςγ,τγ} ∗
(since H1 = ∅ this in particular implies our desired result sγ ←−−−−→ tγ for every equation
                                                                  R;∅;∅
context (ς ; s ≈ t ; τ) [ψ] ∈ E1 and every ground substitution γ that respects ψ). The most
difficult deduction rule in these proofs is (Induct). To present the proofs in a comprehensible
way, we will therefore first prove a property for every deduction rule other than (Induct).
Definition 4.9 (Base Soundness Property). We say a deduction rule has the Base Soundness
Property if, whenever we can deduce (E, H) ⊢ (E ′ , H′ ) by this rule and all equation contexts
in E are bounded, then H′ = H and for all (ς ; s ≈ t ; τ) [ψ] ∈ E \ E ′ , and for every ground
                                                {ςγ,τγ} ∗
substitution γ that respects ψ, we have: sγ ←−−−−→
                                                 ′
                                                   tγ.
                                                 R;H;E

    Now we can see that all rules other than (Induct) indeed have this property.
Lemma 4.10. (Simplify) has the Base Soundness Property.
Proof. We can write E = E0 ⊎ {(ς ; C[ℓδ] ≃ t ; τ) [ψ]} and E ′ = E0 ∪ {(ς ; C[rδ] ≈ t ; τ) [ψ]}
for some ℓ → r [φ] ∈ R ∪ Rcalc such that ψ |=δ φ.
     Let γ be a ground subsitution that respects ψ. Then we have:
              {ςγ,τγ}
▷ C[ℓδ]γ ←−−−−→
              ′
                C[rδ]γ by (A). This holds because:
         R;H;E
  – From ψ |=δ φ we know that γ respects φδ. Phrased differently, the composed substitution
    σ := δγ respects φ. Therefore, sγ = C[ℓδ]γ = Cγ[ℓσ] →R Cγ[rσ] = C[rδ]γ.
  – Since ς ⪰ s [ψ], and ⪰ includes ▷, we have ςγ ⪰ sγ ⪰ ℓσ.
  – Since →R is included in ⪰, it follows that ςγ ⪰ ℓσ ⪰ rσ as well.
              {ςγ,τγ}
▷ C[rδ]γ ←−−−−→
              ′
                tγ by (C), because {ςγ, τγ} ⪰mul {ςγ, τγ} by reflexivity.
              R;H;E
                                                    {ςγ,τγ} ∗
Hence, putting these steps together we have sγ ←−−−−→
                                                    ′
                                                      tγ.
                                                     R;H;E

Lemma 4.11. If R is weakly normalising and quasi-reductive, then (Case) has the Base
Soundness Property.
Proof. We can write E = E0 ⊎ {(ς ; s ≈ t ; τ) [ψ]} and E ′ = E0 ∪ {(ςδ ; sδ ≈ tδ ; τδ) [ψδ ∧ φ] |
(δ, φ) ∈ C} for C a cover set of s ≈ t [ψ]. Let γ be a ground substitution that respects
(ς ; s ≈ t ; τ) [ψ]. Since our rules are weakly normalising and quasi-reductive, every term
has a normal form, and every ground normal form must be a semi-constructor term. Let
γ ↓ be the substitution that maps each x to a normal form of γ(x). Since γ(x) maps all
variables in ψ to values, γ ↓ (x) = γ(x) on those variables, so also γ ↓ respects ψ. Thus we see:
      {ςγ,τγ} ∗
▷ sγ ←−−−−→
          ′
            sγ ↓ by 0 or more steps using (A), because:
           R;H;E
  – The assumption that (ς ; s ≈ t ; τ) [ψ] is a bounded equation context gives ςγ ⪰ sγ.
  – Writing sγ = u0 →R u1 →R . . . →R un , the inclusion of →R in ⪰ (along with
    transitivity of ⪰) ensures that ςγ ⪰ ui for all i.
26                                       K. HAGENS AND C. KOP




     – For 1 ≤ i ≤ n, writing ui−1 = C[ℓδ] and ui = C[rδ], we observe that ui−1 ⪰ ℓδ and
       ui ⪰ rδ because ▷ is included in ⪰.
          {ςγ,τγ}
▷ sγ ↓ ←−−−−→
            ′
              tγ ↓ by (C):
          R;H;E
     – By definition of cover set, there exist a pair (δ, φ) ∈ C and a substitution ϵ such that ϵ
       respects ψδ ∧ φ and γ ↓ = δϵ on all variables in dom(γ ↓ ). In particular, this means that
       sγ ↓ = sδϵ and tγ ↓ = tδϵ and ςγ ↓ = ςδϵ and τγ ↓ = τδϵ.
     – Hence, we can use the step with (ςδ ; sδ ≈ tδ ; τδ) [ψδ ∧ φ] ∈ E ′ .
     – We have {ςγ, τγ} ⪰mul {ςγ ↓ , τγ ↓ } = {ςδϵ, τδϵ} because by definition of a bounding pair
       (in particular the inclusion of →R in ⪰), ςγ ⪰ ςγ ↓ and τγ ⪰ τγ ↓ .
         {ςγ,τγ} ∗
▷ tγ ↓ ←−−−−→
            ′
              tγ by (A) by the same reasoning as the reduction from sγ to sγ ↓ .
          R;H;E

Lemma 4.12. (Delete) has the Base Soundness Property.
Proof. We can write E = E ′ ⊎{(ς ; s ≈ t ; τ) [ψ]}, where either s = t or ψ is unsatisfiable. Let
γ be a ground substitution that respects ψ. The existence of γ implies that ψ is satisfiable,
                                                 {ςγ,τγ} ∗
so necessarily s = t. But then clearly sγ ←−−−−→
                                               ′
                                                 tγ, using 0 steps.
                                                  R;H;E

Lemma 4.13. (Semi-constructor) has the Base Soundness Property.
Proof. We can write E = E0 ⊎ {(ς ; f s1 · · · sn ≈ f t1 · · · tn ; τ) [ψ]} and E ′ = E0 ∪ {(ς ; si ≈
ti ; τ) [ψ] | 1 ≤ i ≤ n} for f a variable or function symbol. Let γ be some ground substitution
that respects the equation context. Since {{ςγ, τγ}} ⪰mul {{ςγ, τγ}}, we use (C) to derive
                            {ςγ,τγ}                       {ςγ,τγ}        {ςγ,τγ}
         (f s1 s2 · · · sn )γ ←−−−−→
                                   ′
                                     (f t1 s2 · · · sn )γ ←−−−−→
                                                               ′
                                                                 . . . ←−−−−→
                                                                            ′
                                                                              (f t1 t2 · · · tn )γ
                             R;H;E                           R;H;E       R;H;E

using a context C[□] = f t1 · · · ti−1 □ si+1 · · · sn for the ith step. Together, this exactly
                           {ςγ,τγ} ∗
gives (f s1 s2 · · · sn )γ ←−−−−→
                                ′
                                  (f t1 t2 · · · tn )γ as required.
                            R;H;E

Lemma 4.14. (H-Delete) has the Base Soundness Property.
Proof. We can write E = E ′ ⊎ {(ς ; C[ℓδ] ≈ C[rδ] ; τ) [ψ]} for some ℓ ≃ r [φ] in H such
that ψ |=δ φ, and we have (a) ς ≻ ℓδ [ψ] or (b) τ ≻ rδ [ψ]. Let γ be a ground substitution
that respects the equation context. The above gives (a’) ςγ ≻ ℓδγ or (b’) τγ ≻ rδγ.
Since equation contexts in E are bounded, and ▷ is included in ⪰, we also know that (c)
ςγ ⪰ C[ℓδ]γ ⪰ ℓδγ and (d) τγ ⪰ C[rδ]γ ⪰ rδγ. Using (a’) with (d), or (b’) with (c), we have
                                                               {ςγ,τγ}
{{ςγ, τγ}} ≻mul {{ℓδγ, rδγ}}. So, C[ℓδ]γ = Cγ[ℓδγ] ←−−−−→
                                                        ′
                                                          Cγ[rδγ] = C[rδ]γ by (B).
                                                               R;H;E

Lemma 4.15. (Postulate) has the Base Soundness Property.
Proof. Since H = H′ and E \ E ′ = ∅ in the case of (Postulate), there is nothing to prove.
Lemma 4.16. (Hypothesis) has the Base Soundness Property.
Proof. We can write E = E0 ⊎ {(ς ; C[ℓδ] ≃ t ; τ) [ψ]} and E ′ = E0 ∪ {(ς ; C[rδ] ≈ t ; τ) [ψ]}
for some ℓ ≃ r [φ] in H such that ψ |=δ φ. Let γ be a ground substitution that respects the
equation context. Then from ς ≻ ℓδ [ψ] and ς ≻ rδ [ψ], we have ςγ ≻ ℓδγ and ςγ ≻ rδγ,
                                                                                                 {ςγ,τγ}
which together implies {{ςγ, τγ}} ≻mul {{ℓδγ, rδγ}}. Hence, C[ℓδ]γ = Cγ[ℓδγ] ←−−−−→
                                                                                  ′                  R;H;E
                                                                         {ςγ,τγ}
Cγ[rδγ] = C[rδ]γ by (B). Moreover, we clearly have C[rδ]γ ←−−−−→
                                                               ′
                                                                 tγ by (C).
                                                                         R;H;E
                          BOUNDED REWRITING INDUCTION FOR LCSTRSs                                     27




Lemma 4.17. If R is weakly normalising and quasi-reductive, then (Generalize) and (Alter)
have the Base Soundness Property.
Proof. In both cases, we have E = E0 ⊎{(ς ; s ≈ t ; τ) [ψ]} and E ′ = E0 ∪{(ς ′ ; s′ ≈ t′ ; τ′ ) [ψ ′ ]},
where the latter equation context generalizes the former. Let γ be a ground substitution that
respects (ς ; s ≈ t ; τ) [ψ]. As R is weakly normalizing we can define γ ↓ as a substitution
that maps each x to a normal form of γ(x); since R is quasi-reductive we know that γ ↓
is a gsc substitution. Hence, by definition of generalization, there is a substitution δ that
respects ψ ′ such that (a) ςγ ↓ ⪰ ς ′ δ, (b) τγ ↓ ⪰ τ′ δ, (c) sγ ↓ = s′ δ and (d) tγ ↓ = t′ δ.
                                {ςγ,τγ} ∗                {ςγ,τγ} ∗
▷ Clearly, we have both sγ ←−−−−→
                                ′
                                  sγ ↓ and tγ ↓ ←−−−−→
                                                     ′
                                                       tγ by (A): the facts that ςγ ⪰ sγ,
                                 R;H;E                    R;H;E
  τγ ⪰ tγ, and that both →R and ▷ are included in ⪰ ensure the ordering requirements.
▷ Since ⪰ includes →R , we know that ςγ ⪰ ςγ ↓ and τγ ⪰ τγ ↓ , so from (a) and (b) together
                                                                     {ςγ,τγ}
  we obtain {{ςγ, τγ}} ⪰mul {{ς ′ δ, τ′ δ}}. Hence, sγ ↓ = s′ δ ←−−−−→
                                                                     ′
                                                                       t′ δ = tγ ↓ by (C).
                                                                     R;H;E



4.4. Soundness of Bounded Rewriting Induction. Now, instead of proving Theorem 3.4
directly, we will obtain the following, more general property.
Theorem 4.18. Let L be a weakly normalizing, quasi-reductive LCSTRS; let (≻, ⪰) be a
bounding pair, and E1 a set of bounded equation contexts. Suppose (E1 , ∅) ⊢ (E2 , H2 ) ⊢ · · · ⊢
(EN , HN ), where each ⊢ is derived using either (Induct) or a derivation rule that has both
the Preserving Bounds and Base Soundness Properties. Consider some 1 ≤ i ≤ N . Then
every equation context in Ei is R/Hi /EN -bounded ground convertible (where H1 = ∅).
    Note that this result implies Theorem 3.4, but with the stronger property of bounded
ground convertibility rather than merely ground convertibility. Moreover, it easily allows us
to extend the system of Figure 1 with additional deduction rules, and maintain soundness of
the system so long as the new deduction rules satisfy two properties that are often easy to
prove (Preserving Bounds and the Base Soundness Property).
    The proof of Theorem 4.18 roughly proceeds by observing that for i = N , every equation
context in Ei is R/Hi /EN -bounded ground convertible, and then showing that if this property
holds for Ei with i > 0, then it also holds for Ei−1 . We first show the inductive step for the
deduction rules where H is unchanged; that is, all rules other than (Induct).
    To avoid excessive whitespace in the following three proofs (which use these relations a
                     {a,b}                                        {a,b}        {a,b}∗      {a,b} ∗
lot), we will use ↔R;H;E as an alternative notation for ←−−→ and ↔R;H;E for ←−−−→.
                                                                  R;H;E                    R;H;E

Lemma 4.19. Let (E, H) ⊢ (E ′ , H). Suppose that (a) for every (ς ; s ≈ t ; τ) [ψ] ∈ E \ E ′
                                                           {ςγ,τγ}∗
and ground substitution γ that respects it we have sγ ↔R;H;E ′ tγ; and (b) for every
                                                                                           {ςγ,τγ}∗
(ς ; s ≈ t ; τ) [ψ] ∈ E ′ and ground substitution γ that respects it we have sγ ↔R;H;EN tγ.
     Then for every (ς ; s ≈ t ; τ) [ψ] ∈ E and ground substitution γ that respects this
                                 {ςγ,τγ}∗
equation context we have sγ ↔R;H;EN tγ.
Proof. Let (ς ; s ≈ t ; τ) [ψ] ∈ E and γ a ground substitution that respects this equation
context ψ. To start, if (ς ; s ≈ t ; τ) [ψ] ∈ E ′ then we are done by assumption (b). Otherwise,
                                                         {ςγ,τγ}∗
(ς ; s ≈ t ; τ) [ψ] ∈ E \ E ′ . We will show that sγ ↔R;H;EN tγ.
28                                          K. HAGENS AND C. KOP




    By assumption (a), we may write sγ = c0 , tγ = ck , and there are c1 , . . . , ck−1 such that
    {ςγ,τγ}                                                                           {ςγ,τγ}∗
ci ↔R;H;E ′ ci+1 for 0 ≤ i < k. We are done if we can show that in fact ci ↔R;H;EN ci+1
                                                                                        {ςγ,τγ}
for all such i. To see that this is the case, consider the definition of ↔R;H;E ′ ; that is,
                                                                                            {ςγ,τγ}
Definition 4.5. If the step from ci to ci+1 is by (A) or (B), then this is also a ↔R;H;EN step,
so we are immediately done. Otherwise, it is by (C), so ci = C[s′ σ] and ci+1 = C[t′ σ] for
some (ς ′ ; s′ ≃ t′ ; τ′ ) [φ] ∈ E ′ such that σ respects φ and {{ςγ, τγ}} ⪰mul {{ς ′ σ, τ′ σ}}.
                                                  {ς ′ σ,τ′ σ}∗
    By assumption (b), we have that s′ σ ↔R;H;EN t′ σ. By Lemma 4.7, this also implies
                    {ς ′ σ,τ′ σ}∗
that ci = C[s′ σ] ↔R;H;EN           C[t′ σ] = ci+1 . Then, from {{ςγ, τγ}} ⪰mul {{ς ′ σ, τ′ σ}} we obtain
     {ςγ,τγ}∗
ci ↔R;H;EN ci+1 by Lemma 4.8, as required.
     Next, we obtain a lemma that will be very useful for when the (Induct) rule is used.
Lemma 4.20. Suppose ς ⪰ s [ψ] and τ ⪰ t [ψ], let H be a set of equations and H′ = H∪{s ≈
                {sγ,tγ}∗
t [ψ]}. Let sγ ↔R;H′ ;EN tγ hold for all ground substitutions γ that respect (ς ; s ≈ t ; τ) [ψ].
                                                                                          {ςγ,τγ}∗
     Then for all ground substitutions γ that respect (ς ; s ≈ t ; τ) [ψ]: sγ ↔R;H;EN tγ.
     (So using H instead of H′ , and ςγ, τγ instead of sγ, tγ.)
Proof. Let γ be a ground substitution that respects (ς ; s ≈ t ; τ) [ψ]. We prove the lemma
by induction on the multiset {sγ, tγ}, ordered with ≻mul .
            {sγ,tγ}∗
    Since ↔R;H′ ;EN denotes a transitive closure, we have a sequence c0 , c1 , . . . , ck such that
                                                     {sγ,tγ}
c0 = sγ and ck = tγ and for 0 ≤ i < k: ci ↔R;H′ ;EN ci+1 . Each step from ci to ci+1 that uses
                                         {sγ,tγ}                           {ςγ,τγ}
↔R or ↔H or ↔EN is also a ↔R;H;EN step, and therefore a ↔R;H;EN step by Lemma 4.8.
So, suppose the step from ci to ci+1 uses H′ \ H; that is, there exists a ground substitution δ
that respects s ≈ t [ψ], such that {{sγ, tγ}} ≻mul {{sδ, tδ}}, and such that either ci = C[sδ]
and ci+1 = C[tδ], or ci = C[tδ] and ci+1 = C[sδ]. Either way, by the induction hypothesis,
     {sδ,tδ}∗                                                 {ςγ,τγ}∗
sδ ↔R;H;EN tδ, and therefore by Lemmas 4.7 and 4.8, ci ↔R;H;EN ci+1 .
     With this, we have all the preparations needed to prove our primary soundness result
for bounded rewriting induction. We recall the theorem:
Theorem 4.18. Let L be a weakly normalizing, quasi-reductive LCSTRS; let (≻, ⪰) be
a bounding pair, and E1 a set of bounded equation contexts. Suppose (E1 , ∅) ⊢ (E2 , H2 ) ⊢
· · · ⊢ (EN , HN ), where each ⊢ is derived using either (Induct) or a derivation rule that has
both the Preserving Bounds and Base Soundness Properties. Consider some 1 ≤ i ≤ N .
Then every equation context in Ei is R/Hi /EN -bounded ground convertible (where H1 = ∅).

Proof. By definition of Preserving Bounds (Definition 4.1), and the fact that (Induct) also
preserves bounds (Lemma 4.2), we obtain by induction on i that (**) each Ei contains only
bounded equation contexts. Now, we will prove the required result by induction on N − i.
So assume given 1 ≤ i ≤ N , let (ς ; s ≈ t ; τ) [ψ] ∈ Ei , and let γ be a ground substitution
                                       {ςγ,τγ}∗
that respects ψ. We must show: sγ ↔R;Hi ;EN tγ.
                                                               {ςγ,τγ}
    If N − i = 0 this is obvious: we have sγ ↔R;Hi ;EN tγ by a single step using (C). If
N − i > 0, so 1 ≤ i < N , consider the deduction step (Ei , Hi ) ⊢ (Ei+1 , Hi+1 ). If this step has
the Base Soundness Property, then by (**), property (a) of Lemma 4.19 is satisfied, while
                                                                    {ςγ,τγ}∗
property (b) is satisfied by the induction hypothesis. Thus, sγ ↔R;Hi ;EN tγ. by Lemma 4.19.
                        BOUNDED REWRITING INDUCTION FOR LCSTRSs                                29




    The only remaining case is that the deduction step was performed by (Induct). That is,
Ei = E ⊎{(a ; u ≈ v ; b) [φ]} and Ei+1 = E ∪{(u ; u ≈ v ; v) [φ]} and Hi+1 = Hi ∪{u ≈ v [φ]}.
We distinguish two cases.
▷ (ς ; s ≈ t ; τ) [ψ] ∈ E. Then this equation context is in Ei+1 , so by induction hypothesis
                 {ςγ,τγ}∗
  we have sγ ↔R;Hi+1 ;EN tγ. That is, there exist c0 , . . . , ck with k ≥ 0 such that sγ = c0 ,
                                            {ςγ,τγ}                                 {ςγ,τγ}∗
  tγ = ck and for 0 ≤ j < k we have cj ↔R;Hi+1 ;EN cj+1 . It suffices if each cj ↔R;Hi ;EN cj+1
  as well. So fix j ∈ {0, . . . , k − 1}, and consider how the step from cj to cj+1 is produced.
  If the step from cj to cj+1 is by (A) (so using ↔R ) or (C) (so using ↔EN ), or if it is by
                                                                   {ςγ,τγ}
  (B) with an equation in Hi , then we immediately have cj ↔R;Hi ;EN cj+1 as well.
     The only alternative is a step by (B) using Hi+1 \ Hi = {u ≈ v [φ]}. That is, there
  exists a ground substitution σ that respects φ and for which {{ςγ, τγ}} ≻mul {{uσ, vσ}},
  such that either cj = C[uσ] and cj+1 = C[vσ], or cj = C[vσ] and cj+1 = C[uσ]. Now,
                                                                             {uδ,vδ}∗
  observe that for all ground substitutions δ that respect φ we have uδ ↔R;Hi+1 ;EN vδ by the
  induction hypothesis, because (u ; u ≈ v ; v) [φ] ∈ Ei+1 . Hence we may apply Lemma 4.20
                                                         {uδ,vδ}∗
  (with u ⪰ u [φ] and v ⪰ v [φ]) to obtain that uδ ↔R;Hi ;EN vδ. By Lemma 4.7, this implies
       {uδ,vδ}∗                                          {ςγ,τγ}∗
  cj ↔R;Hi ;EN cj+1 , and by Lemma 4.8 we have cj ↔R;Hi ;EN cj+1 as required.
▷ (ς ; s ≈ t ; τ) [ψ] ∈
                      / E, so Ei = E ⊎ {(ς ; s ≈ t ; τ) [ψ]} and Ei+1 = E ∪ {(s ; s ≈ t ; t) [ψ]}
  Then the conditions to apply Lemma 4.20 are satisfied:
  – by (**) and definition of a bounded equation context, we have ς ⪰ s [ψ] and τ ⪰ t [ψ]
  – Hi+1 = Hi ∪ {s ≈ t [ψ]}
                                                                  {sδ,tδ}∗
  – for all ground substitutions δ that respect ψ we have sδ ↔R;Hi+1 ;EN tδ by the induction
     hypothesis because (s ; s ≈ t ; t) [ψ] ∈ Ei+1
                                                 {ςγ,τγ}∗
  Hence, we immediately conclude that sγ ↔R;Hi ;EN tγ.

    With this, we can easily obtain a core soundness claim of bounded rewriting induction:
Theorem 4.21. Let L be a weakly normalizing, quasi-reductive LCSTRS and let E be a set
of bounded equation contexts. Let (≻, ⪰) be some bounding pair, such that (E, ∅) ⊢∗ (∅, H),
for some H using the derivation rules in Figure 1.
     Then for every equation context (ς ; s ≈ t ; τ) [ψ] ∈ E, and every ground substitution γ
                               {ςγ;τγ}                {ςγ;τγ}       {ςγ,τγ}
that respects ψ, we have: sγ ←−−−→∗ tγ, where u ←−−−→ v if u ←−−−−→ by (A).
                                 R                      R             R;∅;∅

Proof. By Lemmas 4.10, 4.11, 4.12, 4.13, 4.14, 4.15, 4.16 and 4.17, all derivation rules of
Figure 1 other than (Induct) have the Base Soundness Property. By Lemma 4.2 they also all
preserve bounds. Hence, we apply Theorem 4.18 and find that, choosing i = 1 (with E1 = E)
we conclude that every equation context in E is R/∅/∅-bounded ground convertible.
    We obtain the original soundness result as a corollary:
Theorem 3.4. Let L be a weakly normalizing, quasi-reductive LCSTRS; A a set of
equations; and let E be the set of equation contexts {(• ; s ≈ t ; •) [ψ] | s ≈ t [ψ] ∈ A}. Let
(≻, ⪰) be some bounding pair, such that (E, ∅) ⊢∗ (∅, H), for some H using the derivation
rules in Figure 1. Then every equation in A is an inductive theorem.

Proof. Clearly, equation contexts of the form (• ; s ≈ t ; •) [ψ] are bounded. Hence, the
result immediately follows by Theorem 4.21.
30                                    K. HAGENS AND C. KOP




4.5. Completeness. To prove Theorem 3.19, we start with a proposition.
Proposition 4.22. Let R be a quasi-reductive, ground confluent LCSTRS and let E be a
set of equations. If (E, H) ⊢ ⊥ then there are an equation context (ς ; s ≈ t ; τ) [ψ] ∈ E and
a ground substitution γ that respects (ς ; s ≈ t ; τ) [ψ] for which sγ ↔∗R tγ does not hold.
Proof. We first observe that, by definition of ground confluence, we have sγ ↔∗R tγ exactly if
sγ →∗R ← tγ, where we say u →∗R ← v if there exists w such that both u →∗R w and v →∗R w.
     The only derivation rule that allows us to deduce ⊥ is (Disprove), and by definition
of this rule, E contains an equation context (ς ; s ≈ t ; τ) [ψ] such that s ≈ t [ψ] is
contradictory. We consider all possibilities of being contradictory.
     (1): there exist f, g ∈ Σ with f ̸= g and a ground substitution γ that respects ψ such
that sγ = f s1 · · · sm and tγ = g t1 . . . tm with n < ar (f) and m < ar (g). Claim: γ is a
substitution for which sγ →∗R ← tγ does not hold (and therefore neither does sγ ↔∗R tγ).
To see this, assume that there exists u such that both sγ →∗R u and tγ →∗R u. By the
arity restriction, sγ cannot reduce at the root, and nor can any of its reducts. Therefore,
head (u) = f. Similarly, we conclude head (u) = g. This gives the desired contradiction.
     (2): s, t ∈ T (Σtheory , V) and there is a ground substitution γ that respects ψ, with
[[(ψ ∧ s ̸= t)γ]] = ⊤. Hence, γ maps every variable in V ar(s) ∪ V ar(t) to a ground theory
term. Using only →Rcalc we reduce sγ and tγ to their normal forms (which must be
values). We have [[sγ]] ̸= [[tγ]], and since calculation rules preserve interpretation, this implies
[[(sγ) ↓]] ̸= [[(tγ) ↓]]. But then also (sγ) ↓̸= (tγ) ↓, as there is a one-to-one correspondence
between values and their interpretations. Hence, sγ →∗R ← tγ does not hold.
    Proposition 4.22 only proves the desired statement for a single-step deduction. To obtain
the full statement of Theorem 3.19, we will use an inductive reasoning.
Theorem 3.19. Let L be a weakly normalizing, quasi-reductive, ground confluent LCSTRS
and let E be a set of equations. If (E, ∅) ⊢∗ ⊥ then there is an equation in E which is not an
inductive theorem.
Proof. Assume given a (bounded or general) RI deduction
                              (E1 , H1 ) ⊢ (E2 , H2 ) ⊢∗ (En , Hn ) ⊢ ⊥
With H1 = ∅. Towards a contradiction, assume that all equations in E1 are inductive
theorems; that is, that ↔E1 ⊆ ↔∗R on ground terms. We show that this assumption
implies that ↔Ei ∪ ↔Hi ⊆ ↔∗R on ground terms for all 1 ≤ i ≤ n, by induction on i (the
contradiction then follows by considering i = n and Proposition 4.22).
     For i = 1 this is true by assumption (since H1 = ∅). So let i > 1.
     If the step (Ei−1 , Hi−1 ) ⊢ (Ei , Hi ) uses a deduction rule with the Completeness Property,
then from the induction hypothesis we immediately obtain ↔Ei ∪ ↔Hi ⊆ ↔∗R on ground
terms. So assume that this step does not use such a deduction rule.
     First, let s ≈ t [ψ] ∈ Hi and γ be a ground substitution that respects ψ. If s ≈ t [ψ] ∈
Hi−1 then sγ ↔∗R tγ by the induction hypothesis. Otherwise, note that the only deduction
rule that adds elements to the set of induction hypotheses is (Induct); as such, there is some
(ς ; s ≈ t ; τ) [ψ] ∈ Ei−1 , and therefore we also have sγ ↔∗R tγ by the induction hypothesis.
Hence, either way, ↔Hi ⊆ ↔∗R on ground terms.
     Next, we consider Ei . Observe that En is necessarily a complete proof state, otherwise
the (Disprove) rule could not have been used on it. So, there exists j ≥ i such that (Ej , Hj )
is complete; let N be the smallest such j. Then (EN −1 , HN −1 ) ⊢ (EN , HN ) cannot have been
                            BOUNDED REWRITING INDUCTION FOR LCSTRSs                                           31




derived using case (b) of Definition 3.17 (since either i = N in which case the preceding step
does not satisfy the Completeness Property, or i < N in which case the preceding proof
state is not complete), nor using (a) (since N ≥ i > 1), so there must exist some k < N
such that (Ek , Hk ) is complete, and EN ⊆ Ek . Since we chose the smallest possible N , we
have k < i, and therefore ↔EN ⊆ ↔Ek ⊆ ↔∗R by the induction hypothesis.
    Let (ς ; s ≈ t ; τ) [ψ] ∈ Ei and γ a ground substitution that respects ψ. Then we
                                                     {ςγ,τγ} ∗
observe that by Theorem 4.18 we have sγ ←−−−−→ tγ, and since we have already seen that
                                                     R;Hi ;EN
both ↔Hi and ↔EN are included in ↔∗R , we conclude sγ ↔∗R tγ as required.
    Note that this proof only uses that derivation rules other than (Induct) and (Disprove)
don’t change H. Hence, like Theorem 4.18, the result is applicable to extensions of Figure 1.

                                       5. Ground Confluence
We now turn our eye to ground confluence. This property is both necessary to deduce that
an equation is not an inductive theorem using rewriting induction (using subsection 3.3),
and interesting to study in its own right – since, in a terminating and ground confluent
system, reduction essentially computes a unique result for every ground term. In [AT16], it
is illustrated that (traditional) rewriting induction can be used as a tool to prove ground
confluence of a terminating TRS. We will see now that the same holds for bounded RI.

5.1. Critical pairs. Critical pairs are a standard tool for proving confluence. They have
also been defined for first-order LCTRSs [SM23]. This definition relies on the notion of
positions, which we here adapt to our (higher-order) definition of terms:
Definition 5.1. For a term t S           = a t1 · · · tn with
                                                         S a ∈ Σ ∪ V and n ≥ 0, the set of positions
Pos(t) is defined as Pos(t) = ( ni=0 {⋆i}) ∪ ( ni=1 {i · p | p ∈ Pos(ti )}).
     Define the subterm t|p of t at position p ∈ Pos(t) as follows:
▷ (a t1 · · · tn )|⋆i = (a t1 · · · tn−i )
▷ (a t1 · · · tn )|i·p = ti |p
If t is a term, p ∈ Pos(t), and s a term of the same type as t|p , then let t[s]p be the term
obtained from t by replacing t|p by s. We will denote the position ⋆0 as ϵ.
     Definition 5.1 differs from the definition for first-order rewriting by including positions
for partial applications; in first-order terms, we only have positions of the form i1 · · · in ⋆ 0.1
     With this preparation, we recall the first-order definition of critical pairs from [SM23]:
Definition 5.2 (Critical pairs). An overlap in an LCTRS R is a triple ⟨ρ1 , p, ρ2 ⟩ with rules
ρ1 := ℓ1 → r1 [φ1 ] and ρ2 := ℓ2 → r2 [φ2 ] and position p, satisfying
▷ ρ1 and ρ2 are variable-disjoint renamings of rewrite rules in R ∪ Rcalc
▷ p ∈ Pos(ℓ2 ) with ℓ2 |p not a variable
▷ σ = mgu(ℓ1 , ℓ2 |p ) and σ(V ar(φ1 ) ∪ V ar(φ2 )) ⊆ Val ∪ V
▷ φ1 σ ∧ φ2 σ is satisfiable
▷ If p = ϵ and ρ1 and ρ2 are renamings of the same rule, then V ar(r1 ) \ V ar(ℓ1 ) ̸= ∅.
   1This definition also differs from the usual presentation of positions in higher-order rewriting, which does
not use the ⋆ notation but rather sets (s t)|1p = s|p and (s t)2p = t|p . This difference is not significant; the
presentation above is chosen for human reasons: in practice (and in our tool) it is convenient if the positions
used for first-order rewriting refer to the same subterm when viewing the term as higher-order.
32                                    K. HAGENS AND C. KOP




The critical pair of ⟨ρ1 , p, ρ2 ⟩ is the equation
                                    ℓ2 [r1 ]p σ ≈ r2 σ [φ1 σ ∧ φ2 σ]
     The “overlap” here refers to the fact that ℓ2 has a subterm that unifies with ℓ1 . In
particular, ℓ2 σ can be reduced in two ways: if σ respects φ1 ∧φ2 then, as ℓ2 σ = (ℓ2 σ)[ℓ2 |p σ]p =
(ℓ2 σ)[ℓ1 σ]p , we apply ρ1 to obtain ℓ2 σ →R (ℓ2 σ)[r1 σ]p . Of course, we also have ℓ2 σ →R r2 σ.
Example 5.3. Let us apply Definition 5.2 to Example 3.14. We have the following variable-
disjoint copies of H-rules, which are not renamings of each other
                      ρ1 := H f n m x → H f (n − 1) m (f x) [n > 0]
                         ρ2 := H g i j y → H g (j − 1) i (g y)           [j > 0]
There is an overlap ⟨ρ1 , ϵ, ρ2 ⟩ with σ = [g := f, i := n, j := m, y := x]. This yields
          CP(R) = {H f (n − 1) m (f x) ≈ H f (m − 1) n (f x) [n > 0 ∧ m > 0]}
     While this definition was designed for LCTRSs – so first-order systems where variables
cannot be applied, and partially applied function symbols do not occur – our updated
definition of positions allows the definition to be used unaltered for (higher-order) LCSTRSs!
Example 5.4. Consider an LCSTRS containing the following variable-disjoint rules
                             ρ1 := f → g             ρ2 := u (f x) → h x
We have an overlap (ρ1 , 1 ⋆ 1, ρ2 ) with σ the empty substitution. This yields the critical pair
u (g x) ≈ h x, because ℓ2 σ = u (f x) reduces to both sides.
     As it turns out, it is useful to also preserve the source ℓ2 σ. We do so using critical peaks:
Definition 5.5 (Critical peaks). The critical peak of an overlap ⟨ρ1 , p, ρ2 ⟩ is the tuple
                               ℓ2 [r1 ]p σ ← ℓ2 σ → r2 σ [φ1 σ ∧ φ2 σ]
The set of all critical peaks in an LCSTRSs is denoted by CP(R).
Example 5.6. Following Example 5.3, we have ℓ2 σ = H f n m x, so the corresponding
critical peak is given by:
        H f (n − 1) m (f x) ← H f n m x → H f (m − 1) n (f x) [n > 0 ∧ m > 0]
     In Example 5.4 we obtain a critical peak:
                                 u (g x) ← u (f x) → h x [true]
     Critical pairs rely on positions, which we have otherwise not used in our definitions. To
relate these to our notion of reduction, we use the following helper result:
Lemma 5.7. Let γ be a substitution, X a finite set of variables, and s, t ∈ T (Σ, V) such
that sγ →R t and X ⊇ V ar(s). Then one of the following holds.
   (i). There exist a substitution δ, variable-renamed rule ℓ → r [φ] ∈ R∪Rcalc with variables
        disjoint from X, and p ∈ Pos(s) such that δ(x) = γ(x) for all x ∈ X, δ respects φ,
        s|p ∈
            / V, s|p δ = ℓδ and t = s[r]p δ.
  (ii). There exist x ∈ V ar(s) and substitution γ ′ such that γ(x) →R γ ′ (x), and γ ′ (y) = γ(y)
        for all other y and t →∗R sγ ′ .
Proof. Assume sγ →R t. By induction on the term shape of s we prove that either (i) or
(ii) holds. Any s ∈ T (Σ, V) can be written as s = a s1 · · · sn with a ∈ Σ ∪ V and n ≥ 0.
                             BOUNDED REWRITING INDUCTION FOR LCSTRSs                                               33




▷ Base case 1: a ∈ V and γ(a) →R u and t = u (s1 γ) · · · (sn γ). Define γ ′ as follows:
                             γ ′ (a) = u                 γ ′ (y) = γ(y) if y ̸= a
  Then clearly t = u (s1 γ) · · · (sn γ) →∗R u (s1 γ ′ ) · · · (sn γ ′ ) = sγ ′ ; thus, (ii) holds.
▷ Base case 2: sγ = (ℓσ) (si+1 γ) · · · (sn γ) →R (rσ) (si+1 γ) · · · (sn γ) = t for some i ∈
  {0, . . . , n}, and some σ which respects some ℓ → r [φ] ∈ R ∪ Rcalc . If i = 0 and a is a
  variable we are in the first case and are done. Otherwise, let p = ⋆(n − i). As we can
  safely assume (by renaming) that the variables in ℓ → r [φ] do not occur in X, we can
  define δ(x) = γ(x) for x ∈ X and δ(x) = σ(x) for all other x. Then (i) holds.
▷ Induction case: there is some 1 ≤ i ≤ n with si γ →R ti and t = (aγ) (s1 γ) · · · ti · · · (sn γ).
  By the induction hypothesis there are two possibilities
     (i). There exist δ, ℓ → r [φ] and pi ∈ Pos(si ) such that δ respects φ, δ(x) = γ(x) for all
            x ∈ X (and therefore sγ = sδ), si |pi ∈             / V, si |pi δ = ℓδ and ti = si [r]pi δ. Let p = i pi .
            Then (i) also holds for sγ →R t, since s|p = si |pi , and t = (aγ) (s1 γ) · · · ti · · · (sn γ) =
            (aδ) (s1 δ) · · · (si [r]pi δ) · · · (sn δ) = s[r]p σ.
    (ii). There exist x ∈ V ar(si ) and substitution γ ′ such that γ(x) →R γ ′ (x), γ ′ (y) =
            γ(y) for all y ∈ dom(γ) \ {x} and ti →∗R si γ ′ . We have sj γ →∗R sj γ ′ for all
            j ̸= i. Conclude t = (aγ) (s1 γ) · · · ti · · · (sn γ) →∗R (aγ) (s1 γ) · · · (si γ ′ ) · · · (sn γ) →∗R
            (aγ ′ ) (s1 γ ′ ) · · · ti · · · (sn γ ′ ) = sγ ′ .
   In analogy to the Critical Pair Lemma [BN98, Lemma 6.2.3] we introduce the Critical
Peak Lemma.
Lemma 5.8 (Critical Peak Lemma). If s →R ti , i = 1, 2, then either
                                                     ∗         ∗
   (i). There exists a term t such that t1 −
                                           →t←
                                             − t2 .
                                                     R      R
  (ii). There exist a critical peak b ← a → c [φ], context C and substitution δ that respects φ
        such that s = C[aδ], t1 = C[bδ] and t2 = C[cδ].
Proof. By induction on the term-shape of s we prove that either (i) or (ii) holds. Any
s ∈ T (Σ, V) can be written as s = f s1 · · · sn with f ∈ Σ ∪ V and n ≥ 0. We consider all
                       R      R
possibilities of t1 ←
                    −s−  → t2 .
(1). There exist 1 ≤ i, j ≤ n and terms vi , wj such that si →R vi , sj →R wj and
                                    t1 = s[vi ]i         and       t2 = s[wj ]j
     • If i =
            ̸ j then the reductions are in parallel positions; (i) holds with t = t1 [wj ]j = t2 [vi ]i .
                              R      R
     • If i = j then vi ←
                        − si −
                             → wi . By induction hypothesis we either have
                                         ∗     ∗
       – There is a term t′ such that vi −
                                         → t′ ←
                                              − wi . Then (i) holds: take t = s[t′ ]i .
                                                    R       R
       – There exist a critical peak a ← b → c [φ], context C ′ and substitution δ that
         respects φ such that si = C ′ [bδ], vi = C ′ [aδ] and wi = C ′ [cδ]. Then (ii) holds: take
         C[□] = s[C ′ [□]]i = f s1 · · · si−1 C[□] si+1 · · · sn , and p = i pi .
(2). One of the reductions is at the head; without loss of generality, we assume it is the step
     s →R t1 . That is, there exist a rule ρ1 := ℓ → r [φ] ∈ R ∪ Rcalc with ℓ = f v1 · · · vk and
     a substitution γ which respects φ, and ⃗s = sk+1 · · · sn such that k = ar (f) ≤ n and
                             s = (ℓγ)⃗s = f (v1 γ) · · · (vk γ) ⃗s →R (rγ)⃗s = t1
     We consider the possibilities for s →R t2
     • si →R s′ , for some i > k, and t2 = s[s′ ]i . Then (i) holds, as we can see by choosing
       t = (rγ) s1 · · · si−1 s′ si+1 · · · sn .
34                                          K. HAGENS AND C. KOP




     • si = vi γ →R s′ , with 1 ≤ i ≤ k, and t2 = s[s′ ]i . By Lemma 5.7, applied with
       X = V ar(ℓ) ∪ V ar(r) ∪ V ar(φ) ⊇ V ar(vi ), there are two possibilities
       – si = vi γ = vi δ for some δ that respects a renamed rule ρ2 := ℓ′ → r′ [φ′ ] with
          ℓ′ = g l1′ · · · lm
                            ′ and there is a p′ ∈ Pos(v ) such that v | ′ ∈
                                                               i
                                                                                                      ′        ′
                                                                                 i p / V, vi |p′ δ = ℓ δ and s =
               ′
          vi [r ]p′ δ; moreover, δ(x) = γ(x) on all x ∈ X. Then t2 = f (v1 γ) · · · (vi−1 γ) vi [r ]p′ δ     ′

         (vi+1 γ) · · · (vk γ) ⃗s = (f v1 · · · vi−1 vi [r′ ]p′ vi+1 · · · vk )δ ⃗s and (ii) holds: let C = □ ⃗s
          and p = i p′ . We have
                                                             s = C[ℓδ]

                                                        R                   R
                                    t2 = C[ℓ[r′ ]p δ]               t1 = C[rδ]
                                                    ′
          Since δ is a unifier of ℓ|p = vi |p′ and ℓ , there exist a most general unifier σ and a
         substitution χ so that δ = σχ. Since δ respects both φ (because it corresponds with
         γ on X ⊇ V ar(φ)) and φ′ , clearly (φ′ ∧ φ)σ is satisfiable (by the substitution χ).
         Hence, the figure above is an instance of the critical peak ℓ[r′ ]p σ ← ℓσ → rσ [φ′ ∧φ].
       – There exist x ∈ V ar(vi ) and substitution γ ′ such that γ(x) →R γ ′ (x), γ ′ (y) = γ(y)
         for all y ̸= x and s′ →∗R vi γ ′ . Then (i) holds: choosing t = (rγ ′ )⃗s we have:
                                        s = (ℓγ)⃗s
                                R                                R


                  t1 = (rγ)⃗s                           t2 = (ℓγ)[s′ ]i⃗s = f (v1 γ) · · · s′ · · · (vn γ) ⃗s
                                                                                     R ∗
                                    ∗
                                R
                                                            (ℓγ ′ )⃗s = f (v1 γ ′ ) · · · (vi γ ′ ) · · · (vn γ ′ ) ⃗s

                                                                 R
                                t = (rγ ′ )⃗s
     • The other reduction is also at the head; since each function symbol has a fixed arity,
       this means there exist a rule ρ2 := ℓ′ → r′ [φ′ ] with ℓ′ = f v1′ · · · vk′ and substitution γ ′
       which respects φ′ such that s = (ℓ′ γ ′ ) ⃗s and t2 = (r′ γ ′ ) ⃗s. If rγ = r′ γ ′ then (i) holds,
       choosing t = t1 = t2 . Otherwise, (ii) holds with C[□] = □ ⃗s: by renaming variables
       we can safely assume that dom(γ) ∩ dom(γ ′ ) = ∅, so δ = γ ∪ γ ′ is well-defined. Then
                                                      s = C[ℓ′ δ]

                                             R            R
                                     ′
                     t1 = C[rδ] = C[ℓ [r]ϵ δ]                 t2 = C[r′ δ]
       Let σ be an mgu between ℓ and ℓ′ , and χ such that δ = σχ. Then the figure above
       corresponds to the critical peak rσ ← ℓ′ σ → r′ σ [φσ ∧ φ′ σ]. (If ρ1 and ρ2 are
       renamings of the same rule, then ℓσ = ℓ′ σ implies rσ = r′ σ unless V ar(r) ⊆ V ar(ℓ)
       does not hold, so the last requirement of an overlap is also satisfied.)
     The critical peak lemma is valuable both for proving (local) confluence and ground
(local) confluence. In this paper, we focus on ground confluence. The following lemma gives
a way to prove this property:
Lemma 5.9. Assume given an LCSTRS L = (Σ, R) which is not ground locally confluent,
and let (≻, ⪰) be a bounding pair on T (Σ, ∅). Then
                         BOUNDED REWRITING INDUCTION FOR LCSTRSs                                                     35




  (i). There is a ≻-minimal ground term s for which there exist terms t1 , t2 with t1 ←
                                                                                      −s−
                                                                                        → t2
                                                                                                             R   R
                                                ∗           ∗
      but such that there is no t with t1 −
                                          →t←
                                            − t2 .
                                               R            R
        Moreover, there exist a critical peak v1 ← u → v2 [φ] and ground substitution γ that
        respects φ such that s = uγ, t1 = v1 γ and t2 = v2 γ.
  (ii). If in addition →R is terminating, then for all ground terms r with s ≻ r or s →+R r:
                                      ∗  ∗                                        ∗   ∗
        if there are q1 , q2 with q1 ←
                                     −r− → q2 then there is a term q such that q1 −
                                                                                  →q← − q2 .
                                  R        R                                                             R       R

Proof. If →R is terminating, let ⊐ be the relation with a ⊐ b if a ≻ b or a →+
                                                                             R ⊵b or a ▷ b.
If →R is not terminating, then let ⊐ be the relation with a ⊐ b if a ≻ b or a ▷ b. Either
way, this relation is well-founded, because a →R b and a ▷ b both imply a ⪰ b, and if →R is
terminating then so is the union of →+  R ⊵ and ▷.
   (i). By definition of not being ground locally confluent: there are ground terms s, t1 , t2
                                                                  ∗    ∗
        with t1 ←−s−  → t2 , for which there is no t such that t1 −
                                                                  →t←  − t2 . Hence, we can
               R     R                                                                           R   R
       take s to be a term with this property that is minimal with respect to ⊐.
         By Lemma 5.8 there exist a critical peak v1 ← u → v2 [φ], context C and
       substitution γ that respects φ such that s = C[uγ], t1 = C[v1 γ] and t2 = C[v2 γ].
       Since uγ is ground – and therefore its reducts v1 γ and v2 γ as well – necessarily γ is
       ground on V ar(u, v1 , v2 ); we can safely assume that γ is ground overall. Furthermore,
       we must have C = □ because otherwise s ⊐ uγ, contradicting minimality of s.
                                                                                     ∗    ∗
 (ii). Assume →R is terminating. Let r, q1 , q2 be ground terms with s ⊐ r and q1 ←  −r−  → q2 .
                                                                                                         R       R
                                                                        ∗           ∗
      We show that there is a term q such that q1 − − q2 , using induction on →+
                                                  →q←                          R.
                                                                        R           R
         If q1 = r or q2 = r then there is nothing to prove, so we might assume there are
                                   ∗                 ∗
      terms w1 , w2 such that q1 ← − w1 ← −r− → w2 − → q2 . Since s ⊐ r and s is a minimal
                                   R           R        R               R
                                                                ∗               ∗
      term, there exists a term w such that w1 −
                                               →w←
                                                 − w2 .
                                                                R           R
                         ∗    ∗
         But then q1 ←
                     − w1 −
                          → w and s ⊐ w1 (because →R ⊆ ⪰), so by induction hypothesis
                      R      R
                                       ∗        ∗
      there is a term a such that q1 −
                                     →a←
                                       − w. In a similar way, we can apply the induction
                                       R        R
                                                                ∗           ∗
      hypothesis to find a term b such that w −
                                              →b←
                                                − q2 . We complete the proof like in
                                                   R            R
      the diagram below: since both r →∗R a and r →∗R b, one additional application of the
      induction hypothesis will give us the term q.
                                                r

                                                        R           R
                                               w1                           w2
                                       ∗                ∗           ∗                   ∗
                                           R        R                   R           R
                                  q1                        w                               q2
                                           ∗        ∗                   ∗           ∗
                                       R                R           R                   R
                                               a                            b
                                                        ∗           ∗
                                                    R                   R
                                                                q
36                                     K. HAGENS AND C. KOP




5.2. RI for ground confluence. A first-order unconstrained term rewriting system is
ground confluent when all its critical pairs are bounded ground convertible [AT16]. We
can use rewriting induction as a method to prove bounded ground convertibility. We will
generalize this result to LCSTRSs with bounded rewriting induction.
    Analogously to the Critical Pair Theorem [BN98, Theorem 6.2.4] we introduce the
Ground Critical Peak Theorem.
Theorem 5.10 (Ground Critical Peak Theorem). Let R be a terminating LCSTRS and
let (≻, ⪰) be a bounding pair. Then R is ground confluent if for all its critical peaks
v1 ← u → v2 [φ], the equation context (u ; v1 ≈ v2 ; u) [φ] is R/∅/∅-bounded ground
convertible using (≻, ⪰).
    In Theorem 4.21 we showed that bounded rewriting induction proves R/∅/∅-bounded
ground convertibility. Therefore, we conclude the following result:
Corollary 5.11 (Bounded RI for ground confluence). Let R be a terminating, quasi-reductive
LCSTRS, (≻, ⪰) a bounding pair, and E the set {(u ; v1 ≈ v2 ; u) [φ] | v1 ← u → v2 [φ] ∈
CP(R)}. If (E, ∅) ⊢∗ (∅, H) for some set H, then R is ground confluent.
Example 5.12. In the LCSTRS from Example 3.14 we have CP(R) = {H f (n−1) m (f x) ←
H f n m x → H f (m − 1) n (f x) [n > 0 ∧ m > 0]}. For E = {(H f n m x ; H f (n −
1) m (f x) ≈ H f (m − 1) n (f x) ; H f n m x) [n > 0 ∧ m > 0]}, it is easy to show that
(E, ∅) ⊢∗ (∅, H) for some set H. By Corollary 5.11 R is ground confluent.
     Towards a proof of Theorem 5.10 we introduce two lemmas.
Lemma 5.13. Assume C1 [a1 ] = C2 [a2 ]. Then at least one of the following cases holds
   (i). C1 [□] = D[□, a2 ] and C2 = D[a1 , □] for some context D[□, □]
  (ii). a1 = D[a2 ] for some context D[□]
 (iii). a2 = D[a1 ] for some context D[□]
Proof. By induction on the shape of C1 . Any term can be written as f s1 · · · sn with
f ∈ Σ ∪ V and n ≥ 0. Therefore, any context C[□] has one of the following shapes
(A). C[□] = □ si+1 · · · sn , for some 1 ≤ i ≤ n
(B). C[□] = f s1 · · · si−1 C ′ [□] si+1 · · · sn , for some 1 ≤ i ≤ n and context C ′
Now, assume C1 [a1 ] = C2 [a2 ]. We consider the four combinations for C1 [□], C2 [□]
(AA): C1 [□] = □ si+1 · · · sn and C2 [□] = □ sj+1 · · · sn
      ▷ If i = j then C1 = C2 and a1 = a2 = f s1 · · · sn . In particular (ii) holds with D = □.
      ▷ If i > j then a1 = f s1 · · · sj · · · si and a2 = f s1 · · · sj . Then (ii) holds with
        D[□] = □ sj+1 · · · si (then a1 = D[a2 ]).
      ▷ Similarly, if i < j then (iii) holds by a symmetrical reasoning.
(AB): C1 [□] = □ si+1 · · · sn and C2 [□] = f s1 · · · sj−1 C ′ [□] sj+1 · · · sn . In particular
      a1 = f s1 · · · si and C ′ [a2 ] = sj .
      ▷ If i ≥ j then (ii) holds: a1 = D[a2 ] with D[□] = f s1 · · · sj−1 C ′ [□] sj+1 · · · si .
      ▷ If j > i then (i) holds: D[□1 , □2 ] = □1 si+1 · · · sj−1 C ′ [□2 ] sj+1 · · · sn .
(BA): Symmetrical to (AB).
(BB): C1 [□] = f s1 · · · si−1 C1′ [□] si+1 · · · sn and C2 [□] = f s1 · · · sj−1 C2′ [□] sj+1 · · · sn .
      In particular C1′ [a1 ] = si and C2′ [a2 ] = sj .
      ▷ If i = j then C1′ [a1 ] = C2′ [a2 ] and we apply the induction hypothesis; in case
        (ii) and (iii) we are done, and if the induction hypothesis gives us D′ we let
        D[□1 , □2 ] = f s1 · · · si−1 D′ [□1 , □2 ] si+1 · · · sn .
                             BOUNDED REWRITING INDUCTION FOR LCSTRSs                                    37




      ▷ If j > i then (i) holds, choosing D[□1 , □2 ] = f s1 · · · si−1 C1′ [□1 ] si+1 · · · sj−1 C2′ [□2 ]
        sj+1 · · · sn . Similarly, if i > j we have (i) by taking D[□1 , □2 ] = f s1 · · · sj−1 C2′ [□2 ]
        sj+1 · · · si−1 C1′ [□1 ] si+1 · · · sn .
                                   s≻∗
   In the following, let u −−→R v if we can write u = C[a], v = C[b], s ≻ a, s ≻ b, and
   ∗           s≻∗          s≻∗              s≻∗                s≻∗           s≻∗
a →R b. Let u ←−−R v if v −−→R u. We use u ←−→R v if either u −−→R v or u ←−−R v.
Lemma 5.14. Let R be a terminating, non-ground locally confluent LCSTRS and (≻, ⪰)
                                                                                  s≻∗
a bounding pair. Let s be the ≻-minimal term that exists by Lemma 5.9. Suppose v ←−−R
   s≻∗                                         s≻∗       s≻∗
u −−→R w. Then there is a term u′ such that v −−→R v ′ ←−−R w.
Proof. There are contexts C1 , C2 and terms a1 , a2 , b1 , b2 such that
▷ u = C1 [a1 ] = C2 [a2 ], v = C1 [b1 ] and w = C2 [b2 ]
▷ a1 →∗R b1 , a2 →∗R b2
▷ s ≻ a1 , s ≻ b1 , s ≻ a2 , s ≻ b2 .
By Lemma 5.13 there are three options:
  (i). C1 [□] = D[□, a2 ] and C2 = D[a1 , □] for some context D[□, □]: then
                                           s≻∗                     s≻∗
                       D[b1 , a2 ] = v ←−−R u = D[a1 , a2 ] −−→R w = D[a1 , b2 ]
        We can take u′ = D[b1 , b2 ]. We have s ≻ b1 and s ≻ b2 , as required.
  (ii). a1 = D[a2 ] for some context D[□]: then
                                 s≻∗                                     s≻∗
                   C1 [b1 ] = v ←−−R u = C1 [a1 ] = C1 [D[a2 ]] −−→R w = C1 [D[b2 ]]
                                                 +         +
       Since s ≻ a1 = D[a2 ] and b1 ←
                                    − D[a2 ] −
                                             → D[b2 ] we apply part (ii) of Lemma 5.9
                                                 R         R
                                                       ∗       ∗
       to obtain a term t such that b1 −   − D[b2 ]. Now, let u′ = C1 [t]. Then
                                       → t ←
                                                       R       R
                       s≻∗                       s≻∗
        v = C1 [b1 ] −−→R u′ = C1 [w] ←−−R C1 [D[b2 ]] = w. We will check the necessary
        inequalities. By assumption s ≻ b1 , and from b1 →∗R w (and →R ⊆ ⪰) s ≻ w follows.
        Also by assumption s ≻ a1 = D[a2 ] and from D[a2 ] →∗R D[b2 ], s ≻ D[b2 ] follows.
 (iii). a2 = D[a1 ] for some context D[□]: similar to (ii).
    With this, we are ready to prove the Ground Critical Peak Theorem:
Proof of Theorem 5.10. In a terminating system, ground confluence is implied by ground
local confluence. So, towards a contradiction, assume all equation contexts corresponding to
critical pairs are bounded ground convertible but that L is not ground locally confluent.
     By Lemma 5.9.(i) there is a ≻-minimal ground term s for which there are terms t1 , t2
                                                   ∗     ∗
such that t1 ← −s−  → t2 but there is no t with t1 −
                                                   →t←   − t2 . There are also a critical peak
               R       R                                       R     R
v1 ← u → v2 [φ] and ground substitution γ that respects φ such that s = uγ, t1 = v1 γ and
t2 = v2 γ. By assumption, (u ; v1 ≈ v2 ; u) [φ] is R/∅/∅-bounded ground convertible. This
                     {uγ,uγ} ∗
implies that v1 γ ←−−−−−→ v2 γ, so there exist c0 , . . . , ck such that v1 γ = c0 and v2 γ = ck , and
                       R;∅;∅
         {uγ,uγ}
each ci ←−−−−→ ci+1 . Since only case (A) of the definition can be used (and s = uγ, t1 = v1 γ
          R;∅;∅
                                                                                            s≻∗
and t2 = v2 γ), we can conclude that c0 = t1 and ck = t2 and (∀0 ≤ i < k): ci ←−→R ci+1 .
    To obtain the contradiction, we show that if the properties above are satisfied, then
                          ∗    ∗
there is a z such that t1 −
                          →z←  − t2 . We do so, using induction on k.
                               R       R
38                                    K. HAGENS AND C. KOP




▷ k = 0. Then t1 = t2 and we can choose z := t1 .
▷ k = 1. Then t1 →∗R t2 or t2 →+R t1 , so it trivially holds.
▷ k ≥ 2. We distinguish the following cases:
                s≻∗
  – If t1 = c0 −−→R c1 then the IH provides z such that t1 →∗R c1 →∗R z and t2 →∗R z.
             s≻∗
  – If ck−1 ←−−R ck = t2 then the IH provides z such that t1 →∗R z and t2 →∗R ck−1 →∗R z.
                                                  s≻∗        s≻∗       s≻∗          s≻∗
  – Otherwise, there exists m > 0 such that c0 ←−−R · · · ←−−R cm−1 ←−−R cm −−→R cm+1 .
    We use a second induction on m. Observe that, by Lemma 5.14, there exists c′m such
                 s≻∗      s≻∗
    that cm−1 −−→R c′m ←−−R cm+1 . Then the sequence c0 , . . . , cm−1 , c′m , cm+1 , . . . , ck still
    satisfies the properties above. If m = 1, we are have t1 →∗R c′1 and we complete by
                                                                                s≻∗            s≻∗
    the first induction hypothesis; if m > 1 then we observe that now c0 ←−−R · · · ←−−R
           s≻∗
    cm−2 −−→R cm , so we complete by the second induction hypothesis.


                                 6. Finding a Bounding Pair
The bounding pair (≻, ⪰) is an important component of bounded rewriting induction. Yet,
how to find it in practice? As we have seen, we do not have to fix the pair in advance, but
can use the process of bounded rewriting induction to accumulate requirements. Let us say
the process delivers a set REQS of requirements of the form s ≻ t [φ] or s ⪰ t [φ] with s ̸= t
(if s = t, then we already know s ⪰ t [φ] is true and s ≻ t [φ] is false if φ is satisfiable). But
having done so, we are still left with the difficulty of proving that a bounding pair for those
requirements exists. We discuss two different approaches to define such a pair.

6.1. Using a reduction ordering. A reduction ordering is a monotonic (i.e. s ⊐ t implies
C[s] ⊐ C[t] for every context C[□]) well-founded partial ordering on the set of terms.
Monotonicity does not imply that s ⊐ t whenever s ▷ t but we can use a reduction ordering
that includes →R to construct a bounding pair, as follows:
▷ define a ≻1 b if a ⊐ b or a ▷ b; define a ≻ b if a ≻+                    ∗
                                                      1 b, and a ⪰ b if a ≻1 b;
▷ require that ℓγ ⊐ rγ for each ℓ → r [φ] ∈ R and ground substitution γ that respects φ
The monotonicity requirement ensures that well-foundedness of ⊐ is preserved in ≻: if
s ⊐ t = C[t′ ] and t′ ⊐ u, then s ⊐ C[t′ ] ⊐ C[u], so any infinite sequence of ≻ steps can be
converted into an infinite sequence of ⊐ steps.
     There are various methods to define a reduction ordering in traditional term rewriting,
with recursive path orderings and polynomial interpretations being among the most well-
known. Unfortunately, there are not as many methods for higher-order or constrained term
rewriting, and even fewer for the combination (although a variant of the recursive path
ordering for LCSTRSs exists [GK24]). That being said, while the method of Bounded RI
is defined on LCSTRSs, it can also be used on unconstrained first-order term rewriting
systems, and there we have many methods at our disposal.

Using a rewrite relation. However, it is worth noting that if Q is a set of rules such that
R ∪ Q is a terminating rewrite system, then →+ Q∪R is by definition a reduction ordering. So,
if every s ≻ t [φ] or s ⪰ t [φ] in REQS gives a valid rewrite rule s → t [φ], we can simply
let Q be this set of rules, and use any method to prove termination. Thus, we could in
particular use the dependency pair framework [AG00, GTSK05], which allows reduction
orderings to be used in a more liberal way by requiring weak instead of full monotonicity.
                         BOUNDED REWRITING INDUCTION FOR LCSTRSs                                    39




     A downside of this approach is that it is possible to encounter requirements that are not
valid rules, and this is especially common in higher-order rewriting since the left-hand side of
a rule may not have a variable as the head, and must have the same type as the right-hand
side. For example, suppose REQS ∋ f (F x) y ≻ y − 1 [x > y], with f :: int → int → list.
We cannot include a rule f (F x) y → y − 1 [x > y] in Q, because the two sides have a
different type (list versus int). Even if they had the same type, the only dependency pair
framework for LCSTRSs that has thus far been defined [GHKV24] does not support rules
whose left-hand side contains applied variables, so the subterm F x is problematic.
     A solution to this issue is to not derive Q from the set REQS directly, but merely to
ensure that sγ (→Q∪R ∪▷)+ tγ for all s ≻ t [φ] or s ⪰ t [φ] in REQS and γ that respect
φ. For example, if we introduce a new function symbol inttolist :: int → list, then the above
requirement is handled by including a rule f z y → inttolist (y − 1) [true] in Q. While it is
not immediately obvious how to build such an abstraction in general, at least it is easy to
avoid the issue of different types through the introduction of constructors like inttolist.
     An advantage of using a reduction relation is that it generates a bounding pair that
satisfies the premise of Lemma 4.3. Hence, by taking some care with the use of (Hypothesis),
(Alter) and (Generalize), we can ensure that equation contexts are always strongly bounded.
This yields substantially fewer ordering requirements – and thus an easier proof search.


6.2. Separating top and inner steps. The idea explored above – of deriving our bounding
pair from a single reordering – is quite powerful and allows us to reuse existing termination
methods. In particular the approach of letting ⊐ be a terminating relation →Q∪R is
reminiscent of traditional ways of using RI (e.g., [Red90, FK12, FKN17, HK24]), where the
induction hypotheses in H are oriented as rules, and we prove termination of →R∪H .
     However, in these approaches we do not fully take advantage of the weaker requirements
in the present setting. In particular, the elements of REQS do not need to be oriented with
a monotonic relation. For example, if R = {f a → f b} and REQS = {b ≻ a}, there is
no reduction ordering ⊐ that orients REQS, since then we would need both f a ⊐ f b and
f b ⊐ f a (by monotonicity). Yet, there are bounding pairs for these requirements: e.g., the
relation (→{b→a [true]},top ∪ →R ∪▷)+ , whose subrelation →Q,top is defined by:
Definition 6.1. For a set Q of triples (ℓ, r, φ) of two terms and a constraint, let s →Q,top t
if there exist (ℓ, r, φ) ∈ Q and a substitution γ that respects φ, such that s = ℓγ and t = rγ.
    In terms of the (first-order) dependency pair framework, the difference can roughly be
summarised as follows: termination of →Q∪R coincides with finitess of the DP problem
(DP(Q ∪ R), Q ∪ R), whereas termination of →Q,top ∪ →R ∪▷ coincides with finiteness of
(DP(Q ∪ R), R). In higher-order rewriting, there are multiple dependency pair frameworks,
and their full introduction requires some theoretical development that is beyond the scope
of this paper. However, we will show how the question whether a suitable bounding pair
exists can be reduced to the existence of something much like a dependendency pair chain.

Dependency-pair-like chains. In the following, we assume that REQS contains only
requirements of the form f ⃗ℓ ≻ r [φ] or f ⃗ℓ ⪰ r [φ] with f ∈ Σ. We define:
• REQS⪰ = {(ℓ, r, φ) | ℓ ⪰ r [φ] ∈ REQS} and REQS≻ = {(ℓ, r, φ) | ℓ ≻ r [φ] ∈ REQS}.
• R′ is the set {(ℓ x1 · · · xi , r x1 · · · xi , φ) | ℓ → r [φ] ∈ R ∧ ℓ :: σ1 → . . . → σn → ι (ι ∈ S)
  ∧ 0 ≤ i ≤ n ∧ x1 :: σ1 , . . . , xi :: σi fresh variables}.
40                                      K. HAGENS AND C. KOP




• Defs is the set of pairs (f, n) such that there exists (f ℓ1 · · · ℓn , r, φ) ∈ R′ ∪REQS≻ ∪REQS⪰ .
• A candidate is a term s of the form f s1 · · · sn with either f ∈ V and n > 0, or (f, n) ∈ Defs.
• Let Pweak = {ℓ → r [φ] ∈ REQS⪰ ∪R′ | r is a candidate} and Pstrong = {ℓ → r [φ] ∈ Q1 | r
   is a candidate} ∪ {ℓ → p [φ] | ℓ → r [φ] ∈ REQS≻ ∪ REQS⪰ ∪ R′ ∧ r ▷ p ∧ p is a candidate}.
• A strong chain is an infinite sequence si →Pstrong ,top ti (→R ∪ →Pweak ,top )∗ si+1 for all i.
      The elements of Pweak ∪Pstrong are essentially the dynamic dependency pairs of REQS∪R′
(see [KR12]), except that we did not mark the head symbol of the left-hand side; such a
marking can always be added at a later stage in a termination proof. Correspondinglyy, a
strong chain is a dependency pair chain in which the DPs in Pstrong occur infinitely often.
Lemma 6.2. For ground terms s, t, let s ⪰ t if s (→REQS≻ ∪REQS⪰ ,top ∪ →R ∪▷)∗ t and
s ≻ t if there exist u, v such that s ⪰ u →REQS≻ ,top v ⪰ t. Suppose no strong chain exists.
    Then (≻, ⪰) is a bounding pair that orients all requirements in REQS.
Proof. Clearly ⪰ is transitive and reflexive, as it is the transitive-reflexive closure of the
relation ⪰base :=→REQS≻ ∪REQS⪰ ,top ∪ →R ∪▷. We have ≻ ⊆ ⪰ because →REQS≻ ,top ⊆ ⪰base
⊆ ⪰ and ⪰ is transitive, while transitivity of ≻ follows because a ⪰ · →REQS≻ ,top · ⪰ b ⪰
· →REQS≻ ,top · ⪰ c implies a ⪰ · →Q1 ,top · ⪰ · ⪰ · ⪰base · ⪰ c and ⪰ is transitive. The
properties ≻ · ⪰ ⊆ ⪰ and ⪰ · ≻ ⊆ ⪰ follow similarly. It is also obvious that all requirements
in REQS are oriented. All that remains to be shown is well-foundedness of ≻.
     Towards a contradiction, suppose that ≻ is not well-founded; that is, there is a sequence
of →REQS≻ ,top ∪ →REQS⪰ ,top ∪ →R ∪▷ steps in which →REQS≻ ,top appears infinitely often.
We define that a term s is non-terminating if there is an infinite such sequence starting in s,
terminating if there is not, and minimal non-terminating (MNT) if s is non-terminating but
all its strict subterms terminate; i.e., t is terminating whenever s ▷ t.
     Since ⪰ includes both ▷, we first make the following important observation:
     (OBS1) if u is terminating and u ▷ q then also q is terminating.
     Using this property along with an induction on the size of s, we easily observe:
     (OBS2) if sγ is non-terminating but for all x ∈ V ar(s) the term γ(x) is terminating,
then there is a non-variable term t with s ⊵ t such that tγ is minimal non-terminating.
     If an MNT term s = f u1 · · · un is reduced with →REQS≻ ∪REQS⪰ ,top then (f, n) ∈ Defs.
If it is reduced with →R at the top or head, then it could be reduced with →R′ ,top , so
also (f, n) ∈ Defs. If s ▷ t then by definition t is no longer MNT. And if s →R t by some
reduction not at the head, then t = f u1 · · · u′i · · · un with ui →R u′i ; so t has the same
outer shape, and is terminating or MNT. This last point holds because u′i and each uj are
terminating, as is f u1 · · · u′i · · · un−1 (being equal to, or a reduct of, the terminating subterm
f u1 · · · un−1 of s). Hence we conclude:
     (OBS3) if s = f u1 · · · un is MNT then (f, n) ∈ Defs
     Finally, again using (OBS1) we have:
     (OBS4) for (f ℓ1 · · · ℓk , r, φ) ∈ REQS≻ ∪ REQS⪰ ∪ R′ and substitution γ: if ℓi γ is
terminating, then so is each γ(x) with x ∈ V ar(ℓi ).
    Towards obtaining the required contradiction, we will construct a strong chain. From
the assumption that ≻ is not well-founded, we know that a non-terminating term exists, and
use (OBS2) with γ = [] to obtain a MNT term t0 . In the following, denote →R,in for a step
not at the top or head of a term, i.e., f s1 · · · sj · · · sn →R,in f s1 · · · s′j · · · sn if sj →R s′j .
    Now, for natural number i, assume given a minimal non-terminating term ti . Then,
denoting ⇝ for the relation (→REQS⪰ ,top ∪ →R ∪▷), non-termination of ti implies that
there is a reduction ti = a1 ⇝ a2 ⇝ · · · ⇝ am →REQS≻ ,top b, with b still non-terminating.
                          BOUNDED REWRITING INDUCTION FOR LCSTRSs                                      41




We prove, by induction on m − j for j ∈ {1, . . . , m}, that if aj is MNT then there exist MNT
terms si+1 and ti+1 such that aj (→R,in ∪ →Pweak ,top )∗ si+1 and si+1 →Pstrong ,top ti+1 .
▷ If j = m then aj = ℓγ for some (ℓ, r, φ) ∈ REQS≻ ; write ℓ = f ℓ1 · · · ℓk . Then (f, k) ∈ Defs,
  and each ℓn γ is terminating by minimality. By (OBS4), also all γ(x) are terminating.
  As b = rγ, by (OBS2), there is a non-variable subterm r ⊵ p such that pγ is MNT. By
  (OBS3), pγ is a candidate, and because p is not itself a variable, this means p must be a
  candidate. Hence, we can let si+1 := aj = ℓγ and ti+1 := pγ.
▷ If j < m and aj ▷ aj+1 , then a′j ⊵ aj+1 for some immediate argument term a′j of aj , and
  therefore aj+1 would be terminating by definition of aj being MNT. This is not possible
  as aj+1 reduces to the non-terminating term b.
▷ If j < m and aj →R aj+1 by a step not at the head, then we can write aj = f u1 · · · un · · · um
  and aj+1 = f u1 · · · u′n · · · um . All arguments ul are terminating, and therefore so is u′n . Also,
  f u1 · · · um−1 is terminating (as a strict subterm of aj ), so if n′ < m then f u1 · · · u′n · · · um−1
  is terminating as well. Hence, all strict subterms of aj+1 are terminating, and aj+1 is still
  MNT. Hence, by the induction hypothesis, aj →R,in aj+1 (→R,in ∪ →Pweak ,top )∗ si+1 and
  si+1 →Pstrong ,top ti+1 for suitable si+1 , ti+1 .
▷ Finally, if j < m and either aj →R aj+1 at the head, or aj →REQS⪰ ,top aj+1 , then there
  is some (ℓ, r, φ) ∈ R′ ∪ REQS⪰ such that aj = ℓγ and aj+1 = rγ and γ respects φ. Then
  by (OBS4) and minimality of aj , all γ(x) are terminating. Since aj+1 is necessarily
  non-terminating (as it reduces to the non-terminating term b), clearly r is not a variable.
  By (OBS2) there is a non-variable term p with r ⊵ p such that pγ is MNT. By (OBS3)
  and the fact that p is not a variable, p is a candidate. There are two options:
  – If r = p, then (ℓ, r, φ) ∈ Pweak . Hence, using the induction hypothesis, aj →Pweak ,top
     aj+1 (→R,in ∪ →Pweak ,top )∗ si+1 and si+1 →Pstrong ,top ti+1 for some MNT si+1 , ti+1 .
  – If r ▷ p, then (ℓ, p, φ) ∈ Pstrong . Hence, we let si+1 := ℓγ and ti+1 := pγ.
In particular (for j = 1), ti (→R ∪ →Pweak ,top )∗ si+1 and si+1 →Pstrong ,top ti+1 . We have thus
constructed a strong chain, which contradicts the lemma’s assertion that no strong chain
exists. We conclude a contradiction with the assumption that ≻ is not well-founded.
    Overall, if all elements of REQS have a shape f s1 · · · sn ≻ t [φ] or f s1 · · · sn ⪰ t [φ] with
f not a variable, then we know that a suitable bounding pair for REQS exists so long as we
can prove the absence of a strong chain.
    If the elements of REQS do not all have this form, we may still be able to apply a similar
approach (by changing REQS so the original requirements are captured by the pair (≻, ⪰)
defined in Lemma 6.2), but the techniques to do so are beyond the scope of this section.

Reduction triples. To directly investigate the presence of strong chains we can use an
extension of the notion of reduction ordering:
Corollary 6.3. A reduction triple is a triple (>, ≳, ≥) of three relations such that:
• > is a well-founded partial ordering on the set of terms
• ≳ is a quasi-ordering on the set of terms, such that s > t ≳ u implies s > u
• ≥ is a monotonic quasi-ordering on the set of terms, such that s ≥ t implies s ≳ t
There exists no infinite strong chain if we can find a reduction triple (>, ≳, ≥) such that:
• for all (ℓ, p, φ) ∈ Pstrong and all γ that respect φ: ℓγ > pγ
• for all (ℓ, p, φ) ∈ Pweak and all γ that respect φ: ℓγ ≳ pγ
• for all ℓ → r [φ] ∈ R and all γ that respect φ: ℓγ ≥ rγ
42                                    K. HAGENS AND C. KOP




     The advantage of a reduction triple compared to a reduction ordering is that the
monotonicity requirement is replaced by weak monotonicity: only ≥ needs to be monotonic.
It also allows us to more easily take advantage of the difference between ≻ and ⪰ requirements.
     Reduction triples can be constructed using for instance argument filterings or weakly
monotonic algebras. While there has not yet been extensive research in this direction for
higher-order constrained rewriting, this is a natural direction for future work.


                     7. Obtaining new deduction rules more easily
In section 4, we set out to prove soundness and completeness of Bounded RI in a modular
way: rather than merely proving that the system as given in Figure 1 satisfies Theorem 3.4,
we have hown the stronger Theorem 4.18. This means that any extension of the system
with derivation rules that satisfy both the Preserving Bounds Property (Definition 4.1)
and Base Soundness Property (Definition 4.9), is still sound; and if these rules satisfy the
Completeness Property (Definition 3.15) they can also be used in a non-equivalence proof.
    Let us discuss two naturally arising situations for which we can exploit this approach to
introduce a new deduction rule, and establish its soundness relatively easy.

Calculations. In the definition of Bounded RI, we follow the approach of [HK24] for the
definition of the (Simplify) (and (Hypothesis)) rules: these rules are much more basic than
the corresponding rule in the first-order RI definition for LCTRSs [FKN17] which uses
a more sophisticated definition of “constrained reduction”. Essentially, a slightly weaker
version of the (Alter) step is included in the (Simplify) rule of [FKN17].
     The price for this simplicity, however, is that we often require extra steps, especially
when it comes to calculation rules. For example, in subsection 3.2 we encountered the
equation (for the sake of clarity we omit the bounding terms of the equation context):
                 f i (recdown f n (i − 1) a) ≈ tailup f (n + 1) i (f n a) [i ≥ n]
Here, we first had to apply (Alter) to obtain the equation
     f i (recdown f n (i − 1) a) ≈ tailup f (n + 1) i (f n a) [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
before we could apply two (Simplify) steps, using calculation rules i − 1 → i′ [i′ = i − 1] and
n + 1 → n′ [n′ = n + 1], turning the equation into
          f i (recdown f n i′ a) ≈ tailup f n′ i (f n a) [i′ = i − 1 ∧ n′ = n + 1 ∧ i ≥ n]
With constrained reductions, we could do the (Simplify) steps directly to obtain the same
result. Fortunately, we can regain this facility by observing that the following deduction rule

(Calc)                                                                         n>0
              (E ⊎ {(ς ; C[s1 , . . . , sn ] ≈ t ; τ) [ψ]}, H)                 s1 , . . . , sn theory terms

(E ∪ {(ς ; C[x1 , . . . , xn ] ≈ t ; τ) [ψ∧(x1 = s1 )∧. . .∧(xn = sn )]}, H)   x1 , . . . , xn distinct fresh
                                                                               variables


can be considered as a shortcut for an (Alter) step, followed by some (Simplify) steps,
possibly followed again by some (Alter) steps. (Provided all variables in each si are in
V ar(ψ), or theory sorts are inextensible.) Therefore, it immediately satisfies the two
invariants.
                       BOUNDED REWRITING INDUCTION FOR LCSTRSs                                  43




Example 7.1. We may use (Calc) to replace an equation f (x + (y + 1)) ≈ t by f z ≈ t [z =
x + (y + 1)]. To do so without (Calc) would require four steps:
          (E0)     f (x + (y + 1)) ≈ t
          (E1)     f (x + (y + 1)) ≈ t [q = y + 1 ∧ z = x + q]              by (Alter)
          (E2)            f (x + q) ≈ t   [q = y + 1 ∧ z = x + q]           by (Simplif y)
          (E3)                  f z≈t     [q = y + 1 ∧ z = x + q]           by (Simplif y)
          (E4)                  f z≈t     [z = x + (y + 1)]                 by (Alter)
This cannot be done with only one (Alter) step because the rules in Rcalc do not have
composite terms on their right-hand sides; there is no rule x + (y + 1) → z [z = x + (y + 1)].

Axioms. We can use the two properties to go beyond just composite rules, though. A
particular example, from a rule that is implemented in incremental Rewriting Induction
(iRI) [Aot06, Section 5], is the use of axioms: equations that are known to be consequences
of R, but for which we may not have a proof using Bounded RI. Let A be a set of such
axioms. We distinguish the following two cases:
▷ R is ground confluent, and all equations in A are ground convertible; that is, sγ ↔∗R tγ
   for all s ≈ t [φ] ∈ A and ground substitutions γ that respect the equation.
▷ A is a set of equations such that every equation context in EA = {(ℓ ; ℓ ≈ r ; r) [φ] | ℓ ≈
   r [φ] ∈ A} is R/∅/∅-bounded ground convertible with respect to the same ordering pair
  (≻, ⪰) that is used in the RI derivation under consideration.
     Either way, we introduce the following deduction rule:

    (Axiom)
                 (E ⊎ {(ς ; C[ℓδ] ≃ t ; τ) [ψ]}, H)       ℓ ≃ r [φ] ∈ A and ψ |=δ φ
                 (E ∪ {(ς ; C[rδ] ≈ t ; τ) [ψ]}, H)       ς ⪰ C[rδ] [ψ]

Lemma 7.2. The (Axiom) rule preserves bounds.
Proof. If (ς ; C[ℓδ] ≃ t ; τ) [ψ] is a bounded equation context, then τ ⪰ t [ψ]. Since the
derivation rule requires ς ⪰ C[rδ] [ψ], also (ς ; C[rδ] ≈ t ; τ) [ψ] is bounded.
Lemma 7.3. (Axiom) satisfies the Base Soundness Property.
Proof. To see this, we will show that if (ς ; C[ℓδ] ≃ t ; τ) [ψ] is a bounded equation context
                                                                {ςγ,τγ} ∗             {ςγ,τγ}
and γ a gsc substitution which respects it, then C[ℓδ]γ ←−−−−→
                                                             ′
                                                               C[rδ]γ ←−−−−→
                                                                           ′
                                                                             tγ holds
                                                                 R;H;E                R;H;E
for any E, H and E ′ = E ∪ {(ς ; C[rδ] ≈ t ; τ) [ψ]}.
     The latter step is obvious: by Definition 4.5.(C) we only have to show that {ςγ, τγ} ⪰mul
{ςγ, τγ}, which is trivially true. So consider the former step.
     In the first case, where R is gound confluent and ℓχ ↔∗R rχ for all ground substitutions χ
that respect the equation, we have in particular that ℓδγ →∗R · ←∗R rδγ. Since →R is included
                                            {ℓδγ,rδγ} ∗
in ⪰ by definition of a bounding pair, ℓδγ ←−−−−−−→ rδγ holds by Definition 4.5.(A). In the
                                               R;∅;∅
second case, where all equation contexts in EA are R/∅/∅-bounded ground convertible, we
                                                          {ℓδγ,rδγ} ∗
have this property by definition. Either way, C[ℓδ]γ ←−−−−−−→ C[rδ]γ holds by Lemma 4.7,
                                                             R;∅;∅
44                                 K. HAGENS AND C. KOP



                                                                   {ℓδγ,rδγ} ∗
and since this derivation can only use steps with R, C[ℓδ]γ ←−−−−−−
                                                                  ′
                                                                    → C[rδ]γ follows
                                                                     R;H;E
regardless of H and E ′ . Observe that ςγ ⪰ C[ℓδ]γ ⪰ ℓδγ since the original equation context
is bounded and ⪰ includes ▷; and that τγ ⪰ C[rδ]γ ⪰ rδγ by definition of the rule. Hence,
                                                                  {ςγ,τγ} ∗
we apply Lemma 4.8 to increase the bounds and obtain C[ℓδ]γ ←−−−−→
                                                                 ′
                                                                   C[rδ]γ.
                                                                   R;H;E




                                    8. Implementation
We have implemented bounded rewriting induction in our tool Cora [Kop25] as an interactive
proving procedure. Here, the user has to supply the proof steps, while the tool keeps track
of all equation contexts, ensures that deduction rules are applied correctly, and searches for
a bounding pair. We choose the strategy from subsection 6.1: we maintain strongly bounded
equation contexts by viewing each occurrence of s ⪰ t [ψ] in Figure 1 as s ⪰! t [ψ], and use
the results of [GHKV24] to, essentially, prove termination of the LCSTRS REQS ∪ R.
     Validity and satisfiability checks are delegated to an external SMT-solver (by default
Z3 [dMB08] , but the user can set other preferences), on the theory of (first-order) integer
arithmetic (QF NIA) [BFT25]. For the two highly undecidable derivation rules (Generalize)
and (Alter), only limited versions are available to handle the most common cases:
• for (Generalize), Cora allows the user to change the constraint to an implied one, or to
  supply an equation that the current goal is an instance of;
• for (Alter), Cora allows the user to supply an equivalent constraint, or add definitions
  x = u into the constraint with x a fresh variable; in addition, case II combined with a
  (Delete) step can be accessed through the eq-delete command.
     The use of Cora is illustrated in Figure 2. By default, Cora shows only the equation
part of an equation context, coupled with a red ⊚ if a side of the equation is the same as its
bounding term. (The full equation context can be queried using the command :equations
full.) The deduction rules are implemented through commands like simplify and delete,
and explained by a :help command. Termination checks are done once the proof is complete,
but can also be forced earlier by the user executing :check.
     While Cora does require user guidance, there is some automation. As shown in Figure 2,
commands like simplify can be called with more or less information: simplify without
arguments rewrites with an arbitrary rule at some innermost position, but the user can
also supply the rule, position and substitution to be used. An auto command is supplied
to automatically do simplify, calc, delete, hdelete, eq-delete, disprove and semiconstructor
steps as far as possible. This use of automation is shown in Figure 3.
     In the future, we hope to further automate the rewriting induction process. However,
a fully automatic process will need to include a powerful lemma generation engine for the
(Postulate) and (Generalize) commands, so this is a large project.
     An evaluation page with savefiles that provide full proofs for the inductive theorems in
this paper (including two proofs for inductive theorems in our earlier work, which we will
briefly discuss in section 10) is provided at
                  https://cs.ru.nl/~cynthiakop/experiments/lmcs26/
     Here, you will also find a pre-compiled version of Cora, and instructions on how to start
the proof process.
BOUNDED REWRITING INDUCTION FOR LCSTRSs   45




      Figure 2: Basic usage of Cora
46             K. HAGENS AND C. KOP




     Figure 3: Using the auto command in Cora
                        BOUNDED REWRITING INDUCTION FOR LCSTRSs                               47




                            9. Comparison to related work
As briefly mentioned in section 3, improvements on the termination requirements for the
basic RI system [Red90] were already introduced in [Aot06, Aot08a, Aot08b]. These works
also explore ways to have more flexibility in the construction of a well-founded ordering ≻,
either fixed beforehand (e.g., the lexicographic path ordering), or constructed during or after
the proof. Essentially, they already employed a bounding pair (≻, ⪰), using a second (milder)
ordering ⪰, to allow for reduction steps with an induction hypothesis to be oriented with ⪰
rather than the default ≻. However, there are differences compared to our approach using
equation contexts and bounding terms. In our case, we do not orient induction hypotheses
themselves: we only require that a particular instance of the induction hypothesis is strictly
dominated by the bounding terms of the equation context under consideration. Another
notable difference is that their approach imposes more bureaucracy, since derivation rules
rely on several steps being done at once, by reasoning modulo a set of induction hypotheses.
This makes it quite hard to use especially when the relation ≻ is not fixed beforehand but
constructed on the fly. Finally, a difference compared to our work is that we do not impose
a ground totality requirement, allowing us, for instance, to choose ≻ = (→A ∪▷)+ , or to
use a construction based on dependency pairs (see section 6). This is particularly important
in higher-order rewriting, where very few ground-total orderings exist.

(Expand). Many of the existing RI systems in the literature include a deduction rule called
(Expand), used to perform induction proofs. At a first encounter, the (Expand) rule can
be difficult to grasp, since it combines many conceptual steps simultaneously — something
that is also undesirable from the perspective of modularity. This motivated us to decompose
the rule, making the individual proof steps explicit, which in turn naturally led to the
introduction of two new deduction rules: (Induct) and (Case). In the setting of Bounded RI,
(Expand) can be viewed as the consecutive execution of three deduction rules:
(1). (Induct). Given a proof state P0 = (E ⊎ {(ς ; s ≈ t ; τ) [ψ]}, H) we apply (Induct) to
     obtain P1 = (E ∪ {(s ; s ≈ t ; t) [ψ]}, H ∪ {s ≈ t [ψ]}).
        However, in most of the literature, the set H contains oriented equations, and R ∪ H
     is required to be terminating. In our system we can model this by choosing one side of
     the equation where we will apply (Expand), and orienting the equation in that direction.
     For example, if we choose the left-hand side s, then we require s ≻ t [ψ]. (In this setting,
     we let ⪰ be the reflexive closure of ≻ and impose →R ⊆ ≻.)
(2). (Case). In the (Expand) rule, the user provides a position p in the chosen side of the
     equation (in our example: in s), such that the subterm s|p at this position has a form
     f s1 · · · sn with f ∈ D, n ≥ ar (f), and such that si is a semi-constructor term for all
     1 ≤ i ≤ ar (f). With these ingredients we define a cover set as follows:
                                                                              
                                    ℓ → r [φ] ∈ R, δ = mgu(f s1 · · · sk , ℓ),
                    CEXP = (δ, φδ)
                                    δ(V ar(φ) ∪ V ar(ψ)) ⊆ Val ∪ V
    Due to the assumption of quasi-reductivity, this really is a cover set. We apply (Case)
    to P1 , using CEXP to obtain the following proof state
          P2 = (E ∪ {(sδ ; sδ ≈ tδ ; tδ) [ψδ ∧ φ] | (δ, φ) ∈ CEXP }, H ∪ {s ≈ t [ψ]})
(3). (Simplify) on each of the equations obtained in (2), using the corresponding rule
     ℓ → r [φ] ∈ R. Due to the choice of cover set, the conditions of (Simplify) are satisfied.
48                                     K. HAGENS AND C. KOP



                                    →R                            →R
       This yields P3 = (E ∪ EEXP       , H ∪ {s ≈ t [ψ]}) with EEXP =
                                                                                               
                                                             ℓ → r [φ] ∈ R,                    
      (sδ ; s[r sk+1 · · · sn ]p δ ≈ tδ ; tδ) [(ψδ) ∧ (φδ)] δ = mgu(f s1 · · · sk , ℓ),
                                                              δ(V ar(φ, ψ) ∪ V ar(ψ)) ⊆ Val ∪ V
                                                                                               

Hence, we can still do the traditional (Expand) rule in our work by using multiple steps, and
improve on it by not requiring s ≻ t [ψ]. Instead, a typically weaker requirement is imposed
when we apply the induction hypothesis s ≈ t [ψ] in a (Hypothesis) or (H-Delete) step.

                               10. Conclusion & Future Work
With the introduction of Bounded Rewriting Induction, we revised the existing RI system for
LCSTRSs, making fundamental changes with the aim of reducing termination requirements.
We replaced a well-founded order ≻ or terminating relation →R∪H with a bounding pair
(≻, ⪰) allowing for less strict ordering requirements with ⪰. We replaced equations by
equation contexts, which contain bounding terms, keeping track of induction bounds efficiently.
As a byproduct, we have obtained a more intuitive proof system with a higher degree of
modularity, which makes it easy to add new deduction rules to the system.

Easier induction proofs. In Bounded RI, we deviate from our earlier work by not requiring
the induction hypotheses themselves to be oriented. In particular, the (H-Delete) rule is
beneficial, as it often allows us to complete a proof with minimal termination requirements
(e.g., requirements that are immediately satisfied if →R is included in ≻). This allows us to
entirely avoid challenges we encountered in our previous work. We provide two examples.
(1). The paper [HK23] proves sum2 x ≈ sum3 x in the LCSTRS
             sum2 x → add x (sum2 (x − 1)) [x > 0] sum3 x → v x 0
             sum2 x → return 0                   [x ≤ 0]    v x a → v (x − 1) (a + x) [x > 0]
 add x (return y) → return (x + y)                          v x a → return a              [x ≤ 0]
     As explained in [HK23], it is easy to find the lemma equation add x (v y z) ≈ v y a [a =
     x + z] that is needed for a rewriting induction proof to succeed. In the RI system
     of [HK23], however, this is not a suitable induction hypothesis, as neither the rule
     v y a → add x (v y z) [a = x + z] nor add x (v y z) → v y a [a = x + z] is terminating.
     Further effort needs to be spent to find invariants x > 0 and z ≥ 0 to obtain a
     terminating induction rule. In Bounded RI this is not necessary: we can directly use
     the equation as induction hypothesis, since (H-Delete) imposes lower requirements.
(2). The paper [HK24] proves sumfun f n ≈ fold [+] 0 (map f (init n))[n ≥ 0] in the LCSTRS
            fold g v nil → v                     map f nil → nil
               fold g v (h : t) → fold g (g v h) t map f (h : t) → (f h) : map f t
               init n → nil [n < 0]                 init n → n : init (n − 1)   [n ≥ 0]
       The proof requires the induction rule x + (fold [+] y l) → fold [+] z l [z = x + y] which is
       non-standard, as it has a theory symbol + as root symbol on the left. Termination can
       be proven, but requires a very advanced method that is not easy to use automatically.
       In practice, we would like to avoid such induction rules as much as possible. Again,
       Bounded RI provides a solution, since the application of (H-Delete) with induction
       hypotheses x+(fold [+] y l) ≈ fold [+] z l [z = x+y] does not impose such a requirement.
                       BOUNDED REWRITING INDUCTION FOR LCSTRSs                              49




Ground confluence. Since Bounded RI proves bounded ground convertibility, rather than
merely ground convertibility as in, e.g., [HK24], we can use the system to prove ground
confluence: we defined critical pairs for LCSTRSs and showed that a terminating LCSTRS
is ground confluent if all its critical peaks are bounded ground convertible. Finally, as a
natural application of this result, we showed that for ground confluent LCSTRSs, Bounded
RI can be extended into a system for disproving inductive theorems.
    We would like to conclude with some practically motivated directions for future research.

Global rewriting induction. A property not discussed in this work, but a major topic
in [AYC11, HK24], is extensibility. This means that if an equation is an inductive theorem
in L, it remains an inductive theorem in any “reasonable” extension of L (intuitively, a
reasonable extension is one that represents a real-world program, in which L is a separate
module). Such inductive theorems are called global inductive theorems. In terms of functional
programming, if two functions are equivalent this should not change when these functions
are used inside a larger program. Extensibility is a way to express that local reasoning
extends globally, at least for such reasonable LCSTRSs. From a perspective of software
verification this is a desirable property: to prove properties about a small part of a larger
system, we only need to consider the rules that are directly related.
     Global Rewriting Induction [HK24] is an extension of RI, designed to prove global
inductive theorems. An interesting question is of course whether we can apply a similar
construction to Bounded RI. The major challenge in this will be to guarantee that a bounding
pair (≻, ⪰) on T (Σ, V) can be extended to a bounding pair (≻′ , ⪰′ ) on T (Σ′ , V ′ ), for any
reasonable extension L′ = (R′ , Σ′ ) of L = (R, Σ). In particular, we will have to reconsider
every deduction rule in Figure 1 that has an ordering requirement, including (Hypothesis),
(H-Delete), (Generalize) and (Alter).

Ground convertibility modulo axioms. In practice, we encounter inductive theorems
which are only provable once we are allowed to utilize our knowledge about the instantiation
of certain variables. For example, an equivalence P1 f ≈ P2 f may hold only under the
assumption that f :: int → int → int is instantiated by a commutative function. So instead
of considering convertibility under all ground substitutions, we restrict to those ground
substitutions that instantiate f as a commutative function.
     Designing a corresponding RI system is non-trivial, because this new kind of equivalence
is no longer based on the standard notion of inductive theorem, but on a restricted form of
ground convertibility. This likely brings us into a setting similar to term rewriting modulo a
set A of axioms. A natural first step is therefore to examine how the soundness proofs from
section 4 can be adapted to the setting of rewriting modulo A.

Automating RI proofs. Currently, any proof by Bounded RI is (almost) completely
human driven. Ideally, we would like to incorporate some tactics in Cora for automatically
proving inductive theorems with Bounded RI, building on what has been implemented in
Ctrl [FKN17] for first-order LCTRSs. As observed in section 8, a major obstacle in this is
finding lemmas automatically. Here, existing generalization methods can be employed, but
it remains a challenge to determine when and how to apply them effectively. Of course, as
program equivalence in general is undecidable, we cannot expect them to be exhaustive.
50                                  K. HAGENS AND C. KOP




Unbounded RI. The definition of Bounded RI takes advantages of the restriction that all
our equation contexts are bounded (and remain so because our derivation rules have the
Preserving Bounds property). However, this restriction is not fundamental: as shown by
the proofs in section 4, what matters most is that the right multiset ordering conditions are
imposed. To obtain these conditions we currently use the property that equation contexts
are bounded, but we could alternatively require it directly in the derivation rules. This
would for instance replace the (Hypothesis) rule by
                (E ⊎ {(ς ; C[ℓδ] ≃ t ; τ) [ψ]}, H)    ℓ ≃ r [φ] ∈ H and ψ |=δ φ and
                (E ∪ {(ς ; C[rδ] ≈ t ; τ) [ψ]}, H)    {{ς, τ}} ≻mul {{ℓδ, rδ}} [ψ]

And (Induct) would become:
                    (E ⊎ {(ς ; s ≈ t ; τ) [ψ]}, H)
                                                              {{ς, τ}} ⪰mul {{s, t}} [ψ]
             (E ∪ {(s ; s ≈ t ; t) [ψ]}, H ∪ {s ≈ t [ψ]})
On the upside, we could then weaken the restrictions for (Alter)/(Generalize) (since it is no
longer necessary to preserve bounds). We have checked all the proofs for this altered system,
and it is sufficient to derive ground convertibility, though not bounded ground convertiblity.
     The advantage of such a change is that we can further weaken the ordering requirements:
instead of requiring that →R is included in ⪰ it would suffice if s ⪰ s ↓R for all ground terms
s. However, a downside is that it is not obviously usable for proving ground confluence.
     The most important complication is that six different combinations of ≻ and ⪰ are
admissible when realizing a multiset ordering. This is not a problem if the bounding pair
(≻, ⪰) is fixed in advance, but is challenging if the search for a bounding pair is done
afterwards. Naı̈vely exploring the entire search space – i.e. considering all options at every
deduction step that imposes requirements on the ordering – would lead to exponential growth
in the length of the deduction sequence. From this perspective, Bounded RI can be seen
as a heuristic that provides guidance on which ordering requirements to impose. In future
work, it would be interesting to further explore Unbounded RI and determine if there are
strategies to take advantage of the greater generality, and still find a bounding pair easily.
                           BOUNDED REWRITING INDUCTION FOR LCSTRSs                                                                    51




                                               References
[AG00]    T. Arts and J. Giesl. Termination of term rewriting using dependency pairs. TCS, 236(1–2):133–
          178, 2000. doi:10.1016/S0304-3975(99)00207-8.
[ANS24]   T. Aoto, N. Nishida, and J. Schöpf. Equational theories and validity for logically constrained
          term rewriting. In Proc. FSCD 24, volume 299 of LIPIcs, pages 31:1–31:21, 2024. doi:10.4230/
          LIPICS.FSCD.2024.31.
[Aot06]   T. Aoto. Dealing with non-orientable equations in rewriting induction. In Proc. RTA 06, volume
          4098 of LNCS, pages 242–256, 2006. doi:10.1007/11805618\_18.
[Aot08a] T. Aoto. Designing a rewriting induction prover with an increased capability of non-orientable
          theorems. In Proc. SCSS 08, 2008.
[Aot08b] T. Aoto. Soundness of rewriting induction based on an abstract principle. Inf. Media Technol.,
          3(2):225–235, 2008. doi:10.11185/IMT.3.225.
[AT16]    T. Aoto and Y. Toyama. Ground confluence prover based on rewriting induction. In Proc.
          FSCD 16, volume 52 of LIPIcs, pages 33:1–33:12, 2016. doi:10.4230/LIPICS.FSCD.2016.33.
[AYC11] T. Aoto, T. Yamada, and Y. Chiba. Natural inductive theorems for higher-order rewriting. In
          Proc. RTA 11, volume 10 of LIPIcs, pages 107–121, 2011. doi:10.4230/LIPIcs.RTA.2011.107.
[AYT04] T.. Aoto, T. Yamada, and Y. Toyama. Inductive theorems for higher-order rewriting. In Proc.
          RTA 04, volume 3091 of LNCS, pages 269–284, 2004. doi:10.1007/978-3-540-25979-4_19.
[BFT25]   C. Barrett, P. Fontaine, and C. Tinelli. The SMT-LIB Standard: Version 2.7. Technical report,
          Department of Computer Science, The University of Iowa, 2025. Available at http://www.
          SMT-LIB.org. For QF NIA, see https://smt-lib.org/logics-all.shtml#QF_NIA.
[BN98]    F. Baader and T. Nipkow. Term rewriting and all that. Cambridge University Press, 1998.
          doi:10.1017/CBO9781139172752.
[dMB08] L. de Moura and N. Bjørner. Z3: An efficient SMT solver. In Proc. TACAS 08, volume 4963 of
          LNCS, pages 337–340, 2008. doi:10.1007/978-3-540-78800-3_24.
[FK12]    S. Falke and D. Kapur. Rewriting induction + linear arithmetic = decision procedure. In Proc.
          IJCAR 12, volume 7364 of LNAI, pages 241–255, 2012. doi:10.1007/978-3-642-31365-3_20.
[FKN17] C. Fuhs, C. Kop, and N. Nishida. Verifying procedural programs via constrained rewriting
          induction. ACM Transactions On Computational Logic (TOCL), 18(2):14:1–14:50, 2017. doi:
          10.1145/3060143.
[GHKV24] L. Guo, K. Hagens, C Kop, and D. Vale. Higher-order constrained dependency pairs for (universal)
          computability. In Proc. MFCS 24, 2024. doi:10.48550/arXiv.2406.19379.
[GK24]    L. Guo and C. Kop. Higher-order LCTRSs and their termination. In Proc. ESOP 24, volume
          14577 of LNCS, pages 331–357, 2024. doi:10.1007/978-3-031-57267-8_13.
[GTSK05] J. Giesl, R. Thiemann, and P. Schneider-Kamp. The dependency pair framework: combining
          techniques for automated termination proofs. In F. Baader and A. Voronkov, editors, Proc. LPAR,
          pages 301–331, 2005. doi:10.1007/978-3-540-32275-7_21.
[HK23]    K. Hagens and C. Kop. Matrix invariants for program equivalence in lctrss. In Proc. WPTE 23,
          2023. URL: https://wpte2023.github.io/paper2.pdf.
[HK24]    K. Hagens and C. Kop. Rewriting induction for higher-order constrained term rewriting systems. In
          Proc. LOPSTR 24, volume 14919, pages 202–219, 2024. doi:10.1007/978-3-031-71294-4\_12.
[Kop25]   C. Kop. COnstrained Rewriting Analyser (CORA). Open-source analysis tool for higher-order
          constrained term rewriting, 2025. URL: https://github.com/hezzel/cora.
[KR12]    C. Kop and F. van Raamsdonk. Dynamic dependency pairs for algebraic functional systems.
          LMCS, 8(2):1–51, 2012. doi:10.2168/LMCS-8(2:10)2012.
[NNK+ 10] N. Nakabayashi, N. Nishida, K. Kusakari, T. Sakabe, and M. Sakai. Lemma generation method
          in rewriting induction for constrained term rewriting systems. Computer Software, 28(1):173–189,
          2010. URL: https://www.trs.css.i.nagoya-u.ac.jp/crisys/nakabayashi10.pdf.
[Red90]   U.S. Reddy. Term rewriting induction. In Proc. CADE ’90, volume 449 of LNCS, pages 162–177,
          1990. doi:10.1007/3-540-52885-7_86.
[SM23]    J. Schöpf and A. Middeldorp. Confluence criteria for logically constrained rewrite systems. In Proc.
          CADE 23, volume 14132 of LNCS, pages 474–490, 2023. doi:10.1007/978-3-031-38499-8\_27.




                                              This work is licensed under the Creative Commons Attribution License. To view a copy of this
                                              license, visit https://creativecommons.org/licenses/by/4.0/ or send a letter to Creative
                                              Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or Eisenacher Strasse 2,
                                              10777 Berlin, Germany
