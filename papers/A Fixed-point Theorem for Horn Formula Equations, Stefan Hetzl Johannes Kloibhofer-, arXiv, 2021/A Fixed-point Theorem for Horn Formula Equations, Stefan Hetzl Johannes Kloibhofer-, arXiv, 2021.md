         A Fixed-point Theorem for Horn Formula Equations

                                Stefan Hetzl                 Johannes Kloibhofer*
                                    Institute of Discrete Mathematics and Geometry
                                                  TU Wien
                                               Vienna, Austria
                           stefan.hetzl@tuwien.ac.at           j.kloibhofer@gmx.net



       We consider constrained Horn clause solving from the more general point of view of solving formula
       equations. Constrained Horn clauses correspond to the subclass of Horn formula equations. We state
       and prove a fixed-point theorem for Horn formula equations which is based on expressing the fixed-
       point computation of a minimal model of a set of Horn clauses on the object level as a formula in
       first-order logic with a least fixed point operator. We describe several corollaries of this fixed-point
       theorem, in particular concerning the logical foundations of program verification, and sketch how to
       generalise it to incorporate abstract interpretations.


1     Introduction
Constrained Horn clauses are a versatile and practical formalism for representing and solving a variety
of problems in program verification and model checking [4, 17]. In this paper we approach constrained
Horn clause solving from a theoretical point of view. In logic, related problems have a long history:
solving Boolean equations goes back to the 19th century and was already investigated in [32], see [30] for
a comprehensive textbook. Solving Boolean equations is closely related to Boolean unification, a subject
of thorough study in computer science, see, e.g., [26] for a survey. The generalisation of this problem
from propositional to first-order logic has been made explicit as early as [2, 3]. Solving a formula
equation in first-order logic is closely related to second-order quantifier elimination, a problem with
applications in a variety of areas in computer science, e.g., databases or common-sense reasoning [14].
A seminal work on second-order quantifier elimination and basis of several algorithms still in use today
is Ackermann’s [1]. See [35] for a recent survey of this area of related problems.
    Solving constrained Horn clauses is closely related to solving formula equations. In fact, constrained
Horn clauses correspond to a natural class of formula equations which we will call Horn formula equa-
tions. This relationship allows for an elegant theoretical description of the connections between problems
considered from Ackermann to contemporary verification.
    Fixed-point theorems play an important role for solving equations in many areas of mathematics. In
recursion theory, a subject with close ties to verification, the recursion theorem guarantees the existence
of a solution of a system of recursion equations by computing a fixed point. But also in areas quite remote
from verification similar constructions can be found, as in the use of Banach’s fixed-point theorem in the
proof of the Picard-Lindelöf theorem on the unique solvability of ordinary differential equations. In
constrained Horn clause solving we have a comparable situation: it is a well-known result from logic
programming and constraint logic programming that every set of Horn clauses has a unique minimal
model (in the sense of identifying a model with the ground atoms true in it) and that this minimal model
can be computed as the fixed-point of an operator induced by the clause set [33, 22].
    * Supported by the Vienna Science and Technology Fund (WWTF) as part of the Vienna Research Group VRG 12-004


Hossein Hojjat and Bishoksan Kafle (Eds.): 8th Workshop on                      © S. Hetzl & J. Kloibhofer
Horn Clauses for Verification and Synthesis (HCVS 2021)                         This work is licensed under the
EPTCS 344, 2021, pp. 65–78, doi:10.4204/EPTCS.344.5                             Creative Commons Attribution License.
66                                                          A Fixed-point Theorem for Horn Formula Equations


     In this paper we formulate and prove a fixed-point theorem for Horn formula equations which (es-
sentially) makes the construction of the minimal model explicit in the logic. Expressing this construction
will be achieved by using FO[LFP], first-order logic with a least fixed-point operator, thus providing a
canonical solution for any Horn formula equation. The fixed-point theorem has a number of applications:
it helps to explain, at least from a theoretical point of view, the efficacy of interpolation for Horn clause
solving and invariant generation. Moreover, as a simple corollary one can obtain the expressibility of the
weakest precondition and the strongest postcondition, and thus the partial correctness of an imperative
program in FO[LFP]. As another corollary it allows a generalisation of a result by Ackermann [1] on
second-order quantifier-elimination in a direction different from the recent generalisation [34]. A result
from a recently introduced approach to inductive theorem proving with tree grammars described in [10]
on generating a proof with induction based on partial information about that proof can be obtained from
our fixed-point theorem as another straightforward corollary. Last, but not least, an abstract form of the
fixed-point theorem, stated here as Conjecture 24, would permit to considerably simplify the proof of the
decidability of affine formula equations [19].
     In Section 2 we relate constrained Horn clause solving with solving formula equations. The fixed-
point theorem is stated and proved in detail in Section 3. Section 4 describes some of its applications
to the foundations of program verification. In Section 5 we sketch how to generalise our fixed-point
theorem to accommodate abstract interpretation based on Galois connections. This paper is an improved
presentation of some of the main results of the second authors master’s thesis [25].



2    Constrained Horn clauses and formula equations
We use standard notation from logic. In particular, for a first-order language L , an L -structure M , an
L -formula ϕ , and an interpretation I of the free variables of ϕ in M we write M , I |= ϕ to express that
ϕ is true in M under the interpretation I (in the usual sense of Tarski semantics). Occasionally we will,
in a slight abuse of notation, also allow elements of M or relations over M to appear on the right-hand
side of |= by which we intend to denote truth in M under an accordingly modified interpretation I. We
write |= ϕ to express that ϕ is a valid formula. Individual variables will be denoted by lowercase Latin
letters x, y, z, u, v . . .. Predicate variables will be denoted by uppercase Latin letters X ,Y, . . .. If X is a k-
ary predicate variable and χ is a first-order formula with the free variables v1 , . . . , vk we write [X \χ ] for
the substitution of X by χ inserting the i-th argument of an X -atom for vi . We write [X1 \χ1 , . . . , Xn \χn ]
for the simultaneous substitution of Xi by χi for i = 1, . . . , n. A substitution [X1 \χ1 , . . . , Xn \χn ] is called
first-order substitution if χ1 , . . . , χn are first-order formulas. The logical symbol ⊥ is a nullary predicate
constant which is false in all structures.
     Let L be a first-order language and let T be an L -theory. A constrained Horn clause is an L -
formula of the form ϕ ∧ X1 (t1 ) ∧ · · · ∧ Xn (tn ) → Y (s) or ϕ ∧ X1 (t1 ) ∧ · · · ∧ Xn (tn ) → ⊥ where t1 , . . . ,tn , s
are tuples of first-order terms of appropriate arity and ϕ is a first-order formula, i.e., a formula not
containing predicate variables. Note that a constrained Horn clause is allowed to (and typically does)
contain free individual variables which, as usual in clause logic, are treated as universally quantified.
A finite set S of constrained Horn clauses is considered as the conjunction of these clauses and is thus
logically equivalent to a formula of the form ∀∗ C∈S C where ∀∗ denotes the universal closure w.r.t.
                                                            V

