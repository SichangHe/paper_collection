                                              On Counterexample Guided Quantifier Instantiation
                                                         for Synthesis in CVC4⋆ ⋆⋆

                                                                    Andrew Reynolds1 , Morgan Deters2 ,
                                                             Viktor Kuncak1, Cesare Tinelli3 , and Clark Barrett2
arXiv:1502.04464v3 [cs.LO] 23 Jun 2015




                                                       1
                                                           École Polytechnique Fédérale de Lausanne (EPFL), Switzerland
                                                             2
                                                                Department of Computer Science, New York University
                                                            3
                                                               Department of Computer Science, The University of Iowa



                                                Abstract. We introduce the first program synthesis engine implemented inside
                                                an SMT solver. We present an approach that extracts solution functions from un-
                                                satisfiability proofs of the negated form of synthesis conjectures. We also discuss
                                                novel counterexample-guided techniques for quantifier instantiation that we use
                                                to make finding such proofs practically feasible. A particularly important class of
                                                specifications are single-invocation properties, for which we present a dedicated
                                                algorithm. To support syntax restrictions on generated solutions, our approach
                                                can transform a solution found without restrictions into the desired syntactic
                                                form. As an alternative, we show how to use evaluation function axioms to embed
                                                syntactic restrictions into constraints over algebraic datatypes, and then use an
                                                algebraic datatype decision procedure to drive synthesis. Our experimental eval-
                                                uation on syntax-guided synthesis benchmarks shows that our implementation in
                                                the CVC4 SMT solver is competitive with state-of-the-art tools for synthesis.


                                         1 Introduction

                                         The synthesis of functions that meet a given specification is a long-standing fundamen-
                                         tal goal that has received great attention recently. This functionality directly applies to
                                         the synthesis of functional programs [17, 18] but also translates to imperative programs
                                         through techniques that include bounding input space, verification condition generation,
                                         and invariant discovery [27–29]. Function synthesis is also an important subtask in the
                                         synthesis of protocols and reactive systems, especially when these systems are infinite-
                                         state [3,26]. The SyGuS format and competition [1,2,22] inspired by the success of the
                                         SMT-LIB and SMT-COMP efforts [5], has significantly improved and simplified the
                                         process of rigorously comparing different solvers on synthesis problems.
                                              Connection between synthesis and theorem proving was established already in early
                                         work on the subject [12, 20]. It is notable that early research [20] found that the capa-
                                         bilities of theorem provers were the main bottleneck for synthesis. Taking lessons from
                                         automated software verification, recent work on synthesis has made use of advances
                                          ⋆
                                            This work is supported in part by the European Research Council (ERC) Project Implicit Pro-
                                            gramming and Swiss National Science Foundation Grant Constraint Solving Infrastructure for
                                            Program Analysis.
                                         ⋆⋆
                                            This paper is dedicated to the memory of Morgan Deters who died unexpectedly in Jan 2015.
2         Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli, and Clark Barrett

in theorem proving, particularly in SAT and SMT solvers. However, that work avoids
formulating the overall synthesis task as a theorem proving problem directly. Instead,
existing work typically builds custom loops outside of an SMT or SAT solver, often us-
ing numerous variants of counterexample-guided synthesis. A typical role of the SMT
solver has been to validate candidate solutions and provide counterexamples that guide
subsequent search, although approaches such as symbolic term exploration [15] also
use an SMT solver to explore a representation of the space of solutions. In existing
approaches, SMT solvers thus receive a large number of separate queries, with limited
communication between these different steps.
Contributions. In this paper, we revisit the formulation of the overall synthesis task as
a theorem proving problem. We observe that SMT solvers already have some of the key
functionality for synthesis; we show how to improve existing algorithms and introduce
new ones to make SMT-based synthesis competitive. Specifically, we do the following.

    – We show how to formulate an important class of synthesis problems as the prob-
      lem of disproving universally quantified formulas, and how to synthesize functions
      automatically from selected instances of these formulas.
    – We present counterexample-guided techniques for quantifier instantiation, which
      are crucial to obtain competitive performance on synthesis tasks.
    – We discuss techniques to simplify the synthesized functions, to help ensure that
      they are small and adhere to specified syntactic requirements.
    – We show how to encode syntactic restrictions using theories of algebraic datatypes
      and axiomatizable evaluation functions.
    – We show that for an important class of single-invocation properties, the synthesis of
      functions from relations, the implementation of our approach in CVC4 significantly
      outperforms leading tools from the SyGuS competition.

Preliminaries. Since synthesis involves finding (and so proving the existence) of func-
tions, we use notions from many-sorted second-order logic to define the general prob-
lem. We fix a set S of sort symbols and an (infix) equality predicate ≈ of type σ × σ for
each σ ∈ S. For every non-empty sort sequence σ ∈ S+ with σ = σ1 · · · σn σ, we fix
an infinite set Xσ of variables xσ1 ···σn σ of type σ1 × · · · × σn → σ. For each sort σ we
identity the type () → σ with σ and call it a first-order type. We assume the sets Xσ are
pairwise disjoint and let X be their union. A signature Σ consists of a set Σ s ⊆ S of sort
symbols and a set Σ f of function symbols f σ1 ···σn σ of type σ1 × · · · × σn → σ, where
n ≥ 0 and σ1 , . . . , σn , σ ∈ Σ s . We drop the sort superscript from variables or function
symbols when it is clear from context or unimportant. We assume that signatures al-
ways include a Boolean sort Bool and constants ⊤ and ⊥ of type Bool (respectively, for
true and false). Given a many-sorted signature Σ together with quantifiers and lambda
abstraction, the notion of well-sorted (Σ-)term, atom, literal, clause, and formula with
variables in X are defined as usual in second-order logic. All atoms have the form s ≈ t.
Having ≈ as the only predicate symbol causes no loss of generality since we can model
other predicate symbols as function symbols with return sort Bool. We will, however,
write just t in place of the atom t ≈ ⊤, to simplify the notation. A Σ-term/formula is
ground if it has no variables, it is first-order if it has only first-order variables, that is,
variables of first-order type. When x = (x1 , . . . , xn ) is a tuple of variables and Q is
            On Counterexample Guided Quantifier Instantiation for Synthesis in CVC4              3

either ∀ or ∃, we write Qx ϕ as an abbreviation of Qx1 · · · Qxn ϕ. If e is a Σ-term or
formula and x = (x1 , . . . , xn ) has no repeated variables, we write e[x] to denote that
all of e’s free variables are from x; if t = (t1 , . . . , tn ) is a term tuple, we write e[t] for
the term or formula obtained from e by simultaneously replacing, for all i = 1, . . . , n,
every occurrence of xi in e by ti . A Σ -interpretation I maps: each σ ∈ Σ s to a non-
empty set σ I , the domain of σ in I, with BoolI = {⊤, ⊥}; each uσ1 ···σn σ ∈ X ∪ Σ f
to a total function uI : σ1I × · · · × σnI → σ I when n > 0 and to an element of σ I
when n = 0. The interpretation I induces as usual a mapping from terms t of sort σ to
elements tI of σ I . If x1 , . . . , xn are variables and v1 , . . . , vn are well-typed values for
them, we denote by I[x1 7→ v1 , . . . , xn 7→ vn ] the Σ-interpretation that maps each xi
to vi and is otherwise identical to I. A satisfiability relation between Σ-interpretations
and Σ-formulas is defined inductively as usual.
     A theory is a pair T = (Σ, I) where Σ is a signature and I is a non-empty class
