                                                ANCORA: Learning to Question via
                                        Manifold-Anchored Self-Play for Verifiable Reasoning


                                                                                    Chengcao Yang
                                                                                    Wuhan University
                                                                                     Wuhan, China
                                                                                 adammyhos@gmail.com
arXiv:2604.27644v2 [cs.LG] 7 May 2026




                                                                                          GitHub
                                                                                        Abstract
                                                    We propose a paradigm shift toward open-ended curriculum self-play: rather
                                                    than learning to answer on a fixed prompt set, a unified policy learns to question—
                                                    generating verifiable problems, solving them, and turning verifier feedback into
                                                    self-improvement without human-annotated solutions. We introduce ANCORA, in
                                                    which the policy alternates between a Proposer that synthesizes novel specifications
                                                    and a Solver that produces verified solutions, anchored by three load-bearing
                                                    mechanisms: a two-level group-relative update coupling Proposer advantages
                                                    across specifications with Solver advantages across solution attempts; iterative
                                                    self-distilled SFT projecting the base model onto its valid-output manifold before
                                                    RL; and a UCB-guided Curriculum DAG whose policy-induced problem set
                                                    can provably expand under self-composition. Without these stabilizers, sparse
                                                    verifier feedback drives Proposer collapse even under MLRL-aligned rewards; with
                                                    them, ANCORA bootstraps a verifiable curriculum from zero human solutions.
                                                    Instantiated in Verus, ANCORA lifts Dafny2Verus pass@1 from a 26.6% SFT
                                                    baseline to 81.5% in test-time training (TTT, 0-shot), outperforming PSV self-
                                                    play by 15.8 points despite PSV’s 1-shot inference; in a transfer setting, training
                                                    from Dafny2Verus seeds yields 36.2% and 17.2% pass@1 on held-out MBPP and
                                                    HumanEval.


                                        1    Introduction
                                        Large language models have achieved broad competence via pre-training on web-scale corpora,
                                        supervised fine-tuning (SFT), and reinforcement learning from verifiable feedback DeepSeek-AI et al.
                                        [2025a]. However, this paradigm faces converging bottlenecks: public human-generated text may
                                        become a scaling bottleneck if current data-demand trends continue Villalobos et al. [2024], human
                                        annotation does not scale, and imitation-based training caps performance at human level Singh et al.
                                        [2024]. Tool-augmented reasoning frameworks such as ReAct Yao et al. [2023] broaden how models
                                        interact with external environments, but they still typically assume a given task distribution rather
                                        than building a verifier-backed curriculum of newly generated problems.
                                        We propose ANCORA, an anchored-curriculum framework that shifts from learning to answer to
                                        learning to question. A unified policy πθ alternates between a Proposer that synthesizes novel problem
                                        specifications and a Solver that produces verified solutions, coupling both roles through a shared
                                        internal model of the problem–solution space. The framework has three load-bearing components:
                                        (i) a two-level group-relative update coupling Proposer advantages across candidate specifications
                                        with Solver advantages across solution attempts; (ii) iterative self-distilled SFT that lifts the base
                                        model onto its valid-output manifold before full RL; and (iii) a UCB-guided Curriculum DAG that
                                        grows only through strictly filtered, novel, Solver-verified specifications, allowing the prompt pool to
                                        expand without poisoning the valid manifold.

                                        Preprint.
Imitation Learning       Reinforcement Learning                                                Self-Evolving
         (SFT)                        (RLVR)                                                    (ANCORA, ours)


        Policy πθ                    Policy πθ                                                 Shared Policy πθ
                                                                                 seed xseed      Proposer ∪ Solver
                                                                                                                                   Q-Gen
                                                                                                       (k)
                                                                                                     rS =                        (Proposer)
      Supervised         Reward        Static       Action          Dynamic                        ′
                                                                                               V(x , y (k) ) ∈ {0, 1}         x′ ∼ πθ (· | xseed )
     πθ (y|x) ← y ∗        r          Prompts       y ∼ πθ                         absorb x′
                                                                   Seed Pool S                    rQ = f (rS )
                                                                   (UCB-DAG)                      rS ∈ {0, 1}K ,
                                                                                                                              S-Gen (Solver)
                                                                                                 frontier-targeting
          Static
                                     Verifier V                                                                               y ∼ πθ (· | x′ )
          Data
                                                                                               Verus Compiler V




    Static supervision   Verifier feedback on static prompts                           Self-generated verifiable curriculum




Figure 1: Learning paradigms. Left: SFT is bounded by static-data supervision. Middle: RLVR uses
environment feedback but a fixed prompt pool. Right: ANCORA. The Proposer (Q-Gen) generates
a novel spec x′ from seed xseed via 1-shot ICL; the Solver (S-Gen) attempts implementation y. A
coupled MLRL update shapes both personas of πθ via Solver outcomes rS ∈ {0, 1}K (§4.2.3–§4.3).
Strictly filtered, novel, Solver-verified specs re-enter the Dynamic Seed Pool, yielding a self-growing
curriculum beyond the initial seed set.



The joint update remains close to GRPO Shao et al. [2024], but its mean normalization is motivated
by Maximum-Likelihood RL (MLRL) Tajwar et al. [2026]: for binary Solver rewards, it matches the
likelihood-aligned weighted-PASS@k estimator up to a score-function baseline. This matters because
recent pass@k analyses suggest that conventional RLVR can mainly sharpen small-k sampling
efficiency without expanding, and sometimes while narrowing, the large-k reasoning boundary
already present in the base model Yue et al. [2025]. For the Proposer, the goal is complementary:
generate specifications near the Solver’s epistemic frontier, where outcome entropy is high enough to
create useful Solver learning signal.
A central failure diagnosis is manifold collapse: when valid outputs are sparse relative to the full
generation space, sparse verifier feedback can push the Proposer off the valid manifold regardless
of whether the Proposer reward is Bernoulli variance 4p(1−p), a low-pass exponential surrogate
e−Kp −e−K , or a Band-1-of-K indicator 1[m=1] (Appendix B). Iterative SFT and the strictly
gated UCB-DAG are therefore not auxiliary engineering details; they are the stabilizers that let
frontier-targeted Proposer rewards operate without curriculum poisoning. Under these stabilizers, the
Band-1-of-K reward is our main-result default; we ablate the other two shapes in Appendix D.3.
We validate ANCORA on Verus formal verification Lattuada et al. [2023], where a deterministic
compiler provides scalable ground-truth rewards. Compared to prior self-play and self-improvement
methods Zhao et al. [2025], Wilf et al. [2025], Chen et al. [2025], ANCORA is distinguished by
its combination of coupled two-level optimization, manifold-first initialization, and strictly gated
UCB-DAG exploration.
Our contributions are: (1) We introduce ANCORA, the first framework, to our knowledge, that
integrates a unified-policy Proposer/Solver with the three mechanisms above for verifiable reasoning.
(2) We diagnose the manifold collapse problem for sparse-verifier RL and show why manifold
projection plus gated anchored exploration is necessary for stable Proposer learning. (3) We empiri-
cally demonstrate that a Qwen2.5-Coder-3B model trained with ANCORA significantly outperforms
baselines on three Verus benchmarks.


2   Related Work

Reasoning with Static Prompts. STaR Zelikman et al. [2022], OpenAI o1 OpenAI [2024], and
DeepSeek-R1 DeepSeek-AI et al. [2025a] train reasoning via RL on a fixed set of human-curated
prompts. While effective at distilling search compute into the policy, they do not expand the problem
space itself, and performance is bounded by the cardinality of the initial prompt set.


                                                               2
Concurrent Self-Play Methods. AZR Zhao et al. [2025] uses a single model for code-based
reasoning with a proposer reward of 1 − r̄solve and Task-Relative REINFORCE++ Hu et al. [2025].
SPELL Yang et al. [2026] adds three roles (questioner, responder, verifier) for document QA via
summed GRPO losses. SPICE Liu et al. [2025a] applies dual-role Dr. GRPO Liu et al. [2025b] to
corpus-grounded math reasoning. SSR Wei et al. [2025] trains a shared bug-injector/solver policy via
PPO Schulman et al. [2017] for software engineering. Notably, negative-gradient destabilization is
not unique to our setting: Kimina-Prover Wang et al. [2025], training a 72B Lean-4 prover via GRPO,
reports early “format collapse” and resorts to probabilistically discarding negative-advantage samples
(ω = 0.5). The underlying phenomenon—thin valid manifolds concentrating repulsion on a few
off-manifold modes rather than spreading it across the vast invalid space—is shared by formal proofs,
verified specifications, and strictly typed code (Appendix B). Unlike ad-hoc sample discarding or
linear inverted rewards, ANCORA prevents format collapse systematically via manifold-constraining
SFT and a UCB-DAG-anchored frontier objective.
Decoupled or Alternating Self-Play. An alternative family maintains separate proposer/solver
models or updates them in alternating phases: Self-Questioning LMs Chen et al. [2025] (asymmetric
self-play), Dr.Zero Yue et al. [2026] (alternating HRPO/GRPO on separate copies), SOAR Sundaram
et al. [2026] (bilevel teacher-student meta-RL), Tool-R0 Acikgoz et al. [2026] (which finds shared
weights hurt their tool-calling domain—a finding our coupled spec/implementation setting reverses),
STP Dong and Ma [2025] (alternating expert iteration for Lean), and Sol-Ver Lin et al. [2026]
(sequential SFT+DPO without RL proposing). These decoupled strategies sidestep gradient conflicts
but forfeit the mutual regularization of shared parameters Silver et al. [2017].
Formal Verification and Self-Improvement. PSV Wilf et al. [2025] uses an alternating propose-
solve loop for Verus. However, its proposer relies on in-context learning rather than RL, and its
solver is updated via rejection fine-tuning. DeepSeek-Prover Ren et al. [2025] uses Lean as a static
reward model without generating new theorems. In contrast, ANCORA formulates specification
generation and solution as a unified RL policy, trained jointly via MLRL-aligned GRPO, repurposing
the compiler as a dynamic engine for autonomous problem discovery.
Positioning. ANCORA’s distinguishing feature is the joint use of all three mechanisms above; Table 3
in the appendix gives a per-feature comparison.


3     Preliminaries

3.1   Maximum Likelihood Reinforcement Learning

Standard binary-reward RL optimizes the expected pass rate E[pθ (x)], sharpening small-k sampling
but not necessarily expanding the underlying reasoning boundary Yue et al. [2025]. MLRL Tajwar
                              the log-likelihood E[log pθ (x)], equivalent at the gradient level to the
et al. [2026] instead targets P
weighted-PASS@k identity k≥1 k1 ∇PASS@k = ∇ log pθ . With N samples and success count
       P
m = i ri (ri ∈ {0, 1}), the hit-conditioned finite-sample estimator normalizes by successes rather
than total samples:
                                                 N
                             ĝML = 1[m>0] m
                                                 X
                                           1
                                                       ri ∇θ log πθ (yi |x).                        (1)
                                                 i=1

Unconditionally this estimator is multiplied by the hit probability 1 − (1 − pθ (x))N ; it is unbiased
conditional on at least one success and becomes exact as the no-hit probability vanishes. We
implement Eq. 1 as a GRPO-style advantage with mean (not std) normalization,

                                                 ri − r̄
                                AML
                                 i  = 1[r̄>0]            ,      r̄ = m
                                                                     N,                             (2)
                                                    r̄
because the resulting group-averaged gradient recovers the same positive-success coefficient as ĝML
plus the corresponding centered score term within hit groups. A rare success (m=1, N =8) thereby
weights N/m=8× REINFORCE’s    √     flat 1/N , matching MLRL’s 1/m. Standard std-normalized
GRPO instead gives A+ ∝ 1/ m, which is heuristic. Throughout ANCORA, “GRPO advantage”
refers to this mean-normalized, MLRL-aligned variant.


                                                  3
                                 Iter 1                           Iter 2                     Iter 3
                         each SFT from base model
                                                                                                       Manifold Init
      Base Model   68 demos      SFT                              SFT                          SFT                 ANCORA RL
        (0.4%)                 (∼0.5%)                          (∼2.8%)                      (26.6%)                 (81.5%)




                              ANCORA RL                        ANCORA RL
                              (early attempt)                  (early attempt)     distill
                                                     distill

                                      Verus c=1                        Verus c=1



                                Verified                        Deduped
                                 Q+S              ∪ dedup        Q+S



Figure 2: Iterative Self-Distilled SFT for valid manifold initialization. Direct RL from the base model
fails due to verified-spec sparsity (positive-signal starvation). Early RL rollouts are filtered by the
Verus compiler and distilled back into the policy; the iterative projection (0.4% → 26.6%) anchors
the model onto the valid manifold before full ANCORA RL.


4     Methodology
4.1     The ANCORA Optimization Framework

ANCORA is a discrete-time dynamic system where a single unified policy πθ serves as both Proposer
and Solver. We refer to Proposer rollouts as question/specification generation (Q-Gen) and Solver roll-
outs as solution generation (S-Gen); correspondingly, subscripts Q and S denote the Proposer/Q-Gen
and Solver/S-Gen branches. At each iteration, the Proposer samples a novel task x′ ∼ πθ (x′ |xseed )
from a dynamically expanding Seed Pool S, and the Solver attempts a solution y ∼ πθ (y|x′ ) judged
by a deterministic verifier V(x′ , y) ∈ {0, 1}. The framework couples the two roles through a shared
policy update while admitting new curriculum nodes only after strict filtering, novelty checks, and
Solver verification, so that self-expansion remains anchored to the valid manifold.

Anchoring as a unifying principle. ANCORA (Manifold-Anchored) names a single rationale
shared by iterative self-distilled SFT (§5), the binary-only filter gate (§4.2.2), and solved-only
UCB-DAG admission (§4.4): refusing off-manifold gradient pressure under sparse verifier feedback,
whether from external-distribution warm-up traces, heuristic-score noise, or unverified curriculum
nodes. CoT itself is then the policy’s manifold-preserving navigation through fragmented pretrained-
known paths Zhou et al. [2023], Wen et al. [2025], the same property that lets RLVR’s verifier signal
generalize without overwriting the base model’s pretrained prior.

4.2     Proposer Policy Strategy

4.2.1    Curriculum Generation
At each step, a seed xseed is selected from the DAG Seed Pool via UCB sampling (§4.4), and the
Proposer generates a one-step curriculum extension. The iterative SFT warm-up teaches the model to
make focused semantic changes rather than superficial rewrites, keeping exploration local enough
to remain on the valid manifold while still walking toward new frontier regions; prompt details are
deferred to Appendix E.

4.2.2    Filter Gate and Zero-Distortion Rewards
Generated candidates pass through a lightweight three-stage accept/reject gate (format checks,
compiler stub syntax validation, and semantic heuristics rejecting vacuous postconditions); rejected
candidates are excluded from the GRPO group. We strictly decouple search from learning: heuristic
scores and MinHash novelty Broder [1997] drive only gating and deduplication, while the policy
gradient is driven exclusively by binary verifier outcomes cj,k ∈ {0, 1}. Injecting tiered heuristics
into the reward instead induces spurious advantage rankings among invalid outputs and displaces
correct-output likelihood mass Deng et al. [2025] (Appendix B).


                                                                      4
4.2.3    Proposer Objective: Frontier-Targeting Reward
The Proposer must generate specifications whose Solver outcomes are informative rather than
degenerate: not saturated (pj ≈ 1), not purely off-manifold noise, but likely to expose useful MLRL
signal for the Solver. Our contribution here is a frontier-targeting reward family: bounded functions of
the Solver’s K binary outcomes that turn the empirical outcome   P distribution itself into the Proposer’s
                                                               1
learning signal.P For each filter-passing spec xj , let pj = K      k cj,k be the Solver’s empirical pass
rate and mj = k cj,k the success count. We instantiate the family with three designs:
                  Rfront (pj , mj ) ∈ 4pj (1 − pj ), e−Kpj − e−K , 1[mj = 1] .
                                     
                                                                                                       (3)
The Bernoulli-variance reward 4pj (1 − pj ) is a smooth symmetric uncertainty kernel (equivalent up
to a constant to the Gini impurity, and the second-order Taylor expansion of H(p) around p=1/2),
peaked at pj =1/2 and zero at both extremes. The exponential variant is a low-pass stress-test kernel
rather than an entropy proxy: it upweights very low empirical pass rates and therefore relies on the
filter and solved-only admission gates to avoid off-manifold zero-signal proposals. The Band-1-of-K
variant is a sparse binary nonzero-signal proxy:
                                       Rprop (xj ) = 1[mj = 1] .                                      (4)
