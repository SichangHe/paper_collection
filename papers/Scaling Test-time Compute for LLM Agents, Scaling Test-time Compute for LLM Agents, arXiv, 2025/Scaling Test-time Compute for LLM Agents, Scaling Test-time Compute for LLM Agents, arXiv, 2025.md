                                                                                                                                            M-A-P



                                                     Scaling Test-time Compute for LLM Agents


                                                                                    OPPO AI Agent Team




                                                                                          Abstract
arXiv:2506.12928v1 [cs.AI] 15 Jun 2025




                                              Scaling test time compute has shown remarkable success in improving the reasoning abilities of
                                              large language models (LLMs). In this work, we conduct the first systematic exploration of applying
                                              test-time scaling methods to language agents and investigate the extent to which it improves
                                              their effectiveness. Specifically, we explore different test-time scaling strategies, including: (1)
                                              parallel sampling algorithms; (2) sequential revision strategies; (3) verifiers and merging methods;
                                              (4)strategies for diversifying rollouts. We carefully analyze and ablate the impact of different
                                              design strategies on applying test-time scaling on language agents, and have follow findings: 1.
                                              Scaling test time compute could improve the performance of agents. 2. Knowing when to reflect is
                                              important for agents. 3. Among different verification and result merging approaches, the list-wise
                                              method performs best. 4. Increasing diversified rollouts exerts a positive effect on the agent’s task
                                              performance.

                                              Date: June 17, 2025
                                              Correspondence: Wangchunshu Zhou at zhouwangchunshu@oppo.com
                                              Code: https://github.com/OPPO-PersonalAI/OAgents




                                         1   Introduction
                                         Language agents demonstrate exceptional capabilities in various domains [5, 9, 26, 33–35].For example,
                                         LangChain[24] connects LLMs with various tools to solve different tasks in an end-to-end manner, while
                                         Meta-GPT[9] enables multiple AI Agents to take on different roles and collaborate to accomplish tasks.
                                         Recently, long-thinking models like O1 [11] and R1 [8] showcase excellent reasoning abilities of Large Language
                                         Models (LLMs). Recent approaches [15, 18] leverage the extended thinking capabilities of long-activation
                                         models for planning, code writing, tool calling, and completing complex tasks. However, despite LLMs’ strong
                                         capabilities, they still struggle to match human performance on complex search and reasoning tasks [12, 32].
                                         This occurs due to remaining limitations in model capabilities, errors in task planning and question answering,
                                         and issues with complex tool calling abilities.
                                         Increasing computational resources during the inference phase greatly enhances LLMs’ performance. Some
                                         works [19, 20] improve model exploration during inference through different sampling strategies, achieving
                                         excellent scores in challenging areas like mathematical reasoning.Charlie Snell et al.[25] investigated the
                                         effects of scaling inference-time computational consumption, while Wei Xiong et al.[31] focused on enhancing
                                         model performance through self-correction methods. However, directly applying TTS methods to the Agentic
                                         Framework presents many challenges. Unlike LLMs that solve specific problems in an end-to-end manner,
                                         Agents typically decompose complex problems into distinct steps, invoking multiple models sequentially for
                                         resolution. Due to the extended sequence of steps and the accumulation of errors, traditional TTS methods
                                         (e.g., BoN) can significantly undermine the final outcome, because they randomly generate N responses at
                                         each step.


                                                                                               1
To address the aforementioned challenges, we first conduct a systematic exploration of test-time scaling
methods for language agents. First, we investigate the effectiveness of different parallel sampling methods for
agentic test-time scaling, including variants of Best-of-N (BoN), beam search, and tree search algorithms. We
adapt and implement these parallel sampling mechanisms within language agents and showing that despite
simplicity, BoN achieves the optimal performance. Subsequently, we investigate the effectiveness of various
sequential revision techniques, such as reflection and self-refinement, for language agents. We introduce a
reflection agent to summarize and reflect based on the current state and recent actions/observations to help
the agent consistently progress toward accomplishing the task. Experimental results show that the direct
gains from having the agent perform reflection at each step are not obvious. Instead, allowing the agent
to perform reflection when it performs poorly in the current step brings certain benefits. This indicates
that knowing when the agent should reflect is more important than having the agent perform reflection
at every step directly. Finally, we conduct a detailed study on the impact of different verify and result
merging methods, including voting, scoring, and list-wise approaches. Our experimental results demonstrate
that whether for merge results methods or verify methods, using the list-wise method outperforms other
methods. This provides an effective verify method reference for agentic frameworks. Finally, we test different
strategies to expand the agent’s exploration space and enhance the diversity of different rollouts, and propose a
multi-agent collaborative sampling strategy. Experimental results indicate that performance under multi-agent
collaboration surpasses that of a single agent.
Our core contributions are:
      • We explore the application of different parallel sampling strategies in agentic frameworks. Through
        parallel sampling strategies, agent performance can be significantly improved.
      • We study the impact of sequential revision techniques in agentic frameworks. In particular, we point
        out that it is very important for agents to know when they should perform revision.
      • We also conduct detailed comparative analysis of different verify and result merge strategies. Experiments
        show that the list-wise method significantly outperforms other methods.

2     ATTS: Agentic Test-Time Scaling
In this section, we describe and compare different strategies for agentic test-time scaling including: (1)
Parallel Sampling Algorithms; (2) Sequential Revision Strategies; (3) Verifier and Result Merging Methods;
(4) Strategies for Diversifying Rollouts.

