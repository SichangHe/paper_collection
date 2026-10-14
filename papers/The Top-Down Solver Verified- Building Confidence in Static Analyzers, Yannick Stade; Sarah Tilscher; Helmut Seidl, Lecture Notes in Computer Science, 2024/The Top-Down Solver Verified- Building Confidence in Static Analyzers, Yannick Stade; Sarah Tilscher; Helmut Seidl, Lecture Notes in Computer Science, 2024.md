         The Top-Down Solver Verified: Building
             Confidence in Static Analyzers

         Yannick Stade1 , Sarah Tilscher1,2(B) , and Helmut Seidl1
            1
                 TUM School of Computation, Information and Technology,
                    Technical University of Munich, Munich, Germany
                 {yannick.stade,sarah.tilscher,helmut.seidl}@tum.de
                          2
                            Department of Computer Science,
                Ludwig-Maximilians-Universität Munich, Munich, Germany



       Abstract. The top-down solver (TD) is a local ﬁxpoint algorithm for
       arbitrary equation systems. It considers the right-hand sides as black
       boxes and detects dependencies between unknowns on the ﬂy—features
       that signiﬁcantly increase both its usability and practical eﬃciency. At
       the same time, the recursive evaluation strategy of the TD, combined
       with the non-local destabilization mechanism, obfuscates the correctness
       of the computed solution. To strengthen the conﬁdence in tools relying on
       the TD as their ﬁxpoint engine, we provide a ﬁrst machine-checked proof
       of the partial correctness of the TD. Our proof builds on the observation
       that the TD can be obtained from a considerably simpler recursive ﬁx-
       point algorithm, the plain TD, by applying an optimization that neither
       aﬀects the termination behavior nor the computed result. Accordingly,
       we break down the proof into a partial correctness proof of the plain TD,
       which is only then extended to include the optimization. The backbone of
       our proof is a mutual induction following the solver’s computation trace.
       We establish suﬃcient invariants about the solver state to conclude the
       correctness of its optimization, i.e., the plain TD terminates if and only
       if the TD terminates, and they return the identical result. The proof
       is written using Isabelle/HOL and is available in the archive of formal
       proofs.


       Keywords: ﬁxpoint algorithm · correctness proof · static analysis


1    Introduction

Fixpoint engines are at the heart of static program analyzers based on abstract
interpretation [9]. An analysis introduces a set of unknowns and a domain of
abstract values, which encode the properties of interest. Consider, e. g., the anal-
ysis of uninitialized variables as used by Java [13] or Kotlin [1]. Here, the


Y. Stade and S. Tilscher—Contributed equally to this research and are ordered alpha-
betically.
c The Author(s) 2024
A. Gurfinkel and V. Ganesh (Eds.): CAV 2024, LNCS 14681, pp. 303–324, 2024.
https://doi.org/10.1007/978-3-031-65627-9_15
304     Y. Stade et al.

unknowns are program points, while the abstract values are sets of local vari-
ables that have been initialized. The abstract value of an unknown may depend
on the abstract values of preceding program points. These dependencies are for-
malized as an equation x = fx . The right-hand side fx is the intersection of all
sets of deﬁnitely initialized variables arriving at x via incoming edges. Such an
incoming edge may be an assignment like a = 5, which adds the variable a to the
set of initialized unknowns. Accordingly, the analysis of the program compiles it
into a system of equations, cf. Example 1. A solution to this system approximates
the concrete set of initialized variables when reaching a program point.
    Solutions of equation systems can be computed using ﬁxpoint iteration. Pop-
ular ﬁxpoint algorithms are round-robin [14] and worklist iteration [20]. Both
algorithms, though, have limitations. Round-robin iteration requires a ﬁxed
ﬁnite equation system; also, its running time depends on the evaluation order of
unknowns. Worklist iteration is generally more eﬃcient but, at least in the base
setting, also suﬀers from the restriction that the dependencies between unknowns
must be known beforehand. The latter short-coming is overcome by Vergauwen
et al. [29], de Vilhena et al. [30] where the evaluation of right-hand side functions
is enhanced with self-observation to dynamically detect the dependencies. More
enhanced solvers recursively descend into queried unknowns to obtain their best
values before the evaluation of a right-hand side proceeds. One instance of the
latter is the recursive local descent solver (RLD) [16]. The unknowns, aﬀected by
an updated value, are collected in a local worklist for immediate re-evaluation.
    This is in contrast to the top-down solver (TD) [21,22,28]. Like RLD, it relies
on a recursive descent into queried unknowns combined with dynamic detection
of dependencies. However, when an unknown changes its value, the inﬂuenced
unknowns are not immediately scheduled for re-evaluation. Instead, all transi-
tively inﬂuenced unknowns are marked as unstable so that, when queried again,
their re-evaluation is triggered. The destabilization mechanism, combined with
the delayed re-evaluation, potentially further increases the eﬃciency of the iter-
ation but also obfuscates the correctness of the TD. Still, due to its conceptual
simplicity, the TD opens possibilities for extensions, e.g., with widening and
narrowing [4,9,10,28] or side-eﬀects [26], which otherwise are not so easy to
incorporate [3]. This is one of the reasons why tools like the Ciao system [15]
or Goblint [31] rely on variants of the TD as ﬁxpoint engines. To strengthen
the conﬁdence in these tools, we formalize the TD with the interactive theorem
prover Isabelle [24,25] and prove it to be partially correct. Here, partial correct-
ness means that assuming the TD terminates, it returns a partial solution of the
equation system.
    To accomplish the proof, we build on the observation [28] that the original
TD, which we will also call TD for short, can be obtained from a signiﬁcantly
simpler ﬁxpoint algorithm that we call the plain TD. The plain TD still uses a
recursive descent into queried unknowns while using a set called to avoid inﬁnite
descent due to unknowns with cyclic dependencies. However, it neither keeps
track of dependencies between unknowns nor maintains a set of stable unknowns
whose value has already been computed. Adding these features to obtain the TD
                                             The Top-Down Solver Veriﬁed        305

thus can be seen as an optimization of the plain TD. Accordingly, the proof is
structured into two steps: In the ﬁrst step, we show the partial correctness of the
plain TD. As this algorithm consists of several mutually recursive functions, the
proof consists of a mutual induction. To make the proof more comprehensible,
we utilize the concept of a computation trace to explain its structure and to
highlight important invariants. In the second step, the invariants of the plain
TD are extended to obtain invariants for the TD. The extensions cover the
correctness and modiﬁcations of the additional data structures that collect the
already computed stable unknowns and the dependencies between unknowns.
Additional eﬀort is required to capture the eﬀect of the non-local destabilization
mechanism on those two data structures. Altogether, we prove that the TD and
the plain TD are equivalent, i.e., the TD terminates if and only if the plain TD
terminates and returns the same result whenever they terminate.
    For our formalization, we use the function package with domain predicates
and mutual recursion to deﬁne the solver algorithms in Isabelle. This allows for
a clean proof structure. The combination of features is, however, not supported
by the code generation framework provided by Isabelle. To obtain executable
solver programs from our formalization we, therefore, reﬁne the programs and
use equivalent versions of the solver algorithms based on partial functions with
options for the code generation. We extract executable code for both solvers
and demonstrate their application on a small example. The formalization in
Isabelle/HOL is publicly available in the archive of formal proofs [27].


2   Preliminaries

