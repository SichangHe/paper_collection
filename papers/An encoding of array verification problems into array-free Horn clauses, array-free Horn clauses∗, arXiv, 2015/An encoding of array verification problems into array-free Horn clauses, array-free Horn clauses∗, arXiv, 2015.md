                                             An encoding of array verification problems into
                                                        array-free Horn clauses∗
                                                                         David Monniaux
                                                        Univ. Grenoble Alpes, VERIMAG, F-38000 Grenoble
arXiv:1509.09092v1 [cs.PL] 30 Sep 2015




                                                            CNRS, VERIMAG, F-38000 Grenoble, France

                                                                          Laure Gonnord
                                                                      LIP, Univ. Lyon-1, France

                                                                            May 6, 2018


                                                                               Abstract
                                                   Automatically verifying safety properties of programs is hard, and it
                                               is even harder if the program acts upon arrays or other forms of maps.
                                               Many approaches exist for verifying programs operating upon Boolean
                                               and integer values (e.g. abstract interpretation, counterexample-guided
                                               abstraction refinement using interpolants), but transposing them to array
                                               properties has been fraught with difficulties.
                                                   In contrast to most preceding approaches, we do not introduce a new
                                               abstract domain or a new interpolation procedure for arrays. Instead, we
                                               generate an abstraction as a scalar problem and feed it to a preexisting
                                               solver, with tunable precision.
                                                   Our transformed problem is expressed using Horn clauses, a common
                                               format with clear and unambiguous logical semantics for verification prob-
                                               lems. An important characteristic of our encoding is that it creates a non-
                                               linear Horn problem, with tree unfoldings, even though following “flatly”
                                               the control-graph structure ordinarily yields a linear Horn problem, with
                                               linear unfoldings. That is, our encoding cannot be expressed by an en-
                                               coding into another control-flow graph problem, and truly leverages the
                                               capacity of the Horn clause format.
                                                   We illustrate our approach with a completely automated proof of the
                                               functional correctness of selection sort.


                                         1     Introduction
                                         Formal program verification, that is, proving that a given program behaves
                                         correctly according to specification in all circumstances, is difficult. Except for
                                         very restricted classes of programs and properties, it is an undecidable question.
                                         Yet, a variety of approaches have been developed over the last 40 years for
                                           ∗ The   research leading to these results has received funding from the
                                         European Research Council under the European Union’s Seventh Framework Programme
                                         (FP/2007-2013) / ERC Grant Agreement nr. 306595 “STATOR”.




                                                                                   1
automated or semi-automated verification, some of which have had industrial
impact.
    In this article, we consider programs operating over arrays, or, more gen-
erally, maps from an index type to a value type. (in the following, we shall
use “array” and “map” interchangeably). Such programs contain read (e.g.
v := a[i]) and write (a[i] := v) operations over arrays, as well as “scalar” oper-
ations.1

Universally quantified properties Very often, desirable properties over ar-
rays are universally quantified; e.g. sortedness may be expressed as ∀k1 , k2 k1 <
k2 =⇒ a[k1 ] ≤ a[k2 ]. However, formulas with universal quantification and
linear arithmetic over integers and at least one predicate symbol (a predicate
being a function to the Booleans) are so expressive that one can define the ex-
ecution of a Turing machine as a model to such a formula, whence this class is
undecidable [12]. Some decidable subclasses have however been identified [6].
    There is therefore no general algorithm for checking that such invariants
hold, let alone inferring them. Yet, there have been several approaches proposed
to infer such invariants (more on this in Section 7). In this article, we propose a
method for inferring such universally quantified invariants, given a specification
on the output of the program. Because of undecidability, this approach may fail
to terminate in the general case.
    Our approach is based on conversion to Horn clauses, a popular format
for program verification problems [25] supported by a number of tools. Most
conversions to Horn clauses map variables and operations from the program to
variables of the same type and the same operations in the Horn clause problem:2
an integer is mapped to an integer, an array to an array, etc. If some data types
are not supported by the back-end analysis, the variables of these types may be
discarded, at the expense of precision — thus if the back-end analysis does not
support arrays, array reads are abstracted as nondeterministic choices, array
writes are discarded, and scalar operations are mapped “as is”. In contrast, our
approach abstracts programs much less violently, with tunable precision, even
though the result still is a Horn clause problems without arrays. Section 3
explains how many properties (e.g. initialization) can be proved using one
“distinguished cell”, Section 4 explains how properties such as sortedness can
be proved using two of them; completely discarding arrays corresponds to using
zero of them.
    We illustrate this approach with an automated proof that the output of
selection sort is sorted: we apply Section 4 to obtain a system of Horn clauses
without arrays, which we feed to the Spacer solver, which produces a model of
this system, meaning that the sortedness postcondition truly holds. Note that
Spacer cannot, on its own, reason about universal properties on arrays.
    Previous approaches [21] using “distinguished cells” amounted (even though
they were not described as such) to linear Horn rules; on contrast, our abstract
semantics uses non-linear Horn rules, which leads to higher precision (Sec. 7.2).
   1 In the following, we shall lump as “scalar” operations all operations not involving the array

under consideration, e.g. i := i + 1. Any data types (integers, strings etc.) are supported
provided that they are supported by the back-end solver.
   2 With the exception of pointers and references, which need special handling and may be

internally converted to array accesses.




                                                2
Multiset of contents It is often necessary to reason not only about individual
elements of an array or map, but also about its contents as a whole: e.g. sorting
algorithms preserve the contents of the array (even though, locally, when moving
elements around, they may break this invariant).
    The multiset of the contents of an array of elements of type β is a map from β
to N. Using that remark, we can abstract the array both using our “distinguish
cell” approach and as the multiset of its elements (Sec. 5.2); we provide suitable
program transformations.
    We illustrate that approach with an automated proof that the output of
selection sort has the same contents as its input (that is, the output is a per-
mutation of the input).

Contributions Our main contribution is a system of rules for transforming
the atomic program statements in a program operating over arrays or maps, as
well as (optionally) the universally quantified postcondition to prove, into a sys-
tem of non-linear Horn clauses over scalar variables only, with tunable precision.
Statements operating over non-arrays variables are mapped (almost) identically
to their concrete semantics. This system over-approximates the behavior of the
program. A solution of that system can be mapped to inductive invariants over
the original programs, including universally properties over arrays.
    A second contribution, based upon the first, is a system of rules of the same
kind that also keeps tracks of array/map contents.
    We illustrate both these systems with automated proofs of functional cor-
rectness of array initialization, array reversal and selection sort. For each of
these proofs, we simply apply our transformation rules and apply a third-party
solver for Horn clauses over scalars. We also show the user can optionally help
the solver converge faster by supplying partial invariants.
    A third contribution is a counterexample reconstruction scheme (Sec. 6), if
the property to prove is actually false.


2    Program Verification as solving Horn clauses
A classical approach to program analysis is to consider a program as a control-
flow graph and to attach to each vertex pi (control point) an inductive invariant
Ii : a set of possible values x of the program variables (and memory stack and
heap, as needed) so that i) the set associated to the initial control point pi0
contains the possible initialization values Si0 ii) for each edge pi →c pj , the
set Ij associated to the target control point pj should include all the states
reachable from the states in the set Ii associated to the source control point
pi according to the transition relation τi,j of the edge. Inductiveness is thus
defined by Horn clauses:

                                  ∀x, x ∈ Si0 =⇒ x ∈ Ii0                         (1)
                  ∀x, x′ x ∈ Ii ∧ (x, x′ ) ∈ τi,j =⇒ x′ ∈ Ij                     (2)

    For proving safety properties, in addition to inductiveness, one requires that
error locations pe1 , . . . , pen are proved to be unreachable (the associated set of
states is empty): this amounts to Horn clauses implying false (⊥): ∀x, x ∈
Iei =⇒ ⊥.


                                         3
                                   exit

                                      i≥n          j := j + 2
                          i := 0
                          j := 1
                  init             loop            incr i                incr j
                                          i<n               i := i + 1


                  Figure 1: The control-flow graph for Program 1


    Various tools can solve such systems of Horn clauses, that is, can synthesize
suitable predicates Ii , which constitute inductive invariants. In this article, we
tried Z33 with the PDR fixed point solver [14], Z3 with the Spacer solver
[17, 16],4 and Eldarica5 [26].6 Since program verification is undecidable, such
tools, in general, may fail to terminate, or may return “unknown”.
    For the sake of simplicity, we shall consider, in this article, that all integer
variables in programs are mathematical integers (Z) as opposed to machine
integers.7 In our semantics, we consider that reads from out-of-range locations
(array index out of bounds, buffer overflows) stop the execution of the program
immediately, but that a write to a location makes this location defined. Again,
it is easy to modify our semantics to include systematic array bound checks,
jumps to error conditions, etc.
    In examples, instead of writing Istmt for the name of the predicate (inductive
invariant) at statement stmt, we shall write stmt directly, for readability’s sake:
thus we write e.g. loop for a predicate at the head of a loop.
Example 1. Consider the following program

                         Listing 1: A simple loop without arrays
int loop ij ( int n) {
  int i = 0 , j = 1;
  while ( i < n ) {
    i = i + 1;
    j = j + 2;
  }
}
   Its semantics gets encoded into Horn rules as predicates over triples (n, i, j),
one predicate for each node of the control-flow graph in Figure 1:

                                                      ∀n ∈ Z loop(n, 0, 1)                  (3)
   3 https://github.com/Z3Prover
   4 https://bitbucket.org/spacer/code
   5 https://github.com/uuverifiers/eldarica
   6 This list is not exhaustive; we apologize to authors of other tools. Neither did we conduct

systematic comparisons between these three tools, which each have numerous configuration
options: for our purposes, it sufficed that at least one concluded within reasonable time that
our property was proved.
   7 A classical approach is to add overflow checks to the intermediate representation of pro-

grams in order to be able to express their semantics with mathematical integers even though
they operate over machine integers.


                                               4
                  ∀n, i, j ∈ Z loop(n, i, j) ∧ i < n =⇒ incr i (n, i, j)                 (4)
                    ∀n, i, j ∈ Z loop(n, i, j) ∧ i ≥ n =⇒ exit(n, i, j)                  (5)
                     ∀n, i, j ∈ Z incr i (n, i, j) =⇒ incr j (n, i + 1, j)               (6)
                       ∀n, i, j ∈ Z incr j (n, i, j) =⇒ loop(n, i, j + 2)                (7)

   If we wish to prove that, at the end of the program, n ≥ 0 =⇒ i = n, we
add the Horn query

                      ∀n, i, j ∈ Z exit(n, i, j) ∧ n ≥ 0 =⇒ i = n                        (8)

Spacer and Z3/PDR then answer “satisfiable” after synthesizing suitable
predicates loop, incr i etc. satisfying the Horn system — otherwise said, in-
ductive invariants implying the postcondition 8.
   If we had made the mistake of forgetting that i = n holds finally only for
n ≥ 0, we would have written the query as

                            ∀n, i, j ∈ Z exit(n, i, j) =⇒ i = n                          (9)

and these solvers would have answered “unsatisfiable”.8
   Let us now try proving that n ≥ 0 ⇒ j ≤ 2 + 3n holds finally:

                   ∀n, i, j ∈ Z exit (n, i, j) ∧ n ≥ 0 =⇒ j ≤ 2 + 3n                    (10)

While Spacer answers instantaneously, Z3/PDR seems to enter a neverending
sequence of refinements.
    For reasons of efficiency of the back-end solver, it may be desirable to have
fewer predicates. It is possible to automatically simplify the system of Horn rules
by coalescing several rules together: for instance, if we have ∀x, y, I1 (x, y) ⇒
I2 (x + 1, y) and ∀y, z, I2 (x, y) ⇒ I3 (x, y + 2), and I2 does not occur elsewhere,
then we can remove I2 and use a single rule ∀x, y, I1 (x, y) =⇒ I3 (x + 1, y + 2).
Similarly, if in the antecedent of a Horn rule we have an equality x = e where e
is an expression and x is universally quantified in the rule, then we can remove
this variable and replace it with e in the rest of the rule. We shall often apply
such syntactic simplifications to make examples shorter and more readable.
    The flat encoding of the program described by initialization (Formulas 1)
and inductiveness (Formulas 2), following the control-flow graph (CFG), results
in a linear system of Horn clauses, in the sense that if one “unfolds” the system
by repeatedly rewriting the right-hand sides of implications l1 ∧ · · · ∧ ln =⇒ r
into their left-hand side in the rest of the Horn clauses, one gets a list, not a
tree structure.
Example 2. Consider the program:

                                   Listing 2: 1D array fill
void a r r a y f i l l 1 ( i n t n , i n t a [ n ] ) {
  int i = 0;
  while ( i < n ) {
   8 Horn clause solvers based on counterexample-based refinement are rather good at handling

disjunctions (here, n < 0 vs n ≥ 0). Tools based on convex domains, such as polyhedra, may
have more difficulties.



                                                5
                    start        init                loop           end
                                        n>0                   i≥n
                                        i := 0

                                                 i<n
                                                 a[i] := 42
                                                 i := i + 1


                Figure 2: Compact control-flow graph for Program 2


        a [ i ] = 42;
        i = i +1;
    }
}
We would like to prove that this program truly fills array a[] with value 42. The
flat encoding into Horn clauses assigns a predicate (set of states) to each of the
control nodes (Fig. 2), and turns each transition into a Horn rule:

                  ∀n ∈ Z ∀a ∈ Array (Z, Z) n > 0 =⇒ loop(n, 0, a)              (11)
                        ∀n, i ∈ Z ∀a ∈ Array (Z, Z) i < n ∧ loop(n, i, a)
                                                                               (12)
                                       =⇒ loop(n, i + 1, store(a, i, 42))

                        ∀n, i ∈ Z ∀a ∈ Array (Z, Z) i ≥ n ∧ loop(n, i, a)
                                                                               (13)
                                                         =⇒ end (n, a)

                    ∀n ∈ Z ∀a ∈ Array (Z, Z) 0 ≤ x < n ∧ end (n, a)
                                                                               (14)
                                                              =⇒ a[x] = 42

where store(a, i, v) is array a where the value at index i has been replaced by v.
   None of the tools we have tried (Z3/PDR, Spacer, Eldarica) has been
able to solve this system, presumably because they cannot infer universally
quantified invariants over arrays. Indeed, here the invariant needed in the loop
is
                   0 ≤ i ≤ n ∧ (∀k 0 ≤ k < i =⇒ a[k] = 42)                  (15)
While 0 ≤ i ≤ n is inferred by a variety of approaches, the rest of the formula
is a tougher problem.
    Most software model checkers attempt constructing invariants from Craig in-
terpolants obtained from refutations of the accessibility of error states in partial
unfoldings of the problem, but interpolation over array properties is difficult,
especially since the goal is not to provide any interpolant, but interpolants that
generalize well to invariants [2, 1].
    This article instead introduces a way to derive universally quantified invari-
ants from the analysis of a system of Horn clauses on scalar variables (without
array variables).
    The flat encoding is not the only possible one. One may for instance instead
choose to find invariants not as sets of states (unary predicates on states), but
as binary relations on states: a procedure or function, or in fact any part of the

                                                 6
program with one single entry and one single exit point (e.g. a loop bosdy with
no break statement) is represented by a set of input-output pairs. In general, e.g.
when a procedure encoded in this way calls itself twice in a row, the resulting
system of Horn clauses is nonlinear : unfolding the Horn clauses may lead to an
exponentially growing tree [25] (see Fig. 7 for an example of a tree unfolding
of a nonlinear system). This is one reason why the Horn format for program
verification is richer and more flexible than a mere CFG. In this article, we
are going to exploit nonlinear systems of Horn clauses even if encoding a CFG
“flatly”.


3     Getting rid of the arrays
To use the power of Horn solver on array-free problems, we soundly abstract
problems with arrays to problems without arrays.
    In the Horn clauses for example 2, we attached to each program point pk
