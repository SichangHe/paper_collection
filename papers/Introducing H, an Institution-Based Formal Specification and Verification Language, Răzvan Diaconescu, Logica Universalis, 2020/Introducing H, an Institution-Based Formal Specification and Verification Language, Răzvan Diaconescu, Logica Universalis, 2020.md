                                           Introducing H, an institution-based formal specification and
                                                              verification language
arXiv:1908.09868v1 [math.LO] 26 Aug 2019




                                                                                 Răzvan Diaconescu
                                                    Simion Stoilow Institute of Mathematics of the Romanian Academy, Bucharest, Romania




                                           Abstract
                                           This is a short survey on the development of the formal specification and verification
                                           language H with emphasis on the scientific part. H is a modern highly expressive
                                           language solidly based upon advanced mathematical theories such as the internalisation
                                           of Kripke semantics within institution theory.


                                           1. Introduction

                                               H is a language for formal specification and verification that has emerged out of a
                                           theoretical effort spread over a period of more than 25 years. It has been provisionally
                                           implemented as a prototype running system during 2017 – 2018 [8] and following this
                                           implementation a number of succesful case studies have been reported [8, 38]. H is
                                           designed as a two-component system:
                                                • Hspec – the specification language. This is an institution-based language in the
                                                  sense that is parameterised over a variety of base logic systems captured as insti-
                                                  tutions (in the sense of the institution theory of Goguen and Burstall [19]). The
                                                  role of the base logics refer to the specification of the data part of the system. For
                                                  the dynamics part, Hspec employs the essentials of modal logic. This design is
                                                  based upon the understanding that the essential ingredients of modal logic (both
                                                  at the syntactic and at the semantic level) are independent of the base level logic.
                                                  The fact that Hspec is parameterised by base logics gives it unparalleled specifi-
                                                  cation expressivity and power since the most appropriate logic for the data part
                                                  may be chosen. Moreover the list of base logics is open, any new logic may be
                                                  added when convenient.
                                                • Hver – a collection of verification tools and methods for specifications developed
                                                  with Hspec. At this moment Hver contains only one such method which is based
                                                  on translations to first order logic. However in the future we plan to extend Hver
                                                  with other methods and tools.
                                           A web page of H is currently maintained at


                                               Email address: Razvan.Diaconescu@imar.ro (Răzvan Diaconescu)


                                           Preprint submitted to Elsevier                                                       August 28, 2019
          http://imar.ro/˜diacon/forver/forver.html.
The H concept, the core of H represented by its scientific foundation, is based on devel-
oping an abstract Kripke semantics within the institution theory of Goguen and Burstall
[19]. This is the core of H, from which the vision of H had emerged, its development
being the result of a sustained mathematical effort reported in a series of papers from
which the most representative are [18, 14, 17]. In this way H may be a typical exam-
ple of a formal method that has emerged out of initially purely theoretically motivated
work.
    In this paper we survey the development of H, with emphasis on its most important
aspects. This goes as follows:
   1. In the first part, which is also the main part of the survey, we present the mathe-
      matical foundations of H and its basic design. As mentioned above this consists
      essentially of the internalisation of Kripke semantics in abstract institutions. This
      concept has been developed very gradually over many years and in our paper we
      will survey the most important moments of this development. I believe that pre-
      senting the H concept in this way has several benefits for the reader, including
      the possibility to understand the flow of ideas behind the H concept. This may
      be quite difficult if we chose to present only the end result of this rather complex
      process.
   2. The next section is dedicated to the current implementation of H. This is only a
      temporary implementation that is based on the Hets system [29]. In long term,
      our vision for H is to have an independent implementation.
   3. In the last section we discuss very briefly some case studies that have been for-
      mally specified and verified with H.
    The readership must be familiar with some very basic category theory concepts,
which are now quite commonly used in some areas of formal methods. Some familiar-
ity with institution theory and modal logic may be also quite helpful.

2. The H concept

    The broader scientific context of the H concept is the theory of institutions of
Goguen and Burstall [19]. The narrower context is the development of Kripke se-
mantics within abstract institutions [18, 14, 17]. In this section we first give a very
brief presentation of institution theory, and then survey the development process of the
institution-theoretic Kripke semantics.

2.1. Institutions
    The model theory oriented axiomatic approach by Goguen and Burstall to the no-
tion of a logical system [19] that is based on the notion of institution has started a line
of important developments of adequately abstract and general approaches to the foun-
dations of software specifications and formal system development (see [33]) as well as
a modern version of very abstract model theory (see [11]). One of the main original
motivations for introducing institution theory was to respond to the explosion in the


                                            2
population of logics in use in computing almost four decades ago, a situation that con-
tinues today perhaps at an accelerated pace. These days the concept of institution lies
at the foundations of several formal modern specification languages and environments
such as Maude [7], CASL [3] or CafeOBJ [16], Hets [29] etc. In the area of formal
specification and verification the contribution of the institution-theoretic approach to
modularity and heterogeneity are priceless. Let us recall the notorious concept of in-
stitution:
 An institution I = Sign I , Sen I , Mod I , |=I consists of
                                                

     • a category Sign I whose objects are called signatures,
     • a sentence functor Sen I : Sign I → Set defining for each signature a set whose
       elements are called sentences over that signature and defining for each signature
       morphism a sentence translation function,
     • a model functor Mod I : (Sign I )op → CAT defining for each signature Σ the
       category Mod I (Σ) of Σ-models and Σ-model homomorphisms, and for each
       signature morphism ϕ the reduct functor Mod I (ϕ),
     • for every signature Σ, a binary Σ-satisfaction relation |=IΣ ⊆ |Mod I (Σ)| ×
       Sen I (Σ),
