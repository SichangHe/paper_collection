                                         A Cyclic Proof System for HFLN
                                         Mayuko Kori
                                         Department of Informatics, The Graduate University for Advanced Studies (SOKENDAI), Hayama,
                                         Japan
                                         National Institute of Informatics, Tokyo, Japan
                                         mkori@nii.ac.jp

                                         Takeshi Tsukada
                                         Graduate School of Science, Chiba University, Chiba, Japan
                                         tsukada@math.s.chiba-u.ac.jp

                                         Naoki Kobayashi
                                         The University of Tokyo, Tokyo, Japan
                                         koba@is.s.u-tokyo.ac.jp

                                               Abstract
arXiv:2010.14891v3 [cs.LO] 12 Aug 2021




                                         A cyclic proof system allows us to perform inductive reasoning without explicit inductions. We
                                         propose a cyclic proof system for HFLN , which is a higher-order predicate logic with natural numbers
                                         and alternating fixed-points. Ours is the first cyclic proof system for a higher-order logic, to our
                                         knowledge. Due to the presence of higher-order predicates and alternating fixed-points, our cyclic
                                         proof system requires a more delicate global condition on cyclic proofs than the original system of
                                         Brotherston and Simpson. We prove the decidability of checking the global condition and soundness
                                         of this system, and also prove a restricted form of standard completeness for an infinitary variant
                                         of our cyclic proof system. A potential application of our cyclic proof system is semi-automated
                                         verification of higher-order programs, based on Kobayashi et al.’s recent work on reductions from
                                         program verification to HFLN validity checking.

                                         2012 ACM Subject Classification Theory of computation → Proof theory

                                         Keywords and phrases Cyclic proof, higher-order logic, fixed-point logic, sequent calculus


                                         Acknowledgements We would like to thank anonymous referees for useful comments. This work
                                         was supported by JSPS KAKENHI Grant Number JP15H05706, JP20H00577, and JP20H05703. We
                                         also acknowledge Dominik Wehr for pointing out a gap in Section 3. The first author is supported
                                         by ERATO HASUO Metamathematics for Systems Design Project (No. JPMJER1603), JST.


                                          1     Introduction

                                         There have recently been extensive studies on cyclic proof systems. They allow a proof to
                                         be cyclic, as long as it satisfies a certain sanity condition called the “global trace condition.”
                                         Cyclic proofs enable inductive reasoning without explicit inductions, which would be useful
                                         for proof automation. Various cyclic proof systems have been proposed [3, 7, 12] for first-order
                                         logics, and some of them have been applied to automated program verification [1, 2, 13].
                                             In the present paper, we propose a cyclic proof system for HFLN , a higher-order logic
                                         with natural numbers and least/greatest fixpoint operators on higher-order predicates. HFLN
                                         has been introduced by Kobayashi et al. [9, 10] as an extension of HFL [15], and shown to
                                         be useful for higher-order program verification. Verification of various temporal properties of
                                         higher-order programs can naturally be reduced to validity checking for HFLN formulas. For
                                         example, consider the following OCaml program:

                                         let rec g n = if n=0 then () else g (n-1) in
                                         let rec f h m = h m; f h (m+1) in f g 0
                                                          Leibniz International Proceedings in Informatics
                                                          Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
2


    The property “f is infinitely often called” is then expressed as the following formula:
                                                                                 
          νF.λh.λm.h m ∧ F h (m + 1)          µG.λn.(n = 0 ∨ (n 6= 0 ∧ G (n − 1))) 0.

    Here, νF.λh. · · · and µG.λn. · · · respectively represent the greatest and least predicates such
    that F = λh. · · · and G = λn. · · ·. Notice the close correspondence between the program and
    the formula: the functions f and g correspond to the predicates F and G, and function calls
    correspond to applications of the predicates; an interested reader may wish to consult [9, 10]
    to learn how program verification problems can be translated to HFLN formulas. Our cyclic
    proof system for HFLN presented in this paper would, therefore, be useful for semi-automated
    verification of higher-order programs.
        A key issue in the design of our cyclic proof system is how to formalize a decidable “global
    trace condition,” to guarantee the soundness of cyclic proofs in the presence of higher-order
    predicates and alternating fixed-points. Our global trace condition has been inspired by,
    and is actually very similar to that of Doumane [7]. The decidability of our global trace
    condition is, however, non-trivial, due to the presence of higher-order predicates. Inspired by
    the approach of Brotherston and Simpson [3], we reduce the global trace condition to the
    containment problem for Büchi automata.
        We also consider an infinitary version of our proof system, and prove that the infinitary
    proof system is complete for sequents without higher-order variables. The restriction to
    sequents without higher-order variables is sufficient for the aforementioned application of our
    proof system to higher-order program verification.
        The rest of this paper is structured as follows. Section 2 reviews the syntax and semantics
    of HFLN . Section 3 defines our cyclic proof system. Sections 4 and 5 respectively prove
    the decidability of the global trace condition and the soundness of our cyclic proof system.
    Section 6 discusses the restricted form of completeness of the infinitary variant of our proof
    system. Section 7 discusses related work, and Section 8 concludes the paper.

     2      HFLN : Higher-Order Fixed-Point Arithmetic
    This section introduces the target logic HFLN , which is a higher-order logic with natural
    numbers and alternating fixed-points. It has been introduced by Kobayashi et al. [10, 16] as
    an extension of higher-order modal fixed-point logic (HFL) [15].

    2.1     Syntax of HFLN
    HFLN is simply typed. The syntax of types is given as follows:

         A ::= N | T            T ::= Ω | A → T.

    N is the type of natural numbers, Ω is the type of propositions and A → T is a function type.
    Occurrences of N are restricted to argument positions for a technical reason (see below).
       Let V be a countably infinite set of variables, ranged over by x, y, z, f, X, Y, Z, . . .. The
    syntax of terms and formulas is given by:

         term           s, t   ::=   x | Z | St
         formula       ϕ, ψ    ::=   s = t | ϕ ∨ ψ | ϕ ∧ ψ | x | λxA .ϕ | ϕ ψ | ϕ t | µxT .ϕ | νxT .ϕ.

    We shall often omit the type annotations. The syntax of terms is standard: Z represents
    zero and S is the successor function. A closed term must be of the form Sn Z, which is often
M. Kori, T. Tsukada and N. Kobayashi                                                                         3


identified with the natural number n. Constructors of formulas are logical ones (s = t, ϕ ∨ ψ
and ϕ ∧ ψ), those from the λ-calculus (variable x, abstraction λx.ϕ, and application ϕ ψ
and ϕ t), and fixed-point operators (least fixed-point µx.ϕ and greatest fixed-point νx.ϕ).
Some standard constructs such as summation t1 + t2 = s, multiplication t1 × t2 = s, truth >
and quantifiers ∀ and ∃ are definable; see examples later in this subsection. The set of free
variables is defined as usual; the binders are λx, µx and νx.
    A sequent is a pair (Γ, ∆) of finite sequences of formulas, written as Γ ` ∆. For a finite
sequence Γ of formulas, FV (Γ) denotes the union of the sets of free variables of formulas in
Γ. The free variables of a sequent Γ ` ∆ is FV (Γ) ∪ FV (∆).
    The type system is presented in Figure 1. Here H is a type environment, which is a map
from a finite subset of variables to the set of types. The typing rules should be easy to
understand. The types of fixed-point formulas µx.ϕ and νy.ψ, as well as the types of the
variables x and y, are restricted to T (i.e., they cannot be N). A formula ϕ is well-typed if
H ` ϕ : T for some H and T . In the sequel, we shall consider only well-typed formulas.
    For a sequent Γ ` ∆, we write H | Γ ` ∆ if H ` ϕ : Ω for every ϕ in Γ or ∆. A sequent
is well-typed if H | Γ ` ∆ for some H.
    We give some examples of formulas and explain their intuitive meaning.

I Example 1. The truth > and falsity ⊥ can be defined as fixed-points:

     > := νxΩ .x          and       ⊥ := µxΩ .x.

The former means that > is the greatest element in the set of truth values (i.e. elements
in the semantic domain of Ω) such that x = x. Similarly ⊥ is the least truth value. The
greatest >T and least ⊥T value of type T are defined in a similar way.                 J

I Example 2. The quantifiers over natural numbers are definable. Let forall be a predicate
of type (N → Ω) → N → Ω defined by

     forall    :=    νX.λpN→Ω .λxN .p x ∧ X p (S x).

Then forall ϕ n holds if and only if ϕ m holds for every m ≥ n. To see this, notice that
(forall ϕ n) = (ϕ n) ∧ (forall ϕ (n + 1)) since forall is a fixed-point. By iteratively applying
this equation, we have

     (forall ϕ n)    =     (ϕ n) ∧ (ϕ (n + 1)) ∧ (ϕ (n + 2)) ∧ · · ·

and thus forall ϕ n if and only if ∀m ≥ n.ϕ m.1 Then the universal quantifier over natural
numbers is defined by

     ∀x.ϕ     :=     forall (λx.ϕ) Z.

The existential quantifier can be defined similarly. A direct definition is
                                           
   ∃xN .ϕ :=        µY N→Ω .λx.ϕ ∨ Y (Sx) Z.

The quantifiers over T are easier because of monotonicity (see next subsection); we define
∀xT .ϕ := (λx.ϕ) ⊥T and ∃xT .ϕ := (λx.ϕ) >T .                                           J

1
    The reader may notice that this intuitive argument does not explain why we should use ν instead of µ.
    Here we skip this subtle issue. An interested reader may compare the interpretations of forall and its
    µ-variant, following the definition in the next subsection.
                    Leibniz International Proceedings in Informatics
                    Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
4


    For terms:
                                                                      H`t:N
                         H, x : A ` x : A          H`Z:N              H ` St : N
    For formulas:
                                        H`s:N H`t:N
                                          H`s=t:Ω
                       H`ϕ:Ω  H`ψ:Ω                        H`ϕ:Ω  H`ψ:Ω
                         H`ϕ∨ψ :Ω                            H`ϕ∧ψ :Ω
                        H, x : A ` ϕ : T           H ` ϕ : T0 → T     H ` ψ : T0
                       H ` λxA .ϕ : A → T                   H ` ϕψ : T

                                     H`ϕ:N→T         H`t:N
                                          H ` ϕt : T
                                H, x : T ` ϕ : T           H, x : T ` ϕ : T
                                H ` µxT .ϕ : T             H ` νxT .ϕ : T

       Figure 1 Typing Rules for HFLN .


    I Example 3. Let sum be the summation, i.e. the predicate such that sum n m k holds if
    and only if n + m = k. This predicate can be defined as follows:

       µsum. λxN .λy N .λz N .(x = Z ∧ y = z) ∨ (∃x0 .∃z 0 .x = Sx0 ∧ sum x0 y z 0 ∧ z = Sz 0 ).

    This formula represents the standard inductive definition of the summation: Z + y = y and
    x0 + y = z 0 =⇒ Sx0 + y = Sz 0 . One can define the multiplication in a similar way, representing
    the standard inductive definition of the multiplication using sum.                             J

    I Example 4. The inequality s < t on terms is also definable. The idea is to appeal to the
    following fact: if n < m, then n + 1 = m or (n + 1) < m. This justifies

       (s < t)    :=      µX.λy N .(Sy = t) ∨ X (Sy)) s.

    Here X is a variable of type N → Ω and X s0 means s0 < t. Then the inequality s 6= t can
    be defined as (s < t) ∨ (t < s).                                                       J

    I Remark 5. HFLN does not have negation ¬. The absence of negation plays an important
    role in the interpretation of fixed-point operators, as we shall see in the next subsection.
    For a formula ϕ with no free variables except for those of type N, the negation ¬ϕ can be
    obtained by replacing each logical connective with its De Morgan dual,

       ∧ ! ∨,          µ ! ν,    and = ! 6=,

    as discussed in [11].                                                                          J


    2.2    Semantics of HFLN
    This subsection introduces the interpretations of types and formulas.