Our main run uses Band-1-of-K: a sparse binary event (m=1 out of K) that emphasizes hard-but-
nonzero specifications and avoids sensitivity to noisy continuous pass-rate estimates. This m=1
regime is precisely where MLRL’s 1/m coefficient (Eq. 1) diverges most from REINFORCE’s flat
1/N , so Band-1-of-K is the binary indicator of the rare-success region that the Solver’s MLRL
update already treats as most informative—rewarding the Proposer for landing there directly aligns
Q/S likelihood signals. The other two shapes, ablated in Appendix D.3, are equally stabilized by
the same SFT+UCB-DAG mechanisms; we treat the family itself, rather than a single shape, as the
methodological contribution.

4.3     Solver Policy Strategy

                    P under the same MLRL principle. For each spec xj with K attempts and
The solver is optimized
                  1
group mean c̄j = K    k cj,k , the token advantage on solution yj,k is
                                                          cj,k − c̄j
                                       Asolve (yj,k ) =              ,                                (5)
                                                           c̄j + ϵ
By Eq. 1, the group-averaged gradient induced by this advantage is the finite-sample MLRL/MaxRL
estimator plus a zero-mean score baseline. All-fail and all-pass groups produce zero centered gradient;
mixed groups update the Solver on exactly the uncertain cases where likelihood mass can still move.

4.4     UCB-Guided Seed Pool and Curriculum DAG

A single Proposer rollout usually produces only a local variation of its conditioning seed. To reach
distant regions without leaving the valid manifold, ANCORA composes such local moves: verified
novel specs are reinserted as future seeds, forming a curriculum DAG (Figure 3). Initial curated
seeds are protected roots; non-original nodes are admitted only if at least one Solver rollout verifies
them (solved-only admission, Lemma G.1); near-duplicates are rejected by MinHash. Seed selection
uses MCTS-style UCB descent Auer et al. [2002], Kocsis and Szepesvári [2006] with a tunable root
quota ρ ∈ [0, 1]: a fraction ρ of the batch is sampled from UCB-chosen roots, and the remaining
1 − ρ performs UCB descent into Q-Gen-discovered children. Our main run uses ρ = 0.50; the
limiting case ρ=1 is reported as the No-Descent ablation (§5.3). Discounted backups, depth-capped
absorb-and-merge, and production deviations are formalized in Appendix G.3–G.12.

Why composition produces novel problems. A single Q-Gen step from a fixed seed explores only
a local neighborhood; the DAG composes such steps. Let Fk be the history, Zk ∈ Rk the selected
seed, Xk ∼ πθ (·|Zk ), and g(Xk ) ∈ {0, 1} the admission gate, so Rk+1 = Rk ∪ {Xk : g(Xk )=1}.
Proposition 4.1 (Compositional reachability). Before saturation, assume Pr[g(Xk )=1, Xk ∈   / Rk |
Fk ] ≥ δ > 0 for all k. Then E[|Rk+1 | | Fk ] ≥ |Rk | + δ and |Rk | → ∞ a.s. (until saturation
if finite). Let U1 = ∪s∈S0 {x : g(x)=1, πθ (x|s) > 0}. If an admitted non-root z is revisited with
probability α > 0 and Pr[g(X)=1, X ∈   / U1 |Z=z] ≥ β > 0, then a composition-only spec outside
U1 is eventually admitted a.s.


                                                    5
                                                   Curriculum DAG Structure


       Original         x1                                         x2                                x3

                                             kin

                                                    ↑ UCB
   Depth 1        x′1                       x′2                    x′3             x′4               x′5

                                                                                  ↓ UCB

   Depth 2                     x′′1                         x′′2                     x′′3

                             ↑ UCB                                                  ↑ UCB

                                      UCB-Guided Seed Selection (one descent)
                                                                                     p
                             x2           Step 1. Pick root by UCB (µ̂ + λZPD ZPD + c ln Ntot /n).
                                descend

                             x′3          Step 2. Compare Ustay vs. maxc Uchild ; descend if child wins by margin m.
                                descend

                             x′′3         Step 3. Stay wins / no children; use x′′3 as next Q-Gen seed; backprop r · γ d .




Figure 3: The UCB-guided Curriculum DAG. Top: Original seeds (blue) are protected roots;
Proposer-generated specs (green) are admitted as children only after solved-only verification; high-
UCB frontier nodes (orange) become next-step seeds, low-UCB nodes (red, dashed) are deprioritized;
dashed-violet edges mark structural kinship (Jaccard ≥ 0.70). Bottom: Selection first picks a root
by UCB, then performs local stay-vs-child descent, using the terminal node as the next Q-Gen
conditioning seed. Appendix G.12 gives the full production deviations.


Proof. Let Ik = 1[g(Xk )=1, Xk ∈  / Rk ]. Since |Rk+1 | = |Rk | + Ik , the expectation bound follows.
Also Pr[Ik = · · · = Ik+m−1 = 0 | Fk ] ≤ (1 − δ)m , giving finite waiting time for each new node a.s.;
induction gives divergence until saturation. The second claim is the same geometric-tail argument
with success probability αβ. □
Thus sustained expansion needs persistent exploration, not only a good local generator. ANCORA
approximates this with protected roots, the ρ=0.50 root/DAG mixture, UCB bonuses, and solved-only
admission; a literal guarantee would add an ϵ-refresh or sampling floor over active roots/frontier leaves.
Empirically, Q-Gen validity stays bounded away from zero and the seed pool grows monotonically
over the logged diagnostic window (Appendix D), so composition expands the effective training
distribution beyond its initial seed support.

4.5   Coupled Joint Optimization

Both Proposer and Solver are segments of a single unified policy πθ . For each iteration, B prompts
yield N candidate specifications each; each valid specification receives K solver rollouts. Problem
tokens receive Rprop via the mean-normalized GRPO variant in §3.1; Proposer advantages are
normalized within each seed’s N Q-Gen candidates, with invalid candidates assigned zero Proposer
reward and skipped only by the Solver rollout. Solver tokens receive binary Rsolve ∈ {0, 1} over
K solutions, for which the same normalization realizes the MLRL weighted-PASS@k estimator
exactly. The Band-1-of-K Proposer reward is also binary and follows the same algebra, but targets
the likelihood of an informative-frontier event (mj =1 of K) rather than literal Solver correctness—an
MLRL-style update on a different binary signal.
Branch balancing. Solver responses are much longer than Proposer specs, so raw token-level
advantages let the Solver dominate. We equalize generated token mass per batch with scaleQ =


                                                                     6
(TQ + TS )/(2TQ ) and scaleS = (TQ + TS )/(2TS ), then apply a static Proposer scale wQ = qscale =
0.375, wS = 1.0. Adaptive ℓ2 -balance and the reverse-imbalance failure mode are analyzed in
Appendices D.6 and D.7; Algorithm 1 gives the full iteration.

5     Experiments
In our Verus instantiation, specifications (spec/ensures) serve as questions and implementations as
answers, with the compiler providing deterministic binary feedback.

5.1   Setup

Datasets. We evaluate on three Verus benchmarks: Dafny2Verus (274 problems, translated from
Dafny Aggarwal et al. [2024]; of these, 234 pass the seed-pool quality filter and form the curriculum’s
initial roots in the Transfer setting), MBPP-Verified (78 problems Austin et al. [2021], Yang et al.
[2025]), and HumanEval-Verified (85 functions converted from HumanEval Chen et al. [2021]). We
adopt Pass@k Chen et al. [2021] with n=100 samples.

Baselines. We compare against: (1) AlphaVerus Aggarwal et al. [2024] (50-shot prompting), the
prior SOTA for verified code generation; (2) iterative RFT Yuan et al. [2023], Singh et al. [2024],
expert iteration without proposing; and (3) PSV Wilf et al. [2025], alternating propose-solve with
rejection fine-tuning.

Implementation. Built on verl/HybridFlow Sheng et al. [2024] with vllm for rollout Kwon
et al. [2023]. All experiments use 2×A100 (40GB). We perform full-parameter fine-tuning on
Qwen2.5-Coder-3B-Instruct Hui et al. [2024] with AdamW, Flash-Attention 2, and bfloat16. The SFT
phase uses lr=1×10−5 with cosine schedule; the RL phase uses lr=1×10−6 with 5% linear warmup.
Each training step samples B=8 seeds from the curriculum DAG; each seed yields N =8 candidate
specifications, and each valid specification receives K=8 solver rollouts. Maximum sequence length
is 4096 tokens. The RL phase runs for 2,000 steps, totaling approximately 200 GPU-hours on
2×A100.

Iterative SFT warm-up. The unadapted Qwen2.5-Coder-3B-Instruct achieves only 0.4% pass@1
on Dafny2Verus, and direct RL from this point triggers the manifold collapse of Appendix B. We
start with 68 basic Verus specs whose Q-Gen/S-Gen traces are generated by Kimi-K2.5 Kimi Team
et al. [2026] and DeepSeek-V3.2 DeepSeek-AI et al. [2025b], mainly to teach formatting and proof
skeletons (0.4% → ∼0.5%), then distill MinHash-deduplicated Verus-verified rollouts across three
early ANCORA iterations (2 epochs). Beyond three iterations SFT overfits, so only early-stage data
is used; Table 1 shows the progression. In the TTT setting all methods already use the full evaluation
set as RL seed prompts, so the warm-up specs introduce no additional test-set exposure.

Table 1: SFT bootstrapping via accumulated verified rollouts. Each iteration collects Verus-verified
Proposer/Q-Gen specifications and Solver/S-Gen implementations from ANCORA training, dedupli-
cates them, and distills the resulting traces into SFT data for the next round.

              Phase                          Data source                      D2V p@1
              Base model                     —                                   0.4
              SFT iter 1                     68 basic seed demos (Kimi/DS)      ∼0.5
              SFT iter 2                     + iter 1 verified rollouts         ∼2.8
              SFT iter 3                     + dedup(iter 1+2 rollouts)         26.6
              + ANCORA RL (2,000 steps)      —                                   81.5

The final sft_init reaches 26.6% / 8.8% / 6.2% pass@1 on D2V / MBPP / HumanEval—sufficient
manifold coverage for stable RL training (Appendix B).

5.2   Main Results

Table 2 presents pass rates across all benchmarks.


                                                  7
Table 2: Pass@k (%) on Verus benchmarks. All methods use Qwen2.5-Coder-3B-Instruct. Transfer
Learning trains on Dafny2Verus and evaluates on MBPP/HumanEval as held-out sets; Test-Time
Training (TTT) uses filtered evaluation roots as RL seed prompts. Our TTT run uses the union of the
three benchmark root sets and reports each benchmark separately.
                                    Dafny2Verus                       MBPP                       HumanEval
                               p@1       p@5      p@10         p@1     p@5       p@10       p@1       p@5      p@10
  Transfer Learning (seed X0 = Dafny2Verus)
  AlphaVerus (50-shot)        24.06     52.42      63.44     6.48      18.36     24.57     7.24      15.38     18.02
  RFT (1-shot)                  –         –          –       10.99     26.03     31.19     10.99     18.07     20.02
  PSV (1-shot)                  –         –          –       25.25     38.32     41.51     16.18     21.61     23.13
  ANCORA (0-shot)               –         –          –       36.20     38.49     39.94     17.19     20.16     21.03
  Test-Time Training (seed X0 = test dataset)
  AlphaVerus (50-shot)        24.06     52.42      63.44      6.48     18.36     24.57      7.24     15.38     18.02
  RFT (1-shot)                34.46     57.12      63.40      3.83     14.56     22.64      5.56     12.46     14.80
  PSV (1-shot)                65.63     78.04      80.06     36.78     51.22     53.67     19.07     23.42     25.16
  ANCORA (0-shot)             81.46     83.86      84.58     44.11     46.62     47.91     19.15     21.67     23.91
AlphaVerus uses 50-shot prompting (no training); PSV and RFT results from Wilf et al. [2025]. Human-written solutions are
                                                    never trained on.


Evaluation protocol note. ANCORA is reported at 0-shot throughout, while PSV results are
at 1-shot Wilf et al. [2025]; the +15.8-point Dafny2Verus gap is therefore conservative in spirit
rather than a formal lower bound, since prompt mismatch at 1-shot could in principle help or hurt
ANCORA’s score.
ANCORA significantly outperforms baselines on Dafny2Verus and MBPP, and remains competi-
tive on HumanEval. At step 2,000 (with n=100 rollouts), ANCORA achieves 81.5% pass@1 on
Dafny2Verus, a +15.8-point gain over PSV (1-shot). In TTT on MBPP, ANCORA reaches 44.1%
pass@1, exceeding PSV by 7.3 points. On HumanEval, ANCORA matches PSV at pass@1 (19.2%
vs. 19.1%) and remains within 1.3 points on pass@10 (23.9% vs. 25.2%), reflecting the protocol-
controlled tradeoff: ANCORA recovers PSV’s 1-shot pass@1 without any in-context exemplar at
inference time. The flat TTT MBPP pass@k curve (44.1→47.9 across k=1→10) indicates the policy
has sharpened to near-deterministic solutions for solvable problems. On Transfer MBPP, ANCORA’s
pass@10 (39.9) is within 1.6 points of PSV (41.5), and its pass@1 remains higher (36.2 vs. 25.3 for
PSV) despite a slightly narrower sampling tail. The narrower HumanEval margin reflects task-origin
domain shift orthogonal to this sharpening: although all three benchmarks are evaluated as Verus
code, HumanEval-Verified’s 85 functions are Verus translations of general Python programming
tasks (string parsing, list manipulation, arithmetic loops) rather than algorithm-verification specifica-
tions native to D2V, so the D2V-seeded Proposer distribution transfers less directly to HumanEval
than to MBPP’s algorithmic-task style. This is the price of training the Proposer on a single seed
family—transferable problem-solving structure is preserved (HE pass@1 rises from 6.2% SFT init to
17.2% Transfer / 19.2% TTT), but the gain narrows as the evaluation domain drifts further from the
seed-induced distribution.

5.3   Learning Curves and Coupled-Branch Ablation

Figure 4 traces live pass@1 in the test-time-training setting corresponding to the lower block of
Table 2. Starting from the manifold-projected sft_init (26.6% / 8.8% / 6.2% on D2V / MBPP
/ HumanEval), the final n=100 evaluation at step 2,000 gives the headline numbers in Table 2.
Dafny2Verus and MBPP show a sustained upward trend with small checkpoint-level fluctuations;
HumanEval shows higher variance due to its smaller evaluation set (85 problems). Late-stage Solver
responses are well-formed proof-oriented derivations rather than pathological repetition (Appendix F).
To isolate the contribution of each branch in the coupled optimization, we conduct branch-freeze
experiments: Freeze-Q masks the Proposer/Q-Gen loss contribution (only Solver tokens update the
shared policy), and Freeze-S masks the Solver/S-Gen loss contribution (only Proposer tokens update
it). Both variants share the same SFT initialization and hyperparameters as the full ANCORA run.
Figure 4 reports pass@1 on all three benchmarks.


                                                           8
                          (a) Dafny2Verus                    (b) MBPP                      (c) HumanEval

                 80
                                               40                                  20

    Pass@1 (%)
                 60

                 40
                                               20                                  10
                 20

                  0                              0                                0
                      0   500   1,000 1,500 2,000 0      500     1,000 1,500 2,000 0      500    1,000 1,500 2,000

                                Step                             Step                            Step

                                    ANCORA            Freeze-Q          Freeze-S        No-Descent


Figure 4: Branch-freeze and root-only curriculum ablation in the test-time-training setting across
∼2,000 RL steps. Curves show live training-time evaluation (small-n); the headline pass@k numbers
in Table 2 use n=100 at the final checkpoint and may differ by 1–2 points due to sampling variance,
particularly on HumanEval (85 problems). See text for detailed analysis of the failure modes of
Freeze-Q (plateaus), Freeze-S (collapses), and No-Descent (initially peaks then collapses).


• Freeze-Q (static curriculum): initially tracks ANCORA (step 99: 36.9% vs. 38.6% D2V) but
  plateaus by step 300, ending 14.4 points below ANCORA at the matched step 499—Proposer
  co-evolution is essential.
• Freeze-S (reward collapse): proposed problems become unsolvable or trivial, the informative
  frontier-reward region vanishes, and performance falls below SFT init by step 400—a manifestation
  of the manifold collapse in Appendix B.
• No-Descent (root-only anchoring collapse): in the TTT root-only run, the limiting case ρ=1
  initially climbs steeply (51.3% D2V at step 400) by exploiting curated seeds, then collapses after
  step 500 (D2V 12% by step 1,999; MBPP falls to 1.6% by step 799 and 0% by step 1,999).
  Without the 50% DAG-descent fraction into verified Q-Gen children, the curriculum cannot
  bootstrap once original seeds are exhausted.
The non-zero descent fraction is the load-bearing stabilizer that converts early gains into sustained
improvement.