such that for each morphism ϕ : Σ → Σ′ ∈ Sign I , the Satisfaction Condition

                M ′ |=IΣ′ Sen I (ϕ)(ρ) if and only if Mod I (ϕ)(M ′ ) |=IΣ ρ              (1)

holds for each M ′ ∈ |Mod I (Σ′ )| and ρ ∈ Sen I (Σ).

                                                   |=I
                                    Mod I (Σ)            Sen I (Σ)
                                                     Σ
                        Σ
                                        O
                       ϕ        Mod I (ϕ)                         Sen I (ϕ)
                                                             
                        Σ′          Mod I (Σ′ )          Sen I (Σ′ )
                                                  |=I
                                                    Σ′




    The literature (e.g. [11, 33]) shows myriads of logical systems from computing or
from mathematical logic captured as institutions. In fact, an informal thesis underlying
institution theory is that any ‘logic’ may be captured by the above definition. While
this should be taken with a grain of salt, it certainly applies to any logical system based
on satisfaction between sentences and models of any kind. In concrete institutions,
typically the signatures are structured collections of symbols, the sentences are induc-
tively defined from atoms by using sentence building operators, the sentence transla-
tions (along signature morphisms) rename symbols, the models interpret the symbols
of the signatures as sets and functions, the reducts “forget” interpretations of some
symbols, and the satisfaction is defined inductively on the structure of the sentences in
Tarski’s style [37].
    Here we refrain from presenting examples of logical systems captured as institu-
tions since the institution theory literature abounds of such examples. Instead let us just
point out that the process of defining particular logical systems as institutions is not nec-


                                             3
essarily a trivial one since one may have to reconsider and give a serious fresh thought
to concepts such as signature morphisms, variables, quantifiers, etc. This rethinking
of various concepts may have to do very much with the intended applications, such
as formal specification. For example, from the specification perspective the concept
of signature morphism has to be much more general than what is usually employed in
conventional logic, in order for the mathematics to work the variables require a kind of
qualifications that are inspired from the practice of specification languages, etc. Some
of these issues have been discussed in extenso in [13].

2.2. Kripke semantics in institutions
    The semantics for modal logics, known as Kripke semantics was introduced in [22].
The origin of the development of Kripke semantics in institutions – often refereed to
as ‘modalization of institutions’ – lies in some research undertaken within the group of
the late Professor Joseph Goguen at Oxford in the early nineties regarding institutions
for modal logics. First there was the realisation of the fact that the model amalgamation
properties in modal logic institutions are a direct consequence of the respective proper-
ties in the base logics, such as propositional or first order logic. From there it followed
the idea that each modal logic institution has an underlying simpler base institution and
that the Kripke models may be defined uniformly on the basis of the models in a base
institution. However it took over a decade to see the first paper on this published [18],
mainly due to a rather complicated refereeing process.
    In [18] – which may be considered the seminal paper for the H concept – we have
introduced the first version of Kripke semantics in abstract institutions first by consid-
ering a “base” institution I and then by building a “modal” institution HI on top of I.
This construction has several components:
   1. An extension of the syntax of I. While the signatures stay the same, new sen-
      tences are built from the sentences of I by iteration of sentences building opera-
      tors such as the usual Boolean operators, quantifiers, and modalities.
   2. Kripke models built from the models of I.
   3. The definition of a modal satisfaction relation between the Kripke models and
      the new sentences.
Now let us review these three components of the construction of HI one by one.

2.2.1. The syntax of HI
    For any signature Σ, the set Sen HI (Σ) of the Σ-sentences of the “modal” institu-
tion HI is the least set closed under the following operations:




                                            4
 • Sen I (Σ) ⊆ Sen HI (Σ);
 • ρ ⋆ ρ′ ∈ Sen HI (Σ) for any ρ, ρ′ ∈ Sen HI (Σ) and any ⋆ ∈ {∨, ∧, ⇒},
 • ¬ρ ∈ Sen HI (Σ), for any ρ ∈ Sen HI (Σ),
 • [λ](ρ1 , . . . , ρn ), hλi(ρ1 , . . . , ρn ) ∈ Sen HI (Σ),
   for any λ ∈ Λn+1 , ρi ∈ Sen HI (Σ), i ∈ {1, . . . , n};
 • (∀χ)ρ, (∃χ)ρ ∈ Sen HI (Σ), for any ρ ∈ Sen HI (Σ′ ) and χ : Σ → Σ′ ∈ D;

Some explanations are necessary:
• The first condition says that each sentence of the base institution becomes auto-
  matically a sentence of the “modal”institution.
• The second and the third conditions does the Boolean connectors on the sen-
  tences of the “modal” institution. Note that the sentences of the base institution
  may also involve Boolean connectors, in this case it is important to distinguish
  between the Boolean connectors at the base level and at the modal level since in
  general their effects may be differ.
• The fourth condition introduces modalities as sentences building operators. Here
  Λn means the set of modalities of arity n, which may be thought just as relation
  symbols. For now the modalities are not considered part of the signatures, they
  are rather fixed.
• Quantifiers are considered in the institution-theoretic manner, via designated sig-
  nature morphisms (see for example [11] for details). Conventional concrete
  quantifiers would correspond to those signature morphisms that are in fact ex-
  tensions of signatures with variables. So, not each signature morphisms may
  be used in quantifiers, those that are designated for such use form a so-called
  quantification space which is the D from the last condition above. This concept
  represents an axiomatic approach to quantifiers that considers coherence proper-
  ties with respect to translations along signature morphisms; it has been defined
  first in [12] and given this name in [14].
• Like with the Boolean connectors we have to carefully distinguish between quan-
  tifiers the level of HI and those that come with the sentences of the base institu-
  tion as their effects may differ.
• The general institution-theoretic feature of the quantifiers, namely that they sup-
  port higher-order quantification (up to what the concrete concept of signature
  supports) applies also here. So, depending on how we chose D we may have
  first order, or second order, or even higher order quantifiers.




                                          5
