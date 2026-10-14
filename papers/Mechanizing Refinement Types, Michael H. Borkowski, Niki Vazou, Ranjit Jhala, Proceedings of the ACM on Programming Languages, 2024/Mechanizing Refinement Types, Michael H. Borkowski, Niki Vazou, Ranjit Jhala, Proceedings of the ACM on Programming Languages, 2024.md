                                         Mechanizing Refinement Types

                                         MICHAEL BORKOWSKI, UC San Diego, USA
                                         NIKI VAZOU, IMDEA Software Institute, Spain
arXiv:2207.05617v1 [cs.PL] 12 Jul 2022




                                         RANJIT JHALA, UC San Diego, USA
                                         Practical checkers based on reﬁnement types use the combination of implicit semantic subtyping and para-
                                         metric polymorphism to simplify the speciﬁcation and automate the veriﬁcation of sophisticated properties
                                         of programs. However, a formal meta-theoretic accounting of the soundness of reﬁnement type systems us-
                                         ing this combination has proved elusive. We present 𝜆𝑅𝐹 , a core reﬁnement calculus that combines semantic
                                         subtyping and parametric polymorphism. We develop a metatheory for this calculus and prove soundness of
                                         the type system. Finally, we give a full mechanization of our metatheory using the reﬁnement-type based
                                         LiqidHaskell as a proof checker, showing how reﬁnements can be used for mechanization.

                                         1 INTRODUCTION
                                         Reﬁnements constrain types with logical predicates to specify new concepts. For example, the
                                         reﬁnement type Pos  Int {𝜈 : 0 < 𝑣 } describes positive integers and Nat  Int {𝜈 : 0 ≤ 𝑣 } spec-
                                         iﬁes natural numbers. Reﬁnements on types have been successfully used to deﬁne sophisticated
                                         concepts (e.g. secrecy [Fournet et al. 2011], resource constraints [Knoth et al. 2020], security poli-
                                         cies [Lehmann et al. 2021]) that can then be veriﬁed in programs developed in various program-
                                         ming languages like Haskell [Vazou et al. 2014b], Scala [Hamza et al. 2019], Racket [Kent et al.
                                         2016] and Ruby [Kazerounian et al. 2017].
                                            The success of reﬁnement types relies on the combination of two essential features. First, im-
                                         plicit semantic subtyping uses semantic (SMT-solver based) reasoning to automatically convert
                                         the types of expressions without troubling the programmer for explicit type casts. For example,
                                         consider a positive expression 𝑒 : Pos and a function expecting natural numbers 𝑓 : Nat → Int.
                                         To type check the application 𝑓 𝑒, the reﬁnement type system will implicitly convert the type of 𝑒
                                         from Pos to Nat, because 0 < 𝑣 ⇒ 0 ≤ 𝑣 semantically holds. Importantly, reﬁnement types prop-
                                         agate semantic subtyping inside type constructors to, for example, treat function arguments in
                                         a contravariant manner. Second, parametric polymorphism allows the propagation of the reﬁned
                                         types through polymorphic function interfaces, without the need for extra reasoning. As a triv-
                                         ial example, once we have established that 𝑒 is positive, parametric polymorphism should let us
                                         conclude that 𝑓 𝑒 : Pos if, for example, 𝑓 is the identity function 𝑓 : 𝑎 → 𝑎.
                                            As is often the case with useful ideas, the engineering of practical tools has galloped far ahead
                                         of the development of the meta-theoretical foundations for reﬁnements with subtyping and poly-
                                         morphism. In fact, such a development is diﬃcult. As Sekiyama et al. [2017] observe, a naïve com-
                                         bination of type variables and subtyping leads to unsoundness because potentially contradicting
                                         reﬁnements can be lost at type instantiation. Their suggested solution replaces semantic with
                                         syntactic subtyping, which is signiﬁcantly less expressive. Other recent formalizations of reﬁne-
                                         ment types either drop semantic subtyping [Hamza et al. 2019] or polymorphism [Flanagan 2006;
                                         Swamy et al. 2016].
                                            In this paper we present 𝜆𝑅𝐹 , a core calculus with a reﬁnement type system that combines seman-
                                         tic subtyping with reﬁned polymorphic type variables. We develop and establish the properties of
                                         𝜆𝑅𝐹 with four concrete contributions.
                                         1. Reconciliation Our ﬁrst contribution is a language that combines reﬁnements and polymor-
                                         phism in a way that ensures the metatheory remains sound without sacriﬁcing the expressiveness
                                         Authors’ addresses: Michael Borkowski, UC San Diego, USA, mborkows@eng.ucsd.edu; Niki Vazou, IMDEA Software
                                         Institute, Spain, niki.vazou@imdea.org; Ranjit Jhala, UC San Diego, USA, rjhala@eng.ucsd.edu.

                                                                                                       , Vol. 1, No. 1, Article . Publication date: July 2022.
2                                                           Michael Borkowski, Niki Vazou, and Ranjit Jhala


needed for practical veriﬁcation. To this end, 𝜆𝑅𝐹 introduces a kind system that distinguishes the
type variables that can be soundly reﬁned (without the risk of losing reﬁnements at instantiation)
from the rest, which are then left unreﬁned. In addition our design includes a form of existential
typing [Knowles and Flanagan 2009b] which is essential to synthesize the types – in the sense of
bidirectional typing – for applications and let-binders in a compositional manner (§ 3, 4).
2. Foundation Our second contribution is to establish the foundations of 𝜆𝑅𝐹 by proving sound-
ness, which says that if 𝑒 has a type then, either 𝑒 is a value or it can step to another term of
the same type. The combination of semantic subtyping, polymorphism, and existentials makes
the soundness proof challenging with circular dependencies that do not arise in standard (unre-
ﬁned) calculi. To ease the presentation and tease out the essential ingredients of the proof we stage
the metatheory. First, we review an unreﬁned base language 𝜆𝐹 , a classic System F [Pierce 2002]
with primitive Int and Bool types (§ 5). Next, we show how reﬁnements (kinds, subtyping, and
existentials) must be accounted for to establish the soundness of 𝜆𝑅𝐹 (§ 6).
3. Reiﬁcation Our third contribution is to introduce data propositions a novel feature that en-
ables the encoding of derivation trees for inductively deﬁned judgments as reﬁned data types, by
ﬁrst reifying the propositions and evidence as plain Haskell data, and then using reﬁnements to
connect the two. Hence, data propositions let us write plain Haskell functions over reﬁned data to
provide explicit, constructive proofs (§ 7). Without data propositions reasoning about potentially
non-terminating computations was not possible in LiqidHaskell, thereby precluding even sim-
ple meta-theoretic developments such as the soundness of 𝜆𝐹 let alone 𝜆𝑅𝐹 .
4. Veriﬁcation Our ﬁnal contribution is to fully mechanize the metatheory of 𝜆𝑅𝐹 using Liqid-
Haskell. Our formalization uses data propositions and recursive Haskell functions on derivation
trees to produce explicit witnesses that correspond to proofs of our soundness theorems [Vazou et al.
2018]. Our proof is non-trivial, requiring 9,400 lines of code and 30 minutes to verify. While we
are certain that it is possible, and perhaps simpler, to implement the mechanization with special-
ized proof assistants and tactics, our contribution is to show this is feasible purely as a (reﬁned)
Haskell program. Indeed, we show that substantial meta-theoretical formalizations over arbitrary
computations are feasible via data propositions via LiqidHaskell-style reﬁnement typing (§ 8).

2 OVERVIEW
Our overall strategy is to present the metatheory for 𝜆𝑅𝐹 in two parts. First, we review the metathe-
ory for 𝜆𝐹 : a familiar starting point that corresponds to the full language with reﬁnements erased
(§ 5). Second, we use the scaﬀolding established by 𝜆𝐹 to highlight the extensions needed to develop
the metatheory for reﬁnements in 𝜆𝑅𝐹 (§ 6). Let’s begin with a high-level overview that describes a
proof skeleton that is shared across the developments for 𝜆𝐹 and 𝜆𝑅𝐹 , the speciﬁc challenges posed
by reﬁnements, and the machinery needed to go from the simpler 𝜆𝐹 to the reﬁned 𝜆𝑅𝐹 .
Types and Terms Both 𝜆𝐹 and 𝜆𝑅𝐹 have the same syntax for terms 𝑒 (Fig. 2). 𝜆𝐹 has the usual
syntax for types 𝑡 familiar from System F, while 𝜆𝑅𝐹 additionally allows (𝜆𝐹 ’s) types to be reﬁned
by terms (respectively, the white parts and all of Fig. 3), and existential types. Both languages
include a notion of kinds 𝑘 that qualify the types that are allowed to be reﬁned.
Judgments Both languages have typing judgments Γ ⊢ 𝑒 : 𝑡 which say that a term 𝑒 has type 𝑡 with
respect to a binding environment (i.e. context) Γ. Additionally, both languages have well-formedness
judgments Γ ⊢𝑤 𝑡 : 𝑘 which say that a type 𝑡 has the kind 𝑘 in context Γ, by requiring that the free
variables in 𝑡 are appropriately bound in the environment Γ. (Though some presentations of 𝜆𝐹
[Pierce 2002] eschew well-formedness judgments, they are helpful for a mechanized metatheory
[Aydemir et al. 2008]). Crucially, 𝜆𝑅𝐹 has a subtyping judgment Γ ⊢ 𝑡 1  𝑡 2 which says that type 𝑡 1
is a subtype of 𝑡 2 in context Γ. Subtyping for reﬁned base types is established via an axiomatized

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                                     3


                                                                                              Values Stuck
                        Progress                        Preservation
                                                                                             Det. Semantics



             Canonical Forms       Inversion of Typing                 Primitives                 Polym. Prim.



                                      Transitivity                 Substitution Lemma
            Narrowing Lemmas
                                                                  Substitute: var in typ        Substitution Lemma
                                                                                                Substitute: var in wf
                                   Weakening Lemma                Substitute: var in sub
               Exact Types
                                   Weaken: var in typ                                            Substitute: tv in wf
                                                                   Substitute: tv in typ
                                   Weaken: var in sub
              Exact Subtypes                                       Substitute: tv in sub         Weakening Lemma
                                    Weaken: tv in typ                                            Weaken: var in wf

                                    Weaken: tv in sub                                             Weaken: tv in wf




Fig. 1. Logical dependencies in the metatheory. We write “var” to abbreviate a term variable and “tv” to
abbreviate a type variable.


implication judgment Γ ⊢ 𝑝 ⇒ 𝑞 which says that the term 𝑝 logically implies the term 𝑞 whenever
their free variables are given values described by Γ. We take an axiomatized approach to capture
the properties required by an implication checking oracle for proving soundness.
Proof Landscape Fig. 1 charts the overall landscape of our formal development as a dependency
graph of the main lemmas which establish meta-theoretic properties of the diﬀerent judgments.
Nodes shaded light grey represent lemmas in the metatheories for 𝜆𝐹 and 𝜆𝑅𝐹 . The dark grey nodes
denote lemmas that only appear in 𝜆𝑅𝐹 . An arrow shows a dependency: the lemma at the tail is
used in the proof of the lemma at the head. Darker arrows are dependencies in 𝜆𝑅𝐹 only.
Soundness via Preservation and Progress For both 𝜆𝑅𝐹 and 𝜆𝐹 we establish soundness via
• Progress: If a closed term is well-typed, then either it is a value or it can be further evaluated;
• Preservation: If a closed term is well-typed, then its type is preserved under evaluation.
The type soundness theorem states that a well-typed closed term cannot become stuck: any se-
quence of evaluation steps will either end with a value or the sequence can be extended by another
step. Next, we describe the lemmas used to establish preservation and progress for 𝜆𝐹 and then
outline the essential new ingredients that demonstrate soundness for the reﬁned 𝜆𝑅𝐹 .

2.1 Metatheory for 𝜆𝐹
Progress in 𝜆𝐹 is standard as the typing rules are syntax-directed. The top-level rule used to obtain
the typing derivation for a term 𝑒 uniquely determines the syntactic structure of 𝑒 which lets us
use the appropriate small-step reduction rule to obtain the next step of the evaluation of 𝑒.
Preservation says that when a well-typed expression 𝑒 steps to 𝑒 ′ , then 𝑒 ′ is also well-typed.
As usual, the non-trivial case is when the step is a type abstraction Λ𝛼 :𝑘.𝑒 (respectively lambda
abstraction 𝜆𝑥 .𝑒) applied to a type (respectively value), in which case the term 𝑒 ′ is obtained by
substituting the type or value appropriately in 𝑒. Thus, our 𝜆𝐹 metatheory requires us to prove
a Substitution Lemma, which describes how typing judgments behave under substitution of free

                                                                            , Vol. 1, No. 1, Article . Publication date: July 2022.
4                                                                           Michael Borkowski, Niki Vazou, and Ranjit Jhala


term or type variables. Additionally, some of our typing rules use well-formedness judgments and
so we must also prove that well-formedness is preserved by substitution.
Substitution requires some technical lemmas that let us weaken judgments by adding any fresh
variable to the binding environment.
Primitives Finally, the primitive reduction steps (e.g. arithmetic operations) require the assump-
tion that the reduction rules deﬁned for the built-in primitives are type preserving.

2.2    What’s hard about Refinements?
Subtyping Reﬁnement types rely on implicit semantic subtyping, that is, type conversion (from
subtypes) happens without any explicit casts and is checked semantically via logical validity. For
example, consider a function 𝑓 that requires natural numbers as input, applied to a positive argu-
ment 𝑒. Let
                                    Γ  𝑓 : Nat → Int, 𝑒 : Pos
The application 𝑓 𝑒 will type check as below, using the T-Sub rule to implicitly convert the type of
the argument and the S-Base rule to check that positive integers are always naturals by checking
the validity of the formula ∀𝑣. 0 < 𝑣 ⇒ 0 ≤ 𝑣.
                                                                                       ∀𝑣. 0 < 𝑣 ⇒ 0 ≤ 𝑣
                                                                           T-Var                                  S-Base
                                                             Γ ⊢ 𝑒 : Pos                  Γ ⊢ Pos  Nat
                                        T-Var                                                                     T-Sub
              Γ ⊢ 𝑓 : Nat → Int                                                Γ ⊢ 𝑒 : Nat
                                                                                                                   T-App
                                                          Γ ⊢ 𝑓 𝑒 : Int
  Importantly, most reﬁnement type systems use type-constructor directed rules to destruct sub-
typing obligations into basic (semantic) implications. For example, in Fig. 8 the rule S-Func states
that functions are covariant on the result and contravariant on the arguments. Thus, a reﬁnement
type system can, without any annotations or casts, decide that 𝑒 : Nat → Pos is a suitable argu-
ment for the higher order function 𝑓 : ( Pos → Nat) → Int.
Existentials For compositional and decidable type checking, some reﬁnement type systems use
an existential type [Knowles and Flanagan 2009a] to check dependent function application, i.e. the
TApp-Exists rule below, instead of the standard type-theoretic TApp-Exact rule.
              Γ ⊢ 𝑓 : 𝑥 :𝑡𝑥 → 𝑡            Γ ⊢ 𝑒 : 𝑡𝑥                      Γ ⊢ 𝑓 : 𝑥 :𝑡𝑥 → 𝑡         Γ ⊢ 𝑒 : 𝑡𝑥
                                                          TApp-Exact                                              TApp-Exists
                        Γ ⊢ 𝑓 𝑒 : 𝑡 [𝑒/𝑥]                                          Γ ⊢ 𝑓 𝑒 : ∃ 𝑥 :𝑡𝑥 . 𝑡
    To understand the diﬀerence, consider some expression 𝑒 of type Pos and the identity function
𝑓
                            𝑒 : Pos                              𝑓 : 𝑥 : Int → Int {𝑣 : 𝑣 = 𝑥 }
The application 𝑓 𝑒 is typed as Int {𝑣 : 𝑣 = 𝑒} with the TApp-Exact rule, which has two problems.
First, the information that 𝑒 is positive is lost. To regain this information the system needs to
re-analyze the expression 𝑒 breaking compositional reasoning. Second, the arbitrary expression 𝑒
enters the reﬁnement logic making it impossible for the system to restrict reﬁnements into decid-
able logical fragments. Using the TApp-Exists rule, both of these problems are addressed. The type
of 𝑓 𝑒 becomes ∃ 𝑥 : Pos . Int {𝑣 : 𝑣 = 𝑥 } preserving the information that the application argument
is positive, while the variable 𝑥 cannot break any carefully crafted decidability guarantees.
   Knowles and Flanagan [2009a] introduce the existential application rule and show that it pre-
serves the decidability and completeness of the reﬁnement type system. An alternative approach
for decidable and compositional type checking is to ensure that all the application arguments are

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                     5


variables by ANF transforming the original program [Flanagan et al. 1993]. ANF is more amicable
to implementation as it does not require the deﬁnition of one more type form. However, ANF is
more problematic for the metatheory, as ANF is not preserved by evaluation. Additionally, existen-
tials let us synthesize types for let-binders in a bidirectional style: when typing let 𝑥 = 𝑒 1 in 𝑒 2 ,
the existential lets us eliminate 𝑥 from the type synthesized for 𝑒 2 , yielding a precise, algorithmic
system [Cosman and Jhala 2017]. Thus, we choose to use existential types in 𝜆𝑅𝐹 .
Polymorphism Polymorphism is a precious type abstraction [Wadler 1989], but combined with
reﬁnements, it can lead to imprecise or, worse, unsound systems. As an example, below we present
the function max with four potential type signatures.
                               Deﬁnition     max   = 𝜆𝑥 𝑦.if 𝑥 < 𝑦 then 𝑦 else 𝑥
  Attempt 1:        Monomorphism max               ::   𝑥 : Int → 𝑦: Int → Int {𝜈 : 𝑥 ≤ 𝜈 ∧ 𝑦 ≤ 𝜈 }
  Attempt 2: Unreﬁned Polymorphism max             ::   𝑥 :𝛼 → 𝑦:𝛼 → 𝛼
  Attempt 3:   Reﬁned Polymorphism max             ::   𝑥 :𝛼 → 𝑦:𝛼 → 𝛼 {𝜈 : 𝑥 ≤ 𝜈 ∧ 𝑦 ≤ 𝜈 }
       𝜆𝑅𝐹 :   Kinded Polymorphism max             ::   ∀ 𝛼 :𝐵. 𝑥 :𝛼 → 𝑦:𝛼 → 𝛼 {𝜈 : 𝑥 ≤ 𝜈 ∧ 𝑦 ≤ 𝜈 }
As a ﬁrst attempt, we give max a monomorphic type, stating that the result of max is an integer
greater or equal to any of its arguments. This type is insuﬃcient because it forgets any information
known for max’s arguments. For example, if both arguments are positive, the system cannot decide
that max x y is also positive. To preserve the argument information we give max a polymorphic
type, as a second attempt. Now the system can deduce that max x y is positive, but forgets that
it is also greater or equal to both x and y. In a third attempt, we naively combine the beneﬁts of
polymorphism with reﬁnements to give max a very precise type that is suﬃcient to propagate the
arguments’ properties (positivity) and max behavior (inequality).
    Unfortunately, reﬁnements on arbitrary type variables are dangerous for two reasons. First, the
type of max implies that the system allows comparison between any values (including functions).
Second, if reﬁnements on type variables are allowed, then, for soundness [Belo et al. 2011], all the
types that substitute variables should be reﬁned. For example, if a type variable is reﬁned with
false (that is, 𝛼 {𝜈 : false}) and gets instantiated with an unreﬁned function type (𝑥 :𝑡𝑥 → 𝑡),
then the false reﬁnement is lost and the system becomes unsound.
Base Kind when Reﬁned To preserve the beneﬁts on reﬁnements on type variables, without
the complications of reﬁning function types, we introduce a kind system that separates the type
variables that can be reﬁned with the ones that cannot. Variables with the base kind 𝐵, can be
reﬁned, compared, and only substituted by base, reﬁned types. The other type variables have kind
★ and can only be trivially reﬁned with true. With this kind system, we give max a polymorphic
and precise type that naturally rejects non comparable (e.g. function) arguments.

2.3   From 𝜆𝐹 to 𝜆𝑅𝐹
The metatheory for 𝜆𝑅𝐹 requires us to enrich that of 𝜆𝐹 with three essential and non-trivial blocks
— shown as shaded regions in Fig. 1 — that help surmount the challenges posed by the combination
of reﬁnements with existentials, subtyping and polymorphism.
Typing Inversion First, thanks to (reﬁnement) subtyping 𝜆𝑅𝐹 is not syntax directed, and so we
cannot directly invert the typing derivations of terms to get derivations for their sub-terms. For
example, we cannot directly invert a derivation Γ ⊢ 𝜆𝑥 .𝑒 : 𝑥 :𝑡𝑥 → 𝑡 to obtain a typing derivation
that the body 𝑒 has type 𝑡 because the above derivation may have been established using (multiple
instances of) subtyping. The typing inversion lemmas addresses this problem by using the transi-
tivity of subtyping to restructure the judgment tree to collapse all use of subtyping in a way that
lets us invert the non-subtyping judgment to conclude that if a term (e.g. 𝜆𝑥 .𝑒) is well-typed, then

                                                            , Vol. 1, No. 1, Article . Publication date: July 2022.
6                                                                        Michael Borkowski, Niki Vazou, and Ranjit Jhala


                     Primitives        𝑐    ::=    true | false         booleans
                                              |    0, 1, 2, . . .       integers
                                              |    ∧, ∨, ¬, ↔           boolean ops.
                                              |    ≤, =                 polymorphic comparisons
                          Values 𝑣          ::= 𝑐                       primitives
                                              | x, y, . . .             variables
                                              | 𝜆𝑥 .𝑒                   abstractions
                                              | Λ𝛼 :𝑘.e                 type abstractions
                           Terms 𝑒          ::=    𝑣                    values
                                              |    𝑒1 𝑒2                applications
                                              |    𝑒 [𝑡]                type applications
                                              |    let 𝑥 = 𝑒 1 in 𝑒 2   let-binders
                                              |    𝑒 :𝑡                 annotations

                                 Fig. 2. Syntax of Primitives, Values, and Expressions.


its components (e.g. 𝑒) are also well-typed. The proof of transitivity of subtyping is non-trivial due
to the presence of existential types. We cannot proceed by induction on the structure of the two
subtyping judgments (Γ ⊢ 𝑡 1  𝑡 2 and Γ ⊢ 𝑡 2  𝑡 3 ), because we do not apply the inductive hy-
pothesis directly to subderivations. We must ﬁrst apply the substitution and narrowing lemmas in
various cases, which may increase the size of derivations used in the inductive hypothesis (§ 6.1).
Instead, our proof goes by induction on a more intricate size (the combined depth of types 𝑡 1 , 𝑡 2 ,
and 𝑡 3 ).
Subtyping The biggest diﬀerence between the two metatheories is that 𝜆𝑅𝐹 has a notion of sub-
typing which is crucial to making reﬁnements practical. Subtyping complicates 𝜆𝑅𝐹 by introducing
a mutual dependency between the lemmas for typing and subtyping judgments. Recall that typing
depends on subtyping due to the usual subsumption rule (T-Sub in Fig. 7) that lets us weaken the
type of a term with a super-type. Conversely, subtyping depends upon typing because of the rule
(S-Witn in Fig. 8) which establishes subtyping between existential types. Thanks to this mutual
dependency, all of the lemmas from 𝜆𝐹 that relate to typing judgments, i.e. the weakening and sub-
stitution lemmas, are now mutually recursive with new versions for subtyping judgments shown
in the diagonal lined region in Fig. 1.
Narrowing Finally, due to subtyping, the proofs of the typing inversion and substitution lemmas
for 𝜆𝑅𝐹 require narrowing lemmas that allow us to replace a type that appears inside the binding
environment of a judgment with a subtype, thus “narrowing” the scope of the judgment. Due to the
mutual dependencies between the typing and subtyping judgments of 𝜆𝑅𝐹 , we must prove narrow-
ing for both typing and subtyping, which in turn depend on narrowing for well-formedness judg-
ments. A few important cases of the narrowing proofs require other technical lemmas shown in
the checkerboard region of Fig. 1. For example, the proof of narrowing for the “occurrence-typing”
rule T-Var that crucially enables path-sensitive reasoning, uses a lemma on selﬁfying [Ou et al.
2004] the types involved in the judgments.

