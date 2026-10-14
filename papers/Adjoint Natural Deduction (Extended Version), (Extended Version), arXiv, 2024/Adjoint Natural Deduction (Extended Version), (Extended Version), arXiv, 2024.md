                                                                 Adjoint Natural Deduction
                                                                    (Extended Version)

                                                          Junyoung Jang                            Sophia Roshal
arXiv:2402.01428v1 [cs.LO] 2 Feb 2024




                                                         McGill University                   Carnegie Mellon University
                                                        Frank Pfenning                               Brigitte Pientka
                                                   Carnegie Mellon University                       McGill University

                                                                               February 2, 2024


                                                                                     Abstract
                                                 Adjoint logic is a general approach to combining multiple logics with different
                                             structural properties, including linear, affine, strict, and (ordinary) intuitionistic log-
                                             ics, where each proposition has an intrinsic mode of truth. It has been defined in the
                                             form of a sequent calculus because the central concept of independence is most clearly
                                             understood in this form, and because it permits a proof of cut elimination following
                                             standard techniques.
                                                 In this paper we present a natural deduction formulation of adjoint logic and show
                                             how it is related to the sequent calculus. As a consequence, every provable proposition
                                             has a verification (sometimes called a long normal form). We also give a computational
                                             interpretation of adjoint logic in the form of a functional language and prove proper-
                                             ties of computations that derive from the structure of modes, including freedom from
                                             garbage (for modes without weakening and contraction), strictness (for modes disal-
                                             lowing weakening), and erasure (based on a preorder between modes). Finally, we
                                             present a surprisingly subtle algorithm for type checking.


                                        1 Introduction
                                        A substructural logic provides fine control over the use of assumptions during reasoning. It
                                        usually does so by denying the general sequent calculus rules of contraction (which permits
                                        an antecedent to be used more than once) and weakening (which permits an antecedent
                                        not to be used). Instead, these rules become available only for antecedents of the form
                                        !A. Ever since the inception of linear logic [Girard, 1987], researchers have found appli-
                                        cations in programming languages, for example, to avoid garbage collection [Girard and
                                        Lafont, 1987], soundness of imperative update [Wadler, 1990], the chemical abstract ma-
                                        chine [Abramsky, 1993], and session-typed communication [Caires and Pfenning, 2010,
                                        Wadler, 2012], to name just a few.
                                            Besides linear logic, there are other substructural logics and type systems of interest.
                                        For example, affine logic denies general contraction but allows weakening and is the basis



                                        E XTENDED V ERSION                                                                F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                  2


for the type system of Alms [Tov and Pucella, 2011] (an affine functional language) and
Rust (an imperative language aimed at systems programming).
    If we deny weakening but accept contraction we obtain strict logic (a variant of rele-
vance logic) where every assumption must be used at least once. On the programming
language side, this corresponds to strictness, which allows optimizations in otherwise non-
strict functional languages such as Haskell [Mycroft, 1980]. Interestingly, Church’s original
λI calculus [Church, 1941] was also strict in this sense.
    The question arises how we can combine such features, both in logics and in type sys-
tems. Recently, this question has been tackled through graded or quantitative type sys-
tems (see for example, Atkey [2018], Moon et al. [2021], Choudhury et al. [2021], Wood
and Atkey [2022], Abel et al. [2023]). The essential idea is to track and reason explicitly
about the usage of a given assumption through grades. This provides very fine-grained
control and allows us to, for example, model linear, strict, and unrestricted usage of as-
sumptions through graded modalities. In this paper, we pursue an alternative taking a
proof-theoretic view with the goal of building a computational interpretation. There are
three possible options that emerge from existing proof-theoretic explorations that could
serve as a foundation of such a computational interpretation. The first one is by embedding.
For example, we can embed (structural) intuitionistic logic in linear logic writing !A ⊸ B
for A → B. Similarly, we can embed affine logic in linear logic by mapping hypotheses A to
A N 1 so they do not need to be used. The difficulties with such embeddings is that, often,
they neither respect proof search properties such as focusing [Andreoli, 1992] nor do they
achieve a desired computational interpretation.
    A second approach is taken by subexponential linear logic [Nigam and Miller, 2009,
Nigam et al., 2016, Kanovich et al., 2018] that defines multiple subexponential modali-
ties !m A, where each mode m has a specific set of structural properties. As in linear logic,
all inferences are carried out on linear formulas, so while it resolves some of the issues
with embeddings, it still requires frequent movement into the linear layer using explicit
subexponentials.
    We pursue a third approach, pioneered by Benton [1994a] who symmetrically com-
bined (structural) intuitionistic logic with (purely) linear intuitionistic logic. He employs
two adjoint modalities that switch between the two layers and works out the proof the-
oretic and categorical semantics. This approach has the advantage that one can natively
reason and compute within the individual logics, so we preserve not only provability but
the fine structure of proofs and proof reduction from each component. This has been gen-
eralized in prior work [Reed, 2009, Pruiksma et al., 2018] by incorporating from subexpo-
nential linear logic the idea to have a preorder between modes m ≥ k that must be compat-
ible with the structural properties of m and k (explained in more detail in Section 2). This
means we can now also model intuitionistic S4 [Pfenning and Davies, 2001] and lax logic
[Benton et al., 1998], representing comonadic and monadic programming, respectively. We
hence arrive at a unifying calculus firmly rooted in proof theory that is more general than
previous graded modal type systems in that we can construct monads as well as comonads.
We will briefly address dependently typed variations of the adjoint approach in Section 8.
    Most substructural logics and many substructural type systems are most clearly for-
mulated as sequent calculi. However, natural deduction has not only an important foun-
dational role [Gentzen, 1935, Prawitz, 1965, Dummett, 1991], it also has provided a simple


E XTENDED V ERSION                                                         F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                   3


and elegant notation for functional programs through the Curry-Howard correspondence
[Howard, 1969]. We therefore develop a system of natural deduction for adjoint logic that,
in a strong sense, corresponds to the original sequent formulation. It turns out to be sur-
prisingly subtle because we have to manage not only the substructural properties that may
be permitted or not, but also respect the preorder between modes. We show that the our
calculus satisfies some expected properties like substitution and has a natural notion of ver-
ification that corresponds to proofs in long normal form, satisfying a subformula property.
     In order to illustrate computational properties, we also give an abstract machine and
show the consequences of the mode structure: freedom from garbage for linear modes
(that is, modes admitting neither weakening nor contraction), strictness for modes that do
not admit weakening, and erasure for modes that a final value may not depend on, based
on the preorder of modes. We close with an algorithmic type checker for our language
which, again, is surprisingly subtle.


2 Adjoint Sequent Calculus
We briefly review the adjoint sequent calculus from Pruiksma et al. [2018]. We start with
a standard set of possibly substructural propositions, indexing each with a mode of truth,
denoted by m, k, n, r. Propositions are perhaps best understood by using their linear mean-
ing as a guide, so we uniformly use the notation of linear logic. Also, for programming
convenience, we generalize the usual binary and nullary disjunction (A ⊕ B and 0) and
conjunction (A N B and ⊤) by using labeled disjunction ⊕{ℓ : Aℓm }ℓ∈L and conjunction
N{ℓ : Aℓm }ℓ∈L . From the linear logical perspective, these are internal and external choice,
respectively; from the programming perspective they are sums and products. We write Pm
for atomic propositions of mode m.

   Propositions Am , Bm ::= Pm | Am ⊸ Bm | N{ℓ : Aℓm }ℓ∈L | ↑mk Ak   (negative)
                            | Am ⊗ Bm | 1m | ⊕{ℓ : Aℓm }ℓ∈L | ↓nm An (positive)
   Contexts       Γ          ::= · | Γ, x : Am                               (unordered)

Each mode m comes with a set σ(m) ⊆ {W, C} of structural properties, where W stands for
weakening and C stands for contraction. We further have a preorder m ≥ r that specifies
that a proof of the succedent Cr may depend on an antecedent Am . This is enforced using
the presupposition that in a sequent Γ ⊢ Cr , every antecedent Am in Γ must satisfy m ≥ r,
written as Γ ≥ r. We have the additional stipulation of monotonicity, namely that m ≥
k implies σ(m) ⊇ σ(k). This is required for cut elimination to hold. Furthermore, we
presuppose that in ↑m                                  n
                      k Ak we have m ≥ k and for ↓m An we have n ≥ m. Also, contexts
may not have any repeated variables and we will implicitly apply variable renaming to
maintain this presupposition. Finally, we abbreviate ·, x : A as just x : A.
    In preparation for natural deduction, instead of explicit rules of weakening and con-
traction (see [Pruiksma et al., 2018] for such a system) we have a context merge operation
Γ1 ; Γ2 . Since, as usual in the sequent calculus, we read the rules bottom-up, it actually
describes a nondeterministic split of the context that is pervasive in the presentations of




E XTENDED V ERSION                                                          F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                        4


linear logic [Andreoli, 1992].

        (Γ1 , x : Am )   ;   (Γ2 , x : Am )   =   (Γ1 ; Γ2 ), x : Am provided C ∈ σ(m)
        (Γ1 , x : Am )   ;   Γ2               =   (Γ1 ; Γ2 ), x : Am provided x 6∈ dom(Γ2 )
                   Γ1    ;   (Γ2 , x : Am )   =   (Γ1 ; Γ2 ), x : Am provided x ∈6 dom(Γ1 )
                   (·)   ;   Γ2               =   Γ2
                   Γ1    ;   (·)              =   Γ1

Note that the context merge is a partial operation, which prevents, for example, the use of
an antecedent without contraction in both premises of the ⊗R rule.
   The complete set of rules can be found in Figure 1. In the rules, we write ΓW for a
context in which weakening can be applied to every antecedent, that is, W ∈ σ(m) for
every antecedent x : Am . Also, as is often the case in presentations of the sequent calculus,
we omit explicit variable names that tag antecedents. We only discuss the rules for ↓nm An
because they illustrate the combined reasoning about structural properties and modes.
   First, the ↓R rule.
                                    Γ′ ≥ n Γ′ ⊢ An
                                                       ↓R
                                     ΓW ; Γ′ ⊢ ↓nm An
 Because we presuppose the conclusion is well-formed, we know ΓW ; Γ′ ≥ m since ↓nm An
has mode m. Again, by presupposition n ≥ m and we have to explicitly check that Γ′ ≥ n
because it doesn’t follow from knowing that ΓW ; Γ′ ≥ m. There may be some antecedents
Ak in the conclusion such that k 6≥ n. If the mode k admits weakening, we can sort them
into ΓW . If it does not, then the rule is simply not applicable.
    On to the ↓L rule:
                                          Γ, An ⊢ Cr
                                                        ↓L
                                        Γ ; ↓nm An ⊢ Cr
 By presupposition on the conclusion, we know Γ ; ↓nm An ≥ r which means that Γ ≥ r and
m ≥ r. Since n ≥ m we have n ≥ r by transitivity, so Γ, An ≥ r and we do not need any
explicit check. The formulation of the antecedents in the conclusion Γ ; ↓nm An means that if
mode m admits contraction, then the antecedent ↓nm An may also occur in Γ, that is, it may
be preserved by the rule. If m does not admit contraction, this occurrence of ↓nm An is not
carried over to the premise.
    This implicit sequent calculus satisfies the expected theorems, due to Reed [2009],
Pruiksma et al. [2018] and, most closely reflecting the precise form of our formulation,
Pruiksma [2024]. They follow standard patterns, modulated by the substructural proper-
ties and the preorder on modes.

Theorem 1 (Admissibility of Weakening and Contraction) The following are admissible:

           ΓW ≥ m Γ ⊢ Am                           C ∈ σ(m)    Γ, Am , Am ⊢ Cr
                                   weaken                                        contract
              ΓW ; Γ ⊢ Am                                  Γ, Am ⊢ Cr

Theorem 2 (Admissibility of Cut and Identity)

 (i) In the system without cut, cut is admissible.