a predicate Ik over, say, Z × Z × Array (Z, Z) when the program variables are
two integers i, n and one integer-value, integer-indexed array a. In any solution
of the system of clauses, ¬Ik (i, n, a) implies that i, n, a cannot be reached at
program point pk . Instead, we will consider a predicate Ik♯ over Z × Z × Z × Z
such that ¬Ik♯ (i, n, k, ak ) implies that there is at pk no reachable state (i, n, a)
such that a[x] = ak . We thus have to provide abstract transformers for each
statement.
    Without loss of generality, any statement in the program can be assumed to
be either
  i) an array read to a fresh variable, v=a[i ]; in C syntax, v := a[i] in pseudo-
     code; the variables of the program are (x, i) before the statement and
     (x, i, v) after the statement, where x is a vector of arbitrarily many vari-
     ables;
 ii) an array write, a[ i]=v; (where v and i are variables) in C syntax, a[i] := v
     in pseudo-code; the variables of the program are (x, i, v) before and after
     the statement;
iii) a scalar operation, including assignments and guards over scalar variables.
More complex statements can be transformed to a sequence of such statements,
by introducing temporary variables if needed: for instance, a[i] := a[j] is trans-
formed into temp := a[j]; a[i] := temp.
Definition 1 (Read statement). Let v be a variable of type β, i be a variable
of type ι, and a be an array of values of type β with an index of type ι. Let x
be the other program variables, taken in χ. The concrete “next state” relation
for the read statement v=a[i ]; is (x, i, a) →c (x, i, a[i], a).
    Its forward abstract semantics is encoded into two Horn clauses, assuming
the statement is between locations p1 and p2 :

                           ∀x ∈ χ ∀i ∈ ι ∀ai ∈ β ∀k ∈ ι ∀ak ∈ β
                    k 6= i ∧ I1♯ (x, i), (k, ak ) ∧ I1♯ (x, i), (i, ai )
                                                                       
                                                                                 (16)
                                          =⇒ I2♯ (x, ai , i), (k, ak )
                                                                        



                                             7
                                 ∀x ∈ χ ∀i ∈ ι ∀ai ∈ β ∀k ∈ ι ∀ak ∈ β
                                                                                      (17)
                          I1♯   (x, i), (i, ai ) =⇒ I2♯ (x, ai , i), (i, ai )
                                                                            

    While rule 17 is straightforward, the nonlinear rule 16 may be more difficult
to comprehend. The intuition is that, to have ai = a[i] and ak = a[k] at the read
instruction with a given valuation (x, i) of the other variables, both ai = a[i]
and ak = a[k] had to be reachable with the same valuation.
Remark 1. One weakens the semantics by replacing these two rules by a single
Rule 16 without the i 6= k guard. Rule 17 ensures that in the outcome, if i = k
then v = ak .
Definition 2 (Write statement). With the same notations as above. The
concrete “next state” relation for the write statement a[ i]=v; is (x, i, v, a) →c
(x, i, v, store(a, i, v)).
    Its forward abstract semantics is encoded into two Horn clauses:
                                       ∀x ∈ χ ∀i ∈ ι ∀v ∈ β ∀k ∈ ι ∀ak ∈ β
                                                                                      (18)
                 I1♯   (x, i, v), (k, ak ) ∧ i 6= k =⇒ I2♯ (x, v, i), (k, ak )
                                                                             

                                        ∀x ∈ χ ∀i ∈ ι ∀v ∈ β ∀k ∈ ι ∀ak ∈ β
                                                                                      (19)
                                I1♯   (x, i, v), (i, ak ) =⇒ I2♯ (x, v, i), (i, v)
                                                                                 

Definition 3 (Initialization). Creating an array variable with nondeterminis-
tically chosen initial content is abstracted by

                       ∀x ∈ χ ∀k ∈ ι ∀ak ∈ β I1♯ (x) =⇒ I2♯ (x, k, ak )               (20)

      In particular, creating an array variable indexed by 0 . . . n − 1 is abstracted
by:

                         ∀x ∈ χ ∀k ∈ Z ∀ak ∈ β I1♯ (x) ∧ 0 ≤ k < n
                                                                                      (21)
                                                          =⇒ I2♯ (x, k, ak )

Remark 2. Because the 0 ≤ k < n condition gets naturally propagated through-
out the rules (it holds at the initialization state and can be assumed to hold at
other states), in our examples, we shall often omit this condition from the other
rules, for the sake of brevity, and simply write k ∈ Z.
Definition 4 (Scalar statements). With the same notations as above, we con-
sider a statement (or sequence thereof) operating only on scalar variables:
x →s x′ if it is possible to obtain scalar values x′ after executing the state-
ment on scalar values x. The concrete “next state” relation for that statement
is (x, i, v, a) →c (x′ , i, v, a).
    Its forward abstract semantics is encoded into one Horn clause:
                                                 ∀x ∈ χ ∀k ∈ ι ∀ak ∈ β
                                                                                      (22)
                          I1♯ (x, k, ak ) ∧ x →s x′ =⇒ I2♯ (x′ , k, ak )

Example 3. A test x 6= y gets abstracted as

                ∀x, y, k, ak I1♯ (x, y, k, ak ) ∧ x 6= y =⇒ I2♯ (x, y, k, ak )        (23)


                                                    8
Definition 5. The scalar operation kill (v1 , . . . , vn ) removes variables v1 , . . . , vn :
(x, v1 , . . . , vn ) → x.
   We shall apply it to get rid of dead variables, sometimes, for the sake of
brevity, without explicit note, by coalescing it with other operations.
   We use the same Galois connection [7] as some earlier works [21] [8, Sec. 2.1]:
Definition 6. The concretization of I ♯ ⊆ χ × (ι × β) is

                  γ I ♯ = {(x, a) | ∀i ∈ ι (x, i, a[i]) ∈ I ♯ }
                       
                                                                                           (24)

The abstraction of I ⊆ χ × Array (ι, β) is

                            α (I) = {(x, i, a[i]) | x ∈ χ, i ∈ ι}                          (25)

Theorem 1. α and γ form a Galois connection
                                                   γ
                      P (χ × Array (ι, β)) ←−−
                                           −− −− P (χ × (ι × β)) .
                                             α→

    Our Horn rules are of the form ∀y I1♯ (f1 (y)) ∧ · · · ∧ I1♯ (fm (y)) ∧ P (y) =⇒
  ♯
I2 (g(y) (y is a vector of variables, f1 , . . . , fm vectors of terms depending on
y, P an arithmetic predicate over y). In other words, they impose in I2♯ the
presence of g(y) as soon as certain elements f1 (y), . . . , fm (y) are found in I1♯ .
      ♯
Let I2−  be the set of such imposed elements. This Horn rule is said to be sound
if γ(I2− ) includes all states (x′ , a′ ) such that there exists (x, a) in γ(I1♯ ) and
       ♯

(x, a) →c (x′ , a′ ).
Lemma 2. The forward abstract semantics of the read statement (Def. 1) is
sound.
                                                                                          v:=a[i]
Proof. Let (x, i, a) ∈ γ(I1♯ ), that is ∀k ∈ ι I1♯ (x, i, k, a[k]). Suppose(x, i,a) −−−−→c
                                                                       ♯
(x, i, v, a), that is v = a[i]. Let us now show that (x, i, v, a) ∈ γ I2− , that is,
i) for all k ∈ ι such that k 6= i, I1♯ (x, i, i, v) and I1♯ (x, i, k, a[k]) both hold: both
follow from ∀k ∈ ι I1♯ (x, i, k, a[k]), and, for the first, from v = a[i]; ii) the case
k = i is also trivial.
Lemma 3. The forward abstract semantics of the write statement (Def. 2) is
sound.
                                                                                          a[i]:=v
Proof. Let (x, i, a) ∈ γ(I1♯ ), that is ∀k ∈ ι I1♯ (x, i, k, a[k]). Suppose (x, i, a) −−−−→c
(x, i, v, a′ ), that is, a′ [i] = v and for all k 6= i, a′ [k] = a[k] Let us now show that
                        ♯
(x, i, v, a′ ) ∈ γ I2−        , that is, for all k ∈ ι, either i) I1♯ (x, i, v, k, a′k ) and i 6= k
ii) i = k, v = a′ [k], and there exists ak such that I1♯ (x, i, v, i, ak ). Both cases are
trivial.
    The following two lemma are also easily proved:
Lemma 4. The forward abstract semantics of array initialization (Def. 3) is
sound.
Lemma 5. The forward abstract semantics of the scalar statements (Def. 4) is
sound.

                                               9
                                         i<n               a[i] := 42
               init              loop              write                incr
                        n>0
                        i := 0
                             i≥n
                                                 i := i + 1

                                 end



              Figure 3: Detailed control-flow graph for program 2


Remark 3. The scalar statements include “killing” dead variables (Def. 5).
Note that, contrary to many other abstractions, in ours, removing some variables
may cause irrecoverable loss of precision on other variables [21, Sec. 4.2]: if v
is live, then one can represent ∀k, a[k] = v, which implies ∀k1 , k2 a[k1 ] = a[k2 ]
(constantness), but if v is discarded, the constantness of a is lost.

Theorem 6. If I1♯ , . . . , Im
                             ♯
                               are a solution of a system of Horn clauses sound in
the above sense, then γ(I1♯ ), . . . , γ(Im
                                          ♯
                                            ) are inductive invariants with respect to
the concrete semantics →c .
Proof. From the general properties of fixed points of monotone operators and
Galois connections [7].

Definition 7 (Property conversion). A property “at program point pi , for
all x ∈ χ and all k ∈ ι, φ(x, k, a[k]) holds” (where φ is a formula, say over
arithmetic) is converted into a Horn query ∀x ∈ χ ∀k ∈ ι φ(x, k, ak ).
   Our method for converting a scalar program into a system of Horn clauses
over scalar variables is thus:
Algorithm 1.          1. Construct the control-flow graph of the program.
   2. To each control point pi , with vector of scalar variables xi , associate a
      predicate I(♯ xi , k, ak ) in the Horn clause system (the vector of scalar vari-
      ables may change from control point to control point).
   3. For each transition of the program, generate Horn rules according to
      Def. 1, 2, 4 as applicable (an initialization node does not need antecedents
      in its rule).
   4. Generate Horn queries from desired properties according to Def. 7.
Example (Ex. 2, continued). Let us now apply the Horn abstract semantics
from Definitions 1, 2 and 4 to Program 2, following the detailed control-flow
graph (Fig 3); in this case, α = Z, ι = {0, . . . , n − 1}, χ = Z. After a slight
simplification of the Horn clauses, we obtain (Listing 8):
                         ∀n, k, ak ∈ Z 0 ≤ k < n =⇒ loop(n, 0, k, ak )           (26)
                  ∀n, i, k, ak ∈ Z 0 ≤ k < n ∧ i < n ∧ loop(n, i, k, ak )
                                                                                 (27)
                                                  =⇒ write(n, i, k, ak )


                                           10
                       end


         i≥n−1−i
                           i<n−i−1
                                                        v1 := a[i]
  init                 loop               read 1                      read 2
            n>0
            i := 0
                     i := i + 1                    v2 := a[n − i − 1]


           incr                          write 2                      write 1
                  a[n − i − 1] := v1                    a[i] := v2

                                  Figure 4: Array reversal

                     ∀n, i, k, ak ∈ Z 0 ≤ k < n ∧ i 6= k ∧ write(n, i, k, ak )
                                                                                     (28)
                                                            =⇒ incr (n, i, k, ak )

                                           ∀n, i, ak ∈ Z ∧ write(n, i, i, ak )
                                                                                     (29)
                                                            =⇒ incr (n, i, i, 42)

                              ∀n, i, k, ak ∈ Z 0 ≤ k < n ∧ incr (n, i, k, ak )
                                                                                     (30)
                                                        =⇒ loop(n, i + 1, k, ak )

                      ∀n, i, k, ak ∈ Z 0 ≤ k < n ∧ i ≥ n ∧ loop(n, i, k, ak )
                                                                                     (31)
                                                              =⇒ end (n, k, ak )

    Finally, we add the postcondition (using Def. 7):

               ∀n, k, ak ∈ Z 0 ≤ k < n ∧ end(n, i, k, ak ) =⇒ ak = 42                (32)

    Z3/PDR, Spacer and Eldarica (-splitClauses), all unable to deal with
the original array problem (Formulas 11–14) solve this problem quickly.

Example 4. Consider now an array reversal procedure:
                                  Listing 3: Array reversal
void r e v e r s e ( i n t n , i n t a [ n ] ) {
  int i = 0;
  while ( t r u e ) {
    i n t j = n−1−i ;
    i f ( i >= j ) break ;
    i n t v1 = a [ i ] , v2 = a [ j ] ;
    a [ i ] = v2 ; a [ j ] = v1 ;
    i = i +1;
  }
}
   In order to prove that the final array is the reversal of the initial array,
we keep a copy of the initial array as b. Applying the rules for the forward

                                                   11
abstraction (Def. 1, 2, 4), and some simple simplifications (removal of dead
variables, propagation of j = n − i − 1), we obtain the Horn clauses (Listing 10):
                                          ∀n, k, ak , l, bl ∈ Z init(n, k, al , l, bl )
                                                                                              (33)
                                                        =⇒ loop(n, 0, k, ak , l, bl )

                                    ∀n, i, k, ak , l, bl ∈ Z loop(n, i, k, ak , l, bl )
                                                                                              (34)
                                 ∧i < n − i − 1 =⇒ read 1 (n, i, k, ak , l, bl )

                          ∀n, i, v1 , v2 , k, ak , l, bl ∈ Z read 1 (n, i, k, ak , l, bl )
                                                  ∧i 6= k ∧ read 1 (n, i, i, v1 , l, bl )     (35)
                                                  =⇒ read 2 (n, i, v1 , k, ak , l, bl )

                                  ∀n, i, v1 , v2 , k, l, bl ∈ Z read 1 (n, i, i, v1 , bl )
                                                                                              (36)
                                                   =⇒ read 2 (n, i, v1 , i, v1 , l, bl )

                 ∀n, i, v1 , v2 , k, ak , l, bl ∈ Z read 2 (n, i, v1 , v2 , k, ak , l, bl )
                       ∧n − 1 − i 6= k ∧ read 2 (n, i, v1 , n − i − 1, v2 , l, bl )           (37)
                                             =⇒ write 1 (n, i, v1 , v2 , k, ak , l, bl )

               ∀n, i, v1 , v2 , l, bl ∈ Z read 2 (n, i, v1 , v2 , n − 1 − i, v2 , l, bl )
                                                                                              (38)
                                   =⇒ write 1 (n, i, v1 , v2 , n − 1 − i, v2 , l, bl )

                ∀n, i, v1 , v2 , k, ak , l, bl ∈ Z write 1 (n, i, v1 , v2 , k, ak , l, bl )
                                                                                              (39)
                                      ∧i 6= k =⇒ write 2 (n, i, v1 , k, ak , l, bl )

                ∀n, i, v1 , v2 , k, ak , l, bl ∈ Z write 1 (n, i, v1 , v2 , k, ak , l, bl )
                                                                                              (40)
                                                  =⇒ write 2 (n, i, v1 , i, v2 , l, bl )

                        ∀n, i, v1 , k, ak , l, bl ∈ Z write 2 (n, i, v1 , k, ak , l, bl )
                                                                                              (41)
                                  ∧n − 1 − i 6= k =⇒ incr (n, i, k, ak , l, bl )

                        ∀n, i, v1 , k, ak , l, bl ∈ Z write 2 (n, i, v1 , k, ak , l, bl )
                                                                                              (42)
                                              =⇒ incr (n, i, n − 1 − i, v1 , l, bl )

                                    ∀n, i, k, ak , l, bl ∈ Z incr (n, i, k, ak , l, bl )
                                                                                              (43)
                                                   =⇒ loop(n, i + 1, k, ak , l, bl )

               ∀n, i, k, ak , l, bl ∈ Z i ≥ n − i − 1 ∧ loop(n, i, k, ak , l, bl )
                                                                                              (44)
                                                          =⇒ end 1 (n, k, ak , l, bl )

   We specify that, initially, a[k] = b[k] for all legal index k as:

                ∀n, k, ak ∈ Z 0 ≤ k < n =⇒ init (n, k, ak , k, ak )                           (45)
                 ∀n, k, ak , l, al ∈ Z 0 ≤ k < n ∧ 0 ≤ l < n ∧ k 6= l
                                                                                              (46)
                                                       =⇒ init (n, k, ak , l, bl )

   We finally specify that the final array is the reversal of the initial:

             ∀n, i, ak , bj ∈ Z 0 ≤ i < n ∧ end (n, i, ak , n − 1 − k, bj )
                                                                                              (47)
                                                             =⇒ ak = bj

