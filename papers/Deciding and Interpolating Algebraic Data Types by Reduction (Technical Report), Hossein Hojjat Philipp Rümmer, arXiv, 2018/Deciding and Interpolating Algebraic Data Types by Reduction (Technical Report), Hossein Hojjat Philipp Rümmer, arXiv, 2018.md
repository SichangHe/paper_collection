                                         Deciding and Interpolating Algebraic Data Types by Reduction (Technical Report)


                                                                        Hossein Hojjat                                            Philipp Rümmer
                                                               Department of Computer Science                            Department of Information Technology
                                               Rochester Institute of Technology, Rochester, NY, United States           Uppsala University, Uppsala, Sweden



                                           Abstract—Recursive algebraic data types (term algebras,         that constructors are free. EUF takes care of upward and
                                        ADTs) are one of the most well-studied theories in logic, and      downward closure, while cycle detection and constructor
                                        find application in contexts including functional programming,
arXiv:1801.02367v1 [cs.LO] 8 Jan 2018




                                                                                                           testers are handled by LIA constraints. The reduction can be
                                        modelling languages, proof assistants, and verification. At this
                                        point, several state-of-the-art theorem provers and SMT solvers    implemented with little effort, and is widely applicable since
                                        include tailor-made decision procedures for ADTs, and ver-         EUF and LIA are supported by virtually all SMT solvers,
                                        sion 2.6 of the SMT-LIB standard includes support for ADTs.        and increasingly also by other theorem provers. Reduction
                                        We study an extremely simple approach to decide satisfiability     to EUF+LIA has a few further advantages, in particular it
                                        of ADT constraints, the reduction of ADT constraints to            is possible to reuse existing, highly optimised EUF+LIA
                                        equisatisfiable constraints over uninterpreted functions (EUF)
                                        and linear integer arithmetic (LIA). We show that the reduction    simplifiers in solvers, and to compute interpolants using
                                        approach gives rise to both decision and Craig interpolation       EUF+LIA interpolation procedures.
                                        procedures in (extensions of) ADTs.                                   The contributions of the paper are (i) definition and
                                          Keywords-Decision procedures; Craig interpolation; alge-         correctness proof of the reduction from ADTs to EUF+LIA;
                                        braic data types; term algebras                                    (ii) discussion of Craig interpolation for ADTs; (iii) exten-
                                                                                                           sion to ADTs with size constraints, and an effective charac-
                                                              I. I NTRODUCTION                             terisation of the ADTs for which the resulting procedure is
                                           Recursive algebraic data types (ADTs) with absolutely           complete. The procedures discussed in the paper have been
                                        free constructors are increasingly supported by SMT solvers,       implemented in the P RINCESS theorem prover [14].1
                                        and find application in a variety of areas, including func-
                                        tional programming, modelling languages, proof assistants,         A. Related Work
                                        and verification. In solvers, ADTs are usually implemented
                                        as native theory solvers [2], [12], [13], [17] that apply                ADT Solving: While ADTs have only recently been
                                        congruence closure (upward closure), syntactic unification         standardised in the SMT-LIB, some solvers (including
                                        (downward closure), cycle detection (occurs-check), and in         STeP [11], CVC3 [3], CVC4 [1], and Z3 [7]) have for a
                                        additional handle selectors and testers in order to decide         while supported ADTs through native decision procedures
                                        satisfiability of quantifier-free ADT formulas.                    extending the congruence closure algorithm [2], [12], [13].
                                           In this paper, we study a simple alternative approach to        Native solvers offer excellent performance, but also require
                                        ADT reasoning, based on the reduction of ADT formulas              significant implementation effort. The listed solvers do not
                                        to equisatisfiable formulas over uninterpreted functions and       support Craig interpolation or formulas with size constraints.
                                        linear integer arithmetic (EUF+LIA). Our approach is partly           Satisfiability of ADT formulas can also be checked by
                                        inspired, besides by eager SMT in general, by the reduction        introducing explicit axioms about the constructors and selec-
                                        approach from [10], in which quantifier-free formulas are          tors. Since ADTs form a local theory [16], the set of required
                                        mapped to simpler theories for the purpose of checking satis-      instances of the axioms can effectively be computed, and a
                                        fiability and computing interpolants. For instance, as shown       decision procedure for ADT satisfiability is obtained.
                                        in [10], the theory of sets with finite cardinality constraints       Our reduction-based approach sits in between native
                                        can be reduced to the theory of equality with uninterpreted        solvers and methods based on explicit axioms. Like with ex-
                                        functions (EUF). Like in [10], the target theories of our          plicit axioms, our method leaves most of the heavy work to
                                        ADT reduction are EUF and linear arithmetic. Unlike [10],          other theory solvers (EUF and LIA), and is therefore easy to
                                        we are able to completely avoid universal quantifiers in           implement. The reduction approach is structure-preserving,
                                        the process of reduction, but the reduction depends on the         however, which makes us believe that it can utilise existing
                                        introduction of further uninterpreted functions (which create      contextual simplifiers (pre-processors or in-processors) more
                                        some additional work in interpolation, see Section V).             effectively than approaches based on axioms; it also directly
                                           The main idea of reduction is to augment an ADT                 gives rise to an interpolation procedure.
                                        formula with additional literals that ensure that construc-
                                        tors, selectors, and testers are interpreted consistently, and       1 http://www.philipp.ruemmer.org/princess.shtml
      ADT Interpolation: It has been observed in [10] that                     fi : σ1 × · · · × σn → σ0 , and testers is fi expect an argument
the theory of ADTs has the interpolation property; this result                 of type σjd if fi : σjd . In the whole paper, we assume that
directly follows from admissibility of quantifier elimination                  considered expressions are well-typed.
in ADTs [12]. To the best of our knowledge, our ADT
                                                                               Example 1 (Lists) We show examples in the concrete syn-
solver implemented in P RINCESS is the first proof-based
                                                                               tax used in our implementation.
interpolation procedure for ADTs.
      ADTs with Size Constraints: Our approach for handling                1 \sorts {
ADT formulas with size constraints is inspired by the more                 2   Colour { red ; green ; blue ; } ;
                                                                           3   CList { nil ; cons ( Colour head , CList tail ) ;               };
general unfolding-based decision procedure for ADTs with                   4 }
abstractions (i.e., catamorphisms) in [17]. The algorithm
in [17] is complete for sufficiently surjective abstraction                       Given variables x of sort CList and y of sort Colour,
functions, which includes the size function on binary trees,                   a formula over this data type is:2
but not the size function on ADTs in general. We augment
                                                                           1     x . is_cons & y ! = blue &
the setting from [17] by giving a necessary and sufficient                 2     ( x . head = red | x = cons ( y , nil ) )
criterion for sufficient surjectivity of the size function, and
thus for completeness of the overall procedure.                                corresponding to the abstract syntax formula
   ADTs with size constraints can also be represented in
                                                                                         is cons (x) ∧ ¬(y ≈ blue) ∧
the local theory framework [16], again by introducing the
                                                                                          cons1 (x) ≈ red ∨ x ≈ cons(y, nil)
                                                                                                                                           
necessary instances of explicit axioms.
   A further decision procedure for ADTs with size con-                        Assigning {x 7→ cons(red, nil), y 7→ green} satisfies
