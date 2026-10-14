                                                                                                                                               January 27, 2026




                                                 TheoremForge: Scaling up Formal Data Synthesis with
                                                 Low-Budget Agentic Workflow
                                                 Yicheng Tao 1 , Hongteng Xu∗ 1, 2, 3
                                                 1
                                                   Gaoling School of Artificial Intelligence, Renmin University of China
                                                 2
                                                   Beijing Key Laboratory of Research on Large Models and Intelligent Governance
                                                 3
                                                   Engineering Research Center of Next-Generation Intelligent Search and Recommendation, MOE


                                                                                                   Abstract
                                                 The high cost of agentic workflows in formal mathematics hinders large-scale data synthesis, ex-
arXiv:2601.17332v1 [cs.AI] 24 Jan 2026




                                                 acerbating the scarcity of open-source corpora. To address this, we introduce TheoremForge, a
                                                 cost-effective formal data synthesis pipeline that decomposes the formalization process into five
                                                 sub-tasks, which are statement formalization, proof generation, premise selection, proof correction
                                                 and proof sketching. By implementing a Decoupled Extraction Strategy, the workflow recovers valid
                                                 training signals from globally failed trajectories, effectively utilizing wasted computation. Experi-
                                                 ments on a 2,000-problem benchmark demonstrate that TheoremForge achieves a Verified Rate of
                                                 12.6%, surpassing the 8.6% baseline, at an average cost of only $0.481 per successful trajectory using
                                                 Gemini-3-Flash. Crucially, our strategy increases data yield by 1.6× for proof generation compared
                                                 to standard filtering. These results establish TheoremForge as a scalable framework for constructing
                                                 a data flywheel to train future expert models. Our code is available here.



                                         1           Introduction
                                         Agentic workflows based on large language models have recently achieved significant advancements in the
                                         domain of formal mathematics. Compared to traditional single-turn interaction paradigms, agentic workflows
                                         demonstrate superior performance and robustness in autoformalization and automated theorem proving
                                         tasks (Varambally et al., 2025; Chen et al., 2025b,c; Xu et al., 2025; Wang et al., 2025b). This success is
                                         largely attributed to targeted strategy designs and test-time scaling techniques. However, the scarcity of
                                         training data hinders further development in this field. The diverse task requirements within workflows and
                                         the inherent data scarcity of the formalization domain exacerbate this challenge. Many current studies employ
                                         proprietary data for training while open-source formalization data remain insufficient in terms of quantity and
                                         diversity. Synthesizing training data suitable for formal reasoning models at a low cost and large scale has
                                         therefore become a critical research question.
                                         Current formalization tasks are primarily categorized into Autoformalization and Automated Theorem Prov-
                                         ing. A complete formalization workflow should be capable of translating natural language mathematical
                                         propositions into semantically consistent formal propositions and generating compilable proofs. We analyze
                                         common and effective strategy designs in existing methods to extract five sub-tasks (see Figure 1). These
                                         include statement formalization (Gao et al., 2025; Chen et al., 2025a; Wang et al., 2025b), proof genera-
                                         tion (Wang et al., 2025a; Lin et al., 2025; Xin et al., 2025b,a; Ren et al., 2025), premise selection (Gao et al.,
                                         2024; Asher, 2025; Liu et al., 2025; Wang et al., 2025b), proof correction (Lin et al., 2025; Chen et al.,
                                         2025c), and proof sketching (Jiang et al., 2023; Varambally et al., 2025; Chen et al., 2025b,c). Optimizing
                                         these sub-tasks individually provides a modular path toward enhancing the global performance of the for-
                                         malization pipeline. The open-source community currently lacks training data for tasks other than statement
                                         formalization and proof generation. Furthermore, the absence of expert models for the remaining sub-tasks
                                             ∗
                                                 Corresponding author. Email: hongtengxu@ruc.edu.cn



                                                                                                        1
necessitates the use of general-purpose large models as substitutes.
                                                                                        Formalization Sub-Tasks
This paper focuses on data synthesis for these five sub-tasks and
                                                                               Informal Statement         Formal Statement               Query         Verifier
presents TheoremForge. This complete formalization workflow
                                                                               Informal Proof           Subgoal                Premise            Formal Proof
covers all the aforementioned tasks and serves as a data synthesis
                                                                          Statement Formalization                         Premise Selection
pipeline that achieves a favorable cost-performance trade-off. We
utilize Gemini-3-Flash as the reasoning model to attain an average
cost for a successful trajectory of $0.481. Existing formalization
workflows aim primarily to improve success rates and incur ex-            Proof Generation                                Proof Correction

tremely high test-time scaling costs (Varambally et al., 2025; Chen                                                               Error Message       ❌
et al., 2025b,c). These high costs manifest as large-scale parallel
sampling and iterative subgoal decomposition which makes them
unsuitable for large-scale data synthesis.                                Proof Sketching



The contributions of this paper are summarized below.
                                                                                                        Proof Sketch


• We design and open-source a formalization workflow capable of
                                                                                                    TheoremForge
  generating the full process from natural language mathematical        NL Problem                                                                     FL Proof
                                                                                            Premise                    Proof Generation
  propositions to formal proofs.                                                            Selection


                                                                                                                    Proof             Proof

• The workflow serves as a low-cost data synthesis pipeline for                           Statement
                                                                                        Formalization
                                                                                                                  Correction        Sketching



  formal training data which covers multiple sub-tasks and facil-
  itates the training of agentic models.
                                                                       Figure 1 . Schematic overview of the for-
• We evaluate the performance and cost of common formalization         malization workflow and its five sub-tasks.
  strategies under low inference budgets to provide a benchmark
  for future research.


2    Preliminaries and Notations
We formally define the five sub-tasks and their data formats. For concrete data instances, please refer to
Appendix C.
Statement Formalization translates an informal statement SN into a formal specification SF conditioned
on retrieved premises P . While syntax is compiler-verified, semantic equivalence is often evaluated via
LLM-as-Judge Chen et al. (2025a); Gao et al. (2025) to ensure the mathematical meaning is preserved.
Training samples are triplets (SN , P, SF ), where SF is both syntactically and semantically valid.
Proof Generation aims to generate a complete formal proof RF from SF and P that passes the kernel check.
Unlike translation, the correctness of RF is deterministically verifiable, providing an objective reasoning
signal. Training samples are triplets (SF , P, RF ).
Premise Selection identifies pertinent definitions and theorems P from a library Yang et al. (2023) using
natural language queries Q based on SN /SF . Effective selection reduces context noise and prevents model
overwhelm. Training samples are triplets (SN /SF , Q, P ) where premises directly contribute to a successful
downstream formalization or proof.
Proof Correction leverages compiler error messages E to repair a failed proof RF into a successful version
RF′ Lin et al. (2025). This task emphasizes iterative refinement and precise fault localization, significantly
enhancing efficiency compared to re-sampling Chen et al. (2025c). Training samples are triplets (RF , E, RF′ ).
Proof Sketching decomposes complex theorems into manageable intermediate subgoals. Given SF , P ,
and a natural language proof RN , the model generates a compilable sketch RS as a high-level reasoning
roadmap Varambally et al. (2025). Training samples are quadruplets (SF , P, RN , RS ).




                                                      2
                                                             Semantic Check
                        Statement
                      Normalization

                                                                                  Formalization        Formal
    Target Theorem                          Formalizer       Semantic Check
                                                                                    Selection         Statement



                                                             Semantic Check   ❌
                     Agentic Search


Figure 2 . Statement Formalization Workflow. The pipeline consists of three phases: 1) Information Preprocessing
for normalization and definition retrieval; 2) Expert Model Sampling for candidate generation and compilation checks;
and 3) Statement Filtering for semantic verification via LLM-as-Judge and final selection.


3     System Design
In this section, we present the architecture of TheoremForge. While the system functions as a robust solver
through two primary stages defined as Statement Formalization and Proof Generation, its overarching
design objective is to serve as a high-efficiency data synthesis pipeline. We explicitly architect the workflow
to support a Decoupled Extraction Strategy which maximizes data yield by independently validating
and harvesting intermediate outputs from every inference trajectory. We detail the execution logic of the
formalization and proving stages followed by the specific mechanisms for data extraction. See Appendix A
for details.

3.1    Statement Formalization
The system must derive a syntactically correct and semantically aligned formal statement from the input prior
to generating a proof. The workflow for this process is illustrated in Figure 2.
Information Preprocessing. Informal input statements exhibit diverse characteristics in both type and form.
This heterogeneity often compels the formalization process to encompass ancillary tasks such as supplying
implicit premises, solving for numerical answers, and interpreting ambiguous semantics. These factors can
adversely affect model performance. We first employ a general-purpose LLM to denoise the input statement
before engaging the expert formalizer to address these challenges. We subsequently implement an agentic
premise selection strategy leveraging the open-source search engine LeanExplore Asher (2025). The model
generates search queries Q based on the normalized statement SN and selectively incorporates valid premises
P from the retrieval results into the context.
Statement Filtering. The workflow imposes a series of filtering procedures on the statements SF generated
by the expert model to enhance the quality of formalization. These procedures encompass both syntactic and
semantic verifications. We retain only those candidates that successfully pass both compilation checks and
semantic evaluations based on the LLM-as-Judge paradigm. The optimal statement is then selected as the
final output of the formalization phase. This process effectively eliminates distractors that exhibit obvious
semantic inconsistencies although it does not guarantee the absolute correctness of the formalization.

3.2    Proof Generation
We employ the workflow illustrated in Figure 3 to search for a valid proof if the system successfully formalizes
the statement. The design of this workflow draws inspiration from Hilbert Varambally et al. (2025) and
principally adopts strategies involving iterative proof refinement driven by compiler feedback together with
subgoal decomposition based on proof sketches.
Iterative Proof Refinement. The workflow captures compiler feedback from failed attempts by either the
expert or general-purpose LLM to guide repairs. To prevent context pollution and ensure synthesized data


                                                         3
                                                           Subgoal            General LLM
    Formal              Prover                                                                 Proof
                                         Proof Sketching                                                   Formal Proof
   Statement       (with Correction)                                                          Assembly
                                                           Subgoal            General LLM


                         ❌
                               Agentic Search


Figure 3 . Proof Generation Workflow. The process comprises two phases. 1) Expert Model Sampling is where an
expert model is invoked to generate a proof. A general-purpose LLM attempts to rectify the errors if all candidates fail.
2) Subgoal Decomposition is where a proof sketch is generated and the problem is decomposed into subgoals.


remains consistent with our formal task definition, we restrict the model’s visibility strictly to the incorrect
code RF and current error message E , excluding interaction history. This stateless design ensures that each
refinement step can be extracted as an independent, high-quality (RF , E, RF′ ) correction pair, effectively
maximizing data yield from globally failed trajectories. We maintain scalability by capping iteration rounds
to balance reasoning depth with computational expenditure.
Subgoal Decomposition. The workflow proceeds to the subgoal decomposition phase should the proof
remain incomplete relying solely on the expert model and proof correction. This stage initiates with an
agentic premise selection process analogous to that used in statement formalization yet is distinguished by the
fact that the model generates retrieval queries based specifically on the formal statement SF . The premises
P obtained thereby serve as the shared context for all subsequent subgoal proof attempts. The workflow
builds upon this foundation by prompting the general-purpose LLM to generate a comprehensive step-by-step
natural language proof RN before attempting to construct a formal proof sketch RS . The embedded subgoals
are extracted for parallel resolution via a generation sequence that utilizes the expert model followed by the
general-purpose LLM provided the sketch successfully passes compilation. These subgoals are synthesized
with the original sketch to constitute the complete formal proof RF upon the successful verification of all
subgoals.

3.3    Decoupled Data Extraction Strategy
The efficiency of TheoremForge as a data synthesis pipeline stems from its ability to isolate valid training
signals even when the global reasoning trajectory fails. Unlike traditional approaches that filter solely for
complete proofs, we implement a decoupled extraction strategy that harvests high-quality training samples
for individual sub-tasks based on local verification signals. This approach ensures that intermediate successes
such as a correct formal statement or a verified subgoal are preserved regardless of the final outcome. We
delineate the sourcing logic for each specific data type below.
Statement Formalization Data. We extract valid triplets (SN , P, SF ) from all trajectories where the formal
statement SF passes the compilation check and the semantic check. This process is independent of the
subsequent proof generation success and allows us to harvest formalization data at a high rate.
Proof Generation Data. We extract verified proofs from two distinct sources. The first source is the
successful trajectories of the main theorems. The second source comprises the individual subgoals that are
successfully proved during the decomposition phase even if the parent theorem remains unproved. This
strategy significantly expands the dataset volume as a single failed trajectory often yields multiple valid
lemma-proof pairs from its subgoals.
Premise Selection Data. We construct positive samples by strictly filtering for premises that explicitly appear
in the successfully generated code, including successful subgoals in a failed trajectory. This ensures that the
selected premises are not merely retrieved but are essential for the derivation. Hard negatives can be easily


                                                           4
generated using the invalid queries and unused retrieval results.
Proof Correction Data. The iterative refinement module provides a rich source of correction pairs
(RF , E, RF′ ). We capture every instance within the refinement loop where the model successfully fixes a
compilation error regardless of whether the final proof is completed. This mechanism effectively converts
intermediate failures into valuable debugging data.
Proof Sketching Data. We capture proof sketches generated during the subgoal decomposition phase. While
we collect all sketches that pass the compilation check to ensure structural diversity, we note that only those
sketches that result in a fully closed proof are guaranteed to be logically sound. These verified sketches
constitute the high-quality core of the dataset while the remaining compilable sketches serve as supplementary
data or hard negative cases for downstream training.