M. Kori, T. Tsukada and N. Kobayashi                                                                5


                JH ` x : AK(ρ) = ρ(x)
               JH ` Z : NK(ρ) = 0
              JH ` St : NK(ρ) = 1 + JH ` t : NK(ρ)
           JH ` s = t : ΩK(ρ) = (JH ` s : NK(ρ) = JH ` t : NK(ρ))
           JH ` ϕ ∨ ψ : ΩK(ρ) = (JH ` ϕ : ΩK(ρ) ∨ JH ` ψ : ΩK(ρ))
           JH ` ϕ ∧ ψ : ΩK(ρ) = (JH ` ϕ : ΩK(ρ) ∧ JH ` ψ : ΩK(ρ))
     JH ` λxA .ϕ : A → T K(ρ) = λv ∈ JAK.JH, x : A ` ϕ : T K(ρ[x 7→ v])
             JH ` ϕ ψ : T K(ρ) = (JH ` ϕ : A → T K(ρ)) (JH ` ψ : AK(ρ))
              JH ` ϕ t : T K(ρ) = (JH ` ϕ : N → T K(ρ)) (JH ` t : NK(ρ))
          JH ` µxT .ϕ : T K(ρ) = lfp(JH ` λxT .ϕ : T → T K(ρ))
          JH ` νxT .ϕ : T K(ρ) = gfp(JH ` λxT .ϕ : T → T K(ρ))


     Figure 2 Interpretation of terms and formulas.


     The interpretation of a type A is a poset JAK = (JAK, ≤A ). It is inductively defined by

          JNK := N                                               x ≤N y :⇔ x = y
          JΩK := { >, ⊥ }                                        x ≤Ω y :⇔ x = ⊥ or y = >
     JA → T K := {f : JAK → JT K | f is monotone}             f ≤A→T g :⇔ ∀x ∈ JAK.f (x) ≤T g(x).

Note that
   JA → T K is the space of monotone functions, and
   JT K is a complete lattice for every T .
On the contrary JAK is not necessarily a complete lattice since JNK is not.
   The interpretation JHK of a type environment H is the set of mappings ρ such that
ρ(x) ∈ JH(x)K for every x in the domain of H. The set JHK forms a poset with respect to
the point-wise ordering. An element of JHK is called a valuation. We write ρ[x 7→ v] for the
mapping defined by ρ[x 7→ v](x) = v and ρ[x 7→ v](y) = ρ(y) for y 6= x.
   Assume H ` ϕ : A (where ϕ is a formula or a term). Its interpretation JH ` ϕ : AK is a
monotone function JHK −→ JAK. The definition is in Figure 2. Here lfp(f ) and gfp(f ) are
the least and greatest fixed-points of the function f . The interpretations of the fixed-point
operators are well-defined since every monotone function f : P −→ P on a complete lattice
P has both the least and greatest fixed-points. We shall write JH ` ϕ : AK(ρ) simply JϕKρ
when no confusion can arise.
I Definition 6. Let H | Γ ` ∆ be a sequent and ρ be a valuation in JHK. Then we write
            V         W
Γ |=ρ ∆ if ϕ∈Γ JϕKρ ≤ ψ∈∆ JψKρ , or equivalently, if JϕKρ = ⊥ for some ϕ ∈ Γ or JψKρ = >
for some ψ ∈ ∆. A sequent H | Γ ` ∆ is valid if Γ |=ρ ∆ for all valuations ρ, and we denote
it briefly by Γ |= ∆.

 3      A Cyclic Proof System for HFLN
In this section, we introduce a cyclic proof system for HFLN . A cyclic proof is a proof
diagram which can contain cycles and should satisfy a certain condition in order to ensure
the soundness. Subsection 3.1 describes derivations and the soundness condition to define
cyclic proofs and Subsection 3.2 shows that the induction rule based on prefixed-points is
admissible. In Subsection 3.3, we show some examples of cyclic proofs.
                  Leibniz International Proceedings in Informatics
                  Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
6


    3.1    Definition of the Cyclic Proof System
    Figure 3 shows our deduction rules, which are based on Gentzen’s sequent calculus. Here
    ϕ[ψ/x] represents the capture-avoiding substitution and Γ[ϕ/x] represents the sequence of
    formulas which is the result of applying the substitution [ϕ/x] to all formulas in Γ. The rules
    should be easy to understand since most of the rules are standard. We explain uncommon
    rules. The rule (Mono) is based on the fact that each formula defines a monotone function,
    i.e. JψK v JχK implies Jϕ[ψ/x]K v Jϕ[χ/x]K. Since only a formula of type Ω can appear in a
    sequent, JψK v JχK is expressed as ψ ~y ` χ ~y for fresh ~y . The rules (λL) and (λR) are justified
    by the fact that the β-equivalence (λx.ϕ) ψ = ϕ[ψ/x] preserves semantics. The rules (σL) and
    (σR) express the fact that σx.ϕ (where σ is µ or ν) is a fixed-point and thus σx.ϕ = ϕ[σx.ϕ/x].
    The rule (Nat) says that a variable of type N indeed represents a natural number, and (P1)
    and (P2) correspond to the axioms (Z = Sx) → ⊥ and (Sx = Sy) → (x = y).
         Although every leaf of an ordinary proof tree is an axiom, this is not the case in cyclic
    proof systems. A (finite) derivation tree is a tree obtained by using the rules in Figure 3,
    whose leaves are not necessarily axioms. A leaf that is not an axiom is called open.
    I Remark 7. Though the rule (Mono) has only one premise in Figure 3, from now on, we
    treat it as the following rule with multiple premises:
                        {Γ, ψ ~y ` χ ~y , ∆}1,··· ,k
                                                       ~y ∩ F V (Γ, ψ, χ, ∆) = ∅, (Mono) .
                      Γ, ϕ[ψ/xT ] ` ϕ[χ/xT ], ∆
    Here, k is the number of occurrences of x in ϕ, and the rule above has a copoy of the premise
    Γ, ψ~y ` χ~y , ∆ for each occurence of x in ϕ. For example, the inference:
                                           x`x∨y
                                                                       (Mono)
                           x ∨ µz.(x ∨ z) ` (x ∨ y) ∨ µz.((x ∨ y) ∨ z)
    should actually be interpreted as
                                   x`x∨y          x`x∨y
                                                                      (Mono) .
                          x ∨ µz.(x ∨ z) ` (x ∨ y) ∨ µz.((x ∨ y) ∨ z)
        This enables us to trace fixed-point operators precisely in a derivation tree. See Defini-
    tion 9.

    I Definition 8 (Pre-proof). A pre-proof consists of a finite derivation tree D and a function
    R that assigns to each open leaf n in D a non-leaf node R(n) that has the same sequent as n.

       A pre-proof induces the infinite derivation tree by iteratively replacing an open leaf n
    with R(n). This correspondence would be helpful to understand the definitions below.
       A pre-proof is unsound in general, i.e., the root sequent of a pre-proof may be invalid.
    We introduce a sanity condition called the global trace condition, and define cyclic proofs as
    pre-proofs that satisfy this condition.
       Given a pre-proof (D, R), its path is a (finite or infinite) sequence (ni )i=1,2,... of nodes of
    D such that, for every i,
       if ni is an open leaf, then ni+1 = R(ni ), and
       otherwise ni+1 is a premise of ni .

        Given a path (ni )i=1,2,... , a pre-trace in this path is a sequence (τi )i=1,2,... of occurrences
    of formulas such that, for every i, τi is an occurrence of a formula in the sequent ni and τi+1
    is a “relevant occurrence” of τi in the sequent ni+1 . The latter condition means that τi+1
    originates from τi in a bottom-up construction of the proof. For example, if ni and ni+1
M. Kori, T. Tsukada and N. Kobayashi                                                            7




  Identity rules
                                                Γ ` ϕ, ∆   Γ, ϕ ` ∆
                              (Axiom)                               (Cut)
                      ϕ`ϕ                               Γ`∆
  Structural rules
                            Γ ` ∆ (Wk L)                 Γ ` ∆ (Wk R)
                           Γ, ϕ ` ∆                     Γ ` ϕ, ∆

                        Γ, ϕ, ϕ ` ∆                     Γ ` ϕ, ϕ, ∆
                                    (Ctr L)                         (Ctr R)
                         Γ, ϕ ` ∆                        Γ ` ϕ, ∆

                      Γ, ψ, ϕ, Γ0 ` ∆                  Γ ` ∆, ψ, ϕ, ∆0
                                      (Ex L)                           (Ex R)
                      Γ, ϕ, ψ, Γ0 ` ∆                  Γ ` ∆, ϕ, ψ, ∆0

                                         Γ`∆         (Subst)
                                     Γ[ϕ/x] ` ∆[ϕ/x]

                        Γ, ψ ~y ` χ ~y , ∆
                                             ~y ∩ F V (Γ, ψ, χ, ∆) = ∅, (Mono)
                   Γ, ϕ[ψ/xT ] ` ϕ[χ/xT ], ∆

  Logical rules (σ = µ, ν)

                  Γ[t/x, s/y] ` ∆[t/x, s/y]                                       (= R)
                                                (= L)             Γ ` t = t, ∆
               Γ[s/x, t/y], s = t ` ∆[s/x, t/y]

                     Γ, ϕ ` ∆      Γ, ψ ` ∆                    Γ ` ϕ, ψ, ∆
                                            (∨L)                           (∨R)
                          Γ, ϕ ∨ ψ ` ∆                        Γ ` ϕ ∨ ψ, ∆

                      Γ, ϕ, ψ ` ∆                 Γ ` ϕ, ∆    Γ ` ψ, ∆
                                  (∧L)                                 (∧R)
                     Γ, ϕ ∧ ψ ` ∆                     Γ ` ϕ ∧ ψ, ∆

                                ~`∆
                      Γ, ϕ[ψ/x] ψ                                   ~ ∆
                                                         Γ ` ϕ[ψ/x] ψ,
                                     (λL)                                (λR)
                                 ~`∆
                     Γ, (λx.ϕ) ψ ψ                                   ~ ∆
                                                        Γ ` (λx.ϕ) ψ ψ,

                                ~`∆
                   Γ, ϕ[σx.ϕ/x] ψ                                     ~ ∆
                                                        Γ ` ϕ[σx.ϕ/x] ψ,
                                    (σL)                                  (σR)
                              ~`∆
                    Γ, (σx.ϕ) ψ                                     ~ ∆
                                                         Γ ` (σx.ϕ) ψ,

  Natural number rules
  N ≡ µX.λx.(x = Z) ∨ (∃x0 .x = Sx0 ∧ X x0 )

              Γ, N xN ` ∆                                          Γ, s = t ` ∆
                          (Nat)                        (P1)                      (P2)
                 Γ`∆                      Ss = Z `                Γ, Ss = St ` ∆

  Figure 3 Deduction Rules.




              Leibniz International Proceedings in Informatics
              Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
8


    are respectively the conclusion and premise of (∧L), i.e., if ni is the sequent Γ, ϕ ∧ ψ ` ∆
    and ni+1 is Γ, ϕ, ψ ` ∆, then (i) ϕ and ψ in ni+1 are relevant occurrences of ϕ ∧ ψ in ni ,
    and (ii) each formula in Γ (resp. ∆) of ni+1 is a relevant occurrence of the corresponding
    formula in Γ (resp. ∆) of ni . For another example, if ni is the conclusion of (∨L), ni+1 is
    the left premise and τi is the occurrence of ϕ ∨ ψ, then τi+1 is the occurrence of ϕ. The
    concrete definition, which we omit here, is lengthy but straightforward; a possible exception
    is (Mono), in which ψ ~y and χ ~y are defined as relevant occurrences of ϕ[ψ/x] and ϕ[χ/x]
    respectively. See Appendix A for more detail. A pre-trace is a trace if, for infinitely many i,
    τi is the principal occurrence2 of a logical rule.
        The global trace condition requires existence of a “good” trace for each infinite path.
    The appropriate notion of “good” traces depends on the logic. In [3], a trace is “good” if
    it contains infinitely many principal occurrences of (µL) or (νR). In other words, a “good”
    trace contains infinitely many expansions of µ. This fairly simple condition comes from the
    restriction of usage of fixed-points: their logic does not allow alternation of fixed-points,
    e.g. µP.ϕ is allowed only if the free predicate variables of ϕ are bound by µ. Allowing nested
    fixed-points makes the definition of “good” traces more complicated; the definition in [7]
    refers to the most significant fixed-point operator among those that are expanded infinitely
    many times. The higher-order nature of HFLN requires us to more precisely track the usage
    of fixed-point operators.
        The following definition is inspired by the winning criterion of game semantics of HFLN [4,
    10, 14]. The idea is to track which occurences of fixed-point operators are unfolded infinitely
    in depth by annotating each occurrence with a sequence that grows with each unfolding. By
    abuse of notation, a path is written as a sequence (Γi ` ∆i )i=1,2,... of sequents. We often
    identify an occurrence of a formula with the formula. For example, τi ≡ ϕ means that τi is
    an occurrence of ϕ.
    I Definition 9 (µ-trace, ν-trace). Let (τi )i≥0 be a trace. We assign a sequence of natural
    numbers to every fixed-point operator in τi for all i by the following algorithm. We use σ as
    a metavariable of fixed-point operators { µ, ν }. We write σp for the fixed-point operator to
    which the sequence p is assigned.
        For every σ in τ0 , we assign  to σ.
        If τi is the principal occurrence of (σL/R), τi with annotation is σp x.ϕ (where fixed-point
        operators in ϕ are also annotated). Then τi+1 with annotation is ϕ[σp.k x.ϕ/x] where k is
        a natural number that has not been used in this annotation process.3
        If τi is the principal occurence of (Mono) and τi+1 is in the j-th premises, τi with
        annotation is ϕ[ψ1 /x1 , · · · ψk /xk ] (see Remark 7). Then τi+1 with annotation is ψj ~y .
        Otherwise, the sequence of a fixed-point operator in τi+1 comes from the corresponding
        operator in τi . For example, if τi is the principal occurrence of (λL/R) and τi with
        annotation is (λx.ϕ) ψ, then τi+1 with annotation is ϕ[ψ/x].
    Let p[0 : n] denote the sequence consisting of the first n elements of p. We call (τi )i≥0 a
    µ-trace (resp. ν-trace) if there is an infinite sequence p such that p[0 : n] is assigned to µ
    (resp. ν) in some τi for every natural number n.
    In the definiton above, for each trace (τi )i≥0 , there is at most one infinite trace p that satisfies
    the condition above; hence, no trace can be both a µ-trace and a ν-trace; see Lemma 23.


    2
      An occurrence of a formula in the conclusion of a rule in Figure 3 is principal if it belongs to neither Γ
      nor ∆.
    3
      One can weaken the freshness requirement for k: the minimal requirement is that the sequence p.k has
      not been used.
M. Kori, T. Tsukada and N. Kobayashi                                                                   9


I Example 10. Let us consider the following pre-proof (D, R).
                              (?) ` (νf.λg.g (f g)) (µx.λa.a)
                                                                  (λR)
                            ` (λa.a) ((νf.λg.g (f g)) (µx.λa.a))
                                                                    (µR)
                          ` (µx.λa.a) ((νf.λg.g (f g)) (µx.λa.a))
                                                                    (λR)
                           ` (λh.h ((νf.λg.g (f g)) h)) (µx.λa.a)
                                                                   (νR)
                              (?) ` (νf.λg.g (f g)) (µx.λa.a)
In the diagram, the function R is indicated by the ? marks: the open leaf (?) is mapped to
the other node marked (?). This pre-proof has a unique path, and the path has a unique
trace (τi )i≥0 (since each sequent consists of a single formula).
    We assign a sequence of natural numbers to each occurrence of a fixed-point operator in
the trace (τi )i≥0 . Both fixed-point operators in τ0 are annotated by the empty sequence:
   τ0    ≡    (ν f.λg.g (f g)) (µ x.λa.a).
The first rule expands ν, and we annotate the recursive occurrence of this ν with a fresh
natural number, say 0:
   τ1    ≡    (λh.h ((ν0 f.λg.g (f g)) h)) (µ x.λa.a).
The next rule is (λR) and we just substitute the annotated formula (µ x.λa.a) for h:
   τ2    ≡    (µ x.λa.a) ((ν0 f.λg.g (f g)) (µ x.λa.a)).
Then we expand µ and annotate its recursive occurrences (if there were any) with 1; actually,
since x does not appear in the body λa.a, the resulting formula does not have label 1.
   τ3    ≡    (λa.a) ((ν0 f.λg.g (f g)) (µ x.λa.a)).
Applying the β-reduction, we have
   τ4    ≡    (ν0 f.λg.g (f g)) (µ x.λa.a).
The current node is the open leaf, and the next node is determined by R. The annotation is
copied: τ5 ≡ τ4 . The next rule is (νR) and we name the recursive occurrences 0.2, extending
the annotation 0 by a fresh number 2:
   τ6    ≡    (λh.h ((ν0.2 f.λg.g (f g)) h)) (µ x.λa.a).
By continuing this argument, we have
   τ1+5k     ≡    (λh.h ((νp f.λg.g (f g)) h)) (µ x.λa.a)
where p = 0.2.4. . . . .(2k). Note that the annotation of ν grows but that of µ does not. Hence
this trace is a ν-trace but not a µ-trace.                                                   J
    A trace (τi )i≥0 is a left trace (resp. right trace) if τ0 occurs on the left (resp. right) side
of `. Note that every τi occurs on the same side as τ0 .
I Definition 11 (Cyclic proof). A cyclic proof is a pre-proof that satisfies the global trace
condition: for every infinite path, a tail of the path has a left µ-trace or right ν-trace.
I Example 12. The pre-proof in Example 10 is a cyclic proof.                                       J
I Remark 13. One may find our global trace condition (cf. Definitions 9 and 11) complicated
and wonder if it is possible to replace it with a simpler conidition such as the parity condition.
A recent result [14, Theorem 25] suggests a negative answer: It shows that the validity of
HFLN formulas cannot be captured by parity games, but games with more complicated
winning criteria. Our global trace condition is inspired by the criteria.                       J
                 Leibniz International Proceedings in Informatics
                 Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
10


     3.2    Some Admissible Rules
     This subsection shows that some familiar rules for quantifiers and inductions are admissible
     in our cyclic proof system.
         As we saw in Subsection 2.1, formulas with quantifiers can be expressed by fixed-points.
     The proposition below enables us to use quantifier rules in our cyclic proof system.

     I Proposition 14. If there is a cyclic proof of Γ ` ∆ derived by the rules in Figure 3 plus
     the following quantifier rules, then there exists a cyclic proof of Γ ` ∆ without the quantifier
     rules.

                       Γ, ϕ[ψ/x] ` ∆                    Γ ` ϕ, ∆
                                     (∀L)                          x 6∈ F V (Γ, ∆) (∀R)
                        Γ, ∀x.ϕ ` ∆                    Γ ` ∀x.ϕ, ∆

                        Γ, ϕ ` ∆                                     Γ ` ϕ[ψ/x], ∆
                                   x 6∈ F V (Γ, ∆) (∃L)                            (∃R)
                       Γ, ∃x.ϕ ` ∆                                    Γ ` ∃x.ϕ, ∆

     Proof. See Appendix B.                                                                                 J

        We can also embed explicit induction rules, so-called Park’s fixed-point rules:

                  Γ, ϕ[χ/x] ~y ` χ ~y , ∆            ~`∆
                                                Γ, χ ψ
                                                             ~y ∩ F V (Γ, ϕ[χ/x], ∆) = ∅ (Pre)
                                        ~`∆
                              Γ, (µx.ϕ) ψ

                  Γ, χ ~y ` ϕ[χ/x] ~y , ∆            ~ ∆
                                               Γ ` χ ψ,
                                                            ~y ∩ F V (Γ, ϕ[χ/x], ∆) = ∅ (Post)
                                        ~ ∆
                             Γ ` (νx.ϕ) ψ,

     They are inspired by Knaster-Tarski’s fixed-point theorem: these rules replace pre/postfixed-
     points with least/greatest fixed-points. The rule (Pre) is sound because χ is a prefixed-point
     by the left premise and µx.ϕ is the least one. The same argument holds for (Post).

     I Proposition 15. If there is a cyclic proof of Γ ` ∆ derived by the rules in Figure 3 +
     (Pre) + (Post), then there exists a cyclic proof of Γ ` ∆ without (Pre) and (Post).

     Proof. Given a cyclic proof Π that may use (Pre) and (Post), we first construct a pre-proof
     Π0 by removing (Pre) and (Post). For every instance of (Pre) of the form:

                                  Γ, ϕ[χ/x] ~y ` χ ~y , ∆          ~`∆
                                                              Γ, χ ψ
                                                                            (Pre)
                                                        ~`∆
                                              Γ, (µx.ϕ) ψ
     we will replace it with the following diagram.
                                                          ~`∆
                                                     Γ, χ ψ
                                                                 (Wk L)
                                       Π                  ~ χψ
                                               Γ, (µx.ϕ) ψ,  ~`∆
                                                                 (Cut)
                                              Γ, (µx.ϕ) ψ~`∆

                                                                                y ` χ~
                                                                  (?) Γ, (µx.ϕ) ~    y, ∆
                                                                                                (Mono)
                                                                             y ` ϕ[χ/x] ~
                                                                Γ, ϕ[µx.ϕ/x] ~          y, ∆
                                                                                                   (Wk R)
                                 y ` χ~
                       Γ, ϕ[χ/x] ~    y, ∆                                 y ` χ~
                                                              Γ, ϕ[µx.ϕ/x] ~    y , ϕ[χ/x] ~
                                                                                           y, ∆
           Π :=                                    (Wk L)                                          (µL)
                  Γ, (µx.ϕ) ~          y ` χ~
                            y , ϕ[χ/x] ~    y, ∆                         y ` χ~
                                                               Γ, (µx.ϕ) ~    y , ϕ[χ/x] ~
                                                                                         y, ∆
                                                                                                  (Cut)
                                                           y ` χ~
                                             (?) Γ, (µx.ϕ) ~    y, ∆
                                                                     (Subst)
                                                         ~ ` χ ψ,
                                               Γ, (µx.ϕ) ψ     ~ ∆
M. Kori, T. Tsukada and N. Kobayashi                                                                                11


     (Post) can also be removed in the same manner.
     We show that the resulting pre-proof Π0 is a cyclic proof. For each infinite path π in
Π0 , if some tail of π goes through only one cycle as the above one from (?) to (?) then we
can trace the left µ in µx.ϕ or the right ν in νx.ϕ. Otherwise, there exists a corresponding
infinite path in Π, which satisfies the global trace condition. Therefore Π0 is a cyclic proof of
Γ ` ∆.                                                                                         J

3.3    Examples
This subsection presents two examples of cyclic proofs.
I Example 16 (Well-foundedness of a tree). In this example, we write N∗ for the type of
finite sequences of natural numbers. We also use the concatenation operation (−) · (−). This
N∗ can be expressed by N and thus this additional type does not increase the expressivity.
    A tree is a subset of finite sequences of natural numbers that represents the complement
                                                                                      ∗
of the tree; the idea is to regard  as the root and p as the parent of p · i. Let f N →Ω be a
term representing a tree. We define Φ and Ψ as follows:
                  ∗                    ∗                             ∗
   Φ := µw(N →Ω)→Ω .λk N →Ω .k  ∨ ∀iN .w (λz N .k (i · z))
              ∗              ∗
   Ψ := µv N →Ω .λz N .f z ∨ ∀iN .v (z · i)
Then both Φ f and Ψ  represent well-foundedness of f , i.e. whether there is no infinite path
in f . Φ checks whether the tree k satisfies well-foundedness. This returns true if k has only
one node or all the immediate children of the root satisfy well-foundedness. Ψ checks whether
the subtree of f whose root node is z satisfies well-foundedness. This returns true if z is a
leaf or all subtrees under z satisfy well-foundedness.
    A cyclic proof of Φ f ` Ψ  is given as follows:
                                 (†)       Φ (λz.f (l · n · z)) ` Ψ (l · n)   (?)   YΦ (Sn) ` YΨ (Sn)
                                                                                                          (∧L, R)
                                             Φ (λz.f (l · n · z)) ∧ YΦ (Sn) ` Ψ (l · n) ∧ YΨ (Sn)
                                                                                                    (νL, R)
                                                        (?) YΦ n ` YΨ n
              (Axiom)                                                      (Subst)
      fl`fl                                                YΦ Z ` YΨ Z
                                                                         (∨L, ∨R, W k)
              f l ∨ ∀i.Φ (λz.f (l · i · z)) ` f l ∨ ∀i.Ψ (l · i)
                                                                 (µL, R)
                       (†) Φ (λz.f (l · z)) ` Ψ l
                                                       (Subst) and f ≡ λz.f ( · z)
                                Φf ` Ψ
where YΦ ≡ (νY.λi.Φ (λz.f (l · i · z)) ∧ Y (Si)) and YΨ ≡ (νY.λi.Ψ (l · i) ∧ Y (Si)). Here we
omit (Subst) for open leaves; hence cycles of (?) and (†) are valid, although two nodes for
each label have different sequents. Note that YΦ Z ≡ ∀i.Φ (λz.f (l · i · z)) and YΨ ≡ ∀i.Ψ (l · i).
   For all infinite paths, if the path includes (†) → (†) infinitely then we can trace the left µ
in Φ and otherwise we can trace the right ν in ∀i.Ψ (l · i).                                    J
    The example below demonstrates an application of our cyclic proof system to program
verification, based on the reduction of Kobayashi et al. [10, 16] from program verification to
HFLN validity checking.
I Example 17 (Example 2.4 and 3.3 in [16]). Consider the following OCaml-like program.
      let rec repeat f x =
        if x = 0 then ()
        else if * then repeat f (f x) else repeat f (x-1)
      in let y = input() in
        repeat (fun x -> x-y) n

                      Leibniz International Proceedings in Informatics
                      Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
12


     In this program, * represents a non-deterministic Boolean value and input() means a user
     input. We aim to verify that an appropriate input y makes this program eventually terminate.
         To verify this, we have to check ` input 0 (g n) where

          repeat := µR.λf.λx.(x = 0) ∨ (∃x0 .x = x0 + 1 ∧ f x (R f ) ∧ R f x0 )
             sub := λy.λx.λk.k (x − y)
               g := λz.λy.repeat (sub y) z
           input := µI.λx.λk.(k x) ∨ (I (x + 1) k)

     where (−) is defined naturally by using µ. Here, functions on integers of type N → N
     in the program have been turned into predicates of type N → (N → Ω) → Ω, which are
     obtained by CPS translation; for example, the function fun x->x-y has been turned into
     sub y (≡ λx.λk.k(x − y)). Note that input 0 (g n) is equivalent to ∃y.g n y, which models an
     angelic non-determinsm of input() in the program.
         The goal sequent can be proved by the following cyclic proof:
                                                (=R)
                                     `0=0           (µR, ∨R)
                                ` repeat (sub 1) 0
                                                        (=L)
                             n = 0 ` repeat (sub 1) n             Π
                                                                     (µL)
                                 (?, †) N n ` repeat (sub 1) n
                                                                (λR, Nat)
                                             ` gn1
                                                             (Wk R)
                                      ` g n 1, input 2 (g n)
                                                             (µR, ∨R)
                                         ` input 1 (g n)
                                                             (Wk R)
                                      ` g n 0, input 1 (g n)
                                                             (µR, ∨R)
                                         ` input 0 (g n)
                    (?) N n0 ` repeat (sub 1) n0
                                                        (λR)
               N n0 ` (sub 1) (n0 + 1) (repeat (sub 1))           (†) N n0 ` repeat (sub 1) n0
                                                                                               (∧R)
                        N n0 ` (sub 1) (n0 + 1) (repeat (sub 1)) ∧ repeat (sub 1) n0
      Π :=                                                                            (µR)
                                        N n0 ` repeat (sub 1) (n0 + 1)
                                                                          (=L)
                                    N n0 , n = n0 + 1 ` repeat (sub 1) n
                                                                            (∃L, ∧L)
                                  ∃n0 .N n0 ∧ n = n0 + 1 ` repeat (sub 1) n
         This satisfies the global trace condition because we can trace the left µ in N for every
     infinite path.                                                                            J

      4      Decidability of the Global Trace Condition
     For our cyclic proof system to be useful, there should exist an algorithm to check whether a
     given proof candidate is indeed a cyclic proof. It is easy to check whether a given candidate
     is a pre-proof, but it is non-trivial to check whether the pre-proof also satisfies the global
     trace condition. In this section we prove that the global condition is indeed decidable. We
     follow the approach in [3], which reduces the global trace condition of a pre-proof to Büchi
     automata containment. One automaton accepts all infinite paths of the pre-proof and the
     other accepts those that satisfy the global trace condition. Then whether the pre-proof is a
     cyclic proof corresponds to the inclusion between these automata.
         Let us briefly recall the definition of Büchi automata. A (nondeterministic) Büchi
     automaton is a tuple (Q, Σ, δ, Q0 , F ) where Q is a finite set of elements called states, Σ is a
     finite set of symbols, δ : Q × Σ × Q is a transition relation, Q0 ⊆ Q is a set of initial states,
M. Kori, T. Tsukada and N. Kobayashi                                                                          13


and F ⊆ δ is a set of accepting transition rules.4 Given an infinite word w = (ai )i≥0 ∈ Σω ,
a run over w is a sequence (qi )i≥0 of states such that q0 ∈ Q0 and (qi , ai , qi+1 ) ∈ δ for all
i ≥ 0. This run is accepting if (qi , ai , qi+1 ) ∈ F for infinitely many i. The automaton accepts
an infinite word if there is an accepting run over the word.
    Let (D, R) be a given pre-proof. The alphabet Σ is the set of nodes of D. Then an
infinite path is represented as an infinite word, and it is easy to construct an automaton
Apath that accepts all the paths of D. We define an automaton Agtc that checks if a given
path satisfies the global trace condition.
    The idea of the automaton is as follows. Recall Definition 9, in which we assign a sequence
of natural numbers to each occurrence of a fixed-point operator. One cannot directly simulate
the annotation process by an automaton since the set of sequences of natural numbers is
infinite. However, at the end of Definition 9, we focus on an infinite sequence p of natural
numbers, and sequences that are not prefixes of p can be safely ignored. Furthermore, it
suffices to remember exactly one finite sequence by the following argument. Consider the
case that τi ≡ σq x.ϕ where q is a prefix of p, and τi+1 ≡ ϕ[σq.k x.ϕ/x].
    If q.k is not a prefix of p, then we can safely forget the annotation q.k.
    If q.k is a prefix of p, then we can safely forget the annotation q.
To see the latter, observe that other expansions of σq generate annotations q.k 0 with k 0 6= k
by freshness of k 0 . Hence q.k 0 is not a prefix of p and thus we can forget it. So any extension
of q that will be generated afterward can be safely ignored, and thus we can forget q itself.
    The above argument motivates the following definition.
I Definition 18. A marked formula ϕ̌ is a formula in which some occurrences of fixed-point
operators σ are marked; a marked fixed-point operator is written as σ• . We write |ϕ̌| for the
(standard) formula obtained by removing marks. An occurrence-with-marks τ̌ is a pair (τ, ϕ̌)
of an occurrence τ and a marked formula ϕ̌ such that τ ≡ |ϕ̌|.
    We define Agtc . The set of states of Agtc consists of occurrences-with-marks of D and
a distinguished (initial) state ∗. Most rules just simulate Definition 9. For example, if τ
is the principal occurrence in the conclusion of (λL), (λx.ϕ̌) ψ̌ is a marked formula such
that τ ≡ (λx.|ϕ̌|) |ψ̌| and n is the premise, then ((τ, (λx.ϕ̌) ψ̌), n, (τ 0 , ϕ̌[ψ̌/x])) where τ 0 is the
unique occurrence in v that is relevant to τ . Important transition rules are those dealing
with (σL/R). Consider the state τ̌ = (τ, ϕ̌) where τ is the principal occurrence of (σL/R).
Let n be the premise and τ 0 be the unique relevant occurrence in n.
    Case ϕ̌ ≡ (σx.ψ̌) χ ~ˇ: The automaton just unfolds the fixed-point operator, i.e.,

                      ~ˇ), n, (τ 0 , ψ̌[(σx.ψ̌)/x] χ
         ((τ, (σx.ψ̌) χ                            ~ˇ)) ∈ δ.

                         ~ˇ: Note that there may be other copies of σ• x.ψ̌ in χ
     Case ϕ̌ ≡ (σ• x.ψ̌) χ                                                     ~ˇ or ψ̌. So the auto-
     maton has to choose which copy should be tracked, and the transition is nondeterministic.
     If the automaton decides to track the occurrence of σ• x.ψ̌ being unfolded, it removes all
     marks in χ~ˇ and tracks the recursive calls of the head occurrence by marking them:

                        ~ˇ), n, (τ 0 , |ψ̌|[(σ• x.|ψ̌|)/x] |χ
         ((τ, (σ• x.ψ̌) χ                                   ~ˇ|)) ∈ δ.

     Otherwise it removes the mark of the fixed-point operator being unfolded and unfolds it:

                        ~ˇ), n, (τ 0 , ψ̌[(σx.ψ̌)/x] χ
         ((τ, (σ• x.ψ̌) χ                            ~ˇ)), ∈ δ.


4
    This differs from the standard definition, in which the acceptance condition is specified by the set of
    accepting states. It is not difficult to see that this change does not affect the expressive power.
                    Leibniz International Proceedings in Informatics
                    Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
14


         If the rule is (µL) or (νR), then the former transition is an accepting transition. All
         other transitions for (σL/R) and other rules are not accepting.
     The initial state either ignores the input ((∗, n, ∗) ∈ δ) or nondeterministically chooses an
     occurrence-with-marks ((∗, n, τ̌ ) ∈ δ if τ̌ is an occurrence in n and has exactly one marked
     fixed-point operator).

     I Lemma 19. Let (D, R) be a pre-proof. For every infinite path π, π ∈ L(Agtc ) if and only
     if π satisfies the global trace condition.

     Proof. Assume that π satisfies the global trace condition. Let ((τi )i≥0 , p) be the pair of
     a trace (with annotations) and an infinite sequence of natural numbers that witnesses the
     global trace condition. For each i, let qi be the longest prefix of p among the annotations in
     τi . Let us mark σqi in τi and write ϕ̌i for the resulting marked formula. Then (τi , ϕ̌i )i≥0 is
     an accepting run.
          We prove the converse. Assume a (possibly non-accepting) run, which determines a
     trace (τi )i≥0 . We annotate (τi )i≥0 following Definition 9. Let qi be the sequence assigned
     to the marked operator in τi and p be the limit of (qi )i≥0 . The transition rules ensure
     the well-definedness of qi and p. If the run is accepting, p is infinite since (qi )i≥0 must
     grow infinitely many times. Furthermore it is a left µ-trace or right ν-trace as all accepting
     transitions are for (µL) or (νR).                                                              J

          We have the following theorem as a corollary.

     I Theorem 20. The validity checking of a pre-proof (D, R) is decidable.

      5      Soundness
     The soundness proof follows the proof strategy of [3]. We prove the claim by contraposition.
     Assume that the conclusion Γ ` ∆ of a cyclic proof is invalid. Then there exists a valuation
     ρ such that Γ 6|=ρ ∆. Since all rules are locally sound (i.e. if the premises are valid under
     a valuation, the conclusion is also valid under the valuation), there exists an infinite path
     whose sequents are invalid under ρ. Using the global trace condition, we construct an infinite
     decreasing chain of ordinals, a contradiction.
         To be precise, we impose on the infinite path a condition slightly stronger than the
     invalidity under ρ. To describe the condition, we need fixed-point operators µα x.ϕ and ν α x.ϕ
     annotated by ordinals. The semantics of µα x.ϕ is given by
                                                      G
         Jµ0 xT .ϕK(ρ) := ⊥T and Jµα xT .ϕK(ρ) :=        J(λx.ϕ) (µβ xT .ϕ)K(ρ).
                                                      β<α

     The definition of ν α x.ϕ is similar (but uses the dual operations).
         During the construction of the path, we give ordinal annotations to occurrences µ on
     the left side of ` and to occurrences of ν on the right side. The annotation processes are
     essentially the same as that in Definition 9. Again, the most important case is that τi is
     the principal occurrence of (µL) or (νR). Consider the (µL) case. Then τi ≡ (µα x.ϕ) ψ      ~
     (where µ in ϕ and ψ ~ are also annotated). By the assumption of the invalidity of the sequent
                                    ~
     under ρ, we have J(µα x.ϕ) ψK(ρ)    = >. The annotation to τi+1 is ϕ[µβ x.ϕ/x] ψ~ where β is
                                            β     ~
     the minimum ordinal such that Jϕ[µ x.ϕ] ψK(ρ) = >. By this process, fixed-point operators
     annotated with the same sequence of natural numbers have the same ordinal annotation. In
     other words, it defines a function from sequences q of natural numbers appearing in the trace
     to ordinal numbers αq . Furthermore one can show that αq.k < αq (provided that q.k appears
M. Kori, T. Tsukada and N. Kobayashi                                                               15


in the trace). Therefore, if the path has a left µ-trace witnessed by an infinite sequence p,
then αp[0:1] > αp[0:2] > αp[0:3] > . . . is an infinite decreasing chain of ordinals.
    The above argument shows the following theorem. A detailed proof is in Appendix C.

I Theorem 21 (Soundness). If there is a cyclic proof of Γ ` ∆, then Γ ` ∆ is valid.

 6     Completeness of Infinitary Variant
Our cyclic proof system is incomplete. Existence of a proof in our cyclic proof system is
computably enumerable, but the valid sequents in HFLN are not because HFLN includes
Peano arithmetic.
    The aim of this section is to find a complete proof system. Following [3], we study the
infinitary variant of our cyclic proof system, in which a proof is an infinite tree instead of a
finite tree with cycles. More precisely, an infinitary proof is a (possibly) infinite derivation
tree (without open leaves) of which all infinite paths satisfy the global trace condition.
Soundness proof of the previous section is applicable to the infinitary system as well. Here
we discuss its completeness.

I Theorem 22. Let Γ ` ∆ be a sequent without higher-order free variables. That means,
every free variable of the sequent is of type N or of type Nk → Ω for some k ≥ 0. If Γ |= ∆,
then Γ ` ∆ is provable in the infinitary proof system.

    We give a sketch of the proof. A detailed proof is given in Appendix D. We can assume
without loss of generality that the sequent has no free variable of type N.
    The construction of the infinitary proof is surprisingly straightforward. We start from
a (finite) pre-proof consisting only of the root node, which is an open leaf, and iteratively
expand each open leaf by applying rules (∨L/R), (∧L/R), (λL/R), and (σL/R). The only
restriction is that the expansion must be “fair”: the fairness condition we impose is that (i)
each open leaf will eventually be expanded, and (ii) for every path, each formula in a sequent
will eventually appear in the principal position (unless the path is terminated by the axiom
rule). This process generates a growing sequence of (finite) pre-proofs, and the infinitary
proof is defined as its limit.
    Now it suffices to show the global trace condition of the above constructed candidate
proof, but this is the hardest part of the proof. Assume an infinite path π. Since Γ |= ∆, for
each valuation ρ, there exists ϕ ∈ Γ such that JϕK(ρ) = ⊥ or ψ ∈ ∆ such that JϕK(ρ) = >.
Then, by a similar argument to the proof of soundness, existence of a left ν-trace or a right
µ-trace leads to a contradiction. It is worth noting that the construction is “dual”: whereas
in the soundness proof we ensure Jτi K(ρ) = > for a left-trace (τi )i≥0 , here Jτi K(ρ) = ⊥ is
kept. This difference allows us to construct a trace of the intended path π. By appropriately
choosing ρ, one can ensure that the generated trace is infinite; hence we have constructed an
infinite trace that is not left ν- nor right µ-trace. The proof is completed by the following
lemma, which is technical but often used in the analysis of HFL (cf. [4, Lemma 6 & 7], [10,
Lemma 26, Appendix E.2] and [14, Lemma 14]):

I Lemma 23. Every infinite trace (τi )i≤0 is either a µ-trace or a ν-trace but not both.

I Remark 24. We are not sure if the proof can be extended to sequents with higher-order free
variables. The problem is the construction of ρ. In the current setting, for each free variable
f of type Nk → Ω, the valuation ρ is defined for follows: for each k-tuple m     ~ of natural
numbers, (i) if f m
                  ~ appears on the left side of a sequent in the path, then ρ(f )(m)  ~ := >;
(ii) if f m                                                                 ~ := ⊥; and (iii)
          ~ appears on the right side of a sequent in the path, then ρ(f )(m)
                Leibniz International Proceedings in Informatics
                Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
16


     otherwise the value of ρ(f )(m)
                                   ~ is arbitrary. The point is that the values of arguments of
     each fully-applied occurrence of f is canonically determined. This construction of ρ is no
     longer possible in the presence of a higher-order free variable, say g : Ω → Ω. When g (f m)
                                                                                               ~
     appears on the left side, there are two assignments that make this formula true, namely
     ρ1 (g)(⊥) = > with ρ1 (f )(m)
                                ~ = ⊥ and ρ2 (g)(>) = > with ρ2 (f )(m)  ~ = >.                 J

         7    Related Work

     7.1      Cyclic Proof Systems
     The idea of cyclic proof can at least be traced back to the work of Sprenger and Dam [12] on
     a cyclic proof system called Sglob , where proofs are explicitly annotated with ordinals. The
     ordinal annotations are not convenient for automated theorem proving.
         Brotherston and Simpson [3] proposed a cyclic proof system called CLKID for a first-order
     predicate logic with inductive definitions, which does not require ordinal annotations. They
     have proved soundness of CLKID, and also shown that a proof system with explicit induction
     rules (called LKID) can be embedded into CLKID; we have shown analogous results in
     Theorem 21 and Proposition 15 for HFLN . Doumane [7] formalized a cyclic proof system
     for the linear-time (propositional) µ-calculus, which features alternating fixed-points. Our
     global trace condition has been inspired by her trace condition.
         Besides cyclic proof systems for ordinary first-order logics, cyclic proof systems have also
     been proposed for separation logics [1, 2, 13], and automated tools have been developed
     based on those cyclic proof systems.

     7.2      Proof Systems and Games for HFL
     HFL was originally proposed by Viswanathan and Viswanathan [15], and its extensions
     with arithmetic (such as HFLN ) have recently been drawing attention in the context of
     higher-order program verification [10, 16].
         For pure HFL (without natural numbers), Kobayashi et al. [8] proposed a type-based
     inference system for proving the validity of HFL formulas.5 It is left for future work to
     study the relationship between their type system and our cyclic proof system; it would be
     interesting to see whether their type system can be embedded in our cyclic proof system.
         Tsukada [14] gave a game-based characterization of HFLN . His game may be considered
     a special case of the infinitary version of our proof system, where formulas are restricted to
     those whose free variables have only natural number types.
         Burn et al. [5] proposed a refinement type system for HoCHC, which is closely related
     to the ν-only fragment of HFLN . Their proof system is incomplete, and does not support
     fixed-point alternations.

         8    Conclusion
     We have proposed a cyclic proof system for HFLN , a higher-order logic with natural numbers
     and alternating fixed-points, which we expect to be useful for higher-order program verification.
     Our proof system has been inspired by previous cyclic proof systems for first-order logics [3, 7].
     We have shown the soundness of the proof system and the decidability of the global trace


     5
         Actually, they formalized a type system for model checking, which can also be used as a proof system
         for proving validity of HFLN formulas without natural numbers.
M. Kori, T. Tsukada and N. Kobayashi                                                                 17


condition. We have also shown a restricted form of standard completeness for the infinitary
version of our proof system.
    Constructing a (semi-)automated tool based on our cyclic proof system is left for future
work. On the theoretical side, we plan to study whether Henkin completeness and the cut
elimination property hold for (possibly a variation of) our cyclic proof system.


     References
 1   James Brotherston, Dino Distefano, and Rasmus Lerchedahl Petersen. Automated cyclic
     entailment proofs in separation logic. In Nikolaj Bjørner and Viorica Sofronie-Stokkermans,
     editors, Automated Deduction - CADE-23 - 23rd International Conference on Automated
     Deduction, Wroclaw, Poland, July 31 - August 5, 2011. Proceedings, volume 6803 of Lecture
     Notes in Computer Science, pages 131–146. Springer, 2011. doi:10.1007/978-3-642-22438-6_
     12.
 2   James Brotherston, Nikos Gorogiannis, and Rasmus Lerchedahl Petersen. A generic cyclic
     theorem prover. In Ranjit Jhala and Atsushi Igarashi, editors, Programming Languages and
     Systems, pages 350–367, Berlin, Heidelberg, 2012. Springer Berlin Heidelberg.
 3   James Brotherston and Alex Simpson. Sequent calculi for induction and infinite descent.
     Journal of Logic and Computation, 21(6):1177–1216, December 2011.
 4   Florian Bruse. Alternating parity Krivine automata. In Erzsébet Csuhaj-Varjú, Martin
     Dietzfelbinger, and Zoltán Ésik, editors, Mathematical Foundations of Computer Science
     2014 - 39th International Symposium, MFCS 2014, Budapest, Hungary, August 25-29, 2014.
     Proceedings, Part I, volume 8634 of Lecture Notes in Computer Science, pages 111–122.
     Springer, 2014. URL: https://doi.org/10.1007/978-3-662-44522-8_10.
 5   Toby Cathcart Burn, C.-H. Luke Ong, and Steven J. Ramsay. Higher-order constrained Horn
     clauses for verification. PACMPL, 2(POPL):11:1–11:28, 2018. doi:10.1145/3158099.
 6   Patrick Cousot and Radhia Cousot. Constructive versions of Tarski’s fixed point theorems.
     Pacific J. Math., 82(1):43–57, 1979. URL: https://projecteuclid.org:443/euclid.pjm/
     1102785059.
 7   Amina Doumane. On the infinitary proof theory of logics with fixed points. Theses, Université
     Sorbonne Paris Cité, June 2017.
 8   Naoki Kobayashi, Étienne Lozes, and Florian Bruse. On the relationship between higher-order
     recursion schemes and higher-order fixpoint logic. ACM SIGPLAN Notices, 52(1):246–259,
     2017.
 9   Naoki Kobayashi, Takeshi Nishikawa, Atsushi Igarashi, and Hiroshi Unno. Temporal verification
     of programs via first-order fixpoint logic. In International Static Analysis Symposium, pages
     413–436. Springer, 2019.
10   Naoki Kobayashi, Takeshi Tsukada, and Keiichi Watanabe. Higher-order program verification
     via HFL model checking. In European Symposium on Programming, pages 711–738. Springer,
     2018.
11   Étienne Lozes. A type-directed negation elimination. In Ralph Matthes and Matteo Mio,
     editors, Proceedings Tenth International Workshop on Fixed Points in Computer Science,
     FICS 2015, Berlin, Germany, September 11-12, 2015, volume 191 of EPTCS, pages 132–142,
     2015. doi:10.4204/EPTCS.191.12.
12   Christoph Sprenger and Mads Dam. On the structure of inductive reasoning: Circular and
     tree-shaped proofs in the µ-calculus. In Foundations of Software Science and Computation
     Structures, pages 425–440. Springer Berlin Heidelberg, 2003.
13   Gadi Tellez and James Brotherston. Automatically verifying temporal properties of pointer
     programs with cyclic proof. J. Autom. Reasoning, 64(3):555–578, 2020. doi:10.1007/
     s10817-019-09532-0.
14   Takeshi Tsukada. On computability of logical approaches to branching-time property veri-
     fication of programs. In Proceedings of the 35th Annual ACM/IEEE Symposium on Logic
               Leibniz International Proceedings in Informatics
               Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
18


          in Computer Science, LICS ’20, page 886–899, New York, NY, USA, 2020. Association for
          Computing Machinery. doi:10.1145/3373718.3394766.
     15   Mahesh Viswanathan and Ramesh Viswanathan. A higher order modal fixed point logic. In
          International Conference on Concurrency Theory, pages 512–528. Springer, 2004.
     16   Keiichi Watanabe, Takeshi Tsukada, Hiroki Oshikawa, and Naoki Kobayashi. Reduction
          from branching-time property verification of higher-order programs to HFL validity checking.
          In Proceedings of the 2019 ACM SIGPLAN Workshop on Partial Evaluation and Program
          Manipulation, PEPM 2019, page 22–34, New York, NY, USA, 2019. Association for Computing
          Machinery. doi:10.1145/3294032.3294077.
M. Kori, T. Tsukada and N. Kobayashi                                                               19


 A     Definition of relevant occurrences
Here we give a detailed definition of the notion of relevant occurrences introduced after
Definition 8. We have already defined relevant occurrences for the rules (∧L), (∨L), and
(Mono). We give the definition for the other rules. Below, ni refers to the conclusion of each
rule, and ni+1 refers to one of the premises. In all the rules, each formula in Γ or ∆ in ni+1
is a relevant occurrence of the corresponding formula in Γ or ∆ in ni .
    In (Cut), ϕ in ni+1 is not relevant to any formula in ni .
    In (Ctr L) and (Ctl R), both occurrences of ϕ are relevant to ϕ in ni .
    In (Ex L) and (Ex R), ψ (ϕ, resp.) in ni+1 is a relevant occurrence of ψ (ϕ, resp.) in ni .
    In (Subst), each formula ψ in Γ (∆, resp.) of ni+1 is relevant to ψ[ϕ/x] in Γ[ϕ/x] (∆[ϕ/x],
    resp.) of ni .
    In (=L), each formula ψ[t/x, s/y] in Γ[t/x, s/y] (∆[t/x, s/y], resp.) of ni+1 is relevant to
    ψ[s/x, t/y] in Γ[s/x, t/y] (∆[s/x, t/y], resp.) of ni .
    In (∨R), ϕ and ψ in ni+1 are relevant to ϕ ∨ ψ in ni .
    In (∧R), ϕ and ψ in ni+1 are relevant to ϕ ∧ ψ in ni .
    In (λL) and (λR), ϕ[ψ/x] ψ  ~ in ni+1 is relevant to (λx.ϕ) ψ ψ
                                                                  ~ in ni .
    In (σL) and (σR), ϕ[σx.ϕ/x] ψ   ~ in ni+1 is relevant to (σx.ϕ) ψ
                                                                    ~ in ni .
    In (Nat), N x in ni+1 is not relevant to any formula in ni .
    In (P2), s = t in ni+1 is relevant to Ss = St in ni .


 B     Proof of Proposition 14
I Lemma 25. There exists a cyclic proof of ` Z ≤ t where ≤ ≡ (µY.λn.λm.(n = m) ∨
Y (Sn, m)).

Proof. The proof is as below:
                                           (?) N t ` Z ≤ t
                                            N t0 ` Z ≤ t0        Π
                                                                     (Cut)
                                                N t0 ` SZ ≤ St0
                                                                  (µR, ∨R, Wk)
                ` Z = Z (µR, ∨R, Wk)            N t0 ` Z ≤ St0
                                                                    (=L)
                `Z≤Z                         N t0 , t = St0 ` Z ≤ t
                          (=L)                                         (∃L, ∧L)
              t=Z`Z≤t                     ∃t0 .N t0 ∧ t = St0 ` Z ≤ t
                                                                       (µL)
                               (?) N t ` Z ≤ t
                                                 (Nat)
                                   `Z≤t
                                                  (†) z ≤ t0 ` Sz ≤ St0
                              (=R)                                       (Subst)
                  ` St0 = St0 (µR, ∨R)            Sz ≤ t0 ` SSz ≤ St0
                                                                             (Wk R)
                  ` St0 ≤ St0                 Sz ≤ t0 ` Sz = St0 , SSz ≤ St0
       Π :=                      (=L)                                        (µR, ∨R)
               z = t0 ` Sz ≤ St0                   Sz ≤ t0 ` Sz ≤ St0
                                                                        (µL)
                               (†) z ≤ t0 ` Sz ≤ St0
                                                        (Wk,   Subst)
                              N t0 , Z ≤ t0 ` SZ ≤ St0

For each infinite path π in the above pre-proof, if π goes along (†) infinitely often then we
can trace the left µ in the predicate ≤; otherwise, we can trace the left µ in N . Thus this
pre-proof satisfies the global trace condition.                                             J

Proof (Proposition 14). We first replace quantifier rules by the following proofs and con-
struct a pre-proof Π0 with no quantifier rules.
                 Leibniz International Proceedings in Informatics
                 Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
20


          If the rule is (∃L) and xN :
                             (?) Γ, (µE.λy.ϕ[y/x] ∨ E (Sy)) x ` ∆
                                                                   (Subst) since x 6∈ F V (Γ, ∆)
              Γ, ϕ ` ∆       Γ, (µE.λy.ϕ[y/x] ∨ E (Sy)) (Sx) ` ∆
                                                                   (∨L)
                   Γ, ϕ ∨ (µE.λy.ϕ[y/x] ∨ E (Sy)) (Sx) ` ∆
                                                              (µL)
                     (?) Γ, (µE.λy.ϕ[y/x] ∨ E (Sy)) x ` ∆
                                                            (Subst)
                       Γ, (µE.λy.ϕ[y/x] ∨ E (Sy)) Z ` ∆

          If the rule is (∃L) and xT :
                                     Γ, ϕ ` ∆
                                                 (Subst) since x 6∈ F V (Γ, ∆)
                                 Γ, ϕ[>T /x] ` ∆
                                                  (λL)
                                Γ, (λx.ϕ) >T ` ∆

          If the rule is (∃R) and xN :
                      Γ ` ϕ[t/x], ∆                 (?) Γ, z ≤ t ` Eϕ z, ∆
                                     (µR, ∨R)                               (Subst)
                       Γ ` Eϕ t, ∆                 Γ, Sz ≤ t ` Eϕ (Sz), ∆
                                        (= L)                               (µR, ∨R)
                   Γ, z = t ` Eϕ z, ∆                Γ, Sz ≤ t ` Eϕ z, ∆
                                                                           (∨L)
                                Γ, z = t ∨ Sz ≤ t ` Eϕ z, ∆
                                                              (µL)
                                   (?) Γ, z ≤ t ` Eϕ z, ∆
                                                            (Subst) where z is a free variable
                                     Γ, Z ≤ t ` Eϕ Z, ∆
                                                          (Cut) and ` Z ≤ t (see Lemma 25)
                                         Γ ` Eϕ Z, ∆
          where Eϕ ≡ (µE.λy.ϕ[y/x] ∨ E (Sy)) and ≤ ≡ (µY.λn.λm.n = m ∨ Y (Sn, m)).
          If the rule is (∃R) and xT :
                                                            (?) Γ, ψ ~y ` >T ~y , ∆
                                                                                    (νR)
                        Γ ` ϕ[ψ/x], ∆                       (?) Γ, ψ ~y ` >T ~y , ∆
                                             (Wk R)                                   (Mono)
                    Γ ` ϕ[ψ/x], ϕ[>T /x], ∆               Γ, ϕ[ψ/x] ` ϕ[>T /x], ∆
                                                                                      (Cut)
                                           Γ ` ϕ[>T /x], ∆
                                                              (λR)
                                          Γ ` (λx.ϕ) >T , ∆
          If the rule is (∀L) or (∀R) then the same method can be applied as (∃R) or (∃L).

     We need to check whether the pre-proof Π0 satisfies the global trace condition. For all
     infinite paths π, if there exits a tail of π which goes along only one cycle made by the above
     construction, then we choose the trace of the cycle. Otherwise, the corresponding path in Π
     is infinite and this path satisfies the global trace condition. Therefore we can choose a left
     µ-trace or right ν-trace in π.                                                              J

      C       Proof of Theorem 21
     Let f be a function on a complete lattice. For each ordinal α, we define f α (⊥) by:
                                    G
        f 0 (⊥) = ⊥ and f α (⊥) =       f (f β (⊥)).
                                         β<α

     Similarly f α (>) is defined by:
                                         l
          f 0 (>) = > and f α (>) =            f (f β (>)).
                                         β<α
M. Kori, T. Tsukada and N. Kobayashi                                                                 21


I Lemma 26 (Cousot-Cousot [6]). Let (C, ≤) be a complete lattice, f be a monotone function
and γ be an ordinal number greater than the cardinality of C. Then f γ (⊥) is the least
fixed-point of f and f γ (>) is the greatest fixed-point of f .

    We extend the definition of formulas by allowing µ and ν to have ordinal numbers like
µα , ν α . The definition of J.K for µα , ν α is as follows.

                   ~
   JH ` (µα xT .ϕ) ψK(ρ)                                             ~
                         = ((λv.JH, x : T ` ϕK(ρ[x 7→ v]))α (⊥n )) ρ(ψ)
                     ~
    JH ` (ν α xT .ϕ) ψK(ρ)                                             ~
                           = ((λv.JH, x : T ` ϕK(ρ[x 7→ v]))α (>n )) ρ(ψ)

