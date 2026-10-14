                                        Substructural Parametricity
                                        C. B. Aberlé #
                                        Carnegie Mellon University
                                        Chris Martens #
                                        Northeastern University
                                        Frank Pfenning #
                                        Carnegie Mellon University

                                              Abstract
                                        Ordered, linear, and other substructural type systems allow us to expose deep properties of programs
                                        at the syntactic level of types. In this paper, we develop a family of unary logical relations that allow
arXiv:2503.03153v1 [cs.LO] 5 Mar 2025




                                        us to prove consequences of parametricity for a range of substructural type systems. A key idea is to
                                        parameterize the relation by an algebra, which we exemplify with a monoid and commutative monoid
                                        to interpret ordered and linear type systems, respectively. We prove the fundamental theorem
                                        of logical relations and apply it to deduce extensional properties of inhabitants of certain types.
                                        Examples include demonstrating that the ordered types for list append and reversal are inhabited by
                                        exactly one function, as are types of some tree traversals. Similarly, the linear type of the identity
                                        function on lists is inhabited only by permutations of the input. Our most advanced example shows
                                        that the ordered type of the list fold function is inhabited only by the fold function.

                                        2012 ACM Subject Classification Theory of computation → Type structures

                                        Keywords and phrases Substructural type systems, logical relations, ordered logic


                                        Acknowledgements We would like to thank Karl Crary for an early instantiation of the underlying
                                        idea.


                                         1     Introduction
                                        Substructural type systems and parametric polymorphism are two mechanisms for capturing
                                        precise behavioral properties of programs at the type level, enabling powerful static reasoning.
                                        The goal of this paper is to give a theoretical account of these mechanisms in combination.
                                            Substructural type systems have been investigated since the advent of linear logic,
                                        starting with the seminal paper by Girard and Lafont [11]. Among other applications, with
                                        substructural type systems one can avoid garbage collection, update memory in place [20, 21],
                                        make message-passing [9, 7] or shared memory concurrency [10, 28] safe, model quantum
                                        computation [8], or reason efficiently about imperative programs [19]. Substructural type
                                        systems have thus been incorporated into languages that seek to offer such guarantees, such
                                        as Rust, Koka, Haskell, Oxidized OCaml, and ProtoQuipper.
                                            Parametricity, originally introduced for System F [35], enables the idea that programs
                                        whose types involve universal quantification over type parameters have certain strong semantic
                                        properties. This idea supports powerful program reasoning principles such as representation
                                        independence across abstraction boundaries [23] and “theorems for free” that can be derived
                                        about all inhabitants of certain types, for example that every inhabitant of ∀α. α → α is
                                        equivalent to the identity function [38].
                                            The theory of substructural logics and type systems is now relatively well understood,
                                        including several ways to integrate substructural and structural type systems [6, 31, 12]. It
                                        is therefore somewhat surprising that we do not yet know much about how parametricity
                                        and its applications interact with them. The main foray into substructural parametricity is a
                                        paper by Zhao et al. [39] that accounts for a polymorphic dual-intuitionistic linear logic. They
                                                   © C. B. Aberlé, Chris Martens, and Frank Pfenning;
                                                   licensed under Creative Commons License CC-BY 4.0
                                                          Leibniz International Proceedings in Informatics
                                                          Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
XX:2   Substructural Parametricity


       point out that logical relations on closed terms are problematic because substitution obscures
       linearity. Their solution was to construct a logical relation on open terms, necessitating the
       introduction of “semantic typing” judgments that mirror the syntactic type system, which
       complicates their definition and application.
           In this paper, we follow an approach using constructive resource semantics in the style
       of Reed et al. [32, 34, 33] to construct logical relations on closed terms. We start with
       an ordered type system [30, 29, 17], which may be considered the least permissive among
       substructural type systems and therefore admits a pleasantly minimal definition. However,
       the construction is generic with respect to certain properties of the resource algebra, which
       allows us to extend it also to linear and unrestricted types. Consequences of our development
       include that certain polymorphic types are only inhabited by the polymorphic append and
       reverse functions on lists. Similarly, certain types are only inhabited by functions that swap
       or maintain the order of pairs. The most advanced application shows that the ordered type
       of fold over lists is inhabited only by the fold function.
           We conjecture that the three substructural modes we investigate—ordered, linear, and
       unrestricted—can also be combined in an adjoint framework [6, 12] but leave this to future
       work. Similarly, we simplify our presentation by defining only a unary logical relation since
       it is sufficient to demonstrate proof-of-concept, but nothing stands in the way of a more
       general definition (for example, to support representation independence results).


        2     A Minimalist Fragment

       We start with a small fragment of the Full Lambek Calculus [18, 22], extended with parametric
       polymorphism [36]. This fragment is sufficient to illustrate the main ideas behind our
       constructions. For the sake of simplicity we choose a Curry-style formulation of typing,
       concentrating on properties of untyped terms rather than intrinsically typed terms. This
       allows the same terms to inhabit ordered, linear, and unrestricted types and thereby focus
       on semantic rather than syntactic issues.

            Types       A, B     ::=   α | A • B | A ↣ B | A ↠ B | ∀α. A
            Expressions e        ::=   x
                                   |   (e1 , e2 ) | match e ((x, y) ⇒ e′ )    (A • B)
                                   |   λx. e | e1 e2                          (A ↣ B, A ↠ B)

       In this fragment, we have A • B (read “A fuse B”) which, logically, is a noncommutative
       conjunction. We have two forms of implication: A ↣ B (read: “A under B”, originally
       written as A\B) which is true if from the hypothesis A placed at the left end of the antecedents
       we can deduce B, and A ↠ B (read: “B over A”, originally written as B / A) which is true if
       from the hypothesis A placed at the right and of the antecedents we can prove B. Lambek’s
       original notation was suitable for the sequent calculus and its applications in linguistics, but
       is less readable for natural deduction and functional programming.
           Our basic typing judgment has the form ∆ | Ω ⊢ e : A where ∆ consists of hypotheses
       α type, and Ω is an ordered context (x1 : A1 ) . . . (xn : An ). We make the standard presuppo-
       sitions that ∆ ⊢ A type and ∆ ⊢ Ai type for every xi : Ai in Ω, and that both type variables
       and term variables are pairwise distinct. The rules are show in Figure 1.
           Here are a few example judgments that hold or fail.          We elide the context ∆ =
       (α type, β type, γ type).