4       Experiments
We conduct a comprehensive evaluation of TheoremForge to validate its efficacy as a scalable data synthesis
pipeline for formal mathematics. Our experiments focus on assessing the capabilities of general-purpose
LLMs within this workflow. We place particular emphasis on the trade-off between reasoning performance
and computational cost to ensure the feasibility of large-scale data generation.
We organize our experimental analysis around four pivotal research questions.
• RQ1: How do different general-purpose foundation models compare in utilizing the workflow for formal-
  ization, and which model offers the optimal balance between capability and efficiency?
• RQ2: Is TheoremForge a cost-effective solution for large-scale data synthesis, and what are the specific
  resource expenditures associated with successful trajectories?
• RQ3: How robust is the workflow across diverse mathematical domains and difficulty levels, and what
  characterizes the distribution of the synthesized data?
• RQ4: How do individual agentic modules contribute to the overall success of the workflow, and what are
  the characteristic bottlenecks that lead to failed trajectories?
In the following subsections, we first detail the experimental setup including benchmarks and baselines before
presenting empirical results that address these research questions sequentially.

4.1     Experimental Setup
Datasets. We construct a small-scale (100 problems) and a large-scale (2,000 problems) evaluation set by
sampling uniformly from DeepMath (He et al., 2025), which comprises 103K challenging problems, and
DeepTheorem (Zhang et al., 2025e), which contains 121K IMO-level proof-based theorems.
Baseline. Due to the lack of open-source end-to-end workflows, we establish a baseline by directly applying
expert models without agentic orchestration: ReForm-32B (Chen et al., 2025a) for formalization and Goedel-
Prover-32B (Lin et al., 2025) for proving. To ensure fair comparison, these models also serve as the underlying
expert modules in TheoremForge, with a consistent sampling budget of n = 4.1
Metrics. We evaluate the workflow across three metrics: (1) Formalization Rate (FR): the percentage of
successfully compiled statements; (2) Proof Rate (PR): the percentage of valid formal proofs generated; and
(3) Verified Rate (VR): the percentage of problems judged semantically consistent by a majority vote of
LLM verifiers. To ensure independence, for each problem, we exclude the original generator from the pool of
7 participating models and use the remaining 6 as judges2 . See Appendix A.4 for details.
    1
     The workflow will make extra expert calls. However, the improvement in sampling budget can be marginal.
    2
     DeepSeek-V3.2 variants (with and without thinking) are treated as a single model entity. If either variant is the generator, both
are excluded from the voting pool to ensure independence.


                                                                  5
Environment. We use Lean v4.19.0 to match the LeanExplore (Asher, 2025) database.
For detailed configurations, see Appendix A.

4.2      RQ1: Model Selection and Performance Analysis
Table 1 . Model performance comparison on the small-scale benchmark. Gemini-3-Pro and Gemini-3-Flash are tested
with low thinking level. The tokens and cost are calculated excluding expert models. We define Expert Calls as the total
number of sampling invocations by the expert model, where a pass@4 task is counted as four calls. Best and Second
Best results are highlighted.

                                   DeepMath                    DeepTheorem          Overall   Expert   Tokens    Cost
 Model
                             FR       PR        VR        FR       PR        VR       VR       Calls     (M)    (USD)
 GPT-5.2                   74.0%     14.0%    14.0%     58.0%    16.0%     14.0%     14.0%     1372     3.41    $17.27
 Claude-Sonnet-4.5         88.0%     28.0%    26.0%     80.0%    36.0%     32.0%     29.0%     2072     5.12    $32.83
 Gemini-3-Pro (low)        90.0%     32.0%    30.0%     76.0%    42.0%     36.0%     33.0%     1608     7.90    $65.21
 Gemini-3-Flash (low)      94.0%     26.0%    20.0%     72.0%    32.0%     26.0%     23.0%     1616     4.70     $6.94
 DeepSeek-V3.2-Thinking    70.0%     10.0%     8.0%     54.0%    18.0%     18.0%     13.0%      900     3.09     $2.72
 DeepSeek-V3.2             68.0%     18.0%    14.0%     62.0%    22.0%     22.0%     18.0%     1100     3.14     $2.78
 Qwen-Max                  88.0%     10.0%    10.0%     76.0%    22.0%     22.0%     16.0%      796     2.94     $2.45
 Baseline                  92.0%     16.0%    14.0%     76.0%    20.0%     16.0%     15.0%      736       –        –

We specifically investigate the performance of various general-purpose large language models acting as the
reasoning core of TheoremForge to answer the first research question. The results presented in Table 1 reveal
significant disparities in both formalization capability and economic efficiency across different models.
Effectiveness of the Agentic Workflow. A comparison between the baseline and the agentic configurations
highlights the substantial value added by the workflow. The baseline method employs the expert models
directly and achieves a high Formalization Rate of 92.0% on DeepMath. This indicates that the ReForm-
32B model is proficient at generating syntactically correct Lean code. However, the verified rate of the
baseline remains limited at 15.0% overall. In contrast, workflows driven by capable reasoning models such as
Gemini-3-Pro and Claude-Sonnet-4.5 significantly outperform the baseline with verified rates reaching 33.0%
and 29.0% respectively. This empirical evidence suggests that the inclusion of premise selection, iterative
proof refinement, and subgoal decomposition modules effectively converts static formalization capability into
successful theorem proving outcomes.
Cost-Performance Trade-off. The feasibility of large-scale data synthesis depends critically on the balance
between success rate and inference cost. We visualize this relationship in Figure 4a which maps the verified
rate against the average cost per verified problem. The plot reveals that Gemini-3-Flash occupies the
optimal upper-left region of the Pareto frontier. This positioning indicates that it achieves high verification
performance while maintaining minimal expenditure per successful instance. While Gemini-3-Pro delivers
the highest raw performance, it is situated in the upper-right high-cost region and incurs a substantial total
cost of $65.21. Conversely, Gemini-3-Flash achieves 69.7% of the performance of the Pro version but reduces
the total cost by approximately 89.4% to merely $6.94. This also represents a significant efficiency advantage
over Claude-Sonnet-4.5 which costs $32.83. DeepSeek and Qwen appear in the bottom-left region as the most
economical options but their low success rates render them unsuitable for generating high-quality training
data.
Mechanism of Collaboration. We previously demonstrated the synergy of general-purpose LLM and
expert model. Figure 4b further details this mechanism by plotting cumulative success against the token
consumption of the general-purpose LLM. The extended tails observed for Gemini-3-Pro demonstrate that
powerful reasoning models effectively leverage larger token budgets to raise the performance upper bound of
the workflow. In contrast, less capable models tend to plateau early regardless of the available budget.



                                                           6
                             Cost-Performance Trade-off Across Models                                                       Empirical Cumulative Distribution of Verified Problems over Token Budget
                 35
                                                                                                                                                                                               Gemini-3-Pro
                                                                      Gemini-3-Pro                                      30                                   Claude-Sonnet-4.5




                                                                                                Cumulative Verified Count
                 30
                                                        Claude-Sonnet-4.5                                               25                 Gemini-3-Flash
 Verified Rate (%)



                                                                                                                                                                                         Avg. Tokens per Verified
                 25                                                                                                     20                  DeepSeek-V3.2
                                Gemini-3-Flash                                                                                                                                           Gemini Pro 52.8K
                                                                                                                        15                           GPT-5.2                             Gemini Flash 33.7K
                                                                                                                                      Qwen-Max
                 20                                                                                                                                         DeepSeek-V3.2-Thinking
                            DeepSeek-V3.2                                                                               10
                            Qwen-Max
                 15                                        GPT-5.2                                                          5
                             DeepSeek-V3.2-Thinking                         Avg Rate: 20.9%
                                                                            Avg Cost: $0.737
                                                                                                                            0
                     0.0           0.5            1.0           1.5               2.0                                        0K              50K               100K              150K           200K
                                  Average Cost per Verified Problem (USD)                                                                          Token Consumption (per problem)
                                                 (a)                                                                                                                  (b)

Figure 4 . (a) This figure illustrates the cost–performance comparison across different models, where models located
in the upper-left region achieve a more favorable balance. The average cost is calculated by Total Cost / Number of
Verified Problem. (b) This figure compares models by the cumulative number of verified problems as a function of
per-problem token consumption, revealing their efficiency under limited computational budgets.


4.3                        RQ2: Scalability and Data Synthesis Efficiency
We assess the scalability of TheoremForge by deploying the Gemini-3-Flash powered workflow on the
large-scale benchmark comprising 2,000 problems. This experiment evaluates both the robustness of the
system on unseen data and the economic feasibility of mass production.
Large-scale Performance and Cost. The results presented in Table 2 demonstrate the superior performance
of our workflow compared to the baseline expert models. Gemini-3-Flash achieves a verified rate of 12.60%
which surpasses the 8.60% rate of the baseline. This improvement confirms that the agentic strategies remain
effective when scaled to a larger and more diverse problem set. Most critically, the average cost for generating
a successful verified trajectory is merely $0.481. This is a manageable budget for academic and industrial
research labs relative to the high value of formal mathematics data.

      Table 2 . Comparison between TheoremForge (with Gemini-3-Flash) and Baseline on the large-scale benchmark.

                                            Method                             FR               PR                                      VR           Expert Calls                 Avg Cost
                                            TheoremForge                    81.30%             14.45%                                 12.60%                 24056                   $0.4806
                                            Baseline                        72.25%             12.55%                                  8.60%                 13780                      –

Efficiency of Decoupled Extraction. The statistics presented in Figure 5 validate the success of our strategy
in salvaging valuable data from globally failed inference trajectories. We observe that valid samples extracted
from failed trajectories constitute the majority of the dataset for key tasks like statement formalization
and proof generation. Specifically, the workflow harvests 1,338 valid formalization samples from failed
runs which is more than four times the number obtained from successful trajectories. Similarly, the sub-
task of proof generation benefits from subgoal decomposition as it yields 1,129 valid lemma proofs from
failed trajectories compared to only 693 from successful ones. This result demonstrates that TheoremForge
effectively maximizes the utility of computational resources by identifying and preserving local successes
within broader failures.
Necessity of Specialized Training. The relatively lower data yields observed in proof sketching and proof
correction reveal the inherent limitations of current general-purpose LLMs in handling these specific tasks.
The total volume of collected samples for proof correction is the lowest among all sub-tasks with only 334
instances combined. This scarcity indicates that general-purpose LLMs struggle to accurately diagnose and

                                                                                                                                  7
                                                   Sub-Task Data Collection Statistics
                               2000
                                                                         Successful Trajectory       Failed Trajectory
                                      693 / 1129
                                                      289 / 1338
           Number of Samples
                               1500



                                                                     195 / 849
                               1000



                                                                                          55 / 520
                                500
                                                                                                        113 / 221


                                  0
                                        Proof         Statement      Premise              Proof          Proof
                                      Generation     Formalization   Selection          Sketching      Correction

Figure 5 . Data collection statistics for the five sub-tasks. The stacked bars distinguish between samples derived from
fully successful trajectories (bottom) and valid samples extracted from intermediate steps of failed trajectories (top).
The latter reveals data yield improvements by decoupled extraction..


repair functional code based on compiler error messages. A similar trend is evident in proof sketching where
the model often fails to generate logically sound high-level structures that lead to valid proofs. These findings
underscore the critical need for training specialized expert models for these tasks. The data synthesized by
our pipeline, though limited in quantity for these specific tasks, serves as a high-quality seed corpus to initiate
the training of such experts.

4.4    RQ3: Domain Robustness and Data Distribution
We analyze the distribution of the synthesized data across diverse mathematical domains and difficulty levels
to characterize the quality and training potential of the generated corpus.
Metadata Unification. To facilitate a standardized analysis, we unify the heterogeneous metadata schemas
from DeepTheorem and DeepMath. For domain classification, we aggregate specific tags into broad macro-
categories including Algebra, Geometry, Analysis, Discrete Mathematics, Number Theory, Applied Mathe-
matics and Other. We utilize the primary label for classification when a problem contains multiple domain
tags. We further align the differing numerical difficulty scales into three tiers defined as Easy, Normal, and
Hard. Specifically, we define Easy as difficulty values up to 6 for DeepTheorem and 4 for DeepMath. We
classify values above 8 for DeepTheorem and 7 for DeepMath as Hard while the intermediate ranges are
designated as Normal.
Domain Robustness. Figure 6a illustrates the Verified rate across different mathematical fields. Theorem-
Forge consistently surpasses the baseline in all categories and demonstrates a comprehensive coverage of
formal mathematics. The workflow exhibits particular strength in Algebra and Number Theory where the
verified rates are notably high. This performance suggests that the agentic strategies effectively handle
symbolic manipulation and arithmetic properties which are foundational to formal reasoning. This broad
domain coverage ensures that the synthesized dataset promotes semantic diversity.
Adaptability to Difficulty. Figure 6b presents the distribution of verified problems across difficulty levels.
We observe a natural inverse correlation between problem complexity and verified rate. The DeepMath dataset


                                                                     8
   Performance Breakdown by Mathematical Domain                                                                Verified Problems by Difficulty Level
                   Applied Mathematics
                                                                                            60
                                                  Analysis                                                                                DeepTheorem            DeepMath
                                                                                                            47.3%
                                                                                            50              (44/93)
 Discrete Mathematics




                                                                        Verified Rate (%)
                                                                                            40

                                         10%      20%      30%Algebra                       30

                                                                                            20    13.3%                                15.0%
                                                                                                 (74/555)                            (102/678)
      Geometry                                                                                                                                          7.1%
                                                                                            10                              5.6%                        (5/70)
                                                                                                                          (21/374)                                2.6%
                                                                                                                                                                 (6/229)
                                                   Other
                                                                                            0
                        Number Theory                                                                  Easy                   Normal                         Hard
                         TheoremForge          Baseline                                                                    Difficulty Level
                                (a)                                                                                         (b)