E XTENDED V ERSION                                                                F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                              5


                                              Γ≥m≥r        Γ ⊢ Am        Γ′ , Am ⊢ Cr
                                 id                                                     cut
               ΓW ; Am ⊢ Am                               Γ ; Γ ′ ⊢ Cr


                                           Γ, Am ⊢ Bm
                                                           ⊸R
                                          Γ ⊢ Am ⊸ Bm

                               Γ ≥ m Γ ⊢ Am         Γ ′ , Bm ⊢ Cr
                                                                    ⊸L
                                      Γ ; Γ′ ; Am ⊸ Bm ⊢ Cr

                   Γ ⊢ Aℓm     (∀ℓ ∈ L)               Γ, Aℓm ⊢ Cr        (ℓ ∈ L)
                                          NR                                       NL
                   Γ ⊢ N{ℓ : Aℓm }ℓ∈L                Γ ; N{ℓ : Aℓm }ℓ∈L ⊢ Cr

                     Γ ⊢ Am      Γ ′ ⊢ Bm                 Γ, Am , Bm ⊢ Cr
                                              ⊗R                                  ⊗L
                      Γ ; Γ′ ⊢ Am ⊗ Bm                  Γ ; Am ⊗ Bm ⊢ Cr

                                                          Γ ⊢ Cr
                                            1R                       1L
                                ΓW ⊢ 1m              Γ ; 1m ⊢ Cr

                    Γ ⊢ Aℓm     (ℓ ∈ L)              Γ, Aℓm ⊢ Cr     (∀ℓ ∈ L)
                                          ⊕R                                       ⊕L
                   Γ ⊢ ⊕{ℓ : Aℓm }ℓ∈L                Γ ; ⊕{ℓ : Aℓm }ℓ∈L ⊢ Cr


                              Γ ⊢ Ak                k≥r     Γ, Ak ⊢ Cr
                                         ↑R                                 ↑L
                           Γ ⊢ ↑m
                                k Ak                 Γ ; ↑m
                                                          k Ak ⊢ Cr

                         Γ′ ≥ n Γ′ ⊢ An                    Γ, An ⊢ Cr
                                               ↓R                            ↓L
                          ΓW ; Γ′ ⊢ ↓nm An                Γ ; ↓nm An ⊢ Cr

                          Figure 1: Implicit Adjoint Sequent Calculus


 (ii) In the system with identity restricted to atoms Pm , the general identity is admissible.

    We call a proof cut-free if it does not contain cut and long if the identity is restricted to
atomic propositions P . It is an immediate consequence of Theorem 2 that every derivable
sequent has a long cut-free proof. The subformula property of cut-free proofs directly
implies that a cut-free proof of a sequent Γm ⊢ Am where all subformulas are of mode m
is directly a proof in the logic captured by the mode m. Moreover, an arbitrary proof can
be transformed into one of this form by cut elimination. These strong conservative extension
properties are a hallmark of adjoint logic.
    Since our main interest lies in natural deduction, we consider only three examples.

Example 3 (G3) We obtain the standard sequent calculus G3 [Kleene, 1952] for intutionistic logic

E XTENDED V ERSION                                                                      F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                              6


with a single mode U. All side conditions are automatically satisfied since U ≥ U.

Example 4 (LNL and DILL) By specializing the rules to two modes, U and L with the order
U > L, we obtain a minor variant of LNL in its parsimonious presentation [Benton, 1994b].
Our notation is F X = ↓UL X and GA = ↑UL A. Significant here is that we do not just model
provability, but the exact structure of proofs except that our structural rules remain implicit.
    We obtain the sequent calculus formulation of dual intuitioninstic linear logic (DILL) [Barber,
1996, Chang et al., 2003] by restricting the formulas of mode U so that they only contain ↑UL AL . In
this version we have !A = ↓UL ↑UL A. Again, the rules of dual intuitionistic linear logic are modeled
precisely.

Example 5 (Intuitionistic Subexponential Linear Logic) Subexponential linear logic [Nigam
and Miller, 2009, Nigam et al., 2016] also uses a preorder of modes, each of which permits specific
structural rules. We obtain a formulation of intuitionistic subexponential linear logic by adding
a new distinguished mode L with m ≥ L for all given subexponential modes m, retaining all the
other relations. We further restrict all modes m except for L to contain only ↑m
                                                                               L AL , forcing all logical
inferences to take place at mode L.
    Compared to Chaudhuri [2010] our system does not contain ?A and is not focused; compared to
Kanovich et al. [2017], our base logic is linear rather than ordered. Also, all of our structural rules
are implicit.


3 Adjoint Natural Deduction
Substructural sequent calculi have recently found interesting computational interpretations
[Caires and Pfenning, 2010, Wadler, 2012, Caires et al., 2016, Pfenning and Pruiksma, 2023,
Pruiksma and Pfenning, 2022], including adjoint logic [Pruiksma and Pfenning, 2021]. In
this paper, we look instead at functional interpretations, which are most closely related to
natural deduction. Some guide is provided by natural deduction systems for linear logic
(see, for example, Abramsky [1993], Benton et al. [1993], Troelstra [1995]), but already they
are not entirely straightforward. For example, some of these calculi do not satisfy sub-
ject reduction. The interplay between modes and substructural properties creates some
further complications. The closest blueprint to follow is probably Benton’s [1994b, Figure
8], but his system does not exhibit the full generality of adjoint logic and is also not quite
“parsimonious” in the sense of the LNL sequent calculus.
    In the interest of economy, we present the calculus with proof terms and two bidirec-
tional typing judgments, ∆ ⊢ e ⇐= Am (expression e checks against Am ) and ∆ ⊢ s =⇒
Am (expression s synthesizes Am ). The syntax for expressions can be found in Figure 2, the
rules in Figure 3. The bidirectional nature will allow us to establish a precise relationship
to the sequent calculus (Section 4), but it does not immediately yield a type checking al-
gorithm since the context merge operation is highly nondeterministic when used to split
contexts. An algorithmic system can be found in Section 7.
    We obtain the vanilla typing judgment by replacing both checking and synthesis judg-
ments with ∆ ⊢ e : A, dropping the rules ⇒/⇐ and ⇐/⇒, and removing the syntactic
form (e : Am ). We further obtain a pure natural deduction system by removing the proof



E XTENDED V ERSION                                                                  F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                     7


               Checkable Exps.          e ::= λx. e                           (⊸)
                                            | {ℓ ⇒ eℓ }ℓ∈L                    (N)
                                            | susp e                          (↑)
                                           |     (e1 , e2 )                   (⊗)
                                           |     match s ((x1 , x2 ) ⇒ e′ )
                                           |     ()                           (1)
                                           |     match s (( ) ⇒ e′ )
                                           |     ℓ(e)                         (⊕)
                                           |     match s (ℓ(x) ⇒ eℓ )ℓ∈L
                                           |     down e                 (↓)
                                           |     match s (down x ⇒ e′ )
                                           |     s

               Synthesizable Exps. s ::=         x
                                       |         se                           (⊸)
                                       |         s.ℓ                          (N)
                                       |         force s                      (↑)
                                       |         (e : Am )

                Figure 2: Expressions for Bidirectional Natural Deduction

terms, although uses of the hypothesis rule then need to be annotated with variables in
order to avoid any ambiguities.
   The rules maintain a few important invariants, particularly independence:
  (i) ∆ ⊢ e ⇐= Am presupposes ∆ ≥ m
 (ii) ∆ ⊢ s =⇒ Am presupposes ∆ ≥ m
This is somewhat surprising because we think of the synthesis judgment s =⇒ Am as pro-
ceeding top-down rather than bottom-up. Indeed, there are other choices with dependence
and structural properties being checked in different places. We picked this particular form
because we want general typing e : Am to arise from collapsing the checking/synthesis
distinction. This means that the two rules ⇒/⇐ and ⇐/⇒ should have no conditions be-
cause those would disappear. The algorithmic system in Section 7 checks the conditions in
different places.
    As an example of interesting rules we revisit ↓nm An (where n ≥ m is presupposed). The
introduction rule of natural deduction mirrors the right rule of the sequent calculus, which
is the case throughout.
               Γ′ ≥ n Γ′ ⊢ An                    ∆′ ≥ n      ∆′ ⊢ e ⇐= An
                                   ↓R                                          ↓I
                ΓW ; Γ′ ⊢ ↓nm An               ∆W ; ∆′ ⊢ down e ⇐= ↓nm An
As is typical for these translations, the elimination rules turns the left rule “upside down”
because (like all rules in natural deduction) the principal formula is on the right-hand

E XTENDED V ERSION                                                             F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                             8



                 ∆ ⊢ s =⇒ Am                            ∆ ⊢ e ⇐= Am
                                      ⇒/⇐                                     ⇐/⇒
                 ∆ ⊢ s ⇐= Am                        ∆ ⊢ (e : Am ) =⇒ Am

                                                                hyp
                                     ∆W ; x : Am ⊢ x =⇒ Am


                                      ∆, x : Am ⊢ e ⇐= Bm
                                                                ⊸I
                                  ∆ ⊢ λx. e ⇐= Am ⊸ Bm

                         ∆ ⊢ s =⇒ Am ⊸ Bm             ∆′ ⊢ e ⇐= Am
                                                                       ⊸E
                                      ∆ ; ∆′ ⊢ s e =⇒ Bm

        ∆ ⊢ eℓ ⇐= Aℓm      (∀ℓ ∈ L)                     ∆ ⊢ s =⇒ N{ℓ : Aℓm }ℓ∈L       (ℓ ∈ L)
                                               NI                                                NE
    ∆ ⊢ {ℓ ⇒ eℓ }ℓ∈L ⇐= N{ℓ : Aℓm }ℓ∈L                            ∆ ⊢ s.ℓ =⇒ Aℓm

                     ∆ ⊢ e ⇐= Ak                     ∆′ ≥ m    ∆′ ⊢ s =⇒ ↑m
                                                                          k Ak
                                          ↑I                                        ↑E
              ∆ ⊢ susp e ⇐= ↑m
                             k Ak                     ∆W ; ∆′ ⊢ force s =⇒ Ak


                             ∆ ⊢ e1 ⇐= Am           ∆′ ⊢ e2 ⇐= Bm
                                                                      ⊗I
                                ∆ ; ∆′ ⊢ (e1 , e2 ) ⇐= Am ⊗ Bm

         ∆ ⊢ s =⇒ Am ⊗ Bm            ∆≥m≥r          ∆′ , x1 : Am , x2 : Bm ⊢ e′ ⇐= Cr
                                                                                         ⊗E
                         ∆ ; ∆′ ⊢ match s ((x1 , x2 ) ⇒ e′ ) ⇐= Cr

                                        ∆ ⊢ s =⇒ 1m       ∆≥m≥r            ∆′ ⊢ e′ ⇐= Cr
                           1I                                                               1E
        ∆W ⊢ ( ) ⇐= 1m                         ∆ ; ∆′ ⊢ match s (( ) ⇒ e′ ) ⇐= Cr

                                         ∆ ⊢ e ⇐= Aℓm
                                                                 ⊕I
                                 ∆ ⊢ ℓ(e) ⇐= ⊕{ℓ : Aℓm }ℓ∈L

       ∆ ⊢ s =⇒ ⊕{ℓ : Aℓm }ℓ∈L        ∆≥m≥r           ∆′ , x : Aℓm ⊢ eℓ ⇐= Cr    (∀ℓ ∈ L)
                                                                                            ⊕E
                         ∆ ; ∆′ ⊢ match s (ℓ(x) ⇒ eℓ )ℓ∈L ⇐= Cr

  ∆′ ≥ n ∆′ ⊢ e ⇐= An                  ∆ ⊢ s =⇒ ↓nm An     ∆≥m≥r            ∆′ , x : An ⊢ e′ ⇐= Cr
                                ↓I                                                                    ↓E
∆W ; ∆′ ⊢ down e ⇐= ↓nm An                     ∆ ; ∆′ ⊢ match s (down x ⇒ e′ ) ⇐= Cr


                     Figure 3: Implicit Bidirectional Natural Deduction




E XTENDED V ERSION                                                                F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                    9


