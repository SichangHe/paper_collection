                                          Your Simulation Runs but Solves the Wrong Physics:
                                                 PDE-Grounded Intent Verification for
                                            LLM-Generated Multiphysics Simulation Code


                                                                    Zhenghan Song∗                                       Yulong Liu∗†
                                                                    Cornell University                                 Cornell University
arXiv:2605.09360v1 [cs.LG] 10 May 2026




                                                                      Cheng Wan                                          Chenjun Li
                                                                    Cornell University                                 Cornell University

                                                                      Lingfu Liu                                         Yunyi Li
                                                                   Cornell University                                Columbia University

                                                                                        Congcong Yuan
                                                                     Harvard University & Nanyang Technological University



                                                                                                  Abstract
                                                      Execution-based evaluation of LLM-generated code implicitly treats successful
                                                      execution as a proxy for correctness. In scientific simulation, this proxy is insuffi-
                                                      cient: a generated input file can run, mesh, and converge while encoding governing
                                                      equations that differ from the user’s intent. We call this mismatch between intended
                                                      physics and generated code the comprehension–generation gap. We instantiate
                                                      this in MOOSE, where Kernel and BC objects map compositionally to weak-form
                                                      residual terms, enabling deterministic reconstruction of the encoded PDE and
                                                      comparison against an intended contract. We formalize this comparison as the
                                                      Intent Fidelity Score (IFS), a structural metric covering governing terms, BCs,
                                                      ICs, coefficients, and time scheme. Building on IFS, we develop a PDE-grounded
                                                      refinement loop that uses deterministic violation reports to correct generated code
                                                      iteratively. We evaluate on MooseBench, a 220-case multiphysics benchmark with
                                                      PDE-level ground truth released with this work. On this benchmark, our method
                                                      consistently improves mean IFS over direct generation, with gains concentrated on
                                                      hard cases. On the subset where direct generation falls below IFS 0.7, refinement
                                                      adds +0.22 to +0.41 absolute IFS. In the deployment audit, execution-only repair
                                                      improves execution success while leaving 39–40% of all 220 cases runnable but
                                                      still solving the wrong physics across the three main deployment-audit models,
                                                      exposing executability and intent fidelity as separable failure modes. Static proof-
                                                      of-concept experiments on four PDE-oriented DSLs (UFL/FEniCS, FreeFEM,
                                                      FiPy, and Devito) suggest that the reconstruction-and-comparison pattern extends
                                                      beyond MOOSE. These findings reinforce that executable simulation code should
                                                      be verified against the mathematical structure it is intended to encode, not accepted
                                                      on execution alone.


                                             ∗       Joint first authors. Yulong Liu and Zhenghan Song contributed equally. The order of the joint first authors
                                                     was determined by a coin flip.
                                             †       Correspondence to: Yulong Liu, yl3825@cornell.edu.


                                         Preprint.
                                       2
                                                 (a) Cavity-boundary error         2
                                                                                             (b) Missing source term          2
                                                                                                                                        (c) Wrong diffusivity field         (d) Transient solved as steady-state 2
                                                                                                                                                                            2
                                                                                                                                                                                                                                  (e) Wrong initial condition           1.00




Erroneous solution Intended solution
                                            Correct: no-flux cavity wall                Correct: source/sink included              Correct: heterogeneous D(x)                   Correct: finite-time transient              Correct: transient IC


                                       0                                           0                                          0                                             0                                           0




                                                                                                                                                                                                                                                                           Normalized concentration c
                                                                                                                                                                                                                                                                        0.75


                                       2                                           2                                          2                                             2                                           2
                                                                                                                                                                                                                                                                        0.50
                                       2                                           2                                          2                                             2                                           2
                                            Wrong: absorbing cavity wall                Wrong: source/sink omitted                 Wrong: homogeneous D                          Wrong: steady-state solve                   Wrong: incorrect initial condition


                                       0                                           0                                          0                                             0                                           0                                               0.25



                                       2                                           2                                          2                                             2                                           2                                               0.00
                                           3.5                    0.0        3.5       3.5                  0.0         3.5       3.5                  0.0            3.5       3.5                    0.0        3.5       3.5                      0.0          3.5
                                                                  x                                          x                                         x                                                x                                            x




          Figure 1: Silent-failure gallery for cavity diffusion simulations. Panels show runnable simulations
          that produce plausible fields while violating the intended specification: (a) cavity boundary condition,
          (b) source/sink term, (c) diffusivity field, (d) transient formulation, and (e) initial condition.


            1                                    Introduction

           The dominant evaluation paradigm for LLM-generated code relies on execution-based testing, where
           successful execution is often taken as evidence of functional correctness. In scientific computing,
           however, the relevant specification is a mathematical model of the underlying physics rather than
           merely input–output behavior. Execution checks can verify syntactic validity and runtime stability, but
           they cannot determine whether the generated code faithfully encodes the intended governing equations
           and physical assumptions. We define this structural alignment between generated simulation code
           and the intended physical specification as intent fidelity, which serves as the central criterion for
           evaluating scientific simulation code in this work.
          Multiphysics simulation is central to engineering design and scientific discovery, especially when
          experiments are prohibitive [4]; in safety-critical settings such as nuclear reactor operation, silently
          solving the wrong PDE can affect estimates of maximum sustainable core power [15]. Multiphysics
          Object-Oriented Simulation Environment (MOOSE) [26] is a widely used open-source finite-element
          platform where simulations are specified by structured input files declaring meshes, variables,
          kernels, boundary conditions, materials, and solvers. Since kernels encode weak-form residual
          contributions, constructing intent-faithful MOOSE inputs requires mapping a physical scenario to the
          correct combination of MOOSE objects. Figure 1 illustrates five such silent failures that converge
          without warning, indistinguishable from correct simulations under execution-based metrics (details
          in Appendix A).
            Recent LLM-based systems generate scientific simulation code from natural language, including
            MOOSEnger for MOOSE, MetaOpenFOAM for CFD, and AutoFLUKA for radiation transport [16,
            6, 21]. These systems reduce the expertise required to initiate simulations, but their evaluation largely
            centers on executability, conflating syntactic validity with intent fidelity. DPIaC-Eval shows a similar
            deployment–intent gap (95.5% deployment success vs. 25.2% intent satisfaction) [28]; the same
            failure mode appears in MOOSE (Appendix J).
          We identify this as a comprehension–generation gap: LLMs may explain the governing physics
          correctly, yet fail to encode all required terms in executable simulation code. MOOSE makes this
          gap structurally verifiable: each Kernel or BC object contributes a specific weak-form or boundary
          term, so the active object set determines a compact PDE-level representation of the generated input.
          This enables intent alignment: reconstructing the PDE encoded by generated code and comparing
          it with the user-intended PDE. This raises a concrete question: can the physics encoded in LLM-
          generated simulation code be verified automatically against the user’s intended PDE, without relying
          on execution or the model’s own judgment?
            Our central contribution is a physics-level diagnostic layer for LLM-generated MOOSE simulations:
            a framework that exploits MOOSE’s explicit mathematical semantics rather than attempting general-
            purpose program verification. Around this layer, we make four contributions:

                                                   1. Silent physics failures and MooseBench. We show that LLM-generated simulations can
                                                      execute while encoding incorrect physics, and introduce MooseBench, a 220-case audited
                                                      benchmark spanning seven physics families with PDE-level ground truth.


                                                                                                                                                             2
      2. Deterministic PDE reconstruction and IFS. We formalize the kernel↔weak-form corre-
         spondence, reconstruct the PDE encoded by MOOSE inputs, and define IFS as a weighted
         structural-fidelity metric with actionable violation reports.
      3. Contract-guided generation and refinement. We use structured physics contracts as
         interfaces between intent understanding and code generation, with deterministic violation
         reports enabling targeted refinement beyond execution-only feedback.
      4. Portability and boundary analysis. We extend the reconstruction and comparison pattern
         to UFL/FEniCS, FreeFEM, FiPy, and Devito as proof-of-concept demonstrations. We also
         report MCS as a limitation-aware diagnostic for the coefficient/material blind spots that
         structural IFS does not cover.

2     Related Work
LLM systems for simulation code. A growing line of work applies LLMs to scientific simulation
code generation. MOOSEnger [16] generates MOOSE inputs through a multi-agent pipeline, and
MechAgents [22] uses a similar architecture for mechanics. MetaOpenFOAM [6] targets CFD,
and AutoFLUKA [21] targets Monte Carlo radiation transport. All four rely on execution-based
validation, equating a successful run with functional correctness. We show this signal is insufficient:
a MOOSE input can execute and converge while encoding a PDE different from the one specified.

Verifying generated code against user intent. Intent verification for generated code has been
studied through specification-based translation [27], step-wise verifiers that ask whether each gener-
ated step matches user intent [8], and policy-guided verifier feedback for Infrastructure-as-Code [12].
These methods require the verifier itself to reason about correctness, whether through formal proof
obligations, LLM critique, or learned policies. We instead exploit MOOSE’s compositional structure,
where each Kernel and BC object contributes a fixed weak-form term, reducing verification to a
deterministic structural comparison between two PDE objects. Our diagnostic also sits upstream of
traditional simulation V&V [23], which assumes the input file already encodes the correct equations.

Self-refinement and PDE representations. LLM self-refinement methods iteratively improve
generated code via the model’s own critique [20] or runtime traces [5]. These signals are themselves
produced by the same model that generated the code, leaving them exposed to the comprehension–
generation gap we identify. Our refinement instead feeds the LLM a deterministic, structurally
computed PDE discrepancy, so missing or extra terms are surfaced explicitly regardless of whether the
model would detect them. Prior machine-readable PDE representations [13, 17, 1] encode equations
as inputs to models that solve equations, generate code, or constrain physics-aware learning [19, 18].
Our representation supports verification, which only requires deterministic comparison between two
discrete structures and admits a coarser classification-level descriptor.

3     MOOSE Semantics and Silent Physics Failures
3.1   MOOSE Framework: Kernels as Weak-Form Residual Terms

The MOOSE framework [26] solves systems of partial differential equations with the finite element
method. Its core abstraction is the Kernel, a modular object representing a domain contribution to the
weak form; boundary integrals are handled separately by boundary-condition objects. For example,
the weak form of the zero-gravity Darcy pressure equation can be written as
                                                             
                                       K              K
                                  ∇ψ, ∇p − ψ, ∇p · n̂ = 0.                                         (1)
                                       µ               µ
                               |      {z      } |        {z      }
                                   Kernel        Boundary Condition

The detailed derivation of (1) and its corresponding MOOSE input file structure are given in Ap-
pendix B. For the representative Kernels covered in Table 6, enumerating the active Kernel and
boundary-condition objects in a MOOSE input file reconstructs its encoded weak-form residual for
intent-fidelity comparison. Figure 2 illustrates this mapping on a coupled thermomechanical example.


                                                  3
MOOSE objects as semantic macros. We use                                                Weak-Form Physics             MOOSE Objects
semantic macro informally to describe a MOOSE                                           PDE Weak-Form Terms          MOOSE Kernels / BCs




                                                              User's intended physics




                                                                                                                                           Code-encoded physics
object as a named, reusable unit of PDE semantics.                                             cp Tt d         1:1       HeatConduction
                                                                                                                         TimeDerivative
Instantiating an object correctly means satisfying its                                                         1:1
schema, such as required parameters and valid types;                                          k T     d                  HeatConduction


however, this only checks that the object can exist in                                           :   d         1:1      StressDivergence
                                                                                                                            Tensors
the input file. Intent fidelity asks a different question:                                                      1:1
                                                                                            T = g on D                     DirichletBC
whether the chosen objects collectively encode the
                                                                                            Deterministic term-by-term correspondence
weak-form structure intended by the user.
To make this structure explicit, term comparison is
                                                        Figure 2: Weak-form terms map to MOOSE
keyed by the variable and a normalized PDE opera-
                                                        Kernel/BC objects.
tor type drawn from the kernel–PDE mapping table.
As a structural witness for each operator type, the table additionally records a descriptor

               (τ, ϕ, γ) ∈ Otrial × Otest × G,       |Otrial | = 8,                         |Otest | = 4,            |G| = 3,

capturing the operator on the trial-side quantity, the operator on the test function, and their contraction.
This two-level representation makes operator-type assignments auditable against the underlying
weak-form contributions rather than taken on faith. Thus, for the covered fragment, reconstruction
reduces MOOSE objects to bound normalized PDE terms plus BC, IC, coefficient/material, and
time-scheme facts; the full formalization appears in Appendix G.


4     PDE-Grounded Intent Verification and Generation

4.1   Problem Formulation

Given a natural-language description d of a physical simulation, the task is to generate MOOSE input
code c that faithfully encodes the intended physics. We measure fidelity by comparing the physics
contract deterministically reconstructed from c against a reference physics contract. Let Pcode (c)
denote the contract reconstructed from code c, and let Pref denote the comparison reference: Pgt
during benchmark evaluation and Pllm during deployment-time refinement. We use Pcand for a
generic candidate contract. The resulting score is

                          IFS(Pref , Pcode (c)) = 1 − ∆phys (Pref , Pcode (c)) ,                                                                                  (2)

where ∆phys is the weighted checkpoint discrepancy defined in Section 4.3, so higher IFS indicates
fewer mismatches in the reconstructed physics.

4.2   PDE Formal Representation

We use a compact representation for the physics encoded by a MOOSE input:

                                        P = (T , B, I, C, S, Ω) ,                                                                                                 (3)

where T contains governing-equation terms, B boundary conditions (BCs), I initial conditions (ICs),
C coefficient/material facts, S the time scheme, and Ω the domain specification. We call this tuple a
physics contract when it is used as the reference for synthesis or evaluation. We use the subscript
convention introduced in Section 4.1 for ground-truth, LLM-extracted, code-reconstructed, reference,
and candidate contracts.
Reconstruction is deterministic for the covered MOOSE fragment: each active Kernel is mapped
by M to a normalized PDE operator type, an optional descriptor witness, a coefficient extraction
rule, and a severity weight; BCs and ICs are normalized analogously. The term set T is keyed by
variable and normalized operator type. The mapping is sufficient for the MooseBench coverage;
uncovered kernel–term instances are tracked in U and excluded from IFS computation. Exact
coverage statistics appear in Appendix G and Table 6. The full mapping and reconstruction algorithm
appear in Appendices E and C (Algorithm 1).


                                                       4
                                                                            PDE-Refine Workflow
                                                                                    ⚙ Deployment-time pipeline
                                                                                   Solid data · data flow available during generation
                                      STAGE 1                         LLM               STAGE 2                               LLM              STAGE 3                          No LLM

                                                     PDE Extraction                                          Spec-Guided
                                 PDE Reconstruction
                                                                                                              Synthesis                                                                            offline only
          Natural-language
              prompt d
              user input                       terms · BCs · ICs ·                              contract acts as checklist:                          parse AST · enumerate active
                                           coefficients · time scheme                         term → kernel · BC → BC block                       Kernels, BCs, ICs · apply mapping M
                                          explicit, inspectable contract                 [Mesh] [Variables] [Kernels] [BCs] …                     deterministic, no model in the loop


                                                          STAGE 4                        IFS Verification                                No LLM       IFS ≥ τ               Accept
                                                                                                                                                                            final MOOSE code
           refinement feedback                                        checkpoints: terms · BCs · ICs · coefficients · time scheme
          re-synthesize with violations                            deterministic comparison · variable alignment by operator signature
           until IFS ≥ τ or N_max iters                                                                                                                                Benchmark-only evaluation
                                                                                                         IFS < τ                                                                        offline only
                                                                                                                                                                           dashed: NOT visible to extractor /
                                                                                                                                                                                 synthesizer / refiner
                                                                                 Structured Violation Report
                                                                  missing/mismatched terms · BCs · ICs · coefficients · time scheme
                                                              !
                                                                     deterministic, machine-computed — not LLM self-critique                                             expert-authored                Offline IFS
                                                                  e.g., add TimeDerivative for T; change DirichletBC on right to NeumannBC                                  benchmark
                                                                                                                                                                           ground truth                  MooseBench
                                                                                                                                                                                                          tables only



                       Baseline (Direct)                                                                               Ours (PDE-Refine)
                       NL → code (one-shot, no PDE-level verification)                                                 NL →         → code →          → IFS → (refine if < τ)


