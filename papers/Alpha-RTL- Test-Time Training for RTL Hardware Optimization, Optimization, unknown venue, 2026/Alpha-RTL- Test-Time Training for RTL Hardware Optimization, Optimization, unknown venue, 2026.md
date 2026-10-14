                                            Alpha-RTL: Test-Time Training for RTL Hardware
                                                             Optimization


                                                           Peilong Zhou1,2,3 , Zhirong Chen1,2 , Cangyuan Li1,2 , Haoyu Gao1,2,3 ,
                                                                     Kaiyan Chang1,2 , Ziming Qu1,2 , Ying Wang1,2
                                                              1
                                                                  SKLP, Institute of Computing Technology, Chinese Academy of Sciences
                                            2
                                                University of the Chinese Academy of Sciences 3 School of Advanced Interdisciplinary Sciences
arXiv:2606.05253v1 [cs.LG] 3 Jun 2026




                                                                        Correspondence: wangying2009@ict.ac.cn



                                                                                           Abstract

                                                     Large language models (LLMs) have shown increasing promise in generat-
                                                     ing functionally correct register-transfer-level (RTL) hardware designs. Recent
                                                     LLM-for-RTL systems further improve this ability through Verilog-domain distilla-
                                                     tion, RLVR with automated testbenches, or EDA-integrated reinforcement learning
                                                     with syntax, simulation, and PPA rewards. However, these methods primarily train
                                                     a general RTL generator before deployment, while test-time approaches typically
                                                     search with a frozen policy. We instead perform reinforcement learning at test time,
                                                     allowing the LLM policy to adapt to executable EDA feedback from the specific
                                                     RTL optimization problem. This setting is challenging because candidate designs
                                                     must pass sparse discrete validity gates—syntax checking and simulation—before
                                                     receiving meaningful synthesis-derived feedback on area, timing, or power. We pro-
                                                     pose TTT-RTL, to our knowledge the first per-design test-time training framework
                                                     that closes the loop between an LLM policy and an EDA pipeline for RTL optimiza-
                                                     tion. TTT-RTL samples candidate implementations, verifies them through syntax
                                                     checking and simulation, scores valid designs using synthesis-derived PPA product,
                                                     reuses high-reward variants through a PUCT-indexed design-state pool, and updates
                                                     the policy with an entropic policy-gradient objective. To stabilize policy updates
                                                     under sparse or plateaued reward groups, we introduce an adaptive KL-budget
                                                     controller that adjusts the entropy constraint using reference KL, effective sample
                                                     size, constant-reward fraction, and beta-search saturation. On RTLLM v2.0 under
                                                     Nangate 45 nm, TTT-RTL reduces the geometric-mean PPA product by 65.1% over
                                                     the reference, outperforming the strongest published frozen-policy agent baseline
                                                     under the same reference-normalized metric at 26.1%. On an industrial XuanTie
                                                     C910 FPU leading-zero-anticipation unit under Sky130, TTT-RTL achieves a
                                                     59.4% ADP reduction over the original implementation, and ablations show that
                                                     policy adaptation, state reuse, and KL-budget control each contribute to the gain.
                                                     These results suggest that test-time training with executable EDA feedback can
                                                     move LLM-based RTL generation beyond functional correctness toward physically
                                                     optimized hardware.


                                        1        Introduction

                                        Hardware design is a laborious process whose quality is ultimately judged by physical metrics: area,
                                        clock frequency, and power consumption. Modern EDA flows translate a register-transfer-level
                                        (RTL) description written in Verilog or VHDL into a physical circuit; the resulting PPA product
                                        (Area×Delay×Power, the joint figure of merit used by RTLLM v2.0 reports) depends not only on

                                        Preprint.
the logical correctness of the code but on fine-grained micro-architectural choices— pipeline depth,
operator scheduling, signal encoding—that are difficult to predict without running synthesis.
Recent work has shown that LLMs can generate functionally correct RTL code [Liu et al., 2023b,c,
Blocklove et al., 2023]. These models learn to imitate high-quality Verilog from training corpora,
and when prompted with a hardware specification they can produce designs that pass functional
simulation. However, functional correctness is a necessary but insufficient condition for hardware
quality. A multiplier that passes all testbench cases may still be 30% larger or 30% slower than an
optimized reference implementation. Because physical synthesis metrics are computed by EDA tools
at evaluation time—not during LLM training—existing models cannot learn to minimize the PPA
product.
Existing approaches to optimize RTL fall into two families, each capturing only half of what is needed.
Frozen-LLM search agents—EvolVE [Hsin et al., 2026], VeriAgent [Wang et al., 2026], and the
current SOTA REvolution [Min et al., 2025]—drive an LLM through evolutionary or reflective loops
with synthesis feedback, but the weights never update: search quality is bounded by the unchanged
base policy, and the design knowledge accumulated from EDA tools is discarded the moment the run
ends. Training-time RL methods—ChipSeek [Chen et al., 2025] and EARL [Shi et al., 2025]—do
learn from synthesis signals, but they ship a single amortized policy evaluated under Pass@k: each
candidate is an independent single-shot generation, with no mechanism to feed EDA results from one
attempt back into the next on the same design.
We argue the missing regime is to fuse search into training at test time: given one design and
its reference, run a multi-round search whose every rollout’s EDA feedback updates the model
online for that problem, so the policy itself deepens as the search progresses. Concretely, we treat
Verilog candidates as nodes in a PUCT tree whose every expansion is scored by a three-stage EDA
pipeline (syntax → simulation → synthesis), and we feed that dense physical reward back into online
policy-gradient updates on the same design. The result is a closed loop in which exploration and
training co-evolve under EDA-grounded feedback, rather than search being grafted on top of a frozen
policy. On RTLLM v2.0 this regime substantially outperforms the strongest published agent baseline
on PPA-product reduction, and on a XuanTie C910 industrial floating-point unit it improves over
well-tuned production RTL—we quantify both below.

Contributions.
      1. We formulate per-design RTL optimization as a test-time training problem, fusing
         PUCT-guided search into online policy updates driven by EDA feedback.
      2. We propose TTT-RTL, instantiating this regime with a Verilog state pool, EDA-feedback
         prompting, an entropic advantage estimator, and a three-stage syntax/simulation/ synthesis
         reward, built on verl [Sheng et al., 2024].
      3. On RTLLM v2.0 TTT-RTL covers 48/49 designs and cuts the PPA product by a
         geometric-mean of 65.1% vs. 26.1% for the strongest published agent baseline (REvo-
         lution); on a XuanTie C910 industrial LZA unit it improves over well-tuned production
         RTL by 59.4% ADP at seed 42, with single-seed component ablations isolating the contri-
         bution of the PUCT pool and the entropic estimator.

2     Related Work
2.1   Test-time training and RL with verifiable rewards

Test-time training (TTT) [Sun et al., 2020] updates model parameters at inference time using an
auxiliary self-supervised objective constructed from the test input. Yuksekgonul et al. [2026] extended
TTT to discrete reasoning via PUCT-guided exploration: a verifier scores candidate solutions and
policy-gradient updates improve the generation policy for the specific problem at hand, enabling
LLMs to solve mathematical problems beyond their static training distribution. TTRL [Zuo et al.,
2025] similarly performs test-time RL using majority-vote pseudo-labels on unlabeled data, while
Snell et al. [2024] and Wu et al. [2024] scale test-time compute without updating the model at all.
On the optimizer side, GRPO [Shao et al., 2024] provides the group-relative policy-gradient recipe
we build on, originally developed for verifiable mathematical correctness, and CodeRL [Le et al.,
2022] is the closest precedent in program synthesis, using unit-test pass/fail as the RL reward signal.


                                                  2
2.2   LLMs for RTL and PPA optimization

Verilog generation targeting functional correctness. A growing body of work applies LLMs to
hardware description language generation and evaluates them on open benchmarks. VerilogEval [Liu
et al., 2023b] measures pass rates on 156 HDLBits tasks, while RTLLM [Lu et al., 2024] and its
v2.0 successor OpenLLM-RTL [Liu et al., 2025] extend the setting to larger designs with synthesis
feedback; RTLLM v2.0 is the benchmark we use throughout this paper. On the generation side,
RTLCoder [Liu et al., 2023c], Chip-Chat [Blocklove et al., 2023], ChipNeMo [Liu et al., 2023a], and
BetterV [Pei et al., 2024] fine-tune or steer LLMs for Verilog but target functional correctness only
and do not optimize physical metrics.

Frozen-policy agents for PPA. A more recent line targets physical optimization directly, using
LLMs as frozen components inside a search or multi-agent loop: EvolVE [Hsin et al., 2026] (evolu-
tionary code generation), VeriAgent [Wang et al., 2026] (multi-agent system with synthesis-feedback
critic), REvolution [Min et al., 2025] (population-based search with reflection, current SOTA), and
COEVO [Ping et al., 2026] (co-evolution of correctness and PPA). These four are the headline
baselines for our RTLLM v2.0 comparison; in all cases LLM weights are never updated.

Training-time RL on RTL. ChipSeek [Chen et al., 2025] is the closest RL-based prior work:
it trains RTL-generation models with hierarchical EDA feedback and reports 84.09% Pass@5 on
RTLLM v2.0, with average normalized EDAP reduced to 0.76 in its best configuration. EARL
[Shi et al., 2025] is a concurrent training-time RL method that combines SFT with entropy-aware
DAPO-style updates on verifiable compiler/testbench signals. Both produce an offline, amortized
policy shared across all designs and are evaluated under a Pass@k generation protocol.

Differentiation. Unlike functional-only Verilog generators, frozen-LLM PPA agents whose weights
never update, and offline RL methods that ship a single amortized policy, TTT-RTL combines
EDA-grounded reward with per-design test-time adaptation: each problem triggers its own on-the-fly
policy update driven by a PUCT state pool, with a verifier gated by mixed discrete–continuous
physical metrics rather than scalar pass/fail, and we report coverage and reference-normalized
PPA-product over the full RTLLM v2.0 benchmark rather than Pass@k.

3     Method: TTT-RTL

Figure 1 summarizes the four parts of the closed-loop TTT-RTL pipeline; the rest of this section
formalizes each component.

3.1   Problem Formulation and PUCT-Guided State Sampling

Let P denote an RTL design problem specified by a natural-language description, a functional
testbench, and a reference implementation. A design state s = (v, r, t) consists of a Verilog
implementation v, its reward r, and creation timestep t. The goal is to find a design v ∗ that is
functionally correct and minimizes a target metric M (v) defined in Section 3.3. We initialize a
state pool S with a single root state s0 = (ϵ, 0, −1) (ϵ is an empty implementation), and grow S
iteratively by sampling parents under a PUCT score that balances exploitation (high-reward nodes)
and exploration (rarely-sampled nodes):
                                                                √
                                                                  1+T
                           PUCT(s) = Q(s) + c · σ · P (s) ·              ,                    (1)
                                                               1 + N (s)