We ﬁrst introduce some notation used throughout the paper. The powerset of a
set M is denoted by P (M ), and the set diﬀerence of two sets A and B is written
as A − B. Given a mapping f : X → Y , the updated mapping f ⊕ {x → y} :
X → Y is deﬁned by (f ⊕ {x → y}) x = y and (f ⊕ {x → y}) x = f x for all
x = x. For a mapping f : X → P (X), the transitive closure is the mapping
f + : X → P (X) where f + x is the minimal set such that f x ⊆ f + x and
f y ⊆ f + x for all y ∈ f + x. Moreover, the reﬂexive and transitive closure is the
mapping f ∗ : X → P (X) where f ∗ x is deﬁned as f ∗ x := {x} ∪ f + x.
     For the remainder of this article, we consider some (possibly inﬁnite) set
U of unknowns1 and a domain2 D of abstract values. The set D contains one
special element ⊥ (bottom), used as the initial value for the ﬁxpoint iteration.
Elements from D need to be comparable for equality, but there is no need to
require a partial order or existence of least upper bounds. The equation system
associates each unknown x (the left-hand side) with a right-hand side function
fx , specifying other unknowns’ contribution to the left-hand side x. Following

1
  We use the term unknown instead of variable because, in the context of program
  analysis, variables usually denote program variables, not unknowns in the equation
  system.
2
  In program analysis this is often a complete lattice of abstract values describing
  concrete program states.
306    Y. Stade et al.

Fecht and Seidl [11], the right-hand side function fx is considered as a black box
functional. The only requirement is that the right-hand side is pure [17], i. e.,
parametric in the solver state. That limitation has slightly been relaxed by de
Vilhena et al. [30] to apparent purity, which allows functions to have internal
side eﬀects, e. g., logging important events or spawning a new thread—as long
as two identical calls of a function return the same result. Here, we stick to the
original notion of purity. For pure functionals in that sense, Hofmann et al. [17]
prove that they can be represented as strategy trees. A strategy tree is composed
of Answer nodes, the leaves of the tree, containing an element of D, and Query
nodes that contain an unknown y to be queried together with a function g. Based
on the value dy of the queried unknown y, the call g dy returns the subtree to
continue the evaluation of the right-hand side. In this work, we assume the depth
of strategy trees to be ﬁnite, i.e., only ﬁnitely many unknowns may be queried
in a right-hand side. As a shorthand, we write t σ when evaluating the strategy
treet t using the mapping σ.

type (U, D) strategy-tree = Answer D | Query U (D → (U, D) strategy-tree)

Note that the strategy trees can describe right-hand sides with varying depen-
dencies, which the TD can cope with. Further, their tree representation lends
itself to a structural induction on the right-hand sides. A system of equations T
is then formally the function
                               T : U → (U, D) strategy-tree                    (1)
that maps every unknown in U to a strategy tree.
Example 1. Consider the following code snippet and the corresponding control-
ﬂow graph, where a and b are local program variables.




    The domain for the variable initialization analysis is D = P ({a, b}), with ⊥
being the complete set {a, b} and the empty set. A variable is added to the set
of initialized variables whenever it occurs on the left-hand side of an assignment.
Accordingly, we retrieve the following equation system and show its strategy tree
representation in Fig. 1:
                                  w=∅
                                  z = (y ∪ {a}) ∩ (w ∪ {a})
                         T :                                                   (2)
                                  y = z ∪ {b}
                                  x=y ∩ z
    For the remaining part, we ﬁx some system of equations T and assume that it
is globally available. A total solution of such a system of equations is a mapping
                                                 The Top-Down Solver Veriﬁed      307




Fig. 1. The ﬁgure shows the value table of T from Example 1. Each unknown maps
to a strategy tree with query nodes (Q) and answer nodes (A). The trees are deﬁned
over the domain P ({a, b}) where ⊥ represents the full set {a, b} and  the empty set.


σ : U → D from unknowns to values such that for all unknowns x ∈ U

                                     T xσ=σx .                                    (3)

   However, we are often not interested in a solution for the entire (potentially
inﬁnite) equation system, but rather in a partial solution. For an unknown x ∈ U
and a mapping σ : U → D, let the function dep x σ return the set of all unknowns
occurring in T x when traversed with σ, the so-called (direct) dependencies of x.
Then, the mapping σ : U → D is a partial solution for a set s ⊆ U if3

                         ∀x ∈ s. dep∗ x σ ⊆ s ∧ T x σ = σ x.                      (4)

    If x is in dep+ x σ for some σ, i. e., the unknown x depends transitively on
itself, we call the associated system of equations T recursive (with respect to σ).
In the proof, we argue about the subset of dep∗ composed of all unknowns
visited when solving some unknown x. Such unknowns are reachable from x via
the depends-relation without passing through (but including) unknowns of a set
X, where the recursive descent stops. Hence, we deﬁne the set RX inductively
for a given mapping σ : U → D and an unknown x to contain all unknowns in
dep σ x if x ∈/ X, and all unknowns in dep σ y if y ∈ RX − X. We denote RX by
                                       
                                    depU −X∗ σ x .
                          
 Note that dep∗ σ x = depU −∅∗ σ x holds. We extend the deﬁnitions of dep and
    
depU −X∗ to strategy trees and use the same symbol for simplicity. This allows
to compute both sets also for partial right-hand sides.


3     The Plain Top-Down Solver
The TD can be obtained from a considerably simpler ﬁxpoint algorithm [28],
which we call the plain TD. First, we prove the plain TD to be partially correct;
3
    Recall, dep∗ denotes the reﬂexive and transitive closure of dep.
308     Y. Stade et al.

second, we extend this proof to the original TD. Tilscher et al. [28], consider
an even simpler version of the TD, the monadic base solver. It is, however, not
as powerful as the TD since it does not track the set of called unknowns and
thus cannot solve recursive equation systems. Therefore we excluded it from our
layered approach.
     The plain TD maintains a solver state that consists of the set of called
unknowns c containing the unknowns that are already being evaluated, and
a mapping σ storing the current value of every unknown. The algorithm consists
of three mutually recursive functions: iterateplain , evalplain , and queryplain .
The function iterateplain iterates one unknown x until a ﬁxpoint is reached for
it, i. e., the newly computed value and the value from the previous iteration coin-
cide. When the iteration continues because the value has changed, the mapping
σ of unknowns to values is updated.

iterateplain x c σ =
  let (d, σ) = evalplain x (T x) c σ in
  if d = σ x then (d, σ)
  else iterateplain x c (σ ⊕ {x → d})

For the evaluation of x’s right-hand side, the function evalplain is invoked. The
function evalplain receives a right-hand side in the form of a strategy tree and
traverses it top-down until reaching an answer node, whose value it returns.

evalplain x t c σ = case t of
    Answer d ⇒ (d, σ)
  | Query y g ⇒ let (d, σ) = queryplain x y c σ in evalplain x (g d) c σ

The function queryplain is called to determine the current value for y and thereby
the subtree g d in which to descend next, when evalplain is called for some query
node Query y g. A call to queryplain checks whether a call to queryplain for the
same unknown y already occurred in the current call stack. If this is the case,
i. e., the unknown is contained in the set c of called unknowns, the current value
of y is looked up in the mapping σ. Otherwise, queryplain invokes the function
iterateplain with y added to c to start the ﬁxpoint iteration for y.

queryplain x y c σ =
  if y ∈ c then (σ y, σ)
  else iterateplain y (c ∪ {y}) σ