Figure 3: System architecture. The deployment-time loop extracts Pllm , synthesizes MOOSE code,
reconstructs Pcode , and feeds deterministic IFS violations back for refinement. Offline benchmark
evaluation uses Pgt only after generation; it is never available to the extractor, generator, or refiner.

4.3   Intent Fidelity Score (IFS)

IFS compares a reference physics contract Pref with a candidate Pcand through checkpoints Q(Pref )
induced by the reference. We first define the weighted physics discrepancy:
                                           P
                                              j∈Q(Pref ) wj · 1[failj (Pref , Pcand )]
                   ∆phys (Pref , Pcand ) =             P                               .      (4)
                                                          j∈Q(Pref ) wj
The reported fidelity score is its complement:
                            IFS(Pref , Pcand ) = 1 − ∆phys (Pref , Pcand ).                       (5)
where wj > 0 is the importance weight of checkpoint j, and 1[failj ] indicates a checkpoint mismatch.
Checkpoints cover terms, BCs, ICs, direct coefficient attributes represented in the contract, and
time scheme; variables are aligned by signatures over normalized PDE operator types, so naming
differences do not affect the score. Severity weights emphasize equation-structure errors and assign
lower weights to parameter-level mismatches. Details on variable alignment, operator-type matching,
descriptor auditing, and severity weights are provided in Appendix G.
IFS is a structural fidelity score, not a physical validity certificate. It does not assess mesh adequacy,
solver convergence, discretization error, or coefficient magnitudes hidden in complex material chains.
We use the Material Consistency Score (MCS) as a conditional secondary diagnostic for explicit
coefficient/material facts when comparable facts are available; Appendix F defines and scopes this
diagnostic. Within the covered MOOSE semantic fragment, IFS is exact over the induced checkpoints.
The representation-relative guarantee and proof appear in Appendix G (Theorems G.1 to G.3).

4.4   Error-Guided Refinement

Before refinement, the system factors synthesis as d → Pllm → c: the extracted contract lists
governing terms, BCs, ICs, coefficients/material facts, and time scheme, and code generation uses
it as a checklist for MOOSE synthesis. After code generation, the system reconstructs Pcode and
compares it with Pllm . If IFS < τIFS , a structured violation report in the candidate’s own variable
names is fed back to the LLM for targeted correction; the loop repeats until convergence or Nmax
iterations (Figure 3). The feedback is computed by deterministic physics-contract comparison.

5     MooseBench: A PDE-Grounded Multiphysics Benchmark
We construct MooseBench, a 220-case benchmark for AI-assisted multiphysics code generation
with deterministic PDE-level ground truth. The benchmark spans seven physics families and three


                                                                                                                5
complexity tiers; the full family distribution and tier definitions are reported in Appendix O (Table 17).
Prompts vary in verbosity and engineering context, but each is well-posed enough to determine the
target PDE, boundary/initial conditions, coefficients, geometry, and time scheme.

5.1   Ground Truth Construction and Audit

For each prompt, an expert-written reference MOOSE input encodes the intended governing equations,
BCs, ICs, material properties, and time scheme. Applying the deterministic reconstruction in
Section 4.2 gives Pgt . To avoid circularity, the audit reviews the prompt, reference input, and
reconstructed Pgt jointly, checking prompt faithfulness, operator coverage, BC/IC consistency,
material and time-scheme consistency, and prompt leakage. Kernel variants are canonicalized to
normalized PDE operator types by the mapping table, and all benchmark artifacts are released in the
supplementary material.

6     Experiments
6.1   Experimental Setup

LLMs. We evaluate four LLMs spanning capability tiers and providers: Claude Sonnet 4.6 (An-
thropic) [3], GPT-5.4 and GPT-4.1-mini (OpenAI) [25, 24], and DeepSeek V4 Flash (DeepSeek) [7],
all at temperature = 0. Sonnet 4.6, GPT-5.4, and DeepSeek V4 Flash form the main sweep; GPT-4.1-
mini serves as a weak-model case study. Two additional models appear in appendix experiments only.
Claude Haiku 4.5 [2] appears in the weak-model registry stress tests, and Gemini 3.1 Flash Lite [9]
appears in both the mixed-model ablation and weak-model stress tests (Appendix P).

Method variants. We organize variants by the feedback source available to the generator. Direct
maps the prompt directly to MOOSE code. SpecGen first extracts an intermediate Pllm contract and
uses it as a synthesis checklist, but receives no deterministic comparison feedback. PDE-Refine adds
deterministic reconstruction: the generated code is mapped to Pcode , compared against Pllm , and
corrected using the resulting IFS violation report.
The execution audit holds the object-realization registry (Appendix H.1) frozen and varies only
the feedback signal: Exec-Repair+Reg receives runtime-log feedback, while PDE-Reg receives
PDE/IFS feedback. Official-document retrieval is reported separately as a secondary access control.

Key hyperparameters. We use Nmax = 2 refinement iterations, IFS convergence threshold τIFS =
0.85, and coefficient relative tolerance δcoef = 0.1. Each PDE refinement step uses a regression
guard that accepts refined code only when IFS improves. The full reproducibility manifest, including
registry-repair settings, the InitExec2 definition, and convergence diagnostics, is in Appendix H
(Table 11) and Appendix P (Figure 7).

6.2   Main Results

Table 1 reports the 220-case standard non-registry sweeps (parse failures scored as IFS = 0). All
three main models are compared under identical Direct/SpecGen/PDE-Refine configurations. Under
structural-uniform checkpoint weights, PDE-Refine gains remain positive for all three sweeps; full
deltas are reported in Appendix P (Table 18).
Table 2 reports the controlled deployment audit. Exec uses InitExec2: an output is accepted if
MOOSE exits with code 0, a solve starts before the first error, or no error appears within 2 seconds—
an object-realization signal, not a convergence certificate. GoodExec is the fraction of all 220 cases
passing Exec with IFS ≥ 0.85; FalseExec is the fraction passing Exec with IFS < 0.85.
Finding 1: PDE-grounded physics contracts raise fidelity most where direct generation is weak.
Tables 1 and 12 show that PDE-Refine improves the standard semantic sweeps, with the largest gains
on weaker models and IFSDirect < 0.7 hard cases.
Finding 2: executability and intent fidelity are separable. Table 2 shows that, under the same
frozen registry, PDE-Reg reduces FalseExec and increases GoodExec relative to execution-only repair:
object-realization infrastructure can make simulations run, while PDE-grounded feedback is needed
to reduce runnable-but-wrong outputs. PDE-Reg also raises Exec itself relative to Exec-Repair+Reg


                                                    6
Table 1: 220-case standard non-registry MooseBench results. IFS is the unconditional mean over all
cases with parse failures counted as 0; entries report mean ± 95% bootstrap half-width over case IDs.
Bold indicates the best deployable method within each sweep.

                 LLM                     Direct              SpecGen       PDE-Refine
                 Claude Sonnet 4.6    0.744±0.032        0.800±0.023      0.816±0.021
                 GPT-5.4              0.756±0.033        0.769±0.028      0.802±0.025
                 DeepSeek V4 Flash    0.599±0.048        0.668±0.045      0.782±0.031

Table 2: Deployment audit: PDE feedback vs. execution-only feedback under the same frozen
object-realization registry. IFS is unconditional mean IFS; GoodExec and FalseExec are fractions of
all cases, not conditional fractions among executed cases.

          LLM                  Method                  IFS     Exec      GoodExec      FalseExec
          Claude Sonnet 4.6    Exec-Repair+Reg     0.753       83.2%      43.2%         40.0%
          Claude Sonnet 4.6    PDE-Reg             0.854       91.4%      60.0%         31.4%
          GPT-5.4              Exec-Repair+Reg     0.757       82.3%      42.3%         40.0%
          GPT-5.4              PDE-Reg             0.839       86.8%      56.8%         30.0%
          DeepSeek V4 Flash    Exec-Repair+Reg     0.626       74.1%      35.0%         39.1%
          DeepSeek V4 Flash    PDE-Reg             0.824       87.7%      60.0%         27.7%


in weaker-model stress tests (GPT-4.1-mini 25.5% → 63.2%, Gemini 3.1 Flash Lite 51.8% → 85.0%;
Table 22). This is consistent with PDE-grounded feedback producing more self-consistent variable,
kernel, BC, and material references, leaving the frozen registry fewer mechanical gaps to resolve
(Appendix M).

Official-document access control. We use official-document retrieval as a secondary control, not a
main method family. It improves Direct IFS (0.599 to 0.672), but documentation plus execution-only
repair mainly raises Exec while leaving a large runnable-but-wrong region (38.2% FalseExec). With
the same documents and frozen registry, Docs+PDE-Reg reaches the best IFS and GoodExec in this
control (Table 3), supporting the same conclusion: documentation helps object realization, while
PDE-level feedback drives the fidelity gain. Leakage controls are reported in Appendix D.

Table 3: Official-document access control on the full 220-case DeepSeek V4 Flash setting. Exec uses
InitExec2; GoodExec and FalseExec are fractions of all cases.

                    Method              IFS       Exec        GoodExec     FalseExec
                    DocsDirect          0.672     41.8%        25.5%        16.4%
                    Docs+ExecRepair     0.660     74.1%        35.9%        38.2%
                    Docs+PDE-Reg        0.816     87.3%        58.6%        28.6%


Weak-model stress test. We report GPT-4.1-mini, Claude Haiku 4.5, and Gemini 3.1 Flash Lite as
appendix stress tests rather than main deployment-audit models. They follow the same qualitative
pattern, with PDE-Reg improving fidelity and GoodExec over execution-only repair despite lower
absolute model capability (Appendix P, Table 22).

6.3   Error Analysis

Direct generation primarily fails through BC mismatches and missing/extra terms, especially in
weaker models; coefficient, IC, and time errors are secondary. BC failures rarely occur alone;
most co-occur with term, time, or coefficient errors. Coefficient/material-only cases retain high
IFS and motivate MCS as a secondary diagnostic. Per-model taxonomy, BC co-attribution, and
family/sub-dimensional breakdowns appear in Appendix P (Tables 20, 21, 24, 26).

Error detection coverage. Table 4 quantifies the IFS detection boundary for Direct outputs. Of
766 imperfect parsed Direct outputs, 87.5% contain a structural component (term, BC, IC, or time


                                                   7
Table 4: Error category breakdown under Direct generation (three main sweeps plus the GPT-4.1-mini
stress sweep; n=766 imperfect outputs). IFS detects structural errors; coefficient/material-only errors
motivate MCS as a complementary diagnostic.

                Error Category                       %      Mean IFS   IFS Detects?
                Structural only (term/time/IC)     7.4%       0.60     Yes
                BC only                           14.4%       0.74     Yes
                Structural + coefficient          32.8%       0.64     Yes (structural)
                Mixed structural                  32.9%       0.25     Yes
                Coefficient/material only         12.5%       0.94     No (structural); MCS

Table 5: Cross-DSL proof-of-concept results (DeepSeek V4 Flash). “Deploy” uses Direct generation
when IFSDirect ≥ 0.7 and physics-contract generation otherwise. ∆hard is the PDE-Refine−Direct
improvement on the hard subset (IFSDirect < 0.7).

      DSL         Slice                      n     Direct    PDE-Refine   Deploy      ∆hard    nhard
                  Five-family                25    0.779       0.779       0.851      +0.455     4
      UFL         Hard-stress                30    0.580       0.749       0.791      +0.486    13
                  Documentation-source       12    0.857       0.984       0.984      +0.764     2
      FreeFEM     Documentation-source       11    0.862       0.926       0.919      +0.207     3
      FiPy        Documentation-source        7    0.769       0.943       0.933      +0.574     2
      Devito      Documentation-source        9    0.793       0.831       0.829      +0.109     3
       FreeFEM/FiPy/Devito combined          27    0.815       0.899       0.893      +0.262     8



scheme error) that IFS detects through the reconstructed physics contract. The remaining 12.5% are
coefficient/material-only cases: their mean IFS remains high because the mismatch is not a structural
PDE discrepancy, motivating MCS as a conditional diagnostic for comparable coefficient/material
facts (Appendix F).

6.4   Cross-DSL Generalization

We instantiate the same P-reconstruction/IFS engine on UFL/FEniCS [1], FreeFEM [11], FiPy [10],
and Devito [14] via framework-specific parsers and static analysis (no runtime execution). Table 5
reports documentation-derived slices and a UFL stress-test slice. The configured deployment setting,
which uses physics contract generation only when IFSDirect < 0.7, improves the eight hard non-
UFL cases by a mean IFS of +0.262, with the strongest gains on FiPy advection and FreeFEM
Robin/Helmholtz cases (where DSL syntax differs from typical training data). Adoption requirements
per framework are summarized in Table 19.


7     Discussion

7.1   Empirical Validation: IFS Detects Structural Physics Errors

