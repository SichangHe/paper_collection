                                                     Monotonic Reference-Free Refinement for
                                                               Autoformalization


                                                                     Lan Zhang1 , Marco Valentino2 , André Freitas1,3,4
                                                     1
                                                         Department of Computer Science, University of Manchester, United Kingdom
                                                           2
                                                             School of Computer Science, University of Sheffield, United Kingdom
                                                                           3
                                                                             Idiap Research Institute, Switzerland
                                                         4
arXiv:2601.23166v2 [cs.CL] 7 May 2026




                                                           National Biomarker Centre, CRUK Manchester Institute, United Kingdom
                                                                       lan.zhang-6@postgrad.manchester.ac.uk



                                                                                       Abstract

                                                    While statement autoformalization has advanced rapidly, full-theorem autofor-
                                                    malization remains largely unexplored. Existing iterative refinement methods in
                                                    statement autoformalization typically improve isolated aspects of formalization,
                                                    such as syntactic correctness, but struggle to jointly optimize multiple quality
                                                    dimensions, which is critical for full-theorem autoformalization. We introduce
                                                    a reference-free iterative monotonic process at inference time for full-theorem
                                                    autoformalization that leverages complementary feedback from theorem provers
                                                    and LLM-based judges, without access to ground-truth or existing formalizations
                                                    and without human intervention. Our approach optimizes a masked composite
                                                    objective over Formal Validity, Logical Preservation, Mathematical Consistency,
                                                    and Formal Quality, guided by a responsiveness map that indicates how different
                                                    LLMs acting as different roles preferentially improve each dimension. We further
                                                    propose an acceptance policy that guarantees certified monotonic improvement, and
                                                    provide conditions ensuring convergence and termination. Empirical experiments
                                                    demonstrate the proposed process enables simultaneous improvement across multi-
                                                    ple dimensions, achieving 100.00% formal validity and a 90.27% overall score on
                                                    miniF2F, and 77.96% formal validity and a 52.45% overall score on ProofNet.


                                        1    Introduction
                                        Recent advances in Large Language Models (LLMs) have substantially improved their ability to
                                        perform mathematical reasoning [Shao et al., 2024, 2025, Petrov et al., 2025, Zhang et al., 2025a].
                                        However, reasoning trajectories expressed in natural-language mathematics are difficult to verify
                                        automatically, posing a major challenge for reliably evaluating instances generated through mathe-
                                        matical discovery [Romera-Paredes et al., 2024, Naskrecki and Ono, 2025]. Autoformalization [Wu
                                        et al., 2022, Yang et al., 2025] provides a crucial bridge between informal and formal mathematics by
                                        converting informal reasoning into transparent and mechanically verifiable formalizations. Existing
                                        autoformalization research has primarily focused on statement formalization [Zhang et al., 2024, Lu
                                        et al., 2024, Li et al., 2024, Gao et al., 2025], often omitting full formal proofs by relying on “sorry”
                                        placeholders. However, proof-level autoformalization is equally essential for faithfully verifying the
                                        correctness of natural-language mathematical reasoning and remains an underexplored yet critical
                                        direction.
                                        Given a natural-language theorem and its accompanying proof, full-theorem autoformalization aims
                                        to produce a complete formalization consisting of both a formal statement and a fully verified formal
                                        proof. While this task could in principle be approached by combining statement autoformalization
                                        with automated theorem proving (ATP), such a pipeline may introduce error propagation, and the two

                                        Preprint.
                                                                      Monotonic Reference-Free Refinement

                                                                                                                        ,   ,...                                  Acceptance Policy
                                                                             theorem ...:=by...               theorem ...:=by...                                     Based on
       Mathematical
    Statement and Proof
                                               One-Off
                                              Generators
                                               (OOGs)                        theorem ...:=by...



                                                                                                                  FV-Repairers
                                                                             theorem ...:=by...                     (FVRs)


       theorem name                                                                                         Incorrect       Correct                                 theorem name
       (hyps): claim:=by                                                                                                                                            (hyps): claim:=by
       have ...                               Recurrent                                                                                                             have ...
       tactics ...                            Generators                     theorem ...:=by...                                                                     tactics ...
                                                (REGs)

                                                                                                                                               Judges
                                                                                                 Next Iteration




   NL Statement: For an element in         show that and       have the same order.
   NL Proof: Recall that the order of a group element is either a positive integer or                        theorem order_of_inverse (G :
   infinity. Suppose    is infinite and that          for some . Then                                        Type*) [Group G] (x : G) : orderOf               theorem
                                                                                                             x = orderOf x⁻¹ := by                            order_of_inverse {G :
                                                                                                               have h₁ : orderOf x = orderOf                  Type*} [Group G] (x : G) :
                                                                                                             x⁻¹ := by                                        orderOf x = orderOf x⁻¹
                                                                                                                apply Eq.symm                                 := by
   a contradiction. So if     is infinite,       must also be infinite. Likewise, if       is                   apply Eq.symm                           ...
                                                                                                                     rw [← orderOf_injective                    rw [← orderOf_inv]
   infinite, then                    is also infinite. Suppose now that           and
                                                                                                             (MulAut.conj       x).toMonoidHom                  <;> simp
         are both finite. Then we have                                                                       (MulAut.conj x).injective x⁻¹]                   [orderOf_eq_zero_iff]
                                                                                                                      simp [MulAut.conj_apply,                  <;> aesop
                                                                                                             mul_assoc,           mul_right_inj,
                                                                                                             mul_left_inj]
   so that          . Likewise,        . Hence          and    and        have the same order.                exact h₁




Figure 1: Schematic illustration of the monotonic process with an example. In this process, One-Off
Generators (OOGs) produce formalizations from scratch, Recurrent Generators (REGs) refine the
current best formalization using feedback from LLM judges, and FV-Repairers (FVRs) correct
formally invalid candidates generated by OOGs and REGs. The acceptance policy retains only the
formalization estimated to have the highest quality among all candidates and the previous best.

tasks are typically studied in isolation. In contrast, we formulate full-theorem autoformalization as a
single, unified task in which the formal statement and the formal proof are generated jointly.
To obtain higher-quality full-theorem formalizations, we argue that four dimensions must be con-
sidered: (i) Formal Validity (FV), which ensures that the formal reasoning process is mechanically
verified by the theorem prover; (ii) Logical Preservation (LP) and Mathematical Consistency (MC),
which ensure semantic alignment with the original informal theorem; and (iii) Formal Quality (FQ),
which captures properties such as clarity, structure, and reusability of the resulting formalization.
The process of full-theorem autoformalization is inherently a multi-dimensional optimization problem.
However, relying on a single LLM at test time to perform full-theorem autoformalization, whether
through vanilla prompting [Wu et al., 2022] or refinement-based methods [Zhang et al., 2024], offers
limited potential for simultaneously improving multiple dimensions. Moreover, different LLMs used
for refinement often exhibit distinct biases toward particular dimensions of formalization quality. This
observation motivates the following research question: ‘How can we leverage the complementary
strengths of different LLMs to improve full-theorem autoformalization across multiple objectives at
test time?’
To address this research question, we propose a unified objective that accounts for all relevant
dimensions, and design a reference-free, iterative, monotonic optimization process at test time that
yields non-decreasing improvement with high probability under theoretical guarantees. Our main
contributions are summarized as follows:
1. To the best of our knowledge, we are the first to formally define full-theorem autoformalization
and to study it using LLM-based methods. We propose a masked composite objective for this task
that jointly considers multiple quality dimensions, including a hard constraint, Formal Validity (FV),
and several soft dimensions: Logical Preservation (LP), Mathematical Consistency (MC), and Formal
Quality (FQ).
2. We decompose the roles of LLMs in full-theorem autoformalization into three categories: One-Off
Generators (OOG), FV-Repairers (FVR), and Recurrent Generators (REG). The FVRs and REGs can


                                                                                                        2
leverage feedback to refine formalizations along different quality dimensions. We further introduce a
responsiveness map that models the expected, dimension-specific improvements induced by each
generator, thereby enabling sample-efficient generator selection.
3. We propose a monotonic optimization process at test time (Figure 1) that employs an acceptance
policy aggregating signals from both theorem prover and LLM-based judges, without access to ground-
truth or existing formalizations and without human involvement in selection, ensuring non-decreasing
certified progress across iterations. This acceptance rule leverages a lower confidence bound (LCB)
assumption to quantify uncertainty in LLM-based judges when evaluating soft dimensions.
4. We empirically demonstrate that specialized mathematical LLMs and general-purpose LLMs
exhibit complementary strengths across different generator roles, and that our iterative framework
effectively ensembles these strengths to achieve monotonic improvement under realistic evaluation
noise. For full-theorem autoformalization on the miniF2F and ProofNet benchmarks, our final
monotonic process achieves 100.00% and 77.96% formal validity, as verified by the Lean4 theorem
prover, and overall scores of 90.27% and 52.45%, based on combined judgments from the theorem
prover and GPT-4.1-mini judges, respectively.

2     Monotonic Test-Time Optimization for Full-Theorem Autoformalization
2.1   Problem Statement

The task of full-theorem autoformalization can be formally defined as follows: given a mathematical
statement snl expressed in natural language and its corresponding proof pnl , the goal is to automat-
ically obtain a formal representation x = (s, p) consisting of a formal statement s and a proof p,
where s must be semantically aligned with snl , and p should have a similar reasoning process to pnl
but does not necessarily follow the exactly same reasoning steps. The essence of a formalization
x = (s, p) with good quality can be categorized to four dimensions:
Formal Validity (FV). The full theorem formalization should be formally valid such that the formal
statement s must be syntactically correct and the formal proof p entails such formal statement. This
formal validity can be rigorously checked by the relevant theorem prover. This is also commonly
referred to as Pass rate.
Logical Preservation (LP). The formal theorem s must capture the logical content and inferential
structure of snl .
Mathematical Consistency (MC). The formal theorem s must coherently and accurately represent
the mathematical objects and operations present in snl .
Formal Quality (FQ). The full theorem formalization x should intrinsically have high-quality in
terms of structural clarity and conciseness. For instance, the full theorem formalization should contain
non-redundant statements and reasoning steps.
FV, LP, MC are essential for a complete and correct formalization of a theorem. Without FV, the
formalization is practically unusable. If LP or MC is lost, the formalization no longer represents the
natural-language theorem, resulting in a non-target formalization even if it remains formally valid.
Although FQ is not strictly necessary, it remains a desirable property, particularly in contexts where
the formalization is intended for reuse, such as in the construction of formal libraries.

Dimension Scores. Let X be the space of all possible candidate formalizations. We score each
candidate x by
                  π(x) = πFV (x), πLP (x), πMC (x), πFQ (x) ∈ [0, 1]4 ,
                                                            
                                                                                          (1)
where πFV (x)       ∈    {0, 1} indicates the pass status from theorem prover, and
πLP (x), πMC (x), πFQ (x) ∈ [0, 1] indicate evaluations on soft dimensions. The goal of full
theorem autoformalization is an optimization process to automatically select the ideal formalization
x⋆ ∈ X such that π(x⋆ ) = (1, 1, 1, 1).

Masked Composite Objective.         For the optimization process, we define an objective function:
                                    1                                    
                        JOA (x) =     πFV (x) πLP (x) + πMC (x) + πFQ (x) ,                          (2)
                                    3

                                                   3
The multiplicative factor πFV ∈ {0, 1} is a mask since it enforces FV as a hard constraint while
retaining a single scalar potential for the soft dimensions. This objective function (i) precludes
selecting invalid-but-high soft scores; (ii) simplifies acceptance since it is not required to handle
penalties and slack variables separately; (iii) matches downstream utility where FV is binary and
primary. For the ideal formalization, we have JOA (x⋆ ) = 1.

2.2     Approximation with LLM Judges

The automatic evaluation on soft dimensions πLP (x), πMC (x), πFQ (x) in JOA (x) is inherently
intractable. Previous work [Zhang et al., 2025b] indicates the ability of using LLM judges for the
evaluation of certain aspects of formalizations, however, LLM judges can be ambiguous and should
be accepted under uncertainty. We make the following assumptions for LLM judges:
Assumption 2.1. We assume that for each soft dimension i ∈ {LP, MC, FQ}, the fused estimator
                                                 Ki
                                                            (k)
                                                 X
                                      π
                                      bi (x) =         wi,k π
                                                            bi (x).                                   (3)
                                                 k=1

                             (k)
constructed from signals πbi (x) ∈P[0, 1], k = 1, . . . , Ki produced by a set of Ki LLM judges,
where weights satisfy wi,k > 0 and k wi,k = 1, satisfy the following:
(i) Asymptotic stability: After asymptotic calibration of weights and LLM judgments, for every x,
each πbi (x) is a deterministic value almost surely;
(ii) Measurable uncertainty: There exists a one-sided lower confidence bound for the true πi (x) at
uncertainty level δi ∈ (0, 1), given by:
                                                             
                               Pr πbi (x) − mi (δi ) ≤ πi (x) ≥ 1 − δi ,                        (4)
where the margin term mi (δi ) > 0 absorbs calibration error, inter-judge correlation, and distributional
drift.

Assumption 2.1 formalizes the reliability of LLM judges. Specifically, (i) asserts that their judgments
are stable across comparisons, and (ii) limits the likelihood that low-quality formalizations are
mistakenly evaluated favorably along soft dimensions, with such errors occurring with probability at
most δi . We provide a naive uncertainty estimation for LLM judges using Eq. 4 in Appendix F.3.
Theorem 2.2 (Lower Confidence Bound of JOA ). Assuming that the evaluations of LP, MC and FQ
are independent, there exists a lower confidence bound for the masked composite objective JOA (x)
given by:
             1         h                                                                     i
LCBδ (x) = πFV (x) π     bLP (x)−mLP (δLP ) + π   bMC (x)−mMC (δMC ) + π  bFQ (x)−mFQ (δFQ )
             3
                                                                                              (5)
with uncertainty level δ = 1 − (1 − δLP )(1 − δMC )(1 − δFQ ).

Proof. See Appendix A.

Theorem 2.2 establishes a lower confidence bound for the masked composite objective, enabling its
use in an LCB-based optimization framework.

2.3     The Monotonic Optimization Process

We propose a monotonic process {xt } that gradually generates candidate formalizations and selects
the one most likely to achieve the highest quality.

2.3.1    Candidate Generation
Let Ct ⊆ X denote the set of candidate formalizations obtained at step t. Maintaining diversity within
Ct is crucial for covering the space of possible formalizations as comprehensively as possible. We
define G = {G1 , . . . , GM } as the set of generators to sample candidate formalizations from X . We
classify generators into three categories:


                                                   4
One-Off Generator (OOG). The one-off generator G assigns a fixed distribution over samples
conditioned on (snl , pnl ), generating outputs according to x ∼ pG (x | snl , pnl ).

FV-Repairer (FVR). Given that the objective places the highest priority on formal validity,the
FV-Repairer G is designed to correct instances in which πFV (x) = 0, such that Pr πFV G(x) =
 
1 > 0.

