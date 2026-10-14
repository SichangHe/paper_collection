         Verified and Optimized Implementation
                of Orthologic Proof Search

                 Simon Guilloud(✉)         and Clément Pit-Claudel

              School of Computer and Communication Sciences, EPFL,
                        Station 14, 1015 Lausanne, Switzerland
                      {simon.guilloud,clement.pit-claudel}@epfl.ch




       Abstract. We report on the development of an optimized and veriﬁed
       decision procedure for orthologic equalities and inequalities. This deci-
       sion procedure is quadratic-time and is used as a sound, eﬃcient and
       predictable approximation to classical propositional logic in automated
       reasoning tools. We formalize, in the Coq proof assistant, a proof system
       in sequent-calculus style for orthologic. We then prove its soundness and
       completeness with respect to the algebraic variety of ortholattices, and
       we formalize a cut-elimination theorem. In doing so, we discover and ﬁx
       a missing case in a previously published proof.
          We then implement and verify a complete proof search procedure for
       orthologic. A naive implementation is exponential; to obtain an optimal
       quadratic run time, we optimize the implementation by memoizing its
       results and simulating reference equality testing. We leverage the result-
       ing correctness theorem to implement a reﬂective Coq tactic. We present
       benchmarks showing that the procedure, under various optimizations,
       matches its theoretical complexity.
          Finally, we develop a collection of tactics, including normalization
       with respect to orthologic and a boolean solver, which we also bench-
       mark. We make tactics available as a standalone Coq plugin.


1    Introduction

Specialized, reliable and eﬃcient building blocks are indispensable in scaling
automated reasoning software. Program veriﬁers, SMT solvers, proof assistants
and automated theorem provers use them to tackle the various theories and
subproblems that comprise a logical statement. As they build up, so does the
possibility of an implementation error. To ensure that they can be used as
trusted components in program veriﬁcation pipelines, these veriﬁcation algo-
rithms should themselves be veriﬁed.
    One fragment of particular interest is propositional logic. Despite signiﬁcant
progress in SAT solvers, solving satisﬁability or validity of propositional formu-
las remains a major challenge to scalability of decision procedures. An alter-
native and complementary approach to heuristics is orthologic-based reasoning.
Orthologic (OL) is a non-distributive generalization of classical propositional

 c The Author(s) 2025
R. Piskac and Z. Rakamarić (Eds.): CAV 2025, LNCS 15933, pp. 130–152, 2025.
https://doi.org/10.1007/978-3-031-98682-6_8
          Veriﬁed and Optimized Implementation of Orthologic Proof Search            131

logic which admits polynomial-time (O(n2 )) validity checking and normaliza-
tion algorithms [4, 9, 12]. Orthologic oﬀers a trade-oﬀ: it sacriﬁces completeness
(with respect to classical semantics) in exchange for guaranteed eﬃciency and
predictability. It also admits a quadratic-time normalization algorithm, allowing
to compute a unique normal form (with respect to the laws of orthologic) of
guaranteed minimal size.
    In the Lisa proof assistant [10], orthologic is key in making proofs shorter and
easier to write: while the proof system supports classical sequent calculus, any
formula transformation that holds true in (a ﬁrst order extension of) orthologic
can be deduced implicitly in a single step. This in particular takes into account
a variety of intuitive transformations, such as negation normal form, absorption
and reordering conjuncts and disjuncts, and keeps proof checking eﬃcient.
    In [9], orthologic normal form is used to improve the cache hit ratio of veriﬁ-
cation conditions, and to simplify them before sending them to an SMT solver.
    The foundations of an extension to Datalog with negation and disjunction
based on orthologic has been suggested in [12]. Indeed, by generalizing ortho-
logic to predicate orthologic, and restricting the presence of function symbols,
we obtain the orthologic equivalent of eﬀectively propositional logic, but with
exponentially faster decision procedure. Moreover, the resulting theory has the
same semantics as Datalog on the Datalog subset of all problems, yielding a
proper extension.
    The fact that orthologic admits the interpolation property [11, 18], suggests
possible use in model checking, and additional applications have been proposed
in [12], including in type systems with subtyping or reﬁnement/liquid types.
Table 1 presents the laws of orthologic.


 Table 1. Laws of ortholattices, algebraic varieties with signature (S, ∧, ∨, 0, 1, ¬).

              V1: x ∨ y = y ∨ x             V1’: x ∧ y = y ∧ x
              V2: x ∨ (y ∨ z) = (x ∨ y) ∨ z V2’: x ∧ (y ∧ z) = (x ∧ y) ∧ z
              V3: x ∨ x = x                 V3’: x ∧ x = x
              V4: x ∨ 1 = 1                 V4’: x ∧ 0 = 0
              V5: x ∨ 0 = x                 V5’: x ∧ 1 = x
              V6: ¬¬x = x
              V7: x ∨ ¬x = 1                V7’: x ∧ ¬x = 0
              V8: ¬(x ∨ y) = ¬x ∧ ¬y        V8’: ¬(x ∧ y) = ¬x ∨ ¬y
              V9: x ∨ (x ∧ y) = x           V9’: x ∧ (x ∨ y) = x



    In this work, we present the ﬁrst formalization and veriﬁcation, using the Coq
proof assistant, of an eﬃcient decision procedure for the validity and equivalence
problems for propositional formulas in orthologic. This algorithm [12] is based
on proof search in a proof system for orthologic that is a restriction of the clas-
sical sequent calculus where a sequent can never contain more than two distinct
132     S. Guilloud and C. Pit-Claudel

formulas at a time. Despite this restriction, the proof system admits cut elimi-
nation, which we formalize. The cut elimination property implies a subformula
property, which is key to the completeness of the proof search procedure.
    A naive implementation of the decision procedure has exponential complexity.
