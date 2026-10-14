Generically Automating Separation Logic by Functors,
Homomorphisms, and Modules
QIYUAN XU, Nanyang Technological University, Singapore
DAVID SANAN, Singapore Institute of Technology, Singapore
ZHE HOU, Griffith University, Australia
XIAOKUN LUAN, Peking University, China
CONRAD WATT, Nanyang Technological University, Singapore
YANG LIU, Nanyang Technological University, Singapore
Foundational verification considers the functional correctness of programming languages with formalized
semantics and uses proof assistants (e.g., Coq, Isabelle) to certify proofs. The need for verifying complex pro-
grams compels it to involve expressive Separation Logics (SLs) that exceed the scopes of well-studied auto-
mated proof theories, e.g., symbolic heap. Consequently, automation of SL in foundational verification relies
heavily on ad-hoc heuristics that lack a systematic meta-theory and face scalability issues. To mitigate the gap,
we propose a theory to specify SL predicates using abstract algebras including functors, homomorphisms, and
modules over rings. Based on this theory, we develop a generic SL automation algorithm to reason about any
data structures that can be characterized by these algebras. In addition, we also present algorithms for auto-
matically instantiating the algebraic models to real data structures. The instantiation works compositionally,
reusing the algebraic models of component structures and preserving their data abstractions. Case studies on
formalized imperative semantics show our algorithm can instantiate the algebraic models automatically for
a variety of complex data structures. Experimental results indicate the automatically instantiated reasoners
from our generic theory show similar results to the state-of-the-art systems made of specifically crafted rea-
soning rules. The presented theories, proofs, and the verification framework are formalized in Isabelle/HOL.
CCS Concepts: • Theory of computation → Separation logic; Program verification; Automated rea-
soning; Abstraction; Logic and verification; • Computing methodologies → Algebraic algorithms.
Additional Key Words and Phrases: Separation Logic, automatic rule generation, subtyping rules, abstract
algebras, transformation of refinements
ACM Reference Format:
Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu. 2025. Generically Automating
Separation Logic by Functors, Homomorphisms, and Modules. Proc. ACM Program. Lang. 9, POPL, Article 67
(January 2025), 41 pages. https://doi.org/10.1145/3704903

1 Introduction
Foundational verification [13] involves verifying the functional correctness of concrete programs
based on formal semantics using a proof assistant, in which both the inference and the proofs
are certified. Therefore, foundational verification relies on a smaller trust base and produces more
Authors’ Contact Information: Qiyuan Xu, Nanyang Technological University, Singapore, xu@qiyuan.me; David Sanan,
Singapore Institute of Technology, Singapore, david.miguel@singaporetech.edu.sg; Zhe Hou, Griffith University, Brisbane,
Australia, z.hou@griffith.edu.au; Xiaokun Luan, Peking University, Beijing, China, luanxiaokun@pku.edu.cn; Conrad Watt,
Nanyang Technological University, Singapore, conrad.watt@ntu.edu.sg; Yang Liu, Nanyang Technological University, Sin-
gapore, and China-Singapore International Joint Research Institute (CSIJRI), Guangzhou, yangliu@ntu.edu.sg.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and
the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses,
contact the owner/author(s).
© 2025 Copyright held by the owner/author(s).
ACM 2475-1421/2025/1-ART67
https://doi.org/10.1145/3704903

                                 Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:2                                       Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


trustworthy results than other formal methods. These advantages have promoted the rapid devel-
opment of the field in recent years [23, 47, 59, 63–65].
   Foundational semantics often include complex and low-level resource models that involve alias-
ing or references [27, 39, 45, 74], in which case Separation Logic (SL) has shown to be an effective
verification method [54]. In a typical workflow of an SL-based foundational verification, the pro-
cess has the following steps: (1) extract SL entailments (i.e., implications between SL formulas) that
imply program correctness (e.g., by a predicate transformer [31, 64]), (2) then extract pure proof
obligations (e.g., first-order logic formulas) to entail the validity of the entailments, and finally, (3)
the pure proof obligations are sent to Automated Theorem Provers (ATPs) [1, 59, 64] for solving.
   Step 2 above is often the bottleneck of the automation. Despite an abundance of techniques
for such extraction [2, 4, 20, 21, 29, 43, 44, 51, 52, 62, 67], their adoption in foundational verifica-
tion faces three issues: (1) Existing techniques focus on a small fragment of SL, usually variants
of symbolic heap, based on a simplified memory model having limited support to pointer arith-
metic [4, 8, 34, 62, 68]. The use of SL in foundational verification can easily exceed this fragment by
either unsupported connectives [37, 66], abstract models like partial commutative monoids [11, 18],
or deeply formalized semantics involving real pointer arithmetic [49]. (2) Most techniques support
only linked data structures like linked lists and trees [20, 43, 44, 57], whereas complex software
heavily uses advanced data structures like arrays, dynamic arrays, and hash tables. (3) In founda-
tional verification, scalability relies on abstractions that encapsulate complicated concrete details
and provide abstract layers to ease the verification [24, 25, 40, 61]. Predicates are essential means to
provide abstraction, whereas existing techniques rely on unfolding predicates, which can destroy
such abstractions, blow up expressions, and finally cause scalability limitations.
   The absence of solutions addressing these issues has motivated researchers to develop approaches
for automating expressive SLs in foundational verification. Among them, RefinedC [64] represents
a milestone. Based on Iris, it proposes a type-based specification language and a logic programming-
based reasoning framework, providing automation that is on par with non-foundational methods.
   While state-of-the-art tools like RefinedC have made significant progress, they still face limita-
tions in providing automation support for user-defined data structures. In particular, automation
support on user structures is limited to the generation of folding and unfolding rules. Further com-
plex transformations depend on manually crafted typing rules that constitute ad-hoc reasoning
procedures. Depending on the complexity of the structures involved, crafting the typing rules de-
mands substantial expertise, coupled with extensive creative input and additional proving efforts.
   We can see examples in non-trivial transformations such as subtyping List(𝑇 ) <: List(𝑈 ), which
is ubiquitous when containers have different element types; spliting and concatenating array slices,
e.g., from int[1..9] to int[1..5] ∗int[6..9], which are essential in divide-and-conquer algorithms like
Quicksort; or separating container abstractions along element components, e.g., from Array(𝑇 ∗𝑈 )
to Array(𝑇 ) ∗ Array(𝑈 ), useful when components are owned by different program modules. Con-
sidering these examples, there is an absence of a systematic theory that enables a generic mecha-
nism supporting the automatic generation of reasoning rules for data structures and modalities.
   In this work, borrowing the satisfaction operator from Hybrid Logic [5, 30], we present an inter-
pretation of SL predicates from the perspective of data refinement (§4). This interpretation reveals
properties of SL predicates (Table 1) that correspond to laws of abstract algebras, capable of mod-
eling many data structures and modalities (§ 6). From these predicate properties, it is possible to
automatically instantiate the necessary rules for the aforementioned transformations, providing an
approach for the automatic generation of non-trivial1 data structure reasoning rules, discharging
users from providing manual specifications and additional proofs when proving certain properties

1 meaning transformations that are not for folding or unfolding definitions



Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                 67:3


   Table 1. Algebraic properties identified by the paper, over which our generic SL automation is built.
 Property                                   Description*
  TF denotes Functor of SL implications, useful for modeling data containers (e.g., List). It is the
       key to subtyping like List(𝑇 ) <: List(𝑈 ), which allows a reasoning process to shift from
       the space of containers into the space of elements.
  SH Homomorphism of predicate operators over ∗, useful to extract components of elements in
       a container and to split container abstractions along the separation of element components.
  SA denotes Associativity of module-like predicate operators, useful to model concatenation
       of paths to resources, such as a file path or the path to a member field in a nested record.
  SD Scalar Distributivity of module-like predicates is useful for modeling split and concatena-
       tion of data structure slices, like array slices.
  IE denotes Identity Elements used to specify the abstractions representing empty.
  Tr denotes Transitivity and equivalences between abstractions.
 * Predicate and refinement relations are interchangeably used as they are the same thing in our system.


over data structures. In particular, we can automate the process for any aggregated data structure,
where users only need to manually specify and prove base datatypes, as is the case for integer
datatypes in programming languages.
   The instantiated transformation rules are powerful enough to constitute the core of an SL rea-
soner for an generic imperative heap language, as demonstrated in §10. Specifically, this reasoner
first extracts SL entailments that entail the functional correctness of a given program, using a
typical 𝑤𝑝 or 𝑠𝑝 transformer (§ 7.2). Then, it reduces the decision problems of the entailments
to transformations between predicates (i.e., subtypings in terms of RefinedC) using bi-abduction
(§8.2.1, §8.2.2). Finally, it applies the automatically instantiated transformation rules to extract ver-
ification conditions that entail the transformations’ validity (§ 6). The verification conditions are
sent to SMT solvers or handed to users. Consequently, we present a generic SL reasoner over the
abstractions of the algebras listed in Table 1. It generally supports any data structure or modalities
that satisfy (even some of) the algebras.
   We evaluate this reasoner through 10 widely-used data structures and 592 lines of programs in
formalized semantics in Isabelle/HOL. In most cases, our reasoner is able to prove the properties
with less human intervention compared with state-of-the-art foundational verification tools.
   In summary, the main contributions of this paper are summarized as follows:
   (1) A set of algebraic properties that captures general transformations between refinements of
       data structures. Transformation rules for specific data structures are instantiated automati-
       cally once the properties of the structures are proven.
   (2) A generic SL reasoner that: a) Uses rule instances of the algebraic properties for automatic
       inference of SL entailments in a compositional manner minimizing the need for unfolding; b)
       Allows automatic proving of the algebraic properties of predicates, minimizing even further
       manual proving from users.
   (3) The Isabelle/HOL formalization for the algebraic properties and the SL reasoner.
   (4) The evaluation of our reasoner and its formalization on a battery of examples involving
       10 data structures in a total of 592 lines of 8 programs.

2 Motivating Example
Let us consider verifying a two-line program { alloc_data (l); free_data (l) }, which necessarily
requires a non-trivial transformation, or in RefinedC, a manually proven typing rule.

                             Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:4                                       Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


struct list { void* data; list* next; };                                  void free_data (list* l) {
void* safe_alloc (size_t s) {                                               if (l) { free (l->data); free_data (l->next); }
   void* ret = alloc (s);                                                 }
   if (ret) return ret; else abort ();                                    void verify_this (list* l) {
}
                                                                            alloc_data (l);
void alloc_data (list* l) {
                                                                            free_data (l);
   if (l) { l->data = safe_alloc(42); alloc_data (l->next); }
}                                                                         }
    Before delving into the example, we first introduce a refinement-based assertion language sim-
plified from recent refinement-type approaches [59, 64, 65] — we use SL predicate to represent data
refinement. We interpret a predicate 𝑇 as a refinement relation that relates concrete constructs (like
memory heaps) to abstractions. Specifically, 𝑇 (𝑥) defines the set of concrete constructs that refine
abstraction 𝑥. The notion of refinement type in the recent works [59, 64, 65] corresponds to SL
predicates in our theory. To emphasize this correspondence and to be intuitive, we introduce the
notation 𝑥 ⦂ 𝑇 to abbreviate predicate application 𝑇 (𝑥), i.e., 𝑥 ⦂ 𝑇 ≜ 𝑇 (𝑥).
    Returning to the above example, we fix a predicate 𝑇 to represent the refinement relation of the
data in the linked list. The refinement of the linked list itself is then specified by a predicate operator
List𝑎 : Predicate → Predicate, where 𝑎 denotes the address of the list. Predicate application 𝑙 ⦂
List𝑎 (𝑇 ) relates the memory heap of a concrete linked list to a sequence 𝑙, where the 𝑖 th element of 𝑙
is the abstraction of the data in the 𝑖 th linked node. To account for potentially null data pointers, we
use the sum operator (𝑇 + Null) to represent a data entry that may be null2 . There is an implication
𝑥 ⦂ 𝑇 −→ (inj1 𝑥) ⦂ (𝑇 + Null) that corresponds to a subtyping: the type of non-null pointers is a
subtype of the nullable pointer type.
    The safe_alloc always returns a non-null pointer, while a null pointer is a valid argument of free.
Therefore, we stipulate the postcondition of routine alloc_data to be 𝑙 ⦂ List𝑎 (𝑇 ), representing a list
of non-null pointers. For routine free_data, we stipulate its precondition to be 𝑙 ′ ⦂ List𝑎 (𝑇 + Null),
representing a list of nullable pointers. Given the specifications, if we want to verify { alloc_data
(l); free_data (l)) }, we must prove an SL entailment 𝑙 ⦂ List𝑎 (𝑇 ) −→ 𝑙 ′ ⦂ List𝑎 (𝑇 + Null), where
𝑙 ′ = List.map(inj1 ) (𝑙). This entailment corresponds to a subtyping: a list of non-null pointers is a
subtype of a list of nullable pointers. Importantly, while this subtyping seems intuitive, it cannot
be derived automatically by state-of-the-art tools such as RefinedC.
    Taking RefinedC as an example, non-null pointers are specified by type &own while nullable
pointers are by optional(&own, null). The system provides subtyping &own <: optional(&own, null).
However, it cannot derive subtyping list(&own ) <: list(optional(&own, null)). This limitation stems
from RefinedC’s restricted automation support for user-defined types. While RefinedC automati-
cally derives (un)folding rules for user-defined types, it does not generate subtyping rules for them.
This gap necessitates manual intervention to prove the subtyping rule of user-defined types. This
task requires extensive expertise in understanding the internal implementation of RefinedC and
in proving SL lemmas using Iris, therefore presenting a significant challenge for non-experts.
    In our system, a mechanism is provided for deriving subtyping rules of user-defined predicate
operators automatically. Continuing the example, the subtyping rule of List is represented as
      ∀𝑒 ∈ set(𝑙). 𝑒 ⦂ 𝑇 −→ 𝑓 (𝑒) ⦂ 𝑈        map(𝑓 )([𝑙 1, · · ·, 𝑙𝑛 ]) ≜ [𝑓 (𝑙 1 ), · · ·, 𝑓 (𝑙𝑛 )] is the mapper of lists;
  𝑙 ⦂ List𝑎 (𝑇 ) −→ map(𝑓 ) (𝑙) ⦂ List𝑎 (𝑈 ) set([𝑙 1, · · ·, 𝑙𝑛 ]) ≜ {𝑙 1, · · ·, 𝑙𝑛 } gives the set of elements in a list
The premise assumes that when the refinement relation of an element changes from 𝑇 to 𝑈 , its
abstraction changes from 𝑒 to 𝑓 (𝑒). The conclusion then shows that the refinement relation of the
2 The sum operator is generally defined as (inj
                                                  1 𝑥 ) ⦂ (𝑇1 + 𝑇2 ) ≜ 𝑥 ⦂ 𝑇1 and (inj2 𝑦) ⦂ (𝑇1 + 𝑇2 ) ≜ 𝑦 ⦂ 𝑇2 where inj1 is the
left injection while inj2 is the right.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                        67:5

                                           bi-Abductive     Solved    Solver §6                Algebra Properties §5
Programs    Specifications                Transformation      by
            wp-transformer (§7.2)       Problems (Def. 6.2)        Ad-hoc Rules §6.2       Functor SepHom       Module
             or other methods            §8.2.2     Reduce                                Instantiate (§6.5)
                                                                     Instantiated Rules
 Decision Problems of Reduce bi-Abductive Entailment                                               Templates §6.5
   SL Entailments               Problems (Def. 8.2)                   Fallbacks §6.3
                      §8.2.1                                                               TF SH SDL SDR SAL SAR ...

                            Fig. 1. Overall workflow of our Separation Logic reasoner.

entire list can change from List𝑎 (𝑇 ) to List𝑎 (𝑈 ), and its abstraction changes accordingly from 𝑙 to
map(𝑓 )(𝑙). In essence, this rule specifies how to transform the refinement of a linked list based on
the transformation of the refinements of its elements.
   The target proof goal 𝑙 ⦂ List𝑎 (𝑇 ) −→ 𝑙 ′ ⦂ List𝑎 (𝑇 + Null) is then derived from this subtyping
rule, the known fact ∀𝑒. (𝑒 ⦂ 𝑇 −→ (inj1 𝑒) ⦂ (𝑇 + Null)), and a proof obligation 𝑙 ′ = map(inj1 ) (𝑙).
   This subtyping rule reflects the covariant functor property of List over the SL implication (−→).
Indeed, the rule is instantiated from an instance Functor(List, map, set) of a generally defined
algebraic property Functor(𝐹, 𝑚, 𝑑) specifying that predicate operator 𝐹 is a functor over (−→),
           Functor(𝐹, 𝑚, 𝑑) ≜ for any 𝑓 , 𝑥 and predicate 𝑇 ,𝑇 ′ ,
                                                                                                                     (TF)
               𝑥 ⦂ 𝐹 (𝑇 ) −→ 𝑚(𝑓 )(𝑥) ⦂ 𝐹 (𝑇 ′ ) holds if ∀𝑒∈𝑑 (𝑥). 𝑒 ⦂ 𝑇 −→ 𝑓 (𝑒) ⦂ 𝑇 ′ holds.
Assuming 𝐹 represents some data container, then 𝑚 represents the mapper of (the abstraction of)
the container, e.g., list mapper; 𝑑 (𝑥) gives the element domain of (the abstraction of) a container
instance 𝑥. This property then provides a generic mechanism for generating subtyping rules for
any predicate operators satisfying the property.
   If a predicate operator 𝐹 is defined as a composition of other functors, say 𝐹 ≜ 𝐺 1 ◦ · · · ◦ 𝐺𝑛 , our