5.3.1            Additional Diagnostics
Detailed training diagnostics and partial-control ablations are reported in Appendix D, including
Q-Gen validity, seed-pool growth, Proposer reward variants, UCB exploit statistics, ZPD admission-
window clipping (a negative-result variant of the ZPD prior), and static vs. adaptive Q/S branch
weighting.

6   Discussion and Conclusion
We presented ANCORA, a framework for autonomous self-improvement in verifiable reasoning that
unifies problem proposing and solving within a single RL policy. The results—81.5% pass@1 on
Dafny2Verus at 0-shot and 36.2% / 17.2% on held-out MBPP / HumanEval in a separate D2V-seeded
transfer run—show that a 3B model can bootstrap a verifiable problem distribution from curated
seeds without human-written training solutions.
Takeaways and limitations. For thin-manifold RL, our evidence points to two load-bearing in-
gredients: a manifold-projection phase that lifts pM above 1/N before policy gradients apply, and
a state-conditioned exploration anchor that prevents drift back below this threshold. Concurrent
Lean work Wang et al. [2025] reaches a related conclusion via gradient filtering. ANCORA remains
compute-limited to a 3B Verus study and does not yet solve within-manifold mode collapse (Ap-
pendix D.5); long-horizon TTT is also open, since an unbounded solved-only Seed Pool should
ideally support steady gains, yet our 2,000-step runs plateau after the main phase. Testing Lean4 and
other verifier-backed domains remains future work.


                                                                 9
Acknowledgments and Disclosure of Funding
The numerical calculations in this paper have been done on the supercomputing system in the
Supercomputing Center of Wuhan University, funded by computational grants provided by Prof. Jun
Chen. We extend our deepest gratitude to Prof. Jun Chen for his essential support. We also thank
Xuewei Jiao for computational support during the early stages of this project, and Haopeng Lao for
generously sharing access to Codex, which assisted in code development.

References
E. C. Acikgoz, C. Qian, J. Hübotter, H. Ji, D. Hakkani-Tür, and G. Tur. Tool-r0: Self-evolving llm
   agents for tool-learning from zero data, 2026. URL https://arxiv.org/abs/2602.21320.
P. Aggarwal, B. Parno, and S. Welleck. AlphaVerus: Bootstrapping Formally Verified Code
   Generation through Self-Improving Translation and Treefinement, Dec. 2024. URL https:
   //arxiv.org/abs/2412.06176v1.
P. Auer, N. Cesa-Bianchi, and P. Fischer. Finite-time analysis of the multiarmed bandit problem.
   Machine Learning, 47(2–3):235–256, 2002.
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry,
   Q. Le, and C. Sutton. Program synthesis with large language models, 2021. URL https:
   //arxiv.org/abs/2108.07732.
A. Z. Broder. On the resemblance and containment of documents. In Proceedings. Compression and
  Complexity of SEQUENCES 1997 (Cat. No. 97TB100171), pages 21–29. IEEE, 1997.
L. Chen, M. Prabhudesai, K. Fragkiadaki, H. Liu, and D. Pathak. Self-questioning language models,
   2025. URL https://arxiv.org/abs/2508.03682.
M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda,
 N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin,
 B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P.
 Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol,
 A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr,
 J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati,
 K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba.
 Evaluating large language models trained on code, 2021. URL https://arxiv.org/abs/2107.
 03374.
DeepSeek-AI, D. Guo, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement
  learning, 2025a. URL https://arxiv.org/abs/2501.12948.
DeepSeek-AI, A. Liu, et al. Deepseek-v3.2: Pushing the frontier of open large language models,
  2025b. URL https://arxiv.org/abs/2512.02556.
W. Deng, Y. Ren, M. Li, D. J. Sutherland, X. Li, and C. Thrampoulidis. On the effect of negative
  gradient in group relative deep reinforcement optimization, 2025. URL https://arxiv.org/
  abs/2505.18830.
K. Dong and T. Ma. Stp: Self-play llm theorem provers with iterative conjecturing and proving, 2025.
  URL https://arxiv.org/abs/2502.00212.
A. Garivier and E. Moulines. On upper-confidence bound policies for switching bandit problems. In
  International conference on algorithmic learning theory, pages 174–188. Springer, 2011.
J. Hu, J. K. Liu, H. Xu, and W. Shen. Reinforce++: Stabilizing critic-free policy optimization with
   global advantage normalization, 2025. URL https://arxiv.org/abs/2501.03262.
B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Dang, et al. Qwen2.5-
  coder technical report. arXiv preprint arXiv:2409.12186, 2024. URL https://arxiv.org/abs/
  2409.12186.


                                                 10
Kimi Team, T. Bai, et al. Kimi k2.5: Visual agentic intelligence, 2026. URL https://arxiv.org/
  abs/2602.02276.
R. Kleinberg, A. Slivkins, and E. Upfal. Multi-armed bandits in metric spaces. In Proceedings of the
  fortieth annual ACM symposium on Theory of computing, pages 681–690, 2008.
L. Kocsis and C. Szepesvári. Bandit based Monte-Carlo planning. In Machine Learning: ECML
  2006, pages 282–293. Springer, 2006.
W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Sto-
  ica. Efficient memory management for large language model serving with pagedattention. In
 Proceedings of the 29th Symposium on Operating Systems Principles, pages 611–626, 2023.
A. Lattuada, T. Hance, C. Cho, M. Brun, I. Subasinghe, Y. Zhou, J. Howell, B. Parno, and C. Haw-
  blitzel. Verus: Verifying rust programs using linear ghost types. Proceedings of the ACM on
  Programming Languages, 7(OOPSLA1):286–315, 2023.
Z. Lin, S. Shen, I. Kulikov, J. Shang, J. Weston, and Y. Nie. Learning to solve and verify: A self-play
   framework for code and test generation, 2026. URL https://arxiv.org/abs/2502.14948.
B. Liu, C. Jin, S. Kim, W. Yuan, W. Zhao, I. Kulikov, X. Li, S. Sukhbaatar, J. Lanchantin, and
  J. Weston. Spice: Self-play in corpus environments improves reasoning, 2025a. URL https:
  //arxiv.org/abs/2510.24684.
Z. Liu, C. Chen, W. Li, P. Qi, T. Pang, C. Du, W. S. Lee, and M. Lin. Understanding r1-zero-like
  training: A critical perspective, 2025b. URL https://arxiv.org/abs/2503.20783.
OpenAI. Openai o1 system card, 2024. URL https://arxiv.org/abs/2412.16720.
Z. Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao, L. Zhang, Z. Fu, Q. Zhu, D. Yang, Z. F. Wu,
   Z. Gou, S. Ma, H. Tang, Y. Liu, W. Gao, D. Guo, and C. Ruan. Deepseek-prover-v2: Advancing
   formal mathematical reasoning via reinforcement learning for subgoal decomposition, 2025. URL
   https://arxiv.org/abs/2504.21801.
J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization
   algorithms, 2017. URL https://arxiv.org/abs/1707.06347.
Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. K. Li, Y. Wu, and D. Guo.
   Deepseekmath: Pushing the limits of mathematical reasoning in open language models, 2024.
   URL https://arxiv.org/abs/2402.03300.
G. Sheng, C. Zhang, Z. Ye, X. Wu, W. Zhang, R. Zhang, Y. Peng, H. Lin, and C. Wu. Hybridflow: A
  flexible and efficient rlhf framework, 2024. URL https://arxiv.org/abs/2409.19256.
D. Silver, T. Hubert, J. Schrittwieser, I. Antonoglou, M. Lai, A. Guez, M. Lanctot, L. Sifre,
  D. Kumaran, T. Graepel, T. Lillicrap, K. Simonyan, and D. Hassabis. Mastering chess
  and shogi by self-play with a general reinforcement learning algorithm, 2017. URL https:
  //arxiv.org/abs/1712.01815.
A. Singh, J. D. Co-Reyes, R. Agarwal, A. Anand, P. Patil, X. Garcia, P. J. Liu, J. Harrison, J. Lee,
  K. Xu, A. Parisi, A. Kumar, A. Alemi, A. Rizkowsky, A. Nova, B. Adlam, B. Bohnet, G. Elsayed,
  H. Sedghi, I. Mordatch, I. Simpson, I. Gur, J. Snoek, J. Pennington, J. Hron, K. Kenealy, K. Swersky,
  K. Mahajan, L. Culp, L. Xiao, M. L. Bileschi, N. Constant, R. Novak, R. Liu, T. Warkentin, Y. Qian,
  Y. Bansal, E. Dyer, B. Neyshabur, J. Sohl-Dickstein, and N. Fiedel. Beyond human data: Scaling
  self-training for problem-solving with language models, 2024. URL https://arxiv.org/abs/
  2312.06585.
S. Sundaram, J. Quan, A. Kwiatkowski, K. Ahuja, Y. Ollivier, and J. Kempe. Teaching models to
   teach themselves: Reasoning at the edge of learnability, 2026. URL https://arxiv.org/abs/
   2601.18778.
F. Tajwar, G. Zeng, Y. Zhou, Y. Song, D. Arora, Y. Jiang, J. Schneider, R. Salakhutdinov, H. Feng,
   and A. Zanette. Maximum likelihood reinforcement learning, 2026. URL https://arxiv.org/
   abs/2602.02710.


                                                  11
P. Villalobos, A. Ho, J. Sevilla, T. Besiroglu, L. Heim, and M. Hobbhahn. Position: Will we run out
   of data? Limits of LLM scaling based on human-generated data. In R. Salakhutdinov, Z. Kolter,
   K. Heller, A. Weller, N. Oliver, J. Scarlett, and F. Berkenkamp, editors, Proceedings of the 41st
   International Conference on Machine Learning, volume 235 of Proceedings of Machine Learning
   Research, pages 49523–49544. PMLR, 21–27 Jul 2024. URL https://proceedings.mlr.
   press/v235/villalobos24a.html.
H. Wang, M. Unsal, X. Lin, M. Baksys, J. Liu, M. D. Santos, F. Sung, M. Vinyes, Z. Ying, Z. Zhu,
  J. Lu, H. de Saxcé, B. Bailey, C. Song, C. Xiao, D. Zhang, E. Zhang, F. Pu, H. Zhu, J. Liu, J. Bayer,
  J. Michel, L. Yu, L. Dreyfus-Schmidt, L. Tunstall, L. Pagani, M. Machado, P. Bourigault, R. Wang,
  S. Polu, T. Barroyer, W.-D. Li, Y. Niu, Y. Fleureau, Y. Hu, Z. Yu, Z. Wang, Z. Yang, Z. Liu, and
  J. Li. Kimina-prover preview: Towards large formal reasoning models with reinforcement learning,
  2025. URL https://arxiv.org/abs/2504.11354.
Y. Wei, Z. Sun, E. McMilin, J. Gehring, D. Zhang, G. Synnaeve, D. Fried, L. Zhang, and S. Wang.
  Toward training superintelligent software agents through self-play swe-rl, 2025. URL https:
  //arxiv.org/abs/2512.18552.
X. Wen, Z. Liu, S. Zheng, S. Ye, Z. Wu, Y. Wang, Z. Xu, X. Liang, J. Li, Z. Miao, J. Bian, and
  M. Yang. Reinforcement learning with verifiable rewards implicitly incentivizes correct reasoning
  in base llms, 2025. URL https://arxiv.org/abs/2506.14245.
A. Wilf, P. Aggarwal, B. Parno, D. Fried, L.-P. Morency, P. P. Liang, and S. Welleck. Propose,
  solve, verify: Self-play through formal verification, 2025. URL https://arxiv.org/abs/2512.
  18160.
Y. Xu. Optimizer-induced low-dimensional drift and transverse dynamics in transformer training,
   2026. URL https://arxiv.org/abs/2602.23696.
C. Yang, X. Li, M. R. H. Misu, J. Yao, W. Cui, Y. Gong, C. Hawblitzel, S. Lahiri, J. R. Lorch,
  S. Lu, F. Yang, Z. Zhou, and S. Lu. AutoVerus: Automated Proof Generation for Rust Code.
  Proc. ACM Program. Lang., 9(OOPSLA2):3454–3482, Oct. 2025. doi: 10.1145/3763174. URL
  https://dl.acm.org/doi/10.1145/3763174.
Z. Yang, W. Shen, C. Li, R. Chen, F. Wan, M. Yan, X. Quan, and F. Huang. Spell: Self-play
  reinforcement learning for evolving long-context language models, 2026. URL https://arxiv.
  org/abs/2509.23863.
S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao. React: Synergizing reasoning
   and acting in language models, 2023. URL https://arxiv.org/abs/2210.03629.
Z. Yuan, H. Yuan, C. Li, G. Dong, K. Lu, C. Tan, C. Zhou, and J. Zhou. Scaling relationship on
  learning mathematical reasoning with large language models, 2023. URL https://arxiv.org/
  abs/2308.01825.
Y. Yue, Z. Chen, R. Lu, A. Zhao, Z. Wang, Y. Yue, S. Song, and G. Huang. Does reinforcement
  learning really incentivize reasoning capacity in llms beyond the base model?, 2025. URL
  https://arxiv.org/abs/2504.13837.
Z. Yue, K. Upasani, X. Yang, S. Ge, S. Nie, Y. Mao, Z. Liu, and D. Wang. Dr. zero: Self-evolving
  search agents without training data, 2026. URL https://arxiv.org/abs/2601.07055.
E. Zelikman, Y. Wu, J. Mu, and N. D. Goodman. Star: Bootstrapping reasoning with reasoning, 2022.
   URL https://arxiv.org/abs/2203.14465.
A. Zhao, Y. Wu, Y. Yue, T. Wu, Q. Xu, Y. Yue, M. Lin, S. Wang, Q. Wu, Z. Zheng, and G. Huang.
  Absolute zero: Reinforced self-play reasoning with zero data, 2025. URL https://arxiv.org/
  abs/2505.03335.
C. Zhou, P. Liu, P. Xu, S. Iyer, J. Sun, Y. Mao, X. Ma, A. Efrat, P. Yu, L. Yu, S. Zhang, G. Ghosh,
  M. Lewis, L. Zettlemoyer, and O. Levy. Lima: Less is more for alignment, 2023. URL https:
  //arxiv.org/abs/2305.11206.



                                                  12
A     Feature Comparison with Concurrent Methods

Table 3: Feature comparison of self-play and self-improvement methods. ✓= present, × = absent.

    Method       Unified Policy    RL Proposer     Manifold SFT      UCB Seed      Binary Reward
    AZR                ✓                ✓                ×               ×               ×
    SPELL              ×                ✓                ×               ×               ×
    SPICE              ✓                ✓                ×               ×               ×
    Dr.Zero            ×                ✓                ×               ×               ×
    PSV                ×                ×                ×               ×               ✓
    ANCORA             ✓                ✓                ✓               ✓               ✓


B     Off-Manifold Gradient Dominance and Policy Collapse
We formalize why RL with sparse valid outputs leads to policy collapse through three complementary
mechanisms: gradient starvation from rare positive signals, sparse-sampling distortion of the GRPO
gradient, and optimizer momentum drift under zero-gradient batches. The analysis applies to
any setting where the valid output space is a small fraction of the full generation space—formal
specifications, theorem proofs, type-correct programs, or any task with strict structural constraints.

B.1   Setup

Let Y = V T denote the space of token sequences of length T over vocabulary V, with |Y| = |V|T . Let
M ⊂ Y denote the valid manifold—the set of outputs satisfying task-specific structural constraints
(e.g., compilable specifications, well-typed proofs). Define the on-manifold probability mass:
                                                X
                                         pM ≜        πθ (y | x)                                  (6)
                                               y∈M

Scope of this analysis. The collapse mechanisms below concern samples that enter the GRPO
loss: every Solver rollout, and every filter-passing Proposer specification. The Q-Gen filter pipeline
(§4.2.2) rejects malformed Proposer candidates outright, so they never appear as yi in the group and
contribute no gradient at all—this is a separate, intentional zero-gradient pathway and is not the
subject of the theorems that follow.
Reward structure. For samples that do enter the group, we use pure binary rewards: R(y) = 1 if
y ∈ M and is verified correct (or, on the Proposer side, if the Solver-outcome reward fires), and
R(y) = 0 otherwise. This is a deliberate design choice validated empirically: we found that heuristic
intermediate scores (e.g., partial credit for syntactically valid but semantically incorrect outputs)
harm training by introducing reward noise that destabilizes the policy gradient (see §4.2.2). In the
MLRL-aligned GRPO variant used by ANCORA, the advantage for sample yi in a group of N
                                                            PN