To obtain a polynomial version, we leverage memoization, i.e. storing in a table
the intermediate results of the recursive calls. Moreover, using structural equality
to check if a key is in the memoization map costs an additional linear runtime
factor. To obtain an optimal quadratic version, we modify the algorithm to use
a form of reference equality. As our algorithm is purely functional, this means
we have to extend our formulas’ abstract syntax trees to assign to each node a
unique identiﬁer (or pointer) that can then be used in the memoization map.
We formally prove the correctness of these constructions.
    We implement and verify multiple versions of the algorithm: without opti-
mization (O(2n )), with memoization using lists (O(n5 )), using AVL maps
(O(n3 )), and using AVL maps and simulated reference equality (O(n2 )). Memo-
ization and reference equality are generic, and important in many tools and algo-
rithms. Our approach to verifying these optimizations is not speciﬁc to orthologic
proof search and we expect it to extend to any recursive algorithm over algebraic
datatypes (ADT).
    Using the technique of proofs by reﬂection, we then obtain a set of executable
proof tactics, each deciding equality modulo orthologic rule and, applicable to
any ortholattice and in particular the type bool of boolean values. This tactic is
able to solve automatically, for example,



    We present benchmarks attesting that each version of the proof search pro-
cedure (with memoization using a list-based map, with memoization using AVL
trees, and with both memoization and reference equality) meets the theoretical
complexity.
    Many formulas are not completely provable in the fragment of orthologic,
in which case the decision procedure alone cannot do anything, even if most
of the structure of the formula reduces under orthologic rules. The orthologic
simpliﬁcation algorithm [9] on the other hand is widely applicable, and can make
substantial progress on a problem even if the formula is not equivalent to true.
This is also very useful if the propositional formulas are built on some theories,
such as arithmetic, in which case even classical boolean decision procedures
would not work. We implement this simpliﬁer in OCaml as a Coq plugin, using
the above tactic to eﬃciently prove equivalence with the original expression.
This yields a generic simpliﬁcation tactic for terms of type bool.
    We ﬁnally leverage this normalization tactic to implement a boolean solver
which alternates between branching on a variable and normalizing the formulas,
as in [10]. We present benchmarks comparing this procedure to the built-in btauto
tactic.
    We expect that our approach and results, such as the proof of soundness and
completeness and the cut elimination theorem, can be replicated to other similar
          Veriﬁed and Optimized Implementation of Orthologic Proof Search       133

logics, although they may not satisfy the key subformula property that yields
an algorithm that is both complete and polynomial. Moreover, our veriﬁcation
of optimization techniques for proof search using memoization and reference
equality are very general by nature and we expect our approach to generalize
well to other logics. All our tactics are available as a Coq plugin alongside with
benchmarks at
                   github.com/SimonGuilloud/orthologic-coq.

A permanent record is also available at

                        doi.org/10.5281/zenodo.15215613.


1.1   Contributions

In Sect. 2, we ﬁrst formalize in the Coq proof assistant a proof system for ortho-
logic (in the style of sequent calculus) and its soundness and completeness with
respect to truth in every ortholattice. In Sect. 3, we then formalize the cut elim-
ination theorem (without non-logical axioms) of orthologic, and in the process
discover a missing edge case in the proof of [12].
    In Sect. 4, we implement the proof-search-based decision procedure for ortho-
logic from [12]. We prove soundness and completeness of the algorithm. We
then use reﬂection to obtain a Coq proof tactic which can solve any equality
or inequality valid in orthologic, for any ortholattice, in particular the type bool
of truth values. In Sect. 5, we describe our implementation and veriﬁcation of
the memoized version of the algorithm. In Sect. 6, we discuss reference equal-
ity. This optimization is signiﬁcantly more complex. It requires redeﬁning trees
representing orthologic terms to include pointers and proving that the trans-
formation from pointer-free terms to terms with pointers is correct, which was
surprisingly diﬃcult.
    In Sect. 7, we present an alternative tactic that directly produces proof terms
instead of using reﬂection, which is faster in practice but less space eﬃcient. We
also implement tactics for OL-normalization and an orthologic-based boolean
solver.
    In Sect. 8, we present a series of benchmarks which are supposed to hit the
asymptotic worst case of every implementation of the proof search procedure,
using diﬀerent reduction strategies, and ﬁnd that the resulting curves match the
theoretical complexity. We then present benchmarks comparing our OL-based
boolean validity tactic to the built-in btauto tactic of Coq on random formulas
generated according to [19].

1.2   Related Work

The word problem for ortholattices (deciding if given two terms, one is always
≤ than the other) was ﬁrst solved by [4], extended in [9] to obtain normal forms
of terms. A similar proof system for orthologic, with the property that sequents
134     S. Guilloud and C. Pit-Claudel

never contain more than one formula, was already described by [20]. Diﬀerent
proof systems have also been considered [15–17].
     The authors of [5] formalize cut elimination for intuitionistic logic and those
of [7] formalze cut elimination for the logic of bunched implications in Coq, but
their approach is semantic rather than syntactic. [23], still using Coq, shows cut
elimination for a class of coalgebraic logics, including a variety of modal logics.
They propose both a syntactic and a semantic proof. In Isabelle, [25] formalizes
a particular, strongly normalizing version of cut elimination for classical ﬁrst
order logic.
     Whitman’s algorithm, a decision procedure for inequalities holding in every
lattice (without negation), has been formalized in Coq by [14], also using reﬂec-
tion. Reﬂection has also been used to verify and import proofs from SMT solvers
[2].
     Ortholattices have been deﬁned in Mizar [24], but little about them proven.
In Coq, [16] formalized results about a diﬀerent proof system for orthologic.
     Veriﬁed memoization has been studied in [26]. The authors propose a frame-