C. B. Aberlé and Chris Martens and Frank Pfenning                                                            XX:3



                                                             hyp
                                              ∆|x:A⊢x:A

            ∆ | Ω (x : A) ⊢ e : B                 ∆ | Ω ⊢ e1 : A ↠ B     ∆ | ΩA ⊢ e 2 : A
                                       ↠I                                                      ↠E
           ∆ | Ω ⊢ λx. e : A ↠ B                          ∆ | Ω ΩA ⊢ e1 e2 : B

             ∆ | (x : A) Ω ⊢ e : B               ∆ | Ω ⊢ e1 : A ↣ B      ∆ | ΩA ⊢ e 2 : A
                                        ↣I                                                  ↣E
            ∆ | Ω ⊢ λx. e : A ↣ B                        ∆ | ΩA Ω ⊢ e1 e2 : B

 ∆ | ΩA ⊢ e1 : A ∆ | ΩB ⊢ e2 : B               ∆|Ω⊢e:A•B           ∆ | ΩL (x : A) (y : B) ΩR ⊢ e′ : C
                                         •I                                                             •E
    ∆ | ΩA ΩB ⊢ (e1 , e2 ) : A • B                 ∆ | ΩL Ω ΩR ⊢ match e ((x, y) ⇒ e′ ) : C

               ∆, α type | Ω ⊢ e : A               ∆ | Ω ⊢ e : ∀α.A(α)     ∆ ⊢ B type
                                         ∀I                                               ∀E
                 ∆ | Ω ⊢ e : ∀α. A                         ∆ | Ω ⊢ e : A(B)


   Figure 1 Ordered Natural Deduction




                           ⊢     λx. x : α ↣ α
                         ⊢       λx. x : α ↠ α
                         ̸ ⊢     λx. λy. x : α ↠ (β ↠ α)                          (no weakening)
                           ̸⊢    λx. (x, x) : α ↠ (α • α)                         (no contraction)
                            ⊢    λx. λy. (x, y) : α ↠ (β ↠ (α • β))
                            ̸⊢   λx. λy. (x, y) : α ↣ (β ↣ (α • β))               (no exchange)
     f : β ↠ (α ↣ γ)     ⊢ λx. λy. (f y) x : α ↣ (β ↠ γ)                          (“associativity”)
     g : α ↣ (β ↠ γ)     ⊢ λy. λx. (g x) y : β ↠ (α ↣ γ)
     g : (α • β) ↠ γ     ⊢       λx. λy. g (x, y) : α ↠ (β ↠ γ)                   (currying)
     f : α ↠ (β ↠ γ)     ⊢       λp. match p ((x, y) ⇒ f x y) : (α • β) ↠ γ       (uncurrying)

    The strictures of the typing judgment imply that certain types may be uninhabited, or
may be inhabited by terms that are extensionally equivalent to a small number of possibilities.
To count the number of linear functions, translate (A ↠ B)L = (A ↣ B)L = AL ⊸ B L and
(A • B)L = AL ⊗ B L and similarly for unrestricted functions.

                     Types                     Ordered   Linear    Unrestricted
                     α↠α                          1        1            1
                     α ↠ (α ↠ α)                  0        0            2
                     α ↠ (α ↠ (α • α))            1        2            4
                     α ↠ (α ↣ (α • α))            1        2            4
                     α ↠ (β ↠ (β • α))            0        1            1
                     α ↠ (β ↠ (α • β))            1        1            1

    Because our intended application language based on adjoint natural deduction [12] is
call-by-value, we can give a straightforward big-step operational semantics [15] relating an
expression to its final value. Because this evaluation does not directly interact with or benefit
from substructural properties, we show it without further comment in Figure 2. It has the
property of preservation that if · ⊢ e : A and e ,→ v then · ⊢ v : A. Jang et al. give an
XX:4   Substructural Parametricity


       account [12] that exploits linearity and other substructural properties, although not the lack
       of exchange.


                                        e1 ,→ λx. e′1   e2 ,→ v2     [v2 /x]e′1 ,→ v
             λx. e ,→ λx. e                             e1 e2 ,→ v

             e1 ,→ v1     e2 ,→ v2           e ,→ (v1 , v2 )   [v1 /x, v2 /y]e′ ,→ v ′
             (e1 , e2 ) ,→ (v1 , v2 )           match e ((x, y) ⇒ e′ ) ,→ v ′


            Figure 2 Big-Step Operational Semantics



        3      An Algebraic Logical Predicate
       Because of our particular setting, we define two mutually dependent logical predicates: JAK
       for closed expressions and [A] for closed values. In addition, the relation is parameterized
       by elements from an algebraic domain which may have various properties. For the ordered
       case, it should be a monoid, for the linear case a commutative monoid. However, the rules
       themselves do not require this for the pure sets of terms. We use m·n for the binary operation
       on the monoid, and ϵ for its unit.
           Ignoring polymorphism for now, we write m ⊩ e ∈ JAK and m ⊩ v ∈ [A], which is defined
       by

        m ⊩ e ∈ JAK               ⇐⇒     e ,→ v ∧ m ⊩ v ∈ [A]

        m ⊩ v ∈ [1]               ⇐⇒ m = ϵ ∧ v = ( )
        m ⊩ v ∈ [A • B]           ⇐⇒ ∃m1 , m2 . m = m1 · m2 ∧ v = (v1 , v2 ) ∧ m1 ⊩ v1 ∈ [A] ∧ m2 ⊩ v2 ∈ [B]
        m ⊩ v ∈ [A ↠ B]           ⇐⇒ ∀k. k ⊩ w ∈ [A] =⇒ m · k ⊩ v w ∈ JBK
        m ⊩ v ∈ [A ↣ B]           ⇐⇒ ∀k. k ⊩ w ∈ [A] =⇒ k · m ⊩ v w ∈ JBK

       We can see how the algebraic structure of the monoid tracks information about order if its
       operation is not commutative.
           The key step, as usual in logical predicates of this nature, is the case for universal
       quantification and type variables. We map type variables α to relations RB between monoid
       elements and values in [B] where B is a closed type. We indicate this mapping from type
       variables to sets of values S and write it as a superscript on ⊩.

             m ⊩S v ∈ [α]               ⇐⇒      m S(α) v
             m ⊩S v ∈ [∀α. A(α)]        ⇐⇒      ∀B, RB . m ⊩S,α7→RB v ∈ [A(α)]

       The mapping S is just passed through identically in the cases of the relation defined above.
           We can already verify some interesting properties. As a first example we show that the
       logical predicates are nonempty.
       ▶ Theorem 1.

            ϵ ⊩ λx. λy. (x, y) ∈ J∀α. α ↠ (α ↠ (α • α))K

       Proof. Because the λ-expression is a value, we need to check

            ϵ ⊩ λx. λy. (x, y) ∈ [∀α. α ↠ (α ↠ (α • α))]
C. B. Aberlé and Chris Martens and Frank Pfenning                                                   XX:5


By definition, this is true if for an arbitrary A and relation m RA v we have

     ϵ ⊩α7→RA λx. λy. (x, y) ∈ [α ↠ (α ↠ (α • α))]

Using the definition of the logical predicate for right implication twice and one intermediate
step of evaluation, this holds iff

     m · k ⊩α7→RA (λy. (v, y)) w ∈ Jα • αK

for all m, k with m ⊩α7→RA v and k ⊩α7→RA w. By evaluation, this is true iff

     m · k ⊩α7→RA (v, w) ∈ [α • α]

