                                                                 What are the Right Symmetries
                                                                 for Formal Theorem Proving?


                                                           Krzysztof Olejniczak1 Radoslav Dimitrov Xingyue Huang1
                                                        Bernardo Cuenca Grau1 Jinwoo Kim∗ 2 İsmail İlkan Ceylan* 3,4,1
                                                             1
                                                               University of Oxford 2 KAIST 3 TU Wien 4 AITHYRA
arXiv:2605.22257v1 [cs.LG] 21 May 2026




                                                                                             Abstract
                                                     Formal theorem provers based on large language models (LLMs) are highly sen-
                                                     sitive to superficial variations in problem representation: semantically equivalent
                                                     statements can exhibit drastically different proof success rates, revealing a fail-
                                                     ure to respect structural symmetries inherent in formal mathematics. This raises
                                                     a central question: what are the right symmetries for formal theorem proving?
                                                     We introduce rewriting categories, a category-theoretic framework capturing the
                                                     compositional, generally non-invertible transformations induced by proof tactics,
                                                     and use it to formalize two symmetry notions: proof equivariance, governing
                                                     how proof distributions transform under rewrites, and success invariance (i.e.,
                                                     invariance of success probability), requiring equivalent statements to be solved
                                                     with the same probability. We observe that state-based next-tactic provers naturally
                                                     satisfy proof equivariance by operating on proof states. In contrast, state-of-the-art
                                                     LLM-based provers satisfy neither property, exhibiting large performance variation
                                                     across equivalent formulations. To mitigate this, we propose test-time methods
                                                     that aggregate over equivalent rewritings of the input, showing theoretically that
                                                     they recover success invariance in the sampling limit, and empirically, that they
                                                     improve robustness and performance under fixed inference budgets. Our results
                                                     highlight symmetry as a key missing inductive bias in LLM-based theorem proving
                                                     and suggest test-time computation as a practical route to approximate it.


                                            1) Commuting arguments                 2) Algebraic transformations               3) Alternative formulations


                                           theorem number_theory_1 :       theorem algebra_1 (n : N) (h0 : n % 2 = 0)         theorem induction_1 (n : N)
                                             Nat.gcd 200000 20! = 40000      (h1 : (n-2)*(n-2) + n*n + (n+2)*(n+2) = 12296)     : (20 + 4 * 4^n) % 12 = 0
                                                                             : (n * (n+2) * (n-2)) / 8 = 32736

                                             Success rate: 63/64 (98.4%)              Success rate: 32/64 (50.0%)              Success rate: 62/64 (96.9%)


                                           theorem number_theory_2 :       theorem algebra_2 (n : N) (h0 : Even n)            theorem induction_2 (n : N)
                                             Nat.gcd 20! 200000 = 40000      (h1 : (n-2) ^ 2 + n ^ 2 + (n+2) ^ 2 = 12296)       : 12 | 4^(n + 1) + 20
                                                                             : (n-2) * n * (n+2) / 8 = 32736

                                             Success rate: 44/64 (68.9%)               Success rate: 3/64 (4.7%)               Success rate: 13/64 (20.3%)



                                         Figure 1: Sensitivity of DeepSeek-Prover-V2 [1] to semantics-preserving rewrites. Each pair of
                                         statements is mathematically equivalent, yet exhibits drastically different proof success rates under
                                         minor transformations. This highlights a systematic violation of symmetry: the prover’s success
                                         probability depends strongly on the representation instead of the underlying mathematical content.
                                            ∗ Equal advising.



                                         Preprint.
1     Introduction
Large language model (LLM) theorem provers, operating on textual representations of formal
statements, are highly sensitive to how problems are expressed [2, 3]. As shown in Figure 1, even
simple, semantics-preserving rewrites, such as reordering arguments, applying elementary algebraic
transformations, or alternative notation, can lead to drastic changes in proof success rates. In some
cases, a theorem that is solved nearly always becomes almost unsolvable under another formulation,
despite the two statements being mathematically equivalent. This behavior, widely observed in
mathematical reasoning and language understanding [4–8], reveals a fundamental limitation of
current systems: failure to generalize across different representations of the same problem.
LLM-based provers [9–11] process statements as text,
                                                                Original statement
making their behavior depend on surface form instead of
                                                                theorem T (x : R) (h : x > 1) : . . . := by
the underlying mathematical structure. This discrepancy
motivates a central question: what are the right symme-
                                                                      replace h : x > 0 := by linarith
tries for formal theorem proving? In classical machine
learning, symmetries are typically modeled via group ac-
                                                                Updated statement
tions [12], which capture invertible transformations such
                                                                theorem T (x : R) (h : x > 0) : . . . := by
as rotations or permutations. However, this framework
is insufficient for formal reasoning. In proof assistants
                                                          Figure 2: An example of tactic irreversibil-
such as Lean [13], transformations between statements
                                                          ity in Lean. Applying a tactic transforms
arise via sequences of tactics, which are generally non-
                                                          x > 1 into x > 0, losing information.
invertible and may discard information (see Figure 2).
Consequently, the resulting transformation space cannot be characterized by group symmetries alone.
In this work, we introduce rewriting categories, a category-theoretic framework for modeling trans-
formations between theorem statements. This perspective allows us to formalize two symmetry
notions for formal theorem provers: proof equivariance, which requires proof distributions to
transform consistently along rewrites, and success invariance (i.e., invariance of success probability),
which requires equivalent statements to be solved with the same probability. Proof equivariance is
naturally satisfied by next-tactic predictors [10, 14, 15] when used generate proofs sequentially from
intermediate proof states. On the other hand, modern state-of-the-art LLM-based provers [1, 16–18]
satisfy neither property, exhibiting large variability across equivalent formulations.
We show that this lack of symmetry can be mitigated by aggregating over equivalent rewritings of
the input statement. We prove that such procedures recover success invariance in the sampling limit,
and empirically demonstrate improved robustness and performance under fixed inference budgets.
These results suggest that symmetry, defined in a categorical sense, is a key missing inductive bias in
current LLM-based theorem provers, and that it can be effectively approximated through test-time
computation without modifying the underlying model. Our contributions can be summarized as2 :
(1) Category-theoretic framework. We introduce rewriting categories, a category-theoretic frame-
    work for modeling transformations between formal theorem statements, and formalize two
    symmetry notions: proof equivariance and success invariance.
(2) Empirical analysis of invariance. We construct miniF2F-rw, a benchmark consisting of seman-
    tically equivalent reformulations of formal problems, and show that state-of-the-art LLM-based
    provers exhibit large violations of success invariance.
(3) Test-time invariance. We propose a simple, model-agnostic test-time procedure that aggregates
    over equivalent rewritings of the input, and theoretically prove that this approach recovers success
    invariance in the sampling limit.
(4) Competitive performance. We demonstrate empirically that the proposed method improves
    both robustness to input reformulations and overall proof success under fixed inference budgets.

2     Formal theorem proving in Lean
Theorem proving in Lean. Formal theorem proving in Lean is structured around transformations
of proof states [13]. A theorem statement is compiled into an initial state representing assumptions
and goals, and proofs are constructed by applying sequences of tactics that transform this state until
no goals remain. This operational view exposes a key structural property: transformations between
statements arise through sequences of tactics, which are compositional but generally non-invertible.
    2 Code available at: https://github.com/kolejnyy/rw-ensembles




                                                             2
 Lean theorem statement T1 ∈ Stmt                       Mathlib lemma                                    Resulting proof
 theorem thm1 (x y : N) (h0 : Nat.lcm x y = 12)         theorem Nat.gcd_mul_lcm (x y : N)                theorem thm1 (x y : N) (h0 : Nat.lcm x y = 12)
   (h1 : Nat.gcd x y = 2) : x * y = 24 := by              : x.gcd y * x.lcm y = x * y                      (h1 : Nat.gcd x y = 2) : x * y = 24 := by
                                                                                                           rw [← Nat.gcd_mul_lcm x y]
                                                                                                           norm_num [h0 , h1 ]
                          compile


           Compiled state L(T1 ) ∈ Ω                                          Updated state
                                             rw [← Nat.gcd_mul_lcm x y]                                        norm_num [h0 , h1 ]
          xy: N                                                               xy: N                                                    Updated state
          h0 : x.lcm y = 12                                                   h0 : x.lcm y = 12
          h1 : x.gcd y = 2                                                    h1 : x.gcd y = 2                                         no goals

           ⊢ x * y = 24                                                       ⊢ x.gcd y * x.lcm y = 24



Figure 3: An example of a successful proof in Lean. The original statement T is converted into
an initial state L(T ), and tactics are then sequentially executed, until the empty state ∅ is reached.


Formally, let Stmt denote the set of all valid theorem statements, T the set of all tactics, and Ω the
set of all Lean states, with Ω containing an empty state ∅ (no remaining goals) and an error state ⊥
(failure during compilation). Given a theorem T , we will write L(T ) for the corresponding state.
Each tactic t ∈ T can be seen as a function t : Ω → Ω. In this view, a sequence of tactics
t = (t1 , . . . , tk ) is a valid proof of a statement T , if their composition maps L(T ) to the empty state:
                                         t(L(T )) = (tk ◦ tk−1 ◦ · · · ◦ t1 )(L(T )) = ∅.

Formal LLM-based provers. We focus on single-pass whole-proof generation models [1, 16–18].
In this setting, an LLM defines a distribution pθ (· | T ) over sequences of tactics (i.e., candidate
proofs), conditioned on a Lean statement T . The success rate sθ (T ) is then the probability that a
sampled sequence of tactics t transforms the initial state L(T ) into ∅:
                                        X
                            sθ (T ) :=      pθ (t | T ) 1(t(L(T )) = ∅)
                                                              t

Importantly, both the input theorems and output proofs are represented as text.
The structure of Lean statement space. In Lean, transformations between statements arise through
sequences of tactics acting on proof states, linking statements T and T ′ whenever L(T ′ ) = t(L(T )).
While it is tempting to model this structure via group actions, such an abstraction is inappropriate.
These transformations are compositional but generally non-invertible: multiple statements may map
to the same state, and tactic application can discard information, preventing reversal. As a result, the
transformation structure cannot be captured by group symmetries.

3     Formalization of mathematical symmetries via rewriting categories
We now formalize the transformations described in Section 2 using category theory. We model
theorem statements as objects and transformations between them as composable, generally non-
invertible morphisms. This induces a categorical structure that captures the behavior of tactics, which
we refer to as a rewriting category. This framework provides the foundation for defining symmetry in
formal theorem proving and explains inductive biases present in prior works as special cases.

3.1     Category theory preliminaries

We recall the basic categorical notions needed for our construction; see Appendix A for more details.
Definition 1 (Category). A category C consists of
    • a collection of objects ob(C ),
    • for each A, B ∈ ob(C ), a collection C (A, B) of maps or arrows from A to B,
    • for each pair of arrows f ∈ C (A, B) and g ∈ C (B, C), their composition g ◦ f ∈ C (A, C),
    • for each object A ∈ ob(C ), an element 1A of C (A, A), called the identity on A,
satisfying the following axioms:
    • associativity: (h ◦ g) ◦ f = h ◦ (g ◦ f ) for any f ∈ C (A, B), g ∈ C (B, C) and h ∈ C (C, D),
    • identity laws: for each f ∈ C (A, B), we have f ◦ 1A = f = 1B ◦ f .
                                                                                                         f
We often write A ∈ C to mean A ∈ ob(C ), and f : A → B or A −    → B to mean f ∈ C (A, B). We
will also write A ⇆ B for objects A, B ∈ C such that there exist arrows A → B and B → A in C .


                                                                          3
When for all objects A, B ∈ C , there is an arrow A → B if and only if there is an arrow B → A, we
call C reciprocal. If categories C and D satisfy ob(C ) ⊆ ob(D), and for every A, B ∈ C , we have
C (A, B) ⊆ D(A, B), we call C a subcategory of D, denoted as C ⊆ D.
Example 2. There is a category Set whose objects are sets, whose maps are functions between sets,
with function composition as composition and identity functions as identities.
The following example instantiates this structure for Lean theorem proving.
Example 3. There is a full tactic rewriting category RT , whose objects are Lean statements Stmt
and arrows represent sequences of tactics. More precisely, if statements T, T ′ ∈ Stmt satisfy
L(T ′ ) = t(L(T )) for some sequence of tactics t, there is an arrow t : T → T ′ . Identities correspond
to the empty sequence of tactics, representing no action. Composition becomes concatenation:
                                                                  t      t′
                          t′ ◦ t = [t : t′ ]   whenever          − T′ −
                                                               T →    → T ′′

To let categories act on concrete data, we use structure-preserving maps, called functors:
Definition 4 (Functor). A functor F : C → D consists of an object map F : ob(C ) → ob(D), and,
for each pair A, B ∈ ob(C ), an assignment on arrows, F : C (A, B) → D(F (A), F (B)), satisfying:
                                                                               f      g
   • preservation of composition: F (g ◦ f ) = F (g) ◦ F (f ) whenever A −→B−  → C in C ,
   • preservation of identities: F (1A ) = 1F (A) for every A ∈ C .
Example 5. There is an implementation functor I : RT → Set mapping each theorem T ∈ Stmt to
the singleton set {T }, while arrows are mapped to the unique functions between singletons.

3.2   Rewriting categories

With the language of Section 3.1 in hand, we introduce the specific categorical objects we will use to
reason about semantics-preserving rewrites of theorem statements. Our goal is to define categories R
with Lean statements as objects, and whose arrows encode their transformations induced by tactics.
The maximal semantic rewriting category. Every T ∈ Stmt carries intended mathematical content,
and we posit an abstract maximal semantic rewriting category R ∗ whose objects are statements,
and arrows are all mathematically-sound transformations (including, but not limited to Lean tactics).
Concretely, there is an arrow a : T → T ′ in R ∗ for any logically valid argument a reducing T to T ′ .
Rewriting categories for Lean. In the general case, however, we do not have explicit access to R ∗
and hence consider subcategories of the tractable subcategory RT ⊆ R ∗ from Example 3.
Definition 6. A (Lean) rewriting category is a subcategory R ⊆ RT of RT with ob(R) = Stmt.
Of particular interest are rewriting categories R that restrict the allowed set of tactics. For a set
T ′ ⊆ T , we say that R is generated by T ′ if R is the inclusion-wise minimal rewriting category,
such that for all T, T ′ ∈ Stmt and t ∈ T ′ with L(T ′ ) = t(L(T )), there is an arrow t : T → T ′ in R.
Each such category encodes a specific, increasingly conservative notion of available transformations.
This hierarchy of subcategory approximations of R ∗ is used to scaffold our empirical study in
Section 5, where different rule sets yield augmentations of varying semantic strength, and the
sensitivity of a prover to the choice measures how far its behavior is from the invariance we desire.
With the rewriting category RT in place, and its restrictions R ⊆ RT , we are ready to define the
structural biases expected from formal provers. We begin with the notion of R-equivariance of the
proof distribution, ensuring that the structures of solutions produced by the prover align with R.