side of judgment, not the left as in the sequent calculus. This means we now have some
conditions to check.
      Γ, An ⊢ Cr             ∆ ⊢ s =⇒ ↓nm An     ∆≥m≥r         ∆′ , x : An ⊢ e′ ⇐= Cr
                      ↓L                                                                ↓E
    Γ ; ↓nm An ⊢ Cr                 ∆ ; ∆′ ⊢ match s (down x ⇒ e′ ) ⇐= Cr

 ∆ ≥ m is needed to enforce independence on the first premise. m ≥ r together with
n ≥ m enforces independence on the second premise. Similar restrictions appear in the
other elimination rules for the positive connectives (⊗, 1, ⊕).
   In general we see the following patterns in the correctness proofs below:

   • The identity corresponds to ⇒/⇐

   • Cut corresponds to ⇐/⇒

   • Right rules correspond to introduction rules

   • Left rules correspond to upside-down elimination rules

        – For negative connectives (⊸, N, ↑) they are just reversed
        – For positive connectives (⊗, 1, ⊕, ↓) in addition a new hypothesis is introduced
          in a second premise

From the last point we see that the hypothesis x : Am should just be read as x =⇒ Am .
    We often say a natural deduction is normal, which means that it cannot be reduced, but
under which collection of reductions? The difficulty here is that rewrite rules that reduce
an introduction of a connective immediately followed by its elimination are not sufficient
to achieve deductions that are analytic in the sense that they satisfy the subformula prop-
erty. To obtain analytic deductions, we have to add permuting conversions.
    We follow a different approach by directly characterizing verifications [Dummett, 1991,
Martin-Löf, 1983], which are proofs that can be seen as constructed by applying introduc-
tion rules bottom-up and elimination rules top-down. By definition, verifications satisfy
the subformula property and are therefore analytic and a suitable “normal form” even
without defining a set of reductions.
    How does this play out here? It turns out that if ∆ ⊢ e ⇐= Am then the corresponding
proof of Am (obtained by erasure of expressions) is a verification if the ⇐/⇒ rule is disal-
lowed and the ⇒/⇐ rule is restricted to atomic propositions P . By our above correspon-
dence that corresponds precisely to a cut-free sequent calculus proof where the identity is
restricted to atomic propositions. Proof-theoretically, the meaning of a proposition is de-
termined by its verifications, which, by definition, only decompose the given proposition
into its components. Compare this with general proofs that do not obey such a restriction.
    In the next section we will prove that every proposition that has a proof also has a
verification by relating the sequent calculus and natural deduction.

Example 6 (Church’s λI calculus) Church [1941, Chapter II] introduced the λI calculus in
which each bound variable requires at least one occurrence. We obtain the simply-typed λI cal-
culus with one mode S with σ(S) = {C} and using AS ⊸ BS as the only type constructor.


E XTENDED V ERSION                                                          F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                       10


    Similarly, we obtain the simply-typed λ-calculus with a single mode U with σ(U) = {W, C}
and the simply-typed linear λ-calculus with a single mode L with σ(L) = { }, using AL ⊸ BL as
the only type constructor.

Example 7 (Intuitionistic Natural Deduction) We obtain (structural) intutionistic natural de-
duction with a single mode U with σ(U) = {W, C}, where we can define A ∨ B = ⊕{inl : A, inr :
B} and ⊥ = ⊕{ }, A ∧ B = N{π1 : A, π2 : B} and ⊤ = N{ } and A → B = A ⊸ B.

Example 8 (Intuitionistic S4) We obtain the fragment of intuitionistic S4 in its dual formulation
[Pfenning and Davies, 2001] without possibility (♦A) with two modes V and U with V > U and
σ(V) = σ(U) = {W, C}. As in the DILL example of the adjoint sequent calculus, the mode V is
inhabited only by types ↑VU AU and we define AU = ↓VU ↑VU AU , which is a comonad. The judgment
∆ ; Γ ⊢ C true with valid hypotheses ∆ and true hypothesis Γ is modeled by ∆V , ΓU ⊢ CU .
    The structure of verifications is modeled almost exactly with one small exception: we allow the
form ∆V ⊢ CV . Because any proposition BV = ↑VU AU , there is only one applicable rule to construct
a verification of this judgment: ↑I (which, not coincidentally, is invertible).

Example 9 (Lax Logic) We obtain natural deduction for lax logic [Benton et al., 1998, Pfenning
and Davies, 2001] with two modes, U and X, with U > X and σ(U) = σ(X) = {W, C}. The mode
X is inhabited only by ↓UX AU . We define AU = ↑UX ↓UX AU , which is a strong monad [Benton et al.,
1998].
    We model the rules of Pfenning and Davies [2001] exactly, except that we allow hypotheses BX ,
which must have the form ↓UX AU . We can eagerly apply ↓E to obtain AU , which again does not lose
completeness by the invertibility of ↓L in the sequent calculus.
    We can also obtain linear versions of these relationships following [Benton and Wadler, 1996],
although the term calculi do not match up exactly.


4 Relating Sequent Calculus and Natural Deduction
Rather than trying to find a complete set of proof reductions for natural deduction, we
translate a proof to the sequent calculus, apply cut and identity elimination, and then
translate the resulting proof back to natural deduction. This is not essential, but it simul-
taneously proves the soundness and completeness of natural deduction for adjoint logic
and the completeness of verifications. This allows us to focus on the computational inter-
pretation in Section 5 that is a form of substructural functional programming.
    For completeness of natural deduction, one might expect to prove that Γ ⊢ C in the
sequent calculus implies Γ ⊢ e ⇐= C in natural deduction. While this holds, a direct
proof would not generate a verification from a cut-free proof. Intuitively, the way the
proof proceeds instead is to take a sequent x1 : A1 , . . . , xn : An ⊢ C (ignoring modes for
the moment) and annotate each antecedent with a synthesizing term and the succedent
with an expression s1 =⇒ A1 , . . . , sn =⇒ An ⊢ e ⇐= C. This means we have to account
for the variables in si , and we do this with a substitution θ assigning synthesizing terms
to each antecedent in Γ. We therefore define substitutions as mapping from variables to
synthesizing terms.
                              Substitutions θ ::= · | θ, x 7→ s

E XTENDED V ERSION                                                              F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                     11


We type substitutions with the judgment ∆ ⊢ θ =⇒ Γ, where ∆ contains the free vari-
ables in θ. This judgment must respect independence and the structural properties of each
antecedent in Γ, as defined by the following rules:

                                      ∆ ⊢ θ =⇒ Γ      ∆′ ≥ m     ∆′ ⊢ s =⇒ Am
                · ⊢ (·) =⇒ (·)           ∆ ; ∆′ ⊢ (θ, x 7→ s) =⇒ (Γ, x : Am )

 We will use silently that if ∆ ⊢ θ =⇒ Γ and Γ ≥ m then ∆ ≥ m.
    We write e(x) and s′ (x) for terms with (possibly multiple, possibly no) occurrences of
x and e(s) and s′ (s) for the result of substituting s for x, respectively. Because variables
x : A synthesize their types x =⇒ A, the following admissible rules are straightforward
assuming the premises satisfy our presuppositions.

Theorem 10 (Substitution Property) The following are admissible:

                     ∆ ⊢ s =⇒ Am       ∆′ , x : Am ⊢ e(x) ⇐= Cr
                                                                    subst/⇐
                                 ∆ ; ∆′ ⊢ e(s) ⇐= Cr

                     ∆ ⊢ s =⇒ Am       ∆′ , x : Am ⊢ s′ (x) =⇒ Bk
                                                                    subst/⇒
                                 ∆ ; ∆′ ⊢ s′ (s) =⇒ Bk

Proof: By a straightforward simultaneous rule induction on the second given derivation.
In some cases we need to apply monotonicity. For example, if m admits contraction and
∆ ≥ m, then each hypothesis in ∆ must also admit contraction.                        

Lemma 11 (Substitution Split) If ∆ ⊢ θ =⇒ (Γ; Γ′ ) then there exists θ1 and θ2 and ∆1 and ∆2
such that ∆ = ∆1 ; ∆2 and ∆1 ⊢ θ1 =⇒ Γ and ∆2 ⊢ θ2 =⇒ Γ′ .

Proof: By case analysis on the definition of context merge operation and induction on
∆ ⊢ θ =⇒ (Γ; Γ′ ). We rely on associativity and commutativity of context merge. We show
two cases.

Case: (Γ1 , x : Am ) ; (Γ2 , x : Am ) = (Γ1 ; Γ2 ), x : Am and C ∈ σ(m)

                           ∆ ⊢ θ12 =⇒ Γ1 ; Γ2      ∆′ ≥ k   ∆′ ⊢ s =⇒ Am
                             ∆ ; ∆′ ⊢ (θ12 , x 7→ s) =⇒ (Γ1 ; Γ2 ), x : Am

      ∆1 ⊢ θ1 =⇒ Γ1 and
      ∆2 ⊢ θ2 =⇒ Γ2 and
      ∆ = ∆1 ; ∆2                                                                         by IH
      ∆1 ; ∆′ ⊢ θ1 , x 7→ s =⇒ Γ1 , x : Am                                               by rule
      ∆2 ; ∆′ ⊢ θ2 , x 7→ s =⇒ Γ2 , x : Am                                               by rule
      since C ∈ σ(m) and ∆′ ≥ m, we have C ∈ σ(k) for any Bk ∈ ∆′               by monotonicity
      (∆1 ; ∆′ ) ; (∆2 ; ∆′ ) = (∆1 ; ∆2 ) ; ∆′ = ∆ ; ∆′                        by previous line



E XTENDED V ERSION                                                              F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                        12


Case: Γ1 ; (Γ2 , x : Am ) = (Γ1 ; Γ2 ), x : Am and x 6∈ dom(Γ1 )
                           ∆ ⊢ θ12 =⇒ Γ1 ; Γ2      ∆′ ≥ k       ∆′ ⊢ s =⇒ Am
                           ∆ ; ∆′ ⊢ (θ12 , x 7→ s) =⇒ ((Γ1 ; Γ2 ), x 7→ Am )

      ∆1 ⊢ θ1 =⇒ Γ1 and
      ∆2 ⊢ θ2 =⇒ Γ2 and
      ∆ = ∆1 ; ∆2                                                                            by IH
      ∆2 ; ∆′ ⊢ θ2 , x 7→ s =⇒ Γ2 , x 7→ Am                                                 by rule
      ∆1 ; (∆2 ; ∆′ ) = (∆1 ; ∆2 ) ; ∆′ = ∆ ; ∆′                 by associativity of context merge

                                                                                                  

   Now we have the pieces in place to prove the translation from the sequent calculus to
natural deduction.

Theorem 12 (From Sequent Calculus to Natural Deduction)
If Γ ⊢ Ar and ∆ ⊢ θ =⇒ Γ then ∆ ⊢ e ⇐= Ar for some e.

Proof: By rule induction on the derivation D of Γ ⊢ Ar and applications of inversion on
the definition of substitution. We present several indicative cases. In this proof we write
out the variables labeling the antecedents in sequents to avoid ambiguities.

Case: D ends in the identity.
                                                                   id
                                     D=      ΓW ; x : Am ⊢ Am

      ∆ ⊢ θ =⇒ (ΓW ; x : Am )                                                                Given
      θ = (θW , x 7→ s)                                                                By inversion
      ∆ = (∆W ; ∆′ ) with ∆W ⊢ θW =⇒ ΓW and ∆′ ⊢ s =⇒ A                             By context split
      ∆W satisfies weakening                                                       By monotonicity
      ∆′ ⊢ s ⇐= A                                                                     By rule ⇒/⇐
      ∆W ; ∆′ ⊢ s ⇐= A                                                               By weakening
      ∆ ⊢ s ⇐= A                                                               Since ∆ = (∆W ; ∆′ )