Now we can apply the definition of [A • B], splitting m · k into m and k and reducing it to

     m ⊩α7→RA v ∧ k ⊩α7→RA w

Both of these hold because, by assumption, m RA v and k RA w.                                   ◀

     More interesting, perhaps, is the reverse.

▶ Theorem 2. If

     ϵ ⊩ e ∈ J∀α. α ↠ (α ↠ (α • α))K

then e is extensionally equal to λx. λy. (x, y). In particular, it can not be λx. λy. (y, x).

Proof. We choose our monoid to be the free monoid over two generators a and b and we
choose an arbitrary closed type A and two elements v and w. Moreoever, we pick RA relating
only a RA v and b RA w.
   From the definitions (and skipping over some simple properties regarding evaluation), we
obtain

     a · b ⊩α7→RA e v w ∈ Jα • αK

By the clauses for Jα • αK, [α • α] and α we conclude that

     e v w ,→ (u1 , u2 )

for some values u1 and u2 with a RA u1 and b RA u2 . Because the only value related to a is
v and the only value related to b is w, we conclude u1 = v and u2 = w. Therefore

     e v w ,→ (v, w)

Since v and w were chosen arbitrarily, we see that e is extensionally equal to λx. λy. (x, y). ◀

 4      The Fundamental Theorem
The fundamental theorem of logical predicates states that every well-typed term is in the
predicate. Our relations also include terms that are not well-typed, which can occasionally
be useful when one exceeds the limits of static typing.
   We need a few standard lemmas, adapted to this case. We only spell out one.

▶ Lemma 3 (Compositionality). Define RA such that k RA w iff k ⊩ w ∈ [A]. Then
m ⊩S,α7→RA v ∈ [B(α)] iff m ⊩S v ∈ [B(A)]
XX:6   Substructural Parametricity


       Proof. By induction on B(α).                                                              ◀

          We would like to prove the fundamental theorem by induction over the structure of the
       typing derivation. Since our logical relation is defined for closed terms, we need a closing
       substitution η. We define:

        m ⊩S (x 7→ v) ∈ [x : A] ⇐⇒ m ⊩S v ∈ [A]
        m ⊩S (η1 η2 ) ∈ [Ω1 Ω2 ] ⇐⇒ ∃m1 , m2 . m = m1 · m2 ∧ m1 ⊩S η1 ∈ [Ω1 ] ∧ m1 ⊩S η2 ∈ [Ω2 ]
        m ⊩S (·) ∈ [·]           ⇐⇒ m = ϵ

       Due to the associativity of the monoid operation and concatenation of contexts, this consti-
       tutes a valid definition.

       ▶ Theorem 4 (Fundamental Theorem (purely ordered)). Assume ∆ | Ω ⊢ e : A, a mapping S
       with domain ∆, and closing substitution m ⊩S η ∈ [Ω]. Then m ⊩S η(e) ∈ JAK.

       Proof. By induction on the structure of the given typing derivation. We show a few cases.
       Case:
                                hyp
              ∆|x:A⊢x:A

          Then m ⊩S η(x) ∈ [A] by assumption and definition, and m ⊩S η(x) ∈ JAK since η(x) is
          a value.
       Case:
               ∆ | Ω (x : A) ⊢ e : B
                                        ↠I
              ∆ | Ω ⊢ λx. e : A ↠ B

          m ⊩S η ∈ [Ω]                                                                      Given
          k ⊩S v ∈ [A]                                                            Assumption (1)
          k ⊩S (x 7→ v) ∈ [x : A]                                                    By definition
          m · k ⊩S (η, x 7→ v) ∈ [Ω (x : A)]                                         By definition
          m · k ⊩S (η, x 7→ v)(e) ∈ JBK                                               By ind. hyp.
          m · k ⊩S (η(λx. e)) v ∈ JBK                              By reverse evaluation, v closed
          m ⊩S η(λx. e) ∈ [A ↠ B]                                   By definition, discharging (1)
          m ⊩S η(λx. e) ∈ JA ↠ BK                                                    By definition
       Case:
              ∆ | Ω ⊢ e1 : A ↠ B       ∆ | ΩA ⊢ e 2 : A
                                                          ↠E
                      ∆ | Ω ΩA ⊢ e1 e2 : B

          m ⊩S η ∈ [Ω ΩA ]                                                                  Given
          m1 ⊩S η1 ∈ [Ω] and m2 ⊩S η2 ∈ [ΩA ]
          for some m1 , m2 , η1 , and η2 with m = m1 · m2 and η = η1 η2              By definition
          m1 ⊩S η1 (e1 ) ∈ JA ↠ BK                                                   By ind. hyp.
          m2 ⊩S η2 (e2 ) ∈ JAK                                                       By ind. hyp.
          η1 (e1 ) ,→ v1 with m1 ⊩S v1 ∈ [A ↠ B]                                     By definition
          η2 (e2 ) ,→ v2 with m2 ⊩S v2 ∈ [A]                                         By definition
          m1 · m2 ⊩S v1 v2 ∈ JBK                                                     By definition
          (η1 η2 )(e1 e2 ) = (η1 (e1 )) (η2 (e2 ))                   By properties of substitution
          m ⊩S η(e1 e2 ) ∈ JBK                                 Since m = m1 · m2 and η = (η1 η2 )
C. B. Aberlé and Chris Martens and Frank Pfenning                                                    XX:7


Case:
        ∆, α type | Ω ⊢ e : A
                                ∀I
          ∆ | Ω ⊢ e : ∀α. A

   m ⊩S η ∈ [Ω]                                                                           Given
   RB an arbitrary relation k RB v                                              Assumption (1)
   m ⊩S,α7→RB η ∈ [Ω]                                                              Since α fresh
   m ⊩S,α7→RB η(e) ∈ JAK                                                            By ind. hyp.
   m ⊩S η(e) ∈ J∀α. AK                                            By definition, discharging (1)
Case:
        ∆ | Ω ⊢ e : ∀α.A(α)     ∆ ⊢ B type
                                             ∀E
                ∆ | Ω ⊢ e : A(B)

     m ⊩S η ∈ [Ω]                                                                         Given
     m ⊩S η(e) ∈ J∀α. A(α)K                                                         By ind. hyp.
     Define k RB v iff k ⊩S v ∈ [B]
     m ⊩S,α7→RB η(e) ∈ JA(α)K                                                    By definition
     m ⊩S,α7→RB v ∈ [A(α)] for η(e) ,→ v                                         By definition
     m ⊩S v ∈ [A(B)]                                           By compositionality (Lemma 3)
     m ⊩S η(e) ∈ JA(B)K                                                          By definition
                                                                                             ◀

   Because typing implies that the logical predicate holds, the earlier examples now apply
to well-typed terms.

▶ Theorem 5 ((Theorem 2 revisited)). If

     · ⊢ e : ∀α. α ↠ (α ↠ (α • α))

