                                                  Higher-Order Constrained Horn Clauses and Refinement Types
                                                            Toby Cathcart Burn               C.-H. Luke Ong                Steven J. Ramsay
                                                             University of Oxford           University of Oxford          University of Oxford




                                                 Motivated by applications in automated veriﬁcation of higher-order functional programs, we develop a notion
                                              of constrained Horn clauses in higher-order logic and a decision problem concerning their satisﬁability. We show
                                              that, although satisﬁable systems of higher-order clauses do not generally have least models, there is a notion
                                              of canonical model obtained through a reduction to a problem concerning a kind of monotone logic program.
                                              Following work in higher-order program veriﬁcation, we develop a reﬁnement type system in order to reason
                                              about and automate the search for models. This provides a sound but incomplete method for solving the decision
                                              problem. Finally, we show that there is a sense in which we can use reﬁnement types to express properties of
                                              terms whilst staying within the higher-order constrained Horn clause framework.
arXiv:1705.06216v2 [cs.PL] 1 Aug 2017




                                        1 Introduction
                                        There is evidence to suggest that many ﬁrst-order program veriﬁcation problems can be framed as solvability
                                        problems for systems of constrained Horn clauses (Beyene et al., 2013; Bjørner et al., 2013b, 2015), which are Horn
                                        clauses of ﬁrst-order logic containing constraints expressed in some suitable background theory. This makes the
                                        study of these systems particularly worthwhile since they provide a purely logical basis on which to develop tech-
                                        niques for ﬁrst-order program veriﬁcation. For example, results on the development of highly eﬃcient constrained
                                        Horn clause solvers (Grebenshchikov et al., 2012; Hoder et al., 2011; Gurﬁnkel et al., 2015) can be exploited by a
                                        large number of program veriﬁcation tools, each of which oﬄoads some complex task (invariant ﬁnding is a typical
                                        example) to a solver by framing it in terms of constrained Horn clauses.
                                           This paper concerns automated veriﬁcation of higher-order, functional programs. Whilst there are approaches
                                        to the veriﬁcation of functional programs in which constrained Horn clause solving plays an important role,
                                        there is inevitably a mismatch between the higher-order nature of the program and the ﬁrst-order logic in which
                                        the Horn clauses are expressed, and this must be addressed in some intelligent way by the program veriﬁer. For
                                        example, in recent work on reﬁnement types (Rondon et al., 2008; Vazou et al., 2015; Unno et al., 2013), a type
                                        system is used to reduce the problem of ﬁnding an invariant for the higher-order program, to ﬁnding a number of
                                        ﬁrst-order invariants of the ground-type data at certain program points. This latter problem can often be expressed
                                        as a system of constrained Horn clauses. When that system is solvable, the ﬁrst-order invariants obtained can be
                                        composed in the type system to yield a higher-order invariant for the program (expressed as a type assignment).
                                           In this paper we introduce higher-order constrained Horn clauses, a natural extension of the notion of constrained
                                        Horn clause to higher-order logic, and examine certain aspects that we believe are especially relevant to appli-
                                        cations in higher-order program veriﬁcation, namely: the existence of canonical solutions, the applicability of
                                        existing techniques to automated solving and the expressibility of program properties of higher type.
                                           Let us elaborate on these goals and illustrate our motivation more concretely by discussing a particular example.
                                        Consider the following higher-order program:

                                                                      let add x y = x + y
                                                                      let rec iter f s n = if n ≤ 0 then s else f n (iter f s (n − 1))
                                                                      in λn. assert (n ≤ iter add 0 n)

                                        The term iter add 0 n occurring in the last line of the program is the sum of the integers from 1 to n in case n is
                                        non-negative and is 0 otherwise. Let us say that the program is safe just in case the assertion is never violated, i.e.
                                        the summation is not smaller than n.
                                          To verify safety, we must ﬁnd an invariant that implies the required property. For our purposes, an invariant
                                        will be an over-approximation of the input-output graphs of the functions deﬁned in the program. If we can ﬁnd
                                        an over-approximation of the graph of the function iter add 0 which does not contain any pair (n, m) with n > m,
                                        then we can be certain that the guard on the assertion is never violated. Hence, we seek a set of pairs of natural
                                        numbers relating n to m at least whenever iter add 0 n evaluates to m and which has no intersection with >.



                                                                                                     1
  The idea is to express the problem of ﬁnding such a program invariant logically, as a satisﬁability problem for
the following set of higher-order constrained Horn clauses:

                                ∀xyz. z = x + y ⇒ Add x y z
                                ∀f snm. n ≤ 0 ∧ m = s ⇒ Iter f s n m            
                                ∀f snm. n > 0 ∧ ∃p. Iter f s (n − 1) p ∧ f n p m ⇒ Iter f s n m
                                ∀nm. Iter Add 0 n m ⇒ n ≤ m

The clauses constrain the variables Add : int → int → int → o and Iter : (int → int → int → o) → int →
int → int → o with respect to the theory of integer linear arithmetic, so a model is just an assignment of
particular relations1 to these variables that satisﬁes the formulas. The ﬁrst clause constrains Add to be an over-
approximation of the graph of the addition function add: whenever z = x + y, we at least know that x, y and z
are related by Add. The second and third constrain Iter to be an over-approximation of the graph of the iteration
combinator iter. Observe that the two branches of the conditional in the program appear as two clauses, expressing
over-approximations in which the third input n is at most or greater than 0 respectively. The ﬁnal clause ensures
that, taken together, these over-approximations are yet precise enough that they exclude the possibility of relating
an input n of iter add 0 to a smaller output m. In other words, a model of these formulas is an invariant, in the
sense we have described above, and thus constitutes a witness to the safety of the program.
   Notice that what we are describing in this example is a compositional approach, in which an over-approximation
Iter Add 0 : int → int → o to the graph of the function iter add 0 : int → int is constructed from over-
approximations Add and Iter of the graphs of the functions add and iter. Consequently, where iter was a higher-
order function, Iter is a higher-order relation taking a ternary relation on integers as input, and the quantiﬁcation
∀f is over all such ternary relations f . However, for the purposes of this paper, the details of how one obtains a
system of higher-order constrained Horn clauses are not actually relevant, since we here study properties of such
systems independently of how they arise.

Existence of canonical solutions. A set of higher-order constrained Horn clauses may have many models or none
(consider that there are many invariants that can prove a safety property or none in case it is unprovable). One
model of the above set of clauses is the following assignment of relations (expressed in higher-order logic):

         Add 7→ λx y z. z = x + y              Iter 7→ λ f s n m. (∀x y z. f x y z ⇒ 0 < x ⇒ y < z) ∧ 0 ≤ s ⇒ n ≤ m

Notice that this represents quite a large model (a coarse invariant). For example, under this assignment the relation
described by Iter Add (−1) relates every pair of integers n and m. In the case of ﬁrst-order constrained Horn clauses
over the theory of integer linear arithmetic, if a set of clauses has a model, then it has a least model2 , and this least
model property is at the heart of many of the applications of Horn clauses in practice. If we consider the use of
constrained Horn clauses in veriﬁcation, a key component of the design of many successful algorithms for solving
systems of clauses (and program invariant ﬁnding more generally) is the notion of approximation or abstraction.
However, to speak of approximation presupposes there is something to approximate. For program veriﬁers there
is, for example, the set of reachable states or the set of traces of the program, and for ﬁrst-order constrained Horn
clause solvers there is the least model.
    In contrast, in Section 4 we show that satisﬁable systems of higher-order constrained Horn clauses do not
necessarily have least models. The problem, which has also been observed for pure (without constraint theory)
higher-order Horn clauses by Charalambidis et al. (2013), can be attributed to the use of unrestricted quantiﬁcation
over relations. By restricting the semantics, so that interpretations range only over monotone relations (monotone
propositional functions), we ensure that systems do have least solutions, but at the cost of abandoning the standard
(semantics of) higher-order logic. The monotone semantics is natural but, for the purpose of specifying constraint
systems, it can be unintuitive. For example, consider the formula ∀x . (∃yz. x y ∧ y z) ⇒ P x which constrains
P : ((int → o) → o) → o so that it is at least true of all non-empty sets of non-empty sets of integers 3 . In the
monotone semantics, this formula is guaranteed to have a least model, but inside that model P is not true of the
set {{0}}.

 1 Throughout this paper we will speak of relations but work with their characteristic functions, which are propositional (Boolean-valued)

   functions, using o for the sort of propositions.
 2 In general, one can say that for each model of the background theory, a satisﬁable set of clauses has a least satisfying valuation.
 3 Viewing relations of sort int → o as sets of integers.




                                                                       2
   Ideally, we would like to be able to specify constraint systems using the standard semantics of higher-order logic,
but solve (build solvers for) systems in the monotone semantics. In fact, we show that this is possible: we construct
a pair of adjoint mappings with which the solutions to the former can be mapped to solutions of the latter and
vice versa. This allows us to reduce the problem of solving an system of constraints in the standard semantics to
the problem of solving a system in the monotone semantics. Monotonicity and the fact that satisﬁable monotone
systems have canonical solutions are key to the rest of the work in the paper.

Applicability of existing techniques to automated solving. Many of the techniques developed originally for the
automation of ﬁrst-order program veriﬁcation transfer well to ﬁrst-order constrained Horn clause solving. Hence,
to construct automated solvers for systems of higher-order clauses, we look to existing work on higher-order
program veriﬁcation. In automated veriﬁcation for functional programs, one of the most successful techniques of
recent years has been based on reﬁnement type inference (Rondon et al., 2008; Kobayashi et al., 2011; Vazou et al.,
2015; Zhu and Jagannathan, 2013). The power of the approach comes from its ability to lift rich ﬁrst-order theories
over data to higher types using subtyping and the dependent product.
   In Section 5, we develop a reﬁnement type system for higher-order constrained Horn clauses, in which types
are assigned to the free relation variables that are being solved for. The idea is that a valid type assignment is a
syntactic representation of a model. For example, the model discussed previously can be represented by the type
assignment ΓI :

         Add: x:int → y:int → z:int → ohz = x + yi
         Iter: (x:int → y:int → z:int → oh0 < x ⇒ y < zi) → s:int → n:int → m:int → oh0 ≤ s ⇒ n ≤ mi

The correspondence hinges on the deﬁnition of reﬁnements ohφi of the propositional sort o, which are parametrised
by a ﬁrst-order constraint formula φ describing an upper bound on the truth of any inhabitant. The dependent
product and integer types are interpreted standardly, so that the ﬁrst type above can be read as the set of all ternary
relations on integers x, y and z that are false whenever z is not x + y.
   The system is designed so that its soundness allows one to conclude that a given ﬁrst-order constraint formula
can be used to approximate a given higher-order formula4 . Given a formula G, from the derivability of the judge-
ment Γ ⊢ G : ohφi it follows that G ⇒ φ in those interpretations of the relational variables that satisfy Γ. For
example, the judgement
                                    ΓI , n: int, m: int ⊢ Iter Add 0 n m : ohn ≤ mi
is derivable, from which we may conclude that n ≤ m is a sound abstraction of Iter Add 0 n m in any interpretation
of Iter and Add that satisﬁes ΓI . This is a powerful assertion for automated reasoning because the formula φ in
reﬁnement type ohφi is a simple ﬁrst-order constraint formula (typically belonging to a decidable theory) whereas
the formula G in the subject is a complicated higher-order formula, possibly containing relational variables whose
meanings are a function of the whole system. By adapting machinery developed for reﬁnement type inference
of functional programs, we obtain a sound (but incomplete) procedure for solving systems of higher-order con-
strained Horn clauses. An implementation shows the method to be feasible.

Expressibility of program properties of higher type. We say that a property is of higher type if it is a property
of a higher-order function. It is possible to do whole-program veriﬁcation in a higher-order setting using only
properties of ﬁrst-order type, because a complete program typically has a ﬁrst-order type like int → int. However,
it is also natural to want to specify properties of higher types, for example properties of higher-order functions
of type (int → int) → int. Even when the ultimate goal is one of whole-program veriﬁcation, being able to verify
properties of higher types is advantageous because it can allow a large analysis to be broken down into smaller
components according to the structure of the program.
   However, the kinds of higher-type properties expressible by higher-order constrained Horn clauses is not im-
mediately clear. Therefore, we conclude Section 5 by showing that it is possible to state at least those properties
that can be deﬁned using reﬁnement types, since their complements are expressible using goal terms.
   The rest of the paper is structured as follows. In Section 2 we ﬁx our presentation of higher-order logic and the
notion of higher-order constrained Horn clause is made precise in Section 3 along with the associated deﬁnition
of solvability. Section 4 introduces monotone logic programs, which are better suited to automated reasoning, and

 4 Technically, the subjects of the type system are not all higher-order formulas but only the so-called goal formulas.




                                                                       3
shows that solvability of higher-order constrained Horn clause problems can be reduced to solvability of these
programs. This class of logic programs forms the basis for the reﬁnement type system deﬁned in Section 5, which
yields a sound but incomplete method for showing solvability through type inference. An implementation of the
method is also discussed in this section, which concludes by discussing the deﬁnability of higher-type properties
deﬁned by reﬁnement types. Finally, in Section 6, we discuss related work and draw conclusions in Section 7. Full
proofs are included in the appendices.

2 Higher-order logic
We will work in a presentation of higher-order logic as a typed lambda calculus.

Sorts. Given a sort ι of individuals (for example int), and a sort o of propositions, the general sorts are just the
simple types that can be built using the arrow: σ F ι | o | σ1 → σ2 . The order of a sort σ , written order(σ ), is
deﬁned as follows:

                  order(ι) = 1   order(o) = 1       order(σ1 → σ2 ) = max(order(σ1 ) + 1, order(σ2 ))

Note: we follow the convention from logic of regarding base sorts to be of order 1. Consequently, we will consider,
for example, an int variable to be of order 1 and an (int → o) → int function to be of order 3.

Terms. The terms that we consider are just terms of an applied lambda calculus. We will write variables generally
using x, y, z, or X , Y , Z when we want to emphasise that they are of higher-order sorts.

                                          M, N      F     x | c | M N | λx:σ . M

in which c is a constant. We assume that application associates to the left and the scope of the abstraction extends
as far to the right as possible. We identify terms up to α-equivalence.

Sorting A sort environment, typically ∆, is a ﬁnite sequence of pairs x : σ , all of whose subjects are required to be
distinct. We assume, for each constant c, a given sort assignment σc . Then sorting rules for terms are, as standard,
associated with the judgement ∆ ⊢ s : σ deﬁned by:


                             (SCst)                              (SVar)
                                       ∆ ⊢ c : σc                         ∆1 , x : σ , ∆2 ⊢ x : σ
                     ∆ ⊢ s : σ1 → σ2         ∆ ⊢ t : σ1                                ∆, x : σ1 ⊢ s : σ2
           (SApp)                                                          (SAbs)                          x < dom(∆)
                                ∆ ⊢ s t : σ2                                          ∆ ⊢ λx . s : σ1 → σ2

  Given a sorted term ∆ ⊢ M : σ , we say that a variable occurrence x in M is of order k just if the unique
subderivation ∆ ′ ⊢ x : σ ′ rooted at this occurrence has σ ′ of order k. We say that a sorted term ∆ ⊢ M : σ is of
order k just if k is the largest order of any of the variables occurring in M.

Formulas. Given a ﬁrst-order signature Σ specifying a collection of base sorts and sorted constants, we can
consider higher-type formulas over Σ, by considering terms whose constant symbols are either drawn from the
signature Σ or are a member of the following set LSym of logical constant symbols:

                          true, false : o                                  ¬ : o →o
                            ∧, ∨, ⇒ : o → o → o                      ∀σ , ∃σ : (σ → o) → o

As usual, we write ∃σ (λx:σ . M) more compactly as ∃x:σ . M and deﬁne the set of formulas to be just the well-sorted
terms of sort o. In the context of formulas, it is worthwhile to recognise the subset of relational sorts, typically ρ,
which have the sort o in tail position and whose higher-order subsorts are also relational. Formally:

                                                 ρFo|ι→ρ |ρ→ρ

Since formulas are just terms, the notion of order carries over without modiﬁcation.



                                                             4
Interpretation. Let A be a Σ-structure. In particular, we assume that A assigns a non-empty set Aι to each of the
base sorts ι ∈ B and to the sort o is assigned the distinguished lattice 2 = {0 ≤ 1}. We deﬁne the full sort frame
over A by induction on the sort:

                        Snιo ≔ Aι                 Snoo ≔ 2                   Snσ1 → σ2 o ≔ Snσ1 o ⇒ Snσ2 o

where X ⇒ Y is the full set-theoretic function space between sets X and Y . The lattice 2 supports the following
functions:
                  or(b1 )(b2 )   =     max{b1 , b2 }                              not(b) =         1−b
                and(b1 )(b2 )    =     min{b1 , b2 }                      implies(b1 )(b2 ) =      or(not(b1 ))(b2 )
                 existsσ (f )    =     max{ f (v) | v ∈ nσ o}                 forallσ (f ) =       not(existsσ (not ◦ f ))

We extend the order on 2 to order the set Snρo of all relations of a given sort ρ pointwise, deﬁning the order ⊆ρ
inductively on the structure of ρ:
    • For all b1 , b2 ∈ Snoo: if b1 ≤ b2 then b1 ⊆o b2
    • For all r 1 , r 2 ∈ Snι → ρo: if, for all n ∈ Snιo, r 1 (n) ⊆ρ r 2 (n), then r 1 ⊆ι→ρ r 2 .
    • For all r 1 , r 2 ∈ Snρ 1 → ρ 2 o: if, for all s ∈ Snρ 1 o, r 1 (s) ⊆ρ 2 r 2 (s), then r 1 ⊆ρ 1 →ρ 2 r 2 .
This ordering determines a complete lattice structure on each Snρo, we will denote the (pointwise) join and meet
    Ð       Ñ
by ρ and ρ respectively. To aid readability, we will typically omit subscripts.
   We interpret a sort environment ∆ by the indexed product: Sn∆o ≔ Πx ∈ dom(∆).Sn∆(x)o, that is, the set of