Figure 4 summarizes the empirical mechanism. Panel (a) shows that PDE extraction quality predicts
final code fidelity: cases with high Pllm fidelity also achieve high final IFS, supporting the extraction–
synthesis factorization underlying mixed-model transfer (Section 7.2). Panel (b) shows that PDE-
Refine gains concentrate in low-Direct-IFS cases, with the trend curve approaching the maximum
possible gain 1 − IFSDirect in the hard regime.
To validate that IFS captures physically meaningful differences, not merely syntactic discrepancies, we
construct 30 MOOSE-executed perturbation pairs spanning structural, boundary-value, and coefficient
errors. The set combines controlled edits with perturbations applied to real MooseBench ground-truth
files, matching the observed LLM error taxonomy (Table 20). Both versions are run through MOOSE,
and we report the final-field relative error EL2 on the common output grid (definition in Appendix F).
All simulations converge successfully, while execution-based testing detects none of these physics
errors.


                                                      8
                             (a) Extraction quality                                                                                     (b) Conditional benefit
                       1.0                                                                                                       1.00
                                   Sonnet                                                                                                       max possible gain                                   Sonnet
                                   DeepSeek V4 Flash                                                                                                                                                DeepSeek V4 Flash
                                                                                                                                 0.75
                       0.8




                                                                                                              PDE-Refine gain
      Final code IFS
                                                                                                                                 0.50
                       0.6
                                                                                                                                 0.25
                       0.4
                                                                                                                                 0.00

                       0.2                                                                                                      −0.25

                       0.0                                                                                                      −0.50
                             0.0            0.2             0.4               0.6     0.8               1.0                             0.0             0.2                0.4              0.6     0.8           1.0
                                                             Extraction IFS                                                                                                      Direct IFS



Figure 4: Compact PDE-pipeline diagnostics for two representative 220-case sweeps. (a) PDE
extraction quality predicts final code fidelity; the dotted diagonal is the y = x reference, not a fitted
trend. (b) PDE-Refine gains concentrate in low-Direct-IFS cases; trend curves summarize rolling
means, and the dotted ceiling marks the maximum possible gain 1 − IFSDirect .

                             (a) IFS structural-error detection                                                                         (b) MCS coefficient blind-spot repair
                       2.0                                                                                                        1.0
                                   Structural                                                                                                 No mismatch           Material param.
                                   BC value                                              blind quadrant                                       Kernel coeff.         Constitutive
                                                                                       high IFS / high EL 2
                       1.5         Coefficient                                                                                    0.8         BC coeff.             Repair subset
                                   Structural trend
                                                                                                                                  0.6


                                                                                                                         MCS
                       1.0
      EL 2




                                                                                                                                  0.4
                       0.5
                                                                                                                                  0.2

                       0.0                                                                                                        0.0
                                     0.5              0.6         0.7          0.8   0.9          1.0                                         0.5             0.6             0.7             0.8   0.9           1.0
                                                                        IFS                                                                                                           IFS



Figure 5: IFS/MCS validation diagnostics. (a) IFS validation on 30 MOOSE-verified perturbation
pairs: structural and BC-value errors fall outside the blind quadrant, whereas coefficient errors
can remain high-IFS with large field error; all simulations converge. (b) MCS coefficient/material
blind-spot repair: the shaded quadrant marks high-IFS/low-MCS cases, colors denote mismatch type,
and black rings mark repaired cases.


Figure 5a validates IFS’s structural boundary rather than calibrating it to numerical error: structural
perturbations fall below high IFS, while coefficient-magnitude errors can remain near IFS ≈ 1.0
despite nontrivial field error. This blind spot motivates MCS as a conditional secondary diagnostic,
not a replacement for IFS. Figure 5b visualizes the complementary diagnostic: on the 220-case
GPT-5.4→DeepSeek V4 Flash PDE-Refine sidecars, MCS identifies 32 high-IFS/low-MCS cases
among 176 comparable outputs; point color marks the main coefficient/material mismatch source and
black rings mark the repair subset. Appendix F, Table 8, reports that the 22-case repair diagnostic
raises mean MCS from 0.316 to 0.985 while preserving structural IFS.

7.2                    Mixed-Model PDE Contract Transfer

Because PDE-Refine factors extraction from synthesis, we test whether Pllm transfers across tested
model families (Appendix P, Table 23). GPT-5.4 extraction with DeepSeek generation reaches 0.772
IFS, between DeepSeek self (0.765) and GPT self (0.792); Gemini extraction with DeepSeek shows
the same ordering (0.784 vs. 0.765 and 0.796). Contracts transfer across the tested model families,
but final quality remains bounded by the generator.

7.3                    Scope and Limitations

Scope. IFS checks structural correspondence in the covered MOOSE fragment: terms, BCs, ICs,
direct coefficient checkpoints represented in the physics contract, and time scheme. It does not
verify mesh quality, solver convergence, discretization error, formal soundness, agreement with
measurements, or coefficient/material-only facts outside that reconstructed structural contract. Custom
objects and specialized kernel branches outside the covered semantic map require registered mappings
for representation-relative claims and are tracked through U when encountered. Cross-DSL extensions


                                                                                                                9
are symbolic-PDE proof-of-concepts, not runtime verification. MCS is the conditional diagnostic for
comparable coefficient/material blind spots.

8   Conclusion
This paper addresses the comprehension–generation gap for AI-generated MOOSE simulations by
separating object executability from PDE intent fidelity. Deterministic reconstruction and IFS turn
silent physics mismatches into violation reports; on 220-case MooseBench, PDE-Refine improves
fidelity most on weak models and hard cases (+0.22 to +0.41 IFS), and under a frozen object-
realization registry, PDE-Reg reduces runnable-but-wrong outputs (Sonnet 4.6 FalseExec 40.0% →
31.4%) relative to execution-only repair. Mixed-model, MCS, and cross-DSL diagnostics define
the boundary of the approach: contracts transfer across tested model families, coefficient/material
facts require a secondary diagnostic, and reconstruction-and-comparison extends to DSLs with
compositional PDE semantics. The results support treating execution as a runtime-validity check, not
as a proxy for the structural fidelity of the encoded physics.

Code Availability
The code for this work is publicly available at:

                       https://github.com/HaningZS/moose-ifs.git

References
 [1] Martin Sandve Alnæs. Ufl: a finite element form language. In Automated solution of differential
     equations by the finite element method: the FEniCS Book, pages 303–338. Springer, 2012.

 [2] Anthropic. Introducing Claude Haiku 4.5.      https://www.anthropic.com/news/
     claude-haiku-4-5, October 2025. Accessed: 2026-05-07.

 [3] Anthropic. Introducing Claude Sonnet 4.6.     https://www.anthropic.com/news/
     claude-sonnet-4-6, February 2026. Accessed: 2026-05-07.

 [4] Meron Belachew, Yulong Liu, J. David Frost, and Chloé Arson. Numerical assessment of
     plasticity development and energy expenditure of ant-like microtunnelling. Tunnelling and
     Underground Space Technology, 172:107501, 2026. ISSN 0886-7798. doi: https://doi.org/
     10.1016/j.tust.2026.107501. URL https://www.sciencedirect.com/science/article/
     pii/S0886779826000593.

 [5] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. Teaching large language
     models to self-debug, 2023. URL https://arxiv.org/abs/2304.05128.

 [6] Yuxuan Chen, Xu Zhu, Hua Zhou, and Zhuyin Ren. Metaopenfoam: an llm-based multi-agent
     framework for cfd. arXiv preprint arXiv:2407.21320, 2024.

 [7] DeepSeek-AI. Deepseek-v4: Towards highly efficient million-token context intelligence, 2026.

 [8] Madeline Endres, Sarah Fakhoury, and Saikat Chakraborty. Can we verify step by step for
     correct user intent satisfaction? In Proceedings of FSE, 2024.

 [9] Gemini Team, Google. Gemini 3.1 Flash-Lite: Built for intelligence at scale. https:
     //blog.google/innovation-and-ai/models-and-research/gemini-models/
     gemini-3-1-flash-lite/, March 2026. Accessed: 2026-05-07.

[10] Jonathan E Guyer, Daniel Wheeler, and James A Warren. Fipy: Partial differential equations
     with python. Computing in Science & Engineering, 11(3):6–15, 2009.

[11] Frédéric Hecht. New development in freefem++. Journal of numerical mathematics, 20(3-4):
     1–14, 2012.


                                                   10
[12] Prithwish Jana, Sam Davidson, Bhavana Bhasker, Andrey Kan, Anoop Deoras, and Laurent
     Callot. Terraformer: Automated infrastructure-as-code with llms fine-tuned via policy-guided
     verifier feedback. arXiv preprint arXiv:2601.08734, 2026.
[13] Guillaume Lample and François Charton. Deep learning for symbolic mathematics. In Inter-
     national Conference on Learning Representations, 2020. URL https://openreview.net/
     forum?id=S1eZYeHFDS.
[14] Michael Lange, Navjot Kukreja, Mathias Louboutin, Fabio Luporini, Felippe Vieira, Vin-
     cenzo Pandolfo, Paulius Velesko, Paulius Kazakas, and Gerard Gorman. Devito: Towards
     a generic finite difference dsl using symbolic python. In 2016 6th workshop on python for
     high-performance and scientific computing (PyHPC), pages 67–75. IEEE, 2016.
[15] Jae Ryong Lee and Han Young Yoon. Multi-physics simulation of nuclear reactor core by
     coupled simulation using cupid/master. International Journal of Heat and Mass Transfer, 115:
     1020–1032, 2017.
[16] Mengnan Li, Jason Miller, Zachary Prince, Alexander Lindsay, and Cody Permann. Moosenger–
     a domain-specific ai agent for the moose ecosystem. arXiv preprint arXiv:2603.04756, 2026.
[17] Zongyi Li, Nikola B. Kovachki, Kamyar Azizzadenesheli, Burigede Liu, Kaushik Bhattacharya,
     Andrew M. Stuart, and Anima Anandkumar. Fourier neural operator for parametric partial
     differential equations. CoRR, abs/2010.08895, 2020. URL https://arxiv.org/abs/2010.
     08895.
[18] Yulong Liu and Chloé Arson. Physics-informed neural network surrogate modeling of pressur-
     ized cavity in homogeneous and bilayered media. In ARMA US Rock Mechanics/Geomechanics
     Symposium, page D022S018R006. ARMA, 2025.
[19] Yulong Liu and Chloé Arson. A physics-informed neural network for modeling pressurized
     cavities of arbitrary smooth shape embedded in heterogeneous rock, January 2026. URL
     https://doi.org/10.21203/rs.3.rs-8492281/v1. Preprint, Version 1, Research Square.
[20] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri
     Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al. Self-refine: Iterative refinement
     with self-feedback. Advances in neural information processing systems, 36:46534–46594, 2023.
[21] Zavier Ndum Ndum, Jian Tao, John Ford, and Yang Liu. Autofluka: A large language
     model based framework for automating monte carlo simulations in fluka. arXiv preprint
     arXiv:2410.15222, 2024.
[22] Bo Ni and Markus J Buehler. Mechagents: Large language model multi-agent collaborations
     can solve mechanics problems, generate new data, and integrate knowledge. Extreme Mechanics
     Letters, 67:102131, 2024.
[23] William L Oberkampf and Christopher J Roy. Verification and validation in scientific computing.
     Cambridge university press, 2010.
[24] OpenAI. Introducing GPT-4.1 in the API. https://openai.com/index/gpt-4-1/, April
     2025. Accessed: 2026-05-07.
[25] OpenAI. Introducing GPT-5.4. https://openai.com/index/introducing-gpt-5-4/,
     March 2026. Accessed: 2026-05-07.
[26] Cody J Permann, Derek R Gaston, David Andrš, Robert W Carlsen, Fande Kong, Alexander D
     Lindsay, Jason M Miller, John W Peterson, Andrew E Slaughter, Roy H Stogner, et al. Moose:
     Enabling massively parallel multiphysics simulation. SoftwareX, 11:100430, 2020.
[27] Gerhard Schellhorn, Stefan Bodenmüller, and Wolfgang Reif. Vericode: Correct translation of
     abstract specifications to c code. In International Conference on Integrated Formal Methods,
     pages 53–74. Springer, 2024.
[28] Tianyi Zhang, Shidong Pan, Zejun Zhang, Zhenchang Xing, and Xiaoyu Sun. Deployability-
     centric infrastructure-as-code generation: Fail, learn, refine, and succeed through llm-
     empowered devops simulation. arXiv preprint arXiv:2506.05623, 2025.


                                                11
A    Details of the Silent-Failure Simulations
Figure 1 uses a diffusion problem on a perforated rectangular domain
Ω = Ω0 \Ωcav ,       Ω0 = [−3.5, 3.5]×[−2, 2],           Ωcav = {(x, y) : x2 +y 2 < R2 },     R = 0.65.
The intended transient model is
      ∂t c − ∇· (D(x)∇c) = s(x, t)          in Ω,   ∇c · n = 0        on Γcav ,   c(x, 0) = c0 (x).
Steady-state cases are obtained by omitting the transient term ∂t c.
The five columns perturb different parts of this specification. Panel (a) replaces the no-flux cavity
wall with an absorbing cavity boundary. Panel (b) omits the source/sink term. Panel (c) replaces the
heterogeneous diffusivity D(x) with a homogeneous coefficient. Panel (d) solves the steady-state
problem instead of the intended transient problem. Panel (e) uses an incorrect initial condition. All
fields are normalized for visualization.

B    Weak-Form Derivation and MOOSE Input Example
To illustrate the kernel–PDE correspondence, consider the zero-gravity, divergence-free form of
Darcy’s pressure equation:                       
                                            K
                                    −∇ ·       ∇p = 0 in Ω.
                                            µ
Multiplying by a test function ψ and integrating by parts gives the weak-form residual
                        Z                      Z                 
                                 K                      K
                            ∇ψ · ∇p dΩ −            ψ      ∇p · n dΓ = 0.                   (6)
                                  µ                     µ
                        |Ω      {z       }     | ∂Ω       {z          }
                           Kernel contribution           BC contribution
The volume term is assembled by a MOOSE Kernel, while the boundary term is imposed through a
BC object. The corresponding MOOSE input file is:
                         Listing 1: MOOSE input for Darcy’s pressure law.
[Kernels]
   [ ./ diff]
      type = DarcyFluxPressure
      variable = pressure
   [ ../ ]
[]

[BCs]
   [ ./ left_bc]
      type = DirichletBC
      variable = pressure
      boundary = left
      value = 1.0 e6
   [ ../ ]
   [ ./ right_bc]
      type = DirichletBC
      variable = pressure
      boundary = right
      value = 0.0
   [ ../ ]
[]

[Materials]
   [ ./ porous]
      type = G en er i cC on st a nt Ma te r ia l
      prop_names = ’ permeability viscosity ’
      prop_values = ’1e -12 1e -3 ’
   [ ../ ]
[]



                                                    12
C    Full System Architecture
The system factors generation through an explicit physics contract and verifies the generated input
by reconstructing its encoded contract. The deterministic reconstruction step is formalized in
Algorithm 1.

Algorithm 1 Deterministic PDE Reconstruction from MOOSE Input
Require: MOOSE input file AST A, Kernel–PDE mapping M
Ensure: Physics contract Pcode
 1: T ← ∅; B ← ∅; I ← ∅; C ← {}; U ← ∅
 2: S ← T RANSIENT if A.Executioner.type = Transient else S TEADY
 3: for each kernel κ in A.Kernels do
 4:   if κ.type ∈  / M then
 5:      U ← U ∪ {κ.type}; continue {unresolved}
 6:   end if
 7:   (vκ , oκ , ακ ) ← M[κ.type](κ.params)
 8:   T ← T ∪ {(vκ , oκ , ακ )}
 9: end for