2.2.2. Kripke models
    The models of HI are Kripke models defined on the basis of the models of the base
institution I:

Given a signature Σ, a Kripke model (M, W ) consists of
     • a set |W | – called the set of the “possible worlds”;
     • for each λ ∈ Λn , a relation Wλ ⊆ |W |n ; and
     • a mapping M : |W | → |Mod I (Σ)|.

So, for each w ∈ W , Mw is a model of the base institution I. Moreover, W =
(|W |, (Wλ )λ∈Λ ) is called the Kripke frame of (M, W ).
     However in order for the quantifications to work properly, usually the models Mw
have to share something. For example in the concrete case of first order modal logic
it is quite common to require that the first order logic models Mw that are part of a
Kripke model share their underlying sets and the interpretations of the variables. At
the level of the abstract institutions this condition has been expressed in a general way
in [18] as

βΣ (Mw ) = βΣ (Mv ) for all w, v ∈ |W |.

where βΣ : Mod (Σ) → Dom(Σ) is a functor satisfying some rather mild technical
conditions (we omit them here).

2.2.3. The “modal” satisfaction
     The satisfaction relation that relate the syntax of the “modal institution” HI to
its semantics is defined by following the usual institution theoretic definitions and in
Tarski’s style by recursion on the structure of the sentences, the recursion base being
the satisfaction in the base institution I. For each Kripke model (M, W ) and each
w ∈ |W | we define a “local” satisfaction relation as follows:




                                            6
     • (M, W ) |=w ρ iff Mw |=I ρ; when ρ ∈ Sen I (Σ),
     • (M, W ) |=w ρ ∧ ρ′ iff (M, W ) |=w ρ and (M, W ) |=w ρ′ , and similarly for the
       other Boolean connectors;
     • (M, W ) |=w [λ](ξ1 , . . . , ξn ) iff for any (w, w1 , . . . , wn ) ∈ Wλ we have that
       (M, W ) |=wi ρi for some 1 ≤ i ≤ n.
     • (M, W ) |=w hλi(ξ1 , . . . , ξn ) iff there exists (w, w1 , . . . , wn ) ∈ Wλ such that
       and (M, W ) |=wi ξi for any 1 ≤ i ≤ n.
     • (M, W ) |=w (∀χ)ρ iff (M ′ , W ′ ) |=w ρ for any (M ′ , W ′ ) such that
       Mod (χ)(M ′ , W ′ ) = (M, W ),
     • (M, W ) |=w (∃χ)ρ iff (M ′ , W ′ ) |=w ρ for some (M ′ , W ′ ) such that
       Mod (χ)(M ′ , W ′ ) = (M, W ), and

Under these definition in [18] it has been proved that HI is an institution where
the satisfaction (M, W ) |= ρ is defined on the basis of the “local” satisfaction by
(M, W ) |=w ρ for all w ∈ |W |. Moreover, the adequacy of this construction has been
tested against some deep model theoretic results including a very general “modal” ul-
traproducts theorem and its compactness consequences. Although in [18] we have not
used multi-modalities (i.e. the relations from Λ) but instead used the more familiar ✷
and ✸, this difference is insignificant, being just a matter of form.
    Note that HI in fact represents a class of institutions rather than a single institu-
tion because of the several parameters involved in its construction. Besides the base
institution I of course, we also have the modalities Λ, the quantification space D and
the sharing functor β. From this perspective a notation such as HI(Λ, D, β) appears
as more appropriate, however this is rather heavy so we usually stick to the simpler
version when the involved parameters are clear.
    The usual modal logic institutions arise immediately as examples of HI. For in-
stance modal propositional logic arises when considering propositional logic as base
institution (eventually stripped of the Boolean connectors) and with D being trivial,
while first order modal logic arises when considering atomic first order logic as the
base institution (i.e. first order logic stripped off the Boolean connectors and off the
quantifiers) and D consisting of the extensions of the signatures with appropriate vari-
ables. However the potential of the construction of HI goes much beyond that of
known examples of modal logics because it frees modal logic from its conventional
base. For example, at the base level it is possible to have partial functions with various
kinds of sharing (an interesting one from an [17] would consider the sharing only of
the definition domains of the partial functions). A more intriguing example is given by
the possibility to iterate this construction for a number of times, obtaining hierarchical
modal logics.
    The construction of the “modal institution” of [18] is quite emblematic for all other
developments in the area and constitutes the very basis for Hspec as both the syntax
and the semantics of Hspec are based on this construction, but subject to some further


                                             7
additions that will be presented below.

2.3. Adding nominals
    An important development in the area of institution-theoretic Kripke semantics is
the extension of the theory of [18] with the ingredients of the so-called “hybrid logic”.
Hybrid logics [4] are a brand of modal logics that provides appropriate syntax for the
Kripke semantics in a simple and very natural way through the so-called nominals.
Historically, hybrid logic was introduced in [31] and further developed in works such
as [30, 2, 6] etc. The name “hybrid logics” was coined by Blackburn, but I consider this
an uninspired choice leading to confusions because of at least two reasons. On the one
hand this name does not suggest in any way the reality, namely that “hybrid logics”
is a sub-brand of the modal logics. In fact the difference between the two is rather
minor because technically it boils down only to a simple syntactic addition, whilst they
share the same semantics. On the other hand the term “hybrid” has a clear meaning in
ordinary language, which is difficult to relate to the corresponding brand of logics. In
spite of all these considerations, the terminology “hybrid logics” is already established
in the literature, and even the name H owes to it.
    The presence of nominals brings in several advantages from the point of view of