of Σ-interpretations, the models of T , that is closed under variable reassignment (i.e.,
every Σ-interpretation that differs from one in I only in how it interprets the variables is
also in I) and isomorphism. A Σ-formula ϕ[x] is T -satisfiable (resp., T -unsatisfiable )
if it is satisfied by some (resp., no) interpretation in I. A satisfying interpretation for ϕ
models (or is a model of) ϕ. A formula ϕ is T -valid, written |=T ϕ, if every model of
T is a model of ϕ. Given a fragment L of the language of Σ-formulas, a Σ-theory T is
satisfaction complete with respect to L if every T -satisfiable formula of L is T -valid. In
this paper we will consider only theories that are satisfaction complete wrt the formulas
we are interested in. Most theories used in SMT (in particular, all theories of a specific
structure such various theories of the integers, reals, strings, algebraic datatypes, bit
vectors, and so on) are satisfaction complete with respect to the class of closed first-
order Σ-formulas. Other theories, such as the theory of arrays, are satisfaction complete
only with respect to considerably more restricted classes of formulas.


2 Synthesis inside an SMT Solver

We are interested in synthesizing computable functions automatically from formal log-
ical specifications stating properties of these functions. As we show later, under the
right conditions, we can formulate a version of the synthesis problem in first-order
logic alone, which allows us to tackle the problem using SMT solvers.
    We consider the synthesis problem in the context of some theory T of signature Σ
that allows us to provide the function’s specification as a Σ-formula. Specifically, we
consider synthesis conjectures expressed as (well-sorted) formulas of the form

                       ∃f σ1 ···σn σ ∀xσ1 1 · · · ∀xσnn P [f, x1 , . . . , xn ]                (1)

or ∃f ∀x P [f, x], for short, where the second-order variable f represents the function
to be synthesized and P is a Σ-formula encoding properties that f must satisfy for all
possible values of the input tuple x = (x1 , . . . , xn ). In this setting, finding a witness for
this satisfiability problem amounts to finding a function of type σ1 × · · · × σn → σ in
some model of T that satisfies ∀x P [f, x]. Since we are interested in automatic synthe-
sis, we the restrict ourselves here to methods that search over a subspace S of solutions
4          Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli, and Clark Barrett

representable syntactically as Σ-terms. We will say then that a synthesis conjecture is
solvable if it has a syntactic solution in S.
    In this paper we present two approaches that work with classes L of synthesis con-
jectures and Σ-theories T that are satisfaction complete wrt L. In both approaches,
we solve a synthesis conjecture ∃f ∀x P [f, x] by relying on quantifier-instantiation
techniques to produce a first-order Σ-term t[x] of sort σ such that ∀x P [t, x] is T -
satisfiable. When this t is found, the synthesized function is denoted by λx. t .
    In principle, to determine the satisfiability of ∃f ∀x P [f, x] an SMT solver sup-
porting the theory T can consider the satisfiability of the (open) formula ∀x P [f, x] by
treating f as an uninterpreted function symbol. This sort of Skolemization is not usually
a problem for SMT solvers as many of them can process formulas with uninterpreted
symbols. The real challenge is the universal quantification over x because it requires
the solver to construct internally (a finite representation of) an interpretation of f that
is guaranteed to satisfy P [f, x] for every possible value of x [11, 23].
    More traditional SMT solver designs to handle universally quantified formulas have
focused on instantiation-based methods to show unsatisfiability. They generate ground
instances of those formulas until a refutation is found at the ground level [10]. While
these techniques are incomplete in general, they have been shown to be quite effective
in practice [9, 24]. For this reason, we advocate approaches to synthesis geared toward
establishing the unsatisfiability of the negation of the synthesis conjecture:

                                           ∀f ∃x ¬P [f, x]                                           (2)

Thanks to our restriction to satisfaction complete theories, (2) is T -unsatisfiable exactly
when the original synthesis conjecture (1) is T -satisfiable.4 Moreover, as we explain in
this paper, a syntactic solution λx. t for (1) can be constructed from a refutation of (2),
as opposed to being extracted from the valuation of f in a model of ∀x P [f, x].
Two synthesis methods. Proving (2) unsatisfiable poses its own challenge to current
SMT solvers, namely, dealing with the second-order universal quantification of f . To
our knowledge, no SMT solvers so far had direct support for higher-order quantifica-
tion. In the following, however, we describe two specialized methods to refute negated
synthesis conjectures like (2) that build on existing capabilities of these solvers.
    The first method applies to a restricted, but fairly common, case of synthesis prob-
lems ∃f ∀x P [f, x] where every occurrence of f in P is in terms of the form f (x). In
this case, we can express the problem in the first-order form ∀x.∃y.Q[x, y] and then
tackle its negation using appropriate quantifier instantiation techniques.
    The second method follows the syntax-guided synthesis paradigm [1, 2] where the
synthesis conjecture is accompanied by an explicit syntactic restriction on the space
of possible solutions. Our syntax-guided synthesis method is based on encoding the
syntax of terms as first-order values. We use a deep embedding into an extension of the
background theory T with a theory of algebraic data types, encoding the restrictions of
a syntax-guided synthesis problem.
 4
      Other approaches in the verification and synthesis literature also rely implicitly, and in some
     cases unwittingly, on this restriction or stronger ones. We make satisfaction completeness ex-
     plicit here as a sufficient condition for reducing satisfiability problems to unsatisfiability ones.
             On Counterexample Guided Quantifier Instantiation for Synthesis in CVC4                  5

    For the rest of the paper, we fix a Σ-theory T and a class P of quantifier-free
Σ-formulas P [f, x] such that T is satisfaction complete with respect to the class of
synthesis conjectures L := {∃f ∀x P [f, x] | P ∈ P}.

3 Refutation-Based Synthesis
When axiomatizing properties of a desired function f of type σ1 × · · · × σn → σ, a
particularly well-behaved class are single-invocation properties (see, e.g., [13]). These
properties include, in particular, standard function contracts, so they can be used to
synthesize a function implementation given its postcondition as a relation between the
arguments and the result of the function. This is also the form of the specification for
synthesis problems considered in complete functional synthesis [16–18]. Note that, in
our case, we aim to prove that the output exists for all inputs, as opposed to, more
generally, computing the set of inputs for which the output exists.
    A single-invocation property is any formula of the form Q[x, f (x)] obtained as
an instance of a quantifier-free formula Q[x, y] not containing f . Note that the only
occurrences of f in Q[x, f (x)] are in subterms of the form f (x) with the same tuple x
of pairwise distinct variables.5 The conjecture ∃f ∀x Q[x, f (x)] is logically equivalent
to the first-order formula
                                      ∀x ∃y Q[x, y]                                   (3)
By the semantics of ∀ and ∃, finding a model I for it amounts (under the axioms of
choice) to finding a function h : σ1I ×· · ·×σnI → σ I such that for all s ∈ σ1I ×· · ·×σnI ,
the interpretation I[x 7→ s, y 7→ h(s)] satisfies Q[x, y]. This section considers the
case when P consists of single-invocation properties and describes a general approach
for determining the satisfiability of formulas like (3) while computing a syntactic rep-
resentation of a function like h in the process. For the latter, it will be convenient
to assume that the language of functions contains an if-then-else operator ite of type
Bool × σ × σ → σ for each sort σ, with the usual semantics.
    If (3) belongs to a fragment that admits quantifier elimination in T , such as the linear
fragment of integer arithmetic, determining its satisfiability can be achieved using an
efficient method for quantifier elimination [7,21]. Such cases have been examined in the
context of software synthesis [17]. Here we propose instead an alternative instantiation-
based approach aimed at establishing the unsatisfiability of the negated form of (3):

                                           ∃x ∀y ¬Q[x, y]                                            (4)