then e is extensionally equivalent to λx. λy. (x, y).

Proof. We just note that

     ϵ ⊩ e ∈ J∀α. α ↠ (α ↠ (α • α))K

since (·) ∈ [·] and (·)e = e and the empty mapping S suffices without any free type variables.
Then we appeal to the reasoning in Theorem 2.                                              ◀


 5      Unrestricted Functions
We are interested in properties of functions such as list append or list reversal, or higher-order
functions such as fold. This requires inductive types, but the functions on them are not used
linearly. For example, append has a recursive call in the case of a nonempty list, but none
in the case of an empty list. We could introduce a general modality !A for this purpose. A
simpler alternative that is sufficient for our situation is to introduce unrestricted function
types A → B (usually coded as !A ⊸ B in linear logic or !A ↠ B in ordered logic). This
path has been explored previously [30] with different motivations. There, an open logical
relation was defined on the negative monomorphic fragment in order to show the existence
of canonical forms, a property that is largely independent of ordered typing.
XX:8   Substructural Parametricity


           Adding unrestricted functions is rather straightforward in typing by using two kinds of
       variables: those that are ordered and those unrestricted. Then, in the logical predicate,
       unrestricted variables must not use any resources, that is, they are assigned the unit element
       ϵ of the monoid during the definition.
           The generalized judgment has the form ∆ | Γ ; Ω ⊢ e : A where Γ contains type
       assignments for variables that can be used in an unrestricted (not linear and not ordered) way.
       All the previous rules are augmented by propagating Γ from the conclusion to all premises.
       Because our term language is untyped, no extensions are needed there. Similarly, the rules
       of our dynamics do not need to change.


                                                                       hyp
                                            ∆ | Γ, x : A ; · ⊢ x : A

             ∆ | Γ, x : A ; Ω ⊢ e : B                ∆ | Γ ; Ω ⊢ e1 : A → B     ∆ | Γ ; · ⊢ e2 : A
                                         →I                                                          →E
            ∆ | Γ ; Ω ⊢ λx. e : A → B                           ∆ | Γ ; Ω ⊢ e1 e2 : B


          Figure 3 Unrestricted functions

           We extend the logical predicate using arguments not afforded any resources.

            m ⊩ v ∈ [A → B] ⇐⇒           ∀w. ϵ ⊩ w ∈ [A] =⇒ m ⊩ v w ∈ JBK

       The fundamental theorem extends in a straightforward way.
       ▶ Theorem 6 (Fundamental Theorem (mixed ordered/unrestricted)). Assume ∆ | Γ ; Ω ⊢ e : A,
       a mapping S with domain ∆, and two closing substitutions ϵ ⊩S θ ∈ [Γ] and m ⊩S η ∈ [Ω].
       Then m ⊩S (θ ; η)(e) ∈ JAK.
       Proof. By induction on the structure of the given typing derivation.                               ◀

          An interesting side effect of these definitions is that if we omit ordered functions but
       retain pairs we obtain the “usual” formulation closed logical predicates, including certain
       consequences of parametricity for the ordinary λ-calculus.
       ▶ Theorem 7. If

           · ⊢ e : ∀α. α → (α → (α • α))

       then e is extensionally equivalent to one of 4 functions: λx. λy. (x, y), λx. λy. (y, x), λx. λy. (x, x),
       or λx. λy. (y, y).
       Proof. By the fundamental theorem, we have

           ϵ ⊩ e ∈ J∀α. α → (α → (α • α))K

       We use this for an abitrary closed type A with two arbitary values v, and w and relation RA
       with ϵ RA v and ϵ RA w. Exploiting the definition, we get

           ϵ ⊩α7→RA e ∈ Jα → (α → (α • α))K

       Using the definition of function twice and skipping over some evaluation and reverse evaluation,
       we obtain

           ϵ ⊩α7→RA f v w ∈ Jα • αK
C. B. Aberlé and Chris Martens and Frank Pfenning                                                     XX:9


This means that f v w ,→ (u1 , u2 ) with ϵ RA u1 and ϵ RA u2 . Because of the definition of
RA there are 4 possibilities for (u1 , u2 ), namely (v, w), (w, v), (v, v) and (w, w). This in turn
means e is extensionally equal to one of the 4 functions shown.                                  ◀

 6     Unit, Sums, Twist, and Recursive Types
At this point, we are at a crossroads. Because we would like to prove theorems regarding more
complex data structures such as lists, trees, or streams, we could extend the development
with general inductive and coinductive types and their recursors. We conjecture that this
is possible and leave it to future work. The other path is to work with purely positive
types, including recursive ones whose values can be directly observed. In this approach, the
definition of the logical predicate is quite easy to extend. It becomes a nested inductive
definition: either the type becomes smaller or, once we encounter a purely positive type and
recursion is possible, from then on the terms become strictly smaller. In this paper we take
the latter approach, which excludes coinductive types such as streams from consideration,
but still yields many interesting and intuitive consequences.
    We take the opportunity to also round out our language with unit, sums, and twist (the
symmetric counterpart of fuse). We use a signature defining equirecursive type names that
may be arbitrarily mutually recursive. Because such type definitions are otherwise closed,
they constitute metavariables in the sense of contextual modal type theory [24]. Each type
definition F [∆] = A+ must be contractive, that is, its definiens cannot be be another type
name. Moreover, A+ must be purely positive, which is interpreted inductively.

     Types                     A          ::=   . . . | A ◦ B | ⊕{ℓ : Aℓ }ℓ∈L | 1
     Purely Positive Types     A+ , B +   ::=   A+ • B + | A+ ◦ B + | 1 | ⊕{ℓ : A+ℓ }ℓ∈L | F [θ]
     Type Definitions          Σ          ::=   F [∆] = A+ | (·) | Σ1 , Σ2
     Type Substitutions        θ          ::=   α 7→ A+ | (·) | θ1 θ2


The language of expressions does not change much because type names are equirecursive.

     Expression e ::=       ...
                    |       k(e) | match e {ℓ(xℓ ) ⇒ e′ }ℓ∈L     (⊕{ℓ : Aℓ })
                    |       ( ) | match e (( ) ⇒ e′ )            (1)

We add the type A ◦ B (“twist”), symmetric to A • B, since encoding it as B • A requires
rewriting terms, flipping the order of pairs. For A ◦ B it is merely the typechecking that
changes. This allows more types to be assigned to the same term. We allow silent unfolding
of type definitions, so there are no explicit rules for F [θ].
    The logical predicate is also extended in a straightforward manner. We assume the
