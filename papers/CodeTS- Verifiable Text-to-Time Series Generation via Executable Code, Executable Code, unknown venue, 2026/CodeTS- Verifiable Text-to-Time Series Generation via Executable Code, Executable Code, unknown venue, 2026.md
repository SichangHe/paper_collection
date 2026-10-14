                                         CodeTS: Verifiable Text-to-Time Series Generation via
                                                           Executable Code


                                             Xudong Yuan1 Shunyu Liu2 Tongya Zheng1 Huiping Zhuang3 Mingli Song1 Kaixuan Chen1
                                                                      1
                                                                        Zhejiang University, Hangzhou, China
                                                                  2
                                                                    Nanyang Technological University, Singapore
                                                            3
                                                              South China University of Technology, Guangzhou, China
arXiv:2609.15393v1 [cs.LG] 14 Sep 2026




                                                                                         Abstract
                                                     Text-to-Time Series Generation (Text-to-TS) provides a promising paradigm for
                                                     synthesizing time series from natural language, enabling scenario-specific gener-
                                                     ation when real observations are scarce or costly to acquire. However, existing
                                                     methods typically lack an explicit mechanism for deriving generation logic from
                                                     textual descriptions to guide time series synthesis. In this paper, we propose
                                                     CodeTS, a verifiable framework that uses code as an intermediate generation
                                                     interface, reformulating Text-to-TS generation as a Text-to-Code-to-TS process.
                                                     CodeTS first maps textual temporal descriptions into an explicit code space, where
                                                     executable code specifies how textual requirements shape target temporal patterns,
                                                     and then obtains the time series through code execution. To learn this code gener-
                                                     ation process reliably without real code annotations, CodeTS constructs aligned
                                                     Text-Code-TS triplets from structured temporal attributes for supervised initializa-
                                                     tion. More importantly, we further design multi-stage execution-based rewards
                                                     that verify format validity, code executability, and time series quality, enabling
                                                     real Text-TS pairs to provide training signals for Reinforcement Learning with
                                                     Verifiable Rewards (RLVR). Extensive experiments on eight benchmarks across
                                                     short, medium, and long generation lengths demonstrate that CodeTS provides a
                                                     strong zero-shot solution for Text-to-TS generation, outperforming LLM-based
                                                     baselines and achieving better averaged results than supervised generative base-
                                                     lines trained on the target datasets. The anonymized code repository is available at
                                                     https://anonymous.4open.science/r/CodeTS-54DA.


                                         1    Introduction
                                         Time series data are pervasive across real world (a) Text-to-TS Process
                                         domains such as finance, healthcare, energy sys-                        Latent Space
                                                                                                                                Decode
                                         tems, transportation networks, and climate sci-                            Implicit
                                         ence [Sezer et al., 2020, Faust et al., 2018, Deb        Text                                   TS
                                         et al., 2017, Ermagun and Levinson, 2018, An (b) Text-to-Code-to-TS Process
                                         et al., 2025], where they support fundamental                           Code Space
                                                                                                                                Execute
                                         tasks including forecasting, classification, and                           Explicit
                                         anomaly detection [Wen et al., 2022]. These              Text                                    TS
                                         tasks require representative data that adequately
                                         cover diverse temporal patterns and characteris- Figure 1: Illustration of the Text-to-TS process and
                                         tic behaviors across application contexts. How- the proposed Text-to-Code-to-TS process.
                                         ever, such comprehensive time series data are often scarce and costly to obtain, especially when the
                                         target patterns involve rare events, privacy restricted sensor measurements, or expert descriptions of
                                         temporal behaviors [Ge et al., 2025, Wu et al., 2025, Wen et al., 2021]. As a result, many important
                                         temporal patterns remain insufficiently covered, limiting model performance in downstream scenarios

                                         Preprint.
where such patterns are most critical. Therefore, this underscores the need for time series generation
methods that synthesize samples with targeted temporal characteristics rather than simply increasing
the number of synthetic samples.
Existing time series generation methods have mainly focused on learning temporal distributions from
observed series and synthesizing new samples with similar statistical properties [Jeong et al., 2025,
Yoon et al., 2019, Lee et al., 2023, Yuan and Qiao, 2024]. To improve controllability, conditional
generation methods further incorporate auxiliary signals, such as metadata, labels, or historical
observations, to guide the synthesis process [Narasimhan et al., 2024, Shankar et al., 2025, Lin et al.,
2020, Ni et al., 2020, Liao et al., 2024]. However, these forms of conditioning are often predefined
and structured, making it difficult to specify fine-grained temporal requirements [Gu et al., 2025],
such as desired trends, periodicity, amplitude changes and local events, in a flexible and intuitive
manner. Natural language, in contrast, provides a more expressive interface for specifying such target
temporal behaviors, thereby motivating time series generation from text.
Following this direction, Text-to-Time Series Generation (Text-to-TS) has emerged as a promising
paradigm for natural language-guided time series synthesis, enabling compositional temporal require-
ments to be specified in a flexible form. Existing approaches can be broadly divided into supervised
Text-to-TS generation methods and LLM-based generation methods. The former learn Text-to-TS
mappings from paired Text-TS data, typically by aligning textual and temporal representations and
training neural generators to synthesize numerical sequences [Gu et al., 2025, Ge et al., 2025, Li et al.,
2025, Zhang, 2026]; the latter use large language models either through prompting or by autoregres-
sively modeling textualized time series representations to synthesize temporal data [Rousseau et al.,
2025, Xie et al., 2025, Wang et al., 2025, Guan et al., 2025]. However, these existing methods connect
textual descriptions and temporal patterns through latent representation spaces (Fig. 1(a)), where
the transformation from textual semantics to temporal patterns remains implicit and underspecified,
which leaves the Text-TS semantic gap insufficiently addressed and makes the underlying generation
logic difficult to verify or optimize. This raises a key challenge:

  How to develop an explicit intermediate interface that maps textual requirements into time
  series generation logic, while making the process verifiable and optimizable to better bridge the
  semantic gap between textual descriptions and temporal dynamics?

In this paper, we propose CodeTS, a novel Text-to-Code-to-TS framework that bridges the semantic
gap between textual descriptions and temporal dynamics by introducing executable code as an
explicit intermediate interface, as illustrated in Fig. 1(b). Specifically, CodeTS decomposes Text-to-
TS generation into Code Generation (CodeGen), which grounds textual temporal requirements into
executable generation programs, and Code Execution (CodeExe), which executes these programs to
produce time series. This decomposition transforms the implicit Text-to-TS mapping into an explicit
generation process, enabling verification through execution while allowing the code generation policy
to be initialized with supervised learning and further optimized through reinforcement learning. To
support this two-stage learning process, we construct aligned Text-Code-TS triplets from structured
temporal attributes for supervised initialization, and design multi-stage execution-based rewards over
format validity, code executability, and time series quality for reinforcement learning optimization.
Finally, extensive experiments on eight benchmarks across different generation lengths demonstrate
the effectiveness of CodeTS compared with state-of-the-art baselines.
Our main contributions are summarized as follows:
    • We are the first to reformulate Text-to-TS generation as a Text-to-Code-to-TS process, trans-
      forming the implicit mapping between text and time series into an explicit code space. This
      formulation provides a new perspective for mitigating the gap between language semantics
      and temporal dynamics.
    • We propose CodeTS, a novel framework that implements Text-to-Code-to-TS with normalized
      code generation and sandboxed execution, making time series generation explicit, verifiable,
      and optimizable via execution-based rewards.
    • We develop aligned Text-Code-TS triplets for supervised initialization and multi-stage exe-
      cution rewards for reinforcement learning. These designs provide code-level supervision and
      multi-stage verification over format validity, code executability, and time-series quality.



                                                    2
      • Extensive experiments on eight benchmarks across different generation lengths demonstrate
        the effectiveness of CodeTS compared with state-of-the-art supervised Text-to-TS methods
        and LLM-based zero-shot baselines.

2     Related Work
Time Series Generation and Text-to-TS Generation. Deep generative models for time series have
progressed from GAN-based approaches, such as TimeGAN [Yoon et al., 2019] and GT-GAN [Jeon
et al., 2022], to diffusion and discrete-latent models, such as Diffusion-TS [Yuan and Qiao, 2024]
and TimeVQVAE [Lee et al., 2023]. Recent Text-to-TS studies extend conditional generation to
natural language, including VerbalTS [Gu et al., 2025], T2S [Ge et al., 2025], BRIDGE [Li et al.,
2025], and textualized autoregressive generation methods [Rousseau et al., 2025]. Despite their
differences in supervision, architecture, and generation strategy, existing methods mostly rely on
implicit representations, making the gap between textual requirements and temporal patterns difficult
to inspect and directly optimize.
Language Models and Foundation Models for Time Series. Recent studies have explored lan-
guage models and foundation models for time series forecasting, representation learning, and mul-
timodal understanding. Representative examples include LLM-based forecasting methods such
as GPT4TS [Zhou et al., 2023] and Time-LLM [Jin et al., 2024], foundation models such as
Chronos [Ansari et al., 2024], and multimodal time series systems such as ChatTime [Wang et al.,
2025] and TimeOmni-1 [Guan et al., 2025]. These works highlight the potential of language
model-based time series modeling, but still rely on numerical, discretized, or textualized sequence
representations, leaving the translation from textual requirements to temporal patterns largely implicit.
Additionally, TS2Code [Tan et al., 2026] recently explores code-based time series understanding
by generating code from time series visualizations, but it focuses on reconstruction and forecasting
rather than text-conditioned generation.

3     Problem Definition
Text-to-TS generation aims to synthesize a time series conditioned solely on a natural language
description. Following the setting in [Ge et al., 2025], the dataset with N samples can be denoted as:
                                          D = {(xi , di )}N
                                                          i=1 ,                                       (1)
where xi ∈ RLi denotes a univariate time series of length Li and di denotes its corresponding
description. The generated time series x̂i is expected to match the target time series xi , which can be
written as:
                        min E(xi ,di )∼D ∥xi − x̂i ∥22 ,
                                                      
                                                              x̂i ∼ πθ (· | d),                      (2)
                           θ
where πθ denotes a conditional generative model. In this formulation, πθ can be instantiated as a
text-conditioned diffusion or as an LLM-based generator. However, the generation logic that maps
textual semantics to temporal dynamics remains implicit.

4     Methodology
This section presents CodeTS, which reformulates Text-to-TS generation as Text-to-Code-to-TS: a
textual description is first translated into executable code, and the time series is then obtained by code
execution. We first formalize this formulation in Sec. 4.1, then describe how aligned Text-Code-TS
triplets are constructed to provide code-level supervision in Sec. 4.2. We next introduce execution-
based rewards for evaluating generated code and its executed time series in Sec. 4.3, followed by the
supervised initialization and RLVR-based [Lambert et al., 2024] optimization procedure in Sec. 4.4.

4.1    Text-to-Code-to-TS Formulation

Conventional Text-to-TS generation directly maps a natural language description d to a numerical
sequence x, leaving the mapping implicit and making it difficult to inspect whether key temporal
factors are reflected in the output. Executable code addresses this limitation by externalizing textual
temporal requirements into executable generation programs, making the Text-to-TS mapping explicit,


                                                    3
Figure 2: Overview of CodeTS. (a) Synthetic Text-Code-TS triplets are constructed from structured
temporal attributes. (b) Execution-based rewards verify normalized format, code executability, and
time series quality. (c) The model is first initialized on synthetic triplets by SFT and then optimized
on real Text-TS pairs with execution-based rewards and GRPO. At inference time, CodeTS maps
input text to normalized code and executes it to generate the target time series.

verifiable through execution, and optimizable with execution-based rewards. To this end, we formu-
late Text-to-TS generation as a Text-to-Code-to-TS process (Fig. 1(b)). Given a natural language
description d, the model generates a code program y from the code space Y:
                                             y ∼ πθ (· | d),                                           (3)
where πθ denotes the code generation policy. The generated time series is then obtained by executing
the code:
                                             x̂ = Execute(y).                                           (4)
Therefore, the Text-to-TS generation is formulated as the composition of code generation and
execution:
                                               πθ    Execute
                                            d −→  y −−−−−→ x̂.                                          (5)
This formulation changes the generation target from raw numerical sequences to executable generation
logic, which is well suited to time series because temporal patterns such as trends, periodic fluctuations,
local events, and noise can be explicitly specified and combined in code. However, real world Text-TS
pairs lack executable code, which motivates the rule-based construction of synthetic Text-Code-TS
triplets in the next subsection.

4.2   Text-Code-TS Triplet Construction

The Text-to-Code-to-TS formulation requires learning a mapping from textual descriptions to exe-
cutable code, whereas real world Text-to-TS datasets typically provide only Text-TS pairs without
corresponding code annotations. This motivates the construction of synthetic Text-Code-TS triplets,
which provide code-level supervision for initializing the framework.
Inspired by the synthetic data construction in [Xie et al., 2025, Lin et al., 2026], we adopt a rule-based
triplet construction strategy. Each triplet is generated from a shared structured temporal attribute
aj , which specifies the temporal factors to be realized, including sequence length, trend, seasonality,
local events, and noise characteristics:
                            aj = alen    trend season event noise
                                                                       
                                    j , aj     , aj     , aj   , aj       ∈ A,                          (6)
where A denotes the structured temporal attribute space. For synthetic data construction, aj serves
as a shared source for generating the description, code, and time series, thereby aligning the three


                                                    4
elements of each triplet:
                   dj = Gtext (aj ),      yj = Gcode (aj ), xj = Execute(yj ),                (7)
where Gtext and Gcode generate the textual description and executable code from aj , respectively.
The synthetic triplet dataset is then defined as:
                                       Dsyn = {(dj , yj , xj )}N
                                                               j=1 .
                                                                 s
                                                                                                        (8)
In each triplet, dj is the textual input, yj is the reference code for supervised code generation, and xj
is the execution result of yj . Since all three elements are generated from the same temporal attribute
aj , the triplet is aligned by construction.
Normalized Code Representation. Although the above construction provides aligned descriptions,
code, and time series, reliable parsing, execution, and reward computation require a structured
code format. We therefore represent each reference code yj as a normalized JSON object with two
fields: params, which stores temporal parameters such as length, trend, seasonality, local events, and
noise settings, and code, which defines a Python function that generates the time series from these
parameters. A concrete example is provided in Appendix B.

4.3   Execution-Based Reward Design

Given a textual description d, the model samples a code y ∼ πθ (· | d). Following Eq. (4), the
code is executed to obtain the generated time series x̂ if it passes the required format and execution
checks. The reward is designed to evaluate both the generated code and its executed output, covering
normalized format validity, executable correctness, and time-series quality.
Formally, the overall reward is defined as
                 R(y, x, d) = λfmt Rfmt (y) + λexec Rexec (y) + Ivalid (y)λts Rts (x̂, x),              (9)
where Rfmt evaluates whether the output follows the normalized params/code schema, Rexec
evaluates whether the generated code is safe and executable, and Rts , defined in Eq. (10), measures
the quality of the executed time series. The indicator Ivalid (y) equals 1 only when the generated
output can be correctly parsed and executed; otherwise, the sequence-level reward is not assigned.
This design prevents invalid code from receiving misleading feedback based on time-series similarity.
After successful execution, the generated time series x̂ is compared with the paired target series x.
The time series reward is defined as a weighted combination of complementary criteria:
      Rts (x̂, x) = λlen Rlen (x̂, x) + λerr Rerr (x̂, x) + λcorr Rcorr (x̂, x) + λstat Rstat (x̂, x). (10)
Here, Rlen checks length consistency, Rerr measures pointwise numerical accuracy, Rcorr evaluates
temporal-pattern alignment through correlation, and Rstat compares distributional statistics such as
scale or variance. Together, these terms assess whether the executed code produces a time series
that matches the paired target sequence in both local values and global temporal structure. Detailed
definitions of these rewards are provided in Appendix C.
This reward design turns executable generation into a verifiable optimization signal. For real Text-
to-TS pairs where reference code is unavailable, the model can still be optimized through format
validation, execution checking, and direct comparison between the generated and target time series.

4.4   Initialization and Execution-based Optimization