reasoner is able to derive 𝐹 ’s functor property automatically by Functor composition — Functors
𝐺 1, 𝐺 2 yield 𝐺 1 ◦ 𝐺 2 as a functor.
                   Functor(𝐺 1, 𝑚 1, 𝑑 1 )     Functor(𝐺 2, 𝑚 2, 𝑑 2 )
                                                                       (Functor Composition),
                                Ð 1 ◦ 𝐺 2, 𝑚 1 ◦ 𝑚 2, 𝑑 1 >>= 𝑑 2 )
                         Functor(𝐺
where (𝑑 1 >>= 𝑑 2 ) ≜ (𝜆𝑥 . 𝑒 ∈𝑑1 (𝑥 ) 𝑑 2 (𝑒)) is the monadic bind of sets. This composition principle
allows us to prove the algebraic properties of a composite predicate operator without unfolding
its component operators. For recursively defined predicate operators, our reasoner applies an in-
duction tactic, as elaborated later in §9.

3 Overview
This work aims to increase the automation of program verification by adding automated support
to user-defined data structures. Such support comes from two different aspects: automated rule
generation and automated SL entailment reasoning by means of the automated generated rules.
   By identifying algebraic structures encoding refinement transformation scenarios between pred-
icates, presented in § 5, it is possible to design a generic reasoner that has the knowledge of the
scenarios and can automate refinement of any data structure satisfying the algebraic axioms in the
scenarios. This approach leads to a systematic method for automating our SL logic (§4).
   To facilitate this, the reasoner centers around a designed family of problems called bi-abductive
Transformation Problems (bi-TPs). These problems are formulated to represent refinement transfor-
mations of the form 𝑥 ⦂ 𝑇 −→ 𝑓 (𝑥) ⦂ 𝑈 , allowing direct application of the algebraic properties.
   Illustrated in Fig. 1, our reasoning process unfolds in two stages: (1) introduced in §7 and §8 a SL
reasoner reduces program verification problems to bi-TPs; (2) introduced in §6 a TP-Solver applies
rules automatically generated based on algebraic properties of predicates to solve the bi-TPs. The
algorithms for proving the algebraic properties of a given predicate are provided in §9.

                                    Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:6                                     Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


4 A Separation Logic with a Perspective of Data Refinement
The theory of our Separation Logic (SL) automation algorithm is based on interpreting SL predi-
cates as data refinement relations. Before presenting the algorithm, we have to first formalize how
this interpretation is established on an SL semantics, and we also formalize this SL semantics. For
brevity, this SL formalization is simplified while the complete version is left to Appendix A.
   The assertion language of our SL is parameterized by a finite set P of SL predicates, and a first-
order logic FOL with equality. Let 𝑤, 𝑥, 𝑦, 𝑧, 𝑡 range over terms in FOL, 𝛼, 𝛽 over variables in FOL,
and 𝑇 , 𝑈 over SL predicates P. The assertion language F of our SL includes all standard connectives
plus a satisfaction operator () borrowed from Hybrid Logic [5, 30] (originally denoted by @).
F ∋ 𝜙,𝜓 F ⊤ | ⊥ | emp | 𝑇 (𝑥) | ¬𝜙 | 𝜙 ∗ 𝜓 | 𝜙 ∧ 𝜓 | 𝜙 ∨ 𝜓 | 𝜙 −∗ 𝜓 | 𝜙 → 𝜓 | ∃𝛼 . 𝜙 | ∀𝛼 . 𝜙 | 𝑡  𝜙
         | any other formula in FOL, e.g., 𝑥 = 𝑦.
Ranged over by 𝐹, 𝐺, the set P∗ of SL predicate operators is defined as an inductive set consisting of
all predicates in P, all maps from P to P∗ , and all maps from FOL terms to P∗ . This notion of predicate
operator will be used later in formalizing algebraic properties. The logic is first-order and does not
support quantifying over predicates. Predicate operators are defined in the meta-logic.
   The semantics of an SL is conventionally defined upon a partial algebra known as Separation
Algebra (SA). There are various ways in the literature to define the notion of SA. We follow a widely
accepted one [11] that defines an SA as a Partial Commutative Monoid (PCM), written (𝑆, •, 𝜖) for
a carrier set 𝑆, a partial binary operation (•) over 𝑆, and an identity element 𝜖 ∈ 𝑆.
   Fix a domain of discourse O and an interpretation function [[−]] from FOL terms to O. Fix a
PCM A = (𝑆, •, 𝜖) such that O ⊆ 𝑆. Elements in 𝑆 are called worlds and ranged over by 𝑤.
   The semantics of formulas in F is defined by forcing relation (|=), a binary relation between
𝑆 and F. Note that (|=) should be parameterized by the interpretation function that maps every
predicate to a subset of O, but we omit it here. For 𝑤 ∈ 𝑆, and 𝜙,𝜓 ∈ F,
     𝑤 |= 𝜙 ∗ 𝜓 holds iff there exists 𝑤 1, 𝑤 2 such that 𝑤 = 𝑤 1 • 𝑤 2 and both 𝑤 1 |= 𝜙, 𝑤 2 |= 𝜓 hold.
     𝑤 |= 𝜙 −∗𝜓 holds iff for any 𝑤 ′ such that 𝑤 ′ |= 𝜙 holds and 𝑤 ′ • 𝑤 is defined, 𝑤 ′ • 𝑤 |= 𝜓 holds.
     𝑤 |= (𝑡  𝜙) holds for any term 𝑡 iff the world represented by term 𝑡 satisfies formula 𝜙, i.e.
     [[𝑡]] |= 𝜙 holds. Essentially, () internalizes the forcing relation (|=) into the object logic.
The definition of (|=) on predicate application and other connectives is standard and omitted here.
   Definition 4.1 (Validity). We say an SL formula 𝜙 holds, iff ∀𝑤 ∈ 𝑆. 𝑤 |= 𝜙 holds.
   Definition 4.2 (Type notation). 𝑥 ⦂ 𝑇 ≜ 𝑇 (𝑥), for any term 𝑥 and predicate 𝑇 .
   Definition 4.3 (Data Refinement implied by SL predicates). Iff 𝑤 |= 𝑥 ⦂ 𝑇 holds, we say 𝑤 refines
𝑥, or equivalently, 𝑥 is an abstraction of 𝑤, w.r.t. refinement relation 𝑇ˆ ≜ {(𝑤, 𝑥) | (𝑤 |= 𝑇 (𝑥))}.
   𝑥 ⦂ 𝑇 relates a set of concrete constructs to one specific abstract object 𝑥. In order to relate
concrete constructs to a set of abstract objects, one can use (∃), e.g., ∃𝑎. 𝑎 ⦂ 𝑇 ∧ 𝑎 ∈ 𝐴 which
specifies concrete constructs that refine one of the abstract objects in set 𝐴.
   Turning back to (), there are two reasons to introduce (). First, it allows us to specify stepwise
refinement, 𝑥 ⦂ (𝑈 ;𝑇 ) ≜ (∃𝑦. 𝑦 ⦂ 𝑈 ∧ (𝑦  𝑥 ⦂ 𝑇 )). Second, it allows us to use and express a
predicate as a refinement relation 𝑇ˆ (𝑤, 𝑥) ≜ (𝑤  𝑇 (𝑥)) within the logic. This explicit expression
of refinement relation is essential. For example, assuming 𝑎 ↦→ 𝑣 is an assertion specifying a
singleton heap which has value 𝑣 at address 𝑎, the predicate 𝑥 ⦂Ref 𝑎 (𝑇 ) ≜ ∃𝑣. (𝑎 ↦→ 𝑣) ∧ (𝑣  𝑥 ⦂𝑇 )
specifies a memory object at address 𝑎 that has a value refining 𝑥 w.r.t. 𝑇 .
   We require the PCM A of our SL to encompass all elements in the domain of discourse O and
all concrete constructs including memory heaps and program values. This allows us to write our

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                 67:7


refinement relations as regular SL predicates to abstract any constructs we want. Examples include
the definition of stepwise refinement 𝑇 ; 𝑈 above (which requires 𝑦 in the PCM), and the definition
of Ref which requires 𝑣 in the PCM.
   We use SL predicates to build refinements because (1) we want to use (∗) to separately and com-
positionally specify the refinement of each component, e.g. Ref 𝑎 (𝑇 ∗𝑈 ) for a reference containing
two components; (2) instead of introducing a different relational separating conjunction to express
the 𝑇 ∗ 𝑈 in Ref 𝑎 (𝑇 ∗ 𝑈 ), we want every connective and operator to stay in a uniform category so
that we could use a uniform automation mechanism for all of them, e.g., the same mechanism can
be used to reason about both Ref 𝑎 (𝑇 ∗ 𝑈 ) and (𝑇 ∗ 𝑈 ).
   This big PCM A may seem cumbersome, and its group operation is hard to define when elements
belonging to different sorts are involved. In implementations, we adopt a many-sorted variant SL
through a shallow embedding into typeclasses provided by the underlying proof assistants. This
allows us to define the group operation individually for each sort of PCM. This many-sorted version
is left to Appendix B while the paper’s theoretical discussion only considers the single monolithic
PCM, for the sake of simplicity.
   Returning to unifying SL predicates and refinement relations, we axiomatically declare a predi-
cate Id to represent identity refinement. Semantically, 𝑤 |= (𝑥 ⦂ Id) holds iff 𝑤 = 𝑥.
   By means of Id, we can represent any relation 𝑅 as an SL predicate 𝑅(𝑥)    ˆ    ≜ (∃𝑤 . 𝑤 ⦂Id∧𝑅(𝑤, 𝑥)).
Together with 𝑇ˆ that represents an SL predicate as a refinement relation, it unifies SL predicates and
refinement relations. Indeed, 𝑇ˆˆ = 𝑇 and 𝑅ˆˆ = 𝑅 ; this hat operator is a bijection between SL predicates
and refinement relations. It unifies SL predicates and refinement relations, thus justifying

Notation. Every predicate and its corresponding refinement relation are denoted by the same symbol.

  By interpreting SL predicates as refinement relations, implications between SL predicate appli-
cations have a meaning of transformations between refinement relations: Formula 𝑥 ⦂𝑇 −→ 𝑦 ⦂ 𝑈
represents that any semantic construct that refines 𝑥 w.r.t. 𝑇 also refines 𝑦 w.r.t. 𝑈 .

5 Algebras of Refinement Transformations
Our methodology is based on the assumption that typical SL entailments in real program verifica-
tion are synthesizable from finite algebraic scenarios of refinement transformations.
   This algebraic approach also offers an additional advantage: it allows us to abstract away con-
crete details, reveal common properties among diverse constructs, and then automate them gener-
ically in one unified mechanism. As an example, which we will explore later, fractional permission
has the same model, module-like structure, as array slices. Without an algebraic approach, it is hard
to recognize that fractional permissions and array slices can be automated by one mechanism.
   While our implementation explores additional algebraic structures, we present three key alge-
braic structures in this section. Their axioms are defined in Fig. 2. Parameterized over the axioms
of the algebras, a generic SL reasoner is presented in the subsequent sections of the paper.

5.1   Transformation Functor (TF)
Functor (from Fig. 2) captures the essence of covariant subtyping. Assume predicate operator 𝐹 (·)
represents a data container such as List(·). Property Functor(𝐹, m, 𝑑) specifies how to transform the
refinement of the container’s elements. Specifically, consider a data container instance represented
by 𝑥 ⦂𝐹 (𝑇 ). Predicate 𝑇 represents the refinement relation of the container’s elements. The domain
of the elements in the instance is represented by 𝑑 (𝑥). Besides, if a function 𝑓 can transform
the abstractions of the elements from refinement relation 𝑇 to refinement relation 𝑈 , then the
abstraction of the container instance can be transformed from 𝑥 ⦂ 𝐹 (𝑇 ) to m (𝑓 ) (𝑥) ⦂ 𝐹 (𝑈 ).

                             Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:8                                     Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


  Functor(𝐹, m, 𝑑) ≜ for any 𝑇 , 𝑈 , 𝑓 , and 𝑥 ∈ dom(m (𝑓 )),
     𝑥 ⦂ 𝐹 (𝑇 ) −→ m (𝑓 )(𝑥) ⦂ 𝐹 (𝑈 ) holds if ∀𝑒∈𝑑 (𝑥). 𝑒 ⦂ 𝑇 −→ 𝑓 (𝑒) ⦂ 𝑈 holds.
                                                                                                            (TF)
 SepHom(𝐹, 𝑠, 𝑧) ≜ for any 𝑇 , 𝑈 , any 𝑥 ∈ dom(𝑧) and 𝑦 ∈ dom(𝑠),
    𝑥 ⦂ (𝐹 (𝑇 ) ∗ 𝐹 (𝑈 )) −→ 𝑧 (𝑥) ⦂ 𝐹 (𝑇 ∗𝑈 ) and 𝑦 ⦂ 𝐹 (𝑇 ∗𝑈 ) −→ 𝑠 (𝑦) ⦂ (𝐹 (𝑇 ) ∗ 𝐹 (𝑈 )) hold.
                                                                                                           (SH)
 The following properties are parameterized by a ring-like algebra (S , +, ·) called scalar algebra.
 Assoc(𝐹, 𝑔, ℎ) ≜ for any 𝑇 , any 𝑛, 𝑚 ∈ S , 𝑥 ∈ dom(𝑔𝑛,𝑚 ) and 𝑦 ∈ dom(ℎ𝑛,𝑚 )
    𝑥 ⦂ 𝐹𝑛 (𝐹𝑚 (𝑇 )) −→ 𝑔𝑛,𝑚 (𝑥) ⦂ 𝐹𝑛·𝑚 (𝑇 ) and 𝑦 ⦂ 𝐹𝑛·𝑚 (𝑇 ) −→ ℎ𝑛,𝑚 (𝑦) ⦂ 𝐹𝑛 (𝐹𝑚 (𝑇 )) hold.
                                                                                                            (SA)
  Dist(𝐹, 𝑠, 𝑧) ≜ for any 𝑇 , any 𝑛, 𝑚 ∈ S , 𝑥 ∈ dom(𝑠𝑛,𝑚 ) and 𝑦 ∈ dom(𝑧𝑛,𝑚 ),
     𝑥 ⦂ 𝐹𝑛+𝑚 (𝑇 ) −→ 𝑠𝑛,𝑚 (𝑥) ⦂ (𝐹𝑛 (𝑇 )∗𝐹𝑚 (𝑇 )) and 𝑦 ⦂ (𝐹𝑛 (𝑇 )∗𝐹𝑚 (𝑇 )) −→ 𝑧𝑛,𝑚 (𝑦) ⦂ 𝐹𝑛+𝑚 (𝑇 ) hold.
                                                                                                           (SD)
  SUnit(𝐹, 𝑔, ℎ) ≜ for any 𝑇 , identity scalar 𝜖 ∈ S , any 𝑥 ∈ dom(𝑔𝜖 ) and 𝑦 ∈ dom(ℎ𝜖 ),
    𝑥 ⦂ 𝐹𝜖 (𝑇 ) −→ 𝑔𝜖 (𝑥) ⦂ 𝑇 and 𝑦 ⦂ 𝑇 −→ ℎ𝜖 (𝑦) ⦂ 𝐹𝜖 (𝑇 ) hold.
                                                                                                            (S1)
  SZero(𝐹, 𝐷) ≜ 𝑥 ⦂ 𝐹 0 (𝑇 ) ←→ emp holds for any 𝑇 , any zero scalar 0 ∈ S and 𝑥 ∈ 𝐷.                      (S0)

Fig. 2. Algebras of common refinement transformations. Notation 𝑥 ⦂𝑇 ≜ 𝑇 (𝑥) denotes predicate application.


   In an expressive refinement-based assertion language, predicates and predicate operators (types
and type operators) are usually hierarchically combined, forming a structure reminiscent of nested
“Matryoshka dolls”. Functor enables a reasoning process to systematically “unpack” these nested
structures layer by layer, reducing reasoning problems about containers to problems about their
elements, recursively until reaching atoms. Continuing the example in § 2, in order to prove the
transformation (subtyping) from 𝑙 ⦂ List𝑎 (𝑇 ) to 𝑙 ′ ⦂ List𝑎 (𝑈 ), Functor indicates that it suffices to
show that any element 𝑒 ⦂ 𝑇 in the list can transform to 𝑒 ′ ⦂ 𝑈 for some 𝑒, 𝑒 ′ constrained by 𝑙, 𝑙 ′ .
   Additionally, we call this property Functor because of its categorical correspondence. Given a
category C where its objects are all SL predicates and its morphisms between two objects 𝑇 , 𝑈
are partial functions 𝑓 such that ∀𝑥 ∈ dom(𝑓 ). 𝑥 ⦂ 𝑇 −→ 𝑓 (𝑥) ⦂ 𝑈 , a Functor(𝐹, m, 𝑑) describes a
functor in C, where predicate operator 𝐹 is its object function and m is its morphism function (𝑑
plays a minor role restricting the domains of morphisms).
   Regarding generality, Functor is ubiquitous in data structures. In particular, most data containers
are Functor instances. Furthermore, many modalities and connectives are also Functors, such as
the operator Ref. 𝑥 ⦂ Ref 𝑎 (𝑇 ) specifies a memory object at address 𝑎 has a value refining 𝑥 w.r.t 𝑇 .
It satisfies Functor(Ref 𝑎 , 𝜆𝑥 .{𝑥 }, 𝜆𝑓 .𝑓 ). Another example is permission modality 𝑥 ⦂ 𝑛 ⨸𝑇 , which
claims ownership of an 𝑛 fraction of an object 𝑥 ⦂ 𝑇 , for a fraction 0 ≤ 𝑛 ≤ 1. When 𝑛 = 1, it
represents total permission that permits read and write; when 0 < 𝑛 < 1, it permits read-only
access; when 𝑛 = 0, 𝑥 ⦂ 0 ⨸ 𝑇 equals empty. It has a property Functor(𝑛⨸, 𝜆𝑥 . {𝑥 }, 𝜆𝑓 . 𝑓 ). As one
more example, consider the Later modality ⊲ seen in many impredicative SLs [1, 37]. Its predicate
version 𝑥 ⦂ ⊲𝑇 ≜ ⊲(𝑥 ⦂ 𝑇 ) satisfies Functor(⊲, 𝜆𝑥 . {𝑥 }, 𝜆𝑓 . 𝑓 ) because of the so-called mono rule
(𝜙 −→ 𝜓 ) −→ (⊲𝜙 −→ ⊲𝜓 ). Indeed, any modality that has such a mono rule is a Functor.

5.2    Separating Homomorphism (SH)
A separating homomorphism, given by SepHom(𝐹, 𝑠, 𝑧), specifies that the predicate operator 𝐹
is homomorphic over the predicate separating conjunction (∗). Recall the predicate separating
conjunction (𝑥, 𝑦)⦂(𝑇 ∗𝑈 ) ≜ (𝑥 ⦂𝑇 )∗(𝑦⦂𝑈 ). Assuming that 𝑥 ⦂𝐹 (𝑇 ∗𝑈 ) represents a data container,
then 𝑇 ∗ 𝑈 represents that every element in the container contains two components abstracted
respectively by 𝑇 and 𝑈 . SepHom(𝐹, 𝑠, 𝑧) allows us to split the abstraction of the container along
the separation between the two element components and also merge the two divided parts back.
The split operation 𝑠 transforms 𝑥 ⦂ 𝐹 (𝑇 ∗ 𝑈 ) to 𝑠 (𝑥) ⦂ (𝐹 (𝑇 ) ∗ 𝐹 (𝑈 )). The merge operation 𝑧

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                    67:9


transforms (𝑥, 𝑦) ⦂ (𝐹 (𝑇 ) ∗ 𝐹 (𝑈 )) to 𝑧 (𝑥, 𝑦) ⦂ 𝐹 (𝑇 ∗ 𝑈 ). Connecting to category theory, a Functor
that also satisfies SepHom is a lax-monoidal functor in the category constructed in § 5.1, taking
predicate separation conjunction as the tensor product.
   SepHom is useful when partitions for different element components of a data container are
referenced by different structures in a program. For example, in our case studies, 𝑥 ⦂ Ref addr (𝑇 )
is separating-homomorphic by SepHom(Ref addr , 𝜆𝑥 . 𝑥, 𝜆𝑥 . 𝑥). It allows us to split a reference to a
composite memory object into references to each of its components. To illustrate, recall that we
use {a:𝑇 } ∗ {b: 𝑈 }, abbreviated as {a:𝑇 , b: 𝑈 }, to represent a record with two fields. The SepHom
of Ref implies transformation (𝑥, 𝑦) ⦂ Ref addr {a:𝑇 , b: 𝑈 } −→ 𝑥 ⦂ Ref addr {a:𝑇 } ∗ 𝑦 ⦂ Ref addr {b: 𝑈 },
which allows us to split one reference to the record into two references to each field of the record.
Note, the SepHom of Ref does not hold on concrete memory models. Our system supports basic
fictional separation to lift the concrete address-to-bytes memory model to an abstract one based on
a map from records with fields to values with permissions, on which addr ↦→ {a: 𝑢, b: 𝑣 } = addr ↦→
{a: 𝑢} ∗ addr ↦→ {b: 𝑣 } holds and therefore the SepHom of Ref holds. These are detailed in §10.1.
   Regarding generality, SepHom is also ubiquitous. Ref 𝑎 is an example already introduced above.
Permission modality and Later modality are also examples. We have SepHom(𝑛⨸, 𝜆𝑥 . 𝑥, 𝜆𝑥 . 𝑥) and
SepHom(⊲, 𝜆𝑥 . 𝑥, 𝜆𝑥 . 𝑥). Another example is array, satisfying SepHom(Array𝑎 , unzip, zip), where
[𝑥 1, · · ·, 𝑥𝑛 ] ⦂ Array𝑎 (𝑇 ) ≜ (𝑥 1 ⦂ Ref 𝑎 𝑇 ) ∗ · · · ∗ (𝑥𝑛 ⦂ Ref 𝑎+𝑛−1 𝑇 ) is defined as a collection of array
elements connected by (∗). List operations zip([𝑎 1, · · ·, 𝑎𝑛 ], [𝑏 1, · · ·, 𝑏𝑛 ]) ≜ [(𝑎 1, 𝑏 1 ), · · ·, (𝑎𝑛 , 𝑏𝑛 )],
and unzip[(𝑎 1, 𝑏 1 ), · · ·, (𝑎𝑛 , 𝑏𝑛 )] ≜ ([𝑎 1, · · ·, 𝑎𝑛 ], [𝑏 1, · · ·, 𝑏𝑛 ]) are defined as usual. The example in
§6.6 illustrates how to utilize the SepHom of arrays in practice.
   For more advanced data structures, SepHom might seem uncommon due to the presence of
control structures that cannot be easily split and shared between divided abstractions. For instance,
consider a dynamic array, which typically includes a length record. When attempting to separate
dynamic-array(𝑇 ∗ 𝑈 ) into dynamic-array(𝑇 ) and dynamic-array(𝑈 ), a challenge arises: which
separated part should own the length record? This issue suggests that a straightforward refinement
like dynamic-array(𝑇 ∗ 𝑈 ) may not be separable. However, a solution exists through the fiction
of disjointness [19, 35]. This technique allows us to 1) freeze the state of the common structure
and 2) share constant copies of this frozen state between divided abstractions For example, in
our dynamic array case, we could freeze the length and provide a copy of this constant length to
each separated part of the array. Conclusively, it is possible to construct separating-homomorphic
refinements for most data containers.

5.3   Modules over Rings
The next two algebraic properties are inspired by the theory of modules over rings. A left module-
like structure over a ring-like structure (S , +, ·) comprises a group-like structure (G, ✼) and a
scalar multiplication • : S × G → G. For any 𝑛, 𝑚 ∈ S and 𝑥, 𝑦 ∈ G, a module-like structure
may satisfy, (1) Scalar associativity, (𝑛 · 𝑚) • 𝑥 = 𝑛 • (𝑚 • 𝑥); (2) Scalar distributivity, (𝑛 + 𝑚) • 𝑥 =
(𝑛 • 𝑥) ✼ (𝑚 • 𝑥); (3) Distributivity over group operation, 𝑛 • (𝑥 ✼ 𝑦) = (𝑛 • 𝑥) ✼ (𝑛 • 𝑦); (4) Scalar
zero, 0 • 𝑥 = 𝜖 for 0 ∈ S and 𝜖 ∈ G; (5) Scalar identity, 1 • 𝑥 = 𝑥 for 1 ∈ S .
   Let us consider a predicate operator 𝐹𝑛 parameterized by a scalar 𝑛 belonging to some ring-like
partial algebra (S , +, ·) called scalar algebra, ranged over by 𝑛, 𝑚, 𝛿. Construct a left module-like
structure over (S , +, ·), such that the carrier G is the set of all SL predicates, the group operation
( ✼) is predicate separating conjunction (∗), the group identity is predicate Emp(𝑥) ≜ emp ∧𝑥 = (),
and the scalar multiplication (•) is the predicate operator 𝐹 . Based on this module-like construc-
tion, properties SA, SD, S1, S0 represent the laws of scalar associativity, scalar distributivity, iden-
tity, and scalar zero, respectively; the SepHom that specifies transformations between 𝐹𝑛 (𝑇 ∗ 𝑈 )
and 𝐹𝑛 (𝑇 ) ∗ 𝐹𝑛 (𝑈 ), corresponds to the third axiom, Distributivity over the group operation.

                                Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:10                                          Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


   Unlike Functor and SepHom, the module-like properties do not have a general interpretation in
terms of data refinement. Instead, various refinements and modalities with distinct meanings can
be specified by the language of modules. We present some examples in the following discussion.
(1) Permission modality 𝑛 ⨸ 𝑇 satisfies both Assoc(⨸, 𝜆𝑛 𝑚 𝑥 . 𝑥, 𝜆𝑛 𝑚 𝑥 . 𝑥), Dist(⨸,
    𝜆𝑛 𝑚 𝑥 . (𝑥, 𝑥), 𝜆𝑛 𝑚 (𝑥, 𝑥). 𝑥), SUnit(⨸, 𝜆𝜖 𝑥 . 𝑥, 𝜆𝜖 𝑥 . 𝑥), and SZero(⨸, ⊤), where 𝜆(𝑥, 𝑥). 𝑥 de-
    notes a partial map from (𝑥, 𝑥) to 𝑥 for any 𝑥. The scalar algebra is a partial algebra obtained
    by restricting elements in the rational field to interval (0, 1]. However, if we extend the domain
    of permission to allow it to be locally greater than 1, e.g., to allow 12 ⨸ (2 ⨸ 𝑇 ) = 1 ⨸ 𝑇 , (the
    similar relaxation is also seen in [17]), then the scalar algebra extends to the semiring of non-
    negative rationals, and the module of ⨸ extends to a semimodule. Transformations of 𝑛 ⨸ 𝑇
    then can be perfectly described by the laws of semimodule as follows:
     • Scalar Distributivity, 𝑥 ⦂ (𝑛 +𝑚) ⨸𝑇 ←→ (𝑥 ⦂𝑛 ⨸𝑇 ) ∗ (𝑥 ⦂𝑚 ⨸𝑇 ), for sharing of ownership.
     • Scalar Associativity, 𝑥 ⦂ 𝑛 ⨸ 𝑚 ⨸ 𝑇 ←→ 𝑥 ⦂ (𝑛 · 𝑚) ⨸ 𝑇 states that 𝑛 proportion of 𝑚
       proportion of ownership equals 𝑛 · 𝑚 proportion of ownership.
     • The property of identity states unit permission can be omitted, 𝑥 ⦂ 1 ⨸ 𝑇 ←→ 𝑥 ⦂ 𝑇
     • The property of zero states zero permission means empty, 𝑥 ⦂ 0 ⨸ 𝑇 ←→ emp.
(2) Let 𝑥 ⦂ Path𝑛 𝑇 represent a subtree 𝑥 ⦂ 𝑇 located at path 𝑛. Let the scalar algebra (S , ·)
    be the monoid of path concatenation and leave the scalar addition unspecified. Path satis-
    fies Assoc(Path, 𝜆𝑛 𝑚 𝑥 . 𝑥, 𝜆𝑛 𝑚 𝑥 . 𝑥) and SUnit(Path, 𝜆𝑛 𝑥 . 𝑥, 𝜆𝑛 𝑥 . 𝑥). The properties charac-
    terize the path concatenation and empty path. This predicate operator Path is useful in cases
    where a tree abstraction is used, e.g., file systems. Particularly, in our case studies, the memory
    model of a nested record whose fields can be another nested record is represented by such a
    tree, whose edge labels are field names and leaves are non-aggregate values like integers. We
    use 𝑥 ⦂ Path𝑛 𝑇 to represent a field 𝑛 that has a value refining 𝑥 w.r.t. 𝑇 . The scalar 𝑛 repre-
    sents a dot-connected path (e.g., a.b.c) that locates a member field in a nested record (e.g.,
    {a: {b: {c: int}, d: int}, e: int}).
(3) Let [𝑙𝑖 , · · ·, 𝑙𝑖+𝑘 −1 ] ⦂ Slice [𝑖,𝑖+𝑘 ) 𝑇 specify the slice of an array 𝑙 that starts from index 𝑖 and
    has length 𝑘. Let the scalar algebra (S , +) be the partial semigroup of interval concatenation
    (defined as follows) and leave the multiplication unspecified.
                     [𝑖, 𝑗) + [ 𝑗, 𝑘) ≜ [𝑖, 𝑘),        and      [𝑖, 𝑗) + [ 𝑗 ′, 𝑘) is undefined if 𝑗 ≠ 𝑗 ′ .
    We also stipulate that any [𝑖, 𝑖) is a zero element and any [𝑖, 𝑖 + 1) is an identity element of
    the semigroup. Predicate operator Slice satisfies Dist(Slice, split, cat) and SZero(Slice, {[]})
    where, assuming 𝑙 ⦂ Slice [𝑖,𝑖+𝑘 ) 𝑇 maintains an invariant such that the length of 𝑙 equals 𝑘,
          cat [𝑖,𝑗 ),[ 𝑗 ′ ,𝑘 ) (𝑙 1, 𝑙 2 ) ≜ if 𝑗 = 𝑗 ′ then the concatenation of 𝑙 1, 𝑙 2 else undefined.
          split [𝑖,𝑗 ),[ 𝑗 ′ ,𝑘 ) (𝑙) ≜ if 𝑗 = 𝑗 ′ then ([𝑙 0, · · ·, 𝑙 𝑗 −𝑖 −1 ], [𝑙 𝑗 −𝑖 , · · ·, 𝑙𝑘 −𝑖 −1 ]) else undefined.
    The scalar distributivity of array slices represents the concatenation and splitting of sub-slices.
    The property zero then specifies predicate application 𝑙 ⦂Slice [𝑖,𝑖 ) 𝑇 equals empty because the in-
    terval is empty. Slice also has an extended identity property, SUnit′ (Slice, Ref, 𝜆[𝑥]. 𝑥, 𝜆𝑥 . [𝑥])
    if we extend the definition S1 to define,
           SUnit′ (𝐹, 𝐺, 𝑓 , 𝑔) ≜ for any 𝑇 , identity scalar 𝜖 ∈ S , any 𝑥 ∈ dom(𝑓𝜖 ) and 𝑦 ∈ dom(𝑔𝜖 ),
                                                                                                                                  (S1’)
              𝑥 ⦂ 𝐹𝜖 (𝑇 ) −→ 𝑓𝜖 (𝑥) ⦂ 𝐺𝜖 (𝑇 ) and 𝑦 ⦂ 𝐺𝜖 (𝑇 ) −→ 𝑔𝜖 (𝑦) ⦂ 𝐹𝜖 (𝑇 ) hold.
    The identity property states how to unwrap a slice into a single reference object when the slice
    specifies exactly one element.
                                                         ∗
(4) Finite separating quantifier {𝑥𝑖 }𝑖 ∈𝐼 ⦂ 𝑖 ∈𝐼 𝑇𝑖 ≜ (𝑥𝑖 1 ⦂ 𝑇𝑖 1 ∗ · · · 𝑥𝑖𝑛 ⦂ 𝑇𝑖𝑛 ) for 𝐼 = {𝑖 1, · · ·, 𝑖𝑛 }, is
    the fourth example of module-like predicate operators, where the scalar 𝐼 is a finite set. The
    addition between the scalars is the disjoint union ⊔, and every singleton set is a scalar identity.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                 67:11


      The zero is the empty set.     ∗                    ∗
                                             satisfies Dist( , disjoin, join) where disjoin𝐼,𝐽 ({𝑥𝑘 }𝑘 ∈𝐼 ⊔𝐽 ) ≜
      ({𝑥𝑘 }𝑘 ∈𝐼 , {𝑥𝑘 }𝑘 ∈ 𝐽 ) and join(𝑥, 𝑦) ≜ 𝑥 ⊔ 𝑦.

6 Utilizing the Algebraic Abstractions to Solve Transformation Problems
In this section, we introduce a generic SL reasoner designed to apply rules for transforming predi-
cates from one form to another, directly mirroring the transformations described by the algebraic
properties introduced in Section 5.
   The reasoning rules are automatically instantiated from templates leveraging the generality pro-
vided by their parameters, which are algebraic properties. Collectively, they form a generic rea-
soning procedure capable of automating the reasoning for any predicate satisfying the specified
properties. This endows our reasoner with a high degree of generalization capability.

6.1     Transformation Problem (TP) and bi-Abductive Transformation Problem (bi-TP)
Recall that formula 𝑥 ⦂ 𝑇 −→ 𝑓 (𝑥) ⦂ 𝑈 represents a transformation between refinements: any
concrete construct refining 𝑥 w.r.t 𝑇 also refines 𝑓 (𝑥) w.r.t 𝑈 . Based on this interpretation, we
define a Transformation Problem (TP) as:
  Definition 6.1 (TP). Given predicates 𝑇 , 𝑈 and a set 𝐷, a Transformation Problem TP(𝑇 , 𝑈 , 𝐷)
looks for a pair (𝜃, 𝑓 ), where 𝜃 is an FOL formula that represents proof obligation, and 𝑓 is a
function such that ∀𝑥 ∈𝐷. 𝑥 ⦂ 𝑇 −→ 𝑓 (𝑥) ⦂ 𝑈 holds if (𝜃 ∧ 𝐷 ⊆ dom(𝑓 )) holds.
Intuitively, given any concrete construct 𝑤 refining abstraction 𝑥 w.r.t. refinement relation 𝑇 , TP
looks for the abstraction of 𝑤 under (another) refinement relation 𝑈 . Formula 𝜃 is the proof obli-
gation that entails the validity of the transformation. It constitutes a part of the final output of our
SL reasoner — the proof obligation of program correctness.
   However, a limitation is that TP(𝑇 , 𝑈 , 𝐷) only considers predicates 𝑇 , 𝑈 that specify the same