where c = 1.0 is the exploration coefficient, T is the total number of expanded parents so far, and
N (s) counts how often s (or any of its descendants) has been expanded. Q(s) is the best one-step
reachable child reward of s for visited states, falling back to R(s) when s has not yet been expanded.
The scale factor σ = Rmax − Rmin is the reward range taken globally over the current pool S, and
P (s) is the normalized linear-rank prior
                                |S| − rank(s)
                P (s) = P                     ′
                                                 ,     rank(s) ∈ {0, . . . , |S| − 1},           (2)
                            s′ ∈S |S| − rank(s )


                                                  3
 Part 1 Problem Assets                                        Part 2 PUCT State Pool +                              Part 3 LLM Rollout +                                       Part 4 Test-Time Policy
                                                                     Prompt Builder                                 EDA Reward Pipeline                                       Update + State Pool Update
          SPEC
                                      PUCT State Pool
                      Design spec                                                                     LLM Rollout Policy
                                      State 1
                                                                    zz
                                                                                    Prompt Builder                     EDA Reward Pipeline                                              GPG Actor Update
                                                              Verilog candidate
                                                                                                                                                      Verilog extraction                 good RTL trajectories
                                                              Syntax/ functional       task spec
                                                                                                                                                                                         bad RTL trajectories
                     Reference RTL    State 2
                                              zz
                                          Reward                                      previous RTL
                                                              PPA metrics
                                                              Verilog candidate
                                          P       P       A
                                                                                                                                                      Syntax check
                                                                                     EDA feedback




                                                                                                                                                  !
                                                              EDA  feedback                           assign lza_result = candidate 1
                                                              Syntax/
                                                                   z z functional                      (b23) ? 5'd0 :
          TB
                                      State 3                                                          ... (b0) ? 5'd23 : 5'd24;                                              Entropic ß Advantage   KL Correction
                                                              Rewardcandidate                         assign zero = ~|bits;
                       Testbench                              Verilog                 optimization                                           TB


                                                                                                                                                      Functional
                                                                                                                                                                                                     Reference-policy
                                                               PPA metrics
                                                              Syntax/ functional       instruction
                                                                                                      ct_vfmau_lza_32 u_15( candidate 2               simulation
                                          P       P       A




                                                              EDA feedback
                                                                  zz                                    .lza_precod({b15,b14,b13}),
                                      StateReward
                                            X                                                           .lza_p0(p0_2), .lza_p1(p1_2),
                                                                                                        .lza_vld(vld_2) );
                                                              PPA metrics
                                                              Verilog candidate
                      Dependencies    P       P       A




                                                              EDA  feedback
                                                                                                                                                       Synthesis+timing
                                                              Syntax/ functional                                                                        power analysis
                                                              Reward                                                          candidate n
                                                                                                      wire p0_23, p1_23, vld_23;
                                                                                                      ct_vfmau_lza_32 u_32_0 (                                              grouped
                                                              PPA metrics                               .lza_precod({b23,b22,b21}), ... );
                                      P       P       A



                                                                                                      assign zero = ~lza_vld;                                              learning
                      Baseline PPA                            EDA feedback                                                                   PPA product reward            advantage
      P    P     A




                                                                                                                                                                                       Grouped EDA Rewards
                                                                                                                                                                                        same parent, n rollouts
 Reference RTL provides initial
 context and golden functional                                                                         repair and
           behavior                                           Balances high-reward states and         optimization
                                                                  under-explored states.                feedback



                                                                                    state reuse and
                                                                                                                Top-k verified                               Closed-loop test-time training
                                                                                    exploration
                                                                                                                 candidates



Figure 1: Overview of TTT-RTL. The framework comprises four parts: Problem Assets (Sec-
tion 3.1), the PUCT State Pool with EDA-feedback prompt builder (Section 3.2), the LLM rollout
and three-stage EDA reward pipeline (Section 3.3), and the test-time policy update with state-pool
admission (Section 3.4).


with states sorted in descending reward order so that rank(s) = 0 is the best state [Yuksekgonul et al.,
2026, App. A.2]. To maintain batch diversity, TTT-RTL applies lineage blocking: no two states from
the same direct parent-child chain appear in one batch.

3.2                  EDA-Feedback Prompt Construction

The prompt for each parent state s contains the reference implementation with its synthesis metrics,
the design specification, and—for non-root states—the parent’s Verilog and its EDA feedback (root
prompts elide the parent block):

                         [Reference] area={A_ref}, delay={D_ref}, power={P_ref}, M ={M_ref}.
                         [Spec] {design_description}
                         [Previous] {verilog_code}
                         [Feedback] Syntax: PASS. Functional: PASS. Synthesis: area={A},
                         delay={D}, power={P}, M ={M} (improved by {∆}).
                         Produce a Verilog module with M lower than {M}.

Stating the target as a concrete numerical threshold grounds the generation objective in measurable
physical quantities.

3.3                  Three-Stage Reward Function

Each implementation v is evaluated through three stages, with the reward
                             r = ωsyn rsyn + ωfunc rfunc + ωppa rppa ,                                                              (ωsyn , ωfunc , ωppa ) = (0.1, 1.0, 10.0),                                          (3)
and evaluation terminating early on failure. Stage 1 (syntax): iverilog compilation; on failure
rsyn ∈ (0, 1] decays with the number of error messages (detailed scoring in Section I). Stage 2
(functional): simulation against the reference testbench; rfunc ∈ {0, 1}. Stage 3 (physical synthesis):
Yosys + OpenSTA report area A (µm2 ), critical-path delay D (ps) and (where collected) power P
(µW); the PPA reward is the reference-normalized ratio
                                    
               Mref                   A · D · P (RTLLM v2.0 PPA product, PPA-product)
      rppa =        ,     M (v) =                                                                  (4)
              M (v)                   A·D          (C910 LZA ablation, ADP; no power)

                                                                                                                             4
so that rppa = 1 matches the reference and rppa > 1 strictly improves it. The large ωppa reflects that
PPA optimization is the primary objective once functional correctness is achieved. After scoring,
the top-k deduplicated children of each parent enter S, PUCT statistics are updated, and the pool is
pruned to Cmax if exceeded (values in Table 8).

3.4   Entropic Advantage Estimation

Following TTT-Discover [Yuksekgonul et al., 2026], we estimate advantages within each group
(rollouts sharing a common parent). For a group of rewards {r1 , . . . , rk }, if max ri −min ri < 10−12
the group is degenerate and all advantages are zero; otherwise we find β ∗ such that the softmax
distribution qi ∝ exp(β ∗ ri ) attains a target KL divergence (KL budget) δ from uniform:
                                                 X
                                    KL(q∥U) =        qi ln(k · qi ) = δ,                              (5)
                                                  i
solved by binary search. Small δ keeps q near uniform (diffuse advantages); large δ allows q to peak
on a single rollout. The leave-one-out advantage is
                                             exp(β ∗ ri )
                                 Ai = 1 P                 ∗
                                                               − 1,                               (6)
                                        k−1    j̸=i exp(β rj )
which compares each rollout’s exponential reward weight against the average weight of the other
rollouts in the same group, yielding a group-relative contrast while avoiding self-normalization. For
RTLLM v2.0 we use the canonical fixed δ = ln 2; Section 3.7 introduces an adaptive variant we
study on the C910 LZA case study (Section 4.3).

3.5   Policy Gradient Update

For rollout i with prompt xi , the policy loss is
                                     L(θ) = − log πθ (vi |xi ) · Ai ,                       (7)
averaged over non-degenerate rollouts; following TTT-Discover, we omit the PPO importance-ratio
clip [Schulman et al., 2017].

3.6   Full Algorithm

Algorithm 1 TTT-RTL
Require: Design problem P (spec, testbench, reference), LLM πθ , budget S, batch size B, rollouts
    per prompt n
 1: Initialize pool S ← {s0 } (root), T ← 0
 2: for step = 1 to S do
 3:    Sample B parent states via Equation (1) with lineage blocking
 4:    Construct prompts {xb }Bb=1 (Section 3.2)
 5:    Generate n rollouts per prompt using πθ via vLLM [Kwon et al., 2023]
 6:    Evaluate rewards via 3-stage EDA pipeline (Section 3.3)
 7:    Update pool S, PUCT statistics, prune to Cmax
 8:    Compute advantages via entropic β ∗ at fixed δ = ln 2 (Section 3.4)
 9:    Update θ via policy gradient Equation (7)
10: end for
11: return Best-reward design in S



3.7   Adaptive KL-budget controller

For RTLLM v2.0 we use the canonical fixed δ = ln 2. On the C910 LZA case study (Section 4.3)
we additionally study an adaptive variant that replaces the constant with δt updated once per step
from four EMA-smoothed signals—policy-vs-reference KL, effective number of distinct rollouts per
group, fraction of constant-reward groups, and binary-search saturation rate—combined through a
four-rule priority ladder (KL brake, winner-take-all, stagnation, over-exploring) that resets, shrinks, or
grows δt within [0.25 ln 2, 4 ln 2]. Full equations (Equation (8)–Equation (12)) and hyperparameters
(Table 9) are in Section I.


                                                      5
4     Experiments

4.1   Experimental Setup

Base model and training configuration. The policy model is Qwen3-8B [Yang et al., 2025].
RTLLM v2.0 main runs initialize from a lightweight format-and-style SFT warm-up (ttt-rtl-sft
step 18; see Section G); the C910 LZA ablations (Section 4.3) instead use the raw Qwen3-8B base
model with no SFT, isolating the contribution of test-time RL on top of an off-the-shelf backbone.
Each run is 100 gradient steps with B = 4 parent states, top-k = 2 children, exploration coefficient
c = 1.0, and the reward weights of Equation (3); RTLLM v2.0 uses n = 4 rollouts/prompt and C910
LZA ablations use n = 8, matching TTT-Discover’s per-step budget [Yuksekgonul et al., 2026].
RTLLM v2.0 uses the canonical fixed δ = ln 2; C910 ablations vary δ along one axis of Table 3. Full
hyperparameters are in Table 8.

Benchmark and baselines. RTLLM v2.0 [Lu et al., 2024, Liu et al., 2025] provides a
human-written reference and testbench for each of 49 designs. We report the PPA-product ra-
tio PPA-product = A · D · P of each method’s best functionally correct design over the v2.0
reference (lower is better; 1.0 matches the reference). Baselines are three published agent-based
methods that target the same metric: EvolVE [Hsin et al., 2026], VeriAgent [Wang et al., 2026], and
the current SOTA REvolution [Min et al., 2025]; per-design ratios are taken verbatim from Table 3
of Ping et al. [2026], where every baseline runs under GPT-4o-mini against the v2.0 reference under
the same PPA-product metric.

Synthesis flow. Yosys [Wolf and Glaser, 2013] for logic synthesis, OpenSTA for timing/power.
RTLLM v2.0 uses Nangate 45 nm typical-corner (matching the published baseline flow); C910 LZA
uses Sky130 HD (the C910 release convention). All comparisons are reference-normalized within a
single PDK; we discuss residual cross-flow uncertainty in Section B.

Compute and seed protocol. All runs use A800 GPUs and seed 42, in line with the baselines
(none of EvolVE / VeriAgent / REvolution report seed variance); a four-seed paired replication on
LZA simd_half and a single-seed case study on a second C910 unit are reported in Section D.

4.2   RTLLM v2.0: Framework vs Published Agent Baselines