10: for each BC β / IC ι / material µ do
11:   B ← B ∪ {(β.type, β.boundary, β.value)}; similarly for I, C
12: end for
13: return (T , B, I, C, S, A.Mesh, U)



Stage 1: PDE Intent Extraction. The extractor receives a natural-language simulation description
and produces Pllm , a structured physics contract containing governing terms, BCs, ICs, coefficient/-
material facts, and time scheme. The output is parsed as JSON before being passed downstream.

Stage 2: Specification-Guided Code Synthesis. The generator receives Pllm and writes a MOOSE
input file. The contract is used as a checklist for terms, BCs, ICs, materials, and time scheme rather
than as a hidden ground truth.

Stage 3: PDE Reconstruction and Verification. The verifier parses the generated input, ex-
tracts kernel, BC, IC, and material blocks, and applies the kernel–PDE mapping to reconstruct
Pcode . It computes IFS(Pllm , Pcode ) and emits a dimension-wise violation report; when comparable
coefficient/material facts exist, the same parse also yields MCS.

Stage 4: Error-Guided Refinement. If IFS < τIFS , the refiner receives the current code and the
structured violation report, then makes targeted edits. The revised code is re-verified until convergence
or Nmax iterations.

Prompt-level self-checking. Generation and refinement prompts ask the model to identify gov-
erning equations, select MOOSE objects, and check the file against the provided contract before
returning the final input. This is prompt structure rather than an additional verification signal.

Iteration and regression guard. The refinement loop is bounded by Nmax and controlled by the
IFS threshold. A regression guard keeps the best-scoring candidate if a refinement step lowers IFS.

Mixed-LLM configuration. Because PDE extraction and code generation are separated by an
explicit Pllm contract, the framework can assign different models to each stage. The 220-case
mixed-model ablation in Table 23 uses this configuration to cross GPT-5.4, Gemini 3.1 Flash Lite,
and DeepSeek V4 Flash as extractor/generator pairs. The cross-model rows diagnose whether the
physics contract transfers across providers rather than measuring a new leaderboard method.

Execution-based refinement (Exec-Repair) prompt construction. The Exec-Repair baseline
follows the standard self-refinement paradigm [20, 5]: the LLM receives its previously generated
code along with the generic instruction “Review your code for correctness and fix any issues.” No
physics-specific guidance, PDE-level analysis, or structured violation report is provided. When the


                                                   13
LLM encounters blocks referencing undefined variables or material properties, a common repair is
deletion: removing the problematic block to eliminate the error. This can remove physically necessary
kernels. For example, deleting a TimeDerivative kernel that referenced an undefined material
property resolves the runtime error but changes the PDE from parabolic to elliptic. The resulting
code executes successfully but solves a different problem.

D    Official-Document RAG Diagnostics
The official-document diagnostics isolate document access from PDE-level feedback. They test
whether realistic MOOSE documentation snippets, without benchmark answers or PDE violation
reports, explain the gains from PDE-grounded verification.

Corpus. The main corpus is an official MOOSE object-documentation corpus whose records
expose object names, descriptions, and documentation text. The runner also provides core HIT syntax
snippets as fallback context. Retrieval is a deterministic keyword top-k over documentation snippets,
with at most eight retrieved snippets and a 6000-character prompt budget. No vector index, case
library, or generated-answer corpus is used.

Diagnostic variants. DocsDirect retrieves official documentation before direct code generation.
Docs+ExecRepair adds the same object-realization registry and one runtime-log repair round without
PDE/IFS feedback, while Docs+PDE-Reg adds the same documentation context to PDE-Reg. These
diagnostics test whether official-document access and execution repair alone explain the PDE-
grounded gains.

Leakage controls. The RAG corpus excludes MooseBench reference inputs, Pgt , generated
answers, cached benchmark outputs, and annotated input-card or case-card corpora. In partic-
ular, records with answer-like fields such as input_card_name, annotated_input_card, or
overall_description are not used, and full HIT input-card shaped records are skipped. Docs-
Direct and Docs+ExecRepair receive no deterministic PDE reconstruction or IFS violation report.
Docs+PDE-Reg uses the same PDE-level feedback as non-document PDE-Reg, but receives no
benchmark reference input, no Pgt , and no execution/check-input feedback. Each JSONL result
stores rag_sources; in the 220-case DeepSeek V4 Flash runs used for Table 3, all records had
non-empty official-document sources.

Interpretation. DocsDirect tests documentation access alone; Docs+ExecRepair tests documenta-
tion plus execution-only repair; Docs+PDE-Reg tests whether PDE-grounded repair also benefits
from the same documents. The results show that official documentation helps Direct generation,
but docs plus execution repair still leaves a large FalseExec region. Documentation-conditioned
generation does not by itself solve structural PDE alignment or material-value consistency; IFS and
MCS handle those semantic checks separately.

E    Kernel–PDE Mapping Table
Table 6 provides the covered kernel–PDE weak-form mapping table used for MooseBench, including
source-grounded weak-form contributions and normalized operator types.




                                                 14
                   Table 6: Kernel–PDE weak-form mapping table for the covered MOOSE frag-
                   ment; the listed source-grounded weak-form contributions cover 762 of 766
                   MooseBench ground-truth kernel-term instances (99.48%). The “Canonical Weak-
                   Form Residual Contribution” column records the most explicit kernel-level contri-
                   bution to the assembled weak-form residual for each kernel, identified primarily
                   from the MOOSE source code and supplemented by official documentation when
                   clarification is needed. Depending on the kernel implementation, entries may
                   appear in integration-by-parts form, as direct test-function-weighted strong-form
                   terms, or, when necessary, as kernel-level energetic, matrix, stabilization, or
                   discrete residual contributions. For covered entries, these source-grounded repre-
                   sentations are normalized to a canonical weak-form operator descriptor (τ, ϕ, γ),
                   where τ denotes the operation on the trial-side quantity, ϕ the operation on
                   the test function, and γ the contraction pattern. This descriptor captures the
                   weak-form shape associated with the corresponding normalized operator type; co-
                   efficients, coupled variables, constitutive choices, and nonlinear energetic factors
                   are represented separately in the explicit contribution, mapping metadata, or the
                   coefficient/material contract.

MOOSE Kernel                          Operator             Variable      Canonical Weak-Form Residual Contribution
                                                                                                               
                                                                           ψ, µ ηi3 − ηi + 2ηi j γij ηj2
                                                                                                    P
ACGrGrMulti                           allen_cahn              ηi
ACInterface                           allen_cahn              ηi         (κi ∇ηi , ∇(Li ψ))
                                                                                                              
                                                                                                             2
                                                                           ∇(Lψ), 21 ∂∇η ∂κ
                                                                                                P
ACInterface2DMultiPhase1              allen_cahn          ηαi                              αi
                                                                                                   (∇η  βj )

ACInterface2DMultiPhase2              allen_cahn          ηαi            (κ∇ηαi , ∇(Lψ))
                                                                              P ∂hj