partitions of program states. In practice, we often encounter situations where predicates specify
different partitions of states or different resource instances, and in that case, the partitions may
only partially overlap. For example, consider three resources 𝐴, 𝐵, 𝐶. Let predicate 𝑇 specify 𝐴, 𝐵,
while 𝑈 specify 𝐵, 𝐶. The transformation from 𝑇 to 𝑈 then cannot be described by TP, as it would
be trivially unsolvable. This motivates us to introduce a variant of TP, inspired by [10].
   Definition 6.2 (bi-TP). Given SL predicates 𝑇 , 𝑈 and a set 𝐷 of terms, a bi-abductive Transforma-
tion Problem bi-TP(𝑇 , 𝑈 , 𝐷) looks for a quadruple (𝜃, 𝑓 , 𝑍, 𝑅), for an FOL formula 𝜃 , a function 𝑓
and two predicates 𝑍, 𝑅, such that (𝜃, 𝑓 ) is a solution of TP(𝑇 ∗𝑍, 𝑈 ∗𝑅, 𝐷).
  Definition 6.3. The operator (∗) between predicates is defined as (𝑇 ∗ 𝑍 )(𝑥, 𝑧) ≜ 𝑇 (𝑥) ∗ 𝑍 (𝑧).
 Compared to TP, bi-TP additionally looks for two predicates, frame 𝑅 and anti-frame 𝑍 , which
represent the resources covered by 𝑇 but not by 𝑈 (in our example, 𝐴) and the resources covered
by 𝑈 but not by 𝑇 (in our example, 𝐶). Intuitively, anti-frame 𝑍 represents the missing resources
not presented in 𝑇 but claimed by 𝑈 ; frame 𝑅 the remaining resources of 𝑇 after extracting 𝑈 from
it. A solution (𝜃, 𝑓 , 𝑍, 𝑅) of bi-TP(𝑇 , 𝑈 ) then states, in order to transform 𝑇 to 𝑈 , some additional
resources (specified by) 𝑍 are required; the transformation also leaves 𝑅 as a remainder. Symbols
𝜃 and 𝑓 retain their meanings from TP.
    For example, let 𝑥 ⦂ {a:𝑇 } specify a record with one field 𝑎 whose value refines 𝑥 w.r.t. 𝑇 . Also let
{a:𝑇1 } ∗ {b:𝑇2 }, abbreviated as {a:𝑇1, b:𝑇2 }, specify a record with two fields 𝑎, 𝑏. bi-TP({a:𝑇1, b:𝑇2 },
{b:𝑇2′, c:𝑇3 }, 𝐷) for some 𝐷 is an example for partial overlapping in field b between source and
target predicates. The bi-TP has a solution (𝜃, 𝜆(( (𝑎, 𝑏), 𝑐)) . ( (𝑓 (𝑏), 𝑐), 𝑎)) , {c:𝑇3 }, {a:𝑇1 }) for some
𝜃, 𝑓 . This tells us how to transform abstractions from 𝑇2 to 𝑇2′ (using 𝑓 ), and indicates that {c:𝑇3 }
is needed to complete the transformation, and {a:𝑇1 } stays available for future transformations.

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:12                                    Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


6.2     A Generic TP/bi-TP Solver
Let ℜ be a sequence of inference rules. The solver is a typical backward reasoning procedure.

Notation (P ← A ). For a problem P that can be a TP, a bi-TP, or a bi-EP (introduced later),
P ← A denotes a judgment, “problem P has a solution A ”.

Routine 1 (TP/bi-TP Solver). Given a problem P, which can be a TP(𝑇 , 𝑈 , 𝐷) or a bi-TP(𝑇 , 𝑈 , 𝐷),
Routine 1 performs backward reasoning using rules in ℜ to generate a proof tree with a root
P ← A for some A . The rules are prioritized; one that occurs earlier in ℜ has a higher priority.
This means that, whenever more than one rule is applicable to a subgoal, the routine adopts the
rule that occurs earliest in ℜ. It ensures the generated proof tree is unique. Let P ← A denote
the root of the unique tree. If all its leaves are axioms, return A . Otherwise, the routine fails.

   Specifically, ℜ consists of three sorts of rules: ad-hoc rules, rules instantiated from templates,
and fallbacks. The rules are prioritized: ad-hoc rules have the highest priority, then instantiated
rules, and at last fallbacks. This priority scheme allows users to override instantiated rules by pro-
viding custom ad-hoc rules. This enables fine-tuning in specific cases where the generic reasoning
procedure derived from the templates may not perform optimally. In the following subsections, we
introduce the three sorts of rules, respectively, and focus most of our attention on the templates.

6.3     Ad-hoc Rules
Ad-hoc rules are used to cover the special cases that cannot be handled by the generic templates
over general algebraic abstractions. In our experience, the special cases are limited to:
(1) Specific transformation problems that cannot be generally specified by algebraic axioms, e.g.,
    the one reinterpreting arrays of structures to structures of arrays. As another example, TPs
    and bi-TPs between identical refinement relations are solved by the following ad-hoc rules.
                           Axiom                                            Axiom                         (ID)
                  TP(𝑇 ,𝑇 ) ← (true, 𝜆𝑥 . 𝑥)            bi-TP(𝑇 ,𝑇 ) ← (true, 𝜆𝑥 . 𝑥, Emp, Emp)
    Emp(𝑥) ≜ emp ∧ 𝑥 = () is the refinement relation for empty.
(2) Elimination of predicate counterparts of logic connectives. For example, our case studies re-
    quire two rules to eliminate predicate (∗) defined as (𝑇1 ∗ 𝑇2 ) (𝑥 1, 𝑥 2 ) ≜ 𝑇1 (𝑥 1 ) ∗ 𝑇2 (𝑥 2 ). One
    rule reduces bi-TP((𝑇1 ∗𝑇2 ), 𝑈 , 𝐷) to bi-TP(𝑇1, 𝑈 , 𝐷 1 ) and bi-TP(𝑇2, 𝑍 ′, 𝐷 2 ) for certain 𝑍 ′, 𝐷 1, 𝐷 2 .
    Another rule reduces bi-TP(𝑇 , (𝑈 1 ∗𝑈 2 ), 𝐷) to bi-TP(𝑇 , 𝑈 1, 𝐷 1 ) and bi-TP(𝑅 ′, 𝑈 2, 𝐷 2 ) for certain
    𝑅 ′, 𝐷 1, 𝐷 2 . We leave the details to Appendix C, in order to prevent distracting readers.

6.4     Fallbacks
The rules that have the lowest priorities are fallbacks. When a bi-TP(𝑇 , 𝑈 , 𝐷) fails to be covered
by either ad-hoc rules or instantiated rules, fallbacks are applied, which are listed as follows.
        TP(𝑇 , 𝑈 , 𝐷) ← (𝜃, 𝑓 )                                    Axiom
                                      (FB1 )                                                       (FB2 )
 bi-TP(𝑇 , 𝑈 , 𝐷) ← (𝜃, 𝑓 , Emp, Emp)          bi-TP(𝑇 , 𝑈 , 𝐷) ← (true, (𝜆(𝑥, 𝑧). (𝑧, 𝑥)), 𝑈 ,𝑇 )
The first fallback reduction (FB1 ) downgrades a bi-TP to a TP to allow the reasoning process to
attempt rules and templates written for the TP form (e.g., the transformation between rationals
and integer pairs and transformations of predicates that are not separating-homomorphic). If the
TP(𝑇 , 𝑈 , 𝐷) induced by the first fallback fails to be solved, given that there is no further fallback
for TP, the algorithm attempts the second fallback (FB2 ). The fallback considers the partitions of
program states specified by 𝑇 and 𝑈 to be disjoint. Therefore, the fallback assigns the demand for
transforming 𝑇 to 𝑈 to be the entire 𝑈 and the remainder to be the entire 𝑇 .

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                        67:13


                                     bi-TP(Emp, 𝑈 , {()}) ← (𝜃, 𝑓 , 𝑍, 𝑅)               { ( ) } is the singleton set
       given SZero(𝐹, 𝐷 ′ ),                                        ′            (S0L ) containing only ( ).
                                 bi-TP(𝐹 0 (𝑇 ), 𝑈 , 𝐷) ← (𝜃 ∧ 𝐷 ⊆ 𝐷 , 𝑓 , 𝑍, 𝑅)        𝑥 ⦂ Emp ≜ emp ∧ 𝑥 = ().
                                             bi-TP(𝑇 , Emp, 𝐷) ← (𝜃, 𝑓 , 𝑍, 𝑅)
            given SZero(𝐹, 𝐷 ′ ),                                                            (S0R )
                             bi-TP(𝑇 , 𝐹 0 (𝑈 ), 𝐷) ← (𝜃 ∧ 𝑦 ∈ 𝐷 ′, 𝔪1 (𝜆_.𝑦) ◦ 𝑓 , Emp, 𝑈 )
                            TP(𝑇 , 𝑈 , 𝐷 >>= 𝑑) ← (𝜃, 𝑓 )                                     Ð
  given Functor(𝐹, m, 𝑑),                                       (TF) recalling (𝐷 >>= 𝑑) ≜ 𝑥 ∈𝐷 𝑑 (𝑥)
                          TP(𝐹 (𝑇 ), 𝐹 (𝑈 ), 𝐷) ← (𝜃, m (𝑓 ))          is the monadic bind of sets

           given Functor(𝐹, m, 𝑑)     bi-TP(𝑇 , 𝑈 , 𝐷 >>= (𝑑 ◦ 𝑧)) ← (𝜃, 𝑓 , 𝑍, 𝑅)
                                                                                              (SH)
           and SepHom(𝐹, 𝑠, 𝑧), bi-TP(𝐹 (𝑇 ), 𝐹 (𝑈 ), 𝐷) ← (𝜃, 𝑠 ◦ m (𝑓 ) ◦ 𝑧, 𝐹 (𝑍 ), 𝐹 (𝑅))
                                  bi-TP(𝐹𝑚 (𝑇 ), 𝐹𝑚 (𝑈 ), ℎ(𝐷)) ← (𝜃, 𝑓 , 𝑍, 𝑅)
      given Dist(𝐹, 𝑠, 𝑧),                                                            (SDL ) if 𝑛 ≠ 𝑚 and
                              bi-TP(𝐹𝑛 (𝑇 ), 𝐹𝑚 (𝑈 ), 𝐷) ← (𝜃, 𝑓 ◦ ℎ, 𝐹𝛿 (𝑇 ) ∗ 𝑍, 𝑅)        𝑛 +𝛿 =𝑚
                             where ℎ = 𝜆(𝑥𝑛 , (𝑥𝛿 , 𝑤)). (𝑧𝑛,𝛿 (𝑥𝑛 , 𝑥𝛿 ), 𝑤);
                                  bi-TP(𝐹𝑚 (𝑇 ), 𝐹𝑚 (𝑈 ), ℎ(𝐷)) ← (𝜃, 𝑓 , 𝑍, 𝑅)
      given Dist(𝐹, 𝑠, 𝑧),                                                                      (SDR ) if 𝑛 ≠ 𝑚 and
                              bi-TP(𝐹𝑛 (𝑇 ), 𝐹𝑚 (𝑈 ), 𝐷) ← (𝜃, 𝑔, 𝑍, 𝐹𝛿 (𝑇 ) ∗ 𝑅)                      𝑛 =𝑚 +𝛿
                 where ℎ = 𝜆(𝑥𝑛 , 𝑤). let (𝑥𝑚 , 𝑥𝛿 ) = 𝑠𝑚,𝛿 (𝑥𝑛 ) in (𝑥𝑚 , 𝑤)
                       𝑔 = 𝜆(𝑥𝑛 , 𝑤). let (𝑥𝑚 , 𝑥𝛿 ) = 𝑠𝑚,𝛿 (𝑥𝑛 ); (𝑦, 𝑟 ) = 𝑓 (𝑥𝑚 , 𝑤) in (𝑦, (𝑥𝛿 , 𝑟 ))

                          bi-TP(𝐹𝑚 (𝐹𝛿 (𝑇 )), 𝐹𝑚 (𝑈 ), 𝔪1 (ℎ𝑚,𝛿 )(𝐷)) ← (𝜃, 𝑓 , 𝑍, 𝑅)
given Assoc(𝐹, 𝑔, ℎ),                                                                 (SAL ) if 𝑛 ≠ 𝑚 and
                             bi-TP(𝐹𝑛 (𝑇 ), 𝐹𝑚 (𝑈 ), 𝐷) ← (𝜃, 𝑓 ◦ 𝔪1 (ℎ𝑚,𝛿 ), 𝑍, 𝑅)          𝑛 =𝑚 ·𝛿
                                 bi-TP(𝐹𝑛 (𝑇 ), 𝐹𝑛 (𝐹𝛿 (𝑈 )), 𝐷) ← (𝜃, 𝑓 , 𝑍, 𝑅)
given Assoc(𝐹, 𝑔, ℎ),                                                                         (SAR ) if 𝑛 ≠ 𝑚 and
                             bi-TP(𝐹𝑛 (𝑇 ), 𝐹𝑚 (𝑈 ), 𝐷) ← (𝜃, 𝔪1 (𝑔𝑛,𝛿 ) ◦ 𝑓 , 𝑍, 𝑅)                 𝑛 ·𝛿 =𝑚
                              bi-TP(𝐹𝜖 (𝑇 ), 𝐹𝑚 (𝑈 ), 𝐷) ← (𝜃, 𝑓 ,𝑊 , 𝑅)           if 𝑇 does not match
given SUnit(𝐹, 𝑔, ℎ),                                                       (S1I ) pattern 𝐹 (𝑇 ′ ) for any 𝑛,𝑇 ′
                           bi-TP(𝑇 , 𝐹𝑚 (𝑈 ), 𝐷) ← (𝜃, 𝔪1 (ℎ𝜖 ) ◦ 𝑓 ,𝑊 , 𝑅)                 𝑛

                             bi-TP(𝑇 , 𝑈 , 𝔪1 (𝑔𝜖 )(𝐷)) ← (𝜃, 𝑓 ,𝑊 , 𝑅)           if 𝑈 does not match pattern
given SUnit(𝐹, 𝑔, ℎ),                                                      (S1E ) 𝐹 (𝑈 ′ ) for any 𝑚, 𝑈 ′
                           bi-TP(𝐹𝜖 (𝑇 ), 𝑈 , 𝐷) ← (𝜃, 𝑓 ◦ 𝔪1 (𝑔𝜖 ),𝑊 , 𝑅)          𝑚

Notation (P ← A ) denotes a judgment, “problem P has a solution A ”.
Notation ℎ(𝐷) denotes the image of set 𝐷 under function ℎ. Mapper 𝔪1 (ℎ) ≜ 𝜆(𝑥, 𝑦). (ℎ(𝑥), 𝑦).

Fig. 3. Representative templates of rules for TPs and bi-TPs. Parameters of the templates are notated by the
“given” clauses on the left side. Side conditions are given on the right side.

6.5     Generic Templates Parameterized by Algebraic Properties
The reasoner uses rules instantiated from templates shown in Fig. 3 to solve TPs and bi-TPs. A
template takes a set of algebraic properties as its parameters. Given a set of instances of these
properties, the template is instantiated into a concrete reasoning rule by (1) substituting the in-
stance arguments for the property parameters throughout the template; (2) deriving the proof of
the instantiated rule using the proofs of the instances. Instantiated reasoning rules are then in-
serted into ℜ so the reasoner can use it. Each template defines a reduction aimed at eliminating a
predicate operator, and they are organized according to the priority of the rules they instantiate.
   Rules instantiated from S0L and S0R are attempted first, eliminating any zero-parameterized
operator 𝐹 0 (𝑇 ) for the left side of the bi-TP, and 𝐹 0 (𝑈 ) for the right side, respectively. They reduce
the given bi-TP to a form solvable by the ad-hoc rules of Emp (cf. Appendix C).
   Next, the reasoner tries to apply TF and SH. SH is essentially the bi-abductive version of TF. They
both depend on property TF, and SH additionally demands property SH. Given a TP(𝐹 (𝑇 ),𝐹 (𝑈 ),𝐷)
                                 Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:14                                           Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


or a bi-TP(𝐹 (𝑇 ), 𝐹 (𝑈 ), 𝐷), they eliminate the common predicate operator 𝐹 . Intuitively, if 𝐹 (𝑇 )
represents a container, the templates forward the reasoning process from the container’s space to
its elements’ space, reducing the problem about the container to a problem about its elements.
   If we consider 𝐹𝑛 (𝑇 ), 𝐹𝑚 (𝑈 ) as slices of some structure, templates SDL and SDR leverage the
scalar distributivity property SD to split and merge slices. Given bi-TP(𝐹𝑛 (𝑇 ), 𝐹𝑚 (𝑈 ), 𝐷), by check-
ing if 𝑛 = 𝑚 + 𝛿, SDR checks if the source slice 𝐹𝑛 (𝑇 ) covers a larger domain than the target 𝐹𝑚 (𝑇 ),
represented by 𝐹𝛿 (𝑇 ). If so, it splits the source slice into two: 𝐹𝑚 (𝑇 ) and 𝐹𝛿 (𝑈 ). Then it leaves the
slice 𝐹𝛿 (𝑇 ) as a residue and induces a subproblem bi-TP(𝐹𝑚 (𝑇 ), 𝐹𝑚 (𝑈 ), 𝐷) reducible by SH.
   The case in SDL is symmetric to SDR , but checks if the source slice cannot cover the target and de-
