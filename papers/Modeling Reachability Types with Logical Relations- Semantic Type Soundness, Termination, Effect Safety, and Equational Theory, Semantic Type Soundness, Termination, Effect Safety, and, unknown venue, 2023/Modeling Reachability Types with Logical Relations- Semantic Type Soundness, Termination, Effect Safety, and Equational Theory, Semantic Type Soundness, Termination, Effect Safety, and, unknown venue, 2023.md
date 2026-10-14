                                        Modeling Reachability Types with Logical Relations:
                                        Semantic Type Soundness, Termination, Effect Safety, and
                                        Equational Theory
                                        YUYAN BAO, Augusta University, USA
                                        SONGLIN JIA, Purdue University, USA
                                        GUANNAN WEI∗ , Tufts University, USA
                                        OLIVER BRAČEVAC† , EPFL, Switzerland
arXiv:2309.05885v3 [cs.PL] 8 Oct 2025




                                        TIARK ROMPF, Purdue University, USA
                                        Reachability types are a recent proposal to bring Rust-style reasoning about memory properties to higher-level
                                        languages, with a focus on higher-order functions, parametric types, and shared mutable state – features that
                                        are only partially supported by current techniques as employed in Rust. While prior work has established key
                                        type soundness results for reachability types using the usual syntactic techniques of progress and preservation,
                                        stronger metatheoretic properties have so far been unexplored. This paper presents an alternative semantic
                                        model of reachability types using logical relations, providing a framework in which we study key properties of
                                        interest: (1) semantic type soundness, including of not syntactically well-typed code fragments, (2) termination,
                                        especially in the presence of higher-order mutable references, (3) effect safety, especially the absence of
                                        observable mutation, and, finally, (4) program equivalence, especially reordering of non-interfering expressions
                                        for parallelization or compiler optimization.

                                        1   Introduction
                                        Reachability types are a recent proposal to bring Rust-style reasoning about memory properties
                                        to higher-level languages. Instead of Rust’s rigid “shared XOR mutable” model, reachability types
                                        emphasize tracking of resources such as mutable references using type qualifiers, which enables
                                        richer programming patterns, e.g., based on sharing captured mutable data, in languages that make
                                        pervasive use of higher order functions and type-level abstraction.
                                           In prior work, key type soundness results for reachability types have been established [Bao et al.
                                        2021; Wei et al. 2024] using the usual syntactic techniques of progress and preservation [Wright and
                                        Felleisen 1994] with respect to (w.r.t.) a small-step, substitution-based, operational semantics. These
                                        results assure us that reachability information is preserved through evaluation, serving, e.g., as an
                                        informal justification that expressions with non-overlapping reachability can be safely evaluated in
                                        a different order or in parallel. Likewise, prior work [Bao et al. 2021; Wei et al. 2024] has proposed
                                        that reachability types could be used as the basis for effect systems to track (the absence of) store
                                        modifications in a fine-grained way, e.g., to parallelize overlapping reads as long as there are no
                                        conflicting writes. However, no end-to-end formal proof of such properties exists so far, and in
                                        general, stronger metatheoretic properties beyond basic type safety have been left unexplored.
                                           We address this gap by presenting an alternative semantic model of reachability types using
                                        the technique of logical relations [Ahmed et al. 2009; Benton et al. 2007; Plotkin 1973; Tait 1967;
                                        Timany et al. 2024], providing a framework in which to study key properties of interest such as
                                        semantic type soundness, termination, effect safety, and contextual equivalence.
                                        ∗ Work completed while at Purdue University.
                                        † Work completed while at Purdue University.


                                        This article is an extended version of Bao et al. [2025].
                                        Authors’ Contact Information: Yuyan Bao, Augusta University, Augusta, USA, yubao@augusta.edu; Songlin Jia, Purdue
                                        University, West Lafayette, USA, jia137@purdue.edu; Guannan Wei, Tufts University, Medford and Somerville, USA,
                                        guannan.wei@tufts.edu; Oliver Bračevac, EPFL, Lausanne, Switzerland, oliver.bracevac@epfl.ch; Tiark Rompf, Purdue
                                        University, West Lafayette, USA, tiark@purdue.edu.
2                                         Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf


   Bottom-up Design of Logical Relations. We construct logical relations (LR) for a family of
reachability type systems with increasing sets of features. Our starting point is the standard LR for
the simply-typed 𝜆-calculus with first-order references, which we augment with internal invariants
to track the flow of store locations, without restricting expressiveness (Section 2). From these added
invariants, we “rediscover” reachability types by propagating certain choices to qualifiers in the
user-facing type system (Section 3). Then, we scale up the set of features, from first-order mutable
references to higher-order mutable references (Section 3.6), from tracking all mentioned references
uniformly to distinguishing reads and writes (Section 3.7), and from a unary LR to a binary LR
(Section 4) to support equational reasoning (Section 5).
    Semantic Type Soundness. The most immediate result from the LR model is semantic type
soundness. As Timany et al. [2024] have argued, semantic type soundness is a stronger notion
than syntactic type soundness, so our semantic type soundness result has significance beyond the
existing syntactic results [Bao et al. 2021; Wei et al. 2024]. First, semantic type soundness does not
require terms to be syntactically well-typed, just to behave in a well-typed way, e.g., disregarding
ill-typed branches that are never taken. Thus, it provides a foundation for studying potentially
unsafe features and interactions with the outside world. Second, unlike prior results [Bao et al. 2021;
Wei et al. 2024] that were established w.r.t. a small-step operational semantics based on substitution,
we adopt a big-step operational semantics based on closures and environments. Thus, our results
map more closely to realistic language implementations.
   Termination. The LR model actually proves a stronger property than the absence of type
errors, namely that evaluation of all well-typed terms must terminate with a well-typed value. This
termination result is interesting in addition to soundness. First, the reachability type systems in
Section 3.6 and beyond contain several non-trivial features such as nested mutable references and
self references in function qualifiers, whose termination properties are non-obvious. Second, our
LR model is defined by simple structural recursion on types, with a store typing invariant that
precludes cycles in the store. This is in contrast to other recent work, which proposed a form
of transfinite step indexing to prove termination for a feature-rich language with higher-order
state [Spies et al. 2021]. In comparison, our model achieves a similar result but is entirely elementary
and requires neither step-indexes, nor advanced set-theoretic concepts, nor classical reasoning.
More broadly, the termination result is both reassuring, in the sense that reachability types can
support flexible mutation in places where termination is required (e.g., dependent type systems) but
also points out a non-obvious limitation in prior work [Bao et al. 2021; Wei et al. 2024], namely the
inability to construct cyclic heap structures such as doubly-linked lists. We leave it to future work
to study this limitation and possible remedies further. Recently, promising steps in this direction
were made by Deng et al. [2025].
   Effect Safety. The built-in store invariants of the LR model guarantee that an expression can
only observe or modify reachable store locations. Thus, reachability provides a natural upper bound
on potential side effects. Specifically, the latent effect of a function is limited to the store locations
reachable from the function and any locations reachable from the provided argument. In Section 3.7,
we extend our LR model with an effect system that tracks write effects on sets of variables in addition
to reachability. With this added precision of distinguishing pure observations from effectful write
operations, we are able to prove an effect safety theorem, stating that all store changes are covered
by write effects, i.e., pure expressions never cause any observable effects. While similar extensions
have been proposed in prior work [Bao et al. 2021; Bračevac et al. 2023a], no end-to-end proofs of
effect safety have been provided so far. And in fact the desired properties are non-trivial to capture
using progress and preservation, since effects are “performed” during reduction and not preserved
in the types of values.
Modeling Reachability Types with Logical Relations                                                                        3


   Program Equivalence. We extend our unary LR to a binary LR model in Section 4 to support
equational reasoning, and we prove key equivalences in Section 5. This equational reasoning
framework is significant as it provides a foundation for parallelization and for a variety of effect-
based compiler optimizations in the style of Benton et al. [2007] or Birkedal et al. [2016]. First,
we prove a reordering theorem for non-interfering expressions which justifies parallel execution.
Second, we prove 𝛽-equivalence for functions applied to pure and non-interfering arguments. This
result shows that the evaluation semantics used here is consistent with substitution (specifically,
substitution with values), despite not using substitution internally. It also justifies function inlining
as a compiler optimization, e.g., in the context of Bračevac et al. [2023a]’s compiler IR based on
reachability types for dependency analysis. We formulate equivalences for the calculus with and
without effect qualifiers (Section 3.7) and show that write effects enable a more precise notion of
non-interference than pure reachability.
   Contributions. In summary, this paper makes the following contributions:
   • We review the standard LR model for simply-typed 𝜆-calculus with first-order mutable refer-
     ences, and discuss how adding certain store invariants leads to reachability types (Section 2).
   • We present a unary logical relation that establishes semantic type soundness as well as
     termination for types with reachability qualifiers (Section 3).
   • We extend the calculus to support higher-order mutable references and show that the system
     remains sound and terminating (Section 3.6).
   • We extend the calculus with an effect system including an effect safety invariant, guaranteeing
     that pure expressions have no observable side effects (Section 3.7).
   • We extend the model to a binary logical relation to support relational reasoning w.r.t. the
     observational equivalence of two programs (Section 4).
   • We prove a reordering theorem for non-interfering expressions and 𝛽-equivalence for functions
     applied to pure and non-interfering arguments (Section 5).
   The formal results in this paper have all been mechanized in Rocq. The developments are available
online at https://github.com/tiarkrompf/reachability.

2     Motivation
2.1    Brief Review of Reachability Types
Reachability types [Bao et al. 2021; Wei et al. 2024] are a recent proposal to bring Rust-style
reasoning about memory properties to higher-level languages, specifically reasoning about sharing
and the absence of sharing: separation. Reachability types are based on four key ideas:
   (1) Tracking reachable variables in type qualifiers: Types are of the form 𝑇 𝑝 , where 𝑝 is a
reachability qualifier, a set of variables that may additionally include the freshness marker q.
    val x = new Ref(0)          // : Ref[Int]x in context [ x: (Ref Int)q ]
    val y = x                   // : Ref[Int]y in context [ y: (Ref Int)x , x: (Ref Int)q ]

The value of expression new Ref(0) is fresh: it must be tracked, but is not bound to a variable. The
typing context 𝑥 : (Ref Int) q means x reaches a fresh value. The type system keeps reachability
sets minimal in type assignment, i.e., in the example, we assign the one-step reachability set y to
the type of variable y. The complete reachability set y,x 1 can be retrieved by computing transitive
closures w.r.t. the typing context [Wei et al. 2024].
   Functions can reach all tracked values they close over. Thus, the reachability qualifier of a
function includes the set of its free variables, consistent with the interpretation as a closure record:
    def incr() = { x += 1 }     // : (() => Int)x in context [ y: (Ref Int)x , x: (Ref Int)q ]

1 For readability, we often drop the set notation for qualifiers and write them down as comma-separated lists of atoms.
4                                               Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf


   (2) Contextual freshness for function arguments: Reachability types can implement Rust-
style borrowing that grants unique access to a store location while temporarily disabling other
access paths. The following code defines a combinator borrow: 2
    // : ((z: (Ref Int)q ) => ((Int => Int)q => Unit)z )∅
    def borrow(z: (Ref Int)q )(f: (Int => Int)q ) = { z := f(!z) }

A fresh argument type means that the locations reachable from the argument and the function
must be mutually disjoint, so that the function cannot observe any potential overlap with variables
in the environment. This extends naturally to curried arguments such as z, f above:
    val d = new Ref(0)
    borrow(x)(y => y + !d)        // ok: argument type (Int => Int)d is fresh relative to borrow(x)
    borrow(x)(y => incr())        // type error: argument (Int => Int)incr overlaps with borrow(x) via x

The first function call typechecks as the arguments are separate and fresh relative to the partially
applied function borrow(x), but the second does not, as both the passed closure and the partially
applied function reach x.
  (3) Self references to approximate reachable data for escaping values: The type system
uses self-references in function types to track reachable values that escape from their defining scope.
Our self references are similar to this pointers in OO languages, as formalized, e.g., in the DOT
family of type systems [Amin et al. 2016; Rompf and Amin 2016].
    def cell(init: Int) = {     // : Int => (𝜇 f.() => (Ref Int)f )q
        val c = new Ref(init)     // : (Ref Int)c
        () => c                   // : (() => (Ref Int)c )c
    }                           // : (𝜇 f.() => (Ref Int)f )q introduce self-ref to avoid local variable 𝑐
    val z = cell(0)             // : (() => (Ref Int)z )z     instantiate self-ref 𝑓 with bound name 𝑧

The above function cell returns a closure that captures and leaks the internal reference c. Once
the closure escapes its defining scope, the variable c is no longer in scope, and thus cannot be
mentioned in its type, as doing so would make the type meaningless to clients. 3 Thus, we use
self-references in its type instead. The escaping closure is a fresh value before being bound to z. Its
return type uses a self-reference introduced by the 𝜇-notation (similar to DOT) to express that the
returned value overlaps with the closure itself. Like this pointers in OO languages, self-references
provide a way to tie hidden internal data to an externally visible identity, allowing us to track it
throughout the interaction with the caller.
   (4) Tracking effects: Reachability qualifiers provide a capability to reason about effects. Specif-
ically, a function’s qualifier is as an upper bound on what the function can observe or modify
from the context. Effects can be tracked even more precisely if the type system is extended with
a reachability-sensitive effect system [Bao et al. 2021; Bračevac et al. 2023a,b]. This enables, e.g.,
distinguishing reads and writes on the same store reference. In this paper, we focus on tracking store
modifications as write effects (Section 3.7). This allows us to distinguish pure from effectful code.
This distinction also provides additional precision for program equivalence (Section 5). Consider
the following example, where variables x and y are aliased.
        val x = new Ref(5); val y = x; val z = new Ref(1)
        y := y + !z             // :   @wr(y) in context [z: Ref[Int]q , y: Ref[Int]x , x: Ref[Int]q ]




2 Reachability types is a dependent type system, allowing a function’s result type to mention its argument.
3 The return type can only mention what is in scope, and needs to avoid any variable names going out of scope. This is

called the “avoidance problem” in the context of ML modules and other languages with restricted forms of dependent types
(e.g., DOT [Amin et al. 2016; Rompf and Amin 2016]), where substitution is not always permitted.
Modeling Reachability Types with Logical Relations                                                                                                              5



   Syntax                                                                                                                                              𝜆𝐵
                     𝑆,𝑇 , 𝑈 , 𝑉       ::=     𝐵𝑜𝑜𝑙 | 𝑇 → 𝑈 | Ref 𝑇                                              Types
                     𝑐                 :=      true | false                                                      Constants
                     𝑡                 ::=     𝑐 | 𝑥 | 𝜆𝑥 .𝑡 | 𝑡 1 𝑡 2 | ref 𝑡 | ! 𝑡 | 𝑡 1 := 𝑡 2 | 𝑡 1 ; 𝑡 2    Terms
                     𝑣                 ::=     𝑐 | ℓ | ⟨𝐻, 𝜆𝑥 .𝑡 ⟩                                               Values
                     Γ                 ::=     ∅ | Γ, 𝑥 : 𝑇                                                      Typing Environment
                     𝐻                 ::=     ∅ | 𝐻 ; (𝑥, 𝑣)                                                    Value Environment
                     𝜎                 :=      ∅ | 𝜎; (ℓ, 𝑣)                                                     Store
  Typing Rules                                                                                                                                Γ ⊢ 𝑡 :𝑇

                       (t-cst)                 Γ (𝑥 ) = 𝑇                             Γ ⊢ 𝑡 : 𝐵𝑜𝑜𝑙                               Γ ⊢ 𝑡 : Ref 𝐵𝑜𝑜𝑙
      Γ ⊢ 𝑐 : 𝐵𝑜𝑜𝑙                                           (t-var)                                            (t-ref)                                (t-!)
                                               Γ ⊢ 𝑥 :𝑇                          Γ ⊢ ref 𝑡 : Ref 𝐵𝑜𝑜𝑙                              Γ ⊢ !𝑡 : 𝐵𝑜𝑜𝑙

      Γ ⊢ 𝑡 1 : Ref 𝐵𝑜𝑜𝑙                      Γ ⊢ 𝑡 1 : 𝐵𝑜𝑜𝑙                                                                  Γ ⊢ 𝑡1 : 𝑇 → 𝑈
        Γ ⊢ 𝑡 2 : 𝐵𝑜𝑜𝑙                        Γ ⊢ 𝑡 2 : 𝐵𝑜𝑜𝑙                            Γ, 𝑥 : 𝑇 ⊢ 𝑡 : 𝑈                        Γ ⊢ 𝑡2 : 𝑇
                              (t-:=)                                (t-seq)                                       (t-abs)                          (t-app)
      Γ ⊢ 𝑡 1 := 𝑡 2 : 𝐵𝑜𝑜𝑙                  Γ ⊢ 𝑡 1 ; 𝑡 2 : 𝐵𝑜𝑜𝑙                      Γ ⊢ 𝜆𝑥 .𝑡 : 𝑇 → 𝑈                        Γ ⊢ 𝑡1 𝑡2 : 𝑈
   Big-Step Semantics                                                                                                                 𝑡, 𝐻, 𝜎 ⇓ 𝑣, 𝜎 ′
                                                        𝑡, 𝐻, 𝜎     ⇓ ℓ, 𝜎 ′      𝜎 ′ (ℓ ) = 𝑣
                              (e-cst)                                                             (e-!)                                                (e-abs)
          𝑐, 𝐻, 𝜎 ⇓ 𝑐, 𝜎                                        !𝑡, 𝐻, 𝜎 ⇓ 𝑣, 𝜎 ′                                  𝜆𝑥 .𝑡, 𝐻, 𝜎 ⇓ ⟨𝐻, 𝜆𝑥 .𝑡 ⟩, 𝜎

          𝑡, 𝐻, 𝜎 ⇓ 𝑣, 𝜎 ′                                 𝑡 1 , 𝐻, 𝜎 ⇓ 𝑏 1 , 𝜎 ′                                   𝑡 1 , 𝐻, 𝜎 ⇓ ℓ, 𝜎 ′
            ℓ ∉ dom(𝜎 ′ )                                 𝑡 2 , 𝐻, 𝜎 ′ ⇓ 𝑏 2 , 𝜎 ′′                                 𝑡 2 , 𝐻, 𝜎 ′ ⇓ 𝑣, 𝜎 ′′
                                       (e-ref)                                             (e-seq)                                                    (e-:=)
   ref 𝑡, 𝐻, 𝜎 ⇓ ℓ, 𝜎 ′ ; (ℓ, 𝑣)                     𝑡 1 ; 𝑡 2 , 𝐻, 𝜎 ⇓ 𝑏 1 ∧ 𝑏 2 , 𝜎 ′′                  𝑡 1 := 𝑡 2 , 𝐻, 𝜎 ⇓ true, 𝜎 ′′ [ℓ ↦→ 𝑣 ]

          𝐻 (𝑥 ) = 𝑣                          𝑡 1 , 𝐻, 𝜎 ⇓ ⟨𝐻 ′ , 𝜆𝑥 .𝑡 ⟩, 𝜎 ′        𝑡 2 , 𝐻, 𝜎 ′ ⇓ 𝑣, 𝜎 ′′       𝑡, 𝐻 ′ ; (𝑥, 𝑣), 𝜎 ′′ ⇓ 𝑣, 𝜎 ′′′
                           (e-var)                                                                                                                    (e-app)
       𝑥, 𝐻, 𝜎 ⇓ 𝑣, 𝜎                                                                𝑡 1𝑡 2 , 𝐻, 𝜎   ⇓ 𝑣, 𝜎 ′′′

Fig. 1. The syntax, static and dynamic semantics of 𝜆𝐵 . We use type 𝐵𝑜𝑜𝑙 as a representative type for primitive
types, e.g., TUnit and TInt. Thus, assignments (rule T-:=) return type 𝐵𝑜𝑜𝑙.

Incrementing the content of y by the value referenced by z induces a write effect (@wr) on variable y,
and transitively on x too, but not on z. Thus, such an effect system can be used to show that values
(e.g., the referent of z) are preserved over a potential effectful computation [Bračevac et al. 2023b].
  Towards a Semantic Model of Reachability Types. Having seen key examples of reachability
types, we will now recap the structure of semantic type soundness via the standard 𝜆-calculus LR
definitions, and then proceed to “rediscover” reachability types from semantic store properties.

2.2     Semantic Soundness of 𝜆𝐵
After introducing the standard LR model for simply-typed 𝜆-calculus (STLC), we will add high-
level semantic store invariants in Section 2.3 that track the flow of store-allocated values without
restricting the set of typeable terms. Setting the scene for Section 3, we show how these semantic
invariants naturally lead to the idea of exposing the corresponding information through user-facing
type qualifiers, so that the flow of store-allocated values can be tracked and controlled by the
programmer. We thus rediscover reachability types from first principles, and justify them in a
semantic rather than syntactic way.
   The 𝜆𝐵 Language. Fig. 1 shows the syntax and typing rules for 𝜆𝐵 , STLC with first-order store-