formal specification and verification, such as the possibility of explicit reference to spe-
cific states of the model and a better more uniform proof theory. All these specification
benefits have called for an extension of the original theory of [18], a first attempt in
this direction being [24]. That had been technically a rather straightforward enterprise,
which is briefly presented below.

2.3.1. Upgrading the signatures
    At the level of the signatures of HI we add the nominals, so after this addition a
signature consists of a pair (Nom, Σ) where Nom is a set (of nominal symbols) and Σ
is a signature of the base institution I. This had been a good moment to include also
the modalities Λ in the signatures, a move that is specification oriented. When speci-
fying dynamics of systems it is necessary to have user defined modalities. Therefore a
signature in HI is now a triple (Nom, Λ, Σ).

2.3.2. Upgrading the sentences
    The collection of the sentence building operators gets expanded with:


     • Nom ⊆ Sen HI (Nom, Λ, Σ);
     • @i ρ ∈ Sen HI (Nom, Λ, Σ) for any ρ ∈ Sen HI (Nom, Λ, Σ) and i ∈ Nom;

Then there is the issue of upgrading the quantification by allowing quantifications over
the nominals. For this we have to consider D as a quantification space for the up-
graded signatures, but one which does not have any effect on the modalities. Thus the
quantification building operators get upgraded to:



                                             8
     • (∀χ)ρ, (∃χ)ρ ∈ Sen HI (Nom, Λ, Σ), for any ρ ∈ Sen HI (Nom′ , Λ, Σ′ ) and
       χ : (Nom, Λ, Σ) → (Nom′ , Λ, Σ′ ) ∈ D;


2.3.3. Upgrading the semantics
    The upgrade of the concept of Kripke models is very simple, just interpret the new
syntactic entities by extending W with interpretations for the nominals. So for each
i ∈ Nom we have a designated element Wi ∈ |W |.

2.3.4. Upgrading the satisfaction relation
    This upgrade adds the semantics of the new building operators as follows:


     • (M, W ) |=w i iff Wi = w; when i ∈ Nom,
     • (M, W ) |=w @j ρ iff (M, W ) |=Wj ρ.

We can see that the upgrade of the construction of HI from [18] in the direction of
nominals is technically very straightforward. This is one of the reasons the paper [24]
may be considered as only a minor contribution to the general development of the H
concept. But there are other more serious reasons for this evaluation. Due to being a
conference paper – and therefore being quite rushed and suffering from severe space
limitations – the authors had to scrap some crucial features of the original construction
from [18], such as the sharing at the level of the Kripke models. One of the dramatic
consequences of this simplification – called the “free hybridisation” – was that the
quantification became nonfunctional, thus reducing a lot the specification power of
the formalism. However these shortcomings have been corrected in the journal paper
[14], which may be considered as the first paper addressing the extension of [18] with
nominals in a proper way.

2.4. More general constraints
    In [14] an ultimate very general axiomatic approach to the constraints on Kripke
models had been proposed. This approach captures a wide variety of constraints, such
as various sharing constraints or constraints on the shape of the Kripke frames (such as
reflexivity, transitivity, etc.). It is for instance more general and more accommodating
than the sharing constraints defined in [18]. Let us recall from [14]:

A constrained HI-model functor is a sub-functor Mod C ⊆ Mod HI such that it reflects
weak amalgamation for the designated pushout squares corresponding to the quantifi-
cation space DI at the level of the base institution I (that is obtained by “forgetting” the
nominals part from DHI ). The models in Mod C are called constrained HI-models.
We omit here detailed explanations concerning the technical condition on weak amal-
gamation as the interested reader may consult [14] or [17]. Informally, the meaning
of the reflection condition of is that in the case of the designated pushout squares used

                                            9
in quantifications the amalgamation of constrained models yields a constrained model.
The role of this condition, which is rather mild in the applications, is to ensure that
the constrained models support smoothly the quantifications. At the end we get a ‘sub-
institution’ of HI with constrained Kripke models that is denoted HI C .

2.5. Hspec and HI C
    The definition of Hspec sticks closely to the construction of HI C , being just a re-
alisation of this construction as a specification language. The following ideas underlie
the definition of Hspec:
    • The syntax of Hspec comes on two layers. The “upper” layer follows the def-
      inition of the signatures and of the sentences of HI C , which become Hspec
      declarations. The “lower” layer follows the definition of the signatures and of
      the sentences of the base institution I, which is the most important parameter
      the respective specification. In principle there is almost absolute freedom about
      the “lower” layer, in practice however we have to commit to something concrete,
      usually to something that already exists in the realm of current specification lan-
      guages. For example CASL [3] may be used in many situations because its
      underlying institution is a rather complex one which includes many logical fea-
      tures, such as Boolean connectors, first order quantifications, partial functions,
      etc.
    • The semantics of a Hspec specification is the class of the constrained HI C mod-
      els (Kripke models) that satisfy the axioms declared in the respective specifica-
      tion.
    • In Hspec, currently the constraints on the Kripke models are specified in two
      ways. Either by “rigidity” declarations for the syntactic entities (sorts, opera-
      tions, relations, etc.) that are meant to be interpreted uniformly across the base
      institution models in a Kripke model, or else by specific axioms in other cases
      (such as various properties of the Kripke frame, but not only). The constraint
      axioms do not appear in the specifications as they are part of the definition of all
      Kripke models and therefore are common to all specifications; they are declared
      when defining the respective logic/institution.
    Let us see how these ideas are realised in the case of a concrete example of a Hspec
specification. The following Hspec specification is that of a reconfigurable calculator
for natural numbers with a binary operation that in one state is sum and in the other
one is multiplication, an example which is discussed in [23].
spec Nat =
 logic : RigidCASL
 rigid sort Nat
 rigid op 0 : Nat
 rigid op suc : Nat -> Nat
 op X : Nat * Nat -> Nat
end