Z3/PDR solves this problem within 4 s, Spacer takes 5 min

                                                  12
Example 5. Consider now the problem of finding the minimum of an array
slice a[l . . . h − 1], with value b = a[p]:

                      Listing 4: Find minimum in an array slice
void find minimum ( i n t n , i n t a [ n ] , i n t l , i n t h ) {
  i n t p = l , b = a [ l ] , i = l +1;
  while ( i < h ) {
      int v = a [ i ] ;
      if (v < b) {
        b = v;
        p = i;
     }
      i = i +1;
  }
}
    Again, we encode the abstraction of the statements (Def. 1, 2, 4) as Horn
clauses (Listing 13). At the end we have a predicate end (l, h, p, b, k, a[k]) on
which we impose the properties

                         ∀l, h, p, b, ap end (l, h, p, b, p, ap) =⇒ b = ap       (48)
                   ∀l, h, p, b, k, ap, ak l ≤ k < h ∧ end (l, h, p, b, k, ak )
                                                                                 (49)
                                                                 =⇒ b ≤ ak

Rule 48 imposes the postcondition b = a[p], Rule 49 imposes the postcondition
∀k l ≤ k < h =⇒ b ≤ a[k]. Again, Z3/PDR and Spacer solve this Horn
system (but not Eldarica).
    The kind of relationship that can be inferred between loop indices, array
indices and array contents is limited only by the capabilities of the Horn solver,
as shown in the following example:
Example 6. Consider for instance this array fill where a[i] gets i mod 2:

                    Listing 5: Fill 1D-array with even/odd values
void a r r a y f i l l 1 e v e n o d d ( i n t n , i n t a [ n ] ) {
  int i = 0;
  while ( i < n ) {
    a[ i ] = i & 1;
    i = i +1;
  }
}
    The abstract semantics is Formulas 26–31 except that the constant 42 is
replaced by i mod 2. We wish to prove postconditions

                                   ∀k 0 ≤ 2k < n =⇒ a[2k] = 0                    (50)
                         ∀k 0 ≤ 2k + 1 < n =⇒ a[2k + 1] = 1                      (51)

which get translated into Horn clauses

                                ∀k end (n, 2k, ax ) =⇒ ax = 0                    (52)
                            ∀k end (n, 2k + 1, ax ) =⇒ ax = 1                    (53)


                                               13
                                    exit                        incr i


                                 i≥m                  i := i + 1    j≥n
                                                  i<m
                        i := 0                    j := 0
              init                  loop i                   loop j

                                                                         j<n
                                                       j := j + 1

                                    incr j                      write
                                                a[i, j] := 42


                            Figure 5: Fill 2D array


Spacer solves this problem (Listing 9) instantaneously, while Z3/PDR cannot
solve it. We suppose this is because Z3/PDR cannot infer interpolants depending
on divisibility predicates.
    We have made no assumption regarding the nature of the indexing variable:
we used integers because arrays indexed by an integer range are a very common
kind of data structure, but really it can be any type supported by the Horn
clause solver, e.g. rationals:
Example 7. Consider the following program, handling a mutable map a [] from
the rationals to the integers, initialized to 0:
a [1] = 10;     a [2] = 20;       a [3] = 30;
   We can encode it as (Listing 11):

                                                 ∀x ∈ Q init (x, 0)            (54)
              ∀x ∈ Q ∀ax ∈ Z init (x, ax ) ∧ x 6= 1 =⇒ w1 (x, ax )             (55)
                            ∀ax ∈ Z init (1, ax) =⇒ w1 (1, 10)                 (56)
               ∀x ∈ Q ∀ax ∈ Z w1 (x, ax ) ∧ x 6= 2 =⇒ w2 (x, ax )              (57)
                              ∀ax ∈ Z w1 (2, ax) =⇒ w2 (2, 20)                 (58)
              ∀x ∈ Q ∀ax ∈ Z w2 (x, ax ) ∧ x 6= 3 =⇒ exit (x, ax )             (59)
                                 ∀ax ∈ Z w2 (3, ax) =⇒ exit (3, 30)            (60)

   The postcondition ∀x ∈ Q a[x] ≥ 0, encoded as ∀x ∈ Q ax ≥ 0, is easily
proved by Z3/PDR and Spacer.
    Matrices are bidimensional arrays, that is, arrays indexed by two integers x
and y: 0 ≤ x < m, 0 ≤ y < n for a m × n arrays. More generally, arrays can
be defined for an arbitrary number d of dimensions. Everything that we have
seen so far applies when the type ι of the indexing variable is a subset of Zd
(e.g. for d = 2, ι = {(x, y) | 0 ≤ x < m ∧ 0 ≤ y < n}). We may therefore apply
directly what precedes and generate Horn clauses referring to pairs of indices

                                           14
(x, y). Since not every solver supports these, one may instead use two indices x
and y: a comparison (x1 , y1 ) = (x2 , y2 ) is expressed as x1 = x2 ∧ y1 = y2 .
Example 8. The following program fills a m × n matrix:

                                Listing 6: Fill 2D-matrix
void a r r a y f i l l 2 ( i n t m, i n t n , i n t a [m] [ n ] ) {
  int i = 0;
  while ( i < m) {
    int j = 0;
    while ( j < n ) {
      a [ i ] [ j ] = 42;
       j = j +1;
    }
    i = i +1;
  }
}
    It gets encoded as (Listing 12, Fig. 5):
                               ∀m, n, x, y, axy ∈ Z 0 ≤ x < m ∧ 0 ≤ y < n
                                                                                       (61)
                                                       =⇒ init(m, n, x, y, axy )

                                    ∀m, n, x, y, axy ∈ Z init(m, n, x, y, axy )
                                                                                       (62)
                                                  =⇒ loop i (m, n, 0, x, y, axy )

                     ∀m, n, i, x, y, axy ∈ Z loop i (m, n, i, x, y, axy ) ∧ i < m
                                                                                       (63)
                                               =⇒ loop j (m, n, i, 0, x, y, axy )

                     ∀m, n, i, x, y, axy ∈ Z loop i (m, n, i, x, y, axy ) ∧ i ≥ m
                                                                                       (64)
                                                       =⇒ exit (m, n, x, y, axy )

                ∀m, n, i, j, x, y, axy ∈ Z loop j (m, n, i, j, x, y, axy ) ∧ j < n
                                                                                       (65)
                                                =⇒ write(m, n, i, j, x, y, axy )

                ∀m, n, i, j, x, y, axy ∈ Z loop j (m, n, i, j, x, y, axy ) ∧ j ≥ n
                                                                                       (66)
                                                  =⇒ incr i (m, n, i, x, y, axy )

                                                    ∀m, n, i, j, x, y, axy , aij ∈ Z
                       write(m, n, i, j, x, y, axy ) ∧ write(m, n, i, j, i, j, aij )   (67)
                       ∧ ∧ (i 6= x ∨ j 6= y) =⇒ incr j (m, n, i, j, x, y, axy )

                                 ∀m, n, i, j, aij ∈ Z write(m, n, i, j, i, j, aij )
                                                                                       (68)
                                                  =⇒ incr j (m, n, i, j, i, j, 42)

                         ∀m, n, i, j, x, y, axy ∈ Z incr j (m, n, i, j, x, y, axy )
                                                                                       (69)
                                           =⇒ loop j (m, n, i, j + 1, x, y, axy )

                              ∀m, n, i, x, y, axy ∈ Z incr i (m, n, i, x, y, axy )
                                                                                       (70)
                                             =⇒ loop i (m, n, i + 1, x, y, axy )

    Again, we can prove that ∀m, n, x, y, axy ∈ Z, exit =⇒ axy = 42; otherwise
said, finally, ∀x, y a[x, y] = 42.



                                               15
4      Sortedness
The Galois connection of Def. 6 expresses relations of the form ∀k ∈ ι φ(x, k, a[k])
where x are variables from the program, a a map and k an index into the map
a; in other words, relations between each array element individually and the
rest of the variables. It cannot express properties such as sortedness, which
link two array elements: ∀k1 , k2 ∈ ι k1 < k2 =⇒ a[k1 ] ≤ a[k2 ]. Let us now
see an abstraction with two “distinguished cells”, capable of representing such
properties:
Definition 8. The concretization with two indices of I ♯ ⊆ χ × (ι × β)2 is
          γ2 I ♯ = {(x, a) | ∀k1 , k2 ∈ ι (x, k1 , a[k1 ], k2 , a[k2 ]) ∈ I ♯ }
                
                                                                                (71)
The abstraction with two indices of I ⊆ χ × Array (ι, β) is
                α2 (I) = {(x, k1 , a[k1 ], k2 , a[k2 ]) | x ∈ χ, k1 , k2 ∈ ι}                 (72)
Theorem 7. α2 and γ2 form a Galois connection
                                         γ2
                   P (χ × Array (ι, β)) ←−−−− P χ × (ι × β)2 .
                                                            
                                        −−
                                         α→            2

   With respect to implementation efficiency, it may be preferable to break this
symmetry between indices k1 and k2 by imposing k1 ≤ k2 for some total order.
One then gets:
Definition 9. The concretization with two ordered indices of I ♯ ⊆ χ × (ι × β)2
is
         γ2≤ I ♯ = {(x, a) | ∀k1 ≤ k2 ∈ ι (x, k1 , a[k1 ], k2 , a[k2 ]) ∈ I ♯ }
                
                                                                                (73)
The abstraction with two indices of I ⊆ χ × Array (ι, β) is
              α2≤ (I) = {(x, k1 , a[k1 ], k2 , a[k2 ]) | x ∈ χ, k1 ≤ k2 ∈ ι}                  (74)
Theorem 8. α2≤ and γ2≤ form a Galois connection
                             γ2≤
    P (χ × Array (ι, β)) ←−−
                         −− −−−
                          α −→ 2≤

                         P ({(x, k1 , v1 , k2 , v2 ) | x ∈ χ, k1 ≤ k2 ∈ ι, v1 , v2 ∈ β}) .
Definition 10 (Read statement, two indices k1 ≤ k2 ). The abstraction of
v := a[i] is:
                                      ∀x ∈ χ ∀i, k1 , k2 ∈ ι ∀v, ak1 , ak2 ∈ β
                            I1♯ (x, i, k1 , ak1 , k2 , ak2 ) ∧ I1♯ (x, i, i, v, k2 , ak2 )    (75)
                       ∧k1 6= i ∧ i < k2 =⇒             I2♯ (x, i, v, k1 , ak1 , k2 , ak2 )
                                      ∀x ∈ χ ∀i, k1 , k2 ∈ ι ∀v, ak1 , ak2 ∈ β
                            I1♯ (x, i, k1 , ak1 , k2 , ak2 ) ∧ I1♯ (x, i, k1 , ak1 , i, v)    (76)
                       ∧k2 6= i ∧ k1 < i =⇒             I2♯ (x, i, v, k1 , ak1 , k2 , ak2 )

                                                 ∀x ∈ χ ∀i, k2 ∈ ι ∀v, ak2 ∈ β
                                                                                              (77)
                 I1♯ (x, i, i, v, k2 , ak2 ) ∧ i < k2 =⇒ I2♯ (x, i, i, v, k2 , ak2 )

                                                 ∀x ∈ χ ∀i, k1 ∈ ι ∀v, ak1 ∈ β
                                                                                              (78)
                 I1♯ (x, i, k1 , ak1 , i, v) ∧ k1 ≤ i      =⇒ I2♯ (x, i, k1 , ak1 , i, v)


                                                  16
Definition 11 (Write statement, two indices k1 ≤ k2 ). The abstraction of
a[i] := v is:
                                      ∀x ∈ χ ∀i, k1 , k2 ∈ ι ∀v, ak1 , ak2 ∈ β
                              I1♯ (x, i, v, k1 , ak1 , k2 , ak2 ) ∧ i 6= k1 ∧ i 6= k2         (79)
                                                =⇒      I2♯ (x, i, v, k1 , ak1 , k2 , ak2 )

                             ∀x ∈ χ ∀i, k2 ∈ ι ∀v, ak1 , ak2 ∈ β ∧ i 6= k2
                                                                                              (80)
                 ∧I1♯ (x, i, v, i, ak1 , k2 , ak2 )   =⇒ I2♯ (x, i, v, i, v, k2 , ak2 )

                             ∀x ∈ χ ∀i, k1 ∈ ι ∀v, ak1 , ak2 ∈ β‘ ∧ i 6= k1
                                                                                              (81)
                 ∧I1♯ (x, i, v, k1 , ak1 , i, ak2 )   =⇒ I2♯ (x, i, v, k1 , ak1 , i, v)

                                                           ∀x ∈ χ ∀i ∈ ι ∀v, ak ∈ β
                                                                                              (82)
                            I1♯ (x, i, v, i, ak , i, ak )   =⇒ I2♯ (x, i, v, i, v, i, v)

Lemma 9. The abstract forward semantics of the read statement, with two
indices k1 ≤ k2 (Def. 10) is a sound abstraction of the concrete semantics given
in Def. 1.
Proof. Let k1 ≤ k2 ∈ ι and i ∈ ι, ι being totally ordered. Then one necessarily
falls in one of the following cases, corresponding to rules 75–78: i) k1 6= i∧i < k2
ii) k2 6= i ∧ k < i iii) k1 = i ∧ i < k2 iv) k2 = i ∧ k1 ≤ i It is easy to see that, for
each of these cases, the corresponding rule is sound.
Lemma 10. The abstract forward semantics of the write statement, with two
indices k1 ≤ k2 (Def. 11) is a sound abstraction of the concrete semantics given
in Def. 2.
Proof. Similarly, one is necessarily in one of the four exclusive cases, each corre-
sponding to a rule easily proved to be sound: i) i 6= k1 ∧ i 6= k2 ii) i = k1 ∧ i 6= k2
iii) i 6= k1 ∧ i = k2 iv) i = k1 = k2 .
   It is possible to mix abstractions with one or two “distinguished cells” within
the same problem. Let us see how to convert between the two:
                                                                               α
Definition 12. Let I1♯ be an abstraction according to ←−−
                                                      −− −−; we wish to expand
                                                        γ→
                                                   α2≤
it to an abstraction I2♯ according to ←−−
                                      −− −−−.
                                       γ −→           2≤




                                    ∀x ∈ χ ∀k1 , k2 ∈ ι ∀β1 , β2 ∈ β
                        I1♯ (x, k1 , ak1 ) ∧ I1♯ (x, k2 , ak2 ) ∧ k1 < k2                     (83)
                                          =⇒ I2♯ (x, k1 , ak1 , k2 , ak2 )
                                                 ∀x ∈ χ ∀k ∈ ι ∀β ∈ β
                                                                                              (84)
                                   I1♯ (x, k)    =⇒ I2♯ (x, k, ak , k, ak )

Remark 4 (Initialization). By coalescing these rules with initialization for one
“distinguished cell” (Def. 3), we obtain a direct abstraction of initialization for
the case of an array indexed by 0 . . . n − 1, which we use in our examples:



                                                   17
                                                   v := a[i]
                                        read 2                  test

                   exit
                                                                               v<b
                                                          v≥b                  b := v
  init
                                                          i := i + 1           p := i
                        l ≥h−1                                                 i := i + 1
                                               i<h
   l0 ≤ h
   l := l0
                  outer     l <h−1
                                          read 1                        loop
                   loop                             f := b := a[l]
                                                    p := l
                                                    i := l + 1             i≥h