Proof (Theorem 21). Assume there exists a cyclic proof Π of Γ ` ∆. We can naturally
transform this cyclic proof to an infinitary proof Π without (Subst). We assume towards
a contradiction that the root sequent Γ ` ∆ is invalid. Let ρ0 be a valuation such that
Γ 6|=ρ0 ∆.
      We will define an infinite path (ni )i≥0 = (Γi ` ∆i )i≥0 starting from Γ ` ∆ in Π , sequents
(n0i )i≥0 = (Γ0i ` ∆0i )i≥0 and valuations (ρi )i≥0 which satisfy the following four conditions:
 1. Γi ` ∆i is obtained by forgetting ordinal numbers of Γ0i ` ∆0i ;
 2. each µ in Γ0i (resp. ν in ∆i ) has an ordinal number;
 3. Γ0i 6|=ρi ∆0i holds;
 4. the ordinal number is determined by the sequence of natural numbers generated by
      Definition 9; and
 5. for each finite sequence q and natural number k, the ordinal for q.k is smaller than that
      for q.

   The definition of (ni , n0i , ρi )i≥0 is as below:

   n0 := Γ ` ∆. Because Γ0 ` ∆0 is invalid under ρ0 , we can get Γ00 ` ∆00 which is invalid
   under ρ0 by assigning ordinal numbers to all µ in Γ and ν in ∆.
   If ni , n0i , ρi are defined, then we define ni+1 , n0i+1 , ρi+1 as follows.
      If ni is an axiom, Γi ` ∆i must be valid and then Γ0i ` ∆0i must be so too. This is a
      contradiction.
      If ni is an open leaf: ni+1 := R(ni ), Γ0i+1 := Γ0i , ∆0i+1 := ∆0i , ρi+1 := ρi .
      Otherwise, we devide cases by the rule which has ni as the conclusion. Let p0 , p1 , ...
      be the premises sequents from left to right. Below, ϕ0 means the formula in Γ0i ∪ ∆0i
      which corresponds to ϕ in Γi ∪ ∆i .
       ∗ Case (Cut):
                                             Γ ` ϕ, ∆        Γ, ϕ ` ∆
                                                                        (Cut)
                                                        Γ`∆
           If there exists a valuation ρ such that (1) ρ is equal to ρi in F V (Γ, ∆) (i.e. x ∈
           F V (Γ, ∆) ⇒ ρ(x) = ρi (x)) and (2) JϕKρ = >, then ni+1 := p1 , ρi+1 := ρ. Since
           JϕKρ = >, there exists ϕ0 which holds Jϕ0 Kρ = > by assigning ordinal numbers to
           all µ in ϕ. Then Γ0i+1 := (Γ0i , ϕ0 ), ∆0i+1 := ∆0i .
           Otherwise, there exists ρ such that (1) and (3) JϕKρ = ⊥. By using this ρ, we execute
           ni+1 := p0 , ρi+1 := ρ. Since JϕKρ = ⊥, there exists ϕ0 which holds Jϕ0 Kρ = ⊥ by
           assigning ordinal numbers to all ν in ϕ. Γ0i+1 := Γ0i , ∆0i+1 := (ϕ0 , ∆0i ).
       ∗ Case (Mono):
                             {Γ, ψ ~y ` χ ~y , ∆}1,··· ,k
                                                          ~y ∩ F V (Γ, ψ, χ, ∆) = ∅, (Mono)
                           Γ, ϕ[ψ/xT ] ` ϕ[χ/xT ], ∆
                 Leibniz International Proceedings in Informatics
                 Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
22


       Let ψj and χj denote ψ and χ in the j-th premise. Suppose Jψj0 Kρi ≤ Jχ0j Kρi for all
       j ∈ {1, · · · , k} then J(ϕ[ψ/x])0 Kρi ≤ J(ϕ[χ/x])0 Kρi because Jλx.ϕ0 Kρi is a monotone
       function. This contradicts Γ0i 6|=ρi ∆0i thus there exists j ∈ {1, · · · , k} and ~v ∈ JT K
       such that Jψj0 Kρi ~v = > and Jχ0j Kρi ~v = ⊥. ni+1 := pj−1 , ρi+1 := ρi [~y 7→ ~v ], Γ0i+1 :=
       (Γ0 , ψj0 ~y ), ∆0i+1 := (χ0j ~y , ∆0 ).
     ∗ Case (∨L):
                                             Γ, ϕ ` ∆         Γ, ψ ` ∆
                                                                        (∨L)
                                                    Γ, ϕ ∨ ψ ` ∆
       Jϕ0 ∨ ψ 0 Kρi = Jϕ0 Kρi ∨ Jψ 0 Kρi = > since Γ0 , ϕ0 ∨ ψ 0 6|=ρi ∆0 . Therefore, Jϕ0 Kρi = > or
       Jψ 0 Kρi . If Jϕ0 Kρi = > then ni+1 := p0 , ρi+1 := ρi , Γ0i+1 := (Γ0 , ϕ0 ), ∆0i+1 := ∆0i else
       ni+1 := p1 , ρi+1 := ρi , Γ0i+1 := (Γ0 , ψ 0 ), ∆0i+1 := ∆0i .
     ∗ Case (∧R):
                                             Γ ` ϕ, ∆        Γ ` ψ, ∆
                                                                        (∧R)
                                                   Γ ` ϕ ∧ ψ, ∆
       Jϕ ∧ ψ Kρi = Jϕ Kρi ∧ Jψ Kρi = ⊥ since Γ 6|=ρi ϕ ∧ ψ 0 , ∆0 . Therefore, Jϕ0 Kρi = ⊥ or
          0        0          0           0                 0        0

       Jψ 0 Kρi = ⊥. If Jϕ0 Kρi = ⊥ then ni+1 := p0 , ρi+1 := ρi , Γ0i+1 := Γ0i , ∆0i+1 := (ϕ0 , ∆0 )
       else ni+1 := p1 , ρi+1 := ρi , Γ0i+1 := Γ0i , ∆0i+1 := (ψ 0 , ∆0 ).
     ∗ Case (µL):
                                                Γ, ϕ[µx.ϕ/x] ψ ~`∆
                                                                       (µL)
                                                 Γ, (µx.ϕ) ψ~`∆
       Let α be the ordinal number which assigned to the head µ of (µx.ϕ) ψ.              ~ If α = 0
                     0 T    0 ~0                  ~ 0
       then J(µ x .ϕ ) ψ Kρ = J(⊥T ) ψ Kρ = ⊥ and this contradicts the assumption.
                                 i                  i



           J(µα xT .ϕ0 ) ψ~ 0 Kρi = ((λv.Jϕ0 Kρi [x7→v] )α (⊥T )) (Jψ~ 0 Kρi )
                                      G
                                  =(     (λv.Jϕ0 Kρi [x7→v] ) ((λv.Jϕ0 Kρi [x7→v] )β (⊥T ))) (Jψ~ 0 Kρi )
                                     β<α

                                 =>

       Thus there exists β < α such that
                      ((λv.Jϕ0 Kρi [x7→v] ) ((λv.Jϕ0 Kρi [x7→v] )β (⊥T ))) (Jψ~ 0 Kρi ) = >.
       ni+1 := p0 , ρi+1 := ρi , Γ0i+1 := (Γ0 , ϕ0 [µβ x.ϕ0 /x] ψ~ 0 ), ∆0i+1 := ∆0i then

           J(ϕ0 [µβ x.ϕ0 /x]) ψ~ 0 Kρi = ((λv.Jϕ0 Kρi [x7→v] ) (Jµβ x.ϕ0 Kρi )) (Jψ~ 0 Kρi )
                                      = ((λv.Jϕ0 Kρi [x7→v] ) ((λv.Jϕ0 Kρi [x7→v] )β (⊥T ))) (Jψ~ 0 Kρi )
                                      =>

     ∗ Case (νR):
                                                          ~ ∆
                                            Γ ` ϕ[νx.ϕ/x] ψ,
                                                              (νR)
                                                        ~ ∆
                                             Γ ` (νx.ϕ) ψ,
       Let α be the ordinal number which assigned to the head ν of (νx.ϕ) ψ.            ~ If α = 0
       then J(ν 0 xT .ϕ0 ) ψ~ 0 Kρi = J(>T ) ψ~ 0 Kρi = > and this contradicts the assumption.

           J(ν α xT .ϕ0 ) ψ~ 0 Kρi = ((λv.Jϕ0 Kρi [x7→v] )α (⊥T )) (Jψ~ 0 Kρi )
                                       l
                                   =(     (λv.Jϕ0 Kρi [x7→v] ) ((λv.Jϕ0 Kρi [x7→v] )β (>T ))) (Jψ~ 0 Kρi )
                                     β<α

                                 =⊥

       Thus there exists β < α such that
M. Kori, T. Tsukada and N. Kobayashi                                                                                23


                          ((λv.Jϕ0 Kρi [x7→v] ) ((λv.Jϕ0 Kρi [x7→v] )β (>T ))) (Jψ~ 0 Kρi ) = ⊥.
           ni+1 := p0 , ρi+1 := ρi , Γ0i+1 := Γ0i , ∆0i+1 := (ϕ0 [ν β x.ϕ0 /x] ψ~ 0 , ∆0 ) then

               J(ϕ0 [ν β x.ϕ0 /x]) ψ~ 0 Kρi = ((λv.Jϕ0 Kρi [x7→v] ) (Jν β x.ϕ0 Kρi )) (Jψ~ 0 Kρi )
                                           = ((λv.Jϕ0 Kρi [x7→v] ) ((λv.Jϕ0 Kρi [x7→v] )β (>T ))) (Jψ~ 0 Kρi )
                                           =⊥

         ∗ Case (Nat):
                                            Γ, N xN ` ∆
                                                               (Nat)
                                                 Γ`∆
           If x ∈ F V (Γ, ∆) then ρi+1 := ρi and otherwise ρi+1 := ρi [x 7→ Z]. For each case,
           there is an ordinal number α such that JN α xKρi+1 = >. Then ni+1 := p0 , Γ0i+1 :=
           (Γ0i , N α x), ∆0i+1 := ∆0i .
         ∗ Otherwise: ni+1 := p0 , ρi+1 := ρi , Γ0i+1 := Γ0i , ∆0i+1 := ∆0i .

    Because of the global trace condition, (Γi ` ∆i )i≥0 has a trace (τi )i≥k which is a left