3.3   Proof equivariance

If for a pair of statements T, T ′ ∈ Stmt, a tactic t ∈ T transforms L(T ) into L(T ′ ), then any proof t
of T ′ can be lifted to a proof of T by concatenating t at the beginning, i.e., [t : t]. This observation
motivates an equivariance property for formal provers pθ . Formally, this corresponds to transporting
distributions along arrows in the rewriting category. Intuitively, the distribution pθ ([t : ·] | T ) of
completions of proofs of T that start with t should match the distribution of proofs for T ′ . If a prover
pθ meets this condition, improving its performance on T ′ would automatically translate to increased
performance on T , for proofs that start with t. To ensure that this distribution transport is well-defined
and unambiguous, we will assume the following:


                                                    4
Assumption 7. Denote by T ∗ the space of finite sequences of Lean tactics, and let D+ (T ∗ ) be the
set of distributions over T ∗ , assigning non-zero probability to each element t ∈ T ∗ . Let T ∈ Stmt.
Given T , pθ has a non-zero probability of producing any proof t ∈ T ∗ , i.e. pθ (· | T ) ∈ D+ (T ∗ ).
Assumption 7 holds, in principle, for various classes of models, including LLMs, relying on logit-
based next-token sampling. The concept of proof transport can now be defined in terms of functors:
Definition 8 (Proof functor). The (stochastic) proof functor on R is the functor P : R → Set that
maps each object T ∈ R to P(T ) = D+ (T ∗ ), and whose action on arrows t : T → T ′ is defined as:
                      [P(t)](ν)(t′ ) ∝ ν([t : t′ ])  ∀ν ∈ D+ (T ∗ ), t′ ∈ T ∗
In words, for any arrow t : T → T ′ in R, P(t) : D+ (T ∗ ) → D+ (T ∗ ) is a function mapping each
distribution ν ∈ D+ (T ∗ ) to its restriction over proofs that start with t. The proof of functoriality of
P is presented in Appendix E.1. Using proof functors, we can formalize the property outlined above:
Definition 9 (R-equivariance of proof distribution). Let P : R → Set be the proof functor.
A prover pθ is R-equivariant in proof distribution if
                pθ (· | T ′ ) = P(t)(pθ (· | T ))     for every arrow t : T → T ′ in R.
Under Assumption 7, this is a well-typed definition. R-equivariant provers, correspond precisely to
natural transformations I → P, which we properly introduce and elaborate on in Appendix B.1. Im-
portantly, a prover satisfying Definition 9 assigns structurally matched proofs matching probabilities,
allowing for generalization between any pair of problems linked by an arrow in R.
Proof equivariance in the literature. Although Lean proof equivariance has not been formalized
previously, some approaches share closely related inductive biases. In particular, next-tactic predic-
tors [10, 14, 15] operate on intermediate proof states rather than theorem statements, and can satisfy
RT -equivariance. Note, however, that this symmetry breaks when these models rely on a search under
fixed budgets (Appendix B.3). Moreover, their multi-step training introduces optimization challenges,
often resulting in weaker performance than single-pass provers. At the same time, incorporating such
bias into whole-proof generation models would require severe architectural changes.
Consequently, in this work, we focus on an adjacent notion of bias for formal provers, defined by the
invariance of the success probability across statements that share the same mathematical content.

3.4   Success invariance

Proof R-equivariance, stated in Section 3.3, requires proof distributions to transfer according to
the arrows of a rewriting category R. With the examples from Figure 1 in mind, a less restrictive
condition could require the prover to achieve the same success rate on problems equivalent w.r.t R:
Definition 10 (R-equivalent statements). We say that statements T, T ′ ∈ R are R-equivalent,
denoted as T ∼R T ′ , if T ⇆ T ′ in R, i.e. there exist some arrows t : T → T ′ and t′ : T ′ → T .
The motivation behind Definition 10 is the ability to transform valid proofs between T and T ′ via
the arrows of R. We encapsulate the ability of models to perform such transfer by requiring that
the probabilities of success of solving R-equivalent statements are equal:
Definition 11 (Success invariance). A prover pθ is R-invariant in success probability if
                              sθ (T ) = sθ (T ′ )  for every T ∼R T ′ .