Finally, we have a function solveplain that wraps the initial call to iterateplain
and provides it with the initial arguments, the singleton set {x} as called
unknowns, and the empty mapping σ0 that implicitly maps every unknown to ⊥.


solveplain x = let (_, σ) = iterateplain x {x} σ0 in σ

A computation trace captures the execution of a solver’s run. It is a tree that con-
tains a node for each function call, along with essential parameters and result
values. The solveplain node constitutes its root node. Nested calls to other
                                                 The Top-Down Solver Veriﬁed        309




Fig. 2. The ﬁgure shows the computation trace of the plain TD for solving the unknown
z from the equation system from Example 1. In dark, we highlight the function calls
corresponding to unknowns in dep∗ x σ where σ is the ﬁnal result. (Color ﬁgure online)



functions are added as children, while recursive calls (to the same function) are
appended to the right as siblings.4 In Figs. 2 and 4, we omit evalplain nodes for
clarity since they essentially only add an intermediate node between iterateplain
and queryplain nodes. The backbone of the partial correctness proof is an induc-
tion over this computation trace, which can be conveniently implemented with
the induction rules generated by Isabelle for the mutually recursive functions.
The concept of a computation trace is illustrated in the following example.

Example 2. Consider the equation system from Example 1. We observe the exe-
cution of the TD when solving the unknown z and illustrate the occurring mutu-
ally recursive function calls as computation trace in Fig. 2.
    The initial call solveplain z invokes the function iterateplain to iterate on
the queried unknown z. In z’s ﬁrst iteration, the call to evalplain queries the
unknowns y and w to fully traverse the right-hand side of z. The querying of
y entails a call to iterateplain for its iteration which takes only one turn to
stabilize. The evaluation of y’s right-hand side only depends on the unknown
z, for which the call to queryplain immediately returns since z is already being
evaluated. The iteration of w entails no further queries because the strategy tree
representing its right-hand side is an answer node.

    The computation trace reveals the information available during the solver’s
computations. When the algorithm reaches a node v in the computation trace,
(computations of) all nodes on the path to the root are in progress, and nodes in
subtrees on the left of this path are already completed; we call this history the
reaching left-context of v. The solver’s state, i. e., the internal data structures
maintained by the solver, can be seen as an abstraction of the (concrete) left-
context. Since the algorithm always refers to the latest abstraction of the solver
state, it could also be implemented as a reference to a mutable data structure.
4
    For the TD, the order of function calls during execution corresponds to the preorder
    traversal of the computation trace, because all recursive calls are tail calls.
 310     Y. Stade et al.

     For a subtree t of the computation
                                        trace and σ  returned by the corresponding
 function call, the set depU −c∗ t σ  matches the unknowns occurring in the last
 iterations of t. Based on this, we introduce a set s that is an abstraction of
 the reaching left-context: it collects the unknowns of the last iterations in the
 reaching left-context, and unknowns under evaluation. A re-evaluation of x ∈ s
 returns the same value already stored in σ for x. This holds speciﬁcally for
 unknowns in c, a subset of s, because the algorithm looks up their value instead
 of initiating a new iteration. Unknowns in s − c re-evaluate to the same value
 because they only depend on unknowns in s; hence, we call them truly stable.
 Accordingly, the two milestones for proving the correctness of the plain TD are:
                           
  (i) deﬁning the set depU −c∗ to describe the set of unknowns queried in the last
      iterations for a subtree of the computation trace, and
 (ii) introducing the set s to collect unknowns that, when re-evaluated, evaluate
      to the same value.
    Milestone (ii) is essential to ensure that the plain TD computes the same
 value for recurring occurrences of an unknown in a right-hand side.
    For unknowns in s we show that σ is a partial solution after updating the
 value for the current unknown in iterateplain .
 Lemma 1. Assume σ is a partial solution for all x ∈ s − c, the set s is closed
 under dep except for elements that are in c, i. e., ∀y ∈ s − c, dep σ y ⊆ s, and
 σ and σ  are identical on s, i. e., ∀x ∈ s. σ x = σ  x. Then, σ  is also a partial
 solution for all x ∈ s − c.
     Recall that σ is a partial solution of all unknowns in the set s. Within the
 iterateplain function, when the newly computed value for an unknown x and
 its old value stored in σ diﬀer, we can conclude that x was not a member of s
 because the old σ would not have been a partial solution.
 Lemma 2. Assume T x σ = σ x and σ is a partial solution of all unknowns in
 a set s. Then, x is not a member of s.
    The following deﬁnition summarizes the properties used as invariant for the
 partial correctness proof in one predicate.
 Definition 1 (Plain TD Invariant). For c, s ⊆ U and the mapping σ : U →
 D the predicate validplain c s σ is satisﬁed if
 (i) ∀x ∈ s − c. dep σ x ⊆ s, i. e., the set s is closed under dep except for unknowns
     that are also in c, and
(ii) ∀x ∈ s − c. T x σ = σ x, i. e., σ fulﬁlls the equations for truly stable unknowns.
    For c = ∅, which holds after a call to solveplain terminated, the predicate
 implies that σ is a partial solution for s. Using the predicate, we formulate the
 partial correctness theorem.
 Theorem 1 (Partial Correctness of the plain TD). The theorem shows
 three mutual statements:
                                                  The Top-Down Solver Veriﬁed            311




Fig. 3. The ﬁgure illustrates exemplary for the Continue subcase in the Iterate case
an induction step. First, the induction hypothesis (IH) for the nested queryplain is
instantiated, such that its premises are fulﬁlled. Its application then provides facts to
reason that the premises of the IH for the recursive iterateplain call are satisﬁed.


• Assume queryplain x y c σ = (dy , σ  ) is deﬁned and validplain c s σ holds.
                                                                                      
  Then, we show (i) validplain c s σ , and (ii) ∀u ∈ s. σ u = σ u where s :=
  s ∪ depU −c∗ σ  y.
• Let c = c − {x}. Assume iterateplain x c σ = (dx , σ  ) is deﬁned, x ∈ c, and
  validplain c s σ holds. Then,
                               we show     (i) validplain c s σ  , and (ii) ∀u ∈ s. σ u =
    
  σ u where s      :=           ∗   
                       s ∪ dep U −c σ x.
• Assume evalplain x t c σ = (dx , σ  ) is deﬁned, and validplain c s σ holds.
  Then, we show (i) validplain c s σ  , (ii) ∀u ∈ s. σ u = σ  u, and (iii) t σ  = dx
  where s := s ∪ depU −c∗ σ  t.

Proof. This proof is more of a sketch to convey the proof idea; for a rigorous
proof, see the Isabelle formalization [27]. We prove the statement by mutual
induction. The induction rule derived from the three mutually recursive functions
leads to three cases. Figure 3 illustrates an induction step in the computation
trace exemplary for the iterate case.
Case 1 (Query). The ﬁrst case reasons about a call to the queryplain function.
Let x, y ∈ U, c ⊆ U, σ, σ  : U → D, and dy ∈ D such that queryplain x y c σ =
(dy , σ  ) is deﬁned. We distinguish two subcases: the queried unknown can either
be called or not, the former leading to a lookup and the latter to an iteration.
Subcase 1.1 (Lookup). This case is a base case since there are no further mutual
recursive calls. In the computation trace, it corresponds to a query node as leaf.
The proof goal follows directly from the premises since σ is not changed.
Subcase 1.2 (Iterate). In this case, the function iterateplain is called, and its
result directly returned by the enclosing queryplain function. Thus, iterateplain
y (c ∪ {y}) σ = (dy , σ  ) and the induction hypothesis for the iterateplain call
can be applied. The proof goal follows immediately because the result of the call
to iterateplain is returned without modiﬁcations.
Case 2 (Iterate). Let c ⊆ U, x ∈ c, σ, σ  : U → D, and dx ∈ D such that
iterateplain x c σ = (dx , σ  ) is deﬁned. We distinguish two subcases: either a
ﬁxpoint is reached or not. In either case, the function evalplain is invoked ﬁrst,
and the subcase depends on its result. Both subcases constitute two diﬀerent
induction steps, and both cases use the induction hypothesis for evalplain .
312     Y. Stade et al.

