                                            Evaluating the Architectural Reasoning Capabilities of LLM Provers via the
                                                               Obfuscated Natural Number Game
                                                                                                           Lixing Li
                                                                               St Anne’s College, Oxford, OX26HS, United Kingdom
                                                                                            lixing.li@st-annes.ox.ac.uk



                                                                   Abstract                                      fails to evaluate a model’s capacity for true logical synthe-
arXiv:2605.00677v1 [cs.LG] 1 May 2026




                                                                                                                 sis in novel or unexplored mathematical domains where no
                                          While Large Language Models have achieved notable suc-                 such library exists.
                                          cess on formal mathematics benchmarks such as MiniF2F,                    Recent research in general software engineering has be-
                                          it remains unclear whether these results stem from genuine
                                          logical reasoning or semantic pattern matching against pre-
                                                                                                                 gun to uncover the fragility of these models. For instance, a
                                          training data. This paper identifies Architectural Reason-             study on the LiveCodeBench benchmark demonstrated that
                                          ing—the ability to synthesize formal proofs using exclusively          ”semantics-preserving perturbations”—such as variable re-
                                          local axioms and definitions within an alien math domain—as            naming or identifier obfuscation—measurably degrade code
                                          the necessary ability for future automated theorem discov-             generation performance (Ma et al. 2025).
                                          ery AI. We use the Obfuscated Natural Number Game, a                      This phenomenon suggests that LLMs are highly re-
                                          benchmark to evaluate Architectural Reasoning. By renam-               liant upon the semantic cues provided by human-readable
                                          ing identifiers in the Natural Number Game in Lean 4, we               names rather than the underlying structural logic. Despite
                                          created a zero-knowledge, closed environment. We evaluate              these findings in general programming, the extent of this
                                          state-of-the-art models, finding a universal latency tax where         semantic-reasoning gap in formal deductive logic remains
                                          obfuscation increases inference time. The results also reveal
                                          a divergence in robustness: while general models (Claude-
                                                                                                                 largely unquantified.
                                          Sonnet-4.5, GPT-4o) suffer performance degradation, rea-
                                          soning models (DeepSeek-R1, GPT-5, DeepSeek-Prover-V2)                 Motivation: Testing Architectural Reasoning
                                          maintain the same accuracy despite the absence of semantic             To achieve the automated discovery of novel mathematical
                                          cues. These findings provide a quantitative metric for assess-         theorems, AI must possess the ability to reason within en-
                                          ing the true capacity for mathematical reasoning.                      tirely unfamiliar mathematical structures. In such alien do-
                                                                                                                 mains, semantic identifiers and libraries are absent, leaving
                                        Code — https://github.com/lllx125/Obfuscated-NNG                         pure structural logic as the only path to a solution. We iden-
                                                                                                                 tify this capability as Architectural Reasoning. This paper
                                                                                                                 aims to test such ability in SOTA LLMs.
                                                               Introduction                                         We define Architectural Reasoning as the ability to syn-
                                        The integration of LLMs with interactive theorem provers                 thesize formal proofs using exclusively local definitions, ax-
                                        such as Lean 4 has facilitated progress in automated theo-               ioms, theorems, and limited tactics within a closed theory.
                                        rem proving (de Moura and Ullrich 2021). State-of-the-art                This capability is characterized by three specific exclusions.
                                        (SOTA) LLM provers such as DeepSeek-Prover-V2 have                       First, it requires independence from semantic knowledge,
                                        achieved notable results on benchmarks such as MiniF2F                   meaning the system cannot utilize the semantic meaning of
                                        and PutnamBench, often reaching success rates that rival                 identifiers (e.g., add, succ) to infer mathematical proper-
                                        high-school Olympiad medalists and undergraduate math-                   ties. Second, it necessitates independence from external li-
                                        ematics students (Ren et al. 2025; Zheng, Han, and Polu                  braries, avoiding reliance on pre-existing repositories like
                                        2022; Tsoukalas et al. 2024). However, a critical question re-           Mathlib (The mathlib Community 2020). Finally, it excludes
                                        mains: are these models demonstrating genuine logical rea-               the use of high-level automated tactics (e.g., linarith,
                                        soning, or are they performing sophisticated pattern match-              simp) that encapsulate complex decision procedures, fo-
                                        ing against their training dataset?                                      cusing instead on fundamental manipulations such as rw
                                           Modern benchmarks primarily emphasize library re-                     (rewrite) and induction.
                                        trieval. A correct proof often relies on the model’s ability to             The Natural Number Game (NNG) serves as the basis
                                        identify and retrieve the correct high-level lemma to prove              for our benchmark (Buzzard and Eugster 2023) because
                                        a goal. While retrieval is efficient for existing knowledge, it          it provides a suitable experimental framework for evaluat-
                                                                                                                 ing Architectural Reasoning. Unlike other benchmarks that
                                        Copyright © 2026, Association for the Advancement of Artificial          rely heavily on Mathlib, the NNG represents a closed the-
                                        Intelligence (www.aaai.org). All rights reserved.                        ory where every mathematical theorem is derived from the