i := i + 1

         kill(p, b, f )    end     a[p] := f              a[l] := b
  incr                                         write 2                 write 1
             (Def. 5)     swap


                                    Figure 6: Selection sort




                                  ∀x ∈ χ ∀n ∈ Z ∀k1 , k2 ∈ Z ∀β1 , β2 ∈ β
                                                                                            (85)
                   0 ≤ k1 < k2 < n ∧ I1♯ (x) =⇒ I2♯ (x, k1 , ak1 , k2 , ak2 )

                                                         ∀x ∈ χ ∀k ∈ Z ∀β ∈ β
                                                                                            (86)
                                 0 ≤ k < n ∧ I1♯ (x)     =⇒ I2♯ (x, k, ak , k, ak )


Example 9 (Selection sort). Selection sort finds the least element in a[l . . . h−1]
(using Prog. 4 as its inner loop) and swaps it with a[l], then sorts a[l + 1, h − 1].
At the end, a[l0 . . . h − 1] is sorted, where l0 is the initial value of l.

                                    Listing 7: Selection sort
void s e l e c t i o n s o r t ( i n t l 0 , i n t h , i n t a [ ] ) {
  int l = l0 ;
  while ( l < h−1) {
    i n t p = l , b = a [ l ] , f = b , i = l +1;
    while ( i < h ) {
        int v = a [ i ] ;
        if (v < b) {
           b = v;
           p = i;
       }
        i = i +1;
    }
    a[ l ] = b;
    a [p] = f ;
    l = l +1;
  }
}



                                                   18
   Using the control points from Fig. 6, and the rules for the read (Def. 10)
and write (Def. 11) statements, we write the abstract forward semantics of this
program as a system of Horn clauses (Listing 14).
   We wish to prove that, at the end, a[l0 , h − 1] is sorted: at the exit node,

                         ∀l0 ≤ k1 < k2 < h a[k1 ] ≤ a[k2 ]                     (87)

    This is expressed as the final condition

                         ∀l0 , h, k1 , ak1 , k2 , ak2 l0 ≤ k < k2 < h
                                                                               (88)
                    ∧exit (l0 , h, k1 , ak1 , k2 , ak2 ) =⇒ ak1 ≤ ak2

    Spacer solves the resulting system of Horn clauses in 8 min.
    We have thus, fully automatically, proved that the output of selection sort
is truly sorted (in Example 10 we shall see how to prove that the multiset of
elements in the output is the same as in the input).
    One may be concerned about an analysis time of 6 minutes for a 17-line
program. In our experience, the average undergraduate student taking a course
in program verification and asked to provide inductive invariants (in the Floyd-
Hoare sense; say, as annotations for a tool such as Frama-C) to prove that
property takes longer time to provide them. In particular, this invariant for the
outer loop is somewhat non trivial:

              ∀k1 , k2 l0 ≤ k1 < l ∧ k1 ≤ k2 < h =⇒ a[k1 ] ≤ a[k2 ]            (89)

This invariant can be expressed in our system of Horn clauses as:

              ∀l0 , l, h, k1 , ak1 , k2 , ak2 ∈ Z l0 ≤ k1 < l ∧ k1 ≤ k2 < h
                                                                               (90)
                 ∧outerloop(l0 , l, h, k1 , ak1 , k2 , ak2 ) =⇒ ak1 ≤ ak2

If this invariant is added to the problem as an additional query to prove, Spacer
solves the problem in 1 second! It could seem counter-intuitive that a solver
would take less time to solve a problem with an additional constraint; but
this constraint expresses an invariant necessary to prove the solution, and thus
nudges the solver towards the solution.
    Our approach is therefore flexible: if a solver fails to prove the desired prop-
erty on its own, it is possible to help it by providing partial invariants. This
is a less tedious approach than having to provide full invariants at every loop
header, as common in assisted Floyd-Hoare proofs.


5     Sets and multisets
Our abstraction for maps may be used to abstract (multi)sets.

5.1    Simple sets and multisets
Many programming languages provide libraries for computing over sets or mul-
tisets of elements. One should reason on programs using these libraries by
using the set-theoretic, high-level specification of their interface, as opposed to
internal implementation details.

                                           19
     Remark, again, that we have made no assumption on the set of indices ι
(except, occasionally, that is endowed with a total order, but that assumption
may be dispensed from). A subset of ι is just a map from ι to the Booleans, a
multiset a map from ι to the natural numbers. Testing the membership of one
item k ∈ ι therefore just amounts to an array read a[k], forcing membership or
non-membership just amounts to a write.
     A single (multi)set a is abstracted as a set of pairs (k, a[k]). If one has
several (multi)sets a, b, c, one may either abstract them with separate indices
(i, a[i], j, a[j], k, a[k]), or with a common index (k, a[k], b[k], c[k]). This last op-
tion is less expressive, but simpler, and is often sufficient.
Definition 13 ((Multi)set union). The operation a := union(b, c) is abstracted
as:

          ∀x ∈ χ ∀k ∈ ι I1♯ (x, k, ak , bk , ck ) =⇒ I2♯ (x, k, bk ∨ ck , bk , ck )   (91)

(For multiset, replace ∨ by +.)
Definition 14 (Set intersection). The operation a := intersection(b, c) is ab-
stracted as:

          ∀x ∈ χ ∀k ∈ ι I1♯ (x, k, ak , bk , ck ) =⇒ I2♯ (x, k, bk ∧ ck , bk , ck )   (92)

   If operations such as “get the (min/max)imal element” are to be abstracted
precisely, then one can enrich the abstraction by adding tracking variables l and
h for the minimal and maximal elements, and updating them accordingly. In
the case of sets of integers, such tracking variables may be used to implement
the “for each” iterator: iterate i from l to h and test whether i is in the set.

5.2    Multiset of elements in an array
In Example 9, we showed how to prove that the output of selection sort is sorted.
This is not enough for functional correctness: we also have to prove that the
output is a permutation of the input, or, equivalently, that the multiset of
elements in the output array is the same as that in the input array.
   Let us remark that it is easy to keep track, in an auxiliary map, of the
number #a(x) of elements of value x in the array a[]. Only write accesses to a[]
have an influence on #a: a write a[i] := v is replaced by a sequence:

             #a(a[i]) := #a(a[i]) − 1; a[i] := v; #a(v) := #a(v) + 1                  (93)

(that is, in addition to the array write, the count of elements for the value that
gets overwritten is decremented, and the count of elements for the new value is
incremented).
    This auxiliary map #a can itself be abstracted using our approach! Let
us now see how to implement this in our abstract forward semantics expressed
using Horn clauses. We enrich our Galois connection (Def. 6) as follows:
Definition 15. The concretization of I ♯ ⊆ χ × (ι × β) × (β × N) is
         n
  γ# I ♯ = (x, a) | ∀i ∈ ι ∀v ∈ β


                                             20
                                                                                        o
                                        x, (i, a[i]), (v, card{j ∈ ι | a[j] = v}) ∈ I ♯
                                                                                 
                                                                                                          (94)

where card X denotes the number of elements in the set X.
   The abstraction of I ⊆ χ × Array (ι, β) is
           n                                        
  α# (I) = x, (i, a[i]), (v, card{j ∈ ι | a[j] = v})
                                                                                                      o
                                                                                          x ∈ χ, i ∈ ι    (95)

Theorem 11. α# and γ# form a Galois connection
                                                 γ#
             P (χ × Array (ι, β)) ←−−
                                  −− −−
                                    α−
                                      − P (χ × (ι × β) × (β × N)) .
                                      →              #


    The Horn rules for array reads and for scalar operations are the same as those