Recurrent Generator (REG). The recurrent generator G assigns a fixed distribution over samples
conditioned on (snl , pnl ) and a previous candidate formalization xt−1 , generating outputs according
to xt ∼ pG (x | snl , pnl , xt−1 ).
In practice, the one-off generator can rely on few-shot prompting [Wu et al., 2022] or retrieval-
augmented generation [Zhang et al., 2025c, Liu et al., 2025a]. The FV-repairer may be implemented
using either LLM-based approaches [Zhang et al., 2024] or rule-based systems [Zhang et al., 2025c].
The recurrent generator can be instantiated via refinement-based methods [Zhang et al., 2025d]. When
using prompt-based refinement methods either in FVR settings with feedback from theorem prover,
or REG settings with feedback from LLM judges, we propose a method to model each generator’s
dimension-wise response to the feedback.
Definition 2.3 (Responsiveness Map). For generator Gm which leverages LLM with feedback FB,
we define the local responsiveness for dimension i ∈ {FV, LP, MC, FQ} at state x as
                         ρi (Gm | x) = Ex′ ∼LLM(x;FB(x)) πi (x′ ) − πi (x) .
                                                                         
                                                                                                  (6)

The responsiveness map captures the expected local gain for each dimension. For the FV dimension,
this quantity is equivalent to the probability that the generator fixes formal validity when it is config-
                                                     (t)             (m,b)
ured as the FV-Repairer. When Gm proposes Bm candidates xt                  at each time step t, assuming
that the used LLM judges are unbiased towards the generator, the estimation of responsiveness
of generator Gm at step t for i ∈ {LP, MC, FQ} could be achieved by aggregated differences:
                      PBm (t)
                                     (m,b)
ρbi (Gm | xt ) = 1(t) b=1
                                                      
                               πbi (xt     )−πbi (xt ) with some variance introduced by LLM judges,
                  Bm
                                        PBm (t)
                                                         (m,b)
and for FV, ρbFV (Gm | xt ) = 1(t) b=1
                                                                            
                                                 πFV (xt       ) − πFV (xt ) . For sample efficiency, the
                                    Bm
proposal budgets should be set proportionally to generator Gm with better responsiveness maps.
An example of sampling candidate formalizations from different generators is provided in Algorithm 1
in Appendix D. We also provide a concrete process of how to determine the generator roles for a set
of candidate LLMs in Appendix F.1.

2.3.2   The Acceptance Policy
We first define a plug-in estimator which indicates the overall performance as:
                              1                                                
                     J(x)
                     b     = max πFV (x), ϵ π     bLP (x) + πbMC (x) + πbFQ (x)                 (7)
                              3
where ϵ > 0 is a sufficiently small number such that ϵ < min({mi (δi )} ∪ {wi,k }). Assumption 2.1
provides a theoretical guarantee that J(x)
                                       b     is asymptotically stable and can therefore be used for
reliable comparison. We propose the following acceptance policy:

Conservative Acceptance Policy. Assume J(x
                                        b 0 ) < 1 almost surely. We define the best candidate
as:
                                 x⋆t+1 = arg max J(x).
                                                 b                                        (8)
                                                        x∈Ct