Figure 6 . Robustness Analysis across Domain and Difficulty. (a) The radar chart illustrates the verified rate across
five aggregated mathematical domains where TheoremForge consistently outperforms the baseline. (b) The bar chart
details the verification statistics across three difficulty tiers. While success rates decline with complexity, the workflow
successfully synthesizes a valuable set of high-difficulty training samples.


exhibits a high success rate of 47.3% in the Easy category which provides a solid foundation of fundamental
training data. DeepTheorem generally presents a greater challenge although the workflow successfully
verifies a combined total of 11 Hard problems across both datasets. These successful high-difficulty samples
are particularly valuable as they represent complex reasoning paths that contain rich logical structures. The
resulting data distribution forms a natural curriculum that spans from abundant simple exercises to sparse but
high-quality complex theorems.

4.5       RQ4: Component Analysis and Failure Modes
We analyze the results on large-scale benchmark to identify the performance gains from each module and
categorize failure trajectories.
Module Contributions. As shown in Figure 7 (Left), while the Expert Prover completes 69.9% of tasks,
agentic modules provide a 30.1% boost: Subgoal Decomposition accounts for 19.0%, tackling complex
theorems beyond monolithic horizons, and Iterative Refinement contributes 11.1% by repairing local tactical
errors via compiler feedback.
Failure and Bottleneck Analysis. Figure 7 (Right) identifies Proof Sketching as the primary bottleneck
(47.8% of failures). Although the system generated 575 compilable sketches, many were logically unsound
or led to unjustifiable subgoals, highlighting the challenge of ensuring mathematical viability over mere
syntactic correctness.
Subgoal Dynamics and Efficiency. Subgoal Solving is the second-largest failure category (30.3%). Across
5,763 extracted subgoals (∼10 per sketch), the expert model proved 1,372, with 161 recovered through
refinement and 196 definitive failures. Crucially, 4,034 subgoals were bypassed by our early stop policy,
which terminates a sketch’s remaining subgoals as soon as one fails. This mechanism significantly optimizes
resources by pruning unviable trajectories.
Detailed error taxonomies are in Appendix B.




                                                                                                 9
                 Success Reason                                                   Failed Phase
                        19.0%                                                           30.4%
                                   11.1%

                                                                          14.5%


                                                                           7.3%
                                                                                                47.8%
                          69.9%



                   Expert Prover                                                    Syntax Check
                   Iterative Proof Refinement                                       Semantic Check
                   Subgoal Decomposition                                            Proof Sketching
                                                                                    Subgoal Solving

Figure 7 . Analysis of the Formalization Workflow. (Left) Success reasons for verified proofs. (Right) Distribution of
failed phases.


5     Related Works
5.1    Agentic Architectures
Agentic workflows extend single-pass inference through iterative planning and tool integration which enables
structured reasoning for complex tasks. Recent research emphasizes automating architecture design via
agentic supernets to search for optimal multi-agent compositions (Zhang et al., 2025c; Wang et al., 2025e;
Zhang et al., 2025b; Hu et al., 2025b). Self-improvement mechanisms further allow agents to adaptively
develop and maintain complex software libraries through continuous iteration (Zhang et al., 2025a; Wang et al.,
2025d). Execution-aware approaches integrate runtime feedback or external solvers to refine solutions (Ni
et al., 2025; Yuksekgonul et al., 2025; Singh et al.; Nezhad et al., 2025). Theoretical frameworks for
heterogeneous agents also investigate strategic collaboration to ensure rationality and truthful contribution
among diverse components (Clinton et al.). These advancements collectively support the shift towards
modular systems where specialized agents collaborate to solve long-horizon problems.

5.2    AI for Formal Mathematics
The integration of large language models with formal methods is increasingly recognized as a prerequisite
for building trustworthy AI agents (Zhang et al., 2025d; Wang et al., 2024; Yao et al., 2025). Contemporary
systems in formal mathematics predominantly employ modular workflows that decompose theorem proving
into coordinated sub-tasks. These systems leverage the Lean kernel for rigorous feedback and enable scalable
exploration through specialized components (Lin et al., 2025; Xin et al., 2025b; Varambally et al., 2025;
Chen et al., 2025b,c; Hubert et al., 2025; Xu et al., 2025; Hu et al., 2025a; Baba et al., 2025; Ospanov et al.,
2025; Kozyrev et al.; Wang et al., 2025c). For autoformalization tasks, recent methods shift from purely
semantic translation to process-driven approaches that exploit tactic structures and type checkers to guide
stepwise formalization (Jana et al., 2025; Lu et al., 2025; Wang et al., 2025b).




                                                         10
6    Conclusion and Discussion
In this paper we present TheoremForge, a formal data synthesis pipeline to accumulate high-quality training
data for downstream formalization tasks. It shows potential in establishing a data flywheel by iteratively
training sub-task experts using the synthetic data. Here are some discussions about the insights and limitations
of our work.
Decoupling Reasoning from Coding. Our workflow underscores the necessity of specialized agents over
monolithic solvers. Since mathematical reasoning and formal coding require divergent cognitive capabilities,
and specialized models often lag behind general-purpose ones in reasoning Jiang et al. (2025), a collaborative
paradigm that divides labor based on model strengths is more effective for complex formalization.
Efficiency and Scaling. To bridge the gap between vast natural language mathematics and scarce formal
corpora, synthesis must optimize both quality control and cost-performance. We posit that the future of
scalable formalization lies in deploying lightweight, specialized models on distinct sub-tasks. Running such
models locally can maximize throughput and minimize computational overhead without relying on expensive
proprietary APIs.
Limitations and Evaluation. Due to high computational costs and the practical challenges of replicating
existing agentic workflows, a direct empirical comparison with other contemporary systems remains for
future work. Furthermore, while this study focuses on the synthesis framework itself, the downstream impact
of the generated data on model fine-tuning has not yet been fully quantified. Systematically evaluating these
performance gains and benchmarking TheoremForge against alternative architectures are essential next steps
to validate the utility of our synthetic corpora.


References
Justin Asher. Leanexplore: A search engine for lean 4 declarations, 2025.
Kaito Baba, Chaoran Liu, Shuhei Kurita, and Akiyoshi Sannai. Prover agent: An agent-based framework for formal
  mathematical proofs. In 2nd AI for Math Workshop @ ICML 2025, 2025.
Guoxin Chen, Jing Wu, Xinjie Chen, Wayne Xin Zhao, Ruihua Song, Chengxi Li, Kai Fan, Dayiheng Liu, and Minpeng
  Liao. Reform: Reflective autoformalization with prospective bounded sequence optimization, 2025a.
Jiangjie Chen, Wenxiang Chen, Jiacheng Du, Jinyi Hu, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing Jin, Chenggang
   Li, Wenlei Shi, Zhihong Wang, Mingxuan Wang, Chenrui Wei, Shufa Wei, Huajian Xin, Fan Yang, Weihao Gao,
   Zheng Yuan, Tianyang Zhan, Zeyu Zheng, Tianxi Zhou, and Thomas Hanwen Zhu. Seed-prover 1.5: Mastering
   undergraduate-level theorem proving via learning from experience, 2025b.
Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing Jin, Chenggang
  Li, Kaijing Ma, Cheng Ren, Jiawei Shen, Wenlei Shi, Tong Sun, He Sun, Jiahui Wang, Siran Wang, Zhihong Wang,
  Chenrui Wei, Shufa Wei, Yonghui Wu, Yuchen Wu, Yihang Xia, Huajian Xin, Fan Yang, Huaiyuan Ying, Hongyi
  Yuan, Zheng Yuan, Tianyang Zhan, Chi Zhang, Yue Zhang, Ge Zhang, Tianyun Zhao, Jianqiu Zhao, Yichi Zhou, and
  Thomas Hanwen Zhu. Seed-prover: Deep and broad reasoning for automated theorem proving, 2025c.
Alex Clinton, Yiding Chen, Jerry Zhu, and Kirthevasan Kandasamy. Collaborative mean estimation among heterogeneous
  strategic agents: Individual rationality, fairness, and truthful contribution. In Forty-second International Conference
  on Machine Learning.
Guoxiong Gao, Haocheng Ju, Jiedong Jiang, Zihan Qin, and Bin Dong. A semantic search engine for mathlib4. In Yaser
  Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, Findings of the Association for Computational Linguistics:
  EMNLP 2024, pages 8001–8013, Miami, Florida, USA, November 2024. Association for Computational Linguistics.
  doi: 10.18653/v1/2024.findings-emnlp.470.
Guoxiong Gao, Yutong Wang, Jiedong Jiang, Qi Gao, Zihan Qin, Tianyi Xu, and Bin Dong. Herald: A natural language
  annotated lean 4 dataset. In The Thirteenth International Conference on Learning Representations, 2025.



                                                          11
Zhiwei He, Tian Liang, Jiahao Xu, Qiuzhi Liu, Xingyu Chen, Yue Wang, Linfeng Song, Dian Yu, Zhenwen Liang,
  Wenxuan Wang, Zhuosheng Zhang, Rui Wang, Zhaopeng Tu, Haitao Mi, and Dong Yu. Deepmath-103k: A large-scale,
  challenging, decontaminated, and verifiable mathematical dataset for advancing reasoning. 2025.
Jilin Hu, Jianyu Zhang, Yongwang Zhao, and Talia Ringer. Hybridprover: Augmenting theorem proving with llm-driven
   proof synthesis and refinement, 2025a.
Yaojie Hu, Qiang Zhou, Qihong Chen, Xiaopeng Li, Linbo Liu, Dejiao Zhang, Amit Kachroo, Talha Oz, and Omer
  Tripp. Qualityflow: An agentic workflow for program synthesis controlled by llm quality checks. arXiv preprint
  arXiv:2501.17167, 2025b.
Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z Horváth, Goran Žužić, Eric Wieser, Aja Huang, Julian
  Schrittwieser, Yannick Schroecker, Hussain Masoom, et al. Olympiad-level formal mathematical reasoning with
  reinforcement learning. Nature, pages 1–3, 2025.
Prithwish Jana, Kaan Kale, Ahmet Ege Tanriverdi, Cruise Song, Sriram Vishwanath, and Vijay Ganesh. Proofbridge:
  Auto-formalization of natural language proofs in lean via joint embeddings, 2025.
Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou, Timothee Lacroix, Jiacheng Liu, Wenda Li, Mateja Jamnik,
  Guillaume Lample, and Yuhuai Wu. Draft, sketch, and prove: Guiding formal theorem provers with informal proofs.
  In The Eleventh International Conference on Learning Representations, 2023.
Jiedong Jiang, Wanyi He, Yuefeng Wang, Guoxiong Gao, Yongle Hu, Jingting Wang, Nailing Guan, Peihao Wu, Chunbo
   Dai, Liang Xiao, et al. Fate: A formal benchmark series for frontier algebra of multiple difficulty levels. arXiv
   preprint arXiv:2511.02872, 2025.
Andrei Kozyrev, Nikita Khramov, Gleb Solovev, and Anton Podkopaev. Rocqstar: Leveraging similarity-driven retrieval
  and agentic systems for rocq generation. In NeurIPS 2025 Fourth Workshop on Deep Learning for Code.
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng, Jiawei Ge, Jingruo
  Sun, et al. Goedel-prover-v2: Scaling formal theorem proving with scaffolded data synthesis and self-correction.
  arXiv preprint arXiv:2508.03613, 2025.
Qi Liu, Xinhao Zheng, Xudong Lu, Qinxiang Cao, and Junchi Yan. Rethinking and improving autoformalization:
  Towards a faithful metric and a dependency retrieval-based approach. In The Thirteenth International Conference on
  Learning Representations, 2025.
Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang, Jing Xiong, Liu Chengwu, Jianhao Shen, Hui Jin, Jipeng
   Zhang, Haiming Wang, Zhicheng Yang, Jing Tang, and Zhijiang Guo. Process-driven autoformalization in lean 4,
   2025.
Sina Bagheri Nezhad, Yao Li, and Ameeta Agrawal. Symcode: A neurosymbolic approach to mathematical reasoning
  via verifiable code generation. arXiv preprint arXiv:2510.25975, 2025.
Ziyi Ni, Yifan Li, Ning Yang, Dou Shen, Pin Lyu, and Daxiang Dong. Tree-of-code: A self-growing tree framework for
  end-to-end code generation and execution in complex tasks. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova,
  and Mohammad Taher Pilehvar, editors, Findings of the Association for Computational Linguistics: ACL 2025, pages
  9804–9819, Vienna, Austria, July 2025. Association for Computational Linguistics. ISBN 979-8-89176-256-5. doi:
  10.18653/v1/2025.findings-acl.509.
Azim Ospanov, Farzan Farnia, and Roozbeh Yousefzadeh. APOLLO: Automated LLM and lean collaboration for
  advanced formal reasoning. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025.
Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu, Qihao
  Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao, Daya Guo, and
  Chong Ruan. Deepseek-prover-v2: Advancing formal mathematical reasoning via reinforcement learning for subgoal
  decomposition, 2025.
Joykirat Singh, Raghav Magazine, Yash Pandya, and Akshay Nambi. Agentic reasoning and tool integration for llms via
  reinforcement learning, 2025. 5.