Case: D ends in cut.
                                                  D1                D2
                                Γ1 ≥ m ≥ r     Γ1 ⊢ Am      Γ2 , x : Am ⊢ Cr
                                                                               cut
                        D=                     Γ 1 ; Γ 2 ⊢ Cr

      ∆ ⊢ θ =⇒ (Γ1 ; Γ2 )                                                             Given
      ∆ = (∆1 ; ∆2 ), θ = (θ1 , θ2 ) with ∆1 ⊢ θ1 =⇒ Γ1 and ∆2 ⊢ θ2 =⇒ Γ2 By context split
      ∆1 ⊢ e1 ⇐= Am                                                             By IH on D1
      ∆1 ⊢ (e1 : Am ) =⇒ Am                                                    by rule ⇐/⇒
      ∆2 , x : Am ⊢ (θ2 , x 7→ x) =⇒ (Γ2 , x : Am )                           By subst. rule
      ∆2 , x : Am ⊢ e2 (x) ⇐= Cr                                                By IH on D2
      ∆1 ; ∆2 ⊢ e2 (e1 : Am ) ⇐= Cr                            By substitution (Theorem 10)

E XTENDED V ERSION                                                                F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                     13


Case: D ends in ↑L.
                                                       D′
                                        k≥r     Γ, y : Ak ⊢ Cr
                                                                 ↑L
                                D=        Γ ; x : ↑m
                                                   k Ak ⊢ Cr

     We consider two subcases: x : ↑m                 m
                                    k Ak ∈ Γ and x : ↑k Ak 6∈ Γ.

     Subcase: x : ↑m                                         m           ′       m
                   k Ak ∈ Γ and so C ∈ σ(m). Hence, Γ ; x : ↑k Ak = Γ = Γ , x : ↑k Ak .

          Γ ; x : ↑m
                   k Ak = Γ ≥ r                                         by presupposition
          m≥r                                                       since (x : ↑m
                                                                                k Ak )m ∈ Γ
          ∆ ⊢ θ =⇒ Γ                                                        by assumption
          ∆1 ⊢ θ ′ =⇒ Γ′ and ∆2 ⊢ s =⇒ ↑m k Ak and ∆2 ≥ m      by inversion on subst. rule
                                                     where ∆ = ∆1 ; ∆2 and θ = (θ ′ , x 7→ s)
          ∆2 ⊢ force s =⇒ Ak                                                     by rule ↑E
          ∆ ; ∆2 ⊢ (θ, y 7→ force s) =⇒ (Γ, y : Ak )                         by subst. rule
          ∆ ; ∆2 ⊢ e ⇐= Cr for some e                                          by IH on D ′
          ∆ ; ∆2 = ∆       since C ∈ σ(m) and ∆2 ≥ m, we have C ∈ σ(j) for any Bj ∈ ∆2
          ∆ ⊢ e ⇐= Cr                                                     by previous line
     Subcase: x : ↑m
                   k Ak ∈
                        / Γ.
          Γ, x : ↑m
                  k Ak ≥ r                                                by presupposition
          Γ ≥ r and m ≥ r                                                   by previous line
                                m
          ∆ ⊢ θ =⇒ (Γ, x : ↑k Ak )                                           by assumption
          ∆1 ⊢ θ ′ =⇒ Γ and ∆2 ⊢ s =⇒ ↑m     A
                                           k k   and   ∆ 2 ≥ m   by inversion on subst. rule
                                                       where ∆ = ∆1 ; ∆2 and θ = (θ ′ , x 7→ s)
          ∆2 ⊢ force s =⇒ Ak                                                     by rule ↑E
          ∆1 ; ∆2 ⊢ (θ ′ , x 7→ force s) =⇒ (Γ, y : Ak )                      by subst. rule
          ∆1 ; ∆2 ⊢ e ⇐= Cr                                                     by IH on D ′
          ∆ ⊢ e ⇐= Cr                                                   since ∆ = (∆1 ; ∆2 )

Case: D ends in ↓L. Similarly to the previous case, we need to distinguish whether x :
     ↓km Ak appears in Γ.
                                                   D′
                                            Γ, y : Ak ⊢ Cr
                                                                ↓L
                                   D=     Γ ; x : ↓km Ak ⊢ Cr
     We only show the case where x : ↓km Ak is in Γ; the other follows similar reasoning.

     Subcase: x : ↓km Ak ∈ Γ and so C ∈ σ(m). Hence, Γ ; x : ↓km Ak = Γ = Γ′ , x : ↓km Ak .
          Γ≥r                                                       by presupposition
          k≥m≥r                                                    by presuppositions
          ∆ ⊢ θ =⇒ Γ ; x : ↓km Ak                                      by assumption
          ∆1 ⊢ θ ′ =⇒ Γ′ and ∆2 ⊢ s =⇒ ↓km Ak and ∆2 ≥ m by inversion on subst. rule
                                                 where ∆ = ∆1 ; ∆2 and θ = (θ ′ , x 7→ s)
          y:Ak ⊢ x =⇒ Ak                                                         by hyp


E XTENDED V ERSION                                                          F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                  14


          ∆, y:Ak ⊢ (θ, x 7→ x) =⇒ (Γ, y : Ak )  by subst. rule (using ∆ ; y:Ak = ∆, y:Ak )
                     ′
          ∆, y:Ak ⊢ e ⇐= Cr for some e   ′                                     by IH on D ′
          ∆2 ≥ m ≥ r                                                     by previous lines
                                           ′
          ∆2 ; ∆ ⊢ match s (down y ⇒ e ) ⇐= Cr                                  by rule ↓E
          ∆ ; ∆2 = ∆        since C ∈ σ(m) and ∆2 ≥ m, we have C ∈ σ(j) for any Bj ∈ ∆2
          ∆ ⊢ match s (down y ⇒ e′ ) ⇐= Cr                                by previous line

                                                                                            

   While there are no substitutions involved, the other direction has to take care to intro-
duce a cut only for uses of the ⇐/⇒ rule, and identity only for uses of the ⇒/⇐ rule. This
requires a generalization of the induction hypothesis so that the elimination rules can be
turned “upside down”.

Theorem 13 (From Natural Deduction to Sequent Calculus)

 (i) If ∆ ⊢ e ⇐= Cr then ∆ ⊢ Cr

 (ii) If ∆ ⊢ s =⇒ Am and ∆′ , x : Am ⊢ Cr and ∆ ≥ r then ∆ ; ∆′ ⊢ Cr

Proof: By simultaneous rule induction on ∆ ⊢ e ⇐= Cr and ∆ ⊢ s =⇒ Am . We provide
four sample cases.

Case: The derivation ends in ⇒/⇐.

                                               D′
                                          ∆ ⊢ s =⇒ Am
                                                         ⇒/⇐
                                   D=     ∆ ⊢ s ⇐= Am

     x : Am ⊢ Am                                                             By identity rule
     ∆ ⊢ Am                                                            By IH(ii) with ∆′ = (·)

Case: The derivation ends in ⇐/⇒.

                                               D′
                                          ∆ ⊢ e ⇐= Am
                                                            ⇐/⇒
                               D=     ∆ ⊢ (e : Am ) =⇒ Am

     ∆′ , x : Am ⊢ Cr and ∆ ≥ r                                                 Assumption
     ∆ ⊢ Am                                                                    By IH(i) on D ′
     ∆ ; ∆ ′ ⊢ Cm                                                              By rule of cut

Case: The derivation ends in ↑E

                                                    D′
                                     ∆≥m      ∆ ⊢ s =⇒ ↑m
                                                        k Ak
                                                                ↑E
                              D=     ∆W ; ∆ ⊢ force s =⇒ Ak

E XTENDED V ERSION                                                          F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                 15


     ∆′ , x : Ak ⊢ Cr with ∆′ , x : Ak ≥ r                                   by assumption
     ∆W ; ∆ ≥ k                                                           by presupposition
     k≥r                                                                    since ∆′ , Ak ≥ r
     ∆′ ; y : ↑m
               k Ak ⊢ Cr                                                                by ↑L
     ∆W ; ∆ ≥ r                                                         using previous lines
     ∆ W ; ∆ ; ∆ ′ ⊢ Cr                                                            by IH(ii)

Case: The derivation ends in ↓E

                             D1                                      D2
                      ∆1 ⊢ s =⇒ ↓km Ak       ∆1 ≥ m ≥ r   ∆2 , x : Ak ⊢ e′ ⇐= Cr
                                                                                   ↓E
               D=             ∆1 ; ∆2 ⊢ match s (down x ⇒ e′ ) ⇐= Cr

     ∆2 , x : Ak ⊢ Cr                                                          by IH(i) on D2
     ∆2 ; x : ↓km Ak ⊢ Cr                                                          by rule ↓L
     ∆ 1 ; ∆ 2 ⊢ Cr                                                           by IH(ii) on D1

                                                                                           

   As mentioned above, verifications are the foundational equivalent of normal forms in
natural deduction. Using the two translations above we can show that every provable
proposition has a verification. While we have not written the translations out as functions,
they constitute the computational contents of our constructive proof of Theorem 12 and
Theorem 13.

Theorem 14 If ∆ ⊢ e ⇐= Am then there exists a verification of ∆ ⊢ e ⇐= Am .

Proof: Given an arbitrary deduction of ∆ ⊢ e ⇐= Am , we can use Theorem 13 (ii) to
translate it to a sequent derivation of ∆ ⊢ Am .
    By the admissibility of cut and identity (Theorem 2), we can obtain a long cut-free proof
of ∆ ⊢ Am .
    We observe that the translation of Theorem 12 translates only cut to ⇐/⇒ and only
identity to ⇒/⇐. Using the translation back to natural deduction from a long cut-free
proof therefore results in a verification.                                                 


5 Dynamics
As mentioned in Section 3, we obtain a simple typing judgment ∆ ⊢ e : A by collapsing the
distinction between e ⇐= A and s =⇒ A, using e as a universal notation for all expressions.
Furthermore, the annotation (e : Am ) is removed and the rules ⇒/⇐ and ⇐/⇒ are also
removed. The resulting rules remain syntax-directed in the sense that for every form of
expression there is a unique typing rule.
    We further annotate the mode-changing constructors with the mode of their subject,
which in each case is uniquely determined by the typing derivation. Some of these anno-
tations are necessary, because the computation rules depend on them; other information is
redundant but kept for clarity.

E XTENDED V ERSION                                                         F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                  16


                m
   • suspm
         k e : ↑k Ak if e : Ak

   • forcem                m
          k e : Ak if e : ↑k Ak

   • downnm e : ↓nm An if e : An

   • matchm e Mr : Cr if e : Am
We give a sequential call-by-value semantics similar to the K machine (e.g., [Harper, 2016,
Chapter 28]), but maintaining a global environment similar to the Milner Abstract Machine
[Accattoli et al., 2014]. There are two forms of state in the machine:
   • η ; K ⊲m e (evaluate e of mode m under continuation stack K and environment η)

   • η ; K ◭m v (pass value v of mode m to continuation stack K in environment η)
In the first, e is an expression to be evaluated and K is a stack of continuations that the
value of e is passed to for further computation. The second then passes this value v to the
continuation stack.
    The global environment η maps variables to values, but these values may again ref-
erence other variables. In this way it is like Launchbury’s [1993] heap, a connection we
exploit in Section 6 to model call-by-need. Because we maintain a global environment, we
do not need to build closures, nor do we need to substitute values for variables. Instead,
we only (implicitly) rename variables to make them globally unique. This form of speci-
fication allows us to isolate the dynamic use of variables, which means we can observe the
computational consequences of modes and their substructural nature. We could also use
the translation to the sequent calculus and then observe the consequence with an explicit
heap [Pruiksma and Pfenning, 2022, Pfenning and Pruiksma, 2023], but in this paper we
study natural deduction and functional computation more directly.
    The syntax for continuations, environments, values, and machine states is summarized
in Figure 4. Although not explicitly polarized (as in Levy [2006]), values of negative type
(⊸, N, ↑) are lazy in the sense that they abstract over unevaluated expressions, while val-
ues of positive types (⊗, 1, ⊕, ↓) are constructed from other values. This will be significant
in our analysis of the computational properties of modes. Continuation frames just reflect
the left-to-right call-by-value nature of evaluation.
    Values are typed as expressions. Frames are typed with Γ ⊢ f : Bk < Am , which means