all functions on dom(∆) that map x to an element of Sn∆(x)o; these functions, typically α, are called valuations.
We similarly order Sn∆o pointwise, with f 1 ⊆∆ f 2 just if, for all x : ρ ∈ ∆, f 1 (x) ⊆ρ f 2 (x); thus determining a
complete lattice structure.
   For the purpose of interpreting formulas, we extend the structure A to interpret the symbols from LSym ac-
cording to the functions given above. The interpretation of a term ∆ ⊢ M : σ is a function Sn∆ ⊢ M : σ o (we leave
A implicit) that belongs to the set Sn∆o ⇒ Snσ o, and which is deﬁned by the following equations.

                                  Sn∆ ⊢ x : σ o(α)            = α(x)
                                  Sn∆ ⊢ c : σ o(α)            = cA                                         
                             Sn∆ ⊢ M N : σ2 o(α)              = Sn∆ ⊢ M : σ1 → σ2 o(α) Sn∆ ⊢ N : σ1 o(α)
                  Sn∆ ⊢ λx : σ1 . M : σ1 → σ2 o(α)            = λv ∈ Snσ1 o. Sn∆, x : σ1 ⊢ M : σ2 o(α[x 7→ v])

Satisfaction For a Σ-structure A, a formula ∆ ⊢ M : o and a valuation α ∈ Sn∆o, we say that hA, αi satisﬁes M
and write A, α  M just if Sn∆ ⊢ M : oo(α) = 1. We deﬁne entailment M  N between two formulas M and N in
terms of satisfaction as usual.

3 Higher-order constrained Horn clauses
We introduce a notion of constrained Horn clauses in higher-order logic.

Constraint language. Assume a ﬁxed, ﬁrst-order language over a ﬁrst-order signature Σ, consisting of: distin-
guished subsets of ﬁrst-order terms Tm and ﬁrst-order formulas (φ ∈) Fm, and a ﬁrst-order theory Th in which to
interpret those formulas. We refer to this ﬁrst-order language as the constraint language, and Th as the background
theory.

Atoms and constraints. An atom is an applicative formula of shape X M1 · · · Mk in which X is a relational variable
and each Mi is a term. A constraint, φ, is just a formula from the constraint language. For technical convenience,
we assume that atoms do not contain any constants (including logical constants), and constraints do not contain
any relational variables.




                                                                      5
Constrained Horn clauses. Fix a sorting ∆ of relational variables. The constrained goal formulas over ∆, typically
G, and the constrained deﬁnite formulas over ∆, typically D, are the subset of all formulas deﬁned by induction:

                                           G    F     M | φ | G ∧ G | G ∨ G | ∃x:σ . G
                                           D    F     true | ∀x:σ . D | D ∧ D | G ⇒ X x

in which σ is either the sort of individuals ι or a relational sort ρ, M is an atom5 , φ a constraint and, in the
last alternative, X is required to be a relational symbol inside dom(∆) and x = x 1 · · · x n a sequence of pairwise
distinct variables. It will often be convenient to view a constrained deﬁnite formula equivalently as a conjunction
of (constrained) deﬁnite clauses, which are those deﬁnite formulas with shape: ∀x . G ⇒ X x.
Remark 1. Our class of constrained deﬁnite formulas resembles the deﬁnitional fragment of (Wadge, 1991), due to
the restrictions on the shape of X x occurring in the head of deﬁnite clauses. However, the formalism discussed in
loc. cit., which was intended as a programming language, also restricted the existential quantiﬁers that could occur
inside goal formulas and did not consider any notion of underlying constraint language.

Problem.     A (higher-order) Constrained Horn Clause Problem is given by a tuple h∆, D, Gi in which:
    • ∆ is a sorting of relational variables.
    • ∆ ⊢ D : o is a constrained deﬁnite formula over ∆.
    • ∆ ⊢ G : o is a constrained goal formula over ∆.
The problem is of order k if k is the largest order of the bound variables that occur in D or G. We say that such a
problem is solvable just if, for all models A of the background theory Th, there exists a valuation α of the variables
in ∆ such that A, α  D, and yet A, α 6 G.
Remark 2. The presentation of the problem follows some of the literature for the use of ﬁrst-order Horn clauses in
veriﬁcation. The system of higher-order constrained Horn clauses is partitioned into two, distinguishing the deﬁnite
clauses as a single deﬁnite formula and presenting the negation of non-deﬁnite clauses as a single goal formula, which
is required to be refuted by valuations. This better reﬂects the distinction between the program and the property to
be proven. Furthermore, solvability is deﬁned in a way that allows for incompleteness in the background theory to
be used to express under-speciﬁcation of programming language features (for example, because they are diﬃcult to
reason about precisely).
Example 1. Let us place the motivating system of clauses from the introduction formally into the framework. To that
end, let us ﬁx the quantiﬁer free fragment of integer linear arithmetic (ZLA) as the underlying constraint language.
The sorting ∆ of relational variables (the unknowns to be solved for) are given by:

                                   Add:     int → int → int → o
                                   Iter:    (int → int → int → o) → int → int → int → o

The higher-order constrained deﬁnite formula D consists of a conjunction of the following three constrained deﬁnite
clauses:
                         ∀x y z. z = x + y ⇒ Add x y z
                         ∀f s n m. n ≤ 0 ∧ m = 0 ⇒ Iter f s n m
                         ∀f s n m. (∃p. n > 0 ∧ Iter f s (n − 1) p ∧ f n p m) ⇒ Iter f s n m
Finally, the clause ∀nm. Iter Add 0 n m ⇒ n ≤ m expressing the property of interest is negated to give goal G =
∃n m. Iter Add 0 n m ∧m < n. This problem is solvable. Being a complete theory, ZLA has one model up to isomorphism
and, with respect to this model, the valuation given in the introduction satisﬁes D but refutes G.


  We believe that the generalisation of constrained horn clauses to higher orders is very natural. However, our
principal motivation in its study is the possibility of obtaining interesting applications in higher-order program
veriﬁcation (analogous to those in ﬁrst-order program veriﬁcation with ﬁrst-order constrained Horn clauses).
 5 We do not require the head variable of M to be in dom(∆).




                                                                 6
We interpret higher-order program veriﬁcation in its broadest sense, encompassing not just purely functional
languages but, more generally, problems in which satisfaction of a property depends upon an analysis of higher-
order control ﬂow. For example, an early application of ﬁrst-order constrained Horn clauses in the very success-
ful constraint logic programming (CLP) paradigm of (Jaﬀar and Maher, 1994) was the analysis of circuit designs
(Heintze et al., 1992), for which systems of clauses were felt to be particularly suitable since they give a succinct,
declarative speciﬁcation of the analyses. The relative advantages of circuit design description using higher-order
combinator libraries or speciﬁcation languages based on higher-order programming, such as (Bjesse et al., 1998),
are well documented, and systems of higher-order of constrained Horn clauses would therefore be a natural setting
in which to verify the properties of such designs.

4 Monotone models
One of the attractive features of ﬁrst-order constrained Horn clauses is that, for any given choice of interpretation
of the background theory, every deﬁnite formula (set of deﬁnite clauses) possesses a unique, least model. Conse-
quently, it follows that there is a solution to a ﬁrst-order Horn clause problem h∆, D, Gi iﬀ for each model of the
background theory, the least model of D refutes G. This reformulation of the problem is of great practical beneﬁt
because it allows for the design of algorithms that, at least conceptually, exploit the canonicity. For example, at
the heart of the design of many successful algorithms for ﬁrst-order Horn clause solving (and program invariant
ﬁnding more generally) is the notion of approximation or abstraction. However, to speak of approximation pre-
supposes there is something to approximate. For program veriﬁers there is, for example, the set of reachable states
or the set of traces of the program, and for ﬁrst-order constrained Horn clause solvers there is the least model.
   The fact that ﬁrst-order deﬁnite formulas possess a least model is paid for by restrictions placed on the syntax. By
forbidding negative logical connectives in goal formulas, it can be guaranteed that the unknown relation symbols
in any deﬁnite clause occur positively exactly once, and hence obtaining the consequences of a given formula is a
monotone operation. We have made the same syntactic restrictions in our deﬁnition of higher-order constrained
Horn formulas, but we do not obtain the same outcome.
Theorem 1. Higher-order constrained deﬁnite formulas do not necessarily possess least models.
Proof. Consider the sorting ∆one of relational variables P: ((one → o) → o) → o and Q : one → o and the deﬁnite
formula D one :
                                               ∆ ⊢ ∀x . x Q ⇒ P x : o
over a ﬁnite constraint language consisting of the sort one of individuals and no functions, relations or constants
of any kind. The language is interpreted in the background theory axiomatised by the sentence ∀xy.x = y, so
that all models consist of a single individual Snoneo = {⋆}. Let us use 0 to denote the mapping ⋆ 7→ 0 and 1
denote the mapping ⋆ 7→ 1, both of which together comprise the set Snone → oo; and let us name the elements
of Sn(one → o) → oo as follows:
                      0   7→ 0                 0 →
                                                 7   0                0   7→ 1                  0   7→ 1
               a≔                       b≔                       c≔                      d≔
                      1    7→ 1                1 → 7 0                1    7→ 1                 1    7→ 0
Then we can describe minimal models α 1 and α 2 by the following equations:
                                   α 1 (Q) = 0                                α 2 (Q) = 1
                       α 1 (P)(a) = 0       α 1 (P)(b) = 0        α 2 (P)(a) = 1       α 2 (P)(b) = 0
                       α 1 (P)(c) = 1       α 1 (P)(d) = 1        α 2 (P)(c) = 1       α 2 (P)(d) = 0
It is easy to verify that there are no models smaller than these and yet they are unrelated, so there is no least
model.                                                                                                         
A similar observation has been made in the pure (without constraint theory) setting by Charalambidis et al. (2013).
  Some consideration of the proof of this theorem leads to the observation that, despite an embargo on negative
logical connectives in goal formulas, it may still be the case that unknown relation symbols occur negatively in
goal formulas (and hence may occur positively more than once in a deﬁnite clause). For example, consider the
deﬁnite clause from above, namely: ∀x . x Q ⇒ P x. Whether or not Q can be said to occur positively in the goal
formula x Q depends on the action of x. If we consider the subterm Snx Qo as a function of x and Q, then it is
monotone in Q only when the function assigned to x is itself monotone. By contrast, if x is assigned an antitone
function, as is the case when x takes on the value d, then Snx Qo will be antitone in Q; for example α 1 (Q) ⊆ α 2 (Q)
but Snx Qo(α 2 [x 7→ d]) ⊆ Snx Qo(α 1 [x 7→ d]).



                                                             7
4.1 Logic programs
As we show in the following section, by restricting to an interpretation in which every function is monotone (in the
logical order) we can obtain a problem in which there is a notion of least solution6 . However, in doing so it seems
that we sacriﬁce some of the logical purity of our original problem: if the universe of our interpretation contains
only monotone functions, it does not include the function implies and so it becomes unclear how to interpret
deﬁnite formulas. Consequently, it requires a new deﬁnition of what it means to be a model of a formula. Rather,
the version of the problem we obtain by restricting to a monotone interpretation is much more closely related to
work on the extensional semantics of higher-order logic programs e.g. (Wadge, 1991; Charalambidis et al., 2013),
which emphasises the role of Horn clauses as deﬁnitions of rules. Hence, we present the monotone restriction in
those terms.

Goal terms. The class of well-sorted goal terms ∆ ⊢ G : ρ is given by the sorting judgements deﬁned by the rules
below, in which c is one of ∧, ∨ or ∃σ and here, and throughout the rules, σ is required to stand for either the
sort of individuals ι or otherwise some relational sort. It is easily veriﬁed that the constrained goal formulas are
a propositional sorted subset of the goal terms. From now on we shall use G, H and K to stand for arbitrary goal
terms and disambiguate as necessary.


 (GCst)                     c ∈ {∧, ∨, ∃ι } ∪ {∃ρ | ρ}                          (GVar)
             ∆ ⊢ c : ρc                                                                     ∆1 , x : ρ, ∆2 ⊢ x : ρ

                                                                                      ∆, x : σ ⊢ G : ρ
      (GConstr)                      ∆ ⊢ φ : o ∈ Fm                     (GAbs)                          x < dom(∆)
                       ∆⊢φ :o                                                        ∆ ⊢ λx . G : σ → ρ

                  ∆⊢G :ι →ρ                                                          ∆ ⊢ G : ρ1 → ρ2      ∆ ⊢ H : ρ1
    (GAppI)                 ∆ ⊢ N : ι ∈ Tm                             (GAppR)
                  ∆⊢GN :ρ                                                                      ∆ ⊢ G H : ρ2


Logic programs. A higher-order, constrained logic program, P, over a sort environment ∆ = x 1 : ρ 1 , . . . , xm : ρm
is just a ﬁnite system of (mutual) recursive deﬁnitions of shape:

                                                    x 1: ρ 1 = G 1 ,    ...,     xm : ρm = Gm

Such a program is well sorted when, for each 1 ≤ i ≤ m, ∆ ⊢ G i : ρ i . Since each x i is distinct, we will sometimes
regard a program P as a ﬁnite map from variables to terms, deﬁned so that P(x i ) = G i . We will write ⊢ P : ∆ to
abbreviate that P is a well-sorted program over ∆.

Standard interpretation. Logic programs can be interpreted in the standard semantics by interpreting the right-
hand sides of the equations using the term semantics given in Section 2. The program P itself then gives rise to
the functional TPS:∆ : Sn∆o ⇒ Sn∆o, sometimes called the one-step consequence operator in the literature on the
semantics of logic programming, which is deﬁned by: TPS:∆ (α)(x) = Sn∆ ⊢ P(x) : ∆(x)o(α).

The logic program of a deﬁnite formula. Every deﬁnite formula D gives rise to a logic program, which is obtained
by collapsing clauses that share the same head X x by taking the disjunction of their bodies, and viewing the
resulting expression as a recursive deﬁnition of X . The formulation as logic program is more convenient in two
ways. First, it is a more natural object to which to assign a monotone interpretation since we have eliminated
implication, which does not act monotonically in its ﬁrst argument, in favour of deﬁnitional equality. Second,
looking ahead to Section 5, the syntactic structure of logic programs allows for a more transparent deﬁnition of a
type system.
   To that end, ﬁx a deﬁnite formula ∆ ⊢ D : o. We assume, without loss of generality7 , that D has the shape:

                                      ∀x r 1 . G 1 ⇒ Xr1 xr1       ∧     ···     ∧      ∀x r ℓ . G ℓ ⇒ Xrℓ xrℓ
 6 Recall that least (respectively monotone) here refers to smallest in (preservation of) the logical order, i.e. with respect to inclusion of relations.
 7 Observe that such a shape can always be obtained by applying standard logical equivalences.




                                                                           8
                               Mn∆ ⊢ x : ρo(α)                   = α(x)
                                Mn∆ ⊢ φ : oo(α)                  = Sn∆ ⊢ φ : oo(α)
                           Mn∆ ⊢ G H : ρ 2 o(α)                  = Mn∆ ⊢ G : ρ 1 → ρ 2 o(α)(Mn∆ ⊢ H : σ1 o(α))
                            Mn∆ ⊢ G N : ρo(α)                    = Mn∆ ⊢ G : ι → ρo(α)(Sn∆ ⊢ N : ιo(α))
                       Mn∆ ⊢ λx : σ . G : σ o(α)                 = λx ′ ∈ Mnσ o. Mn∆, x : σ ⊢ G : σ o(α[x 7→ x ′ ])
                     Mn∆ ⊢ ∧ : o → o → oo(α)                     = and
                     Mn∆ ⊢ ∨ : o → o → oo(α)                     = or
                    Mn∆ ⊢ ∃σ : (σ → o) → oo(α)                   = mexistsσ

                                              Figure 1: Monotone semantics of goal terms.


over a sort environment ∆ = {X 1 : ρ 1 , . . . , X k : ρ k }, i.e. {1, . . . , k} = {r 1 , . . . , r ℓ }. We construct a program over ∆,
called the logic program of D and denoted P D , as follows:

                                                    X 1 = λx 1 . G1′ ,    ...,     X k = λx k . Gk′
              Ô
where G j′ = {G i | r i = j}. Note that {G i | r i = j} are exactly the bodies of all the deﬁnite clauses in D whose
heads are X j . The fact that ⊢ P D : ∆ follows immediately from the well-sortedness of D.
Example 2. The deﬁnite formula component of the Horn clause problem from Example 1 is transformed into the
following logic program P:

        Add = λx y z. z = x + y               Iter = λ f s n m. (n ≤ 0 ∧m = s) ∨ (∃p. 0 < n ∧ Iter f s (n − 1) p ∧ f n p m)

Characterisation. If we were to consider only the standard interpretation then the foregoing development of logic
programs would have limited usefulness. As is well known at ﬁrst-order, the deﬁnite formula and the program
derived from it essentially deﬁne the same class of objects.
Lemma 1. For deﬁnite formula D, the preﬁxed points of TPSD are exactly the models of D.

In contrast to the ﬁrst-order case, it follows that TPSD does not have a least (pre-)ﬁxed point8 . Indeed, for reasons
already outlined, this functional is not generally monotone. However, it will play an important role in Section 4.3.

4.2 Monotone semantics
The advantage of logic programs is that they have a natural, monotone interpretation.

Monotone sort frame. We start from the interpretation of the background theory A, regarding Aι as a discrete
poset. We then deﬁne the monotone sort frame over A by induction:

                         Mnιo ≔ Aι                 Mnoo ≔ 2                  Mnσ1 → σ2 o ≔ Mnσ1 o ⇒m Mnσ2 o

