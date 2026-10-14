                                            O NLINE V ERIFICATION OF L ANGUAGE M ODEL R ESPONSES
                                                           U NDER C OST C ONSTRAINTS

                                                                                             A P REPRINT


                                                                                        Erfan Hajihashemi
                                                                      Department of Electrical Engineering & Computer Science
                                                                                  University of California, Irvine
                                                                                        ehajihas@uci.edu
arXiv:2610.02632v1 [cs.LG] 2 Oct 2026




                                                                                           Yanning Shen
                                                                      Department of Electrical Engineering & Computer Science
                                                                                  University of California, Irvine
                                                                                        yannings@uci.edu


                                                                                            October 5, 2026

                                                                                             A BSTRACT
                                                 As large language models are increasingly deployed for multi-step reasoning, verifying the correctness
                                                 of their outputs has become essential for maintaining reliability at scale. Verifying the correctness
                                                 of large language model outputs is often done by querying a costly ground-truth oracle, which is
                                                 impractical to invoke at every step in an online setting. Prior work addresses this by querying a single
                                                 weak verifier on every step, and using its score to decide whether the costly strong verifier needs to
                                                 be queried as well, reserving strong verification for only a small fraction of the steps. However, a
                                                 single fixed weak verifier may not perform consistently well as the subject matter or difficulty of
                                                 incoming queries changes over time, and committing to one in advance risks either overly costly
                                                 or inaccurate verification. We introduce OMVV (Online Multi-Verifier Verification), an algorithm
                                                 that maintains a pool of K candidate weak verifiers with differing cost and verification performance,
                                                 and adaptively routes each round’s decision to a verifier selected via an online score combiner and
                                                 an exponential-weights routing policy. OMVV provides a distribution-free, finite-time guarantee
                                                 on false-accept and false-reject rates across the full pool of verifiers, and further achieves sublinear
                                                 regret against the best fixed verifier in hindsight under a combined cost and consistency objective.
                                                 Experiments on reasoning dataset benchmarks show that OMVV achieves higher accuracy at lower
                                                 verification cost than any single fixed verifier, across a range of operating budgets.

                                        1   INTRODUCTION
                                        Large language models increasingly solve complex problems by producing multi-step chain of thought reasoning traces
                                        (Wei et al., 2022). As such traces are used to drive downstream decisions, search, and agentic pipelines, an incorrect
                                        final answer that goes unflagged can propagate silently into the final output. Verifying a candidate solution against
                                        ground-truth is an effective remedy: training a separate model to judge the correctness of a candidate answer and using
                                        it to rerank or filter samples substantially improves accuracy (Cobbe et al., 2021).
                                        In many practical applications, a language model does not answer queries in isolation: it faces a stream of queries that
                                        arrive sequentially over time, which can naturally be modeled as an online environment. In such a stream, verification is
                                        not only a per query concern, since a mistake left unflagged at one step can propagate forward into the queries and
                                        responses that follow, whether by feeding a wrong intermediate result into subsequent reasoning or by shaping later
                                        interactions around a flawed answer. This has motivated a growing line of work that studies verification of language
                                        models directly as an online problem (Kiyani et al., 2026; Balcan et al., 2026). However, providing an oracle that
                                        checks the correctness of every single generated response in this online setting is often not doable in practice.
                      Online Verification of Language Model Responses Under Cost Constraints                  A P REPRINT



To avoid the cost of obtaining ground-truth for every query, a weak verifier, an inexpensive way to estimate correctness
that is cheaper than the oracle but also less reliable, can be integrated. Relying on such a verifier makes it possible to
decide most responses without ever querying the oracle, calling the oracle only on the subset of responses the weak
verifier is least certain about. However, a single weak verifier might not be sufficient throughout the entire stream:
how well it matches the queries it encounters depends on their subject and difficulty, both of which can shift over the
course of a stream. A verifier well suited to easier queries may become overconfident as difficulty increases, while a
verifier calibrated for harder queries may query the oracle unnecessarily on queries it could have resolved on its own.
We propose OMVV, which addresses this by maintaining a pool of candidate weak verifiers with differing cost and
verification performance rather than committing to a single one. At each round, OMVV routes the response to one of
the candidate verifiers. The oracle is queried only when the selected verifier is itself uncertain about the response. This
routing decision is learned online, and OMVV additionally satisfies a regret guarantee on it, ensuring that its accuracy
and cost approach those of the best fixed verifier in the pool in hindsight. Across mathematical reasoning, logic, and
factual tasks, OMVV outperforms single verifier selective verification (Kiyani et al., 2026), run separately with each of
the two candidate weak verifiers, on accuracy and cost simultaneously.
Contributions. Overall, our contributions can be summarized as follows:

      I) We introduce OMVV, an online algorithm for verifying language model outputs that maintains a pool of weak
         verifiers with differing cost and verification performance and adaptively routes each response to a candidate
         verifier based on its historical performance.
     II) It is proven that OMVV maintains distribution-free finite-time control over both wrongly accepting an incorrect
         response and wrongly rejecting a correct one. We further establish a regret guarantee on the routing decision
         itself, showing that OMVV’s accuracy and cost approach those of the best fixed verifier in the pool in hindsight.
    III) Through experiments on mathematical reasoning, logic, and factual tasks, it is demonstrated that OMVV
         outperforms single-verifier selective verification (Kiyani et al., 2026) achieving better accuracy and cost
         simultaneously.


2   RELATED WORKS

Verifying language model outputs without exhaustive ground-truth checking has been approached from several directions.
One line of work improves individual verification mechanisms. Some use LLM as a judge to evaluate outputs directly
(Liu et al., 2023), while others check generated claims against source documents (Tang et al., 2024). Other work trains
verifiers via next token prediction rather than discriminative classification (Zhang et al., 2025), or scores intermediate
reasoning steps with process level reward models (Wang et al., 2024). A separate line of work improves test time
response selection by combining multiple verifiers. Weaver aggregates weak verifiers using weak supervision to estimate
verifier accuracies with minimal labeled data (Saad-Falcon et al., 2025), while Multi-Agent Verification combines best
of n sampling with equal weight voting across multiple aspect verifiers to scale test time compute (Lifshitz et al., 2025).
Both use a fixed verifier aggregation procedure at inference time: candidate responses are generated and then scored by
an ensemble of verifiers, rather than adaptively deciding, for each query, which verifier to use or whether to escalate to
a costly oracle. Closest to our setting is Selective Strong Verification (SSV) (Kiyani et al., 2026), which uses a single
weak verifier together with adaptive accept and reject thresholds. In contrast, OMVV considers a pool of K candidate
weak verifiers and learns how to route each round among them through an adaptive policy, while also establishing a
regret guarantee for the routing decisions. SSV’s accept and reject framework is closely related to the broader selective
prediction literature. Foundational work poses classification with a reject option as risk minimization with an explicit
rejection cost (Bartlett & Wegkamp, 2008) and formalizes the resulting risk coverage tradeoff (El-Yaniv & Wiener,
2010); more recent work extends selective classification to online settings with partial feedback (Gangrade et al., 2021).
A related line of work is learning to defer. The goal is to learn, for each instance, whether to route the decision to a
model or to a human expert (Mozannar & Sontag, 2020; Mozannar et al., 2023; Okati et al., 2021; Verma & Nalisnick,
2022). In contrast, we consider online routing among a heterogeneous pool of weak verifiers with differing costs and
verification performance, together with the option to escalate to a costly oracle.


3   PROBLEM SETUP

The verification of language models in an online setting is studied in this work. Queries arrive sequentially, and multiple
candidate verifiers are available to verify the generated responses. There is also an oracle that provides the ground-truth
verification label for a pair when queried, at a cost higher than that of any candidate verifier. The generator receives
queries sequentially and, for each query, produces a fixed set of M candidate responses under a predefined generation


                                                            2
                       Online Verification of Language Model Responses Under Cost Constraints                 A P REPRINT



budget, consistent with prior selective-verification settings that consider multiple candidate generations per query
(Kiyani et al., 2026); these candidates are then given to the verifier one at a time for verification.
Online query and response: In the online setting, at each time t = 1, . . . , T , a query response pair pt = (xt , rt ) is
presented for verification, where rt is one candidate response to the query xt . Next, the pair will be verified to see
whether the generated response rt is a valid response for xt or not. We make no assumption that the incoming query
distribution remains fixed over time; the subject matter or difficulty of the queries may change throughout the stream.
Oracle verification: There is an oracle that provides the ground-truth verification for a given pair pt if needed. The
oracle verifier maps pt to a binary value, denoted gt ∈ {0, 1}, which indicates whether the generated response rt is
correct or not.
Multi-verification: A set of K candidate verifiers is available at each time t. Based on the historical performance of
the verifiers, a single verifier kt is selected among the candidate verifiers at each round. The verifier maps pt into a
discrete space {A, R, Q}, and we denote the resulting decision as dt ∈ {A, R, Q}, where A stands for accepting the
response rt , R stands for rejecting the generated response for query xt , and Q stands for querying the oracle, which
models the uncertainty of the verifier in verifying the given pair pt .
Problem Statement. At any time step 0 < t ≤ T :

    Given:
          • a query response pair pt = (xt , rt );
           • K verifiers with different verification performance and cost;
           • an oracle that provides ground-truth verification gt ∈ {0, 1} for a pair pt when queried;
           • target error rates αI , αII ∈ (0, 1) bounding the false-accept and false-reject rates;
            • the historical pairs (xτ , rτ )t−1
                                             τ =1 and their verification outcomes.
    Goal: adaptively select a verifier for each pair pt to achieve high verification accuracy at low cost, while keeping
    the false-accept and false-reject rates below αI and αII , respectively.