Sumanth Varambally, Thomas Voice, Yanchao Sun, Zhifeng Chen, Rose Yu, and Ke Ye. Hilbert: Recursively building
  formal proofs with informal reasoning, 2025.


                                                        12
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood Sung, Marina Vinyes,
  Zhenzhe Ying, Zekai Zhu, Jianqiao Lu, Hugues de Saxcé, Bolton Bailey, Chendong Song, Chenjun Xiao, Dehao
  Zhang, Ebony Zhang, Frederick Pu, Han Zhu, Jiawei Liu, Jonas Bayer, Julien Michel, Longhui Yu, Léo Dreyfus-
  Schmidt, Lewis Tunstall, Luigi Pagani, Moreira Machado, Pauline Bourigault, Ran Wang, Stanislas Polu, Thibaut
  Barroyer, Wen-Ding Li, Yazhe Niu, Yann Fleureau, Yangyang Hu, Zhouliang Yu, Zihan Wang, Zhilin Yang, Zhengying
  Liu, and Jia Li. Kimina-prover preview: Towards large formal reasoning models with reinforcement learning. 2025a.
Hanyu Wang, Ruohan Xie, Yutong Wang, Guoxiong Gao, Xintao Yu, and Bin Dong. Aria: An agent for retrieval and
  iterative auto-formalization via dependency graph, 2025b.
Lei Wang, Ruobing Zuo, Gaolei He, Jianlin Wang, and Zhengfeng Yang. Qdtsynth: Quality-driven formal theorem
  synthesis for enhancing proving performance of llms. In Proceedings of the 63rd Annual Meeting of the Association
  for Computational Linguistics (Volume 1: Long Papers), pages 14683–14698, 2025c.
Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe Diao, Renjie Pi, and Tong Zhang. Theoremllama: Transforming
  general-purpose llms into lean4 experts. arXiv preprint arXiv:2407.03203, 2024.
Yanbo Wang, Zixiang Xu, Yue Huang, Xiangqi Wang, Zirui Song, Lang Gao, Chenxi Wang, Xiangru Tang, Yue Zhao,
  Arman Cohan, Xiangliang Zhang, and Xiuying Chen. Dyflow: Dynamic workflow framework for agentic reasoning.
  In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025d.
Yingxu Wang, Siwei Liu, Jinyuan Fang, and Zaiqiao Meng. Evoagentx: An automated framework for evolving agentic
  workflows. arXiv preprint arXiv:2507.03616, 2025e.
Huajian Xin, Z.Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang, Xuan Lu,
  Qiushi Du, Wenjun Gao, Haowei Zhang, Qihao Zhu, Dejian Yang, Zhibin Gou, Z.F. Wu, Fuli Luo, and Chong Ruan.
  Deepseek-prover-v1.5: Harnessing proof assistant feedback for reinforcement learning and monte-carlo tree search.
  In The Thirteenth International Conference on Learning Representations, 2025a.
Ran Xin, Zeyu Zheng, Yanchen Nie, Kun Yuan, and Xia Xiao. Scaling up multi-turn off-policy rl and multi-agent tree
  search for llm step-provers. arXiv preprint arXiv:2509.06493, 2025b.
Jundong Xu, Hao Fei, Meng Luo, Qian Liu, Liangming Pan, William Yang Wang, Preslav Nakov, Mong-Li Lee, and
  Wynne Hsu. Aristotle: Mastering logical reasoning with a logic-complete decompose-search-resolve framework.
  In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar, editors, Proceedings of
  the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 3052–
  3075, Vienna, Austria, July 2025. Association for Computational Linguistics. ISBN 979-8-89176-251-0. doi:
  10.18653/v1/2025.acl-long.153.
Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan Prenger, and
  Anima Anandkumar. LeanDojo: Theorem proving with retrieval-augmented language models. In Neural Information
  Processing Systems (NeurIPS), 2023.
Jiarui Yao, Ruida Wang, and Tong Zhang. FANS: Formal answer selection for LLM natural language math reason-
   ing using lean4. In Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng, editors,
   Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pages 3181–3200,
   Suzhou, China, November 2025. Association for Computational Linguistics. ISBN 979-8-89176-332-6. doi:
   10.18653/v1/2025.emnlp-main.158.
Mert Yuksekgonul, Federico Bianchi, Joseph Boen, Sheng Liu, Pan Lu, Zhi Huang, Carlos Guestrin, and James Zou.
 Optimizing generative ai by backpropagating language model feedback. Nature, 639:609–616, 2025.
Genghan Zhang, Weixin Liang, Olivia Hsu, and Kunle Olukotun. Adaptive self-improvement LLM agentic system for
  ML library development. In ICLR 2025 Third Workshop on Deep Learning for Code, 2025a.
Guibin Zhang, Luyang Niu, Junfeng Fang, Kun Wang, LEI BAI, and Xiang Wang. Multi-agent architecture search via
  agentic supernet. In Forty-second International Conference on Machine Learning, 2025b.
Jiayi Zhang, Jinyu Xiang, Zhaoyang Yu, Fengwei Teng, Xiong-Hui Chen, Jiaqi Chen, Mingchen Zhuge, Xin Cheng,
   Sirui Hong, Jinlin Wang, Bingnan Zheng, Bang Liu, Yuyu Luo, and Chenglin Wu. AFlow: Automating agentic
   workflow generation. In The Thirteenth International Conference on Learning Representations, 2025c.



                                                        13
Yedi Zhang, Yufan Cai, Xinyue Zuo, Xiaokun Luan, Kailong Wang, Zhe Hou, Yifan Zhang, Zhiyuan Wei, Meng Sun,
  Jun Sun, Jing Sun, and Jin Song Dong. Position: Trustworthy AI agents require the integration of large language
  models and formal methods. In Forty-second International Conference on Machine Learning Position Paper Track,
  2025d.
Ziyin Zhang, Jiahao Xu, Zhiwei He, Tian Liang, Qiuzhi Liu, Yansi Li, Linfeng Song, Zhenwen Liang, Zhuosheng
  Zhang, Rui Wang, Zhaopeng Tu, Haitao Mi, and Dong Yu. Deeptheorem: Advancing llm reasoning for theorem
  proving through natural language and reinforcement learning, 2025e.




                                                      14
Appendix
A       Implementation and Configuration
In this section, we present a detailed demonstration of the implementation of TheoremForge workflow and
the inference configuration. Some of the prompts are taken from Hilbert (Varambally et al., 2025), which will
not be presented here. These include prompts for search query generation, premise selection, proof sketch
generation, iterative proof refinement, subgoal extraction and proof assembly. You can find the details in our
code. Our code is open-sourced3 .

A.1     Details on Closed-Source Models and Reproducibility
All closed-source large language models used in our experiments were accessed via commercial API services.
Except for Qwen-Max, all models were invoked through the CloseAI aggregation platform4 . Qwen-Max was
accessed through the Alibaba Cloud Large Model Platform 5 . GPT-5.2, Claude Sonnet 4.5, DeepSeek models,
and Qwen-Max were called using an OpenAI-compatible SDK, while Gemini models were accessed via the
official Google GenAI SDK.
For the concrete model identifiers used in our experiments, see Table 3. All experiments were conducted in
December 2025 using the latest available model versions at the time.
For inference configuration, the sampling temperature was set to 0 for all non-Gemini models. For Gemini
models, we followed the provider’s recommendation and set the temperature to 1.0. All other inference
parameters were left at their platform-default values.
All evaluated models except for DeepSeek-V3.2 are proprietary and closed-source, and explicit version
hashes were not exposed through the APIs. Moreover, these models may undergo unannounced updates by
the service providers. We therefore report the exact model identifiers, access platforms, SDKs, inference
parameters, and the evaluation time window to maximize reproducibility. While exact bit-level reproducibility
cannot be guaranteed, these details sufficiently constrain the experimental setting to enable meaningful
comparison under comparable API
The local expert models are served on a 4xA100 server. The prices are calculated using Table 3.

                    Table 3 . Identifier and pricing of evaluated language models ($/M token).

             Model                          Identifier                             Input    Output
             Gemini-3-Pro                   gemini-3-pro-preview                    2.00     12.00
             Gemini-3-Flash                 gemini-3-flash-preview                  0.50      3.00
             GPT-5.2                        gpt-5.2                                 1.75     14.00
             DeepSeek-V3.2                  deepseek-chat                           0.55      1.70
             DeepSeek-V3.2-Thinking         deepseek-reasoner                       0.55      1.70
             Qwen-Max                       qwen-max                                0.46      1.84
             Claude-Sonnet-4.5              claude-sonnet-4-5                       3.00     15.00


A.2     Statement Formalization Workflow
Statement Normalization. Input statements vary in format and often contain implicit premises or lack explicit
answers. This step preprocesses and normalizes the inputs to facilitate accurate downstream translation.
    3
      https://github.com/timechess/TheoremForge.git
    4
      https://www.closeai-asia.com/
    5
      https://bailian.console.aliyun.com/


                                                         15
Definition Retrieval. Based on the normalized statement, we prompt the LLM to generate up to kquery = 5
queries to search for relevant definitions. We utilize the open-source search engine LeanExplore (Asher,
2025) to retrieve the top-5 most similar constants from Mathlib for each query. Subsequently, we prompt the
LLM selects the most relevant constants from these results.
Expert Sampling. Given the normalized statement and the selected constants, we employ an expert model
to generate kformalizer = 4 candidates and perform syntax checks using the compiler. If no valid code is
generated, we prompt the LLM to attempt a fix based on the compiler’s error messages. If not otherwise
mentioned, we only give one chance for correction to each failed code in this section.
Semantic Check. All candidates that pass the syntax check undergo semantic verification, where the LLM
assesses their consistency with the original input semantics. The final justification will be a binary signal,
which is “ALIGNED” or “NOT_ALIGNED”. If the LLM identifies an inconsistency, it is prompted to provide
a correction. If the corrected code compiles successfully, it is deemed to have passed the semantic check.
Formalization Selection. Following the filtering steps, we instruct the LLM to select the optimal candidate
as the final output based on criteria such as semantic consistency and estimated proof difficulty. The model is
also required to provide a rationale for its selection.

A.3    Proof Generation
Expert Sampling. We invoke an expert prover model to generate kprover = 4 candidate proofs. If all
candidates fail, we prompt the LLM to correct the proofs. We observe that most open-source prover models
are not trained in a retrieval-augmented style. Consequently, providing auxiliary theorems in the context
offers negligible performance benefits at this stage.
Theorem Retrieval. This phase mirrors the definition retrieval process used in the statement formalization
workflow.
Informal Proof Generation. Given the formal statement and the retrieval results, we prompt the LLM to
generate a step-by-step informal proof to serve as a reference for the subsequent decomposition.
Subgoal Decomposition. Using the formal statement, retrieval results, and the informal proof, we prompt
the LLM to generate a formal proof sketch. This sketch includes several intermediate steps (using have
statements) and the logic connecting them. We then leverage the LLM to extract these have statements
into independent lemmas. We rely on LLM-based extraction rather than the extract_goals tactic, as
the latter has proven unreliable in certain contexts. If the proof sketch fails the compiler check, the LLM is
prompted to attempt a fix.
Subgoal Solving. The extracted subgoals undergo the expert sampling stage. We do not perform new retrieval
for these subgoals. Instead, we reuse the retrieval results from the root problem. Still, we first sample from
the expert prover with kprover = 4 attempts and try to correct the failed proofs if all fail. If the expert prover
cannot provide valid proofs with one chance to correct, we prompt the general-purpose LLM to generate
an informal proof for this subgoal. Then the LLM is required to generate the formal proof according to the
informal proof, along with useful theorems retrieved in the stage ahead. We set krefine = 2 to allow at most 2
attempts to fix failed proof.
Proof Assembly. Once all subgoals are solved, we prompt the LLM to synthesize the final proof by
assembling the sub-proofs according to the original sketch. If the assembly fails, we give the LLM one
chance to fix. If one subgoal fails to be proved, then the other subgoals in the queue will be cancelled, serving
as an Early Stop policy to save budget.

A.4    Semantic Verification
Here we provide a detailed specification of the semantic verification process.


                                                       16
Let P = {p1 , . . . , pN } denote a set of mathematical problems expressed in natural language. For each
problem pi , a proof generation model produces a formal statement ŷi . We only perform semantic verifications
for formal statements that succeed in generating proofs. Assuming there are M ≤ N problems satisifying the
condition, denoted as {p′1 , . . . , p′M }.

Verifier Models and Identities. We consider a set of K = 7 LLM-based semantic verifier models

                                                E = {E1 , E2 , . . . , E7 }.

Each verifier Ek is associated with a verifier identity id(Ek ). In particular, different variants of the same
underlying model (DeepSeek-V3.2 with and without thinking) are treated as sharing the same identity.
Each verifier takes as input a pair (p′i , ŷi ), where p′i is the original natural-language proposition and ŷi′ is the
generated formal output, and outputs a binary judgment

                                                  Ek (p′i , ŷi′ ) ∈ {0, 1},

with 1 indicating that ŷi′ is judged to be semantically consistent with the meaning of p′i , and 0 otherwise.

Exclusion of Generator from Voting. Let Gi denote the generator model that produces ŷi′ . To avoid self-
evaluation bias, all verifier models whose identities coincide with that of the generator are excluded from
voting. Formally, the effective verifier set for (p′i , ŷi′ ) is defined as

                                        Ei = {Ek ∈ E | id(Ek ) ̸= id(Gi )}.

For Baseline, we do not exclude any model.