f takes a value of type Am and passes a value of type Bk further up the continuation stack.
We show sample rules for a negative (⊸) and a positive (⊕) type.
                         ∆ ⊢ e2 : Am                   ∆ ⊢ v1 : Am ⊸ Bm
                ∆ ⊢ _ e2 : Bm < (Am ⊸ Bm )             ∆ ⊢ v1 _ : Bm < Am

                                                ∆, x : Aℓm ⊢ e(x) : Cr   (∀ℓ ∈ L)
 ∆W ⊢ ℓ(_) : ⊕{ℓ : Aℓm }ℓ∈L < Aℓm      ∆ ⊢ matchm _ (ℓ(x) ⇒ e(x)) : Cr < ⊕{ℓ : Aℓm }ℓ∈L


                                         ∆ ⊢ K : Cr < Bk     ∆′ ⊢ f : Bk < Am
             ∆W ⊢ ǫ : Am < Am                  ∆ ; ∆′ ⊢ K · f : Cr < Am

E XTENDED V ERSION                                                          F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                      17


               Frames           f     ::= _ e2 | v1 _                    (⊸)
                                        | _.ℓ                            (N)
                                        | forcemk _                      (↑)
                                       |    (_, e2 ) | (v1 , _)          (⊗)
                                       |    ℓ(_)                         (⊕)
                                       |    downnm _                     (↓)
                                       |    matchm _ Mr                  (⊗, 1, ⊕, ↓)

               Continuations K        ::= ǫ | K · f

               Environments η         ::= · | η, x 7→ v | η, [x 7→ v]

               Matches          M     ::=   (x1 , x2 ) ⇒ e′ (x1 , x2 )   (⊗)
                                        |   ( ) ⇒ e′                     (1)
                                        |   (ℓ(x) ⇒ eℓ (x))ℓ∈L           (⊕)
                                        |   down x ⇒ e′ (x)              (↓)

               Values           v     ::= λx. e(x)                       (⊸)
                                        | {ℓ ⇒ eℓ }ℓ∈L                   (N)
                                        | suspmk e                       (↑)
                                       |    (v1 , v2 )                   (⊗)
                                       |    ()                           (1)
                                       |    ℓ(v)                         (⊕)
                                       |    downnm v                     (↓)

               States           S     ::= η ; K ⊲m e
                                        | η ; K ◭m v

                                    Figure 4: Machine States


    Regarding environments we face a fundamental choice. One possibility is to extend the
term language of natural deduction with explicit constructs for weakening and contrac-
tion. Then, similar to Girard and Lafont [1987], no garbage collection would be required
during evaluation since uniqueness of references to variables would be maintained.
    We pursue here an alternative that leads to slightly deeper properties. We leave the
structural rules implicit as in the rules so far. This means that variables of linear mode (that
is, a mode that allows neither weakening nor contraction) have uniqueness of reference
and their bindings can be deallocated when dereferenced. Variables of structural mode
(that is, a mode that allows both weakening and contraction) are simply persistent in the
dynamics and therefore could be subject to an explicit garbage collection algorithm.
    A difficulty arises with variables that only admit contraction but not weakening. After
they are dereferenced the first time, they may or may not be dereferenced again. That is,
they could be implicitly weakened after the first access. In order to capture this we intro-
duce a new form of typing [x : Am ] and binding [x 7→ v] we call provisional. A provisional


E XTENDED V ERSION                                                               F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                                 18


binding does not need to be referenced even if m does not admit weakening. The impor-
tant new property is that an “ordinary” variable y : Ak that does not admit weakening
can not appear in a binding [x 7→ v]. In addition, all the usual independence requirements
have to be observed.
    The rules for typing expressions, continuations, etc. are extended in the obvious way,