samples is A(yi ) = (R(yi ) − R̄)/(R̄ + ϵ), where R̄ = N1 j=1 R(yj ).
Consequence of binary rewards. When all N samples in a group earn R(yi ) = 0 (no Solver
attempt verifies, or no filter-passing Proposer spec fires the frontier-targeting reward), the GRPO
baseline becomes R̄ = 0, and every advantage is A(yi ) = 0. The gradient contribution from this
group is exactly zero. This is strictly better than tiered negative rewards (which would produce
nonzero advantages that push the policy in arbitrary directions), but as we show in Theorem B.3
and Proposition B.4, zero gradients create their own pathology through sparse-sampling distortion
and optimizer momentum drift; meanwhile, the rare mixed group with 0 < k < N positive samples
produces concentrated negative-advantage directions on the N − k zero-reward samples, which is the
second mechanism formalized in Theorem B.2.

B.2   Gradient Starvation (Theorem 1)

Theorem B.1 (Positive Signal Starvation). Given group size N and on-manifold probability pM , the
probability that a group contains zero valid samples is:
                                           / M) = (1 − pM )N ≥ 1 − N pM
                       Pr (∀ i ∈ [N ] : yi ∈                                                       (7)


                                                 13
When pM ≪ 1/N :
                                    (1 − pM )N ≈ e−N pM → 1                                        (8)

Proof. Direct application of the Bernoulli trial model. Each sample independently hits M with
probability pM . For pM = 1/256 and N = 8 (our practical setting), the probability of at least one
valid sample is 1 − (1 − 1/256)8 ≈ 0.031, meaning ∼97% of groups produce zero gradient under
binary rewards.

Implication. With binary rewards, a zero-hit group produces zero GRPO gradient. The policy
receives a learning signal from at most ∼3% of groups. The remaining 97% are wasted compute that,
as we show next, create pathological gradient estimates in the groups that do contain valid samples.

B.3   Gradient Decomposition (Theorem 2)

Theorem B.2 (Off-Manifold Coupling in Informative Groups). The expected mean-normalized
GRPO policy gradient decomposes as:
                             ∇θ J(θ) =       p · g+            + (1 − pM ) · g−                    (9)
                                             | M{z }             |     {z     }
                                          on-manifold signal     off-manifold signal

where:
                           g+ = Ey∼πθ (·|x), y∈M [A(y)∇θ log πθ (y | x)]                          (10)
                            −
                           g = Ey∼πθ (·|x), y∈M
                                             /  [A(y)∇θ log πθ (y | x)]                           (11)
For any informative group with 0 < k < N valid samples, the group-averaged estimator contains
both the ML-normalized positive term and a sampled negative score term:
                                                                                
                     1 N − k X                            X
             ĝMN =                   ∇θ log πθ (y + |x) −     ∇θ log πθ (y − |x) .     (12)
                     N      k      +                       −
                                   y ∈G                              y ∈G

Thus mean normalization fixes the positive coefficient required by MLRL, but it does not remove the
off-manifold directions sampled in the same finite group.

Proof. By the law of total expectation, conditioning on y ∈ M vs. y ∈/ M. Under mean-normalized
binary rewards, in a group with k ≥ 1 valid samples out of N , the baseline is R̄ = k/N , and
advantages are A(y + ) = (N − k)/k for valid and A(y − ) = −1 for invalid samples. Thus the
positive coefficient recovers the MLRL 1/k success normalization after the group average, while
every sampled invalid output still contributes a negative score term. When pM ≪ 1, informative
groups are rare and the negative component is estimated from only N − k sampled off-manifold
directions, producing the sparse-sampling distortion formalized next.

B.4   Sparse Sampling Distortion (Theorem 3)

In practice, group sizes are small (N = 8 in our setting) while the true positive rate can be extremely
sparse (pM ≈ 1/256). This creates a finite-sample distortion in the GRPO gradient that concentrates
repulsion on a few specific negatives rather than diffusing it uniformly.
Theorem B.3 (GRPO Sparse-Sampling Distortion). Let the true positive rate be pM = 1/M where
M ≫ N . Consider the idealized gradient under full enumeration vs. the realized gradient with N
samples. Assumption (uniform off-manifold sampling): the policy assigns near-equal probability
πθ (y + | x) ≈ 1/M to the valid output and πθ (yi− | x) ≈ 1/M to each of the M − 1 invalid modes,
so the total off-manifold mass is (M − 1)/M . This is the conservative case for the variance estimate
below; if πθ (·|x) is concentrated on a few modes off the manifold, the qualitative claim of repulsion
concentration on a small subspace strengthens.
Full-enumeration gradient. With access to all M outputs (one positive, M − 1 negatives), baseline
R̄ = 1/M :
                                                     M  −1
                             M −1                     X     1
                  ∇θ Jfull =                    +
                                    ∇θ log πθ (y ) −          ∇θ log πθ (yi− )               (13)
                               M                      i=1
                                                           M


                                                     14
The negative gradient is spread uniformly across M − 1 negatives, each receiving weight 1/M .
GRPO gradient with N samples. Conditioned on a group containing exactly one valid sample
y + and N − 1 negatives {yj−1 , . . . , yj−N −1 } drawn without replacement from Y \ M, the advantage
baseline is R̄ = 1/N , giving:
                                                            N −1
                                 N −1                    X 1
                   ∇θ JˆGRPO =        ∇θ log πθ (y + ) −     ∇θ log πθ (yj−k )                   (14)
                                  N                        N
                                                            k=1

The finite-sample deviation in the negative component is:
                                 N −1                       M −1
                               1 X                        1 X
                    ∆g− = −           ∇θ log πθ (yj−k ) +        ∇θ log πθ (yi− )                (15)
                               N                          M i=1
                                  k=1

The variance of this deviation term scales as:
                                                                           2
                                             
                                     1     1                              σscore
                   Var[∆g− ] = O        −       · Vary∈M
                                                      / [∇θ log πθ (y)] ≈                        (16)
                                     N     M                               N
       2
where σscore is the variance of score functions across the off-manifold space.

Proof. The key observation is that the GRPO negative gradient concentrates weight 1/N on each of
N − 1 specific negatives, while the ideal gradient distributes weight 1/M across M − 1 negatives.
Since 1/N ≫ 1/M (e.g., 1/8 ≫ 1/256), each sampled negative receives M/N ≈ 32 times more
repulsion than it should.
Concretely, with M = 256 and N = 8: the ideal gradient pushes away from each of 255 negatives
with weight 1/256 ≈ 0.004, producing a near-uniform “repulsion shell.” The realized GRPO gradient
pushes away from 7 specific negatives with weight 1/8 = 0.125—a 32× amplification on these 7
directions and zero repulsion on the remaining 248. This is not just noisy; it is anisotropic because
the 7 sampled negatives determine a specific (random) subspace of the off-manifold space. Over
multiple steps, the policy learns to avoid the specific outputs it has encountered rather than moving
away from the off-manifold region as a whole, causing Lazy Likelihood Displacement [Deng et al.,
2025]: the likelihood of the correct answer decreases because the policy wastes capacity actively
suppressing a few sampled negatives rather than uniformly distributing mass away from the invalid
region toward M.

Connection to LLD. Deng et al. [2025] empirically demonstrate that GRPO with negative-only
groups causes the likelihood of correct outputs to decrease even when they are not sampled—a
phenomenon they term Lazy Likelihood Displacement. Our analysis provides the mechanism: the
sparse negative gradient creates an anisotropic finite-sample repulsion field that displaces mass non-
uniformly, inadvertently reducing πθ (y + ) for correct outputs that happen to share parameter-space
structure with the over-penalized negatives.

B.5   Optimizer Momentum Drift (Mechanism)

Even in groups where all advantages are zero (the ∼97% zero-gradient groups under binary rewards),
stateful optimizers like AdamW continue to update parameters due to accumulated momentum. The
following proposition is a direct unrolling of the AdamW recursion under a run of zero gradients, not
a deep result; we label it as a proposition to emphasize that its content is mechanistic.
Proposition B.4 (AdamW Momentum Drift under Zero Gradients). Consider AdamW with mo-
mentum coefficients (β1 , β2 ) and weight decay λ. Suppose at step t, the GRPO gradient is gt = 0
(all-zero advantages from a zero-hit group). The parameter update is nonetheless:
                                                            β1 mt−1
                              θt+1 = (1 − λη) θt − η · p                                         (17)
                                                            β2 vt−1 + ϵ
where mt−1 , vt−1 are the first and second moment estimates from previous steps. After τ consecutive
zero-gradient steps:
                                  mt+τ = β1τ mt , vt+τ = β2τ vt                                 (18)


                                                 15
The accumulated parameter displacement is:
                                          τ                    τ −1
                                               βsm
                                              p s1 t
                                          X                    X
                               ∆θτ = −η                   − λη      θt+s                          (19)
                                          s=1
                                               β2 v t + ϵ      s=0
                                                                                          √
                                         the per-step displacement uses the ratio r ≡ β1 / β2 .
Since β1 < β2 (typically 0.9 vs. 0.999), √
                                                                                    P∞ s
With β1 =0.9, β2 =0.999 we get r = 0.9/ 0.999 ≈ 0.9005, so the geometric series s=1 r =
r/(1−r) ≈ 9.05. Substituting and absorbing the constant:
                                               η           mt
                         ∥∆θτ ∥momentum ≈              √          · (1 − β1τ ) ,                  (20)
                                             1 − β1        vt + ϵ
recovering the standard "∼ 1/(1 − β1 ) ≈ 10 momentum-equivalent steps of post-signal drift" rule of
thumb.

Proof. At step t + 1 with gt+1 = 0:
                                mt+1 = β1 mt + (1 − β1 ) · 0 = β1 mt                              (21)
                                vt+1 = β2 vt + (1 − β2 ) · 0 = β2 vt                              (22)
The AdamW update (decoupled weight decay) is:
                                                                      
                             mt+1                       β1 mt
           θt+1 = θt − η √             + λθt = θt − η √            + λθt                          (23)
                             vt+1 + ϵ                   β2 v t + ϵ
The momentum term mt retains the direction of the last nonzero gradient. If the last informative
gradient was an anisotropic sparse-sampling gradient (Theorem B.3), then the momentum drift
continues to push the policy in that direction for ∼ 1/(1 − β1 ) = 10 additional steps even without
any new learning signal.
Simultaneously, the weight decay term −ληθt shrinks all parameters toward zero uniformly, which
further erodes the on-manifold capability that the SFT phase established. This is the mechanism
identified by Xu [2026] as “optimizer-induced low-dimensional drift”: the parameters evolve along
a low-rank manifold determined by historical gradients, even when current gradients carry no task-
relevant information.

Combined pathology. In a typical training step with pM = 1/256 and N = 8: (1) ∼97% of groups
produce zero gradient and contribute only momentum drift; (2) the ∼3% of groups with a valid sample
produce a gradient with 32× concentrated repulsion on 7 specific negatives; (3) the momentum from
these anisotropic gradients persists for ∼10 steps of zero-gradient updates. The net effect is a policy
that slowly drifts away from the SFT-initialized manifold along directions determined by a handful of
over-penalized negatives.

B.6   Self-Reinforcing Collapse (Sketch)

Proposition B.5 (Collapse Dynamics, Informal). Under the combined action of sparse-sampling
distortion (Theorem B.3) and momentum drift (Proposition B.4), and assuming that pM (θ) is locally
L-Lipschitz in policy parameters, the system enters a self-reinforcing decrease of the on-manifold
mass:

      1. Likelihood displacement: Biased repulsion gradients reduce πθ (y + ) for correct outputs
         that share parameter-space structure with over-penalized negatives (LLD).
      2. Manifold erosion: Momentum drift during zero-gradient steps moves the policy away from
         the SFT manifold, reducing pM .
      3. Starvation amplification: Reduced pM increases the fraction of zero-gradient groups
         (Theorem B.1), lengthening drift episodes and further amplifying distortion.
                         (0)   (1)
The expected sequence pM , pM , . . . exhibits a monotone decreasing trend with attractor p∗ = 0.


                                                  16
                    (k)
Sketch. Let pk = pM , and let τk = 1/(N pk ) be the expected inter-arrival of informative groups.
During τk zero-gradient steps, AdamW momentum drift accumulates parameter displacement
                                                mt                         1
                          ∥∆θ∥drift ≤ Cm η √           ,        Cm ≈           .                   (24)
                                                vt + ϵ                  1 − β1
Thus a single zero-gradient burst is geometrically bounded rather than linear in τk , but as pk falls,
such bursts become more frequent and informative hit groups become rarer. Under the local Lipschitz
assumption, the change in on-manifold mass is bounded by |pk+1 − pk | ≤ L · ∥∆θk→k+1 ∥. Taking
expectations and combining the bounded momentum drift with the anisotropic informative-group
gradient (Theorem B.3), we assume a net negative renewal drift
                            E[pk+1 − pk | pk ] ≤ −α ϕ(pk ),           α > 0,                       (25)
for some nonnegative ϕ capturing the increasing zero-gradient frequency and decreasing hit rate as pk
shrinks. This establishes the qualitative self-reinforcing direction toward the absorbing state p = 0,
without claiming a specific square-root collapse law. We label this a sketch rather than a theorem
because (i) the Lipschitz constant L is not directly verifiable, (ii) the directional alignment between
drift and anisotropic finite-sample updates is only established empirically, and (iii) the renewal drift
ϕ is not estimated from first principles. The empirical evidence in Appendix D (seed-pool collapse
under empirical UCB; Freeze-S manifold erosion) is consistent with this sketch.

B.7   Implications for ANCORA

Theorems B.1–B.5 establish three mechanisms by which RL training collapses when pM ≪ 1/N .
The ANCORA framework addresses each:

      1. SFT Warm-Up (Breaking Theorem B.1): Fine-tuning on verified demonstrations raises
         pM from near-zero to a level where N pM ≫ 1, ensuring that most groups contain at least
         one valid sample for positive-advantage gradients.
      2. Pure Binary Rewards (Mitigating Theorem B.3): By using binary rewards R ∈ {0, 1}
         with filtering as accept/reject gating (rather than tiered heuristic scores), zero-hit groups
         produce exactly zero gradient rather than arbitrary off-manifold gradients. This eliminates
         the most damaging source of directional misalignment. Heuristic scores were found experi-
         mentally to harm training—a finding consistent with the LLD analysis of Deng et al. [2025],
         who show that reward noise amplifies likelihood displacement.
      3. UCB-DAG Anchoring (Breaking Theorem B.5): By conditioning generation on verified
         seed specifications, the anchor mechanism constrains exploration to a neighborhood of M
         where valid outputs have higher density (pM ≫ 1/N locally), dramatically reducing the
         fraction of zero-gradient groups and shortening momentum drift episodes. The UCB selec-
         tion further keeps training near the Solver’s capability frontier, while the frontier-targeting
         reward family prevents already-mastered all-pass groups from dominating the Proposer
         update and, depending on the variant, biases the signal toward symmetric uncertainty or
         hard nonzero frontier cases.

C     Homotopy-Continuation Interpretation
This appendix offers a homotopy-continuation reading of the dynamic-curriculum schedule. It is
an interpretation, not a convergence theorem: actual training uses AdamW (not Robbins–Monro
step sizes), runs for a finite horizon, has a non-stationary objective driven by the evolving Seed Pool,
and we verify neither Hessian non-singularity along the path nor the regularity assumptions required
by stochastic-approximation guarantees. We retain the framework because the predictor–corrector
intuition organizes several otherwise-disconnected design choices.
Let λ ∈ [0, 1] be a notional curriculum parameter, where λ = 1 corresponds to the full-context
(guided) regime and λ = 0 to the zero-shot (intrinsic) regime, and consider the family of objectives
                             J (θ, λ) = λJguided (θ) + (1 − λ)Jintrinsic (θ).
The dynamic curriculum is heuristically described as stochastic gradient ascent on J (θ, λt ) with
λt → 0; the conceptual content of homotopy continuation is that, under stronger regularity than we
verify, the iterate would track a slowly drifting stationary path.


                                                   17
1. Smooth homotopy path (assumption-level). If Jguided and Jintrinsic are twice continuously
differentiable and the Hessian ∇2θ J (θ, λ) is non-singular along the path, the implicit function
theorem produces a continuous curve θ∗ (λ) from the guided to the intrinsic optimum. We treat this
as a structural hypothesis that motivates the schedule rather than as a verified property of LLM RL.
2. Bias–variance decomposition. Writing θt+1 = θt + ηt ĝt , we decompose the stochastic gradient
relative to the zero-shot target ∇J0 (θt ):




                               ĝt = ∇J0 (θt ) +        bt          + ξt ,
                                     | {z }            |{z}          |{z}
                                         target    annealing bias     noise




where bt := ∇Jλt (θt ) − ∇J0 (θt ) and ξt := ĝt − ∇Jλt (θt ). As λt → 0, continuity of ∇J in
λ implies bt → 0. Under bounded rewards and Lipschitz-smooth policies, {ξt } behaves like a
bounded-variance martingale-difference sequence around the population gradient.
3. ODE-tracking sketch (under     Pstronger assumptions).       If the step sizes additionally satisfied
the Robbins–Monro conditions t ηt = ∞, t ηt2 < ∞ (which AdamW does not, and our finite
                                                 P
training horizon does not need to), the stochastic-approximation theory for slowly varying targets
(e.g., Borkar 2008) would predict that θt tracks the ODE θ̇ = ∇J0 (θ) and converges to its stable set.
In our setting this should be read as a qualitative suggestion rather than a guarantee: it explains why
a slow withdrawal of in-context guidance can succeed in principle, not why our specific 2,000-step
AdamW run does.
Predictor–corrector view. The schedule acts as a predictor–corrector loop: the prompt provides a
coarse “prediction” of the high-reward region, and the gradient updates “correct” the intrinsic policy
to retain this performance once the prompt is withdrawn. Let Sk denote the set of problems solvable
by πθk with probability p > 1 − ϵ. The Proposer’s frontier-targeting reward is zero at degenerate
extremes and positive on uncertain boundary problems: in the main Band-1-of-K instantiation,
Rprop (p) = 1[m = 1] with m = Kp fires on the rare-success band; in the Bernoulli-variance
instantiation, 4p(1 − p) peaks at p = 1/2. Filter-rejected proposals are excluded from the GRPO
group (contributing no gradient), fully-solved proposals yield zero reward (p = 1 =⇒ Rprop = 0),
and unsolvable proposals likewise yield zero. The gradient on the Proposer therefore points towards
the boundary ∂Sk , and as πθ updates and solves boundary problems, Sk expands to Sk+1 , shifting
the reward surface outward. The coupled system is consistent with a path-following dynamic on the
solvable-problem manifold; converting this consistency into a quantitative guarantee is left to future
work.


                                                  18
D     Additional Ablation Studies
D.1   Algorithm Detail

Algorithm 1 ANCORA: One Training Iteration
 1: Input: Policy πθ , Verifier V, Seed Pool DAG S, Batch B, Specs/prompt N , Solutions/spec K
 2: // Stage 1: UCB Seed Selection                                                       p
 3: Select B seeds from S via UCB tree search (§4.4): roots by µ̂ratchet      i       + c ln Ntot /ni , then
    DAG descent with root quota ρ=0.50. The exploit term µ̂ratchet  i       is the discounted max-ratcheted
    aggregate (ucb_exploit_mode=ratchet); the discounted empirical mean alternative collapses
    substantially earlier in our ablation (Appendix D.5).
 4: // Stage 2: Question Generation (Q-Gen; Proposer Rollout)
 5: for each seed xseed do
 6:    Construct 1-shot prompt from xseed ; sample N candidate specs {x1 , . . . , xN } ∼ πθ
 7:    Run 3-stage filter (structural → compiler stub → semantic heuristics) on each xj
 8:    Discard rejected candidates {No reward signal; excluded from GRPO group}
 9: end for
10: // Stage 3: Solution Generation (S-Gen; Solver Rollout)
11: for each valid spec xj do
12:    Sample K solutions {yj,1 , . . . , yj,K } ∼ πθ (· | xj ); verify cj,k = V(xj , yj,k ) ∈ {0, 1}
13: end for
14: // Stage 4: CoupledP MLRL Advantage Computation
15: Proposer: mj =         k cj,k ; Rprop (xj ) = 1[mj = 1] {Eq. 4; Band-1-of-K}
                         1
                             P                                   R (xj )−R̄prop
16:          R̄prop = |Gq | x∈Gq Rprop (x); Aprop (xj ) = propR̄prop     +ϵ
                                                                                 {Mean-normalized among
    valid specs}
                               cj,k −c̄j
17: Solver: Asolve (yj,k ) = c̄ +ϵ {Mean-normalized MLRL estimator}
                                  j
18: // Stage 5: Joint Policy Update
19: Broadcast Aprop and Asolve to proposer/solver response tokens
20: Compute generated token counts TQ , TS ; rescale by scaleQ = (TQ + TS )/(2TQ ) and scaleS =
    (TQ + TS )/(2TS )
21: Apply static branch weights wQ = 0.375 for Q-Gen and wS = 1.0 for S-Gen; single gradient
    step on πθ
22: // Stage 6: Seed Pool Absorption & Pruning
23: Absorb: Add novel verified specs as children of their seed parent (linkage expansion for diversity)
24: Prune: Deduplicate near-duplicate nodes (MinHash); an optional long-horizon cleanup of dead-
    end nodes is available but not triggered in our main run (Appendix G.9). Backpropagate reward
    along UCB path


D.2   Training Diagnostics

The main text focuses on benchmark performance and the coupled-branch ablation. Figure 5 reports
lower-level diagnostics for the first 1,500 RL steps of the same main Band-1-of-K run; the final
n=100 benchmark evaluation at step 2,000 is the headline number reported in Table 2. The Q-Gen
valid specification rate remains broadly stable despite exploration, and the test-time-training Seed
Pool DAG grows monotonically from 436 filtered evaluation roots to 1,258 nodes by step 1,500, with
all 822 novel nodes having been solved at least once before admission. This 436-root TTT pool is the
filtered union of benchmark roots used for the TTT run, separate from the 234 filtered Dafny2Verus
roots used for the Transfer setting. The gradient norm fluctuates after initial transients rather than
serving as a primary performance metric; we therefore treat it as a stability diagnostic rather than a
main-result claim.

D.3   Proposer Reward Variant Ablation

We compare the three bounded Proposer rewards introduced in Eq. 3 under matched seed pool, UCB
hyperparameters, and Solver checkpoint: (1) Band-1-of-K 1[m=1] (Eq. 4), (2) Bernoulli variance
4p(1−p), and (3) Exponential decay e−Kp − e−K . Bernoulli variance is the symmetric uncertainty


                                                    19
                       (a) Q-Gen Valid Rate (%)                           (b) Seed Pool Size                         (c) Gradient Norm
             100
                                                            1,200
                                                                                                          20
                  80                                        1,000

                                                             800                                          10
                  60
                                                             600

                  40                                          400                                         0
                               0     500     1,000       1,500        0      500     1,000        1,500          0       500     1,000   1,500

                                   Training Step                            Training Step                               Training Step

Figure 5: Training diagnostics over the first 1,500 RL steps of the canonical 2,000-step run; diagnostic
logging ended slightly before the final n=100 benchmark eval at step 2,000 (Table 2). (a) Q-Gen
valid specification rate (fraction passing the 3-stage filter) fluctuates between 55–88%, reflecting
ongoing exploration near the valid-manifold boundary. (b) Seed Pool DAG grows from 436 filtered
TTT roots (the union of benchmark roots used for the TTT run) to 1,258 nodes as novel verified
specifications pass the dedup gate. (c) Actor gradient norm remains bounded after initial transients
but is not monotonic; we use it as a stability diagnostic rather than a primary result.


                                     (a) Dafny2Verus Pass@1                                          (b) Actor Gradient Norm

                   60
                                                                                         20
     Pass@1 (%)




                   40
                                                                                   ∥∇∥




                                                                                         10
                   20


                       0                                                                 0
                           0       200     400     600     800      1,000 1,200               0    200         400     600     800   1,000 1,200

                                                    Step                                                               Step

                                                 Band-1-of-K (main)            Bernoulli 4p(1−p)                     Exp Decay


Figure 6: Proposer reward variant ablation on the 234-seed d2v241 pool (identical UCB/SFT; single
run per variant, illustrative only). (a) Dafny2Verus pass@1. In this particular run, Band-1-of-K rises
overall to 62.2% at step 1199 with small checkpoint-level fluctuations; Bernoulli variance 4p(1−p)
plateaus near 58% after step 400; Exponential decay reaches 54% by step 399 and then collapses at
step 699 (49.9% → 17.3%), partially recovering to ∼ 35% without regaining the prior peak — one
instance of the manifold-collapse regime under a reward that over-amplifies zero-success low-pass
(p → 0) specs. (b) Actor gradient norm; the Band run declines toward low single-digit gradient
norms, the denser rewards stay in [10, 20], and the exponential variant spikes to 21 at its collapse step.
Follow-up runs with different surrounding hyperparameters have produced stable trajectories for each
shape, with Bernoulli variance sometimes stronger than Band-1-of-K; the cross-shape ranking under
a controlled sweep remains an open empirical question.


kernel with maximum at p = 0.5; exponential decay is a low-pass stress-test kernel that shifts mass
toward very low empirical pass rates; Band-1-of-K is the concentrated sparse proxy used in the
main run. Figure 6 shows training curves from a single run per variant. We treat these as illustrative
rather than definitive: subsequent runs under different settings of the surrounding hyperparameters
(pass-rate decay, ZPD prior weight, UCB-statistic decay, branch weights) show that each of the
three shapes can both run stably for long horizons and collapse, with Bernoulli variance sometimes
outperforming the Band variant. The robust empirical finding across our runs is that collapse is
possible under any of the three shapes without the manifold-stabilization mechanisms (iterative SFT
+ UCB-DAG), and each of the three can be stabilized by them; the specific curves below show one
particular instance of the collapse regime for exponential decay, not a definitive ranking.


                                                                                20
D.4    ZPD Upper-Margin Clipping (Negative Result)

Beyond the default ZPD window [â, â+δ], we ablated a stricter variant that shrinks the window’s
upper end by a fixed margin u, i.e. hi = min(â+δ−u, 1), hypothesizing that denying the UCB
selector access to near-ceiling seeds would reduce reward-dead proposals and slow Solver entropy
collapse. At u=0.10 (with δ=0.40), at matched step 200 the intervention produces only within-noise
suppression of proposer pass rate (∆qpass =−0.021) and structural similarity (∆qstruct =−0.015),
while imposing a 4–7× cold-start seed-supply deficit: during steps 50–100 the baseline accrues +516
new pool entries (a jackpot admission phase) whereas the clipped variant accrues only +75, and
both runs converge to ∼0.7 new seeds/step thereafter. The knob is also structurally time-limited:
once â > 1−δ+u (here =0.70, crossed near step 150), the clamp min(·, 1) becomes the binding
constraint and the margin has no effect. We report this as evidence that late-stage Proposer drift is not
remediable by narrowing the ZPD window at admission time; the drift originates downstream in the
reward-variance dynamics rather than in the sampling support.


D.5    Exploit-Mode and Crossover: Long-Horizon Stability Ablation

Proposition G.4 analyzes the discounted empirical mean µ̂t (q) = st (q)/nt (q) as the UCB exploit
term. The production code defaults to a max-ratcheted aggregate (ucb_exploit_mode=ratchet).
We ablate the four-cell grid {empirical, ratchet} × {q_crossover_ratio= 0.5, = 0.0}, where
q_crossover_ratio controls the fraction of Proposer rollouts conditioned on two parent seeds
simultaneously (a forced dual-parent “merge A+B” prompt). All other hyperparameters—topology,
admission gates, LR, batch size, discount rates—are matched within the 2×2. We label the four cells
Emp-XO, Emp-NoXO, Ratchet-NoXO, and the main-paper run Main (ratchet+crossover= 0.5 with
the production root quota ρ=0.50, i.e., the same 50%-descent schedule used elsewhere in this paper).
Result: empirical UCB collapses regardless of crossover. Table 4 reports windowed validity, the
collapse onset (first sustained 20-step window with qvalid < 0.30), and end-of-run state. Crossover
acts as a ∼120-step accelerator of an underlying empirical-UCB collapse rather than a necessary
condition: Emp-XO breaks at step 300, Emp-NoXO breaks at step 420, both end in identical end-
states (qvalid <0.10, seed-pool growth frozen, near-zero solver feed). Ratchet-NoXO is the only
no-crossover cell that preserves Q-format validity through the longest training horizon we logged
(∼530 steps).

Table 4: Exploit-mode × crossover ablation (4p1p reward, matched seeds and gates). Collapse onset
= first sustained 20-step window with qvalid < 0.30.
 Run            Exploit / Crossover / Topology   qvalid @[200,300]   qvalid @[400,500]   Collapse onset           End-state
 Emp-XO         empirical / 0.5 / DAG                 0.543               0.184             step 300       dead (qvalid =0.08@568)
 Emp-NoXO       empirical / 0.0 / DAG                 0.708               0.171             step 420       dead (qvalid =0.02@580)
 Ratchet-NoXO   ratchet / 0.0 / DAG                   0.568               0.662           none by 530      stable, qvalid =0.77@528
 Main           ratchet / 0.5 / ρ=0.50 DAG       ≥0.4 throughout          ≥0.4           none by 1,500    stable, 81.5% D2V pass@1



Mechanism (validity-censored reward). Inspection of Emp-XO and Emp-NoXO rollouts at their
respective collapse boundaries shows the same failure signature: > 89% of rejected Q candidates
fail post-parse static filtering ([NO ensures CLAUSE IN SPEC] or implementation-body leakage),
while compiler-stub rejections fall toward zero—i.e., the model emits parseable Verus-flavored
code that lacks the spec contract. Let Vt ∈ {0, 1} denote Q-format validity and Ut ∈ [0, 1] the
uncertainty/difficulty utility (e.g. 4p(1−p)). The bandit reward is the censored product Rt = Vt Ut ,
and Proposition G.4 implicitly assumes Pr(Vt =1 | arm) ≥ α > 0 uniformly. The empirical exploit
term reflects only instantaneous reward, so once Solver updates push the conditioning distribution
into a region where Pr(V =1) is locally lower, the bandit chases the now-higher-mean arms in that
region and stops re-exploring the previously-valid arms; the censored reward dynamics admit a
self-reinforcing drift that empirical statistics cannot dampen. The max-ratcheted alternative is non-
decreasing in observed reward, so previously-valid arms retain their selection priority and the variation
budget ΥT stays bounded. Crossover accelerates the collapse because dual-parent prompts directly
raise Pr(Vt =0 | operator)—the model interprets “merge A+B” as “write a merged implementation”
rather than a new spec—but the underlying drift is a property of empirical UCB applied to a censored
reward.


                                                                21
Caveat: ratchet preserves validity but not output diversity. Ratchet-NoXO is stable on qvalid
but its Proposer entropy contracts hard: HQ falls 1.13 → 0.046 over 530 steps. This is a different
pathology from the empirical-mode validity collapse—the model converges on a narrow valid output
mode rather than drifting off the manifold. The ratcheted aggregate solves the validity question
(Assumption 4 of §G.11) but does not by itself address mode collapse, which would require an
explicit entropy or KL regularizer.
Theoretical fix directions, not enabled in the reported runs. The cleanest theoretical remedy is
either (i) an operator-aware bandit with arm = (seed-path, generation-operator) so crossover can be
learned to be down-weighted by UCB statistics, or (ii) a validity-aware reward RQ = V ·U −λ(1−V )
that supplies a direct corrective gradient on Q-format violations. The production system instead
uses the simpler combination—ratcheted UCB on the censored reward, with crossover = 0.5 and
a balanced root/DAG schedule (ρ=0.50). The within-table cells (run at the same ρ schedule but
stopped earlier) show that the ratchet exploit alone is sufficient for validity stability whether or not
crossover is enabled, while empirical exploit collapses regardless.
Tool-augmented Solver introduces a separate failure mode. Adding verifier-conditioned multi-turn
repair (S-ReAct) on top of the Ratchet-NoXO stable cell does not reproduce the validity collapse of
the empirical cells: through step ∼400 the Q-format rejection rate stays low. However, by step ∼400
a different pathology emerges—compiler-stub rejection climbs to ∼46/64 at step 408 while heuristic
rejections remain near zero. Inspection of repair-turn outputs shows the model generating semantically
reasonable but syntactically broken Verus bodies (type mismatches, malformed quantifier ranges)
that fail compiler verification. We interpret this as the repair turn pushing the Solver branch into a
local mode where post-edit code is plausible-looking but type-incorrect. We therefore do not include
S-ReAct as a method ingredient in the main results; the rescue-rate gains it provides on the Q-Gen
reward proxy do not translate cleanly into stable benchmark performance within our compute horizon,
and the new compiler-rejection drift would need its own validity-shaping mechanism (analogous to
point (ii) above) before being deployed.




D.6   Branch-Balance Failure under Reverse Imbalance (Negative Result)


The token-mass equalization in §4.5 is designed for the regime TS ≳ TQ (Solver implementations
longer than Proposer specs). One of our long-horizon runs (q4p1p, empirical UCB, slow decay)
exposed an opposite regime where this assumption silently flips and the formula becomes anti-
stabilizing.
Signature. After step ∼300 the Proposer drifts off its output contract: the dominant rejection
signal is [NO ensures CLAUSE IN SPEC] (rising from ∼9% at step 100 to >89% by step 568),
with rollouts emitting implementation-style bodies rather than spec targets. q_valid_rate falls
0.61 → 0.08, while the surviving valid Q subset becomes increasingly easy (qpass rises 0.40 → 0.82).
Because invalid Q rows generate long token responses but reach no Solver, TQ stays large while TS
shrinks; the formula yields scaleQ ≈ 0.83, and with static qscale =0.375 the effective Q multiplier
falls from ∼1.4 to ∼0.31, while the effective S multiplier rises to ∼1.9. The branch most needing
repair receives the smallest gradient share.
Remediation directions (not enabled in the main run, since the Ratchet-Band balanced root/DAG
configuration did not enter this regime within our compute budget): (i) impose a rescue floor
wQ ≥ wmin when q_valid_rate falls below a threshold; (ii) replace the token denominator with a
row-count variant, which is insensitive to per-row response length drift; (iii) tie qscale to a moving
estimate of q_valid_rate so the static prior tracks Proposer health. The exploit-mode ablation
(§D.5) shows that this reverse-imbalance pathway is a downstream symptom of validity collapse rather
than an independent driver: both empirical-UCB cells (with and without crossover) eventually enter
the validity bottleneck and therefore eventually trip branch-weight inversion, while the ratchet cell
preserves qvalid and never enters the inverted regime within our compute horizon. The branch-balance
formula is therefore safe whenever the upstream Q-format manifold is preserved by the exploit term,
and the rescue floor remains a defensive measure for runs that may dip into the empirical regime
under different reward shapes.


                                                  22
D.7                         Static vs. Adaptive Branch Weighting

§4.5 introduces two branch-weighting designs after token-mass equalization. The main run uses
a fixed Proposer branch weight wQ = qscale = 0.375; the adaptive alternative equalizes Proposer
and Solver advantage ℓ2 -norms (wQ ∝ r · scaleS ∥US ∥2 /∥UQ ∥2 with target ratio r=0.5, floor
  min
wQ    =0.125). On paper the adaptive scheme is the more direct choice—it targets a constant relative
gradient footprint between the two roles rather than a constant relative weight. Figure 7 compares the
actor gradient norm under the two regimes on otherwise-identical Band-1-of-K training runs.

                                          (a) Full trajectories (log-y)                                         (b) Distribution in overlap window
                      102                                                                           35
                                                                     Static (qscale = 0.375)                                                         Static
                                                                     L2-balance (r = 0.5)           30                                               L2-balance
2 (actor grad norm)




                                                                                                    25
                      101                                                                           20




                                                                                                2
                                                                                                    15
                                                                                                    10
                      100                                                                           5
                                                                                                    0
                             0      500           1000         1500            2000                      0-99     100-199    200-299     300-399     400-437
                                                 Training step                                                        Training-step window



Figure 7: Actor gradient-norm trajectories comparing the two Proposer/Solver branch-weighting
schemes on otherwise-identical Band-1-of-K runs. (a) Full-horizon view (log-y): light traces are
per-step values, solid lines are EMA (α=0.02) for readability. The static run (qscale =0.375) exhibits
a clear long-horizon annealing pattern, with EMA grad-norm descending from ∼ 13 at step 100 to
∼ 5 by step 1500; the ℓ2 -balance run (r=0.5) instead plateaus in the 10–13 band and was halted at
step 437 without settling. (b) Distribution of per-step grad-norm within the overlap window [0, 437],
binned by 100-step windows. The two schemes have comparable early-phase spread, but the static
scheme’s median begins to decline around step 200 whereas the adaptive scheme’s median stays
elevated. Because the adaptive run did not reach a stable regime within our compute budget, we could
not obtain a like-for-like comparison on downstream pass-rate metrics; the stability evidence alone is
load-bearing for the main-experiment choice of the static scheme.


E                       Prompt Templates
E.1                         Proposer System Prompt (Abridged)

The Proposer system prompt enforces a 7-label structured chain-of-thought discipline. The key
elements are shown below (minor formatting details omitted for brevity):
You are an expert Verus (Rust) programmer specializing in formal verification.
Your job is to generate one new curriculum question, not a solution.

Output contract:
- Output exactly one <think>...</think> block followed by one ‘‘‘rust‘‘‘ block.
- The rust block must contain exactly one target item (fn/spec fn/proof fn).
- Do not include a function body.

Reasoning discipline inside <think>:
Use exactly these seven labels in this order:
1. Parent core:     Identify the core objective in plain language.
2. Direction target: Restate the requested direction (up/down).
3. Solver-skill focus: Name the one reusable solver obligation the child should teach.
4. Minimal decomposition: For up, explain why no further decomposition is needed;
                        for down, isolate the smallest blocker subproblem.
5. Stepping-stone rationale: Explain why this child is the right next step.
6. Next-step child choice: Formulate the minimal plan by choosing the best child.
7. Check: Verify the full reasoning chain for consistency.

Hard bans:
- No rename-only mutation.
- No child whose extra property is already implied by the seed.
- No child whose difficulty cannot be tied to a reusable S-Gen proof skill.



                                                                                               23
E.2   Proposer Curriculum Template (Abridged)

The curriculum template provides a seed specification and a direction (up or down), determined
adaptively by the system (§4.2.1):
Below is a seed problem from the existing pool:

‘‘‘rust
{seed_code}
‘‘‘

Direction: {direction}

Task:
- Generate one new Verus target item that is a plausible next curriculum step.
- Make one focused semantic change rather than a rename or superficial mutation.
- If Direction: up, keep the parent family and add one minimal semantic extension.
- If Direction: down, keep the parent family and expose one smaller
  blocker-focused stepping stone.
- The new difficulty must correspond to one reusable solver skill.




F     Qualitative Examples from Late-Stage Rollouts
To verify that longer late-stage responses correspond to meaningful reasoning rather than degenerate
repetition, we manually inspected solved long responses from the rollout log at training step 1422.
In this batch, the response-length distribution had median 1283 characters, 90th percentile 1750
characters, and maximum 3431 characters. The longest solved responses were generally well-formed
proof-oriented explanations paired with concise Verus implementations, rather than the pathological
repetition patterns observed in some earlier unstable phases.

F.1   Abridged Solver CoT Examples

Example A: Minimum Second Value Subject to a Threshold Constraint. The following is an
abridged excerpt from a solved long response (step 1368, sample 190):
The function returns a value ‘first_of_min_second‘ that satisfies the
postcondition. Specifically, it returns an index ‘i‘ such that
‘0 <= i < s.len()‘ and ‘first_of_min_second == s[i as int][0]‘,
and it satisfies the universal postcondition that for all indices ‘j‘,
either ‘s[i as int][1] <= s[j as int][1]‘ and
‘s[i as int][0] > threshold‘, or ‘i == j‘.
</think>

‘‘‘rust
let mut min_index: usize = 0;
    for i in 1..s.len()
        invariant
            1 <= i <= s.len(),
            min_index < i,
            forall|j: nat| 0 <= j && j < i ==>
                s[min_index as int][1] <= s[j as int][1]
                && s[min_index as int][0] > threshold,
            1 <= i <= s.len(),
            forall|i: nat| i < s.len() ==> s[i as int].len() >= 2,
            forall|i: nat| i < s.len() ==>
                s[i as int][1] <= s[i as int][1]
                && s[i as int][0] > threshold,
        decreases s.len() - i
    {
        if s[i][1] < s[min_index][1]
            || (s[i][1] == s[min_index][1] && s[i][0] > s[min_index][0])
        {
            min_index = i;
        }
    }
    s[min_index][0]
}
‘‘‘