3 LANGUAGE
For brevity, clarity and also to cut a circularity in the metatheory (in rule WF-Refn in § 4.1), we
formalize reﬁnements using two calculi. The ﬁrst is the base language 𝜆𝐹 : a classic System F [Pierce
2002] with call-by-value semantics extended with primitive Int and Bool types and operations.

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                            7


                      Kinds 𝑘        ::= 𝐵                                      base kind
                                       | ★                                      star kind
                 Predicates 𝑝        ::=   {𝑒 | ∃ Γ. Γ ⊢𝐹 𝑒 : Bool }            boolean-typed terms
                Base Types      𝑏    ::= Bool                                   booleans
                                       | Int                                    integers
                                       | 𝛼                                      type variables
                       Types     𝑡   ::= 𝑏 {𝜈 : 𝑝 }                              reﬁned base type
                                       |  𝑥 :𝑡𝑥 → 𝑡                             function type
                                       |  ∃ 𝑥 :𝑡𝑥 . 𝑡                            existential type
                                       | ∀ 𝛼 :𝑘. 𝑡                              polymorphic type
            Environments        Γ ::=      ∅                                    empty environment
                                    |      Γ, 𝑥 :𝑡                              variable binding
                                    |      Γ, 𝛼 :𝑘                              type binding

Fig. 3. Syntax of Types. The grey boxes are the extensions to 𝜆𝐹 needed by 𝜆𝑅𝐹 . We use 𝜏 for 𝜆𝐹 -only types.



The second calculus is the reﬁned language 𝜆𝑅𝐹 which extends 𝜆𝐹 with reﬁnements. By using
the ﬁrst calculus to express the typing judgments for our reﬁnements, we avoid making the well-
formedness and typing judgments be mutually dependent in our full language. We use the grey
highlights to indicate the extensions to the syntax and rules of 𝜆𝐹 needed to support reﬁnements
in 𝜆𝑅𝐹 .

3.1   Syntax
We start by describing the syntax of terms and types in the two calculi.
Constants, Values and Terms Fig. 2 summarizes the syntax of terms in both calculi. Terms are
stratiﬁed into primitive constants and values. The primitives 𝑐 include Int and Bool constants,
primitive boolean operations, and polymorphic comparison and equality primitive. Values 𝑣 are
those expressions which cannot be evaluated any further, including primitive constants, binders
and 𝜆- and type- abstractions. Finally, the terms 𝑒 comprise values, value- and type- applications,
let-binders and annotated expressions.
Kinds & Types Fig. 3 shows the syntax of the types, with the grey boxes indicating the extensions
to 𝜆𝐹 required by 𝜆𝑅𝐹 . In 𝜆𝑅𝐹 , only base types Bool and Int can be reﬁned: we do not permit
reﬁnements for functions and polymorphic types. 𝜆𝑅𝐹 enforces this restriction using two kinds
which denote types that may (𝐵) or may not (★) be reﬁned. The (unreﬁned) base types 𝑏 comprise
Int, Bool, and type variables 𝛼. The simplest type is of the form 𝑏{𝜈 : 𝑝 } comprising a base type 𝑏
and a reﬁnement that restricts 𝑏 to the subset of values 𝜈 that satisfy 𝑝 i.e. for which 𝑝 evaluates to
true. We use reﬁned base types to build up dependent function types (where the input parameter
𝑥 can appear in the output type’s reﬁnement), existential and polymorphic types. In the sequel, we
write 𝑏 to abbreviate 𝑏{𝜈 : true} and call types reﬁned with only true “trivially reﬁned” types.
Reﬁnement Erasure The reduction semantics of our polymorphic primitives are deﬁned using
an erasure function that returns the unreﬁned, 𝜆𝐹 version of a reﬁned 𝜆𝑅𝐹 type:

  ⌊𝑏{𝜈 : 𝑝 }⌋  𝑏,   ⌊𝑥 :𝑡𝑥 → 𝑡⌋  ⌊𝑡𝑥 ⌋ → ⌊𝑡⌋,         ⌊∃ 𝑥 :𝑡𝑥 . 𝑡 ⌋  ⌊𝑡⌋,     and    ⌊∀ 𝛼 :𝑘. 𝑡 ⌋  ∀ 𝛼 :𝑘. ⌊𝑡⌋

                                                                   , Vol. 1, No. 1, Article . Publication date: July 2022.
8                                                                               Michael Borkowski, Niki Vazou, and Ranjit Jhala


Operational Semantics                                                                                                𝑒 ↩→ 𝑒 ′
                                                                                  𝑒 ↩→ 𝑒 ′
                             E-Prim                                  E-PrimT                      E-Ann                E-AnnV
         𝑐 𝑣 ↩→ 𝛿 (𝑐, 𝑣)                𝑐 [𝑡] ↩→ 𝛿𝑇 (𝑐, ⌊𝑡⌋)                   𝑒 : 𝑡 ↩→ 𝑒 ′ : 𝑡           𝑣 : 𝑡 ↩→ 𝑣

                      𝑒 ↩→ 𝑒 ′                            𝑒 ↩→ 𝑒 ′
                                      E-App1                           E-App2                                 E-AppAbs
                   𝑒 𝑒 1 ↩→ 𝑒 ′ 𝑒 1                  𝑣 𝑒 ↩→ 𝑣 𝑒 ′                     (𝜆𝑥 .𝑒) 𝑣 ↩→ 𝑒 [𝑣/𝑥]

                                 𝑒 ↩→ 𝑒 ′
                                                 E-AppT                                              E-AppTAbs
                             𝑒 [𝑡] ↩→ 𝑒 ′ [𝑡]                          (Λ𝛼 :𝑘.𝑒) [𝑡] ↩→ 𝑒 [𝑡/𝛼]

                                  𝑒𝑥 ↩→ 𝑒𝑥′
                                                                 E-Let                                           E-LetV
                let 𝑥 = 𝑒𝑥 in 𝑒 ↩→ let 𝑥 = 𝑒𝑥′ in 𝑒                              let 𝑥 = 𝑣 in 𝑒 ↩→ 𝑒 [𝑣/𝑥]


                                              Fig. 4. The small-step semantics.


                                            𝛽{𝑥 : 𝑝 }[𝑡𝛼 /𝛼]  𝛽{𝑥 : 𝑝 [𝑡𝛼 /𝛼]}, 𝛼 ≠ 𝛽
                                        (𝑥 :𝑡𝑥 → 𝑡) [𝑡𝛼 /𝛼]  𝑥 :(𝑡𝑥 [𝑡𝛼 /𝛼]) → 𝑡 [𝑡𝛼 /𝛼]
                                         (∃ 𝑥 :𝑡𝑥 . 𝑡) [𝑡𝛼 /𝛼]  ∃ 𝑥 :(𝑡𝑥 [𝑡𝛼 /𝛼]). 𝑡 [𝑡𝛼 /𝛼]
                                          (∀ 𝛽 :𝑘. 𝑡) [𝑡𝛼 /𝛼]  ∀ 𝛽 :𝑘. 𝑡 [𝑡𝛼 /𝛼]
                                           𝛼 {𝑥 : 𝑝 }[𝑡𝛼 /𝛼]  strengthen(𝑡𝛼 , 𝑝 [𝑡𝛼 /𝛼], 𝑥)

                             strengthen(𝛼 {𝑧 : 𝑞}, 𝑝, 𝑥)  𝛼 {𝑧 : 𝑝 [𝑧/𝑥] ∧ 𝑞}
                             strengthen(∃ 𝑧:𝑡𝑧 . 𝑡, 𝑝, 𝑥)  ∃ 𝑧:𝑡𝑧 . strengthen(𝑡, 𝑝, 𝑥)
                            strengthen(𝑥 :𝑡𝑥 → 𝑡, _, _)  𝑥 :𝑡𝑥 → 𝑡
                              strengthen(∀ 𝛼 :𝑘. 𝑡, _, _)  ∀ 𝛼 :𝑘. 𝑡

                                                  Fig. 5. Type substitution.


Environments Fig. 3 describes the syntax of typing environments Γ which contain both term
variables bound to types and type variables bound to kinds. These variables may appear in types
bound later in the environment. In our formalism, environments grow from right to left.
Note on Variable Representation Our metatheory requires that all variables bound in the envi-
ronment be distinct. Our mechanization enforces this invariant via the locally nameless represen-
tation [Aydemir et al. 2005]: free and bound variables become distinct objects in the syntax, as are
type and term variables. All free variables have unique names which never conﬂict with bound
variables represented as de Bruijn indices. This eliminates the possibility of capture in substitution
and the need to perform alpha-renaming during substitution. The locally nameless representation
avoids technical manipulations such as index shifting by using names instead of indices for free
variables (we discuss alternatives in § 9). To simplify the presentation of the syntax and rules, we
use names for bound variables to make the dependent nature of the function arrow clear.

3.2    Dynamic Semantics
Fig. 4 summarizes the substitution-based, call-by-value, contextual, small-step semantics for both
calculi. We specify the reduction semantics of the primitives using the functions 𝛿 and 𝛿𝑇 .

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                               9


Substitution The key diﬀerence with standard formulations is the notion of substitution for type
variables at (polymorphic) type-application sites as shown in rule E-AppTAbs in Fig. 4. Fig. 5 sum-
marizes how type substitution is deﬁned, which is standard except for the last line which deﬁnes
the substitution of a type variable 𝛼 in a reﬁned type variable 𝛼 {𝑥 : 𝑝 } with a type 𝑡 which is po-
tentially reﬁned. To do this substitution, we combine 𝑝 with the type 𝑡 by using strengthen(𝑡, 𝑝, 𝑥)
which essentially conjoins the reﬁnement 𝑝 to the top-level reﬁnement of a base-kinded 𝑡. For ex-
istential types, strengthen pushes the reﬁnement through the existential quantiﬁer. Function and
quantiﬁed types are left unchanged as they cannot be used to instantiate a reﬁned type variable
(which must be of base kind).
Primitives The function 𝛿 (𝑐, 𝑣) speciﬁes what an application 𝑐 𝑣 of a built-in monomorphic
primitive evaluates to. The reductions are deﬁned in a curried manner, i.e. we have that ≤ 𝑚 𝑛 ↩→∗
𝛿 (𝛿 (≤, 𝑚), 𝑛). Currying gives us unary relations like 𝑚≤ which is a partially evaluated version of
the ≤ relation. We also denote by 𝛿𝑇 (=, ⌊𝑡⌋) and 𝛿𝑇 (≤, ⌊𝑡⌋) a function specifying the reduction
rules for type applications for the polymorphic built-in primitives = and ≤.
         𝛿 (∧, true)          𝜆𝑥 . 𝑥      𝛿 (↔, true)             𝜆𝑥 . 𝑥           𝛿𝑇 (=, Bool)             ↔
        𝛿 (∧, false)          𝜆𝑥 . false 𝛿 (↔, false)             𝜆𝑥 . ¬𝑥           𝛿𝑇 (=, Int)             =
         𝛿 (∨, true)          𝜆𝑥 . true       𝛿 (≤, 𝑚)            𝑚≤               𝛿𝑇 (≤, Bool)             ≤
        𝛿 (∨, false)          𝜆𝑥 . 𝑥         𝛿 (𝑚≤, 𝑛)            (𝑚 ≤ 𝑛)           𝛿𝑇 (≤, Int)             ≤
          𝛿 (¬, true)         false            𝛿 (=, 𝑚)           𝑚=
        𝛿 (¬, false)          true           𝛿 (𝑚=, 𝑛)            (𝑚 = 𝑛)
Determinism Our proof of soundness uses the following property of the operational semantics.
  Lemma 3.1 (Determinism). For every expression 𝑒,
    • there exists at most one term 𝑒 ′ such that 𝑒 ↩→ 𝑒 ′ ,
    • there exists at most one value 𝑣 such that 𝑒 ↩→∗ 𝑣, and
    • if 𝑒 is a value there is no term 𝑒 ′ such that 𝑒 ↩→ 𝑒 ′ .

4 STATIC SEMANTICS
The static semantics of our calculi comprise four main judgment forms: well-formedness judgments
that determine when a type or environment is syntactically well-formed (in 𝜆𝐹 and 𝜆𝑅𝐹 ); typing
judgments that stipulate that a term has a particular type in a given context (in 𝜆𝐹 and 𝜆𝑅𝐹 ); sub-
typing judgments that establish when one type can be viewed as a subtype of another (in 𝜆𝑅𝐹 );
and implication judgments that establish when one predicate implies another (in 𝜆𝑅𝐹 ). Next, we
present the static semantics of 𝜆𝑅𝐹 by describing each of these judgments and the rules used to
establish them. We use grey to highlight the antecedents and rules speciﬁc to 𝜆𝑅𝐹 .
Co-ﬁnite Quantiﬁcation We deﬁne our rules using the co-ﬁnite quantiﬁcation technique of Aydemir et al.
[2008]. This technique enforces a small (but critical) restriction in the way fresh names are intro-
duced in the antecedents of rules. For example, below we present the standard (on the left) and
our (on the right) rules for type abstraction.
        𝛼 ′ ∉ Γ 𝛼 ′ :𝑘, Γ ⊢ 𝑒 [𝛼 ′ /𝛼] : 𝑡 [𝛼 ′ /𝛼]              ∀𝛼 ′ ∉ 𝐿. 𝛼 ′ :𝑘, Γ ⊢ 𝑒 [𝛼 ′ /𝛼] : 𝑡 [𝛼 ′ /𝛼]
                                                      T-Abs-Ex                                                     T-TAbs
                 Γ ⊢ Λ𝛼 :𝑘.𝑒 : ∀ 𝛼 :𝑘. 𝑡                                   Γ ⊢ Λ𝛼 :𝑘.𝑒 : ∀ 𝛼 :𝑘. 𝑡
The standard rule T-Abs-Ex requires the existence of a fresh type variable name 𝛼 ′ . Instead our co-
ﬁnite quantiﬁcation rule states that the rule holds for any name excluding a ﬁnite set of names 𝐿.
As observed by Aydemir et al. [2008] this rephrasing simpliﬁes the mechanization of metatheory
by eliminating the need for renaming lemmas.

                                                                      , Vol. 1, No. 1, Article . Publication date: July 2022.
10                                                            Michael Borkowski, Niki Vazou, and Ranjit Jhala


4.1    Well-formedness



Judgments The ternary judgment Γ ⊢𝑤 𝑡 : 𝑘 says that the type 𝑡 is well-formed in the environment
Γ and has kind 𝑘. The judgment ⊢𝑤 Γ says that the environment Γ is well formed, meaning that
variables are only bound to well-formed types. Well-formedness is also used in the (unreﬁned)
system 𝜆𝐹 , where Γ ⊢𝑤 𝜏 : 𝑘 means that the (unreﬁned) 𝜆𝐹 type 𝜏 is well-formed in environment
Γ and has kind 𝑘 and ⊢𝑤 Γ means that the free type and expression variables of the unreﬁned
environment Γ are bound earlier in the environment. While well-formedness is not strictly required
for 𝜆𝐹 , we found it helpful to simplify the mechanization [Rémy 2021].



Rules Fig. 6 summarizes the rules that establish the well-formedness of types and environments,
with the grey highlighting the parts relevant for reﬁnements. Rule WF-Base states that the two
closed base types (Int and Bool) are well-formed and have base kind on their own or with trivial
reﬁnement true. Similarly, rule WF-Var says that an unreﬁned or trivially reﬁned type variable
𝛼 is well-formed having kind 𝑘 so long as 𝛼 :𝑘 is bound in the environment. The rule WF-Refn
stipulates that a reﬁned base type 𝑏{𝑥 : 𝑝 } is well-formed with base kind in some environment if
the unreﬁned base type 𝑏 has base kind in the same environment and if the reﬁnement predicate
𝑝 has type Bool in the environment augmented by binding a fresh variable to type 𝑏. Note that if
𝑏 ≡ 𝛼 then we can only form the antecedent Γ ⊢𝑤 𝛼 {𝑥 : true} : 𝐵 when 𝛼 : 𝐵 ∈ Γ (rule WF-Var),
which prevents us from reﬁning star-kinded type variables. To break a circularity in our judgments,
in which well-formedness judgments can appear in the antecedent position of typing judgments
and a typing judgment would appear in the antecedent position of WF-Refn, we stipulate only
a 𝜆𝐹 judgment for 𝑝 having underlying type Bool. Our rule WF-Func states that a function type
𝑥 :𝑡𝑥 → 𝑡 is well-formed with star kind in some environment Γ if both type 𝑡𝑥 is well-formed (with
any kind) in the same environment and type 𝑡 is well-formed (with any kind) in the environment Γ
augmented by binding a fresh variable to 𝑡𝑥 . Rule WF-Exis states that an existential type ∃ 𝑥 :𝑡𝑥 . 𝑡 is
well-formed with some kind 𝑘 in some environment Γ if both type 𝑡𝑥 is well-formed (with any kind)
in the same environment and type 𝑡 is well-formed with kind 𝑘 in the environment Γ augmented
by binding a fresh variable to 𝑡𝑥 . Rule WF-Poly establishes that a polymorphic type ∀ 𝛼 :𝑘. 𝑡 has
star kind in environment Γ if the inner type 𝑡 is well-formed (with any kind) in environment Γ
augmented by binding a fresh type variable 𝛼 to kind 𝑘. Finally, rule WF-Kind simply states that if
a type 𝑡 is well-formed with base kind in some environment, then it is also well-formed with star
kind. This rule is required by our metatheory to convert base to star kinds in type variables.
    As for environments, rule WFE-Emp states that the empty environment is well-formed. Rule
WFE-Bind says that a well-formed environment Γ remains well-formed after binding a fresh vari-
able 𝑥 to any type 𝑡𝑥 that is well-formed in Γ. Finally rule WFE-TBind states that a well-formed
environment remains well-formed after binding a fresh type variable to any kind.



4.2    Typing
The judgment Γ ⊢ 𝑒 : 𝑡 states that the term 𝑒 has type 𝑡 in the context of environment Γ. We write
Γ ⊢𝐹 𝑒 : 𝜏 to indicate that term 𝑒 has the (unreﬁned) 𝜆𝐹 type 𝜏 in the (unreﬁned) context Γ. Fig. 7
summarizes the rules that establish typing for both 𝜆𝐹 and 𝜆𝑅𝐹 , with grey for the 𝜆𝑅𝐹 extensions.


, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                              11


Well-formed Type                                                                                              Γ ⊢𝑤 𝑡 : 𝑘

                        𝑏 ∈ {Bool, Int }                                     𝛼 :𝑘 ∈ Γ
                                                 WF-Base                                          WF-Var
                     Γ ⊢𝑤 𝑏 {𝑥 : true} : 𝐵                          Γ ⊢𝑤 𝛼 {𝑥 : true} : 𝑘

                     Γ ⊢𝑤 𝑏{𝑥 : true} : 𝐵        ∀𝑦 ∉ Γ. 𝑦 :𝑏, ⌊Γ⌋ ⊢𝐹 𝑝 [𝑦/𝑥] : Bool
                                                                                                    WF-Refn
                                               Γ ⊢𝑤 𝑏{𝑥 : 𝑝 } : 𝐵

                           Γ ⊢ 𝑤 𝑡𝑥 : 𝑘𝑥       ∀𝑦 ∉ Γ.        𝑦 :𝑡𝑥 , Γ ⊢𝑤 𝑡 [𝑦/𝑥] : 𝑘
                                                                                           WF-Func
                                               Γ ⊢𝑤 𝑥 :𝑡𝑥 → 𝑡 : ★

                               Γ ⊢ 𝑤 𝑡𝑥 : 𝑘𝑥    ∀𝑦 ∉ Γ. 𝑦 :𝑡𝑥 , Γ ⊢𝑤 𝑡 [𝑦/𝑥] : 𝑘
                                                                                           WF-Exis
                                               Γ ⊢𝑤 ∃ 𝑥 :𝑡𝑥 . 𝑡 : 𝑘

                     ∀𝛼 ′ ∉ Γ. 𝛼 ′ :𝑘, Γ ⊢𝑤 𝑡 [𝛼 ′ /𝛼] : 𝑘𝑡                         Γ ⊢𝑤 𝑡 : 𝐵
                                                                 WF-Poly                           WF-Kind
                                Γ ⊢𝑤 ∀ 𝛼 :𝑘. 𝑡 : ★                                  Γ ⊢𝑤 𝑡 : ★


Well-formed Environment                                                                                              ⊢𝑤 Γ

                                    Γ ⊢ 𝑤 𝑡𝑥 : 𝑘𝑥     ⊢𝑤 Γ 𝑥 ∉ Γ                        ⊢𝑤 Γ 𝛼 ∉ Γ
                     WFE-Emp                                             WFE-Bind                          WFE-TBind
              ⊢𝑤 ∅                             ⊢𝑤 𝑥 :𝑡𝑥 , Γ                                ⊢𝑤 𝛼 :𝑘, Γ

       Fig. 6. Well-formedness of types and environments. The rules for 𝜆𝐹 exclude the grey boxes.


Typing Primitives The type of a built-in primitive 𝑐 is given by the function ty(𝑐), which is de-
ﬁned for every constant of our system. Below we present essential examples of the ty(𝑐) deﬁnition.
                     ty(true)        Bool {𝑥 : 𝑥 = true}
                         ty(3)       Int {𝑥 : 𝑥 = 3}
                        ty(∧)        𝑥 : Bool → 𝑦: Bool → Bool {𝑣 : 𝑣 = 𝑥 ∧ 𝑦}
                      ty(𝑚≤)         𝑦: Int → Bool {𝑣 : 𝑣 = (𝑚 ≤ 𝑦)}
                        ty(≤)        ∀ 𝛼 :𝐵. 𝑥 :𝛼 → 𝑦:𝛼 → Bool {𝑣 : 𝑣 = (𝑥 ≤ 𝑦)}
                        ty(=)        ∀ 𝛼 :𝐵. 𝑥 :𝛼 → 𝑦:𝛼 → Bool {𝑣 : 𝑣 = (𝑥 = 𝑦)}
We note that the = used in the reﬁnements is the polymorphic equals with type applications elided.
Further, we use 𝑚≤ to represent an arbitrary member of the inﬁnite family of primitives 0≤, 1≤
, 2≤, . . .. For 𝜆𝐹 we erase the reﬁnements using ⌊ty(𝑐)⌋. The rest of the deﬁnition is similar.
   Our choice to make the typing and reduction of constants external to our language, i.e. respec-
tively given by the functions ty(𝑐) and 𝛿 (𝑐), makes our system easily extensible with further con-
stants. The requirement, for soundness, is that these two functions on constants together satisfy
the following four conditions.
  Reqirement 1. (Primitives) For every primitive 𝑐,
  (1) If ty(𝑐) = 𝑏{𝑥 : 𝑝 }, then ∅ ⊢𝑤 ty(𝑐) : 𝐵 and ∅ ⊢ true ⇒ 𝑝 [𝑐/𝑥].

                                                                      , Vol. 1, No. 1, Article . Publication date: July 2022.
12                                                                            Michael Borkowski, Niki Vazou, and Ranjit Jhala


Typing                                                                                                               Γ⊢𝑒 :𝑡
                                    𝑥 :𝑡 ∈ Γ        Γ ⊢𝑤 𝑡 : 𝑘                Γ ⊢ 𝑒 : 𝑥 :𝑡𝑥 → 𝑡           Γ ⊢ 𝑒 𝑥 : 𝑡𝑥
          ty(𝑐) = 𝑡                                               T-Var                                                  T-App
                       T-Prim
           Γ⊢𝑐 :𝑡                    Γ ⊢ 𝑥 : self( 𝑡 , 𝑥, 𝑘)                         Γ ⊢ 𝑒 𝑒𝑥 : ∃ 𝑥 :𝑡𝑥 . 𝑡

      ∀𝑦 ∉ Γ. 𝑦 :𝑡𝑥 , Γ ⊢ 𝑒 [𝑦/𝑥] : 𝑡 [𝑦/𝑥]                 Γ ⊢ 𝑤 𝑡𝑥 : 𝑘𝑥             Γ ⊢ 𝑒 : ∀ 𝛼 :𝑘. 𝑠       Γ ⊢𝑤 𝑡 : 𝑘
                                                                             T-Abs                                          T-TApp
                           Γ ⊢ 𝜆𝑥 .𝑒 : 𝑥 :𝑡𝑥 → 𝑡                                              Γ ⊢ 𝑒 [𝑡] : 𝑠 [𝑡/𝛼]

                                        ∀𝛼 ′ ∉ Γ.     𝛼 ′ :𝑘, Γ ⊢ 𝑒 [𝛼 ′ /𝛼] : 𝑡 [𝛼 ′ /𝛼]
                                                                                            T-TAbs
                                                    Γ ⊢ Λ𝛼 :𝑘.𝑒 : ∀ 𝛼 :𝑘. 𝑡

                     Γ ⊢ 𝑒 𝑥 : 𝑡𝑥        ∀𝑦 ∉ Γ. 𝑦 :𝑡𝑥 , Γ ⊢ 𝑒 [𝑦/𝑥] : 𝑡 [𝑦/𝑥]                Γ ⊢𝑤 𝑡 : 𝑘
                                                                                                            T-Let
                                                  Γ ⊢ let 𝑥 = 𝑒𝑥 in 𝑒 : 𝑡

                Γ⊢𝑒 :𝑡              Γ ⊢𝑤 𝑡 : 𝑘                   Γ⊢𝑒 :𝑠          Γ⊢𝑠 𝑡           Γ ⊢𝑤 𝑡 : 𝑘
                                                 T-Ann                                                            T-Sub
                         Γ⊢𝑒 :𝑡 :𝑡                                                 Γ⊢𝑒 :𝑡


              Fig. 7. Typing rules. The judgment Γ ⊢𝐹 𝑒 : 𝜏 is defined by excluding the grey boxes.


     (2) If ty(𝑐) = 𝑥 :𝑡𝑥 → 𝑡 or ty(𝑐) = ∀ 𝛼 :𝑘. 𝑡, then ∅ ⊢𝑤 ty(𝑐) : ★.
     (3) If ty(𝑐) = 𝑥 :𝑡𝑥 → 𝑡, then for all 𝑣 𝑥 such that ∅ ⊢ 𝑣 𝑥 : 𝑡𝑥 , ∅ ⊢ 𝛿 (𝑐, 𝑣 𝑥 ) : 𝑡 [𝑣 𝑥 /𝑥].
     (4) If ty(𝑐) = ∀ 𝛼 :𝑘. 𝑡, then for all 𝑡𝛼 such that ∅ ⊢𝑤 𝑡𝛼 : 𝑘, ∅ ⊢ 𝛿𝑇 (𝑐, 𝑡𝛼 ) : 𝑡 [𝑡𝛼 /𝛼].
    To type constants, rule T-Prim gives the type 𝑡𝑦(𝑐) to any built-in primitive 𝑐, in any context.