where X ⇒m Y is the monotone function space between posets X and Y , i.e. the set of all functions f ∈ X ⇒ Y
that have the property that x 1 ≤ x 2 implies f (x 1 ) ≤ f (x 2 ). It is easy to verify that this function space is itself
a poset with respect to the pointwise ordering. Of course, in case X is discrete poset Aι , this coincides with the
full function space. We extend the lattice structure of 2 to all relations Mnρo, analogously to the case of the
full function space (and we reuse the same notation since there will be no confusion); and we similarly deﬁne
Mn∆o ≔ Πx ∈ dom(∆). Mn∆(x)o.
     It is worth considering the implications of monotonicity in the special case of relations, i.e. propositional func-
tions. A relation r is an element of X 1 ⇒m · · · ⇒m X k ⇒m 2 just if it is upward closed: whenever r is true of
x 1 , . . . , x k (x i ∈ X i ), and x 1′ , . . . , x k′ (x i′ ∈ X i ) has the property that x i ⊆ x i′ , then r must also be true of x 1′ , . . . , x k′ .
In particular, when r ∈ X ⇒m 2, then r can be thought of as an upward closed set of elements of X .



 8 In this paper we use the term preﬁxed point to refer to those x for which f (x ) ≤ x




                                                                            9
Monotone interpretation. The interpretation of goal terms is deﬁned in Figure 1. As for the standard interpretation,
we assume a ﬁxed interpretation A of the background theory, which is left implicit in the notation. Whilst the stan-
dard interpretation of the positive logical constants for conjunction and disjunction will suﬃce, the interpretation
of existential quantiﬁcation needs to be relativised to the monotone setting: mexistsσ (r ) = max{r (d) | d ∈ Mnσ o}.
Since the implication function implies is not monotone (in its ﬁrst argument), deﬁnite formulas are not inter-
pretable in a monotone frame. However, it is possible to interpret logic programs. To that end, we deﬁne the
functional TPM:∆ on semantic environments by: TPM:∆ (α)(x) = Mn∆ ⊢ P(x) : ∆(x)o(α). In analogy with the Horn
clause problem, we call a preﬁxed point of TPM:∆ a model of the program P. This construction preserves the logical
order.

Lemma 2. Mn∆ ⊢ G : ρo ∈ Mn∆o ⇒m Mnρo and TPM:∆ ∈ Mn∆o ⇒m Mn∆o.
Proof. Immediately follows from the fact that mexists, and and or are monotone and all the constructions are
monotone combinations.                                                                                    
It follows from the Knaster-Tarski theorem that, unlike the functional arising from the standard interpretation,
the monotone functional TPM:∆ has a least ﬁxed point, which we shall write µTPM:∆ . Consequently, logic programs
⊢ P : ∆ have a canonical monotone interpretation, n⊢ P : ∆o, which we deﬁne as µTPM:∆ .

Monotone problem. By analogy with the ﬁrst-order case, we are led to the following monotone version of the
higher-order constrained Horn clause problem. A Monotone Logic Program Safety Problem (more often just mono-
tone problem) is a triple (∆, P, G) consisting of a sorting of relational variables ∆, a logic program ⊢ P : ∆ and a
goal ∆ ⊢ G : o. The problem is solvable just if, for all models of the background theory, there is a preﬁxed point α
of TPM:∆ such that MnGo(α) = 0.

4.3 Canonical embedding
In the monotone problem we have obtained a notion of safety problem that admits a least solution. Due to the
monotonicity of MnGo, there is a preﬁx point witnessing solvability iﬀ the least preﬁx point is such a witness, i.e.
iﬀ MnGo(MnPo) = 0. This clears the way for our algorithmic work in Section 5, which consists of apparatus in
which to construct sound approximations of MnPo. However, the price we have had to pay seems severe, since
we have all but abandoned our original problem deﬁnition.
   The monotone logic program safety problem lacks the logical purity of the higher-order constrained Horn clause
problem, which is stated crisply in terms of the standard interpretation of higher-order logic and the usual notion
of models of formulas. In the context of program veriﬁcation, the monotone problem appears quite natural, but
if we look further aﬁeld, to e.g. traditional applications of constrained Horn clauses in constraint satisfaction, it
seems a little awkward. For example, the signiﬁcance of allowing only monotone solutions seems unclear if one
is looking to state a scheduling problem for a haulage company or a packing problem for a factory.
   Ideally, we would like to specify constraint systems using the standard Horn clause problem, with its clean
logical semantics, but solve instances of the monotone problem, which is easier to analyse, due to monotonicity
and the existence of canonical models. In fact, we shall show that this is possible: every solution to the Horn clause
problem h∆, D, Gi determines a solution to the monotone problem h∆, P D , Gi and vice versa (Theorem 2).

Transferring solutions Let us begin by considering what a mapping between solutions of h∆, P D , Gi and solu-
tions of h∆, D, Gi would look like. In both cases, a solution is a model: the former is a mapping from variables to
monotone relations and the latter is a mapping from (the same) variables to arbitrary relations.
   At ﬁrst glance, it might appear that one can transfer models of P D straightforwardly to models of D, because
monotone relations are, in particular, relations. However, the situation is a little more diﬃcult. Although the
solution space of the Horn clause problem is larger, more is required of a valuation in order to qualify as a model
because the constraints of the Horn clause problem, which involve universal quantiﬁcation over all relations, are
more diﬃcult to satisfy than the equations of the monotone problem, which involve (implicitly) quantiﬁcation
over only the monotone relations.
   To see this concretely, it is useful to consider the simpler case in which all relations are required to be unary,
i.e. ρ is of shape (· · · ((ι → o) → o) → · · · ) → o. In the unary case, we can think of a relation simply as describing
a set of objects, where those objects may themselves be sets of objects. For example, Sn(ι → o) → oo describes
the collection of all sets of sets of individuals. On the other hand, the constraint on monotonicity of relations has



                                                           10
the consequence that, if we think of Mn(ι → o) → oo as describing a collection of sets, it is the collection only
consisting of those sets of sets of individuals that are upward closed. That is, a set s is in Mn(ι → o) → oo just
if, whenever a set of individuals t is in s and t ⊆ u then u is also in s. In general, we can think of Snσ → oo as
the collection of all sets of objects from Snσ o, and Mnσ → oo as the collection of hereditarily upward-closed
sets. Now consider the logic program P = λx . true, in which P is of sort ((int → o) → o) → o. One model of this
program is to take for P the set of all upward-closed sets of sets of integers, which is a relation in Mn((int →
o) → o) → oo. However, the set of all upward-closed sets of sets of integers is not a model of the corresponding
formula ∀x . true ⇒ P x in the standard semantics, because it does not contain, for example, the set {{0}} which
is not upward closed (i.e. its characteristic function is not a monotone Boolean-valued function), yet the universal
quantiﬁcation requires it.
    So, although there is a canonical inclusion of Mnρo into Snρo, it does not extend to map models of P D to models
of D in general. If we return to thinking of the elements of ((int → o) → o) → o formally as Boolean-valued
functions, the inclusion described above is mapping the monotone function r ∈ Mn(int → o) → o)o ⇒m 2,
which satisﬁes r (t) = 1 for all t ∈ Mn(int → o) → oo, to the function J (r ) ∈ Sn(int → o) → oo ⇒ 2, which
satisﬁes, for all t ∈ Sn(int → o) → o)o:
                                                  (
                                                   r (t) if t ∈ Mn(int → o) → o)o
                                      J (r )(t) =
                                                    0    otherwise

In other words, it lifts a function whose domain consists only of hereditarily monotone relations to a function
whose domain consists of all relations simply by mapping non-hereditarily monotone inputs to 0. We could equally
well consider the dual, in which all such inputs were mapped to 1, but the image of the mapping would typically
not refute the goal G because the models so constructed are too large.
   This counterexample suggests that we require a mapping of monotone relations r ∈ Mn((int → o) → o) → oo
to standard relations J (r ) ∈ Sn((int → o) → o) → oo that is a little more sophisticated in the action of J (r ) on
inputs that are not hereditarily monotone. Instead of mapping all such inputs to 0 or all such inputs to 1 we shall
determine the value of J (r ) on some non-monotone input t ∈ Sn(int → o) → oo by considering the value of r on
a monotone input U (t) ∈ Mn(int → o) → oo which is somehow close to t. In fact there are two canonical choices
of hereditarily monotone relations close to a given relation t, which are obtained as, respectively, the largest
monotone relation included in t and the smallest monotone relation in which t is included. We will describe the
situation in general using Galois connection.

Galois connection. A pair of functions f : P → Q and д : Q → P between partial orders P and Q is a Galois
connection just if, for all x ∈ P and y ∈ Q: f (x) ≤ y iﬀ x ≤ д(y). In such a situation we write f ⊣ д and f is said to
be the left adjoint of д, and д the right adjoint of f . First, it is easy to verify that if f ⊣ д then f and д are monotone.
Proposition 1. Given a pair of monotone maps f : P → Q and д : Q → P, the following are equivalent:
(1) The pair (f , д) is a Galois connection.
(2) f ◦ д ≤ 1Q and д ◦ f ≤ 1P .
(3) For all x ∈ P, inf {y ∈ Q | x ≤ д(y)} is deﬁned and equal to f (x); and for all y ∈ Q, sup {x ∈ P | f (x) ≤ y} is
    deﬁned and equal to д(y).
Further, if any one of the above conditions holds, then
  (4) f preserves all existing suprema, and д preserves all existing inﬁma.
  (5) f = f ◦ д ◦ f and д = д ◦ f ◦ д.
  To see the Proposition, just view the pair (f , д) as functors on categories (Mac Lane, 1971); then they forms a
Galois connection exactly when they are an adjunction pair. The following facts are easy to verify:
  (i) If P is a complete lattice and f : P → Q preserves all joins, then f is a left adjoint.
 (ii) If Q is a complete lattice and д : Q → P preserves all meets, then д is an right adjoint.




                                                             11
(iii) If f 1 : P → Q, д1 : Q → P, f 2 : Q → R and д2 : R → Q with f 1 ⊣ д1 and f 2 ⊣ д2 then it follows that
      f 1 ◦ f 2 ⊣ д1 ◦ д2 , is a Galois connection between partial orders P and R.
(iv) If f 1 : P1 → Q 1 , д1 : Q 1 → P1 , f 2 : P2 → Q 2 and д2 : Q 2 → P2 with f 1 ⊣ д1 and f 2 ⊣ д2 then it follows
     that the pair of functions f : [P1 ⇒m P2 ] → [Q 1 ⇒m Q 2 ] and д : [Q 1 ⇒m Q 2 ] → [P1 ⇒m P2 ], deﬁned by:
     f (h) = f 1 ◦ h ◦ д2 and д(k) = д1 ◦ k ◦ f 2 is a Galois connection f ⊣ д between the corresponding monotone
     function spaces (ordered pointwise).
Facts (i) and (ii) are just the Adjoint Functor Theorem (see e.g. (Mac Lane, 1971)) specialised to the case of preorders.
Notice that a special case of (iv) is the construction of a Galois connection f ⊣ д between the (full) function spaces
A ⇒ P and A ⇒ Q (with pointwise order) for ﬁxed set A and partial orders P and Q, whenever there is a Galois
connection f 2 ⊣ д2 between P and Q. This is because there is always a trivial Galois connection id ⊣ id on any set
A by viewing it as a discrete partial order.

Embedding the monotone relations. For general ρ, every complete lattice of monotone relations Mnρo can be
embedded in the complete lattice of all relations Snρo in the following two ways.
                                                         Iρ                  Uρ
                                           Snρo ←
                                                −−− −−− Mnρo ←−
                                                  −−→
                                                   −−→        ←
                                                             −−−−−−−−→
                                                                     −− Snρo                                          (1)
                                                        Lρ                    Jρ

We deﬁne the family of right adjoints Iρ and the family of left adjoints Jρ , by induction on the sort ρ. In the
deﬁnition, Lρ is the uniquely determined left adjoint of Iρ and Uρ is the uniquely determined right adjoint of Jρ .

                                Io (b) = b                                        Jo (b) = b
                             Iι→ρ (r ) = Iρ ◦ r                                Jι→ρ (r ) = Jρ ◦ r
                          Iρ 1 →ρ 2 (r ) = Iρ 2 ◦ r ◦ Lρ 1                  Jρ 1 →ρ 2 (r ) = Jρ 2 ◦ r ◦ Uρ 1

    We brieﬂy discuss this deﬁnition before verifying its correctness. It is worth observing that, rather than deﬁning
Iρ 1 →ρ 2 and Jρ 1 →ρ 2 using the induced left and right adjoints at ρ 1 , we could have given the deﬁnition explicitly
(recalling Galois connection properties (ii) and (iii)) by:
                                             Ù                                                   Ø               
                 Iρ 1 →ρ 2 (r )(s) = Iρ 2 r ( {t | s ⊆ Iρ 1 (t)}) and Jρ 1 →ρ 2 (r )(s) = Jρ 2 r ( {t | Jρ 1 ⊆ s}) .

We have not given the deﬁnition in this way because the proofs that follow only require the adjunction properties
of Lρ 1 and Uρ 1 , and not any explicit characterisation. To unpack the deﬁnition a little more, suppose ρ is restricted
to unary relations and consider the ﬁrst few elements of this inductive family. When ρ is either o or ι → o,
Snρo = Mnρo, and I and J are both the identity. Consequently, they are both left and right adjoint to themselves,
so that L and U are also both the identity. When ρ is (ι → o) → o, by deﬁnition Jρ (r ) = Jo ◦r ◦Uι→o but, as discussed,
both of Jo and Uι→o are identities on their respective domains, so Jρ (r ) is just r . However, Mn(ι → o) → oo is
strictly contained within Sn(ι → o) → oo, so Jρ is merely an inclusion and, consequently, the induced right adjoint
Uρ is more interesting. Using Galois connection property (ii) it can be computed explicitly, revealing that it maps
                      Ð
each s ∈ Snρo to {t ∈ Mnρo | Jρ (t) ⊆ s}. But, we have seen that J(ι→o)→o (t) = t, so it follows that Uρ (s) is
just the largest monotone relation included in s, and we arrive back at the discussion with which we started this
subsection. The following proof gives more insight on the structure of the mappings.
Lemma 3. For each ρ, (i) Lρ ⊣ Iρ and (ii) Jρ ⊣ Uρ are well-deﬁned Galois connections.
Proof. We prove only (i) because the proof of (ii) is analogous. We show that Iρ : Mnρo → Snρo is a well-deﬁned
right adjoint by induction on ρ.
    • When ρ is o, Mnoo = Snoo and Io is the identity, which has left adjoint also the identity.
    • When ρ is of shape ι → ρ 2 , it follows from the induction hypothesis that Iρ 2 : Mnρ 2 o → Snρ 2 o is a well-
      deﬁned right adjoint. It follows from Galois connection property (vi) that the mapping r 7→ Iρ 2 ◦ r : Mnι →
      ρ 2 o → Snι → ρ 2 o is a well-deﬁned right adjoint.
    • Finally, when ρ has shape ρ 1 → ρ 2 , we decompose the deﬁnition of Iρ as follows:
                                               r 7→ I ρ 2 ◦ r ◦ Lρ 1                         s 7→ s
                     Mnρ 1 o ⇒m Mnρ 2 o −−−−−−−−−−−−−→ Snρ 1 o ⇒m Snρ 2 o −−−−→ Snρ 1 o ⇒ Snρ 2 o



                                                                       12
      It follows from the induction hypothesis that Iρ 1 : Mnρ 1 o → Snρ 1 o and Iρ 2 : Mnρ 2 o → Snρ 2 o are both
      well-deﬁned right-adjoints, from which we may infer the existence of left adjoint Lρ 1 : Snρ 1 o → Mnρ 1 o.
      It follows from Galois connection property (iv) that the mapping r 7→ Iρ 2 ◦ r ◦ Lρ 1 : Mnρ 1 o ⇒m Mnρ 2 o →
      Snρ 1 o ⇒m Snρ 2 o is a well-deﬁned right adjoint (with codomain the monotone function space). Finally,
      observe that there is a canonical inclusion between the monotone and full function spaces which, since
      it trivially preserves meets, is as an right adjoint according to Galois connection property (ii). The result
      follows since right adjoints compose (Galois connection property (iii)).
                                                                                                                     
   The Galois connections give a canonical way to move between the universes of monotone and arbitrary rela-