straints, based on the concept of length constraint comple-                    the formula.
tion, has been described in [19]. Our method uses the simple
approach of unfolding in order to add size constraints to the                     A constructor term is a ground term t that only consists
overall reduction-based procedure; it is at this point unclear                 of constructors (i.e., does not contain selectors or variables).
whether length constraint completion could be combined                         We denote the set of all constructor terms (for some fixed
with the reduction approach as well.                                                                  T
                                                                               ADT signature) by , and the set of all constructor terms
                                                                                                T                                      T
                                                                               of type σjd by σjd . An ADT is well-defined if σjd is non-
                       II. P RELIMINARIES                                      empty for all sorts σ1d , . . . , σkd , and we will henceforth only
   We formulate our approach in the setting of multi-sorted                    consider well-defined ADTs.
first-order logic. The signature Σ of an ADT is defined by                        Semantics is defined in terms of structures ( , I) overT
a sequence σ1d , . . . , σkd of sorts and a sequence f1 , . . . , fm           the universe   T   of constructor terms, i.e., constructors are
of constructors. The type α(fi ) of an n-ary constructor is                    absolutely free. Selectors f j : σ0 → σj in particular are
an (n + 1)-tuple hσ0 , . . . , σn i ∈ {σ1d , . . . , σkd }n+1 , normally                                                               T
                                                                               mapped to total set-theoretic functions I(f j ) : σ0 → σj         T
written in the form fi : σ1 × · · · × σn → σ0 . Zero-ary                       satisfying I(f j )(f (t1 , . . . , tn )) = tj .
constructors are also called constants. By slight abuse of
                                                                                              III. A V ERIFICATION E XAMPLE
notation, we also write fi : σjd if the result type of fi is σjd ,
i.e., if fi : σ1 × · · · × σn → σjd for some σ1 , . . . , σn .                    As a high-level example, we outline how a simple pro-
   In addition to constructors, formulas over ADTs can be                      gram operating on the ADT from Example 1 can be verified
formulated in terms of variables x ∈ X (with some type                         using our procedures. We represent the program in the
α(x) ∈ {σ1d , . . . , σkd }); selectors fij , which extract the j th           form of (constrained) Horn clauses, following the approach
argument of an fi -term; and testers is fi , which determine                   taken in several recent verification systems [8], [15]. The
whether a term is an fi -term. The syntactic categories of                     result resembles a classical logic program implementing the
terms t and formulas φ are defined by the following rules:                     concatenation of two lists; C(x, y, r) expresses that r is the
                                                                               result of concatenating lists x, y:
   t ::= x                                    Variables
                                                                           1 \forall CList y ;                                         // (C1)
         |   fi (t̄)                          Constructors                 2   C ( nil , y , y )
                                                                           3 \forall CList x , y , r ; \forall Colour c ; // (C2)
         |   fij (t)                          Selectors                    4   ( C ( x , y , r ) −> C ( cons ( c , x ) , y , cons ( c , r ) ) )
   φ ::= is fi (t)                            Testers
                                                                                  As a first property of the program, we can observe that
         |   t≈t                              Equality
                                                                               the head of a non-empty result list r has to be the head of
         |   φ ∧ φ | φ ∨ φ | ¬φ | . . .       Boolean operators                one of the arguments x, y:
  Well-typed terms and formulas are defined as expected,                        2 In all examples, the link  will take you to the web interface of our
assuming that selectors have type fij : σ0 → σj whenever                       SMT solver P RINCESS and directly load the given constraint.


                                                                           2
                                                                           Note that the \size operator also counts the nil symbol, as
1 \forall CList x , y , r ; (                             // (P1)
2   r ! = nil & C ( x , y , r ) −>                                         well as the colour constructors red, green, blue, leading to
3   ( r . head = x . head | r . head = y . head ) )                        the stated relationship between the size and the length of a
                                                                           list. The correctness of the model can be checked using the
       To verify this property, it is enough to find a model of the        procedure we define in Section VI.
    (constrained) Horn clauses (C1), (C2), (P1), i.e., an interpre-
    tation of the predicate C that satisfies all three formulas. The         IV. C HECKING ADT S ATISFIABILITY BY R EDUCTION
    predicate C can then be considered as a post-condition (or                We now define our reduction from ADTs to EUF+LIA.
    inductive invariant) that is sufficient to show property (P1).         Suppose φ is an ADT formula as defined in Section II. For
    One solution of (C1), (C2), (P1) is to interpret C(x, y, r) as         sake of presentation, we assume that φ has been brought into
1 C ( CList x , CList y , CList r ) {                                      a flat form upfront. A formula φ is flat if function symbols
2     r = y | r . head = x . head                                          (in our case, constructors and selectors) only occur in
3 }
                                                                           equations of the form g(x1 , . . . , xn ) ≈ x0 (where x0 , . . . , xn
                                                                           are variables, though not necessarily pairwise distinct), and
    which can indeed be observed to satisfy all three clauses.
                                                                           only in positive positions. Flatness can be established at the
    The decision procedure for ADTs defined in the next section
                                                                           cost of introducing a linear number of additional variables.
    can easilycheck correctness of this model mechanically,
    after inlining the definition of C, and skolemising away               Example 2 The formula in Example 1 can be flattened by
    quantifiers.                                                           introducing variables t1, t2 : Colour, and t3 : CList:
       To find models of clauses like (C1), (C2), (P1) automat-
                                                                       1     x . is_cons & blue = t1 & y ! = t1 &
    ically, the principle of Craig interpolation can be applied        2     ( ( red = t2 & x . head = t2 ) |
    to derivation trees of the clauses, an approach that has           3       ( nil = t3 & cons ( y , t3 ) = x ) )
    been implemented in several model checkers [8], [15]. To
    support ADTs, which are currently beyond the scope of most                  Notation: We need some further notation before we can
    model checkers, in Section V we explain how our decision               formally define the reduction. As before, we assume that k
    procedure can be extended to Craig interpolation.                      sorts σ1d , . . . , σkd and m constructors f1 , . . . , fm have been
       Consider now additional clauses computing the list length:          fixed. For each sort σ ∈ {σ1d , . . . , σkd }, we define #Ctor σ
                                                                           to be the number of constructors of σ:
1 L ( nil , 0 )                                           // (C3)
2 \forall CList x ;                                       // (C4)                 #Ctor σ = |{j | j ∈ {1, . . . , m} and fj : σ}|
3     \forall Colour c ; \forall int n ;
4       ( L ( x , n ) −> L ( cons ( c , x ) , n + 1 ) )
                                                                           Similarly, each constructor fi with fi : σ is given a unique
                                                                           index Id fi ∈ {1, . . . , #Ctor σ } as identifier within its sort σ:
      We can combine the two programs to state a second
    property relating concatenation and list length. Concatenat-                     Id fi = |{j | j ∈ {1, . . . , i} and fj : σ}|
    ing two lists yields a list whose length is the sum of the
    individual list lengths:                                               For each sort σ ∈ {σ1d , . . . , σkd }, we furthermore need
1 \forall CList x , y , r ;                               // (P2)
                                                                                                          T
                                                                           to know the cardinality | σ | of the term domain σ .            T
2   \forall int nx , ny , nr ; (
                                                                           The cardinality can be derived by computing the strongly
3     C ( x , y , r ) & L ( x , nx ) & L ( y , ny ) & L ( r , nr )         connected components of the dependency graph induced by
4     −> nr = nx + ny )                                                    the constructors (the graph with sorts σ1d , . . . , σkd as nodes,
                                                                           and edges σid → σjd whenever there is a constructor with a
       To verify this property, as before by showing the existence
    of a model of (C1), (C2), (C3), (C4), (P2), we need a slightly
                                                                                                                                    T
                                                                           σjd -sorted argument and result sort σid ). We write | σ | = ∞
                                                                           for infinite domains.
    extended logic providing also an operator for the size of
    ADT terms (Section VI). ADT constraints without size                   A. Definition of the Reduction
    operator are not sufficiently expressive to formulate any
                                        T
    model. The size of a term t ∈ is the number of constructor
                                                                              Suppose φ is a flat formula in negation normal form
                                                                           (NNF) over an ADT as defined in Section II. To translate
    occurrences in t. A model of (C1), (C2), (C3), (C4), (P2),
                                                                           φ to an EUF+LIA formula φ̃, we introduce a new set of
    interpreting both the predicate C and L, is then
                                                                           function symbols ranging over integers: for each construc-
1   C ( CList x ,     CList y , CList r ) {                                tor f : σ1 × · · · × σn → σ0 a new function f˜ : n →      Z         Z
2       \size ( x )   + \size ( y ) = \size ( r ) + 1                      with the same arity n; for each selector f j : σ0 → σj a
3   };
                                                                                                 Z Z
                                                                           unary function f˜j : → ; for each sort σ ∈ {σ1d , . . . , σkd }
                                                                                                      Z Z
4   L ( CList x ,     int n ) {
5       \size ( x )   = 2*n + 1                                            a function symbol ctorId σ : → to encode testers, and
6   };                                                                     a function depth σ : → Z Z   to ensure acyclicity of terms.

                                                                       3
  Reduction rules for constructors f : σ1 × · · · × σn → σ0 , selectors f j : σ0 → σj , testers is f , and equations between variables:
                                            f (x1 , . . . , xn ) ≈ x0     =⇒ CtorSpec f (x̃0 , . . . , x̃n )                                   (1)
                                                                                                       _
                                                        f j (x) ≈ y       =⇒ f˜j (x̃) ≈ ỹ ∧                          ExCtorSpec g (x̃)        (2)
                                                                                                    g∈{f1 ,...,fm }
                                                                                                        g:σ0
                                                            is f (x)      =⇒ ExCtorSpec f (x̃)                                                 (3)
                                                                                 _
                                                           ¬is f (x)      =⇒              ExCtorSpec g (x̃)                                    (4)
                                                                                  g∈{f1 ,...,fm }
                                                                                   g:σ0 and g6=f
                                                            x≈y           =⇒ x̃ ≈ ỹ                                                           (5)
                                                         ¬(x ≈ y)         =⇒ ¬(x̃ ≈ ỹ)                                                        (6)

  The following abbreviations are used, for each constructor f : σ1 × · · · × σn → σ0 and each sort σ ∈ {σ1d , . . . , σkd }:

                                                                 f˜(x1 , . . . , xn ) ≈ x0 ∧ ctorId σ0 (x0 ) ≈ Id f ∧
                                                                                                                        
                                                               n                                                        
                            CtorSpec f (x0 , . . . , xn ) =      ^                                                     
                                                                      f˜j (x0 ) ≈ xj ∧ depth σ0 (x0 ) > depth σj (xj ) 
                                                                        j=1

                                                                                        n
                                                                                       ^                                                  
                                     ExCtorSpec f (x)        =    ∃x1 , . . . , xn .         In σj (xj ) ∧ CtorSpec f (x, x1 , . . . , xn )
                                                                                       j=1

                                                                        0 ≤ x < |Tσ | if |Tσ | < ∞
                                                                   (
                                                In σ (x)     =
                                                                        true             otherwise

                                                                      Table I
                                                     RULES FOR REDUCTION OF ADT S TO EUF+LIA



                                                                                  Vl
Further, for each variable x : σ occurring in φ, we introduce        φ̃ = φ∗ ∧ i=1 In σi (x̃i ).
an integer-valued variant x̃ : .    Z
    The actual reduction is defined through the rewriting            Example 3 In the encoded version of the formula from
rules in the upper half of Table I. Since the reduction              Example 2, all variables and functions range over integers;
works differently for positive and negative occurrences of           for readability, we keep the names of all variables. New vari-
is f (x) literals, we assume that rules are only applied in          ables s1, . . . , s4 are introduced to eliminate the quantifiers
positive positions, and handle negation explicitly in the rules      of ExCtorSpec f expressions through Skolemisation:
(and assume that φ is in negation normal form). Rule (1)
                                                                   1    // encoding of x.is_cons
augments every occurrence of a constructor symbol with 2 cons ( s1 , s2 ) = x & ctorId_CList ( x ) = 1 &
corresponding statements about selectors (ensuring that both 3 head ( x ) = s1 & tail ( x ) = s2 & 0<=s1 & s1<3 &
are inverses of each other); about the index Id f of the 4 depth_CList ( x ) > depth_Colour ( s1 ) &
                                                                   5    depth_CList ( x ) > depth_CList ( s2 ) &
constructor (ensuring that different constructors of the same 6 // encoding of blue = t1
sort produce distinct values); and about the depth of the 7 blue = t1 & ctorId_Colour ( t1 ) = 2 &
constructed term (ensuring that no term can occur as sub- 8 // encoding of y != t1 (unchanged)
                                                                   9    y ! = t1 &
term of itself). Essentially the same translation is done for 10            // encoding of red = t2
testers by rule (3), introducing fresh constructor arguments 11         ( ( red = t2 & ctorId_Colour ( t2 ) = 0 &
through an existential quantifier. Rule (2) augments each 12                // encoding of x.head = t2
                                                                  13        head ( x ) = t2 & (
occurrence of a selector with a disjunction stating that 14                   // case x.is_nil
the considered term was actually created using one of the 15                  ( nil = x & ctorId_CList ( x ) = 0 ) |
constructors of the sort; this is necessary in general since 16               // case x.is_cons
                                                                  17          ( cons ( s3 , s4 ) = x & ctorId_CList ( x ) = 1 &
selectors f j can be applied to terms constructed using 18                      head ( x ) = s3 & tail ( x ) = s4 &
constructors other that f (an optimisation is discussed in 19                   0 <= s3 & s3 < 3 &
Section IV-C). Rule (4) asserts that the constructor of a term 20               depth_CList ( x ) > depth_Colour ( s3 ) &
                                                                  21            depth_CList ( x ) > depth_CList ( s4 ) ) ) ) |
is different from f , and (5), (6) translate equations by simply 22         // encoding of nil = t3
renaming variables.                                               23      ( nil = t3 & ctorId_CList ( t3 ) = 0 &
    Suppose φ∗ is the result of exhaustively applying the rules 24          // encoding of cons(y, t3) = x
                                                                  25        cons ( y , t3 ) = x & ctorId_CList ( x ) = 1 &
at positive positions in φ, and x1 : σ1 , . . . , xl : σl are all 26        head ( x ) = y & tail ( x ) = t3 &
variables occurring in φ, then the reduct of φ is defined as 27             depth_CList ( x ) > depth_Colour ( y ) &


                                                                                   4
28       depth_CList ( x ) > depth_CList ( t3 ) ) ) &                                                                 ˜
                                                                             hf, (c1 , σ1 ), . . . , (cn , σn )i if I(ctorId   σ )(a) = Id f , with
29     // range constraints for x, y, t1, t2, t3                                                                        ˜  ˜j
                                                                             f : σ1 ×· · ·×σn → σ, and cj = I(f )(a) for j ∈ {1, . . . , n}.
30     // (some of which are just "true")
31     0<=y & y<3 & 0<=t1 & t1<3 & 0<=t2 & t2<3                                 Let Dt contain all pairs (ci , σi ) in tuples dep(a, σ) =
                                                                             hf, (c1 , σ1 ), . . . , (cn , σn )i, for any (a, σ) ∈ D; as well as
        It should be noted that it is not necessary to assume                pairs (β̃(x̃), σ) 6∈ D for any further variable x : σ in φ.
                                                                                We inductively define a sequence γ0 , γ1 , . . . , γ|P | of par-
     positiveness of the depth σ functions, since the functions are
     only used to ensure acyclicity of terms by comparing the                tial functions P → :   T
     depth of a term with the depths of its direct sub-terms. In                1) let γ0 = ∅;
     general, although the formula makes use of integer arith-                  2) for i > 0, if there is (a, σ) ∈ D such that dep(a, σ) =
     metic, only very simple arithmetic constraints are needed.                     hf, (c1 , σ1 ), . . . , (cn , σn )i, the function γi−1 is defined
     Up to slight syntactic modifications, all constraints fall into                for each pair (cj , σj ) (for j ∈ {1, . . . , n}), but γi−1 is
     the Unit-Two-Variable-Per-Inequality fragment UTVPI [6],                       not defined for (a, σ), then let γi = γi−1 ∪ {(a, σ) 7→
     [9], i.e., only inequalities with up to two variables and unit                 f (γi−1 (c1 , σ1 ), . . . , γi−1 (cn , σn ))}.
     coefficients are needed. The constraints can therefore be both             3) for i > 0, if case 2) does not apply, pick any
                                                                                    pair (a, σ) ∈ P \ D for which γi−1 is not defined,
                                                                                                                              T
     solved and interpolated efficiently (of course, presence of
     Boolean structure or negation still implies NP-hardness).                      and any constructor term s ∈                    σ that does not
                                                                                    occur in the range of γi−1 yet; choose (a, σ) and
     B. Correctness of Reduction                                                    s such that the depth of s becomes minimal. Let
     Theorem 1 The reduct φ̃ of a flat ADT formula φ in NNF                         γi = γi−1 ∪ {(a, σ) 7→ s}.
     is satisfiable (over EUF+LIA) if and only if φ is satisfiable              Importantly, the final function γ = γ|P | is defined for all
     (over an ADT).                                                          elements of P , and no two elements of P are mapped to
           Proof: Since reduction preserves the Boolean structure            the same term. To see that γ is defined for all elements of
     of a formula, and the reduction rules are agnostic of the               P , observe that the use of depth σ functions in the encoding
     position at which they are applied, it is enough to prove               ensures that the dep function is acyclic, i.e., no term can
     the theorem for flat conjunctions of literals (i.e., formulas in        ever be required to contain itself as a sub-term. To see that
     negation normal form that do not contain disjunctions).                 γ is injective, observe that by definition the choice of s in
         “⇐=” (easy direction) Suppose φ is satisfiable, with                3) cannot violate injectivity in γi . Different iterations of 2)
                T
     structure ( , I) and variable assignment β. We construct a              cannot construct a term f (γi−1 (c1 , σ1 ), . . . , γi−1 (cn , σn ))
     family (ασid )ki=1 of injective functions as embedding of the           twice, due to the presence of constructor literals f˜(. . .) ≈ x̃
               T          Z                    T
     domains σid into . For i such that σid is infinite, ασid                in φ̃ that are consistently interpreted. Finally, the fact that
                           T        Z T
     can be any bijection σid → ; if σid is finite, we choose                case 2) is always preferred over 3) implies that the term
                            T                  T
     α d to be a bijection σid → {0, . . . , | σid | − 1}. Let α =
     Sσki
                                                                             f (γi−1 (c1 , σ1 ), . . . , γi−1 (cn , σn )) has to contain the most
                                                                             recently chosen term s from case 3) (if there is any) as a sub-
        i=1 ασid . To satisfy φ̃, choose variable assignment β̃ =            term; this implies that f (γi−1 (c1 , σ1 ), . . . , γi−1 (cn , σn )) is
     α ◦ β, and the interpretation I˜ of constructors and selectors
          Z                                  ˜
     over that is induced by α. Define I(depth       σ )(n) to be the
                                                                             deeper than all terms s previously chosen in case 3), and
                                                                             therefore different from all of them.
                                                   ˜
     depth of the constructor term ασ−1 (n), and I(ctorId    σ )(n) as          It is then possible to choose the variable assignment
     the index Id f of the head symbol f of ασ−1 (n) (and arbitrary          β(x) = γ(β̃(x̃), σ) for each variable x : σ in φ.
     if ασ−1 (n) is undefined).
                                                           Z
         “=⇒” Suppose φ̃ is satisfiable, with structure ( , I)  ˜ and        C. Two Optimisations
     assignment β̃. We construct a set P of relevant integer                    The reduction, as presented so far, can be improved
     indices a and corresponding sorts σ in the model, and                   in a number of ways. A first optimisation concerns the
     a mapping γ : P →          T                      T
                                    (with γ(a, σ) ∈ σ for each               way selectors are translated to EUF+LIA, rule (2). It can
     (a, σ) ∈ P ) that can be used to define a variable assign-              be observed that the disjunction of ExCtorSpec g literals
     ment β(x : σ) = γ(β̃(x̃), σ) to satisfy φ. The main difficulty          introduced by rule (2) is in most cases unnecessary, and
     is to ensure that γ is injective, since otherwise disequalities         usually the rule can be simplified to
     in φ might be violated.
         We set P = D ∪Dt , where D is the set of pairs (β̃(x̃), σ)                           f j (x) ≈ y     =⇒       f˜j (x̃) ≈ ỹ            (2’)
     for variables x : σ for which φ contains a constructor                  This simplification is possible whenever rule (2) is applied
     literal f (. . .) ≈ x, a selector literal f j (x) ≈ . . ., or           to guarded selector literals, i.e., whenever f j (x) ≈ y occurs
     a (possibly negated) tester is f (x). The encoding ensures              in conjunction with a (positive or negative) test is g (x), or
     that head symbols and children of terms represented by                  in conjunction with a constructor literal g(x1 , . . . , xn ) ≈ x
     elements of D are defined by the ctorId σ functions and                 (in both cases, regardless of whether f = g).
     the selectors; for (a, σ) ∈ D, define therefore dep(a, σ) =

                                                                         5
    Example 4 The effect of this redundancy can be seen in                conjunction φA ∧ φB , the problem of (reverse) interpolation
    Example 3: given lines 1–5, the disjunction in 14–21 can be           is to find a formula I such that φA ⇒ I, φB ⇒ ¬I, and
    simplified to s3 = s1 & s4 = s2, and can be removed entirely          all variables in I are common to φA and φB . If φA , φB
    since s3 and s4 do not occur elsewhere in the formula.                are ADT formulas, it is natural to approach interpolation by
                                                                          first computing an EUF+LIA interpolant I˜ for the reduced
    Example 5 The full rule (2) is necessary for the following
                                                                          conjunction φ̃A ∧ φ̃B .
    formula over the ADT in Example 1:
                                                                          Example 6 An interpolation problem over the list ADT