or, equivalently, of a Skolemized version ∀y ¬Q[k, y] of (4) for some tuple k of fresh
uninterpreted constants of the right sort. Finding a T -unsatisfiable finite set Γ of ground
instances of ¬Q[k, y], which is what an SMT solver would do to prove the unsatisfia-
bility of (4), suffices to solve the original synthesis problem. The reason is that, then, a
solution for f can be constructed directly from Γ , as indicated by the following result.
Proposition 1. Suppose some set Γ = {¬Q[k, t1 [k]], . . . , ¬Q[k, tp [k]]} where t1 [x],
. . ., tp [x] are Σ-terms of sort σ is T -unsatisfiable. One solution for ∃f ∀x Q[x, f (x)]
is λx. ite(Q[x, tp ], tp , ( · · · ite(Q[x, t2 ], t2 , t1 ) · · · )).
 5
     An example of a property that is not single-invocation is ∀x1 x2 f (x1 , x2 ) ≈ f (x2 , x1 ).
6           Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli, and Clark Barrett

    1. Γ := {G ⇒ Q[k, e]} where k consists of distinct fresh constants
    2. Repeat
            If there is a model I of T satisfying Γ and G
            then let Γ := Γ ∪ {¬Q[k, t[k]]} for some Σ-term t[x] such that t[k]I = eI ;
            otherwise, return “no solution found”
       until Γ contains a T -unsatisfiable set {¬Q[k, t1 [k]], . . . , ¬Q[k, tp [k]]}
    3. Return λx. ite(Q[x, tp [x]], tp [x], ( · · · ite(Q[x, t2 [x]], t2 [x], t1 [x]) · · · )) for f

Fig. 1. A refutation-based synthesis procedure for single-invocation property ∃f ∀x Q[x, f (x)].
Proof: Let ℓ be the solution specified above, and let u be an arbitrary set of ground
terms of the same sort as x. Given a model I, we show that I |= Q[u, ℓ(u)]. Consider
the case that I |= Q[u, ti [u]] for some i ∈ {2, . . . , p}; pick the greatest such i. Then,
ℓ(u)I = (ti [u])I , and thus I |= Q[u, ℓ(u)]. If no such i exists, then I |= ¬Q[u, ti [u]]
for all i = 2, . . . , p, and ℓ(u)I = (t1 [u])I . Since Γ is T -unsatisfiable and k are fresh,
we have ¬Q[u, t2 [u]], . . . , ¬Q[u, tp [u]] |=T Q[u, t1 [u]], which is Q[u, ℓ(u)]. 


Example 1. Let T be the theory of linear integer arithmetic with the usual signature and
integer sort Int. Let x = (x1 , x2 ). Now consider the property

              P [f, x] := f (x) ≥ x1 ∧ f (x) ≥ x2 ∧ (f (x) ≈ x1 ∨ f (x) ≈ x2 )                         (5)

with f of type Int × Int → Int and x1 , x2 of type Int. The synthesis problem
∃f ∀x P [f, x] is solved exactly by the function that returns the maximum of its two
inputs. Since P is a single-invocation property, we can solve that problem by proving
the T -unsatisfiability of the conjecture ∃x ∀y ¬Q[x, y] where

                         Q[x, y] := y ≥ x1 ∧ y ≥ x2 ∧ (y ≈ x1 ∨ y ≈ x2 )                               (6)

After Skolemization the conjecture becomes ∀y ¬Q[a, y] for fresh constants a =
(a1 , a2 ). When asked to determine the satisfiability of that conjecture an SMT solver
may, for instance, instantiate it with a1 and then a2 for y, producing the T -unsatisfiable
set {¬Q[a, a1 ], ¬Q[a, a2 ]}. By Proposition 1, one solution for ∀x P [f, x] is f =
λx. ite(Q[x, x2 ], x2 , x1 ), which simplifies to λx. ite(x2 ≥ x1 , x2 , x1 ), representing
the desired maximum function.                                                            

Synthesis by Counterexample-Guided Quantifier Instantiation. Given Proposi-
tion 1, the main question is how to get the SMT solver to generate the necessary ground
instances from ∀y ¬Q[k, y]. Typically, SMT solvers that reason about quantified for-
mulas use heuristic quantifier instantiation techniques based on E-matching [9], which
instantiates universal quantifiers with terms occurring in some current set of ground
terms built incrementally from the input formula. Using E-matching-based heuristic in-
stantiation alone is unlikely to be effective in synthesis, where required terms need to
be synthesized based on the semantics of the input specification. This is confirmed by
our preliminary experiments, even for simple conjectures. We have developed instead
a specialized new technique, which we refer to as counterexample-guided quantifier
instantiation, that allows the SMT solver to quickly converge in many cases to the in-
stantiations that refute the negated synthesis conjecture (4).
           On Counterexample Guided Quantifier Instantiation for Synthesis in CVC4          7

    The new technique is similar to a popular scheme for synthesis known as
counterexample-guided inductive synthesis, implemented in various synthesis ap-
proaches (e.g., [14, 28]), but with the major difference of being built-in directly into
the SMT solver. The technique is illustrated by the procedure in Figure 1, which grows
a set Γ of ground instances of ¬Q[k, y] starting with the formula G ⇒ Q[k, e] where
G and e are fresh constants of sort Bool and σ, respectively. Intuitively, e represents a
current, partial solution for the original synthesis conjecture ∃f ∀x Q[x, f (x)], while G
represents the possibility that the conjecture has a (syntactic) solution in the first place.
    The procedure, which may not terminate in general, terminates either when Γ be-
comes unsatisfiable, in which case it has found a solution, or when Γ is still satisfiable
but all of its models falsify G, in which case the search for a solution was inconclusive.
The procedure is not solution-complete, that is, it is not guaranteed to return a solution
whenever there is one. However, thanks to Proposition 1, it is solution-sound : every
λ-term it returns is indeed a solution of the original synthesis problem.

Finding instantiations. The choice of the term t in Step 2 of the procedure is inten-
tionally left underspecified because it can be done in a number of ways. Having a good
heuristic for such instantiations is, however, critical to the effectiveness of the procedure
in practice. In a Σ-theory T , like integer arithmetic, with a fixed interpretation for sym-
bols in Σ and a distinguished set of ground Σ-terms denoting the elements of a sort, a
simple, if naive, choice for t in Figure 1 is the distinguished term denoting the element
eI . For instance, if σ is Int in integer arithmetic, t could be a concrete integer constant
(0, ±1, ±2, . . .). This choice amounts to testing whether points in the codomain of the
sought function f satisfy the original specification P .
     More sophisticated choices for t, in particular where t contains the variables x,