work for automatic veriﬁed memoization of programs in Isabelle/HOL. In Coq,
[3] studies the related topic of hash-consing, which can be seen as memoization
of constructors. In their approach, they entirely replace nodes of an ADT by
identiﬁers, so that the recursive structure only exist in the hash-consing map,
while we add identiﬁers to the tree.




2     Formalizing Ortholattices and Orthologic
We ﬁrst formalize the algebraic class of ortholattices as a typeclass (Listing 1.1).
Ortholattices are of course lattices, and in particular a partial order with ≤ given
by
                               x ≤ y ⇐⇒ x ∧ y = x
or equivalently
                              x ≤ y ⇐⇒ x ∨ y = y.
Ortholattices can be axiomatized equivalently as an algebraic variety, such as in
Table 1, or as a partial order.
         Veriﬁed and Optimized Implementation of Orthologic Proof Search      135

    We then implement using Ltac Whitman’s algorithm [6], a simple decision
procedure for lattices. This helps us to quickly show a number of useful lemmas
about ortholattices. This simple tactic is subsumed by the tactic for ortholat-
tices we will obtain with reﬂection. We then show that , under the axiom
                              , is a congruence relation for        and . This
makes ortholattices setoids, and enables the use of generalized rewriting [22].

Orthologic

We deﬁne in the standard way the type of ortholattice terms, and the evaluation
of a term in an arbitrary ortholattice:




    and then implement the OL proof system of [12] (without axioms), formulated
as a sequent calculus. One can think of this proof system as Gentzen’s sequent
calculus for classical logic [8] restricted to ensure that at any given point in a
proof, a sequent never has more than two formulas on both sides combined.
    We represent sequents as (ordered) pairs of annotated formulas as in [12]:




    where N represents no formula, L a formula on the left and R a formula on the
right. For example, (L φ, R ψ) stands for φ ψ in more conventional notation.
    We implement the proof system using dependent inductive types, so that the
correctness of a proof is guaranteed by construction, and no additional proof-
checking function is required. For example, the RightAnd rule from [12], is
                            Γ, φR       Γ, ψ R
                                                 RightAnd
                               Γ, (φ ∧ ψ)R
   and                      is                      encoded                    as
136      S. Guilloud and C. Pit-Claudel

   In [12], sequents are formally considered as sets. We have deﬁned them in
Coq using ordered pairs and hence need to deﬁne two additional rules, simulating
the set-like nature of sequents: the Swap and Contract rules.
                           Γ, Δ                   Γ, Γ
                                  Swap                    Contract
                           Δ, Γ                   Γ, N
   Soundness of the proof systems states that if a sequent is provable, then the
corresponding inequality must be true in every ortholattice (semantic truth),
and completeness is the converse. Both are straightforward to prove.


3     Cut Elimination for Orthologic
The key property of the orthologic proof system is that it admits cut elimination:
any provable sequent can be proved without using the cut rule. Cut elimination
has important theoretical and practical consequences. Since the |Cut| step is the
only one in which a term can appear in the premise but not the conclusion, cut
elimination implies the subformula property: if a sequent has a proof, then it
has a proof where only subterms of the conclusion appear. This is key to the
orthologic proof search procedure.




   This theorem is not straightforward to formalize. The paper proof starts with
“Consider the topmost instance of the cut rule in the proof”. This deceptively
short step requires a double induction, ﬁrst on the number of instances of the
cut rule appearing in a proof (fuelCut), then on the size of the proof (fuelSize)1 .
The corresponding lemma takes as arguments proofs that the given fuel is larger
than the metric it represents, and every induction step needs to justify that the
measures are decreasing. This step allows to reduce the problem to the case
where the proof ends with a single Cut step whose premises are cut-free.
   Graphically, we have the following situation:
                                   A               B
                                  Γ, bR          L
                                                 b ,Δ
                                                         Cut
                                          Γ, Δ
   and need to obtain the conclusion Γ, Δ with a cut-free proof. The proof again
works by double induction: ﬁrst on the size of the cut formula b (fuelB), then on
the total size of A and B (fuelSize), as expressed in the lemma’s statement:




1
    Two nested inductions on natural numbers is equivalent to transﬁnite induction on
    ω2 .
         Veriﬁed and Optimized Implementation of Orthologic Proof Search                137




   The proof proceeds by case analysis on A and B, and gives in each case
a speciﬁc transformation resulting in a cut-free proof of Γ, Δ. We provide two
examples to illustrate the process.


                  A                                               A             B
                 αL , bL                B                        αL , bL       bR , Δ
  Example 1.               RightNot                       →                           Cut
                ¬αR , bL               bR , Δ                           αL , Δ
                                                  Cut                            RightNot
                           ¬αR , Δ                                     ¬αR , Δ


                            A                        B           B
                          Γ, αR                     αL , Δ    βL, Δ
                                      RightOr                              LeftOr
                       Γ, (α ∨ β)R                    (α ∨ β)L , Δ
                                                                        Cut
                                          Γ, Δ
         Example 2.
                                                  →

                                       A                B
                                      Γ, αR            αL , Δ
                                                                Cut
                                                Γ, Δ
   Note that in both examples, the transformed proof contains instances of the
Cut rule. But since they have a smaller cut formula, by induction their conclusion
have cut-free proofs. Every single recursive use of the induction hypothesis has
to provide the required proof of decreasing measures corresponding to the fuel
properties.
   The main challenge of the proof comes from the sheer size of the case analysis:
the Swap step essentially duplicates every other proof step by allowing them to
act on the ﬁrst or second formula, which implies we have to analyse each of
A and B on 23 cases each, for a total of more than 500 cases. In practice, we
can ﬁrst do the analysis on A, and for some cases the proof is independent of
the structure of B, as in Example 1. However, there is no way to undo the case
analysis on A when conversely the cases of pattern matching on B have a proof
independent of the structure of A.
   Then, some combinations of cases are impossible. For example, it is not