This function initializes ‘min_index‘ to 0 and iterates over the rest
of the vector, updating ‘min_index‘ whenever it finds a pair of indices
‘i‘ and ‘j‘ where ‘s[i][1] < s[j][1]‘ or
‘s[i][1] == s[j][1] && s[i][0] > s[j][0]‘. The postcondition is



                                                    24
maintained through modifications to ‘min_index‘ within the loop, and
the function returns ‘s[min_index][0]‘ after completion.



Example B: Minimum-Length Nonempty Sublist. The following is another abridged excerpt
from a solved long response (step 1413, sample 253):
The function returns a vector ‘min_sublist‘ such that:
- ‘min_sublist.len()‘ is less than or equal to the length of some
  element in ‘s‘.
- There exists an index ‘i‘ with ‘0 <= i < s.len()‘ where
  ‘min_sublist.len()‘ equals the length of ‘s[i]‘.
- For all indices ‘i‘ with ‘0 <= i < s.len()‘, ‘min_sublist.len()‘
  is less than or equal to the length of ‘s[i]‘.
- The function satisfies all preconditions.
</think>

‘‘‘rust
let mut min_sublist: Vec<int> = s[0].clone();
    for i in 1..s.len()
        invariant
            1 <= i <= s.len(),
            0 <= i,
            i <= s.len(),
            min_sublist.len() <= s[0].len(),
            exists|k: int| 0 <= k && k < i as int
                && min_sublist.len() == s[k].len(),
            forall|j: int| 0 <= j && j < i ==>
                min_sublist.len() <= s[j].len(),
            s.len() > 0,
        decreases s.len() - i
    {
        if s[i].len() < min_sublist.len()
        {
            min_sublist = s[i].clone();
        }
    }
    min_sublist
}
‘‘‘