spec Calc =


                                           10
  hlogic : HRigidCASLC
  data Nat
  {
  nominals mult, sum
  modality shift : 2
  . mult \/ sum
  . @ sum
     : <shift> mult /\ [shift] mult
  . @ mult
     : <shift> sum /\ [shift] sum
  . @ mult : not sum
  . @ sum
     : forall m : Nat
         . X(m, 0) = m
  . @ sum
     : forall m, n : Nat
         . X(m, suc(n)) = suc (X(m, n))
  . @ mult
     : forallH m : Nat
      . forallH n : Nat
      . existsH x : Nat
      . existsH y : Nat
         . X(m, n) = x /\ X(m, suc(n)) = y /\ <shift> X(x, m) = y
 }
end

The first specification, at the level of the base institution, declares the data of the natural
numbers together with the binary operation that will change modes that can be either
interpreted as addition or as multiplication. This uses the CASL logic (essentially first
order logic with partial functions). Rigidity constraints are also specified at this stage in
order to prepare for the Kripke models in which the base models share their underlying
sets and some of the operations. The rigidity declarations do not have any semantic
effect at the level of the data (Nat), however they will have an effect at the level of
the hybridisation. This latter aspect, although does not introduce any error, is a little
“unclean”. It is not a kind of implementation shortcut, it rather comes from a small gap
in the theory. Currently, when building a hybridisation HI C , the signatures of the base
institution are preserved. Since rigidity of sorts and operations are in fact declarations
at the level of the base institution signatures, they have to be there already in order
to specify sharing constraints in the hybridisation. A possible solution to this is to go
more abstract about the signatures of HI C by specifying them abstractly together with
a projection functor to the signatures of I (the base institution) that may be subject to
some axioms, in the style of how frame and nominals extractions are defined in [15].
    The second specification is at the level of a hybridisation, which in this case is
HRigidCASLC (rigid sorts, rigid total functions and the domain of each rigid partial
function are interpreted uniformly). Its definition does not appear in this specification
as it resides in a library, being a predefined entity of Hspec. However in this particular
example we do not use any partial functions. The data Nat is imported and nominals
and the modality are declared. In the case of the modality note its arity 2. This is
the part that declares the respective HI C signature. Then follows a series of axioms
mainly regarding the dynamics of the system. For example, the first axiom says that
the Kripke frames have only two elements. Note the two levels of quantifiers, forall


                                              11
is at the level of the base institution while forallH and existsH are quantifiers at
the level of the hybridised institution. Because the base is a kind of fully fledged kind
of first order logic, its hybridisation HI C differs substantially from the classical first
order hybrid logics.

2.6. Encoding into first-order logic
    The current version of Hver contains only one method and tool that is based upon
a mathematical result that constitutes the main achievement in [17]. That result repre-
sents an extension of the traditional translation of modal logic to first order logic [39]
(for the hybrid variant [5]) to encodings of abstract hybridised institutions into first
order logic.
    That encoding uses the mathematical notion of comorphism [25, 35, 36, 26, 20],
which is an important concept of institution theory. From the perspective of the math-
ematical structure, comorphisms are just ‘homomorphisms of institutions’. So they are
mappings between institutions that preserve the mathematical structure of institutions.

An institution comorphism (Φ, α, β) : I → I ′ consists of
    1. a functor Φ : Sign → Sign ′ ,
    2. a natural transformation α : Sen ⇒ Φ; Sen ′ , and
    3. a natural transformation β : Φop ; Mod ′ ⇒ Mod
such that the following satisfaction condition holds

                          M ′ |=′Φ(Σ) αΣ (e) iff βΣ (M ′ ) |=Σ e

for each signature Σ ∈ |Sign|, for each Φ(Σ)-model M ′ , and each Σ-sentence e.
While the α represents the translation of the syntax, the β represents the translation of
the semantics. The satisfaction condition ensures the mutual coherence between these
translations.
     Although comorphisms generally express an embedding relationship between in-
stitutions, they can also be used for ‘encoding’ a ‘more complex’ institution I into a
‘simpler’ one I ′ . In such encodings the structural complexity cost is shifted to the
mapping Φ on the signatures, thus Φ maps signatures of I to theories of I ′ rather than
signatures. This is why in the literature these are sometimes [26, 20] called ‘theoroidal’
comorphisms. A theory in I is just a specification in I, i.e. a signature Σ plus a set E
of Σ-sentences. Technically speaking a ‘theoroidal’ comorphism is in fact an ordinary
comorphism when we replace the institution I ′ with the institution of its theories I ′th .
This is achieved through a general construction that can be applied to absolutely any
institution, in which the signatures of I ′th are the theories of I. The details of this
construction may be found in may places in the literature, such as in [11] (but under
the name of the institution of ‘presentations’).
     Due to the generality of the construction of HI C , including its parameters D and
the constraint sub-functor on models, the definition of the general encoding of HI C
into first order logic is technically rather complex. Therefore we omit it here (for
the details the interested reader has to refer to [17]) and instead we present briefly its


                                            12
main idea. The basis of the construction of the comorphism HI C → FOLth (where
FOL is the institution of first order logic in its many sorted form) is a given encoding
from the base institution to FOL, i.e. a comorphism I → FOLth . This is considered
abstractly, so it may vary, and in this way it constitutes the main parameter of this
construction. In practice these comorphisms may be well established translations. Then
under some technical conditions – mainly about quantifiers and model constraints – that
are commonly satisfied in the applications, the comorphism I → FOLth is “lifted” to
a comorphism HI C → FOLth .

2.6.1. How Hver works in principle
    Suppose that we have a specification in Hspec, which corresponds to a theory