4    METHODOLOGY

To verify the generated answer of a language model, a possible way is to query an oracle that provides ground truth
on whether the generated response for the given query is correct (Cobbe et al., 2021; Lightman et al., 2024). In the
online setting, however, querying the oracle at every timestep is prohibitively expensive, which motivates deciding most
rounds with a cheaper weak verifier and reserving the oracle for the rounds the verifier is least certain about (Kiyani
et al., 2026). Committing to a single such verifier can be limiting, since weak verifiers can differ in their verification
performance (Saad-Falcon et al., 2025). We therefore maintain a set of K verifiers, all cheaper than the oracle, differing
in cost and verification performance, and design an online algorithm that learns which verifier to select at each round
from the oracle feedback it collects over time.
Designing such an algorithm requires a way to measure how well a choice of verifier performs at each step, along two
complementary axes: the cost of using that verifier, and how closely its decisions agree with the oracle. We formalize
both next.
Cost. Each candidate verifier incurs a fixed cost ck ∈ [0, 1] to run, reflecting the intuition from before that cheaper
verifiers should be preferred when they suffice. Always selecting the cheapest verifier trivially minimizes the cost
incurred, but may lead to poorer verification performance, since the cheapest verifier is not necessarily the right one for
every input.
Error. A decision made without the oracle can go wrong in two ways, either accepting an incorrect response or rejecting
a correct one. For verifier k, let Tk (T ) := {t ≤ T : kt = k} denote the rounds routed to verifier k, and define
                       (k)                                            (k)
                    N0 (T ) := {t ∈ Tk (T ) : gt = 0} ,             N1 (T ) := {t ∈ Tk (T ) : gt = 1} .                    (1)
The per-verifier false-accept and false-reject rates are then
                                      (k)            1          X
                                   ErrI (T ) :=    (k)
                                                                      1{gt = 0, dt = A},                                   (2)
                                                  N0 (T ) t∈Tk (T )


                                                                3
                      Online Verification of Language Model Responses Under Cost Constraints                     A P REPRINT



                                      (k)             1        X
                                   ErrII (T ) :=     (k)
                                                                       1{gt = 1, dt = R}.                                  (3)
                                                   N1 (T ) t∈Tk (T )
The pooled quantities N0 (T ), N1 (T ), ErrI (T ), ErrII (T ) are defined identically, summing over all t ≤ T without
restricting to a single verifier’s sub stream. The oracle can always be queried to avoid error entirely, but doing so
incurs the maximum possible cost. A good policy must therefore keep cost and error small simultaneously, which is
the tradeoff our algorithm is designed to navigate. We formalize this tradeoff as the following loss for each candidate
verifier k at round t:                                          2
                                           ℓt (k) := λ sk,t − gt + (1 − λ) ck ,                                     (4)
where λ ∈ [0, 1] is a tradeoff parameter. In Equation 4, the first term captures the consistency of verifier k with the
oracle: sk,t is the score verifier k would produce for the current pair pt , which determines the decision made by verifier
k at time t, and a smaller distance from the oracle’s label gt reflects a more reliable decision by verifier k at this round.
We describe how sk,t is computed in further detail later in this section. The second term, ck , is a fixed cost associated
with verifier k.
We treat choosing which verifier to consult as a K-armed decision problem. One verifier is sampled and used at each
round, as in the multi-armed bandit setting (Auer et al., 2002). Querying every verifier at every round would undermine
the cost savings that motivate routing in the first place, so OMVV queries only the sampled verifier kt . The verifier
score is therefore observed for kt alone. This is the defining property of bandit feedback, and it separates our setting
from the full information “prediction with expert advice” setting (Littlestone & Manfred, 1994; Freund & Schapire,
1997), where every expert’s loss is revealed every round regardless of which one is followed.
The loss ℓt (k) in Equation 4 has two parts, each observed under a different rule. The cost term ck is fixed and known in
advance for every verifier, so nothing needs to be observed to use it. It is available every round for every k, selected
or not. The consistency term depends on both the verifier score sk,t and the oracle label gt . Since only the sampled
verifier is queried, its score is the only verifier-specific score observed at round t, while gt is observed only when the
oracle is queried. The loss is therefore full information in its cost part, and bandit feedback, thinned further by the
oracle query decision, in its consistency part. Feedback that sits between full information and bandit feedback has
been studied broadly under partial monitoring (Piccolboni & Schindelhauer, 2001; Cesa-Bianchi et al., 2006), and
selectively querying the true label is closely related to label efficient prediction (Cesa-Bianchi et al., 2005). Our setting
does not need the full generality of partial monitoring, however: it can be handled with the same importance weighted
estimators used for standard adversarial bandits (Auer et al., 2002), alongside a known, deterministic cost term that
needs no observation at all.

4.1   ALGORITHM

We now describe OMVV in full: how a verifier is selected at each round, how its threshold pair governs the ac-
cept/reject/query decision, and how the sampled verifier’s thresholds and score combiner are updated from the oracle’s
feedback.
In the multi-verification setting, we have K candidate verifiers, each initialized in advance with weight wk1 = 1/K.
The weight wkt reflects how favorably verifier k has performed under the objective in Equation 4 up to round t.
                                        wt
Normalizing these weights, w̄kt := PK k wt , gives w̄kt , the probability of selecting verifier k at round t. Collecting these
                                       j=1   j
normalized weights over all K verifiers gives a probability mass function Wt := (w̄1t , . . . , w̄K
                                                                                                  t
                                                                                                    ). At round t, a verifier
kt ∈ {1, . . . , K} is sampled according to Wt and used to evaluate the incoming pair pt = (xt , rt ).
When verifier k is selected at round t, it is prompted with the pair pt and returns a raw score uk,t ∈ [0, 1], with larger
values indicating higher confidence that the response is correct. In addition to the raw score, we also use agreement as a
second signal of correctness, computed from the generator’s own outputs and independent of any verifier’s judgment.
We combine the two via logistic regression. Formally, the agreement feature at ∈ [0, 1] is the fraction of the other
candidate responses generated for the same query that agree with the current one. We refer to the result as a combined
score sk,t , and base each verifier’s decision on sk,t . Formally,
                                                                                  
                                                      (k),t    (k),t        (k),t
                                         sk,t := σ β0       + β1 uk,t + β2 at                                          (5)

                                                    (k),t   (k),t   (k),t
where σ is the logistic sigmoid and β (k),t := (β0 , β1 , β2 ) is verifier k’s coefficient vector, fit separately for
each verifier on its own history of oracle queried rounds and refit as more become available.
Given the combined score sk,t , each verifier’s decision follows a two-threshold rule: reject below a lower threshold,
accept above an upper threshold, and defer to the oracle in between. The intuition behind this structure, as laid out by


                                                               4
                      Online Verification of Language Model Responses Under Cost Constraints                     A P REPRINT



Kiyani et al. (2026), is that when a verifier’s score is confidently low, the response is likely incorrect and should be
rejected; when the score is confidently high, the response is likely correct and should be accepted; and when the score
falls in between, neither conclusion is well supported, and the safer choice is to defer to the oracle rather than guess.
We adopt this structure for each of our K verifiers, applied to its own combined score sk,t .
                                                                      (k),t   (k),t        (k),t     (k),t
Each verifier k maintains its own pair of adaptive thresholds (τR , τA ), with τR           ≤ τA , updated only on
rounds when verifier k is selected and oracle feedback is observed. At round t, the combined score skt ,t of the sampled
verifier is compared against that verifier’s own thresholds:
                                                                       (k ),t
                                               Accept,
                                                            skt ,t > τA t ,
                                                               (kt ),t             (k ),t
                                  region(t) = Uncertain, τR            < skt ,t ≤ τA t ,                             (6)
                                                                       (kt ),t
                                                 Reject,     skt ,t ≤ τR .
                                               

A separate threshold pair is kept for each verifier, rather than one shared pair across all K, since different verifiers can
differ substantially in both the scale of their scores and how those scores relate to correctness.
The action taken at round t follows directly from this region: in the Accept region the response is accepted, in the Reject
region it is rejected, and in the Uncertain region, the oracle is queried and its label gt determines the action. Querying
the oracle only in the Uncertain region, however, is not enough on its own. If a verifier’s Accept region rarely or never
triggers a query, the algorithm does not learn whether the responses it accepts there are actually correct, and an overly
permissive threshold could continue accepting incorrect responses without a signal for correction. To prevent this, the
algorithm queries the oracle with a small probability even in the Accept and Reject regions, governed by exploration
probabilities PA and PR : with probability 1 − PA an Accept-region round is accepted outright, and with probability PA
the oracle is queried to obtain feedback for the adaptive updates without changing the Accept decision already made;
the Reject region is handled symmetrically with PR .
When the oracle is queried, whether from the Uncertain region or from exploration in the Accept or Reject region, the
selected verifier’s threshold pair is updated using the resulting label gt . For verifier kt , with step size η > 0,
                                                                                       (k ),t        !
                        (kt ),t+1           (kt ),t (kt ),t     1[gt =0] 1[skt ,t > τA t ] − αI
                      τA          ← max τR , τA             +η·                                          ,           (7)
                                                                                  qt

                                                                                             (k ),t 
                                                                                                        !
                     (k ),t+1            (kt ),t+1    (kt ),t     1[gt =1] αII − 1[skt ,t ≤ τR t ]
                    τR t      ← min     τA         , τR       +η·                                           ,             (8)
                                                                                 qt