Majority-Based Verification Rule. Let |Ei | denote the number of effective verifiers for problem pi . We define
the aggregated semantic verification decision V (pi , ŷi ) using majority voting over Ei :
                                                                               
                                               1, if P E (p′ , ŷ ′ ) ≥ |Ei | ,
                                               
                                                               k i i
                             V (p′i , ŷi′ ) =       Ek ∈Ei                  2
                                               
                                                0, otherwise.

Verified Rate. The Verified Rate (VR) is defined as the fraction of problems whose generated outputs are
semantically verified under the above aggregation rule while having a valid proof:
                                                                   M
                                                    1 X
                                               VR =     V (p′i , ŷi′ ).
                                                    N
                                                                  i=1


Conservative and Lenient Variants. For completeness, we also define two alternative verification criteria
based on the effective verifier set Ei :
                                                         "                         #
                                                           X
                                 Vstrict (pi , ŷi ) = I     Ek (pi , ŷi ) = |Ei | ,
                                                              Ek ∈Ei
                                                              "                             #
                                                                   X
                                   Vlenient (pi , ŷi ) = I                Ek (pi , ŷi ) ≥ 1 ,
                                                                  Ek ∈Ei

which provide conservative and optimistic bounds on the reported verified rate, respectively.



                                                                  17
Results on Semantic Verification. The results for verified rates (VR) across different models and aggregation
rules are summarized in Table 4 and Figure 8a. Among all evaluated models on the small-scale benchmark,
Gemini-3-Pro (low) and Claude-Sonnet-4.5 demonstrate the highest formalization quality, achieving 33.0%
and 29.0% Majority VR, respectively. Notably, we observe a substantial gap between Strict VR and Lenient
VR; for instance, Gemini-3-Pro drops from 36.0% (Lenient) to 16.0% (Strict), suggesting that while most
models can produce formalizations recognized as correct by at least one verifier, achieving universal consensus
across all LLM judges remains a high bar. On the large-scale benchmark, TheoremForge significantly
outperforms the baseline (12.6% vs. 8.6% Majority VR), validating the efficacy of our proposed framework
in maintaining semantic fidelity during large-scale formalization tasks.

                          Table 4 . Semantic verified rates (VR) under different aggrega-
                          tion rules on small-scale and large-scale benchmarks.

                       Model / Method              Majority VR     Strict VR    Lenient VR
                       Small-Scale Benchmark
                       GPT-5.2                         14.0            6.0         15.0
                       Claude-Sonnet-4.5               29.0           12.0         31.0
                       Gemini-3-Flash (low)            23.0            9.0         29.0
                       Gemini-3-Pro (low)              33.0           16.0         36.0
                       DeepSeek-V3.2-Thinking          13.0            8.0         14.0
                       DeepSeek-V3.2                   18.0           12.0         20.0
                       Qwen-Max                        16.0            4.0         16.0
                       Baseline                        15.0            4.0         18.0
                       Large-Scale Benchmark
                       TheoremForge                    12.6            6.2         14.2
                       Baseline                         8.6            4.2         11.9


Inter-Judge Reliability. To evaluate the consistency of the LLM-based ensemble, we analyze the inter-judge
agreement between verifier models. The agreement rate A(Ea , Eb ) between two verifiers Ea , Eb ∈ E is
defined as the fraction of instances where they provide identical judgments, calculated over the set of problems
where both models are eligible to vote. Formally:
                                     PM
                                          I[Ea ∈ Ei ∧ Eb ∈ Ei ∧ Ea (p′i , ŷi′ ) = Eb (p′i , ŷi′ )]
                      A(Ea , Eb ) = i=1           PM
                                                    i=1 I[Ea ∈ Ei ∧ Eb ∈ Ei ]

where I[·] is the indicator function. Note that A(Ea , Ea ) = 1.0 by definition.
As illustrated in Figure 8b, the majority of verifier pairs exhibit robust consensus, with agreement rates
typically exceeding 0.75. The Gemini family shows the highest internal consistency, with an agreement rate
of 0.90 between Gemini Flash and Gemini Pro. Claude also demonstrates strong alignment with both the
Gemini and DeepSeek series, maintaining scores between 0.80 and 0.84.
However, GPT stands out as a relative outlier, exhibiting a noticeably lower agreement with all other verifiers
in the ensemble. Specifically, its agreement rates with other frontier models range from a minimum of
0.54 (with Qwen Max) to a maximum of only 0.72 (with Claude). This systematic divergence suggests that
GPT may employ a fundamentally different or more idiosyncratic internal rubric for assessing semantic
equivalence compared to its peers. Such results underscore the importance of our ensemble-based majority
voting, as it prevents the specific biases or divergent judgment patterns of a single model like GPT from
disproportionately affecting the final verified rate.




                                                       18
                                                                            Verified Rate Comparison                                                                                                                                Inter-Judge Agreement
                                                                                                                                                                                                                                                                                         1.0
                0.4                                                                                                                                                                                                       Claude 1.00     0.80    0.81       0.80   0.84   0.72   0.77
                                         0.36                                                                                           Majority                       Strict                       Lenient
                           0.33                                                                                                                                                                                                                                                          0.8
                                                               0.31                                                                                                                                                    DeepSeek 0.80      1.00    0.81       0.82   0.79   0.69   0.72
                0.3                              0.29                                   0.29




                                                                                                                                                                                                                                                                                               Agreement Rate
                                                                                                                                                                                                                DeepSeek-Thinking 0.81    0.81    1.00       0.79   0.81   0.69   0.73
Verified Rate



                                                                         0.23                                                                                                                                                                                                            0.6
                                                                                                               0.20                                                                                                  Gemini Flash 0.80    0.82    0.79       1.00   0.90   0.62   0.81
                0.2                                                                              0.18                                                         0.18
                                  0.16                                                                                  0.16          0.16      0.15                               0.15
                                                                                                                                                                     0.14                                0.14                                                                            0.4
                                                        0.12                                            0.12                                                                               0.13                       Gemini Pro 0.84     0.79    0.81       0.90   1.00   0.64   0.82
                0.1                                                              0.09                                                                                                             0.08
                                                                                                                                                                            0.06                                            GPT 0.72      0.69    0.69       0.62   0.64   1.00   0.54   0.2
                                                                                                                               0.04                    0.04
                                                                                                                                                                                                                       Qwen Max 0.77      0.72    0.73       0.81   0.82   0.54   1.00
                0.0                                                                                                                                                                                                                                                                      0.0
                               ro                       e                     sh                     ek                   Max                       ne
                                                   ud                                                                                            eli                  GPT                    king




                                                                                                                                                                                                                                e




                                                                                                                                                                                                                                                         sh

                                                                                                                                                                                                                                                                    o

                                                                                                                                                                                                                                                                        Qw T

                                                                                                                                                                                                                                                                                x
                           ni P




                                                                                                                                                                                                                                         ek

                                                                                                                                                                                                                                                 ing
                                                                            la                     Se




                                                                                                                                                                                                                                                                             Ma
                                                                                                                                                                                                                               ud




                                                                                                                                                                                                                                                                Pr
                                                Cla




                                                                                                                                                                                                                                                                             GP
                                                                      ini F                                           wen                    Bas                                         hin




                                                                                                                                                                                                                                                       Fla
                                                                                                                                                                                                                                    Se
                       emi                                                                     eep




                                                                                                                                                                                                                                              ink
                                                                                                                                                                                                                             Cla




                                                                                                                                                                                                                                                               ni
                                                                                                                                                                                    ek-T




                                                                                                                                                                                                                                                                          en
                                                                                                                                                                                                                                    ep
                                                                                           D




                                                                                                                                                                                                                                                             mi
                                                                                                                                                                                                                                          -Th

                                                                                                                                                                                                                                                   ni
                      G                                        Gem                                                Q




                                                                                                                                                                                                                                   De




                                                                                                                                                                                                                                                  mi

                                                                                                                                                                                                                                                         Ge
                                                                                                                                                                             pSe




                                                                                                                                                                                                                                         ek

                                                                                                                                                                                                                                                 Ge
                                                                                                                                                                                                                                        Se
                                                                                                                                                                      Dee




                                                                                                                                                                                                                                    ep
                                                                                                                                                                                                                                   De
                                                                                                (a)                                                                                                                                              (b)

 Figure 8 . Quantitative analysis of the semantic verification process. (a) Comparison of verified rate (VR) on the
 small-scale benchmark under Majority, Strict, and Lenient aggregation rules. (b) Heatmap of pairwise agreement rates
 between the seven LLM verifiers. Higher values (darker blue) indicate stronger consensus between models. The results
 are calculated using verification data from large-scale benchmark (including TheoremForge and Baseline).


 A.5                      Prompts
                Prompt for Statement Normalization

                You are helping to prepare an informal mathematical statement for formalization
                 ,→ into Lean.
                The input statement may be a math word problem, a question, or an incomplete
                 ,→ statement that needs to be transformed into a clear mathematical proposition.

                Normalization Process:
                1. Convert questions into declarative statements:
                   - "What is the value of x?" -> "The value of x is [answer]" or "There exists a
                    ,→ unique x such that..."
                   - "Is f continuous?" -> "f is continuous" or "f is not continuous"
                   - "Can we prove that...?" -> "It holds that..." or "The statement ... is true"

                2. Transform word problems into formal propositions:
                   - Extract the mathematical content from the narrative
                   - Identify all variables, constraints, and relationships
                   - State what needs to be proven or computed as a clear proposition

                3. Make implicit statements explicit:
                   - Add missing quantifiers (for all, there exists)
                   - Specify domains and ranges of variables
                   - If the constraints can be inferred or proved from the problem, do not add
                    ,→ them to the normalized statement

                4. Structure the proposition clearly:
                   - State assumptions/hypotheses first
                   - Then state the conclusion or claim
                   - Use standard mathematical language and notation

                Guidelines:
                - If the statement is already a clear proposition, you may keep it as is
                - If it's a question without a known answer, solve the problem and state the
                 ,→ answer along with the constraints as a proposition




                                                                                                                                                               19
- If it's a question with an answer provided, state the answer along with the
 ,→ constraints as a proposition
- Maintain the mathematical content and intent of the original statement
- Use precise mathematical language suitable for formalization
- Check whether the normalized statement is semantically aligned with the
 ,→ informal statement
- DO NOT only output the answer to the problem, you should state the answer along
 ,→ with the constraints as a proposition.

Input Statement:

{{ informal_statement }}

Output Format:
Provide the normalized statement in <normalized> tags.

Please reason step by step before providing the normalized statement.



Prompt for Semantic Check

You are an expert in mathematical formalization and Lean 4. Your task is to
 ,→ verify that a formal Lean 4 statement accurately captures the mathematical
 ,→ meaning of the original informal statement.

Original Informal Statement:
{{ informal_statement }}

{% if normalized_statement %}
Normalized Statement:
{{ normalized_statement }}
{% endif %}

{% if useful_definitions %}
Useful Definitions:
{{ useful_definitions }}
{% endif %}

Generated Formal Statement (Lean 4):
```lean4
{{ formal_statement }}
```

Your Task:
Carefully analyze whether the formal Lean 4 statement is semantically aligned
 ,→ with the original informal statement{% if normalized_statement %} and the
 ,→ normalized statement{% endif %}. Note that the normalized statement may
 ,→ contain information (e.g. the answer to a question) that is not present in
 ,→ the informal statement. Check whether the normalized statement is aligned
 ,→ with the informal statement. Then check whether the formal statement is
 ,→ aligned with the normalized statement. If NOT_ALIGNED, try to fix the formal
 ,→ statement to be aligned with the informal statement.

Evaluation Criteria:
1. **Mathematical Equivalence**: Does the formal statement express the same
 ,→ mathematical claim as the normalized statement?
2. **Completeness**: Are all conditions, hypotheses, and conclusions from the
 ,→ normalized statement captured in the formal statement?




                                       20
3. **Correctness**: Are the mathematical objects, operations, and properties
 ,→ correctly formalized?
4. **Type Accuracy**: Are the types and type classes appropriate for the
 ,→ mathematical concepts?
5. **Quantifiers**: Are the quantifiers used correctly and do they match the
 ,→ informal statement?
6. **No Extra Constraints**: Does the formal statement avoid introducing
 ,→ additional constraints not present in the normalized statement? Or does the
 ,→ normalized statement contain additional constraints that are not present in
 ,→ the informal statement?
7. **No Missing Constraints**: Does the formal statement include all constraints
 ,→ from the normalized statement?
8. **Provability**: Is the formal statement provable given the provided premises?

Analysis Process:
1. Identify the key mathematical concepts in the informal statement
2. Check how each concept is formalized in the Lean 4 code
3. Verify that the logical structure is preserved
4. Look for any discrepancies, missing elements, or extra constraints
5. Check whether the formal statement is provable given the provided premises

Output Format:
Provide your analysis in the following structure:

<analysis>
[Provide a detailed step-by-step analysis comparing the informal and formal
 ,→ statements]
</analysis>

<verdict>
[Output EXACTLY one of: "ALIGNED" or "NOT_ALIGNED"]
</verdict>

<fixed_formal_statement>
[Output the fixed formal statement inside ```lean4``` code blocks. You should only
 ,→ output ONE fixed formalization at the end.]
</fixed_formal_statement>



Prompt for Formalization Selection

You are an expert in Lean 4 theorem proving. Your task is to select the BEST
 ,→ formalization to prove from multiple semantically aligned formalizations of
 ,→ the same informal statement.

**Informal Statement:**
{{ informal_statement }}

**Available Formalizations:**
{% for idx, formalization in formalizations %}
**Formalization {{ idx + 1 }}:**
```lean4
{{ formalization }}
```
{% endfor %}