2.1     Parallel Sampling Algorithms
To establish a comprehensive evaluation framework for our proposed methods, we regard several parallel
sampling algorithms that are commonly used in the test-time scaling (TTS) domain as baselines.
Best-of-N (BoN) Give a sample times N and question Q, the Best-of-N (BoN) method samples N independent
responses from the LLMs:
                                            {R1 , R2 , ..., RN } = BoN(Q),
then selects the best answer by verifying model. The effectiveness of BoN relies heavily on the quality of the
reward model and the diversity of sampled candidates.
Step-wise-Best-of-N (BoN-wise) BoN selects the optimal result from candidate trajectories as the final response,
while BoN-wise generates N responses at each steps. Specifically, given the thoughts {T 1, T 2, ..., Tt−1 } from
the previous step at time t, BoN-wise generate N responses:
                                {R1 , R2 , ..., RN } = BoN-Wise(Q, T1 , T2 , ..., Tt−1 ),
then it select the optimal response as thought Tt at time t.
Beam Search Beam search maintains a fixed-size beam size K at each step. Specifically, at time t, it generates
N responses for each leaf nodes LNi , then maintains the most suitable K responses that :
                                     {R1 , R2 , ..., RK } = BeamSearch(Q, LNi )


                                                           2
           Q Question              Rejected by PRM                 Selected by PRM           T    Thought                R   Response       Sum Summary              S        Score of PRM



                                       Parallel Sampling                                                                                    Sequential Revision
            BoN                      BoN-wise                      Beam-Search                    DVTS
                Q                         Q                              Q                   Q                  Q                       Q      T1            T2      Sum1          T3




                              T1     T2       T3   T4         T1    T2       T3    T4   T1        T2       T3       T4

                                                                                                                                               R         Sum2            T5         T4
 R1        R2       R3   R4   R1     R2       R3   R4         R1    R2       R3    R4   R1        R2       R3       R4


                                    Verifiers and Merging                                                                               Diversifying Rollouts
                Q
                                                             List-wise                                                                                   Q
                         Verifiers                      R1                    R1        Result Merging
                                                        R2                    R2
                                                        R3                    R3
      T1        T2       T3                                                                      R1       Voting                                                                …
                                                             Scoring                             R1
                                                   R1                    S1        R1                               Rn           Agent 1       Agent 2            Agent 3                Agent N




                                                                                                 …
                                                   R2                    S2        R2                  select majority
      T1        T2       T3
                                                   R3                    S3        R3            RN                                R1            R2                 R3                     R4




Figure 1 Overview of our agentic test-time scaling framework with four key strategies: (1) Parallel Sampling: BoN,
BoN-wise, Beam Search, and DVTS;(2) Sequential Revision: Reflection model with threshold-driven re-generation;(3)
Verifiers and Result Merging Methods: Scoring, list-wise, and majority voting;(4) Diversifying Rollouts: Sampling
across heterogeneous agents.


Most promising partial solutions at each generation step. This algorithm prunes less promising candidates
early in the generation process based on cumulative log-probabilities or reward scores.
DVTS (Diverse Verifier Tree Search): DVTS decomposes the task into K subtrees, where each subtree
operates as an independent beam search algorithm. By exploring multiple subtrees in parallel, DVTS achieves
more diverse search behavior. Under the same computational budget, it finds higher-quality solutions more
effectively than a single beam search with deep exploration.
                                                             {R1 , R2 , ..., RK } = DVTS(Q, SubT reei )


2.2         Sequential Revision Strategies
Besides, given the previous steps {T1 , T2 , ..., Tt−1 } at time t, we leverage a reflection model RefM, to summarize
information:
                                          Sumt = RefM(T1 , T2 , ..., Tt−1 ).

To ensure the model understands when reflection is needed, we use a verify model to objectively score each
step of the model to represent the quality of the current step action, and set different score T hreshold. If and
only if the model action score is less than the T hreshold, the Sumt is added into the LLM to generate the
responses for time t.

2.3         Verifiers and Merging Methods
Verifiers To enable agents to receive positive feedback signals during the sampling process, we have designed
two different process-based reward functions that evaluate the value of each sampling action.
scoring PRM: we score each thought steps at each intermediate step t to revise the final response. For N
thought steps {T1 , T2 , ..., TN } generated at step t, we utilize a LLM as Reward Model (RM), to obtain the
score of each response Si = RM (Tcurrent_i ).


                                                                                          3
list-wise PRM: Another commonly used verify method is to select the optimal trajectory through direct
comparison. For N thought steps {T1 , T2 , . . . , TN } generated at step t, we provide all candidate actions to
the LLM, asking it to select the optimal trajectory from among them, Si = RM(Tcurrent_i )

Result Merging Methods we compare mainstream Result Merging approaches, including voting: Directly
select the majority from all candidates, scoring: using verify for direct scoring, and list-wise: where the model
directly selects the optimal answer from candidate responses.

2.4    Diversifying Rollouts
The efficiency of Parallel Sampling Algorithms is influenced by diversifying rollouts—more diverse rollouts
mean the agent has a greater chance of exploring and discovering the correct answer. LLMs generate diverse
candidates by controlling hyperparameters such as temperature and top_p.
However, in agent frameworks, employing multi-agents to collaboratively accomplish the same task often
enhances task performance. To further increase diversity in the agents’ sampling process, we utilize different
LLMs as rollout models. Different LLMs often exhibit distinct capability profiles; some excel in coding, while
others demonstrate exceptional performance in tool using. We have designed various agent combinations to
maximize rollout diversity.

3     Experiments
3.1   Experiments Setting
To thoroughly investigate the effects of TTS algorithms within the agentic framework, we conduct the following
comparative experiments:

Comparison of Different parallel sampling algorithms In order to comprehensively compare different parallel
sampling algorithms in the agentic framework, we select mainstream parallel sampling algorithms, including
BON, BON-wise, Beam-Search, Tree search, and conduct comparative experiments under identical experimental
settings. We ensure a sampling width of 4, and for Beam-Search and Tree-search, we fix the beam-size at 2.

Comparison of different Sequential Revision Strategies To investigate how self-reflection affect agent per-
formance, focusing on when and how reflection should be applied. We set up the following two settings:
Step-based Reflection: Reflection is conducted at every step to enable continuous error correction. Score-
based Reflection: Initially, the Verify model scores each step of the agent’s process. The agent performs
reflection only when a step’s score falls below a predefined threshold. To further explore how the frequency of
reflection affects performance, we conduct ablation studies using three triggering thresholds: <8 (frequent),
<5 (moderate), and <2 (selective).

Comparison of Different Verifiers and Merging Methods To investigate the impact of different Verifiers and
Merging Methods. First, we compare the performance differences among three mainstream result merging
methods, then based on the optimal result merging method, we compare the effects of different verifiers.

Diversifying Rollouts We explore this influence from two perspectives: on the one hand, we study the
differences in agent capabilities under different sampling widths; on the other hand, we introduce multi-agent
rollouts to explore the benefits of increasing rollout diversity.

3.2    Baseline
We select the SmoLAgents framework as our baseline. In this framework, agents take on different roles
such as code actor and tool calling. In order to more intuitively compare the differences between various
TTS algorithms, we remove the nesting of ToolAgent in the original smolagent framework and only use
CodeAgent to directly call tools. We choose GPT-4.1 as the baseline model for the majority of our experiments.



                                                       4
                          Question:
                          What integer-rounded percentage of the total length of the
                          harlequin shrimp recorded in Omar Valencfia-Mendez 2017
                          paper was the sea star fed to the same type of shrimp in G.
                          Curt Fiedler's 2002 paper?



                                 Agent 1                               Agent N
                           I need to identify and                  I need to find Omar
                               access the Omar                   Valencfia-Mendez's 2017
                           Valencfia-Mendez 2017                  paper on harlequin. I
                             paper on harlequin                  will use google_search
                          shrimp…I will search for                to find the paper and
                            the full citations…                   its relevant details…


                          ResearchGate cites                     ResearchGate cites
                          Valencia-Mendez 2017                   Valencia-Mendez 2017
                          recording Harlequin                    reporting Harlequin
                          Shrimp (Hymenocera                     Shrimp (Hymenocera
                          picta) at ~4.5 cm TL,                  picta) at ~5 cm TL,
                          while Fiedler 2002 used                while Fiedler 2002 used
                          ~1 cm sea star pieces                  ~1 cm sea star pieces
                          for feeding. The                       for feeding. The
                          integer-rounded                        integer-rounded
                          percentage ratio is                    percentage ratio is
                          calculated as:(1 cm /                  calculated as: (1 cm /
                          4.5 cm) × 100.                         5 cm) × 100 = 20.


                             Fianl Answer: 22                           Fianl Answer: 20
                                                  Result Merge


                                                Fianl
                                                 Fianl Answer:
                                                        Answer: 22
                                                                 22            The best
                                                  Fianl
                                                   Fianl Answer:
                                                          Answer: 22
                                                                   22        Final answer
                                                                                 is:22


                                                Fianl Answer: 22        Judge Agent


Figure 2 A case study for ATTS: Given one question, the agent performs operations such as coding and tool calls
during a single rollout, and returns diverse results. The judge agent will merge the final result and output the best
answer.


Additionally, we select current state-of-the-art models including Claude-3-7, Gemini-2.5-Pro, and Claude-3-5
for comparative experiments involving mixed models.

3.3    Benchmark
We choose GAIA[22] as our primary evaluation benchmark. The GAIA validation dataset contains 165
data samples across three different difficulty levels - level1, level2, and level3. It primarily assesses agents’
capabilities in web search and handling multimodal files.

4     Experimental Results




                                                          5
4.1     Comparison of Different Parallel Sampling Algorithms

      Findings 1
      The Parallel Sampling Algorithms significantly enhance agent performance.

As shown in Table 1, we compare the application of mainstream parallel sampling algorithms in agentic
frameworks. The experimental results demonstrate that by applying the parallel sampling algorithms, agents
can achieve superior performance. Compared to the baseline, BoN, BoN-wise, and Beam-Search achieve
significant performance gains, while DVTS performs similarly to the baseline. These results demonstrate the
general effectiveness of Parallel Sampling Algorithms in the agentic framework. Meanwhile, different parallel
sampling algorithms exhibit varying performance characteristics.

Table 1 Comparison with Open-Source Agentic Models and Open-Source Agent Frameworks. For the
open-source models and frameworks, we adopt the results reported in their official papers. For our method, we
consistently use GPT-4.1 as the base model for benchmarking.


      Framework                  Model Family                       Average    Level 1   Level 2   Level 3
      Agentic Model
      Search-o1-32B [16]         -                                    39.8       53.8     34.6      16.7
      WebThinker-32B-RL [17]     -                                    48.5       56.4     50.0      16.7
      Open-Source Agent Frameworks
      TapeAgents [2]             Claude-3-7 etclet@tokeneonedot       55.76     71.70     53.49     30.77
      AutoAgent [26]             Claude-3-5 etclet@tokeneonedot       55.15     71.70     53.40     26.92
      Open Deep Research [1]     OpenAI o1                            55.15     67.92     53.49     34.62
      Magnetic-1 [7]             OpenAI o1 etclet@tokeneonedot        46.06     56.60     46.51     23.08
      FRIDAY [30]                GPT-4 turbo                          34.55     45.28     34.88     11.54
      Smolagents [5]             Openai o1 etclet@tokeneonedot        53.33     62.26     54.65     30.77
      Our Method
      Baseline                   GPT-4.1                              55.76     66.04     58.14     26.92
      BoN                        GPT-4.1                              63.03     77.36     63.95     30.77
      BoN-wise                   GPT-4.1                              58.79     69.23     58.62     38.46
      Beam-Search                GPT-4.1                              56.97     69.81     55.81     34.62
      DVTS                       GPT-4.1                              55.76     58.49     62.79     26.92