where qt ∈ (0, 1] is the probability with which the oracle is queried at round t (PA in the Accept region, PR in the
Reject region, and 1 in the Uncertain region). Every other verifier’s thresholds are left unchanged. Three things about
                                                                                                     (k ),t+1      (k ),t+1
this update are worth making explicit. The max(·) and min(·) operations preserve the ordering τR t            ≤ τA t
after every update, so the region ordering in Equation 6 is never violated. The accept threshold update only fires when
gt = 0, since that is exactly the condition under which accepting the response would mean wrongly accepting an
incorrect one, and it moves the threshold in the direction that drives the false accept rate toward the target αI ; the
reject threshold update is the mirror image, tied to gt = 1 and the target αII . Dividing by qt corrects for partial oracle
feedback through importance weighting, so the update is unbiased with respect to the corresponding full feedback
update.
The routing weights are updated separately, and every round, for every verifier, not only the sampled one. For each k,
define the loss estimate
                                                      2 1[kt =k] Ot
                                ℓ̂t (k) := λ sk,t − gt ·              + (1 − λ) ck ,                               (9)
                                                            w̄kt qt
where Ot ∈ {0, 1} indicates whether the oracle was queried at round t. The cost term is deterministic and known for
every k, so it is added every round regardless of which verifier was selected. The consistency term, however, is nonzero
only for the sampled verifier on a oracle queried round. Dividing by w̄kt qt corrects for the fact that the consistency term
is observed only when verifier k is sampled and the oracle is queried. Since w̄kt qt is the probability of that event, inverse
probability weighting makes ℓ̂t (k) unbiased for the corresponding full feedback loss. The weight of each verifier is
then updated multiplicatively,
                                            wkt+1 ← wkt · exp − ηH ℓ̂t (k) ,
                                                                             
                                                                                                                          (10)
for a fixed learning rate ηH > 0, and w̄kt+1 is obtained by renormalizing as before. Algorithm 1 summarizes the full
procedure described above.


                                                              5
                      Online Verification of Language Model Responses Under Cost Constraints                   A P REPRINT



Algorithm 1 Online Multi-Verifier Verification (OMVV)
Require: Target error rates αI , αII ∈ (0, 1); tradeoff parameter λ ∈ [0, 1]; exploration probablities {PA , PR };
    threshold step size η > 0; Hedge learning rate ηH > 0; verifier costs (ck )K
                                                                               k=1 ;
 1: Initialize weights wk1 ← 1/K for each k = 1, . . . , K
 2: for t = 1, 2, . . . do
 3:     Receive pair pt = (xt , rt )
        Route: normalize weights, w̄kt ← wkt / j wjt for each k; sample kt ∼ w̄t
                                                P
 4:
 5:     Score: obtain raw score ukt ,t ; compute combined score skt ,t ( 5)
                                                       (k ),t (k ),t
 6:     Region test: set Ot ← 0; compare skt ,t to (τR t , τA t )
                      (kt ),t
 7:     if skt ,t > τA        then
 8:          dt ← A; w.p. PA , query the oracle for gt and set Ot ← 1; set qt ← PA
                             (k ),t
 9:     else if skt ,t ≤ τR t then
10:          dt ← R; w.p. PR , query the oracle for gt and set Ot ← 1; set qt ← PR
11:     else
12:          dt ← Q; query the oracle for gt and set Ot ← 1;
13:     end if
14:     Decision: accept rt if dt = A or (dt = Q ∧ gt = 1); otherwise reject rt .
15:     if Ot = 1 then
16:          Threshold update for verifier kt only ( 7–8)
17:     end if
18:     (thresholds of every k ̸= kt left unchanged)
19:     Routing update: ∀k ∈ [K], compute the loss estimate ℓ̂t (k) ( 9) and update wkt+1 ( 10)
20: end for


5   THEORETICAL ANALYSIS
Error control. OMVV updates each verifier’s thresholds only on rounds when the oracle is queried and feedback is
observed. Since the query stream, the generator, and each verifier’s performance are all allowed to be arbitrary and
time-varying, it is not obvious that these threshold updates keep the realized false-accept and false-reject rates close to
their targets αI , αII . The following theorem shows that they do: OMVV’s error rates remain controlled at every finite
horizon, with no assumption on the stream, the generator, or the verifiers.
Theorem 1 (Error control). Fix a horizon T ≥ 1. For any δ ∈ (0, 1), with probability at least 1 − δ,
                           ErrI (T ) ≤ αI + ∆Ipool (T, δ),       ErrII (T ) ≤ αII + ∆II
                                                                                     pool (T, δ).

Here, ∆Ipool (T, δ) and ∆II
                          pool (T, δ) are finite sample slack terms that decrease as the relevant per verifier sample counts
increase, for fixed exploration and algorithm parameters. Their exact form and the proof are given in Section A.

Regret. Because OMVV operates online, it does not know in advance which of the K verifiers is the best choice
under the combined cost consistency objective in Equation 4. Instead, it must learn an effective routing policy from the
feedback observed over time. We therefore evaluate its routing performance through regret relative to the best fixed
                                                      PT                                    PT               PT
verifier in hindsight, denoted by k ⋆ ∈ arg mink∈[K] t=1 ℓt (k). Formally, let RT (k ⋆ ) := t=1 ℓt (kt ) − t=1 ℓt (k ⋆ )
denote the regret of OMVV’s routing decisions relative to k ⋆ .
Theorem 2 (Routing regret). For any horizon T ≥ 1, OMVV achieves the following expected regret
                                                                  s                   !
                                         ⋆
                                                   p                λ2 K         2
                                                                                    
                                  E RT (k ) = O        T log K ·          + 1−λ         .
                                                                     qmin
                                                                      √
In particular, for fixed K, λ, and qmin > 0, the expected regret is O( T ) and hence sublinear in T . qmin is the smallest
probability, over the whole horizon, with which the oracle is queried. The proof is given in Section A.


6   EMPIRICAL PERFORMANCE
Datasets: We evaluate OMVV on four tasks spanning mathematical reasoning, logic puzzles, factual question answering,
and algebra, to test whether the improvements it provides over a single fixed verifier hold beyond one narrow domain.


                                                             6
                      Online Verification of Language Model Responses Under Cost Constraints                    A P REPRINT




Figure 1: Mean probability that OMVV routes to the cheaper verifier (Qwen2-1.5B), by difficulty. On easy problems,
OMVV favors the cheaper verifier with substantially higher probability than on hard problems, where it shifts toward
the more expensive verifier.


MATH. We use 400 problems from the MATH benchmark (Hendrycks et al., 2021), which contains five difficulty
levels. We select 200 problems from the easiest level, D1, and 200 from the hardest level, D5, as our easy and hard
subsets, respectively. Zebra Logic. A set of 200 logic-grid puzzles (100 easy, 100 hard) from ZebraLogic (Lin et al.,
2025), each requiring the solver to infer a unique assignment of attributes to entities satisfying a list of constraints.
TriviaQA. A set of 400 factual question-answering examples (200 easy, 200 hard) from TriviaQA (Joshi et al., 2017).
DeepMind Mathematics. A set of 600 algebra problems (300 easy, 300 hard) drawn from the linear_2d category of
the DeepMind Mathematics dataset (Saxton et al., 2019), which requires solving a system of two linear equations.
Generator and oracle. For each problem, GPT-4o-mini generates a fixed set of M = 5 candidate responses before
verification. These candidates are subsequently processed one at a time. Ground truth is provided by an oracle specific
to each dataset: for MATH and TriviaQA, the oracle is GPT-4o, acting as an LLM judge that determines whether a
candidate response is correct. For Zebra Logic and DeepMind Mathematics, the oracle is a deterministic programmatic
grader that checks the generated output against the corresponding ground truth. For the programmatic graders, we
assign a normalized unit query cost of 1.0, matching the oracle cost used for GPT-4o, so that verification cost is reported
on a comparable scale across all four datasets.
Verifier pool and query stream. We consider K = 2 candidate weak verifiers for our experimental analysis: Qwen2-
1.5B-Instruct (Yang et al., 2024) and Qwen2.5-3B-Instruct (Qwen et al., 2025), a cheap versus expensive pair with
normalized costs of 0.10 and 0.20, respectively, relative to an oracle cost of 1.0. For every dataset, the query stream is
constructed as alternating blocks of easy and hard problems, presenting a block of easy problems first, followed by a
block of hard problems.
Baselines and evaluation metrics. We compare OMVV against each candidate verifier run independently: Qwen2-
1.5B-Instruct and Qwen2.5-3B-Instruct, each following the single-verifier adaptive procedure of Kiyani et al. (2026). For
each run, we report accuracy, the fraction of problems solved correctly; the false-accept and false-reject ratesErrI (T )
and ErrII (T ), defined in Equations 2 and 3, along with their average (ErrI (T ) + ErrII (T ))/2 as a single summary
of verification error; cost, the average total verification cost per round, accounting for both the selected weak verifier
                                                                                PT
