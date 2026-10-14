                                         D IRECT O PTIMIZATION OF G ENERATORS FOR S EARCH
                                         IN AUTOMATED T HEOREM P ROVING

                                          Adam Ousherovitch                                    Ambuj Tewari
                                          Department of Statistics                             Department of Statistics
                                          University of Michigan                               University of Michigan
                                          aoushero@umich.edu                                   tewaria@umich.edu


                                                                                     A BSTRACT
arXiv:2609.25575v1 [cs.AI] 22 Sep 2026




                                               Fine-tuned Large Language Models (LLMs) significantly advance Automated Theorem
                                               Proving (ATP), but are often deployed as guiding policies within tree search rather
                                               than for single-attempt generation. Recent work shows cross entropy is suboptimal
                                               for an LLM used in flat search strategies such as aggregation or filtering and that
                                               work has developed new loss functions to correct this misalignment. Extending this
                                               alignment to tree search is more challenging: proof discovery depends on exploration
                                               and recovery through off-trace states that supervised demonstrations do not reveal.
                                               We extend Compute-Aligned Training (CAT) to this setting through an abstraction
                                               of policy-guided search, deriving tractable, trace-supported losses. Alongside these
                                               search-aware losses, we introduce a search-agnostic uniform-allocation (UA) loss that
                                               accounts for the budget without specifying the specific search. Both induce scalar
                                               weights on per-tactic cross-entropy gradients. We characterize how off-trace behavior
                                               affects the search-aware weights, including conditions for vanishing approximation
                                               error at large budgets. On a Lean benchmark, both approaches achieve higher observed
                                               proof-success rates than cross-entropy across six search strategies, with strong results
                                               from a single shared UA adapter. Budget sweeps show larger gains over cross-entropy
                                               at 256 than at 16 expansions, implying CAT scales with test time compute.



                                         1   I NTRODUCTION

                                         Automated Theorem Proving (ATP) is an important frontier in Artificial Intelligence (AI) (Yang
                                         et al., 2024), with applications in software and hardware verification (Bengio & Malkin, 2024).
                                         Formal verifiers such as Lean 4 (de Moura & Ullrich, 2021) allow generated proofs to be checked,
                                         but proof generation remains difficult because rewards are sparse and horizons are long (Poesia et al.,
                                         2024). Large Language Models (LLMs) predict proof steps (Polu & Sutskever, 2020), yet a single
                                         flawed step can invalidate an entire attempt. Recent approaches therefore pair LLMs with structured
                                         search (Lample et al., 2022; Polu et al., 2022; Song et al., 2024), which retains partial proofs and
                                         explores alternative continuations rather than requiring every step to succeed on the first attempt.
                                         LLMs driving search are typically trained through Supervised Fine-Tuning (SFT) with Cross-
                                         Entropy (CE). Recent work shows that CE can be suboptimal when deployment uses search
                                         (Ousherovitch & Tewari, 2026; Chen et al., 2025), but existing corrections focus on flat strategies
                                         such as candidate aggregation (Wang et al., 2023) or filtering (Chen et al., 2021; Cobbe et al., 2021).
                                         Extending alignment to tree search is fundamentally more difficult because success probability in-
                                         cludes unsuccessful exploration followed by recovery, and depends on how compute is allocated
                                         across intermediate proof states. An exact objective therefore requires off-trace continuations that
                                         demonstrated proof traces do not supply.
                                         We address this gap by formalizing policy-guided search and constructing tractable Compute-
                                         Aligned Training (CAT) losses for this kind of search. Given a demonstrated proof trace, we restrict
                                         the modeled search to observed states and collapse deviations into a trace-miss event. This yields
                                         search-aware objectives that preserve selected aspects of the strategy’s compute allocation. Their
                                         gradients are weighted sums of the usual per-tactic CE gradients, emphasizing steps according to
                                         their influence on modeled proof success.


                                                                                           1
Alongside these objectives, we introduce a simple search-agnostic uniform-allocation (UA) loss.
UA assigns a uniform local compute budget to each demonstrated step, accounting for repeated
sampling without specifying the deployed search rule. It thus provides a shared training objective for
use across search algorithms, rather than an approximation tied to one particular deployed strategy.
Trace support introduces approximation error because demonstrations omit alternative proofs and
the compute consumed by off-trace exploration. We characterize these effects through the per-tactic
gradient weights and identify when search-aware weights scale better than CE with more budget.
On a Lean benchmark, both strategy-specific CAT and UA attain higher accuracy than an epoch-
matched CE control under all six evaluated strategies (Table 1). A shared UA adapter performs
strongly across strategies, while search-aware CAT yields an additional observed gain under
Pass@N . Experiments also show larger gains over CE at N = 256 than at N = 16 (Table 2).


1.1   R ELATED W ORK

Automated Theorem Proving. The application of deep learning to ATP has rapidly evolved along-
side LLMs (Polu & Sutskever, 2020; Han et al., 2022). Modern neural provers target interactive
verification environments like Lean (de Moura & Ullrich, 2021; Zheng et al., 2022), with open-
weight milestones such as Lean Copilot (Song et al., 2024), Llemma (Azerbayev et al., 2023), and
ReProver (Song et al., 2025) powered almost exclusively by SFT. Our work is strictly situated within
this SFT paradigm. We explicitly scope our analysis away from systems that interleave informal
natural-language reasoning with formal verification (Jiang et al., 2023; Wu et al., 2022), as well as
online Reinforcement Learning (RL) pipelines (DeepMind, 2024).
Test-Time Search Algorithms. The use of search in ATP falls in the wider trends of utilizing
inference-time compute (Snell et al., 2024). Search in ATP is diverse. It includes uninformed traver-
sal methods like Depth-First Search (DFS) (Pearl, 1984) or Pass@N (Chen et al., 2021), and the
more complex policy-guided searches like Best-First Search (BFS) (Hart et al., 1968), most notably
Levin Search and its modern neural adaptations (Orseau et al., 2018; Orseau & Lelis, 2021; Xin et al.,
2025). While prior literature has extensively benchmarked these algorithms in isolation, it treats the
language model as a static, search-agnostic prior. Crucially, the literature has never investigated how
the structural assumptions of these distinct search rules interact with the training of the policy itself.
Test-Time Aligned Training. A growing body of work recognizes that standard supervised ob-
jectives fail to align models with inference-time search (Ousherovitch & Tewari, 2026; Chen et al.,
2025; Chow et al., 2025; Balashankar et al., 2025; Tang et al., 2025). However, these efforts focus
overwhelmingly on non-branching strategies where the global search objective can be expressed as
an exact function of observed generation probabilities. Within ATP, the sole existing attempt at test-
time aligned training is Direct Coverage Optimization (DCO) (Chen et al., 2025), which focused
exclusively on Pass@N. Because the global success probability of Pass@N can be expressed as a
closed-form function of on-path tactic probabilities, DCO sidesteps the structural approximation
problem entirely. By contrast, state-of-the-art theorem provers rely on branching strategies whose
objectives cannot be resolved purely from on-path data. This paper bridges that gap.


1.2   C ONTRIBUTIONS

• A Framework for Search-Aligned Training. We formalize policy-guided search and derive
  tractable losses for branching strategies. We also develop a budget-based UA loss independent of
  the specific search’s structure. Both approaches induce scalar weights on per-tactic CE gradients.


• Characterizing the Trace-Supported Approximation. For Pass@N and best-first search, we
  analyze how unobserved alternative proofs and off-trace compute consumption affect search-
  aware gradient weights, including their dependence on the test-time budget.


• Empirical Evaluation in Lean. Across six search strategies, strategy-specific CAT and UA each
  attain higher success rates than CE. We also evaluate gains across deployment budgets.


                                                    2
2       A G ENERAL O BJECTIVE FOR S EARCH -A LIGNED T RAINING
This section formalizes LLM-guided search and derives a general aligned objective and the search-
agnostic UA objective. We assume familiarity with Interactive Theorem Proving (ITP).1

2.1       S ETUP
Let the environment be a state space X (proof states), an action space Y, and a transition T :
X × Y → X ∪ {xerr }, where xerr is the state produced by incorrect tactics. The LLM defines a
stochastic policy πθ (y | x). A dataset D provides valid traces; a single trace is
                              τ ∗ = (x0 , y1∗ , x1 , . . . , xL−1 , yL
                                                                     ∗
                                                                       , xL ),       xL = xQED ,
where each demonstrated tactic yt∗ moves the environment from xt−1 to xt . Write pt =                 πθ (yt∗ |
xt−1 ). Standard SFT with CE maximizes the likelihood of these traces:
                          L                            L
                                                                     (t)
                         X                            X
            LCE (θ) = −      log πθ (yt∗ | xt−1 ) = −     log pt ,  LCE := − log pt .                      (1)
                         t=1                          t=1
At test time, the policy is deployed inside a search algorithm A with a compute budget. We wish to
optimize the probability that A, using πθ , finds a proof within that budget.

2.2       S EARCH AS C ONFIGURATION DYNAMICS
A is defined by its interaction with memory, which we define via configurations: c = ⟨F , M ⟩.
The frontier F holds the nodes available for expansion with a heuristic score (insertion order, internal
confidence, etc.); its elements are tuples (x, s) with x ∈ X , s ∈ R. We may write x ∈ F for
(x, s) ∈ F for notational ease. M holds everything else: the policy, the remaining budget, the
unavailable nodes, etc. Budget is most naturally interpreted as either tactic expansions or rollouts.
Budget handling can be encoded in the specification of the strategy.
A selects a node x ∈ F , samples a tactic y ∼ πθ (· | x), executes it, and updates its configuration
from the observation z = T (x, y). Excluding the initialization of c0 from x0 and the compilation of
the returned proof from M , A is fully specified by two operations,
                                                SA (x | c),          UA (c, x, z),