allocated mutable references (restricted to hold Boolean values). The definitions are mostly standard,
and can be found, e.g., in the popular TAPL textbook [Pierce 2004]. We use a big-step semantics with
a value environment 𝐻 and a store 𝜎, where 𝐻 is a partial function that maps variables to values,
and 𝜎 is a partial function that maps locations to values. We write 𝑡, 𝐻, 𝜎 ⇓ 𝑣, 𝜎 ′ to denote that
6                                                       Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf


    Interpretation of Value Reachability                                                                                                𝜆𝐵
                                                                                Ð
     𝐿 (𝑐 ) = ∅     𝐿 (ℓ ) = {ℓ }  𝐿 ( ⟨𝐻, 𝜆𝑥 .𝑡 ⟩ ) = 𝐿 (fv(𝜆𝑥 .𝑡 ) )𝐻 𝐿 (𝑞)𝐻 = 𝑥 ∈𝑞 𝐿 (𝐻 (𝑥 ) )
    Semantic Interpretation of Types, Terms, and Typing Contexts
                Σ ::= ∅ | Σ, ℓ : V
            Σ ⊑ Σ′ = ∀ ℓ. ℓ ∈ dom(Σ) ⇒ (ℓ ∈ dom(Σ′ ) ∧ Σ(ℓ ) = Σ′ (ℓ ) )
                     def

          Σ ⊑ L Σ′ =       L ⊆ dom(Σ) ∧ L ⊆ dom(Σ′ ) ∧ (∀ ℓ ∈ L. Σ(ℓ ) = Σ′ (ℓ ′ ) )
                   def


              𝜎 : Σ = dom(𝜎 ) = dom(Σ) ∧ (∀ℓ ∈ dom(𝜎 ). 𝜎 (ℓ ) ∈ Σ(ℓ ) )
                     def

                     def
         𝜎→ 𝐿 𝜎 ′ = ∀ℓ ∈ dom(𝜎 ). ℓ ∉ 𝐿 ⇒ 𝜎 (ℓ ) = 𝜎 ′ (ℓ )

        𝑉 [[Bool]] = { (𝐻, Σ, 𝑐 ) }
    𝑉 [[Ref Bool]] = { (𝐻, Σ, ℓ ) | ℓ ∈ dom(Σ) ∧ (∀ Σ′ . (𝑣 ∈ Σ(ℓ ) ⇐⇒ (𝐻, Σ′ , 𝑣) ∈ 𝑉 [[Bool]] ) ) }

     𝑉 [[𝑇 → 𝑈 ]] = { (𝐻, Σ, ⟨𝐻 ′ , 𝜆𝑥 .𝑡 ⟩ ) | ∀ 𝑣, 𝜎 ′ , Σ′ . 1 Σ ⊑ 𝐿 ( ⟨𝐻 ′, 𝜆𝑥 .𝑡 ⟩ ) Σ′ ∧ 𝜎 ′ : Σ′ ∧
                             2 𝐿 (𝑣) ⊆ 𝐿 ( ⟨𝐻, 𝜆𝑥 .𝑡 ⟩ ) ∪ 𝐿 ( ⟨𝐻, 𝜆𝑥 .𝑡 ⟩ ) ∧ (𝐻, Σ′ , 𝑣) ∈ 𝑉 [[𝑇 ]] ⇒
                                  ∃ 𝜎 ′′ , Σ′′ , 𝑣 ′ . 𝑡, 𝐻 ′ ; (𝑥; 𝑣), 𝜎 ′ ⇓ 𝑣 ′ , 𝜎 ′′ ∧ 𝜎 ′′ : Σ′′ ∧ Σ′ ⊑ Σ′′ ∧ (𝐻, Σ′′ , 𝑣 ′ ) ∈ 𝑉 [[𝑈 ]] ∧
                                      3 𝐿 (𝑣 ′ ) ⊆ 𝐿 ( ⟨𝐻, 𝜆𝑥 .𝑡 ⟩ ) ∪ 𝐿 (𝑣) ∪ dom(Σ′ ) ∧ 4 𝜎 ′ → (𝐿 ( ⟨𝐻, 𝜆𝑥 .𝑡 ⟩ ) ∪ 𝐿 (𝑣) ) 𝜎 ′′ }


            𝐸 [[𝑇 ]] = { (𝐻, Σ, 𝑡 ) | ∀ 𝜎 . 𝜎 : Σ ∧ ∃ 𝜎 ′ , Σ′ , 𝑣 ′ . 𝑡, 𝐻, 𝜎 ⇓ 𝑣 ′ , 𝜎 ′ ∧ 𝜎 ′ : Σ′ ∧ Σ ⊑ Σ′ ∧
                             (𝐻, Σ′ , 𝑣 ′ ) ∈ 𝑉 [[𝑇 ]] ∧ 𝐿 (𝑣 ′ ) ⊆ 𝐿 (fv(𝑡 ) )𝐻 ∪ dom(Σ) ∧ 𝜎 ′ → 𝐿 (fv(𝑡 ) )𝐻 𝜎 ′′ }

       𝐺 [[Γ 𝜑 ]] = { (𝐻, Σ) | dom(𝐻 ) = dom(Γ) ∧ 𝜑 ⊆ dom(Γ) ∧ (∀ 𝑥,𝑇 . Γ (𝑥 ) = 𝑇 ∧ 𝑥 ∈ 𝜑 ⇒
                       (𝐻, Σ, 𝐻 (𝑥 ) ) ∈ 𝑉 [[𝑇 ]] ) }
                                                                         fv(𝑡 )
                                      Γ |= 𝑡 : 𝑇      = ∀ (𝐻, Σ) ∈ 𝐺 [[Γ        ]]. (𝐻, Σ, 𝑡 ) ∈ 𝐸 [[𝑇 ]]
                                                     def
    Semantic Typing Judgment
Fig. 2. The value interpretation of types, terms, and typing context interpretation for 𝜆𝐵 . Formula 2 is a
tautology here, but we will see that our reachability qualifiers can specify how argument values nontrivially
interact with function values in Section 3. The highlighted formulas demonstrate that the knowledge about
locations reachable from given values allows the proof to track properties of an effectful operation, i.e.,
properties of locations unreachable during an operation will be preserved.
term 𝑡 is evaluated to value 𝑣, resulting in a store transition from 𝜎 to 𝜎 ′ . The value environment
is immutable, as is standard. Evaluating each sub-term in a sequence 𝑡 1 ; 𝑡 2 term yields a Boolean
value, and the overall result conjuncts the sub-terms’ resulting values. 4 The definition of dynamic
semantics shown in Fig. 1 is standard.
   Following [Amin and Rompf 2017; Ernst et al. 2006; Siek 2013; Wang and Rompf 2017], in the
proof of semantic type soundness, we extend the big-step semantics ⇓ to a total evaluation function
by adding a numeric fuel value and explicit timeout and error results. Note, however, that while
the operational semantics is step-indexed in this way, the logical relations we define are not, and
could be defined just as well with a partial (big-step or small-step) evaluation semantics.
   Modeling Stores. Considering the restriction to first-order references here, the store layouts are
always “flat”, i.e., free of cycles. To specify well-typed stores, we use a store typing Σ that maps
from locations to semantic types. A semantic type is a set of values (V). Observing the semantics,
a store always grows monotonically during the course of evaluation, which is modeled by the
store typing extension relation, written Σ ⊑ Σ′ . Store typing extension satisfies reflexivity and
transitivity. Given a store 𝜎, we write 𝜎 : Σ to mean that 𝜎 is well-formed w.r.t. the store typing Σ.
Fig. 2 (top, ignoring the highlighted formulas) summarizes the definitions of these notations.
4 To verify that reordering two terms (rules in Section 5.1) yields equivalent results, we have to choose a commutative

operation to combine the results. The most natural would be to combine the two results into a pair, but this would require
either including pairs in the base language, or using a 𝜆-encoding. Instead, we chose to allow each sub-term to yield a
Boolean value, as it captures the essential property with less complexity than those alternatives approaches.
Modeling Reachability Types with Logical Relations                                                                           7


   Value Interpretation of Types and Term Interpretation. Fig. 2 (middle) defines the value
interpretation of types, as well as the term and typing context interpretations, ignoring the high-
lighted formulas for now. The value interpretation of type 𝑇 , written as 𝑉 [[𝑇 ]], is a set of triples of
form (𝐻, Σ, 𝑣), where 𝐻 is a value environment, Σ is a store typing, and 𝑣 is a value.
   The values of type Bool are true and false; the values of reference type Ref Bool are store locations
that store a value of type Bool. The set of values of function type 𝑇 → 𝑈 w.r.t. store typing Σ is
defined based on its computational behavior. It says that for all future stores 𝜎 ′ : Σ′ , where Σ ⊑ Σ′ ,
for any value 𝑣 of type 𝑇 w.r.t. store typing Σ′ , if evaluating the function body in the extended
value environment with store 𝜎 ′ results in a value of type 𝑈 , a store 𝜎 ′′ , and a store typing Σ′′ ,
such that 𝜎 ′′ : Σ′′ and Σ′ ⊑ Σ′′ , then we conclude that the function values are valid at type 𝑇 → 𝑈
w.r.t. store typing Σ. Note that we inline the term interpretation to characterize the function body’s
computational behavior.
   A term 𝑡 has type 𝑇 w.r.t. store typing Σ if for all 𝜎 : Σ, term 𝑡 evaluates to a value of type 𝑇 , a
final store 𝜎 ′ and a store typing Σ′ , such that 𝜎 ′ : Σ′ and Σ ⊑ Σ′ .
   The Compatibility Lemmas, Fundamental Theorem and Adequacy. The semantic typing
judgment Γ |= 𝑡 : 𝑇 is defined in Fig. 2 (bottom, ignoring the highlighted formula). It means that
term 𝑡 inhabits the term interpretation of type 𝑇 under any value environment 𝐻 and store typing Σ
that satisfies the semantic interpretation of the typing context 𝐺 [[Γ]], as defined in Fig. 2 (bottom).
The semantic typing rules have the same shape as the syntactic ones, but turning the symbol ⊢ (in
Fig. 1) into the symbol |=. Each of the semantic typing rules is a compatibility lemma.
   Theorem 2.1. (Fundamental Theorem of Unary Logical Relations) Every syntactically well-typed
term is semantically well-typed, i.e., if Γ ⊢ 𝑡 : 𝑇 , then Γ |= 𝑡 : 𝑇 .
  The following theorem entails that a semantically typed term always terminates. The termination
property is defined as part of the semantic typing judgment.
   Theorem 2.2. (Adequacy of Unary Logical Relations) Every closed semantically well-typed term 𝑡
is safe: if ∅ |= 𝑡 : T, then ∃ 𝑣, 𝜎. 𝑡, ∅, ∅ ⇓ 𝑣, 𝜎.
  The fundamental theorem (Theorem 2.1) follows immediately from the compatibility lemmas,
and Theorem 2.2 (Adequacy) and semantic type safety follow from the fundamental theorem
(Theorem 2.1) and the definition of semantic term interpretation Γ |= 𝑡 : 𝑇 and 𝐸 [[𝑇 ]].

2.3    Rediscovering Reachability Types
The logical definition allows us to establish strong theoretical re- def m() {
sults such as semantic type soundness and termination but remains       val x = new Ref(1)

fairly limited in describing program behavior in other ways. Firstly,   val y = new Ref(2)

it does not allow us to prove the assertion true on the right, as       def f () = { y += 1 }
                                                                        f()
the logical definition does not say anything about preserving store
                                                                        assert (!x == 1)
values across certain operations. Secondly, the assertion statement
                                                                      }
gets stuck if !x == 1 is false, thus it is an unsafe feature [Timany
et al. 2024], although the example uses it safely, which cannot be Fig. 3. Safe use of unsafe feature
proven using the given logical definitions. 6 7                       encapsulated in function m.5

5 The code that omits the assertion statement can be encoded as a sequence of 𝜆-abstractions and applications in our systems.
6 Those are not the general motivations behind reachability types, but rather to give an explanation for some requirements

of an effective logical relations model. Please refer to prior works [Bao et al. 2021; Wei et al. 2024] for general motivation.
7 See an informal justification of the safe use of the assertion statement in Fig. 3, using our binary logical relations in

Section 4.3, but our goal is not primarily to verify safe use of general unsafe code like Jung et al. [2018a]’s work.
8                                                Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf


  The highlighted formulas in Fig. 2 illustrate that information about reachable locations from
given values can give us useful semantic store invariants. We first introduce function 𝐿(𝑣) (Fig. 2,
top) that computes reachable locations from value 𝑣. In Fig. 3, function m reaches what its free
variables reach; i.e., ∅.
  With the knowledge of reachable locations, instead of using the standard definition of store typing
extension, we introduce relational store typing (RST), written as Σ ⊑ L Σ′ , which parameterizes the
definition of store typing extension with reachable locations L. RST is symmetric, allowing Σ′ to
be defined from Σ, such that they agree on L, leaving the remainder unspecified.8 The standard
definition of store typing extension Σ ⊑ Σ′ can be defined as Σ ⊑ dom(Σ) Σ′ .
   The Time Travelling Property. Now the reasoning can time travel between a past store typing
and another (possible future) one back and forth, as long as they agree on reachable locations, i.e.,
formula 1 , which is characterized by the following lemma:

    Lemma 2.3 (Time Travelling). If (𝐻, Σ, 𝑣) ∈ 𝑉 [[𝑇 ]], and Σ ⊑ 𝐿(𝑣) Σ′ , then (𝐻, Σ′, 𝑣) ∈ 𝑉 [[𝑇 ]].

   The lemma allows us to establish that the triple (𝐻, Σ′, 𝑣) is a valid element of 𝑉 [[𝑇 ]] if we know
(𝐻, Σ, 𝑣) is valid as long as the two store typings agree on the locations reachable from value 𝑣.
   In the interpretation of function types, formula 1 states that types are only preserved w.r.t.
reachable locations from function values, which gives us a degree of local reasoning, as Σ′ does
not assume anything from Σ that is not reachable from the function value. Under this assumption
together with the argument value being semantically well-typed in Σ′ , the safe reduction of the
function body implies that functions can only access locations reachable from their arguments
and themselves. This characterizes a separation logic [O’Hearn et al. 2001; Reynolds 2002] style of
reasoning, but without enforcing exclusiveness of ownership, uniqueness, or immutability.
   In the example of Fig. 3, formula 1 implies no store locations are needed in the pre-store (specified
by Σ), characterizing proper encapsulation. In function m, function f reaches what y reaches, which
is separate from what x reaches. Thus, we can prove the assertion true by formula 4 .
   In addition, with the reachability information, the value interpretation of function types can
also know that an argument is either separate from the function, or has some overlap with the
function (formula 2 ). This is a tautology here, but we will see that our reachability qualifiers can
specify how argument values nontrivially interact with function values in Section 3. The return
value may further reach fresh locations (formula 3 ). In the proof context, we know fresh locations
are part of Σ′′ , so it is redundant to use Σ′′ − Σ′ here. A similar refinement is adapted to the term
interpretation. Now, for 𝜆𝐵 , the semantic typing judgment for open terms 𝑡 can be localized to 𝑡’s
free variables, as formulated by the highlighted formula in Fig. 2 (bottom).
   Having added these semantic store invariants to the logical relation, why don’t we expose them
to the programmer as features of the type system? This is precisely the idea of reachability types.

3    Semantic Type Soundness of 𝜆Bq
In this section, we first present the reachability type system 𝜆Bq that tracks aliasing and expresses
values reachable from a given expression’s result, define its value interpretation of types and
terms, and present the semantic typing rules and show semantic type soundness. Then we present
  q (in Section 3.5) that extends 𝜆 q with subtyping, and 𝜆 q (in Section 3.6) that extends 𝜆 q to
𝜆B<:                                  B                                                          B
support higher-order mutable references. Finally, we present 𝜆𝜺q (in Section 3.7) that extends 𝜆 q
with observable write effect qualifiers, demonstrating a stronger value preservation property than
what is defined for 𝜆 q .

8 Starting from Section 3, we adopt the notation Σ ≡ 𝐿 Σ′ to reflect the symmetric nature of the RST.
Modeling Reachability Types with Logical Relations                                                                                      9



   Syntax                                                                                                                         𝜆Bq
      𝑐             :=    true | false                                                      Literals
      𝑡             ::=   𝑐 | 𝑥 | (𝜆𝑥 .𝑡 ) 𝑞 | 𝑡 1 𝑡 2 | ref 𝑡 | ! 𝑡 | 𝑡 := 𝑡 | 𝑡 1 ; 𝑡 2   Terms
      𝑟, 𝑠          ∈     Pfin (Var ⊎ {q} ⊎ {s} )                                           Function Domain/Codomain Qualifiers
      𝑝, 𝑜          ∈     Pfin (Var ⊎ {q} )                                                 Reachability Qualifiers
      𝜑, 𝑞          ∈     Pfin (Var)                                                        Observations
      𝑆,𝑇 , 𝑈 , 𝑉   ::=   𝐵𝑜𝑜𝑙 | (𝑥 :𝑇 𝑠 ) → 𝑈 𝑟 | Ref 𝑇 𝑝                                  Types
      Γ             ::=   ∅ | Γ, 𝑥 : 𝑇 𝑝                                                    Typing Environments
      𝑣             ::=   𝑐 | ℓ | ⟨𝐻, (𝜆𝑥 .𝑡 ) 𝑞 ⟩                                          Values

                    Fig. 4. The syntax of 𝜆Bq . Differences from 𝜆𝐵 (in Fig. 1) are highlighted.

3.1   The 𝜆Bq Language
Fig. 4 shows the syntax of 𝜆Bq , where the differences from 𝜆𝐵 (in Fig. 1) are highlighted. Terms
follow 𝜆𝐵 , except that 𝜆 terms are in the form of (𝜆𝑥 .𝑡)𝑞 , carrying a reachability qualifier 𝑞 that
includes the function’s captured variables. 𝜆Bq adds reachability qualifiers to its type language and
allows dependent function types, which are in the form of (𝑥 : 𝑇 𝑠 ) → 𝑈 𝑟 , where both argument
and return types are qualified. The codomain 𝑈 𝑟 may depend on the argument 𝑥 in its qualifier 𝑟 .
To avoid dealing with deep substitution, we prohibit references to 𝑥 from inside 𝑈 . This restriction
is purely technical; some prior works [Wei et al. 2024] do allow deep references, but this choice
does not appear to impact expressiveness in any significant way [Jia et al. 2024] as deep references
can also be modeled indirectly via chains of argument and self-references.
   Following prior works on reachability types [Bao et al. 2021; Wei et al. 2024], types in 𝜆Bq are of
the form 𝑇 𝑝 , where 𝑝 is a reachability qualifier, a finite set of variables that may include the distinct
freshness marker q, representing the values reachable from the given expression’s result.
   For simplicity, we introduce a self-reference marker s, rather than formalizing self-references
𝜆𝑓 as a binder of a 𝜆 term (as in prior works [Bao et al. 2021; Wei et al. 2024]). The self-reference
marker s may appear in the qualifiers of a function’s argument and its result, often expressed by
the symbols 𝑠 and 𝑟 as shown in Fig. 4. If present, it denotes that the corresponding value may reach
what the function reaches. This simplified formalization does not change the use of self-references
in prior works [Bao et al. 2021; Wei et al. 2024], but frees us from engaging in reasoning about
recursion within the logical definitions, which could otherwise be done using well-established
techniques such as step-indexing [Ahmed et al. 2009; Ahmed 2004; Appel and McAllester 2001].
   Mutable reference types Ref 𝑇 𝑝 track the known aliases of the value held by the reference. We
use observation 𝜑, which is a finite set of variables, to specify which variables in the typing context
Γ are observable, where the typing context assigns qualified typing assumptions to variables.

3.2   Store Typing and Semantic Typing Context
We refine the definition of store typings from Fig. 2 by adding reachable locations to each entry.
Now, a store typing Σ maps from locations to pairs of semantic types and reachable locations,
as shown in Fig. 5. A well-formed store 𝜎 w.r.t. store typing Σ demands that each location ℓ in
𝜎 stores well-typed values (w.r.t. Σ), which reach the empty set of locations, i.e. 𝐿 (𝜎 (ℓ ) ) ⊆ ∅ . This
condition reflects the restriction in 𝜆Bq , where reference types are limited to the form of Ref 𝑇 ∅ ,
i.e., the referent of a reference does not reach any locations. This restriction is relaxed by 𝜆 q in
Section 3.6.
   Our logical definition is established on a well-defined logical program state, which is defined in