individual variables. We are interested in solving a given finite set of constrained Horn clauses. There
are different notions of solvability in the literature which we will discuss in detail below.
     In this paper we embed constrained Horn clauses in the more general framework of formula equa-
S. Hetzl & J. Kloibhofer                                                                                    67


tions. In the context of logical formulas, we consider an equation to be

                  an L -formula ϕ1 ↔ ϕ2 containing predicate variables X = X1 , . . . , Xn .               (1)

A solution of (1) is a first-order substitution [X\χ ] s.t. |= (ϕ1 ↔ ϕ2 )[X\χ ]. A solution in T has to satisfy
T |= (ϕ1 ↔ ϕ2 )[X\χ ] instead. Since the concept of solution in T subsumes that of solution (by setting
T = 0)
     / we will only use the former. We can simplify equations to instead considering

                     an L -formula ϕ containing predicate variables X = X1 , . . . , Xn .                  (2)

Then, as a solution in T , we ask for a first-order substitution [X\χ ] s.t. T |= ϕ [X\χ ]. Note that every
instance of (1) is an instance of (2) by letting ϕ be ϕ1 ↔ ϕ2 and every instance of (2) is an instance
of (1) by letting ϕ1 be ϕ and ϕ2 be ⊤. Moreover, it will be notationally useful to explicitly indicate the
predicate variables by existential quantifiers. Consequently we define:
Definition 1. A formula equation is a closed L -formula ∃X ϕ where ϕ contains only first-order quanti-
fiers. A solution of ∃X ϕ in T is a first-order substitution [X\χ ] s.t. T |= ϕ [X\χ ].
     The problem of computing a solution to a formula equation given as input will be denoted as FEQ in
the sequel. A formula equation ∃X ϕ is called valid if it is a valid second-order formula and satisfiable if
it is a satisfiable second-order formula. If S is a set of constrained Horn clauses in the predicate variables
X = X1 , . . . , Xn , then ∃X∀∗ C∈S C will be called Horn formula equation. Thus constrained Horn clauses
                               V

correspond to existential second order Horn logic, which also plays a significant role in finite model
theory, see [15].
     There are different notions of solvability for constrained Horn clauses in the literature: satisfiability
of [17] is satisfiability of a Horn formula equation, semantic solvability of [31] is validity of a Horn
formula equation, and syntactic solvability of [31] is solvability of a Horn formula equation. In this paper
we will primarily be interested in this last notion: solvability of a Horn formula equation. Every solvable
formula equation is valid and every valid formula equation is satisfiable but neither of the converse
implications are true as the following example shows.
Example 2. If ϕ is a first-order formula which is satisfiable but not valid and does not contain X then,
trivially, ∃X ϕ is a formula equation which is satisfiable but not valid.
     Towards an example for a valid but unsolvable Horn formula equation we work in the first-order
language L = {0/0, s/1}. Let A1 be ∀x s(x) 6= 0 and let A2 be ∀x∀y (s(x) = s(y) → x = y) and consider
the formula
                                                                                                  
    A1 ∧ A2 → ∃X ∃Y ∀u X (0) ∧Y (s(0)) ∧ (X (u) → Y (s(u))) ∧ (Y (u) → X (s(u))) ∧ ¬(X (u) ∧Y (u))

which, up to some simple logical equivalence transformations, is a Horn formula equation Φ. Now Φ is
valid since, in a model M of A1 ∧ A2 , interpreting X by {s2n (0) | n ∈ N} and Y by {s2n+1 (0) | n ∈ N}
makes the remaining formula true.
    For unsolvability suppose that Φ has a solution [X \χ (u),Y \ψ (u)], then, since the standard model N
in the language L satisfies A1 ∧ A2 , we would have

       N |= χ (0) ∧ ψ (s(0)) ∧ ∀u (χ (u) → ψ (s(u))) ∧ ∀u (ψ (u) → χ (s(u))) ∧ ∀u ¬(χ (u) ∧ ψ (u)),

in particular χ would be a definition of the even numbers. However, the theory of N in L admits
quantifier elimination [11, Theorem 31G] which has the consequence that the L-definable sets in N are
the finite and co-finite subsets of N [11, Section 3.1, Exercise 4] and thus we obtain a contradiction to χ
being a definition of the even numbers (which is neither finite nor co-finite).
68                                                     A Fixed-point Theorem for Horn Formula Equations


    Solving formula equations (FEQ) is closely related to the problem of second-order quantifier elim-
ination (SOQE): given a formula ∃X ϕ where ϕ contains only first-order quantifiers find a first-order
formula ψ s.t. |= ∃X ϕ ↔ ψ . The relationship between FEQ and SOQE often hinges on a third problem:
second-order quantifier elimination by a witness (WSOQE): given a formula ∃X ϕ where ϕ contains
only first-order quantifiers find a first-order substitution [X\χ ] s.t. |= ∃X ϕ ↔ ϕ [X\χ ], see [35] for more
details. This complex of problems has a long history in logic and a wealth of applications in com-
puter science, see the textbook [14] on second-order quantifier elimination. A number of algorithms for
second-order quantifier elimination have been developed, for example: The SCAN algorithm introduced
in [13] (tries to) compute(s) a first-order formula equivalent to ∃X ϕ for a conjunctive normal form ϕ
by forming the closure of ϕ under constraint resolution which only resolves on X -literals. The DLS
algorithm has been introduced in [8] and consists essentially of formula rewriting steps tailored to allow
application of Ackermann’s lemma (which instantiates a predicate variable provided some conditions on
the polarity of its occurrences are met).


3     The fixed-point theorem
It is well-known that a set of Horn clauses has a minimal model and that it can be obtained as least
fixed point of an operator induced by the clause set. In order to integrate this insight seamlessly into the
framework of formula equations we will express it on the object level by representing this least fixed-
point by means of an explicit least fixed-point operator. An adequate tool to that end is first-order logic
with least fixed points, FO[LFP], which plays an important role in finite model theory and descriptive
complexity [21].
     In order to introduce FO[LFP] we first define, by induction on a formula ϕ , what it means for a
predicate variable X to occur positively (negatively) in ϕ :
     1. If ϕ is an atom of the form X (t) then X occurs positively in ϕ .
     2. X occurs positively (negatively) in ¬ϕ iff X occurs negatively (positively) in ϕ .
     3. For ◦ ∈ {∧, ∨}, X occurs positively (negatively) in ϕ ◦ ψ iff X occurs positively (negatively) in ϕ
        or X occurs postively (negatively) in ψ .
     4. X occurs positively (negatively) in ϕ → ψ iff X occurs positively (negatively) in ψ or X occurs
        negatively (positively) in ϕ .
     5. For Q ∈ {∀, ∃}, X occurs positively (negatively) in Qx ϕ iff X occurs positively (negatively) in ϕ .