ACSwitching                           allen_cahn           ηi            (ψ,     j ∂ηi Fj )
ADBodyForce                           source                u            (ψ, −f )
ADDiffusion                           diffusion             u            (∇ψ, ∇u)
ADHeatConduction                      diffusion            T             (∇ψ, k∇T )
ADHeatConductionTimeDerivative        time_derivative      T             (ψ, ρcp ∂t T )
ADStressDivergenceRZTensors           stress_divergence (ur , uz )       (∇ψ, σRZ ) + (ψr /r, σθθ )
ADStressDivergenceTensors             stress_divergence     u            (∇ψ, σ)
ADTimeDerivative                      time_derivative       u            (ψ, ∂t u)
ADVectorDiffusion                     diffusion             u               ∇u)
                                                                         (∇ψ,                         
                                                                              ∂floc     ∂Ed
AllenCahn                             allen_cahn              ηi         L            +        , ψm
                                                                               ∂ηi       ∂ηi
AnisotropicDiffusion                  diffusion               u          (∇ψ, e k∇u)
ArrayBodyForce                        source                  u          (ψ, −f )
ArrayDiffusion                        diffusion               u          (∇ψ, D∇u)
ArrayReaction                         reaction                u          (ψ, Ru)
ArrayTimeDerivative                   time_derivative         u          (ψ, T ∂t u)
BodyForce                             source                  u          (ψ, −f )
CHInterface                           cahn_hilliard           ci         (κi ∇2 ci , ∇ · (Mi ∇ψ))
CHMath                                other                   c          (∇ψ, ∇(c3 − c))
CHSplitFlux                           cahn_hilliard           j           j
                                                                         (ψ,    + M ∇µ)                          
                                                                                     ∂floc        ∂Ed
CahnHilliard                          cahn_hilliard           ci           Mi ∇            +∇              , ∇ψ
                                                                                      ∂ci          ∂ci
CoefDiffusion                         diffusion               u          (∇ψ, D∇u)
CoefReaction                          reaction                u          (ψ, λu)
CoefTimeDerivative                    time_derivative         u          (ψ, α∂t u)
ConservativeAdvection                 advection               u          −(∇ψ, vu)
CosseratStressDivergenceTensors       stress_divergence       u          (∇ψ, σCosserat
                                                                                     P     )
CoupledBEEquilibriumSub               other                  Cj          (ψ, ∂t (ϕ Pi νji Ci ))
CoupledBEKinetic                      other                  Cm          (ψ, ∂t (ϕ P   m wm Cm ))
CoupledConvectionReactionSub          reaction               Cj          (ψ, q · ∇( Pi νji Ci ))
CoupledDiffusionReactionSub           diffusion              Cj          (∇ψ, D∇( i νji Ci ))
CoupledForce                          source                  u           −αv)
                                                                         (ψ,  P                    
                                                                                      ∂hj
CoupledSwitchingTimeDerivative        time_derivative         ηi           ψ,       j ∂ηi F j   ∂t v
CoupledTimeDerivative                 time_derivative         u          (ψ, ∂t v)
                                                                                                          continued on next page




                                                   15
                    Table 6: Kernel–PDE mapping table for the covered MOOSE fragment (contin-
                    ued).

MOOSE Kernel                        Operator              Variable   Canonical Weak-Form Residual Contribution
CurlCurlField                       curl_curl                u       (∇ × ψ, a ∇ × u)
                                                                             K
DarcyFluxPressure                   other                    P       (∇ψ,       (∇P − ρg))
                                                                             µ
DesorptionFromMatrix                source                   m       (ψ, ṁ)
DesorptionToPorespace               source                   m       (ψ, −ṁ)
Diffusion                           diffusion                u       (∇ψ, ∇u)
DynamicStressDivergenceTensors      stress_divergence        u       (∇ψ, σdyn )
FunctionDiffusion                   diffusion                u       (∇ψ, f (x, t)∇v)
FunctorKernel                       other                    u       (ψ, ±(p − u))
GradientComponent                   other                    u       (ψ, u − ∂α v)
Gravity                             source                   u       (ψ, g)
HeatConduction                      diffusion                T       (∇ψ, k∇T )
HeatConductionTimeDerivative        time_derivative          T       (ψ, ρCp ∂t T )
HeatSource                          source                   T       (ψ, −q̇)
INSADMass                           ns_continuity            p       (ψ, ∇ · u)
INSADMomentumAdvection              advection                u       (ψ, ρ(u · ∇)u)
INSADMomentumPressure               ns_pressure              u       −(∇ · ψ, p)
INSADMomentumSUPG                   ns_viscous               u       (τ u · ∇ψ, Rmom )
INSADMomentumViscous                ns_viscous               u       (∇ψ, τ )
INSFEFluidMassKernel                ns_continuity            p       −ρ v̄ · ∇ψ
INSFEFluidMomentumKernel            ns_viscous               v       ρ ϵ (v·∇v) ψ +ϵ (∇p) ψ −ϵρg ψ +τ ·∇ψ +ffric ψ
INSMass                             ns_continuity            p       (ψ, −∇ · u)
INSMomentumLaplaceForm              ns_viscous               u       (∇ψ, µ∇u)
INSMomentumTimeDerivative           time_derivative          u       (ψ, ρ ∂t u)
InertialForce                       inertia                  u       (ψ, ρ ü + η ρ u̇)
InertialTorque                      inertia                  u       (ψ,
                                                                      ρ ϵijk uj ük )              
                                                                             ∂F1 P ∂hj
KKSMultiACBulkC                     allen_cahn              η1         ψ, −            j        c j
                                                                             ∂c1          ∂η1          
                                                                           P ∂hj                   ∂gi
KKSMultiACBulkF                     allen_cahn               ηi        ψ,     j       Fj + w i
                                                                                ∂ηi              ∂η i
                                                                           ∂Fa 1          ∂Fb 1
KKSPhaseChemicalPotential           other                   ca         ψ,             −
                                                                           ∂ca ka          ∂cb kb
MassEigenKernel                     other                    u       λ(ψ, −c u)
MassLumpedTimeDerivative            time_derivative          u       (ψ, ∂t u)
MatDiffusion                        diffusion                u       (∇ψ, D∇u)
MatReaction                         reaction                 u       (ψ, −L v)
                                                                                                             
                                                                                            P ∂hj
                                                                       ψ, − m ∂c∂F
                                                                             P           1
NestedKKSMultiACBulkC               allen_cahn               ηi                        m,1      j   ∂ηi
                                                                                                        c m,j
                                                                     
                                                                           P ∂hj                   ∂gi
NestedKKSMultiACBulkF               allen_cahn               ηi        ψ,     j       F j  + w  i
                                                                                 ∂ηi              ∂ηi
NullKernel                          other                    u       (ψ,
                                                                         0)                    
                                                                                ∂ρ         ∂ρ
PINSFEFluidPressureTimeDerivative   time_derivative          p         ψ, ϵ         Ṫ +       ṗ
                                                                               ∂T         ∂p
                                                                             ∂vi         ∂ρ
PINSFEFluidVelocityTimeDerivative   time_derivative          vi        ψ, ρ        + vi
                                                                            ∂t          ∂t                            
                                                                             P κ k kr,β
PorousFlowAdvectiveFlux             advection               χκβ        ∇ψ,         χ
                                                                                 β β   ρ β           (∇P   β −  ρ β g)
                                                                                             µβ
PorousFlowBasicAdvection            advection                u       −(∇ψ,
                                                                              v β u)               
                                                            χκβ                          κ       κ
                                                                             P
PorousFlowDispersiveFlux            diffusion                          ∇ψ,       β ρβ Dβ ∇Xβ
PorousFlowEffectiveStressCoupling   pf_effective_stress     u        −αB peff
                                                                             ∂xc ψ                                
                                                                                                     P
PorousFlowEnergyTimeDerivative      time_derivative          T         ψ, ∂t (1 − ϕ)er + ϕ β Sβ ρβ eβ
                                                                                                                      
                                                                             P κ k kr,β
PorousFlowFluxLimitedTVDAdvection   advection                u         ∇ψ,       β χ β ρ β           (∇P   β −  ρ β g)
                                                                                             µβ
                                                                                                     continued on next page




                                                 16
                     Table 6: Kernel–PDE mapping table for the covered MOOSE fragment (contin-
                     ued).

MOOSE Kernel                           Operator            Variable   Canonical Weak-Form Residual Contribution
                                                                                                      
                                                                                     k
                                   advection
PorousFlowFullySaturatedAdvectiveFlux                        χκ         ∇ψ, (ρ)χκ (∇P − ρg)
                                                                                    µ              
                                                                                 k
PorousFlowFullySaturatedDarcyBase      pf_darcy_flux          P         ∇ψ, (ρ) (∇P − ρg)
                                                                                µ                     
                                                                                     k
PorousFlowFullySaturatedDarcyFlow      advection             χκ         ∇ψ, (ρ)χκ (∇P − ρg)
                                                                                    µ                             
                                                                              P            k kr,β
PorousFlowHeatAdvection                advection              h         ∇ψ,     β h β ρ β          (∇P  β − ρ β g)
                                                                                             µβ
PorousFlowHeatConduction               diffusion              T       (∇ψ, λ∇T )
PorousFlowHeatMassTransfer             other                  u       (ψ,
                                                                       ktr  (u − v))              
                                                             χκ         ψ, ∂t ϕ β (ρβ )Sβ χκβ
                                                                                 P
PorousFlowMassTimeDerivative           time_derivative
                                                                                                  
                                                             χκ         ψ, ϕ β (ρβ )Sβ χκβ ϵ̇v
                                                                             P
PorousFlowMassVolumetricExpansion      source
                                                                                 P                
PorousFlowPreDis                       reaction               ci       ψ, ϕ Saq r νir ρr Rr
PrimaryConvection                      advection              u       (ψ, vD · ∇u)
PrimaryDiffusion                       diffusion              cj      −(∇ψ,
                                                                              ϕD∇c
                                                                                  j)
                                                                             ∂cj
PrimaryTimeDerivative                  time_derivative        cj        ψ, ϕ
                                                                              ∂t
Reaction                               reaction               u       (ψ, λu)
                                                                                                            
                                                                                      ∂floc        ∂Ed
SplitCHParsed                          cahn_hilliard          c         −κi ∇2 ci +            +        − µi
                                                                                        ∂ci        ∂ci
SplitCHWRes                            cahn_hilliard          w       (M ∇u, ∇ψ)
StressDivergenceTensors                stress_divergence      u       (∇ψ, σ)
StressDivergenceTensorsTruss           stress_divergence      u       (∇ψ, σ)
SusceptibilityTimeDerivative           time_derivative        u       (ψ, F (u, a, b, . . .) ∂t u)
TimeDerivative                         time_derivative        u       (ψ, ∂t u)
VectorBodyForce                        source                 u       (ψ, −f )
VectorDiffusion                        diffusion              u       (∇ψ, ∇u)
VectorFunctionReaction                 reaction               u       (ψ, λ(x, t)u)
VectorTimeDerivative                   time_derivative        u       (ψ, ∂t u)




F   MCS Definition and Boundary Diagnostics

MCS is a limitation-aware diagnostic for the coefficient/material blind spot of structural IFS. It is
reported only when comparable material or coefficient facts can be extracted from both reference
and candidate files. For the MOOSE perturbation study in Figure 5a, we compute EL2 = ∥upert −
ugt ∥2 / max(∥ugt ∥2 , 10−15 ) on the common output grid, where upert and ugt are the concatenated
final solution vectors.
Definition F.1 (MCS diagnostic facts). Let F(c) be the set of normalized coefficient/material facts
extracted from a MOOSE input file, including material-backed kernel coefficients, convective/Robin
BC coefficients, material model signatures, and uncovered constitutive parameters. For comparable
reference and candidate facts,
                          1     X
 MCS(cref , ccand ) =             1[∃g ∈ Fcand : key(g) = key(f ) ∧ value(g) ≈ value(f )] . (7)
                        |Fref |
                             f ∈Fref

Here ≈ denotes the normalized fact comparator: scalar values use the same reference-relative
numerical tolerance as ≈δ in Definition G.6, categorical material signatures use exact normalized
matching, and structured values are compared by their normalized representation. MCS is undefined
when no comparable reference facts exist. It is a coefficient/material diagnostic for high-IFS blind
spots, not part of IFS term matching or descriptor-level structural auditing.


                                                   17
Table 7: Representative boundary-condition mappings in MOOSE; these follow the same normaliza-
tion logic as the kernel–PDE mappings.

MOOSE BC                                                      Mathematical Form                                  Type
DirichletBC                                                    u = g on ∂ΩD                                      Dirichlet (essential)
FunctionDirichletBC                                           u = g(t, x) on ∂ΩD                                 Dirichlet (space/time-dependent)
FunctorDirichletBC                                            u = h(t, x, . . .) on ∂ΩD                          Dirichlet (functor-based)
PenaltyDirichletBC                                            u = g on ∂ΩD                                       Dirichlet (penalty/weak)
PostprocessorDirichletBC                                       u = gpp on ∂ΩD                                    Dirichlet (postprocessor-driven)
                                                               ∂u
NeumannBC                                                           = h on ∂ΩN                                   Neumann (prescribed flux)
                                                               ∂n
                                                               ∂u
FunctionNeumannBC                                                   = h(t, x) on ∂ΩN                             Neumann (space/time-dependent)
                                                               ∂n
                                                               ∂u
FunctorNeumannBC                                                    = h(t, x, . . .) on ∂ΩN                      Neumann (functor-based)
                                                               ∂n
                                                               ∂u
CoupledVarNeumannBC                                                 = v on ∂ΩN                                   Neumann (coupled-variable)
                                                               ∂n
                                                               C ∂u
MatNeumannBC                                                           = M h on ∂ΩN                              Neumann (material-scaled flux)
                                                                 ∂n
FunctionGradientNeumannBC                                      −⟨ψi , n·k∇f ⟩ on ∂ΩN                             Neumann (gradient-based weak form)
ConvectiveHeatFluxBC                                           q · n̂ = h(T − T∞ ) on ∂Ω
                                                               Z                                                 Robin (convective heat transfer)
                                                                     α u(r) ψt (r)
VacuumBC                                                                            dS                           Robin (vacuum-type)
                                                                 ∂Ω
                                                                  Z       2
                                                                         ∂u
DiffusionFluxBC                                                −            v ds                                 Flux contribution (residual only)
                                                                    ∂ΩF ∂n
Periodic BC                                                    u(xs ) = u(xm ) on paired boundaries              Periodic constraint
PorousFlowSink                                                 s = f (t, x) on ∂Ω                                PorousFlow sink/source flux BC
PorousFlowPiecewiseLinearSink                                 sZ = f (t, x) g(P β − Pe ) on ∂Ω                   PorousFlow piecewise-linear sink/source BC
PorousFlowOutflowBC                                                 ψn·F                                         PorousFlow outflow flux contribution
                                                               ∂Ω




                                                                                                 (b) MCS repair
                (a) IFS-blind coefficient failures (n=32)                                        mean 0.316->0.985; 21/22 at 1.0
          1.0                                                                              1.0

                                                                                           0.8

                                                                                           0.6
                                                                                    MCS




          0.8
                                                                                           0.4

                                                                                           0.2                                           before
                                                                                                                                         after
                                                                                           0.0
          0.6
    MCS




                                                                                                 (c) IFS preserved
          0.4                                                                                    mean 0.959->0.987; 22/22 non-decrease
                                                                                          1.00

                                                                                          0.95
          0.2         No MCS mismatch
                                                                                    IFS




                                                                                          0.90
                      Kernel coefficient
                      BC coefficient
                      Material parameter                                                  0.85
                      Constitutive model                                                                                                 before
          0.0         repair smoke                                                        0.80                                           after

                    0.5            0.6      0.7         0.8         0.9     1.0
                                                  IFS


Figure 6: Full MCS blind-spot and repair diagnostic, referenced from Section 7.1. The left panel
shows high-IFS/low-MCS coefficient/material blind spots; black rings mark the 22-case repair subset.
The right panels show that MCS repairs remove almost all coefficient/material mismatches while
preserving structural IFS.



                                                                           18
Table 8: MCS coefficient/material diagnostics. The survey uses the 220-case post-guard GPT-
5.4→DeepSeek V4 Flash PDE-Refine sidecars; the repair diagnostic uses 22 representative blind-spot
cases repaired by DeepSeek V4 Flash from only the MCS mismatch facts and the candidate code.

              Quantity                              Survey / before repair      After repair
              Comparable generated outputs                 176 / 220                  –
              High-IFS / low-MCS outputs                      32                      –
              Mismatch facts                        kernel 125; BC 79; material 279; model 110
              Repair smoke cases                               22                     22
              Accepted local repairs                            –                  22 / 22
              Mean IFS                                       0.959                  0.987
              Mean MCS                                       0.316                  0.985
              Mean MCS mismatches                             3.91                   0.05
              Cases with MCS= 1.0                            0 / 22                21 / 22

Table 9: Relationship between IFS and MCS in deployment. IFS remains the main structural gate;
MCS is a conditional secondary check for explicit material/coefficient facts.

Gate    Purpose                                       Always available?                      Main-text role
IFS     PDE structural fidelity                       Yes, within covered fragment           Main metric
MCS     Explicit material/coefficient consistency     Only when comparable facts exist       Boundary diagnostic


G      Operator-Type Formalization
This appendix formalizes the two-level representation used by reconstruction and IFS: normalized
PDE operator types are the comparison keys, while weak-form descriptors are structural witnesses
for auditing the mapping table.
Definition G.1 (Operator sets).
                Otrial = {identity, grad, div, curl, ddt, ddt2, stress, strain}                                (8)
                Otest = {identity, grad, div, curl}                                                            (9)
                    G = {scalar_mult, dot, double_dot}                                                        (10)
Otrial describes operators on the trial-side quantity, Otest describes operators on the test function,
and G describes the contraction mode.
Definition G.2 (Normalized PDE operator type and descriptor projection). Let OPDE be the finite
inventory of normalized PDE operator types in the kernel–PDE mapping table. When an operator
type has a weak-form witness, the table records the partial descriptor projection
                                    d : OPDE ⇀ Otrial × Otest × G.                                            (11)
Here ⇀ denotes a partial function: d(o) is defined only when the operator type o has an associated
weak-form descriptor in the mapping table.
Remark G.1 (Role of the descriptor). The operator type o ∈ OPDE is the term-comparison key;
the descriptor d(o) is its weak-form witness. Together they make the kernel–PDE mapping table
auditable: operator-type assignments are justified by the corresponding weak-form contributions
recorded in the table, while IFS scoring uses normalized operator-type equality.
Definition G.3 (Bound PDE term).
            BoundTerm := (v, o, α),                 v ∈ Variables, o ∈ OPDE , α ∈ R ∪ {⊥}.                    (12)
Here α = ⊥ denotes a unit coefficient (unspecified or identically 1). Descriptor metadata remains
attached to o through the mapping table; it is not part of the runtime term key.
Definition G.4 (Kernel–PDE mapping). M maps each covered MOOSE kernel class deterministically
to a normalized PDE operator type, coefficient extraction rule, severity weight, and optional descriptor
witness. Applied to a concrete kernel block κ, it yields a bound term (vκ , oκ , ακ ). The paper table
documents 762 of 766 MooseBench ground-truth kernel-term instances (99.48%) with source-
grounded weak-form contributions; BC and IC maps contain 16 and 21 entries, respectively.


                                                        19
Definition G.5 (Descriptor structural equivalence). For available descriptors da = (τa , ϕa , γa ) and
db = (τb , ϕb , γb ),
                         da ∼s db ⇐⇒ τa = τb ∧ ϕa = ϕb ∧ γa = γb .                                (13)
Proposition G.1. ∼s is an equivalence relation on available weak-form descriptors.

Proof. ∼s is the conjunction of equality on three descriptor components.

Remark G.2 (Audit-only structural relation). ∼s is used only for descriptor-level auditing; IFS scoring
uses operator-type equality on OPDE and does not depend on ∼s .
Definition G.6 (Coefficient-tolerant match). For an ordered reference–candidate pair of bound terms
tref = (vref , oref , αref ) and tcand = (vcand , ocand , αcand ),
                                                                  |αref − αcand |
            tref ≈δ tcand ⇐⇒ vref = vcand ∧ oref = ocand ∧                          ≤ δcoef .         (14)
                                                                  max(|αref |, ϵ0 )
Here δcoef is the coefficient relative tolerance (default 0.1), and ϵ0 prevents division by zero.
Remark G.3 (Reference-relative coefficient matching). The predicate ≈δ is reference-relative: for
δcoef > 0 it is generally neither symmetric nor transitive. This asymmetry is intentional, because IFS
scores candidate checkpoints against the fixed reference-induced set Q(Pref ) rather than comparing
two terms as an unordered pair. The reference coefficient αref defines the tolerance scale, consistent
with Pref serving as ground truth during evaluation and as the LLM-extracted contract during
deployment-time refinement.

Severity weight table. Each IFS checkpoint inherits a severity weight from the mapping table,
reflecting the physical impact of the error type:

                      Table 10: IFS severity weights (6-level, expert-defined).

       Severity        Weight    Justification
       Highest             4.0   Missing/wrong time derivative or inertial term (changes PDE class)
       Very High           3.0   Wrong dominant operator (changes PDE structure)
       High                2.0   Coupling term missing, BC/IC type wrong (breaks constraints)
       Medium              1.0   Value-level change with correct operator (quantitative error)
       Medium-Low          0.7   Source/forcing term missing (quantitative > structural impact)
       Low                 0.5   Non-physics metadata issue


Variable alignment procedure. Before IFS comparison, candidate variable names are aligned
to reference names via operator-signature matching. For each variable v, its operator signature
σ(v) = sort({oi : ti acts on v}) is the sorted set of normalized PDE operator types. A 1:1 mapping
is found between reference and candidate variables with matching signatures. When multiple
candidates share identical signatures (e.g., two species with identical diffusion–reaction equations),
the mapping is disambiguated by: (1) boundary condition alignment (matching boundary names and
values), and if needed, (2) coefficient values. All subsequent IFS comparisons use the aligned names.
Definition G.7 (Term set of a PDE). T = {(vi , oi , αi )}ni=1 , i.e., a PDE is represented as the set of
bound normalized PDE terms.
Definition G.8 (Term matching function). Given reference Tref and candidate Tcand :
                          
                            t       if ∃ tcand ∈ Tcand : vref = vcand ∧ oref = ocand ,
            match(tref ) = cand                                                                       (15)
                            ⊥       otherwise (missing term).

Extra terms are Textra = Tcand \ range(match).
Theorem G.1 (Reconstruction soundness). Let c be a syntactically valid MOOSE input file and
M a correct kernel–PDE mapping. Then Pcode = reconstruct(c, M) satisfies: (a) Completeness:
every covered active kernel has a corresponding bound term; (b) Fidelity: each bound term uses the
normalized operator type and descriptor witness, when defined, specified by M; (c) No spurious
terms: |T | = |{covered active kernels}|.


                                                   20
Proof sketch. By construction of Algorithm 1: the algorithm iterates all kernel blocks, applies M to
covered kernels, and adds exactly one bound term per covered kernel. Unknown kernels are tracked
in unresolved_kernels and reported diagnostically.
Theorem G.2 (IFS soundness). If IFS(Pref , Pcand ) = 1.0, then: (a) a bijection σ : Tref → Tcand
exists with matching variables and normalized PDE operator types; (b) all BC checkpoints pass their
type, boundary, and value predicates; (c) all IC checkpoints pass their type and value predicates; (d)
time schemes agree; (e) all reference coefficient checkpoints are matched by the candidate under ≈δ .

Proof. IFS = 1.0 implies zero failed weight across all dimensions. For terms, zero failures means no
missing and no extra terms, yielding a bijection over aligned variables and normalized operator types.
For BCs, ICs, time scheme, and coefficients, zero failures means every reference-induced checkpoint
predicate passes, including coefficient matches under ≈δ .
Theorem G.3 (Representational completeness). Let Pref and Pcand be two aligned PDE represen-
tations. If they differ in any represented dimension covered by the checkpoint set Q(Pref )—i.e.,
there exists a reference term with no candidate term sharing the aligned variable and normalized
PDE operator type, or an attribute (type, value, boundary) fails its prescribed reference-induced
predicate—then at least one checkpoint fails and IFS(Pref , Pcand ) < 1.

Proof. By construction, every represented reference item induces at least one checkpoint with positive
weight wj > 0. If the candidate differs on that item, the corresponding checkpoint predicate evaluates
to failure (1[failj ] = 1). The IFS numerator therefore contains at least one positive term, making the
penalty nonzero and IFS < 1.
Corollary G.1. Combining Theorems G.1 to G.3: within the covered MOOSE semantic fragment,
reported violations correspond to reconstructed PDE mismatches, and all represented mismatches
are detected as failed checkpoints.
Remark G.4 (Severity weight design). The six-level severity assignment (highest: 4.0 down to low:
0.5) encodes a domain-expert prior over typical physical impact: errors changing PDE type receive
the largest weights; errors changing coefficient values receive lower structural-fidelity weights. The
numerical values are engineering choices rather than universal physical constants; their relative
ordering reflects typical impact severity in multiphysics practice. The severity of each checkpoint is
inherited from the normalized operator type and checkpoint dimension in the domain-expert-annotated
mapping table (Appendix E).

H     Reproducibility Manifest
This manifest summarizes the parameters needed to reproduce all experiments. Provider snapshot
IDs, API access dates, container hashes, result JSONLs, and a SHA-256 manifest will be recorded in
the anonymous supplementary material.

H.1    Object-Realization Registry

The object-realization registry is a deterministic engineering layer that translates generated kernel/BC
blocks into MOOSE-instantiable objects: parameter resolution, material wiring, default Mesh /
Executioner / Outputs fill-ins, and minimal type repair when names mismatch the framework. The
registry does not modify IFS or MCS computation, does not provide PDE-level feedback, and is held
frozen across Exec-Repair+Reg and PDE-Reg in the deployment audit (Table 2). We treat it as
standard engineering infrastructure for experimental reproducibility rather than as a methodological
contribution.

I     Statistical Details
Wilcoxon signed-rank test. For each pair of methods, we compute the Wilcoxon signed-rank
statistic on per-prompt IFS differences within the same experiment sweep. The paper contains
standard semantic sweeps and registry execution-audit sweeps, so comparisons are not made across
incompatible method families unless they share the same generated-output setting.


                                                  21
Table 11: Key reproducibility parameters for MooseBench experiments. Provider snapshot IDs,
access dates, result JSONLs, SHA-256 manifests, and container hashes will be recorded in the
anonymous supplementary manifest.

Item                              Value
Benchmark                         MooseBench canonical 220-case clean set
Benchmark exclusions              40 excluded cases, fixed exclusion list
MOOSE execution app               local combined-opt, Application Version 541a9f6f
Standard non-registry methods     Direct, SpecGen, PDE-Refine
Deployment-audit methods          Exec-Repair+Reg, PDE-Reg
Official-doc diagnostics          DocsDirect, Docs+ExecRepair, Docs+PDE-Reg
RAG corpus                        official MOOSE object docs only; no benchmark answers or execution feedback
LLM temperature                   0
Maximum refinement iterations     Nmax = 2
IFS threshold                     τIFS = 0.85
Coefficient relative tolerance    δcoef = 0.1
MCS applicability                 reported when comparable coefficient/material facts exist
Parse failure handling            parse failures counted as IFS = 0
Exec definition                   InitExec2: exit 0, solve start before first error, or no error within 2s
Main statistic                    paired mean IFS difference + Wilcoxon signed-rank test
Execution audit statistic         Exec, GoodExec, FalseExec over all 220 cases
Release artifact                  benchmark, mapping table, code, result JSONLs and SHA-256 manifest




Table 12: Paired statistical comparisons on 220-case MooseBench sweeps. ∆ is the mean paired
IFS difference across all 220 cases; Wilcoxon W and p use the standard signed-rank test with zero
differences omitted.
 Sweep                           Comparison                       n      ∆            W              p
 Claude Sonnet 4.6               SpecGen vs. Direct             220    +0.056    7000.5          0.037
 Claude Sonnet 4.6               PDE-Refine vs. Direct          220    +0.072    6553.5          0.002
 GPT-5.4                         SpecGen vs. Direct             220    +0.014      6225          0.167
 GPT-5.4                         PDE-Refine vs. Direct          220    +0.046    4911.5          0.003
 DeepSeek V4 Flash               SpecGen vs. Direct             220    +0.069      5679          0.004
 DeepSeek V4 Flash               PDE-Refine vs. Direct          220    +0.183      4170    6.4 × 10−11
 Claude Sonnet 4.6 registry      PDE-Reg vs. Exec-Repair+Reg    220    +0.101    3637.5     2.6 × 10−8
 GPT-5.4 registry                PDE-Reg vs. Exec-Repair+Reg    220    +0.082    3416.5     1.6 × 10−7
 GPT-4.1-mini registry           PDE-Reg vs. Exec-Repair+Reg    220    +0.357    2595.0    1.3 × 10−20
 DeepSeek V4 Flash registry      PDE-Reg vs. Exec-Repair+Reg    220    +0.198    2416.5    2.1 × 10−15




Table 13: Conditional pipeline effectiveness on hard cases (IFSDirect < 0.7). The method is PDE-
Refine for standard non-registry sweeps and PDE-Reg for registry sweeps.

                     LLM                       n    ∆ IFS        W                p
                                                                                −11
                     Claude Sonnet 4.6         84   +0.273     188     1.0 × 10
                     GPT-5.4                   67   +0.219     227      3.3 × 10−8
                     GPT-4.1-mini             197   +0.406   1494.0    7.3 × 10−23
                     DeepSeek V4 Flash        108   +0.414      178    1.1 × 10−15




                                                    22
Threshold sensitivity.   The hard-case effect remains positive across Direct-IFS thresholds:
    Table 14: Threshold sensitivity for PDE-grounded improvement on cases where IFSDirect < θ.

                       LLM                  θ         n   ∆ IFS        p
                       Claude Sonnet 4.6   0.6    61      +0.341   1.0 × 10−9
                       Claude Sonnet 4.6   0.7    84      +0.273   1.0 × 10−11
                       Claude Sonnet 4.6   0.8   109      +0.212   1.6 × 10−11
                       GPT-5.4             0.6    44      +0.284   2.4 × 10−7
                       GPT-5.4             0.7    67      +0.219   3.3 × 10−8
                       GPT-5.4             0.8    97      +0.170   7.4 × 10−10
                       GPT-4.1-mini        0.6   172      +0.438   7.2 × 10−22
                       GPT-4.1-mini        0.7   197      +0.406   7.3 × 10−23
                       GPT-4.1-mini        0.8   202      +0.367   1.3 × 10−19
                       DeepSeek V4 Flash   0.6    86      +0.505   1.8 × 10−14
                       DeepSeek V4 Flash   0.7   108      +0.414   1.1 × 10−15
                       DeepSeek V4 Flash   0.8   135      +0.334   1.3 × 10−16


Bootstrap confidence intervals. For descriptive means and table values, confidence intervals can
be reproduced by bootstrap resampling over case IDs. We do not pool standard non-registry and
registry runs for paired inference because their generation prompts and object-realization controls
differ.

Execution-audit proportions. Registry audit claims are additionally evaluated with GoodExec and
FalseExec, which are Bernoulli case-level proportions over the same 220 prompts.

J     Motivating Examples: Detailed Descriptions
The four additional failure modes below illustrate the same silent-error pattern as Figure 1. All
examples are from actual MOOSE simulations that converge without error.

Example 1: Missing TimeDerivative (transient → steady-state). An LLM asked to model
“transient heat conduction in a steel rod” generates the HeatConduction kernel but omits
TimeDerivative. The code runs without error—but it solves Laplace’s equation ∇2 T = 0 in-
stead of the heat equation ρcp ∂T
                               ∂t − ∇ · (k∇T ) = 0. The simulation converges in one time step; the
entire time-dependent behavior is absent.

Example 2: Wrong boundary condition type. A prompt specifies “convective cooling on the
right side” (q = h(T − T∞ ) with h = 2 W/m2 K, T∞ = 20 K). The LLM instead generates a
DirichletBC fixing T = 20 K. The code executes, but the boundary condition is physically wrong—
forced temperature instead of convective heat transfer, producing an ≈80 K boundary-region error in
the tested setup.

Example 3: Wrong coefficient value. The prompt specifies thermal conductivity k = 3 W/m · K.
The LLM generates k = 0.3, an order-of-magnitude error. The simulation runs and produces
plausible-looking contour plots, but heat diffuses ten times more slowly than intended.

Example 4: Missing source term (3D). A 3D simulation requires a volumetric heat source
(BodyForce kernel) representing internal heat generation with a Gaussian spatial profile (peak
80,000 W/m3 ). The LLM omits this kernel entirely, solving Laplace’s equation ∇2 T = 0 instead of
the Poisson equation −∇2 T = f (x). The entire internal-heating response vanishes despite successful
execution.

K      Prompt Templates
The following templates are used verbatim in the pipeline. All LLMs receive identical prompts; only
the natural-language description d varies per case.


                                                 23
PDE extraction prompt (Stage 1).
You are a MOOSE simulation physics expert. Given a natural language description
of a simulation problem, extract the physics contract as a JSON object.

Return ONLY valid JSON with this structure:
{ "variables": ["var1"],
  "terms": [
    {"variable": "var1", "operator": "diffusion", "coefficient": 45.0},
    {"variable": "var1", "operator": "time_derivative", "coefficient": null}
  ],
  "boundary_conditions": [
    {"variable":"var1","boundary":"left","bc_type":"Dirichlet","value":300.0}
  ],
  "initial_conditions": [{"variable":"var1","value":300.0,"ic_type":"constant"}],
  "time_scheme": "transient", "dimensions": 2 }

Valid operators: diffusion, time_derivative, source, reaction, advection,
  stress_divergence, coupled_force, curl_curl, inertia, pf_darcy_flux,
  pf_effective_stress, allen_cahn, cahn_hilliard, ns_continuity,
  ns_pressure, ns_viscous
Valid bc_type: Dirichlet, Neumann, Robin



SpecGen prompt (Stage 2).
You are a MOOSE simulation expert. Given a structured physics contract,
generate a complete MOOSE input file (.i format) that implements exactly
this physics.

CRITICAL: the coefficient values listed in the specification are EXACT.
You MUST use them verbatim in [Materials]. Do NOT substitute 1.0 or any
default value for a coefficient that is explicitly given.



PDE-Refine prompt (Stage 4).
The MOOSE input file you generated has specific physics-level errors
detected by automated PDE verification.

Current code: <code>
Violations detected: <structured violation report>

CRITICAL: Make ONLY minimal changes to fix the listed violations.
Do NOT modify kernels/BCs not mentioned in violations.
If "missing term": ADD the missing kernel without removing existing ones.
If "extra term": REMOVE only that specific kernel.
For coefficient violations: set the EXACT numerical value.



Exec-Repair prompt.
The MOOSE input file you generated may have errors. Please review
and fix any problems. Return the corrected MOOSE input file.



The Exec-Repair prompt is deliberately generic—no physics-specific guidance is provided, mirroring
standard self-debugging practice.

L     Case Study: Pipeline Walkthrough
We trace the full pipeline on framework_009, a medium-complexity coupled diffusion-reaction
problem (IFS: Direct=0.62 → PDE-Refine=0.98).

Natural-language prompt. “In a 1D domain (1 m), variable v (initially 10 everywhere) diffuses
and decays at rate 0.5/s, with left boundary at 10 and right at 0. Variable u (initially zero) diffuses
and is produced proportionally to the local value of v (coefficient 0.5). Left boundary of u is zero,
right boundary has zero flux. Simulate 3 s with dt = 0.05 s.”

Stage 1: PDE extraction. The LLM correctly identifies two coupled variables with: (1) v: diffusion
+ time derivative + reaction (decay −0.5v), Dirichlet BCs; (2) u: diffusion + time derivative + coupled
source (+0.5v), mixed BCs (Dirichlet left, Neumann right).

Direct failure. Direct generation (IFS = 0.62) omits the CoupledForce kernel linking u to v and
uses a DirichletBC instead of NeumannBC on the right boundary of u. The code executes without
error, but the two variables evolve independently—the intended coupling is entirely absent.


                                                            24
PDE-Refine correction. The IFS violation report identifies: (1) missing coupled_force term
on variable u; (2) wrong BC type on u/right (Dirichlet vs. Neumann). The LLM adds the missing
CoupledForce kernel and changes the BC type. After one refinement iteration, IFS reaches 0.98
(the residual 0.02 deficit is a minor coefficient relative-tolerance issue).

M     Execution-Based Refinement Failure Analysis
We document the characteristic failure mode of execution-only repair. In the registry audit, Exec-
Repair+Reg raises Exec for GPT-5.4 (82.3%) and DeepSeek V4 Flash (74.1%) but leaves large
executable-but-low-IFS fractions (40.0% and 39.1%), whereas PDE-Reg achieves higher mean IFS
and higher GoodExec.

Why PDE-Reg can also improve executability. PDE-Reg routes generation through an extracted
PDE contract and IFS-guided refinement, so generated files tend to preserve more consistent variable,
kernel, BC, and material references. Under this structural consistency, the registry can resolve
remaining mechanical gaps such as parameter wiring, material-property closure, and safe defaults.
Execution-only repair starts from Direct outputs with more accumulated inconsistencies; MOOSE
error logs usually surface the first encountered failure, so repairing the reported issue may leave later
object, variable, or material mismatches unresolved. This explains why PDE-Reg can improve both
GoodExec and Exec while still being a PDE-feedback method rather than an execution-optimization
method, consistent with the weaker-model stress tests in Table 22.

Deletion strategy. When the LLM encounters a kernel referencing an undefined variable or ma-
terial property, its typical repair strategy under generic self-debugging is deletion—removing the
problematic block to eliminate the error. This resolves the runtime error but can destroy physically
necessary kernels.

Example: mechanics_004 (Direct=0.61 → Exec-Repair=0.00). Direct generation produces a
partially correct elasticity input with StressDivergenceTensors kernels but references an unde-
fined elasticity tensor. The Exec-Repair prompt (“review and fix any problems”) leads the LLM to
remove the stress kernels entirely, producing a degenerate file that parses but encodes no physics. IFS
drops from 0.61 to 0.00.

Example: coupled_014 (Direct=0.90 → Exec-Repair=0.41). A high-quality direct generation
with a minor material property mismatch. Exec-Repair “fixes” the mismatch by restructuring the
entire file, inadvertently removing two of three boundary conditions and changing the time scheme.
IFS drops by −0.49.
These examples illustrate why execution-based feedback is insufficient: the LLM optimizes for “code
that runs” rather than “code that solves the intended PDE.”

N    Execution-Optimized Direct Generation
We include a diagnostic variant that explicitly optimizes Direct generation for MOOSE acceptance
rather than PDE fidelity. The model is asked to produce a minimal executable surrogate when the
full multiphysics realization is difficult. This is not a proposed method; it isolates the failure mode
induced by an execution-only objective.

Table 15: Execution-pressure diagnostic on a 20-case DeepSeek V4 Flash coupled slice. Execution
is measured by a short MOOSE acceptance audit. Exec-Optimized Direct substantially improves
executability, but creates executable semantic regressions; PDE-Reg shows that object realization
support can improve executability without abandoning the PDE-level contract.

              Method                   Mean IFS      Exec    Executable IFS drops > 0.1
              Direct                      0.711       4/20                 –
              Exec-Optimized Direct       0.722      16/20                 4
              PDE-Reg                     0.829      17/20                 –



                                                  25
Table 16: Qualitative example from coupled_012. The execution-optimized output is accepted by
MOOSE but solves a simplified surrogate rather than the intended coupled carburization problem.

    Aspect                Intended prompt                                 Exec-Optimized output
    Domain                2D steel component                              1D line
    Variables             temperature + carbon                            temperature only
    Terms                 heat time/diffusion + carbon time/diffusion     time + scalar diffusion
    Boundary conditions   temperature/carbon Dirichlet + oil convection   temperature Dirichlet left/right
    IFS / execution       Direct IFS = 0.894                              IFS = 0.415, execution pass



The example clarifies why execution should be treated as a mechanical signal rather than a semantic
objective. The generated file is easier for MOOSE to accept because it removes the carbon field,
carbon diffusion, carbon boundary conditions, the two-dimensional domain, and the convective
heat-flux boundary. IFS detects this drift because the reconstructed PDE no longer contains the
intended terms and boundary conditions.

O     MooseBench Benchmark Details
MooseBench contains 220 curated prompts (260 total, 40 excluded) spanning 7 expert-defined physics
families and 3 complexity tiers:

        • Simple (≤ 4 checkpoints): Single-physics, minimal configuration (e.g., steady-state diffu-
          sion with two BCs).
        • Medium (5–8 checkpoints): Single-physics with richer configuration or simple coupling.
        • Complex (≥ 9 checkpoints): Coupled multiphysics, multiple variables, or sophisticated
          boundary conditions.

Family balance. The heat-transfer families are larger because they supply many stable single- and
multi-physics MOOSE examples with clean PDE-level ground truth and executable source files, not
because they are selected to favor the proposed method. We therefore report per-family results in
Appendix P rather than relying only on aggregate means. The largest gains are not concentrated in
the heat subsets; coupled, elasticity, plasticity, THM, and phase-field families provide the harder tail
where PDE-grounded feedback has the most headroom.

Table 17: Canonical 220-case MooseBench family distribution, referenced from Section 5.
Complexity-tier Direct-IFS breakdowns are reported in Appendix P.

                           Physics Family                        Count     %
                           Transient Heat Conduction                 66   30.0
                           Steady-State Heat Conduction              36   16.4
                           TH-Coupled Porous Media Flow              30   13.6
                           Linear Elasticity                         28   12.7
                           THM-Coupled Porous Media Flow             20    9.1
                           Plasticity                                20    9.1
                           Phase-Field                               20    9.1
                           Total                                    220    100


Prompt design. All prompts describe physics in domain-expert language without referencing
MOOSE-specific constructs (kernel names, BC type names, variable naming conventions). Each
prompt is well-posed: it explicitly specifies all boundary conditions, initial conditions, material
properties (with numerical values), geometry, and time scheme.
Complex-tier prompts feature genuinely challenging physics: multi-variable coupling (up to 3
fields), specialized MOOSE kernels (HeatConduction, MatDiffusion, AnisotropicDiffusion,
CoupledForce, CoefReaction), mixed boundary condition types (Dirichlet + Neumann + con-
vective), and real-world scenarios (nuclear fuel pellet, cascade reaction A→B→C, thermal shock


                                                    26
with hydrogen permeation). The hardest case (coupled_007) involves 10 kernels, 3 variables, and 7
numerical coefficients.

Ground-truth construction. For each prompt, a reference MOOSE input file im-
plements the intended physics.            Ground truth Pgt is derived deterministically via
reconstruct_pde(), ensuring consistency with the kernel–PDE mapping M. Each GT includes
an acceptable_kernel_variants field auto-populated from the equivalent_to relations in the
mapping table, so that kernel variants normalized to the same PDE operator type (e.g., Diffusion ≡
ADDiffusion ≡ HeatConduction for the diffusion operator) are all accepted.
All 220 cases pass self-validation: IFS(Pgt , Pgt ) = 1.0 with zero MOOSE-term leakage in NL
descriptions.

Example prompts (one per tier). Simple (thermal_001): “A thin membrane separates two regions
with different concentrations of a dissolved substance. The bottom side is maintained at concentration
1, the top side at concentration 0. Assuming uniform diffusivity, find the steady-state concentration
distribution through the membrane.” GT: 1 term (diffusion), 2 Dirichlet BCs, steady. Results: Claude
Direct=1.00, GPT Direct=0.33, both SpecGen=PDE-Refine=1.00.
Medium (diffusion_004): “A substance with diffusivity 0.1 m2 /s spreads through a 2D square re-
gion (1 m × 1 m). The left boundary is held at zero concentration. A constant mass flux of 1
mol/(m2 s) enters from the right. The top and bottom are insulated. Starting from zero concentration
everywhere, simulate the transient evolution for 2 seconds using dt = 0.1 s.” GT: 2 terms (diffu-
sion + time_derivative), Dirichlet + Neumann BCs, transient. Results: Claude Direct=0.92, GPT
Direct=0.53; GPT SpecGen=0.80 (+51%).
Complex (coupled_007): “A three-step cascade reaction A → B → C occurs in a 1D tube (length
10 cm). Species A (D = 10−4 m2 /s) enters from the left at 5 mol/m3 and degrades at rate 1 s−1 to
produce B. Species B (D = 5×10−5 m2 /s) degrades at rate 0.5 s−1 to produce C. Species C (D =
2×10−5 m2 /s) is collected at the right (concentration 0). All other boundaries: zero flux. Simulate 1
second.” GT: 10 terms, 6 BCs, 3 variables, transient. Results: Claude Direct=0.73, SpecGen=0.90;
GPT Direct=0.22, SpecGen=0.26.

Full pipeline walkthrough (diffusion_004, GPT-4.1-mini). Stage 1 (PDE extraction): LLM
reads the NL prompt and produces a structured physics contract: {variable: c, operators: [diffusion
(D = 0.1), time_derivative], BCs: [Dirichlet on left (c = 0), Neumann on right (flux = 1)], time:
transient}.
Stage 2 (SpecGen): LLM generates a MOOSE input file guided by the spec, including
[Kernels] with Diffusion and TimeDerivative, [BCs] with DirichletBC and NeumannBC,
and [Materials] with diffusivity=0.1.
Stage 3 (PDE reconstruction): reconstruct_pde() parses the generated code into Pcode with 2
terms, 2 BCs, transient.
Stage 4 (IFS evaluation): IFS(Pgt , Pcode ) = 0.80. Two checkpoints fail: coefficient mismatch
(diffusivity resolved as string, not numeric) and BC value tolerance. Without spec guidance, Direct
scored 0.53 — missing the Neumann BC entirely and using steady-state instead of transient.

P    Additional Figures and Tables

Table 18: Severity-weight ablation on standard non-registry sweeps, referenced from Section 6.2. Val-
ues are paired mean deltas for PDE-Refine against Direct with 95% bootstrap CIs. Structural-uniform
scoring removes expert severity weights over term, BC, IC, and time checkpoints; coefficient/material
facts are evaluated separately by MCS.

    LLM                 Feedback Method        Severity-Weighted ∆         Structural-Uniform ∆
    Claude Sonnet 4.6   PDE-Refine           +0.072 [+0.042, +0.104]     +0.058 [+0.041, +0.076]
    GPT-5.4             PDE-Refine           +0.046 [+0.019, +0.077]     +0.021 [+0.005, +0.037]
    DeepSeek V4 Flash   PDE-Refine           +0.183 [+0.139, +0.228]     +0.107 [+0.076, +0.139]



                                                 27
Table 19: Framework conditions for instantiating the PDE-grounded diagnostic pattern, referenced
from Section 6.4.
Framework        Compositional semantics?               Direct op map?                 Shared contract?
MOOSE                        Yes                             Yes                              Yes
FEniCS / UFL                 Yes                  Yes, via symbolic forms      Yes (proof-of-concept, Section 6.4)
FreeFEM                      Yes                    Yes, via int2d text        Yes (proof-of-concept, Section 6.4)
FiPy                         Yes                 Yes, via term constructors    Yes (proof-of-concept, Section 6.4)
Devito                     Partial               Yes, via symbolic stencils    Yes (proof-of-concept, Section 6.4)
Firedrake                    Yes                   Yes, via UFL frontend                 Yes (expected)
deal.II                    Partial               Requires assembly analysis                  Partial
OpenFOAM        No direct weak-form exposure               Indirect                 Requires different target




Figure 7: Refinement convergence in an instrumented 220-case DeepSeek V4 Flash PDE-Refine
diagnostic run, referenced from Section 6.1. Mean GT IFS rises from 0.715 initially to 0.782 after
one refinement and 0.786 after two; internal IFS follows the same monotone trend. This diagnostic
supports the Nmax = 2 setting without replacing the main standard non-registry sweep in Table 1.



Table 20: Error taxonomy under Direct generation in 220-case sweeps, referenced from Section 6.3.
Entries are the fraction of cases where the corresponding IFS sub-dimension is imperfect; each model
column has n=220, so Wilson 95% half-widths are at most about 7 percentage points.

            Error Type                Dim.     Sonnet     GPT-5.4   GPT-mini      DeepSeek
            Missing/extra kernel      Term      35%         25%          87%         40%
            Wrong coefficient         Coeff     35%         45%          40%         37%
            Wrong/missing BC          BC        56%         60%          80%         66%
            Missing IC                IC         1%          1%           1%         1%
            Time scheme mismatch      Time      10%          8%          13%         19%




Table 21: BC error co-attribution under Direct generation across 220-case sweeps, referenced from
Section 6.3. The cohort is all Direct outputs with imperfect BC alignment (n=578). Shares use
Wilson 95% CIs; mean IFS uses bootstrap 95% CIs.

               BC-Error Cohort                 Share of BC Errors         Mean IFS
               Isolated BC only                19.0% [16.0, 22.4]    0.739 [0.706, 0.769]
               BC + coefficient only           22.8% [19.6, 26.4]    0.756 [0.734, 0.775]
               BC + term/time/IC               43.6% [39.6, 47.7]    0.253 [0.222, 0.286]
               BC + structural + coefficient   14.5% [11.9, 17.6]    0.440 [0.403, 0.476]




                                                   28
                                                     GoodExec           FalseExec             Non-executing
                 100                         8.6                                                                              12.3
                              16.8                              17.7                 13.2
                                                                                                         25.9
                  80                        31.4                                                                              27.7
                                                                                     30.0
                              40.0                              40.0
                  60
     Cases (%)


                                                                                                         39.1


                  40
                                            60.0                                     56.8                                     60.0
                              43.2
                  20                                            42.3
                                                                                                         35.0


                   0
                              Sonnet        Sonnet            GPT-5.4               GPT-5.4        DeepSeek V4 Flash    DeepSeek V4 Flash
                         Exec-Repair+Reg   PDE-Reg        Exec-Repair+Reg           PDE-Reg         Exec-Repair+Reg         PDE-Reg



Figure 8: Execution/fidelity quadrants under controlled object-realization infrastructure, referenced
from Section 6.2. Bars partition all 220 cases into GoodExec (Exec and IFS ≥ 0.85), FalseExec
(Exec but IFS < 0.85), and non-executing outputs. Execution-only repair leaves a large FalseExec
region, while PDE-Reg shifts more cases into GoodExec by adding PDE-grounded feedback.




Table 22: Weak-model registry stress tests under the same frozen object-realization registry. Exec
uses InitExec2; GoodExec and FalseExec are fractions of all 220 cases. These appendix rows test
registry-control transfer to weaker or lower-cost models without changing the main deployment-audit
model set.
                 LLM                       Method                           IFS         Exec        GoodExec              FalseExec
                 GPT-4.1-mini              Exec-Repair+Reg              0.346         25.5%             3.6%                 21.8%
                 GPT-4.1-mini              PDE-Reg                      0.703         63.2%            43.6%                 19.5%
                 Claude Haiku 4.5          Exec-Repair+Reg              0.735         74.1%            39.1%                 35.0%
                 Claude Haiku 4.5          PDE-Reg                      0.811         80.0%            48.2%                 31.8%
                 Gemini 3.1 Flash Lite     Exec-Repair+Reg              0.671         51.8%            23.6%                 28.2%
                 Gemini 3.1 Flash Lite     PDE-Reg                      0.828         85.0%            55.9%                 29.1%




Table 23: 220-case mixed-model ablation for PDE-Refine, referenced from Section 7.2. Rows cross
the model used for PDE extraction with the model used for code generation and refinement. Mixed
rows are diagnostic: a stronger extractor can improve a weaker generator, but the resulting fidelity
remains bounded by the downstream generator and below the strongest self pipeline. Errors are
retained model parse/extraction failures and are scored as IFS 0.

                 Configuration                                                                            Mean IFS             Errors
                 GPT-5.4 / DeepSeek V4 Flash diagnostic
                 GPT-5.4 extracts → GPT-5.4 generates                                                           0.792                 0
                 DeepSeek V4 Flash extracts → DeepSeek V4 Flash generates                                       0.765                12
                 GPT-5.4 extracts → DeepSeek V4 Flash generates                                                 0.772                 0
                 DeepSeek V4 Flash extracts → GPT-5.4 generates                                                 0.783                 8
                 Gemini 3.1 Flash Lite / DeepSeek V4 Flash diagnostic
                 Gemini 3.1 Flash Lite extracts → Gemini 3.1 Flash Lite generates                               0.796                0
                 DeepSeek V4 Flash extracts → DeepSeek V4 Flash generates                                       0.765                12
                 Gemini 3.1 Flash Lite extracts → DeepSeek V4 Flash generates                                   0.784                1
                 DeepSeek V4 Flash extracts → Gemini 3.1 Flash Lite generates                                   0.791                 7




                                                                       29
Table 24: Per-family IFS by method for 220-case results, referenced from Section 6.3. Bold = best
deployable method within each model block. PDE-Reg rows come from the registry execution audit
and use the same frozen object-realization registry as the registry-enabled baselines.
                                 Claude Sonnet 4.6                             GPT-5.4                      GPT-4.1-mini                     DeepSeek V4 Flash
Physics Family   n     Direct      PDE-Refine       PDE-Reg     Direct      PDE-Refine         PDE-Reg    Direct    PDE-Reg          Direct    PDE-Refine    PDE-Reg
Trans. Heat      66    0.834            0.826        0.886      0.826          0.848            0.866     0.436         0.657        0.738        0.834          0.901
SS Heat          36    0.911            0.871        0.891      0.836          0.863            0.882     0.650         0.677        0.786        0.878          0.880
TH-Coupled       30    0.774            0.815        0.889      0.825          0.824            0.859     0.349         0.770        0.719        0.758          0.847
Elasticity       28    0.685            0.931        0.947      0.870          0.879            0.911     0.194         0.890        0.519        0.915          0.946
THM-Coupled      20    0.493            0.641        0.679      0.367          0.602            0.745     0.131         0.624        0.182        0.519          0.551
Plasticity       20    0.487            0.812        0.807      0.684          0.731            0.806     0.223         0.755        0.395        0.813          0.840
Phase-Field      20    0.691            0.706        0.719      0.575          0.674            0.667     0.351         0.494        0.360        0.522          0.523




Table 25: Per-family IFS for registry execution-audit variants. All model blocks use the same frozen
object-realization registry; only PDE-Reg receives PDE/IFS feedback.
                                Claude Sonnet 4.6                          GPT-5.4                          GPT-4.1-mini                       DeepSeek V4 Flash

Physics Family   n      Exec-Repair+Reg         PDE-Reg       Exec-Repair+Reg        PDE-Reg       Exec-Repair+Reg        PDE-Reg        Exec-Repair+Reg      PDE-Reg

Trans. Heat      66             0.856            0.886             0.830               0.866             0.427             0.657                0.789            0.901
SS Heat          36             0.925            0.891             0.846               0.882             0.619             0.677                0.794            0.880
TH-Coupled       30             0.849            0.889             0.830               0.859             0.330             0.770                0.753            0.847
Elasticity       28             0.604            0.947             0.860               0.911             0.246             0.890                0.527            0.946
THM-Coupled      20             0.515            0.679             0.322               0.745             0.114             0.624                0.194            0.551
Plasticity       20             0.449            0.807             0.715               0.806             0.215             0.755                0.336            0.840
Phase-Field      20             0.712            0.719             0.580               0.667             0.325             0.494                0.461            0.523




Table 26: Full sub-dimensional IFS breakdown for standard non-registry and registry sweeps,
referenced from Section 6.3.
                      Sweep                                  Method                     Term        Coeff          BC           IC       Time
                      Sonnet 4.6                             Direct                     0.750       0.737        0.743      0.991        0.905
                                                             SpecGen                    0.892       0.435        0.785      0.991        0.918
                                                             PDE-Refine                 0.906       0.485        0.797      0.995        0.923
                      Sonnet 4.6 registry                    Exec-Repair+Reg            0.742       0.745        0.767      0.991        0.914
                                                             PDE-Reg                    0.924       0.633        0.828      0.995        0.923
                      GPT-5.4                                Direct                     0.827       0.627        0.728      0.991        0.923
                                                             SpecGen                    0.814       0.496        0.782      0.991        0.914
                                                             PDE-Refine                 0.869       0.599        0.770      0.995        0.918
                      GPT-5.4 registry                       Exec-Repair+Reg            0.827       0.638        0.730      0.991        0.914
                                                             PDE-Reg                    0.924       0.607        0.787      1.000        0.918
                      GPT-4.1-mini registry                  Direct                     0.344       0.626        0.441      0.991        0.868
                                                             Exec-Repair+Reg            0.332       0.608        0.433      0.991        0.873
                                                             PDE-Reg                    0.759       0.572        0.686      0.995        0.827
                      DeepSeek V4 Flash plain                Direct                     0.656       0.688        0.559      0.991        0.814
                                                             SpecGen                    0.742       0.534        0.643      0.891        0.759
                                                             PDE-Refine                 0.873       0.537        0.750      0.959        0.864
                      DeepSeek V4 Flash registry             Exec-Repair+Reg            0.677       0.729        0.585      0.991        0.841
                                                             PDE-Reg                    0.900       0.609        0.799      0.968        0.886




                                                                                30
                                            Direct IFS by Physics Family and Complexity


              Claude Sonnet 4.6                                                           GPT-5.4

      0.95           0.86            0.88                                   0.90            0.76           0.69
     (n=21)         (n=12)          (n=3)                                  (n=21)          (n=12)         (n=3)
                                                         1.0                                                      1.0

      0.93           0.85           0.79                                    0.92            0.85          0.77
     (n=6)          (n=33)         (n=27)                                  (n=6)           (n=33)        (n=27)
                                                         0.8                                                      0.8
      0.95           0.80           0.72                                    0.93             0.90         0.76
     (n=4)          (n=9)          (n=17)                                  (n=4)            (n=9)        (n=17)

                                                         0.6                                                      0.6
                                                               IFS




                                                                                                                        IFS
      0.65           0.81            0.46                                   0.91            0.91           0.72
     (n=9)          (n=13)          (n=6)                                  (n=9)           (n=13)         (n=6)

                                                         0.4                                                      0.4
      0.43           0.44            0.57                                   0.24             0.44          0.38
     (n=5)          (n=7)           (n=8)                                  (n=5)            (n=7)         (n=8)


                                                         0.2                                                      0.2
      0.50           0.48            0.48                                   0.78             0.71          0.58
     (n=6)          (n=7)           (n=7)                                  (n=6)            (n=7)         (n=7)



      0.83           0.79            0.49                0.0                0.68             0.59          0.50   0.0
     (n=4)          (n=9)           (n=7)                                  (n=4)            (n=9)         (n=7)



    Simple        Medium          Complex                                 Simple          Medium        Complex

                GPT-4.1-mini                                                        DeepSeek V4 Flash

      0.57           0.69            0.76                                   0.84            0.68           0.80
     (n=21)         (n=12)          (n=3)                                  (n=21)          (n=12)         (n=3)
                                                         1.0                                                      1.0

      0.23           0.44           0.47                                    0.73            0.78          0.68
     (n=6)          (n=33)         (n=27)                                  (n=6)           (n=33)        (n=27)
                                                         0.8                                                      0.8
      0.35           0.35           0.35                                    0.95             0.83         0.60
     (n=4)          (n=9)          (n=17)                                  (n=4)            (n=9)        (n=17)

                                                         0.6                                                      0.6
                                                               IFS




                                                                                                                        IFS
      0.18           0.28            0.01                                   0.54            0.54           0.45
     (n=9)          (n=13)          (n=6)                                  (n=9)           (n=13)         (n=6)

                                                         0.4                                                      0.4
      0.02           0.06            0.06                                   0.34             0.14          0.12
     (n=5)          (n=7)           (n=8)                                  (n=5)            (n=7)         (n=8)


                                                         0.2                                                      0.2
      0.15           0.27            0.09                                   0.46             0.33          0.40
     (n=6)          (n=7)           (n=7)                                  (n=6)            (n=7)         (n=7)



      0.33           0.44            0.18                0.0                0.83             0.34          0.12   0.0
     (n=4)          (n=9)           (n=7)                                  (n=4)            (n=9)         (n=7)



    Simple        Medium          Complex                                 Simple          Medium        Complex




Figure 9: Direct IFS by physics family and complexity tier for the four Direct sweeps. Each cell
shows mean IFS and sample count.




                                                                     31
                                                                        Direct IFS by Physics Family × Complexity
                                                            (annotations show Δ(SpecGen−Direct) where SpecGen is available)


                        Claude Sonnet 4.6                                                                                                             GPT-5.4




                                         +0.10                                                                                                                                                                     1.0
                      -0.06                                                                                                                   -0.07       -0.14+0.09
                                                      -0.14                                                                           -0.01
      -0.06
              -0.01                                                                     1.0                                      +0.04                         -0.14                                     1.0
                                                                                                                         -0.00                         -0.01           -0.11
                           +0.13     +0.24+0.14                                                                                                                             +0.15
                                -0.05+0.10                                             0.8                                                        +0.01                                                  0.8
                          -0.01 +0.25             +0.32
                                         -0.06+0.28
                                              +0.00+0.04
                                                                       +0.02
                                                              +0.07+0.24               0.6 IFS                                            +0.06
                                                                                                                                                  +0.29
                                                                                                                                                                   +0.07+0.03
                                                                                                                                                                   +0.04
                                                                                                                                                                             -0.08      -0.00+0.01
                                                                                                                                                                                                         0.6 IFS
                                                          +0.42                        0.4                                                                    +0.19                 +0.09               0.4
                                                                                       0.2                                                                                                              0.2        0.8
                                                                                       0.0                                                                                                              0.0
                                                                                    Phas                                                                                                             Phas
                                                                                Plastic e-Field                                                                                                  Plastic e-Field
 Simple                                                                   THM          ity                          Simple                                                                  THM         ity
                                                                      Elast       -Cou                                                                                                  Elast      -Cou
                                                                            icity      pled                                                                                                  icity      pled
          Medium                                                   TH-C                                                      Medium                                                  TH-C
                                                              Trans.    oupled                                                                                                  Trans.    oupled
                                                                     Heat                                                                                                              Heat
                              Complex                     SS H
                                                               eat                                                                              Complex                     SS H
                                                                                                                                                                                 eat                               0.6


                              GPT-4.1-mini                                                                                             DeepSeek V4 Flash




                                                                                                                                                                                                                         IFS
                                                                                                                                                                                                                   0.4
                                                                                                                                                              +0.07
                                                                                                                                      -0.14
                                                                                        1.0                                                                                                              1.0
                                                                                                                         +0.06
                                                                                        0.8                                   +0.27
                                                                                                                                              +0.21
                                                                                                                                                       +0.06
                                                                                                                                                        +0.33                                            0.8
                                                                                                                                                  +0.02
                                                                                       0.6 IFS                                                     -0.08    +0.24
                                                                                                                                                                       +0.50
                                                                                                                                                                            +0.19
                                                                                                                                                                                                         0.6 IFS
                                                                                                                                          +0.12
                                                                                                                                                              +0.07
                                                                                                                                                                   +0.13+0.00           +0.27                      0.2
                                                                                       0.4                                                                                   +0.17                      0.4
                                                                                                                                                                  +0.26                     +0.02
                                                                                       0.2                                                                                                              0.2
                                                                                                                                                                                 +0.28
                                                                                       0.0                                                                                                              0.0
                                                                                    Phas                                                                                                             Phas
                                                                                Plastic e-Field                                                                                                  Plastic e-Field
 Simple                                                                   THM          ity                          Simple                                                                  THM         ity
                                                                      Elast       -Cou                                                                                                  Elast      -Cou
                                                                                       pled                                                                                                             pled
          Medium                                                   TH-C
                                                                            icity                                            Medium                                                  TH-C
                                                                                                                                                                                             icity                 0.0
                                                              Trans.    oupled                                                                                                  Trans.    oupled
                              Complex                     SS H       Heat                                                                       Complex                     SS H       Heat
                                                               eat                                                                                                               eat




Figure 10: Companion family–complexity Direct IFS view. Bars compare Direct baselines by expert
family and complexity tier for each model; annotations report ∆(SpecGen–Direct) where SpecGen is
available.




                                                                                                         32
                                                                         Sub-Dimensional IFS Profile by Method


                                                                                        Direct                                                                                                             Direct
            Claude Sonnet 4.6                                                           SpecGen
                                                                                                                                                    GPT-5.4                                                SpecGen
                                                         Coeff                                                                                                            Coeff
                                                                                        PDE-Refine                                                                                                         PDE-Refine
                                                                                        Exec-Repair+Reg                                                                                                    Exec-Repair+Reg
                                                                                        PDE-Reg                                                                                                            PDE-Reg

 BC                                                                                                                  BC


                                                                                  1.0                                                                                                                1.0
                                                                            0.8                                                                                                                0.8
                                                                   0.6                                                                                                                   0.6
                                                           0.4                                                                                                                   0.4
                                                   0.2                                                                                                              0.2
                                                                                          Term                                                                                                               Term




 IC                                                                                                                  IC




                                                         Time                                                                                                             Time

                                                                                        Direct                                                                                                             Direct
                                     GPT-4.1-mini                                       Exec-Repair+Reg
                                                                                                                                            DeepSeek V4 Flash                                              SpecGen
                                                         Coeff                                                                                                            Coeff
                                                                                        PDE-Reg                                                                                                            PDE-Refine
                                                                                                                                                                                                           Exec-Repair+Reg
                                                                                                                                                                                                           PDE-Reg

 BC                                                                                                                  BC


                                                                                  1.0                                                                                                                1.0
                                                                            0.8                                                                                                                0.8
                                                                   0.6                                                                                                                   0.6
                                                           0.4                                                                                                                   0.4
                                                   0.2                                                                                                              0.2
                                                                                          Term                                                                                                               Term




 IC                                                                                                                  IC




                                                         Time                                                                                                             Time




Figure 11: Sub-dimensional IFS profiles for standard non-registry and registry variants. Registry-only
execution repair improves object realization but does not dominate the structural term/BC dimensions;
PDE-Reg gives the largest structural lift for weak models.

                                                                                  Residual Error Across the PDE-Grounded Pipeline
                                                                                                                    Direct error            Contract error                 Final-code error
                                             0.7                                                                          0.65


                                             0.6
             Mean residual error (1 - IFS)




                                             0.5
                                                                                                                                                             0.40
                                             0.4
                                                                                                                                          0.30
                                             0.3   0.26                                    0.24
                                                            0.20                                   0.21
                                                                                                                                   0.19                                   0.19
                                             0.2                     0.15
                                                                                                            0.16                                                                       0.15


                                             0.1

                                             0.0
                                                   Claude Sonnet 4.6                              GPT-5.4                    GPT-4.1-mini                    DeepSeek V4 Flash



Figure 12: Residual-error view for PDE-grounded methods. Bars compare Direct error, extracted-
contract error, and final-code error, separating the PDE-comprehension bottleneck from the final
synthesized-code fidelity.


                                                                                                               33