Subcase 2.1 (Fixpoint). The induction hypothesis of evalplain provides all nec-
essary facts, and since σ is not updated anymore, the proof goal follows.

Subcase 2.2 (Continue). Obtain dx ∈ D and σ1 : U → D such that the call
evalplain x (T x) cσ = (dx , σ1 ) is deﬁned. The induction hypothesis for evalplain
states (i) validplain s c σ1 , (ii) ∀y ∈ s ∪ {x} . σ y = σ1 y, and (iii) T x σ1 = dx
where s := s ∪ {x} ∪ depU −c∗ σ1 c x. Since we are in the Continue case, we
know that σ1 x = dx . From Lemma 2 it follows x ∈       / s. This allows us to show
together with Lemma 1 that also validplain s (c − {x}) (σ1 ⊕ {x → dx }) holds.
This is required to instantiate the induction hypothesis for the successive call to
iterateplain , which concludes the case.

Case 3 (Eval). The strategy tree passed to evalplain can either be a single
answer node or a non-trivial strategy tree with a query node as a root.

Subcase 3.1 (Answer). This case is the second induction base of the entire induc-
tion and follows trivially.

Subcase 3.2 (Query). The proof follows from the facts retrieved from the induc-
tion hypotheses for both recursive calls to queryplain and evalplain using the
fact that σ remains unchanged for unknowns in s.                             
                                                                             

    The corollary below summarizes the results from this section. It follows
directly from Theorem 1.

Corollary 1 (Partial Correctness of the plain TD). Assume the equality
solveplain x = σ is deﬁned. Then, σ is a partial solution for dep∗ x σ.


4     The Top-Down Solver
So far, we have proven partial correctness only for the plain TD. In the following,
we extend the correctness statement to the original TD by showing that both
ﬁxpoint algorithms are equivalent. The TD improves the plain TD through more
extensive self-observation. While the plain TD solely maintains a set of called
unknowns to prevent non-termination in the case of recursive equation systems,
the TD introduces two additional data structures for self-observation:
• A set stable collecting all unknowns that do not need to be re-evaluated,
  because they only depend on other stable unknowns whose value has not
  changed since their last evaluation.
• An infl map that dynamically records for each unknown x a set of unknowns
  inﬂuenced by x. It, therefore, records the inverse of the dep relationship.
The set stable is similar to set s used in the proof of the plain TD; and indeed,
s is in every step a subset of stable. However, stable additionally collects
unknowns that have been fully evaluated in earlier iterations but are not aﬀected
by any unknowns whose value changed in the meantime. Its additional mainte-
nance allows skipping unnecessary re-evaluations of already stable unknowns.
                                                  The Top-Down Solver Veriﬁed    313

   Three modiﬁcations are necessary to integrate the new data structures and to
keep them consistent. In the following code snippets, we highlight those changes.
The function eval is only adapted marginally to facilitate the passing of the
additional parameters (not highlighted).

eval x t c infl stable σ = case t of
    Answer d ⇒ (d, infl, stable, σ)
  | Query y g ⇒ let (d, infl, stable, σ) = query x y c infl stable σ in
                 eval x (g d) c infl stable σ

At the end of a call to query, the dependency is recorded in the map infl,
i. e., the parent unknown is inserted into the set of unknowns inﬂuenced by the
queried unknown.

query y x c infl stable σ =
  let (d, infl, stable, σ) =
    if x ∈ c then (σ x, infl, stable, σ)
    else iterate x (c ∪ {x}) infl stable σ
  in (d, infl ⊕ {x → infl x ∪ {y}}, stable, σ)

The improvement to skip re-evaluations of unknowns in stable is implemented
in the function iterate. If iterate is invoked for an unknown that is already in
stable, its right-hand side is not evaluated; instead, its value is simply looked
up in σ. In case the current unknown is not yet stable, it is optimistically added
to the set stable when starting the evaluation of its right-hand side.

iterate x c infl stable σ =
  if x ∈
       / stable then
    let (d, infl, stable, σ) = eval x (T x) c infl (stable ∪ {x}) σ in
    if d = σ x then (d, infl, stable, σ)
    else
      let (infl, stable) = destab x infl stable in
      iterate x c infl stable (σ ⊕ {x → d})
  else (σ x, infl, stable, σ)

After the evaluation of the right-hand side of x, iterate x updates the value
of x in σ. If the value has changed, the values of unknowns that are (indi-
rectly) inﬂuenced by x need to be recomputed. Instead of recomputing them
immediately, all aﬀected unknowns are removed from stable. This will trigger
their re-evaluation in case they are queried again. To remove all indirectly inﬂu-
enced unknowns the additional function destab is provided. A call destab x ﬁrst
removes all unknowns directly inﬂuenced by x from stable and resets the set of
inﬂuenced unknowns of x in infl to the empty set, and then continues recur-
sively to destabilize indirectly inﬂuenced unknowns of x. Note that destab x
only removes x itself from the set stable if x (transitively) depends on itself.
If x does not depend on itself, x remains in stable, and the ﬁxpoint iteration
terminates after one iteration.5

5
    Recall that x is inserted optimistically into stable before its iteration.
314     Y. Stade et al.



destab x infl stable =
  let f y (infl, stable) = destab y infl (stable − {y}) in
  fold f (infl ⊕ {x → ∅}, stable) (infl x)

With those changes, the solve function of the TD is deﬁned as follows, where
infl0 represents the empty mapping, i. e., where every unknown in U maps to
the empty set.

solve x = let (_, _, stabl, σ) = iterate x {x} infl0 ∅ σ0 in (stabl, σ)



    Calling solve for the unknown x and the equation system from Example
1 results in the computation trace shown in Fig. 4. The ﬁgure illustrates the
eﬀect of skipping superﬂuous computations. Nodes that belong to additional
computations the plain TD would perform but which are skipped by the TD are
indicated with small grey nodes. In this example, the TD saves more than half
of the computations.




Fig. 4. The ﬁgure shows the computation trace corresponding to the TD when solving
the equation system from Example 1 for unknown x. Some computation paths termi-
nate because the queried unknown is called, others because the iterated unknown is
already stable. The grey nodes below stable leaves indicate the additional computation
steps that the plain TD would execute.


    A crucial part of showing the correctness of the optimizations in the TD, is
verifying that the destabilization preserves the essential properties of the solver’s
state. This includes proving that destabilization is thorough enough to remove all
unknowns possibly aﬀected by a changed value from stable, such that no evalu-
ation builds on possibly outdated values of stable unknowns. On the other hand,
it also requires showing that destabilization is speciﬁc enough to not remove
                                              The Top-Down Solver Veriﬁed       315

from stable any unknown that was already stable before the iteration started.
This ensures that the set of called unknowns remains a subset of stable and
thus invariants for stable unknowns also hold for called unknowns where values
are simply looked up without further descending. To guarantee these bounds of
destabilization, we have found two invariants to be essential milestones:
 (i) An invariant that the data structure infl is complete, i. e., records all rele-
     vant dependencies, and