Example 3. X occurs positively but not negatively in ∀u (P(u) → X (u)). X occurs both positively and
negatively in ∀u (X (u) → X (s(u))).
FO[LFP] is first-order logic, augmented with a least fixed point operator lfp which allows to add new
predicates to the logic that have the form [lfpX ϕ (X , u)] where ϕ is a formula in which X occurs only
positively and the length of u is the arity of X . Then ϕ defines a monotone function Fϕ : P(M)k →
P(M)k and since the power set lattice P(M)k is complete, the Knaster-Tarski theorem applies and the
least fixed point of Fϕ is well-defined. The predicate [lfpX ϕ (X , u)] is interpreted as that least fixed point.
Example 4. Working in the language {E/2} of graphs, let X be a binary predicate variable and define

                              ϕ (X , u, v)   ≡   u = v ∨ ∃w(X (u, w) ∧ E(w, v)).

As X occurs only positively in ϕ we can form [lfpX ϕ (X , u, v)] and observe that [lfpX ϕ (X , u, v)](a, b) is
true iff there is a path from a to b.
S. Hetzl & J. Kloibhofer                                                                                                            69


    In this paper we will consider first-order logic with an operator for simultaneous least fixed points
(which corresponds to introducing mutual recursion). Then we require a tuple Φ = (ϕi (X1 , . . . , Xn , ui ))ni=1
of formulas containing the Xi only positively where the length of ui is the arity ki of Xi . For a structure
M with domain M we define

                          Fi :   M k1 × · · · × M kn → M ki ,
                                      (R1 , . . . , Rn ) 7→ {a ∈ M ki | M |= ϕi (R1 , . . . , Rn , a)}.

and the operator FΦ = (F1 , ..., Fn ) : M k1 × · · · × M kn → M k1 × · · · × M kn . Since the Xi occur only positively
in the ϕ j , the operator FΦ is monotone and, again, the Knaster-Tarski theorem applies. Thus we obtain
new predicates [lfpXi Φ] for i = 1, . . . , n which are interpreted by the i-th component of the least fixed
point of the operator FΦ . For more details, the reader is referred to [7].
    Let ∃X1 · · · ∃Xn ψ be a Horn formula equation. We distinguish three different types of clauses in ψ :

                                     (B)                                ϕ → Xi0 (s),
                                     (I) ϕ ∧ Xi1 (t1 ) ∧ · · · ∧ Xim (tm ) → Xi0 (s),
                                     (E) ϕ ∧ Xi1 (t1 ) ∧ · · · ∧ Xim (tm ) → ⊥,

where the constraint ϕ is a formula in L not containing a predicate variable, m ≥ 1, t1 , ..,tm , s are tuples
of first-order terms in L of appropriate arity and i0 , i1 , . . . , im ∈ {1, . . . , n}. Note that free variables y may
occur in the formulas ϕ and the terms s,t1 , . . . ,tm . We call the first base clauses, the second induction
clauses, and the third end clauses. The idea now is to build an inductive relation from the base and
induction clauses for every formula variable. For j = 1, . . . , n let B j and I j be the sets of clauses of the
form (B) and (I), respectively, where i0 = j. In order to abbreviate notation we write ι := (i1 , . . . , im )
and τ := (t1 , . . . ,tm ). A clause in I j is determined by the tuple (ϕ , ι , τ , s), thus we write (ϕ , ι , τ , s) for the
clause ϕ ∧ Xi1 (t1 ) ∧ · · · ∧ Xim (tm ) → X j (s) in I j . Analogously we write (ϕ , s) for the clause ϕ → X j (s) in
B j.
Definition 5. Let ∃X1 · · · ∃Xn ψ be a Horn formula equation. Define the n-tuple Φψ = (ϕ j (X1 , . . . , Xn , x j ))nj=1
where, for j = 1, . . . , n,
                                                                                                                           !
                                                _                               _                  m
                                                                                                   ^
         ϕ j (X1 , . . . , Xn , x j ) is ∃y             (ϕ ∧ x j = s) ∨                      ϕ∧         Xik (tk ) ∧ x j = s 
                                            (ϕ ,s)∈B j                     (ϕ ,ι ,τ ,s)∈I j        k=1


where y are the free variables of the clauses in B j ∪ I j and x j is a tuple of variables s.t. |x j | equals the
arity of X j .
    From the point of view of (constraint) logic programming, the above tuple of formulas is a first-order
definition of the operator TP induced by ∃X ψ when considered as a constraint logic program P, see,
e.g., [22]. Note that X1 , . . . , Xn only occur positively in Φψ , hence we can introduce the simultaneous
fixed-point formulas [lfpX j Φψ ] for j ∈ {1, . . . , n}.
Lemma 6. Let ∃X1 · · · ∃Xn ψ be a Horn formula equation and µ j := [lfpX j Φψ ] for j ∈ {1, . . . , n}, then

   1. |= ∃X ψ ↔ ψ [X\µ ] and
                                                                                                                    Vn
   2. if M |= ψ [X\R] for some structure M and relations R1 , . . . , Rn in M , then M |=                              j=1 (µ j → R j ).
70                                                           A Fixed-point Theorem for Horn Formula Equations


Proof. The right-to-left direction of 1 is clear. For the left-to-right direction we first observe that the
formulas µ1 , . . . , µn satisfy all clauses in (B) and (I), i.e., for all j ∈ {1, . . . , n} we have

                  |=∀y (ϕ → µ j (s)),                                                           ∀(ϕ , s) ∈ B j ,
                  |=∀y (ϕ ∧ µi1 (t1 ) ∧ · · · ∧ µim (tm ) → µ j (s)),                    ∀(ϕ , ι , τ , s) ∈ I j .

To see this let M be a structure and a s.t. M , [y := a] |= ϕ ∧ µi1 (t1 ) ∧ · · · ∧ µim (tm ), then, as (µ1 , . . . , µn )
is a fixed point of FΦ , we have M , [y := a] |= µ j (s). The argumentation is analogous for clauses of the
form (B).
     Now let M be a structure s.t. M |= ∃X ψ . Let R1 , . . . , Rn be relations in M s.t. M |= ψ [X\R]. Then
for all j ∈ {1, . . . , n}:

                M |=∀y (ϕ → R j (s)),                                                            ∀(ϕ , s) ∈ B j ,       (3)
                M |=∀y (ϕ ∧ Ri1 (t1 ) ∧ · · · ∧ Rim (tm ) → R j (s)),                      ∀(ϕ , ι , τ , s) ∈ I j .     (4)

Assume a j ∈ FΦ (R1 , . . . , Rn ) j . Then there either exists (ϕ , s) ∈ B j s.t. M |= ∃y (ϕ ∧ a j = s) or there exists
(ϕ , ι , τ , s) ∈ I j s.t. M , [X := R] |= ∃y (ϕ ∧ m k=1 Xik (tk ) ∧ a j = s). We assume the latter, the proof for the
                                                   V

former is analogous. Thus let a be s.t.
                                                                    m
                                                                    ^
                                  M , [X := R, y := a] |= ϕ ∧            Xik (tk ) ∧ x j = s.
                                                                   k=1

From (4) we obtain M , [y := a] |= R j (s) and thus M |= R j (a j ).
   Hence FΦ (R1 , . . . , Rn ) ⊆ (R1 , . . . , Rn ) and as (µ1 , . . . , µn ) is the least fixed point of FΦ we obtain