1     x = cons ( x . head , x . tail ) <−> x . is_cons
                                                                          from Example 1 is:
    This is because x.head and x.tail occur unguarded.                1   \part [ left ] ( x . is_cons & x . tail = z &
                                                                      2                     z . is_cons & x . head ! = z . head )
       As a second optimisation, the treatment of sorts with finite   3 & \part [ right ] ( x = cons ( c , cons ( c , y ) ) )
    domain can be improved, in particular for sorts that are
    enumerations (i.e., sorts with only nullary constructors). The        The only common variable of the two formulas is x, and
    full EUF encoding is overkill for enumerations, since instead         a solution of the interpolation problem is the disequality
    we can map each constructor f directly to the index Id f :            x.head != x.tail.head. Note that this formula is a correct
                                                                          interpolant even though the selectors are unguarded.
                       f ≈ x0   =⇒     Id f ≈ x̃0              (1’)
                                                                             To translate I˜ back to an ADT interpolant I, three main
    Similarly, testers in enumerations reduce to simple arith-
                                                                          points have to be addressed. First, since all ADT sorts are
    metic comparisons.
                                                                          translated to integers, the formula I˜ might contain arithmetic
    D. Size Increase Caused by the Reduction                              operations on ADT terms that cannot easily be mapped back
       The reduction rules replace every literal in a formula φ           to the ADT world. This turns out to be a non-issue for
    with an expression that is linear in the size n of the                infinite ADT sorts, since reduction does not make use of
    considered ADT, so that |φ̃| ∈ O(n · |φ|). If the ADT is              arithmetic operations for terms over infinite sorts (indeed,
    considered as fixed, the reduction is linear.                         equivalently every infinite ADT sort σ d could be mapped
       As an experimental evaluation of the size increase, we             to a fresh uninterpreted sort σ̃ d ). The situation is different
    applied the procedure (including the optimisations from the           for finite sorts, where predicates In σ from Table I represent
    previous section) to the 8000 randomly generated ADT                  cardinality constraints that can contribute to unsatisfiability
    benchmarks from [2] (4422 of the benchmarks are unsat).               of a formula. One solution is the optimisation discussed in
    The benchmarks themselves are not very challenging, with              Section IV-C: by defining a fixed mapping of terms in finite
    the most complicated one solved in around 1 s, and the                domains to integers, translation of interpolants back to ADT
    average solving time of 43 ms dominated by parsing, pre-              formulas is significantly simplified.3
    processing, etc. The average problem sizes, counted as the               Second, the functions ctorId σ introduced by the reduction
    number of sub-expressions of each formula, were:                      are not valid ADT operations, and have to be translated back
                                                                          to testers (which can be done quite easily).
       After parsing     After reduction   After red. & simpl.               Third, interpolants might also mention depth σ operations,
            76                 337                 34                     which have no direct correspondence in the original ADTs
    This means that reduction led to an increase in size by a             theory. Instead of devising ways how to eliminate such
    factor of 4.5, but this increase was more than offset by subse-       operations, we decide to embrace them instead as a useful
    quent simplification (using the standard EUF+LIA simplifier           extension of ADTs, and adapt our reduction method accord-
    implemented in P RINCESS). Analysing further, it turned               ingly. Since depth is but one measure that can be used to
    out that reduction followed by simplification was extremely           ensure acyclicity, the next sections therefore discuss how we
    effective on the unsatisfiable benchmarks: of the 4422 un-            can reason about ADTs with size constraints.
    satisfiable problems, 4334 could directly be simplified to
    false. The average size of the remaining 3666 problems,                     VI. S OLVING ADT S WITH S IZE C ONSTRAINTS
    after reduction and simplification, was 74, incidentally the             We now consider ADT formulas extended with constraints
    same as the average initial size of all benchmarks.
       An experimental comparison of our solver with other
                                                                                                                           T
                                                                          about term size. The size |t| of a term t ∈ is the number of
                                                                          constructor occurrences in t. The resulting formal language
    SMT solvers, on a larger set of benchmarks, is ongoing.               is an extension of the language defined in Section II:
     V. C RAIG I NTERPOLATION IN (E XTENSIONS OF ) ADT S
                                                                             φ ::= . . . | φPres (|t1 |, . . . , |tn |)    Size constraints
       Since quantifier-free Craig interpolation in EUF+LIA is
    well understood (e.g., [4]–[6]), the reduction approach can             3 In our implementation, such fixed mapping is currently only done for
    also be leveraged for interpolation. Given an unsatisfiable           enumerations, not for other finite ADT sorts.


                                                                      6
    where φPres (|t1 |, . . . , |tn |) is any Presburger formula about         The resulting modified reduction approach is sound for
    the size of ADT terms t1 , . . . , tn .                                  checking unsatisfiability of ADT formulas:
    Example 7 Consider the ADT in Example 1, and a variable                  Lemma 1 If the reduct φ̃ of a flat ADT formula φ in NNF
    x of sort CList. The formula                                             with size constraints is unsatisfiable, then φ is unsatisfiable.