Table 1 aggregates the per-design PPA-product ratios across all 49 RTLLM v2.0 problems; the full
per-design table, including the 5 designs where at least one method failed to produce compilable,
functionally correct RTL, is in Table 4 (Section A). We characterize the comparison along three
complementary views, all of which point in the same direction. (i) Coverage: TTT-RTL produces a
valid implementation on 48/49 designs (highest of any method evaluated; missing only asyn_fifo),
and is the only method that succeeds on freq_divbyfrac and freq_divbyodd. (ii) Intersection
GeoMean (N =44): on the subset where all four methods produced a valid output — the only
domain on which GeoMean is mathematically well-defined for direct comparison — TTT-RTL
achieves a geometric-mean PPA-product ratio of 0.349 versus 0.739 for the strongest published
baseline (REvolution). (iii) Penalized full-benchmark GeoMean (N =49, failures= 1.0): imputing
each method’s failures as ratio 1.0 (“no improvement over the reference”, the most lenient possible
imputation since it credits a failed method with matching the reference) and recomputing GeoMean
over the full 49 designs gives 0.341 for TTT-RTL versus 0.762 for REvolution (Table 1, last column).
The intersection metric (N =44) is therefore not a cherry-pick: any defensible way of folding baseline
failures into the comparison only widens the TTT-RTL margin, never narrows it.
The advantage is consistent across complexity bins (Table 2), including on small combinational
designs where prior methods barely improve. Full per-design ratios and the failure breakdown are in
Table 4 and Section A.
Of the five non-intersection designs, four are ones our flow handles where one or more baselines
failed, so excluding them is conservative for TTT-RTL rather than a cherry-pick; per-design failures
are listed in Section A. A small number of v2.0 designs hit the OpenSTA 0 ps delay-reporting floor
(PPA product collapses to area-only), which affects all four methods uniformly under the shared
reference; we flag this as a reward-shaping limitation in the NeurIPS checklist (Limitations).


                                                  6
Table 1: Reference-normalized external comparison on RTLLM v2.0. Each cell reports the
PPA-product ratio (PPA-product = A · D · P ) of a method’s best functionally correct design
over the v2.0 reference implementation; lower is better. Baseline ratios are taken from Table 3 of
Ping et al. [2026] (GPT-4o-mini), while TTT-RTL is evaluated under our matched Yosys / OpenSTA /
Nangate 45 nm flow. Coverage counts designs (out of 49) on which a method produced compilable,
functionally correct RTL; GeoMean / ArithMeanN =44 are over the common subset where all four
methods completed; #Improved / #Best count common-subset designs with ratio < 1 / lowest ratio
(ties split equally); GeoMeanpen
                              N =49 imputes each method’s failures as ratio 1.0 (subset choices and
robustness check are detailed below). See Section 4.2 and Section B for the flow sanity check.
 Method                                                                      Coverage                            GeoMeanN =44 ↓                      ArithMeanN =44 ↓                          #Improved              #Best          GeoMeanpen
                                                                                                                                                                                                                                            N =49 ↓

 EvolVE                                                                            46/49                                 0.872                                     0.909                          17/44               0.5/44              0.892
 VeriAgent                                                                         44/49                                 0.813                                     0.853                          25/44               2.0/44              0.830
 REvolution                                                                        45/49                                 0.739                                     0.813                          29/44               8.0/44              0.762
 TTT-RTL                                                                           48/49                                 0.349                                     0.527                          38/44              33.5/44              0.341
    PPA-product ratio vs reference (lower is better)




                                                                                          Per-design PPA-product ratio on RTLLM v2.0 (common subset, N = 44, in benchmark order)
                                                       1.6
                                                                       Reference (RTLLM v2.0)                                  EvolVE             VeriAgent                    REvolution         TTT-RTL
                                                       1.4

                                                       1.2

                                                       1.0

                                                       0.8

                                                       0.6

                                                       0.4

                                                       0.2

                                                       0.0
                                                                                                                                        shifter
                                                                    LFSR


                                                                             RAM




                                                                                                                                                                                                                           wave
                                                                     nter




                                                                                   ROM
                                                                                          accu




                                                                                                                                                                                                                              ifter
                                                                      ffer




                                                                                         _16bit
                                                                                                               _32bit
                                                                                                                 _8bit
                                                                                                                 _bcd


                                                                                                                         alu


                                                                                                                                             ar




                                                                                                                                          r_12




                                                                                                                                                                      der
                                                                                                                 64bit




                                                                                                                                            bit
                                                                                                                                            bit


                                                                                                                                                                       bit
                                                                                                                                                                   detect



                                                                                                                                                                         r
                                                                                                                                                                      ulti
                                                                                                                                                                                iv
                                                                                                                                                                                                    fsm
                                                                                                                                                                                                       g
                                                                                                                                                                                                  16bit
                                                                                                                                                                                                    8bit
                                                                                                                                                                                                   _8bit
                                                                                                                                                                                                     bit
                                                                                                                                                                                                     bit


                                                                                                                                                                                                                                pe
                                                                                                                                                                                                l2serial


                                                                                                                                                                                                                          detect



                                                                                                                                                                                                                                  r
                                                                                                                                                                                                                           ector

                                                                                                                                                                                                                                  l
                                                                                                                                                                                                                              ator


                                                                                                                                                                                                                              4bit
                                                                                                                                                                                                                         ronizer

                                                                                                                                                                                                                             light
                                                                                                                                                                                                                              nter
                                                                                                                                                                                                                            to16
                                                                                                                                                                                                                        paralle
                                                                                                                                                                 btracto




                                                                                                                                                                                                                          ounte
                                                                                                                                                                                              instr_re
                                                                                                                                                                         freq_d
                                                                                                                                      calend
                                                                                                                                     ator_3
                                                                                                                                     ator_4


                                                                                                                                                                div_16




                                                                                                                                                                                             pipe_4
                                                                                                                                                                                             pipe_8
                                                                                                                                                              float_m
                                                                                                                                                              oint_ad
                                                               LIFObu




                                                                                                                                                                                             multi_




                                                                                                                                                                                                                      sub_6
                                                                                                                                                                                                                   right_sh




                                                                                                                                                                                                                     _gener
                                                             JC_cou




                                                                                                                                                                                                                      n_cou
                                                                                                                                   counte




                                                                                                                                                                                                                    traffic_


                                                                                                                                                                                                                   width_8
                                                                                                           adder
                                                                                                           adder




                                                                                                                                                                                            booth
                                                                                                          _pipe_




                                                                                                                                                                                          multi_




                                                                                                                                                                                                                   ce_det




                                                                                                                                                                                                                  square_
                                                                                           adder
                                                                                                   adder




                                                                                                                           barrel_




                                                                                                                                                            edge_




                                                                                                                                                                                                            pulse_


                                                                                                                                                                                                                  ring_c




                                                                                                                                                                                                                  synch
                                                                                                                                                                                       paralle




                                                                                                                                                                                                                 serial2
                                                                                                                                                         oint_su
                                                                                                                               compar
                                                                                                                               compar




                                                                                                                                                                                      multi_
                                                                                                                                                                                      multi_




                                                                                                                                                                                                             up_dow
                                                                                                                                                      fixed_p




                                                                                                                                                                                     multi_




                                                                                                                                                                                                              signal
                                                                                                    adder




                                                                                                                                                                                                            sequen
                                                                                                                                                 fixed_p




   EvolVE                                                                                                                                                                                                                    0.872
 VeriAgent                                                                                                                                                                                                           0.813
REvolution                                                                                                                                                                                             0.739
  TTT-RTL                                                                                                                               0.349
                                                         0.0                                               0.2                             0.4                                        0.6                     0.8                       1.0
                                                                                                                            Geometric-mean PPA-product ratio (common subset, N = 44)


Figure 2: Per-design PPA-product ratio (PPA-product = A · D · P ) on RTLLM v2.0 (the N =44
common subset, listed in benchmark order; the 5 designs with at least one missing method are
shown in Table 4). The EvolVE / VeriAgent / REvolution per-design ratios are the GPT-4o-mini
numbers reported in Table 3 of Ping et al. [2026]; TTT-RTL ratios are produced under the flow
described in Section 4. Top: four-method bar chart; the dashed black line is the v2.0 reference (1.0),
and the colored dotted lines are each method’s N =44 geometric-mean ratio. Bottom: aggregate
geometric-mean PPA-product ratio per method on the N =44 common subset. TTT-RTL is below the
reference on 38/44 designs and is the best method on 33.5/44 (next-best is REvolution at 8/44).


Caveat: external systems comparison, not same-backbone isolation. The four methods in
Table 1 share the same v2.0 reference, the same PPA-product metric, and (for our re-runs) the same
Yosys+OpenSTA flow, so the comparison is reference-normalized and ratio-controlled. The methods
do, however, use different policy LLMs: EvolVE, VeriAgent, and REvolution use GPT-4o-mini
(as reported in Ping et al. [2026], Table 3), while TTT-RTL uses Qwen3-8B with domain SFT
plus per-design test-time training. We therefore read Table 1 as a systems comparison—per-design
test-time training on top of an open-source backbone vs. frozen agentic search on top of a stronger
commercial backbone—rather than as a pure algorithmic isolation. A frozen Best-of-N baseline on
the C910 unit (Table 3, “Best-of-N ” row), which uses the raw Qwen3-8B base model with no SFT
and no test-time updates, never produces a functionally correct design within the 3200-rollout budget,
supporting that test-time updates—not the backbone or the SFT warm-up—drive the framework’s
gains.


                                                                                                                                                               7
Table 2: Geometric-mean PPA-product ratio on RTLLM v2.0, broken down by design complexity
(binned by reference PPA product). Lower is better; bold marks the best method per row.
                 Complexity bin                 N     EvolVE       VeriAgent      REvolution    TTT-RTL
                                          3
                 Small (ref PPA < 10 )          17    0.902          0.836           0.731         0.305
                 Medium (103 –105 )             14    0.963          0.906           0.901         0.475
                 Large (105 –107 )              10    0.736          0.675           0.559         0.274
                 Huge (> 107 )                   3    0.790          0.779           0.787         0.403


Table 3: Ablation results on ct_vfmau_lza_simd_half (Sky130, Qwen3-8B, seed 42, 3200-rollout
budget). All rows are single-seed. Reward 11.1 corresponds to the reference ADP; entries marked
“—” never produced any functionally correct design within the budget. Per-step reward trajectories
are in Figure 3; KL-budget trajectories are in Section C. Quantitative gaps within the table should be
read as consistent ranking evidence rather than tight effect sizes.
      Configuration                                      Best reward (↑)       Best ADP (µm2 ·ps, ↓)   ADP reduction
      Reference (C910 baseline)                                      11.10                3,402,207              —
      TTT-RTL (PUCT + entropic + adaptive δ)                        25.72                1,381,970          −59.4%
      δ-schedule axis (reuse = PUCT, train = entropic)
        cosine 1.1 → 0.3 (high→low)                                  21.02                1,708,247         −49.8%
        fixed δ = ln 2 (TTT-Discover default)                        19.38                1,860,973         −45.3%
        cosine 0.3 → 1.1 (low→high)                                  15.91                2,296,653         −32.5%
      Train axis (reuse = PUCT, δ = fixed ln 2)
        expected reward (no entropic)                                16.65                2,187,460         −35.7%
      Reuse axis (train = entropic, δ = fixed ln 2)
        ϵ-greedy (ϵ=0.1)                                             21.69                1,652,580         −51.4%
        no reuse                                                     12.63                2,951,048         −13.3%
      Naive Test-time RL (expected reward + no reuse)                 0.89                       —               —
      Best-of-N (frozen policy + no reuse, N =3200)                   1.00                       —               —



4.3     XuanTie C910 LZA: Industrial Case Study

The RTLLM v2.0 results above establish that TTT-RTL beats published agent baselines on a
textbook benchmark. To stress-test the framework on production silicon, we now turn to the
leading-zero-anticipation unit ct_vfmau_lza_simd_half from the open-source XuanTie C910
RISC-V core [Chen et al., 2020]—well-tuned hand-written RTL where any ADP reduction is
non-trivial. We use this single industrial unit to ablate TTT-RTL along three axes: the reuse strategy,
the training-time advantage estimator, and the KL-budget schedule. All runs share the same sam-
pling budget (100 steps × 4 parents × n = 8 rollouts = 3200 rollouts), base model (Qwen3-8B),
technology library (Sky130), seed (42), and reward function (Equation (3)). The reference ADP for
this unit is 3.40M µm2 ·ps, at which the reward is exactly 11.1; any reward above 11.1 corresponds
to a functionally correct design that strictly improves ADP.