This function initializes ‘min_sublist‘ with the first vector in ‘s‘
and iterates over the rest, updating the invariant to maintain
correctness. The loop maintains the existence of a valid candidate
by updating ‘min_sublist‘ only when a shorter sublist is found.



F.2   Interpretation

These late-stage solved examples support two qualitative observations:

      1. Longer responses are not necessarily pathological. In late training, some increase in
         response length reflects explicit invariant narration and postcondition checking rather than
         raw repetition.
      2. The dominant style is “spec recap + invariant-driven implementation + brief proof
         sketch.” This is consistent with the intended solver behavior in ANCORA, where reusable
         proof obligations are surfaced explicitly.

At the same time, these examples also show that the model often produces over-explained solutions.
The extra length typically comes from rephrasing the same postcondition in prose before and after
the code, rather than from discovering substantially new proof content.

G     Curriculum Bandit Analysis: Discounted UCB on a Lipschitz DAG
This appendix formalizes the curriculum explorer used by ANCORA as a non-stationary discounted-
UCB problem on a Lipschitz arm space, and derives a surrogate regret object that the implementation
qualitatively targets. A flat epochized UCB1 framing over an active set Ve would make the vanilla
bound vacuous because the online system grows its arm set at every step (Ke linear in T ). The
genuine mathematical object exercised by the production implementation is a discounted UCB
recursion on arms that live in an ϵ-packing of a similarity metric space, with solved-only admission


                                                      25
guaranteeing boundedness of rewards and with topological hard-keep restricted to being an optional
long-horizon cleanup policy rather than a load-bearing theoretical primitive. The rest of this appendix
makes each of these claims precise and gives the corresponding qualitative regret scaling.

G.1   Objective and Teacher Utility

The outer objective of the curriculum RL system is solver improvement,
                                                                       
                        J(π) = τT − τ0 ,      τt = Eq∼Dtest Pass(St , q) ,                          (26)
where St denotes the solver at step t. Since a UCB analysis requires a bounded per-rollout reward
signal, we introduce a surrogate teacher utility
                                                     (p − τ )2
                                                              
                         uτ (p) = 4 p(1 − p) exp −               ∈ [0, 1],                    (27)
                                                       2σ 2
where p is the rollout pass-rate of the generated question and τ is the current solver-ability estimate.
The factor 4p(1 − p) favors ZPD-edge questions (maximum at p = 21 ); the Gaussian localizes
around the frontier; and the normalization uτ ∈ [0, 1] is what the analysis consumes. The reward
multiplexer q_reward_mode=band_1of8 replaces 4p(1 − p) with its sparse quantile variant, and
q_reward_mode=exp_decay with a monotone frontier kernel; both remain in [0, 1], so the surrogate
scaling below is unchanged under any of these choices.

G.2   Solved-only Admission and Metric Arm Space

Let X be the space of candidate Verus specifications and let d : X × X → [0, 1] be the MinHash128
Jaccard distance used by SeedPoolManager.question_similarity. The admission rule of
SeedPoolManager.add_seed only inserts q ∈ X if the trainer stored a non-empty best_ans
string for q; best_ans is only set when strict_pass=True on at least one solver rollout of q.
Lemma G.1 (Solved-only admission invariant). Let Pt ⊂ X be the seed pool at step t, and let
Ptext ⊂ Pt be the subset of non-original nodes admitted after step 0. Then every q ∈ Ptext has been
solved at least once by St′ for some t′ ≤ t. The per-arm reward variable R(q) ∈ [0, 1] is bounded
for every q ∈ Pt (both extended and original), but strict-positivity of the current-model pass-rate
statistic is guaranteed only on Ptext : original root anchors are loaded with pass_rate= 0 under the
fresh-start reset in SeedPoolManager._load_from_file (invoked with reset_pass_rate=True
on cold start) and acquire positive statistics only after visitation by the current solver.

The lemma follows from the trainer-side admission guard, which only inserts new non-original nodes
for which best_ans is non-empty; best_ans is in turn only set inside the strict_pass=True
branch of the solver-verification loop. Its consequence for the regret analysis is that admission itself—
rather than arm retirement—ensures every non-original arm carries bounded reward R(q) ∈ [0, 1]
with a strictly positive historical pass, so no separate retirement lemma is required.
Lemma G.2 (ϵ-packing of the pool). Let ϵ = 1 − max_pool_sim. For every t and every q, q ′ ∈ Pt
with q ̸= q ′ , d(q, q ′ ) > ϵ. Consequently |Pt | ≤ N (X , d, ϵ/2), the ϵ/2-covering number of (X , d).

Proof. The admission gate SeedPoolGate.check(..., max_pool_sim) rejects any candidate
whose maximum Jaccard similarity to the current pool exceeds max_pool_sim, i.e., whose Jaccard
distance to at least one existing member is ≤ ϵ. Hence accepted pool elements are pairwise separated
by more than ϵ, so Pt is an ϵ-packing. The standard packing-covering inequality bounds the maximum
size of an ϵ-packing by the ϵ/2-covering number.

Under our configuration, max_pool_sim = 0.72, so ϵ = 0.28; empirically |P200 | ≈ 690, which is
compatible with the covering-number bound as long as N (X , d, 0.14) is of this order. The Lipschitz
arm-space bandit literature Kleinberg et al. [2008] shows that all subsequent regret analysis depends
on X only through the relevant covering number.

G.3   Discounted UCB Recursion

For analysis we collapse the production DAG traversal into a node-level discounted-UCB surro-
gate that treats each q ∈ Pt as a single arm pulled with a global UCB index. The production


                                                  26
SeedPoolManager.ucb_sample routine refines this surrogate into hierarchical root/stay/child ac-
tions with parent-local visit denominators and several bounded additive priors; these deviations are
catalogued in §G.12 and do not invalidate the qualitative regret object derived below.
At step t, the explorer maintains for each arm q ∈ Pt a discounted visit count nt (q) and discounted
reward sum st (q) with decay γUCB ∈ (0, 1) (Hydra: ucb_stat_decay, value 0.995 in our main
configuration):
         nt+1 (q) = γUCB nt (q) + 1[At = q],               st+1 (q) = γUCB st (q) + Rt 1[At = q].       (28)
The discounted empirical mean is µ̂t (q) = st (q)/nt (q), and the discounted UCB index is
                                          s
                                              log ntot
                                                    t
                                                                     X
                   Ut (q) = µ̂t (q) + c                ,     ntot
                                                               t =       nt (q),                        (29)
                                               nt (q)
                                                                           q∈Pt

with c = ucb_c = 2.5. The effective window of the discount is τγ ≡ 1/(1 − γUCB ) =
200 steps—each arm’s statistics geometrically forget observations older than τγ . The imple-
mentation in SeedPoolManager.decay_pass_rates multiplies visit_counts, value_sums,
stay_visit_counts, edge_visit_counts and _total_visits by γUCB at the end of every
step, which realizes (28) exactly.
Crucially, we use the discount rate ucb_stat_decay only as a bandit non-stationarity knob: the
trainer tracks a separate forgetting rate pass_rate_decay (default 0.996) for its operational model
of solver ability, so that the two decays can be tuned independently.

G.4    Two-Gate Bounded Reward

Given a candidate x with rollout pass-rate p(x), the trainer assigns the two-gate reward
                                                                
               Rt (x) = H(x) (1 − β) uτt (p(x)) + β A(x) ,              0 ≤ β ≤ 0.1,                    (30)