possible for A to conclude with a RightAnd and B with LeftOr1, as the cut formula
138     S. Guilloud and C. Pit-Claudel

b would then need to be both a conjunction and a disjunction. Thanks to the
use of dependent types to deﬁne the proof system, those cases are automatically
eliminated. The paper proof can also aﬀord a lot of reasoning by symmetry.
There are particular combined symmetries between left and right rules, meet
and join, swapped and non-swapped cases, A and B, etc., which can easily be
informally treated in a paper proof but not in Coq. In the end, the formal proof
contains around 200 cases.
    Among these cases, we caught one in particular that was not properly con-
sidered in the paper proof of [12]. Indeed, the example reduction in Example 2
would fail in the presence of an implicit contraction due to set semantics. Written
with an explicit contraction, this is:
                                          B                    B
                 A                  αL , (α ∨ β)L       β L , (α ∨ β)L
                                                                         LeftOr
               Γ, αR                      (α ∨ β)L , (α ∨ β)L
                          RightOr                                  Contract
            Γ, (α ∨ β)R                       (α ∨ β)L , N
                                                             Cut
                                Γ, N
   And the transformation above would yield Γ, (α ∨ β)L instead of Γ, N , and
hence is not correct. In this case, a correct transformation is:
                                A
                              Γ, αR                         B
                                           RightOr
                A          Γ, (α ∨ β)R                 (α ∨ β)L , αL
                                                                         Cut
               Γ, αR                         αL , Γ
                                                      Cut
                              Γ, Γ
                                       Contract
                              Γ, N
   The topmost cut is justiﬁed by induction because its proof is smaller. The
second, however, is not: after recursive elimination from the cut above, we cannot
guarantee that the new proof is smaller. Instead, this cut needs to be justiﬁed
by outer induction on the size of the cut formula.


4     Decision Procedure for Orthologic
The word problem for ortholattices consists in deciding, for arbitrary terms s and
t over (∧, ∨, ¬), if s = t in all ortholattices. Cases of particular interest involve
deciding if s = 1 (validity) or s = 0 (unsatisﬁability). Since s = t ⇐⇒ s ≤ t
& t ≤ s, and vice-versa s ≤ t ⇐⇒ s = s ∧ t, we can equivalently see the
word problem as deciding inequality between arbitrary words. By soundness
and completeness of the orthologic proof system, this is in turn equivalent to
deciding if the sequent sL , tR has a proof.
    This is decidable with a recursive backward proof search procedure, as in [12]:
given a sequent Γ, Δ, try to apply all the rules which can conclude with Γ, Δ, and
recursively solve the premise. Since orthologic admits cut elimination, we never
need to consider the Cut step. Moreover, because the orthologic proof system
         Veriﬁed and Optimized Implementation of Orthologic Proof Search      139

admits the subformula property, we also know that the depth of a proof of a
sequent of size n will never exceed 4n2 . We implement this proof search procedure
as a Coq function in Listing 1.2, and show soundness and completeness of the
proof system with respect to validity in all ortholattices.
   The soundness of this algorithm, which is required for obtaining a reﬂection
tactic, is expressed as




Reflection

Suppose we have a goal s ≤ t or s = t, where s and t are expressions in an
arbitrary ortholattice, for example:
140       S. Guilloud and C. Pit-Claudel

    We want to solve this problem by executing the above algorithm, which we
proved correct. First, we split s = t in two independent inequalities. Then, reﬂec-
tion consists in two separate steps: reification and evaluation (or type checking).
    Reiﬁcation consists in ﬁnding two terms s’ and t’ as well as a function
                      2
                        such that eval s’ f is convertible to s and eval t’ f is con-
vertible to t. Here, convertible means that the two expressions are equivalent
up to βα conversion, unfolding of deﬁnitions, and additional relations deﬁned
by Coq3 . In particular, any expression can always be freely replaced by one it
is convertible to, without additional proof. Hence, the inequality in the goal is
convertible to (and can be changed to):




    We can then apply a lemma derived from the soundness of the decision
procedure with respect to the proof system, and of the proof system with respect
to the class of ortholattices to reduce the problem to:




      Now, we can complete this proof using the term eq_refl bool true : (true =
true), which is by deﬁnition a proof of true = true. For this to typecheck, the left-
hand side of the equality needs to be convertible to true. Hence to typecheck the
proof, Coq evaluates the algorithm. Eﬀectively, we have oﬄoaded the burden of
proof to the evaluator inside Coq’s kernel. Note also that the proof has constant
size.
    We now describe how to ﬁnd a suitable f in our reiﬁcation process,
which is implemented in its own tactic. First, put all the leaves of s and
t in a list named env. A leaf is a subexpression that is neither a meet, a
join or a negation. These leaves will correspond to variables in s’ and t’.
f is then the function that maps n to the element in the list at place n.
The reiﬁcation tactic then uses this list to compute the terms s’ and t’.
We mechanize the entire process as the tactic solveOL, solving, for example:




Note on Soundness and Completeness. An error of implementation in a decision
procedure can take two forms: soundness (incorrectly accepting a wrong equal-
ity) and completeness (incorrectly rejecting a correct equality). However, Coq’s
logical kernel guarantees the soundness of every tactic. In the process above,
the decision algorithm is proven sound. However, the reiﬁcation process is not
2
    In general,                  , where OL is the ortholattice in which the terms live.
3
    See https://rocq-prover.org/doc/v8.18/refman/language/core/conversion.html.
           Veriﬁed and Optimized Implementation of Orthologic Proof Search       141

(and it cannot be), so it may contain errors and produce incorrect terms. In that
case however, Coq’s kernel will refuse to replace the goal and produce an error
message.