Ablation axes. We sweep three orthogonal axes one at a time. On the δ-schedule axis, the other
two axes are fixed at the full TTT-RTL configuration (PUCT reuse, entropic advantage), and the
“adaptive δ” row is the headline full-TTT-RTL row at the top of Table 3. On the reuse and train
axes we instead hold δ at the fixed ln 2 TTT-Discover default rather than at adaptive δ, so that the
component-isolation comparisons do not implicitly inherit the controller’s exploratory gain; the
framework-only (−45.3%) row is the natural reference for those rows. The three axes are then
(i) reuse ∈ {PUCT, ϵ-greedy (ϵ=0.1), none}, where “none” restarts every rollout from the empty
root; (ii) train ∈ {entropic advantage, expected reward}, where the latter is standard GRPO [Shao
et al., 2024] with group-mean-centred, std-normalised advantages and no entropic temperature;
(iii) δ-schedule ∈ {adaptive (controller of Section 3.7), fixed ln 2 (TTT-Discover’s constant), cosine
1.1 → 0.3 (“explore-then-exploit”), cosine 0.3 → 1.1 (reverse, sanity-check)}. Two combined-weakest
configurations bound the ablation from below: Naive Test-time RL (expected reward + no reuse) and
Best-of-N (frozen actor at lr 10−12 , N =3200).


                                                               8
                                                        RTL-Discover ablations on ct_vfmau_lza_simd_half (ref ADP = 3.40M μm²·ps, reward = 11.1 at reference ADP)
              (a) Max reward up to step                                               (b) Mean reward within rollouts in step                         (c) Max reward within rollouts in step

         25                                                                             25                                                                           25



         20                                                                             20                                                                           20



         15                                                                             15                                                                           15
Reward




              reference ADP (r=11.1)                                                         reference ADP (r=11.1)                                                       reference ADP (r=11.1)

         10                                                                             10                                                                           10



         5                                                                               5                                                                           5



         0                                                                               0                                                                           0
              0           20           40          60         80             100             0            20             40          60        80         100             0           20           40          60   80   100
                                        Training step                                                                     Training step                                                             Training step


                                                         TTT-RTL (full)            fixed δ = ln 2 (Discover)          adaptive + ε-greedy   expected reward + PUCT        Best-of-N (frozen)
                                                         cosine δ: 1.1→0.3         cosine δ: 0.3→1.1                  adaptive + no reuse   naive RL




Figure 3: Ablation trajectories on ct_vfmau_lza_simd_half, following the three-panel format of
Yuksekgonul et al. [2026], Fig. 10. (a) Max reward up to step; (b) Mean reward within rollouts
in step (typical policy behaviour); (c) Max reward within rollouts in step (per-step exploration
quality). The dashed red line marks r = 11.1 (reference ADP); designs above the line strictly improve
over the C910 baseline. All runs share the same 3200-rollout budget, base model, reward, and seed;
the only differences are the train/reuse components as in Table 3.



Reuse and train axes. With δ held at the TTT-Discover default ln 2, the framework alone (PUCT +
entropic + fixed δ) reaches −45.3% ADP. Removing the entropic advantage estimator drops this to
−35.7% (plateauing after step ∼ 30), while replacing PUCT with ϵ-greedy reuse closes most of the
reuse-side gap (−51.4% at seed 42). Removing reuse entirely is the most costly single-axis change:
−13.3%. Naive-RL (expected reward + no reuse) and Best-of-N on the frozen policy never produce
a single functionally correct design within the 3200-rollout budget. The reuse-vs-ϵ-greedy gap is
small enough that we read it as “PUCT helps but is not the sole driver”; the entropic-vs-expected
gap is larger and consistent with Yuksekgonul et al. [2026]’s observation that exploration matters
most outside kernel-engineering settings, where uniform sampling from the base policy almost never
yields a correct Verilog module.


δ-schedule axis. On top of the framework’s −45.3%, the adaptive δ-controller adds another ∼ 14
pp at seed 42 (−59.4%). The cosine 1.1 → 0.3 schedule, hand-tuned to approximate “explore early,
exploit late,” recovers most of the gap (−49.8%); the reverse cosine is uniformly worse. This is
consistent with the controller firing P4 (over-exploring, grow δ) when advantages are diffuse early on,
and P2/P3 (winner-take-all / stagnation, shrink δ) once a winner emerges—i.e. the trajectory resembles
the explore-then-exploit shape that the cosine encodes by hand. Per-step KL-budget trajectories
appear in Section C. A four-seed paired replication on LZA simd_half and a single-seed case study
on a second C910 unit (Section D) confirm task-responsive direction and a ∼2.6× reduction in
seed-wise variance, but the gap does not reach p < 0.05 at n = 4; we discuss this caveat further in
Section D.


Mean vs. max reward. Figure 3b,c isolates the entropic advantage estimator: expected-reward +
PUCT lifts the per-step mean reward but caps the per-step max below TTT-RTL’s, trading a slightly
worse average rollout for a consistently better best rollout—the quantity that matters in a discovery
setting.


5                 Conclusion

We presented TTT-RTL, a framework that closes the loop between an LLM policy and EDA synthesis
tools to apply test-time training to RTL optimization. On RTLLM v2.0 it cuts the PPA product against
the strongest published agent baseline, and on a XuanTie C910 industrial LZA unit it improves over
well-tuned production RTL while component ablations isolate the contribution of the PUCT state
pool and the entropic advantage estimator.


                                                                                                                             9
References
Tutu Ajayi, Vidya A. Chhabria, Mateus Fogaça, Soheil Hashemi, Abdelrahman Hosny, Andrew B.
  Kahng, Minsoo Kim, Jeongsup Lee, Uday Mallappa, Marina Neseem, Geraldo Pradipta, Sherief
  Reda, Mehdi Saligane, Sachin S. Sapatnekar, Carl Sechen, Mohamed Shalan, William Swartz,
  Lutong Wang, Mingyu Woo, and Bang Xu. Toward an open-source digital flow: First learnings
  from the OpenROAD project. In Proceedings of the 56th Annual Design Automation Conference
  (DAC), 2019. doi: 10.1145/3316781.3326334.
Jason Blocklove, Siddharth Garg, Ramesh Karri, and Hammond Pearce. Chip-chat: Challenges and
  opportunities in conversational hardware design, 2023. URL https://arxiv.org/abs/2305.
  13243.
Chen Chen, Xiaoyan Xiang, Chang Liu, Yunhai Shang, Ren Guo, Dongqi Liu, Yimin Lu, Ziyi
  Hao, Jiahui Luo, Zhijian Chen, Chunqiang Li, Yu Pu, Jianyi Meng, Xiaolang Yan, Yuan Xie, and
  Xiaoning Qi. XuanTie-910: A commercial multi-core 12-stage pipeline out-of-order 64-bit high
  performance RISC-V processor with vector extension. In Proceedings of the 47th International
  Symposium on Computer Architecture (ISCA), pages 52–64, 2020. doi: 10.1109/ISCA45697.2020.
  00016.
Zhirong Chen, Kaiyan Chang, Zhuolin Li, Cangyuan Li, Xinyang He, Chujie Chen, Mengdi Wang,
  Haobo Xu, Yinhe Han, Huawei Li, and Ying Wang. ChipSeek: Optimizing Verilog generation via
  EDA-integrated reinforcement learning, 2025. URL https://arxiv.org/abs/2507.04736.
Wei-Po Hsin, Ren-Hao Deng, Yao-Ting Hsieh, En-Ming Huang, and Shih-Hao Hung. EvolVE:
 Evolutionary search for LLM-based Verilog generation and optimization, 2026. URL https:
 //arxiv.org/abs/2601.18067.
Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.
 Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model
 serving with PagedAttention. In Proceedings of the 29th Symposium on Operating Systems
 Principles (SOSP), 2023. doi: 10.1145/3600006.3613165. URL https://arxiv.org/abs/
 2309.06180.
Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven C. H. Hoi. CodeRL:
  Mastering code generation through pretrained models and deep reinforcement learning. In Advances
  in Neural Information Processing Systems 35 (NeurIPS), 2022. URL https://arxiv.org/abs/
  2207.01780.
Mingjie Liu, Teodor-Dumitru Ene, Robert Kirby, Chris Cheng, Nathaniel Pinckney, Rongjian Liang,
 Jonah Alben, Himyanshu Anand, Sanmitra Banerjee, Ismet Bayraktaroglu, Bryan Catanzaro, Arjun
 Chaudhuri, Brucek Khailany, Haoxing Ren, et al. ChipNeMo: Domain-adapted LLMs for chip
 design, 2023a. URL https://arxiv.org/abs/2311.00176.
Mingjie Liu, Nathaniel Pinckney, Brucek Khailany, and Haoxing Ren. VerilogEval: Evaluating large
 language models for verilog code generation, 2023b. URL https://arxiv.org/abs/2309.
 07544.
Shang Liu, Wenji Fang, Yao Lu, Qijun Zhang, Hongce Zhang, and Zhiyao Xie. RTLCoder: Outper-
  forming GPT-3.5 in design RTL generation with our open-source dataset and lightweight solution,
  2023c. URL https://arxiv.org/abs/2312.08617.
Shang Liu, Yao Lu, Wenji Fang, Mengming Li, and Zhiyao Xie. OpenLLM-RTL: Open dataset and
  benchmark for LLM-aided design RTL generation, 2025. URL https://arxiv.org/abs/2503.
  15112.
Yao Lu, Shang Liu, Qijun Zhang, and Zhiyao Xie. RTLLM: An open-source benchmark for design
  RTL generation with large language model. In Proceedings of the 29th Asia and South Pacific
  Design Automation Conference (ASP-DAC), 2024. doi: 10.1109/ASP-DAC58780.2024.10473904.
  URL https://arxiv.org/abs/2308.05345.
Kyungjun Min, Kyumin Cho, Junhwan Jang, and Seokhyeong Kang. REvolution: An evolutionary
  framework for RTL generation driven by large language models, 2025. URL https://arxiv.
  org/abs/2510.21407. Accepted to ASP-DAC 2026.


                                               10
Zehua Pei, Hui-Ling Zhen, Mingxuan Yuan, Yu Huang, and Bei Yu. BetterV: Controlled Verilog
  generation with discriminative guidance. In Proceedings of the 41st International Conference on
  Machine Learning (ICML), volume 235 of Proceedings of Machine Learning Research. PMLR,
  2024. URL https://arxiv.org/abs/2402.03375.
Heng Ping, Peiyu Zhang, Shixuan Li, Wei Yang, Anzhe Cheng, Shukai Duan, Xiaole Zhang,
  and Paul Bogdan. COEVO: Co-evolutionary framework for joint functional correctness and
  PPA optimization in LLM-based RTL generation, 2026. URL https://arxiv.org/abs/2604.
  15001.
John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy
  optimization algorithms. CoRR, abs/1707.06347, 2017. URL http://arxiv.org/abs/1707.
  06347.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
  Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. DeepSeekMath: Pushing the limits of mathemat-
  ical reasoning in open language models, 2024. URL https://arxiv.org/abs/2402.03300.
Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng,
  Haibin Lin, and Chuan Wu. HybridFlow: A flexible and efficient RLHF framework, 2024. URL
  https://arxiv.org/abs/2409.19256.
Jiahe Shi, Zhengqi Gao, Ching-Yun Ko, and Duane Boning. EARL: Entropy-aware RL alignment of
   LLMs for reliable RTL code generation, 2025. URL https://arxiv.org/abs/2511.12033.
Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling LLM test-time compute optimally
  can be more effective than scaling model parameters, 2024. URL https://arxiv.org/abs/
  2408.03314.