may increase the generalization power of this procedure and hence its ability to find a
solution. For instance, our present implementation in the CVC4 solver relies on the fact
that the model I in Step 2 is constructed from a set of equivalence classes over terms
computed by the solver during its search. The procedure selects the term t among those
in the equivalence class of e, other than e itself. For instance, consider formula (6) from
the previous example that encodes the single-invocation form of the specification for
the max function. The DPLL(T) architecture, on which CVC4 is based, finds a model
for Q[a, e] with a = (a1 , a2 ) only if it can first find a subset M of that formula’s
literals that collectively entail Q[a, e] at the propositional level. Due to the last conjunct
of (6), M must include either e ≈ a1 or e ≈ a2 . Hence, whenever a model can be
constructed for Q[a, e], the equivalence class containing e must contain either a1 or a2 .
Thus using the above selection heuristic, the procedure in Figure 1 will, after at most
two iterations of the loop in Step 2, add the instances ¬Q[a, a1 ] and ¬Q[a, a2 ] to Γ . As
noted in Example 1, these two instances are jointly T -unsatisfiable. We expect that more
sophisticated instantiation techniques can be incorporated. In particular, both quantifier
elimination techniques [7, 21] and approaches currently used to infer invariants from
templates [8, 19] are likely to be beneficial for certain classes of synthesis problems.
The advantage of developing these techniques within an SMT solver is that they directly
benefit both synthesis and verification in the presence of quantified conjectures, thus
fostering cross-fertilization between different fields.
8          Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli, and Clark Barrett

    ∀x y ev(x1 , x, y) ≈ x           ∀s1 s2 x y ev(leq(s1 , s2 ), x, y) ≈ (ev(s1 , x, y) ≤ ev(s2 , x, y))
    ∀x y ev(x2 , x, y) ≈ y           ∀s1 s2 x y ev(eq(s1 , s2 ), x, y) ≈ (ev(s1 , x, y) ≈ ev(s2 , x, y))
    ∀x y ev(zero, x, y) ≈ 0          ∀c1 c2 x y ev(and(c1 , c2 ), x, y) ≈ (ev(c1 , x, y) ∧ ev(c2 , x, y))
    ∀x y ev(one, x, y) ≈ 1           ∀c x y ev(not(c), x, y) ≈ ¬ev(c, x, y)
    ∀s1 s2 x y ev(plus(s1 , s2 ), x, y) ≈ ev(s1 , x, y) + ev(s2 , x, y)
    ∀s1 s2 x y ev(minus(s1 , s2 ), x, y) ≈ ev(s1 , x, y) − ev(s2 , x, y)
    ∀c s1 s2 x y ev(if(c, s1 , s2 ), x, y) ≈ ite(ev(c, x, y), ev(s1 , x, y), ev(s2 , x, y))

         Fig. 2. Axiomatization of the evaluation operators in grammar R from Example 2.
4 Refutation-Based Syntax-Guided Synthesis
In syntax-guided synthesis, the functional specification is strengthened by an accom-
panying set of syntactic restrictions on the form of the expected solutions. In a recent
line of work [1, 2, 22] these restrictions are expressed by a grammar R (augmented
with a kind of let binder) defining the language of solution terms, or programs, for the
synthesis problem. In this section, we present a variant of the approach in the previ-
ous section that incorporates the syntactic restriction directly into the SMT solver via a
deep embedding of the syntactic restriction R into the solver’s logic. The main idea is
to represent R as a set of algebraic datatypes and build into the solver an interpretation
of these datatypes in terms of the original theory T .
     While our approach is parametric in the background theory T and the restriction R,
it is best explained here with a concrete example.
Example 2. Consider again the synthesis conjecture (6) from Example 1 but now with
a syntactic restriction R for the solution space expressed by these algebraic datatypes:
              S    :=    x1 | x2 | zero | one | plus(S, S) | minus(S, S) | if(C, S, S)
              C :=       leq(S, S) | eq(S, S) | and(C, C) | not(C)
The datatypes are meant to encode a term signature that includes nullary constructors
for the variables x1 and x2 of (6), and constructors for the symbols of the arithmetic
theory T . Terms of sort S (resp., C) refer to theory terms of sort Int (resp., Bool).
     Instead of the theory of linear integer arithmetic, we now consider its combination
TD with the theory of the datatypes above extended with two evaluation operators, that
is, two function symbols evS×Int×Int→Int and evC×Int×Int→Bool respectively embedding
S in Int and C in Bool. We define TD so that all of its models satisfy the formulas in
Figure 2. The evaluation operators effectively define an interpreter for programs (i.e.,
terms of sort S and C) with input parameters x1 and x2 .
     It is possible to instrument an SMT solver that support user-defined datatypes, quan-
tifiers and linear arithmetic so that it constructs automatically from the syntactic restric-
tion R both the datatypes S and C and the two evaluation operators. Reasoning about
S and C is done by the built-in subsolver for datatypes. Reasoning about the evalua-
tion operators is achieved by reducing ground terms of the form ev(d, t1 , t2 ) to smaller
terms by means of selected instantiations of the axioms from Figure 2, with a number
of instances proportional to the size of term d. It is also possible to show that TD is
satisfaction complete with respect to the class
                        L2 := {∃g ∀z P [λz. ev(g, z), x] | P [f, x] ∈ P}
              On Counterexample Guided Quantifier Instantiation for Synthesis in CVC4             9

 1. Γ := ∅
 2. Repeat
    (a) Let k be a tuple of distinct fresh constants.
        If there is a model I of TD satisfying Γ and G, then Γ := Γ ∪ {¬Pev [eI , k]} ;
        otherwise, return “no solution found”
    (b) If there is a model J of TD satisfying Γ , then Γ := Γ ∪ {G ⇒ Pev [e, kJ ]} ;
        otherwise, return eI as a solution

         Fig. 3. A refutation-based syntax-guided synthesis procedure for ∃f ∀x Pev [f, x].

where instead of terms of the form f (t1 , t2 ) in P we have, modulo β-reductions, terms
of the form ev(g, t1 , t2 ).6 For instance, the formula P [f, x] in Equation (5) from Exam-
ple 1 can be restated in TD as the formula below where g is a variable of type S:

      Pev [g, x] := ev(g, x) ≥ x1 ∧ ev(g, x) ≥ x2 ∧ (ev(g, x) ≈ x1 ∨ ev(g, x) ≈ x2 )

In contrast to P [f, x], the new formula Pev [g, x] is first-order, with the role of the
second-order variable f now played by the first-order variable g.
     When asked for a solution for (5) under the restriction R, the instrumented SMT
solver will try to determine instead the TD -unsatisfiability of ∀g ∃x ¬Pev [g, x]. Instan-
tiating g in the latter formula with s := if(leq(x1 , x2 ), x2 , x1 ), say, produces a formula
that the solver can prove to be TD -unsatisfiable. This suffices to show that the program
ite(x1 ≤ x2 , x2 , x1 ), the analogue of s in the language of T , is a solution of the synthe-
sis conjecture (5) under the syntactic restriction R.                                       

    To prove the unsatisfiability of formulas like ∀g ∃x ¬Pev [g, x] in the example above
we use a procedure similar to that in Section 3, but specialized to the extended theory
TD . The procedure is described in Figure 3. Like the one in Figure 1, it uses an unin-
terpreted constant e representing a solution candidate, and a Boolean variable G repre-
senting the existence of a solution. The main difference, of course, is that now e ranges
over the datatype representing the restricted solution space. In any model of TD , a term
of datatype sort evaluates to a term built exclusively with constructor symbols. This is
why the procedure returns in Step 2b the value of e in the model I found in Step 2a.
As we showed in the previous example, a program that solves the original problem can
then be reconstructed from the returned datatype term.
Implementation. We implemented the procedure in the CVC4 solver. Figure 4 shows
a run of that implementation over the conjecture from Example 2. In this run, note
that each model found for e satisfies all values of counterexamples found for previ-
ous candidates. After the sixth iteration of Step 2a, the procedure finds the candidate
if(leq(x1 , x2 ), x2 , x1 ), for which no counterexample exists, indicating that the procedure
has found a solution for the synthesis conjecture. Currently, this problem can be solved
in about 0.5 seconds in the latest development version of CVC4.
     To make the procedure practical it is necessary to look for small solutions to synthe-
sis conjectures. A simple way to limit the size of the candidate solutions is to consider
 6
      We stress again, that both the instrumentation of the solver and the satisfaction completeness
     argument for the extended theory are generic with respect to the syntactic restriction on the
     synthesis problem and the original satisfaction complete theory T .