5    Verified Memoization
The naively implemented proof search procedure has superexponential runtime
complexity, making it unusable in practice. We need to optimize it. First, observe
that some proof steps, when applied backward, are not merely suﬃcient condi-
tions but also necessary. For example, consider a sequent of the form Γ, (φ1 ∧φ2 )L .
It is a theorem of lattices that s ≤ t1 ∧ t2 ⇐⇒ s ≤ t1 & s ≤ t2 , corresponding
to the RightAnd step. Hence, for Γ, (s ∧ t)R to have a proof, it is not only suﬃ-
cient but also necessary that both Γ, sR and Γ, tR have a proof. It follows that
if RightAnd is applicable, we do not need to try other steps, and similarly with
LeftOr, Hyp, RightNot and LeftNot. Moreover, note that the algorithm will naively
try to apply the Swap rule over and over. This makes the algorithm structurally
non-terminating, and only fuel prevents inﬁnite loops. This can be prevented by
“unfolding” the swap step, and ensuring that a meaningful rule is always applied,
but loops also are possible using the Contract and Weaken rules. To handle this
situation, we add two boolean variables to the input of the algorithm, each one
denoting respectively weather g N and N d have already been tried. We imple-
ment a second version of the algorithm, named decideOL_opti implementing these
optimizations:




    We prove its soundness and implement a corresponding reﬂection tactic
solve_OL_opti.
                                                              2
   The algorithm still has an exponential runtime of O(2n ). To obtain a poly-
nomial time procedure, we need to implement memoization. Observe that since
orthologic admits cut elimination, it also admits the subformula property:

Theorem 1. (Subformula Property, [12]). If an orthologic sequent Γ, Δ has
a proof, then it has a proof where only subformulas of Γ and Δ appear.

    Let n be the size of the input sequent, i.e. the number of subformulas. The
number of subformulas of the initial input sequent is O(n), and there can only
exist at most O(n2 ) diﬀerent sequents built from these subformulas. Hence, in
a full run of decideOL_bool, there can only be at most O(n2 ) unique recursive
calls. Using memoization, we can ensure that the body of the program is never
executed more than O(n2 ) times. Note that we also need to memoize the two
boolean ﬂags cg and cd, but this only multiplies the number of input by 4.
142      S. Guilloud and C. Pit-Claudel

    We implement this version of the algorithm using the state monad
paradigm. Let MemoMap be some type of maps with keys in (AnTerm * AnTerm)
and values in bool. The function decideOL_memo then returns an object of type
                           . Boolean conjunctions and disjunctions are modiﬁed
to compute the results in series, as in:




and the decision algorithm is modiﬁed as follows:




    The correctness of the algorithm is expressed as equivalence with the non-
memoized version of the algorithm, and relative to the correctness of the map
given as input. A map is correct if and only if for every key k with a value of
true, the non-memoized version of the algorithm returns true on k.




In particular, the empty map is correct. Note that the two versions of the
algorithm are not necessarily equivalent for an arbitrary allowance of fuel: the
memoized version might require less. We prove the soundness of the memoized
algorithm4 :




4
    Note that completeness is not required to deﬁne a reﬂection-based tactic.
          Veriﬁed and Optimized Implementation of Orthologic Proof Search      143

    The induction has to be performed jointly on the statement that the returned
map is correct, and that the returned truth value is the same as that of the
original algorithm. The proof again proceeds with a large case analysis, which
required signiﬁcant custom automation and side lemmas about the monadic
structure of the memoization, but was carried completely independently of the
orthologic proof system and would work similarly with any other recursive algo-
rithm on algebraic datatypes.
    We ﬁrst implement the algorithm using a list of pairs as a base for the
memoization map. However, lookup inside a list takes time linear in its size.
As explained above, the number of stored values is quadratic in the size of the
input. Moreover, checking equality between the input and the elements of the
list costs an additional linear factor. Overall, the complexity of lookup is cubic,
for a total runtime of O(n5 ).
    We then implement a second version, using AVL maps from the Coq standard
library. This requires to deﬁne a total order on anTerm, which we do following the
usual total order on labelled ordered trees. Sorted maps such as AVL maps only
require a logarithmic number of comparisons, down from quadratic with a list-
based implementation. However, comparison still takes linear time, for a total
time complexity of O(n3 log n).
    We hence obtain two more versions of the algorithm, decideOL_memo and
decideOL_fmap, and two corresponding tactics solveOL_memo and solveOL_fmap.




6   Reference Equality

Lookup in a map requires deciding either equality or ordering between two terms,
which takes linear time in the size of the terms and even in a Hashmap, equality
checking is necessary to avoid collisions. In the previous two algorithms, either
based on lists or on AVL maps, equality is structural: two terms are equal if they
have the same constructor and recursively their arguments are equal. However,
this is too strong for memoization.
    First, observe that if we replace this notion of equality by a strictly weaker
relation, the algorithm is still sound, and we only risk losing some of the beneﬁts
of memoization.
    Then recall that by the subformula property, the algorithm only ever sees
the O(n2 ) diﬀerent subnodes of the original input. Assigning a diﬀerent binary
identiﬁer to each of these nodes requires only O(log n) bits for each identiﬁer.
Then, if two terms have the same identiﬁer, they must be structurally equal.
However, the converse does not hold in general: if the original input contains
multiple copies of the same subtree, they will be assigned diﬀerent identiﬁers.
    This corresponds, in imperative programming, to pointer equality. Checking
if two objects have the same location in memory is a sound approximation to
deciding if they are structurally equal. Formally, we deﬁned an extended version
of the datatype of terms:
144     S. Guilloud and C. Pit-Claudel




   where Pointer := positive is the type of binary positive numbers. We deﬁne
the projection onto regular terms                                        and a
getter                                       as expected. We extend pointers to
annotated pointers:




    and TermPointer to AnTermPointer similarly. For g an AnTermPointer (that is, a term
with a pointer and a left or right annotation), we denote [[g]] its corresponding
AnPointer. We again use AVL maps, but this time with keys being pairs of AnPointer.
The algorithm is modiﬁed accordingly:




    As a reminder, fuel is an accessory argument ensuring termination, g and d