signature Σ is fixed and therefore do not carry it explicitly through the definitions.

     m ⊩S v ∈ [1]                    ⇐⇒
                                    m = ϵ ∧ v = ()
     m ⊩S v ∈ [A ◦ B]                ⇐⇒
                                    ∃m1 , m2 . m = m2 · m1 ∧ v = (v1 , v2 )
                                    ∧ m1 ⊩S v1 ∈ [A] ∧ m2 ⊩S v2 ∈ [B]
     m ⊩ k(v) ∈ [⊕{ℓ : Aℓ }ℓ∈L ] ⇐⇒ m ⊩S v ∈ [Ak ] ∧ k ∈ L
        S

     m ⊩S v ∈ [F [θ]]            ⇐⇒ m ⊩S v ∈ θ(A+ ) where F [∆] = A+ ∈ Σ

    Because we have equirecursive type definitions, the last clause is usually applied silently.
The definition of the logical predicate is no longer straightforwardly inductive on the structure
of the type. However, we see that for purely positive types (the only ones involved in recursion),
XX:10   Substructural Parametricity



                                 ∆ | Γ ; ΩA ⊢ e1 : A ∆ | Γ ; ΩB ⊢ e2 : B
                                                                                  ◦I
                                        ∆ | Γ ; ΩB ΩA ⊢ (e1 , e2 ) : A ◦ B

                     ∆|Γ;Ω⊢e:A◦B                 ∆ | Γ ; ΩL (y : B) (x : A) ΩR ⊢ e′ : C
                                                                                           ◦E
                               ∆ | Γ ; ΩL Ω ΩR ⊢ match e ((x, y) ⇒ e′ ) : C

                                               ∆|Γ;Ω⊢e:A◦B                ∆ | Γ ; ΩL ΩR ⊢ e′ : C
                                   1I                                                              1E
              ∆ | Γ ; · ⊢ () : 1                ∆ | Γ ; ΩL Ω ΩR ⊢ match e (( ) ⇒ e′ ) : C

                                          (k ∈ L)    ∆ | Γ ; Ω ⊢ e : Ak
                                                                             ⊕I
                                        ∆ | Γ ; Ω ⊢ k(e) : ⊕{ℓ : Aℓ }ℓ∈L

            ∆ | Γ ; Ω ⊢ e : ⊕{ℓ : Aℓ }ℓ∈L       (∆ | Γ ; ΩL (xℓ : Aℓ ) ΩR ⊢ eℓ : Aℓ )    (∀ℓ ∈ L)
                                                                                                    ⊕E
                           ∆ | Γ ; ΩL Ω ΩR ⊢ match e {ℓ(xℓ ) ⇒ eℓ }ℓ∈L : C


           Figure 4 Ordered Natural Deduction, Extended


                                            e ,→ ( ) e′ ,→ v ′
                  ( ) ,→ ( )            match e (( ) ⇒ e′ ) ,→ v ′

               e ,→ v                    e ,→ k(v)    [v/xk ]ek ,→ v ′
            k(e) ,→ k(v)            match e {ℓ(xℓ ) ⇒ eℓ }ℓ∈L ,→ v ′


           Figure 5 Big-Step Operational Semantics, Extended


        the value in the definition becomes strictly smaller in each clause if type definitions are
        contractive. In other words, we now have a nested inductive definition of the logical predicate,
        first on the type, and when the type is purely positive, on the structure of the value.
            We can also add recursion to our expression language with the key proviso that we
        either restrict ourselves to certain patterns of recursion (for example, primitive recursion),
        or termination is guaranteed by other external means (for example, using an analysis using
        sized types [1]). This assumption allows us to maintain the structure of the logical predicate,
        even if it is no longer a means to prove termination (which we are not interested in for this
        paper).

        ▶ Lemma 8 (Compositionality (including purely positive equirecursive types)). Define RA such
        that k RA w iff k ⊩ w ∈ [A]. Then m ⊩S,α7→RA v ∈ [B(α)] iff m ⊩S v ∈ [B(A)].

        Proof. By nested induction on the definition of the logical predicate for B(α), first on the
        structure of B and second on the structure of the value when a purely positive type F [θ] has
        been reached.                                                                              ◀

        ▶ Theorem 9 (Fundamental Theorem (including purely positive recursive types)). Assume
        ∆ | Γ ; Ω ⊢ e : A, a mapping S with domain ∆, and two closing substitutions ϵ ⊩S θ ∈ [Γ]
        and m ⊩S η ∈ [Ω]. Then m ⊩S (θ ; η)(e) ∈ JAK.
C. B. Aberlé and Chris Martens and Frank Pfenning                                                                       XX:11


Proof. By induction on the structure of the given typing derivation. When reasoning about
functions and recursion, we need the assumption of termination.                        ◀

 7       Free Theorems for Ordered Lists
We start with some theorems about ordered lists, not unlike those analyzed by Wadler [38],
but much sharper due to substructural typing. We define two versions of ordered lists, one
that is ordered left-to-right and one that is ordered right-to-left. Both of these use exactly
the same representation; just their typing is different.
  llist α = ⊕{nil : 1, cons : α • llist α}
  rlist α = ⊕{nil : 1, cons : α ◦ rlist α}
The following will be a useful lemma about ordered lists.
▶ Lemma 10 (Ordered Lists).

      m ⊩S v ∈ [llist α]       ⇐⇒      m = ϵ ∧ v = nil ( )
                                       ∨ ∃m1 , m2 . m = m1 · m2 ∧ v = cons (v1 , v2 )
                                         ∧ m1 S(α) v1 ∧ m2 ⊩ v2 ∈ [llist α]

      m ⊩S v ∈ [rlist α] ⇐⇒            m = ϵ ∧ v = nil ( )
                                       ∨ ∃m1 , m2 . m = m2 · m1 ∧ v = cons (v1 , v2 )
                                         ∧ m1 S(α) v1 ∧ m2 ⊩ v2 ∈ [rlist α]

Proof. By unrolling the definitions of the logical predicate and the equirecursive nature of
the definition of lists.                                                                  ◀

     For the applications, we abbreviate lists, writing [v1 , . . . , vn ] for cons(v1 , . . . , cons(vn , nil ( ))).

 m ⊩α7→RA v ∈ [llist α] ⇐⇒ m = m1 · · · mn , v = [v1 , . . . , vn ] where mi RA vi (for some mi , vi )

 m ⊩α7→RA v ∈ [rlist α] ⇐⇒ m = mn · · · m1 , v = [v1 , . . . , vn ] where mi RA vi (for some mi , vi )

    Now we state a first property of lists that follows as a consequence of our parameterized
logical predicate.
▶ Theorem 11. If · ⊢ f : ∀α. llist α ↠ llist α then f is extensionally equal to the identity
function on lists.
Proof. By the fundamental theorem, we have

     ϵ ⊩ f ∈ [∀α. llist α ↠ llist α]

To construct a relation RA we pick an arbitary closed type A. For the monoid, we pick the
one freely generated by a1 , a2 , . . . and define

     m RA v ⇐⇒ m = ai ∧ v = vi

for arbitrary elements vi . By definition, we obtain

     ϵ ⊩S f ∈ [llist α ↠ llist α]

Again by definition, that’s the case iff

     ∀m, v. m ⊩S v ∈ [llist α] =⇒ ϵ · m ⊩S f v ∈ Jllist αK