for our first abstraction, except that we carry over the extra two components
identically.
Definition 16 (Read statement). With the same notations in Def. 1:
                           ∀x ∈ χ ∀i ∈ ι ∀v ∈ β ∀k ∈ ι ∀ak , z ∈ β ∀a#z ∈ N
                                              k 6= i ∧ I1♯ (x, i), (k, ak ), (z, a#z )
                                                                                       
                                                                                                          (96)
                             ∧I1♯ (x, i), (i, v), (z, a#z ) =⇒ I2♯ (x, v, i, k, ak )
                                                           

                                                                      ∀x ∈ χ ∀i ∈ ι ∀v ∈ β
                                                                                                          (97)
               I1♯                                            I2♯
                                                                                                
                     (x, i), (i, v), (z, a#z )       =⇒             (x, v, i), (i, v), (z, a#z )

Lemma 12. The abstract forward semantics of the read statement (Def. 16) is
a sound abstraction of the concrete semantics given in Def. 1.
    The abstraction of the write statement is more complicated (see the sequence
of instructions in Formula 93). To move by a write operation a[i] := v from a
control point p1 to a control point p2 , we need two intermediate control points
pa and pb .
Definition 17 (Write statement). With the same notations in Def. 2:

                               ∀x ∈ χ ∀i, k ∈ ι ∀ai , ak , v, z ∈ β ∀a#z ∈ N ai 6= z∧
                     I1♯   (x, v, i), (k, ak ), (z, a#z ) ∧ I1♯ (x, v, i), (i, ai ), (z, a#z )
                                                                                              

                                                      =⇒ Ia♯ (x, v, i), (k, ak ), (z, a#z )
                                                                                               

                                            ∀x ∈ χ ∀i, k ∈ ι ∀ai , ak , v ∈ β ∀a#z ∈ N
                 I1♯   (x, v, i), (k, ak ), (ai , a#z ) ∧ I1♯ (x, v, i), (i, ai ), (ai , a#z )
                                                                                              

                                              =⇒ Ia♯ (x, v, i), (k, ak ), (ai , a#z − 1)
                                                                                               

                                          ∀x ∈ χ ∀i, k ∈ ι ∀ai , ak , v, z ∈ β ∀a#z ∈ N
          v 6= z ∧ Ia♯     (x, v, i), (k, ak ), (z, a#z ) ∧ Ia♯ (x, v, i), (i, ai ), (z, a#z )
                                                                                              

                                                      =⇒ Ib♯ (x, v, i), (k, ak ), (z, a#z )
                                                                                               

                                             ∀x ∈ χ ∀i, k ∈ ι ∀ai , ak , v ∈ β ∀a#z ∈ N
                     Ia♯   (x, v, i), (k, ak ), (v, a#z ) ∧ Ia♯ (x, v, i), (i, ai ), (v, a#z )
                                                                                              

                                                  =⇒ Ib♯ (x, v, i), (k, ak ), (v, a#z + 1)
                                                                                               


                                                         21
                                       ∀x ∈ χ ∀i ∈ ι ∀v ∈ β ∀x ∈ ι ∀ak ∈ β i 6= k∧
              I1♯    (x, i, v), (k, ak ), (z, a#z ) =⇒ I2♯ (x, v, i), (k, ak ), (z, a#z )
                                                                                         

                                                    ∀x ∈ χ ∀i ∈ ι ∀v ∈ β ∀k ∈ ι ∀ak ∈ β
                    I1♯   (x, i, v), (i, ak ), (z, a#z ) =⇒ I2♯ (x, v, i), (i, v), (z, a#z )
                                                                                            

Lemma 13. The abstract forward semantics of the write statement (Def. 17)
is a sound abstraction of the concrete semantics given in Def. 2.
   If we want to compare the multiset of the contents of an array a at the end of
a procedure to its contents at the beginning of the procedure, one needs to keep
a copy of the old multiset. It is common that the property sought is a relation
between the number of occurrences #a(z) of an element z in the output array
a and its number of occurrences #a0 (z) in the input array a0 . In the above
formulas, one may therefore replace the pair (z, a#z ) by (z, a#z , a0#z ), with a0#z
always propagated identically.
Example 10. Consider again selection sort (Program 7). We use the abstract
semantics for read (Def. 16) and write (Def. 17), with an additional component
a0#z for tracking the original number of values z in the array a (Listing 15).
    We specify the final property as the query

                ∀l0 , h, k, ak , z, a#z , a0#z exit (l0 , h, k, ak , z, a#z , a0#z )
                                                                                                 (98)
                                                                   =⇒ a#z = a0#z

6      Counterexamples
Solvers for Horn clauses based on counterexample-based abstraction refinement
(CEGAR) construct a sequence of increasingly more precise abstractions of the
Horn clause problem. At every step, they search for a counterexample to the
satisfiability of the Horn clauses: that is, a tree unfolding of the Horn clauses
and matching assignments to the variables in the clauses, rooted at a violated
query. If such a counterexample is found, the solver answers “unsatisfiable”:
this counterexample is a witness to the absence of solution of the system. If
it is found not to exist, the solver examines its proof of nonexistence for clues
how to refine the abstraction, typically by generating tree interpolants, and the
process goes on [26].
    In our case, a counterexample provided by the Horn solver proves the nonex-
istence of an inductive invariant capable of proving the desired properties in our
abstraction: it means that either our abstraction is too coarse, either the desired
safety property is wrong because there exists a concrete counterexample.
Example 11. The assertion at the end of this program is obviously valid (and
may be established by, e.g., global value numbering):
/∗   r 1 ∗ / v1 = a [ 1 ] ; / ∗ r 2 ∗ / v2 = a [ 2 ] ;
/∗   cmp ∗ / assume ( v1 == v2 ) ; / ∗ k i l l ( v1 , v2 ) ∗ /
/∗   r 3 ∗ / v1 = a [ 1 ] ; / ∗ r 4 ∗ / v2 = a [ 2 ] ;
/∗   end ∗ / a s s e r t ( v1 == v2 ) ;
     The system of Horn rules produced by Algorithm 1 is:
                                                             ∀k, ak ∈ Z r1 (k, ak )              (99)


                                                    22
                                    ..
 r1 (1, 0)                           ..
             v1 := a[1] (101)
r2 (0, 1, 0)                   r2 (0, 2, 0)
                                              v2 := a[2] (102)
              cmp(0, 1, 1, 0)
                              v1 := a[1] (106)                              ..
                  r3 (1, 0)                                                  ..
                 r4 (0, 1, 0)                                          r4 (0, 2, 0)
                                                                                      v2 := a[2] (107)
                                        end (0, 1, 1, 0)

Figure 7: Counterexample unfolding of Ex 11 leading to end (v1 .v2 , 1, a1 ) with
v1 ≤ v2 , violating the condition

                                 ∀v1 , k, ak ∈ Z r1 (k, ak ) ∧ r1 (1, v1 ) ∧ k 6= 1
                                                                                                   (100)
                                                                =⇒ r2 (v1 , k, ak )

                                               ∀v1 r1 (1, v1 ) =⇒ r2 (v1 , 1, v2 )                 (101)
                     ∀v1 , v2 , k, ak ∈ Z r2 (v1 , k, ak ) ∧ r2 (v1 , 2, v2 ) ∧ k 6= 2
                                                                                                   (102)
                                                         =⇒ cmp(v1 , v2 , k, ak )

                           ∀v1 , v2 ∈ Z r2 (v1 , 2, v2 ) =⇒ cmp(v1 , v2 , 2, v2 )                  (103)
                              ∀v, k, ak ∈ Z cmp(v, v, k, ak ) =⇒ r3 (k, ak )                       (104)

                                 ∀v1 , k, ak ∈ Z r3 (k, ak ) ∧ r3 (1, v1 ) ∧ k 6= 1
                                                                                                   (105)
                                                                =⇒ r4 (v1 , k, ak )

                                               ∀v1 r3 (1, v1 ) =⇒ r4 (v1 , 1, v1 )                 (106)

                     ∀v1 , v2 , k, ak ∈ Z r4 (v1 , k, ak ) ∧ r4 (v1 , 2, v2 ) ∧ k 6= 2
                                                                                                   (107)
                                                          =⇒ end (v1 , v2 , k, ak )

                            ∀v1 , v2 ∈ Z r4 (v1 , 2, v2 ) =⇒ end (v1 , v2 , 2, v2 )                (108)
                            ∀v1 , v2 , a1 ∈ Z end (v1 , v2 , 1, a1 ) =⇒ v1 = v2                    (109)


    This system is too abstract to prove the desired property; an abstract coun-
terexample exists (Fig. 7).
    Note that all our Horn rules are of the form9

      ∀ . . . I1♯ . . . , (k, ak ) ∧ · · · ∧ I1♯ (. . . , . . . ) =⇒ I2♯ . . . , (k, ak )
                                                                                        
                                                                                                  (110)

thus, in the unfolding, the children of a node associated with a control point p2
are all associated to the same control point p1 . Furthermore, the rule associ-
ated to a node corresponds to one statement transitioning from p1 to p2 . Any
branch from a leaf to the root of the unfolding thus corresponds to a sequence of
statements from the original program. It is, in the CEGAR view, an “abstract
counterexample trace” from an initialization control point to a possible viola-
tion. By conjoining the concrete semantics associated to each step we obtain a
first-order formula over arithmetic and arrays. If this formula is satisfiable, we
have a concrete counterexample.
  9 In this explanation we use a single (k, a ), as in Sec. 3, but the same carries to the use of
                                             k
multiple indices (k1 , ak1 , k2 , ak2 ) etc.



                                                   23
Example (Ex. 11, continued). From the unfolding in Figure 7, one obtains the
sequence of instructions to be tested for a concrete counterexample. (On this
example with no tests or loops, there is only one sequence from the start to the
end of the program, but in general this says which test branches are taken.)
Algorithm 2.          1. Construct the Horn clause system using Algorithm 1.
    2. Run the Horn clause solver. It returns “satisfiable”, report “proved”.
    3. If it returns a counterexample unfolding, select a branch, collect the corre-
       sponding concrete transition relations and construct a trace satisfiability
       problem in first-order arithmetic plus arrays.
    4. Run a satisfiability modulo theory (SMT) solver on this problem. If it
       returns “satisfiable”, report “violated”.
   5. (Optional refinement step) Examine the array axioms in use in the unsat-
      isfiability proof provided by the SMT-solver; increase the precision of the
      abstraction of these arrays by increasing the number of indices (e.g. move
      from a single index k to two indices k1 ≤ k2 ), and go back to step 1.
    Any branch in the unfolding could work, but we propose selecting the left-
most one according to the order in which we listed the antecedents of the Horn
rules in this article.
    The values for the variables in the counterexample unfolding provided by the
Horn clause solver may be used as hints for finding the values of the variables
in the SMT problem.


7     Related work
7.1     Abstract interpretation
Smashing The simplest abstraction for an array is to “smash” all cells into a
single one — this amounts to removing the k component from our first Galois
connection (Def. 6). The weakness of that approach is that all writes are treated
as “may writes”: a[i] := x adds the value x to the set of values admissible for
the array a, but there is no way to remove any value from that set. Such an
approach thus cannot treat initialization loops (e.g. Program 2) precisely: it
cannot prove that the old values have been erased.

Exploding At the other extreme, for an array of statically known finite length
N (which is common in embedded safety-critical software), one can distinguish
all cells a[0], . . . , a[N − 1] and treat them as separate variables a0 , . . . , aN −1 ; e.g.
a read x = a[ i ]; is treated as a
switch ( i ) {
  c a s e 0 : x = a 0 ; break ;
  ...
  c a s e N − 1 : x=a N−1 ; break ;
}

   This is a good solution when N is small, but a terrible one when N is large:
1. many analysis approaches scale poorly with the number of active variables


                                              24
2. an initialization loop will have to be unrolled N times to show it initializes
all cells.
    Both these approaches have been used with success in the Astrée static an-
alyzer [4, 3], where the “smashed” cell or the individual array cells are typically
further abstracted by intervals and other non-relational analyses.

Slices More sophisticated analyses [10, 11, 22, 23, 9] distinguish slices or seg-
ments in the array, their boundaries depending on the index variables. For
instance, in array initialization (Program 2), such an analysis will tend to distin-
guish the area already initialized (indices < i) and the area yet to be initialized
(indices ≥ i). In the simplest case, each slice is “smashed” into a single value,
but more refined analyses express relationships between slices. Since the slices
are segments [a, b] of indices, these analyses generalize poorly to multidimen-
sional arrays. Also, there is often a combinatorial explosion in analyzing how
array slices may or may not overlap.
    To our best knowledge, all these approaches factor through our Galois con-
             γ     γ2≤
nections ←−−−−−−, ←−−
             α→ −−
                    −−
                   α2≤
                      −→
                       − or combinations thereof: that is, their abstraction can
be expressed as a composition of our abstraction and further abstraction —
even though our implementation of the abstract transfer functions is completely
different from theirs. Our approach, however, separates the concerns of i) ab-
stracting array problems to array-less problems ii) abstracting the relationships
between different cells and indices.

7.2    Array removal by program transformation
Monniaux and Alberti [21] recently published a method for analyzing array pro-
grams by transforming them into array-free programs. They use the same Ga-
                    γ     γ2≤
                  ←
lois connections (−
                  −−−−−, ←−−
                           −−−→
                              −) as us, but they implement the abstract transfer
                    α→ −− α2≤
functions differently. While we transform the program into a system of non-
linear Horn clauses, they transform it into another program without arrays.
Definition 18 (Array analysis by transformation to an array-free program).
Non-array operations are left unchanged. A read v=a[i ]; is transformed into
i f ( i ==k ) x=ak ; e l s e havoc ( x ) ;
and a write a[ i]=v; is transformed into
i f ( i ==k ) ak=x ;

havoc(x) sets x to a nondeterministic value.

    Note that the “flat” encoding of programs into Horn clauses yields a system
of linear clauses. Thus, chaining Monniaux and Alberti [21] and a tool for
turning scalar program analysis problems into a system of Horn clauses would
yield linear clauses: the resulting encoding would thus be different from the
one produced by our approach. The reason is that their abstraction is actually
weaker than our abstraction. Let us see the Horn clauses corresponding to the
encoding of the “read” operation in their approach.
Definition 19 (Read statement, weakened). With the same notations as in
Def. 1, another forward abstract semantics for v=a[i ]; is given by the Horn


                                             25
clauses:
                            ∀x ∈ χ ∀i ∈ ι ∀v ∈ α ∀k ∈ ι ∀ak ∈ α
                                                                                      (111)
                      i 6= k ∧ I1♯ (x, i, k, ak ) =⇒ I2♯ (x, v, i, k, ak )
                            ∀x ∈ χ ∀i ∈ ι ∀v ∈ α ∀k ∈ ι ∀ak ∈ α
                                                                                      (112)
                                   I1♯ (x, i, i, v) =⇒ I2♯ (x, v, i, i, v)

Lemma 14. This forward abstract semantics is sound and equivalent to the for-
ward semantics of the transformation of a read statement according to Def. 18.
Proof. Soundness follows from this definition over-approximating Def. 1 (re-
moval of one conjunct). Equivalence to the forward semantics of the transformed
read statement is obvious.
    Using this weakened semantics to abstract arrays a and b by quadruplets
(x, a[x], y, b[y]), the correctness of Ex. 4 cannot be proved. Monniaux and Al-
berti [21] are able to prove the correctness of this program by using a more
expensive abstraction, where array a (current working array of the reversal)
and array b (original values of a) are abstracted using a set I ♯ of sextuplets
such that ∀0 ≤ x ≤ y < n ∀0 ≤ z < n (x, a[x], y, a[y], z, b[z]) ∈ I ♯ ; that is, a is
abstracted as in Sec. 4.
    Monniaux and Alberti [21, Sec. 5.5] are sometimes able to recover the loss
of precision induced by their abstractions by applying a form of quantifier elim-
ination. When they have an abstract state (x, k1 , ak1 , k2 , ak2 ), they reason that
a state is spurious if there exist k1′ (k1′ 6= k1 , k1′ ≤ k2 ) such that there is no ab-
stract state (x, k1′ , ak1′ , k2 , ak2 ). In intuitive terms, this means that if a[k2 ] = ak2
then there is no way to fill the value at cell a[k1 ] — but since all cells in the
array must have a value, this means that a[k2 ] = ak2 is impossible.
    Thus, one could have a “filtering” or reduction rule
                                                                             
                     ∀k1′ k1′ ≤ k2 =⇒ ∃ak1′ I1♯ (x, k1′ , ak1′ , k2 , ak2 )
                                                                                        (113)
                    ∧I1♯ (x, k1 , ak1 , k2 , ak2 ) =⇒ I2♯ (x, k1 , ak1 , k2 , ak2 )
                                                                                 
which would not change the concretization — γ2≤ I2♯ = γ2≤ I1♯ — but re-
duce the abstract state, which may later yield a more precise result (applying
the same sound abstract operation to two sets of abstract states with the same
concretization may yield two sets of abstract states with different concretiza-
tions).
    We cannot specify such a reduction rule using Horn clauses (because a ∀
on the left of =⇒ is effectively an existential in the prenex form, which is
banned). However, we can easily specify a partial filtering by instantiating the
universal quantifier on certain values, thereby obtaining a finite conjunction in
the antecedent of the implication. This is, in essence, what we gain by the use
of non-linear Horn clauses.
    Thus, using non-linear Horn clauses, we are able to integrate partial re-
ductions in the abstract domain to the fixed-point problem to solve, whereas
Monniaux and Alberti [21, Sec. 5.5] had to first solve the full fixed point problem
(analysis of the transformed program), then perform reductions. In general, it
is more precise to solve a fixed point problem using a precise operator f than

                                              26
to solve it using an imprecise operator g ≥ f , then reduce the final result.
We believe therefore that our approach improves in this respect upon that of
Monniaux and Alberti’s.
    Another difficulty they obviously faced was the limitations of the back-end
solvers that they could use. The integer acceleration engine Flata severely
limits the kind of transition relations that can be considered and scales poorly.
The abstract interpreter ConcurInterproc can infer disjunctive properties
(necessary to distinguish two slices in an array) only if given case splits using
observer Boolean variables; but the cost increases greatly (exponentially, in the
worst case) with the number of such variables.

7.3    Predicate abstraction, CEGAR and array interpolants
There exist a variety of approaches based on counterexample-guided abstraction     
refinement using interpolants (see also Sec. 6). In a nutshell: let τi (xi , xi+1 ) 0≤i<n
be the transition relations associated to a sequence of statements (assignments
and guards), where xi is the vector of active program variables after i steps. It
is impossible to reach the end of the sequence from the beginning if and only if
this formula is unsatisfiable:

                         τ0 (x0 , x1 ) ∧ · · · ∧ τn−1 (xn−1 , xn )              (114)

The proof of unsatisfiability of this formula, as obtained from a satisfiability
modulo theory (SMT) solver, may be convoluted. For the purpose of inferring
useful “candidate invariants” on the program, we would prefer “local” arguments
Ii , talking only about the variables at a given step:

                       Ii (xi ) ∧ τ0 (xi , xi+1 ) =⇒ Ii+1 (xi+1 )               (115)

and In = false. Such Ii are known as Craig interpolants [18, 20, 19] and are
typically obtained by reprocessing the proof of unsatisfiability from the SMT
solver. One difficulty with that approach is that not all interpolants are equally
interesting: one seeks interpolants that not only prove that an individual se-
quence of statements leading to a bad state is infeasible, but that generalize
well and can be used in a proof that many sequences of statements leading to a
bad state are infeasible, hopefully leading to a proof that no sequence can lead
to a bad state.
    Generating good interpolants from purely arithmetic problems is already a
difficult problem, and generating good universally quantified interpolants on
array properties has proved even more challenging [15, 1, 2].

7.4    Acceleration
It is possible to compute exactly the transitive closure of some transition rela-
tions, and thus to summarize some loop exactly. The class of transition relations
supported is however restricted.
    Bozga et al. [5] have proposed a method for accelerating certain transition
relations involving actions over arrays, which outputs the transitive closure in
the form of a counter automaton. Translating the counter automaton into a
first-order formula expressing the array properties however results in a loss of
precision.

                                            27
8    Conclusion and perspectives
We have proposed a generic approach to abstract programs and universal prop-
erties over arrays (and, more generally, arbitrary maps) by syntactic transfor-
mation into a system of Horn clauses without arrays, which is then sent to a
solver. This transformation is powerful enough that it can be used to prove, fully
automatically and within minutes, that the output of selection sort is sorted and
is a permutation of the input.
    While some solvers have difficulties with the kind of Horn systems that we
generate, some (e.g. Spacer) are capable of solving them quite well. We have
used the stock version of the solvers, without help from their designers or special
tuning, thus higher performance is to be expected in the future. Indeed, we feel
the kind of systems we generate would make good benchmarks for Horn solvers.
If the solver cannot find the invariants on its own, it can be helped by partial
invariants from the user. Also, if it finds a counterexample in the abstraction,
we propose a method for reconstructing a concrete counterexample (Sec. 6) or
triggering a refinement.

Existentials Our approach can be used, a fortiori, to prove or infer quantifier-
free properties, but not existentials. Future work could include quantifier in-
stantiation heuristics for existentials.

Backward analysis Our rules are for “forward analysis”: they express that
if configuration is possible at one step during one execution, then some config-
uration may be possible at the next step during that execution. We thus define
a super-set of all states reachable from program initialization, and the desired
property is proved if this set is included in the property.
    An alternative approach is “backward analysis”: find a super-set of the set
of all states reachable from a property violation, such that this set has empty
intersection with the initial states. A possible research direction would be to
derive backward rules and compare their efficiency to that of forward rules.

Procedures One approach to procedures is to consider a call to a procedure as
jump to the first node of the callee and a return as a jump back to each possible
caller node. Because this mixes together all calls to the same procedure, it can
lose a lot of precision; some tracking variables, abstracting the stack (in the
simplest case, the topmost call site), may be added to avoid precision loss. Such
an approach may be immediately combined with ours.
    In contrast, some other approaches encode procedures (or other program
fragments, such as the loop bodies) as binary input/output relations over the
variable state — or, rather, the fragment of the state that may be read or written
by the procedure. This maps well to Horn clauses: in the solution of the solver,
the predicate associated to a procedure summarizes its action. How to combine
this vision with our approach is a topic for future research.

High-level maps and sets Many programming languages provide libraries
for finite maps and (multi)sets. In this article, we have explained how to abstract
some, but not all of their features (Sec. 5.1) — for instance we do not provide an



                                        28
iterator for non-integer set element types. Future work should include reviewing
their features and common usage in order to design suitable abstractions.

Query-less analysis One advantage of some of earlier approaches (the ab-
stract interpretation ones from Sec. 7.1 and the program transformation from
Monniaux and Alberti [21]) is that they are capable of inferring what a pro-
gram does, or at least a meaningful abstraction of it (e.g. “at the end of this
program all cells in the array a contains 42”) as opposed to merely proving a
property supplied by the user. Our approach can achieve this as well, provided it
is used with a Horn clause solver that does not require queries and still provides
some interesting solution (a query-less Horn problem has a trivial, uninteresting
solution: “true” to all predicates).
    This Horn clause solver should however be capable of generating disjunctive
properties (e.g. (k < i ∧ ak = 0) ∨ (k ≥ i ∧ ak = 42)); thus a simple approach
by abstract interpretation of the Horn clauses in, say, a sub-class of the convex
polyhedra, will not do. We know of no such Horn solver; building one is an
interesting research challenge. Maybe certain partitioning approaches used in
sequential program verification [24, 13] may be transposed to Horn clauses.
    We have expressed an abstraction of the semantics of programs with array
reads and writes into a system of Horn clauses on scalar variables. Another
approach would be to directly work from Horn clauses on array variables, and
over-approximate the rules and under-approximate the queries into an array-free
Horn problem.

Objects We have considered simple programs operating over arrays or maps,
as opposed to a real-life programming language with objects, references or,
horror, pointer arithmetic. Yet, our approach can be adapted to such languages.
One can indeed see each object field name in a language such as Java (e.g.
String x; ) as a map from object references to values (here, of type String). The
reference may be an index (perhaps i if the object is the i-th object allocated)
or a more complex record of the site of allocation.

Pointers Languages with pointers, pointer arithmetic and, worse, access to
an object of a type through a pointer of an incompatible type (not uncommon
in traditional C programming), can be handled by seeing the memory as an
array of bytes, but this leads to impractically inefficient analysis. It is however
often possible to segment the memory into independent variables (never accessed
through pointers, or at least accessed only through pointers at known locations)
and a number of disjoint arrays. Our analysis can then be used over these arrays.


References
 [1] F. Alberti et al. “An extension of lazy abstraction with interpolation for
     programs with arrays”. In: Formal Methods in Systems Design 45.1 (2014),
     pp. 63–109.
 [2] Francesco Alberti and David Monniaux. “Polyhedra to the rescue of array
     interpolants”. In: Symposium on applied computing (Software Verification
     & Testing). ACM, 2015.


                                        29
 [3] Blanchet et al. “A Static Analyzer for Large Safety-Critical Software”. In:
     PLDI. ACM. 2003, pp. 196–207. doi: 10.1145/781131.781153. arXiv:cs/0701193.
 [4] Bruno Blanchet et al. “Design and Implementation of a Special-Purpose
     Static Program Analyzer for Safety-Critical Real-Time Embedded Soft-
     ware”. In: The Essence of Computation: Complexity, Analysis, Transfor-
     mation. LNCS 2566. Springer, 2002, pp. 85–108. doi: 10.1007/3-540-36377-7_5.
 [5] M. Bozga et al. “Automatic Verification of Integer Array Programs”. In:
     CAV. 2009, pp. 157–172.
 [6] A.R. Bradley, Z. Manna, and H.B. Sipma. “What’s Decidable About Ar-
     rays?” In: VMCAI. 2006, pp. 427–442.
 [7] Patrick Cousot and Radhia Cousot. “Abstract Interpretation Frameworks”.
     In: J. Log. Comput. 2.4 (1992), pp. 511–547. doi: 10.1093/logcom/2.4.511.
 [8] Patrick Cousot and Radhia Cousot. “Invited Talk: Higher Order Abstract
     Interpretation. Application to Comportment Analysis Generalizing Strict-
     ness, Termination, Projection, and PER Analysis”. In: IEEE International
     Conference on Computer Languages. IEEE, 1994, pp. 95–112.
 [9] Patrick Cousot, Radhia Cousot, and Francesco Logozzo. “A parametric
     segmentation functor for fully automatic and scalable array content analy-
     sis”. In: POPL. ACM, 2011, pp. 105–118. doi: 10.1145/1926385.1926399.
[10] D. Gopan, T.W. Reps, and S. Sagiv. “A framework for numeric analysis
     of array operations”. In: POPL. 2005, pp. 338–350.
[11] Nicolas Halbwachs and Mathias Péron. “Discovering properties about
     arrays in simple programs”. In: PLDI. ACM, 2008, pp. 339–348. doi:
     10.1145/1375581.1375623.
[12] J.Y. Halpern. “Presburger arithmetic with unary predicates is Π11 com-
     plete”. In: J. Symbolic Logic 56.2 (1991), pp. 637–642. issn: 0022-4812.
     doi: 10.2307/2274706. url: http://dx.doi.org/10.2307/2274706.
[13] J. Henry, D. Monniaux, and M. Moy. “Succinct Representations for Ab-
     stract Interpretation”. In: SAS. 2012, pp. 283–299.
[14] Kryštof Hoder and Nikolaj Bjørner. “Generalized Property Directed Reach-
     ability”. In: SAT. Vol. 7317. Lecture Notes in Computer Science. Springer,
     2012, pp. 157–171. isbn: 978-3-642-31611-1. doi: 10.1007/978-3-642-31612-8_13.
[15] R. Jhala and K.L. McMillan. “Array Abstractions from Proofs”. In: CAV.
     2007, pp. 193–206.
[16] Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. “SMT-Based Model
     Checking for Recursive Programs”. In: Computer Aided Verification - 26th
     International Conference, CAV 2014, Held as Part of the Vienna Summer
     of Logic, VSL 2014, Vienna, Austria, July 18-22, 2014. Proceedings. Ed.
     by Armin Biere and Roderick Bloem. Vol. 8559. Lecture Notes in Com-
     puter Science. Springer, 2014, pp. 17–34. isbn: 978-3-319-08866-2. doi:
     10.1007/978-3-319-08867-9_2.




                                      30
[17] Anvesh Komuravelli et al. “Automatic Abstraction in SMT-Based Un-
     bounded Software Model Checking”. In: Computer Aided Verification -
     25th International Conference, CAV 2013, Saint Petersburg, Russia, July
     13-19, 2013. Proceedings. Ed. by Natasha Sharygina and Helmut Veith.
     Vol. 8044. Lecture Notes in Computer Science. Springer, 2013, pp. 846–
     862. isbn: 978-3-642-39798-1. doi: 10.1007/978-3-642-39799-8_59.
[18] Kenneth L. McMillan. “Applications of Craig Interpolation to Model Check-
     ing”. In: ICATPN. Vol. 3536. LNCS. Springer, 2005, pp. 15–16. isbn: 3-
     540-26301-2. doi: 10.1007/11494744_2.
[19] K.L. McMillan. “Interpolants from Z3 proofs.” In: FMCAD. 2011, pp. 19–
     27.
[20] K.L. McMillan. “Lazy Abstraction with Interpolants”. In: CAV. 2006,
     pp. 123–136.
[21] David Monniaux and Francesco Alberti. “A simple abstraction of arrays
     and maps by program translation”. In: Static analysis symposium (SAS).
     Lecture Notes in Computer Science. To appear, available at http://arxiv.org/abs/1506.04161.
     Springer, 2015.
[22] Mathias Péron. “Contributions to the Static Analysis of Programs Han-
     dling Arrays”. Theses. Université de Grenoble, Sept. 2010. url: https://tel.archives-ouvertes.fr/
[23] Valentin Perrelle. “Analyse statique de programmes manipulant des tableaux”.
     Theses. Université de Grenoble, Feb. 2013. url: https://tel.archives-ouvertes.fr/tel-00973892.
[24] Xavier Rival and Laurent Mauborgne. “The trace partitioning abstract do-
     main”. In: ACM Trans. Program. Lang. Syst. 29.5 (2007). doi: 10.1145/1275497.1275501.
[25] Philipp Rümmer, Hossein Hojjat, and Viktor Kuncak. “Classifying and
     Solving Horn Clauses for Verification”. In: VSTTE 2013, revised selected
     papers. Ed. by Ernie Cohen and Andrey Rybalchenko. Vol. 8164. Lecture
     Notes in Computer Science. Springer, 2014, pp. 1–21. doi: 10.1007/978-3-642-54108-7_1.
[26] Philipp Rümmer, Hossein Hojjat, and Viktor Kuncak. “Disjunctive In-
     terpolants for Horn-Clause Verification”. In: Computer-aided verification
     (CAV). Ed. by Natasha Sharygina and Helmut Veith. Vol. 8044. Lecture
     Notes in Computer Science. Springer, 2013, pp. 347–363. isbn: 978-3-642-
     39798-1. doi: 10.1007/978-3-642-39799-8_24.




                                     31
A       Horn clause problems

                                    Listing 8: Array fill 1D
( s e t − l o g i c HORN)

( declar e−fun loop ( I n t I n t I n t I n t ) Bool ) ; n i k a [ k ]
( declar e−fun w r i t e ( I n t I n t I n t I n t ) Bool ) ; n i k a [ k ]
( declar e−fun i n c r ( I n t I n t I n t I n t ) Bool ) ; n i k a [ k ]
( declar e−fun end ( I n t I n t I n t ) Bool ) ; n a [ ]

( a s s e r t ( f o r a l l ( ( n I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( and (<= 0 k ) (< k n ) ) ( loop n 0 k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( and (< i n ) ( loop n i k ak ) ) ( w r i t e n i k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( and ( d i s t i n c t i k ) ( w r i t e n i k ak ) ) ( i n c r n i k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( w r i t e n i k ak ) ( i n c r n i i 4 2 ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( i n c r n i k ak ) ( loop n (+ i 1 ) k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( and (>= i n ) ( loop n i k ak ) ) ( end n k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( and (>= k 0 ) (< k n ) ( end n k ak ) ) (= ak 4 2 ) ) ) )

( check−sat )
( get−model )

                             Listing 9: Array fill 1D, even-odd
( s e t − l o g i c HORN)

( declar e−fun loop ( I n t I n t I n t I n t ) Bool ) ; n i k a [ k ]
( declar e−fun w r i t e ( I n t I n t I n t I n t ) Bool ) ; n i k a [ k ]
( declar e−fun i n c r ( I n t I n t I n t I n t ) Bool ) ; n i k a [ k ]
( declar e−fun end ( I n t I n t I n t ) Bool ) ; n a [ ]

( a s s e r t ( f o r a l l ( ( n I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( and (<= 0 k ) (< k n ) ) ( loop n 0 k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( and (< i n ) ( loop n i k ak ) ) ( w r i t e n i k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( and ( d i s t i n c t i k ) ( w r i t e n i k ak ) ) ( i n c r n i k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( w r i t e n i k ak ) ( i n c r n i i (mod i 2 ) ) ) ) )


                                                 32
( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( i n c r n i k ak ) ( loop n (+ i 1 ) k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( and (>= i n ) ( loop n i k ak ) ) ( end n k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( end n ( ∗ 2 k ) ak ) (= ak 0 ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( end n (+ ( ∗ 2 k ) 1 ) ak ) (= ak 1 ) ) ) )

( check−sat )

                                   Listing 10: Array reverse
( s e t − l o g i c HORN)

( declar e−fun i n i t ( I n t I n t I n t I n t I n t ) Bool ) ; n k a [ k ] l a0 [ l
     ]
( declar e−fun loop ( I n t I n t I n t I n t I n t I n t ) Bool ) ; n i k a [ k ]
     l a0 [ l ]
( declar e−fun read1 ( I n t I n t I n t I n t I n t I n t ) Bool ) ; n i k a [ k ]
       l a0 [ l ]
( declar e−fun read2 ( I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; n i
     tmp1 k a [ k ] l a0 [ l ]
( declar e−fun w r i t e 1 ( I n t I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; n
       i tmp1 tmp2 k a [ k ] l a0 [ l ]
( declar e−fun w r i t e 2 ( I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; n i
     tmp1 k a [ k ] l a0 [ l ]
( declar e−fun i n c r ( I n t I n t I n t I n t I n t I n t ) Bool ) ; n i k a [ k ]
     l a0 [ l ]
( declar e−fun end ( I n t I n t I n t I n t I n t ) Bool ) ; n k a [ k ] l a0 [ l ]

( a s s e r t ( f o r a l l ( ( n I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( and (<= 0 k ) (< k n ) )
            ( i n i t n k ak k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( k I n t ) ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )
   (=> ( and (<= 0 k ) (< k n ) (<= 0 l ) (< l n ) ( d i s t i n c t k l ) )
            ( i n i t n k ak l a 0 l ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( k I n t ) ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )
   (=> ( i n i t n k ak l a 0 l )
            ( loop n 0 k ak l a 0 l ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( k I n t ) ( ak I n t ) ( l I n t ) ( a 0 l
       Int ) )
    ( l e t ( ( j (− n (+ i 1 ) ) ) )
        (=> ( and (< i j ) ( loop n i k ak l a 0 l ) )
              ( read1 n i k ak l a 0 l ) ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( tmp1 I n t )
        ( k I n t ) ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )


                                                  33
   ( l e t ( ( j (− n (+ i 1 ) ) ) )
       (=> ( and ( d i s t i n c t i k )
                   ( read1 n i k ak l a 0 l )
                   ( read1 n i i tmp1 l a 0 l ) )
             ( read2 n i tmp1 k ak l a 0 l ) ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( tmp1 I n t )
        ( k I n t ) ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )
    ( l e t ( ( j (− n (+ i 1 ) ) ) )
        (=> ( read1 n i i tmp1 l a 0 l )
              ( read2 n i tmp1 i tmp1 l a 0 l ) ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( tmp1 I n t ) ( tmp2 I n t )
        ( k I n t ) ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )
    ( l e t ( ( j (− n (+ i 1 ) ) ) )
        (=> ( and ( d i s t i n c t j k )
                        ( read2 n i tmp1 k ak l a 0 l )
                        ( read2 n i tmp1 j tmp2 l a 0 l ) )
              ( w r i t e 1 n i tmp1 tmp2 k ak l a 0 l ) ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( tmp1 I n t ) ( tmp2 I n t )
        ( k I n t ) ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )
    ( l e t ( ( j (− n (+ i 1 ) ) ) )
        (=> ( and ( read2 n i tmp1 j tmp2 l a 0 l ) )
              ( w r i t e 1 n i tmp1 tmp2 j tmp2 l a 0 l ) ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( tmp1 I n t ) ( tmp2 I n t )
        ( k I n t ) ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )
    ( l e t ( ( j (− n (+ i 1 ) ) ) )
        (=> ( and ( w r i t e 1 n i tmp1 tmp2 k ak l a 0 l ) ( d i s t i n c t i k ) )
              ( w r i t e 2 n i tmp1 k ak l a 0 l ) ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( tmp1 I n t ) ( tmp2 I n t )
        ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )
    ( l e t ( ( j (− n (+ i 1 ) ) ) )
        (=> ( w r i t e 1 n i tmp1 tmp2 i ak l a 0 l )
              ( w r i t e 2 n i tmp1 i tmp2 l a 0 l ) ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( tmp1 I n t )
                              ( k I n t ) ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )
    ( l e t ( ( j (− n (+ i 1 ) ) ) )
        (=> ( and ( w r i t e 2 n i tmp1 k ak l a 0 l ) ( d i s t i n c t j k ) )
              ( i n c r n i k ak l a 0 l ) ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( tmp1 I n t )
                              ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )
    ( l e t ( ( j (− n (+ i 1 ) ) ) )
        (=> ( w r i t e 2 n i tmp1 j ak l a 0 l )
              ( i n c r n i j tmp1 l a 0 l ) ) ) ) )

( assert ( f o r a l l ( ( n Int ) ( i Int )
                         ( k I n t ) ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )
   ( l e t ( ( j (− n (+ i 1 ) ) ) )
       (=> ( i n c r n i k ak l a 0 l )


                                                  34
             ( loop n (+ i 1 ) k ak l a 0 l ) ) ) ) )

( assert ( f o r a l l ( ( n Int ) ( i Int )
                         ( k I n t ) ( ak I n t ) ( l I n t ) ( a 0 l I n t ) )
   ( l e t ( ( j (− n (+ i 1 ) ) ) )
       (=> ( and (>= i j ) ( loop n i k ak l a 0 l ) )
             ( end n k ak l a 0 l ) ) ) ) )

( a s s e r t ( f o r a l l ( ( n I n t ) ( i I n t ) ( ak I n t ) ( a 0 l I n t ) )
    ( l e t ( ( j (− n (+ i 1 ) ) ) )
        (=> ( and (>= i 0 ) (< i n )
                       ( end n i ak j a 0 l ) )
              (= ak a 0 l ) ) ) ) )

; ( ass e rt ( f o r a l l ( ( n Int ) ( i Int ) ( ai Int ) ( j Int ) ( a0j Int ) )
;    ( n o t ( end n i a i j a 0 j ) ) ) )

( check−sat )

                                 Listing 11: Real-index maps
( s e t − l o g i c HORN)

( declar e−fun i n i t ( Real I n t ) Bool )              ;   x ax
( declar e−fun w1 ( Real I n t ) Bool ) ;                 x   ax
( declar e−fun w2 ( Real I n t ) Bool ) ;                 x   ax
( declar e−fun e x i t ( Real I n t ) Bool )              ;   x ax

( a s s e r t ( f o r a l l ( ( x Real ) ) ( i n i t x 0 ) ) )

( a s s e r t ( f o r a l l ( ( x Real ) ( ax I n t ) )
   (=> ( and ( i n i t x ax ) ( d i s t i n c t x 1 ) )
            (w1 x ax ) ) ) )

( a s s e r t ( f o r a l l ( ( ax I n t ) )
   (=> ( i n i t 1 ax ) ( i n i t 1 1 0 ) ) ) )

( a s s e r t ( f o r a l l ( ( x Real ) ( ax I n t ) )
   (=> ( and (w1 x ax ) ( d i s t i n c t x 2 ) )
            (w2 x ax ) ) ) )

( a s s e r t ( f o r a l l ( ( ax I n t ) )
   (=> (w1 2 ax ) (w2 2 2 0 ) ) ) )

( a s s e r t ( f o r a l l ( ( x Real ) ( ax I n t ) )
   (=> ( and (w2 x ax ) ( d i s t i n c t x 3 ) )
            ( e x i t x ax ) ) ) )

( a s s e r t ( f o r a l l ( ( ax I n t ) )
   (=> (w2 3 ax ) ( e x i t 3 3 0 ) ) ) )

( a s s e r t ( f o r a l l ( ( x Real ) ( ax I n t ) )
   (=> ( e x i t x ax ) (>= ax 0 ) ) ) )

( a s s e r t ( f o r a l l ( ( x Real ) ( ax I n t ) )


                                                  35
  (=> ( e x i t x ax ) (<= ax 3 0 ) ) ) )

( check−sat )

                                   Listing 12: Array fill 2D
( s e t − l o g i c HORN)

( declar e−fun i n i t ( I n t I n t I n t I n t I n t ) Bool ) ; m n x y a [ x , y ]
( declar e−fun l o o p i ( I n t I n t I n t I n t I n t I n t ) Bool ) ; m n i x y
     a [x , y]
( declar e−fun l o o p j ( I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; m n i
     j x y a [x , y]
( declar e−fun w r i t e ( I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; m n i
     j x y a [x , y]
( declar e−fun i n c r j ( I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; m n i
     j x y a [x , y]
( declar e−fun i n c r i ( I n t I n t I n t I n t I n t I n t ) Bool ) ; m n i x y
     a [x , y]
( declar e−fun end ( I n t I n t I n t I n t I n t ) Bool ) ; m n x y a [ x , y ]

( a s s e r t ( f o r a l l ( (m I n t ) ( n I n t ) ( x I n t ) ( y I n t ) ( axy I n t ) )
   (=> ( and (<= 0 x ) (< x m) (<= 0 y ) (< y n ) ) ( i n i t m n x y axy
           ))))

( a s s e r t ( f o r a l l ( (m I n t ) ( n I n t ) ( x I n t ) ( y I n t ) ( axy I n t ) )
   (=> ( i n i t m n x y axy ) ( l o o p i m n 0 x y axy ) ) ) )

( a s s e r t ( f o r a l l ( (m I n t ) ( n I n t ) ( i I n t ) ( x I n t ) ( y I n t ) ( axy
       Int ) )
   (=> ( and (< i m) ( l o o p i m n i x y axy ) )
            ( l o o p j m n i 0 x y axy ) ) ) )

( a s s e r t ( f o r a l l ( (m I n t ) ( n I n t ) ( i I n t ) ( x I n t ) ( y I n t ) ( axy
       Int ) )
   (=> ( and (>= i m) ( l o o p i m n i x y axy ) )
            ( end m n x y axy ) ) ) )

( a s s e r t ( f o r a l l ( (m I n t ) ( n I n t ) ( i I n t ) ( j I n t ) ( x I n t ) ( y I n t
       ) ( axy I n t ) )
   (=> ( and (< j n ) ( l o o p j m n i j x y axy ) )
            ( w r i t e m n i j x y axy ) ) ) )

( a s s e r t ( f o r a l l ( (m I n t ) ( n I n t ) ( i I n t ) ( j I n t ) ( x I n t ) ( y I n t
       ) ( axy I n t ) )
   (=> ( and (>= j n ) ( l o o p j m n i j x y axy ) )
            ( i n c r i m n i x y axy ) ) ) )

( a s s e r t ( f o r a l l ( (m I n t ) ( n I n t ) ( i I n t ) ( j I n t ) ( x I n t ) ( y I n t
       ) ( axy I n t ) )
   (=> ( and ( w r i t e m n i j x y axy )
                      ( not ( and (= i x ) (= j y ) ) ) )
            ( i n c r j m n i j x y axy ) ) ) )

( a s s e r t ( f o r a l l ( (m I n t ) ( n I n t ) ( i I n t ) ( j I n t ) ( a i j I n t ) )


                                                 36
  (=> ( w r i t e m n i j i j a i j )
      ( i n c r j m n i j i j 42) ) ) )

( a s s e r t ( f o r a l l ( (m I n t ) ( n I n t ) ( i I n t ) ( j I n t ) ( x I n t ) ( y I n t
       ) ( axy I n t ) )
   (=> ( i n c r j m n i j x y axy )
            ( l o o p j m n i (+ j 1 ) x y axy ) ) ) )

( a s s e r t ( f o r a l l ( (m I n t ) ( n I n t ) ( i I n t ) ( x I n t ) ( y I n t ) ( axy
       Int ) )
   (=> ( i n c r i m n i x y axy )
            ( l o o p i m n (+ i 1 ) x y axy ) ) ) )

( a s s e r t ( f o r a l l ( (m I n t ) ( n I n t ) ( x I n t ) ( y I n t ) ( axy I n t ) )
   (=> ( end m n x y axy ) (= axy 4 2 ) ) ) )

( check−sat )

                                 Listing 13: Find minimum
( s e t − l o g i c HORN)

( declar e−fun i n i t ( I n t I n t I n t I n t ) Bool ) ; l h k a [ k ]
( declar e−fun read1 ( I n t I n t I n t I n t ) Bool ) ; l h k a [ k ]

( declar e−fun loop ( I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; l h i p
      b k a[k]

( declar e−fun read2 ( I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; l h i
     p b k a[k]
( declar e−fun t e s t ( I n t I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; l h
      i p b v k a[k]

( declar e−fun end ( I n t I n t I n t I n t I n t I n t ) Bool ) ; l h p b k a [
     k]

( a s s e r t ( f o r a l l ( ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( b I n t ) )
   (=> ( and ( i n i t l h k ak ) (< l (− h 1 ) ) )
            ( read1 l h k ak ) ) ) )

( a s s e r t ( f o r a l l ( ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( b I n t ) )
   (=> ( and ( read1 l h k ak )
                    ( read1 l h l b )
                    ( distinct k l ) )
            ( loop l h (+ l 1 ) l b k ak ) ) ) )

( assert ( f o r a l l ( ( l Int ) (h Int ) (b Int ) )
   (=> ( read1 l h l b )
       ( loop l h (+ l 1 ) l b l b ) ) ) )

( assert ( f o r a l l ( ( l Int ) (h Int ) ( i Int ) (p Int ) (b Int ) (k Int
     ) ( ak I n t ) )
   (=> ( and ( loop l h i p b k ak ) (< i h ) )
        ( read2 l h i p b k ak ) ) ) )



                                                 37
( assert ( f o r a l l ( ( l Int ) (h Int ) ( i Int ) (p Int ) (b Int ) (v Int
     ) ( k I n t ) ( ak I n t ) )
   (=> ( and ( read2 l h i p b k ak )
                 ( read2 l h i p b i v )
                 ( distinct k i ) )
        ( t e s t l h i p b v k ak ) ) ) )

( assert ( f o r a l l ( ( l Int ) (h Int ) ( i Int ) (p Int ) (b Int ) (v Int
     ))
   (=> ( read2 l h i p b i v )
        ( test l h i p b v i v) ) ) )

( assert ( f o r a l l ( ( l Int ) (h Int ) ( i Int ) (p Int ) (b Int ) (v Int
     ) ( k I n t ) ( ak I n t ) )
   (=> ( and ( t e s t l h i p b v k ak )
               (< v b ) )
        ( loop l h (+ i 1 ) i v k ak ) ) ) )

( assert ( f o r a l l ( ( l Int ) (h Int ) ( i Int ) (p Int ) (b Int ) (v Int
     ) ( k I n t ) ( ak I n t ) )
   (=> ( and ( t e s t l h i p b v k ak )
               (>= v b ) )
        ( loop l h (+ i 1 ) p b k ak ) ) ) )

( assert ( f o r a l l ( ( l Int ) (h Int ) ( i Int ) (p Int ) (b Int ) (k Int
     ) ( ak I n t ) )
   (=> ( and ( loop l h i p b k ak )
              (>= i h ) )
        ( end l h p b k ak ) ) ) )

; Initialization
( a s s e r t ( f o r a l l ( ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) )
    ( i n i t l h k ak ) ) )

; Pr o p e r t ie s to prove
( a s s e r t ( f o r a l l ( ( l I n t ) ( h I n t ) ( p I n t ) ( b I n t ) ( k I n t ) ( ak
       Int ) )
   (=> ( end l h p b k ak )
           (>= p l ) ) ) )

( a s s e r t ( f o r a l l ( ( l I n t ) ( h I n t ) ( p I n t ) ( b I n t ) ( k I n t ) ( ak
       Int ) )
   (=> ( end l h p b k ak )
           (< p h ) ) ) )

( a s s e r t ( f o r a l l ( ( l I n t ) ( h I n t ) ( p I n t ) ( b I n t ) ( k I n t ) ( ap
       Int ) )
   (=> ( end l h p b p ap )
            (= b ap ) ) ) )

( a s s e r t ( f o r a l l ( ( l I n t ) ( h I n t ) ( p I n t ) ( b I n t ) ( k I n t ) ( ap
       I n t ) ( ak I n t ) )
   (=> ( and (>= k l )
                   (< k h )


                                                 38
              ( end l h p b k ak ) )
         (<= b ak ) ) ) )

( check−sat )

                            Listing 14: Selection sort: sortedness
; SELECTION SORT
; S o l v e d i n 6 ’ by S p a c e r 2015−07−01
       0dfed9c654a6f715b8660ff1d27de74fbfc41916

( s e t − l o g i c HORN)

( declar e−fun i n i t ( I n t I n t I n t I n t I n t I n t ) Bool ) ; l 0 h k a [ k ]
      k2 a [ k2 ]
( declar e−fun o u t e r l o o p ( I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; l 0
      l h k a [ k ] k2 a [ k2 ]
( declar e−fun e x i t ( I n t I n t I n t I n t I n t I n t ) Bool ) ; l 0 h k a [ k ]
      k2 a [ k2 ]

( declar e−fun read1 ( I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; l 0 l h
      k a [ k ] k2 a [ k2 ]

( declar e−fun loop ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t )
      Bool ) ; l 0 l h i p b f k a [ k ] k2 a [ k2 ]

( declar e−fun read2 ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
     ) Bool ) ; l 0 l h i p b f k a [ k ] k2 a [ k2 ]
( declar e−fun t e s t ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
     I n t ) Bool ) ; l 0 l h i p b v f k a [ k ] k2 a [ k2 ]

( declar e−fun w r i t e 1 ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t )
     Bool ) ; l 0 l h p b f k a [ k ] k2 a [ k2 ]
( declar e−fun w r i t e 2 ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t )
     Bool ) ; l 0 l h p b f k a [ k ] k2 a [ k2 ]
( declar e−fun endswap ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t )
     Bool ) ; l 0 l h p b f k a [ k ] k2 a [ k2 ]
( declar e−fun i n c r ( I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; l 0 l h
     k a [ k ] k2 a [ k2 ]

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) (
       ak2 I n t ) )
   (=> ( and ( i n i t l 0 h k ak k2 ak2 ) (<= l 0 h ) )
            ( o u t e r l o o p l 0 l 0 h k ak k2 ak2 ) ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( k2
       I n t ) ( ak2 I n t ) )
   (=> ( and ( o u t e r l o o p l 0 l h k ak k2 ak2 ) (< l (− h 1 ) ) )
            ( read1 l 0 l h k ak k2 ak2 ) ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( k2
       I n t ) ( ak2 I n t ) )
   (=> ( and ( o u t e r l o o p l 0 l h k ak k2 ak2 ) (>= l (− h 1 ) ) )
            ( e x i t l 0 h k ak k2 ak2 ) ) ) )



                                                39
( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( b I n t ) ( k I n t ) ( ak
       I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( read1 l 0 l h k ak k2 ak2 )
                    ( read1 l 0 l h l b k2 ak2 )
                    ( d i s t i n c t k l ) (< l k2 ) )
            ( loop l 0 l h (+ l 1 ) l b b k ak k2 ak2 ) ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( b I n t ) ( k I n t ) ( ak
       I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( read1 l 0 l h k ak k2 ak2 )
                    ( read1 l 0 l h k ak l b )
                    ( d i s t i n c t k2 l ) (< k l ) )
            ( loop l 0 l h (+ l 1 ) l b b k ak k2 ak2 ) ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( b I n t ) ( k2 I n t ) ( ak2
         Int ) )
   (=> ( and (< l k2 ) ( read1 l 0 l h l b k2 ak2 ) )
            ( loop l 0 l h (+ l 1 ) l b b l b k2 ak2 ) ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( b I n t ) ( k I n t ) ( ak
       Int ) )
   (=> ( and (<= k l ) ( read1 l 0 l h k ak l b ) )
            ( loop l 0 l h (+ l 1 ) l b b k ak l b ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( loop l 0 l h i p b f k ak k2 ak2 ) (< i h ) )
          ( read2 l 0 l h i p b f k ak k2 ak2 ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( v I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( read2 l 0 l h i p b f k ak k2 ak2 )
                   ( read2 l 0 l h i p b f i v k2 ak2 )
                   ( d i s t i n c t k i ) (< i k2 ) )
          ( t e s t l 0 l h i p b v f k ak k2 ak2 ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( v I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( read2 l 0 l h i p b f k ak k2 ak2 )
                   ( read2 l 0 l h i p b f k ak i v )
                   ( d i s t i n c t k2 i ) (< k i ) )
          ( t e s t l 0 l h i p b v f k ak k2 ak2 ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( v I n t ) ( f I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and (< i k2 ) ( read2 l 0 l h i p b f i v k2 ak2 ) )
          ( t e s t l 0 l h i p b v f i v k2 ak2 ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( v I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) )
   (=> ( and (<= k i ) ( read2 l 0 l h i p b f k ak i v ) )
          ( t e s t l 0 l h i p b v f k ak i v ) ) ) )




                                                40
( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( v I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( t e s t l 0 l h i p b v f k ak k2 ak2 )
                (< v b ) )
          ( loop l 0 l h (+ i 1 ) i v f k ak k2 ak2 ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( v I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( t e s t l 0 l h i p b v f k ak k2 ak2 )
                (>= v b ) )
          ( loop l 0 l h (+ i 1 ) p b f k ak k2 ak2 ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( loop l 0 l h i p b f k ak k2 ak2 )
                    (>= i h ) )
          ( w r i t e 1 l 0 l h p b f k ak k2 ak2 ) ) ) )

; The Swap , 1 s t w r i t e
( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( d i s t i n c t l k ) ( d i s t i n c t l k2 )
                    ( w r i t e 1 l 0 l h p b f k ak k2 ak2 ) )
          ( w r i t e 2 l 0 l h p b f k ak k2 ak2 ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( ak I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( d i s t i n c t l k2 )
                    ( w r i t e 1 l 0 l h p b f l ak k2 ak2 ) )
          ( w r i t e 2 l 0 l h p b f l b k2 ak2 ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ak I n t ) ( ak2 I n t ) )
   (=> ( and ( d i s t i n c t l k )
                    ( w r i t e 1 l 0 l h p b f k ak l ak2 ) )
          ( w r i t e 2 l 0 l h p b f k ak l b ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( ak I n t ) )
   (=> ( w r i t e 1 l 0 l h p b f l ak l ak )
          ( write2 l 0 l h p b f l b l b ) ) ) )

; The Swap , 2nd w r i t e
( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( d i s t i n c t p k ) ( d i s t i n c t p k2 )
                ( w r i t e 2 l 0 l h p b f k ak k2 ak2 ) )
          ( endswap l 0 l h p b f k ak k2 ak2 ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( ak I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( and ( d i s t i n c t p k2 )
                 ( w r i t e 2 l 0 l h p b f p ak k2 ak2 ) )
          ( endswap l 0 l h p b f p f k2 ak2 ) ) ) )


                                              41
( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ak I n t ) ( ak2 I n t ) )
   (=> ( and ( d i s t i n c t p k )
                ( w r i t e 2 l 0 l h p b f k ak p ak2 ) )
          ( endswap l 0 l h p b f k ak p f ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( ak I n t ) )
   (=> ( w r i t e 2 l 0 l h p b f p ak p ak )
          ( endswap l 0 l h p b f p f p f ) ) ) )

; i n c r and o u t e r l o o p
( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) ( ak2 I n t ) )
   (=> ( endswap l 0 l h p b f k ak k2 ak2 )
          ( i n c r l 0 l h k ak k2 ak2 ) ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( k2
       I n t ) ( ak2 I n t ) )
   (=> ( i n c r l 0 l h k ak k2 ak2 )
            ( o u t e r l o o p l 0 (+ l 1 ) h k ak k2 ak2 ) ) ) )

; Initialization
( a s s e r t ( f o r a l l ( ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) ( ak2
         Int ) )
   (=> (< k k2 ) ( i n i t l h k ak k2 ak2 ) ) ) )
( a s s e r t ( f o r a l l ( ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) )
    ( i n i t l h k ak k ak ) ) )

; Various i n v a r i a n t s

; Removing t h i s o n e y i e l d s 1 8 . 2 s w i t h Z3 /PDR
      b1d649fe1c842208f701c6b1d1dfa5d17e8dc679
; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
      I n t ) ( k I n t ) ( a k I ; n t ) ( k2 I n t ) ( a k 2 I n t ) )
; (=> ( w r i t e 1 l 0 l h p b f k a k k2 a k 2 )
;           (>= p l ) ) ) )

; Removing t h e f i r s t two o n e s y i e l d s 1 0 . 5 s w i t h Z3 /PDR
      b1d649fe1c842208f701c6b1d1dfa5d17e8dc679
; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
      I n t ) ( k I n t ) ( a k I n t ) ( k2 I n t ) ( a k 2 I n t ) )
; (=> ( w r i t e 1 l 0 l h p b f k a k k2 a k 2 )
;           (< p h ) ) ) )

; Removing t h e f i r s t t h r e e o n e s y i e l d s 1 1 . 5 s w i t h Z3 /PDR
      b1d649fe1c842208f701c6b1d1dfa5d17e8dc679
; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
      I n t ) ( ap I n t ) )
; (=> ( w r i t e 1 l 0 l h p b f p ap p ap )
;           (= b ap ) ) ) )




                                                42
; Removing t h e f i r s t f o u r o n e s y i e l d s 1 7 . 1 s w i t h Z3 /PDR
      b1d649fe1c842208f701c6b1d1dfa5d17e8dc679
; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
      Int ) ( al Int ) )
; (=> ( w r i t e 1 l 0 l h p b f l a l l a l )
;         (= f a l ) ) ) )

; Removing t h e f i r s t f i v e o n e s y i e l d s 6 . 2 s w i t h Z3 /PDR
      b1d649fe1c842208f701c6b1d1dfa5d17e8dc679
; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
      I n t ) ( k I n t ) ( ak I n t ) )
; (=> ( and (>= k l )
;                 (< k h )
;                 ( w r i t e 1 l 0 l h p b f k ak k ak ) )
;           (<= b a k ) ) ) )

; Removing t h e f i r s t s i x o n e s y i e l d s 6 . 7 s w i t h Z3 /PDR
      b1d649fe1c842208f701c6b1d1dfa5d17e8dc679
; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
      I n t ) ( k I n t ) ( ak I n t ) ( a l I n t ) )
; (=> ( and (>= k l )
;                 (< k h )
;                 ( endswap l 0 l h p b f l a l k a k ) )
;           (<= a l a k ) ) ) )

; Removing t h e f i r s t s e v e n o n e s y i e l d s 4 . 6 s w i t h Z3 /PDR
       b1d649fe1c842208f701c6b1d1dfa5d17e8dc679
; 8 . 5 s i n Z3 /PDR 2015−06−01
         168ea2e948bf6d946e163a5a1af0ddf084552cd6
; 5 . 5 s i n Z3 / S p a c e r 2014−08−06
         b1d649fe1c842208f701c6b1d1dfa5d17e8dc679
; ( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( a l
         Int ) )
; (=> ( and (>= k l )
;                    (< k h )
;                     ( i n c r l 0 l h l a l k ak ) )
;             (<= a l a k ) ) ) )

; T h i s h i n t s e e m s REALLY NECESSARY: w i t h i t
; Z / S p a c e r 2014−08−06 b 1 d 6 4 9 f e 1 c 8 4 2 2 0 8 f 7 0 1 c 6 b 1 d 1 d f a 5 d 1 7 e 8 d c 6 7 9
      ta ke s 2.4 s
; w i t h o u t i t , no c o n v e r g e n c e a f t e r 9min

; Removing t h i s e x t r a c o n d i t i o n y i e l d s UNSAT! ? w i t h Z3 /PDR
       b1d649fe1c842208f701c6b1d1dfa5d17e8dc679
; ( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( k I n t ) ( a k I n t ) ( k2
         I n t ) ( ak2 I n t ) )
; (=> ( and (>= k l 0 ) (< k l ) (>= k2 k ) (< k2 h )
;                     ( o u t e r l o o p l 0 l h k a k k2 a k 2 ) )
;             (<= a k a k 2 ) ) ) )

; This one g r e a t l y h e l p s provi n g t h e s o r t e d n e s s p r o p e r t y with k
     <=k2
; i n s t e a d o f k<k2 !


                                                      43
; ( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( k
       I n t ) ( ak2 I n t ) )
; (=> ( and (>= k l 0 ) (< k h ) ( o u t e r l o o p l 0 l h k a k k a k 2 ) )
;             (= a k a k 2 ) ) ) )

; F i n a l : s o r t e d n e s s ( t i m e 2 s −> 14 s i f u s i n g k <= k2 )
( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( k2 I n t ) (
       ak2 I n t ) )
   (=> ( and (>= k l 0 ) (< k k2 ) (< k2 h )
                    ( e x i t l 0 h k ak k2 ak2 ) )
           (<= ak ak2 ) ) ) )

; w i t h t h i s c o n d i t i o n , s h o u l d b e UNSAT
; ( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( h I n t ) ( k I n t ) ( a k I n t ) ( k2 I n t ) (
       ak2 I n t ) )
;     ( n o t ( e x i t l 0 h l 0 a k (+ l 0 1 ) a k 2 ) ) ) )

( check−sat )

                            Listing 15: Selection sort: permutation
; S t a t u s : SAT i n 9 s by S p a c e r 2015−07−01
       0dfed9c654a6f715b8660ff1d27de74fbfc41916

( s e t − l o g i c HORN)

( declar e−fun i n i t ( I n t I n t I n t I n t I n t ) Bool ) ; l 0 h k a [ k ] z #
     a0 ( z )
( declar e−fun o u t e r l o o p ( I n t I n t I n t I n t I n t I n t I n t I n t ) Bool )
     ; l 0 l h k a [ k ] z # a ( z ) # a0 ( z )
( declar e−fun e x i t ( I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; l 0 h k
     a [ k ] z # a ( z ) # a0 ( z )

( declar e−fun read1 ( I n t I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; l 0
       l h k a [ k ] z # a ( z ) # a0 ( z )
( declar e−fun loop ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
     I n t ) Bool ) ; l 0 l h i p b f k a [ k ] z # a ( z ) # a0 ( z )
( declar e−fun read2 ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
       I n t ) Bool ) ; l 0 l h i p b f k a [ k ] z # a ( z ) # a0 ( z )
( declar e−fun t e s t ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
     I n t I n t ) Bool ) ; l 0 l h i p b v f k a [ k ] z # a ( z ) # a0 ( z )

( declar e−fun w r i t e 1 ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
     I n t ) Bool ) ; l 0 l h p b f k a [ k ] z # a ( z ) # a0 ( z )
( declar e−fun w r i t e 1 a ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
     I n t ) Bool ) ; l 0 l h p b f k a [ k ] z # a ( z ) # a0 ( z )
( declar e−fun w r i t e 1 b ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
     I n t ) Bool ) ; l 0 l h p b f k a [ k ] z # a ( z ) # a0 ( z )

( declar e−fun w r i t e 2 ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
     I n t ) Bool ) ; l 0 l h p b f k a [ k ] z # a ( z ) # a0 ( z )
( declar e−fun w r i t e 2 a ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
     I n t ) Bool ) ; l 0 l h p b f k a [ k ] z # a ( z ) # a0 ( z )
( declar e−fun w r i t e 2 b ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
     I n t ) Bool ) ; l 0 l h p b f k a [ k ] z # a ( z ) # a0 ( z )


                                                44
( declar e−fun endswap ( I n t I n t I n t I n t I n t I n t I n t I n t I n t I n t
     I n t ) Bool ) ; l 0 l h p b f k a [ k ] z # a ( z ) # a0 ( z )
( declar e−fun i n c r ( I n t I n t I n t I n t I n t I n t I n t I n t ) Bool ) ; l 0
     l h k a [ k ] z # a ( z ) # a0 ( z )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( a0z
         Int ) )
    ( i n i t l 0 h k z a0z ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( a0z
         Int ) )
     (=> ( and ( i n i t l 0 h k z a0z ) (<= l 0 h ) )
             ( o u t e r l o o p l 0 l 0 h k ak z a0z a0z ) ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( z
       I n t ) ( az I n t ) ( a0z I n t ) )
     (=> ( and ( o u t e r l o o p l 0 l h k ak z az a0z ) (< l (− h 1 ) ) )
              ( read1 l 0 l h k ak z az a0z ) ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( z
       I n t ) ( az I n t ) ( a0z I n t ) )
     (=> ( and ( o u t e r l o o p l 0 l h k ak z az a0z ) (>= l (− h 1 ) ) )
              ( e x i t l 0 h k ak z az a0z ) ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( b I n t ) ( k I n t ) ( ak
       I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
     (=> ( and ( read1 l 0 l h k ak z az a0z )
                      ( read1 l 0 l h l b z az a0z )
                      ( distinct k l ) )
              ( loop l 0 l h (+ l 1 ) l b b k ak z az a0z ) ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( b I n t ) ( z I n t ) ( az
       I n t ) ( a0z I n t ) )
     (=> ( read1 l 0 l h l b z az a0z )
              ( loop l 0 l h (+ l 1 ) l b b l b z az a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
    (=> ( and ( loop l 0 l h i p b f k ak z az a0z ) (< i h ) )
            ( read2 l 0 l h i p b f k ak z az a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) ( v
     Int ) )
    (=> ( and ( read2 l 0 l h i p b f k ak z az a0z )
                     ( read2 l 0 l h i p b f i v z az a0z )
                     ( distinct k i ) )
            ( t e s t l 0 l h i p b v f k ak z az a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( v I n t ) ( f I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( read2 l 0 l h i p b f i v z az a0z )
          ( t e s t l 0 l h i p b v f i v z az a0z ) ) ) )


                                                45
( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( v I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z
     Int ) )
   (=> ( and ( t e s t l 0 l h i p b v f k ak z az a0z )
                (< v b ) )
          ( loop l 0 l h (+ i 1 ) i v f k ak z az a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( v I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z
     Int ) )
   (=> ( and ( t e s t l 0 l h i p b v f k ak z az a0z )
                (>= v b ) )
          ( loop l 0 l h (+ i 1 ) p b f k ak z az a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) ( i Int ) (p Int ) ( b
     I n t ) ( f I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( and ( loop l 0 l h i p b f k ak z az a0z )
                    (>= i h ) )
          ( w r i t e 1 l 0 l h p b f k ak z az a0z ) ) ) )

; The Swap , 1 s t w r i t e
( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( a l I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( and ( w r i t e 1 l 0 l h p b f k ak z az a0z )
                    ( w r i t e 1 l 0 l h p b f l a l z az a0z )
                    ( dist inc t al z ) )
          ( w r i t e 1 a l 0 l h p b f k ak z az a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( a l I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( and ( w r i t e 1 l 0 l h p b f k ak a l az a0z )
                    ( w r i t e 1 l 0 l h p b f l a l a l az a0z ) )
          ( w r i t e 1 a l 0 l h p b f k ak a l (− az 1 ) a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( a l I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( and ( w r i t e 1 a l 0 l h p b f k ak z az a0z )
                    ( w r i t e 1 a l 0 l h p b f l a l z az a0z )
                    ( distinct b z) )
          ( w r i t e 1 b l 0 l h p b f k ak z az a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( a l I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( and ( w r i t e 1 a l 0 l h p b f k ak b az a0z )
                    ( w r i t e 1 a l 0 l h p b f l a l b az a0z ) )
          ( w r i t e 1 b l 0 l h p b f k ak b (+ az 1 ) a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( and ( d i s t i n c t l k )
                    ( w r i t e 1 b l 0 l h p b f k ak z az a0z ) )
          ( w r i t e 2 l 0 l h p b f k ak z az a0z ) ) ) )




                                              46
( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( w r i t e 1 b l 0 l h p b f l ak z az a0z )
          ( w r i t e 2 l 0 l h p b f l b z az a0z ) ) ) )

; The Swap , 2nd w r i t e
( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ap I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( and ( w r i t e 2 l 0 l h p b f k ak z az a0z )
                    ( w r i t e 2 l 0 l h p b f p ap z az a0z )
                    ( d i s t i n c t ap z ) )
          ( w r i t e 2 a l 0 l h p b f k ak z az a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ap I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( and ( w r i t e 2 l 0 l h p b f k ak ap az a0z )
                    ( w r i t e 2 l 0 l h p b f p ap ap az a0z ) )
          ( w r i t e 2 a l 0 l h p b f k ak ap (− az 1 ) a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ap I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( and ( w r i t e 2 a l 0 l h p b f k ak z az a0z )
                    ( w r i t e 2 a l 0 l h p b f p ap z az a0z )
                    ( distinct f z) )
          ( w r i t e 2 b l 0 l h p b f k ak z az a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ap I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( and ( w r i t e 2 a l 0 l h p b f k ak f az a0z )
                    ( w r i t e 2 a l 0 l h p b f p ap f az a0z ) )
          ( w r i t e 2 b l 0 l h p b f k ak f (+ az 1 ) a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( and ( d i s t i n c t p k )
                ( w r i t e 2 b l 0 l h p b f k ak z az a0z ) )
          ( endswap l 0 l h p b f k ak z az a0z ) ) ) )

( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( w r i t e 2 b l 0 l h p b f p ak z az a0z )
          ( endswap l 0 l h p b f p f z az a0z ) ) ) )

; i n c r and o u t e r l o o p
( assert ( f o r a l l ( ( l0 Int ) ( l Int ) (h Int ) (p Int ) (b Int ) ( f
     I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( endswap l 0 l h p b f k ak z az a0z )
          ( i n c r l 0 l h k ak z az a0z ) ) ) )

( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( l I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( z
       I n t ) ( az I n t ) ( a0z I n t ) )
   (=> ( i n c r l 0 l h k ak z az a0z )
            ( o u t e r l o o p l 0 (+ l 1 ) h k ak z az a0z ) ) ) )




                                                47
; Various i n v a r i a n t s ( h i n t s )

; ; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
       I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
;;     (=> ( w r i t e 1 l 0 l h p b f k a k z a z a 0 z )
;;            (>= p l ) ) ) )

; ; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
       I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
;;     (=> ( w r i t e 1 l 0 l h p b f k a k z a z a 0 z )
;;            (< p h ) ) ) )

; ; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
       I n t ) ( ap I n t ) ( z I n t ) ( a z I n t ) ( a 0 z I n t ) )
;;     (=> ( w r i t e 1 l 0 l h p b f p ap z a z a 0 z )
;;            (= b ap ) ) ) )

; ; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
       I n t ) ( a l I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
;;     (=> ( w r i t e 1 l 0 l h p b f l a l z a z a 0 z )
;;            (= f a l ) ) ) )

; ; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
       I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
;;     (=> ( and (>= k l )
;;                   (< k h )
;;                    ( w r i t e 1 l 0 l h p b f k ak z az a0z ) )
;;            (<= b a k ) ) ) )

; ; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
       I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
;;     (=> ( w r i t e 1 l 0 l h p b f k a k z a z a 0 z )
;;            (= a z a 0 z ) ) ) )

; ; ( assert ( f o r a l l (( l0 Int ) ( l Int ) (h Int ) (p Int ) ( b Int ) ( f
       I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az I n t ) ( a0z I n t ) )
;;     (=> ( endswap l 0 l h p b f k a k z a z a 0 z )
;;            (= a z a 0 z ) ) ) )

; Final property
( a s s e r t ( f o r a l l ( ( l 0 I n t ) ( h I n t ) ( k I n t ) ( ak I n t ) ( z I n t ) ( az
       I n t ) ( a0z I n t ) )
   (=> ( e x i t l 0 h k ak z az a0z ) (= az a0z ) ) ) )

( check−sat )




                                                48
