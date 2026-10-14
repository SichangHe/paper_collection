                                                Reinforcement Learning with Verifiable Physics:
                                                Post-training LLMs with Continuous Rewards


                                                                Pengfei Cai ∗                                   Utkarsh Utkarsh∗
                                                     Massachusetts Institute of Technology              Massachusetts Institute of Technology

                                                              Alan Edelman                               Christopher Vincent Rackauckas †
                                                     Massachusetts Institute of Technology              Massachusetts Institute of Technology

                                                                                    Rafael Gomez-Bombarelli†
                                                                                Massachusetts Institute of Technology
arXiv:2607.10474v1 [cs.LG] 11 Jul 2026




                                                                                                 Abstract
                                                      Partial differential equations (PDEs) are foundational to modeling in science and
                                                      engineering, but constructing reliable numerical solvers remains labor-intensive,
                                                      demanding expert knowledge of discretization schemes, stability conditions, and
                                                      boundary treatments. Recent work has begun to frame PDE solving as a code-
                                                      generation task for large language models (LLMs), yet existing approaches operate
                                                      primarily at inference time: relying on prompting, debugging, self-refinement, and
                                                      test-time scaling rather than adapting the model itself. In parallel, reinforcement
                                                      learning with verifiable rewards has emerged as a powerful post-training paradigm
                                                      for code and math reasoning, but its verifiers are typically binary: a compiler runs,
                                                      or a test passes. Such signals discard the graded structure of scientific correctness,
                                                      where two solvers may both execute and yet differ in solution accuracy by orders
                                                      of magnitude. In this work, we introduce RLVP: Reinforcement Learning with
                                                      Verifiable Physics, an RL post-training framework for multi-PDE solver code
                                                      generation. RLVP addresses this verifiability gap with a hybrid verifier: hard
                                                      program-validity checks ensure executability, while continuous physics rewards
                                                      score function-space accuracy and PDE-residual consistency. A single policy is
                                                      post-trained across diverse PDE families spanning hyperbolic, parabolic, elliptic,
                                                      and incompressible-flow systems. RLVP improves over both pre-trained and
                                                      supervised-only baselines on PDE benchmarks, and shows zero-shot improvement
                                                      transfer to held-out PDEs. We show that a smaller LLM post-trained with RLVP can
                                                      outperform prompting a frontier model on in-distribution PDE solver generation.
                                                      The trained policy shows evidence of compositionality in numerical motifs: it
                                                      recombines stencils, time-stepping schemes, and boundary-handling primitives
                                                      learned from the PDEs used in training into generated solvers for unseen PDE
                                                      problems.


                                         1     Introduction
                                         Partial differential equations (PDEs) are a central language of the physical sciences, governing
                                         systems in fluid dynamics, heat transfer, electromagnetism, structural mechanics, and beyond [1–3].
                                         Decades of scientific computing have produced powerful solver families, including finite-difference,
                                             ∗ Equal contribution. Order decided by coin toss.
                                             † Corresponding authors: crackauc@mit.edu, rafagb@mit.edu




                                         Preprint.
finite-volume, finite-element, spectral, implicit, and operator-splitting schemes [2–5]. Yet writing a
reliable solver remains a specialized task: correctness depends on discretization, stability constraints,
boundary treatment, time integration, solver tolerances, and physical invariants. Code can compile,
return arrays of the right shape, and still violate a CFL condition, mishandle a boundary, introduce
excessive diffusion, or produce a qualitatively wrong solution.
Large language models (LLMs) have become strong code generators and coding agents [6–11],
raising the question of whether PDE solver construction can be automated as code generation. Recent
work suggests that this direction is promising but incomplete: LLMs can produce plausible scientific
code, but reliable solver accuracy often requires domain-informed prompting, execution feedback,
debugging loops, self-refinement, agentic orchestration, or test-time scaling [12–19]. These inference-
time methods can improve individual outputs, but they do not amortize numerical reliability into the
model’s solver-writing distribution. We instead ask whether the experience of executing and grading
PDE solvers can be converted into model parameter updates.
Reinforcement learning with verifiable rewards (RLVR) provides a natural starting point: models can
improve when trained against rule-based execution feedback rather than imitation alone [20, 21, 9, 22].
However, standard RLVR verifiers are usually binary: an answer matches, a unit test passes, or a
format constraint is satisfied. PDE solver generation is graded rather than binary. A generated
program may be executable and finite while still being unstable, overly diffusive, dispersive, biased,
or inconsistent with the governing equation; two valid programs may differ by orders of magnitude in
solution error. This graded structure makes PDE simulation an unusually rich verifiable environment:
predicted trajectories can be compared to hidden numerical references, checked for physics residual
consistency, and evaluated across held-out grids, parameters, initial and boundary conditions.
We introduce Reinforcement Learning with Verifiable Physics (RLVP), a post-training framework for
PDE solver code generation. Starting from supervised fine-tuning on a curated bank of teacher solvers,
we apply GRPO [20] with a hybrid verifier: hard execution-validity gates ensure program feasibility,
while continuous function-space rewards score generated solutions against hidden references with
residual-consistency regularization. This moves physical feedback from post-hoc evaluation into
the training loop. A single policy is trained jointly across eight PDE families spanning hyperbolic
transport, parabolic reaction–diffusion, steady elliptic problems, and incompressible Navier–Stokes.
Our contributions are:

      1. Hybrid binary–continuous verifier for PDE solver code. We design an RLVR-style
         verifier whose complete reward combines hard program validity V , a continuous physical
         accuracy reward Rtraj based on function-space trajectory error, and a physics residual
         consistency reward Rphys . The verifier is computed deterministically from numerical
         reference solutions and PDE residuals, with no learned reward model in the loop. The
         hybrid reward outperforms a binary-validity-only baseline by 8–13 percentage points while
         reducing nRMSE by 38%, demonstrating that continuous physical accuracy contributes
         substantially beyond binary execution feedback.
      2. A multi-PDE solver-bank and open post-training recipe. We curate a solver-code dataset
         spanning 8 PDE families and 71 standard numerical schemes, including finite-difference
         stencils, conservative updates, CFL substepping, sparse linear solves, projection steps,
         and boundary conditions handling. We pair this dataset with a reproducible RLVP post-
         training pipeline built on vLLM [23] and verl [24], which we will release together with
         the verifier environment and training recipes. Unlike prompt engineering approaches that
         require detailed PDE-specific domain knowledge, our pipeline uses simpler prompts, making
         post-trained models closer to useful scientific computing agents for broader audience.
      3. Multi-PDE post-training. A single policy is trained jointly across PDE families spanning
         hyperbolic, parabolic, elliptic, and incompressible-flow systems in 1D and 2D. To our
         knowledge, this is the first verifiable-reward RL pipeline that post-trains one model across
         PDE families rather than specializing to a single equation or narrow benchmark distribution.
      4. Small RLVP-trained models can outperform larger static prompting baselines. Across
         model sizes (3B, 7B, 14B), the post-trained policy matches or exceeds substantially larger
         frontier baselines under the same direct-generation protocol.
      5. Selective zero-shot cross-PDE transfer. The trained policy improves solver code gen-
         eration on held-out PDEs absent from training, especially by recombining or extending


                                                   2
         numerical structures, indicating that RLVP post-training can instill transferable numerical-
         programming motifs rather than per-prompt template memorization.

                                                           RLVP policy update:




         1 Prompts + Solver bank SFT         2      Sample rollouts                               3   Verifiable Physics Reward                         4     RLVP update

                   8 PDE tasks                                                                                                                           Group-relative ranking
                                                                                                               Physical                    Residual
                                                         Policy πθ                 Validity                                                             normalized advantages Âi
                                                                                                               Accuracy                   Consistency
                                                                                                                                                           KL anchor to SFT
                                                                                    V(y,c)                     Rtraj(y,c)                  Rphys(y,c)
                                                                                                         predicted   reference
                  Prompt formats:                n candidate solver programs     ✓ executes
                      generic /                                                  ✓ correct shape
                                                         import numpy as np
               parameter-conditioned /       rollout 1   from scipy.sparse       ✓ finite values
                   IC-conditioned                        def solve(params):
                                                           ...
                                                                                                                                                            Updated policy

                                                         import numpy as np                                                                                      πθnew
                                             rollout 2   def solve(params):                           Complete RLVP reward
                                                           ...

                Teacher solver bank              ⋯                                            R(y,c) = V(y,c) · Rtraj(y,c) · Rphys(y,c)
             PDE solver codes using only                 import numpy as np
                                                         from scipy.linalg
                                             rollout n
               Numpy or Scipy imports                    def solve(params):                                                                                  Generates better
                                                                                                                                                        ◎ solvers (improved
                                                           ...


                                                                                                                                                             solution quality)
                                                                                             r1           r2           r3                 rn
                                                                                                                                 ⋯                           Solver motif
                                                                                                                                                        ✣ recombination
          Warm start supervised finetuning   For each prompt, sample                                                                                         for OOD transfer
          on PDE solver bank training data   multiple candidate solvers




Figure 1: Overview of RLVP for multi-PDE solver code generation. We warm-start the policy
with supervised fine-tuning (SFT) on a multi-PDE solver bank across diverse PDE problems. During
RL, sampled solver programs are executed by the RLVP verifier and scored by a reward combining
validity, physical accuracy against hidden numerical references, and physics residual consistency.
Group-relative advantages update the policy with a KL anchor to the SFT model.


2   Related Work
LLMs for PDEs and Scientific Computing. A growing line of work treats scientific simulation as
a code-generation problem and probes the limits of LLMs in that role [12, 13, 25, 14, 15]. Within this
space, existing systems pursue different strategies. CodePDE studies PDE solver construction directly
and improves reliability through inference-time refinement against numerical references, including
reasoning chains, debugging loops, self-refinement, and test-time scaling [12]. Other scientific-code-
generation systems emphasize domain-informed prompting, numerical-method guidance, agentic
orchestration, or fine-tuning to improve executability and numerical validity across broader scientific
computing tasks [13–17]. More broadly, research-grade scientific coding benchmarks show that
realistic scientific programming remains difficult for modern LLMs, despite strong performance
on generic code benchmarks [25]. Thus, prior work largely improves scientific reliability through
inference-time guidance, reference-solution feedback, or agentic refinement; RLVP instead studies
whether numerical and physical preferences can be internalized through post-training.

LLMs as Simulator Agents and Simulator-Grounded Learners. A related but distinct line of
work uses LLMs to operate scientific simulators or to learn from simulation outcomes. Simulator-
agent systems treat mature scientific software as an external backend: the LLM writes input files,
code wrappers, configuration scripts, or domain-specific commands, while the numerical solver
itself remains fixed by the underlying software stack [26–32]. Other work uses simulation-derived
signals as supervision for reasoning or scientific model construction, including sparse simulator
rewards, preferences, curated physics outcomes, or execution rewards [33–35]. These works establish
simulators as tools and feedback sources for LLMs. RLVP differs in the object being trained: the
model is post-trained to generate the numerical PDE solver itself, and the verifier scores the executed
solution using reference-solution error and PDE-residual information.

Reinforcement Learning with Verifiable Rewards. RL with verifiable rewards (RLVR) has
become a central post-training paradigm for code and mathematical reasoning [20, 21, 36, 37]. In
its canonical form, the verifier is binary or near-binary: DeepSeek-R1 uses rule-based accuracy and
format rewards and avoids learned reward models in R1-Zero [21], while DAPO and GSPO refine
GRPO through improved normalization, stability, and open RL system design [36, 37]. Related work
on RL for code generation has used unit-test outcomes, learned critic signals, compiler-feedback
curricula, and iterative execution-feedback grounding [9, 38, 11, 39]. Recent methods move beyond
strict binary supervision through process-level reward models and graded correctness signals [40, 22].
However, these verifiers still largely operate on discrete outcomes, labels, or program-execution.


                                                                                 3
Scientific Machine Learning. A central paradigm in scientific machine learning trains neural
networks to approximate PDE solution operators or solution fields directly. Physics-informed neural
networks (PINNs) and related methods minimize PDE residuals on network outputs [41]; neural
operators learn solution maps between function spaces [42–44]; and benchmarks such as PDEBench
standardize the evaluation of these surrogates against numerical references using trajectory-level
L2 error [45]. More recently, generative PDE surrogates have used diffusion and flow-matching
objectives to model distributions over physical fields [46–49]. These approaches use physics to train,
regularize, or constrain neural surrogates that directly output physical states. In contrast, RLVP does
not train a neural network to be the simulator. It post-trains a language model to write conventional
numerical-methods code, using reference-solution error and PDE residuals as execution-grounded
verifier rewards on the generated program.
3     Methodology
We frame PDE solver synthesis as a code-generation problem and post-train language models with
a verifier that provides continuous feedback over function-valued numerical outputs. Code is the
action; physics is the verifier. The model emits a solver program, which is run inside an execution
environment and graded by comparing the resulting trajectory to the function-space behavior of a
reference solution. This differs from standard RLVR, where correctness is typically determined
by sparse rule-based checks such as unit-test pass/fail outcomes [9, 22, 20]. PDE correctness is
intrinsically graded: a generated solver may execute and return arrays of the correct shape while still
being unstable, biased, diffusive, dispersive, or inconsistent with the underlying physical law. Our
verifier exploits this graded structure to provide a richer optimization signal than binary execution
outcomes alone, while retaining the rule-based verifiability that makes RLVR attractive.
Our pipeline has two stages. Supervised fine-tuning (SFT) on a curated bank of teacher solvers
initializes the policy within the space of executable numerical programs. RL then sharpens this prior
using a hybrid binary–continuous verifier that rewards execution validity, physical accuracy, and PDE
residual consistency. Thus, we follow the standard warm-start SFT plus RL recipe [50, 20, 21], but
replace discrete answer verification with execution-grounded physical verification.

3.1   Numerical PDE Solver Synthesis as a Code-Generation Task

Let x denote a prompt specifying a PDE, inputs, and the required code interface. A policy πθ
generates a candidate solver program y ∼ πθ (· | x), where y is an implementation, not a numerical
solution array. Each program is evaluated on hidden PDE instances c = (Ωh , T , u0 , µ, b), where
Ωh is the mesh, T the requested output times, u0 the initial condition when applicable, µ the PDE
parameters, and b the boundary/forcing data. Sandboxed execution returns U b = Exec(y, c), as either
a steady field or a time-indexed trajectory. The verifier compares U to a hidden reference solution
                                                                   b
U ⋆ ; physical correctness enters training only through rewards computed after execution.

3.2   Multi-PDE Environment

We train one policy across eight PDE families spanning hyperbolic transport, nonlinear conservation
laws, parabolic reaction–diffusion, elliptic steady-state solves, and incompressible flow in 1D and 2D.
Hidden verifier instances vary grid resolutions, output times, parameters, and initial conditions; where
boundary treatments also differ across PDE problems. Thus, high reward requires an algorithmic
solver rather than memorized outputs. Full equations, parameter ranges, boundary conditions, and
reference-solver configurations are in Appendix B.1.
Prompt design. Prompts are sampled in three forms: generic, parameter-conditioned, and parameter
and initial condition conditioned. All forms specify the mathematical problem and the same solver
interface, but not the numerical method. Concrete examples, sampling weights, and per-PDE counts
are provided in Appendix I.

3.3 Solver-Bank Supervised Fine-Tuning
Direct RL from a base language model is inefficient because most early generations fail before
producing meaningful physical feedback. We therefore construct a solver bank Bp for each PDE
family p, containing executable teacher implementations that cover common numerical idioms,
including finite-difference stencils, conservative updates, CFL substepping, sparse linear solves,


                                                   4
projection steps, and boundary-condition handling. Detailed solver-bank tables and verification
checks are in Appendix B.2. We report numerical verifications of the solver bank in Appendix B.3,
including self-convergence and MMS checks.
Given prompt–solver pairs {(xi , yiteach )}M
                                                            S
                                           i=1 drawn from p Bp , we minimize the standard supervised
                                1
                                    P  M            teach
next-token loss LSFT (θ) = − M         i=1 log πθ (yi     | xi ). SFT provides a solver prior: it places
executable schemes within the policy support and raises execution success to the regime where
verifier feedback becomes informative. RL then optimizes hidden-instance robustness, stability, and
physics consistency.

3.4   Verifier Design for PDE Solver Generation

