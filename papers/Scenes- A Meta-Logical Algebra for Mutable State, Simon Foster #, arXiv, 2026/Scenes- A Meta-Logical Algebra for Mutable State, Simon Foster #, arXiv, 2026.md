                                         Scenes: A Meta-Logical Algebra for Mutable State
                                         Simon Foster #
                                         University of York
                                         Carlos Isasa
                                         University of Aarhus
                                         Christian Pardillo Laursen
                                         University of York

                                               Abstract
                                         Modelling of mutable state spaces and precisely describing how variables are manipulated in a
                                         program is a fundamental problem in compositional verification. Though we can make use of the
                                         embedded abstract syntax of a program for such analysis, this runs contrary to the shallow-embedding
arXiv:2609.29380v1 [cs.LO] 24 Sep 2026




                                         approach, and hampers efficient proof automation. On the other hand, lenses and prisms provide
                                         an elegant algebraic foundation for modelling state, which provide sufficient structure to provide
                                         meta-logical program analysis, but without requiring a deep embedding. Nevertheless lenses, as
                                         complex algebraic objects, cannot easily be combined, complemented, or collected in sets. In this
                                         paper we contribute an accompanying algebraic structure called the scene, which allows us to
                                         characterise the set of variables, or coordinates, in a state space. Scenes intuitively correspond
                                         to sets of lenses, but like lenses they are purely semantic algebraic objects. We demonstrate that
                                         scenes provide us with sufficient structure to characterise the lens-based meta-logical properties, like
                                         independence and equivalence. Moreover, we introduce the notion of a scene space, analogous to a
                                         vector space, which allows us to recover a set-like algebraic structure. Finally, we show how scenes
                                         allow us to characterise the free and bound variables of expressions and programs, without any need
                                         for syntax, and demonstrate their use for reasoning about programs by deriving reasoning principles
                                         for the parallel composition operator.

                                         2012 ACM Subject Classification Theory of computation → Semantics and reasoning

                                         Keywords and phrases Program verification, State modelling, Isabelle, Formal verification

                                         Acknowledgements We thank Brijesh Dongol and Georg Struth for their helpful feedback on an
                                         early version of this work.
2   Scenes: A Meta-Logical Algebra for Mutable State


     1     Introduction

    Modelling the mutable state of a program is a fundamental problem in verification [2, 29, 7].
    Though a naive model for state can be given through functions from variables to values (e.g.
    N → V ), in reality state spaces and stores are more complex and multi-faceted than this. For
    example, they can consist of concurrency, hierarchy, and addresses. In previous work [10, 22],
    we have used lenses — an algebraic structure that pairs a get and put function [9] — to
    provide a flexible and powerful foundation for modelling state.
        Lenses significantly narrow the gap between deep and shallow semantic embeddings [10].
    On the one hand, they do not require the formalisation of names and abstract syntax, which
    ensures that lens-based verification tools can maximise proof automation, through reuse
    of host logic facilities, as in a shallow embedding. On the other hand, lenses also provide
    sufficient structure on the store so that the semantics, rather than the abstract syntax,
    provides sufficient information for laws of programming, akin to a deep embedding. With
    them we can encode meta-logical operators, that is those operators that characterise program
    properties, such as substitutions for variables, whether an expression depends on a variable
    or not, and whether a program modifies a variable. This has allowed us to develop several
    verification tools with lenses as the foundation, including concurrent systems [11, 12], hybrid
    systems [22], probabilistic systems [32], and robotic state machines [13, 31].
        However, whilst lenses have demonstrable utility, they lack the ability to describe collec-
    tions of variables, and the typical set operators (membership, union, etc.). This is required,
    for example, so that we can compute the set of free variables in an expression, and so that
    we can manipulate a program’s frame – the set of variables that a program modifies [28].
    Almost every formal verification approach requires that we can model sets of variables, in
    tools as diverse as Event-B [1] and KeYmaera X [16]. The research question that this paper
    tackles is: how can we effectively model sets of program variables in the context of a shallow
    embedding?
        Our answer to this question is scenes, a simple yet powerful algebraic structure that
    allows us to semantically encode a set of variables. Scenes are essentially merge operators,
    which allow us to combine two program states together, according to a pre-defined division of
    the state variables. As with lenses, scenes do not depend on a particular state space model,
    but can be applied to any type that can be subdivided into variables. The intuition of scenes
    as sets requires that we can also formalise scene spaces, which characterises foundational
    consistency properties for state spaces. Thus, scenes allow us to characterise a region of the
    store semantically, which in turn provides the basis for compositional reasoning by allowing
    us to precisely capture how a program modifies the state. We use scenes to derive results
    from Platzer’s differential dynamic logic [27, 28], which are foundational to reasoning about
    concurrent hybrid programs.
        Our theory does not require dependent types, and has been mechanised in the Isabelle
    proof assistant [24]. Every significant definition and theorem is accompanied by a link to our
    Git repository with the mechanised artefact         However, our results are also applicable to
    other proof assistants, such as Lean [6] and Rocq [30].
        In Section 2 we review preliminaries on lenses and state spaces. In Section 3 we introduce
    the scene as an algebraic structure, and describe the fundamental operators. In Section 4 we
    introduce scene spaces, which characterise consistent state spaces, and give rise to a complete
    Boolean algebra. In Section 5 we apply all of the aforementioned theory in mechanising free
    variables and bound variables for expressions and programs, and derive key theorems from
    Platzer’s work. In Section 6 we consider related work and in Section 7 we conclude.
Simon Foster, Carlos Isasa, Christian Pardillo Laursen                                                3


 2     Preliminaries: Lenses and State Spaces
Lenses are used to model the mutation of variables in the program state. A lens X : V =⇒ S
is a structure (V, S, get, put), where getX : S → V and putX : V → S → S, V is the view, and
S is the source. Intuitively, a lens describes a V-shaped region of a source type, S. They can
capture either the individual variables of type V, or several variables. We constrain lenses to
obey a number of algebraic laws, which describe how a single variable may be updated:

          get (put v s) = v        put v (put v ′ s) = put v s       put (get s) s = s

For example, if S ≜ V1 ×V2 ×· · ·×Vn then we can form a lens for each projection πi : Vi =⇒ S
for i ∈ {1 · · · n}. In general, state spaces can be arbitrarily complex with hierarchy and
nested data structures. Thus, lenses may be independent from each other, meaning they do
not interfere, or one lens may be part of another. We characterise independence below:

▶ Definition 1. Lenses X : V1 =⇒ S and Y : V2 =⇒ S are independent, written X ▷◁ Y ,
provided that putX v1 ◦ putY v2 = putY v2 ◦ putX v1 , for any v1 ∈ V1 and v2 ∈ V2 .

In the n-ary product space, πi and πj are independent πi ▷◁ πj precisely when i =   ̸ j. We can
compose lenses X # Y when the source of X matches the view of Y [10].
    We also define 1 ≜ (A, A, λs. s, λ v s. s), which provides a left and right unit for #, and
covers the whole state space. It is an example of a bijective lens, that is a lens that satisfies
put s (get s′ ) = s′ . Bijective lenses relate isomorphic representations of the same state space.
    We can now characterise the part-of relationship using a heterogeneous preorder on lenses:

▶ Definition 2. Lens X : V1 =⇒ S is a sublens Y : V2 =⇒ S, written X ⪯ Y , if there exists
Z : V1 =⇒ V2 , such that X = Z # Y .

Intuitively, X ⪯ Y when Y encompasses all the variables in X. For example, 1 encompasses
all of the state, and so X ⪯ 1. Moreover, we can define a heterogeneous equivalence:
X ≈ Y ↔ (X ⪯ Y ∧ Y ⪯ X), for when two lenses encompass the same region. For example, if
X ≈ 1, it means that X covers all the state, and so is bijective.
    In addition, we can compose two lenses in parallel using the lens sum operator:

▶ Definition 3. Given independent lenses X : V1 =⇒ S and Y : V2 =⇒ S, the summation of
two lenses is defined X ⊕ Y = (V1 × V2 , S, λs. (getX s, getY s), λ(v1 , v2 ). putX v1 ◦ putY v2 ).

Operationally, X ⊕ Y corresponds to a simultaneous update to the coordinates characterised
by X and Y . However, it also allows us to characterise the region of the source covered by
both X and Y . Using this, we can now formally characterise a state space:

                                       P of lensesA = {x1 , x2 , · · · , xn }, such that xi ▷◁ xj
▶ Definition 4. A state space is a family
for i ̸= j, which form a span, that is   i∈{1···n} xi ≈ 1.

Each xi ∈ A is called a basis lens. Analogous to a vector space, combinations of basis
lenses allow us to address any location. A state is then a set of maplets [x1 ⇝ v1 , x2 ⇝
v2 , · · · , xn ⇝ vn ]. However, we do yet not have the mathematical machinery necessary to
formally characterise or construct such bases, which is the objective of sections 3 and 4.
     Each basis lens can also be considered as a coordinate (or set thereof) that forms part
of a coordinate system. The summation of the lenses in A yields a bijective lens that is
                                                           P
analogous to a coordinate chart [23]. Specifically, X = ( i∈{1···n} xi ) is a bijective lens of
           Q
type ( i∈{1···n} Vi ) =⇒ S. Since A forms a span, getX transforms S into a flat product
4   Scenes: A Meta-Logical Algebra for Mutable State


    space, similar to how a coordinate chart φ : U → Rn transforms a manifold into a Euclidean
    space.
         As an example, consider a type for Cartesian coordinates in a 2-dimensional plane coord
    (i.e. R × R). We define xc, yc : R =⇒ coord, which are independent (xc ▷◁ yc), and form a
    span (xc ⊕ yc ≈ 1). They form a state space and a consistent coordinate system. We can
    also consider an alternative state space on the coord type, as shown below.

    ▶ Example 5 (Polar Coordinates Lenses).

                   radius-of(x, y) ≜ sqrt(x2 + y 2 )            angle-of(x, y) ≜ arctan(y/x)
                       xc-of(r, θ) ≜ r · cos(θ)                    yc-of(r, θ) ≜ r · sin(θ)
            radius ≜ (radius-of, (λ(x, y) r. (xc-of(r, angle-of(x, y)), xc-of(r, angle-of(x, y)))))
             angle ≜ (angle-of, (λ(x, y) θ. (xc-of(radius-of(x, y), θ), yc-of(radius-of(x, y), θ))))

    We consider only strictly positive coordinates in the first quadrant by defining pcoord ≜
    R>0 ×R>0 , and define lenses radius : R>0 =⇒ pcoord and angle : A =⇒ pcoord. These convert
    Cartesian coordinates into polar coordinates using trigonemtric identities. These lenses obey
    the three lens laws1 . Moreover, radius ▷◁ angle, since we can modify either coordinate without
    affecting the other, and also radius ⊕ angle ≈ 1, confirming that every Cartesian coordinate
    has a polar coordinate. Of course, these two coordinate systems are not compatible: we
    cannot switch arbitrarily between them without corrupting the state space.
        We have seen that lenses allow us to characterise a state space. However, they are complex
    algebraic objects to deal with, due to the presence of two sorts: the view V and the source
    S. The preorder (⪯) and equality relation (≈) are both heterogeneous, and so equational
    rewriting cannot be automated in proofs assistants like Isabelle. Moreover, though we can
    describe the family A, in reality we cannot collect a set of lenses in a set within a typed
    logic, since every element of a set must have the same type. Therefore, in the next section
    we introduce a related algebraic object that will allow us to overcome these issues.

        3      Scenes
    In this section we introduce a novel algebraic structure called a scene. In contrast to lenses,
    scenes allow us to formally model sets of variables or coordinates, in a given state space.

    ▶ Definition 6. A scene is a structure A ≜ (S, mrg) where S ̸= ∅ and mrg : S → S → S is
    a binary operator called the merge function. For any x, y, z : S, it obeys the following laws2 :

            mrg (mrg x y) z = mrg x z            mrg x (mrg y z) = mrg x z               mrg x x = x

    We write Scene(S) for the set of scenes over S, that is, a family of merge functions over S.
    We write mrgA and mrgB to distinguish the merge functions from several scenes.

    Intuitively, mrg merges two states, analogous to merge operators in programming languages.
    Given a state [x1 ⇝ v1 , x2 ⇝ v2 , · · · ] then a merge function mrg s1 s2 replaces the value of a
    subset of the variables in s1 with those in s2 . Scenes therefore semantically describe a subset
    of the state variables without capturing the view, which yields a simpler algebraic structure.
        We give an example family of scenes based on total functions.


    1
        This primarily follows because we have removed the origin.
    2
        In Isabelle/HOL, these are called “idempotent scenes”, but for this paper this distinction is irrelevant.