The acceptance rule at step t + 1 is designed as:
                                (
                                  x⋆t+1 , if almost surely J(x
                                                           b ⋆ ) > J(x
                                                               t+1
                                                                   b t)
                        xt+1 =                                                                        (9)
                                  xt ,     else

The process applying this acceptance rule is illustrated in Algorithm 2 in Appendix D. Such a process
{xt } is certified to exhibit monotonicity by the following theorem:


                                                    5
Theorem 2.4 (Certified Monotonicity). For all t, we have JOA (xt+1 ) ≥ JOA (xt ) or almost surely
LCBδ (xt+1 ) > LCBδ (xt ).

Proof. See Appendix B.

Theorem 2.4 indicates that, at each step of the process, either the true objective does not decrease or
its lower confidence bound increases. Hence, the process guarantees non-negative progress, thereby
consistently promoting improvement in autoformalization.
Theorem 2.5. For the monotonic process {xt } defined above, we have:
(i) (Convergence) {LCBδ (xt )} converges almost surely;
                                                  S
(ii) (Process Terminability) If there exists x ∈ t CtSsuch that J(x)b    = 1 almost surely, then
                                                   ∗                                          ∗
almost
       surely there exists an optimal candidate x   ∈  t C t such
                                                                  that ∃t0 , ∀t > t0 , xt = x and

Pr 1 − 31 mLP (δLP ) + mMC (δMC ) + mFQ (δFQ ) ≤ JOA (x∗ ) ≥ 1 − δ.
                                                   


Proof. See Appendix C.

Theorem 2.5 implies that after a sufficiently large number of steps, the change in the lower confidence
bound becomes incremental, and the bound tends to stabilize. Moreover, if the plug-in estimator
prioritizes a candidate (e.g., an ideal formalization), the process selects a strong candidate whose true
objective value exceeds a certain threshold with probability at least 1 − δ.

2.4   Summary of Choice Coherence

Our methodological design of forming a process for formalizations with better quality pursues the
following goals:
Priority on Feasibility: The objective must not favor unusable formalizations (i.e., failing FV);
Consideration of Alignment and Quality: The objective should highlight formalization which
reflects the theorem’s original meaning (LP) and mathematics (MC), and has better code quality to be
included in formal libraries (FQ);
Complementarity of LLMs and TPs: The approach should amplify strengths from different types
of LLMs and theorem provers;
Sample Efficiency: The usage of responsiveness map ensures that complementary generators are
sampled in regions where they contribute most to the components of the composite objective;
Monotonicity in the Process: Each accepted step is non-decreasing under certified criteria;
Robustness to Noise: Since LLM judges can be biased and heteroscedastic, the final results should
be guaranteed while hold under uncertainty.
Together, these choices yield a prover-anchored, judge-informed, responsiveness-aware hill-climber
whose steps are safe (preserving FV) and measurable (LCB-certified) with convergence to a Pareto
stationary set under mild reachability conditions.

3     The Monotonic Process
General Setup. Lean4 [de Moura et al., 2015] (version v4.19.0-rc3 with REPL) is chosen as the
formal language for all experiments. We evaluate our approach on miniF2F-Test [Zheng et al., 2022,
Jiang et al., 2023] and ProofNet-Test [Azerbayev et al., 2023], as both benchmarks provide natural-
language proofs. DeepSeek-Prover-V2-7B [Ren et al., 2025], Goedel-Prover-V2-8B [Lin et al., 2025],
Seed-Coder-8B [Seed et al., 2025], Qwen2.5-7B [Qwen-Team, 2025], and GPT series [OpenAI, 2024,
2025] are selected as candidate LLMs for our experiments. The description and rationale behind
the selection of benchmarks and models are provided in Appendix E. On the evaluation front, we
use the formal validity score πFV from the theorem prover, soft-dimension scores π    bLP , π
                                                                                            bMC , and
π
bFQ from LLM judges with the OAP settings [Zhang et al., 2025b], and their aggregation Jb with
ϵ = 0.001 as metrics. To complement the results with a stricter evaluation, we use Jb = 1 to measure


                                                   6
                                                                                                                                                                                                                        
                                             πFV                     π MC
                                                                     c                       Jb                                                                        π MC
                                                                                                                                                                        c                  Jb                                                                 π MC
                                                                                                                                                                                                                                                              c                         Jb
                                          π LP
                                             c                       π FQ
                                                                     c
                                                                                             Jb = 1                                               π LP
                                                                                                                                                  c                    π FQ
                                                                                                                                                                        c
                                                                                                                                                                                           Jb = 1                                      π LP
                                                                                                                                                                                                                                          c                   π FQ
                                                                                                                                                                                                                                                              c
                                                                                                                                                                                                                                                                                        Jb = 1
                                                                                                                                   
                                                                                                                                                                                                                          

         6 F R U H    




                                                                                                                 6 F R U H    




                                                                                                                                                                                                          6 F R U H    
                                                                                                                                                                                                                             
                                                                                                                                                                                                                               
                                                                                                                                   
                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                              
                                                        7 L P H  6 W H S  t                                                                            7 L P H  6 W H S  t                                                                7 L P H  6 W H S  t 
                             (a) Mono-miniF2F (GPT-Eval)                                                                        (b) Mono-miniF2F (Qwen-Eval)                                                        (c) Mono-miniF2F (Human-Eval)
                                                                                                                                                                                                                            
                                        πFV                      π MC                    Jb                                                                           π MC
                                                                                                                                                                      c                    Jb                                                                   π MC
                                                                                                                                                                                                                                                                c                        Jb
                                                                                                                                                                                                                               
                                                                 c

                                     π LP
                                        c                        π FQ
                                                                 c
                                                                                         Jb = 1                                              π LP
                                                                                                                                             c                        π FQ
                                                                                                                                                                      c
                                                                                                                                                                                           Jb = 1                                         π LP
                                                                                                                                                                                                                                          c                     π FQ
                                                                                                                                                                                                                                                                c
                                                                                                                                                                                                                                                                                         Jb = 1
                                                                                                                                                                                                                              



                                                                                                         6 F R U H    




                                                                                                                                                                                                          6 F R U H    
 6 F R U H    




                                                                                                                                                                                                                              
                                                                                                                                                                                                                              
                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                   
                                                     7 L P H  6 W H S  t                                                                              7 L P H  6 W H S  t                                                                  7 L P H  6 W H S  t 
                     (d) Mono-ProofNet (GPT-Eval)                                                                            (e) Mono-ProofNet (Qwen-Eval)                                                              (f) Mono-ProofNet (Human-Eval)
  Figure 2: Performance of the monotonic process using an ensemble of LLMs acting different
  generator roles. The evaluators of soft-dimensions includes: (GPT-Eval): GPT-4.1-mini judges;
  (Qwen-Eval): Qwen2.5-Coder-7B judges; (Human-Eval): one human expert.


   the percentage of perfect formalizations where all dimensions receive score 1. Unless otherwise
   specified, GPT-4.1-mini serves as the backend for the judges.
  We employ Algorithm 1 in Appendix D to construct candidate formalizations at each step of the
  monotonic optimization process. DeepSeek-Prover-7B and Goedel-Prover-8B are selected as the One-
  Off Generators and FV Repairers. For Recurrent Generators, we consider refinement using feedback
  on individual soft dimensions from LLM judges (REG-LP, REG-MC, and REG-FQ). Specifically,
  we use Seed-Coder-8B with REG-LP, Qwen2.5-7B with REG-LP, and DeepSeek-Prover-7B with
  REG-FQ in the monotonic process. Further discussion of this setup is provided in Appendix F.1.
  We run the monotonic optimization process for six iterations on both miniF2F and ProofNet. To
  better support the reliability of the evaluation, we also use Qwen2.5-Coder-7B as alternative LLM
  judges and conduct human evaluations. Performance at each iteration is illustrated in Figure 2 with
  detailed numbers provided in Table 4 in Appendix J.

   3.1                               Main Results

  The monotonic process guarantees non-decreasing progress and converges within a few steps.
  In Figure 2, across both datasets, the overall evaluation scores consistently improve as the process
  proceeds. On miniF2F, the gains become relatively incremental after the fourth time step, indicating
  that the process tends to converge. At the final time step, the monotonic process achieves formal
  validity of 100.00%, an overall score of 90.27%, and 49.18% perfect formalizations on miniF2F
  (Figure 2a). On the much harder benchmark ProofNet, the monotonic process leads to 77.96% formal
  validity, 52.45% overall score, and 17.74% perfect formalizations (Figure 2d).
   Different evaluation dimensions exhibit distinct trends throughout the monotonic process. On
   ProofNet, while formal validity improves across all steps, some soft-dimensions tend to stabilize
   or fluctuate after the first three iterations on both datasets. However, this discrepancy still leads to
   a gradual increase in the overall objective, as validated by human evaluation, suggesting that the
   process produces a set of auto-formalizations with progressively higher quality. Such improvements
   indicate the potential of this approach to support mathematical discovery and to generate high-quality
   formalization data for further training of existing models.
   Monotonic improvement is not solely an artifact of using the same LLM judges for both
   acceptance and evaluation. The monotonic process continues to exhibit a near non-decreasing trend
   and convergence when evaluated with LLM judges from a different model family (Figure 2b, 2e).


                                                                                                                                                               7
                                                                                                                                                                                                                                                                           
                                 πFV                 π MC
                                                     c                   Jb                                                               π MC
                                                                                                                                          c                   Jb                                          πFV                 π MC
                                                                                                                                                                                                                              c                   Jb                                                               π MC
                                                                                                                                                                                                                                                                                                                   c                   Jb
                              π LP
                                 c                   π FQ
                                                     c
                                                                         Jb = 1                                     π LP
                                                                                                                      c                   π FQ
                                                                                                                                          c
                                                                                                                                                              Jb = 1                                   π LP
                                                                                                                                                                                                          c                   π FQ
                                                                                                                                                                                                                              c
                                                                                                                                                                                                                                                  Jb = 1                                     π LP
                                                                                                                                                                                                                                                                                               c                   π FQ
                                                                                                                                                                                                                                                                                                                   c
                                                                                                                                                                                                                                                                                                                                       Jb = 1
                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                     


 6 F R U H    




                                                                                        6 F R U H    




                                                                                                                                                                             6 F R U H    




                                                                                                                                                                                                                                                                 6 F R U H    
                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                 

                                                                                                                                                                                                                                                                                                                      
                                         7 L P H  6 W H S  t                                                              7 L P H  6 W H S  t                                                             7 L P H  6 W H S  t                                                              7 L P H  6 W H S  t 

                     (a) miniF2F (GPT-Eval) (b) miniF2F (Qwen-Eval) (c) ProofNet (GPT-Eval) (d) ProofNet (Qwen-Eval)
                               Figure 3: Performance of the monotonic process with only GPT-5.4 as OOG and FVR.


While bias may arise from LLM-based evaluation, this observation suggests that the improvements
are not purely driven by the preferences of a particular judge, but instead reflect a more consistent
improvement behavior of the proposed monotonic process. Human evaluation provides further
evidence supporting the monotonic improvement of the proposed process (Figure 2c, 2f).

3.2                            Ablation Studies

We design two ablation studies: (i) using only a single strong LLM (GPT-5.4) as both the OOG
and the FVR in the monotonic process; and (ii) an iterative self-refinement (ISR) process on three
independent LLMs (DeepSeek-Prover-7B, Goedel-Prover-8B, GPT-5.4), with error feedback from
the theorem prover and no acceptance policy. The results of (i) are reported in Figure 3, while the
results of (ii) are provided in Table 6 in Appendix J.
The gain from the monotonic process is not inherently dependent on an ensemble of multiple
LLMs, however, an ensemble of smaller LLMs can outperform a single larger model. As shown
in Figures 3a, 3c, applying the monotonic process with GPT-5.4 yields consistent improvements
across all evaluated dimensions. These improvements are further validated by external judges
(Figures 3b, 3d). These results collectively demonstrate that even when using a single LLM, the
proposed monotonic process can produce consistent iterative improvements, highlighting its efficiency
and generalizability. However, both formal validity and overall performance are notably lower when
relying on a single large LLM compared to using multiple LLMs assigned to distinct roles. This
finding further supports our design choice of role specialization within the monotonic process.
Monotonic improvement does not arise from simply running models with feedback from a
theorem prover multiple times. In the ISR process with DeepSeek-Prover-7B and Goedel-Prover-
8B, the scores fluctuate across iterations, and no clear trend of consistent improvement is observed.
While the ISR process with GPT-5.4 exhibits some degree of monotonicity in formal validity and
overall scores, this improvement remains weaker than that of the monotonic process with GPT-5.4, as
shown in Figure 3.

3.3                            Comparison with Other Methods

We present a comparative evaluation of different full-theorem generation methods, using a policy
that selects, for each sample, the formalization with the highest J.
                                                                  b We consider two generation
baselines with DeepSeek-Prover-7B, Goedel-Prover-8B, and GPT-5.4: iterative self-refinement (ISR)
and sampling k independent outputs from a single model (analogous to Pass@k). The results are
reported in Table 1.
Best-of-k is more effective for models with less capability, whereas Best-of-ISR is more effective
for those with large capability. For smaller or weaker base models such as DeepSeek-Prover-7B
and Goedel-Prover-8B, Best-of-k significantly outperforms Best-of-ISR in terms of the final score. In
contrast, for stronger models such as GPT-5.4, which have shown explicit capability for refinement,
Best-of-ISR performs better. This suggests that sampling diversity combined with post-hoc selection
is more effective than ISR when the underlying model has limited reasoning capability, whereas ISR
benefits more capable models.
The monotonic process demonstrates superiority for full-theorem autoformalization. Even
in the single-model configuration, our proposed monotonic process yields robust and consistent
improvements across multiple metrics compared to both Best-of-ISR and Best-of-k. Most importantly,
the monotonic process with an ensemble of smaller LLMs achieves the strongest or comparable


                                                                                                                                                                            8
Table 1: Performance of different methods. Best-of-ISR selects the best formalization based on Jb
across six iterations for each sample. Best-of-k (k = 8) selects the best formalization based on Jb
from k outputs of a single model. All numbers are reported as percentages. Bold and Underline mark
the highest and second-highest scores.
                                             miniF2F-Test                                          ProofNet-Test
    t                     πFV      π
                                   bLP     π
                                           bMC      π
                                                    bFQ      Jb         Jb = 1   πFV     π
                                                                                         bLP     π
                                                                                                 bMC      π
                                                                                                          bFQ       Jb     Jb = 1

    DeepSeek-Prover-V2-7B
    Best-of-ISR           60.66    58.40   86.07    63.73   44.74       11.89    18.28   50.94   78.85    55.11    12.24    3.76
    Best-of-k             88.11    72.34   90.85    69.88   68.78       21.72    43.01   57.26   83.69    66.94    25.86    6.99

    Goedel-Prover-V2-8B
    Best-of-ISR           82.38    51.33   80.19    68.44   57.49        6.15    36.56   37.23   63.98    64.25    19.94    3.23
    Best-of-k             90.57    62.50   86.34    68.44   66.16        9.43    54.84   47.04   71.15    61.02    27.27    3.76

    GPT-5.4
    Best-of-ISR           56.97    87.60   97.27    85.45   51.88       32.79    20.43   95.43   98.92    91.94    19.54   14.52
    Best-of-k             49.59    90.37   97.40    88.93   45.24       32.79    15.59   96.91   98.57    91.40    14.46   10.22

    Monotonic Process (Ours)
    Single (GPT-5.4)      60.66    90.16   97.54    87.09   55.64       38.52    21.51   94.49   98.57    92.47    20.19   15.59
    Ensemble              100.00   83.71   96.72    90.37   90.27       49.18    77.96   58.06   78.32    82.80    52.45   17.74




performance across nearly all metrics. It attains the highest πFV and substantially improves J,    b
outperforming both Best-of-k and Best-of-ISR across all settings by a large margin. It also achieves
the best Jb = 1 scores, indicating improved rates of perfect autoformalization.
Computational cost vs performance gain. We report the computational costs of different settings,
measured by the number of LLM calls, in Table 7 (Appendix J). In the single-model setting, although
the monotonic process requires more generator calls, it uses fewer judge calls and achieves higher
performance, especially in producing high-quality formalizations (as indicated by Jb = 1). The
monotonic process with an ensemble of LLMs incurs substantially higher computational cost, however,
it relies on smaller LLMs, and the cost decreases progressively over iterations. Given its superior
performance, we consider this a reasonable trade-off between computational cost and performance.


4    Related Work

Autoformalization Autoformalization refers to the automatic translation of natural-language math-
ematics into formal mathematics [Wu et al., 2022, Yang et al., 2025, Mensfelt et al., 2025]. Most
research in this area has focused on statement formalization, including theorem autoformaliza-
tion [Zhang et al., 2024, Lu et al., 2024, Li et al., 2024, Gao et al., 2025] and definition autoformal-
ization [Zhang et al., 2025c]. On the proof autoformalization side, some works develop pipelines for
generating formal proofs [Ying et al., 2024, Gao et al., 2025], however, the quality of the generated
proofs is often unclear, and such outputs are mainly used for fine-tuning. Other approaches leverage
natural-language proof reasoning steps within automated theorem-proving pipelines to improve
formal reasoning [Jiang et al., 2023, Tarrach et al., 2024, Liu et al., 2025b]. While integrating
natural-language reasoning can increase proof success rates, it also presents an opportunity for
full-theorem autoformalization, directly translating theorems and proofs from natural language into
fully formalized statements. This paper focuses specifically on this scope.

Retrieval-Augmented Autoformalization. Retrieval-Augmented Generation (RAG) [Lewis et al.,
2020] has shown improvements in code generation [Lu et al., 2022, Zhang et al., 2023]. In formal
mathematics, Yang et al. [2023] trained a retrieval-augmented language model for premise selection
and theorem proving in Lean. In autoformalization, Zhang et al. [2024] use a BM25 retriever to find
similar examples from existing libraries in Isabelle and inject them into prompts. Similarly, Liu et al.
[2025a], Wang et al. [2025] retrieve potentially dependent objects from formal libraries to augment
statement autoformalization in Lean, and Zhang et al. [2025e] decomposes informal statements
into smaller components and retrieves relevant premises from Mathlib. All of these methods rely
on content from formal mathematical libraries as references. In contrast, our proposed monotonic
process operates in a reference-free manner, requiring no retrieval from existing formal libraries to
guide generation.


                                                                    9
Test-Time Optimization. Chain-of-Thoughts [Wei et al., 2022] highlights the importance of
studying optimization at test time for LLMs. Building on this idea, token-level methods such as
Tree-of-Thoughts [Yao et al., 2023] focus on optimizing intermediate tokens to produce higher-quality
completions, whereas response-level methods such as Self-Consistency [Wang et al., 2023] aggregate
multiple LLM outputs to improve overall performance. In the domain of autoformalization, Li et al.
[2024] propose a scoring framework that selects the best candidate from multiple autoformalizations
using complementary self-consistency measures. Multi-agent frameworks [Zhang et al., 2025d]
similarly organize outputs from multiple LLMs to collectively optimize results. Our framework
extends these ideas by employing both theorem provers and LLM-based judges to iteratively select
high-quality autoformalization candidates, resulting in a monotonic improvement process at test time.

5   Conclusion
We present an iterative monotonic framework for full-theorem autoformalization that combines
a masked multi-dimensional objective, role-specialized LLMs guided by a responsiveness map
and a principled acceptance policy. The framework provides certified monotonic improvement
under realistic judge noise and is supported by theoretical guarantees. Experiments on miniF2F
and ProofNet demonstrate that our approach effectively integrates the complementary strengths
of general-purpose and specialized LLMs, achieving high formal validity while improving overall
formalization quality. This work offers a practical and theoretically grounded step toward more
reliable autoformalization, with future directions including the design of more effective test-time
LLM allocation policies.

References
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
  Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. Deepseekmath: Pushing the limits of mathemat-
  ical reasoning in open language models, 2024. URL https://arxiv.org/abs/2402.03300.
Zhihong Shao, Yuxiang Luo, Chengda Lu, Z. Z. Ren, Jiewen Hu, Tian Ye, Zhibin Gou, Shirong Ma,
  and Xiaokang Zhang. Deepseekmath-v2: Towards self-verifiable mathematical reasoning, 2025.
  URL https://arxiv.org/abs/2511.22570.
Ivo Petrov, Jasper Dekoninck, Lyuben Baltadzhiev, Maria Drencheva, Kristian Minchev, Mislav
  Balunović, Nikola Jovanović, and Martin Vechev. Proof or bluff? evaluating llms on 2025 usa
  math olympiad, 2025. URL https://arxiv.org/abs/2503.21934.
Ziyin Zhang, Jiahao Xu, Zhiwei He, Tian Liang, Qiuzhi Liu, Yansi Li, Linfeng Song, Zhenwen Liang,
  Zhuosheng Zhang, Rui Wang, Zhaopeng Tu, Haitao Mi, and Dong Yu. Deeptheorem: Advancing
  llm reasoning for theorem proving through natural language and reinforcement learning, 2025a.
  URL https://arxiv.org/abs/2505.23754.
Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog,
  M Pawan Kumar, Emilien Dupont, Francisco J R Ruiz, Jordan S Ellenberg, Pengming Wang,
  Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi. Mathematical discoveries from program
  search with large language models. Nature, 625(7995):468–475, January 2024. doi: 10.1038/
  s41586-023-06924-6. URL https://www.nature.com/articles/s41586-023-06924-6.
Bartosz Naskrecki and Ken Ono. Mathematical discovery in the age of artificial intelligence. Nat.
  Phys., 21(10):1504–1506, October 2025. doi: 10.1038/s41567-025-03042-0. URL https:
  //www.nature.com/articles/s41567-025-03042-0.
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus Norman Rabe, Charles E Staats, Mateja
  Jamnik, and Christian Szegedy. Autoformalization with large language models. In Alice H. Oh,
  Alekh Agarwal, Danielle Belgrave, and Kyunghyun Cho, editors, Advances in Neural Information
  Processing Systems, 2022. URL https://openreview.net/forum?id=IUikebJ1Bf0.
Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li, Kristin E. Lauter, Swarat Chaudhuri, and
  Dawn Song. Position: Formal mathematical reasoning—a new frontier in AI. In Forty-second
  International Conference on Machine Learning Position Paper Track, 2025. URL https://
  openreview.net/forum?id=HuvAM5x2xG.


                                                 10
Lan Zhang, Xin Quan, and Andre Freitas. Consistent autoformalization for constructing mathematical
  libraries. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, Proceedings of the
  2024 Conference on Empirical Methods in Natural Language Processing, pages 4020–4033,
  Miami, Florida, USA, November 2024. Association for Computational Linguistics. doi: 10.18653/
  v1/2024.emnlp-main.233. URL https://aclanthology.org/2024.emnlp-main.233/.
Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang, Jing Xiong, Chengwu Liu, Jianhao Shen, Hui
   Jin, Jipeng Zhang, Haiming Wang, Zhicheng Yang, Jing Tang, and Zhijiang Guo. Process-driven
   autoformalization in lean 4, 2024. URL https://arxiv.org/abs/2406.01940.
Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Xian Zhang, Fan Yang, and Xiaoxing Ma. Aut-
  oformalize mathematical statements by symbolic equivalence and semantic consistency. In
  The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024. URL
  https://openreview.net/forum?id=8ihVBYpMV4.
Guoxiong Gao, Yutong Wang, Jiedong Jiang, Qi Gao, Zihan Qin, Tianyi Xu, and Bin Dong. Herald: A
  natural language annotated lean 4 dataset. In The Thirteenth International Conference on Learning
  Representations, 2025. URL https://openreview.net/forum?id=Se6MgCtRhz.
Lan Zhang, Marco Valentino, and Andre Freitas. Beyond gold standards: Epistemic ensemble of llm
  judges for formal mathematical reasoning, 2025b. URL https://arxiv.org/abs/2506.10903.
Lan Zhang, Marco Valentino, and Andre Freitas. Autoformalization in the wild: Assessing LLMs
  on real-world mathematical definitions. In Christos Christodoulopoulos, Tanmoy Chakraborty,
  Carolyn Rose, and Violet Peng, editors, Proceedings of the 2025 Conference on Empirical Methods
  in Natural Language Processing, pages 1720–1738, Suzhou, China, November 2025c. Association
  for Computational Linguistics. ISBN 979-8-89176-332-6. doi: 10.18653/v1/2025.emnlp-main.90.
  URL https://aclanthology.org/2025.emnlp-main.90/.
Qi Liu, Xinhao Zheng, Xudong Lu, Qinxiang Cao, and Junchi Yan. Rethinking and improving
  autoformalization: towards a faithful metric and a dependency retrieval-based approach. In
  The Thirteenth International Conference on Learning Representations, 2025a. URL https:
  //openreview.net/forum?id=hUb2At2DsQ.
Lan Zhang, Marco Valentino, and Andre Freitas. MASA: LLM-driven multi-agent systems for
  autoformalization. In Ivan Habernal, Peter Schulam, and Jörg Tiedemann, editors, Proceed-
  ings of the 2025 Conference on Empirical Methods in Natural Language Processing: System
  Demonstrations, pages 615–624, Suzhou, China, November 2025d. Association for Computa-
  tional Linguistics. ISBN 979-8-89176-334-0. doi: 10.18653/v1/2025.emnlp-demos.44. URL
  https://aclanthology.org/2025.emnlp-demos.44/.
Leonardo de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob von Raumer. The
  lean theorem prover (system description). In Amy P. Felty and Aart Middeldorp, editors, Automated
  Deduction - CADE-25, pages 378–388, Cham, 2015. Springer International Publishing.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. minif2f: a cross-system benchmark for
  formal olympiad-level mathematics. In International Conference on Learning Representations,
  2022. URL https://openreview.net/forum?id=9ZPegFuFTFv.
Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou, Timothee Lacroix, Jiacheng Liu, Wenda Li,
  Mateja Jamnik, Guillaume Lample, and Yuhuai Wu. Draft, sketch, and prove: Guiding formal
  theorem provers with informal proofs. In The Eleventh International Conference on Learning
  Representations, 2023. URL https://openreview.net/forum?id=SMa9EAovKMC.
Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir Radev, and
  Jeremy Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level mathematics,
  2023. URL https://arxiv.org/abs/2302.12433.
Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang,
   Zhe Fu, Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang, Yuxuan Liu,
  Wenjun Gao, Daya Guo, and Chong Ruan. Deepseek-prover-v2: Advancing formal mathematical
   reasoning via reinforcement learning for subgoal decomposition, 2025. URL https://arxiv.
   org/abs/2504.21801.


                                                11
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan
  Geng, Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing Lu, David Acuna, Kaiyu Yang,
  Hongzhou Lin, Yejin Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-prover-v2: Scaling
  formal theorem proving with scaffolded data synthesis and self-correction, 2025. URL https:
  //arxiv.org/abs/2508.03613.
ByteDance Seed, Yuyu Zhang, Jing Su, Yifan Sun, Chenguang Xi, Xia Xiao, Shen Zheng, Anxiang
  Zhang, Kaibo Liu, Daoguang Zan, Tao Sun, Jinhua Zhu, Shulin Xin, Dong Huang, Yetao Bai,
  Lixin Dong, Chao Li, Jianchong Chen, Hanzhi Zhou, Yifan Huang, Guanghan Ning, Xierui Song,
  Jiaze Chen, Siyao Liu, Kai Shen, Liang Xiang, and Yonghui Wu. Seed-coder: Let the code model
  curate data for itself, 2025. URL https://arxiv.org/abs/2506.03524.
Qwen-Team. Qwen2.5 technical report, 2025. URL https://arxiv.org/abs/2412.15115.
OpenAI. Gpt-4 technical report, 2024. URL https://arxiv.org/abs/2303.08774.
OpenAI. Openai gpt-5 system card, 2025. URL https://arxiv.org/abs/2601.03267.
Agnieszka Mensfelt, David Tena Cucala, Santiago Franco, Angeliki Koutsoukou-Argyraki, Vince
 Trencsenyi, and Kostas Stathis. Towards a common framework for autoformalization, 2025. URL
  https://arxiv.org/abs/2509.09810.
Huaiyuan Ying, Zijian Wu, Yihan Geng, JIayu Wang, Dahua Lin, and Kai Chen. Lean workbook: A
  large-scale lean problem set formalized from natural language math problems. In The Thirty-eight
  Conference on Neural Information Processing Systems Datasets and Benchmarks Track, 2024.
  URL https://openreview.net/forum?id=Vcw3vzjHDb.
Guillem Tarrach, Albert Q. Jiang, Daniel Raggi, Wenda Li, and Mateja Jamnik. More details, please:
  Improving autoformalization with more detailed proofs. In AI for Math Workshop @ ICML 2024,
  2024. URL https://openreview.net/forum?id=AkJvzpYMvK.
Qi Liu, Xinhao Zheng, Renqiu Xia, Qinxiang Cao, and Junchi Yan. Bootstrapping hierarchical
  autoregressive formal reasoner with chain-of-proxy-autoformalization. In The Thirty-ninth Annual
  Conference on Neural Information Processing Systems, 2025b. URL https://openreview.
  net/forum?id=2Xn8h68mP3.
Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman
  Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel,
  and Douwe Kiela. Retrieval-augmented generation for knowledge-intensive nlp tasks. In
  H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin, editors, Advances in
  Neural Information Processing Systems, volume 33, pages 9459–9474. Curran Associates,
  Inc., 2020. URL https://proceedings.neurips.cc/paper_files/paper/2020/file/
  6b493230205f780e1bc26945df7481e5-Paper.pdf.
Shuai Lu, Nan Duan, Hojae Han, Daya Guo, Seung-won Hwang, and Alexey Svyatkovskiy. ReACC:
  A retrieval-augmented code completion framework. In Smaranda Muresan, Preslav Nakov, and
  Aline Villavicencio, editors, Proceedings of the 60th Annual Meeting of the Association for
  Computational Linguistics (Volume 1: Long Papers), pages 6227–6240, Dublin, Ireland, May
  2022. Association for Computational Linguistics. doi: 10.18653/v1/2022.acl-long.431. URL
  https://aclanthology.org/2022.acl-long.431.
Kun Zhang, Xiexiong Lin, Yuanzhuo Wang, Xin Zhang, Fei Sun, Cen Jianhe, Hexiang Tan, Xuhui
  Jiang, and Huawei Shen. ReFSQL: A retrieval-augmentation framework for text-to-SQL gener-
  ation. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, Findings of the Association
  for Computational Linguistics: EMNLP 2023, pages 664–673, Singapore, December 2023.
 Association for Computational Linguistics. doi: 10.18653/v1/2023.findings-emnlp.48. URL
  https://aclanthology.org/2023.findings-emnlp.48.
Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
  Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with retrieval-augmented
  language models. In A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine,
  editors, Advances in Neural Information Processing Systems, volume 36, pages 21573–21612.
  Curran Associates, Inc., 2023. URL https://openreview.net/forum?id=g7OX2sOJtn.


                                               12
Shaoqi Wang, Lu Yu, Siwei Lou, Feng Yan, Chunjie Yang, Qing Cui, and Jun Zhou. Improving
  autoformalization using direct dependency retrieval, 2025. URL https://arxiv.org/abs/
  2511.11990.
Meiru Zhang, Philipp Borchert, Milan Gritta, and Gerasimos Lampouras. Drift: Decompose, retrieve,
 illustrate, then formalize theorems, 2025e. URL https://arxiv.org/abs/2510.10815.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei Xia, Ed H. Chi, Quoc V
  Le, and Denny Zhou. Chain of thought prompting elicits reasoning in large language models.
  In Alice H. Oh, Alekh Agarwal, Danielle Belgrave, and Kyunghyun Cho, editors, Advances in
  Neural Information Processing Systems, 2022. URL https://openreview.net/forum?id=
  _VjQlMeSB_J.
Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and Karthik R
  Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. In
  Thirty-seventh Conference on Neural Information Processing Systems, 2023. URL https://
  openreview.net/forum?id=5Xc1ecxO1h.
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang, Aakanksha
  Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language
  models. In The Eleventh International Conference on Learning Representations, 2023. URL
  https://openreview.net/forum?id=1PL1NIMMrw.
Lawrence C. Paulson. Isabelle: The next 700 theorem provers, 2000.
Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li, Zhongyuan Peng, Minghao Liu, Yifan Zhang,
  Zheng Yuan, Huajian Xin, Wenhao Huang, Yandong Wen, Ge Zhang, and Weiyang Liu. For-
  malmath: Benchmarking formal mathematical reasoning of large language models, 2025. URL
  https://arxiv.org/abs/2505.02735.
Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin,
  Xing Jin, Chenggang Li, Kaijing Ma, Cheng Ren, Jiawei Shen, Wenlei Shi, Tong Sun, He Sun,
  Jiahui Wang, Siran Wang, Zhihong Wang, Chenrui Wei, Shufa Wei, Yonghui Wu, Yuchen Wu,
  Yihang Xia, Huajian Xin, Fan Yang, Huaiyuan Ying, Hongyi Yuan, Zheng Yuan, Tianyang Zhan,
  Chi Zhang, Yue Zhang, Ge Zhang, Tianyun Zhao, Jianqiu Zhao, Yichi Zhou, and Thomas Hanwen
  Zhu. Seed-prover: Deep and broad reasoning for automated theorem proving, 2025. URL
  https://arxiv.org/abs/2507.23726.


A    Proof of Theorem 2.2
Proof. Recall:
                             1                                    
                  JOA (x) = πFV (x) πLP (x) + πMC (x) + πFQ (x)
                             3
          1       h                                                                 i
LCBδ (x) = πFV (x) πbLP (x)−mLP (δLP ) + π  bMC (x)−mMC (δMC ) + π  bFQ (x)−mFQ (δFQ )
          3
                         δ = 1 − (1 − δLP )(1 − δMC )(1 − δFQ )
We have:
                        
    Pr LCBδ (x) ≤ JOA (x)
                                                                                 
      ≥ Pr π bLP (x) − mLP (δLP ) + πbMC (x) − mMC (δMC ) + π   bFQ (x) − mFQ (δFQ )
                                          
            ≤ πLP (x) + πMC (x) + πFQ (x)
          
      ≥ Pr πbLP (x) − mLP (δLP ) ≤ πLP (x),                                                 (10)
                                                                               
            πbMC (x) − mMC (δMC ) + π   bFQ (x) − mFQ (δFQ ) ≤ πMC (x) + πFQ (x)
          
      ≥ Pr πbLP (x) − mLP (δLP ) ≤ πLP (x), π
                                            bMC (x) − mMC (δMC ) ≤ πMC (x),
                                            
            bFQ (x) − mFQ (δFQ ) ≤ πFQ (x)
            π


                                               13
Using the assumption of independence and Eq. 4, we have:
        
    Pr π  bLP (x) − mLP (δLP ) ≤ πLP (x), π
                                          bMC (x) − mMC (δMC ) ≤ πMC (x),
                                         
         πbFQ (x) − mFQ (δFQ ) ≤ πFQ (x)
                                                                               
     = Pr π  bLP (x) − mLP (δLP ) ≤ πLP (x) ∗ Pr π  bMC (x) − mMC (δMC ) ≤ πMC (x) ∗               (11)
                                             
          Pr π bFQ (x) − mFQ (δFQ ) ≤ πFQ (x)
     ≥ (1 − δLP )(1 − δMC )(1 − δFQ ) = 1 − δ
                                                      
Combining Eq. 10 and 11, we have: Pr LCBδ (x) ≤ JOA (x) ≥ 1 − δ, meaning LCBδ (x) is a
lower confidence bound for JOA (x) with confidence level 1 − δ.

B    Proof of Theorem 2.4
Proof. Recall:
                         1                                                     
                   J(x)
                   b    = max πFV (x), ϵ             π
                                                     bLP (x) + π
                                                               bMC (x) + π
                                                                         bFQ (x) ,
                         3
                                          x⋆t+1 = arg max J(x).
                                                          b
                                                      x∈Ct
                                 (
                                     x⋆t+1 ,                    b ⋆ ) > J(x
                                               if almost surely J(x t+1
                                                                        b t)
                        xt+1 =
                                     xt ,      else

When xt+1 = xt , we have JOA (xt+1 ) = JOA (xt ) ≥ JOA (xt ). When xt+1 = x⋆t+1 , we use proof
by cases:
a. If πFV (xt ) = 0, we have JOA (xt+1 ) ≥ 0 = JOA (xt ).
                                                                          b t ) − 1 mLP (δLP ) +
b. If πFV (xt ) = 1, πFV (x⋆t+1 ) = 0, we have almost surely LCBδ (xt ) = J(x     3
                                    b ⋆ ) − 1 mLP (δLP ) + mMC (δMC ) + mFQ (δFQ ) ≤ ϵ −
                                                                                    
mMC (δMC ) + mFQ (δFQ ) < J(x           t+1    3
1
                                             
3 mLP (δLP ) + mMC (δMC ) + mFQ (δFQ ) . Since ϵ is a sufficiently small     number such that
ϵ < min{mi (δi )}, it follows that ϵ− 31 mLP (δLP )+mMC (δMC )+mFQ (δFQ ) < 0 = LCBδ (xt+1 ).
c. If πFV (xt ) = 1, πFV (x⋆t+1 ) = 1, we have LCBδ (xt+1 ) − LCBδ (xt ) = J(x
                                                                           b ⋆ ) − J(x
                                                                               t+1
                                                                                   b t) > 0
almost surely.

C    Proof of Theorem 2.5
Proof. (i) We first prove that ∃t0 , ∀t > t0 , LCBδ (xt+1 ) ≥ LCBδ (xt ) almost surely by cases:
a. If ∃t0 such that ∀t > t0 , πFV (xt+1 ) = πFV (xt ) = 0, thereby ∀t > t0 , LCBδ (xt+1 ) =
LCBδ (xt ) = 0 almost surely.
b. If ∀t, πFV (xt+1 ) = πFV (xt ) = 1, then almost surely either xt+1 = xt , in which case
LCBδ (xt+1 ) = LCBδ (xt ), or xt+1 = x⋆t+1 , in which case LCBδ (xt+1 ) − LCBδ (xt ) =
b ⋆ ) − J(x
J(x         b t ) > 0. In both cases, LCBδ (xt+1 ) ≥ LCBδ (xt ) almost surely, therefore,
    t+1
∀t, LCBδ (xt+1 ) ≥ LCBδ (xt ) almost surely.
c. If ∃t1 , πFV (xt1 ) = 1, πFV (xt1 +1 ) = 0 and ∃t2 > t1 , πFV (xt2 ) = 0, πFV (xt2 +1 ) = 1, we have
almost surely J(xb t +1 ) > J(xb t ) ≥ 0, thereby almost surely J(x  b t +1 ) ≥ min{wi,k } > ϵ. For
                      2            2                                     2

every t > t2 , we next prove that if πFV (xt ) = 1, J(x
                                                      b t ) > ϵ, then πFV (xt+1 ) = 1, J(x b t+1 ) > ϵ.
Assume that πFV (xt ) = 1 and J(xt ) > ϵ. Then either xt+1 = xt , in which case J(x
                                     b                                                       b t+1 ) =
                             ⋆                                                     ⋆
J(xt ) > ϵ, or xt+1 = xt+1 , in which case almost surely J(xt+1 ) = J(xt+1 ) > J(xt ) > ϵ.
 b                                                                b            b             b
Moreover, πFV (xt+1 ) = 0 is impossible, otherwise, we would have J(x    b t+1 ) ≤ ϵ which contradicts


                                                    14
Algorithm 1 Candidates Construction at Step t
 1: Inputs: Natural language statement and proof (snl , pnl ), Previous formalization xt , Set of One-Off Genera-
    tors Gi , Set of FV-Repairers Gj , Set of Recurrent Generators Gk , Theorem Prover T P.
 2: Ct ← ∅
 3: for G ∈ Gi do
 4:     Sample one x ∼ pG (x | snl , pnl )
 5:     if πFV (x) == 0 from T P then
 6:        for G′ ∈ Gj do
 7:           Sample one x′ ∼ pG′ (x′ | snl , pnl , x)
 8:           Ct ← Ct ∪ {x′ }
 9:        end for
10:     else
11:        Ct ← Ct ∪ {x}
12:     end if
13: end for
14: if t > 0 then
15:     for G ∈ Gk do
16:        Sample one x ∼ pG (x | snl , pnl , xt )
17:        if πFV (x) == 0 from T P then
18:           for G′ ∈ Gj do
19:              Sample one x′ ∼ pG′ (x′ | snl , pnl , x)
20:              Ct ← Ct ∪ {x′ }
21:           end for
22:        else
23:           Ct ← Ct ∪ {x}
24:        end if
25:     end for
26: end if


 b t+1 ) > ϵ. Applying mathematical induction, we have ∀t > t2 , πFV (xt ) = 1. Using the same
J(x
strategy as in case b, we have ∀t > t2 , LCBδ (xt+1 ) ≥ LCBδ (xt ) almost surely.
We have proved that {LCBδ (xt )}t>t0 is almost surely a non-decreasing sequence. Since
{LCBδ (xt )} are bounded by 1, the monotone convergence theorem implies that {LCBδ (xt )} con-
verges almost surely.
                            S
(ii) Since there exists x ∈ t Ct such that J(x)
                                             b     = 1 almost surely, we have a non-empty set
                    a.s.                                  a.s.
{t | ∃x ∈ Ct , J(x)
               b    = 1}. Let t0 = min{t | ∃x ∈ Ct , J(x)
                                                     b    = 1} and x∗ = x⋆t +1 = arg max J(x).
                                                                                       0
                                                                                         b
                                                                                                    x∈Ct0
                        b ⋆ ) almost surely, thereby xt +1 = x⋆             ∗
We have J(x
         b t ) < 1 = J(x
              0            t0 +1                          0        t0 +1 = x and J(xt0 +1 ) = 1
                                                                                   b
almost surely. We next prove that if J(xt ) = 1 almost surely, then xt+1 = xt and J(x
                                     b                                              b t+1 ) = 1
almost surely. Assuming J(x
                         b t ) = 1 almost surely, we have max J(x)
                                                                 b    ≤ 1 = J(x
                                                                             b t ) almost surely.
                                                                     x∈Ct
         b ⋆ ) ≤ 1 = J(x
Hence, J(x               b t ) almost surely. Applying acceptance rule Eq. 9, we have xt+1 = xt
             t+1
and thereby J(xb t+1 ) = J(x
                           b t ) = 1 almost surely. Applying mathematical induction, we have
∀t > t0 , xt = x . Since J(x∗ ) = 1 almost surely, we have πFV (x∗ ) = 1. Applying Eq. 5 and 7, we
                 ∗       b
               ∗     1
    LCBδ (x ) = 3 3 − mLP (δLP ) − mMC (δMC) − mFQ (δFQ) almost surely. In other words,
have
Pr 1 − 31 mLP (δLP ) + mMC (δMC ) + mFQ (δFQ ) ≤ JOA (x∗ ) ≥ 1 − δ.


D    Algorithms
We provide the algorithm we used in practice to construct candidate formalizations at each time step
in Algorithm 1, and the algorithm of the monotonic process in Algorithm 2.

E    Rationale for Empirical Setups
We describe the existing formal benchmarks and the reasons for selecting miniF2F and ProofNet as
follows:


                                                            15
Algorithm 2 The Monotonic Process
 1: Inputs: Natural language statements and proofs D = {(snl , pnl )}, Sets of LLM Judges JLP , JMC , JFQ ,
      Theorem Prover T P, Maximum number of iterations T .
 2: for (snl , pnl ) ∈ D do
 3:    x0 ← ””, J0 ← −1
 4:    for t = 0, . . . , T − 1 do
 5:       Construct Ct (e.g., Algorithm 1)
 6:       J ← Jt
 7:       for x ∈ Ct do
 8:           Obtain πFV (x) from theorem prover T P
 9:           if J ≤ ϵ or πFV (x) == 1 then
10:              for i ∈ {LP, MC, FQ} do
11:                                    bi (x) from Ji using Eq. 3
                     Obtain estimation π
12:              end for
13:              Calculate plug-in estimator J(x)
                                               b   using Eq. 7
14:            if J(x)
                  b    ≥ J then
15:               x⋆t+1 ← x, J ← J(x)
                                 b
16:            end if
17:         end if
18:      end for
19:      if J > Jt then
20:         xt+1 ← x⋆t+1 , Jt+1 ← J
21:      else
22:         xt+1 ← xt , Jt+1 ← Jt
23:      end if
24:      if Jt+1 == 1 then
25:         break
26:      end if
27:   end for
28: end for



         • miniF2F [Zheng et al., 2022] is a dataset of formal Olympiad-level mathematics problems
           with both Isabelle [Paulson, 2000] and Lean formalizations. The original dataset lacks
           natural language proofs, but an improved version [Jiang et al., 2023] provides them. It
           contains 244 validation instances and 244 test instances. Due to the availability of natural
           language proofs and its relatively small size, miniF2F is considered as a representative
           benchmark for validating the methods in this work.
         • ProofNet [Azerbayev et al., 2023] is a benchmark for autoformalization and formal proving
           of undergraduate-level mathematics, consisting of 185 validation samples and 186 test
           samples. Compared to miniF2F, it has higher complexity. Its combination of natural
           language proofs and manageable scale makes it suitable for evaluating our monotonic
           process.
         • Lean Workbook [Ying et al., 2024] contains 57,231 formalized math problems (5k with
           formal solutions) generated via a pipeline of synthetic data generation and filtering. However,
           it lacks natural language proofs, making it unsuitable for the full-theorem autoformalization
           task in this work.
         • FormalMATH [Yu et al., 2025] is a large-scale Lean4 benchmark with 5,560 formally
           verified problems ranging from high-school Olympiad challenges to undergraduate-level
           theorems. While it includes natural language proofs, its large scale makes it less practical as
           a representative benchmark for testing our methods in this paper.
         • Herald [Gao et al., 2025] contains 579,883 samples generated from a structural-information-
           aware pipeline, of which 44,553 include natural language proofs. Similar to FormalMATH,
           although it provides natural language proofs, its large scale limits its suitability as a repre-
           sentative benchmark for this work.

We elicit the LLMs used in this work and the reasons for their selection as follows:

         • DeepSeek-Prover-V2 [Ren et al., 2025] is an open-source LLM designed for formal theorem
           proving in Lean4, available in 7B and 671B sizes. This model family has demonstrated


                                                       16
           state-of-the-art performance in generating formal proofs [Chen et al., 2025]. Since this work
           focuses on full-theorem autoformalization, which requires complete formalization including
           proofs, its superiority in generating Lean4 proofs makes it a suitable candidate. The 7B
           version is selected here due to computational resource constraints.
         • Goedel-Prover-V2 [Lin et al., 2025] is another series of open-source LLMs for automated
           theorem proving in Lean4, available in 8B and 32B sizes. Unlike DeepSeek-Prover-V2, this
           model can iteratively revise its proofs by leveraging feedback from the Lean theorem prover,
           which is particularly useful in the FV-Repair setting of this work. We select the 8B version
           due to computational resource constraints.
         • Qwen2.5 [Qwen-Team, 2025] is a comprehensive series of open-source models designed to
           meet diverse needs. Qwen2.5-7B-Instruct is a representative small-scale general-purpose
           model within our computational budget and is therefore included in this study.
         • Seed-Coder [Seed et al., 2025] is a series of open-source LLMs specialized in code genera-
           tion. While not fully general-purpose, formal languages can be considered a type of code,
           and thus this model serves as a state-of-the-art coding model suitable for our purposes. The
           8B version is chosen due to computational resource limitations.
         • GPT series [OpenAI, 2024, 2025] are the latest and largest state-of-the-art general-purpose
           closed-source LLM at the time of this work. Full versions of GPT-4.1 and GPT-5.4 are used
           for generating formalizations, while the smaller GPT-4.1-mini balances performance and
           cost, making it suitable as LLM judges in our experiments.

F     Complementary Results
All smaller LLMs used in this work are run on two 24GB NVIDIA Quadro RTX 6000 GPUs, while
GPT models are accessed via their API.

F.1     Determination of Generator Roles

For the following experiments, we use greedy decoding for open-source models to improve repro-
ducibility. We sample one instance per generator to reduce computational cost, while empirical
evidence suggests that the results remain indicative.

F.1.1    One-Off Generators and FV-Repairers
We assess LLMs’ capabilities as (i) One-Off Generators under zero-shot autoformalization, and (ii)
FV-Repairers under refinement guided by rigorous error feedback from theorem provers. We report
scores in Table 2.
Models fine-tuned on the specialized domain perform best in the One-Off Generator setting.
Both DeepSeek-Prover-7B and Goedel-Prover-8B achieve higher FV scores than GPT-4.1 under this
setting. In particular, Goedel-Prover-8B produces syntactically correct formal theorems and proofs for
58.61% of miniF2F examples and 17.74% of ProofNet examples. Under zero-shot autoformalization,
specialized LLMs generate formalizations with higher FV and overall scores, making them well
suited to the One-Off Generator setting. However, formalizations produced by these specialized
LLMs still receive relatively lower scores on soft semantic dimensions such as LP and FQ, indicating
persistent challenges in alignment faithfulness.
Specialized LLMs and general-purpose larger LLMs can both serve as effective FV-Repairers
for high-validity formalizations. On miniF2F, when acting as FV-Repairers, the general-purpose
smaller LLMs Qwen2.5-7B and Seed-Coder-8B show no and limited improvement in FV, respectively.
Across both miniF2F and ProofNet, GPT-4.1 achieves larger gains in FV than DeepSeek-Prover-7B
when refining formalizations that already have relatively high initial validity, although its improve-
ments still fall short of Goedel-Prover-8B’s performance. Goedel-Prover-8B delivers the highest
overall gains in FV, but these improvements come at the cost of lower scores on soft-semantic
dimensions such as LP and MC. This trade-off indicates that FV alone is insufficient for evaluating
overall performance. Taken together, these results highlight the strengths of specialized LLMs and
GPT-4.1 as FVRs. Under the FVR setting with Goedel-Prover-8B, we obtain 66.39% syntactically
correct formal theorems with proofs on miniF2F and 20.43% on ProofNet.


                                                   17
Table 2: Performance of LLMs as One-Off Generators (OOG) and FV-Repairers (FVR) for full
theorem autoformalization on miniF2F and ProofNet benchmark using Lean4. FVRs are applied
to formalizations generated by OOGs (i.e., zero-shot autoformalization). LLMs include: Qwen
(Qwen2.5-7B-Instruct), Seed (Seed-Coder-8B-Instruct), DSP (DeepSeek-Prover-V2-7B), GDP
(Goedel-Prover-V2-8B), and GPT (GPT-4.1).
         Type    LLM                        πFV          π
                                                         bLP      π
                                                                  bMC      π
                                                                           bFQ       Jb
         miniF2F-Test
         OOG     Qwen2.5-7B-Instruct        0.00        28.89    73.50    15.78     0.04
         FVR     Qwen2.5-7B-Instruct       0.00         −0.61    +1.23    +0.41     0.00
         FVR     Seed-Coder-8B-Instruct   +0.82         +0.92    −1.78    +2.05    +0.57
         FVR     DeepSeek-Prover-V2-7B    +22.95        +18.24   +4.64    +23.36   +15.07
         FVR     Goedel-Prover-V2-8B      +30.33        +12.60   −6.01    +28.89   +18.71
         FVR     GPT                      +12.30        +59.84   +23.91   +53.89   +11.31
         OOG     Seed-Coder-8B-Instruct     7.38        28.38    63.39    21.11     5.35
         FVR     Seed-Coder-8B-Instruct   +1.64         −1.43    +3.01    +2.05    +1.21
         FVR     DeepSeek-Prover-V2-7B    +21.31        +13.73   +10.52   +16.39   +14.45
         FVR     Goedel-Prover-V2-8B      +20.49        +8.61    +3.28    +18.65   +11.97
         FVR     GPT                      +13.11        +54.00   +32.79   +46.93   +11.54
         OOG     DeepSeek-Prover-V2-7B     50.41        55.02    80.87    51.02    35.15
         FVR     Qwen2.5-7B-Instruct       0.00         −1.74    +1.37    −5.33    0.00
         FVR     Seed-Coder-8B-Instruct    +1.64        −4.92    −1.50    −6.97    +1.16
         FVR     DeepSeek-Prover-V2-7B     +1.64        +0.92    +0.96    −2.05    +0.90
         FVR     Goedel-Prover-V2-8B       +6.56        −3.38    −2.05    +1.02    +4.02
         FVR     GPT                       +3.69        +18.24   +9.97    +11.48   +3.38
         OOG     Goedel-Prover-V2-8B       58.61        47.34    73.63    49.80    35.61
         FVR     DeepSeek-Prover-V2-7B     +1.64         0.00    −0.68    −1.02    +1.15
         FVR     Goedel-Prover-V2-8B       +7.79        −1.23    −4.51    +1.43    +5.50
         FVR     GPT                       +2.05        +16.91   +9.15    +10.25   +1.92
         OOG     GPT                        9.02        90.16    98.09    58.81     8.33
         FVR     DeepSeek-Prover-V2-7B    +20.08        −7.99    −3.96    −3.69    +16.36
         FVR     Goedel-Prover-V2-8B      +27.87        −20.39   −9.15    −2.05    +21.65
         FVR     GPT                      +6.56         +2.46    +1.23    +9.22    +6.08
         ProofNet-Test
         OOG     Seed-Coder-8B-Instruct     0.00        13.71    51.25     6.18     0.02
         OOG     DeepSeek-Prover-V2-7B     11.83        41.80    67.38    35.75     7.14
         FVR     DeepSeek-Prover-V2-7B     +0.54        +1.21    +2.15    +3.49    +0.35
         FVR     Goedel-Prover-V2-8B       +4.30        −2.96    −0.54    +3.76    +2.88
         FVR     GPT                       +1.08        +46.77   +27.42   +36.56   +1.11
         OOG     Goedel-Prover-V2-8B       17.74        31.59    63.44    29.84     6.89
         FVR     DeepSeek-Prover-V2-7B     0.00         +0.13    −1.43    +0.81    0.00
         FVR     Goedel-Prover-V2-8B       +2.69        −7.53    −5.38    +4.30    +1.61
         FVR     GPT                       +1.08        +48.52   +25.63   +38.44   +1.11
         OOG     GPT                        1.08        91.67    99.46    66.67     1.12
         FVR     DeepSeek-Prover-V2-7B     +1.61        −10.22   −5.02    −7.26    +1.51
         FVR     Goedel-Prover-V2-8B       +6.99        −31.85   −16.31   −6.99    +4.76
         FVR     GPT                       0.00         +2.96    −0.18    +8.33    0.00



Specialized LLMs acting as FV-Repairers on low-validity formalizations do not necessarily
outperform their own zero-shot autoformalization results. On miniF2F, when DeepSeek-Prover-
7B and Goedel-Prover-8B refine zero-shot outputs generated by Qwen2.5-7B, Seed-Coder-8B, or
GPT-4.1, the percentage of recovered syntactically correct full theorems is substantially lower than
their respective zero-shot performances. GPT-4.1 does achieve more correct full theorems when


                                                   18
            ) 9 5                                                  ) 9 5                                               ) 9 5                                                   ) 9 5                       
     5 ( *  / 3                                           5 ( *  / 3                                         5 ( *  / 3                                            5 ( *  / 3                       
   5 ( *  0 &                          5 ( *  0 &                         5 ( *  0 &                                                                              5 ( *  0 &                      
    5 ( *  ) 4                                           5 ( *  ) 4                                           5 ( *  ) 4                                            5 ( *  ) 4                       
  5 ( *  $ / /                          5 ( *  $ / /                          5 ( *  $ / /                       5 ( *  $ / /                       
                       ρbFV ρbLP ρbMC ρbFQ                                                      ρbFV ρbLP ρbMC ρbFQ                                                    ρbFV ρbLP ρbMC ρbFQ                                                      ρbFV ρbLP ρbMC ρbFQ
              (a) Qwen2.5-7B                                                        (b) Seed-Coder-8B                                              (c) DeepSeek-Prover-7B                                                       (d) Goedel-Prover-8B
                           Figure 4: Average of local responsiveness (%)for LLMs as different generators.
                            $ Y J  ' L I I H U H Q F H                                          $ Y J  ' L I I H U H Q F H                                                  & R K H Q 
 V  G                                                        & R K H Q 
 V  G
    5 ( *  / 3                                      5 ( *  / 3                                    5 ( *  / 3                                       5 ( *  / 3                             
   5 ( *  0 &                                 5 ( *  0 &                                        5 ( *  0 &                                      5 ( *  0 &                             
    5 ( *  ) 4                                      5 ( *  ) 4                                    5 ( *  ) 4                                       5 ( *  ) 4                                  
  5 ( *  $ / /                                 5 ( *  $ / /                               5 ( *  $ / /                               5 ( *  $ / /                             
                   πFV        π LP
                               c         π MC π FQ
                                         c           c
                                                                   Jb                       πFV        π LP
                                                                                                       c          π MC π FQ
                                                                                                                  c           c
                                                                                                                                           Jb                      πFV        π LP
                                                                                                                                                                              c           π MC π FQ
                                                                                                                                                                                          c           c
                                                                                                                                                                                                                    Jb                      πFV        π LP
                                                                                                                                                                                                                                                       c           π MC π FQ
                                                                                                                                                                                                                                                                   c           c
                                                                                                                                                                                                                                                                                            Jb

                    (a) miniF2F                                                             (b) ProofNet                                                            (c) miniF2F                                                             (d) ProofNet
        Figure 5: Average and Cohen’s d of improvements using different feedback on each dataset.


refining the zero-shot outputs of Qwen2.5-7B and Seed-Coder-8B than in its own zero-shot setting,
but the magnitude of its gains remains smaller than those achieved by the specialized LLMs.

F.1.2               Responsiveness Maps of Generators
We evaluate the ability of LLMs to act as Recurrent Generators under iterative refinement with
feedback from LLM judges. In addition to REG-LP, REG-MC, and REG-FQ, we also consider REG-
ALL, which uses feedback aggregated across all evaluation dimensions. We consider Qwen2.5-7B,
Seed-Coder-8B, DeepSeek-Prover-7B, and Goedel-Prover-8B as generators, but exclude GPT-4.1 to
avoid potential bias from GPT-4.1-mini judgments. Refinement is applied to formalizations with high
formal validity produced by the specialized LLMs DeepSeek-Prover-7B and Goedel-Prover-8B. For
all generators that use LLM-based feedback (FVR and REG), we compute the responsiveness map
for each individual instance and report the mean across all samples for the four LLMs in Figure 4.
Responsiveness maps can illustratively prioritize settings that exhibit the greatest expected gain
across the soft dimensions. Among all REG settings, Seed-Coder-8B with REG-LP achieves the
highest average expected gain with respect to LP (5.44%), Qwen2.5-7B with REG-MC attains the
highest gain for MC (8.02%), and DeepSeek-Prover-7B with REG-FQ yields the largest gain for FQ
(2.91%).
Specialized LLMs are more responsive to formal validity, whereas general-purpose LLMs
tend to focus on soft semantic properties. Across all settings, Qwen2.5-7B exhibits no positive
local responsiveness (Figure 4a). Seed-Coder-8B likewise shows negative responsiveness toward
FV in REG settings and only limited responsiveness when configured as FVR (Figure 4b). In
contrast, both DeepSeek-Prover-7B and Goedel-Prover-8B demonstrate substantial responsiveness
(>10%) when configured as FVR (Figures 4c, 4d). These results indicate that specialized LLMs are
more responsive to FV. Specialized models also exhibit stronger responsiveness in formal quality
compared to general-purpose LLMs. However, for dimensions less directly tied to formal structure
(LP and MC), specialized LLMs show limited refinement capability, particularly Goedel-Prover-8B.
This contrast suggests that general-purpose and specialized LLMs emphasize different aspects of
refinement, reflecting a trade-off between formal and informal dimensions.

F.2           Dataset-Level Performance of Recurrent Generators

We report the average improvement and Cohen’s d on the miniF2F and ProofNet datasets in Figure 5.
Providing feedback on a single dimension yields targeted improvements on that dimension. In
Figure 5a, on miniF2F, REG-LP, REG-MC, REG-FQ consistently lead to average improvements
in π
   bLP , π
         bMC , π
               bFQ , respectively. In Figure 5b and 5d, on ProofNet, REG-MC likewise exhibits a
positive effect on MC judgments. Taken together, these results suggest that providing LLMs with


                                                                                                                                                19
                                     * 3 7  ( Y D O                                            * 3 7  ( Y D O                                            * 3 7  ( Y D O                                            * 3 7  ( Y D O                                            * 3 7  ( Y D O                                            * 3 7  ( Y D O
                                        4 Z H Q  ( Y D O                                             4 Z H Q  ( Y D O                                             4 Z H Q  ( Y D O                                             4 Z H Q  ( Y D O                                             4 Z H Q  ( Y D O                                             4 Z H Q  ( Y D O
                                                                                                                                                                                                                                                                                                                      

                                                                                                                                                                                                                                                                                                                      




                                                                                                                              m(δFQ )




                                                                                                                                                                                                                                                                                                                        m(δFQ )
                                                                m(δMC )




                                                                                                                                                                                                                                                          m(δMC )
m(δLP )




                                                                                                                                                                                            m(δLP )
                                                                                                                                                                                                                                                                                                                      

                                                                                                                                                                                                                                                                                                                      

                                                                                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                                                                             
                              δLP                                                           δMC                                                           δFQ                                                           δLP                                                           δMC                                                           δFQ

  (a) miniF2F π
              bLP (b) miniF2F π
                              bMC (c) miniF2F π
                                              bFQ (d) Proofnet π
                                                               bLP (e) ProofNet π
                                                                                bMC (f) ProofNet π
                                                                                                 bFQ
                                                                                            Figure 6: Uncertainty estimation of LLM judges.




feedback focused on a specific dimension is an effective strategy for improving performance along
that dimension.
However, direct feedback on a given dimension is not necessarily the most effective way to
improve that dimension. Across both datasets, all REG settings lead to improvements in MC.
Notably, the method achieving the largest Cohen’s d for π      bMC is REG-FQ rather than REG-MC
(Figure 5c, 5d). This result suggests that refining formalizations using feedback on formal quality can
have a statistically larger impact on mathematical consistency than providing MC-specific feedback
alone.
Refining one dimension does not guarantee the preservation of other dimensions. All REG
settings lead to decreases in formal validity, even when error details are provided alongside LLM
judgments. Moreover, in some cases, non-targeted dimensions are negatively affected by giving
feedback focused on a specific target dimension. This pattern highlights the difficulty of jointly
optimizing multiple dimensions of formalizations and further underscores the necessity of our
proposed iterative monotonic process for more reliable autoformalization.




F.3                         Uncertainty Estimation


Using the results of the human evaluation in the monotonic process experiments as the ground-
truth evaluation πi (x) in Eq. 4, we compute the curves of δi and m(δi ), which correspond to the
maximum admissible margin mi (δi ) for the LLM judges used in our experiments (GPT-4.1-mini and
Qwen2.5-Coder-7B). Figure 6 illustrates the behavior of LLM judges under uncertainty.
There is a trade-off between uncertainty level and the effort required to calibrate LLM judges.
Across all settings, we observe that the required margin m(δi ) increases as the uncertainty level
δi decreases. This suggests that achieving lower uncertainty requires stronger calibration of LLM
judgments. Conversely, using less-calibrated LLM judges leads to higher uncertainty levels.
LLM judges exhibit different levels of uncertainty across different aspects. On both datasets,
both LLM judges are more confident in logical preservation (LP) than in mathematical consistency
(MC), and least confident in formal quality (FQ). This behavior indicates that MC and FQ are harder
to align with human evaluations for LLM judges.
While Qwen2.5-Coder-7B requires less calibration at the same uncertainty level, it is a more
conservative judge than GPT-4.1-mini for autoformalization evaluation and is less informative
for selection. The curves corresponding to GPT-4.1-mini consistently lie above those of Qwen2.5-
Coder-7B, indicating that larger margins are needed to guarantee the same confidence level. This
suggests that GPT-4.1-mini exhibits higher variability and requires stronger correction to obtain
reliable positive judgments. However, Qwen2.5-Coder-7B is a conservative evaluator that tends to
assign lower scores. Although it has lower uncertainty in the lower-bound sense, it also does not
provide sufficient discrimination for selecting better formalizations.


                                                                                                                                                                                    20
G      Details of Prompts

G.1     Prompts for Generators

      One-Off Generator
    System Prompt:
    You are an expert in formal language Lean4.
    You will be given a mathematical statement and its proof written in natural language and
    LaTeX symbols.
    Your task is to provide the formal code of the given natural language mathematical statement
    and its proof in Lean4 with the following instructions:
    1. You should give the formal code directly without any additional comments or explanations.
    2. In case that you need to import any necessary preambles, you should not import any fake
    (non-exist) preambles.
    3. You should wrap the formal code in a way illustrated as the following:
    %%%%%%%%%%
    Your Formal Code
    %%%%%%%%%%
    Strictly follow the instructions that have been claimed.

      User Prompt:
      Natural language statement: {Natural Language Statement}
      Natural language proof: {Natural Language Proof}
      Give me the Lean4 formal code of them:


      FV-Repairer

    System Prompt:
    You are an expert in formal language Lean4.
    You will be given a mathematical statement and its proof written in natural language and
    LaTeX symbols.
    You will also be given a formal code which attempted to describe the given mathematical
    statement and its proof in Lean4.
    Your task is to refine the given formal code to make it correct while maintaining the alignment
    with the given natural language mathematical statement and proof.
    Here are some instructions for your task:
    1. You should give the formal code directly without any additional comments or explanations.
    2. In case that you need to import any necessary preambles, you should not import any fake
    (non-exist) preambles.
    3. You should wrap the formal code in a way illustrated as the following:
    %%%%%%%%%%
    Your Formal Code
    %%%%%%%%%%
    Strictly follow the instructions that have been claimed.

    User Prompt:
    Natural language statement: {Natural Language Statement}
    Natural language proof: {Natural Language Proof}
    There are some Lean4 formal codes describing the given mathematical statement and its
    proof: {Formal Code}
    You should refine the formal code for your task to make it correct.
    Here are some feedbacks about the formal code which can be used to help your task: {Ac-
    cording to the theorem prover, the error details of the provided formal code are:
    Error Details
    }



                                                  21
Example of Error Details:
Error on line 5, start column 0, end column 1: unexpected token ’#’; expected command
Error on line 138, start column 0, end column None: unexpected end of input; expected ’{’ or
indented tactic sequence


Recurrent Generator
System Prompt:
You are an expert in formal language Lean4.
You will be given a mathematical statement and its proof written in natural language and
LaTeX symbols.
You will also be given a formal code which attempted to describe the given mathematical
statement and its proof in Lean4.
Your task is to refine the given formal code to make it correct while maintaining the alignment
with the given natural language mathematical statement and proof.
Here are some instructions for your task:
1. You should give the formal code directly without any additional comments or explanations.
2. In case that you need to import any necessary preambles, you should not import any fake
(non-exist) preambles.
3. You should wrap the formal code in a way illustrated as the following:
%%%%%%%%%%
Your Formal Code
%%%%%%%%%%
Strictly follow the instructions that have been claimed.

User Prompt:
Natural language statement: {Natural Language Statement}
Natural language proof: {Natural Language Proof}
There are some Lean4 formal codes describing the given mathematical statement and its
proof: {Formal Code}
You should refine the formal code for your task to make it correct.
Here are some feedbacks about the formal code which can be used to help your task: {Feed-
back from LLM Judges}

Example of Feedback from LLM Judges:
Aspect: Is the formalized code expressed in a minimal, non-redundant form, avoiding
unnecessary repetition or complexity?
Evaluation: Explanation: The formalized code is not expressed in a minimal, non-redundant
form. It contains multiple intermediate steps (h4, h5, h6, h7, h8) that are stated but left as
“sorry," indicating incomplete proofs or placeholders. While these steps reflect the logical
progression of the proof, they are somewhat verbose and could be streamlined by directly
manipulating the logarithmic equalities or by combining steps to avoid repetition. For
example, the relationships between the logarithms of x, y, and z could be derived more
compactly without separately stating each intermediate equality. Additionally, the final
step h9 is also a “sorry," so the proof is incomplete and does not demonstrate minimality or
efficiency in its current form. Overall, the code structure suggests redundancy and unnecessary
complexity rather than a minimal, concise formalization.
Judgement: False

Aspect: Is the formalized code internally coherent and contains no contradictions under the
logical rules of the relevant formal system?
Evaluation: Explanation: The formalized code is internally coherent and contains no contra-
dictions under the logical rules of Lean4 and the real number theory it uses. The theorem
statement is well-formed, assuming the standard definitions of logarithms (Real.logb) and
the domain conditions (x, y, z > 1, w > 0). The proof structure is consistent: it introduces
variables and hypotheses, then states intermediate lemmas (h4 to h9) that relate the logarithms



                                              22
      of w and the bases x, y, z. Although the proof steps are marked as “sorry" (placeholders for
      omitted proofs), this does not introduce contradictions; it simply means the proof is incom-
      plete but not inconsistent. The chain of equalities and substitutions aligns with the natural
      language proof logic, and the final conclusion matches the problem statement. Therefore, the
      code is internally coherent and free of contradictions.
      Judgement: True


G.2     Prompts for LLM Judges

We use the Operable Atomic Properties (OAPs) in [Zhang et al., 2025b] to estimate scores for soft-
dimensions. OAPs within one soft-dimension are considered equally (i.e., for i ∈ {LP, MC, FQ},
wi,k is the same for every k in Eq. 3). The descriptions of OAPs used in the prompts are listed as
follows:

For π
    bLP 1. Pre-arg Structure: ‘Does the formalized code reflect the inherent predicate-argument
       structure of the natural language statement?’; 2. Quantification: ‘Does the formalized code
       accurately formalize all quantifiers, such as universal and existential, present in the natural
       language statement?’; 3. Formula: ‘Are all mathematical formulas and expressions in the
       natural language statement, such as equations and inequalities, correctly and completely
       represented in the formalized code?’; 4. Relation: ‘Are the logical and mathematical rela-
       tionships between propositions in the natural language statement preserved in the formalized
       code?’.
For π
    bMC 1. Concept: ‘Are all mathematical concepts mentioned in the natural language statement,
        such as integers, fractions, real numbers, complex numbers, derivatives, integrals, vectors,
        matrices, probabilities, expectations, and variances, are correctly formalized in the formal-
        ized code?’; 2. Constant: ‘Are all mathematical constants mentioned in the natural language
        statement, such as 1, 23 , π, e, are properly included in the formalized code?’; 3. Operator:
       ‘Are all mathematical operators used in the natural language statement, such as addition,
        subtraction, multiplication, division, summation, exponentiation, and product, are correctly
        represented in the formalized code?’.
For π
    bFQ 1. Conciseness: ‘Is the formalized code expressed in a minimal, non-redundant form,
       avoiding unnecessary repetition or complexity?’; 2. Logical Consistency: ‘Is the formalized
       code internally coherent and contains no contradictions under the logical rules of the
       relevant formal system?’.

      LLM Judges

   System Prompt:
   You are an expert in formal language Lean4.
   You will be given a mathematical statement and its proof written in natural language and
   LaTeX symbols.
   You will also be given a formal code which attempted to describe the given mathematical
   statement and its proof in Lean4.
   Your task is to evaluate a specific aspect of the formal code.
   The description of the aspect is: {OAP Description}
   Your need to give two things about your evaluation:
   1. the judgement of whether the formalization meets this aspect. This should be a binary
   value in “True" or “False".
   2. the detailed explanation of your judgement.
   You should wrap your final results in a way illustrated as the following:
   %%%%%%%%%%
   Explanation: Your Detailed Explanation
   Judgement: Your Binary Judgement
   %%%%%%%%%%
   Strictly follow the instructions that have been claimed.



                                                   23
                                     Table 3: Annotation criteria
    Logical Preservation (LP)
    From your point of view, does the formal code capture the logical structure and content of the
    natural language statement?
    1: Fully captures the logical structure and content.
    0.5: Partially captures the logical structure and content.
    0: Does not capture the logical structure or content.
    Mathematical Consistency (MC)
    From your point of view, does the formal code accurately represent mathematical objects and
    operations present in the natural language statement?
    1: Accurately represents all mathematical objects and operations.
    0.5: Partially represents the involved mathematical objects and operations.
    0: Does not represent the involved mathematical objects or operations.
    Formal Quality (FQ)
    From your point of view, does the formalized code alone demonstrate high quality in terms of
    structural clarity, readability, and usefulness?
    1: Demonstrates high structural clarity, readability, and usefulness.
    0.5: Demonstrates moderate structural clarity, readability, or usefulness.
    0: Does not demonstrate adequate structural clarity, readability, or usefulness.



     User Prompt:
     Natural language statement: {Natural Language Statement}
     Natural language proof: {Natural Language Proof}
     There are some Lean4 formal codes describing the given mathematical statement and its
     proof: {Formal Code}


H      Human Evaluation Criteria

We provide the detailed human evaluation criteria of formalizations in Table 3. Logical Preservation
(LP), Mathematical Consistency (MC), and Formal Quality (FQ) are rated on a 3-point scale. Since
mathematics is a rigorous discipline and formal languages are designed to reflect this rigor, any
human with sufficient knowledge of mathematics and formal language should be able to apply these
criteria consistently and reach similar judgments.


I     Discussion

Full-theorem autoformalization is essential for formal verification of claims, proof checking, and
knowledge discovery. In this context, minimizing false positives is crucial: incorrect claims should
not be validated, and flawed proofs should be repaired. Achieving this requires prioritizing alignment
between natural-language claims and formal statements, beyond relying solely on theorem-prover
pass rates. The masked composite objective captures this requirement, and our lower confidence
bound assumptions provide a theoretical framework for modeling the reliability of LLM judges
in evaluating alignment dimensions under uncertainty.
Our iterative monotonic framework shows that combining complementary LLMs with formal
verifier feedback produces formalizations with provably non-decreasing quality under realistic
evaluation noise. By explicitly modeling multiple dimensions of formalization quality and adaptively
allocating refinement effort, the framework provides a principled methodology for AI-assisted
autoformalization and the integration of machine-generated proofs. This makes it possible to reduce
human oversight in large-scale formal verification pipelines, potentially accelerating the formalization
of complex mathematical results.
Furthermore, by operating in a reference-free manner, our approach is broadly applicable even
in domains lacking extensive formal libraries, opening opportunities for formalizing underex-


                                                  24
plored areas of mathematics or science. The theoretical guarantees of monotonic improvement
also provide a foundation for future research in safe, reliable AI-assisted formal reasoning, where
uncertainty in judgment or verification can be explicitly quantified and controlled.

I.1   Limitations

One-sided uncertainty modeling of LLM judges. The uncertainty modeling of LLM judges in this
work focuses on a one-sided lower confidence bound (LCB), rather than full two-sided uncertainty
intervals. This choice is motivated by the design of our monotonic optimization framework, where
decision-making is based on conservative acceptance under lower-bound estimates. As a result, our
notion of reliability is also defined in terms of lower-bound guarantees. A more comprehensive
treatment of bidirectional uncertainty estimation is an interesting direction but is beyond the scope of
this study.
Potential bias from using LLM judges in both optimization and evaluation. LLM-based judges
are used both in the test-time optimization loop and in reporting soft-dimension evaluation metrics,
which may introduce systematic bias due to shared model preferences. To mitigate this concern, we
decouple formal correctness from LLM judgments by using the Lean4 theorem prover as an external
verifier for formal validity. In addition, human and cross-model evaluation are conducted to validate
the observed trends of the monotonic process. In our framework, LLM judges are explicitly modeled
as noisy and imperfect estimators rather than ground-truth oracles. The monotonic acceptance rule
based on lower confidence bounds is designed to reduce sensitivity to judge noise and promote
conservative updates. While these design choices reduce potential bias, we acknowledge that some
residual coupling between optimization and evaluation may remain, particularly in soft metrics.
Dependence on single-annotator human evaluation for uncertainty estimation. The empirical
estimation of uncertainty parameters in the LCB formulation relies on human evaluation conducted
by a single annotator. While this provides a consistent labeling signal, it may not fully capture
inter-annotator variability, and thus may introduce noise in the absolute calibration of uncertainty
estimates. Nevertheless, the evaluation is primarily used to characterize relative trends rather than
to establish absolute ground-truth values. Future work could explore multi-annotator protocols or
probabilistic annotation models to refine uncertainty estimation. Importantly, the proposed monotonic
process itself does not depend on perfect calibration of these parameters, and its qualitative behavior
remains consistent under reasonable perturbations of the estimates.
Computational cost of ensemble-based monotonic optimization. The proposed monotonic process
involves multiple LLM generations and evaluations, and thus incurs higher computational cost
compared to single-pass inference methods. This overhead is a direct consequence of its ensemble-
style decision mechanism and iterative refinement procedure. However, this cost is offset by improved
performance and stability across tasks. In addition, the framework naturally allows performance
to scale with increased computation budget (e.g., more iterations or stronger judges), suggesting a
form of test-time scaling behavior. Exploring more efficient variants of the monotonic process is a
promising direction for future work.

J     Additional Results, Tables, and Figures
The explicit results of the monotonic process, the monotonic process with GPT-5.4 only, and the
iterative self-refinement process are provided in Table 4, 5, and 6, respectively. The costs of different
settings, in terms of the number of LLM calls, are reported in Table 7. We provide a running example
of full-theorem autoformalization with our monotonic process for “Dummit-Foote_exercise_1_1_20”
from ProoNet in Figure 7. The explicit results of Recurrent Generators (REGs) are reported in
Table 8.




                                                  25
Table 4: Performance of the monotonic process. All numbers are reported in percentage.
                          miniF2F-Test                                      ProofNet-Test
t    πFV       π
               bLP    π
                      bMC       π
                                bFQ        Jb    Jb = 1   πFV     π
                                                                  bLP     π
                                                                          bMC      π
                                                                                   bFQ        Jb    Jb = 1
GPT-4.1-mini Judges
0    86.07    57.58   80.60     60.86    57.03     8.61   36.02   48.52   72.04    57.80    18.75     3.23
1    95.90    70.90   89.21     75.82    75.33    27.46   54.84   59.01   80.47    75.54    34.12     9.68
2    99.59    75.41   91.53     82.58    82.76    35.66   62.90   61.83   81.00    79.57    41.37    12.37
3   100.00    79.82   94.54     86.27    86.87    42.21   67.74   61.56   80.47    82.53    45.86    16.13
4   100.00    82.79   96.17     89.34    89.44    46.72   73.12   60.48   79.39    82.53    49.26    17.20
5   100.00    83.71   96.72     90.37    90.27    49.18   77.96   58.06   78.32    82.80    52.45    17.74
Qwen2.5-Coder-7B Judges
0      -      32.68   46.99     15.98    26.10    0.82      -     26.75   35.13    12.63     7.78    0.54
1      -      36.89   50.41     21.52    34.14    1.64      -     23.79   34.77    16.94    11.23    1.61
2      -      39.34   52.46     22.95    37.96    2.46      -     22.45   33.69    17.20    12.44    2.15
3      -      41.09   54.64     23.57    39.77    2.87      -     19.89   33.51    17.20    12.70    2.15
4      -      40.47   56.01     23.77    40.08    3.28      -     19.49   32.97    16.13    13.78    2.15
5      -      41.39   56.28     24.80    40.82    2.87      -     18.68   32.62    14.52    14.46    2.15
Human Evaluation
0      -      68.24   68.03     33.61    49.46    1.23      -     62.63   57.53    24.46    15.71    1.61
1      -      73.98   75.82     36.89    59.63    4.92      -     69.62   63.44    22.58    28.25    5.91
2      -      75.41   77.46     38.11    63.32    7.38      -     72.04   65.86    21.78    33.62    6.45
3      -      77.46   79.71     38.32    65.16    8.20      -     70.70   65.32    20.70    35.77    6.99
4      -      78.69   81.35     38.11    66.05    8.20      -     70.97   66.94    21.24    38.63    8.06
5      -      78.89   81.76     39.14    66.60    9.02      -     68.55   68.55    21.77    40.96    8.06




      Table 5: Performance of the monotonic process with a single LLM (GPT-5.4).
                          miniF2F-Test                                      ProofNet-Test
t    πFV      π
              bLP     π
                      bMC       π
                                bFQ       Jb     Jb = 1   πFV     π
                                                                  bLP     π
                                                                          bMC      π
                                                                                   bFQ       Jb     Jb = 1
GPT-4.1-mini Judges
0    43.44    81.15   94.26     70.49    37.20   17.62    11.29   86.29   95.16   75.00     10.23    5.91
1    52.87    86.78   96.72     80.74    46.76   26.64    16.13   91.40   97.49   82.26     14.83    9.68
2    56.56    86.78   96.45     84.43    50.27   31.15    17.20   92.88   98.39   86.56     16.10   11.83
3    59.02    88.01   96.58     85.04    52.96   34.84    20.43   93.28   98.21   89.78     19.03   13.98
4    59.43    89.65   97.54     86.48    54.34   37.30    20.97   93.55   98.39   91.67     19.65   15.05
5    60.66    90.16   97.54     87.09    55.64   38.52    21.51   94.49   98.57   92.47     20.19   15.59
Qwen2.5-Coder-7B Judges
0      -      57.48   62.57     34.22    20.94    4.10      -     56.85   56.99   41.67      5.92    2.69
1      -      59.53   62.70     35.66    24.74    4.92      -     57.53   56.81   41.67      8.14    3.76
2      -      59.73   62.70     37.09    26.88    4.92      -     60.48   58.60   42.74      8.84    3.76
3      -      59.53   63.93     36.89    28.26    4.92      -     60.08   57.89   42.74      9.78    3.76
4      -      59.43   63.80     36.07    28.17    4.92      -     60.75   58.24   44.09     10.07    3.76
5      -      59.22   63.66     35.86    29.01    4.92      -     61.83   58.60   44.35     10.42    3.76




                                                     26
Table 6: Performance of iterative self-refinement (ISR) with error feedback from the theorem prover
and no acceptance policy.
                                miniF2F-Test                                            ProofNet-Test
      t     πFV     π
                    bLP     π
                            bMC       π
                                      bFQ        Jb     Jb = 1     πFV      π
                                                                            bLP       π
                                                                                      bMC      π
                                                                                               bFQ       Jb      Jb = 1
      ISR-DeepSeek-Prover-V2-7B
      0     50.41   47.75   80.05     45.08     32.23    6.97      14.52    41.94     69.71   38.17     7.75      1.08
      1     47.13   48.16   78.28     43.03     29.47    6.15       8.06    40.59     68.64   32.53     5.46      2.15
      2     48.77   49.90   81.42     40.57     30.87    5.74       9.14    39.38     69.18   29.57     6.91      2.15
      3     49.59   51.33   80.05     39.34     31.74    5.74       8.06    40.19     69.53   34.95     5.76      2.69
      4     48.77   50.20   78.83     37.70     30.56    4.92       7.53    42.20     72.58   30.38     5.48      2.69
      5     50.41   52.46   81.01     40.78     33.06    6.15       6.99    42.20     71.68   31.72     5.26      2.15
      ISR-Goedel-Prover-V2-8B
      0     65.16   46.62   75.82     47.54     39.12    2.46      22.04    33.47     58.60   36.02      9.93     1.61
      1     60.66   40.06   69.67     48.98     36.04    2.05      17.74    25.40     53.05   35.48      8.91     2.69
      2     60.66   38.52   68.44     46.31     35.08    1.64      18.28    26.08     54.84   33.33      7.60     2.15
      3     59.43   38.32   65.98     44.88     34.37    2.46      21.51    27.55     53.76   36.02      9.20     1.61
      4     57.38   37.60   65.44     48.98     32.70    2.05      20.97    25.13     52.51   36.56      8.38     1.08
      5     55.74   37.30   65.98     46.72     30.72    1.64      23.66    23.52     52.33   35.22     10.21     1.08
      ISR-GPT-5.4
      0     30.74   80.94   94.54     72.54     26.84   14.75       9.68    90.32     97.31   73.92      9.04      3.76
      1     44.67   80.43   95.22     78.48     39.32   21.31      10.75    86.69     94.09   75.81      9.99      6.45
      2     49.18   81.66   93.99     75.20     42.93   22.13      15.05    86.56     96.06   77.42     14.02      8.60
      3     53.28   80.84   94.26     76.64     46.28   22.54      17.74    84.68     96.06   71.51     16.60     11.83
      4     52.46   79.82   95.49     74.18     45.89   23.77      18.82    88.71     95.70   77.42     17.54     11.83
      5     54.92   81.25   95.08     76.23     48.01   23.36      18.82    86.56     95.70   75.00     17.63     12.37




Table 7: Costs of different settings measured in LLM calls. Mean and standard deviation are computed
on a per-sample basis. "Total" denotes the aggregate over all samples in the datasets.
                                            Generator Calls               Judge Calls
                                      Mean      Std    Total      Mean       Std       Total
          Best-of-k, k = 8
          DeepSeek-Prover-V2-7B                8.00       -        3,440            55.95       17.99          24,057
          Goedel-Prover-V2-8B                  8.00       -        3,440            57.20       17.21          24,597
          GPT-5.4                              8.00       -        3,440            66.06       12.99          28,404
          Iterative Self-Refinement (6 Iterations)
          Per Iteration                        1.00       -         430              9.00          -            3,870
          Overall                              6.00       -        2,580            54.00          -           23,220
          The Monotonic Process – Single (GPT-5.4)
          Iteration 0                          1.78     0.41        766              9.00        0.00           3,870
          Iteration 1                          1.63     0.70        701              7.51        3.34           3,231
          Iteration 2                          1.52     0.80        655              6.70        3.93           2,880
          Iteration 3                          1.46     0.84        627              6.43        4.07           2,763
          Iteration 4                          1.41     0.87        608              6.01        4.24           2,583
          Iteration 5                          1.39     0.89        599              5.90        4.28           2,538
          Overall                              9.20     4.11       3,956            41.55       17.48          17,865
          The Monotonic Process – Ensemble
          Iteration 0                          4.42     1.54       1,900            28.88        6.93          12,420
          Iteration 1                         11.78      3.92       5,067            49.37      32.54          21,231
          Iteration 2                         10.17      5.47       4,371            34.93      32.86          15,021
          Iteration 3                          9.56     5.90       4,112            29.74       31.56          12,789
          Iteration 4                          8.89     6.25       3,823            25.81       30.79          11,097
          Iteration 5                          8.53     6.38       3,666            22.81       29.14           9,810
          Overall                             53.35     26.48      22,939           191.55     135.43          82,368



                                                              27
                                                       NL Statement
                For    an element in show that and            have the same order.                                                                                                                                        Feedback of LLM Judges
                                                         NL Proof                                                                            theorem order_of_inverse (G : Type*)
                Recall that the order of a group element is either a positive integer or                                                    [Group G] (x : G) : orderOf x = orderOf                                     Aspect: OAP1 Description
                infinity. Suppose     is infinite and that           for some . Then                                                                        x⁻¹ := by                                                   Evaluation:
                                                                                                                                             have h₁ : orderOf x = orderOf x⁻¹ := by
                                                                                                                                                                                                                        Explanation: ...
                                                                                                                                                          apply Eq.symm
                                                                                                                                                          apply Eq.symm                                                 Judgment: ...
                a contradiction. So if          is infinite,        must also be infinite. Likewise, if                         is
                infinite, then                         is also infinite. Suppose now that          and
                                                                                                                                                    rw [← orderOf_injective                                             Aspect: OAP2 Description
                       are both finite. Then we have
                                                                                                                                                (MulAut.conj x).toMonoidHom                                             Evaluation:
                                                                                                                                                 (MulAut.conj x).injective x⁻¹]                                         Explanation: ...
                                                                                                                                              simp [MulAut.conj_apply, mul_assoc,
                                                                                                                                                                                                                        Judgment: ...
                so that            . Likewise,             . Hence               and      and         have the same order.
                                                                                                                                                  mul_right_inj, mul_left_inj]
                                                                                                                                                             exact h₁




       OOG Prompt                                                           OOG Prompt                                                     REG Prompt with LP                                        REG Prompt with LP                                              REG Prompt with FQ
   DeepSeek-Prover-V2-7B                                                 Goedel-Prover-V2-7B                                                 SeedCoder-8B                                               Qwen2.5-7B                                                  DeepSeek-Prover-V2-7B

import Mathlib                                                                                                                       import Mathlib                                           import Mathlib
open BigOperators Real Nat Topology                                import Mathlib                                                    open BigOperators Real Nat Topology                      open BigOperators Real Nat Topology
                                                                                                                                                                                                                                                                 import Mathlib
theorem order_of_inverse (G : Type*) [Group G] (x : G) :           open BigOperators Real Nat Topology                               theorem order_of_inverse {G : Type*} [Group G] (x : G)   theorem order_of_inverse {G : Type*} [Group G] (x : G)
orderOf x = orderOf x⁻¹ := by                                      theorem order_inv_eq_order (x : G) : orderOf x =                  : orderOf x = orderOf x⁻¹ := by                          : orderOf x = orderOf x⁻¹ :=
                                                                                                                                                                                                                                                                 open BigOperators Real Nat Topology
 have h₁ : orderOf x = orderOf x⁻¹ := by                           orderOf x⁻¹ := by                                                   have h_infinite : orderOf x = orderOf x⁻¹ := by        begin
   apply Eq.symm                                                    have h₁ : orderOf x = orderOf x⁻¹ := by                             rw [← orderOf_inv]                                      -- Case 1: Both orders are infinite
                                                                                                                                                                                                                                                                 theorem order_of_inverse {G : Type*} [Group G] (x : G)
   apply Eq.symm                                                      -- Use the property that the order of an element is the           simp [orderOf_eq_zero_iff]                              have h_infinite : (orderOf x = ∞) → (orderOf (x⁻¹) = ∞),
                                                                                                                                                                                                                                                                 : orderOf x = orderOf x⁻¹ := by
   rw [← orderOf_injective (MulAut.conj                            same as the order of its inverse                                     aesop                                                   {rintro h,
                                                                                                                                                                                                                                                                   rw [← orderOf_inv]
x).toMonoidHom (MulAut.conj x).injective x⁻¹]                         rw [← orderOf_inv]                                               have h_finite : orderOf x = orderOf x⁻¹ := by              rw [← orderOf_inv],
                                                                                                                                                                                                                                                                   <;> simp [orderOf_eq_zero_iff]
   simp [MulAut.conj_apply, mul_assoc, mul_right_inj,                 <;> simp [orderOf_inv]                                            rw [← orderOf_inv]                                        simp only [orderOf_eq_top],
                                                                                                                                                                                                                                                                   <;> aesop
mul_left_inj]                                                       exact h₁                                                            ...                                                       exact h
 exact h₁                                                                                                                                                                                     ...




                                                                                                          If Incorrect                                                                        If Incorrect



                                                          FVR Prompt                                                                                                                                                    FVR Prompt
                                                     DeepSeek-Prover-V2-7B                                                                                                                                           Goedel-Prover-V2-7B

                                                  import Mathlib                                                                                                                                              import Mathlib

                                                  open BigOperators Real Nat Topology                                                                                                                         open BigOperators Real Nat Topology

                                                  theorem order_inv_eq_order (x : G) : orderOf x =                                                                                                            theorem order_inv_eq_order (x : G) : orderOf x =
                                                  orderOf x⁻¹ := by                                                                                                                                           orderOf x⁻¹ := by
                                                   have h₁ : orderOf x = orderOf x⁻¹ := by                                                                                                                     have h₁ : orderOf x = orderOf x⁻¹ := by
                                                     rw [← orderOf_inv]                                                                                                                                          rw [← orderOf_inv]
                                                     <;> simp [orderOf_inv]                                                                                                                                      <;> simp [orderOf_inv]
                                                   exact h₁                                                                                                                                                    exact h₁




                                                                                                            If Correct




                                  LP OAP Judge Prompt                                              MC OAP Judge Prompt                                               FQ OAP Judge Prompt
                                      GPT-4.1-mini                                                    GPT-4.1-mini                                                      GPT-4.1-mini

                            Explanation: ...                                                 Explanation: ...                                                  Explanation: ...
                            Judgment: True/False                                             Judgment: True/False                                              Judgment: True/False




                                                                                  Acceptance Policy Based on




                                                                                        theorem order_of_inverse {G : Type*} [Group G] (x : G) : orderOf x = orderOf x⁻¹ := by
                                                                                         rw [← orderOf_inv]
                                                                                         <;> simp [orderOf_eq_zero_iff]
                                                                                         <;> aesop



Figure 7: Illustrative example of a single step in the monotonic process. The monotonic process
enables the construction of high-quality formalizations that are both formally valid, as verified by the
theorem prover, and semantically aligned, as evaluated by LLM judges.




                                                                                                                                                          28
Table 8: Performance of refinement with feedback. All results are based on zero-shot autoformaliza-
tion.
                        Generator Type        LLM                           Feedback   πFV     π
                                                                                               bLP     π
                                                                                                       bMC     π
                                                                                                               bFQ      Jb

         miniF2F-Test

         Baseline       One-Off Generator     DeepSeek-Prover-V2-7B         -          50.41   55.02   80.87   51.02   35.15
                        Recurrent Generator   Qwen2.5-7B-Instruct           LP          4.10   56.05   86.20   34.84   3.53
                        Recurrent Generator   Qwen2.5-7B-Instruct           MC         4.92    55.43   85.52   39.34   4.17
                        Recurrent Generator   Qwen2.5-7B-Instruct           FQ         7.79    50.72   84.84   49.59   6.89
                        Recurrent Generator   Qwen2.5-7B-Instruct           ALL         4.10   53.89   87.30   43.44   3.72
                        Recurrent Generator   Seed-Coder-8B-Instruct        LP         22.54   64.86   89.34   45.90   19.51
                        Recurrent Generator   Seed-Coder-8B-Instruct        MC         31.97   57.07   87.70   52.25   26.14
                        Recurrent Generator   Seed-Coder-8B-Instruct        FQ         25.41   56.66   82.65   56.15   21.94
                        Recurrent Generator   Seed-Coder-8B-Instruct        ALL        28.28   55.53   81.83   49.39   22.42
                        Recurrent Generator   DeepSeek-Prover-V2-7B         LP         50.82   59.02   84.29   51.64   36.04
                        Recurrent Generator   DeepSeek-Prover-V2-7B         MC         49.18   56.15   84.43   51.43   35.44
                        Recurrent Generator   DeepSeek-Prover-V2-7B         FQ         51.23   59.53   84.15   53.07   37.45
                        Recurrent Generator   DeepSeek-Prover-V2-7B         ALL        50.82   56.86   83.06   51.43   36.79
                        Recurrent Generator   Goedel-Prover-V2-8B           LP         50.00   44.98   73.50   48.57   33.45
                        Recurrent Generator   Goedel-Prover-V2-8B           MC         51.23   47.44   75.82   48.77   35.36
                        Recurrent Generator   Goedel-Prover-V2-8B           FQ         53.28   52.66   78.96   53.48   37.93
                        Recurrent Generator   Goedel-Prover-V2-8B           ALL        52.46   41.91   71.58   45.70   32.50

         Baseline       One-Off Generator     Goedel-Prover-V2-8B           -          58.61   47.34   73.63   49.80   35.61
                        Recurrent Generator   Qwen2.5-7B-Instruct           LP          0.82   51.23   83.06   28.69   0.82
                        Recurrent Generator   Qwen2.5-7B-Instruct           MC         2.05    46.82   83.61   35.25   1.64
                        Recurrent Generator   Qwen2.5-7B-Instruct           FQ         10.66   44.88   81.01   45.08   9.10
                        Recurrent Generator   Qwen2.5-7B-Instruct           ALL         8.20   51.74   82.79   39.14   7.50
                        Recurrent Generator   Seed-Coder-8B-Instruct        LP         17.62   52.77   81.56   39.96   13.62
                        Recurrent Generator   Seed-Coder-8B-Instruct        MC         27.05   50.00   82.92   47.34   19.92
                        Recurrent Generator   Seed-Coder-8B-Instruct        FQ         25.00   44.98   76.64   52.46   17.88
                        Recurrent Generator   Seed-Coder-8B-Instruct        ALL        27.46   47.44   79.10   48.57   19.77
                        Recurrent Generator   DeepSeek-Prover-V2-7B         LP         56.56   49.28   77.19   50.61   35.83
                        Recurrent Generator   DeepSeek-Prover-V2-7B         MC         55.74   48.77   77.32   47.95   34.57
                        Recurrent Generator   DeepSeek-Prover-V2-7B         FQ         57.38   49.08   75.68   50.82   35.54
                        Recurrent Generator   DeepSeek-Prover-V2-7B         ALL        56.97   45.90   74.86   49.18   35.04
                        Recurrent Generator   Goedel-Prover-V2-8B           LP         52.46   40.27   68.31   48.16   32.17
                        Recurrent Generator   Goedel-Prover-V2-8B           MC         54.51   40.57   70.22   48.77   32.91
                        Recurrent Generator   Goedel-Prover-V2-8B           FQ         54.92   45.59   73.63   50.61   35.30
                        Recurrent Generator   Goedel-Prover-V2-8B           ALL        59.02   40.37   67.90   45.90   33.53

         ProofNet-Test

         Baseline       One-Off Generator     DeepSeek-Prover-V2-7B         -          11.83   41.80   67.38   35.75   7.14
                        Recurrent Generator   Qwen2.5-7B-Instruct           LP          0.54   40.46   75.99   22.04   0.31
                        Recurrent Generator   Qwen2.5-7B-Instruct           MC         2.15    42.07   74.55   22.85   1.82
                        Recurrent Generator   Qwen2.5-7B-Instruct           FQ         0.54    40.86   74.73   23.12   0.54
                        Recurrent Generator   Qwen2.5-7B-Instruct           ALL         0.54   43.55   76.34   22.58   0.54
                        Recurrent Generator   Seed-Coder-8B-Instruct        LP          6.45   45.83   76.16   31.45    4.69
                        Recurrent Generator   Seed-Coder-8B-Instruct        MC          6.45   42.34   73.48   31.45   5.29
                        Recurrent Generator   Seed-Coder-8B-Instruct        FQ          4.84   42.20   72.22   33.60   4.26
                        Recurrent Generator   Seed-Coder-8B-Instruct        ALL         7.53   40.86   72.22   29.30    5.29
                        Recurrent Generator   DeepSeek-Prover-V2-7B         LP         11.29   44.62   73.12   35.22   6.66
                        Recurrent Generator   DeepSeek-Prover-V2-7B         MC         10.22   43.95   73.48   39.52   6.54
                        Recurrent Generator   DeepSeek-Prover-V2-7B         FQ         11.83   46.24   72.76   40.86   7.50
                        Recurrent Generator   DeepSeek-Prover-V2-7B         ALL        12.90   45.30   72.94   40.05    8.23
                        Recurrent Generator   Goedel-Prover-V2-8B           LP         20.43   37.50   62.01   41.67   12.40
                        Recurrent Generator   Goedel-Prover-V2-8B           MC         18.82   32.53   60.93   44.35   11.81
                        Recurrent Generator   Goedel-Prover-V2-8B           FQ         11.83   40.46   67.03   39.52   8.12
                        Recurrent Generator   Goedel-Prover-V2-8B           ALL        16.67   32.53   63.08   38.17   10.26

         Baseline       One-Off Generator     Goedel-Prover-V2-8B           -          17.74   31.59   63.44   29.84   6.89
                        Recurrent Generator   Qwen2.5-7B-Instruct           LP          1.61   33.33   72.58   13.44   1.30
                        Recurrent Generator   Qwen2.5-7B-Instruct           MC         1.08    33.74   71.86   15.59   1.08
                        Recurrent Generator   Qwen2.5-7B-Instruct           FQ         1.61    31.85   70.07   18.28   1.57
                        Recurrent Generator   Qwen2.5-7B-Instruct           ALL         1.61   35.62   70.61   17.47   1.52
                        Recurrent Generator   Seed-Coder-8B-Instruct        LP          3.23   32.66   68.64   18.55   2.76
                        Recurrent Generator   Seed-Coder-8B-Instruct        MC          4.30   33.60   70.43   22.58   3.29
                        Recurrent Generator   Seed-Coder-8B-Instruct        FQ          3.23   32.12   66.67   25.27   2.66
                        Recurrent Generator   Seed-Coder-8B-Instruct        ALL         4.84   30.91   63.98   24.46   3.54
                        Recurrent Generator   DeepSeek-Prover-V2-7B         LP         15.05   35.48   67.56   32.80   7.97
                        Recurrent Generator   DeepSeek-Prover-V2-7B         MC         14.52   34.14   68.46   30.11   6.82
                        Recurrent Generator   DeepSeek-Prover-V2-7B         FQ         14.52   35.35   67.20   34.14   7.26
                        Recurrent Generator   DeepSeek-Prover-V2-7B         ALL        16.13   34.95   66.31   33.87   7.57
                        Recurrent Generator   Goedel-Prover-V2-8B           LP         16.13   21.91   53.41   34.14   8.65
                        Recurrent Generator   Goedel-Prover-V2-8B           MC         19.35   21.51   51.25   34.68   9.98
                        Recurrent Generator   Goedel-Prover-V2-8B           FQ         17.74   25.27   58.60   34.68   8.74
                        Recurrent Generator   Goedel-Prover-V2-8B           ALL        18.82   24.19   56.81   36.83   8.96




                                                                       29