XX:12   Substructural Parametricity


        Here, ϵ · m = m, by the monoid laws. Therefore f v ,→ w and
           ∀m, v. m ⊩S v ∈ [llist α] =⇒ m ⊩S w ∈ [llist α]
        We use this for m = a1 · · · an and v = [v1 , . . . , vn ]. By our lemma about lists and the arbitrary
        nature of A and vi we conclude that w = v.                                                          ◀

           By similar reasoning we can obtain the following properties.
        ▶ Theorem 12.
        1. If f : ∀α.rlist α ↠ rlist α then f is extensionally equal to the identity function.
        2. If f : ∀α.rlist α ↠ llist α then f is extensionally equal to the list reversal function.
        3. If f : ∀α.llist α ↠ rlist α then f is extensionally equal to the list reversal function.
        Proof. By very similar reasoning to the one in Theorem 11.                                         ◀

           But can we deduce properties of higher-order functions using ordered parametricity? We
        show one primary example; others such as map follow directly from it or similarly.
           Unlike the usual or even linear parametricity, the type of fold guarantees that it must
        be the fold function! Note that the combining function and initial element are unrestricted
        arguments (one is called for every list element, and one is called only for the empty list), but
        that the combining function’s arguments are ordered.
        ▶ Theorem 13. If
           · ⊢ f : ∀α. ∀β. (α • β ↠ β) → β → llist α ↠ β
        then f extensionally equal to the fold function, that is,
           f g b [v1 , v2 , . . . , vn ] = g(v1 , g(v2 , . . . , g(vn , b)))
        Proof. We use the free monoid over constructors a1 , a2 , . . .. Furthermore, given a type A
        with arbitrary elements vi we define the relation RA by
           m RA v ⇐⇒ m = ai ∧ v = vi for some i
        Since the type involves another quantified type β, we need to define a second relation RB
        where
           m RB d ⇐⇒ m = ai1 · · · aik ∧ d = g(vi1 , g(vi2 , . . . , g(vik , b)))
        With these relations and the definition on of the logical predicate we get the following two
        properties.
        1. ∀m1 , m2 , v, d. m1 RA v ∧ m2 RB d =⇒ m1 · m2 RB g(v, d)
        2. ϵ RB g
        Since
           a1 · · · an ⊩α7→RA [v1 , . . . , vn ] ∈ [llist α]
        we can use the second and iterate the first property to conclude that
           a1 · · · an RB w          for f g b [v1 , . . . , vn ] ,→ w
        By definition of RB , this yields
           f g b [v1 , . . . , vn ] = g(v1 , . . . g(vn , b))
        in the sense that both sides evaluate to w. Because functions and values were chosen
        arbitrarily, this expresses the desired extensional equality.                      ◀
C. B. Aberlé and Chris Martens and Frank Pfenning                                                     XX:13


 8      Free Theorems Regarding Trees
Consider

  lxrtree α = ⊕{leaf : 1, cons : lxrtree α • α • lxrtree α}
  xlrtree α = ⊕{leaf : 1, cons : (xlrtree α ◦ α) • xlrtree α}
  lrxtree α = ⊕{leaf : 1, cons : lrxtree α • (α ◦ xlrtree α)}

     Here are a few free theorems regarding such trees. Further variations exist.

▶ Theorem 14.
1. If f : ∀α. lxrtree α ↠ llist α then f t lists the elements of t following an inorder traversal.
2. If f : ∀α. xlrtree α ↠ llist α then f t lists the elements of t following a preorder traversal.
3. If f : ∀α. lrxtree α ↠ llist α then f t lists the elements of t following a postorder traversal.

Proof. Trees, like lists, are purely positive types. As such, we can prove an analogue of
Lemma 10. We only show one of them, writing t for tree values.

 m ⊩S t ∈ [lxrtree α] ⇐⇒        m = ϵ ∧ t = leaf( )
                                ∨ ∃m1 , k, m2 . m = m1 · k · m2 ∧ v = node(t1 , v, t2 )
                                  ∧ m1 ⊩S t1 ∈ [lxrtree α] ∧ k S(α) v ∧ m2 ⊩S t2 ∈ [lxrtree α]

                                                                                                ◀

 9      From Ordered to Linear Types
Exploring parametricity for linear types instead of ordered ones is now a rather straightforward
change. We conflate the left and right implication into a single implication, and similarly for
conjunction.

      ordered      linear      structural    values
      B/A
                   A⊸B         A→B           λx. e
      A↣B
      A•B
                   A⊗B         A×B           (v1 , v2 )
      A◦B
      1            1          1              ()
      ⊕{ℓ : Aℓ }   ⊕{ℓ : Aℓ } ⊕{ℓ : Aℓ }     ℓ(v)

We see that in the transition from the linear to the structural case, no further connectives
collapse. That’s because we would still distinguish eager pairs (A × B) from lazy records
that we have elided from our development since they do not introduce any fundamentally
new ideas.
    From the point of view of typing, the easiest change is to just permit the silent rule of
exchange

     ∆ | Γ ; ΩL (y : B) (x : A) ΩR ⊢ e : C
                                             exchange
     ∆ | Γ ; ΩL (x : A) (y : B) ΩR ⊢ e : C

The more typical change is to replace context concatenation ΩL ΩR with context merge
ΩL ▷◁ ΩR which allows arbitrary interleavings of the hypotheses.
XX:14   Substructural Parametricity


            Our definition of the logical predicates remains that same, except that we assume that the
        algebraic structure parameterizing our definitions is a commutative monoid. This immediately
        validates the rules of exchange and the fundamental theorem goes through as before.
            The results of exploiting the fundamental theorem to obtain parametricity results are no
        longer as sharp. For example:
        ▶ Theorem 15. If · ⊢ e : ∀α. α ⊸ α ⊸ α ⊗ α then f is extensionally equal to λx. λy. (x, y)
        or λx. λy. (y, x).
        Proof. By the fundamental theorem, we have
             ϵ ⊩ e ∈ J∀α. α ⊸ α ⊸ α ⊗ αK
        Therefore e ,→ f and
             ϵ ⊩ f ∈ [∀α. α ⊸ α ⊸ α ⊗ α]
        We use a free commutative monoid with two generators, a and b, arbitrary values v and w
        such that a R v and b R w. By the fundamental theorem:
             ϵ ⊩α7→R f ∈ [α ⊸ α ⊸ α ⊗ α]
        Applying this function to v and w, we obtain that f v w ,→ p and
             a · b ⊩α7→R p ∈ [α ⊗ α]
        This is true, again by definition, if for some m and k and p1 and p2 we have
             m · k = a · b ∧ p = (p1 , p2 ) ∧ m ⊩α7→R p1 ∈ [α] ∧ k ⊩α7→R p2 ∈ [α]
        Further applying definitions, we get that for some m, k, p1 , and p2 , we have
             m · k = a · b ∧ m R p1 ∧ k R p2
        There are 4 ways that a · b could be decomposed into m · k, but the definition of R leaves
        only two possibilities: m = a, k = b, p1 = v and p2 = w or m = b, k = a, p1 = w and p2 = v.
        Summarizing: either
             e v w ,→ (v, w)
        or
             e v w ,→ (w, v)
        which expresses that e is extensionally equal to λx. λy. (x, y) or λx. λy. (y, x).          ◀

        ▶ Theorem 16. If · ⊢ e : ∀α.list α ⊸ list α then e is extensionally equal to a permutation of
        the list elements.
        Proof. As in the proof of the related ordered theorem, we apply the fundamental theorem and
        then the definition for arbitrary values vi with ai R vi where α 7→ R, and the commutative
        monoid is freely generated from a1 , a2 , . . ..
           Taking analogous steps to the ordered case, we conclude that a1 · · · an = m1 · · · mn
        modulo commutative (and associativity, as always) where each mi is a unique aj .          ◀

            In the unrestricted case where various algebraic elements are fixed to be ϵ, we can only
        obtain that every element of the output list must be a member of the input list, because those
        elements are in ϵ R vi . We do not write out the details of this straightforward adaptation of
        foregoing proofs.