tions; we extend them to mappings on valuations α ∈ Mn∆o by:
                         (                                              (
                          α(x)           if ∆(x) = ι                     α(x)           if ∆(x) = ι
             I∆ (α)(x) =                                    J∆ (α)(x) =
                           I∆(x ) (α(x)) otherwise                        J∆(x ) (α(x)) otherwise

The action is pointwise on relations and trivial on individuals. It is easy to verify that each I∆ and J∆ are right and
left adjoints respectively.
Corollary 1. For each sorting ∆, (i) L∆ ⊣ I∆ and (ii) J∆ ⊣ U∆ are well-deﬁned Galois connections.
We now have a canonical way to move between monotone and arbitrary valuations, but our aim was to be able to
map models of P D to models of D (and vice versa), and we do not yet have any evidence that our mappings are at
all useful in this respect. In both cases, models are preﬁxed points of certain functionals so we look for conditions
which ensure that mappings preserve the property of being a preﬁx point. One such condition is the following: if
F : P → Q is monotone, T1 : P → P and T2 : Q → Q then F will send preﬁxed points of T1 to preﬁxed points of T2
whenever it satisﬁes T2 ◦ F ⊆ F ◦ T1 (in the pointwise order). This is because if T1 (x) ≤ x then F (T1 (x)) ≤ F (x) by
monotonicity, but also T2 (F (x)) ≤ F (T1 (x)) by the assumption so that T2 (F (x)) ≤ F (x).
   In the following we will prove that the right adjoints I and U preserve preﬁx points by showing that T M ◦ U ⊆
U ◦ T S and T S ◦ I ⊆ I ◦ T M . The meat of the deﬁnitions of T S and T M lies in the semantics of goal terms, so we
ﬁrst show that, for all goal terms G, MnGo ◦ U ⊆ U ◦ SnGo and SnGo ◦ I ⊆ I ◦ MnGo. However, we rephrase
MnGo ◦ U ⊆ U ◦ SnGo equivalently as J ◦ MnGo ◦ U ⊆ SnGo and SnGo ◦ I ⊆ I ◦ MnGo equivalently as
SnGo ⊆ I ◦ MnGo ◦ L, which allows for a straightforward induction.
Lemma 4. For all goal terms ∆ ⊢ G : ρ, Jρ ◦ MnGo ◦ U∆ ⊆ SnGo ⊆ Iρ ◦ MnGo ◦ L∆ .
The fact that the two right adjoints map between preﬁx points now follows immediately once the equivalence of
our rephrasings have been veriﬁed.
Lemma 5 (Model translation). Fix a program ⊢ P : ∆.
 (i) If β is a preﬁxed point of TPS:∆ then U∆ (β) is a preﬁxed point of TPM:∆ .

 (ii) If α is a preﬁxed point of TPM:∆ , then I∆ (α) is a preﬁxed point of TPS:∆ .
Proof. It follows from Lemma 4 and Lemma 1 that, for any goal term G:

                            MnGo(U(β)) ⊆ U(SnGo(β)) and SnGo(I(α)) ⊆ I(MnGo(α))

The ﬁrst follows from J ◦ MnGo ◦ U ⊆ SnGo since J is left adjoint. The second follows from SnGo ⊆ I ◦ MnGo ◦ L
by pre-composing with I on both sides and noting that L◦I is deﬂationary. By deﬁnition: T M (α)(x) = MnP(x)o(α)
and T S (β)(x) = SnP(x)o(β), so that we can deduce the following from the above inclusions:

                                  T M (U(β)) ⊆ U(T S (β)) and T S (I(α)) ⊆ I(T M (α))

For part (i), it only remains to observe that if T S (β) ⊆ β then, by monotonicity, U(T S (β)) ⊆ U(β) and, by the
above inclusion, T M (U(β)) ⊆ U(β). Part (ii) is analogous.                                                     
Moreover, these mappings preserve refutation of the goal. Intuitively, we think of U(β) (respectively I(α)) as the
largest monotone (respectively standard) valuation that is smaller than β (respectively α). So, (as is made precise
in Lemma 4) if the latter refutes a goal, so should the former. Hence, we obtain the following problem reduction.



                                                               13
Theorem 2. The higher-order constrained Horn clause problem h∆, D, Gi is solvable, iﬀ the monotone logic program
safety problem h∆, P D , Gi is solvable, and iﬀ in all models of the background theory MnGo(MnP D o) = 0.
Proof. We prove a chain of implications.
    • Assume that h∆, D, Gi is solvable, so that for each model A of the background theory, there is a valuation β
      and A, β  D and A, β 6 G, i.e. SnGo(β) = 0. Fix such a model A of the background theory and then let β
      be the witness given above. Then it follows from Lemma 4 that J(MnGo(U(β))) ⊆ 0, i.e. MnGo(U(β)) = 0.
      Since β is a model of D, it follows from Lemma 1 that it is also a preﬁxed point of TPSD and hence U(β) is a
      preﬁxed point of TPMD
                            by Lemma 5. Therefore, h∆, P D , Gi is also solvable.

    • If h∆, P D , Gi is solvable, then, for each model A of the background theory, there is a preﬁx point α of TPM
                                                                                                                  D
      and MnGo(α) = 0. However, MnP D o is, by deﬁnition, the least preﬁxed point so MnP D o ⊆ U(α) and hence
      MnGo(MnP D o) = 0 follows by monotonicity.
    • Finally assume that in all models of the background theory MnGo(MnP D o) = 0. Fix such a model of the
      background theory. We claim that L(SnGo(I(MnP D o))) ⊆ 0 follows from Lemma 4, which is to say that
      SnGo(I(MnP D o))) = 0. To see this, observe that SnGo(I(MnP D o)) ⊆ I(MnGo(MnP D o)) follows as in the
      proof of Lemma 5 and note that I is right adjoint. Since MnP D o is a preﬁxed point of TPM
                                                                                               D :∆
                                                                                                    , it follows from
                                                         S
      Lemma 5 that I(MnP D o) is a preﬁxed point of TP D . Finally, by Lemma 1 it is therefore a model of D, so
      h∆, D, Gi is solvable.
                                                                                                                                     

5 Refinement Type Assignment
Having reduced the higher-order Horn clause problem to a problem about the least-ﬁxpoint semantics of higher-
order logic programs, we now consider the task of automating reasoning about such programs. For this purpose,
we look to work on reﬁnement type systems, which are one of the most successful approaches to automatically
obtaining invariants for higher-order, functional programs. In this section, we develop a reﬁnement type system
for monotone logic programs.

Elimination of higher-order existentials. Due to monotonicity, it is possible to eliminate higher-order existential
quantiﬁcation from goal terms, simplifying the design of the type system. Given any goal term of shape ∃x : ρ. G,
observe that MnGo is a monotone function of x. If there is a relation that can be used as a witness for x then, by
monotonicity, so too can any larger relation. In particular, G is true of some x of sort ρ iﬀ G is true of the universal
relation of sort ρ, that is, the relation u ρ satisfying u ρ (r 1 ) · · · (r k ) = 1 for all r 1, . . . , r k . Moreover, the universal
relation of sort ρ is itself deﬁnable by a goal term, it is just the term U ρ ≔ λx 1 . . . x k . true. Consequently, Mn∃x :
ρ. G : oo = MnG[U ρ /x]o, in which the instance of existential quantiﬁcation over relations has been eliminated
by a syntactic substitution. For the rest of the paper, we assume without loss of generality that monotone logic
programs contain only existential quantiﬁcation over individuals.

5.1 Syntax
The reﬁnement types are built out of constraint formulas which are combined using the dependent arrow. For
the purposes of this section, we shall assume that the constraint language is closed under conjunction and closed
under (well-sorted) substitution, in the sense that, for every constraint formula ∆, x : ι ⊢ φ : o ∈ Fm and term
∆ ⊢ N : ι ∈ Tm, it follows that φ[N /x] ∈ Fm.

Types. The restricted syntax of goal terms allows us to make several simpliﬁcations to our reﬁnement type
system, in comparison to those in the literature. The ﬁrst is that we only allow reﬁnement of the propositional
sort o and we only allow dependence on the sort of individuals ι. Formally, we deﬁne the set of type expressions
according to the following grammar:

                                         (Type) T        F ohφi | x:ι → T | T1 → T2

in which φ ∈ Fm is a constraint formula. We make this deﬁnition under the assumption that both kinds of arrow
associate to the right and we identify types up to α-equivalence.



                                                                  14
Reﬁnement We restrict attention to those types that we consider to be well-formed, which is deﬁned by a system
of judgements ∆ ⊢ T :: ρ, in which ∆ is a sort environment, T is a type and ρ is a relational sort. In case such a
judgement is provable we say that T reﬁnes ρ.

                     ∆ ⊢ φ : o ∈ Fm                  ∆, x: ι ⊢ T :: ρ                   ∆ ⊢ T1 :: ρ 1   ∆ ⊢ T2 :: ρ 2
     ∆ ⊢ ohφi :: o                                ∆ ⊢ x:ι → T :: ι → ρ                    ∆ ⊢ T1 → T2 :: ρ 1 → ρ 2

Type environments. A type environment Γ is a ﬁnite sequence of pairs of variables and types, x : T , such that
the variable subjects are pairwise distinct. We write the empty sort environment as ϵ. We place similar well-
formedness restrictions on environments, using the judgement ⊢ Γ :: ∆, in which Γ is a type environment and ∆
a sort environment. In case such a judgement is provable we say that Γ reﬁnes ∆.
                                                         ⊢ Γ :: ∆                         ⊢ Γ :: ∆        ∆ ⊢ T :: ρ
                ⊢ ϵ :: ϵ                         ⊢ (Γ, x : ι) :: (∆, x : ι)               ⊢ (Γ, x : T ) :: (∆, x : ρ)

Since the variable subjects of a type environment are required to be distinct, we will frequently view such an
environment as a ﬁnite map from variables to types. Thus, whenever x is a subject in Γ, we will write Γ(x) for the
type assigned to x and dom(Γ) for its set of subjects.

Subtype theory. Much of the power of reﬁnement types is derived from the associated subtype theory, which
imports wholesale the reasoning apparatus of the underlying constraint language. Subtyping between types is the
set of inequalities given by the judgement form ⊢ T1 ⊑ T2 deﬁned inductively.


                            Th  φ ⇒ ψ                   ⊢ T1 ⊑ T2                       ⊢ T1′ ⊑ T1    ⊢ T2 ⊑ T2′
         ⊢ ohφi ⊑ ohψ i                           ⊢ x:ι → T1 ⊑ x:ι → T2                   ⊢ T1 → T2 ⊑ T1′ → T2′

It is natural to view ⊑ as a preorder and useful to distinguish the extremal elements. We write ⊤ρ and ⊥ρ for the
families of reﬁnement types deﬁned inductively as follows:

                               ⊤o      = ohtruei                                ⊥o   = ohfalsei
                             ⊤ι→ρ      = z:ι → ⊤ρ                             ⊥ι→ρ   = z:ι → ⊥ρ
                           ⊤ρ 1 →ρ 2   = ⊥ρ 1 → ⊤ρ 2                     ⊥ρ 1 →ρ 2   = ⊤ρ 1 → ⊥ρ 2

in which the variables z are chosen to be suitably fresh. It is clear that, by construction, ⊢ ⊤ρ :: ρ and ⊢ ⊥ρ :: ρ.

Type assignment. Type assignment for goal terms ∆ ⊢ G : σ and programs ⊢ P : ∆ are deﬁned by a system of
judgements of the forms Γ ⊢ G : T and ⊢ P : Γ respectively, in which type environment Γ and type T are required
to satisfy ⊢ Γ :: ∆ and ∆ ⊢ T :: σ . The system is deﬁned in Figure 2.

Application and abstraction. There are two versions of each of abstraction and application, corresponding to the
fact that we have chosen to emphasize the diﬀerence between dependence of a result type on an argument of
individual sort and non-dependence on arguments of relational sort.
   In common with other reﬁnement type systems in the literature but unlike more general dependent type sys-
tems, our types are not closed under substitution of arbitrary terms of the programming language. This can be
reconciled with the usual rule for dependent application, in which substitution T [N /x] into a type T occurs, in
a number of ways. For example, in the system of (Rondon et al., 2008), terms N of the programming language
that are substituted into a type T through application are understood using uninterpreted function symbols in the
logic; in (Unno and Kobayashi, 2009), the rule for application trivialises the substitution by requiring that T does
not contain the dependent variable x and; in (Terauchi, 2010), the operand N is required to be a variable (which
can be guaranteed when the program is assumed to be in A-normal form). In our case, dependence can only occur
at sort ι and, since the subjects of the system are goal terms, all subterms of sort ι are necessarily already terms of
the constraint language, so we avoid the need for any further conditions.




                                                             15
             (TVar)                                                (TConstraint)                   φ ∈ Fm
                      Γ1 , x: T , Γ2 ⊢ x : T                                        Γ ⊢ φ : ohφi

                      Γ ⊢ G : T1      ⊢ T1 ⊑ T2                              Γ, x : ι ⊢ G : ohφi
             (TSub)                                           (TExists)                          Th  φ ⇒ ψ
                              Γ ⊢ G : T2                                     Γ ⊢ ∃x:ι. G : ohψ i

                 Γ ⊢ G : ohφi      Γ ⊢ H : ohψ i                      Γ ⊢ G : ohφi     Γ ⊢ H : ohψ i    Th  φ ⇒ χ
       (TAnd)                                              (TOr)
                      Γ ⊢ G ∧ H : ohφ ∧ ψ i                                  Γ ⊢ G ∨ H : ohχi           Th  ψ ⇒ χ

                         Γ, x: T1 ⊢ G : T2                                    Γ ⊢ G : T1 → T2       Γ ⊢ H : T1
           (TAbsR)                                                 (TAppR)
                      Γ ⊢ λx:ρ. G : T1 → T2                                             Γ ⊢ G H : T2

            (TAbsI)
                          Γ, x: ι ⊢ G : T                         (TAppI) Γ ⊢ G : x:ι → T      ⊢ Γ :: ∆
                      Γ ⊢ λx:ι. G : x:ι → T                                    Γ ⊢ G N : T [N /x]


                                       Figure 2: Type assignment for goal terms.


Subtyping Our subsumption rule (TSub) is quite standard, we just note that the fact that there are no non-trivial
reﬁnements of the base sort ι has the consequence that there is no signiﬁcant advantage for the subtype judgement
to refer to the type context Γ, which is why it has been formulated in this context-free way. Similar comments can
be made about avoiding the need to distinguish between base and function types in (TVar) .

Constraints and logical constants. To understand the rules for typing constraint, existential, conjunctive and dis-
junctive formulas, it is instructive to assign a meaning to the judgement Γ ⊢ G : ohφi. One should view this
judgement as asserting that: in those valuations that satisfy Γ, G implies φ. This statement is made precise in
Lemma 6 once the semantics of types has been introduced. Under this reading, we can view the type system as a
mechanism for concluding assertions of the form “goal formula G is approximated by constraint φ” or “constraint
φ is an abstraction of goal formula G”. This is a useful assertion for automated reasoning because it is relating
the complicated formula G, which may include higher-order relation symbols whose meanings are deﬁned re-
cursively by the program, to the much more tractable constraint formula φ, which is drawn from a (typically
decidable) ﬁrst-order theory.
   This view helps to clarify the intuition behind the rules for assigning types to formulas headed by a constant. In
particular, for goal terms G that are themselves formulas of the constraint language, the rule (TConstraint) loses
no information in the abstraction. Note that we give only a rule for typing existential quantiﬁcation at base sort ι,
which is justiﬁed by the remarks at the start of this section. Finally, observe that the side condition on (TExists) is
equivalent to the condition Th  (∃x . φ) ⇒ ψ since, due to the well-formedness of the judgement,ψ cannot contain
x freely. We use the side condition in the given form because the constraint language may not allow existential
quantiﬁcation. A similar remark may be made concerning the rule (TOr) and the ability to express disjunction.
   To programs ⊢ P : ∆, of shape x 1 = G 1 , . . . , xm = Gm , we assign type environments according to the rule:

                                               Γ ⊢ G 1 : Γ(x 1)      ···     Γ ⊢ Gm : Γ(xm )
                                 (TProg)
                                                    ⊢ x1 = G 1,     ...,   xm = Gm : Γ
Once we have deﬁned the relational semantics of types, in which a type environment Γ is interpreted as a valu-
ation MLΓM, the soundness of this rule will guarantee that MLΓM is a preﬁx point of TPM:∆ , and hence is an over-
approximation of MnPo.
Example 3. Using (TProg) the program in Example 2 can be assigned the type environment ΓI from the introduction.
For example, the type of Iter can be justiﬁed from the following judgements. First, for the subterms n ≤ 0 and m = 0
in the body of Iter we can apply the (TConstraint) rule to immediately derive the judgements:

                                 Γ ′ ⊢ n ≤ 0 : ohn ≤ 0i      and       Γ ′ ⊢ m = s : ohm = si

in which Γ ′ is the type environment Γ, f : x:int → y:int → z:int → oh0 < x ⇒ y < zi, s : int, n : int, m : int.
Then using (TAnd) , we can derive the judgement: Γ ′ ⊢ n ≤ 0 ∧ m = s : ohn ≤ 0 ∧m = si. Moreover, since also



                                                              16
ZLA  n ≤ 0 ∧ m = s ⇒ 0 ≤ s ⇒ n ≤ m, it follows from the subsumption rule (TSub) that the judgement:

                                       Γ ′ ⊢ n ≤ 0 ∧ m = s : oh0 ≤ s ⇒ n ≤ mi                                        (2)

is also derivable. Next, consider the subterm Iter f s (n − 1) p. Observe that ⊢ ohz = x + yi ⊑ oh0 < x ⇒ y < zi so,
using (TVar) and (TSub) we can assign to f the type

                                     x:int → y:int → z:int → oh0 < x ⇒ y < zi

Hence, it follows from the (TAppR) and (TAppI) rules that we can derive the judgement: Γ ′ ⊢ Iter f s (n − 1) p :
oh0 ≤ s ⇒ n − 1 ≤ pi. To the term f n p m we can assign the type oh0 < n ⇒ p < mi. Hence, by (TAnd) and then
(TExists) we can conclude the judgement:

                          Γ ′ ⊢ ∃p. 0 < n ∧ Iter f s (n − 1) p ∧ f n p m : oh0 ≤ s ⇒ n ≤ mi                          (3)

since ZLA  (∃p. 0 < n ∧ (0 ≤ s ⇒ n − 1 ≤ p) ∧ (0 < n ⇒ p < m)) ⇒ 0 ≤ s ⇒ n ≤ m. Using (1), (2) and (TOr) we
can therefore derive an overall type for the body of the deﬁnition of Iter as oh0 ≤ s ⇒ n ≤ ri. The desired type follows
from applications of (TAbsI) and (TAbsR).

5.2 Semantics
We ascribe two meanings to types. The ﬁrst is the usual semantics in which types are some kind of set and, as is
typical, such sets have the structure of an order ideal. The second is speciﬁc to our setting and exploits the fact
that every type reﬁnes a relational sort. The second semantics assigns to each type a speciﬁc relation. This makes
later developments, such as the demonstration of the soundness of type assignment, simpler and also makes a link
to the notion of symbolic model from the ﬁrst-order case.

Ideal semantics of types. The ideal semantics of reﬁnement types is deﬁned so as to map a well-formed typing
sequent ∆ ⊢ T :: ρ and appropriate valuation α to a subset MnT o(α) ⊆ Mnρo.

                  Mn∆ ⊢ ohφi :: oo(α) =           {0, Sn∆ ⊢ φ : oo(α)}
          Mn∆ ⊢ x:ι → T :: ι → ρo(α) =            {r | ∀n ∈ Aι . r (n) ∈ Mn∆, x : ι ⊢ T :: ρo(α[x 7→ n])}
         Mn∆ ⊢ T1 → T2 :: ρ 1 → ρ 2 o(α) =        { f | ∀r ∈ Mn∆ ⊢ T1 :: ρ 1 o(α). f (r ) ∈ Mn∆ ⊢ T2 :: ρ 2 o(α)}

We are now in a position to make precise the remark following the deﬁnition of type assignment.
Lemma 6. MnGo(α) ∈ Mnohφio(α) iﬀ α  G ⇒ φ.
The soundness of type assignment will guarantee that, additionally, Γ ⊢ G : ohφi implies that MnGo(α) ∈
Mnohφio(α) for all appropriate α.

Relational semantics of types. We will also consider a monotone relational semantics of types. Fix a sort environ-
ment ∆. Given an appropriate ﬁrst-order valuation α, we can associate relations ML∆ ⊢ T :: ρM(α) ∈ Mnρo to
each well formed type ∆ ⊢ T : ρ.

                  ML∆ ⊢ ohφi :: oM(α)         =    Sn∆ ⊢ φ : oo(α)
        ML∆ ⊢ x:ι → T :: ι → ρM(α)(n)         =    ML∆, x : ι ⊢ T :: ρM(α[x 7→ n])
       ML∆ ⊢ T1 → T2 :: ρ 1 → ρ 2 M(α)(r )    =    ML∆ ⊢ T2 :: ρ 2 M(α)            if r ⊆ ML∆ ⊢ T1 :: ρ 1 M(α)
       ML∆ ⊢ T1 → T2 :: ρ 1 → ρ 2 M(α)(r )    =    MLϵ ⊢ ⊤ρ 2 :: ρ 2 M(∅)          otherwise

It follows straightforwardly from the deﬁnitions that MLT M(α) is a monotone relation.

Symbolic models. Additionally, we can consider a type environment under a relational interpretation. We deﬁne,
for all x ∈ dom(∆), ML⊢ Γ :: ∆M(x) = MLΓ(x)M(∅). This object is a monotone valuation and hence, following the
results of Section 4, this semantics makes precise the idea of a type environment Γ as a (candidate) symbolic model,
that is, a ﬁnite representation of a model designed for the purposes of automated reasoning.




                                                           17
Relationship. The ideal and the relational semantics are closely related: the relational interpretation MLT M(α) of
a type T is the largest element of the ideal MnT o(α). Thus we see also that MnT o(α) is principal. For each relation
r ∈ Mnρo let us write ⇓ρ r for the downward closure of {r } in Mnρo (we will typically omit the subscript).
Lemma 7. For all types ∆ ⊢ T :: ρ and α ∈ Sn∆o, MnT o(α) = ⇓MLT M(α).

5.3 Soundness
We return to the discussion of type assignment by deﬁning semantic judgements paralleling those for the type
system. First let us make a preliminary deﬁnition. Let ⊢ Γ :: ∆, then we say that valuation α ∈ Mn∆o satisﬁes Γ
just if, for all x ∈ dom(∆), α(x) ∈ MnΓ(x)o. We write the following judgement forms:

                                  T1 ⊑ T2              Γ G :T                   P :Γ

In the ﬁrst, we assume that ∆ ⊢ T1 : ρ and ∆ ⊢ T2 : ρ are types of the same sort. Then the meaning of  T1 ⊑ T2 is
that, for all α ∈ Mn∆o, MnT1 o(α) ⊆ MnT2 o(α). In the second, we assume that ⊢ Γ :: ∆, ∆ ⊢ G : ρ and ∆ ⊢ T :: ρ.
Then the meaning of Γ  G : T is that, for all valuations α ∈ Mn∆o, if α satisﬁes Γ then MnGo(α) ∈ MnT o(α).
Finally, in the third, we assume that ⊢ P : ∆ and ⊢ Γ :: ∆. Then the meaning of  P : Γ is that MnPo satisﬁes Γ.
Theorem 3 (Soundness of Type Assignment).


 (i) If ⊢ T1 ⊑ T2 then  T1 ⊑ T2 .
 (ii) If Γ ⊢ G : T then Γ  G : T .
(iii) If ⊢ P : Γ then  P : Γ.
Proof sketch. The ﬁrst and second claims are proven by straightforward inductions on the relevant judgements.
In the third case it follows from (ii) and the deﬁnition of (TProg) that MLΓM satisﬁes Γ and is therefore a preﬁxed
point of TPM:∆ . Since MnPo is the least such, the result follows.                                                
   This allows for a sound approach to solving systems of higher-order constrained Horn clauses. Given an instance
of the problem h∆, D, Gi, we construct the corresponding logic program h∆, P D , Gi. If there is a type environment
⊢ Γ :: ∆ such that ⊢ P D : Γ and Γ ⊢ G : ohfalsei then it follows from Theorem 3 that, for each model A of
the background theory, MLΓM (with constants interpreted with respect to A) is a valuation that satisﬁes D but
refutes G. The approach is, however, incomplete. Consider the following instance, adapted from an example of
(Unno et al., 2013) showing the incompleteness of reﬁnement type systems for higher-order program veriﬁcation.
Example 4. The higher-order constrained Horn clause problem h∆, D, Gi speciﬁed by, respectively:

                 Leq : int → int → o                ∀i j. i ≤ j ⇒ Leq i j
                                                                               ∃i. Holds (Leq i) (i − 1)
                 Holds : (int → o) → int → o        ∀p n. p n ⇒ Holds p n

is solvable in the theory of integer linear arithmetic (ZLA), since there is no integer i smaller than its predecessor.
However, the logic program P D deﬁned as Leq = λij. i ≤ j, Holds = λpn. pn is not typable. This is because if there
were a type environment ⊢ Γ :: ∆ for which ⊢ P D : Γ and Γ ⊢ G : ohfalsei, it would have shape:

                      Leq : i:int → j:int → ohχi       Holds : (x:int → ohφi) → n:int → ohψ i

for some formulas i: int, j: int ⊢ χ : o and x: int ⊢ φ : o and n: int ⊢ ψ : o. These formulas would necessarily satisfy
the following conditions: 1. ZLA  i ≤ j ⇒ χ, 2. ZLA  φ[n/x] ⇒ ψ , 3. ZLA  χ[x/j] ⇒ φ, and 4. ZLA  (∃i. φ[i −
1/n]) ⇒ false, implied by the deﬁnition of the type system. It follows from (1) and (3) that also ZLA  i ≤ x ⇒ φ.
Since φ does not contain i freely, it follows that this is equivalent to ZLA  (∃i. i ≤ x) ⇒ φ, itself equivalent to
ZLA  φ. However, this contradicts (4), so there can be no such type assignment.
It seems likely that, to obtain a sound and (relatively) complete approach, one could adapt the development de-
scribed in (Unno et al., 2013), at the cost of complicating the system a little.




                                                          18
5.4 Automation
This approach to solving the higher-order constrained Horn clause problems relies on ﬁnding a reﬁnement type
environment to act as a witness. It is well understood that, for reﬁnement type systems following a certain pat-
tern, typability (i.e. the existence of a type environment satisfying some properties) can be reduced to ﬁrst-order
constrained Horn clause solving (Terauchi, 2010; Bjørner et al., 2012; Jhala et al., 2011). Hence, the search for a
witnessing environment can be automated using standard techniques (an explicit deﬁnition is included in Ap-
pendix C).
   In order to check that the approach is feasible, we have implemented a prototype tool and used it to automatically
verify a few small systems of clauses. The tool is written in Haskell and uses the Parsec library for parsing input in
a mathematical syntax using unicode characters or ascii equivalents. Output is either a similar format or conforms
to SMT-LIB in a manner that lets Z3 (De Moura and Bjørner, 2008) solve the system of ﬁrst order clauses.
   The test cases are obtained from that subset of the functional program veriﬁcation problems given in (Kobayashi et al.,
2011) which do not make local assertions, re-expressed as higher-order Horn clause problems according to the
method sketched by example in Section 1. The prototype9 and the exact suite of test cases is available at http://github.com/p
In all but one of the examples the prototype takes around 0.01s to transform the system of clauses and Z3 takes
around 0.02s to solve the resulting ﬁrst-order system. The remaining example, named neg, suﬀers from our choice
of reﬁnement type system. It is solved by the system described in loc. cit., which allows type-level intersection,
but cannot be solved using our approach.

5.5 Expressibility of type assertions
It is possible to express the complement of a type using a goal formula. For example, according to the forgoing
semantics, the type
                               T ≔ (x:ι → y:ι → ohx ≡ y mod 2i) → z:ι → ohz , 0i
represents the set MnT o(∅) of all monotone relations of sort (ι → ι → o) → ι → o that relate all parity-preserving
inputs to non-zero outputs. The complement of this set of relations can be deﬁned (in the monotone semantics)
by the goal term Com(T ) ≔ λz. z (λxy. x ≡ y mod 2) 0 which classiﬁes such relations according to whether or not
they relate the particular parity-preserving relation λxy. x ≡ y mod 2 to 0. The mode of deﬁnition we have in mind
is the following.

Goal deﬁnability. We say that a relation r ∈ Mnρo is goal term deﬁnable (more brieﬂy G-deﬁnable) just if there
exists a closed goal term ⊢ H : ρ and MnH o(∅) = r . We say that a class of relations is G-deﬁnable just if the
characteristic predicate of the class is G-deﬁnable.

   Returning to the example, if a given relation r does not relate λxy. x ≡ y mod 2 to 0, then r is not a member
of MnT o(∅). On the other hand, if r is not a member MnT o(∅), then there is some parity-preserving relation s
that is related by r to 0. Since r is monotone, it follows that r also relates all relations larger than s to 0. Since
λxy. x ≡ y mod 2 is the largest of the parity-preserving relations, it follows that r relates λxy. x ≡ y mod 2 to 0.
Hence the set
                                  {r ∈ Mn(ι → ι → o) → ι → oo | r < MnT o(∅)}
is G-deﬁnable by the goal term Com(T ).

Deﬁnability of type complements and the relational semantics. Any G-deﬁnition Com(T ) of the complement ofT is
intertwined with a G-deﬁnition of the largest element of T : to understand when a relation r is not in the type T1 →
T2 you must understand when there exists a relation s ∈ MnT1 o(∅) such that r (s) is not in MnT2 o(∅), i.e. when the
property MnCom(T )o(∅)(r (s)) holds. However, since MnCom(T )o(∅) and r are monotone, if MnCom(T )o(∅)(r (s))
holds then MnCom(T )o(r (s ′)) holds for any s ′ ⊇ s. Consequently, there exists an s ∈ MnT1 o(∅) satisfying the
property iﬀ the largest element of MnT1 o(∅) satisﬁes the property. This leads to the deﬁnitions by mutual induction
on type:

          Com(ohφi) = λz. z ∧¬φ                                     Lar(G)(ohφi) = G ∨ φ
        Com(x:ι → T ) = λz. ∃x :ι. Com(T ) (z x)                Lar(G)(x:ι → T ) = λz. Lar(G)(T [z/x])
        Com(T1 → T2 ) = λz. Com(T2 ) (z Lar(false)(T1 ))        Lar(G)(T1 → T2 ) = λz. Lar(G ∨ Com(T1 ) z)(T2 )
 9 A basic web interface to the prototype tool is available at http://mjolnir.cs.ox.ac.uk/horus.




                                                           19
in which Com(T ) is a G-deﬁnition of the complement of the class MnT o(∅). The deﬁnition of Lar is parametrised
by a goal formula representing domain conditions that are accumulated during the analysis of function types. It
follows that Lar(false)(T ) is a G-deﬁnition of the largest element of the class MnT o(∅).
Lemma 8. For any closed type ⊢ T :: ρ:
 (i) The goal term Com(T ) is a G-deﬁnition of the class {r ∈ Mnρo | r < MnT o(∅)}.
 (ii) The goal term Lar(false)(T ) is a G-deﬁnition of the relation MLT M(∅).
   This gives a sense in which we can express the higher-type property G : T within the higher-order constrained
Horn clause framework, namely as the goal formula Com(T ) G deﬁning the negation of the type assertion (recall
that in the higher-order Horn clause problem we aim to refute the negation of property to be proven, expressed as
a goal formula). Furthermore, we can use this result in order to justify an extension of the syntax of higher-order
constrained Horn clauses with a new kind of type-guarded existential quantiﬁcation. This allows us to state goal
formulas like ∃x :T .G, i.e. there exists a relation in (the set deﬁned by) reﬁnement type T that moreover satisﬁes
G. The full development is contained in the anonymous supplementary materials.

6 Related Work
Constrained Horn-clause solving in ﬁrst-order program veriﬁcation Our motivation comes mainly from the use of
constrained Horn clauses to express problems in the veriﬁcation of ﬁrst-order, imperative programs. The papers
of Bjørner et al. (2012) and Bjørner et al. (2015) argue the case for the approach and provide a good overview of
it. One of the best recommendations for the approach is the selection of highly eﬃcient solvers that are available,
such as (Grebenshchikov et al., 2012; Hoder et al., 2011; Gurﬁnkel et al., 2015), which we exploit in this work as
part of the automation of our prototype solver for higher-order clauses.

Higher-order logic programming Work on higher-order logic programming is typically concerned with program-
ming language design and implementation. Consequently, one of the main themes of the work discussed in the
following is that of (i) ﬁnding a good semantics for higher-order logic programming languages, and one of the cen-
tral criteria for a good semantics is that (ii) it lends itself well to developing techniques for enumerating answers
to queries. In contrast to (i), our work is about a particular satisﬁability problem of logic, namely the existence of
a model of a formula satisfying certain criteria (modulo a background theory). In higher-order logic programming
(e.g. Nadathur and Miller (1990); Chen et al. (1993); Charalambidis et al. (2013)) it often does not make sense, a
priori, to ask about the existence of models because the semantics of the logic programming language is ﬁxed
once and for all as part of its deﬁnition. One can ask whether the set of answers to a program query is empty, but
to understand this as a logical question about the models of a formula is only possible through a result such as our
contribution in Section 4. In contrast to (ii), our goal is to develop techniques, such as the type system in Section
5, for the dual problem, namely to show that a Horn formula is satisﬁable (recall that we require the existence of
a model refuting the goal G, and the goal is the negation of a Horn clause G ⇒ false). Query answering (unsat-
isﬁability) is recursively enumerable, whereas satisﬁability, in particular where there is a background theory, is
typically harder.
   Recent work on extensional semantics for higher-order logic programming started with Wadge (1991) and con-
tinued with, for example, Charalambidis et al. (2013, 2014). Wadge was the ﬁrst to observe that relational variables
appearing as arguments in the head of clauses is problematic. This line of work gives a denotational semantics to
higher-order logic programs and so is very closely related to the monotone semantics of logic programs that we
use in Section 4, except that there is no treatment of constraint theories (discussed in the following paragraph).
Unlike our work, Charalambidis et al. (2013) are very careful to ensure the algebraicity of their domains so that
they can build a sophisticated system of query answering based on enumerating compact elements. If we were to
extend our work to encompass a treatment of counterexamples, then we would want to exploit algebraicity in a
similar manner. Their work does not make any connection between their denotational semantics of higher-order
logic programs and satisﬁability in standard higher-order logic; it seems likely that our result could be adapted to
their setting.

Higher-order constraint logic programming. Another way in which all of the foregoing work diﬀers from our own
is that, in the work we have mentioned so far, there is no treatment of constraints. Whilst ﬁrst-order constraint



                                                          20
logic programming is a very well developed area (an old, but good survey is (Jaﬀar and Maher, 1994)), there is
very little existing work on the higher-order extension. Lipton and Nieva (2007) give a Kripke semantics for a
λProlog-like language extended with a generic framework for constraints. In contrast to our work, the underlying
higher-order logic is intuitionistic and the precise notion of model is bespoke to the paper.

Interpretations of higher-order logic Under the standard semantics, an interpretation of a higher-order theory
consists of a choice of universe Aι in which to interpret the sort of individuals ι and an interpretation of the
constants of the theory. In particular, the interpretation Snσ1 → σ2 o of any arrow sort σ1 → σ2 is ﬁxed by the
choice of Aι . In Henkin (or general) semantics, an interpretation consists of all of the above but, additionally, also
a choice of interpretation for each of the inﬁnitely many arrow sorts (under some natural restrictions regarding
deﬁnability of elements). For example, there are Henkin interpretations in which the collection nint → oo does not
contain all sets of integers. We choose to frame the higher-order constrained Horn clause problem using standard
semantics because it is already established in veriﬁcation. For example, when monadic second order logic (MSO)
is used to express veriﬁcation problems on transition systems, the second-order variables range over all sets of the
states10 . Consequently, the standard semantics seems the most appropriate starting point for work on higher-order
constrained Horn clauses in veriﬁcation.

Automated veriﬁcation of functional programs Two of the most well-studied approaches to the automated veri-
ﬁcation of functional programs are based on higher-order model checking (Ong, 2006; Kobayashi and Ong, 2009;
Kobayashi, 2013) and reﬁnement types (Rondon et al., 2008; Vazou et al., 2015; Jhala et al., 2011; Zhu and Jagannathan,
2013; Unno et al., 2013). A method to verify higher-order programs more directly using ﬁrst-order constrained
Horn clauses has been suggested by Bjørner, McMillan, and Rybalchenko (2013a).
   In higher-order model checking, the problem of verifying a higher-order program is reformulated as the problem
of verifying a property of the tree generated by a higher-order recursion scheme, see e.g. (Kobayashi et al., 2011).
The approach has the advantage of being based around a natural, decidable problem, which is an attractive tar-
get for the construction of eﬃcient solvers (Ramsay et al., 2014; Broadbent et al., 2013; Broadbent and Kobayashi,
2013). By contrast, we propose to investigate higher-order program veriﬁcation based around the higher-order
constrained Horn clause problem. Although this problem is generally undecidable, it has the advantage of being
able to express (background theory) constraints directly and so has the potential to be a better setting in which to
search for higher-order program invariants.
   In approaches based on reﬁnement types, a type system is used to the reduce the problem of ﬁnding an invariant
for the higher-order program, to ﬁnding a number of ﬁrst-order invariants of the ground-type data at certain pro-
gram points, which can often be expressed as ﬁrst-order constrained Horn clause solving. As exempliﬁed by the
LiquidHaskell system of Vazou et al. (2014), one advantage of using a type system directly is that it can very nat-
urally encompass all the features of modern programming languages. We have not addressed the problem of how
best to frame a higher-order program veriﬁcation problem using higher-order clauses (excepting our motivating
sketch in the introduction) but it does not seem as clear as for approaches using reﬁnement types. On the other
hand, the reduction to ﬁrst-order invariants that underlies reﬁnement type approaches has a cost in expressibil-
ity. In principle, it is possible to overcome this deﬁciency, for example by employing types in which higher-order
invariants can be encoded as ﬁrst-order statements of arithmetic (Unno et al., 2013); we mention also the scheme
of Bjørner et al. (2013a) which proposes to view higher-order invariants as ﬁrst-order statements about closures
(encoded as data structures). However, in both cases it seems plausible that working directly in higher-order logic
may lead to the development of more transparent and generic techniques. To beneﬁt from this would necessitate
a move to a diﬀerent technology from our system of reﬁnement types used for solving.

7 Conclusion and future work
In this work, we have presented our notion of higher-order constrained Horn clauses and the ﬁrst foundational
results, with an emphasis on making connections to existing work in the veriﬁcation of higher-order programs.
By analogy with the situation for ﬁrst-order program veriﬁcation, we believe that higher-order constrained Horn
clauses can be an attractive, programming-language independent setting for developing automated techniques for
the veriﬁcation of higher-order programs. Let us conclude by giving some more justiﬁcation to this belief through
a discussion of future work.
10 Or all ﬁnite sets of states in the case of weak MSO, but in both cases the domain is ﬁxed by the setting. A Henkin semantics formulation of
   the problem would allow for a solution to the satisﬁability problem to specify its own domain for the second order variables.




                                                                     21
   We have shown, in Example 4, that our method for solving is bound by the same limitations as typical reﬁnement
type systems in the literature. However, there is a lot of scope to develop new approaches to solving which may
not suﬀer in the same way. A general result in this direction would be to show that these limitations are not
intrinsic to the higher-order constrained Horn clause problem. For example, it seems plausible that higher-order
clauses are expressive (in the sense of Cook) for suitable Hoare logics over higher-order programs, mirroring the
case at ﬁrst-order (Blass and Gurevich, 1987; Bjørner et al., 2015). A speciﬁc technique for solving, which we plan
to pursue, is an approach for reducing higher-order clauses to ﬁrst-order clauses with datatypes, using the ideas
of Bjørner et al. (2013a) (which is itself in the spirit of Reynolds’ defunctionalisation (Reynolds, 1972)).
   In defunctionalisation, as in our method of Section 5, the goal is to reduce the problem to that of ﬁrst-order
clauses by doing some reasoning about the behaviour of higher-order functions. Without further investigation, it
is unclear whether this reduction should happen at the level of programs (as is the case in e.g. (Bjørner et al., 2013a))
or at the level of a higher-order intermediate representation such as higher-order constrained Horn clauses (as
we have suggested in the introduction). However, if one believes that the reasoning involved in such a reduction
is generic, in the sense of being essentially the same whether the programs are written in Haskell, or ML, or
Javascript, then this suggests that it is worthwhile to investigate whether this reasoning can be done eﬃciently
on the intermediate representation, rather than have the reasoning re-implemented in each diﬀerent analysis of
each diﬀerent higher-order programming language.
   Finally, we make the observation that higher-order constraints may be useful even in the veriﬁcation of ﬁrst-
order procedures. For example, in reﬁnement type systems, a reﬁnement of a base type is typically a predicate on
values of the type. Therefore, it seems reasonable that a reﬁnement of a type constructor should be a (Boolean-
valued) function on predicates, i.e. a higher-order relation. It would be interesting to develop a type inference
algorithm that can reason about reﬁnements of type constructors (a concern that is orthogonal to the existence
of higher-order procedures) using higher-order constraints, and to understand the connections with the work of
Vazou, Rondon, and Jhala (2013).

Acknowledgements. Research was partially completed while the second and third authors were visiting the In-
stitute for Mathematical Sciences, National University of Singapore in 2016.




                                                           22
References
Tewodros A. Beyene, Corneliu Popeea, and Andrey Rybalchenko. 2013. Solving Existentially Quantiﬁed Horn
  Clauses. In Computer Aided Veriﬁcation - 25th International Conference, CAV 2013, Saint Petersburg, Russia, July
  13-19, 2013. Proceedings. 869–882.
Per Bjesse, Koen Claessen, Mary Sheeran, and Satnam Singh. 1998. Lava: Hardware Design in Haskell. In Pro-
  ceedings of the third ACM SIGPLAN International Conference on Functional Programming (ICFP ’98), Baltimore,
  Maryland, USA, September 27-29, 1998. 174–184.
Nikolaj Bjørner, Arie Gurﬁnkel, Kenneth L. McMillan, and Andrey Rybalchenko. 2015. Horn Clause Solvers for
  Program Veriﬁcation. In Fields of Logic and Computation II - Essays Dedicated to Yuri Gurevich on the Occasion
  of His 75th Birthday. 24–51.
Nikolaj Bjørner, Kenneth L. McMillan, and Andrey Rybalchenko. 2012. Program Veriﬁcation as Satisﬁability Mod-
  ulo Theories. In 10th International Workshop on Satisﬁability Modulo Theories, SMT 2012, Manchester, UK, June
  30 - July 1, 2012. 3–11.
Nikolaj Bjørner, Kenneth L. McMillan, and Andrey Rybalchenko. 2013a. Higher-order Program Veriﬁcation as
  Satisﬁability Modulo Theories with Algebraic Data-types. CoRR abs/1306.5264 (2013).
Nikolaj Bjørner, Kenneth L. McMillan, and Andrey Rybalchenko. 2013b. On Solving Universally Quantiﬁed Horn
  Clauses. In Static Analysis - 20th International Symposium, SAS 2013, Seattle, WA, USA, June 20-22, 2013. Proceed-
  ings. 105–125.
Andreas Blass and Yuri Gurevich. 1987. Computation Theory and Logic. Springer-Verlag, London, UK, UK, Chapter
  Existential Fixed-point Logic, 20–36.
Christopher H. Broadbent, Arnaud Carayol, Matthew Hague, and Olivier Serre. 2013. C-SHORe: a collapsible
  approach to verifying higher-order programs. In International Conference on Functional Programming, ICFP’13.
  ACM, 13–24.
Christopher H. Broadbent and Naoki Kobayashi. 2013. Saturation-based model checking of higher-order recursion
  schemes. In Computer Science Logic, CSL’13 (LIPIcs), Vol. 23. Schloss Dagstuhl – Leibniz-Zentrum fuer Informatik,
  129–148.
Angelos Charalambidis, Zoltán Ésik, and Panos Rondogiannis. 2014. Minimum Model Semantics for Extensional
  Higher-order Logic Programming with Negation. TPLP 14, 4-5 (2014), 725–737.
Angelos Charalambidis, Konstantinos Handjopoulos, Panagiotis Rondogiannis, and William W. Wadge. 2013. Ex-
  tensional Higher-Order Logic Programming. ACM Trans. Comput. Log. 14, 3 (2013), 21.
Weidong Chen, Michael Kifer, and David S. Warren. 1993. HiLog: A foundation for higher-order logic program-
 ming. Journal of Logic Programming 15, 3 (1993), 187–230.
Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An Eﬃcient SMT Solver. In Proceedings of the Theory and
  Practice of Software, 14th International Conference on Tools and Algorithms for the Construction and Analysis of
  Systems (TACAS’08/ETAPS’08). 337–340.
Sergey Grebenshchikov, Ashutosh Gupta, Nuno P. Lopes, Corneliu Popeea, and Andrey Rybalchenko. 2012.
  HSF(C): A Software Veriﬁer Based on Horn Clauses - (Competition Contribution). In Tools and Algorithms for
  the Construction and Analysis of Systems - 18th International Conference, TACAS 2012, Held as Part of the Euro-
  pean Joint Conferences on Theory and Practice of Software, ETAPS 2012, Tallinn, Estonia, March 24 - April 1, 2012.
  Proceedings. 549–551.
Arie Gurﬁnkel, Temesghen Kahsai, Anvesh Komuravelli, and Jorge A. Navas. 2015. The SeaHorn Veriﬁcation
  Framework. In Computer Aided Veriﬁcation - 27th International Conference, CAV 2015, San Francisco, CA, USA,
  July 18-24, 2015, Proceedings, Part I. 343–361.
Nevin Heintze, Spiro Michaylov, and Peter Stuckey. 1992. CLP(âĎĲ) and some electrical engineering problems.
  Journal of Automated Reasoning 9, 2 (1992), 231–260.



                                                        23
Krystof Hoder, Nikolaj Bjørner, and Leonardo Mendonça de Moura. 2011. µZ- An Eﬃcient Engine for Fixed Points
  with Constraints. In Computer Aided Veriﬁcation - 23rd International Conference, CAV 2011, Snowbird, UT, USA,
  July 14-20, 2011. Proceedings. 457–462.
Joxan Jaﬀar and Michael J. Maher. 1994. Constraint Logic Programming: A Survey. J. Log. Program. 19/20 (1994),
  503–581.
Ranjit Jhala, Rupak Majumdar, and Andrey Rybalchenko. 2011. HMC: Verifying Functional Programs Using Ab-
  stract Interpreters. In Computer Aided Veriﬁcation - 23rd International Conference, CAV 2011, Snowbird, UT, USA,
  July 14-20, 2011. Proceedings. 470–485.
Naoki Kobayashi. 2013. Model Checking Higher-Order Programs. J. ACM 60, 3 (2013), 20:1–20:62.
Naoki Kobayashi and C.-H. Luke Ong. 2009. A Type System Equivalent to the Modal Mu-Calculus Model Checking
  of Higher-Order Recursion Schemes. In Logic in Computer Science, LICS 2009. IEEE Computer Society, 179–188.
Naoki Kobayashi, Ryosuke Sato, and Hiroshi Unno. 2011. Predicate abstraction and CEGAR for higher-order model
  checking. In Programming Languages Design and Implementation, PLDI’11. ACM, 222–233.
James Lipton and Susana Nieva. 2007. Higher-Order Logic Programming Languages with Constraints: A Seman-
  tics. In Typed Lambda Calculi and Applications: 8th International Conference, TLCA 2007, Paris, France,June 26-28,
  2007. Proceedings, Simona Ronchi Della Rocca (Ed.). Springer Berlin Heidelberg.
Saunders Mac Lane. 1971. Categories for the Working Mathematician. Springer.
Gopalan Nadathur and Dale Miller. 1990. Higher-Order Horn Clauses. J. ACM 37, 4 (1990), 777–814.
C.-H. Luke Ong. 2006. On Model-Checking Trees Generated by Higher-Order Recursion Schemes. In Logic In
  Computer Science, LICS’06. IEEE Computer Society, 81–90.
Steven J. Ramsay, Robin P. Neatherway, and C.-H. Luke Ong. 2014. A Type-Directed Abstraction Reﬁnement
  Approach to Higher-Order Model Checking. In Principles of Programming Languages, POPL’14. ACM, 61–72.
John C. Reynolds. 1972. Deﬁnitional Interpreters for Higher-order Programming Languages. In Proceedings of the
  ACM Annual Conference - Volume 2 (ACM ’72). 717–740.
Patrick Maxim Rondon, Ming Kawaguchi, and Ranjit Jhala. 2008. Liquid types. In Proceedings of the ACM SIGPLAN
  2008 Conference on Programming Language Design and Implementation, Tucson, AZ, USA, June 7-13, 2008. 159–
  169.
Tachio Terauchi. 2010. Dependent types from counterexamples. In Proceedings of the 37th ACM SIGPLAN-SIGACT
  Symposium on Principles of Programming Languages, POPL 2010, Madrid, Spain, January 17-23, 2010. 119–130.
Hiroshi Unno and Naoki Kobayashi. 2009. Dependent type inference with interpolants. In Proceedings of the 11th
  International ACM SIGPLAN Conference on Principles and Practice of Declarative Programming, September 7-9,
  2009, Coimbra, Portugal. 277–288.
Hiroshi Unno, Tachio Terauchi, and Naoki Kobayashi. 2013. Automating Relatively Complete Veriﬁcation of
  Higher-order Functional Programs. In Proceedings of the 40th Annual ACM SIGPLAN-SIGACT Symposium on
  Principles of Programming Languages (POPL ’13). ACM, New York, NY, USA, 75–86.
Niki Vazou, Alexander Bakst, and Ranjit Jhala. 2015. Bounded reﬁnement types. In Proceedings of the 20th ACM
  SIGPLAN International Conference on Functional Programming, ICFP 2015, Vancouver, BC, Canada, September 1-3,
  2015. 48–61.
Niki Vazou, Patrick Maxim Rondon, and Ranjit Jhala. 2013. Abstract Reﬁnement Types. In Programming Lan-
  guages and Systems - 22nd European Symposium on Programming, ESOP 2013, Held as Part of the European Joint
  Conferences on Theory and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013. Proceedings. 209–228.
Niki Vazou, Eric L. Seidel, Ranjit Jhala, Dimitrios Vytiniotis, and Simon Peyton-Jones. 2014. Reﬁnement Types
  for Haskell. In Proceedings of the 19th ACM SIGPLAN International Conference on Functional Programming (ICFP
  ’14). 269–282.



                                                        24
William W. Wadge. 1991. Higher-Order Horn Logic Programming. In Logic Programming, Proceedings of the 1991
 International Symposium, San Diego, California, USA, Oct. 28 - Nov 1, 1991. 289–303.
He Zhu and Suresh Jagannathan. 2013. Compositional and Lightweight Dependent Type Inference for ML. In
  Veriﬁcation, Model Checking, and Abstract Interpretation, 14th International Conference, VMCAI 2013, Rome, Italy,
  January 20-22, 2013. Proceedings. 295–314.


A Supplementary material for Section 4
A.1 Proof of Lemma 4
We ﬁrst consider the special case in which G is existential quantiﬁcation and rephrase the latter claim equivalently
as L ◦ Sn∃o ⊆ Mn∃o ◦ L (which is easier to prove).
Lemma 9. For sorts σ (either ι or some ρ), mexistsσ ◦ Uσ →o ⊆ existsσ ⊆ mexistsσ ◦ Lσ →o .
Proof. In case σ is ι, by deﬁnition mexistsι = existsι and Uι→o (s) = s = Lι→o (s), so the result is clear. Otherwise,
σ is some relational sort ρ and we observe that both of the following are true for all s ∈ Snρ → oo:

(i) for all r ∈ Mnρo: Uρ →o (s)(r ) = 1 implies s(Jρ (t)) = 1
(i) for all t ∈ Snρo: s(t) = 1 implies Lρ →o (s)(Lρ (t)) = 1
Hence, (i) witnesses r to the satisﬁability of U(s) can be mapped to witnesses J(t) to the satisﬁability of s and (ii)
witnesses t to the satisﬁability of s can be mapped to witnesses L(t) to the satisﬁability of L(s); thus proving the
lemma. To see that (i) is true we just observe that if Uρ →o (s)(r ) = 1, then s(Jρ (r )) = 1 by deﬁnition. To see that
(ii) is true, we reason as follows. If s(t) = 1, then since I ◦ L is inﬂationary, also Iρ →o (Lρ →o (s))(t) = 1. Hence, by
deﬁnition, Lρ →o (s)(Lρ (t)) = 1.                                                                                        
Lemma 4. For all goal terms ∆ ⊢ G : ρ, Jρ ◦ MnGo ◦ U∆ ⊆ SnGo ⊆ Iρ ◦ MnGo ◦ L∆ .
Proof. The proof of the inclusion J ◦ MnGo ◦ U ⊆ SnGo is by induction on the sorting judgement for goal terms.
We give here only the more interesting cases:
    • If ∆ ⊢ x : ρ then:
                                       J(Mnxo(U(α))) = J(U(α(x))) ⊆ α(x) = Snxo(α)
      by deﬁnition and the fact that J ◦ U is deﬂationary.
    • If ∆ ⊢ φ : o with φ a formula of the constraint language, then:

                                          J(Mnφo(U(α))) = Snφo(U(α)) = Snφo(α)

      by deﬁnition and since the free variables of φ are assumed to be all ﬁrst-order.
    • If ∆ ⊢ HK : ρ 2 with ∆ ⊢ H : ρ 1 → ρ 2 and ∆ ⊢ K : ρ 1 , then we reason as follows. First observe that:

                           Jρ 2 (MnHKo(U(α)))      =    Jρ 2 (MnH o(U(α))(MnKo(U(α))))
                                                   ⊆    Jρ 2 (MnH o(U(α))(Uρ 1 (Jρ 1 (MnKo(U(α))))))

      by deﬁnition and because J ◦ MnH o(U(α)) is monotone and U ◦ J is inﬂationary. Then:

               Jρ 2 (MnH o(U(α))(Uρ 1 (Jρ 1 (MnKo(U(α)))))) =       Jρ 1 →ρ 2 (MnH o(U(α)))(Jρ 1 (MnKo(U(α))))
                                                            ⊆       Jρ 1 →ρ 2 (MnH o(U(α)))(SnKo(α))

      by deﬁnition, the induction hypothesis and because J(r ) is monotone in general because r is. Finally:

                           Jρ 1 →ρ 2 (MnH o(U(α)))(SnKo(α)) ⊆ SnH o(α)(SnKo(α)) = SnHKo(α)

      by deﬁnition and the induction hypothesis.




                                                               25
    • If ∆ ⊢ λx . H : ρ 1 → ρ 2 and ∆, x : ρ 1 ⊢ H : ρ 2 , we ﬁrst observe that:
                Jρ 1 →ρ 2 (Mnλx . H o(U(α)))(s) = Jρ 2 (Mnλx . H o(U(α))(Uρ 1 (s))) = Jρ 2 (MnH o(U(α[x 7→ s])))
      follows from the deﬁnitions. Then we note that:
                             Jρ 2 (MnH o(U(α[x 7→ s]))) ⊆ SnH o(α[x 7→ s])) = Snλx . H o(α)(s)
      follows by deﬁnition and the induction hypothesis.
    • If ∆ ⊢ ∨ : o → o → o or ∆ ⊢ ∧ : o → o → o, the result holds by deﬁnition.
    • If ∆ ⊢ ∃σ : (σ → o) → o then:
                              J(Mn∃o(U(α))) = J(mexists) = mexists ◦ U ⊆ exists = Sn∃o(α)
      follows by deﬁnition and Lemma 9.