The model is trained in two stages. First, supervised initialization is performed on the synthetic
triplets in Eq. (8), where each textual description is paired with a reference executable code. The
second stage further optimizes the initialized code generation model on real Text-TS pairs using the
reward in Eq. (9), where no reference code is available.
Supervised Code Initialization. Given the synthetic triplet dataset Dsyn = {(dj , yj , xj )}N            s
                                                                                                       j=1 ,
the supervised stage trains the model to generate the reference code yj conditioned on the textual
description dj . The executed series xj is not used as a direct generation target in this stage; instead, it
verifies that the reference code is executable and aligned with the temporal attribute used to construct
the triplet. The supervised fine-tuning objective is defined as the negative log-likelihood of the
reference code:
                                                        |y|
                                                       X
                          LSFT (θ) = −E(d,y,x)∼Dsyn         log πθ (yt | y<t , d).                     (11)
                                                         t=1


                                                     5
This stage teaches the model the normalized params/code format and initializes the mapping from
textual temporal descriptions to executable generation code. Such initialization is important for the
subsequent reinforcement learning stage, where invalid or non-executable code would otherwise lead
to sparse and noisy feedback.
Execution-Guided Policy Optimization. After supervised initialization, the model is further
optimized on real Text-TS pairs, where no reference code is available. For each description di , the
policy samples a group of G candidate code. Each candidate is checked, executed when valid, and
                                                           (k)
scored by the execution-based reward in Eq. (9). Let Ri denote the reward of the k-th sampled code
for the pair (di , xi ). The relative advantage used by GRPO [Shao et al., 2024] is computed within the
sampled group:
                                               (k)             (j)     
                                       (k)   Ri − mean {Ri }G      j=1
                                     Âi =             (j)              ,                         (12)
                                                std {Ri }G  j=1 + ε
where ε is a small constant for numerical stability. This group-relative normalization encourages
code that outperform other candidates generated for the same description, while suppressing invalid
or low-quality code.
The policy is updated with GRPO using the relative advantages. For stable optimization, we maximize
a clipped surrogate objective with KL regularization [Schulman et al., 2015] toward the supervised
initialization policy:
                               "    G
                                                                                   #
                                  1 X (k)                                        
                JGRPO (θ) = E          ℓi (θ) − βDKL πθ (· | di )∥πSFT (· | di ) ,             (13)
                                 G
                                       k=1

where the clipped surrogate term is:
                             Tk
               (k)       1 X       
                                     (k)      (k)       (k)                   (k) 
              ℓi (θ) =          min ρi,t (θ)Âi , clip ρi,t (θ), 1 − ε, 1 + ε Âi    .             (14)
                         Tk t=1
                                              (k)
Here, Tk is the total length of output code, ρi,t (θ) is the policy ratio between the current policy and
the sampling policy, ε is the clipping threshold, and β controls the KL regularization strength. The
clipped surrogate favors candidates with higher relative advantages while limiting overly large policy
updates, and the KL term keeps the policy close to the supervised initialization policy.
Overall, the training process is summarized as:
                θSFT = arg min LSFT (θ),            θfinal = arg max JGRPO (θ; θSFT ).             (15)
                               θ                                 θ

The supervised stage initializes executable code generation, and the execution-guided stage improves
generation quality through verifiable feedback from code execution and TS comparison.

5     Experiments
5.1   Experimental Setup

Datasets. We evaluate on eight public benchmarks, including ETTh1, ETTh2, ETTm1, ETTm2 [Wu
et al., 2021], Electricity, Exchange, Weather [Zhou et al., 2021], and Web [Casado-Vara et al., 2021],
with generation lengths of 96, 192, and 336. Details of the text-conditioned benchmark and the real
Text-TS data used for RLVR training are provided in Appendix D.
Metrics. We report Mean Squared Error (MSE), Dynamic Time Warping distance (DTW) [Sakoe
and Chiba, 2003], and Pearson correlation as general quality metrics. For LLM-based zero-shot
baselines, we additionally report Pass@1 [Chen et al., 2021] Success Rate (SR), defined as the
fraction of samples whose outputs can be successfully parsed and, when applicable, executed.
Detailed introductions are provided in Appendix E.
Baselines. We compare CodeTS with four supervised generative baselines, including Diffusion-
TS [Yuan and Qiao, 2024], T2S [Ge et al., 2025], VerbalTS [Gu et al., 2025], and TimeVQVAE [Lee
et al., 2023]; Diffusion-TS and TimeVQVAE use text-conditioning adapters following Ge et al. [2025].
To adapt non-text generative baselines to the Text-to-TS setting, Diffusion-TS and TimeVQVAE are


                                                    6
Table 1: Comparison with supervised time series generation baselines. CodeTS is evaluated zero-shot,
while all supervised baselines are trained separately on each target dataset and generation length.
Bold and underline denote the best and second-best results.
                          CodeTS               VerbalTS                T2S              Diffusion-TS          TimeVQVAE
Datasets    Length MSE↓ DTW↓ Pearson↑ MSE↓ DTW↓ Pearson↑ MSE↓ DTW↓ Pearson↑ MSE↓ DTW↓ Pearson↑ MSE↓ DTW↓ Pearson↑
            96     0.0202 0.0799 0.8136 0.1438 0.1794 0.0600 0.1114 0.1740 -0.0253 0.1286 0.1721 0.1351 0.0575 0.1545 0.3571
ETTh1       192    0.0219 0.0808 0.7714 0.1430 0.1847 0.0889 0.1242 0.1626 -0.0331 0.0933 0.1415 0.1620 0.0578 0.1533 0.3005
            336    0.0232 0.0823 0.7242 0.1895 0.2368 0.0414 0.0839 0.1522 -0.0474 0.0835 0.1385 0.2414 0.0666 0.2061 0.0608
            96     0.0305 0.1041 0.7302 0.1238 0.1891 0.2522 0.1126 0.1931 0.0150 0.1259 0.2118 0.2064 0.0741 0.1769 0.2389
ETTh2       192    0.0295 0.0999 0.6835 0.1598 0.2220 0.0668 0.1277 0.2078 0.0199 0.1465 0.2312 0.1246 0.0852 0.1977 0.2234
            336    0.0292 0.0993 0.6456 0.2531 0.3584 0.0336 0.1003 0.1945 0.0251 0.1059 0.1868 0.1001 0.0935 0.2368 0.0202
            96     0.0161 0.0669 0.8713 0.0723 0.1139 0.4928 0.1143 0.1998 0.0069 0.1480 0.1824 0.0386 0.0830 0.2338 0.0434
ETTm1       192    0.0181 0.0685 0.8338 0.0854 0.1274 0.3767 0.1104 0.1900 -0.0123 0.1246 0.1595 0.1136 0.0679 0.1647 0.3147
            336    0.0276 0.0704 0.7341 0.1429 0.1786 0.0011 0.0730 0.1564 0.0257 0.1124 0.1450 0.0264 0.0619 0.1933 0.0000
            96     0.0279 0.0982 0.7944 0.0883 0.1354 0.4486 0.1604 0.2525 0.0125 0.1820 0.2372 0.0266 0.0882 0.2253 0.0629
ETTm2       192    0.0295 0.1016 0.7532 0.1091 0.1608 0.2999 0.1167 0.1925 0.0298 0.1434 0.1994 0.1579 0.0705 0.1556 0.3092
            336    0.0332 0.0968 0.6689 0.1305 0.1830 -0.0058 0.0945 0.1838 0.0331 0.1320 0.1940 0.0118 0.0671 0.2117 -0.0111
            96     0.0159 0.0622 0.8599 0.0741 0.0874 0.4925 0.1636 0.2468 0.0023 0.1566 0.1839 0.0374 0.0907 0.2312 0.0108
Weather 192        0.0159 0.0592 0.8427 0.0787 0.0930 0.4415 0.1652 0.2370 0.0284 0.1566 0.1894 0.0188 0.0812 0.2114 0.0044
            336    0.0213 0.0648 0.7701 0.1344 0.1409 -0.0026 0.1105 0.1951 0.0219 0.1532 0.1986 0.0097 0.0721 0.2008 -0.0045
            96     0.0301 0.0923 0.8112 0.0458 0.0968 0.7666 0.1725 0.2206 0.0629 0.1033 0.1389 0.5250 0.0559 0.1027 0.7242
Electricity 192    0.0284 0.0845 0.7982 0.0461 0.1024 0.7372 0.1515 0.1869 0.1028 0.0966 0.1421 0.5896 0.0657 0.1341 0.6669
            336    0.0280 0.0824 0.7811 0.0533 0.1197 0.7024 0.1121 0.1550 0.1137 0.1020 0.1585 0.5294 0.0670 0.1620 0.6459
            96     0.0795 0.1643 0.4815 0.2182 0.2499 0.0318 0.1296 0.2235 0.0013 0.2110 0.2906 0.0516 0.1660 0.3090 0.2021
Exchange 192       0.0837 0.1481 0.5180 0.2714 0.2979 0.0083 0.1777 0.2634 0.0059 0.2064 0.2794 0.1936 0.1038 0.2646 0.0447
            336    0.0870 0.1449 0.5159 0.2336 0.3207 0.0047 0.1090 0.1921 -0.0246 0.1315 0.2021 0.1139 0.0957 0.2508 0.0040
            96     0.0326 0.1162 0.3672 0.0518 0.0940 0.0533 0.0727 0.1597 -0.0147 0.0582 0.1169 -0.0123 0.0430 0.1274 -0.0411
Web         192    0.0246 0.1002 0.3024 0.0343 0.0733 0.0577 0.0391 0.1056 -0.0147 0.0360 0.0909 -0.0080 0.0277 0.0925 -0.0270
            336    0.0175 0.0823 0.2664 0.0273 0.0751 0.0203 0.0212 0.0749 0.0209 0.0219 0.0662 0.0463 0.0171 0.0653 0.1078
     Average       0.0321 0.0938 0.6808 0.1213 0.1675 0.2279 0.1148 0.1883 0.0148 0.1233 0.1774 0.1433 0.0733 0.1859 0.1774



Table 2: Comparison with zero-shot LLM baselines for time series generation. SR denotes the
pass@1 execution success rate. † indicates values that are approximately 100.0%. Bold and underline
denote the best and second-best results.
                               CodeTS                   TimeOmni-1                 ChatTime                  GPT4o-mini
Datasets    Length MSE↓ DTW↓ Pearson↑ SR(%)↑ MSE↓ DTW↓ Pearson↑ SR(%)↑ MSE↓ DTW↓ Pearson↑ SR(%)↑ MSE↓ DTW↓ Pearson↑ SR(%)↑
            96     0.0202 0.0799 0.8136 100.0 0.1749 0.2736 0.0669 87.1 0.1826 0.2772 0.0063  92.0 0.1721 0.3344 0.0810  97.3
ETTh1       192    0.0219 0.0808 0.7714 100.0 0.1592 0.2644 0.0660 82.9 0.1672 0.2561 0.0156  92.9 0.1552 0.3201 0.0527  93.7
            336    0.0232 0.0823 0.7242 100.0 0.1615 0.2737 0.0499 66.0 0.1536 0.2458 0.0182  89.8 0.1488 0.3201 0.0098  87.1
            96     0.0305 0.1041 0.7302 100.0 0.2489 0.3131 0.0368 79.3 0.1771 0.2814 -0.0020 90.8 0.3353 0.5147 0.0152  97.1
ETTh2       192    0.0295 0.0999 0.6835 100.0 0.2094 0.3091 0.0514 77.8 0.1730 0.2740 -0.0087 88.9 0.3237 0.5116 0.0082  92.1
            336    0.0292 0.0993 0.6456 100.0 0.2047 0.3078 0.0441 56.5 0.1450 0.2432 -0.0446 91.2 0.2995 0.4919 -0.0048 74.1
            96     0.0161 0.0669 0.8713 100.0 0.1967 0.2755 0.1279 86.4 0.1924 0.2856 -0.0050 92.7 0.2004 0.3543 0.1668  97.3
ETTm1       192    0.0181 0.0685 0.8338 100.0 0.1836 0.2759 0.0796 80.5 0.1742 0.2651 0.0011  91.6 0.1808 0.3419 0.0772  94.3
            336    0.0276 0.0704 0.7341 100.0 0.1669 0.2695 0.0548 66.1 0.1607 0.2538 -0.0039 86.4 0.1702 0.3417 0.0136  91.6
            96     0.0279 0.0982 0.7944 100.0 0.2618 0.3079 0.0901 80.2 0.1983 0.2955 -0.0038 92.5 0.3669 0.5284 0.0134  96.8
ETTm2       192    0.0295 0.1016 0.7532 100.0 0.2423 0.3209 0.0484 73.4 0.1815 0.2733 0.0001  91.3 0.3500 0.5255 0.0009  93.1
            336    0.0332 0.0968 0.6689 100.0 0.2242 0.3200 0.0521 59.7 0.1578 0.2538 -0.0016 86.7 0.3382 0.5223 -0.0005 84.5
            96     0.0159 0.0622 0.8599 100.0 0.2330 0.2748 0.1505 79.1 0.2400 0.3338 -0.0040 92.9 0.3276 0.4507 0.0758  98.0
Weather 192        0.0159 0.0592 0.8427 100.0 0.2586 0.3068 0.0680 68.1 0.2375 0.3273 0.0010  91.5 0.2981 0.4279 0.0341  95.0
            336    0.0213 0.0648 0.7701 100.0 0.2144 0.2765 0.0858 59.2 0.2206 0.3112 0.0102  87.2 0.2512 0.3928 0.0234  88.1
            96     0.0301 0.0923 0.8112 100.0 0.2490 0.2817 0.0123 79.3 0.2165 0.2903 0.0045  92.8 0.3337 0.4789 0.0054  97.0
Electricity 192    0.0284 0.0845 0.7982  99.8 0.2186 0.2998 0.0034 73.6 0.2106 0.2847 0.0006  90.1 0.3161 0.4699 0.0024  94.9
            336    0.0280 0.0824 0.7811  99.9 0.1887 0.2992 0.0205 65.0 0.1858 0.2711 0.0000  84.9 0.3000 0.4611 0.0036  85.3
            96     0.0795 0.1643 0.4815 100.0 0.3052 0.3530 0.0577 64.3 0.2118 0.3079 0.0411  96.2 0.4009 0.4932 0.0264  97.3
Exchange 192       0.0837 0.1481 0.5180 100.0 0.2893 0.3536 0.0324 51.6 0.1924 0.2956 0.0213  92.3 0.3706 0.4718 0.0619  92.3
            336    0.0870 0.1449 0.5159 100.0 0.2927 0.3896 0.0353 28.6 0.1983 0.3133 -0.0800 91.1 0.3415 0.4784 0.0301  71.4
            96     0.0326 0.1162 0.3672 100.0 0.1738 0.2314 0.0639 81.6 0.3097 0.4230 -0.0012 92.0 0.0631 0.1690 0.0577  90.0
Web         192    0.0246 0.1002 0.3024 100.0 0.2420 0.2924 0.0476 65.0 0.3359 0.4486 0.0001  91.8 0.0406 0.1293 0.0509  67.7
            336    0.0175 0.0823 0.2664  99.9 0.2387 0.2776 0.0242 48.9 0.3313 0.4483 -0.0099 87.5 0.0254 0.0997 0.0657  37.3
     Average                                 †
                   0.0321 0.0938 0.6808 100.0 0.2224 0.2978 0.0571 69.2 0.2064 0.3025 -0.0019 90.7 0.2546 0.4012 0.0363  88.1




equipped with text-conditioning adapters [Ge et al., 2025]. For LLM-based baselines, we evaluate
direct zero-shot generators, including ChatTime [Wang et al., 2025], TimeOmni-1 [Guan et al.,
2025], and GPT-4o-mini [Hurst et al., 2024], as well as recent coding-capable LLMs under the same
Text-to-Code-to-TS prompting setup, including IQuest-Coder-V1-7B-Instruct [Yang et al., 2026],
Devstral-Small-2-24B-Instruct-2512 (Devstral-Instruct-24B) [Rastogi et al., 2025], Seed-Coder-8B-
Instruct [Seed et al., 2025], and Qwen3.5-9B [Team, 2026].
Implementation Details. CodeTS is initialized from Qwen2.5-Coder-7B-Instruct [Hui et al., 2024].
For SFT warmup, we train on 500 synthetic triplets for one epoch with a maximum sequence length
of 3072, a learning rate of 5 × 10−6 , a batch size of 64. For RLVR, we train on 6300 real (d, x)
pairs using GRPO with 4 samples per prompt, learning rate 5 × 10−7 , KL coefficient 10−3 , and 200
update steps. We use ZeRO-2 [Rajbhandari et al., 2020] for SFT and ZeRO-3 with vLLM [Kwon
et al., 2023] for RLVR on A100 GPUs. More details are provided in Appendix G.


                                                              7