are the actual input formulas augmented with pointers, cg and cd are ﬂags used to
prevent loops and memo is the memoization map. In practice, we deﬁne a separate
function decideOL_pointers_simp g d, setting initial fuel to (|g| + |d|)2 , cg and cd to
false, memo to the empty map and computing the pointers for g and d.
    The correctness of the algorithm of course depends on how pointers are
assigned. If two diﬀerent terms are assigned the same pointer, the algorithm
will not be correct. Formally, GetPointer must be injective on the domain of all
subterms of the input. In the correctness theorem, it is convenient to express
this condition as the existence of a function                                    , corre-
sponding to address lookup, which is left and right inverse to GetPointer on all
subterms of the input.
    Proving the correctness of the algorithm extends with moderate eﬀort from
the previous algorithm with some additional side lemmas and boilerplate. How-
          Veriﬁed and Optimized Implementation of Orthologic Proof Search      145

ever, showing that the pointer assignment is correct is signiﬁcantly more chal-
lenging. We deﬁne a function add_pointer assigning pointers with depth-ﬁrst, pre-
order traversal of the syntactic tree, such as in Example 3.
Example 3. The following trees represent the formula ¬(x ∧ ¬y) as respectively
a Term and the corresponding TermPointer.
                      ¬                                  ¬, 1

                      ∧                                  ∧, 2

                 x          ¬                     x, 3          ¬, 4

                            y                                   y, 5
                     Term                           TermPointer



    To construct the required inverse function, we ﬁrst compute the list of sub-
terms of a term, and map a pointer to the ﬁrst term of the list with this pointer.
It seems very obvious from the deﬁnition of our pointer assignment function
add_pointer that there exists only one such term and hence that the two func-
tions are inverse of each other, yet this was surprisingly diﬃcult to prove, and
required a lot of intermediate lemmas about the structure of subterms, the mono-
tonicity of add_pointer along subterms, correspondence between the pointer and
non-pointer version of terms, etc. The development is however independent of
the orthologic proof system, and only depends upon the number and arity of
constructors of orthologic terms. Hence, the theorems can straightforwardly be
transfered to any other algebraic datatypes.


7   Proof-Producing Tactics and Validity Solvers
An alternative to veriﬁed decision procedures is proof-producing decision pro-
cedures, which also allows to implement tactics for proof assistants. Instead of
relying on a soundness theorem, a proof-producing tactic will compute a proof
(in Coq, a proof term) that is then checked by the logical kernel.
    We implement a proof-producing version of the proof search algorithm of [12]
in OCaml, and make it available as a Coq tactic, which we refer to as olcert_goal.
In theory, this should be less eﬃcient, as producing a proof takes additional
time, but in practice an OCaml implementation (leveraging, in particular, muta-
bility) is a faster computation method than reducing lambda-terms. Compared
to solveOL_pointer, it has the additional practical advantage of persistence of its
memoization across calls, as the pointers are assigned once and memoization is
maintained globaly. Moreover, when possible, we memoize results as ﬁelds of the
term nodes rather than in a map, making retrieval more eﬃcient.
146      S. Guilloud and C. Pit-Claudel

    On the other hand, the proof term produced has size up to O(n2 ), while the
proof term of solveOL_pointer has constant size. Moreover, the proof-producing
tactic is not veriﬁed, so it is not guaranteed that it does not contain a bug and
outputs an incorrect proof. In fact, because Coq’s logic is rather complex and its
inner workings hard to work with (and sparsely documented), it is quite unlikely
that our implementation does not have issues with edge cases, for example involv-
ing universes or uniﬁcation variables. This is less likely with reﬂection-based
tactic, where only the reiﬁcation step is sensible to such issues.
    We then develop a tactic olnormalize, a tactic to normalize OL terms accord-
ing to [9]. An OCaml algorithm computes the normal form f of a formula f ,
and we then use either solveOL_pointer or olcert_goal to prove f = f . We believe
this tactic has the most impact for automation, as [9] demonstrated it can sig-
niﬁcantly reduce the size of formulas in practical contexts. For example in the
ﬁrst benchmark of next section, the goal is not an OL tautology, but olnormalize
signiﬁcantly simpliﬁes it.




    Finally, we use the olnormalize tactic as basis for a complete tactic for Boolean
equality (i.e. validity). This tactic is similar to the DPLL algorithm: it recursively
branches on a literal and simpliﬁes the result. The simpliﬁcation is performed
using olnormalize. We implement two versions of this tactic, one named oltauto
which uses the reﬂexive orthologic tactic and one named oltauto_cert, which uses
the proof-producing orthologic tactic. Figure 1 presents an overview of the dif-
ferent components and their relations to each other.


8     Evaluation of Resulting Tactics
Evaluation of the OL Proof Search Tactics. The implementations of the previous
section yield six algorithms and corresponding proof tactics for deciding equality
in orthologic, each with diﬀerent time complexity5 :
                      n
–   solveOL ("OL", O(2    ))
                               n
–   solve_OL_opti ("OL+o", O(2     ))
                                   5
–   solve_OL_memo ("OL+o+l", O(n        ))
5
    Exact complexity of algorithms up to logarithmic factors depends on the precise
    model of computation; for simplicity, the algorithmic complexity below assume the
    usual Word RAM model, where checking equality of words takes constant time, even
    though this does not precisely match Coq’s evaluation of terms.
           Veriﬁed and Optimized Implementation of Orthologic Proof Search      147

                                   3
–   solve_OL_fmap ("OL+o+m", O(n  ))
                                      2
–   solve_OL_pointers ("OL+o+m+φ", O(n ))
                              2