(∆, E) in some HI C . Suppose that we have a property e that we have to check;
this means that we have to prove that E |=Σ e (which means that any model of E also
satisfies e). In order to establish E |= e we have to perform the following steps:
   1. Then we translate E and e by using the comorphism HI C → FOLth ; this yields
      Ẽ and ẽ in FOL. Usually Ẽ includes both the syntactic translation α(E) of
      E and the sentences of the theory Φ(∆). Obviously in the case of ẽ it is not
      necessary to include the latter sentences, so ẽ = α(e).
   2. If we had a theorem prover for FOL then this step would not be necessary. But
      unfortunately, at least up to my knowledge, all major first order logic theorem
      provers work with the unsorted version of first order logic. So we translate again
      both Ẽ and ẽ along a well known comorphism that encodes many sorted first
      order logic into unsorted first order logic (the details of this comorphism may be
      found for example in [11]). We thus arrive at Ē and ē.
   3. Now we employ a first order theorem prover and attempt to prove that Ē |= ē.
   4. If we are successful with the previous task then we may conclude that E |= e.
      However this move backwards is not straightforward. It holds as a consequence
      of an important property of comorphisms, namely that of conservativity:

       An institution comorphism (Φ, α, β) : I → I ′ is conservative when for each Σ-model
       M in I, there exists a Φ(Σ)-model M in I such that M = βΣ (M ).
      In [17] we have shown that under some technical conditions that are usually sat-
      isfied in the applications, the conservativity of the comorphism HI C → FOLth
      is inherited from the conservativity of the base comorphism I → FOLth . In or-
      der to complete the argument we still need that the encoding of FOL to unsorted
      first order logic is conservative, which indeed is.
In practice all the translations and the proofs are performed automatically using tools.
We will see more about this later on.

3. The current H implementation

3.1. ForVer and Hets
    In the year 2017 the author of this paper won funding for the project proposal
Formal Verification of Reconfigurable Systems (acronym: ForVer) under a new funding

                                          13
scheme of a Romanian government agency for funding of research that was dedicated
to experimental-demonstrative projects. That competition was highly competitive, with
a succes rate of about 5%, and the reviewers of the project proposals were selected from
the international scientific community. The goal of ForVer was to realise the long term
vision of H and of the science behind it as a running prototype. Then the project hired
Mihai Codescu for programming the prototype.
    The basic plan for this implementation of H was to rely on Hets [29]. Hets is a
tool for heterogeneous multi-logic specification and modeling of software systems and
ontology development. In both these fields, there are a large number of logics and lan-
guages in use, each better suited for a different task or providing a better support for a
different aspect of a complex system. Instead of trying to integrate the features of all
these logics into a single formalism, the paradigm of heterogenous multi-logic specifi-
cation is to integrate all logics by the means of a so-called Grothendieck construction
over a graph of logics and their translations (captured as institutions and institution
comorphisms, respectively). Thus, for each logic we can make use of its dedicated
syntax(es) and proof tools. The specifier has the freedom to choose the logic that suits
best the problem to be solved, offers best tool support and according to the degree of fa-
miliarity with a certain specification language. Hets provides an implementation of this
paradigm. Because of the multi-logic feature of H and also because of Hver is based
logic encodings (translations), Hets appeared as suitable for a smooth implementation
of a first prototype for H.

3.1.1. Grothendieck institutions
    As mentioned above the foundation of Hets are the so-called Grothendieck institu-
tions, which represents the ultimate theoretical answer to the problem of heterogeneous
multi-logic specification. Instead of presenting the rather intricate technicalities of this
concept let us review how it was developed. This theory has been initially developed
gradually within the context of the CafeOBJ [16], which was the first heterogeneous
specification language. A first attempt to address this heterogeneity institution the-
oretically was in [9]. Then the late Professor Martin Hoffman, while writing a re-
view for this publication, suggested a construction on institutions similar to the famous
construction by Alexandre Grothendieck on categories [21] originating from algebraic
geometry. In the year 2000 this suggestion was realised in [10], but that was based
on the original concept of homomorphism of institutions, the institution morphisms
of [19], which is somehow dual to the concept of institution comorphisms that was
discussed above. A few years later it was realised [27] that some crucial proporties of
Grothendieck institutions may be obtained more smoothly by the same construction but
based on institution comorphisms rather than institution morphisms. The Hets system
is based on the later version of Grothendieck institutions.

3.2. The Hets implementation of H
    A more detailed description of this implementation, may be found in [8]. Note that
this is an open implementation that supports further enhancements. Here we review
very briefly its main components:



                                            14
3.2.1. Syntactic support for the declarations of the parameters of the hybridisation
       process
    The considered parameters of the hybridisation are:
    • The base institution. This is specified by using its internal Hets name, based on
      a Hets qualification mechanism it is possible to select also a sub-institution of an
      institution already implemented in Hets.
    • The quantifier symbols. These may be nominal symbols or classes of symbols
      that are specific to the quantifications in the base institutions (such as constants,
      rigid constants, total constants).
    • The constraints on the Kripke models. These are specified through a fixed gram-
      mar that cover two different kinds of constraints: on the Kripke frames and on
      the interpretations of symbols in the local models.

The definitions of the hybridised logics are registered in such a way that allows new
additions of quantifications symbols and of constraints.

3.2.2. Generic method for generating new instances of the Hets class Logic
    The generation of new instances of the Hets class logic Logic is achieved on the
basis of the definitions of hybridisations of institutions by introducing Haskell poly-
morphic types for the signatures of the base institution, for the nominals, and for the
modalities.

3.2.3. Support for structured specifications
    The specification structuring operators of Hspec consist of unions, specification
translations alongs signature morphisms (which are symbols renaming), and colimits
of signatures. These are supported on the basis of a correspondence between the struc-
tured Hspec specifications and DOL [28], the structuring language supported in Hets.
This correspondence is embedded in the concrete definition of Hspec.