5.2   Main Results

In Table 1, CodeTS achieves the best averaged performance across all three metrics, despite being
evaluated zero-shot against supervised baselines trained separately on each target dataset and gener-
ation length. Compared with the strongest supervised baseline for each metric, CodeTS improves
MSE from 0.0733 to 0.0321, DTW from 0.1675 to 0.0938, and Pearson correlation from 0.2279 to
0.6808, corresponding to relative improvements of 56.2%, 44.0%, and 198.7%, respectively. On the
Web dataset, although CodeTS does not always achieve the best MSE or DTW, it consistently obtains
the best Pearson correlation across all generation lengths. This metric is particularly informative
in this dataset, where long flat regions and sparse abrupt variations make shape preservation more
relevant than pointwise error alone. We provide a detailed analysis of the Web results in Appendix H.
Table 2 shows that CodeTS achieves the best performance across all length settings and all reported
metrics. In the averaged results, CodeTS reduces MSE from 0.2064 to 0.0321 and DTW from 0.2978
to 0.0938 compared with the strongest zero-shot LLM baseline for each error metric, corresponding
to relative reductions of 84.4% and 68.5%, respectively. It also increases the average Pearson
correlation from 0.0571 to 0.6808, corresponding to 11.9 times the strongest zero-shot LLM baseline,
while maintaining a near-perfect pass@1 execution success rate.
We further compare with mainstream and recent strong coding-capable LLMs, including IQuest-
Coder-V1-7B-Instruct [Yang et al., 2026], Devstral-Instruct-24B [Rastogi et al., 2025], Seed-Coder-
8B-Instruct [Seed et al., 2025], and Qwen3.5-9B [Team, 2026], under the same Text-to-Code-to-TS
setup. Although these models achieve high execution success rates, CodeTS remains stronger overall,
especially in Pearson correlation, indicating better preservation of temporal patterns rather than
merely producing executable code. Detailed comparisons are provided in Appendix F.

5.3   Ablation Studies

We conduct ablation studies on three key components of CodeTS: the training stages, the normalized
code representation, and the reward design; the main paper reports averaged and representative results,
with detailed per-dataset and per-length statistics provided in Appendix I. Additional supporting
analyses, including RLVR training dynamics, prompt settings, and representative case studies, are
provided in Appendix K–N.
Training Stage Ablation. We analyze the contribution of each training stage by comparing the base
model, the SFT-initialized model, and the final RLVR-optimized model. As shown in Table 3, the
averaged performance over all benchmark datasets improves from the base model to SFT and further
to the full RLVR-optimized model across output lengths. This shows that both stages are beneficial:
SFT improves MSE, DTW, and Pearson correlation by learning the normalized code format and
basic executable generation patterns, while RLVR further improves the executed time series through
reward-based optimization on real Text-TS pairs. The improvement from SFT is moderate because
it mainly serves as a warmup for format alignment and executable code initialization, rather than
directly optimizing the generated series against real targets. Fig. 3 further decomposes the relative
gains on representative datasets, showing that SFT provides a stable warmup contribution, whereas
RLVR accounts for the dominant share of the improvement, especially on Pearson correlation.
Normalized Code Representation Ablation. We evaluate the effect of the normalized code repre-
sentation by comparing full CodeTS with a variant that directly generates executable code without
explicit temporal parameters. As shown in Fig. 4(a), removing normalized code consistently worsens
the results on ETTm1, ETTm2, and Weather, leading to higher MSE and DTW and lower Pearson
correlation. This shows that the improvement of CodeTS does not come only from using executable
code, but also from structuring the output into explicit temporal parameters and executable logic.
Reward Design Ablation. We evaluate the reward design by removing key components from the
time-series quality reward while keeping the format and execution rewards fixed. As shown in
Fig. 4(b), the full reward achieves the best overall performance across the evaluated datasets, with
lower MSE and DTW and higher Pearson correlation. Removing the statistical reward weakens the
results, and removing both correlation and statistical rewards leads to further degradation, especially
in Pearson correlation.

5.4   Template Dependency Analysis


                                                  8
Table 3: Training-stage ablation aver-                                                                                             SFT warmup        RLVR

aged over all benchmark datasets and                                          80
                                                                                              ETTm1                                          ETTm2                           Weather
output lengths.
                                                                              60
 Length                Metric          Base       SFT      Full




                                                                   Gain (%)
                       ↓MSE            0.095      0.089    0.032              40

            96         ↓DTW            0.147      0.141    0.098
                        ↑PC            0.238      0.282    0.716              20


                       ↓MSE            0.092      0.086    0.031              0
            192        ↓DTW            0.137      0.134    0.093
                        ↑PC            0.185      0.210    0.688                   MSE               DTW                 PC         MSE       DTW          PC          MSE        DTW   PC


                       ↓MSE            0.084      0.081    0.033   Figure 3: Stage-wise gains from SFT and RLVR on three
            336        ↓DTW            0.135      0.133    0.090   datasets. Stacked bars show the percentage improvement
                        ↑PC            0.132      0.157    0.638
                                                                   contributed by each stage.

                                Full       w/o Normalized Code                                                                      Full        w/o stat        w/o corr & stat

                     ETTm1                     ETTm2             Weather                                                       ETTm1                 ETTm2                   Weather

            0.12                                                                     0.8                                                                                                0.8




                                                                                                          MSE / DTW
MSE / DTW




                                                                                                                      0.12




                                                                                                                                                                                             Pearson
                                                                                           Pearson
            0.06                                                                     0.4                                                                                                0.4
                                                                                                                      0.06


            0.00                                                                     0.0                              0.00                                                              0.0
                   MSE DTW PC            MSE DTW PC         MSE DTW PC                                                       MSE DTW PC          MSE DTW PC               MSE DTW PC

                                (a) Normalized code                                                                                        (b) Reward function
Figure 4: Ablation results for normalized code representation and reward design. Panel (a) studies
normalized code, and panel (b) studies reward components.

                                                                     Full w/ perturbation      SFT w/ perturbation
We further evaluate whether CodeTS remains ef-               MSE ↓                        DTW ↓                     Pearson ↑
fective when the input description is written in a                              0.2
                                                     0.15
different form. Specifically, we rewrite each
                                                                                                     Perturbed




                                                     0.10                                                   0.5
description by preserving the same temporal
                                                                                0.1
attributes while changing the wording and at-        0.05

tribute order, and then test the model on these           0.05 0.10 0.15                 0.1       0.2
                                                                                                            0.0
                                                                                                                0.0     0.5
perturbed descriptions. As shown in Figure 5,                 origin                        origin                    origin
performance generally decreases after perturba- Figure 5: Template robustness analysis under per-
tion, indicating that the model is still affected turbed descriptions.
by changes in description form. However, the
final RLVR-optimized model remains much closer to the diagonal line than the SFT-warmup model
across MSE, DTW, and Pearson correlation. Since points closer to the diagonal indicate smaller
performance changes after perturbation, this result shows that RLVR improves robustness to textual
perturbations and helps CodeTS learn a more stable mapping from temporal descriptions to generated
time series, rather than relying only on fixed training templates. Detailed analysis are provided in
Appendix J.


6                 Conclusion

We presented CodeTS, a verifiable Text-to-Code-to-TS framework that uses executable code as an
explicit intermediate interface for Text-to-Time Series Generation. Through Text-Code-TS triplet
initialization and execution-based RLVR, CodeTS learns to generate executable programs that trans-
late textual temporal requirements into time series and can be optimized through verifiable feedback.
Experiments on eight benchmarks show that CodeTS achieves strong Text-to-TS generation perfor-
mance, outperforming LLM-based baselines and achieving better averaged results than supervised
generative baselines trained on the target datasets.
Limitations and Future Work. While CodeTS demonstrates strong zero-shot generation ability,
its current formulation is limited to univariate time series and can still be sensitive to ambiguous
descriptions or missing temporal attributes. Future work will extend CodeTS to multivariate temporal
data, and explore richer execution-based rewards for more data-scarce and high-value application
generation scenarios.


                                                                                                     9
References
Sojung An, Tae-Jin Oh, Eunha Sohn, and Donghyun Kim. Deep learning for precipitation nowcasting:
  A survey from the perspective of time series forecasting. Expert Systems with Applications, 268:
  126301, 2025.
Abdul Fatir Ansari, Lorenzo Stella, Caner Turkmen, Xiyuan Zhang, Pedro Mercado, Huibin Shen,
  Oleksandr Shchur, Syama Sundar Rangapuram, Sebastian Pineda Arango, Shubham Kapoor, et al.
  Chronos: Learning the language of time series. arXiv preprint arXiv:2403.07815, 2024.
Roberto Casado-Vara, Angel Martin del Rey, Daniel Pérez-Palau, Luis de-la Fuente-Valentín, and
  Juan M. Corchado. Web traffic time series forecasting using lstm neural networks with distributed
  asynchronous training. Mathematics, 9(4):421, 2021. doi: 10.3390/math9040421.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared
 Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large
 language models trained on code. arXiv preprint arXiv:2107.03374, 2021.
Chirag Deb, Fan Zhang, Junjing Yang, Siew Eang Lee, and Kwok Wei Shah. A review on time
  series forecasting techniques for building energy consumption. Renewable and Sustainable Energy
  Reviews, 74:902–924, 2017.
Alireza Ermagun and David Levinson. Spatiotemporal traffic forecasting: review and proposed
  directions. Transport Reviews, 38(6):786–814, 2018.
Oliver Faust, Yuki Hagiwara, Tan Jen Hong, Oh Shu Lih, and U Rajendra Acharya. Deep learning
  for healthcare applications based on physiological signals: A review. Computer methods and
  programs in biomedicine, 161:1–13, 2018.
Yunfeng Ge, Jiawei Li, Yiji Zhao, Haomin Wen, Zhao Li, Meikang Qiu, Hongyan Li, Ming Jin, and
  Shirui Pan. T2s: high-resolution time series generation with text-to-series diffusion models. In
  Proceedings of the Thirty-Fourth International Joint Conference on Artificial Intelligence, pages
  5208–5216, 2025.
Shuqi Gu, Chuyue Li, Baoyu Jing, and Kan Ren. Verbalts: Generating time series from texts. In
  Forty-second International Conference on Machine Learning, 2025.
Tong Guan, Zijie Meng, Dianqi Li, Shiyu Wang, Chao-Han Huck Yang, Qingsong Wen, Zuozhu
  Liu, Sabato Marco Siniscalchi, Ming Jin, and Shirui Pan. Timeomni-1: Incentivizing complex
  reasoning with time series in large language models. arXiv preprint arXiv:2509.24803, 2025.
Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang,
  Bowen Yu, Keming Lu, et al. Qwen2. 5-coder technical report. arXiv preprint arXiv:2409.12186,
  2024.
Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Os-
  trow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card. arXiv preprint
  arXiv:2410.21276, 2024.
Jinsung Jeon, Jeonghak Kim, Haryong Song, Seunghyeon Cho, and Noseong Park. Gt-gan: General
   purpose time series synthesis with generative adversarial networks. Advances in Neural Information
   Processing Systems, 35:36999–37010, 2022.
Seungwoo Jeong, Junghyo Sohn, Jaehyun Jeon, and Heung-Il Suk. Frequency-conditioned diffusion
  models for time series generation. In Proceedings of the 34th ACM International Conference on
  Information and Knowledge Management, pages 1114–1123, 2025.
Ming Jin, Shiyu Wang, Lintao Ma, Zhixuan Chu, James Y Zhang, Xiaoming Shi, Pin-Yu Chen, Yux-
 uan Liang, Yuan-Fang Li, Shirui Pan, et al. Time-llm: Time series forecasting by reprogramming
 large language models. In International Conference on Learning Representations, 2024.
Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph
 Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model
 serving with pagedattention. In Proceedings of the 29th symposium on operating systems principles,
 pages 611–626, 2023.


                                                 10
Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brahman,
  Lester James V Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, et al. Tulu 3: Pushing frontiers in
  open language model post-training. arXiv preprint arXiv:2411.15124, 2024.
Daesoo Lee, Sara Malacarne, and Erlend Aune. Vector quantized time series generation with a
  bidirectional prior model. In International Conference on Artificial Intelligence and Statistics,
  pages 7665–7693. PMLR, 2023.
Hao Li, Yu-Hao Huang, Chang Xu, Viktor Schlegel, Renhe Jiang, Riza Batista-Navarro, Goran
  Nenadic, and Jiang Bian. Bridge: Bootstrapping text to control time-series generation via multi-
  agent iterative optimization and diffusion modeling. arXiv preprint arXiv:2503.02445, 2025.
Shujian Liao, Hao Ni, Marc Sabate-Vidales, Lukasz Szpruch, Magnus Wiese, and Baoren Xiao.
  Sig-wasserstein gans for conditional time series generation. Mathematical Finance, 34(2):622–670,
  2024.
Jiafeng Lin, Yuxuan Wang, Jialong Wu, Huakun Luo, Zhongyi Pei, and Jianmin Wang. Thoth:
   Mid-training bridges llms to time series understanding. arXiv preprint arXiv:2603.01042, 2026.
Zinan Lin, Alankar Jain, Chen Wang, Giulia Fanti, and Vyas Sekar. Using gans for sharing networked
  time series data: Challenges, initial promise, and open questions. In Proceedings of the ACM
  Internet Measurement Conference, pages 464–483, 2020.
Sai Shankar Narasimhan, Shubhankar Agarwal, Oguzhan Akcin, Sujay Sanghavi, and Sandeep
  Chinchali. Time weaver: a conditional time series generation model. In International Conference
  on Machine Learning, pages 37293–37320, 2024.
Hao Ni, Lukasz Szpruch, Magnus Wiese, Shujian Liao, and Baoren Xiao. Conditional sig-wasserstein
  gans for time series generation. arXiv preprint arXiv:2006.05421, 2020.
Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, and Yuxiong He. Zero: Memory optimizations
  toward training trillion parameter models. In SC20: international conference for high performance
  computing, networking, storage and analysis, pages 1–16. IEEE, 2020.
Abhinav Rastogi, Adam Yang, Albert Q Jiang, Alexander H Liu, Alexandre Sablayrolles, Amélie
  Héliou, Amélie Martin, Anmol Agarwal, Andy Ehrenberg, Andy Lo, et al. Devstral: Fine-tuning
  language models for coding agent applications. arXiv preprint arXiv:2509.25193, 2025.
Cécile Rousseau, Tobia Boschi, Giandomenico Cornacchia, Dhaval Salwala, Alessandra Pascale, and
  Juan Bernabe Moreno. Forging time series with language: A large language model approach to
  synthetic data generation. In Advances in Neural Information Processing Systems, 2025.
Hiroaki Sakoe and Seibi Chiba. Dynamic programming algorithm optimization for spoken word
  recognition. IEEE transactions on acoustics, speech, and signal processing, 26(1):43–49, 2003.
John Schulman, Sergey Levine, Pieter Abbeel, Michael Jordan, and Philipp Moritz. Trust region
  policy optimization. In Proceedings of the 32nd International Conference on Machine Learning,
  pages 1889–1897, 2015.
ByteDance Seed, Yuyu Zhang, Jing Su, Yifan Sun, Chenguang Xi, Xia Xiao, Shen Zheng, Anxiang
  Zhang, Kaibo Liu, Daoguang Zan, et al. Seed-coder: Let the code model curate data for itself.
  arXiv preprint arXiv:2506.03524, 2025.
Omer Berat Sezer, Mehmet Ugur Gudelek, and Ahmet Murat Ozbayoglu. Financial time series fore-
 casting with deep learning : A systematic literature review: 2005–2019. Applied Soft Computing,
 90:106181, 2020.
Aditya Shankar, Lydia Chen, Arie van Deursen, and Rihan Hai. Wavestitch: Flexible and fast
  conditional time series generation with diffusion models. Proceedings of the ACM on Management
  of Data, 3(6):1–25, 2025.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
  Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathemat-
  ical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.


                                                11