Yu Sun, Xiaolong Wang, Zhuang Liu, John Miller, Alexei A. Efros, and Moritz Hardt. Test-time
  training with self-supervision for generalization under distribution shifts. In Proceedings of the
  37th International Conference on Machine Learning, volume 119 of Proceedings of Machine
  Learning Research, pages 9229–9248. PMLR, 2020.
Yaoxiang Wang, Qi Shi, ShangZhan Li, Qingguo Hu, Xinyu Yin, Bo Guo, Xu Han, Maosong Sun,
  and Jinsong Su. VeriAgent: A tool-integrated multi-agent system with evolving memory for
  PPA-aware RTL code generation, 2026. URL https://arxiv.org/abs/2603.17613.
Clifford Wolf and Johann Glaser. Yosys – a free verilog synthesis suite. In Proceedings of the 21st
  Austrian Workshop on Microelectronics (Austrochip), 2013. Post-2014, the first author goes by
  Claire Wolf.
Yangzhen Wu, Zhiqing Sun, Shanda Li, Sean Welleck, and Yiming Yang. Inference scaling laws: An
  empirical analysis of compute-optimal inference for problem-solving with language models, 2024.
  URL https://arxiv.org/abs/2408.00724.
An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang
  Gao, Chengen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, Junyang
  Lin, Jingren Zhou, et al. Qwen3 technical report, 2025. URL https://arxiv.org/abs/2505.
  09388.
Mert Yuksekgonul, Daniel Koceja, Xinhao Li, Federico Bianchi, Jed McCaleb, Xiaolong Wang, Jan
 Kautz, Yejin Choi, James Zou, Carlos Guestrin, and Yu Sun. Learning to discover at test time,
 2026. URL https://arxiv.org/abs/2601.16175.
Yaoyu Zhu and contributors. CodeV-R1: A verilog reasoning-distillation dataset. Hugging Face
  dataset, 2025. URL https://huggingface.co/datasets/zhuyaoyu/CodeV-R1-dataset.
Yuxin Zuo, Kaiyan Zhang, Li Sheng, Shang Qu, Ganqu Cui, Xuekai Zhu, Haozhan Li, Yuchen
  Zhang, Xinwei Long, Ermo Hua, Biqing Qi, Youbang Sun, Zhiyuan Ma, Lifan Yuan, Ning Ding,
  and Bowen Zhou. TTRL: Test-time reinforcement learning. In Advances in Neural Information
  Processing Systems 38 (NeurIPS), 2025. URL https://arxiv.org/abs/2504.16084.



                                                11
A                 Per-design Results on RTLLM v2.0
Table 4 reports the per-design ratio of every method on every RTLLM v2.0 problem (all 49 designs).
“–” indicates that the method failed to produce a compilable / functionally correct design within its
reported budget. The TTT-RTL column is the PPA-product ratio (A · D · P ) that drove its training
reward; the EvolVE / VeriAgent / REvolution columns are the PPA-product ratios reported by the
original authors against the same v2.0 reference (see “Caveat: external systems comparison, not
same-backbone isolation” in Section 4.2). The summary statistics (Table 1 in the main text) are
computed over the N =44 common subset where all four methods completed (the intersection required
for a fair GeoMean); the five remaining designs (asyn_fifo, radix2_div, freq_divbyeven,
freq_divbyfrac, freq_divbyodd) are excluded from GeoMean / #Best but are shown in the
per-design table below for completeness.

B                 Flow Sanity Check: Local vs. Published Reference PPA
To support the ratio-normalized comparison protocol described in Section 4.2 (“Flow sanity check
and ratio-normalized comparison”), we re-evaluated the RTLLM v2.0 reference Verilog on every
design under our local Yosys+OpenSTA flow with the Nangate 45 nm typical-corner library, and
compared the resulting area / delay / power against the published reference numbers reported in
Table 3 of Ping et al. [2026] (the open-source pipeline released as hping666/COEVO). Table 5 shows
representative rows spanning the four complexity bins of Table 2; Table 6 reports aggregate error
statistics over the designs that synthesize cleanly under both flows (47 for area, 43 for delay/power;
see the table caption).
The full per-design CSV (reference_ppa_measured.csv) is released alongside the codebase.

C                 KL-Budget Ablation Trajectories

                                        Dynamic KL budget ablation on ct_vfmau_lza_simd_half (ref ADP = 3.40M μm²·ps, reward = 11.1 at reference ADP)

              (a) Max reward up to step                                     (b) Mean reward within rollouts in step                  (c) Max reward within rollouts in step
                    adaptive δ (RTL-Discover, ours)
         25         fixed δ = ln 2 (Discover)
                                                                       25                                                       25
                    cosine schedule 1.1 → 0.3
                    cosine schedule 0.3 → 1.1
         20                                                            20                                                       20



         15                                                            15                                                       15
Reward




              reference ADP (r=11.1)                                        reference ADP (r=11.1)                                   reference ADP (r=11.1)

         10                                                            10                                                       10



         5                                                              5                                                       5



         0                                                              0                                                       0
              0         20             40        60     80      100         0         20             40        60    80   100        0         20             40        60    80   100
                                       Training step                                                 Training step                                            Training step



Figure 4: KL-budget ablation trajectories on ct_vfmau_lza_simd_half, in the same three-panel
layout as Figure 3. Adaptive δ (dark blue, RTL-Discover) keeps a strictly higher upper-tail reward
than all three alternatives throughout training (panel c) and is the only strategy whose best-so-far
reward (panel a) crosses r = 20. The cosine 1.1 → 0.3 schedule recovers a substantial fraction of
the gap, supporting the interpretation that early-large / late-small δ is a useful inductive bias for
RTL search; the reverse schedule is uniformly worse. The fixed Discover-style δ = ln 2 falls in
between but plateaus before reaching the reference-ADP line on (a). Headline numbers are in Table 3
(Section 4.3).


D                 Multi-Seed and Multi-Task Replication of the Adaptive KL-Budget
                  Controller
Section 4.3 reports the adaptive vs. fixed δ = ln 2 contrast at a single seed on
ct_vfmau_lza_simd_half. We extend that contrast in two directions: (i) a four-seed paired
replication on the same problem, and (ii) a single-seed case study on a second C910 unit,


                                                                                                      12
ct_vfdsu_fadd_close_s0_d. Both arms share the recipe of Section 4.3 (PUCT + entropic, sky130,
KL penalty active, 100 RL steps, 4 parents × 8 rollouts) and differ only in the algorithmic switch
algorithm.ttt_entropic_kl_budget_mode. Raw extracts, statistics scripts, and figures are
released under experiment/checklist/multi-seed-c910/.

LZA simd_half (n = 4 paired). Table 7 shows the four headline metrics paired across seeds. No
metric reaches p < 0.05 under either paired t-test or Wilcoxon at n = 4; the unpaired Welch test
on best_reward_ever returns p = 0.51. The mean advantage of +0.67 on best_reward_ever
is robust to dropping any single seed (leave-one-out ∆ ∈ [+0.12, +0.95], all positive), but the gap
remains within seed-wise noise. Adaptive does, however, reduce seed-wise standard deviation by
∼ 2.6× (0.56 vs. 1.48) and reaches score ≥ 20 on 4/4 seeds while fixed reaches it on 3/4. Across all
four adaptive seeds the controller drives δ below ln 2, with per-seed minima in [0.17, 0.50] (Figure 5,
top).




Figure 5: LZA simd_half, n = 4 paired. Left: per-step δt for all four adaptive seeds and the
fixed δ = ln 2 baseline. Adaptive consistently drives δ below ln 2 across seeds. Right: per-seed
best_reward_ever bars (paired). Adaptive wins 3/4 but the gap is within seed-wise noise.

The four adaptive runs were not originally generated as seeds 1–4; they are historical runs treated as a
four-seed pool for this analysis. An exhaustive enumeration of all 24 adaptive-to-fixed permutations
yields paired-t p ∈ [0.31, 0.59] with 0/24 significant at p < 0.10, so the headline conclusion is
invariant to pairing choice.

fadd_close_s0_d (n = 1). A single-seed case study on a second C910 unit shows a qualitatively
different picture: the fixed arm plateaus at best_reward = 9.86 from step ∼ 20 onwards and never
crosses 10, while the adaptive arm reaches 12.55 (peak) and 12.33 (end-of-run mean over the last 20
steps), a +27% / +34% relative gap. Crucially, the controller raises δ above ln 2 on this problem
(to 1.44, see Figure 6, right) – the opposite direction from LZA – demonstrating that the four EMA
signals of Section 3.4 respond to task-specific structure rather than moving in a fixed direction.




Figure 6: fadd_close_s0_d, n = 1 vs. 1. Left: running-max best-in-batch reward. Fixed plateaus
at 9.86; adaptive escapes around step 30 and stabilises near 12.5. Right: δt trajectory. Fixed stays at
ln 2 ≈ 0.693; adaptive raises δ to 1.44 at step ∼ 50, after the policy breakthrough.



                                                  13
What this experiment supports. (1) The adaptive controller is task-responsive in direction – it
lowers δ on LZA and raises it on fadd. (2) Adaptive matches or exceeds fixed on every aggregate
metric we report (+0.67 peak and −25 steps to score ≥ 20 on LZA; +2.69 peak and +3.11 end-of-run
on fadd). (3) Seed-wise variance on LZA is reduced ∼ 2.6× and the worst-case fixed seed (peak
18.75, fails to cross score 20) has no adaptive counterpart.

What this experiment does not support. (1) Statistical significance: no metric reaches p < 0.05 on
LZA at n = 4, and fadd is n = 1 and admits no test. (2) Causal attribution on fadd: the δ raise occurs
at step ∼ 50, after the policy has already plateaued at the new peak near step 30. In the first 50 steps
both arms run with δ = ln 2 and the divergence is from PUCT / vLLM stochasticity, not the scheduler.
(3) A peak-performance claim: the LZA +0.67 falls inside the [15.6, 25.7] development-time spread
reported in Section 5, and fadd is a single trial.
We accordingly frame the adaptive controller in the body of the paper as a robustness and
task-responsiveness observation rather than a peak-performance win. Re-running fadd at n ≥ 4 and
extending LZA to n ≥ 8 remain the obvious follow-ups.

E     C910 LZA Case Study: Baseline, Optimized Code, and Testbench
This appendix documents the concrete artifact behind the C910 numbers in Sections D and 4.3: the
baseline RTL we start from, the best discovered candidate (best_reward_ever = 25.72, A·D =
1.38×106 vs. baseline 3.40×106 , i.e. −59.4% ADP at sky130 HD), and the verification harness that
gates every rollout.

E.1   Baseline: Xuantie OpenC910 ct_vfmau_lza_simd_half

The baseline is the upstream RTL from the open-sourced Xuantie C910 core
(ct_vfmau_lza_simd_half.v), which implements a 24-bit leading-zero anticipator for the
SIMD half-precision lane of the VFMAU. The module has two stages:

Stage 1: pre-encode. Carry signals P =summand ⊕ addend, G=summand & addend,
D=summand | addend are formed bitwise, followed by a vectorized 24-bit pre-decode
lza_precod[23:0] with three boundary cases (LSB, MSB, and the bulk [22:1] slice gated on
sub_vld). Both arms keep this stage byte-for-byte identical; the optimization budget is entirely in
stage 2.