Showing the inclusion SnGo ⊆ I ◦ MnGo ◦ L is dual: just observe that whenever, in the above proof, an inclusion
is justiﬁed by U ◦ J being inﬂationary (respectively J ◦ U deﬂationary), the corresponding reverse inclusion can be
justiﬁed by noting that L ◦ I is deﬂationary (respectively I ◦ L inﬂationary).                                    

B Supplementary Material for Section 5
B.1 Proof of Lemma 7
Lemma 10. Let ∆ ⊢ T1 → T2 :: ρ 1 → ρ 2 be a type and let α ∈ Mn∆o be a ﬁrst order valuation. Then MLT1 → T2 M(α)
is monotone.
Proof. Let t 1 , t 2 ∈ Mnρ 1 o and consider the following two cases.
    • If t 1 ⊆ MLT1 M(α), then MLT1 → T2 M(α)(t 1 ) = MLT2 M(α). Since MLT1 → T2 M(α)(t 2 ) is either MLT2 M(α) or ⊤,
      it follows that MLT1 → T2 M(α)(t 1 ) ⊆ MLT1 → T2 M(α)(t 2 ).
    • Otherwise, MLT1 → T2 M(α)(t 1 ) = ⊤ and it follows from the assumption that t 2 * MLT1 M(α). Hence, also
      MLT1 → T2 M(α)(t 2 ) = ⊤.
                                                                                                                         