**Instructions:**
1. Analyze each formalization carefully, considering:




                                        21
   - Structural complexity
   - How many hypotheses need to be handled
   - Whether the formalization uses complex type theory constructs
   - Whether it requires proving stronger/more general results
   - Availability of library theorems that might help
   - How natural the proof approach would be
   - Avoid using too general definitions that are hard to compute. (e.g.
    ,→ `Euclidean.dist` in real space or general `Field` instead of $\mathbb{Q}$.)
   - If the informal statement contains quantifiers, the formalization should
    ,→ also contain quantifiers.

2. The BEST formalization should be EASY to prove while maintaining the
 ,→ mathematical meaning of the informal statement.

3. Provide your analysis in the following format:
   - Wrap your reasoning in <analysis></analysis> tags
   - Specify the selected formalization number (1, 2, 3, etc.) in
    ,→ <selected>number</selected> tags

**Example Response Format:**
<analysis>
Your detailed reasoning about why you chose this formalization...
</analysis>
<selected>2</selected>



Prompt for Semantic Verification

Role: Lean & Formal Verification Expert

Input:

- Mathematical_Text: A math problem and its answer (no proof).
- Lean4Code: A Lean 4 theorem statement formalizing the problem. Proof is
 ,→ intentionally omitted (e.g., sorry).

Goal:
Determine if the Lean theorem statement is an exact and faithful formalization of
 ,→ the mathematical problem.
**Do not evaluate or consider the answer or the proof. Your sole task is to
 ,→ verify the correctness of the formalization.**

Evaluation Stages (All required):

1. Math Assertion Analysis
   Identify all structurally and semantically relevant components of the
    ,→ mathematical problem, including variables, types, quantifiers,
    ,→ constraints, logic structure, conclusion, and so on. The analysis should
    ,→ be based on the actual content of the text.

2. Lean Statement Analysis (ignore proof part)
   Extract all structurally and semantically relevant components from the Lean
    ,→ statement, including variables, types, conditions, quantifiers,
    ,→ constraints, the final claim, and so on. The analysis should reflect the
    ,→ actual content present in the Lean code.

3. Comparative Verification




                                          22
       Check for exact correspondence between the math and Lean statements; you may
        ,→ refer to aspects like:
       - Semantic alignment, logic structure, and quantifier correctness.
       - Preservation of constraints and boundary assumptions.
       - Accurate typing and use of variables.
       - Syntactic validity and proper Lean usage (free from errors).
       - Use of symbols and constructs without semantic drift.
       - No missing elements, no unjustified additions, and no automatic corrections
        ,→ or completions.

    4. Final Judgement
       Based solely on the above analysis, judge whether the Lean statement is a
        ,→ correct and exact formalization of the mathematical problem.

    5. Accuracy Confirmation
       If correct: clearly confirm why all elements match.
       If incorrect: list all mismatches and explain how each one affects
        ,→ correctness.

    Note: While the analysis may be broad and open to interpreting all relevant
     ,→ features, the final judgment must be based only on what is explicitly and
     ,→ formally expressed in the Lean statement.
    **Do not consider or assess any part of the proof. Your judgment should be
     ,→ entirely about the accuracy of the statement formalization.**

    Output Format:
    Please provide your analysis and conclusion. At the end of your response, clearly
     ,→ state your final judgment using one of these exact phrases:
    - "Final Judgment: Correct" (if the formalization is correct)
    - "Final Judgment: Incorrect" (if the formalization is incorrect)

    You may format your response in any way you prefer (plain text, markdown, etc.),
     ,→ but make sure to include the "Final Judgment: Correct" or "Final Judgment:
     ,→ Incorrect" statement at the end.

    Input Data:
    -- Start of Mathematical_Text --
    {mathematical_statement}
    -- End of Mathematical_Text --

    -- Start of Lean4Code --
    {autoformalization_placeholder}
    -- End of Lean4Code --



B     Error Analysis and Case Study
B.1    Semantic Mismatch in Statement Formalization
In this section, we present some failed cases in statement formalization due to semantic mismatch.




                                                    23
B.1.1   DeepTheorem 665126

   Informal Statement
   Let f : Domain → Range, U be a special function of three variables, and n and k be integers such
   that k ≤ n. If the function λ is defined as:
                          n min(k,n−1)
                          X    X k  (−1)k
                   λ=−                                   f k−c U (−c, k − 2c + 1, −f )ϕ(n, k),
                                           c       k!
                          k=1     c=1

   prove that the order of summation can be switched, and λ can equivalently be expressed as:
                          n                     min(k,n−1) 
                            (−1)k
                                                                 
                          X                        X           k k−c
                   λ=−                ϕ(n, k)                      f U (−c, k − 2c + 1, −f ).
                                 k!                            c
                          k=1                      c=1



   Formal Statement

   theorem sum_rearrangement_proof (n : N) (f : R) (U : Z → Z → R → R)
      (phi : N → N → R) :
     -Σ k in Finset.Icc 1 n, Σ c in Finset.Icc 1 (min k (n - 1)),
       (Nat.choose k c : R) * ((-1 : R) ^ k / (Nat.factorial k : R)) *
       f ^ (k - c) * U (-c) (k - 2 * c + 1) (-f) * phi n k =
     -Σ k in Finset.Icc 1 n,
       ((-1 : R) ^ k / (Nat.factorial k : R)) * phi n k *
       (Σ c in Finset.Icc 1 (min k (n - 1)),
         (Nat.choose k c : R) * f ^ (k - c) * U (-c) (k - 2 * c + 1) (-f))
      := by sorry



In the example above, the model makes a typical error involving natural number subtraction. Although the
expression k − 2c + 1 is expected to be an integer based on the type of U , the subtraction itself is performed
within the domain of natural numbers because k, c ∈ N. Since k − 2c + 1 is not guaranteed to be positive,
this leads to a result that diverges from the intended mathematical logic. In Lean, subtraction on the type
Nat is truncated at zero (i.e., n − m = 0 if m > n), a behavior known as saturating subtraction.

B.1.2   DeepTheorem 618039

   Informal Statement
   Let y : R \ {0} → R be a differentiable function satisfying the nonlinear first-order differential
                          2
                  dy      dy
   equation y + x dx = x4 dx  . Prove that the general solution is given by

                                                         a
                                                   y=      + a2 ,
                                                         x
   where a ∈ R is a constant.




                                                         24
   Formal Statement

   theorem verify_differential_equation_solution (a : R) :
     let y : R → R := fun x => a / x + a^2
     (∀ x : R, x ̸= 0 → DifferentiableAt R y x) ∧
     (∀ x : R, x ̸= 0 → y x + x * (deriv y x) = x^4 * (deriv y x)^2) := by
      sorry



In the example above, the model captures only a portion of the original proposition’s semantics. Specifically,
it verifies that y = xa + a2 is a solution to the differential equation, but fails to establish that all solutions
must take this specific form. In other words, the model proves only the sufficiency of the condition without
addressing its necessity.

B.2    Failed Proof Sketch Analysis
To identify general failure patterns, we utilize Gemini-3-Flash to analyze the failed proof sketches and
summarize the underlying causes. The results are presented in Figure 9, where the errors are classified into
four primary categories:
   • Unreasonable Subgoal Decomposition: The model partitions the proof into subgoals that are logically
     disjointed or involve excessively large logical leaps that hinder formalization.
   • Mathematical Error: The sketch contains fundamental mathematical fallacies or involves subgoals
     that are logically false.
   • Other: Miscellaneous errors that do not fall into the above categories.

                                Failed Proof Sketch Reasons Distribution

                                          1.0%

                                                     19.4%




                                                                     Unreasonable Subgoal Decomposition
                                                                     Mathematical Error
                                                                     Other Reasons




                              79.6%




                 Figure 9 . The failed reasons of the 520 sketches from large-scale benchmark run.

It should be noted that these results provide a general diagnostic trend rather than an absolute metric, given the
potential for LLM hallucinations. As illustrated in Figure 9, Unreasonable Subgoal Decomposition (79.6%)
emerges as the overwhelming failure mode, representing the vast majority of unsuccessful sketches. The
model primarily struggles with orchestrating a coherent and well-founded proof strategy. While such flawed
sketches would be detrimental if naively included in training sets, they could serve as valuable negative
samples for contrastive learning. Additionally, Mathematical Errors (19.4%) point to persistent imprecision
during the informal-to-formal translation process. To gain a more granular understanding of these failure


                                                         25
patterns, we conduct a manual analysis of representative cases in the following section.

B.2.1   DeepMath 53832

   Formal Statement

   theorem count_distinct_terms_expansion :
     ∃ (S : Finset Z),
       (∀ k ∈ S, ∃ (a b c d : N),
         a + b + c + d = 15 ∧
         k = a - b + 2*c - 2*d) ∧
       (∀ k : Z, (∃ (a b c d : N),
         a + b + c + d = 15 ∧
         k = a - b + 2*c - 2*d) → k ∈ S) ∧
       S.card = 61 := by sorry



   Proof Sketch

   theorem count_distinct_terms_expansion :
     ∃ (S : Finset Z),
       (∀ k ∈ S, ∃ (a b c d : N),
         a + b + c + d = 15 ∧
         k = a - b + 2*c - 2*d) ∧
       (∀ k : Z, (∃ (a b c d : N),
         a + b + c + d = 15 ∧
         k = a - b + 2*c - 2*d) → k ∈ S) ∧
       S.card = 61 := by
     -- Define the candidate set S as the interval of integers from -30 to
      30
     let S : Finset Z := Finset.Icc (-30) 30
     use S
     -- Subgoal 1: Show that every k in the set [-30, 30] can be expressed
      in the required form
     have h_achievable : ∀ k ∈ S, ∃ (a b c d : N), a + b + c + d = 15 ∧ k =
      a - b + 2 * c - 2 * d := by sorry
     -- Subgoal 2: Show that any k satisfying the equation must lie in the
      range [-30, 30]
     have h_bounded : ∀ k : Z, (∃ (a b c d : N), a + b + c + d = 15 ∧ k = a
      - b + 2 * c - 2 * d) → k ∈ S := by sorry
     -- Subgoal 3: Prove that the maximum value of the expression is 30
     have h_max_val : (0 : Z) - 0 + 2 * 15 - 2 * 0 = 30 := by sorry
     -- Subgoal 4: Prove that the minimum value of the expression is -30
     have h_min_val : (0 : Z) - 0 + 2 * 0 - 2 * 15 = -30 := by sorry
     -- Subgoal 5: Calculate the cardinality of the integer interval
      Finset.Icc (-30) 30
     have h_card : S.card = 61 := by sorry
     -- Combine the subgoals to complete the proof
     exact ⟨h_achievable, h_bounded, h_card⟩



The aforementioned case serves as a representative example of unreasonable subgoal decomposition. While


                                                    26
the partitioning of the proof into h_achievable, h_bounded, and h_card is logically valid, given that
the formal proposition is structured as a conjunction, it remains practically trivial. Such a decomposition does
not facilitate meaningful mathematical progress. Specifically, although h_achievable and h_bounded
are inherently complex, the generated sketch fails to provide any auxiliary sub-steps to assist in their derivation.
This instance highlights the excessively coarse granularity of the current model’s problem-solving approach.
To address this limitation, we posit that an iterative subgoal decomposition strategy would be more effective
in handling such complex formalization tasks.

B.2.2   DeepMath 9543

   Formal Statement

   theorem count_even_sum_floor_div :
     (Finset.filter (fun m => Even (Σ k in Finset.Icc 1 m, m / k))
      (Finset.Icc 1 1000)).card = 495 := by sorry



   Proof Sketch

   theorem count_even_sum_floor_div :
     (Finset.filter (fun m => Even (Σ k in Finset.Icc 1 m, m / k))
      (Finset.Icc 1 1000)).card = 495 := by
     have h1 : ∀ m ∈ Finset.Icc 1 1000, Σ k in Finset.Icc 1 m, m / k = Σ n
      in Finset.Icc 1 m, (Nat.divisors n).card := by sorry
     have h2 : ∀ n, Odd (Nat.divisors n).card ↔ IsSquare n := by sorry
     have h3 : ∀ m, (Σ n in Finset.Icc 1 m, (Nat.divisors n).card) \% 2 =
      (Finset.filter IsSquare (Finset.Icc 1 m)).card \% 2 := by sorry
     have h4 : ∀ m, (Finset.filter IsSquare (Finset.Icc 1 m)).card =
      Nat.sqrt m := by sorry
     have h5 : ∀ m ∈ Finset.Icc 1 1000, Even (Σ k in Finset.Icc 1 m, m / k)
      ↔ Even (Nat.sqrt m) := by sorry
     have h6 : (Finset.filter (fun m => Even (Nat.sqrt m)) (Finset.Icc 1
      1000)).card = (Finset.filter (fun m => Even (Nat.sqrt m)) (Finset.Icc
      1 1000)).card := by sorry
     have h7 : (Finset.filter (fun m => Even (Nat.sqrt m)) (Finset.Icc 1
      1000)) = (Finset.Icc 1 15).biUnion (fun j => Finset.Icc (4 * j * j)
      (min 1000 (4 * j * j + 4 * j))) := by sorry
     have h8 : ∀ j ∈ Finset.Icc 1 15, (Finset.Icc (4 * j * j) (min 1000 (4 *
       j * j + 4 * j))).card = if j = 15 then 40 else 4 * j + 1 := by sorry
     have h9 : (Finset.filter (fun m => Even (Nat.sqrt m)) (Finset.Icc 1
      1000)).card = (Σ j in Finset.Icc 1 14, (4 * j + 1)) + 40 := by sorry
     have h10 : (Σ j in Finset.Icc 1 14, (4 * j + 1)) + 40 = 4 * (Σ j in
      Finset.Icc 1 14, j) + 14 + 40 := by sorry
     have h11 : Σ j in Finset.Icc 1 14, j = 105 := by sorry
     have h12 : 4 * 105 + 14 + 40 = 495 := by sorry
     rw [Finset.filter_congr h5]
     rw [h9]
     rw [h10]
     rw [h11]
     exact h12




                                                        27