where H(x) ∈ {0, 1} is the reusable hard gate (struct-sim < 1, non-duplicate) and A(x) ∈ {0, 1}
is the pool-admission gate. Boundedness Rt ∈ [0, 1] is the only property the surrogate argument
exploits. The β-mixing keeps credit flowing to productive intermediate nodes even when rollouts
score uτ = 0 but still successfully admit a novel seed. We emphasize that Rt (x) here is the backed-up
reward credited along the sampled path and used to update st (q) in Equation (28); it is distinct from
the selection-time UCB index Ut (q) in Equation (29), and from the bounded additive selection priors
(ZPD kernel, kinship prior, neighborhood cold-start fallback) that the production code adds to Ut but
not to Rt (§G.12). The surrogate argument only requires Rt ∈ [0, 1]; it places no restriction on the
priors attached to Ut beyond boundedness.
After a rollout of depth L along a sampled action path (v0 , a0 ), . . . , (vL , aL ), discounted path backup
credits each ancestor action with
                                  Yi = γ L−i Rt (x),            0 ≤ γ ≤ 1.                              (31)
Because (31) is itself in [0, 1] and is a deterministic function of the rollout outcome, it merely rebrands
the terminal reward at each intermediate node and does not break the bandit structure.

G.5    Piecewise-Stationary Curriculum and Variation Budget

Because the solver St changes from step to step, the expected reward µt (q) = E[Rt | At = q]
is non-stationary. Following Garivier and Moulines Garivier and Moulines [2011], we model this
non-stationarity by a variation budget
                                        T
                                        X −1
                               ΥT =              max        µt+1 (q) − µt (q) ,                         (32)
                                               q∈Pt ∩Pt+1
                                        t=1

which counts the total pointwise drift of the reward landscape over T steps. The curriculum as-
sumption is that µt is piecewise stationary with ΥT -controlled break magnitude, an assumption
satisfied whenever solver improvements are Lipschitz-in-t—e.g., as long as per-step policy updates
are bounded. In particular, we do not assume an exogenous epoch partition; the analysis is phrased
directly against (32).


                                                      27
G.6   Recent-Arm Proxy and Covering Number

Because statistics decay geometrically with rate γUCB , an arm last pulled s steps ago retains a
                   s
discount weight γUCB   in (29). This does not literally make old arms inactive: as nt (q) decays, the
UCB bonus can make a neglected arm attractive again. We therefore use the following recent-arm
count only as an analytical proxy for the finite set that dominates a bounded compute window. Fix a
tolerance δ ∈ (0, 1) and define the δ horizon
                                        log(1/δ)              τδ
                                 τδ =               ⇐⇒       γUCB ≤ δ,
                                        1 − γUCB
so that an observation older than τδ retains discount weight at most δ. The natural-time scale
τγ = 1/(1−γUCB ) corresponds to δ = e−1 ≈ 0.37, which is not small; we therefore quote scalings
parametrized by δ and instantiate them with a moderately small choice, e.g. δ = e−3 ≈ 0.05 giving
τδ ≈ 3τγ . Let
               Kγ (δ) = sup {q ∈ Pt : q has been pulled within the last τδ steps} .
                           t≤T

If the per-step branching factor of seed insertion is bounded by B (Hydra: q_gen_n, value 8), each
step can activate at most B fresh arms; combined with Lemma G.2 this gives:
                                                                                          
Corollary G.3 (Recent-arm count, δ-tolerance). Kγ (δ) ≤ min B τδ , N (X , d, ϵ/2) . With B = 8,
τγ = 200, ϵ = 0.28 and the choice δ = e−3 (so τδ ≈ 600), this gives Kγ (δ) ≤ 4800 independent of
the horizon T . The bound is qualitative: δ trades off the looseness of the effective-set approximation
against the size of τδ , and the bound below should be read with this δ-dependence in mind.

G.7   Main Surrogate Scaling: Discounted UCB

Proposition G.4 (Surrogate discounted-UCB scaling on a Lipschitz DAG). Fix δ ∈ (0, 1). Un-
der Lemmas G.1–G.2, the variation budget (32), and the recent-arm proxy of Corollary G.3, the
discounted-UCB sampler (28)–(29) with discount γUCB = 1 − 1/τγ motivates the following gap-
independent surrogate scaling, for some universal C1 , C2 > 0:
                                  s
                                     Kγ (δ) T log T            ΥT
               E[Reg(T )] ≲ C1                        + C2           + O(δ T ).          (33)
                                       1 − γUCB             1 − γUCB
The O(δT ) slack records the cost of using a recent-arm proxy rather than the literal decayed-UCB
active set. We state this as a surrogate scaling rather than a literal theorem: the underlying Garivier–
Moulines (2011) result is for a fixed-cardinality finite arm set, while our active arm set is a growing
metric ϵ-packing and neglected arms are not truly removed from the UCB index.

Heuristic derivation. This adapts the gap-independent discounted-UCB scaling of Garivier–Moulines
(2011) to our setting. Their finite-arm result places the arm count inside the square root for a
fixed cardinality K. We replace K by the recent-arm proxy Kγ (δ) of Corollary G.3. This is an
approximation: arms not pulled within τδ steps have old observations downweighted by at most
δ, but their UCB bonus can still make them selectable, so the proxy should be read as a finite-
budget diagnostic rather than a literal runtime truncation. The arm space being a metric ϵ-packing
rather than a flat discrete set is handled by the zooming argument of Kleinberg–Slivkins–Upfal
(2008, Theorem 3.1): the per-step regret against the continuous optimum is dominated by the
covering number N (X , d, ϵ/2), which is absorbed into Kγ (δ) by Lemma G.2 and Corollary G.3.
Boundedness Rt ∈ [0, 1] needed for Hoeffding concentration is furnished by Lemma G.1 and the
gating construction (30). A fully rigorous transfer would additionally require quantifying the bias
introduced by the time-varying active arm set; we leave this to future work and read (33) as a
qualitative scaling rather than a sharp inequality.

Interpretation. Pluggingpin τγ = 200 at δ = e−3 (so τδ ≈ 600, Kγ (δ) ≤ 4800) and T = 2000
yields a dominant term C1 4800 · 2000 · log(2000)/0.005 ≈ 1.2×105 · C1 , with truncation slack
O(δT ) ≈ 100. We stress that this numerical evaluation is not a useful per-step regret guarantee at
our compute horizon. The load-bearing content of the bound is therefore qualitative: (i)√it replaces
lifetime arm count |PT | with a recent-arm/covering proxy, (ii) its T -dependence is Õ( T ) rather


                                                   28
than the linear-in-T regret of unanchored exploration, and (iii) it tolerates the empirical growth |Pt |:
234 → 690 we observe across 200 steps, as long as the admission gate continues to enforce the
packing invariant.

G.8    Arm Merging and Depth Cap as Lipschitz Operations

Two operations further compress the arm space without invalidating Proposition G.4.
Absorb (mcts_absorb_sim_threshold). When a child q ′ of q has d(q, q ′ ) ≤ 1 − ρ with ρ =
mcts_absorb_sim_threshold = 0.60, the child statistics are merged into the parent. Since d is
a metric (MinHash Jaccard over 128 permutations), triangle inequality gives |µt (q) − µt (q ′ )| ≤
L · d(q, q ′ ) for any L-Lipschitz reward model; absorb therefore introduces a bounded bias ≤ L(1 − ρ)
per merge event, which is absorbed into C1 .
Depth cap (mcts_depth_cap). Hard-capping rollout depth at D = 6 bounds the path-backup
exponent in (31) and keeps the per-step expected reward in [0, 1]. The cap does not affect the UCB
analysis—it only affects the mapping from rollouts to arm pulls.
Symmetric crossover (q_crossover_ratio=0.5). Secondary crossover credit adds a second,
symmetrized backup path per rollout. Because both paths still land in [0, 1], the analysis is unchanged;
the constant C1 grows by a factor of at most two.

G.9    Optional Long-horizon Cleanup: prune_unsolvable

Note that prune_unsolvable is not load-bearing in the main theorem. It performs an optional
garbage collection of nodes with cumulative discounted visits ≥ mcts_prune_min_visits =
20 that are also non-original and lie outside HardKeep. Since admission is already solved-only
(Lemma G.1), the pool never contains the no-signal arms that pruning was originally designed to
remove; empirically prune_unsolvable fires zero times in our main run across 200 steps. We keep
it available as a long-horizon sanity cleanup but no longer attribute regret consequences to it.

G.10    Lower Bound

Theorem G.5 (Minimax
                   p lower
                         bound). Any algorithm for the problem class of Sections G.2–G.5 has
worst-case regret Ω Kγ T .

Proof. Our problem class contains the special case ΥT = 0, γUCB → 1, with Kγ arms that never
           p This is the finite stochastic Kγ -armed bandit with rewards in [0, 1], for which the
absorb or merge.
standard Ω( Kγ T ) lower bound holds Auer et al. [2002].

G.11    Assumptions Actually Used

Proposition G.4 relies on five assumptions, each verified against the production code path:

1. Boundedness (Rt ∈ [0, 1]): enforced by the two-gate construction (30); the three
   q_reward_mode variants (band_1of8, 4p1p, exp_decay) each return values in [0, 1].
2. Solved-only admission (Lemma G.1): enforced by the best_ans guard in the trainer admission
   path, combined with the strict_pass requirement of the solver-verification loop.
3. ϵ-packing (Lemma G.2): enforced by SeedPoolGate.check with the dedup thresh-
   olds specified in our main configuration (max_pool_sim=0.72, max_sibling_sim=0.55,
   duplicate_struct_sim_threshold=0.90).
4. Piecewise stationarity with variation budget ΥT : not verifiable from code alone; this is an
   assumption on the solver learning dynamics, equivalent to requiring that policy updates do not
   induce unbounded drift between successive steps. Empirically τ̂t = s_ability_ema evolves
   slowly (per-step changes < 0.05 in the first 200 steps), giving an order-of-magnitude check
   ΥT ≲ 10 in our main run. The ablation in §D.5 shows that this assumption is not automatic:
   replacing the max-ratcheted exploit term with the discounted empirical mean µ̂t (q) raises ΥT
   enough to trigger Proposer drift within 300 steps, confirming that Assumption 4 is load-bearing
   and that the ratchet choice is the practical mechanism enforcing it.


                                                   29
5. Recent-arm proxy: Kγ (δ) is an analytical proxy, not a runtime truncation. Older arms have
   geometrically decaying statistics in (29) and may become attractive again through the exploration
   bonus; the O(δT ) term in (33) records this approximation rather than claiming those arms vanish.

The five assumptions above suffice; in particular, no clean epoch partition with UCB statistic resets, no
UCB-LCB certificate for safe retirement, and no central load-bearing role for topological hard-keep
is required for Proposition G.4.

G.12    Production Deviations from the Surrogate

Proposition G.4 analyzes a clean node-level discounted-UCB surrogate: a flat arm set Pt , a single UCB
index Ut (q) with a global visit denominator, and the discounted empirical mean µ̂t (q) = st (q)/nt (q)
as the exploit term. The production selector (SeedPoolManager.ucb_sample) is a constrained
DAG-UCT controller that inherits this surrogate’s regret intuition but deviates from it in six bounded
ways; we list them here so the analysis-to-code correspondence is honest rather than overstated.

1. Hierarchical root/stay/child actions. mcts_select first chooses a root via _root_score
   (global denominator log(_total_visits+1)/(nt (q)+1)), then at each descent step compares
   _stay_score(q) against maxq′ _child_score(q,q’). Stay and child scores use parent-local
   denominators log(nt (qparent )+1)/(nstay  t  (q)+1) and log(nt (qparent )+1)/(nedge
                                                                                     t   (qparent , q ′ )+1)
   respectively, rather than the single ntot
                                           t   of Equation (29).
2. Default ratchet exploit. ucb_exploit_mode defaults to ratchet; our Main run and its
   Ratchet-4p1p variant both run ratchet. The Empirical-Band and Empirical-4p1p ablations override
   to empirical, and both crashed within 300 steps—see the negative ablation in §D.5, which also
   argues that the ratchet choice is the practical mechanism enforcing Assumption (4).
3. Cold-start neighborhood prior. _node_value returns st (q)/nt (q) only on visited arms
   (nt (q)>0); on unvisited arms it falls back through a three-step neighborhood_pass_rate
   chain (own pass_rate → mean child pass_rate → global positive-pass-rate mean → constant
   0.15). The surrogate abstracts this warm-start prior away; in the code it is what allows freshly
   inserted nodes to be selectable before they accumulate backed-up reward.
4. Additive selection priors. Under empirical mode, _exploit returns µ̂t (q)+λZPD ZPD(q, ât );
   and _root_score/_child_score/_stay_score each further add a bounded kinship prior
   λkin µ̄(KinN(q)). These are selection-time bonuses attached to Ut , distinct from the backed-up
   reward Rt of Equation (30). All three priors lie in [0, 1] up to their (bounded) weights.
5. Adaptive difficulty window and root quota. Each step, an α=ucb_root_ratio fraction of
   prompts is reserved for root-level sampling (α = 0.50 in the main run, leaving the other 50% for
   DAG descent), and candidates are restricted to the difficulty window [ât −δZPD /2, ât +δZPD /2]
   around the solver-ability estimate ât . Both constrain the feasible action set; neither alters the arm
   space X or the reward gate, so boundedness and ϵ-packing remain intact.
6. Batch repulsion and descend margin. Within-batch penalties discourage repeated root/edge/stay
   actions, and ucb_descend_margin biases the stay-vs-child comparison by a small additive
   constant. These alter selection probabilities inside a batch but preserve the one-step reward
   boundedness the surrogate argument uses.

All six deviations are bounded admissible perturbations of the surrogate: the hierarchical traversal
reduces to root-level UCB at depth zero, the additive priors are bounded, and the adaptive window
and batch repulsion are feasibility constraints that leave the arm space and the backed-up-reward
gate unchanged. We do not claim these deviations preserve the exact constants in Equation (33);
we claim only that none of them invalidates the qualitative regret object (covering-number-bounded,
variation-sensitive, and sub-linear under bounded ΥT ).

G.13    Closest Implementation Counterparts

For each theory object we give the closest implementation site in qsv/qs_trainer.py. Several
correspondences are approximate rather than literal: the surrogate UCB index uses parent-local
denominators and additive priors in the code (§G.12); the teacher utility uτ is realized as a reward
mode used in backed-up tree reward, separately from the ZPD kernel used as a selection prior; and
solved-only admission is enforced by the trainer-side admission path, not by a single function call.


                                                    30
 Theory object                        Closest implementation site                 Main value
 uτ (p) teacher utility (backed up)   q_reward_mode, used in tree_reward backup   band_1of8
 ZPD selection prior                  SeedPoolManager._zpd_exploit                σ = 0.15, λZPD via zpd_prior_weight
 Discount recursion (28)              SeedPoolManager.decay_pass_rates            γUCB = 0.995
 UCB index (29) (surrogate)           _root_score/_child_score/_stay_score        c = 2.5
 Root quota / DAG-descent split       ucb_root_ratio in ucb_sample                0.50/0.50
 MinHash Jaccard metric d             SeedPoolManager.question_similarity         128 perms
 Solved-only admission (Lemma G.1)    trainer-side admission path                 strict_pass only
 ϵ-packing gate (Lemma G.2)           SeedPoolGate.check                          ϵ = 0.28
 Effective horizon τγ                 1/(1 − γUCB )                               τγ = 200
 Branching bound B                    q_gen_n                                     B=8
 Two-gate reward (30)                 pool_admit_bonus controls β                 β = 0.1
 Arm-merging (absorb)                 mcts_absorb_sim_threshold                   ρ = 0.60
 Depth cap                            mcts_depth_cap                              D=6
 Symmetric crossover                  q_crossover_ratio                           0.5
 Optional cleanup (§G.9)              prune_unsolvable(mode="zpd")                never fires in our main run


Plugging these values into Corollary G.3 gives a finite Kγ (δ) independent of T , and Proposi-
tion G.4 yields a sublinear-in-T surrogate scaling for all horizons up to which the ϵ-packing invariant
holds. The scaling rests on the assumptions actually used—boundedness via solved-only admission
(Lemma G.1), the ϵ-packing arm space (Lemma G.2), the piecewise-stationary variation budget
ΥT (32), and the recent-arm proxy that approximates arms outside the last τδ steps—and we do not
claim it follows from the lemmas alone.