Stage 2 (baseline): flat 24-way casez priority encoder. The leading-one position is decoded by
a single always @(*) casez block with 24 one-hot patterns of the form 24’b1???... → 5’d0,
24’b01??... → 5’d1, . . . , 24’b...001 → 5’d23, plus a default 5’d24. Yosys synthesizes this
into a 24-input priority chain whose critical path traverses all 24 casez arms before the 5-bit encoder;
together with the (already large) pre-encode this is what gives the baseline ADP of 3.40×106 .

E.2   Best discovered candidate

The best rollout under our adaptive-δ recipe keeps stage 1 unchanged and rewrites stage 2 as a
hierarchical 4-bit grouped priority encoder (?? 1). Three changes drive the ADP reduction:
      1. Group-then-encode.              lza_precod[23:0] is sliced into six 4-bit
         groups ({23:20}, {19:16}, . . . , {3:0}).        Within a group the 4-way prior-
         ity over a 4-bit one-hot vector collapses to a depth-3 ternary cascade
         a[3]? k: a[2]? k+1: a[1]? k+2: a[0]? k+3: 5’d24, which Yosys maps to four
         2-input gates per group instead of the shared 24-priority chain.
      2. Group-validity reuse. Six instances of the existing C910 sub-cell ct_vfmau_lza_42
         (a 4:2 LZA compressor already shipped in the deps/ directory) compute a lza_vld flag
         per group; the outer cascade picks the highest-index valid group, so each 4-bit decoder
         fires only when its group is selected. The lza_p0/lza_p1 outputs of the compressor are
         deliberately left unconnected — the policy reuses the cell only for its valid bit. This converts
         the baseline’s monolithic priority chain into a log4 (24)-style two-level structure, which is
         the dominant source of the delay reduction (2191 → 1315 ps, −40%).


                                                  14
      3. Combinational, not registered. The baseline declares reg [4:0] lza_result and drives
         it from an always @(*) block; the candidate uses a single assign with a nested ternary,
         which is functionally equivalent (no clock anywhere in the spec) but lets Yosys schedule
         the decoder under one cone of logic with the group-validity lookups, trimming both area
         (1553 → 1051 µm2 , −32%) and the fan-in to the final mux.
The interface (port list, widths, directions) is preserved exactly, so the candidate is a drop-in replace-
ment. This module-internal restructuring is the only change in stage 2.
Listing 1: Stage 2 of the best candidate (ttt_c910_state_pool/latest.json, state #304, A·D =
1.38×106 ). Stage 1 (carry_p/g/d, lza_precod) is unchanged from the baseline and elided.
// 4-bit grouping of lza_precod
wire [3:0] lza_4_23_20 = lza_precod[23:20];
wire [3:0] lza_4_19_16 = lza_precod[19:16];
wire [3:0] lza_4_15_12 = lza_precod[15:12];
wire [3:0] lza_4_11_8 = lza_precod[11:8];
wire [3:0] lza_4_7_4 = lza_precod[7:4];
wire [3:0] lza_4_3_0 = lza_precod[3:0];

// Reuse C910 LZA 4:2 compressor for the per-group valid flag only
ct_vfmau_lza_42 lza_42_23_20 (.lza_precod(lza_4_23_20),
                           .lza_p0(), .lza_p1(), .lza_vld());
// ... five more identical instances for the remaining groups ...

// Hierarchical priority: highest-index valid group wins
assign lza_result =
   (lza_42_23_20.lza_vld) ?
       (lza_4_23_20[3] ? 5’d0 : lza_4_23_20[2] ? 5’d1 :
        lza_4_23_20[1] ? 5’d2 : lza_4_23_20[0] ? 5’d3 : 5’d24) :
   (lza_42_19_16.lza_vld) ?
       (lza_4_19_16[3] ? 5’d4 : lza_4_19_16[2] ? 5’d5 :
        lza_4_19_16[1] ? 5’d6 : lza_4_19_16[0] ? 5’d7 : 5’d24) :
   /* ... four more group arms ... */
   (lza_42_3_0.lza_vld) ?
       (lza_4_3_0[3] ? 5’d20 : lza_4_3_0[2] ? 5’d21 :
        lza_4_3_0[1] ? 5’d22 : lza_4_3_0[0] ? 5’d23 : 5’d24) :
   5’d24;

assign lza_result_zero = ~|lza_precod[23:0];



E.3   Verification harness

Every rollout is gated by an iverilog testbench that co-instantiates the candidate and a re-
named copy of the baseline (ct_vfmau_lza_simd_half_ref) and compares lza_result and
lza_result_zero cycle by cycle. The harness contains 5 phases (∼ 1,050 vectors total):
       • Edge cases (sub_vld = 0, addition mode). Both operands zero, both all-ones,
         MSB-only and LSB-only patterns, one operand zero with the other all-ones, alternating
         0xAAAAAA/0x555555, walking-1 over all 24 bit positions on each operand, adjacent-bit
         carry-propagate patterns, and the three saturated carry chains P =1, G=1, D=1.
       • Edge cases (sub_vld = 1, subtraction mode). The same zero / all-ones / boundary /
         walking-1 / alternating set, exercising the sub_vld-dependent branches of lza_precod[0]
         and lza_precod[23].
       • Random, 800 vectors. 400 with sub_vld = 0 and 400 with sub_vld = 1, drawn from
         $random(seed) with seed 42.
       • Sparse / mixed. 100 vectors with sub_vld sampled per trial and only 2–3 random bits set
         across the two operands, to stress the priority encoder under near-degenerate inputs.
       • Close-path. 100 vectors with addend = summand XOR-perturbed at one random bit
         position under sub_vld = 1; this is the regime where leading-zero anticipation dominates
         the floating-point add-round critical path and is the original engineering motivation for the
         LZA cell.
A run is accepted only when all ∼ 1,050 comparisons pass (fail_count = 0, “Your Design Passed”);
any single mismatch zeroes the functional reward and the candidate is rejected before PPA synthesis
is even invoked. This is what makes the −59.4% ADP claim a functional-equivalence claim against
the upstream Xuantie cell rather than a synthesis-only PPA claim.


                                                    15
F    Hyperparameter Summary

G    SFT Warm-up Recipe
The ttt-rtl-sft checkpoint that initializes the policy model is a lightweight format-and-style
warm-up applied to Qwen3-8B before any test-time RL. Its sole purpose is to make the base model
reliably emit Verilog inside the expected <think>...</think> block and “‘verilog fences while
respecting the prompt structure of Section H; it is not intended as a knowledge distillation step that
would short-circuit the role of test-time training.

Data source. The SFT corpus is 5,000 uniformly sampled rows from the public CoDeV-R1 dis-
tillation dataset [Zhu and contributors, 2025] (87K Verilog reasoning-chain records in total), with
the original <think>/<answer> tags rewritten to match our <think> convention. No RTLLM v2.0
problems are used at SFT time — the warm-up is purely an out-of-distribution format-and-style
prior, and all benchmark exposure happens during test-time RL. The corpus is in the verl multi-turn
messages format with a 95/5 train/val split.

Training. We train Qwen3-8B for 3 epochs at learning rate 10−5 with FSDP, global batch size 64,
max sequence length 16,384, on 8× A800 GPUs. All RL experiments in this paper start from the
global-step-18 checkpoint, which corresponds to roughly 1,152 examples seen (∼ 0.23 epochs over
the corpus): on average each training row has been seen at most once. This minimal warm-up is
intentional — in pilot runs longer SFT degraded downstream exploration during RL — and the goal
is only to lock in response format, not to teach problem-specific solutions.

Is SFT or test-time RL doing the work? Two factors bound the risk that SFT, rather than test-time
RL, drives the headline numbers. (1) The ∼ 0.23-epoch budget on a corpus that contains no RTLLM
v2.0 problems is too small for the model to memorize benchmark solutions: the warm-up shifts
response format, not benchmark answers. (2) The C910 LZA experiments do not use the SFT
checkpoint at all: they initialize from the raw Qwen3-8B base model (Table 8). The Best-of-N row of
Table 3 freezes that raw base policy and draws N = 3200 samples on ct_vfmau_lza_simd_half;
it never produces a single functionally correct design within the budget. Since SFT plays no role
on C910, the −59.4% ADP improvement on this unit is attributable to test-time RL on top of
the off-the-shelf backbone. The released artifact ships the SFT configuration and merge script so
reviewers can re-run the warm-up under any policy of choice.

H    Prompt Templates
System prompt.     The system prompt is fixed for all problems:
         You are an expert Verilog RTL designer.
         When reasoning, use <think>...</think> tags.
         Output only Verilog code within “‘verilog fences.

The templates below are the RTLLM v2.0 main-run prompts in which the PPA product M = A · D · P
is shown to the model. In the C910 LZA ablation (where the OpenSTA power column is not collected)
the same templates degenerate to ADP (M = A · D); we use the generic placeholder “{M}” below to
make this dual usage explicit.

Root state user prompt.
        ## Reference Implementation
        Below is a known working implementation that synthesizes to
        area={A}µmˆ2, delay={D}ps, power={P}µW (PPA-product={M}).
        Your task is to produce a functionally correct implementation
        with lower PPA-product (Area × Delay × Power).
        “‘verilog
        {reference_code}
        “‘
        ## Design Specification


                                                 16
         {specification}
         Write a complete Verilog module with PPA-product lower than {M}.
         Output only Verilog code within “‘verilog fences.

Non-root state user prompt. The non-root prompt appends the following block after the reference
and specification:
          ## Previous Attempt
         “‘verilog
         {parent_code}
         “‘
          ## Feedback from Previous Attempt
         - Syntax: PASS
         - Functional Test: PASS
         - Synthesis: area={A}µmˆ2, delay={D}ps, power={P}µW, PPA-product={M}
          Previous PPA-product: {prev_M} -> current: {M} (improved by {∆})
         You are iteratively optimizing PPA-product (lower is better).
          Produce a design with PPA-product lower than {M}.


I   Entropic Adaptive Beta: Implementation Detail
Stage-1 syntax score. On iverilog failure the syntax reward is rsyn = 1/(1 + nerr ), additionally
multiplied by 0.3 when the log contains a port-binding keyword (port, unknown module, not a
module), and falling back to 0.5 when the log cannot be parsed.

Binary search for β ∗ . The binary search for β ∗ operates on [10−6 , 106 ] with 64 iterations at the
current step’s KL budget δt . TTT-Discover [Yuksekgonul et al., 2026] sets δt ≡ ln 2 as a constant;
we report this as the fixed baseline in the KL-budget ablation (Table 3). RTL-Discover replaces
the constant with the adaptive controller of Section 3.4; its hyperparameters are listed in Table 9.
Intuitively, the constant ln 2 enforces that the group’s softmax distribution is no more concentrated
than a Bernoulli(0.5) distribution, preventing the policy gradient from collapsing to a single rollout
even when reward differences are large; the adaptive controller relaxes this hard cap and instead
modulates δ between 0.25 ln 2 and 4 ln 2 in response to the four EMA signals described in Section 3.4.

Signals and EMA update. At step t, given the batch of G groups produced by δt−1 , the controller
measures four scalar signals: (i) the average policy-vs-reference KL KLref , (ii) the effective number
                                                      1
                                                        PG P 2 −1
of distinct rollouts averaged across groups, eff-n = G     g=1 (  i qg,i ) , (iii) the fraction of groups
with degenerate (constant) reward, const-frac, and (iv) the binary-search saturation rate βmax -rate
(the fraction of groups whose β ∗ hits the search bound 106 ). Each signal is smoothed by a single
EMA with mixing α = 0.30:
             x̄t = (1 − α) x̄t−1 + α xt ,     x ∈ {KLref , eff-n, const-frac, βmax -rate}.             (8)