mands an additional 𝛿-portion. Let us explain this trying to solve bi-TP(Slice [𝑖,𝑗 ) 𝑇 , Slice [𝑖,𝑘 ) 𝑈 , 𝐷).
If 𝑗 < 𝑘 it implies [𝑖, 𝑗) + [ 𝑗, 𝑘) = [𝑖, 𝑘). Thus, SDL is applicable if we instantiate 𝑛, 𝛿, 𝑚 to
[𝑖, 𝑗), [ 𝑗, 𝑘), [𝑖, 𝑘). Application of SDL induces the subgoal bi-TP(Slice [𝑖,𝑘 ) 𝑇 , Slice [𝑖,𝑘 ) 𝑈 , ℎ(𝐷) and
indicates that Slice [ 𝑗,𝑘 ) (𝑇 ) is demanded to be extracted in the subsequent reasoning process, where
ℎ(𝐷) augments the Domain of 𝑇 with 𝛿.
   Templates SDL and SDR are insufficient when the scalar addition is not commutative, associative,
and cancellation; for example, interval addition that is non-commutative. If 𝑗 < 𝑘 and 𝑖 ′ < 𝑖,
bi-TP(Slice [𝑖,𝑗 ) , Slice [𝑖 ′ ,𝑘 ) , 𝐷) cannot be handled by SDL and SDR because there is no 𝛿 such that
[𝑖, 𝑗) + 𝛿 = [𝑖 ′, 𝑘) or [𝑖, 𝑗) = [𝑖 ′, 𝑘) + 𝛿. Instead, it requires a template for (𝛿 ′ + 𝑛 + 𝛿 = 𝑚) and
instantiates 𝛿 ′, 𝑛, 𝛿, 𝑚 to [𝑖 ′, 𝑖), [𝑖, 𝑗), [ 𝑗, 𝑘), [𝑖 ′, 𝑘). This is detailed in Appendix F.
   Templates SAL and SAR leverage property SA to respectively collapse nested 𝐹𝑛 (𝐹𝑚 (𝑇 )) into
𝐹𝑛·𝑚 (𝑇 ) and expand collapsed 𝐹𝑛·𝑚 (𝑇 ) into 𝐹𝑛 (𝐹𝑚 (𝑇 )). They are symmetric to SDL and SDR in
terms of considering scalar multiplication instead of scalar addition,
   Notably, our reasoner does not generically support module-like operators that are both scalar
associative and scalar distributive. Consider a bi-TP( 12 ⨸ 𝑇 , 31 ⨸ 𝑈 , 𝐷) and assume 𝑇 = 14 ⨸ 𝑇 ′ for
some 𝑇 ′ . Permission modality ⨸ is both scalar associative and scalar distributive. There are inde-
terminate solutions 𝛿, 𝛿 ′ such that 12 = 𝛿 · 13 +𝛿 ′ . Consequently, we do not know which value should
be used to instantiate 𝛿 in SAL , SAR , SDL , or SDR . However, it is possible to rewrite 𝐹𝑛 (𝐹𝑚 (𝑇 )) to
𝐹𝑛·𝑚 (𝑇 ) for any scalar-associative 𝐹 and any 𝑛, 𝑚,𝑇 before invoking the TP/bi-TP solver. If after
this it is not necessary to apply SAL and SAR , the reasoning succeeds by applying SDL and SDR .
   Finally, if a bi-TP(𝑇 , 𝐹𝑏 (𝑈 ), 𝐷) expects to transform a non-module-like 𝑇 to a module-like 𝐹𝑏 (𝑈 ),
S1I wraps 𝑇 to 𝐹𝜖 (𝑇 ). Conversely, if a bi-TP(𝐹𝜖 (𝑇 ), 𝑈 , 𝐷) expects to transform a module-like 𝐹𝜖 (𝑇 )
to a non-module-like 𝑈 , S1E unwraps 𝐹𝜖 (𝑇 ) when its scalar 𝜖 is an identity.
   As a side note, the side conditions in the templates are arithmetic equations within the ring-like
scalar algebra(s). We assume our reasoner is parameterized by solvers to handle them.

6.6     Example: Matrix Partitioning
To illustrate how instantiated rules from the templates are applied   
                                                                           to real problems, we consider
the transformation that splits the abstraction of a big matrix 𝐶𝐴 𝐵𝐷 into four sub-matrixes 𝐴, 𝐵, 𝐶, 𝐷,
which is a key step in our case study of Strassen’s matrix multiplication algorithm.
   A 2𝑁 × 2𝑁 matrix is represented by a two-dimensional array of lengths 2𝑁 . We represent its
refinement by predicate Slice [0,2𝑁 ) (Slice [0,2𝑁 ) Z). The desired transformation is then
                                                                                                                               
                                                𝑙𝐴 ⦂ Slice [0,𝑁 ) (Slice [0,𝑁 ) Z) ∗ 𝑙𝐵 ⦂ Slice [0,𝑁 ) (Slice [𝑁 ,2𝑁 )Z ) ∗
   𝑙 ⦂ Slice [0,2𝑁 ) (Slice [0,2𝑁 ) Z) −→
                                                𝑙𝐶 ⦂ Slice [𝑁 ,2𝑁 ) (Slice [0,𝑁 ) Z) ∗ 𝑙𝐷 ⦂ Slice [𝑁 ,2𝑁 ) (Slice [𝑁 ,2𝑁 ) Z)
where 𝑙𝐴 = 𝑙 [0:𝑁 ] [0:𝑁 ] , 𝑙𝐵 = 𝑙 [0:𝑁 ] [𝑁 :2𝑁 ] , 𝑙𝐶 = 𝑙 [𝑁 :2𝑁 ] [0:𝑁 ] and 𝑙𝐷 = 𝑙 [𝑁 :2𝑁 ] [𝑁 :2𝑁 ] , in Python’s slicing
notation. The transformation raises four bi-TPs for extracting each sub-matrix. Let us consider the
first bi-TP, ignore the domain of the bi-TP, and leave the detailed reduction process to Appendix D,
                       bi-TP( Slice [0,2𝑁 ) (Slice [0,2𝑁 ) Z) , Slice [0,𝑁 ) (Slice [0,𝑁 ) Z), · · · ).                             (1)

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                            67:15


As Slice satisfies SD, this property of Slice instantiates template SDR . The instantiated rule is shown
in Appendix D. The rule reduces goal (1) to the following bi-TP.
                        bi-TP( Slice [0,𝑁 ) (Slice [0,2𝑁 ) Z) , Slice [0,𝑁 ) (Slice [0,𝑁 ) Z) , · · · )                         (2)
As Slice also satisfies TF and SH, these properties of Slice instantiate template SH. The instantiated
rule eliminates the outer-most common operator Slice [0,𝑁 ) and reduces goal (2) to,
                                         bi-TP( Slice [0,2𝑁 ) Z , Slice [0,𝑁 ) Z , · · · )                                      (3)
Again, our reasoner applies the previous rule instantiated from SDR to split the source slice and to
reduce goal (3) to bi-TP( Slice [0,𝑁 ) Z , Slice [0,𝑁 ) Z , · · ·) which is immediately solvable by (ID) rule.

7 Programming Language and wp-Transformer
Starting from this section, we turn to complete our SL reasoner. We demonstrate how a program
verifier can be built on top of the TP/bi-TP solver, in order to show that algebra-based rule genera-
tion can benefit program verification. To ground our discussion on program verification, and in line
with our automation algorithm’s generic design, we base our discussion on a minimally-specified
generic formalization that can be instantiated to many concrete languages, including C.

7.1      A Generic Formalization for Programming Languages
We formalize our language using non-deterministic state monad to define a generic semantic for-
malization for programming languages. We abstract the language operations as a set of operators
Opr represented by 𝜌. Operators can be parameterized by one or more programs, becoming a
higher-order operator, with arity(𝜌) denoting the number of higher-order parameters of 𝜌. This
allows for the formalization of control flow (e.g., If and While) as higher-order operators.
𝑢, 𝑣 ∈ Value,          Program ⊆ Value → Monad,                      where Monad ≜ State → powerset(Value × State)
Program ∋ 𝐶 1, 𝐶 2, · · · F 𝜌 (𝐶 1, · · · , 𝐶 arity(𝜌 ) ) | 𝜆𝑣 . (𝐶 1 (𝑣) >>= 𝐶 2 ),      where (>>=) is monadic bind
To illustrate how higher-order operators represent control flows, If (𝐶 T, 𝐶 F )(𝑏) ≜ if 𝑏 then 𝐶 T else 𝐶 F
is an operator having 𝑏 as its argument and 𝐶 T, 𝐶 F as two programs that represent the two branches.

7.2      Separation Logic over the Programming Language Formalization
Conventionally, we use wp𝐶 (𝑢 ) {𝑣. 𝜓 (𝑣)} to denote the weakest precondition of a computation
𝐶 (𝑢), where 𝜓 (𝑣) is an SL formula parameterized by variable 𝑣. Judgement (wp𝐶 (𝑢 ) {𝑣. 𝜓 (𝑣)} ⊣ 𝜙)
specifies that given argument 𝑢 and an initial state 𝑠 satisfying 𝜙, the computation 𝐶 (𝑢) returns a
value 𝑣 and results in a state 𝑠 ′ satisfying 𝜓 (𝑣) — recall the discussion in §4 about our “big PCM”.
                  (wp𝐶 (𝑢 ) {𝑣. 𝜓 (𝑣)} ⊣ 𝜙) ≜ ∀𝑠 𝑠 ′ 𝑣. (𝑠 |= 𝜙) ∧ (𝑣, 𝑠 ′ ) ∈ 𝐶 (𝑢) −→ (𝑠 ′ |= 𝜓 (𝑣))                    (wp)
Hoare triples are conventionally specified based on it, {𝜙 }𝐶 (𝑢){𝑣. 𝜓 (𝑣)} ≜ (wp𝐶 (𝑢 ) {𝑣. 𝜓 (𝑣)} ⊣ 𝜙).
  Based on this generic formalization for programming languages, we do not stipulate any specific
wp rule. Instead, we assume a set W of wp rules in the following form
      wp𝐶1 (𝑢1 ) {𝑣 1 . 𝜓 1 (𝑣 1 )} ⊣ 𝜙 1     ···     wp𝐶𝑛 (𝑢𝑛 ) {𝑣𝑛 . 𝜓𝑛 (𝑣𝑛 )} ⊣ 𝜙𝑛               for fresh fixed
                                                                                        (wp-rule)
                         wp𝜌 (𝐶1,··· ,𝐶𝑛 ) (𝑢0 ) {𝑣 0 . 𝜓 0 (𝑣 0 )} ⊣ 𝜙 0                           variables 𝑢 1, · · · , 𝑢𝑛
Some examples are listed in Fig. 4. Based on the set W , we formalize a standard wp-transformer.
Routine 2 (wp-transformer). Given (𝜙, 𝐶 (𝑢),𝜓 (𝑣)), perform backward reasoning using rules in
W and rule (Bind) in Fig. 4 to generate a proof tree with a root wp𝐶 (𝑢 ) {𝑣. 𝜓 (𝑣)} ⊣ 𝜙 ′ for some 𝜙 ′ .
Return 𝜙 −→ 𝜙 ′ if all leaves in the tree are axioms. Otherwise, the routine fails.

                                      Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:16                                         Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


        wp𝐶2 (𝑢 ′ ) {𝑣. 𝜓 (𝑣)} ⊣ 𝜓 ′ (𝑢 ′ )     wp𝐶1 (𝑢 ) {𝑣. 𝜓 ′ (𝑣)} ⊣ 𝜓
                                                                             (Bind) for a fresh fixed variable 𝑢 ′
                         wp (𝐶1 >>=𝐶2 ) (𝑢 ) {𝑣. 𝜓 (𝑣)} ⊣ 𝜓
                wpload(addr ) {𝑣. 𝜓 (𝑣)} ⊣ (𝑥 ⦂ Ref addr𝑇 ) ∗ ∀𝑣. (𝑥 ⦂ Ref addr𝑇 ∗ 𝑥 ⦂ val𝑣 𝑇 −∗ 𝜓 (𝑣))
                wpstore(addr,𝑢 ) {𝑣. 𝜓 (𝑣)} ⊣ (𝑥 ⦂ Ref addr𝑇 ) ∗ (𝑦 ⦂ val𝑢 𝑈 ) ∗ (𝑦 ⦂ Ref addr 𝑈 −∗ 𝜓 ())
                                   wp𝐶T ( ) {𝑣. 𝜓 (𝑣)} ⊣ 𝜙 1      wp𝐶F () {𝑣. 𝜓 (𝑣)} ⊣ 𝜙 2
                      wp If (𝐶T,𝐶F ) (𝑢 ) {𝑣. 𝜓 (𝑣)} ⊣ (𝑃 ⦂ val𝑢 Bool) ∗ ((𝑃 → 𝜙 1 ) ∧ (¬𝑃 → 𝜙 2 ))
Notations: (𝑥 ⦂ Ref addr 𝑇 ) ≜ (∃𝑣. addr ↦→ 𝑣 ∧ 𝑣  𝑥 ⦂ 𝑇 ) claims the ownership of a memory object at
address addr and asserts it has a value 𝑣 refining 𝑥 w.r.t. 𝑇 .
(𝑥 ⦂ val𝑣 𝑇 ) ≜ (emp ∧ 𝑣  𝑥 ⦂ 𝑇 ) asserts a value 𝑣 that refines 𝑥 w.r.t. 𝑇 .

              Fig. 4. Example rules for wp-transformer, using the simple imperative language IMP.


8 Connecting the TP/bi-TP Solver to Program Verification
In this section, we build an SL reasoner on top of the TP/bi-TP solver introduced in § 6 to show
that our algebraic method for TPs/bi-TPs can be used to tackle real-world program verification
problems, which then implies the significance of our algebraic abstractions (§ 5) and automatic
rule generation (§6) based on the algebraic abstractions.
   This SL reasoner is based on a standard process using wp-transformer. Illustrated in Fig. 1, the
process first uses the wp-transformer shown in Routine 2 to extract an SL entailment that implies
the desired program correctness; then, it applies an SL entailment reasoner to extract an FOL for-
mula as a proof obligation that implies the validity of the given SL entailment. The proof obligation
is either sent to users for manual proof or to ATPs for automatic proof.
   Focusing on proving SL entailments, Section 8.1 first restricts the domain of formulas considered
by our reasoner. Then, as an intermediate step, §8.2.1 first reduces the decision problem of a given
SL entailment to so-called bi-abductive Entailment Problems (bi-EPs), used merely as a stepping-
stone. §8.2.2 finally reduces these bi-EPs to a series of bi-TPs. Through these steps, we establish a
connection between our TP/bi-TP solver (§6) and program verification, completing the chain from
program specifications to algebraic problem-solving. In the end of the section, § 8.3 clarifies how
the reasoning process matches hypotheses of an entailment with its goals; § 8.4 provides details
about how to instantiate existential quantifications and evars.

8.1      Restricting Formulas Reducible to bi-TPs
Before delving into formalizing the SL reasoner, we must clarify that not all decision problems of
SL entailments are reducible to bi-TPs by our reasoner. Following RefinedC [64] and Argon [65],
we restrict the formulas for SL entailments and program state specification to subsets E and S,
                   State               S F 𝑥 ⦂ 𝑇 | ⊤ | ⊥ | emp | S ∗ S | S ∧ 𝑃 | ∃𝛼 . S                            (S)
                   Goal                G F S | S ∗ G | S −∗ G | 𝑃 → G | G ∧ G | ∀𝛼 . G | ∃𝛼 . G                   (G)
                   Entailment          EFS→G                                                                       (E)
where 𝑃 ranges over FOL formulas; 𝑇 ranges over all SL predicates, no matter if the formula of the
definition of 𝑇 is within E, G, or S. Specifically, this restriction means that, (1) we only consider
program specifications {𝜙 }𝐶{𝑣. 𝜓 (𝑣)} such that 𝜙 ∈ S and 𝜓 (𝑣) ∈ G; (2) for any wp rule given in
the set W (cf., §7.2) and in form (wp-rule), we require 𝜓𝑖 (𝑣𝑖 ) ∈ G for every 𝑖 ∈ {0, 1, · · ·, 𝑛}.
   Lemma 8.1 (wp-tRansfoRmeR Routine 2 is closed in E). For any program 𝐶, any 𝜙 ∈ S and
𝜓 (𝑣) ∈ G, the return of the wp-transformer Routine 2 belongs to E.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                               67:17


   Although the restriction on formulas limits the capability of our reasoner, a practical mitigation
exists. To specify program states using a formula 𝜙 ∉ S, users can define a predicate 𝑇 (𝑥) ≜ 𝜙
to wrap 𝜙. The resulting formula (𝑥 ⦂ 𝑇 ) belongs to S. As long as users can provide algebraic
properties of 𝑇 , 𝜙 can be equivalently handled by our reasoner through rewriting 𝜙 into 𝑥 ⦂𝑇 . For
example, consider the predicate definition 𝑥 ⦂ Ref 𝑎 (𝑇 ) ≜ ∃𝑣. (𝑎 ↦→ 𝑣) ∧ (𝑣  𝑥 ⦂𝑇 ), which involves
the satisfaction operator  that is not in S. Our reasoner can still handle 𝑥 ⦂ Ref 𝑎 (𝑇 ) because the
algebraic properties of Ref 𝑎 (𝑇 ) are provided. Through this wrapping technique, our reasoner can
support formulas that would otherwise exceed S or G. Consequently, our reasoner still targets the
entire SL, provided that the necessary properties of the wrapper predicates are supplied.

8.2   Reduction from SL Entailments to bi-TPs
Given an SL entailment between two formulas, if any of the formulas is composite, we apply a
decomposition process to reduce the decision problem of the entailment to decision problems of
a series of smaller entailments between atomic formulas. We say a formula is atomic iff it is a
predicate application, and composite iff it is not atomic (⊤, ⊥, emp are nullary connectives which
are eliminated by the decomposition process). We want this decomposition because entailments
between predicate applications, 𝑥 ⦂ 𝑇 −→ 𝑦 ⦂ 𝑈 , are close to the statement of bi-TP, allowing us
to easily reduce their decision problems to bi-TPs.
    Roughly, this decomposition splits a big entailment between 𝑛 source items 𝜙 1 ∗ · · · ∗ 𝜙𝑛 and 𝑚
target items 𝜓 1 ∗ · · · ∗ 𝜓𝑚 into about 𝑛 × 𝑚 smaller entailments between (parts of) 𝜙𝑖 and (parts of)
𝜓 𝑗 for 1 ≤ 𝑖 ≤ 𝑛 and 1 ≤ 𝑗 ≤ 𝑚. Let us consider an entailment between 𝜙 and 𝜓 as extracting a
bunch of target resources 𝜓 from a bunch of source resources 𝜙. The big entailment 𝜙 1 ∗· · ·∗𝜙𝑛 −→
𝜓 1 ∗ · · ·𝜓𝑚 then aims to extract the 𝑚 bunches of resources from the 𝑛 bunches. The decomposition
divides the extraction into many small steps: We first extract the bunch 𝜓 1 from the bunch 𝜙 1 .
Because the two bunches may not be perfectly matched but partially overlapped, some part 𝑍 1 of
the target 𝜓 1 may be missing in the source 𝜙 1 , and some part 𝑅1 of the source 𝜙 1 may remain after
the extraction. To find the missing 𝑍 1 , we move to the next bunch 𝜙 2 , which may provide some
components but still lack others, so we continue to look in 𝜙 3, · · · , 𝜙𝑛 . All the source bunches
leave some parts 𝑅1, · · · , 𝑅𝑛 (can be empty) after the extraction. After 𝜓 1 is gathered, we turn to
extract the next target 𝜓 2 from the remaining parts 𝑅1 ∗ · · · ∗ 𝑅𝑛 of the source bunches, in the same
way described above. Repeatedly, we extract 𝜓 3, · · · ,𝜓𝑚 iteratively from the remaining parts of the
source bunches after each extraction.
    To formalize the extraction that can leave some remaining source (e.g., 𝑅1 above) and unfulfilled
target (e.g., 𝑍 1 above), we introduce bi-abductive entailment, 𝜙 ∗ 𝑍 −→ 𝜓 ∗ 𝑅, where frame 𝑅
represents the remaining part of 𝜙 after the extraction and anti-frame 𝑍 the missing part claimed
by 𝜓 but not seen in 𝜙. Both 𝑍, 𝑅 are variables that represent unknowns to infer. We define the
problems of inferring such 𝑍, 𝑅 as bi-abductive Entailment Problems

   Definition 8.2 (bi-EP). Given 𝜙,𝜓 ∈ S, if ∃ does not occur in 𝜙, a bi-abductive Entailment Problem
bi-EP(𝜙,𝜓 ) looks for a triple (𝜃, 𝑍, 𝑅), for an FOL formula 𝜃 as the proof obligation, and two SL
formulas 𝑍, 𝑅 ∈ S, such that 𝜙 ∗ 𝑍 −→ 𝜓 ∗ 𝑅 holds if 𝜃 holds.

   The decomposition of composite entailments is realized by rules in Fig. 7. Rule (∗L ) and (∗R )
formalize the intuition at the beginning of this subsection: to extract 𝜓 from two bunches 𝜙 1 ∗ 𝜙 2
of resources, we first look in bunch 𝜙 1 . It may leave some unfulfilled target 𝑍 , so we continue to
look for it in bunch 𝜙 2 . The remainders 𝑅1, 𝑅2 of the two small extractions are left as the remainder
of the original big extraction. In (∗R ), where we extract two bunches 𝜓 1,𝜓 2 from one bunch 𝜙, we
first extract 𝜓 1 from 𝜙 and then 𝜓 2 from the remaining part 𝑅 of 𝜙.

                             Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:18                                          Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


                bi-EP(𝑆 1, 𝑆 2 ) ← (𝜃, 𝑆𝑍 , 𝑆𝑅 )     emp −→ 𝑆𝑍         𝑆𝑅 −→ emp
                                                                                      (bi-EP) ∃ does not
                                             𝜃 | 𝑆1 ⊢ 𝑆2                                      occur in 𝑆 1
               bi-EP(𝑆 1, 𝑆 2 ) ← (𝜃 1, 𝑆𝑍 , 𝑆𝑅 )     emp −→ 𝑆𝑍        𝜃 2 | 𝑆𝑅 ⊢ 𝐺
                                                                                      (bi-EPR ) ∃ does not
                                      𝜃 1 ∧ 𝜃 2 | 𝑆1 ⊢ 𝑆2 ∗ 𝐺                                   occur in 𝑆 1
             𝜃 (𝛽) | 𝑆 (𝛽) ⊢ 𝐺             for a fresh fixed                 𝜃 (𝛽) | 𝑆 ⊢ 𝐺 (𝛽)      for a fresh fixed
                                    (S ∃ )
        ∀𝛼 . 𝜃 (𝛼) | ∃𝛼 . 𝑆 (𝛼) ⊢ 𝐺        variable 𝛽                   ∀𝛼 . 𝜃 (𝛼) | 𝑆 ⊢ ∀𝛼 . 𝐺 (𝛼) variable 𝛽
  𝜃 | 𝑆1 ∗ 𝑆2 ⊢ 𝐺           𝜃 | 𝑆 ∧𝑃 ⊢𝐺           𝜃 1 | 𝑆 ⊢ 𝐺1 𝜃 2 | 𝑆 ⊢ 𝐺2        𝜃 (𝛽) | 𝑆 ⊢ 𝐺 (𝛽)      for a fresh free
  𝜃 | 𝑆 1 ⊢ 𝑆 2 −∗ 𝐺       𝜃 |𝑆 ⊢𝑃 →𝐺               𝜃 1 ∧ 𝜃 2 | 𝑆 ⊢ 𝐺1 ∧ 𝐺2   ∀𝛼 . 𝜃 (𝛼) | 𝑆 ⊢ ∃𝛼 . 𝐺 (𝛼) variable 𝛽

Fig. 5. Rules Reducing SL Entailments to bi-EPs. Notation bi-EP(𝜙,𝜓 ) ← (𝜃, 𝑆𝑍 , 𝑆𝑅 ) denotes a judgement,
“the problem bi-EP(𝜙,𝜓 ) has a solution (𝜃, 𝑆𝑍 , 𝑆𝑅 )”.

 Axiom          𝜙 −→ emp 𝜓 −→ emp              𝜙 −→ emp         𝜙 (𝛽 ) −→ emp for a fresh        IdEleI (𝑇 , 𝐷 ) 𝑥 ∈𝐷
⊥ −→ emp           𝜙 ∗ 𝜓 −→ emp              𝜙 ∧ 𝑃 −→ emp      ∃𝛼 . 𝜙 (𝛼 ) −→ emp fixed 𝛽             𝑥 ⦂ 𝑇 −→ emp
  Axiom          emp −→ 𝜙 emp −→ 𝜓            emp −→ 𝜙 𝑃          emp −→ 𝜙 (𝛽 ) for a fresh       IdEleE (𝑇 , 𝐷 ) 𝑥 ∈𝐷
emp −→ ⊤             emp −→ 𝜙 ∗ 𝜓             emp −→ 𝜙 ∧ 𝑃      emp −→ ∃𝛼 . 𝜙 (𝛼 ) free 𝛽              emp −→ 𝑥 ⦂ 𝑇

 Fig. 6. Transformations to or from empty, used to solve two subgoals raised by rule (bi-EP) and (bi-EPR ).

                              bi-TP(𝑇 , 𝑈 , {(𝑥, 𝑧)}) ← (𝜃, 𝑓 , 𝑍, 𝑅)   Trans(𝑈 , ≤)
                                                                                                                 (biTP)
        bi-EP(𝑥 ⦂ 𝑇 , 𝑦 ⦂ 𝑈 ) ← (𝜃 ∧ (𝑥, 𝑧) ∈ dom(𝑓 ) ∧ 𝜋1 (𝑓 (𝑥, 𝑧)) ≤ 𝑦 , 𝑧 ⦂ 𝑍 , 𝜋 2 (𝑓 (𝑥, 𝑧)) ⦂ 𝑅)
    where 𝜋𝑖     denotes the 𝑖 th projection of a tuple.
                       Axiom                                                        Axiom               (empR )
                                           (empL )
            bi-EP(emp,𝜓 ) ← (true,𝜓, emp)                                bi-EP(𝜙, emp) ← (true, emp, 𝜙)
                        Axiom                                                        Axiom
                                           (⊥L )                                                        (⊤R )
              bi-EP(⊥,𝜓 ) ← (true, emp, ⊥)                                bi-EP(𝜙, ⊤) ← (true, ⊤, emp)
                            bi-EP(𝜙 1,𝜓 ) ← (𝜃 1, 𝑍, 𝑅1 )     bi-EP(𝜙 2, 𝑍 ) ← (𝜃 2, 𝑍 ′, 𝑅2 )
                                                                                               (∗L )
                                     bi-EP(𝜙 1 ∗ 𝜙 2,𝜓 ) ← (𝜃 1 ∧ 𝜃 2, 𝑍 ′, 𝑅1 ∗ 𝑅2 )
                            bi-EP(𝜙,𝜓 1 ) ← (𝜃 1, 𝑍 1, 𝑅)    bi-EP(𝑅,𝜓 2 ) ← (𝜃 2, 𝑍 2, 𝑅 ′ )
                                                                                              (∗R )
                                    bi-EP(𝜙,𝜓 1 ∗ 𝜓 2 ) ← (𝜃 1 ∧ 𝜃 2, 𝑍 1 ∗ 𝑍 2, 𝑅 ′ )
             bi-EP(𝜙,𝜓 ) ← (𝜃, 𝑍, 𝑅)                                       bi-EP(𝜙,𝜓 ) ← (𝜃, 𝑍, 𝑅)
                                        (pure-∧L )                                                    (pure-∧R )
        bi-EP(𝜙 ∧ 𝑃,𝜓 ) ← (𝑃 → 𝜃, 𝑍, 𝑅)                                bi-EP(𝜙,𝜓 ∧ 𝑃) ← (𝜃 ∧ 𝑃, 𝑍, 𝑅)
                               bi-EP(𝜙,𝜓 (𝛽)) ← (𝜃, 𝑍, 𝑅)
                                                              (∃R ) for a fresh free variable 𝛽
                             bi-EP(𝜙, ∃𝛼 . 𝜓 (𝛼)) ← (𝜃, 𝑍, 𝑅)

          Fig. 7. Reducing bi-EPs to bi-TPs. Symbols 𝜙,𝜓, 𝑍, 𝑅 range over S, and 𝜃, 𝑃 over FOL formulas.


   In the rest of this section, we return to elaborate on the reduction from SL entailments to bi-TPs,
which is split into two stages: the construction of bi-EPs as in §8.2.1 and the reduction from bi-EPs
to bi-TPs as in §8.2.2.
8.2.1 Reduction from SL Entailments to bi-EPs. This reduction starts from judgment 𝜃 | 𝑆 ⊢ 𝐺 that
encodes the task of inferring the proof obligation 𝜃 of entailment (𝑆 → 𝐺).
                       (𝜃 | 𝑆 ⊢ 𝐺) ≜ (if FOL formula 𝜃 holds, SL formula (𝑆 → 𝐺) holds)
Given an SL entailment 𝑆 → 𝐺, for 𝑆 ∈ S and 𝐺 ∈ G, our reasoner first initiates a goal (𝜃 | 𝑆 ⊢ 𝐺),
setting 𝜃 as a fresh free variable to be instantiated by the later reasoning process. The obtained

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                 67:19


instantiation of 𝜃 is the output of our reasoner, which is a proof obligation strong enough to prove
the given entailment. This proof obligation is sent to automatic solvers or manual proof works.
   Our reasoner then applies rules in Fig. 5 exhaustively in a backward manner to decompose the
goal (𝜃 | 𝑆 ⊢ 𝐺) into a series of bi-EPs and subgoals in forms emp −→ S and S −→ emp. (bi-EP) and
(bi-EPR ) are the rules that convert entailments into bi-EPs. Other rules eliminate connectives on
the right-hand side of entailments, to convert them into a form applicable by (bi-EP) or (bi-EPR ).
   The obtained bi-EPs are handled in the next subsection. Subgoals in forms emp −→ S and S −→
emp are solved by rules in Fig. 6 via backward reasoning. Two algebraic properties of predicates are
used here to provide abstract domains 𝐷 about empty resource. IdEleI (IdEleE ) specifies a domain
𝐷 of abstractions that can transform to (be made from) empty.
IdEleI (𝑇 , 𝐷) ≜ ∀𝑥 ∈𝐷. (𝑥 ⦂ 𝑇 −→ emp)             IdEleE (𝑇 , 𝐷) ≜ ∀𝑥 ∈𝐷. (emp −→ 𝑥 ⦂ 𝑇 )             (IEI & IEE ).
   Besides, rules (bi-EP) and (bi-EPR ) require that no ∃ occurs on an entailment’s left-hand side. To
eliminate any ∃ in this position, we can apply rewriting to move it to the outermost scope (by the
rewrite rules used in Skolemization) and then apply (S∃ ) to eliminate it.
   Additionally, our reasoning process can be extended to support overloading multiple wp-rules
on one program operation and resolving the proper rule to apply. As we primarily focus on deriving
SL entailments using the TP/bi-TP solver, we leave this extension to Appendix G.
8.2.2 Reductions from bi-EPs to bi-TPs. Having reduced decision problems of SL entailments to
bi-EPs in the previous subsection, now we present the reduction from bi-EPs to bi-TPs.
   This reduction is realized by applying the rules in Fig. 7 exhaustively in a backward manner.
Rule (biTP) reduces a bi-EP between predicate applications to a bi-TP. All other rules are used to
eliminate connectives, ultimately reducing a bi-EP between composite formulas to bi-EPs between
predicate applications, into a form to which (biTP) can apply.
   In rule (biTP), Trans(𝑈 , ≤) is an algebraic property specifying that the order (≤) is a lower
approximation to the entailment relation of the abstractions of refinement relation 𝑇 .
                Trans(𝑈 , ≤) ≜ for any 𝑥, 𝑦 such that 𝑥 ≤ 𝑦, there is 𝑥 ⦂ 𝑈 −→ 𝑦 ⦂ 𝑈                             (Tr)
To explain the rationale behind (biTP), assume bi-TP(𝑇 , 𝑈 , {(𝑥, 𝑧)}) has an answer (𝜃, 𝑓 , 𝑍, 𝑅).
                   by the bi-TP’s answer                      by property Trans(𝑈 , ≤ )
(𝑥, 𝑧) ⦂ (𝑇 ∗ 𝑍 ) −−−−−−−−−−−−−−−→ 𝑓 (𝑥, 𝑧) ⦂ (𝑈 ∗ 𝑅) −−−−−−−−−−−−−−−−−−→ (𝑦, 𝜋 2 (𝑓 (𝑥, 𝑧))) ⦂ (𝑈 ∗ 𝑅)
The answer provides us a transformation from 𝑇 ∗ 𝑍 to 𝑈 ∗ 𝑅 as illustrated by the first arrow in the
above diagram. This transformation also claims a proof obligation 𝜃 ∧ (𝑥, 𝑧) ∈ dom(𝑓 ) according
to the definitions of TP and bi-TP. The abstraction returned by the transformation is 𝑓 (𝑥, 𝑦) while
the goal bi-EP(𝑥 ⦂ 𝑇 , 𝑦 ⦂ 𝑈 ) expects 𝑦. It forces us to subsequently apply property Trans(𝑈 , ≤) to
transform 𝜋1 (𝑓 (𝑥, 𝑧))⦂𝑈 into 𝑦⦂𝑈 as illustrated by the second arrow. This application yields a proof
obligation 𝜋 1 (𝑓 (𝑥, 𝑧)) ≤ 𝑦. Recall that 𝜋𝑖 (𝑥 1, 𝑥 2 ) ≜ 𝑥𝑖 is the 𝑖 th projection of a tuple. Consequently,
the bi-EP(𝑥 ⦂ 𝑇 , 𝑦 ⦂ 𝑈 ) has a solution as that presented in rule (biTP).

8.3   Matching Goals and Hypothesis
When multiple hypotheses and goals are involved in an entailment, e.g., 𝜙 1 ∗ · · · ∗ 𝜙𝑛 −→ 𝜓 ∗ · · · ,
we initially treat every hypothesis as possibly transformable into part of a goal. Thus, we decom-
pose the entailment to smaller bi-abductive entailments from (𝜙 1,𝜓 ), (𝜙 2,𝜓 ), · · · , iteratively asking
every hypothesis whether it entails any component of 𝜓 . For each entailment query, our reasoner
wields its full power in applying our TP/bi-TP rules, to try and prove an entailment holds. As an
example, a proof tree for deriving 𝑥 ⦂ 𝑇 ∗ 𝑦 ⦂ 𝑈 −→ 𝑦 ⦂ 𝑈 ∗ 𝑥 ⦂ 𝑇 is presented in Appendix H.
   In practice, many obtained entailment subgoals are quickly discarded by falling back to (FB2 ),
for example due to lack of applicatable rules. Most predicates are parameterized by identifiers like

                               Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:20                                    Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


memory addresses or domains like initial indexes and lengths of slices. These help syntacically
guide the solver in applying relevant transformations. In principle the solver can choose a wrong
transformation if multiple options are available, which would cause spurious failure of the rea-
soning process, but our reasoning rule templates are carefully chosen and given priorities in the
reasoning system to minimize overlap (a user must still take care when providing their own ad-hoc
rules §6.3). We did not observe erroneous rule application in practice in our case studies (§10).
   Also, in principle our search strategy has at least quadratic worst-case complexity, although we
observe much better practical performance in our evaluation (§10.2).

8.4     Handling Existential Quantification and Evars
Correct instantiation of ∃-quantification and evars is a common problem in SL automation frame-
works. We describe our strategy and briefly compare it that of RefinedC and Diaframe.
   First, our assertion syntax of 𝑥 ⦂ 𝑇𝑎 differentiates the predicate argument 𝑥 and predicate pa-
rameter 𝑎. Predicate parameter 𝑎 is used to identify the name or the address of a resource, or to
indicate the domain of a slice. Since our reasoning process is guided by predicates (𝑇𝑎 ), only the
evars occurring in predicate parameters are influential to the reasoning process. Evars in predicate
arguments, FOL constraints (e.g., the len(?𝑥) = 2 in ?𝑥 ⦂ List ∧len(?𝑥) = 2), or any other place, are
left uninstantiated until they are presented in the final proof obligations, which are solved by FOL
solvers like Isabelle’s Sledgehammer. These evars are then instantiated by the solvers.
   Evars in predicate parameters can occur in side conditions, which then affect the reasoning
process. First, we simplify side conditions. Then, if the side condition is an equation, we apply
unification only when one side of the equation is an evar. It provides more confidence to believe
the instantiation is correct. For any other side conditions, the reasoner uses Isabelle’s built-in tactic
auto to instantiate evars, which involves a limited strategy for unsafe instantiation, correctable
by manual intervention.
   RefinedC [64] employs a hybrid heuristic. First, it seals the created evars wherever possible to
prevent premature instantiation due to Coq unification. When an evar occurs a side condition,
which is an equation, RefinedC removes the seal and tries to unify the equation’s two-hand sides,
which can badly instantiate some evar, causing a provable goal to be unprovable without manual
intervention. For other forms of side conditions, RefinedC can use a set of user rules to simplify the
conditions into a unifiable form. Our system attempts to simplify and unify conditions in roughly
equivalent places, although using the built-in capabilities of Isabelle’s auto or Sledgehammer.
   Diaframe [50] includes a particularly strong reasoning system for deferring the introduction of
evars, due to their frequent folding and unfolding of invariants. As the authors note [50], ordering
problems between the introduction of evars (through elimination of existential quantifiers) and the
automated unfolding of predicates (which may introduce new quantifiers with conflicting scopes)
can threaten the completeness of automation strategies without backtracking. Our automation
simply eliminates existential quantifiers eagerly — RefinedC reports an analogous goal-directed
approach [64]. This approach makes particular sense for us since we currently manually annotate
all predicate unfolding points — ordering issues can be addressed by moving the position of the
existing annotation. We leave further automation of predicate unfolding, and related solutions for
handling existential quantifiers, to future work.

9 Automatically Proving the Algebraic Properties of Predicates
Section § 8 has completed the formalization of our SL reasoner. However, this does not conclude
our work. The SL reasoner requires users to provide the algebraic properties of their predicates,
which still demands manual effort. To minimize this effort, this section presents algorithms for

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                               67:21


automatically proving the algebraic properties of predicates, aiming to limit the manual effort to
specifying the arguments of the algebraic properties and to proving FOL proof obligations.
  The algebraic properties involved in the paper — IEI , IEE , Tr, TF, SH, SA, SD, S1, S0 — are
defined based on SL entailments belonging to E (cf. § 8.1). We name these entailments as their
definitional entailments. To prove a property, it suffices to prove its definitional entailment. Let
us first consider non-recursively defined predicates. The algorithm for proving a property P of a
predicate (operator) 𝑇 is generically formalized as follows.
Routine 3 (Proving a property P for a non-recursively defined predicate (operator) 𝑇 ).
 (1) Construct the definitional entailment of P, denoted as 𝜙 −→ 𝜓 .
 (2) Unfold the definition of 𝑇 in 𝜙,𝜓 , resulting in formulas 𝜙 ′,𝜓 ′ comprising connectives and the
     component predicates used to define 𝑇 .
 (3) Send the entailment 𝜙 ′ −→ 𝜓 ′ to our SL algorithm described in § 8 and § 6, which uses
     algebraic properties of the component predicates to prove the entailment.
As an instance, and also as an exception requiring specific handling, the algorithm for proving
Functor property is formalized as follows.
Routine 4 (Proving Functor(𝐹, 𝑚, 𝑑), for a non-recursive predicate 𝐹 ). Given (𝐹, 𝑠, 𝑧), in order
to prove Functor(𝐹, 𝑚, 𝑑), the routine first constructs TF’s definitional entailment 𝑥 ⦂ 𝐹 (𝑇 ) −→
𝑚(𝑓 )(𝑥) ∗𝐹 (𝑈 ), fixing 𝑥 ∈ dom(𝑚(𝑓 )). Then 𝐹 is unfolded in the formula sending the resulting en-
tailment to the SL algorithm described in §8 and §6, after prepending the TP rule TP(𝑇 ,𝑈 ,𝐷Axiom
                                                                                             ′ )←(𝐷 ′ ⊆𝐷,𝑓 )

into the sequence ℜ of the rules used by the TP/bi-TP solver Routine 1. The registration of the TP
rule is the only difference between the routine and the generic process Routine 3.
   Since our SL algorithm accepts only entailments belonging to E, it restricts the algorithms above
to support only predicates whose definitions are within S. For other predicates, their properties
must be proven manually. In our case studies, only two predicates have definitions that fall outside
S: the identity refinement Id axiomatically introduced in §4, and the stepwise refinement operator
(𝑇 ; 𝑈 ) which is also defined in § 4. Readers may recall 𝑥 ⦂ Ref 𝑎 (𝑇 ). In our implementation, it is
actually defined using the stepwise operator (𝑇 ; 𝑈 ).
   For recursively defined predicates, the automatic proving is complicated because it is necessary
to use induction in the proofs. We adopt an intuitive but not necessarily complete strategy for
induction. To keep the discussion simple, we introduce a lemma stating that any formula in S can
be equivalently represented into a predicate application form 𝑦 ⦂ 𝑈 . It allows us to represent a
recursive definition as 𝑥 ⦂ 𝑇 ≜ 𝑓 (𝑥) ⦂ 𝐹 (𝑇 ) for some 𝑓 , 𝐹 . We assume a well-founded recursion
mechanism is provided in the underlying proof assistants, allowing this recursive definition. Our
implementation uses Alexander’s work [41]. We also assume the mechanism generates the well-
founded relation R that orders the arguments in the recursive calls of 𝑇 . The induction rule of 𝑇
has the following form: For any proposition 𝑃 about 𝑥 ⦂ 𝑇 ,
                  𝑃 (𝑥 ⦂ 𝑇 ) holds, if for any 𝑦 such that 𝑦 R 𝑥, 𝑃 (𝑦 ⦂ 𝑇 ) holds
                                                                                   (Ind)
                                      𝑃 (𝑥 ⦂ 𝑇 ) holds for any 𝑥
The definitional entailments of our algebraic properties take one of two forms:
                          (I). 𝑥 ⦂ 𝑇 −→ ℎ(𝑥) ⦂ 𝑈          (II). 𝑥 ⦂ 𝑈 −→ ℎ(𝑥) ⦂ 𝑇
for certain ℎ and 𝑈 . Note that 𝑇 may occur in the expression of 𝑈 . Let us consider form (I) only as
the case in form (II) is symmetric.
   Initiate a definitional entailment in form (I) as the initial proof goal. Our algorithm first applies
rule Ind, instantiating 𝑃 as 𝜆𝑋 . (𝑋 −→ ℎ(𝑥) ⦂ 𝑈 ). This results in the following proof state.

                             Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:22                                    Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


                    Inductive Hypothesis (IH): ∀𝑎 ∈ pre(𝑥). 𝑎 ⦂ 𝑇 −→ ℎ(𝑎) ⦂ 𝑈
                                  Proof Goal: 𝑥 ⦂ 𝑇 −→ ℎ(𝑥) ⦂ 𝑈
Here, pre(𝑥) ≜ {𝑦 | 𝑦 R 𝑥 } denotes the set of elements related to 𝑥 by 𝑅 + , where R + is the strict
                         +

transitive closure of R. Next, in order to leverage the IH, which applies to the strict antecedents
of 𝑥, our algorithm unfolds 𝑥 ⦂ 𝑇 , resulting in,
                                 Proof Goal:         𝑓 (𝑥) ⦂ 𝐹 (𝑇 ) −→ ℎ(𝑥) ⦂ 𝑈 .
Our algorithm requires that 𝐹 is a functor and to provide property Functor(𝐹, 𝑚, 𝑑). The property
can be synthesized automatically by using Functor composition, following the process in §2. From
this functor property and the IH, our algorithm deduces a lemma 𝑓 (𝑥) ⦂ 𝐹 (𝑇 ) −→ 𝑚(ℎ)(𝑓 (𝑥)) ⦂
𝐹 (𝑈 ) and produces a proof obligation 𝑑 (𝑓 (𝑥)) ⊆ pre(𝑥). Given this lemma, to show goal (9), it
suffices to show that
                            Proof Goal:         𝑚(ℎ) (𝑓 (𝑥)) ⦂ 𝐹 (𝑈 ) −→ ℎ(𝑥) ⦂ 𝑈 .
Recall that 𝑇 may occur in the expression of 𝑈 . Because we have unfolded 𝑇 on the left-hand side
once in step 9, the occurrences of T there have a recursion depth one level lower than those in U
on the right-hand side. To balance this, our algorithm performs a single-level unfolding for every
occurrence of 𝑇 in 𝑈 on the right-hand side, thus equalizing the recursion depth on the two sides.
  At this point, the algorithm assumes that all reasoning processes about induction have been
completed. This assumption, while potentially incorrect, allows the algorithm to proceed; if it is
not true, the algorithm is still sound but incomplete. Given this assumption, our algorithm then
passes the proof goal to the SL entailment algorithm formalized in §8 and §6, following the same
process for non-recursive predicates.

10      Evaluation and Case Studies
In this section, we perform an evaluation to: (1) Validate the feasibility of the reasoner in verifying
real data structures and algorithms written in an imperative language having a block memory
model that resembles CompCert. (2) Demonstrate that our approach indeed reduces the need for
manually crafting predicates’ reasoning rules (in terms of refinement-type system, manual typing
rules). (3) Evaluate the degree of automation of the generic reasoner. We show that the result
is similar to the state-of-the-art works. (4) Demonstrate the effectiveness of our algorithms for
proving the algebraic properties. The algorithms automate the verification condition generation
for all properties in the case studies in this section and ∼95% of the properties used in our system
implementation.

10.1     Implementation Details: Semantic Formalization and Fictional Separation
To perform the evaluation, we formalize our theory in Isabelle/HOL [53], implement the automa-
tion algorithms based on a semantics formalized in Isabelle/HOL, and evaluate the reasoner on
592 lines of programs involving 10 different data structures, from usual structures like linked lists
to more challenging ones, such as AVL trees and bucket hash maps. As a side note, our imple-
mentation is based on an 𝑠𝑝-transformer for the sake of symbolic execution, which is essentially
equivalent to the 𝑤𝑝-transformer.
   The semantics of our generic heap language supports pointer arithmetic, the address-of oper-
ator for memory objects, and fixed-size integers. The memory model is based on a map (block ×
offset → byte) from memory blocks and offsets to the base addresses of the blocks to bytes.
A pointer is represented as a pair (block × offset) (this resembles the basic CompCert memory
model [45]). Using a pointer (blk, ofs) to access a location beyond the boundaries of the block blk
of the pointer always fails, and pointer comparison between pointers of different memory blocks

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                67:23


                         Table 2. Property derivation of selected predicate operators.

               Operator(s)       Abst.     Tr     IE    TF     SH     SD/SA/S1      R     R′     M M′
                Record           tuple      0     0      0      0      ×/0/0        20    25     0    0
             Variable, Ref      identity    0     0      0      0      0/0/0        6,6   0,2    0   0,4
             Quantifier  ∗        map       0     0      0      0      0/0/0        19    38     2    0
              Array Slice          list     0     0     3+1     0      0/×/0        25     4     4    0
              Linked List          list     0     0      0      ×        ×           9     0     0    0
            Dynamic Array          list    3+1    ×      0      ×        ×           7     4     0    0
             Binary Tree          tree      0     0     1+1     ×        ×          10     8     0    0
             Search Tree          map      3+3    0     2+1     ×        ×           5     0     0    0
             Lookup AVL           map      3+3    0      0      ×        ×           5     0     0    0
             Bucket Hash          map      2+8    ×    14+9     ×        ×           7     0     0    0

                     Table 3. Evaluation of our verification framework over the cases.

   Group (#)       M/M ′ R/R ′     Prop Anot Fold Othr Prf Aux Ovh                Ovh∗     LoC          Time
  Rational (4)     0/0     20/358 0.02     0.37   0.37 0      0   0 0.40       -     43 0.4s + 2.9min + 3s
 Link-List (10)    0/0     48/1120 0.04    0.19   0.19 0      0   0 0.24 0.25 [64] 67 0.3s + 0.7min + 8s
 Quicksort (1)     0/0     57/750    0     0.39     0    0 0.33 0 0.72 4.95 [70] 18 0.5s + 3.4min + 50s
Bin. Search (2)    0/0     32/706    0     0.24     0    0    0   0 0.24 0.60 [64] 33 0.3s + 1.0min + 12s
Dyn. Array (8)     0/0     87/3838 0.05    0.19   0.18 0      0   0 0.24 0.19 [65] 62 2.5s + 3.1min + 53s
   Matrix (6)      0/0     56/1200 0.05    0.36   0.15 0 0.03 0 0.44 2.86 [69] 39 0.6s + 0.6min + 20s
Strassen Al. (2)   2/8     68/4168 0.03    0.26   0.09 0.17 0.43 0 0.72        -     65 2.4s + 3.6min + 47s
Binary Tree (3)    0/0     47/3174 0.07    0.41   0.41 0 0.03         1.34 1.07 [64] 46 0.7s + 3.6min + 22s
                                                                 0.84
 AVL Tree (3)      0/0    60/20533 0.06    0.27   0.27 0 0.11         1.28     -     106 6.8s + 6.2min + 201s
Buck. Hash (11)    0/0    102/3747 0.08    0.31   0.09 0.04 0.12 0 0.51 2.44 [13] 113 3.7s + 6.3min + 23s


always returns false. These simplifying assumptions mean that we do not grapple with complex
questions of pointer provenance that are raised by program logics over a fully-faithful C semantics
with undefined behaviour [64].
   We also do not support concurrency [16, 38], address-of operator for local variables, goto, loose
expression evaluation ordering [22], and first-class function pointers. However, we believe a low-
level block memory model is still sufficient to examine the degree of automation for an SL reasoner.
   Fictional separation is also supported by our system in basic form. This allows us to write
assertions with separating conjunction over an abstract fictional memory of records with fields,
and relate them to assertions about the underlying concrete memory layout. We follow Jensen
and Birkedal’s Fictional Separation Logic [35], which is designed for sequential reasoning and
perfectly matches our needs. It introduces two PCMs, one for abstract representations (called
fictions), and another for concrete resources. Denote the PCMs by A and C. A usual assertion
logic of SL (also known as Bunched Implications) is built over the fictional PCM A, i.e., A is
the model of the assertion logic, and its assertions are about fictions. So-called fictional interpreta-
tion 𝐼 : A → 2 C is a map from fictions to sets of concrete representations. It converts assertions
about fictions into assertions about concrete resources. For further details, we refer readers to their
work [35]. In our work, the concrete PCM C encompasses the concrete memory model, and the
fictional PCM A encompasses an abstract memory model (logical-address → permission × value)
where we associate logical addresses with permissions and high-level value representations. The
logical-address ≜ (block × field-name list) uses a path of field names to locate the address of a
field entry. The value is an algebraic data type that deep-embeds integers, arrays, structures, and

                              Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:24                                    Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


their combinations. The permission ≜ (positive rational) annotates the ownership of each logical
address. Permission modality ⨸ is implemented based on it, (𝑤 |= 𝑥 ⦂ 𝑛 ⨸ 𝑇 ) = (𝑤 ′ |= 𝑥 ⦂ 𝑇 ),
where 𝑤 ′ (𝑎) = (𝑝, 𝑣) iff 𝑤 (𝑎) = (𝑛𝑝, 𝑣). The fictional interpretation 𝐼 involves 1) how we translate
logical addresses to physical addresses and how to represent values as bytes; 2) constraining the
sum of permissions of every reference to equal 1. As we discuss in §12, we aim to extend our logic
with further fictions in future work.