Setting R = R ∗ recovers the informal notion of success invariance. An R-invariant prover respects
the transformations assigned by R and guarantees that R-equivalent problems are correctly solved
with the same probability. Therefore, improvement on solving a specific theorem T directly translates
to improvements over the whole equivalence class [T ]R .
A hierarchy of invariances. Under R ∗ ⊇ RT ⊇ R of Section 3.2, we obtain the implications
                    R ∗
                                } =⇒ RT -invariance =⇒ R-invariance
                    | -invariance
                         {z
                     ideal success invariance
This hierarchy formalizes progressively weaker but more tractable notions of invariance. Invariance
with respect to the unreachable maximal category R ∗ is the strongest, capturing what we ideally
want from a prover. Restricting to a tractable subcategory R ⊆ RT is a necessary condition that we
can computationally evaluate. Our methodology pursues the latter, and the observed variance can be
seen as a lower bound on the error of R ∗ -invariance.

                                                    5
4     Test-time scaling with rewriting for success invariance
Section 3.4 formalizes success invariance of a prover pθ with respect to a rewriting category R ⊆ RT .
We now address how to realize this property in practice. Prior work [3] encourages invariance through
training-time data augmentation, but is limited to a small set of transformations and requires retraining.
Instead, we seek a test-time method that, given an already-trained pθ that may not satisfy success
invariance, produces another prover p̄θ that is (approximately) R-invariant, without retraining pθ .
Our construction is inspired by sampling and canonicalization strategies for group invariance [19–24].

4.1   The rewriting ensemble

We take the rewriting subcategory R ⊆ RT from Section 3.2 as fixed, together with a sampling
procedure µ(· | T, k) that, given a theorem statement T ∈ Stmt and a number k, returns k theorems
T1 , . . . , Tk ∈ Stmt reachable from T via a finite chain of arrows in R. These variants approximate
the equivalence class [T ]R , and serve as alternative representations of the same underlying problem.
Definition 12 (Rewriting ensemble). Fix a prover pθ , budget N ∈ N and a variant count K ≤ N .
                                           (K,N )
The (K, N )-rewriting ensemble prover p̄θ,µ , applied to a statement T , proceeds as follows:
                                                                                                   ri
 (1) Sample K variants {T1 , . . . , TK } ∼ µ(· | T, K), with the corresponding transitions T −→      Ti .
 (2) Run pθ for ⌊N/K⌋ independent attempts on each Ti .
                                                                                                   ri
 (3) Return any resulting valid proof, verified with Lean, lifted to a proof of T via the arrow T −→  Ti
     in R; return failure if no attempt succeeds.
Assuming independence of attempts, the expected success probability of the ensemble is
                                                            " K                         #
                 (K,N )
                                                              Y                ⌊N/K⌋
               s̄θ,µ (T ) = 1 − E{T1 ,...,TK } ∼ µ(·|T,K)          1 − sθ (Ti )
                                                              i=1
Two limiting cases are worth bearing in mind: K = 1 collapses the ensemble to running pθ on a
single random variant, and K = N spreads the budget one attempt per variant. Our analysis below
               (K,N )
concerns how s̄θ,µ (T ) depends on K, and how it compares across T ∼R T ′ .

4.2   Invariance in the sample-size limit

For the ensemble prover to satisfy the R-invariance of Definition 11, the sampling distribution
µ(· | T, K) must exhibit behavior generalizable over the whole equivalence class [T ]R . This is not
automatic, as following arrows from a statement T can, in general, reach different statements than
when starting in T ′ ∼R T . We hence assume that µ has syntactically invariant support:
Assumption 13 (Sampling coverage). Let T ∼R T ′ and let T ′′ ∈ R be a statement. Suppose that
for some K, the probability P(T ′′ ∈ µ(· | T, K)) of sampling T ′′ is greater than 0. Then:
                     lim P(T ′′ ∈ µ(· | T, K)) = lim P(T ′′ ∈ µ(· | T ′ , K)) = 1
                   K→∞                             K→∞
              ′′
In words, if T can be sampled for some input theorem T , as the number of samples tends to infinity,
it will eventually be sampled for any member of the equivalence class [T ]R . Assumption 13 holds in
two cases of interest: (i) when µ(· | T, K) eventually covers every state T ′′ reachable from T in R,
and (ii) when the sampler performs canonicalization [21] and outputs a fixed representative of [T ]R .
Proposition 14 (Invariance in the sample-size limit). Let n : N → N be a function such that
⌊n(x)/x⌋ → ∞ as x → ∞. Then, under Assumption 13:
                        (K,n(K))               (K,n(K))
                  lim s̄θ,µ      (T ) = lim s̄θ,µ       (T ′ )   for every T ∼R T ′ ,
               K→∞                       K→∞
so the limiting ensemble prover is R-invariant in success probability (Definition 11).
Informally, averaging over enough variants reachable from the full equivalence class washes out the
dependence on the particular initial theorem statement. The proof is provided in Appendix E.2.

4.3   Monotonicity in the number of rewritings
We now characterize the optimal number of variants of the input statement T , for reciprocal R,
regardless of the choice of sampling protocol µ. Assuming an equal prior on sθ (T ′ ) for all T ′ ∼R T ,
spreading the budget across more versions is never worse, in expectation, than committing to fewer:


                                                    6
Proposition 15 (Monotonicity). Let R be reciprocal and T ∈ Stmt be a statement. Assume that for
any T ′ ∼R T , the success probability sθ (T ′ ) ∈ [0, 1] is an independent random variable sampled
from some (prior) distribution P[T ]R . Then, for any budget N and divisors K ≤ K ′ of N ,
                                         (K,N )             (K ′ ,N )
                                     s̄θ,µ        (T ) ≤ s̄θ,µ          (T ),
with strict inequality whenever K < K ′ and sθ is non-constant on the support of µ(· | T, K) ⊆ [T ]R .
                                (K,N )             (1,N )
Corollary 16. In particular, s̄θ,µ       (T ) ≥ s̄θ,µ (T ) for every K ≥ 1 dividing N .
The proof of Proposition 15 is given in Appendix E.3. Note that whenever sθ (T ) > 0, repeated
sampling [25] without rewriting also achieves s̄ → 1 as N → ∞, a property the ensemble does not
improve on asymptotically. The value of the rewriting ensemble is therefore at a finite budget N . Our
empirical results in Section 6 instantiate this comparison at budgets of practical interest.

5    Methodology
Motivated by the sensitivity of LLM-based formal provers to specific formulations of theorems, and
the guarantees from Section 4, we design our experiments to study the following questions:
 (Q1) How far from success invariance are the modern LLM-based single-pass formal provers?
 (Q2) Can rewriting ensembles improve their robustness, and even increase performance?
We introduce the miniF2F-rw dataset, consisting of verified, RT -equivalent rewritings of problems
from miniF2F [26] and use it to test the robustness of leading open-source models [1, 16–18]. We
then confirm the beneficial impact of rewriting ensembles in two settings: controlled, using the
verified variants from miniF2F-rw, and test-time, producing reformulations at inference time.
Online augmentations. Augmenting formal statements is substantially harder than query rewriting
in natural language tasks [27–29] due to strict syntactic constraints (Appendix C.1). To address this,
we devise a three-stage test-time rewriting algorithm, outlined below and detailed in Appendix C.3:
    (1) Sampling. Rewrites are drawn from the rewriting category R generated by non-conditional
        lemmas from Mathlib [30] supplemented with a small set of simplification tactics.
    (2) Scoring. Each sampled variant is ranked by a model-based energy function [20], based on the
        model’s surprise when processing the input theorem, which acts as a cheap proxy for sθ .
    (3) Selection. The top-scoring variants, together with the seed, are passed to the prover.
Benchmarks. We propose miniF2F-rw benchmark, built on top of miniF2F [26]. Each of the 488
original problems is paired with 5-15 rewrites, each with a Lean certificate of semantic equivalence,
yielding roughly 5700 statements in total. All variants were additionally manually filtered to remove
ones that changed mathematical content. For more details, see Appendix C.2. To further demonstrate
the potential of test-time ensembles, we use ProofNet [31], and Ineq-Comp [2] containing a ‘trans’
split, designed specifically to test robustness to transformations of its ‘seed’ problems.
Models. Following Tian et al. [3], we focus on leading open-source non-reasoning models in our
main experiments: DeepSeek-Prover-V2 [1], Goedel-Prover-DPO [16], and Goedel-Prover-SFT [16].
Reasoning provers produce thousands of tokens per proof [1, Table 3], which is prohibitive here. We
include smaller-scale evaluations of the robustness of chosen reasoning models in Appendix D.
Evaluation. On miniF2F-rw, we compare each prover in four configurations, under fixed budget k:
    • seed: all k attempts on the original statement (corresponds to miniF2F benchmark performance).
    • random: all k attempts on a single variant, drawn uniformly from the pool in miniF2F-rw.
    • controlled: 8 variants drawn uniformly from the pool; budget split to k8 attempts per variant.
    • test-time: seed + 7 variants sampled online; budget split to k8 attempts per variant.
We report PASS@k at three budgets, k ∈ {8, 32, 64}. Each variant is attempted n = 64 times. As the
results for random and controlled depend on the drawn variants, we sample 20,000 variant selections
and report the mean and standard deviation. An ablation on the ensemble size is in Appendix C.4.
We further evaluate seed and test-time mode for chosen provers on ProofNet [31] and Ineq-Comp [2].
For the latter, in addition to PASS@k, we also measure the ratio of PASS@k results on the ‘trans’
and ‘seed’ splits, displaying provers’ generalizability to problems with similar proof structures [2, 3].
We compare their results against EvolProver [3], which proposed training data augmentations for
implicitly learning generalization over equivalent formulations during training time.

                                                        7
Table 1: PASS@k results of selected LLM provers on the miniF2F-rw benchmark. The best result for
each prover on each split is highlighted as bold, and the second-best is underlined.
                                                                    miniF2F-rw-valid                         miniF2F-rw-test
        Model                            Variant         k=8            k = 32     k = 64         k=8          k = 32          k = 64
                                         seed            57.7           62.8       64.8           51.7         56.5            57.8
                                         random          51.6±0.9       58.2±0.9   60.9±1.1       47.4±0.8     53.3±0.9        55.2±1.0
        Goedel-Prover-SFT [16]
                                         controlled      54.7±0.2       60.8±0.2   63.4±0.2       50.0±0.1     55.7±0.1        57.4±0.2
                                         test-time       56.3           62.6       63.6           50.5         56.0            57.6
                                         seed            58.6           63.1       64.3           52.9         57.7            59.0
                                         random          53.9±1.0       59.7±1.0   61.6±1.2       49.5±0.9     54.7±1.0        56.4±1.1
        Goedel-Prover-DPO [16]
                                         controlled      57.7±0.2       63.4±0.2   65.4±0.3       52.6±0.2     57.9±0.2        59.9±0.2
                                         test-time       57.7           63.5       65.2           49.1         55.5            57.1
                                         seed            78.4           79.1       79.5           61.7         64.6            66.8
                                         random          71.1±1.1       74.1±1.1   75.3±1.2       59.7±0.9     63.2±1.0        64.8±1.1
        DeepSeek-Prover-V2-7B [1]
                                         controlled      77.2±0.3       79.7±0.3   80.8±0.4       64.0±0.3     67.3±0.3        68.8±0.3
                                         test-time       79.7           81.1       81.5           62.6         66.0            67.6


    Table 2: The comparison between test-time ensembles and baselines on the considered datasets.
             Model                                    Budget   ProofNet-test   Ineq-Comp-seed   Ineq-Comp-trans   Ineq-Comp-ratio

             EvolProver [3]                             32          –              52.2              34.0               65.2

                                                        32        13.6             40.5              12.3             30.4%
             Goedel-Prover-DPO [16]
                                                        64        14.5             44.0              15.3             34.8%

                                                        32        15.6             42.3              14.5             34.3%
             Goedel-Prover-DPO + Ensemble
                                                        64        16.8             46.6              17.0             36.5%

                                                        32        21.9             64.8              34.8             53.7%
             DeepSeek-Prover-V2-7B [1]
                                                        64        23.1             66.7              37.3             55.9%

                                                        32        21.9             63.4              40.8            64.4%
             DeepSeek-Prover-V2-7B + Ensemble
                                                        64        23.2             64.7              45.5            70.3%



6     Evaluation results
Success invariance. Results on miniF2F-rw (Table 1) reveal a consistent drop in performance under
random perturbations relative to the seed baseline for all tested models, confirming their sensitivity
to input formulation. Interestingly, this degradation is substantially larger on the validation split. For
example, at PASS@8, DeepSeek-Prover-V2 drops by 7.3 points on the validation split, compared to
only 2.0 on test. This reveals its dependence on surface structures witnessed during model selection.
Rewriting ensembles effectively mitigate this gap. Both controlled and test-time variants significantly
outperform single random rewrites (e.g., +4% PASS@64 for DeepSeek on test), while additionally
reducing variance. Notably, despite their bias toward original statements, both Goedel-Prover-DPO
and DeepSeek-Prover-V2 benefit from ensembling, surpassing the seed baseline. This empirically val-
idates the theoretical advantages outlined in Section 4. Remarkably, DeepSeek-Prover-V2’s ensemble
performance is competitive with or surpasses reasoning at matched token counts (Appendix D.2).
Test-time ensembling. We compare seed baselines and test-time ensembles across benchmarks
(Table 2), using EvolProver as a retraining-based reference. Despite models’ bias toward seed formu-
lations in ProofNet-test and Ineq-Comp-seed, test-time ensembling consistently yields competitive or
improved performance over the baselines. On the main split of interest, Ineq-Comp-trans, rewriting
ensemble increases PASS@64 of DeepSeek-Prover-V2 from 37.3% to 45.5%, establishing a new
state of the art among non-reasoning models. The resulting robustness ratio is competitive with
EvolProver (65.2% vs 64.4% at PASS@32). This shows that our framework can efficiently reduce
sensitivity of underlying provers to surface forms of problems, without retraining.
Across all datasets, we observe cases where DeepSeek-Prover fails on the original formulation yet
consistently solves rewritten variants (Figure 4). In several examples, rewriting increases the success
rate from 0/64 on seed to 8/16, or even 16/16, on the reformulation. These results show that our
method discovers non-trivial rewrites that substantially improve solvability across diverse domains.

7     Related work
Statement augmentations. To evaluate the generalization of Lean provers across related problems,
Zhao et al. [2] introduces Ineq-Comp, a benchmark of inequality questions and their algebraic


                                                                          8
               miniF2F                             ProofNet                                 Ineq-Comp

 Seed                       0/64 SR    Seed                    0/64 SR   Seed                                         0/64 SR
 theorem mathd_algebra_362 (a b : R)   theorem exercise_1_1_17           theorem cauchy_p19 (x y z : R)
   (h0 : a ^ 2 * b ^ 3 = 32 / 27)        {G : Type*} [Group G] {x : G}     (hx : x > 0) (hy : y > 0) (hz : z > 0)
   (h1 : a / b ^ 3 = 27 / 4)             {n : N} (hxn : orderOf x = n)     (h : 1/(1 + x^2) + 1/(1 + y^2) + 1/(1 + z^2) = 2)
   : a + b = 8 / 3 := by                 : x^-1 = x^(n-1 : Z) := by        : x^2 + y^2 + z^2 + 3 ≥ (x + y + z)^2 := by

 Augmented                  2/16 SR    Augmented              16/16 SR   Augmented                                    8/16 SR
 theorem mathd_algebra_362 (a b : R)   theorem exercise_1_1_17           theorem cauchy_p19 (x y z : R)
   (h0 : a ^ 2 * b ^ 3 = 32 / 27)        {G : Type*} [Group G] {x : G}     (hx : 0 < x) (hy : 0 < y) (hz : 0 < z)
   (h1 : b ^ 3 / a = 4 / 27)             {n : N} (hxn : orderOf x = n)     (h : (1 + x^2)−1 + (1 + y^2)−1 + (1 + z^2)−1 = 2)
   : a + b = 8 / 3 := by                 : x^-1 = x^n * x^-1 := by         : (x + y + z)^2 ≤ x^2 + y^2 + z^2 + 3 := by

    Tactic used:                         Tactic used:                      Tactic used:
 rw [div_eq_div_iff_comm] at h1        rw [zpow_sub_one, zpow_coe_nat]   norm_num at *


 Figure 4: Examples of problems solved by the test-time ensemble framework, where seed failed.

transformations. While not strictly equivalent under our definition, these variants share the proof
structure, hence testing compositional reasoning. To address the observed robustness gap, EvolProver
[3] augments training data with fixed abstract syntax tree (AST) transformations, encoding common
symmetries. Our approach improves consistency through test-time augmentation, without retrain-
ing. FormalEvolve [32] showed that enforcing the generation of diverse reformulations of formal
statements benefits autoformalization [33, 34]; we extend this insight to LLM-based proof generation.
Equivalence of formal statements. Determining equivalence between formal theorems is a core
challenge in autoformalization, the task of mapping natural language problems to formal represen-
tations. Reliable evaluation requires accurately verifying equivalence with the ground truth. BEq
[35], defines equivalence via reducibility: T is equivalent to T ′ if T can be proved using T ′ , and vice
versa. In contrast, we adopt a perspective based on co-reachability in rewriting categories.
Structural representations in formal theorem proving. Prior work has explored explicit structural
encodings of formal statements [36–38], yet typically representing them as AST-based graphs
processed with graph neural networks. While these approaches naturally capture symmetries such as
variable renaming and commutativity, they have struggled to scale to harder problems compared to
LLM-based methods. To bridge this gap, Algebraic Positional Encodings (APE) [39] incorporate
algebraic structure, e.g., of binary trees, directly into the attention mechanisms. In [40], they were
applied to theorem proving by encoding inputs as ASTs and training models to exploit their structure.
Symmetries in deep learning. Symmetry is usually modeled as group actions [12] and incorporated
into neural networks either via weight sharing [41, 42], data augmentation [43, 44], or test-time
methods [19–24]. Prior works generalized to categories via monad algebras [45] or naturality [46],
although focusing on theorizing weight sharing. Bottou [47] posited that rewrite rules of natural
language [48, 49] may form a groupoid, a category with all arrows invertible, though not necessarily
preserving semantics. We extend these views, modeling semantics-preserving rewrites with a category,
using naturality to formulate invariance and equivariance, and realizing invariance at test time.

8    Summary, limitations, and future work
We frame Lean theorem proving in a category-theoretic framework, modeling statement augmen-
tations as arrows in rewriting categories. This perspective yields two symmetry principles for
LLM-based provers: success invariance and proof equivariance. We show that state-of-the-art provers
violate these properties, exhibiting strong sensitivity to equivalent reformulations. To address this,
we propose a test-time ensembling method that approximates invariance for arbitrary provers. We
provide theoretical guarantees and show improved robustness and performance across benchmarks.
We restrict our experiments with ensembles to non-reasoning provers. Although we expect the
qualitative picture to carry over to reasoning models, whether the magnitude of the achieved marginal
gains differs is left as an open question. Another natural extension is to increase the ensemble
expressivity, which currently uses a model-based energy function as a lightweight proxy for sθ .
A selector trained to predict proof success, or an adaptive bandit allocating compute across variants at
inference, are both possible next steps. A further idea is to incorporate our symmetry framework into
model design, e.g., by extending APE [39] to categorical structures. Lastly, outside the mathematical
domain, rewriting categories could be used to model symmetries of formal languages in programming
and logic [50, 51] (see Appendix B.5), as well as certain aspects of natural language [5, 6, 52, 53].


                                                               9
Acknowledgments
The authors would like to acknowledge the use of the University of Oxford Advanced Research
Computing (ARC) facility in carrying out this work. https://doi.org/10.5281/zenodo.22558. We also
would also like to thank Rob Cornish for helpful discussions.

References
 [1] ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue
     Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, et al. Deepseek-prover-v2: Advancing formal
     mathematical reasoning via reinforcement learning for subgoal decomposition. arXiv preprint
     arXiv:2504.21801, 2025.
 [2] Haoyu Zhao, Yihan Geng, Shange Tang, Yong Lin, Bohan Lyu, Hongzhou Lin, Chi Jin,
     and Sanjeev Arora. Ineq-comp: Benchmarking human-intuitive compositional reasoning in
     automated theorem proving on inequalities. In Advances in Neural Information Processing
     Systems, 2025.
 [3] Yuchen Tian, Ruiyuan Huang, WANG XUANWU, Jing Ma, Zengfeng Huang, Ziyang Luo,
     Hongzhan Lin, Da Zheng, and Lun Du. Evolprover: Advancing automated theorem proving
     by evolving formalized problems via symmetry and difficulty. In The Fourteenth International
     Conference on Learning Representations, 2026.
 [4] Seyed Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio,
     and Mehrdad Farajtabar. GSM-symbolic: Understanding the limitations of mathematical
     reasoning in large language models. In The Thirteenth International Conference on Learning
     Representations, 2025.
 [5] Alex Irpan, Alexander Matt Turner, Mark Kurzeja, David K Elson, and Rohin Shah. Consistency
     training helps stop sycophancy and jailbreaks. arXiv preprint arXiv:2510.27062, 2025.
 [6] Lukas Berglund, Meg Tong, Maximilian Kaufmann, Mikita Balesni, Asa Cooper Stickland,
     Tomasz Korbak, and Owain Evans. The reversal curse: LLMs trained on “a is b” fail to learn “b
     is a”. In The Twelfth International Conference on Learning Representations, 2024.
 [7] Zhaofeng Wu, Michihiro Yasunaga, Andrew Cohen, Yoon Kim, Asli Celikyilmaz, and Marjan
     Ghazvininejad. rewordbench: Benchmarking and improving the robustness of reward models
     with transformed inputs. In Proceedings of the 2025 Conference on Empirical Methods in
     Natural Language Processing, 2025.
 [8] Anjiang Wei, Jiannan Cao, Ran Li, Hongyu Chen, Yuhui Zhang, Ziheng Wang, Yuan Liu,
     Thiago SFX Teixeira, Diyi Yang, Ke Wang, et al. Equibench: Benchmarking large language
     models’ reasoning about program semantics via equivalence checking. In Proceedings of the
     2025 Conference on Empirical Methods in Natural Language Processing, 2025.
 [9] Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving.
     arXiv preprint arXiv:2009.03393, 2020.
[10] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
     Godil, Ryan J Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with
     retrieval-augmented language models. In Advances in Neural Information Processing Systems,
     2023.
[11] Huajian Xin, Z.Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu,
     Liyue Zhang, Xuan Lu, Qiushi Du, Wenjun Gao, Haowei Zhang, Qihao Zhu, Dejian Yang,
     Zhibin Gou, Z.F. Wu, Fuli Luo, and Chong Ruan. Deepseek-prover-v1.5: Harnessing proof
     assistant feedback for reinforcement learning and monte-carlo tree search. In The Thirteenth
     International Conference on Learning Representations, 2025.
[12] Michael M Bronstein, Joan Bruna, Taco Cohen, and Petar Veličković. Geometric deep learning:
     Grids, groups, graphs, geodesics, and gauges. arXiv preprint arXiv:2104.13478, 2021.


                                               10
[13] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming
     language. In Automated Deduction – CADE 28: 28th International Conference on Automated
     Deduction, 2021.

[14] Yang Li, Dong Du, Linfeng Song, Chen Li, Weikang Wang, Tao Yang, and Haitao Mi. Hun-
     yuanprover: A scalable data synthesis framework and guided tree search for automated theorem
     proving. arXiv preprint arXiv:2412.20735, 2024.

[15] Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang Wu, Xia Xiao, Yifan Sun, Shen Zheng,
     and Ming Ding. Bfs-prover: Scalable best-first tree search for llm-based automatic theorem
     proving. In Proceedings of the 63rd Annual Meeting of the Association for Computational
     Linguistics (Volume 1: Long Papers), 2025.

[16] Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia LI, Mengzhou
     Xia, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-prover: A frontier model for open-source
     automated theorem proving. In Second Conference on Language Modeling, 2025.

[17] Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan
     Geng, Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing Lu, David Acuna, Kaiyu Yang,
     Hongzhou Lin, Yejin Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-prover-v2: Scaling
     formal theorem proving with scaffolded data synthesis and self-correction. In The Fourteenth
     International Conference on Learning Representations, 2026.

[18] Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood
     Sung, Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jianqiao Lu, Hugues de Saxcé, Bolton Bailey,
     Chendong Song, Chenjun Xiao, Dehao Zhang, Ebony Zhang, Frederick Pu, Han Zhu, Jiawei
     Liu, Jonas Bayer, Julien Michel, Longhui Yu, Léo Dreyfus-Schmidt, Lewis Tunstall, Luigi
     Pagani, Moreira Machado, Pauline Bourigault, Ran Wang, Stanislas Polu, Thibaut Barroyer,
     Wen-Ding Li, Yazhe Niu, Yann Fleureau, Yangyang Hu, Zhouliang Yu, Zihan Wang, Zhilin
     Yang, Zhengying Liu, and Jia Li. Kimina-prover preview: Towards large formal reasoning
     models with reinforcement learning. http://arxiv.org/abs/2504.11354, 2025.

[19] Jinwoo Kim, Olga Zaghen, Ayhan Suleymanzade, Youngmin Ryou, and Seunghoon Hong.
     Revisiting random walks for learning on graphs. In The Thirteenth International Conference on
     Learning Representations, 2025.

[20] Jinwoo Kim, Sékou-Oumar Kaba, Jiyun Park, Seunghoon Hong, and Siamak Ravanbakhsh.
     Inverting data transformations via diffusion sampling. arXiv preprint arXiv:2602.08267, 2026.

[21] Sékou-Oumar Kaba, Arnab Kumar Mondal, Yan Zhang, Yoshua Bengio, and Siamak Ra-
     vanbakhsh. Equivariance with learned canonicalization functions. In Fortieth International
     Conference on Machine Learning, 2023.

[22] Johann Schmidt and Sebastian Stober. Tilt your head: Activating the hidden spatial-invariance
     of classifiers. In Forty-first International Conference on Machine Learning, 2024.

[23] Zakhar Shumaylov, Peter Zaika, James Rowbottom, Ferdia Sherry, Melanie Weber, and Carola-
     Bibiane Schönlieb. Lie algebra canonicalization: Equivariant neural operators under arbitrary
     lie groups. In The Thirteenth International Conference on Learning Representations, 2025.

[24] Utkarsh Singhal, Ryan Feng, Stella X. Yu, and Atul Prakash. Test-time canonicalization by
     foundation models for robust perception. In Forty-second International Conference on Machine
     Learning, 2025.

[25] Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V Le, Christopher Ré,
     and Azalia Mirhoseini. Large language monkeys: Scaling inference compute with repeated
     sampling. arXiv preprint arXiv:2407.21787, 2024.

[26] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. minif2f: a cross-system benchmark
     for formal olympiad-level mathematics. In The Tenth International Conference on Learning
     Representations, 2022.


                                               11
[27] Xinbei Ma, Yeyun Gong, Pengcheng He, Hai Zhao, and Nan Duan. Query rewriting in retrieval-
     augmented large language models. In Proceedings of the 2023 Conference on Empirical
     Methods in Natural Language Processing, 2023.
[28] Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale
     Schuurmans, Claire Cui, Olivier Bousquet, Quoc V Le, and Ed H. Chi. Least-to-most prompting
     enables complex reasoning in large language models. In The Eleventh International Conference
     on Learning Representations, 2023.
[29] Kyle O’Brien, Nathan Hoyen Ng, Isha Puri, Jorge Mendez-Mendez, Hamid Palangi, Yoon Kim,
     Marzyeh Ghassemi, and Thomas Hartvigsen. Improving black-box robustness with in-context
     rewriting. Transactions on Machine Learning Research, 2024.
[30] The mathlib Community. The Lean Mathematical Library. In Proceedings of the 9th ACM
     SIGPLAN International Conference on Certified Programs and Proofs, 2020.
[31] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir Radev,
     and Jeremy Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level
     mathematics, 2023.
[32] Haijian Lu, Wei Wang, and Jing Liu. Formalevolve: Neuro-symbolic evolutionary search for
     diverse and prover-effective autoformalization. arXiv preprint arXiv:2603.19828, 2026.
[33] Meiru Zhang, Philipp Borchert, Milan Gritta, and Gerasimos Lampouras. DRIFT: Decompose,
     retrieve, illustrate, then formalize theorems. In The Fourteenth International Conference on
     Learning Representations, 2026.
[34] Rafael Medeiros Cabral, Tuan Manh Do, Yu Xuejun, Wai Ming Tai, Zijin Feng, and SHEN
     XIN. Proofflow: A dependency graph approach to faithful proof autoformalization. In The
     Fourteenth International Conference on Learning Representations, 2026.
[35] Qi Liu, Xinhao Zheng, Xudong Lu, Qinxiang Cao, and Junchi Yan. Rethinking and improving
     autoformalization: Towards a faithful metric and a dependency retrieval-based approach. In
     The Thirteenth International Conference on Learning Representations, 2025.
[36] Aditya Paliwal, Sarah Loos, Markus Rabe, Kshitij Bansal, and Christian Szegedy. Graph
     representations for higher-order logic and theorem proving. In Proceedings of the AAAI
     Conference on Artificial Intelligence, 2020.
[37] Zhaoyu Li, Binghong Chen, and Xujie Si. Graph contrastive pre-training for effective theorem
     reasoning. In Proceedings of the 38th International Conference on Machine Learning, 2021.
[38] Lasse Blaauwbroek, Miroslav Olšák, Jason Rute, Fidel Ivan Schaposnik Massolo, Jelle Piepen-
     brock, and Vasily Pestun. Graph2tac: online representation learning of formal math concepts.
     In Proceedings of the 41st International Conference on Machine Learning, 2024.
[39] Konstantinos Kogkalidis, Jean-Philippe Bernardy, and Vikas Garg. Algebraic positional encod-
     ings. In Advances in Neural Information Processing Systems, 2024.
[40] Konstantinos Kogkalidis, Orestis Melkonian, and Jean-Philippe Bernardy. Learning structure-
     aware representations of dependent types. In Advances in Neural Information Processing
     Systems, 2024.
[41] Siamak Ravanbakhsh, Jeff Schneider, and Barnabás Póczos. Equivariance through parameter-
     sharing. In Proceedings of the 34th International Conference on Machine Learning, 2017.
[42] Risi Kondor and Shubhendu Trivedi. On the generalization of equivariance and convolution
     in neural networks to the action of compact groups. In Proceedings of the 35th International
     Conference on Machine Learning, 2018.
[43] Shuxiao Chen, Edgar Dobriban, and Jane H Lee. A group-theoretic framework for data
     augmentation. Journal of Machine Learning Research, 2020.
[44] Clare Lyle, Mark van der Wilk, Marta Kwiatkowska, Yarin Gal, and Benjamin Bloem-Reddy.
     On the benefits of invariance in neural networks, 2020.


                                               12
[45] Bruno Gavranović, Paul Lessard, Andrew Joseph Dudzik, Tamara von Glehn, João Guil-
     herme Madeira Araújo, and Petar Veličković. Position: Categorical deep learning is an algebraic
     theory of all architectures. In Forty-first International Conference on Machine Learning, 2024.
[46] Yoshihiro Maruyama. Categorical equivariant deep learning: Category-equivariant neural
     networks and universal approximation theorems. arXiv preprint arXiv:2511.18417, 2025.
[47] Léon Bottou. Conceptual challenges in modern ai, 2024.              URL https://youtu.be/
     MEeqneHqukg?si=p46WJqu9aPWwVPTR.
[48] Zellig Harris. Mathematical structures of language. Interscience tracts in pure and applied
     mathematics, 1968.
[49] Zellig Harris. A theory of language and information: a mathematical approach. Oxford
     University Press, 1991.
[50] Kexin Pei, Weichen Li, Qirui Jin, Shuyang Liu, Scott Geng, Lorenzo Cavallaro, Junfeng Yang,
     and Suman Jana. Exploiting code symmetries for learning program semantics. In Forty-first
     International Conference on Machine Learning, 2024.
[51] Hoyeon Chang, Bálint Mucsányi, and Seong Joon Oh. Dynamics reveals structure: Challenging
     the linear propagation assumption. In ICLR 2026 Workshop on Unifying Concept Representation
     Learning, 2026.
[52] Matt J Kusner, Joshua Loftus, Chris Russell, and Ricardo Silva. Counterfactual fairness.
     Advances in Neural Information Processing Systems, 2017.
[53] Itamar Pres, Belinda Z Li, Laura Ruis, Zifan Carl Guo, Keya Hu, Mehul Damani, Isha Puri,
     Ekdeep Singh Lubana, and Jacob Andreas. Position: It’s time to optimize for self-consistency,
     2026.
[54] Tom Leinster. Basic category theory. Cambridge University Press, 2014.
[55] Glynn Winskel. The formal semantics of programming languages: an introduction. MIT press,
     1993.
[56] Herbert B Enderton. A mathematical introduction to logic. Elsevier, 2001.
[57] Jean-Yves Girard, Paul Taylor, and Yves Lafont. Proofs and types. Cambridge university press
     Cambridge, 1989.
[58] Henry Gordon Rice. Classes of recursively enumerable sets and their decision problems.
     Transactions of the American Mathematical society, 1953.
[59] A. M. Turing. On computable numbers, with an application to the entscheidungsproblem.
     Proceedings of the London Mathematical Society, 1937.
[60] Ronald V Book and Friedrich Otto. String-rewriting systems. Springer-Verlag, 1993.
[61] Franz Baader and Tobias Nipkow. Term rewriting and all that. Cambridge university press,
     1998.
[62] Ross Tate, Michael Stepp, Zachary Tatlock, and Sorin Lerner. Equality saturation: a new ap-
     proach to optimization. In Proceedings of the 36th annual ACM SIGPLAN-SIGACT symposium
     on Principles of programming languages, 2009.
[63] Justin Lubin, Jeremy Ferguson, Kevin Ye, Jacob Yim, and Sarah E Chasins. Equivalence by
     canonicalization for synthesis-backed refactoring. Proceedings of the ACM on Programming
     Languages, 2024.
[64] Marcus Rossel. An Equality Saturation Tactic for Lean. PhD thesis, Master’s thesis, 2024.
[65] OpenAI. Introducing gpt-5.2. https://openai.com/index/introducing-gpt-5-4/, 2026. Accessed:
     2026-04-26.


                                                 13
[66] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu,
     Joseph Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language
     model serving with pagedattention. In Proceedings of the 29th symposium on operating systems
     principles, pages 611–626, 2023.


A     Background on category theory

Our formalization uses a small amount of elementary category theory. We leave a minimal introduc-
tion here, and refer the reader to Leinster [54] for further background.

A.1   Categories

Categories provide a natural abstraction of local, non-invertible transformations, just as groups
provide a natural abstraction of context-independent (i.e. global) and invertible symmetries.
Definition 1 A category C consists of
    • a collection of objects ob(C ),
    • for each A, B ∈ ob(C ), a collection C (A, B) of maps or arrows from A to B,
    • for each pair of arrows f ∈ C (A, B) and g ∈ C (B, C), their composition g ◦ f ∈ C (A, C),
    • for each object A ∈ ob(C ), an element 1A of C (A, A), called the identity on A,
satisfying the following axioms:
    • associativity: (h ◦ g) ◦ f = h ◦ (g ◦ f ) for any f ∈ C (A, B), g ∈ C (B, C) and h ∈ C (C, D),
    • identity laws: for each f ∈ C (A, B), we have f ◦ 1A = f = 1B ◦ f .
Example 2 There is a category Set whose objects are sets, whose maps are ordinary functions, with
function composition as composition and identity functions as identities.
Given Example 2 above, it may be tempting to think of maps as functions, but the definition only
requires that they compose associatively with identities:
Example 17. Any group G is a category BG with a single object • and arrows BG(•, •) = G,
where composition is the group operation and the identity arrow is the group identity. The invertibility
of group elements translates to the statement that every arrow of BG is an isomorphism.

A.2   Functors

To relate categories to one another and, in particular, to let an abstract category act on concrete data,
we use structure-preserving maps between categories, called functors.
Definition 4 A functor F : C → D consists of an object map F : ob(C ) → ob(D), and, for each
pair A, B ∈ ob(C ), an assignment on arrows, F : C (A, B) → D(F (A), F (B)), satisfying:
                                                                              f     g
    • preservation of composition: F (g ◦ f ) = F (g) ◦ F (f ) whenever A − → C in C ,
                                                                          →B−
    • preservation of identities: F (1A ) = 1F (A) for every A ∈ C .
The target D may differ substantially from the source C , but the compositional structure of C is
reflected in its image under F . Of particular importance in our setting are functors into Set, which
model how the abstract transformations in C act on concrete data. We illustrate this with groups:
Example 18. A group action of G on a set X is exactly a functor F : BG → Set sending the unique
object • to X and each group element g ∈ G to a function F (g) : X → X. The functor axioms
unfold to the familiar identities F (gh) = F (g) ◦ F (h) and F (1) = 1X , which are precisely the
defining axioms of a group action.

We will also find useful a simple implementation functor, mapping theorems from rewriting categories
to the corresponding singleton sets:
Example 5. There is an implementation functor I : RT → Set mapping each theorem T ∈ Stmt to
the singleton set {T }, while arrows are mapped to the unique functions between singletons.


                                                   14
A.3   Natural transformations

We now introduce natural transformations, the categorical analogue of invariant and equivariant maps.
Just as an equivariant map is defined between two G-sets (sets equipped with an action of a group G),
a natural transformation is defined between two functors sharing a common source and target.
Definition 19. Let F, G : C → D be two functors. A natural transformation α : F → G is an
object-indexed family of arrows (αA : F (A) → G(A))A∈ob(C ) in D such that, for every arrow
f : A → B in C , the following naturality square commutes:
                                                    F (f )
                                            F (A)            F (B)
                                           αA                    αB

                                            G(A)             G(B)
                                                    G(f )

Equivalently, αB ◦ F (f ) = G(f ) ◦ αA for every arrow f : A → B.
The commutativity of this square, called naturality, says that the family α is compatible with the
transformations encoded by C : transporting along C and then applying α yields the same result as
applying α and then transporting along the corresponding arrow of D. This compatibility is exactly
the content of invariance and equivariance in our setting.
Example 20. Taking C = BG, a natural transformation α : F → H between two group actions
F, H : BG → Set reduces to a single map α• : F (•) → H(•) whose naturality square, instantiated
at each g ∈ G, becomes the familiar equivariance condition α• (g · x) = g · α• (x). When H acts
trivially on the target (i.e. H(g) = 1 ∀g ∈ G), this reduces further to α(g · x) = α(x), recovering
invariance.
The example also illustrates the global character of group transformations: because BG has a single
object, a natural transformation collapses to one map α• that applies uniformly. In a category with
many objects, such as the rewriting categories (introduced in Section 3.2), each object A carries its
own component αA , and naturality is what coordinates them across the arrows of C . This is how the
framework captures local, context-dependent transformations central to our setting.

B     Extended formalization of rewriting categories
B.1   Proof equivariance as natural transformations

Let R be a rewriting category. Recall the definition of the proof functor on R from Section 3.3:
Definition 8. The (stochastic) proof functor on R is the functor P : R → Set that maps each object
T ∈ R to P(T ) = D+ (T ∗ ), and whose action on arrows t : T → T ′ is defined as:
                        [P(t)](ν)(t′ ) ∝ ν([t : t′ ])        ∀ν ∈ D+ (T ∗ ), t′ ∈ T ∗

We then formulate an inductive bias for formal theorem provers in terms of the proof functor P,
requiring that their proof distributions can be transported over arrows of R by the action of P:
Definition 9. Let P : R → Set be the proof functor. A prover pθ is R-equivariant in proof
distribution (with respect to P) if
                pθ (· | T ′ ) = P(t)(pθ (· | T ))        for every arrow t : T → T ′ in R.

For Definition 9 to be well-defined, as P(t) is a function D+ (T ∗ ) → D+ (T ∗ ), we need to assume
that pθ (· | T ) ∈ D+ (T ∗ ) for every theorem statement T ∈ R. This is not a radical simplification, as
whole-proof generation LLMs, which rely on logits for next token generation, satisfy this property.
Assumption 7. For any T ∈ Stmt, the prover pθ satisfies pθ (· | T ) ∈ D+ (T ∗ ).
Let I be the implementation functor for R. We can treat pθ as a family ((pθ )T )T ∈R of functions
(pθ )T : {T } → D+ (T ∗ ) mapping ((pθ )T )(T ) = pθ (· | T ). With this perspective, let t : T → T ′ be
an arrow in R. We can rewrite the sides of the equality from Definition 9 as:
               pθ (· | T ′ ) = ((pθ )T ′ )(T ′ ) = ((pθ )T ′ )(I(t)(T )) = ((pθ )T ′ ◦ I(t))(T )


                                                        15
Similarly,
                      P(t)(pθ (· | T )) = P(t)(((pθ )T )(T )) = (P(t) ◦ (pθ )T )(T )
which allows us to rephrase the condition for R-equivariance in proof distribution as:
          ((pθ )T ′ ◦ I(t))(T ) = (P(t) ◦ (pθ )T )(T )      for every arrow t : T → T ′ in R.
Both functions (pθ )T ′ ◦ I(t) and P(t) ◦ (pθ )T are of the type {T } → D+ (T ∗ ), so them being equal
on the argument T translates to the equality of the functions themselves. As a result, we can simplify
the requirement above into:
              ((pθ )T ′ ◦ I(t)) = (P(t) ◦ (pθ )T )      for every arrow t : T → T ′ in R.
But this is precisely the definition of pθ being a natural transformation I → P.
In conclusion, we have shown that both proposed notions of inductive bias for Lean-based formal
theorem provers can be precisely characterized as naturality conditions, and hence as natural transfor-
mations. This formulation extends the perspective of geometric deep learning [12], where structural
inductive biases are captured via invariance and equivariance under group actions, to a categorical
setting. In this broader context, operating over functors R → Set, the appropriate analogue of such
equivariance (and also invariance, as we show in the next section) is given by naturality. A similar
formulation has been proposed by [46], but without being grounded in concrete applications. We find
that categories are a natural fit for modeling semantics-preserving rewritings in formal languages.

B.2   Success invariance as natural transformations

Recall that given a rewriting category R, we define the notion of prover R-invariance as follows:
Definition 10. We say that statements T, T ′ ∈ R are R-equivalent, denoted as T ∼R T ′ , if T ⇆ T ′
in R, i.e. there exist some arrows t : T → T ′ and t′ : T ′ → T .
Definition 11. A prover pθ is R-invariant in success probability if
                            sθ (T ) = sθ (T ′ )   for every T ∼R T ′ .
For the reciprocal R, we can equivalently formalize this definition in terms of natural transformations.
Let us introduce a functor JR : R → Set that maps each object T ∈ R to the interval [0, 1] ⊂ R,
and every arrow to the identity function 1[0,1] . Consider the implementation functor I : R → Set.
For any T ∈ R, we have I(T ) = {T } and J (T ) = [0, 1]. This creates a perfect setting to define the
success probability map sθ as a family of functions (I(T ) → J (T ))T ∈R . Concretely, for a given
prover pθ , consider functions STθ : {T } → [0, 1] given by STθ (T ) = sθ (T ). By the observation above,
each of these functions is of type STθ : I(T ) → J (T ). This gives rise to a family S θ of functions
(STθ : {T } → [0, 1])T ∈ob(R) . For reciprocal R, naturality of S θ coincides with R-invariance of pθ :
Claim 21. When R is reciprocal, S θ is a natural transformation I → J if and only if the prover pθ
satisfies Definition 11.

Proof. Recall that in a reciprocal category R, T ∼R T ′ if and only if there is some arrow T → T ′ .
Let t : T → T ′ be an arrow in R. The naturality condition from Definition 19 requires:
                                        STθ ′ ◦ I(t) = J (t) ◦ STθ
Both these functions are from I(T ) = {T } to J (T ′ ) = [0, 1], so the functions above are equal if
and only if they act equally on T . Finally, unfolding their definitions, we get:
                              STθ ′ ◦ I(t) (T ) = STθ ′ (T ′ ) = sθ (T ′ )
                                           

                              J (t) ◦ STθ (T ) = J (t)(sθ (T )) = sθ (T )
                                           

Combining the observations listed above, we can derive the following equivalence chain:
  pθ is R-invariant ⇐⇒ sθ (T ) = sθ (T ′ ) for all T ∼R T ′
                      ⇐⇒ sθ (T ) = sθ (T ′ ) whenever there is an edge t : T → T ′
                      ⇐⇒ STθ ′ ◦ I(t) (T ) = J (t) ◦ STθ (T ) whenever t : T → T ′ is in R
                                                        

                      ⇐⇒ STθ ′ ◦ I(t) = J (t) ◦ STθ      whenever t : T → T ′ is an arrow in R
                      ⇐⇒ S θ is a natural transformation I → J



                                                   16
Remark 22. More generally, even when R is not reciprocal, S θ defines a natural transformation
I → J provided sθ (T ) = sθ (T ′ ) for any statements T, T ′ connected by an arrow in R. Although
this condition does not imply equivalence, an appropriate choice of generating tactics for R can still
induce useful structure in an R-invariant prover. For instance, if the generating set includes tactics
invoking external solvers (e.g., omega), R-invariance may correspond to the model’s ability to reduce
statements to forms automatically closed by such tactics.

B.3   Structural biases of next-tactic prediction models

In this work, we study whole-proof LLM-based provers, which take a Lean theorem statement as
input and autoregressively generate a complete proof in a single pass. This approach benefits from
efficient inference in modern LLMs, but requires committing to an entire reasoning trajectory without
intermediate feedback from the Lean compiler.
An alternative approach formulates theorem proving as search over Lean states, with tactics as
actions. Next-tactic predictors [10, 14, 15] condition on the current proof state and predict the next
tactic, hence defininig a conditional distribution mθ (· | L(T )). They are typically integrated into
best-first [14, 15] or Monte Carlo tree search [11] frameworks, transforming mθ into a multi-step
prover Mθ (· | T ). From the perspective of inductive biases, of particular interest are sequential
multi-step provers, corresponding to the special case of beam size 1. We will call a multi-step prover
Mθ sequential, if it repeatedly samples a tactic, applies it to the current state, and continues from the
resulting state. The probability of generating a proof t = (t1 , . . . , tn ) ∈ T ∗ is then
                                                n
                                                Y
                                Mθ (t | T ) =         mθ (ti | t<i (L(T )))
                                                i=1

By operating on states, these frameworks can implicitly capture the proposed inductive biases:
                                  t
RT proof equivariance. Let T →  − T ′ be an arrow in RT . This corresponds to the relation between
induced states: L(T ) = t(L(T )). Let P : RT → Set be the proof functor. Suppose Mθ is a
                     ′

sequential multi-step prover. Recall that we would call Mθ RT -equivariant in proof distribution if:
               Mθ (· | T ′ ) = P(t)(Mθ (· | T ))           for every arrow t : T → T ′ in R.
Now, let us unwrap the substance of the right-hand side of the equation above. P(t) is a function that
takes a distribution over proofs T ∗ and returns the induced marginal distribution of proofs that start
with t. Therefore, for any t′ ∈ T ∗ , we have:
                                                          Q|[t:t′ ]|         ′         ′
                              ′     Mθ ([t : t′ ] | T )    t′i ∈[t:t′ ] mθ (ti | [t : t ]<i (L(T )))
          P(t)(Mθ (· | T ))(t ) =                       =      Q|t|
                                       Mθ (t | T )                      mθ (ti | t<i (L(T )))
                                                                           ti ∈t
                                                                |t′ |
                                                                Y
                                                           =             mθ (t′i | t′ <i (t(L(T ))))
                                                               t′i ∈t′
                                                                  ′
                                                                |t |
                                                                Y
                                                           =             mθ (t′i | t′ <i (L(T ′ )))
                                                               t′i ∈t′

                                                           = Mθ (t′ | T ′ )
Hence, Mθ is R-equivariant in proof distribution. In general, however, when combined with explicit
search, this symmetry is lost due to the finite sampling budgets – a state reached once during the
search may never be explored, leading to a non-transferable distribution of proofs.
Rι -invariance of success probability. The inductive biases of multi-step provers become even
clearer when considering success invariance (Section 3.4). Let Rι denote the rewriting category
                                                                                                 ι
generated solely by the empty tactic sequence ι ∈ T ∗ . Every arrow in Rι is then of the form T →
                                                                                                − T′
and satisfies L(T ) = ι(L(T )) = L(T ). Hence, whenever T ⇆ T in Rι , both statements compile to
                  ′                                                ′

the same initial proof state. As a result, Mθ performs search from an identical starting point on both
inputs, implying equal success probabilities. Therefore, Mθ is Rι -invariant in success probability.
Notably, this argument does not require Mθ to be sequential.


                                                      17
Remark 23. Next-tactic prediction introduces a more complex training objective, making optimiza-
tion challenging and leading to weaker empirical performance. A promising direction for future work
is to combine these paradigms by integrating state-conditioned reasoning into single-pass approaches.

B.4   Capturing compositional behavior in Lean proofs

In this work, we consider rewriting categories R in which each tactic sequence induces a distinct
arrow. Concretely, for arrows t, t′ : T → T ′ in R, if the underlying tactic sequences t and t′
are syntactically distinct, then the corresponding arrows are treated as distinct. Nevertheless, the
formalization of the Lean statement–tactic space introduced in Section 3 can capture richer structural
properties of this space, requiring provers to reason about the underlying structure of tactics rather
than their syntactic form alone.
Consider the tactics t1 , t2 , and t3 shown in Figure 5. Tactics t1   Tactic t1
and t2 rewrite the current proof state using the Mathlib lemmas       rw [Nat.sub_add_eq]
Nat.sub_add_eq and Nat.sub_add_cancel, respectively, while
                                                                      Tactic t2
t3 applies both these rewriting rules, within a single tactic.
                                                                      rw [Nat.sub_add_cancel]
Hence, the sequential composition [t1 : t2 ] has the same ef-
                                                                  Tactic [t1 : t2 ]
fect as applying t3 directly. Although both induce the same
                                                                  rw [Nat.sub_add_eq]
transformation function d : Ω → Ω on Lean states, the con-        rw [Nat.sub_add_cancel]
catenation [t1 : t2 ] and t3 remain syntactically distinct, as
                                                                  Tactic t3
shown in Figure 5. A categorical formulation allows these
                                                                  rw [Nat.sub_add_eq, Nat.sub_add_cancel]
transformations to be identified in R by requiring that, for
any objects T, T ∈ R, the morphisms [t1 : t2 ] : T → T
                 ′                                           ′
                                                               Figure 5: Composition [t1 : t2 ] has
and t3 : T → T ′ coincide, without imposing any equiva-
                                                               the same effect as t3 , despite them
lence between t3 and either t1 or t2 individually. This notion
                                                               being syntactically different.
of compositional equivalence cannot be naturally expressed
using graph- or group-based representations.
The example in Figure 5 concerns tactic sequences that are
globally equivalent as functions Ω → Ω. Category-theoretic
                                                                    Tactic l1
structure also enables a finer notion of local equivalence. Con-
                                                                    have h0 : x * 3 ≡ 1 [ZMOD 7] := by
sider the tactics l1 and l2 from Figure 6. Both introduce the         norm_num
auxiliary statement that 3x ≡ 1 (mod 7), but construct the
                                                                    Tactic l2
proof differently. Consequently, they are not extensionally
                                                                    have h0 : x * 3 ≡ 1 [ZMOD 7] := by
equivalent: for example, l2 requires the presence of a hypoth-        simpa [hx]
esis hx in the proof state. Nevertheless, categorical structure
allows these transformations to be identified whenever both Figure 6: Tactics l1 and l2 may act
act successfully on a given state, capturing an informal notion differently on some statements.
of “having proved an auxiliary result inside the main proof, no
matter how, the model should continue in the same way”.
These examples further motivate the use of category theory as a formal framework for the space
of Lean statements and tactics. In contrast to graph- or group-based representations, categorical
structure naturally captures compositional and contextual equivalences between tactics, including
both globally equivalent transformations and locally equivalent behaviors conditioned on proof states.
This additional expressive power enables modeling structural relationships between tactics that extend
beyond purely syntactic or functional representations.

B.5   Rewriting categories of formal languages

In this subsection, we leave a brief remark on how rewriting categories could be used to model
symmetries of formal languages, beyond the mathematical domain that we focus on in this work.
We consider formal languages equipped with a syntax and a semantics, where the syntax specifies
which expressions are valid, and the semantics assigns meaning to expressions. Programming and
logical languages are the canonical examples [55–57]. A central concern therein is checking whether
two given expressions are semantically equivalent. In programming languages, this could be if two
programs map every input to the same output, or if they execute in the same way. In logic, this could
be if each formula is derivable from the other. Unfortunately, these are largely undecidable [58, 59].


                                                     18
A workaround is using a tractable notion of equivalence based on a set of rewriting rules that takes an
expression and syntactically transforms it without altering its semantics of interest. If two expressions
can be made identical through rewriting, we call them syntactically equivalent, which implies they
are semantically equivalent (as in Section 3.4, the converse does not necessarily hold). This approach
is usually implemented with rewriting systems that reduce expressions to normal forms that cannot
be further rewritten, and compare those to check equivalence [60, 61]. This idea is used in compiler
optimization [62], program refactoring [63], and (classical) automated theorem proving [64].
Rewriting categories (Section 3.2) can be used to describe rewriting systems. An (abstract) rewriting
system consists of a set A, elements called objects or signatures, together with a binary relation on A,
denoted by →, called the rewrite relation [60]. Then we can construct a rewriting category R by
    • taking as its objects the set A,
                                                            ∗
    • taking as its arrows the reflexive transitive closure → of →, i.e. the transitive closure of
      → ∪ {id}, where id is the identity relation.
In other words, we can lift a rewriting system to a rewriting category by composing its rewriting
relations and identity. Thus, the relationship between them is analogous to that between a group and
its generating set. An R-invariant map, defined in naturality sense (as in Appendix B.2), preserves
syntactic equivalence by construction, and hence preserves semantic equivalence.
From a rewriting system, one can take a subset of its relations to obtain a restriction. For example, if
the relations of a system (A, →) is an indexed union → = →1 ∪ →2 of two rewriting rules, one can
take (A, →1 ) as a restriction. It would yield sound rewrites, but more incomplete as some semantically
equivalent expressions would no longer be syntactically equivalent. For the respective categories R
and R1 , this translates to a subcategory relation R1 ⊆ R, and so a hierarchy of invariances as in
Section 3.4. We exemplify with lambda calculus, a foundational example in programming and logic.
Example 24. The untyped lambda calculus consists of lambda expressions defined by the syntax
e ::= x | (λx.e) | (e e) where x ranges over a namespace. Its rewriting system can be identified as
(Λ, →), where Λ is the set of all lambda expressions, and the relations →=→α ∪ →β ∪ →η consist of
    • α-conversion (variable renaming) that rewrites λx.M to λy.M [x := y] if y is not free in M ,
    • β-reduction (function application) that reduces an expression of the form (λx.t)s to t[x := s].
    • η-conversion (extensionality) that converts between λx.f x and f if x does not appear free in f .
Hence, there is a restricted rewriting system (Λ, →α ) that only performs variable renaming. Between
                                     ∗                  ∗
the rewriting categories R = (Λ, →) and Rα = (Λ, →α ), this translates to Rα ⊆ R.

In the context of deep learning, Example 24 illustrates how approaches that aim to analyze or improve
the robustness of neural networks on formal languages primarily focusing on variable renaming
[4, 50] yield weaker invariances than more general rewritings, such as in our work.

C     Extended methodology
This section provides additional details on the experimental methodology. We first describe the
construction of the miniF2F-rw dataset, which augments miniF2F [26] with equivalent problem
reformulations (Appendix C.2). We then detail the sampling mechanism µ(· | T, K) used in the
test-time ensemble setting (Section C.3) and report ablations over its design choices (Section C.3)
and the number of ensemble variants in miniF2F-rw evaluations (Appendix C.4). The codebase,
containing implementations of rewriting ensembles and the miniF2F-rw dataset can be found at:
https://github.com/kolejnyy/rw-ensembles.

C.1   Practical challenges of statement reformulation in Lean

Before detailing our methodology, we emphasize that statement rewriting in Lean is substantially
more challenging than in natural language settings. In NLP, query rewriting is a standard technique
for improving the robustness and reasoning capabilities of LLMs [27–29]. Such approaches rely
on the assumption that semantically equivalent queries admit interchangeable solutions: answers to
rewritten queries can typically be reused directly or mapped back to the original formulation with
minimal effort. For example, the question “What is the capital of Germany?” may be rewritten as
“Which city in Germany is the capital?”, while preserving both meaning and answerability. Moreover,


                                                   19
modern LLMs exhibit strong understanding of natural language, making the generation of such
rewrites fairly simple.
In Lean theorem proving, these assumptions no longer apply.
Proof correctness is determined by a syntactically strict formal       Statement T         1

system, where even minor modifications to a statement may              theorem T1 (n : N) (h : n + 1 = 3) : 3 = n + 1 := by

invalidate an existing proof. As a result, semantically equiva- Proof of statement T             1
lent statements do not necessarily admit interchangeable proofs, theorem T1 (n : N) (h : n + 1 = 3) : 3 = n + 1 := by
                                                                          exact h.symm
and transferring proofs between related formulations can require
non-trivial transformations. Consider the statements T1 and            Statement T         2

T2 in Figure 7. Although n + 1 and 1 + n are mathematically            theorem T2 (n : N) (h : 1 + n = 3) : 3 = n + 1 := by

equivalent, they are syntactically distinct terms, and Lean does       Incorrect proof of statement T   2
not identify them automatically. Consequently, the proof term          theorem T2 (n : N) (h : 1 + n = 3) : 3 = n + 1 := by
h.symm, which proves T1 , is rejected as a proof of T2 . This illus-      exact h.symm

trates that meaningfully transforming a problem while remaining
capable of recovering a proof of the original is non-trivial.        Figure 7: Lean proofs do not trans-
                                                                     fer between equivalent statements.
A sound augmentation mechanism can be implemented in two
distinct ways:
    • Out-of-Lean. Analogously to augmentation methods in natural language tasks, an LLM may
      generate rewrites of the original statement directly. However, this approach additionally requires
      constructing a Lean certificate that transfers proofs of the augmented statement back to the
      original problem. In general, such certificates are non-trivial to obtain and may themselves
      require LLM inference, which needs to be accounted for under fixed computation budgets.
    • Within-Lean. Alternatively, augmentations can be generated directly within Lean by exploring
      the space of proof states via tactics. This avoids using LLM calls outside the core proving
      process, but introduces two challenges: selecting meaningful rewrite rules without exces-
      sively complicating the proof state, and defining a mapping from proof states back to theorem
      statements, since LLM provers operate on statements, whereas Lean applies tactics on states.
In our test-time sampling framework (Appendix C.3), we adopt the latter approach. We sample
transformations from the large collection of unconditional premises available in Mathlib, comprising
over 30,000 lemmas. This yields non-trivial statement rewritings, as illustrated in Figure 4, while
retaining a principled mechanism for proof transfer through tactic composition.

C.2    Generation of the miniF2F-rw dataset

To systematically demonstrate semantic inconsistency among LLM-based Lean provers, we construct
miniF2F-rw, a dataset of 5726 theorems (2922 validation, 2804 test) obtained as semantics-preserving
reformulations of problems from the miniF2F benchmark. Each variant is paired with Lean certificates
of variant ⇔ seed, ensuring that any proof of the augmented statement can be translated into a proof
of the original, and vice versa. We further apply manual checks to remove variants that introduce
spurious complexity or trivialize the task. An overview of the pipeline is shown in Figure 8.
Initial variant generation. First, we generate candidate augmentations by prompting GPT-5.4 to
produce 5-15 rewrites of each miniF2F statement. For each seed theorem, we then sample 20% of its
variants and apply a second transformation, again using GPT-5.4, to rename variables and hypothesis
names. The exact prompts used in this process are listed in Appendix F. At the end of this stage, we
obtain over 7500 statements for subsequent verification.
Certifying equivalence. To ensure semantic equivalence between augmented statements and their
seeds, we employ a two-stage validation procedure. First, we manually check each variant and discard
those that alter the content in an unreasonably complicated (e.g., replacing 1 with 0.factorial) or
simplistic (e.g., simplifying algebraic expressions) way.
Second, we generate Lean certificates establishing variant ⇔ seed. Each such implication is
decomposed into a series of simpler subproblems. Writing a seed theorem T and its variant T ′ as:
          T := (C1 ∧ . . . ∧ Ck ) =⇒ G          and    T ′ := (C1′ ∧ . . . ∧ Cl′ ) =⇒ G′
for the direction variant ⇒ seed, it suffices to show:
                       (C1 ∧ . . . ∧ Ck ) =⇒ Ci′         for all i ∈ 1, . . . , l
                                                G′ =⇒ G

                                                           20
                     Figure 8: Process of generation of the miniF2F-rw dataset.


Given these components, a proof of T can be obtained by reconstructing the premises of T ′ , invoking
T ′ (simulated via sorry), and finally reducing G′ to G (see Figure 9 for a code example). The inverse
implication can be derived analogously, by flipping T and T ′ . This methodology resembles that
of BEq [35], which calls a prover to produce “a proof of T using T ′ ”. However, BEq only checks
whether the name of T ′ was mentioned in the proof, without assessing whether it was meaningfully
used, while our decomposition enforces semantic correctness.
To close each of these subgoals, we initially apply a set of fixed simplification tactics (see the proof
of goal_to_goal in Figure 9). If this fails, we invoke DeepSeek-Prover-V2 [1] with up to 8 attempts
per subproblem. Since the decomposed goals are significantly simpler than the original statements,
this budget suffices in most cases. Finally, we manually check the failure instances and repair them
when a small number of augmentations of a specific problem are successfully verified.

C.3   Description of the test-time sampling mechanism

Beyond the controlled miniF2F-rw setting, where augmentations are precomputed and verified, we
consider a test-time ensemble framework, generating reformulations online. The procedure consists
of three stages: rewriting, composition, and reranking, described below and illustrated in Figure 10.
Rewriting tactics sampling. In the first stage, we use Lean to sample rewrite sequences applicable
to each expression in the input statement. For a given expression, we construct sequences of
(L1 , . . . , Ld ) lemmas drawn from Mathlib [30]. To guarantee semantic equivalence, we restrict
attention to the subset M0 of unconditioned lemmas of the form P = Q or P ⇔ Q, whose application
is inherently reversible. Despite this constraint, the resulting transformation space strictly generalizes
prior augmentation schemes [3, 36–38], which rely on abstract syntax tree (AST) symmetries to
ensure soundness. In contrast, M0 induces a richer rewriting category RM0 that supports non-trivial
transformations (see Figure 4), while preserving correctness through Lean tactic semantics. This
provides a tractable, more complete approximation to the full tactic rewriting category RT .
To sample the sequences of rewriting rules, we use a methodology similar to the rw? tactic, yet with
increased exploration breadth and depth. At each step, candidate lemmas from M0 are matched
against the expression’s AST, ranked using the rw?’s utility heuristic, and validated via application.
We pick the top-b valid rewrites and recursively expand them up to depth d. This yields up to bd
candidate sequences and corresponding rewritten expressions.
To control complexity, we apply AST-based filtering, discarding rewrites whose tree depth or node
count exceeds that of the original expression. We then deduplicate syntactically equal outputs arising
from different rewrite paths. After validation, we found that b = 15 and d = 2 provide a favorable
performance-to-efficiency trade-off, usually producing 5–50 distinct variants per expression.
As the search space over M0 remains large, limiting to top-b candidates may omit semantically
meaningful rewrites. To mitigate this, we explicitly augment the pool with selected commu-
tativity rules (ge_iff_le, ←ge_iff_le, ←gt_iff_lt, gt_iff_lt, eq_comm, add_comm, mul_comm,


                                                   21
theorem mathd_algebra_405_v2 (S : Finset N)
  ( h : ∀ x , x \ in S ↔ 0 < x \ and (x + 2) ^ 2 < 20) :
  2 = S. card := by
  sorry

theorem cond_1 (S : Finset N)
  ( h : ∀ x , x \ in S ↔ 0 < x \ and x ^ 2 + 4 * x + 4 < 20)
  : ∀ x , x \ in S ↔ 0 < x \ and (x + 2) ^ 2 < 20 := by
  intro x
  simp_all only [ Finset . mem_filter , Finset . mem_range , Finset . mem_univ ,
     true_and_iff , and_true_iff , Nat . cast_ofNat , Nat . cast_one ,
     Nat . cast_add , Nat . cast_mul , Nat . cast_sub , Nat . cast_pow ]
  constructor <;> intro h <;>
  ( try constructor ) <;>
  ( try simp_all [ sq ]) <;>
  ( try ring_nf at * <;> omega ) <;>
  ( try nlinarith ) <;>
  ( try linarith )

theorem goal_to_goal (S : Finset N) ( aug_goal : 2 = S. card ) : S. card = 2
  := by
  try decide
  try native_decide
  try trivial
  try linarith
  try nlinarith
  try omega
  try norm_num
  try field_simp
  try simp
  try ring_nf
  try ring
  try exact ?

theorem mathd_algebra_405 (S : Finset N)
  ( h : ∀ x , x \ in S ↔ 0 < x \ and x ^ 2 + 4 * x + 4 < 20) :
  S . card = 2 := by
  have aug_0 : ∀ x , x \ in S ↔ 0 < x \ and (x + 2) ^ 2 < 20 := cond_1 S h
  have aug_goal : 2 = S. card := mathd_algebra_405_v2 S aug_0
  exact goal_to_goal S aug_goal

Figure 9: An example of a Lean certificate, proving mathd_algebra_405_v2 ⇒ mathd_algebra_405.




              Figure 10: Sampling process for the test-time ensemble mechanism.

                                             22
and_comm, or_comm) and standard normalization tactics (ring_nf, simp, norm_num, field_simp). The re-
sulting outputs are incorporated into the final set of candidate rewrites.
Composition of augmented statements. Given the set of rewritten versions for each expression
(premises and goal), we construct augmented theorem statements suitable for downstream provers.
This involves two design choices: (i) how to select rewrites for each statement, and (ii) how to map
rewritten expressions back to a coherent theorem.
For rewrite selection, a simple baseline modifies a single expression per variant, keeping all others
unchanged. While straightforward, this approach becomes restrictive for statements with many
components, as all but one remain unchanged in each augmentation. To increase diversity, we
instead sample a rewrite for each expression independently from its candidate set. Concretely, for
an expression E with ranked rewrites (E1 , . . . , En ), we form (E0 = E, E1 , . . . , En ) and sample Ei
                                  1
with probability proportional to i+1 . Applying this procedure across all expressions yields a sampled
state. Repeating it 20 times and removing duplicates produces a diverse set of augmented states.
We then convert each state into a theorem statement. This step is non-trivial, as Lean’s internal
representation may differ from its surface syntax (e.g., implicit type annotations or notation changes
such as Real.pi vs. π). While syntactic correctness is not strictly required (generated proofs are
ultimately checked against the original statement after tactics-based transfer), poorly formed outputs
can degrade prover performance. We therefore consider two strategies. A naive approach directly
linearizes the state into a statement-like format. A more advanced state-to-statement function is
realised by prompting an LLM to convert provided Lean states to theorems. Empirically, the latter
yields higher-quality outputs and resolves common inconsistencies, as confirmed by ablations. In
our experiments, we use GPT-5.4 [65] for this conversion (prompt available in Appendix F.3). This
choice is primarily for convenience: the mapping is highly systematic, and a small LLM trained on
(state, statement) pairs should suffice. We leave this simplification for future work.
Energy function reranking. Given a set S of retrieved statements, we select a subset of 7 variants
to pass to the prover. Inspired by orbit canonicalization methods [21, 24, 63], we rank candidates
using an energy function that approximates the success probability sθ of prover pθ . As estimating sθ
directly would require full proof attempts, we introduce a lightweight proxy, called theorem surprise.
The underlying intuition is that LLM-based provers perform better on in-distribution inputs. We
therefore prioritize statements that appear more “natural” to the model, as measured by their token-
level likelihood under pθ . Concretely, for a statement T , to generate a proof for T , pθ is prompted
with input [P : T ], where P is the initial set of instructions ("You are an expert in Lean4..."). Letting
T1 , . . . , Tl be the tokens representing T , we define the theorem surprise of T as:
                                                  l
                                              1X
                             ThSur(T ) = −          log pθ (Ti | [P : T<i ])
                                              l i=1

where pθ (Ti | [P : T<i ]) is the probability of pθ generating token Ti after seeing P and the first i − 1
tokens of T . Higher values indicate less familiar inputs. We rank candidates by ThSur and select
the seven lowest-scoring statements, which, together with the original problem, are passed to pθ for
proof generation.

      Table 3: Success rate per ensemble style on miniF2F-valid (with DeepSeek-Prover-V2)

     Budget                                                      8         16        32        64
     DSP-V2 (baseline)                                         78.4       78.8      79.1      79.5
     DSP-V2 (ThSur + simp)                                     78.7      79.2      79.7       80.1
     DSP-V2 (ThSur + simp + excomm + comb20)                   78.9      79.6      80.1       80.6
     DSP-V2 (ThSur + simp + excomm + comb20 + LLM)             79.7      80.5      81.1       81.5

Ablation on the sampling protocol. We iteratively refine the sampling procedure via ablations on
miniF2F-valid (Table 3). All variants use theorem surprise for reranking and include rewrites obtained
from standard simplification tactics. Augmenting the rewrite pool with explicit commutativity rules
and switching to the combination-based state construction (sampling 20 variants) yields consistent
improvements. Finally, replacing the naive state-to-statement conversion with GPT-5.4 further boosts
performance, highlighting the importance of well-formed input representations for prover success.


                                                      23
Figure 11: PASS@k success rates on miniF2F-rw for ensemble sizes 2, 4, and 8 (solid lines), with
single seed and random-sample baselines as narrower dashed lines. Ensemble and random curves
include ± one estimated standard error.


C.4   Ablation on the number of sampled rewrites

Proposition 15 predicts that ensemble performance should increase with the number of sampled
augmentations. We empirically validate this by evaluating ensemble sizes of 2, 4, and 8 on miniF2F-
rw. Figure 11 reports validation and test success rates as a function of the sample budget for each
non-reasoning prover in our main setup. Across all models, PASS@k improves monotonically with
the ensemble size, consistent with the theoretical prediction. Notably, for Goedel-Prover-DPO and
DeepSeek-Prover-V2, using 4 variants already surpasses the seed baseline despite the performance
gap between seed and random augmentations, with further gains observed at 8 samples. Based on
these results, we use 8 variants in all miniF2F-rw experiments.

C.5   Adaptation of PASS@k to ensembles

In its standard formulation, given C successes over N attempts, PASS@k is measured as:
                                                       N −C
                                                            
                                                            k
                                      PASS@k = 1 −          N
                                                              
                                                            k

representing the probability of seeing at least one success across randomly chosen k. For an ensemble,
running on K variants with success-total attempt pairs (N1 , C1 ), . . . , (NK , CK ), we report:
                                                              Ni −Ci
                                                         K
                                                                     
                                                               k/K
                                                         Y
                                   PASSens @k = 1 −             Ni
                                                                    
                                                      i=1     k/K


C.6   Testing environment specification and hyperparameters.

Hardware specifications. We perform proof generation on a machines equipped with Intel Platinum
8628 CPUs and NVIDIA H100 GPUs (80GB VRAM). Each model is allocated 8 CPU cores, 64GB
RAM, and a single H100 GPU. Under this setup, non-reasoning models generate one proof attempt
every 0.5-1.3s on average, while models with explicit informal reasoning require 7-10s per attempt.
Proof verification is conducted on machines with Intel Platinum 8628 or Intel Xeon Gold 6326 CPUs.
This stage is highly parallelizable; we dispatch separate jobs per problem, each using 8 CPU cores
and 64GB RAM. Verification latency is approximately 1s per attempt. Overall, for the miniF2F-rw
benchmark (5,700 problems, 64 attempts each), a single non-reasoning prover requires approximately
4–5 GPU-days for generation and an additional ~4 CPU-days for Lean-based verification.


                                                 24
    Table 4: PASS@k results of selected reasoning LLM provers on the miniF2F-rw benchmark.
                                                         minif2f-aug-valid                          minif2f-aug-test

    Model                      Variant      k=1      k=8         k = 16      k = 32     k=1     k=8         k = 16     k = 32

                               seed         68.8     81.1        82.5        83.2       58.9     74.6     76.4     77.5
                               random       65.2±0.7 79.5±0.6    81.2±0.6    82.2±0.6   56.0±0.7 72.9±0.7 75.3±0.8 76.7±0.8
    Goedel-Prover-V2-8B
                               controlled   –        80.6±0.1    81.9±0.1    82.8±0.1   –        75.0±0.1 77.0±0.1 78.3±0.1
                               test-time    –        80.4        81.9        82.8       –        74.4     76.7     78.6

                               seed         67.4     78.1        79.7        80.7     58.0     71.0         73.2       75.0
                               random       62.7±0.8 75.9±0.7    77.7±0.8    79.3±1.0 53.4±0.8 68.5±0.7     70.8±0.7   73.0±0.9
    DeepSeek-Prover-V2-7B
                               controlled   –        77.7±0.1    79.5±0.2    81.0±0.2 –        70.3±0.1     72.3±0.1   74.2±0.1
                               test-time    –        77.5        79.3        81.0     –        70.9         72.9       74.2

                               seed         61.9     73.4     75.4     76.6     55.0     68.2               70.0       71.3
                               random       57.6±0.9 70.9±0.9 73.6±0.9 75.8±1.1 52.2±0.8 66.5±0.8           68.9±0.8   70.7±0.9
    Kimina-Prover-Distill-8B
                               controlled   –        74.2±0.2 76.5±0.2 78.3±0.2 –        68.8±0.1           71.0±0.1   72.5±0.1
                               test-time    –        72.0     74.5     76.3     –        70.1               72.6       74.4




Model hyperparameters. All LLM provers used in our experiments are prompted with the original
prompts from their repositories. We use vLLM [66] for more efficient generation, and sampling
temperature of 0.7 for all models. The maximum number of output tokens is set to 2000 for non-
reasoning, and 8192 for reasoning provers. For calls to GPT-5.4 [65], we fix the temperature at 0.2.
API costs. We use GPT-5.4 to augment problem statements during construction of the miniF2F-rw
dataset. The cost per statement ranges from $0.01 to $0.05, totaling approximately $14.50 for 488
benchmark problems. At test time, GPT-5.4 is additionally employed to convert states into statements
for ensembling. This incurs a total cost of $18.19 across all datasets (miniF2F, ProofNet, and Ineq-
Comp), corresponding to approximately $0.009 per problem. As discussed in Appendix C.3, this
transformation can be implemented using a local model, mitigating cost in practical deployments.

D      Additional experiments with reasoning models
D.1      Robustness of reasoning provers on miniF2F-rw

We evaluate three state-of-the-art open-source reasoning LLM provers: Goedel-Prover-V2-8B [17],
Kimina-Prover-Distill-8B [18] and DeepSeek-Prover-V2-7B [1] (in CoT mode). We run each prover
for n = 32 attempts on all variants from miniF2F-rw and report PASS@k for k ∈ {1, 8, 16, 32}.
The results are presented in Table 4. Although the degradation is less severe than for non-reasoning
provers (Table 1), suggesting that an explicit reasoning phase improves robustness to formal rewrites,
all models still consistently prefer the seed statements over their augmented variants. For example, on
the miniF2F-rw-test split, Goedel-Prover-V2-8B drops from 58.9 to 56.0 PASS@1 and from 77.5 to
76.7 PASS@8. The effect is more pronounced for DeepSeek-Prover-V2-7B, whose PASS@1 declines
from 67.4 to 62.7 on the validation split, and from 58.0 to 53.4 on the test set. This indicates that
current reasoning-oriented provers remain sensitive to syntactic formulation and do not exhibit full
invariance under semantics-preserving transformations. Consequently, these results further motivate
the structural bias criteria proposed in this work, even for reasoning models.
Consistent with the observations in Section 6, ensembling across semantically equivalent variants
reduces performance variance and consistently improves over selecting a single random sample.
This trend holds across all evaluated models, datasets, and sampling budgets. Importantly, both the
controlled and test-time sampling protocols remain at least competitive with the seed baselines in
every configuration. For Kimina-Prover-Distill-8B, they substantially outperform the default model,
increasing PASS@32 on the test split from 71.3% to 74.4%. Overall, these results suggest that,
even for reasoning-based formal provers, allocating the inference budget across multiple equivalent
representations of the input theorem can yield significant performance gains.

D.2      Comparisons at matched token counts on miniF2F

Table 5 contains average token counts per problem on miniF2F. Since reasoning mode uses 9-10×
more tokens on average per problem, in Tables 1 and 4, a comparison at roughly matched token
counts within DeepSeek-Prover-V2 results would be comparing reasoning with budget k against
ensemble with budget 8k. In these comparisons, ensemble is competitive with and often surpasses


                                                                    25
      Table 5: Average token usage per inference mode per attempt for DeepSeek-Prover-V2-7B.

                       Model                                   miniF2F-valid           miniF2F-test
                       DeepSeek-Prover-V2-7B                              346                  395
                       DeepSeek-Prover-V2-7B (CoT)                       3138                 3763


reasoning, showing its utility as an inference-time scaling method in this setting. While this matches
token counts, we remark that in terms of the computational cost of forward passes, reasoning would
be more inefficient, because in modern LLMs, generating a single long chain is worse than a set of
shorter generations due to lack of parallelizability and the quadratic cost of self-attention.

E     Proofs
E.1    Functoriality of the proof functor

Let R be a rewriting category. Recall the definition of the (stochastic) proof functor map on R:
Definition 8. Let D+ (T ∗ ) be the set of all distributions over the set T ∗ of Lean proofs, which assign
non-zero probability to each element t ∈ T ∗ . The (stochastic) proof functor on R is the functor
P : R → Set that maps each object T ∈ Stmt to P(T ) = D+ (T ∗ ), and whose action on arrows
   t
T −→ T ′ of R is defined as:
                          P(t)(ν)(t′ ) ∝ ν([t : t′ ])            ∀ν ∈ D+ (T ∗ ), t′ ∈ T ∗

We claim that the so-defined map is indeed a functor.
Proposition 25. The map from Definition 8 is a well-defined functor P : R → Set.

Proof. First of all, note that D+ (T ∗ ) ∈ Set, so the function of P on objects is well-defined.
Pick any t, t′ ∈ T ∗ and ν ∈ D+ (T ∗ ). The concatenation [t : t′ ] is also an element of T ∗ . Moreover,
by positivity of ν, the sum of ν([t : t′′ ]) over t′′ ∈ T ∗ is greater than 0. Hence, we can define a
distribution ν ′ ∈ D+ (T ∗ ) with probabilities proportional to ν([t : ·]), as follows:
                                                     ν([t : t′ ])
                                   ν ′ (t′ ) = P                  ′′
                                                                             ∀ t′ ∈ T ∗
                                                 t′′ ∈T ∗ ν([t : t ])

being precisely the distribution P(t)(ν)(t′ ) from Definition 8. Therefore, the action of P on arrows
of R is also well-defined. It now suffices to show that P satisfies the functor conditions, i.e. preserves:

    • identities: Let T ∈ Stmt be a statement. The identity arrow 1T in R is associated with
      the application of the empty tactic sequence ι. Unfolding the definition from above, we obtain:
                                        ν([ι : t′ ])
          P(1T )(ν)(t′ ) = P                           ′′ ])
                                                             = ν([ι : t′ ]) = ν(t′ )       ∀ ν ∈ D+ (T ∗ ), t′ ∈ T ∗
                                     ′′
                                    t ∈T   ∗ ν([ι  : t
       meaning that P(1T )(ν) = ν for all ν ∈ D+ (T ∗ ). Consequently, P(1T ) = 1D+ (T ∗ ) = 1P(T ) .
                               t          t′
    • composition: Let T −→ T ′ −−→ T ′′ be arrows in R. We need to show P(t′ ) ◦ P(t) = P(t′ ◦ t).
      Let ν ∈ D+ (T ∗ ) be a distribution and let t′′ ∈ T ∗ be a proof. Then:
         (P(t′ ) ◦ P(t)) (ν)(t′′ ) = (P(t′ )) (P(t)(ν))(t′′ ) ∝ (P(t)(ν))([t′ : t′′ ]) ∝ ν([t : t′ : t′′ ])
       and similarly
                           P(t′ ◦ t)(ν)(t′′ ) ∝ ν([(t′ ◦ t) : t′′ ]) = ν([t : t′ : t′′ ])
       Since both (P(t′ ) ◦ P(t))(ν) and P(t′ ◦ t)(ν) are distributions over T ∗ , by the result above,
       they must be equal. As ν was arbitrary, we can conclude that P(t′ ) ◦ P(t) = P(t′ ◦ t).




                                                            26
E.2   Proof of Proposition 14

To prove R-invariance of the ensemble framework in the limit of samples, we assume the following:
Assumption 13. Let T ∼R T ′ and let T ′′ ∈ R be a statement. Suppose that for some K,
the probability P(T ′′ ∈ µ(· | T, K)) of sampling T ′′ is greater than 0. Then:
                    lim P(T ′′ ∈ µ(· | T, K)) = lim P(T ′′ ∈ µ(· | T ′ , K)) = 1
                   K→∞                                K→∞


As mentioned in Section 4.2, this assumption is true whenever the sampling protocol explores the
space of reachable states thoroughly enough, or when it canonicalizes the input theorem, transforming
it into a specific representative of its equivalence class. In our methodology described in Section 5,
we propose a mixture of these ideas: sampling various statements reachable from the input theorem,
followed by re-ranking using an energy function. This way, we approximate canonicalization by
optimizing an objective function over a sampled subspace of reachable reformulations.
Under Assumption 13, we can prove that the ensemble framework is R-invariant in success probability
in the limit of computational budget and the number of samples:
Proposition 14 Let n : N → N be a function such that ⌊n(x)/x⌋ → ∞ as x → ∞. Then,
                       (K,n(K))                     (K,n(K))
                lim s̄          (T )   =     lim s̄          (T ′ )        for every T ∼R T ′ .
               K→∞ θ,µ                      K→∞ θ,µ

so limiting ensemble prover is R-invariant in success probability.

                                       (K,N )
Proof. Recall that the probability s̄θ,µ(T ) of success of an (N, K)-ensemble on statement T is:
                                                           " K                     #
                  (K,N )
                                                            Y               ⌊N/K⌋
                s̄θ,µ (T ) = 1 − E(T1 ,...,TK ) ∼ µ(·|T,K)     1 − sθ (Ti )          .        (1)
                                                                   i=1


Let T ∼R T ′ be R-equivalent statements. Denote by Pµ (T ′′ | T, K) the probability that T ′′ will be
among the samples drafted by µ(· | T, K). Suppose there exists some T ′′ with sθ (T ′′ ) > 0, such
that for some K, Pµ (T ′′ | T, K) > 0. Then, by the Assumption 13, we have:
                          lim Pµ (T ′′ | T, K) = lim Pµ (T ′′ | T ′ , K) = 1
                         K→∞                          K→∞
                                ⌊N/K⌋
Since each term 1 − sθ (Ti )           in Equation (1) is bounded above by 1, we can write:
                             " K                      #
                              Y                ⌊N/K⌋                                        ⌊N/K⌋
   E(T1 ,...,TK ) ∼ µ(·|T,K)      1 − sθ (Ti )           ≤ Pµ (T ′′ | T, K) · 1 − sθ (T ′′ )
                           i=1
                                                                    + 1 − Pµ (T ′′ | T, K)
                                                                                             

Indeed, if T ′′ appears among the sampled states, which happens with probability Pµ (T ′′ | T, K),
                                     ⌊N/K⌋
the product is at most 1 − sθ (T ′′ )       . Otherwise, with the probability of 1 − Pµ (T ′′ | T, K),
we can crudely bound it by 1.
With this observation, we can derive a lower bound for the limit from the problem statement:
                                                         " K                         #!
       (K,n(K))
                                                           Y               ⌊n(K)/K⌋
 lim s̄θ,µ      (T ) = lim 1 − E(T1 ,...,TK ) ∼ µ(·|T,K)       1 − sθ (Ti )
K→∞                     K→∞
                                                                    i=1
                                                                   " K                            #!
                                                                    Y                 ⌊n(K)/K⌋
                     = 1 − lim         E(T1 ,...,TK ) ∼ µ(·|T,K)          1 − sθ (Ti )
                            K→∞
                                                                    i=1
                                                                          ⌊n(K)/K⌋                            
                     ≥ 1 − lim         Pµ (T | T, K) · 1 − sθ (T ′′ )
                                             ′′
                                                                                       + 1 − Pµ (T ′′ | T, K)
                            K→∞

Now, we already know that
                                           lim Pµ (T ′′ | T, K) = 1
                                        K→∞


                                                      27
Furthermore, as n(K)/K → ∞ as K → ∞ and 0 ≤ 1 − sθ (T ′′ ) < 1, we can deduce that
                                               ⌊n(K)/K⌋
                            lim 1 − sθ (T ′′ )           =0
                                 K→∞

Combining these observations, we can derive that
                                                                ⌊n(K)/K⌋                        
       (K,n(K))
 lim s̄θ,µ      (T ) ≥ 1 − lim Pµ (T ′′ | T, K) · 1 − sθ (T ′′ )           + 1 − Pµ (T ′′ | T, K)
K→∞                        K→∞
                    = 1 − (1 · 0 + (1 − 1))
                    =1
                             (K,n(K))                                               (K,n(K))
As by definition, limK→∞ s̄θ,µ       (T ) ≤ 1, we must have limK→∞ s̄θ,µ        (T ) = 1. Since
the proof of this property did not involve any properties specific to T apart from the fact that
limK→∞ Pµ (T ′′ | T, K) = 1, using limK→∞ Pµ (T ′′ | T ′ , K) = 1, we can derive an analogous
result for T ′ , giving us:
                                 (K,n(K))                    (K,n(K))
                          lim s̄          (T )   =    lim s̄          (T ′ ) = 1
                         K→∞ θ,µ                     K→∞ θ,µ


For the second case, suppose that for all T ′′ with Pµ (T ′′ | T, K) > 0 for some K, the probability
sθ (T ′′ ) that the prover pθ solves T ′′ equals 0. This clearly leads to:
                                  (K,n(K))
                                 s̄θ,µ       (T ) = 0           for all K
and consequently
                                             (K,n(K))
                                      lim s̄          (T )       = 0
                                     K→∞ θ,µ
                                                           (K,n(K))
Then, an analogous result has to hold for limK→∞ s̄θ,µ        (T ′ ). Indeed, otherwise, there would
                                                          ′
exist some statement S with sθ (S) > 0 such that Pµ (S | T , K) > 0 for some K. By Assumption 13,
since T ′ ∼R T , this would imply that
                          lim Pµ (S | T, K) = lim Pµ (S | T ′ , K) = 1
                         K→∞                         K→∞

so in particular, there would exist some value of K such that Pµ (S | T, K) > 0. This contradicts the
assumption that µ(· | T, K) cannot sample any statement with positive provability chance sθ . Hence,
                                 (K,n(K))                    (K,n(K))
                          lim s̄          (T )   =    lim s̄          (T ′ ) = 0
                         K→∞ θ,µ                     K→∞ θ,µ

Either way,
                                   (K,n(K))                       (K,n(K))
                            lim s̄          (T )     =     lim s̄          (T ′ )
                           K→∞ θ,µ                        K→∞ θ,µ




                                                     28
E.3   Proof of Proposition 15

As the second theoretical result about the proposed ensembling framework, we establish that under
minor symmetry assumptions on the success rate of equivalent theorems, increasing the number of
considered reformulations improves the chances of finding a correct proof.
The assumption used for this proposition states that for a given prover pθ , statement T and a rewriting
category R, the probability sθ (T ′ ) of producing a correct proof for T ′ ∈ [T ]R can be viewed as a
random variable sampled from a distribution P[T ]R , characteristic for the equivalence class [T ]R .
Intuitively, this means that given two equivalent formulations of the same problem, we cannot predict
which one of them will be more favorable to pθ . This is motivated by the empirical examples of
inconsistency of modern formal provers (Figure 1, Section 6).
Before proving the main theorem, we first establish a helpful auxiliary result:
Lemma 26. Let X be a [0, 1]-valued random variable, and let K ≤ K ′ be divisors of N . Then,
                               h          ′
                                            iK ′      h         iK
                              E X ⌊N/K ⌋         ≤ E X ⌊N/K⌋

Proof. If K = K ′ , we trivially get equality, so suppose K < K ′ . Let a = N/K ′ and b = N/K.
                                                                     ′
Then, a < b. Applying Hölder’s inequality with exponents r = ab = K                b
                                                                   K > 1 and s = b−a > 1, gives:
                                                            1                 1                a
                  E[X a ] = E[X a · 1b ] ≤ (E[(X a )r ]) r · (E[(1b )s ]) s = (E[X b ]) b
Therefore, raising both sides to the power K ′ , we obtain:
      h         ′
                  iK ′               ′             a K ′
                                                               h            i ab ·K ′    h        iK
    E X ⌊N/K ⌋         = (E[X a ])K ≤ (E[X b ]) b          = E X ⌊N/K⌋                = E X ⌊N/K⌋


Proposition 15 Let R be reciprocal, and T ∈ R be a statement. Assume that for any T ′ ∼R T , the
success probability sθ (T ′ ) ∈ [0, 1] can be viewed as an independent random variable sampled from
some (prior) distribution P[T ]R . Then, for any budget N and divisors K ≤ K ′ of N ,
                                          (K,N )           (K ′ ,N )
                                     s̄θ,µ (T ) ≤ s̄θ,µ (T ),
with strict inequality whenever sθ is non-constant on the support of µ(· | T, K) ⊆ [T ]R .

Proof. Recall that if R is reciprocal, any statement T ′ reachable from T by arrows of R is, in
fact, R-equivalent to T . Hence, µ(· | T, K) samples from [T ]R . The success rate sθ (Ti ) of the
ith sampled statement can be seen as a random variable Si following the distribution Si ∼ P[T ]R .
                                                                                                   (K,N )
Moreover, these random variables are independent, so we can rewrite the probability s̄θ,µ                   (T ) as:
                                                          " K                     #
                 (K,N )
                                                           Y               ⌊N/K⌋
               s̄θ,µ (T ) = 1 − E{T1 ,...,TK } ∼ µ(·|T,K)     1 − sθ (Ti )
                                                                  i=1
                                                                " K                        #
                                                                 Y                ⌊N/K⌋
                            = 1 − E{T1 ,...,TK } ∼ µ(·|T,K)             1 − Si
                                                                  i=1
                                                           " " K               ##
                                                              Y         ⌊N/K⌋
                            = 1 − E{T1 ,...,TK } ∼ µ(·|T,K) E    1 − Si
                                                                        i=1
                                                            "K                  #
                                                             Y h        ⌊N/K⌋ i
                            = 1 − E{T1 ,...,TK } ∼ µ(·|T,K)    E 1 − Si
                                                                  i=1
                                                            "K                #
                                                             Y h     ⌊N/K⌋ i
                            = 1 − E{T1 ,...,TK } ∼ µ(·|T,K)    E 1−S
                                                                  i=1
                                 "K               #
                                  Y h     ⌊N/K⌋ i
                            =1−E    E 1−S
                                          i=1
                                      h            ⌊N/K⌋ iK
                            =1−E           1−S


                                                      29
where S ∼ P[T ]R . Analogously,

                             (K ′ ,N )
                                                     h      ⌊N/K ′ ⌋ iK ′
                            s̄θ,µ        (T ) = 1 − E 1 − S

For notational convenience, let X = 1 − S. It suffices to show:
                                 h       ′
                                            iK ′           h     iK
                           1 − E X ⌊N/K ⌋        ≥ 1 − E X ⌊N/K⌋

which follows trivially from Lemma 26. Tracing back the argument using Hölder’s inequality, we
can additionally conclude that the equality holds if random variables X ⌊N/K⌋ and 1 are proportional,
which is equivalent to requiring X to be constant. This, in turn, translates to sθ being constant on the
support µ(· | T, K).

F     Prompts
F.1   Rewrite generation prompt for GPT

You are an expert Lean4 mathematician .
Task :
Generate { variants_min } -{ variants_max } alternative theorem statements
     that are semantically equivalent
to the provided Lean theorem . Produce as many high - quality distinct
     rewrites as possible , up to the maximum .
Hard constraints :
1) Keep the same variables and hypotheses names exactly as in the input .
2) Keep the same theorem name stem and append suffixes `_v2 `, `_v3 `, ...
     in increasing order .