The typing rules for boolean and integer constants are included in T-Prim.
Typing Variables with Selﬁﬁcation Rule T-Var establishes that any variable 𝑥 that appears as
𝑥 :𝑡 in environment Γ can be given the selﬁﬁed type [Ou et al. 2004] self(𝑡, 𝑥, 𝑘) provided that Γ ⊢𝑤
𝑡 : 𝑘. This rule is crucial in practice, to enable path-sensitive “occurrence” typing [Tobin-Hochstadt and Felleise
2008], where the types of variables are reﬁned by control-ﬂow guards. For example, suppose we
want to establish 𝛼 : 𝐵 ⊢ (𝜆𝑥 .𝑥) : 𝑥 :𝛼 → 𝛼 {𝑦 : 𝑥 = 𝑦}, and not just 𝛼 : 𝐵 ⊢ (𝜆𝑥 .𝑥) : 𝛼 → 𝛼. The latter
judgment would result from applying rule T-Abs if T-Var merely stated that Γ ⊢ 𝑥 : 𝑡 whenever
𝑥 :𝑡 ∈ Γ. Thus we need to strengthen the T-Var rule to be selﬁﬁed. Informally, to get information
about 𝑥 into the reﬁnement level, we need to say that 𝑥 is constrained to elements of type 𝛼 that
are equal to 𝑥 itself. In order to express the exact type of variables, we introduce a “selﬁﬁcation”
function that strengthens a reﬁnement with the condition that a value is equal to itself. Since ab-
stractions do not admit equality, we only selﬁfy the base types and the existential quantiﬁcations
of them; using the self function deﬁned below.
               self(𝑏{𝑧 : 𝑝 }, 𝑥, 𝐵)  𝑏{𝑧 : 𝑝 ∧ 𝑧 = 𝑥 } self(∃ 𝑧:𝑡𝑧 . 𝑡, 𝑥, 𝑘)  ∃ 𝑧:𝑡𝑧 . self (𝑡, 𝑥, 𝑘)
              self(𝑥 :𝑡𝑥 → 𝑡, _, _)  𝑥 :𝑡𝑥 → 𝑡          self(∀ 𝛼 :𝑘. 𝑡, _, _)  ∀ 𝛼 :𝑘. 𝑡
Typing Applications with Existentials Our rule T-App states the conditions for typing a term
application 𝑒 𝑒𝑥 . Under the same environment, we must be able to type 𝑒 at some function type
𝑥 :𝑡𝑥 → 𝑡 and 𝑒𝑥 at 𝑡𝑥 . Then we can give 𝑒 𝑒𝑥 the existential type ∃ 𝑥 :𝑡𝑥 . 𝑡. The use of existen-
tial types in rule T-App is one of the distinctive features of our language and was introduced
by Knowles and Flanagan [2009b]. As overviewed in § 2.2, we chose this form of T-App over the

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                      13


conventional form with Γ ⊢ 𝑒 𝑒𝑥 : 𝑡 [𝑒𝑥 /𝑥] in the consequent position because our version prevents
the substitution of arbitrary expressions (e.g. functions and type abstractions) into reﬁnements. As
an alternative, we could have used A-Normal Form [Flanagan et al. 1993], but since this form is not
preserved under the small step operational semantics, it would greatly compicate our metatheory,
by forcing the deﬁnition of closing subtitutions for non-value expressions.

Other Typing Rules Rule T-Abs says that we can type a lambda abstraction 𝜆𝑥 .𝑒 at a function
type 𝑥 :𝑡𝑥 → 𝑡 whenever 𝑡𝑥 is well-formed and the body 𝑒 can be typed at 𝑡 in the environment
augmented by binding a fresh variable to 𝑡𝑥 . Our rule T-TApp states that whenever a term 𝑒 has
polymorphic type ∀ 𝛼 :𝑘. 𝑠, then for any well-formed type 𝑡 with kind 𝑘 in the same environment,
we can give the type 𝑠 [𝑡/𝛼] to the type application 𝑒 [𝑡]. For the 𝜆𝐹 variant of T-TApp, we erase
the reﬁnements (via ⌊𝑡⌋) before checking well-formedness and performing the substitution. The
rule T-TAbs establishes that a type-abstraction Λ𝛼 :𝑘.𝑒 can be given a polymorphic type ∀ 𝛼 :𝑘. 𝑡
in some environment Γ whenever 𝑒 can be given the well-formed type 𝑡 in the environment Γ
augmented by binding a fresh type variable to kind 𝑘. Next, rule T-Let states that an expression
let 𝑥 = 𝑒𝑥 in 𝑒 has type 𝑡 in some environment whenever 𝑡 is well-formed, 𝑒𝑥 can be given some
type 𝑡𝑥 , and the body 𝑒 can be given type 𝑡 in the augmented environment formed by binding a
fresh variable to 𝑡𝑥 . Rule T-Ann establishes that an explicit annotation 𝑒 : 𝑡 can indeed be given
the type 𝑡 when the underlying expression has type 𝑡 and 𝑡 is well-formed in the same context.
The 𝜆𝐹 version of the rule erases the reﬁnements and uses ⌊𝑡⌋. Finally, rule T-Sub tells us that we
can exchange a subtype 𝑠 for a supertype 𝑡 in a judgment Γ ⊢ 𝑠 : 𝑡 provided that 𝑡 is well-formed
in the same context and Γ ⊢ 𝑠  𝑡, which we present next.

4.3   Subtyping

Judgments Fig. 8 summarizes the rules that establish the subtyping judgment. The subtyping
judgment Γ ⊢ 𝑠  𝑡 stipulates that the type 𝑠 is a subtype of type the 𝑡 in the environment Γ and is
used in the subsumption typing rule T-Sub (of Fig. 7).

Subtyping Rules The rule S-Func states that one function type 𝑥 1 :𝑡𝑥1 → 𝑡 1 is a subtype of
another function type 𝑥 2 :𝑡𝑥2 → 𝑡 2 in a given environment Γ when both 𝑡𝑥2 is a subtype of 𝑡𝑥1 and
𝑡 1 is a subtype of 𝑡 2 when we augment Γ by binding a fresh variable to type 𝑡𝑥2 . As usual, note that
function subtyping is contravariant in the input type and covariant in the outputs. Rules S-Bind
and S-Witn establish subtyping for existential types [Knowles and Flanagan 2009b], respectively
when the existential appears on the left or right. Rule S-Bind allows us to exchange a universal
quantiﬁer (a variable bound to some type 𝑡𝑥 in the environment) for an existential quantiﬁer. If we
have a judgment of the form 𝑦 :𝑡𝑥 , Γ ⊢ 𝑡 [𝑦/𝑥]  𝑡 ′ where 𝑦 does not appear free in either 𝑡 ′ or in
the context Γ, then we can conclude that ∃ 𝑥 :𝑡𝑥 . 𝑡 is a subtype of 𝑡 ′ . Rule S-Witn states that if type
𝑡 is a subtype of 𝑡 ′ [𝑣 𝑥 /𝑥] for some value 𝑣 𝑥 of type 𝑡𝑥 , then we can discard the speciﬁc witness for
𝑥 and quantify existentially to obtain that 𝑡 is a subtype of ∃ 𝑥 :𝑡𝑥 . 𝑡 ′ . Rule S-Poly states when one
polymorphic type ∀ 𝛼 :𝑘. 𝑡 1 is a subtype of another polymorphic type ∀ 𝛼 :𝑘. 𝑡 2 in some environment
Γ. The requirement is that 𝑡 1 be a subtype of 𝑡 2 in the environment where we augment Γ by binding
a fresh type variable to kind 𝑘.
    Reﬁnements enter the scene in the rule S-Base which uses implication to specify that a reﬁned
base type 𝑏{𝑥 1 : 𝑝 1 } is a subtype of another 𝑏{𝑥 2 : 𝑝 2 } in context Γ when 𝑝 1 implies 𝑝 2 in the envi-
ronment Γ augmented by binding a fresh variable to the unreﬁned type 𝑏. Next, we describe how
implication is formalized in our system.

                                                              , Vol. 1, No. 1, Article . Publication date: July 2022.
14                                                                    Michael Borkowski, Niki Vazou, and Ranjit Jhala


4.4 Implication
The implication judgment Γ ⊢ 𝑝 1 ⇒ 𝑝 2 states that the implication 𝑝 1 ⇒ 𝑝 2 is (logically) valid under
the assumptions captured by the context Γ. In reﬁnement type implementations [Swamy et al. 2016;
Vazou et al. 2014a], this relation is implemented as an external automated (usually SMT) solver.
In non-mechanized reﬁnement type formalizations, there have been two approaches to formalize
predicate implication. Either directly reduce it into a logical implication (e.g. in Gordon and Fournet
[2010]) or deﬁne it using operational semantics (e.g. in Vazou et al. [2018]). It turns out that none
of these approaches can be directly encoded in a mechanized proof. The former approach is insuﬃ-
cient because it requires a formal connection between the (deeply embedded) terms of 𝜆𝑅𝐹 and the
terms of the logic, which has not yet been clearly established. The second approach is more direct,
since it gives meaning to implication using directly the terms of 𝜆𝑅𝐹 , via denotational semantics.
Sadly, the deﬁnition of denotational semantics for our polymorphic calculus is not currently pos-
sible: encoding type denotations as an inductive data type (or proposition in our LiqidHaskell
encoding § 8) requires a negative occurrence which is not currently admitted.
Abstracting over SMT-based Implication To bypass these problems we follow the approach
of Lehmann and Tanter [2016] and encode implication as an axiomatized judgment that satisﬁes
the below requirements.

     Reqirement 2. The implication relation satisﬁes the following statements:
  (1) (Reﬂexivity) Γ ⊢ 𝑝 ⇒ 𝑝.
  (2) (Transitivity) If Γ ⊢ 𝑝 1 ⇒ 𝑝 2 and Γ ⊢ 𝑝 2 ⇒ 𝑝 3 , then Γ ⊢ 𝑝 1 ⇒ 𝑝 3 .
  (3) (Introduction) If Γ ⊢ 𝑝 1 ⇒ 𝑝 2 and Γ ⊢ 𝑝 1 ⇒ 𝑝 3 , then Γ ⊢ 𝑝 1 ⇒ 𝑝 2 ∧ 𝑝 3 .
  (4) (Conjunction 1) Γ ⊢ 𝑝 1 ∧ 𝑝 2 ⇒ 𝑝 1 .
  (5) (Conjunction 2) Γ ⊢ 𝑝 1 ∧ 𝑝 2 ⇒ 𝑝 2 .
  (6) (Repetition) Γ ⊢ 𝑝 1 ∧ 𝑝 2 ⇒ 𝑝 1 ∧ 𝑝 1 ∧ 𝑝 2 .
  (7) (Narrowing) If Γ1 , 𝑥 :𝑡𝑥 , Γ2 ⊢ 𝑝 1 ⇒ 𝑝 2 and Γ2 ⊢ 𝑠𝑥  𝑡𝑥 , then Γ1 , 𝑥 :𝑠𝑥 , Γ2 ⊢ 𝑝 1 ⇒ 𝑝 2 .
  (8) (Weakening) If Γ1 , Γ2 ⊢ 𝑝 1 ⇒ 𝑝 2 , 𝑎, 𝑥 ∉ Γ, then Γ1 , 𝑥 :𝑡𝑥 , Γ2 ⊢ 𝑝 1 ⇒ 𝑝 2 and Γ1, 𝑎 :𝑘, Γ2 ⊢ 𝑝 1 ⇒
      𝑝2.
  (9) (Subst I) If Γ1 , 𝑥 :𝑡𝑥 , Γ2 ⊢ 𝑝 1 ⇒ 𝑝 2 and Γ2 ⊢ 𝑣 𝑥 : 𝑡𝑥 , then Γ1 [𝑣 𝑥 /𝑥], Γ2 ⊢ 𝑝 1 [𝑣 𝑥 /𝑥] ⇒ 𝑝 2 [𝑣 𝑥 /𝑥].
 (10) (Subst II) If Γ1 , 𝑎 :𝑘, Γ2 ⊢ 𝑝 1 ⇒ 𝑝 2 and Γ2 ⊢𝑤 𝑡 : 𝑘, then Γ1 [𝑡/𝑎], Γ2 ⊢ 𝑝 1 [𝑡/𝑎] ⇒ 𝑝 2 [𝑡/𝑎].
 (11) (Strengthening) If 𝑦 :𝑏{𝑥 : 𝑞}, Γ ⊢ 𝑝 1 ⇒ 𝑝 2 , then 𝑦 :𝑏, Γ ⊢ 𝑞[𝑦/𝑥] ∧ 𝑝 1 ⇒ 𝑞[𝑦/𝑥] ∧ 𝑝 2 .

  This axiomatic approach precisely explicates the properties that are required of the implication
checker in order to establish the soundness of the entire reﬁnement type system. In the future, we
can look into either verifying that these properties hold for SMT-based checkers, or even build
other kinds of implication oracles that adhere to this contract.

5 𝜆𝐹 SOUNDNESS
Next, we present the metatheory of the underlying (unreﬁned) 𝜆𝐹 that, even though it follows the
textbook techniques of Pierce [2002], it is a convenient stepping stone towards the metatheory for
(reﬁned) 𝜆𝑅𝐹 . In addition, the soundness results for 𝜆𝐹 are used for our full metatheory, as our well-
formedness judgments require the reﬁnement predicate to have the 𝜆𝐹 type Bool thereby avoiding
the circularity of using a regular typing judgment in the antecedents of the well-formedness rules.
The light grey boxes in Fig. 1 show the high level outline of the metatheory for 𝜆𝐹 which provides
a miniaturized model for 𝜆𝑅𝐹 but without the challenges of subtyping and existentials. Next, we de-
scribe the top-level type safety result, how it is decomposed into progress (§ 5.1) and preservation
(§ 5.2) lemmas, and the various technical results that support the lemmas.

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                              15


Subtyping                                                                                                       Γ⊢𝑠 𝑡

                           Γ ⊢ 𝑡𝑥2  𝑡𝑥1        ∀𝑦 ∉ Γ. 𝑦 :𝑡𝑥2 , Γ ⊢ 𝑡 1 [𝑦/𝑥]  𝑡 2 [𝑦/𝑥]
                                                                                                S-Func
                                          Γ ⊢ 𝑥 :𝑡𝑥1 → 𝑡 1  𝑥 :𝑡𝑥2 → 𝑡 2

          Γ ⊢ 𝑣 𝑥 : 𝑡𝑥    Γ ⊢ 𝑡  𝑡 ′ [𝑣 𝑥 /𝑥]              ∀𝑦 ∉ free(𝑡) ∪ Γ. 𝑦 :𝑡𝑥 , Γ ⊢ 𝑡 [𝑦/𝑥]  𝑡 ′
                                                 S-Witn                                                         S-Bind
                  Γ ⊢ 𝑡  ∃ 𝑥 :𝑡𝑥 . 𝑡 ′                                     Γ ⊢ ∃ 𝑥 :𝑡𝑥 . 𝑡  𝑡 ′

      ∀𝛼 ′ ∉ Γ. 𝛼 ′ :𝑘, Γ ⊢ 𝑡 1 [𝛼 ′ /𝛼]  𝑡 2 [𝛼 ′ /𝛼]            ∀𝑦 ∉ Γ. 𝑦 :𝑏, Γ ⊢ 𝑝 1 [𝑦/𝑥] ⇒ 𝑝 2 [𝑦/𝑥]
                                                          S-Poly                                                      S-Base
                Γ ⊢ ∀ 𝛼 :𝑘. 𝑡 1  ∀ 𝛼 :𝑘. 𝑡 2                                Γ ⊢ 𝑏{𝑥 : 𝑝 1 }  𝑏{𝑥 : 𝑝 2 }

                                                 Fig. 8. Subtyping Rules.


  The main type safety theorem for 𝜆𝐹 states that a well-typed term does not get stuck: i.e. either
evaluates to a value or can step to another term (progress) of the same type (preservation). The
judgment Γ ⊢𝐹 𝑒 : 𝜏 is deﬁned in Fig. 7 without the grey boxes, and for clarity we use 𝜏 for 𝜆𝐹
types.
  Theorem 5.1. (Type Safety) If ∅ ⊢𝐹 𝑒 : 𝜏 and 𝑒 ↩→∗ 𝑒 ′ , then 𝑒 ′ is a value or 𝑒 ′ ↩→ 𝑒 ′′ for some 𝑒 ′′ .
  We prove type safety by induction on the length of the sequence of steps comprising 𝑒 ↩→∗ 𝑒 ′ ,
using the preservation and progress lemmas.

5.1   Progress
The progress lemma says that a well-typed term is either a value or steps to some other term.
  Lemma 5.2. (Progress) If ∅ ⊢𝐹 𝑒 : 𝜏, then 𝑒 is a value or 𝑒 ↩→ 𝑒 ′ for some 𝑒 ′ .
   Proof of progress requires a Canonical Forms lemma (Lemma 5.3) which describes the shape
of well-typed values and some key properties about the built-in Primitives (Lemma 5.5). We also
implicitly use an Inversion of Typing lemma (Lemma 5.4) which describes the shape of the type
of well-typed terms and its subterms. For 𝜆𝐹 , unlike 𝜆𝑅𝐹 , this lemma is trivial because the typing
relation is syntax-directed.
  Lemma 5.3. (Canonical Forms)
  (1) If ∅ ⊢𝐹 𝑣 : Bool, then 𝑣 = true or 𝑣 = false.
  (2) If ∅ ⊢𝐹 𝑣 : Int, then 𝑣 is an integer constant.
  (3) If ∅ ⊢𝐹 𝑣 : 𝜏 → 𝜏 ′, then either 𝑣 = 𝜆𝑥 .𝑒 or 𝑣 = 𝑐, a constant function where 𝑐 ∈ {∧, ∨, ¬, ↔}.
  (4) If ∅ ⊢𝐹 𝑣 : ∀ 𝛼 :𝑘. 𝜏 , then either 𝑣 = Λ𝛼 :𝑘.𝑒 or 𝑣 = 𝑐, a polymorphic constant 𝑐 ∈ {≤, =}.
  (5) If ∅ ⊢𝑤 𝜏 : 𝐵, then 𝜏 = Bool or 𝜏 = Int.
  Lemma 5.4. (Inversion of Typing)
  (1) If Γ ⊢𝐹 𝑐 : 𝜏, then 𝜏 = ⌊ty(𝑐)⌋.
  (2) If Γ ⊢𝐹 𝑥 : 𝜏, then 𝑥 :𝜏 ∈ Γ.
  (3) If Γ ⊢𝐹 𝑒 𝑒𝑥 : 𝜏, then there is some type 𝜏𝑥 such that Γ ⊢𝐹 𝑒 : 𝜏𝑥 → 𝜏 and Γ ⊢𝐹 𝑒𝑥 : 𝜏𝑥 .
  (4) If Γ ⊢𝐹 𝜆𝑥 .𝑒 : 𝜏,then 𝜏 = 𝜏𝑥 → 𝜏 ′ and 𝑦 :𝜏𝑥 , Γ ⊢𝐹 𝑒 [𝑦/𝑥] : 𝜏 ′ for any 𝑦 ∉ Γ and well-formed 𝜏𝑥 .
  (5) If Γ ⊢𝐹 𝑒 [𝑡] : 𝜏, then there is some type 𝜎 and kind 𝑘 such that Γ ⊢𝐹 𝑒 : ∀ 𝛼 :𝑘. 𝜎 and 𝜏 =
      𝜎 [⌊𝑡⌋/𝛼].

                                                                      , Vol. 1, No. 1, Article . Publication date: July 2022.
16                                                                  Michael Borkowski, Niki Vazou, and Ranjit Jhala


     (6) If Γ ⊢𝐹 Λ𝛼 :𝑘.𝑒 : 𝜏, then there is some type 𝜏 ′ and kind 𝑘 such that 𝜏 = ∀ 𝛼 :𝑘. 𝜏 ′ and 𝛼 ′ :𝑘, Γ ⊢𝐹
         𝑒 [𝛼 ′ /𝛼] : 𝜏 ′ [𝛼 ′ /𝛼] for some 𝛼 ′ ∉ Γ.
     (7) If Γ ⊢𝐹 let 𝑥 = 𝑒𝑥 in 𝑒 : 𝜏, then there is some type 𝜏𝑥 and 𝑦 ∉ Γ such that Γ ⊢𝐹 𝑒𝑥 : 𝜏𝑥 and
         𝑦 :𝜏𝑥 , Γ ⊢𝐹 𝑒 [𝑦/𝑥] : 𝜏.
     (8) If Γ ⊢𝐹 𝑒 : 𝑡 : 𝜏, then 𝜏 = ⌊𝑡⌋ and Γ ⊢𝐹 𝑒 : 𝜏.
     Lemma 5.5. (Primitives) For each built-in primitive 𝑐,
     (1) If ⌊ty(𝑐)⌋ = 𝜏𝑥 → 𝜏 and ∅ ⊢𝐹 𝑣 𝑥 : 𝜏𝑥 , then ∅ ⊢𝐹 𝛿 (𝑐, 𝑣 𝑥 ) : 𝜏.
     (2) If ⌊ty(𝑐)⌋ = ∀ 𝛼 :𝑘. 𝜏 and ∅ ⊢𝑤 𝜏𝛼 : 𝑘, then ∅ ⊢𝐹 𝛿𝑇 (𝑐, 𝜏𝛼 ) : 𝜏 [𝜏𝛼 /𝛼].
  Lemmas 5.3 and 5.4 are proved without induction by inspection of the derivation tree, while
lemma 5.5 relies on the Primitives Requirement 1.

5.2     Preservation
The preservation lemma states that 𝜆𝐹 typing is preserved by evaluation.
     Lemma 5.6. (Preservation) If ∅ ⊢𝐹 𝑒 : 𝜏 and 𝑒 ↩→ 𝑒 ′ , then ∅ ⊢𝐹 𝑒 ′ : 𝜏.
   The proof is by structural induction on the derivation of the typing judgment. We use the de-
terminism of the operational semantics (Lemma 3.1) and the canonical forms lemma to case split
on 𝑒 to determine 𝑒 ′ . The interesting cases are for T-App and T-TApp. For applications of prim-
itives, preservation requires the Primitives Lemma 5.5, while the general case needs a Substitu-
tion Lemma A.7.
Substitution Lemma To prove type preservation when a lambda or type abstraction is applied,
we proved that the substituted result has the same type, as established by the substitution lemma:
     Lemma 5.7. (Substitution) If Γ ⊢𝐹 𝑣 𝑥 : 𝜏𝑥 and Γ ⊢𝑤 ⌊𝑡𝛼 ⌋ : 𝑘𝛼 , then
     (1) if Γ′, 𝑥 :𝜏𝑥 , Γ ⊢𝐹 𝑒 : 𝜏 and ⊢𝑤 Γ, then Γ′, Γ ⊢𝐹 𝑒 [𝑣 𝑥 /𝑥] : 𝜏.
     (2) if Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 : 𝜏 and ⊢𝑤 Γ, then Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 [𝑡𝛼 /𝛼] : 𝜏 [⌊𝑡𝛼 ⌋/𝛼].
  The proof goes by induction on the derivation tree. Because we encoded our typing rules using