the semantic typing context 𝐺 [[Γ 𝜑 ]] shown in Fig. 5 (bottom). The logical program state specifies
what can be observed by the observation 𝜑, as anything outside the observation is irrelevant. In
10                                                       Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf



     Interpretation of Value Reachability                                                                                         𝜆Bq
                                                                                          Ð
      𝐿 (𝑐 ) = ∅       𝐿 (ℓ ) = {ℓ }     𝐿 ( ⟨𝐻, (𝜆𝑥 .𝑡 ) 𝑞 ⟩ ) = [[𝑞 ]] 𝐻   [[𝑞 ]] 𝐻 =   𝑥 ∈𝑞 𝐿 (𝐻 (𝑥 ) )
     Variable Reachability and Qualifier Saturation                                                           Γ ⊢𝑥 { 𝑥      Γ ⊢ 𝑞∗
         Reachability Relation         Γ ⊢ 𝑥 { 𝑦 ⇔ 𝑥 : 𝑇 𝑞,𝑦 ∈ Γ             Variable Saturation      Γ ⊢ 𝑥∗ := { 𝑦 | 𝑥 { ∗ 𝑦 }
                                       Γ ⊢ 𝑞∗ :=
                                                   Ð
         Qualifier Saturation                      𝑥 ∈𝑞 𝑥∗
     Unary Logical Relations
                    Σ ::= ∅ | Σ, ℓ : (V, L )
                   Σ ⊑ L Σ′ = L ⊆ dom(Σ) ∧ L ⊆ dom(Σ′ ) ∧ (∀ ℓ ∈ L. Σ(ℓ ) = Σ′ (ℓ ′ ) )
                             def

                      𝜎 : Σ = dom(𝜎 ) = dom(Σ) ∧ (∀ℓ ∈ dom(𝜎 ). ∃ V.Σ(ℓ ) = (V, ∅ ) ∧ 𝜎 (ℓ ) ∈ V ∧ 𝐿 (𝜎 (ℓ ) ) ⊆ ∅ )
                             def

                             def
                   WF(Σ, 𝑣) = 𝐿 (𝑣) ⊆ dom(Σ)
                   WF(𝑝𝑥Γ ) = 𝑝˜ ⊆ dom(Γ1 )        where Γ = Γ1 , 𝑥 : 𝑇 𝑝 , Γ2 for some 𝑇
                             def

                   𝜎→ 𝐿 𝜎 ′ = ∀ℓ ∈ dom(𝜎 ). ℓ ∉ 𝐿 ⇒ 𝜎 (ℓ ) = 𝜎 ′ (ℓ )

             𝑉 [[𝐵𝑜𝑜𝑙 ]] = { (𝐻, Σ, 𝑐 ) }
           𝑉 [[Ref 𝑇 ∅ ]] = { (𝐻, Σ, ℓ ) | WF(Σ, ℓ ) ∧ (∃ V, Σ(ℓ ) = (V, ∅) ∧ (∀ Σ′ , 𝑣. 𝐿 (𝑣) ⊆ ∅ ⇒
                               (𝑣 ∈ V ⇐⇒ (𝐻, Σ′ , 𝑣) ∈ 𝑉 [[𝑇 ]] ) ) ) }

 𝑉 [[ (𝑥 : 𝑇 𝑠 ) → 𝑈 𝑟 ]] = { (𝐻, Σ, ⟨𝐻 ′ , (𝜆𝑥 .𝑡 ) 𝑞 ⟩ ) | WF(Σ, ⟨𝐻 ′ , (𝜆𝑥 .𝑡 ) 𝑞 ⟩ ) ∧ (∀ 𝑣, 𝜎 ′ , Σ′ . 1 Σ ≡ [[𝑞 ]] 𝐻 ′ Σ′ ∧
                               𝜎 ′ : Σ′ ∧ (𝐻, Σ′ , 𝑣) ∈ 𝑉 [[𝑇 ]] ∧ 2 𝐿 (𝑣) ⊆ [[𝑠˜ ]] 𝐻 ∪s∈𝑠 [[𝑞 ]] 𝐻 ′ ∪q∈𝑠 [[𝑞 ]] 𝐻 ′ ⇒
                                     ∃ 𝜎 ′′ , Σ′′ , 𝑣 ′ . 𝐻 ′ ; (𝑥, 𝑣), 𝜎 ′ , 𝑡 ⇓ 𝑣 ′ , 𝜎 ′′ ∧ 𝜎 ′′ : Σ′′ ∧ Σ′ ⊑ Σ′′ ∧
                                            (𝐻, Σ′′ , 𝑣 ′ ) ∈ 𝑉 [[𝑈 ]] ∧
                                             3 𝐿 (𝑣 ′ ) ⊆ ( [[𝑟˜ \𝑥 ]] 𝐻 ∩ [[𝑞 ]] 𝐻 ′ ) ∪𝑥 ∈𝑟 𝐿 (𝑣) ∪s∈𝑟 [[𝑞 ]] 𝐻 ′ ∪q∈𝑟 dom(Σ′ ) ) ∧
                                             4 𝜎 ′ → [[𝑞 ]] 𝐻 ′ ∪ 𝐿 (𝑣) 𝜎 ′′ }

               𝐸 [[𝑇 𝑝 ]] 𝜑 = { (𝐻, Σ, 𝑡 ) | ∀ 𝜎 . 𝜎 : Σ ∧ ∃ 𝜎 ′ , Σ′ , 𝑣 ′ . 𝐻, 𝜎, 𝑡 ⇓ 𝑣 ′ , 𝜎 ′ ∧ 𝜎 ′ : Σ′ ∧ Σ ⊑ Σ′ ∧
                                             (𝐻, Σ′ , 𝑣 ′ ) ∈ 𝑉 [[𝑇 ]] ∧ 𝐿 (𝑣 ′ ) ⊆ [[𝜑 ∩ 𝑝˜ ]] 𝐻 ∪q∈𝑝 dom(Σ) ∧ 𝜎→ [[𝜑 ]] 𝐻 𝜎 ′ }

                𝐺 [[Γ 𝜑 ]] = { (𝐻, Σ) | dom(𝐻 ) = dom(Γ) ∧ 𝜑 ⊆ dom(Γ) ∧ Inv𝑜 (Γ, 𝐻, Σ, 𝜑 ) ∧ Inv𝑆 (𝐻, Σ, 𝜑 ) }
        Inv𝑜 (Γ, 𝐻, Σ, 𝜑 ) = ∀ 𝑥,𝑇 , 𝑝. Γ (𝑥 ) = 𝑇 𝑝 ⇒ WF(𝑝𝑥Γ ) ∧ (𝑥 ∈ 𝜑 ⇒ (𝐻, Σ, 𝐻 (𝑥 ) ) ∈ 𝑉 [[𝑇 ]] ) ∧
                                                       (q ∉ 𝑝 ⇒ 𝐿 (𝐻 (𝑥 ) ) ⊆ [[ 𝑝˜ ]] 𝐻 )
          Inv𝑆 (𝐻, Σ, 𝜑 ) = ∀𝑝, 𝑝 ′ . 𝑝˜ ⊆ 𝜑 ∧ 𝑝˜′ ⊆ 𝜑 ⇒ [[ 𝑝˜ ]] 𝐻 ∩ [[ 𝑝˜′ ]] 𝐻 ⊆ [[ 𝑝∗
                                                                                       ˜ ∩ 𝑝˜′ ∗]] 𝐻

Fig. 5. The value interpretation of types, terms and typing context interpretation for 𝜆Bq . Differences from 𝜆𝐵
(in Fig. 2) are highlighted. Qualifiers 𝑠 and 𝑟 may include the self-references marker s, and are used to specify
function domain and codomain. The notation Σ ≡ 𝐿 Σ′ means the RST introduced in Section 2.


terms of encapsulation safety, the observation can also be considered as a boundary to another
world. The semantic typing context defines two reachability invariants: Inv𝑜 and Inv𝑆 . Invariant
Inv𝑜 states that locations reachable from non-fresh values are bounded by those from its qualifier.
   Invariant Inv𝑆 states that reachability qualifier intersection distributes over locations w.r.t. quali-
fier saturation, which is written as 𝑝∗. This invariant is critical for function applications, where
one needs to ensure an argument value is permissible to invoke the function by inspecting the ar-
gument’s qualifier against the prescribed separation/overlapping from a function’s type. Following
Wei et al. [2024]’s work, we assign minimal variable sets (called one-step reachability) and compute
transitive closures when checking separation/overlapping. Fig. 5 (top) recaps their definitions of
variable reachability and qualifier saturation, which compute all reachable variables transitively. In
addition, the predicate WF(𝑝𝑥Γ ) for 𝑥 : 𝑇 𝑝 ∈ Γ 𝜑 (defined in Fig. 5) prohibits cycles in qualifiers, as
the typing context is extended with the binder (in a 𝜆 term), where a parameter’s qualifier is in the
same scope as the 𝜆 term. Thus, cycles in qualifiers are not syntactically well-formed.
Modeling Reachability Types with Logical Relations                                                    11


3.3   The Logical Interpretation of Types and Terms
The definitions of logical interpretation of types and terms are shown in the middle of Fig. 5. They
follow a similar logical structure as for 𝜆𝐵 in Fig. 2, but are enriched with the knowledge about
reachability specified by the qualifiers in types (highlighted).
   We use the notation ∪𝑏 to denote the conditional set union operator, i.e., if the predicate 𝑏 is true,
the operator performs a union of the left- and right-hand operands; otherwise, the result defaults to
the left-hand operand only. Let 𝑝 be a reachability qualifier that may include the freshness marker q
and the self-reference marker s. We write 𝑝˜ to denote dropping the freshness and the self-reference
markers in 𝑝, resulting in the set of variables appearing in 𝑝, i.e., 𝑝˜ := 𝑝 \ (q, s).
   Interpretation of Reachability. Fig. 5 (top) refines function 𝐿(𝑣) that computes reachable
locations from value 𝑣 for 𝜆Bq . The definition follows that for 𝜆𝐵 (Fig. 2), except for function values.
Here, reachable locations from a closure record ⟨𝐻, (𝜆𝑥 .𝑡)𝑞 ⟩ include those from its qualifier, i.e.,
[[𝑞]] 𝐻 , which computes reachable locations from variables in 𝑞. We often write [[𝑞]] 𝐻 for the
reachable locations from a closure record when the context is clear.
   Well-Defined Reachable Locations. To use the reachability information in logical definitions,
we use the predicate WF(Σ, 𝑣) (shown in Fig. 5) to guarantee reachable locations from a value 𝑣
are well-defined w.r.t. a store typing Σ, i.e., 𝐿(𝑣) ⊆ dom(Σ). For example, a location ℓ can only
reach itself. Thus the predicate WF(Σ, ℓ) checks ℓ ∈ dom(Σ). For values of type 𝐵𝑜𝑜𝑙, their reachable
locations are the empty set. So their well-defined predicates are trivially true, and thus are omitted
from its value interpretation.
   Reference Types. The value interpretation of reference type Ref 𝑇 ∅ are store locations that hold
values of type 𝑇 , and their contents reach the empty set of locations. Comparing with 𝜆𝐵 that only
allows references to hold Boolean values, here, references can store any typeable values as long as
they reach the empty set of locations.
   Function Types. The logical interpretation of function type (𝑥 : 𝑇 𝑠 ) → 𝑈 𝑟 is defined in Fig. 5,
where 𝑠, 𝑇 and 𝑈 are closed under value environment 𝐻 . Their closedness predicates are omitted in
the figure, and in the logical definitions in the subsequent sections. The qualifier of the return value
may include parameter 𝑥, as well as the freshness and self-reference markers. The qualifiers of a
function and its argument specify how the argument value communicates with its function value
(formula 2 ). Here, we discuss several examples in Wei et al. [2024]’s work against the formula.
Consider the following reachability-polymorphic identity function:
def id(x: Tq ): T{x} = x            // : ((x: Tq ) => T{x} )∅

The type specifies that id cannot reach anything from its context (𝑞 = ∅ in 2 ), and accepts argument
values that may reach separate locations from what id reaches (𝑠 = q in 2 ). Thus, the id function
accepts any values of type T.
  A different parameter qualifier specifies permissible overlapping between functions and their
argument values. Consider the following variants of id which capture some variable z in the context:
def id2(x: T{ q } ): T{x} = { val u = z; x }         // : ((x: T{ q } ) => T{x} ){z}
def id3(x: T{ q ,z} ): T{x} = { val u = z; x }       // : ((x: T{ q ,z} ) => T{x} ){z}

The qualifiers on the function types and their parameters specify the reachability assumption that
the implementation can observe about its context (𝑞 = {𝑧} in 2 ), and about any given argument
value, respectively. Function id2 accepts arguments reaching anything that does not (directly or
transitively) reach z (𝑠 = q in 2 ), and id3 permits z in the parameter’s qualifier, i.e., allowing any
argument (𝑠 = {q, 𝑧} in 2 ).
   The reachability qualifiers of return values express how they communicate with arguments and
function values (formula 3 ). Consider the following function that mutates a captured reference
12                                             Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf


cell and returns the argument (here, 𝑞 = {𝑐1}, 𝑠 = {𝑐1, q}). We annotate that the argument x is
potentially aliased with the captured argument c1 but apply the function with argument c2. Our type
system would not propagate such imprecision by tracking one-step reachability. The return type
only tracks the argument x (𝑟 = {𝑥 } in 3 ), meaning the return value reaches what the argument
reaches. When applying different arguments to the function, precise reachability is retained:
... // c1: T{c1} , c2: T{c2}
def incr(x: T{c1, q } ): T{x} = { c1 := !c1 + 1; x } // : ((x: T{c1, q } ) => T{x} ){c1}
incr(c1)                                               // : T{c1}
incr(c2)                                               // : T{c2} ← precision retained

The logical definition precisely captures our crucial design that has the freshness marker q in
qualifiers to explicitly communicate (non-)freshness, which is preserved by dependent application
and substitution [Wei et al. 2024] (see rule t-appq in Fig. 6).
   If the argument’s qualifier includes both the self-reference and the freshness markers, any
argument values of the proper pretype are allowed. If the self-reference marker appears in the
return value’s qualifier, as in the cell example in Section 2.1, it means the return value can reach
whatever the returning closure reaches.
  The Term Interpretation. The term interpretation also adds the interpretation of reachability
for its result values 𝑣. If the result value 𝑣 is not fresh, then we check that its reachable locations
are bounded by those from the reachability qualifier observed by the observation 𝜑, i.e., 𝜑 ∩ 𝑝;      ˜
otherwise, it may additionally include fresh locations dom(Σ). The preserved store values are those
not reachable from observation 𝜑.

3.4   The Compatibility Lemmas, Fundamental Theorem and Adequacy
The semantic typing judgment is defined as Γ 𝜑 |= 𝑡 : 𝑇 𝑝 = ∀ (𝐻, Σ) ∈ 𝐺 [[Γ 𝜑 ]]. (𝐻, Σ, 𝑡) ∈
                                                                          def

𝐸 [[𝑇 𝑝 ]] 𝜑 , meaning that term 𝑡 inhabits the term interpretation of type 𝑇 𝑝 under any value envi-
ronment 𝐻 and store typing Σ that satisfies the semantic interpretation of typing context 𝐺 [[Γ 𝜑 ]].
   Fig. 6 shows the semantic typing rules. For readability, we often drop the set notation for qualifiers
and write them down as comma-separated lists of atoms. Each of the rules is a compatibility lemma,
and has been proved in Rocq. The syntactic typing judgments have the form Γ 𝜑 ⊢ 𝑡 : 𝑇 𝑝 . The
syntactic typing rules have the same shape as the semantic one, but turning the symbol |= (in Fig. 6)
into the symbol ⊢ .
   We have proved the compatibility lemmas, fundamental theorem and adequacy for 𝜆Bq . The
fundamental theorem follows immediately from the compatibility lemmas, and adequacy, semantic
type safety, and termination follow from the fundamental theorem and the definition of semantic
term interpretation in Fig. 5.
  Encapsulation. Now, we study encapsulation property demanded for rule 𝛽-eqiv in Section 5.
The typing judgment Γ ∅ ⊢ 𝑡 : 𝑇 ∅ expresses encapsulated computations, which are logically
characterized by the following lemma:

  Lemma 3.1 (Encapsulated Computations (𝜆Bq )). If Γ ∅ ⊢ 𝑡 : 𝑇 ∅ , then ∀ (𝐻, Σ) ∈ 𝐺 [[Γ ∅ ]].
∀ Σ′ . Σ ≡ ∅ Σ′ ⇒ (𝐻, Σ′, 𝑡) ∈ 𝐸 [[𝑇 ∅ ]] ∅ .

Note that the notation Σ ≡ ∅ Σ′ means the RST introduced in Section 2. The lemma expresses that
expression 𝑡 is valid at type 𝑇 ∅ w.r.t. arbitrary store typing, including the empty one. Note that
term 𝑡 can be an implementation of an abstract data type, which may internally allocate new store
locations. The empty qualifier (in 𝑇 ∅ ) dictates that 𝑡’s evaluation result cannot be tracked, hence
are encapsulated.
Modeling Reachability Types with Logical Relations                                                                                              13


   Semantic Typing                                                                                                             Γ 𝜑 |= 𝑡 : 𝑇 𝑝

                                                Γ (𝑥 ) = 𝑇 𝑝        𝑥 ∈𝜑                                Γ 𝜑 |= 𝑡 1 : (Ref 𝑇 ∅ ) 𝑝
          Γ 𝜑 |= 𝑐 : 𝐵𝑜𝑜𝑙 ∅
                              (t-cst)
                                                     Γ 𝜑 |= 𝑥 : 𝑇 𝑥
                                                                               (t-var)                      Γ 𝜑 |= 𝑡 2 : 𝑇 ∅
                                                                                                                                         (t-:=)
                                                                                                        Γ 𝜑 |= 𝑡 1 := 𝑡 2 : 𝐵𝑜𝑜𝑙 ∅
                                               ′                ′
                (Γ, 𝑥 : 𝑇 𝜑∩(𝑠 [𝑞/s])∪q∈𝑠 q ) 𝑞 ,𝑥 |= 𝑡 : 𝑈 𝑟 [𝑞 /s]
                              𝑞′ = 𝜑 ∩ 𝑞        𝑠˜ ⊆ 𝑞 ′
                                      ′                                         (t-abs)                  Γ 𝜑 1 |= 𝑡 1 : 𝐵𝑜𝑜𝑙 𝑞1
                     Γ 𝜑 |= (𝜆𝑥 .𝑡 ) 𝑞 : ( (𝑥 : 𝑇 𝑠 ) → 𝑈 𝑟 ) 𝑞                                          Γ 𝜑 2 |= 𝑡 2 : 𝐵𝑜𝑜𝑙 𝑞2
                                                                                                         𝜑1 ⊆ 𝜑         𝜑2 ⊆ 𝜑
                  Γ 𝜑 |= 𝑡 1 : ( (𝑥 : 𝑇 𝑠 ) → 𝑈 𝑟 ) 𝑝 q ∉ 𝑠, 𝑜                                                                          (t-seq)
                                                                                                         Γ 𝜑 |= 𝑡 1 ; 𝑡 2 : 𝐵𝑜𝑜𝑙 ∅
        Γ 𝜑 |= 𝑡 2 : 𝑇 𝑜      𝑜˜ ⊆ 𝑠˜ ⊆ 𝜑      𝑟˜ ⊆ 𝜑, 𝑥    𝑥 ∉ fv(𝑈 )
                                                                                (t-app)
                          Γ 𝜑 |= 𝑡 1 𝑡 2 : 𝑈 𝑟 [𝑜/𝑥,𝑝/s]                                                     Γ 𝜑 |= 𝑡 : 𝑇 𝑝 1
                                                                                                         𝑝˜1 ⊆ 𝑝˜2 ⊆ dom(Γ)
          Γ 𝜑 |= 𝑡 1 : ( (𝑥 : 𝑇 𝑠 ) → 𝑈 𝑟 ) 𝑝 q ∈ 𝑠 𝑥 ∉ fv(𝑈 )                                          𝑝 3 = 𝑝 2 ∪q∈𝑝 1 ∨q∈𝑝 2 q
      Γ 𝜑 |= 𝑡 2 : 𝑇 𝑜      s ∉ 𝑠 ⇒ 𝑝∗˜ ∩ 𝑜∗ ˜ ⊆ 𝑠˜ 𝑠˜ ⊆ 𝜑 𝑟˜ ⊆ 𝜑, 𝑥                                         Γ 𝜑 |= 𝑡 : 𝑇 𝑝 3
                                                                                                                                        (t-sub)
                                                                               (t-appq)
                        Γ 𝜑 |= 𝑡 1 𝑡 2 : 𝑈 𝑟 [𝑜/𝑥,𝑝/s]
                                                                                                 Γ 𝜑 |= 𝑡 : 𝑈 𝑝         𝑥 ∈ 𝑝˜
             Γ 𝜑 |= 𝑡 : 𝑇 ∅                              Γ 𝜑 |= 𝑡 : (Ref 𝑇 ∅ ) 𝑝                  Γ (𝑥 ) = 𝑇 𝑞         𝑞⊆𝜑
                                      (t-ref)                                        (t-!)                                         (t-sub-var)
       Γ 𝜑 |= ref 𝑡 : (Ref 𝑇 ∅ ) q                           Γ 𝜑 |= !𝑡 : 𝑇 ∅                           Γ 𝜑 |= 𝑡 : 𝑈 𝑝 [𝑞/𝑥 ]

   Qualifier Substitution                                                                                             𝑟 [𝑝/𝑥 ]       𝑟 [𝑞/s]
                       𝑟 [𝑝/𝑥 ] = 𝑟 \ {𝑥 } ∪ 𝑝       𝑥 ∈𝑟                          𝑟 [𝑞/s] = 𝑟 \ {s} ∪ 𝑞        s∈𝑟
                       𝑟 [𝑝/𝑥 ] = 𝑟                  𝑥 ∉𝑟                          𝑟 [𝑞/s] = 𝑟                  s∉𝑟
   Qualifier Shorthands              𝑝, 𝑞 := 𝑝 ∪ 𝑞    𝑥 := {𝑥 }            q := {q}           s := {s}        qs𝑝 := {q} ∪ {s} ∪ 𝑝
                                     𝑝 ∪𝑏 𝑞 := 𝑏 = true ? 𝑝, 𝑞 : 𝑝                           𝑝˜ := 𝑝 \ (q, s)

Fig. 6. Semantic typing rules for 𝜆Bq . Qualifiers 𝑠 and 𝑟 may include the self-references marker s, and are used
to specify function domain and codomain.

3.5   Subtyping
To keep the exposition consistent with prior work [Wei et al. 2024], we extend 𝜆Bq with subtyping,
              q . Fig. 7 shows the interpretation of subqualifiers, subpretypes and subtypes, as
resulting in 𝜆B<:
well as the semantic subtyping rules. Qualifier subtyping includes the subset relation (q-sub and
q-sub-s), and transitivity (q-trans). Rule q-var is contextual and allows assigning the qualifier
to a type in the upper level of the reachability chain. Subtyping for reference type (s-ref) and
function type (s-fun) are standard modulo qualifiers. Rule s-fun additionally demands that if the
argument qualifier includes the self-reference marker, then it must be fresh. Subtyping for types
(sq-sub) forwards to qualifier subtyping and ordinary type subtyping judgments. Rule t-sub-stp
is the subsumption rule, allowing a term with a subtype to be safely used in a context where a
supertype is expected.
                                                                          q provides an ideal vehicle
   The semantic subtyping notion provided by the logical relations for 𝜆B<:
to identify subtyping rules in a specific scenario, which is not present in prior work [Wei et al.
2024]. Here we discuss one of the key technical points with the following example, demonstrating
how the local variable x from the result type’s qualifier can be replaced by the self-reference marker
s, by using stepwise subtyping rules.
                                 1               ′                    2                  ′         ′        3                  ′
   ((𝑥 : 𝑇 q,s ) → 𝑈 𝑥 )𝑞 <: ((𝑥 : 𝑇 𝑞 ) → 𝑈 𝑥 )𝑞 <: ((𝑥 : 𝑇 𝑞 ) → 𝑈 𝑞 )𝑞 <: ((𝑥 : 𝑇 𝑞 ) → 𝑈 s )𝑞
Here we assume 𝑞 ′ <: 𝑞. The step 1 is established by contravariance on the argument type, which is
always valid as the qualifier {q, s} permits any argument values of type 𝑇 . The step 2 is established
by covariance on the result type, provided {𝑥 } <: 𝑞 ′ by the rule q-var. The step 3 is valid only
in the context such that 𝑞 ′ <: 𝑞, meaning what is reachable from 𝑞 ′ is a subset of those reachable
14                                                         Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf



     Semantic Interpretation of Subqualifiers, Subpretypes and Subtypes                                                                    q
                                                                                                                                          𝜆B<:
                Γ |= 𝑞 1 <: 𝑞 2 = ∀ (𝐻, Σ) ∈ 𝐺 [[Γ ∅ ]]. [[𝑞 1 ]] 𝐻 ⊆ [[𝑞 2 ]] 𝐻
                                    def

                Γ |= 𝑇1 <: 𝑇2 = ∀ (𝐻, Σ) ∈ 𝐺 [[Γ ∅ ]]. ∀𝑣. (𝐻, Σ, 𝑣) ∈ 𝑉 [[𝑇1 ]] ⇒ (𝐻, Σ, 𝑣) ∈ 𝑉 [[𝑇2 ]]
                                def

            Γ |= 𝑇1 <: 𝑇2 = ∀ (𝐻, Σ) ∈ 𝐺 [[Γ 𝜑 ]]. ∀𝑡 . (𝐻, Σ, 𝑡 ) ∈ 𝐸 [[𝑇1 1 ]] 𝜑 ⇒ (𝐻, Σ, 𝑡 ) ∈ 𝐸 [[𝑇2 2 ]] 𝜑
             𝜑     𝑝1       𝑝 2 def                                              𝑝                       𝑝


     Semantic Typing                                                                                                             Γ 𝜑 |= 𝑡 : 𝑇 𝑝
                                                        Γ 𝜑 |= 𝑡 : 𝑇1 1     Γ 𝜑 |= 𝑇1 1 <: 𝑇2 2
                                                                     𝑝               𝑝       𝑝
                                                                                                            𝑝˜2 ⊆ 𝜑
                                  ···                                                                                 (t-sub-stp)
                                                                           Γ |= 𝑡 : 𝑇2
                                                                             𝜑         𝑝2


     Semantic Subtyping                                               Γ |= 𝑝 <: 𝑝      Γ |= 𝑠 <: 𝑠       Γ |= 𝑇 <: 𝑇         Γ 𝜑 |= 𝑇 𝑝 <: 𝑈 𝑜

                                                                                              Γ |= 𝑈 <: 𝑆          Γ |= 𝑆 <: 𝑈
         𝑝 1 ⊆ 𝑝 2 ⊆ q dom(Γ)                 𝑠 1 ⊆ 𝑠 2 ⊆ qs dom(Γ)                          Γ |= 𝑝 1 <: 𝑝 2       Γ |= 𝑝 2 <: 𝑝 1
                                                                                                                                          (s-ref)
             Γ |= 𝑝 1 <: 𝑝 2                       Γ |= 𝑠 1 <: 𝑠 2                             Γ |= Ref 𝑈 𝑝 1 <: Ref 𝑆 𝑝 2
                                (q-sub)                           (q-sub-s)
                                                                                    Γ |= 𝑇2 <: 𝑇1 Γ |= 𝑈 1 <: 𝑈 2 s ∈ 𝑠 1 ⇒ q ∈ 𝑠 1
                                                                                           Γ |= 𝑠 2 <: 𝑠 1 Γ, 𝑥 : 𝑇2 2 |= 𝑟 1 <: 𝑟 2
                                                                                                                    𝑠
                  Γ (𝑥 ) = 𝑇 𝑞2     𝑥 ∈ 𝑞1    𝑞 1 ⊆ dom(Γ)
                                                                                           Γ |= 𝑇1 1 → 𝑈 1 1 <: 𝑇2 2 → 𝑈 2 2
                                                                    (q-var)                          𝑠         𝑟         𝑠          𝑟
                          Γ |= q𝑞 1 <: q𝑞 1 [𝑞 2 /𝑥 ]
                                                                                                                                         (s-fun)
                                                                                              Γ |= 𝑆 <: 𝑇             Γ |= 𝑝 <: 𝑞
     Γ |= 𝑝 1 <: 𝑝 2   Γ |= 𝑝 2 <: 𝑝 3                   Γ ⊢ 𝑇 wf                                                                       (sq-sub)
                                          (q-trans)                   (s-refl)                           Γ 𝜑 |= 𝑆 𝑝 <: 𝑇 𝑞
              Γ |= 𝑝 1 <: 𝑝 3                           Γ |= 𝑇 <: 𝑇
                                                                                   q .
                                             Fig. 7. Semantic subtyping rules for 𝜆B<:


from the function’s qualifier 𝑞. This kind of stepwise reasoning enables a sound way of introducing
self-references via subtyping to type escaping values without term-level coercions. See Jia et al.
[2024]’s work for more detailed elaboration.
   The Compatibility Lemmas, Fundamental Theorem and Adequacy. The syntactic subquali-
fiers, subpretyping and subtyping judgments and those syntactic rules have the same form as the
semantic ones, but turning the symbol |= (in Fig. 7) into the symbol ⊢ .

  Theorem 3.2 (Fundamental Theorem of Subqalifiers). Every syntactically well-typed sub-
qualifier relation is semantically well-typed, i.e., if Γ ⊢ 𝑝 1 <: 𝑝 2 , then Γ |= 𝑝 1 <: 𝑝 2 , and if Γ ⊢ 𝑠 1 <: 𝑠 2 ,
then Γ |= 𝑠 1 <: 𝑠 2

  Theorem 3.3 (Fundamental Theorem of Subpretypes). Every syntactically well-typed subpre-
type relation is semantically well-typed, i.e., if Γ ⊢ 𝑇1 <: 𝑇2 , then Γ |= 𝑇1 <: 𝑇2

   Theorem 3.4 (Fundamental Theorem of Subtypes). Every syntactically well-typed subtype
relation is semantically well-typed, i.e., if Γ 𝜑 ⊢ 𝑇1 1 <: 𝑇2 2 , then Γ 𝜑 |= 𝑇1 1 <: 𝑇2 2
                                                      𝑝       𝑝                  𝑝       𝑝



   The definition of semantic typing for 𝜆B<: q follows what is defined for 𝜆 q , i.e., Γ 𝜑 |= 𝑡 : 𝑇 𝑝 =                                          def
                                                                               B
∀ (𝐻, Σ) ∈ 𝐺 [[Γ ]]. (𝐻, Σ, 𝑡) ∈ 𝐸 [[𝑇 ]] 𝜑 , meaning that term 𝑡 inhabits the term interpretation of
                𝜑                     𝑝

type 𝑇 𝑝 under any value environment 𝐻 and store typing Σ that satisfies the semantic interpretation
of typing context 𝐺 [[Γ 𝜑 ]].
   We have proved the compatibility lemmas, fundamental theorem and adequacy for 𝜆B<:            q . The

fundamental theorem follows immediately from the compatibility lemmas, and adequacy and
semantic type safety follow from the fundamental theorem and the definition of semantic term
interpretation.
Modeling Reachability Types with Logical Relations                                                           15


3.6   Extension with Higher-Order Mutable References (𝜆 q )
As presented so far, 𝜆Bq only supports first-order mutable references, i.e., mutable references cannot
hold values that contain references to other store locations. In this section, we introduce 𝜆 q , which
extends 𝜆Bq to support higher-order mutable references. We outline the major differences from 𝜆Bq
here.
    The 𝜆 q Language. We relax the restriction on referent type 𝑇 ∅ for mutable references, i.e., a
referent’s type can now carry a reachability qualifier 𝑇 𝑞 , indicating that the referent is a non-fresh
value of type 𝑇 , and may reach locations specified by 𝑞.
    Following 𝜆Bq , a store typing maps from locations to pairs of semantic types and reachable
locations. Let ℓ be a location in store typing Σ, such that Σ(ℓ) = (V, L), for some V and L, where V
is its semantic type, and L prescribes the set of locations reachable from the value stored in location
ℓ. As location ℓ can indirectly reach some locations in a store, following prior work [Wei et al. 2024],
we use location saturation, written as L∗Σ , to transitively compute reachable sets, and demand that
the saturated reachable locations from the content is a subset of the saturated ones from L. In
addition, following the syntactic typing rules that disallow cyclic references [Wei et al. 2024], our
logical definition requires that earlier allocated locations cannot reach those allocated later, which
is defined in 𝜎 : Σ, i.e., ∀ℓ ′ ∈ L. ℓ ′ < ℓ. Here, store locations are ordered by their allocation time.
    The Logical Interpretation of Types and Terms. The definitions of the value interpretation of
types, terms, and typing contexts (shown in Fig. 8) follow 𝜆Bq , but taking location saturation into
consideration. For example, the predicate WF(Σ, 𝑣) is refined to ensure all the indirectly reachable
locations are well-defined w.r.t. a store typing, i.e., WF(Σ, 𝑣) = 𝐿(𝑣) ∗Σ ⊆ dom(Σ).
    Similarly, in the definition of value interpretation of Boolean and function types, and term
interpretation, the reachability properties defined by 𝐿(𝑣) and [[𝑞]] 𝐻 for 𝜆Bq are now defined using
location saturation, i.e., 𝐿(𝑣) ∗Σ and [[𝑞]] 𝐻Σ ∗ for some store typing Σ. For example, formula 2 in Fig. 5
is refined to 𝐿(𝑣) ∗Σ′ ⊆ [[𝑠]]
                                 ′                ′                ′
                            ˜ 𝐻Σ′ ∗ ∪s∈𝑠 [[𝑞]] 𝐻Σ′ ∗ ∪q∈𝑠 [[𝑞]] 𝐻Σ′ ∗ .
                                        𝑞
    Values of reference type Ref 𝑇 are store locations ℓ, where its content may change over time,
but must always be of type 𝑇 . The reachability qualifier 𝑞 allows the reasoning to time travel
back and forth between two store typings as long as they agree on the reachable locations from
the referent. Thus, the value interpretation of a reference type Fig. 5 is refined to (∀ Σ′, 𝑣. Σ ≡
L∗Σ Σ ∧ 𝐿(𝑣) Σ′ ⊆ LΣ′ ⇒ (𝑣 ∈ V ⇐⇒ (𝐻, Σ , 𝑣) ∈ 𝑉 [[𝑇 ]])), where LΣ is the logical interpretation
     ′        ∗       ∗                              ′                        ∗

of 𝑞, i.e., L = [[𝑞]] 𝐻 .
    The Time Travelling Property. The time travelling lemma (Lemma 2.3 in Section 2) is refined
with saturated locations as follows:
   Lemma 3.5 (Time Travelling (𝜆 q )). If (𝐻, Σ, 𝑣) ∈ 𝑉 [[𝑇 ]], and Σ ≡ 𝐿(𝑣) ∗Σ Σ′ , then (𝐻, Σ′, 𝑣) ∈ 𝑉 [[𝑇 ]].
The lemma allows the validity of the value 𝑣 at type 𝑇 to be preserved from store typing Σ to
another Σ′ , as long as they agree on the saturated locations reachable from value 𝑣.
   The Compatibility Lemmas, Fundamental Theorem and Adequacy. The definition of se-
mantic typing judgment follows what was defined for 𝜆Bq in Fig. 5. Fig. 8 shows the selected semantic
typing rules. Following prior work [Wei et al. 2024], the type system supports a restricted form of
nested references: only non-fresh values can be stored/read from/written into in a reference (t-ref,
t-! and t-:=). As referent qualifiers are invariant, store typing is monotonic. Each of the semantic
typing rules is a compatibility lemma, and has been proven in Rocq.
   We have proved the compatibility lemmas, fundamental theorem and adequacy for 𝜆 q . The
fundamental theorem follows immediately from the compatibility lemmas, and adequacy, semantic
type safety, and termination follow from the fundamental theorem and the definition of semantic
term interpretation.
16                                                             Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf



     Location Saturation                                                                                                                       𝜆q
      ℓ { Σ ℓ ′ ⇔ Σ(𝑙 ) = (V, L ∪ {ℓ ′ } )           ℓΣ∗ ⇔ {ℓ ′ | ℓ { ∗Σ ℓ ′ }       L∗Σ := ℓ ∈L ℓΣ∗
                                                                                           Ð


     Unary Logical Relations
               WF(Σ, 𝑣) = 𝐿 (𝑣) ∗Σ ⊆ dom(Σ)
                      Σ ::= ∅ | Σ, ℓ : (V, L)
                        𝜎 : Σ = dom(𝜎 ) = dom(Σ) ∧ (∀ℓ ∈ dom(𝜎 ). ∃ V, L. Σ(ℓ ) = (V, L) ∧ 𝜎 (ℓ ) ∈ V ∧
                               def

                                 1 𝐿 (𝜎 (ℓ ) ) ∗Σ ⊆ L∗Σ ∧ 2 (∀ℓ ′ ∈ L. ℓ ′ < ℓ ) )

                  𝑉 [[𝐵𝑜𝑜𝑙 ]] = { (𝐻, Σ, 𝑐 ) }

               𝑉 [[ Ref 𝑇 𝑞 ]] = { (𝐻, Σ, ℓ ) | WF(Σ, ℓ ) ∧ (∃ V, L. Σ(ℓ ) = (V, L) ∧ L = [[𝑞 ]] 𝐻 ∧ L∗Σ ⊆ ℓΣ∗ ∧
                                      (∀ Σ′ , 𝑣.Σ ≡ L∗Σ Σ′ ∧ 𝐿 (𝑣) ∗Σ′ ⊆ L∗Σ′ ⇒ (𝑣 ∈ V ⇐⇒ (𝐻, Σ′ , 𝑣) ∈ 𝑉 [[𝑇 ]] ) ) ) }

     𝑉 [[ (𝑥 : 𝑇 𝑠 ) → 𝑈 𝑟 ]] = { (𝐻, Σ, ⟨𝐻 ′ , (𝜆𝑓 (𝑥 ).𝑡 ) 𝑞 ⟩ ) | WF(Σ, ⟨𝐻 ′ , (𝜆𝑓 (𝑥 ).𝑡 ) 𝑞 ⟩ ) ∧ (∀ 𝑣, 𝜎 ′ , Σ′ . Σ ≡ [[𝑞 ]] 𝐻Σ ∗ Σ′ ∧
                                                                                                                                       ′




                                         𝜎 ′ : Σ′ ∧ (𝐻, Σ′ , 𝑣) ∈ 𝑉 [[𝑇 ]] ∧ 𝐿 (𝑣) ∗Σ′ ⊆ [[𝑠˜ ]] 𝐻Σ′ ∗ ∪s∈𝑠 [[𝑞 ]] 𝐻Σ′ ∗ ∪q∈𝑠 [[𝑞 ]] 𝐻Σ′ ∗ ⇒
                                                                                                            ′              ′            ′



                                         ∃ Σ′′ , 𝜎 ′′ , 𝑣 ′ . 𝐻 ′ ; (𝑥, 𝑣), 𝜎 ′ , 𝑡 ⇓ 𝑣 ′ , 𝜎 ′′ ∧ Σ′ ⊑ Σ′′ ∧ 𝜎 ′′ : Σ′′ ∧
                                               (𝐻, Σ′′ , 𝑣 ′ ) ∈ 𝑉 [[𝑈 ]] ∧
                                               𝐿 (𝑣 ′ ) ∗Σ′′ ⊆ ( [[𝑟˜ \𝑥 ]] 𝐻Σ′′∗ ∩ [[𝑞 ]] 𝐻Σ′′∗ ) ∪𝑥 ∈𝑟 𝐿 (𝑣) ∗Σ′′ ∪s∈𝑟 [[𝑞 ]] 𝐻Σ′′∗ ∪q∈𝑟 dom(Σ′ ) ∧
                                                                               ′              ′                                    ′


                                                ′                           ′′
                                               𝜎 → [[𝑞 ]] 𝐻Σ ∗ ∪ 𝐿 (𝑣) ∗Σ′ 𝜎 ) }
                                                           ′
                                                          ′




                  𝐸 [[𝑇 𝑝 ]] 𝜑 = { (𝐻, Σ, 𝑡 ) | ∀ 𝜎 : Σ. ∃. Σ′ , 𝜎 ′ , 𝑣 ′ . 𝐻, 𝜎, 𝑡 ⇓ 𝑣 ′ , 𝜎 ′ ∧ Σ ⊑ Σ′ ∧ 𝜎 ′ : Σ′ ∧
                                      (𝐻, Σ′ , 𝑣 ′ ) ∈ 𝑉 [[𝑇 ]] ∧ 𝐿 (𝑣) ∗Σ′ ⊆ [[𝜑 ∩ 𝑝˜ ]] 𝐻Σ′∗ ∪q∈𝑝 dom(Σ) ∧ 𝜎→ [[𝜑 ]] 𝐻Σ ∗ 𝜎 ′ }

                   𝐺 [[Γ 𝜑 ]] = { (𝐻, Σ) | dom(𝐻 ) = dom(Γ) ∧ 𝜑 ⊆ dom(Γ) ∧ Inv𝑜 (Γ, Σ, 𝐻, 𝜑 ) ∧ Inv𝑆 (Σ, 𝐻, 𝜑 ) }
           Inv𝑜 (Γ, Σ, 𝐻, 𝜑 ) = ∀ 𝑥,𝑇 , 𝑝. Γ (𝑥 ) = 𝑇 𝑝 ⇒ WF(𝑝𝑥Γ ) ∧
                                           (𝑥 ∈ 𝜑 ⇒ (𝐻, Σ, 𝐻 (𝑥 ) ) ∈ 𝑉 [[𝑇 ]] ) ∧ (q ∉ 𝑝 ∧ 𝑝˜ ⊆ 𝜑 ⇒ 𝐿 (𝐻 (𝑥 ) ) ∗Σ ⊆ [[ 𝑝˜ ]] 𝐻Σ ∗ )
                                      ′
             Inv𝑆 (Σ, 𝐻, 𝜑 ) = ∀𝑝, 𝑝 . 𝑝˜ ⊆ 𝜑 ∧ 𝑝˜′ ⊆ 𝜑 ∧ 𝑝∗∩˜ 𝑝˜′ ∗ ⊆ 𝜑 ⇒ [[ 𝑝˜ ]] 𝐻Σ ∗ ∩ [[ 𝑝˜′ ]] 𝐻Σ ∗ ⊆ [[ 𝑝∗∩
                                                                                                               ˜ 𝑝˜′ ∗]] 𝐻Σ ∗ .

                                                 Γ 𝜑 |= 𝑡 : 𝑇 𝑝            ∀ (𝐻, Σ) ∈ 𝐺 [[Γ 𝜑 ]]. (𝐻, Σ, 𝑡 ) ∈ 𝐸 [[𝑇 𝑝 ]] 𝜑
                                                                     def
     Semantic Typing Judgment                                        =

     Semantic Typing
                                                                                                          Γ 𝜑 |= 𝑡 1 : (Ref 𝑇 𝑝 1 ) 𝑝
         Γ 𝜑 |= 𝑡 : 𝑇 𝑞        𝑞⊆𝜑                   Γ 𝜑 |= 𝑡 : (Ref 𝑇 𝑞 ) 𝑝         𝑞⊆𝜑               Γ 𝜑 |= 𝑡 2 :𝑇 1
                                                                                                                       𝑝˜     𝑝˜1 ⊆ 𝜑
                                         (t-ref)                                              (t-!)                                        (t-:=)
        Γ 𝜑 |= ref 𝑡 : (Ref 𝑇 𝑞 )
                                  q𝑞
                                                                  Γ 𝜑 |=!𝑡 : 𝑇
                                                                               𝑞                          Γ 𝜑 |= 𝑡 1 := 𝑡 2 : 𝐵𝑜𝑜𝑙 ∅


Fig. 8. The value interpretation of types, terms, typing context interpretation, semantic typing judgment and
refined semantic typing rules for 𝜆 q . Differences from 𝜆Bq are highlighted.

   Encapsulation. The encapsulated computation lemma for 𝜆Bq (Lemma 3.1) remains valid for 𝜆 q .
Its formalization is similar, and thus is omitted.
 Discussion 1: Modeling Key Features in Prior Work. Our logical relations for 𝜆 q models a
major subset of Wei et al. [2024]’s 𝜆 q system. We summarize the differences as follows:
   (1) Self-References: As mentioned previously, we use a self-reference marker s, instead of
formalizing self-references 𝜆𝑓 as a binder of a 𝜆 term as in Wei et al. [2024]’s work. However, this
simplified formalization retains their key feature, i.e., the lightweight form of qualifier polymorphism
which is achieved by rule t-appq in both works.
   (2) Deep Substitution: As mentioned previously, to simplify the formalization, our t-app rule
does not consider deep substitution as theirs does. This restriction is purely technical, and does not
appear to impact expressiveness in any significant way [Jia et al. 2024] as deep references can also
be modeled indirectly via chains of argument and self-references.
Modeling Reachability Types with Logical Relations                                                     17


   (3) Reference Rules: In addition, our references rules require that a reference’s qualifier be
bounded by observation 𝜑. This property is not explicitly specified in their system, but can be
inferred from their tying rules. Thus, our reference rules are semantically equivalent to theirs.
   Discussion 2: Termination. Our semantic is parameterized over a fuel value that bounds the
steps that the execution is allowed; if it runs out of fuel, timeout will be returned. In this setting, we
prove termination by providing enough fuel for the execution. In addition, proving termination in
the presence of higher-order mutable references requires some constraints: the qualifiers attached
to a store location prohibit storing any values that may reach the location itself, thus excluding
cycles. This is a limitation in prior work [Wei et al. 2024] we discovered, leading to programs like
Landin‘s knot [Landin 1964] not being typeable. In particular, the introduction and assignment
rules for mutable references in Wei et al. [2024]’s work prohibit creating cycles through the store.
Specifically, rules t-ref and t-assgn (in their work) ensure that referent qualifiers are treated as
invariant, so only values with equivalent qualifiers can be assigned. Consider a typical version of
Landin‘s knot [Landin 1964]:
 (𝜆 x. (x := (𝜆 z. !x z); !x))(ref (𝜆 y y))

In this example, the reference type for the argument cannot capture any reachable variable, but the
function body updates the reference with a value that captures variable x. Thus, the example is not
typable in their system.
   Discussion 3: Strong Type Soundness. Prior works [Bao et al. 2021; Wei et al. 2024] proved
syntactic type soundness using small-step semantics, where reachability properties are checked
for intermediate values through their preservation theorems. In contrast, our work extends the
big-step semantics ⇓ to a total evaluation function, making a distinction between timeout, errors,
and normal values, leading to strong soundness results [Amin and Rompf 2017]. In particular,
we define reachability properties as invariants in the value interpretation of types and terms in
the logical framework. The fundamental theorem is proven by induction on the type derivation
(Γ 𝜑 ⊢ 𝑡 : 𝑇 𝑞 ), where each case is the corresponding compatibility lemma (i.e., semantic typing
rule). Therefore, the reachability properties are also verified for each sub-expression.

3.7     Write Effect System Extension (𝜆𝜺q )
In the previously presented frameworks, any reachable location could be modified while evalu-
ating an expression. This section presents 𝜆𝜺q that adds observable write effect qualifiers to track
which locations are modified, as opposed to just read or, e.g., passed as argument without being
dereferenced. This gives us a stronger store value preservation property than previous frameworks.
   Effect Types. The syntax of effect qualifiers are shown in Fig. 9 (bottom). Effect qualifiers (𝜺) are
finite sets of variables, and may include the self-reference marker s, denoting the locations (in the
pre-state) that may be modified during computation. Function types carry effect qualifiers 𝜺 for
their latent effects.
   Logical Interpretation of Effects. Fig. 9 shows the interpretation of function types and terms
that includes effects, which are highlighted in the figure. Consider the following example:
... // c1: Tc1 , c2: Tc2
def f (x: Tq ) = { c1 := !x + 1 }     // : ((x:Tq ) =>c1 ()){c1}
f(c2)                                 // : () c1

The function f has its latent effect on the variable c1, meaning that its body can only modify the
locations reachable from c1, as shown in the highlighted formula in Fig. 9. When the function
is invoked, i.e., f(c2), the effect is just c1 as well, according to rule e-app-q. In contrast, without
the effect extension, 𝜆 q approximates the write effect to what the argument and function reaches.
18                                                                Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf



     Unary Logical Relations                                                                                                                        𝜆𝜺q
                     𝜺
     𝑉 [[ (𝑥 : 𝑇 𝑠 ) → 𝑈 𝑟 ]] = { (𝐻, Σ, ⟨𝐻 ′ , (𝜆𝑥 .𝑡 ) 𝑞 ⟩ ) | WF(Σ, ⟨𝐻 ′ , (𝜆𝑥 .𝑡 ) 𝑞 ⟩ ) ∧ (∀ 𝑣, 𝜎 ′ , Σ′ . Σ ≡ [[𝑞 ]] 𝐻 ′∗ Σ′   Σ       ∧ 𝜎 : Σ′ ∧
                                                                                                                                                ′

                                               (𝐻, Σ′ , 𝑣) ∈ 𝑉 [[𝑇 ]] ∧ 𝐿 (𝑣) ∗Σ′ ⊆ [[𝑠˜ ]] 𝐻Σ′∗ ∪s∈𝑠 [[𝑞 ]] 𝐻Σ ∗ ∪q∈𝑠 [[𝑞 ]] 𝐻Σ ∗ ⇒
                                                                                                                      ′                  ′



                                                   ∃ 𝜎 ′′ , Σ′′ , 𝑣 ′ . 𝐻 ′ ; (𝑥, 𝑣), 𝜎 ′ , 𝑡 ⇓ 𝑣 ′ , 𝜎 ′′ ∧ Σ′ ⊑ Σ′′ ∧ 𝜎 ′′ : Σ′′ ∧
                                                          (𝐻, Σ′′ , 𝑣 ′ ) ∈ 𝑉 [[𝑈 ]] ∧
                                                         𝐿 (𝑣 ′ ) ∗Σ′′ ⊆ ( [[𝑟˜ \𝑥 ]] 𝐻Σ′′∗ ∩ [[𝑞 ]] 𝐻Σ′′∗ ) ∪𝑥 ∈𝑟 𝐿 (𝑣) ∗Σ′′ ∪s∈𝑟 [[𝑞 ]] 𝐻Σ′′∗
                                                                                             ′                ′                              ′



                                                                         ∪q∈𝑟 dom(Σ ) ∧        ′

                                                          𝜎 ′ → [[𝜺 \𝑥 ]] 𝐻Σ ∗ ∪𝑥 ∈𝜺 𝑣Σ∗ ′ ∪s∈𝜺 [[𝑞 ]] 𝐻Σ ∗ 𝜎 ′′ ) }
                                                                           ′                   ′
                                                                                                ′




                𝐸 [[𝑇 𝑝 𝜺 ]] 𝜑 = { (𝐻, Σ, 𝑡 ) | ∀ 𝜎 : Σ. ∃ Σ′ , 𝜎 ′ , 𝑣 ′ . 𝑡, 𝐻, 𝜎 ⇓ 𝑣 ′ , 𝜎 ′ ∧ Σ ⊑ Σ′ ∧ 𝜎 ′ : Σ′ ∧
                                      (𝐻, Σ′ , 𝑣 ′ ) ∈ 𝑉 [[𝑇 ]] ∧ 𝐿 (𝑣) ∗Σ′ ⊆ [[𝜑 ∩ 𝑝˜ ]] 𝐻Σ′∗ ∪q∈𝑝 dom(Σ) ∧ 𝜎→ [[𝜑 ∩ 𝜺 ]] 𝐻Σ ∗ 𝜎 ′ }


     Syntax      𝜺 ∈ Pfin (Var⊎ {s} )                       Flow-Insensitive Sequential Effects Composition                              𝜺1 ▷ 𝜺2 := 𝜺1 ∪𝜺2

Fig. 9. Effect interpretation and selected typing rules for 𝜆𝜺q . Differences from 𝜆 q are highlighted. Effect
qualifiers (𝜺) are finite set of variables, and may include the self-reference marker s. The effect composition
(e.g., 𝜺1 ▷ 𝜺2 ) is defined as set union (i.e., 𝜺1 ∪ 𝜺2 ).

     Semantic Typing                                                                                                                     Γ 𝜑 |= 𝑡 : 𝑇 𝑝 𝜺

                                                        Γ (𝑥 ) = 𝑥 : 𝑇 𝑝             𝑥 ∈𝜑                      Γ 𝜑 |= 𝑡 : 𝑇 𝑞 𝜺          𝑞⊆𝜑
                                       (e-cst)                                              (e-var)                                                   (e-ref)
          Γ 𝜑 |= 𝑐 : 𝐵𝑜𝑜𝑙 ∅ ∅                                 Γ 𝜑 |= 𝑥 : 𝑇 𝑥 ∅                                Γ 𝜑 |= ref 𝑡 : (Ref 𝑇 𝑞 ) q𝑞 𝜺
                                                   ′                  ′
              (Γ, 𝑥 : 𝑇 𝜑∩(𝑠 [𝑞/s])∪q∈𝑠 q ) 𝑞 ,𝑥 |= 𝑡 : 𝑈 𝑟 [𝑞 /s] 𝜺 [𝑞 ′ /s]                                    Γ 𝜑 |= 𝑡 : (Ref 𝑇 𝑞 ) 𝑝 𝜺
                               𝑞′ = 𝜑 ∩ 𝑞         𝑠˜ ⊆ 𝑞 ′                                                                𝑞⊆𝜑
                                                                                                (e-abs)                                                  (e-!)
                                           ′                  𝜺
                       Γ 𝜑 ⊢ (𝜆𝑥 .𝑡 ) 𝑞 : ( (𝑥 : 𝑇 𝑠 ) → 𝑈 𝑟 ) 𝑞 ∅                                                    Γ 𝜑 |=!𝑡 : 𝑇 𝑞 𝜺

                                         𝜺3
                                                𝑝                                                                Γ 𝜑 1 |= 𝑡 1 : 𝐵𝑜𝑜𝑙 𝑞 𝜺1
                  Γ 𝜑 |= 𝑡 1 : (𝑥 : 𝑇 𝑠 ) → 𝑈 𝑟    𝜺1                     q ∉ 𝑠, 𝑜                                Γ 𝜑 2 |= 𝑡 2 : 𝐵𝑜𝑜𝑙 𝑝 𝜺2
         Γ 𝜑 |= 𝑡 2 : 𝑇 𝑜 𝜺2       𝑜˜ ⊆ 𝑠˜ ⊆ 𝜑  𝑟˜ ⊆ 𝜑, 𝑥     𝑥 ∉ fv(𝑈 )                                          𝜑1 ⊆ 𝜑          𝜑2 ⊆ 𝜑
              𝜺3 ⊆ 𝜑, 𝑥          𝜃 = [𝑜/𝑥, 𝑝/s]    𝜃 ′ = [𝑜/𝑥,                                                                                        (e-seq)
                                                               ˜
                                                          ˜ 𝑝/s]
                                                                                                (e-app)      Γ 𝜑 |= 𝑡 1 ; 𝑡 2 : 𝐵𝑜𝑜𝑙 ∅ 𝜺1 ▷ 𝜺2
                         Γ 𝜑 |= 𝑡   1 𝑡2   : 𝑈 𝑟𝜃 (𝜺   1 ▷ 𝜺2 ▷ 𝜺3 )𝜃
                                                                      ′
                                                                                                                     Γ 𝜑 |= 𝑡 : 𝑇 𝑝 1 𝜺1
                                  𝜺3                                                                              𝑝˜1 ⊆ 𝑝˜2 ⊆ dom(Γ)
                                       𝑝
             Γ 𝜑 |= 𝑡 1 : 𝑥 : 𝑇 𝑠 → 𝑈 𝑟    𝜺1                  𝜃 = [𝑜/𝑥, 𝑝/s]
                                                                                                                   𝜺˜1 ⊆ 𝜺˜2 ⊆ dom(Γ)
      Γ 𝜑 |= 𝑡 2 : 𝑇 𝑜 𝜺2     s ∉ 𝑠 ⇒ 𝑝∗ ∩ 𝑜∗
                                            ˜ ⊆ 𝑠˜                    q∈𝑠        𝑠˜ ⊆ 𝜑                          𝑝 3 = 𝑝 2 ∪q∈𝑝 1 ∨q∈𝑝 2 q
         𝑥 ∉ fv(𝑈 )       𝜺˜3 ⊆ 𝜑, 𝑥   𝑟˜ ⊆ 𝜑, 𝑥                   𝜃 ′ = [𝑜/𝑥, ˜
                                                                          ˜ 𝑝/s]                                                                      (e-sub)
                                                                                            (e-app-q)                Γ 𝜑 |= 𝑡 : 𝑇 𝑝 3 𝜺2
                        Γ 𝜑 |= 𝑡 1 𝑡 2 : 𝑈 𝑟𝜃 (𝜺1 ▷ 𝜺2 ▷ 𝜺3 )𝜃 ′
                                                                                                             Γ 𝜑 |= 𝑡 : 𝑈 𝑝 𝜺       𝑥 ∈ 𝑝˜
          Γ 𝜑 |= 𝑡 1 : (Ref 𝑇 𝑝 1 ) 𝑝 𝜺1            Γ 𝜑 |= 𝑡 2 : 𝑇 𝑝˜1 𝜺2        𝑝˜1 ⊆ 𝜑                       Γ (𝑥 ) = 𝑇 𝑞        𝑞⊆𝜑
                                                                                                    (e-:=)                                        (e-sub-var)
                         Γ 𝜑 |= 𝑡 1 := 𝑡 2 : 𝐵𝑜𝑜𝑙 ∅ 𝜺1 ▷ 𝜺2 ▷ 𝑝˜                                                Γ 𝜑 |= 𝑡 : 𝑈 𝑝 [𝑞/𝑥 ] 𝜺
     Effects Shorthands                𝜺1 ▷ 𝜺2 := 𝜺1 ∪ 𝜺2

                                                       Fig. 10. Semantic typing rules for 𝜆𝜺q .

As a result, f(c2) would induce effect on both c1 and c2, leading to a weaker value preservation
property, as illustrated by formula 4 and term interpretation in Fig. 5.
   Other definitions follow 𝜆 q , and are omitted in Fig. 9.
   Semantic Typing Judgment and Rules. The definition of the semantic typing judgment is
defined as: Γ 𝜑 |= 𝑡 : 𝑇 𝑝 𝜺 = ∀ (𝐻, Σ) ∈ 𝐺 [[Γ 𝜑 ]]. (𝐻, Σ, 𝑡) ∈ 𝐸 [[𝑇 𝑝 𝜺]] 𝜑 . It means that term 𝑡 inhabits the
                             def

term interpretation of type 𝑇 𝑝 𝜺 under any value environment 𝐻 and store typing Σ that satisfies
the semantic interpretation of the typing context 𝐺 [[Γ 𝜑 ]], which follows 𝜆 q .
Modeling Reachability Types with Logical Relations                                                                         19


    Fig. 10 shows the semantic typing rules for 𝜆𝜺q , extending those of 𝜆 q with observable write
effect qualifiers (𝜺), denoting the set of locations (in the pre-state) that may be modified during the
execution. The effect rules are straightforward: the final effect of a compound term combines the
effects of sub-terms with the intrinsic effect of this term. For example, the effects of assignments
(rule E:=) consist of two parts: (1) the effects 𝜺1 and 𝜺2 , which are those of sub-terms, and (2)
the effect 𝑝,˜ which denotes the reachable locations from variables in 𝑝˜ being modified. The final
effects are sequential composition of those effects. In a flow-insensitive effect system like 𝜆𝜺q , the
composition is defined as set union . 9
    Fundamental Theorem and Adequacy. The syntactic typing judgments have the form Γ 𝜑 ⊢ 𝑡 :
𝑇 𝑝 𝜺, and the typing rules have the same shape as the semantic ones, but turning the symbol |= into
the symbol ⊢ . We have proved the compatibility lemmas, fundamental theorem and adequacy for
𝜆𝜺q . The fundamental theorem follows immediately from the compatibility lemmas, and adequacy,
semantic type safety, and termination follow from the fundamental theorem and the definition of
semantic term interpretation.
    Encapsulation. The encapsulated computation lemma for 𝜆𝜺q demand that an encapsulated
computation does not induce observable effects.
  Lemma 3.6 (Encapsulated Computation (𝜆𝜺q )). If Γ ∅ ⊢ 𝑡 : 𝑇 ∅ ∅, then ∀ (𝐻, Σ) ∈ 𝐺 [[Γ ∅ ]].
∀ Σ′ . Σ ≡ ∅ Σ′ ⇒ (𝐻, Σ′, 𝑡) ∈ 𝐸 [[𝑇 ∅ ∅]] ∅ .

4     Contextual Equivalence via Binary Logical Relations
We now switch from modeling soundness, termination, and other properties of a single expression
to properties concerning pairs of expressions, specifically notions of observational equivalence. Thus,
we extend our unary logical relations for 𝜆 q and 𝜆𝜺q to binary logical relations, with the intention
that semantically equivalent values and terms are exactly the ones that will be logically related. We
formalize their judgments into one, as 𝜆𝜺q only adds conditions regarding effects. For example, the
typing judgment is written as Γ 𝜑 |= 𝑇 𝑝 𝜺 , where formula 𝜺 applies only to 𝜆𝜺q .

4.1    Contextual Equivalence
Two programs are contextually equivalent if a well-typed program context cannot distinguish
between them, i.e., they have the same observable behavior. Here, we define contextual equivalence
to verify equational rules (Section 5). A program 𝑡 1 is said to be contextually equivalent to another
program 𝑡 2 , written as Γ 𝜑 |= 𝑡 1 ≈ctx 𝑡 2 : 𝑇 𝑝 𝜺 , if for any program context 𝐶 with a hole of type
𝑇 𝑝 𝜺 , if 𝐶 [𝑡 1 ] has some (observable) behavior, then so does 𝐶 [𝑡 2 ]. The definition of context 𝐶
is shown soon. Following the approach of Timany et al. [2024] and related prior work [Ahmed
et al. 2009], we define a judgement for logical equivalence using binary logical relations, written as
Γ 𝜑 |= 𝑡 1 ≈log 𝑡 2 : 𝑇 𝑝 𝜺 .
   Unlike reduction contexts, contexts 𝐶 for reasoning about equivalence allow a “hole” to appear
                                                     ′       ′
in any place. We write 𝐶 : (Γ 𝜑 ;𝑇 𝑝 𝜺 ) ⇛ (Γ ′ 𝜑 ;𝑇 ′ 𝑝 𝜺 ′ ) to mean that the context 𝐶 is a program
              ′                      ′
of type 𝑇 ′ 𝑝 𝜺 ′ (closed under Γ ′ 𝜑 ) with a hole that can be filled with any program of type 𝑇 𝑝 𝜺
(closed under Γ ). The typing rules for well-typed contexts imply that if Γ 𝜑 ⊢ 𝑡 : 𝑇 𝑝 𝜺 and
                     𝜑
                              ′  ′                         ′            ′
𝐶 : (Γ 𝜑 ;𝑇 𝑝 𝜺 ) ⇛ (Γ ′ 𝜑 ;𝑇 ′ 𝑝 𝜺 ′ ) hold, then Γ ′ 𝜑 ⊢ 𝐶 [𝑡] : 𝑇 ′ 𝑝 𝜺 ′ . Fig. 11 shows the selected
typing rules for well-typed contexts.
   Two well-typed terms, 𝑡 1 and 𝑡 2 , under typing context Γ 𝜑 , are contextually equivalent if any
occurrences of the first term in a closed term can be replaced by the second term without affecting
the observable results of reducing the program, which is formally defined as follows:
9 One could also incorporate a flow-sensitive effect system, as suggested by Bao et al. [2021], to model more complex effects.
20                                                      Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf



     Context for Contextual Equivalence                                                                                            𝜆 q /𝜆𝜺q
                  𝐶 ::= □ | 𝐶 𝑡 | 𝑡 𝐶 | (𝜆𝑥 .𝐶 ) 𝑞 | ref 𝐶 | ! 𝐶 | 𝐶 := 𝑡 | 𝑡 := 𝐶 | 𝑡 ; 𝐶 | 𝐶; 𝑡
                                                                                                                            ′      ′
     Context Typing Rules                                                                    𝐶 : (Γ 𝜑 ;𝑇 𝑞 𝜺 ) ⇛ (Γ ′ 𝜑 ;𝑇 ′ 𝑞         𝜺′ )
                                                                                       ′                       ′        ′
                                                𝐶 : (Γ 𝜑 ; 𝑆 𝑝 𝜺 ) ⇛ ( (Γ ′ , 𝑥 : 𝑇 𝜑 ∩(𝑠 [𝑞/s])∪q∈𝑠 q ) 𝑞 ,𝑥 ; 𝑈 𝑟 [𝑞 /s] 𝜺 ′ )
                                                                          𝑞 ′ = 𝜑 ′ ∩ 𝑞 𝑠˜ ⊆ 𝑞 ′
                                                                                                                                       (c-𝜆)
      □ : (Γ 𝜑 ;𝑇 𝑞 𝜺 ) ⇛ (Γ 𝜑 ;𝑇 𝑞 𝜺 )                                                                          𝜺′
                                    (c-□)              (𝜆𝑥 .𝐶 ) 𝑞 : (Γ 𝜑 ; 𝑆 𝑝 𝜺 ) ⇛ (Γ    ′ 𝜑′   ; ( (𝑥 : 𝑇 𝑠 ) → 𝑈 𝑟 ) 𝑞 ∅)

                                         ′            ′
                                                         𝜺3       ′ ′            ′          ′
          𝐶 : (Γ 𝜑 ; 𝑆 𝑝 𝜺1 ) ⇛ (Γ ′ 𝜑 ; ( (𝑥 : 𝑇 ′ 𝑠 ) → 𝑈 ′ 𝑟 ) 𝑝 𝜺4 ) Γ ′ 𝜑 ⊢ 𝑡 2 : 𝑇 ′ 𝑜 𝜺2 q ∈ 𝑠 ′ 𝑠˜′ ⊆ 𝜑 ′
                      s ∉ 𝑠 ′ ⇒ 𝑞˜′ ∗ ∩ 𝑜˜′ ∗ ⊆ 𝑠˜′ 𝑟˜′ ⊆ 𝜑 ′ , 𝑥 𝜺3 ⊆ 𝜑 ′ , 𝑥 𝑥 ∉ fv(𝑈 ′ ) 𝜃 = [𝑜 ′ /𝑥, 𝑝˜′ /s]
                                                                      ′       ′
                                       𝐶 𝑡 2 : (Γ 𝜑 ; 𝑆 𝑝 𝜺1 ) ⇛ (Γ ′ 𝜑 ; 𝑈 ′ 𝑟 𝜃 (𝜺4 ▷ 𝜺2 ▷ 𝜺3 )𝜃 )
                                                                                                                                (c-app-q-1)

               ′                    ′
                                       𝜺4     ′   ′                                    ′
          Γ ′ 𝜑 ⊢ 𝑡 1 : ( (𝑥 : 𝑇 ′ 𝑠 ) → 𝑈 ′ 𝑟 ) 𝑝 𝜺2       𝐶 : (Γ 𝜑 ; 𝑆 𝑝 𝜺1 ) ⇛ (Γ ′ 𝜑 ;𝑇 ′ 𝑜 𝜺3 )        q ∈ 𝑠′   𝑠˜′ ⊆ 𝜑
              s ∉ 𝑠 ′ ⇒ 𝑞˜′ ∗ ∩ 𝑜∗
                                 ˜ ⊆ 𝑠˜′    𝑟˜′ ⊆ 𝜑 ′ , 𝑥      𝜺3 ⊆ 𝜑 ′ , 𝑥       𝑥 ∉ fv(𝑈 ′ )          𝜃 = [𝑜/𝑥, 𝑝˜′ /s]
                                                                  ′       ′
                                                                                                                                (c-app-q-2)
                                  𝑡 1 𝐶 : (Γ 𝜑 ; 𝑆 𝑝 𝜺1 ) ⇛ (Γ ′ 𝜑 ; 𝑈 ′ 𝑟 𝜃 (𝜺2 ▷ 𝜺3 ▷ 𝜺4 )𝜃 )


                            Fig. 11. Selected context typing rules for the 𝜆 q - and 𝜆𝜺q calculus.

     Relational Worlds, Well-Defined Relations and Store Typing                                                                   𝜆 q /𝜆𝜺q
                        Σ := ∅ | Σ, ℓ : L
                    𝜎 : Σ = dom(𝜎 ) = dom(Σ) ∧ (∀ℓ ∈ dom(Σ).𝐿 (𝜎 (ℓ ) ) ∗Σ ⊆ Σ(ℓ ) ∗Σ ∧ (∀ℓ ′ ∈ Σ(ℓ ). ℓ ′ < ℓ ) )
                            def


                            def
          WR(W, L, L′ ) = (L, L′ ) ⊆ dom(W) ∧ (∀ℓ1 , ℓ2 , (ℓ1 , ℓ2 ) ∈ 𝑓 ⇒ (ℓ1 ∈ L ⇐⇒ ℓ2 ∈ L′ ) )
          W ≡ (L,L′ ) 𝑊   ′ def
                            = WR(W, L, L′ ) ∧ WR(W′ , L, L′ ) ∧ W1 ≡ L W1′ ∧ W2 ≡ L′ W2′ ∧
                              (∀ ℓ1 ∈ L, ℓ2 ∈ L′ . W(ℓ1 , ℓ2 ) ⇒ WV (ℓ1 , ℓ2 ) = WV ′ (ℓ , ℓ ) ) ∧
                                                                                        1 2
                                               ′                                  ′
                              (∀ ℓ1 ∈ L, ℓ2 ∈ L . (ℓ1 , ℓ2 ) ∈ W ↔ (ℓ1 , ℓ2 ) ∈ W )
                            def
            (𝜎1 , 𝜎2 ) : W = 𝜎1 : W1 ∧ 𝜎2 : W2 ∧ (∀ℓ1 , ℓ2 , W(ℓ1 , ℓ2 ) ⇒ (𝜎 (ℓ1 ), 𝜎 (ℓ2 ) ) ∈ WV (ℓ1 , ℓ2 ) ∧
                             WR(W, 𝜎1 (ℓ1 ) ∗W1 , 𝜎2 (ℓ2 ) ∗W2 ) )

Fig. 12. Definitions of relational worlds, well-defined relations and store typing for binary logical relations.


    Definition 4.1 (Contextual Equivalence). Term 𝑡 1 is contextually equivalent to 𝑡 2 , written Γ 𝜑 |=
𝑡 1 ≈ctx 𝑡 2 : 𝑇 𝑝 𝜺 , if Γ 𝜑 ⊢ 𝑡 1 : 𝑇 𝑝 𝜺 , and Γ 𝜑 ⊢ 𝑡 2 : 𝑇 𝑝 𝜺 , and ∀𝐶 : (Γ 𝜑 ;𝑇 𝑝 𝜺 ) ⇛
(∅; Unit ∅ ∅ ). 𝐶 [𝑡 1 ] ↓ ⇐⇒ 𝐶 [𝑡 2 ] ↓.

We write 𝑡 ↓ to mean term 𝑡 terminates, if 𝑡, ∅, ∅ ⇓ 𝑣, 𝜎, for some value 𝑣 and final store 𝜎.
  The above definition is standard [Ahmed et al. 2009] and defines a partial program equivalence.
However, since we focus on a total fragment of the systems here, program termination can not be
used as an observer for program equivalence. We thus rely on a refined definition of contextual
equivalence using Boolean contexts.

     ∀𝐶 : (Γ 𝜑 ;𝑇 𝑝 𝜺 ) ⇛ (∅; 𝐵𝑜𝑜𝑙 ∅ ∅ ). ∃ 𝜎, 𝜎 ′, 𝑣. 𝐶 [𝑡 1 ], ∅, ∅ ⇓ 𝑣, 𝜎 ∧ 𝐶 [𝑡 2 ], ∅, ∅ ⇓ 𝑣, 𝜎 ′ .

That is to say, we consider two terms contextually equivalent if they yield the same answer value
in all Boolean contexts.
Modeling Reachability Types with Logical Relations                                                      21


4.2    The World Model
Following other prior works [Ahmed 2004; Benton et al. 2007; Thamsborg and Birkedal 2011], we
apply Kripke logical relations to our systems. Our logical relations are indexed by types and store
layouts via worlds, generalized store typings relating two stores. This allows us to interpret Ref 𝑇 𝑞
as an allocated location that holds values of type 𝑇 𝑞 . The invariant that all allocated locations hold
well-typed values w.r.t. the world must hold in the pre-state and be re-established in the post-state
of a computation. The world may grow as more locations may be allocated. It is important that this
invariant must hold in future worlds, which is commonly referred to as monotonicity.
   World, Relational Worlds & World Extension. As discussed in Section 3.6, our store layout
is specified by the logical interpretation of reachability qualifiers in a store typing, and is free of
cycles. The notion of world for our systems is defined as:
  Definition 4.2 (World). A world W is a tuple (Σ1, Σ2, 𝑓 , V̂), where
      • Σ1 and Σ2 are store typings defined in Fig. 12,
      • 𝑓 ⊆ (dom(Σ1 ) × dom(Σ2 )) is a partial bijection.
      • V̂ ⊆ (dom(Σ1 ) × dom(Σ2 ) × V × V).
  A world is meant to define relational stores. The partial bijection captures the fact that a relation
holds under permutation of store locations. The notation V̂ maps from pairs of locations to semantic
types. A semantic type is a set of values (V).
  If W = (Σ1, Σ2, 𝑓 , V̂) is a world, we refer to its components as follows:
                              (
                          (ℓ1, ℓ2 ) ∈ 𝑓 ℓ1 ∈ dom(Σ1 ) and ℓ2 ∈ dom(Σ2 ) and when defined
               W(ℓ1, ℓ2 ) =
                          ⊥             otherwise
      dom1 (W) = dom(Σ1 )         dom2 (W) = dom(Σ2 )         dom(W) = (dom(Σ1 ), dom(Σ2 ))
            W1 = Σ1                     W2 = Σ2                   WV = V̂
   If W and W′ are worlds, such that dom1 (W) ∩ dom1 (W′ ) = dom2 (W) ∩ dom2 (W′ ) = ∅, then W
and W′ are called disjoint, and we write W; W′ to mean extending W with a disjoint world W′ . Let
𝜎1 and 𝜎2 be two stores. We write (𝜎1, 𝜎2 ) : W to mean the stores are well-defined w.r.t. the world
W, which is formally defined in Fig. 12.
   Similar to the unary versions, we define relational worlds, written as W ≡ (L,L′ ) W′ to mean that
types and relations are preserved over two related worlds at a pair of locations (L, L′ ). Note that
the pair of locations can not be arbitrary. Consider related locations at world W, e.g., (ℓ1, ℓ2 ) ∈ 𝑓 . If
ℓ1 ∈ L, but ℓ2 ∉ L′ , then the relation is broken, resulting in ill-defined relational worlds. Thus, we use
the predicate WR (defined in Fig. 12) to make sure the relation is defined in both directions. In other
words, ℓ1 must be related to some location, and it cannot be related to more than one location. Fig. 12
summarizes the definitions of these notations. We write W ⊑ W′ to mean W ≡ (dom1 (W),dom2 (W) ) W′ .
The definition of world extension satisfies reflexivity and transitivity.

4.3    Binary Logical Relations for 𝜆 q and 𝜆𝜺q
This section presents the definition of binary logical relations for our systems, as shown in Fig. 13.
In the figure, we use the subscript 𝑖 in formulas to refer to both programs when the context is
clear, where 𝑖 = 1 or 2. For example, in the value interpretation of reference types, we write
W(ℓ𝑖 ) = [[𝑞𝑖 ]] 𝐻ˆ𝑖 to mean W(ℓ1 ) = [[𝑞 1 ]] 𝐻ˆ 1 ∧ W(ℓ2 ) = [[𝑞 2 ]] 𝐻ˆ 2 .
   In the figure, the highlighted formulas in teal are assertions on well-formed relations, and related
values. Formulas in pink and in gray are exclusively for 𝜆 q and 𝜆𝜺q respectively. As in their unary
counterparts, 𝜆 q interprets observations as an approximation of write effects, and 𝜆𝜺q establishes a
stronger value preservation property with explicit write effect annotations.
22                                                                Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf


  Binary Value Interpretation of Types and Terms                                                                                       𝜆 q /𝜆𝜺q
       V [[𝐵𝑜𝑜𝑙, 𝐵𝑜𝑜𝑙 ]] = { (𝐻, W, 𝑐, 𝑐 ) }
                                  ˆ
           𝑞          𝑞
 V [[Ref 𝑇1 1 , Ref 𝑇2 2 ]] = { ( 𝐻,
                                  ˆ W, ℓ1 , ℓ2 ) | W(ℓ1 , ℓ2 ) ∧ 1 WR(W, {ℓ1 }, {ℓ2 } ) ∧ (W(ℓ𝑖 ) = [[𝑞𝑖 ]] ˆ ∧
                                                                                                                          𝐻𝑖
                                  W𝑖 (ℓ𝑖 ) ∗W𝑖 ⊆ ℓ𝑖 ∗W ∧ (∀ 𝜎1′ , 𝜎2′ , W′ , 𝑣1 , 𝑣2 . (𝜎1′ , 𝜎2′ ) : W′ ∧ W ≡ (W1 (ℓ1 ) ∗ ,W2 (ℓ2 ) ∗ ) W′ ∧
                                                              𝑖                                                                          W1                W2
                                     𝐿 (𝑣𝑖 ) ∗W′ ⊆ W𝑖 (ℓ𝑖 ) ∗W′ ∧ 2 WR(W′ , 𝐿 (𝜎1′ (ℓ1 ) ) ∗W′ , 𝐿 (𝜎2′ (ℓ2 ) ) ∗W′ ) ⇒
                                               𝑖              𝑖                               1                   2
                                                                              ˆ W′ , 𝑣1 , 𝑣2 ) ∈ V [[𝑇1 ,𝑇2 ]] ) ) ) }
                                            ( (𝑣1 , 𝑣2 ) ∈ WV (ℓ1 , ℓ2 ) ⇐⇒ ( 𝐻,

                  𝜺1
             𝑠          𝑟
 V [[ (𝑥 : 𝑇1 1 ) → 𝑈 1 1 ,          ˆ W, ⟨𝐻 1 , (𝜆𝑥 .𝑡 1 ) 𝑞1 ⟩, ⟨𝐻 2 , (𝜆𝑥 .𝑡 2 ) 𝑞2 ⟩ ) | 3 WR(W, [[𝑞 1 ]] 𝐻W1 ∗ , [[𝑞 2 ]] 𝐻W2 ∗ ) ∧
                               = { ( 𝐻,                                                                         1                2
                  𝜺2
                                   (∀𝑣1 , 𝑣2 , W′ , 𝜎1′ , 𝜎2′ . (𝜎1′ , 𝜎2′ ) : W′ ∧ W ≡ ( [[𝑞 ]] W1 ∗ ,[[𝑞 ]] W2 ∗ ) 𝑊 ′ ∧
             𝑠           𝑟
      (𝑥 : 𝑇2 2 ) → 𝑈 2 2 ]]
                                                                                                      1 𝐻′        2 𝐻′
                                                                                                         1           2

                                      4 WR(W′ , dom1 (W′ ), dom2 (W′ ) ) ∧ ( 𝐻,
                                                                             ˆ W′ , 𝑣1 , 𝑣2 ) ∈ V [[𝑇1 ,𝑇2 ]] ∧
                                                                  W′ ∗
                                     𝐿 (𝑣𝑖 ) ∗W′ ⊆ [[𝑠˜𝑖 ]] 𝐻ˆ 𝑖 ∪s∈𝑠𝑖 [[𝑞𝑖 ]] 𝐻W𝑖𝑖′∗ ∪q∈𝑠𝑖 [[𝑞𝑖 ]] 𝐻W𝑖𝑖′∗ ⇒
                                               𝑖                   𝑖

                                            (∃ W′′ , 𝜎1′′ , 𝜎2′′ , 𝑣1′ , 𝑣2′ . 𝑡 1 , 𝐻 1 ; (𝑥, 𝑣1 ), 𝜎1′ ⇓ 𝑣1′ , 𝜎1′′ ∧ 𝑡 2 , 𝐻 2 ; (𝑥, 𝑣2 ), 𝜎2′ ⇓ 𝑣2′ , 𝜎2′′ ∧
                                                    W′ ⊑ W′′ ∧ WR(W′′ , dom1 (W′′ ), dom2 (W′′ ) ) ∧ (𝜎1′′ , 𝜎2′′ ) : W′′ ∧
                                                       ˆ W′′ , 𝑣 ′ , 𝑣 ′ ) ∈ V [[𝑈 1 , 𝑈 2 ]] ∧
                                                     ( 𝐻,              1 2
                                                    𝐿 (𝑣𝑖′ ) ∗W′′ ⊆ ( [[𝑟˜𝑖 \𝑥 ]] 𝐻W𝑖𝑖′′∗ ∩ [[𝑞𝑖 ]] 𝐻W𝑖𝑖′′∗ ) ∪𝑥 ∈𝑟𝑖 𝐿 (𝑣𝑖′ ) ∗W′′ ∪s∈𝑟𝑖 [[𝑞𝑖 ]] 𝐻W𝑖𝑖′′∗
                                                                                           ˆ

                                                                       𝑖                                                           𝑖
                                                                         ∪q∈𝑟𝑖 dom(W𝑖′ ) ∧
                                                         𝜎𝑖 → [[𝑞𝑖 ]] 𝐻 ∪ 𝐿 (𝑣𝑖 ) ∗W𝑖′ 𝜎𝑖′′
                                                          ′                                 𝜎𝑖′ → [[𝜺 𝒊 \𝑥 ]] 𝐻W ∗ ∪𝑥 ∈𝜺 𝒊 𝑣𝑖 ∗W′ ∪s∈𝜺 𝒊 [[𝑞𝑖 ]] 𝐻W ∗ 𝜎𝑖′′ ) ) }
                                                                      W∗   ′                                          ′                           ′
                                                                           𝑖                                          𝑖                           𝑖
                                                                                                                                                   ′
                                                                           𝑖                                          𝑖                            𝑖
                                                                                                                                   𝑖



                                 ˆ W, 𝑡 1 , 𝑡 2 ) | ∀ 𝜎1 , 𝜎2 .(𝜎1 , 𝜎2 ) : W ∧ ∃ W′ , 𝜎 ′ , 𝜎 ′ , 𝑣1 , 𝑣2 . 𝑡 1 , 𝐻ˆ 1 , 𝜎1 ⇓ 𝑣1 , 𝜎 ′ ∧
            E [[𝑇 𝑝 𝜺 ]] 𝜑 = { (𝐻,                                                      1 2                                          1
                                𝑡 2 , 𝐻ˆ 2 , 𝜎2 ⇓ 𝑣2 , 𝜎2′ ∧ W ⊑ W′ ∧ WR(W′ , dom1 (W′ ), dom2 (W′ ) ) ∧ (𝜎1′ , 𝜎2′ ) : W′ ∧
                                (𝐻, ˆ W′ , 𝑣1 , 𝑣2 ) ∈ V [[𝑇 ,𝑇 ]] ∧ 𝐿 (𝑣𝑖 ) ∗ ′ ⊆ [[𝜑 ∩ 𝑝 ]] W𝑖 ∗ ∪q∈𝑝 dom(W𝑖 ) ∧
                                                                               W                𝑖   𝐻ˆ                    𝑖

                                      (𝜎1 → [[𝜑 ]] 𝐻Wˆ ∗ 𝜎1′ ∧ 𝜎2 → [[𝜑 ]] 𝐻Wˆ ∗ 𝜎2′ )
                                                     1
                                                     1
                                                                                2
                                                                                2
                                                                                                    (𝜎1 → [[𝜑 ∩ 𝜺 ]] 𝐻Wˆ ∗ 𝜎1′ ∧ 𝜎2 → [[𝜑 ∩ 𝜺 ]] 𝐻Wˆ ∗ 𝜎2′ ) }
                                                                                                                          1
                                                                                                                              1                        2
                                                                                                                                                       2




                 𝐺 [[Γ 𝜑 ]] = { ( 𝐻,
                                  ˆ W) | dom𝑖 ( 𝐻ˆ ) = dom(Γ) ∧ 𝜑 ⊆ dom(Γ) ∧ Inv𝑜 (Γ, 𝜎, 𝐻,          ˆ 𝜑 ) ∧ Inv𝑆 (W, 𝐻,    ˆ 𝜑)}
                     ˆ 𝜑 ) = ∀ 𝑥,𝑇 , 𝑝. Γ (𝑥 ) = 𝑇 𝑝 ⇒ WF(𝑝𝑥Γ ) ∧ (𝑥 ∈ 𝜑 ⇒ (𝐻,
        Inv𝑜 (Γ, W, 𝐻,                                                          ˆ W, 𝐻ˆ 1 (𝑥 ), 𝐻ˆ 2 (𝑥 ) ) ∈ V [[𝑇 ,𝑇 ]] ) ∧
                                                                       ∗
                              (q ∉ 𝑝 ∧ 𝑝˜ ⊆ 𝜑 ∧ 𝑥 ∈ 𝜑 ⇒ 𝐿 (𝐻ˆ 𝑖 (𝑥 ) ) W𝑖 ⊆ [[ 𝑝˜ ]] 𝐻W𝑖𝑖∗ )
                                                                                      ˆ


                                                          ˜ 𝑝˜ ∗ ⊆ 𝜑 ⇒ [[ 𝑝˜ ]] W𝑖 ∩ [[ 𝑝˜′ ]] 𝐻W𝑖𝑖∗ ⊆ [[ 𝑝∗∩
                                                                                  ˆ𝑖 ∗
                                     ′                                                                    ˜ 𝑝˜′ ∗]] 𝐻W𝑖𝑖∗ .
                                                  ′             ′                               ˆ                    ˆ
          Inv𝑆 (W, 𝐻,ˆ 𝜑 ) = ∀𝑝, 𝑝 . 𝑝˜ ⊆ 𝜑 ∧ 𝑝˜ ⊆ 𝜑 ∧ 𝑝∗∩                       𝐻


Fig. 13. The binary interpretation of types and terms, and semantic context interpretation. The highlighted
formulas in teal are assertions on well-formed relations, and related values. Formulas in pink and in gray are
exclusively for 𝜆 q and 𝜆𝜺q .



    The Binary Value and Term Interpretation. As our systems use dependent types, we consider
two related values at two equivalent but not identical types. For example, in the proof of rule
𝛽-eqiv in Section 5.2, we relate two types across substitutions. Thus, our relational interpretation
of type 𝑇 is written as V [[𝑇 ,𝑇 ]], which is a set of tuples of form (𝐻,
                                                                       ˆ W, 𝑣 1, 𝑣 2 ), where 𝐻ˆ is a pair of
relational value environments (defined in Fig. 13, bottom), W is a world, and 𝑣 1 and 𝑣 2 are values.
    A pair of Boolean values are related if they are both true or false. A pair of locations are related
if they store related values, in addition to their unary counterpart. Two closure records are related
if applying their enclosing 𝜆 terms with argument values that are related at the domain type,
their reduction results are related at the codomain type. In addition to the unary counterpart, we
use predicate WR to ensure that the relations on the locations reachable from related values are
well-defined, e.g., 1 , 2 , 3 and 4 in Fig. 13.
    Two terms are related if their reduction results are related at the given types.

   Example: Re-ordering (part 1). In the following example, we assume three distinct Boolean
references 𝑐 1 , 𝑐 2 and 𝑐 3 . The two sub-programs 𝑡 1 and 𝑡 2 update references 𝑐 1 and 𝑐 2 respectively,
Modeling Reachability Types with Logical Relations                                                                                  23


and are typed in the 𝜆𝜺q system that tracks observable write effects: 10

            Γ 𝑐 1 ,𝑐 2 ,𝑐 3 ⊢ 𝑐 1 : (Ref 𝐵𝑜𝑜𝑙)𝑐 1   Γ 𝑐 1 ,𝑐 2 ,𝑐 3 ⊢ 𝑐 2 : (Ref 𝐵𝑜𝑜𝑙)𝑐 2   Γ 𝑐 1 ,𝑐 2 ,𝑐 3 ⊢ 𝑐 3 : (Ref 𝐵𝑜𝑜𝑙)𝑐 3
                                                    Γ 𝑐 1 ,𝑐 3 ⊢ 𝑡 1 : 𝐵𝑜𝑜𝑙 𝑐 1
               def
           𝑡 1 = 𝑐 1 := !𝑐 3 ∧ !𝑐 1
                                                    Γ 𝑐 2 ,𝑐 3 ⊢ 𝑡 2 : 𝐵𝑜𝑜𝑙 𝑐 2
               def
           𝑡 2 = 𝑐 2 := !𝑐 3 ∧ !𝑐 2

The goal is to show that 𝑡 1 ; 𝑡 2 and 𝑡 2 ; 𝑡 1 are logically equivalent: Γ 𝑐 1,𝑐 2,𝑐 3 |= 𝑡 1 ; 𝑡 2 ≈log 𝑡 2 ; 𝑡 1 : 𝐵𝑜𝑜𝑙 𝑐 1, 𝑐 2 .
Let (𝐻,
      ˆ W) ∈ 𝐺 [[Γ 𝑐 1,𝑐 2,𝑐 3 ]]. By the definition of typing context interpretation in Fig. 13, we know
that (𝐻,
       ˆ W, 𝐻ˆ 1 (𝑐𝑖 ), 𝐻ˆ 2 (𝑐𝑖 )) ∈ V [[Ref 𝐵𝑜𝑜𝑙, Ref 𝐵𝑜𝑜𝑙]], where 𝑖 ∈ {1, 2, 3}. By the definition of value
interpretation of reference types, we know that there exists three pairs of locations (referred by
the three references), which are related in the world W (formula 1 ). Thus, each pair of the related
locations stores a pair of equivalent Boolean values (formula 2 in Fig. 13), where all the referents
(boolean values) reach the empty location, satisfying the premise of formula 2 trivially. We can
prove the equivalence by applying Theorem 5.3 in Section 5.1.
   The Time Travelling Property. Similar to the unary versions, our relational reasoning can time
travel back and forth from a past world to another (possible future) one as long as they agree on
pairs of reachable locations from the given values:

 Lemma 4.3 (Time Travelling for Binaries). If (𝜎1, 𝜎2 ) : W, and (𝐻,    ˆ W, 𝑣 1, 𝑣 2 ) ∈ V [[𝑇 ,𝑇 ′ ]], and
                               ′           ′                       ′
W ≡ (𝐿 (𝑣1 ) ∗W ,𝐿 (𝑣2 ) ∗W ) W , then (𝐻,
                                        ˆ W , 𝑣 1, 𝑣 2 ) ∈ V [[𝑇 ,𝑇 ]].
              1          2


This lemma allows us to prove the validity of a pair of values preserved w.r.t. a constructed world
in the proof of rules re-order-𝜆 q , re-order-𝜆𝜺q and 𝛽-eqiv in Section 5.

4.4    The Compatibility Lemmas, Fundamental Theorem and Soundness
Fig. 13 (bottom) defines the interpretation of typing contexts. In the definition, 𝐻ˆ ranges over a pair
of relational value environments that are finite maps from variables 𝑥 to pairs of values (𝑣 1, 𝑣 2 ). If
𝐻ˆ (𝑥) = (𝑣 1, 𝑣 2 ), then 𝐻ˆ 1 (𝑥) denotes 𝑣 1 and 𝐻ˆ 2 (𝑥) denotes 𝑣 2 . We write dom1 (𝐻ˆ ) and dom2 (𝐻ˆ ) to
mean the domain of the first and second value environment respectively. The binary semantic typing
judgment is defined as: Γ 𝜑 |= 𝑡 1 ≈log 𝑡 2 : 𝑇 𝑝 𝜺 = ∀(𝐻,
                                                          def   ˆ W) ∈ 𝐺 [[Γ 𝜑 ]].(𝐻,
                                                                                    ˆ W, 𝑡 1, 𝑡 2 ) ∈ E [[𝑇 𝑝 𝜺 ]] 𝜑 .

   Theorem 4.4 (Fundamental Property). If Γ 𝜑 ⊢ 𝑡 : 𝑇 𝑝 𝜺 , then Γ 𝜑 |= 𝑡 ≈log 𝑡 : 𝑇 𝑝 𝜺 .

   Lemma 4.5 (Congruency of Binary Logical Relations). The binary logical relation is closed
under well-typed program contexts, i.e., if Γ 𝜑 |= 𝑡 1 ≈log 𝑡 2 : 𝑇 𝑝 𝜺 , and 𝐶 : (Γ 𝜑 ;𝑇 𝑝 𝜺 ) ⇛
      ′      ′                 ′                                 ′
(Γ ′ 𝜑 ;𝑇 ′ 𝑝 𝜺 ′ ), then Γ ′ 𝜑 |= 𝐶 [𝑡 1 ] ≈log 𝐶 [𝑡 2 ] : 𝑇 ′ 𝑝 𝜺 ′ .

   Lemma 4.6 (Adeqacy of the binary logical relations). The binary logical relation preserves
termination, i.e., if ∅ |= 𝑡 1 ≈log 𝑡 2 : 𝑇 ∅ ∅ , then ∃ 𝜎, 𝜎 ′, 𝑣 1, 𝑣 2 . 𝑡 1, ∅, ∅ ⇓ 𝑣 1, 𝜎 ∧ 𝑡 2, ∅, ∅ ⇓ 𝑣 2, 𝜎 ′ .

   Theorem 4.7 (Soundness of Binary Logical Relations). The binary logical relation is sound
w.r.t. contextually equivalence, i.e., if Γ 𝜑 ⊢ 𝑡 1 : 𝑇 𝑝 𝜺 and Γ 𝜑 ⊢ 𝑡 2 : 𝑇 𝑝 𝜺 , then Γ 𝜑 |= 𝑡 1 ≈log 𝑡 2 :
𝑇 𝑝 𝜺 implies Γ 𝜑 |= 𝑡 1 ≈ctx 𝑡 2 : 𝑇 𝑝 𝜺 .

  The formalization of the encapsulated computation lemma for the binary logical relations is
omitted here. We will show its use in the proof of rule 𝛽-eqiv (i.e., Lemma 5.4) in Section 5.2.

10 Conjunction can be encoded by our sequence terms.
24                                                            Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf


     Equational Rules                                                                                                                     𝜆 q /𝜆𝜺q
                                     Γ   𝜑1
                                              ⊢ 𝑡 1 : 𝐵𝑜𝑜𝑙   𝑝1
                                                                   Γ   𝜑2
                                                                             ⊢ 𝑡 2 : 𝐵𝑜𝑜𝑙   𝑝2
                                                                                                 𝜑1 ⊆ 𝜑       𝜑2 ⊆ 𝜑   𝜑1 ∗ ∩ 𝜑2 ∗ = ∅
               (re-order-𝜆 q )
                                                                       Γ 𝜑 |= 𝑡 1 ; 𝑡 2 ≈log 𝑡 2 ; 𝑡 1 : 𝐵𝑜𝑜𝑙 ∅

                        Γ 𝜑1 ⊢ 𝑡 1 : 𝐵𝑜𝑜𝑙 𝑝 1 𝜺1        Γ 𝜑 2 ⊢ 𝑡 2 : 𝐵𝑜𝑜𝑙 𝑝 2 𝜺2           𝜑1 ⊆ 𝜑     𝜑2 ⊆ 𝜑     𝜑 1 ∗ ∩ 𝜺2 ∗ = ∅ 𝜑 2 ∗ ∩ 𝜺1 ∗ = ∅
     (re-order-𝜆𝜺q )
                                                                  Γ 𝜑 |= 𝑡 1 ; 𝑡 2 ≈log 𝑡 2 ; 𝑡 1 : 𝐵𝑜𝑜𝑙 ∅ 𝜺1 ▷ 𝜺2
                                                                         ′                   ′
                                  (Γ, 𝑥 : 𝑇 𝜑∩(𝑠 [𝑞/s])∪q∈𝑠 q ) 𝑞 ,𝑥 ⊢ 𝑡 2 : 𝑈 𝑟 [𝑞 /s] 𝜺 [𝑞 ′ /s]  Γ ∅ ⊢ 𝑡1 : 𝑇 ∅ ∅
                                                     ′                        ′
                                                    𝑞 =𝜑 ∩𝑞           𝑠˜ ⊆ 𝑞         𝜃 = [∅/𝑥, 𝑞/s]
                   (𝛽-eqiv)                                                     ′
                                                        Γ 𝜑 |= (𝜆𝑥 .𝑡 2 ) 𝑞 𝑡 1 ≈log 𝑡 2 [𝑡 1 /𝑥 ] : 𝑈 𝑟𝜃 𝜺𝜃
                                     Fig. 14. The re-ordering and 𝛽-inlining rules for 𝜆 q /𝜆𝜺q .
    Key Properties. Now, we present key properties of our binary logical relations. The following
lemma allows us to tighten a given semantic typing context to the one specified by a sub-observation.
It is used in the proof of the compatibility lemma for a sequence term, and rules re-order-𝜆 q and
re-order-𝜆𝜺q in Section 5.
                                                       ˆ W) ∈ 𝐺 [[Γ 𝜑 ]]. For all 𝜑 ′ , such
  Lemma 4.8 (Semantic Typing Context Tightening). Let (𝐻,
      ′                            ′
that 𝜑 ⊆ 𝜑, we have (𝐻,
                     ˆ W) ∈ 𝐺 [[Γ ]].
                                 𝜑

The following lemma allows us to obtain a subset of related locations that are well-defined:
  Lemma 4.9 (Relation Tightening). Let (𝐻,   ˆ W) ∈ 𝐺 [[Γ 𝜑 ]], and (𝜎1, 𝜎2 ) : W, and 𝜑 ′ ⊆ 𝜑, then
WR(W, [[𝜑 ′ ]] 𝐻W11∗, [[𝜑 ′ ]] 𝐻W22∗ )
                    ˆ            ˆ


   The following lemma allows the reasoning to focus on a world W′ , where only types and the
relation on locations (L1′ , L2′ ) are preserved.
   Lemma 4.10 (Relational Worlds Tightening). Let W and W′ be two worlds, and L1 , L2 , L1′ and
L2′ be four set of locations, such that W ≡ (L1,L2 ) W′ , and L1 ⊆ L1′ , and L2 ⊆ L2′ , and WR(W′, L1′ , L2′ ).
Then W ≡ (L1′ ,L2′ ) W′ .
   The above tightening lemmas are commonly used together in the proofs of the compatibility
lemmas (e.g., for the 𝜆- and ref cases). In those proofs, we establish relational worlds for the value
interpretation of function types and reference types respectively by those tightening lemmas,
where a world extension is assumed from a given term interpretation. Also in the proofs of rules
re-order-𝜆 q and re-order-𝜆𝜺q in Section 5.1, those tightening lemmas allow the reasoning to focus
on locations specified by the pair of sub-observations.
   Discussion: Example in Fig. 3. Now we provide informal justification for the safe use of unsafe
features (i.e., the assertion statement) in the example of Fig. 3, using the binary logical relation for 𝜆𝜺q .
We reduce the problem by showing the program where the assertion is substituted with !x == 1 is
observationally equivalent to the one where the assertion is substituted with true. This allows us to
establish the safety of the assertion without extending 𝜆𝜺q . The reasoning is straightforward: by the
fundamental property, the two programs right before the substituted statements are observationally
equivalent, where their two local references are related. Moreover, since the effect of function f
is variable 𝑦, which reaches locations separate from variable 𝑥. Thus, the referent of 𝑥 remains
unchanged, and hence, the two programs are observationally equivalent.

5     Equational Theory
This section shows applications of our binary logical relations by proving two re-ordering and
𝛽-equivalence rules. We outline the key ideas of the proofs, primarily by presenting key lemmas
and suitable worlds definitions used in the proof. Full proofs can be found in the Rocq artifacts.
Modeling Reachability Types with Logical Relations                                                                                                      25


         Pre-State: W = (Σ1 , Σ2 , 𝑓 , V̂)                                            Store locations:

                                       (𝜎1, 𝜎2 ) : W                                                       𝜑 1, 𝜑 2 : readable by 𝑡 1 , 𝑡 2
                                                                                       𝜑1        𝜑2
                                                                                                           𝜺 1, 𝜺 2 : writable by 𝑡 1 , 𝑡 2
                              𝜑1                        𝜑2                              𝜺1       𝜺2             and       to indicate reads
                                                                                                           and writes have taken place
               Prog1 :                                            Prog2 :
                t1 ; t2                                           t2 ; t1
                                                                                       Obligations:
          𝑡 1, 𝐻ˆ 1, 𝜎1 ⇓ 𝑣 𝑎 , 𝜎1′                    𝑡 2, 𝐻 2, 𝜎2 ⇓ 𝑣𝑏 , 𝜎2′
                                                            ˆ                                                    (𝜎1, 𝜎2 ) : W

 𝜑1              𝜑2       𝑂 1 : ≡𝜑1               𝑂 2 : ≡𝜑2           𝜑1                𝜑2        𝑂 3 : ≡𝜑1                          𝑂 4 : ≡𝜑2

         𝑡 2, 𝐻ˆ 1, 𝜎1′ ⇓ 𝑣𝑏′ , 𝜎1′′                   𝑡 1, 𝐻ˆ 2, 𝜎2′ ⇓ 𝑣 𝑎′ , 𝜎2′′           (𝜎1, 𝜎2′ ) : W1                        (𝜎1′ , 𝜎2 ) : W2




                                                                                                       ⊑




                                                                                                                                              ⊑
                                                                                                𝑂5 :                                   𝑂6 :
                                                                                          (𝜎1′ , 𝜎2′′ ) : W3                   (𝜎1′′, 𝜎2′ ) : W4
                                                                                              1 , Σ2 , 𝑓 , V̂ )
                                                                                      W3 = (Σ′′′                                      1 , Σ2 , 𝑓 , V̂ )
                                                                                                      ′′ 3   3               W4 = (Σ′′       ′′′ 4   4
        Post-State:           𝜑1                        𝜑2
                                                                                                                          𝑂7 :




                                                                                                                                 ⊑
                                 (𝜎1′′, 𝜎2′′ ) : W𝑅                                                             (𝜎1′′, 𝜎2′′ ) : W𝑅

                                  1 , Σ2 , 𝑓𝜺1 ,𝜺2 ; 𝑓𝜺2 ; 𝑓fr ; 𝑓𝜺1 ; 𝑓fr ; V̂𝜺1 ,𝜺2 ; V̂𝜺2 ; V̂fr ; V̂𝜺1 ; V̂fr )
                           W𝑅 = (Σ′′   ′′              4     4 3         3                4      4      3      3


Fig. 15. Illustrated proof that Prog1 = 𝑡 1 ; 𝑡 2 and Prog2 = 𝑡 2 ; 𝑡 1 are logically equivalent at world W. The key
obligations are (1) establishing equivalence of subterms (𝑡 1, 𝑡 1 ) and (𝑡 2, 𝑡 2 ) at worlds W1 and W2 respectively
(𝑂 1 & 𝑂 2 ); and (2) showing the final store pairs (𝜎1′′, 𝜎2′′ ) are well-formed w.r.t. world W𝑅 , an extension of the
inital one W (𝑂 7 ).
5.1   Re-ordering
Rules re-order-𝜆 q and re-order-𝜆𝜺q in Fig. 14 permit two computations to commute. The former
is applied to 𝜆 q , and requires the observations of the two terms to be separate; the latter is applied
to 𝜆𝜺q , and demands the observation of one term to be separate from the effects of the other. Here
we outline the proof of rule re-order-𝜆𝜺q . Rule re-order-𝜆 q can be proved analogously.
    In Fig. 15, the left side shows the definitions of the initial world W (top) and final world W𝑅
(bottom), the semantics of programs Prog1 = 𝑡 1 ; 𝑡 2 and Prog2 = 𝑡 2 ; 𝑡 1 (following the two vertical
arrows), and the major proof objections (𝑂 1 − 𝑂 7 ). The bottom right shows world relations. We
write (𝜎1, 𝜎2 ) : W ≡𝜑1 (𝜎1, 𝜎2′ ) : W1 to mean that stores (𝜎1, 𝜎2 ) and (𝜎1, 𝜎2′ ) are well-formed
w.r.t. worlds W and W1 respectively, and worlds W1 and W are related w.r.t. to 𝜑 1 . The notation
(𝜎1, 𝜎2′ ) : W1 ⊑ (𝜎1′ , 𝜎2′′ ) : W3 is defined similarly, but for world extension. We need to show that
programs Prog1 and Prog2 are logically equivalent at world W, where (𝐻,                    ˆ W) ∈ 𝐺 [[Γ 𝜑 ]].
    As shown at the top right of Fig. 15, the entire set of store locations consists of three parts: those
not observed by either the execution of term 𝑡 1 or 𝑡 2 , i.e., 𝜑 1, 𝜑 2 , and those needed by the execution
of term 𝑡 1 and 𝑡 2 respectively, i.e., 𝜑 1 and 𝜑 2 . In addition, 𝑡 1 and 𝑡 2 exclusively modify locations in 𝜺1
and 𝜺2 , respectively.
    Key Idea: Term Equivalence Preservation (Obligations 1 & 2). From the fundamental property
(Theorem 4.4), we know that (𝑡 2, 𝑡 2 )/(𝑡 1, 𝑡 1 ) are logically equivalent at world W. Observing the
semantics in Fig. 15, term 𝑡 1 /𝑡 2 is evaluated first in Prog1 /Prog2 . The key is to show that after
evaluating 𝑡 1 /𝑡 2 , the equivalence (𝑡 2, 𝑡 2 )/(𝑡 1, 𝑡 1 ) still holds at some world. Informally, the observation
𝜑 2 / 𝜑 1 specifies what is needed for maintaining the equivalence of (𝑡 2, 𝑡 2 )/(𝑡 1, 𝑡 1 ) at world W respec-
tively. As the observation of one term is separate from the effects of the other, their equivalences
are preserved.
26                                             Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf


   Lemma 5.1 (Term Eqivalence Preservation). If Γ 𝜑 ⊢ 𝑡 : 𝑇 𝑞 𝜺, and (𝐻,             ˆ W) ∈ 𝐺 [[Γ𝜑 ]], and
W = (Σ1, Σ2, 𝑓 , V̂), and (𝜎1, 𝜎2 ) : W, and ∀ℓ1, ℓ2 . W(ℓ1, ℓ2 ) ⇒ ℓ1 ∉ L and 𝜎1 → L 𝜎1′ , and Σ1 ⊑ Σ′1 , and
𝜎1′ : Σ′1 , and let W′ = (Σ′1, Σ2, 𝑓 , V̂), then (𝐻,
                                                  ˆ W′, 𝑡, 𝑡) ∈ E [[𝑇 𝑞 𝜺]] 𝜑 .
   We strengthen the conclusion of the lemma by saying that (𝑡 2, 𝑡 2 ) are equivalent at a world, such
that their relatedness is irrelevant to anything not reachable from 𝑡 2 ’s observation 𝜑 2 , or the fresh
locations during the course of evaluating 𝑡 1 in Prog1 .
   Lemma 5.2 (Term Eqivalence Preservation & Reachability). If Γ 𝜑 ⊢ 𝑡 : 𝑇 𝑞 𝜺, and (𝐻,       ˆ W) ∈
𝐺 [[Γ ]], and W = (Σ1, Σ2, 𝑓 , V̂), and (𝜎1, 𝜎2 ) : W, and 𝜎1 → L 𝜎1 , and Σ1 ⊑ Σ1 , and 𝜎1 : Σ′1 , and
     𝜑                                                             ′             ′        ′

L ∩ [[𝜑]] 𝐻W11∗ = ∅, and let W′ = (Σ′1, Σ2, 𝑓 ′, V̂′ ), and 𝑓 ′ = {(ℓ1, ℓ2 ) ∈ 𝑓 | ℓ1 ∉ L ∧ ( [[𝜑]] 𝐻W11∗ ∪
            ˆ                                                                                                    ˆ


dom(Σ)) ∩ ℓ1 ∗W1 = ∅}, and V̂′ = {(ℓ1, ℓ2, 𝑣 1, 𝑣 2 ) ∈ V̂ | ℓ1 ∉ 𝐿 ∧ ([[𝜑]] 𝐻W11∗ ∪ dom(Σ)) ∩ ℓ1 ∗W1 = ∅}, then
                                                                                ˆ


 ˆ W′, 𝑡, 𝑡) ∈ E [[𝑇 𝑞 𝜺]] 𝜑 .
(𝐻,
   Well-Formed Relational Worlds (Obligations 3 & 4). We know W ⊑𝜑2 W2 and W ⊑𝜑1 W1 by
the definition of relational worlds in Fig. 13.
   Well-Formed World Extensions (Obligations 5 & 6). These can be discharged by the definition
of term interpretation in Fig. 13.
   Well-Formed Final World (Obligation 7). We discuss the key technical points that show world
W𝑅 is a valid extension of the initial world W, and the pair of final stores are well-formed w.r.t. W𝑅 .
   We first introduce the notations 𝑓𝜺1,𝜺2 , 𝑓𝜺42 , and 𝑓𝜺31 shown in Fig. 15. Without loss of generalization,
we assume (𝐻,   ˆ W) ∈ 𝐺 [[Γ 𝜑 ]], and W = (Σ1, Σ2, 𝑓 , V̂), and the effect 𝜺 is closed at Γ. The notation
𝑓𝜺 denotes that weakening the relation to the part only covered by the interpreation of 𝜺, i.e.,
𝑓𝜺 = {(ℓ1, ℓ2 ). (ℓ1, ℓ2 ) ∈ 𝑓 ∧ ℓ1 ∈ [[𝜑 ∩ 𝜺]] 𝐻W11∗ ∧ ℓ2 ∈ [[𝜑 ∩ 𝜺]] 𝐻W22∗ }. For example, W𝜺1 ;𝜺2 denotes the
                                                 ˆ                      ˆ

relations that are unchanged during the computation.
   Now we show that 𝑓𝜺31 = 𝑓𝜺1 and 𝑓𝜺42 = 𝑓𝜺2 . This is established by W ≡𝜑2 W2 and W2 ⊑ W4 , i.e.,
W preserves the relation from 𝑓𝜑2 , and W4 is a valid extension of W2 . The notation 𝑓fr3 means the
  1

related locations that are fresh at world W3 , i.e., ∀ℓ1, ℓ2, 𝑓 3 (ℓ1, ℓ2 ) ∧ℓ1 ∈ fr(W31, W11 ) ∧ℓ2 ∈ fr(W32, W12 ).
The meaning of the notation 𝑓fr4 is defined similarly. Now, we can see that we construct the relation
in a mutually disjoint way, i.e., W𝑅𝑓 and W𝑅 are well-defined, and world W𝑅 is a valid extension of
                                                  V̂
W. From Fig. 15, we know that 𝜎1′′ : W41 and 𝜎2′′ : W32 . Thus, the pair of final stores are well-formed
w.r.t. world W𝑅 .
     Theorem 5.3. Rules re-ordering-𝜆 q and re-ordering-𝜆𝜺q in Fig. 14 are sound.
   Example: Re-ordering (part 2). The re-ordering example in Section 4.3 can now be proved
directly by applying Theorem 5.3, where 𝜑 1 = 𝑐 1, 𝑐 3 , 𝜑 2 = 𝑐 2, 𝑐 3 , 𝜑 = 𝑐 1, 𝑐 2, 𝑐 3 , 𝜺1 = 𝑐 1 , and 𝜺2 = 𝑐 2 ,
and the side conditions of rule re-order-𝜆𝜺q are all satisfied.
   Discussion: Stronger than Parallel Reduction. Prior works on reachability types [Bao et al.
2021; Wei et al. 2024] do not consider any notion of equivalance. The “progress and preservation in
parallel reduction“ property (Corollary 4.9) in prior work [Wei et al. 2024] only shows that reduction
can proceed in parallel for top-level programs, but does not show that commuting two reduction
sequences yields equivalent results in arbitrary typed program contexts. Thus, the corollary in
their work cannot be used to justify our re-ordering rules.

5.2     𝛽-Equivalence
Rule 𝛽-eqiv in Fig. 14 permits replacing a function call site 𝑡 1 with the body of the called function,
                                                              ′
provided that 𝑡 1 is observably pure. Let Prog1 be (𝜆𝑥 .𝑡 2 )𝑞 𝑡 1 , and Prog2 be 𝑡 2 [𝑡 1 /𝑥]. We need to
Modeling Reachability Types with Logical Relations                                                                                                       27


show that programs Prog1 and Prog2 are logically equivalent at world W, where (𝐻,    ˆ W) ∈ 𝐺 [[Γ 𝜑 ]],
W = (Σ1, Σ2, 𝑓 , V̂), and (𝜎1, 𝜎2 ) : W. Recall the program semantics in the followings:
                               ′                                ′
       Prog1 :   (𝜆𝑥 .𝑡 2 ) 𝑞 , 𝐻ˆ 1 , 𝜎1 ⇓ ⟨𝐻ˆ 1 , (𝜆𝑥 .𝑡 2 ) 𝑞 ⟩, 𝜎1′   𝑡 1 , 𝐻ˆ 1 , 𝜎1′ ⇓ 𝑣𝑎 , 𝜎1′′   𝑡 2 , 𝐻ˆ 1 ; (𝑥 : 𝑣𝑎 ), 𝜎1′′ ⇓ 𝑣2 , 𝜎1′′′
       Prog2 :                              ′    ′
                 𝑡 2 [𝑡 1 /𝑥 ], 𝐻 2 , 𝜎2 ⇓ 𝑣2 , 𝜎2
                                 ˆ

   Observing the above semantics of Prog1 , we know that the 𝜆-term gets evaluated first with final
store 𝜎1′ , such that 𝜎1′ : Σ′1 . Then 𝑡 1 gets evaluated to value 𝑣 𝑎 with final store 𝜎1′′ , such that 𝜎1′′ : Σ′′     1.
Let W be (Σ1, Σ, 𝑓 , V̂), and W be (Σ1 , Σ, 𝑓 , V̂). By the definition of world extension in Fig. 13, we
      1         ′                    2        ′′

know that W ⊑ W1 , and W1 ⊑ W2 . Thus, we know W ⊑ W2 by the transitivity of world extension.
   Now, our goal is to prove (𝐻ˆ 1 ; (𝑥 : 𝑣 𝑎 ), 𝐻ˆ 2,𝑊 2, 𝑡 2, 𝑡 2 [𝑡 1 /𝑥]) ∈ E [[𝑈 𝑟𝜃 𝜺𝜃 ]] 𝜑 , where 𝜃 = [∅/𝑥, 𝑞 ′ /s].
In Prog2 , term 𝑡 1 may get evaluated any time during the course of evaluating 𝑡 2 [𝑡 1 /𝑥], where 𝑡 2 ’s
effects may already occur. Note term 𝑡 1 ’s observation is the empty set, i.e., establishing (𝑡 1, 𝑡 1 )
equivalence does not need any related locations in the pre-stores. We formalize this observation in
the following lemma, which is an application of encapsulated computation lemma for binaries:
  Lemma 5.4. If Γ ∅ ⊢ 𝑡 : 𝑇 ∅ ∅, and (𝐻,  ˆ W) ∈ 𝐺 [[Γ ∅ ]], and W = (Σ1, Σ2, 𝑓 , V̂), then
(𝐻, (Σ1, Σ2, ∅, ∅), 𝑡, 𝑡) ∈ E [[𝑇 ∅]] ∅ .
 ˆ                               ∅


     From the lemma above, we know that the resulting values (𝑣 1, 𝑣 2 ) reach the empty set of locations,
i.e., 𝐿(𝑣𝑖 ) ∗W𝑐 , where W𝑐 is the resulting world and 𝑖 = 1 or 2. Now we know that (𝑣 1, 𝑣 2 ) are logically
                𝑖
equivalent at any world by Lemma 4.3. The following shows the top-level semantic weakening
lemma that captures the fact that (1) 𝑡 1 may get evaluated any time during the course of evaluating
𝑡 2 [𝑥/𝑡 1 ]; (2) 𝑣 𝑎 and the resulting value from 𝑡 1 in Prog2 are logically equivalent at any given world.
                                                                                                    ′                                                ′
   Lemma 5.5 (Semantic Weakening). If Γ ∅ ⊢ 𝑡 1 : 𝑇 ∅ ∅, and W1 = (Σ′1, Σ2, ∅, ∅), and (𝐻,                     ˆ W1 ) ∈
                                    ′
𝐺 [[Γ ∅ ]], and (𝜎1′ , 𝜎2 ) : W1 , and there exists 𝑣 𝑎 , 𝜎1′′ and Σ′′   1 , such that
      • 𝑡 1, 𝐻 1, 𝜎1′ ⇓ 𝑣 𝑎 , 𝜎1′′ , and 𝐿(𝑣 𝑎 ) ⊆ ∅, and 𝜎1′ → ∅ 𝜎1′′ , and (𝜎1′′ : Σ′′1 ), and Σ1 ⊑ Σ1 , and
                                                                                                   ′     ′′

( for all 𝐻 2 , 𝜎2 , Σ2 , L. Σ2 ≡ L Σ2 , and (𝜎2 : Σ2 ) implies there exists 𝑣𝑏 , 𝜎2 , Σ2 , such that
             ′    𝑏      𝑏                 𝑏          𝑏   𝑏                           ′ 𝑐    𝑐

      • 𝑡 1, 𝐻ˆ 2 ; 𝐻 2′, 𝜎2𝑏 ⇓ 𝑣𝑏′ , 𝜎2𝑐 , and 𝜎2𝑏 → ∅ 𝜎2𝑐 , and Σ𝑏2 ⊑ Σ𝑐2 , and
            1 , Σ2, ∅, ∅), and (𝜎1 , 𝜎2 ) : W , and ((𝐻 1, 𝐻 2 ; 𝐻 2 ), W , 𝑣 𝑎 , 𝑣𝑏 ) ∈ V [[𝑇 ,𝑇 ]], and 𝐿(𝑣 𝑎 ) Σ′′
                                                                                                                  ∗
𝑊 𝑐 = (Σ′′       𝑐                    ′′ 𝑐          𝑐          ˆ ˆ     ′      𝑐     ′                                 ⊆ ∅,
                                                                                                                    1
          ′  ∗
and 𝐿(𝑣𝑏 ) Σ𝑐 ⊆ ∅).
             2

  The following shows the top-level semantic substitution lemma, which uses the conclusion of
the semantic weakening lemma as hypothesis.
                                                                                                             ′                         ′
    Lemma 5.6 (Semantic Substitution). If (Γ, 𝑥 : 𝑇 𝜑∩(𝑠 [𝑞/s] )∪q∈𝑠 q )𝑞 ,𝑥 ⊢ 𝑡 2 : 𝑈 𝑟 [𝑞 /s] 𝜺 [𝑞 ′ /s],
and 𝑞 ′ = 𝜑 ∩𝑞, and 𝑆˜ ⊆ 𝑞 ′ , and 𝑟\𝑥 ⊆ 𝜑, and 𝜺\𝑥 ⊆ 𝜑, and W = (Σ1, Σ2, 𝑓 , V̂), and W2 = (Σ′′          1 , Σ2, 𝑓 , V̂),
and (𝐻, ˆ W2 ) ∈ 𝐺 [[Γ 𝜑 ]] and WR(W, dom1 (W), dom2 (W)) and WR(W, dom1 (W2 ), dom2 (W2 )), and
𝑡 1 satisfies semantic weakening (Lemma 5.5), then (𝐻ˆ 1 ; (𝑥 : 𝑣 𝑎 ), 𝐻ˆ 2 ), W2, 𝑡 2, 𝑡 2 [𝑡 1 /𝑥] ∈ E [[𝑈 𝑟𝜃 𝜺𝜃 ]] 𝜑 ,
where 𝜃 = [∅/𝑥, 𝑞 ′ /s].
   In the proofs of Lemma 5.5 and Lemma 5.6, we give new definitions of typing context interpreta-
tion for the not-aligned value environments, and define term substitution (omitted here). Their
proofs are conducted by induction on the type derivation of 𝑡 1 and 𝑡 2 respectively.
   From the conclusion of Lemma 5.6, we get resulting world W′ . Let 𝑓 ′ and V̂′ be the relation and
                                                                       1 , Σ2, 𝑓𝜑 ; 𝑓𝜑 ; 𝑓fr ; V̂𝜑 ; V̂𝜑 ; V̂fr ),
the related values in W′ respectively. Now we construct the world as (Σ′′′  ′         ′ ′              ′     ′

which is a valid extension of initial world W. The remainder of the proof follows similarly to the
proof of reordering and is thus omitted.
   Theorem 5.7. Rule 𝛽-equiv in Fig. 14 is sound.
28                                       Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf


   Discussion: Extensions. Rule 𝛽-eqiv restricts the argument 𝑡 1 to an empty observation set,
empty reachability qualifier, and empty write effect. While effects certainly have to be excluded
(e.g., substitution may lead to duplication of 𝑡 1 ), scenarios with non-empty observation should
also be safe, as long as 𝑡 1 is in the restricted form of variables or 𝜆-terms. While we have not yet
mechanized such extended cases in Rocq, a proof would need to show that the equivalence of two
terms is preserved over relational worlds w.r.t. the reachable locations from the given values, and
                                                       ′
the hypothesis of Lemma 5.5 needs to change W1 to (Σ′1, Σ2, 𝜑 1 ), capturing the fact that reduction
of 𝑡 1 requires locations specified in 𝜑 1 . Given the experience with different reordering rules, we are
confident that our binary logical relation can mirror the full range of possible application cases,
including fresh/non-fresh arguments, self-references in the function type, etc.

6    Related Work
   Reachability/Capturing Types. Prior works on reachability types [Bao et al. 2021; Wei et al.
2024] proved syntactic type soundness (progress and preservation). This paper presents semantic
models of reachability systems and establishes stonger semantic properties via logical relations.
The models in Section 3 are based on 𝜆 q in Wei et al. [2024]’s work, and have already been
extended with support for subtyping and polymorphism in Jia et al. [2024]’s work. Recently, Deng
et al. [2025] refined Wei et al. [2024]’s system to support cyclic references, addressing the key
limitation identified in this paper. We leave it to future work to model cyclic store structures and
non-terminating programs using step-indexed logic relations. In parallel to this work, Bunting and
Murawski [2025] investigate contextual equivalence for Bao et al. [2021]’s system using operational
game semantics and present a full abstraction model based on a labelled transition system.
   Closely related to reachability types and also tracking variables in types, capturing types [Boruch-
Gruszecki et al. 2023; Xu and Odersky 2023] are a recent effort to integrate capability tracking
and escape checking into Scala 3. While the overall goals and design are similar, there are also
important differences. Specifically, the use of self-references for escaping values and the modeling
of freshness is unique to reachability types.
   Tracking Sharing/Uniqueness/Immutability. [Giannini et al. 2019a,b] develops calculi that
infer introduced sharing during an expression’s execution. and can detect capsule references and
borrowing. Those works adopt a non-standard operational model that encodes store in the language
term. In contrast, reachability types tracks sharing as well, but uses the standard operational
semantics. [Bianchini et al. 2022] tracks sharing and mutation in a coeffect system that can model
uniqueness and immutability of references. Reachability types track sharing in qualifiers, and
mutation is tracked via the write effect extension (see Section 3.7). Language features, i.e., uniqueness
and borrowing, can be enforced by a flow-sensitive effect system, which are discussed in prior
works [Bao et al. 2021; Wei et al. 2024]. A recent work [Deng et al. 2025] introduces cyclic reference
types with dual-component that can be used to enforce read-only references. The logical relations
presented in this work does not rely on uniqueness and immutability of references.
   Ownership Types. Ownership type systems [Clarke et al. 2013, 1998; Noble et al. 1998; Potanin
et al. 2006] typically enforce strict heap invariants and selectively re-introduce sharing in a con-
trolled way via borrowing [Clebsch et al. 2015a; Hogg 1991; Naden et al. 2012]. The Rust type
system [Matsakis and Klock 2014] adopts a strong ownership model. Its “shared XOR mutable”
mechanism enforces uniqueness of mutable references while allowing sharing among immutable
ones. Marshall and Orchard [2024]’s work connects Granule’s uniqueness modality [Orchard et al.
2019] and its graded model types with ideas from Rust, allowing ownership tracking in a graded
type system. In contrast, reachability types are designed to track sharing (thus separation), rather
than restrict it. The focus is on higher-level languages, where many common idioms rely on sets of
Modeling Reachability Types with Logical Relations                                                  29


closures as an interface to interact with a piece of (shared!) mutable state. Uniqueness properties
can be enforced via flow-sensitive move effects [Bao et al. 2021; Jia et al. 2024]. In the context of
Rust, Jung et al. [2018a] developed lifetime logic to model lifetimes and borrowing in a variant of
Rust’s MIR, where programs are expressed in continuation-passing style. Their logical framework
can verify unsafe code with safe APIs for Rust programs. In contrast, our work aims to verify
equational rules using observational equivalence. We showed an informal justification of a safe use
of assertion statements by reducing the problem to proving observational equivalence (Section 4.4),
but unlike Jung et al. [2018a]’s work, our goal is not to verify safe use of general unsafe code.
   Capabilities and Permissions. Capability systems [Boyland et al. 2001; Castegren and Wrigstad
2016] have been used to reason about program resources and external calls [Drossopoulou et al.
2025]. In Pony [Clebsch 2017], reference capabilities describe what other aliases are denied [Clebsch
et al. 2015b; Dodds et al. 2009], e.g., deny local/global read/write aliases. In contrast, reachability
types [Bao et al. 2021; Wei et al. 2024] do not distinguish read and write capabilities. Read-only
capabilities can be enforced via cyclic reference types with dual-component [Deng et al. 2025],
which is not modeled in this work. Haller and Odersky [2010] leverage capabilities to ensure
externally unique access with borrowing. Gordon et al. [2012] extend their work with immutable
references for safe parallelism. Their symmetric parallelism rule enforces constraints on read and
write that are similar to our rule re-ordering-𝜆𝜺q . In contrast, our system does not rely on the
uniqueness or immutability of references, but instead leverages aliasing/separation and write effects
tracking. Unique mutable references can be enforced via a flow-sensitive effect system, which has
been discussed in prior works [Bao et al. 2021; Wei et al. 2024]. We leave a thorough investigation
as future work.
   Step-Indexed Logical Relations. Step-indexed logical relations have been used to prove semantic
type soundness [Ahmed 2004; Appel and McAllester 2001], program termination [Spies et al. 2021;
Timany et al. 2024] and contextual equivalence [Ahmed 2006], representation independence [Ahmed
et al. 2009; Timany et al. 2024], monadic encapsulation of state achieved by runST using rank-2
polymorphism [Timany et al. 2018] for languages with general recursive and polymorphic types.
In these approaches, types are indexed by computation steps to guarantee well-founded recursions
have unique fixed points. Since all well-typed programs are guaranteed to terminate in our systems,
our LR models do not require step-indexes. As future work, we plan to extend our models to support
recursion and cyclic references, and we are interested in using the Iris logic framework [Jung et al.
2016, 2018b, 2015; Krebbers et al. 2017] to avoid manual step indexes and similar proof devices.
   Effect-Based Program Transformation. Close to our approach that uses effects for validating
program transformations, Benton et al. [2014, 2007] developed denotational, semantic relational
models based on a monotonic regions and effects for a higher-order language with dynamically
allocated first-order mutable stores, and with high-order stores without dynamic allocation [Benton
et al. 2009, 2006]. Our world model is adapted from Benton et al. [2007]’s work, and our use of
observable write effects to prove observational equivalence coincides with Benton et al. [2014]’s
work. Unlike their works, we adopt a big-step operational semantics based on closures and envi-
ronments, which is closer to real language implementations. In addition, our effect system does not
track allocation effects, thus, our models assume allocation always occurs during the reduction
of a term. This design works well, as we can leverage reachability qualifiers. For example, the
absence of the freshness marker indicates values do not reach fresh locations. In this case, freshly
allocated locations cannot be reached from clients. Benton et al. [2016] developed models to validate
effect-dependent program transformations for concurrent programs, which is beyond the scope of
this work and left as future work.
30                                               Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf


   World Models. Birkedal et al. [2016]; Thamsborg and Birkedal [2011]’s work defines a Kripke
logical relation based on a region-polymorphic type-and-effect system for an ML-like programming
language with higher-order mutable stores with dynamic allocations. In their work, a world is the
part of the entire store that the program controls, while our world describes the entire store, and
we use the separation of saturated reachability qualifiers/observations and observable write effects
to achieve different degrees of local reasoning. Reachability types feature lightweight reachability
polymorphism via qualifier dependent function application, and use self-references to succinctly
express if returned values are fresh, without introducing explicit quantification. Wei et al. [2024]’s
work has proven syntactic type soundness for reachability and type polymorphism (F<:     q ).

7 Conclusion
In this paper, we presented semantic models for a family of reachability type systems with increas-
ing sets of features, and showed how reachability types naturally lead to strong local reasoning
properties. The results established, i.e., semantic type soundness, termination, effect safety, and pro-
gram equivalence, are stronger than those in prior works on reachability types. We also proved key
equational rules such as reordering and 𝛽-equivalence, providing a firm foundation for reachability-
driven program transformations. All results are proven in Rocq.

Acknowledgments
We thank Siyuan He and Haotian Deng for related contributions to reachability types. This work
was supported in part by NSF awards 2348334 and Augusta faculty startup package, as well as gifts
from Meta, Google, Microsoft, and VMware.

References
Amal Ahmed, Derek Dreyer, and Andreas Rossberg. 2009. State-dependent representation independence. In POPL. ACM,
   340–353. doi:10.1145/1480881.1480925
Amal Jamil Ahmed. 2004. Semantics of types for mutable state. Princeton University.
Amal J. Ahmed. 2006. Step-Indexed Syntactic Logical Relations for Recursive and Quantified Types. In ESOP (Lecture Notes
   in Computer Science, Vol. 3924). Springer, 69–83. doi:10.1007/11693024_6
Nada Amin, Samuel Grütter, Martin Odersky, Tiark Rompf, and Sandro Stucki. 2016. The Essence of Dependent Object
   Types. In A List of Successes That Can Change the World (Lecture Notes in Computer Science, Vol. 9600). Springer, 249–272.
   doi:10.1007/978-3-319-30936-1_14
Nada Amin and Tiark Rompf. 2017. Type soundness proofs with definitional interpreters. In POPL. ACM, 666–679.
   doi:10.1145/3009837.3009866
Andrew W. Appel and David A. McAllester. 2001. An indexed model of recursive types for foundational proof-carrying
   code. ACM Trans. Program. Lang. Syst. 23, 5 (2001), 657–683. doi:10.1145/504709.504712
Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf. 2025. Modeling Reachability Types with Logical
   Relations. Proc. ACM Program. Lang. 9, OOPSLA (2025). doi:10.1145/3763116
Yuyan Bao, Guannan Wei, Oliver Bračevac, Yuxuan Jiang, Qiyang He, and Tiark Rompf. 2021. Reachability types: tracking
   aliasing and separation in higher-order functional programs. Proc. ACM Program. Lang. 5, OOPSLA (2021), 1–32.
   doi:10.1145/3485516
Nick Benton, Martin Hofmann, and Vivek Nigam. 2014. Abstract effects and proof-relevant logical relations. In POPL. ACM,
   619–632. doi:10.1145/2535838.2535869
Nick Benton, Martin Hofmann, and Vivek Nigam. 2016. Effect-dependent transformations for concurrent programs. In
   PPDP. ACM, 188–201. doi:10.1145/2967973.2968602
Nick Benton, Andrew Kennedy, Lennart Beringer, and Martin Hofmann. 2007. Relational semantics for effect-based program
   transformations with dynamic allocation. In PPDP. ACM, 87–96. doi:10.1145/1273920.1273932
Nick Benton, Andrew Kennedy, Lennart Beringer, and Martin Hofmann. 2009. Relational semantics for effect-based program
   transformations: higher-order store. In PPDP. ACM, 301–312. doi:10.1145/1599410.1599447
Nick Benton, Andrew Kennedy, Martin Hofmann, and Lennart Beringer. 2006. Reading, Writing and Relations. In APLAS
   (Lecture Notes in Computer Science, Vol. 4279). Springer, 114–130. doi:10.1007/11924661_7
Riccardo Bianchini, Francesco Dagnino, Paola Giannini, Elena Zucca, and Marco Servetto. 2022. Coeffects for sharing and
   mutation. Proc. ACM Program. Lang. 6, OOPSLA2 (2022), 870–898. doi:10.1145/3563319
Modeling Reachability Types with Logical Relations                                                                    31


Lars Birkedal, Guilhem Jaber, Filip Sieczkowski, and Jacob Thamsborg. 2016. A Kripke logical relation for effect-based
   program transformations. Inf. Comput. 249 (2016), 160–189. doi:10.1016/J.IC.2016.04.003
Aleksander Boruch-Gruszecki, Martin Odersky, Edward Lee, Ondrej Lhoták, and Jonathan Immanuel Brachthäuser. 2023.
   Capturing Types. ACM Trans. Program. Lang. Syst. 45, 4 (2023), 21:1–21:52. doi:10.1145/3618003
John Boyland, James Noble, and William Retert. 2001. Capabilities for Sharing: A Generalisation of Uniqueness and
   Read-Only. In ECOOP (Lecture Notes in Computer Science, Vol. 2072). Springer, 2–27. doi:10.1007/3-540-45337-7_2
Oliver Bračevac, Guannan Wei, Songlin Jia, Supun Abeysinghe, Yuxuan Jiang, Yuyan Bao, and Tiark Rompf. 2023a. Graph IRs
   for Impure Higher-Order Languages – Making Aggressive Optimizations Affordable with Precise Effect Dependencies.
   Proc. ACM Program. Lang. 7, OOPSLA2 (2023), 236:1–236:30. doi:10.1145/3622813
Oliver Bračevac, Guannan Wei, Songlin Jia, Supun Abeysinghe, Yuxuan Jiang, Yuyan Bao, and Tiark Rompf. 2023b. Graph
   IRs for Impure Higher-Order Languages (Supplement). arXiv:2309.08118 [cs.PL]
B Bunting and AS Murawski. 2025. Reachability types, traces and full abstraction. 40th Annual ACM/IEEE Symposium on
   Logic in Computer Science (LICS 2025) (2025). https://ora.ox.ac.uk/objects/uuid:7ec96a90-1bb8-408d-90a8-26126a3bbc05
Elias Castegren and Tobias Wrigstad. 2016. Reference Capabilities for Concurrency Control. In ECOOP (LIPIcs, Vol. 56).
   Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 5:1–5:26. doi:10.4230/LIPICS.ECOOP.2016.5
Dave Clarke, Johan Östlund, Ilya Sergey, and Tobias Wrigstad. 2013. Ownership Types: A Survey. In Aliasing in Object-
   Oriented Programming. Lecture Notes in Computer Science, Vol. 7850. Springer, 15–58. doi:10.1007/978-3-642-36946-9_3
David Clarke, John Potter, and James Noble. 1998. Ownership Types for Flexible Alias Protection. In OOPSLA. ACM, 48–64.
Sylvan Clebsch. 2017. ’Pony’: co-designing a type system and a runtime. Ph. D. Dissertation. Imperial College London, UK.
   https://ethos.bl.uk/OrderDetails.do?uin=uk.bl.ethos.769552
Sylvan Clebsch, Sebastian Blessing, Juliana Franco, and Sophia Drossopoulou. 2015a. Ownership and reference counting
   based garbage collection in the actor world. In ICOOOLPS’2015. ACM.
Sylvan Clebsch, Sophia Drossopoulou, Sebastian Blessing, and Andy McNeil. 2015b. Deny capabilities for safe, fast actors.
   In AGERE SPLASH. ACM, 1–12. doi:10.1145/2824815.2824816
Haotian Deng, Siyuan He, Songlin Jia, Yuyan Bao, and Tiark Rompf. 2025. Complete the Cycle: Reachability Types with
   Expressive Cyclic References. Proc. ACM Program. Lang. 9, OOPSLA (2025). doi:10.1145/3763172
Mike Dodds, Xinyu Feng, Matthew J. Parkinson, and Viktor Vafeiadis. 2009. Deny-Guarantee Reasoning. In ESOP (Lecture
   Notes in Computer Science, Vol. 5502). Springer, 363–377. doi:10.1007/978-3-642-00590-9_26
Sophia Drossopoulou, Julian Mackay, Susan Eisenbach, and James Noble. 2025. Reasoning about External Calls.
   arXiv:2506.06544 [cs.PL]
Erik Ernst, Klaus Ostermann, and William R. Cook. 2006. A virtual class calculus. In POPL. ACM, 270–282. doi:10.1145/
   1111037.1111062
Paola Giannini, Tim Richter, Marco Servetto, and Elena Zucca. 2019a. Tracing sharing in an imperative pure calculus. Sci.
   Comput. Program. 172 (2019), 180–202. doi:10.1016/J.SCICO.2018.11.007
Paola Giannini, Marco Servetto, Elena Zucca, and James Cone. 2019b. Flexible recovery of uniqueness and immutability.
   Theor. Comput. Sci. 764 (2019), 145–172. doi:10.1016/J.TCS.2018.09.001
Colin S. Gordon, Matthew J. Parkinson, Jared Parsons, Aleks Bromfield, and Joe Duffy. 2012. Uniqueness and reference
   immutability for safe parallelism. In OOPSLA. ACM, 21–40. doi:10.1145/2384616.2384619
Philipp Haller and Martin Odersky. 2010. Capabilities for uniqueness and borrowing. In European Conference on Object-
   Oriented Programming. Springer, 354–378. doi:10.1007/978-3-642-14107-2_17
John Hogg. 1991. Islands: Aliasing Protection in Object-Oriented Languages. In OOPSLA. ACM, 271–285. doi:10.1145/117954.
   117975
Songlin Jia, Guannan Wei, Siyuan He, Yueyang Tang, Yuyan Bao, and Tiark Rompf. 2024. Escape with Your Self: Expressive
   Reachability Types with Sound and Decidable Bidirectional Type Checking. arXiv:2404.08217 [cs.PL]
Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2018a. RustBelt: securing the foundations of the
   rust programming language. Proc. ACM Program. Lang. 2, POPL (2018), 66:1–66:34. doi:10.1145/3158154
Ralf Jung, Robbert Krebbers, Lars Birkedal, and Derek Dreyer. 2016. Higher-order ghost state. In ICFP. ACM, 256–269.
   doi:10.1145/2951913.2951943
Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and Derek Dreyer. 2018b. Iris from the
   ground up: A modular foundation for higher-order concurrent separation logic. J. Funct. Program. 28 (2018), e20.
   doi:10.1017/S0956796818000151
Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. 2015. Iris:
   Monoids and Invariants as an Orthogonal Basis for Concurrent Reasoning. In POPL. ACM, 637–650. doi:10.1145/2676726.
   2676980
Robbert Krebbers, Ralf Jung, Ales Bizjak, Jacques-Henri Jourdan, Derek Dreyer, and Lars Birkedal. 2017. The Essence of
   Higher-Order Concurrent Separation Logic. In ESOP (Lecture Notes in Computer Science, Vol. 10201). Springer, 696–723.
   doi:10.1007/978-3-662-54434-1_26
32                                               Yuyan Bao, Songlin Jia, Guannan Wei, Oliver Bračevac, and Tiark Rompf


P. J. Landin. 1964. The Mechanical Evaluation of Expressions. Comput. J. 6, 4 (1964), 308–320. doi:10.1093/COMJNL/6.4.308
Danielle Marshall and Dominic Orchard. 2024. Functional Ownership through Fractional Uniqueness. Proc. ACM Program.
    Lang. 8, OOPSLA1 (2024), 1040–1070. doi:10.1145/3649848
Nicholas D. Matsakis and Felix S. II Klock. 2014. The Rust language. In HILT. ACM, 103–104. doi:10.1145/2663171.2663188
Karl Naden, Robert Bocchino, Jonathan Aldrich, and Kevin Bierhoff. 2012. A type system for borrowing permissions. In
    POPL. ACM, 557–570. doi:10.1145/2103656.2103722
James Noble, Jan Vitek, and John Potter. 1998. Flexible Alias Protection. In ECOOP (Lecture Notes in Computer Science,
    Vol. 1445). Springer, 158–185. doi:10.1007/BFb0054091
Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local Reasoning about Programs that Alter Data Structures.
    In CSL (Lecture Notes in Computer Science, Vol. 2142). Springer, 1–19. doi:10.1007/3-540-44802-0_1
Dominic Orchard, Vilem-Benjamin Liepelt, and Harley Eades III. 2019. Quantitative program reasoning with graded modal
    types. Proc. ACM Program. Lang. 3, ICFP (2019), 110:1–110:30. doi:10.1145/3341714
Benjamin C. Pierce. 2004. Advanced Topics in Types and Programming Languages. The MIT Press.
G. D. Plotkin. 1973. Lambda Definability and Logical Relations. Memorandum SAI-RM-4. University of Edinburgh. https:
    //homepages.inf.ed.ac.uk/gdp/publications/logical_relations_1973.pdf
Alex Potanin, James Noble, Dave Clarke, and Robert Biddle. 2006. Generic ownership for generic Java. In OOPSLA. ACM,
    311–324. doi:10.1145/1167473.1167500
John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In LICS. IEEE Computer Society,
    55–74. doi:10.1109/LICS.2002.1029817
Tiark Rompf and Nada Amin. 2016. Type soundness for dependent object types (DOT). In OOPSLA. ACM, 624–641.
    doi:10.1145/2983990.2984008
Jeremy Siek. 2013. Type safety in three easy lemmas. http://siek.blogspot.com/2013/05/type-safety-in-three-easy-lemmas.
    html.
Simon Spies, Neel Krishnaswami, and Derek Dreyer. 2021. Transfinite step-indexing for termination. Proc. ACM Program.
    Lang. 5, POPL (2021), 1–29. doi:10.1145/3434294
William W. Tait. 1967. Intensional Interpretations of Functionals of Finite Type I. J. Symb. Log. 32, 2 (1967), 198–212.
    doi:10.2307/2271658
Jacob Thamsborg and Lars Birkedal. 2011. A Kripke logical relation for effect-based program transformations. In ICFP. ACM,
    445–456. doi:10.1145/2034773.2034831
Amin Timany, Robbert Krebbers, Derek Dreyer, and Lars Birkedal. 2024. A Logical Approach to Type Soundness. J. ACM
    71, 6 (2024), 40:1–40:75. doi:10.1145/3676954
Amin Timany, Léo Stefanesco, Morten Krogh-Jespersen, and Lars Birkedal. 2018. A logical relation for monadic encapsulation
    of state: proving contextual equivalences in the presence of runST. Proc. ACM Program. Lang. 2, POPL (2018), 64:1–64:28.
    doi:10.1145/3158152
Fei Wang and Tiark Rompf. 2017. Towards Strong Normalization for Dependent Object Types (DOT). In ECOOP (LIPIcs,
    Vol. 74). Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 27:1–27:25. doi:10.4230/LIPIcs.ECOOP.2017.27
Guannan Wei, Oliver Bračevac, Songlin Jia, Yuyan Bao, and Tiark Rompf. 2024. Polymorphic Reachability Types: Tracking
    Freshness, Aliasing, and Separation in Higher-Order Generic Programs. Proc. ACM Program. Lang. 8, POPL (2024),
    393–424. doi:10.1145/3632856
Andrew K. Wright and Matthias Felleisen. 1994. A Syntactic Approach to Type Soundness. Inf. Comput. 115, 1 (1994), 38–94.
    doi:10.1006/INCO.1994.1093
Yichen Xu and Martin Odersky. 2023. Degrees of Separation: A Flexible Type System for Data Race Prevention. doi:10.
    48550/ARXIV.2308.07474