1       \size ( x ) = 3 & x . head = blue                                       Reduction does not directly give rise to a decision proce-
                                                                             dure for ADT constraints with size constraints, in contrast
    has the satisfying assignment x 7→ cons(blue, nil), and                  to the situation without size. This is because reduction
    this assignment is unique. In contrast, the formula                      does not precisely translate the number of terms for each
1       \size ( x ) % 2 = 0                                                             N
                                                                             size n ∈ ≥1 (issue (ii) from above). We can observe that
                                                                             the reduct φ̃ of the formula φ in Example 8 is satisfiable,
    is unsatisfiable, since the size of any list term is odd (term           while φ is unsatisfiable, showing that reduction alone is not
    size does not exactly coincide with the length of a list).               sound for satisfiability (unsurprisingly).
                                                                                Different approaches exist to establish soundness also for
       To extend our reduction approach to formulas with size
                                                                             satisfiability, in particular the extraction of length constraint
    constraints, there are two main issues that have to be
                                                                             completion formulas [19] that precisely define term sizes
    addressed: (i) constructor terms might not exist for all
               N
    sizes n ∈ ≥1 , and (ii) even if terms of some size n ∈ ≥1   N            with sufficiently many distinct terms. We follow the ap-
                                                                             proach of incrementally unfolding (aka. unrolling) from [17],
    exist, there might be too few of them to satisfy a formula.
                                                                             which is quite flexible, and complete in many relevant cases.
    Example 8 Consider the ADT of positive natural numbers:                     Let φ again be a (flat and NNF) ADT formula with size
                                                                             constraints. We construct unfolding sequences φ0 , φ1 , . . . by
1 \sorts {
2   Nat { one ; succ ( Nat pred ) ;      };                                  setting φ0 = φ, and for each i ≥ 1 deriving φi by unfolding
3 }                                                                          one ADT variable x : σ that occurs in φi−1 . If f1 , . . . , fn
                                                                             are all constructors of the considered ADT, we set
                              N
    For every size b ∈ ≥1 there is exactly one constructor                                                  _
    term t with |t| = b. This implies unsat. of the formula                          φi = φi−1 ∧                   fj (xj1 , xj2 , . . .) ≈ x
                                                                                                          j∈{1,...,n}