M |= nj=1 (µ j → R j ).
     V

   For all clauses in (E) we have

                               M , [X := R] |= ∀y (ϕ ∧ Xi1 (t1 ) ∧ · · · ∧ Xim (tm ) → ⊥),

and therefore, as X1 , . . . , Xn occur only negatively in this formula, we obtain

                               M , [X := µ ] |= ∀y (ϕ ∧ Xi1 (t1 ) ∧ · · · ∧ Xim (tm ) → ⊥).

Thus M , [X := µ ] satisfies all clauses in ψ and we conclude that M |= ψ [X\µ ]. For 2. we get M |=
Vn
 j=1 (µ j → R j ) analogously to the proof of 1.

Theorem 7 (Fixed-Point theorem). Let ∃X1 · · · ∃Xn ψ be a valid Horn formula equation and let µ j =
[lfpX j Φψ ] for j ∈ {1, . . . , n}. Then:
     1. |= ψ [X \µ ],
                                                                            Vn
     2. If |= ψ [X\χ ] for FO[LFP]-formulas χ1 , . . . , χn , then |=          j=1 (µ j → χ j ).

Proof. Follows immediately from Lemma 6.

    We now turn to dual and linear Horn formula equations. A dual constrained Horn clause is an L-
formula of the form ϕ ∧ X (t) → Y1 (s1 ) ∨ · · · ∨ Yn (sn ) or ϕ → Y1 (s1 ) ∨ · · · ∨ Yn (sn ) where t, s1 , . . . , sn are
tuples of first-order terms of appropriate arity and ϕ is a first-order formula, i.e., a formula not containing
predicate variables. A dual Horn formula equation is a formula equation of the form ∃X∀y m
                                                                                                                V
                                                                                                                    i=1 Hi ,
S. Hetzl & J. Kloibhofer                                                                                              71


where Hi is a constrained dual Horn clause for i ∈ {1, . . . , m}. A linear Horn formula equation is a
formula equation that is both Horn and dual Horn.
    For a formula ψ we define ψ D as ψ [X1 \¬X1 , . . . , Xn \¬Xn ] where X1 , . . . , Xn are all predicate variables
occurring in ψ . Note that |= ψ ↔ (ψ D )D for all formulas ψ . Moreover, note that |= ∃X ψ ↔ ∃X ψ D
where X = X1 , . . . , Xn are all predicate variables occurring in ψ . If ∃X ψ is a Horn formula equation,
then ∃X ψ D is logically equivalent to a dual Horn formula equation and if ∃X ϕ is a dual Horn formula
equation, then ∃X ϕ D is logicall equivalent to a Horn formula equation. Note that dualisation of a (dual)
Horn formula equation interchanges (B)- and (E)-clauses.
Example 8. Consider the constrained Horn clauses

                         ψ       ≡    X (a) ∧ (X (u) ∧ X (v) → Y ( f (u, v))) ∧ (Y (w) → ⊥).

The dualisation of ψ is

                   ψD        ≡    ¬X (a) ∧ (¬X (u) ∧ ¬X (v) → ¬Y ( f (u, v))) ∧ (¬Y (w) → ⊥)

which is logically equivalent to the dual constrained Horn clauses

                                 (X (a) → ⊥) ∧ (Y ( f (u, v)) → X (u) ∨ X (v)) ∧Y (w).

    We can now prove the following result which is dual to Lemma 6.
Lemma 9. Let ∃X1 · · · ∃Xn ψ be a dual Horn formula equation and ν j := ¬[lfpX j Φψ D ] for j ∈ {1, . . . , n},
then
   1. |= ∃X ψ ↔ ψ [X\ν ] and
                                                                                               Vn
   2. if M |= ψ [X \R], for a structure M and relations R1 , . . . , Rn in M , then M |=          j=1 (R j → ν j ).

Proof. Let µ j := [lfpX j Φψ D ] for j = 1, . . . , n. For 1. note that, since ∃X ψ is a dual Horn formula
equation, ∃X ψ D is logically equivalent to a Horn formula equation. An application of Lemma 6/1.
yields |= ∃X ψ D ↔ ψ D [X \µ ]. Since ψ D [X\µ ] is syntactically equal to ψ [X\ν ] we obtain |= ∃X ψ ↔
∃X ψ D ↔ ψ D [X\µ ] ↔ ψ [X\ν ].
     For 2. assume that M |= ψ [X\R] for a structure M and relations R1 , . . . , Rn in M . Then M |=
ψ D [X1 \Rc1 , . . . , Xn \Rcn ], so, by Lemma 6/2., M |= nj=1 (µ j → Rcj ) which yields M |= nj=1 (R j → ν j ) by
                                                         V                                   V

contraposition.

Theorem 10 (Dual Horn fixed-point theorem). Let ∃X1 · · · ∃Xn ψ be a valid dual Horn formula equation
and let ν j = ¬[lfpX j Φψ D ] for j = 1, . . . , n, then
   1. |= ψ [X \ν ] and
                                                                      Vn
   2. if |= ψ [X\χ ] for FO[LFP]-formulas χ1 , . . . , χn , then |=     j=1 (χ j → ν j ).

Proof. Follows immediately from Lemma 9.

    Note that the operator induced by Φψ D is not the dual operator of the one induced by Φψ in the sense
of [12] because Φψ D is not the (pointwise) negation of Φψ . Therefore ν is not the greatest fixed point of
Φψ . The question whether ν permits a sensible definition as a greatest fixed point is left as future work
by this paper. For the case of linear Horn formula equations we obtain:
72                                                      A Fixed-point Theorem for Horn Formula Equations


Theorem 11 (Linear Horn fixed-point theorem). Let ∃X1 · · · ∃Xn ψ be a valid linear Horn formula equa-
tion, let µ j = [lfpX j Φψ ] and ν j = ¬[lfpY j Φψ D ] for j = 1, . . . , n, then
     1. |= ψ [X \µ ] and |= ψ [X\ν ] and
   2. if |= ψ [X\χ ] for FO[LFP]-formulas χ1 , . . . , χn , then |= nj=1 ((µ j → χ j ) ∧ (χ j → ν j )).
                                                                   V

    Theorem 11/2. shows that solving a linear Horn formula equation is equivalent to solving an inter-
polation problem in FO[LFP] in the sense that, given two tuples of FO[LFP]-formulas we seek to find
a tuple of first-order, i.e., fixed-point free, formulas which is between them in the implication ordering.
At least from a theoretical point of view this result helps to explain the efficacy of interpolation-based
methods for solving constrained Horn clauses, see, e.g., [28]. The relationship between interpolation and
Horn clauses has also been studied by encoding interpolation problems with a language condition on the
constant symbols as Horn clause sets [31, 16].


4     Applications to program verification

    In this section we will describe some direct applications of our fixed-point theorem to the foun-