A separate slower EMA with αr = 0.10 tracks the running peak reward r̄t used by the stagnation
counter Nnoimp , which is incremented when the batch maximum fails to exceed r̄t−1 by at least
∆rmin = 0.02 and reset to 0 whenever a new peak is observed.

Priority ladder. For the first Twarm = 20 steps only the KL brake (P1) is active, with δt ≡ δ0
otherwise. Past warm-up, the ladder evaluates P1–P4 in order and applies the assignment of the first
rule whose guard holds; if none holds, δt ← δt−1 (hold).
      (P1) KL brake: KLref t > τKL ⇒ δt ← δ0 ,                                                        (9)
(P2) winner-take-all: βmax -ratet > τβ ∧       eff-nt < τnwta   ⇒ δt ← max(ρ− δt−1 , δmin ),         (10)
     (P3) stagnation:    Nnoimp ≥ Tstag ∧ const-fract < τconst ∧        eff-nt < τnstag   ⇒ δt ← max(ρ− δt−1 , δmin ),
                                                                                                  (11)
                                                  lo
(P4) over-exploring: eff-nt > τn ∧ const-fract < τconst ∧ Nnoimp < Tplat ⇒ δt ← min(ρ+ δt−1 , δmax ).
                                                                                   (12)
The eff-n joint gates on P2 and P3 (τnwta , τnstag ) are essential: they prevent the controller from
shrinking δ when group weights are already near uniform (a flat-reward regime that would collapse


                                                   17
the advantages to zero on further shrinkage), and instead require that the rule that fires acts on a
genuinely concentrated group.




                                                18
Table 4: Per-design ratio on RTLLM v2.0 (lower is better; bold = best per row; “–” = method failed
to produce compilable RTL). All four methods report the PPA-product ratio A·D·P against the same
v2.0 reference; EvolVE / VeriAgent / REvolution numbers are taken from Ping et al. [2026], Table 3
(GPT-4o-mini).
         Design                         ref M    EvolVE   VeriAgent   REvolution   TTT-RTL
         JC_counter                    10180.4    1.000     1.000       1.000       1.000
         LFSR                             93.5    1.140     1.140       1.140       1.000
         LIFObuffer                    28866.5    1.000     0.770       0.770       0.632
         RAM                           63406.1    1.083     1.026       1.026       1.036
         ROM                              46.3    1.000     1.000       0.964       1.000
         accu                          82040.8    1.000     0.904       0.885       0.760
         adder_16bit                    3513.1    1.000     0.955       0.955       0.872
         adder_32bit                   25037.3    0.967     0.939       0.967       0.235
         adder_8bit                      440.0    1.152     1.152       1.152       0.014
         adder_bcd                       484.6    0.638     0.617       0.638       0.943
         adder_pipe_64bit            6109235.7    0.423     0.423       0.423       0.094
         alu                         3192539.6    0.375     0.348       0.321       0.241
         asyn_fifo                    580752.5      –         –           –           –
         barrel_shifter                   94.4    1.127     1.127       1.127       0.840
         calendar                       9374.5    0.953     0.840       0.953       0.548
         comparator_3bit                  10.2    0.664     0.600       0.664       0.454
         comparator_4bit                  26.9    0.621     0.586       0.621       0.234
         counter_12                      824.7    1.000     1.000       1.000       0.940
         div_16bit                  94019995.7    1.089     1.045       1.089       0.510
         edge_detect                      40.5    1.000     0.904       0.904       0.086
         fixed_point_adder            233273.1    0.752     0.752       1.000       0.062
         fixed_point_subtractor       354996.9    0.888     0.824       0.888       0.201
         float_multi               914343626.2    0.453     0.453       0.453       0.129
         freq_div                       4986.7    0.561     0.526       0.561       0.417
         freq_divbyeven                  290.5    1.574       –           –         0.607
         freq_divbyfrac                  388.2      –         –           –         0.561
         freq_divbyodd                  2347.5      –         –           –         0.425
         fsm                             429.1    0.476     0.297       0.476       0.011
         instr_reg                      2415.7    1.000     1.000       1.000       0.143
         multi_16bit                 2354913.0    0.342     0.342       0.342       0.335
         multi_8bit                   725109.1    1.000     0.771       0.153       0.311
         multi_booth_8bit             196035.4    0.989     0.918       0.918       0.691
         multi_pipe_4bit               11025.1    1.000     0.884       0.734       0.750
         multi_pipe_8bit              584498.4    1.319     1.000       1.000       0.149
         parallel2serial                 450.8    1.000     0.965       0.771       0.726
         pe                        224095126.1    1.000     1.000       0.986       0.996
         pulse_detect                    153.2    1.000     0.727       0.075       0.174
         radix2_div                    88514.0    0.973       –         0.973       0.011
         right_shifter                   108.5    1.000     1.000       1.000       1.000
         ring_counter                    263.1    1.000     1.000       1.000       0.425
         sequence_detector               211.0    1.040     1.040       1.000       0.041
         serial2parallel               14019.8    1.027     1.000       1.000       0.782
         signal_generator                678.1    0.906     0.894       0.738       0.705
         square_wave                   12354.9    1.066     1.000       0.954       0.108
         sub_64bit                    238797.5    0.995     0.899       0.890       0.885
         synchronizer                    671.8    1.000     0.847       0.706       1.000
         traffic_light                 32088.5    1.000     1.000       1.000       0.561
         up_down_counter              101304.7    1.000     1.000       0.584       0.878
         width_8to16                   14891.7    0.960     1.000       0.960       0.253
         GeoMean (common, N =44)            –     0.872     0.813       0.739       0.349
         #Best / 44                         –      0.5       2.0         8.0        33.5




                                                 19
Table 5: Representative per-design comparison of the v2.0 reference RTL under our local flow
vs. the published numbers [Ping et al., 2026]. Area in µm2 , delay in ns, power in µW; the ∆
columns are signed relative error (ours − pub)/pub. Area and delay are closely matched on the
vast majority of designs; absolute power shows larger discrepancies driven by OpenSTA activity /
reporting assumptions, which is the reason we only report ratios against the shared reference in the
main comparison. Two outlier-style cases (RAM and asyn_fifo, where Yosys infers different array /
synchronizer structures across flows) are included for completeness.
  Design                  Apub      Aours             ∆A   Dpub      Dours            ∆D        Ppub         Pours           ∆P
  comparator_3bit         12.0       12.0       +0.0%       0.15      0.16        +6.7%           5.7        4.7       −18.3%
  adder_8bit              48.9       48.9       +0.0%       0.31      0.34        +9.7%          29.0       16.8       −42.1%
  calendar               164.1      164.9       +0.5%       0.42      0.47       +11.9%         136.0      105.0       −22.8%
  adder_16bit             96.8       94.7       −2.2%       0.59      0.67       +13.6%          61.5       40.4       −34.3%
  adder_32bit            208.5      211.2       +1.3%       0.87      0.91        +4.6%         138.0       85.1       −38.3%
  alu                   1953.0     1967.1       +0.7%       1.93      2.10        +8.8%         847.0      688.0       −18.8%
  multi_16bit            951.5      933.9       −1.8%       1.98      2.19       +10.6%        1250.0      796.0       −36.3%
  adder_pipe_64bit      2529.4     2523.5       −0.2%       0.83      0.90        +8.4%        2910.0     1920.0       −34.0%
  pe                    3649.5     3640.2       −0.3%       1.72      1.91       +11.0%       35700.0     1400.0       −96.1%
  Outlier-style cases (different inferred structure across flows)
  RAM                     474.8      633.9     +33.5%        0.22     0.32       +45.5%         607.0      479.0       −21.1%
  asyn_fifo             1099.9      1341.7     +22.0%        0.33     0.87      +163.6%        1600.0     1140.0       −28.7%




Table 6: Aggregate flow-sanity statistics over the RTLLM v2.0 designs that synthesize cleanly under
both flows. The Area row covers all 47 designs that complete area synthesis under both flows; the
Delay and Power rows are restricted to the 43-design subset for which both flows also produce a
valid OpenSTA timing report (designs where one flow returns a delay-floor or missing-power report
are excluded from those two rows only). Error is signed relative error of our local measurement
against the published value; within-X% counts designs whose absolute relative error is at most
X. The takeaway is that the PPA product’s area and delay components are tightly matched, and
the residual cross-flow discrepancy lives almost entirely in absolute power—which the main-result
protocol absorbs by reporting only ratios against the shared v2.0 reference.
                          Component         median |err|   mean |err|        within 5%     within 15%
                          Area                 0.6%           6.9%            36/47          43/47
                          Delay                8.2%          13.4%            19/43          39/43
                          Power               31.3%          35.8%            4/43           13/43




Table 7: Paired multi-seed comparison on ct_vfmau_lza_simd_half (sky130, n = 4 adaptive vs.
4 fixed, 100 RL steps each). Mean ± std across seeds; p-values are paired t-test. No metric reaches
p < 0.05.
    Metric                                   Direction         adaptive           fixed δ = ln 2         ∆           paired p
    best_reward_ever                              ↑        21.96 ± 0.56          21.30 ± 1.48           +0.67         0.32
    end_reward_last20                             ↑        19.01 ± 1.60          19.44 ± 2.00           −0.43         0.57
    step_to_score ≥ 20                            ↓         44.5 ± 33.3           69.5 ± 77.7           −25.0         0.42
    const_group_frac_last20                       ↓         0.46 ± 0.18           0.52 ± 0.09           −0.06         0.58




                                                              20
           Table 8: TTT-RTL hyperparameter configuration used in all experiments.
 Hyperparameter                 Value
 Base model                             RTLLM v2.0: Qwen3-8B + ttt-rtl-sft step 18 (Sec-
                                        tion G); C910 LZA: raw Qwen3-8B (no SFT)
 Gradient steps per problem             100
 Batch size (parent states)             4
 Rollouts per prompt (n)                4 (RTLLM v2.0 main runs) / 8 (C910 LZA ablations)
 PUCT exploration coefficient (c)       1.0
 State pool size (Cmax )                500
 Top-k children per parent              2
 Reward weight ωsyn                     0.1
 Reward weight ωfunc                    1.0
 Reward weight ωppa                     10.0
 KL budget δt for β ∗ search            RTLLM v2.0: fixed δ = ln 2 (TTT-Discover canonical); C910
                                        LZA: per-row, see Table 3 (incl. adaptive controller of Table 9,
                                        range [0.25 ln 2, 4 ln 2])
 Technology library                     Nangate 45 nm (RTLLM v2.0) / Sky130 HD (C910 LZA)
 Synthesis tool                         Yosys
 Functional simulation                  iverilog / vvp
 Training framework                     verl [Sheng et al., 2024]




Table 9: Hyperparameters of the adaptive KL-budget controller (Section 3.4). All values are held fixed
across all problems and PDKs reported in this paper. Symbols match the priority-ladder description
in Section 3.4.
              Symbol     Description                                                  Value
              δ0         Init / KL-brake reset value                            ln 2 ≈ 0.693
              δmin       Lower bound of δt                                 0.25 ln 2 ≈ 0.173
              δmax       Upper bound of δt                                    4 ln 2 ≈ 2.773
              ρ−         Shrink factor (P2, P3)                                         0.85
              ρ+         Grow factor (P4)                                               1.20
              α          EMA mixing for KL / eff-n / const-frac / β-rate                0.30
              αr         EMA mixing for reward peak tracking                            0.10
              τKL        P1 KL-brake threshold                                          0.40
              τβ         P2 winner-take-all β-rate threshold                            0.60
              τnwta      P2 eff-n joint gate (sharp groups only)                         3.5
              Tstag      P3 stagnation steps                                              15
              ∆rmin      P3 minimum relative improvement                                0.02
              τconst     P3 const-frac guard (signal exists)                            0.70
              τnstag     P3 eff-n joint gate (sharp groups only)                         4.0
              τn         P4 effective-n threshold                                        5.5
                lo
              τconst     P4 const-frac threshold                                        0.30
              Tplat      P4 plateau guard (steps)                                          5
              Twarm      Warm-up steps (P1 only)                                          20




                                                    21