The BoN algorithm achieves the best performance gains, with an eight-point improvement over the baseline,
and achieves SOTA results on level 1 and level 2. These two levels are heavily dependent on the agent’s ability
to call and use tools. Under the BoN algorithm, the agent is given more opportunities to repeatedly attempt
similar tasks, which enhances performance particularly on simpler and mid-level difficult problems. BoN-wise
achieves the second-best results after BoN, with a three-point improvement over the baseline. In particular,
BoN-wise achieves the best performance on the most difficult level3 problems, surpassing both the baseline
and BoN. BoN-wise allows for the largest exploration space at each decision node, further demonstrating that
increasing step-wise exploration leads to better performance on complex tasks.
Notably, Beam-search and DVTS show no significant improvement over baseline. This is because although
these algorithms can significantly increase the agent’s exploration space, their exploration also depends on
the accuracy of signals provided by the verify model, which prevents the agent from stably approaching the
correct answers.




                                                      6
4.2     The impact of different Sequential Revision Strategies

      Findings 2
      Understanding the opportune moments for reflection is key to its profound benefit.

As shown in Table 2, we first compare the baseline agent with the reflection-enabled agent to assess the
effectiveness of self-reflection. The baseline achieves an overall score of 55.76, while the reflection model
scores slightly lower at 55.15, suggesting that reflection, while enabling error correction, may also disrupt
the model’s reasoning flow. At Level 1, reflection significantly improves performance (71.7), indicating its
benefit for simple tasks where minor errors can be quickly corrected without much overhead. However, at
Level 2, reflection underperforms compared to the baseline, especially when applied frequently, suggesting
that moderate-complexity tasks are more susceptible to disruption from excessive introspection. At Level 3,
reflection leads to a moderate improvement (34.62), showing its value in preventing critical failures in complex
scenarios, although overall performance remains limited by task difficulty.

                                       Table 2 Performance with reflection

                               Search type      Score   Level 1     Level 2   Level 3
                               Baseline         55.76       66.04   58.14     26.92
                               Reflection       55.15       71.7    51.16     34.62
                               Threshold(<8)    53.33       66.04   53.49     26.92
                               Threshold(<5)    52.12       69.81    50.0     23.08
                               Threshold(<2)    56.36        71.7   55.81     26.92


As reflection introduces both benefits and potential disruptions, we examine how varying the frequency of
reflection impacts task execution across different levels of complexity. Frequent reflection (threshold <8)
results in the lowest overall score (53.66), particularly hurting performance at Level 2 due to reasoning
interruptions. Moderate reflection (<5) yields even lower performance (52.12), whereas selective reflection
(<2) achieves the best result (56.36), outperforming other strategies across all levels. This indicates that
restricting reflection to only the most critical steps minimizes disruption while still allowing meaningful error
correction. These findings suggest that effective use of reflection depends heavily on its application frequency
and timing—low-frequency, context-aware reflection is most beneficial, especially for maintaining coherence in
multi-step reasoning processes.

4.3     The impact of different verifiers and result merging methods

      Findings 3
      The list-wise approach outperforms alternative methods in both verification and result merging.


The impact of different result merges method As shown in Table 3, we first compare common result merging
methods. For these three algorithms - BoN, Beam-Search, and Tree Search - the list-wise approach outperforms
other approaches. This is because: 1) compared to scoring that directly relies on standard scoring, list-wise
has comparable standards for reference, making evaluation more accurate; and 2) compared to voting methods,
list-wise not only considers majority options in the answers, but can also select potentially correct answers
from diverse candidates. s

The impact of different verify methods As shown in Table 4, we compare the effects of different verify
methods on agent performance. The list-wise verify method scores 3 points higher on average than the scoring,
which indicate that, whether in BoN-wise or Beam-Search, using list-wise comparison of candidates is superior
to the scoring approach. This suggests that compared to directly having PRM score the agent’s trajectory


                                                        7
       Table 3 Comparing performance of different result merging methods thought BoN and Beam-Search.

                                 Search type      voting   Scoring    list-wise
                                 BoN               56.8      59.39      63.03
                                 Beam-Search      54.55      53.94      56.97


(scoring), using a list-wise approach to have PRM select the relatively optimal trajectory can bring more
precise benefits.

                Table 4 Performance with different verify methods across various search methods.

                                    Search type     Verify method     Score
                                                         scoring       56.36
                                    BoN-wise
                                                        list-wise      58.79
                                                         scoring       53.94
                                    Beam-Search
                                                        list-wise      56.97
                                                         scoring       50.91
                                    Tree-Search
                                                        list-wise      55.76



4.4    The impact of Diversifying Rollouts

      Findings 4
   Increasing diversifying rollouts enhances agent performance.


Performance with different search size Figure 3 presents the performance variations of the agent under
different sampling widths. The experimental results demonstrate that increasing the agent’s sampling width
leads to significant performance improvements, a finding that aligns with test-time scaling phenomena observed
in the LLM domain.




   Figure 3 Performance comparison of BoN and BoN-wise algorithms across different search sizes (1, 2, and 4).



