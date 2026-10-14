                                                                     MirrorShard: Proof by Computational
                                                                         Reflection with Verified Hints
                                                   Gregory Malecha                                       Adam Chlipala                                Thomas Braibant
                                                Harvard University SEAS                                    MIT CSAIL                        University of Grenoble and MIT CSAIL
                                                gmalecha@cs.harvard.edu                                adamc@csail.mit.edu                        thomas.braibant@inria.fr


                                                                      Patrick Hulin                                                    Edward Z. Yang
                                                                            MIT                                                        Stanford University
arXiv:1305.6543v1 [cs.PL] 28 May 2013




                                                                      phulin@mit.edu                                                 ezyang@cs.stanford.edu




                                        Abstract                                                                   gations, freeing the programmer to focus on providing invariants
                                        We describe a method for building composable and extensible ver-           and other pieces of high-level insight. However, conventional au-
                                        ification procedures within the Coq proof assistant. Unlike tradi-         tomated program verifiers as in the ESC family [18] suffer from a
                                        tional methods that rely on run-time generation and checking of            number of disadvantages.
                                        proofs, we use verified-correct procedures with Coq soundness               • Debuggability. Theorem prover implementations can be quite
                                        proofs. Though they are internalized in Coq’s logic, our provers              complex. While the prover will facilitate effective static veri-
                                        support sound extension by users with hints over new domains, en-             fication for many other programs, the prover itself is usually
                                        abling automated reasoning about user-defined abstract predicates.            debugged tediously via testing, and “bugs” often manifest as
                                        We maintain soundness by developing an architecture for modular               confusing failures of the tool to discharge specific goals.
                                        packaging, construction, and composition of hint databases, which
                                        had previously only been implemented in Coq at the level of its dy-         • Trustworthiness. As a corollary of the last concern, we might
                                        namically typed, proof-generating tactic language. Our provers also           worry that an off-the-shelf theorem prover is unsound in a way
                                        include rich handling of unification variables, enabling integration          that can have serious consequences for security and so forth, if
                                        with other tactic-based deduction steps within Coq. We have imple-            we use it as a trusted component of a verification system.
                                        mented our techniques in MirrorShard, an open-source framework              • Flexibility. The logics of automated theorem provers are gen-
                                        for reflective verification. We demonstrate its applicability by in-          erally chosen to be decidable or otherwise tractable in practice,
                                        stantiating it to separation logic in order to reason about imperative        ruling out expressive higher-order features. As a result, some
                                        program verification.                                                         important correctness theorems (e.g., semantic correctness of a
                                                                                                                      compiler) may not be possible to state, and others must be stated
                                        1.   Introduction                                                             in prohibitively verbose ways.
                                        In using proof assistants to establish theorems with very high assur-       • Composability. Many theorem provers act as standalone sys-
                                        ance at relatively low human cost, two main methods are employed.             tems that do not easily produce results that can be combined
                                        One can implement proof-generating theorem provers that justify               with results arising from other tools using a unified logical lan-
                                        their decisions in terms of more primitive reasoning steps, or one            guage. For instance, we may want to verify the correctness of
                                        can employ the proof by reflection style, which involves verifying            a compiler (which is outside the reach of traditional program
                                        the correctness of provers formally, so that there is no need to audit        verifiers), verify the correctness of a program in the compiler’s
                                        their outputs. The latter style has been used fairly heavily in the type      source language (which is well within the scope of traditional
                                        theory community, where it is often viewed as a straightforward               verifiers), and compose the results into a high-confidence de-
                                        implementation technique to improve both performance of and as-               duction about the compiled version of that source program.
                                        surance about proof search. To our knowledge, however, proof by
                                        reflection has only been applied to fairly focused problems where              All of the above reasons have contributed to the popularity of
                                        the domain of discourse (or its axiomatization) is known a priori.         program verification with proof assistants like Coq [16] and Is-
                                        To explore its limits, we explore mostly automated correctness ver-        abelle [29]. Such systems are based on small, trustworthy proof
                                        ification of imperative programs, in a framework supporting higher-        checkers for relatively simple sets of axioms and inference rules.
                                        order logic and abstract predicates. Extensibility is crucial in this      They achieve trustworthiness by allowing the use of arbitrary
                                        domain, as the (expert) author of an abstract data type (ADT) would        proof search techniques without expanding the trusted code base
                                        like to teach the prover how to reason about related proof goals           for proof checking. The underlying logics are higher order, provid-
                                        that arise in verifying (non-expert) client code that calls the ADT’s      ing very good flexibility. It is even possible to leverage external
                                        methods. We hope to achieve this modularity and expressivity while         tools, like SMT solvers, to generate proof assistant proofs, address-
                                        minimizing the overhead of proofs.                                         ing the composability concern.
                                                                                                                       However, debuggability remains a serious concern. While au-
                                           Realistic program verification involves consideration of many           tomated provers support many features, they are not a panacea. For
                                        details of program behavior. Automated theorem provers play a              example, combinations of modal, linear, and higher-order logic are
                                        crucial role in discharging the many straightforward proof obli-           not supported by any prover that we are aware of. And even when
they are, the undecidability of powerful logics forces frequent use
of new, problem-specific heuristics that must be embedded into au-        Listing 1. Verification of binary search trees implementing finite-
tomation or applied manually each time they are needed. Without           set “lookup”
the ability to justify such extensions, user customization compro-        (* "Spine" type to define the rep. predicate *)
mises the trustworthiness of the entire system. While, it is possible     Inductive tree := Leaf : tree | Node : tree → tree → tree.
to use arbitrary implementations to generate proof traces in novel
                                                                          (* Recursive representation predicate for BSTs *)
ways, such procedures can be nearly as hard to debug as conven-           Fixpoint bst’ (s : set) ( t : tree) ( p : W) : HProp :=
tional, non-proof-generating theorem provers.                               (* details omitted *).
    It is also true that switching to an approach based on proof gen-




                                                                                                                                              user predicate
eration can bring substantial performance costs. A proof language         (* Main rep. predicate, which wraps the above with a
with few orthogonal features is very attractive because it allows          * mutable pointer to its root *)
proof checkers to be small and trustworthy, but small proof lan-          Definition bst (s : set) ( p : W) := d freeable p 2 e
guages tend to promote large proofs. Automated provers must be              ∗ Ex t, Ex r, Ex junk, p 7→ r ∗ (p +̂ $4) 7→ junk ∗ bst’ s t r.
augmented to support generation of proofs, which adds code com-




                                                                                                                                                refinement hints
plexity and performance overhead. Later, it is necessary to check         (* A standard tree refinement hint *)
                                                                          Theorem nil_fwd : ∀ s t (p : W), p = 0 →
the proofs, which adds further overhead.                                    bst’ s t p =⇒ d s ' empty ∧ t = Leaf e.
                                                                          Proof. destruct t; sepLemma. Qed.
    An established best-of-both-worlds technique for type-theoretic
                                                                          (* . . .more hints. . . *)
proof assistants is proof by reflection [9]. Here, instead of writing
a procedure that generates a proof on each invocation, we instead




                                                                                                                                                combine hints
                                                                          (* Combine the hints into a first-class package *)
verify the procedure itself. Now no proofs need to be generated,          Definition hints : HintPackage.
freeing us from the associated overhead. However, the formal guar-        prepare (nil_fwd, bst_fwd, cons_fwd) (nil_bwd, bst_bwd, . . .).
antees are just as strong, because we have proved the correctness         Defined.
of the procedure, which is generally implemented in a functional
programming language within the proof assistant’s logic.                  Definition bstM : bmodule := { . . .
    Proof by reflection has previously been implemented for con-          (* Method implementation *)




                                                                                                                                              quantified invariants
ventional mathematical decision problems. For instance, Coq               bfunction "lookup"("s", "k", "tmp") [lookupS]
                                                                            "s" ← ∗ "s";;
comes packaged with a tactic for algebraic simplification over              [ Al s, Al t,
mathematical rings. This procedure, and others out there, oper-                PRE[V] bst’ s t ( V "s") ∗ mallocHeap
ate over a small vocabulary of logical symbols whose semantics                 POST[R] d ( V "k" ∈ s) \is R e ∗ bst’ s t ( V "s") ∗
must be understood. Often the procedures are extensible in the                   mallocHeap]
sense of allowing customization of the set of symbols. However,             While ("s" 6= 0) {
such procedures can be thought of as single-minded, never com-                 "tmp" ← ∗ "s" + 4;;
bining multiple, user-defined reasoning strategies in the way that             If ( "k" = "tmp") {
successful automated program verifiers do.                                       (* Key matches! *)
    To investigate how far the scope of proof by reflection may be               Return 1
                                                                               } else {
expanded, we built reflective implementations of two key proof                   If ( "k" < "tmp") {
procedures for imperative program verification with higher-order                    (* Searching for a lower key *)
separation logic [32] within the Bedrock [13] library for Coq. Pre-                 "s" ← ∗ "s"
viously, these procedures were implemented in a proof-generating                 } else {
way, with Coq’s domain-specific tactic language Ltac [17].                          (* Searching for a higher key *)
    Listing 1 shows how our verification procedures handle user-                    "s" ← ∗ "s" + 8
defined abstractions by showing a verification of binary search tree             }
“lookup.” The code defines a representation invariant for binary               }
                                                                            };;



                                                                                                                                              prove with hints
search trees (bst). Afterward, a few hint lemmas are proved about
                                                                            Return 0 . . . }.