NeurIPS Paper Checklist
    1. Claims
       Question: Do the main claims made in the abstract and introduction accurately reflect the
       paper’s contributions and scope?
       Answer: [Yes]
       Justification: The abstract and introduction state three contributions: (i) a per-design
       test-time training framework that closes the LLM–EDA loop (Section 3), (ii) external
       comparison on RTLLM v2.0 reporting a 65.1% geomean PPA-product reduction vs. the
       v2.0 reference, against 26.1% for the strongest published baseline (Table 1, Section 4.2),
       and (iii) an industrial C910 LZA case study with a 59.4% ADP reduction and compo-
       nent ablations (Table 3, Section 4.3). The adaptive KL-budget controller is framed as a
       robustness/task-responsiveness observation rather than a peak-performance win, matching
       the multi-seed evidence in Section D.
    2. Limitations
       Question: Does the paper discuss the limitations of the work performed by the authors?
       Answer: [Yes]
       Justification: (L1) Single-seed main results. RTLLM v2.0 and the C910 main-table
       results are single-seed (matching the published agent baselines, none of which report seed
       variance); a four-seed paired replication on LZA simd_half and a single-seed case study
       on ct_vfdsu_fadd_close_s0_d (Section D) confirm direction and a ∼2.6× seed-wise
       variance reduction but do not reach p < 0.05 at n = 4, so per-row gaps in Table 3 should be
       read as ranking evidence rather than tight effect sizes. (L2) Simulation-only correctness.
       Designs are validated against the RTLLM testbench, not formal equivalence; a Yosys eqy
       check is the natural next step, as is timing-accurate synthesis (OpenROAD [Ajayi et al.,
       2019] or commercial flows) for more reliable PPA estimates. (L3) Internal ablation of the
       controller. We do not yet report a leave-one-rule-out study of P1–P4 within the adaptive
       controller, so we cannot claim which rule drives the gain. Section D additionally documents
       the controller’s negative results: no metric reaches p < 0.05 at n = 4 on LZA, the fadd
       δ raise post-dates the breakthrough, and the +0.67 peak gap lies inside the development
       spread of 15.6–25.7 best-so-far reward observed across development repeats of adaptive-δ +
       PUCT on the C910 unit.
    3. Theory assumptions and proofs
       Question: For each theoretical result, does the paper provide the full set of assumptions and
       a complete (and correct) proof?
       Answer: [N/A]
       Justification: The paper does not prove new theorems. Section 3 reuses the entropic
       policy-gradient objective and binary-search β ∗ from TTT-Discover [Yuksekgonul et al.,
       2026] and adds an empirical control rule (Section 3.7); we do not claim convergence or
       optimality results.
    4. Experimental result reproducibility
       Question: Does the paper fully disclose all the information needed to reproduce the main
       experimental results of the paper to the extent that it affects the main claims and/or conclu-
       sions of the paper?
       Answer: [Yes]
       Justification: Section 4 and Section F specify the base model (RTLLM v2.0: Qwen3-8B
       + ttt-rtl-sft step 18; C910 LZA: raw Qwen3-8B with no SFT), training framework
       (verl), 100-step budget, B = 4 parents, n ∈ {4, 8} rollouts, PUCT c = 1.0, pool cap
       Cmax = 500, reward weights (Equation (3)), KL-budget controller hyperparameters (Ta-
       ble 9), PDKs (Nangate 45 nm, Sky130 HD), tools (Yosys, OpenSTA, iverilog), seed (42), and
       prompt templates (Section H). The artifact (to be released on GitHub) ships per-rollout logs,
       all generated Verilog, synthesis scripts, liberty-file manifests, and machine-readable result
       tables; re-evaluating any reported ratio from the released Verilog requires no retraining.
    5. Open access to data and code
       Question: Does the paper provide open access to the data, code, and instructions needed to
       faithfully reproduce the main experimental results, as described in supplemental material?
       Answer: [Yes]
       Justification: All datasets and PDKs are public: RTLLM v2.0 [Lu et al., 2024, Liu et al.,


                                               22
    2025], the open-source XuanTie C910 RTL [Chen et al., 2020], Nangate 45 nm and Sky130.
    The artifact (to be released on GitHub under Apache 2.0) contains synthesis scripts, generated
    Verilog, prompts, and result CSVs; the training code and SFT checkpoint will be released
    alongside.
 6. Experimental setting/details
    Question: Does the paper specify all the training and test details (e.g., data splits, hyperpa-
    rameters, how they were chosen, type of optimizer, etc.) necessary to understand the results?
    Answer: [Yes]
    Justification: Per-run hyperparameters are in Section 4 (training config, sampling budget,
    baselines, synthesis flow, PDK choice) and Section F and Table 9. We also disclose the hy-
    perparameter selection protocol: TTT-Discover defaults are inherited unmodified except for
    the adaptive KL-budget controller, whose thresholds were fixed once on the C910 LZA pilot
    and held constant across all 49 RTLLM v2.0 designs and the second C910 unit (Section 3.7,
    Section D).
 7. Experiment statistical significance
    Question: Does the paper report error bars suitably and correctly defined or other appropriate
    information about the statistical significance of the experiments?
    Answer: [Yes]
    Justification: The main RTLLM v2.0 and C910 main-table numbers are single-seed, match-
    ing all three published agent baselines (none of EvolVE / VeriAgent / REvolution report
    seed variance), and we say so explicitly in Section 4 and Table 3 (“All rows are single-seed”).
    For the adaptive vs. fixed δ contrast, Section D reports a four-seed paired replication on
    LZA simd_half with mean ± std and paired t-test p-values for four metrics (Table 7), an
    exhaustive enumeration over all 24 adaptive-to-fixed pairings, leave-one-out checks, and
    a single-seed second-task replication on fadd_close_s0_d. The negative-significance
    results are reported alongside the positive variance-reduction result.
 8. Experiments compute resources
    Question: For each experiment, does the paper provide sufficient information on the com-
    puter resources (type of compute workers, memory, time of execution) needed to reproduce
    the experiments?
    Answer: [Yes]
    Justification: All experiments use A800 GPUs. RTLLM v2.0: each of the 49 designs runs
    on 2 nodes × 4 A800 GPUs (8 GPUs total), wall-clock ∼2 h per design (∼16 GPU-h per
    design); the full 49-design sweep is ∼780 GPU-h. C910 LZA ablations: each row runs on 1
    node × 8 A800 GPUs, wall-clock ∼4.5 h per row (∼36 GPU-h per row); the 8 ablation rows
    in Table 3 total ∼320 GPU-h. The seed and replication protocol is in Section 4 (“Compute
    and seed protocol”).
 9. Code of ethics
    Question: Does the research conducted in the paper conform, in every respect, with the
    NeurIPS Code of Ethics?
    Answer: [Yes]
    Justification: The work uses publicly released model weights (Qwen3-8B), public bench-
    marks (RTLLM v2.0), and the open-source XuanTie C910 RTL under their respective
    permissive licenses. No human subjects, no crowdsourcing, no scraped or private data are
    involved. The synthesized RTL is hardware-design output, not personal data.
10. Broader impacts
    Question: Does the paper discuss both potential positive societal impacts and negative
    societal impacts of the work performed?
    Answer: [Yes]
    Justification: TTT-RTL targets PPA reduction in fixed-function hardware modules, which
    can reduce energy and silicon area for deployed designs. Negative impacts are limited: the
    framework requires both an LLM and a full EDA flow, so it does not lower the barrier to
    malicious hardware generation beyond what is already achievable with standard EDA tools.
    We do not foresee dual-use risk that would warrant a release-time gating mechanism beyond
    the standard model card.
11. Safeguards
    Question: Does the paper describe safeguards that have been put in place for responsible


                                             23
    release of data or models with a high risk for misuse (e.g., pretrained language models,
    image generators, or scraped datasets)?
    Answer: [N/A]
    Justification: We release fine-tuned Verilog-domain weights of an existing public base model
    (Qwen3-8B) plus per-design rollout logs and synthesis scripts. The artifact does not contain
    scraped data, pretrained generative models for natural-language or image content, or any
    content with elevated misuse risk relative to the base model.
12. Licenses for existing assets
    Question: Are the creators or original owners of assets (e.g., code, data, models), used in
    the paper, properly credited and are the license and terms of use explicitly mentioned and
    properly respected?
    Answer: [Yes]
    Justification: All third-party assets are cited in-text and respected in license: Qwen3-8B
    [Yang et al., 2025] (Apache 2.0), verl [Sheng et al., 2024] (Apache 2.0), Yosys [Wolf and
    Glaser, 2013] (ISC), OpenSTA (GPLv3), iverilog (GPLv2), Nangate Open Cell Library
    45 nm (Apache-style), Sky130 PDK (Apache 2.0), RTLLM v2.0 [Lu et al., 2024, Liu et al.,
    2025] (MIT), the XuanTie C910 RTL [Chen et al., 2020] (Apache 2.0), and baseline numbers
    from Ping et al. [2026] (released under MIT). Per-asset versions are listed in Sections 4
    and F.
13. New assets
    Question: Are new assets introduced in the paper well documented and is the documentation
    provided alongside the assets?
    Answer: [Yes]
    Justification: New assets are: (a) the TTT-RTL training code, (b) the ttt-rtl-sft SFT
    checkpoint, (c) generated Verilog for all 49 × 4 = 196 method×design rollout pools, and (d)
    the reference_ppa_measured.csv flow-sanity table (Section B). The artifact contains a
    top-level README with the directory layout, run instructions, license (Apache 2.0), and
    per-design provenance metadata. Section F doubles as a model card for the SFT checkpoint.
14. Crowdsourcing and research with human subjects
    Question: For crowdsourcing experiments and research with human subjects, does the paper
    include the full text of instructions given to participants and screenshots, if applicable, as
    well as details about compensation (if any)?
    Answer: [N/A]
    Justification: No crowdsourcing or human-subjects studies were conducted. All evaluation
    signals come from automated EDA tools (Yosys, OpenSTA, iverilog) on public Verilog
    inputs.
15. Institutional review board (IRB) approvals or equivalent for research with human
    subjects
    Question: Does the paper describe potential risks incurred by study participants, whether
    such risks were disclosed to the subjects, and whether Institutional Review Board (IRB)
    approvals (or an equivalent approval/review based on the requirements of your country or
    institution) were obtained?
    Answer: [N/A]
    Justification: No human-subjects research was performed; IRB review does not apply.
16. Declaration of LLM usage
    Question: Does the paper describe the usage of LLMs if it is an important, original, or
    non-standard component of the core method development in this research?
    Answer: [Yes]
    Justification: An LLM is the central object of study—the policy that TTT-RTL fine-tunes per
    design. The base model (Qwen3-8B), the SFT corpus (ttt-rtl-sft, step 18), the training
    framework (verl), the prompt templates (Section H), and all training-time hyperparameters
    (Tables 8 and 9) are documented in Section 4 and the appendix. LLMs were not used as a
    tool for paper writing or experiment design beyond standard authorial assistance, and any
    such use does not affect the reported methodology, results, or originality.




                                             24