a (possibly stochastic) selection rule SA and a deterministic update rule UA .
A configuration is solved if it contains a completed proof, and dead if its budget is exhausted. Let
J A (c) be the true probability that A, started from c, ever discovers a proof. It satisfies
                  (
          A          1 if c solved; 0 if c dead (and unsolved),
        J (c) = P                          P                  A
                                                                                                (2)
                        x∈F (c) SA (x | c)   y∈Y πθ (y | x) J   UA (c, x, T (x, y)) , otherwise

and the deployed objective is J A (θ) = J A (c0 ), where c0 encodes the start state x0 and the full
budget. Returning any valid trajectory from x0 to xQED counts as success.
Equation (2) is exact but cannot be evaluated from a supervised trace. Consider expanding a frontier
node on the trace, say x = xt−1 . The tactic space partitions into three disjoint sets: the demonstrated
tactic {yt∗ }, the invalid tactics It := {y : T (xt−1 , y) = xerr }, and the valid but off-trace tactics
Ot := {y : T (xt−1 , y) ∈     / {xerr , xt }}. With off-trace states defined as xt,y = T (xt−1 , y) for
y ∈ Ot , the sum in Equation (2) then expands to:
     X
        πθ (y | xt−1 ) J A UA (c, xt−1 , T (xt−1 , y)) = pt J A UA (c, xt−1 , xt )
                                                                                 
         y
             X                                              X                                             (3)
                    πθ (y | xt−1 ) J A UA (c, xt−1 , xerr ) +  πθ (y | xt−1 ) J A UA (c, xt−1 , xt,y ) .
                                                                                                      
        +
             y∈It                                                    y∈Ot

The dataset supplies neither probabilities within It ∪ Ot nor continuations J A (UA (c, xt−1 , xt,y ))
containing unobserved off-trace states. Off-trace tactics may lead to alternate proofs or rejoin the
trace so the exact objective depends on the search space outside of our dataset.
    1
        A full formalization is provided in Section B.


                                                                 3
2.3    T HE T RACE -S UPPORTED S URROGATE
To obtain a tractable objective, we restrict the search to states from the demonstrated trace. Let Cbτ ∗
be the configurations whose frontier and memory reference only x0 , . . . , xL . We replace the true
transition by an offline version,
                                                      xt , y = yt∗ ,
                                                    
                                  Tτ ∗ (xt−1 , y) =
                                  b                                                                 (4)
                                                      ⊥τ , y ̸= yt∗ ,
where ⊥τ marks any deviation from the trace: valid off-trace and invalid tactics are collapsed into
one training-time event. This transition induces two projected update rules,
                                        b + (b
                                        U                  b − (b
                                         A c, x),          U A c, x),

the positive update when the selected node advances xt−1 → xt , and the negative update following
a trace miss. Both updates map to Cbτ ∗ . At a demonstrated state, the model either samples yt∗ with
probability pt or deviates with probability 1 − pt .

Trace-supported recurrence. The surrogate success probability is
            (
             1 if b
                  c solved; 0 if b   c dead,
JbA (b
     c; p) = P                         h
                                                  b + (b
                                                                
                                                                                    b − (b
                                                                                                  i
                x∈F (b
                    b c) SA (x | c
                                 b ; p) p t(x) J
                                               bA U
                                                   A   c , x); p  + (1 − pt(x) ) J
                                                                                 bA U
                                                                                      A  c , x); p   ,   else
                                                                                                           (5)
where t(x) is the index of x in τ ∗ .
We call this loss Compute Aligned Training (CAT), following Ousherovitch & Tewari (2026)
                     JbτA∗ (θ) = JbA b           bA                bA
                                              
                                     c0 ; p(θ) , L CAT (θ) = − log Jτ ∗ (θ),                              (6)
      c0 encodes x0 and the initial budget. We will assume the recursion is finite.2
where b

2.4    T HE CAT G RADIENT
The following Proposition shows search strategy can be completely specified for training by its triple
           b − ), and that its loss and per-tactic gradient weights follow mechanically.
      b +, U
(SA , UA    A

                                                               b − ). Then:
                                                          b +, U
Proposition 1 (CAT Loss). Fix a strategy A given by (SA , UA    A


  (i) Equation (5) has a unique solution, and JbτA∗ (θ) depends on θ only through p = (p1 , . . . , pL ).3
  (ii) The CAT gradient is a weighted sum of per-step cross-entropy gradients,
                                            L
                              bA
                                            X              (t)                   pt ∂ JbτA∗
                           ∇θ LCAT (θ) =           btA ∇θ LCE ,
                                                   w                    btA =
                                                                        w                   .             (7)
                                             t=1                                JbA∗ ∂pt
                                                                                 τ

Proof. (i) Under the assumption the budget is finite and decrements with each update, it terminates
after finitely many steps and assigns a unique value to each configuration. All θ-dependence enters
only through pt(v) or possibly through the scores sA (·; p).
                                                  (t)                                     (t)
(ii) By (i), ∇θ JbτA∗ = t ∂pt JbτA∗ ∇θ pt . From LCE = − log pt we have ∇θ pt = −pt ∇θ LCE , so
                       P

                                    L                      L
                               1 X ∂ JbτA∗          (t) 
                                                          X   pt ∂ JbτA∗     (t)
          ∇θ − log JbτA∗ = −
                       
                                           − pt ∇θ LCE =                 ∇θ LCE .
                             JbτA∗ t=1 ∂pt                   JbA∗ ∂pt
                                                          t=1 τ


As noted by Chen et al. (2025) for the case of Pass@N , separating w     btA lets one filter low-weight
gradients before they corrupt batch normalization statistics, stabilizing training.
   2
     Sufficient conditions for this include decrements of budget every expansion or decrements every rollout
and a finite demonstrated trace.
   3
     Differentiability naturally follows if selection is smooth in θ.


                                                       4
2.5       A S EARCH -AGNOSTIC U NIFORM -A LLOCATION O BJECTIVE
The same gradient form permits a compute-aware objective without specifying A. For an expansion
budget N ≥ L, UA assigns each demonstrated step a uniform local budget K̄ = N/L and uses
                                YL
                 JbUA (p; N ) =     1 − (1 − pt )K̄ ,    b UA = − log JbUA .
                                                  
                                                         L CAT                              (8)
                                         t=1
For integer K̄, this is the probability that every demonstrated step succeeds within its own quota of
independent attempts, without transferring unused quota between steps. For noninteger N/L, we
use the continuous extension of the formula. This allocation is a modeling choice, not a claim about
how a particular deployed algorithm distributes its budget. By Proposition 1,
                                                K̄pt (1 − pt )K̄−1
                                       btUA =
                                       w                           .                              (9)
                                                 1 − (1 − pt )K̄
The rule depends on N , L, and pt , but not on A. At N = L it recovers CE; additional local attempts
reduce the emphasis on tactics already likely to be sampled. Thus UA is search-agnostic, but not
compute-agnostic. Its connection to the shared-budget formulation is detailed in Section J.

3       S TRATEGY-S PECIFIC O BJECTIVES
We instantiate the construction for Pass@N and best-first search using Proposition 1.4

3.1       PASS @N
Pass@N uses up to N independent rollouts (Figure 3); here N counts rollouts, not tactic expansions.
                                  c = (r, t), where r counts remaining rollouts, including the current
In the trace-supported model, let b
one, and t indexes the next demonstrated tactic. Advancement gives (r, t + 1); a miss abandons the
rollout and gives (r − 1, 1). Thus Equation (5) becomes
                           J(r,         b t + 1) + (1 − pt )J(r
                            b t) = pt J(r,                     b − 1, 1),                         (10)
with J(r,                b t) = 0 for t ≤ L. A rollout completes the demonstrated trace with
     b L + 1) = 1 and J(0,
                     QL
probability πproof := t=1 pt , giving
                               JbτPass@N
                                   ∗     (θ) = 1 − (1 − πproof )N .                     (11)
Applying Proposition 1 yields the same weight at every step of the trace:
                                         N πproof (1 − πproof )N −1
                             wbtPass@N =                             .
                                            1 − (1 − πproof )N

3.2       B EST-F IRST S EARCH
We consider policy-guided best-first search (BFS) (Orseau et al., 2018; Orseau & Lelis, 2021; Xin
et al., 2025). A node xk reached through tactics y1 , . . . , yk , k ≥ 1, is scored by
                                                                      1/k
                                                Yk
                            sBFS (xk ; πθ ) =      πθ (yj | xj−1 ) .                       (12)
                                                        j=1
The algorithm pops the highest-scoring frontier node, samples B tactics there, and inserts valid
children (Figure 4). Here N counts tactic expansions: each sample costs one unit.

Trace-supported instantiation. We use a retry surrogate with configuration b        c = (b, t), where b is
the remaining expansion budget and the only live node is xt−1 . Starting from (N, 1), advancement
gives (b − 1, t + 1) and a miss gives (b − 1, t). Retaining the node after a miss is a modeling choice:
this surrogate replaces the deployed finite per-pop sampling with retries until the demonstrated tactic
is sampled or the budget is exhausted. Its singleton frontier also removes score-based competition.
The recurrence is
                       JbBFS (b, t) = pt JbBFS (b − 1, t + 1) + (1 − pt )JbBFS (b − 1, t),
                                                                                                     (13)
                 JbBFS (b, L + 1) = 1,        JbBFS (0, t) = 0 (t ≤ L).
    4
        Objectives for other strategies are given in Sections D and E.


                                                           5
Objective. Let Tt ∼ Geom(pt ) independently count the samples needed at step t, including the
                                 PL
successful sample, and write SL = t=1 Tt . For N ≥ L, the surrogate success probability is
                                  JbτBFS
                                     ∗   (θ) = P(SL ≤ N ).                                 (14)
The shared budget couples the per-tactic weights, which follow by differentiating Equation (13).
The connection to UA’s fixed local allocation is detailed in Section J.

4       A PPROXIMATION E RROR
A demonstrated trace tells us how one proof succeeds, but not what happens when search leaves that
path. At state xt−1 , we can compute the probability of missing the demonstrated tactic. This section
intends to characterize what is lost in not having information about this event at training. We study
this missing information through two channels: alternative proofs (the bypass channel) and compute
spent on unsuccessful off-trace exploration (the trap channel). How do these unseen consequences
change the importance of sampling the demonstrated tactic? Full derivations are in Section C.5

4.1     E FFECTS OF THE C HANNELS ON THE T RUE W EIGHT
Bypass: missing the trace isn’t failing. A different tactic may lead to a valid proof without
completing τ ∗ . The surrogate cannot see these successes. For Pass@N , accounting for alternative
proofs reduces the deployed weight relative to the trace-supported weight.
Theorem 1 (Bypass Deflation). Under Assumption 1, for Pass@N with N > 1 and every step t,
                                   wt⋆ ≤ wbtPass@N < 1 = wtCE .                                         (15)
               btPass@N − wt⋆ | < |1 − wt⋆ |.
Consequently, |w

The proof and decomposition of the missing alternative-success contributions are given in Theo-
rem 4 and eq. (25).

Trap: a miss can cost much more than one attempt. A valid but unhelpful tactic can lead
search into a branch that consumes many expansions before the demonstrated state is selected again.
Unlike an immediate rejection, this excursion leaves less budget for completing the proof. Our
approximation understates the cost of such misses.
To isolate this effect, we censor alternative proofs, so only completion of τ ∗ counts as success while
off-trace exploration remains possible (Lemma 4). We quantify the resulting upward pressure on
weights in a model with a common deterministic return cost.
Theorem 2 (Shared-Budget Bracketing under Deterministic Excursions). Under Assumption 2, let
N ≥ L be an integer. Every miss costs 1 ≤ κ ≤ κ̄ < ∞ expansions before returning to the same
trace state; successful trials cost one, and κ is independent of p. Then
                                                             
                                                        N −L
                      wttrap (N ) ∈ w bt (N ), w
                                               bt L +               ⊆ [w
                                                                       bt (N ), 1],      (16)
                                                          κ̄
where wttrap = wt (J trap ) and noninteger budget arguments are rounded down.

The mechanism is a reduction in effective budget to Neff = L + (N − L)/κ (Proposition 3). The
surrogate assumes κ = 1: a miss costs one expansion. At the other extreme, if every miss prevents
recovery, success requires following the trace without mistakes, recovering CE’s unit weights. Finite
excursion costs interpolate between these cases within this model.

What the trace cannot determine. Two environments can agree on every demonstrated transition,
all ps , the search rule, and the budget, yet differ in what a miss causes. When those off-trace
differences produce distinct deployed weights, no rule using only these trace-level inputs can be
exact in both environments (Proposition 4). Thus, solving the trace-supported recurrence exactly
does not resolve the missing information about recovery.
    5
     Throughout, ps ∈ (0, 1) and wt (J) = pt ∂pt log J for differentiable J > 0. Derivatives follow Equa-
tion (19): all other demonstrated probabilities, conditional distributions over non-demonstrated tactics, and
off-trace policy conditionals are held fixed.


                                                     6
 4.2     L ARGE -C OMPUTE S CALING : C AN S EARCH R ECOVER FROM A M ISS ?
 More compute can compensate for a delay, but not for permanent loss of the opportunity to recover.
 At N = L in the trap-only model, there is no room for wasted expansions: success requires every
 demonstrated tactic on its first attempt, and both the deployed and surrogate weights equal one.
 Larger budgets create opportunities to recover, making the outcome depend on whether excursions
 eventually return. The following limits hold with the policy and excursion parameters fixed.
 Theorem 3 (Large-Budget Limits and Recoverability). (i) Pass@N . Under Assumption 1,
                                    wt⋆ (N ) −→ 0,       bt (N ) −→ 0.
                                                         w
     Hence the search-aware weight error tends to zero, while CE’s weight error tends to one.
(ii) Shared-budget excursions. Under Assumption 3, each miss at step s independently causes per-
     manent absorption with probability qs ∈ [0, 1); otherwise it incurs a bounded excursion before
     returning to the same trace state. Only the demonstrated proof counts as success. Holding qs
     and the finite-excursion laws fixed under differentiation,
                                                                        qt
                         bt (N ) −→ 0,
                         w                  wttrap (N ) −→ ωt :=                  .
                                                                 pt + (1 − pt )qt

 See Propositions 5 and 6 for the derivations.
 When all excursions are recoverable (qs = 0), both deployed and surrogate weights eventually
 vanish: avoiding a particular miss matters less when search has enough budget to try again. With
 permanent absorption, avoiding the miss retains value even with unlimited compute. The retry
 surrogate overlooks this risk, leaving limiting error ωt ; CE’s limiting error is 1 − ωt .
 The analysis therefore identifies what trace-only training leaves unresolved: alternative routes to
 success, the compute needed to recover, and the possibility of never recovering. These quantities can
 be modeled, but are not determined by the demonstrated trace. Additional assumptions can specify
 them, and training-time search offers a way to collect evidence about them. Neither is replaced by
 evaluating the same trace-supported surrogate more exactly.

 5       E XPERIMENTS
 We test whether accounting for budgeted search during SFT improves proof discovery, whether
 matching the training objective to the deployed strategy helps, and how the resulting gains vary with
 test-time budget. We compare search-aware CAT and search-agnostic UA with a CE control.

 Setup. We use Lean 4 through LeanDojo (Yang et al., 2023), training on leandojo-
 benchmark-4-random, a random split of mathlib4 (The mathlib Community, 2020). The held-
 out pool contains 458 theorems whose reference proofs have 2–5 steps; any kernel-verified proof
 counts as success. We initialize from Qwen2.5-Math-7B-Instruct (Qwen Team, 2024) and fine-tune
 with LoRA (Hu et al., 2021). Within each experiment, models share a CE warm-up.6 The control
 then receives one additional CE epoch, while the search-aware and UA models use one additional
 epoch with their respective weights. Data, ordering, and optimizer settings are otherwise identi-
 cal. Evaluation budgets count node expansions, each comprising one tactic sample and its kernel
 verification.7 Full details are in Section G.

 5.1     E XPERIMENT 1: T RAINING FOR S EARCH ACROSS S TRATEGIES
 At N = 256 expansions, we evaluate Pass@N , BFS, DFS variants (Section D), and Monte Carlo
 Tree Search (MCTS) (Kocsis & Szepesvári, 2006).8 For each deployed strategy, we compare CE,
 the corresponding search-aware weights, and the same single shared UA adapter. This study also
 applies wall-clock caps; capped runs without a proof count as failures (Section G.3).
     6
      Two warm-up epochs for Section 5.1 and one for Section 5.2.
     7
      The Pass@N objective in Section 3.1 counts rollouts. We use N/4 as its training parameter, a fixed
 approximation to the expansion budget rather than an exact conversion.
    8
      Our MCTS implementation uses the policy’s Levin score as its value estimate.


                                                     7
Table 1: Proofs found (%) at N = 256 on 458 held-out theorems. Columns are deployed strate-
gies. The same UA adapter is used throughout. ∗ marks p < 0.05 against CE under the same
strategy; bold marks the highest reported rate.

              Training objective   Pass@N    BFS    DFS     RDFS    VDFS     MCTS
              CE                    21.2     23.8   19.2    20.7     21.2    20.3
              Search-aware CAT      26.6∗    25.1   20.7    23.6∗    23.8    22.5
              Shared UA             25.1∗    26.9   23.6∗   25.3∗    24.5∗   25.1∗




Figure 1: Both training families improve accuracy over CE. Proofs found (%) on 458 held-out
theorems with a budget of N = 256 tactic expansions. Search-aware CAT uses strategy-matched
training objectives. UA uses one adapter across all strategies. UA has the highest accuracy under
branching strategies; search-aware CAT leads under Pass@N . Error bars show 95% intervals.
Results Both search-aware CAT and UA have higher observed success rates than CE under all
six strategies (Table 1), showing that accounting for deployment-time compute provides substantial
gains over standard SFT. The shared UA objective is a strong search-agnostic approach, attaining
the highest point estimate under the five branching strategies. At the same time, search-aware CAT
achieves the highest observed success under Pass@N (26.6% versus 25.1% for UA), showing mod-
eling the deployed search strategy can yield additional improvement. Consistent with this, within
the search-aware family, matching training and deployment gives higher point estimates for the
Pass@N /BFS adapter pair: 26.6% versus 23.7% under Pass@N , and 25.1% versus 24.5% under
BFS (Table 3). Together, these results support compute-aware training and suggest that modeling
the deployed strategy can provide additional benefits.

5.2   E XPERIMENT 2: A LIGNMENT G AIN VERSUS T EST-T IME B UDGET

We train a separate search-aware CAT adapter for each strategy (Pass@N or BFS) and budget N ∈
{16, 64, 256}, and evaluate each adapter at its corresponding budget. This sweep removes the per-
strategy and per-theorem wall-clock caps, but each model receives at most 80 hours of evaluation
on four A100 GPUs. At each budget, we compare CAT and CE only on theorems for which both
completed evaluation; Table 2 reports the paired subset sizes. N = 1024 runs completed only 56–57
paired theorems and are reported separately in Section H.

Gains persist across the evaluated budgets. Search-aware CAT has positive paired gains at every
reported budget in Table 2. The observed gains at N = 256 exceed those at N = 16 for both
Pass@N (+4.2 versus +2.0 points) and BFS (+6.9 versus +4.4). However, these are finite-budget
performance comparisons, not direct measurements of the weight-error limits in Section 4.

6     C ONCLUSION
This paper studies how to train an LLM from demonstrations when it will be deployed within
policy-guided search under a finite compute budget. We develop two complementary approaches:


                                                8
Table 2: Paired search-aware CAT gain over CE. n is the paired subset size; b and c count CAT-
only and CE-only successes. Gains are in percentage points. The 95% intervals use the variance
approximation (b + c)/n2 on the probability scale; p is the exact two-sided McNemar test.

              Strategy                                        Budget N        n      b/c       Gain (pp), 95% interval       p
                                                              16             458    10/1           +2.0 [0.5, 3.4]          0.012
              Pass@N                                          64             458    28/8           +4.4 [1.8, 6.9]          0.001
                                                              256            408    29/12          +4.2 [1.1, 7.2]          0.012
                                                              16             458     28/8         +4.4 [1.8, 6.9]           0.001
              BFS                                             64             458    34/13         +4.6 [1.7, 7.5]           0.003
                                                              256            407     37/9         +6.9 [3.6, 10.1]         < 0.001

                                                                          Alignment Gain versus Test-Time Budget

                                                                         Pass@N
                                                              10
                                                                         BFS
                         Alignment gain (percentage points)




                                                               8


                                                               6


                                                               4


                                                               2


                                                               0
                                                                    16                      64                       256
                                                                                    Expansion budget N


Figure 2: Paired search-aware CAT gain over CE with budget-matched adapters. Error bars are 95%
intervals. Completed subsets differ across budgets, so connecting lines are descriptive rather than a
common-cohort comparison.


search-aware CAT objectives that incorporate a model of the search strategy, and a search-agnostic
uniform-allocation objective that accounts for compute without specifying the search rule. Both
induce scalar weights on the usual per-tactic CE gradients. Although our experiments focus on
ATP, the framework provides a starting point for studying other settings in which generative mod-
els guide tree search. Our analysis characterizes how alternative proofs and off-trace exploration
affect search-aware gradient weights. It identifies conditions under which their approximation error
vanishes as the test-time budget grows while CE remains misaligned. Empirically, all objectives
attain higher observed proof-success rates than an epoch-matched CE control across all six evalu-
ated strategies. The shared UA objective performs strongly across search algorithms, while search-
aware CAT achieves the highest observed success under Pass@N , demonstrating that incorporating
strategy-specific structure can, in some cases, provide an additional benefit beyond generic compute
awareness. Budget sweeps additionally show larger gains over CE at 256 than at 16 expansions for
both tested strategies. Together, these findings show that considering the downstream search during
training can improve performance.

Limitations and Future Work. Our experiments use one model and short reference proofs, with
training restricted to offline SFT. UA accounts for compute without modeling the search rule; search-
aware CAT models selected search dynamics on the demonstrated trace. Both remain trace-only. Ad-
ditional training-time compute could sample one-step deviations, explore local trees around demon-
strations, and increasingly approximate deployment search. One-step samples reveal alternative
transitions; deeper searches provide evidence about alternative proofs and recovery costs. Such
observations could refine search-aware objectives beyond fixed allocation. Testing whether these
refinements improve performance, and how to allocate training compute between supervision and
search, remain future work.




                                                                                           9
R EFERENCES
Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen McAleer, Al-
  bert Q Jiang, Jia Deng Jia, Sean Welleck, et al. Llemma: An open language model for mathemat-
  ics. arXiv preprint arXiv:2310.10631, 2023.
Ananth Balashankar, Ziteng Sun, Jonathan Berant, Jacob Eisenstein, Michael Collins, Adrian Hutter,
  Jong Lee, Chirag Nagpal, Flavien Prost, Aradhana Sinha, Ananda Theertha Suresh, and Ahmad
  Beirami. Infalign: Inference-aware language model alignment, 2025. URL https://arxiv.
  org/abs/2412.19792.
Yoshua Bengio and Nikolay Malkin. Machine learning and information theory concepts towards an
  ai mathematician, 2024. URL https://arxiv.org/abs/2403.04571.
Feng Chen, Allan Raventós, Nan Cheng, Surya Ganguli, and Shaul Druckmann. Rethinking fine-
  tuning when scaling test-time compute: Limiting confidence improves mathematical reasoning.
  In Advances in Neural Information Processing Systems, 2025. URL https://openreview
  .net/forum?id=jvVQeSMeGM.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared
 Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large
 language models trained on code. arXiv preprint arXiv:2107.03374, 2021.
Yinlam Chow, Guy Tennenholtz, et al. Inference-aware fine-tuning for best-of-n sampling in large
  language models. In International Conference on Learning Representations, 2025.
Karl Cobbe, Vineet Kosaraju, et al. Training verifiers to solve math word problems. arXiv preprint
  arXiv:2110.14168, 2021.
Rémi Coulom. Efficient selectivity and backup operators in monte-carlo tree search. In Computers
   and games, pp. 72–83. Springer, 2006.
Rémi Coulom. Computing elo ratings of move patterns in the game of go. In Computer Games
   Workshop, 2007.
Tri Dao. FlashAttention-2: Faster attention with better parallelism and work partitioning. In Inter-
  national Conference on Learning Representations (ICLR), 2024.
Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language.
  In Automated Deduction – CADE 28, pp. 625–635. Springer International Publishing, 2021. doi:
  10.1007/978-3-030-79876-5_37. URL https://doi.org/10.1007/978-3-0
  30-79876-5_37.
Google DeepMind. Ai achieves silver-medal standard solving international mathematical olympiad
  problems. Google DeepMind Blog, 2024. URL https://deepmind.google/discover
  /blog/ai-achieves-silver-medal-standard-solving-international-m
  athematical-olympiad-problems/.
Jesse Michael Han, Jason Razeghi, Igor Babuschkin, Ilya Sutskever, and Stanislas Polu. Proof arti-
  fact co-training for theorem proving with language models. In International Conference on Learn-
  ing Representations, 2022.
Peter E Hart, Nils J Nilsson, and Bertram Raphael. A formal basis for the heuristic determination
  of minimum cost paths. IEEE Transactions on Systems Science and Cybernetics, 4(2):100–107,
  1968.
Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang,
  and Weizhu Chen. Lora: Low-rank adaptation of large language models, 2021. URL https:
  //arxiv.org/abs/2106.09685.
Albert Q Jiang, Sean Welleck, Jin P Zhou, Timothée Li, Jiacheng Liu, Mateja Jamnik, Simon
  Lacoste-Julien, and Yuhuai Wu. Draft, sketch, and prove: Guiding formal theorem provers with
  informal proofs. In International Conference on Learning Representations (ICLR), 2023.


                                                10
Levente Kocsis and Csaba Szepesvári. Bandit based monte-carlo planning. In European Conference
  on Machine Learning, pp. 282–293. Springer, 2006.
Guillaume Lample, Marie-Anne Lachaux, Thibaut Lavril, Xavier Martinet, Amaury Hayat, Gabriel
  Ebner, Aurélien Rodriguez, and Timothée Lacroix. Hypertree proof search for neural theorem
  proving. arXiv, 2022. doi: 10.48550/arxiv.2205.11491.
Laurent Orseau and Levi H. S. Lelis. Policy-guided heuristic search with guarantees, 2021. URL
  https://arxiv.org/abs/2103.11505.
Laurent Orseau, Levi H. S. Lelis, Tor Lattimore, and Théophane Weber. Single-agent policy tree
  search with guarantees, 2018. URL https://arxiv.org/abs/1811.10928.
Adam Ousherovitch and Ambuj Tewari. Test time aligned post training. arXiv preprint, 2026. Forth-
  coming/Under Review.
Judea Pearl. Heuristics: Intelligent Search Strategies for Computer Problem Solving. Addison-
  Wesley, 1984.
Gabriel Poesia, David Broman, Nick Haber, and Noah D. Goodman. Learning formal mathematics
  from intrinsic motivation, 2024. URL https://arxiv.org/abs/2407.00695.
Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving,
  2020. URL https://arxiv.org/abs/2009.03393.
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya
  Sutskever. Formal mathematics statement curriculum learning. arXiv, 2022. doi: 10.48550
  /arxiv.2202.01344.
Qwen Team. Qwen2.5 technical report. arXiv preprint arXiv:2412.15115, 2024.
Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling LLM test-time compute optimally
  can be more effective than scaling model parameters. arXiv preprint arXiv:2408.03314, 2024.
  URL https://arxiv.org/abs/2408.03314.
Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Lean copilot: Large language models as copi-
  lots for theorem proving in lean. arXiv, 2024. doi: 10.48550/arxiv.2404.12534.
Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Lean copilot: Large language models as copi-
  lots for theorem proving in lean, 2025. URL https://arxiv.org/abs/2404.12534.
Yunhao Tang, Kunhao Zheng, Gabriel Synnaeve, and Rémi Munos. Optimizing language models for
  inference time objectives using reinforcement learning. arXiv preprint arXiv:2503.19595, 2025.
  URL https://arxiv.org/abs/2503.19595.
The mathlib Community. The Lean mathematical library. In Proceedings of the 9th ACM SIGPLAN
  International Conference on Certified Programs and Proofs (CPP), pp. 367–381. ACM, 2020.
  doi: 10.1145/3372885.3373824.
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang, Aakanksha
  Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language
  models. In International Conference on Learning Representations, 2023.
Yuhuai Wu, Albert Q Jiang, Wenda Li, Markus N Rabe, Charles Staats, Mateja Jamnik, and Chris-
  tian Szegedy. Autoformalization with large language models. In Advances in Neural Information
  Processing Systems (NeurIPS), volume 35, pp. 32353–32368, 2022.
Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang Wu, Xia Xiao, Yifan Sun, Shen Zheng, and
  Kai Shen. Bfs-prover: Scalable best-first tree search for llm-based automatic theorem proving,
  2025. URL https://arxiv.org/abs/2502.03438.
Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godbole,
  Zhichen Lai, and Anima Anandkumar. LeanDojo: Theorem proving with retrieval-augmented
  language models. In Advances in Neural Information Processing Systems (NeurIPS), volume 36,
  pp. 23722–23745, 2023.


                                               11
Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li, Kristin Lauter, Swarat Chaudhuri, and Dawn
  Song. Formal mathematical reasoning: A new frontier in ai, 2024. URL https://arxiv.or
  g/abs/2412.16075.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. minif2f: a cross-system benchmark for
  formal olympiad-level mathematics. In International Conference on Learning Representations,
  2022.




                                             12
A    S TRATEGY I MAGES

                                           Budget: N = 4 parallel threads


                                                                  x0

                                      y1              y1                      y2         y3


                x1                               x1                                ×                        x′1
             y1,a                                    y1,b                                                       y3,a


                    ×                          QED                                                              ×


Figure 3: Pass@N Parallel Search. N = 4 independent paths explore the tree simultaneously. A
single valid path reaching QED constitutes a global success.


                                                     Best-First Node Expansions
                                                                       S = 1.0

                                                                         x0

                                                     ⃝
                                                     1 y1                              ⃝
                                                                                       4 y2


                                   S = 0.8      x1                                            x′1     S = 0.6


                                  ⃝
                                  2 y1,a                    ⃝
                                                            3 y1,b                                  ⃝
                                                                                                    5 y3



                        S = 0.3    x2                         ×                          QED




                                           Global frontier re-evaluation:
                                                S(x′1 ) > S(x2 )




Figure 4: Policy-Guided Best-First Search. The numbered circles indicate chronological node ex-
pansions. Expanding x0 yields two valid states on the frontier, x1 (S = 0.8) and x′1 (S = 0.6). The
algorithm greedily expands x1 (step 2). However, generating the tactic to reach x2 drops the path’s
geometric mean to S = 0.3. Because the algorithm evaluates the global frontier, the decision rule
abandons the active path and dynamically jumps across the tree to expand x′1 (step 4), ultimately
finding the proof.




                                                                  13
                                Global Budget: N = 5 sequential expansions


                                                          x0

                                                   ⃝
                                                   1 y1


                                                          x1

                                         ⃝
                                         2 y1,a                    ⃝
                                                                   3 y1,b


                                          ×                          x2

                                                          ⃝
                                                          4 y2,a            ⃝
                                                                            5 y2,b


                                                            ×               QED


Figure 5: Depth-First Search. The numbered circles indicate the chronological order of node expan-
sions. The algorithm pushes forward, backtracks locally upon failure (e.g., from step 2 back to x1 ),
and terminates the search immediately upon reaching the QED state at step 5.




                                         Randomized Backtracking


                                                            x0

                                                     ⃝
                                                     1 y1


                                                            x1

                                              ⃝
                                              2 y2                 5 y2′
                                                                   ⃝

           ⃝
           4 Uniform random
                                              x2
              backtrack to x1                                        QED

                                       ⃝
                                       3 y3


                                              ×

Figure 6: Randomized Depth-First Search. After expanding a deep, dead-end path (steps 1–3), the
algorithm selects a node uniformly at random from the active path {x0 , x1 , x2 } to backtrack to. In
this case, it randomly selects x1 (step 4), escaping the trap at x2 and successfully finding the proof
on an alternative branch (step 5).




                                                          14
                                                  Value-Guided Backtracking
                                                                   S = 1.0

                                                                      x0

                                                               ⃝
                                                               1 y1


                                                         S = 0.8      x1

                                                        ⃝
                                                        2 y2                 5 y2′
                                                                             ⃝

      ⃝
      4 Score-weighted random
               backtrack to x1            S = 0.3       x2                    QED
                   (P ∝ 0.8)

                                                 ⃝
                                                 3 y3


                                                        ×

Figure 7: Value Guided Depth-First Search (VDFS). After expanding into a dead end (step 3), the
algorithm evaluates the active path prefix {x0 , x1 , x2 }. Instead of backtracking uniformly, it samples
an ancestor proportional to its Levin score S. In this case, it randomly jumps to x1 (step 4) because
its higher score (S = 0.8) makes it a heavily favored target over the deep trap at x2 (S = 0.3). This
allows it to successfully escape and find the proof on an alternative branch (step 5).




                                                               MCTS


                                                                x0

                                           ⃝
                                           1 y1                               ⃝
                                                                              2 y2
                                     V =0.80                                     V =0.60

                                          x1                                         x′1

                                 ⃝
                                 3 y1,a                  UCT re-evaluation:                ⃝
                                                                                           4 y2,b
                                               UCT(x′1 ) = 1.12 > UCT(x1 ) = 0.77

                                          ×                                          QED
                      backup: Q(x1 ) ← 0.40, n(x1 ) = 2
Figure 8: Deployed Monte Carlo Tree Search. Circled numbers indicate the chronological order of
node expansions; a budget of N = 4 expansions is exhausted in this run. Selection/Expansion: the
root is expanded twice, sampling y1 into x1 (step 1) and y2 into x′1 (step 2); each is evaluated once
via the policy’s own Levin score, giving V (x1 ) = 0.80 and V (x′1 ) = 0.60. With both children
visited once, UCT (exploration constant c = 0.5) scores x1 at 1.22 against x′1 at 1.02, so the search
commits to the higher-value child and expands it (step 3), reaching a dead end. Backup: the failure
backs up a value of 0 through x1 , dropping its running average to Q(x1 ) = 0.40. Selection reverses:
recomputing UCT with the updated statistics gives x′1 a score of 1.12 against x1 ’s now-diminished
0.77 – unlike Policy-Guided Best-First Search (Figure 4), where the frontier is re-ranked by a static
score, here it is the shrinking exploration bonus and the value drop from a real backup that overturn
the earlier choice. The search abandons x1 ’s subtree, expands x′1 (step 4), and reaches QED.




                                                                15
B    F ORMAL MDP F ORMULATION OF AUTOMATED T HEOREM P ROVING
We formalize the structure of LLM-guided theorem proving in interactive environments like Lean,
where text generation is strictly mediated by a formal verifier (the Lean kernel), as a Markov De-
cision Process (MDP) (Polu & Sutskever, 2020; Lample et al., 2022; Song et al., 2024). We define
this sequential decision-making process as a tuple M = ⟨X , Y, T , R, x0 ⟩:

    • State Space (X ): The discrete set of all valid Lean proof states. This space includes two
      terminal absorbing states: a universal success state xQED and a failure state xerr .
    • Action Space (Y): The space of possible tactics the LLM can generate.
    • Transition Function (T ): The deterministic update rules governed by the Lean kernel, de-
      fined as T : X × Y → X . Given a state xt−1 and tactic yt , T (xt−1 , yt ) = xt if the tactic
      is logically and syntactically valid. If yt is invalid, the kernel immediately rejects it, and
      T (xt−1 , yt ) = xerr . If yt completes the proof, T (xt−1 , yt ) = xQED .
    • Reward Function (R): A sparse terminal reward function mapping to {0, 1}. R(xt−1 , yt ) =
      1 if T (xt−1 , yt ) = xQED , and 0 otherwise.
    • Initial State (x0 ): The underlying theorem declaration to be proven.

The probability of executing any valid trajectory of length K, denoted τ = (x0 , y1 , x1 , . . . , yK , xK ),
is the product of the model’s autoregressive action probabilities:
                                                      K
                                                      Y
                                    Pπθ (τ | x0 ) =         πθ (yt | xt−1 )                             (17)
                                                      t=1


Let Γsucc (x0 ) denote the intractable set of all valid, successful trajectories originating from x0
and terminating in xQED . The true probability of proof discovery without search (Pass@1) is the
marginal likelihood over this entire set:
                                               X
                                  Pany :=              Pπθ (τ | x0 )                             (18)
                                              τ ∈Γsucc (x0 )

Because marginalizing over Γsucc (x0 ) is computationally impossible, standard SFT sidesteps this
global objective, reducing the objective to maximizing the likelihood of a single optimal trace τ ∗
via behavioral cloning, which yields the standard cross-entropy loss discussed in Section 2.




                                                      16
C      A PPROXIMATION E RROR AND S CALING
This appendix develops the approximation analysis for the search-aware objectives introduced in
Section 3. These objectives replace the deployed success probability J A with a trace-supported
proxy JbA . We study the resulting approximation through the per-tactic gradient weights, asking two
questions: (i) at a fixed budget, when is the search-aware weight closer to the deployed weight than
CE’s constant unit weight? (ii) how does this approximation error change as the test-time budget
grows? The search-agnostic UA objective is a separate budget-based construction, discussed in
Section J, and need not approximate the dynamics of a particular deployed search.
We study Pass@N (Section C.2) and the shared-budget retry model used for best-first search (Sec-
tion C.3). For Pass@N , the budget counts independent rollouts, allowing us to isolate the effect of
alternative successful trajectories omitted by the demonstrated trace. For the retry model, we ex-
amine how unsuccessful off-trace excursions consume a shared expansion budget. The latter results
rely on explicit assumptions about excursion costs and recovery, rather than providing a complete
characterization of deployed best-first search.
The analysis separates three effects:

      • Bypass channel. For Pass@N , under the proportional-reallocation convention and Assump-
        tion 1, the deployed weight is no larger than the trace-supported weight, which is no larger
        than CE’s unit weight (Theorem 4).
      • Trap channel. In a trap-only retry model with a common deterministic miss cost, excur-
        sions that return to the same trace state reduce the effective budget. The resulting weight lies
        between the retry-surrogate weight and CE’s unit weight (Proposition 3).
      • Budget scaling. In the models studied here, large-budget weight error vanishes for Pass@N
        and for recoverable shared-budget excursions. Permanent absorption can instead leave a
        nonzero error floor (Section C.4).

These results identify off-trace quantities that demonstrations alone do not determine. Incorporat-
ing them requires additional modeling assumptions or observations of search behavior. Section I
explores a simple use of such assumptions through priors on off-trace cost and recovery.

C.1     W ELL - POSED DEPLOYED WEIGHTS
The true objective depends on the entire policy, not only on the demonstrated probabilities p =
(p1 , . . . , pL ), so ”∂J/∂pt ” is meaningless until we fix how the remaining probability mass moves
when pt does. We adopt the assumption of proportional reallocation: at each demonstrated state,
write
                   πθ (y | xt−1 ) = pt 1{y = yt∗ } + (1 − pt ) ρt (y), ρt ∈ ∆ Y \ {yt∗ } ,
                                                                                        
                                                                                                 (19)
and define derivatives in pt holding ρt , all other ps , and all conditionals at non-demonstrated states
fixed. This is not explicitly true, tactics similar to the demonstrated tactic will gain probability mass
while distant ones will lose mass; however, this convention makes analysis feasible. This is strictly
a convention and not a statement about how changing the gradient redistributes mass to unobserved
tactics. All statements about the true weights below are relative to this convention. For any success
function J > 0 define the elasticity
                                                 ∂ log J    pt ∂J
                                     wt (J) :=            =       ,                                 (20)
                                                 ∂ log pt   J ∂pt
so that wt⋆ := wt (J A ) is the (unknown) deployed weight, w
                                                           bt := wt (JbA ) is the CAT weight of
Proposition 1, and CE corresponds to wtCE ≡ 1. Comparing training rules then reduces to a scalar
question at each step.
Proposition 2 (When is CAT closer than CE?). Suppose 0 ≤ w    bt < 1. Then wt⋆ − w
                                                                                 bt ≤ wt⋆ − 1
                ⋆   1
if and only if wt ≤ 2 (1 + w
                           bt ). If w
                                    bt = 1, CAT and CE coincide.

Proof. Square both sides, cancel (wt⋆ )2 , and divide by 1 − w
                                                             bt > 0.


                                                   17
Thus, CAT wins exactly when the deployed search makes the demonstrated tactic less critical than
single-shot generation assumes; CE can win only when the tactic remains a near single-shot bot-
tleneck under deployment. The next two subsections determine which side of the crossover each
strategy occupies.

C.2   PASS @N : UNIT ELASTICITY AND A ONE - SIDED SQUEEZE
             QL
Let a(p) = i=1 pi be the one-rollout probability of the demonstrated trace, b(p) the one-rollout
probability of proving the theorem by any other successful trajectory, and Pany = a + b.9 With
F (x) = 1 − (1 − x)N , the deployed objective is J true = F (Pany ) and the surrogate is Jb = F (a).
Define the elasticity of the outer function,
                                                          xF ′ (x)
                                               HF (x) =            .                                       (21)
                                                           F (x)

Lemma 1 (Properties of HF ). For F (x) = 1 − (1 − x)N and x ∈ (0, 1),
                                                             N
                                          HF (x) = PN −1                    ,                              (22)
                                                                       −j
                                                     j=0 (1 − x)

so HF is nonincreasing, HF (x) ≤ 1 with HF (0+ ) = 1, and for fixed x, HF (x) → 0 as N → ∞.

                PN −1
Proof. F (x) = x k=0 (1 − x)k and F ′ (x) = N (1 − x)N −1 ; divide and shift the index by N − 1.
Each summand (1 − x)−j ≥ 1 and is nondecreasing in x, giving the bound and monotonicity; the
sum diverges geometrically in N for fixed x, giving the limit.

Assumption 1 (At most one visit). Almost surely, every successful one-rollout trajectory visits each
demonstrated proof state xt−1 at most once. This holds automatically when states are history-
augmented (the search tree), which is the case in our setting.

Lemma 2 (Unit elasticity). Under Equation (19) and Assumption 1, partition the non-demonstrated
success mass at step t as b = bsh      sib     ∅
                                 t + bt + bt : trajectories that traverse the demonstrated transition
         ∗                ∗
(xt−1 , yt ) but are not τ ; trajectories that visit xt−1 and deviate there; and trajectories that never
visit xt−1 . Then
              ∂Pany                 pt                                                  pt ∂pt Pany
                    = a + bsh           bsib ≤ Pany ,
                              
         pt                t    −                                 i.e.          ηt :=               ≤ 1.   (23)
               ∂pt                1 − pt t                                                 Pany
No demonstrated tactic can move the total success probability excessively. (ηt may be negative when
sibling mass dominates.)

Proof. By Assumption 1 each successful trajectory contains the conditional at xt−1 at most once.
Under Equation (19) its probability is therefore of the form pt C, (1 − pt )ρt (y)C, or C with C free
of pt , according to which subset of b it belongs. Differentiate termwise and multiply by pt . The
inequality follows since the first term is at most Pany and the second is nonpositive.

Theorem 4 (Weight squeeze for Pass@N ). Under Assumption 1, for every step t and budget N ,

                  wt⋆ = ηt HF (Pany ) ≤ HF (Pany ) ≤ HF (a) = w
                                                              bt ≤ 1 = wtCE .                              (24)
Consequently |w bt − wt⋆ | ≤ |1 − wt⋆ |: CAT weakly dominates CE at every step and every budget,
with strict domination whenever any inequality is strict.

Proof. wt⋆ = HF (Pany ) ηt and w
                               bt = HF (a) · 1 by the chain rule and pt ∂pt a = a. Apply Lemma 2,
then a ≤ Pany with HF nonincreasing, then HF ≤ 1 (Lemma 1). Domination: wt⋆ ≤ w       bt ≤ 1 gives
wbt − wt⋆ ≤ 1 − wt⋆ .
   9
       Note that πproof in Section 3.1 equals a.


                                                     18
Error decomposition. The gap localizes into the two ways the surrogate is blind:
                 bt − wt⋆ = HF (a) − HF (Pany ) + (1 − ηt ) HF (Pany ) .
                                                
                w                                                                                   (25)
                           |        {z           }    |        {z        }
                                     ignored bypass mass       sharing / reallocation structure

The first term is the objective-level blindness to b; the second is present even at N = 1 and reflects
that raising pt proportionally starves sibling alternatives at xt−1 while riding along with shared-
prefix alternatives.

Remark. A useful strengthening is assuming b ≤ εa, the mean value theorem bounds the first term
of Equation (25) by εa supx∈[a,a+b] |HF′ (x)|, giving a quantitative guarantee. This assumption is in
a sense that the expert trace takes up a nontrivial chunk of the probability mass of correct proofs.

C.3     B EST- FIRST SEARCH : CENSORING AND EXCURSIONS
For BFS the surrogate is the retry objective of Equation (14),
                                                  L
                                                  X
            b ) = P(SL ≤ N ),
            J(N                           SL =          Tt ,   Tt ∼ Geom(pt ) independent.          (26)
                                                  t=1
Unlike Pass@N , a deployed miss does not cost exactly one budget unit. The search may wander
off-trace before the trace node is re-selected, or it may find a proof out there without returning. We
separate these two events, then approximate each.

C.3.1    T HE CAT WEIGHT IS A CRITICALITY
Lemma 3 (CAT weight as criticality). Let Tt′ be an independent copy of Tt and pi ∈ (0, 1). For
Equation (26),
                            P(SL + Tt′ ≤ N )
             wbt (N ) = 1 −                   = P(SL ≤ N < SL + Tt′ | SL ≤ N ) .            (27)
                               P(SL ≤ N )
Hence 0 ≤ wbt (N ) ≤ 1, w           bt (N ) → 0 as N → ∞, and w
                        bt (L) = 1, w                          bt (N ) is non-increasing in N .

Proof. For T ∼ Geom(p) and any bounded ψ, p ∂p E[ψ(T )] = E[ψ(T )] − E[ψ(T + T ′ )]. Apply
                                     P
with ψ(k) = P(Rt +k ≤ N ), Rt = i̸=t Ti , and divide by J(N  b ). For monotonicity: the pmf of SL
is a convolution of log-concave pmfs, hence log-concave, and so is its CDF F ; thus F (n − k)/F (n)
                                              bt (n) = ETt′ [F (n−Tt′ )/F (n)] is nondecreasing.
is nondecreasing in n for fixed k ≥ 1, and 1− w

C.3.2    S EPARATING ALTERNATIVE PROOFS : THE BYPASS CENSORED COUPLING
To analyze the impact of off-trace proofs on BFS, consider an artificial ”bypass censored process”.
This process behaves exactly like standard, deployed BFS. Except, if it ever samples a tactic which
would yield a proof other than the expert proof, we replace the observation of xQED by xerr . So it
only succeeds if it returns the demonstrated trace but it is allowed to be off path during the search.
Lemma 4 (Bypass Censoring). Let N be the initial budget, J trap (N ) be the censored process’
success probability and let β(N ) be the probability that the deployed run samples a transition which
would have been censored if we had instead run the censored process. Then
                          J trap (N ) ≤ J true (N ) ≤ J trap (N ) + β(N ).                       (28)

Proof. Couple the two runs on the same tactic draws and selector randomness. They are identical
until the deployed run first samples a transition which would have been censored: at that moment, the
deployed run has succeeded. If no censored transition is ever sampled, outcomes agree. So censored
success implies deployed success, and deployed success implies censored success or divergence.

This is just to say that alternate proof paths can only add success. To use this to analyze the weights,
split the true success probability by which event occurs first, J true = J † + B (J † : completion of the
demonstrated trace; B: completion of an alternate trace). From looking at the sum of elasticities,
                                         ∂J true   ∂J †   ∂B
                                                 =      +
                                          ∂pt      ∂pt    ∂pt

                                                      19
                                           pt ∂J †      pt ∂B
                                   wt⋆ = true       + true
                                         J     ∂pt    J      ∂pt
                               †              †
                                                                    
                          ⋆       J       p t ∂J          B       pt ∂B
                         wt =                       +
                                J true    J † ∂pt       J true    B ∂pt
                                                                     J†
                         wt⋆ = λ wt J † + (1 − λ) wt (B),
                                       
                                                               λ = true ,                           (29)
                                                                    J
holds exactly.
This mixture identity reveals that the true weight is subject to a tug-of-war between two competing
”channels” of success.
First, the trap channel (J † ) captures trajectories that wander into dead ends but eventually return
to complete the demonstrated proof. Because these off-trace excursions consume a shared compute
budget, they increase the bottleneck on the remaining path. This increased criticality pushes the
weight wt (J † ) up relative to the trace-supported surrogate w
                                                              bt (formalized in Proposition 3).
Conversely, the bypass channel (B) captures trajectories that successfully discover alternative, un-
observed proofs. The existence of these alternative solutions makes the exact demonstrated tactic
less critical for global success, which pushes the weight down, mirroring the elasticity squeeze ob-
served in the Pass@N analysis. Thus, we will focus the remaining analysis on the effect of the trap
channel.
One structural caveat remains: the true BFS selector’s geometric-mean scores dynamically depend
on p, a dependence the trace-supported surrogate erases to maintain independence between steps.
Because Levin scores are cumulative, increasing an early on-trace probability ps creates a cascading
advantage for all subsequent trace nodes. This allows the trace to win frontier comparisons sooner,
actively suppressing the length of future off-trace excursions. This positive feedback loop means the
true search penalizes on-trace mistakes even more heavily than our surrogate models. Consequently,
the trap channel’s upward pressure on the deployed weight wt⋆ is strictly stronger in reality. We will,
however, treat the mixture identity (Equation (29)) as exact.

C.3.3    T HE T RAP C HANNEL : E XPLORATION WASTE AND S HARED -B UDGET B RACKETING
In the trap channel, when BFS samples an off-trace tactic at state xt−1 , the algorithm embarks on an
off-trace excursion until it returns back to the trace. To quantify the computational toll of deviations,
let Et,j ∈ {0, 1, . . .} ∪ {∞} denote the number of wasted node expansions spent off-trace following
the j-th miss at state xt−1 before the search backtracks and re-selects the trace node (Et,j = ∞
if the algorithm is permanently absorbed). The trap-channel success probability is then precisely
represented by:                                                           
                                             L
                                             X          XL TXt −1

                            J trap (N ) = P    Tt +              Et,j ≤ N  ,                       (30)
                                           t=1          t=1 j=1

where Tt ∼ Geom(pt ) tracks on-trace trials. Different choices of weight during training can be
viewed as distinct assumptions on E:

    • Minimal waste (E ≡ 0): Every off-trace tactic is instantly rejected by the environment (xerr ).
      A miss costs exactly 1 expansion, recovering our CAT retry surrogate exactly (J trap (N ) =
      J(N
      b )).

    • Permanent absorption (E ≡ ∞): Any off-trace mistake traps the search indefinitely. Here,
                   QL
      J trap (N ) = t=1 pt for any budget N ≥ L, yielding unit elasticity (wt⋆ = 1), recovering the
      exact regime where standard SFT weighting is optimal.

Between these two extremes lies the realistic setting where off-trace excursions consume finite, non-
zero compute before backtracking. To isolate how this exploration waste alters the true weight, we
first examine the case of a fixed return cost.
Assumption 2 (Deterministic excursion cost). In the trap-channel process, every miss incurs a total
expenditure of κ ≥ 1 expansions (the initial trial plus an excursion of length E ≡ κ − 1) before
returning the search to xt−1 ; successful trials cost 1 expansion; κ is independent of the policy
probabilities p.


                                                   20
Proposition 3 (Shared-budget bracketing). Under Assumption 2, let N ≥ L be an integer budget
and ps ∈ (0, 1) for all s. Completing the demonstrated path in the bypass-censored process within
budget N is equivalent to evaluating the retry surrogate at a reduced effective budget:
                                                                  N −L
                        J trap (N ) = J(N
                                      b eff ),       Neff = L +        ≤ N.                          (31)
                                                                    κ
For noninteger budget arguments B, interpret J(B)
                                             b    = J(⌊B⌋)
                                                    b      and w
                                                               bt (B) = w
                                                                        bt (⌊B⌋).
Define the trap-channel weight by wttrap (N ) := wt (J trap (N )). Because κ is independent of p, the
effective-budget identity and Lemma 3 give

                            bt (N ) ≤ wttrap (N ) = w
                            w                       bt (Neff ) ≤ 1 = wtCE .                          (32)

Proof. Completing step t requires Gt ∼ Geom(pt ) trials costing κ(Gt − 1) + 1 total expansions.
Summing over the trace yields a total cost κSL − (κ − 1)L ≤ N ⇐⇒ SL ≤ Neff . The bracket
directly follows since Neff ≤ N for κ ≥ 1 and w
                                              bt (·) is non-increasing.

In real policy-guided Best-First Search, excursions do not incur deterministic costs; rather, they
exhibit stochastic, bounded trajectories (E ≤ κ̄ − 1 a.s.). Crucially, we can actively engineer this
bound during deployment to prevent permanent absorption.

Enforcing Bounded Excursions via Global Search Restarts. In practical ATP deployments,
we actively prevent policies from being trapped in cyclical or deep, unguided proof attempts
(P (E = ∞) = 0) by deploying a restart-based Best-First Search heuristic. Specifically, if the
global BFS does not discover a complete proof within a step threshold of M < N total node expan-
sions, the active search tree is aborted and the algorithm resets entirely to the initial theorem state x0
to begin a fresh run with the remaining compute budget. However, the cost to setting such an M too
low is aborting a possibly prominent path so in practice this M is fairly high. This restart mechanism
guarantees that no single exploratory trajectory can waste more than M expansions off-trace. Con-
sequently, the exploration waste incurred before re-attempting the demonstrated trajectory is strictly
bounded (E ≤ M a.s., enforcing a maximum excursion severity κ̄ ≤ M + 1). While enforcing this
test-time constraint eliminates the SFT ceiling (wt⋆ < 1), combining it with Proposition 3 reveals an
irreducible tension between trace-only supervision and search optimization.

Proposition 4 (Irreducible Ambiguity under Bounded Excursions). Call a per-step weighting rule
trace-supported if it depends solely on training-time observables along τ ∗ (specifically, the demon-
strated probabilities {ps }L
                           s=1 , the search strategy A, and the initial budget N ). Suppose test-time
search engineering enforces an upper bound on excursion waste such that κ ∈ [1, κ̄] for a finite limit
κ̄ > 1. Then:

  (i) The true deployed weight wt⋆ is strictly confined to the compressed bracket:
                                                                  
                                   ⋆                          N −L
                                wt ∈ w     bt (N ), w
                                                    bt L +             .                             (33)
                                                                 κ̄

  (ii) Because the realized excursion waste κ depends on unobserved off-trace dynamics, no trace-
       supported objective can uniquely identify wt⋆ . Any trace-supported rule wt incurs a worst-
       case approximation error bounded below by half the bracket width:
                                                                            
                                              1              N −L
                   sup wt − wt⋆ (κ; N ) ≥         wbt L +            −w bt (N ) > 0.         (34)
                  κ∈[1,κ̄]                    2                κ̄

Proof. By Proposition 3, an environment with effective excursion cost κ realizes the deployed
weight wt⋆ = w bt (L + N κ−L ). Because environments with κ = 1 (instant syntax error) and κ = κ̄
(maximum restart cap M ) yield identical training-time observables along τ ∗ , any trace-supported
rule must output the same scalar wt across both environments. The minimax lower bound follows
directly from applying the triangle inequality to the interval endpoints.


                                                   21
C.4   B UDGET SCALING OF THE WEIGHT ERROR : HUMP OR FLOOR
Using the understanding we’ve built, we can understand how the error in our approximation scales.
A key intuition we will need is that the surrogate’s weight error is generally not monotone in N .
When N is minimal (N = 1 in our setting), we are just performing a single rollout. We aren’t
really performing search, and both the surrogate and real weights understand this, so the error of the
surrogate is 0. Conversely, as N → ∞, our probability of success (with some caveats) becomes 1.
Thus, both the surrogate and deployed weights tend to 0. The error only really occurs in the middle
between these two extremes.

The minimal-budget endpoint is universal. At the smallest budget that can possibly succeed,
any strategy must execute τ ∗ with no misses: both J A (trap channel) and JbA equal t pt , whose
                                                                                      Q
                                  bt = wt⋆ = 1 = wtCE and all three rules coincide (alternate proofs
elasticity is 1 at every step. So w
shorter than L are the only exception, entering through B in Equation (29)).
Proposition 5 (Pass@N : vanishing error). Fix the policy with a ∈ (0, 1). Then w       bt (1) = 1 and
wt⋆ (1) = ηt ; both w
                    bt (N ) and wt⋆ (N ) tend to 0 as N → ∞; the bypass term of Equation (25) is zero
at N = 1 and vanishes as N → ∞ (a hump), while the reallocation term decays monotonically
from 1 − ηt . In particular, the CAT error tends to 0 while the CE error |1 − wt⋆ | tends to 1.

Proof. At N = 1, HF ≡ 1. As N → ∞, HF (x) → 0 for fixed x > 0 (Lemma 1); apply to x = a
and x = Pany in Theorem 4 and Equation (25).

For BFS, the outcome depends on the excursions. We isolate it to a specific case.
Assumption 3 (Absorbing-excursion model). In the trap-only censored process, each miss at step
t, independently of everything else, launches a non-returning excursion (E = ∞) with probability
qt ∈ [0, 1], and otherwise an excursion of bounded length E ≤ κ̄ − 1.
Proposition 6 (Hump or floor). Under Assumption 3:

  (a) (Recurrence ⇒ hump.) If qt = 0 for all t and excursions are deterministic (E ≡ κ − 1), the
      trap-channel error is wt⋆ (N ) − w         bt (Neff ) − w
                                       bt (N ) = w            bt (N ) ≥ 0, which is 0 at N = L, tends
      to 0 as N → ∞ (since Neff → ∞), and is positive in between whenever κ > 1: the error
      is humped. For bounded random excursions with no absorption, the error is likewise zero at
      N = L and vanishes as N → ∞; its finite-budget behavior is governed by Equation (30).
  (b) (Absorption ⇒ floor.) If qt > 0, then as N → ∞,
                             L
                             Y          pt                                       qt
           J trap (N ) −→                          ,        wt⋆ (N ) −→                    > 0,      (35)
                             t=1
                                 p t + (1 − pt )qt                        pt + (1 − pt )qt

      while wbt (N ) → 0: the CAT error converges to the strictly positive floor (35). As qt → 1,
      the floor tends to 1 and CE becomes asymptotically exact at step t, recovering the permanent-
      absorption limit; as qt → 0, the limiting error at that step vanishes.

Proof. (a) is Proposition 3 plus Lemma 3. (b) With unlimited budget, finite excursions are free, so
step t succeeds iff yt∗ is sampled before an absorbing excursion: per trial, advance w.p. pt , absorb
w.p. (1 − pt )qt , retry otherwise, giving per-step success f (pt ) = pt /(pt + (1 − pt )qt ), independent
across steps. Direct computation gives ∂ log f /∂ log p = q/(p + (1 − p)q). The interchange             of
limit and derivative is justified within the model by monotone convergence of J trap (N ) ↑ t f (pt )
                                                                                                  Q
together with monotonicity of wt⋆ (N ) inherited from Lemma 3 applied at the extended-cost repre-
sentation.

Approximation is Incorrect Asymptotically, but Weights Converge. The pieces we don’t ac-
count for in our surrogate (the alternate proof mass β(N ) and total excursion expansions) do grow
with N . But their effect on the weights is self-limiting. Both objectives saturate near 1, and ev-
ery elasticity is near 0, so no weighting rule can be far from the truth. This is a key advantage of
test-time aligned training.


                                                       22
D     D EPTH F IRST S EARCH VARIANTS
Depth First Search (DFS) is not a standard algorithm used in policy guided search. We introduce it
in this context because analyzing it and its variants serve as excellent examples about the mechanics
of constructing search aligned loss functions.

D.1    S TANDARD DFS
Standard DFS utilizes its computational budget to sequentially construct a single path. When the
algorithm expands a node xt−1 and the tactic is rejected (T (xt−1 , yt ) = xerr ), the search does not
abandon the entire trajectory. Instead, the decision rule dictates a retreat of exactly one step to the
immediate parent state xt−1 , expending another unit of compute to sample an alternative tactic. This
localized trial-and-error continues until the algorithm either successfully reaches xQED or exhausts
the global node expansion budget N .
Finally, we note that because standard DFS commits rigidly to a valid path, its chronologically local
backtracking is a structural weakness. If the search ventures into a deep, valid, but useless branch,
the localized backtracking cannot escape the broader strategic error. The LLM will simply exhaust
its entire computational budget trapped in the depths of a spurious path.

Instantiation. Define bc = ⟨x, b⟩, where x is the active trace state and b is the remaining node
expansion budget. The trace-supported frontier is always a singleton, Fb = {x}.
The positive update advances the path and consumes one expansion. For the negative update, an off-
trace tactic immediately collapses the search back to the parent xt−1 at the cost of one expansion.
Thus, the updates are:
                Ub + (xt−1 , b) = (xt , b − 1),    Ub − (xt−1 , b) = (xt−1 , b − 1)
                   DFS                                   DFS
Because the frontier is always a single node, the selector is trivial: SDFS (x | b
                                                                                 c) = 1. Consequently,
the trace-supported recurrence for DFS perfectly mirrors the recurrence for BFS (Equation (13)):
                   JbDFS (b, t) = pt JbDFS (b − 1, t + 1) + (1 − pt )JbDFS (b − 1, t).
Thus, the closed form loss will collapse to that which we derived for BFS.

D.2    R ANDOMIZED D EPTH -F IRST S EARCH (RDFS)
To mitigate the vulnerability of DFS to spurious paths, we introduce a randomized variant. RDFS
disrupts this failure mode by altering the backtracking target. When the policy πθ reaches a dead
end, the algorithm does not simply return to xt−1 . Instead, it selects a state uniformly at random
from the entire active path prefix (x0 , x1 , . . . , xt−1 ) and resumes expansion from there. This allows
the search to stochastically jump out of deep traps, efficiently reallocating compute to higher-level
branching points while preserving the depth-seeking advantages of the standard algorithm. A visu-
alization is given in Figure 6.

Instantiation. Let b c = ⟨t, b⟩, with the frontier tracking the full active path Fb = {1, 2, . . . , t}. To
incorporate randomized backtracking, the randomness is injected directly into the selector. When a
dead end is reached, rather than the update rule deterministically collapsing the path, the negative
update triggers the selector to sample a state uniformly at random from the entire available frontier
F.
 b

Trace-supported recurrence. Because of this randomized selector, the compute consumed at
depth t cannot be modeled as a simple sequence of independent geometric random variables. In-
stead, the trace-supported objective forms a dynamic program.
Let JbRDFS (b, t) denote the exact probability of discovering the complete proof given that the search
is currently evaluating the trace state at index t with a remaining budget b. The boundary conditions
are:
                JbRDFS (b, L + 1) = 1 for all b ≥ 0 (Proof successfully completed)                (36)
                     JbRDFS (0, t) = 0 for all t ≤ L (Compute budget exhausted)                   (37)


                                                    23
For b > 0 and t ≤ L, the recurrence relation resolving Equation (5) branches into two outcomes.
With probability pt , the model generates the correct tactic and advances. With probability (1 − pt ),
the model fails, and the selector backtracks uniformly to any valid ancestor index k ∈ {1, . . . , t}.
Thus, the recurrence becomes:
                                                                    t
                                                                  1X b
             JbRDFS (b, t) = pt JbRDFS (b − 1, t + 1) + (1 − pt )     JRDFS (b − 1, k)          (38)
                                                                  t
                                                                    k=1

Unlike Pass@N or BFS, this objective does not reduce to a standard closed-form probability distri-
bution.

D.3   VALUE G UIDED D EPTH -F IRST S EARCH (VDFS)
To mitigate the vulnerability of DFS while leveraging the policy’s own internal confidence, we in-
troduce Value Guided DFS (VDFS). Unlike RDFS, which backtracks uniformly, VDFS makes an
informed retreat. When the search reaches a dead end, it backtracks to an ancestor state in the active
path prefix with probability proportional to that state’s Levin score (from Equation (12)). By using
the geometric mean of the policy’s probabilities as a confidence metric, the search preferentially
returns to the most promising points on the current path. This concentrates the remaining compu-
tational budget on states the policy deems most reliable, while maintaining enough stochasticity to
escape deep, spurious branches. A visualizaiton can be seen in Figure 7.

Instantiation. Let b   c = ⟨t, b⟩, where t is the active trace index (corresponding to the state xt−1 ),
and b is the remaining node expansion budget. The trace-supported frontier tracks the full active
path prefix of states: Fb = {x0 , x1 , . . . , xt−1 }.
To compute the backtrack distribution, we evaluate the Levin score for each state on the frontier. Let
sk denote the Levin score of state xk . For the root, s0 = 1. For k ≥ 1, the score is the geometric
mean of the on-trace probabilities leading to that state:
                                                          k1
                                                  Y k
                                         sk =         pj                                        (39)
                                                   j=1


The positive update advances the proof by one step: U b + (t, b) = (t + 1, b − 1). For the negative
                                                       VDFS
update, an off-trace tactic consumes a unit of budget and triggers a backtrack. The selector samples
a backtrack target state xk ∈ Fb with probability proportional to its score sk . Transitioning to xk
sets the new active trace index to k + 1. Thus, the negative update maps stochastically:
                   b − (t, b) = (k + 1, b − 1), where k ∼ P (k) = P sk
                   U                                                                            (40)
                     VDFS                                                   t−1
                                                                            i=0 si

Trace-supported recurrence. Let JbVDFS (b, t) denote the exact probability of discovering the
complete proof from the trace state at index t with remaining budget b. The boundary conditions are
identical to RDFS:
               JbVDFS (b, L + 1) = 1 for all b ≥ 0 (Proof successfully completed)             (41)
                   JbVDFS (0, t) = 0 for all t ≤ L (Compute budget exhausted)                 (42)
For b > 0 and t ≤ L, the recurrence resolving Equation (5) weights the backtrack sum by the Levin
scores. With probability pt , the model generates the correct tactic and advances. With probability
(1 − pt ), the model fails, and the selector backtracks to state xk (k ∈ {0, . . . , t − 1}) according to
the score distribution. The recurrence becomes:
                                                           t−1
                                                           X      sk
      JbVDFS (b, t) = pt JbVDFS (b − 1, t + 1) + (1 − pt )     Pt−1 JbVDFS (b − 1, k + 1)            (43)
                                                           k=0   i=0 si

Like RDFS, this objective doesn’t have a closed form. Notably, the gradients flow not only through
the direct local transitions but also through the Levin scores sk , which are themselves functions
of the policy probabilities. This couples the training objective, forcing the model to calibrate its
on-path probabilities to optimize the resulting backtracking distribution.


                                                   24
E    M ONTE C ARLO T REE S EARCH (MCTS)
The strategies considered so far commit their budget by a rule fixed in advance: DFS always retries
the deepest node, RDFS backtracks uniformly, and VDFS backtracks in proportion to a static per-
node score. Monte Carlo Tree Search (Kocsis & Szepesvári, 2006; Coulom, 2006) instead allocates
compute according to statistics it accumulates as the search runs. We include it because it is the
only strategy in our taxonomy whose selector depends on the history of the search rather than on the
current configuration alone, and it therefore tests our construction at its least convenient.
MCTS is a 4-phase process at deployment. At each node, Selection either commits to its most
promising child or stops to gain more information about another tactic at the current node. The
choice to widen is governed
                       √         by a progressive-widening schedule: a node that has been visited n
times is permitted ⌈ n + 1⌉ distinct tactic samples (Coulom, 2007). Expansion samples one tactic
from πθ at the selected node and submits it to the kernel, consuming one node expansion. Evaluation
assigns the resulting state a value; in the variant, we choose to use the policy’s own Levin score
Equation (12) rather than a learned critic, so that MCTS requires no component the other strategies
don’t utilize. Backup propagates that value to every ancestor on the selected path, updating the
statistics that drive future selections. A visualization is given in Figure 8.

Instantiation.    With abuse of notation, let a configuration be
                                     c =
                                     b       (nk , mk , Wk )L−1
                                                            k=0 , b ,

where nk is the visit count of the state xk , mk the number of tactics already sampled there, Wk the
accumulated backed-up value, and b the remaining expansion budget. The trace-supported frontier
is the prefix {x0 , . . . , xL−1 }. The selector is not stochastic: the descent stops at the shallowest node
that is either allowed a new tactic by the widening schedule or has no child yet,
                                    n             √                                     o
                  d(b c) = min k : mk <              nk + 1 or xk+1 not yet reached ,
                                                                                                         (44)
                               SbMCTS (xk | b
                                            c) = 1{k = d(b   c)}.
The updates apply the expansion and the backup together. Writing d = d(b  c), a demonstrated tactic
advances the trace and backs up the value V (xd+1 ) of the state it reaches, while a miss backs up
zero:
           b+
           U                               nk += 1, Wk += V (xd+1 ) ∀k ≤ d,             b −= 1,
            MCTS (b
                  c) :      md += 1,                                                                    (45)
           b−
           U     (b
                  c) :      md += 1,       nk += 1, Wk += 0 ∀k ≤ d,            b −= 1,                  (46)
             MCTS

with solved configurations (for the trace supported version) those in which depth L has been reached
and dead configurations those with b = 0. Both updates decrement the budget, so the recurrence
terminates.
For BFS, the naive selector is degenerate on a demonstrated trace because a chain never offers two
frontier candidates at once. The same erasure happens here, in a slightly different place. The UCT
rule ranks the children of a node by an exploration-adjusted value estimate, but under the trace
transition Equation (4) every node has at most one child, so there is never a comparison for it to
make. What survives is only the widening schedule in Equation (44): the rule that decides how
many tactic samples a node receives before the search commits to descending. Thus in practice, this
strategy trains like a local Pass@N at each node.




                                                     25
F   S TRATEGY M ATCHING W ITHIN THE S EARCH -AWARE FAMILY
The main comparison evaluates search-aware CAT and search-agnostic UA across deployed strate-
gies. Here, we isolate a different question: within the search-aware family, does matching the
training objective to the deployed strategy improve proof success? Using the fixed-budget setup
of Section 5.1, we evaluate the Pass@N and BFS search-aware adapters under both deployment
strategies, with CE as a reference.

Table 3: Strategy matching within the search-aware family. Proof-success rates (%) at N = 256
tactic expansions. Columns are deployed strategies; rows are training objectives. Bold marks the
higher point estimate among the two search-aware objectives in each column.

                          Training objective           Pass@N     BFS
                          CE                             21.2     23.8
                          Search-aware CAT (Pass@N )     26.6     24.5
                          Search-aware CAT (BFS)         23.7     25.1

The matched objective has the higher observed success rate under each deployment strategy. This
supports strategy matching within the tested search-aware pair, complementing the comparison with
shared UA in Table 1.




                                               26
G     E XPERIMENTAL D ETAILS

G.1   C OMMON SETUP

Environment. All experiments run against Lean 4 through LeanDojo 4.20.0 (Yang et al., 2023).
The policy is prompted with the pretty-printed proof state and emits a single tactic, which is submit-
ted to the Lean kernel; the kernel verdict determines the transition. One node expansion denotes one
policy sample together with its kernel verification, and is the unit in which all budgets are expressed.
Kernel interaction is serial within a theorem, so wall-clock cost per unsolved theorem grows linearly
in the budget.

Data. Training and evaluation both draw on cat-searcher/leandojo-benchmark-4-
random, a random split of mathlib4 (The mathlib Community, 2020). The alignment stage con-
sumes 40,660 traced proofs comprising 76,003 (state, tactic) training examples. The evaluation pool
is the 458 held-out theorems whose reference proofs contain between 2 and 5 tactic steps; there is
no overlap between training and evaluation theorems. Reference proofs are used only to compute
training weights and to define the pool. At evaluation, a theorem counts as solved if the search
returns any kernel-verified proof, whether or not it matches the reference.

Model and adapters. The policy is Qwen2.5-Math-7B-Instruct (Qwen Team, 2024) in bfloat16.
All fine-tuning uses LoRA (Hu et al., 2021) with rank r = 16, α = 32, dropout 0.05, applied to the
query, key, value, output, gate, up, and down projections. This trains 40,370,176 of 7,655,986,688
parameters (0.53%). Gradient checkpointing is enabled throughout. All runs use a single NVIDIA
A100-40GB. Training runs used FlashAttention-2 (Dao, 2024).

G.2   T RAINING PROCEDURE AND HYPERPARAMETERS

Stage 1: Warm-up. A single supervised checkpoint is the common ancestor of every model we
report. The first set of experiments branch off of two warm up epochs of SFT; while the second set
branch off of only one. This discrepancy is a result of human error; however, given that runs are not
compared cross-experiment, we find it reasonable to keep.

Stage 2: Alignment. From the warm-up checkpoint the runs branch. The control receives one
further epoch of standard cross-entropy SFT. Each aligned model receives one further epoch over
the same examples in the same order under the same optimizer settings, with the only difference
                        btA applied to each tactic’s cross-entropy gradient. An alignment epoch is
being the scalar weight w
19,001 optimizer steps and takes approximately 2.4 h.

      Table 4: Optimization hyperparameters, identical for the control and every aligned run.

                   Optimizer                   AdamW
                   Learning rate               1 × 10−4
                   Schedule                    linear decay, warm-up over 5% of steps
                   Micro-batch size            4
                   Gradient accumulation       16
                   Effective batch size        64
                   Gradient clipping           1.0 (global ℓ2 norm)
                   Maximum sequence length     512 tokens
                   Precision                   bfloat16 with autocast
                   Alignment epochs            1 (on top of the shared warm-up)
                   Random seed                 42


Non-finite losses are skipped without an optimizer step; this occurs rarely and is logged. Examples
exceeding the maximum sequence length are dropped at dataset construction rather than truncated,
so no partially-supervised tactic enters training. The closed-form weights are evaluated directly
in log space for numerical stability. The weights defined by a dynamic program are obtained by
autodiff.


                                                  27
G.3   I NFERENCE AND EVALUATION

Serving. Generation uses vLLM 0.6.3 with the LoRA adapter supplied per request, GPU memory
fraction 0.85, and maximum model length 4096 tokens. Sampling temperature is 0.8. The evaluation
seed (42) fixes both the shuffle of the theorem pool and the sampling stream, so every configuration
sees the identical theorems in the identical order; this is what licenses the paired analysis below and
what makes a truncated cell a well-defined prefix of the full pool.

                     Table 5: Search parameters. Budgets are node expansions.

                     Parameter                     Experiment 1   Experiment 2
                     Budget N                      256            16, 64, 256, 1024
                     Best-first beam width         2              2
                     Expansions per pop            4              4
                     Best-first score exponent α   0.5            0.5
                     Pass@N generation batch       16             64
                     Maximum proof depth           5              5
                     Per-strategy wall-clock cap   90 s           none
                     Per-theorem wall-clock cap    500 s          none



Scoring and truncation. A theorem is scored as solved only if a kernel-verified proof is returned
within the budget; unsolved-within-budget counts as a failure, with no exclusion. The two exper-
iments differ in one respect that we record explicitly. Experiment 1 imposes the wall-clock caps
in Table 5, so a theorem may in principle be cut off before its expansion budget is exhausted; Ex-
periment 2 disables them, guaranteeing that every theorem spends its full budget. The caps are the
reason the two experiments’ absolute rates are not directly comparable, and they were removed for
Experiment 2 because the effect grows with the budget: a wall-clock cap binds far more often at
N = 1024 than at N = 64 and would otherwise have depressed exactly the high-budget cells whose
behavior the experiment is about.

Statistics. Because all configurations are evaluated on the same theorems in the same order, every
comparison is paired. For two configurations we report b, the number of theorems solved by the
second and not the first, and c, the number solved by the first and not the second, on the subset n that
both evaluated. The reported difference is (b − c)/n; its 95% interval uses the McNemar variance
Var[(b−c)/n] = (b+c)/n2 ; and the reported p-value is the exact two-sided McNemar (sign) test on
the b + c discordant pairs. We use the paired difference rather than the difference of marginal rates
throughout, because the two diverge whenever the cells being compared cover different numbers
of theorems, and only the paired quantity is consistent with the interval and the p-value beside it.
Where a figure shows unpaired intervals on individual rates (Figure 1) this is stated in the caption;
those intervals are wider than the paired ones and overlapping bars do not indicate a non-significant
difference.

G.4   E XPERIMENT 1: FIXED - BUDGET COMPARISON

Configurations. Six deployed strategies at N = 256: Pass@N and best-first search from Sec-
tion 3, and DFS, RDFS, VDFS and MCTS from Section D. Each is paired with the CAT weight
derived for it (same for BFS/DFS), and we additionally deploy the single shared UA adapter under
every strategy.

Control. The control for this experiment is the epoch-matched model: warm-up plus one addi-
tional epoch of standard SFT. Control and aligned models therefore receive identical total optimiza-
tion, and the comparison isolates the loss weighting.

G.5   E XPERIMENT 2: BUDGET SWEEP

Budget-matched adapters. We train a separate adapter per evaluation budget with the weight’s
budget parameter set to the deployment value, and evaluate each at its own budget only.


                                                   28
Control. The control for this experiment is the shared warm-up checkpoint, with an additional
SFT epoch.

Pools. The N ∈ {16, 64, 256, 1024} are evaluated on the full 458-theorem pool. However, we
only allowed 80 GPU hours so not all evaluations were fully completed.

Reproduction. Given the trained adapters, each cell is one invocation of the evaluation harness
with the strategy, budget, and adapter path. Cells write one JSON log per strategy keyed by theorem
name, and all tables and figures in this paper are generated directly from those logs.




                                                29
H    H IGH -B UDGET E VALUATION
To complement Section 5.2, we also evaluated budget-matched CAT adapters at N = 1024 under
Pass@N and BFS, using the same training and evaluation protocol. The evaluation-time limit re-
stricted the paired comparisons to 57 theorems for Pass@N and 56 for BFS. Table 6 reports these
results, and Figure 9 shows the complete budget sweep.

Table 6: Compute-limited evaluation at N = 1024 node expansions. n is the paired subset size,
b counts CAT-only successes, and c counts control-only successes. Gains and 95% intervals are in
percentage points. Intervals and exact two-sided McNemar tests follow Table 2.

                 Strategy   Budget N    n    b/c    Gain (pp), 95% interval    p
                 Pass@N     1024        57   6/1      +8.8 [−0.3, 17.9]       0.125
                 BFS        1024        56   5/2      +5.4 [−3.9, 14.6]       0.453




Figure 9: Complete budget sweep, including the compute-limited N = 1024 evaluation. Error
bars show 95% intervals; filled markers denote p < 0.05 and hollow markers denote p ≥ 0.05.
Dashed segments connect to the N = 1024 estimates, annotated with their paired subset sizes. The
completed subsets differ across budgets, so connecting lines are descriptive rather than a common-
cohort comparison.


Interpretation. Both high-budget point estimates favor CAT, but each comparison is based on
only seven discordant theorem pairs, and both reported 95% intervals include zero. These results
are therefore inconclusive about the magnitude of the alignment benefit at N = 1024 and do not
establish a trend from N = 256 to N = 1024. We report them for completeness rather than using
them as evidence of increasing alignment gains at large budgets.




                                               30
I     P RIORS ON O FF -T RACE B EHAVIOUR
In Section C, we characterized the gap between our trace-supported surrogate and the deployed
search. However, we haven’t deeply explored if we can use this to meaningfully improve training.
We implied that placing priors on off-trace seems like a reasonable way to utilize this observation.
We use this section to take a brief step in that direction and see if a simple prior on loss can be
beneficial.

I.1    A TWO - PARAMETER PRIOR
Proposition 3 and Proposition 6 show that off-trace behaviour enters the objective through two
scalars:

      • κ ≥ 1, the expected number of expansions a miss consumes, counting the off-trace excursion
        before the search returns to the trace;
      • q ∈ [0, 1), the probability that a miss launches an excursion that never returns.

Both enter mechanically and in a strategy-independent way. Proposition 3 states that a deployment
in which a miss costs κ expansions realises the surrogate at the deflated budget
                                                      N −L
                                      Neff = L +           ≤ N,                                  (47)
                                                        κ
so κ is applied by evaluating the strategy’s own objective at, Neff in place of N . Absorption enters
the trace-supported recurrence Equation (5) by splitting the miss branch: with probability (1 − pt )q
the search is absorbed and contributes nothing, and with probability (1 − pt )(1 − q) it continues
as the uncorrected recurrence prescribes. Every occurrence of (1 − pt ) on a continuation branch is
therefore replaced by (1 − pt )(1 − q), with the missing mass leaking to a terminal failure state.
Note that a better prior can make assumptions on κ and q as functions of p or prior probabilities, but
we are merely going to test the simple case.

I.2    A PPLYING THE PRIOR TO EACH STRATEGY
The prior is applied to the objective the surrogate implies for each strategy.

Best-first search. The trace-supported objective for BFS is the retry recurrence Equation (13).
The prior is applied directly to that recurrence,

                 Jbκ,q (b, t) = pt Jbκ,q (b − 1, t + 1) + (1 − pt )(1 − q) Jbκ,q (b − 1, t),     (48)

with Jbκ,q (b, L) = 1, Jbκ,q (0, t) = 0, run to b = Neff = L + (N − L)/κ.

RDFS and VDFS. The same substitution applies to the dynamic programs of Section D: the bud-
get axis runs to Neff and the backtrack branch carries the factor (1 − q), leaving the uniform and
value-weighted backtrack kernels otherwise unchanged.

MCTS. Similarly, we just readjust the dynamic program in essentially the same fashion as the
other search strategies.

I.3    S ETUP
The prior is set by hand. The primary setting is κ = 5, q = 0.02; under BFS we additionally
train κ = 3, q = 0 to probe sensitivity. Everything else matches Section 5.1: the same warm-up
checkpoint, one alignment epoch over the same examples in the same order under the same optimiser
settings, a budget of N = 256 node expansions, and the full 458-theorem pool. The only difference
between a prior-corrected adapter and its uncorrected counterpart is the scalar weight applied to
each tactic’s cross-entropy gradient. Each adapter is deployed under the strategy whose objective it
corrects.


                                                     31
Table 7: The off-trace prior applied to each strategy’s own CAT objective (proofs found, %, N =256
node expansions, 458 theorems). “CAT” is the uncorrected weight of Sections 3 and D, i.e. the
(κ, q) = (1, 0) member of the family.

                          Strategy   Prior            SFT    CAT    +prior
                                     κ=5, q=0.02      23.8   25.1    25.8
                          BFS
                                     κ=3, q=0         23.8   25.1    25.1
                          RDFS       κ=5, q=0.02      20.7   23.6    22.7
                          VDFS       κ=5, q=0.02      21.2   23.8    24.2
                          MCTS       κ=5, q=0.02      20.3   22.5    22.9


I.4   R ESULTS
Table 7 reports the strategies for which the prior was applied. Generally, the priors edged out the
basic CAT weights but not by a significant amount in any case. The conclusion we take from this is
that perhaps with optimal tuning of the prior, we can get increased gains, but the value is marginal.




                                                 32
J   S EARCH -AGNOSTIC U NIFORM -A LLOCATION O BJECTIVE : A DDITIONAL
    D ETAILS
This appendix supplements the search-agnostic UA objective introduced in Section 2.5. UA ac-
counts for the compute budget through a uniform local allocation without specifying the deployed
search rule. We relate its weighting function to the shared-budget retry objective, providing an
additional interpretation of how the two objectives account for compute.

From shared-budget to local criticality. Consider the retry objective in Equation (14), with in-
dependent Tt ∼ Geom(pt ), pt ∈ (0, 1), and integer N ≥ L. Write
                               L
                               X                       X
                        SL =         Ts ,      Rt =           Ts ,   Bt = N − Rt .
                               s=1                     s̸=t
Here, Bt is the budget left for step t after accounting for the waiting times of all other steps. For
integer k ≥ 1, define the success probability and gradient weight of a single-tactic retry problem by
                             F (p, k) = 1 − (1 − p)k ,
                                      ∂ log F (p, k)    kp(1 − p)k−1                                 (49)
                              h(p, k) =              =               .
                                          ∂ log p       1 − (1 − p)k
The shared-budget retry weight then has the exact representation
                               wbtretry (N ) = E[h(pt , Bt ) | SL ≤ N ] .                             (50)
                                                            retry
To see this, extend F (p, k) = 0 for k ≤ 0 and write J   b        (N ) = E[F (pt , Bt )]. The distribution
of Bt does not depend on pt , so differentiating and dividing by the success probability weights each
residual budget by P(Bt = k)F (pt , k)/Jbretry (N ) = P(Bt = k | SL ≤ N ), giving Equation (50).
Only k ≥ 1 occurs under this conditional distribution.
Thus, the shared-budget weight combines two ingredients: the local criticality h(pt , k) and a distri-
bution over the budget available to that step. The other tactic probabilities enter through this budget
distribution.

Uniform allocation and objective.           The UA objective instead assigns each demonstrated step a
uniform local allocation,
                                                     N
                                                 K̄ =  .                                    (51)
                                                     L
This is a modeling choice, not an estimate of E[Bt | SL ≤ N ] or an average over deployed search
strategies. It yields the factorized objective
                                                L h
                                                Y                  i
                                    Jb UA (θ) =     1 − (1 − pt )K̄ .                       (52)
                                                 t=1
For integer K̄, this is the probability that every demonstrated step succeeds within its own quota of
K̄ independent attempts, without transferring unused quota between steps. Noninteger N/L uses
the continuous extension of the same formula. Applying the gradient identity in Equation (7) gives
                                       K̄pt (1 − pt )K̄−1
                               btUA =
                               w                          = h(pt , K̄).                            (53)
                                        1 − (1 − pt )K̄
Comparing Equations (50) and (53), UA evaluates the local criticality at a fixed allocation, whereas
the shared-budget retry objective averages it over the conditional distribution of the residual budget.
The UA weight is the exact gradient weight of its own objective in Equation (52). This connection
does not require UA to approximate the dynamics of a particular deployed search algorithm.

Properties of the uniform-allocation weights. UA is search-agnostic, but not compute-agnostic.
At K̄ = 1, Equation (52) reduces to the demonstrated trace likelihood and all weights equal one,
recovering CE. For fixed K̄ ≥ 1, the weight approaches one as pt → 0; for fixed pt ∈ (0, 1), it
approaches zero as K̄ → ∞. Thus, tactics that are unlikely to be found within the local budget
retain high weight, whereas tactics that can already be recovered through repeated sampling receive
less emphasis. Unlike the shared-budget retry weight, the UA weight does not depend on the other
steps’ consumption of a shared budget. At fixed N and L, each weight depends only on pt .


                                                       33
Interpretation. The shared-budget and UA objectives retain the same local retry criticality but
differ in their treatment of compute allocation. As discussed in Section 4, demonstrations alone do
not generally determine deployed gradient weights because they omit alternative proofs and off-trace
recovery behavior. The empirical comparison in Table 1 evaluates the usefulness of search-aware
CAT and search-agnostic UA for training; it does not establish which objective more accurately
approximates the deployed gradient weights.




                                                34
K    LLM D ISCLOSURE
LLMs were used in 3 primary ways. The first is essentially all experiments were set up and instan-
tiated with LLM coding. We had a separate LLM check for correctness of the code. The second is
when the paper was drafted, we repeatedly asked LLMs to critique and we incorporated its feedback
if we deemed it to be appropriate. The third was finding related papers. We read all of these before
ever citing them to confirm the relation to our work.




                                                35