ground up using Peano axioms. This structure addresses the        with probability P using valid Unicode/ASCII candidates.
condition of independence from external libraries. Addition-      Second, insertion injects new characters with probability
ally, since definitions and previously proven theorems are        0.4P . Finally, deletion removes characters with probability
concise, the complete local state fits within a standard LLM      0.3P , subject to a constraint ensuring identifiers remain non-
context window, ensuring the model can prove the next the-        empty. These insertion and deletion ratios were calibrated to
orem based on all previous knowledge. Furthermore, the            ensure that the resulting strings maintain a length distribu-
NNG is designed to be solved using a restricted set of fun-       tion similar to the original identifiers.
damental tactics, preventing the model from using high-level
automation such as ring.                                          Experimental Pipeline and Setup
   The Obfuscated Natural Number Game (O-NNG) re-                 The evaluation framework follows a structured six-stage
places identifier names with random strings. This process re-     pipeline. The process begins with Parsing, where the NNG
moves semantic cues from the dataset, preventing the model        is extracted into a structured format while maintaining strict
from using previous knowledge of NNG and related mathe-           dependency order. This is followed by Obfuscation, in-
matics. Consequently, the model must rely solely on the log-      volving the generation of multiple datasets by applying
ical structure to construct its proof. By benchmarking LLMs       character-level perturbations to identifiers based on λ. The
on the O-NNG and NNG, this paper aims to quantify the             third stage, Query Generation, constructs prompts contain-
performance tax imposed by the removal of semantic identi-        ing the ”alien” axiomatic definitions, target theorems, previ-
fiers, thereby providing a more rigorous measure of the Ar-       ous theorems, and a set of available tactics. The output for-
chitectural Reasoning capabilities of current LLM provers.        mat is constrained to a specific JSON schema while encour-
   While current agents often rely on retrieving semantic         aging chain-of-thought reasoning. The pipeline proceeds to
patterns from large knowledge bases, robust semantic un-          Benchmarking, which involves iterative querying of LLMs
derstanding requires the ability to manipulate formal knowl-      to generate formal Lean 4 proofs. These proofs undergo Ver-
edge structures even when surface-level lexical cues are ab-      ification via automated validation using the Lean 4 compiler
sent. By isolating structural reasoning from lexical retrieval,   (version v4.27.0) to detect syntax and logic errors. Fi-
our benchmark assesses the agent’s capacity to ground its         nally, Analysis is performed through statistical evaluation of
reasoning in the explicit logical architecture of the domain      success rates, timing data, and proof plan length across all
rather than probabilistic associations.                           experimental runs.
                                                                  O-NNG Dataset The benchmark is derived from the Nat-
                      Methodology                                 ural Number Game and comprises 68 formal problems. The
To evaluate Architectural Reasoning, we designed a pipeline       problems are organized into eight modules: Addition, Im-
that transforms standard mathematical problems into a             plication, Algorithm, Multiplication, Power, Advanced Ad-
semantics-free environment. This section details the obfus-       dition, Less-Than-or-Equal, and Advanced Multiplication.
cation algorithm and the experimental setups.                     The original benchmark (λ = 0) is the NNG and the ob-
                                                                  fuscated ones (λ > 0) comprise the O-NNG datasets.
Obfuscation Algorithm
                                                                  LLM Models Due to computational resource constraints,
The core of our experiment involves the construction of           all evaluations were conducted via API calls. Consequently,
an obfuscated benchmark. To achieve this, a Noise Level           models requiring high-performance computing clusters,
λ ∈ [0, 1] is defined. An exponential relationship is estab-      such as Goedel-Prover-v2, were excluded (Lin et al. 2025).
lished between noise level λ and the actual probability P of      The study evaluates five specific models categorized by their
a character-level perturbation:                                   primary architecture or training focus. We assess reasoning
                          P = λ2.5                         (1)    models, specifically DeepSeek-R1 and GPT-5 (Guo et al.
                                                                  2025; OpenAI 2025), alongside general-purpose models in-