10        Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli, and Clark Barrett

       Step   Model                                       Added Formula
        2a    {e 7→ x1 , . . .}                           ¬Pev [x1 , a1 , b1 ]
        2b    {a1 7→ 0, b1 7→ 1, . . .}                   G ⇒ Pev [e, 0, 1]
        2a    {e 7→ x2 , . . .}                           ¬Pev [x2 , a2 , b2 ]
        2b    {a2 7→ 1, b2 7→ 0, . . .}                   G ⇒ Pev [e, 1, 0]
        2a    {e 7→ one, . . .}                           ¬Pev [one, a3 , b3 ]
        2b    {a3 7→ 2, b3 7→ 0, . . .}                   G ⇒ Pev [e, 2, 0]
        2a    {e 7→ plus(x1 , x2 ), . . .}                ¬Pev [plus(x1 , x2 ), a4 , b4 ]
        2b    {a4 7→ 1, b4 7→ 1, . . .}                   G ⇒ Pev [e, 1, 1]
        2a    {e 7→ if(leq(x1 , one), one, x1 ), . . .}   ¬Pev [if(leq(x1 , one), one, x1 ), a5 , b5 ]
        2b    {a5 7→ 1, b5 7→ 2, . . .}                   G ⇒ Pev [e, 1, 2]
        2a    {e 7→ if(leq(x1 , x2 ), x2 , x1 ), . . .}   ¬Pev [if(leq(x1 , x2 ), x2 , x1 ), a6 , b6 ]
        2b    none

For i = 1, . . . , 6, ai and bi are fresh constants of type Int.

                            Fig. 4. A run of the procedure from Figure 3.
smaller programs before larger ones. Adapting techniques for finding finite models of
minimal size [25], we use a strategy that starting, from n = 0, searches for programs
of size n + 1 only after its has exhausted the search for programs of size n. In solvers
based on the DPLL(T ) architecture, like CVC4, this can be accomplished by introducing
a splitting lemma of the form (size(e) ≤ 0 ∨ ¬size(e) ≤ 0) and asserting size(e) ≤ 0
as the first decision literal, where size is a function symbol of type σ → Int for every
datatype sort σ and stands for the function that maps each datatype value to its term
size (i.e., the number of non-nullary constructor applications in the term). We do the
same for size(e) ≤ 1 if and when ¬size(e) ≤ 0 becomes asserted. We extended the
procedure for algebraic datatypes in CVC4 [6] to handle constraints involving size. The
extended procedure remains a decision procedure for input problems with a concrete
upper bound on terms of the form size(u), for each variable or uninterpreted constant u
of datatype sort in the problem. This is enough for our purposes since the only term u
like that in our synthesis procedure is e.

Proposition 2. With the search strategy above, the procedure in Figure 3 has the fol-
lowing properties:
 1. (Solution Soundness) Every term it returns can be mapped to a solution of the
    original synthesis conjecture ∃f ∀x P [f, x] under the restriction R.
 2. (Refutation Soundness) If it answers “no solution found”, the original conjecture
    has no solutions under the restriction R.
 3. (Solution Completeness) If the original conjecture has a solution under R, the pro-
    cedure will find one.

Proof: To show solution soundness, consider the case when the procedure returns
eI as a solution. Then, Γ ∪ ¬Pev [eI , k] is TD -unsatisfiable for some Γ, k, where Γ
is TD -satisfiable and k is a tuple of distinct fresh constants. Since k are fresh, Γ ∪
∃x ¬Pev [eI , x] is TD -unsatisfiable. Since Γ is TD -satisfiable and Γ ∪ ∃x ¬Pev [eI , x] is
not, then at least one model of TD (namely, one for Γ ) does not satisfy ∃x ¬Pev [eI , x].
Thus, since TD is satisfaction complete, no models of TD satisfy ∃x ¬Pev [eI , x], and
            On Counterexample Guided Quantifier Instantiation for Synthesis in CVC4              11

thus all models of TD satisfy ∀x Pev [eI , x]. Assuming our translation from P to Pev
is faithful, the analogue of eI in the language of T is a solution for the conjecture
∃f ∀x P [f, x].
     To show refutation soundness, consider the case when the procedure returns “no
solution found”. Then, there exists a Γ = (Γ ′ ∪ G ⇒ Pev [e, kJ ]) such that Γ ′ is TD -
satisfiable, and Γ ∪G is TD -unsatisfiable. Clearly based on the clauses added by the pro-
cedure, we have that Γ is equivalent to Γ ′′ ∪G ⇒ (Pev [e, u1 ]∧. . .∧Pev [e, un ]), for some
u1 . . . un where Γ ′′ ⊆ Γ ′ is TD -satisfiable and does not contain G or e. Since Γ ∪ G is
TD -unsatisfiable, we have that Γ ′′ ∪Pev [e, u1 ]∧. . .∧Pev [e, un ] is TD -unsatisfiable. Since
Γ ′′ does not contain e, Γ ′′ ∪ ∃y (Pev [y, u1 ] ∧ . . . ∧ Pev [y, un ]) is TD -unsatisfiable. Since
TD is satisfaction complete and Γ ′′ is TD -satisfiable, ∃y (Pev [y, u1 ] ∧ . . . ∧ Pev [y, un ])
is TD -unsatisfiable. Thus, ∃y (Pev [y, u1 ] ∧ . . .∧ Pev [y, un ]) is TD -unsatisfiable, and thus
∃y ∀x Pev [y, x] is TD -unsatisfiable. Assuming our translation from P to Pev is faithful,
this implies there is no solution for the conjecture ∃f ∀x P [f, x].
     Given solution and refutation soundness of the procedure, to show the procedure is
solution complete, it suffices to show that the procedure terminates when the original
conjecture has a solution under R. Let λx. t be such a solution, and let d be the analogue
of t in the language of TD . Let n be equal to the number of datatypes of the same type
as d that are at most the size of d, which we know is finite. For i = 1, 2, . . ., let Ii and
Ji be the models found on the ith iteration of Steps 2a and 2b respectively. Assume the
procedure runs at least k iterations, and let 1 ≤ j < k. Since Jj satisfies ¬Pev [eIj , k],
all models of TD satisfy ¬Pev [eIj , kJj ] since TD is satisfaction complete. Since Ik
satisfies G, it must also satisfy Pev [e, kJj ], and thus eIk 6= eIj . Thus, each eI1 , eI2 , . . .
is distinct, and the procedure in Figure 3 executes at most n iterations of Step 2a. Since
the background theory TD is decidable, Steps 2a and 2b are terminating, and thus the
procedure is terminating when a solution exists.                                                  
     Note that by this proposition the procedure can diverge only if the input synthesis
conjecture has no solution.


5 Single Invocation Techniques for Syntax-Guided Problems

In this section, we considered the combined case of single-invocation synthesis conjec-
tures with syntactic restrictions. Given a set R of syntactic restrictions expressed by a
datatype S for programs and a datatype C for Boolean expressions, consider the case
where (i) S contains the constructor if : C × S × S → S (with the expected meaning)
and (ii) the function to be synthesized is specified by a single-invocation property that
can be expressed as a term of sort C. This is the case for the conjecture from Example 2
where the property Pev [g, x] can be rephrased as:

      PC [g, x] := ev(and(leq(x1 , g), and(leq(x2 , g), or(eq(g, x1 ), eq(g, x2 )))), x)        (7)

where again g has type S, x = (x1 , x2 ), and x1 and x2 have type Int. The procedure
in Figure 1 can be readily modified to apply to this formula, with PC [g, k] and g taking
the role respectively of Q[k, y] and y in that figure, since it generates solutions meeting
our syntactic requirements. Running this modified procedure instead the one in Figure 3
12       Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli, and Clark Barrett

 1. A := ∅ ; t′ := t ↓
 2. for i = 1, 2, . . .
     (a) (s, U ) := rcon(t′ , S, A);
     (b) if U is empty, return s; otherwise, for each datatype Dj occurring in U
              let di be the ith term in a fair enumeration of the elements of Dj
              let ti be the analogue of di in the background theory T
              add (ti ↓, ti , Dj ) to A