C. B. Aberlé and Chris Martens and Frank Pfenning                                                  XX:15


 10     Related Work

The most directly related work is Zhao et al.’s [40] open logical relation for parametricity
for a dual intuitionistic-linear polymorphic lambda calculus. In this work, they define an
open logical relation that includes an analog of typing contexts in the semantic model. While
our development follows a similar structure, our resource algebraic account allows us to
eliminate spurious typechecking premises in definitions and permits a more flexible range of
substructural type systems.
    Ahmed, Fluet, and Morrisett [3] introduce a logical relation for substructural state via
step-indexing, followed by [4] a linear language with locations (L3) defined by a Kripke-style
logical relation to account for a language with mutable storage. However, the underlying
languages in these developments do not support parametric polymorphism. Ahmed, Dreyer,
and Rossberg later provide a logical relations account of a System F-based language supporting
imperative state update, and they demonstrate representation independence results for this
system [2]. The languages modeled in this body of work represent a specific point in the
design space with respect to imperative state update and references, as opposed to our more
general schema for substructural types in a functional setting. However, Kripke-style logical
relations that model a store as a partial commutative monoid have some parallels to our
development, and drawing out a more precise relationship between these systems represents
an interesting path of future work.
    Finally, there are a few developments that start from different settings but develop
semantics with similar properties. Pérez et al. develop logical relations for linear session
types [26, 27] to establish normalization results, but there is no account of parametricity. The
Iris system for program reasoning via higher-order separation logic incorporates a semantic
model initially based on monoids [14], which is later extended to more general resource
algebras [13]. Their parameterization over resource algebras seems to work similarly to ours,
but towards the goal of program verification rather than type-based reasoning. The use
of “resource semantics” more generally to account for the semantics of substructural logics
extends at least to Kamide [16] and the logic of bunched implications [25], and similar ideas
have recently gained traction in the context of graded modal type systems [37].




 11     Conclusion

We have provided an account of substructural parametricity including ordered, linear, and
unrestricted disciplines. The fewer structural properties are supported, the more precise
the characterization of a function’s behavior from its type. We have also implemented an
ordered type checker using a bidirectional type system with so-called additive contexts [5],
but the details are beyond the scope of this paper. Suffice it to say that all the functions
such as append, reverse, tree traversals, and fold can actually be implemented in a variety of
ways and are therefore not vacuous theorems.
    The most immediate item of future work is to support general inductive and coinductive
types instead of purely positive recursive types. This would allow a new class of applications,
including (productive) stream processing and object-oriented program patterns. We also
envision an adjoint combination of different substructural type systems [12], extended to
include exchange among the explicit structural rules.
XX:16   Substructural Parametricity


             References
         1   Andreas Abel and Brigitte Pientka. Well-founded recursion with copatterns and sized types.
             Journal of Functional Programming, 26:e2, 2016.
         2   Amal Ahmed, Derek Dreyer, and Andreas Rossberg. State-dependent representation indepen-
             dence. SIGPLAN Not., 44(1):340–353, January 2009. doi:10.1145/1594834.1480925.
         3   Amal Ahmed, Matthew Fluet, and Greg Morrisett. A step-indexed model of substructural
             state. In Proceedings of the tenth ACM SIGPLAN international conference on Functional
             programming, pages 78–91, 2005.
         4   Amal Ahmed, Matthew Fluet, and Greg Morrisett. Lˆ 3: a linear language with locations.
             Fundamenta Informaticae, 77(4):397–449, 2007.
         5   Robert Atkey. Syntax and semantics of quantitative type theory. In Anuj Dawar and Erich
             Grädel, editors, 33rd Conference on Logic in Computer Science (LICS 2018), pages 56–65,
             Oxford, UK, July 2018. ACM.
         6   P. N. Benton. A mixed linear and non-linear logic: Proofs, terms and models. In Leszek
             Pacholski and Jerzy Tiuryn, editors, Selected Papers from the 8th International Workshop
             on Computer Science Logic (CSL’94), pages 121–135, Kazimierz, Poland, September 1994.
             Springer LNCS 933. An extended version appears as Technical Report UCAM-CL-TR-352,
             University of Cambridge.
         7   Luís Caires and Frank Pfenning. Session types as intuitionistic linear propositions. In
             Proceedings of the 21st International Conference on Concurrency Theory (CONCUR 2010),
             pages 222–236, Paris, France, August 2010. Springer LNCS 6269.
         8   Peng Fu, Kohei Kishida, and Peter Selinger. Linear dependent type theory for quantum
             programming languages. In 34th Symposium on Logic in Computer Science (LICS 2020),
             pages 440–453, Saarbrücken, Germany, July 2020. ACM.
         9   Simon J. Gay and Vasco T. Vasconcelos. Linear type theory for asynchronous session types.
             Journal of Functional Programming, 20(1):19–50, January 2010.
        10   Aïna Linn Georges, Benjamin Peters, Laila Albeheiry, Leo White, Stephan Dolan, Richard A.
             Eisenberg, Chris Casinghino, François Pottier, and Derek Dreyer. Data race freedom à la
             mode. In Principles of Programming Languages (POPL 2025), volume 9 of Proceedings on
             Programming Languages, pages 656–686. ACM, January 2025.
        11   Jean-Yves Girard and Yves Lafont. Linear logic and lazy computation. In H. Ehrig, R. Kowalski,
             G. Levi, and U. Montanari, editors, Proceedings of the International Joint Conference on
             Theory and Practice of Software Development, volume 2, pages 52–66, Pisa, Italy, March 1987.
             Springer-Verlag LNCS 250.
        12   Junyoung Jang, Sophia Roshal, Frank Pfenning, and Brigitte Pientka. Adjoint natural
             deduction. In Jakob Rehof, editor, 9th International Conference on Formal Structures for
             Computation and Deduction (FSCD 2024), pages 15:1–15:23, Tallinn, Estonia, July 2024.
             LIPIcs 299. Extended version available as https://arxiv.org/abs/2402.01428.
        13   Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Aleš Bizjak, Lars Birkedal, and Derek
             Dreyer. Iris from the ground up: A modular foundation for higher-order concurrent separation
             logic. Journal of Functional Programming, 28:e20, 2018.
        14   Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal,
             and Derek Dreyer. Iris: Monoids and invariants as an orthogonal basis for concurrent reasoning.
             ACM SIGPLAN Notices, 50(1):637–650, 2015.
        15   Gilles Kahn. Natural semantics. In Proceedings of the Symposium on Theoretical Aspects of
             Computer Science, pages 22–39. Springer-Verlag LNCS 247, 1987.
        16   Norihiro Kamide. Kripke semantics for modal substructural logics. Journal of Logic, Language
             and Information, 11:453–470, 2002.
        17   Max Kanovich, Stepan Kuznetsov, Vivek Nigam, and Andre Scedrov. A logical framework
             with commutative and non-commutative subexponentials. In International Joint Conference
             on Automated Reasoning (IJCAR 2018), pages 228–245. Springer LNAI 10900, 2018.