3.2.4. Support for Hver
     There is a special declarative syntax for this that takes as parameters the base the-
oroidal comorphism (from the base institution I to FOL) and the name of the respec-
tive hybridised logic HI C . A generic method analises these definitions and generates
Haskell code containing a corresponding new instance of the type class for Hets en-
codings. The compilation of this code makes the new encoding available for the veri-
fication process, where the translation Ē |= ē of a goal E |= e is passed to one of the
first order logic theorem provers of choice, such as SPASS [40], Vampire [32], E [34].

3.2.5. Support for new logics
    In order to cover in H the institutions that are presented as examples in [17] it was
necessary to implement in Hets the institution of the partial algebras with rigid symbols
and first order logic with rigid symbols (as a sub-institution of the former).




                                           15
4. H at work
    A number of succesful case studies with H have been already reported. In this
section we present very briefly a couple of them.

4.1. A steam boiler control
    The problem of this case study is a very notorious benchmark in formal methods
[1]. The case study with H has been reported in [8] and the H code is available at
          https://ontohub.org/forver/Sbcs.dol
    The H specification of the boiler control system illustrates almost all of features
of H. The base institution I is many-sorted first order logic, the hybridised institution
HI C has quantifications over nominals and rigid constants, and the constraints are
given by the sharing of the domains and of the interpretations of rigid symbols.
    The properties that have been verified include changes of modes when an event
takes place and that in all states of the system the expected functionality takes place. In
the H formalisation, the system has five modes (nominals) and nine events (modalities).

4.2. A bike-sharing system design
    This case study has been reported in [38] and the H code is available at
          https://ontohub.org/forver/BSS.dol
    It is based on a double hybridisation (hybridisation iterated twice) the base level for
the first level hybridisation being the (atomic fragment) of propositional logic.
    • The first level hybridisation has quantifications over nominals and one constraint,
      namely that the interpretation of one of the modalities (‘parent’) is a forest (a set
      of disjoint trees).
    • The second level of hybridisation admits quantifications over first level nominals
      (called “actors”) as well as quantifications over second level nominals (called
      “configurations”). There is a sharing constraint: the first level Kripke models in
      a second level Kripke model share the same underlying set of “actors”.
Since at the verification stage this modelling leads to some timeout problems (due to
a huge number of sentences obtained by the encoding in FOL), the first level of the
hybridisation has been encoded in an institution of relations.
   The first order theorem prover employed by this case study is SPASS.

5. H in the future
   There are several directions that I see with respect to the future evolution of H.
    • When conditions allow there should be a new implementation of H that is inde-
      pendent of Hets. The reasons for this are manifold. For example Hets is a rather
      big system and H relates only to a small part of Hets. Such big systems are prone
      to errors that may easily affect the functionality of H. Moreover H maintainers
      have little control on the evolution of Hets.

                                            16
    • Hver should be enhanced with more tools and methods. For example a direct
      tool based on proof systems at the level of hybridised institutions (so not by
      translation) would be an welcome enhancement of Hver.
    • Adding new base institutions and constraints to the current Hets implementation
      of H.
    • Some slight upgrades of the foundations may be necessary in order to acco-
      modate certain specification methodologies. For instance, we have already dis-
      cussed the issue of rigidity declarations at the level of the base institutions which
      may be solved by considering ‘projection’ functors from the categories of the
      signatures of the hybridised institutions to the categories of the signatures of the
      base institution.
    • More larger case studies should be developed with the aim to finally have H as
      an industrial tool.


References

[1] Abrial, J.-R., Börger, E., and Langmaack, H., editors (1996). Formal Methods for
   Industrial Applications – Specifying and Programming the Steam Boiler Control,
   volume 1165 of LNCS. Springer.
[2] Areces, C., Blackburn, P., and Delany, S. R. (2001). Bringing them all together.
   Journal of Logic and Computation, 11:657–669.
[3] Astesiano, E., Bidoit, M., Kirchner, H., Krieg-Brückner, B., Mosses, P., Sannella,
   D., and Tarlecki, A. (2002). CASL: The common algebraic specification language.
   Theoretical Computer Science, 286(2):153–196.
[4] Blackburn, P. (2000). Representation, reasoning, and relational structures: a hybrid
   logic manifesto. Logic Journal of IGPL, 8(3):339–365.
[5] Blackburn, P. and Seligman, J. (1995). Hybrid languages. Journal of Logic, Lan-
   guage and Information, 4(3):251–272.
[6] Braüner, T. (2011). Hybrid Logic and its Proof-Theory, volume 37 of Applied
   Logic Series. Springer.
[7] Clavel, M., Durán, F., Eker, S., Lincoln, P., Martı́-Oliet, N., Meseguer, J., and
   Talcott, C. (2007). All About Maude - A High-Performance Logical Framework,
   volume 4350 of Lecture Notes in Computer Science. Springer.
[8] Codescu, M. (2019). Hybridisation of institutions in Hets. In CALCO 2019, 8th
   Conference on Algebra and Coalgebra in Computer Science.
[9] Diaconescu, R. (1998). Extra theory morphisms for institutions: logical semantics
   for multi-paradigm languages. Applied Categorical Structures, 6(4):427–453. A
   preliminary version appeared as JAIST Technical Report IS-RR-97-0032F in 1997.

                                           17
[10] Diaconescu, R. (2002). Grothendieck institutions. Applied Categorical Struc-
   tures, 10(4):383–402. Preliminary version appeared as IMAR Preprint 2-2000,
   ISSN 250-3638, February 2000.
[11] Diaconescu, R. (2008). Institution-independent Model Theory. Birkhäuser.
[12] Diaconescu, R. (2010). Quasi-boolean encodings and conditionals in algebraic
   specification. Journal of Logic and Algebraic Programming, 79(2):174–188.
