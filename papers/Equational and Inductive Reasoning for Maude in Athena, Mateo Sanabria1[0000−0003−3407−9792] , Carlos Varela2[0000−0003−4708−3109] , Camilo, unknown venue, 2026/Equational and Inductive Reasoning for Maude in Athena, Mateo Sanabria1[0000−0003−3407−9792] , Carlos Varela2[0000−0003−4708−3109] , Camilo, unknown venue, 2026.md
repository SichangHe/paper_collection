                                             Equational and Inductive Reasoning for Maude in Athena

                                                 Mateo Sanabria1[0000−0003−3407−9792] , Carlos Varela2[0000−0003−4708−3109] , Camilo
                                                     Rocha3[0000−0003−4356−7704] , and Nicolás Cardozo1[0000−0002−1094−9952]
                                                                      1
                                                                       Universidad de los Andes, Bogotá , Colombia
                                                                       2
                                                                        Rensselaer Polytechnic Institute, Troy, USA
                                                                    3
                                                                      Pontificia Universidad Javeriana, Cali, Colombia
arXiv:2604.19475v1 [cs.LO] 21 Apr 2026




                                               Abstract. In the rewriting logic framework, equational-based specifications are used to de-
                                               fine deterministic functional behavior, abstract data types, and canonical representations of
                                               data. These specifications include a (possibly order-sorted) signature and equations inter-
                                               preted modulo structural axioms, such as associativity, commutativity, and identity. While
                                               equational rewriting provides a powerful basis for execution and symbolic reasoning, it does
                                               not by itself offer native support for inductive or deductive reasoning. This paper presents
                                               maude2athena, a framework that systematically translates Maude’s equational theories into
                                               Athena, a theorem proving language designed to support natural deduction proofs over many-
                                               sorted first-order logic specifications, including inductive reasoning, equational chaining, case-
                                               based reasoning, and proofs by contradiction. The translation supports induction-based rea-
                                               soning modulo structural axioms with parametric induction rules; it faithfully encodes mem-
                                               bership equational logic in a many-sorted setting without exponential blowup under reason-
                                               able conditions. This approach preserves the semantics of the original specification, while
                                               ensuring that the translation remains compact and amenable to deductive reasoning. This
                                               work helps bridge the gap between model checking and theorem proving, enabling formal
                                               verification efforts that can benefit from both of these approaches.

                                               Keywords: Deductive reasoning · Inductive reasoning · Membership equational logic · Rea-
                                               soning modulo axioms · Model checking and theorem proving · Maude · Athena


                                         1   Introduction
                                         Rewriting Logic [1] has established itself as a powerful semantic and specification framework for
                                         modeling computational systems, supporting both executable specifications and rigorous equational
                                         reasoning. Within this framework, equational-based specifications play a central role in defining de-
                                         terministic functional behavior, abstract data types, and canonical representations of data. Lan-
                                         guages such as Maude [2] provide strong support for this style of specification through membership
                                         equational logic, offering subsort relations, operator overloading, and rewriting modulo structural
                                         axioms such as associativity, commutativity, and identity. While rewriting logic is a logical frame-
                                         work that can be used for symbolic reasoning, including reasoning over its own specifications [3],
                                         Maude currently offers limited support for interactive theorem proving, especially for proofs that
                                         require explicit inductive reasoning or fine-grained proof control. In contrast, interactive theorem
                                         provers such as Athena [4] provide robust environments for natural-deduction reasoning in many-
                                         sorted first-order logic, together with strong support for induction and proof structuring. However,
                                         Athena lacks native support for the order-sorted features that are essential to many Maude spec-
                                         ifications. As a consequence, fully-fledged Maude specifications cannot be directly reused within
                                         Athena without a careful reconciliation of their underlying logical foundations.
2        M.Sanabria et al.

    This paper presents maude2athena, a framework that systematically translates Maude functional
modules into Athena modules, enabling equational and inductive reasoning over Maude specifica-
tions within Athena’s interactive proof environment. The translation is grounded in a semantics-
preserving mapping from membership equational logic to many-sorted first-order logic, in which
subsort relations are made explicit through cast operators and coherence axioms [5]. To ensure
scalability and avoid exponential blowup, the approach relies on the notion of strictly sensible
order-sorted algebras [5, 6], which guarantees a linear and unambiguous translation in the presence
of operator overloading.
    A central challenge in this translation is the loss of native structural induction when order-sorted
datatypes are flattened into many-sorted domains. Although this transformation preserves equa-
tional reasoning, it removes the inductive structure that is essential for proving many correctness
properties. To address this issue, Athena is extended with parametric structural induction primitives
that reconstruct the induction principles implicit in the original Maude specification. This design
allows different induction schemes to be instantiated as needed, enabling inductive proofs over trans-
lated domains without resorting to encodings of operational semantics or meta-level reasoning. In
this paper, this parametric framework is instantiated with structural induction for sufficiently com-
plete equational specifications [7]; other induction principles can be accommodated as well, such as
structural induction over the oriented equations of a terminating equational theory.
    By bridging executable equational specifications in Maude with interactive inductive proofs
in Athena, maude2athena enables a compositional workflow in which specification, execution, and
proof coexist within a single formal development. The proposed translation preserves the equational
theory of the original specification while remaining compact and amenable to both interactive
and automated reasoning. The approach is validated through theoretical results establishing the
correctness of the translation, as well as through a non-trivial case study involving the verification
of a compiler specification that relies heavily on subsorting and inductive reasoning.4


2     Preliminaries

This section presents an overview on rewriting logic in Maude, and theorem proving in Athena.


2.1    Rewriting Logic and Maude

Rewriting logic [1] is built on top of membership equational logic [8] as the underlying equational
formalism. Maude [2] is a high-performance logical framework and specification language based on
rewriting logic. Membership equational logic supports sorts, equations, and membership axioms
that characterize the elements of a sort. While the full language extends these characteristics with
rewrite rules to represent transitions in concurrent systems, this paper focuses on the translation
of the functional (equational) sub-language.
    Membership equational logic is defined over a many-kinded signature (K, F ), where K is a set
of kinds and F = {Fw,k }(w,k)∈K ∗ ×K is a family of function symbols typed over those kinds. In
addition to kinds, the logic considers a K-indexed family of sorts S = {Sk }k∈K , which allows for
ascribing sorts to terms using the notation t : s (term t has sort s). Thus, a complete signature
in membership equational logic is a triple Σ = (K, F, S). The sorts S are equipped with a partial
order ≤ (subsorting), and operators in F are defined over these sorts. This view associates the
4
    The maude2athena framework is available at https://github.com/FLAGlab/Maude2Athena.
                                          Equational and Inductive Reasoning for Maude in Athena        3

     kinds K as the connected components of the subsort relation ≤. Since an order-sorted algebra can
     be canonically mapped to a membership algebra [1, 9], the order-sorted setting is used throughout
     this paper. A membership equational theory is a pair (Σ, E), combining a signature Σ with a set
     of sentences E (conditional equations and membership axioms). Equality modulo E, denoted =E ,
     is the finest congruence on the term algebra TΣ (X) that satisfies the Horn clauses in E. That is,
     for any terms t, u ∈ TΣ (X), t =E u iff E ⊢ t = u. Semantic structures of equational theories are
     called algebras. The expression TΣ is the sorted ground term algebra of Σ and TΣ (X) the sorted
     term algebra of Σ with variables in X. Likewise, the quotient structure TΣ/E is the initial algebra
     of (Σ, E) meaning that two terms t, u ∈ TΣ are in the same equivalence class iff t =E u. This is
     naturally extended to the algebra TΣ/E (X) of terms with variables in X modulo the equations E.
         Maude partitions the specification into a set of structural axioms A (such as associativity, com-
     mutativity, and identity) and a set of functional equations E ′ . Consequently, an equational theory
     is understood as (Σ, E ′ ∪ A), where rewriting is performed modulo the structural axioms A by
     orienting the equations from left to right. In Maude, functional modules correspond to membership
     equational theories and define data types and their operations. Equations are treated as simplifica-
     tion rules applied left to right. By assuming sort-decreasingness, ground confluence, and operational
     termination, repeated application of the oriented equations reduces a term to its canonical form [10,
     11]. Furthermore, it is assumed that an equational theory (Σ, E ′ ∪ A) is sufficiently complete with
     respect to a subsignature Ω ⊆ Σ meaning that, for any sort s ∈ S and term t ∈ TΣ,s , there is a
     term u ∈ TΩ,s such that t =E u.
         Listing 1.1 presents a functional module specification of Peano numbers. The PEANO module
     is delimited by the Maude keywords fmod and endfm. Sorts are declared with the sort keyword,
     and subsort relations use subsorts together with the symbol < (Lines 2–3). Operators are declared
     with op; each declaration specifies the operator name, its sort signature, and an optional set of
     attributes that declare the structural set of axioms for the equational theory. Particularly, the
     attribute ctor marks constructors for the sort. The elements of the sort Even are defined recursively
     by a conditional equation (Line 8), and the Peano axioms are introduced as equations (Lines 9–10)
     defining the set E for the equational theory.