and any oracle query; and the oracle query frequency, OracleFreq(T ) := T1 t=1 Ot , the fraction of rounds on which
the oracle is queried.

6.1   RESULTS

The main goal of OMVV is to improve the accuracy and cost tradeoff over single verifier selective verification while
maintaining the target error rates. As shown in Table 1, OMVV achieves the highest accuracy and the lowest average
error across all four datasets at αI = αII = 0.2, while also attaining the lowest overall verification cost. The two single
verifier baselines exceed the ErrI target on every dataset, whereas OMVV satisfies both target error rates throughout.
A primary reason for OMVV’s accuracy and cost advantage is that it is not committed to a single verifier over the entire
stream. Its routing policy updates the probability of selecting each verifier at every round according to the observed
verification loss, allowing the algorithm to shift toward the verifier that offers a better cost and performance tradeoff for
the current portion of the stream. This adaptive routing is supported by verifier specific score adaptation, with each
verifier maintaining its own score combiner and threshold pair. For example, on MATH, the weak verifiers assign
average raw scores of about 0.83–0.84 even to incorrect responses, indicating limited separation from the raw scores


                                                             7
                      Online Verification of Language Model Responses Under Cost Constraints                    A P REPRINT


Table 1: OMVV versus single-verifier baselines, pooled easy and hard subsets, at αI = αII = 0.2. ErrI and ErrII
values exceeding the 0.2 target are shown in red; the best value in each of Accuracy, Avg(ErrI , ErrII ), Cost, and Oracle
frequency, within each dataset, is bolded.

          Dataset              Method           Accuracy      ErrI      ErrII      Avg     Oracle freq      Cost
                               Qwen2-1.5B        0.6775      0.7655     0.0845    0.425      0.2713       0.3713
          MATH                 Qwen2.5-3B        0.6975      0.5848     0.0807    0.333      0.1425       0.3425
                               OMVV              0.7325      0.1649     0.1919    0.178      0.1952       0.3080
                               Qwen2-1.5B        0.7500      0.5562     0.1617    0.359      0.2718       0.3718
          Zebra Logic          Qwen2.5-3B        0.7250      0.8361     0.0221    0.429      0.1962       0.3962
                               OMVV              0.8550      0.1844     0.1982    0.191      0.2461       0.3659
                               Qwen2-1.5B        0.8025      0.4031     0.0410    0.222      0.1932       0.2932
          TriviaQA             Qwen2.5-3B        0.8050      0.3250     0.1746    0.250      0.1447       0.3447
                               OMVV              0.8325      0.1987     0.1993    0.199      0.1650       0.2778
                               Qwen2-1.5B        0.9267      0.4805     0.4635    0.472      0.1717       0.2717
          DeepMind Math        Qwen2.5-3B        0.9383      0.2558     0.5635    0.410      0.1700       0.3700
                               OMVV              0.9667      0.1384     0.1107    0.125      0.1487       0.2627




alone. Incorporating agreement among the generator’s candidate responses provides an additional signal for the adaptive
threshold decisions.
The oracle query frequency should be interpreted together with the cost of the selected weak verifier. A lower oracle
query frequency does not necessarily imply a lower overall verification cost, since a more expensive single verifier may
require fewer oracle queries because its decisions are less often uncertain, while still incurring a higher verifier cost on
every round. OMVV may therefore query the oracle more frequently than a single more expensive verifier on some
datasets while still achieving a lower overall verification cost by routing a fraction of rounds to the cheaper verifier. The
improvements in Table 1 thus reflect the combined effect of adaptive verifier routing, verifier specific score adaptation,
and selective oracle use.
Figure 1 illustrates how OMVV’s routing adapts to changes in problem difficulty. OMVV has no prior knowledge of
which verifier is better suited to a given problem and receives no explicit difficulty label; instead, its routing policy is
updated from the oracle feedback collected over time. As harder problems enter the stream, the exponential weights
update described in Section 4.1 shifts more probability toward the higher cost verifier over the rounds that follow. On
MATH, for instance, the probability of routing to the cheaper verifier falls from 0.551 on easy problems to 0.190 on
hard ones, indicating a substantial shift toward the stronger verifier as the stream becomes more difficult. This behavior
reflects the motivation in Section 3: rather than committing to a single verifier for the entire stream, OMVV adapts its
routing policy online as the relative performance of the available verifiers changes.
Table 2 extends this analysis beyond a single difficulty change to a setting where the difficulty of the incoming stream
shifts repeatedly, at a rate controlled by the block size B: larger values of B correspond to less frequent shifts, while
B = 1 alternates the difficulty at every problem. Across all block sizes, OMVV achieves the highest accuracy, the
lowest average error, and the lowest verification cost, while also satisfying both target error rates. Notably, even under
the most rapidly changing stream with B = 1, OMVV maintains an accuracy of 0.7250 and an average error of 0.1493,
whereas both single-verifier baselines violate at least one of the target error rates. These results show that OMVV’s
advantage persists even when the stream difficulty shifts frequently.



7   CONCLUSION

We introduced OMVV, an online verification algorithm that adaptively routes responses among weak verifiers with
different costs and verification performance. OMVV provides distribution-free finite-time error control and achieves
sublinear expected regret relative to the best fixed verifier in hindsight. Experiments across multiple benchmarks and
stream conditions show higher accuracy and lower verification cost than single-verifier baselines while maintaining the
target error rates. single verifier baselines while maintaining the target error rates.


                                                             8
                      Online Verification of Language Model Responses Under Cost Constraints                A P REPRINT


Table 2: OMVV versus single-verifier baselines on the MATH stream, at αI = αII = 0.2, across block sizes B. ErrI
and ErrII values exceeding the 0.2 target are shown in red; the best value in each of Accuracy, Avg(ErrI , ErrII ), Cost,
and Oracle frequency, within each block size, is bolded.

                 B     Method          Accuracy      ErrI        ErrII     Avg     Oracle freq    Cost
                       Qwen2-1.5B       0.6675      0.7288       0.0396   0.3842     0.1275      0.2275
                100    Qwen2.5-3B       0.6975      0.2000       0.2116   0.2058     0.1129      0.3129
                       OMVV             0.7225      0.1333       0.1581   0.1457     0.1035      0.2090
                       Qwen2-1.5B       0.6725      0.7927       0.0289   0.4108     0.1587      0.2587
                50     Qwen2.5-3B       0.6900      0.2287       0.1862   0.2074     0.1199      0.3199
                       OMVV             0.7275      0.1119       0.1532   0.1326     0.1328      0.2432
                       Qwen2-1.5B       0.6725      0.7588       0.0563   0.4076     0.1938      0.2938
                25     Qwen2.5-3B       0.6850      0.3621       0.0714   0.2167     0.1025      0.3025
                       OMVV             0.7250      0.1308       0.1498   0.1403     0.1311      0.2423
                       Qwen2-1.5B       0.6825      0.5749       0.2202   0.3975     0.1750      0.2750
                 1     Qwen2.5-3B       0.6875      0.3518       0.0748   0.2133     0.1181      0.3181
                       OMVV             0.7250      0.1385       0.1601   0.1493     0.1250      0.2383



References
Peter Auer, Nicolo Cesa-Bianchi, Yoav Freund, and Robert E Schapire. The nonstochastic multiarmed bandit problem.
  SIAM journal on computing, 32(1):48–77, 2002.
Maria Florina Balcan, Avrim Blum, Kiriaki Fragkia, Zhiyuan Li, and Dravyansh Sharma. Online learnability of chain-
 of-thought verifiers: Soundness and completeness trade-offs. In 3rd AI for Math Workshop: Toward Self-Evolving
 Scientific Agents, 2026. URL https://openreview.net/forum?id=RyX0XTfaDT.
Peter L. Bartlett and Marten H. Wegkamp. Classification with a reject option using a hinge loss. Journal of Machine
  Learning Research, 9(59):1823–1840, 2008. URL http://jmlr.org/papers/v9/bartlett08a.html.
Nicolo Cesa-Bianchi, Gábor Lugosi, and Gilles Stoltz. Minimizing regret with label efficient prediction. IEEE
  Transactions on Information Theory, 51(6):2152–2162, 2005.
Nicolo Cesa-Bianchi, Gábor Lugosi, and Gilles Stoltz. Regret minimization under partial monitoring. Mathematics of
  Operations Research, 31(3):562–580, 2006.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert,
  Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to solve math word problems, 2021. URL
  https://arxiv. org/abs/2110.14168, 9, 2021.
Ran El-Yaniv and Yair Wiener. On the foundations of noise-free selective classification. Journal of Machine Learning
  Research, 11(53):1605–1641, 2010. URL http://jmlr.org/papers/v11/el-yaniv10a.html.
Yoav Freund and Robert E Schapire. A decision-theoretic generalization of on-line learning and an application to
  boosting. Journal of computer and system sciences, 55(1):119–139, 1997.
Aditya Gangrade, Anil Kag, Ashok Cutkosky, and Venkatesh Saligrama. Online selective classification with limited
  feedback. Advances in Neural Information Processing Systems, 34:14529–14541, 2021.
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob
  Steinhardt. Measuring mathematical problem solving with the math dataset. arXiv preprint arXiv:2103.03874, 2021.