NeurIPS Paper Checklist
       1. Claims
          Question: Do the main claims made in the abstract and introduction accurately reflect the
          paper’s contributions and scope?
          Answer: [Yes]
          Justification: The claims match our empirical results in Section 5.
          Guidelines:
             • The answer [N/A] means that the abstract and introduction do not include the claims
                made in the paper.
             • The abstract and/or introduction should clearly state the claims made, including the
                contributions made in the paper and important assumptions and limitations. A [No] or
                [N/A] answer to this question will not be perceived well by the reviewers.
             • The claims made should match theoretical and experimental results, and reflect how
                much the results can be expected to generalize to other settings.
             • It is fine to include aspirational goals as motivation as long as it is clear that these goals
                are not attained by the paper.
       2. Limitations
          Question: Does the paper discuss the limitations of the work performed by the authors?
          Answer: [Yes]
          Justification: Discussed in Section 6 (Conclusion and Discussion).
          Guidelines:
             • The answer [N/A] means that the paper has no limitation while the answer [No] means
                that the paper has limitations, but those are not discussed in the paper.
             • The authors are encouraged to create a separate “Limitations” section in their paper.
             • The paper should point out any strong assumptions and how robust the results are to
                violations of these assumptions (e.g., independence assumptions, noiseless settings,
                model well-specification, asymptotic approximations only holding locally). The authors
                should reflect on how these assumptions might be violated in practice and what the
                implications would be.
             • The authors should reflect on the scope of the claims made, e.g., if the approach was
                only tested on a few datasets or with a few runs. In general, empirical results often
                depend on implicit assumptions, which should be articulated.


                                                              31
     • The authors should reflect on the factors that influence the performance of the approach.
       For example, a facial recognition algorithm may perform poorly when image resolution
       is low or images are taken in low lighting. Or a speech-to-text system might not be
       used reliably to provide closed captions for online lectures because it fails to handle
       technical jargon.
     • The authors should discuss the computational efficiency of the proposed algorithms
       and how they scale with dataset size.
     • If applicable, the authors should discuss possible limitations of their approach to
       address problems of privacy and fairness.
     • While the authors might fear that complete honesty about limitations might be used by
       reviewers as grounds for rejection, a worse outcome might be that reviewers discover
       limitations that aren’t acknowledged in the paper. The authors should use their best
       judgment and recognize that individual actions in favor of transparency play an impor-
       tant role in developing norms that preserve the integrity of the community. Reviewers
       will be specifically instructed to not penalize honesty concerning limitations.
3. Theory assumptions and proofs
  Question: For each theoretical result, does the paper provide the full set of assumptions and
  a complete (and correct) proof?
  Answer: [Yes]
  Justification: Formal claims are stated with assumptions and proofs in the appendix. Informal
  mechanisms and surrogate analyses are explicitly labeled as sketches, interpretations, or
  qualitative scalings, with their assumptions and gaps stated.
  Guidelines:
     • The answer [N/A] means that the paper does not include theoretical results.
     • All the theorems, formulas, and proofs in the paper should be numbered and cross-
       referenced.
     • All assumptions should be clearly stated or referenced in the statement of any theorems.
     • The proofs can either appear in the main paper or the supplemental material, but if
       they appear in the supplemental material, the authors are encouraged to provide a short
       proof sketch to provide intuition.
     • Inversely, any informal proof provided in the core of the paper should be complemented
       by formal proofs provided in appendix or supplemental material.
     • Theorems and Lemmas that the proof relies upon should be properly referenced.
4. Experimental result reproducibility
  Question: Does the paper fully disclose all the information needed to reproduce the main ex-
  perimental results of the paper to the extent that it affects the main claims and/or conclusions
  of the paper (regardless of whether the code and data are provided or not)?
  Answer: [Yes]
  Justification: Training details and dataset information are provided in Section 5.
  Guidelines:
     • The answer [N/A] means that the paper does not include experiments.
     • If the paper includes experiments, a [No] answer to this question will not be perceived
       well by the reviewers: Making the paper reproducible is important, regardless of
       whether the code and data are provided or not.
     • If the contribution is a dataset and/or model, the authors should describe the steps taken
       to make their results reproducible or verifiable.
     • Depending on the contribution, reproducibility can be accomplished in various ways.
       For example, if the contribution is a novel architecture, describing the architecture fully
       might suffice, or if the contribution is a specific model and empirical evaluation, it may
       be necessary to either make it possible for others to replicate the model with the same
       dataset, or provide access to the model. In general. releasing code and data is often
       one good way to accomplish this, but reproducibility can also be provided via detailed
       instructions for how to replicate the results, access to a hosted model (e.g., in the case


                                           32
       of a large language model), releasing of a model checkpoint, or other means that are
       appropriate to the research performed.
     • While NeurIPS does not require releasing code, the conference does require all submis-
       sions to provide some reasonable avenue for reproducibility, which may depend on the
       nature of the contribution. For example
       (a) If the contribution is primarily a new algorithm, the paper should make it clear how
           to reproduce that algorithm.
       (b) If the contribution is primarily a new model architecture, the paper should describe
           the architecture clearly and fully.
       (c) If the contribution is a new model (e.g., a large language model), then there should
           either be a way to access this model for reproducing the results or a way to reproduce
           the model (e.g., with an open-source dataset or instructions for how to construct
           the dataset).
       (d) We recognize that reproducibility may be tricky in some cases, in which case
           authors are welcome to describe the particular way they provide for reproducibility.
           In the case of closed-source models, it may be that access to the model is limited in
           some way (e.g., to registered users), but it should be possible for other researchers
           to have some path to reproducing or verifying the results.
5. Open access to data and code
  Question: Does the paper provide open access to the data and code, with sufficient instruc-
  tions to faithfully reproduce the main experimental results, as described in supplemental
  material?
  Answer: [No]
  Justification: We do not provide anonymized code or data as supplementary material at
  submission time. The paper includes the implementation details, hyperparameters, datasets,
  and evaluation protocol needed to assess the main claims, and we plan to release code after
  review.
  Guidelines:
     • The answer [N/A] means that paper does not include experiments requiring code.
     • Please see the NeurIPS code and data submission guidelines (https://neurips.cc/
       public/guides/CodeSubmissionPolicy) for more details.
     • While we encourage the release of code and data, we understand that this might not
       be possible, so [No] is an acceptable answer. Papers cannot be rejected simply for not
       including code, unless this is central to the contribution (e.g., for a new open-source
       benchmark).
     • The instructions should contain the exact command and environment needed to run to
       reproduce the results. See the NeurIPS code and data submission guidelines (https:
       //neurips.cc/public/guides/CodeSubmissionPolicy) for more details.
     • The authors should provide instructions on data access and preparation, including how
       to access the raw data, preprocessed data, intermediate data, and generated data, etc.
     • The authors should provide scripts to reproduce all experimental results for the new
       proposed method and baselines. If only a subset of experiments are reproducible, they
       should state which ones are omitted from the script and why.
     • At submission time, to preserve anonymity, the authors should release anonymized
       versions (if applicable).
     • Providing as much information as possible in supplemental material (appended to the
       paper) is recommended, but including URLs to data and code is permitted.
6. Experimental setting/details
  Question: Does the paper specify all the training and test details (e.g., data splits, hyperpa-
  rameters, how they were chosen, type of optimizer) necessary to understand the results?
  Answer: [Yes]
  Justification: Hyperparameters, data splits, and optimizers are detailed in Section 5.1.
  Guidelines:


                                           33
      • The answer [N/A] means that the paper does not include experiments.
      • The experimental setting should be presented in the core of the paper to a level of detail
         that is necessary to appreciate the results and make sense of them.
      • The full details can be provided either with the code, in appendix, or as supplemental
         material.
7. Experiment statistical significance
   Question: Does the paper report error bars suitably and correctly defined or other appropriate
   information about the statistical significance of the experiments?
   Answer: [No]
   Justification: We were unable to report error bars due to severe computational constraints.
   Training the 3B model with our RL pipeline on limited resources (2×A100 40GB GPUs)
   is at the absolute limit of our capacity, taking approximately 5 days to complete a single
   2,000-step run, making multiple random seed runs computationally prohibitive.
   Guidelines:
      • The answer [N/A] means that the paper does not include experiments.
      • The authors should answer [Yes] if the results are accompanied by error bars, confidence
         intervals, or statistical significance tests, at least for the experiments that support the
         main claims of the paper.
      • The factors of variability that the error bars are capturing should be clearly stated (for
         example, train/test split, initialization, random drawing of some parameter, or overall
         run with given experimental conditions).
      • The method for calculating the error bars should be explained (closed form formula,
         call to a library function, bootstrap, etc.)
      • The assumptions made should be given (e.g., Normally distributed errors).
      • It should be clear whether the error bar is the standard deviation or the standard error
         of the mean.
      • It is OK to report 1-sigma error bars, but one should state it. The authors should
         preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis
         of Normality of errors is not verified.
      • For asymmetric distributions, the authors should be careful not to show in tables or
         figures symmetric error bars that would yield results that are out of range (e.g., negative
         error rates).
      • If error bars are reported in tables or plots, the authors should explain in the text how
         they were calculated and reference the corresponding figures or tables in the text.
8. Experiments compute resources
   Question: For each experiment, does the paper provide sufficient information on the com-
   puter resources (type of compute workers, memory, time of execution) needed to reproduce
   the experiments?
   Answer: [Yes]
   Justification: Hardware specifications (2xA100) and runtimes are stated in Section 5.1.
   Guidelines:
      • The answer [N/A] means that the paper does not include experiments.
      • The paper should indicate the type of compute workers CPU or GPU, internal cluster,
         or cloud provider, including relevant memory and storage.
      • The paper should provide the amount of compute required for each of the individual
         experimental runs as well as estimate the total compute.
      • The paper should disclose whether the full research project required more compute
         than the experiments reported in the paper (e.g., preliminary or failed experiments that
         didn’t make it into the paper).
9. Code of ethics
   Question: Does the research conducted in the paper conform, in every respect, with the
   NeurIPS Code of Ethics https://neurips.cc/public/EthicsGuidelines?


                                             34
   Answer: [Yes]
   Justification: The research strictly adheres to the code of ethics.
   Guidelines:
      • The answer [N/A] means that the authors have not reviewed the NeurIPS Code of
        Ethics.
      • If the authors answer [No], they should explain the special circumstances that require a
        deviation from the Code of Ethics.
      • The authors should make sure to preserve anonymity (e.g., if there is a special consid-
        eration due to laws or regulations in their jurisdiction).
10. Broader impacts
   Question: Does the paper discuss both potential positive societal impacts and negative
   societal impacts of the work performed?
   Answer: [Yes]
   Justification: The work may improve the reliability of generated code and formal verification
   workflows. Potential negative impacts are indirect and include overreliance on automated
   code-generation systems or misuse of stronger code-generation models; our setting mitigates
   these risks by requiring formal verification feedback and by not releasing high-risk models.
   Guidelines:
      • The answer [N/A] means that there is no societal impact of the work performed.
      • If the authors answer [N/A] or [No], they should explain why their work has no societal
        impact or why the paper does not address societal impact.
      • Examples of negative societal impacts include potential malicious or unintended uses
        (e.g., disinformation, generating fake profiles, surveillance), fairness considerations
        (e.g., deployment of technologies that could make decisions that unfairly impact specific
        groups), privacy considerations, and security considerations.
      • The conference expects that many papers will be foundational research and not tied
        to particular applications, let alone deployments. However, if there is a direct path to
        any negative applications, the authors should point it out. For example, it is legitimate
        to point out that an improvement in the quality of generative models could be used to
        generate Deepfakes for disinformation. On the other hand, it is not needed to point out
        that a generic algorithm for optimizing neural networks could enable people to train
        models that generate Deepfakes faster.
      • The authors should consider possible harms that could arise when the technology is
        being used as intended and functioning correctly, harms that could arise when the
        technology is being used as intended but gives incorrect results, and harms following
        from (intentional or unintentional) misuse of the technology.
      • If there are negative societal impacts, the authors could also discuss possible mitigation
        strategies (e.g., gated release of models, providing defenses in addition to attacks,
        mechanisms for monitoring misuse, mechanisms to monitor how a system learns from
        feedback over time, improving the efficiency and accessibility of ML).
11. Safeguards
   Question: Does the paper describe safeguards that have been put in place for responsible
   release of data or models that have a high risk for misuse (e.g., pre-trained language models,
   image generators, or scraped datasets)?
   Answer: [N/A]
   Justification: No high-risk models or scraped datasets are released.
   Guidelines:
      • The answer [N/A] means that the paper poses no such risks.
      • Released models that have a high risk for misuse or dual-use should be released with
        necessary safeguards to allow for controlled use of the model, for example by requiring
        that users adhere to usage guidelines or restrictions to access the model or implementing
        safety filters.


                                            35
       • Datasets that have been scraped from the Internet could pose safety risks. The authors
         should describe how they avoided releasing unsafe images.
       • We recognize that providing effective safeguards is challenging, and many papers do
         not require this, but we encourage authors to take this into account and make a best
         faith effort.
12. Licenses for existing assets
    Question: Are the creators or original owners of assets (e.g., code, data, models), used in
    the paper, properly credited and are the license and terms of use explicitly mentioned and
    properly respected?
    Answer: [Yes]
    Justification: We cite the creators of Verus, Dafny2Verus, MBPP, and HumanEval, and
    use these assets under their upstream licenses and terms of use. The submission does not
    redistribute these codebases or datasets.
    Guidelines:
       • The answer [N/A] means that the paper does not use existing assets.
       • The authors should cite the original paper that produced the code package or dataset.
       • The authors should state which version of the asset is used and, if possible, include a
         URL.
       • The name of the license (e.g., CC-BY 4.0) should be included for each asset.
       • For scraped data from a particular source (e.g., website), the copyright and terms of
         service of that source should be provided.
       • If assets are released, the license, copyright information, and terms of use in the
         package should be provided. For popular datasets, paperswithcode.com/datasets
         has curated licenses for some datasets. Their licensing guide can help determine the
         license of a dataset.
       • For existing datasets that are re-packaged, both the original license and the license of
         the derived asset (if it has changed) should be provided.
       • If this information is not available online, the authors are encouraged to reach out to
         the asset’s creators.
13. New assets
    Question: Are new assets introduced in the paper well documented and is the documentation
    provided alongside the assets?
    Answer: [N/A]
    Justification: We do not release new datasets or non-code assets.
    Guidelines:
       • The answer [N/A] means that the paper does not release new assets.
       • Researchers should communicate the details of the dataset/code/model as part of their
         submissions via structured templates. This includes details about training, license,
         limitations, etc.
       • The paper should discuss whether and how consent was obtained from people whose
         asset is used.
       • At submission time, remember to anonymize your assets (if applicable). You can either
         create an anonymized URL or include an anonymized zip file.
14. Crowdsourcing and research with human subjects
    Question: For crowdsourcing experiments and research with human subjects, does the paper
    include the full text of instructions given to participants and screenshots, if applicable, as
    well as details about compensation (if any)?
    Answer: [N/A]
    Justification: This research does not involve crowdsourcing or human subjects.
    Guidelines:


                                             36
       • The answer [N/A] means that the paper does not involve crowdsourcing nor research
          with human subjects.
       • Including this information in the supplemental material is fine, but if the main contribu-
          tion of the paper involves human subjects, then as much detail as possible should be
          included in the main paper.
       • According to the NeurIPS Code of Ethics, workers involved in data collection, curation,
          or other labor should be paid at least the minimum wage in the country of the data
          collector.
15. Institutional review board (IRB) approvals or equivalent for research with human
    subjects
    Question: Does the paper describe potential risks incurred by study participants, whether
    such risks were disclosed to the subjects, and whether Institutional Review Board (IRB)
    approvals (or an equivalent approval/review based on the requirements of your country or
    institution) were obtained?
    Answer: [N/A]
    Justification: This research does not involve human subjects.
    Guidelines:
       • The answer [N/A] means that the paper does not involve crowdsourcing nor research
          with human subjects.
       • Depending on the country in which research is conducted, IRB approval (or equivalent)
          may be required for any human subjects research. If you obtained IRB approval, you
          should clearly state this in the paper.
       • We recognize that the procedures for this may vary significantly between institutions
          and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the
          guidelines for their institution.
       • For initial submissions, do not include any information that would break anonymity (if
          applicable), such as the institution conducting the review.
16. Declaration of LLM usage
    Question: Does the paper describe the usage of LLMs if it is an important, original, or
    non-standard component of the core methods in this research? Note that if the LLM is used
    only for writing, editing, or formatting purposes and does not impact the core methodology,
    scientific rigor, or originality of the research, declaration is not required.
    Answer: [Yes]
    Justification: The usage of LLMs (Qwen2.5, Kimi-K2.5, DeepSeek-V3.2) as the core
    reasoning policy and for generating initial demonstrations is fully described in Section 5.
    Guidelines:
       • The answer [N/A] means that the core method development in this research does not
          involve LLMs as any important, original, or non-standard components.
       • Please refer to our LLM policy in the NeurIPS handbook for what should or should not
          be described.




                                             37