the invariant. These lemmas encapsulate the semantic knowledge
that the reflective procedures will need to reason about bst. Spec-       (* Prove our implementation partially correct. *)
ifications for the imperative code make heavy use of logical quan-        Theorem bstMOk : moduleOk bstM.
tifiers, which create additional challenges for our automation. List-     Proof. vcgen; abstract (sep hints; auto). Qed.
ing 1 ends with a short proof of program correctness, via the sep
tactic that calls the reflective procedures with a particular package
of program-specific hints.
    Our high-level contributions come from adapting the proof-
by-reflection approach to a more open-ended setting. In partic-
ular:                                                                        correct) classic data structure examples like arrays, linked lists,
                                                                             and search trees.
 • To the best of our knowledge, ours are the first reflective tac-        • We extend the proof-by-reflection approach to handle proof
   tics to support a notion of reusable hints, similar to the no-            goals containing quantifiers, and we implement and verify a
   tions exposed in Coq Ltac programming. Our approach lever-                unification algorithm to facilitate related reasoning. Coq itself
   ages three types of hints to teach our core procedures about              includes a disjoint treatment of unification, and we have devel-
   new abstract predicates. Even the usual “points-to” predicate             oped an approach to two-way communication between the two
   of separation logic is not built into our tactics, but rather taught      unification systems. This interface is not trivial because unifi-
   to it via hints. We identify three hint mechanisms that suffice           cation is not part of Coq’s logic, but rather added on outside the
   to support all of the above from a small core, and we prove the           trusted base and interfaced with using Ltac, Coq’s tactic lan-
   soundness of the hint architecture. We also demonstrate (proved           guage for building proofs.
 • Hints are naturally expressed over different logical theories, in-
                                                                            Inductive expr :=
     volving different data structure representation predicates and         | Func: nat → list expr → expr.
     different background theories (e.g., bitvectors, lists, strings) for
     stating side conditions of lemmas. We have developed a modu-           Variable types : list Type.
     lar architecture for composing verified hints over different
     theories, including a mechanism for carving out and combining          Fixpoint ftype (domain: list nat) (range: nat) : Type :=
     smaller domains.                                                         match dom with
                                                                                | [] ⇒ nth range types
 • We also provide a performance analysis of design choices                     | t::dom ⇒ nth t types → ftype dom range
     in implementation of extensible reflective tactics. We en-               end.
     countered surprising challenges in achieving reasonable perfor-
     mance while supporting all of the above features.                      Record sig := {dom: list nat; rng: nat; val: ftype dom rng}.

    We begin with background on reflective proofs (Section 2). We           Variable functions : list sig.
then discuss the broadly applicable novel technical devices behind          Fixpoint denote (e: expr) (ty: nat): option (nth ty types) := . . .
our implementation, which enable us to apply reflective reason-                     Listing 2. Representing multi-sorted expressions
ing to the complicated expressions that arise in our verification
tasks (Section 3). We then try to distill the reusable engineering
lessons we have learned about implementing and optimizing reflec-
tive procedures at this scale (Section 5). Next comes an evaluation         Let types := [ nat; bool].
of the automation achieved by our procedures and an analysis of             Let functions := [sig [0;0] 0 plus; sig [0;0] 1 ltb;
their performance characteristics compared to non-reflective verifi-                           sig [] 0 x; sig [] 0 y; sig [] 0 z]
cation (Section 6), where our overall conclusion is that we improve
asymptotic performance substantially, though well-abstracted pro-           Func 1 [ Func 0 [ Func 2 []; Func 3 []]; Func 4 []] : expr
grams and specifications may not lead to large enough invariants to
exhibit the scaling improvements clearly. We wrap up with a dis-                Using this representation, we can implement a (heuristic) de-
cussion of related work (Section 7).                                        cision procedure in Gallina. The procedure considers the head
    Our techniques, and many of the components that we built, are           symbols of two expressions. If they are the same, it proceeds re-
implemented in the MirrorShard library, available for download at:          cursively on their arguments. Otherwise it accumulates a “proof
                                                                            obligation” (i.e., a pair of expressions whose denotations must be
       https://github.com/gmalecha/mirror-shard/                            proven equal).
                                                                            Fixpoint f_eq (a b: expr) (ty: nat) : list (nat∗expr∗expr) :=
2.    A Primer on Proof By Computational                                      match a , b with
      Reflection                                                                | Func f1 args1 , Func f2 args2 ⇒
                                                                                  if f1 == f2
In this section, we discuss the idea of reflection [9]. For the sake of           then union (map3 f_eq args1 args2 (domainOf f1))
simplicity, we shall present reflection using a stripped-down exam-               else [( ty, a, b)]
ple: here, we are interested in reducing the proof of equalities like         end.
f a (g b) = f c (g (h a)) to the proof of a = c and b = h a. That
is: we are computationally discharging equalities between terms in              Finally, we prove the procedure sound. That is, we prove that
the (multi-sorted) algebra generated by an arbitrary signature, gen-        if all of the constraints are satisfied then the denotations of the
erating new proof obligations for equalities between subterms that          original terms are equal.
do not follow from basic properties of equality.
                                                                            Theorem f_eq_correct : ∀ a b ty,
    The first step of reflection is to encode the syntax of proof goals       Forall (fun (t,x, y) ⇒ denote x t = denote y t) (f_eq a b ty)
in a datatype defined within your proof assistant’s logic. In the case        → denote a ty = denote b ty.
of Coq, this logic is Gallina, a dependently typed lambda calculus
with inductive definitions. Thus, we start by defining a datatype               Applying this lemma makes it possible to replace several proof
expr to represent terms: in this syntaxified representation, an ex-         steps (one proof step for every common head symbol between the
pression is just a function symbol applied to a list of expressions         lefthand-side and righthand-side expressions) by a single proof
(see Listing 2). We break the circularity using 0-argument functions        step, plus a computation. That is, we come to the final crucial
to represent variables and constants. This is important because it is       element of a proof by reflection: a goal is proved by appealing
imperative that the expr type has a decidable equality so we can            to a theorem and then proving its hypothesis by “running” the
avoid generating obligations such as x = x. We achieve this by rep-         hypothesis to reduce it to a normal form, which should then be
resenting functions as indices into an environment of functions.            much easier to prove than the original goal.
    To make the meaning of our syntax formal, we define a deno-                 For example, suppose that we want to prove ltb (x+y) z = ltb
tation function denote that maps an expression e supposedly of               (x+y) w. We can apply the aforementioned lemma, using suitable
the type represented by ty, to a value of type option (nth types            values a and b of type expr, and Coq will check that denote 1 a
 ty). Note that this denotation function is partial, because our data       (resp. denote 1 b) is convertible to the lefthand side (resp. right-
type admits the encoding of ill-typed terms. (We will return to this        hand side) of the goal, according to the lambda calculus reduction
particular design choice in Section 5.) The denotation function is          rules of Gallina. Here we take advantage of the fact that, in Coq’s
parameterized by an environment of types and function signatures            logic, reduction-equivalent terms may always be used interchange-
(of type sig indexed by the type environment), and will perform             ably, with no need to include explicit proof steps as justification.
dynamic type-checking to ensure that the Gallina term that it pro-
duces is well-typed. Thus, where ltb is a Boolean-valued less-than          Reification In the above discussion, we side-stepped a difficulty:
test for natural numbers, the term ltb (x + y) z can be represented         we have to automate the construction of the syntactic representation
using the following environments and term.                                  (i.e., terms of type expr) from the terms that appear in the goal.
                                                                            While this operation, called reification, is conceptually the dual
Record type := { Impl : Type ; Eq : Impl → Impl → bool }.
                                                                           Binders and local variables are represented by the constructors
                                                                              Exists of sexpr and Var of expr. Our encoding is similar
Inductive tvar := tvProp : tvar | tvType : nat → tvar.                        to the locally nameless technique for lambda terms, in that
                                                                              we maintain distinct representations of global/free variables
Inductive expr (ts : list type) : Type :=                                     (nullary function applications via Func) and local/bound vari-
| Const: ∀ ( ty : tvar), tvarD ty ts → expr ts                                ables (via Var).
| Var: nat → expr ts
| UVar : nat → expr ts                                                     Unification variables (represented with UVar) are represented
| Func: nat → list (expr ts) → expr ts                                        explicitly so that our procedures may deduce and substi-
| Equal : expr ts → expr ts → expr ts.                                        tute values for them. Informally, a Var expression supports
                                                                              universal-quantifier reasoning, while a UVar expression sup-
Inductive sexpr (ts : list type) : Type :=                                    ports existential-quantifier reasoning. We must prove any theo-
| Star : sexpr ts → sexpr ts → sexpr ts                                       rem considering all possible Var values, but we are allowed to
| Emp : sexpr ts                                                              choose specific UVar values that make the theorem true.
| Pred : nat → list (expr ts) → sexpr ts
| Inj : expr ts → sexpr ts                                                 To support our new features, the denotation functions exprD and
| Exists : tvar → sexpr ts → sexpr ts.                                     sexprD have several new parameters for variables, unification vari-
                                                                           ables, and separation logic predicates.
Fixpoint exprD (ts : list type) (fs : list (signature ts))                     To see how these components fit together, we show a simple
  ( vars uvars : list { t : tvar & tvarD ts t })                           heap assertion for a cons cell where the first value is a unification
  ( e : expr ts) ( t : tvar) : option (tvarD ts t) := . . ..
                                                                           variable from the context (?a) and the second (occurring 4 bytes
Fixpoint sexprD (ts : list type) (fs : list (signature ts))                later) is an existentially quantified value (v):
  ( ps : list (psignature ts))                                                                   ∃v, p 7→ ?a ∗ (p + 4) 7→ v
  ( vars uvars : list { t : tvar & tvarD ts t })
  ( e : sexpr ts) : hprop := . . ..                                        This term can be represented as:
Listing 3. Representing separation logic expressions with binders          Let types := [( word, eq_word)].
                                                                           Let funcs := [([], tvType 0,p); ([ tvType 0;tvType 0],tvType 0,+)].
                                                                           Let preds := [([ tvType 0; tvType 0], 7→)].
                                                                           Let vars := []. (* p is represented as a function *)
of denote, it must be performed at the meta level using special-
                                                                           Let uvars := [( tvType 0, ?a)].
purpose tactics. We shall return to this problem in Section 5.             Exists (tvType 0)
                                                                                  ( Star (Pred 0 [ Func 0 [] ; UVar 0])
3.    An Extensible Verification Architecture                                            ( Pred 0 [ Func 1 [ Func 0 []; Const 4]; Var 0]) )

Compared to past work on proof by reflection, our verification
architecture achieves its powerful form of extensibility through           3.2   Achieving Compositionality
three novel technical devices:                                             To be useful, hints must be both self-contained, packaging together
Extensible Syntax enables us to encode terms with arbitrary Coq            the hint and its soundness proof, and compositional, enabling us to
   constants and quantifiers, while retaining the ability to compute       combine separately defined hints in a meaningful way. Here, our
   on constants embedded in terms. (Section 3.1)                           type-family representation introduces problems. The most naı̈ve
                                                                           prover type, with one environment of types fixed for all provers,
Composable Soundness enables us to combine soundness proofs                will never compose with provers using different types. We solve
  about procedures that reason about different logical domains.            the problem using a sort of universal quantification over type envi-
  (Section 3.2)                                                            ronments that imposes constraints on the presence of specific iden-
Integration with Unification enables flexible integration of re-           tifiers.
   flective procedures with traditional Ltac-based automation that         A Constraint Formulation One way of representing the con-
   uses unification variables that are not formalized in Coq’s core        straints is propositionally, with explicit logical assertions. We can
   logic. (Section 3.3)                                                    encode constraints using partial environments and say that an en-
                                                                           vironment (e) satisfies a constraint (C), written C |= e, when all
3.1   An Extensible Syntax with Binders                                    mappings in the constraint are consistent with the environment. Us-
Our reified syntax for assertions of separation logic [32] (summa-         ing this formulation, we can define two provers, one for lists and the
rized in Listing 3) is similar in spirit to the generic syntax described   other for machine words. Each constraint is a list of optional types,
in Section 2 but incorporates several new forms for dealing with           where the presence of a type forces the final environment to contain
binders, manipulating proofs, and performing domain-specific rea-          that type in that list position.
soning. The four key differences are:
                                                                           Let C1 := [ None; Some (list word)].
A distinguished encoding for the type of logical propositions              Definition prover_1 : ∀ ts, C1 |= ts → expr ts → bool.
   (tvProp) simplifies representing logical properties and enables         Let C2 := [ Some word].
   us to represent polymorphic equality (Equal), even though our           Definition prover_2 : ∀ ts, C2 |= ts → expr ts → bool.
   encoding does not support polymorphic functions in general.                 Since C1 and C2 are compatible, these provers can be composed
An expression type family indexed by a type environment, which             into a new prover that accepts an environment that satisfies both C1
   gives for each type both its Coq representation and a compat-            and C2. The difficulty of this formulation arises in type-checking
   ible equality testing function. The Const constructor is used           prover implementations, where it is generally necessary to use casts
   to inject terms that our unification algorithm should consider          justified by appealing to the consistency proof. For example, sup-
   comparing for equality by calling type-specific procedures, in          pose that prover_2 is determining whether a number is a multiple
   contrast to the syntactic equality check used for the rest of the       of 4. An ideal formulation of the soundness of this prover would
   constructors.                                                           be:
Theorem prover2_sound’ : ∀ ts fs vars uvars e v (pf : C2 |= ts),           Definition prover_2 : ∀ ts,
  FC2 |= fs → prover_2 ts pf e = true →                                      let ts’ := applyC C2 ts in expr ts’ → bool.
  exprD ts fs vars uvars (tvType 0) e = Some v →
  v mod 4 = 0.                                                             Theorem prover2_sound : ∀ ts fs vars uvars e v,
                                                                             let ts’ := applyC C2 ts in let fs’ := applyC FC2 fs in
where FC2 is prover_2’s constraint on the function environment.              exprD ts’ fs’ vars uvars (tvType 0) e = Some v →
Unfortunately, this soundness statement is not well typed. The               prover_2 ts’ e = true →
problem stems from v. In line 3, v must have type tvarD ts (                 v mod 4 = 0.
tvType 0), while in line 4 v must have type word.
   The core problem lies in the intensional nature of Coq’s type               Now, tvarD (applyC C2 ts) (tvType 0) is definitionally equal
theory. Coq distinguishes between two notions of equality.                 to word since the environment has been reformed by applyC so
                                                                           that it is manifestly a series of “cons” operations, containing the
Definitionally equal (≡) terms are identical after reduction. This         proper type in the proper position. In particular, reduction tells us
   notion of equality is part of Coq’s core logic and requires no          applyC C2 ts ≡ word :: tl ts. In general, we may now extract
   extra work to apply during type-checking.                               any constant index occurring in the constraint from the updated
Provably equal (=) terms are defined by a binary inductive predi-          environment, without any need for dependent casts.
   cate x = y. This type encodes an explicit proof (in Coq’s logic)            In fact, this formulation gives us much more: it enables compu-
   that x and y are equal. To use this type of equality, we must           tational composition. When two constraint environments are com-
   perform a cast using the proof.                                         patible, i.e. they do not specify different values for any index, ap-
                                                                           plying applyC to them commutes definitionally.
For a concrete example, we return to the problem above. From the
meaning of |= we can prove tvarD ts (tvType 0) = word, but the                  applyC C1 (applyC C2 e) ≡ applyC C2 (applyC C1 e)
two are not definitionally equal under Coq’s reduction rules, since
                                                                           This feature makes composition of two provers trivial. If we wish
ts is a variable and not a concrete environment; the reduction to
                                                                           to compose two provers, say p1 and p2, with different, but compat-
determine equality gets stuck examining the structure of ts. We
                                                                           ible, environments TC1 and TC2, then we can pre-compose each
can solve this problem using the following cast:
                                                                           function by applying the other’s type constraint to produce two
Theorem prover2_sound : ∀ ts fs vars uvars e v (pf : C2 |= ts),            provers on the same environment. Concretely:
  FC2 |= fs → prover_2 ts pf e = true →
  exprD ts fs vars uvars (tvType 0) e = Some v →                           ( fun ts ⇒ p1 (applyC TC2 ts))
  ( cast v ( GetConsistent pf 0)) mod 4 = 0.                                   : ∀ ts, expr (applyC TC1 (applyC TC2 ts)) → bool
                                                                           ( fun ts ⇒ p2 (applyC TC1 ts))
where GetConsistent takes the consistency proof and the index                  : ∀ ts, expr (applyC TC2 (applyC TC1 ts)) → bool
and returns a proof of tvarD ts (tvType 0) = word (i.e. by look-
ing up the index in the constraint). The cast is present for a reason:     Since these types are definitionally equal, we can treat them identi-
removing it produces an ill-typed term. Therefore, it would be un-         cally, applying both functions to the exact same term. That is, any
sound to include a reduction rule that removes useful casts. The           composition operation can be written free of both explicit proofs
problem is that proving triviality of casts (i.e., that they convert be-   and explicit casts.
tween definitionally equal terms) is extra work with no counterpart            Using this representation, we can package together reusable,
in pencil-and-paper reasoning. A proof step like this one must be          self-contained verification hints using Coq’s dependent records.
preceded by another proof step that rearranges the proof context to
a form that is well-typed both before and after the cast is removed,       Record HintDatabase :=
which can be surprisingly subtle and case-specific. Furthermore,           { Types : constraint type
justifying this step (“removing a cast between definitionally equal        ; Funcs : ∀ ts, constraint (signature (applyC Types ts))
                                                                           ; Preds : ∀ ts, constraint (psignature (applyC Types ts))
terms has no effect”) is not possible in Coq’s core logic without          ; Hints : ∀ ts, HintsT (applyC Types ts)
appealing to axioms.                                                       ; Hints_correct : ∀ ts fs ps,
                                                                             HintsT_correct (Hints ts) (applyC (Funcs ts) fs)
                                                                                                       ( applyC (Preds ts) ps) }.
The Computational Formulation While Coq’s reduction mech-
anism does not handle the above formulation well, we can give              The first three fields express the constraints on the type, function,
an alternative formulation that enjoys better computational proper-        and heap predicate environments. The fourth field contains a record
ties. In this formulation we achieve constrained quantification over       that packages together the three different types of hints that our
environments not by starting from an arbitrary environment and             system uses (discussed in Section 4). Note that the type of Hints
asserting a constraint over it, but rather by starting with an arbi-        is dependent on the value of the Types field. The final field
trary environment and performing a computation on it to make it            encapsulates the soundness proofs for the hints. When applying our
constraint-compliant by construction. The heart of the technique is        reflective procedures, our tactics use the first three fields to seed the
a recursive function called like applyC c e, which “instruments”           environments used to reify terms, the hints to compute the results,
environment e to satisfy constraint c.                                     and the soundness proof to justify reasoning with the hints.
                                                                               Because we use a shallow embedding of constraints, we do not
Fixpoint applyC (c: constraint T) (e: list T) : list T :=
  match c with
                                                                           need to write a proof that two packages compose. Unfortunately,
    | nil ⇒ e                                                              this means that we cannot write a Gallina function that combines
    | None :: c’ ⇒ hd d e :: applyC c’ (tl e)                              two hint databases. Rather, we use Ltac (a dynamically typed lan-
    | Some v :: c’ ⇒ v :: applyC c’ (tl e)                                 guage) to construct the term and turn the type checker loose on it.
  end.                                                                     If the result type-checks, then the environments are consistent and
                                                                           the hints compose; otherwise, the programmer gets an error mes-
Reformulating the previous theorem leads to the following:                 sage about compatibility.
 p, q, r : word                                                    (a)                       {list xs p} ++*p {list ?L p}
                                                                                                                                          Extension point
 ?a : word
 ==============================                                                      1. Forward reﬁnement                                     base
                                                                                        Extension point: Unfold hints    Prove p≠0...
 p 7→ q ∗ ∃ x, q 7→ x =⇒ p 7→ ?a ∗ ∃ y, ?a 7→ y ∗ ∃ z, r 7→ z                                                                               theorem
                                                                                                                                             prover
 p, q, r : word                                                    (b)           {p ↦ x,q * list ys q} ++*p {list ?L p}
 ?a : word                                                                                                                                  Prove side-
 ==============================                                                               2. Symbolic evaluation                        conditions...
 ∀ x, ∃ z, ?a = q ∧ (* unification equation *)                                                   Extension point: Predicate evaluators
     ( p 7→ q ∗ q 7→ x =⇒ p 7→ q ∗ q 7→ x ∗ r 7→ z)
                                                                               {p ↦ x+1,q * list ys q} skip {list ?L p}
 p, q, r : word                                                    (c)
 x : word (* from [∀ x] *)
                                                                                                                3. Backward reﬁnement
 ?b : word (* from [∃ z] *)                                                                                        Extension point: Unfold hints
 ==============================
 p 7→ q ∗ q 7→ x =⇒ p 7→ q ∗ q 7→ x ∗ r 7→ ?b
                                                                               {p ↦ x+1,q * list ys q}skip {p ↦?X,?P * list?L'?P}
Figure 1. Representation of variables as they pass through our
verification procedures: (a) initial goal; (b) direct output of the
unification procedure; (c) after simplification with Ltac                                       ?X=x+1;?P=q                              4. Cancellation

                                                                               {p ↦ x+1,q * list ys q} skip {p ↦?X,?P * list?L'?P}
3.3   Interfacing with Unification Variables                                                                        ?L'=ys;?P=q
Traditional proofs in Coq are done in “proof mode” using tactics          Figure 2. The high-level verification strategy applied to a simple
that manipulate a goal that is displayed to resemble a standard           program that increments a memory cell
sequent calculus. Universally quantified variables are displayed in
a “proof context” above a double line, while the goal is displayed
below the line. In order to integrate well with existing tactic-based         A unification is represented as a map from unification variable
and interactive proof techniques, our reflective procedures must fit      to syntactic expression. As for our other syntactic representations,
naturally into this view.                                                 our soundness proofs ascribe a denotation to unifications, this time
    Figure 1 demonstrates how our reflective procedures manipulate        as a conjunction of provable equalities (substD). Using this deno-
binders and unification variables. The implementation of these pro-       tation function in a premise, we can prove that syntactic instantia-
cedures is complicated by manipulation of de’Bruijn indicies but is       tion, by instantiate, preserves the semantic meaning of terms.
otherwise mostly standard. It is the phrasing of the soundness theo-
rems that we focus on here. We begin with an illustrative example,        Theorem substD_instantiate : ∀ funcs U G e t sub,
Figure 1.(a), which shows a simple heap implication (denoted by             substD funcs U G sub →
=⇒) with three internal quantifiers and a unification variable (?a).        exprD funcs U G (instantiate sub e) t = exprD funcs U G e t.
Unlike in normal Coq output, we include unification variables ex-
                                                                              The final step occurs in Ltac. We simplify the goal by moving
plicitly in proof contexts, i.e. we can pick any term of type word
                                                                          variables “above the line” into the proof context. All ∀ quantifiers
for ?a as long as it mentions only globals and variables that occur
                                                                          lead to normal Coq variables (e.g., x), and all ∃ quantifiers lead to
above it.
                                                                          Coq unification variables (e.g., ?a). More importantly, we remove
    Our procedures take as inputs goals, like the one in Figure 1.(a),
                                                                          the unification equations like ?a = q by first performing the side ef-
after they are reified as terms in the logic. For explanatory purposes,
                                                                          fect of setting ?a equal to q and then proving the equation trivially
here we consider a simple procedure that only performs unification,
                                                                          by reflexivity. These side effects are possible in Ltac but not Gal-
attempting to learn the values of both bona fide Coq unification
                                                                          lina, and our strategy for generating initial output goals is designed
variables (e.g., ?a) and variables that are quantified existentially in
                                                                          to be very telegraphic in suggesting side effects.
the conclusion of the implication (e.g., y and z). A key question
is how the unification procedure, a pure function in the logic, can
cause side effects to resolve unification variables in the original Coq   4.     Reflective Procedures
proof context. As in proof by reflection in general, our procedures       The techniques described in the previous sections enable extensible
may only announce results by replacing one logical formula with           reflective verification with rich formulas. In this section, we show
another that has been proven to imply the original.                       how to apply MirrorShard, the Coq library we have built with those
    The result of the unification procedure is shown in Figure 1.(b).     techniques, to create reflective automation for the Bedrock [13] li-
Four different sorts of variables have been handled in four different     brary, which supports program verification in separation logic. Our
ways. First, a variable existentially quantified on the lefthand side     development leverages MirrorShard to build the two core verifica-
of the original implication (e.g., x here) is returned via a top-level    tion components: symbolic execution and separation logic cancel-
universal quantification. Second, a normal Coq unification variable       lation. The procedure is illustrated in Figure 2 and described in the
(e.g., ?a here) is asserted to be equal to whatever replacement has       rest of the section.
been inferred for it. Finally, there are two cases for a variable
existentially quantified on the righthand side of the implication.        Symbolic Execution First, symbolic execution takes a precondi-
Either no unification was found for it (e.g., z in this example),         tion and a sequence of instructions and computes a post-condition.
in which case it gets a top-level existential quantifier in the new       Symbolic execution starts by using pure facts in the context to re-
goal; or some unification was found (e.g., y in this example) and         fine abstract predicates. In the example, the procedure finds that the
the variable is simply removed by substituting for it everywhere it       linked list predicate can be unfolded since the head pointer is not
appears.                                                                  null. This information is encoded in our first type of hint:
Refinement Hints are stylized Coq theorems that express predi-               the list predicate, exposing the first cell. In the conclusion, exis-
   cated heap implications. These theorems are reified into Coq as           tential variables are introduced as new unification variables that the
   inhabitants of a record type with fields for a list of universally        rest of cancellation will attempt to instantiate.
   quantified variables, a list of pure premises (exprs), and the ex-            The core of the cancellation algorithm uses the cancellative
   pressions on each side of the separation logic implication. Due           properties of separation logic to prove the implication. Since can-
   to their first-order nature, these hints can be constructed com-          cellation leverages unification to resolve unification variables and
   pletely automatically (using Ltac programs) from actual Coq               does not backtrack, the order of considering predicates to cancel
   theorems that have a particular syntactic form.                           matters. We use a simple heuristic based on a lexicographic order-
                                                                             ing of syntactic expressions where unification variables have the
Pure facts, such as the side conditions on refinement hints (e.g.,
                                                                             highest values and are thus unified last. This ordering, for example,
“pointer is not null”), are discharged by our second type of hint:
                                                                             will attempt to unify p 7→ ?a with p 7→ v before it tries to unify it
Base Theory Provers are verified Coq functions taking the place              with ?b 7→ ?c.
   of Coq tactics (since we cannot call Ltac from Gallina code),                 The Bedrock-specific instantiation of MirrorShard, including all
   proving expr-encoded proof goals with arbitrary algorithms                of the examples, is available online:
   that can be coded and verified in Gallina.
                                                                              https://github.com/gmalecha/bedrock-mirror-shard
   We have developed four provers:
     • A reflexivity prover, which proves statements of the form             5.    Lessons Learned: Engineering Reflective Proof
        e = e.                                                                     Procedures in Coq
     • An assumption prover, which maintains a list of known
                                                                             In this section we highlight a variety of design choices that arise in
        facts and attempts to find the goal as a syntactic match to          the development of reflective decision procedures. While the details
        one of these facts.                                                  are Coq-specific, the ideas generalize and shed light on interesting
     • A prover for reasoning about linear arithmetic on width-              design decisions both for users and developers of proof assistants.
        32 bitvectors to prove equalities and inequalities. This
        prover makes inferences by combining hypotheses repre-               5.1   Term representation
        senting expressions e1 = e2 + k for constants k. (This               General dependent types provide many representation alternatives
        last form of reasoning is especially applicable to common            that are not available in most programming languages. The first im-
        patterns of pointer arithmetic.)                                     plementation choice is whether the type of terms should guarantee
     • A prover oriented toward array bounds checks, which un-               that every term is well-typed. Such a representation allows us to
        derstands that array writes preserve length.                         make the denotation function (exprD) total, simplifying theorem
                                                                             statements and avoiding the need to prove that functions preserve
    We support composing provers in a simple disjunctive style, i.e.         the well-typedness of terms.
    a proposition is provable if either of two provers can prove it.             The cost of this convenience is indexing terms by additional en-
After predicate refinement, symbolic execution begins interpreting           vironments. In our setting, we would need to parameterize expr by
instructions. Total arithmetic and logical instructions are trivial to       the environments of functions, variables, and unification variables
model by converting the transfer functions into their syntaxified            in addition to the expression type, leading to a type like:
forms. Instructions that access memory (both reading and writing)            Inductive dexpr (ts : list type) (fs : list signature)
require more care, but our use of separation logic enables an effec-            ( uvars vars : list tvar) : tvar → Type := . . .
tive algorithm based on our third type of hint:
Memory Evaluators are verified functions that reason about reads             This representation moves the hard work from the soundness proofs
  from and writes to heaps satisfying a separation logic assertion.          to the computational operations that manipulate terms. For exam-
  This approach enables the symbolic evaluator to interpret mem-             ple, with dependent types, we weaken terms by structural recursion:
  ory operations in terms of many different data structure predi-            Fixpoint dexpr_weaken ts fs u u’ g g’ t (e : dexpr ts fs u g t)
  cates, without the need to expose individual points-to assertions            : dexpr ts fs (u ∪ u’) ( g ∪ g’) t := . . .
  algebraically.
  In addition to a composition operator that combines two mem-               Only the variable cases are interesting, essentially needing to jus-
  ory evaluators into one, we have implemented memory evalua-                tify that valid references into u (respectively g) are the same as
  tors for 32-bit points-to, arrays (of both words and bytes), and           references into u ∪ u’ (respectively g ∪ g’).
  local variable stack frames.                                                   Using a non-dependent representation, this function becomes a
                                                                             no-op since environments are extended at the end. Our proofs ap-
In the example, the memory evaluator uses the provers to inspect             peal to the following lemma that relates the meanings of expres-
the separation logic formula and determines that the value read              sions to their meanings under weakened environments.
from p is x (because a subformula p 7→ x appears) and the value
written is therefore x+1, which is constructed syntactically when            Theorem exprD_weaken : ∀ ts fs u g t e v,
interpreting the addition.                                                     exprD ts fs u g e t = Some v →
                                                                               exprD ts fs (u ∪ u’) ( g ∪ g’) e t = Some v.
Cancellation Cancellation proves that the strongest post-condition,
computed by symbolic execution, implies the specification’s post-                 This ease of implementation also translates to performance im-
condition. The algorithm begins with backward refinement, which              provements for procedures like cancellation, as shown in Figure 3.
uses the same type of refinement hints but refines in the conclusion         The first bar uses the dependent representation while the second
of the heap implication 1 . In the example, an analogous hint refines        uses the minimally dependent representation described in Sec-
                                                                             tion 3.1. We believe that the large difference between the bars is
1 Forward and backward refinement are both thin wrappers around a com-       due to the need to evaluate proof terms to reduce dependent casts,
mon, general, unification-based procedure for determining when quantified-   though Coq provides no profiling tools for verifying this hypothe-
equality hints apply to a goal.                                              sis.
                                                                    Sheet4



                                            Cancellation Performance (40 conjuncts)               backtracking tactics for proof search, rather than building actual
                                                                                                  terms. Second, we had to circumvent the lack of support for ma-
                                                                                                  nipulating open terms (i.e., terms with free variables) caused by
                                       t                                                          embedded binders. The trick requires copious use of second-order
      Term Representation




                                     en

                                                                                                  pattern matching, which is considerably more time-intensive and
                                   nd
                                 pe




                                                                                                  results in code that is more difficult to read and maintain. Third,
                               De




                                                                                                  we had to split reification into two passes: first, to gather the type
                                                                                                  environment, and then to build the reified terms indexed by this
                                                                                                  environment.
                                        t




                                                                                    Check
                                      en
                                    nd




                                                                                    Verify            To address the performance problem, we implemented a second
                                  pe
                                De




                                                                                                  version of our reification as an OCaml plugin. This alleviates all of
                              n-
                            No




                                            0          7.5              15   22.5            30   the previously mentioned problems: we use OCaml data structures
                                                             Time (s)                             (which are more efficient than their Ltac counterparts) to build
                                                                                                  environments and terms; we manipulate open terms, which makes
                             Figure 3. Verification times for two term encodings                  reification more direct; we make a single pass on the Coq term to
                                                                                                  build the reification environment and the reified terms, rather than
                                                                                                  two in Ltac. This plugin does not need to be trusted more than any
5.2                         Efficient Computation
                                                                                                  Ltac tactic since it constructs terms that are fed into the Coq kernel.
Analogous to the choice of term representation is the choice of                                       Using this plugin dramatically reduced the time spent on reifica-
function implementation. We may implement functions with de-                                      tion. Whereas Ltac reification had taken approximately 32 minutes
pendent types, making their properties manifest directly; or we may                               for a test suite of 10 examples, OCaml reification takes approxi-
choose simple types and then prove properties after the fact. The                                 mately 22 seconds (an 88X speedup). Processing of a single file
most common manifestation of this choice is for equality-testing                                  will typically perform hundreds of reifications, so these figures are
functions. In the dependent style, it is common to write the type                                 quite reasonable.
of an equality function as: ∀ x y, {x = y} + {x 6= y} (which is a                                     The reason for this slowdown is more than the interpretive
particular case of dependent sum type carrying proofs). The non-                                  overhead of Ltac. The explanation is a Coq feature (misfeature?)
dependent version (eqb) returns a Boolean, and provides a separate                                dealing with building terms in Ltac. To illustrate, consider two
proof: ∀ x y, eqb x y = true ↔ x = y.                                                             different Ltac expressions that build a natural number by repeatedly
    From a computational perspective, the latter is much more effi-                               applying the successor function S to the zero constant O. First, there
cient under call-by-value reduction, since in the former the proofs                               is the simple version S ( S ( . . .O. . .)), which just builds the term
that are constructed must be reduced completely. Changing our al-                                 directly. For reasonably sized numbers, this expression evaluates
gorithms to use the non-dependent version of equality checks re-                                  instantly. Then, there is the expanded form let n := O in let n
sulted in a 40% reduction in the proof generation and checking                                     := ( S n) in . . .(S n). . ., which binds an Ltac-level variable for
time. (Note also that in the context of code extraction from Coq,                                 each intermediate term. This expression evaluates in time quadratic
the difference between the solutions disappears.)                                                 in the term size.
    While this fact may be well-known for seasoned implementers                                       The underlying problem is that Coq re-typechecks all parts
of reflective decision procedures, there is little guidance from Coq’s                            of each new term that is constructed in Ltac. This is not an
standard library toward this choice. Page
                                        In adapting
                                               7        the proofs, we                            unreasonable-sounding requirement for a dynamically typed lan-
have found it easy to recover the proof behavior of the dependent                                 guage. Ltac-bound variables appearing in Gallina terms have their
equality using Coq’s dependent type classes [33].                                                 contents substituted in explicitly. Reification naturally builds terms
    Traditional type classes carry additional information about                                   step-by-step through a recursive process. The overhead of repeated
types, e.g. an equality decider. Dependent types enable type classes                              typechecking can become overwhelming in such cases. In contrast,
to carry additional information about values. For example, a type                                 all Coq-level type checking in OCaml is done explicitly. This al-
class indexed by a function can carry a proof about that function:                                lows dramatic speed-ups by only typechecking the final term once.
Class EqOk (T : Type) ( f : T → T → bool) : Type :=                                               5.4   Engineering Proof Terms
{ eq_ok : ∀ x y, f x y = true ↔ x = y }.
                                                                                                  While Coq proofs are often thought of as tactic scripts, the final
Proofs and automation can now reference the symbol eq_ok and                                      product of Coq proving is proof terms in a core type theory. Tactics
Coq’s type class resolution will attempt to find an appropriate                                   merely provide a more convenient way to construct these terms
instance. This approach is similar to the development in the math                                 (which often make heavy use of dependency). A proof that looks
classes project [34] and is the core principle underlying recent work                             straightforward at the tactic level may produce proof terms that take
on ExtLib 2 .                                                                                     substantially longer to check than the proof script took to run.
                                                                                                      The central issue in term engineering is the statement of the
5.3                         Reification                                                           correctness theorem. Two broad strategies are used commonly. The
Most sources gloss over the (mostly) uninteresting problem of                                     first, more traditional approach uses an equality proof to separate
reifying terms. While not particularly glamorous, the reification                                 the computation from its meaning:
process can dramatically affect verification time.                                                Theorem cancel_correct_with_eq : ∀ ts fs ps uvars pures l r,
    Our first version of reification for pure expressions, separation                               AllProvable ts fs ps uvars pures → (* premises (1) *)
logic formulas, and object-language commands used Ltac. How-                                        ∀ l’ r’, cancel l r = ( l’, r’) → (* computation (2) *)
ever, an initial performance evaluation showed that reification was                                  sexprD uvars l’ =⇒ sexprD uvars r’ → (* denote (3) *)
a major performance bottleneck (taking almost 50% of total ver-                                      sexprD uvars l =⇒ sexprD uvars r.      (* denote (4) *)
ification time). First, some of this overhead can be attributed to
Ltac itself: the language is dynamically typed and built for writing                              The benefit, and curse, of this formulation lies in the quantification
                                                                                                  over l’ and r’, which together act as the result of the cancellation
2 https://github.com/coq-ext-lib/coq-ext-lib                                                      procedure. To apply the above theorem, our proof must directly
record the values of l’ and r’. Thus, when Coq checks the proof it       adding additional provers), and is very difficult to debug. Missing
knows exactly what type line (3) has, regardless of the unification      symbols cause evaluation to get stuck producing enormous, par-
procedure used to justify the equation in line (2).                      tially evaluated terms that can chew through 8G of RAM in under
    Representing and type checking these embedded terms in the           a minute. Nevertheless, once the whitelist is complete, evaluation
final proof, however, can be expensive if they are large. While our      is fast. We post-process the resulting term folding named defini-
representation does not necessarily look large on the surface, the       tions that may have occurred in the reflective code and in the user
dependency of terms on the type environment requires that the type       function environment. That is, we substitute an identifier for its as-
environment be repeated syntactically at every constructor. Even         sociated definition, to simplify the term.
paring down the type environment to contain only the type (eliding           It is this final point that makes a blacklist unattractive. Though
the equality function and its proof) does not shrink the term enough.    the list would be considerably shorter, we would not know which
This is a limitation of Coq’s type checker, but not a theoretical one.   terms to refold or how to refold them at the end of the reduction.
Adapting Coq to use bi-directional type checking [31] could solve
                                                                         vm compute vm_compute [21] is an even faster Coq reduction
this problem.
                                                                         mechanism based on compiling Gallina terms to the OCaml virtual
    To circumvent the embedded term problem, we replace the
                                                                         machine, executing them there, and translating the results back to
quantifier with a let declaration scoped over the relevant premises.
                                                                         Gallina. The price for this speed is reduced flexibility in two ways:
Theorem cancel_correct : ∀ ts fs ps uvars pures l r,                     1. Neither whitelists nor blacklists are supported. All identifier are
  AllProvable ts fs ps uvars pures →     (* premises (1) *)                 unfolded if definitions for them exist.
  ( let (l’, r’) := cancel l r in    (* computation (2) *)
    sexprD uvars l’ =⇒ sexprD uvars r’) → (* denote (3) *)               2. vm_compute fails if it encounters Coq unification variables.
  sexprD uvars l =⇒ sexprD uvars r.         (* denote (4) *)
                                                                             On the surface, both limitations appear to be show-stoppers.
The drawback to this approach is that naı̈ve uses of this theorem do     Without a whitelist (or blacklist), separation logic abstractions (in
not record the result of the reduction. During proof checking, Coq       addition to simple functions like plus) will be torn apart, revealing
will lazily evaluate this term, leaving large, partially reduced terms   symbolic memories and 32-bit words. Further, the goals fed to our
unevaluated at key places, requiring them to be reduced multiple         tactics routinely contain several unification variables introduced by
times during subsequent proof checking. While Coq provides only          program-specific Ltac code.
limited methods for specifying reduction strategies in proof terms,          Our solution to these problems relies on building an anonymous
in practice knowing the result is enough to make proof checking          function that explicitly abstracts over terms that should not be
reasonably efficient. In general, we can save the result by perform-     reduced. This allows us to reduce only in the anonymous function
ing cut elimination with an explicit type annotation. We revisit this    and leave the dangerous subterms alone. Consider the following
problem in Section 5.5, discussing our solution for making this          simplified example, where we want to reduce the lefthand side to
phrasing efficient.                                                      the righthand side:
                                                                                                 2 ∗ 9 =⇒ 9 + 9 + 0
5.5   Engineering Reduction
                                                                         Naı̈vely using vm_compute produces 18. It is easy to abstract 9,
The workhorse of proof by reflection is the computation step, and        but + does not occur syntactically in the term. To expose it, we use
fast evaluation of terms is essential to making reflective proofs ef-    a special form of ∗ that takes + as an argument:
ficient. Unfortunately, as we demonstrated in Section 5.4, standard
formulations of reflective theorems do not work well in our set-         Fixpoint mult’ (plus’ : nat → nat → nat) (n m : nat) : nat :=
ting. Our formulation requires fast delimited evaluation, i.e. evalu-      match n with
ation keeping certain symbols opaque. Since Coq’s logic admits               | 0 ⇒0
                                                                             | S n’ ⇒ plus’ m (mult’ plus’ n’ m)
reduction under binders, evaluation strategies are able to handle          end.
opaque terms. However, to maintain abstraction by not unfolding
user-defined logical symbols, we need the ability to engineer the        Using this definition, we can engineer the following reduction:
handling of particular identifiers. Throughout our development we                                          vm
evaluated several reduction mechanisms, two of which are notewor-               (fun p x ⇒ mult0 p 2 x) =⇒ (fun p x ⇒ p x (p x 0))
thy.                                                                     which differs from our target reduction by a single, cheap β-
Delimited cbv Coq’s full-beta, call-by-value reduction mecha-            reduction when applied to + and 9.
nism is reasonably fast and supports the abstraction that we need            This technique works to make many terms opaque while still
to avoid the reduction of certain terms. As an illustration, consider    avoiding the problems of embedding the intermediate syntactic rep-
the goal after an application of cancel_correct.                         resentation in the proof term (see Section 5.4); however, there are
                                                                         several limitations. First, we cannot use it to limit reduction in types
let (l’, r’) := cancel funcs l r in                                      since abstracting by a type will often produce an ill-typed term.
sexprD funcs uvars l’ =⇒ sexprD funcs uvars r’                           Second, the abstractions are manifest in the resulting proof term,
                                                                         making it larger than it would be using delimited cbv. Finally, pro-
We would like to reduce the above proposition to a heap implication      ducing the abstraction using Ltac can be expensive since each ab-
using the standard separation logic connectives, e.g. ∗ and emp.         straction must perform a linear walk over the term. Because we
Since we know the definition of cancel, we can customize Coq’s           need to abstract all terms in the function and separation predicate
cbv tactic to leave certain constants, like ∗, opaque by specifying a    environments, it is not uncommon to be blacklisting 30 or more
whitelist of identifiers that should be reduced.                         symbols, each of which requires a linear pass over the term. To im-
    Unfortunately, specifying this list modularly is not possible.       prove efficiency, we packaged the functionality with vm_compute
The customization available to cbv requires an explicit whitelist        into a tactic called evm_compute in a Coq plugin available online 3 .
(or blacklist) of identifiers, with no facility for supporting dynami-   Unlike cbv, our tactic supports dynamic blacklists by accepting
cally constructed lists or using wildcards to include all values from    Coq lists of identifiers.
a module. The whitelist required to reduce the above goal con-
tains roughly 450 symbols, is sensitive to any refactoring (including    3 https://github.com/braibant/evm_compute
                                               Scale-Reduction



                              Reduction Scaling                                   File            Program           Invar.   Tactics           Other    Overhead
             100         cbv                                                      LinkedList           42              26        27               31         2.0
                         cbv-qed
                         evm
                                                                                  Malloc               43              16       112               94         5.2
              10         evm-qed                                                  ListSet              50              31        23               46         2.0
                         vm                                                       TreeSet             108              40        25               45         1.0
                         vm-qed
                                                                                  Queue                53              22        80               93         3.7
  Time (s)




               1                                                                  Memoize              26              13        56               50         4.6
                                                                           Figure 5. Case study verifications, with data on annotation burden,
              0.1
                                                                           in lines of code

             0.01
                                                                                                  Predicate Refinement & Cancellation
                    32             64                    128      256
                                                                                      10000
                                        # of Conjuncts
                                                                                      1000            Ltac
Figure 4. Performance measurements for different reduction
                                                                                                      Ltac-Qed
strategies. Number of conjuncts proxies complexity.                                    100            Refl-verify
                                                                                                      Qed




                                                                           Time (s)
                                                                                        10
Comparison To make the performance difference concrete, Fig-
ure 5.5 shows the reduction and proof checking times for delimited                       1

cbv, evm_compute, and vm_compute. We use the number of con-                             0.1
juncts as a proxy for the amount of computation since the cancella-
tion algorithm is O(n2 ) in this case.                                                 0.01
                                                                                              1   2           4            8              16           32      64
    First, note that cbv is considerably slower than the virtual
                                                                                                             Problem Size (list length)
machine-based strategies for large problems. The further slow-
down during checking cbv proofs is due to the customized reduc-
tion strategy not being recorded in the proof term. This causes the             Figure 6. Performance comparison to non-reflective procedures
proof checker to fall back on lazy evaluation, which is considerably
slower.
    The virtual-machine based strategies are considerably faster               Our case studies exercise reasoning about a variety of user-
with much better scaling properties. The overhead of blacklisting          defined abstract predicates. With the exception of a small set of
is roughly constant, becoming negligible for problems with more            obligations about words (mostly pertaining to memory access), the
than 64 conjuncts. This behavior justifies the efficiency of the           correctness side conditions (such as theorems about lists and sets)
lightly dependent design that MirrorShard advocates. However,              are verified by Ltac proof search. Our case studies are: LinkedList,
better facilities for customizing reduction would still be beneficial.     consisting of the classic functions is-empty, length, reverse, and
One promising idea is to use a delimiting function such as:                concatenate (the latter two performed in-place with mutation);
                                                                           Malloc, a naı̈ve memory allocator, based on an unsorted free list
Definition block (T : Type) (v : T) : T := v.
                                                   Page 1                  with no coalescing, used by all the later case studies; ListSet and
While such a term would have no effect on the logical meaning              TreeSet, implementations of a common finite set interface speci-
of a statement, certain reduction strategies could treat occurrences       fied with mathematical sets, respectively using unsorted lists and
of block x opaquely, not unfolding x. This would enable blocking           binary search trees; Queue, a standard FIFO queue specified math-
reduction inside types and avoid the need to write functions like          ematically using bags; and Memoize, a higher-order function that
mult’ in Section 5.4 that abstract their dependencies to make them         memoizes Bedrock code that implements a mathematical function.
visible at the top level. Reduction strategies like vm_compute could       The last of these requires interesting interplay between our automa-
then be parameterized by a set of these blocking functions.                tion and custom Ltac code to handle higher-order proof obligations
                                                                           related to first-class code pointers.
                                                                               The proof overhead is slightly lower than with the case studies
6.            Evaluation                                                   used for the old fully Ltac-based Bedrock [13]. The decrease arises
In this section we evaluate reflective proof techniques, comparing         mostly from our modularization Page   of hint
                                                                                                                     1   databases. Our ability to
them to the standard Ltac-style verify-and-check approach to mech-         verify the same examples demonstrates that we have achieved a
anized verification. We begin with a brief discussion of the automa-       similar level of automation and integration with Ltac.
tion level of our verification framework by discussing our test suite,         Our procedures have also been used in a larger case study [14]
before focusing on two grounds for comparison with Ltac-based              that has built a verified cooperative threading library and then ver-
verification methodologies: performance and debuggability.                 ified a Web server running on top of the library. The thread library
                                                                           includes about 400 lines of implementation code and 3000 addi-
Usability & Automation In addition to the example excerpted in             tional lines for its verification, while the Web server has 200 lines of
Figure 1, we have carried out a number of other library module             implementation and 500 more for the proof, which establishes that
verifications, to validate the usefulness and extensibility of Mirror-     representation invariants are maintained for key data structures.
Shard. Figure 5 shows some statistics of our six largest case studies.
In order, the columns of Figure 5 count the executable part of the         Performance Beyond expressive power, a crucial benchmark for
module being verified, the function specifications and invariants as-      verification tools is performance. Long-running tactics (or tools)
serted in code, the Ltac tactic proof scripts (including commands to       cut the programmer out of the loop, making iterative development
register hints), all the remaining lines, and finally the ratio of veri-   difficult.
fication lines to program lines. The lines that we account for under           Figure 6 uses a microbenchmark to compare the performance of
“Other” are almost all definitions of data structure representation        our reflective procedures based on MirrorShard to those Chlipala
predicates and statements of theorems about them.                          developed for his initial version of Bedrock [13]. The background
for this task is an abstract predicate sll for singly linked lists, along                                     Ltac                   Reflection
with two theorems that we use as refinement hints:
                                                                                                         VC Generation
                                                                                                                                     Symbolic
                          dp = 0e =⇒ sll([], p)                                                                                      Execution
        dp 6= 0e ∗ ∃p0 . p 7→ x, p0 ∗ sll(`, p0 )) =⇒ sll(x :: `, p)




                                                                                               Repeat
                                                                                                           Higher-order
                                                                                                                                    Cancellation
   Out of these theorems, we can derive variants for concrete list                                          Extension
lengths. For readability, we leave out side conditions on nullness
                                                                                                                                  Breakdown
or non-nullness of pointer variables, which appear in our actual                                        Theory Extension
benchmark theorem statements.
                             emp =⇒ sll([], p0 )                                                             Verificat ion Time
                                                                                         80%                                                       76.5%
                      p0 7→ x0 , p1 =⇒ sll(x0 :: [], p0 )
      p0 7→ x0 , p1 ∗ p1 7→ x1 , p2 =⇒ sll(x0 :: x1 :: [], p0 )                          60%




                                                                             % of Time
...and so on, generalizing to an arbitrary number of list cells. If                      40%
the length of the list is n, solving this problem requires n + 1
refinements, with n refinements via the theorem for non-empty                            20%                                          14.6%
lists and the final refinement using the empty-list theorem. In the                                                   4.9%
                                                                                                    4.1%
process, we introduce n unification variables and n pure facts (that
                                                                                         0%
none of the intermediate pointers are equal to 0).                                                Cancel             SymEval           Qed         Ltac
    Proving this family of theorems using the Ltac automation from
                                                                                                                          Phase
the old Bedrock system [13] is painfully slow both to find a proof
(Ltac) and check it (Ltac-Qed). Our experiments time out for a list         Figure 7. Verification process and the breakdown of verification
of length 32, while our new reflective automation (Refl) finishes in        time
under a second. We also see that the reflective tactic spends only
slightly longer on proof search than checking, while with the old
Ltac approach we see proof search running for at least 10 times             have complicated backtracking semantics that can make them dif-
longer. It is now faster to find proofs than it had been to check them.     ficult to write and even more difficult to debug. For example, the
    This straightforward result is the “good news” arising from our         backtracking severely complicated debugging our Ltac-based reifi-
experiments. We achieve asymptotically better performance scaling           cation code, since a typo in a single case would cause an exponen-
than the Ltac-based alternative, and the constants are low enough           tial backtrack through the algorithm. In addition, debugging tools
that the performance gap becomes clear even for relatively small            are difficult, and tactics that compute terms must be hand-coded in
microbenchmarks.                                                            continuation-passing style to get reasonable debugging support via
    The “bad news” arising from our experiments is that we see no           idtac, Ltac’s equivalent of printf debugging.
clear change in overall performance for our full case studies like in           On the other hand, even with a minimally dependent term rep-
Figure 5. Our experimental set-up is quite conservative, since our          resentation, coding in Gallina enables us to use Coq’s type checker
new Bedrock system involves a number of complexities not found              to get shallow “sanity” properties. Our soundness theorems allow
in the original. For instance, we added support for higher-order            us to prove the deeper properties that we are relying on. During de-
quantification in assertions; we switched the machine word rep-             velopment we found ourselves frequently fixing bugs related to de
resentation from natural numbers to size-32 bitvectors; and we in-          Bruijn indices and binders, up until the point when the proofs about
troduced the possibility for programs to crash by accessing invalid         the components were completed. The proving process contributed
memory addresses, creating many new crash-safety proof obliga-              considerably to the development process, pointing out bugs that our
tions for each program. Seen from this perspective, one might con-          initial test cases did not cover.
sider it a very promising sign that we hold overall verification per-
formance at approximately the same level. It is probably also true          7.           Related Work
that programs making good use of data structure encapsulation will
tend to feature relatively small assertions that do not provide much        Our work is part of a recent trend to improve the automation
opportunity to show off the asymptotic scaling of proof procedures.         available in proof assistants, which have traditionally supported
    Figure 7 shows how our reflective proofs fit into the overall           only very manual proof styles. Researchers have proposed several
verification. The flexibility afforded to us by this method is, in          alternative approaches.
some sense, its downfall. Two-thirds of verification time is spent              Proof by reflection [9] is a well-established technique in the
in Ltac, and pushing more reasoning into Gallina procedures is              communities of Coq and other closely    Pagerelated
                                                                                                                          1     proof assistants.
likely to reduce verification time drastically. We expect that our          Grégoire and Mahboubi built a reflective tactic to simplify terms
general techniques to support quantifiers and integrate pure provers        using the operators of any ring algebraic structure [22], and
should streamline further development of similar procedures. As             Braibant and Pous built a reflective implementation of rewriting
we experiment with more programs to verify, we expect both to               modulo associativity and commutativity of user-specified opera-
improve the performance of our pure provers, by introducing more            tors [10]. These past projects consider self-contained, well-defined
efficient Gallina data structures; and to add new procedures to             problems in the style of classical decision problems. In contrast,
discharge obligations in new mathematical theories.                         our work considers open-ended, extensible procedures more along
                                                                            the lines of those commonly used for automated program verifica-
Debuggability A crucial benefit of reflective proofs over their             tion. Such an expansion of scope raises the new issues that we have
Ltac counterparts beyond performance is the ability to reason about         described, like supporting quantifiers, an interface with a proof as-
the correctness of the proof-generating procedure. Ltac programs            sistant’s unification engine, and modular combination of verified
decision procedures over different theories. The last of these has      tools, though traditional proof techniques can be applied directly in
been considered by Lescuyer [23], who developed an SMT imple-           places where sophisticated, custom reasoning is necessary.
mentation in Coq. The theory composition that he achieves is more
integrated than the simple composite provers that we implemented,       8.   Conclusion
but the approach does not share the computational composition
that enables us to achieve lightweight extension. The Ssreflect Coq     We have built a core reflective proof framework that supports user
library [19] employs a small-scale reflection style where many          extensions via reflected lemmas and custom proof procedures that
predicates are coded as functional programs returning Booleans,         are packaged into reusable strategies. Our framework allows bi-
sidestepping concerns of decidability. The approach of Gonthier         directional communication with Coq’s unification variables, sup-
et al. [20] uses Coq’s canonical structures mechanism as a clever       porting both the instantiation of existing unification variables and
means of building proof-generating procedures, retaining most of        the construction of new unification variables.
the usual relative advantages and disadvantages of proof generation         To justify the framework’s applicability, we have instantiated
versus verification of proof procedures like ours.                      it to reason about a combination of higher-order and separation
    Other recent work has proposed Mtac [37], a new style of            logic including support for user-defined abstract predicates. In ad-
proof automation in Coq. Like reflective proofs, Mtac proof proce-      dition to the benefit of user extension for handling abstract pred-
dures are implemented in Gallina; however, in order to to provide       icates, our reflective tactics scale much better performance-wise
the types of operations necessary for making tactic development         than Bedrock’s original tactic-based verification procedure [13],
simple, these “tactics” have a monadic type. The monad supports         while producing at least comparable performance for the realistic
non-termination, failure, and syntactic matching of patterns against    case studies that we have experimented with.
terms. The last of these features makes it impossible to reason about       We succeeded in isolating two large chunks of separation logic-
Mtac procedures inside of Coq, since syntactic matching breaks the      based verification engines. Looking forward, it seems that the ripest
substitution property of equality, i.e. x = y → f x = f y. Execu-       areas for performance improvements are the non-reflective por-
tion of these programs is done at type-elaboration time through a       tions. Building a larger library of (reusable) base theory provers
special run expression that exists outside of Gallina.                  in our framework would reduce the number of goals passed back to
    Several projects [8, 27] have studied translation of SMT-solver     Ltac and enable us to apply more refinements reflectively. It would
proof traces into forms acceptable to proof assistants, and some        also be interesting see how the framework can be extended to cap-
of these projects [3, 7] are based on reflective Coq tactics. In the    ture fragments of higher-order logic that are common during verifi-
latter case, one verifies a proof checker rather than the prover it-    cation. This would enable us, in simple cases, to avoid some of the
self. Compared to our approach, there are non-obvious performance       ping-ponging which we believe is the source of much of our over-
trade-offs. Verifying the prover removes the need for potentially       head. While full reflective verification would be ideal, the ability of
expensive proof generation and checking, but the proof-generating       our framework to integrate nicely with more manual proofs enables
approach is compatible with using efficient low-level languages         us to choose to invest time in automation only when there will be
and optimizing compilers to implement the provers. Verifying the        a comparable payoff, i.e. where similar obligations crop up repeat-
prover helps avoid completeness bugs, where a tool may sometimes        edly. Highly specialized reasoning can still be proved manually or
generate invalid proof traces; but proof checkers are generally eas-    semi-automatically.
ier to verify than provers. Lescuyer and Conchon [24] built a re-
flective SAT solver tactic for Coq, and Nanevski et al. [28] and Oe     References
et al. [30] have verified efficient low-level code for a part of an      [1] A. W. Appel. Tactics for separation logic. Draft of January 2006.
SMT solver and a full SAT solver, respectively. None of this past
work supports modular extension with new provers rather than just        [2] A. W. Appel. Verismall: Verified Smallfoot shape analysis. In Proc.
                                                                             CPP, 2011.
proof checkers, and none supports a rich formula language includ-
ing quantifiers and user-specified predicates with associated axioms     [3] M. Armand, G. Faure, B. Gregoire, C. Keller, L. Thery, and B. Werner.
that should be applied automatically.                                        A modular integration of SAT/SMT solvers to Coq through proof
                                                                             witnesses. In Proc. CPP, 2011.
    A few past projects have proved the correctness of non-extensible
separation logic proof procedures. Marti and Affeldt [25] verified a     [4] J. Bengtson, J. Jensen, and L. Birkedal. Charge!: a framework for
simplification of Smallfoot [5] using Coq. Stewart et al. have done          higher-order separation logic in Coq. In Proc. ITP, 2012.
Coq verification of a Smallfoot-style verification tool VeriSmall [2]    [5] J. Berdine, C. Calcagno, and P. W. O’Hearn. Smallfoot: Modular
that relies on a novel verified heap theorem prover VeriStar [35].           automatic assertion checking with separation logic. In Proc. FMCO,
The prior work of this kind has considered none of functional cor-           2005.
rectness verification (as opposed to just memory safety), extension      [6] J. Berdine, B. Cook, and S. Ishtiaq. SLAyer: Memory safety for
with abstract predicates, or higher-order programs or specifications.        systems-level code. In Proc. CAV, 2011.
    Many standalone tools do efficient, automated analysis of large      [7] F. Besson, P.-E. Cornilleau, and D. Pichardie. Modular SMT proofs
low-level code bases for memory safety, using separation logic,              for fast reflexive checking inside Coq. In Proc. CPP, 2011.
outside of the context of proof assistants. Examples include Small-      [8] S. Bohme, A. Fox, T. Sewell, and T. Weber. Reconstruction of Z3’s
foot [5], SpaceInvader [11], and SLAyer [6]. Xisa [12] bears a               bit-vector proofs in HOL4 and Isabelle/HOL. In Proc. CPP, 2011.
special relationship to our new work, as it is extensible with new       [9] S. Boutin. Using reflection to build efficient and certified decision
predicate definitions in separation logic. Several other proof assis-        procedures. In Proc. TACS, 1997.
tant libraries provide support for separation logic proofs, including   [10] T. Braibant and D. Pous. Tactics for reasoning modulo AC in Coq. In
the tactic libraries of Appel [1] and McCreight [26], Holfoot [36],          Proc. CPP, 2011.
Ynot [15], and Charge! [4]. Some of the libraries in this latter cat-
                                                                        [11] C. Calcagno, D. Distefano, P. O’Hearn, and H. Yang. Compositional
egory provide proof automation comparable to that of the stan-               shape analysis by means of bi-abduction. In Proc. POPL, 2009.
dalone tools. Our work described in this paper is the first to ver-
                                                                        [12] B.-Y. E. Chang and X. Rival. Relational inductive shape analysis. In
ify such automation formally, rather than merely constructing it to
                                                                             Proc. POPL, 2008.
output program-specific proofs. One disadvantage of all such ap-
proaches is greater performance overhead compared to standalone         [13] A. Chlipala. Mostly-automated verification of low-level programs in
                                                                             computational separation logic. In Proc. PLDI, 2011.
[14] A. Chlipala. Modular verification of a software platform for multi-
     threaded Internet servers. Under review, 2013.
[15] A. Chlipala, G. Malecha, G. Morrisett, A. Shinnar, and R. Wisnesky.
     Effective interactive proofs for higher-order imperative programs. In
     Proc. ICFP, 2009.
[16] Coq Development Team. The Coq proof assistant reference manual,
     version 8.4. 2012. URL http://coq.inria.fr/distrib/V8.4/
     refman/.
[17] D. Delahaye. A tactic language for the system Coq. In Proc. LPAR,
     2000.
[18] C. Flanagan, K. R. M. Leino, M. Lillibridge, G. Nelson, J. B. Saxe,
     and R. Stata. Extended static checking for Java. In Proc. PLDI, 2002.
[19] G. Gonthier and A. Mahboubi. An introduction to small scale reflec-
     tion in Coq. Journal of Formalized Reasoning, 3(2):95–152, 2010.
[20] G. Gonthier, B. Ziliani, A. Nanevski, and D. Dreyer. How to make ad
     hoc proof automation less ad hoc. In Proc. ICFP, 2011.
[21] B. Grégoire and X. Leroy. A compiled implementation of strong
     reduction. In Proc. ICFP, 2002.
[22] B. Grégoire and A. Mahboubi. Proving equalities in a commutative
     ring done right in Coq. In Proc. TPHOLs, 2005.
[23] S. Lescuyer. Formalisation et développement d’une tactique réflexive
     pour la démonstration automatique en Coq. Thèse de doctorat, Uni-
     versité Paris-Sud, Jan. 2011.
[24] S. Lescuyer and S. Conchon. Improving Coq propositional reasoning
     using a lazy CNF conversion scheme. In Proc. FroCos, 2009.
[25] N. Marti and R. Affeldt. A certified verifier for a fragment of separa-
     tion logic. Computer Software, 25(3):135–147, 2008.
[26] A. McCreight. Practical tactics for separation logic. In Proc. TPHOLs,
     2009.
[27] S. McLaughlin, C. Barrett, , and Y. Ge. Cooperating theorem provers:
     A case study combining HOL-Light and CVC Lite. In Proc. PDPAR,
     2005.
[28] A. Nanevski, V. Vafeiadis, and J. Berdine. Structuring the verification
     of heap-manipulating programs. In Proc. POPL, 2010.
[29] T. Nipkow, L. C. Paulson, and M. Wenzel. Isabelle/HOL — A Proof
     Assistant for Higher-Order Logic, volume 2283 of LNCS. Springer,
     2002.
[30] D. Oe, A. Stump, C. Oliver, and K. Clancy. Versat: A verified modern
     SAT solver. In Proc. VMCAI, 2012.
[31] B. C. Pierce and D. N. Turner. Local type inference. ACM Trans.
     Program. Lang. Syst., 22(1):1–44, Jan. 2000. ISSN 0164-0925.
[32] J. C. Reynolds. Separation logic: A logic for shared mutable data
     structures. In Proc. LICS, 2002.
[33] M. Sozeau and N. Oury. First-class type classes. In Proc. TPHOLs.
     2008.
[34] B. Spitters and E. Van der Weegan. Type classes for mathematics in
     type theory. Mathematical Structures in Computer Science, 21, 2011.
[35] G. Stewart, L. Beringer, and A. W. Appel. Verified heap theorem
     prover by paramodulation. In Proc. ICFP, 2012.
[36] T. Tuerk. A formalisation of Smallfoot in HOL. In Proc. TPHOLs,
     2009.
[37] B. Ziliani, D. Dreyer, N. Krishnaswami, A. Nanevski, and
     V. Vafeiadis. Mtac: A monad for typed tactic programming in coq,
     2013. URL http://www.mpi-sws.org/~beta/mtac/.
