                                                  Elaboration in Dependent Type Theory
arXiv:1505.04324v2 [cs.LO] 17 Dec 2015




                                                    Leonardo de Moura, Jeremy Avigad, Soonho Kong,
                                                                   and Cody Roux∗
                                                                         December 18, 2015


                                                                                Abstract
                                                    To be usable in practice, interactive theorem provers need to pro-
                                                vide convenient and efficient means of writing expressions, definitions,
                                                and proofs. This involves inferring information that is often left implicit
                                                in an ordinary mathematical text, and resolving ambiguities in mathemat-
                                                ical expressions. We refer to the process of passing from a quasi-formal
                                                and partially-specified expression to a completely precise formal one as
                                                elaboration. We describe an elaboration algorithm for dependent type
                                                theory that has been implemented in the Lean theorem prover. Lean’s
                                                elaborator supports higher-order unification, type class inference, ad hoc
                                                overloading, insertion of coercions, the use of tactics, and the computa-
                                                tional reduction of terms. The interactions between these components are
                                                subtle and complex, and the elaboration algorithm has been carefully de-
                                                signed to balance efficiency and usability. We describe the central design
                                                goals, and the means by which they are achieved.


                                         1      Introduction
                                         Just as programming languages run the spectrum from untyped languages like
                                         Lisp to strongly-typed functional programming languages like Haskell and ML,
                                         foundational systems for mathematics exhibit a range of diversity, from the
                                         untyped language of set theory to simple type theory and various versions of
                                         dependent type theory. Having a strongly typed language allows the user to
                                         convey the intent of an expression more compactly and efficiently, since a good
                                         deal of information can be inferred from type constraints. Moreover, a type
                                         discipline catches routine errors quickly and flags them in informative ways.
                                         But there is a downside: as we increasingly rely on types to serve our needs, the
                                         computational support that is needed to make sense of expressions in efficient
                                         and predictable ways becomes increasingly subtle and complex.
                                             Our goal here is to describe the elaboration algorithm used in a new inter-
                                         active theorem prover, Lean [10, 4]. Lean is based on an expressive dependent
                                             ∗ Avigad’s work partially supported by AFOSR FA9550-12-1-0370 and FA9550-15-1-0053.




                                                                                    1
type theory, allowing us to use a single language to define datatypes, mathemat-
ical objects, and functions, and also to express assertions and write proofs, in
accordance with the propositions-as-types paradigm. Thus, filling in the details
of a function definition and ensuring it is type correct is no different from filling
in the details of a proof and checking that it establishes the desired conclusion.
    The elaboration algorithm that we describe employs nonchronological back-
tracking, as well as heuristics for unfolding defined constants that are very effec-
tive in practice. Elaboration algorithms for dependent type theory are not well
documented in the literature, making the practice something of a dark art. We
therefore also hope to fill an expository gap, by describing the problem clearly
and presenting one solution.
    Lean’s elaborator is quite powerful. It solves not only first-order unification
problems, but nontrivial higher-order unification problems as well. It supports
the computational interpretation of terms in dependent type theory, reducing
expressions as necessary in the elaboration process. It supports ad hoc over-
loading of constants, and it can insert coercions automatically. It supports
a mechanism for type class inference in a manner that is integrated with the
other components of the elaboration procedure. It also supports interaction
with built-in and user-defined tactics. The interaction between the components
we have just enumerated is subtle and complex, and many pragmatic design
choices were made to attain efficience and usability.
    We start in Section 2 with an overview of the task of the elaborator, focusing
on its outward effects. In other words, we try to convey a sense of what the
elaborator is supposed to do. In Section 3, we explain the algorithm that is
used to achieve the desired results. We describe related work and draw some
conclusions in Section 4. Lean is an open-source project, and the source code is
freely available online.1 Many of the features discussed below are described in
greater detail in a tutorial introduction to Lean [4].


2      The elaboration task
What makes dependent type theory “dependent” is that types can depend on
elements of other types. Within the language, types themselves are terms, and
a function can return a type just as another function may return a natural num-
ber. Lean’s standard library is based on a version of the Calculus of Inductive
Constructions with Universes [9, 24, 18], as are formal developments in Coq [6]
and Matita [3]. We assume some familiarity with dependent type theory, and
provide only a brief overview here.
    Lean’s core syntax is based on a sequence of non-cumulative type universes
and Π-types. There is an infinite sequence of type universes Type0, Type1 ,
Type2, . . . , and any term t : Typei is intended to denote a type in the ith
universe. Each universe is closed under the formation of Π-types Πx : A, B,
where A and B are type-valued expressions, and B can depend on x. The idea is
that Πx : A, B denotes the type of functions f that map any element a : A
    1 http://leanprover.github.io




                                         2
to an element of B[a/x]. When x does not appear in B, the type Πx : A, B is
written A → B and denotes the usual non-dependent function space.
    Lean’s kernel can be instantiated in different ways. In the standard mode,
Type0 is distinguished by the fact that it is impredicative, which is to say,
Πx : A, B is an element of Prop for every B : Prop and every A. Elements
of Prop are intended to denote propositions. When Πx : A, B is in Prop, it
can also be written as ∀x : A, B, and it is interpreted as the proposition that
B holds for every element x of A. Given P : Prop, an element t : P can be
interpreted as a proof of P, under the propositions-as-types correspondence, or
more simply as “evidence” that P holds. Such a type P is proof-irrelevant, which
is to say, any two terms s, t : P are treated as definitionally equal by the
kernel.
    Lean also provides a predicative mode for homotopy type theory, without
any special treatment of Type0. The result is a version of Martin-Löf type
theory [20, 30] similar to the one used in Agda [7].
    In both standard and hott modes, the type universes are non-cumulative.
They are treated polymorphically, which is to say, there are explicit quantifi-
cations over universes. In practice, users generally write t : Type, leaving it
to Lean to insert an implicit universe variable and manage universe constraints
accordingly.
    Extensions to the core type theory inhabit a second layer of the kernel. Both
modes allow one to form inductive families [11], a mechanism that can be used
to define basic types like nat and bool, and common type-forming operations,
like Cartesian products, lists, Σ-types, and so on. Each inductive family dec-
laration generates a recursor (also known as the eliminator ). The standard
mode includes a mechanism for forming quotient types, and the mode for ho-
motopy type theory includes certain higher-inductive types [32]. We need not
be concerned with the precise details here, except to note that terms in depen-
dent type theory come with a computational interpretation. For example, given
t : B possibly depending on a variable x : A and s : A, the term (λx, t) s
reduces to t [s / x], the result of replacing x by s in t. Similarly, inductive
types support definition by recursion; for example, if one defines addition on
the natural numbers by structural recursion on the second argument, t + 0
reduces to t. The kernel type checker should identify terms that are equivalent
under the induced equivalence relation, and, as much as possible, the elaborator
should take this equivalence into account when inferring missing information.
We discuss this further in Section 2.3.

2.1    Type inference and implicit arguments
The task of the elaborator, put simply, is to convert a partially specified ex-
pression into a fully specified, type-correct term. For example, in Lean, one can
define a function do_twice as follows:
  definition do_twice (f : N → N) (x : N) : N := f (f x)



                                       3
One can omit any two of the three type annotations, leaving it to the elaborator
to infer the missing information. Inferring types like these can be seen as a
generalization of the Hindley-Milner algorithm [16, 23], which takes an unsigned
term in the λ-calculus and assigns a simple type to it, if one exists.
    When entering a term, a user can leave an argument implicit by inserting an
underscore, leaving it to the elaborator to infer a suitable value. One can also
mark function arguments as implicit by declaring them using curly brackets
when defining the function, to indicate that they should be inferred rather
than entered explicitly. For example, we can define the append function, which
concatenates two lists, so that it has the following type:
  append : Π {A : Type}, list A → list A → list A
Users can then write append l1 l2 rather than append A l1 l2 , leaving Lean
to infer the first argument.

2.2    Higher-order unification
Many of the constraint problems that arise in type inference and the synthesis of
implicit arguments are easily solved using first-order unification. For example,
suppose a user writes append l1 l2 , where l1 can be seen to have type list
T. Temporarily naming the implicit argument to append as ?M, we see that next
argument to append should have type list ?M. Given that l1 in fact has type
list T, we easily infer ?M = T.
    Nevertheless, it is often the case that the elaborator is required to infer an