Mandar Joshi, Eunsol Choi, Daniel S Weld, and Luke Zettlemoyer. Triviaqa: A large scale distantly supervised
 challenge dataset for reading comprehension. In Proceedings of the 55th Annual Meeting of the Association for
 Computational Linguistics (Volume 1: Long Papers), pp. 1601–1611, 2017.
Shayan Kiyani, Sima Noorani, George J. Pappas, and Hamed Hassani. When to trust the cheap check: Weak and
  strong verification for reasoning. In Forty-third International Conference on Machine Learning, 2026. URL
  https://openreview.net/forum?id=dfN4HMZbc9.
Shalev Lifshitz, Sheila A. McIlraith, and Yilun Du. Multi-agent verification: Scaling test-time compute with goal
  verifiers. In ICLR 2025 Workshop on Modularity for Collaborative, Decentralized, and Continual Deep Learning,
  2025. URL https://openreview.net/forum?id=mGAAoEWOq9.


                                                             9
                      Online Verification of Language Model Responses Under Cost Constraints                A P REPRINT



Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman,
  Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In The Twelfth International Conference on Learning
  Representations, 2024. URL https://openreview.net/forum?id=v8L0pN6EOi.
Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson, Ashish Sabharwal, Radha Poovendran, Peter Clark, and Yejin
  Choi. Zebralogic: On the scaling limits of LLMs for logical reasoning. In Forty-second International Conference on
  Machine Learning, 2025. URL https://openreview.net/forum?id=sTAJ9QyA6l.
Nick Littlestone and K. Warmuth Manfred. The weighted majority algorithm. Information and computation, 108(2):
  212–261, 1994.
Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang, Ruochen Xu, and Chenguang Zhu. G-eval: NLG evaluation using
  gpt-4 with better human alignment. In Houda Bouamor, Juan Pino, and Kalika Bali (eds.), Proceedings of the 2023
  Conference on Empirical Methods in Natural Language Processing, pp. 2511–2522, Singapore, December 2023.
  Association for Computational Linguistics. doi:10.18653/v1/2023.emnlp-main.153. URL https://aclanthology.
  org/2023.emnlp-main.153/.
Hussein Mozannar and David Sontag. Consistent estimators for learning to defer to an expert. In International
  conference on machine learning, pp. 7076–7087. PMLR, 2020.
Hussein Mozannar, Hunter Lang, Dennis Wei, Prasanna Sattigeri, Subhro Das, and David Sontag. Who should predict?
  exact algorithms for learning to defer to humans. In International conference on artificial intelligence and statistics,
  pp. 10520–10545. PMLR, 2023.
Nastaran Okati, Abir De, and Manuel Rodriguez. Differentiable learning under triage. Advances in Neural Information
  Processing Systems, 34:9140–9151, 2021.
Antonio Piccolboni and Christian Schindelhauer. Discrete prediction games with arbitrary feedback and loss. In
  International Conference on Computational Learning Theory, pp. 208–223. Springer, 2001.
Qwen, :, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu,
  Fei Huang, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou,
  Junyang Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu,
  Rui Men, Runji Lin, Tianhao Li, Tianyi Tang, Tingyu Xia, Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su,
  Yichang Zhang, Yu Wan, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. Qwen2.5 technical report, 2025.
  URL https://arxiv.org/abs/2412.15115.
Jon Saad-Falcon, E. Kelly Buchanan, Mayee F Chen, Tzu-Heng Huang, Brendan McLaughlin, Tanvir Bhathal, Shang
  Zhu, Ben Athiwaratkun, Frederic Sala, Scott Linderman, Azalia Mirhoseini, and Christopher Re. Shrinking the
  generation-verification gap with weak verifiers. In ES-FoMo III: 3rd Workshop on Efficient Systems for Foundation
  Models, 2025. URL https://openreview.net/forum?id=BHRFAubSf9.
David Saxton, Edward Grefenstette, Felix Hill, and Pushmeet Kohli. Analysing mathematical reasoning abilities of
  neural models. arXiv preprint arXiv:1904.01557, 2019.
Liyan Tang, Philippe Laban, and Greg Durrett. MiniCheck: Efficient fact-checking of LLMs on grounding documents.
  In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen (eds.), Proceedings of the 2024 Conference on Empirical
  Methods in Natural Language Processing, pp. 8818–8847, Miami, Florida, USA, November 2024. Association for
  Computational Linguistics. doi:10.18653/v1/2024.emnlp-main.499. URL https://aclanthology.org/2024.
  emnlp-main.499/.
Rajeev Verma and Eric Nalisnick. Calibrated learning to defer with one-vs-all classifiers. In International Conference
  on Machine Learning, pp. 22184–22202. PMLR, 2022.
Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang Sui. Math-shepherd:
  Verify and reinforce LLMs step-by-step without human annotations. In Lun-Wei Ku, Andre Martins, and Vivek
  Srikumar (eds.), Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume
  1: Long Papers), pp. 9426–9439, Bangkok, Thailand, August 2024. Association for Computational Linguistics.
  doi:10.18653/v1/2024.acl-long.510. URL https://aclanthology.org/2024.acl-long.510/.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-
  of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems,
  35:24824–24837, 2022.
An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan Li, Dayiheng
  Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong Tang, Jialin Wang, Jian Yang, Jianhong Tu, Jianwei
  Zhang, Jianxin Ma, Jianxin Yang, Jin Xu, Jingren Zhou, Jinze Bai, Jinzheng He, Junyang Lin, Kai Dang, Keming
  Lu, Keqin Chen, Kexin Yang, Mei Li, Mingfeng Xue, Na Ni, Pei Zhang, Peng Wang, Ru Peng, Rui Men, Ruize
  Gao, Runji Lin, Shijie Wang, Shuai Bai, Sinan Tan, Tianhang Zhu, Tianhao Li, Tianyu Liu, Wenbin Ge, Xiaodong


                                                           10
                          Online Verification of Language Model Responses Under Cost Constraints                           A P REPRINT



  Deng, Xiaohuan Zhou, Xingzhang Ren, Xinyu Zhang, Xipin Wei, Xuancheng Ren, Xuejing Liu, Yang Fan, Yang
  Yao, Yichang Zhang, Yu Wan, Yunfei Chu, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, Zhifang Guo, and Zhihao Fan.
  Qwen2 technical report, 2024. URL https://arxiv.org/abs/2407.10671.
Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran Kazemi, Aviral Kumar, and Rishabh Agarwal. Generative
  verifiers: Reward modeling as next-token prediction. In The Thirteenth International Conference on Learning
  Representations, 2025. URL https://openreview.net/forum?id=Ccwp4tFEtE.


A     Proofs
A.1   Proof of Theorem 1

We prove the two bounds via a common argument. We first control the error rates within the substream of rounds routed
to each verifier. We then obtain simultaneous guarantees across all K verifiers by a union bound and combine them
through the pooled error definitions.
Lemma 1 (Per-verifier error control). Fix a horizon T ≥ 1 and a verifier k. Suppose the threshold step size η
is a fixed positive constant, the exploration probabilities satisfy PA , PR ∈ (0, 1] for every t ≤ T with qmin :=
                                                              (k),1     (k),1
mint≤T min{PA , PR } > 0, and the initial thresholds satisfy τR     ≤ τA with both in [0, 1]. Then for any δ ∈ (0, 1),
with probability at least 1 − δ,
                         (k)                 (k)                (k)                   (k)      
                     ErrI (T ) ≤ αI + ∆ N0 (T ), δ ,          ErrII (T ) ≤ αII + ∆ N1 (T ), δ ,                  (11)
where, writing B := 1 + 2η/qmin ,
                                                      s
                                          B                 2 log(4/δ) log(4/δ)
                              ∆(N, δ) :=    +                         +         ,               ∆(0, δ) := 0.
                                         ηN                   N qmin    3N qmin

We prove Lemma 1 through the following four claims. The threshold updates in (7) and (8) fire only when the
oracle-query indicator Ot (Eq. (9)) equals 1, with query probability
                                         qt := Pr(Ot = 1 | Ft−1 , kt , skt ,t ) ∈ {PA , 1, PR }
determined by which region skt ,t falls into, so qt ≥ qmin . Here Ft−1 is the history immediately before round t (all
earlier pairs, decisions, and observed oracle labels, together with every candidate’s raw score and agreement feature
generated alongside pt ). For the analysis, let Ht := σ(Ft−1 , kt , skt ,t , gt ) denote the information after verifier selection
and scoring, with the latent label gt fixed, but before the oracle-query randomization Ot is drawn; the inclusion of gt is
only for analysis and does not imply that OMVV observes it unless the oracle is queried.
        A,(k)                  (k),t
Write xt        := 1[sk,t > τA         ] − αI ∈ [−1, 1], and define
                    A,(k)                                   A,(k)            A,(k)                            Ot A,(k)
                   et       := 1[kt = k] 1[gt = 0] xt               ,     ebt        := 1[kt = k] 1[gt = 0]     x      .             (12)
                                                                                                              qt t
                           R,(k)   R,(k)           R,(k)                                                                    (k),t
The reject quantities xt , et    , and eet   are defined analogously, replacing αI with αII , 1[sk,t > τA                           ] with
          (k),t