Performance with different rollout models To further explore the impact of different rollout models on
Diversifying Rollouts, we measure the pass@1 performance of SOTA models and calculate their pass@2 and
pass@4 performance when combined with the baseline model GPT-4.1.



                                                       8
As shown in Table 5, under the pass@1 setting, GPT-4.1 achieves the highest score. Notably, under the
pass@2 and pass@4 settings, using other models mixed with GPT-4.1 yields higher results than using GPT-4.1
alone, which further demonstrates the effectiveness of using different rollouts models. Additionally, using all
four different models achieves a total score of 74.55 for pass@4, reaching a level that surpasses the open-source
SOTA.
Table 5 Performance with different rollout models evaluated by Pass@K. Under each setting, the best performance is
indicated with underlining.

               Model                                                  all    level1   level2   level3
               GPT-4.1                                              55.76    66.04    58.14    26.92
               Claude-3-5                                           42.42    50.94    46.51    11.54
               Claude-3-7                                           50.30    54.72    50.00    42.31
               Gemini-2.5-PRO                                       41.82    54.72    41.86    15.38
               Pass@2
               GPT-4.1 only                                         60.49    70.59    60.00    42.31
               GPT-4.1,Claude-3-5                                   64.24    71.70    69.77    30.77
               GPT-4.1,Claude-3-7                                   64.24    71.70    63.95    50.00
               GPT-4.1,Gemini-2.5-PRO                               62.42    79.25    60.47    34.62
               Pass@4
               GPT-4.1 only                                         69.14    82.35    71.76    34.62
               GPT-4.1,Claude-3-5, Gemini-2.5-PRO,Claude-3-7        74.55    86.79    74.42    50.00


5    Related Work
Language Agents In previous research work, many mature agentic frameworks have been established,
such as Meta-GPT[10] which enables GPT to assume different roles and collaboratively complete tasks,
LangChain[24] which uses natural language to describe tools and solve complex tasks, and AGENTS[34] which,
in addition to supporting basic tool calling and long-term memory, also supports human-agent interaction
and controllability through symbolic plans (SOPs). Recently, with the emergence of OPENAI’s deep research
concept, numerous agentic frameworks have appeared, such as Manus[18], OWL[15], and SmoLAgents[5].
These agentic frameworks support collaborative work among various agents, decompose task inputs, conduct
multi-step task planning, and invoke diverse tools to complete complex tasks. However, current agentic
frameworks predominantly employ a single linear workflow to solve problems and have not yet conducted
in-depth exploration of Test-Time-Scaling (TTS) capabilities.

LLM Test-Time Scaling Snell et al. [25] propose that scaling LLMs Test-time Compute[29] optimally can be
more effective than scaling model parameters. OpenAI’s o1 model 1 is designed to spend more time reasoning
before they respond for the sake of obtaining better performance. Recently, various TTS algorithms have
emerged, such as Best-Of-N, Beam-Search, Tree-Search, and Majority-Vote.[6, 13, 21] Moreover, [14] and [31]
investigate enabling LLMs to perform self-reflection through self-rewarding and self-correlation mechanisms to
enhance their performance.
Besides, Some works([3, 25, 28]) design reward models to guide the trajectory selection process in LLM
test-time scaling . [4] incorporates deep thinking into reward models, while [23] uses RM for complex tool
selection. [20] and [27] provide a comprehensive experimental analysis of LLM Test-Time Scaling. However,
Test-Time Scaling strategies have not yet been fully discussed within agentic frameworks. In this work, we
investigate four key aspects of test-time scaling strategies: parallel sampling algorithms, sequential revision
strategies, verifiers and merging methods, and strategies for diversifying rollouts, and conduct comprehensive
ablation experiments comparing various strategies within each aspect.
    1 https://openai.com/o1/




                                                        9
6   Conclusion
Test Time Scaling (TTS) can significantly enhance LLM inference performance by increasing computational
resources during the inference phase. However, the application of Test Time Scaling in the agentic domain
still needs to be explored. In this paper, we explore four different aspects of test-time scaling strategies:
Parallel Sampling Algorithms; Sequential Revision Strategies; Verifiers and Merging Methods; Strategies for
Diversifying Rollouts. We conduct detailed comparative ablation experiments for strategies in each aspect.
Our experimental results indicate: 1. Applying parallel sampling algorithms to scale agent test time compute
could improve agent performance, 2. For sequential revision, it is important to know when to revise, 3.
Among different verify and result merge methods, list-wise methods perform best, 4. Increasing diversified
rollouts exerts a positive benefit on agent, which aligns with test-time scaling phenomena observed in the
LLM domain.




                                                     10
7   Contributions
Core Contributors

    • King Zhu                • Siwei Wu
    • Hanhao Li


Contributors

    • Tianshun Xing           • Jiaheng Liu
    • Dehua Ma                • Yuchen Eleanor Jiang
    • Xiangru Tang            • Changwang Zhang
    • Minghao Liu             • Chenghua Lin
    • Jian Yang               • Jun Wang


Corresponding Authors

    • Wangchunshu Zhou        • Ge Zhang




                         11