element of a Π-type, which constitutes a higher-order unification problem. For
example, if e : a = b is a proof of the equality of two terms of some type A,
and H : P is a proof of some expression involving a, then the term subst e H
denotes a proof of the result of replacing some or all of the occurrences of a
in P with b. Here, in addition to inferring the type A, we also need to infer an
expression T : A → Prop denoting the context for the substitution, that is, the
expression with the property that T a is convertible to P. Such an expression is
inherently ambiguous; for example, if H has type R (f a a) a, then with subst
e H the user may have in mind R (f b b) b or R (f a b) a or something else,
and the elaborator has to rely on context and a backtracking search to find an
interpretation that fits. Similar issues arise with proofs by induction, which
require the system to infer an induction predicate.
    The need for higher-order unification even arises with common datatypes.
For example, the type Σx : A, B denotes the type of dependent pairs ha, bi,
where a : A and b : B a. Here B is in general a function A → Type. In the
notation ha, bi, the arguments A and B are left implicit. The argument A can
easily be inferred from the type of A, but the type of b will generally be an
expression that involves a as an argument. In this case, higher-order unification
is used to infer B.
    Even second-order unification is known to be generally undecidable [13],
but the elaborator merely needs to perform well on instances that come up in



                                        4
practice. For example, in Lean, users can import the notation H ⊲ H’ for subst
H H’. If we have proved
  theorem mul_mod_mul_left {z : N} (x y : N) (zpos : z > 0) :
          (z * x) mod (z * y) = z * (x mod y)
we can then write
  theorem mul_mod_mul_right (x z y : N) :
          (x * z) mod (y * z) = (x mod y) * z :=
  !mul.comm ⊲ !mul.comm ⊲ !mul.comm ⊲ !mul_mod_mul_left
The proof applies the commutativity of multiplication three times to an appro-
priate instance of the theorem mul_mod_mul_left. (The symbol ! indicates
that all arguments should be synthesized by the elaborator.) The unifier can
similarly handle nested inductions and iterated recursion.
  theorem add.comm (n m : N) : n + m = m + n :=
  nat.induction_on m
   (nat.induction_on n rfl
     (take n, assume IH : n = 0 + n,
       show succ n = succ (0 + n), from IH ⊲ rfl))
     -- induction step omitted
Or, in the context of homotopy type theory, where equality proofs are relevant,
we can write:
  definition concat_assoc (p : x = y) (q : y = z) (r : z = t) :
             p · (q · r) = (p · q) · r :=
  eq.rec_on r (eq.rec_on q idp)
Here rec_on denotes a form of recursion which, like induction, has to infer the
relevant predicate.
     We will see below that higher-order unification is a complex process, and
places a high burden on the elaborator. It should thus be used sparingly. But
it is often convenient and sometimes unavoidable, so it is important that it can
be handled by the elaboration algorithm.

2.3    Computational behavior
The elaborator should also respect the computational interpretation of terms.
It should, for instance, recognize the equivalence of the terms (λx, t) s and
t[s/x], as well as hs, ti.1 (denoting the first projection of the pair) and s
under the relevant reduction rule for pairs. Elements of inductive types also
have computational behavior; on the natural numbers, 2 + 2 and 4 are both
definitionally equal to succ (succ (succ (succ 0))), x + 0 is definitionally
equal to x, and x + 1 is definitionally equal to succ x. The elaborator should
also support unfolding definitions where necessary: for example, if x - y is
defined as x + (-y), the elaborator should allow us to use the commutativity
of addition to rewrite x - y to -y + x. Unfolding definitions and reducing


                                       5
projections is especially crucial when working with algebraic structures, where
many basic expressions cannot even be seen to be type correct without carrying
out such reductions. For example, given a : A and b : B a, the left-hand side
of the expression ha, bi.2 = b has type B (ha, bi.1) and the right-hand side
has type B a. Both the elaborator and the type checker need to recognize these
types as the same.
    Determining when to unfold defined constants is a crucial part of the practice
of theorem proving. It is therefore unsurprising that the naive approach of
performing all such unfoldings leads to unacceptable performance, and it is
an important aspect of building a practical elaboration procedure to design
heuristics that limit unfolding to situations that require it. Lean allows users
to annotate definitions, providing hints to the elaborator, as follows:
   • An irreducible definition will never be unfolded during higher-order uni-
     fication (but can still be unfolded in other situations, for example during
     type checking).
   • A reducible definition will be always eligible for unfolding.
   • A semireducible definition can be unfolded during simple decisions and
     won’t be unfolded during complex decisions.
For example, users can mark definitions which ought to be viewed as abbrevi-
ations as reducible. The meaning of these annotations is discussed further in
Section 3.3. These annotations are used only by the elaborator; they have no
bearing at all when it comes to checking the type of a fully elaborated term. As
a result, the user can modify these annotations at any time, as needed, when
developing a theory.

2.4    Type classes
Lean supports the use of Haskell-style type classes [15]. For example, we can
define a class has_mul A of types A with an associated multiplication as follows:
  structure has_mul [class] (A : Type) := (mul : A → A → A)
In other words, for every type A, has_mul A is a record with one element,
has_mul.mul, which we should think of as a multiplication operation on A.
We then define the generic multiplication operation,
  definition mul {A : Type} [s : has_mul A] : A → A → A :=
  has_mul.mul
and the notation
  infix * := mul
The square brackets indicate that the argument s is implicit, and that the
relevant instance of has_mul A should be synthesized by the class inference
mechanism. We can declare a particular instance as follows:


                                        6
  definition nat_has_mul [instance] : has_mul nat :=
  has_mul.mk nat.mul
Suppose the user writes s * t, when s is inferred to have type nat. When
the elaborator is called to solve ?M : has_mul nat, it finds nat_has_mul on a
stored list of instances, and assigns that to ?M.
    Instance declarations themselves can have implicit class arguments, in which
case, class inference performs a backward-chaining Prolog-like search. For ex-
ample, we can declare
  structure semigroup [class] (A : Type) extends has_mul A :=
  (mul_assoc : ∀a b c, mul (mul a b) c = mul a (mul b c))
The structure declaration above automatically declares semigroup to be an
instance of has_mul, so that if, instead, nat was only declared to be an instance
of semigroup, class inference could synthesize the instance of has_mul nat in
two steps. We then get the generic theorem mul.assoc in the same way we
obtained the generic notation for multiplication.
    We can then go on to define monoids, groups, rings, and commutative ver-
sions. The structure command supports the construction of the algebraic
hierarchy by allowing the user to extend and merge multiple structures:
  structure group [class] (A : Type)
            extends monoid A, has_inv A :=
  (mul_left_inv : ∀a, mul (inv a) a = one)
Users can also rename structure components on the fly. In the following example,
type class inference finds the appropriate inverse and instance of the theorem
inv_inv when processing eq_inv_of_eq_inv:
  theorem inv_inv {A : Type} [s : group A] (a : A) :
          (a−1 )−1 = a :=
  ...

  theorem eq_inv_of_eq_inv {A : Type} [s : group A] {a b : A}
                           (H : a = b−1 ) : b = a−1 :=
  by rewrite [H, inv_inv]
Here, the rewrite tactic replaces a by b−1 in the goal, and then rewrites
(b−1 )−1 to b. Since any group is an instance of a monoid and any monoid
is an instance of a semigroup, generic theorems about semigroups and monoids
can be applied to any group. The type class inference is seamless integrated in
all proof procedures implemented in Lean. We remark that the theorem above
can be proved without any user guidance using these procedures.
    We can also declare so called fully bundled structures in the style of the
Mathematical Components library [12]. For example:
  structure Group := (carrier : Type) (struct : group carrier)

  attribute Group.carrier [coercion]
  attribute Group.struct [instance]

                                       7
This means that whenever we have G : Group, we can write g : G, and G is
coerced to its carrier type. And whenever we have g : carrier G, type class
resolution can infer that struct G is the relevant group structure on carrier
G.
    In Lean, type classes can be used to infer not only notation and generic
facts, but fairly complex data. For example, in the standard library, we define
the class of propositions that are decidable:
  inductive decidable [class] (p : Prop) : Type :=
  | inl : p → decidable p
  | inr : ¬p → decidable p
Logically speaking, since decidable p lives in Type rather than Prop, having an
element t : decidable p is more informative than having an element t : p
∨ ¬p; it enables us to define values of an arbitrary type depending on the truth
value of p. This distinction is only useful in constructive mathematics, because
classically every proposition is decidable. But the decidable class allows for
a smooth transition between constructive and classical logic, allowing classical
reasoning in suitable constructive settings as well. It is especially relevant for
users interested in defining computable functions. In Lean, (if c then t else
e) is notation for (ite c t e), where ite is defined as:
  definition ite (c : Prop) [H : decidable c] {A : Type}
                 (t e : A) : A :=
  decidable.rec_on H (λ Hc, t) (λ Hnc, e)