Simon Foster, Carlos Isasa, Christian Pardillo Laursen                                               5


▶ Definition 7 (Function Domain Scene). We assume non-empty sets A and B, which provide
the domain and range types for a function, and a set D ⊆ A, and then define
                                                  (                !
                                                    f (x) if x ∈ D
                    fdsA
                       B (D) ≜  A → B, λf g. λx.
                                                    g(x) otherwise

This scene overrides f with g when an input value x is a member of D. It is easy to show
that the overriding function obeys the three laws in Definition 6.                     ◀

Consider an example instantiation, where A = {a, b, c}, B = Z, and D = {a, b}. Then, we
have mrg {a 7→ 1, b 7→ 2, c 7→ 3} {a 7→ 7, b 7→ 8, c 7→ 9} = {a 7→ 7, b 7→ 8, c 7→ 3}, which takes
the values of the keys in D from the first function, and the remaining values from the second.
   Every scene induces an equivalence relation on states:

▶ Definition 8 (State Equivalence). s1 ≃F s2 ↔ (mrgF s1 s2 ) = s1

States s1 and s2 are equivalent modulo F when merging the two states yields s1 . This means
that the region of the state space described by F has the same valuation in both s1 and s2 .
For any given scene F , we show that (≃F ) is an equivalence relation on S: it is reflexive,
symmetric, and transitive. We sometimes also use the notation s1 ≃ s2 on F for s1 ≃F s2 .
This relation has a central role in program verification, since it allows us to reason about the
frame of an expression or program: how much of these state is changed.
    Every lens X : V =⇒ S has an underlying scene on S that captures the region of the
state space viewed by X. The scene of a (total) lens X is defined as follows:

▶ Definition 9 (Lens Scene). X ∼ ≜ (λs1 s2 . putX s1 (getX s2 ))

This updates s1 by copying the data located at X from the corresponding data in s2 . It
corresponds to the region of S characterised by X. Any lens satisfying the three lens laws
yields a scene satisfying the three scene laws. We can therefore overload the lens operators
(e.g. ▷◁) to apply to both lenses and scenes. As for lenses, we can also define independence:

▶ Definition 10 (Independence). Scenes F and G over S are independent, written F ▷◁ G,
provided that, for any s1 , s2 , s3 ∈ S, they satisfy G (F s1 s2 ) s3 = F (G s1 s3 ) s2 .

Here, two sets of updates are applied to s1 : F is used to merge with updates from s2 and G is
used to merge the updates from s3 . If these updates commute, then it means that there is no
interference, and so they are independent. This definition also subsumes lens independence:

▶ Theorem 11. X ∼ ▷◁ Y ∼ if and only if putX v1 ◦ putY v2 = putY v2 ◦ putX v1 .

We are therefore justified in substituting lens independence for scene independence. We can
also prove an important theorem linking lens equivalence and scene equality:

▶ Theorem 12 (Lens equivalence is Scene equality). X ≈ Y ←→ X ∼ = Y ∼

Lens equivalence can by characterised by showing that the two underlying scenes are
equal, using the standard homogeneous equality. This means that we can substitute the
heterogeneous lens equivalence with a homogeneous scene equivalence, meaning the simplifier
can be used to reason about lens equivalence. Similarly, we can define an order on scenes:

▶ Definition 13 (Scene Order). F is a subscene of G, written F ≤ G, provided that
mrgF (mrgG s1 s2 ) s3 = mrgG s1 (mrgF s2 s3 ) for any s1 , s2 , s3 ∈ S.
6   Scenes: A Meta-Logical Algebra for Mutable State


    The scene order is reflexive, transitive, and antisymmetric and thus forms a partial order
    on scenes. It also preserves state equivalence: if s1 ≃G s2 , and F ≤ G, then also s1 ≃F s2 .
    Moreover, we have X ⪯ Y if and only if X ∼ ≤ Y ∼ , which validates our order on scenes.
       Scenes are intended to model not just individual lenses, but also sets of lenses. We therefore
    next define a set of Boolean algebra operators for scenes, including complementation.

    ▶ Definition 14 (Scene Boolean Lattice).
                ⊥     = (λs1 s2 . s1 )                ⊤    = (λs1 s2 . s2 )
               F∁     = (λs1 s2 . F s2 s1 )        F ⊔G    = (λs1 s2 . G (F s1 s2 ) s2 )

    The ⊥ scene is the merge function that ignores its second argument, and so takes none
    of s2 . Intuitively, ⊥ is an empty set of lenses. Conversely, ⊤ ignores the first argument,
    and so takes all of the state from s2 . It therefore corresponds to the set of all consistent
    lenses. The complement operator, F ∁ , switches the two arguments of the merge function.
    It corresponds to the set complement, an operator that cannot easily be defined for lenses,
    due to the need to calculate the complement view [21]. The join operator, F ⊔ G, combines
    the two underlying merge functions. It first merges s1 and s2 using F , and then merges the
    resulting state with s2 using G. We can also define a meet operator, F ⊓ G ≜ (F ∁ ⊔ G∁ )∁ .
        Intuitively, ⊔ corresponds to the set union operator, and ⊓ is intersection. These intuitions
    are partly justified and demonstrated in the following algebraic laws:

    ▶ Theorem 15 (Scene Laws).

     ⊤∁ = ⊥       (F ∁ )∁ = F     ⊤⊔F =F ⊔⊤=⊤               ⊥⊔F =F ⊔⊥=F               F ⊔ F∁ = ⊤

                ⊥≤F         F ≤⊤        F ▷◁ F ∁     F ▷◁ G∁ ←→ F ≤ G         s1 ≃⊥ s2

    We also show correspondences between the lens combinators and scenes:

    ▶ Theorem 16 (Lenses as Scenes).

     1∼ = ⊤     0∼ = ⊥    (X ⊕ Y )∼ = X ∼ ⊔ Y ∼ for X ▷◁ Y      s1 ≃X ∼ s2 iff getX s1 = getX s2

    The scene of the identity lens is the top scene, since 1 covers the whole state space. Corres-
    pondingly, the empty lens, 0, views none of the state space. The summation of lenses X
    and Y yields the union of the two underlying scenes, provided X ▷◁ Y . Finally, two states s1
    and s2 are equivalent modulo lens X precisely when applying the underlying getX function
    yields the same value for each state.
        In order to substantiate the intuition of scenes as sets of variables, we would reasonably
    expect that scenes form a complete Boolean algebra. However, this is not the case for the
    set of all scenes, Scene(S). For example, we cannot prove that ⊔ is associative, and several
    other properties do not hold. We therefore need to place additional restrictions on the space
    of scenes. This is because several valid state spaces over S may exist. We can characterise
    whether two scenes address consistent coordinate systems using scene compatibility.

    ▶ Definition 17. Scenes F and G are compatible, written F # G, if F ⊔ G = G ⊔ F .

    Compatibility is specified as commutativity of scene union. This means that the merge
    functions can be applied in either order with the same result, that is, G (F s1 s2 ) s2 =
    F (G s1 s2 ) s2 for any given states s1 and s2 . The intuition here is that F and G both use
    the same coordinate system, and one does not interfere with the other. This is the case if F
    are G are independent, and so we have the result F ▷◁ Q =⇒ F # G. But it is not necessary
Simon Foster, Carlos Isasa, Christian Pardillo Laursen                                              7


for scenes to be independent to be compatible, for example, every scene is self-compatible,
F # F . Similarly, F # F ∁ , ⊤ and ⊥ are both compatible with any scene, and compatibility
is closed under ⊔. Moreover, ⊔ is associative when applied to a set of pairwise compatible
scenes. We also have the following important result:
▶ Theorem 18. Given scenes F # G, s1 ≃(F ⊔G) s2 ←→ (s1 ≃F s2 ∧ s1 ≃G s2 ).
This theorem allows us to decompose state equality according to the scene union operator,
provides that the two scenes F and G are compatible. This theorem allows us to partition
the state, and will form the basis for many of the results in Section 5.
    However, compatibility of scenes is not a given. For example, consider the Cartesian
coordinate lenses xc and yc and the polar coordinate lenses radius and angle from Example 5.
These two pairs of lenses are fundamentally incompatible with each other since, they provide
two different views on the underlying state space. Therefore, we can derive ¬(xc # radius), for
example, since these two lenses interfere with each other’s view. Changing the x-coordinate
affects the radius in the polar coordinate system, and vice-versa. Therefore, when speaking
of a state space, we will be identifying a family of compatible scenes.

 4      Scene Spaces
In this section, we introduce scene spaces, which allow us to characterise consistent subsets
of Scene(S) that satisfy the laws from Boolean algebra and the algebra of sets. We do this
by restriction to subsets of scenes that are pairwise compatible, and thus address a consistent
coordinate system. To introduce scene spaces, we first need to introduction of the scene
basis, which allow us to identify the fundamental set of atomic variables:
▶ Definition 19 (Scene space basis). A sequence of scenes Si ∈ Scene(S), i ∈ {1 · · · n} for
some nonempty set S forms a scene space basis B if it satisfies the following conditions:

     ∀ i, j ≤ n, i ̸= j =⇒ Si ▷◁ Sj (independence); and S1 ⊔ S2 ⊔ · · · ⊔ Sn = ⊤ (coverage)

We define B = {Si | i ∈ {1 · · · n}} as the set of basis scenes. In the context of program
verification, we also call the basis scenes the variables, or Vars, of the program. The use
of a sequence here hints at the needs of the underlying mechanisation — a sequence lets
us ensure that the basis is finite, that it can be used for computation (due to the natural
mapping to lists), and gives us a unique, canonical label for each scene in the basis.
    Intuitively, the set of basis scenes is the collection of atomic state components, or the set
of named variables — each such component uniquely identifies a coordinate in the state space.
The conditions imposed on basis scenes ensures that they do not overlap (independence),
and that together they cover the entire space (coverage) so that every part of the state can
be updated with one of the components. Since every lens can be assigned a scene, we can
also identify the set of basis lenses, as those lenses that have a corresponding basis scene.
    A scene space is the smallest set SB , which contains the basis and is closed under union.
▶ Definition 20 (Scene space). A scene space over B is a finite set SB such that:

             ⊥ ∈ SB ;   If A ∈ B then A ∈ SB ;    If A, B ∈ SB then A ⊔ B ∈ SB .

We encode this in Isabelle as an inductive predicate, which provides an inductive reasoning
principle for reasoning over elements of SB . If we consider the basis scenes as individual,
atomic variables, then each A ∈ SB corresponds to some set of variables, including the empty
set (⊥). All pairs of scenes within a scene space satisfy the core property of compatibility:
8   Scenes: A Meta-Logical Algebra for Mutable State


    ▶ Lemma 21. For any A, B ∈ SB , we have A # B.
    Proof. By induction on the scene space structure of A and B.                                   ◀

    The proof relies on the fact that scene union preserves compatibility, and the basis scenes
    are all compatible due to their pairwise independence. Given this property, we can see that
    scene spaces are better behaved than the set of all scenes of a given type. In particular, we
    now have commutative unions, which allows defininition of the following operator:
    ▶ Definition 22 (Scene Set Union). Given some finite set of scenes S = {S1 , S2 , . . . , Sn } in
                                   S
    some scene space SB we define S = S1 ⊔ S2 ⊔ · · · ⊔ Sn
    This works analogously to the standard finite set union operator. The chosen ordering given
    to the scenes in the finite set S does not matter as scene union commutes within a scene
    space. With this, we can define the decomposition of scenes into their component basis
    scenes. This important result will allow us to justify our intuition of scenes-as-sets:
    ▶ Lemma 23 (Basis decomposition). Given some scene A in scene space SB , its decomposition
    D(A) ∈ P(Scene(S)) is the unique set of scenes satisfying the following properties:
                                         [
                          D(A) ⊆ B          D(A) = A        ⊥∈ / D(A)

    Thus, we can decompose any A ∈ SB into a set of basis scenes. The decomposition is unique
    as every element of SB is built by composition of basis scenes, and we exclude the bottom
    scene. D is an injective function on SB , so we can demonstrate equality of two scenes by
    showing these decompose to the same set. The decomposition gives us a way to relate set
    operations to scene operations, and we find a direct relation between them:

        D(⊤) = B \ {⊥}         D(A ⊔ B) = D(A) ∪ D(B)          D(A ⊓ B) = D(A) ∩ D(B)

                     D(A∁ ) = B \ D(A) \ {⊥}        (A ⊆ B) ⇐⇒ D(A) ⊆ D(B)
    The equalities demonstrate that D is a homomorphism between scene spaces and sets, and
    therefore justifies our use of scenes to characterise sets of variables. We can define the
                                                                          Tn       Sn
    distributed scene intersection by taking advantage of this analogy: i=1 Si ≜ ( i=1 Si∁ )∁ .
                                                                                 S
        This lattice structure allows us to prove the following properties of the operator:
                                 S
    ▶ Lemma 24. s1 ≈ s2 on         X ⇐⇒ (∀ x ∈ X. (s1 ≈ s2 on x))
    This is a generalisation of Theorem 18, but for a subset X ⊆ SB . Similarly, we can prove
    the following law relating the set complement B and the scene complement:
    ▶ Lemma 25 (Scene Complement Union). Given X ⊆ B, the union of the set of all the
    variables B minus X is the complement of the union of X: (B \ X) = ( X)∁
                                                            S           S

    With this, we can show that scene spaces form a complete lattice, where the scene set union
    acts as a supremum, and also a complete Boolean algebra, with A∁ as complementation:
                                                                           S
    ▶ Theorem 26 (Scene Set Complete Boolean Algebra). The operator           together with the
                                  ∁
    ordering ⊆ and complement A induces a complete Boolean algebra on the scene space.
        Thus, with scene spaces we have arrived at sufficient structure on a source S to characterise
    the variables in the state space, the relationship between them (independence and overlap),
    the characterisation of a state space (cf. Definition 4) and the ability to collect them in sets.
    In the next section we will put this theory to work in describing the meta-logical operators
    of a programming reasoning calculus.
Simon Foster, Carlos Isasa, Christian Pardillo Laursen                                             9


 5     Reasoning about Programs
Through scene spaces, we are equipped with a sufficient algebraic structure to develop meta-
logical functions on expressions and programs. Our development is based on the Isabelle/UTP
program model [10], which follows the programs-as-predicates approach [18, 20]. Isabelle/UTP
is an implementation of Hoare and He’s Unifying Theories of Programming [20] semantic
framework in Isabelle/HOL.
     As usual in a shallow embedding, expressions are modelled as functions e : S → V .
Application of a function, e(s), corresponds to evaluation of the expression in a particular
state s ∈ S. For example, given lenses x, y, z : Z =⇒ S, we denote the expression x + y ≤ z
(syntax) by the expression function λs. getx s + gety s ≤ gety s (semantics). Our Shallow
Expressions library manages the automatic translation between these two representations [14].
     Although expression functions represent only semantics, without explicit abstract syntax
tree, scenes allows us to characterise meta-logical properties. The unrestriction operator
a ♯ e [26] describes dependence of an expression on scene a. If e does not make use of any of
the variables of a in its evaluation, then a is unrestricted, that is a ♯ e. This operator has
been formally defined over lenses, but we can now generalise it for scenes.
▶ Definition 27 (Unrestriction). (a ♯ e) ≜ (∀s s′ . e (mrga s s′ ) = e(s))
The expression e is unrestricted by the variables of a if whenever we overwrite the values
with those from another state s′ , the evaluation of e does not change. With this definition,
we can recover the more specific definition of unrestriction for lenses [10]:
▶ Theorem 28. x∼ ♯ e ↔ (∀s v. e (putx s v) = e s)
An expression is unrestricted by a lens, x∼ ♯ e, if evaluating the expression in a state where
x has been modified does not alter the evaluation. Proving an unrestriction conjecture
for a lens is, on the most part, fully automated. In Isabelle this process reduces to β-
reduction and substitution. We can show that if substitution of a lens with an arbitrary
value does not change the valuation of the expression, then the variable is unrestricted,
e.g. (x + y)[z 7→ v] = x + y, and so z ♯(x + y). However, checking that an expression is
not unrestricted by x is, in general, undecidable. We cannot simply check for the presence
of a variable, since this does not guarantee a dependency. For example, the expression
x ≤ 0 ∨ x > 0 reduces to True and so does not depend on x, even though it is mentioned.
    Unrestriction has a deep link with the free variables of an expression. We take the
following definition from André Platzer [28, Definition 8], used in his foundational work on a
uniform substitution principle for differential dynamic. Here, the free variables are those
that influence the evaluation of an expression. With scenes, we define:
▶ Definition 29. F V (e) ≜ {x ∈ B | ∃ s, s′ : s ≈ s′ on x∁ ∧ e(s) ̸= e(s′ )}
                             S

The set of free variables of e is the subset of the basis scenes where there are two states s
and s′ that are equal except on x, but disagree on their evaluation of e, which implies a
dependency. For example, F V (x + y) = {x, y}. From this, we can prove the following lemma:
▶ Lemma 30 (Coincidence Effect for Terms and Formulas). The set of free variables of a
term/formula F V (e) is the smallest set that holds the coincidence effect property:
             [
   s ≈ s′ on    F V (e) =⇒ e(s) = e(s′ )

Which ensures that two states that agree on the free variables of an expression will agree on
the evaluation of that expression. Its usefulness comes from the fact that if all the end states
10   Scenes: A Meta-Logical Algebra for Mutable State


     of two programs always agree on the values of the free variables of an expression, then the
     evaluation of that expression will be the same after any of the two programs.
         We can restate F V using unrestriction:

     ▶ Lemma 31 (Not Unrestricted is Free). F V (e) = {x ∈ V | ¬(x ♯ e)}

     Which implies that checking x ∈ / F V (e) is decidable, since unrestriction is decidable.
        We can use scene spaces to define programs as predicates P (s, s′ ) with s and s′ being
     states. This predicate is true if (s, s′ ) is a valid transition of the program P , i.e. there is
     a valid run of program P with initial state s and final state s′ . Ensuring that a program
     P holds a property F , specified as a boolean expression, is at the core of any verification
     problem. We will use the modal box operator to define this concept:

     ▶ Definition 32 (Box Operator). We say that property F holds for program P , [P ]F , if every
     final state of a valid run of P holds F , that is [P ]F ⇐⇒ ∀s′ P (s, s′ ) : F s′

          Free and bound variables can be used to reason about programs and properties. We
     lift the definitions of free and bound variables of a program from [28, Definition 8]. These
     definitions can be mechanised using scenes:

     ▶ Definition 33. F V (P ) ≜ {x ∈ B | ∃ s0 , s′0 , s1 : s0 ≈ s1 on x∁ ∧ P (s0 , s′0 ) ∧ (∄ s′1 : s′0 ≈
                                    S

     s′1 on x∁ ∧ P (s1 , s′1 ))}

     The free variables of a program are the ones that influence the runs of that program, i.e. the
     variables whose values influence the values of other variables after the program ends.

     ▶ Definition 34. BV (P ) ≜ {x ∈ B | ∃ s0 , s′0 : P (s0 , s′0 ) ∧ ¬(s0 ≈ s′0 on x)}
                                  S

     On the other hand, the bound variables of a program are the ones whose value changes
     through a run of a program. Using these definitions we can demonstrate a simple example:

     ▶ Example 35. Given P ≜ {x := x + 1}, BV (P ) = {x} and F V (P ) = {}.

     As x changes value through the execution of the program and there are no variables that
     influence other variables (x only influences itself). Furthermore, we can prove that free
     variables are the ones that influence the output of a program.

     ▶ Lemma 36 (Coincidence Effect Lemma for Programs). A set of variables S satisfies the
     coincidence effect property of P if s0 ≈ s1 on V ⊇ S and P (s0 , s′0 ), then there is an s′1
                                                            S

     such that P (s1 , s′1 ) and s′0 ≈ s′1 on V . F V (P ) is the smallest such set: F V (P ) ⊆ S.

     This lemma states that if two initial states agree on the free variables of a program, for any
     final state of one we can find a final state of the other that agrees on any superset of the free
     variables, including the entire variable space. The proof of the lemma is split into two parts:
     proving that F V (P ) holds the coincidence lemma and proving that it is the smallest set. For
     the first part, we can prove it using induction over some intermediate states (following the
     original proof [28]). For the second, it can be proven using Definition 33. As an example:

     ▶ Example 37. {} satisfies the coincidence effect property for P ≜ {x := x + 1}.

     As the F V (P ) = {}, it holds per the coincidence effect lemma.
        We can also prove the fact that the initial and final state of any valid transition of a
     program will agree at least in all non-bounded variables.
Simon Foster, Carlos Isasa, Christian Pardillo Laursen                                                 11


▶ Lemma 38 (Bound Effect Lemma for Programs). The set of bound variables of a program
BV (P ) is the smallest set that satisfies the bound effect property:
                             [
   P (s, s′ ) =⇒ s ≈ s′ on ( BV (P ))∁
Which can be proven using Definition 34. As an example:
▶ Example 39. The set {x} satisfies the bound effect property for P ≜ {x := x + 1}.
Which holds as {x} corresponds to the bound variables of P .
   Using these two lemmas and the definitions of bound and free variables we can prove
foundational properties that are widely applied in program verification. For example:
▶ Lemma 40. Given two programs P and Q, if BV (P ) ∩ BV (Q) = ∅, F V (P ) ∩ BV (Q) = ∅
and BV (P ) ∩ F V (Q) = ∅, then P ; Q = Q; P .
As the free variables are the ones that influence the runs of the programs and the bound
variables are the ones that change, if these two sets are pairwise disjoint, the changes that P
makes do not influence Q and vice-versa. Furthermore, since the bound variables are also
disjoint, Q does not overwrite the changes that P makes and vice-versa.
    In order to further showcase the power of scenes we define a simple composition operator
and prove some properties about it. This operator, P ∥ Q, merges over the bound variables
of the different processes in the parallel composition. We are going to use a simplified version
of the one defined in [4] with no trace or communication. We will prove that it holds two
desirable properties: parallel injection and parallel decomposition
    First, parallel injection states that if [P ]F and Q does not-interfere (i.e. runs of this
program do not affect the truth value of this program), then [P ∥ Q]F . We can can
characterize non-interference using free and bound variables:
▶ Definition 41 (Non-interference). Program P does not interfere with formula F if BV (P ) ∩
F V (F ) = ∅
The set BV (P ) contains the variables that can be affected by running P while F V (F )
contains the variables that influence the value of F , so if these two sets are disjointed, we
achieve what we want, runs of P will not influence the value of F .
   Second, parallel decomposition states the fact that if P does not interfere with FQ and Q
does not interfere with FP , then [P ]FP and [Q]FQ are sufficient to state [P ∥ Q](FP ∧ FQ ).
Parallel decomposition is a powerful property to have, as it allows us to decompose safety
properties of the parallel composition into properties that hold for the partial programs and
decompose a proof of safety for the composition into one of the partial programs.
   We define the parallel composition as follows:
▶ Definition 42 (Simple Parallel Operator). The parallel operator, P ∥ Q is a parallel-by-merge
operator [20] that merges P and Q over the bound variables of P
                                                   [
   (P ∥ Q)(s, s′ ) ⇐⇒ ∃ sP , sQ . s′ = sQ ◁ sP on BV (P ) ∧ P (s, sP ) ∧ Q(s, sQ )
Here, s1 ◁ s2 on A is notation for mrgA P Q. This parallel operator splits the state into two,
the variables bounded by P and the rest. It runs both programs independently and then it
merges the state, taking the values of the bound variables of P from P itself and the rest
from Q.
   For example, given variables x, y, z and the program P ≜ {x := z ∥ y := z} that assigns
x and y to z in parallel, it will have as valid runs any pair of states (s, s′ ) where s′ [x] = s[z]
and s′ [y] = s[z].
   Our parallel operator commutes given that the programs do not share bound variables:
12   Scenes: A Meta-Logical Algebra for Mutable State


     ▶ Lemma 43 (Commutativity of ∥). Given that BV (P ) ∩ BV (Q) = ∅, P ∥ Q = Q ∥ P
     This holds by the bound effect lemma (Lemma 38) and the definition of the parallel operator.
     As P and Q are merged over the bound variables of P , and as Q can only affect variables in
     BV (Q), if these two sets are disjoint the operator commutes.
         In order to prove both parallel injection and decomposition we need to discuss the final
     states of the programs that make up the parallel composition. We can mechanise them using
     scenes:
     ▶ Definition 44 (Partial Left and Partial Right). For a valid run of the parallel composition P ∥
     Q (s, s′ ), we define a partial left state, sP as any state that holds P (s, sP )∧s′ ≈ s on
                                                                                                 S
                                                                                                   BV (P )
                                                                                                  ∁
     and a partial right state sQ as any state that holds Q(s, sQ ) ∧ s′ ≈ s on ( BV (P ))
                                                                                         S

         With these definitions we can reason about the final states of the parallel composition
     using the final states of the programs that take part in the composition. Specifically, we can
     show the following result:
     ▶ Lemma 45. For all s, s′ and sP s.t. (P ∥ Q)(s, s′ ) and sP is a partial left, we have:
                      [            ∁
        s′ ≈ sP on         BV (Q)

     First by the definition of the parallel operator, s′ ≈ sP on BV (P ) so the states also agree on
     BV (P ) ∩ (BV (Q))∁ . Second, s ≈ sP on (BV (P ))∁ by the bound effect lemma, and for all
     partial right states sQ we can make the same argument s ≈ sQ on (BV (Q))∁ , which means
     that sP ≈ sQ on (BV (P ))∁ ∩ (BV (Q))∁ . Finally, sQ ≈ s′ on (BV (P ))∁ by the definition of
     the parallel operator, so sP ≈ s′ on (BV (P ))∁ ∩ (BV (Q))∁ . Putting everything together we
     have sP ≈ s′ on (BV (P ) ∩ (BV (Q))∁ ) ∪ ((BV (P ))∁ ∩ (BV (Q))∁ ) = (BV (Q))∁ . And as a
     direct consequence we have
     ▶ Lemma 46 (Non-interference Preserves Safety). For any pair of states belonging to the
     parallel composition (P ∥ Q)(s, s′ ) with partial left sP , given that Q does not interfere with
     formula F , s′ JF K holds if and only if sP JF K.
                                   S             S          ∁
     As due to non-interference F V (F ) ≤ ( BV (Q)) and the lemma holds by coincidence.
         Finally, using the box operator and the previous lemma we can obtain the parallel
     injection property:
     ▶ Theorem 47 (Parallel Injection). Given that Q does not interfere with formula F , [P ]F =⇒
     [P ∥ Q]F
     The power of this theorem is tied to the fact that it allows us to verify properties about
     programs in a parallel composition without having to use the definition of the operator:
     ▶ Example 48. Let P ≜ {x := y + 1}, Q ≜ {z := y + 1} and F ≜ x > y. Q does not interfere
     with F as BV (Q) = {z} and F V (F ) = {x, y} and [P ]F trivially, then [P ∥ Q]F .
        Finally, with the previous lemma and commutativity:
     ▶ Theorem 49 (Parallel Decomposition). Given that P does not interfere with formula FQ
     and Q does not interfere with formula FP , [P ]FP ∧ [Q]FQ =⇒ [P ∥ Q](FP ∧ FQ )
     With this last theorem, we can conclude that scenes, via the definitions of free and bound
     variables, allow us to reason about parallel programs (defined through Definition 42) compos-
     itionally. Further examples on how to use free and bound variables to enable compositional
     reasoning can be seen in the proofs of soundness of dLCHP [4] and dL [28].
Simon Foster, Carlos Isasa, Christian Pardillo Laursen                                               13


 6     Related Work
We previously surveyed different approaches to state space modelling in proof assistants [10,
Section 2.4], using Schirmer and Wenzel’s categories as a framework [29]. They identify
four approaches employed in developing verification tools: state as a (1) function; (2) tuple;
(3) record; and (4) abstract type. Lenses unify these different approaches by providing an
algebraic account of state that does not depend on a particular model [10]. In particular,
Isabelle/UTP is a confluence of ideas from Oliveira [26] et al. and Feliachi et al. [8] in their
previous respective mechanisations of the UTP. Scenes build on this by allowing lenses to be
collected in sets, and without any loss of generality in our previous work. Crucially, scenes
avoid the need to formalise (1) names for variables and (2) a value universe for the state
model, which is necessary for a shallow embedding.
    The term “lens” originates in the work of Nate Foster [9], and lenses are now ubiquitous
in functional programming. The idea of using algebra to provide a foundation for state space
modelling is well-known in the literature, going back to the work of Tarski [19] and Oles [25].
Notably, Back and von Wright [2] use essentially the same algebraic structure [10] to lenses to
model variables in their refinement calculus. Hayes [17, 5] et al. have also employed similar
algebraic properties, including unrestriction, in the context of rely-guarantee reasoning for
shared variable concurrency. Also in this line, Dongol et al. [7] use a functional state space
and mechanised algebra to implement cylindrical algebra in Isabelle/HOL, which is then
extended for programs and used to model concepts like local variables. Similarly, Platzer
uses the algebraic properties of variables to formulate properties of hybrid programs for his
uniform substitution calculus [28]. Our work on lenses and scenes allows these ideas to be
generalised and put to work in the context of verification tools in proof assistants.


 7     Conclusions
We have introduced scenes as a meta-logical algebra for reasoning about mutable state.
Though based on an elementary algebraic foundation, they allow us to model sets of variables
in the context of a shallow embedding, and thus allow us to support laws of programming that
depend on the program frame. These results on scenes form part of our Optics library [15]
for Isabelle/HOL, and our Isabelle/UTP relational program model [10].
    In future work, we are using our mechanisation of BV and F V as a foundation to
implement Brieger’s dLCHP [3] in Isabelle/HOL. In parallel with this, we are currently
developing automation support for generation of scene spaces in Isabelle/HOL. For example,
while calculation of x ∈/ F V (e) can be automated through unrestriction, calculating F V (e)
itself requires further proof methods. In a different axis, we are also currently developing a
port of the Optics library in Lean, so that our results can have more reach.


      References
 1   Jean-Raymond Abrial. Modeling in Event-B: System and Software Engineering. Cambridge
     University Press, Cambridge, 2010. doi:10.1017/CBO9780511778841.
 2   R.-J. Back and J. von Wright. Refinement Calculus: A Systematic Introduction. Springer,
     1998.
 3   Marvin Brieger, Stefan Mitsch, and André Platzer. Uniform substitution for dynamic logic with
     communicating hybrid programs. In Brigitte Pientka and Cesare Tinelli, editors, Automated
     Deduction – CADE 29, volume 14132 of LNCS, pages 96–115. Springer, 2023. doi:10.1007/
     978-3-031-38499-8_6.
14   Scenes: A Meta-Logical Algebra for Mutable State


      4   Marvin Brieger, Stefan Mitsch, and André Platzer. Complete dynamic logic of communicating
          hybrid programs, 2025. URL: https://arxiv.org/abs/2408.05012, arXiv:2408.05012.
      5   R. J. Colvin, I. J. Hayes, and L. A. Meinicke. Designing a semantic model for a wide-spectrum
          language with concurrency. Formal Aspects of Computing, 2017.
      6   Leonardo de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob von Raumer.
          The lean theorem prover. In Automated Deduction – CADE-25, pages 378–388. Springer
          International Publishing, 2015. doi:10.1007/978-3-319-21401-6_26.
      7   B. Dongol, I. Hayes, L. Meinicke, and G. Struth. Cylindric Kleene lattices for program
          construction. In MPC, volume 11825 of LNCS, pages 192–225. Springer, October 2019.
      8   A. Feliachi, M.-C. Gaudel, and B. Wolff. Unifying theories in Isabelle/HOL. In UTP 2010,
          volume 6445 of LNCS, pages 188–206. Springer, 2010.
      9   J. Foster, M. Greenwald, J. Moore, B. Pierce, and A. Schmitt. Combinators for bidirectional
          tree transformations: A linguistic approach to the view-update problem. ACM Trans. Program.
          Lang. Syst., 29(3), May 2007. URL: http://doi.acm.org/10.1145/1232420.1232424, doi:
          10.1145/1232420.1232424.
     10   S. Foster, J. Baxter, A. Cavalcanti, J. Woodcock, and F. Zeyda. Unifying semantic foundations
          for automated verification tools in Isabelle/UTP. Science of Computer Programming, 197,
          October 2020. doi:10.1016/j.scico.2020.102510.
     11   S. Foster, A. Cavalcanti, S. Canham, J. Woodcock, and F. Zeyda. Unifying theories of reactive
          design contracts. Theoretical Computer Science, 802:105–140, January 2020.
     12   S. Foster, C.-K. Hur, and J. Woodcock. Unifying model execution and deductive verification
          with Interaction Trees in Isabelle/HOL. ACM Trans. on Software Engineering Methodology
          (TOSEM), 2024.
     13   S. Foster, Y. Nemouchi, C. O’Halloran, K. Stephenson, and N. Tudor. Formal model-based
          assurance cases in Isabelle/SACM: An autonomous underwater vehicle case study. In Proc.
          8th Intl. Conf. on Formal Methods in Software Engineering (FormaliSE). ACM, 2020.
     14   Simon Foster. Shallow expressions. Archive of Formal Proofs, May 2025. https://isa-afp.
          org/entries/Shallow_Expressions.html, Formal proof development.
     15   Simon Foster, Christian Pardillo-Laursen, and Frank Zeyda. Optics. Archive of Formal Proofs,
          May 2017. https://isa-afp.org/entries/Optics.html, Formal proof development.
     16   N. Fulton, S. Mitsch, J.-D. Quesel, M. Völp, and A. Platzer. KeYmaera X: An axiomatic
          tactical theorem prover for hybrid systems. In A. P. Felty and A. Middeldorp, editors,
          CADE, volume 9195 of LNCS, pages 527–538, Heidelberg, 2015. Springer. doi:10.1007/
          978-3-319-21401-6_36.
     17   I. J. Hayes. Generalised rely-guarantee concurrency: an algebraic foundation. Formal Aspects
          of Computing, 28(6):1057–1078, 2016.
     18   E. C. R. Hehner. A Practical Theory of Programming. Springer, 1993.
     19   L. Henkin, J. Monk, and A. Tarski. Cylindric Algebras, Part I. North-Holland, 1971.
     20   C. A. R. Hoare and J. He. Unifying Theories of Programming. Prentice-Hall, 1998.
     21   Martin Hofmann, Benjamin C. Pierce, and Daniel Wagner. Symmetric lenses. ACM SIGPLAN
          Notices, 46(1):371–384, January 2011. doi:10.1145/1925844.1926428.
     22   Jonathan Julián Huerta y Munive, Simon Foster, Mario Gleirscher, Georg Struth, Chris-
          tian Pardillo Laursen, and Thomas Hickman. IsaVODEs: Interactive verification of
          cyber-physical systems at scale. Journal of Automated Reasoning, 68(4):21, 2024. doi:
          10.1007/s10817-024-09709-2.
     23   John M. Lee. Introduction to Smooth Manifolds, volume 218 of Graduate Texts in Mathematics.
          Springer Science & Business Media, New York, NY, second edition, 2012. doi:10.1007/
          978-1-4419-9982-5.
     24   T. Nipkow, M. Wenzel, and L. C. Paulson. Isabelle/HOL: A Proof Assistant for Higher-Order
          Logic, volume 2283 of LNCS. Springer, 2002.
     25   Frank Oles. A Category-Theoretic Approach to the Semantics of Programming Languages.
          PhD thesis, Syracuse University, 1982.
Simon Foster, Carlos Isasa, Christian Pardillo Laursen                                              15


26   M. Oliveira, A. Cavalcanti, and J. Woodcock. Unifying theories in ProofPower-Z. In UTP
     2006, volume 4010 of LNCS, pages 123–140. Springer, 2007.
27   André Platzer. Logical Foundations of Cyber-Physical Systems. Springer, Heidelberg, 2018.
28   André Platzer. A Complete Uniform Substitution Calculus for Differential Dynamic
     Logic. Journal of Automated Reasoning, 59(2):219–265, August 2017. doi:10.1007/
     s10817-016-9385-1.
29   N. Schirmer and M. Wenzel. State spaces – the locale way. In SSV 2009, volume 254 of
     ENTCS, pages 161–179, 2009.
30   The Coq/Rocq Development Team. The Coq/Rocq Proof Assistant Reference Manual. Inria,
     2024. Available at https://coq.inria.fr/distrib/current/refman/.
31   Fang Yan, Simon Foster, and Ibrahim Habli. Automated compositional verification for
     robotic state machines using isabelle/hol. In Yamine Aït-Ameur, Ferhat Khendek, and
     Dominique Méry, editors, 27th International Conference on Engineering of Complex Computer
     Systems, ICECCS 2023, Toulouse, France, June 14-16, 2023, pages 167–176. IEEE, 2023.
     doi:10.1109/ICECCS59891.2023.00029.
32   Kangfeng Ye, Jim Woodcock, and Simon Foster. Probabilistic unifying relations for modelling
     epistemic and aleatoric uncertainty: Semantics and automated reasoning with theorem proving.
     Theoretical Computer Science, 1021:114876, 2024. URL: https://www.sciencedirect.com/
     science/article/pii/S0304397524004936, doi:10.1016/j.tcs.2024.114876.