µ-trace or a right ν-trace. Then there is an infinite sequence p of the trace by the definition
of σ-trace. For all n ≥ 1, there is a σp[0:n] in some τi and we denote by αn the ordinal number
assigned to this σ.
    By the definiton of (αn )n≥1 and (Γ0i ` ∆0i )i≥0 , every ordinal number assigned to σp[0:n]
is αn . Thus for all n ≥ 1, there exists i such that (τi ≡ (σp[0:n] x.ϕ) ψ)      ~ → (τi+1 ≡
                     ~
(ϕ[σp[0:n+1] x.ϕ/x]) ψ). Hence αn > αn+1 holds for all n ≥ 1 so (αn )n≥1 is a decreasing
sequence of ordinal numbers. However, such a sequence does not exist so this is a contradic-
tion.                                                                                         J


 D       Proof of Theorem 22
I Lemma 27. Let Γ ` ∆ be a sequent and xN ∈ F V (Γ, ∆). If (Γ[Sn Z/x] ` ∆[Sn Z/x]) is
cut-free provable for all n ∈ N then Γ ` ∆ is cut-free provable.
Proof. Assume (Γ[Sn Z/x] ` ∆[Sn Z/x]) is cut-free provable for all n ∈ N, and let Πn be
the proof. We define (Πi )i≥0 recursively whose root node is (N x, Γ[Si x/x] ` ∆[Si x/x]) as
follows:
                                                                                 Πi+1
                                                                          i+1
                                                               N x, Γ[S         x/x] ` ∆[Si+1 x/x]
                                                                                                     (Subst)
     i                    Πi                                   N x0 , Γ[Si Sx0 /x] ` ∆[Si Sx0 /x]
  Π :=                                                                                                 (=L)
               Γ[Si Z/x] ` ∆[Si Z/x]                         x = Sx0 , N x0 , Γ[Si x/x] ` ∆[Si x/x]
                                              (=L)                                                       (∃L, ∧L)
            x = Z, Γ[Si x/x] ` ∆[Si x/x]                 ∃x0 .x = Sx0 ∧ N x0 , Γ[Si x/x] ` ∆[Si x/x]
                                                                                                         (µL)
                                           N x, Γ[Si x/x] ` ∆[Si x/x]

                      Π0
   Then Π := N x, Γ ` ∆             is a pre-proof of Γ ` ∆. For all infinite paths π in the
                              (Nat)
                    Γ`∆
pre-proof Π, if π goes through some Πi then there exists left µ-trace or right ν-trace because
Πi is a proof, and otherwise, we can trace the left µ in N . Therefore, Π is a proof of
Γ ` ∆.                                                                                      J

I Corollary 28. Let Γ ` ∆ be a sequent and ~x are all natural number free variables in Γ ∪ ∆.
                                                           ~ then Γ ` ∆ is cut-free provable.
If (Γ[~n/~x] ` ∆[~n/~x]) is cut-free provable for all ~n ∈ N
                   Leibniz International Proceedings in Informatics
                   Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
24


         Thanks to this corollary, it suffices to prove completeness of valid sequents whose free
     variables have type Nk → Ω for some k ≥ 0. In other words, we can assume without loss of
     generality that the sequent of interest has no free variable of type N.
         The next two definitions construct a tree Tω of Γ ` ∆ without natural number free
     variables. The first definition is needed to deal with all formulas in a fair manner.

     I Definition 29 (Schedule). A schedule element is a formula of the form ϕ ∨ ψ, ϕ ∧
                 ~ (σx.ϕ) ψ.
     ψ, (λx.ϕ) ψ ψ,       ~ We call (Ei )i≥0 a schedule if Ei is a schedule element for all i
     and every schedule element appears infinitely often in (Ei )i≥0 .

     There exists a schedule and we fix one.

     I Definition 30 (Tω ). Let Γ ` ∆ be a valid sequent that does not have natural number or
     higher-order free variables. That is, the type of each free variable in Γ ` ∆ is Nn → Ω for
     some n ∈ N.
         Then we will define trees (Ti )i≥0 whose roots are Γ ` ∆ inductively by using a schedule
     (Ei )i≥0 . First, T0 is defined by T0 := Γ ` ∆.
         Assume Ti is already defined. Then we define Ti+1 in Ti by replacing each open leaf
     Γ0 ` ∆0 with the following tree:
         If there exists a formula ϕ ∈ Γ0 ∩ ∆0 :
                                                       (Axiom)
                                                ϕ`ϕ
                                                        (Wk)
                                               Γ0 ` ∆0
        If (Sn Z = Sm Z) ∈ Γ0 for some different natural numbers n, m:
                                                         (P1)
                                          Z = S|n−m| Z ` (P2)
                                          Sn Z = Sm Z ` (Wk)
                                             Γ 0 ` ∆0
        If (Sn Z = Sn Z) ∈ ∆0 for some n:
                                                          (=R)
                                            ` Sn Z = Sn Z (Wk)
                                               Γ0 ` ∆0
        Otherwise: This replacement is performed in such a way that each formula is chosen as
        the target of expansion in a fair manner, so that every formula is expanded at some point.
           Case (Ei ≡ ϕ ∨ ψ):
           ∗ if Ei ∈ Γ0 :
                                          Γ 0 , ϕ ` ∆0         Γ0 , ψ ` ∆0
                                                                             (∨L)
                                                  Γ 0 , ϕ ∨ ψ ` ∆0
                                                                       (Ctr)
                                                        Γ0 ` ∆0
           ∗ if Ei ∈ ∆0 :
                                                   Γ0 ` ϕ, ψ, ∆0
                                                                      (∨R)
                                                  Γ0 ` ϕ ∨ ψ, ∆0
                                                                      (Ctr)
                                                        Γ 0 ` ∆0
           Case (Ei ≡ ϕ ∧ ψ): The tree is defined in the similar way to the case Ei ≡ ϕ ∨ ψ.
                                 ~
           Case (Ei ≡ (λx.ϕ) ψ ψ):
           ∗ if Ei ∈ Γ0 :
                                                         ~ ` ∆0
                                             Γ0 , ϕ[ψ/x] ψ
                                                                 (λL)
                                                          ~ ` ∆0
                                            Γ0 , (λx.ϕ) ψ ψ
                                                                 (Ctr)
                                                   Γ 0 ` ∆0
           ∗ if Ei ∈ ∆0 :
M. Kori, T. Tsukada and N. Kobayashi                                                                25


                                           Γ0 ` ϕ[ψ/x] ψ,~ ∆0
                                                               (λR)
                                          Γ0 ` (λx.ϕ) ψ ψ,~ ∆0
                                                               (Ctr)
                                                Γ 0 ` ∆0
                        ~
      Case (Ei ≡ (σx.ϕ) ψ):
      ∗ if Ei ∈ Γ :
                 0

                                         Γ0 , ϕ[σx.ϕ/x] ψ ~ ` ∆0
                                                                 (σL)
                                                       ~ ` ∆0
                                           Γ0 , (σx.ϕ) ψ
                                                                (Ctr)
                                                  Γ0 ` ∆0
       ∗ if Ei ∈ ∆0 :
                                      Γ0 ` ϕ[σx.ϕ/x] ψ,  ~ ∆0
                                                              (σR)
                                         Γ0 ` (σx.ϕ) ψ,~ ∆0
                                                             (Ctr)
                                              Γ 0 ` ∆0
Note that for all i ≥ 0, Ti ⊆ Ti+1 and each sequent of an open leaf in Ti+1 includes the
sequent of the corresponding leaf in Ti . We define Tω to be limi→∞ Ti .

   We aim to prove that Tω is a proof of Γ ` ∆.

I Definition 31 (Γω `n/π ∆ω , ρω ). For all open leaves n of Tω , we define Γω `n ∆ω as the
leaf sequent. For all infinite paths π = (πi )i≥0 in Tω , we define Γω `π ∆ω as limi→∞ (Γi ` ∆i )
where Γi ` ∆i is the sequent of πi .
    A valuation ρω of Γω `n/π ∆ω is defined as below:
                      (
               Ω        > if x ∈ Γω
          ρω (x ) :=
                        ⊥ otherwise
                             (
          Nn →Ω          Nn    > if f ~x ∈ Γω
    ρω (f        ) := λ~x .
                               ⊥ otherwise

I Lemma 32. Tω is a proof.

Proof. We aim to show that Tω is a pre-proof and Tω satisfies the global trace condition.
    Assume Tω is not a pre-proof. There exists an open leaf n in Tω , and all formulas of the
leaf are of the form xΩ , f ~t or Sm Z = Sn Z. Then the definition of ρω of Γω `n ∆ω induces
JϕKρω = > for all ϕ ∈ Γω and JϕKρω = ⊥ for all ϕ ∈ ∆ω . This contradicts to Γ |= ∆ because
Γ ⊆ Γω and ∆ ⊆ ∆ω . Therefore Tω is a pre-proof.
    We next show that Tω satisfies the global trace condition. For all infinite paths π in Tω ,
we define ρω of Γω `π ∆ω as Definition 31. We have Γ |= ∆, Γ ⊆ Γω and ∆ ⊆ ∆ω by the
assumption and the construction of Tω . Therefore, it follows that there exists either (1) a
formula ϕ ∈ Γω such that JϕKρω = ⊥ or (2) a formula ϕ ∈ ∆ω such that JϕKρω = >. We now
give the proof only for the case (1). The other case can be also proved by the same method.
    Let j be a number such that ϕ ∈ πj . We will show that there exists a left µ-trace (τi )i≥j
in π starting from ϕ.
    We define (τi )i≥j and (τi0 )i≥j which satisfy the following conditions:
 1. τi ∈ Γi ;
 2. we can get τi by forgetting ordinal numbers of τi0 ;
 3. each ν in τi0 has an ordinal number;
 4. Jτi0 Kρω = ⊥ where J.K for ν α is the same as Appendix C;
 5. each ordinal number in τi+10
                                   is less than or equal to the corresponding ordinal number in
     0
    τi .
   The definition of (τi )i≥j and (τi0 )i≥j as below:
                Leibniz International Proceedings in Informatics
                Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
26


        τj := ϕ. Because JϕKρω = ⊥, we can get ϕ0 which satisfies Jϕ0 Kρω = ⊥ by assigning
        ordinal numbers to all ν in ϕ.
        Assume τi and τi0 are defined. Below, ψ 0 means the corresponding subformula of τi0 for
        each subformula ψ of τi .
           If τi ≡ x:
           Since x ∈ Γi , JxKρω = > because of the definition of ρω . By the assumption of τi0 ,
           J(x)0 Kρω = JxKρω = ⊥. This is a contradiction.
           If τi ≡ (Sn Z = Sm Z):
           By the assumption of τi0 , J(Sn Z = Sm Z)0 Kρω = JSn Z = Sm ZKρω = ⊥. Then n 6= m
           holds and π is not infinite because of the construction of Tω . This contradicts the fact
           that π is an infinite path.
           If τi ≡ f ~t:
           Since f ~t ∈ Γi , Jf ~tKρω = > because of the definition of ρω . By the assumption of τi0 ,
           J(f ~t)0 Kρω = Jf ~tKρω = ⊥. This is a contradiction.
                                                    0
           If Ei 6≡ τi then τi+1 := τi and τi+1        := τi0 .
           Otherwise:
           ∗ Case τi ≡ (ψ ∨ χ):
              Since Jψ 0 ∨ χ0 Kρω = ⊥, Jψ 0 Kρω = Jχ0 Kρω = ⊥. τi+1 := ψ, τi+1 0
                                                                                   := ψ 0 if π goes to the
                                                           0       0               0
              left leaf, and otherwise τi+1 := χ, τi+1 := χ . In each case, Jτi+1      Kρω = ⊥ holds.
           ∗ Case τi ≡ (ψ ∧ χ):
              Since Jψ 0 ∧ χ0 Kρω = ⊥, either Jψ 0 Kρω or Jχ0 Kρω is ⊥.
                            0
              τi+1 := ψ, τi+1     := ψ 0 if Jψ 0 Kρω = ⊥, and otherwise τi+1 := χ, τi+1
                                                                                     0
                                                                                         := χ0 .
           ∗ Case τi ≡ (λx.ψ) χ θ:     ~
              τi+1 := ψ[χ/x] θ,  ~ τ 0 := ψ 0 [χ0 /x] θ~0
                                      i+1
              then Jψ 0 [χ0 /x] θ~0 Kρω = J(λx.ψ 0 ) χ0 θ~0 Kρω = ⊥.
           ∗ Case τi ≡ (µx.ψ) θ:     ~
              τi+1 := ψ[µx.ψ/x] θ,    ~ τ 0 := ψ 0 [µx.ψ 0 /x] θ~0
                                          i+1
              then J(ψ [µx.ψ /x]) θ~0 Kρω = J(µx.ψ 0 ) θ~0 Kρω = ⊥.
                         0       0

           ∗ Case τi ≡ (νx.ψ) θ:     ~
              Let α be the ordinal number assigned to the head ν of (νx.ϕ) ψ.           ~ If α = 0 then
                   0 T    0 ~0                  ~ 0
              J(ν x .ϕ ) ψ Kρ = J(>T ) ψ Kρ = > and this contradicts the assumption.
                                 ω                   ω



                  J(ν α x.ψ 0 ) θ~0 Kρω = ((λv.Jψ 0 Kρω [x7→v] )α (>n )) Jθ~0 Kρω
                                            l
                                        =(     (λv.Jψ 0 Kρω [x7→v] ) ((λv.Jψ 0 Kρω [x7→v] )β (>n ))) Jθ~0 Kρω
                                           β<α

                                      =⊥

              There exists β < α such that ((λv.Jψ 0 Kρω [x7→v] ) ((λv.Jψ 0 Kρω [x7→v] )β (>n ))) Jθ~0 Kρω = ⊥.
                                ~ τ 0 := ψ 0 [ν β x.ψ 0 /x] θ~0 then
              τi+1 := ψ[νx.ψ/x] θ,  i+1


                  J(ψ 0 [ν β x.ψ 0 /x]) θ~0 Kρω = ((λv.Jψ 0 Kρω [x7→v] ) (Jν β x.ψ 0 Kρω )) Jθ~0 Kρω
                                              = ((λv.Jψ 0 Kρω [x7→v] ) ((λv.Jψ 0 Kρω [x7→v] )β (>n ))) Jθ~0 Kρω
                                              =⊥

     If this (τi )i≥j is a ν-trace, there is an infinite sequence p of the trace by the definition of
     ν-trace. For all n ≥ 1, there is a νp[0:n] in some τi and we denote by αn the ordinal number
     assigned to this ν in τi0 . By the definition of (τi0 )i≥j , all ordinal numbers assigned to νp[0:n]
     is equal to αn . Then for all n ≥ 1, there exists i such that (τi ≡ (νp[0:n] x.ψ) θ)  ~ → (τi+1 ≡
M. Kori, T. Tsukada and N. Kobayashi                                                                27


                     ~ Hence αn > αn+1 holds for all n ≥ 1 so (αn )n≥1 is a decreasing
(ψ[νp[0:n+1] x.ψ/x]) θ).
sequence of ordinal numbers. However, such a sequence does not exist, hence a contradiction.
By Lemma 23, it follows that (τi )i≥j is a left µ-trace of π.
   Therefore Tω satisfies the global trace condition.                                     J

Proof (Theorem 22). Let ~x be all natural number free variables of Γ ` ∆. By Corollary 28,
                                                                               ~ For each ~n ∈ N,
it suffices to show that Γ[~n/~x] ` ∆[~n/~x] is cut-free provable for all ~n ∈ N.              ~
we construct Tω for Γ[~n/~x] ` ∆[~n/~x] as Definition 30, then Lemma 32 concludes that Tω is a
proof. Besides, Tω is cut-free by the construction of Tω .                                     J




                Leibniz International Proceedings in Informatics
                Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