dations of program verification. As an exemplary framework we will consider the Hoare calculus for
a simple imperative programming language as in [36]. We fix the first-order language of arithmetic
L = {0, 1, +, −, ·, ≤}. The set of programs is defined by

                      p ::= skip | x := t | p0 ; p1 | if B then p0 else p1 | while B do p0 ,

where t is an L -term, B a quantifier-free first-order formula in L and x is a program variable.
     The denotational semantics of programs is defined as usual based on a set of states Σ: we write C(p)
for the partial function from Σ to Σ that is the denotational semantics of the program p. A Hoare triple is
written as {ϕ }p{ψ }. For the purposes of this paper we fix the program variables to taking values in the
integers and thus we can work in the standard model Z. We write σ |= {ϕ }p{ψ } if Z, σ |= ϕ implies that
Z,C(p)(σ ) |= ψ and |= {ϕ }p{ψ } if σ |= {ϕ }p{ψ } for all σ ∈ Σ. The Hoare calculus can be defined as
usual, see, e.g. [36]. We write ⊢ {ϕ }p{ψ } if {ϕ }p{ψ } is provable in the Hoare calculus. We can then
consider the verification condition of a Hoare triple as a Horn formula equation as follows:
Definition 12. The verification condition of a Hoare triple {ϕ }p{ψ }, written vc({ϕ }p{ψ }), is a formula
equation ∃I∀∗ vc({
                 ˜ ϕ }p{ψ }), where vc({
                                       ˜ ϕ }p{ψ }) is defined by structural induction on p as follows:

                              ˜ ϕ }skip{ψ }) = ϕ → ψ
                             vc({                                                                       (1)
                            ˜ ϕ }x j := t{ψ }) = ϕ → ψ [x j \t]
                           vc({                                                                         (2)
                             ˜ ϕ }p0 ; p1 {ψ }) = vc({
                            vc({                   ˜ ϕ }p0 {I}) ∧ vc({I}p
                                                                   ˜     1 {ψ })                        (3)
               ˜ ϕ }if B then p0 else p1 {ψ }) = vc({
              vc({                                ˜ ϕ ∧ B}p0 {ψ }) ∧ vc({
                                                                      ˜ ϕ ∧ ¬B}p1 {ψ })                 (4)
                    ˜ ϕ }while B do p0 {ψ }) = vc({I
                   vc({                         ˜    ∧ B}p0 {I}) ∧ (ϕ → I) ∧ (I ∧ ¬B → ψ )              (5)

where, in clauses (3) and (5), I is a fresh predicate variable which does not appear in ϕ nor in ψ . Then
vc({ϕ }p{ψ }) = ∃I∀∗ vc({
                        ˜ ϕ }p{ψ }) is obtained from vc({ ˜ ϕ }p{ψ }) by existential quantification of all
                        ∗ ˜ ϕ }p{ψ }).