rcon(t, D, A)
   if (t, s, D) ∈ A, return (s, ∅); otherwise, do one of the following:
    (1) choose a f (t1 , . . . , tn ) s.t. f (t1 , . . . , tn ) ↓ = t and f has an analogue cD1 ...Dn D in D
        let (si , Ui ) = rcon(ti ↓, Di , A) for i = 1, . . . , n
        return (f (s1 , . . . , sn ), U1 ∪ . . . ∪ Un )
    (2) return (t, {(t, D)})

Fig. 5. A procedure for finding a term equivalent to t that meets the syntactic restrictions specified
by datatype S.

has the advantage that only the outputs of a solution need to be synthesized, not con-
ditions in ite-terms. However, in our experimental evaluation found that the overhead
of using an embedding into datatypes for syntax-guided problems is significant with
respect to the performance of the solver on problems with no syntactic restrictions. For
this reason, we advocate an approach for single-invocation synthesis conjectures with
syntactic restrictions that runs the procedure from Figure 1 as is, ignoring the syntactic
restrictions R, and subsequently reconstructs from its returned solution one satisfying
the restrictions. For that it is useful to assume that terms t in T can be effectively re-
duced to some (T -equivalent and unique) normal form, which we denote by t ↓.
    Say the procedure from Figure 1 returns a solution λx. t for a function f . To con-
struct from that a solution that meets the syntactic restrictions specified by datatype S,
we run the iterative procedure described in Figure 5. This procedure maintains an evolv-
ing set A of triples of the form (t, s, D), where D is a datatype, t is a term in normal
form, s is a term satisfying the restrictions specified by D. The procedure incrementally
makes calls to the subprocedure rcon, which takes a normal form term t, a datatype D
and the set A above, and returns a pair (s, U ) where s is a term equivalent to t in T , and
U is a set of pairs (s′ , D′ ) where s′ is a subterm of s that fails to satisfy the syntactic
restriction expressed by datatype D′ . Overall, the procedure alternates between calling
rcon and adding triples to A until rcon(t, D, A) returns a pair of the form (s, ∅), in
which case s is a solution satisfying the syntactic restrictions specified by S.

Example 3. Say we wish to construct a solution equivalent to λx1 x2 . x1 + (2 ∗ x2 ) that
meets restrictions specified by datatype S from Example 2. To do so, we let A = ∅,
and call rcon((x1 + (2 ∗ x2 )) ↓, S, A). Since A is empty and + is the analogue of
constructor plusSSS of S, assuming (x1 + (2 ∗ x2 )) ↓ = x1 + (2 ∗ x2 ), we may choose
to return a pair based on the result of calling rcon on x1 ↓ and (2 ∗ x2 ) ↓. Since xS1 is a
constructor of S and x1 ↓ = x1 , rcon(x1 , S, A) returns (x1 , ∅). Since S does not have a
constructor for ∗, we must either choose a term t such that t ↓ = (2 ∗ x2 ) ↓ where the
topmost symbol of t is the analogue of a constructor in S, or otherwise return the pair
(2 ∗ x2 , {(2 ∗ x2 , S)}). Suppose we do the latter, and thus rcon(x1 + (2 ∗ x2 ), S, A)
           On Counterexample Guided Quantifier Instantiation for Synthesis in CVC4          13

returns (x1 + (2 ∗ x2 ), {(2 ∗ x2 , S)}). Since the second component of this pair is not
empty, we pick in Step 2b the first element of S, x1 say, and add (x1 , x1 , S) to A.
We then call rcon((x1 + (2 ∗ x2 )) ↓, S, A) which by the same strategy above returns
(x1 + (2 ∗ x2 ), {(2 ∗ x2 , S)}). This process continues until we pick, the term plus(x2 , x2 )
say, whose analogue is x2 + x2 . Assuming (x2 + x2 ) ↓ = (2 ∗ x2 ) ↓, after adding the pair
(2∗x2 , x2 +x2 , S) to A, rcon((x1 +(2∗x2 )) ↓, S, A) returns the pair (x1 +(x2 +x2 ), ∅),
indicating that λx1 x2 . x1 + (x2 + x2 ) is equivalent to λx1 x2 . x1 + (2 ∗ x2 ), and meets
the restrictions specified by S.                                                            
    This procedure depends upon the use of normal forms for terms. It should be noted
that, since the top symbol of t is generally ite, this normalization includes both low-level
rewriting of literals within t, but also includes high-level rewriting techniques such as ite
simplification, redundant subterm elimination and destructive equality resolution. Also,
notice that we are not assuming that t ↓ = s ↓ if and only if t is equivalent to s, and thus
normal forms only underapproximate an equivalence relation between terms. Having a
(more) consistent normal form for terms allows us to compute a (tighter) underapproxi-
mation, thus improving the performance of the reconstruction. In this procedure, we use
the same normal form for terms that is used by the individual decision procedures of
CVC4. This is unproblematic for theories such as linear arithmetic whose normal form
for terms is a sorted list of monomials, but it can be problematic for theories such as
bitvectors. As a consequence, we use several optimizations, omitted in the description
of the procedure in Figure 5, to increase the likelihood that the procedure terminates
in a reasonable amount of time. For instance, in our implementation the return value
of rcon is not recomputed every time A is updated. Instead, we maintain an evolving
directed acyclic graph (dag), whose nodes are pairs (t, S) for term t and datatype S
(the terms we have yet to reconstruct), and whose edges are the direct subchildren of
that term. Datatype terms are enumerated for all datatypes in this dag, which is incre-
mentally pruned as pairs are added to A until it becomes empty. Another optimization
is that the procedure rcon may choose to try simultaneously to reconstruct multiple
terms of the form f (t1 , . . . , tn ) when matching a term t to a syntactic specification S,
reconstructing t when any such term can be reconstructed.
    Although the overhead of this procedure can be significant when large subterms
do not meet the syntactic restrictions, we found that in practice it quickly terminates
successfully for a majority of the solutions we considered where reconstruction was
possible, as we discuss in the next section. Furthermore, it makes our implementation
more robust, since it effectively treats in the same way different properties that are equal
modulo normalization (which is parametric in the built-in theories we consider).


6 Experimental Evaluation
We implemented the techniques from the previous sections in the SMT solver CVC4 [4],
which has support for quantified formulas and a wide range of theories including arith-
metic, bitvectors, and algebraic datatypes. We evaluated our implementation on 243
benchmarks used in the SyGuS 2014 competition [1] that were publicly available on
the StarExec execution service [30]. The benchmarks are in a new format for speci-
fying syntax-guided synthesis problems [22]. We added parsing support to CVC4 for
14        Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli, and Clark Barrett

                   array (32) bv (7)     hd (56)      icfp (50)    int (15)     let (8) multf (8) Total (176)
                    #    time # time #        time #        time #       time # time # time #             time
        esolver     4 2250.7 2 71.2 50 878.5 0                  0 5 1416.7 2 0.0 7            0.6 70 4617.7
        cvc4+sg     1      3.1 0     0 34 4308.9 1            0.5 3        1.7 2 0.5 7 628.3 48          4943
        cvc4+si-r (32)     1.2 (6) 4.7 (56)     2.1 (43) 3403.5 (15)       0.6 (8) 1.0 (8) 0.2 (168) 3413.3
        cvc4+si    30 1449.5 5 0.1 52 2322.9 0                  0 6        0.1 2 0.5 7        0.1 102 3773.2