1    fmod PEANO is
2      sort NzNat Even Nat .
3      subsorts NzNat Even < Nat .
4      op zero : -> Even [ctor] .
5      op s_ : Nat -> NzNat [ctor] .
6      op _+_ : Nat Nat -> Nat .
7      vars N M : Nat .
8      cmb s s N : Even if N : Even .
9      eq N + zero = N .
10     eq N + s M = s (N + M) .
11   endfm
                              Listing 1.1. Definition of Peano numbers in Maude.



     2.2   Theorem Proving in Athena
     Athena [4] is a dual deduction and computation language: users can define procedures, which ab-
     stract over computations (i.e., lambda calculus abstractions in functional programming); and meth-
     ods, which abstract over Fitch-style natural deductions [12, 13]. When evaluating procedures, if
    4       M.Sanabria et al.

    successful, Athena can return values (of different types), or else, it can diverge or result in an error.
    When evaluating methods, if successful, Athena produces logically sound theorems—modulo its
    assumption base—as sentences in many-sorted first order logic [14]. Athena has been effectively
    used to reason about concurrent programming—particularly, the actor model [15, 16], and about
    safety-critical cyber-physical systems [17, 18].
        Athena’s proofs have a natural deduction style. Logical sentences can either be asserted into the
    assumption base or proven as theorems using Athena’s deduction tools, with a soundness guarantee
    that any proven theorem is a logical consequence of sentences in the assumption base. Athena per-
    forms automatic sort-checking to prevent ill-sorted expressions in specifications and allows theorems
    to be introduced at an abstract level by encapsulating proofs in parameterized methods, which can
    be instantiated to prove different specializations of the abstract theorems. It defines two syntactic
    categories: an expression, which represents a computation, and a deduction, a logical argument such
    as a proof. A valid deduction always concludes with a sentence, i.e., the conclusion of the proof.
        Sorts form the foundation of Athena’s deductive language, classifying all terms in its sentences.
    Sorts can be defined as domains, structures, and datatypes, each providing different mechanisms for
    constructing elements and each assuming different primitive axioms.
        Domains are sorts that describe the sets of objects to be modeled. A datatype is a special kind
    of domain that is inductively generated, meaning that every element of the domain can be built up
    in a finite number of steps by applying constructors of the datatype. Beyond providing syntactic
    convenience over domains, datatypes can be assumed to follow free-generation axioms for their
    elements, ensuring that different constructor applications create different elements (no-confusion
    axioms), and that every element is represented by some constructor application (no-junk axioms).
        Structures, just like regular datatypes, are inductively generated by their constructors. The only
    difference is that the constructors might not be injective, so that the same constructor applied to
    two distinct sequences of arguments might result in the same value.
        The keyword domain introduces domains in Athena. Listing 1.2 presents a definition for Peano
    numbers based on three domains: Nat, Even, NzNat, with function symbols zero,S,plus, de-
    fined using the declare instruction. Note that, alternatively, Peano numbers can be defined using
    datatypes as: datatype Nat := zero | (s Nat).

1   domains    Nat , Even , NzNat
2   declare    zero :[]          - > Even
3   declare    s:    [ Nat ]     - > NzNat
4   declare    plus :[ Nat Nat ] - > Nat [+]
5   define     [n m]               := [? n : Nat ? m : Nat ]
6   assert     Plus-zero-axiom := ( forall n . ( zero + n ) = n )
7   assert *   Plus-s-axiom        := (( n + ( s m ) ) = ( s ( n + m ) ) )
                                Listing 1.2. Peano example definition using domains.

        The datatype definition provides free-generation axioms, ensuring that different constructor ap-
    plications yield distinct elements. In contrast, the domain based approach offers more expressiveness
    by allowing sort refinements, like Even and NzNat, which enable more precise sort specifications.
    The version using domains is inspired by languages with subsort capabilities, such as Maude, and
    leverages Athena’s many-sorted foundation to provide fine-grained sort control.
        The semantics of Athena defines how phrases F (expressions or deductions) are evaluated within
    an evaluation context, a four-tuple ⟨ρ, β, σ, γ⟩ representing the logical and computational environ-
    ment in which expressions are interpreted, where:
                                            Equational and Inductive Reasoning for Maude in Athena          5

      – ρ is the execution environment, a computable function that maps any given identifier I either
        to a value V or to a special unbound token.
      – β is the assumption base, a finite set of sentences.
      – σ is the store, a computable function that maps any natural number (representing a memory
        location) to a value (the location’s contents) or to a special unassigned token.
      – γ is a set of symbols with their associated signatures, and a collection of sort constructors
        (with arities). γ also includes information on whether a given sort constructor is a datatype or
        structure, and if so, which function symbols are its constructors.
        The result of evaluating a phrase F in an evaluation context ⟨ρ, β, σ, γ⟩ is one of the following:
      1. A pair (V, σ ′ ) consisting of a value V and a store σ ′ , where V is the output of the evaluation
         and σ ′ reflects any side effects accumulated during the evaluation.
      2. A pair consisting of an error message and a store σ ′ , indicating the occurrence of an error during
         the computation.
      3. Nontermination.
         Sentences are added into the assumption base using assert or assert*, where assert* uses im-
     plicit universal quantification for all free variables, before inserting the sentence into the assumption
     base. Lines 6–7 in Listing 1.2 add the properties of Peano numbers into the assumption base.
         Once sentences are introduced into the assumption base, they can be used in deductive reasoning.
     Further, the datatypes and structures definitions allow deductions of theorems that are not derivable
     from the free-generation axioms alone, by using the by-induction method. For example, assuming
     that Nat follows a datatype definition, Listing 1.3 displays the induction proof for the associativity
     property for the plus operator, Line 2.
         In general, the method by-induction requires the proof of the property for all base cases (zero
     in the case of Peano, Lines 5–8) and the proof for all inductive definitions (S for Nat datatype,
     Lines 9–16). Additionally, this induction proof showcases one of the most useful Athena methods:
     chain (Lines 6–8 and Lines 12–16). chain allows equational chaining based proofs, where each step
     is labeled with its justification.