3) Do not include proofs ; every theorem must end exactly at `:= by ` with
     nothing after
(` sorry `, tactics , or extra lines ).
4) Each rewrite must remain mathematically equivalent to the original
     theorem .
5) Avoid trivial whitespace - only edits . Prefer algebraic / logical rewrites
     .
6) DO NOT substitute hypothesis values / terms into other hypotheses or the
       goal (e.g. if `b = 30 ` , do not replace `b ` with `30 `) .
7) Do not weaken / strengthen the theorem or add junk conjuncts / disjuncts (
     forbidden : `\ and True `, `\ iff False `, extra unrelated assumptions /
     goals ).
Diversity requirement :
- Include several SIMPLE rewrites that only use symmetry / commutativity
     style transformations .
- Examples of SIMPLE rewrites :
   * `a = b ` -> `b = a `
   * `a < b ` -> `b > a `
   * `2 * x = y ` -> `y = x * 2`
   * `u + v = c ` -> `v + u = c `
   * `x ^ 3` -> `x * x * x `
   * `x ^ 2` -> `x * x `
   * `a * b ` -> `b * a `
- Across the whole set , rewrite every hypothesis and the goal at least
     once when possible .
- Also include non - trivial but equivalent reformulations ( not only simple
       ones ).
Coverage checklist ( must satisfy across produced variants ):
- At least 3 variants must rewrite power notation ( `^ 2` or `^ 3 `) into
     repeated multiplication .