1       \size ( x ) = 3 & \size ( y ) = 3 & x ! = y                                                          fj :σ


                                                                             with fresh sorted argument variables x11 , x12 , . . . , x21 , x22 , . . ..
    A. Reduction and Incremental Unfolding
                                                                                In practice, unfolding will usually happen incrementally:
       We address issue (i) noted above by reasoning globally                the next variable to unfold is selected based on a model
    about possible term sizes within an ADT. For an ADT                      of the previous partial unfolding φi−1 , until enough terms
                          S
    sort σjd , we define σjd = {|t| | t ∈ σjd } ⊆T          N  to be         have been constructed to obtain a genuine model of φ, or
                                        T
    the size image of the term set σjd , i.e., the set of term               unsatisfiability is detected.
              T
    sizes in σjd . The size image turns out to be a special case
                                                                             Lemma 2 Let φ0 , φ1 , . . . be an unfolding sequence for φ,
    of the Parikh image of a context-free language, since an
    ADT can be interpreted as a context-free grammar over
                                                                             and for each i ∈      N
                                                                                                   let Ui be the set of variables unfolded
                                                                             in φi (i.e., U0 = ∅, and Ui = Ui−1 ∪ {x} if φi was derived
    a singleton alphabet (by considering every sort as a non-
    terminal symbol, and mapping every constructor to the
                                                                             by unfolding x in φi−1 ). Then for any i ∈ :          N
    unique letter in the singleton alphabet). This implies that                 1) if φ̃i is unsatisfiable (over EUF+LIA) then φ is unsat-
    S σjd is semi-linear, and that a representation of the set in
                                                                                   isfiable (over ADTs with size);
    the form of an existential Presburger formula can be derived                2) if φ̃i is satisfied by a model M̃ and assignment β̃,
    from the set of constructors in linear time [18].                              such that for every ADT variable x : σ in φi there
       Table II shows how the reduction from Section IV-A (and                     is a variable y ∈ Ui with y : σ and valM̃ ,β̃ (x̃) =
    Table I) is augmented to deal with size constraints. Instead                   valM̃ ,β̃ (ỹ), then φ is satisfiable (over ADTs with size).
    of the depth σ functions, for each sort σ ∈ {σ1d , . . . , σkd } a
                      Z Z
    function size σ : → representing term size is introduced,
                                                                                  Proof: 1) follows directly from Lemma 1.
                                                                                2) Models over EUF+LIA can be translated to ADT
    and the CtorSpec f constraints are changed accordingly;
                                                                             models like in the proof of Theorem 1 “=⇒”. It can be noted
    and an additional reduction rule (7) is introduced to handle
                                                                             that case 3) in the proof never applies due to the assumption
    equations |x| ≈ y with the size operation. Rule (7) adds
                      S
    constraints y ∈ σ to ensure that only genuine term sizes
                                                                             that all variables are mapped to unfolded terms.
    are considered, assuming implicitly that the size image σ     S          Example 9 In Example 8, unsatisfiability is detected after
    is represented as a Presburger formula.                                  unfolding x and y three times each.

                                                                         7
      Additional reduction rule for size expressions, assuming x is a variable of sort σ ∈ {σ1d , . . . , σkd }, and y a variable of sort Z:
                                                                 |x| ≈ y    =⇒ size σ (x̃) ≈ y ∧ y ∈ Sσ                                                   (7)
      Compared to Table I, for each constructor f : σ1 × · · · × σn → σ0 the abbreviation CtorSpec f is replaced with CtorSpec 0f :

                                                             f˜(x1 , . . . , xn ) ≈ x0 ∧ ctorId σ0 (x0 ) ≈ Id f ∧
                                                                                                                                            
                                                            n                                                                n
                      CtorSpec 0f (x0 , . . . , xn )
                                                                                                                                             
                                                       =
                                                                   f˜j (x0 ) ≈ xj ∧ size σj (xj ) ∈ Sσj ∧ size σ0 (x0 ) ≈ 1 +
                                                           ^                                                                X              
                                                                                                                               size σj (xj )
                                                               j=1                                                                j=1


                                                                         Table II
                                       A DDITIONAL RULES FOR REDUCTION OF ADT S WITH SIZE CONSTRAINTS TO EUF+LIA




                                                                           red         applies) for all formulas φ if and only if the considered ADT
       nil          CList                                  Colour          blue        is expanding.
                                                                           green
                                        cons                                                  Proof sketch: “=⇒” Example 10 generalises to arbi-
                                                                                       trary non-expanding ADTs: for every non-expanding sort σ
        Figure 1.    Dependency graph for the list ADT from Example 1
                                                                                       there is a constant c ∈             N
                                                                                                                          and an infinite semi-linear
                                                                                                    S               T
                                                                                       set S ⊆ σ such that | bσ | < c for all b ∈ S. The existence
                                                                                       of c, S follows from the proof of Theorem 2 below.
       As the next example shows, however, unfolding is not al-
    ways enough to show unsatisfiability of a formula. The next                           “⇐=” Consider first the case of φ being a conjunction
    sections will therefore formulate a sufficient and necessary                       of disequalities and a size constraint φPres (|x1 |, . . . , |xn |).
    criterion for termination of unfolding.                                            Since the ADT is expanding, satisfiability of φ reduces to
                                                                                       the question whether the size images of the xi -domains
    Example 10 With the ADT from Example 8, the formula                                contain elements large enough, and compatible with φPres ,
                                                                                       that all disequalities can be satisfied. Systematic unfolding of