References
 [1] L. AI. Open deep research: A fully open-source research assistant, 2025. URL https://github.com/langchain-ai/
     open_deep_research.
 [2] D. Bahdanau, N. Gontier, G. Huang, E. Kamalloo, R. Pardinas, A. Piché, T. Scholak, O. Shliazhko, J. P. Tremblay,
     K. Ghanem, S. Parikh, M. Tiwari, and Q. Vohra. Tapeagents: a holistic framework for agent development and
     optimization, 2024. URL https://arxiv.org/abs/2412.08445.
 [3] E. Beeching, L. Tunstall, and S. Rush. Scaling test-time compute with open models, 2024. URL https:
     //huggingface.co/spaces/HuggingFaceH4/blogpost-scaling-test-time-compute.
 [4] X. Chen, G. Li, Z. Wang, B. Jin, C. Qian, Y. Wang, H. Wang, Y. Zhang, D. Zhang, T. Zhang, et al. Rm-r1:
     Reward modeling as reasoning. arXiv preprint arXiv:2505.02387, 2025.
 [5] H. Face. Smolagent: A scalable approach to multi-agent systems, 2025. URL https://github.com/huggingface/
     smolagents.
 [6] G. Faria and N. A. Smith. Sample, don’t search: Rethinking test-time alignment for language models, 2025. URL
     https://arxiv.org/abs/2504.03790.
 [7] A. Fourney, G. Bansal, H. Mozannar, C. Tan, E. Salinas, E. E. Zhu, F. Niedtner, G. Proebsting, G. Bassman,
     J. Gerrits, J. Alber, P. Chang, R. Loynd, R. West, V. Dibia, A. Awadallah, E. Kamar, R. Hosn, and S. Amershi.
     Magentic-one: A generalist multi-agent system for solving complex tasks, 2024. URL https://arxiv.org/abs/
     2411.04468.
 [8] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al. Deepseek-r1:
     Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025.
 [9] S. Hong, X. Zheng, J. Chen, Y. Cheng, J. Wang, C. Zhang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, et al. Metagpt:
     Meta programming for multi-agent collaborative framework. arXiv preprint arXiv:2308.00352, 3(4):6, 2023.
[10] S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, C. Zhang, J. Wang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou,
     C. Ran, L. Xiao, C. Wu, and J. Schmidhuber. Metagpt: Meta programming for a multi-agent collaborative
     framework, 2024. URL https://arxiv.org/abs/2308.00352.
[11] A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel, A. Carney,
     et al. Openai o1 system card. arXiv preprint arXiv:2412.16720, 2024.
[12] J. Y. Koh, R. Lo, L. Jang, V. Duvvur, M. C. Lim, P.-Y. Huang, G. Neubig, S. Zhou, R. Salakhutdinov, and D. Fried.
     Visualwebarena: Evaluating multimodal agents on realistic visual web tasks. arXiv preprint arXiv:2401.13649,
     2024.
[13] J. Y. Koh, S. McAleer, D. Fried, and R. Salakhutdinov. Tree search for language model agents, 2024. URL
     https://arxiv.org/abs/2407.01476.
[14] A. Kumar, V. Zhuang, R. Agarwal, Y. Su, J. D. Co-Reyes, A. Singh, K. Baumli, S. Iqbal, C. Bishop, R. Roelofs,
     et al. Training language models to self-correct via reinforcement learning. arXiv preprint arXiv:2409.12917, 2024.
[15] M. H. Y. Z. W. F. Y. N. B. X. T. S. Z. Y. Z. J. Y. L. Z. Z. Y. W. Q. Y. P. L. G. Li. Owl: Optimized workforce learning
     for general multi-agent assistance in real-world task automation, 2025. URL https://github.com/camel-ai/owl.
[16] X. Li, G. Dong, J. Jin, Y. Zhang, Y. Zhou, Y. Zhu, P. Zhang, and Z. Dou. Search-o1: Agentic search-enhanced
     large reasoning models, 2025. URL https://arxiv.org/abs/2501.05366.
[17] X. Li, J. Jin, G. Dong, H. Qian, Y. Zhu, Y. Wu, J.-R. Wen, and Z. Dou. Webthinker: Empowering large reasoning
     models with deep research capability, 2025. URL https://arxiv.org/abs/2504.21776.
[18] X. Liang, J. Xiang, Z. Yu, J. Zhang, S. Hong, S. Fan, and X. Tang. Openmanus: An open-source framework for
     building general ai agents, 2025. URL https://doi.org/10.5281/zenodo.15186407.
[19] F. Liu, W. Chao, N. Tan, and H. Liu. Bag of tricks for inference-time computation of llm reasoning, 2025. URL
     https://arxiv.org/abs/2502.07191.
[20] R. Liu, J. Gao, J. Zhao, K. Zhang, X. Li, B. Qi, W. Ouyang, and B. Zhou. Can 1b llm surpass 405b llm?
     rethinking compute-optimal test-time scaling, 2025. URL https://arxiv.org/abs/2502.06703.




                                                           12
[21] R. Liu, J. Gao, J. Zhao, K. Zhang, X. Li, B. Qi, W. Ouyang, and B. Zhou. Can 1b llm surpass 405b llm?
     rethinking compute-optimal test-time scaling. arXiv preprint arXiv:2502.06703, 2025.
[22] G. Mialon, C. Fourrier, T. Wolf, Y. LeCun, and T. Scialom. Gaia: a benchmark for general ai assistants. In The
     Twelfth International Conference on Learning Representations, 2023.
[23] C. Qian, E. C. Acikgoz, Q. He, H. Wang, X. Chen, D. Hakkani-Tür, G. Tur, and H. Ji. Toolrl: Reward is all tool
     learning needs. arXiv preprint arXiv:2504.13958, 2025.
[24] L. repository. Langchain, 2022. URL https://github.com/langchain-ai/langchain.
[25] C. Snell, J. Lee, K. Xu, and A. Kumar. Scaling llm test-time compute optimally can be more effective than
     scaling model parameters. arXiv preprint arXiv:2408.03314, 2024.