In the aforementioned proof, a manifest mathematical fallacy occurs in h8: when j = 15, the result should be
61 rather than 40. This initial error propagates through several subsequent subgoals, yet the final step, h12,
ostensibly masks these underlying inconsistencies. Our inspection further reveals a significant discrepancy
between the formal proof sketch and the original natural language proof. This mismatch stems partly
from the inherent structural divergence between formal and informal mathematics, and partly from model
hallucinations. Given that the failure of a single subgoal invalidates the entire formal verification, such
hallucinations pose a severe bottleneck to the overall performance of the workflow.
Furthermore, we observed that a subset of failed sketches originates from flawed formal statements. These
errors are attributed either to inherent inaccuracies within the source dataset or to semantic loss during the
statement formalization process. These findings necessitate a more cautious evaluation of the proof sketches
extracted from failed trajectories via the decoupled extraction strategy. Nevertheless, identifying these specific
failure modes provides critical insights for the further optimization of our workflow.


C       Data Example
C.1     Statement Formalization
C.1.1    Example 1

    Informal Statement
    Find the Laplace Transform of the function δ(t − 2π) cos(t), where δ(t) is the Dirac Delta Function.
    Answer: e−2πs


    Premises
    [SchwartzMap.delta, MeasureTheory.Measure.dirac, Real.cos,
    SchwartzMap.integralCLM_dirac_eq_delta]


    Formal Statement

    theorem laplace_transform_delta_cos :
      ∀ s : R, (MeasureTheory.integral (MeasureTheory.Measure.dirac (2 *
       Real.pi))
        (fun t => Real.cos t * Real.exp (-s * t))) =
            Real.exp (-2 * Real.pi * s) := by sorry



C.1.2    Example 2

    Informal Statement
    Let A be an n × n matrix over a field F and b a vector in Fn . Prove that if A is invertible, then the
    linear system Ax = b has a unique solution x in Fn , given by x = A−1 b.




                                                       28
   Premises
   [Matrix.inv, Invertible, Matrix.mulVec.addMonoidHomLeft,
   Matrix.GeneralLinearGroup, Matrix.termGL, Matrix.invertibleOfDetInvertible,
   Matrix.detInvertibleOfInvertible, Matrix.mul_right_inj_of_-
   invertible]


   Formal Statement

   theorem matrix_unique_solution {F : Type*} [Field F] {n : Type*}
      [Fintype n] [DecidableEq n]
     (A : Matrix n n F) (b : n → F) (hA : IsUnit A) :
     (∃! x : n → F, A.mulVec x = b) ∧ (∀ x, A.mulVec x = b ↔ x =
      A−1 .mulVec b) := by sorry



C.2     Proof Generation
C.2.1   Example 1

   Formal Statement

   theorem h_trace_nilpotent (F : Type*) [Field F] (n : N) (hn : 0 < n) (A
      : Matrix (Fin n) (Fin n) F) (h : IsNilpotent A) : IsNilpotent
      (Matrix.trace A) := by sorry



   Premises
   [Matrix.isNilpotent_trace_of_isNilpotent, IsNilpotent]


   Formal Proof

   theorem h_trace_nilpotent (F : Type*) [Field F] (n : N) (hn : 0 < n) (A
      : Matrix (Fin n) (Fin n) F) (h : IsNilpotent A) : IsNilpotent
      (Matrix.trace A) := by
     apply Matrix.isNilpotent_trace_of_isNilpotent h



C.2.2   Example 2

   Formal Statement

   theorem trace_of_nilpotent_matrix (F : Type*) [Field F] (n : N) (hn : 0
      < n) (A : Matrix (Fin n) (Fin n) F)
     (h : IsNilpotent A) : Matrix.trace A = 0 := by sorry




                                      29
Premises
[Matrix.isNilpotent_trace_of_isNilpotent, IsNilpotent]


Formal Proof

theorem h_trace_nilpotent (F : Type*) [Field F] (n : N) (hn : 0 < n) (A
   : Matrix (Fin n) (Fin n) F) (h : IsNilpotent A) : IsNilpotent
   (Matrix.trace A) := by
  apply Matrix.isNilpotent_trace_of_isNilpotent h
theorem h_field_nilpotent_is_zero (F : Type*) [Field F] {x : F} (hx :
   IsNilpotent x) : x = 0 := by
  have h_main : ∀ (n : N), x ^ n = 0 → x = 0 := by
    intro n hn
    by_contra hx'
    -- If x ̸= 0, then x is invertible
    have h : x ̸= 0 := hx'
    -- Since x ̸= 0, we can find its inverse
    have h_inv : ∃ (y : F), x * y = 1 := by
      exact ⟨x−1 , by field_simp [h]⟩
    -- Obtain the inverse y such that x * y = 1
    obtain ⟨y, hy⟩ := h_inv
    -- Compute (x * y)^n = 1^n = 1
    have h1 : (x * y) ^ n = 1 := by
      calc
        (x * y) ^ n = 1 ^ n := by rw [hy]
        _ = 1 := by simp
    -- But x^n = 0, so (x * y)^n = 0 * y^n = 0
    have h2 : (x * y) ^ n = 0 := by
      calc
        (x * y) ^ n = x ^ n * y ^ n := by
           rw [mul_pow]
        _ = 0 * y ^ n := by rw [hn]
        _ = 0 := by simp
    -- Therefore, 1 = 0, which is a contradiction
    have h3 : (1 : F) = 0 := by
      calc
        (1 : F) = (x * y) ^ n := by rw [h1]
        _ = 0 := by rw [h2]
    -- Since 1 ̸= 0 in a field, we have a contradiction
    have h4 : (1 : F) ̸= 0 := by
      exact one_ne_zero
    -- Conclude that x must be 0
    exact h4 h3

  have h_final : x = 0 := by
    obtain ⟨n, hn⟩ := hx
    have h : x = 0 := h_main n hn
    exact h

  exact h_final
set_option maxHeartbeats 0




                                    30
   open BigOperators Real Nat Topology Rat

   theorem trace_of_nilpotent_matrix (F : Type*) [Field F] (n : N) (hn : 0
      < n) (A : Matrix (Fin n) (Fin n) F)
     (h : IsNilpotent A) : Matrix.trace A = 0 := by
     have h_trace_nilpotent : IsNilpotent (Matrix.trace A) := by
       exact h_trace_nilpotent F n hn A h
     have h_field_nilpotent_is_zero {x : F} (hx : IsNilpotent x) : x = 0 :=
      by
       exact h_field_nilpotent_is_zero F hx
     exact h_field_nilpotent_is_zero h_trace_nilpotent



C.3     Premise Selection
C.3.1   Example 1

   Informal Statement
   Determine if there exists a function f (x) such that f (a + b) − f (a) = kab + 3b2 for all real numbers a
   and b, given that f (1) = 3 and f (2) = 10. If such a function exists, find its derivative f ′ (x). Provide
   your answer as an expression for f ′ (x).
   Answer: 6x


   Queries
   [properties of deriv in mathlib, definition of differentiable
   function on real numbers, derivative of a function f at point x]


   Premises
   [deriv, Differentiable]


C.3.2   Example 2

   Formal Statement

   theorem not_cyclic_of_many_elements_of_order_p (G : Type*) [Group G]
      [Fintype G] (p : N) (hp : Nat.Prime p)
     (h : Set.ncard {x : G | orderOf x = p} > p - 1) :
     ¬ IsCyclic G := by sorry



   Queries
   [phi_prime, ncard of set of elements with specific order in cyclic
   group, card_orderOf_eq_totient, number of elements of order d in a



                                                       31
   cyclic group, isCyclic_iff_exists_orderOf_eq_card]


   Premises
   [IsCyclic.card_orderOf_eq_totient, Nat.totient_prime, Prime]


C.4      Proof Correction
C.4.1    Example 1

   Failed Code

   theorem h_map_eval (P : Polynomial Z)
     (h_eval_zero : P.eval 1 = 0) :
     (P.map (algebraMap Z C)).eval 1 = algebraMap Z C (P.eval 1) := by
     -- We want to show that evaluating the mapped polynomial at 1
     -- is the same as mapping the evaluation of the original polynomial at
      1.
     -- This is a general property of polynomial maps and evaluation.
     -- The theorem `Polynomial.eval_map` states: (p.map f).eval (f x) = f
      (p.eval x)
     -- Here, f = algebraMap Z C and x = 1.
     -- Note that (algebraMap Z C) 1 = 1.
     have h_one : (algebraMap Z C) 1 = 1 := by simp
     rw [← h_one, Polynomial.eval_map]



   Error Messages

   Error 1:

   Corresponding Code:
   ```lean4
   theorem h_map_eval (P : Polynomial Z)
     (h_eval_zero : P.eval 1 = 0) :
     (P.map (algebraMap Z C)).eval 1 = algebraMap Z C (P.eval 1) :=
       <error>by
     -- We want to show that evaluating the mapped polynomial at 1
     -- is the same as mapping the evaluation of the original polynomial at
       1.
     -- This is a general property of polynomial maps and evaluation.
     -- The theorem `Polynomial.eval_map` states: (p.map f).eval (f x) = f
       (p.eval x)
     -- Here, f = algebraMap Z C and x = 1.
     -- Note that (algebraMap Z C) 1 = 1.
     have h_one : (algebraMap Z C) 1 = 1 := by simp
     rw [← h_one, Polynomial.eval_map]</error>

   ```




                                      32
   Error Message: unsolved goals
   P : Polynomial Z
   h_eval_zero : Polynomial.eval 1 P = 0
   h_one : (algebraMap Z C) 1 = 1
   ⊢ Polynomial.eval2 (algebraMap Z C) ((algebraMap Z C) 1) P = (algebraMap
      Z C) (Polynomial.eval 1 P)



   Valid Code

   theorem h_map_eval (P : Polynomial Z)
     (h_eval_zero : P.eval 1 = 0) :
     (P.map (algebraMap Z C)).eval 1 = algebraMap Z C (P.eval 1) := by
     -- The core property here is that evaluation of a mapped polynomial at
      f(x)
     -- is the same as applying f to the evaluation of the original
      polynomial at x.
     -- This is stated in the lemma `eval_map`.
     -- Since algebraMap Z C is a ring homomorphism, it preserves 1.
     have h_one : (algebraMap Z C) 1 = 1 := by simp
     rw [← h_one]
     -- Now we can use the theorem: (P.map f).eval (f x) = f (P.eval x)
     -- In mathlib, this is exactly `Polynomial.eval_map` combined with
      some simplification.
     -- Or more directly, `hom_eval` or simply `eval_map`.
     -- Let's check the behavior of eval_map: (p.map f).eval x = p.eval2 f
      x.
     -- There is another identity: eval2 f (f x) p = f (eval x p).
     -- This identity is provided by `Polynomial.eval2 _at_apply`.
     rw [Polynomial.eval_map]
     exact Polynomial.eval2 _at_apply (algebraMap Z C) 1



C.4.2   Example 2

   Failed Code

   theorem h_exp_div_lim : Filter.Tendsto (fun u : R => Real.exp u / u)
      Filter.atTop Filter.atTop := by
     -- We use the theorem tendsto_exp_div_rpow_atTop which states that
     -- exp(x) / x^s tends to +∞ at +∞ for any real s.
     -- Here, our function is exp(u) / u, which is equivalent to exp(u) /
      u^1.
     -- The theorem is available as tendsto_exp_div_rpow_atTop.
     have h := tendsto_exp_div_rpow_atTop 1
     -- Since x^1 = x for x : R, we can use simp to transform the
      expression.
     -- In Lean 4, x^1 is simplified to x for real numbers.
     simp only [pow_one] at h
     exact h




                                      33
   Error Messages

   Error 1:

   Corresponding Code:
   ```lean4
     have h := tendsto_exp_div_rpow_atTop 1
     -- Since x^1 = x for x : R, we can use simp to transform the
       expression.
     -- In Lean 4, x^1 is simplified to x for real numbers.
     simp only [pow_one] at h
     <error>exact h</error>

   ```

   Error Message: type mismatch
     h
   has type
     Filter.Tendsto (fun x => Real.exp x / x ^ 1) Filter.atTop Filter.atTop
       : Prop
   but is expected to have type
     Filter.Tendsto (fun u => Real.exp u / u) Filter.atTop Filter.atTop :
       Prop



   Valid Code

   theorem h_exp_div_lim : Filter.Tendsto (fun u : R => Real.exp u / u)
      Filter.atTop Filter.atTop := by
     -- Use the existing theorem that states exp(x) / x^s tends to +∞ as x
      tends to +∞.
     -- Here s = 1.
     have h := tendsto_exp_div_rpow_atTop 1
     -- In Lean 4, for real numbers x, the expression x ^ (1 : R) is the
      same as x.
     -- The theorem tendsto_exp_div_rpow_atTop uses the real power function
      (rpow).
     -- We use Real.rpow_one to simplify x^1 to x.
     simp only [Real.rpow_one] at h
     exact h