1     \size ( x ) = \size ( y ) & x ! = y
                                                                                                                                                  S
                                                                                       x1 , . . . , xn will add size image constraints |x0 | ∈ σ for all
    is unsatisfiable, but cannot be shown to be unsatisfiable with                     sub-terms, and either find a set of satisfying term sizes (and
    a finite number of unfolding steps.                                                corresponding terms), or conclude unsatisfiability because
                                                                                       the conjunction of size images and size constraint φPres
    B. Completeness and Incompleteness of Unfolding                                    becomes inconsistent.
                                                                                          Adding constructor, selector, or test literals does not
       We give a precise characterisation of the ADTs for which
                                                                                       change the argument, since solutions of such literals can
    unfolding will allow us to eventually detect (un)satisfiable of
                                                                                       be represented in the form of a most-general unifier [17].
    a formula, and therefore gives rise to a decision procedure.
    As identified in [17], the essential property of an ADT (resp.,                      Non-expandingness turns out to be a corner case: all non-
    of the considered catamorphism, which in our case is the size                      expanding ADTs more or less look like the natural numbers
    function) is sufficient surjectivity, implying that ADTs are                       (Example 8), and most other practical ADTs are expanding.
    sufficiently populated to satisfy disequalities in a formula:                      For instance, both ADT sorts in Example 1 expand.
    the number of terms of size b grows unboundedly when b
                                       T
    tends to infinity. We write kσ for the set of constructor terms
                                                T
    of ADT sort σ and size k, i.e., kσ = {t ∈ kσ | |t| = k}.    T                      C. Effective Characterisation of Expanding ADTs
                                                                                          To characterise expanding ADTs, we first make the sim-
    Definition 1 An ADT sort σ d is expanding if for every
    natural number n ∈           N
                             there is a bound b ∈                    N
                                                             such that
                                                                                       plifying assumption that all ADT sorts σjd contain at least
                               0
                                  T                0
                                                       T
    for every b0 ≥ b either bσd = ∅ or | bσd | ≥ n. An ADT is
                                                                                       two constructor terms; sorts with only a single term can
                                                                                       obviously be eliminated easily from a constraint. As a further
    expanding if each of its sorts σ1d , . . . , σkd is expanding.
                                                                                       piece of notation, we need a relativised version of the size
    Example 11 An example of an ADT that is not expanding                              image: for an ADT sort σjd and a constructor f , we write
    are the natural numbers (Example 8): for every size b ∈ ≥1               N
    there is exactly one constructor term t with |t| = b.                                    Sfσ = {|t| | t ∈ Tσ , and t does not start with f }
                                                                                                d
                                                                                                j
                                                                                                                       d
                                                                                                                       j



    Lemma 3 Systematic unfolding terminates (i.e., in every                            for the size image restricted to terms with head symbol 6= f .
    unfolding sequence φ0 , φ1 , . . . in which every variable is                         Consider then the bipartite dependency graph D = (V, E)
    eventually unfolded, eventually one of the cases of Lemma 2                        with vertices V = {σ1d , . . . , σkd } ∪ {f1 , . . . , fm } being sorts

                                                                                   8
  and constructors, and the edge set                                     unique hole •; such terms can alternatively be seen as terms
         (                                                       )       with a single occurrence of a sorted variable. Composition of
           (σ0 , fj ), (fj , σ1 ), . . . , (fj , σn )                    terms with holes is defined as t1 [•] ◦ t2 [•] = t1 [t2 [•]]. Two
  E =
                 | j ∈ {1, . . . , m}, fj : σ1 × · · · × σn → σ0         terms t1 [•], t2 [•] with holes are incomparable if t1 [s1 ] 6=
                                                                         t2 [s2 ] for all constructor terms s1 , s2 of the right sort. The
  Fig. 1 gives the graph for the list ADT in Example 1.
                                                                         size |t[•]| of a term with hole is the number of constructor
  Theorem 2 An ADT is not expanding if and only if the                   symbol occurrences in t, i.e., the hole does not count. This
  graph D contains a simple cycle C = σ 1 → f 1 → σ 2 →                  implies |t1 [•] ◦ t2 [•]| = |t1 [•]| + |t2 [•]|.
  f 2 → · · · → f n → σ 1 with the following properties:
                                                                         Lemma 4 Suppose an ADT sort σ contains two incompa-
     1) C is the only path from σ 1 to itself, i.e., every cycle         rable constructor terms t1 [•], t2 [•] with holes • of sort σ.
        starting and ending in σ 1 is a repetition of C;                 Then σ expands.
     2) all constructors f 1 , f 2 , . . . , f n on C are unary;
     3) the cycle C unboundedly contributes to the size im-                     Proof: Fix some n ∈ N . We need to show that there
             S
        age σ1 , i.e.,                                                   is a bound b ∈
                                                                                    0
                                                                                                   N              T     0
                                                                                                                                     T 0
                                                                                                          ensuring bσ = ∅ or | bσ | ≥ n for
                                              n                          every b ≥ b. Observe that for every g ≥ n there are > n
                 Sσ 6= {0, . . . , k} · n +         Sfσ + i − 1 .
                                                      i
                                                                         pairwise incomparable terms with holes t01 ◦ tg2 ◦ tg1 , t11 ◦ tg2 ◦
                                              [
           ∀k.      1                                 i
                                                                         tg−1  , . . . , tg1 ◦ tg2 ◦ t01 , all of which have size g · (|t1 | + |t2 |).
                                                                                               S       N
                                              i=1                         1
                                                                         The size image σ ⊆ can be represented                    as a finite union
       The characterisation theorem implies that every non-
                                                                                                             S          Sl
                                                                         of arithmetic progressions, σ = i=1 {ai + k · bi | k ∈ }                   N
  expanding ADT has a set of cyclically connected sorts S1,
  . . . , Sn, each of which might contain further constructors
                                                                         with ai , bi ∈    N       for i ∈ {1, . . . , l}. For each i ∈ {1, . . . , l}
                                                                         with bi > 0, assuming that k ≥ n · (|t1 | + |t2 |) we can then
  c1_1, c1_2, . . . that do not lead back to S1, . . . , Sn:
                                                                         pick g = bi · n, and some term t : σ of size ai + (k − n ·
1 \sorts {                                                               (|t1 | + |t2 |)) · bi , and obtain > n pairwise distinct terms
2   // ...
3   S1 { f1 ( S2 s2 ) ; c1_1 ; c1_2 ; /* ... */ } ;                        (t01 ◦ tg2 ◦ tg1 )[t], (t11 ◦ tg2 ◦ tg−1
                                                                                                                1   )[t], . . . , (tg1 ◦ tg2 ◦ t01 )[t]
4   S2 { f2 ( S3 s3 ) ; c2_1 ; c2_2 ; /* ... */ } ;
5   // ...                                                               that are all of size ai +(k−n·(|t1 |+|t2 |))·bi +g·(|t1 |+|t2 |) =
6   Sn { fn ( S1 s1 ) ; cn_1 ; cn_2 ; /* ... */ } ;                      ai +k·bi . This implies that there is also a global bound b ∈                N
7
8 }
    // ...
                                                                                      T 0            0
                                                                                                       T
                                                                         such that bσ = ∅ or | bσ | ≥ n for b0 ≥ b.
                                                                               Proof of Theorem 2: “=⇒” Suppose an ADT is not ex-
     The conditions of the theorem are clearly satisfied for
                                                                         panding, which means that there is a non-expanding sort σ.
  the ADT of natural numbers (Example 8). Condition 3) is                                                       ∗
                        S
                        i
  satisfied whenever fσi is finite for all i ∈ {1, . . . , n}, but
                                                                         Choose σ such that whenever σ → σ 0 in the D-graph, and
                                                                         σ is non-expanding as well, then σ 0 is in the same strongly
                                                                           0
  there are more subtle situations:                                      connected component (SCC) as σ; this is possible because
  Example 12 We extend the list ADT from Example 1 by                    the SCCs of D form a DAG. Then σ has to be infiniteS
  adding two further sorts:                                              (otherwise σ would be expanding), and there is a simple
                                                                         D-path C = σ 1 → f 1 → σ 2 → f 2 → · · · → f n → σ 1 with
1 \sorts {
2   S1 { f1 ( S2 s2 ) ; } ;
                                                                         σ 1 = σ (otherwise there would be a non-expanding sort σ 0
3   S2 { f2 ( S1 s1 ) ; null ; col ( CList list ) ;       };             reachable from σ, but not in the same SCC).
4 }                                                                          We show that C satisfies the conditions of the theorem.
                                                                         1) holds because if there was a second path C 0 from σ to
  The domain of sort S1 contains terms of any size greater               itself that is not a repetition of C, then both paths could be
  than one. However, while the number of terms of size 2k +1             translated to incomparable σ-terms t1 [•], t2 [•] with σ-sorted
  grows exponentially with k, there is exactly one term of               holes •, and by Lemma 4 the sort σ would be expanding.
  size 2k for every k, proving non-expandingness.                        The same argument implies that 2) holds: if any of the
     A cycle of length 3, in contrast, yields an expanding ADT:          constructors fi had multiple arguments, incomparable terms