This exponential mapping was selected to increase the den-        cluding GPT-4o and Claude-Sonnet-4.5 (OpenAI 2024; An-
sity of sampling in a lower noise spectrum, thus captur-          thropic 2025). Additionally, we include DeepSeek-Prover-
ing the non-linear degradation of model performance as the        V2 (Ren et al. 2025), which serves as a specialized math-
recognition of identifiers drops more in low-magnitude noise      specific model that also exhibits reasoning capabilities.
(Arbuzov, Shvets, and Beir 2025).
                                                                  Output Structure To facilitate automated verification,
   The methodology was evaluated in six discrete intervals:
                                                                  LLMs were prompted to return a JSON object containing
λ ∈ {0, 0.2, 0.4, 0.6, 0.8, 1.0}, where λ = 0 corresponds
                                                                  two specific fields: a ”Draft” field containing a natural lan-
to the original Natural Number Game (NNG) and λ = 1.0
                                                                  guage proof plan, and a ”Code” field containing the formal
represents complete randomized identifiers.
                                                                  Lean 4 code block, which is passed directly to the Lean com-
   A character-level transformation was performed using
                                                                  piler for evaluation.
the nlpaug framework, targeting every definition, opera-
tor, axiom, and theorem (Ma 2019). The obfuscation pro-           Experimental Parameters The experimental design in-
cess utilizes a RandomCharAug augmenter with a speci-             corporates specific parameters to ensure robustness. Eval-
fied character pool (ASCII and valid Lean-allowed Unicode)        uations span six discrete noise levels. To mitigate stochastic
to ensure syntactic validity. Three primary operations are        variance, each model was queried five times per theorem at
applied in sequence. First, substitution replaces characters      every noise level.
                                     GPT-4o                                  Claude-Sonnet-4.5                               DeepSeek-R1                                        GPT-5                                  DeepSeek-Prover-V2
                   100                                           100                                           100                                           100                                           100


                    80                                            80                                            80                                            80                                            80
Correct Rate (%)




                    60                                            60                                            60                                            60                                            60


                    40                                            40                                            40                                            40                                            40


                    20                                            20                                            20                                            20                                            20


                     0                                             0                                             0                                             0                                             0
                         0.0   0.2   0.4       0.6   0.8   1.0         0.0   0.2   0.4       0.6   0.8   1.0         0.0   0.2   0.4       0.6   0.8   1.0         0.0   0.2   0.4       0.6   0.8   1.0         0.0    0.2   0.4       0.6   0.8   1.0

                   200                                           200                                           200                                           200                                           200

                   175                                           175                                           175                                           175                                           175
Average Time (s)




                   150                                           150                                           150                                           150                                           150

                   125                                           125                                           125                                           125                                           125

                   100                                           100                                           100                                           100                                           100

                    75                                            75                                            75                                            75                                            75

                    50                                            50                                            50                                            50                                            50

                    25                                            25                                            25                                            25                                            25

                     0                                             0                                             0                                             0                                             0
                         0.0   0.2   0.4       0.6   0.8   1.0         0.0   0.2   0.4       0.6   0.8   1.0         0.0   0.2   0.4       0.6   0.8   1.0         0.0   0.2   0.4       0.6   0.8   1.0         0.0    0.2   0.4       0.6   0.8   1.0
                                           λ                                             λ                                             λ                                             λ                                              λ



Figure 1: LLM performance metrics across varying noise levels λ. The plots illustrate Correct Rate (%) and Average Time (s)
for GPT-4o, Claude-Sonnet-4.5, DeepSeek-R1, GPT-5, and DeepSeek-Prover-V2. Error bars represent standard deviation over
5 independent runs.


                    Model                       Correct Rate      Average Time                                                             Robustness of Reasoning Models
                    GPT-4o                          0.0242*         0.0004*
                    Claude-Sonnet-4.5               0.0001*         0.0000*                                                                We observe a clear distinction in the performance of dif-
                    DeepSeek-R1                     0.1573          0.0000*                                                                ferent types of models. The reasoning models, specifi-
                    GPT-5                            0.0863         0.0001*                                                                cally DeepSeek-R1 and GPT-5, demonstrated resilience; the
                    DeepSeek-Prover-V2               0.3077         0.0000*                                                                degradation in correct rate was not statistically significant.
                    * Indicates statistical significance (p < 0.05)                                                                        This suggests their Architectural Reasoning capabilities al-
                                                                                                                                           low them to navigate Peano axioms without semantic an-