Note that the implicit argument H is automatically synthesized by type class
inference. Moreover, the expression if c then t else e computes whenever
c is a decidable proposition.
    For example, we can prove, constructively, that equality on the natural num-
bers is decidable:
  nat.decidable_eq [instance] : ∀ x y : nat, decidable (x = y)
We can do the same for inequality relations on nat, and moreover show that
decidability is preserved under boolean operations and bounded quantification.
We moreover make the following definitions:
  definition is_true (c : Prop) [H : decidable c] : Prop :=
  if c then true else false

  definition of_is_true {c : Prop} [H1 : decidable c]
                        (H2 : is_true c) : c :=
  decidable.rec_on H1 (λ Hc, Hc)
                      (λ Hnc, !false.rec (if_neg Hnc ⊲ H2 ))

  notation ‘dec_trivial‘ := of_is_true trivial
What is going on here is subtle. The expression is_true c infers a decision
procedure for c, and returns either true or false. Assuming H2 : is_true c,

                                        8
of_is_true H2 is a proof of c. But if is_true c evaluates to true, it has the
canonical proof trivial. Thus, given a proposition c, the notation dec_trivial
does the following:
   • infers a decision procedure for c, and
   • tries to use trivial to prove is_true c.
If it succeeds — that is, if the resulting term type checks — the result is a proof
of c.
     With these definitions, we can write the following proof:
  example : ∀ x : nat, x < 10 → x 6= 10 ∧ x < 12 := dec_trivial
Type class resolution infers the decision procedure for the proposition in ques-
tion, and computational reduction evaluates it. Problems like this can appear
anywhere in a proof or an expression, and type class inference will solve them
at appropriate times within the elaboration process.

2.5    Overloading
We have seen that the standard library relies on type class inference to support
the use arithmetic operations like + and * for different number classes. This
is sometimes known as parametric polymorphism. Lean also supports ad hoc
polymorphism by allowing us to overload identifiers and notation. For example,
the notation ++ is used for concatenation of both lists and tuples:
  import data.list data.tuple
  open list tuple

  variables (A : Type) (m n : N)
  variables (v : tuple A m) (w : tuple A n) (s t : list A)

  check s ++ t
  check v ++ w