Lemma 7. For all types ∆ ⊢ T :: ρ and α ∈ Mn∆o, MnT o(α) = ⇓MLT M(α).
Proof. The proof is by induction on the derivation of the sorting judgement.
    • When the judgement is of shape ∆ ⊢ ohφi :: o, clearly {0, Snφo(α)} = ⇓MLφM(α).
    • When the judgement is of shape ∆ ⊢ x:ι → T :: ι → ρ we ﬁrst observe that, for all n ∈ Aι , it follows
      from the induction hypothesis that MnT o(α[x 7→ n]) = ⇓MLT M(α[x 7→ n]). To see downwards closure, let
      t 2 ∈ Mnx:ι → T o and t 1 ⊆ t 2 . Then, for all n ∈ Aι , t 2 (n) ∈ MnT o(α[x 7→ n]). Since t 1 (n) ⊆ t 2 (n) and this
      set is downwards closed, it follows that t 1 (n) is also a member. To see membership, MLx:ι → T M(α)(n) ∈
      MnT o(α[x 7→ n]) so, by deﬁnition, MLx:ι → T M(α) ∈ Mnx:ι → T o(α). Finally, let r ∈ Mnx:ι → T o(α) and
      let n ∈ Aι . Then it follows that r (n) ∈ MnT o(α[x 7→ n]) so r (n) ⊆ MLT M(α[x 7→ n]) as required.
    • When the judgement has shape ∆ ⊢ T1 → T2 :: ρ 1 → ρ 2 we proceed as follows. To see that MnT1 → T2 o(α)
      is downwards closed, let t 2 be a member and t 1 ⊆ t 2 . Then let t ∈ MnT1 o(α). It follows that t 2 (t) ∈ MnT2 o(α)
      and t 1 (t) ⊆ t 2 (t), so the result follows from the induction hypothesis. To see membership, let t ∈ MnT1 o(α). It
      follows from the induction hypothesis that, therefore t ⊆ MLT1 M(α). Hence MLT1 → T2 M(α)(t) = MLT2 M(α)
      and it follows from the induction hypothesis that MLT2 M(α) ∈ MnT2 o(α), as required. To see the extremal
      property, let s ∈ MnT1 → T2 o(α) and let t ∈ Mnρ 1 o. If t ∈ MnT1 o(α), so that t ⊆ MLT1 M(α) follows
      from the induction hypothesis, then the fact that s(t) ⊆ MLT1 → T2 M(α)(t) follows from the fact that
      s(t) ∈ MnT2 o(α), MLT1 → T2 M(α)(t) = MLT2 M(α) and the induction hypothesis. Otherwise, t < MnT1 o(α)
      and it follows from the induction hypothesis that, therefore, t * MLT1 M(α). Hence MLT1 → T2 M(α)(t) = ⊤ρ 2
      and the result is immediate.
                                                                                                                         



                                                             26