1[sk,t ≤ τR ], and 1[gt = 0] with 1[gt = 1].
Claim 1 (Unbiased importance weighting). For every t and every fixed k,
                            h           i                 h            i
                              A,(k)          A,(k)          R,(k)         R,(k)
                          E ebt     | Ht = et      ,    E ebt     | Ht = et     .
                  A,(k)       A,(k)        A,(k)           R,(k)        R,(k)        R,(k)
Consequently, Zt    := ebt    − et      and Zt     := ebt   − et       have conditional mean zero. Hence their partial
sums form martingales with respect to the corresponding analysis filtration.

                                                           A,(k)        A,(k)                                                        A,(k)
Proof. Condition on Ht . If kt ̸= k, then both ebt  and et    are zero. If kt = k, the quantities 1[gt = 0] and xt
are fixed under the conditioning. The only remaining randomness is Ot ∼ Bernoulli(qt ), so
                                                                A,(k) E[Ot | Ht ]
                            h            i
                               A,(k)                                                  A,(k)
                           E ebt     | Ht = 1[kt = k]1[gt = 0]xt                  = et      .
                                                                           qt
The reject-side identity follows analogously.


                                                                        11
                        Online Verification of Language Model Responses Under Cost Constraints                                         A P REPRINT



Claim 2 (Telescoping). For every T ≥ 1,
                            T             (k),T +1    (k),1                    T             (k),1    (k),T +1
                           X     A,(k)  τ          − τA                       X     R,(k)  τ       − τR
                               ebt     ≤ A                  ,                     ebt     ≤ R                  .
                           t=1
                                                 η                            t=1
                                                                                                    η

                                                                    (k),t+1        (k),t          A,(k)
Proof. On a round with kt = k and Ot = 1, (7) gives τA       ≥ τA + η ebt                                 , since the maximum in (7) is at least
its second argument; hence
                                                       (k),t+1    (k),t
                                             A,(k)   τ         − τA
                                           ebt     ≤ A
                                                              η
                                                                                                          (k),T +1       (k),1
in every case. Summing over t = 1, . . . , T telescopes the right-hand side to (τA            − τA )/η. On the reject
                                      R,(k)                                                            R,(k)
side, the bracket in (8) equals −b   et     exactly on rounds with kt = k and Ot = 1, since ebt              is built from
  R,(k)               (k),t                                                         (k),t+1     (k),t      R,(k)
xt      = 1[sk,t ≤ τR ] − αII , the negative of the term appearing there. Thus τR           ≤ τR − η ebt         whenever
                          R,(k)     (k),t    (k),t+1                                             (k),1    (k),T +1
an update fires, giving ebt     ≤ (τR − τR           )/η in every case; summing telescopes to (τR − τR             )/η.

Claim 3 (Uniform boundedness of thresholds). For all t ≤ T + 1,
                                                                     
                                    (k),t  (k),t        η         η
                                   τA , τR ∈ −              , 1+        ,
                                                       qmin      qmin
             (k),T +1       (k),1                  (k),T +1        (k),1
and hence |τA           − τA        | ≤ B and |τR             − τR         | ≤ B, with B as in Lemma 1.

                A,(k)                                                                                        A,(k)
Proof. Since xt        ∈ [−1, 1] and Ot /qt ≤ 1/qmin , every raw increment satisfies |η ebt  | ≤ η/qmin , and likewise on
                                                    (k),t (k),t
the reject side. We show by induction on t that τA , τR both remain in I := [−η/qmin , 1 + η/qmin ] the base case
t = 1 holds since the initial thresholds lie in [0, 1] ⊂ I. Assume both thresholds lie in I at round t, and consider the
                                                         (k),t
raw, pre-projection accept update in three cases. If τA ∈ [0, 1], the update moves the threshold by at most η/qmin ,
                               (k),t                   (k),t       A,(k)
so the result lies in I. If τA > 1, then sk,t ≤ 1τA , so xt              = −αI < 0 and the raw update can only decrease
the threshold: it stays below 1 + η/qmin , and decreases by at most η/qmin , so it stays above 1 − η/qmin ≥ −η/qmin .
    (k),t                            (k),t   A,(k)
If τA < 0, then sk,t ≥ 0 > τA , so xt              = 1 − αI > 0 and the symmetric argument keeps the raw update in
                         (k),t                                              (k),t
I. (At the boundary τA = 0 with sk,t = 0, the indicator 1[sk,t > τA ] evaluates to 0, so this configuration falls
                                                                             (k),t                           (k),t
under the first case rather than the third.) Finally, the projection max(τR , ·) in (7) preserves I, since τR ∈ I by
                                                             (k),t
the induction hypothesis, completing the induction for τA .
                        (k),t                                                      (k),t            (k),t
The argument for τR      is the mirror image, using 1[sk,t ≤ τR ]: for τR        > 1 the indicator equals 1 and
 R,(k)                                                                             (k),t
xt     = 1 − αII makes the update term αII − 1 < 0, decreasing the threshold; for τR < 0 the indicator equals 0
and the update term αII > 0 increases it.
                           (k),1        (k),T +1                                                                     (k),T +1      (k),1
Since both endpoints τA      and τA                lie in an interval of width B = 1 + 2η/qmin , |τA                            − τA       | ≤ B, and
likewise on the reject side.

                                                      A,(k)        PT      A,(k)
Claim 4 (Freedman concentration). Let MT                      :=      t=1 Zt     . With probability at least 1 − δ/2,
                                                                                             s
                     A,(k)            (k)       (k)                                             2 log(4/δ) log(4/δ)
                    MT             ≤ N0 (T ) ε N0 (T ), δ ,                  ε(N, δ) :=                    +         ,
                                                                                                   N qmin    3N qmin
                          R,(k)         (k)           (k)
and symmetrically |MT             | ≤ N1 (T ) ε(N1 (T ), δ) with probability at least 1 − δ/2.

                A,(k)                                 A,(k)              A,(k)
Proof. Write Zt         = 1[kt = k] 1[gt = 0] xt     Ot /qt − 1 . Since |xt     | ≤ 1 and qt ≥ qmin ,
                                                                       
                                      A,(k)   Ot                  1           1       1
                                     Zt     ≤    − 1 ≤ max 1, − 1 ≤               ≤       .
                                              qt                  qt          qt     qmin
                  A,(k)
By Claim 1, E[Zt          | Ht ] = 0, so
                            A,(k)                                           A,(k) 2       1 − qt   1[kt = k] 1[gt = 0]
                  Var Zt            | Ht = 1[kt = k] 1[gt = 0] xt                      ·          ≤                     ,
                                                                                             qt            qmin

                                                                       12
                        Online Verification of Language Model Responses Under Cost Constraints                                                    A P REPRINT



using E[(Ot /qt − 1)2 | Ht ] = (1 − qt )/qt for Ot ∼ Bernoulli(qt ). Summing over t ≤ T ,
                                                                T
                                                 A,(k)
                                                                X               A,(k)        N (k) (T )
                                                VT         :=         Var Zt            | Ht ≤ 0         .
                                                                t=1
                                                                                               qmin

                                                                            A,(k)                                                                     A,(k)
Applying Freedman’s inequality to the martingale MT         with increment bound 1/qmin and variance proxy VT       ≤
   (k)                                                                A,(k)      (k)       (k)
N0 (T )/qmin , allocating tail probability δ/4 to each side, gives |MT      | ≤ N0 (T ) ε(N0 (T ), δ) with probability
at least 1 − δ/2. The reject-side bound follows identically.


Proof of Lemma 1. By Claims 2 and 3,
                                    T              (k),T +1    (k),1                                 T
                                   X     A,(k)  |τ          − τA |    B                             X     R,(k)  B
                                       ebt     ≤ A                   ≤ ,                                ebt     ≤ .
                                   t=1
                                                          η           η                             t=1
                                                                                                                 η

        A,(k)       A,(k)      A,(k)
Since Zt        = ebt       − et         ,
                                              T            T
                                             X    A,(k)
                                                          X     A,(k)    A,(k)   B    A,(k)
                                                 et     =     ebt     − MT     ≤   + MT     ,
                                             t=1          t=1
                                                                                 η

                                                     (k)              (k)
which by Claim 4 is at most B/η + N0 (T ) ε(N0 (T ), δ) with probability at least 1 − δ/2.
                                                                                                                  (k),t
By construction, within verifier k’s Accept region, dt = A if and only if sk,t > τA                                       , so for t ∈ Tk (T ),
                                                                                                          (k),t
                                               1[gt = 0, dt = A] = 1[gt = 0] 1[sk,t > τA                          ].
                                                 PT        A,(k)  P                             (k),t     (k)
Summing over t ∈ Tk (T ) and using                    t=1 et     = t∈Tk (T ) 1[gt = 0]1[sk,t > τA ] − αI N0 (T ), this gives the
exact identity
                                                                   T
              (k)       (k)          (k)
                                                                  X    A,(k)       (k)     B   (k)       (k)       
             N0 (T ) ErrI (T ) = αI N0 (T ) +                         et     ≤ αI N0 (T ) + + N0 (T ) ε N0 (T ), δ
                                                                  t=1
                                                                                           η

                                                                (k)                     (k)                            (k)
with probability at least 1 − δ/2. Dividing by N0 (T ) gives ErrI (T ) ≤ αI + ∆(N0 (T ), δ). The identical argument
on the reject side holds with probability at least 1 − δ/2; a union bound over the two events gives both simultaneously
with probability at least 1 − δ, proving the lemma.