(ii) An invariant stating that, when evaluating an unknown x, only inﬂuences
     to previously unstable unknowns or x itself, are recorded.
    Similarly to Deﬁnition 1 for the plain TD, we deﬁne a predicate to describe
valid input solver states.

Definition 2 (TD Invariant). For c, stable ⊆ U, σ : U → D and infl : U →
P (U) the predicate valid c σ infl stable is satisﬁed if:
  (i) c ⊆ stable
 (ii) ∀x ∈ stable − c. T x σ = σ x, i. e., the mapping σ fulﬁlls the equations for
      all truly stable unknowns,
(iii) {x ∈ U | infl x = ∅} ⊆ stable, i. e., keys mapping to non-trivial values in
      infl are members of stable, and
(iv) ∀y ∈ stable − c. ∀x ∈ dep σ y. y ∈ inflx, i. e., infl stores the mapping
      “x inﬂuences y” for all unknowns x on which any truly stable unknown y
      depends on.

    Item (i) allows to conclude that x is not only in c but also in stable when
the unknown x is looked up in the query function. We remark that for the
plain
     TD this can be implicitly concluded, for s respectively, from the fact that
depU −c∗ σ x ⊆ s for the currently evaluated unknown x. Item (iv) corresponds
to milestone (i) and relates the map of inﬂuences to the dependencies of the
equation system. It helps to show that stable remains closed under dep also
after the application of destab. With Item (ii) and (iii) the predicate valid
extends validplain from Deﬁnition 1.
Lemma 3. Let infl : U → P (U), and c, stable ⊆ U. Assume
 • {u ∈ U | infl u = ∅} ⊆ stable and
 • ∀u ∈ stable − c. ∀v ∈ dep σ u. u ∈ inflv.
Then ∀u ∈ stable − c. dep σ u. ⊆ stable. This immediately implies

                valid c σ infl stable =⇒ validplain c stable σ .

   Besides the predicate for valid solver states, we deﬁne a predicate relating
the output solver state to the corresponding input state.
Definition 3. (Update relation). For x ∈ U, stable, stable ⊆ U, and
infl, infl : U → P (U) the predicate update x infl stable infl stable is
satisﬁed if
  316     Y. Stade et al.

  (i) stable ⊆ stable , i. e., the stable set is increasing,
 (ii) ∀u. (infl u − infl u) ∩ (stable − {x}) = ∅, i. e., only unknowns that were
      not previously stable (or x) are inserted into infl, and
(iii) ∀u ∈ stable. infl u ⊆ infl u, i. e., the set of inﬂuenced unknowns increases
      for all stable unknowns.
  Item (i) is used to show that Deﬁnition 2 (i) still holds after destabilization
  (cf. Lemma 4). It also aids in deriving the appropriate variants of Item (ii) and
  Item (iii) in the induction steps. Deﬁnition 3 (ii) formalizes the earlier described
  milestone (ii) and allows to show that Item (i) still holds after destabilization.
  Item (iii) expresses that a dependency, recorded due to an unknown occurring
  in some right-hand side, persists till the end of this right-hand side’s evaluation.
  This is required to establish Deﬁnition 2 (iv).
      Both deﬁned predicates enable the formalization of the preservation of invari-
  ants by the destabilization mechanism.
  Lemma 4. For x ∈ U, infl : U → P (U), and stable ⊆ U, let infl : U →
  P (U), and stable ⊆ U such that destab x infl stable = (infl , stable )
  holds. Let c := c − {x} and σ  := σ ⊕ {x → dx }.
  (i) Assume c ⊆ stable and stable ⊆ stable . Then c ⊆ stable holds.
 (ii) Assume
       • ∀x ∈ stable − c. T x σ = σ x,
       • T x σ = dx , and
       • ∀u ∈ stable − c .∀v ∈ dep σ u. u ∈ infl v.
      Then ∀x ∈ stable − c . T x σ  = σ  x holds.
(iii) Assume {u ∈ U | infl u = ∅} ⊆ stable.
      Then {u ∈ U | infl u = ∅} ⊆ stable holds.
(iv) Assume ∀u ∈ stable − c . ∀v ∈ dep σ u. u ∈ infl v.
      Then ∀u ∈ stable − c . ∀v ∈ dep σ  u. u ∈ infl v.
  The TD skips re-evaluation of stable unknowns because it would yield the same
  value. The following lemma supports this and shows that the plain TD will
  return the same value as already computed if an unknown is stable.
  Lemma 5. This lemma shows:
  • Assume queryplain x y c σ = (dy , σ  ) is deﬁned, validplain c s σ is satisﬁed, and
    y ∈ s. Then σ and σ  are equal.
  • Assume iterateplain x c σ = (dx , σ  ) is deﬁned, x ∈ c, validplain (c − {x}) s σ
    is satisﬁed, and x ∈ s. Then σ and σ  are equal.
  • Assume evalplain x t c σ = (dx , σ  ) is deﬁned, validplain c s σ is satisﬁed, and
    dep t σ ⊆ s. Then t σ  = dx and σ = σ  .
      Following the auto-generated induction rules for the plain TD and the TD, we
  split the equivalence proof of both ﬁxpoint algorithms into two directions. The
  ﬁrst assumes the termination of the plain TD and shows that the TD terminates,
  yielding the same value, cf. Theorem 2. The second proves that the plain TD
  returns the same value as the TD under the assumption that the TD terminates,
  cf. Theorem 3. Both results are combined afterward in Corollary 2, and Corollary
  3 concludes the correctness of the TD.
                                            The Top-Down Solver Veriﬁed      317

Theorem 2 (Equivalence I). The theorem shows:
• Assume queryplain x y c σ = (dy , σ  ) is deﬁned, and valid c σ infl stable
   holds. Then there exist infl : U → P (U) and a set stable ⊆ U such that
   (i) query x y c infl stable σ = (dy , infl , stable , σ  ) is deﬁned and
  (ii) valid c σ  infl stable holds.
   Furthermore, (iii) the statements update x infl stable infl stable , and
   (iv) x ∈ infl y hold.
• Assume iterateplain x c σ = (dx , σ  ) is deﬁned, valid c σ infl stable
   holds for c := c − {x}, and x ∈ c. Then there exist infl : U → P (U) and
   stable ⊆ U such that
   (i) iterate x c infl stable σ = (dx , infl , stable , σ  ) is deﬁned and
  (ii) valid c σ  infl stable holds.
   Furthermore, (iii) the statements update x infl stable infl stable , and
   (iv) x ∈ stable hold.
• Assume evalplain x t c σ = (dx , σ  ) is deﬁned, valid c σ infl stable holds,
   and x ∈ stable. Then there exist infl : U → P (U) and stable ⊆ U such
   that
   (i) eval x t c infl stable σ = (dx , infl , stable , σ  ) is deﬁned,
  (ii) valid c σ  infl stable holds.
   Furthermore, (iii) the statements update x infl stable infl stable , (iv)
   t σ  = dx , and (v) ∀u ∈ dep σ  t. x ∈ infl u hold.

Proof. The complete proof is extensive, thus we only highlight pivotal steps and
direct the reader to the formalization in Isabelle [27] for a detailed proof. The
proof uses the same induction rules and covers the same cases as in Theorem 1.