Fig. 6. Results for single-invocation synthesis conjectures, showing times (in seconds) and num-
ber of benchmarks solved by each solver and configuration over 8 benchmark classes with a
3600s timeout. The number of benchmarks solved by configuration cvc4+si-r are in parentheses
because its solutions do not necessarily satisfy the given syntactic restrictions.
most features of this format. All SyGuS benchmarks considered contain synthesis con-
jectures whose background theory is either linear integer arithmetic or bitvectors. We
made some minor modifications to benchmarks to avoid naming conflicts, and to ex-
plicitly define several bitvector operators that are not supported natively by CVC4.
    We considered multiple configurations of CVC4 corresponding to the techniques
mentioned in this paper. Configuration cvc4+sg executes the syntax-guided procedure
from Section 4, even in cases where the synthesis conjecture is single-invocation. Con-
figuration cvc4+si-r executes the procedure from Section 3 on all benchmarks having
conjectures that it can deduce are single-invocation. In total, it discovered that 176 of
the 243 benchmarks could be rewritten into a form that was single-invocation. This
configuration simply ignores any syntax restrictions on the expected solution. Finally,
configuration cvc4+si uses the same procedure used by cvc4+si-r but then attempts to
reconstruct any found solution as a term in required syntax, as described in Section 5.
    We ran all configurations on all benchmarks on the StarExec cluster.7 We pro-
vide comparative results here primarily against the enumerative CEGIS solver ES-
OLVER [31], the winner of the SyGuS 2014 competition. In our tests, we found that
ES OLVER performed significantly better than the other entrants of that competition.
Benchmarks with single-invocation synthesis conjectures. The results for bench-
marks with single-invocation properties are shown in Figure 6. Configuration cvc4+si-r
found a solution (although not necessarily in the required language) very quickly for a
majority of benchmarks. It terminated successfully for 168 of 176 benchmarks, and in
less than a second for 159 of those. Not all solutions found using this method met the
syntactic restrictions. Nevertheless, our methods for reconstructing these solutions into
the required grammar, implemented in configuration cvc4+si, succeeded in 102 cases,
or 61% of the total. This is 32 more benchmarks than the 70 solved by ES OLVER, the
best known solver for these benchmarks so far. In total, cvc4+si solved 34 benchmarks
that ES OLVER did not, while ES OLVER solved 2 that cvc4+si did not.
    The solutions returned by cvc4+si-r were often large, having an order of 10K sub-
terms for harder benchmarks. However, after exhaustively applying simplification tech-
niques during reconstruction with configuration cvc4+si, we found that the size of those
solutions is comparable to other solvers, and in some cases even smaller. For instance,
among the 68 benchmarks solved by both ES OLVER and cvc4+si, the former produced
a smaller solution in 15 cases and the latter in 9. Only in 2 cases did cvc4+si produce
a solution that had 10 more subterms than the solution produced by ES OLVER. This
indicates that in addition to having a high precision, the techniques from Section 5 used
 7
     A detailed summary can be found at http://lara.epfl.ch/w/cvc4-synthesis.
             On Counterexample Guided Quantifier Instantiation for Synthesis in CVC4              15

                                  int (3) invgu (28) invg (28) vctrl (8) Total (67)
                                 # time # time # time # time # time
                         esolver 3 1.6 25 86.3 25 85.6 5 29.5 58 203.0
                         cvc4+sg 3 1476.0 23 811.6 22 2283.2 5 2933.1 53 7503.9

Fig. 7. Results for synthesis conjectures that are not single-invocation, showing times (in seconds)
and numbers of benchmarks solved by CVC4 and ES OLVER over 4 benchmark classes with a
3600s timeout.
for solution reconstruction are effective also at producing succinct solutions for this
benchmark library.
    Configuration cvc4+sg does not take advantage of the fact that a synthesis conjec-
ture is single-invocation. However, it was able to solve 48 of these benchmarks, includ-
ing a small number not solved by any other configuration, like one from the icfp class
whose solution was a single argument function over bitvectors that shifted its input right
by four bits. In addition to being solution complete, cvc4+sg always produces solutions
of minimal term size, something not guaranteed by the other solvers and CVC4 con-
figurations. Of the 47 benchmarks solved by both cvc4+sg and ES OLVER, the solution
returned by cvc4+sg was smaller than the one returned by ES OLVER in 6 cases, and had
the same size in the others. This provides an experimental confirmation that the fairness
techniques for term size described in Section 4 ensure minimal size solutions.
Benchmarks with non-single-invocation synthesis conjectures. Configuration
cvc4+sg is the only CVC4 configuration that can process benchmarks with synthesis
conjectures that are not single-invocation. The results for ES OLVER and cvc4+sg on
such benchmarks from SyGuS 2014 are shown in Figure 7. Configuration cvc4+sg
solved 53 of them over a total of 67. ES OLVER solved 58 and additionally reported
that 6 had no solution. In more detail, ES OLVER solved 7 benchmarks that cvc4+sg did
not, while cvc4+sg solved 2 benchmarks (from the vctrl class) that ES OLVER could
not solve. In terms of precision, cvc4+sg is quite competitive with the state of the art
on these benchmarks. To give other points of comparison, at the SyGuS 2014 compe-
tition [1] the second best solver (the Stochastic solver) solved 40 of these benchmarks
within a one hour limit and Sketch solved 23.
Overall results. In total, over the entire SyGuS 2014 benchmark set, 155 benchmarks
can be solved by a configuration of CVC4 that, whenever possible, runs the methods
for single-invocation properties described in Section 3, and otherwise runs the method
described in Section 4. This number is 27 higher than the 128 benchmarks solved in
total by ES OLVER. Running both configuration cvc4+sg and cvc4+si in parallel8 solves
156 benchmarks, indicating that CVC4 is highly competitive with state-of-the-art tools
for syntax guided synthesis. CVC4’s performance is noticeably better than ES OLVER on
single-invocation properties, where our new quantifier instantiation techniques give it a
distinct advantage.
Competitive advantage on single-invocation properties in the presence of ite. We
conclude by observing that for certain classes of benchmarks, configuration cvc4+si
scales significantly better than state-of-the-art synthesis tools. Figure 8 shows this in
comparison with ES OLVER for the problem of synthesizing a function that computes
 8
     CVC 4 has a portfolio mode that allows it to run multiple configurations at the same time.
16         Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli, and Clark Barrett

                              n      2     3      4    5 6 7 8 9 10
                           esolver 0.01 1377.10 –      – – – – – –
                           cvc4+si 0.01    0.02 0.03 0.05 0.1 0.3 1.6 8.9 81.5

Fig. 8. Results for parametric benchmarks class encoding the maximum of n integers. The
columns show the run time for ES OLVER and CVC4 with a 3600s timeout.
the maximum of n integer inputs. As reported by Alur et al. [1], no solver in the SyGuS
2014 competition was able to synthesize such a function for n = 5 within one hour.
    For benchmarks from the array class, whose solutions are loop-free programs that
compute the first instance of an element in a sorted array, the best reported solver for
these in [1] was Sketch, which solved a problem for an array of length 7 in approx-
imately 30 minutes.9 In contrast, cvc4+si was able to reconstruct solutions for arrays
of size 15 (the largest benchmark in the class) in 0.3 seconds, and solved each of the
benchmarks in the class but 8 within 1 second.


7 Conclusion
We have shown that SMT solvers, instead of just acting as subroutines for automated
software synthesis tasks, can be instrumented to perform synthesis themselves. We have
presented a few approaches for enabling SMT solvers to construct solutions for the
broad class of syntax-guided synthesis problems and discussed their implementation in
CVC4. This is, to the best of our knowledge, the first implementation of synthesis inside
an SMT solver and it already shows considerable promise. Using a novel quantifier
instantiation technique and a solution enumeration technique for the theory of algebraic
datatypes, our implementation is competitive with the state of the art represented by the
systems that participated in the 2014 syntax-guided synthesis competition. Moreover,
for the important class of single-invocation problems when syntax restrictions permit
the if-then-else operator, our implementation significantly outperforms those systems.
Acknowledgments. We would like to thank Liana Hadarean for helpful discussions on
the normal form used in CVC4 for bit vector terms.