C.5      Proof Sketching
C.5.1    Example 1

   Formal Statement

   theorem polynomial_symmetric_odd_coefficients_has_unit_root (n : N) (P :
      Polynomial Z)
     (h_degree : P.natDegree = n)



                                      34
  (h_symm : ∀ i : N, i ≤ n → P.coeff i = -(P.coeff (n - i)))
  (h_odd : ∀ i : N, i ≤ n → Odd (P.coeff i)) :
  ∃ z : C, Complex.abs z = 1 ∧ (P.map (algebraMap Z C)).eval z = 0 := by
   sorry



Informal Proof
1. Let P (x) = ni=0 ai xi be a polynomial with integer coefficients where ai denotes the coefficient
                 P
of xi (given by P.coef f (i)).
2. We are given that n is the natural degree of P , so an ̸= 0.
3. We are given the symmetry condition: for all i ∈ {0, . . . , n}, ai = −an−i .
4. We are given the parity condition: for all i ∈ {0, . . . , n}, ai is an odd integer.
5. Consider the symmetry condition specifically for the "middle" coefficient when n is even. If n = 2k
for some integer k , then for i = k , we have ak = −an−k = −a2k−k = −ak .
6. This implies 2ak = 0, so ak = 0.
7. However, the parity condition states that ak must be an odd integer. By the theorem ‘Int.not_odd_-
zero‘, 0 is not odd.
8. Thus, the assumption that n is even leads to a contradiction. Therefore, n must be an odd natural
number.
9. Now, let’s evaluate the polynomial P at x = 1. By theP        theorem ‘Polynomial.eval_eq_sum‘, the
evaluation of P at 1 is the sum of its coefficients: P (1) = ni=0 ai .
10. Using the symmetry condition ai = −an−i , we can rewrite the sum: P (1) = ni=0 (−an−i ).
                                                                                        P
11. By performing     a change of indices j = n − i, as i goes from 0 to n, j also goes from 0 to n:
P (1) = − nj=0 aj .
            P

12. This shows that P (1) = −P (1), which implies 2P (1) = 0, and thus P (1) = 0 in the ring of
integers Z.
13. Now, we map the polynomial P from Z[X] to C[X] using the canonical homomorphism ‘alge-
braMap Z C‘. Let PC = P.map(algebraM apZC).
14. Evaluation is preserved under the ring homomorphism, so PC (1) = (P (1))C = 0C = 0.
15. We are looking for a complex number z such that |z| = 1 and PC (z) = 0.
16. Let z = 1. The complex absolute value of 1 is |1| = 1.
17. As shown in step 14, PC (1) = 0.
18. Thus, z = 1 is a root of the polynomial PC with |z| = 1.
19. This concludes the proof that there exists a z ∈ C such that |z| = 1 and PC (z) = 0.


Premises
[Polynomial.eval_eq_sum, Int.not_odd_zero, Polynomial.sum,
Polynomial.sum_monomial_eq, Polynomial.eval_sum, Polynomial.eval2 _-
eq_sum]


Proof Sketch

theorem polynomial_symmetric_odd_coefficients_has_unit_root (n : N) (P :
   Polynomial Z)
  (h_degree : P.natDegree = n)




                                                 35
        (h_symm : ∀ i : N, i ≤ n → P.coeff i = -(P.coeff (n - i)))
        (h_odd : ∀ i : N, i ≤ n → Odd (P.coeff i)) :
        ∃ z : C, Complex.abs z = 1 ∧ (P.map (algebraMap Z C)).eval z = 0 := by
        have h_eval_sum : P.eval 1 = Σ i in Finset.range (n + 1), P.coeff i :=
         by sorry
        have h_symm_sum : Σ i in Finset.range (n + 1), P.coeff i = Σ i in
         Finset.range (n + 1), -P.coeff (n - i) := by sorry
        have h_neg_sum : Σ i in Finset.range (n + 1), -P.coeff (n - i) = - Σ i
         in Finset.range (n + 1), P.coeff (n - i) := by sorry
        have h_reindex : Σ i in Finset.range (n + 1), P.coeff (n - i) = Σ i in
         Finset.range (n + 1), P.coeff i := by sorry
        have h_eval_eq_neg_eval : P.eval 1 = -P.eval 1 := by sorry
        have h_eval_zero : P.eval 1 = 0 := by sorry
        have h_map_eval : (P.map (algebraMap Z C)).eval 1 = algebraMap Z C
         (P.eval 1) := by sorry
        have h_map_eval_zero : (P.map (algebraMap Z C)).eval 1 = 0 := by sorry
        have h_abs_one : Complex.abs 1 = 1 := by sorry
        refine ⟨1, h_abs_one, h_map_eval_zero⟩



C.5.2    Example 2

   Formal Statement

   theorem minimize_expression_with_sqrt_constraint :
     (∃ x y : R, 0 < x ∧ x < 2 ∧ y > 0 ∧
       (x - y)^2 + (Real.sqrt (4 - x^2) - 16 / y)^2 = 36 - 16 * Real.sqrt
      2) ∧
     (∀ x y : R, 0 < x ∧ x < 2 ∧ y > 0 →
       (x - y)^2 + (Real.sqrt (4 - x^2) - 16 / y)^2 ≥ 36 - 16 * Real.sqrt
      2) := by sorry



  Informal Proof
                   √                                             √                           √
  1. Let P1 = (x, 4 − x2 ) where 0 < x < 2. Since x2 + ( 4 − x2 )2 = 4 and x > 0, 4 − x2 > 0,
  P1 is a point on the arc of the circle x2 + y 2 = 4 in the first quadrant.
  2. Let P2 = (y, 16                              16
                    y ) where y > 0. Since y · y = 16, P2 is a point on the branch of the hyperbola
  xy = 16 in the first quadrant. √
  3. The expression (x − y)2 + ( 4 − x2 − 16/y)2 is the square of the Euclidean distance between P1
  and P2 , denoted d(P1 , P2 )2 .
  4. Both the circle x2 + y 2 = 4 and the hyperbola xy = 16 are symmetric with respect to the line
  L : y = x. √ √                   √         √ 2
  5. Let P1∗ =√( 2, 2). Since ( 2)2 + ( 2)√         = 2 + 2 = 4, P1∗ is on the circle. This corresponds to
  setting x = 2 in the expression. Note 0 < 2 < 2.
  6. Let P2∗ = (4, 4). Since 4 · 4 = 16, P2∗ is on the hyperbola. This corresponds to setting y = 4 in the
  expression. Note 4 > 0.                                             √         √              √
                                                         ∗   ∗ 2             2          2             2
  7. Calculate
          √ the squared distance                  √d(P1 , P2 ) = ( 2−4) +( 2−4) = 2( 2−4) =
                                  √ at these points:
  2(2 − 8 √2 + 16) = 2(18 − 8 2) = 36 − 16 2. This proves the first part of the theorem: the value
  36 − 16 2 is attained.



                                                    36
8. To show this is the minimum, we use the property that the minimum distance between two convex
sets (or smooth curves) is realized along a common normal.                                      √ √
9. For the√circle√g1 (x, y) = x2 + y 2 − 4 = 0, the gradient is ∇g1 = (2x, 2y). At P1∗ = ( 2, 2),
∇g1 = (2 2, 2 2), which is parallel to the vector (1, 1). Thus the normal line to the circle at P1∗ is
the line y = x.
10. For the hyperbola g2 (x, y) = xy − 16 = 0, the gradient is ∇g2 = (y, x). At P2∗ = (4, 4),
∇g2 = (4, 4), which is also parallel to the vector (1, 1). Thus the normal line to the hyperbola at P2∗
is also the line y = x.
11. The points P1∗ and P2∗ both lie on the line y = x, and their normals√ are aligned along this line.
12. Consider the tangent line to the circle at P1∗ , which
                                                        √   is x + y = 2  2. Since the circle is centered
at the origin, the circle lies in the region x + y ≤ 2 2 (specifically, the part of the circle in the first
quadrant).
13. Consider the tangent line to the hyperbola at P2∗ , which is x + y = 8. Because xy = 16 is a convex
function in the first quadrant, the hyperbola lies in the region x + y ≥ 8.
14. For any point P1 on the circle and P2 on the hyperbola in        √ the first quadrant: d(P1 ,√P2 ) ≥
dist(P1 , Line x + y = 8) + dist(Line x + y = 8, Line x + y = 2 2) + dist(Line x + y = 2 2, P2 )
is not quite right, but we can use the projection onto the line y = x.
15. Let u = √12 (1, 1) be the unit vector along y = x. For any P1 = (x1 , y1 ) on the circle arc,
the projection onto u is P1 · u = x1√+y2
                                         1
                                           . Since x21 + y12 = 4 and x1 , y1 > 0, by Cauchy-Schwarz,
            √         p             √           √
x1 + y1 ≤ 12 + 12 x21 + y12 = 2 · 2 = 2 2. Thus P1 · u ≤ 2.
16. For any P2 = (x2 , y2 ) on the hyperbola branch, the projection onto u is P2 · u = x2√+y
                                                                                           2
                                                                                             2
                                                                                               . Since
                                                       √          √                        8
                                                                                                   √
x2 y2 = 16 and x2 , y2 > 0, by AM-GM, x2 + y2 ≥ 2 x2 y2 = 2 16 = 8. Thus P2 · u ≥ √2 = 4 2.
17. The distance d(P1 , P2 ) is at least the distance
                                                  √ between their projections on the line y = x:
d(P1 , P2 ) = ∥P1 − P2 ∥ ≥ |P2 · u − P1 · √ u| ≥ 4 2 − 2.       √                  √
18. Squaring both sides: d(P1 , P2 )2 ≥ (4 2 − 2)2 = 32 − 16 2√+ 4 = 36 − 16 2.                  √
19. This confirms that for all 0 < x < 2 and y > 0, (x − y)2 + ( 4 − x2 − 16/y)2 ≥ 36 − 16 2.


Premises
[EuclideanSpace.dist_eq, Euclidean.dist, real_inner_le_norm’,
isLocalMin_of_deriv_Ioo, norm_inner_le_norm, abs_real_inner_le_-
norm, InnerProductSpace.Core.norm_inner_le_norm, isLocalMin_of_-
deriv’, inner_mul_inner_self_le]


Proof Sketch

theorem minimize_expression_with_sqrt_constraint :
  (∃ x y : R, 0 < x ∧ x < 2 ∧ y > 0 ∧
    (x - y)^2 + (Real.sqrt (4 - x^2) - 16 / y)^2 = 36 - 16 * Real.sqrt
   2) ∧
  (∀ x y : R, 0 < x ∧ x < 2 ∧ y > 0 →
    (x - y)^2 + (Real.sqrt (4 - x^2) - 16 / y)^2 ≥ 36 - 16 * Real.sqrt
   2) := by
  have h_exists : ∃ x y : R, 0 < x ∧ x < 2 ∧ y > 0 ∧ (x - y)^2 +
   (Real.sqrt (4 - x^2) - 16 / y)^2 = 36 - 16 * Real.sqrt 2 := by
    have h_val_x : Real.sqrt 2 > 0 ∧ Real.sqrt 2 < 2 := by sorry
    have h_val_y : (4 : R) > 0 := by sorry



                                                    37
  have h_calc : (Real.sqrt 2 - 4)^2 + (Real.sqrt (4 - (Real.sqrt 2)^2)
 - 16 / 4)^2 = 36 - 16 * Real.sqrt 2 := by sorry
  exact ⟨Real.sqrt 2, 4, h_val_x.1, h_val_x.2, h_val_y, h_calc⟩
have h_min : ∀ x y : R, 0 < x ∧ x < 2 ∧ y > 0 → (x - y)^2 +
 (Real.sqrt (4 - x^2) - 16 / y)^2 ≥ 36 - 16 * Real.sqrt 2 := by
  intro x y h
  have hx_low : 0 < x := by sorry
  have hx_high : x < 2 := by sorry
  have hy_pos : y > 0 := by sorry
  let P1 : R × R := (x, Real.sqrt (4 - x^2))
  let P2 : R × R := (y, 16 / y)
  have h_dist_sq : (x - y)^2 + (Real.sqrt (4 - x^2) - 16 / y)^2 =
 (P2.1 - P1.1)^2 + (P2.2 - P1.2)^2 := by sorry
  have h_unit_vec : (P2.1 - P1.1)^2 + (P2.2 - P1.2)^2 ≥ (1/2 : R) *
 ((P2.1 + P2.2) - (P1.1 + P1.2))^2 := by sorry
  have h_circle_bound : x + Real.sqrt (4 - x^2) ≤ 2 * Real.sqrt 2 :=
 by sorry
  have h_hyperbola_bound : y + 16 / y ≥ 8 := by sorry
  have h_diff_bound : (y + 16 / y) - (x + Real.sqrt (4 - x^2)) ≥ 8 - 2
 * Real.sqrt 2 := by sorry
  have h_sq_bound : (1/2 : R) * ((y + 16 / y) - (x + Real.sqrt (4 -
 x^2)))^2 ≥ (1/2 : R) * (8 - 2 * Real.sqrt 2)^2 := by sorry
  have h_final_calc : (1/2 : R) * (8 - 2 * Real.sqrt 2)^2 = 36 - 16 *
 Real.sqrt 2 := by sorry
  calc (x - y)^2 + (Real.sqrt (4 - x^2) - 16 / y)^2
    _ = (P2.1 - P1.1)^2 + (P2.2 - P1.2)^2 := h_dist_sq
    _ ≥ (1/2) * ((P2.1 + P2.2) - (P1.1 + P1.2))^2 := h_unit_vec
    _ ≥ 36 - 16 * Real.sqrt 2 := by sorry
exact ⟨h_exists, h_min⟩




                                 38