[13] Diaconescu, R. (2014). From universal logic to computer science, and back. In
   Ciobanu, G. and Méry, D., editors, Theoretical Aspects of Computing – ICTAC 2014,
   volume 8687 of Lecture Notes in Computer Science. Springer.
[14] Diaconescu, R. (2016). Quasi-varieties and initial semantics in hybridized insti-
   tutions. Journal of Logic and Computation, 26(3):855–891.
[15] Diaconescu, R. (2017). Implicit Kripke semantics and ultraproducts in stratified
   institutions. Journal of Logic and Computation, 27(5):1577–1606.
[16] Diaconescu, R. and Futatsugi, K. (1998). CafeOBJ Report: The Language, Proof
   Techniques, and Methodologies for Object-Oriented Algebraic Specification, vol-
   ume 6 of AMAST Series in Computing. World Scientific.
[17] Diaconescu, R. and Madeira, A. (2016). Encoding hybridized institutions into
   first order logic. Mathematical Structures in Computer Science, 26:745–788.
[18] Diaconescu, R. and Stefaneas, P. (2007). Ultraproducts and possible worlds se-
   mantics in institutions. Theoretical Computer Science, 379(1):210–230.
[19] Goguen, J. and Burstall, R. (1992). Institutions: Abstract model theory for spec-
   ification and programming. Journal of the Association for Computing Machinery,
   39(1):95–146.
[20] Goguen, J. and Roşu, G. (2002). Institution morphisms. Formal Aspects of Com-
   puting, 13:274–307.
[21] Grothendieck, A. (1963). Catégories fibrées et descente. In Revêtements étales et
   groupe fondamental, Séminaire de Géométrie Algébraique du Bois-Marie 1960/61,
   Exposé VI. Institut des Hautes Études Scientifiques. Reprinted in Lecture Notes in
   Mathematics, Volume 224, Springer, 1971, pages 145–94.
[22] Kripke, S. (1959). A completeness theorem in modal logic. Journal of Symbolic
   Logic, 24:1–15.
[23] Madeira, A. (2014). Foundations and techniques for software reconfigurability.
   PhD thesis, Universidades do Minho, Aveiro and Porto (Joint MAP-i Doctoral Pro-
   gramme).
[24] Martins, M.-A., Madeira, A., Diaconescu, R., and Barbosa, L. (2011). Hybridiza-
   tion of institutions. In Corradini, A., Klin, B., and Cı̂rstea, C., editors, Algebra and
   Coalgebra in Computer Science, volume 6859 of Lecture Notes in Computer Sci-
   ence, pages 283–297. Springer.

                                            18
[25] Meseguer, J. (1989). General logics. In Ebbinghaus, H.-D. et al., editors, Pro-
   ceedings, Logic Colloquium, 1987, pages 275–329. North-Holland.
[26] Mossakowski, T. (1996). Different types of arrow between logical frameworks.
   In auf der Heide, F. M. and Monien, B., editors, Proc. ICALP 96, volume 1099 of
   Lecture Notes in Computer Science, pages 158–169. Springer Verlag.
[27] Mossakowski, T. (2002). Comorphism-based Grothendieck logics. In Diks, K.
   and Rytter, W., editors, Mathematical foundations of computer science, volume
   2420 of Lecture Notes in Computer Science, pages 593–604. Springer.
[28] Mossakowski, T., Codescu, M., Neuhaus, F., and Kutz, O. (2015). The distributed
   ontology, modeling and specification language – dol. In Koslow A., B. A., editor,
   The Road to Universal Logic. Birkhauser, Cham.
[29] Mossakowski, T., Maeder, C., and Lütich, K. (2007). The Heterogeneous Tool
   Set. In Lecture Notes in Computer Science, volume 4424, pages 519–522.
[30] Passy, S. and Tinchev, T. (1991). An essay in combinatory dynamic logic. Infor-
   mation and Computation, 93(2):263–332.
[31] Prior, A. N. (1967). Past, Present and Future. Oxford University Press.
[32] Riazonov, A. and Voronkov, A. (2002). The design and implementation of VAM-
   PIRE. AI Commun., 15(2–3):91–110.
[33] Sannella, D. and Tarlecki, A. (2012). Foundations of Algebraic Specifications
   and Formal Software Development. Springer.
[34] Schulz, S. (2013). System description: E 1.8. In Proceedings of the 19th con-
   ference on Logic Programming and Autamated Reasoning (LPAR), volume 8312 of
   LNCS, pages 477–483.
[35] Tarlecki, A. (1996). Moving between logical systems. In Haveraaen, M., Owe,
   O., and Dahl, O.-J., editors, Recent Trends in Data Type Specification, volume 1130
   of Lecture Notes in Computer Science, pages 478–502. Springer.
[36] Tarlecki, A. (2000). Towards heterogeneous specifications. In Gabbay, D. and
   van Rijke, M., editors, Proceedings, International Conference on Frontiers of Com-
   bining Systems (FroCoS’98), pages 337–360. Research Studies Press.
[37] Tarski, A. (1944). The semantic conception of truth. Philos. Phenomenological
   Research, 4:13–47.
[38] Ţuţu, I., Chiriţă, C. E., Lopes, A., and Fiadeiro, J. L. (forthcoming (2019)). Log-
   ical support for bike-sharing system design. In SG65@FM 2019, Porto, Portugal,
   October 7–11, 2019, volume 11865 of Lecture Notes in Computer Science. Springer.
[39] van Bentham, J. (1988). Modal Logic and Classical Logic. Humanities Press.
[40] Weidenbach, C., Dimova, D., Fietzke, A., Kumar, R., Suda, M. ., and Wis-
   chnewski, P. (2009). SPASS version 3.5. In Automated Deduction, volume 5663
   of LNCS, pages 140–145.


                                            19