allowing variables [x : Am ] to be used or ignored (as a part of some ∆W ). We extend the
context merge operation as follows, keeping in mind that x : Am may require an occurrence
of x (depending on σ(m)), while [x : Am ] does not.

      (∆1 , [x : Am ]   ;    (∆2 , [x : Am ])   =   (∆1 ; ∆2 ), [x : Am ]   provided C ∈ σ(m)
      (∆1 , x : Am )    ;    (∆2 , [x : Am ])   =   (∆1 ; ∆2 ), x : Am      provided C ∈ σ(m)
      (∆1 , [x : Am ]   ;    (∆2 , x : Am )     =   (∆1 ; ∆2 ), x : Am      provided C ∈ σ(m)
     (∆1 , [x : Am ])   ;    ∆2                 =   (∆1 ; ∆2 ), [x : Am ]   provided x 6∈ dom(∆2 )
                  ∆1    ;    (∆2 , [x : Am ])   =   (∆1 ; ∆2 ), [x : Am ]   provided x 6∈ dom(∆1 )

We have the following typing rules for environments. ∆W now means that every dec-
laration in ∆ can be weakened, either explicitly because its mode allows weakening, or
implicitly because it is provisional.

             η : (∆ ; ∆′ ) ∆′ ≥ m ∆′ ⊢ v : Am               η : (∆ ; ∆′W ) ∆′W ≥ m         ∆′W ⊢ v : Am
 (·) : (·)         (η, x 7→ v) : (∆, x : Am )                      (η, [x 7→ v]) : (∆, [x : Am ])

As an example, consider η0 = (x 7→ ( ), y 7→ λf. f x) where the mode of variables is imma-
terial, but let’s fix them to be L with σ(L) = { }.

                   (·) : (·)     · ⊢ ( ) : 1L                       ..
                                                                     .
                    (x 7→ ( )) : (x : 1L )       x : 1L ⊢ λf. f x : (1L ⊸ AL ) ⊸ AL
                             (x 7→ ( ), y 7→ λf. f x) : (y : (1L ⊸ AL ) ⊸ AL )

We observe that the binding of x 7→ ( ) does not contribute a declaration x : 1 to the result
context due to the occurrence of x in the value of y.
   Now consider a slightly modified version where the mode of both x and y is S with
σ(S) = {C}, and the binding of y 7→ . . . becomes provisional. This modified example is no
longer well-typed.

                 (·) : (·)      · ⊢ ( ) : 1S                       ..
                                                                    .
                  (x 7→ ( )) : (x : 1S )        x : 1S ⊢ λf. f x : (1S ⊸ AS ) ⊸ AS
                                                                                      ??
                        (x 7→ ( ), [y 7→ λf. f x]) : (y : [(1S ⊸ AS ) ⊸ AS )]

The problem is at the rule application marked by ??. The variable y does not need to be
used, despite its mode, because the binding is provisional. This means that x might also
not be used because its only occurrence is in the value of y. But that is not legal, since the
mode of x does not admit weakening and the binding is not provisional.


E XTENDED V ERSION                                                                     F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                       19


   We type abstract machine states with the type of their final answer, that is s : Cr .

                        η : (∆ ; ∆′ ) ∆ ⊢ K : Cr < Am         ∆′ ⊢ e : Am
                                       (η ; K ⊲m e) : Cr

                        η : (∆ ; ∆′ ) ∆ ⊢ K : Cr < Am         ∆′ ⊢ v : Am
                                       (η ; K ◭m v) : Cr

    We now continue with the computational rules for our abstract machine. The rules are
in Figure 5. We factor out passing a value to a match, η ; v ◮m M = η ′ ; e′ that produces
a (possibly extended) environment η ′ and expression e′ . In all cases below, we presuppose
the variable names are chosen so the extended environment has unique bindings for each
variable. For an extension with mutual recursion, see Section 6.
    We obtain the following expected theorems of preservation and progress.

Theorem 15 (Preservation) If S : A and S −→ S ′ then S ′ : A.

Proof: By cases on S −→ S ′ , applying inversion to the typing of S and assembling a typing
derivation of S ′ from the resulting information.
     The trickiest case involves dereferencing a variable x 7→ v admitting contraction. It
is sound because every variable y occurring in v must also admit contraction by mono-
tonicity and, furthermore, such variables still have an occurrence in the value v that is
being returned. Therefore in the typing of the environment we can now type [x 7→ v] with
[x : Am ].                                                                                

   A machine state is final if it has the form η ; ǫ ◭m v, that is, if a value is returned to the
empty continuation in some global environment η. In order to prove progress, we need to
characterize values of a given type using a canonical forms property. Note that we allow a
context ∆ to provide for the variables that may be embedded in a value of negative type
(⊸, N, ↑), but that a variable by itself does not count as a value.

Theorem 16 (Canonical Forms) If ∆ ⊢ v : Am then one of the following applies:

 (i) if Am = Bm ⊸ Cm then v = λx. e(x) for some e

 (ii) if Am = N{ℓ : Aℓm }ℓ∈L then v = {ℓ ⇒ eℓ }ℓ∈L for some set eℓ

(iii) if Am = ↑m                 m
               k Bk then v = suspk e

(iv) if Am = Bm ⊗ Cm then v = (v1 , v2 ) for values v1 and v2

 (v) if Am = 1 then v = ( )
                    ℓ }
(vi) if Am = ⊕{ℓ : Bm                  ′                             ′
                       ℓ∈L then v = ℓ(v ) for some ℓ ∈ L and value v

(vii) if Am = ↓nm An then v = downnm v ′ for some value v ′

Theorem 17 (Progress) If S : Cr then either S is final or S 7→ S ′ for some S ′


E XTENDED V ERSION                                                                F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                                          20



   η    ;          ()    ◮m      (( ) ⇒ e′ )                    =   η                          ;   e′
   η    ;   (v1 , v2 )   ◮m      ((x1 , x2 ) ⇒ e′ (x1 , x2 ))   =   η, x1 7→ v1 , x2 7→ v2     ;   e′ (x1 , x2 )
   η    ;       ℓ(v)     ◮m      (ℓ(x) ⇒ e′ℓ (x))ℓ∈L            =   η, x 7→ v                  ;   e′ℓ (x)
   η    ; downnm v       ◮m      (down(x) ⇒ e′ (x))             =   η, x 7→ v                  ;   e′ (x)

       η, x 7→ v, η ′ ; K ⊲m x                 −→ η, η ′ ; K ◭m v                            (C 6∈ σ(m))
       η, x 7→ v, η ′ ; K ⊲m x                 −→ η, [x 7→ v], η ′ ; K ◭m v                  (C ∈ σ(m))

       η ; K ⊲r matchm e Mr                    −→ η ; K · (matchm _ Mr ) ⊲m e (⊗, 1, ⊕, ↓)
       η ; K · (matchm _ Mr ) ◭m v             −→ η ′ ; K ⊲r e′ where η ; v ◮m Mr = η ′ ; e′

       η ; K ⊲m λx. e(x)                       −→     η ; K ◭m λx. e(x)                      (⊸)
       η ; K ⊲m (e1 e2 )                       −→     η ; K · (_ e2 ) ⊲m e1
       η ; K · (_ e2 ) ◭m v1                   −→     η ; K · (v1 _) ⊲m e2
       ηnn ; K · (λx. e(x), _) ◭m v2           −→     η, x 7→ v ; K ⊲m e(x)

       η ; K ⊲m {ℓ ⇒ eℓ }ℓ∈L                   −→ η ; K ◭m {ℓ ⇒ eℓ }ℓ∈L                      (N)
       η ; K ⊲m e.ℓ                            −→ η ; K · (_.ℓ) ⊲m e
       η ; K · (_.ℓ) ◭m {ℓ ⇒ eℓ }ℓ∈L           −→ η ; K ⊲m eℓ                                (ℓ ∈ L)

       η ; K ⊲m suspm k e            −→ η ; K ◭m suspm  k e                                  (↑)
                      m
       η ; K ⊲k forcek e             −→ η ; K · (forcem
                                                      k _) ⊲m e
                     m           m
       η ; K · (forcek _) ◭m suspk e −→ η ; K ⊲k e

       η ; K ⊲m (e1 , e2 )                     −→ η ; K · (_, e2 ) ⊲m e1                     (⊗)
       η ; K · (_, e2 ) ◭m v1                  −→ η ; K · (v1 , _) ⊲m e2
       η ; K · (v1 , _) ◭m v2                  −→ η ; K ◭m (v1 , v2 )

       η ; K ⊲m ( )                            −→ η ; K ◭m ( )                               (1)

       η ; K ⊲m ℓ(e)                           −→ η ; K · ℓ(_) ⊲m e                          (⊕)
       η ; K · ℓ(_) ◭m v                       −→ η ; K ◭m ℓ(v)

       η ; K ⊲m downnm e                       −→ η ; K · downnm _ ⊲n e                      (↓)
       η ; K · (downnm _) ◭n v                 −→ η ; K ◭m downnm v

                                      Figure 5: Computation Rules


Proof: By cases on the typing derivation for the configuration and inversion on the typing
of the embedded frames, values, and expressions. We apply the canonical forms theorem
when we need the shape of a value.                                                       

    Purely positive types play an important role because we view values of these types as
directly observable, while values of negative types can only be observed indirectly through



E XTENDED V ERSION                                                                           F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                   21


their elimination forms.

         Purely positive types A+ , B + ::= A+ ⊗ B + | 1 | ⊕{ℓ : A+
                                                                  ℓ }ℓ∈L | ↓A
                                                                             +


Values of purely positive types are closed, even if values of negative types may not be.
Lemma 18 (Positive Values) If ∆ ⊢ v : A+                        +
                                              r then · ⊢ v : Ar and all declarations in ∆ admit
weakening (either due to their mode or because they are provisional).

Proof: By induction on the structure of the typing derivation, recalling that variables are
not values.                                                                              

    We call a variable x : Am linear if σ(m) = { }, that is, the mode m admits neither
weakening or contraction. We extend this term to types, bindings in the environment, etc.
in the obvious way.

Theorem 19 (Freedom from Garbage) If · ⊢ e : A+                  ∗
                                              r and · ; ǫ ⊲r e −→ η ; ǫ ◭r v, then η does
not contain a binding x 7→ v with σ(m) = { }.

Proof: Because A+ r is purely positive, we know by Lemma 18 that v is closed.
    When the continuation K is empty, the typing rule for valid states implies that η : ∆
and ∆ ⊢ v : A+r for some ∆. Since v is closed, ∆ cannot contain any linear variables.
    Then we prove by induction on the typing of η that none of variables in η can be linear.
In the inductive case
                           η ′ : (∆ ; ∆′ ) ∆′ ≥ m ∆′ ⊢ v : Am
                                  (η ′ , x 7→ v) : (∆, x : Am )
we know that m must admit weakening or contraction or both. Since ∆′ ≥ m, by mono-
tonicity, ∆′ must also admit weakening or contraction and we can apply the induction
hypothesis to η ′ : (∆ ; ∆′ ).                                                     

   We call a variable xm , an expression e : Am , or a binding x 7→ v strict if σ(m) ⊆ {C},
that is, m does not admit weakening.

Theorem 20 (Strictness) If · ⊢ e : A+                  ∗
                                    r and · ; ǫ ⊲r e −→ η ; ǫ ◭r v, then every strict binding
in η is of the form [x 7→ v].

Proof: Because A+ r is purely positive, we know by Lemma 18 that v is closed.
     When the continuation K is empty, the typing rule for valid states implies η : ∆ and
∆ ⊢ v : A+ r for some ∆. Since v is closed, ∆ contains strict variables only in the form
[x : Am ].
     We prove by induction on the typing of η all strict variables in η have the form [x 7→ w].
There are two inductive cases.
                            η ′ : (∆ ; ∆′ ) ∆′ ≥ m     ∆′ ⊢ w : Am
                                  (η ′ , x 7→ w) : (∆, x : Am )

Since m is not strict, it must admit weakening. Since ∆′ ≥ m, every variable in ∆′ must
also admit weakening by monotonicity, so we can apply the induction hypothesis to ∆ ; ∆′ .

E XTENDED V ERSION                                                          F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                         22



                           η ′ : (∆ ; ∆′W )   ∆′W ≥ m      ∆′W ⊢ w : Am
                                   (η ′ , [x 7→ v]) : (∆, [x : Am ])
Any declaration in ∆′W either directly admits weakening or is of the form [y : Ak ] for a
strict k so we can apply the induction hypothesis to η ′ : (∆ ; ∆′W ).                 

   In this context of call-by-value, this property expresses that every strict variable will be
read at least once, since a binding [x 7→ v] arises only from reading the value of x.

Theorem 21 (Dead Code) If · ⊢ e : A+                       ∗
                                        r and · ; ǫ ⊲r e −→ η ; ǫ ◭r v then every state during
the computation either evaluates ⊲m or returns ◭m for m ≥ r.

Proof: Most rule do not change the subject’s mode. Several rules potentially raise the
mode, name evaluating a match, a force, or a down. For each of these there is a corre-
sponding rule lowering the mode back to its original, namely return a value to a match,
to a force, or to a down.
    We say the mode of a frame f is the mode of the following state after a value is returned
to f . We prove by induction over the computation that in all states, all continuation frames
and subjects have modes m ≥ r.                                                              

Corollary 22 (Erasure) Assume · ⊢ e : A+                            ∗
                                              r and · ; ǫ ⊲r e −→ η ; ǫ ◭r v. Let Ω be a new term
of every type and no transition rule.
    If we obtain e′ by replacing all subterms e′ : Bk for k 6≥ r with Ω, then evaluation e′ still
terminates in a final state. This final state differs from v in that subterms of mode k 6≥ r are also
replaced by Ω.

Proof: The computation of e′ parallels that of e. It would only get stuck for a state η ′ ;
K ′ ⊲k Ω, but that is impossible by the preceding dead code theorem since k 6≥ r.        


6 Adding Recursion and Call-by-Need
To add recursion at the level of types we allow a global environment Σ of equirecursive
type definition tm = Am that may be mutually recursive and restrict Am to be contractive,
that is, start with a type constructor and not a type name. Since we view them as equire-
cursive we can silently unfold them, and the only modification is in the rule for directional
change. The typing judgment is now parameterized by a signature Σ, but since it is fixed
we generally omit it.
                              ∆ ⊢ s =⇒ A′m A′m = Am
                                                         ⇒/⇐
                                     ∆ ⊢ s ⇐= Am
Type equality follows the standard coinductive definition [Amadio and Cardelli, 1993]. It
can also be replaced by subtyping A′m ≤ Am without affecting soundness, but a formal
treatment is beyond the scope of this paper.
    In order to model recursion at the level of expressions, we allow contextual definitions
[Nanevski et al., 2008] in the signature. They have the form f [∆] : Am = e and may be

E XTENDED V ERSION                                                               F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                       23


mutually recursive, so all definitions are checked with respect to the same global signature
Σ, using the ⊢Σ Σ′ sig judgment. We use here a form of checkable substitution ∆′ ⊢ θ ⇐=
∆ which we did not require earlier, and which has the obvious pointwise definition.

   ⊢Σ Σ′ sig   ⊢Σ Am type    Am contractive      ⊢Σ Σ′ sig   ∆ ⊢Σ e ⇐= Am
                ⊢Σ Σ′ , tm = Am                   ⊢Σ Σ′ , f [∆] : Am = e sig       ⊢Σ (·) sig

                          f [∆] : Am = e ∈ Σ    ∆′ ⊢Σ θ ⇐= ∆
                                                                call
                                   ∆′ ⊢Σ f [θ] =⇒ Am

The reason that definitions are contextual is partly pragmatic. We are used to reifying, say,
f (x : A) (y : B) : C = e(x, y) as f : A → B → C = λx. λy. e(x, y). But because Am ⊸ Bm
requires the same mode on both sides, we would have to insert shifts, or generalize the
function type and thereby introduce multiple mode-shifting constructors. By using con-
textual definitions, we can directly express dependence on a mixed context. For example,
f [x : Am , y : Bk ] : Cr = e(x, y) which, by presupposition, requires m, k ≥ r so that the
judgment x : Am , y : Bk ⊢ e(x, y) ⇐= Cr is well-formed.
      In order to demonstrate call-by-need, let’s assume that contextual definitions are in-
deed treated in call-by need manner. In order to model this, we create a new form of
environment entry x 7→ e where e is an unevaluated expression. A substitution θ = (x1 7→
e1 , . . . , xn 7→ en ) then also represents an environment in which none of the expressions ei
depend on any of the variables xi . We also need to new continuation frame x 7→ _ to create
a value binding in the environment. We have the following new rules:

      η ; K ⊲m f [θ]                     −→ η, θ ; K ⊲m e         for f [∆] : Am = e ∈ Σ
      η, x 7→ e, η ′ ; K ⊲m x            −→ η, [x 7→ e], η ′ ; K · (x 7→ _) ⊲m e
      η, [x 7→ e], η ; K · (x 7→ _) ◭m v −→ η, [x 7→ v], η ′ ; K ◭m v
                     ′


We can further simplify these rules if m does not admit contraction, dropping [x 7→ e] and
[x 7→ v]. We could also model “black holes” by rebinding not [x 7→ e] in the second rule,
but [x 7→ Ω] where Ω has every type, but does not reduce.
    The theorems from the previous section continue to hold. They imply that in a final
state of observable type there will be no binding x 7→ e in the environment if the mode of x
is strict (that is, does not admit contraction). In other words, strict expressions are always
evaluated.


7 Algorithmic Type Checking
The bidirectional type system of Section 3 is not yet algorithmic, among other things be-
cause splitting a given context into ∆ = (∆1 ; ∆2 ) is nondeterministic. One standard
solution is track which are hypotheses are used in one premise (which ends up ∆1 ), sub-
tract them from the available ones, and pass the remainder into the second premise (which
ends up ∆2 together with an overall remainder) [Cervesato et al., 2000]. This originated in
proof search, but here when we actually have a proof terms available to check, other op-
tions are available. Additive resource management computes the used hypotheses (rather

E XTENDED V ERSION                                                             F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                 24


than the unused ones) and merges (“adds”) them [Atkey, 2018], which is conceptually
slightly simpler and also has been shown to be more efficient [Hughes and Orchard, 2020].
    The main complication in the additive approach are internal and external choice, more
specifically, the NR and ⊕L rules when the choice is empty. For example, while check
∆ ⊢ { } ⇐= N{ } any subset of ∆ could be used. We reuse the idea from the dynamics to
have hypothesis [x : Am ] which may or may not have been used. Unfortunately, this leads
to a plethora of different judgments, but it is not clear how to simplify them. In defining
the additive approach, the main judgment is

                                            Γ ⊢ e ⇐⇒ Am / Ξ

where Γ is a plain (that is, free of provisional hypotheses) context containing all variables
that might occur in e (regardless of mode or structural properties) and Ξ is a context that
may contain provisional hypotheses. We maintain the mode invariant Ξ ≥ m (even if it
may be the case that Γ 6≥ m).
   Because we keep the contexts ∆ free of provisional hypotheses, we define the relation
Ξ ⊒ ∆ which may remove or keep provisional hypotheses.

                            (Ξ, x : Am )     ⊒   (∆, x : A) if Ξ ⊒ ∆
                           (Ξ, [x : Am ])    ⊒   (∆, x : A) if Ξ ⊒ ∆
                           (Ξ, [x : Am ])    ⊒   ∆          if Ξ ⊒ ∆
                                      (·)    ⊒   (·)

With this relation, we can state the soundness of algorithmic typing (postponing the proof).

Theorem 23 (Soundness of Algorithmic Typing)
If Γ ⊢ e ⇐⇒ Am / Ξ and Ξ ⊒ ∆ then ∆ ⊢ e ⇐⇒ Am .

   For completeness we need a different relation ∆ ≥ Ξ which means that Ξ contains a
legal subset of the hypotheses in ∆. This means hypotheses in ∆ might be in Ξ (possibly
provisional) or not, but then only if they can we weakened.

            (∆, x : Am )    ≥    (Ξ, x : Am ) if ∆ ≥ Ξ
            (∆, x : Am )    ≥    (Ξ, [x : Am ]) if ∆ ≥ Ξ
            (∆, x : Am )    ≥    Ξ              if ∆ ≥ Ξ provided W ∈ σ(m)
                     (·)    ≥    (·)

With this relation we can state the completeness of algorithmic typing (also postponing the
proof).

Theorem 24 (Completeness of Algorithmic Typing)
If ∆ ⊢ e ⇐⇒ Am then ∆ ⊢ e ⇐⇒ Am / Ξ for some Ξ with ∆ ≥ Ξ

   For the algorithm itself we need several operations. The first, Ξ \ x : A removes x : A
from Ξ if this is legal operation. Its prototypical use is in the ⊸I rule:

                                  Γ, x : Am ⊢ e ⇐= Bm / Ξ
                                                                  ⊸I
                           Γ ⊢ λx. e ⇐= Am ⊸ Bm / (Ξ \ x : Am )

E XTENDED V ERSION                                                         F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                      25


 For this rule application to be correct, x : Am must either have been used and therefore
occur in Ξ, or the mode m must allow weakening.

            (Ξ, x : Am )    \    x : Am    =    Ξ
          (Ξ, [x : Am ])    \    x : Am    =    Ξ
             (Ξ, y : Bk )   \    x : Am    =    (Ξ \ x : Am ), y : Bk provided y 6= x
           (Ξ, [y : Bk ])   \    x : Am    =    (Ξ \ x : Am ), y : Bk provided y 6= x
                      (·)   \    x:A       =    (·)                   provided W ∈ σ(m)

We have the following fundamental property (modulo exchange on contexts, as usual).

Lemma 25 If Ξ \ x : Am = Ξ′ then

 (i) either Ξ = (Ξ′ , x : Am )

 (ii) or Ξ = (Ξ′ , [x : Am ])

(iii) or Ξ = Ξ′ with x 6∈ dom(Ξ) and W ∈ σ(m).

We also need two forms of context restriction. The first Ξkm removes all hypotheses whose
mode is not greater or equal to m to restore our invariant. It fails if Ξ contains a used
hypothesis Br with r 6≥ m. It is used only in the ↑I rule to restore the invariant,

                                           Γ ⊢ e ⇐= Ak / Ξ
                                                                  ↑I
                                   Γ ⊢ susp e ⇐= ↑m
                                                  k Ak / Ξkm

                       (Ξ, x : Ak )km      =    Ξkm , x : Ak    provided k ≥ m
                      (Ξ, [x : Ak ])km     =    Ξkm , [x : Ak ] provided k ≥ m
                      (Ξ, [x : Ak ])km     =    Ξkm             provided k ≥
                                                                           6 m
                                (·)km      =    (·)
It has the following defining property.

Lemma 26 If ∆ ≥ m and ∆ ≥ Ξ then ∆ ≥ Ξkm .

    The second form of context restriction occurs in the case of an empty internal or exter-
nal choice. All of the hypothesis that are allowed by the independence principle could be
considered used, but they might also not. We write [Γ|m ] and define:

                      [(Γ, x : Ak )|m ] = [Γ|m ], [x : Ak ] provided k ≥ m
                      [(Γ, x : Ak )|m ] = [Γ|m ]            provided k 6≥ m
                               [(·)|m ] = (·)

It is used only in the nullary case for internal and external choice.

                                                      Γ ⊢ s =⇒ ⊕m { } / Ξ m ≥ r
                                          NI0                                            ⊕E0
        Γ ⊢ { } ⇐= Nm { } / [Γ|m ]                  Γ ⊢ match s ( ) ⇐= Cr / Ξ ; [Γ|r ]




E XTENDED V ERSION                                                               F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                             26


We come to the final operation Ξ1 ⊔ Ξ2 which is needed for NI and ⊕E. We show the case
of NI2 , that is, the binary version.

                          Γ ⊢ e1 ⇐= Am / Ξ1         Γ ⊢ e2 ⇐= Bm / Ξ2
                                                                                    NI2
               Γ ⊢ {π1 ⇒ e1 , π2 ⇒ e2 } ⇐= N{π1 : Am , π2 : Bm } / Ξ1 ⊔ Ξ2

 Variables y : Bk that are definitely used in Ξ1 or Ξ2 must also be used in the other, or be
available for weakening. This could be because they are provisional [y : Bk ] or because
mode k admits weakening. This idea is captured by the following definition.

   (Ξ1 , x : Am )    ⊔   (Ξ2 , x : Am )     =   (Ξ1 ⊔ Ξ2 ), x : Am
  (Ξ1 , [x : Am ])   ⊔   (Ξ2 , x : Am )     =   (Ξ1 ⊔ Ξ2 ), x : Am
   (Ξ1 , x : Am )    ⊔   (Ξ2 , [x : Am ])   =   (Ξ1 ⊔ Ξ2 ), x : Am
  (Ξ1 , [x : Am ])   ⊔   (Ξ2 , [x : Am ])   =   (Ξ1 ⊔ Ξ2 ), [x : Am ]
   (Ξ1 , x : Am )    ⊔   Ξ2                 =   (Ξ1 ⊔ Ξ2 ), x : Am      for x 6∈ dom(Ξ2 ), W ∈ σ(m)
              Ξ1     ⊔   (Ξ2 , x : Am )     =   (Ξ1 ⊔ Ξ2 ), x : Am      for x 6∈ dom(Ξ1 ), W ∈ σ(m)
  (Ξ1 , [x : Am ])   ⊔   Ξ2                 =   Ξ1 ⊔ Ξ2                 for x 6∈ dom(Ξ2 )
              Ξ1     ⊔   (Ξ2 , [x : Am ])   =   Ξ1 ⊔ Ξ2                 for x 6∈ dom(Ξ1 )
              (·)    ⊔   (·)                =   (·)

We have the following two properties, expressing the property of a least upper bound in
two slightly asymmetric judgments.
Lemma 27
 (i) If ∆ ≥ Ξ1 and ∆ ≥ Ξ2 then ∆ ≥ Ξ1 ⊔ Ξ2 .

 (ii) if Ξ1 ⊔ Ξ2 ⊒ ∆ then for some ∆1 , ∆1W , ∆2 , ∆2W we have Ξ1 ⊒ ∆1 , Ξ2 ⊒ ∆2 and ∆ =
      ∆1 ; ∆1W = ∆2 ; ∆2W .

   The complete set of rules for algorithmic typing can be found in Figure 6.

Lemma 28 If Γ ⊢ e ⇐⇒ Am / Ξ then Ξ ≥ m

Proof: By straightforward rule induction.                                                             

Lemma 29 (Context Extension) If Γ ⊢ e ⇐⇒ Am / Ξ and Ξ ⊒ ∆ and Γ′ ⊇ Γ then Γ′ ⊢ e ⇐⇒
Am / Ξ′ for some Ξ′ with Ξ′ ⊒ ∆.

Proof: By rule induction on the given derivation and inversion on the definition of Ξ ⊒ ∆.


Proof: (of soundness, Theorem 23) By rule induction on the algorithmic typing derivation
and inversion of the Ξ ⊒ ∆ judgment.                                                   

Proof: (of completeness, Theorem 24) By rule induction on the given bidirectional typing.


Corollary 30 · ⊢ e ⇐= Am iff · ⊢ e ⇐= Am /·

E XTENDED V ERSION                                                                  F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                 27


8 Conclusion
There have been recent proposals to extend the adjoint approach to combining logics to
dependent types. Licata and Shulman [2016], Licata et al. [2017] permit dependent types
and richer connections between the logics that are combined, but certain properties such as
independence are no longer fundamental, but have to be proved in each case where they
apply. While they mostly stay within a sequent calculus, they also briefly introduce natu-
ral deduction. They also provide a categorical semantics. Hanukaev and Eades [2023] also
permit dependent types and use the graded/algebraic approach to defining their system.
However, their approach to dependency appears incompatible with control of contraction,
so their adjoint structure is not nearly as general as ours. They also omit empty internal
choice (and external choice altogether), which created some of the trickiest issues in our
system. Neither of these proposes an algorithm for type checking or an operational seman-
tics that would exploit the substructural and mode properties to obtain “free theorems”
about well-typed programs.
    We are pursuing several avenues of future work building on the results of this paper.
On the foundational side, we are looking for a direct algorithm to convert an arbitrary
natural deduction into a verification. On the programming side, we are considering mode
polymorphism, that is, type-checking the same expression against multiple different modes
to avoid code duplication. On the application side, we are considering staged computa-
tion, quotation, and metaprogramming, decomposing the usual type A or its contextual
analogue along the lines of Example 8.


References
Andreas Abel, Nils Anders Danielsson, and Oskar Eriksson. A graded modal depen-
 dent type theory with a universe and erasure, formalized. Proc. ACM Program. Lang.,
 7(ICFP’23):920–954, 2023.

Samson Abramsky. Computational interpretations of linear logic. Theoretical Computer
  Science, 111:3–57, 1993.

Beniamino Accattoli, Pablo Barenbaum, and Damiano Mazza. Distilling abstract machines.
  In J. Jeuring and M. Chakravarty, editors, 19th International Conference on Functional Pro-
  gramming (ICFP 2014), pages 363–376, Gothenburg, Sweden, September 2014. ACM.
  Long version available at arXiv:1406.2370.

Roberto M. Amadio and Luca Cardelli. Subtyping recursive types. ACM Transactions on
  Programming Languages and Systems, 15(4):575–631, 1993.

Jean-Marc Andreoli. Logic programming with focusing proofs in linear logic. Journal of
  Logic and Computation, 2(3):197–347, 1992.

Robert Atkey. Syntax and semantics of quantitative type theory. In Anuj Dawar and Erich
  Grädel, editors, 33rd Conference on Logic in Computer Science (LICS 2018), pages 56–65,
  Oxford, UK, July 2018. ACM.


E XTENDED V ERSION                                                         F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                    28


Andrew Barber. Dual intuitionistic linear logic. Technical Report ECS-LFCS-96-347, De-
 partment of Computer Science, University of Edinburgh, September 1996.

P. N. Benton. A mixed linear and non-linear logic: Proofs, terms and models. In Leszek
   Pacholski and Jerzy Tiuryn, editors, Selected Papers from the 8th International Workshop
   on Computer Science Logic (CSL’94), pages 121–135, Kazimierz, Poland, September 1994a.
   Springer LNCS 933. An extended version appears as Technical Report UCAM-CL-TR-
   352, University of Cambridge.

P. N. Benton. A mixed linear and non-linear logic: Proofs, terms and models (preliminary
   report). Technical Report UCAM-CL-TR-352, University of Cambridge, October 1994b.
   URL https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-352.html.

P. N. Benton and Philip Wadler. Linear logic, monads, and the lambda calculus. In
   E. Clarke, editor, Proceedings of the 11th Annual Symposium on Logic in Computer Science,
   pages 420–431, New Brunswick, New Jersey, July 1996. IEEE Computer Society Press.

P. N. Benton, Gavin M. Bierman, Martin Hyland, and Valeria de Paiva. A term calculus for
   intuitionistic linear logic. In International Conference on Typed Lambda Calculi and Applica-
   tions, pages 75–90, Utrecht, The Netherlands, 1993. Springer LNCS 664.

P. N. Benton, G. M. Bierman, and V. C. V. de Paiva. Computational types from a logical
   perspective. Journal of Functional Programming, 8(2):177–193, March 1998.

Luı́s Caires and Frank Pfenning. Session types as intuitionistic linear propositions. In
  Proceedings of the 21st International Conference on Concurrency Theory (CONCUR 2010),
  pages 222–236, Paris, France, August 2010. Springer LNCS 6269.

Luı́s Caires, Frank Pfenning, and Bernardo Toninho. Linear logic propositions as session
  types. Mathematical Structures in Computer Science, 26(3):367–423, 2016. Special Issue on
  Behavioural Types.

Iliano Cervesato, Joshua S. Hodas, and Frank Pfenning. Efficient resource management for
   linear logic proof search. Theoretical Computer Science, 232(1–2):133–163, February 2000.
   Special issue on Proof Search in Type-Theoretic Languages, D. Galmiche and D. Pym,
   editors.

Bor-Yuh Evan Chang, Kaustuv Chaudhuri, and Frank Pfenning. A judgmental analysis
  of linear logic. Technical Report CMU-CS-03-131R, Carnegie Mellon University, Depart-
  ment of Computer Science, December 2003.

Kaustuv Chaudhuri. Classical and intuitionistic subexponential logics are equally expres-
  sive. In Computer Science Logic, pages 185–199. Springer LNCS 6247, August 2010.

Pritam Choudhury, Harley Eades III, Richard A. Eisenberg, and Stephanie Weirich. A
  graded dependent type system with a usage-aware semantics. Proc. ACM Program. Lang.,
  5(POPL’21):1–32, 2021.

Alonzo Church. The Calculi of Lambda-Conversion, volume 6 of Annals of Mathematics Studies.
  Princeton University Press, 1941.

E XTENDED V ERSION                                                           F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                  29


Michael Dummett. The Logical Basis of Metaphysics. Harvard University Press, Cambridge,
 Massachusetts, 1991. The William James Lectures, 1976.

Gerhard Gentzen. Untersuchungen über das logische Schließen. Mathematische Zeitschrift,
 39:176–210, 405–431, 1935. English translation in M. E. Szabo, editor, The Collected Papers
  of Gerhard Gentzen, pages 68–131, North-Holland, 1969.

Jean-Yves Girard. Linear logic. Theoretical Computer Science, 50:1–102, 1987.

Jean-Yves Girard and Yves Lafont. Linear logic and lazy computation. In H. Ehrig,
  R. Kowalski, G. Levi, and U. Montanari, editors, Proceedings of the International Joint Con-
  ference on Theory and Practice of Software Development, volume 2, pages 52–66, Pisa, Italy,
  March 1987. Springer-Verlag LNCS 250.

Peter Hanukaev and Harley Eades, III. Combining dependency, grades, and adjoint logic.
  In 8th Workshop on Type-Driven Development (TyDe 2023), pages 58–70, Seattle, Washing-
  ton, 2023. ACM. URL https://arxiv.org/abs/2307.09563.

Robert Harper. Practical Foundations for Programming Languages. Cambridge University
  Press, second edition, April 2016.

W. A. Howard. The formulae-as-types notion of construction. Unpublished note. An an-
 notated version appeared in: To H.B. Curry: Essays on Combinatory Logic, Lambda Calculus
 and Formalism, 479–490, Academic Press (1980), 1969.

Jack Hughes and Dominic Orchard. Resourceful program synthesis from graded linear
  types. In M. Fernández, editor, 30th International Symposium on Logic-Based Program Syn-
  thesis and Transformation (LOPSTR 2020), pages 151–170, Bologna, Italy, September 2020.
  Springer LNCS 12561.

Max Kanovich, Stepan Kuznetsov, Vivek Nigam, and Andre Scedrov. Subexponentials in
 non-commutative linear logic. ArXiv e-prints, September 2017.

Max Kanovich, Stepan Kuznetsov, Vivek Nigam, and Andre Scedrov. A logical framework
 with commutative and non-commutative subexponentials. In International Joint Confer-
 ence on Automated Reasoning (IJCAR 2018), pages 228–245. Springer LNAI 10900, 2018.

Stephen Cole Kleene. Introduction to Metamathematics. North-Holland, 1952.

John Launchbury. A natural semantics for lazy evaluation. In 20th Annual Symposium
  on Principles of Programming Languages (POPL 1993), pages 144–154, Charleston, South
  Carolina, January 1993. ACM.

Paul Blain Levy. Call-by-push-value: Decomposing call-by-value and call-by-name.
  Higher-Order and Symbolic Computation, 19(4):377–414, 2006.

Daniel R. Licata and Michael Shulman. Adjoint logic with a 2-category of modes. In
 International Symposium on Logical Foundations of Computer Science (LFCS), pages 219–235.
 Springer LNCS 9537, January 2016.


E XTENDED V ERSION                                                          F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                   30


Daniel R. Licata, Michael Shulman, and Mitchell Riley. A fibrational framework for sub-
 structural and modal logics. In Dale Miller, editor, Proceedings of the 2nd International Con-
 ference on Formal Structures for Computation and Deduction (FSCD’17), pages 25:1–25:22,
 Oxford, UK, September 2017. LIPIcs.

Per Martin-Löf. On the meanings of the logical constants and the justifications of the log-
  ical laws. Notes for three lectures given in Siena, Italy. Published in Nordic Journal of
  Philosophical Logic, 1(1):11-60, 1996, April 1983.

Benjamin Moon, Harley Eades III, and Dominic Orchard. Graded modal dependent type
  theory. In 30th European Symposium on Programming (ESOP’21), volume 12648 of Lecture
  Notes in Computer Science, pages 462–490. Springer, 2021.

Alan Mycroft. The theory and practice of transforming call-by-need into call-by-value. In
  4th International Symposium on Programming, pages 269–281. Springer LNCS 83, 1980.

Aleksandar Nanevski, Frank Pfenning, and Brigitte Pientka. Contextual modal type the-
  ory. Transactions on Computational Logic, 9(3), 2008.

Vivek Nigam and Dale Miller. Algorithmic specifications in linear logic with subexpo-
  nentials. In Proceedings of the 11th International Conference on Principles and Practice of
  Declarative Programming (PPDP), pages 129–140, Coimbra, Portugal, sep 2009. ACM.

Vivek Nigam, Elaine Pimental, and Giselle Reis. An extended framework for specifying
  and reasoning about proof systems. Journal of Logic and Computation, 26(2):539–576, 2016.

Frank Pfenning and Rowan Davies. A judgmental reconstruction of modal logic. Mathe-
  matical Structures in Computer Science, 11:511–540, 2001. Notes to an invited talk at the
  Workshop on Intuitionistic Modal Logics and Applications (IMLA’99), Trento, Italy, July 1999.

Frank Pfenning and Klaas Pruiksma. Relating message passing and shared memory, proof-
  theoretically. In S. Jongmans and A. Lopes, editors, 25th International Conference on Co-
  ordination Models and Languages (COORDINATION 2023), pages 3–27, Lisbon, Portugal,
  June 2023. Springer LNCS 13908. Notes to an invited talk.

Dag Prawitz. Natural Deduction. Almquist & Wiksell, Stockholm, 1965.

Klaas Pruiksma. Adjoint Logic with Applications. PhD thesis, Carnegie Mellon University,
  2024. In preparation.

Klaas Pruiksma and Frank Pfenning. A message-passing interpretation of adjoint logic.
  Journal of Logical and Algebraic Methods in Programming, 120(100637), 2021.

Klaas Pruiksma and Frank Pfenning. Back to futures. Journal of Functional Programming,
  32:e6, 2022.

Klaas Pruiksma,  William Chargin,  Frank Pfenning,   and Jason                           Reed.
  Adjoint logic.       Unpublished manuscript, April  2018.                               URL
  http://www.cs.cmu.edu/˜fp/papers/adjoint18b.pdf.


E XTENDED V ERSION                                                          F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                   31


Jason Reed. A judgmental deconstruction of modal logic. Unpublished manuscript, May
  2009. URL http://www.cs.cmu.edu/˜jcreed/papers/jdml2.pdf.

Rust. The Rust programming language. Available at https://www.rust-lang.org/.
  Accessed January 15, 2024.

Jesse A. Tov and Riccardo Pucella. Practical affine types. In T. Ball and M. Sagiv, editors,
  Proceedings of the 38th Symposium on Principles of Programming Languages (POPL 2011),
  pages 447–458. ACM Press, January 2011.

Anne S. Troelstra. Natural deduction for intuitionistic linear logic. Annals of Pure and
 Applied Logic, 73(1):79–108, 1995.

Philip Wadler. Linear types can change the world. In IFIP TC, volume 2, pages 347–359,
  1990.

Philip Wadler. Propositions as sessions. In Proceedings of the 17th International Conference on
  Functional Programming (ICFP 2012), pages 273–286, Copenhagen, Denmark, September
  2012. ACM Press.

James Wood and Robert Atkey. A framework for substructural type systems. In Ilya Sergey,
  editor, 31st European Symposium on Programming (ESOP 2022), pages 376–402, Munich,
  Germany, April 2022. Springer LNCS 13240.




E XTENDED V ERSION                                                          F EBRUARY 2, 2024
Adjoint Natural Deduction                                                                           32




   Γ ⊢ s =⇒ Am / Ξ                 Γ ⊢ e ⇐= Am / Ξ                         x : Am ∈ Γ
                      ⇒/⇐                                   ⇐/⇒                               hyp
   Γ ⊢ s ⇐= Am / Ξ              Γ ⊢ (e : Am ) =⇒ Am / Ξ              Γ ⊢ x =⇒ (x : Am )

                                Γ, x : Am ⊢ e ⇐= Bm / Ξ
                                                                     ⊸I
                       Γ ⊢ λx. e ⇐= Am ⊸ Bm / (Ξ \ x : Am )

                     Γ ⊢ s =⇒ Am ⊸ Bm / Ξ Γ ⊢ e ⇐= Am / Ξ′
                                                                          ⊸E
                                 Γ ⊢ s e =⇒ Bm / Ξ ; Ξ′

                                              Γ ⊢ eℓ ⇐= Aℓm / Ξℓ       (∀ℓ ∈ L 6= ∅)
                                NI0                                                           NI
   Γ ⊢ { } ⇐= Nm { } / [Γ|m ]            Γ ⊢ {ℓ ⇒ eℓ }ℓ∈L ⇐= N{ℓ : Aℓm }ℓ∈L / ⊔ℓ∈L Ξℓ

                         Γ ⊢ e =⇒ N{ℓ : Aℓm }ℓ∈L / Ξ       (ℓ ∈ L)
                                                                     NE
                                   Γ ⊢ e.ℓ =⇒ Aℓm / Ξ

                 Γ ⊢ e ⇐= Ak / Ξ                         Γ ⊢ s =⇒ ↑m
                                                                   k Ak / Ξ
                                            ↑I                                      ↑E
           Γ ⊢ susp e ⇐= ↑m
                          k Ak / Ξkm                   Γ ⊢ force s =⇒ Ak / Ξ

                       Γ ⊢ e1 ⇐= Am / Ξ          Γ ⊢ e2 ⇐= Bm / Ξ′
                                                                      ⊗I
                           Γ ⊢ (e1 , e2 ) ⇐= Am ⊗ Bm / Ξ ; Ξ′

       Γ ⊢ s =⇒ Am ⊗ Bm / Ξ           m≥r    Γ, x1 : Am , x2 : Bm ⊢ e′ ⇐= Cr / Ξ′
                                                                                         ⊗E
         Γ ⊢ match s ((x1 , x2 ) ⇒ e′ ) ⇐= Cr / Ξ ; (Ξ′ \ x1 : Am \ x2 : Bm )

                                      Γ ⊢ s =⇒ 1m / Ξ m ≥ r          Γ ⊢ e′ ⇐= Cr / Ξ′
                           1I                                                             1E
     Γ ⊢ ( ) ⇐= 1m / (·)                 Γ ⊢ match s (( ) ⇒ e′ ) ⇐= Cr / Ξ ; Ξ′

      Γ ⊢ e ⇐= Aℓm / Ξ     (ℓ ∈ L)                   Γ ⊢ s =⇒ ⊕m { } / Ξ       m≥r
                                       ⊕I                                                 ⊕E0
    Γ ⊢ ℓ(e) ⇐= ⊕{ℓ : Aℓm }ℓ∈L / Ξ                 Γ ⊢ match s ( ) ⇐= Cr / Ξ ; [Γ|r ]

   Γ ⊢ s =⇒ ⊕{ℓ : Aℓm }ℓ∈L / Ξ     m≥r      Γ, x : Aℓm ⊢ eℓ ⇐= Cr / Ξ′ℓ      (∀ℓ ∈ L 6= ∅)
                                                                                              ⊕E
             Γ ⊢ match s (ℓ(x) ⇒ eℓ )ℓ∈L ⇐= Cr / Ξ ; ⊔ℓ∈L (Ξ′ℓ \ x : Aℓ )

                                      Γ ⊢ e ⇐= An / Ξ
                                                              ↓I
                                Γ ⊢ down e ⇐= ↓nm An / Ξ

              Γ ⊢ s =⇒ ↓nm An / Ξ m ≥ r           Γ, x : An ⊢ e′ ⇐= Cr / Ξ′
                                                                               ↓E
               Γ ⊢ match s (down x ⇒ e′ ) ⇐= Cr / Ξ ; (Ξ′ \ x : An )


                  Figure 6: Algorithmic Typing for Natural Deduction


E XTENDED V ERSION                                                              F EBRUARY 2, 2024