Case 1 (Query). Let x, y ∈ U, c ⊆ U, σ, σ  : U → D, dy ∈ D such that the call
queryplain x y c σ = (dy , σ  ) is deﬁned. And let infl : U → P (U) , stable ⊆ U
such that valid c σ infl stable holds.

Subcase 1.1 (Lookup). This case follows directly from the premises.

Subcase 1.2 (Iterate). Using the induction hypothesis, we obtain infl1 and
stable1 such that iterate y c infl stable σ = (dy , infl1 , stable1 , σ  )
is deﬁned. The induction hypothesis for the iterate call provides the fact
(infl1 u − infl u) ∩ (stable − {x}) = ∅. Using the deﬁnition of iterate, we
can conclude that the subtraction of {x} can be omitted, which aids in proving
the subgoal.

Case 2 (Iterate). First, assume that x ∈ stable. Lemma 5 implies that the plain
TD returns σ unchanged, and the same holds for the TD since it skips com-
putation altogether. Thus, the proof goals are trivially satisﬁed. Now, assume
that x ∈/ stable. Let x ∈ U, c ⊆ c, σ, σ  : U → D, dx ∈ D such that
iterateplain x c σ = (dx , σ  ) is deﬁned, and let infl : U → P (U) , stable ⊆ U
such that valid c σ infl stable holds.

Subcase 2.1 (Fixpoint). The premises directly imply the subgoal.
318     Y. Stade et al.

Subcase 2.2 (Continue). Let dx ∈ D, σ1 : U → D such that
evalplain x (T x) c σ = (dx , σ1 ) is deﬁned. According to the induction hypothesis
for eval, there exists infl1 : U → P (U) , stable1 ⊆ U such that

        eval x (T x) c infl ({x} ∪ stable) σ = (dx , infl1 , stable1 , σ1 )

is deﬁned. Let furthermore infl2 : U → P (U) , stable2 ⊆ U such that

                  destab x infl1 stable1 = (infl2 , stable2 ) .

Lemma 4 states that the predicate valid is preserved for infl2 and stable2 .
This is key to applying the induction hypothesis for the tail call to iterateplain .
After that, one must show that

 (i) ∀u ∈ stable. infl u ⊆ infl u and
(ii) ∀u. (infl u − infl u) ∩ (stable − {x}) = ∅.
For the ﬁrst, we exploit the fact that we have previously shown that stable ⊆
stable2 and that destab only removes key-value mappings with keys that
are not in stable. For the second, we show similar to the Iterate subcase
in the Query case above, that (infl u − infl2 u) ∩ (stable − {x}) = ∅ and
(infl1 u − infl u) ∩ (stable − {x}) = ∅. Together with the fact that infl2 u ⊆
infl1 u for all u, the statement follows.

Case 3 (Eval). Let x ∈ U, c ⊆ U, σ, σ  : U → D, dy ∈ D and t a strategy tree
such that evalplain x t c σ = (dx , σ  ) is deﬁned. Furthermore, let infl : U →
P (U) , stable ⊆ U such that valid c σ infl stable holds.

Subcase 3.1 (Answer). This case follows directly from the premises.

Subcase 3.2 (Query). The main step here is to show, as in Theorem 1, that once
a value for an unknown has been calculated, this value is preserved during the
evaluation of the remaining right-hand side. To accomplish this, we use Lemma
3 to derive validplain c stable σ and then use the value preserving property
Theorem 1 (ii) of the plain TD.                                              
                                                                             

    A crucial part for the proof in the other direction is to show that when the TD
reaches the Stable case, i. e., stops further descent because the iterated unknown
is in stable, the plain TD terminates for the same parameters and returns the
same value. Since the Stable case constitutes a base case of the induction using
the rules for the TD, no induction hypotheses are available to conclude this fact.
Hence, we add the obvious but vital premise that the set stable is ﬁnite.
Lemma 6. Assume x ∈ c, x ∈ stable, validplain (c − {x}) stable σ holds, and
the set stable is ﬁnite. Then there exists dx ∈ D such that iterateplain x c σ =
(dx , σ) is deﬁned and dx = σ x.
   This lemma holds since the resulting computation trace has ﬁnite width and
height. The ﬁxpoint iterations at any level terminate after one iteration since
                                             The Top-Down Solver Veriﬁed       319

the input is already a solution. Also, the number of query nodes in a right-hand
side is bounded, because we restrict strategy trees to be of ﬁnite height. Finally,
its height is ﬁnite because one unknown is added to c at every second level and
it is always a subset of s. Formally, this lemma is proven by structural induction
over s. With the help of the lemma we can show the remaining direction of the
equivalence:
Theorem 3 (Equivalence II). The theorem shows:
• Assume query x y c infl stable σ = (dy , infl , stable , σ  ) is deﬁned, x ∈
  stable, stable is ﬁnite, and valid c σ infl stable holds. Then
    (i) queryplain x y c σ = (dy , σ  ) is deﬁned and
   (ii) valid c σ  infl stable holds.
  Furthermore, in this case (iii) update x infl stable infl stable holds, (iv)
   stable is ﬁnite, and (v) x ∈ infl y.
• Assume iterate x c infl stable σ = (dx , infl , stable , σ  ) is deﬁned,
  x ∈ c, stable is ﬁnite, and valid c σ infl stable holds. Let c := c − {x}.
  Then
    (i) iterateplain x c σ = (dx , σ  ) is deﬁned and
   (ii) valid c σ  infl stable holds.
  Furthermore, in this case (iii) update x infl stable infl stable holds, (iv)
  the set stable is ﬁnite, and (v) x ∈ stable .
• Assume eval x t c infl stable σ = (dx , infl , stable , σ  ) is deﬁned, x ∈
  stable, stable is ﬁnite, and valid c σ infl stable holds. Then
    (i) evalplain x t c σ = (dx , σ  ) is deﬁned and
   (ii) valid c σ  infl stable holds.
  Furthermore, in this case (iii) update x infl stable infl stable holds, (iv)
  stable is ﬁnite, (v) t σ  = dx , and (vi) ∀u ∈ dep σ  t. x ∈ infl u.

Proof. This proof uses the induction rules for the TD; which results in an addi-
tional subcase Stabl in the Iterate case. This is the only case that diﬀers signiﬁ-
cantly from the previous proof; it is proven using Lemma 6.                      
                                                                                 

  Both theorems combined establish the equivalence of the plain TD and the
TD, which is expressed in the following corollary.

Corollary 2 (Equivalence of the TDs). The equation solveplain x = σ is
deﬁned for some σ ∈ {f : U → D} whenever solve x = (stable, σ  ) is deﬁned
for some stable ⊆ U and σ  : U → D. In this case, σ and σ  are equal.

   The following corollary reads identically to Corollary 1 but refers to the
implementation of the TD. It is a straightforward consequence of Theorem 3.
320    Y. Stade et al.

Corollary 3 (Partial Correctness of the TD). Assume that the equation
solve x = (stable, σ) is deﬁned. Then the corollary shows that σ is a partial
solution for stable and x ∈ stable.

5     Related Work
In the scope of verifying dataﬂow analyses, round-robin iteration [6] and vari-
ations of Kildall’s algorithm [5,8,23] have been veriﬁed. The latter maintain a
global worklist for a chaotic iteration over the control-ﬂow graph. Others for-
malize syntax-directed ﬁxpoint iterators as part of their work on formalizing
abstract interpreters [7,12,18]. Instead of iterating over the control-ﬂow graph
of a program, their abstract interpreters are guided by the program’s syntax.
These dedicated solvers, however, are not generically applicable to all equation
systems. Instead of dynamically detecting dependencies, the dependencies are
derived directly from the program’s control ﬂow.
    The partial correctness of the local generic ﬁxpoint solver RLD has been