Proof of Theorem 1. Apply Lemma 1 to each verifier k = 1, . . . , K at confidence level δ/K; by a union bound over k,
all K per-verifier bounds hold simultaneously with probability at least 1 − δ. Since every round t ≤ T is routed to
                               PK      (k)
exactly one verifier, N0 (T ) = k=1 N0 (T ) and
                                                                               K
                                                                                        (k)         (k)
                                                                               X
                                                 N0 (T ) ErrI (T ) =                 N0 (T ) ErrI (T ).
                                                                               k=1

                                                                 (k)
Substituting the bound of Lemma 1 for each ErrI (T ), at confidence δ/K, and dividing by N0 (T ) gives
                                                                         K
                                                                  1 X (k)              (k)         
                                     ErrI (T ) ≤ αI +                       N0 (T ) ∆ N0 (T ), δ/K
                                                                N0 (T )
                                                                        k=1
                                                                |                {z                }
                                                                                      =: ∆Ipool (T,δ)


with probability at least 1 − δ. The false-reject bound on ErrII (T ) follows identically, defining ∆II
                                                                                                     pool (T, δ) analogously
       (k)                         (k)
with N1 (T ) in place of N0 (T ).


                                                                                13
                       Online Verification of Language Model Responses Under Cost Constraints                     A P REPRINT



A.2   Proof of Theorem 2

We bound the regret through three steps: showing ℓ̂t (k) is an unbiased estimate of ℓt (k) for every verifier, a deterministic
inequality governing the Hedge weight update, and a bound on the estimate’s second moment; combining the three
yields the stated rate.
For the regret analysis, we regard each verifier’s score sk,t and oracle query probability qt (k) as well defined at every
round, conditional on the history and the current candidate context, regardless of whether verifier k is selected. These
quantities are used only in the analysis. During online execution, OMVV evaluates and observes only the score of the
selected verifier kt .
                                                                                   
Claim 1 (Unbiased loss estimate). Let Gt := σ Ft−1 , gt , {sj,t , qt (j)}K      j=1 . For every round t and every k ∈
{1, . . . , K}, selected or not,
                                                          E ⟨w̄t , ℓ̂t ⟩ | Gt = E ℓt (kt ) | Gt .
                                                                                          
                               E ℓ̂t (k) | Gt = ℓt (k),

Proof. All denominators in (9) are strictly positive: w̄kt > 0 and qt (k) ≥ qmin > 0. Condition on Gt , under which w̄t ,
every sk,t , every qt (k), ck , and gt are fixed. Chaining the routing draw and the query indicator,
                                               E 1[kt = k] Ot | Gt = w̄kt qt (k),
                                                                  

so the importance-weighted term in (9) has conditional expectation 1, giving E[ℓ̂t (k) | Gt ] = λ(sk,t −gt )2 +(1−λ)ck =
ℓt (k). For the second identity, w̄t is Gt -measurable, so E[⟨w̄t , ℓ̂t ⟩ | Gt ] = k w̄kt ℓt (k) = E[ℓt (kt ) | Gt ].
                                                                                  P


Claim 2 (Potential-function inequality). Suppose the routing weights are initialized uniformly, wk1 = 1/K for every
k. Then for every fixed comparator k ⋆ and every ηH > 0,
                              T                       T                                T  K
                              X                       X                    log K   ηH X X t
                                        w̄t , ℓ̂t −         ℓ̂t (k ⋆ ) ≤         +          w̄k ℓ̂t (k)2 .
                              t=1                     t=1
                                                                             ηH     2 t=1
                                                                                                 k=1

                          P    t
                                   
Proof. Let Φt := log        k wk       , so Φ1 = log(K · 1/K) = 0. By (10),
                                                                                                      !
                                                                            X
                                              Φt+1 − Φt = log                     w̄kt e−ηH ℓ̂t (k)       .
                                                                             k

Since ℓ̂t (k) ≥ 0 for every k and t, the inequality e−x ≤ 1 − x + x2 /2 holds with x = ηH ℓ̂t (k) ≥ 0. Using            t
                                                                                                                  P
                                                                                                                    k w̄k = 1
and then log(1 + u) ≤ u,
                                                                   η2 X t
                                     Φt+1 − Φt ≤ −ηH w̄t , ℓ̂t + H         w̄k ℓ̂t (k)2 .
                                                                    2
                                                                                           k
Summing over t = 1, . . . , T and using Φ1 = 0 bounds ΦT +1 from above.
For a lower bound, positivity of the weights gives
                                                                 T
                                                                              !!                 T
                                                      1         X                               X
                ΦT +1 ≥ log wkT⋆+1 = log                exp −ηH     ℓ̂t (k ⋆ )   = − log K − ηH     ℓ̂t (k ⋆ ).
                                                      K         t=1                             t=1

Combining the two bounds, rearranging, and dividing by ηH > 0 gives the claim.

Claim 3 (Second-moment bound). Write bk,t := (sk,t − gt )2 ∈ [0, 1]. For every round t,
                    K                               K                      K
                    X                               X  b2k,t               X    1
                          w̄kt E ℓ̂t (k)2 | Gt ≤ λ2          + 1 − λ2 ≤ λ2          + 1 − λ2 .
                                                                                         
                                                      qt (k)                 qt (k)
                    k=1                                     k=1                                       k=1

                                                 
Proof. Write Xt (k) := 1[kt = k] Ot / w̄kt qt (k) , so (9) reads ℓ̂t (k) = λ bk,t Xt (k) + (1 − λ)ck . Since 1[kt = k] and
Ot are {0, 1}-valued, squaring leaves the numerator unchanged, so
                                                                       1
                                    E Xt (k)2 | Gt =
                                                                                                
                                                                              ,       E Xt (k) | Gt = 1,
                                                                  w̄kt qt (k)

                                                                           14
                         Online Verification of Language Model Responses Under Cost Constraints                       A P REPRINT



the second identity following as in Claim 1’s proof. Condition on Gt , under which bk,t , ck , and λ are fixed. Expanding
the square,
                                                   b2k,t
                            E ℓ̂t (k)2 | Gt = λ2 t         + 2λ(1 − λ) bk,t ck + (1 − λ)2 c2k .
                                           
                                                w̄k qt (k)
Multiplying by w̄kt and summing over k, the factor w̄kt cancels the 1/w̄kt in the first term exactly, leaving
                   K                            K            K
                  X                             X   b2k,t    X      h                                   i
                      w̄kt E ℓ̂t (k)2 | Gt = λ2                 w̄kt 2λ(1 − λ) bk,t ck + (1 − λ)2 c2k .
                                         
                                                           +
                                                   qt (k)
                   k=1                             k=1           k=1
Since bk,t ≤ 1 and ck ≤ 1, the bracketed quantity is at most 2λ(1 − λ) + (1 − λ)2 = (1 − λ)(1 + λ) = 1 − λ2 , and
w̄kt averages to at most this same bound. The second inequality in the claim follows from bk,t ≤ 1.

Claim 1 gives E[⟨w̄t , ℓ̂t ⟩ | Gt ] = E[ℓt (kt ) | Gt ] and E[ℓ̂t (k ⋆ ) | Gt ] = ℓt (k ⋆ ). Taking expectations of both and summing
over t turns the left-hand side of Claim 2 into E[RT (k ⋆ )].
For the right-hand side, taking expectations and applying Claim 3, then using qt (k) ≥ qmin for every k, t,
                   " T K                  #  T       K
                                                                          !
                    XX
                               t        2
                                            X
                                                   2
                                                     X     1                       KT
                 E           w̄k ℓ̂t (k) ≤       λ             + (1 − λ ) ≤ λ2
                                                                        2
                                                                                         + (1 − λ2 )T.
                     t=1                    t=1
                                                        qt (k)                     q min
                            k=1                           k=1

Combining,                                                                        
                                            log K       ηH      KT
                               E RT (k ⋆ ) ≤                  λ2      + (1 − λ2 )T
                                 
                                                      +
                                                 ηH       2      qmin
for every ηH > 0. The
                   p  right-hand side has√the form A/η H +η H B/2 with A = log K and B = λ2 KT /qmin +(1−λ2 )T ,
               ⋆
minimized at ηH = 2A/B with value 2AB, giving
                           s                                                      s                !
                                                                                    λ2 K
                                                            
                   ⋆
                      
                                         2
                                           KT            2
                                                                      p
                                                                                                 2
            E RT (k ) ≤ 2 log K λ                + (1 − λ )T = O        T log K ·        + (1 − λ ) ,
                                           qmin                                     qmin
which is sublinear in T .

B     ADDITIONAL EXPERIMENTS
B.1   Empirical Validation of Sublinear Regret

Theorem 2 establishes that OMVV’s expected regret against the best fixed verifier in hindsight, E[RT (k ⋆ )], grows
sublinearly in T . To validate this empirically, we compute the realized (non-expected) trajectory Rt (k ⋆ ) =
Pt                     ⋆
   s=1 ℓs (ks ) − ℓs (k ) on several datasets (MATH, DeepMind Math linear_2d, and TriviaQA), using the same
K=2 verifier pool (qwen2_1.5b, qwen2.5_3b) as the main reported results. Here ks is the verifier OMVV actually
                                   PT