Mingtian Tan, C. Bayan Bruss, Nam H. Nguyen, David Evans, and Thomas Hartvigsen. Ts2code:
 Enhancing time series understanding via learning to code. In ICLR 2026 Conference Submission,
 2026. URL https://openreview.net/forum?id=4Ygp2A6am2. Withdrawn submission.
Qwen Team. Qwen3. 5-omni technical report. arXiv preprint arXiv:2604.15804, 2026.
Chengsen Wang, Qi Qi, Jingyu Wang, Haifeng Sun, Zirui Zhuang, Jinming Wu, Lei Zhang, and
  Jianxin Liao. Chattime: A unified multimodal time series foundation model bridging numerical
  and textual data. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39,
  pages 12694–12702, 2025.
Qingsong Wen, Liang Sun, Fan Yang, Xiaomin Song, Jingkun Gao, Xue Wang, and Huan Xu. Time
  series data augmentation for deep learning: A survey. In Proceedings of the Thirtieth International
  Joint Conference on Artificial Intelligence, pages 4653–4660. International Joint Conferences on
  Artificial Intelligence Organization, 2021.
Qingsong Wen, Tian Zhou, Chaoli Zhang, Weiqi Chen, Ziqing Ma, Junchi Yan, and Liang Sun.
  Transformers in time series: A survey. arXiv preprint arXiv:2202.07125, 2022.
Haixu Wu, Jiehui Xu, Jianmin Wang, and Mingsheng Long. Autoformer: Decomposition transformers
  with auto-correlation for long-term series forecasting. Advances in Neural Information Processing
  Systems, 34:22419–22430, 2021.
Wen Wu, Ziyang Zhang, Liwei Liu, Xuenan Xu, Junlin Liu, Ke Fan, Qitan Lv, Jimin Zhuang, Chen
 Zhang, Zheqi Yuan, et al. Scits: Scientific time series understanding and generation with llms.
 arXiv preprint arXiv:2510.03255, 2025.
Zhe Xie, Zeyan Li, Xiao He, Longlong Xu, Xidao Wen, Tieying Zhang, Jianjun Chen, Rui Shi, and
  Dan Pei. Chatts: Aligning time series with llms via synthetic data for enhanced understanding and
  reasoning. Proceedings of the VLDB Endowment, 18(8):2385–2398, 2025.
Jian Yang, Wei Zhang, Shawn Guo, Zhengmao Ye, Lin Jing, Shark Liu, Yizhi Li, Jiajun Wu, Cening
   Liu, X Ma, et al. Iquest-coder-v1 technical report. arXiv preprint arXiv:2603.16733, 2026.
Jinsung Yoon, Daniel Jarrett, and Mihaela Van der Schaar. Time-series generative adversarial
   networks. Advances in neural information processing systems, 32, 2019.
Xinyu Yuan and Yan Qiao. Diffusion-ts: Interpretable diffusion for general time series generation. In
  International Conference on Learning Representations, 2024.
Shijie Zhang. Spectral-aware text-to-time series generation with billion-scale multimodal meteoro-
  logical data. arXiv preprint arXiv:2603.27135, 2026.
Haoyi Zhou, Shanghang Zhang, Jieqi Peng, Shuai Zhang, Jianxin Li, Hui Xiong, and Wancai Zhang.
  Informer: Beyond efficient transformer for long sequence time-series forecasting. In Proceedings
  of the AAAI conference on artificial intelligence, volume 35, pages 11106–11115, 2021.
Tian Zhou, Peisong Niu, Liang Sun, Rong Jin, et al. One fits all: Power general time series analysis
  by pretrained lm. Advances in neural information processing systems, 36:43322–43355, 2023.




                                                 12
A     Notations
Table 4 summarizes the main mathematical symbols used in the paper.

                                  Table 4: Notations used in CodeTS.
    Notation                                 Description
    D = {(xi , di )}N
                    i=1                      Text-TS dataset.
    di , d                                   Text description.
    xi , x                                   Target time series.
    x̂i , x̂                                 Generated time series.
    Li , L                                   Series length.
    πθ                                       Code-generation policy.
    y, yj                                    Generated code and reference code.
    Y                                        Code space.
    Execute(·)                               Sandboxed code execution.
    aj                                       Structured temporal attribute.
    amj                                      Temporal factor, where m denotes length, trend, sea-
                                             sonality, event, or noise.
    A                                        Attribute space.
    Gtext , Gcode                            Text/code generators.
    Dsyn , Ns                                Synthetic triplet dataset and its size.
    Rfmt , Rexec , Rts                       Format, execution, and TS rewards in the main formu-
                                             lation.
    Rlen , Rerr , Rcorr , Rstat              Length, error, correlation, and statistic rewards.
    λfmt , λexec , λts                       Weights for format, execution, and TS rewards.
    λlen , λerr , λcorr , λstat              Weights for TS reward components.
    Ivalid (y)                               Indicator of parseable and executable generated code.
    G                                        Candidates per prompt.
       (k)
    Ri                                       Reward of candidate k.
       (k)
    Âi                                      Group-normalized advantage.
      (k)
    ρi,t (θ)                                 Token-level policy ratio.
     (k)
    ℓi (θ)                                   Clipped surrogate term for candidate k.
    Tk                                       Output-code length.
    ε                                        Stability constant and clipping threshold.
    β                                        KL coefficient.
    DKL                                      Kullback-Leibler divergence.
    πSFT                                     SFT reference policy.
    LSFT (θ)                                 Supervised fine-tuning objective.
    JGRPO (θ)                                GRPO objective.
    θSFT , θfinal                            SFT-initialized and final model parameters.


B     Normalized Code Representation
Figure 6 illustrates the normalized code representation used by CodeTS. Each output is a JSON
object with two fields: params stores structured temporal specifications such as length, trend,
seasonality, local changes, noise, and target statistics, while code stores an escaped Python function
generate_ts(params) that maps these parameters to a finite one-dimensional time series. This
fixed interface keeps outputs parseable, executable, and rewardable, while still allowing diverse
implementations of temporal patterns inside the generated code.




                                                 13
  Normalized Code Representation
 {                                                        def generate_ts(params):
     "params": {                                              t = arange(params["length"])
       "length": <int>,                                       y = zeros(params["length"])
       "trend_segments": [
         {                                                    y += compose_trend(
           "start": <int>,                                        t,
           "end": <int>,                                          segments=params["trend_segments"]
           "start_value": <float>,                            )
           "end_value": <float>,                              y += compose_seasonality(
           "trend_type": <string>                                 t,
         }                                                        seasonality_type=params["seasonality_type"],
       ],
       "seasonality_type": <string>,                              period=params["period"],
       "period": <float>,                                         amplitude=params["amplitude"],
       "amplitude": <float>,                                      phase=params["phase"],
       "phase": <float>,                                          harmonics=params["harmonics"],
       "harmonics": [                                             envelope=params["amplitude_envelope"]
         {"order": <int>, "amplitude_ratio": <float>}         )
       ],                                                     y += compose_local_changes(
       "amplitude_envelope": <string>,                            t,
       "changes": [                                               changes=params["changes"]
         {                                                    )
           "position": <int>,                                 y += normal_noise(
           "magnitude": <float>,                                  std=params["noise_std"],
           "width": <float>,                                      length=params["length"]
           "change_type": <string>                            )
         }
       ],                                                     y = match_statistics(
       "noise_std": <float>,                                      y,
       "target_mean": <float or null>,                            target_mean=params["target_mean"],
       "target_std": <float or null>                              target_std=params["target_std"]
     },                                                       )
     "code": "def generate_ts(params):\\n    ..."             return y
 }



Figure 6: Normalized code representation in CodeTS. The output separates structured temporal
parameters from the executable generate_ts function, enabling both format-level verification and
execution-based time series evaluation.



C      Detailed Reward Function Design

This section provides the concrete reward construction used in RLVR. The main paper presents the
reward at a high level as a combination of format validity, executability, and time-series quality. In
implementation, all reward terms are scaled to [0, 1], and we expand Eq. (9) by absorbing λts into the
four time-series component weights:

                       R(y, x, d) = λfmt Rfmt (y) + λexec Rexec (y)
                                    + Ivalid (y) (λlen Rlen (x̂, x) + λerr Rerr (x̂, x)                          (16)
                                               +λcorr Rcorr (x̂, x) + λstat Rstat (x̂, x)) ,

where y is the generated JSON object, x̂ = Execute(y) is the executed time series, and Ivalid (y) = 1
only when the code passes parsing, sandbox execution, and returned-array validity checks. The
weights are set to λfmt = 0.05, λexec = 0.10, λlen = 0.10, λerr = 0.30, λcorr = 0.30, and
λstat = 0.15.
Format reward. Rfmt gives graded feedback before execution. It checks whether the model output
follows the normalized params/code interface:

                          
                          
                          0.00,         no JSON-like structure is detected,
                          
                          
                          
                          0.20,         JSON-like content is detected but parsing fails,
                          
                           0.40,         parsing succeeds but the result is not a dictionary,
                          
               Rfmt (y) =                                                                                        (17)
                          
                          0.60,         the dictionary misses either params or code,
                          
                          0.80,         both fields exist but generate_ts(params) is absent,
                          
                          
                          
                           1.00,         the normalized format is complete.
                          


This term reduces reward sparsity by distinguishing malformed text, incomplete JSON, and complete
normalized outputs.


                                                        14
Execution reward. Rexec evaluates whether the generated code can be compiled, sandboxed, invoked,
and converted into a valid numerical sequence:
                      
                      
                        0.00, compilation fails because of syntax errors,
                      
                      0.25, syntax is valid but execution or function definition fails,
                      
                      
         Rexec (y) = 0.50, generate_ts(params) is defined but invocation fails,              (18)
                      
                      
                      
                        0.75,  invocation succeeds but the returned value is invalid,
                      
                      1.00, a finite one-dimensional numerical sequence is returned.

Invalid returned values include non-numerical objects, arrays with incompatible shape, non-finite
values, or empty sequences.
Length reward. For a valid executed output, length consistency is scored by
                                                      min(|x̂|, |x|)
                                     Rlen (x̂, x) =                  .                             (19)
                                                      max(|x̂|, |x|)
This term provides partial credit for approximately correct output length while penalizing sequences
that are too short or too long.
                                                               ˜ denote the first T points of x and x̂
Pointwise error reward. Let T = min(|x̂|, |x|), and let x̃ and x̂
after per-sample min-max normalization. The error reward is
                                                     T
                                                                         !
                                                  1X            ˜    2
                        Rerr (x̂, x) = max 1 −           (x̃t − x̂t ) , 0 .                      (20)
                                                  T t=1