1 \sorts {                                                               t1 [•], t2 [•] could be derived (since, by assumption, every sort
2   S1 { f1 ( S2 s2 ) ; } ;                                              contains at least two constructor terms).
3
4
    S2 { f2 ( S3 s3 ) ; } ;
    S3 { f3 ( S1 s1 ) ; null ; col ( CList list ) ;       };
                                                                             Suppose finally that 3) does not hold, i.e., for some k ∈                N
5 }                                                                                                                   n
                                                                                    Sσ = {0, . . . , k} · n +               Sfσ + i − 1
                                                                                                                                i
                                                                                                                      [
                                                                                                                                i
  We can note that condition 3) of Theorem 2 now fails.                                                               i=1

     Before we can prove Theorem 2, we need some further                 This would imply that from some sort σ i a non-expanding
  results about ADTs. Consider constructor terms t[•] with a             sort σ 0 is reachable, by following a constructor other than f i .

                                                                     9
By choice of σ, then σ 0 has to be in the same SCC as σ,                              [6] Alessandro Cimatti, Alberto Griggio, and Roberto Sebastiani.
therefore there is a path from σ 0 to σ, and condition 1) would                           Interpolant generation for UTVPI. In CADE, volume 5663 of
be violated.                                                                              LNCS, pages 167–182. Springer, 2009.
   “⇐=” Suppose there is a cycle C satisfying 1)–3). Note                             [7] Leonardo Mendonça de Moura and Nikolaj Bjørner. Z3: An
that due to 1) and 2) we have the equality                                                efficient SMT solver. In TACAS, volume 4963 of LNCS, pages
                                     n                                                    337–340. Springer, 2008.
                Sσ = N · n +               Sfσ + i − 1
                                               i
                                     [
                                               i
                                                                                      [8] Sergey Grebenshchikov, Nuno P. Lopes, Corneliu Popeea, and
                                     i=1                                                  Andrey Rybalchenko. Synthesizing software verifiers from
                                     |         {z         }
                                                R                                         proof rules. In PLDI, pages 405–416. ACM, 2012.

                                     N
Together with 3), this means · n + R 6= {0, . . . , k} · n + R                        [9] Joxan Jaffar, Michael J. Maher, Peter J. Stuckey, and Roland
                   N
for every k ∈ . Because R is a semi-linear set, then there                                H. C. Yap. Beyond finite domains. In PPCP, volume 874 of
has to be a finite subset S ⊆ R such that for infinitely many                             LNCS, pages 86–94. Springer, 1994.
               S
points s ∈ σ we have {x ∈ R | s ∈                    N
                                              · n + x} ⊆ S.
                            T
Because the set {t ∈ σ | |t| ∈ S} of terms is finite,4 this
                                                                                     [10] Deepak Kapur, Rupak Majumdar, and Calogero G. Zarba.
                                                                                          Interpolation for data structures. In SIGSOFT’06/FSE-14,
immediately implies that the sort σ is not expanding.                                     pages 105–116, New York, NY, USA, 2006. ACM.

                        VII. C ONCLUSIONS                                            [11] Zohar Manna, Nikolaj Bjørner, Anca Browne, Edward Y.
                                                                                          Chang, Michael Colón, Luca de Alfaro, Harish Devarajan,
   At the moment we are exploring applications and further                                Arjun Kapur, Jaejin Lee, Henny Sipma, and Tomás E. Uribe.
extensions of our approach. We are in the process of integrat-                            STeP: The Stanford temporal prover. In TAPSOFT, volume
ing our procedure into the model checker E LDARICA [15] to                                915 of LNCS, pages 793–794. Springer, 1995.
handle implication checks and interpolation for ADTs; this
                                                                                     [12] Derek C. Oppen. Reasoning about recursively defined data
also requires combination with other data types, and in the                               structures. J. ACM, 27(3):403–411, July 1980.
long run likely interpolation heuristics. It is also frequently
necessary to combine ADTs with quantifier reasoning and                              [13] Andrew Reynolds and Jasmin Christian Blanchette. A deci-
recursively defined functions, a direction that requires further                          sion procedure for (co)datatypes in SMT solvers. J. Autom.
work. Finally, as a side-effect of Theorem 2, there is a simple                           Reasoning, 58(3):341–362, 2017.
way to achieve termination also for non-expanding ADTs,                              [14] Philipp Rümmer. A constraint sequent calculus for first-order
namely by replacing the cycle with an explicit counter                                    logic with linear integer arithmetic. In LPAR, volume 5330
ranging over a built-in type of natural numbers.                                          of LNCS, pages 274–289. Springer, 2008.
     Acknowledgements: Rümmer was supported by the
Swedish Research Council under grant 2014-5484.                                      [15] Philipp Rümmer, Hossein Hojjat, and Viktor Kuncak. Dis-
                                                                                          junctive interpolants for Horn-clause verification. In CAV,
                                                                                          volume 8044 of LNCS, pages 347–363. Springer, 2013.
                             R EFERENCES
 [1] Clark Barrett, Christopher L. Conway, Morgan Deters, Liana                      [16] Viorica Sofronie-Stokkermans. Locality results for certain
     Hadarean, Dejan Jovanovic, Tim King, Andrew Reynolds, and                            extensions of theories with bridging functions. In CADE,
     Cesare Tinelli. CVC4. In CAV, volume 6806 of LNCS, pages                             volume 5663 of LNCS, pages 67–83. Springer, 2009.
     171–177. Springer, 2011.
                                                                                     [17] Philippe Suter, Mirco Dotta, and Viktor Kuncak. Decision
 [2] Clark Barrett, Igor Shikanian, and Cesare Tinelli. An abstract                       procedures for algebraic data types with abstractions. SIG-
     decision procedure for a theory of inductive data types. JSAT,                       PLAN Not., 45(1):199–210, January 2010.
     3(1-2):21–46, 2007.
                                                                                     [18] Kumar Neeraj Verma, Helmut Seidl, and Thomas Schwentick.
                                                                                          On the complexity of equational Horn clauses. In CADE,
 [3] Clark Barrett and Cesare Tinelli. CVC3. In CAV, volume
                                                                                          volume 3632 of LNCS, pages 337–352. Springer, 2005.
     4590 of LNCS, pages 298–302. Springer, July 2007.
                                                                                     [19] Ting Zhang, Henny B. Sipma, and Zohar Manna. Decision
 [4] Angelo Brillout, Daniel Kroening, Philipp Rümmer, and                               procedures for term algebras with integer constraints. Inf.
     Thomas Wahl. Beyond quantifier-free interpolation in ex-                             Comput., 204(10):1526–1574, 2006.
     tensions of Presburger arithmetic. In VMCAI, LNCS, pages
     88–102. Springer, 2011.

 [5] Jürgen Christ, Jochen Hoenicke, and Alexander Nutz. SMTIn-
     terpol: An interpolating SMT solver. In SPIN, pages 248–254,
     2012.
  4 This property breaks down when ADTs are combined with other infinite
data types, e.g., lists over Z. In this case condition 3) has to be modified.


                                                                                10