Table 1: One-Way ANOVA p-values for LLM Performance                                                                                        chors. Similarly, DeepSeek-Prover-V2, which is also based
Metrics across Correct Rate, Average Time.                                                                                                 on a reasoning architecture, maintained its performance con-
                                                                                                                                           sistency across all noise levels. In contrast, the general mod-
                                                                                                                                           els, Claude-Sonnet-4.5 and GPT-4o, both exhibited a statis-
                                               Results and Analysis                                                                        tically significant drop in success rates for λ > 0. This im-
We utilize two primary metrics to quantify model perfor-                                                                                   plies that their performances on standard formal logic tasks
mance. Correct Rate (%) is defined as the ratio of the num-                                                                                rely on semantic pattern matching rather than pure structural
ber of correct problems to the total number of problems (68                                                                                reasoning.
in total). Average Time (s) represents the duration between
the transmission of the query and the receipt of the response                                                                                                                        Discussion
from the LLM.                                                                                                                              The following section evaluates the core limitations of our
                                                                                                                                           experimental framework, proposes future research direc-
Significance Test                                                                                                                          tions, and explores the broader implications of Architectural
The statistical analysis reveals consistent behavioral pat-                                                                                Reasoning.
terns across the evaluated models. As indicated in Table 1,
all models experienced a statistically significant increase in                                                                             Limitations and Foundational Weaknesses
response time. Regarding accuracy, a divergence was ob-                                                                                    A primary limitation of the O-NNG is that while it removes
served: reasoning models achieved similar scores across all                                                                                semantic labels, it preserves the underlying logical struc-
benchmarks, whereas general models experienced a statisti-                                                                                 ture of Peano arithmetic. Frontier models may possess the
cally significant score drop on the O-NNG compared to the                                                                                  heuristic capacity to recognize this structural isomorphism
NNG.                                                                                                                                       and internally map the ”alien” domain back to known math-
                                                                                                                                           ematical concepts, potentially bypassing the intended rea-
The Universal Latency Tax                                                                                                                  soning requirement. However, in our experiment, no LLM
As illustrated in Table 1, every model tested exhibited a sta-                                                                             attempted to map the obfuscated terms back to their origi-
tistically significant increase in average solving time for O-                                                                             nal NNG meaning or explicitly referenced Peano theory. A
NNG compared to NNG. This universal slowdown suggests                                                                                      more rigorous test would require the synthesis of entirely
that removing semantic identifiers necessitates a more in-                                                                                 novel, non-standard axiomatic domains. Additionally, this
tensive search or a complex internal reconstruction of the                                                                                 study evaluated five frontier models across 68 problems fo-
logical context, affecting the model’s processing efficiency                                                                               cused exclusively on natural numbers. While these models
regardless of its base performance.                                                                                                        represent the current state-of-the-art, the findings may not
generalize to mid-sized open-source models or to broader          Arbuzov, M. L.; Shvets, A. A.; and Beir, S. 2025. Be-
mathematical domains such as abstract algebra or topology.        yond Exponential Decay: Rethinking Error Accumulation in
                                                                  Large Language Models. arXiv:2505.24187.
Future Research Directions                                        Buzzard, K.; and Eugster, J. 2023. Natural Number Game
Our data suggests a non-linear relationship where partial         4. https://github.com/leanprover-community/NNG4. Ac-
noise occasionally degrades performance more than total           cessed: 2026-01-20. Commit: d593c1e.
obfuscation. This points to a ”Reasoning Uncanny Valley,”         de Moura, L.; and Ullrich, S. 2021. The Lean 4 Theo-
where residual semantic cues act as distracting heuristics        rem Prover and Programming Language. In Proceedings of
that interfere with structural reasoning rather than aiding it.   the 28th International Conference on Automated Deduction
Future research should investigate whether increased noise        (CADE-28), 625–635. Berlin, Heidelberg: Springer-Verlag.
consistently mitigates hallucination derived from familiar        Guo, D.; Yang, D.; Zhang, H.; Song, J.; Wang, P.; Zhu, Q.;
naming conventions. Furthermore, a critical next step is          Xu, R.; Zhang, R.; Ma, S.; Bi, X.; et al. 2025. DeepSeek-
evaluating model performance in an interactive environment        R1 Incentivizes Reasoning in LLMs through Reinforcement
where the Lean compiler provides real-time error feedback.        Learning. Nature, 645(8081): 633–638.
This would determine if the ”latency tax” observed in this        Lin, Y.; Tang, S.; Lyu, B.; Yang, Z.; Chung, J.-H.;
study can be mitigated by iterative self-correction within an     Zhao, H.; Jiang, L.; Geng, Y.; Ge, J.; Sun, J.; et al.
unfamiliar axiomatic framework.                                   2025. Goedel-Prover-V2: Scaling Formal Theorem Prov-
                                                                  ing with Scaffolded Data Synthesis and Self-Correction.