The clipping prevents large numerical mismatches from producing negative rewards.
Correlation reward. The correlation term measures global shape agreement:
                                                            
                                                     ˜ x̃), 0 ,
                              Rcorr (x̂, x) = max ρ(x̂,                                            (21)

where ρ(·, ·) is Pearson correlation. If either normalized sequence is numerically degenerate, this
term is set to 0. Negative correlations are also truncated to 0 because they indicate mismatched
temporal direction.
Statistical reward. The statistical term is implemented as a standard-deviation ratio:
                                                                     
                                                     σ(x̂1:T )
                            Rstat (x̂, x) = min                    , 1 ,                           (22)
                                                  σ(x1:T ) + εstat
where εstat is a small stability constant for the standard-deviation ratio. This term directly penalizes
low-variance collapsed outputs, which may otherwise obtain nontrivial pointwise error or correlation
rewards after normalization. Excessive variance is mainly controlled by the pointwise error term.

D     Data Sources
D.1   Text-Conditioned Benchmark Construction

The eight evaluation benchmarks used in the main experiments are public time series datasets that
are originally released as numerical sequences rather than as Text-TS pairs. To evaluate Text-to-TS
generation, we therefore convert each benchmark into a text-conditioned benchmark while keeping
the original numerical windows as the ground-truth targets. This conversion does not introduce
human-written captions or reference generation code; it only derives a natural language description
from each target window through a deterministic signal analysis pipeline.
Window construction. For each benchmark, we read the raw CSV file, automatically identify the
time column when present, and treat each remaining numerical column as a univariate series. For
each target length L ∈ {96, 192, 336}, we segment every univariate series into fixed-length windows
using a stride of L/2, i.e., 48, 96, and 168 for the three generation lengths. Windows containing
non-finite values are discarded. Each retained window x ∈ RL becomes the target sequence in one
evaluation pair. The variable or column name is retained as lightweight metadata and may appear in
the generated description.


                                                  15
Deterministic description extraction. For each target window, we extract temporal attributes directly
from its numerical values. The extractor first records summary statistics, including length, mean,
standard deviation, minimum, and maximum. It then estimates trend with linear regression, optionally
using a two-segment trend when the segmented fit significantly improves over a single global line.
After removing the trend, it detects dominant seasonality from the residual using FFT-based spectral
analysis, with an autocorrelation fallback for short or ambiguous windows. The seasonal component
is summarized by period, amplitude, phase, number of visible cycles, and amplitude-envelope
type. Local events are then detected as peaks and troughs on the residual after removing trend and
seasonality; each event records its direction, start position, turning point, end position, magnitude,
and whether it is spike-like or smooth. The remaining residual variance is reported as the noise level.
Text-TS pair formation. The extracted attributes are rendered into a fixed natural-language template.
For example, a description may state the sequence identifier, the length and summary statistics, the
trend direction and endpoints, the dominant seasonal period and amplitude, a list of local events, and
the residual noise level. The final evaluation example is therefore
                                               (d, x),
where d is the automatically rendered description and x is the original benchmark window. During
evaluation, a method receives only d and must generate a time series x̂; all reported metrics compare
x̂ against the unchanged original numerical window x. For supervised baselines, the same conversion
procedure is applied to the corresponding training split of each target benchmark. For CodeTS and
zero-shot LLM baselines, only the converted test descriptions are used at inference time.
This construction makes the evaluation compatible with Text-to-TS generation while preserving the
original public benchmark values. It should be interpreted as a text-conditioned synthesis benchmark:
the text describes the target temporal behavior derived from the target window, and the task is to
realize that described behavior as a numerical sequence, rather than to forecast future values from
historical context.

D.2   Real-World Training Data Sources

Table 5 lists the real-world data sources used to construct the real Text-TS pairs for RLVR. The
entries are filtered according to the final RLVR training file and linked to the corresponding public
data-source pages. These sources are used only for training-data construction and are kept separate
from the evaluation benchmarks reported in the main experiments.




                                                  16
                         Table 5: Real-world data sources used for RLVR training.

    Dataset                                    URL
    Alibaba Cluster Trace                      https://github.com/alibaba/clusterdata
    Binance BTC/USDT                           https://data.binance.vision/
    Currency Hourly/Volatility                 https://finance.yahoo.com/currencies/
    ESC-50                                     https://github.com/karolpiczak/ESC-50
    Freesound Dataset 50k (FSD50K)             https://zenodo.org/records/4060432
    GDELT Event Data                           https://www.gdeltproject.org/data.html
    Google COVID-19 Open Data                  https : / / github . com / GoogleCloudPlatform /
                                               covid-19-open-data
    IMS Bearing Data (NASA)                    https : / / www . nasa . gov / intelligent-systems-division /
                                               discovery-and-systems-health               /         pcoe       /
                                               pcoe-data-set-repository/
    MIT-BIH Arrhythmia                         https://physionet.org/content/mitdb/1.0.0/
    M5 Forecasting (Walmart)                   https://www.kaggle.com/c/m5-forecasting-accuracy
    Natural Gas Futures                        https://www.eia.gov/dnav/ng/ng_pri_fut_s1_d.htm
    NREL Wind Toolkit                          https : / / developer . nrel . gov / docs / wind / wind-toolkit /
                                               wtk-download/
    NYC Yellow Taxi Trip Data                  https : / / www . nyc . gov / site / tlc / about /
                                               tlc-trip-record-data.page
    OpenMeteo Solar Data                       https://open-meteo.com/en/docs/historical-weather-api
    Paderborn University Bearing Dataset       https : / / mb . uni-paderborn . de / en / kat / research /
                                               bearing-datacenter/data-sets-and-download
    PTB-XL                                     https://physionet.org/content/ptb-xl/1.0.3/
    UK-DALE                                    https://jack-kelly.com/data/
    USGS Daily Streamflow                      https://api.waterdata.usgs.gov/ogcapi/v0/collections/
                                               daily



E     Evaluation Metrics and Success Rate

Let V denote the valid sample index set after removing near-constant target windows and clearly
invalid predictions. For each i ∈ V, we align (xi , x̂i ) by truncation to Ti = min(|xi |, |x̂i |). Let
mi = min1≤t≤Ti xi,t and Mi = max1≤t≤Ti xi,t . The normalized sequences are

                                 xi,t − mi         ˜i,t = x̂i,t − mi ,
                       x̃i,t =             ,       x̂                         t = 1, . . . , Ti .             (23)
                                 Mi − m i                 Mi − m i
Samples with numerically degenerate Mi − mi are excluded from V, and the same filtering is applied
to all methods.
The reported MSE is
                                                        Ti             2
                                                1 X 1 X             ˜i,t .
                                    MSE =                   x̃i,t − x̂                                        (24)
                                               |V|  Ti t=1
                                                   i∈V


The reported DTW is the averaged normalized warping cost:
                                            1 X 1       X
                                                                                ˜i,q ,
                                 DTW =             min                  x̃i,p − x̂                            (25)
                                           |V|  Ti π∈Πi
                                                i∈V           (p,q)∈π

where Πi is the set of monotone warping paths between the two aligned sequences.
Pearson correlation is averaged as
                                         PTi                    ˜        ¯
                               1 X           t=1 (x̃i,t − x̄i )(x̂i,t − x̂i )
                         PC =         q                     q                        ,                        (26)
                              |V|      PTi                2
                                                              PTi ˜            ¯ 2
                                  i∈V   t=1 (x̃i,t − x̄i )        t=1 (x̂i,t − x̂i )

              ¯i are means of the normalized sequences.
where x̄i and x̂


                                                         17
For LLM-based zero-shot baselines, we report success rate as pass@k [Chen et al., 2021]. For task i,
suppose ni candidates are sampled and ci of them are successful. The unbiased estimator is
                                          N         ni −ci
                                                           !
                                      1 X
                            \ =
                           pass@k              1 − nki       ,     ni ≥ k.                    (27)
                                      N i=1            k
             Pni
Here ci = j=1      si,j , where si,j = 1 if candidate j passes all required checks and 0 otherwise.
For code-generating methods, these checks require JSON parsing, the params/code fields, the
generate_ts(params) function, sandboxed execution, and a finite one-dimensional returned se-
quence with compatible length. For textualized baselines, the parsing and shape checks are adapted
to their output format. The reported SR is the pass@1 special case:
                                                          SR(%) = 100 × pass@1.
                                                                         \                                                                             (28)

F          Additional Comparison with Recent LLMs under Text-to-Code-to-TS
We further evaluate several mainstream and recent strong LLMs under the same Text-to-Code-to-TS
prompting setup, including IQuest-Coder-V1-7B-Instruct [Yang et al., 2026], Devstral-Instruct-
24B [Rastogi et al., 2025], Seed-Coder-8B-Instruct [Seed et al., 2025], and Qwen3.5-9B [Team,
2026]. These models cover recent code-oriented LLMs, a larger coding-capable instruction model,
and a strong general-purpose LLM with coding capability. This comparison examines whether the
gains of CodeTS come from the proposed training framework rather than from code generation ability
alone.
As shown in Table 6, CodeTS achieves the strongest overall performance across datasets and genera-
tion lengths. Although some prompted LLMs obtain competitive results on a few individual metrics,
their generated series generally show weaker temporal fidelity and less stable execution success. In
contrast, CodeTS maintains consistently low MSE and DTW, substantially higher Pearson correlation,
and near-perfect pass@1 success rate. These results indicate that the advantage of CodeTS does
not come merely from prompting a strong LLM to write code, but from learning the normalized
Text-to-Code-to-TS interface and optimizing generation quality through execution-based feedback.

Table 6: Results of mainstream and recent strong coding-capable LLMs under the Text-to-Code-to-TS
setup. SR denotes the pass@1 success rate.
                         CodeTS (ours) (7B)   IQuest-Coder-V1-7B-Instruct (7B) Seed-Coder-8B-Instruct (8B)    Qwen3.5-9B (9B)      Devstral-Instruct-24B (24B)
Datasets    Length MSE↓ DTW↓ Pearson↑ SR(%)↑ MSE↓ DTW↓ Pearson↑ SR(%)↑ MSE↓ DTW↓ Pearson↑ SR(%)↑ MSE↓ DTW↓ Pearson↑ SR(%)↑ MSE↓ DTW↓ Pearson↑ SR(%)↑
            96     0.0202 0.0799 0.8136 100.0 0.1902 0.1815 0.1463     96.3 0.0975 0.1338 0.1632 99.2 0.0910 0.1316 0.2201 94.1 0.0915 0.1324 0.2172 98.4
ETTh1       192    0.0219 0.0808 0.7714 100.0 0.1516 0.1587 0.1161     92.5 0.0878 0.1261 0.1360 95.6 0.0845 0.1256 0.1742 88.5 0.0867 0.1249 0.1550 97.6
            336    0.0232 0.0823 0.7242 100.0 0.1116 0.1500 0.0969     89.1 0.0798 0.1250 0.1195 95.9 0.0787 0.1251 0.1424 83.7 0.0789 0.1242 0.1288 97.3
            96     0.0305 0.1041 0.7302 100.0 0.1870 0.1860 0.1508     93.3 0.0926 0.1436 0.1689 98.0 0.0881 0.1436 0.2123 93.7 0.0876 0.1419 0.2111 97.8
ETTh2       192    0.0295 0.0999 0.6835 100.0 0.1025 0.1512 0.1556     91.3 0.0793 0.1345 0.1572 96.4 0.0828 0.1404 0.1804 84.9 0.0777 0.1351 0.1767 96.8
            336    0.0292 0.0993 0.6456 100.0 0.0983 0.1503 0.1474     89.8 0.0711 0.1322 0.1510 100.0 0.0752 0.1373 0.1626 85.0 0.0689 0.1337 0.1771 95.9
            96     0.0161 0.0669 0.8713 100.0 0.2059 0.1964 0.4431     93.8 0.0649 0.1258 0.4973 97.8 0.0595 0.1226 0.5471 90.2 0.0588 0.1219 0.5459 98.2
ETTm1 192          0.0181 0.0685 0.8338 100.0 0.1942 0.1811 0.2702     94.4 0.0836 0.1256 0.2886 95.7 0.0798 0.1241 0.3293 87.5 0.0809 0.1233 0.3223 96.2
            336    0.0276 0.0704 0.7341 100.0 0.1299 0.1716 0.1217     92.4 0.0901 0.1414 0.1365 95.4 0.0841 0.1427 0.1916 81.6 0.0865 0.1436 0.1759 97.1
            96     0.0279 0.0982 0.7944 100.0 0.1760 0.1867 0.3395     92.8 0.0860 0.1499 0.3535 97.4 0.0789 0.1460 0.4042 89.3 0.0796 0.1456 0.4023 98.0
ETTm2 192          0.0295 0.1016 0.7532 100.0 0.1373 0.1731 0.2345     94.8 0.0873 0.1437 0.2433 96.4 0.0822 0.1425 0.2887 87.6 0.0817 0.1414 0.2873 96.8
            336    0.0332 0.0968 0.6689 100.0 0.1206 0.1728 0.1403     92.6 0.0857 0.1449 0.1422 95.5 0.0859 0.1492 0.1701 80.7 0.0826 0.1460 0.1708 98.5
            96     0.0159 0.0622 0.8599 100.0 0.1629 0.1626 0.4714     93.5 0.0685 0.1320 0.4869 97.1 0.0621 0.1268 0.5296 83.4 0.0617 0.1259 0.5282 97.6
Weather 192        0.0159 0.0592 0.8427 100.0 0.1341 0.1527 0.4296     94.3 0.0718 0.1304 0.4279 96.7 0.0663 0.1262 0.4662 81.0 0.0646 0.1243 0.4730 97.8
            336    0.0213 0.0648 0.7701 100.0 0.1277 0.1623 0.2729     95.1 0.0778 0.1328 0.2914 96.9 0.0730 0.1333 0.3234 81.1 0.0739 0.1328 0.3158 97.5
            96     0.0301 0.0923 0.8112 100.0 0.1809 0.1599 0.1139     96.4 0.1610 0.1463 0.1133 97.7 0.1593 0.1468 0.1169 90.1 0.1589 0.1476 0.1220 97.4
Electricity 192    0.0284 0.0845 0.7982 99.8 0.1686 0.1463 0.0498      93.7 0.1553 0.1311 0.0470 97.4 0.1558 0.1312 0.0459 89.9 0.1549 0.1310 0.0483 97.3
            336    0.0280 0.0824 0.7811 99.9 0.1595 0.1391 0.0257      88.8 0.1448 0.1260 0.0211 97.7 0.1453 0.1260 0.0212 86.9 0.1437 0.1261 0.0213 94.7
            96     0.0795 0.1643 0.4815 100.0 0.4000 0.2341 0.4954     97.3 0.1229 0.2045 0.1251 96.7 0.0932 0.1828 0.3344 95.1 0.0983 0.1804 0.3100 96.7
Exchange 192       0.0837 0.1481 0.5180 100.0 0.3163 0.2181 0.4745     92.3 0.1018 0.1723 0.1820 91.2 0.0757 0.1505 0.3913 91.2 0.0866 0.1505 0.2901 97.8
            336    0.0870 0.1449 0.5159 100.0 0.2291 0.2051 0.4343     98.2 0.0978 0.1604 0.1211 98.2 0.0745 0.1402 0.3574 87.5 0.0768 0.1330 0.2956 100.0
            96     0.0326 0.1162 0.3672 100.0 0.0954 0.1489 0.0921     94.9 0.0501 0.1168 0.0689 97.7 0.0491 0.1162 0.1001 74.7 0.0482 0.1153 0.0975 97.8
Web         192    0.0246 0.1002 0.3024 100.0 0.0688 0.1367 0.0682     95.9 0.0357 0.0998 0.0451 97.3 0.0349 0.0991 0.0756 69.9 0.0343 0.0981 0.0690 97.4
            336    0.0175 0.0823 0.2664 99.9 0.0570 0.1310 0.0545      96.2 0.0245 0.0845 0.0339 97.9 0.0239 0.0837 0.0518 68.4 0.0235 0.0829 0.0436 96.7


G          Training Configuration
This section supplements the details of the implementation of the two-stage training procedure,
focusing on model initialization, sample organization, parallel training strategy, and optimization
hyperparameters.

G.1         SFT Warmup Configuration

In the SFT warm-up stage, we initialize the policy model from Qwen2.5-Coder-7B-Instruct and
conduct full-parameter supervised fine-tuning using DeepSpeed on four NVIDIA A100-SXM4-80GB


                                                                             18
GPUs. Each training instance is formatted as a dialogue-style sequence, where the input consists
of the task instruction and the corresponding textual description, and the output is the target JSON
object. We adopt the chat template associated with the base model and pack multiple short instances
into a single training sequence whenever feasible to improve computational efficiency.
This stage is conducted with 500 training examples for one epoch, using a maximum sequence
length of 3072. The global batch size is set to 64, with a per-device micro-batch size of 8. We use a
learning rate of 5 × 10−6 , a warm-up ratio of 0.05, and a cosine learning-rate schedule with a nonzero
minimum learning rate. Training is performed in BF16 precision. To reduce memory consumption,
we employ ZeRO-2 optimization together with gradient checkpointing. During training, only the
most recent checkpoint is retained, and the final model is exported in the HuggingFace format.
This configuration reflects the intended function of the warm-up stage in our framework. Rather than
aiming to overfit the synthetic reference code, this stage is designed to provide the model with an
initial alignment to the expected output format, parameter organization, and executable code scaffold,
while incurring only a limited computational cost. The deliberately short training schedule and small
training set further preserve sufficient exploration capacity for the subsequent RLVR stage.

G.2   GRPO Configuration

In the RLVR stage, we continue training from the SFT warm-up model using a training pipeline built
on OpenRLHF, Ray, and vLLM. This stage is conducted on two NVIDIA A100-SXM4-80GB GPUs.
In contrast to the SFT warm-up stage, the training data consist of real text–time-series pairs. The
input side contains a textual description, while the target side provides the corresponding time series
and its length information, which are used to compute verifiable rewards from executed code outputs.
We use the chat template associated with the base model, and set the maximum input length and
maximum generation length to 1024 and 3072, respectively.
The RLVR stage uses 6,300 training examples. For each input, we sample four candidate programs,
corresponding to G = 4 in the main paper. Both the rollout batch size and the training batch size are
set to 16, while the micro rollout batch size and micro training batch size are both set to 2. The model
is trained for one epoch and one episode. For optimization, the actor learning rate is set to 5 × 10−7 ,
the initial KL coefficient is 10−3 , and the clipping range is [εlow , εhigh ] = [0.2, 0.28]. Advantage
estimation is performed with group normalization. Training is conducted in BF16 precision. To
reduce memory consumption, we employ ZeRO-3 optimization, Adam offloading, and gradient
checkpointing. Online sampling is performed with a single vLLM engine using tensor parallel size 2
and a GPU memory utilization ratio of 0.45. The actor model, reference policy, and rollout engine
are deployed in colocated mode and synchronized through NCCL.
A central consideration in this stage is the resource balance among online sampling, reward evaluation,
and gradient-based policy updates. The relatively conservative rollout batch size, number of sampled
candidates, and micro-batch configuration are chosen to limit the sampling pressure at each update
step, avoid excessive reuse of the same real-data batch, and reserve sufficient memory for generating,
executing, and scoring long-form code outputs.


H     Web Benchmark Analysis

The Web benchmark has a more event-concentrated structure than the other benchmarks. In the
target windows used for evaluation, near-flat adjacent steps account for 13.5%, 18.9%, and 25.5% of
the normalized transitions at lengths 96, 192, and 336, respectively. At the same time, the largest
5% of adjacent changes explain 30.9%, 34.9%, and 37.4% of the total variation. This combination
makes Web a stress test for preserving sparse shape changes rather than only matching the dominant
low-variation regions.
Figure 7 summarizes this behavior. The final CodeTS model achieves Pearson correlations of 0.367,
0.302, and 0.266 on Web for lengths 96, 192, and 336, respectively. However, the reward ablation
shows that MSE and DTW alone are not sufficient to characterize this benchmark. After removing
both the correlation and statistic rewards, Web MSE decreases from 0.0249 to 0.0230 and DTW
decreases from 0.0996 to 0.0721, but Pearson drops from 0.3120 to 0.0803. Thus, a model can match
many local values or warped segments while failing to preserve the sparse event-level shape. We


                                                  19
                                    Web structural profile                                                          Reward ablation on Web
                0.4                                                                                                       Full
                                                                                                     0.3                  w/o stat
                0.3                                                                                                       w/o corr & stat
Ratio / share




                                                                                      Metric value
                                                                                                     0.2
                0.2

                                                                                                     0.1
                0.1


                0.0                                                                                  0.0
                      96                       192                        336                              MSE ↓            DTW ↓               PC ↑
                                         Sequence length
                       Near-flat steps     Large jumps      Top-5% variation


Figure 7: Web benchmark analysis. Left: target-window statistics for Web, where near-flat steps are
normalized adjacent differences no larger than 0.01, large jumps are differences at least 0.20, and
top-5% variation is the share of total variation contributed by the largest 5% adjacent changes. Right:
reward ablation on Web averaged over lengths 96, 192, and 336. Removing correlation and statistic
rewards can reduce MSE and DTW while sharply reducing Pearson correlation, showing that low
pointwise or warped error does not necessarily imply event-shape preservation on Web.

                                         Table 7: Training-stage ablation; SR is pass@1 success rate.
                                                                  SFT                                                       SFT+RLVR
Datasets                   Length          MSE↓          DTW↓       Pearson↑           SR(%)↑              MSE↓         DTW↓         Pearson↑      SR(%)↑
                           96              0.0938        0.1358         0.1972                  95.1       0.0202       0.0799        0.8136           100.0
ETTh1                      192             0.0909        0.1342         0.1155                  87.7       0.0219       0.0808        0.7714           100.0
                           336             0.0824        0.1334         0.1069                  84.4       0.0232       0.0823        0.7242           100.0
                           96              0.0894        0.1455         0.1979                  92.2       0.0305       0.1041        0.7302           100.0
ETTh2                      192             0.0776        0.1361         0.1707                  86.1       0.0295       0.0999        0.6835           100.0
                           336             0.0701        0.1349         0.1604                  79.6       0.0292       0.0993        0.6456           100.0
                           96              0.0635        0.1268         0.5096                  94.0       0.0161       0.0669        0.8713           100.0
ETTm1                      192             0.0820        0.1299         0.2973                  88.3       0.0181       0.0685        0.8338           100.0
                           336             0.0873        0.1461         0.1424                  84.9       0.0276       0.0704        0.7341           100.0
                           96              0.0831        0.1489         0.3796                  90.0       0.0279       0.0982        0.7944           100.0
ETTm2                      192             0.0849        0.1450         0.2757                  90.0       0.0295       0.1016        0.7532           100.0
                           336             0.0844        0.1501         0.1662                  86.4       0.0332       0.0968        0.6689           100.0
                           96              0.0630        0.1256         0.5209                  90.2       0.0159       0.0622        0.8599           100.0
Weather                    192             0.0690        0.1280         0.4469                  89.6       0.0159       0.0592        0.8427           100.0
                           336             0.0745        0.1355         0.3119                  85.6       0.0213       0.0648        0.7701           100.0
                           96              0.1590        0.1534         0.1193                  90.9       0.0301       0.0923        0.8112           100.0
Electricity                192             0.1576        0.1473         0.0373                  87.6       0.0284       0.0845        0.7982            99.8
                           336             0.1466        0.1430         0.0139                  85.7       0.0280       0.0824        0.7811            99.9
                           96              0.1108        0.1807         0.2372                  79.7       0.0795       0.1643        0.4815           100.0
Exchange                   192             0.0941        0.1514         0.2716                  70.3       0.0837       0.1481        0.5180           100.0
                           336             0.0819        0.1407         0.3138                  80.4       0.0870       0.1449        0.5159           100.0
                           96              0.0486        0.1148         0.0945                  75.1       0.0326       0.1162        0.3672           100.0
Web                        192             0.0344        0.0970         0.0675                  68.8       0.0246       0.1002        0.3024           100.0
                           336             0.0230        0.0809         0.0429                  67.9       0.0175       0.0823        0.2664            99.9



therefore interpret Pearson correlation as the most diagnostic metric for Web, with MSE and DTW
serving as complementary error measures.

I                 Detailed Ablation Studies

Detailed Training-Stage Ablation Table 7 provides the detailed training stage ablation results for
each benchmark dataset and generation length. Compared with the SFT-warmup model, the final
SFT+RLVR model achieves substantially better generation quality in most settings, with lower
MSE and DTW, higher Pearson correlation, and higher pass@1 success rate. These results further
support the conclusion in the main paper that SFT provides a useful initialization for executable code
generation, while RLVR is the key stage that improves the executed time series through verifiable
feedback from real Text-TS pairs.
Detailed Normalized Code Ablation Table 8 reports the detailed normalized code ablation results
for each benchmark dataset and generation length. Compared with the variant without normalized
code, the full model generally achieves better generation quality, with lower MSE and DTW and


                                                                                 20
                       Table 8: Normalized code ablation; SR is pass@1 success rate.
                                            Full                                   w/o Normalized Code
Datasets      Length      MSE↓     DTW↓        Pearson↑          SR(%)↑   MSE↓     DTW↓       Pearson↑   SR(%)↑
              96          0.0202   0.0799          0.8136        100.0    0.0773   0.1195      0.3598    100.0
ETTh1         192         0.0219   0.0808          0.7714        100.0    0.0718   0.1108      0.3216    100.0
              336         0.0232   0.0823          0.7242        100.0    0.0669   0.1062      0.2901     99.3
              96          0.0305   0.1041          0.7302        100.0    0.0688   0.1327      0.3859     99.8
ETTh2         192         0.0295   0.0999          0.6835        100.0    0.0591   0.1269      0.3705    100.0
              336         0.0292   0.0993          0.6456        100.0    0.0531   0.1186      0.3596    100.0
              96          0.0161   0.0669          0.8713        100.0    0.0411   0.0947      0.6852    100.0
ETTm1         192         0.0181   0.0685          0.8338        100.0    0.0671   0.0988      0.4556     99.7
              336         0.0276   0.0704          0.7341        100.0    0.0719   0.1014      0.3305     99.7
              96          0.0279   0.0982          0.7944        100.0    0.0514   0.1240      0.6143    100.0
ETTm2         192         0.0295   0.1016          0.7532        100.0    0.0650   0.1247      0.4423     99.3
              336         0.0332   0.0968          0.6689        100.0    0.0657   0.1213      0.3367    100.0
              96          0.0159   0.0622          0.8599        100.0    0.0354   0.0839      0.7228     99.9
Weather       192         0.0159   0.0592          0.8427        100.0    0.0391   0.0822      0.6776     99.6
              336         0.0213   0.0648          0.7701        100.0    0.0553   0.0861      0.4938     99.7
              96          0.0301   0.0923          0.8112        100.0    0.1472   0.1253      0.2005     99.7
Electricity   192         0.0284   0.0845          0.7982         99.8    0.1480   0.1066      0.1049     99.6
              336         0.0280   0.0824          0.7811         99.9    0.1412   0.0970      0.0562     99.9
              96          0.0795   0.1643          0.4815        100.0    0.0788   0.1861      0.4406    100.0
Exchange      192         0.0837   0.1481          0.5180        100.0    0.0751   0.1668      0.4722    100.0
              336         0.0870   0.1449          0.5159        100.0    0.0665   0.1385      0.5109    100.0
              96          0.0326   0.1162          0.3672        100.0    0.0285   0.1017      0.4987     99.9
Web           192         0.0246   0.1002          0.3024        100.0    0.0191   0.0831      0.5365     99.9
              336         0.0175   0.0823          0.2664        99.9     0.0126   0.0661      0.5606    100.0




higher Pearson correlation on most datasets. This confirms that the benefit of CodeTS comes not only
from using executable code, but also from organizing the output into explicit temporal parameters
and executable logic. The normalized representation provides a more structured interface for parsing,
execution checking, and reward computation.
Detailed Reward Design Ablation Table 9 reports the detailed reward design ablation results for
each benchmark dataset and generation length. Compared with removing the statistical reward or
removing both correlation and statistical rewards, the full reward generally provides better overall
generation quality, especially in Pearson correlation. This indicates that the correlation and statistical
terms are important for preserving temporal shape and avoiding structurally weak outputs. In several
settings such as Web, removing these terms can reduce MSE or DTW, but it also sharply decreases
Pearson correlation, suggesting that lower local error does not necessarily imply better preservation
of temporal patterns. These results support the use of a balanced reward design that jointly considers
pointwise accuracy, temporal alignment, and statistical consistency.


J     Detailed Template Robustness Analysis

Table 10 reports the detailed template-dependence results for each benchmark dataset and generation
length. The perturbed descriptions preserve the same temporal attributes as the original descriptions,
but change the wording and attribute order. Compared with the SFT-warmup model under perturbed
descriptions, the final CodeTS model achieves substantially better MSE, DTW, Pearson correlation,
and pass@1 success rate in most settings. Although performance still decreases compared with the
original descriptions, the smaller degradation shows that RLVR improves robustness to description
perturbations and reduces reliance on fixed training templates.


K       Reinforcement Learning Training Dynamics and Effectiveness Analysis

During RLVR, we track six reward functions: Rfmt , Rexec , Rlen , Rerr , Rcorr , and Rstat . Figure 8
shows their training trajectories.
The first three scores rise quickly because SFT already teaches the JSON schema, runnable scaffold,
and explicit length parameter. The time-series terms improve more gradually, reflecting the harder
search for code that matches target values, shape, and variability.


                                                            21
                      Table 9: Reward-design ablation; SR is pass@1 success rate.
                                  Full                            w/o stat                          w/o corr, stat
Datasets   Length MSE↓ DTW↓ Pearson↑ SR(%)↑ MSE↓ DTW↓ Pearson↑ SR(%)↑ MSE↓ DTW↓ Pearson↑ SR(%)↑
           96     0.0202 0.0799     0.8136   100.0   0.0391 0.1091    0.6418       100.0   0.0400 0.1184    0.5951     100.0
ETTh1      192    0.0219 0.0808     0.7714   100.0   0.0395 0.1080    0.5899       100.0   0.0393 0.1140    0.5331     100.0
           336    0.0232 0.0823     0.7242   100.0   0.0391 0.1085    0.5377       100.0   0.0379 0.1129    0.4720     100.0
           96     0.0305 0.1041     0.7302   100.0   0.0552 0.1268    0.5055       100.0   0.0505 0.1327    0.4626     100.0
ETTh2      192    0.0295 0.0999     0.6835   100.0   0.0517 0.1238    0.4476       100.0   0.0471 0.1272    0.3860     100.0
           336    0.0292 0.0993     0.6456   100.0   0.0481 0.1211    0.4188       100.0   0.0439 0.1213    0.3477     100.0
           96     0.0161 0.0669     0.8713   100.0   0.0366 0.1040    0.7126       100.0   0.0494 0.1310    0.5885     100.0
ETTm1      192    0.0181 0.0685     0.8338   100.0   0.0365 0.1049    0.6660       100.0   0.0440 0.1152    0.5589     100.0
           336    0.0276 0.0704     0.7341   100.0   0.0520 0.1261    0.5008       100.0   0.0464 0.1230    0.4419     100.0
           96     0.0279 0.0982     0.7944   100.0   0.0604 0.1329    0.5461       100.0   0.0606 0.1512    0.4748     100.0
ETTm2      192    0.0295 0.1016     0.7532   100.0   0.0563 0.1278    0.5076       100.0   0.0546 0.1395    0.4192     100.0
           336    0.0332 0.0968     0.6689   100.0   0.0571 0.1322    0.4210       100.0   0.0520 0.1359    0.3559     100.0
           96     0.0159 0.0622     0.8599   100.0   0.0457 0.1129    0.6469       100.0   0.0538 0.1423    0.5986     100.0
Weather    192    0.0159 0.0592     0.8427   100.0   0.0472 0.1135    0.6049       100.0   0.0556 0.1387    0.4855      99.9
           336    0.0213 0.0648     0.7701   100.0   0.0464 0.1182    0.5470       100.0   0.0447 0.1226    0.5038     100.0
            96    0.0301 0.0923     0.8112   100.0   0.0520 0.1223    0.6827       99.9    0.0485 0.1245    0.6534     100.0
Electricity 192   0.0284 0.0845     0.7982    99.8   0.0482 0.1179    0.6678       99.8    0.0448 0.1186    0.6341     100.0
            336   0.0280 0.0824     0.7811    99.9   0.0462 0.1157    0.6494       99.9    0.0419 0.1148    0.6178      99.9
           96     0.0795 0.1643     0.4815   100.0   0.0740 0.1554    0.4565       100.0   0.0603 0.1598    0.4717     100.0
Exchange   192    0.0837 0.1481     0.5180   100.0   0.0685 0.1389    0.5039       100.0   0.0599 0.1597    0.4961      98.9
           336    0.0870 0.1449     0.5159   100.0   0.0574 0.1253    0.4990       100.0   0.0598 0.1591    0.4875     100.0
           96     0.0326 0.1162     0.3672   100.0   0.0456 0.1140    0.1396       99.9    0.0317 0.0869    0.1121     100.0
Web        192    0.0246 0.1002     0.3024   100.0   0.0334 0.0974    0.0841       98.2    0.0220 0.0705    0.0784     100.0
           336    0.0175 0.0823     0.2664    99.9   0.0232 0.0825    0.0544       99.0    0.0154 0.0588    0.0505     100.0


                  Table 10: Template-dependence ablation; SR is pass@1 success rate.
                                  Full                      Full w/ perturbation                 SFT w/ perturbation
Datasets   Length MSE↓ DTW↓ Pearson↑ SR(%)↑ MSE↓ DTW↓ Pearson↑ SR(%)↑ MSE↓ DTW↓ Pearson↑ SR(%)↑
           96     0.0202 0.0799     0.8136   100.0   0.0440 0.1073    0.6578       92.4    0.0997 0.1481    0.1766     47.0
ETTh1      192    0.0219 0.0808     0.7714   100.0   0.0426 0.1104    0.5815       93.7    0.1005 0.1483    0.1307     46.0
           336    0.0232 0.0823     0.7242   100.0   0.0426 0.1155    0.5138       90.5    0.0836 0.1359    0.1310     38.1
           96     0.0305 0.1041     0.7302   100.0   0.0545 0.1275    0.5432       92.4    0.1045 0.1635    0.1782     44.2
ETTh2      192    0.0295 0.0999     0.6835   100.0   0.0481 0.1235    0.4967       95.6    0.0832 0.1477    0.1710     51.2
           336    0.0292 0.0993     0.6456   100.0   0.0442 0.1182    0.4600       94.6    0.0747 0.1491    0.1945     43.5
           96     0.0161 0.0669     0.8713   100.0   0.0329 0.0932    0.7589       93.2    0.0739 0.1362    0.4775     46.7
ETTm1      192    0.0181 0.0685     0.8338   100.0   0.0386 0.1005    0.6783       93.9    0.0946 0.1440    0.2986     47.0
           336    0.0276 0.0704     0.7341   100.0   0.0563 0.1155    0.5131       94.0    0.0905 0.1502    0.1617     47.5
           96     0.0279 0.0982     0.7944   100.0   0.0528 0.1236    0.6659       93.9    0.0868 0.1529    0.3809     48.2
ETTm2      192    0.0295 0.1016     0.7532   100.0   0.0524 0.1260    0.5913       93.5    0.1045 0.1566    0.2562     51.2
           336    0.0332 0.0968     0.6689   100.0   0.0603 0.1289    0.4786       93.3    0.0832 0.1511    0.1622     49.4
           96     0.0159 0.0622     0.8599   100.0   0.0298 0.0879    0.7644       94.0    0.0768 0.1355    0.4844     47.5
Weather    192    0.0159 0.0592     0.8427   100.0   0.0290 0.0859    0.7451       92.9    0.0704 0.1285    0.4409     45.8
           336    0.0213 0.0648     0.7701   100.0   0.0373 0.0983    0.6353       93.8    0.0773 0.1369    0.3022     44.5
            96    0.0301 0.0923     0.8112   100.0   0.0588 0.1249    0.6690       94.0    0.1700 0.1761    0.1197     38.7
Electricity 192   0.0284 0.0845     0.7982    99.8   0.0641 0.1255    0.6102       91.3    0.1663 0.1626    0.0547     37.0
            336   0.0280 0.0824     0.7811    99.9   0.0604 0.1240    0.5693       91.4    0.1529 0.1597    0.0340     38.8
           96     0.0795 0.1643     0.4815   100.0   0.1000 0.1778    0.4082       92.3    0.1672 0.2177    0.1785     49.5
Exchange   192    0.0837 0.1481     0.5180   100.0   0.0866 0.1546    0.4058       95.6    0.1067 0.1579    0.2739     42.9
           336    0.0870 0.1449     0.5159   100.0   0.0808 0.1397    0.4756       92.9    0.0813 0.1304    0.2678     53.6
           96     0.0326 0.1162     0.3672   100.0   0.0370 0.1178    0.3033       96.5    0.0481 0.1171    0.1015     30.3
Web        192    0.0246 0.1002     0.3024   100.0   0.0271 0.1012    0.2601       96.5    0.0349 0.1000    0.0795     62.5
           336    0.0175 0.0823     0.2664    99.9   0.0197 0.0843    0.2276       96.1    0.0245 0.0854    0.0579     64.8



This trend is consistent with the reward-ablation results in the main paper. Pointwise error alone can
produce numerically plausible but structurally weak sequences; shape correlation improves global
alignment, and variance preservation discourages low-variance collapse.

L       Prompts for Training and Inference
This section documents the prompts used by CodeTS and the zero-shot baselines. For SFT, RLVR,
and fine-tuned model inference, we use the same prompt skeleton so that the output interface remains
consistent across training and evaluation. The system message defines the model role, and the user
message asks the model to translate a natural language time series description into a normalized
JSON object containing params and code. During SFT, the reference JSON object is used as the
supervised target. During RLVR, the same prompt is used to sample candidate code, while the paired


                                                          22
                              Rfmt                                             Rexec                                             Rlen
         1.0                                              1.0                                               1.0

         0.8                                              0.8                                               0.8

Reward




                                                 Reward




                                                                                                   Reward
         0.6                                              0.6                                               0.6

         0.4                                              0.4                                               0.4

         0.2                                              0.2                                               0.2

         0.0                                              0.0                                               0.0
               1   50   100    150   200   250                  1   50   100     150   200   250                  1   50   100     150   200   250
                        Update step                                      Update step                                       Update step

                              Rerr                                             Rcorr                                             Rstat
         1.0                                              1.0                                               1.0

         0.8                                              0.8                                               0.8
Reward




                                                 Reward




                                                                                                   Reward
         0.6                                              0.6                                               0.6

         0.4                                              0.4                                               0.4

         0.2                                              0.2                                               0.2

         0.0                                              0.0                                               0.0
               1   50   100    150   200   250                  1   50   100     150   200   250                  1   50   100     150   200   250
                        Update step                                      Update step                                       Update step


                              Figure 8: Training dynamics of the six RLVR reward functions.


time series is used only for execution-based reward computation. During inference, the test-time
description is appended to the same user instruction.

   System Prompt

 You are an expert time series analyst and Python programmer. You translate natural language
 descriptions of time series patterns into precise generation parameters and executable Python code.


    User Instruction

  You are a time series generation assistant. Given a natural language description of a time series,
  produce a JSON object with two keys: params, the generation-parameter dictionary, and code, the
  complete Python function that generates the time series from these parameters. The params field must
  be directly usable as input to the code function.
  Input: The concrete time-series description d, appended after a blank line.
  Output: A normalized JSON object.


Figure 9: Prompt skeleton used for SFT, RLVR, and fine-tuned CodeTS inference. The concrete
time-series description is appended to the user message; the target JSON object is provided only in
SFT, while RLVR uses the paired time series only for reward computation.

For zero-shot LLM baselines, we use a separate and more explicit prompt because these models have
not been task-specifically tuned to follow the normalized CodeTS output interface. The zero-shot
prompt therefore includes the required JSON schema, the required generate_ts(params) function
signature, the available Python libraries, safety constraints, and an example output format. In this
setting, the user message contains only the test description, while the system prompt provides the
task definition and formatting constraints.

M              Broader Impact
Our work introduces CodeTS, a verifiable Text-to-Code-to-TS generation framework that employs
executable code as an explicit intermediate interface between natural language temporal descriptions
and synthetic time series generation. This design has the potential to facilitate time series modeling
in data-scarce settings, including healthcare, energy systems, transportation, finance, and climate
analysis, where acquiring representative observations may be costly, privacy-sensitive, or constrained


                                                                          23
  Zero-shot Prompt

 You are an expert Python programmer specializing in time series generation.

 Your task is to convert natural language descriptions into:
 1. A JSON parameters object
 2. A Python function that generates the time series

 ## Output Format
 Return a JSON object with this structure:
 {
   "params": {
     "length": <int>,
     // ... other parameters inferred from the description
   },
   "code": "def generate_ts(params):\\n    ..."
 }

 ## Python Code Requirements
 The `code` field must contain a function:

 def generate_ts(params):
     import numpy as np
     # ... implementation
     return ts # numpy array of shape (length,)

 ## Available Libraries
 - `numpy` / `np` - Core numerical operations
 - `math` - Mathematical functions
 - `scipy` - Scientific computing (scipy.signal, scipy.stats, scipy.fft, scipy.interpolate,
 scipy.ndimage, scipy.special)
 - `pandas` / `pd` - Data manipulation
 - `sklearn` - Machine learning (sklearn.preprocessing, sklearn.gaussian_process, sklearn.datasets,
 sklearn.decomposition)
 - `statsmodels` - Time series models (statsmodels.tsa.arima_process, statsmodels.tsa.holtwinters,
 statsmodels.tsa.stattools)
 - `tslearn` - Time series ML (tslearn.generators, tslearn.preprocessing, tslearn.barycenters)
 - `einops` - Tensor operations
 - `fastdtw` - Dynamic Time Warping
 - `librosa` - Audio/music analysis
 - `ruptures` / `rpt` - Change point detection
 - `pywt` - Wavelet transforms
 - `neurokit2` / `nk` - Physiological signals (ECG, PPG, RSP)
 - `pandas_ta` / `ta` - Technical analysis indicators
 - `arch` / `arch_model` - ARCH/GARCH volatility modeling

 ## Code Constraints
 1. **NO file I/O, network, or system calls**
 2. **Function MUST return a numpy array of shape (length,)**
 3. **All parameters MUST come from the `params` dict**
 4. **The `code` field must be a SINGLE STRING with escaped newlines (\\n)**

 The input description contains specific numerical values (mean, std, range, period, amplitude,
 etc.).
 You MUST use these exact values as parameters in your code. Do NOT normalize the output.

 ## Example
 ...

 Output ONLY the JSON object, no other text.


Figure 10: Prompt used for zero-shot LLM baselines. Compared with the fine-tuned-model prompt,
this prompt is more constrained and includes explicit format, code, library, and safety requirements
to improve parseability and executability without task-specific fine-tuning.




                                                  24
by the rarity of relevant events. By rendering the generation process executable and inspectable,
CodeTS further enables users to construct targeted temporal scenarios, stress-test downstream models,
and examine whether generated samples conform to the specified temporal requirements.
Nevertheless, synthetic time series should not be regarded as a replacement for validated domain
observations in high-stakes applications. Ambiguous or underspecified descriptions, biases inherited
from training data or reference programs, and excessive reliance on generated samples may result in
misleading evaluations or undesirable downstream model behavior. In addition, the use of executable
code as an intermediate representation introduces security considerations, since candidate programs
must be evaluated through execution. In this work, normalized code, format validation, sandboxed
execution, and success-rate reporting serve as partial safeguards. However, real-world deployment
should further incorporate domain-specific validation, provenance tracking, privacy assessment,
and explicit disclosure whenever synthetic time series are used for analysis, evaluation, or model
development.

N    Additional Case Studies
We provide three representative successful cases selected from CodeTS evaluation outputs, prioritizing
local-event richness rather than only the lowest global error. Each case forms a Text-Code-TS triplet:
the natural language description d, the normalized generated program y containing params and
code, and the executed time series x̂ = Execute(y). Each case starts on a separate page so that the
compressed text description, time-series visualization, folded parameter summary, execution metrics,
and unframed executable code can be inspected together.




                                                 25
N.1        Case 1: Electricity-336 Client 314
Text description. This sequence is 314. The time series spans 336 points with mean 8271.58, std 4722.22, range [2115.00, 16956.00]. Flat linear trend from baseline 7788.97 to
8754.19 from position 0 to 335. Pure sinusoidal seasonality with period 24.0, amplitude 6468.78, phase 1.96 rad, 14 cycles, constant envelope. One smooth+up from position 19 to
25 (peak at 22), magnitude 0.24. One spike+down from position 23 to 25 (peak at 24), magnitude 0.19. One spike+up from position 27 to 31 (peak at 29), magnitude 0.17. One
spike+down from position 33 to 35 (peak at 34), magnitude 0.17. One spike+up from position 44 to 46 (peak at 45), magnitude 0.19. One smooth+down from position 47 to 51
(peak at 49), magnitude 0.22. One spike+up from position 68 to 70 (peak at 69), magnitude 0.22. One spike+down from position 71 to 75 (peak at 73), magnitude 0.24. One
smooth+up from position 91 to 95 (peak at 93), magnitude 0.24. One spike+down from position 96 to 98 (peak at 97), magnitude 0.19. One smooth+up from position 99 to 103
(peak at 101), magnitude 0.19. One smooth+down from position 118 to 124 (peak at 121), magnitude 0.28. One spike+up from position 130 to 134 (peak at 132), magnitude 0.28.
One spike+down from position 134 to 136 (peak at 135), magnitude 0.29. One smooth+up from position 142 to 156 (peak at 149), magnitude 0.29. One smooth+down from
position 154 to 164 (peak at 159), magnitude 0.38. One smooth+up from position 165 to 181 (peak at 173), magnitude 0.29. One smooth+down from position 181 to 185 (peak at
183), magnitude 0.29. One smooth+up from position 188 to 192 (peak at 190), magnitude 0.16. One spike+down from position 192 to 194 (peak at 193), magnitude 0.16. One
spike+up from position 201 to 205 (peak at 203), magnitude 0.26. One spike+down from position 207 to 209 (peak at 208), magnitude 0.17. One spike+up from position 212 to
214 (peak at 213), magnitude 0.17. One spike+down from position 216 to 218 (peak at 217), magnitude 0.21. One spike+up from position 220 to 222 (peak at 221), magnitude
0.15. One spike+down from position 225 to 227 (peak at 226), magnitude 0.15. One smooth+up from position 231 to 243 (peak at 237), magnitude 0.21. One spike+down from
position 240 to 242 (peak at 241), magnitude 0.20. One spike+up from position 243 to 247 (peak at 245), magnitude 0.20. One spike+down from position 249 to 251 (peak at 250),
magnitude 0.17. One spike+up from position 252 to 254 (peak at 253), magnitude 0.17. One spike+down from position 264 to 266 (peak at 265), magnitude 0.20. One spike+up
from position 267 to 271 (peak at 269), magnitude 0.15. One spike+down from position 273 to 275 (peak at 274), magnitude 0.15. One spike+up from position 276 to 278 (peak at
277), magnitude 0.20. One spike+down from position 287 to 291 (peak at 289), magnitude 0.26. One spike+up from position 299 to 301 (peak at 300), magnitude 0.26. One
spike+down from position 302 to 304 (peak at 303), magnitude 0.16. One smooth+up from position 308 to 312 (peak at 310), magnitude 0.16. One spike+down from position 311
to 315 (peak at 313), magnitude 0.26. One spike+up from position 323 to 325 (peak at 324), magnitude 0.17. One spike+down from position 326 to 328 (peak at 327), magnitude
0.17. Noise std_deviation 1309.070.
Execution. L = 336; 42 events; MSE 0.0063; DTW 0.0453; PC 0.9632.

                                                                                                            Target        Generated
                                                15000
                                        Value




                                                10000


                                                 5000



                                                        0        50        100        150          200       250        300        350
                                                                                       Time step
Folded params.
length =336; target_mean =8271.584; target_std =4722.224; noise_std =1309.07
trend : linear (0 -335): 7788.974 -> 8754.194
seasonality : sinusoidal , period =24.0 , amplitude =6468.784 , phase =1.962 , envelope = constant
events : 42 total = 30 spike + 12 smooth ; 22 with magnitude >= 0.2; max magnitude =0.384
top events : smooth + down at 159 [154 ,164] , mag =0.384; spike + down at 135 [134 ,136] , mag =0.294;
smooth + up at 149 [142 ,156] , mag =0.294; smooth + up at 173 [165 ,181] , mag =0.294

Generated code.
def generate_ts ( params ):
    import numpy as np
    length = params [ ’ length ’]
    t = np . arange ( length , dtype = float )
    def _trend_seg (n , sv , ev , stype , extra ):
        if n <= 0:
              return np . array ([])
        if n == 1:
              return np . array ([ sv ])
        tn = np . arange (n , dtype = float ) / ( n - 1)
        return sv + ( ev - sv ) * tn
    trend = np . zeros ( length )
    for _s in params [ ’ trend_segments ’ ]:
        _a , _b = ( _s . get ( ’ start ’ , 0) , _s . get ( ’ end ’ , length - 1))
        trend [ _a : _b + 1] = _trend_seg ( _b - _a + 1 , _s . get ( ’ start_value ’ , 0.0) ,
        _s . get ( ’ end_value ’ , _s . get ( ’ start_value ’ , 0.0)) , _s . get ( ’ trend_type ’ , ’ constant ’) , _s )
    _last = params [ ’ trend_segments ’ ][ -1]
    _last_end = _last . get ( ’ end ’ , length - 1)
    if _last_end < length - 1:
        trend [ _last_end + 1:] = trend [ _last_end ]
    seasonality_type = params . get ( ’ seasonality_type ’ , None )
    seasonality = np . zeros ( length )
    def _build_seasonal ( t_arr , s_type , period , amplitude , phase , harmonics , envelope_type , length_seg ):
        seg = np . zeros ( len ( t_arr ))
        if s_type is None or s_type == ’ none ’ or amplitude == 0:
              return seg
        t_local = np . arange ( len ( t_arr ) , dtype = float )
        envelope = np . full ( len ( t_arr ) , 1.0)
        omega = 2.0 * np . pi * t_arr / period + phase
        seg = amplitude * np . cos ( omega )
        for h in harmonics :
              order = h . get ( ’ order ’ , 2)
              amp_ratio = h . get ( ’ amplitude_ratio ’ , h . get ( ’ r e la t iv e _a mp l it u de ’ , 0.0))
              seg += amplitude * amp_ratio * np . cos ( order * 2.0 * np . pi * t_arr / period + phase )
        return seg * envelope
    seasonal_regions = params . get ( ’ seasonal_regions ’ , None )
    period = params . get ( ’ period ’ , length )
    amplitude = params . get ( ’ amplitude ’ , 0.0)
    phase = params . get ( ’ phase ’ , 0.0)
    harmonics = params . get ( ’ harmonics ’ , [])
    envelope_type = params . get ( ’ a m p l i t u d e _ e n v e l o p e _ t y p e ’ , ’ constant ’)
    seasonality = _build_seasonal (t , seasonality_type , period , amplitude , phase , harmonics , envelope_type , length )
    changes_array = np . zeros ( length )
    for change in params . get ( ’ changes ’ , []):
        ch_type = change . get ( ’ change_type ’ , ’ spike ’)
        direction = change . get ( ’ direction ’ , ’ up ’)
        tp = change . get ( ’ turning_point ’ , length // 2)
        mag = abs ( change . get ( ’ magnitude ’ , 0.0))
        if direction == ’ down ’:
              mag = - mag
        sp = change . get ( ’ start_position ’ , None )
        ep = change . get ( ’ end_position ’ , None )
        sigma = max (1.0 , ( ep - sp ) / 4.0)
        changes_array += mag * np . exp ( -0.5 * (( t - tp ) / sigma ) ** 2)
    raw_ts = trend + seasonality + changes_array
    raw_mean = params . get ( ’ target_mean ’ , None ). mean ()



                                                                                     26
raw_std = params . get ( ’ target_std ’ , None ). std ()
ts = ( raw_ts - raw_mean ) / raw_std * target_std + target_mean
return ts




                                                27
N.2       Case 2: Weather-96 VPact
Text description. This sequence is VPact (mbar). The time series spans 96 points with mean 10.28, std 0.36, range [9.43, 10.92]. Downward linear trend from baseline
10.74 to 9.72 from position 0 to 47. Upward linear trend from baseline 9.83 to 10.85 from position 48 to 95. Pure sinusoidal seasonality with period 48.0, amplitude 0.20,
phase -3.13 rad, 2 cycles, increasing envelope. One spike+down from position 7 to 11 (peak at 9), magnitude 0.11. One spike+up from position 10 to 12 (peak at 11),
magnitude 0.11. One spike+down from position 14 to 18 (peak at 16), magnitude 0.12. One spike+up from position 17 to 19 (peak at 18), magnitude 0.12. One spike+down
from position 24 to 26 (peak at 25), magnitude 0.09. One spike+up from position 26 to 28 (peak at 27), magnitude 0.09. One smooth+down from position 24 to 34 (peak
at 29), magnitude 0.26. One spike+up from position 30 to 34 (peak at 32), magnitude 0.26. One spike+down from position 34 to 36 (peak at 35), magnitude 0.10. One
spike+up from position 35 to 37 (peak at 36), magnitude 0.10. One smooth+down from position 43 to 53 (peak at 48), magnitude 0.23. One smooth+up from position 61 to
67 (peak at 64), magnitude 0.23. One spike+down from position 68 to 70 (peak at 69), magnitude 0.28. One spike+up from position 72 to 74 (peak at 73), magnitude 0.36.
One spike+down from position 73 to 77 (peak at 75), magnitude 0.36. One spike+up from position 78 to 80 (peak at 79), magnitude 0.14. One spike+down from position 81
to 83 (peak at 82), magnitude 0.14. One spike+up from position 83 to 85 (peak at 84), magnitude 0.34. One smooth+down from position 85 to 89 (peak at 87), magnitude
0.17. One spike+up from position 91 to 93 (peak at 92), magnitude 0.17. Noise std_deviation 0.117.

Execution. L = 96; 20 events; MSE 0.0027; DTW 0.0317; PC 0.9767.

                                                                                                         Target        Generated

                                               10.5


                                       Value   10.0


                                                9.5

                                                      0           20              40             60               80
                                                                                    Time step
Folded params.
length =96; target_mean =10.283; target_std =0.3625; noise_std =0.1174
trend : linear (0 -47): 10.744 -> 9.724; linear (48 -95): 9.832 -> 10.852
seasonality : sinusoidal , period =48.0 , amplitude =0.203 , phase = -3.134 , envelope = increasing
events : 20 total = 16 spike + 4 smooth ; 8 with magnitude >= 0.2; max magnitude =0.364
top events : spike + up at 73 [72 ,74] , mag =0.364; spike + down at 75 [73 ,77] , mag =0.364;
spike + up at 84 [83 ,85] , mag =0.344; spike + down at 69 [68 ,70] , mag =0.284

Generated code.
def generate_ts ( params ):
    import numpy as np
    length = params [ ’ length ’]
    t = np . arange ( length , dtype = float )
    def _trend_seg (n , sv , ev , stype , extra ):
        if n <= 0:
              return np . array ([])
        if n == 1:
              return np . array ([ sv ])
        tn = np . arange (n , dtype = float ) / ( n - 1)
        return sv + ( ev - sv ) * tn
    trend = np . zeros ( length )
    for _s in params [ ’ trend_segments ’ ]:
        _a , _b = ( _s . get ( ’ start ’ , 0) , _s . get ( ’ end ’ , length - 1))
        trend [ _a : _b + 1] = _trend_seg ( _b - _a + 1 , _s . get ( ’ start_value ’ , 0.0) ,
        _s . get ( ’ end_value ’ , _s . get ( ’ start_value ’ , 0.0)) , _s . get ( ’ trend_type ’ , ’ constant ’) , _s )
    _last = params [ ’ trend_segments ’ ][ -1]
    _last_end = _last . get ( ’ end ’ , length - 1)
    if _last_end < length - 1:
        trend [ _last_end + 1:] = trend [ _last_end ]
    seasonality_type = params . get ( ’ seasonality_type ’ , None )
    seasonality = np . zeros ( length )
    def _build_seasonal ( t_arr , s_type , period , amplitude , phase , harmonics , envelope_type , length_seg ):
        seg = np . zeros ( len ( t_arr ))
        if s_type is None or s_type == ’ none ’ or amplitude == 0:
              return seg
        t_local = np . arange ( len ( t_arr ) , dtype = float )
        envelope = np . linspace (0.7 , 1.3 , len ( t_arr ))
        omega = 2.0 * np . pi * t_arr / period + phase
        seg = amplitude * np . cos ( omega )
        for h in harmonics :
              order = h . get ( ’ order ’ , 2)
              amp_ratio = h . get ( ’ amplitude_ratio ’ , h . get ( ’ r e la t iv e_ a mp l it u de ’ , 0.0))
              seg += amplitude * amp_ratio * np . cos ( order * 2.0 * np . pi * t_arr / period + phase )
        return seg * envelope

      seasonal_regions = params . get ( ’ seasonal_regions ’ , None )
      period = params . get ( ’ period ’ , length )
      amplitude = params . get ( ’ amplitude ’ , 0.0)
      phase = params . get ( ’ phase ’ , 0.0)
      harmonics = params . get ( ’ harmonics ’ , [])
      envelope_type = params . get ( ’ a m p l i t u d e _ e n v e l o p e _ t y p e ’ , ’ constant ’)
      seasonality = _build_seasonal (t , seasonality_type , period ,
      amplitude , phase , harmonics , envelope_type , length )
      changes_array = np . zeros ( length )
      for change in params . get ( ’ changes ’ , []):
          ch_type = change . get ( ’ change_type ’ , ’ spike ’)
          direction = change . get ( ’ direction ’ , ’ up ’)
          tp = change . get ( ’ turning_point ’ , length // 2)
          mag = abs ( change . get ( ’ magnitude ’ , 0.0))
          if direction == ’ down ’:
               mag = - mag
          sp = change . get ( ’ start_position ’ , None )
          ep = change . get ( ’ end_position ’ , None )
          sigma = max (1.0 , ( ep - sp ) / 4.0)
          changes_array += mag * np . exp ( -0.5 * (( t - tp ) / sigma ) ** 2)
      noise_segments = params . get ( ’ noise_segments ’ , None )
      noise_std = abs ( params . get ( ’ noise_std ’ , 0.0))
      noise = np . zeros ( length )
      raw_ts = trend + seasonality + changes_array + noise
      target_mean = params . get ( ’ target_mean ’ , None )
      target_std = params . get ( ’ target_std ’ , None )
      raw_mean = raw_ts . mean ()
      raw_std = raw_ts . std ()
      ts = ( raw_ts - raw_mean ) / raw_std * target_std + target_mean
      return ts




                                                                                  28
N.3       Case 3: ETTm1-96 HUFL
Text description. This sequence is HUFL. The time series spans 96 points with mean 7.95, std 5.32, range [-8.97, 16.28]. Upward linear trend from baseline -3.08 to 12.91
from position 0 to 47. Downward linear trend from baseline 15.79 to 6.16 from position 48 to 95. No periodic/seasonal pattern. One spike+up from position 0 to 2 (peak at
1), magnitude 0.21. One spike+down from position 1 to 3 (peak at 2), magnitude 0.44. One spike+up from position 2 to 4 (peak at 3), magnitude 0.47. One spike+down from
position 3 to 5 (peak at 4), magnitude 0.38. One spike+up from position 4 to 6 (peak at 5), magnitude 0.38. One spike+down from position 6 to 8 (peak at 7), magnitude 0.21.
One spike+up from position 7 to 9 (peak at 8), magnitude 0.21. One spike+down from position 12 to 14 (peak at 13), magnitude 0.33. One smooth+up from position 17 to
25 (peak at 21), magnitude 0.17. One smooth+down from position 30 to 42 (peak at 36), magnitude 0.17. One spike+up from position 45 to 47 (peak at 46), magnitude 0.17.
One spike+down from position 66 to 68 (peak at 67), magnitude 0.17. One smooth+up from position 66 to 72 (peak at 69), magnitude 0.33. One smooth+down from
position 72 to 76 (peak at 74), magnitude 0.15. One spike+up from position 79 to 81 (peak at 80), magnitude 0.15. One spike+down from position 80 to 82 (peak at 81),
magnitude 0.37. One smooth+up from position 89 to 95 (peak at 92), magnitude 0.23. Noise std_deviation 1.958.
Execution. L = 96; 17 events; MSE 0.0061; DTW 0.0471; PC 0.9315.
                                                          ETTm1-96 HUFL: MSE=0.0061, DTW=0.0471, PC=0.9315
                      1.0
                                                                                                                                    Target       Generated
              Norm.




                      0.5

                      0.0
                            0                    20                           40                          60                          80
                                                                                    Time index
Folded params.
length=96; target_mean=7.952; target_std=5.324; noise_std=1.9584
trend: linear(0-47): -3.084 -> 12.914; linear(48-95): 15.794 -> 6.164
seasonality: none
events: 17 total = 5 smooth + 12 spike; 10 with magnitude >= 0.2; max magnitude=0.474
top events: spike+up at 3 [2,4], mag=0.474; spike+down at 2 [1,3], mag=0.444; spike+down at 4 [3,5], mag=0.384; spike+up at
      5 [4,6], mag=0.384

Generated code.
def generate_ts(params):
    import numpy as np
    length = params[’length’]
    t = np.arange(length, dtype=float)

     def _trend_seg(n, sv, ev, stype, extra):
         if n <= 0:
             return np.array([])
         if n == 1:
             return np.array([sv])
         tn = np.arange(n, dtype=float) / (n - 1)
         return sv + (ev - sv) * tn

     trend = np.zeros(length)
     for _s in params[’trend_segments’]:
         _a, _b = (_s.get(’start’, 0), _s.get(’end’, length - 1))
         trend[_a:_b + 1] = _trend_seg(_b - _a + 1, _s.get(’start_value’, 0.0), _s.get(’end_value’, _s.get(’start_value’, 0.0)
                ), _s.get(’trend_type’, ’constant’), _s)
     _last = params[’trend_segments’][-1]
     _last_end = _last.get(’end’, length - 1)
     if _last_end < length - 1:
         trend[_last_end + 1:] = trend[_last_end]
     seasonality = np.zeros(length)
     changes_array = np.zeros(length)
     for change in params.get(’changes’, []):
         ch_type = change.get(’change_type’, ’spike’)
         direction = change.get(’direction’, ’up’)
         tp = change.get(’turning_point’, length // 2)
         mag = abs(change.get(’magnitude’, 0.0))
         if direction == ’down’:
             mag = -mag
         sp = change.get(’start_position’, None)
         ep = change.get(’end_position’, None)
         sigma = max(1.0, (ep - sp) / 4.0)
         changes_array += mag * np.exp(-0.5 * ((t - tp) / sigma) ** 2)
     noise_segments = params.get(’noise_segments’, None)
     noise = np.zeros(length)
     noise_std = abs(params.get(’noise_std’, 0.0))
     raw_ts = trend + seasonality + changes_array + noise
     raw_mean = raw_ts.mean()
     raw_std = raw_ts.std()
     ts = (raw_ts - raw_mean) / raw_std * params.get(’target_std’, raw_std) + params.get(’target_mean’, raw_mean)
     return ts




                                                                                   29
NeurIPS Paper Checklist
    1. Claims
      Question: Do the main claims made in the abstract and introduction accurately reflect the
      paper’s contributions and scope?
      Answer: [Yes]
      Justification: The abstract and introduction state the main contributions of CodeTS, includ-
      ing the Text-to-Code-to-TS formulation, normalized executable code interface, synthetic
      Text-Code-TS triplet initialization, and execution-based RLVR optimization. The stated
      experimental claims are supported by comparisons on eight public benchmarks across three
      generation lengths, and the scope is qualified by the limitations discussion on univariate
      generation and ambiguous descriptions.
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
      Justification: The conclusion discusses the main scope limitations, including the focus on
      univariate time series and sensitivity to ambiguous descriptions. Additional risks related
      to synthetic data usage and executable code generation are discussed in the broader impact
      section.
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


                                                 30
       judgment and recognize that individual actions in favor of transparency play an impor-
       tant role in developing norms that preserve the integrity of the community. Reviewers
       will be specifically instructed to not penalize honesty concerning limitations.
3. Theory assumptions and proofs
  Question: For each theoretical result, does the paper provide the full set of assumptions and
  a complete (and correct) proof?
  Answer: [N/A]
  Justification: The paper does not present theoretical results, theorems, or formal proofs. The
  mathematical formulations are used to define the Text-to-Code-to-TS framework, reward
  design, and optimization objective.
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
  Justification: The paper provides the key information needed to reproduce the main results,
  including benchmark datasets, metrics, model initialization, reward definitions, prompts,
  and SFT/RLVR hyperparameters. An anonymized repository is provided to support code
  reproduction.
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
       of a large language model), releasing of a model checkpoint, or other means that are
       appropriate to the research performed.
     • While NeurIPS does not require releasing code, the conference does require all submis-
       sions to provide some reasonable avenue for reproducibility, which may depend on the
       nature of the contribution. For example
       (a) If the contribution is primarily a new algorithm, the paper should make it clear how
            to reproduce that algorithm.
       (b) If the contribution is primarily a new model architecture, the paper should describe
            the architecture clearly and fully.


                                           31
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
  Answer: [Yes]
  Justification: An anonymized code repository is provided in the paper, and the appendix
  documents the public data sources used for training and evaluation. The repository provides
  the implementation and supporting materials for reproducing the main experimental results.
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
  Justification: The paper specifies the benchmark datasets, generation lengths, evaluation met-
  rics, baseline categories, model backbone, SFT and RLVR training settings, reward weights,
  and optimization hyperparameters. Additional details on reward definitions, prompts, real
  data sources, and training configuration are provided in the appendix.
   Guidelines:
      • The answer [N/A] means that the paper does not include experiments.
      • The experimental setting should be presented in the core of the paper to a level of detail
        that is necessary to appreciate the results and make sense of them.
      • The full details can be provided either with the code, in appendix, or as supplemental
        material.
7. Experiment statistical significance


                                            32
  Question: Does the paper report error bars suitably and correctly defined or other appropriate
  information about the statistical significance of the experiments?
  Answer: [Yes]
  Justification: The paper reports aggregate performance metrics, including MSE, DTW, and
  Pearson correlation, to evaluate the generated time series against the ground-truth series.
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
  Answer: [No]
  Justification: The paper reports the main compute hardware and memory configuration,
  including the use of NVIDIA A100-SXM4-80GB GPUs for SFT and RLVR training.
  However, it does not provide wall-clock running time, per-experiment execution time, or an
  estimate of total compute consumption.
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
  Answer: [Yes]
  Justification: The research uses public datasets and pretrained models, reports the evaluation
  protocol, and discusses limitations, broader impacts, and safeguards for executable-code
  generation. To the best of the authors’ knowledge, the work conforms to the NeurIPS Code
  of Ethics.


                                           33
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
   Justification: The appendix includes a Broader Impact section discussing potential posi-
   tive impacts in data-scarce time series domains such as healthcare, energy, transportation,
   finance, and climate analysis. It also discusses negative risks, including over-reliance on
   synthetic data, inherited bias, misleading downstream evaluations, and security concerns
   from executable code generation.
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
   Answer: [Yes]
   Justification: The paper describes safeguards for executable code generation, including
   normalized code formatting, format validation, sandboxed execution, and success rate
   reporting. The broader impact section further notes that real world deployment should
   include domain-specific validation, provenance tracking, privacy assessment, and disclosure
   of synthetic data usage.
   Guidelines:
      • The answer [N/A] means that the paper poses no such risks.
      • Released models that have a high risk for misuse or dual-use should be released with
        necessary safeguards to allow for controlled use of the model, for example by requiring


                                            34
          that users adhere to usage guidelines or restrictions to access the model or implementing
          safety filters.
       • Datasets that have been scraped from the Internet could pose safety risks. The authors
          should describe how they avoided releasing unsafe images.
       • We recognize that providing effective safeguards is challenging, and many papers do
          not require this, but we encourage authors to take this into account and make a best
          faith effort.
12. Licenses for existing assets
    Question: Are the creators or original owners of assets (e.g., code, data, models), used in
    the paper, properly credited and are the license and terms of use explicitly mentioned and
    properly respected?
    Answer: [No]
    Justification: The paper credits the main datasets, pretrained models, and software compo-
    nents through citations and public source URLs, and the appendix lists the public RLVR
    training data sources. However, it does not yet explicitly document the license names,
    versions, and terms of use for all existing assets.
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
    Answer: [Yes]
    Justification: The paper provides an anonymized repository containing the implementation
    and supporting materials for CodeTS. The paper and appendix document the training proce-
    dure, reward design, prompts, data sources, limitations, and broader impact considerations
    relevant to these released assets.
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


                                             35
    Answer: [N/A]
    Justification: The paper does not involve crowdsourcing experiments or research with human
    subjects. All experiments are conducted on public time series datasets, synthetic triplets,
    and model generated outputs.
    Guidelines:
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
    Justification: The paper does not involve crowdsourcing or human-subjects research, so IRB
    approval or equivalent review is not applicable.
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
    Justification: LLMs are a core methodological component of the work: CodeTS is initialized
    from Qwen2.5-Coder-7B-Instruct and trained to generate executable code from textual time
    series descriptions. The paper describes this use in the method, experimental setup, training
    configuration, and prompt appendix.
    Guidelines:
       • The answer [N/A] means that the core method development in this research does not
          involve LLMs as any important, original, or non-standard components.
       • Please refer to our LLM policy in the NeurIPS handbook for what should or should not
          be described.




                                             36
