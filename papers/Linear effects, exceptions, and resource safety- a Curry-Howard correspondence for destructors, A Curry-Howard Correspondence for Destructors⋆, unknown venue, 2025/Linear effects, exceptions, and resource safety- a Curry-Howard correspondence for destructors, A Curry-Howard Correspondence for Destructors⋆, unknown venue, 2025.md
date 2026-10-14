                                                 Linear Effects, Exceptions, and Resource Safety
                                                    A Curry-Howard Correspondence for Destructors⋆

                                                Sidney Congard1,2 , Guillaume Munch-Maccagnoni1 , and Rémi Douence2
                                                                      1
                                                                          INRIA, LS2N CNRS, Nantes, France
                                                                           2
                                                                             IMT Atlantique, Nantes, France

                                                                                  January 25, 2026
arXiv:2510.23517v2 [cs.PL] 21 Apr 2026




                                                 Abstract. We analyse the problem of combining linearity, effects, and exceptions,
                                                 in abstract models of programming languages, as the issue of providing some kind
                                                 of strength for a monad 𝑇 (− ⊕ 𝐸) in a linear setting. We consider in particular for
                                                 𝑇 the allocation monad, which we introduce to model and study resource-safety
                                                 properties. We apply these results to a series of two linear effectful calculi for
                                                 which we establish their resource-safety properties. The first calculus is a linear
                                                 (optionally ordered) call-by-push-value language with two allocation effects 𝐧𝐞𝐰
                                                 and 𝐝𝐞𝐥𝐞𝐭𝐞. The resource-safety properties follow from the linear and ordered
                                                 character of the typing rules.
                                                      We then integrate exceptions with linearity and effects by adjoining default
                                                 destruction actions to types, as inspired by C++/Rust destructors. We see destruc-
                                                 tors as objects 𝛿 ∶ 𝐴 → 𝑇 𝐼 in the slice category over 𝑇 𝐼. This construction gives
                                                 rise to a second calculus, the resource call-by-push-value, featuring exceptions
                                                 and destructors, and whose weakening and exchange rules perform side-effects.
                                                 It is therefore affine at the level of types but ordered at the level of derivations.
                                                 As in C++ and Rust, a “move” operation—the side-effecting exchange rule—is
                                                 necessary for releasing resources in random order, as opposed to LIFO order.


                                         1    Introduction

                                         The application of monads to study effects in programming languages [38, 39, 15, 49,
                                         46, 31, 30], as well as the application of linearity to study resource-sensitive aspects of
                                         computation [19, 29, 3, 14, 33, 5, 26], are well-established. However, the combination of
                                         effects and resources, despite receiving some attention [50, 22, 23, 51, 36, 37, 11], has
                                         much less developed theory and case studies.
                                             In order to understand why the combination of effects and resources poses new
                                         challenges, it is useful to remind that a monad 𝑇 modelling computational effects is given
                                         by an endofunctor on a cartesian category C, together with families of maps

                                                       𝜂𝐴 ∶ 𝐴 → 𝑇 𝐴                   and                𝜇𝐴 ∶ 𝑇 𝑇 𝐴 → 𝑇 𝐴                (1)
                                         ⋆
                                             Slightly longer version with more details of a paper that appeared in ESOP 2026 with
                                             the same title (https://doi.org/10.1007/978-3-032-22720-1_8). To cite this version:
                                             https://doi.org/10.48550/arXiv.2510.23517.
natural in 𝐴 ∈ C and satisfying monoid-like laws, and together with a family of maps
called strength
                             𝜎Γ,𝐴 ∶ Γ × 𝑇 𝐴 → 𝑇 (Γ × 𝐴)                           (2)
natural in Γ ∈ C and 𝐴 ∈ C and satisfying four laws stating the compatibility with 𝜂, 𝜇
and with the monoidal structure induced by × and 1. The general principle is that two
typed expressions of type Γ ⊢ 𝐴 and Γ, 𝐴 ⊢ 𝐵 are allowed to compose as follows:
      Γ⊢𝑡∶𝐴         and       Γ, 𝑥 ∶ 𝐴 ⊢ 𝑢 ∶ 𝐵          ⇐⇒      Γ ⊢ let 𝑥 = 𝑡 in 𝑢 ∶ 𝐵    (3)
which reflects in their interpretation as morphisms in the Kleisli category of 𝑇
             J𝑡K ∶ Γ → 𝑇 𝐴                  and               J𝑢K ∶ Γ × 𝐴 → 𝑇 𝐵
through the ability to select 𝑥 in 𝑢 where the strength plays an essential role:
                                            𝜎Γ,𝐴              𝑇 J𝑢K         𝜇𝐵
           Jlet 𝑥 = [ ] in 𝑢K ∶ Γ × 𝑇 𝐴 ←←←←←←←←→
                                                ← 𝑇 (Γ × 𝐴) ←←←←←←←←→
                                                                    ← 𝑇 𝑇 𝐵 ←←←←←→
                                                                                 ← 𝑇𝐵 .   (4)
    It is also useful to remind that the application of linearity to model resource-sensitive
phenomena of data and computation requires to move from a cartesian category ( C, ×, 1)
to a symmetric monoidal category ( C, ⊗, 𝐼). This modification gives control over du-
plication and erasure (corresponding to contraction and weakening in logic) since the
maps
                  𝐴→𝐴⊗𝐴                         and                   𝐴→𝐼                 (5)
are no longer available for a general 𝐴. The linear logic viewpoint nevertheless subsumes
the cartesian viewpoint using a resource modality “!”. Such a resource modality is
a comonad such that its Eilenberg-Moore category C! , whose objects are coalgebras
(𝐴, 𝜏 ∶ 𝐴 → !𝐴), has a symmetric monoidal structure that coincides with the symmetric
monoidal structure of C in terms of the underlying objects, and such that this symmetric
monoidal structure on C! is cartesian [34, 35]. Concretely, duplication and erasure (5)
are available whenever 𝐴 is given with a map 𝜏 ∶ 𝐴 → !𝐴 satisfying two laws of
compatibility with the comonad structure. More rarely—but importantly in our story—
the symmetric monoidal structure is sometimes replaced by a monoidal structure, which
amounts to providing control over the exchange rule in logic since the symmetry
                                      𝐴⊗𝐵 →𝐵⊗𝐴                                            (6)
is no longer available unconditionally. The corresponding logics are called ordered
instead of linear. But again, the exchange rule can be reintroduced selectively with a
resource modality [21]. Ordered logic can be useful to model the order in the release of
resources [47, 48, 58], as we will see again in this paper.

1.1   Linear effects
In this context, it is tempting to define a notion of linear computational effect to be given
again by a monad (𝑇 , 𝜂, 𝜇) (1) on C and a strength now given as a family of maps
                                𝜎Γ,𝐴 ∶ Γ ⊗ 𝑇 𝐴 → 𝑇 (Γ ⊗ 𝐴)                                (7)
natural in Γ and 𝐴 and satisfying the same four laws. It is also called a left strength


                                                  2
when the monoidal structure ⊗ is non-symmetric. An example of such a strong monad
is the linear state monad 𝑆 ⊸ (− ⊗ 𝑆) for any 𝑆 ∈ C in any symmetric monoidal
closed category C. This transposition to the linear context of computational effects is
well-behaved and works similarly to (non-linear) monadic effects [49, 22].
    Unfortunately, important examples of effects in models of linear logic do not have
a strength (7) in such a restrictive sense, such as the control effects modelled by the
following monads in models of linear logic [8, 22, 23]:
     ∙ the monad “?” of linearly-defined continuations (but not linearly-used) ?𝐴 ≝ !(𝐴 ⊸
       ⊥) ⊸ ⊥, whose effect corresponds to call/cc-style control operators;
     ∙ for any object 𝐸, the exception monad  ≝ (− ⊕ 𝐸), which is used to model error
       types and exceptions with ⊕ the categorical coproduct—the focus of this paper.
At this point, it is instructive to go back to the computational intuition behind the strength
with the interpretation of the monadic binding (4, where × is now replaced by ⊗). We
can see that the parameter Γ in (7) represents the context of variables in the rest of the
computation (let 𝑥 = [ ] in 𝑢) at the location where an effect is performed. But control
effects have this particularity that they can change how many times the rest is computed,
so we cannot guarantee that variables in Γ are not duplicated nor erased.

1.2     Strength with respect to a resource modality
In fact, starting from this intuition we can suggest a relaxed notion of strength, something
like (7) where Γ is assumed to possess a coalgebra structure 𝜏 ∶ Γ → !Γ, so that it can
be erased. It so happens [8, 22, 23] that the monad ? of linearly-defined continuations
and the exception monad  each do have a (left) strength with respect to 𝑈 ! , where
𝑈 ! ∶ C! → C is the forgetful functor of the category of coalgebras,3 defined as a family
of maps
                              𝜎Γ,𝐴 ∶ 𝑈 ! Γ ⊗ 𝑇 𝐴 → 𝑇 (𝑈 ! Γ ⊗ 𝐴)                          (8)

natural in Γ ∈ C! and 𝐴 ∈ C and satisfying again four laws of compatibility with 𝜂,
𝜇 and with the monoidal structures of C and C! . If we look concretely at the strength
with respect to 𝑈 ! of the exception monad , we see that it consists for each 𝐴 ∈ C and
Γ ∈ C! of two maps

         𝑈 ! Γ ⊗ 𝐴 → (𝑈 ! Γ ⊗ 𝐴) ⊕ 𝐸              and         𝑈 ! Γ ⊗ 𝐸 → (𝑈 ! Γ ⊗ 𝐴) ⊕ 𝐸           (9)

corresponding respectively to the normal case and the exceptional case describing the
propagation of the exception, whose copairing must be subject to the mentioned naturality
and coherence conditions. The normal case is given by the left inclusion whereas the
exceptional case is obtained from 𝑈 ! Γ ⊗ 𝐸 → 𝐸, which follows from the erasure (5)
given the hypothesis that the monoidal structure on C! is cartesian. We are now ready
to make an important observation: for the purpose of deriving a strength (8) we could
consider other resource modalities than !; for instance the hypothesis that C! is semi-
cartesian suffices (the monoidal unit of C! being a terminal object). This amounts to
 3
     The cited authors actually consider this notion for the Kleisli adjoint resolution of !, but it can
     be defined similarly for any adjoint resolution, and even any strong monoidal functor 𝑈 .


                                                    3
replacing ! in (8) with an affine resource modality that permits erasure but not duplication
in (5).
      Now that we have described a relaxed notion of strength for the monad of linearly-
defined continuations and the exception monad in a linear context, we have to mention
how restrictive a strength (8) seems to be in light of the interpretation of composition (3).
The notion of strength with respect to ! amounts to precluding any linear variable from
appearing in the monadic binding (4), in other words linear variables can only appear in Γ
if it can be ensured that no control effect is performed. This models a restrictive approach
in which linearity and control effects are exclusive with one another (see section 6).

1.3   Destructors
It is now clear that linearity and control effects do not mix well, or so it seems. Our
goal is to show how linearity and exceptions can actually be mixed in more important
situations than it seems, with a technique that we explain abstractly but that has been
discovered from practical consideration in the context of resource management by the
designers of the C++ programming language [28, 52, 24]. (We are deferring the more
historical discussion to section 6.)
     The starting point for describing this important discovery is to assume a linear model
of computation as above given by a symmetric monoidal closed category C together
with a given notion of linear effect, that is, a given monad 𝑇 on C with a strength (7). As
we have explained, this is a notion of linear model with linear effect which has previously
been studied [49, 22, 36]; in particular a concrete model of computation is given by a
linear call-by-push-value (linear CBPV) calculus [11] that will provide the basis of a
first linear calculus we study.
     In this model, we are interested in integrating exceptions. Assuming C has finite
coproducts and that tensor products distribute over the coproducts, this means that we
want to combine the monad 𝑇 and the exception monad  into a strong monad 𝑇 .
Remember that as a general principle of the exception monad, 𝑇  has a monad structure
arising from a distributive law of monads 𝑇 → 𝑇 . However we meet again the obstacle
that  does not have a strength in general, so we cannot obtain a strength for 𝑇  by
composition.
     But it might still be the case that 𝑇  has some kind of strength. This amounts to
finding for all 𝐴 ∈ C something like
                           Γ ⊗ 𝑇 (𝐴 ⊕ 𝐸) → 𝑇 ((Γ ⊗ 𝐴) ⊕ 𝐸)                              (10)
for which, given that 𝑇 is strong, it suffices to find maps
       Γ ⊗ 𝐴 → 𝑇 ((Γ ⊗ 𝐴) ⊕ 𝐸)              and        Γ ⊗ 𝐸 → 𝑇 ((Γ ⊗ 𝐴) ⊕ 𝐸)
subject to some conditions. The one on the left-hand side—the normal return—is obtained
in a straightforward manner by inclusion and unit of 𝑇 . For the one on the right-hand
side—the exceptional return—observe that the difference with (9) is the presence of
𝑇 on the right-hand side. This second type suggests that Γ has to be erasable, but that
erasure is allowed to perform effects in 𝑇 . Indeed, observe that the second map above
can be derived if Γ is provided with some map Γ → 𝑇 𝐼. We call such an erasure map
that performs an effect a destructor, by analogy with C++ destructors.


                                             4
1.4    The monoidal category of destructors
The desire to find a strength for 𝑇  therefore suggests to consider for Γ in (10) an object
with a given destructor 𝛿 ∶ Γ → 𝑇 𝐼, that is to say an object in the slice category C∕𝑇 𝐼 .
Recall that it is the category whose objects are arbitrary pairs (𝐴 ∈ C, 𝛿 ∶ 𝐴 → 𝑇 𝐼),
and whose morphisms are morphisms in C that preserve the second component 𝛿. The
slice category C∕𝑇 𝐼 enjoys a series of nice properties, the most striking one being that it
gives rise to a resource modality on C [10]. Indeed:
  ∙ C∕𝑇 𝐼 has a monoidal structure arising from the monoid structure on 𝑇 𝐼:
                                    𝜎𝑇 𝐼,𝐼                 ≅        𝜇
                                           ← 𝑇 (𝑇 𝐼 ⊗ 𝐼) ←←←→
                        𝑇 𝐼 ⊗ 𝑇 𝐼 ←←←←←←←←←→                ← 𝑇 𝑇 𝐼 ←←←→
                                                                       ← 𝑇𝐼

      The monoidal unit is given by (𝐼, 𝜂𝐼 ∶ 𝐼 → 𝑇 𝐼) and, for (𝐴, 𝛿𝐴 ∶ 𝐴 → 𝑇 𝐼) and
      (𝐵, 𝛿𝐵 ∶ 𝐵 → 𝑇 𝐼), the tensor product is given by:
                                                  𝛿𝐴 ⊗𝛿𝐵
                     (𝐴 ⊗ 𝐵, 𝛿𝐴⊗𝐵 ∶ 𝐴 ⊗ 𝐵 ←←←←←←←←←←←←→
                                                      ← 𝑇 𝐼 ⊗ 𝑇 𝐼 → 𝑇 𝐼) .

    In words, 𝐴 ⊗ 𝐵 has a canonical destructor which releases 𝐵 and 𝐴, as we will see
    in the reverse order of allocation.
  ∙ We also observe that there is a strong monoidal functor 𝑈 ∶ C∕𝑇 𝐼 → C, that sends
    the monoidal structure of C∕𝑇 𝐼 to the one of C (strictly so).
  ∙ If we assume that C has finite products that we note (&, ⊤), then 𝑈 has a right adjoint
    𝐺 ∶ C → C∕𝑇 𝐼 sending objects 𝐴 ∈ C to

                           (𝐴 & 𝑇 𝐼, 𝜋2 ∶ 𝐴 & 𝑇 𝐼 → 𝑇 𝐼) ∈ C∕𝑇 𝐼                       (11)

    and morphisms 𝑓 ∶ 𝐴 → 𝐵 to 𝑓 & 𝑇 𝐼. In particular if we note  ≝ 𝑈 𝐺 the
    comonad on C associated to the adjunction, one has  = (− & 𝑇 𝐼) as our resource
    modality.
  ∙ The latter adjunction is comonadic: C∕𝑇 𝐼 ≃ C . This can be observed from the fact
    that a coalgebra (𝐴, 𝜏 ∶ 𝐴 → 𝐴) for  boils down to an object 𝐴 provided with a
    morphism 𝐴 → 𝑇 𝐼 in C without any other condition.
This setup was advocated as a starting point to study C++ destructors in [10].
    At this stage we find it useful to sum up the assumptions on C: a distributive symmetric
monoidal category with finite products and a chosen strong monad 𝑇 . In particular any
model of linear logic or intuitionistic linear logic is suitable (where 𝑇 can be any linear
state monad, for instance). We have just established that in those models,  = (− & 𝑇 𝐼)
has the structure of a resource modality whose Eilenberg-Moore category is (equivalent
to) C∕𝑇 𝐼 .
    It is a nice exercise to check that this setup indeed gives a strength for the composite
monad 𝑇  with respect to 𝑈 ∶ C∕𝑇 𝐼 → C, more precisely:
Theorem 1. Let 𝐸 ∈ C,  the exception monad − ⊕ 𝐸, and 𝑇  the monad obtained
from the distributive law of monads 𝑇 → 𝑇 . Then the monad 𝑇  underlies a strong
monad on the C+-category ( C∕𝑇 𝐼 , ∗), in the terminology of Melliès [36], where ∗ is the
pseudo-action defined by composition with −1 ∗ −2 ≝ (𝑈 −1 ) ⊗ −2 .


                                              5
     Now, unlike usual resource modalities that add duplication and/or erasure (5), C∕𝑇 𝐼
is in general not cartesian nor even semi-cartesian. In fact, its monoidal structure is not
even symmetric (unless 𝑇 is commutative). Indeed, 𝛿𝐴⊗𝐵 and 𝛿𝐵⊗𝐴 can in general be
distinguished by the order in which the effects of 𝛿𝐴 and 𝛿𝐵 are performed.
     Nevertheless, just as linear models with a resource modality “!” give rise to an
intuitionistic model by the Girard translations [19], one can build an ordered CBPV
model whose (positive) objects are those of C∕𝑇 𝐼 , as an instance of a general principle
generalising the Girard translation [36, 11] applied to the resource modality . This
motivates the study of a second calculus after the first one, whose (positive) types are
supplied with a destructor and whose effects include those of 𝑇 and exceptions.


1.5   Modelling resources with the allocation monad

In this new context, notice that everything is linear in the sense that we did not make
use of a resource modality “!”. We set out to show how resource-safety properties are
thus ensured by construction. Resource management in programming aims to ensure
the correct allocation, use, and release of resources, which are transient values denoting
the validity of some state (a memory allocation, a lock, or typically resources from the
operating system). The need for correct resource management in programming further
complicates the problems with mixing linearity and control: indeed, a need to handle
errors arises from the possibility that resource acquisition can fail, whereas a need for
linearity arises from the fact that the resources must be released in a timely fashion and
no more than once.
    We introduce the allocation monad as a way to model resource management and
state and establish resource-safety properties. The allocation monad will play the role of
𝑇 in the slice category C∕𝑇 𝐼 . We first assume given an atomic type 𝑅 of resources and
ask for two effectful operations:

  ∙ 𝐧𝐞𝐰 ∶ 𝐼 ⊸ 𝑅 ⊕ 𝐼 acquires a resource, or fails if there are no resources available.
    Later on, it will also be given with type 𝐼 ⊸ 𝑅 when the failure can be represented
    with an exception;
  ∙ 𝐝𝐞𝐥𝐞𝐭𝐞 ∶ 𝑅 ⊸ 𝐼 releases the given resource without fail.

Notice that no operation is given for interacting with resources: we are only interested in
observing resource-safety properties of the program state arising from the (correct) use of
𝐧𝐞𝐰 and 𝐝𝐞𝐥𝐞𝐭𝐞. Notice also that we represent failure with an explicit use of the exception
monad  = (− ⊕ 𝐸) for 𝐸 ≝ 𝐼 as an error type. But using an error type explicitly is not
a solution to the lack of exceptions since we can expect similar obstacles to programming
to arise from the lack of general strength for  (see discussion in section 6).
    To implement those effectful operations, we then define the allocation monad as the
linear state monad on the type [𝑅] of lists of 𝑅:

                                  𝑇 𝐴 ≝ [𝑅] ⊸ 𝐴 ⊗ [𝑅]

As an instance of the linear state monad, it is strong. The morphism 𝐧𝐞𝐰 ∶ 𝐼 → 𝑇 (𝑅⊕𝐼)
is defined by popping an element from the list, or returning the error 𝐼 if the list is empty.


                                              6
The morphism 𝐝𝐞𝐥𝐞𝐭𝐞 ∶ 𝑅 → 𝑇 𝐼 is defined by pushing the resource onto the list; this is
guaranteed to never fail.
    Observe that an effectful, closed program of type 𝐴 in this setup corresponds to a
morphism 𝐼 → ([𝑅] ⊸ 𝐴 ⊗ [𝑅]). Its execution consists of supplying an initial list of
available resources (free-list). Now if the type 𝐴 is purely positive and does not contain the
type 𝑅, we expect that a correct linear program will have as final free-list the same list as
given initially, up to a permutation. We can understand this as a resource-safety property:
only resources acquired from the initial free-list have been released, all resources have
eventually been released including in case of error; no resource has been released twice.
    Moreover, assuming now an ordered rather than linear setting, that is without symme-
try (6), we expect that the final free-list is identical to the initial free-list. This reflects the
observation that without symmetry, resources are managed in a last-in-first-out (LIFO)
order. Ordered logics often have two forms of closures operating on opposite sides 𝐵 ⟜ 𝐴
and 𝐴 ⊸ 𝐵, but as we will see this ordered resource-safety property is only true when
one does not have 𝐴 ⊸ 𝐵; hence we only have 𝐵 ⟜ 𝐴 in this paper for the ordered logics
(which still coincides with 𝐴 ⊸ 𝐵 when adding symmetry).


1.6   Outline and contributions

We have just explained abstractly how to mix linearity and exceptions, and we introduced
the allocation monad modelling an idealised global “free-list” allocator, with the purpose
of studying resource-safety properties. In Section 2 we define a linear CBPV calculus 
which has an ordered fragment by removing its exchange rule (6), hence named . This
calculus features allocation effects (𝐧𝐞𝐰, 𝐝𝐞𝐥𝐞𝐭𝐞), together with a simple type system
and a small-step operational semantics. We establish elementary properties of  and
 relating typing to reduction. Then, in Section 3 we define and prove resource-safety
properties based on the allocation monad.
    In Section 4 we present the resource CBPV, an extension of the ordered language,
through a calculus  ,𝐦𝐨𝐯𝐞 . It is an affine CBPV language with allocation effects and
exceptions, in which every positive type has a chosen effectful erasure map (𝐝𝐫𝐨𝐩), and
in which allocation failure results in an exception. Its exchange rule does a side-effect, as
it changes the observable execution order of destructors; we also consider its ordered
fragment   . We define the semantics of  ,𝐦𝐨𝐯𝐞 by a translation into  that preserves
the ordered fragment.
                                                  J−K
                                                          
                                                            ⊂
                                        ⊂




                                                     J−K
                                     ,𝐦𝐨𝐯𝐞                

 ,𝐦𝐨𝐯𝐞 and   inherit the resource-safety properties of  and , respectively.
    Then, in Section 5 we define a presheaf model for , which models an ordered logic
with a destructor for all types, without being a model of affine logic in a traditional sense.
Lastly, in Section 6, we conclude with a discussion placing the results in the context of
the theory of programming languages.


                                                 7
2   An ordered effectful calculus of allocations

In this section, we describe a calculus with allocation effects 𝐧𝐞𝐰, 𝐝𝐞𝐥𝐞𝐭𝐞, and with an
ordered type system () which optionally can be upgraded to linear (). We provide a
common small-step operational semantics modelling this concrete effect. Our starting
point is a simplified version of the linear CBPV calculus [11]: for simplicity we consider
a calculus given in natural deduction, as opposed to sequent calculus, as we do not
investigate the reductions and conversions on open terms. Starting from the linear CBPV
calculus, this amounts to considering the derivation of natural deduction rules in the
sequent calculus of [11], which directly gives an operational semantics in the form of
typed abstract machines in head reduction. It is then adapted to the allocation effect by
adding a list of resources, the free-list, to every machine configuration.
    Ordered logic refines linear logic by removing the exchange rule, due to which the
order of formulae in the antecedent matters for provability. As in Walker [58], we consider
a sequencing (composition) rule restricted as follows:
                                  Γ, 𝐴 ⊢ 𝐵      Δ⊢𝐴
                                                    let
                                        Γ, Δ ⊢ 𝐵
Unlike [48, 58], we consider left functions:
                𝐴, Γ ⊢ 𝐵 ⟜                       Γ⊢𝐴       Δ ⊢ 𝐵 ⟜ 𝐴 ⟜𝑒
                          𝑖
               Γ⊢𝐵⟜𝐴                                   Γ, Δ ⊢ 𝐵
instead of right functions whose rules are symmetric:
                Γ, 𝐴 ⊢ 𝐵     ⊸𝑖                  Γ⊢𝐴⊸𝐵       Δ ⊢ 𝐴 ⊸𝑒
               Γ⊢𝐴⊸𝐵                                Γ, Δ ⊢ 𝐵
The notation for left functions might seem unusual but one can think of the notation for
an exponential object 𝐵 𝐴 , and it is justified by the isomorphism:

        (𝐶 ⟜ 𝐵) ⟜ 𝐴 ≅ 𝐶 ⟜ (𝐵 ⊗ 𝐴)                 𝐴 ⊸ (𝐵 ⊸ 𝐶) ≅ (𝐴 ⊗ 𝐵) ⊸ 𝐶

We will justify the choice of left vs. right functions in section 3.
    CBPV will play an important role for the translation in section 4, and is also inter-
esting in its own right since its treatment of the arrow type is useful to comprehend the
multiplicity of closure types in the present of first-class resources (as we will discuss in
section 6). Concretely, connectives and types are classified into two kinds, positive and
negative, which require different evaluation strategies. Notably, the type 𝑅 of allocated
resources is positive.
                          {
                            Positive types      𝑃,𝑄 ⩴ 𝑅 ∣ 1 ∣ 𝐴 ⊗ 𝐵 ∣ 𝐴 ⊕ 𝐵
           Types 𝐴, 𝐵 ∶
                            Negative types 𝑁, 𝑀 ⩴ 𝐵 ⟜ 𝐴 ∣ 𝐴 & 𝐵

Expressions of positive type evaluate eagerly, whereas expressions of negative type
evaluate lazily. We introduce the notation 𝜀 ⩴ + ∣ − for polarities, and associate to each
type its polarity 𝜛(𝐴) with 𝜛(𝑃 ) = + and 𝜛(𝑁) = −.


                                             8
                                  var                    Γ⊢𝑡∶𝐴      𝜎 ∈ Σ(Γ, Γ′ )
               𝑥∶𝐴⊢𝑥∶𝐴                                        ′
                                                                                                struct
                                                             Γ ⊢ 𝑡[𝜎] ∶ 𝐴
                                              𝐧𝐞𝐰                                              𝐝𝐞𝐥𝐞𝐭𝐞
               ⊢ 𝐧𝐞𝐰 ∶ (𝑅 ⊕ 1) ⟜ 1                                   ⊢ 𝐝𝐞𝐥𝐞𝐭𝐞 ∶ 1 ⟜ 𝑅
                              Δ ⊢ 𝑡 ∶ 𝐴𝜀                Γ, 𝑥 ∶ 𝐴 ⊢ 𝑢 ∶ 𝐵𝜀′
                                                                 ′
                                                                                 let
                                  Γ, Δ ⊢ (let 𝑥 = 𝑡 in 𝑢)𝜀 ∶ 𝐵
                                                    𝜀


                             1𝑖                     Δ⊢𝑣∶1        Γ, Γ′ ⊢ 𝑡 ∶ 𝐴𝜀
                  ⊢ () ∶ 1                                                                      1𝑒
                                                            ′
                                                     Γ, Δ, Γ ⊢ 𝛿(𝑣, ().𝑡)𝜀 ∶ 𝐴
      Γ⊢𝑣∶𝐴          Δ⊢𝑤∶𝐵              ⊗𝑖         Γ⊢𝑣∶𝐴                 ⊕𝑖1
                                                                                          Γ⊢𝑣∶𝐵                ⊕𝑖2
       Γ, Δ ⊢ (𝑣, 𝑤) ∶ 𝐴 ⊗ 𝐵                    Γ ⊢ 𝜄1 𝑣 ∶ 𝐴 ⊕ 𝐵                       Γ ⊢ 𝜄2 𝑣 ∶ 𝐴 ⊕ 𝐵
                      Δ⊢𝑣∶𝐴⊗𝐵        Γ, 𝑥 ∶ 𝐴, 𝑦 ∶ 𝐵, Γ′ ⊢ 𝑡 ∶ 𝐶𝜀
                                                                                          ⊗𝑒
                                  ′
                           Γ, Δ, Γ ⊢ 𝛿(𝑣, (𝑥, 𝑦).𝑡)𝜀 ∶ 𝐶
            Δ⊢𝑣∶𝐴⊕𝐵                Γ, 𝑥 ∶ 𝐴, Γ′ ⊢ 𝑡 ∶ 𝐶𝜀       Γ, 𝑦 ∶ 𝐵, Γ′ ⊢ 𝑢 ∶ 𝐶
                                                                                                         ⊕𝑒
                                         ′                𝜀
                                  Γ, Δ, Γ ⊢ 𝛿(𝑣, 𝑥.𝑡, 𝑦.𝑢) ∶ 𝐶
              𝑥 ∶ 𝐴, Γ ⊢ 𝑡 ∶ 𝐵                          Γ⊢𝑤∶𝐴       Δ ⊢ 𝑣 ∶ 𝐵𝜀 ⟜ 𝐴
                                   ⟜𝑖                                                                   ⟜𝑒
             Γ ⊢ 𝜆𝑥.𝑡 ∶ 𝐵 ⟜ 𝐴                              Γ, Δ ⊢ (𝑣𝑤)𝜀 ∶ 𝐵
         Γ⊢𝑡∶𝐴          Γ⊢𝑢∶𝐵                       Γ ⊢ 𝑣 ∶ 𝐴𝜀 & 𝐵                 Γ ⊢ 𝑣 ∶ 𝐴 & 𝐵𝜀
                                         &𝑖                                &𝑒1                                &𝑒2
           Γ ⊢ ⟨𝑡, 𝑢⟩ ∶ 𝐴 & 𝐵                       Γ ⊢ (𝜋1 𝑣)𝜀 ∶ 𝐴                Γ ⊢ (𝜋2 𝑣)𝜀 ∶ 𝐵

                                        Fig. 1. Typing rules for 



2.1    Grammar of terms

We define expressions and values with the following grammars:

      Expressions 𝑡, 𝑢 ⩴ 𝑣 ∣ (let 𝑥+ = 𝑡 in 𝑢)+ ∣ (let 𝑥− = 𝑣 in 𝑢)+ ∣ 𝛿(𝑣, (𝑥, 𝑦).𝑡)+ ∣
                             𝛿(𝑣, ().𝑡)+ ∣ 𝛿(𝑣, 𝑥.𝑡, 𝑦.𝑢)+ ∣ (𝑣𝑤)+ ∣ (𝜋1 𝑣)+ ∣ (𝜋2 𝑣)+
          Values 𝑣, 𝑤 ⩴ (let 𝑥+ = 𝑡 in 𝑣)− ∣ (let 𝑥− = 𝑣 in 𝑤)− ∣ 𝛿(𝑣, (𝑥, 𝑦).𝑤)− ∣
                             𝛿(𝑣, ().𝑤)− ∣ 𝛿(𝑣, 𝑥.𝑤, 𝑦.𝑤′ )− ∣ (𝑣𝑤)− ∣ (𝜋1 𝑣)− ∣ (𝜋2 𝑣)− ∣
                             𝑥 ∣ 𝐧𝐞𝐰 ∣ 𝐝𝐞𝐥𝐞𝐭𝐞 ∣ (𝑣, 𝑤) ∣ () ∣ 𝜄1 𝑣 ∣ 𝜄2 𝑣 ∣ 𝜆𝑥.𝑡 ∣ ⟨𝑡, 𝑢⟩ ∣ 𝑟𝑛∈ℕ

Our untyped expressions do not have typing annotations. Instead, expressions correspond-
ing to elimination rules and let bindings have polarity annotations, which is the minimal
amount of information determined by the type that we need to know the evaluation
strategy.
    Values are substitutable expressions: they are made of variables, all negative expres-
sions (as they follow the call-by-name evaluation strategy) and positive expressions that
have the shape of values in call-by-value. Positive values are eliminated with pattern
matching: we note these with a dedicated 𝛿 eliminators for units, strict pairs and sums.
Negative value eliminators follow the usual notation from lambda-calculus: lazy pair
projections and function applications.


                                                         9
2.2    Typing rules
We define in fig. 1 typing rules for . Type polarity annotations in subscript 𝐴𝜀 assert
that 𝐴 has polarity 𝜀. Contexts Γ, Δ are lists of typed variables. Σ(Γ, Γ′ ) is the set of
maps from Γ to Γ′ made of permutations and renamings. The term 𝑡[𝜎] appearing in the
struct(ural) rule denotes 𝑡 where all variables have been substituted according to 𝜎; in
effect (struct) contains the unrestricted exchange rule. For  we simply restrict 𝜎 to be
order-preserving.
    Polarity annotations of expressions are inferred from the type polarities in typing
rules. Hence, we will leave them implicit for typed expressions. The following notations
allow to define and type expressions without restrictions with respect to values, by picking
an arbitrary order to evaluate expressions. Such expressions may not always be well-typed
in , since let bindings can only bind the right-most variable.
       𝜄𝑖 𝑡∗ ≝ let 𝑥 = 𝑡 in 𝜄𝑖 𝑥                𝛿 ∗ (𝑡, (𝑥, 𝑦).𝑢) ≝ let 𝑧 = 𝑡 in 𝛿(𝑧, (𝑥, 𝑦).𝑢)
   (𝑡, 𝑢)∗ ≝ let 𝑥 = 𝑡 in let 𝑦 = 𝑢 in(𝑥, 𝑦)   𝛿 ∗ (𝑡, 𝑥.𝑢, 𝑦.𝑢′ ) ≝ let 𝑧 = 𝑡 in 𝛿(𝑧, 𝑥.𝑢, 𝑦.𝑢′ )
      (𝑣𝑡)∗ ≝ let 𝑥 = 𝑡 in 𝑣𝑥                               𝑡; 𝑢 ≝ let 𝑥 = 𝑡 in 𝛿(𝑥, ().𝑢)
As an example, we can define in  the following program that allocates then frees two
resources. Upon allocation failure of 𝑠, it is forced to free 𝑟 before returning:
             (             (                                               ) )
        ⊢ 𝛿 ∗ 𝐧𝐞𝐰 (), 𝑟.𝛿 ∗ 𝐧𝐞𝐰 (), 𝑠.(𝐝𝐞𝐥𝐞𝐭𝐞 𝑠; 𝐝𝐞𝐥𝐞𝐭𝐞 𝑟), 𝑖.(𝑖; 𝐝𝐞𝐥𝐞𝐭𝐞 𝑟) , 𝑖.𝑖 ∶ 1 (12)

2.3    Purely-positive types without resources
An important notion that we will need is that of purely-positive types without resources
defined as follows:
                           𝑊 ⩴1∣𝑊 ⊗𝑊′ ∣𝑊 ⊕𝑊′                                        (13)
These types are in particular central: they commute for ⊗ with any other types, naturally
so. We indeed can define by induction values
                                       swap𝐴
                                           𝑊 ∶𝑊 ⊗𝐴⟜𝐴⊗𝑊

(corresponding to natural isomorphisms in the semantics of section 5):
                          (             (                ))
         swap𝐴  𝐼  ≝ 𝜆𝑝.𝛿   𝑝, (𝑎, 𝑖).𝛿  𝑖, ().(⋆,    𝑎)
                          (              (                       ))
   swap𝑊 ⊗𝑊 ≝ 𝜆𝑝.𝛿 𝑝, (𝑎, 𝑤).𝛿 𝑤, (𝑥, 𝑥′ ).𝑡𝑥,𝑥′ where
         𝐴
           1     2
               (                                              (                    ))
                                𝐴⊗𝑊
     𝑡𝑥,𝑥′ = let 𝑝1 = swap𝑊 1 ((𝑎, 𝑥), 𝑥′ ) in 𝛿 𝑝1 , (𝑦′ , 𝑝).𝛿(𝑝, (𝑎, 𝑦).𝑢𝑦,𝑦′ )
                                   2
               (                                               (                         )
                                 𝑊 ⊗𝐴                                            (     ))
     𝑢𝑦,𝑦′ = let 𝑝2 = swap𝑊2 ((𝑦′ , 𝑎), 𝑦) in 𝛿 𝑝2 , (𝑧, 𝑝).𝛿 𝑝, (𝑧′ , 𝑎).((𝑧, 𝑧′ ), 𝑎)
                                    1

         𝐴
                          (                                   )
   swap𝑊 ⊕𝑊 ≝ 𝜆𝑝.𝛿 𝑝, (𝑎, 𝑤).𝛿(𝑤, 𝑥.𝑡𝑥 , 𝑦.𝑢𝑦 ) where
           1
            (    2
                                              (                               ))
                                                         ′             ′
     𝑡𝑥 = let 𝑝1 = swap𝐴     𝑊1  (𝑎,  𝑥) in 𝛿   𝑝1 ,  (𝑥   , 𝑎).(𝜄1  𝑥   , 𝑎)
             (                                (                               ))
                                                         ′            ′
     𝑢𝑦 = let 𝑝2 = swap𝐴      𝑊  (𝑎,  𝑦) in 𝛿   𝑝 2 , (𝑦   , 𝑎).(𝜄 2 𝑦   , 𝑎)
                                   2




                                               10
      ⟨(let 𝑥− = 𝑣 in 𝑡)𝜀 ∣𝑠∣𝑙⟩𝜀 ⇝ ⟨𝑡[𝑣∕𝑥]∣𝑠∣𝑙⟩𝜀
      ⟨(let 𝑥+ = 𝑡 in 𝑢)𝜀 ∣𝑠∣𝑙⟩𝜀 ⇝ ⟨𝑡∣(𝑥+ .𝑢)𝜀 · 𝑠∣𝑙⟩+            ⟨𝑣∣(𝑥+ .𝑡)𝜀 · 𝑠∣𝑙⟩+ ⇝ ⟨𝑡[𝑣∕𝑥]∣𝑠∣𝑙⟩𝜀
                 ⟨(𝑣𝑤)𝜀 ∣𝑠∣𝑙⟩𝜀 ⇝ ⟨𝑣∣𝑤𝜀 · 𝑠∣𝑙⟩−                      ⟨𝜆𝑥.𝑡∣𝑣𝜀 · 𝑠∣𝑙⟩− ⇝ ⟨𝑡[𝑣∕𝑥]∣𝑠∣𝑙⟩𝜀
                 ⟨(𝜋𝑖 𝑣) ∣𝑠∣𝑙⟩
                        𝜀       𝜀
                                    ⇝ ⟨𝑣∣𝜋𝑖𝜀 · 𝑠∣𝑙⟩−             ⟨⟨𝑡1 , 𝑡2 ⟩∣𝜋𝑖𝜀 · 𝑠∣𝑙⟩− ⇝ ⟨𝑡𝑖 ∣𝑠∣𝑙⟩𝜀

  ⟨𝛿((𝑣, 𝑤), (𝑥, 𝑦).𝑡)𝜀 ∣𝑠∣𝑙⟩𝜀 ⇝ ⟨𝑡[𝑣∕𝑥, 𝑤∕𝑦]∣𝑠∣𝑙⟩𝜀              ⟨𝐧𝐞𝐰 ∣() · 𝑠∣ Nil⟩− ⇝ ⟨𝜄2 ()∣𝑠∣ Nil⟩+
             ⟨𝛿((), ().𝑡) ∣𝑠∣𝑙⟩ ⇝ ⟨𝑡∣𝑠∣𝑙⟩
                        𝜀       𝜀            𝜀
                                                               ⟨𝐧𝐞𝐰 ∣() · 𝑠∣𝑟𝑛 ∶∶ 𝑙⟩− ⇝ ⟨𝜄1 𝑟𝑛 ∣𝑠∣𝑙⟩+
 ⟨𝛿(𝜄𝑖 𝑣, 𝑥1 .𝑡1 , 𝑥2 .𝑡2 )𝜀 ∣𝑠∣𝑙⟩𝜀 ⇝ ⟨𝑡𝑖 [𝑣∕𝑥𝑖 ]∣𝑠∣𝑙⟩𝜀          ⟨𝐝𝐞𝐥𝐞𝐭𝐞 ∣𝑟𝑛 · 𝑠∣𝑙⟩− ⇝ ⟨()∣𝑠∣𝑟𝑛 ∶∶ 𝑙⟩+

                                             Fig. 2. Reduction rules



These types also happen to be discardable (1 ⟜ 𝐴) and copyable (𝐴 ⊗ 𝐴 ⟜ 𝐴) but we
only rely on centrality in what follows.


2.4     Operational semantics

We define in fig. 2 a small-step operational semantics for untyped expressions with an
abstract machine. We begin by defining a stack that stores the arguments of delayed
operations along with their polarity: indices of lazy pair projections, arguments of function
applications and continuations of let bindings of positive values. Finally, a command
consists of an expression, a stack, a free-list of resources interpreting the allocation
monad and the current polarity.

                            Stacks 𝑠 ⩴ ⋆ ∣ 𝑣𝜀 · 𝑠 ∣ 𝜋𝑖𝜀 · 𝑠 ∣ (𝑥+ .𝑢)𝜀 · 𝑠
                              Lists 𝑙 ⩴ Nil ∣ 𝑟𝑛∈ℕ ∶∶ 𝑙
                  Commands 𝑐 ⩴ ⟨𝑡 ∣ 𝑠 ∣ 𝑙⟩𝜀

We now define reduction rules: let bindings of negative expressions perform the substitu-
tion them immediately, following call-by-name reduction, while let bindings of positive
expressions push their continuation on the stack to first reduce the expression to a value.
All rules that push arguments on the stack come with their dual rule that consumes the
argument on the stack. Pattern-matching rules can reduce immediately as only values can
be bound. Finally, rules for constants 𝐧𝐞𝐰 and 𝐝𝐞𝐥𝐞𝐭𝐞 are the only ones that manipulate
the free-list of resources.
    If we interpret our previous program 𝑝 = (12) with the list of resources 𝑟0 ∶∶ 𝑟1 ∶∶ 𝑙,
we obtain in particular the following reduction steps:

            ⟨𝑝 ∣ ⋆ ∣ 𝑟0 ∶∶ 𝑟1 ∶∶ 𝑙⟩+
                 ⟨        (      (                                          ))       ⟩
                        |                                                        | +
             ⇝∗ 𝜄1 𝑟1 | 𝑥+ .𝛿 𝑥, 𝑠.(𝐝𝐞𝐥𝐞𝐭𝐞 𝑠; 𝐝𝐞𝐥𝐞𝐭𝐞 𝑟0 ), 𝑖.(𝑖; 𝐝𝐞𝐥𝐞𝐭𝐞 𝑟0 ) · ⋆ | 𝑙
                        |                                                        |
             ⇝∗ ⟨() ∣ ⋆ ∣ 𝑟0 ∶∶ 𝑟1 ∶∶ 𝑙⟩+


                                                          11
                        𝑠 ∶ 𝐵𝜀 ⊢𝑝 𝐶         ⊢𝑝 𝑣 ∶ 𝐴       𝑠 ∶ 𝐵𝜀 ⊢𝑝 𝐶         𝑥 ∶ 𝐴 ⊢𝑝 𝑡 ∶ 𝐵
       ⋆ ∶ 𝐴 ⊢𝑝 𝐴
                            𝑣𝜀 · 𝑠 ∶ 𝐵 ⟜ 𝐴 ⊢𝑝 𝐶                    (𝑥+ .𝑡)𝜀 · 𝑠 ∶ 𝐴 ⊢𝑝 𝐶
                         𝑠 ∶ 𝐴 𝜀 ⊢𝑝 𝐶                            𝑠 ∶ 𝐵 𝜀 ⊢𝑝 𝐶
                     𝜀                                       𝜀
                    𝜋1 · 𝑠 ∶ 𝐴 & 𝐵 ⊢𝑝 𝐶                     𝜋2 · 𝑠 ∶ 𝐴 & 𝐵 ⊢𝑝 𝐶

                                      Fig. 3. Stack typing rules


2.5     Properties

We now study properties of . First, we establish standard properties such as confluence
(through determinism), subject reduction and progress.

Proposition 2. The reduction rules are deterministic: at most one reduction rule can be
applied to any command (see appendix B.2).

    We define typing judgements for expressions ⊢𝑝 𝑡 ∶ 𝐴 by extending all typing rules
given in section 2.2 with the following axiom scheme for resources: ⊢𝑝 𝑟𝑛 ∶ 𝑅, to type
resources that occur in commands through a program execution. We then extend those
judgements in fig. 3 for closed stacks 𝑠 ∶ 𝐴 ⊢𝑝 𝐵 which follow sequent calculus rules.
Finally, we extend judgements to commands 𝑐 ∶ 𝐴, which consist of pairs of judgements
⊢𝑝 𝑡 ∶ 𝐵𝜀 and 𝑠 ∶ 𝐵 ⊢𝑝 𝐴 for 𝑐 = ⟨𝑡 ∣ 𝑠 ∣ 𝑙⟩𝜀 ∶ 𝐴. We prove the following substitution
lemma by induction on the derivation of 𝑡:

Lemma 3 (Substitution lemma (SL)). If ⊢𝑝 𝑣 ∶ 𝐴 and Γ, 𝑥 ∶ 𝐴, Γ′ ⊢𝑝 𝑡 ∶ 𝐵, then
Γ, Γ′ ⊢𝑝 𝑡[𝑣∕𝑥] ∶ 𝐵.

Theorem 4 (Subject reduction). The reduction rules preserve typing judgements: for
any 𝑐1 ∶ 𝐴 and 𝑐2 , 𝑐1 ⇝ 𝑐2 implies 𝑐2 ∶ 𝐴. This also holds in the ordered fragment, i.e.
for ⊢𝑝 without the exchange rule. (See appendix B.3.)

    We define final values 𝑣𝑡 ⩴ () ∣ (𝑣, 𝑤) ∣ 𝜄𝑖 𝑣 ∣ 𝑟𝑛 ∣ ⟨𝑡, 𝑢⟩ ∣ 𝜆𝑥.𝑡 ∣ 𝐧𝐞𝐰 ∣ 𝐝𝐞𝐥𝐞𝐭𝐞. They
include in particular all values 𝑣 such that ⊢𝑝 𝑣 ∶ 𝐴+ .

Theorem 5 (Progress). A well-typed command reduces if and only if it is not of the
shape ⟨𝑣𝑡 ∣ ⋆ ∣ 𝑙⟩𝜀 . This also holds in . (See appendix B.4.)

   Together, subject reduction and progress ensures that any well-typed expression
⊢𝑝 𝑡 ∶ 𝐴 reduces either indefinitely4 or to a final command ⟨𝑣𝑡 ∣ ⋆ ∣ 𝑙⟩ with ⊢𝑝 𝑣𝑡 ∶ 𝐴.


3      Resource-safety properties

In this section, we prove a resource-safety property for  pertaining to its linear character.
This property is stated for complete programs: closed expressions that return a purely
 4
     Although we do not have non-terminating features, our proof by progress & subject reduction
     does not rely on termination.


                                                 12
positive type without resource, executed in an empty context. We show that for such a
program 𝑡, the execution starting with any free-list leaves it unchanged upon return, up
to a permutation 𝜎:

               ⟨𝑡 ∣ ⋆ ∣ 𝑙⟩ ⇝∗ ⟨𝑣 ∣ ⋆ ∣ 𝑙′ ⟩            ⇐⇒          ∃𝜎, 𝑙′ = 𝜎(𝑙)

The property is indeed about resource safety as it provides several good properties
expected in programs that manipulate resources:

  ∙ all allocated resources are released by the end of the program,
  ∙ only previously-allocated resources are released,
  ∙ no resource has been released twice (i.e. no “use after free”, in this limited context
    where the only way to use a resource is to release it),
  ∙ these properties remain true in case of an error during the program execution, in-
    cluding an allocation error.

We start by describing a stronger property for : in the ordered language, the final
free-list is identical to the initial one (𝜎 = id). This corresponds to the expected property
with ordered type systems that resources are freed in a LIFO order [58, §1.4]. We also
provide a counter-example showing that we cannot include right functions in  without
breaking the LIFO property.


3.1   Ordered case

Let 𝑊 a purely positive type without resource and ⊢ 𝑡 ∶ 𝑊 a closed typed expression
of  (i.e. without exchange rule).

Proposition 6. For any value 𝑣 and lists of resources 𝑙, 𝑙′ , if

                                    ⟨𝑡 ∣ ⋆ ∣ 𝑙⟩ ⇝∗ ⟨𝑣 ∣ ⋆ ∣ 𝑙′ ⟩

then 𝑙′ = 𝑙.

    To prove this property, we will define the list of resources 𝐿𝑅(𝑡) of a term 𝑡 by
tracking resources in contexts of typing rules, and show that such lists are invariant by
reduction. In order to reason about resources in case of substitutions, 𝐿𝑅(𝑡[𝑣∕𝑥]) must
be definable in terms of 𝐿𝑅(𝑡) and 𝐿𝑅(𝑣), hence their concatenation. To ensure this (see
lemma 8), we restrict contexts to have the shape Θ ≝ Γ; 𝐿; Δ with 𝐿 the list of resources,
Γ, Δ contexts of variables and 𝑥 to be the right-most variable in Γ or the left-most variable
in Δ.
    Given ++ the concatenation operation for lists, Θ = ΓΘ ; 𝐿Θ ; ΔΘ and Θ′ = ΓΘ′ ; 𝐿Θ′ ; ΔΘ′ ,
the expression Θ @ Θ′ asserts that we are in one of the three following cases to define
the concatenation of both contexts:

  ∙ 𝐿Θ = [], then Θ @ Θ′ ≝ ΓΘ , ΔΘ , ΓΘ′ ; 𝐿Θ′ ; ΔΘ′ .
  ∙ 𝐿Θ′ = [], then Θ @ Θ′ ≝ ΓΘ ; 𝐿Θ ; ΔΘ , ΓΘ′ , ΔΘ′ .
  ∙ ΔΘ = ΓΘ′ = ∅, then Θ @ Θ′ ≝ ΓΘ ; 𝐿Θ ++ 𝐿Θ′ ; ΔΘ′ .


                                                13
     ; []; 𝑥 ⊢𝑜 𝑥        ; []; ⊢𝑜 ()      ; []; ⊢𝑜 𝐧𝐞𝐰        ; []; ⊢𝑜 𝐝𝐞𝐥𝐞𝐭𝐞         ; [𝑟𝑛 ]; ⊢𝑜 𝑟𝑛
                      Γ; []; 𝑥, Δ ⊢𝑜 𝑥                           Γ, 𝑥; []; Δ ⊢𝑜 𝑥
                      Γ, 𝑥; []; Δ ⊢𝑜 𝑥                           Γ; []; 𝑥, Δ ⊢𝑜 𝑥
        Θ ⊢𝑜 𝑣                 Θ ⊢𝑜 𝑣            Θ ⊢𝑜 𝑡     Θ ⊢𝑜 𝑢                   𝑥, Θ ⊢𝑜 𝑡
        Θ ⊢𝑜 𝜄𝑖 𝑣             Θ ⊢𝑜 𝜋𝑖 𝑣             Θ ⊢𝑜 ⟨𝑡, 𝑢⟩                      Θ ⊢𝑜 𝜆𝑥.𝑡
                Θ ⊢𝑜 𝑣     Θ′ ⊢𝑜 𝑤                         Θ, 𝑥 ⊢𝑜 𝑢     Θ ′ ⊢𝑜 𝑡
                       ′                                         ′
                  Θ @ Θ ⊢𝑜 (𝑣, 𝑤)                          Θ @ Θ ⊢𝑜 let 𝑥 = 𝑡 in 𝑢
           Θ, 𝑥, 𝑦 @ Θ′′ ⊢𝑜 𝑡     Θ ′ ⊢𝑜 𝑣                  Θ @ Θ′′ ⊢𝑜 𝑡     Θ ′ ⊢𝑜 𝑣
            Θ @ Θ′ @ Θ′′ ⊢𝑜 𝛿(𝑣, (𝑥, 𝑦).𝑡)                  Θ @ Θ′ @ Θ′′ ⊢𝑜 𝛿(𝑣, ().𝑡)
      Θ, 𝑥 @ Θ′′ ⊢𝑜 𝑡   Θ, 𝑦 @ Θ′′ ⊢𝑜 𝑢               Θ ′ ⊢𝑜 𝑣            Θ ⊢𝑜 𝑤     Θ ′ ⊢𝑜 𝑣
                Θ @ Θ @ Θ′′ ⊢𝑜 𝛿(𝑣, 𝑥.𝑡, 𝑦.𝑢)
                      ′                                                           ′
                                                                             Θ @ Θ ⊢𝑜 𝑣𝑤

          Fig. 4. Typing rules of ordered expressions with resources (types omitted)

                                                      ; 𝐿𝑣 ; ⊢𝑜 𝑣         𝐿𝑠 ⊢𝑆𝑜 𝑠
                     [] ⊢𝑆𝑜 ⋆
                                                         𝐿𝑠 ++ 𝐿𝑣 ⊢𝑆𝑜 𝑣 · 𝑠
              ; 𝐿𝑡 ; 𝑥 ⊢𝑜 𝑡   𝐿𝑠 ⊢𝑆𝑜 𝑠                      ; 𝐿𝑡 ; ⊢𝑜 𝑡    𝐿𝑠 ⊢𝑆𝑜 𝑠
                𝐿𝑠 ++ 𝐿𝑡 ⊢𝑜 (𝑥+ .𝑡) · 𝑠
                          𝑆
                                                          𝐿𝑠 ++ 𝐿𝑡 ++ 𝑙 ⊢𝑜 ⟨𝑡 ∣ 𝑠 ∣ 𝑙⟩
                                                                         𝐶



     Fig. 5. Typing rules of ordered stacks and commands with resources (types omitted)


    We can now type terms with resources with the judgement ⊢𝑜 indexed by such
contexts, which enrich the previous typing judgements with information to track their
resources (in fig. 4, where types are omitted for brevity). Given an ordered expression
Γ; 𝐿; Δ ⊢𝑜 𝑡, we define its list of resources 𝐿𝑅(𝑡) ≝ 𝐿. For Θ = Γ; 𝐿; Δ, we define the
notations Θ, 𝑥 ≝ Γ; 𝐿; Δ, 𝑥 and 𝑥, Θ ≝ 𝑥, Γ; 𝐿; Δ.
Lemma 7. If Γ ⊢ 𝑡 ∶ 𝐴, then Γ; ; ⊢𝑜 𝑡 ∶ 𝐴 (see appendix C.1).
   We can then accept substitutions of expressions that preserve well-formed contexts.
The following left and right substitution lemmas cover substitutions encountered in the
operational semantics.
Lemma 8. (Left SL) If ; 𝐿𝑡 ; ⊢𝑜 𝑡 and Γ, 𝑥; 𝐿𝑢 ; Δ ⊢𝑜 𝑢, then Γ; 𝐿𝑡 ++ 𝐿𝑢 ; Δ ⊢𝑜 𝑢[𝑡∕𝑥].
(Right SL) If ; 𝐿𝑡 ; ⊢𝑜 𝑡 and Γ; 𝐿𝑢 ; 𝑥, Δ ⊢𝑜 𝑢, then Γ; 𝐿𝑢 ++ 𝐿𝑡 ; Δ ⊢𝑜 𝑢[𝑡∕𝑥] (see ap-
pendix C.2).
   We then extend ⊢𝑜 for stacks and commands, with only resources in their contexts.
Resources from stacks remain to the left of resources from expressions in the context of
commands:
Theorem 9. Reducing an ordered command results in an ordered command with the
same list of resources, i.e. for all 𝑐1 , 𝑐2 , 𝑀 such that 𝐿 ⊢𝐶
                                                              𝑜 𝑐1 and 𝑐1 ⇝ 𝑐2 one has
𝐿 ⊢𝐶
   𝑜 2𝑐  (see appendix  C.3).


                                                 14
      We can now prove proposition 6:
Proof (proposition 6). For any expression with a purely-positive type without resource
⊢ 𝑡 ∶ 𝑊 in , by subject reduction and progress we have that ⟨𝑡 ∣ ⋆ ∣ 𝑙⟩ either reduces
indefinitely, or there exists a final value ⊢ 𝑣𝑡 ∶ 𝑊 such that ⟨𝑡 ∣ ⋆ ∣ 𝑙⟩ ⇝∗ ⟨𝑣 ∣ ⋆ ∣ 𝑙′ ⟩.
We then prove by induction on derivations that typed expressions without structural
rules are ordered: they do not include resources, so concatenated contexts are always
well-formed. So both 𝑡 and 𝑣 are ordered and without resources. Since reduction rules
preserve the list of resources, we have 𝑙 = 𝑙′ .

3.2    A counter-example for right functions
We only have left functions in , that is, abstractions binding the leftmost variable
together with the matching elimination rule from ordered logic. We provide the following
counter-example to the resource-safety property with right functions. We underline the
right function abstractions and applications.
                       (            (                                ) )
                𝑝 ≝ 𝛿 ∗ 𝐧𝐞𝐰(), 𝑟.𝛿 ∗ 𝐧𝐞𝐰(), 𝑠.(𝑡𝑟 𝑠), 𝑖.(𝐝𝐞𝐥𝐞𝐭𝐞 𝑟; 𝑖) , 𝑖.𝑖
                                (                                           )−
                    where 𝑡𝑟 = let 𝑖 = 𝐝𝐞𝐥𝐞𝐭𝐞 𝑟 in 𝛿(𝑖, ().𝜆𝑥. 𝐝𝐞𝐥𝐞𝐭𝐞 𝑥)             (14)

This example does not belong to  as it uses the right function 𝑡𝑟 ∶ 𝑅 ⊸ 1 and its
application 𝑡𝑟 𝑠.
                                                                       ⟜𝑒
                                          ×
                                           𝑥 ∶ 𝑅 ⊢ 𝐝𝐞𝐥𝐞𝐭𝐞 𝑥 ∶ 1                ⊸𝑖 (not in )
                                                    ⊢ 𝜆𝑥. 𝐝𝐞𝐥𝐞𝐭𝐞 𝑥 ∶ 𝑅 ⊸ 1
                                  ⟜𝑒                                                     1𝑒
           𝑟 ∶ 𝑅 ⊢ 𝐝𝐞𝐥𝐞𝐭𝐞 𝑟 ∶ 1              𝑖 ∶ 1 ⊢ 𝛿(𝑖, ().𝜆𝑥. 𝐝𝐞𝐥𝐞𝐭𝐞 𝑥) ∶ 𝑅 ⊸ 1
                                                                                         let
                  𝑟 ∶ 𝑅 ⊢ let 𝑖 = 𝐝𝐞𝐥𝐞𝐭𝐞 𝑟 in 𝛿(𝑖, ().𝜆𝑥. 𝐝𝐞𝐥𝐞𝐭𝐞 𝑥) ∶ 𝑅 ⊸ 1
                 ........................................................ =
                  𝑟 ∶ 𝑅 ⊢ 𝑡𝑟 ∶ 𝑅 ⊸ 1                      𝑠∶𝑅⊢𝑠∶𝑅
               ×                                                           ⊸𝑒 (not in )
                                 𝑟 ∶ 𝑅, 𝑠 ∶ 𝑅 ⊢ 𝑡𝑟 𝑠 ∶ 1

As we can see from the typing derivation, the context is ordered as 𝑟, 𝑠, which is the
converse of what we would have obtained with a left function. Subsequently, we can
then calculate that two resources 𝑟0 and 𝑟1 are reordered during the execution as follows
(with the obvious reductions rules for the right abstraction and application):

                       ⟨𝑝 ∣ ⋆ ∣ 𝑟0 ∶∶ 𝑟1 ∶∶ 𝑙⟩ ⇝∗ ⟨() ∣ ⋆ ∣ 𝑟1 ∶∶ 𝑟0 ∶∶ 𝑙⟩

This contradicts the LIFO property for .

3.3    Non-ordered case
If we consider expressions ⊢ 𝑡 ∶ 𝑊 in , that is by adding the exchange rule, they have
a weaker property:
Theorem 10. For all 𝑣, 𝑙, 𝑙′ such that ⟨𝑡 ∣ ⋆ ∣ 𝑙⟩ ⇝∗ ⟨𝑣 ∣ ⋆ ∣ 𝑙′ ⟩, there exists a
permutation 𝜎 of lists of resources such that 𝑙′ = 𝜎(𝑙).


                                               15
    This is proved similarly to proposition 6, by forgetting the order of variables and
resources in the predicate Γ; 𝐿; Δ ⊢𝑜 𝑡. This simplifies context concatenation by re-
moving preconditions and requires a single substitution lemma. The proof is detailed in
appendix C.4.


4   The resource call-by-push-value
We now introduce a resource CBPV: an ordered variant of CBPV with an allocation effect
𝐧𝐞𝐰, exceptions, a chosen effectful destructor 𝐝𝐫𝐨𝐩 at all types, and a 𝐦𝐨𝐯𝐞 operation
that implements a side-effecting exchange rule.
    Formally, we define a calculus  ,𝐦𝐨𝐯𝐞 which extends . Its semantics is given by
translation into : exceptions are propagated as errors, removing variables from the
context with their associated destructor. Hence,  serves as a meta-language in which the
ambient allocation monad remains implicit, and which gives resource-safety properties
for  ,𝐦𝐨𝐯𝐞 . In addition, by removing 𝐦𝐨𝐯𝐞, we obtain a calculus   whose translation
falls into .
    As a starting point, we picture the situation described in section 1.4:

                                   𝑈                 𝐹𝑇

                      C∕𝑇 𝐼        ⊥ (𝑎)     C         ⊥ (𝑏)     C𝑇                    (15)
                                   𝐹                 𝑈𝑇

where  = − & 𝑇 𝐼 provides, for an arbitrary linear type, the free type with destructor
(given by its second projection).
     When trying to add exceptions to a general notion of effect given by a strong monad
𝑇 , one would look at the adjunction (𝑏), which, assuming 𝑇  strong, gives rise to a linear
CBPV model [11], with positive types interpreted in C and negative types interpreted in
 C𝑇  . It is unnatural, though, to assume that 𝑇  is strong. In order to recover a strength
for 𝑇 , we want to restrict the positive types to the linear types that are provided with a
chosen destructor, by looking at the monoidal adjunction (𝑎) above. When starting from
an adjunction model, composing with a monoidal adjunction on the left yields another
adjunction model, a construction which generalises the Girard translations [11, §5.3]
(see also [42] for more details). This suggests that we look at the adjoint situation
                                              ↑

                                C∕𝑇 𝐼        ⊥         C𝑇 
                                              ↓


obtained by composition with ↑ ≝ 𝐹 𝑇  𝑈  and ↓ ≝ 𝐹  𝑈 𝑇  . Note that in terms of
underlying types, one has ↑𝐴 = 𝑇 (𝐴 ⊕ 𝐸) and ↓𝐴 = 𝐴 & 𝑇 𝐼.
    We cannot apply the results of [11] directly, which only deals with the situation where
the monoidal categories are symmetric and the monad is strong. Instead, we do this
construction by hand, which we give as a translation of the resource CBPV into  and
. Within this more focused approach, we refine the translation underlying [11, §5.3]


                                             16
                                 var                  Δ⊢𝑡∶𝐴         Γ, 𝑥 ∶ 𝐴 ⊢ 𝑢 ∶ 𝐵
             𝑥∶𝐴⊢𝑥∶𝐴                                                                        let
                                                        Γ, Δ ⊢ let 𝑥 = 𝑡 in 𝑢 ∶ 𝐵
                                  𝐝𝐫𝐨𝐩𝐴                       Γ, Γ′ , 𝑥 ∶ 𝐴 ⊢ 𝑡 ∶ 𝐶
           ⊢ 𝐝𝐫𝐨𝐩𝐴 ∶ 1 ⟜ 𝐴                                                                  𝐦𝐨𝐯𝐞
                                                        Γ, 𝑥 ∶ 𝐴, Γ′ ⊢ 𝐦𝐨𝐯𝐞(𝑥) in 𝑡 ∶ 𝐶
                                            𝐧𝐞𝐰                                     𝐫𝐚𝐢𝐬𝐞
                 ⊢ 𝐧𝐞𝐰 ∶ 𝑅 ⟜ 1                                  ⊢ 𝐫𝐚𝐢𝐬𝐞 ∶ 𝐴 ⟜ 𝐸
                Δ⊢𝑡∶𝑃      Γ, 𝑥 ∶ 𝑃 ⊢ 𝑢 ∶ 𝐴        Γ, 𝑒 ∶ 𝐸 ⊢ 𝑢′ ∶ 𝐴
                                                                                      𝐭𝐫𝐲
                    Γ, Δ ⊢ 𝐭𝐫𝐲 𝑥 ⇐ 𝑡 in 𝑢 𝐮𝐧𝐥𝐞𝐬𝐬 𝑒 ⇒ 𝑢′ ∶ 𝐴
      Γ⊢𝑣∶𝐴          Δ⊢𝑤∶𝐵              ⊗𝑖
                                                   Δ⊢𝑣∶𝐴⊗𝐵        Γ, 𝑥 ∶ 𝐴, 𝑦 ∶ 𝐵, Γ′ ⊢ 𝑡 ∶ 𝐶
                                                                                                         ⊗𝑒
       Γ, Δ ⊢ (𝑣, 𝑤) ∶ 𝐴 ⊗ 𝐵                                   ′
                                                        Γ, Δ, Γ ⊢ 𝛿(𝑣, (𝑥, 𝑦).𝑡) ∶ 𝐶
                            1𝑖                         Δ⊢𝑣∶1         Γ, Γ′ ⊢ 𝑡 ∶ 𝐴
                 ⊢ () ∶ 1                                                             1𝑒
                                                        Γ, Δ, Γ′ ⊢ 𝛿(𝑣, ().𝑡) ∶ 𝐴
                    Γ⊢𝑣∶𝐴                    ⊕𝑖1
                                                                    Γ⊢𝑣∶𝐵            ⊕𝑖2
                 Γ ⊢ 𝜄1 𝑣 ∶ 𝐴 ⊕ 𝐵                                Γ ⊢ 𝜄2 𝑣 ∶ 𝐴 ⊕ 𝐵
           Δ⊢𝑣∶𝐴⊕𝐵                  Γ, 𝑥 ∶ 𝐴, Γ′ ⊢ 𝑡 ∶ 𝐶        Γ, 𝑦 ∶ 𝐵, Γ′ ⊢ 𝑢 ∶ 𝐶
                                                                                              ⊕𝑒
                                          ′
                                   Γ, Δ, Γ ⊢ 𝛿(𝑣, 𝑥.𝑡, 𝑦.𝑢) ∶ 𝐶
             𝑥 ∶ 𝐴, Γ ⊢ 𝑡 ∶ 𝐵          ⟜𝑖              Γ⊢𝑤∶𝐴       Δ⊢𝑣∶𝐵⟜𝐴                   ⟜𝑒
            Γ ⊢ 𝜆𝑥.𝑡 ∶ 𝐵 ⟜ 𝐴                               Γ, Δ ⊢ 𝑣𝑤 ∶ 𝐵
       Γ⊢𝑡∶𝐴          Γ⊢𝑢∶𝐵                 &𝑖
                                                     Γ⊢𝑣∶𝐴&𝐵         &𝑒1
                                                                             Γ⊢𝑣∶𝐴&𝐵               &𝑒2
         Γ ⊢ ⟨𝑡, 𝑢⟩ ∶ 𝐴 & 𝐵                           Γ ⊢ 𝜋1 𝑣 ∶ 𝐴            Γ ⊢ 𝜋2 𝑣 ∶ 𝐵
                                 New and changed rules are in bold.

                                  Fig. 6. Typing rules for  ,𝐦𝐨𝐯𝐞


with ordered sequents, and with the consideration of a strength of 𝑇  with respect to
𝑈  , which is necessary for having antecedents with several variables in the first place.
    Another important difference is that we are translating direct-style calculi into direct-
style calculi: the monad 𝑇 is, already, the ambient monad for side-effects in  and
. As it turns out, we can still adapt the translation to work in this way. Note that
the type ↓𝐴 = 𝐴 & 𝑇 𝐼 is 𝐴 & 1 in , and that the type ↑𝐴 = 𝑇 (𝐴 ⊕ 𝐸) describes
effectful computations of type 𝐴 ⊕ 𝐸 in . In what follows, we make use of these type
constructions in  which we note ⇓𝐴 ≝ 𝐴 & 1 and ⇑𝐴 ≝ 𝐴 ⊕ 𝐸.

4.1   Expressions and types
The grammar of terms of  ,𝐦𝐨𝐯𝐞 extends that for , with the following terms:
  ∙ “𝐧𝐞𝐰”, now of type 1 ⟜ 𝑅, which raises an exception in case of allocation error.
  ∙ “𝐝𝐫𝐨𝐩𝐴 ”, a function of type 1 ⟜ 𝐴 that releases the resources contained in its
    argument.
  ∙ “𝐦𝐨𝐯𝐞(𝑥) in 𝑡”, an expression that places 𝑥 on top of the stack in 𝑡.
  ∙ “𝐫𝐚𝐢𝐬𝐞”, a value that inhabits any type with a given exception.
  ∙ “𝐭𝐫𝐲 𝑥 ⇐ 𝑡 in 𝑢 𝐮𝐧𝐥𝐞𝐬𝐬 𝑒 ⇒ 𝑢′ ”, an expression that catches exceptions occuring in 𝑡
    based on [4].


                                                        17
We call   the fragment of  ,𝐦𝐨𝐯𝐞 without 𝐦𝐨𝐯𝐞. Also, from now on we leave polarity
annotations implicit because they can always be inferred from the type.
   The grammar of types is unchanged:
                           {
                               Positive types        𝑃,𝑄 ⩴ 𝑅 ∣ 1 ∣ 𝐴 ⊗ 𝐵 ∣ 𝐴 ⊕ 𝐵
          Types 𝐴, 𝐵 ∶
                               Negative types        𝑁, 𝑀 ⩴ 𝐵 ⟜ 𝐴 ∣ 𝐴 & 𝐵

However, the interpretation of types is changed, since each positive type is assigned a
chosen destructor.
    The calculus is parameterised by a type of exceptions 𝐸. In   , exceptions must
not exchange resources during stack unwinding, so we add the constraint that 𝐸 is
a purely-positive type without resource. We also assume given some closed value ⊢
Alloc_failure ∶ 𝐸, which is the exception raised whenever an allocation fails. (For
instance, 𝐸 = 1 and Alloc_failure = ().) We will rely on terms swap𝐴
                                                                   𝑊
                                                                       in   defined as
in  (section 2.3).


4.2   Move as an effectful exchange rule

As explained in section 1.4, the category C∕𝑇 𝐼 in the situation (15) depicted above is not
symmetric in general. However, when C is symmetric, there is nevertheless an effectful
map 𝐴 ⊗ 𝐵 → 𝐵 ⊗ 𝐴, as found in the following hom-set:

           C∕𝑇 𝐼 (𝐴 ⊗ 𝐵, 𝐹  𝑈  (𝐵 ⊗ 𝐴)) ≅ C(𝑈  𝐴 ⊗ 𝑈  𝐵, 𝑈  𝐵 ⊗ 𝑈  𝐴)

This is reflected in  ,𝐦𝐨𝐯𝐞 with the operation 𝐦𝐨𝐯𝐞 which exchanges variables. It is
not presented as a structural rule in the traditional way: it indeed performs an effect and
does not commute with other rules. In the following example, two terms allocate three
resources and then frees them in reverse order. They would be identified if 𝐦𝐨𝐯𝐞 was
treated as a structural rule in the usual manner (e.g. as in ), but they behave differently:

        let 𝑟 = 𝐧𝐞𝐰() in                        let 𝑟 = 𝐧𝐞𝐰() in
        let 𝑠 = 𝐧𝐞𝐰() in                        let 𝑠 = 𝐧𝐞𝐰() in 𝐦𝐨𝐯𝐞(𝑟) in
        let 𝑡 = 𝐧𝐞𝐰() in                        let 𝑡 = 𝐧𝐞𝐰() in
        𝐝𝐫𝐨𝐩𝑅 𝑡; 𝐝𝐫𝐨𝐩𝑅 𝑠; 𝐝𝐫𝐨𝐩𝑅 𝑟               𝐝𝐫𝐨𝐩𝑅 𝑡; 𝐦𝐨𝐯𝐞(𝑠) in 𝐝𝐫𝐨𝐩𝑅 𝑠; 𝐝𝐫𝐨𝐩𝑅 𝑟

Both terms allocate three resources then frees them in reverse order. If the allocation
of 𝑡 fails, then the raised exception will free the first two resources in a different order,
which can be observed with the evaluation context ∣ ⋆ ∣ [𝑟0 , 𝑟1 ]⟩: the final free-lists are
respectively [𝑟0 , 𝑟1 ] and [𝑟1 , 𝑟0 ].
    For this reason, 𝐦𝐨𝐯𝐞 cannot give rise to a contextual isomorphism [32] between
𝐴 ⊗ 𝐵 and 𝐵 ⊗ 𝐴 for arbitrary 𝐴 and 𝐵, that is, which would allow us to replace
𝐴 ⊗ 𝐵 with 𝐵 ⊗ 𝐴 in arbitrary context without changing the meaning. Since a contextual
isomorphism just requires inverses and purity (thunkability) [32], 𝐦𝐨𝐯𝐞 must be effectful
in any reasonable interpretation.


                                                18
4.3   Translation into 
Each type 𝐴 has a positive interpretation 𝐴+ equipped with a destructor written drop𝐴
and a negative interpretation 𝐴− .

            1+ ≝ 1                        drop1 ≝ 𝜆𝑣.𝑣
             +
            𝑅 ≝𝑅                        drop𝑅 ≝ 𝜆𝑟. 𝐝𝐞𝐥𝐞𝐭𝐞 𝑟
             +       +     +
                                                     (                            )
      (𝐴 ⊗ 𝐵) ≝ 𝐴 ⊗ 𝐵               drop(𝐴⊗𝐵) ≝ 𝜆𝑝.𝛿 𝑝, (𝑎, 𝑏).(drop𝐵 𝑏; drop𝐴 𝑎)
                                                     (                          )
      (𝐴 ⊕ 𝐵)+ ≝ 𝐴+ ⊕ 𝐵 +           drop(𝐴⊕𝐵) ≝ 𝜆𝑠.𝛿 𝑠, 𝑎.(drop𝐴 𝑎), 𝑏.(drop𝐵 𝑏)
           𝑁 + ≝ ⇓𝑁 −                    drop𝑁 ≝ 𝜆𝑎.𝜋2 𝑎
      (𝐵 ⟜ 𝐴)− ≝ 𝐵 − ⟜ 𝐴+
      (𝐴 & 𝐵)− ≝ 𝐴− & 𝐵 −                    ⋆+ ≝ ⋆
            𝑃 − ≝ ⇑𝑃 +             (Γ, 𝑥 ∶ 𝐴)+ ≝ Γ+ , 𝑥 ∶ 𝐴+

Note that for any purely positive type (hence also 𝐸), we have 𝑊 + = 𝑊 . We define
three expressions which we use in the translation:
  ∙ Γ+ ⊢ drop_ctxΓ ∶ 1 by induction on Γ, which drops each variable from right to left.

            drop_ctx⋆ ≝ ()
         drop_ctxΓ,𝑥∶𝐴 ≝ drop𝐴 𝑥; drop_ctxΓ

  ∙ Γ+ , 𝑒 ∶ 𝐸 ⊢ unwindΓ (𝑒) ∶ 𝐸 by induction on Γ, which drops the context and returns
    𝑒.

           unwind⋆ (𝑒) ≝ 𝑒
                                                   (                                )
        unwindΓ,𝑥∶𝐴 (𝑒) ≝ let 𝑝 = swap𝐴
                                      𝐸 (𝑥, 𝑒) in 𝛿 𝑝, (𝑒, 𝑥).(drop𝐴 𝑥; unwindΓ (𝑒))

  ∙ Γ+ , 𝑒 ∶ 𝐸 ⊢ raise𝐴        −
                      Γ (𝑒) ∶ 𝐴 by induction on 𝐴, which drops the context and inhabits
     −
    𝐴 with 𝑒.

           raise𝐶⟜𝐵
                Γ   (𝑒) ≝ 𝜆𝑏. raise𝐶
                                   𝑏∶𝐵,Γ (𝑒)
           raise𝐵&𝐶
                Γ   (𝑒) ≝ ⟨raise𝐵           𝐶
                                Γ (𝑒), raiseΓ (𝑒)⟩
              raise𝑃Γ (𝑒) ≝ let 𝑒′ = unwindΓ (𝑒) in 𝜄2 𝑒′
We then translate  ,𝐦𝐨𝐯𝐞 derivations with two functions noted J−K defined by mutual
induction on derivations of the two kinds of judgements:
  ∙  ,𝐦𝐨𝐯𝐞 values of type Γ ⊢ 𝐴 are translated to  values of type Γ+ ⊢ 𝐴+ .
  ∙  ,𝐦𝐨𝐯𝐞 expressions of type Γ ⊢ 𝐴 are translated to  expressions of type Γ+ ⊢
    ⇓𝐴− .
   We add explicit coercions to treat positive values as expressions with the notation
coerc(𝑣). The monad strength for 𝑇  can be observed when translating let bindings of
expressions, where the context of the continuation is dropped in case of an error.

       𝑎𝑥 ∶ J𝑥 ⊢ 𝑥 ∶ 𝐴K ≝ 𝑥


                                             19
    𝐝𝐫𝐨𝐩 ∶ J⊢ 𝐝𝐫𝐨𝐩 ∶ 1 ⟜ 𝐴K ≝ ⟨drop𝐴 , ()⟩
    coerc ∶ JΓ ⊢ coerc(𝑣) ∶ 𝑃 K ≝ ⟨𝜄1 J𝑣K, drop_ctxΓ ⟩
    𝐦𝐨𝐯𝐞 ∶ JΓ, 𝑥 ∶ 𝐴, Δ ⊢ 𝐦𝐨𝐯𝐞(𝑥) in 𝑡 ∶ 𝐶K ≝ J𝑡K
                                                 (                                   )
     𝐧𝐞𝐰 ∶ J⊢ 𝐧𝐞𝐰 ∶ 𝑅 ⟜ 1K ≝ let 𝑥 = 𝐧𝐞𝐰() in 𝛿 𝑥, 𝑟.(𝜄1 𝑟), 𝑖.(𝑖; 𝜄2 Alloc_failure)
      let 𝑣 ∶ JΓ, Δ ⊢ let 𝑥 = (𝑣 ∶ 𝐴) in 𝑡 ∶ 𝐵K ≝ let 𝑥 = J𝑣K inJ𝑡K
      let 𝑡 ∶ JΓ, Δ ⊢ let 𝑥 = (𝑡 ∶ 𝑃 ) in 𝑢 ∶ 𝐴K
                                    (                          )
               ≝ let 𝑠 = 𝜋1 J𝑡K in 𝛿 𝑠, 𝑥.J𝑢K, 𝑒. raiseΓ𝐴&𝐼 (𝑒)
    𝐫𝐚𝐢𝐬𝐞 ∶ J⊢ 𝐫𝐚𝐢𝐬𝐞 ∶ 𝐴 ⟜ 𝐸K ≝ ⟨𝜆𝑒. raise𝐴
                                          ⋆ (𝑒), ()⟩
      𝐭𝐫𝐲 ∶ JΓ, Δ ⊢ 𝐭𝐫𝐲 𝑥 ⇐ (𝑡 ∶ 𝑃 ) in 𝑢 𝐮𝐧𝐥𝐞𝐬𝐬 𝑒 ⇒ 𝑢′ ∶ 𝐵K
             ≝ let 𝑠 = 𝜋1 J𝑡K in 𝛿(𝑠, 𝑥.J𝑢K, 𝑒.J𝑢′ K)
       ⊗𝑖 ∶ JΓ, Δ ⊢ (𝑣, 𝑤) ∶ 𝐴 ⊗ 𝐵K ≝ (J𝑣K, J𝑤K)
      ⊗𝑒 ∶ JΓ, Δ, Γ′ ⊢ 𝛿(𝑣, (𝑥, 𝑦).𝑡) ∶ 𝐶K ≝ 𝛿(J𝑣K, (𝑥, 𝑦).J𝑡K)
       1𝑖 ∶ J⊢ () ∶ 1K ≝ ()
       1𝑒 ∶ JΓ, Δ, Γ′ ⊢ 𝛿(𝑣, ().𝑡) ∶ 𝐶K ≝ 𝛿(J𝑣K, ().J𝑡K)
      ⊕𝑖1 ∶ JΓ ⊢ 𝜄1 𝑣 ∶ 𝐴 ⊕ 𝐵K ≝ 𝜄1 J𝑣K
      ⊕𝑖2 ∶ JΓ ⊢ 𝜄2 𝑣 ∶ 𝐴 ⊕ 𝐵K ≝ 𝜄2 J𝑣K
      ⊕𝑒 ∶ JΓ, Δ, Γ′ ⊢ 𝛿(𝑣, 𝑥.𝑡, 𝑦.𝑢) ∶ 𝐶K ≝ 𝛿(J𝑣K, 𝑥.J𝑡K, 𝑦.J𝑢K)
       ⟜𝑖 ∶ JΓ ⊢ 𝜆𝑥.𝑡 ∶ 𝐵 ⟜ 𝐴K ≝ ⟨𝜆𝑥.𝜋1 J𝑡K, drop_ctxΓ ⟩
       ⟜𝑒 ∶ JΓ, Δ ⊢ 𝑣𝑤 ∶ 𝐵K ≝ ⟨(𝜋1 J𝑣K)J𝑤K, drop_ctxΓ,Δ ⟩
       &𝑖 ∶ JΓ ⊢ ⟨𝑡, 𝑢⟩ ∶ 𝐴 & 𝐵K ≝ ⟨⟨𝜋1 J𝑡K, 𝜋1 J𝑢K⟩, drop_ctxΓ ⟩
      &𝑒1 ∶ JΓ ⊢ 𝜋1 𝑣 ∶ 𝐴K ≝ ⟨𝜋1 𝜋1 J𝑣K, drop_ctxΓ ⟩
      &𝑒2 ∶ JΓ ⊢ 𝜋2 𝑣 ∶ 𝐵K ≝ ⟨𝜋2 𝜋1 J𝑣K, drop_ctxΓ ⟩
Note that expressions 𝑡 ∶ 𝑃 have a second component that is immediately discarded, and
they are evaluated eagerly. Hence, they are essentially expressions of type 𝐴 ⊕ 𝐸. The
operational semantics of an affine value 𝑣 is that of J𝑣K, and the operational semantics of
an affine expression 𝑡 is that of 𝜋1 J𝑡K.
Proposition 11. The translation defined above is well-defined: it preserves typing, and
it uses the exchange rule in the target only in the translation of 𝐦𝐨𝐯𝐞, so the translation
of the   fragment indeed falls into .
    More details for the preservation of typing are given in appendix D.1.
Theorem 12. For any expression 𝑡 of  ,𝐦𝐨𝐯𝐞 with a purely-positive type without re-
source 𝑊 , if ⟨𝜋1 J𝑡K ∣ ⋆ ∣ 𝑙⟩ ⇝∗ ⟨𝑣 ∣ ⋆ ∣ 𝑙′ ⟩ then 𝑙′ = 𝜎(𝑙) for some permutation 𝜎.
Moreover, if the expression does not contain “𝐦𝐨𝐯𝐞”, then 𝑙′ = 𝑙.
Proof. Since purely-positive types without resources are translated into themselves, one
has ⇓𝑊 − = (𝑊 ⊕ 𝐸) & 𝐼, hence 𝜋1 J𝑡K is a linear expression of type 𝑊 ⊕ 𝐸. By
hypothesis 𝐸 is purely-positive without resource, and so 𝑊 ⊕ 𝐸 is too. Hence, the
resource-safety property of  applies to 𝜋1 J𝑡K, as well as that of  if 𝑡 does not contain
“𝐦𝐨𝐯𝐞”. Those are precisely the properties we needed to prove.


                                               20
5   A presheaf model of 
The ordered calculus  shows some peculiarities compared to usual formulations of
ordered logic: it has a left arrow and no right arrow, and a right let binding without left
let binding. We find it illustrative to give a simple concrete model showing that these
peculiarities are natural and arise by construction upon consideration of the strengths for
the allocation monad.
     We interpret the calculus  in the presheaf category C ≝ 𝑒𝑡[𝐑] , with [𝐑] the
set of lists of natural numbers considered as a discrete category. We note ++ the non-
symmetric monoidal product on [𝐑] obtained by concatenating two lists of resources.
Its Day convolution [12] lifts it to a non-symmetric monoidal product in C with a right
closed and left closed structure, corresponding to the multiplicative fragment. We define
𝑅 ∈ 𝑒𝑡[𝐑] to be the indicator function for singleton lists. As a presheaf category, C has
products and coproducts. The initial algebra of 1 ⊕ (𝑅 ⊗ −) interpreting lists of resources
is the terminal object ⊤. Concretely, we have the following constructions in C:
                                             ∑
   ∙ The monoidal product (𝐴 ⊗ 𝐵)(𝑙) ≝ (𝑙1 ,𝑙2 )∈[𝑅]2 ∧(𝑙1 ++𝑙2 =𝑙) 𝐴(𝑙1 ) × 𝐵(𝑙2 ).
   ∙ The unit 1([]) ≝ {()}, 1(𝑙) ≝ ∅ is∏the indicator function for the empty list.
   ∙ The right arrow (𝐴 ⊸ 𝐵)(𝑙1 ) ≝ 𝑙2 ∈[𝑅] 𝐴(𝑙2 ) → 𝐵(𝑙1 ++ 𝑙2 ).
                                     ∏
   ∙ The left arrow (𝐵 ⟜ 𝐴)(𝑙2 ) ≝ 𝑙1 ∈[𝑅] 𝐴(𝑙1 ) → 𝐵(𝑙1 ++ 𝑙2 ).
   ∙ The type of resources 𝑅([𝑛]) ≝ {𝑛}, 𝑅(𝑙) ≝ ∅.
   ∙ The type of lists of resources [𝑅](𝑙) ≝ {𝑙}.
   ∙ The product (𝐴 & 𝐵)(𝑙) ≝ 𝐴(𝑙) × 𝐵(𝑙).
   ∙ The coproduct (𝐴 ⊕ 𝐵)(𝑙) ≝ 𝐴(𝑙) + 𝐵(𝑙).
    We exploit the fact that the canonical adjunction
                             𝐹 ≝ (− ⊗ [𝑅]) ⊣ 𝐺 ≝ [𝑅] ⊸ −
for the allocation monad is made of endofunctors such that
                                  𝐴 ⊗ 𝐹 𝐵 ≅ 𝐹 (𝐴 ⊗ 𝐵)                                   (16)
to interpret positive and negative terms in the same category: this allows us to adapt the
model theory of [11] while avoiding the formalism of enriched categories.
     We now have all the ingredients to interpret derivations of  (fig. 1). In fact, we will
interpret derivations of ordered terms with resources from fig. 4 which extends the typing
rules of . Expressions typed with Γ; [𝑟1 ⋯ 𝑟𝑛 ]; Δ ⊢𝑜 𝐴 are interpreted as (oblique)
morphisms in C(𝐹 (Γ ⊗ 𝑅𝑛 ⊗ Δ), 𝐴), following [11] which we adapt to the ordered case
(see appendix E for the complete definition of the interpretation).
     Interpreting the left function and the right let binding uses the isomorphism (16) as a
left strength. We cannot interpret a right function or left let-binding for , as it would
require an isomorphism 𝐹 𝐴 ⊗ 𝐵 ≅ 𝐹 (𝐴 ⊗ 𝐵) which swaps the ambient list of resources
with 𝐵. This corresponds to the re-ordering of resources by the incorrect term 𝑡𝑟 (14).
Lemma 13 (Substitution lemma). For all Θ′′ ⊢𝑜 𝑣 ∶ 𝐴 and Θ, 𝑥 ∶ 𝐴 @ Θ′ ⊢𝑜 𝑡 ∶ 𝐵,
one has J𝑡[𝑣∕𝑥]K = (𝑖𝑑Θ+ ⊗ J𝑣K ⊗ 𝑖𝑑Θ′+ ); J𝑡K (see appendix E.2).
Theorem 14 (Soundness of the interpretation). For all 𝐿, 𝑐, 𝑐 ′ such that 𝐿 ⊢𝑜 𝑐 and
𝐿 ⊢𝑜 𝑐 ′ , if 𝑐 ⇝ 𝑐 ′ then J𝑐K = J𝑐 ′ K (see appendix E.3).


                                             21
5.1    Exceptions and destructors
Exceptions need to be chosen among central objects in order to define a strength for the
exception monad. We ask for objects that commute with all other objects 𝐴 in a coherent
way. Those are the objects in the Drinfeld centre of C (as defined e.g. in [41, §3]).
Proposition 15. Given an object 𝐸, the three following properties are equivalent:
    ∙ 𝐸 is in the Drinfeld centre of C.
    ∙ 𝐸 is resource-free: for all non-empty list 𝑙, 𝐸(𝑙) = ∅.
    ∙ 𝐸 has a trivial destructor: there is a morphism C(𝐸, 𝐼).
See the proof in appendix E.4. By induction, central types in  are resource-free, therefore
they belong to the Drinfeld centre of C.
Proposition 16. Every object in C has a (unique) destructor, but C is not a model of
affine logic in the sense of having an isomorphism 𝐼 ≅ ⊤ (cf. [9, §3.2]).
Proof. Recall that [𝑅] = ⊤ is the terminal object. Destructors for 𝐴 are objects in
(𝐴, 𝛿) ∈ C∕𝑇 𝐼; i.e. 𝛿 ∈ C(𝐴, 𝑇 𝐼) ≅ C(𝐴, [𝑅] ⊸ [𝑅]) ≅ C(𝐴 ⊗ ⊤, ⊤) and no other
condition. By the universal property of ⊤ there exists a unique such morphism. On the
other hand, only central objects have a trivial destructor C(𝐴, 𝐼), which is not the case
for [𝑅] = ⊤.
  Given that any Γ has a unique destructor, one has C∕𝑇 𝐼 ≅ C. In particular, the
monad 𝑇  is left strong.
Proposition 17. Let 𝐸 a central object. The monad 𝑇  where  = (− ⊕ 𝐸) has a left
strength Γ ⊗ 𝑇 𝐴 → 𝑇 (Γ ⊗ 𝐴).
Thus, this gives a model of an affine logic in the sense of the calculus with destructors   ,
but we do not have a model of affine logic in the usual sense of semi-cartesian monoidal
categories. Even if we consider that the monoidal unit 𝐼 is indeed terminal in the Kleisli
category of 𝑇 , the destructors are not thunkable for 𝑇 , a common requirement for mor-
phisms interpreting structural rules in premonoidal categories (see e.g. Führmann [17]).
This is another way of observing the fact that weakening performs a side effect.
    We might wonder how we could extend this model to ones of  and  ,𝐦𝐨𝐯𝐞 . This
amounts to somehow regaining the symmetry of the monoidal product to interpret
the exchange rule. One way to do that would be to quotient our base category [𝐑]
to obtain multisets. However, 𝑇 would become commutative and so C∕𝑇 𝐼 would be
symmetric; intuitively the model does not observe the order of destruction. Instead,
adding permutations as isomorphisms in [𝐑] would result in a presheaf model on a setoid
in which 𝑇 is not commutative; intuitively the model tracks in the interpretation of terms
their action on the free-list of resources. As we cannot re-use our trick with endofunctors
to avoid the presheaf-enriched formalism, we leave this as future work.

6     Discussion and perspectives
After this formal development, we find it useful to place our results in the context of the
theory and practice of programming languages.


                                             22
6.1     Integrating linear types and error handling

We modelled a global allocator with a linear state monad to study notions of resource-
safety for linear calculi: for instance, every allocated resource in  and  ,𝐦𝐨𝐯𝐞 is freed
exactly once, even in case of errors during the execution of the program. This result
strengthens when the exchange rule (6) is not used: in  and   , the resources are
released in a LIFO order. A relationship between ordered logic and stack-like allocation
was proposed previously [47, 48, 58, 45]. In this context, our results suggest to consider
a variant of ordered logic that only has one arrow type and whose composition (let) is
restricted to the opposite side of abstraction (𝜆)—where in particular 𝜆 cannot express let.
The modelling of the exchange rule with a side-effecting “move” operation is also novel.
     Conceptually close to stack allocation, LISP’s higher-order combinator
unwind-protect that executes a clean-up function upon normal or exceptional re-
turn of its argument (like its variants found in modern academic programming languages
such as OCaml and Haskell) has the same constraint of deallocation in LIFO order.
     “Linear types,” on the other hand, promised to let us manipulate resources as first-
class values (see [2, 1] among others). However, extensive practical experiments with
linear types stumbled (among other) on the problematic interaction of linearity with error
handling, another important aspect with resources that are acquired in a program. For
instance, Cyclone, a source of inspiration for the Rust language, permitted resource leaks
in the name of “flexibility and usability” [53, §3.5] (necessitating back-up collection
mechanisms). The practical experiment of Tov and Pucella [57, 55], another milestone in
exploring practical aspects of linear type systems, also mentioned the issue of combining
linearity and control effects, which became the motivation for their “practical” linear
type system to be affine.
     Tov and Pucella [56], separately, seeking to lift the limitation of the affine system
for manipulating resources as first-class values, proposed a type system that offers both
linearity and control effects (e.g. checked exceptions), by typing effects in addition
to linearity. Essentially, effects are constrained when linear variables are in scope (or
conversely), matching the restrictive approach we described in section 1.2 corresponding
to the notion of strength with respect to an affine or an unrestricted resource modality (8).
It should be noted that this system [56], unlike the previous experiment [57], is mainly
justified by its mathematical properties; how useful such a system is, in practice, remains
unclear.5
     Lastly, affine session types [40] do mix linearity and cancellation in a sense similar
to ours. They guarantee a safety property (absence of deadlock) after an exception
(cancellation) arises, by communicating cancellation across channels.
     Our analysis from the introduction applies equally to explicit error handling with an
error monad, as illustrated with the language . Indeed, manual error handling encounters
similar obstacles arising from the lack of unrestricted monadic strength for the error
monad. Concretely, for each location where one would like to use a monadic binding (4),
 5
     As Tov themselves explains: “One question that remains, however, concerns the pragmatics
     of checked exceptions in a higher-order language such as Alms, where latent exception effects
     are likely to appear on many function arrows. Weighing the cost against the benefit, I have
     decided that adding linear types to Alms is not worth the complexity of a programmer-visible
     effect system.” [55, p. 238]


                                                23
one needs to implement by hand a repetitive description of whichever clean-up functions
should be called in case of error propagation—a well-known and tedious problem in C,
which gave rise to specific programming patterns involving goto (see appendix A).
     By 2012, these limitations of linear types with respect to the handling of errors and
exceptions, arising from practical considerations, might seem well-established in the
literature. However, more recent works on linear type systems purporting to implement
practical first-class resources in academic programming languages [6, 44] do not explore
nor mention these obstacles. In the case of [6], a section describing limitations arising
from Haskell exceptions indeed appears in an earlier version with a different title [7], but
is absent from the published peer-reviewed version.
     With the resource CBPV, we set out to model some aspects of C++ resources with
destructors and move operations. Compared to the works cited previously, C++ realised,
much earlier [52], a shift in viewpoint whereby clean-up functions are deduced from
the types, whilst it also later pioneered “move semantics” [24] for treating resources as
first-class values. As we have seen, interpreting resource types in the slice category over
some 𝑇 𝐼, i.e. as types provided with some chosen effectful weakening map 𝐴 → 𝑇 𝐼,
suffices to provide a notion of strength for the exception (or error) monad. Concretely this
means that we can both program with an error monad, and give a meaning to exceptions
as a side-effect. One surprising aspect of the resource CBPV is that it combines facets of
all three of affine, linear and ordered logics:

          affine in terms of types and available control effects
          linear in terms of first-class values and resource-safety properties
         ordered in terms of proof-relevant semantics and type isomorphisms
Given that the logical expressiveness is that of affine logic (including the exchange rule),
without sacrificing the linear character of values (which are correctly released), we do
not have to choose between linearity and control effects. This perspective suggests that it
should be possible to adapt practical works on affine typing (in the lineage of [57]) in
order to integrate first-class resources in functional programming languages [43].

6.2   A model of C++/Rust-style resource management and its interpretation
The resource CBPV is a very idealised model of C++/Rust-style resource management
situated at the intersection of linear logic and the theory of effects. Various models of
ownership in Rust—more practical and less idealised—have been developed to prove
safety and functional properties of Rust programs, such as with separation logic [27], a
dedicated functional logic [13], or by translation into a purely functional language [25].
These recent works, explicitly, do not model exceptions with destructor calls, and they
do not develop a specific understanding of destructors in relationship with linearity.
     To our knowledge, our model is the first to reproduce various phenomena seen
with C++/Rust’s resource management such as: the propagation of errors involving the
release of resources in scope as part of monadic binding; destructors having to never
fail; resources being first-class values that can be passed, returned, or stored in algebraic
data types and closures, and for which “moving” resources (identified with an exchange
rule in logic, albeit performing a side-effect) is responsible for altering the order of


                                            24
destruction; and indeed closures themselves being resources. In fact, in the presence
of both resource modalities ! and , different positive types of closures, derived from
⟜, coexist (!(𝐴 ⟜ 𝐵) and (𝐴 ⟜ 𝐵)), distinguished by the restrictions on the typing
context in accordance with the resource modality (e.g. copyable or resource-like)—a
distinction between several types of closures that can also be seen in C++ and Rust.
    One very interesting aspect of the resource CBPV is that exchange and weakening
are interpreted by morphisms that perform effects. For instance, 𝐴 ⊗ 𝐵 and 𝐵 ⊗ 𝐴
are not contextually isomorphic in the language with destructors because they can be
distinguished observationally from the order in which the destructors of 𝐴 and 𝐵 are
executed. So we can have a logical equivalence in the form of inverse morphisms:
                                     𝐴⊗𝐵 ⇄𝐵⊗𝐴                                             (17)
without the two types being isomorphic. This is because a contextual notion of isomor-
phism (allowing to substitute equals by equals) also requires the two inverse maps (17)
to be pure [32]. This radically departs from symmetric premonoidal categories [49].
    We usually see the Curry-Howard correspondence at work when algebraic and logical
structures inspire new programming language features. Could the concept of destructors
have appeared out of theoretical consideration or practical experiments starting from
linear logic? As it turns out, the interpretation of resource types with destructors as ordered
logic formulae almost arose on several occasions, such as when Baker suggested that C++
constructors and destructors could fit within his linear language, in rarely-cited essays that
anticipated C++ move semantics [2, 1], and when Gan, Tov and Morrisett approached
substructural types using type classes dup and drop [18]. But we find it remarkable that
the Curry-Howard correspondence actually worked this time in the converse direction,
with C++ destructors and move semantics arising from practical consideration over more
than 20 years [28, 52, 24], and with the use of the slice category in this context being
prompted by empirically-observed phenomena with C++ resources [10].

6.3   Conclusion and future work
Our hope is that this newfound understanding of resources in programming will be inspire
improvements to programming languages and designs for better ones. It could also help
proving more properties of programs with formal methods, such as methods based on
translations into pure functional programs. Indeed, the functional correctness of some
Rust programs can depend on the resource-safety properties enforced by the language,
for instance when they use the typestate programming pattern or when they are made
fault-tolerant.
    The Curry-Howard correspondence is sometimes stated as a more technical result
relating logic, categorical structures and programming language models, as in the Curry-
Howard-Lambek correspondence for linear CBPV [11] which the present work is based
on. Though not essential to the results of this paper, it is now clear that extending the
Curry-Howard-Lambek correspondence to ordered CBPV would be useful as a meta-
theory to study resources. Removing the symmetry in monoidal categories and the
exchange rule in logic can create technical issues—we have made some progress already
by understanding that 𝜆 and let bindings work on opposite sides, and that being merely
left-closed or right-closed but not both is already interesting and useful.


                                             25
    Lastly, much remains to be understood in an idealised and principled manner within
this framework, the most obvious ones being:

  ∙ Copyable types Linear languages, including with C++ and Rust, mix in practice
    resource types and unconstrained types. The interaction of the resource modality
    arising from the slice construction with the resource modality ! which controls freely
    copyable and erasable types, should therefore be explored. A general mechanism of
    polarities should provide foundations for kind-based linear type systems [57] and
    extend them to computationally-relevant kinds in the style of Rust’s special traits
    (e.g. Copy, Drop). Interesting questions arise from the practical necessity of kind
    polymorphism in such languages.
  ∙ Borrowing We have modelled resources that can only be allocated and deallocated,
    which lets us observe the effect of deallocations on the final state of the program.
    More questions arise when resources can be used between their allocation and their
    deallocation. Operations that do not consume the resource can be implemented by
    returning it [2, 1]. Borrowing [20, 16], inspired by regions [54], and refined into
    unique borrowing in Rust, was introduced as a more usable and expressive alternative
    to this linear threading of values. As we already mentioned, various works account
    for borrowing using different approaches [27, 13, 25], but it remains to be seen
    whether and how borrowing may be derived in a principled way from a concept of
    linearity (ownership) arising from destructors.

Acknowledgements
We thank the anonymous reviewers for their detailed and thoughtful comments on earlier
versions of this article.


References
 1. Baker, H.G.: “Use-Once” Variables and Linear Objects - Storage Management, Reflection and
    Multi-Threading. SIGPLAN Notices 30(1), 45–52 (1995). https://doi.org/10.1145/
    199818.199860
 2. Baker, H.G.: Linear logic and permutation stacks - the Forth shall be first. SIGARCH Computer
    Architecture News 22(1), 34–43 (1994). https://doi.org/10.1145/181993.181999
 3. Baker, H.G.: Lively linear lisp: “Look ma, no garbage!” ACM Sigplan notices 27(8), 89–98
    (1992)
 4. Benton, N., Kennedy, A.: Exceptional syntax. Journal of Functional Programming 11, 395–410
    (2001). https://doi.org/10.1017/S0956796801004099
 5. Berdine, J., O’Hearn, P.W., Reddy, U.S., Thielecke, H.: Linearly used continuations. In:
    Proceedings of the Third ACM SIGPLAN Workshop on Continuations (CW’01), pp. 47–54
    (2000)
 6. Bernardy, J., Boespflug, M., Newton, R.R., Peyton Jones, S., Spiwack, A.: Linear Haskell:
    practical linearity in a higher-order polymorphic language. PACMPL 2(POPL), 5:1–5:29
    (2018). https://doi.org/10.1145/3158093
 7. Bernardy, J., Boespflug, M., Newton, R.R., Peyton Jones, S., Spiwack, A.: Retrofitting Linear
    Types (In submission), (2017). https://www.microsoft.com/en- us/research/wp-
    content/uploads/2017/03/haskell-linear-submitted.pdf.


                                              26
 8. Blute, R., Cockett, J., Seely, R.: ! and ?-Storage as tensorial strength. Mathematical Structures
    in Computer Science 6(4), 313–351 (1996)
 9. Braüner, T.: A model of intuitionistic affine logic from stable domain theory. In: International
    Colloquium on Automata, Languages, and Programming, pp. 340–351 (1994)
10. Combette, G., Munch-Maccagnoni, G.: A resource modality for RAII (abstract). In: LOLA
    2018: Workshop on Syntax and Semantics of Low-Level Languages (2018). https://hal.
    inria.fr/hal-01806634
11. Curien, P.-L., Fiore, M., Munch-Maccagnoni, G.: A Theory of Effects and Resources: Adjunc-
    tion Models and Polarised Calculi. In: Proc. POPL (2016). https://doi.org/10.1145/
    2837614.2837652
12. Day, B.: On closed categories of functors. In: MacLane, S., Applegate, H., Barr, M., Day, B.,
    Dubuc, E., Phreilambud, Pultr, A., Street, R., Tierney, M., Swierczkowski, S. (eds.) Reports of
    the Midwest Category Seminar IV, pp. 1–38. Springer Berlin Heidelberg, Berlin, Heidelberg
    (1970)
13. Denis, X., Jourdan, J.-H., Marché, C.: Creusot: a Foundry for the Deductive Verification of Rust
    Programs. In: ICFEM 2022 - 23th International Conference on Formal Engineering Methods.
    LNCS, Springer, Heidelberg (2022). https://inria.hal.science/hal-03737878
14. Filinski, A.: Linear Continuations. In: Proc. POPL, pp. 27–38 (1992)
15. Filinski, A.: Representing Monads. In: Proc. POPL, pp. 446–457. ACM Press (1994)
16. Fluet, M., Morrisett, G., Ahmed, A.J.: Linear Regions Are All You Need. In: Sestoft, P. (ed.)
    Programming Languages and Systems, 15th European Symposium on Programming, ESOP
    2006, Held as Part of the Joint European Conferences on Theory and Practice of Software,
    ETAPS 2006, Vienna, Austria, March 27-28, 2006, Proceedings. LNCS, vol. 3924, pp. 7–21.
    Springer, Heidelberg (2006). https://doi.org/10.1007/11693024_2
17. Führmann, C.: Direct Models for the Computational Lambda Calculus. Electr. Notes Theor.
    Comput. Sci. 20, 245–292 (1999)
18. Gan, E., Tov, J.A., Morrisett, G.: Type Classes for Lightweight Substructural Types. In: Alves,
    S., Cervesato, I. (eds.) Proceedings Third International Workshop on Linearity, LINEARITY
    2014, Vienna, Austria, 13th July, 2014. EPTCS, pp. 34–48 (2014). https://doi.org/10.
    4204/EPTCS.176.4
19. Girard, J.-Y.: Linear Logic. Theoretical Computer Science 50, 1–102 (1987)
20. Grossman, D., Morrisett, J.G., Jim, T., Hicks, M.W., Wang, Y., Cheney, J.: Region-Based
    Memory Management in Cyclone. In: Knoop, J., Hendren, L.J. (eds.) Proceedings of the 2002
    ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI),
    Berlin, Germany, June 17-19, 2002, pp. 282–293. ACM (2002). https://doi.org/10.
    1145/512529.512563
21. Hasegawa, M.: Linear Exponential Comonads without Symmetry. In: Fourth International
    Workshop on Linearity (2016). http://arxiv.org/abs/1701.04919
22. Hasegawa, M.: Linearly Used Effects: Monadic and CPS Transformations into the Linear
    Lambda Calculus. In: Hu, Z., Rodríguez-Artalejo, M. (eds.) Functional and Logic Program-
    ming, 6th International Symposium, FLOPS 2002, Aizu, Japan, September 15-17, 2002,
    Proceedings. LNCS, vol. 2441, pp. 167–182. Springer, Heidelberg (2002). https://doi.
    org/10.1007/3-540-45788-7_10
23. Hasegawa, M.: Semantics of linear continuation-passing in call-by-name. In: International
    Symposium on Functional and Logic Programming, pp. 229–243 (2004)
24. Hinnant, H.E., Dimov, P., Abrahams, D.: A Proposal to Add Move Semantics Support to the
    C++ Language, (2002). http://www.open-std.org/jtc1/sc22/wg21/docs/papers/
    2002/n1377.htm
25. Ho, S., Protzenko, J.: Aeneas: Rust Verification by Functional Translation. Proc. ACM Program.
    Lang. 6(ICFP) (2022). https://doi.org/10.1145/3547647


                                                27
26. Hofmann, M.: A Type System for Bounded Space and Functional In-Place Update. Nord. J.
    Comput. 7(4), 258–289 (2000)
27. Jung, R., Jourdan, J., Krebbers, R., Dreyer, D.: RustBelt: securing the foundations of the rust
    programming language. PACMPL 2(POPL), 66:1–66:34 (2018). https://doi.org/10.
    1145/3158154
28. Koenig, A., Stroustrup, B.: Exception Handling for C++. In: Proceedings of the C++ Confer-
    ence. San Francisco, CA, USA, April 1990, pp. 149–176 (1990)
29. Lafont, Y.: The linear abstract machine. Theoretical computer science 59(1-2), 157–180 (1988)
30. Levy, P.B.: Call-By-Push-Value: A Functional/Imperative Synthesis (Semantics Structures in
    Computation, V. 2). Kluwer Academic Publishers, USA (2004)
31. Levy, P.B.: Call-by-Push-Value: A Subsuming Paradigm. In: Proc. TLCA ’99, pp. 228–242
    (1999)
32. Levy, P.B.: Contextual isomorphisms. In: Proceedings of the 44th ACM SIGPLAN Symposium
    on Principles of Programming Languages, pp. 400–414 (2017)
33. Maraist, J., Odersky, M., Turner, D.N., Wadler, P.: Call-by-Name, Call-by-Value, Call-by-Need,
    and the Linear Lambda Calculus. In: Proc. MFPS ’95 (1994)
34. Melliès, P.-A.: “Categorical models of linear logic revisited”. working paper or preprint.
35. Melliès, P.-A.: “Categorical semantics of linear logic”. In: vol. 27. Panoramas et Synthèses.
    Société Mathématique de France, 2009. Chap. 1, pp. 15–215.
36. Melliès, P.-A.: “Parametric monads and enriched adjunctions”. Draft.
37. Møgelberg, R.E., Staton, S.: Linear usage of state. Log. Methods Comput. Sci. 10(1) (2014).
    https://doi.org/10.2168/LMCS-10(1:17)2014
38. Moggi, E.: Computational lambda-calculus and monads. In: Proceedings of the Fourth Annual
    IEEE Symposium on Logic in Computer Science (LICS 1989), pp. 14–23. IEEE Computer
    Society Press, Pacific Grove, CA, USA (1989)
39. Moggi, E.: Notions of computation and monads. Information and Computation 93(1), 55–92
    (1991). https://doi.org/10.1016/0890-5401(91)90052-4
40. Mostrous, D., Vasconcelos, V.T.: Affine Sessions. Logical Methods in Computer Science,
    Volume 14, Issue 4 (November 15, 2018) lmcs:4973 (2018). https://doi.org/10.23638/
    LMCS-14(4:14)2018. arXiv: 1809.02781v2 [cs.LO]
41. Müger, M.: From subfactors to categories and topology II: The quantum double of tensor
    categories and subfactors. Journal of Pure and Applied Algebra 180(1), 159–219 (2003).
    https://doi.org/10.1016/S0022-4049(02)00248-7
42. Munch-Maccagnoni, G.: Note on models of polarised intuitionistic logic. Tech. rep., INRIA
    (2017). https://hal.inria.fr/hal-01540760
43. Munch-Maccagnoni, G.: Resource Polymorphism, (2018). https://doi.org/10.48550/
    arXiv.1803.02796.
44. Orchard, D., Liepelt, V.-B., Eades III, H.: Quantitative program reasoning with graded modal
    types. Proc. ACM Program. Lang. 3(ICFP) (2019). https://doi.org/10.1145/3341714
45. Pfenning, F., Simmons, R.J.: Substructural Operational Semantics as Ordered Logic Program-
    ming. In: Proceedings of the 24th Annual IEEE Symposium on Logic in Computer Science,
    LICS 2009, 11-14 August 2009, Los Angeles, CA, USA, pp. 101–110. IEEE Computer Society
    (2009). https://doi.org/10.1109/LICS.2009.8
46. Plotkin, G., Power, J.: “Notions of Computation Determine Monads”. In: Foundations of
    Software Science and Computation Structures. Springer Berlin Heidelberg, 2002, pp. 342–356.
    ISBN : 9783540459316. https://doi.org/10.1007/3-540-45931-6_24.
47. Polakow, J.: Ordered Linear Logic and Applications. PhD thesis, Carnegie Mellon University
    (2001).
48. Polakow, J., Yi, K.: Proving Syntactic Properties of Exceptions in an Ordered Logical Frame-
    work. In: Kuchen, H., Ueda, K. (eds.) Functional and Logic Programming, 5th International


                                               28
    Symposium, FLOPS 2001, Tokyo, Japan, March 7-9, 2001, Proceedings. LNCS, vol. 2024,
    pp. 61–77. Springer, Heidelberg (2001). https://doi.org/10.1007/3-540-44716-4_4
49. Power, A.J., Robinson, E.: Premonoidal categories and notions of computation. Mathematical
    Structures in Computer Science 5(7), 453–468 (1997)
50. Power, J.: Premonoidal categories as categories with algebraic structure. Theoretical Computer
    Science 278(1), 303–321 (2002). https://doi.org/10.1016/S0304-3975(00)00340-6
51. Selinger, P., Valiron, B.: A linear-non-linear model for a computational call-by-value lambda
    calculus. Lecture Notes in Computer Science 4962, 81–96 (2008)
52. Stroustrup, B.: A History of C++: 1979–1991. In: The Second ACM SIGPLAN Conference
    on History of Programming Languages. HOPL-II, pp. 271–297. Association for Computing
    Machinery, Cambridge, Massachusetts, USA (1993). https://doi.org/10.1145/154766.
    155375
53. Swamy, N., Hicks, M., Morrisett, G., Grossman, D., Jim, T.: Safe manual memory management
    in Cyclone. Science of Computer Programming 62(2), 122–144 (2006)
54. Tofte, M., Talpin, J.-P.: Region-based memory management. Information and computation
    132(2), 109–176 (1997)
55. Tov, J.A.: Practical Programming with Substructural Types. PhD thesis, Northeastern Univer-
    sity (2012).
56. Tov, J.A., Pucella, R.: A Theory of Substructural Types and Control. In: Proceedings of the
    2011 ACM International Conference on Object Oriented Programming Systems Languages
    and Applications. OOPSLA ’11, pp. 625–642. ACM, Portland, Oregon, USA (2011). https:
    //doi.org/10.1145/2048066.2048115
57. Tov, J.A., Pucella, R.: Practical affine types. In: Ball, T., Sagiv, M. (eds.) Proceedings of
    the 38th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
    POPL 2011, Austin, TX, USA, January 26-28, 2011, pp. 447–458. ACM (2011). https:
    //doi.org/10.1145/1926385.1926436
58. Walker, D.: Substructural type systems. In: Advanced Topics in Types and Programming
    Languages. Ed. by B.C. Pierce, pp. 3–44. The MIT Press (2005)


A    Context: resource management in programming

Programmers must sometimes deal with resources: values denoting some memory al-
locations, files, locks, etc.—in general reifying some knowledge about the state of the
world—that must be disposed of at specific points in the program to ensure its proper
functioning. For instance, some task might operate on a file descriptor, obtained and
released through operating system calls, as illustrated with the following pseudo-code:
    let f = open_file (" record . txt ");
    append (f , " starting tasks ");
    run_tasks ( f );
    close_file ( f );
                             Listing 1.1. Opening and closing a file

    It is generally a good idea to close files in a timely manner: for instance, depending
on the operating system and its command, the number of files that the program is allowed
to keep opened concurrently can be fairly low. Another common phenomenon affecting
resources is that their acquisition can fail, which actually complicates the problem of
correctly disposing of resources: it must be carefully done in case of failure of later


                                               29
resource acquisitions. This is where C programmers resort to using goto—one of the
only situations where it is not only allowed but idiomatic; in pseudo-code:
     let f = open_file (" record . txt ");
     if ! f return ;
     append (f , " starting tasks ");
     let g = open_file (" output . txt ");
     if ! g goto err ;
     run_tasks (f , g );
     close_file ( g );
   err :
     close_file ( f );
                            Listing 1.2. Handling errors with goto

Here, f is closed whether opening g succeeds or not.
   Managing resources, especially explicitly as in C, comes with specific concerns:
 1. disposing of the resource in a timely fashion in all the code paths (avoiding leaks, as
    we have seen),
 2. keeping track of who is responsible for disposing of the resource (to avoid for instance
    that the resource is disposed of twice),
 3. making sure that a resource is never used after its disposal (use-after-free).
    In simple situations like the previous one, and in languages that support it, the
resources can be managed automatically with higher-order scoped combinators derived
from LISP’s unwind-protect:
   with_file (" record . txt " , 𝜆 f .
      append (f , " starting tasks ");
      with_file (" output . txt " , 𝜆 g .
         run_tasks (f , g )
      );
   );
              Listing 1.3. Handling errors with higher-order scoped combinators

In words, the combinator with_file opens the file and passes the file descriptor to its
argument. It closes the file upon normal or exceptional return, and returns the same value
that is returned by the functional argument.
     Now, this approach with scoped combinators comes with several limitations. Firstly,
they force resources to be disposed of in a strict LIFO order. They do not model situations
where the duty of clean-up is transferred to the caller or to a callee, nor where the resource
is stored in a data structure. This limits expressiveness but also compositionality, the
ability to reorganise the program in smaller and/or more general parts. In effect, scoped
combinators solve (1) and (2) above albeit in a heavy-handed way.
     The second limitation has to do with the transient nature of the value they pass to their
functional argument: this argument is indeed meaningful for the duration of the scope
only, since using the value after the scope ends (by sneaking it inside the return value, or
by storing it inside some mutable data structure) is an attempt to use the resource after


                                             30
its disposal (3). Yet, keeping track of the value can be far from obvious, especially when
programming using other (e.g. monadic) combinators.
     We focused in this paper on using a notion of ownership, generally understood to
be related to linearity, to lift the first limitation using. We elaborated more precisely a
formal link between a notion of ownership present in the C++ and Rust programming
languages, that has not seen much theoretical study, and linearity. We did not attempt to
model the second limitation, which is already the subject of much study involving other
theoretical tools.


A.1   C++ destructors

Independently from linear types, modern systems programming languages such as C++
and Rust have since the 1980’s evolved automatic resource-management features that
not only combine well with error management and control effects, but in which error
handling is an essential part—indeed resource management requires to deal with the
correct disposal of resources, but also the handling of possible failure of their allocation.
Furthermore, links with linear logic were suggested as early as [2], but remained elusive.
    Each type 𝐴 comes equipped with a destructor, a clean-up action that removes a
value of 𝐴. It is called when such variable goes out of scope, because of an explicit
return or an exception. Destructors provide a notion of ownership, tying resources to
variables lifetime. Local variables hence yields a LIFO ordering for handling resources.
The previous example would be written like this in C++:
   File f {" record . txt "};
   append (f , " starting tasks ");
   File g {" output . txt "};
   run_tasks (f , g );
   // g then f are then closed by their destructors
                        Listing 1.4. Handling errors with destructors

    Sometimes, the control flow of resources becomes more complex. For example, in
the following example, we transfer the file ownership to run_task, in the case where
tasks have been initialised. It then becomes difficult to track the places responsible to
call close_file, leading to potential leaks or errors. Also, this use case does not fit in
the pattern of higher-order combinators, which would always close the file at the end of
the scope.
   let f = open_file (" log . txt ");
   if ! f return ;
   if init_tasks () == ok :
        append (f , " starting tasks ");
        run_tasks ( f );
   else :
        append (f , " failure to init tasks ");
        close_file ( f );
            Listing 1.5. Pseudo-code for manual conditional transfer of ownership


                                             31
     To implement the transfer of ownership, C++ initially experimented with smart point-
ers such as the now-deprecated auto_ptr. So-called “move semantics” was introduced
in C++11 to fix the defects of auto_ptr in representing ownership and the excessive
amounts of deep copies encouraged by the language. So-called “move constructors” and
“move assignment operators”, associated to a notion of “rvalue reference”, enabled the
definition of “unique pointers” and a “move” operation to transfer ownership of values,
as illustrated below:
    File f {" log . txt "};
    if init_tasks () == ok {
        append (f , " starting tasks ");
        run_tasks ( std :: move ( f ));
    } else {
        append (f , " failure to init tasks ");
    }
                  Listing 1.6. C++ pseudo-code using a file to record operations

In effect, std::move is responsible for selecting the move constructor of File for its
argument; the move constructor is then responsible for implementing the move operation
which consists (most of the time) in a shallow copy into the target, followed by the
nullification of the source one (or at least its replacement with some valid, default value).
In this way, it is guaranteed that a single copy of the resource exists at any time, and the
destructor of f is not called (or more precisely, is called on a null or default value, which
does nothing). This notion of ownership in C++ can be described as ensuring that the
owner (responible for calling the destructor) is unique.
    In order to implement first-class resources, C++11 introduced language and standard
library features making it convenient to define resource datatypes, such as the rules for
the automatic derivation of move constructors (which, together with similar rules for
destructors, are responsible for instance for a struct of resources to behave as a resource
in the obvious manner). In actual usage (see e.g. the “rule of zero”), these are very close
to defining separate kinds of movable vs. copyable types.


B     Details: basic properties
B.1   Proof of 𝐬𝐰𝐚𝐩 and definition of 𝐬𝐰𝐚𝐩 inverse
We recall the expressions swap𝐴
                              𝑊
                                :

      swap𝐴
          𝐼 ≝ 𝜆𝑝.𝛿(𝑝, (𝑎, 𝑖).𝛿(𝑖, ().(⋆, 𝑎)))


swap𝐴
    𝑊 ⊕𝑊 ≝ 𝜆𝑝.𝛿(𝑝, (𝑎, 𝑤).𝛿(𝑤,
       1   2

               𝑤1 . let 𝑝1 = swap𝐴
                                 𝑊 (𝑎, 𝑤1 ) in 𝛿(𝑝1 , (𝑤1 , 𝑎).(𝜄1 𝑤1 , 𝑎)),
                                     1

               𝑤2 . let 𝑝2 = swap𝐴
                                 𝑊 (𝑎, 𝑤2 ) in 𝛿(𝑝2 , (𝑤2 , 𝑎).(𝜄2 𝑤2 , 𝑎))))
                                     2




                                                 32
swap𝐴
    𝑊 ⊗𝑊 ≝ 𝜆𝑝.𝛿(𝑝, (𝑎, 𝑤).𝛿(𝑤, (𝑤1 , 𝑤2 ).
        1    2
                                𝐴⊗𝑊1
                 let 𝑝1 = swap𝑊        ((𝑎, 𝑤1 ), 𝑤2 ) in 𝛿(𝑝1 , (𝑤2 , 𝑝).𝛿(𝑝, (𝑎, 𝑤1 ).
                                  2
                                𝑊 ⊗𝐴
                 let 𝑝2 = swap𝑊2       ((𝑤2 , 𝑎), 𝑤1 ) in 𝛿(𝑝2 , (𝑤1 , 𝑝).𝛿(𝑝, (𝑤2 , 𝑎).((𝑤1 , 𝑤2 ), 𝑎)))))))
                                  1


      We define similarly the expressions swap′𝐴
                                              𝑊
                                                 ∶ 𝐴 ⊗ 𝑊 ⟜ 𝑊 ⊗ 𝐴:

      swap′𝐴
          𝐼 ≝ 𝜆𝑝.𝛿(𝑝, (𝑖, 𝑎).𝛿(𝑖, ().(𝑎, ⋆)))


swap′𝐴
    𝑊 ⊕𝑊 ≝ 𝜆𝑝.𝛿(𝑝, (𝑤, 𝑎).𝛿(𝑤,
        1    2

                 𝑤1 . let 𝑝1 = swap′𝐴
                                   𝑊 (𝑤1 , 𝑎) in 𝛿(𝑝1 , (𝑎, 𝑤1 ).(𝑎, 𝜄1 𝑤1 )),
                                       1

                 𝑤2 . let 𝑝2 = swap′𝐴
                                   𝑊 (𝑤2 , 𝑎) in 𝛿(𝑝2 , (𝑎, 𝑤2 ).(𝑎, 𝜄2 𝑤2 ))))
                                       2



swap′𝐴
    𝑊 ⊗𝑊 ≝ 𝜆𝑝.𝛿(𝑝, (𝑤, 𝑎).𝛿(𝑤, (𝑤1 , 𝑤2 ).
        1    2
                                ′𝐴⊗𝑊1
                 let 𝑝1 = swap𝑊            (𝑤1 , (𝑤2 , 𝑎)) in 𝛿(𝑝1 , (𝑝, 𝑤1 ).𝛿(𝑝, (𝑤2 , 𝑎).
                                  2
                                ′𝑊 ⊗𝐴
                 let 𝑝2 = swap𝑊 2          (𝑤2 , (𝑎, 𝑤1 )) in 𝛿(𝑝2 , (𝑝, 𝑤2 ).𝛿(𝑝, (𝑎, 𝑤1 ).(𝑎, (𝑤1 , 𝑤2 ))))))))
                                  1

    Those terms are well-typed: variables are used exactly once and in order. Intro and
elimination rules for positive types do not have ordering constraints. Those from function
application and let bindings are respected: swap arguments use right-most variables.
Informally, those terms implement the following operations on stacks, with permutations
restricted to the two right-most types:
  ∙ swap𝐴
        𝐼
          ≝ 𝐴𝐼 → 𝐴 → 𝐼𝐴.
        𝐴
  ∙ swap𝑊 ⊕𝑊 ≝ 𝐴(𝑊1 ⊕ 𝑊2 ) → 𝐴𝑊𝑖 → 𝑊𝑖 𝐴 → (𝑊1 ⊕ 𝑊2 )𝐴.
             1      2
  ∙ swap𝐴𝑊1 𝑊2
               ≝ 𝐴(𝑊1 𝑊2 ) → (𝐴𝑊1 )𝑊2 → 𝑊2 (𝐴𝑊1 ) → (𝑊2 𝐴)𝑊1 → 𝑊1 (𝑊2 𝐴) →
    (𝑊1 𝑊2 )𝐴.
  ∙ swap𝐼𝐴 ≝ 𝐼𝐴 → 𝐴 → 𝐴𝐼.
            𝑊 ⊕𝑊2
  ∙ swap𝐴 1     ≝ (𝑊1 ⊕ 𝑊2 )𝐴 → 𝑊𝑖 𝐴 → 𝐴𝑊𝑖 → 𝐴(𝑊1 ⊕ 𝑊2 ).
        𝑊1 𝑊2
  ∙ swap𝐴      ≝ (𝑊1 𝑊2 )𝐴 → 𝑊1 (𝑊2 𝐴) → (𝑊2 𝐴)𝑊1 → 𝑊2 (𝐴𝑊1 ) → (𝐴𝑊1 )𝑊2 →
    𝐴(𝑊1 𝑊2 ).

B.2     Proof of determinism (proposition 2)
This is shown by case analysis, first on the command polarity:
    For negative commands, all expressions are mutually exclusive except the two “𝐧𝐞𝐰”
cases, for which the lists are mutually exclusive (empty or not).
    For positive commands, all expressions are mutually exclusive once we analyse 𝑣
in ⟨𝑣 ∣ (𝑥+ .𝑡) · 𝑠 ∣ 𝑙⟩+ ⇝ ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩+ : either the value is a variable or positive, in
which case no other rules apply, or the value is negative and may reduce only in negative
commands.


                                                       33
B.3     Proof of subject reduction (theorem 4)

Show that ∀𝑐1 ∶ 𝐴, ∀𝑐2, 𝑐1 ⇝ 𝑐1 ⇒ 𝑐2 ∶ 𝐴 by case analysis on the reduction step:

  ∙ ⟨(let 𝑥+ = 𝑡 in 𝑢)𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑡 ∣ (𝑥+ .𝑢)𝜀 · 𝑠 ∣ 𝑙⟩+ : by the hypothesis ⟨(let 𝑥+ =
    𝑡 in 𝑢)𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ∶ 𝐴, we get ⊢𝑝 𝑡 ∶ 𝐵+ , 𝑥 ∶ 𝐵 ⊢𝑝 𝑢 ∶ 𝐶𝜀 and 𝑠 ∶ 𝐶 ⊢𝑝 𝐴. Hence,
    we have (𝑥+ .𝑢)𝜀 · 𝑠 ∶ 𝐵 ⊢𝑝 𝐴 and so ⟨𝑡 ∣ (𝑥+ .𝑢)𝜀 · 𝑠 ∣ 𝑙⟩+ ∶ 𝐴.
  ∙ ⟨(let 𝑥− = 𝑣 in 𝑡)𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩𝜀 : by hypothesis, we get ⊢𝑝 𝑣 ∶
    𝐵− , 𝑥 ∶ 𝐵 ⊢𝑝 𝑡 ∶ 𝐶𝜀 and 𝑠 ∶ 𝐶 ⊢𝑝 𝐴. By SL, we have ⊢𝑝 𝑡[𝑣∕𝑥] ∶ 𝐶 and so
    ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩𝜀 ∶ 𝐴.
  ∙ ⟨(𝑣𝑤)𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑣 ∣ 𝑤𝜀 · 𝑠 ∣ 𝑙⟩− : by hypothesis, we get ⊢𝑝 𝑣 ∶ 𝐶𝜀 ⟜ 𝐵, ⊢𝑝 𝑤 ∶ 𝐵
    and 𝑠 ∶ 𝐶 ⊢𝑝 𝐴. Hence, we have 𝑤𝜀 · 𝑠 ∶ 𝐶 ⟜ 𝐵 ⊢𝑝 𝐴 and so ⟨𝑣 ∣ 𝑤𝜀 · 𝑠 ∣ 𝑙⟩− ∶ 𝐴.
  ∙ ⟨(𝜋𝑖 𝑣)𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑣 ∣ 𝜋𝑖𝜀 · 𝑠 ∣ 𝑙⟩− : by hypothesis, we get ⊢𝑝 𝑣 ∶ 𝐵1 & 𝐵2 and
    𝑠 ∶ 𝐵𝑖𝜀 ⊢𝑝 𝐴. Hence, we have 𝜋𝑖𝜀 · 𝑠 ∶ 𝐵1 & 𝐵2 ⊢𝑝 𝐴 and so ⟨𝑣 ∣ 𝜋𝑖𝜀 · 𝑠 ∣ 𝑙⟩− ∶ 𝐴.
  ∙ ⟨𝑣 ∣ (𝑥+ .𝑡)𝜀 · 𝑠 ∣ 𝑙⟩+ ⇝ ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩𝜀 : by hypothesis, we get ⊢𝑝 𝑣 ∶ 𝐵+ , 𝑥 ∶ 𝐵 ⊢𝑝
    𝑡 ∶ 𝐶 and 𝑠 ∶ 𝐶 ⊢𝑝 𝐴. By SL, we have ⊢𝑝 𝑡[𝑣∕𝑥] ∶ 𝐶 and so ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩𝜀 ∶ 𝐴.
  ∙ ⟨𝜆𝑥.𝑡 ∣ 𝑣𝜀 · 𝑠 ∣ 𝑙⟩− ⇝ ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩𝜀 : by hypothesis, we get 𝑥 ∶ 𝐵 ⊢𝑝 𝑡 ∶ 𝐶𝜀 , ⊢𝑝
    𝑣 ∶ 𝐵 and 𝑠 ∶ 𝐶 ⊢𝑝 𝐴. By SL, we have ⊢𝑝 𝑡[𝑣∕𝑥] ∶ 𝐶 and so ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩𝜀 ∶ 𝐴.
  ∙ ⟨⟨𝑡1 , 𝑡2 ⟩ ∣ 𝜋𝑖𝜀 · 𝑠 ∣ 𝑙⟩− ⇝ ⟨𝑡𝑖 ∣ 𝑠 ∣ 𝑙⟩𝜀 : by hypothesis, we get ⊢𝑝 𝑡1 ∶ 𝐵1 , ⊢𝑝 𝑡2 ∶ 𝐵2
    and 𝑠 ∶ 𝐵𝑖𝜀 ⊢𝑝 𝐴. Hence, we have ⟨𝑡𝑖 ∣ 𝑠 ∣ 𝑙⟩𝜀 ∶ 𝐴.
  ∙ ⟨𝛿((𝑣, 𝑤), (𝑥, 𝑦).𝑡)𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑡[𝑣∕𝑥, 𝑤∕𝑦] ∣ 𝑠 ∣ 𝑙⟩𝜀 : by hypothesis, we get
    ⊢𝑝 𝑣 ∶ 𝐵, ⊢𝑝 𝑤 ∶ 𝐶, 𝑥 ∶ 𝐵, 𝑦 ∶ 𝐶 ⊢𝑝 𝑡 ∶ 𝐷𝜀 and 𝑠 ∶ 𝐷 ⊢𝑝 𝐴. By SL, we have
    ⊢𝑝 (𝑡[𝑣∕𝑥])[𝑤∕𝑦] ∶ 𝐷. Because 𝑥 nor 𝑦 do not occur free in 𝑣 nor 𝑤, we have
    (𝑡[𝑣∕𝑥])[𝑤∕𝑦] = 𝑡[𝑣∕𝑥, 𝑤∕𝑦] and so ⟨𝑡[𝑣∕𝑥, 𝑤∕𝑦] ∣ 𝑠 ∣ 𝑙⟩𝜀 ∶ 𝐴.
  ∙ ⟨𝛿((), ().𝑡)𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑡 ∣ 𝑠 ∣ 𝑙⟩𝜀 : by hypothesis, we get ⊢𝑝 𝑡 ∶ 𝐵𝜀 and 𝑠 ∶ 𝐵 ⊢𝑝 𝐴,
    hence we have ⟨𝑡 ∣ 𝑠 ∣ 𝑙⟩𝜀 ∶ 𝐴.
  ∙ ⟨𝛿(𝜄𝑖 𝑣, 𝑥1 .𝑡1 , 𝑥2 .𝑡2 )𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑡𝑖 [𝑣∕𝑥𝑖 ] ∣ 𝑠 ∣ 𝑙⟩𝜀 : by hypothesis, we get ⊢𝑝 𝑣 ∶
    𝐵𝑖 , 𝑥1 ∶ 𝐵1 ⊢𝑝 𝑡1 ∶ 𝐶𝜀 , 𝑥2 ∶ 𝐵2 ⊢𝑝 𝑡2 ∶ 𝐶 and 𝑠 ∶ 𝐶 ⊢𝑝 𝐴. By SL, we have
    ⊢𝑝 𝑡𝑖 [𝑣∕𝑥𝑖 ] ∶ 𝐶 and so ⟨𝑡𝑖 [𝑣∕𝑥𝑖 ] ∣ 𝑠 ∣ 𝑙⟩𝜀 ∶ 𝐴.
  ∙ ⟨𝐧𝐞𝐰 ∣ () · 𝑠 ∣ 𝑟𝑛 ∶∶ 𝑙⟩− ⇝ ⟨𝜄1 𝑟𝑛 ∣ 𝑠 ∣ 𝑙⟩+ : by hypothesis, we have 𝑠 ∶ 𝑅 ⊕ 1 ⊢𝑝 𝐴.
    We always have ⊢𝑝 𝜄1 𝑟𝑛 ∶ 𝑅 ⊕ 1, and so ⟨𝜄1 𝑟𝑛 ∣ 𝑠 ∣ 𝑙⟩+ ∶ 𝐴.
  ∙ ⟨𝐧𝐞𝐰 ∣ () · 𝑠 ∣ Nil⟩− ⇝ ⟨𝜄2 () ∣ 𝑠 ∣ Nil⟩+ : by hypothesis, we have 𝑠 ∶ 𝑅 ⊕ 1 ⊢𝑝 𝐴.
    We always have ⊢𝑝 𝜄2 () ∶ 𝑅 ⊕ 1, and so ⟨𝜄1 𝑟𝑛 ∣ 𝑠 ∣ 𝑙⟩+ ∶ 𝐴.
  ∙ ⟨𝐝𝐞𝐥𝐞𝐭𝐞 ∣ 𝑟𝑛 · 𝑠 ∣ 𝑙⟩− ⇝ ⟨() ∣ 𝑠 ∣ 𝑟𝑛 ∶∶ 𝑙⟩+ : by hypothesis, we have 𝑠 ∶ 1 ⊢ 𝐴. We
    always have ⊢𝑝 () ∶ 1 and so ⟨() ∣ 𝑠 ∣ 𝑟𝑛 ∶∶ 𝑙⟩+ .

      The same proof goes through if we consider ⊢𝑝 without structural rules.


B.4     Proof of progress (theorem 5)

Show that any well-typed command ⟨𝑡 ∣ 𝑠 ∣ 𝑙⟩𝜀 ∶ 𝐴 reduces iff it is not of the shape
⟨𝑣𝑡 ∣ ⋆ ∣ 𝑙⟩𝜀 by case analysis on the judgement ⊢𝑝 𝑡 ∶ 𝐵𝜀 :
If 𝑡 is a final value, we do a case analysis on the judgement 𝑠 ∶ 𝐵 ⊢𝑝 𝐴: if 𝑠 = ⋆, the
context is of the shape ⟨𝑣𝑡 ∣ ⋆ ∣ 𝑙⟩𝜀 and matches no reduction steps. Otherwise, the stack
shape is determined by the type of 𝑡:

  ∙ If 𝜛(𝐵) = +, then 𝑠 = (𝑥+ .𝑢)𝜀 · 𝑠′ and ⟨𝑣𝑡 ∣ (𝑥+ .𝑢)𝜀 · 𝑠′ ∣ 𝑙⟩+ ⇝ ⟨𝑢[𝑣𝑡 ∕𝑥] ∣ 𝑠′ ∣ 𝑙⟩𝜀 .


                                              34
  ∙ If 𝑡 = ⟨𝑡1 , 𝑡2 ⟩, then 𝑠 = 𝜋𝑖𝜀 · 𝑠′ and ⟨⟨𝑡1 , 𝑡2 ⟩ ∣ 𝜋𝑖𝜀 · 𝑠′ ∣ 𝑙⟩− ⇝ ⟨𝑡𝑖 ∣ 𝑠′ ∣ 𝑙⟩𝜀 .
  ∙ If 𝑡 = 𝜆𝑥.𝑡′ , then 𝑠 = 𝑣𝜀 · 𝑠′ and ⟨𝜆𝑥.𝑡′ ∣ 𝑣𝜀 · 𝑠′ ∣ 𝑙⟩− ⇝ ⟨𝑡[𝑣∕𝑥] ∣ 𝑠′ ∣ 𝑙⟩𝜀 .
  ∙ If 𝑡 = 𝐧𝐞𝐰 and 𝑙 = 𝑟𝑛 ∶∶ 𝑙′ , then 𝑠 = () · 𝑠′ and ⟨𝐧𝐞𝐰 ∣ () · 𝑠′ ∣ 𝑟𝑛 ∶∶ 𝑙′ ⟩− ⇝ ⟨𝜄1 𝑟𝑛 ∣
    𝑠′ ∣ 𝑙′ ⟩+ .
  ∙ If 𝑡 = 𝐧𝐞𝐰 and 𝑙 = ⋆, then 𝑠 = () · 𝑠′ and ⟨𝐧𝐞𝐰 ∣ () · 𝑠′ ∣ ⋆⟩− ⇝ ⟨𝜄2 () ∣ 𝑠′ ∣ ⋆⟩+ .
  ∙ If 𝑡 = 𝐝𝐞𝐥𝐞𝐭𝐞 so 𝑠 = 𝑟𝑛 · 𝑠′ and ⟨𝐝𝐞𝐥𝐞𝐭𝐞 ∣ 𝑟𝑛 · 𝑠′ ∣ 𝑙⟩− ⇝ ⟨() ∣ 𝑠′ ∣ 𝑟𝑛 ∶∶ 𝑙⟩+ .

Otherwise:

  ∙ If 𝑡 = 𝛿((𝑣, 𝑤), (𝑥, 𝑦).𝑡′ )𝜀 , then ⟨𝛿((𝑣, 𝑤), (𝑥, 𝑦).𝑡′ )𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑡′ [𝑣∕𝑥, 𝑤∕𝑦] ∣ 𝑠 ∣
    𝑙⟩𝜀 .
  ∙ If 𝑡 = 𝛿((), ().𝑡′ )𝜀 , then ⟨𝛿((), ().𝑡′ )𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑡′ ∣ 𝑠 ∣ 𝑙⟩𝜀 .
  ∙ If 𝑡 = 𝛿(𝜄𝑖 𝑣, 𝑥1 .𝑡1 , 𝑥2 .𝑡2 )𝜀 , then ⟨𝛿(𝜄𝑖 𝑣, 𝑥1 .𝑡1 , 𝑥2 .𝑡2 )𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑡𝑖 [𝑥𝑖 ∕𝑣] ∣ 𝑠 ∣ 𝑙⟩𝜀 .
  ∙ If 𝑡 = (let 𝑥− = 𝑣 in 𝑡′ )𝜀 , then ⟨(let 𝑥− = 𝑣 in 𝑡′ )𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑡′ [𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩𝜀 .
  ∙ If 𝑡 = (let 𝑥+ = 𝑡′ in 𝑢)𝜀 , then ⟨(let 𝑥+ = 𝑡′ in 𝑢)𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑡′ ∣ (𝑥+ .𝑢)𝜀 · 𝑠 ∣ 𝑙⟩+ .
  ∙ If 𝑡 = (𝑣𝑤)𝜀 , then ⟨(𝑣𝑤)𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑣 ∣ 𝑤𝜀 · 𝑠 ∣ 𝑙⟩− .
  ∙ If 𝑡 = (𝜋𝑖 𝑣)𝜀 , then ⟨(𝜋𝑖 𝑣)𝜀 ∣ 𝑠 ∣ 𝑙⟩𝜀 ⇝ ⟨𝑣 ∣ 𝜋𝑖𝜀 · 𝑠 ∣ 𝑙⟩− .

      The same proof goes through if we consider ⊢𝑝 without structural rules.


C      Details: resource-safety properties

C.1     Proof that ⊢ implies resource-free ⊢𝒐 (lemma 7)

Proof. By induction on the derivation of 𝑡, we apply the corresponding rule in ⊢𝑜 :
contexts of premises are always well-formed due to the absence of resources. Rules to
shift between the contexts Γ, 𝑥; []; Δ and Γ; []; 𝑥, Δ are used as needed, in particular at
the end to obtain Γ; ; ⊢ 𝑡.


C.2 Proof of left and right substitution lemmas for ordered expressions (lemma 8)

Show that (Left SL) if ; 𝐿𝑡 ; ⊢𝑜 𝑡 and Γ, 𝑥; 𝐿𝑢 ; Δ ⊢𝑜 𝑢, then Γ; 𝐿𝑡 ++ 𝐿𝑢 ; Δ ⊢𝑜 𝑢[𝑡∕𝑥].
Moreover (Right SL), if ; 𝐿𝑡 ; ⊢𝑜 𝑡 and Γ; 𝐿𝑢 ; 𝑥, Δ ⊢𝑜 𝑢, then Γ; 𝐿𝑢 ++ 𝐿𝑡 ; Δ ⊢𝑜 𝑢[𝑡∕𝑥].
We first prove by induction that if a variable 𝑥 does not occur in an expression 𝑢, then
𝑢[𝑡∕𝑥] = 𝑢. Then, each SL is proven by induction on 𝑢:

  ∙ (), 𝐧𝐞𝐰, 𝐝𝐞𝐥𝐞𝐭𝐞, 𝑟𝑛 : both SL by absurdity from the induction hypothesis (IH): no
    variables in the context.
  ∙ 𝑥 ⊢𝑜 𝑥: for both SL, we have ; 𝐿𝑡 ; ⊢𝑜 𝑡 and 𝑥[𝑡∕𝑥] = 𝑡 so we have ; 𝐿𝑡 ; ⊢𝑜 𝑥[𝑡∕𝑥].
  ∙ 𝜄𝑖 𝑣: for left SL, by IH we have Γ; 𝐿𝑡 ++ 𝐿𝑢 ; Δ ⊢𝑜 𝑣[𝑡∕𝑥]. Because (𝜄𝑖 𝑣)[𝑡∕𝑥] =
    𝜄𝑖 (𝑣[𝑡∕𝑥]), we have Γ; 𝐿𝑡 ++ 𝐿𝑢 ; Δ ⊢𝑜 (𝜄𝑖 𝑣)[𝑡∕𝑥]. The right SL is done similarly,
    swapping 𝐿𝑡 and 𝐿𝑢 : by IH we have Γ; 𝐿𝑢 ++ 𝐿𝑡 ; Δ ⊢𝑜 𝑣[𝑡∕𝑥]. Because (𝜄𝑖 𝑣)[𝑡∕𝑥] =
    𝜄𝑖 (𝑣[𝑡∕𝑥]), we have Γ; 𝐿𝑢 ++ 𝐿𝑡 ; Δ ⊢𝑜 (𝜄𝑖 𝑣)[𝑡∕𝑥].
  ∙ 𝜋𝑖 𝑣: similarly, because (𝜋𝑖 𝑣)[𝑡∕𝑥] = 𝜋𝑖 (𝑣[𝑡∕𝑥]) both SL hold by IH.
  ∙ ⟨𝑢1 , 𝑢2 ⟩: because ⟨𝑢1 , 𝑢2 ⟩[𝑡∕𝑥] = ⟨𝑢1 [𝑡∕𝑥], 𝑢2 [𝑡∕𝑥]⟩, both SL hold by IH.
  ∙ 𝜆𝑦.𝑢1 : because 𝜆𝑦.(𝑢1 [𝑡∕𝑥]) = (𝜆𝑦.𝑢1 )[𝑡∕𝑥], both SL hold by IH.


                                                    35
 ∙ (𝑣, 𝑤): for both SL, given Θ ⊢𝑜 𝑣 and Θ′ ⊢𝑜 𝑤, by case analysis on the three cases
   in which Θ @ Θ′ is well-formed. In the left SL case:
     ∙ Θ = Γ𝑣 ; ; and Θ′ = Γ1𝑤 , 𝑥; 𝐿𝑢 ; Γ2𝑤 : 𝑥 does not occur in 𝑣 so (𝑣, 𝑤)[𝑡∕𝑥] =
        (𝑣, 𝑤[𝑡∕𝑥]) and by IH on 𝑤 we have Γ1𝑤 , 𝑥; 𝐿𝑢 ; Γ2𝑤 ⊢𝑜 𝑤[𝑡∕𝑥], hence we have
        Γ𝑣 , Γ1𝑤 ; 𝐿𝑡 ++ 𝐿𝑢 ; Γ2𝑤 ⊢𝑜 (𝑣, 𝑤)[𝑡∕𝑥].
     ∙ Θ = Γ1𝑣 , 𝑥; 𝐿𝑢 ; Γ2𝑣 and Θ′ = Γ𝑤 ; ;: (𝑣, 𝑤)[𝑡∕𝑥] = (𝑣[𝑡∕𝑥], 𝑤) so the SL holds by
        IH on Θ ⊢𝑜 𝑣.
     ∙ Θ = Γ𝑣 , 𝑥; 𝐿1𝑢 ; and Θ′ =; 𝐿2𝑢 ; Γ𝑤 : (𝑣, 𝑤)[𝑡∕𝑥] = (𝑣[𝑡∕𝑥], 𝑤) so the SL holds by
        IH on 𝑣.
   The right SL is done similarly, swapping 𝑥 and 𝐿𝑢 :
     ∙ Θ =; ; Γ𝑣 and Θ′ = Γ1𝑤 ; 𝐿𝑢 ; 𝑥, Γ2𝑤 : (𝑣, 𝑤)[𝑡∕𝑥] = (𝑣, 𝑤[𝑡∕𝑥]) so the SL holds by
        IH on 𝑤.
     ∙ Θ = Γ1𝑣 ; 𝐿𝑢 ; 𝑥, Γ2𝑣 and Θ′ = Γ𝑤 : (𝑣, 𝑤)[𝑡∕𝑥] = (𝑣[𝑡∕𝑥], 𝑤) so the SL holds by
        IH on 𝑣.
     ∙ Θ = Γ𝑣 ; 𝐿1𝑢 ; and Θ′ =; 𝐿2𝑢 ; 𝑥, Γ𝑤 : (𝑣, 𝑤)[𝑡∕𝑥] = (𝑣, 𝑤[𝑡∕𝑥]) so the SL holds by
        IH on 𝑤.
 ∙ let 𝑦 = 𝑢1 in 𝑢2 : similarly, for both SL we proceed by case analysis on Θ @ Θ′ . For
   the left SL:
     ∙ Θ =; ; Γ𝑢2 , 𝑦 and Θ′ = Γ1𝑢1 , 𝑥, ; 𝐿𝑢 ; Γ2𝑢1 : (let 𝑦 = 𝑢1 in 𝑢2 )[𝑡∕𝑥] = (let 𝑦 =
        𝑢1 in 𝑢2 [𝑡∕𝑥]) so the SL holds by IH on 𝑢2 .
     ∙ Θ = Γ1𝑢2 , 𝑥; 𝐿𝑢 ; Γ2𝑢2 , 𝑦 and Θ′ =; ; Γ𝑤 : (let 𝑦 = 𝑢1 in 𝑢2 )[𝑡∕𝑥] = (let 𝑦 = 𝑢1 [𝑡∕𝑥] in 𝑢2 )
        so the SL holds by IH on 𝑢1 .
     ∙ Θ = Γ𝑢2 ; 𝐿1𝑢 ; 𝑦 and Θ′ =; 𝐿2𝑢 ; 𝑥, Γ𝑢1 : the concatenation is not well-formed due
        to 𝑦 so the SL holds by absurdity.
   The right SL is done similarly by swapping 𝑥 and 𝐿𝑢 .
 ∙ (𝑣, 𝑦.𝑢1 , 𝑧.𝑢2 ): For both SL we proceed by case analysis on Θ @ Θ′ @ Θ′′ , here for
   left SL:
     ∙ Θ = Γ1𝑢 , 𝑥; 𝐿𝑢 ; Γ2𝑢 , Θ′ =; ; Γ𝑣 , Θ′′ =; ; Γ3𝑢 : (𝑣, 𝑦.𝑢1 , 𝑧.𝑢2 )[𝑡∕𝑥] = (𝑣, 𝑦.𝑢1 [𝑡∕𝑥], 𝑧.𝑢2 [𝑡∕𝑥])
        so the SL holds by IH on Γ1𝑢 , 𝑥; 𝐿𝑢 ; Γ2𝑢 , 𝑦, Γ3𝑢 ⊢𝑜 𝑢1 and Γ1𝑢 , 𝑥; 𝐿𝑢 ; Γ2𝑢 , 𝑦, Γ3𝑢 ⊢𝑜 𝑢2 .
     ∙ Θ = Γ1𝑢 , 𝑥; 𝐿1𝑢 , Θ′ =; 𝐿2𝑢 ; Γ𝑣 , Θ′′ =; ; Γ2𝑢 : the SL holds by IH on 𝑢1 and 𝑢2 .
     ∙ Θ =; ; Γ1𝑢 , Θ′ = Γ1𝑣 , 𝑥; 𝐿𝑢 ; Γ2𝑣 , Θ′′ =; ; Γ2𝑢 : the SL holds by IH on 𝑣.
     ∙ Θ =; ; Γ1𝑢 , Θ′ = Γ1𝑣 , 𝑥; 𝐿1𝑢 ; Θ′′ =; 𝐿2𝑢 ; Γ2𝑢 : the SL holds by IH on 𝑣.
     ∙ Θ =; ; Γ1𝑢 , Θ′ =; ; Γ𝑣 , Θ′′ = Γ2𝑢 , 𝑥; 𝐿𝑢 ; Γ3𝑢 : the SL holds by IH on 𝑢1 and 𝑢2 .
     ∙ The other cases yield ill-formed concatenated context.
   The right SL is done similarly by swapping 𝑥 and 𝐿𝑢 .
 ∙ 𝛿(𝑣, (𝑦, 𝑧).𝑢1 ): similarly, by case analysis on Θ @ Θ′ @ Θ′′ .
 ∙ 𝛿(𝑣, ().𝑡): by case analysis on Θ @ Θ′ .
 ∙ 𝑣𝑤: by case analysis on Θ @ Θ′ .


C.3   Proof of ordered predicate invariant by reduction (theorem 9)

Show that ∀𝑐1, ∀𝑐2, ∀𝐿, 𝐿 ⊢𝐶                   𝐶
                           𝑜 𝑐1 ∧ 𝑐1 ⇝ 𝑐2 ⇒ 𝐿 ⊢𝑜 𝑐2 by case analysis on reduction
steps:


                                                36
  ∙ ⟨let 𝑥+ = 𝑡 in 𝑢 ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡 ∣ (𝑥+ .𝑢) · 𝑠 ∣ 𝑙⟩: by definition of 𝐿 ⊢𝐶           𝑜 𝑐1, we get
    ; 𝐿𝑡 ; ⊢𝑜 𝑡, ; 𝐿𝑢 ; 𝑥 ⊢𝑜 𝑢 and 𝐿𝑠 ⊢𝑆𝑜 𝑠 with 𝐿 = 𝐿𝑠 ++ 𝐿𝑢 ++ 𝐿𝑡 ++ 𝑙, hence we have
    ; 𝐿𝑠 ++ 𝐿𝑢 ; ⊢𝑜 (𝑥+ .𝑢) · 𝑠 and so 𝐿𝑠 ++ 𝐿𝑢 ++ 𝐿𝑡 ++ 𝑙 = 𝐿 ⊢𝐶          𝑜 𝑐2.
  ∙ ⟨let 𝑥− = 𝑡 in 𝑢 ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑢[𝑡∕𝑥] ∣ 𝑠 ∣ 𝑙⟩: by definition, we get ; 𝐿𝑡 ; ⊢𝑜 𝑡, ; 𝐿𝑢 ; 𝑥 ⊢𝑜 𝑢
    and 𝐿𝑠 ⊢𝑆𝑜 𝑠 hence by right SL we have ; 𝐿𝑢 ++ 𝐿𝑡 ; ⊢𝑜 𝑢[𝑡∕𝑥] and so 𝐿 ⊢𝐶              𝑜 𝑐2.
  ∙ ⟨𝑣𝑤 ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑣 ∣ 𝑤 · 𝑠 ∣ 𝑙⟩: by definition, we get ; 𝐿𝑤 ; ⊢𝑜 𝑤, ; 𝐿𝑣 ; ⊢𝑜 𝑣 and
    𝐿𝑠 ⊢𝑆𝑜 𝑠, hence we have 𝐿𝑠 ++ 𝐿𝑤 ⊢𝑆𝑜 𝑤 · 𝑠 and so 𝐿 ⊢𝐶              𝑜 𝑐2.
  ∙ ⟨𝜋𝑖 𝑡 ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡 ∣ 𝜋𝑖 · 𝑠 ∣ 𝑙⟩: by definition, we get ; 𝐿𝑡 ; ⊢𝑜 𝑡 and 𝐿𝑠 ⊢𝑆𝑜 𝑠, hence we
    have 𝐿 ⊢𝐶    𝑜 𝑐2.
  ∙ ⟨𝑣 ∣ (𝑥.𝑡) · 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩: by definition, we get ; 𝐿𝑣 ; ⊢𝑜 𝑣, ; 𝐿𝑡 ; 𝑥 ⊢𝑜 𝑡 and
    𝐿𝑠 ⊢𝑆𝑜 𝑠, hence by right SL we have ; 𝐿𝑡 ++ 𝐿𝑣 ; ⊢𝑜 𝑡[𝑣∕𝑥] and so 𝐿 ⊢𝐶              𝑜 𝑐2.
  ∙ ⟨𝜆𝑥.𝑡 ∣ 𝑣 · 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩: by definition, we get 𝐿𝑣 ⊢𝑜 𝑣, 𝑥, 𝐿𝑡 ⊢𝑜 𝑡 and
    𝐿𝑠 ⊢𝑆𝑜 𝑠, hence by left SL we have 𝐿𝑣 , 𝐿𝑡 ⊢𝑜 𝑡[𝑣∕𝑥] and so 𝐿 ⊢𝐶             𝑜 𝑐2.
  ∙ ⟨⟨𝑡1 , 𝑡2 ⟩ ∣ 𝜋𝑖 · 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡𝑖 ∣ 𝑠 ∣ 𝑙⟩: by definition, we get 𝐿𝑡 ⊢𝑜 𝑡1 , 𝐿𝑡 ⊢𝑜 𝑡2 and
    𝐿𝑠 ⊢𝑆𝑜 𝑠, hence we have 𝐿 ⊢𝐶         𝑜 𝑐2.
  ∙ ⟨𝛿((𝑣, 𝑤), (𝑥, 𝑦).𝑡) ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡[𝑣∕𝑥, 𝑤∕𝑦] ∣ 𝑠 ∣ 𝑙⟩: by definition and case analysis
    on composition of contexts, we get ; 𝐿𝑣 ; ⊢𝑜 𝑣, ; 𝐿𝑤 ; ⊢𝑜 𝑤, Θ ⊢𝑜 𝑡 and 𝐿𝑠 ⊢𝑆𝑜 𝑠
    with Θ = either ; 𝐿𝑡 ; 𝑥, 𝑦 or 𝑥, 𝑦; 𝐿𝑡 ;. In the first case, by right SL twice we have
    ; 𝐿𝑡 ++ 𝐿𝑣 ++ 𝐿𝑤 ; ⊢𝑜 𝑡[𝑣∕𝑥, 𝑤∕𝑦] and so 𝐿 ⊢𝐶            𝑜 𝑐2. Similarly, in the second case by
    left SL twice we have ; 𝐿𝑣 ++ 𝐿𝑤 ++ 𝐿𝑡 ; ⊢𝑜 𝑡[𝑣∕𝑥, 𝑤∕𝑦] and so 𝐿 ⊢𝐶              𝑜 𝑐2.
  ∙ ⟨𝛿((), ().𝑡) ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡 ∣ 𝑠 ∣ 𝑙⟩: by definition, we get ; []; ⊢𝑜 (), ; 𝐿𝑡 ; ⊢𝑜 𝑡 and
    𝐿𝑠 ⊢𝑆𝑜 𝑠, hence we have 𝐿 ⊢𝐶         𝑜 𝑐2.
  ∙ ⟨𝛿(𝜄𝑖 𝑣, 𝑥1 .𝑡1 , 𝑥2 .𝑡2 ) ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡𝑖 [𝑥𝑖 ∕𝑣] ∣ 𝑠 ∣ 𝑙⟩: by definition and case analysis, we
    get ; 𝐿𝑣 ; ⊢𝑜 𝑣, Θ𝑖 ⊢ 𝑡𝑖 and 𝐿𝑠 ⊢𝑆𝑜 𝑠 with both Θ𝑖 = either ; 𝐿𝑡 ; 𝑥𝑖 or 𝑥𝑖 ; 𝐿𝑡 ;. In the
    first case, by right SL we have ; 𝐿𝑡 ++ 𝐿𝑣 ; ⊢𝑜 𝑡𝑖 [𝑣∕𝑥𝑖 ] and so 𝐿 ⊢𝐶        𝑜 𝑐2. Similarly, in
    the second case by left SL we have ; 𝐿𝑣 ++ 𝐿𝑡 ; ⊢𝑜 𝑡𝑖 [𝑣∕𝑥𝑖 ] and so 𝐿 ⊢𝐶           𝑜 𝑐2.
  ∙ ⟨𝐧𝐞𝐰 ∣ () · 𝑠 ∣ 𝑟𝑛 ∶∶ 𝑙⟩ ⇝ ⟨𝜄1 𝑟𝑛 ∣ 𝑠 ∣ 𝑙⟩: by definition, we get ; []; ⊢𝑜 (), ; [𝑟𝑛 ]; ⊢𝑜 𝑟𝑛
    and 𝐿𝑠 ⊢𝑆𝑜 𝑠, hence we have 𝐿𝑠 ++ 𝑟𝑛 ∶∶ 𝑙 = 𝐿 ⊢𝐶             𝑜 𝑐2.
  ∙ ⟨𝐧𝐞𝐰 ∣ () · 𝑠 ∣ Nil⟩ ⇝ ⟨𝜄2 () ∣ 𝑠 ∣ Nil⟩: by definition, we get 𝐿𝑠 = 𝐿 ⊢𝐶         𝑜 𝑐2.
  ∙ ⟨𝐝𝐞𝐥𝐞𝐭𝐞 ∣ 𝑟𝑛 · 𝑠 ∣ 𝑙⟩ ⇝ ⟨() ∣ 𝑠 ∣ 𝑟𝑛 ∶∶ 𝑙⟩: by definition, we get ; [𝑟𝑛 ]; ⊢𝑜 𝑟𝑛 , ; []; ⊢𝑜 ()
    and 𝐿𝑠 ⊢𝑆𝑜 𝑠, hence we have 𝐿𝑠 ++ 𝑟𝑛 ∶∶ 𝑙 = 𝐿 ⊢𝐶             𝑜 𝑐2.


C.4   Proof of (theorem 10) in the unordered case
We define the indexed predicate 𝑀; Γ ⊢𝑙 𝑡 by induction with 𝑀 the multiset of resources
and Γ the set of variables in 𝑡. Given a linear expression 𝑀; Γ ⊢𝑙 𝑡, we define its
multiset of resources 𝑀𝑅(𝑡) ≝ 𝑀. The concatenation of contexts is always defined:
Θ = (𝑀1 ; Γ1 ) @ Θ′ = (𝑀2 ; Γ2 ) ≝ 𝑀1 , 𝑀2 ; Γ1 , Γ2 .
   We can then prove the following substitution lemma:

Lemma 18. If Θ ⊢𝑙 𝑡 and Θ′ , 𝑥 ⊢𝑙 𝑢, then Θ @ Θ′ ⊢𝑙 𝑢[𝑡∕𝑥].

Proof. By induction on 𝑢:
  ∙ (), 𝐧𝐞𝐰, 𝐝𝐞𝐥𝐞𝐭𝐞, 𝑟𝑛 : by absurdity from the induction hypothesis (IH): no variables in
    the context.


                                                37
       []; 𝑥 ⊢𝑙 𝑥          []; ⊢𝑙 ()         []; ⊢𝑙 𝐧𝐞𝐰         []; ⊢𝑙 𝐝𝐞𝐥𝐞𝐭𝐞         [𝑟𝑛 ]; ⊢𝑙 𝑟𝑛
    Θ ⊢𝑙 𝑣           Θ ⊢𝑙 𝑣       Θ ⊢𝑙 𝑡      Θ ⊢𝑙 𝑢          Θ, 𝑥 ⊢𝑙 𝑡        Θ ⊢𝑙 𝑣    Θ ′ ⊢𝑙 𝑤
    Θ ⊢𝑙 𝜄𝑖 𝑣       Θ ⊢𝑙 𝜋𝑖 𝑣        Θ ⊢𝑙 ⟨𝑡, 𝑢⟩              Θ ⊢𝑙 𝜆𝑥.𝑡               ′
                                                                                Θ @ Θ ⊢𝑙 (𝑣, 𝑤)
      Θ, 𝑥 ⊢𝑙 𝑢     Θ ′ ⊢𝑙 𝑡              Θ, 𝑥, 𝑦 ⊢𝑙 𝑡   Θ ′ ⊢𝑙 𝑣             Θ ⊢𝑙 𝑡    Θ ′ ⊢𝑙 𝑣
            ′                                     ′                                  ′
      Θ @ Θ ⊢𝑙 let 𝑥 = 𝑡 in 𝑢             Θ @ Θ ⊢𝑙 𝛿(𝑣, (𝑥, 𝑦).𝑡)             Θ @ Θ ⊢𝑙 𝛿(𝑣, ().𝑡)
            Θ, 𝑥 ⊢𝑙 𝑡     Θ, 𝑦 ⊢𝑙 𝑢        Θ ′ ⊢𝑙 𝑣                    Θ ⊢𝑙 𝑤      Θ ′ ⊢𝑙 𝑣
                   Θ @ Θ′ ⊢𝑙 𝛿(𝑣, 𝑥.𝑡, 𝑦.𝑢)                               Θ @ Θ′ ⊢𝑙 𝑣𝑤

                        Fig. 7. Predicate of linear expressions with resources


                            𝑀𝑣 ; ⊢𝑙 𝑣         𝑀𝑠 ⊢𝑆𝑙 𝑠               𝑀𝑡 ; 𝑥 ⊢𝑙 𝑡   𝑀𝑠 ⊢𝑆𝑙 𝑠
          ⊢𝑆𝑙 ⋆
                                𝑀𝑠 ++ 𝑀𝑣 ⊢𝑆𝑙 𝑣 · 𝑠                              𝑆
                                                                      𝑀𝑠 ++ 𝑀𝑠 ⊢𝑙 (𝑥+ .𝑡) · 𝑠
                                         𝑀𝑡 ; ⊢𝑙 𝑡        𝑀𝑠 ⊢𝑆𝑙 𝑠
                                       𝑀𝑡 ++ 𝑀𝑠 ++ 𝑙 ⊢𝐶𝑙 ⟨𝑡 ∣ 𝑠 ∣ 𝑙⟩

                        Fig. 8. Typing rules of ordered stacks and commands


  ∙ ; 𝑥; ⊢𝑙 𝑥: we have Θ ⊢𝑙 𝑡 and 𝑥[𝑡∕𝑥] = 𝑡, hence Θ ⊢𝑙 𝑥[𝑡∕𝑥].
  ∙ 𝜄𝑖 𝑣: by IH we get Θ ⊢𝑙 𝑣[𝑡∕𝑥] and (𝜄𝑖 𝑣)[𝑡∕𝑥] = 𝜄𝑖 (𝑣[𝑡∕𝑥]), hence Θ ⊢𝑙 (𝜄𝑖 𝑣)[𝑡∕𝑥].
  ∙ 𝜋𝑖 𝑣: similarly, because (𝜋𝑖 𝑣)[𝑡∕𝑥] = 𝜋𝑖 (𝑣[𝑡∕𝑥]) the SL holds by IH.
  ∙ ⟨𝑢1 , 𝑢2 ⟩: because ⟨𝑢1 , 𝑢2 ⟩[𝑡∕𝑥] = ⟨𝑢1 [𝑡∕𝑥], 𝑢2 [𝑡∕𝑥]⟩, the SL hold by IH.
  ∙ 𝜆𝑦.𝑢1 : because 𝜆𝑦.(𝑢1 [𝑡∕𝑥]) = (𝜆𝑦.𝑢1 )[𝑡∕𝑥], both SL hold by IH.
  ∙ (𝑣, 𝑤): by case analysis to split the context Θ @ Θ′ , whether 𝑥 is in 𝑣 or 𝑤:
        ∙ Θ = 𝑀𝑣 ; Γ𝑣 , 𝑥 and Θ′ = 𝑀𝑤 ; Γ𝑤 : (𝑣, 𝑤)[𝑡∕𝑥] = (𝑣[𝑡∕𝑥], 𝑤) so the SL holds by
          IH on Θ ⊢𝑙 𝑣.
        ∙ Θ = 𝑀𝑣 ; Γ𝑣 and Θ′ = 𝑀𝑤 ; Γ𝑤 , 𝑥: (𝑣, 𝑤)[𝑡∕𝑥] = (𝑣, 𝑤[𝑡∕𝑥]) so the SL holds by
          IH on Θ′ ⊢𝑙 𝑤.
  ∙ let 𝑦 = 𝑢1 in 𝑢2 : similarly, we proceed by case analysis on the context:
        ∙ 𝑥 ∈ Θ: (let 𝑦 = 𝑢1 in 𝑢2 )[𝑡∕𝑥] = (let 𝑦 = 𝑢1 in 𝑢2 [𝑡∕𝑥]) so the SL holds by IH
          on Θ, 𝑦 ⊢𝑙 𝑢2 .
        ∙ 𝑥 ∈ Θ′ : (let 𝑦 = 𝑢1 in 𝑢2 )[𝑡∕𝑥] = (let 𝑦 = 𝑢1 [𝑡∕𝑥] in 𝑢2 ) so the SL holds by IH
          on Θ′ ⊢𝑙 𝑢1 .
  ∙ (𝑣, 𝑦.𝑢1 , 𝑧.𝑢2 ): by case analysis on the context:
        ∙ 𝑥 ∈ Θ: (𝑣, 𝑦.𝑢1 , 𝑧.𝑢2 )[𝑡∕𝑥] = (𝑣, 𝑦.𝑢1 [𝑡∕𝑥], 𝑧.𝑢2 [𝑡∕𝑥]) so the SL holds by IH on
          Θ, 𝑦 ⊢𝑙 𝑢1 and Θ, 𝑧 ⊢𝑙 𝑢2 .
        ∙ 𝑥 ∈ Θ′ : (𝑣, 𝑦.𝑢1 , 𝑧.𝑢2 )[𝑡∕𝑥] = (𝑣[𝑡∕𝑥], 𝑦.𝑢1 , 𝑧.𝑢2 ) the SL holds by IH on Θ′ ⊢𝑙 𝑣.
  ∙ 𝛿(𝑣, (𝑦, 𝑧).𝑢1 ): by case analysis on the context.
  ∙ 𝛿(𝑣, ().𝑡): by case analysis on the context.
  ∙ 𝑣𝑤: by case analysis on the context.

    We then extend ⊢𝑙 for stacks and commands, with a multiset of resources and no
variables:


                                                     38
Lemma 19. Reducing a linear command results in a linear command with the same
multiset of resources, i.e. for all 𝑐1 , 𝑐2 , 𝑀 such that 𝑀 ⊢𝐶
                                                             𝑙
                                                               𝑐1 and 𝑐1 ⇝ 𝑐2 one has
     𝐶
𝑀 ⊢𝑙 𝑐2 .

Proof. By induction on reduction steps 𝑐1 ⇝ 𝑐2:

  ∙ ⟨let 𝑥+ = 𝑡 in 𝑢 ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡 ∣ (𝑥+ .𝑢) · 𝑠 ∣ 𝑙⟩: by definition of 𝑀 ⊢𝐶    𝑙
                                                                                    𝑐1, we get
    𝑀𝑡 ; ⊢𝑙 𝑡, 𝑀𝑢 ; 𝑥 ⊢𝑙 𝑢 and 𝑀𝑠 ⊢𝑆𝑙 𝑠 with 𝑀 = 𝑀𝑠 ++ 𝑀𝑢 ++ 𝑀𝑡 ++ 𝑙, hence we have
    𝑀𝑠 ++ 𝑀𝑢 ⊢𝑙 (𝑥+ .𝑢) · 𝑠 and so 𝑀𝑠 ++ 𝑀𝑢 ++ 𝑀𝑡 ++ 𝑙 = 𝑀 ⊢𝐶          𝑙
                                                                         𝑐2.
  ∙ ⟨let 𝑥− = 𝑡 in 𝑢 ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑢[𝑡∕𝑥] ∣ 𝑠 ∣ 𝑙⟩: by definition, we get 𝑀𝑡 ; ⊢𝑙 𝑡, 𝑀𝑢 ; 𝑥 ⊢𝑙 𝑢
    and 𝑀𝑠 ⊢𝑆𝑙 𝑠, hence by SL we have 𝑀𝑡 ++ 𝑀𝑢 ; ⊢𝑙 𝑡[𝑢∕𝑥] and so 𝑀 ⊢𝐶            𝑙
                                                                                    𝑐2.
  ∙ ⟨𝜋𝑖 𝑡 ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡 ∣ 𝜋𝑖 · 𝑠 ∣ 𝑙⟩: by definition, we get 𝑀𝑡 ; ⊢𝑙 𝑡 and 𝑀𝑠 ⊢𝑆𝑙 𝑠, hence
    𝑀 ⊢𝐶   𝑙
               𝑐2.
  ∙ ⟨𝑣 ∣ (𝑥.𝑡) · 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩: by definition, we get 𝑀𝑣 ; ⊢𝑙 𝑣, 𝑀𝑡 ; 𝑥 ⊢𝑙 𝑡 and
    𝑀𝑠 ⊢𝑆𝑙 𝑠, hence by SL we have 𝑀𝑡 ++ 𝑀𝑣 ; ⊢𝑙 𝑡[𝑣∕𝑥] and so 𝑀 ⊢𝐶           𝑙
                                                                                 𝑐2.
  ∙ ⟨𝜆𝑥.𝑡 ∣ 𝑣 · 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩: by definition, we get 𝑀𝑡 ; 𝑥 ⊢𝑙 𝑡, 𝑀𝑣 ; ⊢𝑙 𝑣 and
    𝑀𝑠 ⊢𝑆𝑙 𝑠, hence by SL we have 𝑀𝑡 ++ 𝑀𝑣 ; ⊢𝑙 𝑡[𝑣∕𝑥] and so 𝑀 ⊢𝐶           𝑙
                                                                                 𝑐2.
  ∙ ⟨⟨𝑡1 , 𝑡2 ⟩ ∣ 𝜋𝑖 · 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡𝑖 ∣ 𝑠 ∣ 𝑙⟩: by definition, we get 𝑀𝑡 ; ⊢𝑙 𝑡1 , 𝑀𝑡 ; ⊢𝑙 𝑡2 and
    𝑀𝑠 ⊢𝑆𝑙 𝑠, hence 𝑀 ⊢𝐶       𝑙
                                 𝑐2.
  ∙ ⟨𝛿((𝑣, 𝑤), (𝑥, 𝑦).𝑡) ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡[𝑣∕𝑥, 𝑤∕𝑦] ∣ 𝑠 ∣ 𝑙⟩: by definition, we get 𝑀𝑣 ; ⊢𝑙 𝑣,
    𝑀𝑤 ; ⊢𝑙 𝑤, 𝑀𝑡 ; 𝑥, 𝑦 ⊢𝑙 𝑡 and 𝑀𝑠 ⊢𝑆𝑙 𝑠, hence by SL twice we have 𝑀𝑡 ++ 𝑀𝑣 ++
    𝑀𝑤 ; ⊢𝑙 𝑡[𝑣∕𝑥][𝑤∕𝑦] = 𝑡[𝑣∕𝑥, 𝑤∕𝑦] and so 𝑀 ⊢𝐶          𝑙
                                                             𝑐2.
  ∙ ⟨𝛿((), ().𝑡) ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡 ∣ 𝑠 ∣ 𝑙⟩: by definition, we get 𝑀𝑡 ; ⊢𝑙 𝑡 and 𝑀𝑠 ⊢𝑆𝑙 𝑠, hence
    𝑀 ⊢𝐶   𝑙
             𝑐2.
  ∙ ⟨𝛿(𝜄𝑖 𝑣, 𝑥1 .𝑡1 , 𝑥2 .𝑡2 ) ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡𝑖 [𝑥𝑖 ∕𝑣] ∣ 𝑠 ∣ 𝑙⟩: by definition, we get 𝑀𝑣 ; ⊢𝑙 𝑣,
    𝑀𝑡 ; 𝑥1 ⊢𝑙 𝑡1 , 𝑀𝑡 ; 𝑥2 ⊢𝑙 𝑡2 and 𝑀𝑠 ⊢𝑆𝑙 𝑠, hence by SL we have 𝑀𝑡 ++𝑀𝑣 ; ⊢𝑙 𝑡𝑖 [𝑣∕𝑥𝑖 ]
    and so 𝑀 ⊢𝐶      𝑙
                       𝑐2.
  ∙ ⟨𝐧𝐞𝐰 ∣ () · 𝑠 ∣ 𝑟𝑛 ∶∶ 𝑙⟩ ⇝ ⟨𝜄1 𝑟𝑛 ∣ 𝑠 ∣ 𝑙⟩: by definition, we get ; ⊢𝑙 𝐧𝐞𝐰, ; ⊢𝑙 () and
    𝑀𝑠 ⊢𝑆𝑙 𝑠, hence 𝑀𝑠 ++ 𝑟𝑛 ∶∶ 𝑙 = 𝑀 ⊢𝐶           𝑙
                                                     𝑐2.
  ∙ ⟨𝐧𝐞𝐰 ∣ () · 𝑠 ∣ Nil⟩ ⇝ ⟨𝜄2 () ∣ 𝑠 ∣ Nil⟩: by definition, we get ; ⊢𝑙 𝐧𝐞𝐰, ; ⊢𝑙 () and
    𝑀𝑠 ⊢𝑆𝑙 𝑠, hence 𝑀𝑠 = 𝑀 ⊢𝐶           𝑙
                                          𝑐2.
  ∙ ⟨𝐝𝐞𝐥𝐞𝐭𝐞 ∣ 𝑟𝑛 · 𝑠 ∣ 𝑙⟩ ⇝ ⟨() ∣ 𝑠 ∣ 𝑟𝑛 ∶∶ 𝑙⟩: by definition, we get ; ⊢𝑙 𝐝𝐞𝐥𝐞𝐭𝐞, 𝑟𝑛 ; ⊢𝑙 𝑟𝑛 and
    𝑀𝑠 ⊢𝑆𝑙 𝑠, hence 𝑀𝑠 ++ 𝑟𝑛 ∶∶ 𝑙 = 𝑀 ⊢𝐶           𝑙
                                                     𝑐2.

    Finally, we show that ∀ ⊢ 𝑡 ∶ 𝑃 ∈ 𝑃 𝑟, ∀𝑣, ∀𝑙, ∀𝑙′ , ⟨𝑡 ∣ ⋆ ∣ 𝑙⟩ ⇝ ⟨𝑣 ∣ ⋆ ∣ 𝑙′ ⟩ ⇒
∃𝜎, 𝑙′ = 𝜎(𝑙).

Proof. By progress and subject reduction, we have that ⊢ 𝑣 ∶ 𝑊 . By induction on
the typing derivation, we have that ⊢ 𝑡 ∶ 𝐴 ⇒; ⊢𝑙 𝑡, hence 𝑙 ⊢𝐶  𝑙
                                                                   ⟨𝑡 ∣ ⋆ ∣ 𝑙⟩. By the
previous lemma, we get 𝑙 ⊢𝑙 ⟨𝑣 ∣ ⋆ ∣ 𝑙 ⟩. Because 𝑊 is central, 𝑣 is a final value, so it
                           𝐶          ′

does not contain any resource. Hence, 𝑙 and 𝑙′ are obtained from the same multiset, so
∃𝜎, 𝑙′ = 𝜎(𝑙).


                                              39
D     Details: translation of the resource CBPV

D.1   Proof of well-typed translation

All terms must be translated to values. Recall that ⇓𝐴 ≝ 𝐴 & 1, hence the type of
translated expressions and negative values is negative, so they have no value restriction.
So, we must only check the value restriction when translating positive values.
    Contexts are translated by translating each type separately, so (Γ, Δ)+ = Γ+ , Δ+ .
    Values of central types are translated to the same value and type in , so J⊢ Alloc_failure ∶
𝐸K = ⊢ Alloc_failure ∶ 𝐸. Moreover, because  ,𝐦𝐨𝐯𝐞 is an extension of , it can use
linear swaps for exceptions.
    We proceed by cases:

  ∙ J𝑥 ⊢ 𝑥 ∶ 𝐴K must be a value of type 𝐴+ ⊢ 𝐴+ . Hence, 𝑥 is well-typed.
  ∙ J⊢ 𝐝𝐫𝐨𝐩 ∶ 1 ⟜ 𝐴K must be a value of type ⊢ (1 ⟜ 𝐴+ ) & 1. Hence, ⟨drop𝐴 , ()⟩ is
    well-typed.
  ∙ JΓ ⊢ coerc(𝑣) ∶ 𝑃 K must be a value of type Γ+ ⊢ (𝑃 + ⊕ 𝐸) & 𝐼. By IH, we have
    Γ+ ⊢ J𝑣K ∶ 𝑃 + . Hence, ⟨𝜄1 J𝑣K, drop_ctxΓ ⟩ is well-typed.
  ∙ JΓ, 𝑥 ∶ 𝐴, Δ ⊢ 𝐦𝐨𝐯𝐞(𝑥) in 𝑡 ∶ 𝐶K must be a value of type Γ+ , Δ+ , 𝑥 ∶ 𝐴+ ⊢ ⇓𝐶 − .
    By IH, we have Γ+ , 𝑥 ∶ 𝐴+ , 𝑦 ∶ 𝐵 + , Δ+ ⊢ J𝑡K ∶ ⇓𝐶 − . It’s the only rule where we
    allow ourselves to use  structural rule to swap premises. Hence, J𝑡K is well-typed.
  ∙ J⊢ 𝐧𝐞𝐰 ∶ 𝑅 ⟜ 1K must be a value of type ⊢ 𝑅⊕𝐸 ⟜ 1. We have ⊢ Alloc_failure ∶
    𝐸, so let 𝑥 = 𝐧𝐞𝐰() in 𝛿(𝑥, 𝑟.𝜄1 𝑟, 𝑖.𝑖; 𝜄2 Alloc_failure) is well-typed.
  ∙ JΓ, Δ ⊢ let 𝑥 = (𝑣 ∶ 𝐴) in 𝑡 ∶ 𝐵K must be a value of type Γ+ , Δ+ ⊢ ⇓𝐵 − . By IH,
    we have Δ+ ⊢ J𝑣K ∶ 𝐴+ and Γ+ , 𝑥 ∶ 𝐴+ ⊢ J𝑡K ∶ ⇓𝐵 − . Hence, let 𝑥 = J𝑣K inJ𝑡K is
    well-typed.
  ∙ JΓ, Δ ⊢ let 𝑥 = (𝑡 ∶ 𝑃 ) in 𝑢 ∶ 𝐴K must be a value of type Γ+ , Δ+ ⊢ 𝐴− & 𝐼. By
    IH, we have Δ+ ⊢ J𝑡K ∶ (𝑃 + ⊕ 𝐸) & 𝐼 and Γ+ , 𝑥 ∶ 𝑃 + ⊢ J𝑢K ∶ 𝐴− & 𝐼. Then,
    raise𝐴&𝐼
         Γ     (𝑒) is of type Γ+ ⊢ 𝐴− & 𝐼, so let 𝑠 = 𝜋1 J𝑡K in 𝛿(𝑠, 𝑥.J𝑢K, 𝑒. raise𝐴&𝐼
                                                                                    Γ   (𝑒)) is
    well-typed.
  ∙ J⊢ 𝐫𝐚𝐢𝐬𝐞 ∶ 𝐴 ⟜ 𝐸K must be a value of type ⊢ (𝐴− ⟜ 𝐸)&𝐼. Hence, ⟨𝜆𝑒. raise𝐴         ⋆ (𝑒), ()⟩
    is well-typed.
  ∙ JΓ, Δ ⊢ 𝐭𝐫𝐲 𝑥 ⇐ (𝑡 ∶ 𝑃 ) in 𝑢 𝐮𝐧𝐥𝐞𝐬𝐬 𝑒 ⇒ 𝑢′ ∶ 𝐵K must be a value of type Γ+ , Δ+ ⊢
    ⇓𝐵 − . By IH, we have:
       ∙ Δ+ ⊢ J𝑡K ∶ (𝑃 + ⊕ 𝐸) & 𝐼.
       ∙ Γ+ , 𝑥 ∶ 𝑃 + ⊢ J𝑢K ∶ ⇓𝐵 − .
       ∙ Γ+ , 𝑒 ∶ 𝐸 ⊢ J𝑢′ K ∶ ⇓𝐵 − .
    Hence, let 𝑠 = 𝜋1 J𝑡K in 𝛿(𝑠, 𝑥.J𝑢K, 𝑒.J𝑢′ K) is well-typed.
  ∙ JΓ, Δ ⊢ (𝑣, 𝑤) ∶ 𝐴 ⊗ 𝐵K must be a value of type Γ+ , Δ+ ⊢ 𝐴+ ⊗ 𝐵 + . By IH, we
    have Γ+ ⊢ J𝑣K ∶ 𝐴+ and Δ+ ⊢ J𝑤K ∶ 𝐵 + . Hence, (J𝑣K, J𝑤K) is well-typed.
  ∙ JΓ, Δ, Γ′ ⊢ 𝛿(𝑣, (𝑥, 𝑦).𝑡) ∶ 𝐶K must be a value of type Γ+ , Δ+ , Γ′+ ⊢ ⇓𝐶 − . By IH,
    we have Δ+ ⊢ J𝑣K ∶ 𝐴+ ⊗ 𝐵 + and Γ+ , 𝑥 ∶ 𝐴+ , 𝑦 ∶ 𝐵 + , Γ′+ ⊢ J𝑡K ∶ ⇓𝐶 − . Hence,
    𝛿(J𝑣K, (𝑥, 𝑦).J𝑡K) is well-typed.
  ∙ J⊢ () ∶ 1K must be a value of type ⊢ 1. Hence, () is well-typed.
  ∙ JΓ, Δ, Γ′ ⊢ 𝛿(𝑣, ().𝑡) ∶ 𝐶K must be a value of type Γ+ , Δ+ , Γ′+ ⊢ ⇓𝐶 − . By IH, we
    have Δ+ ⊢ J𝑣K ∶ 1 and Γ+ , Γ′+ ⊢ J𝑡K ∶ ⇓𝐶 − . Hence, 𝛿(J𝑣K, ().J𝑡K) is well-typed.


                                              40
    ∙ JΓ ⊢ 𝜄1 𝑣 ∶ 𝐴 ⊕ 𝐵K must be a value of type Γ+ ⊢ 𝐴+ ⊕ 𝐵 + . By IH, we have
      Γ+ ⊢ J𝑣K ∶ 𝐴+ . Hence, 𝜄1 J𝑣K is well-typed.
    ∙ JΓ ⊢ 𝜄2 𝑣 ∶ 𝐴 ⊕ 𝐵K must be a value of type Γ+ ⊢ 𝐴+ ⊕ 𝐵 + . By IH, we have
      Γ+ ⊢ J𝑣K ∶ 𝐵 + . Hence, 𝜄2 J𝑣K is well-typed.
    ∙ JΓ, Δ, Γ′ ⊢ 𝛿(𝑣, 𝑥.𝑡, 𝑦.𝑢) ∶ 𝐶K must be a value of type Γ+ , Δ+ , Γ′+ ⊢ ⇓𝐶 − . By IH,
      we have:
        ∙ Δ+ ⊢ J𝑣K ∶ 𝐴+ ⊕ 𝐵 + .
        ∙ Γ+ , 𝑥 ∶ 𝐴+ , Γ′+ ⊢ J𝑡K ∶ ⇓𝐶 − .
        ∙ Γ+ , 𝑦 ∶ 𝐵 + , Γ′+ ⊢ J𝑢K ∶ ⇓𝐶 − .
      Hence, 𝛿(J𝑣K, 𝑥.J𝑡K, 𝑦.J𝑢K) is well-typed.
    ∙ JΓ ⊢ 𝜆𝑥.𝑡 ∶ 𝐵 ⟜ 𝐴K must be a value of type Γ+ ⊢ (𝐵 − ⟜ 𝐴+ ) & 𝐼. By IH, we have
      𝑥 ∶ 𝐴+ , Γ+ ⊢ J𝑡K ∶ 𝐵 − & 𝐼. Hence, ⟨𝜆𝑥.𝜋1 J𝑡K, drop_ctxΓ ⟩ is well-typed.
    ∙ JΓ, Δ ⊢ 𝑣𝑤 ∶ 𝐵K must be a value of type Γ+ , Δ+ ⊢ ⇓𝐵 − . By IH, we have Γ+ ⊢
      J𝑤K ∶ 𝐴+ and Γ+ ⊢ J𝑣K ∶ (𝐵 − ⟜ 𝐴+ ) & 𝐼. Hence, ⟨(𝜋1 J𝑣K)J𝑤K, drop_ctxΓ,Δ ⟩ is
      well-typed.
    ∙ JΓ ⊢ ⟨𝑡, 𝑢⟩ ∶ 𝐴 & 𝐵K must be a value of type Γ+ ⊢ (𝐴− & 𝐵 − ) & 𝐼. By IH, we have
      Γ+ ⊢ J𝑡K ∶ 𝐴− & 𝐼 and Γ+ ⊢ J𝑢K ∶ 𝐵 − & 𝐼. Hence, ⟨⟨𝜋1 J𝑡K, 𝜋1 J𝑢K⟩, drop_ctxΓ ⟩ is
      well-typed.
    ∙ JΓ ⊢ 𝜋1 𝑣 ∶ 𝐴K must be a value of type Γ+ ⊢ 𝐴− & 𝐼. By IH, we have Γ+ ⊢ J𝑣K ∶
      (𝐴− & 𝐵 − ) & 𝐼. Hence, ⟨𝜋1 𝜋1 J𝑣K, drop_ctxΓ K⟩ is well-typed.
    ∙ JΓ ⊢ 𝜋2 𝑣 ∶ 𝐵K must be a value of type Γ+ ⊢ 𝐵 − & 𝐼. By IH, we have Γ+ ⊢ J𝑣K ∶
      (𝐴− & 𝐵 − ) & 𝐼. Hence, ⟨𝜋2 𝜋1 J𝑣K, drop_ctxΓ K⟩ is well-typed.


E     Details: presheaf model

E.1     Interpretation of types and terms

Resources appearing in terms of the operational semantics are interpreted as variables of
type 𝑅.
    Each type has a positive and negative interpretation:

    ∙ 1+ ≝ 𝐼, (𝐴 ⊗ 𝐵)+ ≝ 𝐴+ ⊗ 𝐵 + , (𝐴 ⊕ 𝐵)+ ≝ 𝐴+ ⊕ 𝐵 + , 𝑁 + ≝ 𝐺(𝑁 − )
    ∙ (𝐵 ⟜ 𝐴)− ≝ 𝐵 − ⟜ 𝐴+ , (𝐴 & 𝐵)− ≝ 𝐴− × 𝐵 − , 𝑃 − ≝ 𝐹 (𝑃 + )

    A context with resources Γ; [𝑟1 … 𝑟𝑛 ]; Δ is interpreted positively by Γ+ ⊗ 𝑅𝑛 ⊗ Δ+
with 𝑅𝑛+1 ≝ 𝑅𝑛 ⊗ 𝑅, 𝑅0 ≝ 𝐼, (𝑥 ∶ 𝐴, Γ)+ ≝ 𝐴+ ⊗ Γ+ . Lists of resources are then
written 𝐿𝑥 and their translation 𝐿+
                                  𝑥.
    Each judgement kind with resources have an interpretation:

    ∙ Values Θ ⊢𝑜 𝑣 ∶ 𝐴 in C(Θ+ , 𝐴+ ).
    ∙ Expressions Θ ⊢𝑜 𝑡 ∶ 𝐴 in C(Θ+ , 𝐺𝐴− ).
    ∙ Stacks 𝐿𝑠; 𝑠 ∶ 𝐴 ⊢𝑜 𝐵 in C(𝐿𝑠+ ⊗ 𝐴− , 𝐵 − ).
    ∙ Commands 𝐿𝑐 ⊢𝑜 𝑐 ∶ 𝐴 in C(𝐿𝑐 + , 𝐴− ).

    To interpret terms, types in the derivation of ⊢𝑜 are made explicit. In particular,
stacks 𝐿 ⊢𝑆𝑜 𝑠 are written 𝐿; 𝑠 ∶ 𝐴 ⊢𝑆𝑜 𝐵.


                                            41
    Composition is written in the diagrammatic order with ;. 𝜂 is the unit of 𝐺𝐹 . 𝑓 ∗ is
the adjoint of 𝑓 under 𝐹 ⊣ 𝐺. 𝑓 𝑠𝑡𝑟Γ precomposes 𝑓 with the isomorphism Γ ⊗ 𝐹 𝐴 ≅
                                         ⟜∕⊸
𝐹 (Γ ⊗ 𝐴) in the relevant direction. 𝑓 𝜆     is the adjoint of 𝑓 under ⊗ ⊣⟜ (respectively
⊸), and 𝑒𝑣⟜∕⊸ the evaluation morphism of this adjunction. 𝑑𝑖𝑠 is the canonical morphism
Γ ⊗ (𝐴 ⊕ 𝐵) ⊗ Γ′ → (Γ ⊗ 𝐴 ⊗ Γ′ ) ⊕ (Γ ⊗ 𝐵 ⊗ Γ′ ) obtained from the fact that the
category is monoidal distributive, because it is biclosed. Apart from 𝑠𝑡𝑟, associators and
unitors of the monoidal product are left implicit.
    Values have explicit coercions inserted on positive values where expressions are
expected, written coerc(𝑣) below.

  ∙ JΘ ⊢𝑜 coerc(𝑣) ∶ 𝑃 K ≝ J𝑣K; 𝜂 ∶ C(Θ+ , 𝐺𝐹 𝑃 + )
  ∙ J𝑥 ∶ 𝐴 ⊢𝑜 𝑥 ∶ 𝐴K ≝ 𝑖𝑑𝐴+ ∶ C(𝐴+ , 𝐴+ )
  ∙ J𝑟 ∶ 𝑅 ⊢𝑜 𝑟 ∶ 𝑅K ≝ 𝑖𝑑𝑅 ∶ C(𝑅, 𝑅)
  ∙ J⊢𝑜 () ∶ 1K ≝ 𝑖𝑑𝐼 ∶ C(𝐼, 𝐼)
  ∙ JΘ, Θ′ ⊢𝑜 (𝑣, 𝑤) ∶ 𝐴 ⊗ 𝐵K ≝ J𝑣K ⊗ J𝑤K ∶ C(Θ+ ⊗ Θ′+ , 𝐴+ ⊗ 𝐵 + )
  ∙ JΘ ⊢𝑜 𝜄1 𝑣 ∶ 𝐴 ⊕ 𝐵K ≝ J𝑣K; 𝑖𝑛𝑙 ∶ C(Θ+ , 𝐴+ ⊕ 𝐵 + )
  ∙ JΘ ⊢𝑜 𝜄2 𝑣 ∶ 𝐴 ⊕ 𝐵K ≝ J𝑣K; 𝑖𝑛𝑟 ∶ C(Θ+ , 𝐴+ ⊕ 𝐵 + )
  ∙ JΘ, Θ′ , Θ′′ ⊢𝑜 𝛿(𝑣, ().𝑡) ∶ 𝐶K ≝ J𝑡K ∶ C(Θ+ ⊗ Θ′+ ⊗ Θ+ , 𝐺𝐶 − )
  ∙ JΘ, Θ′ , Θ′′ ⊢𝑜 𝛿(𝑣, (𝑥, 𝑦).𝑡) ∶ 𝐶K ≝ (𝑖𝑑Θ+ ⊗ J𝑣K ⊗ 𝑖𝑑Θ′′+ ); J𝑡K ∶ C(Θ+ ⊗ Θ′+ ⊗
    Θ+ , 𝐺𝐶 − )
  ∙ JΘ, Θ′ , Θ′′ ⊢𝑜 𝛿(𝑣, 𝑥.𝑡, 𝑦.𝑢) ∶ 𝐶K ≝ (𝑖𝑑Θ+ ⊗J𝑣K⊗𝑖𝑑Θ′′+ ); 𝑑𝑖𝑠; (J𝑡K ∣ J𝑢K) ∶ C(Θ+ ⊗
    Θ′+ ⊗ Θ+ , 𝐺𝐶 − )
                                          ⟜
  ∙ JΘ ⊢𝑜 𝜆𝑥.𝑡 ∶ 𝐵 ⟜ 𝐴K ≝ J𝑡K∗;𝑠𝑡𝑟Θ+ ;𝜆 ;∗ ∶ C(Θ+ , 𝐺(𝐵 − ⟜ 𝐴+ ))
  ∙ JΘ ⊢𝑜 ⟨𝑡, 𝑢⟩K ≝ (J𝑡K∗ × J𝑢K∗ )∗ ∶ C(Θ+ , 𝐺(𝐴− & 𝐵 − ))
  ∙ JΘ, Θ′ ⊢𝑜 𝑣𝑤 ∶ 𝐵K ≝ ((J𝑤K ⊗ J𝑣K∗ ); 𝑒𝑣)𝑠𝑡𝑟Θ+ ;∗ ∶ C(Θ+ ⊗ Θ′+ , 𝐺𝐵 − )
  ∙ JΘ ⊢𝑜 𝜋1 𝑣 ∶ 𝐴K ≝ (𝑣∗ ; 𝜋1 )∗ ∶ C(Θ+ , 𝐺𝐴− )
  ∙ JΘ ⊢𝑜 𝜋2 𝑣 ∶ 𝐵K ≝ (𝑣∗ ; 𝜋2 )∗ ∶ C(Θ+ , 𝐺𝐵 − )
  ∙ JΘ, Θ′ ⊢𝑜 let 𝑥 = (𝑡 ∶ 𝑃 ) in 𝑢K ≝ ((𝑖𝑑Θ+ ⊗ J𝑡K∗ ); J𝑢K∗;𝑠𝑡𝑟Θ+ )𝑠𝑡𝑟Θ+ ;∗ ∶ C(Θ+ ⊗
    Θ′+ , 𝐺𝐵 − )
  ∙ JΘ, Θ′ ⊢𝑜 let 𝑥 = (𝑡 ∶ 𝑁) in 𝑢K ≝ (𝑖𝑑Θ+ ⊗ J𝑡K); J𝑢K ∶ C(Θ+ ⊗ Θ′+ , 𝐺𝐵 − )
  ∙ J⊢𝑜 𝐧𝐞𝐰 ∶ 𝑅⊕1 ⟜ 1K ≝ 𝑙 → 𝑖 → match 𝑙{𝑥∶∶𝑡 → (𝑖𝑛𝑟(𝑥), 𝑡) ∣ [] → (𝑖𝑛𝑟(()), [])} ∶
    C(𝐼, 𝐺(𝐹 (𝑅 ⊕ 𝐼) ⟜ 𝐼))

   Stacks are interpreted as such:

  ∙ J[]; ⋆ ∶ 𝐴 ⊢𝑜 𝐴K ≝ 𝑖𝑑𝐴− ∶ C(𝐴− , 𝐴− )
  ∙ J𝐿𝑠; 𝜋1 · 𝑠 ∶ 𝐴 & 𝐵 ⊢𝑜 𝐶K ≝ 𝜋1 ; J𝑠K ∶ C(𝐿𝑠+ ⊗ (𝐴− & 𝐵 − ), 𝐶 − )
  ∙ J𝐿𝑠; 𝜋2 · 𝑠 ∶ 𝐴 & 𝐵 ⊢𝑜 𝐶K ≝ 𝜋2 ; J𝑠K ∶ C(𝐿𝑠+ ⊗ (𝐴− & 𝐵 − ), 𝐶 − )
  ∙ J𝐿𝑠 ++ 𝐿𝑡; 𝑣 · 𝑠 ∶ 𝐵 ⟜ 𝐴 ⊢𝑜 𝐶K ≝ (𝑖𝑑𝐿𝑠+ ⊗ ((J𝑣K ⊗ 𝑖𝑑𝐵− ⟜𝐴+ ); 𝑒𝑣⟜ )); J𝑠K ∶
    C(𝐿𝑠+ ⊗ 𝐿𝑡+ ⊗ (𝐵 − ⟜ 𝐴+ ), 𝐶 − )
  ∙ J𝐿𝑠 ++ 𝐿𝑡; (𝑥+ .𝑡) · 𝑠 ∶ 𝐴 ⊢𝑜 𝐶K ≝ (𝑖𝑑𝐿𝑠+ ⊗ J𝑡K∗;𝑠𝑡𝑟𝐿𝑡+ ); J𝑠K ∶ C(𝐿𝑠+ ⊗ 𝐿𝑡+ ⊗
    𝐹 𝐴+ , 𝐶 − )

   Finally, J𝐿𝑠 ++ 𝐿𝑡 ++ 𝐿𝑙 ⊢𝑜 ⟨𝑡 ∣ 𝑠 ∣ 𝑙⟩K ≝ (((𝑖𝑑𝐿𝑠+ ⊗ J𝑡K∗ ); J𝑠K)𝑠𝑡𝑟𝐿𝑠+ ;∗ ⊗ (! ∶ 𝐿𝑙 →
[𝑅])); 𝑒𝑣⊸ .


                                           42
E.2   Proof of (lemma 13)
Proof. By induction on the derivation of 𝑡 with explicit coercions. Uses naturality of ⊗
associativity left implicit, as well as other transformations (∗, 𝑠𝑡𝑟, ×, 𝜆) that interpret rules
of negative connectives. For ∗, it means in particular that 𝑓 ; (𝑔 ∗ ; ℎ)∗ = (𝐹 𝑓 ; (𝑔 ∗ ; ℎ))∗ =
((𝑓 ; 𝑔)∗ ; ℎ)∗ :
  ∙ Jcoerc(𝑤)[𝑣∕𝑥]K = J𝑤[𝑣∕𝑥]K; 𝜂 = Jcoerc(𝑤[𝑣∕𝑥]) by induction hypothesis.
  ∙ J𝑥[𝑣∕𝑥]K = J𝑣K.
  ∙ No variables in 𝑟, 𝐧𝐞𝐰 nor ().
  ∙ JΓ, Δ ⊢𝑜 (𝑣, 𝑤)K: either 𝑥 ∈ Γ or 𝑥 ∈ Δ, in which cases we need to show
    J(𝑤, 𝑤′ )[𝑣∕𝑥]K = J(𝑤[𝑣∕𝑥], 𝑤′ )K or J(𝑤[𝑣∕𝑥], 𝑤′ )K. Those hold by IH.
  ∙ J(𝜄𝑖 𝑤)[𝑣∕𝑥]K = J𝜄𝑖 (𝑤[𝑣∕𝑥])K by IH.
  ∙ J𝛿(𝑤, ().𝑡)[𝑣∕𝑥]K: split case on 𝑣 ∈ Γ, 𝑣 ∈ Δ or 𝑣 ∈ Γ′ . In each case, the SL holds
    by IH.
  ∙ J𝛿(𝑤, (𝑦, 𝑧).𝑡)[𝑣∕𝑥]K: same split case. In each case, the SL holds by IH.
  ∙ J𝛿(𝑤, 𝑦.𝑡, 𝑧.𝑢)[𝑣∕𝑥]K: same split case. In each case, the SL holds by IH.
  ∙ ⟨𝑡, 𝑢⟩: for ⟨𝑡, 𝑢⟩[𝑣∕𝑥] = ⟨𝑡[𝑣∕𝑥], 𝑢[𝑣∕𝑥]⟩, we need to show that (𝑖𝑑Γ+ ⊗ J𝑣K ⊗
    𝑖𝑑Γ′+ ); (J𝑡K∗ × J𝑢K∗ )∗ = (((𝑖𝑑Γ+ ⊗ J𝑣K ⊗ 𝑖𝑑Γ′+ ); J𝑡K)∗ × ((𝑖𝑑Γ+ ⊗ J𝑣K ⊗ 𝑖𝑑Γ′+ ); J𝑢K)∗ )∗ .
    Hence, the SL holds by IH and naturality of ∗ and ×.
  ∙ 𝜋𝑖 𝑣: similarly, because (𝜋𝑖 𝑣)[𝑡∕𝑥] = 𝜋𝑖 (𝑣[𝑡∕𝑥]) the SL holds by IH and naturality of
    ∗.
  ∙ 𝜆𝑦.𝑢1 : because 𝜆𝑦.(𝑢1 [𝑡∕𝑥]) = (𝜆𝑦.𝑢1 )[𝑡∕𝑥], both SL hold by IH and naturality of ∗
    and 𝑠𝑡𝑟.
  ∙ 𝑤𝑤′ : split case on whether we have 𝑤[𝑣∕𝑥] = 𝑤 or 𝑤′ [𝑣∕𝑥] = 𝑤′ , in both cases it
    holds by IH and naturality of ∗, 𝑠𝑡𝑟 and 𝜆.
  ∙ JΓ, Δ ⊢𝑜 (let 𝑦 = (𝑡 ∶ 𝑃 ) in 𝑢)[𝑣∕𝑥]K: split case on 𝑣 ∈ Γ or 𝑣 ∈ Δ, in both cases it
    holds by SL and naturality of ∗ and 𝑠𝑡𝑟.
  ∙ JΓ, Δ ⊢𝑜 (let 𝑦 = (𝑡 ∶ 𝑁) in 𝑢)[𝑣∕𝑥]K: same split case. In both cases it holds by SL.

E.3   Proof of (theorem 14)
Proof. By case analysis on reduction steps: when only 𝑡 changes, we show that expres-
sions from both commands are equal. Otherwise, when the stack also changes, we show
that (𝐿𝑠+ ⊗ J𝑡K∗ ); J𝑠K from both command are equal. Finally, we consider the whole
command interpretation pontwise for 𝐧𝐞𝐰 and 𝐝𝐞𝐥𝐞𝐭𝐞 reduction rules.
  ∙ ⟨let 𝑥− = 𝑣 in 𝑢 ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑢[𝑡∕𝑥] ∣ 𝑠 ∣ 𝑙⟩: we need to show that Jlet 𝑥− = 𝑣 in 𝑢K =
    J𝑢[𝑣∕𝑥]K. Both expressions are equal by SL and definition of binding a negative
    value, that is precomposition.
  ∙ ⟨let 𝑥+ = 𝑡 in 𝑢 ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡 ∣ (𝑥+ .𝑢) · 𝑠 ∣ 𝑙⟩: we need to show that (𝑖𝑑𝐿𝑠+ ⊗ ((𝑖𝑑𝐿𝑢+ ⊗
    J𝑡K∗ ); J𝑢K∗;𝑠𝑡𝑟𝐿𝑢+ )𝑠𝑡𝑟𝐿𝑢+ ;∗;∗ ); J𝑠K = (𝑖𝑑𝐿𝑠+ ⊗ 𝑖𝑑𝐿𝑢+ ⊗ J𝑡K∗ ); (𝑖𝑑𝐿𝑠+ ⊗ J𝑢K∗;𝑠𝑡𝑟𝐿𝑢+ ); J𝑠K.
    It holds after cancelling the two ∗, re-associating parentheses with the first 𝑠𝑡𝑟 of the
    left expression then distributing ⊗.
  ∙ ⟨𝑣𝑤 ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑣 ∣ 𝑤 · 𝑠 ∣ 𝑙⟩: holds after cancelling ∗; ∗.
  ∙ ⟨𝜋𝑖 𝑡 ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡 ∣ 𝜋𝑖 · 𝑠 ∣ 𝑙⟩: holds after cancelling ∗; ∗ on the left expression.
  ∙ ⟨𝑣 ∣ (𝑥.𝑡) · 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩: Jcoerc(𝑣)K∗ = 𝐹 J𝑣K, then it holds by SL.


                                               43
  ∙ ⟨𝜆𝑥.𝑡 ∣ 𝑣 · 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡[𝑣∕𝑥] ∣ 𝑠 ∣ 𝑙⟩: holds after cancelling ∗; ∗ and computing 𝜆 with
    𝑒𝑣 on the left expression, then applying SL.
  ∙ ⟨⟨𝑡1 , 𝑡2 ⟩ ∣ 𝜋𝑖 · 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡𝑖 ∣ 𝑠 ∣ 𝑙⟩: holds after cancelling ∗; ∗ and computing 𝜋𝑖 on
    the left expression.
  ∙ ⟨𝛿((𝑣, 𝑤), (𝑥, 𝑦).𝑡) ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡[𝑣∕𝑥, 𝑤∕𝑦] ∣ 𝑠 ∣ 𝑙⟩: both command expressions are
    equal by applying SL twice.
  ∙ ⟨𝛿((), ().𝑡) ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡 ∣ 𝑠 ∣ 𝑙⟩: both command expressions are equal by unit laws.
  ∙ ⟨𝛿(𝜄𝑖 𝑣, 𝑥1 .𝑡1 , 𝑥2 .𝑡2 ) ∣ 𝑠 ∣ 𝑙⟩ ⇝ ⟨𝑡𝑖 [𝑥𝑖 ∕𝑣] ∣ 𝑠 ∣ 𝑙⟩: the left expression with SL is equal
    to the right after computing the distribution morphism and 𝑖𝑛𝑙∕𝑖𝑛𝑟 (for each 𝑖).
  ∙ ⟨𝐧𝐞𝐰 ∣ () · 𝑠 ∣ 𝑟𝑛 ∶∶ 𝑙⟩ ⇝ ⟨𝜄1 𝑟𝑛 ∣ 𝑠 ∣ 𝑙⟩: by definition of popping elements from a
    non-empty list of resources.
  ∙ ⟨𝐧𝐞𝐰 ∣ () · 𝑠 ∣ Nil⟩ ⇝ ⟨𝜄2 () ∣ 𝑠 ∣ Nil⟩: by definition of popping elements from an
    empty list of resources.
  ∙ ⟨𝐝𝐞𝐥𝐞𝐭𝐞 ∣ 𝑟𝑛 · 𝑠 ∣ 𝑙⟩ ⇝ ⟨() ∣ 𝑠 ∣ 𝑟𝑛 ∶∶ 𝑙⟩: by definition of pushing an element in a list
    of resources.

E.4 Proof that centre coincides with resource-free objects, and objects with trivial
    destructors
We will show the bi-implications 1 ⇐⇒ 2 and 2 ⇐⇒ 3 for the following properties
on object 𝐸 ∈ C (see proposition 15):
 1 𝐸 is in the Drinfeld centre of C.
 2 For all 𝑙 such that 𝑙 ≠ [], 𝐸(𝑙) = ∅.
 3 There is a morphism C(𝐸, 𝐼).
                                                         ∏
    Recall that a morphism C(𝐴, 𝐵) is a function family 𝑙 𝐴(𝑙) → 𝐵(𝑙).
    (2 ⇐⇒ 3) Resource-free objects have a trivial destructor:
                                         ∏
    We define the family of functions 𝑑 ∶ 𝑙 𝐸(𝑙) → 𝐼(𝑙) by case on 𝑙:
  ∙ If 𝑙 = [], then 𝐼([]) = {⋆} so we pick the unique function to it.
  ∙ Otherwise, 𝐸(𝑙) = ∅ so we pick the unique function from it.
    (3 ⇐⇒ 2) Objects with a trivial destructor have no resources:
    There is a function family ∀𝑙, 𝐸(𝑙) → 𝐼(𝑙). If 𝑙 = [], 𝐼(𝑙) = ∅ so it must be the case
that 𝐸(𝑙) = ∅.
    (1 ⇐⇒ 2) Objects in the Drinfeld centre have no resources. Such objects are pairs
𝐸 ∶ C, 𝜃 ∶ 𝐸 ⊗ − ≅ − ⊗ 𝐸) such that

                               𝜃𝐴⊗𝐵 = (𝜃𝐴 ⊗ 𝑖𝑑); (𝑖𝑑 ⊗ 𝜃𝐵 ) .

So, we have a bijection family
                  ∏∏ ∏                ∑
                                  ,           𝐸(𝑗) × 𝐴(𝑘) ≅ 𝐴(𝑗 ′ ) × 𝐸(𝑘′ ) .
                     𝐴      +𝑘=𝑙 𝑗 ′ +
                         𝑙 𝑗+        +𝑘′ =𝑙

    Suppose that there exists an inhabited list 𝑟 ∶∶ 𝑡 such that 𝐸(𝑟 ∶∶ 𝑡) is inhabited. We
will show that no such bijection family exists.


                                                 44
    We fix a resource 𝑟′ ≠ 𝑟. We instantiate 𝜃 with 𝐴(𝑡) ≝ {⋆}, 𝐴(−) ≝ ∅, 𝑗 ≝ 𝑟 ∶∶ 𝑡, 𝑘 ≝
[𝑟′ ]. We must show that for all 𝑗 ′ , 𝑘′ such that 𝑗 ′ ++ 𝑘′ = 𝑟 ∶∶ 𝑡 ++ [𝑟′ ], there is no
function 𝐸(𝑟 ∶∶ 𝑡) × 𝐴([𝑟 ]) → 𝐴(𝑗 ) × 𝐸(𝑘 ) : because 𝐸(𝑟 ∶∶ 𝑡) and 𝐴([𝑟′ ]) are inhabited,
                          ′         ′      ′

𝐴(𝑗 ′ ) × 𝐸(𝑘′ ) needs to be inhabited. However, 𝑗 ′ first element must be 𝑟, so 𝑗 ′ ≠ [𝑟′ ].
Hence 𝐴(𝑗 ′ ) = ∅, so the product is empty.
    (2 ⇐⇒ 1) We show that resource-free objects are in the Drinfeld centre. Given 𝐸
                               ∏ ∏ ∏           ∑
resource-free, we define 𝜃 ∶ 𝐴 𝑙 𝑗++𝑘=𝑙 𝑗 ′ ++𝑘′ =𝑙 𝐸(𝑗) × 𝐴(𝑘) ≅ 𝐴(𝑗 ′ ) × 𝐸(𝑘′ ) by
case on 𝑗:
  ∙ If 𝑗 = [] then 𝑘 = 𝑙, so we pick 𝑗 ′ = 𝑘, 𝑘′ = [] and the function

                         swap𝐸([]),𝐴(𝑘) ∶ 𝐸([]) × 𝐴(𝑘) ≅ 𝐴(𝑘) × 𝐸([])

    .
  ∙ Otherwise 𝐸(𝑗) = ∅, so we pick 𝑗 ′ ≝ 𝑗, 𝑘′ ≝ 𝑘 and the unique function from
    𝐸(𝑗) × 𝐴(𝑘).
We are left to check naturality and the centre additional condition. If 𝑗 ≠ [], they hold by
universal property, so we are left with the first case. swap is natural in both arguments,
so it only remains to show that

                               𝜃𝐴⊗𝐵 = (𝜃𝐴 ⊗ 𝑖𝑑); (𝑖𝑑 ⊗ 𝜃𝐵 ) .

    Those morphisms are function families
          ∏ ∏          ∑
                              𝐸(𝑖) × 𝐴(𝑗) × 𝐵(𝑘) ≅ 𝐴(𝑖′ ) × 𝐵(𝑗 ′ ) × 𝐸(𝑘′ )
                 +𝑘=𝑙 𝑖′ +
               +𝑗+
            𝑙 𝑖+         +𝑗 ′ +
                              +𝑘′ =𝑙

. We need to check that they are pointwise equal. Given 𝑓 ∶ 𝐴 → 𝐵 and 𝑔 ∶ 𝐶 → 𝐷,
the Day convolution morphism
                        ∏ ∏ ∑
               𝑓 ⊗𝑔 ∶                   𝐴(𝑗) × 𝐶(𝑘) → 𝐵(𝑗 ′ ) × 𝐷(𝑘′ )
                                +𝑘=𝑙 𝑗 ′ +
                             𝑙 𝑗+        +𝑘′ =𝑙

equals 𝑓 (𝑗) × 𝑔(𝑘) by picking 𝑗 ′ ≝ 𝑗, 𝑘′ ≝ 𝑘. By definition, we thus have

                    (𝜃𝐴 ⊗ 𝑖𝑑); (𝑖𝑑 ⊗ 𝜃𝐵 )(𝑙 = 𝑖 ++ 𝑗 ++ 𝑘)
                     = (swap𝐸(𝑖),𝐴(𝑗) ×𝑖𝑑𝐵(𝑘) ); (𝑖𝑑𝐴(𝑗) × swap𝐸(𝑖),𝐵(𝑘) )
                     = swap𝐸(𝑖),𝐴(𝑗)×𝐵(𝑘)
                     = 𝜃𝐴⊗𝐵 (𝑙 = 𝑖 ++ 𝑗 ++ 𝑘) .




                                                  45