proven by Hofmann et al. [16]. This algorithm records dependencies dynami-
cally to deal with changing dependencies between unknowns. In contrast to the
TD, it locally destabilizes directly inﬂuenced unknowns when the value of the
current unknown has been updated, and immediately triggers their re-evaluation
through a local worklist. This may lead to diﬀerent values being computed by
the solver for repeated queries of the same unknown within a right-hand side.
Extra mechanisms are required to avoid this undesired behavior [19]. In con-
trast, the TD relies on non-local destabilization to remove all unknowns from
the set of stable unknowns that transitively depend on an updated unknown.
The local worklist iteration of RLD is avoided and the same value is computed if
the same unknown is queried multiple times within one right-hand side. In fact,
the latter property constitutes an essential proof step in our formalization. Fur-
thermore, the RLD solver always combines the old value for an unknown with
its new value. This implies that the domain of values should provide some join
operator, whereas our algorithm is fully generic by making no assumptions on
the domain of values—except providing an element ⊥, and an equality operator.
    De Vilhena et al. [30] use Iris to formalize a local generic solver and prove
its partial correctness. Like the RLD, their solver detects dependencies between
unknowns on the ﬂy and can deal with a possibly inﬁnite equation system. It
does, however, not rely on recursive descent into encountered unknowns. Instead,
it uses a worklist to iterate over the unknowns, which are either new or whose
current values are possibly outdated. Similarly to the RLD, this does not require
a non-local destabilization. In comparison, recursive descent into unknowns, as
done by the TD, is likely to be more eﬃcient than plain worklist iteration. Due
to recursive descent, the evaluation of right-hand sides always uses the currently
best values for encountered unknowns and thus may avoid useless computation.
To prove that the results computed by their solver are part of an optimal least
ﬁxpoint, Vilhena et al. [30] assume that the domain of values is partially ordered
and right-hand sides are monotonic. In practical applications such as interpro-
cedural analysis, or the analysis of concurrent systems, though, monotonicity
                                                The Top-Down Solver Veriﬁed         321

cannot always be assumed. This is why our solver is proven partially correct
independent of any assumptions on ordering or monotonicity.

6   Conclusion
This work provides a formal proof of the partial correctness of the TD. We
ﬁrst proved the plain TD to be partially correct and then proved that the TD
is equivalent to the plain TD. For complete lattices and monotonic right-hand
sides, the computed partial solution agrees with the least solution of the equation
system on all stable unknowns. A proof of this fact can be obtained by extending
the given proof with further invariants. When the complete lattice additionally
satisﬁes the ascending chain condition and the set of unknowns is ﬁnite, the
TD is guaranteed to terminate. In this case, partial correctness turns into total
correctness.
    Another task for future work is to incorporate widening and narrowing [3,28]
into the solver and prove correctness. Widening and narrowing cannot be consid-
ered another semantics-preserving optimization. Even for complete lattices, the
computed result is generally no longer the least solution. In case that narrowing
is intertwined with widening as proposed by Seidl and Vogler [26] and right-
hand sides are non-monotonic, the result need not be a (post-)solution. Further
future work is to support side-eﬀecting equation systems [2], where right-hand
sides may not only contribute to the left-hand side but also contribute to other
unknowns.

Acknowledgements. This work was supported by the German Research Foundation
(DFG) - 378803395/2428 ConVeY and by Shota Rustaveli National Science Founda-
tion of Georgia under the project FR-21-7973.


References
 1. Akhin, M., Belyaev, M.: Variable initialization analysis (2020). https://kotlinlang.
    org/spec/control--and-data-ﬂow-analysis.html#variable-initialization-analysis
 2. Apinis, K., Seidl, H., Vojdani, V.: Side-eﬀecting constraint systems: a Swiss army
    knife for program analysis. In: Jhala, R., Igarashi, A. (eds.) Programming Lan-
    guages and Systems - 10th Asian Symposium, APLAS 2012, Kyoto, Japan, 11–
    13 December 2012. Proceedings. LNCS, vol. 7705, pp. 157–172. Springer, Cham
    (2012). https://doi.org/10.1007/978-3-642-35182-2_12
 3. Apinis, K., Seidl, H., Vojdani, V.: How to combine widening and narrowing for
    non-monotonic systems of equations. In: Boehm, H., Flanagan, C. (eds.) ACM SIG-
    PLAN Conference on Programming Language Design and Implementation, PLDI
    2013, Seattle, WA, USA, 16–19 June 2013, pp. 377–386. ACM (2013). https://doi.
    org/10.1145/2491956.2462190
 4. Apinis, K., Seidl, H., Vojdani, V.: Enhancing top-down solving with widening and
    narrowing. In: Probst, C.W., Hankin, C., Hansen, R.R. (eds.) Semantics, Logics,
    and Calculi - Essays Dedicated to Hanne Riis Nielson and Flemming Nielson on
    the Occasion of Their 60th Birthdays. LNCS, vol. 9560, pp. 272–288. Springer,
    Cham (2016). https://doi.org/10.1007/978-3-319-27810-0_14
322     Y. Stade et al.

 5. Bertot, Y., Grégoire, B., Leroy, X.: A structured approach to proving compiler opti-
    mizations based on dataﬂow analysis. In: Filliâtre, J., Paulin-Mohring, C., Werner,
    B. (eds.) Types for Proofs and Programs, International Workshop, TYPES 2004,
    Jouy-en-Josas, France, 15–18 December 2004, Revised Selected Papers. LNCS, vol.
    3839, pp. 66–81. Springer, Cham (2004). https://doi.org/10.1007/11617990_5
 6. Cachera, D., Jensen, T.P., Pichardie, D., Rusu, V.: Extracting a data ﬂow anal-
    yser in constructive logic. In: Schmidt, D.A. (ed.) Programming Languages and
    Systems, 13th European Symposium on Programming, ESOP 2004, Held as Part
    of the Joint European Conferences on Theory and Practice of Software, ETAPS
    2004, Barcelona, Spain, 29 March–2 April 2004, Proceedings. LNCS, vol. 2986, pp.
    385–400. Springer, Cham (2004). https://doi.org/10.1007/978-3-540-24725-8_27
 7. Cachera, D., Pichardie, D.: A certiﬁed denotational abstract interpreter. In: Kauf-
    mann, M., Paulson, L.C. (eds.) Interactive Theorem Proving, First International
    Conference, ITP 2010, Edinburgh, UK, 11–14 July 2010, Proceedings. LNCS, vol.
    6172, pp. 9–24. Springer, Cham (2010). https://doi.org/10.1007/978-3-642-14052-
    5_3
 8. Coupet-Grimal, S., Delobel, W.: A uniform and certiﬁed approach for two static
    analyses. In: Filliâtre, J., Paulin-Mohring, C., Werner, B. (eds.) Types for Proofs
    and Programs, International Workshop, TYPES 2004, Jouy-en-Josas, France,
    15–18 December 2004, Revised Selected Papers. LNCS, vol. 3839, pp. 115–137.
    Springer, Cham (2004). https://doi.org/10.1007/11617990_8
 9. Cousot, P., Cousot, R.: Abstract interpretation: a uniﬁed lattice model for static
    analysis of programs by construction or approximation of ﬁxpoints. In: Graham,
    R.M., Harrison, M.A., Sethi, R. (eds.) Conference Record of the Fourth ACM
    Symposium on Principles of Programming Languages, Los Angeles, California,
    USA, January 1977, pp. 238–252. ACM (1977). https://doi.org/10.1145/512950.
    512973