–   olcert_goal ("OCaml", O(n ))


The diﬀerence of complexity is not only theoretical, but also highly observable
in practice. Consider the family of propositions

                      (x1 ||x2 )&&(x3 ||x4 )&&...&&(xn−1 ||xn )

                     = (x2 ||x1 )&&(x4 ||x3 )&&...&&(xn ||xn−1 )
These equalities are solvable by the laws of ortholattices. Table 2 shows the time
taken by each implementation for n = 30. For comparison, we also include the
runtime of btauto, the solver for boolean equalities included in Coq’s standard
distribution.




Fig. 1. Diagram illustrating the interaction between each algorithm and tactic. Ele-
ments in bold have been benchmarked.


    To conﬁrm the scaling characteristics of our implementation variants, we
solved the family of equalities above for sizes ranging from 2 to 100 variables.
148       S. Guilloud and C. Pit-Claudel

      Table 2. Wall clock time required to prove an equality involving 30 variables.

                                solver        mean std
                                btauto        35.96 13.30
                                OL+o+l        19.89 0.26
                                OL+o+m        0.36 0.01
                                OL+o+m+φ 0.25 0.01
                                OCaml         0.12 0.00




Fig. 2. Wall clock time required to prove a family of equalities with sizes ranging from
2 to 100 variables. Shaded regions indicate 95% conﬁdence intervals. Colours indicate
which implementation was used. Benchmarks were run on an Intel Core i7-1365U CPU
with 32 GB RAM.


Figure 2 shows our results. We conﬁrm the theoretical complexity by verifying
for each tactic that a polynomial of the right degree ﬁts the measurements.
    The proof-producing implementation in OCaml outperforms the implemen-
tation as a Coq function (i.e. in Gallina), but it produces longer proof terms,
and since its soundness is not proven it may contain bugs. But it also demon-
strates the inadequacy of algorithms implemented directly in Coq for practical
purposes, as reduction of lambda-terms is not an eﬃcient computational strat-
egy. This suggests that in an ideal world, it should be possible to verify functions
implemented in a general-purpose programming language and then trust their
output, so that they can run as fast as possible. This was done in some ﬂavour
with the Candle proof assistant (a veriﬁed implementation of HOL Light) in [1].

Evaluating Propositional Solvers. To judge the tactics oltauto and oltauto_cert
compared to the standard btauto solver, we generate a series of formulas according
to the techniques of [19]. These formulas have a ﬁxed structure and are believed
          Veriﬁed and Optimized Implementation of Orthologic Proof Search      149

to be typically hard for SAT solvers. Some of the formulas we generated are
valid and some are not, but this does not aﬀect the runtime meaningfully as all
three algorithms do not stop early if a dissatisfying assignment is found and still
explore the entire search space. We generate a total of 80 random formulas, with
up to 20 diﬀerent variables and 192 literals, and a timeout of 30 s. The results
appear in Fig. 3 and show that oltauto_cert (OCaml+n) consistently outperforms
oltauto (OLT), which in turn consistently outperforms btauto, which scales very
poorly with respect to formula size even with a low number of variables (<6).




Fig. 3. Wall clock time required to prove random hard non-clausal formulas. Each
point is an experiment and indicates the running time for two of the three solvers.




9   Conclusion
We formalized orthologic in the Coq proof assistant, including soundness and
completeness of orthologic sequent calculus with respect to the class of all ortho-
lattices and the cut elimination theorem for orthologic. Doing so, we discovered
a missing edge case in the proof from [12].
    We implemented and veriﬁed a proof search procedure for orthologic, and
used reﬂection to obtain a proof tactic that decides equalities and inequalities in
150     S. Guilloud and C. Pit-Claudel

ortholattices. We improved the algorithm with important but typically imper-
ative programming features: memoization and pointer equality, improving the
algorithm from exponential to quadratic. We implemented additional special-
ized tactics enabling orthologic-based reasoning for Coq users, all of which are
available in a Coq plugin.
    Orthologic is used as a core component of reasoning tools, and the formaliza-
tion of its key properties increases the trust we can have in existing and future
such systems. Our work also opens for further mechanization of orthologic-based
reasoning, such as orthologic with axioms and eﬀectively propositional orthologic
[12], interpolation in orthologic [11, 18], and more [4, 13, 21].
    Finally, veriﬁcation of memoization and reference equality-based optimiza-
tions, which represents a signiﬁcant part of the formalization eﬀort, is in no
way speciﬁc to orthologic proof search. These techniques are also of great prac-
tical relevance, and necessary to obtain optimal complexity of a wide range of
algorithms. We expect that our formalization can be a useful source to anyone
verifying eﬃcient algorithms relying on memoization or reference equality in the
future.

Acknowledgements. We thank the anonymous reviewers for their useful suggestions
and feedback.
    The authors have no competing interests to declare that are relevant to the content
of this article.