PDE solvers do not have a clean binary notion of correctness: a program can execute, return the right
shape, and contain only finite values while still being unstable, biased, or inconsistent with the PDE.
This creates a verifiability gap: hard checks are needed for program feasibility, but they discard the
graded numerical quality that separates a barely stable approximation from an accurate solver. RLVP
closes this gap by gating continuous function-space feedback with binary execution checks, so invalid
programs receive zero reward while valid programs are ranked by the physical field they return. Let p
index the PDE family, and let Rp [u; µ, b] = 0 denote its residual form. For time-dependent problems,
this may be written as Rp [u; µ, b] = ∂t u + Np [u; µ, b], while for steady-state problems it may encode
an elliptic operator or constraint. Let u⋆ : [0, T ] × Ω → Rdu denote the reference solution on spatial
domain Ω, and let u b denote the generated solution. For time-dependent problems, we measure error
with the normalized space-time L2 metric


                    u − u⋆ ∥L2 ([0,T ]×Ω)
                   ∥b                                       2
                                                                           Z TZ
                                                                                                         2
       u, u⋆ ) =
Ltraj (b                                    ,    u − u⋆ ∥L2 ([0,T ]×Ω) =
                                                ∥b                                    u(t, x) − u⋆ (t, x)∥2 dx dt.
                                                                                     ∥b
                   ∥u⋆ ∥L2 ([0,T ]×Ω) + ϵ                                   0    Ω
                                                                                                               (1)
For steady-state problems, the time integral is omitted. For vector-valued systems, the inner norm is
taken over solution channels. In implementation, this integral is approximated by the corresponding
grid-weighted discrete norm on each hidden evaluation mesh.
This gives a uniform function-space error across scalar fields, multi-field systems, steady-state
solutions, and time-dependent trajectories. Because the verifier scores the returned field rather than
the code template, it is agnostic to the numerical method used by the generated program.

3.5   RLVP Reward Construction

We instantiate the verifier in three steps: a binary feasibility gate, stochastic-tolerance scores for
continuous diagnostics, and a final multiplicative reward.

Validity. For a generated solver y on hidden instance c, let vexec , vshape , and vfinite indicate whether
the program executes without error, returns the required output shape, and produces finite values.
Invalid programs receive zero reward. The hard validity gate is
                               V (y, c) = vexec (y, c) vshape (y, c) vfinite (y, c).                           (2)

Uncertain tolerances. For valid programs, each nonnegative diagnostic loss Lj (y, c) is treated
as a binary test with an uncertain acceptance tolerance. A fixed threshold would accept when
Lj (y, c) ≤ ϵj , but acceptable error scales vary across PDE families, grids, discretizations, and
diagnostics. We therefore draw ϵj ∼ pTj and define the soft-verification factor as the expected binary
pass outcome:
                   Rj (y, c) = Eϵj ∼pTj [1{Lj (y, c) ≤ ϵj }] = Pϵj ∼pTj (ϵj ≥ Lj (y, c)) .                     (3)
Thus, the continuous reward is still an RLVR-style pass probability, now marginalizing over un-
certainty
         in the tolerance. With an exponential tolerance distribution this becomes Rj (y, c) =
        L (y,c)
exp − jTj       . We provide the derivation, interpretation of the exponential model, and relation to
Gibbs forms in Section C.


                                                        5
Physical accuracy and physics residual factors.        Applying
                                                               Section 3.5 to the function-space error
                                                       u,u⋆ )
                                             
                                                Ltraj (b
from Equation (1) gives Rtraj (y, c) = exp − Ttraj             . We refer to this as the physical accuracy
reward: this factor ranks valid programs by the accuracy of the physical field or trajectory they
produce on the hidden verifier instance. When a residual operator is available, we also include a
physics residual consistency diagnostic. With the time integral omitted for steady-state problems,
define
                                                                          |ρ(bu) − ρ(u⋆ )|
                u) = ∥Rp [b
              ρ(b          u; µ, b]∥L2 ([0,T ]×Ω)       Lphys (bu, u⋆ ) =                  .            (4)
                                                                             ρ(u⋆ ) + ϵ
Comparing to ρ(u⋆ ) absorbs the discretization error of the reference solution and avoids rewarding
residuals smaller than
                    the numerical    reference itself. The corresponding expected-pass factor is
                              u,u⋆ )
                       Lphys (b
Rphys (y, c) = exp − Tphys            . Finally, the complete RLVP reward is

                                     R(y, c) = V (y, c) · Rtraj (y, c) · Rphys (y, c).                                                    (5)
If no residual diagnostic is used, we set Rphys = 1. The residual term also acts as an attenuation factor
rather than an additive auxiliary objective: it penalizes physically inconsistent returned solutions
without introducing reward for surface-level code features.

3.6   RL Post-Training with GRPO

Starting from the SFT-initialized policy, we apply Group-Relative Policy Optimization (GRPO) [20].
For each prompt xi , we sample a group of G candidate programs from the old policy, yi,1 , . . . , yi,G ∼
πθold (· | xi ), execute each program in the PDE environment, and compute verifier rewards Ri,g =
R(yi,g , xi ). Following GRPO, advantages are computed from the raw verifier rewards, without KL
                                                                          R −mean ′ R ′
shaping, by normalizing rewards within each group: Ai,g = i,gstd ′ R g′ +ϵi,g . The same output-
                                                                                g  i,g
level advantage Ai,g is assigned to each valid response token in the generated program yi,g . Let
                 π (y     |xi ,yi,g,<t )
ρi,g,t (θ) = πθ θ (yi,g,t
                      i,g,t |xi ,yi,g,<t )
                                           denote the token-level policy ratio. The clipped GRPO objective is
               old


                                                                                                                                           
                      G          |yi,g |
                   1 X 1 Xn                                                                                                                o
JGRPO (θ) = Ei                          min (ρi,g,t (θ)Ai,g , clip (ρi,g,t (θ), 1 − ϵclip , 1 + ϵclip ) Ai,g ) − βKL DKL [πθ ∥ πref ]i,g,t  .
                   G g=1 |yi,g | t=1
                                                                                                    (6)
where DKL [πθ ∥ πref ]i,g,t is the per-token KL penalty to the frozen SFT reference model πref . In our
implementation, we use the standard low-variance sample-based approximation
                                                                                              πref (yi,g,t | xi , yi,g,<t )
         DKL [πθ ∥ πref ]i,g,t = qi,g,t − log qi,g,t − 1,                         qi,g,t =                                  .             (7)
                                                                                              πθ (yi,g,t | xi , yi,g,<t )
Here πθold is the policy used to sample the current batch, while πref is used only for KL regularization.
The group baseline removes the need for a learned value model, and the verifier rewards shift
probability mass toward programs that satisfy hidden execution checks and produce physically
accurate solutions. Our implementation uses token-mean aggregation over valid response tokens. We
examine the resulting training dynamics: reward trajectories, and nRMSE trends in Section 4.
4     Empirical Evaluation
4.1   Experimental Setup

Training data and prompts. We post-train on eight seen PDE families: 1D advection, 1D Burgers,
1D reaction–diffusion, 1D diffusion–sorption, 2D reaction–diffusion, 2D Darcy flow, 2D incompress-
ible Navier–Stokes, and 2D shallow water. These tasks span hyperbolic transport, parabolic diffusion
and reaction, elliptic solves, and coupled 2D conservation-law dynamics. During RLVP, each prompt
is paired with hidden PDE instances (varied by initial conditions and PDE parameters) sampled from
the training environment, so the policy is optimized against executable function-space accuracy rather
than token imitation alone. Full PDE specifications, parameter grids, boundary and initial conditions,
and solver bank coverage are provided in Appendix B. Hyperparameters and compute details are in
Appendix A.



                                                                     6
Figure 2: Progress of evaluation metrics during post-training. We compare Base (Qwen2.5-Coder-
Instruct), SFT, and RLVP post-trained checkpoints on the eight seen PDE tasks. Dashed line: Claude
Sonnet 4.5 baseline evaluated with the same k = 8 sampling protocol.


Evaluation problems and metrics. We evaluate all models on fixed PDE prompts and case sets.
The seen-PDE evaluation uses the same eight PDE families as training, with 143 total cases. The
unseen PDE evaluation uses 10 held-out PDE prompts and 137 cases: 2D advection, 1D and 2D
advection–diffusion, 1D advection–reaction–diffusion, 2D Allen–Cahn, 1D Cahn–Hilliard, 2D Darcy–
reaction, 2D Gray–Scott, 1D heat, and 1D KdV. These held-out PDEs are not used as SFT solver-bank
targets or as RL prompts. For each checkpoint, the model generates k = 8 solver programs per
PDE prompt, and each program is evaluated on the fixed test cases for that prompt. We report
combinatorial pass@k, valid execution rate, and median best-of-8 nRMSE as the continuous physical
accuracy metric. Detailed validity criteria, metric definitions, evaluator fallbacks, and aggregation
procedures are provided in Appendix D.

4.2   RLVP Improves Numerical PDE Solver Code Generation

We first quantify how the evaluation metrics change after verifier-based post-training on the eight seen
PDE prompts. SFT teaches the solver program prior: function signatures, correct array shapes, han-
dling of PDE-specific parameters and boundary conditions, and common numerical solver templates.
RLVP then sharpens this prior with execution-grounded feedback, reweighting the prior towards
generating solver programs that both execute and solve a broad range of PDE problems with hidden
cases of varying discretizations, time grids, parameters, and initial conditions. As shown in Figure 2,
RLVP improves both single-sample pass@1 reliability and best-of-8 accuracy across the 3B, 7B,
and 14B Qwen2.5-Coder-Instruct models. The corresponding training reward curves are shown in
Figure 7.
Table 1 and Figure 3 summarize the aggregate and per-PDE performance on the seen tasks. Across
all three model scales, RLVP raises pass@1 and pass@8 from near-zero base model performance to
0.63–0.89 and 0.83–0.97 respectively and drives median-best nRMSE@8 to approximately 6 × 10−4 .
The post-trained local models also outperform static frontier model baselines under the same direct-
generation protocol. For example, the Qwen2.5-Coder-Instruct model (7B) post-trained with RLVP
reaches pass@1/pass@8 0.68/0.83 and nRMSE@8 6.13 × 10−4 , compared with 0.24/0.50 and
1.15 × 10−2 for Claude Sonnet 4.5.




Figure 3: Comparison across local and frontier models on seen PDEs. Base, SFT, RLVP, and
frontier LLMs are compared by valid execution rate, pass@1, pass@8, and median best-of-8 nRMSE.

With RLVP, parameter updates from executable physical feedback can make a smaller policy more
likely to generate numerically reliable solver programs than prompting a much larger static model.
Our multi-PDE setup enables all models to solve most PDE tasks simultaneously and robustly after


                                                   7
Table 1: Aggregate and per-PDE evaluation performance. We report aggregate metrics together
with per-PDE pass@1 and median best-of-8 nRMSE. Additional metrics are provided in Appendix
Table 14. Best and second-best values in each row are marked in bold and underline.
                                                               3B                         7B                         14B              Claude Sonnet 4.5   Qwen3-Coder-480B   DeepSeek V4 Flash   GPT-OSS-120B   Llama-3.1-405B   Llama-3.3-70B
Section           Metric                              Base           RLVP        Base           RLVP        Base            RLVP
Aggregate         Pass@1 ↑                            0.00            0.63       0.00            0.68       0.06             0.89           0.24                0.12               0.23              0.21            0.07            0.04
                  Pass@8 ↑                            0.00            0.84       0.00             0.83      0.19             0.97           0.50                0.39               0.47              0.43            0.29            0.19
                  Median-best nRMSE@8 ↓             8.03E-01        6.20E-04   8.46E-01        6.13E-04   4.14E-01         6.20E-04       1.15E-02            3.22E-02           1.17E-02          1.22E-02        1.67E-01        7.99E-01
                  Valid exec rate ↑                   0.06            0.69       0.17            0.80       0.32             0.92           0.81                0.50               0.74              0.58            0.27            0.21
Per-PDE Pass@1    Advection 1D                        0.00            1.00       0.00            0.88       0.04             0.75           0.14                0.43               0.38              0.38            0.00            0.00
                  Burgers 1D                          0.00            0.69       0.00            0.75       0.00             0.75           0.25                0.08               0.12              0.12            0.12            0.00
                  Darcy Flow 2D                       0.00            0.75       0.00            0.67       0.00             1.00           0.00                0.00               0.00              0.00            0.00            0.00
                  Diffusion-sorption 1D               0.00            0.88       0.00            0.88       0.03             1.00           0.00                0.00               0.00              0.00            0.00            0.03
                  Incompressible Navier Stokes 2D     0.00            0.00       0.00            0.00       0.00             0.62           0.04                0.00               0.00              0.12            0.00            0.00
                  Reaction Diffusion 1D               0.00            0.88       0.00            1.00       0.41             1.00           0.59                0.17               0.87              0.00            0.25            0.25
                  Reaction Diffusion 2D               0.00            0.75       0.00            0.88       0.00             1.00           0.50                0.25               0.25              0.92            0.15            0.04
                  Shallow Water 2D                    0.00            0.12       0.00            0.38       0.00             1.00           0.38                0.00               0.21              0.12            0.00            0.00
Per-PDE nRMSE@8   Advection 1D                      6.05E-01        9.44E-04   2.51E-01        9.29E-04   2.86E-02     9.44E-04           1.34E-02            1.33E-02           1.32E-02          1.34E-02       3.27E-01         1.00E+00
                  Burgers 1D                        1.00E+00        3.03E-03   1.00E+00        3.02E-03   2.29E-01     3.03E-03           1.78E-03            4.64E-03           1.51E-03          1.10E-02       4.03E-02         1.00E+00
                  Darcy Flow 2D                     1.00E+00        3.85E-15   1.00E+00        3.85E-15   5.98E-01     0.00E+00           1.08E-01            4.86E-01           3.56E-02          1.08E-01       2.79E-01         5.98E-01
                  Diffusion-sorption 1D             1.00E+00        2.97E-04   3.26E-01        2.96E-04   3.56E-02     2.97E-04           5.35E-02            3.04E-01           5.07E-02          5.35E-02       1.00E+00         3.56E-02
                  Incompressible Navier Stokes 2D   1.00E+00        1.00E+00   1.00E+00        3.33E-01   1.00E+00     3.48E-03           1.67E-02            1.01E-01           2.78E-02          6.45E-03       1.00E+00         1.00E+00
                  Reaction Diffusion 1D             2.98E-01        3.71E-06   6.92E-01        3.71E-06   3.18E-04     9.73E-08           1.61E-05            4.52E-05           3.71E-06          1.00E+00       3.70E-06         3.70E-06
                  Reaction Diffusion 2D             1.60E-01        1.11E-05   1.51E-01        1.11E-05   1.00E+00     8.44E-06           4.67E-03            3.90E-03           4.03E-03          3.90E-03       8.89E-03         4.86E-02
                  Shallow Water 2D                  5.11E-02        1.23E-03   1.00E+00        1.23E-03   1.00E+00     1.14E-03           9.56E-03            5.11E-02           1.02E-02          1.02E-02       5.53E-02         1.00E+00




RLVP. Incompressible Navier–Stokes remains the hardest PDE task as it requires coupled velocity
evolution and projection-like structure. The 14B RLVP checkpoint is the only local model with strong
Navier–Stokes solver generation (Table 1), reaching pass@1 0.62 and nRMSE@8 3.48 × 10−3 ,
suggesting that this PDE benefits from a larger model capacity.
4.3         Compositional Transfer to Unseen PDE Families

We next evaluate whether the learned prior transfers beyond the PDE families used for SFT and RL.
The 10 held-out tasks cover diffusion, 2D advection, advection–reaction–diffusion, Cahn–Hilliard,
Gray–Scott, and Korteweg–De Vries (KdV) equations. This setting should be interpreted as a test
of selective numerical-methods transfer, rather than as evidence that the model can solve arbitrary
unseen PDEs.




Figure 4: Evaluation on 10 held-out PDE tasks. We compare Base, SFT, and RLVP checkpoints on
unseen PDE prompts not used during SFT or RL training.


Figure 4 reports aggregate performance on the unseen PDE problems. Although these PDEs are
absent from both the SFT solver bank and the RL prompt distribution, RLVP improves pass@1
relative to the base and SFT checkpoints across model sizes. For example in the 7B model, pass@8
increases from 0.28 after SFT to 0.57 after RLVP, while median-best nRMSE@8 decreases from
1.45 × 10−1 to 4.01 × 10−3 . Since the held-out prompts were not training objectives, these results are
best viewed as evidence that RLVP increases the probability of the LLM discovering reusable solver
structure on related PDEs. Aggregate metrics and per-PDE breakdowns are provided in Appendix
Tables 15 and 16.
The per-PDE breakdown in Appendix Table 16 shows that the 7B improvement is not driven by a
single held-out equation. RLVP is strongest on heat, 2D advection, advection–reaction–diffusion,
and Cahn–Hilliard. For 7B, advection–reaction–diffusion improves from SFT pass@8 0.00 to
RLVP pass@8 1.00, with nRMSE@8 dropping from 5.25 × 10−1 to 1.50 × 10−3 . Heat similarly
improves from SFT pass@8 0.00 to RLVP pass@8 1.00, with nRMSE@8 8.11 × 10−5 . In contrast,
advection–diffusion, Darcy–reaction, and KdV equations remain difficult, indicating that transfer
is selective and depends on the numerical structures available in the trained policy. We examine
advection–reaction–diffusion below as a representative case of compositional numerical methods
transfer.




                                                                                                                             8
      Reference
                                                                                       Slope-limited


      Base
                                                                                       reconstruction


                                                                                       Linear
                                                                                       advection flux

                                                                                       Advection,
      SFT




                                                                                       diffusion, and
                                                                                       logistic reaction



                                                                                       CFL substeps
                                                                                       and SSPRK3
      RLVP




Figure 5: Compositional transfer to unseen advection–reaction–diffusion (ARD) (RLVP 7B
model). Left: reference and best-of-8 generated solutions for the held-out ARD problem with β = 1,
ν = 0.02, and ρ = 2. Right: numerical scheme evidences from generated PDE solver snippets: a
Burgers solver from RLVP, and ARD solvers from SFT and RLVP post-trained models.


Evidence of compositional numerical methods transfer. Figure 5 examines advection–reaction–
diffusion (ARD), a held-out PDE that combines linear advection, diffusion, and logistic reaction. The
base model generates an almost trivial solution and the SFT model gives a qualitatively incorrect
trajectory. The RLVP post-trained model generates a solver which gives a solution that closely
matches the reference. The code comparison suggests that the generated solver from RLVP uses
a finite-volume/stencil motif learned on the seen transport PDEs (such as the generated solver for
Burgers’ equation), but adapts it to the new operator composition by combining advection, reaction,
and diffusion terms. Rather than directly copying an SFT template, the post-trained model appears to
exhibit scheme-level compositional reuse.
Additional results on unseen PDE tasks are shown in Appendix F. The heat equation example illus-
trates a diffusion-only subset of the seen reaction–diffusion family, with median nRMSE improving
from 2.07 × 10−1 (SFT) to 8.11 × 10−5 . The unseen 2D advection task shows dimensional lifting
from seen 1D advection, extending the transport update to two spatial dimensions with CFL control
and RK4 integration. Cahn–Hilliard illustrates higher-order operator synthesis by constructing the
chemical potential and applying a second Laplacian. Together with the aggregate held-out results,
these examples suggest that an LLM post-trained with RLVP can reuse and adapt numerical solver
motifs on unseen PDE tasks, while such transfer is selective rather than universal.
Solver components analysis gives a complementary view of the learned distributions: RLVP post-
trained checkpoints more often emit np.roll-based stencils, CFL/substep control, and RK time-
stepping schemes, consistent with a reusable and robust methods-of-lines pattern (Figure 11).

4.4     Physical Accuracy Improves Beyond Validity

Appendix Figures 8 and 9 isolate the effect of adding the continuous physical accuracy reward Rtraj ,
computed from function-space nRMSE, to validity-only RL for the 7B model (comparing R = V
against R = V Rtraj ). On seen PDEs, validity-only RL is worse on pass@1 (0.58 vs. 0.71), pass@8
(0.76 vs. 0.84), and median best-of-8 nRMSE (1.0 × 10−3 vs. 6.2 × 10−4 ). On unseen PDEs, adding
function-space accuracy improves valid execution (0.45 vs. 0.29), pass@1 (0.10 vs. 0.03), pass@8
(0.33 vs. 0.21), and nRMSE@8 (1.3 × 10−1 vs. 1.8 × 10−1 ). These results indicate that binary
reward (validity) alone can reward program executability, but does not provide enough information to
refine physical solution quality; the dense physical-accuracy term is needed to refine solver quality
and support numerical methods transfer, consistent with the verifier design in Section 3.5.
5     Conclusion
We have shown that adapting language models with execution-grounded RL can substantially improve
PDE solver generation. Starting from a solver-bank SFT warm start, RLVP uses a verifiable physics
reward to move beyond executability and optimize for physical accuracy and residual consistency.
Across model sizes, this post-training improves one-shot reliability, pass@k, and best-of-k numerical
accuracy, and under the same direct-generation protocol allows smaller verifier-trained models to


                                                 9
match or exceed much larger static prompting baselines. We also find evidence of selective cross-
family transfer: the trained policy reuses numerical motifs such as CFL substepping, finite-difference
stencils, boundary handling, and stability safeguards on PDEs absent from training.
These findings suggest that future solver-writing LLMs should place more emphasis on adapting
model parameters with verifiable physical feedback, rather than relying only on larger static models or
inference-time scaffolding. Our study covers eight structured PDE families, leaving broader scientific
settings such as complex geometries, richer boundary conditions, adaptive meshes, stochastic PDEs,
and multiphysics systems to future work. Further efforts can combine RLVP with retrieval, debugging
loops, verifier-guided search, or test-time scaling, instead of direct-generation protocol. Nevertheless,
this work is the first to show what post-training can achieve for multi-PDE solver generation even
with compact models and limited compute. We expect the approach to strengthen with broader PDE
coverage, richer solver banks, stronger base models, and extensions to other scientific code-generation
settings such as inverse problems, PDE-constrained optimization, finite-element simulation, and
molecular dynamics.

Acknowledgments
P.C. is supported by the Regenerative Energy-Efficient Manufacturing of Thermoset Polymeric
Materials (REMAT) Energy Frontier Research Center, funded by the U.S. Department of Energy,
Office of Science, Basic Energy Sciences under award DE-SC0023457. This research used resources
of the National Energy Research Scientific Computing Center (NERSC), a U.S. Department of Energy
Office of Science User Facility, using NERSC award ALCC-ERCAP 0038200. We would like to
thank Branden Morioka and Florencia Ojeda for early efforts.
This material is based upon work supported by the U.S. National Science Foundation under award
Nos CNS-2346520, RISE-2425761, and DMS-2325184, by the Defense Advanced Research Projects
Agency (DARPA) under Agreement No. HR00112490488, by the Department of Energy, National
Nuclear Security Administration under Award Number DE-NA0004266 and by the United States Air
Force Research Laboratory under Cooperative Agreement Number FA8750-19-2-1000. Neither the
United States Government nor any agency thereof, nor any of their employees, makes any warranty,
express or implied, or assumes any legal liability or responsibility for the accuracy, completeness,
or usefulness of any information, apparatus, product, or process disclosed, or represents that its use
would not infringe privately owned rights. Reference herein to any specific commercial product,
process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United States Government
or any agency thereof. The views and opinions of authors expressed herein do not necessarily state or
reflect those of the United States Government or any agency thereof.




                                                   10
References
 [1] Lawrence C Evans. Partial Differential Equations. American Mathematical Society, 2 edition,
     2010.
 [2] Randall J LeVeque. Finite volume methods for hyperbolic problems, volume 31. Cambridge
     university press, 2002.
 [3] Alfio Quarteroni and Alberto Valli. Numerical approximation of partial differential equations.
     Springer, 1994.
 [4] Lloyd N Trefethen. Spectral methods in MATLAB. SIAM, 2000.
 [5] Uri M Ascher and Linda R Petzold. Computer methods for ordinary differential equations and
     differential-algebraic equations. SIAM, 1998.
 [6] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared
     Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large
     language models trained on code. arXiv preprint arXiv:2107.03374, 2021.
 [7] Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan Guo,
     Collin Burns, Samir Puranik, Horace He, Dawn Song, et al. Measuring coding challenge
     competence with apps. arXiv preprint arXiv:2105.09938, 2021.
 [8] Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David
     Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, et al. Program synthesis with large
     language models. arXiv preprint arXiv:2108.07732, 2021.
 [9] Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven Chu Hong Hoi.
     Coderl: Mastering code generation through pretrained models and deep reinforcement learning.
     Advances in Neural Information Processing Systems, 35:21314–21328, 2022.
[10] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R. Narasimhan, and
     Yuan Cao. ReAct: Synergizing reasoning and acting in language models. In The Eleventh
     International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5,
     2023. OpenReview.net, 2023. URL https://openreview.net/forum?id=WE_vluYUL-X.
[11] Jonas Gehring, Kunhao Zheng, Jade Copet, Vegard Mella, Quentin Carbonneaux, Taco Cohen,
     and Gabriel Synnaeve. Rlef: Grounding code llms in execution feedback with reinforcement
     learning. arXiv preprint arXiv:2410.02089, 2024.
[12] Shanda Li, Tanya Marwah, Junhong Shen, Weiwei Sun, Andrej Risteski, Yiming Yang, and
     Ameet Talwalkar. Codepde: An inference framework for llm-driven PDE solver generation.
     Trans. Mach. Learn. Res., 2026. URL https://openreview.net/forum?id=eG3Qy5Oux6.
[13] Saarth Gaonkar, Xiang Zheng, Haocheng Xi, Rishabh Tiwari, Kurt Keutzer, Dmitriy Morozov,
     Michael W Mahoney, and Amir Gholami. Sciml agents: Write the solver, not the solution.
     arXiv preprint arXiv:2509.09936, 2025.
[14] Jianda Du, Youran Sun, and Haizhao Yang. Autonumerics: An autonomous, pde-agnostic
     multi-agent pipeline for scientific computing. arXiv preprint arXiv:2602.17607, 2026.
[15] Rushikesh Deotale, Adithya Srinivasan, Mahmoud Golestanian, Yuan Tian, Tianyi Zhang,
     Pavlos Vlachos, and Hector Gomez. All-fem: Agentic large language models fine-tuned for
     finite element methods. Computer Methods in Applied Mechanics and Engineering, 457:118985,
     2026.
[16] Jianming Liu, Ren Zhu, Jian Xu, Kun Ding, Xu-Yao Zhang, Gaofeng Meng, and Cheng-Lin
     Liu. Pde-agent: A toolchain-augmented multi-agent framework for pde solving. arXiv preprint
     arXiv:2512.16214, 2025.
[17] Qingpo Wuwu, Chonghan Gao, Tianyu Chen, Yihang Huang, Yuekai Zhang, Jianing Wang,
     Jianxin Li, Haoyi Zhou, and Shanghang Zhang. Pinnsagent: Automated pde surrogation with
     large language models. arXiv preprint arXiv:2501.12053, 2025.


                                               11
[18] Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling llm test-time compute opti-
     mally can be more effective than scaling model parameters. arXiv preprint arXiv:2408.03314,
     2024.
[19] Yangzhen Wu, Zhiqing Sun, Shanda Li, Sean Welleck, and Yiming Yang. Inference scaling
     laws: An empirical analysis of compute-optimal inference for problem-solving with language
     models. arXiv preprint arXiv:2408.00724, 2024.
[20] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
     Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. DeepSeekMath: Pushing the limits of
     mathematical reasoning in open language models, 2024. URL https://arxiv.org/abs/
     2402.03300.
[21] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu,
     Ruoyu Zhang, Shirong Ma, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin
     Gou, Zhihong Shao, Zhuoshu Li, Ziyi Gao, Aixin Liu, Bing Xue, Bingxuan Wang, Bochao Wu,
     Bei Feng, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chong Ruan, Damai Dai, Deli Chen,
     Dongjie Ji, Erhang Li, Fangyun Lin, Fucong Dai, Fuli Luo, Guangbo Hao, Guanting Chen,
     Guowei Li, H. Zhang, Hanwei Xu, Honghui Ding, Huazuo Gao, Hui Qu, Hui Li, Jianzhong
     Guo, Jiashi Li, Jingchang Chen, Jingyang Yuan, Jinhao Tu, Junjie Qiu, Junlong Li, J. L. Cai,
     Jiaqi Ni, Jian Liang, Jin Chen, Kai Dong, Kai Hu, Kaichao You, Kaige Gao, Kang Guan,
     Kexin Huang, Kuai Yu, Lean Wang, Lecong Zhang, Liang Zhao, Litong Wang, Liyue Zhang,
     Lei Xu, Leyi Xia, Mingchuan Zhang, Minghua Zhang, Minghui Tang, Mingxu Zhou, Meng
     Li, Miaojun Wang, Mingming Li, Ning Tian, Panpan Huang, Peng Zhang, Qiancheng Wang,
     Qinyu Chen, Qiushi Du, Ruiqi Ge, Ruisong Zhang, Ruizhe Pan, Runji Wang, R. J. Chen,
     R. L. Jin, Ruyi Chen, Shanghao Lu, Shangyan Zhou, Shanhuang Chen, Shengfeng Ye, Shiyu
     Wang, Shuiping Yu, Shunfeng Zhou, Shuting Pan, S. S. Li, Shuang Zhou, Shaoqing Wu, Tao
     Yun, Tian Pei, Tianyu Sun, T. Wang, Wangding Zeng, Wen Liu, Wenfeng Liang, Wenjun Gao,
     Wenqin Yu, Wentao Zhang, W. L. Xiao, Wei An, Xiaodong Liu, Xiaohan Wang, Xiaokang
     Chen, Xiaotao Nie, Xin Cheng, Xin Liu, Xin Xie, Xingchao Liu, Xinyu Yang, Xinyuan Li,
     Xuecheng Su, Xuheng Lin, X. Q. Li, Xiangyue Jin, Xiaojin Shen, Xiaosha Chen, Xiaowen
     Sun, Xiaoxiang Wang, Xinnan Song, Xinyi Zhou, Xianzu Wang, Xinxia Shan, Y. K. Li, Y. Q.
     Wang, Y. X. Wei, Yang Zhang, Yanhong Xu, Yao Li, Yao Zhao, Yaofeng Sun, Yaohui Wang,
     Yi Yu, Yichao Zhang, Yifan Shi, Yiliang Xiong, Ying He, Yishi Piao, Yisong Wang, Yixuan
     Tan, Yiyang Ma, Yiyuan Liu, Yongqiang Guo, Yuan Ou, Yuduan Wang, Yue Gong, Yuheng
     Zou, Yujia He, Yunfan Xiong, Yuxiang Luo, Yuxiang You, Yuxuan Liu, Yuyang Zhou, Y. X.
     Zhu, Yanping Huang, Yaohui Li, Yi Zheng, Yuchen Zhu, Yunxian Ma, Ying Tang, Yukun Zha,
     Yuting Yan, Z. Z. Ren, Zehui Ren, Zhangli Sha, Zhe Fu, Zhean Xu, Zhenda Xie, Zhengyan
     Zhang, Zhewen Hao, Zhicheng Ma, Zhigang Yan, Zhiyu Wu, Zihui Gu, Zijia Zhu, Zijun Liu,
     Zilin Li, Ziwei Xie, Ziyang Song, Zizheng Pan, Zhen Huang, Zhipeng Xu, Zhongyu Zhang,
     and Zhen Zhang. Deepseek-r1 incentivizes reasoning in llms through reinforcement learning.
     Nature, 645(8081):633–638, 2025. ISSN 1476-4687. doi: 10.1038/s41586-025-09422-z. URL
     http://dx.doi.org/10.1038/s41586-025-09422-z.
[22] Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang,
     Antonia Creswell, Geoffrey Irving, and Irina Higgins. Solving math word problems with
     process- and outcome-based feedback, 2022. URL https://arxiv.org/abs/2211.14275.
[23] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu,
     Joseph Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language
     model serving with pagedattention. In Proceedings of the 29th symposium on operating systems
     principles, pages 611–626, 2023.
[24] Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua
     Peng, Haibin Lin, and Chuan Wu. Hybridflow: A flexible and efficient rlhf framework. In
     Proceedings of the Twentieth European Conference on Computer Systems, pages 1279–1297,
     2025.
[25] Minyang Tian, Luyu Gao, Shizhuo Dylan Zhang, Xinan Chen, Cunwei Fan, Xuefei Guo, Roland
     Haas, Pan Ji, Kittithat Krongchon, Yao Li, Shengyan Liu, Di Luo, Yutao Ma, Hao Tong, Kha
     Trinh, Chenyu Tian, Zihan Wang, Bohao Wu, Yanyu Xiong, Shengzhu Yin, Minhui Zhu, Kilian


                                               12
     Lieret, Yanxin Lu, Genglin Liu, Yufeng Du, Tianhua Tao, Ofir Press, Jamie Callan, Eliu A.
     Huerta, and Hao Peng. SciCode: A research coding benchmark curated by scientists. 37:
     30624–30650, 2024. doi: 10.52202/079017-0963.
[26] Ling Yue, Nithin Somasekharan, Tingwen Zhang, Yadi Cao, Zhangze Chen, Shimin Di, and
     Shaowu Pan. Foam-agent: Towards automated intelligent cfd workflows. arXiv preprint
     arXiv:2505.04997, 2025.
[27] Sandeep Pandey, Ran Xu, Wenkang Wang, and Xu Chu. Openfoamgpt: A retrieval-augmented
     large language model (llm) agent for openfoam-based computational fluid dynamics. Physics of
     Fluids, 37(3), 2025.
[28] Yuxuan Chen, Xu Zhu, Hua Zhou, and Zhuyin Ren. Metaopenfoam: an llm-based multi-agent
     framework for cfd. arXiv preprint arXiv:2407.21320, 2024.
[29] Tao Zhang, Zhenhai Liu, Yong Xin, and Yongjun Jiao. Mooseagent: A llm based multi-agent
     framework for automating moose simulation, 2025. URL https://arxiv.org/abs/2504.
     08621.
[30] Jingquan Wang, Andrew Negrut, Harry Zhang, Khailanii Slaton, Shu Wang, Radu Serban,
     Jinlong Wu, and Dan Negrut. Chronollm: customizing language models for physics-based
     simulation code generation. Multibody System Dynamics, Feb 2026. ISSN 1573-272X. doi:
     10.1007/s11044-026-10152-x.
[31] Xin He, Liangliang You, Hongduan Tian, Bo Han, Ivor Tsang, and Yew-Soon Ong. Lang-
     pinn: From language to physics-informed neural networks via a multi-agent framework. arXiv
     preprint arXiv:2510.05158, 2025.
[32] Nayantara Mudur, Hao Cui, Subhashini Venugopalan, Paul Raccuglia, Michael P Brenner, and
     Peter Norgaard. Feabench: Evaluating language models on multiphysics reasoning ability.
     arXiv preprint arXiv:2504.06260, 2025.
[33] Mihir Prabhudesai, Aryan Satpathy, Yangmin Li, Zheyang Qin, Nikash Bhardwaj, Amir Zadeh,
     Chuan Li, Katerina Fragkiadaki, and Deepak Pathak. Solving physics olympiad via reinforce-
     ment learning on physics simulators. arXiv preprint arXiv:2604.11805, 2026.
[34] Mauricio Soroco, Jialin Song, Mengzhou Xia, Kye Emond, Weiran Sun, and Wuyang Chen. Pde-
     controller: Llms for autoformalization and reasoning of pdes. arXiv preprint arXiv:2502.00963,
     2025.
[35] Knut-Andreas Lie, Olav Møyner, Elling Svee, and Jakob Torben. Agentic scientific simulation:
     Execution-grounded model construction and reconstruction. arXiv preprint arXiv:2603.00214,
     2026.
[36] Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, YuYue, Weinan Dai,
     Tiantian Fan, Gaohong Liu, Juncai Liu, LingJun Liu, Xin Liu, Haibin Lin, Zhiqi Lin, Bole
     Ma, Guangming Sheng, Yuxuan Tong, Chi Zhang, Mofan Zhang, Ru Zhang, Wang Zhang,
     Hang Zhu, Jinhua Zhu, Jiaze Chen, Jiangjie Chen, Chengyi Wang, Hongli Yu, Yuxuan Song,
     Xiangpeng Wei, Hao Zhou, Jingjing Liu, Wei-Ying Ma, Ya-Qin Zhang, Lin Yan, Yonghui Wu,
     and Mingxuan Wang. DAPO: An open-source LLM reinforcement learning system at scale. In
     The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025. URL
     https://openreview.net/forum?id=2a36EMSSTp.
[37] Chujie Zheng, Shixuan Liu, Mingze Li, Xiong-Hui Chen, Bowen Yu, Chang Gao, Kai Dang,
     Yuqiong Liu, Rui Men, An Yang, Jingren Zhou, and Junyang Lin. Group sequence policy
     optimization, 2025. URL https://arxiv.org/abs/2507.18071.
[38] Shihan Dou, Yan Liu, Haoxiang Jia, Enyu Zhou, Limao Xiong, Junjie Shan, Caishuang Huang,
     Xiao Wang, Xiaoran Fan, Zhiheng Xi, et al. Stepcoder: improving code generation with
     reinforcement learning from compiler feedback. In Proceedings of the 62nd Annual Meeting
     of the Association for Computational Linguistics (Volume 1: Long Papers), pages 4571–4585,
     2024.



                                                13
[39] Sherry Yang, Joy He-Yueya, and Percy Liang. Reinforcement learning for machine learning
     engineering agents, 2025. URL https://arxiv.org/abs/2509.01684.
[40] Mehul Damani, Isha Puri, Stewart Slocum, Idan Shenfeld, Leshem Choshen, Yoon Kim, and
     Jacob Andreas. Beyond binary rewards: Training lms to reason about their uncertainty. arXiv
     preprint arXiv:2507.16806, 2025.
[41] Maziar Raissi, Paris Perdikaris, and George E Karniadakis. Physics-informed neural networks:
     A deep learning framework for solving forward and inverse problems involving nonlinear partial
     differential equations. Journal of Computational physics, 378:686–707, 2019.
[42] Zongyi Li, Nikola Kovachki, Kamyar Azizzadenesheli, Burigede Liu, Kaushik Bhattacharya,
     Andrew Stuart, and Anima Anandkumar. Fourier neural operator for parametric partial differen-
     tial equations. arXiv preprint arXiv:2010.08895, 2020.
[43] Lu Lu, Pengzhan Jin, Guofei Pang, Zhongqiang Zhang, and George Em Karniadakis. Learning
     nonlinear operators via deeponet based on the universal approximation theorem of operators.
     Nature machine intelligence, 3(3):218–229, 2021.
[44] Pengfei Cai, Sulin Liu, Qibang Liu, Philippe Geubelle, and Rafael Gomez-Bombarelli. Towards
     long rollout of neural operators with local attention and flow matching-inspired correction: An
     example in frontal polymerization pdes. NeurIPS 2024 Workshop on Machine Learning and the
     Physical Sciences, 2024. URL https://neurips.cc/virtual/2024/100099.
[45] Makoto Takamoto, Timothy Praditia, Raphael Leiteritz, Daniel MacKinlay, Francesco Alesiani,
     Dirk Pflüger, and Mathias Niepert. Pdebench: An extensive benchmark for scientific machine
     learning. Advances in neural information processing systems, 35:1596–1611, 2022.
[46] Jiahe Huang, Guandao Yang, Zichen Wang, and Jeong Joon Park. Diffusionpde: Generative
     pde-solving under partial observation. Advances in Neural Information Processing Systems, 37:
     130291–130323, 2024.
[47] Jan-Hendrik Bastek, WaiChing Sun, and Dennis M. Kochmann. Physics-informed diffusion
     models, 2024. URL https://arxiv.org/abs/2403.14404.
[48] Utkarsh Utkarsh, Pengfei Cai, Alan Edelman, Rafael Gomez-Bombarelli, and Christopher Vin-
     cent Rackauckas. Physics-constrained flow matching: Sampling generative models with hard
     constraints. arXiv preprint arXiv:2506.04171, 2025.
[49] Utkarsh Utkarsh, Danielle C Maddix, Ruijun Ma, Michael W Mahoney, and Yuyang Wang.
     End-to-end probabilistic framework for learning with hard constraints. arXiv preprint
     arXiv:2506.07003, 2025.
[50] Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin,
     Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton,
     Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano,
     Jan Leike, and Ryan Lowe. Training language models to follow instructions with human
     feedback, 2022. URL https://arxiv.org/abs/2203.02155.
[51] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun
     Zhang, Bowen Yu, Keming Lu, Kai Dang, Yang Fan, Yichang Zhang, An Yang, Rui Men,
     Fei Huang, Bo Zheng, Yibo Miao, Shanghaoran Quan, Yunlong Feng, Xingzhang Ren, Xu-
     ancheng Ren, Jingren Zhou, and Junyang Lin. Qwen2.5-Coder technical report. arXiv preprint
     arXiv:2409.12186, 2024. URL https://arxiv.org/abs/2409.12186.
[52] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang,
     Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. 2021.
     URL https://arxiv.org/abs/2106.09685.
[53] Dwight Barkley. A model for fast computer simulation of waves in excitable media. Physica D:
     Nonlinear Phenomena, 49(1-2):61–70, 1991.




                                                14
[54] Sergei K Godunov and Ihor Bohachevsky. Finite difference method for numerical computation
     of discontinuous solutions of the equations of fluid dynamics. Matematičeskij sbornik, 47(3):
     271–306, 1959.
[55] Bram Van Leer. Towards the ultimate conservative difference scheme. v. a second-order sequel
     to godunov’s method. Journal of computational Physics, 32(1):101–136, 1979.
[56] Alexander Kurganov and Eitan Tadmor. New high-resolution central schemes for nonlinear
     conservation laws and convection–diffusion equations. Journal of computational physics, 160
     (1):241–282, 2000.
[57] Eleuterio F. Toro. Riemann Solvers and Numerical Methods for Fluid Dynamics. Springer
     Berlin, Heidelberg, 3 edition, 2009. ISBN 978-3-540-25202-3. doi: 10.1007/b79761.
[58] Sigal Gottlieb, Chi-Wang Shu, and Eitan Tadmor. Strong stability-preserving high-order time
     discretization methods. SIAM review, 43(1):89–112, 2001.
[59] Gilbert Strang. On the construction and comparison of difference schemes. SIAM journal on
     numerical analysis, 5(3):506–517, 1968.
[60] Uri M Ascher, Steven J Ruuth, and Raymond J Spiteri. Implicit-explicit runge-kutta methods
     for time-dependent partial differential equations. Applied Numerical Mathematics, 25(2-3):
     151–167, 1997.
[61] Aly-Khan Kassam and Lloyd N Trefethen. Fourth-order time-stepping for stiff pdes. SIAM
     Journal on Scientific Computing, 26(4):1214–1233, 2005.
[62] Alexandre Joel Chorin. The numerical solution of the Navier–Stokes equations for an incom-
     pressible fluid. Bulletin of the American Mathematical Society, 73(6):928–931, 1967. doi:
     10.1090/S0002-9904-1967-11853-6.
[63] Gilbert Strang. Introduction to Applied Mathematics. Wellesley-Cambridge Press, 1986.
[64] Pauli Virtanen, Ralf Gommers, Travis E Oliphant, Matt Haberland, Tyler Reddy, David Courna-
     peau, Evgeni Burovski, Pearu Peterson, Warren Weckesser, Jonathan Bright, et al. Scipy 1.0:
     fundamental algorithms for scientific computing in python. Nature methods, 17(3):261–272,
     2020.
[65] Steven A Orszag. On the elimination of aliasing in finite-difference schemes by filtering
     high-wavenumber components. Journal of Atmospheric Sciences, 28(6):1074–1074, 1971.
[66] Andrew Staniforth and Jean Côté. Semi-lagrangian integration schemes for atmospheric
     models—a review. Monthly weather review, 119(9):2206–2223, 1991.
[67] Randall J LeVeque. Finite difference methods for ordinary and partial differential equations:
     steady-state and time-dependent problems. SIAM, 2007.
[68] Vladimir Vasil’evich Rusanov. The calculation of the interaction of non-stationary shock waves
     and obstacles. USSR Computational Mathematics and Mathematical Physics, 1(2):304–320,
     1962.
[69] Peter Lax and Burton Wendroff. Systems of conservation laws. Communications on Pure and
     Applied Mathematics, 13:217–237, 1960. doi: 10.1002/cpa.3160130205.
[70] Robert W MacCormack. The effect of viscosity in hypervelocity impact cratering. Journal of
     spacecraft and rockets, 40(5):757–763, 2003.
[71] Willem H Hundsdorfer, Jan G Verwer, and WH Hundsdorfer. Numerical solution of time-
     dependent advection-diffusion-reaction equations, volume 33. Springer, 2003.
[72] Robert Eymard, Thierry Gallouët, and Raphaèle Herbin. Finite volume methods. Handbook of
     numerical analysis, 7:713–1018, 2000.
[73] Magnus R Hestenes, Eduard Stiefel, et al. Methods of conjugate gradients for solving linear
     systems. Journal of research of the National Bureau of Standards, 49(6):409–436, 1952.


                                                15
[74] Yousef Saad. Iterative methods for sparse linear systems. SIAM, 2003.
[75] Joel H Ferziger, Milovan Perić, and Robert L Street. Computational methods for fluid dynamics.
     Springer, 4 edition, 2020. doi: 10.1007/978-3-319-99693-6.
[76] Philip L Roe. Approximate riemann solvers, parameter vectors, and difference schemes. Journal
     of computational physics, 43(2):357–372, 1981.
[77] Edwin T Jaynes. Information theory and statistical mechanics. Physical review, 106(4):620,
     1957.
[78] Sheldon M Ross. Introduction to Probability Models. Academic Press, 11 edition, 2014.
[79] Nicholas Metropolis, Arianna W Rosenbluth, Marshall N Rosenbluth, Augusta H Teller, and
     Edward Teller. Equation of state calculations by fast computing machines. The journal of
     chemical physics, 21(6):1087–1092, 1953.
[80] Brian D. Ziebart, Andrew Maas, J. Andrew Bagnell, and Anind K. Dey. Maximum entropy
     inverse reinforcement learning. In Proceedings of the AAAI Conference on Artificial Intelligence,
     pages 1433–1438, 2008.
[81] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-
     policy maximum entropy deep reinforcement learning with a stochastic actor. In International
     conference on machine learning, pages 1861–1870. Pmlr, 2018.




                                                 16
          Table 2: Hyperparameters for the 3B, 7B, and 14B model RLVP post-training runs.
Hyperparameter                              3B                          7B                          14B
model                                       Qwen2.5-Coder-3B-Instruct   Qwen2.5-Coder-7B-Instruct   Qwen2.5-Coder-14B-Instruct
active_pdes                                 8                           8                           8
max_prompt_length                           1024                        1024                        1024
max_response_length                         3072                        3072                        3072
train_batch_size                            48                          48                          48
total_epochs                                50                          50                          50
train_rows                                  512                         512                         512
val_rows                                    64                          64                          64
test_rows                                   128                         128                         128
nnodes                                      1                           1                           1
n_gpus_per_node                             8                           8                           8
sft_num_examples                            2048                        2048                        2048
sft_max_len                                 4096                        4096                        4096
sft_batch_size                              16                          16                          16
sft_epochs                                  1                           1                           1
sft_lr                                      2 × 10−5                    2 × 10−5                    2 × 10−5
sft_lora_rank                               32                          32                          32
sft_lora_alpha                              32                          32                          32
grpo_lora_rank                              32                          32                          32
grpo_lora_alpha                             32                          32                          32
actor_lr                                    2 × 10−6                    2 × 10−6                    2 × 10−6
actor_ppo_mini_batch_size                   16                          16                          16
actor_ppo_micro_batch_size_per_gpu          4                           4                           4
kl_loss_coef                                0.001                       0.001                       0.001
rollout_n                                   8                           8                           8
rollout_temperature                         0.7                         0.7                         0.7
rollout_top_p                               1.0                         1.0                         1.0
rollout_tensor_parallel_size                1                           1                           1
rollout_max_model_len                       4096                        4096                        4096
rollout_max_num_batched_tokens              49152                       49152                       32768
rollout_max_num_seqs                        128                         128                         96
vllm_gpu_memory_utilization                 0.8                         0.8                         0.75
rollout_log_prob_micro_batch_size_per_gpu   8                           8                           4
ref_log_prob_micro_batch_size_per_gpu       8                           8                           4
reward_num_workers                          16                          16                          16
success_nrmse_threshold                     0.01                        0.01                        0.01
passk_k_values                              1, 4, 8                     1, 4, 8                     1, 4, 8
passk_temperature                           0.7                         0.7                         0.7
passk_top_p                                 1.0                         1.0                         1.0
passk_max_new_tokens                        3072                        3072                        3072
passk_sample_seed                           2026                        2026                        2026




A     Experimental Details
Table 2 reports the hyperparameters used in post-training across model sizes.

A.1    Training Configuration

Training proceeds in two stages on the same Qwen2.5-Coder-Instruct backbone [51]: an SFT warm-
start of one epoch over 2048 teacher examples of solver code with LoRA rank 32 [52], followed by
GRPO [20] implemented via verl [24] on 512 training problem instances for 50 epochs with rank-32
LoRA. GRPO uses 8 rollouts per prompt, a fixed KL coefficient of 10−3 to a frozen reference policy
(i.e. SFT model), learning rate of 2 × 10−6 , and PPO mini-batch size 16. Rollouts are sampled
with vLLM [23] at temperature 0.7 and top-p = 1.0 with max_response_length 3072. We use an
AdamW optimizer and the SFT phase uses a constant learning rate.
The complete RLVP reward for a rollout follows Equation (5): r = V (y, c)Rtraj (y, c)Rphys (y, c).
The validity gate V (y, c) is 1 when the generated code executes and returns a finite, correctly-shaped
solution field or trajectory, and zero otherwise. In implementation, Ltraj is the rollout nRMSE,
so Rtraj = exp(−nRMSE/Ttraj ) with Ttraj = 0.05. The physics residual consistency term uses
the reference-relative residual loss from Equation (4), giving Rphys = exp(−Lphys /Tphys ) with
Tphys = 2.0. Separately, a rollout is counted as a success for evaluation when nRMSE ≤ 10−2 , this
threshold is used for evaluations in pass@k. The training, validation, and test splits contain 512,
64, and 128 PDE cases respectively, drawn approximately uniformly across the eight PDE families
using a fixed seed of 1234, and with disjoint PDE-specific sets of parameters and initial condition
combinations (refer to B.1) across splits.



                                                          17
A.2   Computational Resources

All training ran on a single node with 8 NVIDIA H200 GPUs, while evaluations were performed
using NVIDIA A100 GPUs. Each GRPO run trains for 50 epochs over 512 training problem instances
with 8 rollouts per prompt; wall-clock training time ranges between 1–2 days. Reward computation
runs on 16 CPU workers in parallel with the rollouts.

B     PDE problems and solver bank
This appendix specifies the eight PDE problems used throughout the paper and the selected solver
bank (used during SFT phase) associated with each. The selected solvers are standard schemes
drawn from numerical-methods literature, implemented in a common interface so that they can be
enumerated and called uniformly. Exact verification of every solver implementation against a closed-
form reference is not generally possible given the nonlinear and multidimensional problems in the
bank, so we adopt the following verification protocol: self-convergence, the method of manufactured
solutions (MMS) where an analytic forced solution is available, and cross-validation against published
reference trajectories, which we view as adequate within our current scope and as a starting point in
which future work can build on.

B.1   PDE problems

We consider eight PDEs spanning linear hyperbolic transport, nonlinear conservation laws, parabolic
reaction–diffusion, diffusion–sorption with mixed boundary conditions, steady variable-coefficient el-
liptic problems, and the incompressible Navier–Stokes and shallow-water systems in two dimensions.
Table 3 summarizes the PDE type, geometry, boundary conditions, and expected solution output
shapes for each. Throughout, subscripts denote partial derivatives, e.g., ut = ∂u/∂t, ux = ∂u/∂x,
and uxx = ∂ 2 u/∂x2 , with the same convention applying to other scalar, vector, and conserved
variables.

1D linear advection. We solve ut + β ux = 0 on x ∈ [0, 1) with periodic boundary conditions. We
use β ∈ {0.1, 0.4, 1.0, 2.0}, uniform grids with N ∈ {64, 128}, output times T ∈ {51, 101}, and
final time tfinal = 2.0. Initial conditions are smooth periodic profiles sampled from four families:
single sine, two-mode superposition, multimode waveform, and absolute-valued windowed waveform.
The analytical solution is u(x, t) = u0 (x − βt mod 1).
                                             2
                                              u
1D viscous Burgers. We solve ut + ∂x          2    = πν uxx on x ∈ [0, 1) with periodic boundary
conditions. Viscosity parameter is sampled from ν ∈ {10−3 , 10−2 , 10−1 , 1}. We use uniform grids
with N ∈ {64, 128}, output times T ∈ {51, 101}, and tfinal = 1.0. Initial conditions are sampled
from smooth periodic profiles: single-sine, two-mode, steeper-multimode families. As ν decreases,
solutions develop steeper gradients, and the positive viscosity keeps the equation in the viscous
regime within t ∈ [0, 1].

1D reaction–diffusion (Fisher–KPP). We solve ut = ν uxx + ρ u(1 − u) on x ∈ [0, 1) with
periodic boundary conditions. Parameters are sampled from (ν, ρ) ∈ {0.5, 1, 2, 5} × {1, 2, 5, 10}.
We use uniform grids with N ∈ {64, 128}, output times T ∈ {51, 101}, and tfinal = 1.0. Initial
conditions are sampled from single-sine, multimode, and front-like periodic families. This semilinear
parabolic problem combines diffusion with logistic growth.

                                                           D
1D nonlinear diffusion–sorption. We solve ut =                 uxx with retardation factor R(u) =
                                                          R(u)
1 + 1−ϕϕ ρs kf nf (u + ε)
                           nf −1
                                 , on x ∈ [0, 1] with the mixed boundary conditions u(t, 0) = usol
and ∂x u(t, 1) = 0. Parameters are sampled from D ∈ {10−4 , 5 × 10−4 , 1.5 × 10−3 } and kf ∈
{10−4 , 3.5 × 10−4 , 10−3 }, with fixed ϕ = 0.29, ρs = 2880, nf = 0.874, usol = 1, and ε = 10−6 .
We use N ∈ {64, 128}, output times T ∈ {51, 101}, and tfinal = 500.0. Initial conditions are
spatially uniform low-, mid-, and high-concentration states. The PDEBench-inspired problem [45]
tests nonlinear diffusion with a concentration-dependent Freundlich retardation factor and mixed
boundary conditions.


                                                  18
2D two-species reaction–diffusion. We solve ut = Du ∆u+(u−u3 −k−v), vt = Dv ∆v+(u−v),
on (x, y) ∈ [−1, 1]2 with homogeneous Neumann boundary conditions. Parameters are sampled
from (Du , Dv , k) ∈ {0.001, 0.002} × {0.005} × {0.005}. We use Nx , Ny ∈ {32, 48}, output times
T ∈ {31, 51}, and tfinal = 5.0. Initial fields are sampled from Gaussian noise, blob pair, and striped
noise families. The cubic activator and linear inhibitor produce labyrinthine and spotted patterns
characteristic of FitzHugh–Nagumo-type activator–inhibitor dynamics [53].

2D Darcy flow. We solve the steady-state elliptic problem −∇·(a(x, y) ∇u) = β on (x, y) ∈ [0, 1]2
with zero Dirichlet boundary conditions u = 0 on ∂Ω. The forcing parameter is sampled from
β ∈ {10−2 , 10−1 , 1, 10, 102 }, the permeability field a(x, y) is sampled from a heterogeneous family:
random blobs, checkerboard, and channelized, and we use Nx , Ny ∈ {32, 48}. The solution output
is expected to be the final steady-state field with shape [B, Nx , Ny ]. This is the only steady-state
problem in the PDE problems and solver bank.

2D incompressible Navier–Stokes. We solve ∇ · v = 0 and vt + (v · ∇)v = −∇p + ν ∆v + f
on [0, 1]2 with no-slip velocity boundary conditions v = 0 on ∂Ω. The viscosity is sampled from
ν ∈ {0.005, 0.01, 0.02}. The initial velocity is generated from a random streamfunction with
τv = −3, producing a divergence-reduced field. The two forcing components are independently
sampled Gaussian random fields with τf = −1. Velocity and forcing scales are sampled from
{0.1, 0.15, 0.2} and {0.25, 0.4, 0.55}, respectively. We use grids (Nx , Ny ) ∈ {(16, 16), (24, 24)},
output times T ∈ {11, 21}, and tfinal = 1.0.

2D shallow water (dam break). We solve the shallow water system              in conservative variables
(h, hu, hv): ht + (hu)x + (hv)y = 0, (hu)t + (hu)2 /h + 12 gh2 x + ((hu)(hv)/h)y = 0, and
                                                                      

(hv)t + ((hu)(hv)/h)x + (hv)2 /h + 12 gh2 y = 0 on (x, y) ∈ [−2.5, 2.5]2 with extrapolation-style
                                               

boundary treatment, g ∈ {1, 2}. We use Nx , Ny ∈ {32, 48}, output times T ∈ {31, 51}, and
tfinal = 1.0. Initial conditions are sampled from radial dam-break states with dam radii 0.35, 0.50, or
0.65.

Table 3: PDE problems used in this work. B denotes the batch dimension of initial conditions, T the
number of output temporal snapshots, and N (or Nx × Ny ) the spatial resolution. For multi-field
systems, the last dimension indexes the returned variables.
       PDE                    Type                     Geometry       Output shape          # solvers
       advection1d            lin. hyperbolic          1D periodic    [B, T, N ]            8
       burgers1d              nonlin. viscous cons.    1D periodic    [B, T, N ]            18
       reaction_diffusion1d   semilin. parabolic       1D periodic    [B, T, N ]            6
       diffusion_sorption1d   nonlin. retarded par.    1D mixed BC    [B, T, N ]            8
       reaction_diffusion2d   2-species parabolic      2D Neumann     [B, T, Nx , Ny , 2]   6
       darcy2d                steady elliptic          2D Dirichlet   [B, Nx , Ny ]         8
       incompressible_ns2d    incomp. NS w/ proj.      2D Dirichlet   [B, T, Nx , Ny , 2]   10
       shallow_water2d        hyperbolic system        2D extrapol.   [B, T, Nx , Ny , 3]   7



B.2   Solver bank organization

Table 3 summarizes the selected solver bank used for training and evaluation. We annotate each
solver here by its numerical method family, spatial discretization, time integrator, stability controls,
and implementation checks before using them in the solver bank for SFT.
The selected solvers in the bank are designed to cover a representative set of standard numerical
idioms associated with each problem class rather than variants of a single template. For hyperbolic and
conservation-law problems, the bank includes semi-Lagrangian characteristic methods, finite-volume
Godunov, Rusanov, HLL/HLLC, Roe-type, MUSCL, Lax–Wendroff, MacCormack, and Kurganov–
Tadmor schemes, paired with standard explicit and strong-stability-preserving time integrators
[54–56, 2, 57, 58]. For parabolic and reaction–diffusion systems, the bank includes method-of-lines
finite differences, Strang splitting with exact reaction updates when available, Fourier and DCT
spectral diffusion, IMEX schemes, and implicit linearized or nonlinear solves [59, 60, 4, 61].



                                                      19
For elliptic and incompressible-flow problems, the bank includes cell-centered finite-volume dis-
cretizations, Jacobi and Gauss–Seidel variants, SOR, CG, preconditioned CG, ILU-preconditioned
solves, and Chorin-style projection methods with finite-difference and spectral pressure solvers
[62–64]. Spectral solvers use standard dealiasing where appropriate [65].
For each PDE problem, detailed curated solver bank tables are listed in Tables 4 to 11. The reference
column records either the implementation source (e.g., PDEBench-derived anchor schemes) or
canonical method references for the corresponding discretization family.

Table 4: Solver bank for 1D linear advection. Each row gives the spatial scheme, time integrator, and
reference source from which the implementation can be derived.
codename                                  spatial scheme                                    time integrator                                  reference
semi_lagrangian                           periodic linear interp.                           characteristic backtrace with interp.            Staniforth and Côté [66]
pdebench_fd2_midpoint_vanleer             limited MUSCL, Rusanov flux                       RK2 midpoint                                     Takamoto et al. [45], Van Leer [55]
pdebench_rusanov2                         MUSCL (minmod), Rusanov flux                      RK2 midpoint                                     Takamoto et al. [45], LeVeque [2]
central4_rk4                              4th-order centered FD                             RK4                                              LeVeque [67]
muscl_rusanov_ssprk3                      limited MUSCL, Rusanov flux                       SSPRK3                                           Van Leer [55], LeVeque [2], Gottlieb et al. [58]
spectral_rk4                              Fourier pseudospectral                            RK4 with CFL substeps                            Trefethen [4]
fourier_exact_shift                       FFT phase shift                                   exact per output interval                        Trefethen [4]
fourier_spectral_rk4                      Fourier pseudospectral                            RK4 with CFL substeps                            Trefethen [4]




Table 5: Solver bank for 1D viscous Burgers. Each row gives the spatial scheme, time integrator, and
reference source from which the implementation can be derived. Most entries combine a hyperbolic
flux with a centered finite-difference Laplacian for viscosity; spectral and IMEX methods instead
treat diffusion in Fourier space or with Crank–Nicolson. Time integrators marked with † couple the
explicit advection and the implicit diffusion through operator splitting within CFL substeps.
codename                                   spatial scheme                                    time integrator                             reference
godunov_{euler,ssprk2,ssprk3}              exact Godunov flux + centered Laplacian           forward Euler / SSPRK2 / SSPRK3             Godunov and Bohachevsky [54], LeVeque [2], Gottlieb et al. [58]
lax_friedrichs_{euler,ssprk2,ssprk3}       local Lax–Friedrichs flux + centered Laplacian    forward Euler / SSPRK2 / SSPRK3             LeVeque [2], Gottlieb et al. [58]
rusanov_{euler,ssprk2,ssprk3}              Rusanov flux + centered Laplacian                 forward Euler / SSPRK2 / SSPRK3             Rusanov [68], LeVeque [2], Gottlieb et al. [58]
muscl_rusanov_{euler,rk2,ssprk2,ssprk3}    MUSCL (minmod), Rusanov flux + Laplacian          forward Euler / RK2 / SSPRK2 / SSPRK3       Van Leer [55], LeVeque [2], Gottlieb et al. [58]
lax_wendroff                               two-step Lax–Wendroff + Laplacian                 single step with CFL substeps               Lax and Wendroff [69], LeVeque [2]
maccormack                                 MacCormack predictor–corrector + Laplacian        predictor–corrector                         MacCormack [70], LeVeque [2]
imex_cn_fixed                              Rusanov flux + periodic Laplacian                 explicit advection + CN diffusion†          Ascher et al. [60], Hundsdorfer et al. [71]
spectral_rk4_dealias                       Fourier pseudospectral, 2/3 dealias               RK4                                         Orszag [65], Trefethen [4]
spectral_if_rk4_dealias                    dealiased nonlinear flux, exact diffusion         integrating-factor RK4                      Orszag [65], Trefethen [4], Kassam and Trefethen [61]




Table 6: Solver bank for 1D reaction–diffusion. Each row gives the spatial scheme, time integrator,
and reference source from which the implementation can be derived. The bank includes both second-
order finite-difference and Fourier-spectral treatments of the periodic diffusion operator.
codename                         spatial scheme                                        time integrator                                                              reference
fd_explicit_{euler,rk2,rk4}      2nd-order centered periodic FD Laplacian              forward Euler / RK2 / RK4 on full RHS                                        LeVeque [67], Hundsdorfer et al. [71]
split_strang_fd_rk2_pes          centered FD diffusion + pointwise logistic reaction   Strang splitting; exact/PES reaction half-steps + RK2 diffusion              Strang [59], Hundsdorfer et al. [71]
spectral_strang_exact_reaction   Fourier spectral diffusion                            Strang splitting with exact logistic reaction and exact spectral diffusion   Strang [59], Trefethen [4]
spectral_imex_exact_diffusion    Fourier spectral diffusion                            RK4 reaction + exact spectral diffusion                                      Hundsdorfer et al. [71], Trefethen [4]




B.3        Numerical methods verification protocol

We audit the code implementations used in the solver bank meant for SFT. Exact verification against
a closed-form reference is not generally possible for the nonlinear and multidimensional problems in
the solver bank, so we use three independent diagnostics, ordered from cheapest to most citable. We
view the combined evidence as adequate within the scope of this paper while acknowledging that
more comprehensive verification (e.g., adaptively-refined reference solutions or cross-comparison
against an independent verified code base) is a natural extension.

           1. Self-convergence. Standard refinement triples in N at fixed output times, asserting that
              errors decrease monotonically and that observed orders match the formal order of the
              scheme. Where applicable, we additionally require that solvers within a scheme family
              agree on smooth initial data to within their formal order at fixed resolution. We present the
              quantitative results in Figure 6.
           2. Method of manufactured solutions (MMS). For each PDE we construct a smooth an-
              alytic solution ue , derive the corresponding source term se symbolically, and run each
              solver on the forced PDE. This produces absolute error against the exact ue at each grid
              level rather than a self-consistency ratio, and detects sign errors and stencil bugs that self-
              convergence cannot. For Burgers we use ue (x, t) = a + b sin(2π(x − ct)); for Darcy we


                                                                                             20
Table 7: Solver bank for 1D nonlinear diffusion–sorption. Each row gives the spatial scheme, time
integrator or nonlinear treatment, and reference source from which the implementation can be derived.
All entries use the mixed left-Dirichlet/right-Neumann boundary conditions treatment.
codename                               spatial scheme                                               time integrator / nonlinear treatment           reference
euler_fixed                            lagged-mobility FD Laplacian                                 forward Euler                                   LeVeque [67]
heun_fixed                             lagged-mobility FD Laplacian                                 Heun / RK2                                      Hundsdorfer et al. [71]
rk4_fixed                              lagged-mobility FD Laplacian                                 classical RK4                                   Hundsdorfer et al. [71]
backward_euler_lagged                  lagged-linearized mixed-BC tridiagonal system                backward Euler                                  Hundsdorfer et al. [71]
crank_nicolson_lagged                  lagged-linearized mixed-BC tridiagonal system                Crank–Nicolson                                  Hundsdorfer et al. [71]
backward_euler_newton_tridiag          nonlinear mixed-BC tridiagonal Jacobian                      Newton backward Euler                           Hundsdorfer et al. [71]
crank_nicolson_newton_tridiag          nonlinear mixed-BC tridiagonal Jacobian                      Newton Crank–Nicolson                           Hundsdorfer et al. [71]
mol_bdf_solve_ivp_mixedbc              mixed-BC method of lines with tridiagonal sparsity           adaptive BDF via solve_ivp                      Virtanen et al. [64]



Table 8: Solver bank for 2D two-species reaction–diffusion. Each row gives the spatial scheme, time
integrator, and reference source from which the implementation can be derived. Finite-difference
entries use edge padding for homogeneous Neumann boundary conditions, while DCT entries
diagonalize the discrete Neumann Laplacian in a cosine basis.
codename                        spatial scheme                                   time integrator                                        reference
fd_explicit_{euler,rk2,rk4}     5-point FD Laplacian with Neumann edge padding   forward Euler / RK2 / RK4 on full RHS                  LeVeque [67], Hundsdorfer et al. [71]
strang_rk4_reaction_cn_sparse   sparse 5-point Neumann Laplacian                 Strang splitting; RK4 reaction + CN diffusion          Strang [59], Hundsdorfer et al. [71]
dct_neumann_strang_split        DCT-diagonalized Neumann Laplacian               Strang splitting; RK4 reaction + exact DCT diffusion   Strang [59], Trefethen [4]
dct_neumann_imex_rk2            DCT-diagonalized Neumann Laplacian               RK2 reaction + exact DCT diffusion                     Hundsdorfer et al. [71], Trefethen [4]




              use ue (x, y) = sin(πx) sin(πy) with permeability ae (x, y) = 1 + 12 cos(2πx) cos(2πy).
              We report representative MMS results for the PDE cases below.
           3. Cross-validation against published reference trajectories. For PDEs covered by
              PDEBench [45], we run the corresponding selected solvers on the published parameter
              settings and compare normalized RMSE against the released reference trajectories. This
              provides a check against an independent benchmark, complementing self-convergence and
              MMS.

Tables 12 and 13 report representative MMS results. Across the tested Burgers schemes, the observed
refinement trends are consistent with the expected behavior of low-order, second-order, and spectral
discretizations [2]. For Darcy flow, MMS results confirm that the cell-centered FV operator with
arithmetic face averaging achieves observed order 2.00 on smooth coefficients.




                                                                             21
Table 9: Solver bank for 2D Darcy flow. Each row gives the spatial discretization, linear solver, and
reference source from which the implementation can be derived. All entries solve a cell-centered
finite-volume system with arithmetic face-averaged permeability and zero Dirichlet boundary values.
codename                                                  spatial discretization                       linear solver                                          reference
steady_state_cg_fv_arithmetic                             5-point cell-centered FV, arithmetic faces   conjugate gradient                                     Eymard et al. [72], Hestenes et al. [73]
steady_state_jacobi_fv_arithmetic                         5-point cell-centered FV, arithmetic faces   Jacobi relaxation                                      Eymard et al. [72], Saad [74]
steady_state_weighted_jacobi_fv_arithmetic                5-point cell-centered FV, arithmetic faces   weighted Jacobi (ω = 0.75)                             Eymard et al. [72], Saad [74]
steady_state_redblack_gauss_seidel_fv_arithmetic          5-point cell-centered FV, arithmetic faces   red–black Gauss–Seidel                                 Eymard et al. [72], Saad [74]
steady_state_sor_fv_arithmetic                            5-point cell-centered FV, arithmetic faces   SOR (ω = 1.7)                                          Eymard et al. [72], Saad [74]
steady_state_pcg_jacobi_fv_arithmetic                     5-point cell-centered FV, arithmetic faces   Jacobi-preconditioned CG                               Eymard et al. [72], Hestenes et al. [73]
geometric_multigrid_vcycle_fv                             5-point cell-centered FV, arithmetic faces   Jacobi-preconditioned CG with sparse-direct fallback   Eymard et al. [72], Hestenes et al. [73], Saad [74], Virtanen et al. [64]
pcg_ilu_fv                                                5-point cell-centered FV, arithmetic faces   ILU-preconditioned CG with sparse-direct fallback      Eymard et al. [72], Hestenes et al. [73], Saad [74], Virtanen et al. [64]




Table 10: Solver bank for 2D incompressible Navier–Stokes. Each row gives the advection/diffusion
discretization, projection and time integration, and reference source from which the implementation
can be derived.
codename                         advection / diffusion discretization                                   projection and time integrator                               reference
chorin_centered_euler            centered finite differences                                            Chorin projection, forward Euler, Jacobi pressure solve      Chorin [62], Ferziger et al. [75]
chorin_centered_rk2              centered finite differences                                            Chorin projection, RK2, Jacobi pressure solve                Chorin [62], Ferziger et al. [75]
chorin_skewsym_euler             skew-symmetric finite-difference advection                             Chorin projection, forward Euler, Jacobi pressure solve      Chorin [62], Ferziger et al. [75]
semiimplicit_centered_euler      centered advection with semi-implicit diffusion                        projection IMEX Euler, Jacobi pressure solve                 Chorin [62], Ascher et al. [60], Ferziger et al. [75]
imex_cnab2_skewsym               skew-symmetric advection + CN diffusion                                CNAB2 projection, Jacobi pressure solve                      Ascher et al. [60], Ferziger et al. [75]
dst_projection_cnab2_runtime     centered/skew-symmetric projection form                                CNAB2 projection with DST Poisson/Helmholtz solves           Chorin [62], Ascher et al. [60], Strang [63], Virtanen et al. [64]
imex_cnab2_skewsym_spectral      skew-symmetric advection + CN diffusion                                CNAB2 projection with DST Poisson/Helmholtz solves           Ascher et al. [60], Strang [63]
semiimplicit_centered_spectral   centered advection + semi-implicit diffusion                           IMEX Euler projection with DST solves                        Ascher et al. [60], Strang [63]
mac_projection_centered          centered advection + semi-implicit diffusion (DST projection alias)    IMEX Euler projection with DST Poisson/Helmholtz solves      Chorin [62], Ascher et al. [60], Strang [63], Virtanen et al. [64]
mac_projection_rk2               skew-symmetric advection + CN diffusion (DST projection alias)         CNAB2 projection with DST Poisson/Helmholtz solves           Ascher et al. [60], Strang [63], Virtanen et al. [64]




Table 11: Solver bank for 2D shallow-water. Each row gives the flux, reconstruction and time
integration strategy, and reference source from which the implementation can be derived.
codename                                               flux                             reconstruction & time integrator                      reference
fv_muscl_hll_ssprk3                                    HLL                              MUSCL (MC), SSPRK3                                    Toro [57], Van Leer [55], Gottlieb et al. [58]
fv_muscl_rusanov_{ssprk2,ssprk3}                       Rusanov                          MUSCL (MC), SSPRK2 / SSPRK3                           Toro [57], Van Leer [55], Gottlieb et al. [58]
kt_central_upwind_muscl_ssprk3                         Kurganov–Tadmor                  MUSCL (MC), SSPRK3                                    Kurganov and Tadmor [56], Van Leer [55], Gottlieb et al. [58]
weno5_rusanov_ssprk3_pos                               Rusanov                          MUSCL (MC), SSPRK3                                    Toro [57], Van Leer [55], Gottlieb et al. [58]
roe_entropy_fix_muscl_ssprk3                           Roe with entropy fix             MUSCL (MC), SSPRK3                                    Roe [76], Toro [57], Van Leer [55], Gottlieb et al. [58]
hllc_muscl_ssprk3_pos                                  HLLC                             MUSCL (MC), SSPRK3                                    Toro [57], Van Leer [55], Gottlieb et al. [58]




Table 12: MMS verification for representative 1D Burgers solvers, ν = 10−2 , tfinal = 0.2, ∆t =
0.4 ∆x. Observed orders are computed by linear regression of log ∥uh − ue ∥L2 against log ∆x across
the refinement sequence.
solver                                                                  formal order                         observed order                          median ∥u − ue ∥L2 at N = 256
lax_friedrichs_ssprk3                                                         1                                          0.99                                                7.6 × 10−4
rusanov_ssprk3                                                                1                                          1.00                                                7.6 × 10−4
muscl_rusanov_ssprk3                                                          2                                          1.97                                                5.2 × 10−5
lax_wendroff                                                                  2                                          1.99                                                4.8 × 10−5
maccormack                                                                    2                                          1.99                                                4.7 × 10−5
spectral_if_rk4_dealias                                                 superalgebraic                                 saturated                                             7.7 × 10−7




Table 13: MMS verification for the 2D Darcy cell-centered FV discretization with arithmetic face
averaging. Reference solve uses tight-tolerance preconditioned CG (relative residual ≤ 10−12 ).
                                                   N                           h                       ∥uh − ue ∥L2                      observed order
                                                                                        −2                                  −3
                                                   16             6.25 × 10                            1.12 × 10                                      –
                                                   32             3.13 × 10−2                          2.80 × 10−4                                  2.01
                                                   64             1.56 × 10−2                          6.99 × 10−5                                  2.00
                                                  128             7.81 × 10−3                          1.75 × 10−5                                  2.00




                                                                                                           22
      10 2
                          central4_rk4                        10 2
                                                                                fourier_exact_shift                     10 2
                                                                                                                                         fourier_spectral_rk4                     10 1
                                                                                                                                                                                                  muscl_rusanov_ssprk3                      10 1
                                                                                                                                                                                                                                                        pdebench_fd2_midpoint_vanleer                10 1
                                                                                                                                                                                                                                                                                                                      pdebench_rusanov2                        10 1
                                                                                                                                                                                                                                                                                                                                                                                  semi_lagrangian                       10 2
                                                                                                                                                                                                                                                                                                                                                                                                                                             spectral_rk4

      10 3                                                    10 3                                                      10 3                                                                                                                10 2                                                                                                                                                                        10 3
                                                                                                                                                                                  10 2                                                                                                               10 2                                                      10 2
err




                                                        err




                                                                                                                  err




                                                                                                                                                                            err




                                                                                                                                                                                                                                      err




                                                                                                                                                                                                                                                                                               err




                                                                                                                                                                                                                                                                                                                                                         err




                                                                                                                                                                                                                                                                                                                                                                                                                  err
      10 4                                                    10 4                                                      10 4                                                                                                                10 3                                                                                                                                                                        10 4


      10 5                                                    10 5                                                      10 5                                                      10 3                                                      10 4                                                     10 3                                                      10 3                                                     10 5
             16          32          64           128                16           32          64            128                16           32          64            128                16           32          64            128                16           32           64          128                16           32          64            128                16           32         64            128                16           32                64     128
                               N                                                        N                                                         N                                                         N                                                          N                                                       N                                                         N                                                           N


      10 1
                         godunov_euler                        10 1
                                                                                 godunov_ssprk2                         10 1
                                                                                                                                           godunov_ssprk3                         10 1
                                                                                                                                                                                                      imex_cn_fixed                         10 1
                                                                                                                                                                                                                                                              lax_friedrichs_euler                   10 1
                                                                                                                                                                                                                                                                                                                      lax_friedrichs_ssprk2                    10 1
                                                                                                                                                                                                                                                                                                                                                                               lax_friedrichs_ssprk3                    10 1
                                                                                                                                                                                                                                                                                                                                                                                                                                            lax_wendroff



      10 2                                                    10 2                                                      10 2                                                      10 2                                                      10 2                                                     10 2                                                      10 2                                                     10 2
err




                                                        err




                                                                                                                  err




                                                                                                                                                                            err




                                                                                                                                                                                                                                      err




                                                                                                                                                                                                                                                                                               err




                                                                                                                                                                                                                                                                                                                                                         err




                                                                                                                                                                                                                                                                                                                                                                                                                  err
      10 3                                                    10 3                                                      10 3                                                      10 3                                                      10 3                                                     10 3                                                      10 3                                                     10 3
             16          32          64           128                16           32          64            128                16           32          64            128                16           32          64            128                16           32           64          128                16           32          64            128                16           32         64            128                16           32                64     128
                               N                                                        N                                                         N                                                         N                                                          N                                                       N                                                         N                                                           N


      10 1
                          maccormack                          10 1
                                                                              muscl_rusanov_euler                       10 1
                                                                                                                                          muscl_rusanov_rk2                       10 1
                                                                                                                                                                                                  muscl_rusanov_ssprk2                      10 1
                                                                                                                                                                                                                                                            muscl_rusanov_ssprk3                     10 1
                                                                                                                                                                                                                                                                                                                         rusanov_euler                         10 1
                                                                                                                                                                                                                                                                                                                                                                                  rusanov_ssprk2                        10 1
                                                                                                                                                                                                                                                                                                                                                                                                                                           rusanov_ssprk3



      10 2                                                    10 2                                                      10 2                                                      10 2                                                      10 2                                                     10 2                                                      10 2                                                     10 2
err




                                                        err




                                                                                                                  err




                                                                                                                                                                            err




                                                                                                                                                                                                                                      err




                                                                                                                                                                                                                                                                                               err




                                                                                                                                                                                                                                                                                                                                                         err




                                                                                                                                                                                                                                                                                                                                                                                                                  err
      10 3                                                    10 3                                                      10 3                                                      10 3                                                      10 3                                                     10 3                                                      10 3                                                     10 3
             16          32          64           128                16           32          64            128                16           32          64            128                16           32          64            128                16           32           64          128                16           32          64            128                16           32         64            128                16           32                64     128
                               N                                                        N                                                         N                                                         N                                                          N                                                       N                                                         N                                                           N


      10 1
                     spectral_if_rk4_dealias                  10 1
                                                                               spectral_rk4_dealias                     10 2
                                                                                                                                           fd_explicit_euler                      10 2
                                                                                                                                                                                                      fd_explicit_rk2                       10 2
                                                                                                                                                                                                                                                                fd_explicit_rk4                      10 2
                                                                                                                                                                                                                                                                                                                 spectral_imex_exact_diffusion                 10 2
                                                                                                                                                                                                                                                                                                                                                                           spectral_strang_exact_reaction               10 2
                                                                                                                                                                                                                                                                                                                                                                                                                                       split_strang_fd_rk2_pes

                                                                                                                        10 3                                                      10 3                                                      10 3                                                     10 3                                                      10 3                                                     10 3
      10 2                                                    10 2
err




                                                        err




                                                                                                                  err




                                                                                                                                                                            err




                                                                                                                                                                                                                                      err




                                                                                                                                                                                                                                                                                               err




                                                                                                                                                                                                                                                                                                                                                         err




                                                                                                                                                                                                                                                                                                                                                                                                                  err
                                                                                                                        10 4                                                      10 4                                                      10 4                                                     10 4                                                      10 4                                                     10 4


      10 3                                                    10 3                                                      10 5                                                      10 5                                                      10 5                                                     10 5                                                      10 5                                                     10 5
             16          32          64           128                16           32          64            128                16           32          64            128                16           32          64            128                16           32           64          128                16           32          64            128                16           32         64            128                16           32                64     128
                               N                                                        N                                                         N                                                         N                                                          N                                                       N                                                         N                                                           N


      10 1
                     backward_euler_lagged                    10 1
                                                                          backward_euler_newton_tridiag                 10 1
                                                                                                                                        crank_nicolson_lagged                     10 1
                                                                                                                                                                                              crank_nicolson_newton_tridiag                 10 1
                                                                                                                                                                                                                                                                  euler_fixed                        10 1
                                                                                                                                                                                                                                                                                                                           heun_fixed                          10 1
                                                                                                                                                                                                                                                                                                                                                                            mol_bdf_solve_ivp_mixedbc                   10 1
                                                                                                                                                                                                                                                                                                                                                                                                                                                 rk4_fixed



      10 2                                                    10 2                                                      10 2                                                      10 2                                                      10 2                                                     10 2                                                      10 2                                                     10 2
err




                                                        err




                                                                                                                  err




                                                                                                                                                                            err




                                                                                                                                                                                                                                      err




                                                                                                                                                                                                                                                                                               err




                                                                                                                                                                                                                                                                                                                                                         err




                                                                                                                                                                                                                                                                                                                                                                                                                  err
      10 3                                                    10 3                                                      10 3                                                      10 3                                                      10 3                                                     10 3                                                      10 3                                                     10 3
             16          32          64           128                16           32          64            128                16           32          64            128                16           32          64            128                16           32           64          128                16           32          64            128                16           32         64            128                16           32                64     128
                               N                                                        N                                                         N                                                         N                                                          N                                                       N                                                         N                                                           N


      10 1
                     dct_neumann_imex_rk2                     10 1
                                                                            dct_neumann_strang_split                    10 1
                                                                                                                                           fd_explicit_euler                      10 1
                                                                                                                                                                                                      fd_explicit_rk2                       10 1
                                                                                                                                                                                                                                                                fd_explicit_rk4                      10 1
                                                                                                                                                                                                                                                                                                                 strang_rk4_reaction_cn_sparse                 10 1
                                                                                                                                                                                                                                                                                                                                                                           geometric_multigrid_vcycle_fv                10 1
                                                                                                                                                                                                                                                                                                                                                                                                                                                 pcg_ilu_fv



      10 2                                                    10 2                                                      10 2                                                      10 2                                                      10 2                                                     10 2
err




                                                        err




                                                                                                                  err




                                                                                                                                                                            err




                                                                                                                                                                                                                                      err




                                                                                                                                                                                                                                                                                               err




                                                                                                                                                                                                                                                                                                                                                         err




                                                                                                                                                                                                                                                                                                                                                                                                                  err
      10 3                                                    10 3                                                      10 3                                                      10 3                                                      10 3                                                     10 3                                                      10 2                                                     10 2
             16                32                 64                 16                 32                  64                 16                 32                  64                 16                 32                  64                 16                  32                64                 16                 32                  64                 16                 32                 64                 16                    32              64
                               N                                                        N                                                         N                                                         N                                                          N                                                       N                                                         N                                                           N


      10 1
                  steady_state_cg_fv_arithmetic               10 1
                                                                          steady_state_jacobi_fv_arith...               10 1
                                                                                                                                    steady_state_pcg_jacobi_fv_a...               10 1
                                                                                                                                                                                              steady_state_redblack_gauss_...               10 1
                                                                                                                                                                                                                                                        steady_state_sor_fv_arithmetic               10 1
                                                                                                                                                                                                                                                                                                                 steady_state_weighted_jacobi...               10 1
                                                                                                                                                                                                                                                                                                                                                                               chorin_centered_euler                    10 1
                                                                                                                                                                                                                                                                                                                                                                                                                                         chorin_centered_rk2
err




                                                        err




                                                                                                                  err




                                                                                                                                                                            err




                                                                                                                                                                                                                                      err




                                                                                                                                                                                                                                                                                               err




                                                                                                                                                                                                                                                                                                                                                         err




      10 2                                                    10 2                                                      10 2                                                      10 2                                                      10 2                                                     10 2                                                      10 2                                               err   10 2
             16                32                 64                 16                 32                  64                 16                 32                  64                 16                 32                  64                 16                  32                64                 16                 32                  64                 16                 32                 64                 16                    32              64
                               N                                                        N                                                         N                                                         N                                                          N                                                       N                                                         N                                                           N


      10 1
                     chorin_skewsym_euler                     10 1
                                                                          dst_projection_cnab2_runtime                  10 1
                                                                                                                                        imex_cnab2_skewsym                        10 1
                                                                                                                                                                                              imex_cnab2_skewsym_spectral                   10 1
                                                                                                                                                                                                                                                           mac_projection_centered                   10 1
                                                                                                                                                                                                                                                                                                                       mac_projection_rk2                      10 1
                                                                                                                                                                                                                                                                                                                                                                            semiimplicit_centered_euler                 10 1
                                                                                                                                                                                                                                                                                                                                                                                                                                    semiimplicit_centered_spectral
err




                                                        err




                                                                                                                  err




                                                                                                                                                                            err




                                                                                                                                                                                                                                      err




                                                                                                                                                                                                                                                                                               err




                                                                                                                                                                                                                                                                                                                                                         err




                                                                                                                                                                                                                                                                                                                                                                                                                  err




      10 2                                                    10 2                                                      10 2                                                      10 2                                                      10 2                                                     10 2                                                      10 2                                                     10 2
             16                32                 64                 16                 32                  64                 16                 32                  64                 16                 32                  64                 16                  32                64                 16                 32                  64                 16                 32                 64                 16                    32              64
                               N                                                        N                                                         N                                                         N                                                          N                                                       N                                                         N                                                           N


       100
                       fv_muscl_hll_ssprk3                     100
                                                                            fv_muscl_rusanov_ssprk2                      100
                                                                                                                                      fv_muscl_rusanov_ssprk3                      100
                                                                                                                                                                                                  hllc_muscl_ssprk3_pos                      100
                                                                                                                                                                                                                                                        kt_central_upwind_muscl_ssprk3                100
                                                                                                                                                                                                                                                                                                                 roe_entropy_fix_muscl_ssprk3                   100
                                                                                                                                                                                                                                                                                                                                                                            weno5_rusanov_ssprk3_pos                                      advection1d
                                                                                                                                                                                                                                                                                                                                                                                                                                          burgers1d
                                                                                                                                                                                                                                                                                                                                                                                                                                          reaction_diffusion1d
      10 1                                                    10 1                                                      10 1                                                      10 1                                                      10 1                                                     10 1                                                      10 1
                                                                                                                                                                                                                                                                                                                                                                                                                                          diffusion_sorption1d
                                                                                                                                                                                                                                                                                                                                                                                                                                          reaction_diffusion2d
err




                                                        err




                                                                                                                  err




                                                                                                                                                                            err




                                                                                                                                                                                                                                      err




                                                                                                                                                                                                                                                                                               err




                                                                                                                                                                                                                                                                                                                                                         err




                                                                                                                                                                                                                                                                                                                                                                                                                                          darcy2d
                                                                                                                                                                                                                                                                                                                                                                                                                                          incompressible_ns2d
      10 2                                                    10 2                                                      10 2                                                      10 2                                                      10 2                                                     10 2                                                      10 2                                                                       shallow_water2d
             16                32                 64                 16                 32                  64                 16                 32                  64                 16                 32                  64                 16                  32                64                 16                 32                  64                 16                 32                 64
                               N                                                        N                                                         N                                                         N                                                          N                                                       N                                                         N




Figure 6: Self-convergence of the solver bank across the 8 PDE families. Each panel shows the
relative pairwise error between consecutive grid resolutions as a function of the coarse resolution,
using log-log axes. Lower error and a decreasing trend under refinement indicate numerically
consistent solver behavior.




                                                                                                                                                                                                                              23
C    From Binary Verification to Expected Pass Rewards
The physical accuracy reward Rtraj , instantiated through function-space trajectory error in Section 3.5,
can also be viewed as a probabilistic analogue of binary RLVR. A standard binary verifier accepts a
generated solver if its trajectory error is below a fixed tolerance,
                                      u, u⋆ ) = 1{Ltraj (b
                                  Vϵ (b                  u, u⋆ ) ≤ ϵ} .                              (8)
Instead of fixing a single tolerance, suppose the tolerance is drawn from a distribution ϵ ∼ D with
cumulative distribution function FD . The corresponding expected binary reward is
                        u, u⋆ ) = Eϵ∼D [Vϵ (b
                    RD (b                   u, u⋆ )] = Pϵ∼D (ϵ ≥ Ltraj (b
                                                                        u, u⋆ )) .                   (9)
Thus, the dense reward induced by a stochastic tolerance is the survival function of the tolerance
distribution:
                               RD (bu, u⋆ ) = 1 − FD (Ltraj (b
                                                             u, u⋆ )) .                           (10)
This shows that a dense reward can be interpreted as the expected pass probability of a binary verifier
under uncertainty over the acceptance tolerance.
RLVP chooses an exponential tolerance distribution,
                    ϵ ∼ Exp(Ttraj ),       P(ϵ ≥ t) = exp(−t/Ttraj )      for t ≥ 0.                (11)
Substituting this survival function into (10) gives
                                                           u, u⋆ )
                                                                  
                                  ⋆                 Ltraj (b
                              u, u ) ≤ ϵ}] = exp −
                 Eϵ [1{Ltraj (b                                               u, u⋆ ).
                                                                     = Rtraj (b                     (12)
                                                       Ttraj
In this sense, Rtraj is not merely a heuristic soft score. It is the exact expected reward of a binary
verifier whose acceptance tolerance is stochastic. The exponential distribution is a minimally
structured choice: it is the maximum-entropy distribution on R≥0 with fixed mean and equivalently
the waiting-time law of a homogeneous Poisson process [77, 78]. It places the highest density near
strict tolerances while retaining an exponentially decaying probability of more lenient thresholds.
The temperature Ttraj controls the typical tolerance scale: small Ttraj concentrates the distribution
near zero and makes the verifier sharper, while large Ttraj spreads probability over a wider range
of tolerances and gives smoother partial credit. In the limit Ttraj → 0, the reward approaches an
exact-zero verifier, Rtraj → 1{Ltraj = 0}; in the limit Ttraj → ∞, Rtraj → 1 for all finite errors.
Other tolerance distributions would induce different dense rewards and we leave their analysis and
inclusion as future work.
The same Gibbs form appears in two classical contexts. In Markov chain Monte Carlo, the Metropolis
acceptance criterion accepts a proposal with energy increase ∆E with probability exp(−∆E/T )
[79]. In maximum-entropy reinforcement learning, entropy-regularized optimal policies take an
exponential form in the value function, with the entropy temperature controlling the sharpness of the
induced distribution [80, 81]. Our use of the Gibbs form is distinct from both: it is not a sampling
acceptance rule and not a policy distribution, but a verifier reward for generated PDE solvers. The
derivation above makes the connection to binary verification explicit: the Gibbs reward is the expected
pass probability of a binary verifier under an exponential distribution over tolerances.
The same stochastic-tolerance construction applies to any nonnegative diagnostic. For physics
residual consistency, RLVP uses the reference-relative residual loss in Equation (4); substituting
this loss into the exponential expected-pass form yields Section 3.5. Comparing to the reference
residual absorbs discretization error from the numerical reference solution and prevents the verifier
from demanding a residual smaller than the reference solver itself. A reference-free variant based
directly on ρ(bu) recovers the canonical physics-residual regularization used in physics-informed
scientific machine learning [41, 48, 47]; we use the reference-relative form for consistency with
reference-solution evaluation.

D    Evaluation details
Let vp,c,s ∈ {0, 1} denote validity for prompt p, case c, and sample s ∈ {1, . . . , 8}.



                                                   24
We use the range-normalized evaluation error
                                          q                           
                                             mean (ûp,c,s − u⋆p,c )2
                          nRMSEp,c,s =                                  ,                     (13)
                                            max(u⋆p,c ) − min(u⋆p,c )
with the evaluator fallback to the RMS magnitude, and then to 1, when the reference range is
numerically zero. A sample succeeds if it is valid and satisfies
                         ap,c,s = 1 vp,c,s = 1 ∧ nRMSEp,c,s ≤ 10−2 .
                                                                 
                                                                                        (14)
We use a success threshold of nRMSE = 10−2 for all PDEs in both seen and unseen tasks.
                                                           P8
We report combinatorial pass@k. For each case, let qp,c = s=1 ap,c,s . With n = 8 samples,
                                                       8−qp,c
                                                              
                                  \ p,c = 1 −            k
                                 pass@k                     .8                            (15)
                                                              k

Thus pass@1 is qp,c /8, the expected success rate of one sampled solver, and pass@8 is 1[qp,c > 0],
i.e. whether at least one of the 8 sampled solvers succeeds.
For continuous physical accuracy, we report median best-of-8 nRMSE. For samples that are invalid,
missing, or non-finite, they receive a 1.0 penalty with valid finite errors capped at 1.0:
                                   
                                       min(nRMSEp,c,s , 1), if valid and finite,
                       ẽp,c,s =                                                              (16)
                                       1,                   otherwise.

For each case, we take b@8                                                             @8
                        p,c = mins=1,...,8 ẽp,c,s . Per-PDE nRMSE@8 is the median of bp,c over
cases. Reported aggregate pass metrics are averaged over PDE prompts and aggregate nRMSE@8 is
the median over PDE prompts (this prevents PDEs with more cases from dominating the aggregate).

E    Additional experimental details and figures




Figure 7: Training reward over RL steps. RLVP training reward increases smoothly across 3B, 7B,
and 14B Qwen2.5-Coder-Instruct models. The curves show that verifier feedback provides a stable
optimization signal after the SFT warm start.




                                                     25
Figure 8: Ablation of physical accuracy reward vs. validity-only reward for 8 seen PDE tasks.
We compare validity-only RL, R = V , against validity plus physical accuracy, R = V Rtraj , for
the 7B model. Here, Rtraj is computed from function-space nRMSE against hidden references.
Validity-only RL attains a similar valid execution rate, but adding Rtraj improves pass@1 (0.71 vs.
0.58), pass@8 (0.84 vs. 0.76), and median best-of-8 nRMSE (6.2 × 10−4 vs. 1.1 × 10−3 ). The
physical accuracy reward improves solution quality beyond executable-code generation.




Figure 9: Ablation of physical accuracy reward vs. validity-only reward for 10 unseen PDE
tasks. On the 10 held-out PDE prompts, adding Rtraj to validity improves valid execution rate (0.45
vs. 0.29), pass@1 (0.10 vs. 0.03), pass@8 (0.33 vs. 0.21), and median best-of-8 nRMSE (1.3 × 10−1
vs. 1.8 × 10−1 ) relative to validity-only RL. The physical accuracy reward is therefore important for
cross-PDE transfer.




Figure 10: Progress of pass@8 evaluation metrics during post-training. Same setup as Figure 2,
but reporting combinatorial pass@8, comparing Base (Qwen2.5-Coder-Instruct), SFT, and RLVP
post-trained checkpoints on the eight seen PDE tasks. Dashed line: Claude Sonnet 4.5 baseline
evaluated with the same k = 8 sampling protocol.




                                                 26
Figure 11: Solver component frequencies across model checkpoints. We parse generated solver
code for numerical-method features. For solver generation on held-out PDE problems, RLVP post-
trained checkpoints tend to more frequently use periodic boundary logic, np.roll-based stencils,
CFL/substep control, and Runge–Kutta time stepping. These features align with the successful
compositional transfer examples in Figure 5 and Appendix F.


F   Additional PDE solution and numerical method compositional transfer
    examples
We show code-level analysis examples for unseen PDE problems such as heat, 2D advection, and
Cahn–Hilliard. For each held-out PDE, we select a representative solver generated by the RLVP
post-trained LLM by success rate and median nRMSE across hidden PDE cases. We then compare it
against the best SFT solver for the same held-out PDE and a corresponding matched seen PDE solver
from RLVP. These examples are intended as possible qualitative evidences of selective numerical-
scheme reuse and adaptation, rather than evidence that the post-trained model can solve arbitrary
unseen PDEs.




                                               27
Figure 12: Dimension lift transfer: 1D advection to 2D advection. The matched seen problem
gives the 1D advection solver generated by the RLVP post-trained model. The held-out RLVP solver
lifts the transport structure to two dimensions using x/y derivative stencils, directional CFL control
with dx and dy, and RK4 time stepping, reaching median nRMSE 5.349 × 10−3 . The SFT model
generated solver is unstable, with median nRMSE 5.185 × 1012 .




Figure 13: Higher-order synthesis: Cahn–Hilliard. The held-out Cahn–Hilliard PDE prompt
requires a fourth-order structure. The solver generated by the RLVP post-trained model constructs
the chemical potential µ = −ϵ2 uxx + u3 − u and applies a second Laplacian, reaching median
nRMSE 2.616 × 10−4 compared with 2.144 × 10−2 for the SFT finetuned model. This suggests that
the post-trained model could adapt familiar finite-difference primitives to assemble the higher-order
operator requested by the prompt.




Figure 14: Diffusion-subset transfer: reaction–diffusion to heat. Heat is the diffusion-only subset
of the seen reaction–diffusion family during SFT and RL. The solver generated by RLVP post-trained
model drops the reaction source while retaining a local periodic Laplacian and explicit substepping,
improving median best-of-8 nRMSE from 2.07 × 10−1 for SFT to 8.11 × 10−5 after RL.




                                                 28
Table 14: Seen PDE problems per-PDE pass@8 and valid execution rate. This table complements
Table 1. Pass@8 measures whether at least one of eight generated solvers succeeds on a case.
Valid execution rate measures execution with correct shape and finite output. Bold marks the best
meaningful value in each row and underline marks the second-best meaningful value.
                                                           3B                  7B                  14B             Claude Sonnet 4.5   Qwen3-Coder-480B    DeepSeek V4 Flash    GPT-OSS-120B        Llama-3.1-405B   Llama-3.3-70B
Section                      Metric                 Base        RLVP    Base        RLVP    Base     RLVP                API                 API                   API               API                 API             API
ID per-PDE Pass@8            advection1d            0.00        1.00    0.00        0.88    0.31         1.00            0.44                0.50                  0.50              0.44                0.00            0.00
                             burgers1d              0.00        0.75    0.00        0.75    0.00         0.75            0.75                0.62                  0.75              0.50                0.50            0.00
                             darcy2d                0.00        1.00    0.00        1.00    0.00         1.00            0.00                0.00                  0.00              0.00                0.00            0.00
                             diffusion-sorption1d   0.00        1.00    0.00        1.00    0.22         1.00            0.00                0.00                  0.00              0.00                0.00            0.22
                             incompressible-ns2d    0.00        0.00    0.00        0.00    0.00         1.00            0.33                0.00                  0.00              1.00                0.00            0.00
                             reaction-diffusion1d   0.00        1.00    0.00        1.00    1.00         1.00            1.00                1.00                  1.00              0.00                1.00            1.00
                             reaction-diffusion2d   0.00        1.00    0.00        1.00    0.00         1.00            1.00                1.00                  1.00              1.00                0.83            0.33
                             shallow-water2d        0.00        1.00    0.00        1.00    0.00         1.00            0.50                0.00                  0.50              0.50                0.00            0.00
ID per-PDE Valid exec rate   advection1d            0.12        1.00    0.72        1.00    0.75         0.75            0.97                1.00                  1.00              1.00                0.53            0.41
                             burgers1d              0.00        1.00    0.12        1.00    0.37         1.00            0.52                0.72                  0.62              0.31                0.33            0.00
                             darcy2d                0.00        0.75    0.00        0.75    0.25         1.00            1.00                0.62                  0.75              1.00                0.25            0.38
                             diffusion-sorption1d   0.00        1.00    0.12        0.88    0.62         1.00            1.00                0.12                  0.96              0.88                0.06            0.12
                             incompressible-ns2d    0.00        0.00    0.00        0.25    0.00         0.62            0.61                0.61                  0.38              0.12                0.00            0.00
                             reaction-diffusion1d   0.12        0.88    0.12        1.00    0.56         1.00            0.59                0.26                  0.96              0.10                0.36            0.25
                             reaction-diffusion2d   0.12        0.75    0.25        1.00    0.04         1.00            0.88                0.38                  0.62              1.00                0.50            0.50
                             shallow-water2d        0.12        0.12    0.00        0.50    0.00         1.00            0.88                0.25                  0.62              0.25                0.12            0.00




Table 15: Aggregate performance on held-out PDE tasks. We report evaluation over 10 unseen
PDE prompts. Best values within each model size are bolded.
                                                                          3B                                                                7B                                                       14B
 Metric                                             Base                 SFT                  RLVP                      Base               SFT              RLVP                Base                 SFT              RLVP
 Pass@1 ↑                                         0.01                   0.03                  0.07                      0.01             0.04               0.11                0.11                 0.14             0.21
 Pass@8 ↑                                         0.12                   0.15                  0.20                      0.06             0.28               0.57                0.40                 0.60             0.50
 Median-best nRMSE@8 ↓                          3.02E-01               3.03E-01             2.64E-01                   4.61E-01         1.45E-01          4.01E-03             3.72E-02            1.32E-03          1.49E-02




Table 16: Unseen PDE performance per-PDE breakdown. This table expands Appendix Table 15
with pass@1, pass@8, nRMSE@8, and valid execution rate for each held-out PDE problem. Bold
marks the best value for each model size and underline marks the second-best value.
                                                                                                                3B                                          7B                                             14B
 Section                                 Metric                                            Base                 SFT             RLVP         Base           SFT            RLVP             Base           SFT           RLVP
 Per-PDE Pass@1                          advection2d                                       0.00                 0.00            0.00         0.00           0.00            0.14            0.00           0.12          0.00
                                         advection-diffusion1d                             0.00                 0.00            0.01         0.00           0.04            0.00            0.00           0.35          0.15
                                         advection-diffusion2d                             0.00                 0.00            0.00         0.00           0.03            0.00            0.38           0.12          0.00
                                         advection-reaction-diffusion1d                    0.00                 0.00            0.00         0.00           0.00            0.25            0.38           0.00          0.09
                                         allen-cahn2d                                      0.03                 0.02            0.00         0.00           0.12            0.12            0.08           0.25          0.38
                                         cahn-hilliard1d                                   0.00                 0.12            0.00         0.00           0.03            0.30            0.21           0.00          0.03
                                         darcy-reaction2d                                  0.00                 0.00            0.00         0.00           0.00            0.00            0.00           0.00          0.00
                                         gray-scott2d                                      0.10                 0.12            0.12         0.00           0.12            0.12            0.08           0.25          1.00
                                         heat1d                                            0.00                 0.00            0.59         0.00           0.00            0.17            0.00           0.25          0.44
                                         kdv1d                                             0.01                 0.00            0.00         0.07           0.00            0.00            0.00           0.00          0.00
 Per-PDE Pass@8                          advection2d                                       0.00                 0.00            0.00         0.00           0.00            0.75            0.00           1.00          0.00
                                         advection-diffusion1d                             0.00                 0.00            0.04         0.00           0.33            0.00            0.00           1.00          1.00
                                         advection-diffusion2d                             0.00                 0.00            0.00         0.00           0.25            0.00            1.00           1.00          0.00
                                         advection-reaction-diffusion1d                    0.00                 0.00            0.00         0.00           0.00            1.00            1.00           0.00          0.75
                                         allen-cahn2d                                      0.25                 0.17            0.00         0.00           1.00            1.00            0.33           1.00          1.00
                                         cahn-hilliard1d                                   0.00                 0.33            0.00         0.00           0.25            1.00            1.00           0.00          0.25
                                         darcy-reaction2d                                  0.00                 0.00            0.00         0.00           0.00            0.00            0.00           0.00          0.00
                                         gray-scott2d                                      0.83                 1.00            1.00         0.00           1.00            1.00            0.67           1.00          1.00
                                         heat1d                                            0.00                 0.00            1.00         0.00           0.00            1.00            0.00           1.00          1.00
                                         kdv1d                                             0.11                 0.00            0.00         0.56           0.00            0.00            0.00           0.00          0.00
 Per-PDE nRMSE@8                         advection2d                                   3.15e-01           3.01e-01          2.63e-01      2.69e-01        1.00e+00        5.35e-03     2.35e-01         1.14e-14       2.91e-01
                                         advection-diffusion1d                         9.26e-01           3.05e-01          9.01e-02      3.29e-01        5.07e-02        2.20e-01     1.50e-01         5.36e-04       5.36e-04
                                         advection-diffusion2d                         2.89e-01           1.33e-01          1.00e+00      1.00e+00        1.34e-01        1.00e+00     1.63e-03         1.63e-03       1.22e-01
                                         advection-reaction-diffusion1d                6.46e-01           4.59e-01          2.65e-01      5.71e-01        5.25e-01        1.50e-03     9.95e-04         1.21e-01       3.90e-03
                                         allen-cahn2d                                  1.59e-02           1.08e-01          2.43e-01      3.52e-01        3.44e-04        3.44e-04     1.70e-02         3.44e-04       2.65e-04
                                         cahn-hilliard1d                               3.58e-02           1.81e-02          1.00e+00      4.17e-02        2.14e-02        2.62e-04     2.82e-04         2.61e-02       1.00e+00
                                         darcy-reaction2d                              6.71e-01           1.00e+00          1.00e+00      1.00e+00        2.00e-01        2.37e-01     1.00e+00         1.00e+00       2.59e-02
                                         gray-scott2d                                  4.54e-03           1.13e-03          1.13e-03      1.00e+00        1.14e-03        2.68e-03     4.50e-03         1.01e-03       1.01e-03
                                         heat1d                                        1.00e+00           3.13e-01          7.39e-05      1.00e+00        2.07e-01        8.11e-05     1.00e+00         1.68e-06       7.39e-05
                                         kdv1d                                         9.49e-02           1.00e+00          1.00e+00      7.50e-03        1.55e-01        1.00e+00     5.75e-02         4.82e-02       1.00e+00
 Per-PDE valid executable rate           advection2d                                       0.25                 0.25            0.12         0.19           0.12            0.88            0.50           0.41          0.28
                                         advection-diffusion1d                             0.12                 0.16            0.31         0.25           0.75            0.29            0.38           0.75          0.72
                                         advection-diffusion2d                             0.38                 0.50            0.00         0.00           0.34            0.00            0.47           0.25          0.69
                                         advection-reaction-diffusion1d                    0.19                 0.12            0.12         0.25           0.25            0.59            0.54           0.75          0.82
                                         allen-cahn2d                                      0.38                 0.25            0.12         0.25           0.24            0.12            0.25           0.75          0.88
                                         cahn-hilliard1d                                   0.12                 0.62            0.00         0.12           0.36            0.69            0.88           0.41          0.06
                                         darcy-reaction2d                                  0.12                 0.00            0.00         0.00           0.25            0.38            0.12           0.02          0.25
                                         gray-scott2d                                      0.12                 0.25            0.12         0.00           0.25            0.38            0.38           0.25          1.00
                                         heat1d                                            0.32                 0.25            0.75         0.00           0.75            0.50            0.00           0.71          0.50
                                         kdv1d                                             0.11                 0.00            0.00         0.25           0.12            0.04            0.14           0.62          0.42




                                                                                                                       29
G    Example Solver Programs Generated by the Post-Trained Policy
In this section, we show example snippets of generated solver codes for evaluated PDE prompts on
the RLVP post-trained 7B model.




Figure 15: Generated solver from the RLVP post-trained model for 1D viscous Burgers. Best
selected solver from the 7B RLVP checkpoint on the seen viscous Burgers task.


                                              30
Figure 16: Generated solver from the RLVP post-trained model for 1D advection. Best selected
solver from the 7B RLVP checkpoint on the seen 1D advection task.




                                            31
Figure 17: Generated solver from the RLVP post-trained model for 1D reaction–diffusion. Best
selected solver from the 7B RLVP checkpoint on the seen reaction–diffusion task.




                                            32
Figure 18: Generated solver from the RLVP post-trained model for 1D diffusion–sorption. Best
selected solver from the 7B RLVP checkpoint on the seen diffusion–sorption task.




                                            33
Figure 19: Generated solver from the RLVP post-trained model for 2D reaction–diffusion. Best
selected solver from the 7B RLVP checkpoint on the seen 2D reaction–diffusion task.




                                            34
Figure 20: Generated solver from the RLVP post-trained model for 2D Darcy flow. Best selected
solver from the 7B RLVP checkpoint on the seen Darcy flow task.


                                             35
Figure 21: Generated solver from the RLVP post-trained model for 2D shallow water equations.
Best selected solver from the 7B RLVP checkpoint on the seen shallow water task.




                                            36
Figure 22: Generated solver from the RLVP post-trained model for 2D incompressible Navier–
Stokes. Best selected solver from the 7B RLVP checkpoint on the seen incompressible Navier–Stokes
task.

                                               37
H    Catalog of example PDE solutions calculated from LLM generated PDE
     solver codes




Figure 23: Burgers 1D solutions example for the steeper-multimode initial condition with ν = 0.1.




Figure 24: Diffusion–sorption 1D solutions example for the uniform initial condition with D = 10−4 ,
kf = 3.5 × 10−4 , nf = 0.874, por = 0.29, ρs = 2880, and sol = 1.




Figure 25: Reaction–diffusion 1D solutions example for the front-like initial condition with ν = 0.5
and ρ = 1.




       Figure 26: Darcy 2D solutions example for the channel diffusion field with β = 0.1.




Figure 27: Advection–reaction–diffusion 1D solutions (unseen PDE) example for the front-like initial
condition with β = 1, ν = 0.02, and ρ = 2.



                                                38
Figure 28: Heat 1D solutions (unseen PDE) example for the single-sine initial condition with ν = 0.1.




                                                 39
Figure 29: Allen–Cahn 2D solutions (unseen PDE) example for the mixed-waves initial condition
with ϵ2 = 0.005 and ρ = 2.




                                             40
I   Prompt Examples
This appendix gives representative examples of the three prompt forms used in the multi-PDE training
corpus described in Section 3.2. The system message instructs the model to return only Python code
and no explanatory text. Each prompt specifies a fixed solver interface and output convention so that
generated programs can be evaluated uniformly by the verifier.

Generic prompt. The generic form states the PDE and function signature, while leaving coefficients
and data as runtime hidden inputs for each case. This encourages the generated solvers to remain
robust across parameter values supplied during execution.

 Write Python code only.

 Define exactly:
     def solver(u0_batch, t_coordinate, beta):

 Solve the PDE
     u_t + beta * u_x = 0
 on x in [0,1) with periodic boundary conditions.

 Requirements:
 - You may use NumPy and/or SciPy
 - do not print anything
 - do not access files or the network
 - output only Python code
 - Return a NumPy array of shape [B, T, N].
 - u0_batch has shape [B, N] and contains periodic initial conditions on a uniform 1D grid.
 - t_coordinate has shape [T] and gives the exact output times that must be returned.
 - beta is the scalar advection speed.
 - returned slice n must correspond to time t_coordinate[n]
 - internal substeps are allowed if needed for stability or accuracy


             Figure 30: Example generic prompt used in the 1D linear advection task.


Parameter-conditioned prompt. The parameter-conditioned form additionally specifies numerical
values of the PDE coefficients. This allows the generated solver to specialize numerical-method
choices to the parameter regime, such as diffusion-dominated versus reaction-dominated dynamics.




                                                 41
 Write Python code only.

 Define exactly:
     def solver(u0_batch, t_coordinate, nu, rho):

 Solve the PDE
     u_t = nu * u_xx + rho * u * (1 - u)
 on x in [0,1) with periodic boundary conditions.

 For this task:
 - nu = 5
 - rho = 10

 Requirements:
 - You may use NumPy and/or SciPy
 - do not print anything
 - do not access files or the network
 - output only Python code
 - Return a NumPy array of shape [B, T, N].
 - u0_batch has shape [B, N] and contains 1D initial conditions on a uniform periodic grid.
 - t_coordinate has shape [T] and gives the exact output times that must be returned.
 - nu is the diffusion coefficient and rho is the reaction coefficient.
 - returned outputs must align with the requested times in t_coordinate
 - internal substeps are allowed if needed for stability or accuracy


    Figure 31: Example parameter-conditioned prompt used in the 1D reaction–diffusion task.


Parameter and initial condition conditioned prompt This prompt additionally describes the struc-
ture of the input data, particularly the initial conditions. For steady-state problems, this conditioning
may refer to coefficient fields rather than initial conditions.

 Write Python code only.

 Define exactly:
     def solver(diffusion_batch, beta):

 Solve the PDE
     -div(a(x,y) grad u) = beta
 on (x,y) in [0,1]^2 with zero Dirichlet boundary conditions.

 For this task:
 - beta = 100
 - the permeability fields come from a channelized family

 Requirements:
 - You may use NumPy and/or SciPy
 - do not print anything
 - do not access files or the network
 - output only Python code
 - Return a NumPy array of shape [B, Nx, Ny] containing the steady-state solution field.
 - diffusion_batch has shape [B, Nx, Ny] and contains heterogeneous permeability fields
      a(x,y).
 - beta is the scalar forcing term.
 - internal substeps are allowed if needed for stability or accuracy


Figure 32: Example parameter and initial condition conditioned prompt used in the 2D Darcy flow
task with channelized permeability fields.


Sampling weights and per-PDE coverage. The three prompt forms are sampled with fixed weights
0.5 (generic), 0.35 (parameter-conditioned), and 0.15 (parameter-and-IC-conditioned). The training
split contains 512 scenarios, with 237/187/88 generic/parameter-conditioned/parameter-and-IC-
conditioned rows, specifically. Per-PDE prompt counts are reported in Table 17.


                                                  42
Table 17: Per-PDE prompt counts in the training corpus, broken down by prompt form.
           PDE                      Generic   Param.   Param.+IC   Total
           advection1d                   30       29           9     68
           burgers1d                     35       20           8     63
           reaction_diffusion1d          36       21           6     63
           diffusion_sorption1d          25       20          11     56
           reaction_diffusion2d          34       22          13     69
           darcy2d                       27       29          12     68
           incompressible_ns2d           29       23          14     66
           shallow_water2d               21       23          15     59
           Total                        237      187          88    512




                                        43