predicate variables in ∀ vc({
    Note that this is an purely syntactic definition, thus we can define vc({ϕ }p{ψ }) analogously for a
program p and second-order formulas ϕ , ψ . We then obtain the following completeness result which
characterises Hoare provability by truth of a formula equation.
S. Hetzl & J. Kloibhofer                                                                                                   73


Theorem 13. Let {ϕ }p{ψ } be a Hoare triple. Then ⊢ {ϕ }p{ψ } iff Z |= {ϕ }p{ψ } iff Z |= vc({ϕ }p{ψ }).

Proof Sketch. ⊢ {ϕ }p{ψ } iff Z |= {ϕ }p{ψ } is soundness and completeness of the Hoare calculus. The
implication from ⊢ {ϕ }p{ψ } to ⇒ Z |= vc({ϕ }p{ψ }) is proved by a straightforward induction on the
structure of the Hoare proof of {ϕ }p{ψ } The implication from Z |= vc({ϕ }p{ψ }) to Z |= {ϕ }p{ψ } is
proved by translating the semantics.

    As a corollary we can now obtain the statement that a partial correctness assertion of an imperative
program is expressible as a formula in FO[LFP], a point also made in [5] for existential least fixed-point
logic.
Corollary 14. Let {ϕ }p{ψ } be a Hoare triple and let µ be the solution of vc({ϕ }p{ψ }) obtained from
Theorem 7, then Z |= vc({ϕ }p{ψ }) iff Z |= vc({
                                             ˜ ϕ }p{ψ })[I\µ ].
    A second corollary is based on the observation that vc({ϕ }p{ψ }) is a linear Horn formula equa-
tion (which can be shown by a straightforward induction). Therefore we can apply Theorem 11 to the
verification condition and obtain:
Corollary 15. Let {ϕ }p{ψ } be a Hoare triple, then ∃I1 · · · ∃In π ≡ vc({ϕ }p{ψ }) is a linear Horn for-
mula equation. Let π D be the dual formula of π with predicate variables K1 , . . . , Kn . Assume Z |=
vc({ϕ }p{ψ }) and let µ j = [lfpI j Φπ ] and ν j = ¬[lfpK j Φπ D ] for j = 1, . . . , n. Then

   1. Z |= vc({
            ˜ ϕ }p{ψ })[I\µ ] and Z |= vc({
                                        ˜ ϕ }p{ψ })[I\ν ].
                                                                                      Vn
   2. If Z, [I := R] |= vc({
                         ˜ ϕ }p{ψ }) for relations R1 , . . . , Rn , then Z |=           j=1 ((µ j → R j ) ∧ (R j → ν j )).

     This corollary shows that finding first-order formulas as loop invariants is equivalent to an interpo-
lation problem in the sense of finding a fixed-point free interpolant. Just as Theorem 11 does for linear
Horn clauses, this corollary contributes to explaining the efficacy of interpolation-based methods for loop
invariant generation, see, e.g. [27].
     As a third corollary we will show that the weakest precondition and the strongest postcondition are
expressed by the least and greatest solutions µ and ν of linear Horn formula equations based on the
verification condition.
Definition 16. Let p be a program and ϕ , ψ be first-order formulas in L . The weakest precondition1 of
p and ψ , written wp(p, ψ ), is defined as

                                      wp(p, ψ ) = {σ ∈ Σ | Z,C(p)(σ ) |= ψ }.

The strongest postcondition of p and ϕ , written sp(p, ϕ ), is defined as

                         sp(p, ϕ ) = {σ ∈ Σ | ∃σ ′ ∈ Σ : Z, σ ′ |= ϕ and C(p)(σ ′ ) = σ }.

   The following property of the weakest precondition and the strongest postcondition justifies the ter-
minology and is of fundamental importance.
Lemma 17. Let {ϕ }p{ψ } be a Hoare triple, then |= {ϕ }p{ψ } iff [ϕ ] ⊆ wp(p, ψ ) iff [ψ ] ⊇ sp(p, ϕ ).
   1 In the literature this is mostly called weakest liberal precondition and the term weakest precondition is reserved for the

context of total correctness. As we only talk about partial correctness of programs there is no need for us to do so.
74                                                    A Fixed-point Theorem for Horn Formula Equations


     For a formula ϕ all of whose free variables are program variables we define [ϕ ] = {σ ∈ Σ | Z, σ |= ϕ },
the set of states defined by ϕ . It is well-known that for any program p and any formula ψ there is a first-
order formula ϕwp which defines wp(p, ψ ), i.e., [ϕwp ] = wp(p, ψ ) and, symmetrically, for any program
p and any formula ϕ there is a first-order formula ψsp which defines sp(p, ϕ ), i.e., [ψsp ] = sp(p, ϕ ). Note
that these formulas rely on the expressivity of the assertion language, i.e, in our setting, on an encoding
of finite sequences in Z.
     We will consider the formula equation ∃X0 vc({ϕ }p{X0 }), which asks for a formula X0 s.t. all states
satisfying ϕ satisfy X0 after running the program p. Symmetrically we will consider the formula equa-
tion ∃X0 vc({X0 }p{ψ }). Note that these are linear Horn formula equations and therefore we can apply
Theorem 11. In general there also occur predicate variables in vc({ϕ }p{ψ }), yet here we will only be
interested in the solution for the outermost predicate variable.
Corollary 18. Let p be a program, let ϕ be a formula, let ∃X π ≡ ∃X0 vc({ϕ }p{X0 }), and let µ =
[lfpX0 Φπ ], then [µ ] = sp(p, ϕ ).

Proof. Since Z |= vc({ϕ }p{⊤}) we have Z |= ∃X vc({ϕ }p{X0 }). From Lemma 6/1. we obtain Z |=
vc({ϕ }p{µ }) which, by Theorem 13, is equivalent to |= {ϕ }p{µ }. By Lemma 17 we obtain [µ ] ⊇
sp(p, ϕ ).
    For the other direction let ψsp be a first-order formula with [ψsp ] = sp(p, ϕ ). By Lemma 17 we have
|= {ϕ }p{ψsp }, which is equivalent to Z |= vc({ϕ }p{ψsp }). By Lemma 6/2. we have Z |= ∀x(µ (x) →
ψsp (x)) and thus [µ ] ⊆ [ψsp ] = sp(p, ϕ ).
Corollary 19. Let p be a program and let ψ be a formula, let ∃X π ≡ ∃X0 vc({X0 }p{ψ }), and let
ν = ¬[lfpX0 Φπ D ], then [ν ] = wp(p, ψ ).
Proof. Symmetric to that of Corollary 18

   Note that the formulas µ and ν thus obtained do not rely on an expressivity hypothesis anymore. The
encoding of sequences is replaced by the least fixed-point operator.


5    Towards an abstract fixed-point theorem
Abstract interpretation, originally introduced in [6], is one of the most important techniques in static
analysis and software verification. Since many verification techniques could successfully be generalised
from programs to the logical level of constrained Horn clauses it is also natural to expect this possibility
for abstract interpretation. And indeed, abstract interpretations have been used in tools for solving Horn
clauses [20, 23]. In this section we briefly outline how we expect this generalisation to apply to our fixed-
point theorem. Proving the main statement of this section, Conjecture 24, is currently work-in-progress.
    An application we have in mind is the following: in the recent article [19] the decidability of the
existence of affine invariants for programs with affine assignments (essentially due to Karr [24]) has
been generalised to formula equations of the form ∃X∀∗ ϕ for ϕ being a quantifier-free formula. The
essential difference between the proof in [19] and Theorem 7 is that in [19] the fixed point is formed
in the lattice of affine subspaces and not in the power set lattice. We can allow for this possibility as
follows.
Definition 20. Let A = (A, ⊆) and B = (B, ⊑) be two partially ordered sets. A Galois connection
between A and B consists of two functions α : A → B and γ : B → A, s.t. for all X ∈ A and Y ∈ B:

                                       X ⊆ γ (Y )    ⇔     α (X ) ⊑ Y.
S. Hetzl & J. Kloibhofer                                                                                              75


Definition 21. Let L be a language. A model abstraction is a pair (M , G), where M is an L -structure
and G = (Vk , αk , γk )k∈N is a sequence of triples, s.t. for all k ∈ N : Vk = (Vk , ⊑) is a complete lattice and
αk : P(M k ) → Vk and γk : Vk → P(M k ) form a Galois-connection between (P(M k ), ⊆) and Vk .
Example 22. Consider the language Laff = (0, 1, +, (c)c∈Q ) where the intended interpretation of the
unary function symbol c for c ∈ Q is multiplication with c. Let Gaff = ((Aff Qk , ⊆), affk , idk )k∈N , where
Aff Qk is the set of all affine subspaces of Qk , affk maps every subset of Qk to its affine hull and idk is
the embedding of Aff Qk in P(Qk ). Then (Q, Gaff ) is a model abstraction.
     We will now introduce the semantics of model abstractions. We will interpret FO[LFP]- and second-
order-formulas ϕ by defining a satisfaction relation (M , G) |=a ϕ . The crucial difference between |=a
and standard Tarski semantics |= will be that second-order quantifiers and the least fixed-point operator
will not be interpreted in the power set of the domain but in G instead (for the appropriate arity). This
restriction of the domain of second-order quantification is reminiscent of (but different from) Henkin
semantics of second- and higher-order logic [18].
Definition 23. The defining clauses for first-order atoms, propositional connectives, and first-order quan-
tifiers for |=a are identical to those for |=. For formulas of the form ∃X ψ , where X is a k-ary predicate
variable, we define
                         (M , G) |=a ∃X ψ          ⇔       ∃S ∈ Vk : (M , G) |=a ψ [X \γk (S)],
and analogously for formulas of the form ∀X ψ . The semantics of the lfp-operator is defined as follows.
Let X1 , . . . , Xn be formula variables with Xi having arity ki , let Φ = (ϕi (X1 , . . . , Xn , ui ))ni=1 be a tuple of
formulas s.t. |ui | = ki and X1 , . . . , Xn occur only positively in ϕi for all i ∈ {1, . . . , n}. Let
                              Fi# : Vk1 × · · · ×Vkn → Vki
                                        (Y1 , . . . ,Yn ) 7→ αki ◦ Fi (γk1 (Y1 ), . . . , γkn (Yn )),
where Fi is defined as in Section 3 and let FΦ# = (F1# , . . . , Fn# ). Then
                               (M , G) |=a [lfpXi Φ](a)            ⇔       a ∈ γki (lfp(FΦ# )i ).
     Note that the semantics of the least fixed-point operator is well-defined: We already know that Fi is
a monotone operator and αki and γki are monotone as they form a Galois connection for i ∈ {1, . . . , n}.
Thus Fi# is monotone for all i ∈ {1, . . . , n} and therefore FΦ# is monotone as well. As Vk is a complete
lattice for all k ∈ N, we can use the Knaster-Tarski theorem to obtain the least fixed point of FΦ# .
Conjecture 24 (Abstract fixed-point theorem). Let L be a language and (M , G) be a model abstraction.
Let ∃X1 · · · ∃Xn ψ be a Horn formula equation and let µ j = [lfpX j Φψ ] for j = 1, . . . , n. Then:
   1. (M , G) |=a ∃X ψ ↔ ψ [X\µ ] and
                                                                                                        Vn
   2. if (M , G) |=a ψ [X\χ ] for FO[LFP]-formulas χ1 , . . . , χn , then (M , G) |=a               j=1 (α j → χ j ).
Example 25. In continuation of Example 22 consider an Laff                        formula equation ∃X ∀∗ ψ where ψ is a
quantifier-free formula. We want to decide whether there are formulas χ s.t. Q |= ψ [X \χ ] and χ1 , . . . , χn
are conjunctions of affine equations, i.e., they define affine subspaces of Qk in the model Q. As in [19]
we reduce the solvability of ∃X∀∗ ψ to solvability of one of its finitely many projections which are Horn
formula equations. Let ∃X∀∗ ϕ be one of them, then an application of Conjecture 24 yields a tuple of
FO[LFP]-formulas µ s.t. (Q, Gaff ) |=a ∃X ϕ ↔ ϕ [X\µ ]. Since all lattices Aff Qk have finite height we
can compute fixed-point free formulas χ equivalent to µ from µ and therefore (Q, Gaff ) |=a ∃X ϕ ↔
ϕ [X\χ ]. Now ϕ [X\χ ] is a first-order formula and hence (Q, Gaff ) |=a ϕ [X\χ ] iff Q |= ϕ [X\χ ]. The
latter statement can now be checked by a decision procedure for linear arithmetic.
76                                                   A Fixed-point Theorem for Horn Formula Equations


6    Conclusion

We have shown a fixed-point theorem for Horn formula equations and applied it to dual Horn formula
equations and linear Horn formula equations. The proof of this result essentially consists of expressing
the construction of a minimal model of a set of Horn clauses, which is familiar from logic programming,
on the object level as a formula in first-order logic with least fixed points, thus providing a canonical
solution to a Horn formula equation in FO[LFP].
    Note that Theorem 7 applies equally to constraints ϕ being FO[LFP]-formulas. It therefore shows
that FO[LFP], in contrast to first-order logic, has the property of being closed under solving Horn formula
equations. It thus shows that in FO[LFP] validity and solvability of Horn formula equations coincide.
This is in contrast to formula equations in first-order logic, cf. Example 2.
    Explicit fixed-point operators have been employed for second-order quantifier elimination in the
DLS∗ algorithm introduced in [29, 9]. In this algorithm Ackermann’s lemma is generalised to a fixed-
point lemma that covers additional situations. While the DLS∗ algorithm as such will fail on Horn
formula equations due to its priority of shifting universal quantifiers inwards, the fixed-point lemma
of the DLS∗ algorithm could be used for solving Horn formula equations with a single variable when
combined with a different preprocessing. However, for Horn formula equations with more than one
predicate variable it would result in solutions with iterated fixed points. In this sense our fixed-point
theorem can be considered a generalisation of the fixed-point lemma of [29]. On the other hand the
fixed-point lemma of [29] is not restricted to Horn formula equations.
     These fixed-point theorems contribute to our theoretical understanding of the logical foundations of
constrained Horn clause solving and software verification: Theorem 11 and Corollary 15 help to ex-
plain, from a theoretical point of view, the efficacy of interpolation for Horn clause solving and invariant
generation respectively. Moreover, as corollary to our fixed point theorem we have obtained the express-
ibility of the weakest precondition and the strongest postcondition, and thus the partial correctness of an
imperative program in FO[LFP].
    As shown in [25], our fixed-point theorem has a number of further corollaries in a variety of applica-
tion areas: it allows a generalisation of a result by Ackermann [1] on second-order quantifier-elimination
in a direction different from the recent generalisation [34] of that result. It allows to obtain a result on
the generation of a proof with induction based on partial information about that proof shown in [10] as
straightforward corollary. Last, but not least, an abstract form of the fixed-point theorem, Conjecture 24,
would permit to considerably simplify the proof of the decidability of affine formula equations given
in [19].
    In conclusion, we believe that it is fruitful to consider constrained Horn clause solving from the more
general point of view of solving formula equations. On the theoretical level this perspective uncovers
connections to a number of topics such as second-order quantifier elimination and results such as Ack-
ermann’s [1]. On the practical level it suggests to study the applicability of algorithms such as DLS
and SCAN for constrained Horn clauses and vice versa, that of algorithms for constrained Horn clause
solving for applications of second-order quantifier elimination.
    Acknowledgements. The authors would like to thank Christoph Wernhard for a number of help-
ful conversations about formula equations and second-order quantifier elimination and the anonymous
reviewers for many useful suggestions that have improved our work on this subject.
S. Hetzl & J. Kloibhofer                                                                                     77


References
 [1] Wilhelm Ackermann (1935): Untersuchungen über das Eliminationsproblem der mathematischen Logik.
     Mathematische Annalen 110(1), pp. 390–413, doi:10.1007/BF01448035.
 [2] Heinrich Behmann (1950): Das Auflösungsproblem in der Klassenlogik. Archiv für mathematische Logik
     und Grundlagenforschung 1(1), pp. 17–29, doi:10.1007/BF01976313. First of two parts.
 [3] Heinrich Behmann (1951): Das Auflösungsproblem in der Klassenlogik. Archiv für mathematische Logik
     und Grundlagenforschung 1(2), pp. 33–51, doi:10.1007/BF01982011. Second of two parts.
 [4] Nikolaj Bjørner, Arie Gurfinkel, Kenneth L. McMillan & Andrey Rybalchenko (2015): Horn Clause Solvers
     for Program Verification. In Lev D. Beklemishev, Andreas Blass, Nachum Dershowitz, Bernd Finkbeiner
     & Wolfram Schulte, editors: Fields of Logic and Computation II - Essays Dedicated to Yuri Gurevich
     on the Occasion of His 75th Birthday, Lecture Notes in Computer Science 9300, Springer, pp. 24–51,
     doi:10.1007/978-3-319-23534-9 2.
 [5] Andreas Blass & Yuri Gurevich (1987): Existential Fixed-Point Logic. In Egon Börger, editor: Computation
     Theory and Logic, In Memory of Dieter Rödding, Lecture Notes in Computer Science 270, Springer, pp.
     20–36, doi:10.1007/3-540-18170-9 151.
 [6] Patrick Cousot & Radhia Cousot (1977): Abstract Interpretation: A Unified Lattice Model for Static Analysis
     of Programs by Construction or Approximation of Fixpoints. In Robert M. Graham, Michael A. Harrison &
     Ravi Sethi, editors: 4th ACM Symposium on Principles of Programming Languages, ACM, pp. 238–252,
     doi:10.1145/512950.512973.
 [7] Anuj Dawar & Yuri Gurevich (2002): Fixed point logics. Bulletin of Symbolic Logic 8(1), pp. 65–88,
     doi:10.2178/bsl/1182353853.
 [8] Patrick Doherty, Witold Lukaszewicz & Andrzej Szalas (1997): Computing Circumscription Revisited: A
     Reduction Algorithm. Journal of Automated Reasoning 18(3), pp. 297–336, doi:10.1023/A:1005722130532.
 [9] Patrick Doherty, Witold Łukaszewicz & Andrzej Szałas (1998): General Domain Circumscription and its
     Effective Reductions. Fundamenta Informaticae 36(1), pp. 23–55, doi:10.3233/FI-1998-3612.
[10] Sebastian Eberhard & Stefan Hetzl (2015): Inductive theorem proving based on tree grammars. Annals of
     Pure and Applied Logic 166(6), pp. 665–700, doi:10.1016/j.apal.2015.01.002.
[11] Herbert B. Enderton (2001): A Mathematical Introduction to Logic, 2nd edition. Academic Press.
[12] Carsten Fritz (2001): Some Fixed Point Basics. In Erich Grädel, Wolfgang Thomas & Thomas Wilke, editors:
     Automata, Logics, and Infinite Games: A Guide to Current Research, Lecture Notes in Computer Science
     2500, Springer, pp. 359–364, doi:10.1007/3-540-36387-4 20.
[13] Dov Gabbay & Hans Jürgen Ohlbach (1992): Quantifier Elimination in Second Order Predicate Logic. South
     African Computer Journal 7, pp. 35–43.
[14] Dov M. Gabbay, Renate A. Schmidt & Andrzej Szałas (2008): Second-Order Quantifier Elimination. College
     Publications.
[15] Erich Grädel (1991): The Expressive Power of Second Order Horn Logic. In Christian Choffrut & Matthias
     Jantzen, editors: 8th Annual Symposium on Theoretical Aspects of Computer Science (STACS), Lecture
     Notes in Computer Science 480, Springer, pp. 466–477, doi:10.1007/BFb0020821.
[16] Ashutosh Gupta, Corneliu Popeea & Andrey Rybalchenko (2014): Generalised Interpolation by Solving
     Recursion-Free Horn Clauses. In Nikolaj Bjørner, Fabio Fioravanti, Andrey Rybalchenko & Valerio Senni,
     editors: Proceedings First Workshop on Horn Clauses for Verification and Synthesis (HCVS), EPTCS 169,
     pp. 31–38, doi:10.4204/EPTCS.169.5.
[17] Arie Gurfinkel & Nikolaj Bjørner (2019): The Science, Art, and Magic of Constrained Horn Clauses. In:
     21st International Symposium on Symbolic and Numeric Algorithms for Scientific Computing SYNASC,
     IEEE, pp. 6–10, doi:10.1109/SYNASC49474.2019.00010.
78                                                    A Fixed-point Theorem for Horn Formula Equations


[18] Leon Henkin (1950): Completeness in the Theory of Types. Journal of Symbolic Logic 15(2), pp. 81–91,
     doi:10.2307/2266967.
[19] Stefan Hetzl & Sebastian Zivota (2020): Decidability of affine solution problems. Journal of Logic and
     Computation 30(3), pp. 697–714, doi:10.1093/logcom/exz033.
[20] Krystof Hoder, Nikolaj Bjørner & Leonardo Mendonça de Moura (2011): µ Z - An Efficient Engine for Fixed
     Points with Constraints. In Ganesh Gopalakrishnan & Shaz Qadeer, editors: 23rd International Conference
     on Computer-Aided Verification (CAV), Lecture Notes in Computer Science 6806, Springer, pp. 457–462,
     doi:10.1007/978-3-642-22110-1 36.
[21] Neil Immerman (1999): Descriptive complexity. Springer, doi:10.1007/978-1-4612-0539-5.
[22] Joxan Jaffar & Michael J. Maher (1994): Constraint Logic Programming: A Survey. The Journal of Logic
     Programming 19/20, pp. 503–581, doi:10.1016/0743-1066(94)90033-7.
[23] Bishoksan Kafle, John P. Gallagher & José F. Morales (2016): Rahft: A Tool for Verifying Horn Clauses
     Using Abstract Interpretation and Finite Tree Automata. In Swarat Chaudhuri & Azadeh Farzan, editors:
     28th International Conference on Computer Aided Verification, Lecture Notes in Computer Science 9779,
     Springer, pp. 261–268, doi:10.1007/978-3-319-41528-4 14.
[24] Michael Karr (1976): Affine Relationships Among Variables of a Program. Acta Informatica 6, pp. 133–151,
     doi:10.1007/BF00268497.
[25] Johannes Kloibhofer (2020): A fixed-point theorem for Horn formula equations. Master’s thesis, TU Wien,
     Austria.
[26] Ursula Martin & Tobias Nipkow (1989): Boolean Unification – The Story So Far. Journal of Symbolic
     Computation 7(3-4), pp. 275–293, doi:10.1016/S0747-7171(89)80013-6.
[27] Kenneth L. McMillan (2003): Interpolation and SAT-Based Model Checking. In Warren A. Hunt Jr. &
     Fabio Somenzi, editors: Computer Aided Verification, 15th International Conference, CAV 2003, Boulder,
     CO, USA, July 8-12, 2003, Proceedings, Lecture Notes in Computer Science 2725, Springer, pp. 1–13,
     doi:10.1016/S0747-7171(86)80028-1.
[28] Kenneth L. McMillan & Andrey Rybalchenko (2012): Solving Constrained Horn Clauses using Interpola-
     tion. Technical Report, Microsoft Research. MSR-TR-2013-06.
[29] Andreas Nonnengart & Andrzej Szałas (1998): A Fixpoint Approach to Second-Order Quantifier Elimination
     with Applications to Correspondence Theory, pp. 307–328. Studies in Fuzziness and Soft Computing 24,
     Springer.
[30] Sergiu Rudeanu (1974): Boolean Functions and Equations. North-Holland.
[31] Philipp Rümmer, Hossein Hojjat & Viktor Kuncak (2013): Classifying and Solving Horn Clauses for Ver-
     ification. In Ernie Cohen & Andrey Rybalchenko, editors: 5th International Conference on Verified Soft-
     ware: Theories, Tools, Experiments (VSTTE), Lecture Notes in Computer Science 8164, Springer, pp. 1–21,
     doi:10.1007/978-3-642-54108-7 1.
[32] Ernst Schröder (1890): Vorlesungen über die Algebra der Logik. 1, Teubner.
[33] M. H. Van Emden & R. A. Kowalski (1976): The Semantics of Predicate Logic as a Programming Language.
     Journal of the ACM 23(4), p. 733–742, doi:10.1145/321978.321991.
[34] Christoph Wernhard: Approximating Resultants of Existential Second-Order Quantifier Elimination upon
     Universal Relational First-Order Formulas. In: Proceedings of the Workshop on Second-Order Quantifier
     Elimination and Related Topics (SOQE 2017).
[35] Christoph Wernhard (2017): The Boolean Solution Problem from the Perspective of Predicate Logic. In: 11th
     International Symposium on Frontiers of Combining Systems (FroCoS), Lecture Notes in Computer Science
     10483, Springer, pp. 333–350, doi:10.1007/978-3-319-66167-4 19.
[36] Glynn Winskel (1993): The Formal Semantics of Programming Languages – An Introduction. Foundation of
     computing series, MIT Press, doi:10.7551/mitpress/3054.001.0001.