coﬁnite quantiﬁcation (§ 4) the proof does not require a renaming lemma, but the rules that lookup
environments (rules T-Var and WF-Var) do need a lemma the below Weakening Lemma 5.8.
     Lemma 5.8. (Weakening Environments) If Γ1, Γ2 ⊢𝐹 𝑒 : 𝜏 and 𝑥, 𝛼 ∉ Γ1, Γ2 , then
     (1) Γ1 , 𝑥 :𝜏𝑥 , Γ2 ⊢𝐹 𝑒 : 𝜏 and (2) Γ1 , 𝛼 :𝑘, Γ2 ⊢𝐹 𝑒 : 𝜏.

6 𝜆𝑅𝐹 SOUNDNESS
We proceed to the metatheory of 𝜆𝑅𝐹 by ﬂeshing out the skeleton of light grey lemmas in Fig. 1
(which have similar statements to the 𝜆𝐹 versions) and describing the three regions (§ 2.3) needed
to establish the properties of inversion, substitution, and narrowing.
Type Safety The top-level type safety theorem, like 𝜆𝐹 , combines progress and preservation
     Theorem 6.1. (Type Safety) If ∅ ⊢ 𝑒 : 𝑡 and 𝑒 ↩→∗ 𝑒 ′ , then 𝑒 ′ is a value or 𝑒 ′ ↩→ 𝑒 ′′ for some 𝑒 ′′ .
     Lemma 6.2. (Progress) If ∅ ⊢ 𝑒 : 𝑡, then 𝑒 is a value or 𝑒 ↩→ 𝑒 ′ for some 𝑒 ′ .
     Lemma 6.3. (Preservation) If ∅ ⊢ 𝑒 : 𝑡 and 𝑒 ↩→ 𝑒 ′ , then ∅ ⊢ 𝑒 ′ : 𝑡.
     Next, let’s see the three main ways in which the proof of Lemma 6.2 diﬀers from 𝜆𝐹 .

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                              17


6.1 Inversion of Typing Judgments
The vertical lined region of Fig. 1 accounts for the fact that, due to subtyping chains, the typing
judgment in 𝜆𝑅𝐹 is not syntax-directed. First, we establish that subtyping is transitive
  Lemma 6.4. (Transitivity) If Γ ⊢𝑤 𝑡 1 :𝑘 1 , Γ ⊢𝑤 𝑡 3 :𝑘 3 , ⊢𝑤 Γ, Γ ⊢ 𝑡 1  𝑡 2 , Γ ⊢ 𝑡 2  𝑡 3 , then Γ ⊢ 𝑡 1  𝑡 3 .
   The proof consists of a case-split on the possible rules for Γ ⊢ 𝑡 1  𝑡 2 and Γ ⊢ 𝑡 2  𝑡 3 .
When the last rule used in the former is S-Witn and the latter is S-Bind, we require the Substitu-
tion Lemma 6.6. As Aydemir et al. [2005], we use the Narrowing Lemma 6.8 for the transitivity for
function types.
Inverting Typing Judgments We use the transitivity of subtyping to prove some non-trivial
lemmas that let us “invert” the typing judgments to recover information about the underlying
terms and types. We describe the non-trivial case which pertains to type and value abstractions:
  Lemma 6.5. (Inversion of T-Abs, T-TAbs)
  (1) If Γ ⊢ (𝜆𝑤 .𝑒) : 𝑥 :𝑡𝑥 → 𝑡 and ⊢𝑤 Γ, then for all 𝑦 ∉ Γ we have 𝑦 :𝑡𝑥 , Γ ⊢ 𝑒 [𝑦/𝑤] : 𝑡 [𝑦/𝑥].
  (2) If Γ ⊢ (Λ𝛼 1 :𝑘 1 .𝑒) : ∀ 𝛼 :𝑘. 𝑡 and ⊢𝑤 Γ, then for every 𝛼 ′ ∉ Γ we have 𝛼 ′ :𝑘, Γ ⊢ 𝑒 [𝛼 ′ /𝛼 1 ] :
      𝑡 [𝛼 ′ /𝛼].
   If Γ ⊢ (𝜆𝑤 .𝑒) : 𝑥 :𝑡𝑥 → 𝑡, then we cannot directly invert the typing judgment to get a typing for
the body 𝑒 of 𝜆𝑤 .𝑒. Perhaps the last rule used was T-Sub, and inversion only tells us that there
exists a type 𝑡 1 such that Γ ⊢ (𝜆𝑤 .𝑒) : 𝑡 1 and Γ ⊢ 𝑡 1  𝑥 :𝑡𝑥 → 𝑡. Inverting again, we may in
fact ﬁnd a chain of types 𝑡𝑖+1  𝑡𝑖  · · ·  𝑡 2  𝑡 1 which can be arbitrarily long. But the proof
tree must be ﬁnite so eventually we ﬁnd a type 𝑤 :𝑠 𝑤 → 𝑠 such that Γ ⊢ (𝜆𝑤 .𝑒) : 𝑤 :𝑠 𝑤 → 𝑠 and
Γ ⊢ 𝑤 :𝑠 𝑤 → 𝑠  𝑥 :𝑡𝑥 → 𝑡 (by transitivity) and the last rule was T-Abs. Then inversion gives us
that for any 𝑦 ∉ Γ we have 𝑦 :𝑠 𝑤 , Γ ⊢ 𝑒 : 𝑠 [𝑦/𝑤]. To get the desired typing judgment, we must
use the Narrowing Lemma 6.8 to obtain 𝑦 :𝑡𝑥 , Γ ⊢ 𝑒 : 𝑠 [𝑦/𝑤]. Finally, we use T-Sub to derive
𝑦 :𝑡𝑥 , Γ ⊢ 𝑒 : 𝑡 [𝑦/𝑤].

6.2 Substitution Lemma
The main result in the diagonal lined region of Fig. 1 is the Substitution Lemma. The biggest dif-
ference between the 𝜆𝐹 and 𝜆𝑅𝐹 metatheories is the introduction of a mutual dependency between
the lemmas for typing and subtyping judgments. Due to this dependency, the substitution lemma,
and the weakening lemma on which it depends must now be proven in a mutually recursive form
for both typing and subtyping judgments:
  Lemma 6.6. (Substitution)
   • If Γ1 , 𝑥 :𝑡𝑥 , Γ2 ⊢ 𝑠  𝑡, ⊢𝑤 Γ2 , and Γ2 ⊢ 𝑣 𝑥 : 𝑡𝑥 , then Γ1 [𝑣 𝑥 /𝑥], Γ2 ⊢ 𝑠 [𝑣 𝑥 /𝑥]  𝑡 [𝑣 𝑥 /𝑥].
   • If Γ1 , 𝑥 :𝑡𝑥 , Γ2 ⊢ 𝑒 : 𝑡, ⊢𝑤 Γ2 , and Γ2 ⊢ 𝑣 𝑥 : 𝑡𝑥 , then Γ1 [𝑣 𝑥 /𝑥], Γ2 ⊢ 𝑒 [𝑣 𝑥 /𝑥] : 𝑡 [𝑣 𝑥 /𝑥].
   • If Γ1 , 𝛼 :𝑘, Γ2 ⊢ 𝑠  𝑡, ⊢𝑤 Γ2 , and Γ2 ⊢𝑤 𝑡𝛼 : 𝑘, then Γ1 [𝑡𝛼 /𝛼], Γ2 ⊢ 𝑠 [𝑡𝛼 /𝛼]  𝑡 [𝑡𝛼 /𝛼].
   • If Γ1 , 𝛼 :𝑘, Γ2 ⊢ 𝑒 : 𝑡, ⊢𝑤 Γ2 , and Γ2 ⊢𝑤 𝑡𝛼 : 𝑘, then Γ1 [𝑡𝛼 /𝛼], Γ2 ⊢ 𝑒 [𝑡𝛼 /𝛼] : 𝑡 [𝑡𝛼 /𝛼].
   The main diﬃculty arises in substituting some type 𝑡𝛼 for variable 𝛼 in Γ1 , 𝛼 :𝑘, Γ2 ⊢ 𝛼 {𝑥 1 : 𝑝 } 
𝛼 {𝑥 2 : 𝑞} because we must deal with strengthening 𝑡𝛼 by the reﬁnements 𝑝 and 𝑞 respectively. As
with the 𝜆𝐹 metatheory, the proof of the substitution lemma does not require renaming, but does
require a lemmas that let us weaken environments (Lemma 6.7) in typing and subtyping judgments.
  Lemma 6.7. (Weakening Environments) If 𝑥, 𝛼 ∉ Γ1 , Γ2 , then
  (1) if Γ1 , Γ2 ⊢ 𝑒 : 𝑡 then Γ1 , 𝑥 :𝑡𝑥 , Γ2 ⊢ 𝑒 : 𝑡 and Γ1 , 𝛼 :𝑘, Γ2 ⊢ 𝑒 : 𝑡.
  (2) if Γ1 , Γ2 ⊢ 𝑠  𝑡 then Γ1 , 𝑥 :𝑡𝑥 , Γ2 ⊢ 𝑠  𝑡 and Γ1, 𝛼 :𝑘, Γ2 ⊢ 𝑠  𝑡.
  The proof is by mutual induction on the derivation of the typing and subtyping judgments.

                                                                      , Vol. 1, No. 1, Article . Publication date: July 2022.
18                                                                    Michael Borkowski, Niki Vazou, and Ranjit Jhala


6.3 Narrowing
The narrowing lemma says that whenever we have a judgment where a binding 𝑥 :𝑡𝑥 appears in the
binding environment, we can replace 𝑡𝑥 by any subtype 𝑠𝑥 . The intuition here is that the judgment
holds under the replacement because we are making the context more speciﬁc.
     Lemma 6.8. (Narrowing) If Γ2 ⊢ 𝑠𝑥 <: 𝑡𝑥 , Γ2 ⊢𝑤 𝑠𝑥 : 𝑘𝑥 , and ⊢𝑤 Γ2 then
     (1) if Γ1 , 𝑥 :𝑡𝑥 Γ2 ⊢𝑤 𝑡 : 𝑘, then Γ1, 𝑥 :𝑠𝑥 , Γ2 ⊢𝑤 𝑡 : 𝑘.
     (2) if Γ1 , 𝑥 :𝑡𝑥 , Γ2 ⊢ 𝑡 1 <: 𝑡 2 , then Γ1 , 𝑥 :𝑠𝑥 , Γ2 ⊢ 𝑡 1 <: 𝑡 2 .
     (3) if Γ1 , 𝑥 :𝑡𝑥 , Γ2 ⊢ 𝑒 : 𝑡, then Γ1 , 𝑥 :𝑠𝑥 , Γ2 ⊢ 𝑒 : 𝑡.
   The narrowing proof requires an Exact Typing Lemma 6.9 which says that a subtyping judgment
Γ ⊢ 𝑠  𝑡 is preserved after selﬁﬁcation on both types. Similarly whenever we can type a value 𝑣
at type 𝑡 then we also type 𝑣 at the type 𝑡 selﬁﬁed by 𝑣.
     Lemma 6.9. (Exact Typing)
     (1) If Γ ⊢ 𝑒 : 𝑡, ⊢𝑤 Γ, Γ ⊢𝑤 𝑡 : 𝑘, and Γ ⊢ 𝑠  𝑡, then Γ ⊢ self (𝑠, 𝑣, 𝑘)  self (𝑡, 𝑣, 𝑘).
     (2) If Γ ⊢ 𝑣 : 𝑡, ⊢𝑤 Γ, and Γ ⊢𝑤 𝑡 : 𝑘, then Γ ⊢ 𝑣 : self (𝑡, 𝑣, 𝑘).

7 REFINED DATA PROPOSITIONS
In § 8 we will present how type soundness 𝜆𝑅𝐹 is encoded in LiqidHaskell. Here we present
reﬁned data propositions, a novel feature of LiqidHaskell that made such a meta-theoretic devel-
opment possible. Intuitively, reﬁned data propositions encode Coq-style inductive predicates to
permit constructive reasoning about potentially non-terminating properties, as required for meta-
theoretic developments. (Parker et al. [2019] developed a meta-theoretic proof in LiqidHaskell
without reﬁned data propositions, but assumed a terminating evaluation relation; see § 9.)
   Reﬁned data propositions encode inductive predicates in LiqidHaskell by reﬁning Haskell’s
data types, allowing the programmer to write plain Haskell functions to provide constructive
proofs for user-deﬁned propositions. Here, for exposition, we present the four steps we followed in
the mechanization of 𝜆𝑅𝐹 to deﬁne the “hastype” proposition and then use it to type the primitive
one.
Step 1: Reifying Propositions as Data Our ﬁrst step is to represent the diﬀerent propositions of
interest as plain Haskell data. For example, we can deﬁne the following types (with the suﬃx Pr
for “proposition”):
        data HasTyPr            = HasTy            Env    Expr Type
        data IsSubTyPr = IsSubTy                   Env    Type Type
Thus, HasTy 𝛾 e t and IsSubTy 𝛾 t t' respectively represent the propositions that e can be
typed as t under environment 𝛾 and that t is a subtype of t' under 𝛾.
Step 2: Reifying Evidence as Data Next, we reify evidence, i.e. derivation trees, also as data by
deﬁning Haskell data types with a single constructor per derivation rule. For example, we deﬁne the
Haskell data type HasTyEv to encode the typing rules of Fig. 7, using a single constructor, whose
name matches the corresponding rule:
     data HasTyEv where
        TPrim :: Env → Prim → HasTyEv
        TSub     :: Env → Expr → Type → Type → HasTyEv → IsSubTyEv → HasTyEv
        ...
Using these data one can construct derivation trees. For instance, TPrim Empty (PInt 1)::
HasTyEv is the tree that types the primitive one under the empty environment.

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                      19


Step 3: Relating Evidence to its Propositions Next, we specify the relationship between the
evidence and the proposition that it establishes, via a reﬁnement-level uninterpreted function that
maps evidence to its proposition:
     measure hasTyEvPr           :: HasTyEv → HasTyPr
     measure isSubTyEvPr :: IsSubTyEv → IsSubTyPr
The above signatures declare that hasTyEvPr (resp. isSubTyEvPr ) is a reﬁnement-level function
that maps has-type (resp. is-subtype) evidence to its corresponding proposition. We can now use
these uninterpreted functions to deﬁne type aliases that denote well-formed evidence that estab-
lishes a proposition. For example, consider the (reﬁned) type aliases
  type HasTy        𝛾 e t      = {ev:HasTyEv        | hasTyEvPr ev == HasTyPr 𝛾 e t }
  type IsSubTy 𝛾 t t' = {ev:IsSubTyEv | isSubTyEvPr ev == IsSubTyPr 𝛾 t t' }
The deﬁnition stipulates that the type HasTy 𝛾 e t is inhabited by evidence (of type HasTyEv )
that establishes the typing proposition HasTyPr 𝛾 e t. Similarly IsSubTy 𝛾 t t' is inhabited
by evidence (of type IsSubTyEv ) that establishes the sub-typing proposition IsSubTyPr 𝛾 t t'.
Note that the ﬁrst three steps have only deﬁned separate data types for propositions and evidence,
and speciﬁed the relationship between them via uninterpreted functions in the reﬁnement logic.
Step 4: Reﬁning Evidence to Establish Propositions Our ﬁnal step is to implement the relation-
ship between evidence and propositions reﬁning the types of the evidence data constructors (rules)
with input types (pre-conditions) that require the rules’ premises hold, and output types (post-
conditions) that ensure the rules’ conclusions. For example, we connect the evidence and proposi-
tion for the typing relation by reﬁning the data constructors for HasTyEv using the premises and
conclusions of their respecting typing rule from Fig. 7.
  data HasTyEv where
     TPrim :: 𝛾 :Env → c:Prim →
                 HasTy 𝛾 (Prim c) (ty c)
     TSub :: 𝛾 :Env → e:Expr → t:Type → t':Type →
                HasTy 𝛾 e t → IsSubTy 𝛾 t t' →
                HasTy 𝛾 e t'
     ...