- At least 3 variants must use explicit symmetry / commutativity in
     products or equalities .
- At least 2 variants should rewrite division - style equalities into
     product - style equalities when safe .
   Example pattern : `a / b = c ` -> `a = c * b ` or `a = b * c `.


                                                     30
- At least 2 variants should alter parenthesization / ordering of
      multiplicative expressions .
- At least 2 variants should convert '|' divisibility statements into [
      MOD ] or [ ZMOD ] expressions , and vice versa .
- Do not keep one key hypothesis text unchanged in almost all variants .
Allowed transformations include :
- equivalent rearrangements of equalities / inequalities
- equivalent predicate forms (`a | b ` vs congruence / mod -0 forms when
      appropriate )
- syntactic rewrites using commutativity / associativity / distributivity
- rewriting `0 < x ` as `x > 0`, rewriting `eg Even x ` as `Odd x ` when
      appropriate
- rewriting equations into equivalent multiplied / divided forms without
      changing assumptions
- replacing expressions with provably equivalent forms
Few - shot examples ( from existing miniF2F 50 x20 rewrites ):
f { examples }
Now produce rewrites for this theorem :
f - - theorem id : { theorem_label }
``` lean4
f { formal_statement . strip () }
```
Output format :
- Output ONLY Lean theorem declarations .
- Separate each theorem block with one blank line .
- Start from suffix `_v2 `.
- Do not use markdown code fences .
- Never print `sorry ` or a proof body after `:= by `.