10.2    Evaluation
The property derivation for the 10 data structures and a modality (the multiplicative quantifier
∗) is detailed in Table 2. The verification condition generation for all the properties is automatic.
Users only need to specify the expression of the properties and to prove any Isabelle/HOL proof
obligations failed to be proven by ATPs.
   In Table 2, Abst denotes the abstract representations used in the refinements of the data struc-
tures. (×) indicates that the property does not hold for the operator. 𝑛+𝑚 denotes that the deriva-
tion generates pure proof obligations that are solved automatically using 𝑛 tactic hints and 𝑚 tactic
arguments. If the proof is fully automated without any hints or arguments needed, we write 0. R
denotes the number of rules that are instantiated from algebraic properties and are used at least
once in verifying programs. R ′ denotes the number of such rules used in deriving other prop-
erties. M denotes the number of handcrafted rules. M ′ denotes the number of lines of manual
configurations required for the derived rules.
   The verification for the programs is detailed in Table 3. Specifications of the programs entail
refinements relating the programs to abstract representations. For example, the insert operations
in the lookup AVL and the bucket hash are related to the same abstraction, update of partial maps,
     {𝑓 ⦂ AVLptr (𝑇 ) ∗ 𝑘 ⦂ val(N) ∗ 𝑥 ⦂ val(𝑇 )} insert_AVL(ptr, 𝑘, 𝑣) {𝑓 (𝑘 ↦→ 𝑥) ⦂ AVLptr (𝑇 )}
   {𝑓 ⦂ Hashptr (𝑇 ) ∗ 𝑘 ⦂ val(N) ∗ 𝑥 ⦂ val(𝑇 )} insert_Hash(ptr, 𝑘, 𝑣) {𝑓 (𝑘 ↦→ 𝑥) ⦂ Hashptr (𝑇 )}.
These specifications cover partial correctness only. The support for total correctness is left to future
works as it demands a predicate property for order-preserving.
   In Table 3, routines are grouped, and their number in each group is labeled in parentheses.
Column LoC shows the number of lines in the source code. Most other metrics are based on the
number of lines and presented as ratios relative to LoC. These include:Prop, which represents man-
ual specifications and proofs for the algebraic properties required by the cases (subtyping rules of
the dynamic array and hash table are not required in verifying their operations); Anot, covering all
annotations; Fold, annotations specifically for folding and unfolding predicates; Othr, other annota-
tions excluding Unfold and loop invariants. Prf, manual proofs for proof obligations; Aux, auxiliary
Isabelle/HOL theories for the abstract representations used in the refinements. If Aux = 0, the ab-
stract representations come from Isabelle system libraries. Ovh = Property + Annot + Prf + Aux,
measuring the ratio of overhead to LoC. Ovh∗ is the best Ovh for the same kind of data structures
and algorithms (but not the same implementation) found in the literature of SL-based verification
for real languages, with citations in brackets. (-) indicates that the case or its statistics are not
observed in the literature or released sources, to the best of our knowledge.
   Time given in format 𝑎 + 𝑏 + 𝑐 denotes the time taken to verify the programs from scratch.
Portion 𝑎 is the time taken in applying the SL rules in the reasoner (§6 and §8), while portions 𝑏 +𝑐
concern the time taken to discharge proof obligations arising during the reasoning process. Portion
𝑏 represents proof search - first with basic tactics like auto, then with Isabelle’s Sledgehammer if
otherwise unsuccessful. Once a proof script is found by this search, it is cached for future use -
the invocation of Sledgehammer and subsequent caching are fully automated by our framework.
Portion 𝑐 represents the time taken to verify a proof script originally discovered in portion 𝑏.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                               67:25


Because of our caching, replaying the same verification (e.g. validating a previous result) takes
only time 𝑎 + 𝑐. Times are measured on an Intel i9-13900K CPU (16 cores) with 32 GB memory.
   Annotations. Among the annotations used in the case studies, 64% are used for folding and un-
folding predicates, which constitute the largest portion as shown in column Unfold, and 25% are
used for loop invariants, while only 11% are used to guide the reasoning process. Different from ex-
isting methods equipped with automatic mechanisms to (un)fold definitions, our reasoner never
silently unfolds predicates and requires any (un)folding to be explicitly annotated. Fortunately,
writing these (un)folding annotations is not as challenging as providing reasoning guidance anno-
tations. Instead, it can be more straightforward because folding and unfolding are usually used in
pairs when the reasoning involves the internal implementations of data structure operations. Al-
though our reasoner preserves predicate abstractions, unfolding is unavoidable to verify internal
implementations; otherwise, there is no way to verify them.
   Generation of reasoning rules. Certainly, any individual case study can be automated using a
tailored heuristic and hand-crafted reasoning rules. However, the key distinction of our work lies in
its generality: all the case studies are automated by one generic algorithm, using rules automatically
instantiated from one theory about algebras of refinement transformations and relying on barely
no manually-written ad-hoc rules for predicates, except for those directly handling primitive types
like fix-size integers.
   Including the entire system implementation, our SL reasoner incorporates ∼300 rules for trans-
forming predicates (which correspond to typing rules in refinement type systems). Of these, ∼80%
are generated automatically, while remains are ad-hoc rules for specific predicates, which are typ-
ically predicate counterparts of connectives such as ∨, ∧, ∗, and if-then-else.
   Regarding the case studies listed in this section, column R presents the number of distinct instan-
tiated rules used in the verification; R ′ indicates the total times of their applications. Columns M
and M ′ represent the numbers of manually written rules and annotations to apply them, respec-
tively. This suggests our method almost eliminates the need for manual rules in the case studies.
The two manual rules are used for splitting and merging matrix into and from four sub-matrixes in
Strassen’s algorithm. The rules are manually specified but automatically derived, after unfolding
the matrix abstractions into two-dimensional arrays. The eight manual applications are for apply-
ing them. The rules are not automated because (1) the scalars of matrixes are two-dimensional
intervals whose addition is not associative, and (2) our reasoner does not support slicing for non-
associative scalar addition.
   Non-trivial transformations by generated rules are essential in the case studies.
   For instance, let’s consider the access to a field of a record in memory. Recall that 𝑥 ⦂ {a:𝑇 }
specifies a record having a field 𝑎 and the field has a value refining 𝑥 w.r.t. 𝑇 ; we use {a:𝑇 } ∗ {b: 𝑈 },
abbreviated as {a:𝑇 , b: 𝑈 } to represent a record of two fields; 𝑎.𝑏 is a path (§ 5.3) to a field in a
nested record. From the definitions of Ref and val in Fig. 4 we specify a load operation as {𝑥 ⦂
Ref addr {a:𝑇 }}load(addr.a){𝑣. 𝑥 ⦂ Ref addr {a:𝑇 } ∗ 𝑥 ⦂ val𝑣 𝑇 }. Given a program state specified by
((𝑥, 𝑦), 𝑧)⦂Ref addr {a: {b:𝑇1, c:𝑇2 }, d:𝑇3 }, the load operation of the field 𝑎.𝑏 requires to transform the
state specification to (1. 𝑥 ⦂ Ref addr {a.b:𝑇1 }) ∗ (2. (𝑦, 𝑧) ⦂ Ref addr {a: {c:𝑇2 }, d:𝑇3 }), so that we can
apply the triple of the load by using the frame rule to frame out (2). This transformation requires
properties SH of Ref, SH of 𝜆𝑇 . {a:𝑇 }, and also SA of 𝜆𝑇 . {a:𝑇 } that allows {a: {b:𝑇 }} = {a.b:𝑇 }.
   SD is necessary in the case study of Quicksort. As a divide-and-conquer algorithm, a key step
of Quicksort is to divide (the abstraction of) an array slice into two and send them respectively to
recursive calls. The divide and merge of the slices require the SD property of array slices (§5.3).
   As our third instance, Strassen’s matrix multiplication is another divide-and-conquer algorithm.
The partitioning of matrix slices in this algorithm requires SD and SH, as discussed in §6.6.


                             Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:26                                    Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu

   The fourth instance is the use of scalar unit property S1 in Bucket Hash. A bucket hash contains
a sequence of buckets, and each bucket is represented by a dynamic array. In the case study, we
                                                   ∗
use finite separating quantifier {𝑥𝑖 }𝑖 ∈𝐼 ⦂ 𝑖 ∈𝐼 𝑇𝑖 ≜ (𝑥 1 ⦂ 𝑇1 ∗ · · · 𝑥𝑛 ⦂ 𝑇𝑛 ) for 𝐼 = {1, · · ·, 𝑛}, to
collet the sequence of the buckets. To access the 𝑘 th bucket represented as 𝑥𝑘 ⦂ 𝑇𝑘 , it requires a
                             ∗                            ∗
transformation {𝑥𝑖 }𝑖 ∈𝐼 ⦂ 𝑖 ∈𝐼 𝑇𝑖 −→ {𝑥𝑖 }𝑖 ∈𝐼 \{𝑘 } ⦂ 𝑖 ∈𝐼 \{𝑘 }𝑇𝑖 ∗𝑥𝑘 ⦂𝑇𝑘 . This transformation is derived
from the properties S1 and SD of .       ∗
   The efficiency of our algorithm is estimated by corre-
                                                                         380
lating the number of rule applications against the number apps                                95th percentile
of connectives and predicate operators in reasoning every                                     regression
step of program operation (Fig. 8). We use the number of                 300
rule applications because it is a fair indicator independent
of specific implementations to measure the time cost of the              200
reasoning process. The time for a single rule application is
generally constant and takes <0.15ms in our implementa- 100
tion. Although the theoretical time complexity is at least
quadratic due to the bi-abduction process (§8), the statistics
                                                                           0