Where it is necessary to disambiguate, Lean allows us to precede an expression
with the notation #<namespace>, to specify the namespace in which notation is
to be interpreted.
  check λ x y, (#list x + y)
  check λ x y, (#tuples x + y)
    We can also overload identifiers. Every identifier in Lean has a full name
that is unique, but identifiers can be grouped into namespaces, and opening the
namespace produces a shorter alias. For example, if we define foo in namepsaces
a and b, we obtain identifiers named a.foo and b.foo respectively. If we open
both namespaces, however, the alias foo is an overloaded reference to both,
leaving the elaborator to resolve the ambiguity.



                                        9
   Ad hoc overloading is more flexible than type class overloading, in that the
overloaded constants can denote entirely different kinds of objects. It adds
ambiguity and choice points to the elaboration process, and should therefore
be used sparingly. But it is often useful, especially when we want to reuse
notation for expressions that do not have the same shape. For example, in
the Lean standard library, we use −1 above to denote the inverse function for
algebraic structures that support it, as well as for the symmetry operation for
equalities. It can also be used to invert bijections, used group isomorphisms, ring
isomorphisms, isomorphisms in a category, or equivalences between categories.

2.6    Coercions
The treatment of coercions in Lean is as one would expect. One can, for example,
coerce a bool to a nat and a nat to an int, and Lean will insert coercions in
list expressions [n, i, m, j] and [i, n, j, m] when n and m have type nat
and i and j have type int. One can also coerce axiomatic structures, so that
the user can provide a group as input anywhere a semigroup is expected. One
can also coerce from a suitable family of types to Type or to a Π-type.
    In fact, just as in Coq, Lean allows us to declare three kinds of coercions:

   • from a family of types to another family of types
   • from a family of types to the class of sorts
   • from a family of types to the class of function types
The first kind of coercion allows us to view any element of a member of the
source family as an element of a corresponding member of the target family.
The second kind of coercion allows us to view any element of a member of the
source family as a type. The third kind of coercion allows us to view any element
of the source family as a function. For details, see [4].

2.7    Tactics and structuring mechanisms
Finally, definitions and proofs can invoke tactics, that is, user-defined or built-
in proof-finding procedures that construct various subterms. The constraint
solver described in this paper invokes user provided tactics to construct terms
that cannot be synthesized by solving unification constraints and type class
resolution. Lean’s tactic language is similar to those found in other LCF-style
theorem provers. Describing the tactic language here would take us too far
afield; we only wish to point out that our implementation makes the use of
tactics continuous with the act of writing terms. Anywhere a term is expected,
a user can used the keywords begin and end to enter a tactic block:
  theorem test (p q : Prop) (Hp : p) (Hq : q) : p ∧ q ∧ p :=
  begin
    apply and.intro,
    exact Hp,


                                        10
    apply and.intro,
    exact Hq,
    exact Hp
  end
One-line tactic proofs can be specified with the keyword by:
  theorem test (p q : Prop) (Hp : p) (Hq : q) : p ∧ q ∧ p :=
  by apply (and.intro Hp); exact (and.intro Hq Hp)
Conversely, when in tactic mode, one can use the exact tactic to specify an
explicit term, as in the example above. The keywords have and show make it
possible to do that in an elegant and structured way.
  theorem card_image_eq_of_inj_on {f : A → B} {s : finset A}
                                  (H1 : inj_on f (ts s)) :
          card (image f s) = card s :=
  begin
    induction s with a t H IH,
     {rewrite [card_empty]},
     {have H2 : ts t ⊆ ts (insert a t),
        by rewrite [-subset_eq_to_set_subset];
          apply subset_insert,
      have H3 : card (image f t) = card t,
        from IH (inj_on_of_inj_on_of_subset H1 H2),
      have H4 : f a ∈
                    / image f t,
        from ..., -- proof suppressed
      show card (image f (insert a t)) = card (insert a t),
        from ... -- proof suppressed}
  end
Thus one can pass freely between the two modes. This yields a tradeoff between
two different strategies for elaboration: tactics build an expression using local
information in a surgical way, whereas the elaborator solves constraints involving
global information, spread out across the entire term.
    The availability of tactic mode also provides a convenient way of sectioning
long proof terms: the construct proof t qed is syntactic sugar for by+ exact
t. Including this in a long proof terms forces the elaborator to process the
surrounding expression independent of t, and then process t, separately, using
information from the surrounding term. Thus we can treat the processing of a
long proof as one large elaboration problem or the composition of smaller ones,
balancing the advantages of the local and global approaches in a convenient and
flexible way.

2.8    Combining the various components
Any given definition or theorem in Lean can draw on many of the features just
described. Consider the following, which defines the composition of two natural


                                       11
transformations between functors (and establishes that it is, indeed, a natural
transformation):
    variables {C D : Category} {F G H : C ⇒ D}

    definition nt_compose (η : G =⇒ H) (θ : F =⇒ G) : F =⇒ H :=
    natural_transformation.mk
      (take a, η a ◦ θ a)
      (take a b f, calc
        H f ◦ (η a ◦ θ a) = (H f ◦ η a) ◦ θ a : assoc
                      ... = (η b ◦ G f) ◦ θ a : naturality
                      ... = η b ◦ (G f ◦ θ a) : assoc
                      ... = η b ◦ (θ b ◦ F f) : naturality
                      ... = (η b ◦ θ b) ◦ F f : assoc)
Here the functors F, G, and H are coerced to their action on morphisms, and
the natural transformations η and θ are coerced to their first component. The
composition symbol ◦ for functions is overloaded to denote composition of mor-
phisms as well, and type class inference infers the category in which the compo-
sition takes place. The appropriate substitution contexts in the calculation are
inferred, as are the arguments to the theorems that are invoked.
    The interactions between the components of the elaboration task are subtle,
and the challenge is to deal with them all at the same time. A definition or
proof may give rise to hundreds of constraints requiring a mixture of higher-
order unification, disambiguation of overloaded symbols, insertion of coercions,
type class inference, and computational reduction. The net effect is then a
difficult constraint-solving problem with a combinatorial explosion of options.
Lean’s elaborator manages to solve such problems, and it is quite fast. (See, for
example, the data presented at the end of Section 3.3.) In the next section, we
explain how the elaborator processes the constraints and navigates the search
space in an effort to balance completeness and efficiency.


3     The elaboration procedure
3.1    Overview
Section 2 describes what we want the elaboration algorithm to do. It needs to
infer types and implicit arguments in expressions, including sometimes higher-
order functions and predicates. It needs to support type class inference that is
robust enough to work with structures in an algebraic hierachy an a uniform
and convenient way. It needs to dismabiguate overloaded notation and iden-
tifiers, and it needs to insert coercions where appropriate. Moreover, it needs
to respect the computational behavior of expressions while performing all these
tasks, since, in general, the constraints can only be solved up to equivalence of
terms. The goal of this section is to describe an algorithm that does this.
     The task of Lean’s parser, which we do not describe here, is to convert a
user’s input to a preterm, a formal but incomplete reflection of that input. The

                                       12
process for getting from a preterm to a fully elaborated term has two main
steps: preprocessing and constraint resolution. The preprocessing phase takes
a preterm and creates a partially specified term, with “holes,” or metavari-
ables, representing the information that needs to be inferred. At the same time,
the preprocesor generates a list of constraints that these metavariables need to
satisfy. Some of the constraints are unification constraints, for example, the
constraint that the type of an argument to a function matches the function’s
argument type. Others are choice constraints, for example, that an inferred
value is among a finite set of possible overloads. Finally, after all constraints
have been solved, Lean invokes the tactic blocks associated with the remaining
holes to produce the terms necessary to fill them. This is a recursive procedure
because some tactics may contain nested preterms that must be also elaborated,
and these preterms may additional tactic blocks, and so on.
    The constraint resolution phase aims to find a consistent solution to all the
unification and choice constraints. Heuristically, “straightforward” constraints
should be solved first, providing useful information to guide the rest of the
search. Choice points result in backtracking, which needs to be handled carefully
to avoid duplication of work. Failures need to be carefully tracked in order to
provide informative error messages to the user.
    The simple division into the preprocessing phase and constraint resolution
phase is slightly too simplistic: even the preprocessing phase has to process
and simplify constraints, in order to detect the possibility of inserting a coer-
cion. Thus both phases make use of a constraint simplification procedure that
performs preliminary reductions.
    We spell out the details below. Sections 3.2 and 3.3 describe the main
data structures and some of the support functions used by the algorithm, and
Section 3.4 describes the constraint simplification procedure. The preprocessing
step is described in Section 3.5, and the constraint solving procedure, which is
both the heart of the elaboration algorithm and the most complex component,
is described in Sections 3.6 and 3.7.

3.2     Main data structures
In this section, we describe the term representation and the main data structures
used in our elaboration procedure. We assume the term language is a dependent
λ-calculus in which terms are described by the following grammar:

             t, s = ℓ | x | f | ?m | Type u | t s | λx : s, t | Πx : s, t

where
   • ℓ a free variable (also called a local constant)
   • x is a bound variable
   • f is a constant (parametrized by a list of universe terms)
   • ?m is a metavariable

                                         13
   • u is a universe term
     We adopt a locally nameless variable binding style: free variables have a
unique identifier and a type, while bound variables are simply represented by a
number, a de Bruijn index. We store the type with each free variable, thereby
removing the need to carry around contexts in the type checker and normal-
izer. As described in [21], this representation style simplifies the implementation
considerably, as it minimizes the number of places where explicit calculations
with de Bruijn indices must be performed. We use the notation t[x := s] to
represent the substitution of x for s in t, where x is a bound variable, free vari-
able, or metavariable. When x is a bound variable, the operation also lowers
all bound variables with index greater than x. We use t to denote sequence of
terms t1 . . . tn , and x : A for the telescope (x1 : A1 ) . . . (xn : An ), where Ai
may depend on xj for j < i.
     While the locally nameless approach simplifies many aspects of the code, the
operations of abstracting and instantiating variables can be costly. Fortunately,
we found a simple optimization that completely eliminates any performance
concerns. The problem, and our solution, are described at the end of Section 3.3.
     An environment stores a sequence of declarations. The Lean kernel supports
three different kinds of declarations: axioms, definitions and inductive families.
Each has a unique identifier, and can be parametrized by a sequence of universe
parameters. Every axiom has a type, and every definition has a type and a
value. A constant is just a reference to a declaration.
     A user’s input to the elaborator can generally be viewed as partial construc-
tions, i.e., constructions containing holes that must be filled by the system.
Internally, each hole is represented by a metavariable. Each metavariable has a
unique identifier and a type. The main operation on metavariables is instantia-
tion. In our implementation, only closed terms can be assigned to metavari-
ables. This design decision guarantees that operations such as β-reduction
and metavariable instantiation commute. Since only closed terms can be as-
signed to metavariables, on creation a metavariable is applied to the variables
in the context where it appears. For example, we encode a hole in the context
(x : A) (y : B) as ?m x y, where ?m is a fresh metavariable. The type of ?m is
Π(x : A) (y : B), C, where C is the expected type for the hole at that position.
If the expected type is also unknown at preprocessing time, we create another
fresh metavariable ?mt : Π(x : A) (y : B), Type ?u, where ?u is a fresh universe
metavariable. This gives us ?m : Π(x : A) (y : B), ?mt x y. We say a term is
fully elaborated if it does not contain metavariables.
     We say a term is β-reducible if it is of the form (λx : A, s)t, and ι-reducible
if it is of the form C.rec s (C.mki r) t, where C.rec is the recursor/eliminator
for an inductive datatype C. Here, the sequence s represents the parameters,
minor premises and indices, and (C.mki r) is the main premise (where C.mki
is the i-th constructor of C). The function reduceβι s applies head β and ι
reduction to s. We say a term t is stuck if computation cannot occur without
instantiating a metavariable ?m, where (?m s) is a sub-term of t. In that case,
we say (?m s) is the reason for t being stuck. More formally, a term is stuck


                                         14
when the head symbol is a metavariable (i.e., it is of the form ?m s), or it is a
recursor application where the main premise is stuck. We say the first case is a
stuck application, and the second a stuck recursor.
    During the preprocessing step, unification and choice constraints are gener-
ated. Unification constraints are used to enforce typing constraints, and choice
constraints are for overloading, coercion resolution, and triggering the type class
mechanism.
    A unification constraint t ≈ s is annotated with a justification, which rep-
resent the facts and assumptions that gave rise to the constraint. Justifications
are used to assist the generation of error messages when a term fails to be elabo-
rated, and to implement non-chronological backtracking [25]. Non-chronological
backtracking allows exploring the (possibly infinite) tree of potential solutions
more efficiently, by eliminating branches which we know cannot possibly contain
an actual solution.
    There are three kinds of justifications: asserted, assumption and join. An
asserted justification is used to annotate constraints generated during the pre-
processing phase. Whenever the solver has to perform a choice (also known as
a case split ), it annotates each choice with a fresh assumption. A join justifi-
cation j1 ⊲⊳ j2 represents the “union” of the justifications j1 and j2 . We use
ht ≈ s, ji to denote the unification constraint justified by j. A substitution
is a finite collection of assignments from metavariables to pairs ht, ji, written
?m 7→ ht, ji, where t is a closed term and j is a justification for the assignment.
Assignments are generated when solving unification constraints. For example,
the constraint h?m ≈ t, ji is solved by adding the assignment ?m 7→ ht, ji.
Whenever we apply a substitution we use a join justification to track its effect.
For example, the result of applying the assignment ?m 7→ ht, jm i over the con-
straint hr ≈ s, ji is the new constraint hr[?m := t] ≈ s[?m := t], j ⊲⊳ jm i. We
also use hs ≈ t, j1 i ⊲⊳ j2 to denote the constraint hs ≈ t, j1 ⊲⊳ j2 i. Moreover, if
a is a list of constraints [c1 , . . . , cn ], a ⊲⊳ j is [c1 ⊲⊳ j, . . . , cn ⊲⊳ j].
    A choice constraint is of the form h?m ℓ : t in f, ji, where:
   • ?m is a metavariable,
   • ℓ are free variables representing the context where ?m was created,
   • t is the type of ?m ℓ, and
   • f is a procedure that, given the term ?m ℓ, its type t, and a substitu-
     tion, produces a (possibly unbounded) stream of constraints representing
     possible ways of synthesizing ?m, and a justification j.
Note that each alternative is itself a list of constraints, and is not necessarily
just a single unification constraint.
    Whereas some constraints should be solved eagerly, other constraints should
be solved only when there is sufficient information to process them in a reliable
way. To that end, a choice constraint ?m ℓ : t in f may be marked as onde-
mand. When the flag ondemand is set, the constraint solver will try to invoke
function f only after all metavariables in t have been instantiated. We say a

                                         15
ondemand choice constraint is ready when t does not contain metavariables,
and postponed otherwise. We will later describe how this feature is used to
implement the type class mechanism and coercions. If a choice constraint is not
marked as ondemand, we say it is a regular choice constraint. We use regular
choice constraints to specify overloaded symbols. The result of applying the
assignment ?m 7→ hs, jm i over the choice constraint h?n ℓ : t in f, ji is the new
constraint h?n ℓ : t[?m := s] in f, j ⊲⊳ jm i. We also use the notation c ⊲⊳ j
when c is a choice constraint.

3.3    Support functions
In this section, we describe some auxiliary functions that are used throughout
the elaboration algorithm.
    The function typeof r returns the inferred type of a term r, where r may
contain metavariables. Specifically, it returns a pair ht, Si where t is the type
of r and S is a set of constraints on the metavariables. If r does not contain
metavariables, then S is empty.
    Given (ℓ1 : A1 ) . . . (ℓn : An ), the operation abstractλ [ℓ1 . . . ℓn ] t returns

 λ(x1 : A1 ) . . . (xn : An [ℓ1 := x1 , . . . , ℓn−1 := xn−1 ]), t[ℓ1 := x1 , . . . , ℓn := xn ]

We also have abstractΠ , the equivalent operation for Π-abstraction.
    The function unfold (f t1 . . . tn ) applies a δ-reduction, i.e. it unfolds the
definition of constant f . In practice, however, it is not feasible to apply δ-
reduction to all constants in a constraint solving problem. To cope with this
performance issue, we allow the user to annotate definitions with the hints ir-
reducible, semireducible or reducible, as described in Section 2.3. Recall that an
irreducible definition is never unfolded by the constraint solver, while a semire-
ducible or reducible definition may be unfolded or not depending on the con-
straint being solved. Roughly, a semireducible definition is unfolded only if the
decision to unfold is “simple,” which is to say, if the unfolding does not require
the procedure to consider an extra case split. When a decision is not simple,
the unfolding produces at least one extra case, and consequently increases the
search space. When no annotation is provided, the system assumes the defini-
tion is semireducible. Note that when the kernel type checks fully elaborated
definitions, these annotations are ignored; they are only relevant during the
elaboration process.
    The function whnf r returns a pair hw, Si where w is a term convertible
to r that is in weak head normal form (whnf ) or is stuck, and S is a set of
unification constraints. (In this paper, we can assume the set S returned by
whnf is always empty. In our implementation, constraints in S arise because
the elimination rule for equality has extra computational reductions when proof
irrelevance is enabled, corresponding to Streicher’s axiom K [29]. Specifically,
given H1 : a = a, the term eq.rec A a C a H2 H1 reduces to H2 even when
H1 is not the constructor eq.refl A a, where eq.rec is the recursor for the
Leibniz equality. To that end, the elaborator has to infer the type of H1 , which


                                               16
can give rise to unification constraints.) The function whnf does not unfold
irreducible definitions, and during type class resolution, it also does not unfold
semireducible ones.
    The procedure error j throws an exception tagged with a justification j.
    Finally, the function ensurefun s j ensures that s has a function type.
Specifically, it infers the type t of s (using typeof) and then reduces t to t′
in weak head normal form. If t′ is a Π-term, then it returns t′ and any new
unification constraints. If t′ is not a Π-term and is not stuck, then it generates an
error with justification j. Otherwise, if ?m s is the reason that t′ is stuck, where
?m : (Πx : A, B), we create two fresh metavariables: ?m1 : (Πx : A, Type ?u1 )
and ?m2 : (Π(x : A) (y : ?m1 x), Type ?u2 ), and the new constraint

                          ht ≈ (Πx : ?m1 s, ?m2 s x), ji.

This ensures that s has a function type, and defers the problem of figuring out
what that type is.
    Recall that we use the local nameless approach for representing terms, in
which free variables have a unique identifier and a type, while bound variables
are represented by a de Bruijn index. We say a term t has a dangling bound
variable if there is a bound variable in t that is not in the scope of any λ/Π-
expression binding it. For example, the λ-expression λx : Type, f x (g x) has
no dangling bound variables, but x is a dangling bound variable in f x (g x).
In the locally nameless approach, all major operations (such as type inference,
normalization, and unification) assume there are no dangling bound variables,
that is, no bound variables that “point out of the scope.” This invariant is
enforced by replacing bound variables with fresh free variables whenever we
visit the body of a λ/Π-expression. In the lambda expression above, we would
replace x in f x (g x) with the free variable ℓ : T ype. This operation is called
instantiate in [21]. The operation abstract ℓ t is the inverse; it replaces the
free variable ℓ in t with the bound variable with de Bruijn index 0. These two
operations are essentially the only ones that have to deal with de Bruijn indices.
    Although the locally nameless approach greatly simplifies the implementa-
tion effort, there is a performance penalty. Given a term t of size n with m
binders, it takes O(nm) time to visit t while making sure there are no dangling
bound variables. In [21], the authors suggest that this cost can be minimized by
generalizing abstract and instantiate to process sequences of free and bound
variables. This optimization is particularly effective when visiting terms con-
taining several consecutive binders, such as λx1 : A1 , λx2 : A2 , . . . , λxn : An , t.
Nonetheless, we observed that these two operations were still a performance
bottleneck for several files in the Lean standard library. We have addressed
this problem using a very simple complementary optimization. For each term
t, we store a bound B such that all de Bruijn indices occurring in t are in the
range [0, B). This bound can easily be computed when we create new terms:
the bound for the de Bruijn variable with index n is n + 1, and given terms t
and s with bounds Bt and Bs respectively, the bound for the application (t s) is
max(Bt , Bs ), and the bound for (λx : t, s) is max(Bt , Bs − 1). We use the bound


                                          17
B to optimize the instantiate operation. The idea is simple: B enables us to
decide quickly whether any subterm contains a bound variable being instanti-
ated or not. If it does not, then our instantiate procedure does not even visit
the subterm. Similarly, for each term t, we store a bit that is set to “true” if
and only if t contains a free variable. We use this bit to optimize the abstract
operation, since it enables us to decide quickly whether a subterm contains a
free variable.
    These optimizations are crucial to our implementation. The Lean standard
library currently contains 172 files, and 41,700 lines of Lean code. With the
optimizations, the whole library can be compiled in 71.06 seconds using an Intel
Core i7 3.6Ghz processor with 32Gb of memory. Without the optimizations, it
takes 2,189.97 seconds to compile the same set of files.

3.4    The constraint simplification procedure
The preprocessing step and the constraint-solving procedure rely on a constraint-
simplification procedure, which we now describe. The idea of the simp procedure
is to decompose all the constraints that can “straightforwardly” be decomposed
to simpler ones, and to detect quickly any constraints that simply cannot be
solved. Thus, given a unification constraint, the simp procedure produces a set
of (potentially) simpler unification constraints or throws an error. Moreover,
if the input constraint does not contain metavariables, then the result is the
empty set {} or an error.
    In the pseudocode below, s and t denote arbitrary terms, ℓ is a free vari-
able, and f and g are constants. The procedure mklocal A creates a fresh
free variable with type A. To simplify the presentation, we assume there is
a global unique name generator. The function depth f returns the defini-
tion depth of the constant f , which is equal to 0 if f is not a definition, and
1 + max{depth g | g appears in the definition of f } otherwise. To save space, we
do not list symmetric cases; for example, we present a case for hs ≈ (λx : B, t), ji
but not h(λx : B, t) ≈ s, ji.

simp ht ≈ t, ji                                  = {}
simp hs ≈ t, ji when s is β/ι-reducible = simp     Sn hreduceβι s ≈ t, ji
simp hℓ s1 . . . sn ≈ ℓ t1 . . . tn , ji         = i=1 simp hsi ≈ ti , ji
simp hf s1 . . . sn ≈ f t1 . . . tn , ji         =
   if s1 . . . sn and t1 . . . tn do not contain metavariables then
       simp (hunfold (f s1 . . . sn ) ≈Sunfold (f t1 . . . tn ), ji)
   else if f is not reducible then ni=1 simp hsi ≈ ti , ji
   else {hf s1 . . . sn ≈ f t1 . . . tn , ji}
simp hf s ≈ g t, ji                              =
   if depth f > depth g and f is not irreducible then
       simp (hunfold (f s) ≈ g t, ji)
   else if depth f < depth g and g is not irreducible then
       simp (hf s ≈ unfold (g t), ji)
   else if depth f = depth g and f and g are not irreducible then


                                        18
       simp (hunfold (f s) ≈ unfold (g t), ji)
simp h(λx : A, s) ≈ (λy : B, t), ji          =
   let ℓ = mklocal A in simp hA ≈ B, ji ∪ simp hs[x := ℓ] ≈ t[y := ℓ], ji
simp h(Πx : A, s) ≈ (Πy : B, t), ji          =
   let ℓ = mklocal A in simp hA ≈ B, ji ∪ simp hs[x := ℓ] ≈ t[y := ℓ], ji
simp hs ≈ (λx : B, t), ji                    =
   let h(Πx : A, C), Si = ensurefun s j in
       simp h(λx : A, s x) ≈ (λx : B, t), ji ∪ S
simp hs ≈ t, ji                              =
   if s or t is stuck then {hs ≈ t, ji} else error j

     In the actual implementation, we also use a heuristic optimization for the
case simp hf s1 . . . sn ≈ f t1 . . . tn , ji, where s1 . . . sn and t1 . . . tn do not contain
metavariables, and f is not a projection. In this case, we first try simp hs1 ≈
t1 , ji . . . simp hsn ≈ tn , ji, and if no error is thrown, we return {}.
     Each unification constraint returned by simp is in one of the following cat-
egories:
    • delta: hf s ≈ f t, ji. Note that, based on the definition of simp, f must
      be a reducible definition.
    • pattern: h?m ℓ1 . . . ℓn ≈ t, ji, where ℓ1 , . . . , ℓn are pairwise distinct free
      variables, t only contains free variables in {ℓ1 , . . . , ℓn }, and ?m does not
      occur in t.
    • quasi-pattern: h?m ℓ1 . . . ℓn ≈ t, ji, where all ℓ1 , . . . , ℓn are free vari-
      ables, but are not pairwise distinct.
    • flex-rigid: h?m s1 . . . sn ≈ t, ji, where at least one of s1 , . . . , sn is not a
      free variable.
    • flex-flex: h?m1 s ≈ ?m2 t, ji.
    • recursor: ht ≈ s, ji, where t or s is a stuck recursor.
In the literature, pattern, quasi-pattern, and flex-rigid are simply called
flex-rigid constraints, and the category pattern corresponds to Miller pat-
terns [22]. Note that flex-flex constraints are badly underconstrained, and we
typically expect that other constraints will do more to limit the interpretation
of the metavariables.

3.5     Preprocessing
The preprocessor is a recursive procedure that, given a preterm and a context,
returns a term t (potentially containing metavariables) and a set of unification
and choice constraints. The basic idea is that if the constraints are solved,
their solution should contain an assignment for all metavariables in t. The
preprocessor must carry a context, a list of free variables, to be able to create
fresh metavariables. This is the only procedure in our implementation that

                                              19
“carries contexts around.” The preprocessor only creates asserted justification
objects.
    Applications (r s) are the main source of unification constraints. After a
preterm p in a context ℓ is converted into the application (r s), the preprocessor
uses ensurefun to make sure that the type of r is of the form Πx : A, B, and
simp to enforce that the type C of s is convertible to A. If C is not convertible
to A, the preprocessor checks the database of available coercions. If there is
a coercion c from C to A, it replaces the application (r s) with (r (c s)).
If A is stuck, but there are coercions {c1 , . . . , cn } from C, the preprocessor
creates a fresh metavariable ?m : abstractΠ ℓ A, replaces the application with
(r (?m ℓ)), and creates a ondemand choice constraint h?m ℓ : A in f, ji, where
the choice function f produces one of the following alternatives s, c1 s, . . . ,
cn s. If possible, the solver will only invoke f after all metavariables in A have
been instantiated. In this ideal situation, f returns at most one solution, and
no case-analysis is needed. The same process is performed when C is stuck and
there are coercions to A. We currently do not try to inject coercions when both
A and C are stuck at preprocessing time.
    As noted in Section 2.6, Lean supports parametric coercions, and coercions
to sorts and function classes. Ad hoc overloading is also realized using choice
constraints. The idea is the same, but we create a regular choice constraint,
where the choice function f produces the different interpretations for the over-
loaded symbol.
    In a context ℓ, a placeholder “ ” is simply replaced by ?m ℓ, where ?m is a
fresh metavariable.
    Finally, to handle implicit arguments, when we infer the type t of a term
r, if t is of the form Π{x : A}, B, then we create a fresh metavariable ?m :
abstractΠ ℓ A and replace r with the application (r (?m ℓ)). If the implicit
argument is marked with square brackets to indicate it should be synthesized
by the type class mechanism, we also create an ondemand choice constraint
h?m ℓ : A in f, ji, where the choice function f invokes the type class resolution
procedure. This procedure is essentially a simple λ-Prolog interpreter [22], where
the Horn clauses are the user-declared instances.

3.6    The constraint solving procedure
Given a set of constraints, our solver returns a failure, or a substitution S and
set of flex-flex constraints of the form h?m1 s ≈ ?m2 t, ji such that neither
?m1 nor ?m2 are assigned in S. In other words, it is required to solve all the
constraints that are presented to it, but it does not assign metavariables whose
solutions are underconstrained.
    The solver uses the following data structures:
   • a priority queue Q of constraints,
   • a mapping U of metavariables to constraints,
   • a substitution S, and


                                       20
    • a case split stack C.
To simplify the presentation, we assume Q, U , S and C are global variables.
   The priorities for the Q are computed using the following total order, ≺, on
constraint categories:
      pattern ≺ ready ≺ regular ≺ delta ≺ quasi-pattern ≺
         flex-rigid ≺ recursor ≺ postponed ≺ flex-flex
Recall that ready, regular, and postponed are all choice constraints. If two
constraints are in the same category, we use the first-in-first-out method.
    The mapping U works as follows: for each metavariable ?m, U [?m] is the
finite subset of the constraints in Q such that for each c in U [?m], c is a uni-
fication constraint stuck because of ?m, or c is an ondemand choice constraint
h?n ℓ : t in f, ji and ?m occurs in t. The set U [?m] contains the set of con-
straints that need to be (re-)visited whenever ?m is assigned. We remark that
a unification constraint in U [?m] may become simpler after we replace ?m with
its assignment. Similarly, an ondemand choice constraint h?m ℓ : t in f, ji in
U [?m] is ready to be processed when all metavariables in t have been assigned.
    Given a set of constraints s, for each constraint c in s, the procedure visit s
simply invokes visiteq c if c is a unification constraint, and visitchoice c
otherwise. The procedure visiteq hr ≈ s, ji is defined as follows:
     if r or s is stuck by some ?m and ?m 7→ ht, jm i in S then
          visit (simp hr[?m := t] ≈ s[?m := t], j ⊲⊳ jm i)
     else if the constraint is a pattern h?m ℓ ≈ t, ji then
          add the assignment ?m 7→ h(abstractλ ℓ t), ji to S
          for each c in U [?m], visit (c)
     else update U , and insert constraint into Q
The procedure visitchoice h?n ℓ : t in f, ji just substitutes any assigned
metavariable ?m occurring in t, updates U , and inserts the constraint into Q.
Note that, we never insert pattern constraints into Q.
    To implement a backtracking search, we need a mechanism for restoring the
state of the solver during a backtrack operation. We use a very simple approach
where Q, U , and S are implemented using pure data structures (red-black trees)
that provide a constant time copy operation. Whenever we need to create a case
split, we simply create copies of Q, U and S. An alternative approach is to use
a trail stack [25] which stores operations that “undo” the destructive updates
performed during the search. We have determined that our simpler approach
for implementing backtracking is not a bottleneck in our implementation.
    When solving a non-pattern constraint c, the solver creates a case split, and
stores it on the stack C. Each case split is a tuple of the form hQc , Uc , Sc , ja , jc , zi,
where
    • Qc , Uc and Sc store the state of the solver when the case split was created,
    • ja is a fresh assumption justification used to track the case split,


                                             21
   • jc is the justification for c, and
   • z is a lazy list containing the remaining alternatives, where each alternative
     is a list of constraints.
We use pull z to denote the operation that destructively extracts the head
of the lazy list z and returns it, or returns none when z is empty. The solver
catches any error j thrown by the simp procedure, and uses the error resolution
procedure resolve j defined as follows:
      while C is not empty
         let hQc , Uc , Sc , ja , jc , zi = top C in
         if j depends on ja then
            restore state Q := Qc , U := Uc , S := Sc
            if pull z = some a then visit (a ⊲⊳ jc ⊲⊳ j) and return pop C
      failed to solve constraints since C is empty
In the procedure above, visit (a ⊲⊳ jc ⊲⊳ j) may throw another error j ′ . If
this happens it recursively invokes resolve j ′ .

3.7     Processing constraints
At the very core of the algorithm is the procedure for processing the constraints
in the the queue Q, which we now describe. We use an auxiliary procedure
process z j, where z is a lazy list of alternatives, and j is a justification. If z
is empty, it just invokes resolve j. Otherwise, it pulls the head a of z, creates
a fresh assumption justification ja , pushes the new case split hQ, U, S, ja , jc , zi
on the stack C, and invokes visit (a ⊲⊳ ja ⊲⊳ j).
    For choice constraints h?m ℓ : t in f, ji, whether they are ready, regular
or postponed, we just invoke process (f (?m ℓ) t S) j.
    For delta constraints hf s1 . . . sn ≈ f t1 . . . tn , ji, we try two alternatives.
In the first one, we assume f is opaque,Sand try to avoid the potentially ex-
                                                 n
pensive δ-reduction step by using a1 = i=1 simp hsi ≈ ti , ji. If it fails, as
our next alternative, we unfold f and try a2 = simp(hunfold (f s1 . . . sn ) ≈
unfold (f t1 . . . tn ), ji). We use the operation tolazy to convert the list [a1 , a2 ]
into a lazy list, and process the delta constraint using process (tolazy [a1 , a2 ]) j.
This case split is a heuristic optimization and is not necessary for completeness.
    The two constraint categories quasi-pattern and flex-rigid are handled in
the same way; we use different categories only to ensure that easier constraints
occur first in the priority queue. We undertake an incomplete search for so-
lutions to these constraints using a variation of the flex-rigid case of Huet’s
unification algorithm [17]. Given a flex-rigid constraint h?m s1 . . . sp ≈ t, ji,
the main idea behind Huet’s algorithm is the observation that t must be a term
of the form f r1 . . . rn , where f is a free variable or a constant. The next idea is
the observation that any solution for ?m is convertible to one in eta-long normal
form, which allows us to consider only solutions for ?m that are of the form

                  λx1 . . . xn , h (?m1 x1 . . . xn ) . . . (?mp x1 . . . xn )      (*)

                                              22
where ?mi are fresh metavariables, and h is a constant or one of the bound
variables x1 . . . xn .
    In Huet’s algorithm, only opaque constants are considered, so if h is a con-
stant different from f of the rigid term t, the solution would lead to an unsolvable
constraint. Therefore, we say that Huet’s procedure has two kinds of case splits:
imitation (when h is the constant f of the rigid term), and projection (when
h is one of the bound variables x1 . . . xn ). However, there are two complica-
tions in our setting. First, we do not eagerly unfold f r1 . . . rn when f is a
constant. For example, assume that sub a b (subtraction for integers) is de-
fined as add a (uminus b). Then h?m (uminus a) ≈ sub b a, ji has a solution
?m = λx, add b x, but we would miss it if we did not unfold sub before trying to
imitate. Second, we have recursors in our language, and even if f is an opaque
constant, it is not the only constant that can be used for h. For example, given
the constraints h?m zero ≈ true, ji, h?m (succ zero) ≈ false, ji, a possible
solution is ?m = λx, nat.rec (λn, bool) true (λn r, false) x, where nat.rec
is the recursor for the type nat (of the natural numbers). We cope with the first
problem using an approach similar to the one used for delta-constraints when
f is a reducible constant. The idea is to have two imitation steps, one where
f is not unfolded, and another one where the term f r1 . . . rn is put into weak
head normal form before performing the imitation. In our implementation, it is
currently infeasible to consider the extra imitation step (after whnf) for all con-
stants. Even using non-chronological backtracking, the search space becomes
too big. The main problem is that the system may spend a huge amount of time
traversing the whole search space when the user provides an incorrect partial
construction. As to the second issue, we currently simply ignore this possiblity,
since the search space would become too big if we considered recursors for h.
Moreover, if h is a recursor, the constraint obtained after replacing ?m would
be a stuck recursor.
    As in most higher-order unification procedures, we try first the projection
case splits because they generate more general solutions. We remark that the
number of case splits can usually be greatly reduced for quasi-patterns, which
is the case the arises most commonly in practice. In this case, if f is a con-
stant (not marked as reducible), then we do not need to consider any projec-
tions. Any projection would fail immediately: if we take h to be ℓi and sub-
stitute (*) for ?m in the original constraint, we obtain an unsolvable constraint
hℓi (?m1 ℓ) . . . (?mp ℓ) ≈ f r1 . . . rn , j ′ i. Finally, if f is a free variable ℓ, then
we only need to consider the projection where h is xi if ℓi = ℓ.
    For flex-rigid constraints h?m s1 . . . sn ≈ t, ji, we only consider the case
h is xi when si is a free variable ℓ, or si is convertible to t. In the second
case, where si is convertible to t, we simply assign λx1 . . . xn , xi to ?m. This
is a heuristic for reducing the size of the state, and minimizing the number
of instances where the procedure exhibits nonterminating behavior. We note
that in the second-order case, the solver does not miss solutions by using this
heuristic. Finally, our solver has a threshold on the number of steps that can
be performed.
    We also use an approximate solution for recursor constraints ht ≈ s, ji.

                                            23
If the head of t and s is the same recursor C.rec, then we try to solve the
constraint by treating C.rec as a regular opaque constant which has no com-
putational behavior associated with it. If t or s is of the form ?m r, then we
treat it as a flex-rigid constraint. In a previous implementation of our algo-
rithm, when the recursor C.rec was stuck because of a term ?m r, we tried to
perform a case split for each constructor C.mki of C, assigning ?m to terms of
the form λx, C.mki (?m1 x) . . . (?mn x). However, this provides only a minor
improvement on the usability of the system: only three theorems in our library
broke after we removed this feature, and all of them could be easily fixed by
providing implicit arguments explicitly.


4    Related work and conclusions
The elaboration algorithm we have described above has been developed and
tuned in conjunction with the development of Lean’s standard and homotopy
type theory libraries. Although these libraries are still under development, they
provide ample evidence that the approach we describe here is effective in prac-
tice. At the time of writing, the standard library consists of about 42k lines of
code, with core datatypes including products, lists, sets, multisets (bags), tu-
ples, subtypes, and vectors; core number systems, namely, the natural numbers,
integers, rationals, reals, and complex numbers; algebraic structures, including
orders, (ordered) groups, (ordered) rings, (ordered) fields, and so on; elementary
finite group theory, through Sylow’s theorem; elementary number theory, such
as the unique factorization theorem; the beginnings of analysis, including the
completeness of the reals and elementary properties of limits. The homotopy
type theory library consists of more than 25k lines of code, including most of
the first seven chapters of the Homotopy Type Theory book [30], and a subst-
natial development of category theory. Specifically, it includes core datatypes
and constructions, such as paths, fibrations, equivalences, and pathovers; higher
inductive types, such as the circle, sphere, torus, quotients, pushouts, suspen-
sions; the calculation of the homotopy group of the circle; and category theory
through the Yoneda lemma. Lean also supported a substantial development in
nonabelian algebraic topology [33], carried out by Jakob von Raumer in the
homotopy type theory framework.
    We attempt to put our work in the context of recent work on elaboration in
dependent type theories. Abel and Pientka present an extension of Miller-style
pattern unification [1] which can handle a larger class of problems (in addition to
Σ-types) by a method they call pruning, which, intuitively, removes arguments
to metavariables which fall outside of the Miller pattern fragment, allowing for
more solutions to be found. They also give a bi-directional inference system for
a dependently typed λ-calculus, which together with the unification algorithm
yields an outline for a practical implementation. They show the soundness of the
unification algorithm with respect to this type system. They do not, however,
treat the case of defined constants, with or without recursion.
    Building upon this is recent work by Ziliani and Sozeau [35] that describes


                                        24
a unification algorithm for the Coq theorem prover which features defined con-
stants and recursively defined functions. They attempt to describe the practical-
ities of such an algorithm for a realistic dependently typed language, outlining
the heuristics and efficiency compromises inherent in this task. In that respect,
their motivations are very similar to ours.
    In addition to Abel and Pientka’s pruning, Ziliani and Sozeau add a more
aggressive form of dependency erasure for metavariables, in an attempt to solve
more unification problems at the cost of uniqueness of solutions. One example
is the problem {?t true ≈ nat, ?t false ≈ nat}. This problem is solved in their
framework by dropping the dependency of ?t on its argument, and returning
the constraint ?t′ ≈ nat which gives the solution ?t 7→ λx, nat. They also
add a resolution rule called first order approximation, in which for example the
constraint ?f ?y ≈ S 0 is solved with the assignment ?f 7→ S, ?y 7→ 0
    Since we have no qualms about allowing multiple solutions and backtracking
search our algorithms can handle both of these problems easily, in the first
case by a special case of projection, and in the second by an imitation step.
Our approach to free variables in metavariables is simple: there are none. In
contrast, Ziliani and Sozeau carry around a suspended substitution with every
metavariable, that needs to be managed in each resolution step. The heuristics
outlined in their paper for unfolding constants are similar to ours: constants are
unfolded only after an attempt has been made to apply type-class resolution,
and constants are unfolded to a pattern match or fixpoint only in last resort.
More study is needed to examine the trade-offs of these various choices. Finally,
their system does not allow postponement of constraints, relying on pruning
and dependency erasure to treat most cases up-front. They argue that great
efficiency gains are obtained in this manner. Again, more study is required to
assess the trade-offs of this approach.
    Various algebraic developments in Coq make use of type classes [27, 28, 14]
and canonical structures [26, 12, 19]; see also [2] for the use of unification hints
in Matita. Many of the features we have described are also implemented in
systems based on simple type theory. For example, Isabelle uses axiomatic
typeclasses [34] and parameterized contexts (locales) [5] to deal with algebraic
structures. It also has mechanisms to insert coercions [31]. The reliance on
simple type theory, however, makes the elaboration problem quite different from
ours. For example, an algebraic structure that depends on a parameter, such as
the integers modulo m, cannot be represented as a type, and so cannot be an
instance of an axiomatic type class. In contrast to Lean, Isabelle uses different
languages to construct expressions and assertions, build proofs, and express
relationships between structures.
    In a different vein, recent work by Brady on the dependently typed language
Idris [8] describes the elaboration process by analogy with theorem proving (and
in the context of pure functional programming). Our work is in stark contrast
with his, as our tactic language is completely disjoint from the methods with
which we specify the constraint resolution for the unification problems. In Lean,
the problems are quite different: in unification, metavariables can be very non-
local, appearing in disparate contexts and the solutions can be an infinite stream

                                        25
rather than a simple finite case split.
   To summarize: we have described the elaboration procedure used in the
new open source interactive theorem prover Lean [10]. Our procedure uses
methods found in state-of-the-art constraints solvers, such as nonchronological
backtracking, indexing, and justification tracking. We have also described how
coercions, type classes and ad-hoc polymorphism can be smoothly integrated in
our framework using choice constraints. Our procedure has been tested with the
development of more than 65k lines of Lean’s formal library, and the experience
has shown that it provides powerful and effective support for the formalization
process.


References
 [1] A. Abel and B. Pientka. Higher-order dynamic pattern unification for
     dependent types and records. In TLCA, volume 6690 of LNCS. Springer,
     2011.
 [2] A. Asperti, W. Ricciotti, C. Sacerdoti Coen, and E. Tassi. Hints in uni-
     fication. In TPHOLs 2009, volume 5674 of LNCS, pages 84–98. Springer,
     Berlin, 2009.
 [3] A. Asperti, W. Ricciotti, C. Sacerdoti Coen, and E. Tassi. The Matita
     Interactive Theorem Prover. In Automated Deduction – CADE-23, volume
     6803 of LNCS, pages 64–69. Springer, 2011.
 [4] J. Avigad, L. de Moura, and S. Kong. Theorem proving in lean. on-
     line version: https://leanprover.github.io/tutorial, PDF version:
     https://leanprover.github.io/tutorial/tutorial.pdf.
 [5] C. Ballarin. Locales and locale expressions in Isabelle/Isar. In Types for
     Proofs and Programs, pages 34–50. Springer, 2004.
 [6] B. Barras, S. Boutin, C. Cornes, J. Courant, J.-C. Filliatre, E. Gimenez,
     H. Herbelin, G. Huet, C. Munoz, C. Murthy, et al. The Coq proof assistant
     reference manual: Version 6.1. 1997.
 [7] A. Bove, P. Dybjer, and U. Norell. A brief overview of Agda–a functional
     language with dependent types. In TPHOL, pages 73–78. Springer, 2009.
 [8] E. Brady. Idris, a general-purpose dependently typed programming lan-
     guage: Design and implementation. Journal of Functional Programming,
     23:552–593, 2013.
 [9] T. Coquand and G. Huet. The calculus of constructions. Information and
     Computation, 76(2):95–120, 1988.
[10] L. de Moura, S. Kong, J. Avigad, F. van Doorn, and J. von Raumer.
     The lean theorem prover. In 25th International Conference on Automated
     Deduction (CADE-25), 2015.

                                      26
[11] P. Dybjer. Inductive families. Formal aspects of computing, 6(4):440–465,
     1994.
[12] F. Garillot, G. Gonthier, A. Mahboubi, and L. Rideau. Packaging Mathe-
     matical Structures. In TPHOL, volume 5674 of LNCS. Springer, 2009.
[13] W. D. Goldfarb. The undecidability of the second-order unification prob-
     lem. Theoretical Computer Science, 13(2):225–230, 1981.
[14] J. Gross, A. Chlipala, and D. I. Spivak. Experience implementing a per-
     formant category-theory library in Coq. In ITP, pages 275–291, 2014.
[15] C. V. Hall, K. Hammond, S. L. Peyton Jones, and P. L. Wadler. Type
     classes in Haskell. TOPLAS, 18(2):109–138, 1996.
[16] J. R. Hindley. The principal type-scheme of an object in combinatory logic.
     Transactions of the American Mathematical Society, 146:29–60, 1969.
[17] G. Huet. A unification algorithm for typed λ-calculus. Theoretical Com-
     puter Science, 1:27–57, 1975.
[18] Z. Luo. ECC, an extended calculus of constructions. In LICS, pages 386–
     395. IEEE, 1989.
[19] A. Mahboubi and E. Tassi. Canonical Structures for the working Coq user.
     In ITP, volume 7998 of LNCS, pages 19–34, Rennes, France, July 2013.
     Springer.
[20] P. Martin-Löf. An intuitionistic theory of types. Twenty-five years of
     constructive type theory, 36:127–172, 1998.
[21] C. McBride and J. McKinna. Functional pearl: I am not a number–I am a
     free variable. In Haskell’04, pages 1–9. ACM, 2004.
[22] D. Miller and G. Nadathur. Programming with Higher-Order Logic. Cam-
     bridge, 2012.
[23] R. Milner. A theory of type polymorphism in programming. Journal of
     Computer and System Science, 17:348–374, 1978.
[24] C. Paulin-Mohring. Inductive definitions in the system Coq rules and prop-
     erties. Typed Lambda Calculi and Applications, pages 328–345, 1993.
[25] F. Rossi, P. Van Beek, and T. Walsh. Handbook of constraint programming.
     Elsevier, 2006.
[26] A. Saı̈bi. Typing algorithm in type theory with inheritance. In POPL ’97,
     pages 292–301. ACM Press, 1997.
[27] M. Sozeau and N. Oury. First-Class Type Classes. In TPHOLs 2008,
     volume 5170 of LNCS, pages 278–293. Springer, August 2008.


                                      27
[28] B. Spitters and E. van der Weegen. Type classes for mathematics in type
     theory. Mathematical Structures in Computer Science, 21(4):795–825, 2011.
[29] T. Streicher. Investigations into intensional type theory, 1993. Habilita-
     tionsschrift, Ludwig-Maximilians-Universität München.
[30] The Univalent Foundations Program. Homotopy Type Theory: Univalent
     Foundations of Mathematics. Institute for Advanced Study, 2013.
[31] D. Traytel, S. Berghofer, and T. Nipkow. Extending Hindley-Milner type
     inference with coercive structural subtyping. In APLAS, LNCS, pages 89–
     104. Springer, 2011.
[32] F. van Doorn. Constructing the propositional truncation using non-
     recursive hits. To appear in Certified Proofs and Programs (CPP) 2016.
[33] J. von Raumer. Formalization of non-abelian topology for homotopy type
     theory. Master’s thesis, Karlsruhe Institute of Technology, 2015.
[34] M. Wenzel. Using axiomatic type classes in Isabelle. 2005.
[35] B. Ziliani and M. Sozeau. A predictable unification algorithm for Coq
     featuring universe polymorphism and overloading. submitted.




                                      28