1    define [ p q r ] := [? p : Nat ? q : Nat ? r : Nat ]
2    define plus_associative := ( forall p q r . (( q + r ) + p ) = ( q + ( r + p ) ) )
3    conclude plus_associative
4    by-induction plus_associative {
5       zero = > pick-any q r
6                 (! chain [(( q + r ) + zero )
7                           -- > ( q + r )                [ Plus-zero-axiom ]
8                           < -- ( q + ( r + zero ) ) [ Plus-zero-axiom ])
9       | ( s p ) = > let { induction-hypothesis :=
10                     ( forall ? q ? r . (? q + ? r ) + p = ? q + (? r + p ) ) }
11                pick-any q r
12                (! chain [ (( q + r ) + ( s p ) )
13                          -- > ( s (( q + r ) + p ) )       [ Plus-s-axiom ]
14                          -- > ( s (( q + ( r + p ) ) ) ) [ induction-hypothesis ]
15                          < -- ( q + ( s ( r + p ) ) )      [ Plus-s-axiom ]
16                          < -- ( q + ( r + ( s p ) ) ) ])
17   }
                  Listing 1.3. Deduction of associativity property using datatype induction.
6       M.Sanabria et al.

3     From Maude to Athena

At the heart of the proposed approach, lies the need to translate the order-sorted structure of terms
of an equational theory in Maude to the many-sorted setting of equational theories in Athena.
This section presents such a translation as a function from Maude modules to Athena theories.
Translation of membership (of terms in sorts) is accomplished by using predicates in Athena.


3.1   Strictly Sensible Order-Sorted Signatures

The translation provides a linear translation of strictly sensible algebras to many-sorted algebras [5].
The key idea of the translation is to add an equivalence relation called core equality to the translated
many-sorted structures. By defining this relation, the complexity of translating a strictly sensible
order-sorted algebra to a many-sorted one is reduced and the translated many-sorted algebra equa-
tions only increase by a very small amount of new equations. Algebras definitions are lifted to
signatures to keep the presentation of their results concise.
    Fix a membership signature Σ = (K, F, S), with kinds K, function symbols F , and sorts S, and
a poset (S, ≤) over the sorts. For a function symbol g : s1 × · · · × sn → s, target(g) = s denotes
its result sort. In what follows, assume f, f ′ , f ′′ ∈ F and, for a fixed n ∈ N and si , s′i , s′′i ∈ S for
0 ≤ i < n, where f : s0 × · · · × sn → s ; f ′ : s′0 × · · · × s′n → s′ ; f ′′ : s′′0 × · · · × s′′n → s′′ .
    Argument compatibility captures the idea of overloaded function symbols that can be treated
uniformly as their pair-wise argument positions share a common supersort. Strongly sensible sig-
natures have argument compatible function symbols in which the target sorts are the same.

Definition 1. Two overloaded function symbols f and f ′ are called argument compatible, denoted
ac(f, f ′ ), iff (∀ i | 0 ≤ i ≤ n : si ≡≤ s′i ), where si ≡≤ s′i is a predicate expressing that si
and s′i are in the same connected component of (Σ, ≤). The signature Σ is strongly sensible iff
(∀ f, f ′ | ac(f, f ′ ) : s = s′ ).

   On the other hand, maximal argument-bounding signatures ensure that every function symbol
has a representative among its compatible function symbols, thereby defining one representative for
each class of argument compatible function symbols.

Definition 2. The signature Σ is maximal argument-bounding iff:

                      (∀ f | (∃ f ′′ | (∀ f ′ | ac(f, f ′ ) : (∀ i | 0 ≤ i ≤ n : s′i ≤ s′′i )))).

    A strictly sensible signature is a signature that is both strongly sensible and maximal argument-
bounding. Strictly sensible signatures play a central role in the translation from order-sorted equa-
tional theories in Maude to many-sorted theories in Athena. It rules out ambiguous cases of function
symbol overloading and ensures that the translation remains well-defined and systematic. In con-
trast to more general translations (e.g., [19]), which can produce non-linear or ambiguous mappings
in the presence of unrestricted overloading, requiring strict sensibility guarantees that every func-
tion symbol has a single, consistent representative in the translated signature. In particular, strict
sensibility ensures that each function symbol has a unique representative in the translated signa-
ture, allowing the order-sorted algebra to be flattened into a many-sorted representation without
loss of soundness or consistency.
    In the rest of the paper, it is assumed that any signature Σ is strictly sensible.
                                              Equational and Inductive Reasoning for Maude in Athena        7

  3.2     The Translation Function
  Let E = (Σ, E ∪ A) be a membership equational theory, with signature (K, F, S) and poset of
  sorts (S, ≤), and Ω ⊆ Σ be a constructor subsignature for E. This section defines the map-
  ping E 7→ (β, γ) as the function tr, where β is an Athena assumption base and γ is its symbol
  set. The ρ execution environment and σ store are omitted from the mapping because they are
  orthogonal to the generated Athena representation. The behavior of tr is driven primarily by the
  subsort relation ≤ and by the constructors Ω.
  Definition 3 (Translation Function tr). Let E = (Σ, E ∪ A) be a membership equational theory
  with signature Σ = (K, F, S), sort poset (S, ≤), and constructor subsignature Ω ⊆ Σ. The function
  tr : E → (β, γ) is defined by the following five components:
 (i) Sort translation (trS ). For each sort s ∈ S:
                  (
                    datatype(s, {c ∈ Ω | target(c) = s})              if s ∈
                                                                           / dom(≤) ∪ ran(≤) and ∃ c ∈ Ω.
        trS (s) =
                    domain(s)                                         otherwise
(ii) Function symbol translation (trF ). Let [f ]ac denote the argument compatibility class of
     f ∈ F . For each class [f ]ac , select the maximal representative f ∗ (guaranteed to exist by strict
     sensibility), where f ∗ : s1 × · · · × sn → s, and set
                                γ ∪ f ∗ : [trS (s1 ) · · · trS (sn )] → trS (s) 7→ γ.
                                      

        For each s ≤ s′ in (S, ≤), set
                                              Casts→s′ : [trS (s)] → trS (s′ )
                                          
                                    γ ∪                                            7→ γ.
        Additionally, for each f ∗ : s × s → s in γ with structural attributes in A, let x, y, z be fresh
        variables of sort trS (s) and set
                         ∗ ∗                       ∗   ∗
                                                                                        
                         f (f (x, y), z) = f (x, f (y, z))
                                                                  if assoc ∈ attr(f ), 
                                                                                        
                   β ∪      f ∗ (x, y) = f ∗ (y, x)                if comm ∈ attr(f ),    7→ β.
                         ∗
                                                     ∗
                                                                                        
                            f (trT (e), x) = x, f (x, trT (e)) = x if id : e ∈ attr(f )
                                                                                        

(iii) Term translation (trT ). For each t ∈ TΣ (X):
                                (
                                  x                                      if t = x ∈ X
                      trT (t) =
                                  f ∗ (trT (t1 ), . . . , trT (tn ))     if t = f (t1 , . . . , tn )

     where f ∗ is the maximal representative of [f ]ac and, at each argument position i where the
     subterm has sort s′i with s′i ≤ si and s′i ̸= si , trT (ti ) is wrapped in the appropriate cast chain
     Castsj →sj+1 (· · · (trT (ti )) · · · ) so that the result has sort trS (si ).
(iv) Equation translation (trE ). For each equation l = r in E ∪ A, set
                                                     
                                                β ∪ trT (l) = trT (r) 7→ β.
        For each composable pair s ≤ s′ ≤ s′′ , add the core equality:
                                
                          β ∪ Casts′ →s′′ (Casts→s′ (x)) = Casts→s′′ (x)                    7→ β,
        ensuring all casting paths between the same source and target sorts are identified.
    8        M.Sanabria et al.

    (v) Membership translation (trM ). For each sort s appearing in a membership axiom, set
                                
                            γ ∪ is_s : [trS (kind(s))] → Boolean 7→ γ.
         Then, for each unconditional membership t : s and each conditional membership t : s if P , set
         β ∪ {trM (·)} 7→ β, where:
                     trM (t : s) = is_s(trT (t))     trM (t : s if P ) = (trT (P ) ⇒ is_s(trT (t)))
        The five components of tr interact as a pipeline: trS determines how each sort is represented
    in Athena; trF uses these representations to declare function and cast symbols and to assert the
    structural axioms of A; trT relies on both to translate terms, inserting casts where implicit subsorting
    must become explicit; trE and trM then lift the term translation to equations and membership
    axioms, respectively. To make each step concrete, the rest of this section walks through tr component
    by component on two variants of the Peano numbers specification: the simple module in Listing 1.4
    (no subsort relation) and the richer module in Listing 1.1 (with subsorts NzNat and Even), showing
    the corresponding Athena output in Listing 1.5 and Listing 1.6.



1   fmod PEANO is
2       sort Nat .
3       op zero : -> Nat [ctor] .                       1   module PEANO {
4       op s_ : Nat -> Nat [ctor] .                     2       datatype Nat := zero | ( s Nat )
5       op _+_ : Nat Nat -> Nat .                       3       declare + : [ Nat Nat ] - > Nat
6       vars N M : Nat .                                4       define [ N M ] := [? N : Nat ? M : Nat ]
7       eq N + zero = N .                               5       assert * ( N + zero = N )
8       eq N + s M = s (N + M) .                        6       assert * ( N + s M = s ( N + M ) )
9   endfm                                               7   }
        Listing 1.4. Simple Peano module in Maude.            Listing 1.5. Simple Peano module in Athena.




    Sorts. Through trS , Maude sorts are translated into Athena domains or datatypes. Whenever a
    sort s ∈ S satisfies that it does not appear in the subsort relation ≤ and that there are constructors
    with target sort s, tr translates it to a datatype. In any other case, sorts are translated to domains.
    For instance, zero and s_ in Listing 1.4 are function symbols (with target sort Nat) defined with
    the ctor attribute. Therefore, trS uses their sort signatures to define the corresponding Athena
    datatype, as shown in Line 2 of Listing 1.5. The remaining defined function symbols with target
    sort s are translated with the declare keyword. This is the case for the _+_ function symbol, which
    is translated into Line 3 of Listing 1.5.
        The treatment is different when the sort s is part of the subsort relation, as is the case in
    Listing 1.1. This module introduces NzNat and Even as subsorts of Nat. In this case, the previous
    translation case no longer applies. For sorts related through the subsort relation (NzNat, Even,
    and Nat) the translation function trS instantiates each sort as a plain Athena domain (Line 2 in
    Listing 1.6). The process then proceeds through the four remaining translation components (trF ,
    trT , trE , trM ): (1) function symbols and introducing explicit cast function symbols, (2) terms using
    casting function symbols, (3) equations into Athena assertions using the transformed terms, and
    (4) conditional membership axioms using term translation and predicate introduction.
                                            Equational and Inductive Reasoning for Maude in Athena          9

     Function Symbols. In the simple module (Listing 1.4), no subsort relation exists, so trF declares
     each function symbol directly: _+_ becomes the Athena declaration in Line 3 of Listing 1.5. In the
     richer module (Listing 1.1), the subsorts introduce overloading. The three operators zero, s_, and
     _+_ are grouped by trF into argument compatibility classes; for each class the unique maximal
     representative is selected and declared in γ (Lines 3–5 of Listing 1.6). Additionally, the two subsort
     pairs Even ≤ Nat and NzNat ≤ Nat produce two cast symbols (Lines 6–7 of Listing 1.6).

     Terms and Equations. In the simple module, no subsort relation exists, so trT leaves terms un-
     changed and trE translates each equation directly into an Athena assertion. In the richer module,
     implicit coercions must be made explicit. Consider the first equation in Listing 1.1 (Line 9): be-
     cause the argument has sort Even while the operator expects Nat, trT inserts a cast (Line 9 of
     Listing 1.6). The second equation (Line 10 of Listing 1.1) requires casts on both the argument and
     the result (Line 11 of Listing 1.6). Because the subsort poset of this module has no composable
     triple s ≤ s′ ≤ s′′ , no core equalities are generated; in specifications with longer subsort chains, trE
     would add the corresponding transitivity assertions to β.

     Memberships. Membership judgements have no native counterpart in Athena’s many-sorted logic.
     The component trM bridges this gap by introducing a unary predicate for each sort that appears
     in a membership axiom; the predicate’s domain is the kind of that sort, so it can be applied to
     any term of the right kind. In the richer Peano module, the conditional membership in Line 8 of
     Listing 1.1 is translated into an implication guarded by a membership predicate (Lines 12–13 of
     Listing 1.6). Here, trM chooses the kind of the target sort as the predicate’s domain (i.e., the top-
     most supersort in the connected component). The simple module contains no membership axioms,
     so trM produces no output for it. The complete translation of Listing 1.1 is shown in Listing 1.6.

1    module PEANO {
2      domains NzNat Even Nat
3      declare s : [ Nat ] - > NzNat
4      declare zero : [] - > Even
5      declare + : [ Nat Nat ] - > Nat
6      declare Cast_Even_to_Nat : [ Even ] - > Nat
7      declare Cast_NzNat_to_Nat : [ NzNat ] - > Nat
8      define [ N M ] := [? N : Nat ? M : Nat ]
9      assert * ((+ N ( Cast_Even_to_Nat zero ) ) = N )
10     assert * ((+ N ( Cast_NzNat_to_Nat ( s M ) ) )
11            = ( Cast_NzNat_to_Nat ( s (+ N M ) ) ) )
12     declare is_even : [ Nat ] - > Boolean
13     assert * (( is_even N ) == > ( is_even s s N ) ) }
                                       Listing 1.6. Peano Athena Module

        Finally, the correctness of the translation is stated with respect to equational provability.
     Theorem 1 (Equational Provability). Let E = (Σ, E ∪ A) be a membership equational theory.
     If Σ is strictly sensible and E is sufficiently complete w.r.t. Ω ⊆ Σ, then for any t, u ∈ TΣ,k (X) of
     the same kind k, the following two sentences are equivalent:
     1. t =E u
     2. trT (t) =β trT (u), i.e., trT (t) and trT (u) are provably equal in Athena under the theory tr(E) =
        (β, γ) with the inference rules of many-sorted equational logic.
10      M.Sanabria et al.

Proof. The equational fragment of the translation (components trS , trF , trT , and trE ) instantiates
the strictly sensible order-sorted–to–many-sorted mapping [5]. The membership component trM
introduces predicate symbols and assertions of the form is_s(trT (t)) and trT (P ) ⇒ is_s(trT (t));
because is_s is a predicate symbol, no assertion produced by trM can have the form t′ = u′ for
terms t′ , u′ of a non-Boolean sort, so trM does not introduce new equalities between translated
terms. Hence, the equational content of β is precisely the image of E under trE , the structural
axioms of A under trF , together with the core equalities.

⋄ t =E u ⇒ trT (t) =β trT (u)
  The proof proceeds by structural induction on the derivation of t =E u, case-splitting on the last
  inference rule applied.
  • Axiom instantiation. Suppose t =E u is obtained by applying a substitution θ to an equation
     l = r in E ∪ A, so that t = θ(l) and u = θ(r). By trE , the translated equation trT (l) = trT (r)
     is in β, universally quantified over all free variables. Because trT is defined compositionally
     and the cast insertion at each argument position depends only on the sort of the subterm and
     the expected sort of the position, trT commutes with substitution: for each variable x, define
     θ̂(x) = trT (θ(x)); then trT (θ(t′ )) = θ̂(trT (t′ )) for any term t′ , possibly up to core equalities in
     β that identify different casting paths to the same target sort. Hence, θ̂(trT (l)) =β θ̂(trT (r))
     follows by instantiation of the universally quantified axiom in β.
  • Reflexivity, symmetry, transitivity. These are inference rules of many-sorted equational
     logic and thus hold natively in Athena’s deductive system.
  • Replacement. Suppose t = C[t′ ] and u = C[u′ ] for a context C and t′ =E u′ , and assume
     by the induction hypothesis that trT (t′ ) =β trT (u′ ). The translation trT maps C to a context
     C ′ in the many-sorted signature γ: each function symbol in C is replaced by its maximal
     representative f ∗ , and explicit casts are inserted at every argument position where a subsort
     coercion is needed. Because each cast symbol Casts→s′ is a function symbol in γ, the standard
     congruence rule of many-sorted equational logic guarantees that if a =β b then Casts→s′ (a) =β
     Casts→s′ (b). Moreover, if t′ and u′ require different casting chains to reach the expected sort of
     the hole in C ′ , the core equalities (added by trE for every composable pair s ≤ s′ ≤ s′′ ) ensure
     that both chains yield equal results in β. Hence, trT (C[t′ ]) = C ′ [trT (t′ )] =β C ′ [trT (u′ )] =
     trT (C[u′ ]) by congruence in many-sorted equational logic.
  Since every inference rule used in the derivation of t =E u is preserved, trT (t) =β trT (u).
⋄ trT (t) =β trT (u) ⇒ t =E u
  It suffices to show that β is a conservative extension of the image of E ∪ A with respect to
  equalities between translated terms. The axioms of β fall into three classes:
  (a) translated equations trT (l) = trT (r) for each l = r in E ∪ A;
  (b) core equalities Casts′ →s′′ (Casts→s′ (x)) = Casts→s′′ (x) for every composable pair s ≤ s′ ≤ s′′ ;
  (c) membership assertions produced by trM .
  As argued above, class (c) consists entirely of Boolean-sorted sentences and cannot produce new
  equalities between non-Boolean terms.
  For classes (a) and (b), the argument proceeds as follows:
  • Unambiguous operator mapping. Strict sensibility guarantees that each argument com-
     patibility class [f ]ac has a unique maximal representative f ∗ . The translation maps every f
     in the same class to the same f ∗ and omits all others. Because the selection is unique, no
     two originally distinct function symbols are merged by the translation, therefore no invalid
     equalities between terms arise from the operator mapping.
                                         Equational and Inductive Reasoning for Maude in Athena          11

    • Conservative cast equalities. Each cast symbol Casts→s′ is a fresh uninterpreted function
      symbol in γ, distinct for each pair s < s′ . The only axioms governing cast symbols are the
      core equalities in class (b), which encode the transitivity and path independence of the subsort
      relation. Because the subsort relation ≤ is already part of E, the core equalities do not identify
      terms that are not already related by subsorting.
    • Isomorphism of initial algebras. According to Li et al. [5], the strictly sensible mapping
      combined with the core casting equalities induces a bijection between the equivalence classes of
      the initial order-sorted algebra TΣ/(E∪A) and those of the initial many-sorted algebra Tγ/βeq ,
      where βeq denotes the equational part of β (classes (a) and (b)). The sufficient completeness
      assumption ensures that every ground term reduces to a constructor term, which is needed for
      the bijection to be an isomorphism of algebras.
    Therefore, if trT (t) =β trT (u), then trT (t) and trT (u) lie in the same equivalence class of Tγ/βeq .
    By the isomorphism, t and u belong to the same class in TΣ/(E∪A) , i.e., t =E u.


4     Inductive Reasoning

The translation function tr from (Σ, E ∪ A) to (β, γ) presented in Section 3 enables equational
reasoning over Maude specifications within Athena by preserving the underlying equational theory
in a many-sorted first-order logic setting. However, equational reasoning alone is often insufficient
to establish properties of interest, which typically require some form of inductive reasoning. This
section explains how equational reasoning with tr(E) in Athena can be extended with inductive
reasoning based on parametric induction principles. The key idea is that for the induction principle
to be applied, it must be instantiated using the structure of sorts in Σ associated with each con-
nected component in the poset (S, ≤). To illustrate this approach, this section presents a concrete
instantiation of such a parametric induction principle, showing how structural induction can be
recovered and applied in practice.
    In Athena, there is native support for structural, constructor-based induction over datatypes,
which allows properties to be proved by reasoning directly on the inductive structure generated by
datatype constructors. However, the translation function tr systematically represents many Maude
sorts as domains, rather than datatypes, in order to preserve the structure induced by subsorting in
the many-sorted setting of Athena. As a consequence, Athena’s built-in induction mechanisms are
no longer directly applicable, and native datatype induction is insufficient for reasoning about the
translated specifications. To address this limitation, the approach adopted here is to equip Athena
with induction principles defined over domains, rather than relying solely on datatype induction.
These principles are formulated in a parametric way, allowing different induction schemes to be
instantiated depending on the structure of the sorts under consideration. In particular, this includes
natural extensions of Athena’s native structural induction to domains that arise from translated
equational specifications.
    More generally, an induction principle in this setting is realized by declaring a primitive method
in Athena that explicitly encodes both the basis cases and the inductive cases associated with a
given sort structure (S, ≤). For a selected induction principle η, the primitive method is defined
separately for each connected component of the sort hierarchy, reflecting the constructors and
subsort relations that characterize that component. The basis cases correspond to the minimal
elements or constructors of the component, while the inductive cases capture how the property is
preserved by the relevant constructor applications. Once declared, such a primitive method can
 12       M.Sanabria et al.

 be applied uniformly to predicates over the corresponding domain, thereby extending equational
 reasoning with inductive reasoning in a principled and modular way.
      The following definition extends the translation function (Definition 3) with a sixth component,
 trη , that formalizes the generation of structural induction principles. It operates on the execution
 environment ρ—previously noted as orthogonal to the generated representation (β, γ), but now
 required to host the primitive methods that realize induction.
 Definition 4 (Induction Method Translation trη ). Let E, Σ, Ω, and (S, ≤) be as in Defini-
 tion 3. The translation function tr is extended with:

(vi) Induction method translation (trη ). For each kind k in (S, ≤), let C = { s ∈ S | ∃ c ∈
     Ω. target(c) = s } ∩ [k]≤ be the set of sorts in the connected component of k that are directly
     generated by Ω-constructors. Define the effective constructor set
                               +
                              ΩC                       / C, s′ ∈ C, s ≤ s′ },
                                 = ΩC ∪ { Casts→s′ | s ∈

      where ΩC = {c ∈ Ω | target(c) ∈ C} and the second component adds subsort injection casts
                                                      +
      from sorts outside C into C. By construction, ΩC  is jointly exhaustive: every constructor normal
                                                        +                                         +
      form of kind k is headed by some element of ΩC      . For each c : s1 × · · · × sn → s in ΩC  , let
      Ic = { i | 1 ≤ i ≤ n, si ∈ C } be the set of recursive argument positions. The component
      trη generates a primitive method that takes a predicate P : trS (k) → Boolean and encodes the
      obligations of ηC (P ) as follows.
      (a) Base-case sentences.
                                            +
          (1) For each constant c :→ s in ΩC   (0-arity, so Ic = ∅), define
                                                                     
                                              bc := P Casts→k (c) .
                                                               +
          (2) For each constructor c : s1 × · · · × sn → s in ΩC with n ≥ 1 and Ic = ∅, define
                                                                                       
                                  bc := ∀ x1 · · · xn . P Casts→k (c(x1 , . . . , xn )) ,

              where each xi : trS (si ).
                                                                                           +
      (b) Inductive-case sentences. For each constructor c : s1 × · · · × sn → s in ΩC        with Ic ̸= ∅,
          define the sentence
                                         ^                                                     
                   hc := ∀ x1 · · · xn .    P Castsi →k (xi )    ⇒ P Casts→k (c(x1 , . . . , xn )) ,
                                        i∈Ic

          where each xi : trS (si ). When |Ic | = 1, the conjunction reduces to a single hypothesis.
      (c) Primitive method assembly. Let B = {bc } and H = {hc } be the collected base-case and
          inductive-case sentences, and let (o1 , . . . , om ) be an enumeration of all sentences in B ∪ H.
          The primitive method for component C is added to the execution environment ρ as
                            
                      ρ ∪ prim-methodC (P ) : checkm ⇒ ∀ x : trS (k). P (x) 7→ ρ,

          where each obligation is verified sequentially through nested check expressions: check1 tests
          holds?(o1 ) and, upon success, enters check2 , which tests holds?(o2 ), and so on. In general,
          for i = 1, . . . , m, checki tests holds?(oi ) and proceeds to checki+1 ; when i = m, the
          innermost check concludes ∀ x : trS (k). P (x). If any holds?(oi ) fails, the method signals an
          error.
                                            Equational and Inductive Reasoning for Maude in Athena            13

        The full translation thus maps E 7→ (β, γ, ρ), extending the original pair with the execution
        environment populated by the generated primitive methods.
        As an example, consider the primitive method in Listing 1.7. It defines nat-induction, a struc-
    tural induction principle for the Nat domain in Listing 1.6. It explicitly captures the two components
    of a standard induction proof. The first definition, labeled basis, corresponds to the sentence of
    the basis case over the constant constructor Cast_Even_to_Nat zero. The second definition, la-
    beled ic, encodes the inductive case: it states that if the property holds for an arbitrary Nat
    element x (inductive hypothesis), then it needs to hold for its successor, Cast_NzNat_to_Nat (s
    x). The check expression enforces both conditions. It first verifies that the basis case holds, and if
    so, proceeds to check the inductive case. This mechanism effectively restores structural induction
    for domains translated from Maude datatypes, allowing the proof of properties such as associativity
    or commutativity complementing the built-in by-induction method.

1   primitive-method ( nat-induction property ) :=
2     let {
3       basis := ( property ( Cast_Even_to_Nat zero ) ) ;
4       ic := ( forall x ( if ( property x ) ( property ( Cast_NzNat_to_Nat ( s x ) ) ) ) )
5       }
6       check { ( holds ? basis ) = >
7                  check {( holds ? ic ) = > ( forall x ( property x ) )
8                         | else = > ( error " Inductive step does not hold . " ) }
9                  | else = > ( error " Basis step does not hold . " ) }
                                Listing 1.7. Primitive induction method for Nat.

        The following theorem establishes the soundness of inductive proofs carried out using the prim-
    itive methods generated by trη .
    Theorem 2 (Soundness of Inductive Proofs). Let E = (Σ, E ∪ A) be a membership equational
    theory that is sufficiently complete a connected component of (S, ≤) with kind k, and P : trS (k) →
    Boolean a predicate. If the primitive method prim-methodC (P ) generated by trη (Definition 4)
    checks all base cases and inductive steps and concludes ∀ x : trS (k). P (x), then for every ground term
    t of sort s ∈ C in TΣ,k , the property P (trT (t)) holds in Athena under the theory tr(E) = (β, γ, ρ).
    Proof. Assume, for contradiction, that there exists a ground term t of sort s ∈ C in TΣ,k such
    that P (trT (t)) does not hold, even though all obligations of prim-methodC (P ) have been checked.
    Because E is sufficiently complete, t reduces to a constructor normal form headed by some c ∈ Ω
                                                                                                  +
    with target(c) in the connected component of k. If target(c) ∈ C, then c ∈ ΩC ⊆ ΩC              ; otherwise c
                                                                     ′         ′
    is an injection from an external sort s ∈        / C with s ≤ s for some s ∈ C, so c = Casts→s′ belongs
                                          +                       +
    to the second component of ΩC           . In either case c ∈ ΩC . By Theorem 1, P (trT (t)) holds if and only
    if P holds on the translated normal form, so it may be assumed without loss of generality that
    t = c(t1 , . . . , tn ) is already in constructor normal form. It proceeds by induction on the number of
    constructor applications in t.
    Base case: (Ic = ∅). The constructor c has no argument positions of sorts in C, so t contains
    exactly one constructor application. The primitive method verified the base-case sentence bc (Def-
    inition 4). Whether c :→ s is a constant (in which case bc directly asserts P (Casts→k (c))) or
    c : s1 × · · · × sn → s with n ≥ 1 and Ic = ∅ (in which case bc is universally quantified and
    instantiates at trT (t1 ), . . . , trT (tn )) the verified sentence bc yields P (trT (t)).
     14        M.Sanabria et al.

     Inductive step: (Ic ̸= ∅). For each i ∈ Ic , the subterm ti is a ground term of sort si ∈ C with
     strictly fewer constructor applications than t. By the induction hypothesis, P (trT (ti )) holds for every
     i ∈ Ic . The primitive method verified the inductive-case sentence hc (Definition 4), which asserts
     that the conjunction of P (Castsi →k (xi )) for i ∈ Ic implies P (Casts→k (c(x1 , . . . , xn ))). Instantiating
     at trT (t1 ), . . . , trT (tn ) and applying modus ponens with the induction hypotheses yields P (trT (t)).

     In both cases P (trT (t)) holds, contradicting the assumption. Since t was arbitrary, P (trT (t)) holds
     for every ground term of kind k.


     5      Case Study

     The case study verifies inductive properties of a compiler for numeric expressions on a Stack Ma-
     chine [4]. The case study relies heavily on order-sorted features of data types and includes structural
     axioms.5 Listing 1.8 shows the Maude specification, defining three sorts: a source language of arith-
     metic expressions (Exp), a target instruction set (Instr/Program), and a stack machine (Stack).
1    fmod TOY-COMPILER is
2      protecting INT .
3      sort Exp .
4      subsort Int < Exp .
5      op _plus_ : Exp Exp -> Exp [ctor] .
6      op _minus_ : Exp Exp -> Exp [ctor] .
7      op _mult_ : Exp Exp -> Exp [ctor] .
8      sorts Instr Program Stack .
9      subsort Instr < Program .
10     op push : Int -> Instr [ctor] .
11     ops add sub mult : -> Instr [ctor] .
12     op nil : -> Program [ctor] .
13     op _++_ : Program Program -> Program [ctor assoc id: nil] .
14     op empty : -> Stack [ctor] .
15     op _::_ : Int Stack -> Stack [ctor] .
16     op I : Exp -> Int .          --- interpreter
17     op compile : Exp -> Program .
18     op exec : Program Stack -> Stack .
19     vars N N1 N2 : Int . vars E1 E2 : Exp .
20     var P : Program .     var S : Stack .
21     eq I(N) = N .
22     eq I(E1 plus E2) = I(E1) + I(E2) .
23     --- I equations for minus, mult analogous
24     eq compile(N) = push(N) .
25     eq compile(E1 plus E2) =
26        compile(E2) ++ compile(E1) ++ add .
27     --- compile equations for minus, mult analogous
28     eq exec(nil, S) = S .
29     eq exec(push(N) ++ P, S) = exec(P, N :: S) .
30     eq exec(add ++ P, N1 :: N2 :: S) =
     5
          The complete Maude specification of the compiler with the translated equationally equivalent Athena
          program (with proofs) is available at: https://github.com/FLAGlab/Maude2Athena
                                           Equational and Inductive Reasoning for Maude in Athena        15

31        exec(P, (N1 + N2) :: S) .
32     --- exec equations for sub, mult analogous
33     ...
34   endfm
                                 Listing 1.8. Toy compiler in Maude (shorten).

         The compiler specification relies on two order-sorted features. First, Int < Exp lets integers ap-
     pear directly as expressions without an explicit injection constructor. Second, Instr < Program lets
     single instructions be used where programs are expected. The operator _++_ carries the structural
     axioms assoc and id: nil.
         To preserve the semantics of Int < Exp, the translation introduces explicit cast functions for
     every subsort relation in the sort poset, as explained in Section 3. maude2athena automatically
     inserts these casts. For example, the equations in lines Line 24 and Line 29 are translated to:

          declare  push : [ Int ] - > Instr
          declare  compile : [ Exp ] - > Program
          declare  Cast_Int_to_Exp : [ Int ] - > Exp
          declare  Cast _Inst r_to_P rogram : [ Instr ] - > Program
          assert * eq_4 := (( compile ( Cast_Int_to_Exp N ) )
                                 = ( C ast_I nstr_t o_Pro gram ( push N ) ) )
          assert * eq_9 := (( exec (++ ( Ca st_In str_to _Prog ram ( push N ) ) P ) S )
                                 = ( exec P (:: N S ) ) )

        Since Athena requires unique function symbols and does not support Maude’s mixfix notations
     natively, the tool flattens operators and resolves overloading. Specifically, the mixfix Maude operator
     _plus_ is translated to a standard prefix function in Athena. If overloading collisions are detected,
     unique identifiers are generated based on sort signatures:

          declare plus : [ Exp Exp ] - > Exp
          declare ++ : [ Program Program ] - > Program
          assert * (( compile ( plus E1 E2 ) ) =
                     (++ ( compile E2 )
                           (++ ( compile E1 ) ( Ca st_In str_to _Prog ram add ) ) ) )
          define [ _v1 _v2 _v3 _v4 ] :=
                  [? _v1 : Program ? _v2 : Program ? _v3 : Program ? _v4 : Program ]
          assert * assoc_ ++ := ((++ (++ _v1 _v2 ) _v3 ) = (++ _v1 (++ _v2 _v3 ) ) )
          assert * left_id_ ++ := ((++ nil _v4 ) = _v4 )
          assert * right_id_ ++ := ((++ _v4 nil ) = _v4 )

     This listing also illustrates how the structural axioms A are handled. The operator _++_ is declared
     with the attributes assoc, id: nil, meaning that rewriting is performed modulo associativity and
     identity. Because Athena has no built-in support for such axioms, trF translates each structural
     axiom into an explicit equational assertion: assoc_++ encodes associativity, while left_id_++ and
     right_id_++ encode the left and right identity axioms for nil. In general, any combination of
     associativity, commutativity, and identity (ACU) attributes attached to operators in A is translated
     by trF into the corresponding set of universally quantified assertions in β.
        The tool analyzes the signature to determine which sorts can be modeled as datatypes (allowing
     native induction) and which must be domains. In this example, the Maude Stack is translated as
     an Athena datatype:
16        M.Sanabria et al.

        datatype Stack := empty | (:: Int Stack )

However, Exp and Program are translated as domains to accommodate the subsorting relations that
are otherwise incompatible with standard datatype constructors.
    The result of this translation is a fully typed Athena module where the correctness of the compiler
(forall e . (exec (compile e)) = (I e)) can be rigorously proven. The core verification goal
is the following theorem, which asserts that compiling an expression e followed by a program p is
equivalent to executing p on a stack with the evaluated result of e:6

        ( forall ? p ? s .        ( exec (++ ( compile ? e ) ? p ) ? s ) =
                                  ( exec ? p (:: ( I ? e ) ? s ) ) )

    Note that this sentence cannot be asserted as a logical sentence because Exp is a domain, not
a datatype. Instead, it is defined as a predicate over expressions. This enables the theorem to be
passed as an argument to the induction method of choice. In this case, the predicate correctness
is defined as:

        declare correctness : [ Exp ] - > Boolean
        assert * correctness_def := ( iff ( correctness ? e )
            ( forall ? p ? s .
                 ( exec (++ ( compile ? e ) ? p ) ? s ) = ( exec ? p (:: ( I ? e ) ? s ) ) ) )

   Proving that (forall ?e . correctness ?e) holds, brings to attention the challenges of rea-
soning over non-inductive domains and handling explicit subsorting.
   Note that in Maude, Exp is defined via subsorting (Int < Exp), which prevents it from being
translated into a standard Athena datatype. Consequently, Athena’s native by-induction method
cannot be applied. To overcome this, maude2athena automatically generates a custom primitive
method that reconstructs the inductive principle of the original Maude sort. The generated method,
exp-induction, takes the correctness predicate as an argument and strictly enforces that the user
proves the inductive step for every constructor (e.g., plus, mult) before discharging the goal:

primitive-method ( exp-induction property ) :=
    let {
        basis_n := ( forall ? n ( property ( Cast_Int_to_Exp ? n ) ) )
        ic_plus := ( forall ? e1 ( forall ? e2
                          ( if ( and ( property ? e1 ) ( property ? e2 ) )
                               ( property ( plus ? e1 ? e2 ) ) ) ) ) ;
        ic_minus := ...
        ic_mult := ...
    }
    check { ( holds ? basis_n ) = >    ... }

    The translation replaces implicit subsorting with explicit cast operators. This requires the proof
script to handle these casts in the basis cases. For instance, the basis case for integers is not
merely forall n, but rather forall n applied to the cast Cast_Int_to_Exp. The proof proceeds
by unwrapping these casts using the axioms generated by the translation (e.g., eq_4):
6
     The correctness property follows trivially as a corollary of this theorem by instantiating it to the empty
     program on an empty stack.
                                      Equational and Inductive Reasoning for Maude in Athena        17

define basis_step := ( forall n . correctness ( Cast_Int_to_Exp n ) )
conclude basis_step
  pick-any n : Int p : Program s : Stack
    (! chain [ ( exec (++ ( compile ( Cast_Int_to_Exp n ) ) p ) s )
             = ( exec (++ ( Cast _Instr _to_P rogram ( push n ) ) p ) s ) [ eq_4 ]
             = ( exec p (:: n s ) )                                       [ eq_9 ]
             ... ])

    This explicit handling ensures that the proof is rigorous and mathematically consistent with
the original order-sorted semantics. Finally, the proof is concluded by invoking the custom induc-
tion method, which aggregates the base case and inductive steps to discharge the main theorem:
(!exp-induction correctness).

6   Related Work
The formal verification of rewriting logic specifications typically involves a trade off between the
high performance execution provided by environments like Maude and the interactive deductive
capabilities of theorem provers like Athena [4], Isabelle [20], or Lean [21]. There are three main
methodologies designed to address this challenge: (1) the development of native domain-specific
theorem provers, (2) the application of automated symbolic reasoning techniques, and (3) the
integration with general purpose proof assistants via translation.
    The native approach, pioneered by the original Maude Inductive Theorem Prover (ITP) [2] and
modernized by NuITP [22], offers powerful automation using variant-based reasoning directly at
Maude’s metalevel. While highly effective for discharging goals automatically without translation,
tools like NuITP inherently generate proofs as metalevel search traces. In contrast, maude2athena
translates specifications into Athena to leverage its natural-deduction framework, which closely mir-
rors standard mathematical reasoning [13]. Rather than competing on pure automation, the pro-
posed approach emphasizes proof transparency and structure. Athena’s built-in methods (equality
chaining, structural induction, case analysis, and many others) allow proofs to be developed and
read as structured mathematical arguments rather than execution traces or low-level tactic scripts,
following human-like proof strategies [23]. Consequently, maude2athena occupies a complementary
niche to native provers like NuITP: it targets verification scenarios where transparent, independently
checkable, and human-readable proofs are the primary requirement.
    A highly effective alternative to interactive deduction relies on automated symbolic methods.
Maude integrates with SMT solvers to discharge proof obligations generated from specifications.
Furthermore, techniques such as narrowing and its combination with SMT solving allow for the
analysis of infinite state systems [24]. Reachability Logic and its associated tools also provide mech-
anisms to deductively reason about Maude programs [25, 26]. These automated methodologies are
essential for verifying safety properties and analyzing state spaces, though they may not cover
properties requiring complex inductive arguments or higher order reasoning.
    The third strategy is to translate specifications to an external formalism to leverage its proof
infrastructure. The Heterogeneous Tool Set (Hets) [27] treats Maude as an institution, enabling
translations to Isabelle/HOL via CASL [28]. While theoretically robust, this path relies on complex
encodings to simulate subsorting. Similarly, approaches to translate order-sorted algebras into many-
sorted algebras have been explored to leverage standard theorem provers [5, 6]. The Maude2Lean
framework [29] presents a direct translation from rewriting logic to the calculus of inductive con-
structions. Unlike the institutional approach of Hets, Maude2Lean translates the syntax of Maude
18      M.Sanabria et al.

terms and the semantics of rewriting logic into inductive datatypes in Lean. This preserves the
inductive structure of the logic, allowing native structural induction on terms and relations. How-
ever, such translations shift the first-order theorem proving problem to a different domain (e.g.,
type theory or higher order logic), sometimes incurring in a verbosity trade-off, as proofs become
arguments about the translated semantics rather than direct reasoning about the domain model.


7    Concluding Remarks
This work presents maude2athena, a tool for translating order-sorted Maude specifications into the
many-sorted first-order logic of Athena. The main contribution of this work is the reconciliation
of symbolic reasoning and equational rewriting with the power of inductive reasoning, enabling
specifications that leverage the best of both worlds. To the best of the authors’ knowledge, this is the
first implementation grounded in the theoretical translation proposed by Li et al. [5]. The proposed
approach bridges the semantic gap between the two formalisms by making subsorting explicit via
cast operators, modeling membership as predicates, and recovering structural induction through
custom primitive methods. The maude2athena framework was validated using several examples. It
includes the case study of a compiler specification, demonstrating the approach’s ability to handle
deep inductive structures and operator overloading, while preserving the equational consistency of
the original system.
    The future work focuses on two key areas. First, to enhance modularity by mapping Maude’s
built-in modules directly to Athena’s native domains. Such integration would allow developers to
leverage Athena’s existing decision procedures and automated reasoning capabilities for standard
data types. Second, extending maude2athena to handle rewrite rules to enable the verification of
concurrent and distributed systems. The current version is restricted to functional modules, while
rewrite rules are the primary mechanism for defining concurrent state transitions. Athena, being
grounded in standard first-order logic, lacks native primitives for modeling the non-determinism
and asynchrony inherent in such rules. Rather than constructing a new concurrency framework
within Athena from scratch, the idea is to directly work on top of Talcott’s formalization of Actor
theories in rewriting logic [30]. By translating these pre-validated semantic structures directly into
Athena, Maude’s system modules can be mapped to logical transition relations. On the one hand,
this would significantly reduce the formalization burden. On the other hand, it will effectively equip
Athena with the capability to reason about temporal properties and distributed protocols without
needing to manually reconstruct the underlying theory of concurrency.

Acknowledgements. The authors would like to thank the anonymous reviewers for their very in-
sightful comments on an earlier version of this paper. They would like to also thank Konstantine
Arkoudas for his insight on encoding structural induction over plain domains as a primitive method
in Athena to preserve the inductive reasoning capabilities. Rocha acknowledges support from the
SGR project PROMUEVA (BPIN 2021000100160) under the supervision of Minciencias (Ministerio
de Ciencia Tecnología e Innovación, Colombia).


References
 1. Meseguer, J.: Conditional rewriting logic as a unified model of concurrency. Theoretical com-
    puter science (1992)
                                      Equational and Inductive Reasoning for Maude in Athena        19

 2. Clavel, M., Durán, F., Eker, S., Lincoln, P., Martí-Oliet, N., Meseguer, J., Talcott, C.: All about
    Maude-a high-performance logical framework: how to specify, program, and verify systems in
    rewriting logic. Springer (2007)
 3. Clavel, M., Meseguer, J., Palomino, M.: Reflection in membership equational logic, many-sorted
    equational logic, Horn logic with equality, and rewriting logic. Theoretical Computer Science
    (2007)
 4. Arkoudas, K., Musser, D.: Fundamental proof methods in computer science: a computer-based
    approach. MIT Press (2017)
 5. Li, L., Gunter, E.L.: A Method to Translate Order-Sorted Algebras to Many-Sorted Algebras.
    In: Fourth International Workshop on Rewriting Techniques for Program Transformations and
    Evaluation. EPTCS, pp. 20–34 (2017)
 6. Goguen, J.A., Meseguer, J.: Order-sorted algebra I: Equational deduction for multiple inheri-
    tance, overloading, exceptions and partial operations. Theoretical Computer Science (1992)
 7. Rocha, C., Meseguer, J.: Constructors, Sufficient Completeness, and Deadlock Freedom of
    Rewrite Theories. In: Logic for Programming, Artificial Intelligence, and Reasoning, pp. 594–
    609. Springer (2010)
 8. Bouhoula, A., Jouannaud, J.-P., Meseguer, J.: Specification and proof in membership equational
    logic. Theoretical Computer Science (2000)
 9. Meseguer, J.: Membership algebra as a logical framework for equational specification. In: Recent
    Trends in Algebraic Development Techniques, pp. 18–61. Springer (1998)
10. Durán, F., Meseguer, J.: On the Church-Rosser and coherence properties of conditional order-
    sorted rewrite theories. The Journal of Logic and Algebraic Programming (2012)
11. Lucas, S., Meseguer, J.: Operational termination of membership equational programs: the order-
    sorted way. Electronic Notes in Theoretical Computer Science (2009)
12. Arkoudas, K.: Denotational proof languages. PhD thesis, Massachusetts Institute of Technology
    (2000).
13. Arkoudas, K.: Simplifying Proofs in Fitch-Style Natural Deduction Systems. Journal of Auto-
    mated Reasoning (2005)
14. Manzano, M.: Extensions of first-order logic. Cambridge University Press (1996)
15. Musser, D.R., Varela, C.A.: Structured Reasoning About Actor Systems. In: Proceedings of the
    2013 Workshop on Programming Based on Actors, Agents, and Decentralized Control. AGERE!
    2013, pp. 37–48. ACM, Indianapolis, Indiana, USA (2013)
16. Varela, C.A.: “The AMST Language: Formal Verification and Execution of Actor Systems”. In:
    Concurrent Programming, Open Systems and Formal Methods: Essays Dedicated to Gul Agha
    to Celebrate His Scientific Career. Cham: Springer Nature Switzerland, 2026, pp. 36–59.
17. Paul, S., McCarthy, C., Patterson, S., Varela, C.: Formal verification of timely knowledge prop-
    agation in airborne networks. Science of Computer Programming (2025)
18. Paul, S., Cruz, E., Dutta, A., Bhaumik, A., Blasch, E., Agha, G., Patterson, S., Kopsaftopoulos,
    F., Varela, C.: Formal Verification of Safety-Critical Aerospace Systems. IEEE Aerospace and
    Electronic Systems Magazine (2023)
19. Meseguer, J., Skeirik, S.: Equational formulas and pattern operations in initial order-sorted
    algebras. Form. Asp. Comput. (2017)
20. Wenzel, M., Paulson, L.C., Nipkow, T.: The Isabelle framework. In: International Conference
    on Theorem Proving in Higher Order Logics, pp. 33–38 (2008)
21. Moura, L.d., Ullrich, S.: The Lean 4 theorem prover and programming language. In: Interna-
    tional Conference on Automated Deduction, pp. 625–635 (2021)
20     M.Sanabria et al.

22. Durán, F., Escobar, S., Meseguer, J., Sapiña, J.: NuITP: An inductive theorem prover for
    equational program verification. In: International Symposium on Principles and Practice of
    Declarative Programming, pp. 1–11 (2024)
23. Bringsjord, S., Govindarajulu, N.S.: Fundamental Proof Methods in Computer Science: A
    Computer-Based Approach, by Arkoudas and Musser, The MIT Press, Cambridge, USA, ISBN
    978-0-262-03553-8. Theory and Practice of Logic Programming (2021)
24. Rocha, C., Meseguer, J., Muñoz, C.: Rewriting modulo SMT and open system analysis. In:
    International Workshop on Rewriting Logic and its Applications, pp. 247–262 (2014)
25. Romero, M., Rocha, C.: Symbolic Execution and Reachability Analysis Using Rewriting Modulo
    SMT for Spatial Concurrent Constraint Systems with Extrusion. In: NASA Formal Methods,
    pp. 435–451. Springer (2018)
26. Arias, J., Bae, K., Olarte, C., Ölveczky, P.C., Petrucci, L., Rømming, F.: Symbolic analysis
    and parameter synthesis for time Petri nets using Maude and SMT solving. In: International
    Conference on Applications and Theory of Petri Nets and Concurrency, pp. 369–392 (2023)
27. Codescu, M., Mossakowski, T., Riesco, A., Maeder, C.: Integrating Maude into HETS. In:
    International Conference on Algebraic Methodology and Software Technology, pp. 60–75 (2010)
28. Astesiano, E., Bidoit, M., Kirchner, H., Krieg-Brückner, B., Mosses, P.D., Sannella, D., Tarlecki,
    A.: CASL: the common algebraic specification language. Theoretical Computer Science (2002)
29. Rubio, R., Riesco, A.: Maude2Lean: Theorem proving for Maude specifications using Lean.
    Journal of Logical and Algebraic Methods in Programming (2022)
30. Talcott, C.: Actor theories in rewriting logic. Theoretical Computer Science (2002)