F.2   Variable renaming prompt for GPT

You are an expert Lean 4 assistant .
Task :
Given a single Lean 4 theorem declaration ( through `:= by `) , produce a
** renaming ** of its variables and hypothesis names only . The mathematical
meaning must stay the same (α- equivalence ): only binder identifiers
      change .
Rules :
1) Keep the same theorem name as in the input .
2) Do not change the conclusion or hypothesis ** types ** except where a
      name
appears as a binder ( you may rename bound variables consistently ).
3) ` variable_map ` maps old variable names → new names (e.g. `x ` → `u `) .
4) ` hypothesis_map ` maps old hypothesis names → new names (e.g. `h ` → `h1
      ` or `h0 `) .
5) If you rename nothing in a category , use an empty object `{}` for that
       map .
6) ` original ` must be exactly the input theorem string ( after trimming ).
7) ` renamed ` must be the full theorem line (s) ending with `:= by ` only -
      no `sorry `,
tactics , or proof body after `by `.
Output format :
- Output ** only ** one JSON object , no markdown fences , no commentary .
- Schema :
' { original : ... , renamed : ... , variable_map : {...} , hypothesis_map :
      {...}} '
f - - theorem id : { label }
Input theorem :``` lean4
f { stmt }
```




                                         31
F.3   State-to-statement conversion prompt

You are an expert Lean4 formalization assistant .
Task :
Given an original Lean4 theorem statement for reference , and a tactic
     state created after
applying some augmentations to the original theorem , create a theorem
     statement corresponding
to the provided augmented state .
Requirements :
1) Keep theorem name and binder structure aligned with the original
     statement unless the augmented state requires changes .
2) Preserve hypothesis order from the augmented state .
3) Preserve the augmented state 's mathematics exactly ( do not simplify
     away changes ).
4) Replace shorthand notation with explicit Lean forms when appropriate (
     e.g. `\ sqrt2 ` -> ` Real . sqrt 2`, `\pi ` -> ` Real .pi `) .
5) Output must contain exactly one block in Lean markdown fence format :
    ``` lean4
    theorem ... := by
    ```
6) Do not output any explanation or extra text outside that block .
7) Do not include a proof body , tactics , or sorry ; stop exactly at `:= by
     `.
Original statement :
{ original_statement }
Original state :
{ original_state }
Augmented state :
{ augmented_state }




                                             32