10. Cousot, P., Cousot, R.: Abstract interpretation frameworks. J. Log. Comput. 2(4),
    511–547 (1992). https://doi.org/10.1093/LOGCOM/2.4.511
11. Fecht, C., Seidl, H.: A faster solver for general systems of equations. Sci. Comput.
    Program. 35(2), 137–161 (1999). https://doi.org/10.1016/S0167-6423(99)00009-X
12. Franceschino, L., Pichardie, D., Talpin, J.: Veriﬁed functional programming of an
    abstract interpreter. In: Dragoi, C., Mukherjee, S., Namjoshi, K.S. (eds.) Static
    Analysis - 28th International Symposium, SAS 2021, Chicago, IL, USA, 17–19
    October 2021, Proceedings. LNCS, vol. 12913, pp. 124–143. Springer, Cham (2021).
    https://doi.org/10.1007/978-3-030-88806-0_6
13. Gosling, J., et al.: Chapter 16. Deﬁnite Assignment, September 2023. https://docs.
    oracle.com/javase/specs/jls/se21/html/jls-16.html
14. Hecht, M.S., Ullman, J.D.: Analysis of a simple algorithm for global data ﬂow
    problems. In: Proceedings of the 1st Annual ACM SIGACT-SIGPLAN Symposium
    on Principles of Programming Languages, pp. 207–217, POPL 1973. Association
    for Computing Machinery, New York, NY, USA (1973). https://doi.org/10.1145/
    512927.512946
                                                   The Top-Down Solver Veriﬁed           323

15. Hermenegildo, M.V., et al.: An overview of the Ciao system. In: Bassiliades, N.,
    Governatori, G., Paschke, A. (eds.) Rule-Based Reasoning, Programming, and
    Applications - 5th International Symposium, RuleML 2011 - Europe, Barcelona,
    Spain, 19–21 July 2011. Proceedings. LNCS, vol. 6826, p. 2. Springer, Cham (2011).
    https://doi.org/10.1007/978-3-642-22546-8_2
16. Hofmann, M., Karbyshev, A., Seidl, H.: Verifying a local generic solver in Coq. In:
    Cousot, R., Martel, M. (eds.) Static Analysis - 17th International Symposium, SAS
    2010, Perpignan, France, 14–16 September, 2010. Proceedings. LNCS, vol. 6337, pp.
    340–355. Springer, Cham (2010). https://doi.org/10.1007/978-3-642-15769-1_21
17. Hofmann, M., Karbyshev, A., Seidl, H.: What is a pure functional? In: Abramsky,
    S., Gavoille, C., Kirchner, C., auf der Heide, F.M., Spirakis, P.G. (eds.) Automata,
    Languages and Programming, 37th International Colloquium, ICALP 2010, Bor-
    deaux, France, 6–10 July 2010, Proceedings, Part II. LNCS, vol. 6199, pp. 199–210.
    Springer, Cham (2010). https://doi.org/10.1007/978-3-642-14162-1_17
18. Jourdan, J.: Verasco: a formally veriﬁed C static analyzer. (Verasco: un analy-
    seur statique pour C formellement vériﬁé). Ph.D. thesis, Paris Diderot University,
    France (2016). https://tel.archives-ouvertes.fr/tel-01327023
19. Karbyshev, A.: Monadic parametricity of second-order functionals. Ph.D. thesis,
    Technische Universität München (2013). https://mediatum.ub.tum.de/1144371
20. Kildall, G.A.: A uniﬁed approach to global program optimization. In: Fischer, P.C.,
    Ullman, J.D. (eds.) Conference Record of the ACM Symposium on Principles of
    Programming Languages, Boston, Massachusetts, USA, October 1973, pp. 194–
    206. ACM Press (1973). https://doi.org/10.1145/512927.512945
21. Le Charlier, B., Van Hentenryck, P.: A universal top-down ﬁxpoint algorithm.
    Technical report CS-92-25, University of Namur and Brown University, May 1992
22. Muthukumar, K., Hermenegildo, M.V.: Compile-time derivation of variable depen-
    dency using abstract interpretation. J. Log. Program. 13(2&3), 315–347 (1992).
    https://doi.org/10.1016/0743-1066(92)90035-2
23. Nipkow, T.: Veriﬁed bytecode veriﬁers. In: Honsell, F., Miculan, M. (eds.) Founda-
    tions of Software Science and Computation Structures, 4th International Confer-
    ence, FOSSACS 2001 Held as Part of the Joint European Conferences on Theory
    and Practice of Software, ETAPS 2001 Genova, Italy, 2–6 April 2001, Proceedings.
    LNCS, vol. 2030, pp. 347–363. Springer, Cham (2001). https://doi.org/10.1007/3-
    540-45315-6_23
24. Nipkow, T., Klein, G.: Concrete Semantics - With Isabelle/HOL. Springer, Cham
    (2014). ISBN 978-3-319-10541, https://doi.org/10.1007/978-3-319-10542-0
25. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL - A Proof Assistant for
    Higher-Order Logic. LNCS, vol. 2283. Springer, Cham (2002). ISBN 3-540-43376,
    https://doi.org/10.1007/3-540-45949-9
26. Seidl, H., Vogler, R.: Three improvements to the top-down solver. Math.
    Struct. Comput. Sci. 31(9), 1090–1134 (2021). https://doi.org/10.1017/
    S0960129521000499
27. Stade, Y., Tilscher, S., Seidl, H.: Partial correctness of the top-down solver. Archive
    of Formal Proofs, May 2024. ISSN 2150-914x. https://isa-afp.org/entries/Top_
    Down_Solver.html. Formal proof development
28. Tilscher, S., Stade, Y., Schwarz, M., Vogler, R., Seidl, H.: The top-down solver—an
    exercise in A2 I. In: Arceri, V., Cortesi, A., Ferrara, P., Olliaro, M. (eds.) Challenges
    of Software Veriﬁcation, vol. 238, pp. 157–179. Springer, Singapore (2023). https://
    doi.org/10.1007/978-981-19-9601-6_9
324     Y. Stade et al.

29. Vergauwen, B., Wauman, J., Lewi, J.: Eﬃcient ﬁxpoint computation. In: Charlier,
    B.L. (ed.) Static Analysis, First International Static Analysis Symposium, SAS
    1994, Namur, Belgium, 28–30 September 1994, Proceedings. LNCS, vol. 864, pp.
    314–328. Springer, Cham (1994). https://doi.org/10.1007/3-540-58485-4_49
30. de Vilhena, P.E., Pottier, F., Jourdan, J.: Spy game: verifying a local generic solver
    in Iris. Proc. ACM Program. Lang. 4(POPL), 33:1–33:28 (2020). https://doi.org/
    10.1145/3371101
31. Vojdani, V., Apinis, K., Rõtov, V., Seidl, H., Vene, V., Vogler, R.: Static race
    detection for device drivers: the Goblint approach. In: Lo, D., Apel, S., Khurshid, S.
    (eds.) Proceedings of the 31st IEEE/ACM International Conference on Automated
    Software Engineering, ASE 2016, Singapore, 3–7 September 2016, pp. 391–402.
    ACM (2016). https://doi.org/10.1145/2970276.2970337




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