Broader Implications                                              arXiv:2508.03613.
We advocate for a shift toward Architectural Reasoning            Ma, E. 2019. NLP Augmentation. https://github.com/
benchmarks that decouple structural logic from concep-            makcedward/nlpaug. Accessed: 2026-01-20.
tual labels. While this study represents a preliminary ex-        Ma, L.; Liu, S.; Bu, L.; Li, S.; Wang, Y.; and Liu,
ploration, it provides a template for zero-knowledge test-        Y. 2025.     SpecEval: Evaluating Code Comprehension
ing environments essential for the automated discovery of         in Large Language Models via Program Specifications.
novel mathematics. The performance divergence observed            arXiv:2409.12866.
reinforces the necessity for the AI4Math community to pri-
oritize reasoning-focused architectures (e.g., DeepSeek-R1,       OpenAI. 2024. GPT-4o Technical Report. https://openai.
GPT-5) over general-purpose models. Finally, the universal        com/index/hello-gpt-4o/. Accessed: 2026-01-20.
latency observed implies that genuine Architectural Reason-       OpenAI. 2025. GPT-5 Technical Report. https://arxiv.org/
ing is not computationally free; the internal reconstruction of   abs/2511.16072. Accessed: 2026-01-20.
an unknown logical context appears to require an intensive        Ren, Z. Z.; Shao, Z.; Song, J.; Xin, H.; Wang, H.; Zhao,
search process that correlates directly with increased infer-     W.; Zhang, L.; Fu, Z.; Zhu, Q. g.; Yang, D.; et al.
ence time.                                                        2025. DeepSeek-Prover-V2: Advancing Formal Mathemat-
                                                                  ical Reasoning via Reinforcement Learning for Subgoal De-
                       Conclusion                                 composition. arXiv:2504.21801.
This paper defines Architectural Reasoning as a critical ca-      The mathlib Community. 2020. The Lean Mathematical Li-
pability for AI systems aiming to discover new theorems           brary. In Proceedings of the 9th ACM SIGPLAN Interna-
and introduces the Obfuscated Natural Number Game (O-             tional Conference on Certified Programs and Proofs (CPP
NNG) to evaluate this capacity. Our results demonstrate a         2020), 367–381. New Orleans, La.: ACM.
clear divergence in model behavior: while all models incur a      Tsoukalas, G.; Lee, J.; Jennings, J.; Xin, J.; Ding, M.; Jen-
measurable latency tax when navigating alien domains, rea-        nings, M.; Thakur, A.; and Chaudhuri, S. 2024. Putnam-
soning models exhibit distinct structural robustness. In con-     Bench: Evaluating Neural Theorem-Provers on the Putnam
trast, general models show a statistically significant perfor-    Mathematical Competition. In Advances in Neural Informa-
mance degradation, suggesting a reliance on semantic pat-         tion Processing Systems 37 (NeurIPS 2024), 12450–12465.
tern matching rather than pure logical synthesis. These find-     Red Hook, N.Y.: Curran Associates, Inc.
ings are particularly relevant for the design of Knowledge-       Zheng, K.; Han, J. M.; and Polu, S. 2022. MiniF2F: A Cross-
Grounded Semantic Agents, which must operate reliably             System Benchmark for Formal Olympiad-Level Mathemat-
even when the semantic ontology of a domain is incom-             ics. In Proceedings of the Tenth International Conference
plete or obscured. By quantifying this ”Semantic-Reasoning        on Learning Representations (ICLR 2022), 1–18. Appleton,
Gap,” O-NNG provides a rigorous framework for assessing           Wis.: OpenReview.net.
whether LLMs possess the foundational capacity to reason
independent of lexical priors.

                        References
Anthropic. 2025. Claude 4.5 Technical Overview. https:
//www.anthropic.com/claude-sonnet-4-5-system-card. Ac-
cessed: 2026-01-20.