References
 1. Abrahamsson, O., Myreen, M.O.: Fast, veriﬁed computation for candle. In: Nau-
    mowicz, A., Thiemann, R. (eds.) 14th International Conference on Interactive
    Theorem Proving (ITP 2023). Leibniz International Proceedings in Informatics
    (LIPIcs), vol. 268, pp. 4:1–4:17. Schloss Dagstuhl – Leibniz-Zentrum für Infor-
    matik, Dagstuhl, Germany (2023). https://doi.org/10.4230/LIPIcs.ITP.2023.4
 2. Besson, F., Cornilleau, P.-E., Pichardie, D.: Modular SMT proofs for fast reﬂexive
    checking inside Coq. In: First International Conference on Certiﬁed Programs and
    Proofs, Kenting, Taiwan (2011)
 3. Braibant, T., Jourdan, J.-H., Monniaux, D.: Implementing and reasoning about
    Hash-consed data structures in Coq. J. Autom. Reason. 53(3), 271–304 (2014).
    https://doi.org/10.1007/s10817-014-9306-0
 4. Bruns, G.: Free ortholattices. Can. J. Math. 28(5), 977–985 (1976). https://doi.
    org/10.4153/CJM-1976-095-6
 5. Forster, Y., Kirst, D., Wehr, D.: Completeness theorems for ﬁrst-order logic anal-
    ysed in constructive type theory: extended version. J. Log. Comput. 31(1), 112–151
    (2021). https://doi.org/10.1093/logcom/exaa073
 6. Freese, R., Jezek, J., Nation, J.: Free Lattices. Mathematical Surveys and Mono-
    graphs, vol. 42. American Mathematical Society, Providence, Rhode Island, March
    1995. https://doi.org/10.1090/surv/042
          Veriﬁed and Optimized Implementation of Orthologic Proof Search          151

 7. Frumin, D.: Semantic cut elimination for the logic of bunched implications, formal-
    ized in Coq, December 2021. arXiv:2112.05515. https://doi.org/10.48550/arXiv.
    2112.05515
 8. Gentzen, G.: Untersuchungen über das logische Schließen I. Math. Z. 39, 176–210
    (1935)
 9. Guilloud, S., Bucev, M., Milovancevic, D., Kuncak, V.: Formula normalizations
    in veriﬁcation. In: 35th International Conference on Computer Aided Veriﬁcation,
    Paris, LNCS, pp. 398–422. Springer, Cham (2023)
10. Guilloud, S., Gambhir, S., Kuncak, V.: LISA – a modern proof system. In: 14th
    Conference on Interactive Theorem Proving, Leibniz International Proceedings in
    Informatics, pp. 17:1–17:19. Daghstuhl, Bialystok (2023)
11. Guilloud, S., Gambhir, S., Kunčak, V.: Interpolation and quantiﬁers in ortholat-
    tices. In: Veriﬁcation, Model Checking, and Abstract Interpretation: 25th Interna-
    tional Conference, VMCAI 2024, London, United Kingdom, 15–16 January 2024,
    Proceedings, Part I, pp. 235–257. Springer, Heidelberg (2024). https://doi.org/10.
    1007/978-3-031-50524-9_11
12. Guilloud, S., Kunčak, V.: Orthologic with axioms. Proc. ACM Programm. Lang.
    8(POPL), 39:1150–39:1178 (2024). https://doi.org/10.1145/3632881
13. Herrmann, C., Roddy, M.S.: On varieties of modular ortholattices which are gen-
    erated by their ﬁnite-dimensional members, p. 9 (2014)
14. James, D.W.H., Hinze, R.: A reﬂection-based proof tactic for lattices in Coq. In:
    Symposium on Trends in Functional Programming (2009)
15. Kawano, T.: Labeled sequent calculus for orthologic. Bull. Sect. Logic 47(4), 217–
    232 (2018). https://doi.org/10.18778/0138-0680.47.4.01
16. Laurent, O.: Focusing in orthologic. In: Kesner, D., Pientka, B. (eds.) 1st Inter-
    national Conference on Formal Structures for Computation and Deduction, FSCD
    2016, 22–26 June 2016, Porto, Portugal. LIPIcs, vol. 52, pp. 25:1–25:17. Schloss
    Dagstuhl - Leibniz-Zentrum für Informatik, Porto, Portugal (2016). https://doi.
    org/10.4230/LIPIcs.FSCD.2016.25
17. Meinander, A.: A solution of the uniform word problem for ortholattices.
    Math. Struct. Comput. Sci. 20(4), 625–638 (2010). https://doi.org/10.1017/
    S0960129510000125
18. Miyazaki, Y.: Some properties of orthologics. Studia Logica Int. J. Symbolic Logic
    80(1), 75–93 (2005). arXiv:2001.6705
19. Navarro, J.A., Voronkov, A.: Generation of hard non-clausal random satisﬁability
    problems. In: Proceedings of the 20th National Conference on Artiﬁcial Intelligence
    - Volume 1, AAAI 2005, pp. 436–442. AAAI Press, Pittsburgh, Pennsylvania, July
    2005
20. Mönting, J.S.: Cut elimination and word problems for varieties of lattices. Algebra
    Universalis 12(1), 290–321 (1981). https://doi.org/10.1007/BF02483891
21. Sherif, M.: Decision problem for orthomodular lattices. Algebra Universalis 37(1),
    70–76 (1997). https://doi.org/10.1007/PL00000328
22. Sozeau, M.: A new look at generalized rewriting in type theory. J. Formalized
    Reasoning 2(1), 41–62 (2009). https://doi.org/10.6092/issn.1972-5787/1574
23. Tews, H.: Formalizing cut elimination of coalgebraic logics in Coq. In: Galmiche,
    D., Larchey-Wendling, D. (eds.) TABLEAUX 2013. LNCS (LNAI), vol. 8123, pp.
    257–272. Springer, Heidelberg (2013). https://doi.org/10.1007/978-3-642-40537-
    2_22
24. Truszkowska, W., Grabowski, A.: On the two short axiomatizations of ortholattices
    (2003)
152     S. Guilloud and C. Pit-Claudel

25. Urban, C., Zhu, B.: Revisiting cut-elimination: one diﬃcult proof is really a proof.
    In: Voronkov, A. (ed.) RTA 2008. LNCS, vol. 5117, pp. 409–424. Springer, Heidel-
    berg (2008). https://doi.org/10.1007/978-3-540-70590-1_28
26. Wimmer, S., Hu, S., Nipkow, T.: Veriﬁed memoization and dynamic programming.
    In: Avigad, J., Mahboubi, A. (eds.) ITP 2018. LNCS, vol. 10895, pp. 579–596.
    Springer, Cham (2018). https://doi.org/10.1007/978-3-319-94821-8_34




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