B.2 Proof of Theorem 3
Theorem 3. For all ⊢ θ : ∆, ⊢ Γ :: ∆, ∆ ⊢ G : σ and ∆ ⊢ T ,T1 ,T2 :: σ , the following is true:
 (i) ⊢ T1 ⊑ T2 implies  T1 ⊑ T2
 (ii) Γ ⊢ G : T implies Γ  G : T
(iii) ⊢ P : Γ implies  P : Γ
Proof. The proof of the ﬁrst claim is by induction on the derivation.
    • If the conclusion is ⊢ int ⊑ int the result follows immediately.
    • If the conclusion is ⊢ ohφi ⊑ ohψ i, then necessarily, for all α ∈ Mn∆o, α  φ ⇒ ψ . Then let α ∈ Mn∆o. It
      follows that Mnohφio(α) = {0, Mnφo(α)} ⊆ {0, Mnψ o(α)}.
    • If the conclusion is ⊢ x:T1 → T2 ⊑ y:T1′ → T2′ , let α ∈ Mn∆o, r ∈ Mnx : T1 → T2 o(α) and s ∈ MnT1′ o. It
      follows from the induction hypothesis that

                                MnT1′ o(α) = MnT1′ [z/y]o(γ ) ⊆ MnT1 [z/x]o(β) = MnT1 o(α)
                                MnT2 o(α) = MnT2 [z/x]o(β) ⊆ MnT2′ [z/y]o(γ ) = MnT2′ o(α)

      where β = (α \ {x 7→ α(x)}) ∪ {z 7→ α(x)} and γ = (α \ {y 7→ α(y)}) ∪ {z 7→ α(y)}. It follows that
      s ∈ MnT1 o(α) and hence r (s) ∈ MnT2 [s/y]o(α). Finally, we observe that therefore r (s) ∈ MnT2′ [s/y]o(α).
The proof of the second claim is by induction on the typing derivation.
    • When the judgement has shape Γ1 , x : T , Γ2 ⊢ x : T , assume α  Γ. Then MnGo(α) = α(x). From our
      assumption, α(x) ∈ MnΓ(x)o, i.e. α(x) ∈ MnT o(α) as required.
    • When the judgement has shape Γ ⊢ φ : ohφi, it follows immediately that Mnφo(α) ∈ Mnohφio.
    • When the judgement has shape Γ ⊢ G ∧ H : ohφ ∧ ψ i, let α  Γ. It follows from the induction hypothesis
      that Γ  G : ohφi and Γ  H : ohψ i and consequently, MnGo(α) ∈ Mnohφio and MnH o(α) ∈ Mnohφio.
      The result then follows from Lemma 6.
    • When the judgement has shape Γ ⊢ G ∨ H : ohφ ∨ ψ i the proof is analogous to the case above.
    • When the judgement has shape Γ ⊢ ∃x .G : oh∃x.φi let α  Γ. It follows from the induction hypothesis that
      Γ, x : int  G : ohφi. Hence, for any n ∈ Mninto, α[x 7→ n]  G ⇒ φ. Assume α  ∃x .G, then there is some
      n such that α[x 7→ n]  G which has the consequence that α[x 7→ n]  φ and hence α  ∃x .φ. The result
      then follows from Lemma 6.
    • When the judgement has shape Γ ⊢ G H : T2 [H /x] and Γ ⊢ H : int, let α  Γ. It follows from the induc-
      tion hypothesis that MnGo(α) ∈ Mnx:int → T2 o(α) and MnH o(α) ∈ Mninto(α). Hence, by deﬁnition,
      MnG H o(α) ∈ MnT2 o(α[x 7→ MnH o(α)]) = MnT2 [H /x]o(α).
    • When the judgement has shape Γ ⊢ G H : T2 and Γ ⊢ H : T1 and T1 is not int, let α  Γ. It follows from the
      induction hypothesis that MnGo(α) ∈ MnT1 → T2 o and MnH o ∈ MnT1 o. Hence, it follows by deﬁnition
      that MnG H o(α) ∈ MnT2 o(α).
    • When the judgement has shape Γ ⊢ λx : int. G : x:int → T , let α  Γ. It follows from the induction hypoth-
      esis that, for all n ∈ Mninto, MnGo(α[x 7→ n]) ∈ MnT o(α[x 7→ n]). By deﬁnition Mnλx : int. Go(α) ∈
      Mnx:int → T o(α) just if, for all n ∈ Mninto, Mnλx : int. Go(α)(n) ∈ MnT o(α[x 7→ n]). The result then
      follows from the deﬁnition of Mnλx . Go(α)(n) and the previous observation.
    • When the judgement has shape Γ ⊢ λx : ρ. G : T1 → T2 for T1 , int, let α  Γ. It follows from the induction
      hypothesis that, for all r ∈ MnT1 o(α), then MnGo(α[x 7→ r ]) ∈ MnT2 o(α[x 7→ r ]). Let r ∈ MnT1 o(α),
      then Mnλx . Go(α)(r ) = MnGo(α[x 7→ r ]). It follows from the previous observation that this expression is
      an element of MnT2 o(α[x 7→ r ]), but T2 cannot have any occurrence of relational variable x since it is built
      out of constraint formulas.



                                                            27
In the third case we reason as follows. Assume ⊢ P : Γ so that, necessarily, for all x ∈ dom(∆), Γ ⊢ P(x) : Γ(x).
Then it follows from part (ii) that, for each x ∈ dom(∆), and α satisfying Γ, MnP(x)o(α) ∈ MnΓ(x)o. It follows
from Lemma 7 that MLΓM satisﬁes Γ. Consequently, for all x ∈ dom(∆), MnP(x)o(MLΓM) ∈ MnΓ(x)o, which is
to say that MnP(x)o(MLΓM) ⊆ MLΓM(x). Hence, MLΓM is a preﬁxpoint of TPM:∆ . It follows from the canonicity of
MnPo that MnPo ⊆ MLΓM and, by Lemma 7, that therefore, for all x ∈ dom(∆), MnPo(x) ∈ MnΓ(x)o.
                                                                                                               

B.3 Proof of Lemma 8
Lemma 8. For any closed type ⊢ T :: ρ:
 (i) The goal term Com(T ) is a G-deﬁnition of the class {r ∈ Mnρo | r < MnT o(∅)}.
 (ii) The goal term Lar(false)(T ) is a G-deﬁnition of the relation MLT M(∅).
Proof. We generalise the statement, proving for all ∆ ⊢ T :: ρ, α ∈ Mn∆o and goal formulas ∆ ⊢ G : o:
MnCom(T )o(α) = {r ∈ Mnρo | r < MnT o(α)} and, for all d of the appropriate sorts: MnLar(G)(T )o(α)(d) = 1
iﬀ MnGo(α) = 1 or MLT M(α)(d) = 1. The proof is by induction on ∆ ⊢ T :: ρ.
    • If the judgement is of shape ∆ ⊢ ohφi :: o then we reason as follows.
        (i) For all b ∈ 2:
                                         MnCom(T )o(α)(b) = Mnx ∧ ¬φo(α[x 7→ b])
           This latter expression evaluates to 1 iﬀ α[x 7→ b] 6 x ⇒ φ (by the variable convention we assume
           that x does not occur in φ). It follows from Lemma 6 that this is the case iﬀ Mnxo(α[x 7→ b]) = b <
           MnT o(α[x 7→ b]) = MnT o(α).
       (ii) Also, MnLar(G)(T )o(α) = MnG ∨ φo(α) = or(MnGo(α))(Mnφo(α)). This latter expression denotes 1
            iﬀ MnGo(α) = 1 or Mnφo(α) = 1.
    • If the judgement is of shape ∆ ⊢ x:ι → T ′ :: ι → ρ then we reason as follows.
        (i) For all r ∈ Mnι → ρo:

                                    MnCom(T )o(α)(r ) = Mn∃x:ι. Com(T ′ )(z x)o(α[z 7→ r ])

           This latter expression denotes 1 iﬀ there is some n ∈ Aι such that MnCom(T ′ )(x y)o(α[z 7→ r ][x 7→
           n]) = 1 and this is true iﬀ there is some n such that MnCom(T ′ )o(α[x 7→ n])(r (n)) = 1. It follows from
           the induction hypothesis that this is true iﬀ there is some n such that r (n) < MnT ′ o(α[x 7→ n]). This
           is exactly r < Mnx:ι → T ′ o(α).
       (ii) For all n ∈ Aι and d:

                                    MnLar(G)(T )o(α)(n)(d) = MnLar(G)(T ′ )o(α[x 7→ n])(d)

           It follows from the induction hypothesis that this denotes 1 iﬀ either MnGo(α[x 7→ n]) = 1 or
           MLT ′ M(α[x 7→ n])(d) = 1. We may assume, by the variable convention, that x does not occur in
           G. This latter expression denotes 1 iﬀ MLx:ι → T ′ M(α) by deﬁnition.
    • If the judgement is of shape ∆ ⊢ T1 → T2 :: ρ 1 → ρ 2 then we reason as follows.
        (i) For all r ∈ Mnρ 1 → ρ 2 o:

                                MnCom(T )o(α)(r ) = MnCom(T2 )(x Lar(false)(T1 ))o(α[x 7→ r ])

           This latter expression is true iﬀ MnCom(T2 )o(α)(r (MnLar(false)(T1 )o(α))) = 1. It follows from the
           induction hypothesis, part (ii), that this is the case iﬀ
           MnCom(T2 )o(α)(r (MLT1 M(α))) = 1. By the monotonicity of the operator and the fact that MLT1 M(α)
           is the largest element of MnT1 o(α) (Lemma 7), this is true iﬀ there is some s ∈ MnT1 o(α) such that
           MnCom(T2 )o(α)(r (s)) = 1. It follows from the induction hypothesis, part (i), that this is true iﬀ there
           is some s ∈ MnT1 o(α) such that r (s) < MnT2 o(α), which is exactly r < MnT1 → T2 o(α).



                                                          28
        (ii) Fix r ∈ Mnρ 1 o(α) and d appropriate to the argument sorts of ρ 2 . Then:

                                  MnLar(G)(T )o(α)(r )(d) = MnLar(G ∨ Com(T1 ) x)(T2 )o(α[x 7→ r ])(d)

             It follows from the induction hypothesis, part (ii), that this expression denotes 1 iﬀ (P1) MnG ∨
             Com(T1 ) xo(α[x 7→ r ]) = 1 or (P2) MLT2 M(α)(d) = 1. It follows that this ﬁrst possibility (P1) is
             true iﬀ MnGo(α) = 1 or MnCom(T1 )o(α)(r ) = 1. It follows from the induction hypothesis, part
             (i), that MnCom(T1 )o(α)(r ) = 1 iﬀ r < MnT1 o(α). Consequently, (P1) or (P2) iﬀ MnGo(α) = 1 or
             (Q1) r < MnT1 o(α) or (Q2) MLT2 M(α)(d) = 1. We claim that (Q1) or (Q2) iﬀ MLT M(α)(r )(d) = 1.
             In the backward direction, assume that (Q1) does not hold. Then, by Lemma 7, r ⊆ MLT1 M(α) and
             MLT M(α)(r )(d) = 1 implies MLT2 M(α)(r )(d) = 1 which is (Q2). In the forward direction we analyse the
             two cases. In case (Q1), by Lemma 7, r * MLT1 M(α). Then MLT M(α)(r )(d) = ⊤ρ 2 (r )(d) = 1 by deﬁni-
             tion. Otherwise we assume (Q2) and not (Q1). Then, by Lemma 7, r ⊆ MLT1 M(α), so MLT2 M(α)(d) = 1
             implies MLT M(α)(r )(d) = 1 by deﬁnition.
                                                                                                                       

C Type Inference
In this appendix we give an algorithm, presented as a collection of syntax directed rules of inference, for determin-
ing the typability of a logic program over quantiﬁer free integer linear arithmetic. For convenience, we assume
that the signature of the constraint language includes, for each sort int → · · · → int → o of any arity, a countable
supply of uninterpreted relation constants11 , which will appear in the inference as constraint formulas reﬁning
the propositional sort. The ﬁnite subset of these constants that are used in a given inference become the unknown
relation symbols to be solved for in a ﬁrst-order constrained Horn clause problem.
   The sort of a well formed reﬁnement type is determined uniquely so we deﬁne the underlying sort T ♭ of a
reﬁnement type T recursively:
                                                    ohsi ♭ = o
                                            (x:int → T )♭ = int → T ♭
                                              (T1 → T2 )♭ = T1♭ → T2♭
The underlying sort environment Γ ♭ of a type environment Γ is obtained recursively as follows:

                                                               ϵ♭    =     ∅
                                                       (Γ, x: T )♭   =     Γ ♭ , x: T ♭

Fresh relational variables. We suppose a function freshRel that, given a sort environment ∆ and a second-order
relational sort ρ, yields some term R x1 · · · xk with

                                                       R: int → · · · → int → ρ
                                                          |     {z       }
                                                                 k-times

a fresh, second-order relation constant, and the set {x 1 : int, . . . , x k : int} exactly the subset of ∆ consisting of
variables of integer sort. We denote this situation by the judgement:
                                                                                          R fresh
                                                R x1 · · · xk = freshRel(∆)(ρ)