[26] J. Tang, T. Fan, and C. Huang. Autoagent: A fully-automated and zero-code framework for llm agents, 2025.
     URL https://arxiv.org/abs/2502.05957.
[27] S. Wu, Z. Peng, X. Du, T. Zheng, M. Liu, J. Wu, J. Ma, Y. Li, J. Yang, W. Zhou, et al. A comparative study on
     reasoning patterns of openai’s o1 model. arXiv preprint arXiv:2410.13639, 2024.
[28] Y. Wu, Z. Sun, S. Li, S. Welleck, and Y. Yang. Inference scaling laws: An empirical analysis of compute-optimal
     inference for problem-solving with language models. arXiv preprint arXiv:2408.00724, 2024.
[29] Y. Wu, Z. Sun, S. Li, S. Welleck, and Y. Yang. Inference scaling laws: An empirical analysis of compute-optimal
     inference for problem-solving with language models, 2025. URL https://arxiv.org/abs/2408.00724.
[30] Z. Wu, C. Han, Z. Ding, Z. Weng, Z. Liu, S. Yao, T. Yu, and L. Kong. Os-copilot: Towards generalist computer
     agents with self-improvement, 2024. URL https://arxiv.org/abs/2402.07456.
[31] W. Xiong, H. Zhang, C. Ye, L. Chen, N. Jiang, and T. Zhang. Self-rewarding correction for mathematical
     reasoning. arXiv preprint arXiv:2502.19613, 2025.
[32] S. Zhou, F. F. Xu, H. Zhu, X. Zhou, R. Lo, A. Sridhar, X. Cheng, T. Ou, Y. Bisk, D. Fried, et al. Webarena: A
     realistic web environment for building autonomous agents. arXiv preprint arXiv:2307.13854, 2023.
[33] W. Zhou, Y. E. Jiang, P. Cui, T. Wang, Z. Xiao, Y. Hou, R. Cotterell, and M. Sachan. Recurrentgpt: Interactive
     generation of (arbitrarily) long text, 2023. URL https://arxiv.org/abs/2305.13304.
[34] W. Zhou, Y. E. Jiang, L. Li, J. Wu, T. Wang, S. Qiu, J. Zhang, J. Chen, R. Wu, S. Wang, S. Zhu, J. Chen,
     W. Zhang, X. Tang, N. Zhang, H. Chen, P. Cui, and M. Sachan. Agents: An open-source framework for
     autonomous language agents, 2023. URL https://arxiv.org/abs/2309.07870.
[35] W. Zhou, Y. Ou, S. Ding, L. Li, J. Wu, T. Wang, J. Chen, S. Wang, X. Xu, N. Zhang, H. Chen, and Y. E. Jiang.
     Symbolic learning enables self-evolving agents. 2024. URL https://arxiv.org/abs/2406.18532.




                                                        13