References
 1. R. Alur, R. Bodik, E. Dallal, D. Fisman, P. Garg, G. Juniwal, H. Kress-Gazit, P. Madhusudan,
    M. M. K. Martin, M. Raghothaman, S. Saha, S. A. Seshia, R. Singh, A. Solar-Lezama, E. Tor-
    lak, and A. Udupa. Syntax-guided synthesis. To Appear in Marktoberdrof NATO proceed-
    ings, 2014. http://sygus.seas.upenn.edu/files/sygus_extended.pdf,
    retrieved 2015-02-06.
 2. R. Alur, R. Bodı́k, G. Juniwal, M. M. K. Martin, M. Raghothaman, S. A. Seshia, R. Singh,
    A. Solar-Lezama, E. Torlak, and A. Udupa. Syntax-guided synthesis. In FMCAD, pages
    1–17. IEEE, 2013.
 3. R. Alur, M. M. K. Martin, M. Raghothaman, C. Stergiou, S. Tripakis, and A. Udupa. Syn-
    thesizing finite-state protocols from scenarios and requirements. In E. Yahav, editor, Haifa
    Verification Conference, volume 8855 of LNCS, pages 75–91. Springer, 2014.
 9
      These benchmarks, as contributed to the SyGuS benchmark set, use integer variables only;
     they were generated by expanding fixed-size arrays and contain no operations on arrays.
            On Counterexample Guided Quantifier Instantiation for Synthesis in CVC4                17

 4. C. Barrett, C. Conway, M. Deters, L. Hadarean, D. Jovanovic, T. King, A. Reynolds, and
    C. Tinelli. CVC4. In Proceedings of CAV’11, volume 6806 of LNCS, pages 171–177.
    Springer, 2011.
 5. C. Barrett, M. Deters, L. M. de Moura, A. Oliveras, and A. Stump. 6 years of SMT-COMP.
    JAR, 50(3):243–277, 2013.
 6. C. Barrett, I. Shikanian, and C. Tinelli. An abstract decision procedure for satisfiability in the
    theory of inductive data types. Journal on Satisfiability, Boolean Modeling and Computation,
    3:21–46, 2007.
 7. N. Bjørner. Linear quantifier elimination as an abstract decision procedure. In J. Giesl and
    R. Hähnle, editors, IJCAR, volume 6173 of LNCS, pages 316–330. Springer, 2010.
 8. P. Cousot. Proving program invariance and termination by parametric abstraction, lagrangian
    relaxation and semidefinite programming. In R. Cousot, editor, VMCAI, volume 3385 of
    LNCS, pages 1–24. Springer, 2005.
 9. L. M. de Moura and N. Bjørner. Efficient e-matching for SMT solvers. In F. Pfenning, editor,
    CADE, volume 4603 of LNCS, pages 183–198. Springer, 2007.
10. D. Detlefs, G. Nelson, and J. B. Saxe. Simplify: A theorem prover for program checking.
    Technical report, J. ACM, 2003.
11. Y. Ge and L. de Moura. Complete instantiation for quantified formulas in satisfiability mod-
    ulo theories. In Proceedings of CAV’09, volume 5643 of LNCS, pages 306–320. Springer,
    2009.
12. C. C. Green. Application of theorem proving to problem solving. In D. E. Walker and L. M.
    Norton, editors, IJCAI, pages 219–240. William Kaufmann, 1969.
13. S. Jacobs and V. Kuncak. Towards complete reasoning about axiomatic specifications. In
    Verification, Model Checking, And Abstract Interpretation, pages 278–293. Springer Berlin
    Heidelberg, 2011.
14. S. Jha, S. Gulwani, S. A. Seshia, and A. Tiwari. Oracle-guided component-based program
    synthesis. In J. Kramer, J. Bishop, P. T. Devanbu, and S. Uchitel, editors, ICSE, pages 215–
    224. ACM, 2010.
15. E. Kneuss, I. Kuraj, V. Kuncak, and P. Suter. Synthesis modulo recursive functions. In A. L.
    Hosking, P. T. Eugster, and C. V. Lopes, editors, OOPSLA, pages 407–426. ACM, 2013.
16. V. Kuncak, M. Mayer, R. Piskac, and P. Suter. Complete functional synthesis. In B. G. Zorn
    and A. Aiken, editors, PLDI, pages 316–329. ACM, 2010.
17. V. Kuncak, M. Mayer, R. Piskac, and P. Suter. Software synthesis procedures. CACM,
    55(2):103–111, 2012.
18. V. Kuncak, M. Mayer, R. Piskac, and P. Suter. Functional synthesis for linear arithmetic and
    sets. STTT, 15(5-6):455–474, 2013.
19. R. Madhavan and V. Kuncak. Symbolic resource bound inference for functional programs.
    In A. Biere and R. Bloem, editors, CAV, volume 8559 of LNCS, pages 762–778. Springer,
    2014.
20. Z. Manna and R. J. Waldinger. A deductive approach to program synthesis. TOPLAS,
    2(1):90–121, 1980.
21. D. Monniaux. Quantifier elimination by lazy model enumeration. In T. Touili, B. Cook, and
    P. Jackson, editors, CAV, volume 6174 of LNCS, pages 585–599. Springer, 2010.
22. M. Raghothaman and A. Udupa. Language to specify syntax-guided synthesis problems.
    CoRR, abs/1405.5590, 2014.
23. A. Reynolds, C. Tinelli, A. Goel, S. Krstić, M. Deters, and C. Barrett. Quantifier instantiation
    techniques for finite model finding in SMT. In M. P. Bonacina, editor, Proceedings of the
    24th International Conference on Automated Deduction (Lake Placid, NY, USA), volume
    7898 of Lecture Notes in Computer Science, pages 377–391. Springer, 2013.
24. A. Reynolds, C. Tinelli, and L. D. Moura. Finding conflicting instances of quantified formu-
    las in SMT. In Formal Methods in Computer-Aided Design (FMCAD), 2014.
18       Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli, and Clark Barrett

25. A. J. Reynolds. Finite Model Finding in Satisfiability Modulo Theories. PhD thesis, The
    University of Iowa, 2013.
26. L. Ryzhyk, A. Walker, J. Keys, A. Legg, A. Raghunath, M. Stumm, and M. Vij. User-guided
    device driver synthesis. In J. Flinn and H. Levy, editors, OSDI, pages 661–676. USENIX
    Association, 2014.
27. A. Solar-Lezama. Program sketching. STTT, 15(5-6):475–495, 2013.
28. A. Solar-Lezama, L. Tancau, R. Bodı́k, S. A. Seshia, and V. A. Saraswat. Combinatorial
    sketching for finite programs. In J. P. Shen and M. Martonosi, editors, ASPLOS, pages 404–
    415. ACM, 2006.
29. S. Srivastava, S. Gulwani, and J. S. Foster. Template-based program verification and program
    synthesis. STTT, 15(5-6):497–518, 2013.
30. A. Stump, G. Sutcliffe, and C. Tinelli. Starexec: a cross-community infrastructure for logic
    solving. In Proceedings of the 7th International Joint Conference on Automated Reasoning,
    Lecture Notes in Artificial Intelligence. Springer-Verlag, 2014.
31. A. Udupa, A. Raghavan, J. V. Deshmukh, S. Mador-Haim, M. M. Martin, and R. Alur. Tran-
    sit: Specifying protocols with concolic snippets. In PLDI, pages 287–296. ACM, 2013.