C. B. Aberlé and Chris Martens and Frank Pfenning                                                      XX:17


18   Joachim Lambek. The mathematics of sentence structure. The American Mathematical
     Monthly, 65(3):154–170, 1958.
19   Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon
     Howell, Bryan Parno, and Chris Hawblitzel. Verus: Verifying Rust programs using linear ghost
     types. In Proceedings of the ACM on Programming Languages, volume 7 (OOPSLA 2023), pages
     286–315, April 2023. Extended version available as https://arxiv.org/abs/2303.05491.
20   Anton Lorenzen, Daan Leijen, and Wouter Swierstra. FP2 : Fully in-place functional program-
     ming. In International Conference on Functional Programming (ICFP 2023), Proceedings on
     Programming Languages, pages 275–304. ACM, August 2023.
21   Anton Lorenzen, Daan Leijen, Wouter Swierstra, and Sam Lindley. The functional essense of
     imperative binary search trees. In Programming Language Design and Implementation (PLDI
     2024), volume 8 of Proceedings on Programming Languages, pages 518–542. ACM, January
     2024.
22   Wendy MacCaull. Relational semantics and a relational proof system for full Lambek calculus.
     Journal of Symbolic Logic, 63(2):623–637, 1998.
23   John C Mitchell. Representation independence and data abstraction. In Proceedings of the
     13th ACM SIGACT-SIGPLAN symposium on Principles of programming languages, pages
     263–276, 1986.
24   Aleksandar Nanevski, Frank Pfenning, and Brigitte Pientka. Contextual modal type theory.
     Transactions on Computational Logic, 9(3), 2008.
25   Peter W O’Hearn and David J Pym. The logic of bunched implications. Bulletin of Symbolic
     Logic, 5(2):215–244, 1999.
26   Jorge A. Pérez, Luís Caires, Frank Pfenning, and Bernardo Toninho. Termination in session-
     based concurrency via linear logical relations. In H. Seidl, editor, 22nd European Symposium
     on Programming, ESOP’12, pages 539–558, Tallinn, Estonia, March 2012. Springer LNCS
     7211.
27   Jorge A. Pérez, Luís Caires, Frank Pfenning, and Bernardo Toninho. Linear logical relations
     and observational equivalences for session-based concurrency. Information and Computation,
     239:254–302, 2014.
28   Frank Pfenning and Klaas Pruiksma. Relating message passing and shared memory, proof-
     theoretically. In S. Jongmans and A. Lopes, editors, 25th International Conference on
     Coordination Models and Languages (COORDINATION 2023), pages 3–27, Lisbon, Portugal,
     June 2023. Springer LNCS 13908. Notes to an invited talk.
29   Jeff Polakow. Ordered Linear Logic and Applications. PhD thesis, Department of Computer
     Science, Carnegie Mellon University, August 2001.
30   Jeff Polakow and Frank Pfenning. Natural deduction for intuitionistic non-commutative
     linear logic. In J.-Y. Girard, editor, Proceedings of the 4th International Conference on Typed
     Lambda Calculi and Applications (TLCA’99), pages 295–309, L’Aquila, Italy, April 1999.
     Springer-Verlag LNCS 1581.
31   Klaas Pruiksma, William Chargin, Frank Pfenning, and Jason Reed. Adjoint logic and its
     concurrent operational interpretation. Unpublished manuscript, January 2018.
32   Jason Reed. Hybridizing a logical framework. In Proceedings of the International Workshop
     on Hybrid Logic (HyLo’06), pages 135–148. Electronic Notes in Theoretical Computer Science,
     v.174(6), 2007.
33   Jason Reed and Frank Pfenning. A constructive approach to the resource semantics of
     substructural logics. Unpublished Manuscript, May 2010. URL: https://www.cs.cmu.edu/
     ~jcreed/papers/rp-substruct.pdf.
34   Jason C. Reed. A Hybrid Logical Framework. PhD thesis, Carnegie Mellon University,
     September 2009. Available as Technical Report CMU-CS-09-155.
35   John C. Reynolds. Types, abstraction, and parametric polymorphism. In R.E.A. Mason,
     editor, Information Processing 83, pages 513–523. Elsevier, September 1983.
XX:18   Substructural Parametricity


        36   Christopher Strachey. Fundamental concepts in programming languages. Higher-Order and
             Symbolic Computation, 13:11–49, 2000. Notes for lecture course given at the International
             Summer School in Computer Programming at Copenhagen, Denmark, August 1967.
        37   Victoria Vollmer, Danielle Marshall, and Harley Eades, III. A mixed linear and graded logic:
             Proofs, terms, and models. In 33rd Conference on Computer Science Logic (CSL 2025), pages
             32:1–32:21, Amsterdam, The Netherlands, February 2025. LIPIcs 326.
        38   Philip Wadler. Theorems for free! In J. Stoy, editor, Proceedings of the 4th International
             Conference on Functional Programming Languages and Computer Architecture (FPCA’89),
             pages 347–359, London, UK, September 1989. ACM.
        39   Jianzhou Zhao, Qi Zhang, and Steve Zdancewic. Relational parametricity for a polymorphic
             linear lambda calculus. In K. Ueda, editor, 8th Asian Symposium on Programming Languages
             and Systems (APLAS 2010), pages 344–359. Springer LNCS 6461, 2010.
        40   Jianzhou Zhao, Qi Zhang, and Steve Zdancewic. Relational parametricity for a polymorphic
             linear lambda calculus. In Programming Languages and Systems: 8th Asian Symposium,
             APLAS 2010, Shanghai, China, November 28-December 1, 2010. Proceedings 8, pages 344–359.
             Springer, 2010.