Fresh types. Similarly, given a sort environment ∆ and a sort σ , we suppose a function freshTy that yields a choice
of type T reﬁning σ and which is constructed from fresh relations as described above. We will write a judgement
of shape T = freshTy(∆)(σ ), which is deﬁned by the following system:

                                                          int = freshTy(∆)(int)

                                                           φ = freshRel(∆)(o)
                                                          ohφi = freshTy(∆)(o)
11 We use relation constants rather than variables to ensure we stay within a ﬁrst-order language.




                                                                     29
                    (ISubBool)
                                    φ ⇒ψ       ohφi ⊑ ohψ i

                                C 1 T1′ ⊑ T1    C 2 T2 ⊑ T2′
            (ISubArrow)
                                C 1 ∧ C 2 T1 → T2 ⊑ T1′ → T2′

                              C T [z/x] ⊑ T ′ [z/y]
     (ISubProd)                                           z fresh
                      ∀z : int. C x:int → T ⊑ y:int → T ′




                      (IVar)
                                Γ1 , x: T , Γ2 true     x :T

                     (IConstraint)
                                       Γ true         φ : ohφi

                      (IAppI)     Γ C       G : x:int → T
                                  Γ C       G N : T [N /x]

           Γ C1       G : T1 → T2    Γ C2              H : T3     C3   T3 ⊑ T1
(IAppR)
                             Γ C1 ∧ C2 ∧ C3            G H : T2

                               Γ, x : int C G : T
            (IAbsI)
                        Γ ∀x : int. C λx:int. G : x:int → T

                    T1 = freshTy(Γ ♭ )(σ ) Γ, x : T1 C            G : T2
      (IAbsR)
                              Γ C λx:ρ. G : T1 → T2

                      Γ C 1 G : ohφ 1 i  Γ C 2 H : ohφ 2 i
          (IAnd)
                         Γ C 1 ∧ C 2 G ∧ H : ohφ 1 ∧φ 2 i

                     Γ C 1 G : ohφ 1 i  Γ C 2 H : ohφ 2 i
           (IOr)
                        Γ C 1 ∧ C 2 G ∨ H : ohφ 1 ∨φ 2 i

                               Γ, x: int C G : ohφi
            (IExists)
                          Γ ∀x : int. C ∃x: int. G : oh∃x. φi



                                  Γ = freshEnv(´)
                        C x′
                           Tx ⊑ Γ(x) (for each x ∈ dom(∆))
                      Γ C x P(x) : Tx (for each x ∈ dom(∆))
          (IProg)          Ó                    ′
                             x ∈dom(∆) (C x ∧ C x ) P:Γ


                        Figure 3: Rules of inference.




                                       30
                                     T1 = freshTy(∆)(ρ 1)    T2 = freshTy(∆)(ρ 2)
                                            T1 → T2 = freshTy(∆)(ρ 1 → ρ 2 )
                                           T = freshTy(∆, z : int)(ρ)
                                                                       z fresh
                                       z:int → T = freshTy(∆)(int → ρ)

Fresh type environments.     We extend the judgement to sort environments ∆ of shape x 1 : σ1 , . . . , x k : σk by the
following rule:
                                    T1 = freshTy(∆)(σ1 ) · · · Tk = freshTy(∆)(σk )
                                             x 1: T1 , . . . , x k : Tk = freshEnv(´)

Inference. Rather than giving a recursive procedure directly, we deﬁne three syntax-directed typing judgements,
which have the following shape:
                                C    T1 ⊑ T2           Γ C      G :T           C    P:Γ
for Γ the type environment in which the type assignment is conducted, C a ﬁrst-order Horn constraint describing
possible assignments to the uninterpreted relational constants, G the term and T the inferred type.
   The three judgement forms are deﬁned according to the rules in Figure 3, where we have generalised the judge-
ments freshRel and freshTy to sets of sorts in the obvious way. Since the system is syntax directed it can be read
as an algorithm by regarding:
                               C T1 ⊑ T2 T1 and T2 as inputs and C as output.
                              Γ C G : T Γ and G as inputs and C and T as outputs.
                                C P : Γ P as input and C and Γ as outputs.
   Given an instance of the monotone problem h∆, P, Gi, let C 1 P : Γ and Γ C 2 G : ohφi. The type environment
Γ and the type ohφi, which we think of as outputs, are built from types containing formulas with occurrences of
fresh relational constants. Then there is a type environment Γ ′ (without fresh relational constants) such that
⊢ P : Γ ′ and Γ ′ ⊢ G : ohfalsei iﬀ the ﬁrst order system of constrained Horn clauses h∆ ′, C 1 ∧ C 2 ∧ φ ⇒ falsei has a
symbolic model, i.e. a solution that is expressible within quantiﬁer free integer linear arithmetic.

D Extension by type guards
It is worthwhile to consider the kinds of safety veriﬁcation questions that can be posed in our formalisation. In par-
ticular, since we are interested in verifying higher-order programs, it would be helpful to be able to state properties
of higher-order functions. In type-based approaches to veriﬁcation, such as (Rondon et al., 2008; Unno et al., 2013),
it is possible to do this. For example, one can state a typing judgement asserting that some program expression is
guaranteed to map evenness preserving functions to non-zero integers.
    It is not immediate how to state a similar property using higher-order constrained Horn clauses. Here, properties
are speciﬁed by stating their negation as a goal formula. The negation of the example property above has the form:
∃f : int → int → o. ∃x :int. EvenPreserving f ∧x = 0∧Gf x, with G playing the role of the program expression, and
EvenPreserving is required to be a goal formula asserting that its argument relates even integers only to other even
integers. That is, a logical formulation of the reﬁnement type x:int → y:int → ohx ≡ 0 mod 2 ⇒ y ≡ 0 mod 2i.
However, the existence of such a goal term is problematic, since evenness preservation of this kind is not a mono-
tone property — it is clearly satisﬁed by the empty relation, yet violated by many relations larger than it.
    The aim of this section is to show that, despite this serious deﬁciency of expression, it is possible to state higher-
type properties of the kind given above. The key is to observe that, in the formulation of a type judgement as a
goal, the properties expressed by reﬁnement types will only occur guarding existentially quantiﬁed variables.
Hence, these “type guards” (such as the hypothetical EvenPreserving predicate above), serve only to limit the
search space from which the existential witness is drawn, rather than to test some quality of a particular, concrete
individual. We begin by making the restricted shape of these type guards precise then, in Section D.1, we show
how monotonicity allows for such guards to be entirely eliminated.

Type guarded existentials. We extend the syntax of higher-order Horn clauses by adding a family of type guarded
existential quantiﬁer constants ∃T ::ρ : ρ → o, which are parametrised by a closed type ⊢ T :: ρ. We write ∃x:T . M
rather than ∃T ::ρ (λx . M), omitting ρ since it can be uniquely determined from T .



                                                           31
Interpretation. For the purposes of interpretation, we need to give two standard semantics to types that parallels
their monotone semantics. The deﬁnitions are completely analogous:

                   Sn∆ ⊢ ohφi :: oo(α) =           {0, Sn∆ ⊢ φ : oo(α)}
            Sn∆ ⊢ x:ι → T :: ι → ρo(α) =           {r | ∀n ∈ Aι . r (n) ∈ Sn∆, x : ι ⊢ T :: ρo(α[x 7→ n])}
          Sn∆ ⊢ T1 → T2 :: ρ 1 → ρ 2 o(α) =        { f | ∀r ∈ Sn∆ ⊢ T1 :: ρ 1 o(α). f (r ) ∈ Sn∆ ⊢ T2 :: ρ 2 o(α)}

but now the set from which e.g. f is drawn in the third clause is the set of all propositional functions Snρ 1 → ρ 2 o.
Similarly for the relational semantics.

                     SL∆ ⊢ ohφi :: oM(α)       =    Sn∆ ⊢ φ : oo(α)
           SL∆ ⊢ x:ι → T :: ι → ρM(α)(n)       =    SL∆, x : ι ⊢ T :: ρM(α[x 7→ n])
         SL∆ ⊢ T1 → T2 :: ρ 1 → ρ 2 M(α)(r )   =    SL∆ ⊢ T2 :: ρ 2 M(α)            if r ⊆ SL∆ ⊢ T1 :: ρ 1 M(α)
         SL∆ ⊢ T1 → T2 :: ρ 1 → ρ 2 M(α)(r )   =    SLϵ ⊢ ⊤ρ 2 :: ρ 2 M(∅)          otherwise

It follows that SLT M(α) is actually a monotone relation. An inspection of the proof of Lemma 7 shows that it carries
over to the case of the standard semantics.
    Having deﬁned this semantics of types, the family of type guarded existential quantiﬁers can be interpreted
in the standard semantics by the family of functions existsT ::ρ ∈ Snρo ⇒ 2 and in the monotone semantics by
the family of functions mexistsT ::ρ ∈ Mnρo ⇒m 2 deﬁned by existsT ::ρ (s) = max{s(d) | d ∈ Sn⊢ T :: ρo} and
mexistsT ::ρ (r ) = max{r (d) | d ∈ Mn⊢ T :: ρo}.

Type guarded higher-order Horn clauses We extend the higher-order Horn clause problem to incorporate type
guarded existentials by adding to the grammar for constrained goal formulas: G F · · · | ∃x:T . G. Note that this
subsumes the existential quantiﬁer on relations completely as: Sn∃ρ o = Sn∃⊤ρ ::ρ o, since the meaning Sn⊤ρ o(α)
of the top type in any valuation α is the whole universe Snρo. The extended problem is called the type-guarded,
higher-order, constrained Horn clause problem. We extend logic programs in the same way, adding the possibility
that constant c can be ∃T ::ρ in the side condition of the rule (GCst). The resulting problem we name the type-
guarded, monotone logic safety problem. The reduction given by Theorem 2 still holds in this extended setting.
Theorem 4. Type-guarded, higher-order constrained Horn clause problem h∆, D, Gi is solvable iﬀ type-guarded,
monotone logic safety problem h∆, P D , Gi is solvable.

D.1 Elimination of type guards within monotone models
We now show that type-guarded existentials can be eliminated under the monotone semantics, that is: any instance
of the type-guarded monotone problem can be reduced to an instance of the ordinary monotone problem. The
obvious approach to this is to try to capture, using a formula, the class of relations deﬁned by a closed type. If H
is a goal term representing the class MnT o(∅), then a type guarded existential formula ∃x:T . G can be eliminated
in favour of an ordinary existential formula ∃x . H x ∧ G.

Goal deﬁnability. We say that a relation r ∈ Mnρo is goal term deﬁnable (more brieﬂy G-deﬁnable) just if there
exists a closed goal term ⊢ H : ρ and MnH o(∅) = r . We say that a class of relations is G-deﬁnable just if the
characteristic predicate of the class is G-deﬁnable. However, having made this precise, we can now observe that
it is not generally possible to capture the class of relations deﬁned by a type.
Lemma 11. The class of relations Mn(x:int → ohx ≡ 0 mod 2i) → ohfalseio(∅) is not G-deﬁnable.
Proof. This type, which we shall abbreviate by T , deﬁnes the predicate MnT o(∅) which contains r just if r is
false of every set of even integers (identifying the elements of Mnint → oo with sets of integers). However, this
predicate MnT o(∅) is not monotone and hence cannot be deﬁned by a goal term. Clearly, the empty relation
⊥ ∈ Mn(int → o) → oo is not an element of MnT o(∅), since it is false of every set of integers. However, ⊥ ⊆ ⊤,
the universal relation, and yet ⊤ is not in MnT o(∅)(⊤) since it assigns true to all sets of integers.         
This result makes it clear that although every r ∈ MnT o(∅) is itself monotone, the set of relations MnT o(∅),
viewed as a monadic predicate, may not be monotone.
   Despite the foregoing result, it is possible to eliminate type guards by representing their semantics logically.
Consider a type guarded formula ∃x:T . G. We can think of G as a monotone function of x, so, if G is true of some



                                                            32
relation r ∈ MnT o(∅) then it will also be true of any larger relation in MnT o(∅). Consequently, ∃x :T . G is true
iﬀ G is true of the largest relation in MnT o(∅), namely (following Lemma 7) MLT M(∅). Hence, we do not need
to represent the whole class of relations MnT o(∅) but only its largest member because, if H is a G-deﬁnition of
MLT M(∅), then we can eliminate ∃x:T G in favour of G[H /x], which is logically equivalent.

Deﬁnability of type complements and the relational semantics. In order to give a G-deﬁnition of the largest member
of a type MnT :: ρo(∅), it is useful to be able to give a G-deﬁnition of the complement of the type, i.e. the class that
contains r ∈ Mnρo just if r < MnT o(∅). This is because the largest element of a type T1 → T2 is a relation that, in
particular, is true of its argument s whenever s is not an element of MnT1 o(∅). In fact, the notions of complement
of T and largest element of T are here intertwined: To understand when a relation r is not in the type T1 → T2
you must understand when there exists a relation s ∈ MnT1 o(∅) such that r (s) is not in MnT2 o(∅). Since this
condition is a type-guarded existential, it follows from the above discussion that it can be re-expressed using the
largest element of MnT1 o(∅). This leads to the deﬁnitions by mutual induction on type:

         Com(ohφi) = λz. z ∧¬φ                                    Lar(G)(ohφi) = G ∨ φ
       Com(x:ι → T ) = λz. ∃x :ι. Com(T ) (z x)                Lar(G)(x:ι → T ) = λz. Lar(G)(T [z/x])
       Com(T1 → T2 ) = λz. Com(T2 ) (z Lar(false)(T1 ))        Lar(G)(T1 → T2 ) = λz. Lar(G ∨ Com(T1 ) z)(T2 )

in which Com(T ) is a G-deﬁnition of the complement of the class MnT o(∅). The deﬁnition of Lar is parametrised
by a goal formula representing domain conditions that are accumulated during the analysis of function types. It
follows that Lar(false)(T ) is a G-deﬁnition of the largest element of the class MnT o(∅).


Lemma 8. For any closed type ⊢ T :: ρ:
 (i) The goal term Com(T ) is a G-deﬁnition of the class {r ∈ Mnρo | r < MnT o(∅)}.
 (ii) The goal term Lar(false)(T ) is a G-deﬁnition of the relation MLT M(∅).
Proof. The following more general statement can be proven by a straightforward induction on ∆ ⊢ T :: ρ. For all
∆ ⊢ T :: ρ, α ∈ Mn∆o and goal formulas ∆ ⊢ G : o, MnCom(T )o(α) = {r ∈ Mnρo | r < MnT o(α)} and, for all d
of the appropriate sorts: MnLar(G)(T )o(α)(d) = 1 iﬀ MnGo(α) = 1 or MLT M(α)(d) = 1.                         
  With a G-deﬁnition of the largest element satisfying a type, we have the necessary apparatus to eliminate
type-guarded existentials. To this end, for each type guarded goal term G, let Elim(G) be deﬁned by:

                   Elim(x)      = x                             Elim(φ)      = φ
              Elim(λx:ι. G)     = λx:ι. Elim(G)           Elim(G 1 ∨ G 2 )   = Elim(G 1 ) ∨ Elim(G 2 )
             Elim(λx:ρ. G)      = λx:ρ. Elim(G)           Elim(G 1 ∧ G 2 )   = Elim(G 1 ) ∧ Elim(G 2 )
               Elim(G 1 N )     = Elim(G 1 ) N            Elim(∃x :T . G)    = Elim(G)[Lar(false)(T )/x]
               Elim(G 1 G 2 )   = Elim(G 1 ) Elim(G 2 )    Elim(∃x :ι. G)    = ∃x :ι. Elim(G)

and extend this to type guarded logic programs ⊢ P : ∆ by, for all x ∈ dom(∆), Elim(P)(x) = Elim(P(x)). It is
immediate that Elim(G) is a goal term not containing any type guarded existentials.
Example 5. We return to the motivating example of this section. Consider the type T , written explicitly as x:int →
y:int → ohx ≡ 0 mod 2 ⇒ y ≡ 0 mod 2i. It follows that Lar(false)(T ) = λxy. x ≡ 0 mod 2 ⇒ y ≡ 0 mod 2 and
Com(T ) = λz. ∃x. ∃y. z x y ∧x ≡ 0 mod 2 ∧y . 0 mod 2 (after a little simpliﬁcation). It is possible to express
that some goal term H : (int → int → o) → int → o is not an element of MnT → z:ι → ohz , 0io(∅) using the
goal term Com(T → z:ι → ohz , 0i) H . This term asserts that H violates the (relational formulation of the) property
of mapping eveness preserving functions to non-zero integers and is equivalent to:

                                   ∃z. H (λxy. x ≡ 0 mod 2 ⇒ y ≡ 0 mod 2) z ∧ z = 0

Here we use Com to assert directly the negation of the property represented by the type. However, as mentioned in the
discussion following the deﬁnition of Com, type guarded existentials are used implicitly. For example, it is easy to see
that this goal formula is logically equivalent to Elim(∃z 1: (T → z:ι → ohz , 0i). ∃z 2 . H z 1z 2 ∧ z 2 = 0).




                                                          33
   As sketched above, due to monotonicity the (ordinary) goal term Elim(G) obained from type-guarded goal term
G is logically equivalent to G. Consequently, there is no loss in performing the elimination: an instance of the
type-guarded monotone problem is solvable iﬀ the instance of the (ordinary) monotone problem obtained by
elimination is solvable. The proof follows the sketch outlined following Lemma 11.
Theorem 5. Type guarded, higher-order constrained Horn clause problem h∆, D, Gi is solvable iﬀ monotone logic
program safety problem h∆, Elim(P D ), Elim(G)i is solvable.
Since every existential quantiﬁer ∃ρ at relational sort can be viewed as an existential quantiﬁer ∃⊤::ρ guarded by
the top type ⊤ρ , it follows that, without loss of generality, one may assume that the latter problem contains only
existential quantiﬁcation over individuals. This justiﬁes the absence of relational sort existential quantiﬁers in the
type system of Section 5.




                                                         34