The constructors TPrim and TSub respectively encode the rules T-Prim and T-Sub rules (with
the latter being simpliﬁed here to elide the well-formedness of t'). The reﬁnements on the input
types, which encode the premises of the rules, are checked whenever these constructors are used.
The reﬁnement on the output type (being evidence of a speciﬁc proposition) is axiomatized to
encode the conclusion of the rules. Consider the type for TSub. The ﬁrst line says “for all 𝛾, 𝑒, 𝑡, 𝑡 ′ ”,
the second line (premise) says, “given evidence that 𝛾 ⊢ 𝑒 : 𝑡 and 𝛾 ⊢ 𝑡  𝑡 ′ ”, and the last line
(conclusion) says the constructor returns “evidence that 𝛾 ⊢ 𝑒 : 𝑡 ′ ”.
Programs as Constructive Proofs Thus, the constructor reﬁnements crucially ensure that only
well-formed pieces of evidence can be constructed, and simultaneously, precisely track the propo-
sition established by the evidence. This lets the programmer write plain Haskell terms as con-
structive proofs, and LiqidHaskell ensures that those terms indeed establish the proposition
stipulated by their type. For example, the below Haskell term is proof that the literal 1 has the
type Int{𝜈 : 𝜈 = 1}
  oneTy :: HasTy Empty (EPrim (PInt 1)) {v:Int | v == 1}
  oneTy = TPrim Empty (PInt 1)


                                                              , Vol. 1, No. 1, Article . Publication date: July 2022.
20                                                                Michael Borkowski, Niki Vazou, and Ranjit Jhala


If instead, the programmer modiﬁed their code to oneTy = TPrim Empty (PInt 2), Liqid-
Haskell would reject the program as the modiﬁed evidence does not establish the proposition
described in the type.

8 MECHANIZATION
We have mechanized soundness of 𝜆𝑅𝐹 in LiqidHaskell. The mechanization, submitted as anony-
mous supplementary material, uses reﬁned data propositions (§ 7) to specify the static (e.g. typing,
subtyping, well-formedness) and dynamic (i.e. small-step transitions and their closure) semantics
of 𝜆𝑅𝐹 . The mechanization is simpliﬁed by SMT-automation (§ 8.1), uses a co-ﬁnite encoding for
reasoning about variables (§ 8.2), and comprises of proofs implemented as recursive functions that
constructively manipulate the evidence to establish propositions by induction (§ 8.3). Note that
while Haskell types are inhabited by diverging ⊥ values, LiqidHaskell’s totality, termination
and type checks ensure that all cases are handled, the induction (recursion) is well-founded, and
that the proofs (programs) indeed establish the given propositions (types).

8.1 SMT Solvers and Set Theory
The most tedious part in mechanization of metatheories is the establishment of invariants about
variables, for example uniqueness and freshness. LiqidHaskell oﬀers a built-in, SMT automated
support for the theory of sets, which simpliﬁes establishing such invariants.
Set of Free Variables Our proof mechanization deﬁnes the Haskell function fv that returns the
Set of free variable names that appear in its argument.
     measure fv
     fv :: Expr → S.Set VName
     fv (EVar x)             = S.singleton x
     fv (ELam e)             = fv e
     fv (EApp e e') = S.union (fv e) (fv e')
     ... -- other cases
In the above (incomplete) deﬁnition, S is used to qualify the standard Data.Set Haskell library.
LiqidHaskell embeds the functions of Data.Set to SMT set operators (encoded as a map to
booleans). For example, S.union is treated as the logical set union operator ∪. Further, we lift fv
into the reﬁnement logic using the measure fv annotation. The measure deﬁnition deﬁnes the
logical function fv in the logic in a way that lets the SMT solver reason about the semantics of fv
in a decidable fashion, as an uninterpreted function reﬁning the type of each Expr data constructor
[Jhala and Vazou 2021]. This embedding, combined with the SMT solver’s support for the theory
of sets, lets LiqidHaskell prove properties about expressions’ free variables “for free”.
Intrinsic Veriﬁcation For example, consider the function subFV x vx e which substitutes the
free variable x with vx in e. The reﬁnement type of subFV describes the free variables of the result.
   subFV :: x:VName → vx:{Expr | isVal vx } → e:Expr
            → {e':Expr | fv e' ⊆ (fv vx ∪ (fv e \ x)) && (isVal e ⇒ isVal e')}
     subFV x vx (EVar y)                  = if x == y then vx else EVar y
     subFV x vx (ELam              e)     = ELam (subFV x vx e)
     subFV x vx (EApp e e') = EApp (subFV x vx e) (subFV x vx e')
     ... -- other cases
The reﬁnement type post condition speciﬁes that the free variables after substitution is a subset
of the free variables on the two argument expressions, excluding x, i.e. fv(𝑒 [𝑣 𝑥 /𝑥]) ⊆ fv(𝑒) ∪
(fv(𝑣 𝑥 ) \ {𝑥 }). This speciﬁcation is proved intrinsically, that is the deﬁnition of subFV constitutes

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                             21


the proof (no user aid is required) and, importantly, the speciﬁcation is automatically established
each time the function subFV is called. So, the user does not have to provide explicit hints to reason
about free variables of substituted expressions.
   The speciﬁcation of subFV shows another example of SMT-based proof simpliﬁcation: the Haskell
boolean function isVal is another measure that deﬁnes when an expression is a value. By doing
so, we can intrinsically prove that that value property is preserved by substitution, as stated by
the second (implication) conjunct in the output of subFV.
Freshness LiqidHaskell’s support for sets simpliﬁes deﬁning a fresh function, which is often
challenging1 . fresh xs returns a variable that provably does not belong to its input xs.
   fresh :: xs:S.Set VName → { x:VName | x ∉ xs }
   fresh xs = n ? above_max n xs'
        where n        = 1 + maxs xs'
               xs'     = S.fromList xs


   maxs :: [VName] → VName
   maxs []           = 0
   maxs (x:xs) = if maxs xs < x then x else maxs xs


   above_max :: x:VName → xs:{[VName]|maxs xs < x} → {x ∉ elems xs}
   above_max _ []     = ()
   above_max x (_:xs) = above_max x xs
The fresh function returns n: the maximum element of the set increased by one. To compute the
maximum element we convert the set to a list and use the inductively deﬁned maxs functions. To
prove fresh ’s intrinsic speciﬁcation we use an extrinsic, i.e. explicit, lemma above_max n xs'
that, via the (?) combinator of type a → b → a, tells LiqidHaskell that n is not in the set xs.
This extrinsic lemma is itself trivially proved by induction on xs and SMT automation.

8.2 Co-finite Quantification
To encode the rules that need a fresh free variable name we use the co-ﬁnite quantiﬁcation of Aydemir et al.
[2008], as discussed in § 4. Figure 9 presents this encoding using the T-Abs rule as an example. The
standard abstraction rule (rule T-Abs-Ex in § 4) requires to provide a concrete fresh name, which is
encoded in the second line of TAbsEx as the y:{VName | y ∉ dom 𝛾 } argument. The co-ﬁnitely
quantiﬁed encoding of the rule TAbs, instead, states that there exists a speciﬁed ﬁnite set of ex-
cluded names, namely l, and requires that the sub-derivation holds for any name y that does not
belong in l. That is, the premise is turned into a function that, given the name y, returns the sub-
derivation. This encoding greatly simpliﬁes our mechanization, since the premises are no more
tied to concrete names, eliminating the need for renaming lemmas. We will often take l to be the
domain of the environment, but the ability to choose l gives us the ﬂexibility when constructing
derivations to exclude additional names that clash with another part of a proof.

8.3     Inductive Proofs as Recursive Functions
The majority of our proofs are by induction on derivations. These proofs are written as recursive
Haskell functions that operate over the reﬁned data types reifying the respective derivations. Liq-
uidHaskell ensures the proofs are valid by checking that they are inductive (i.e. the recursion is
1 For example, Coq cannot fold over a set, and so a more complex combination of tactics is required to generate a fresh

name.


                                                                     , Vol. 1, No. 1, Article . Publication date: July 2022.
22                                                                    Michael Borkowski, Niki Vazou, and Ranjit Jhala


-- Standard Existential Rule
TAbsEx       :: 𝛾 :Env → t𝑥 :Type → e:Expr → t:Type
             → y:{VName | y ∉ dom 𝛾 }
             → HasTy ((y,t𝑥 ):𝛾 ) (unbind y e) (unbindT y t)
             → HasTy 𝛾 (ELam e) (TFunc t𝑥 t)

-- Co-finitely Quantified Rule
TAbs         :: 𝛾 :Env → t𝑥 :Type → e:Expr → t:Type → l:S.Set VName
             → (y:{VName|y ∉ l} → HasTy ((y,t𝑥 ):𝛾 ) (unbind y e) (unbindT y t))
             → HasTy 𝛾 (ELam e) (TFunc t𝑥 t)

-- Note: All rules also include k𝑥 :Kind → WfType 𝛾 t𝑥 k𝑥 elided for clarity.

                                    Fig. 9. Encoding of Co-finitely Quantified Rules.


well-founded), handle all cases (i.e. the function is total) and establish the desired properties (i.e.
witnesses the appropriate proposition.)
Preservation (Theorem 6.3) relates the HasTy data proposition of § 7 with a Step data proposition
that encodes Fig. 4 and is proved by induction on the type derivation tree. The subtyping case
requires an induction while the primitive case is impossible (Lemma 3.1):
     preservation :: e:Expr → t:Type → e':Expr → HasTy Empty e t → Step e e'
                         → HasTy Empty e' t

     preservation _e _t e' (TSub Empty e t' t e_has_t' t'_sub_t) e_step_e'
       = TSub Empty e' t' t e'_has_t' t'_sub_t
             where e'_has_t' = preservation e t' e' e_has_t' e_step_e'
     preservation e _ e' (TPrim _ _) step
       = impossible "value" ? lemValStep e e' step -- 𝑒 ↩→ 𝑒 ′ ⇒ ¬( isVal 𝑒)
     preservation e _ e' (TAbs {}) step
       = impossible "value" ? lemValStep e e' step -- 𝑒 ↩→ 𝑒 ′ ⇒ ¬( isVal 𝑒)
     ...


     impossible :: {v:String | false} → a
     lemValStep :: e:Expr → e':Expr → Step e e' → {¬(isVal e)}
   In the TSub case we note that LiqidHaskell knows that the expression argument _e is equal to
the the subtyping parameter e. Further, the termination checker will ensure that the inductive call
happens on the smaller derivation subtree. The TPrim case goes by contradiction since primitives
cannot step. We separately proved that values cannot step in the lemValStep lemma, which here
is combined with the fact that e is a value to allow the call of the false-precondition impossible .
Finally, LiqidHaskell’s totality checker ensures all the cases of HasTypEv are covered, and the
termination checker ensures the proof is well-founded.
Progress (Theorem 6.2) ensures that a well-typed expression is a value or there exists an expres-
sion to which it steps. To express this claim we used Haskell’s Either to encode disjunction that
contain pairs (reﬁned to be dependent) to encode existentials.

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                 23


  progress :: e:Expr → t:Type → HasTy Empty e t
               → Either {isVal e}       (e'::Expr, Step e e')


  progress _ _ (TSub Empty e t' t e_has_t' _) = progress e t' e_has_t'
  progress _ _ (TPrim _ _)                    = Left ()
  progress _ _ (TAbs {})                                  = Left ()
  ...
The proofs of the TSub and TPrim cases are easily done by, respectively, an inductive call and
establishing is-Value. The more interesting cases require us to case-split on the inductive call in
order to get access to the existential witness.
Soundness (Theorem 6.1) ensures that a well-typed expression will not get stuck, that is, it
will either reach a value or keep evaluating. We reify evaluation sequences with a reﬁned data
proposition Steps e0 e with a reﬂexive and a transitive (recursive) constructor. Our soundness
proof goes by induction on the evaluation sequence.
  soundness :: e0 :Expr → t:Type → e:Expr → HasTy Empty e0 t → Steps e0 e
                → Either {isVal e}        (e𝑖 ::Expr, Step e e𝑖 )


  soundness _e0 t _e e0 _has_t e0 _evals_e = case e0 _evals_e of
     Refl e0 → progress e0 t e0 _has_t         -- 𝑒 0 = 𝑒
        AddStep e0 e1 e0 _step_e 1 e e1 _eval_e → -- 𝑒 0 ↩→ 𝑒 1 ↩→∗ 𝑒
          soundness e1 t e (preservation e0 t e0 _has_t e1 e0 _step_e 1 ) e1 _eval_e
The reﬂexive case is proved by progress . In the inductive case the evaluation sequence is 𝑒 0 ↩→
𝑒 1 ↩→∗ 𝑒 and the proof goes by induction, using preservation to ensure that 𝑒 1 is typed.

8.4   Mechanization Details
We provide a full, mechanically checked proof of the metatheory in § 5 and § 6. The only facts
that are assumed are the Requirements 1 and 2, resp. on built-in primitives and the implication
relation.
Representing Binders In our mechanization, we use the locally-nameless representation [Aydemir et al.
2008; Charguéraud 2012]. Free variables and bound variables are taken to be separate syntactic
objects, so we do not need to worry about alpha renaming of free variables to avoid capture in sub-
stitutions. We also use de Bruijn indices only for bound variables. This enables us to avoid taking
binder names into account in the strengthen function used to deﬁne substitution (Fig. 5).
Quantitative Results In Table 1 we give the empirical details of our metatheory, which was
checked using LiqidHaskell version 0.8.10.7.1 and a Lenovo ThinkPad T15p laptop with an Intel
Core i7-11800H processor with 8 physical cores and 32 GB of RAM. Our mechanized proof is
substantial, spanning about 9400 lines distributed over about 35 ﬁles. Currently, the whole proof
can be checked in about 30 minutes, which can make interactive development diﬃcult. While
incremental modular checking provides a modicum of interactivity, improving the ergonomics,
i.e. veriﬁcation time and providing actionable error messages, remains an important direction for
future work.

9 RELATED WORK
We discuss the most closely related work on the meta-theory of unreﬁned and reﬁned type systems.

                                                         , Vol. 1, No. 1, Article . Publication date: July 2022.
24                                                                       Michael Borkowski, Niki Vazou, and Ranjit Jhala


      Subject                            Files            Spec. (LOC)      Proof (LOC)            Time (mins)
      Deﬁnitions                             6                    1805              374                     1
      Basic Properties                       8                     646             2117                     4
      𝜆𝐹 Soundness                           4                     138              685                     3
      Weakening                              4                     379              467                     1
      Substitution                           4                     458              846                     7
      Exact Typing                           2                      70              230                     4
      Narrowing                              1                      88              166                     1
      Inversion of Typing                    1                     124              206                     1
      Primitives                             3                     120              277                     4
      𝜆𝑅𝐹 Soundness                          1                      14              181                     1
      Total                                  35                  3842                5549                      29
Table 1. Empirical details of our mechanization. We partition the development into sets of modules pertain-
ing to diﬀerent region of Fig. 1, and for each region separate the lines of specification (e.g. definitions and
lemma statements) from those needed for proofs.




Representing Binders Our development for 𝜆𝐹 (§ 5) follows the standard presentation of Sys-
tem F’s metatheory by Pierce [2002]. The main diﬀerence between the two metatheories is that
ours includes well-formedness of types and environments, which help with mechanization [Rémy
2021] and are crucial when formalizing reﬁnements. One of the main challenges in mechanization
of metatheories is the syntactic representation of variables and binders [Aydemir et al. 2005]. The
named representation has severe diﬃculties because of variable capturing substitutions and the
nameless (a.k.a. de Bruijn) requires heavy index shifting. The variable representation of 𝜆𝑅𝐹 is lo-
cally nameless representation [Aydemir et al. 2008; Pollack 1993], that is, free variables are named,
but the bound variables are represented by syntactically distinct deBruijn indices. We chose this
representation because it clearly addresses the following two problems with named bound vari-
ables but nevertheless our metatheory still resembles the paper and pencil proofs (that we per-
formed before mechanization): First, when diﬀerent reﬁnements are strengthened (as in Fig. 5) the
variable capturing problem reappears because we are substituting underneath a binder. Second,
subtyping usually permits alpha-renaming of variables, which breaks a required invariant that
each 𝜆𝑅𝐹 derivation tree is a valid 𝜆𝐹 tree after erasure.
Hybrid & Contract Systems Flanagan [2006] formalizes a monomorphic lambda calculus with
reﬁnement types that diﬀers from our 𝜆𝑅𝐹 in three ways. First, the denotational soundness method-
ology of Flanagan [2006] connects subtyping with expression evaluation. We could not follow this
approach because encoding type denotations as a data proposition requires a negative occurrence
(§ 4.4). Second, in [Flanagan 2006] type checking is hybrid: the developed system is undecidable
and inserts runtime casts when subtyping cannot be statically decided. Third, the original system
lacks polymorphism. Sekiyama et al. [2017] extended hybrid types with polymorphism, but unlike
𝜆𝑅𝐹 , their system does not support semantic subtyping. For example, consider a divide by zero-
error. The reﬁned types for div and 0 could be given by div :: Int → Int {𝑛 : 𝑛 ≠ 0} → Int and
0 :: Int {𝑛 : 𝑛 = 0}. This system will compile div 1 0 by inserting a cast on 0: hInt {𝑛 : 𝑛 = 0} ⇒
Int {𝑛 : 𝑛 ≠ 0}i, causing a deﬁnite runtime failure that could have easily been prevented statically.
Having removed semantic subtyping, the metatheory of [Sekiyama et al. 2017] is highly simpliﬁed.
Static reﬁnement type systems (as summarized by Jhala and Vazou [2021]) usually restrict the deﬁ-
nition of predicates to quantiﬁer-free ﬁrst-order formulae that can be decided by SMT solvers. This

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                  25


restriction is not preserved by evaluation that can substitute variables with any value, thus allow-
ing expressions that cannot be encoded in decidable logics, like lambdas, to seep into the predicates
of types. In contrast, we allow predicates to be any language term (including lambdas) to prove
soundness via preservation and progress: our meta-theoretical results trivially apply to systems
that, for eﬃciency of implementation, restrict their source languages. Finally, none of the above
systems (hybrid, contracts or static reﬁnement types) come with a machine checked soundness
proof.
Reﬁnement Types in Coq Our soundness formalization follows the axiomatized implication rela-
tion of Lehmann and Tanter [2016] that decides subtyping (our rule S-Base) by without formally
connecting implication and expression evaluation. Lehmann and Tanter [2016]’s Coq formaliza-
tion of a monomorphic lambda calculus with reﬁnement types diﬀers from 𝜆𝑅𝐹 in two ways. First,
their axiomatized implication allows them to arbitrarily restrict the language of reﬁnements. We
allow reﬁnements to be arbitrary program terms and intend, in the future, to connect our axioms
to SMT solvers or other oracles. Second, 𝜆𝑅𝐹 includes language features like polymorphism, exis-
tentials, and selﬁﬁcation which are critical for path- and context-sensitive reﬁnement typing, but
make the metatheory more challenging. Hamza et al. [2019] present System FR, a polymorphic, re-
ﬁned language with a mechanized metatheory of about 30K lines of Coq. Compared to our system,
their notion of subtyping is not semantic, but relies on a reducibility relation. For example, even
though System FR will deduce that Pos is a subtype of Int, it will fail to derive that Int → Pos
is subtype of Pos → Int as reduction-based subtyping cannot reason about contra-variance. Be-
cause of this more restrictive notion of subtyping, their mechanization does not require either the
indirection of denotational soundness or the use of an implication proving oracle. Further, Sys-
tem FR’s support for polymorphism is limited in that it disallows reﬁnements on type variables,
thereby precluding many practically useful speciﬁcations.
Metatheory in LiquidHaskell LWeb [Parker et al. 2019] also used LiqidHaskell to prove
metatheory, concretely non-interference of 𝜆LWeb , a core calculus that extends the LIO formalism
with database access. The LWeb proof did not use reﬁned data propositions, which were not present
at the time of its development, and thus it has two major weaknesses compared to our present de-
velopment. First, LWeb assumes termination of 𝜆LWeb ’s evaluation function; without reﬁned data
propositions metatheory can be developed only over terminating functions. This was not a criti-
cal limitation since non-interference was only proved for terminating programs. However, in our
proof the requirement that evaluation of 𝜆𝑅𝐹 terminates would be too strict. In our encoding with
reﬁned data propositions such an assumption was not required. Second, the LWeb development is
not constructive: the structure of an assumed evaluation tree is logically inspected instead of the
more natural case splitting permitted only with reﬁned data propositions. This constructive way
to develop metatheories is more compact (e.g. there is no need to logically inspect the structure of
the derivation trees) and more akin to the standard meta-theoretic developments of constructive
tools like Coq and Isabelle.

10 CONCLUSIONS & FUTURE WORK
We presented and formalized soundness of 𝜆𝑅𝐹 , a core reﬁnement calculus that combines semantic
subtyping, existential types, and parametric polymorphism, which are critical for practical reﬁne-
ment typing but whose combination has never been formalized. Our meta-theory is mechanized
in LiqidHaskell, using the novel feature of reﬁned data propositions to reify e.g. typing and eval-
uation derivations as (reﬁned) Haskell datatypes, and exploits SMT to automate various tedious
invariants about variables. We fully expect our proof can be mechanized in specialized proof sys-
tems like Agda [Norell 2007], Coq [Bertot and Castéran 2004] or Isabelle [Nipkow et al. 2002] or

                                                          , Vol. 1, No. 1, Article . Publication date: July 2022.
26                                                                     Michael Borkowski, Niki Vazou, and Ranjit Jhala


those equipped with SMT-based automation like Dafny [Leino 2010], or F* [Martínez et al. 2019].
Our goal here is not to compare against such systems. Instead, our primary contribution is to, for
the ﬁrst time, establish the soundness of the combination of features critical for practical reﬁne-
ment typing, and secondarily, show that such a proof can be mechanized as a plain program with
reﬁnement types. Looking ahead, we envision two lines of work on mechanizing metatheory of
and with reﬁnement types.
1. Mechanization of Reﬁnements 𝜆𝑅𝐹 covers a crucial but small fragment of the features of
modern reﬁnement type checkers. It would be interesting to extend the language to include fea-
tures like reﬁned datatypes, and abstract and bounded reﬁnements. Similarly, our current work
axiomatizes the requirements of the semantic implication checker (i.e. SMT solver). It would be
interesting to implement a solver and verify that it satisﬁes that contract, or alternatively, show
how proof certiﬁcates [Necula 1997] could be used in place of such axioms.
2. Mechanization with Reﬁnements While this work shows that non-trivial meta-theoretic
proofs are possible with SMT-based reﬁnement types, our experience is that much remains to make
such developments pleasant. For example, programming would be far more convenient with sup-
port for automatically splitting cases or ﬁlling in holes as done in Agda [Norell 2007] and envisioned
by Redmond et al. [2021]. Similarly, when a proof fails, the user has little choice but to think re-
ally hard about the internal proof state and what extra lemmas are needed to prove their goal.
Finally, the stately pace of veriﬁcation — 9400 lines across 35 ﬁles take about 30 minutes — hinders
interactive development. Thus, rapid incremental checking, lightweight synthesis, and actionable
error messages would go a long way towards improving the ergonomics of veriﬁcation, and hence
remain important directions for future work.

REFERENCES
Brian E. Aydemir, Aaron Bohannon, Matthew Fairbairn, J. Nathan Foster, Benjamin C. Pierce, Brian E. Aydemir, Aaron Bo-
   hannon, Matthew Fairbairn, J. Nathan Foster, Benjamin C. Pierce, Peter Sewell, Dimitrios Vytiniotis, Geoﬀrey Washburn,
   Stephanie C. Weirich, Stephan A. Zdancewic, Brian E. Aydemir, Aaron Bohannon, Matthew Fairbairn, J. Nathan Fos-
   ter, Benjamin C. Pierce, Peter Sewell, Dimitrios Vytiniotis, Stephanie Weirich, and Steve Zdancewic. 2005. Mechanized
   metatheory for the masses: The POPLmark challenge. In In TPHOLs, number 3603 in LNCS. Springer, 50–65.
Brian E. Aydemir, Arthur Charguéraud, Benjamin C. Pierce, Randy Pollack, and Stephanie Weirich. 2008. Engineering for-
   mal metatheory. In Proceedings of the 35th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
   POPL 2008, San Francisco, California, USA, January 7-12, 2008, George C. Necula and Philip Wadler (Eds.). ACM, 3–15.
   https://doi.org/10.1145/1328438.1328443
João Filipe Belo, Michael Greenberg, Atsushi Igarashi, and Benjamin C. Pierce. 2011. Polymorphic Contracts. In European
   Symposium on Programming (ESOP). https://doi.org/10.1007/978-3-642-19718-5_2
Y. Bertot and P. Castéran. 2004. Coq’Art: The Calculus of Inductive Constructions. Springer Verlag.
Arthur Charguéraud. 2012.         The Locally Nameless Representation.         J. Autom. Reason. 49, 3 (2012), 363–408.
   https://doi.org/10.1007/s10817-011-9225-2
Benjamin Cosman and Ranjit Jhala. 2017.              Local reﬁnement typing.        PACMPL 1, ICFP (2017), 26:1–26:27.
   https://doi.org/10.1145/3110270
C. Flanagan. 2006. Hybrid Type Checking. In POPL.
C. Flanagan, A. Sabry, B. F. Duba, and M. Felleisen. 1993. The Essence of Compiling with Continuations.. In PLDI.
C. Fournet, M. Kohlweiss, and P-Y. Strub. 2011. Modular code-based cryptographic veriﬁcation. In CCS.
Andrew D. Gordon and C. Fournet. 2010. Principles and Applications of Reﬁnement Types. In Logics and Languages for
   Reliability and Security. IOS Press. https://doi.org/10.3233/978-1-60750-100-8-73
Jad Hamza, Nicolas Voirol, and Viktor Kuncak. 2019. System FR: formalized foundations for the stainless veriﬁer. Proc.
   ACM Program. Lang. 3, OOPSLA (2019), 166:1–166:30. https://doi.org/10.1145/3360592
Ranjit Jhala and Niki Vazou. 2021. Reﬁnement Types: A Tutorial. Found. Trends Program. Lang. 6, 3-4 (2021), 159–317.
   https://doi.org/10.1561/2500000032
Milod Kazerounian, Niki Vazou, Austin Bourgerie, Jeﬀrey S. Foster, and Emina Torlak. 2017. Reﬁnement Types for Ruby.
   CoRR abs/1711.09281 (2017). arXiv:1711.09281 http://arxiv.org/abs/1711.09281
A. M. Kent, D. Kempe, and S. Tobin-Hochstadt. 2016. Occurrence typing modulo theories. In PLDI.


, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                             27


Tristan Knoth, Di Wang, Adam Reynolds, Jan Hoﬀmann, and Nadia Polikarpova. 2020. Liquid resource types. Proc. ACM
   Program. Lang. 4, ICFP (2020), 106:1–106:29. https://doi.org/10.1145/3408988
Kenneth Knowles and Cormac Flanagan. 2009a. Compositional Reasoning and Decidable Checking for Dependent Contract
   Types. In Proceedings of the 3rd Workshop on Programming Languages Meets Program Veriﬁcation (Savannah, GA, USA)
   (PLPV ’09). Association for Computing Machinery, New York, NY, USA, 27–38. https://doi.org/10.1145/1481848.1481853
K. W. Knowles and C. Flanagan. 2009b. Compositional and decidable checking for dependent contract types. In PLPV.
Nico Lehmann, Rose Kunkel, Jordan Brown, Jean Yang, Niki Vazou, Nadia Polikarpova, Deian Stefan, and
   Ranjit Jhala. 2021.          STORM: Reﬁnement Types for Secure Web Applications. In 15th USENIX Sym-
   posium on Operating Systems Design and Implementation (OSDI 21). USENIX Association, 441–459.
   https://www.usenix.org/conference/osdi21/presentation/lehmann
Nico Lehmann and Éric Tanter. 2016. Formalizing Simple Reﬁnement Types in Coq. In 2nd International Workshop on Coq
   for Programming Languages (CoqPL’16). St. Petersburg, FL, USA.
K. Rustan M. Leino. 2010. Dafny: An Automatic Program Veriﬁer for Functional Correctness. In Logic for Programming,
   Artiﬁcial Intelligence, and Reasoning (LPAR). https://doi.org/10.1007/978-3-642-17511-4_20
Guido Martínez, Danel Ahman, Victor Dumitrescu, Nick Giannarakis, Chris Hawblitzel, Catalin Hritcu, Monal
   Narasimhamurthy, Zoe Paraskevopoulou, Clément Pit-Claudel, Jonathan Protzenko, Tahina Ramananandro, Aseem Ras-
   togi, and Nikhil Swamy. 2019. Meta-F*: Proof Automation with SMT, Tactics, and Metaprograms. In European Sympo-
   sium on Programming (ESOP). https://doi.org/10.1007/978-3-030-17184-1_2
George C. Necula. 1997. Proof carrying code. In POPL 97: Principles of Programming Languages. ACM, 106–119.
T. Nipkow, L.C. Paulson, and M. Wenzel. 2002. Isabelle/HOL — A Proof Assistant for Higher-Order Logic.
U. Norell. 2007. Towards a practical programming language based on dependent type theory. Ph.D. Dissertation. Chalmers.
X. Ou, G. Tan, Y. Mandelbaum, and D. Walker. 2004. Dynamic Typing with Dependent Types. In IFIP TCS.
James Parker, Niki Vazou, and Michael Hicks. 2019. LWeb: information ﬂow security for multi-tier web applications. Proc.
   ACM Program. Lang. 3, POPL (2019), 75:1–75:30. https://doi.org/10.1145/3290388
Benjamin C. Pierce. 2002. Types and Programming Languages. MIT Press.
Randy Pollack. 1993. Closure Under Alpha-Conversion. In Types for Proofs and Programs, International Workshop TYPES’93,
   Nijmegen, The Netherlands, May 24-28, 1993, Selected Papers (Lecture Notes in Computer Science), Henk Barendregt and
   Tobias Nipkow (Eds.), Vol. 806. Springer, 313–332. https://doi.org/10.1007/3-540-58085-9_82
Patrick Redmond, Gan Shen, and Lindsey Kuper. 2021. Toward Hole-Driven Development with Liquid Haskell. CoRR
   abs/2110.04461 (2021). arXiv:2110.04461 https://arxiv.org/abs/2110.04461
Didier Rémy. 2021. Type systems for programming languages. Course notes.
Taro Sekiyama, Atsushi Igarashi, and Michael Greenberg. 2017. Polymorphic Manifest Contracts, Revised and Resolved.
   ACM Trans. Program. Lang. Syst. 39, 1 (2017), 3:1–3:36. https://doi.org/10.1145/2994594
Nikhil Swamy, Cătălin Hriţcu, Chantal Keller, Aseem Rastogi, Antoine Delignat-Lavaud, Simon Forest, Karthikeyan
   Bhargavan, Cédric Fournet, Pierre-Yves Strub, Markulf Kohlweiss, Jean-Karim Zinzindohoue, and Santiago Zanella-
   Béguelin. 2016. Dependent Types and Multi-Monadic Eﬀects in F*. In Principles of Programming Languages (POPL).
   https://doi.org/10.1145/2837614.2837655
Sam Tobin-Hochstadt and Matthias Felleisen. 2008. The design and implementation of typed scheme. In POPL.
Niki Vazou, Eric L. Seidel, and Ranjit Jhala. 2014a. LiquidHaskell: Experience with Reﬁnement Types in the Real World.
   In Proceedings of the 2014 ACM SIGPLAN Symposium on Haskell (Gothenburg, Sweden) (Haskell ’14). Association for
   Computing Machinery, New York, NY, USA, 39–51. https://doi.org/10.1145/2633357.2633366
N. Vazou, E. L. Seidel, R. Jhala, D. Vytiniotis, and S. L. Peyton-Jones. 2014b. Reﬁnement Types for Haskell. In ICFP.
Niki Vazou, Anish Tondwalkar, Vikraman Choudhury, Ryan G. Scott, Ryan R. Newton, Philip Wadler, and Ranjit Jhala.
   2018. Reﬁnement reﬂection: complete veriﬁcation with SMT. Proc. ACM Program. Lang. 2, POPL (2018), 53:1–53:31.
   https://doi.org/10.1145/3158141
Philip Wadler. 1989. Theorems for Free!. In Proceedings of the Fourth International Conference on Functional Programming
   Languages and Computer Architecture (Imperial College, London, United Kingdom) (FPCA ’89). Association for Comput-
   ing Machinery, New York, NY, USA, 347–359. https://doi.org/10.1145/99370.99404

A PROOFS OF 𝜆𝐹 SOUNDNESS
In this appendix, we present the proofs for each lemma of our 𝜆𝐹 metatheory presented in § 5.
   Theorem A.1. (Type Safety) If ∅ ⊢𝐹 𝑒 : 𝜏 and 𝑒 ↩→∗ 𝑒 ′ , then 𝑒 ′ is a value or 𝑒 ′ ↩→ 𝑒 ′′ for some 𝑒 ′′ .
   Proof. We proceed by induction on the number of steps in 𝑒 ↩→∗ 𝑒 ′ . There are two cases for
𝑒 ↩→∗ 𝑒 ′ : either 𝑒 = 𝑒 ′ or there exists a term 𝑒 1 such that 𝑒 ↩→ 𝑒 1 ↩→∗ 𝑒 ′ . In the former case we
conclude immediately by the Progress Lemma. In the latter case, ∅ ⊢𝐹 𝑒 1 : 𝜏 by the Preservation

                                                                     , Vol. 1, No. 1, Article . Publication date: July 2022.
28                                                                  Michael Borkowski, Niki Vazou, and Ranjit Jhala


Lemma. Then by the inductive hypothesis applied to 𝑒 1 , we conclude that either 𝑒 ′ is a value or
𝑒 ′ ↩→ 𝑒 ′′ for some 𝑒 ′′ .                                                                     

A.1 Progress
  Lemma A.2. (Progress) If ∅ ⊢𝐹 𝑒 : 𝜏 then 𝑒 is a value or 𝑒 ↩→ 𝑒 ′ for some 𝑒 ′ .
  Proof. We proceed by induction of the structure of ∅ ⊢𝐹 𝑒 : 𝜏. In the cases of rule T-Prim,
T-Var, T-Abs, or T-TAbs, 𝑒 is a value.
Case T-App: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 𝑒 2 . Inverting, we have that there exists some
     type 𝜏2 such that ∅ ⊢𝐹 𝑒 1 : 𝜏2 → 𝜏 and ∅ ⊢𝐹 𝑒 2 : 𝜏2 . We split on ﬁve possible cases for the
     structure of 𝑒 1 and 𝑒 2 . First, suppose 𝑒 1 ≡ 𝜆𝑥 .𝑒 0 and 𝑒 2 is a value. Then by rule E-AppAbs,
     𝑒 ≡ 𝜆𝑥 .𝑒 0 𝑒 2 ↩→ 𝑒 0 [𝑒 2 /𝑥]. Second, suppose 𝑒 1 ≡ 𝜆𝑥 .𝑒 0 and 𝑒 2 is not a value. Then by the
     inductive hypothesis, there exists a term 𝑒 2′ such that 𝑒 2 ↩→ 𝑒 2′ . Then by rule E-App2 𝑒 ≡
     𝜆𝑥 .𝑒 0 𝑒 2 ↩→ 𝜆𝑥 .𝑒 0 𝑒 2′ . Third, suppose 𝑒 1 ≡ 𝑐, a built in primitive and 𝑒 2 is a value. Then by
     rule E-Prim, 𝑒 ≡ 𝑐 𝑒 2 ↩→ 𝛿 (𝑐, 𝑒 2 ), which is well-deﬁned by the primitives lemma. Fourth,
     suppose 𝑒 1 ≡ 𝑐 and 𝑒 2 is not a value. Then by the inductive hypothesis, there exists a term
     𝑒 2′ such that 𝑒 2 ↩→ 𝑒 2′ . Then by rule E-App2 𝑒 ≡ 𝑐 𝑒 2 ↩→ 𝑐 𝑒 2′ . Finally, by the canonical
     forms lemma, 𝑒 1 cannot be any other value, so it must not be a value. Then by the inductive
     hypothesis, there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ . Then by rule E-App1, 𝑒 ≡ 𝑒 1 𝑒 2 ↩→ 𝑒 1′ 𝑒 2 .
Case T-TApp: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 [𝑡] and 𝜏 ≡ 𝜎 [⌊𝑡⌋/𝛼]. Inverting, we have that
     ∅ ⊢𝐹 𝑒 1 : ∀ 𝛼 :𝑘. 𝜎. We split on three cases for the structure of 𝑒 1 . First, suppose 𝑒 1 ≡ Λ𝛼 ′ :𝑘 ′ .𝑒 0 .
     Then by rule E-AppTAbs, 𝑒 ≡ Λ𝛼 ′ :𝑘 ′ .𝑒 0 [𝑡] ↩→ 𝑒 0 [𝑡/𝛼 ′ ]. Second, suppose 𝑒 1 ≡ 𝑐, a built
     in primitive. Then by rule E-PrimT, 𝑒 ≡ 𝑐 [𝑡] ↩→ 𝛿𝑇 (𝑐, ⌊𝑡⌋), which is well-deﬁned by the
     primitives lemma. Finally, by the canonical forms lemma, 𝑠𝑒𝑥𝑝𝑟 1 cannot be any other form
     of value, so it must not be a value. Then by the inductive hypothesis, there is a term 𝑒 1′ such
     that 𝑒 1 ↩→ 𝑒 1′ . Then by rule E-AppT 𝑒 ≡ 𝑒 1 [𝑡] ↩→ 𝑒 1′ [𝑡].
Case T-Let: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ let 𝑥 = 𝑒 1 in 𝑒 2 . Inverting, we have that ∅ ⊢𝐹 𝑒 1 : 𝜏1
     for some type 𝜏1 . By the inductive hypothesis, either 𝑒 1 is a value or there is a term 𝑒 1′ such
     that 𝑒 1 ↩→ 𝑒 1′ . In the former case, rule E-LetV gives us 𝑒 ≡ let 𝑥 = 𝑒 1 in 𝑒 2 ↩→ 𝑒 2 [𝑒 1 /𝑥]. In
     the latter case, by rule E-Let, 𝑒 ≡ let 𝑥 = 𝑒 1 in 𝑒 2 ↩→ let 𝑥 = 𝑒 1′ in 𝑒 2 .
Case T-Ann: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 : 𝑡. Inverting, we have the ∅ ⊢𝐹 𝑒 1 : 𝜏 and 𝜏 = ⌊𝑡⌋.
     By the inductive hypothesis, either 𝑒 1 is a value or there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ . In
     the former case, by rule E-AnnV, 𝑒 ≡ 𝑒 1 : 𝑡 ↩→ 𝑒 1 . In the latter case, rule E-Ann gives us
     𝑒 ≡ 𝑒 1 : 𝑡𝑠𝑡𝑒𝑝𝑒 1′ : 𝑡.
                                                                                                               
   The progress proof is substantially the same for 𝜆𝑅𝐹 . The only diﬀerence is that there is another
straightforward inductive case for rule T-Sub.
     Lemma A.3. (𝜆𝐹 Canonical Forms)
     (1) If ∅ ⊢𝐹 𝑣 : Bool then 𝑣 = true or 𝑣 = false.
     (2) If ∅ ⊢𝐹 𝑣 : Int then 𝑣 is an integer constant.
     (3) If ∅ ⊢𝐹 𝑣 : 𝜏 → 𝜏 ′ then either 𝑣 = 𝜆𝑥 .𝑒 or 𝑣 = 𝑐, a built in primitive function where 𝑐 ∈
         {∧, ∨, ¬, ↔, ≤, =}.
     (4) If ∅ ⊢𝐹 𝑣 : ∀ 𝑎:𝑘. 𝜏 then either 𝑣 = Λ𝑎:𝑘. 𝑒 or 𝑣 is the polymorphic equality =.
     (5) If ∅ ⊢𝑤 𝜏 : 𝐵 then 𝜏 = Bool or 𝜏 = Int.
   Proof. Parts (1) - (4) are easily deduced from the 𝜆𝐹 typing rules in Figure 7 and the deﬁnition
of 𝑡𝑦(𝑐). Part (5) is clear from the well-formedness rules in Figure 6.                           

, Vol. 1, No. 1, Article . Publication date: July 2022.
Mechanizing Refinement Types                                                                                        29


   Lemma A.3 is suﬃcient for our 𝜆𝑅𝐹 metatheory. Our syntactic typing judgments in 𝜆𝑅𝐹 respect
those of 𝜆𝐹 . Speciﬁcally, if Γ ⊢ 𝑒 : 𝑡 and ⊢𝑤 Γ, then ⌊Γ⌋ ⊢𝐹 𝑒 : ⌊𝑡⌋. Therefore, we do not have to
state and prove a separate Canonical Forms Lemma for 𝜆𝑅𝐹 .
  Lemma A.4. (Inversion of Typing)
  (1) If Γ ⊢𝐹 𝑐 : 𝜏 then 𝜏 = ⌊ty(𝑐)⌋.
  (2) If Γ ⊢𝐹 𝑥 : 𝜏 then 𝑥 :𝜏 ∈ Γ.
  (3) If Γ ⊢𝐹 𝑒 𝑒 ′ : 𝜏 then there is some type 𝜏𝑥 such that Γ ⊢𝐹 𝑒 : 𝜏𝑥 → 𝜏 and Γ ⊢𝐹 𝑒 ′ : 𝜏𝑥 .
  (4) If Γ ⊢𝐹 𝜆𝑥 .𝑒 : 𝜏 then 𝜏 = 𝜏𝑥 → 𝜏 ′ and 𝑦 :𝜏𝑥 , Γ ⊢𝐹 𝑒 [𝑦/𝑥] : 𝜏 ′ for some 𝑦 ∉ Γ and well-formed 𝜏𝑥 .
  (5) If Γ ⊢𝐹 𝑒 [𝑡] : 𝜏 then there is some type 𝜎 and kind 𝑘 such that Γ ⊢𝐹 𝑒 : ∀ 𝛼 :𝑘. 𝜎 and 𝜏 =
      𝜎 [⌊𝑡⌋/𝛼].
  (6) If Γ ⊢𝐹 Λ𝛼 :𝑘.𝑒 : 𝜏 then there is some type 𝜏 ′ and kind 𝑘 such that 𝜏 = ∀ 𝛼 :𝑘. 𝜏 ′ and 𝛼 ′ :𝑘, Γ ⊢𝐹
      𝑒 [𝛼 ′ /𝛼] : 𝜏 ′ [𝛼 ′ /𝛼] for some 𝛼 ′ ∉ Γ.
  (7) If Γ ⊢𝐹 let 𝑥 = 𝑒𝑥 in 𝑒 : 𝜏 then there is some type 𝜏𝑥 and 𝑦 ∉ Γ such that Γ ⊢𝐹 𝑒𝑥 : 𝜏𝑥 and
      𝑦 :𝜏𝑥 , Γ ⊢𝐹 𝑒 [𝑦/𝑥] : 𝜏.
  (8) If Γ ⊢𝐹 𝑒 : 𝑡 : 𝜏 then 𝜏 = ⌊𝑡⌋ and Γ ⊢𝐹 𝑒 : 𝜏.
  Proof. This is clear from the deﬁnition of the typing rules for 𝜆𝐹 . Each premise can match only
one rule because the 𝜆𝐹 rules are syntax directed.                                              
    The Inversion of Typing Lemma does not hold in 𝜆𝑅𝐹 due to the subtyping relation. For instance
𝑥 : Int {𝜈 : 𝜈 = 5} ⊢ 𝑥 : Int but 𝑥 : Int ∉ 𝑥 : Int {𝜈 : 𝜈 = 5}. In Lemma ?? we state and prove an
analogous result for 𝜆𝑅𝐹 in the two cases needed to prove progress and preservation.
  Lemma A.5. (Primitives) For each built-in primitive 𝑐,
  (1) If ⌊ty(𝑐)⌋ = 𝜏𝑥 → 𝜏, and ∅ ⊢𝐹 𝑣 : 𝜏𝑥 then ∅ ⊢𝐹 𝛿 (𝑐, 𝑣) : 𝜏.
  (2) If ⌊ty(𝑐)⌋ = ∀ 𝛼 :𝐵. 𝜏 ′ , and ∅ ⊢𝑤 𝜏 : 𝐵, then ∅ ⊢𝐹 𝛿𝑇 (𝑐, 𝜏) : 𝜏 ′ [𝜏/𝛼].
  Proof. (1) First consider 𝑐 ∈ {∧, ∨, ↔}. Then ⌊ty(𝑐)⌋ = Bool → Bool → Bool. Then by
      Lemma A.3, ∅ ⊢𝐹 𝑣 : Bool gives us that 𝑣 = true or 𝑣 = false. For each possibility for 𝑐
      and 𝑣, we can build a judgment that ∅ ⊢𝐹 𝛿 (𝑐, 𝑣) : Bool → Bool. Similarly, if 𝑐 = ¬ then
      ⌊ty(𝑐)⌋ = Bool → Bool and 𝛿 (¬, 𝑣) ∈ {true, false} can be typed at Bool. The analysis for
      the other monomorphic primitives is entirely similar.
  (2) Here 𝑐 is the polymorphic = and ⌊ty(𝑐)⌋ = ∀ 𝛼 :𝐵. 𝛼 → 𝛼 → Bool. By the Canonical Forms
      Lemma, 𝜏 = Bool or 𝜏 = Int. In the former case, 𝛿𝑇 (𝑐, Bool) =↔, which we can type at
      Bool → Bool → Bool = ⌊ty(𝑐)⌋ [ Bool/𝛼]. The case of Int is entirely similar because
      𝛿𝑇 (𝑐, Int) is the monomorphic integer equality.
                                                                                              

A.2 Preservation
  Lemma A.6. (Preservation) If ∅ ⊢𝐹 𝑒 : 𝜏 and 𝑒 ↩→ 𝑒 ′ , then ∅ ⊢𝐹 𝑒 ′ : 𝜏.
  Proof. We proceed by induction of the structure of ∅ ⊢𝐹 𝑒 : 𝜏. The cases of rules T-Prim, T-Var,
T-Abs, or T-TAbs cannot occur because 𝑒 is a value and no value can take a step in our semantics.
Case T-App: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 𝑒 2 . Inverting, we have that there exists some
     type 𝜏2 such that ∅ ⊢𝐹 𝑒 1 : 𝜏2 → 𝜏 and ∅ ⊢𝐹 𝑒 2 : 𝜏2 . We split on ﬁve possible cases for the
     structure of 𝑒 1 and 𝑒 2 . First, suppose 𝑒 1 ≡ 𝜆𝑥 .𝑒 0 and 𝑒 2 is a value. Then by rule E-AppAbs
     and the determinism of our semantics, 𝑒 ′ ≡ 𝑒 0 [𝑒 2 /𝑥]. By the Inversion of Typing, for some
     𝑦 we have 𝑦 :𝜏2 ⊢𝐹 𝑒 0 [𝑦/𝑥] : 𝜏. By the Substitution Lemma, substituting 𝑒 2 through for 𝑦
     gives us ∅ ⊢𝐹 𝑒 0 [𝑒 2 /𝑥] : 𝜏 as desired because 𝑒 0 [𝑦/𝑥] [𝑒 2 /𝑦] = 𝑒 0 [𝑒 2 /𝑥]. Second, suppose

                                                                , Vol. 1, No. 1, Article . Publication date: July 2022.
30                                                                   Michael Borkowski, Niki Vazou, and Ranjit Jhala


     𝑒 1 ≡ 𝜆𝑥 .𝑒 0 and 𝑒 2 is not a value. Then by the progress lemma, there exists a term 𝑒 2′ such that
     𝑒 2 ↩→ 𝑒 2′ . Then by rule E-App2 and the determinism of our semantics, 𝑒 ′ ≡ 𝜆𝑥 .𝑒 0 𝑒 2′ . Now,
     by the inductive hypothesis, ∅ ⊢𝐹 𝑒 2′ : 𝜏2 . Applying rule T-App, ∅ ⊢𝐹 𝑒 1 𝑒 2′ : 𝜏 as desired.
     Third, suppose 𝑒 1 ≡ 𝑐, a built in primitive, and 𝑒 2 is a value. Then by rule E-Prim and the
     determinism of the semantics, 𝑒 ′ ≡ 𝛿 (𝑐, 𝑒 2 ). By the primitives lemma, ∅ ⊢𝐹 𝛿 (𝑐, 𝑒 2 ) : 𝜏 as
     desired. Fourth, suppose 𝑒 1 ≡ 𝑐 and 𝑒 2 is not a value. Then we argue in the same manner
     as the second case. Finally, by the canonical forms lemma, 𝑒 1 cannot be any other value, so
     it must not be a value. Then by the progress lemma, there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ .
     Then by rule E-App1 and the determinism of the semantics, 𝑒 ′ ≡ 𝑒 1′ 𝑒 2 . By the inductive
     hypothesis, ∅ ⊢𝐹 𝑒 1′ : 𝜏2 → 𝜏. Applying rule T-App, ∅ ⊢𝐹 𝑒 1′ 𝑒 2 : 𝜏 as desired.
Case T-TApp: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 [𝑡] and 𝜏 ≡ 𝜎 [⌊𝑡⌋/𝛼]. Inverting, we have that
     ∅ ⊢𝐹 𝑒 1 : ∀ 𝛼 :𝑘. 𝜎 and ∅ ⊢𝑤 ⌊𝑡⌋ : 𝑘. We split on three cases for the structure of 𝑒 1 . First,
     suppose 𝑒 1 ≡ Λ𝛼 :𝑘.𝑒 0 . Then by rule E-AppTAbs and the determinism of the semantics,
     𝑒 ′ ≡ 𝑒 0 [𝑡/𝛼]. By the inversion of typing, for some 𝛼 ′ , we have 𝛼 ′ :𝑘 ⊢𝐹 𝑒 0 [𝛼 ′ /𝛼] : 𝜎 [𝛼 ′ /𝛼].
     By the Substitution Lemma, substituting ⌊𝑡⌋ through for 𝛼 gives us ∅ ⊢𝐹 𝑒 0 [𝑡/𝛼] : 𝜎 [⌊𝑡⌋/𝛼]
     as desired. Second, suppose 𝑒 1 ≡ 𝑐, a built in primitive. Then by rule E-PrimT and the deter-
     minism of the semantics, 𝑒 ′𝛿𝑇 (𝑐, ⌊𝑡⌋). By the primitives lemma, ∅ ⊢𝐹 𝛿𝑇 (𝑐, ⌊𝑡⌋) : 𝜎 [⌊𝑡⌋/𝛼].
     Finally, by the canonical forms lemma, 𝑠𝑒𝑥𝑝𝑟 1 cannot be any other form of value, so it must
     not be a value. Then by the progress lemma, there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ . Then
     by rule E-AppT and the deterministic semantics 𝑒 ′ ≡ 𝑒 1′ [𝑡]. By the inductive hypothesis,
     ∅ ⊢𝐹 𝑒 1′ : ∀ 𝛼 :𝑘. 𝜎. Applying rule T-TApp, ∅ ⊢𝐹 𝑒 1′ [𝑡] : 𝜎 [⌊𝑡⌋/𝛼] as desired.
Case T-Let: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ let 𝑥 = 𝑒 1 in 𝑒 2 . Inverting, we have that 𝑦 :𝜏1 ⊢𝐹
     𝑒 2 [𝑦/𝑥] : 𝜏 and ∅ ⊢𝐹 𝑒 1 : 𝜏1 for some type 𝜏1 . By the progress lemma either 𝑒 1 is a value or
     there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ . In the former case, rule E-LetV and determinism give us
     𝑒 ′ ≡ 𝑒 2 [𝑒 1 /𝑥]. By the Substitution Lemma (substituting 𝑒 1 for 𝑥), we have ∅ ⊢𝐹 𝑒 2 [𝑒 1 /𝑥] : 𝜏 as
     desired because 𝑒 2 [𝑒 1 /𝑥] = 𝑒 2 [𝑦/𝑥] [𝑒 1 /𝑦]. In the latter case, by rule E-Let and determinism
     give us, 𝑒 ′ ≡ let 𝑥 = 𝑒 1′ in 𝑒 2 . By the inductive hypothesis we have that ∅ ⊢𝐹 𝑒 1′ : 𝜏1 and by
     rule T-Let we have ∅ ⊢𝐹 let 𝑥 = 𝑒 1′ in 𝑒 2 : 𝜏.
Case T-Ann: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 : 𝑡. Inverting, we have the ∅ ⊢𝐹 𝑒 1 : 𝜏 and 𝜏 = ⌊𝑡⌋.
     By the progress lemma, either 𝑒 1 is a value or there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ . In the
     former case, by rule E-AnnV and the determinism of the semantics, 𝑒 ′ ≡ 𝑒 1 . Then we already
     have that ∅ ⊢𝐹 𝑒 ′ : 𝜏 In the latter case, rule E-Ann and determinism give us 𝑒 ′ ≡ 𝑒 1′ : 𝑡. By
     the inductive hypothesis we have that ∅ ⊢𝐹 𝑒 1′ : 𝜏. By rule T-Ann we conclude ∅ ⊢𝐹 𝑒 1′ : 𝑡 : 𝜏.
                                                                                                           
   The proof of preservation for 𝜆𝑅𝐹 diﬀers in two cases above. In T-App and T-TApp, we must
use the Inversion of Typing lemma (??) from 𝜆𝑅𝐹 because the presence of rule T-Sub prevents us
from inferring the last rule used to type a term or type abstraction. Furthermore, in case T-App
the substitution lemma would give us that ∅ ⊢ 𝑒 ′ : 𝑡 [𝑣 𝑥 /𝑥] for some value 𝑣 𝑥 . However we need
to show preservation of the existential type ∃ 𝑥 :𝑡𝑥 . 𝑡. This is done by using rule S-Witn to show
that, in fact, ∅ ⊢ 𝑡 [𝑣 𝑥 /𝑥]  ∃ 𝑥 :𝑡𝑥 . 𝑡.
     Lemma A.7. (Substitution) If Γ ⊢𝐹 𝑣 𝑥 : 𝜏𝑥 and if Γ ⊢𝑤 ⌊𝑡𝛼 ⌋ : 𝑘𝛼 then
     (1) If Γ′, 𝑥 :𝜏𝑥 , Γ ⊢𝐹 𝑒 : 𝜏 and ⊢𝑤 Γ′, 𝑥 :𝜏𝑥 , Γ then Γ′, Γ ⊢𝐹 𝑒 [𝑣 𝑥 /𝑥] : 𝜏.
     (2) If Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 : 𝜏 and ⊢𝑤 Γ′, 𝛼 :𝑘𝛼 , Γ then Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 [𝑡𝛼 /𝛼] : 𝜏 [⌊𝑡𝛼 ⌋/𝛼]
  Proof. We give the proofs for part (2); part (1) is similar but slightly simpler because term
variables do not appear in types in 𝜆𝐹 We proceed by induction on the derivation tree of the
typing judgment Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 : 𝜏.

, Vol. 1, No. 1, Article . Publication date: July 2022.
 Mechanizing Refinement Types                                                                                          31


Case T-Prim: We have 𝑒 ≡ 𝑐 and Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑐 : ⌊ty(𝑐)⌋. Neither 𝑐 nor ty(𝑐) has any free variables,
 so each is unchanged under substitution. Then by rule T-Prim we conclude Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑐 :
 ⌊ty(𝑐)⌋ because the environment may be chosen arbitrarily.
Case T-Var: We have 𝑒 ≡ 𝑥; by inversion, we get that 𝑥 :𝜏 ∈ Γ′, 𝛼 :𝑘𝛼 , Γ. We must have 𝛼 ≠ 𝑥 so
 there are two cases to consider for where 𝑥 can appear in the environment. If 𝑥 :𝜏 ∈ Γ, then 𝜏
 cannot contain 𝛼 as a free variable because 𝑥 is bound ﬁrst in the environment (which grows from
 right to left). Then Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑥 : 𝜏 as desired because 𝜏 [⌊𝑡𝛼 ⌋/𝛼] = 𝜏. Otherwise 𝑥 :𝜏 ∈ Γ′
 and so 𝑥 :𝜏 [⌊𝑡𝛼 ⌋/𝛼] ∈ Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ. Thus Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑥 : 𝜏 [⌊𝑡𝛼 ⌋/𝛼]. (In part (1), we have an
 additional case where Γ′, 𝑥 :𝜏, Γ ⊢𝐹 𝑥 : 𝜏. We have 𝑥 [𝑣 𝑥 /𝑥] = 𝑣 𝑥 and so we can apply the weakening
 Lemma to Γ ⊢𝐹 𝑣 𝑥 : 𝜏 to obtain Γ′, Γ ⊢𝐹 𝑣 𝑥 : 𝜏.)
Case T-App: We have 𝑒 ≡ 𝑒 1 𝑒 2 . By inversion we have that Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 1 : 𝜏𝑥 → 𝜏 and Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹
 𝑒 2 : 𝜏𝑥 . Applying the inductive hypothesis to both of these, we get Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 1 [𝑡𝛼 /𝛼] :
 𝜏𝑥 → 𝜏 [⌊𝑡𝛼 ⌋/𝛼] and Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 2 [𝑡𝛼 /𝛼] : 𝜏𝑥 [⌊𝑡𝛼 ⌋/𝛼]. Combining these by rule T-App, we
 conclude Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 1 𝑒 2 [𝑡𝛼 /𝛼] : 𝜏 [⌊𝑡𝛼 ⌋/𝛼].
Case T-Abs: We have 𝑒 ≡ 𝜆𝑥 .𝑒 1 and 𝜏 ≡ 𝜏𝑥 → 𝜏1 . By inversion we have that for some 𝑦, both
 𝑦 :𝜏𝑥 , Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 1 [𝑦/𝑥] : 𝜏1 and Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝑤 𝜏𝑥 : 𝑘𝑥 . By the inductive hypothesis, and
 the Substitution Lemma for well-formedness judgments, we have 𝑦 :𝜏𝑥 [⌊𝑡𝛼 ⌋/𝛼], Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹
 𝑒 1 [𝑡𝛼 /𝛼] [𝑦/𝑥] : 𝜏1 [⌊𝑡𝛼 ⌋/𝛼] and Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝑤 𝜏𝑥 [⌊𝑡𝛼 ⌋/𝛼] : 𝑘𝑥 , where we can switch the order
 of substitutions because 𝑦 does not appear free in the well-formed type 𝑡𝛼 . Then we can conclude
 by applying rule T-Abs that Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝜆𝑥 .𝑒 1 [𝑡𝛼 /𝛼] : 𝜏𝑥 → 𝜏1 [⌊𝑡𝛼 ⌋/𝛼].
Case T-Let: We have 𝑒 ≡ let 𝑥 = 𝑒 1 in 𝑒 2 and by inversion we have that for some type 𝜏1 ,
 Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 1 : 𝜏1 and for some 𝑦 ∉ Γ′, 𝛼 :𝑘𝛼 , Γ, 𝑦 :𝜏1 , Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 2 [𝑦/𝑥] : 𝜏. By the inductive
 hypothesis, we have that Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 1 [𝑡𝛼 /𝛼] : 𝜏1 [⌊𝑡𝛼 ⌋/𝛼] and 𝑦 :𝜏1 [𝑡𝛼 /𝛼], Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹
 𝑒 2 [𝑡𝛼 /𝑥] : 𝜏 [⌊𝑡𝛼 ⌋/𝛼]. Then by rule T-Let we conclude Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 let 𝑥 = 𝑒 1 [𝑡𝛼 /𝛼] in 𝑒 2 [𝑡𝛼 /𝛼] :
 𝜏 [⌊𝑡𝛼 ⌋/𝛼].
Case T-Ann: We have 𝑒 ≡ 𝑒 ′ : 𝑡 and by inversion we have that ⌊𝑡⌋ = 𝜏 and Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 ′ : 𝜏.
 By the inductive hypothesis, we have Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 ′ [𝑡𝛼 /𝛼] : 𝜏 [⌊𝑡𝛼 ⌋/𝛼]. By our deﬁnition
 of reﬁnement erasure, we have ⌊𝑡 [𝑡𝛼 /𝛼]⌋ = ⌊𝑡⌋ [⌊𝑡𝛼 ⌋/𝛼] and we have 𝑒 ′ : 𝑡 [𝑡𝛼 /𝛼] = 𝑒 ′ [𝑡𝛼 /𝛼] :
 𝑡 [𝑡𝛼 /𝛼]. Thus by rule T-Ann, Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 ′ : 𝑡 [𝑡𝛼 /𝛼] : ⌊𝑡⌋ [⌊𝑡𝛼 ⌋/𝛼].                               

 B PROOFS OF SYSTEM RF SOUNDNESS
We present the proofs in this appendix in the same order
 Inversion of Typing Judgments. In the yellow region of Figure 1, we discuss how the fact that the
 typing judgment is no longer syntax-directed leads to an involved proof for the inversion lemma
 below. First, we need a lemma about subtyping:
   Lemma B.1. Transitivity of Subtyping: If Γ ⊢𝑤 𝑡 : 𝑘, Γ ⊢𝑤 𝑡 ′ : 𝑘 ′ , Γ ⊢𝑤 𝑡 ′′ : 𝑘 ′′ , and ⊢𝑤 Γ and
 Γ ⊢ 𝑡  𝑡 ′ and Γ ⊢ 𝑡 ′  𝑡 ′′ then Γ ⊢ 𝑡  𝑡 ′′ . (LemmasTransitive.hs) Our lem_sub_trans depends on
 lem_subst_sub.
   Proof. We proceed by induction on the combined size of the derivation trees of Γ ⊢ 𝑡 ′ <: 𝑡 ′
 and Γ ⊢ 𝑡 ′ <: 𝑡 ′′ . We ﬁrst consider the cases where none of 𝑡, 𝑡 ′, or 𝑡 ′′ are existential types. By
 examination of the subtyping rules, we see that 𝑡, 𝑡 ′ , and 𝑡 ′′ must have the same form, and so there
 are three such cases:
Case Reﬁnement types: In this case 𝑡 ≡ 𝑏{𝑥 1 : 𝑝 1 }, 𝑡 ′ ≡ 𝑏{𝑥 2 : 𝑝 2 }, and 𝑡 ′′ ≡ 𝑏{𝑥 3 : 𝑝 3 }. The last rule
 used in each of Γ ⊢ 𝑡 ′ <: 𝑡 ′ and Γ ⊢ 𝑡 ′ <: 𝑡 ′′ must have been S-Base. Inverting each of these we
 have
                       𝑦:𝑏{𝑥 1 : 𝑝 1 }, Γ ⊢ 𝑝 2 [𝑦/𝑥 2 ] and 𝑧:𝑏{𝑥 2 : 𝑝 2 }, Γ ⊢ 𝑝 3 [𝑧/𝑥 3 ]                 (1)

                                                                   , Vol. 1, No. 1, Article . Publication date: July 2022.
32                                                                       Michael Borkowski, Niki Vazou, and Ranjit Jhala


for some 𝑦, 𝑧 ∉ dom(Γ). We can invert Ent-Pred to get
                                ∀𝜃 . 𝜃 ∈ J𝑦:𝑏{𝑥 1 : 𝑝 1 }, ΓK ⇒ 𝜃 (𝑝 2 [𝑦/𝑥 2 ]) ↩→∗ true                                (2)
and
                          ∀𝜃 . 𝜃 ∈ J𝑦:𝑏{𝑥 2 : 𝑝 2 }, ΓK ⇒ 𝜃 (𝑝 3 [𝑦/𝑥 3 ]) ↩→∗ true.                            (3)
where we also use the change of free variables lemma in the last equation. Let 𝜃 ∈ J𝑦:𝑏{𝑥 1 : 𝑝 1 }, ΓK.
Let 𝑣 = 𝜃 (𝑦) Then 𝑣 ∈ J𝜃 (𝑏{𝑥 1 : 𝑝 1 })K, and so 𝑣 ∈ J𝜃 (𝑏{𝑥 2 : 𝑝 2 })K by the Denotational Soundness
Lemma. Then 𝜃 ∈ J𝑦:𝑏{𝑥 2 : 𝑝 2 }, ΓK also, and so 𝜃 (𝑝 3 ) [𝑦/𝑥 3 ] ↩→∗ true. Therefore we can conclude
that
                                         𝑦:𝑏{𝑥 1 : 𝑝 1 }, Γ ⊢ 𝑝 3 [𝑦/𝑥 3 ]                                      (4)
and thus that Γ ⊢ 𝑏{𝑥 1 : 𝑝 1 }  𝑏{𝑥 3 : 𝑝 3 }.
Case function types : In this case 𝑡 ≡ 𝑥 1 :𝑠 1 → 𝑡 1 , 𝑡 ′ ≡ 𝑥 2 :𝑠 2 → 𝑡 2 , and 𝑡 ′′ ≡ 𝑥 3 :𝑠 3 → 𝑡 3 . The last
rule used in each of Γ ⊢ 𝑡 ′ <: 𝑡 ′ and Γ ⊢ 𝑡 ′ <: 𝑡 ′′ must have been S-Func. Inverting each of these
we have
     Γ ⊢ 𝑠 2  𝑠 1, Γ ⊢ 𝑠 3  𝑠 2, 𝑦:𝑠 2, Γ ⊢ 𝑡 1 [𝑦/𝑥 1 ]  𝑡 2 [𝑦/𝑥 2 ], and 𝑧:𝑠 3 , Γ ⊢ 𝑡 2 [𝑧/𝑥 2 ]  𝑡 3 [𝑧/𝑥 3 ]
for some 𝑦, 𝑧 ∉ dom(Γ). By the inductive hypothesis we can combine the ﬁrst two judgments
to get Γ ⊢ 𝑠 3  𝑠1. By the narrowing lemma (see below) and the change of variables lemma we
have 𝑧:𝑠 3, Γ ⊢ 𝑡 1 [𝑧/𝑥 1 ]  𝑡 2 [𝑧/𝑥 2 ]; then we conclude by the inductive hypothesis that 𝑧:𝑠 3, Γ ⊢
𝑡 1 [𝑧/𝑥 1 ]  𝑡 3 [𝑧/𝑥 3 ]. Then by rule S-Func we conclude that Γ ⊢ 𝑥 1 :𝑠 1 → 𝑡 1  𝑥 3 :𝑠 3 → 𝑡 3 . The well-
formedness judgments required to apply the inductive hypothesis can be constructed by inverting
Γ ⊢𝑤 𝑡 : ∗, Γ ⊢𝑤 𝑡 ′ : ∗, and Γ ⊢𝑤 𝑡 ′′ : ∗ and using the change of free variables and narrowing
lemmas (for well-formedness).
Case polymorphic types : In this case 𝑡 ≡ ∀ 𝛼 1 :𝑘 1 . 𝑡 1 , 𝑡 ′ ≡ ∀ 𝛼 2 :𝑘 1 . 𝑡 2 , and 𝑡 ′′ ≡ ∀ 𝛼 3 :𝑘 1 . 𝑡 3 . The last
rule used in each of Γ ⊢ 𝑡 ′ <: 𝑡 ′ and Γ ⊢ 𝑡 ′ <: 𝑡 ′′ must have been S-Poly. Inverting each of these
we have
                    𝛼 :𝑘 1, Γ ⊢ 𝑡 1 [𝛼/𝛼 1 ]  𝑡 2 [𝛼/𝛼 2 ], and 𝛼 ′ :𝑘 1 , Γ ⊢ 𝑡 2 [𝛼 ′ /𝛼 2 ]  𝑡 3 [𝛼 ′ /𝛼 3 ]
for some 𝛼, 𝛼 ′ ∉ dom(Γ). By the change of variables lemma, we have 𝛼 :𝑘 1, Γ ⊢ 𝑡 2 [𝛼/𝛼 2 ]  𝑡 3 [𝛼/𝛼 3 ].
By the inductive hypothesis we can conclude that 𝛼 :𝑘 1, Γ ⊢ 𝑡 1 [𝛼/𝛼 1 ]  𝑡 3 [𝛼/𝛼 3 ] and thus Γ ⊢
∀ 𝛼 1 :𝑘 1 . 𝑡 1  ∀ 𝛼 3 :𝑘 1 . 𝑡 3 . The well-formedness judgments required to apply the inductive hypothe-
sis can be constructed by inverting Γ ⊢𝑤 𝑡 : ∗, Γ ⊢𝑤 𝑡 ′ : ∗, and Γ ⊢𝑤 𝑡 ′′ : ∗ and using the change of
free variables lemma.
Case 𝑡 ′′



                                                                                                                          
    Lemma B.2. Inversion of TAbs/TAbsT: If Γ ⊢ (𝜆𝑤 .𝑒) : 𝑥 :𝑡𝑥 → 𝑡 and ⊢𝑤 Γ then there exists
𝑦 ∉ dom(()Γ) such that 𝑦:𝑡𝑥, Γ ⊢ 𝑒 [𝑦/𝑤] : 𝑡 [𝑦/𝑥]. If Γ ⊢ (Λ𝑎 1 :𝑘 1 .𝑒) : ∀𝑎:𝑘.𝑡 and ⊢𝑤 Γ then exists
𝑎 ′ ∉ dom(()Γ) such that 𝑎 ′ :𝑘, Γ ⊢ 𝑒 [𝑎 ′ /𝑎 1 ] : 𝑡 [𝑎 ′ /𝑎].




, Vol. 1, No. 1, Article . Publication date: July 2022.
   1                                     Mechanizing Refinements with Types
   2
   3
                                         ANONYMOUS AUTHOR(S)
   4
arXiv:2207.05617v1 [cs.PL] 12 Jul 2022




   5
   6                                     A PROOFS OF 𝜆𝐹 SOUNDNESS
   7
                                         In this appendix, we present the proofs for each lemma of our 𝜆𝐹 metatheory presented in § ??.
   8
   9                                       Theorem A.1. (Type Safety) If ∅ ⊢𝐹 𝑒 : 𝜏 and 𝑒 ↩→∗ 𝑒 ′ , then 𝑒 ′ is a value or 𝑒 ′ ↩→ 𝑒 ′′ for some 𝑒 ′′ .
   10
   11                                        Proof. We proceed by induction on the number of steps in 𝑒 ↩→∗ 𝑒 ′ . There are two cases for
   12                                    𝑒 ↩→∗ 𝑒 ′ : either 𝑒 = 𝑒 ′ or there exists a term 𝑒 1 such that 𝑒 ↩→ 𝑒 1 ↩→∗ 𝑒 ′ . In the former case we
   13                                    conclude immediately by the Progress Lemma. In the latter case, ∅ ⊢𝐹 𝑒 1 : 𝜏 by the Preservation
   14                                    Lemma. Then by the inductive hypothesis applied to 𝑒 1 , we conclude that either 𝑒 ′ is a value or
   15                                    𝑒 ′ ↩→ 𝑒 ′′ for some 𝑒 ′′ .                                                                            
   16
   17
                                         A.1   Progress
   18                                      Lemma A.2. (Progress) If ∅ ⊢𝐹 𝑒 : 𝜏 then 𝑒 is a value or 𝑒 ↩→ 𝑒 ′ for some 𝑒 ′ .
   19
                                           Proof. We proceed by induction of the structure of ∅ ⊢𝐹 𝑒 : 𝜏. In the cases of rule T-Prim,
   20
                                         T-Var, T-Abs, or T-TAbs, 𝑒 is a value.
   21
   22                                    Case T-App: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 𝑒 2 . Inverting, we have that there exists some
   23                                         type 𝜏2 such that ∅ ⊢𝐹 𝑒 1 : 𝜏2 → 𝜏 and ∅ ⊢𝐹 𝑒 2 : 𝜏2 . We split on ﬁve possible cases for the
   24                                         structure of 𝑒 1 and 𝑒 2 . First, suppose 𝑒 1 ≡ 𝜆𝑥 .𝑒 0 and 𝑒 2 is a value. Then by rule E-AppAbs,
   25                                         𝑒 ≡ 𝜆𝑥 .𝑒 0 𝑒 2 ↩→ 𝑒 0 [𝑒 2 /𝑥]. Second, suppose 𝑒 1 ≡ 𝜆𝑥 .𝑒 0 and 𝑒 2 is not a value. Then by the
   26                                         inductive hypothesis, there exists a term 𝑒 2′ such that 𝑒 2 ↩→ 𝑒 2′ . Then by rule E-App2 𝑒 ≡
   27                                         𝜆𝑥 .𝑒 0 𝑒 2 ↩→ 𝜆𝑥 .𝑒 0 𝑒 2′ . Third, suppose 𝑒 1 ≡ 𝑐, a built in primitive and 𝑒 2 is a value. Then by
   28                                         rule E-Prim, 𝑒 ≡ 𝑐 𝑒 2 ↩→ 𝛿 (𝑐, 𝑒 2 ), which is well-deﬁned by the primitives lemma. Fourth,
   29                                         suppose 𝑒 1 ≡ 𝑐 and 𝑒 2 is not a value. Then by the inductive hypothesis, there exists a term
   30                                         𝑒 2′ such that 𝑒 2 ↩→ 𝑒 2′ . Then by rule E-App2 𝑒 ≡ 𝑐 𝑒 2 ↩→ 𝑐 𝑒 2′ . Finally, by the canonical
   31                                         forms lemma, 𝑒 1 cannot be any other value, so it must not be a value. Then by the inductive
   32                                         hypothesis, there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ . Then by rule E-App1, 𝑒 ≡ 𝑒 1 𝑒 2 ↩→ 𝑒 1′ 𝑒 2 .
   33                                    Case T-TApp: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 [𝑡] and 𝜏 ≡ 𝜎 [⌊𝑡⌋/𝛼]. Inverting, we have that
   34                                         ∅ ⊢𝐹 𝑒 1 : ∀ 𝛼 :𝑘. 𝜎. We split on three cases for the structure of 𝑒 1 . First, suppose 𝑒 1 ≡ Λ𝛼 ′ :𝑘 ′ .𝑒 0 .
   35                                         Then by rule E-AppTAbs, 𝑒 ≡ Λ𝛼 ′ :𝑘 ′ .𝑒 0 [𝑡] ↩→ 𝑒 0 [𝑡/𝛼 ′ ]. Second, suppose 𝑒 1 ≡ 𝑐, a built
   36                                         in primitive. Then by rule E-PrimT, 𝑒 ≡ 𝑐 [𝑡] ↩→ 𝛿𝑇 (𝑐, ⌊𝑡⌋), which is well-deﬁned by the
   37                                         primitives lemma. Finally, by the canonical forms lemma, 𝑠𝑒𝑥𝑝𝑟 1 cannot be any other form
   38                                         of value, so it must not be a value. Then by the inductive hypothesis, there is a term 𝑒 1′ such
   39                                         that 𝑒 1 ↩→ 𝑒 1′ . Then by rule E-AppT 𝑒 ≡ 𝑒 1 [𝑡] ↩→ 𝑒 1′ [𝑡].
   40                                    Case T-Let: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ let 𝑥 = 𝑒 1 in 𝑒 2 . Inverting, we have that ∅ ⊢𝐹 𝑒 1 : 𝜏1
   41                                         for some type 𝜏1 . By the inductive hypothesis, either 𝑒 1 is a value or there is a term 𝑒 1′ such
   42                                         that 𝑒 1 ↩→ 𝑒 1′ . In the former case, rule E-LetV gives us 𝑒 ≡ let 𝑥 = 𝑒 1 in 𝑒 2 ↩→ 𝑒 2 [𝑒 1 /𝑥]. In
   43                                         the latter case, by rule E-Let, 𝑒 ≡ let 𝑥 = 𝑒 1 in 𝑒 2 ↩→ let 𝑥 = 𝑒 1′ in 𝑒 2 .
   44                                    Case T-Ann: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 : 𝑡. Inverting, we have the ∅ ⊢𝐹 𝑒 1 : 𝜏 and 𝜏 = ⌊𝑡⌋.
   45                                         By the inductive hypothesis, either 𝑒 1 is a value or there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ . In
   46                                         the former case, by rule E-AnnV, 𝑒 ≡ 𝑒 1 : 𝑡 ↩→ 𝑒 1 . In the latter case, rule E-Ann gives us
   47                                         𝑒 ≡ 𝑒 1 : 𝑡𝑠𝑡𝑒𝑝𝑒 1′ : 𝑡.
   48                                                                                                                                                          
   49
                                                                                                           , Vol. 1, No. 1, Article . Publication date: July 2022.
     2                                                                                                      Anon.


50      The progress proof is substantially the same for 𝜆𝑅𝐹 . The only diﬀerence is that there is another
51   straightforward inductive case for rule T-Sub.
52
         Lemma A.3. (𝜆𝐹 Canonical Forms)
53
54
         (1) If ∅ ⊢𝐹 𝑣 : Bool then 𝑣 = true or 𝑣 = false.
55
         (2) If ∅ ⊢𝐹 𝑣 : Int then 𝑣 is an integer constant.
56
         (3) If ∅ ⊢𝐹 𝑣 : 𝜏 → 𝜏 ′ then either 𝑣 = 𝜆𝑥 .𝑒 or 𝑣 = 𝑐, a built in primitive function where 𝑐 ∈
57
             {∧, ∨, ¬, ↔, ≤, =}.
58
         (4) If ∅ ⊢𝐹 𝑣 : ∀ 𝑎:𝑘. 𝜏 then either 𝑣 = Λ𝑎:𝑘. 𝑒 or 𝑣 is the polymorphic equality =.
59
         (5) If ∅ ⊢𝑤 𝜏 : 𝐵 then 𝜏 = Bool or 𝜏 = Int.
60      Proof. Parts (1) - (4) are easily deduced from the 𝜆𝐹 typing rules in Figure ?? and the deﬁnition
61   of 𝑡𝑦(𝑐). Part (5) is clear from the well-formedness rules in Figure ??.                           
62
        Lemma A.3 is suﬃcient for our 𝜆𝑅𝐹 metatheory. Our syntactic typing judgments in 𝜆𝑅𝐹 respect
63
     those of 𝜆𝐹 . Speciﬁcally, if Γ ⊢ 𝑒 : 𝑡 and ⊢𝑤 Γ, then ⌊Γ⌋ ⊢𝐹 𝑒 : ⌊𝑡⌋. Therefore, we do not have to
64
     state and prove a separate Canonical Forms Lemma for 𝜆𝑅𝐹 .
65
66       Lemma A.4. (Inversion of Typing)
67       (1) If Γ ⊢𝐹 𝑐 : 𝜏 then 𝜏 = ⌊ty(𝑐)⌋.
68       (2) If Γ ⊢𝐹 𝑥 : 𝜏 then 𝑥 :𝜏 ∈ Γ.
69       (3) If Γ ⊢𝐹 𝑒 𝑒 ′ : 𝜏 then there is some type 𝜏𝑥 such that Γ ⊢𝐹 𝑒 : 𝜏𝑥 → 𝜏 and Γ ⊢𝐹 𝑒 ′ : 𝜏𝑥 .
70       (4) If Γ ⊢𝐹 𝜆𝑥 .𝑒 : 𝜏 then 𝜏 = 𝜏𝑥 → 𝜏 ′ and 𝑦 :𝜏𝑥 , Γ ⊢𝐹 𝑒 [𝑦/𝑥] : 𝜏 ′ for some 𝑦 ∉ Γ and well-formed 𝜏𝑥 .
71       (5) If Γ ⊢𝐹 𝑒 [𝑡] : 𝜏 then there is some type 𝜎 and kind 𝑘 such that Γ ⊢𝐹 𝑒 : ∀ 𝛼 :𝑘. 𝜎 and 𝜏 =
72           𝜎 [⌊𝑡⌋/𝛼].
73       (6) If Γ ⊢𝐹 Λ𝛼 :𝑘.𝑒 : 𝜏 then there is some type 𝜏 ′ and kind 𝑘 such that 𝜏 = ∀ 𝛼 :𝑘. 𝜏 ′ and 𝛼 ′ :𝑘, Γ ⊢𝐹
74           𝑒 [𝛼 ′ /𝛼] : 𝜏 ′ [𝛼 ′ /𝛼] for some 𝛼 ′ ∉ Γ.
75       (7) If Γ ⊢𝐹 let 𝑥 = 𝑒𝑥 in 𝑒 : 𝜏 then there is some type 𝜏𝑥 and 𝑦 ∉ Γ such that Γ ⊢𝐹 𝑒𝑥 : 𝜏𝑥 and
76           𝑦 :𝜏𝑥 , Γ ⊢𝐹 𝑒 [𝑦/𝑥] : 𝜏.
77       (8) If Γ ⊢𝐹 𝑒 : 𝑡 : 𝜏 then 𝜏 = ⌊𝑡⌋ and Γ ⊢𝐹 𝑒 : 𝜏.
78
       Proof. This is clear from the deﬁnition of the typing rules for 𝜆𝐹 . Each premise can match only
79
     one rule because the 𝜆𝐹 rules are syntax directed.                                              
80
81       The Inversion of Typing Lemma does not hold in 𝜆𝑅𝐹 due to the subtyping relation. For instance
82   𝑥 : Int {𝜈 : 𝜈 = 5} ⊢ 𝑥 : Int but 𝑥 : Int ∉ 𝑥 : Int {𝜈 : 𝜈 = 5}. In Lemma ?? we state and prove an
83   analogous result for 𝜆𝑅𝐹 in the two cases needed to prove progress and preservation.
84
         Lemma A.5. (Primitives) For each built-in primitive 𝑐,
85
86
         (1) If ⌊ty(𝑐)⌋ = 𝜏𝑥 → 𝜏, and ∅ ⊢𝐹 𝑣 : 𝜏𝑥 then ∅ ⊢𝐹 𝛿 (𝑐, 𝑣) : 𝜏.
87
         (2) If ⌊ty(𝑐)⌋ = ∀ 𝛼 :𝐵. 𝜏 ′ , and ∅ ⊢𝑤 𝜏 : 𝐵, then ∅ ⊢𝐹 𝛿𝑇 (𝑐, 𝜏) : 𝜏 ′ [𝜏/𝛼].
88       Proof. (1) First consider 𝑐 ∈ {∧, ∨, ↔}. Then ⌊ty(𝑐)⌋ = Bool → Bool → Bool. Then by
89           Lemma A.3, ∅ ⊢𝐹 𝑣 : Bool gives us that 𝑣 = true or 𝑣 = false. For each possibility for 𝑐
90           and 𝑣, we can build a judgment that ∅ ⊢𝐹 𝛿 (𝑐, 𝑣) : Bool → Bool. Similarly, if 𝑐 = ¬ then
91           ⌊ty(𝑐)⌋ = Bool → Bool and 𝛿 (¬, 𝑣) ∈ {true, false} can be typed at Bool. The analysis for
92           the other monomorphic primitives is entirely similar.
93       (2) Here 𝑐 is the polymorphic = and ⌊ty(𝑐)⌋ = ∀ 𝛼 :𝐵. 𝛼 → 𝛼 → Bool. By the Canonical Forms
94           Lemma, 𝜏 = Bool or 𝜏 = Int. In the former case, 𝛿𝑇 (𝑐, Bool) =↔, which we can type at
95           Bool → Bool → Bool = ⌊ty(𝑐)⌋ [ Bool/𝛼]. The case of Int is entirely similar because
96           𝛿𝑇 (𝑐, Int) is the monomorphic integer equality.
97                                                                                                   
98
     , Vol. 1, No. 1, Article . Publication date: July 2022.
      Mechanizing Refinements with Types                                                                                  3


99    A.2 Preservation
100
        Lemma A.6. (Preservation) If ∅ ⊢𝐹 𝑒 : 𝜏 and 𝑒 ↩→ 𝑒 ′ , then ∅ ⊢𝐹 𝑒 ′ : 𝜏.
101
102     Proof. We proceed by induction of the structure of ∅ ⊢𝐹 𝑒 : 𝜏. The cases of rules T-Prim, T-Var,
103   T-Abs, or T-TAbs cannot occur because 𝑒 is a value and no value can take a step in our semantics.
104   Case T-App: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 𝑒 2 . Inverting, we have that there exists some
105        type 𝜏2 such that ∅ ⊢𝐹 𝑒 1 : 𝜏2 → 𝜏 and ∅ ⊢𝐹 𝑒 2 : 𝜏2 . We split on ﬁve possible cases for the
106        structure of 𝑒 1 and 𝑒 2 . First, suppose 𝑒 1 ≡ 𝜆𝑥 .𝑒 0 and 𝑒 2 is a value. Then by rule E-AppAbs
107        and the determinism of our semantics, 𝑒 ′ ≡ 𝑒 0 [𝑒 2 /𝑥]. By the Inversion of Typing, for some
108        𝑦 we have 𝑦 :𝜏2 ⊢𝐹 𝑒 0 [𝑦/𝑥] : 𝜏. By the Substitution Lemma, substituting 𝑒 2 through for 𝑦
109        gives us ∅ ⊢𝐹 𝑒 0 [𝑒 2 /𝑥] : 𝜏 as desired because 𝑒 0 [𝑦/𝑥] [𝑒 2 /𝑦] = 𝑒 0 [𝑒 2 /𝑥]. Second, suppose
110        𝑒 1 ≡ 𝜆𝑥 .𝑒 0 and 𝑒 2 is not a value. Then by the progress lemma, there exists a term 𝑒 2′ such that
111        𝑒 2 ↩→ 𝑒 2′ . Then by rule E-App2 and the determinism of our semantics, 𝑒 ′ ≡ 𝜆𝑥 .𝑒 0 𝑒 2′ . Now,
112        by the inductive hypothesis, ∅ ⊢𝐹 𝑒 2′ : 𝜏2 . Applying rule T-App, ∅ ⊢𝐹 𝑒 1 𝑒 2′ : 𝜏 as desired.
113        Third, suppose 𝑒 1 ≡ 𝑐, a built in primitive, and 𝑒 2 is a value. Then by rule E-Prim and the
114        determinism of the semantics, 𝑒 ′ ≡ 𝛿 (𝑐, 𝑒 2 ). By the primitives lemma, ∅ ⊢𝐹 𝛿 (𝑐, 𝑒 2 ) : 𝜏 as
115        desired. Fourth, suppose 𝑒 1 ≡ 𝑐 and 𝑒 2 is not a value. Then we argue in the same manner
116        as the second case. Finally, by the canonical forms lemma, 𝑒 1 cannot be any other value, so
117        it must not be a value. Then by the progress lemma, there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ .
118        Then by rule E-App1 and the determinism of the semantics, 𝑒 ′ ≡ 𝑒 1′ 𝑒 2 . By the inductive
119        hypothesis, ∅ ⊢𝐹 𝑒 1′ : 𝜏2 → 𝜏. Applying rule T-App, ∅ ⊢𝐹 𝑒 1′ 𝑒 2 : 𝜏 as desired.
120   Case T-TApp: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 [𝑡] and 𝜏 ≡ 𝜎 [⌊𝑡⌋/𝛼]. Inverting, we have that
121        ∅ ⊢𝐹 𝑒 1 : ∀ 𝛼 :𝑘. 𝜎 and ∅ ⊢𝑤 ⌊𝑡⌋ : 𝑘. We split on three cases for the structure of 𝑒 1 . First,
122        suppose 𝑒 1 ≡ Λ𝛼 :𝑘.𝑒 0 . Then by rule E-AppTAbs and the determinism of the semantics,
123        𝑒 ′ ≡ 𝑒 0 [𝑡/𝛼]. By the inversion of typing, for some 𝛼 ′ , we have 𝛼 ′ :𝑘 ⊢𝐹 𝑒 0 [𝛼 ′ /𝛼] : 𝜎 [𝛼 ′ /𝛼].
124        By the Substitution Lemma, substituting ⌊𝑡⌋ through for 𝛼 gives us ∅ ⊢𝐹 𝑒 0 [𝑡/𝛼] : 𝜎 [⌊𝑡⌋/𝛼]
125        as desired. Second, suppose 𝑒 1 ≡ 𝑐, a built in primitive. Then by rule E-PrimT and the deter-
126        minism of the semantics, 𝑒 ′𝛿𝑇 (𝑐, ⌊𝑡⌋). By the primitives lemma, ∅ ⊢𝐹 𝛿𝑇 (𝑐, ⌊𝑡⌋) : 𝜎 [⌊𝑡⌋/𝛼].
127        Finally, by the canonical forms lemma, 𝑠𝑒𝑥𝑝𝑟 1 cannot be any other form of value, so it must
128        not be a value. Then by the progress lemma, there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ . Then
129        by rule E-AppT and the deterministic semantics 𝑒 ′ ≡ 𝑒 1′ [𝑡]. By the inductive hypothesis,
130        ∅ ⊢𝐹 𝑒 1′ : ∀ 𝛼 :𝑘. 𝜎. Applying rule T-TApp, ∅ ⊢𝐹 𝑒 1′ [𝑡] : 𝜎 [⌊𝑡⌋/𝛼] as desired.
131   Case T-Let: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ let 𝑥 = 𝑒 1 in 𝑒 2 . Inverting, we have that 𝑦 :𝜏1 ⊢𝐹
132        𝑒 2 [𝑦/𝑥] : 𝜏 and ∅ ⊢𝐹 𝑒 1 : 𝜏1 for some type 𝜏1 . By the progress lemma either 𝑒 1 is a value or
133        there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ . In the former case, rule E-LetV and determinism give us
134        𝑒 ′ ≡ 𝑒 2 [𝑒 1 /𝑥]. By the Substitution Lemma (substituting 𝑒 1 for 𝑥), we have ∅ ⊢𝐹 𝑒 2 [𝑒 1 /𝑥] : 𝜏 as
135        desired because 𝑒 2 [𝑒 1 /𝑥] = 𝑒 2 [𝑦/𝑥] [𝑒 1 /𝑦]. In the latter case, by rule E-Let and determinism
136        give us, 𝑒 ′ ≡ let 𝑥 = 𝑒 1′ in 𝑒 2 . By the inductive hypothesis we have that ∅ ⊢𝐹 𝑒 1′ : 𝜏1 and by
137        rule T-Let we have ∅ ⊢𝐹 let 𝑥 = 𝑒 1′ in 𝑒 2 : 𝜏.
138   Case T-Ann: We have ∅ ⊢𝐹 𝑒 : 𝜏 where 𝑒 ≡ 𝑒 1 : 𝑡. Inverting, we have the ∅ ⊢𝐹 𝑒 1 : 𝜏 and 𝜏 = ⌊𝑡⌋.
139        By the progress lemma, either 𝑒 1 is a value or there is a term 𝑒 1′ such that 𝑒 1 ↩→ 𝑒 1′ . In the
140        former case, by rule E-AnnV and the determinism of the semantics, 𝑒 ′ ≡ 𝑒 1 . Then we already
141        have that ∅ ⊢𝐹 𝑒 ′ : 𝜏 In the latter case, rule E-Ann and determinism give us 𝑒 ′ ≡ 𝑒 1′ : 𝑡. By
142        the inductive hypothesis we have that ∅ ⊢𝐹 𝑒 1′ : 𝜏. By rule T-Ann we conclude ∅ ⊢𝐹 𝑒 1′ : 𝑡 : 𝜏.
143
                                                                                                                 
144
145     The proof of preservation for 𝜆𝑅𝐹 diﬀers in two cases above. In T-App and T-TApp, we must
146   use the Inversion of Typing lemma (??) from 𝜆𝑅𝐹 because the presence of rule T-Sub prevents us
147
                                                                     , Vol. 1, No. 1, Article . Publication date: July 2022.
       4                                                                                                        Anon.


148    from inferring the last rule used to type a term or type abstraction. Furthermore, in case T-App
149    the substitution lemma would give us that ∅ ⊢ 𝑒 ′ : 𝑡 [𝑣 𝑥 /𝑥] for some value 𝑣 𝑥 . However we need
150    to show preservation of the existential type ∃ 𝑥 :𝑡𝑥 . 𝑡. This is done by using rule S-Witn to show
151    that, in fact, ∅ ⊢ 𝑡 [𝑣 𝑥 /𝑥]  ∃ 𝑥 :𝑡𝑥 . 𝑡.
152
153        Lemma A.7. (Substitution) If Γ ⊢𝐹 𝑣 𝑥 : 𝜏𝑥 and if Γ ⊢𝑤 ⌊𝑡𝛼 ⌋ : 𝑘𝛼 then
154
           (1) If Γ′, 𝑥 :𝜏𝑥 , Γ ⊢𝐹 𝑒 : 𝜏 and ⊢𝑤 Γ′, 𝑥 :𝜏𝑥 , Γ then Γ′, Γ ⊢𝐹 𝑒 [𝑣 𝑥 /𝑥] : 𝜏.
155
           (2) If Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 : 𝜏 and ⊢𝑤 Γ′, 𝛼 :𝑘𝛼 , Γ then Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 [𝑡𝛼 /𝛼] : 𝜏 [⌊𝑡𝛼 ⌋/𝛼]
156
157        Proof. We give the proofs for part (2); part (1) is similar but slightly simpler because term
158    variables do not appear in types in 𝜆𝐹 We proceed by induction on the derivation tree of the
159    typing judgment Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 : 𝜏.
160   Case T-Prim: We have 𝑒 ≡ 𝑐 and Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑐 : ⌊ty(𝑐)⌋. Neither 𝑐 nor ty(𝑐) has any free variables,
161    so each is unchanged under substitution. Then by rule T-Prim we conclude Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑐 :
162    ⌊ty(𝑐)⌋ because the environment may be chosen arbitrarily.
163   Case T-Var: We have 𝑒 ≡ 𝑥; by inversion, we get that 𝑥 :𝜏 ∈ Γ′, 𝛼 :𝑘𝛼 , Γ. We must have 𝛼 ≠ 𝑥 so
164    there are two cases to consider for where 𝑥 can appear in the environment. If 𝑥 :𝜏 ∈ Γ, then 𝜏
165    cannot contain 𝛼 as a free variable because 𝑥 is bound ﬁrst in the environment (which grows from
166    right to left). Then Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑥 : 𝜏 as desired because 𝜏 [⌊𝑡𝛼 ⌋/𝛼] = 𝜏. Otherwise 𝑥 :𝜏 ∈ Γ′
167    and so 𝑥 :𝜏 [⌊𝑡𝛼 ⌋/𝛼] ∈ Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ. Thus Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑥 : 𝜏 [⌊𝑡𝛼 ⌋/𝛼]. (In part (1), we have an
168    additional case where Γ′, 𝑥 :𝜏, Γ ⊢𝐹 𝑥 : 𝜏. We have 𝑥 [𝑣 𝑥 /𝑥] = 𝑣 𝑥 and so we can apply the weakening
169    Lemma to Γ ⊢𝐹 𝑣 𝑥 : 𝜏 to obtain Γ′, Γ ⊢𝐹 𝑣 𝑥 : 𝜏.)
170   Case T-App: We have 𝑒 ≡ 𝑒 1 𝑒 2 . By inversion we have that Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 1 : 𝜏𝑥 → 𝜏 and Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹
171    𝑒 2 : 𝜏𝑥 . Applying the inductive hypothesis to both of these, we get Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 1 [𝑡𝛼 /𝛼] :
172    𝜏𝑥 → 𝜏 [⌊𝑡𝛼 ⌋/𝛼] and Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 2 [𝑡𝛼 /𝛼] : 𝜏𝑥 [⌊𝑡𝛼 ⌋/𝛼]. Combining these by rule T-App, we
173    conclude Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 1 𝑒 2 [𝑡𝛼 /𝛼] : 𝜏 [⌊𝑡𝛼 ⌋/𝛼].
174   Case T-Abs: We have 𝑒 ≡ 𝜆𝑥 .𝑒 1 and 𝜏 ≡ 𝜏𝑥 → 𝜏1 . By inversion we have that for some 𝑦, both
175    𝑦 :𝜏𝑥 , Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 1 [𝑦/𝑥] : 𝜏1 and Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝑤 𝜏𝑥 : 𝑘𝑥 . By the inductive hypothesis, and
176    the Substitution Lemma for well-formedness judgments, we have 𝑦 :𝜏𝑥 [⌊𝑡𝛼 ⌋/𝛼], Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹
177    𝑒 1 [𝑡𝛼 /𝛼] [𝑦/𝑥] : 𝜏1 [⌊𝑡𝛼 ⌋/𝛼] and Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝑤 𝜏𝑥 [⌊𝑡𝛼 ⌋/𝛼] : 𝑘𝑥 , where we can switch the order
178    of substitutions because 𝑦 does not appear free in the well-formed type 𝑡𝛼 . Then we can conclude
179    by applying rule T-Abs that Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝜆𝑥 .𝑒 1 [𝑡𝛼 /𝛼] : 𝜏𝑥 → 𝜏1 [⌊𝑡𝛼 ⌋/𝛼].
180   Case T-Let: We have 𝑒 ≡ let 𝑥 = 𝑒 1 in 𝑒 2 and by inversion we have that for some type 𝜏1 ,
181    Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 1 : 𝜏1 and for some 𝑦 ∉ Γ′, 𝛼 :𝑘𝛼 , Γ, 𝑦 :𝜏1 , Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 2 [𝑦/𝑥] : 𝜏. By the inductive
182    hypothesis, we have that Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 1 [𝑡𝛼 /𝛼] : 𝜏1 [⌊𝑡𝛼 ⌋/𝛼] and 𝑦 :𝜏1 [𝑡𝛼 /𝛼], Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹
183    𝑒 2 [𝑡𝛼 /𝑥] : 𝜏 [⌊𝑡𝛼 ⌋/𝛼]. Then by rule T-Let we conclude Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 let 𝑥 = 𝑒 1 [𝑡𝛼 /𝛼] in 𝑒 2 [𝑡𝛼 /𝛼] :
184    𝜏 [⌊𝑡𝛼 ⌋/𝛼].
185   Case T-Ann: We have 𝑒 ≡ 𝑒 ′ : 𝑡 and by inversion we have that ⌊𝑡⌋ = 𝜏 and Γ′, 𝛼 :𝑘𝛼 , Γ ⊢𝐹 𝑒 ′ : 𝜏.
186    By the inductive hypothesis, we have Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 ′ [𝑡𝛼 /𝛼] : 𝜏 [⌊𝑡𝛼 ⌋/𝛼]. By our deﬁnition
187    of reﬁnement erasure, we have ⌊𝑡 [𝑡𝛼 /𝛼]⌋ = ⌊𝑡⌋ [⌊𝑡𝛼 ⌋/𝛼] and we have 𝑒 ′ : 𝑡 [𝑡𝛼 /𝛼] = 𝑒 ′ [𝑡𝛼 /𝛼] :
188    𝑡 [𝑡𝛼 /𝛼]. Thus by rule T-Ann, Γ′ [⌊𝑡𝛼 ⌋/𝛼], Γ ⊢𝐹 𝑒 ′ : 𝑡 [𝑡𝛼 /𝛼] : ⌊𝑡⌋ [⌊𝑡𝛼 ⌋/𝛼].                               
189
190   B PROOFS OF SYSTEM RF SOUNDNESS
191
      We present the proofs in this appendix in the same order
192
193    Inversion of Typing Judgments. In the yellow region of Figure ??, we discuss how the fact
194    that the typing judgment is no longer syntax-directed leads to an involved proof for the inversion
195    lemma below. First, we need a lemma about subtyping:
196
       , Vol. 1, No. 1, Article . Publication date: July 2022.
       Mechanizing Refinements with Types                                                                                           5


197      Lemma B.1. Transitivity of Subtyping: If Γ ⊢𝑤 𝑡 : 𝑘, Γ ⊢𝑤 𝑡 ′ : 𝑘 ′ , Γ ⊢𝑤 𝑡 ′′ : 𝑘 ′′ , and ⊢𝑤 Γ and
198    Γ ⊢ 𝑡  𝑡 ′ and Γ ⊢ 𝑡 ′  𝑡 ′′ then Γ ⊢ 𝑡  𝑡 ′′ . (LemmasTransitive.hs) Our lem_sub_trans depends on
199    lem_subst_sub.
200
201
         Proof. We proceed by induction on the combined size of the derivation trees of Γ ⊢ 𝑡 ′ <: 𝑡 ′
202
       and Γ ⊢ 𝑡 ′ <: 𝑡 ′′ . We ﬁrst consider the cases where none of 𝑡, 𝑡 ′, or 𝑡 ′′ are existential types. By
203
       examination of the subtyping rules, we see that 𝑡, 𝑡 ′ , and 𝑡 ′′ must have the same form, and so there
204
       are three such cases:
205
      Case Reﬁnement types: In this case 𝑡 ≡ 𝑏{𝑥 1 : 𝑝 1 }, 𝑡 ′ ≡ 𝑏{𝑥 2 : 𝑝 2 }, and 𝑡 ′′ ≡ 𝑏{𝑥 3 : 𝑝 3 }. The last rule
206
       used in each of Γ ⊢ 𝑡 ′ <: 𝑡 ′ and Γ ⊢ 𝑡 ′ <: 𝑡 ′′ must have been S-Base. Inverting each of these we
207
       have
208                          𝑦:𝑏{𝑥 1 : 𝑝 1 }, Γ ⊢ 𝑝 2 [𝑦/𝑥 2 ] and 𝑧:𝑏{𝑥 2 : 𝑝 2 }, Γ ⊢ 𝑝 3 [𝑧/𝑥 3 ]                 (1)
209    for some 𝑦, 𝑧 ∉ dom(Γ). We can invert Ent-Pred to get
210
                                     ∀𝜃 . 𝜃 ∈ J𝑦:𝑏{𝑥 1 : 𝑝 1 }, ΓK ⇒ 𝜃 (𝑝 2 [𝑦/𝑥 2 ]) ↩→∗ true                                    (2)
211
212    and
213                                 ∀𝜃 . 𝜃 ∈ J𝑦:𝑏{𝑥 2 : 𝑝 2 }, ΓK ⇒ 𝜃 (𝑝 3 [𝑦/𝑥 3 ]) ↩→∗ true.                                    (3)
214
       where we also use the change of free variables lemma in the last equation. Let 𝜃 ∈ J𝑦:𝑏{𝑥 1 : 𝑝 1 }, ΓK.
215
       Let 𝑣 = 𝜃 (𝑦) Then 𝑣 ∈ J𝜃 (𝑏{𝑥 1 : 𝑝 1 })K, and so 𝑣 ∈ J𝜃 (𝑏{𝑥 2 : 𝑝 2 })K by the Denotational Soundness
216
       Lemma. Then 𝜃 ∈ J𝑦:𝑏{𝑥 2 : 𝑝 2 }, ΓK also, and so 𝜃 (𝑝 3 ) [𝑦/𝑥 3 ] ↩→∗ true. Therefore we can conclude
217
       that
218
                                               𝑦:𝑏{𝑥 1 : 𝑝 1 }, Γ ⊢ 𝑝 3 [𝑦/𝑥 3 ]                            (4)
219
220    and thus that Γ ⊢ 𝑏{𝑥 1 : 𝑝 1 }  𝑏{𝑥 3 : 𝑝 3 }.
221    Case function types : In this case 𝑡 ≡ 𝑥 1 :𝑠 1 → 𝑡 1 , 𝑡 ′ ≡ 𝑥 2 :𝑠 2 → 𝑡 2 , and 𝑡 ′′ ≡ 𝑥 3 :𝑠 3 → 𝑡 3 . The last
222    rule used in each of Γ ⊢ 𝑡 ′ <: 𝑡 ′ and Γ ⊢ 𝑡 ′ <: 𝑡 ′′ must have been S-Func. Inverting each of these
223    we have
224
           Γ ⊢ 𝑠 2  𝑠 1, Γ ⊢ 𝑠 3  𝑠 2, 𝑦:𝑠 2, Γ ⊢ 𝑡 1 [𝑦/𝑥 1 ]  𝑡 2 [𝑦/𝑥 2 ], and 𝑧:𝑠 3 , Γ ⊢ 𝑡 2 [𝑧/𝑥 2 ]  𝑡 3 [𝑧/𝑥 3 ]
225
226    for some 𝑦, 𝑧 ∉ dom(Γ). By the inductive hypothesis we can combine the ﬁrst two judgments
227    to get Γ ⊢ 𝑠 3  𝑠1. By the narrowing lemma (see below) and the change of variables lemma we
228    have 𝑧:𝑠 3, Γ ⊢ 𝑡 1 [𝑧/𝑥 1 ]  𝑡 2 [𝑧/𝑥 2 ]; then we conclude by the inductive hypothesis that 𝑧:𝑠 3, Γ ⊢
229    𝑡 1 [𝑧/𝑥 1 ]  𝑡 3 [𝑧/𝑥 3 ]. Then by rule S-Func we conclude that Γ ⊢ 𝑥 1 :𝑠 1 → 𝑡 1  𝑥 3 :𝑠 3 → 𝑡 3 . The well-
230    formedness judgments required to apply the inductive hypothesis can be constructed by inverting
231    Γ ⊢𝑤 𝑡 : ∗, Γ ⊢𝑤 𝑡 ′ : ∗, and Γ ⊢𝑤 𝑡 ′′ : ∗ and using the change of free variables and narrowing
232    lemmas (for well-formedness).
233    Case polymorphic types : In this case 𝑡 ≡ ∀ 𝛼 1 :𝑘 1 . 𝑡 1 , 𝑡 ′ ≡ ∀ 𝛼 2 :𝑘 1 . 𝑡 2 , and 𝑡 ′′ ≡ ∀ 𝛼 3 :𝑘 1 . 𝑡 3 . The last
234    rule used in each of Γ ⊢ 𝑡 ′ <: 𝑡 ′ and Γ ⊢ 𝑡 ′ <: 𝑡 ′′ must have been S-Poly. Inverting each of these
235    we have
236                        𝛼 :𝑘 1, Γ ⊢ 𝑡 1 [𝛼/𝛼 1 ]  𝑡 2 [𝛼/𝛼 2 ], and 𝛼 ′ :𝑘 1 , Γ ⊢ 𝑡 2 [𝛼 ′ /𝛼 2 ]  𝑡 3 [𝛼 ′ /𝛼 3 ]
237
       for some 𝛼, 𝛼 ′ ∉ dom(Γ). By the change of variables lemma, we have 𝛼 :𝑘 1, Γ ⊢ 𝑡 2 [𝛼/𝛼 2 ]  𝑡 3 [𝛼/𝛼 3 ].
238
       By the inductive hypothesis we can conclude that 𝛼 :𝑘 1, Γ ⊢ 𝑡 1 [𝛼/𝛼 1 ]  𝑡 3 [𝛼/𝛼 3 ] and thus Γ ⊢
239
       ∀ 𝛼 1 :𝑘 1 . 𝑡 1  ∀ 𝛼 3 :𝑘 1 . 𝑡 3 . The well-formedness judgments required to apply the inductive hypothe-
240
       sis can be constructed by inverting Γ ⊢𝑤 𝑡 : ∗, Γ ⊢𝑤 𝑡 ′ : ∗, and Γ ⊢𝑤 𝑡 ′′ : ∗ and using the change of
241
       free variables lemma.
242
243    Case 𝑡 ′′
244
245
                                                                               , Vol. 1, No. 1, Article . Publication date: July 2022.
      6                                                                                                Anon.


246
247                                                                                                        
248
          Lemma B.2. Inversion of TAbs/TAbsT: If Γ ⊢ (𝜆𝑤 .𝑒) : 𝑥 :𝑡𝑥 → 𝑡 and ⊢𝑤 Γ then there exists
249
      𝑦 ∉ dom(()Γ) such that 𝑦:𝑡𝑥, Γ ⊢ 𝑒 [𝑦/𝑤] : 𝑡 [𝑦/𝑥]. If Γ ⊢ (Λ𝑎 1 :𝑘 1 .𝑒) : ∀𝑎:𝑘.𝑡 and ⊢𝑤 Γ then exists
250
      𝑎 ′ ∉ dom(()Γ) such that 𝑎 ′ :𝑘, Γ ⊢ 𝑒 [𝑎 ′ /𝑎 1 ] : 𝑡 [𝑎 ′ /𝑎].
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
      , Vol. 1, No. 1, Article . Publication date: July 2022.
This figure "system_rf.png" is available in "png" format from:

        http://arxiv.org/ps/2207.05617v1