show the actual efficiency is much better than the theoreti-
                                                                               0     25    50    75 operators
cal worst-case quadratic time. In practice, our method is fast
because predicate operators form expression trees. The rea- Fig. 8. Each point represents a bi-EP in-
soning process is segmented by tree hierarchies, with each stance. The X-axis is the number of type
segment focusing solely on the children of each tree node. operators and connectives in this bi-EP;
When the number of children (i.e., components in a hierar- the Y-axis is the number of applications
chy, such as fields in a record) remains constant relative to of rules used to solve the bi-EP.
the scale of the entailment formula, a linear result emerges.
   The degree of automation. Before any discussion, we must acknowledge that the degree of
automation in foundational verification cannot be simply measured by lines of code or annota-
tions. Considerable differences exist in semantic formalizations and the automation capabilities
provided by underlying proof assistants. Moreover, the manual effort for debugging the reasoning
and providing guidance annotations is more arduous than adding (un)folding-annotations that are
generally placed at the beginning or end of internal operations. Although quantitatively measuring
the degree of automation in foundational verification is challenging, columns Ovh, Ovh* suffice to
show that the instantiated automation from our generic reasoner is at least comparable with the
state-of-the-art works based on specially designed reasoning rules and heuristics. Importantly, our
automation stems from a general theory with automatically instantiated rules, conferring better
generality than existing methods.



10.3    Qualitative Comparison
One weakness of our tool in comparison to related works is our reliance on explicit predicate
(un)folding annotations. Regarding the case studies discussed above, recent works, particularly
RefinedC and Quiver, have achieved a high degree of automation here, with almost no annotation
(except loop invariants) required.
   For example, the maintenance routine in AVL involves 4 branches to determine which subtrees
should be rotated. When different subtrees are rotated, different predicates should be unfolded,
which in our tool requires unfolding and folding notations in each branch. Worse, the routine has
multiple return statements, each one in a branch, causing a predicate unfolded by one annotation
to require multiple annotations to fold it back. Consequently, the routine requires 5 unfolding

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                               67:27

annotations and 11 folding annotations. Our unfolding annotations are not smart enough to case-
split algebraic data types, causing 4 additional lines to be required to specify the proper shape of
the abstract tree representations. Finally, 20 lines are used for the annotations.
   As we discuss in §8.4, automatic predicate unfolding strategies of other tools present additional
complications for the syntax-directed handling of ∃-quantification and evars. We believe that our
system can be extended with more ambitious automatic predicate unfolding, although this would
mean that these related challenges would also need to addressed.
   Regarding loop invariants, all discussed tools require some manual annotation. In particular,
both our work and RefinedC require users to specify the invariant refinement relations (refinement
types) of variable states and constraints about the abstract representations (the values of the types).
   While our work is focussed on the automatic derivation of predicate transformations wherever
possible, our tool is not able to automatically derive the predicate transformations necessary to
split and merge the matrix slices of the Strassen’s algorithm example (see § 10.2). Like existing
tools, we must instead prove and apply the relevant predicate transformations ourselves — in our
case requiring 10 additional lines of proof annotation.
   Except for these, all the remaining annotations are used to manually prove FOL side conditions
that cannot be automated. For a side condition, our reasoner first tries to use Isabelle’s built-in
tactic auto to automatically prove or disprove it within a time limit. If the solver neither proves
nor disproves it within the time limit, it will be printed on the screen, and our reasoner proceeds
by assuming it is false. If it is actually true, the reasoning can fail. In this case, users must manually
prove the side condition and register it with our system, so that the reasoner can apply the proper
rule guarded by the condition. Manual effort is also required to prove side conditions in RefinedC.
Users need to annotate tactics that augment the default solver to prove the side conditions that fail
to be automated. Both our and their solvers can be improved to reduce these these annotations.
   The SL used in our work also has expressiveness deficiencies compared with tools [23, 50, 64, 65]
built on rich SLs like Iris. Our logic does not support higher-order fiction, higher-order ghost states,
and the later modality. It would be interesting to investigate how to apply our algebraic system to
later modality, ghost states, update modality, and other connectives specific to these rich logics.
   We highlight earlier sections where we make relevant qualitative comparisons to related tools:
handling of ∃-quantification and evars (§ 8.4); and discrepancies between the semantics such as
our lack of concurrency or provenance support (§10.1). See our discussions in Related Work (§11)
on bi-abduction uses and expressivity of the logic in comparison to other tools.


11   Related Work
Regarding SL-based foundational verification, the literature contains a wealth of related work. Based
on these works, our main advancement is an algebraic approach to generating reasoning rules of
non-trivial transformations. The generation is generic for any predicates satisfying certain alge-
braic properties that can also be automatically proven by our method.
  RefinedC [64] is a foundational verifier for a major fragment of the C language. It provides an
impressive degree of automation comparable to non-foundational tools while being based on an
expressive separation logic, Iris [37]. Two key components contribute to its automation capability.
  One component is the separation logic programming engine, Lithium, which provides a non-
backtracking reasoning mechanism for deriving SL entailments. Lithium has significantly influ-
enced our work. The syntax of our reasoner (§8.1) is essentially borrowed from Lithium’s syntax.
Our reasoning process (Fig. 5) for eliminating connectives mirrors its goal-directed search.
  Another component is its refinement type system, which effectively handles low-level program-
ming idioms. A rich concept of subtyping is an important part of this system, allowing various

                             Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:28                                    Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu

refinement types to be applied to the same data structure. The transformations between predi-
cates studied in our work correspond to their subtypings. Their subtyping rules are given in a
𝑤𝑝-transformer form, which we simplify into implications between predicate applications. This
simplification enables us to develop the algebras of transformations between refinements, form-
ing the basis of our algebraic method for rule generation.
   While rules for user-defined types derived by RefinedC are (un)folding rules, our approach fur-
thermore automatically generates subtyping rules and other non-trivial transformation rules for
both user-defined and system predicates. These instantiated rules are powerful enough to con-
stitute the core of our SL reasoner. The reasoner demonstrates a promising level of automation,
which in many cases is similar to that of RefinedC’s reasoner, despite RefinedC’s use of manually
crafted typing rules. However, RefinedC’s memory model involves more complicated matters like
provenance, padding of structures, and pointer alignment constraints. It would be interesting to
investigate how our rule generation system benefits manually proven rules in RefinedC.
   Diaframe [50] is a more recent tool for automating foundational verification on top of Iris.
Both Diaframe and RefinedC are based on ideas from linear logic programming and share some
common methods for reasoning about certain logic connectives. Similarly to RefinedC’s typing
rules, Diaframe’s automation power depends on an extensible set of hints. A Diaframe hint is
essentially a reasoning rule that plays a similar role to our bi-TP rules, and also uses a similar bi-
abduction technique for a similar purpose — answering which part of the source assertion can be
transformed to which part of the target assertion, and what is left and missing after this transfor-
mation. To extend Diaframe’s automation capability on new predicates, new hints must be crafted
and proven manually. This is where our generic theory of rule generation could be potentially
beneficial. Where Diaframe relies on manually crafted hints, our theory could potentially help it
to identify useful hints and generate hints automatically. On the other hand, Diaframe additionally
automates Iris-specific modalities and ghost state updates, which we have not considered yet, and
many of its discussed examples are on concurrent programs, which we currently do not handle. In
future work, we hope to investigate the composition of our techniques with theirs.
   Quiver [65] is a recent foundational verifier for C that aims to reduce specification overhead by
automatically inferring functional correctness specifications. It is also based on the separation logic
Iris and the same semantic formalization Caesium [64] with RefinedC. Quiver extends RefinedC’s
approach in two key ways: it enhances the refinement type system to work under incomplete in-
formation about the proof context, and it introduces bi-abduction to infer complete specifications
from partial specification sketches provided by users. While Quiver uses bi-abduction for spec-
ification inference, our work employs bi-abduction for a different purpose. We use it as part of
our reasoning process to decompose entailments between composite formulas into those between
predicate applications, which are then reduced to transformation problems. This allows us to apply
our reasoning rules generated from algebraic properties, to the transformation problems.
   RefinedRust [23], built on Iris logic, is a recent approach for verifying both safe and unsafe Rust
programs. RefinedRust adapts and enhances RefinedC’s refinement type system to accommodate
Rust-specific concepts such as borrowing, lifetimes, and “places”. Key innovations include borrow
names and place types, which enable Rust-specific reasoning about borrowed places.
   Islaris [63] is an Iris-based framework for verifying machine code against comprehensive and
authoritative instruction set architecture specifications for Armv8-A and RISC-V. It adapts Re-
finedC’s Lithium to a logic tailored for tracing instruction’s register and memory accesses.
   VST [1, 12] is an SL-based interactive tool for verifying CompCert [45] C programs. Its automa-
tion system is based on a symbolic execution aided by user annotations for intermediate assertions.
VST-A [75] extends VST by allowing users to write proofs in annotations directly.


Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                               67:29


  Bedrock [13–15, 46] is the initial work for SL-based foundational verification. Bedrock and VST
families encode specifications in plain separation logic without systematic use of refinement tech-
niques. Their automation depends on pre-defined heuristics and custom user tactics. In contrast,
we aim to propose a systematic theory for automating SL for almost any data structure.
   Beyond the works directly related to our approach, other foundational verification works based
on SL also make significant contributions in their respective domains [25–28, 36, 39, 47, 48, 58].
Additionally, there is also a wealth of non-foundational tools built on top of expressive SLs.
   CN [59] is a deductive verifier for C language aiming to bridge the gap between verification
techniques and real software development. It is based on a carefully designed refinement-type-
integrated SL where the produced logical constraints always fall into an SMT fragment known to
be decidable. More remarkably, it is built upon an accurate ISO C semantics validated on substantial
C test suites. This shows the feasibility of verifying a large fragment of ISO C.
   VeriFast [33] is an automated, separation logic-based functional correctness verifier for C and
Java. Its automation is also based on predefined or user-provided heuristics [71]. It does not pro-
vide a rule-generation mechanism for non-trivial transformations like ours.
   Finally, the literature also abounds in automatic solvers for specific fragments of separation logic.
This line of research began with symbolic heap [2], a decidable fragment of separation logic. Sub-
sequent works extend it by incorporating inductive predicates [20, 21, 43, 44, 67] and arrays [7],
introducing various automation techniques including superposition calculus [51], lemma synthe-
sis [34], model checking [8, 42], symbolic execution [3, 55], and SMT solvers [52, 56]. Initially, these
approaches focus on shape analysis for memory safety [4, 6, 9, 10, 34]. Subsequent works extend to
functional correctness on intermediate verification languages [32, 57, 60]. While these approaches
have made significant strides in automating reasoning for specific SL fragments, foundational ver-
ification often requires more expressive SLs, which is where our work aims to contribute.


12   Limitations and Future Work
Many refinements listed in Table 2 do not support SH. As explained in the end of § 5.2, this is
because the refinements are defined in a direct and simple manner, while the data structures
contain control structures that cannot be split and shared between separated abstractions under
these simple definitions. As an example of a consequence, we cannot easily verify concurrent
programs where portions of a hash map are owned by different threads. We plan to introduce a
modality based on fiction of disjointness [19, 35] in order to wrap any predicate into a separating-
homomorphic one. Similarly, many refinements in Table 2 do not support SD. We plan to develop
a modality for slicing any predicate, e.g., to slice the mapping abstraction of a hash table into
sub-mappings, so that different program modules can own and modify different sub-mappings.
   Based on other algebraic already defined, we plan to add the necessary automation for deriving
implications like (𝑙 1 ⦂Listaddr1 𝑇 ) ∗ (𝑙 2 ⦂Listaddr2 𝑈 ) −→ addr1 ≠ addr2, useful for pointer arithmetic.
   Besides, an automatic mechanism for (un)folding predicates definitions, and a mechanism for
inferring specifications of algebraic properties are also left to our future works.


Acknowledgements
This research is partially supported by the project MOE-T1-1/2022-43 (funded by Singapore’s Min-
istry of Education), EPSRC grant EP/Z000580/1. Conrad Watt and Qiyuan Xu are supported by an
NTU Nanyang Assistant Professorship Start-Up Grant. The early stage of this research was spon-
sored by Hangzhou Yunphant Network Technology Co. LTD. We are also grateful to the anony-
mous reviewers for their valuable comments. The artifact of this work is available in [72, 73].

                             Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:30                                      Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu

References
 [1] Andrew W. Appel, Robert Dockins, Aquinas Hobor, Lennart Beringer, Josiah Dodds, Gordon Stewart, Sandrine Blazy,
     and Xavier Leroy. 2014. Program Logics for Certified Compilers. Cambridge University Press, USA.
 [2] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2005. A Decidable Fragment of Separation Logic. In FSTTCS
     2004: Foundations of Software Technology and Theoretical Computer Science, Kamal Lodaya and Meena Mahajan (Eds.).
     Springer Berlin Heidelberg, Berlin, Heidelberg, 97–109.
 [3] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2005. Symbolic Execution with Separation Logic. In Pro-
     gramming Languages and Systems, Kwangkeun Yi (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 52–68.
 [4] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2006. Smallfoot: Modular Automatic Assertion Checking
     with Separation Logic. In Formal Methods for Components and Objects, Frank S. de Boer, Marcello M. Bonsangue,
     Susanne Graf, and Willem-Paul de Roever (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 115–137.
 [5] Torben Braüner. 2010. Hybrid Logic and its Proof-Theory. Springer Dordrecht. https://doi.org/10.1007/978-94-007-
     0002-4
 [6] James Brotherston, Dino Distefano, and Rasmus Lerchedahl Petersen. 2011. Automated Cyclic Entailment Proofs
     in Separation Logic. In Automated Deduction – CADE-23, Nikolaj Bjørner and Viorica Sofronie-Stokkermans (Eds.).
     Springer Berlin Heidelberg, Berlin, Heidelberg, 131–146.
 [7] James Brotherston, Nikos Gorogiannis, and Max Kanovich. 2017. Biabduction (and Related Problems) in Array Sepa-
     ration Logic. In Automated Deduction – CADE 26, Leonardo de Moura (Ed.). Springer International Publishing, Cham,
     472–490.
 [8] James Brotherston, Nikos Gorogiannis, Max Kanovich, and Reuben Rowe. 2016. Model checking for symbolic-heap
     separation logic with inductive predicates. In Proceedings of the 43rd Annual ACM SIGPLAN-SIGACT Symposium on
     Principles of Programming Languages (St. Petersburg, FL, USA) (POPL ’16). Association for Computing Machinery,
     New York, NY, USA, 84–96. https://doi.org/10.1145/2837614.2837621
 [9] Cristiano Calcagno and Dino Distefano. 2011. Infer: An Automatic Program Verifier for Memory Safety of C Programs.
     In NASA Formal Methods, Mihaela Bobaru, Klaus Havelund, Gerard J. Holzmann, and Rajeev Joshi (Eds.). Springer
     Berlin Heidelberg, Berlin, Heidelberg, 459–465.
[10] Cristiano Calcagno, Dino Distefano, Peter O’Hearn, and Hongseok Yang. 2009. Compositional shape analysis by
     means of bi-abduction. SIGPLAN Not. 44, 1 (jan 2009), 289–300. https://doi.org/10.1145/1594834.1480917
[11] Cristiano Calcagno, Peter W. O’Hearn, and Hongseok Yang. 2007. Local Action and Abstract Separation Logic. In 22nd
     Annual IEEE Symposium on Logic in Computer Science (LICS 2007). 366–378. https://doi.org/10.1109/LICS.2007.30
[12] Qinxiang Cao, Lennart Beringer, Samuel Gruetter, Josiah Dodds, and Andrew W. Appel. 2018. VST-Floyd: A Separation
     Logic Tool to Verify Correctness of C Programs. Journal of Automated Reasoning 61, 1 (01 Jun 2018), 367–422. https:
     //doi.org/10.1007/s10817-018-9457-5
[13] Adam Chlipala. 2011. Mostly-automated verification of low-level programs in computational separation logic. SIG-
     PLAN Not. 46, 6 (jun 2011), 234–245. https://doi.org/10.1145/1993316.1993526
[14] Adam Chlipala. 2013. The bedrock structured programming system: combining generative metaprogramming and
     hoare logic in an extensible program verifier. SIGPLAN Not. 48, 9 (sep 2013), 391–402. https://doi.org/10.1145/2544174.
     2500592
[15] Adam Chlipala. 2015. From Network Interface to Multithreaded Web Applications: A Case Study in Modular Pro-
     gram Verification. In Proceedings of the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Program-
     ming Languages (Mumbai, India) (POPL ’15). Association for Computing Machinery, New York, NY, USA, 609–622.
     https://doi.org/10.1145/2676726.2677003
[16] Hoang-Hai Dang, Jacques-Henri Jourdan, Jan-Oliver Kaiser, and Derek Dreyer. 2019. RustBelt meets relaxed memory.
     Proc. ACM Program. Lang. 4, POPL, Article 34 (dec 2019), 29 pages. https://doi.org/10.1145/3371102
[17] Thibault Dardinier, Peter Müller, and Alexander J. Summers. 2022. Fractional resources in unbounded separation logic.
     Proc. ACM Program. Lang. 6, OOPSLA2, Article 163 (Oct. 2022), 27 pages. https://doi.org/10.1145/3563326
[18] Thomas Dinsdale-Young, Lars Birkedal, Philippa Gardner, Matthew Parkinson, and Hongseok Yang. 2013. Views:
     compositional reasoning for concurrent programs. SIGPLAN Not. 48, 1 (jan 2013), 287–300. https://doi.org/10.1145/
     2480359.2429104
[19] Thomas Dinsdale-Young, Mike Dodds, Philippa Gardner, Matthew J. Parkinson, and Viktor Vafeiadis. 2010. Concurrent
     Abstract Predicates. In ECOOP 2010 – Object-Oriented Programming, Theo D’Hondt (Ed.). Springer Berlin Heidelberg,
     Berlin, Heidelberg, 504–528.
[20] Mnacho Echenim, Radu Iosif, and Nicolas Peltier. 2021. Decidable Entailments in Separation Logic with Inductive
     Definitions: Beyond Establishment. In 29th EACSL Annual Conference on Computer Science Logic (CSL 2021) (Leibniz
     International Proceedings in Informatics (LIPIcs), Vol. 183), Christel Baier and Jean Goubault-Larrecq (Eds.). Schloss
     Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 20:1–20:18. https://doi.org/10.4230/LIPIcs.CSL.2021.
     20


Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                       67:31

[21] Constantin Enea, Ondřej Lengál, Mihaela Sighireanu, and Tomáš Vojnar. 2017. Compositional entailment checking
     for a fragment of separation logic. Formal Methods in System Design 51, 3 (01 Dec 2017), 575–607. https://doi.org/10.
     1007/s10703-017-0289-4
[22] Dan Frumin, Léon Gondelman, and Robbert Krebbers. 2019. Semi-automated Reasoning About Non-determinism in
     C Expressions. In Programming Languages and Systems, Luís Caires (Ed.). Springer International Publishing, Cham,
     60–87.
[23] Lennard Gäher, Michael Sammler, Ralf Jung, Robbert Krebbers, and Derek Dreyer. 2024. RefinedRust: A Type System
     for High-Assurance Verification of Rust Programs. Proc. ACM Program. Lang. 8, PLDI, Article 192 (jun 2024), 25 pages.
     https://doi.org/10.1145/3656422
[24] David Greenaway, Japheth Lim, June Andronick, and Gerwin Klein. 2014. Don’t sweat the small stuff: formal verifica-
     tion of C code without the pain. In Proceedings of the 35th ACM SIGPLAN Conference on Programming Language Design
     and Implementation (Edinburgh, United Kingdom) (PLDI ’14). Association for Computing Machinery, New York, NY,
     USA, 429–439. https://doi.org/10.1145/2594291.2594296
[25] Ronghui Gu, Jérémie Koenig, Tahina Ramananandro, Zhong Shao, Xiongnan (Newman) Wu, Shu-Chun Weng,
     Haozhong Zhang, and Yu Guo. 2015. Deep Specifications and Certified Abstraction Layers. In Proceedings of the
     42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (Mumbai, India) (POPL ’15).
     Association for Computing Machinery, New York, NY, USA, 595–608. https://doi.org/10.1145/2676726.2676975
[26] Ronghui Gu, Zhong Shao, Hao Chen, Jieung Kim, Jérémie Koenig, Xiongnan (Newman) Wu, Vilhelm Sjöberg, and
     David Costanzo. 2019. Building certified concurrent OS kernels. Commun. ACM 62, 10 (sep 2019), 89–99. https:
     //doi.org/10.1145/3356903
[27] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan (Newman) Wu, Jieung Kim, Vilhelm Sjöberg, and David Costanzo.
     2016. CertiKOS: An Extensible Architecture for Building Certified Concurrent OS Kernels. In 12th USENIX Symposium
     on Operating Systems Design and Implementation (OSDI 16). USENIX Association, Savannah, GA, 653–669. https:
     //www.usenix.org/conference/osdi16/technical-sessions/presentation/gu
[28] Ronghui Gu, Zhong Shao, Jieung Kim, Xiongnan (Newman) Wu, Jérémie Koenig, Vilhelm Sjöberg, Hao Chen, David
     Costanzo, and Tahina Ramananandro. 2018. Certified concurrent abstraction layers. In Proceedings of the 39th ACM
     SIGPLAN Conference on Programming Language Design and Implementation (Philadelphia, PA, USA) (PLDI 2018). As-
     sociation for Computing Machinery, New York, NY, USA, 646–661. https://doi.org/10.1145/3192366.3192381
[29] Zhé Hóu, Rajeev Goré, and Alwen Tiu. 2015. Automated Theorem Proving for Assertions in Separation Logic with
     All Connectives. In Automated Deduction - CADE-25, Amy P. Felty and Aart Middeldorp (Eds.). Springer International
     Publishing, Cham, 501–516.
[30] Andrzej Indrzejczak. 2010. Natural Deduction, Hybrid Systems and Modal Logics (1 ed.). Springer Netherlands, Chapter
     11.2. https://doi.org/10.1007/978-90-481-8785-0
[31] Samin S. Ishtiaq and Peter W. O’Hearn. 2001. BI as an assertion language for mutable data structures. SIGPLAN Not.
     36, 3 (jan 2001), 14–26. https://doi.org/10.1145/373243.375719
[32] Shachar Itzhaky, Hila Peleg, Nadia Polikarpova, Reuben N. S. Rowe, and Ilya Sergey. 2021. Cyclic program synthesis. In
     Proceedings of the 42nd ACM SIGPLAN International Conference on Programming Language Design and Implementation
     (Virtual, Canada) (PLDI 2021). Association for Computing Machinery, New York, NY, USA, 944–959. https://doi.org/
     10.1145/3453483.3454087
[33] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. VeriFast: A
     Powerful, Sound, Predictable, Fast Verifier for C and Java. In NASA Formal Methods, Mihaela Bobaru, Klaus Havelund,
     Gerard J. Holzmann, and Rajeev Joshi (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 41–55.
[34] Christina Jansen, Jens Katelaan, Christoph Matheja, Thomas Noll, and Florian Zuleger. 2017. Unified Reasoning About
     Robustness Properties of Symbolic-Heap Separation Logic. In Programming Languages and Systems, Hongseok Yang
     (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 611–638.
[35] Jonas Braband Jensen and Lars Birkedal. 2012. Fictional Separation Logic. In Programming Languages and Systems,
     Helmut Seidl (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 377–396.
[36] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. RustBelt: securing the foundations
     of the Rust programming language. Proc. ACM Program. Lang. 2, POPL, Article 66 (dec 2017), 34 pages. https:
     //doi.org/10.1145/3158154
[37] Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and Derek Dreyer. 2018. Iris from the
     ground up: A modular foundation for higher-order concurrent separation logic. Journal of Functional Programming
     28 (2018), e20. https://doi.org/10.1017/S0956796818000151
[38] Jan-Oliver Kaiser, Hoang-Hai Dang, Derek Dreyer, Ori Lahav, and Viktor Vafeiadis. 2017. Strong Logic for Weak
     Memory: Reasoning About Release-Acquire Consistency in Iris. In 31st European Conference on Object-Oriented Pro-
     gramming (ECOOP 2017) (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 74), Peter Müller (Ed.). Schloss
     Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 17:1–17:29. https://doi.org/10.4230/LIPIcs.ECOOP.



                                 Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:32                                      Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu

     2017.17
[39] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock, Philip Derrin, Dhammika Elkaduwe,
     Kai Engelhardt, Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and Simon Winwood. 2009. seL4:
     formal verification of an OS kernel. In Proceedings of the ACM SIGOPS 22nd Symposium on Operating Systems Principles
     (Big Sky, Montana, USA) (SOSP ’09). Association for Computing Machinery, New York, NY, USA, 207–220. https:
     //doi.org/10.1145/1629575.1629596
[40] Gerwin Klein, Thomas Sewell, and Simon Winwood. 2010. Refinement in the Formal Verification of the seL4 Microkernel.
     Springer US, Boston, MA, 323–339. https://doi.org/10.1007/978-1-4419-1539-9_11
[41] Alexander Krauss. 2009. Automating Recursive Definitions and Termination Proofs in Higher-Order Logic. Ph. D. Dis-
     sertation. Technische Universität München. https://mediatum.ub.tum.de/681651
[42] Quang Loc Le. 2021. Compositional Satisfiability Solving in Separation Logic. In Verification, Model Checking, and Ab-
     stract Interpretation, Fritz Henglein, Sharon Shoham, and Yakir Vizel (Eds.). Springer International Publishing, Cham,
     578–602.
[43] Quang Loc Le, Jun Sun, and Shengchao Qin. 2018. Frame Inference for Inductive Entailment Proofs in Separation
     Logic. In Tools and Algorithms for the Construction and Analysis of Systems, Dirk Beyer and Marieke Huisman (Eds.).
     Springer International Publishing, Cham, 41–60.
[44] Quang Loc Le, Makoto Tatsuta, Jun Sun, and Wei-Ngan Chin. 2017. A Decidable Fragment in Separation Logic
     with Inductive Predicates and Arithmetic. In Computer Aided Verification, Rupak Majumdar and Viktor Kunčak (Eds.).
     Springer International Publishing, Cham, 495–517.
[45] Xavier Leroy. 2009. Formal verification of a realistic compiler. Commun. ACM 52, 7 (jul 2009), 107–115. https:
     //doi.org/10.1145/1538788.1538814
[46] Gregory Malecha, Adam Chlipala, and Thomas Braibant. 2014. Compositional Computational Reflection. In Interactive
     Theorem Proving, Gerwin Klein and Ruben Gamboa (Eds.). Springer International Publishing, Cham, 374–389.
[47] William Mansky and Ke Du. 2024. An Iris Instance for Verifying CompCert C Programs. Proc. ACM Program. Lang. 8,
     POPL, Article 6 (jan 2024), 27 pages. https://doi.org/10.1145/3632848
[48] Yusuke Matsushita, Xavier Denis, Jacques-Henri Jourdan, and Derek Dreyer. 2022. RustHornBelt: a semantic founda-
     tion for functional verification of Rust programs with unsafe code. In Proceedings of the 43rd ACM SIGPLAN Interna-
     tional Conference on Programming Language Design and Implementation (San Diego, CA, USA) (PLDI 2022). Association
     for Computing Machinery, New York, NY, USA, 841–856. https://doi.org/10.1145/3519939.3523704
[49] Kayvan Memarian, Victor B. F. Gomes, Brooks Davis, Stephen Kell, Alexander Richardson, Robert N. M. Watson, and
     Peter Sewell. 2019. Exploring C semantics and pointer provenance. Proc. ACM Program. Lang. 3, POPL, Article 67 (jan
     2019), 32 pages. https://doi.org/10.1145/3290380
[50] Ike Mulder, Robbert Krebbers, and Herman Geuvers. 2022. Diaframe: automated verification of fine-grained concur-
     rent programs in Iris. In Proceedings of the 43rd ACM SIGPLAN International Conference on Programming Language
     Design and Implementation (San Diego, CA, USA) (PLDI 2022). Association for Computing Machinery, New York, NY,
     USA, 809–824. https://doi.org/10.1145/3519939.3523432
[51] Juan Antonio Navarro Pérez and Andrey Rybalchenko. 2011. Separation logic + superposition calculus = heap theorem
     prover. SIGPLAN Not. 46, 6 (jun 2011), 556–566. https://doi.org/10.1145/1993316.1993563
[52] Juan Antonio Navarro Pérez and Andrey Rybalchenko. 2013. Separation Logic Modulo Theories. In Programming
     Languages and Systems, Chung-chieh Shan (Ed.). Springer International Publishing, Cham, 90–106.
[53] Tobias Nipkow, Markus Wenzel, and Lawrence C Paulson. 2002. Isabelle/HOL: a proof assistant for higher-order logic.
     Springer.
[54] Peter O’Hearn. 2019. Separation logic. Commun. ACM 62, 2 (jan 2019), 86–95. https://doi.org/10.1145/3211968
[55] Long H. Pham, Quang Loc Le, Quoc-Sang Phan, Jun Sun, and Shengchao Qin. 2019. Enhancing Symbolic Execution
     of Heap-Based Programs with Separation Logic for Test Input Generation. In Automated Technology for Verification
     and Analysis, Yu-Fang Chen, Chih-Hong Cheng, and Javier Esparza (Eds.). Springer International Publishing, Cham,
     209–227.
[56] Ruzica Piskac, Thomas Wies, and Damien Zufferey. 2013. Automating Separation Logic Using SMT. In Computer Aided
     Verification, Natasha Sharygina and Helmut Veith (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 773–789.
[57] Nadia Polikarpova and Ilya Sergey. 2019. Structuring the synthesis of heap-manipulating programs. Proc. ACM
     Program. Lang. 3, POPL, Article 72 (jan 2019), 30 pages. https://doi.org/10.1145/3290385
[58] Jonathan Protzenko, Jean-Karim Zinzindohoué, Aseem Rastogi, Tahina Ramananandro, Peng Wang, Santiago Zanella-
     Béguelin, Antoine Delignat-Lavaud, Cătălin Hriţcu, Karthikeyan Bhargavan, Cédric Fournet, and Nikhil Swamy. 2017.
     Verified low-level programming embedded in F*. Proc. ACM Program. Lang. 1, ICFP, Article 17 (aug 2017), 29 pages.
     https://doi.org/10.1145/3110261
[59] Christopher Pulte, Dhruv C. Makwana, Thomas Sewell, Kayvan Memarian, Peter Sewell, and Neel Krishnaswami.
     2023. CN: Verifying Systems C Code with Separation-Logic Refinement Types. 7, POPL, Article 1 (jan 2023), 32 pages.



Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                        67:33

     https://doi.org/10.1145/3571194
[60] Xiaokang Qiu, Pranav Garg, Andrei Ştefănescu, and Parthasarathy Madhusudan. 2013. Natural proofs for structure,
     data, and separation. In Proceedings of the 34th ACM SIGPLAN Conference on Programming Language Design and
     Implementation (Seattle, Washington, USA) (PLDI ’13). Association for Computing Machinery, New York, NY, USA,
     231–242. https://doi.org/10.1145/2491956.2462169
[61] Willem-Paul de Roever and Kai Engelhardt. 2008. Data Refinement: Model-Oriented Proof Methods and their Comparison
     (1st ed.). Cambridge University Press, USA.
[62] Reuben N. S. Rowe and James Brotherston. 2017. Automatic cyclic termination proofs for recursive procedures in sep-
     aration logic. In Proceedings of the 6th ACM SIGPLAN Conference on Certified Programs and Proofs (Paris, France) (CPP
     2017). Association for Computing Machinery, New York, NY, USA, 53–65. https://doi.org/10.1145/3018610.3018623
[63] Michael Sammler, Angus Hammond, Rodolphe Lepigre, Brian Campbell, Jean Pichon-Pharabod, Derek Dreyer, Deepak
     Garg, and Peter Sewell. 2022. Islaris: verification of machine code against authoritative ISA semantics. In Proceedings
     of the 43rd ACM SIGPLAN International Conference on Programming Language Design and Implementation (San Diego,
     CA, USA) (PLDI 2022). Association for Computing Machinery, New York, NY, USA, 825–840. https://doi.org/10.1145/
     3519939.3523434
[64] Michael Sammler, Rodolphe Lepigre, Robbert Krebbers, Kayvan Memarian, Derek Dreyer, and Deepak Garg. 2021.
     RefinedC: automating the foundational verification of C code with refined ownership types. In Proceedings of the 42nd
     ACM SIGPLAN International Conference on Programming Language Design and Implementation (Virtual, Canada) (PLDI
     2021). Association for Computing Machinery, New York, NY, USA, 158–174. https://doi.org/10.1145/3453483.3454036
[65] Simon Spies, Lennard Gäher, Michael Sammler, and Derek Dreyer. 2024. Quiver: Guided Abductive Inference of
     Separation Logic Specifications in Coq. Proc. ACM Program. Lang. 8, PLDI, Article 183 (jun 2024), 25 pages. https:
     //doi.org/10.1145/3656413
[66] Kasper Svendsen and Lars Birkedal. 2014. Impredicative Concurrent Abstract Predicates. In Programming Languages
     and Systems, Zhong Shao (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 149–168.
[67] Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan Chin. 2016. Automated Mutual Explicit Induction
     Proof in Separation Logic. In FM 2016: Formal Methods, John Fitzgerald, Constance Heitmeyer, Stefania Gnesi, and
     Anna Philippou (Eds.). Springer International Publishing, Cham, 659–676.
[68] Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan Chin. 2017. Automated lemma synthesis in
     symbolic-heap separation logic. Proc. ACM Program. Lang. 2, POPL, Article 9 (dec 2017), 29 pages. https://doi.org/10.
     1145/3158097
[69] The Verifast Team. 2021.          Verification of Matrix Multiplication.      https://github.com/verifast/verifast/blob/
     c84c07bdfe777ce11a5c006975e35276ddee8bc0/examples/verifythis2016/matmul.java published in Verifast project.
[70] The Verifast Team. 2021.                 Verification of Quicksort.           https://github.com/verifast/verifast/blob/
     52db325f08149d1d1c4bfa13e204a4d3c903ee26/examples/quicksort.c published in Verifast project.
[71] Frédéric Vogels, Bart Jacobs, Frank Piessens, and Jan Smans. 2011. Annotation Inference for Separation Logic Based
     Verifiers. In Formal Techniques for Distributed Systems, Roberto Bruni and Juergen Dingel (Eds.). Springer Berlin Hei-
     delberg, Berlin, Heidelberg, 319–333.
[72] Qiyuan Xu. 2024. Phi-System. https://github.com/xqyww123/phi-system
[73] Qiyuan Xu. 2024. The Artifact of “Generically Automating Separation Logic by Functors, Homomorphisms, and Modules”’.
     https://doi.org/10.5281/zenodo.14207756
[74] Vadim Zaliva, Kayvan Memarian, Ricardo Almeida, Jessica Clarke, Brooks Davis, Alexander Richardson, David Chis-
     nall, Brian Campbell, Ian Stark, Robert N. M. Watson, and Peter Sewell. 2024. Formal Mechanised Semantics of
     CHERI C: Capabilities, Undefined Behaviour, and Provenance. In Proceedings of the 29th ACM International Confer-
     ence on Architectural Support for Programming Languages and Operating Systems, Volume 1 (ASPLOS ’24). Association
     for Computing Machinery, New York, NY, USA, 181–196. https://doi.org/10.1145/3617232.3624859
[75] Litao Zhou, Jianxing Qin, Qinshi Wang, Andrew W. Appel, and Qinxiang Cao. 2024. VST-A: A Foundationally Sound
     Annotation Verifier. Proc. ACM Program. Lang. 8, POPL, Article 69 (jan 2024), 30 pages. https://doi.org/10.1145/
     3632911




                                 Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:34                                    Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu

A Complete Formalization of the Assertion Language of our Separation Logic
Section §4 has presented a simplified formalization that captures the novelty of how our separation
logic integrates data refinements. In order to be self-contained, the complete formalization of the
assertion language is presented in this appendix for interested readers to refer to.
   The assertion language of the SL is parameterized by a finite set P of SL predicates, and a first-
order logic FOL with equality. Let 𝑤, 𝑥, 𝑦, 𝑧, 𝑡 range over terms in FOL, and 𝛼, 𝛽 over variables in
FOL. Fix a set P of symbols to denote SL predicates, and let 𝑇 , 𝑈 range over them. The assertion
language F of our SL includes all standard connectives plus a satisfaction operator () borrowed
from Hybrid Logic [5, 30] (originally denoted by @).
F ∋ 𝜙,𝜓 F ⊤ | ⊥ | emp | 𝑇 (𝑥) | ¬𝜙 | 𝜙 ∗ 𝜓 | 𝜙 ∧ 𝜓 | 𝜙 ∨ 𝜓 | 𝜙 −∗ 𝜓 | 𝜙 → 𝜓 | ∃𝛼 . 𝜙 | ∀𝛼 . 𝜙 | 𝑡  𝜙
         | any other formula in FOL, e.g., 𝑥 = 𝑦.
   Fix a domain of discourse O and an interpretation function [[−]] from FOL terms to O. Fix a
partial commutative monoid A = (𝑆, •, 𝜖) which we call Separation Algebra. Elements in 𝑆 are
called worlds and ranged over by 𝑤.
   Additionally, fix an interpretation function [[−]] ′ : P → 2 O×𝑆 that assigns every SL predicate
(symbol) a subset of the product of the domain of discourse and the set of worlds.
   The semantics of formulas in F is defined by forcing relation (|=), a binary relation between 𝑆
and F. For 𝑤 ∈ 𝑆, and 𝜙,𝜓 ∈ F,
    𝑤 |= ⊤ holds anytime;
    𝑤 |= ⊥ never holds;
    𝑤 |= emp holds iff 𝑤 is the identity element 𝜖;
    𝑤 |= 𝑇 (𝑥) holds iff (𝑥, 𝑤) ∈ [[𝑇 ]] ′ ;
    𝑤 |= ¬𝜙 holds iff 𝑤 |= 𝜙 does not hold;
    𝑤 |= 𝜙 ∗ 𝜓 holds iff there exists 𝑤 1, 𝑤 2 such that 𝑤 = 𝑤 1 • 𝑤 2 and both 𝑤 1 |= 𝜙, 𝑤 2 |= 𝜓 hold;
    𝑤 |= 𝜙 ∧ 𝜓 iff both 𝑤 |= 𝜙 and 𝑤 |= 𝜓 hold;
    𝑤 |= 𝜙 ∨ 𝜓 iff either 𝑤 |= 𝜙 or 𝑤 |= 𝜓 holds;
    𝑤 |= 𝜙 −∗𝜓 holds iff for any 𝑤 ′ such that 𝑤 ′ |= 𝜙 holds and 𝑤 ′ • 𝑤 is defined, 𝑤 ′ • 𝑤 |= 𝜓 holds;
    𝑤 |= 𝜙 → 𝜓 holds iff, given that 𝑤 |= 𝜙 holds, 𝑤 |= 𝜓 holds;
    𝑤 |= (∃𝛼 . 𝜙) holds iff there is an FOL term 𝑡 such that 𝑤 |= 𝜙 [𝑡/𝛼] holds;
    𝑤 |= (∀𝛼 . 𝜙) holds iff 𝑤 |= 𝜙 [𝑡/𝛼] holds for any FOL term 𝑡;
    𝑤 |= (𝑡  𝜙) holds iff [[𝑡]] |= 𝜙 holds;
    if 𝜙 is an FOL formula, 𝑤 |= 𝜙 holds iff 𝜙 holds according to the semantics of FOL.
Notation 𝜙 [𝑡/𝛼] denotes the formula obtained by substituting term 𝑡 for any occurrences of 𝛼.

B A Many-Sorted Variant of the Assertion Language
As mentioned in §4, we require the worlds of SL assertions to encompass all concrete representa-
tions like program states, memory and values, and also all abstract objects that are used as inter-
mediate representations of stepwise refinements, e.g., the 𝑥 in 𝑦 ⦂ (𝑇 ; 𝑈 ) ≜ ∃𝑥 . 𝑥 ⦂𝑇 ∧ (𝑥 |= 𝑦 ⦂𝑈 ).
   Generally, we want different kinds of objects to be organized in different PCMs, which eases
how to define their group operations. The many-sorted variant presented in this section realizes a
way for this purpose.
   Fix a set K to denote (the symbols of) all sorts. Every world 𝑤 is classified into a unique sort,
written k(𝑤). Syntactically, every formula is represented as a tuple of its unsorted expression
(an element in F) and its sort. Overload k(𝜙) to also denote the sort of formula 𝜙. Every predicate
symbol 𝑃 is also assigned with a unique sort, also denoted as k(𝑃). A formula is well-formed formula
(written wff ) iff the sorts of all subformulas are compatible. Formally,

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                               67:35


                𝜙 is wff      𝜓 is wff       k(𝜙) = k(𝜓 ) = k(𝜙 ★ 𝜓 )
                                                                      for ★ = ∗, ∧, ∨, −∗, →
                                   (𝜙 ★ 𝜓 ) is wff
    𝜙 is wff         k(𝜙) = k(Q𝛼 . 𝜙)                         𝜙 is wff        k(𝜙) = k([[𝑡]]) = k(𝑡  𝜙)
                                      for ★ = ∃, ∀
               (Q𝛼 . 𝜙) is wff                                                (𝑡  𝜙) is wff

       𝜙 is wff        k(𝜙) = k(¬𝜙)                  k(𝑃 (𝑥)) = k(𝑃)                  ⊤ is wff , ⊥ is wff
                  (¬𝜙) is wff                          𝑃 (𝑥) is wff                        emp is wff

Note that a formula is a tuple of its unsorted expression and its sort. The above rules rule out any
such tuples of illegal sorts, ensuring any well-formed formula is a tuple that has a correct sort.
   We only consider well-formed formulas henceforth. Thus, we call a well-formed formula simply
a formula.
   The semantics of this many-sorted SL is also many-sorted. Instead of a single huge PCM, the
semantics depends on a family of PCMs {A𝑘 }𝑘 ∈ K indexed by sorts. The semantics is given by the
forcing relation (|=) between sorted well-formed formulas and the PCMs. Let expr(𝜙) denote the
unsorted expression of 𝜙. Note expr(𝜙) ∈ F. Let (|=′A ) denote the old forcing relation defined in
Appendix A, which uses PCM A as its model. The forcing relation (|=) in our many-sorted variant
is defined based on what we have defined in Appendix A,
                                                                  ′
                      𝑤 |= 𝜙 iff 𝜙 is wff and k(𝑤) = k(𝜙) and 𝑤 |=k(𝑤 ) expr(𝜙).

   The reasoning system can also be migrated accordingly to a many-sorted variant. Our Isabelle
implementation is indeed a many-sorted version. We omit the further discussion about the many-
sorted reasoning system and refer readers to our source.
   As a benefit of this many-sorted SL, the implementation can enjoy shallow embedding and
implements PCMs using typeclasses constraints given by the underlying proof assistants. In our
Isabelle implementation, a PCM is given by an Isabelle/HOL type that satisfies a specific typeclass
C. The set of all values of this type is the carrier set; Typeclass C constrains the presence of the
group operation and its PCM axioms.
 An Isabelle/HOL type 𝛼 satisfies typeclass C iff
       there is a set 𝐷 : (𝛼 × 𝛼) set, which defines the domain of the group operation,
       there is a binary operator (·) : 𝛼 → 𝛼 → 𝛼 that defines the result of the group operation,
       there is a distinguished constant 𝜀 : 𝛼 representing the identity element,
       ∀𝑥 . 𝑥 · 𝜀 = 𝑥 = 𝜀 · 𝑥 ∧ (𝑥, 𝜀) ∈ 𝐷 ∧ (𝜀, 𝑥) ∈ 𝐷
       ∀(𝑥, 𝑦) ∈ 𝐷. 𝑥 · 𝑦 = 𝑦 · 𝑥 ∧ (𝑦, 𝑥) ∈ 𝐷
       ∀(𝑥, 𝑦) ∈ 𝐷, (𝑥 · 𝑦, 𝑧) ∈ 𝐷. (𝑦, 𝑧) ∈ 𝐷 ∧ (𝑥, 𝑦 · 𝑧) ∈ 𝐷 ∧ (𝑥 · 𝑦) · 𝑧 = 𝑥 · (𝑦 · 𝑧)
In this implementation, SL formulas are represented by a family of Isabelle/HOL types {𝛼 set}𝛼:C
indexed by any type 𝛼 satisfying typeclass C. Forcing relation (|=) is implemented by the set
membership (∈). Connectives are implemented by polymorphic types, e.g.,
(∗) : ∀𝛼 : C. 𝛼 set → 𝛼 set → 𝛼 set                                          where 𝐷, (·) are obtained from
(𝜙 ∗ 𝜓 ) ≜ {𝑤 | ∃(𝑤 1, 𝑤 2 ) ∈ 𝐷. 𝑤 = 𝑤 1 · 𝑤 2 ∧ 𝑤 1 ∈ 𝜙 ∧ 𝑤 2 ∈ 𝜓 }        the typeclass instance of 𝛼 : C

The reasoning is also parameterized by a type variable 𝛼 : C that can range over any instance
type of typeclass C. In this way, the many-sorted logic, and the huge SL model that encompasses
any concrete representations and many abstract objects, do not impose much of a burden on both
users and reasoner developers.

                             Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:36                                             Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu

C       Examples of Ad-hoc Transformation Rules
As mentioned in § 6.3, our system involves ad-hoc transformation rules for eliminating predicate
counterparts of logic connectives. The rules for eliminating (𝑥, 𝑦) ⦂ (𝑇 ∗𝑈 ) are illustrated as follows.
             bi-TP(𝑇1, 𝑈 , 𝐷 1 ) ← (𝜃 1, 𝑓1, 𝑍 ′, 𝑅1 )           bi-TP(𝑇2, 𝑍 ′, 𝐷 2 ) ← (𝜃 2, 𝑓2, 𝑍, 𝑅2 )
                                                                                                               (TP∗L )
             bi-TP((𝑇1 ∗ 𝑇2 ), 𝑈 , 𝐷) ← (𝜃 1 ∧ 𝜃 2, 𝑓 , 𝑍, 𝑅1 ∗ 𝑅2 )
             where 𝑓 = 𝜆((𝑥 1, 𝑥 2 ), 𝑤). let (𝑤 ′, 𝑟 2 ) = 𝑓2 (𝑥 2, 𝑤); (𝑦, 𝑟 1 ) = 𝑓1 (𝑥 1, 𝑤 ′ ) in (𝑦, (𝑟 1, 𝑟 2 ))
                   𝐷 1 = {(𝑥 1, 𝜋 1 (𝑓2 (𝑥 2, 𝑧))) | ((𝑥 1, 𝑥 2 ), 𝑧) ∈ 𝐷 }
                   𝐷 2 = {(𝑥 2, 𝑤) | ((𝑥 1, 𝑥 2 ), 𝑤) ∈ 𝐷 }
The rule reduces bi-TP((𝑇1 ∗ 𝑇2 ), 𝑈 , 𝐷) to two problems, bi-TP(𝑇1, 𝑈 , 𝐷 1 ) and bi-TP(𝑇2, 𝑍 ′, 𝐷 2 ). To
answer bi-TP((𝑇1 ∗𝑇2 ), 𝑈 , 𝐷), our reasoner first introduces a fresh free variable 𝑓2 , which occurs in
𝐷 1 . Then, the reasoner tries to solve the sub-problem bi-TP(𝑇1, 𝑈 , 𝐷 1 ). Assume the reasoner obtains
a solution (𝜃 1, 𝑓1, 𝑍 ′, 𝑅1 ), which means the transformation from 𝑇1 to 𝑈 demands 𝑍 ′ and remains 𝑅1 .
Note that variable 𝑓2 can occur in the solution. Next, the reasoner turns to solve bi-TP(𝑇2, 𝑍 ′, 𝐷 2 ),
to extract the demanded 𝑍 ′ from the unused second source 𝑇2 . If it obtains a solution (𝜃 2, 𝑓2, 𝑍, 𝑅2 ),
then initial TP problem bi-TP((𝑇1 ∗𝑇2 ), 𝑈 , 𝐷) has a solution (𝜃 1 ∧𝜃 2, 𝑓 , 𝑍, 𝑅1 ∗𝑅2 ). Given an assertion
((𝑥 1, 𝑥 2 ), 𝑤) ⦂ (𝑇1 ∗𝑇2 ) ∗𝑍 , this solution first transforms (𝑥 2, 𝑤) ⦂ (𝑇2 ∗𝑍 ) to (𝑤 ′, 𝑟 2 ) ⦂ (𝑍 ′ ∗𝑅2 ) using
the solution of the second sub-problem. Then, it transforms (𝑥 1, 𝑤 ′ ) ⦂ (𝑇1 ∗ 𝑍 ′ ) to (𝑦, 𝑟 1 ) ⦂ (𝑈 ∗ 𝑍 ′ ).
Consequently, (𝑦, (𝑟 1, 𝑟 2 )) ⦂ 𝑈 ∗ (𝑅1 ∗ 𝑅2 ) is the final end of the transformation indicated by the
solution (𝜃 1 ∧ 𝜃 2, 𝑓 , 𝑍, 𝑅1 ∗ 𝑅2 ).
   The other rule for bi-TP(𝑇 , (𝑈 1 ∗ 𝑈 2 ), 𝐷) is essentially symmetric to the reduction above. There-
fore, we present it as follows without more explanation.
              bi-TP(𝑇 , 𝑈 1, 𝐷 1 ) ← (𝜃 1, 𝑓1, 𝑍 1, 𝑅 ′ )    bi-TP(𝑅 ′, 𝑈 2, 𝐷 2 ) ← (𝜃 2, 𝑓2, 𝑍 2, 𝑅)
                                                                                                             (TP∗R )
             bi-TP(𝑇 , (𝑈 1 ∗ 𝑈 2 ), 𝐷) ← (𝜃 1 ∧ 𝜃 2, 𝑓 , 𝑍, 𝑅)
             where 𝑓 = 𝜆(𝑥, (𝑤 1, 𝑤 2 )). let (𝑦1, 𝑟 ′ ) = 𝑓1 (𝑥, 𝑤 1 ); (𝑦2, 𝑟 ) = 𝑓2 (𝑟 ′, 𝑤 2 ) in ((𝑦1, 𝑦2 ), 𝑟 )
                   𝐷 1 = {(𝑥, 𝑤 1 ) | ∃𝑤 2 . (𝑥, (𝑤 1, 𝑤 2 )) ∈ 𝐷 }
                   𝐷 2 = {(𝑟 ′, 𝑤 2 ) | ∃𝑥 𝑤 1 𝑦1 . (𝑥, (𝑤 1, 𝑤 2 )) ∈ 𝐷 ∧ (𝑦1, 𝑟 ′ ) = 𝑓1 (𝑥, 𝑤 1 )}
    Additionally, we present the ad-hoc rules for eliminating 𝑥 ⦂ Emp ≜ emp ∧ 𝑥 = ().
                                            Axiom                              (TP-EmpL )
                    bi-TP(Emp, 𝑈 , 𝐷) ← (𝐷 = {()}, 𝜆((), 𝑤). (𝑤, ()), 𝑈 , Emp)
                                              Axiom                            (TP-EmpR )
                        bi-TP(𝑇 , Emp, 𝐷) ← (true, 𝜆(𝑥, ()). ((), 𝑥), Emp, 𝑈 )
D The Detailed Reduction Process of §6.6
Properties hold by Slice:
         Functor(Slice [𝑖,𝑗 ) , map, set)            SepHom(Slice [𝑖,𝑗 ) , unzip, zip)             Dist(Slice, split, cat)
        where map(𝑓 )( [𝑙 1, · · ·, 𝑙𝑛 ]) ≜ [𝑓 (𝑙 1 ), · · ·, 𝑓 (𝑙𝑛 )]
                 set([𝑙 1, · · ·, 𝑙𝑛 ]) ≜ {𝑙 1, · · ·, 𝑙𝑛 }
                 zip([𝑎 1, · · ·, 𝑎𝑛 ], [𝑏 1, · · ·, 𝑏𝑛 ]) ≜ [(𝑎 1, 𝑏 1 ), · · ·, (𝑎𝑛 , 𝑏𝑛 )]
                 unzip[(𝑎 1, 𝑏 1 ), · · ·, (𝑎𝑛 , 𝑏𝑛 )] ≜ ( [𝑎 1, · · ·, 𝑎𝑛 ], [𝑏 1, · · ·, 𝑏𝑛 ])
                 cat [𝑖,𝑗 ),[ 𝑗 ′ ,𝑘 ) (𝑙 1, 𝑙 2 ) ≜ if 𝑗 = 𝑗 ′ then the concatenation of 𝑙 1, 𝑙 2 else undefined.
                 split [𝑖,𝑗 ),[ 𝑗 ′ ,𝑘 ) (𝑙) ≜ if 𝑗 = 𝑗 ′ then ([𝑙 0, · · ·, 𝑙 𝑗 −𝑖 −1 ], [𝑙 𝑗 −𝑖 , · · ·, 𝑙𝑘 −𝑖 −1 ]) else undefined.
Given the above properties, SH and SDR instantiate the following reasoning rules respectively.

Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                             67:37


                              bi-TP(𝑇 , 𝑈 , 𝐷 >>= (𝑑 ◦ 𝑧)) ← (𝜃, 𝑓 , 𝑍, 𝑅)
                                                                                                         (Slice-SH)
          bi-TP(Slice [𝑖,𝑗 ) (𝑇 ), Slice [𝑖,𝑗 ) (𝑈 ), 𝐷) ← (𝜃, 𝑓 ′, Slice [𝑖,𝑗 ) (𝑍 ), Slice [𝑖,𝑗 ) (𝑅))
          where 𝑓 ′ = unzip ◦ map(𝑓 ) ◦ zip

                bi-TP(Slice [𝑖,𝑘 ) (𝑇 ), 𝐹 [𝑖,𝑘 ) ] (𝑈 ), ℎ(𝐷)) ← (𝜃, 𝑓 , 𝑍, 𝑅)
                                                                                           (Slice-SDR ) if 𝑘 < 𝑗
             bi-TP(𝐹 [𝑖,𝑗 ) (𝑇 ), 𝐹 [𝑖,𝑘 ) (𝑈 ), 𝐷) ← (𝜃, 𝑔, 𝑍, 𝐹 [𝑘,𝑗 ) (𝑇 ) ∗ 𝑅)
             where ℎ = 𝜆(𝑥𝑛 , 𝑤). let (𝑥𝑚 , 𝑥𝛿 ) = split [𝑖,𝑘 ),[𝑘,𝑗 ) (𝑥𝑛 )
                   𝑔 = 𝜆(𝑥𝑛 , 𝑤). let (𝑥𝑚 , 𝑥𝛿 ) = split [𝑖,𝑘 ),[𝑘,𝑗 ) (𝑥𝑛 ); (𝑦, 𝑟 ) = 𝑓 (𝑥𝑚 , 𝑤) in (𝑦, (𝑥𝛿 , 𝑟 )) in (𝑥𝑚 , 𝑤)
Using the above instantiated rules, the bi-TP reduction in §6.6 is detailed as follows.
         bi-TP( Slice [0,𝑁 ) Z , Slice [0,𝑁 ) Z ) ← (true, 𝜆𝑥 . 𝑥, Emp, Emp)
                                                                                                (Slice-SDR )
   bi-TP(3) ← (true, 𝜆(𝑦, 𝑟 ). (𝑦 [0:𝑁 ] , (𝑦 [𝑁 :2𝑁 ] , 𝑟 )), Emp, Slice [𝑁 ,2𝑁 ) Z ∗ Emp)
                                                                                                by simplification
        bi-TP(3) ← (true, 𝜆(𝑦, _). (𝑦 [0:𝑁 ] , 𝑦 [𝑁 :2𝑁 ] ), Emp, Slice [𝑁 ,2𝑁 ) Z)
                                                                                          (Slice-SH)
             bi-TP(2) ← (true,
                  unzip ◦ map(𝜆(𝑦, _). (𝑦 [0:𝑁 ] , 𝑦 [𝑁 :2𝑁 ] )) ◦ zip,
                  Slice [0,𝑁 ) Emp,
                  Slice [0,𝑁 ) (Slice [𝑁 ,2𝑁 ) Z))
                                                                                     by simplification
                    bi-TP(2) ← (true,
                           unzip ◦ map(𝜆𝑦. (𝑦 [0:𝑁 ] , 𝑦 [𝑁 :2𝑁 ] )) ◦ 𝜋1,
                           Emp,
                           Slice [0,𝑁 ) (Slice [𝑁 ,2𝑁 ) Z) )
                                                                              Let cut𝑁 (𝑦) ≜ (𝑦 [0:𝑁 ] , 𝑦 [𝑁 :2𝑁 ] )
                    bi-TP(2) ← (true,
                           unzip ◦ map(cut𝑁 ) ◦ 𝜋1,
                           Emp,
                           Slice [0,𝑁 ) (Slice [𝑁 ,2𝑁 ) Z) )
                                                                                      (Slice-SDR )
            bi-TP(1) ← (true,
                 𝜆(𝑦, _). let (𝑦𝐴𝐵 , 𝑦𝐶𝐷 ) = cut𝑁 (𝑦);
                                (𝑦𝐴 , 𝑦𝐵 ) = unzip(map(cut𝑁 )(𝑦𝐴𝐵 ))
                            in (𝑦𝐴 , (𝑦𝐶𝐷 , 𝑦𝐵 )),
                 Emp,
                 Slice [𝑁 ,2𝑁 ) (Slice [0,𝑁 ) Z) ∗ Slice [0,𝑁 ) (Slice [𝑁 ,2𝑁 ) Z)
            )
E Proofs to some Lemmas
    Lemma E.1. Rule SH is sound.
   PRoof. Assume (𝜃, 𝑓 , 𝑍, 𝑅) is a solution of bi-TP(𝐹 (𝑇 ), 𝐹 (𝑈 ), 𝐷). Also assume 𝜃 holds. Starting
with 𝑥 ⦂ 𝐹 (𝑇 ) ∗ 𝐹 (𝑍 ), we can first transform it to 𝑧 (𝑥) ⦂ 𝐹 (𝑇 ∗ 𝑍 ) by property SepHom(𝐹, 𝑠, 𝑧),
then to (𝑚(𝑓 ) ◦ 𝑧) (𝑥) ⦂ 𝐹 (𝑈 ∗ 𝑅) by our assumption and property Functor(𝐹, 𝑚, 𝑑), and finally to
(𝑠 ◦ 𝑚(𝑓 ) ◦ 𝑧)(𝑥) ⦂ 𝐹 (𝑈 ) ∗ 𝐹 (𝑅) by property SepHom(𝐹, 𝑠, 𝑧) again.                                □

F    A Systematic Overview for the Templates
Each template defines a reduction aimed at eliminating a predicate operator. The reasoning system
composed of rules instantiated from the templates can be understood as recursively performing the
following reductions: Given a problem P that can be either a TP(𝑇 ′, 𝑈 ′, 𝐷) or a bi-TP(𝑇 ′, 𝑈 ′, 𝐷),
  1: For any predicate operator 𝐹 having a known property SZero(𝐹, 𝐷 ′ ), if 𝑇 ′ matches pattern
     𝐹𝑎 (𝑇 ) and (𝑎 is a zero element) is provable, apply reduction S0L ; else, if 𝑈 ′ matches pattern
     𝐹𝑎 (𝑇 ) and (𝑎 is a zero element) is provable, apply reduction S0R .

                                 Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
67:38                                    Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu


 2: Else, if (𝑇 ′, 𝑈 ′ ) matches pattern (𝐹 (𝑇 ), 𝐹 (𝑈 )) for some 𝐹 satisfying Functor(𝐹, m, 𝑑),
 3:       if P is a TP, apply reduction TF;
 4:       else, P must be a bi-TP. Then, check if 𝐹 has a known property SepHom(𝐹, 𝑠, 𝑧). If so,
             apply reduction SH; else, go to step 5.
 5: Else, if (𝑇 ′, 𝑈 ′ ) matches pattern (𝐹𝑛 (𝑇 ), 𝐹𝑚 (𝑈 )) for some known predicate operator 𝐹 , then,
 6:       if (𝑛 = 𝑚) is provable and 𝐹𝑚 is a Functor, rewrite P with 𝑛 = 𝑚, and go to step 2;
 7:       else, if 𝐹 has a known property Dist(𝐹, 𝑠, 𝑧), then,
 8:             if 𝑛 + 𝛿 = 𝑚 is provable for some 𝛿, apply reduction SDL ;
 9:             else if 𝑛 = 𝑚 + 𝛿 is provable for some 𝛿, apply reduction SDR ;
10:      else, if 𝐹 has a known property Assoc(𝐹, 𝑔, ℎ), then,
11:             if 𝑛 · 𝛿 = 𝑚 is provable for some 𝛿, apply reduction SAR ;
12:             else, if 𝑛 = 𝑚 · 𝛿 is provable for some 𝛿, apply reduction SAL .
13: Else, if 𝑈 ′ matches pattern 𝐹𝑚 (𝑈 ) for some 𝐹 having a known property SUnit(𝐹, 𝑔, ℎ), and if
     𝑇 ′ does not match 𝐹𝑛 (𝑇 ) for any 𝑛,𝑇 , then apply reduction S1I .
 14: Else, if 𝑇 ′ matches pattern 𝐹𝑛 (𝑇 ) for some 𝐹 satisfying SUnit(𝐹, 𝑔, ℎ), and (𝑛 is an identity) is
      provable, and 𝑈 ′ does not match 𝐹𝑚 (𝑈 ) for any 𝑚,𝑇 , then apply reduction S1E .
As the reasoning involves arithmetic equations of the ring-like scalar algebra(s), our reasoner has
to be parameterized by an automated solver for arithmetics on the algebra(s). In the formalization
above, when we state that a formula 𝑃 is provable, we mean that the formula can be proven by
this solver within a time limit.
   The reductions for scalar distributivity are incomplete if the scalar addition is not commutative,
associative, and cancellative. For bi-TP(𝐹𝑛 (𝑇 ), 𝐹𝑚 (𝑈 ), 𝐷), SDL and SDR only consider the cases
when 𝑛 = 𝑚 + 𝛿 and 𝑛 + 𝛿 = 𝑚 for some 𝛿. However, if the addition is non-commutative (while
still assuming associativity and cancellativity), more templates are required to cover the cases of
(𝛿 ′ + 𝑛 + 𝛿 = 𝑚), (𝑛 + 𝛿 = 𝛿 ′ +𝑚), (𝛿 + 𝑛 = 𝑚 + 𝛿 ′ ), and (𝑛 = 𝛿 +𝑚 + 𝛿 ′ ), for some 𝛿, 𝛿 ′ . For example,
continue the Slice example but consider bi-TP(Slice [𝑖,𝑗 ) , Slice [𝑖 ′ ,𝑘 ) , 𝐷) with 𝑗 < 𝑘 and 𝑖 < 𝑖 ′ . The
bi-TP is irreducible by either SDL or SDR , but a template for 𝑛 + 𝛿 = 𝛿 ′ + 𝑚 where we instantiate
𝑛, 𝛿, 𝛿 ′, 𝑚 to [𝑖, 𝑗), [ 𝑗, 𝑘), [𝑖, 𝑖 ′ ), [𝑖 ′, 𝑘).
   Assuming Dist(𝐹, 𝑠, 𝑧), the templates for the four cases are presented as follows, where we in-
stead use 𝑎, 𝑏, 𝑐, 𝑑, 𝛾 to ranger over scalars.
           bi-TP(𝐹𝑑+𝑎 (𝑇 ), 𝐹𝑏+𝑐 (𝑈 ), ℎ(𝐷)) ← (𝜃, 𝑓 ,𝑊 , 𝑅)                   if 𝑎 ≠ 𝑏 and there are
                                                                               non-zero scalars 𝛾, 𝑐, 𝑑
    bi-TP(𝐹𝑎 (𝑇 ), 𝐹𝑏 (𝑈 ), 𝐷) ← (𝜃, 𝑔◦ 𝑓 ◦ℎ, 𝐹𝑑 (𝑇 )∗𝑊 , 𝐹𝑐 (𝑈 )∗𝑅)
                                                                               such that
    where ℎ = (𝜆(𝑥𝑎 , (𝑥𝑑 , 𝑤)). (𝑧𝑑,𝑎 (𝑥𝑑 , 𝑥𝑎 ), 𝑤))
                                                                               𝑎 = 𝛾 +𝑐 ∧𝑏 = 𝑑 +𝛾
    where 𝑔 = (𝜆(𝑦, 𝑟 ). let (𝑦𝑏 , 𝑦𝑐 ) = 𝑠𝑏,𝑐 (𝑦) in (𝑦𝑏 , (𝑦𝑐 , 𝑟 )))

           bi-TP(𝐹𝑎+𝑑 (𝑇 ), 𝐹𝑐+𝑏 (𝑈 ), ℎ(𝐷)) ← (𝜃, 𝑓 ,𝑊 , 𝑅)                   if 𝑎 ≠ 𝑏 and there are
                                                                               non-zero scalars 𝛾, 𝑐, 𝑑
    bi-TP(𝐹𝑎 (𝑇 ), 𝐹𝑏 (𝑈 ), 𝐷) ← (𝜃, 𝑔◦ 𝑓 ◦ℎ, 𝐹𝑑 (𝑇 ) ∗𝑊 , 𝐹𝑐 (𝑈 ) ∗ 𝑅)
                                                                               such that
    where ℎ = (𝜆(𝑥𝑎 , (𝑥𝑑 , 𝑤)). (𝑧𝑎,𝑑 (𝑥𝑎 , 𝑥𝑑 ), 𝑤))
                                                                               𝑎 = 𝑐 +𝛾 ∧𝑏 = 𝛾 +𝑑
    where 𝑔 = (𝜆(𝑦, 𝑟 ). let (𝑦𝑐 , 𝑦𝑏 ) = 𝑠𝑐,𝑏 (𝑦) in (𝑦𝑏 , (𝑦𝑐 , 𝑟 )))

                 bi-TP(𝐹𝑎+𝑑 (𝑇 ), 𝐹𝑐+𝑏 (𝑈 ), 𝐷) ← (𝜃, 𝑓 ,𝑊 , 𝑅)                if 𝑎 ≠ 𝑏 and there are
        bi-TP(𝐹𝑎 (𝑇 ), 𝐹𝑏 (𝑈 ), 𝐷) ← (𝜃, 𝑔◦ 𝑓 , 𝑊 , 𝐹𝑑 (𝑈 )∗𝐹𝑐 (𝑈 )∗𝑅)         non-zero scalars 𝑐, 𝑑
        where 𝑔 = (𝜆(𝑦, 𝑟 ). let (𝑦𝑑 , 𝑦𝑏𝑐 ) = 𝑠𝑑,𝑏+𝑐 (𝑦)                      such that 𝑎 = 𝑑 + 𝑏 + 𝑐
                                   (𝑦𝑏 , 𝑦𝑐 ) = 𝑠𝑏,𝑐 (𝑦)
                                in (𝑦𝑏 , (𝑦𝑑 , 𝑦𝑐 , 𝑟 )))


Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                                   67:39


             bi-TP(𝐹𝑑+𝑎+𝑐 (𝑇 ), 𝐹𝑏 (𝑈 ), ℎ(𝐷)) ← (𝜃, 𝑓 ,𝑊 , 𝑅)                    if 𝑎 ≠ 𝑏 and there are
      bi-TP(𝐹𝑎 (𝑇 ), 𝐹𝑏 (𝑈 ), 𝐷) ← (𝜃, 𝑓 ◦ℎ, 𝐹𝑑 (𝑇 )∗𝐹𝑐 (𝑇 )∗𝑊 , 𝑅)               non-zero scalars 𝑐, 𝑑
      where ℎ = (𝜆(𝑥𝑎 , (𝑥𝑑 , 𝑥𝑐 , 𝑤)). (𝑧𝑑,𝑎+𝑐 (𝑥𝑑 , 𝑧𝑎,𝑐 (𝑥𝑎 , 𝑥𝑐 )), 𝑤))       such that 𝑑 + 𝑎 + 𝑐 = 𝑏
G Overloading & Resolution
Overloading and resolution are essential for state-of-the-art tools like RefinedC to handle low-level
programming idioms. In this section, we present an extension of our inference system (primarily
the wp-transformer and the reduction to bi-EPs) to support overloading and resolution.

G.1     Introducing Overloading to wp-Transformer
During the backward reasoning process of the wp-tranformer (Routine 2), consider a goal
wp𝐶 (𝑢 ) {𝑣. 𝜓 (𝑣)} ⊣ ? that infers a pre-condition of program computation 𝐶 (𝑢). If there are 𝑁 rules
associated with the program 𝐶, each of which instructs the reasoning process to return a pre-
condition 𝜙𝑖 , the wp-tranformer returns their disjunction,
                                        wp𝐶 (𝑢 ) {𝑣. 𝜓 (𝑣)} ⊣ 𝜙 1 ∨ · · · ∨ 𝜙 𝑁

G.2     Resolving Overloadings
While state-of-the-art tools typically use pattern matching for overloading resolution, we empha-
size the importance of refinement transformations (known as subtypings in refinement-type sys-
tems). Therefore, we adopt a semantic proof search strategy based on refinement transformations.
   As the extended wp-transformer returns a formula involving disjunction ∨, we first extend the
syntax of goal formulas G to involve disjunction.
                 Goal G F S | S ∗ G | S −∗ G | 𝑃 → G | G ∧ G | ∀𝛼 . G | ∃𝛼 . G | G ∨ G
To eliminate the disjunction connective, we introduce two rules,
                     𝜃 | 𝑆 ⊢ 𝐺1                                       𝜃 | 𝑆 ⊢ 𝐺2
                                   (G∨L )                                            (G∨L )
                 𝜃 | 𝑆 ⊢ 𝐺1 ∨ 𝐺2                                   𝜃 | 𝑆 ⊢ 𝐺1 ∨ 𝐺2
The two rules create a branching point in our reasoning process. When deriving the proof goal
𝜃 | 𝑆 ⊢ 𝐺 1 ∨ 𝐺 2 , our reasoner first attempts the branch applying rule (G∨L ). The reasoning process
continues along this branch, eventually producing a set of bi-EPs and subgoals for eliminating the
remains and demands of the bi-EPs. If the subsequent reasoning process successfully solves the
bi-EPs and the subgoals, this means that the refinement of state 𝑆 can transform to 𝐺 1 . Therefore
𝐺 1 is a valid resolution of the overloading. The reasoning process then proceeds along this branch,
discarding the alternative branch for operand 𝐺 2 . Otherwise, if the bi-EPs and subgoals fail to
be solved, 𝐺 2 is then considered as an invalid resolution. The reasoning process backtracks and
applies rule (G∨L ) instead.




                                 Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.




                                                                                                                                                                                                                                                                   67:40
                                                                                                                  Axiom                                                                                                         Define swap(𝑥, 𝑦) ≜ (𝑦, 𝑥).
                                                                                                                                               (FB2 )
                                                                                              bi-TP(𝑇 , 𝑈 , {(𝑥, 𝑧 1 )}) ← (⊤, swap, 𝑈 ,𝑇 )
                                                                                              𝑧 1 is a fresh free variable that represents            Trans(𝑈 , (=))
                                                                                              the unknown antiframe.
                                                                                                                                                                      (biTP)
                                                                                                  bi-EP(𝑥 ⦂ 𝑇 , 𝑦 ⦂ 𝑈 ) ← ((𝑧 1 = 𝑦), 𝑧 1 ⦂ 𝑈 , 𝑥 ⦂ 𝑇 )                                                  Axiom
                                                                                                                                                                                                                                    (ID)
                                                                                                  proof obligation (𝑧 1 = 𝑦) implies the unknown 𝑧 1 is 𝑦.                       bi-TP(𝑈 , 𝑈 , {(𝑦, 𝑧 2 )}) ← (⊤, 𝜆𝑥 .𝑥, Emp, Emp)        Trans(𝑈 , (=))
                                                                                                                                                                 (simplify)                                                                               (biTP)
                                                                                                            bi-EP(𝑥 ⦂ 𝑇 , 𝑦 ⦂ 𝑈 ) ← (⊤, 𝑦 ⦂ 𝑈 , 𝑥 ⦂ 𝑇 )                                            bi-EP(𝑦 ⦂ 𝑈 , 𝑦 ⦂ 𝑈 ) ← (⊤, emp, emp)
                                                                                                                                                                                                                                          (∗L )
                                                                                                                                                   bi-EP(𝑥 ⦂ 𝑇 ∗ 𝑦 ⦂ 𝑈 , 𝑦 ⦂ 𝑈 ) ← (⊤, emp, 𝑥 ⦂ 𝑇 )

                                                                                                                                                                                          Axiom
                                                                                                                                                                                                                     (ID)
                                                                                                                                                                   bi-TP(𝑇 ,𝑇 , {(𝑥, 𝑧 3 )}) ← (⊤, 𝜆𝑥 .𝑥, Emp, Emp)       Trans(𝑇 , (=))
                                                                                                                                                                                                                                         (biTP)
                                                                                                        bi-EP(𝑥 ⦂ 𝑇 ∗ 𝑦 ⦂ 𝑈 , 𝑦 ⦂ 𝑈 ) ← (⊤, emp, 𝑥 ⦂ 𝑇 )                            bi-EP(𝑥 ⦂ 𝑇 , 𝑥 ⦂ 𝑇 ) ← (⊤, emp, emp)
                                                                                                                                                                                                                          (∗R )




                                                                                                                                                                                                                                                                   Qiyuan Xu, David Sanan, Zhe Hou, Xiaokun Luan, Conrad Watt, and Yang Liu
                                                                                                                                     bi-EP(𝑥 ⦂ 𝑇 ∗ 𝑦 ⦂ 𝑈 , 𝑦 ⦂ 𝑈 ∗ 𝑥 ⦂ 𝑇 ) ← (⊤, emp, emp)

                                                                                                                                                                                                      (bi-EP)
                                                                                                                                             ⊤ | (𝑥 ⦂ 𝑇 ) ∗ (𝑦 ⦂ 𝑈 ) ⊢ (𝑦 ⦂ 𝑈 ) ∗ (𝑥 ⦂ 𝑇 )

                                                                                          Fig. 9. The derivation of (𝑥 ⦂ 𝑇 ) ∗ (𝑦 ⦂ 𝑈 ) −→ (𝑦 ⦂ 𝑈 ) ∗ (𝑥 ⦂ 𝑇 ). The tree is too large, so we split it into two parts linked by brown. Blue color denotes a frame
                                                                                          and red denotes an antiframe. Gray arrows help readers to trace the predicates.

                                                                                          H Example: Deriving (𝑥 ⦂ 𝑇 ) ∗ (𝑦 ⦂ 𝑈 ) −→ (𝑦 ⦂ 𝑈 ) ∗ (𝑥 ⦂ 𝑇 )
                                                                                          Instead of permuting predicates on the left-hand sides, nor matching the left-hand side items with the right-hand side, our reasoner decomposes
                                                                                          (𝑥 ⦂ 𝑇 ) ∗ (𝑦 ⦂ 𝑈 ) −→ (𝑦 ⦂ 𝑈 ) ∗ (𝑥 ⦂ 𝑇 ) into three bi-TPs as illustrated in Fig. 9. First, by (∗R ), (∗L ), we extract the first target 𝑦 ⦂ 𝑈 from the
                                                                                          first source item 𝑥 ⦂𝑇 , written bi-EP(𝑥 ⦂𝑇 , 𝑦 ⦂ 𝑈 ). It reduces to bi-TP(𝑇 , 𝑈 , {𝑥 }) by (biTP). As no bi-TP rule is further applicable, fallback (FB2 )
                                                                                          is called, leaving the entire 𝑥 ⦂ 𝑇 as the remaining source and the entire 𝑦 ⦂ 𝑈 as the unfulfilled target. Next, as stated in rule (∗R ) and (∗L ),
                                                                                          the reasoning process turns to extract the unfulfilled target from the second source item and to extract the second target from the remaining
                                                                                          source, i.e., bi-EP(𝑦 ⦂ 𝑈 , 𝑦 ⦂ 𝑈 ) and bi-EP(𝑥 ⦂ 𝑇 , 𝑥 ⦂ 𝑇 ), both of which trivially succeed.
Generically Automating Separation Logic by Functors, Homomorphisms, and Modules                               67:41

I   The Module-like Algebra of Linked List Segment
This section means to show that the data structure of Linked List segment also satisfies the (relaxed)
model of modules over rings.
    • Let 𝑙 ⦂ Lseg 𝑎 𝑛 𝑏 represent a linked list Segment having head address 𝑎, tail address 𝑏 and
      length 𝑛. The abstraction of this segment is denoted by a logical list 𝑙.
    • A scalar is a labelled arrow Lseg 𝑎 𝑛 𝑏 from the head node to the tail node, with the length
      as its label. The scalar addition is the arrow concatenation (with adding the labelled length),
      and a zero scalar is a 0-length loop.
                                                                       b                        0
                    a        n         b                         n            m
                                                     a               n+m             c          a
                      the scalar for
                   an Lseg from a to b                           Scalar Addition           Scalar Zero

                                                         Laws
                                                                                   cat
                                        ©    Lseg 𝑎          𝑛
                                                                 𝑏
                                                                   ∗ Lseg 𝑏 𝑚 𝑐 −−−→ Lseg 𝑎 𝑛+𝑚 𝑐 ª
            Distributivity              ­                                         cut
                                                                                                  ®
                                        «∃𝑏. Lseg 𝑎          𝑛
                                                                 𝑏
                                                                   ∗ Lseg 𝑏
                                                                            𝑚
                                                                              𝑐
                                                                                ← −−− Lseg 𝑎
                                                                                             𝑛+𝑚
                                                                                                 𝑐¬

            Identity                   [𝑥] ⦂ Lseg 𝑎          1
                                                                 𝑏
                                                                           (data: 𝑥, nxt: 𝑏) ⦂ Node𝑎

            Zero                       Lseg 𝑎    0
                                                         𝑎
                                                                     Empty
The red-marked existential quantification might suggest the demand of an extension to the system
presented in the paper.
Received 2024-07-11; accepted 2024-11-07




                             Proc. ACM Program. Lang., Vol. 9, No. POPL, Article 67. Publication date: January 2025.