8   Appendix
    PRM-score Evaluation Prompt

    Evaluation Guidelines:
       • Objective:
           – You will evaluate a candidate ActionStep node, which includes the following fields:
                ∗ step_number: Depth of this step within the TTS search tree.
                ∗ observations: Observations recorded after executing this action.
                ∗ action_output: Direct output resulting from this action.
                ∗ model_output: Raw LLM output that led to this action.
                ∗ error: Any encountered errors (can be None).
                ∗ score: Previously assigned score (for reference only).
                ∗ previous_steps: The history of earlier steps, including TaskStep and PlanningStep, along with the
                  trajectory of ActionSteps leading to the current state.
           – Your goal is to judge how promising this ActionStep is for advancing toward the user’s task, using your inde-
             pendent judgment while considering the continuity and logical flow of the ActionStep sequence, including the
             historical context.
       • Evaluation Criteria:
           – Progress Toward Goal:
               ∗ Assess whether the action_output clearly and tangibly advances the overall task.
               ∗ Reward meaningful progress or valuable new information.
               ∗ Penalize irrelevant actions or weak impact.
           – Error and Stability:
               ∗ Penalize based on the severity of errors:
                    · Fatal/blocking errors: 0-1 points.
                    · Significant errors: 1-3 points.
                    · Minor or recoverable errors: 3-5 points.
               ∗ Reduce the score if the model_output is ambiguous or unstable.
           – TTS Efficiency:
               ∗ Reward actions that contribute efficiently toward reaching the goal.
               ∗ Penalize redundant or repetitive actions without meaningful progress.
           – Reflection Usage:
               ∗ Reward active utilization of reflection to improve upon past mistakes.
               ∗ Penalize ignoring reflection insights.
           – Loop Detection:
               ∗ Detect loops or repetitions compared to previous steps.
               ∗ Identify true loops and penalize based on severity.
           – Contextual Awareness:
               ∗ Infer alignment with previous PlanningStep and TaskStep.
               ∗ Ensure consistency with the TTS strategy and penalize deviations.
       • Scoring Criteria:
           – 9-10: Clearly advances the goal; highly efficient; strong reflection use; no loops.
           – 7-8: Good advancement; minor inefficiencies; clear reflection use; minimal loop risk.
           – 5-6: Moderate progress; limited efficiency; moderate reflection use; mild repetition risks.
           – 3-4: Poor advancement; inefficient; weak reflection use; noticeable loop risks.
           – 1-2: Minimal advancement; repetitive actions; true loops; significant errors.
           – 0: Severe issues: explicit loops, critical errors, or complete irrelevance to the task context.
       • Final Evaluation Output: You must provide your evaluation in valid JSON format with the following structure:
                { "analysis": "Detailed analysis addressing progress, TTS efficiency, reflection
              usage, loop detection, contextual alignment with PlanningStep/TaskStep, error
              severity, and overall action quality.", "score": [integer between 0-10] }
                                                                14
PRM-list Evaluation Prompt

Evaluation Guidelines:
   • Objective:
          – You will evaluate N candidate trajectories, each representing a series of nodes in a search tree. Each trajectory contains the following:
               ∗ step_number: Depth of the node in the trajectory.
               ∗ observations: Observations recorded at each step of the trajectory.
               ∗ action_output: Direct action output at each step.
               ∗ model_output: Raw model output (LLM).
               ∗ error: Any errors encountered (can be None).
               ∗ score: Previously calculated score (if available).
               ∗ previous_steps: The history of earlier steps, including TaskStep and PlanningStep, with the trajectory of ActionSteps leading to the
                  current state.
          – Your goal is to evaluate each trajectory holistically, considering how well it progresses toward solving the user’s task. Select the trajectory that
            most effectively achieves this goal.
   •   Evaluation Criteria:
         – Progress Toward Goal:
                 ∗ Assess how well each trajectory advances the task at hand, considering both the individual node’s progress and the overall progression
                   of the entire trajectory.
                 ∗ Reward trajectories that demonstrate tangible and meaningful progress toward the goal.
                 ∗ Penalize trajectories with weak actions or minimal/no advancement.
          – Trajectory Efficiency:
              ∗ Evaluate how efficiently each trajectory progresses toward the goal, considering the depth and complexity of the steps.
              ∗ Favor trajectories that achieve significant progress with fewer steps.
              ∗ Consider the overall value-to-depth ratio when comparing trajectories of different lengths.
              ∗ Reward efficient exploration of the search space.
          – Loop Detection:
              ∗ Detect loops or repetitions within each trajectory, especially those related to previous steps.
              ∗ Loop types:
                    · Real Loops: Identical nodes (observations, action output, and model output) that do not add value to the trajectory.
                    · Benign Repetitions: Similar strategies with variations yielding additional progress.
              ∗ Heavily penalize trajectories with real loops.
              ∗ Slight penalties for benign repetitions if they lead to meaningful improvements.
          – Error and Stability:
              ∗ Evaluate the severity of errors encountered in each trajectory and penalize based on their impact on progression.
              ∗ Error Severity:
                    · Fatal/Blocking Errors: Major penalty.
                    · Significant Errors: Moderate penalty.
                    · Minor/Recoverable Issues: Minor penalty.
              ∗ Penalize unstable or unclear model outputs.
              ∗ Consider how errors affect the overall trajectory’s ability to move toward the goal.
          – Overall Trajectory Quality:
              ∗ Evaluate the coherence and overall quality of the trajectory.
              ∗ Consider the logical sequence of steps and the exploration-exploitation balance.
              ∗ Evaluate the final node’s closeness to achieving the goal.
              ∗ Reward trajectories that make consistent progress and demonstrate coherent planning.
   •   Final Output Format: Provide your evaluation in the following JSON format. Select the best trajectory and provide a detailed analysis
       explaining why it is the most promising trajectory.
                { "index": [integer], # Index of the best trajectory "analysis": "Detailed analysis addressing progress,
               efficiency, reflection usage, loop detection, error severity, and overall trajectory quality." }




                                                                            15
Single Node Reflection Prompt

Node Information:
   • step_number: The depth of the node within the BON/beam search tree.
   • observations: The data or observations recorded during this step.
   • action_output: The direct output resulting from an action taken at this step (e.g., API call, tool response).
   • model_output: The raw output generated by the model at this step.
   • error: Any errors encountered during this step (if applicable).
Goal:
   • Summarize:
       – Provide a brief overview of what occurred at this node.
       – Describe the action taken and the results or new information that emerged as a result of this action.
   • Reflect:
       – Assess whether the action taken in this node was successful, partially successful, or unsuccessful.
       – Identify any errors, issues, or incompleteness relevant to this step.
       – Compare the node’s outcome with its assigned score, providing an evaluation of whether the score is aligned
          with the actual result.
   • Confidence:
       – Evaluate your confidence in the action taken at this node (High/Medium/Low).
       – If confidence is high, explicitly suggest continuing along this exploration path.
       – If confidence is medium or low, recommend potential improvements or alternatives, while leaving room for
          exploration to remain open.
   • Suggest:
       – Provide specific and focused suggestions for refining the current step.
       – These should be based on the evaluation of the current node, with an emphasis on actionable changes that can
         be made in the next attempt of a similar step.
       – Focus exclusively on improvements that can be applied within this node. Avoid proposing changes that span
         multiple steps or introduce larger, long-term strategies.
       – Base your evaluation strictly on the provided fields—action_output, observations, error, etc. Do not infer
         additional context or hypothesize about alternative paths or unknown factors.
       – Only flag a step as unsuccessful or in need of improvement if there is clear, tangible evidence (e.g., explicit
         errors, missing or incorrect outputs).
       – Do not override factual results based on subjective judgment, even if the node’s score does not seem to match
         the outcome.
   • General Guidelines:
       – Your suggestions should be conservative, focusing only on changes where there is a clear issue or opportunity
         for improvement.
       – If no significant issues are identified, provide minimal or no suggestions for improvement.
Output Format:
   • experience_summary: A concise overview of the events at this node and the key outcomes.
   • confidence_assessment: High/Medium/Low with a recommendation for future exploration.
   • lessons_learned: Key takeaways or specific improvements based on the evaluation of the current node’s action.
   • comments: Optional minor remarks, clarifications, or additional observations.




                                                           16