selected at round s, k ⋆ = arg mink t=1 ℓt (k) is fixed once from the full-horizon totals, and ℓt (k) is computed from
each verifier’s own combiner-transformed score at every round. We compute the same quantity for the single-verifier
SSV baseline, whose verifier choice is fixed throughout the stream.
Figure 2 compares the cumulative regret trajectories of OMVV and SSV across the three datasets. In all cases, OMVV’s
cumulative regret rises steeply early in the stream and then flattens over the remainder, indicating that OMVV’s
per-round loss has essentially matched that of the best fixed verifier. This decelerating growth is consistent with
the sublinear expected regret guarantee in Theorem 2. In contrast, the SSV baseline exhibits approximately linear
cumulative regret growth over the observed horizon, with no comparable flattening. The comparison illustrates the cost
of committing to a single verifier when the better one for a given stream is not known in advance.

B.2   Block size Experiment: DeepMind Math (linear_2d)

We conduct an additional experiment on DeepMind Math (linear_2d) using the same protocol as Table 2, with
the block size B controlling how frequently the stream alternates between easy and hard problems. Table 3 reports
the results. Across all block sizes, OMVV achieves the highest accuracy, the lowest average error, and the lowest
verification cost among the three methods. It also achieves the lowest ErrI at every block size. Neither single verifier
baseline satisfies both error targets for any value of B, whereas OMVV satisfies both targets throughout. These results
show that OMVV remains effective under repeated changes in problem difficulty on DeepMind Mathematics as well as
MATH.


                                                                15
                      Online Verification of Language Model Responses Under Cost Constraints                 A P REPRINT




Figure 2: Empirical cumulative regret Rt (k ⋆ ) of OMVV and the SSV baseline relative to the best fixed verifier in
hindsight. OMVV exhibits flattening cumulative regret, consistent with the sublinear expected regret guarantee of
Theorem 2. In contrast, SSV shows approximately linear regret growth over the observed horizon.

Table 3: OMVV versus single-verifier baselines on the DeepMind Math non-stationary stream, at αI = αII = 0.2,
across block sizes B. ErrI and ErrII values exceeding the 0.2 target are shown in red; the best value in each of Accuracy,
Avg(ErrI , ErrII ), Cost, and Oracle frequency, within each block size, is bolded.

                 B     Method          Accuracy      ErrI        ErrII     Avg      Cost     Oracle freq
                       qwen2_1.5b       0.9333      0.2288       0.6786   0.4537   0.2903      0.1903
                100    qwen2.5_3b       0.9267      0.8627       0.0314   0.4471   0.2833      0.0833
                       OMVV             0.9433      0.1405       0.1417   0.1411   0.2214      0.1153
                       qwen2_1.5b       0.9433      0.2828       0.6419   0.4624   0.2836      0.1836
                 50    qwen2.5_3b       0.9267      0.8627       0.0365   0.4496   0.2813      0.0813
                       OMVV             0.9483      0.1186       0.1588   0.1387   0.2343      0.1242
                       qwen2_1.5b       0.9367      0.1870       0.6791   0.4331   0.2909      0.1909
                 25    qwen2.5_3b       0.9233      0.8679       0.0399   0.4539   0.3017      0.1017
                       OMVV             0.9533      0.1667       0.1095   0.1381   0.2486      0.1393
                       qwen2_1.5b       0.9317      0.3978       0.5075   0.4527   0.2852      0.1852
                 1     qwen2.5_3b       0.9267      0.8627       0.0348   0.4488   0.2847      0.0847
                       OMVV             0.9583      0.0991       0.1915   0.1453   0.2430      0.1384



B.3   Evaluation at a Different Error-Rate Target

We also evaluate OMVV under a different error target by setting αI = αII = 0.25, instead of 0.2, across all four
datasets. Table 4 reports the results. OMVV achieves the highest accuracy, the lowest verification cost, and the lowest
ErrI on every dataset. Moreover, OMVV satisfies both error targets across all four datasets, whereas neither single
verifier baseline satisfies both targets on any dataset. These results indicate that the empirical advantages of OMVV are
not specific to the αI = αII = 0.2 setting used in the main experiments.


B.4   Verifier Implementation Details and Prompt Specifications

Across all four datasets, we use a multi-model pipeline to generate, score, and verify candidate solutions. gpt-4o-mini
serves as the solution generator, while Qwen2-1.5B-Instruct and Qwen2.5-3B-Instruct serve as the two weak verifiers.
Prompt wording varies across datasets: MATH and DeepMind Math (linear_2d) use the same weak verifier prompt,
while Zebra Logic and TriviaQA use prompts tailored to their respective tasks. For MATH and TriviaQA, correctness
is judged by gpt-4o acting as the oracle. For Zebra Logic and DeepMind Math, correctness is determined by a
deterministic programmatic grader, since both tasks admit an exact check against the ground truth. We provide
representative prompts below for the three roles: generator, weak verifier, and oracle.


                                                            16
                     Online Verification of Language Model Responses Under Cost Constraints             A P REPRINT


Table 4: OMVV versus single-verifier baselines, pooled easy and hard subsets, at αI = αII = 0.25. ErrI and ErrII
values exceeding the 0.25 target are shown in red; the best value in each of Accuracy, Avg(ErrI , ErrII ), Cost, and
Oracle frequency, within each dataset, is bolded.

               Dataset      Method         Accuracy      ErrI     ErrII      Avg      Cost     Oracle freq
                            qwen2_1.5b       0.6775     0.7845    0.0352   0.4099    0.3367      0.2367
               MATH         qwen2.5_3b       0.7000     0.4928    0.0845   0.2887    0.3794      0.1794
                            OMVV             0.7175     0.2018    0.2290   0.2154    0.3346      0.2114
                            qwen2_1.5b       0.7200     0.6519    0.0880   0.3700    0.3500      0.2500
            zebra_logic     qwen2.5_3b       0.6900     0.8810    0.0243   0.4527    0.3514      0.1514
                            OMVV             0.8300     0.2447    0.2277   0.2362    0.3430      0.2214
                            qwen2_1.5b       0.7925     0.4069    0.0199   0.2134    0.3001      0.2001
             TriviaQA       qwen2.5_3b       0.7950     0.3306    0.1897   0.2602    0.3435      0.1435
                            OMVV             0.8325     0.1698    0.1796   0.1747    0.2882      0.1755
                            qwen2_1.5b       0.9250     0.2969    0.6573   0.4771    0.2704      0.1704
          DeepMind Math     qwen2.5_3b       0.9267     0.7552    0.1195   0.4374    0.2919      0.0919
                            OMVV             0.9583     0.2488    0.0889   0.1689    0.2651      0.1473




B.4.1    Generator


   Generator Prompt — Math (GPT-4o-mini)

   Solve this math problem step by step.         Show your reasoning, then give the final answer.
   PROBLEM:
   {problem}
   Respond with JSON:
   {
        "reasoning": "Your step-by-step reasoning here...",
        "final_answer": "Your final answer (just the answer,
        e.g., ’42’ or ’3/4’ or ’x=5’)"
   }




   Generator Prompt — Zebra Logic (GPT-4o-mini)

   Solve this logic grid puzzle. Each category has one value per column (entity); use the
   clues to deduce the unique correct arrangement.
   PUZZLE:
   {question}
   Respond with JSON:
   {
        "reasoning": "Brief step-by-step deduction...",
        "answer_table": "The completed table as plain text,
        one line per category, in the exact format:
        | CategoryName | value1 | value2 | ... |
        (same column order as the puzzle’s blank table, left to right)"
   }



                                                        17
                     Online Verification of Language Model Responses Under Cost Constraints   A P REPRINT



B.4.2   Weak Verifier

   Weak Verifier Prompt — MATH

   Rate the correctness of this math solution on a scale from 0.0 to 1.0.
   PROBLEM:
   {problem}
   REASONING:
   {reasoning}
   FINAL ANSWER:
   {final_answer}
   Consider:
         1. Is the reasoning mathematically sound?
         2. Are all calculations correct?
         3. Does the final answer follow from the reasoning?
   Respond with ONLY a JSON object, nothing else:
   {"score":     0.XX}

This prompt is reused verbatim for DeepMind Math.

   Weak Verifier Prompt TriviaQA

   Rate the correctness of this trivia answer on a scale from 0.0 to 1.0.
   QUESTION:
   {question}
   REASONING:
   {reasoning}
   ANSWER:
   {final_answer}
   Consider:
         1. Does the reasoning show genuine knowledge of the relevant facts, or is it
            vague/guessing?
         2. Is the answer specific and directly responsive to the question?
         3. Does the final answer follow logically from the reasoning?
   Respond with ONLY a JSON object, nothing else:
   {"score":     0.XX}


B.4.3   Oracle
   Oracle Prompt — MATH (GPT-4o)

   Determine if two math answers are equivalent.
   PROBLEM:
   {problem}
   STUDENT’S REASONING:
   {reasoning}
   STUDENT’S ANSWER:
   {generated_answer}
   CORRECT ANSWER:
   {ground_truth_answer}



                                                      18
               Online Verification of Language Model Responses Under Cost Constraints    A P REPRINT



Are these answers equivalent?    Consider:
      • Different formats:    "5", "5.0", "5/1", "$5$", "\boxed{5}" are all equivalent
      • Simplified vs unsimplified:    "2/4" = "1/2"
      • Different notation:    "x=3" vs "3" (if asking for x)
Respond with JSON:
{"is_correct": true/false,
  "explanation": "brief reason"}




                                                19
