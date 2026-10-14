                                              A Survey of Vibe Coding with Large Language Models

                                                      Yuyao Ge1∗     Lingrui Mei1∗      Zenghao Duan1    Tianhao Li2     Yujia Zheng2
                                                          Yiwei Wang3     Lexin Wang1      Jiayu Yao1∗   Tianyu Liu4   Yujun Cai5
                                                    Baolong Bi1∗   Fangda Guo1       Jiafeng Guo1∗   Shenghua Liu1†∗      Xueqi Cheng1∗
arXiv:2510.12399v2 [cs.AI] 21 Dec 2025




                                                  1 Institute of Computing Technology, Chinese Academy of Sciences       2 Duke University

                                                   3 University of California, Merced    4 Peking University   5 University of Queensland




                                         The advancement of large language models (LLMs) has catalyzed a paradigm shift from code generation
                                         assistance to autonomous coding agents, enabling a novel development methodology termed "Vibe Coding"
                                         where developers validate AI-generated implementations through outcome observation rather than line-by-
                                         line code comprehension. Despite its transformative potential, the effectiveness of this emergent paradigm
                                         remains under-explored, with empirical evidence revealing unexpected productivity losses and fundamental
                                         challenges in human-AI collaboration. To address this gap, this survey provides the first comprehensive
                                         and systematic review of Vibe Coding with large language models, establishing both theoretical foundations
                                         and practical frameworks for this transformative development approach. Drawing from systematic analysis
                                         of over 1000 research papers, we survey the entire vibe coding ecosystem, examining critical infrastructure
                                         components including LLMs for coding, LLM-based coding agent, development environment of coding
                                         agent, and feedback mechanisms. We first introduce Vibe Coding as a formal discipline by formalizing it
                                         through a Constrained Markov Decision Process that captures the dynamic triadic relationship among
                                         human developers, software projects, and coding agents. Building upon this theoretical foundation, we then
                                         synthesize existing practices into five distinct development models: Unconstrained Automation, Iterative
                                         Conversational Collaboration, Planning-Driven, Test-Driven, and Context-Enhanced Models, thus providing
                                         the first comprehensive taxonomy in this domain. Critically, our analysis reveals that successful Vibe
                                         Coding depends not merely on agent capabilities but on systematic context engineering, well-established
                                         development environments, and human-agent collaborative development models. Based on these findings,
                                         we identify key challenges spanning technical infrastructure optimization, security mechanisms, and
                                         human-centered design considerations. Ultimately, this survey serves as both a conceptual foundation for
                                         AI-augmented software engineering and a technical roadmap for researchers and practitioners navigating
                                         this rapidly evolving field.

                                         ∗:  Also affiliated with: (1) Key Laboratory of Network Data Science and Technology, ICT, CAS; (2) State Key
                                         Laboratory of AI Safety; (3) University of Chinese Academy of Sciences
                                         † : Corresponding Author


                                         Keywords: Vibe Coding, Coding Agent, Large Language Models

                                         Date: December 23, 2025
                                         Contact: geyuyao24z@ict.ac.cn, liushenghua@ict.ac.cn
                                         Github Repository: https://github.com/YuyaoGe/Awesome-Vibe-Coding
Contents
1   Introduction                                                                                                              4
2   Related Work                                                                                                              5
    2.1 Related Surveys . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   5
    2.2 Preliminary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   6
3 Vibe Coding: The Engineering of Managing Coding Agents                                                                       7
  3.1 Definition of Vibe Coding . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        7
  3.2 Why Vibe Coding . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       10
4   Large Language Models for Coding                                                                                          11
    4.1 Data Foundation of Code LLMs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          11
        4.1.1 Pre-training Code Corpora . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         11
        4.1.2 Instruction & Preference Datasets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         12
    4.2 Pre-training Techniques . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     12
        4.2.1 Pre-training Objectives . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     12
        4.2.2 Continual Pre-training Strategies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       13
    4.3 Post-training Techniques . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    15
        4.3.1 Supervised Fine-tuning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        15
        4.3.2 Reinforcement Learning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        15
5   LLM-based Coding Agent                                                                                                    17
    5.1 Decomposition and Planning Capability . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           17
        5.1.1 Task Decomposition Strategies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         17
        5.1.2 Plan Formulation Methods . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          17
    5.2 Memory Mechanism . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        17
        5.2.1 Overview and Fundamentals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           17
        5.2.2 Memory Operations and Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                17
        5.2.3 Memory Architecture in Coding Agents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .              18
    5.3 Action Execution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    19
        5.3.1 Tool Invocation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     19
        5.3.2 Code-based Action Implementation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .            19
    5.4 Reflection: Iteration, Validation, and Debugging . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          21
        5.4.1 Iterative Refinement . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      21
        5.4.2 Code Validation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       21
        5.4.3 Intelligent Debugging . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       21
    5.5 Agent Collaboration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     21
        5.5.1 Collaboration Mechanisms . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          21
        5.5.2 Framework Implementations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           22
6   Development Environment of Coding Agent                                                                                   22
    6.1 Isolated Execution Runtime Environment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          22
        6.1.1 Containerization Technologies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         22
        6.1.2 Security Isolation Mechanisms . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         23
        6.1.3 Cloud-based Execution Platforms . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           23
    6.2 Interactive Development Interface Environment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           24
        6.2.1 AI-Native Development Interfaces . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          24
        6.2.2 Remote Development . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          24
        6.2.3 Tool Integration Protocol Standards . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         24
    6.3 Distributed Orchestration Platform Environment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .            24


                                                               2
                                   A Survey of Vibe Coding with Large Language Models



         6.3.1   CI/CD Pipeline Integration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    24
         6.3.2   Cloud Compute Orchestration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       25
         6.3.3   Multi-Agent Collaboration Frameworks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          25
7   Feedback Mechanisms                                                                                                      26
    7.1 Compiler Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    26
        7.1.1 Syntax and Type Error Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           26
        7.1.2 Static Analysis Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       26
        7.1.3 Runtime Compilation Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           27
    7.2 Execution Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   27
        7.2.1 Unit Test Execution Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      27
        7.2.2 Integration Test Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      28
        7.2.3 Runtime Error and Exception Handling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .             29
    7.3 Human Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     29
        7.3.1 Interactive Requirement Clarification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        29
        7.3.2 Code Review Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         30
    7.4 Self-Refinement Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     31
        7.4.1 Self-Evaluation and Critique . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       31
        7.4.2 Multi-Agent Collaborative Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           31
        7.4.3 Reflection and Memory-Based Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .             32
8 Vibe Coding Development Models                                                                                             33
  8.1 Framework Principles . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       33
  8.2 Unconstrained Automation Model (UAM) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .               33
  8.3 Iterative Conversational Collaboration Model (ICCM) . . . . . . . . . . . . . . . . . . . . . . . . . . .              33
  8.4 Planning-Driven Model (PDM) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          34
  8.5 Test-Driven Model (TDM) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        34
  8.6 Context-Enhanced Model (CEM) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           35
9   Future Impact and Open Challenges                                                                                        35
    9.1 Reengineering of Development Process in Vibe Coding . . . . . . . . . . . . . . . . . . . . . . . . . .              35
        9.1.1 From Phased Lifecycles to Continuous Micro-Iterations . . . . . . . . . . . . . . . . . . . . . .              35
        9.1.2 Redefinition of Developer Roles and Skillsets . . . . . . . . . . . . . . . . . . . . . . . . . . . .          36
        9.1.3 New Challenges in Project Management and Collaboration . . . . . . . . . . . . . . . . . . . .                 36
    9.2 Code Reliability and Security in Vibe Coding . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         37
        9.2.1 The Inadequacy of Manual Review . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .            37
        9.2.2 Architecting an Integrated Security and Reliability Feedback Loop . . . . . . . . . . . . . . .                37
        9.2.3 The Human-in-the-Loop as a Final Arbiter . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           38
    9.3 Scalable Oversight of Vibe Coding Agents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         38
        9.3.1 Emerging Risks of Vide Coding Workflow . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .             38
        9.3.2 Toward Scalable Oversight Architectures . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          39
    9.4 Human Factors in Vibe Coding . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       40
        9.4.1 Mental Model Shift: From Code Logic to Context Engineering . . . . . . . . . . . . . . . . . .                 40
        9.4.2 Evolving Developer Skill Sets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        40
        9.4.3 Team Collaboration and AI Integration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          41
        9.4.4 Broader Implications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     41
10 Conclusion                                                                                                                41




                                                               3
                               A Survey of Vibe Coding with Large Language Models



1   Introduction
Large language models (LLMs) have significantly advanced artificial intelligence through conversational systems
capable of fluent natural language understanding and generation [1, 2]. Early adoption in software development
positioned LLMs as supplementary assistants—developers employed natural language prompts to generate code
snippets, but significant accuracy limitations necessitated manual review and iterative debugging throughout the
software development lifecycle [3–7].
The emergence of advanced architectures like GPT-4 [8] and Claude Sonnet 4 [9] enabled qualitative improvements,
leading to Coding Agents capable of autonomously completing programming tasks through dynamic environmen-
tal interaction via shell commands, file operations, and test execution [10]. These agents have demonstrated rapid
progress on real-world programming tasks. Taking SWE-bench as an example [11], SWE-agent reached 12.5%
with custom interfaces [12], AutoCodeRover achieved 19.0% resolution through code search and fault localization
[13], Agentless attained 27.3% [14], OpenHands achieved 53% on SWE-bench Verified [15], and self-improving
agents demonstrated 17–53% performance gains on SWE-bench Verified [16].
With the advancement of large language models such as GPT-5 Pro [17] and Claude Sonnet 4.5 [9], llm-based
coding agent capabilities have achieved significant breakthroughs, giving rise to “Vibe Coding”—a paradigm
where developers rely on AI-generated code without line-by-line inspection, engaging instead in iterative cycles
of natural language requirement articulation, execution observation, and feedback [18–21]. Coding Agents go
beyond code generation—they autonomously configure environments, execute programs, self-diagnose errors, and
update implementations. This represents a substantial elevation in human trust and a departure from traditional
comprehension mandates toward outcome-oriented validation [22–25].
However, possessing powerful agents proves insufficient. Task complexity exposes fundamental limitations
in unstructured natural language instructions, which fail to convey nuanced requirements and architectural
constraints [11, 26]. Empirical evidence reveals that experienced developers using Cursor with Claude experienced
19% increased completion time rather than anticipated productivity gains [27]. Effective human-AI collaboration
demands systematic prompt engineering and context engineering [28], structured instructions [29, 3, 30, 31], and
balanced agency distribution across various distinct interaction types [32, 33].
To address this critical gap, this survey provides the first comprehensive and systematic review of Vibe Coding
with Large Language Models. As shown in Figure 2, we introduce Vibe Coding as a dynamic triadic relationship
among human developers, software projects, and coding agents, providing its first formal definition as an
engineering discipline through a Constrained Markov Decision Process [34]. Building upon this theoretical
foundation, we distill Vibe Coding workflows into five development models—Unconstrained Automation
Model, Iterative Conversational Collaboration Model, Planning-Driven Model, Test-Driven Model, and Context-
Enhanced Model—representing the first comprehensive synthesis of existing practices. Through this framework,
we: (1) establish rigorous theoretical foundations for understanding human-agent collaboration in software
development; (2) provide developers with actionable guidance for selecting and implementing appropriate
development strategies; and (3) identify critical challenges and future directions spanning technical infrastructure,
security mechanisms, and human factors. This work serves as both a conceptual foundation for the emerging
field of AI-augmented software engineering and a technical roadmap for advancing research and practice in
coding agent systems.
The remainder of this paper is organized as follows. Section 2 reviews related surveys and foundational technolo-
gies relevant to Vibe Coding. Section 3 formally defines Vibe Coding and establishes its theoretical foundations
through a Constrained Markov Decision Process formalization. Section 4 surveys large language models for
coding, covering data foundations, pre-training techniques, and post-training methods. Section 5 examines LLM-
based coding agents, analyzing planning capabilities, memory mechanisms, action execution, and collaborative
architectures. Section 6 explores critical infrastructure components including isolated execution environments,
interactive development interfaces, and distributed orchestration platforms. Section 7 investigates feedback
mechanisms spanning compiler feedback, execution feedback, human feedback, and self-refinement. Section 8
presents our proposed taxonomy of five development models with analysis of their characteristics and applications.
Finally, Section 9 discusses future impacts and open challenges encompassing technical advancement, security
considerations, and human-centered design.




                                                         4
                                                           A Survey of Vibe Coding with Large Language Models



                                                                                Codex [35], MathPile [36], Arctic-SnowCoder [37], OpenCoder [38], Swal-
                                                   Data Foundation of




                     Large Language Mod-
                                                                                lowCode [39], WizardCoder [5], OctoPack [40], OpenCodeInstruct [41],




                      els for Coding (§ 4)
                                                   Code LLMs (§ 4.1)
                                                                                CodeArena [42], CodeUltraFeedback [43], Self-Instruct [44], etc.

                                                                                BERT [45], T5 [46], CodeBPE [47], GraphCodeBERT [48], CodeT5 [49], Code
                                              Pre-training Techniques (§ 4.2)   Llama [7], Birdie [50], Agent-Q [51], GPT-3 [1], CodeBERT [52], UniXcoder [53],
                                                                                CoDist [54], NatGen [55], PLBART [56], CodeT5+ [57], etc.

                                                                                VeriCoder [58], Flan-PaLM [59], FLAN [60], SparkRA [61], PanGu-Coder2 [62],
                                             Post-training Techniques (§ 4.3)   LoRA [63], Adapter Modules [64], LIMA [65], AlpaGasus [66], FinDPO [67],
                                                                                DPO [68], RAG-Gym [69], RLHF [70], DUMP [71], etc.

                                                                                Chain-of-Thought [72], AgentGen [73], ReAct [74], DPPM [75], HuggingGPT [76],
                                                 Planning and Decompo-
                                                                                Zero-shot-CoT [77], Auto-CoT [78], Tree of Thoughts [79], HyperTree Plan-
                                                 sition Capability (§ 5.1)
                                                                                ning [80], CodePlan [81], SQLucid [82], HQD [83], etc.

                                                                                Transformer [84], MMS [85], A-MEM [86], MemEngine [87], TaSL [88], Memory-
                                               Memory Mechanism (§ 5.2)
                     Coding Agent (§ 5)




                                                                                Bank [89], Generative Agents [90], Zero-Shot Planner [91], RET-LLM [92], etc.
                        LLM-based




                                                                                Toolformer [93], Large Knowledge Model [94], Alpha-UMi [95], MCP [96],
                                                 Action Execution (§ 5.3)       MCP-Zero [97], AutoTools [98], OpenHands [15], CodeAgent [99], RAIT [100],
                                                                                ScaleMCP [101], Doc2Agent [102], SE-Agent [103], AgentCoder [104], etc.

                                                                                Self-Refine [105], Saarthi [106], Repeton [107], Self-Planning [108], Pair-
       Vibe Coding




                                                     Reflection (§ 5.4)         Coder [109], Self-Debugging [110], Chained [111], TiCoder [112], ITDCG [113],
                                                                                Self-critique [114], N2M-RSI [115], ReVeal [116], ProCoder [117], RGD [118], etc.

                                                                                CoMAL [119], DRF [120], TeamMedAgents [121], AgentMesh [122], Hybrid [123],
                                               Agent Collaboration (§ 5.5)
                                                                                LMA [124], MASs [125], Agent Forest [126], Chatdev [10], MapCoder [127], etc.

                                                                                Virtual Earth Cloud [128], KUNERVA [129], FunDa [130], COCOS [131], SCHEMA
                                                   Isolated Execution
                                                                                lab [132], Singularity [133], DRIVE [134], MultiPL-E [135], TableGPT2 [136], SWE-
                     Environment (§ 6)




                                                     Runtime (§ 6.1)
                                                                                bench [11], SandboxEval [137], AutoSafeCoder [138], Secure SDLC [139], etc.
                       Development




                                                  Interactive Develop-          Designing PairBuddy [140], MultiMind [141], Language server protocol [142], Git
                                                  ment Interface (§ 6.2)        Context Controller [143], StackSpot AI [144], LSP [145], Opik [146], etc.

                                                                                TosKer [147], TOSCAdata [148], TORCH [149], AutoGen [150], Autogen [151],
                                                  Distributed Orchestra-
                                                                                AUTOGEN [152], CrewAI [153], MetaGPT [154], Microservices [155], XP [156],
                                                   tion Platform (§ 6.3)
                                                                                FogArm [157], Agentic [158], LLMOps [159], PharmaSwarm [160], EGI [161], etc.

                                                                                RLCF [162], CYCLE [163], AlphaTrans [164], RLEF [165], AceCoder [166], Vis-
                                                Compiler Feedback (§ 7.1)
                                                                                Coder [167], InterCode [26], The Art of Repair [168], Rtlfixer [169], etc.
                     Mechanisms (§ 7)




                                                                                PerfCodeGen [170], ExecutionAgent [171], TypeTest [172], ProjectTest [173], Py-
                                               Execution Feedback (§ 7.2)       Capsule [174], ASTER [175], CodeT [176], STROT [177], KPC [178], APT [179],
                        Feedback




                                                                                Seeker [180], TestGen-LLM [181], Healer [182], Agentic workflow [183], etc.

                                                                                Grounded Copilot [184], Cutting-Search [185], Deep Sets [186], MA-RLHF [187],
                                                Human Feedback (§ 7.3)
                                                                                ClarifyGPT [188], PPO [189], RLSF [190], CAGSR–vLLM–MTC [191], etc.

                                                                                CRITIC [192], BioAgents [193], Self-Organized Agents [194], Multi-Agent Col-
                                             Self-Refinement Feedback (§ 7.4)   laboration [195], LLM-Agent-UMF [196], SWE-Search [197], N-Critics [198], Self-
                                                                                Review Framework [199], SAMULE [200], Reflexion [201], etc.


Figure 1 The taxonomy of Vibe Coding is categorized into large language model foundations, coding agent architectures,
development environments, and feedback mechanisms. Each area encompasses specific techniques and frameworks that
collectively advance the systematic integration of LLMs and agents into intelligent and collaborative software development
workflows.


2     Related Work
2.1   Related Surveys
Foundational LLM. Several surveys have documented the evolution of large language models, covering LLM
architectures, training paradigms, and capabilities [202, 203]. These works examine Transformer variants with
a focus on efficient architectures and long-context capabilities [204–206]. The historical trajectory from BERT to
ChatGPT traces the development of foundation models, examining both opportunities and risks [207]. Specialized
surveys address evaluation methodologies, efficiency from model-centric and data-centric perspectives, and
specific capabilities including text generation and knowledge-enhanced PLMs [208].

In-Context Learning. Building on these architectural foundations, research has turned to techniques for utilizing
pre-trained models without additional training. Prompt engineering and in-context learning have emerged as
fundamental techniques, with taxonomies covering extensive prompting methods, applications, security considera-
tions, and performance across Natural Language Processing (NLP) tasks [209–211]. In-context learning mechanisms


                                                                                          5
                               A Survey of Vibe Coding with Large Language Models



are explored with context engineering emerging as a formal discipline [212, 28]. Chain-of-Thought (CoT) reasoning
has proven particularly effective, with taxonomies examining Chain-of-X paradigms and investigating long CoT
and multimodal CoT reasoning [213–215]. Multimodal large language models represent a rapidly advancing
frontier, with surveys examining architectures, training methods, and vision-language integration across multiple
data modalities [216–219].

Post-Training. When in-context learning proves insufficient, post-training methods offer pathways to align
models with specific requirements and enhance reasoning capabilities. Reinforcement learning approaches,
including Proximal Policy Optimization (PPO), Q-Learning, and Actor-Critic methods, have been surveyed with
particular emphasis on Reinforcement Learning from Human Feedback (RLHF), Reinforcement Learning from
AI Feedback (RLAIF), and Direct Preference Optimization (DPO) [220–224]. Instruction tuning and supervised
fine-tuning methodologies are reviewed covering dataset construction and training strategies, with examinations
of data selection approaches for enhanced instruction-following capabilities [225]. Alignment research categorizes
methods into outer and inner alignment with adversarial considerations, while exploring training-free alignment
and personalized alignment techniques [226]. DPO emerges as an reinforcement learning RL-free alternative
to RLHF, with taxonomies categorizing data strategies, learning frameworks, and constraint mechanisms [227].
Post-training paradigms are explored covering fine-tuning, alignment, reasoning, efficiency, and domain adaptation,
with parameter-efficient methods including Low-Rank Adaptation (LoRA) and adapters providing experimental
comparisons of computational overhead [228].

Agent Systems. The integration of tool use and planning capabilities transforms LLMs from passive models
into active agents. Foundational surveys establish frameworks covering agent construction, brain-perception-
action architectures, and autonomous decision-making capabilities, while providing unified taxonomies across
benchmarks spanning reasoning and code generation [229–231]. Multi-agent systems are examined covering agent
profiling, communication protocols, and collaborative workflows across complex task-solving scenarios [232, 233].
Agent capabilities are addressed through specialized surveys: tool use with Retrieval-Augmented Generation
(RAG) and feedback learning [234, 235], planning mechanisms including task decomposition and memory [221],
single and multi-agent architectures for reasoning and tool execution, and memory mechanisms with short-term
and long-term analysis [236]. Evaluation methodologies cover planning, tool use, self-reflection, and application-
specific benchmarks [237, 238]. Domain-specific applications span web automation [239], scientific discovery across
life sciences and materials science [240], Operating System agents with GUI interaction [241], and self-evolving
agents with feedback loops and lifelong learning capabilities [242]. Of particular relevance to this work, recent
surveys examine coding agents with single and multi-agent architectures across the software development lifecycle,
covering planning, context management, and tool integration with benchmarking frameworks [243, 244].

2.2   Preliminary
Reinforcement Learning for Code Generation. Applying reinforcement learning to code generation requires
executable feedback signals, evolving from basic mechanisms to sophisticated training paradigms. Early approaches
combine pretrained language models with deep RL using unit test feedback and critical sampling, achieving strong
performance on competitive benchmarks [245]. Execution-based methods leverage PPO with compiler feedback
for real-time refinement [246]. Advanced RL frameworks employ multi-granularity unit test feedback [247],
break generation into curriculum subtasks with fine-grained optimization [248], use ranking-based alignment
mechanisms [62], and leverage Group Relative Policy Optimization with compiler feedback to achieve competitive
performance [249].

Autonomous Coding Agent Systems. Beyond supervised generation, autonomous agents tackle complete soft-
ware engineering tasks through specialized architectures and multi-agent collaboration. Single-agent systems
introduce custom agent-computer interfaces achieving strong benchmark performance [12], combine structure-
aware code search with spectrum-based fault localization for cost-effective issue resolution [13], and demonstrate
that simple hierarchical localization can outperform complex agents [14, 250]. Repository-level code generation
integrates programming tools with agent strategies showing substantial improvements [99, 251], while itera-
tive retrieval-generation approaches improve baselines on repository evaluation benchmarks [251]. Multi-agent
frameworks employ specialized roles across the development process. These assign distinct programmer, test
designer, and test executor agents achieving high pass rates with reduced token consumption [104], encode



                                                        6
                                 A Survey of Vibe Coding with Large Language Models



standardized operating procedures into assembly-line paradigms with role-based collaboration achieving near-
perfect task completion [252], and implement chat chain architectures with dual-agent communication covering
the full software development lifecycle at minimal cost [10]. Specialized frameworks replicate human program-
ming cycles [127], investigate test-driven development principles showing consistent improvements with upfront
test provision [253], and analyze self-repair mechanisms revealing modest performance gains bottlenecked by
self-feedback abilities [110].

Function Calling. Effective agent systems require mechanisms for tool use, function calling, and execution
infrastructure to interact with external systems and APIs. Function calling frameworks teach language models
to self-supervise tool use with simple APIs requiring minimal demonstrations [93], use teacher models for tool-
related instruction data generation [254], and employ multi-task learning on granular tasks with large-scale API
datasets [255]. Execution and interaction environments provide lightweight RL frameworks with safe execution
for multiple programming languages [26], use executable code as unified action space outperforming alternative
formats with specialized instruction datasets and fine-tuned models [256], and integrate Monte Carlo Tree Search
with external feedback for deliberate problem-solving [257]. Optimization and deployment advances automatically
identify parallelizable function calls achieving significant latency speedup and cost savings [258], enable edge
deployment with compact models matching large model capabilities locally [259], and coordinate specialized
agents for tool selection, execution, and calibration achieving higher success rates [150]. Retrieval, evaluation, and
infrastructure contributions provide large-scale benchmarks showing retrieval from diverse datastores significantly
improves performance [260], decompose tool use capability into evaluation aspects for API manipulation [261],
develop multi-agent systems for code review automation achieving strong results on critical review tasks [150],
enable customizable conversable agents programmed in natural or code language [150], and provide massive
instruction-API pair datasets demonstrating cross-language transfer enabling open-source models to outperform
proprietary alternatives on new API calls [262].

Supervised Fine-Tuning. An alternative to reinforcement learning lies in supervised fine-tuning and instruction
tuning methods, which have become foundational for code model training. Instruction evolution approaches
iteratively evolve code instructions achieving competitive performance [5], while self-instruction methods bootstrap
instruction-following capabilities [44]. Fully transparent self-alignment pipelines enable training without propri-
etary distillation [263], and large-scale instruction datasets combine multiple instruction generation approaches [41].
Specialized tuning addresses security-centric generation improving code security substantially [264], optimization
code generation [265], and code editing, debugging, and refinement through self-debugging approaches and itera-
tive refinement without additional training [110, 105, 266]. Foundation models for code employ repository-level
pretraining with extended context windows [267], train on diverse languages with fill-in-the-middle objectives
and PII redaction [6], incorporate GitHub issues and documentation with repository-level training [268], and
achieve competition-level performance using massive sampling and filtering strategies [269].

3     Vibe Coding: The Engineering of Managing Coding Agents
3.1    Definition of Vibe Coding
In this paper, we define Vibe Coding as an engineering methodology for software development grounded in large
language models [18–21, 270]. At its core, as shown in Figure 2, it represents a dynamic triadic relationship
among human developers, software projects, and Coding Agents. In this paradigm, humans evolve from
direct code authors into intent articulators, context curators, and quality arbiters. Projects extend beyond static
code repositories to become multifaceted information spaces encompassing codebases, databases, and domain
knowledge. Coding Agents, as intelligent executors, perform code generation, modification, and debugging under
the dual guidance of human intent and project constraints.

Formalization of the Triadic Relationship. We model Vibe Coding as a dynamic interactive system defined by
the triple V = ⟨H, P , Aθ ⟩, where:
      • H: Human developer, equipped with requirement cognition capability Hreq : D → I (translating domain
        requirements D into instructions I ) and quality discrimination capability Heval : O → {0, 1} × F (judging
        outputs O with accept/reject decisions and feedback F ),



                                                          7
                                     A Survey of Vibe Coding with Large Language Models



                                                                  Project


                                     Codebase                                           Domain Knowledge

                                     Database                                          Execute Enviroment
     Results




                                                                                                                               Context
                                          Review




                                                                                               Coding
                 Focus on results,                                                                      Coding with project-
                 not code details                               Vibe Coding                               specific context



                 Idea                                                                                              Tools
                                                                Instruction
               Evaluation                                                                                         Memory

               Discussion                                        Feedback                                          Tasks

                    Developer                                                                              Coding Agent

Figure 2 Vibe Coding Overview. A triadic collaboration among developer, coding agent, and project, where iterative
instruction–feedback loops enable context-aware coding and result-oriented review.


   • P : Software project, represented as a project context space P = ⟨Ccode , Cdata , Cknow ⟩, corresponding to
     codebase, database, and domain knowledge respectively,
   • Aθ : Coding Agent, a large language model parameterized by θ, executing the conditional generation function
     Aθ : I × P × E → O .
The collaboration among the three parties can be modeled as a Constrained Markov Decision Process (Constrained
MDP) [34], wherein humans define the goal space and constraint boundaries, projects provide the state space and
transition constraints, and Agents execute policies and state transitions:


                                             VMDP = ⟨SP , AH→Aθ , TAθ |P , RH , γ⟩,                                                (1)

where the state space SP is defined by the project’s current state, the action space AH→Aθ is triggered by human
instructions to Agent behaviors, the transition function TAθ |P is constrained by project specifications, the reward
function RH is determined by human evaluation, and γ is the discount factor.

Agent’s Conditional Generation Process. Given human intent I , project context K ⊆ P (a relevant subset
retrieved from the project information space), and execution environment E , the Agent generates code sequence
Y = (y1 , . . . , y T ) in an auto-regressive manner, with joint probability factorized as:

                                                                          T
                                                   Pθ (Y |I , K, E ) = ∏ Pθ (yt |y<t , Ct ),                                       (2)
                                                                       t =1

where Ct = A(I , K, E , y<t ) denotes the dynamic context at step t, orchestrated by the high-level assembly function
A. Context components ci correspond to distinct information sources from the triadic relationship:
Human Layer:
   • cinstr : System instructions and task requirements.
Project Layer:
   • ccode : Codebase (source code, API interfaces, architectural design),
   • cdata : Database (persistent data, data schemas),


                                                                      8
                                         A Survey of Vibe Coding with Large Language Models



                                                                                                                     PyCapsule      MutaGReP
         Code World Model                                                         AgentPack
                               Qwen3-Coder                     Codex Agent                         DeepSWE            Seed-CTS       CodeSim
  2025                                       Qwen Code CLI                         MLE-Dojo                                           GenX
                               Code-R1                         Gemini CLI                          SWE-smile        SRA-MCTS
           Codestral 25.01                                                                                        RethinkMCTS        PF-PPO
                                               Claude Code                   SWE-bench Live
                                                                                                    R2E-Gym            RLCoder       PlanSearch
           Qwen2.5-Coder       OpenCoder                       ExecutionAgent
                                                   Agentless
                                                                                                     RLHF for Code Completion
                               DeepSeek-Coder V2               SWE-agent           SWE-Gym                                            RLAIF
              SantaCoder2                  AutoCodeRover                                           SWE-bench+
  2024                                                                 SWE-bench Multimodal                                LDB
                                DeepSeek-Coder                                                      MLE-bench                        LeDex
                                                               MAGIS                                                RLPF&DPA
              Code Llama                                                            DA-Code
                               Magicoder           AutoDev     RepoAgent                           COFFEE-GYM                        TGen
             WizardCoder                           CodeAct                        OpenHands                           StepCoder
                               CodeGemma                       CodeAgent                           BigCodeBench
                                                                                                                                    AgentCoder
  2023          CodeT5+                          AgentCoder                     EvoCodeBench                      INTERVENOR
                                StarCoder                      MetaGPT                              SWE-agent                        B-Coder
              SantaCoder                                                                R2E                               RLTF
                                                   ChatDev                                         LiveCodeBench
                                CodeGen                                                                                              InterCode
                                                                AutoGPT             CodeAct                       Self-Debugging
              AlphaCode
                                                   Reflexion                      SWE-bench        ML-Bench
                PLBART          CodeT5                                                                                Reflexion
                                                                                                                                     PPOCoder
  2022

           Implementation            Coding LLMs
                                     Coding Agents                                    APPS           MBPP                          REDCODER
              Open Resource
                                   Coding Environment                                          HumanEval
              Close Resource                                                                                           CompCoder
                                        Feedback

Figure 3 Vibe Coding Evolution Timeline: A comprehensive visualization of the development trajectory of Vibe Coding
implementations from 2022 to 2025, showing the evolution from foundational Coding LLMs to sophisticated coding agent
systems, execute environments and Feedback mechanism.


   • cknow : Domain knowledge (documentation, specifications, best practices).
Agent Layer:
   • ctool : Definitions and signatures of callable tools (compilers, testing frameworks, version control),
   • cmem : Historical interaction memory (multi-turn dialogue context, prior decision records),
   • ctasks : Current tasks (pending actions, task queue, execution status).

Optimization Objective of Vibe Coding. From the triadic perspective, the core challenge of Vibe Coding is to
identify optimal context orchestration strategies F ∗ = {A, Retrieve, Filter, Rank} that maximize generation quality
within the limited context window Lmax . Defining a reward function R : O × O ∗ → R that measures alignment
between generated outputs and human expectations, given task distribution T , the optimization objective is:


                               F ∗ = arg max Eτ ∼T [ R( Pθ (Y |CF (τ )), Yτ∗ )] s.t. |CF (τ )| ≤ Lmax                                          (3)
                                               F

where CF (τ ) represents the context retrieved and filtered from project P by strategy F for task τ, and Yτ∗
denotes the ideal output in the human’s mental model. This optimization problem essentially seeks the subset
with maximum information gain for Agent generation from the exponentially large candidate set in the project
information space.

Human-Agent Collaborative Loop and Task Evolution. The central mechanism of Vibe Coding is human
guidance through continuous feedback to steer the Agent toward project objectives, with explicit support for
humans to iteratively expand constraints and introduce new tasks, forming a dynamically evolving requirement
space. Let the Agent produce output ok ∈ O at iteration k. The human supervision function H : O × R × I →
2O × (F ∪ Inew ), constrained by execution results R and current instructions Ik , returns an acceptance subset
Ak ⊆ ok and a correction signal δk . The iterative evolution is expressed as:




                                                                      9
                                 A Survey of Vibe Coding with Large Language Models



                              
                              (ok , Ik )
                                                                       if Ak = ok (full acceptance, terminate)
              (ok+1 , Ik+1 ) = (Aθ (ok \ Ak ; δk , Ik , K), Ik )        if δk ∈ F (local refinement)                  (4)
                              
                                (Aθ (Ik ∪ {δk }, K), Ik ∪ {δk })        if δk ∈ Inew (requirement expansion)
                              

where (Ak , δk ) = H(ok , Rk , Ik ) with Rk denoting the execution feedback obtained from running ok in environment
E.

Formalization of Iterative Task Expansion. Distinct from conventional software development paradigms where
requirements are frozen early, Vibe Coding supports incremental evolution of requirements. We define the task
evolution trajectory as an instruction set sequence {I0 , I1 , . . . , IK }, where I0 represents the initial requirements
and each expansion satisfies monotonicity Ik ⊆ Ik+1 . The k-th expansion is formalized as:

                                                                       (1)   (2)      (m )
                                         Ik+1 = Ik ⊕ ∆Ik = Ik ∪ {δk , δk , . . . , δk k }                             (5)

where ⊕ denotes the instruction merging operator, ∆Ik represents the instruction set added at step k, and mk is
the number of tasks introduced in this expansion. The cumulative task count throughout the development process
is |IK | = |I0 | + ∑kK=−01 mk . This multi-expansion mechanism embodies two key characteristics: (1) Progressive
Requirement Clarification: Humans need not exhaustively plan all details initially, but can progressively refine
constraints upon observing Agent outputs. This reflects the cognitive reality that complex system requirements
often crystallize through interactive exploration rather than upfront specification. (2) Dynamic Constraint
Reinforcement via Feedback: When Agent outputs expose implicit requirements or boundary cases, humans can
immediately supplement constraints. This interactive requirement discovery process enables adaptive specification
refinement aligned with emergent understanding.
Formally, we model the entire development cycle as a multi-stage optimization problem, where each stage k
corresponds to a task space Ik :

                                     K
                            max ∑ ωk · R(ok , YI∗k )       s.t.    ok = Aθ (Ik , K, E ),     I k ⊆ I k +1             (6)
                           {ok }kK=0 k=0

where ωk is the weight factor for stage k, and YI∗ denotes the ideal output for that stage. This formulation
                                                  k
captures the essence of Vibe Coding: through sustained human intervention and dynamic expansion of the task
space, the system progressively converges toward the ultimate software objective.
This iterative and expansive mechanism embodies the core philosophy of Vibe Coding: Humans govern “What”
(defining the right problems, with problems allowed to evolve dynamically) and “Why” (judging solution
appropriateness); Projects define “Where” (constraining the solution space boundaries); Agents manage “How”
(exploring technical implementation pathways). The synergy of these three entities constitutes a self-adaptive,
requirement-evolvable closed-loop software development system.

3.2   Why Vibe Coding
Vibe Coding transforms software development from passive assistance to collaborative partnerships, addressing
challenges in democratization, workflow efficiency, and ecosystem expansion.

Team-Scale Capabilities for Individual Developers. Vibe Coding enables individual developers to deliver
team-scale capabilities. Production applications traditionally require coordinating frontend, backend, database,
security, DevOps, and QA specialists with substantial overhead. Coding agents provide diverse expertise across
domains [10, 150, 271]. Developers focus on requirements while agents implement across stacks [272]. This reduces
learning overhead through context engineering. Individual developers now implement cloud infrastructure and
performance optimizations without formal training, benefiting resource-constrained entities by compressing
prototypes from weeks to days.




                                                                  10
                                A Survey of Vibe Coding with Large Language Models




                 Large Language Model for Coding
                                                                                                Code Generation


                                                                                              Code Understanding


                                                                                                 Bug Detection

          Data Foundation            Pre-training              Post-training                   Code Optimization



Figure 4 Large Language Model for Coding: Overview of the training lifecycle encompassing Data Foundation, Pre-training,
and Post-training stages, with core capabilities including Code Generation, Code Understanding, Bug Detection, and Code
Optimization.


Continuous Development and Quality Convergence. Vibe Coding aims to balance development velocity and
code quality—historically conflicting objectives. Traditional workflows trade delivery speed against testing rigor
[273]. Vibe Coding can improve both through autonomous iteration decoupled from human constraints. Agents
sustain 24/7 operation: automated testing, refactoring, and performance profiling [274]. Automating mechanical
tasks liberates cognitive resources for design and optimization [275, 13]. Agents enable exhaustive exploration
through rapid iteration [201, 105] while human oversight validates architectural decisions.

Broadening the Software Creator Ecosystem. Vibe Coding democratizes development by lowering technical
barriers. Traditional development required extensive programming knowledge before implementing ideas. Natural
language becomes the primary creation interface [4, 5, 1]. Domain experts—medical practitioners, educators,
designers—articulate needs without computer science education [35]. This diversifies innovation sources, materi-
alizing underrepresented perspectives [276, 90]. Economic impact manifests through creator economy expansion:
domain experts monetize specialized tools without technical co-founders. This parallels previous democratization
waves, representing software literacy’s evolution from specialized skill to broadly accessible capability [277].

4     Large Language Models for Coding
4.1     Data Foundation of Code LLMs
4.1.1    Pre-training Code Corpora
Code LLMs require large-scale training data from diverse sources [35, 278]. These models rely on large-scale code
corpora primarily sourced from open platforms like GitHub and Stack Overflow, with quality filtering based on
metrics such as repository stars, documentation completeness, and community engagement [279].
Training datasets vary significantly in composition and curation strategies, with two primary approaches emerging:
depth-focused strategies that concentrate on popular languages for quality, and breadth-focused strategies that
span diverse languages for coverage [280, 281]. The Stack dataset uses the depth-focused approach, providing 3.1
TB of permissively licensed source code across 30 programming languages with careful attention to licensing and
data provenance [36, 282, 37], while CodeParrot similarly trains exclusively on GitHub code to achieve depth in
popular languages [278]. In contrast, breadth-focused approaches span diverse languages for maximum coverage.
The Stack v2 expands coverage substantially to 67.5 TB across 619 programming and markup languages [37, 38],
GPT-Neo utilizes diverse mixed corpora including "the Pile" [278], while CodeLlama employs SlimPajama’s 627
billion tokens paired with code from The Stack [282] and Arctic-SnowCoder uses a filtered combination yielding
400 billion tokens [37].
Data quality has driven sophisticated processing pipelines, with RefineCode incorporating over 130 carefully
crafted language-specific filtering and cleaning rules across 607 languages to ensure syntactic and semantic validity
[38], and SwallowCode implementing comprehensive four-stage pipelines performing syntax validation, quality
assessment, deduplication, and LLM-based rewriting to enhance training data quality [39].


                                                          11
                                   A Survey of Vibe Coding with Large Language Models



4.1.2    Instruction & Preference Datasets
Beyond raw code corpora, instruction-following requires curated training data. Accordingly, code LLMs have
demonstrated exceptional capabilities across diverse programming tasks [279, 5], with instruction tuning as a
critical technique for enhancing instruction-following abilities and solution generation quality [5]. These instruction
datasets are typically compiled from two primary sources: permissively licensed source code repositories and
synthetically constructed instructional data [279]. Notable instruction datasets in the field include CommitPack
with its impressive 4 TB of raw data carefully filtered to 2GB of high-quality code paired with commit message
instructions that capture developer intent [40], OpenCodeInstruct as the largest openly available dataset with 5
million diverse samples covering multiple programming languages and task types [41], and SynCode-Instruct
providing nearly 20 billion tokens of synthetic instruction-following examples [42]. For preference learning
applications, CodeUltraFeedback provides 10,000 coding instructions each paired with four distinct responses
from 14 different LLMs, all evaluated comprehensively by GPT-3.5 to establish quality rankings [43], while the
PLUM Framework innovatively employs GPT-4-generated unit tests to establish automated preference rankings
based on functional correctness [283].
High-quality instruction dataset construction methodologies have evolved significantly from expensive and
time-consuming human annotation processes toward more scalable synthetic generation approaches that maintain
quality while reducing costs [41, 2]. The Self-Instruct paradigm pioneered the approach of bootstrapping from
limited seed examples, using language models to generate new instructions through carefully designed instruction-
input-output pipelines [44], while Evol-Instruct introduced the concept of progressive complexity increase by
iteratively rewriting and enhancing initial instructions to create more challenging and diverse training examples
[284]. OSS-Instruct advances the field by systematically integrating real-world open-source code snippets as seeds
for generating diverse, contextually realistic instruction data that better reflects actual programming scenarios [285].
Quality enhancement techniques have become sophisticated, employing approaches like CoachLM’s LLM-based
iterative rewriting to improve instruction clarity and task alignment, and CaR (Critique and Revise) approaches
that use specialized scoring models aligned with expert preferences to filter and refine synthetic data, with the
effectiveness of these synthetic data approaches demonstrated by systems like Nvidia’s Nemotron-4 achieving
state-of-the-art performance using 98% synthetically generated alignment data [286].

4.2     Pre-training Techniques
4.2.1    Pre-training Objectives
Large language models for code leverage transfer learning paradigms inherited from BERT and GPT architectures
[45, 287, 207, 47, 46], with pre-training on large-scale data before task-specific fine-tuning proving particularly
effective where LLMs outperform domain-specific models in limited labeled data scenarios [47]. Code-specific
pre-training objectives surpass traditional masked language modeling approaches, with innovations including
GraphCodeBERT’s data flow prediction that captures semantic relationships in code [47, 48] and variable naming
tasks in CodeT5 and DOBF that leverage programming language structure [47, 49, 7].
Pre-training serves the fundamental purpose of instilling general-purpose knowledge and pattern recognition
capabilities from large-scale unlabeled datasets [50, 51], with several well-established paradigms dominating the
landscape. Autoregressive language modeling predicts the next token in a sequence based on all previous context
[288, 51], while masked language modeling focuses on predicting randomly masked tokens using both preceding
and following context for bidirectional understanding [288, 51]. Alternative objectives that have gained traction
include infilling tasks that predict missing spans within sequences and prefix language modeling that generates
continuations from given prefixes [50].
Masked Language Modeling is the dominant approach for code understanding tasks, building directly on BERT’s
remarkable success in natural language processing [289, 53, 45]. This approach is primarily adopted by encoder-
only models like CodeBERT, which utilizes RoBERTa-based architectures for bidirectional code understanding [52].
The standard implementation samples approximately 15% of input tokens, with 80% of selected tokens replaced
by a special [MASK] token to enable bidirectional context-based prediction [53].
Implementation details vary across models, with CodeBERT applying MLM augmented with Replaced Token
Detection to improve robustness [54, 290, 52], while GraphCodeBERT extends this with structure-aware features
discussed below [48].
Autoregressive language modeling serves as the foundational approach for code generation tasks by predicting the


                                                          12
                               A Survey of Vibe Coding with Large Language Models



next token based solely on preceding context [289]. Decoder-only models like CodeGPT effectively leverage GPT
architecture’s powerful Transformer-based decoders for this purpose [291, 45]. Recent models like CodeLlama
have extended this paradigm through innovative fill-in-the-middle objectives that enable models to generate
missing code segments given both prefix and suffix contexts, proving valuable for code completion tasks [292, 293].
In contrast to unidirectional prediction, denoising objectives have proven highly effective for encoder-decoder
architectures through span-level reconstruction tasks [53]. PLBART first applied denoising approaches to code by
building on BART’s sequence-to-sequence architecture [55, 56, 290, 294], while modern unified models increasingly
adopt sophisticated denoising strategies in comprehensive multi-task frameworks exemplified by CodeT5+ which
synergistically combines span denoising with contrastive learning objectives [57, 203].
Structure-aware objectives incorporate the unique structural characteristics inherent to programming languages,
including abstract syntax trees, control flow graphs, and data flow relationships [52, 45]. GraphCodeBERT
incorporates data flow graphs that explicitly encode semantic relationships between variables across code segments
[47, 48], while introducing specialized structure-aware tasks such as code structure edge prediction that require
understanding syntactic and semantic code organization [295, 48]. Contrastive learning explicitly minimizes
representation distance between semantically similar code functions while simultaneously maximizing distance
between dissimilar code, and is a powerful technique for training code models [296, 297]. UniXcoder uses this
approach through sophisticated multi-modal contrastive learning that unifies natural language comments and
linearized abstract syntax tree representations into a shared semantic space [53, 298], while ContraCode leverages
automated compiler transformations to generate semantically equivalent code variations for robust contrastive
data augmentation [296]. Multimodal pre-training strategies leverage multiple complementary data modalities to
enhance model capabilities, with CodeBERT first learning general-purpose code representations through carefully
aligned bimodal natural language-programming language pairs [52, 53, 295, 294], while advanced models like
CodeT5+ implement sophisticated two-stage training procedures involving initial unimodal pre-training on
massive code-only data to establish programming knowledge, followed by bimodal pre-training on carefully
curated code-text pairs with explicit cross-modal alignment learning to bridge natural and programming languages
[57, 279].

4.2.2   Continual Pre-training Strategies
Continual pre-training (CPT) enables models initially pre-trained on broad general corpora to undergo additional
rounds of training on new, often domain-specific datasets, representing an important paradigm [316]. This approach
enables models to acquire substantial new knowledge in specialized domains such as coding, mathematics, or
scientific reasoning while preserving and building upon existing foundational capabilities [316], with research
demonstrating that LLMs possess inherent abilities to effectively accumulate and retain knowledge across sequential
training tasks [317, 1].
The code domain is one of the most successful application areas for continual pre-training strategies. CodeLlama
demonstrates this success by leveraging CPT on the general-purpose LLaMA2 foundation model to achieve
state-of-the-art code generation performance [318, 249], while DeepSeek-Coder-V2 shows more advanced CPT
capabilities by continuing training from DeepSeek-V2 intermediate checkpoints with an additional 6 trillion tokens,
resulting in substantial enhancements to both coding abilities and mathematical reasoning capabilities [318, 249].
Critical to effective CPT are sophisticated data mixing strategies that carefully balance different data types and
domains, with Qwen2.5-Coder’s systematic experimentation determining optimal 7:2:1 mixing ratios for code,
text, and mathematics data, resulting in over 20% average performance improvement compared to code-only
training approaches [318].
However, preventing catastrophic forgetting of previously learned knowledge remains a central challenge in
CPT [319–321]. This is addressed through strategies such as DeepSeek’s approach of replaying 30% of original
pre-training data during continual training phases to maintain performance on previously mastered tasks [318],
with replay-based methods being a well-established approach for mitigating catastrophic forgetting [322].
Critically, data selection for continual pre-training leverages both distributed corpus features and linguistic
characteristics to identify the most valuable training examples [323–325], with empirical research demonstrating
that CPT on appropriately selected unlabeled task data and augmented unlabeled data sampled from in-domain
corpora can significantly enhance end-task performance [323, 326]. Critical CPT challenges that remain active
research areas include the "stability gap" phenomenon where models experience temporary but significant
performance drops at the onset of new domain data training before eventually recovering and surpassing


                                                        13
                                              A Survey of Vibe Coding with Large Language Models


Table 1 Overview of Representative Coding Datasets for Training and Evaluation.

                           Release Date/                  Languages/                Data Collection                              Characteristics/                     Level/
 Dataset
                           Scale                          Task Types                Method                                       Purpose                              Attributes

 SWE-Gym [299]             2025; ~2.4k tasks, includ-     Python; project-level     Collected from real pull requests in 11      Contains complete code con-          Project-level,
                           ing 230 lightweight in-        bug fixing and editing    open-source Python projects with exe-        text, executable test environ-       with     repository
                           stances                        tasks                     cutable environments and unit tests          ments, and unit tests; suitable      context, directly
                                                                                                                                 for training RL coding agents        executable
 Codeforces-CoTs [300]     2025; ~10k Codeforces          C++ and Python com-       Collected 10k+ problems from Code-           Problems accompanied by              Problem-level;
                           problems, ~100k total sam-     petitive programming      forces, using DeepSeek R1 to gener-          model-generated code and             includes multiple
                           ples, ~9.69GB                  problems with chain-      ate up to five reasoning trajectories per    reasoning trajectories; ~84%         subsets (solutions,
                                                          of-thought                problem                                      Python solutions pass public         solutions_w_edi-
                                                                                                                                 tests                                torials, etc.)
 SWE-Fixer [301]           2025; 110k high-quality        Multi-language,     in-   Utilized GitHub events to crawl issue-       Each instance contains issue         File-level     and
                           samples filtered from 2.3k     cluding code retrieval    PR pairs, limited to three files or fewer,   description, code context, and       project-level;
                           repositories and 331k in-      and editing               removed parsing errors, generated chain-     patches; suitable for super-         includes chain-of-
                           stances                                                  of-thought                                   vised and RL training on re-         thought
                                                                                                                                 trieval/editing tasks
 KodCode [302]             2024;     447k      problem-   Synthetic algorithmic/-   Generated through multi-stage pipeline:      All problems equipped with           Function-level;
                           solution-test triples          coding exercises          problem synthesis, solution generation,      verifiable unit tests, covering      fully   synthetic,
                                                                                    unit test creation, and post-processing      various difficulty levels; suit-     emphasizes test
                                                                                                                                 able for SFT and RL training         executability
 Code-R1 [303]             2025; 12k RL samples (2k       Programming     prob-     Selected from LeetCode and TACO ver-         Emphasizes sandbox execution         Function-level;
                           LeetCode + 10k filtered        lems for RL training      ified instances with reliable tests, pro-    for reward verification, avoids      each      contains
                           from TACO)                                               viding prompts and unit tests                test noise; directly usable for      prompt and tests
                                                                                                                                 GRPO optimization
 Z1-Code [304]             2024; 107k coding prob-        Multi-language coding     Filtered from public problem sets and        Provides two reasoning depths        Problem-level; in-
                           lems                           problems with both        synthetic problems, annotated with           to improve model generaliza-         cludes solutions
                                                          short and long reason-    short-chain and long-chain reasoning         tion and avoid over-thinking         and reasoning
                                                          ing trajectories
 rStar-Coder [305]         2024; 418k competitive         Multi-language com-       Aggregated existing competitive prob-        Each problem has verification        Problem-level; in-
                           problems and 580k long-        petitive programming      lems and synthesized new ones, gen-          tests and in-depth reasoning so-     cludes tests and
                           reasoning solutions            problems                  erated input-output tests and long-          lutions; suitable for training in-   reasoning
                                                                                    reasoning solutions                          terpretable coding models
 LeetCodeDataset [306]     2025; 2,613 training prob-     Python LeetCode algo-     Wrapped LeetCode problems into data          Each problem provides com-           Function-level;
                           lems and 256 test problems     rithmic problems          structures containing imports, entry_-       plete unit tests and target code;    includes Python
                                                                                    point, tests, completion, examples, and      suitable for model training and      test scripts
                                                                                    metadata                                     evaluation
 OpenCodeReasoning [307]   2024; 735,255 samples cov-     Multi-language pro-       Integrated data from 11 programming          Large-scale high-quality pro-        Problem-level;
                           ering 28,319 programming       gramming problems         platforms and generated solutions using      gramming reasoning data; sup-        includes problem
                           problems                       with reasoning            NVIDIA R1                                    ports training models with rea-      text,     solutions,
                                                                                                                                 soning capabilities                  and reasoning
 DeepCoder [308]           2025; 24k verified coding      Competitive program-      Merged TACO verified, Prime Intellect        Provides fully open high-            Problem-level; in-
                           problems, each with ≥5         ming problems             synthetic problems, LiveCodeBench, etc.,     quality data for RL training; re-    cludes complete
                           test cases                                               filtered to 24k problems with complete       ward uses binary model (pass/-       test sets
                                                                                    tests                                        fail)
 SWE-Bench Variants
                           Since 2023; Full: 2,294,       Primarily      Python,    Collected issues and PRs from GitHub,        Instances include problem            Project-level; used
 [11, 309, 310]
                           Lite: 300, Verified: 500,      also multi-language       recording base commits, patches, and         descriptions, base commits,          for      evaluating
                           Multimodal: 617, Multilin-     versions; project-level   test patches; some instances expert-         patches, tests, and metadata;        bug-fixing capa-
                           gual: 300                      issue resolution          verified                                     Multilingual version extends         bilities of coding
                                                                                                                                 to 9 languages                       agents
 Multi-SWE-Bench [311]     2025; 1,632 high-quality in-   Seven languages: Java,    Five-stage process: repository selection,    Fills the Python-only gap            Project-level; used
                           stances                        TypeScript, JavaScript,   PR crawling, environment determination,      in SWE-Bench; cross-language         for evaluation
                                                          Go, Rust, C, C++          PR filtering, and human validation           evaluation for coding agents
 MLE-bench [312]           2024; 75 Kaggle competi-       Multi-language; ML        Curated from Kaggle competitions cov-        Challenging tasks testing real-      Competition-
                           tions, 3.3TB dataset           engineering tasks in-     ering various domains (NLP, CV, signal       world ML engineering skills;         level; open-ended
                                                          cluding model train-      processing), with human baselines from       includes competitions like           and difficult tasks
                                                          ing, dataset prepara-     public leaderboards                          COVID-19 vaccine prediction          for     evaluating
                                                          tion, and experiments                                                  and ancient scroll deciphering       autonomous ML
                                                                                                                                                                      engineering
 PaperBench [313]          2025; 20 ICML 2024 pa-         Multi-language;     AI    Selected 20 Spotlight and Oral pa-           Evaluates agents’ ability to         Research-level; hi-
                           pers, 8,316 individually       research   replication    pers from ICML 2024, with rubrics co-        replicate cutting-edge AI re-        erarchical rubrics
                           gradable tasks                 tasks                     developed with original paper authors        search from scratch, includ-         decompose tasks
                                                                                                                                 ing understanding contribu-          into fine-grained
                                                                                                                                 tions, developing codebases,         sub-tasks
                                                                                                                                 and executing experiments;
                                                                                                                                 uses LLM-based judge for au-
                                                                                                                                 tomated grading
 Terminal-Bench [314]      2025; 80 tasks                 Multi-language; termi-    Hand-crafted and human-verified tasks,       Evaluates agents on complete,        System-level; cov-
                                                          nal environment tasks     each with dedicated Docker environ-          end-to-end tasks in terminal en-     ers diverse termi-
                                                                                    ment, human-verified solutions, and test     vironments including scientific      nal behaviors, di-
                                                                                    cases                                        workflows, network configura-        rectly executable
                                                                                                                                 tion, data analysis, API calls,      in sandboxed en-
                                                                                                                                 and cybersecurity; emphasizes        vironments
                                                                                                                                 real-world complexity
 SWE-RL [315]              2024; aggregated 24M PR        Multi-language    bug     Crawled      GitHub     events     from      Uses difflib as reward function;     Project-level; mas-
                           instances and cloned 4.6M      fixing tasks              GHArchive (2015-2024), aggregated PRs        used for training large models       sive scale
                           repositories                                             and used heuristics to select bug-fixing     like Llama3-SWE-RL
                                                                                    seeds; each instance contains problem
                                                                                    description, code context, and patches




previous performance levels [327], the persistent issue of catastrophic forgetting of previous knowledge though
research indicates self-supervised CPT approaches tend to outperform supervised protocols in knowledge retention
[317, 1, 328], and the fundamental difficulty of scaling CPT methods to scenarios with small limited-token corpora
where the restricted diversity of training examples significantly hinders effective knowledge acquisition and
generalization [329, 330].


                                                                                       14
                                   A Survey of Vibe Coding with Large Language Models



4.3     Post-training Techniques
4.3.1    Supervised Fine-tuning
Large language model training follows well-established two-stage paradigms, with an initial pre-training phase
on massive diverse corpora to acquire broad linguistic and world knowledge, followed by post-training that
adapts models to excel at specific tasks and domains [58]. Supervised fine-tuning (SFT) is a critical technique that
enhances LLM capabilities while aligning model behaviors with human expectations and requirements [225, 1, 59].
The SFT process involves adjusting pre-trained model parameters in a supervised manner by utilizing carefully
curated datasets containing high-quality labeled examples, enabling models to maintain their broad foundational
knowledge while simultaneously acquiring highly targeted specialization for specific applications [61, 60, 2, 331].
Instruction tuning represents a particularly impactful form of supervised fine-tuning that enhances model
capabilities by explicitly training models to understand and accurately follow diverse human instructions across
varied task formats [279, 60], with research demonstrating substantial improvements in zero-shot performance on
previously unseen task types [60, 59].
Code generation is one of the most prominent and successful applications of supervised fine-tuning techniques,
with notable implementations including CodeGen and StarCoder which employ a two-stage approach of initial pre-
training on diverse multilingual code corpora followed by targeted fine-tuning on carefully selected monolingual
data to enhance language-specific code generation quality [62], while systems like WizardCoder demonstrate
alternative approaches by fine-tuning on specialized instruction corpora systematically derived from more
capable teacher models [62, 2]. The extremely large parameter counts characteristic of modern language models
make traditional approaches of updating all model parameters during fine-tuning computationally impractical
and prohibitively expensive [63, 64], driving rapid development of Parameter-Efficient Fine-Tuning (PEFT)
methodologies that achieve comparable performance with reduced computational requirements [332]. Adapter
Tuning represents one influential PEFT approach by introducing small trainable adapter modules that add only a
minimal number of new trainable parameters for each specific task while strategically keeping the vast majority
of original pre-trained parameters completely fixed [332, 64], while Low-Rank Adaptation (LoRA) achieves even
greater parameter efficiency by imposing carefully designed low-rank constraints on weight updates, enabling
effective fine-tuning with orders of magnitude fewer trainable parameters [332].
The critical importance of data quality over mere quantity has become a central guiding principle in supervised
fine-tuning research and practice [333, 334, 65], with sophisticated data selection and curation strategies proving
essential for optimal results. The AlpaGasus approach uses this method by systematically using ChatGPT to auto-
matically identify and filter out low-quality training examples, achieving significant performance improvements
using only 9,000 carefully selected high-quality samples compared to much larger but lower-quality datasets [66].
Interestingly, recent empirical research has revealed that supervised fine-tuning on high-quality demonstrations
can in many cases result in superior performance compared to more complex preference fine-tuning approaches,
particularly evident in challenging coding tasks where direct supervision appears especially effective [335].

4.3.2    Reinforcement Learning
Modern post-training approaches encompass two primary paradigms: supervised fine-tuning based on demon-
stration data, and preference fine-tuning methods utilizing techniques like RLHF and DPO [335, 67, 2, 68, 69].
Among these paradigms, reinforcement learning has become a pivotal technique for post-training large language
models, representing fundamental paradigm shifts away from traditional supervised fine-tuning approaches
toward more dynamic optimization strategies [2, 70, 336, 71, 337]. While pre-training establishes robust foun-
dational linguistic knowledge and pattern recognition capabilities, subsequent post-training refinement through
sophisticated RL techniques has proven essential for substantially enhancing models’ complex reasoning abilities
and adaptability to challenging real-world tasks [338]. The foundational framework for RL-based post-training
was firmly established by RLHF systems that align model behaviors using carefully constructed reward signals
derived from human preference judgments [71, 2, 339], with recent breakthrough systems like OpenAI’s o-series
models and DeepSeek-R1 demonstrating that models trained with RL post-training can significantly outperform
comparable models without RL training on demanding reasoning and coding benchmarks [71, 340].
The reinforcement learning algorithmic landscape for language model training centers around several key
complementary approaches, each with distinct advantages and trade-offs. PPO remains the most widely adopted
baseline approach due to its carefully designed clipped objective functions that effectively stabilize the inherently


                                                          15
                                 A Survey of Vibe Coding with Large Language Models




       Core Components                                                Core Capabilities

            Cognitive System


          Memory Mechanism


            Tool Integration                    Planning                     Action                 Collaboration


Figure 5 Coding Agent Architecture: Overview of core components comprising Cognitive System, Memory Mechanism,
and Tool Integration, with fundamental capabilities including Planning, Action execution, and multi-agent Collaboration for
coordinated software development tasks.


unstable RL training process [71, 2, 341, 70], while DPO represents a major algorithmic simplification by cleverly
replacing complex RL rollout procedures with more straightforward classification-style loss functions that directly
optimize preference rankings [71, 68, 342]. Group Relative Policy Optimization (GRPO) emerged to address specific
limitations in DPO by incorporating group-wise comparative feedback that enables more nuanced preference
learning [71, 341]. Significant paradigm shifts have emerged with approaches like Reinforcement Learning with
Verifiable Rewards (RLVR) that strategically replace learned reward models with deterministic task-specific rule-
based reward functions, proving particularly effective for domains like coding and mathematics where answer
correctness can be objectively verified [343].
Reinforcement learning has become a transformative strategy for code generation applications, with significant
empirical advancements demonstrated across multiple diverse programming domains and task types [336].
Foundational approaches in this area are exemplified by CodeRL, which employs sophisticated actor-critic
framework architectures where critic networks learn to accurately predict functional correctness of generated
code, providing learned reward signals that guide actor networks during the training process [341, 245]. Building
on these foundations, PPOCoder demonstrates effective integration of Proximal Policy Optimization with direct
execution-based feedback by utilizing actual compiler results and test case outcomes as immediate reward signals,
enabling models to learn from real program behavior [341], while more recent developments have introduced
sophisticated multi-stage training strategies exemplified by StepCoder which implements carefully designed
curricula progressing through increasingly complex code completion subtasks [341]. Applications of RL-based
code generation have extended to highly specialized technical domains, with systems like VeriSeek demonstrating
RL’s effectiveness for generating correct hardware description language code in challenging Verilog generation
tasks [344].
RL-based post-training faces numerous fundamental challenges that remain active areas of research. Training
stability issues include catastrophic forgetting of previously learned capabilities and reward hacking behaviors
where models exploit reward function specifications rather than learning intended behaviors [338]. Scale-dependent
effectiveness presents another significant limitation, with substantial benefits from RL training observed primarily
in large models ranging from 8 billion to 670 billion parameters [345], while RL techniques remain considerably
more challenging to apply successfully to smaller models with one billion or fewer parameters where training
instability and sample efficiency become critical bottlenecks. Additionally, optimization dilemmas persist in
the form of exploration-exploitation tradeoffs, with RL training often suffering from severe sample inefficiency
particularly when initial policy distributions struggle to adequately explore regions of the action space containing
high-reward trajectories [340], and fundamental mismatches between training objectives and evaluation metrics,
with standard RL formulations focused on maximizing expected cumulative reward while practical evaluation of
code generation systems typically relies on risk-seeking metrics like Pass@k that prioritize generating at least one
correct solution among multiple attempts [339, 346, 347].




                                                            16
                                A Survey of Vibe Coding with Large Language Models



5     LLM-based Coding Agent
5.1     Decomposition and Planning Capability
5.1.1    Task Decomposition Strategies
Task decomposition systematically breaks complex problems into manageable subtasks, proven essential from
traditional planning to modern LLM applications, enabling coding agents to tackle sophisticated challenges
while improving reliability, interpretability, and multi-agent collaboration [70, 348, 72, 73]. Strategies evolved into
distinct paradigms including factored cognition for simultaneous processing, process supervision for sequential
dependencies, Chain-of-Thought for step-by-step reasoning, and extensions like Tree-of-Thought (ToT) and Graph-
of-Thought for multi-path reasoning [72, 74, 349, 75, 201, 76]. Concrete techniques span prompting-based CoT
using few-shot or zero-shot instructions [72, 77, 230], Auto-CoT generating samples through clustering [78],
Plan-and-Solve devising task-dividing plans [230], tree structures like ToT generating branching explorations [79],
and HyperTree Planning enabling divide-and-conquer with Monte Carlo integration [80].
CoT emerges as most popular code generation strategy achieving higher correctness [72, 74], while dynamic
strategies like CodePlan employ adaptive algorithms [81, 73], and multi-path approaches simulate generation
paths with Monte Carlo optimization, though LLMs potentially hallucinate incoherent plans despite proper
instructions [82, 350, 83].

5.1.2    Plan Formulation Methods
LLMs’ training on natural language and code unlocks reasoning producing structured steps connecting to execution
environments, with planning crucial for agents determining action sequences from initial states [73]. Approaches
categorize into External Module Augmented Methods integrating planners and memory, Finetuning-based Methods
enhancing abilities through trajectory data, and Searching-based Methods identifying optimal solutions [349, 85],
while three paradigms emerged: LLM-as-Planner employing inherent reasoning, LLM-as-Facilitator translating to
Planning Domain Definition Language (PDDL) [351, 352], and Multi-Agent Planning coordinating multiple agents
[73, 252], with task decomposition employing Single-Path following linear trajectories [72], Tree-Based exploring
multiple trajectories [79, 353], and Hierarchical Planning at different abstraction levels.
Planning with feedback enables adaptation through ReAct interleaving Thought, Action, and Observation [354, 74],
though incremental approaches risk local optima [355], while Memory-Enhanced Planning addresses limitations
through Reflexion augmenting agents with Evaluator, Self-reflection, and memory buffers enabling continual
improvement [356, 72, 357]. Multi-agent systems coordinate specialized agents distributing planning across
components [351, 358], with Integration combining structured PDDL with LLMs where LLMs allocate sub-
tasks while planners like Fast Downward generate plans [359, 352, 360, 361]. Challenges persist including Goal
Decomposition struggling with actionable steps [362], Long-Horizon Task Management losing coherent strategy
[362, 363], and Training Data Scarcity requiring synthetic augmentation [362].

5.2     Memory Mechanism
5.2.1    Overview and Fundamentals
Extending beyond fixed context windows, memory mechanisms emerge as functional phenomena in LLMs
demonstrating primacy and recency effects despite lacking explicit subsystems [364, 84, 365]. Contemporary
approaches draw parallels to human cognitive architecture, mapping context and parameters to short-term and
long-term memory and transforming contextual knowledge into parameter updates [365, 366].
Following this framework, short-term memory constitutes temporary storage with limited capacity, corresponding
to context window information accessible during inference [367–369, 1, 370], while long-term memory stores
information over days to years, classified into declarative explicit and non-declarative implicit memory [371].
From an implementation perspective, these memory types classify into parametric memory stored in model
weights and non-parametric memory in external systems [371–373, 85].

5.2.2    Memory Operations and Management
Accordingly, memory operations enable coding agents to function beyond static context windows, maintaining
persistent knowledge about codebases, patterns, and debugging histories [357, 86, 221]. These operations are


                                                          17
                               A Survey of Vibe Coding with Large Language Models


Table 2 Capabilities of Coding Agents Based on Large Language Models.

                                                                      Capability
 Coding Agent
                                    Code     File             Web
                                                    Shell               Testing    MCP   Multimodal   Context
                                   Search    Ops             Search

 CodeAgent [99]                      ✓        ✓                ✓          ✓                              ✓
 MapCoder [24]                       ✓                                    ✓                              ✓
 ChatDev [10]                                                             ✓                              ✓
 CodeAct [256]                                        ✓                   ✓
 SWE-Search [197]                    ✓        ✓                           ✓                              ✓
 OpenHands [15]                               ✓       ✓        ✓          ✓                              ✓
 OpenHands-Versa [23]                         ✓       ✓        ✓          ✓                  ✓           ✓
 MetaGPT [252]                                ✓       ✓        ✓          ✓                              ✓
 SWE-agent [12]                      ✓        ✓       ✓                   ✓                              ✓
 AutoSafeCoder [374]                                                      ✓                              ✓
 AutoCodeRover [13]                  ✓                                    ✓                              ✓
 Lita [375]                          ✓        ✓       ✓                   ✓                              ✓
 SWE-dev [376]                                                            ✓
 RepoForge [377]                              ✓       ✓                   ✓                              ✓
 LessonL [378]                                                            ✓                              ✓
 AdaCoder [16]                                                            ✓
 Code2MCP [379]                                                           ✓         ✓                    ✓
 ScreenCoder [380]                                                                           ✓           ✓
 SimuGen [381]                                                            ✓                  ✓
 SoA [194]                                                                                               ✓
 SICA [360]                                   ✓       ✓                   ✓                              ✓
 RGD [118]                                                                ✓                              ✓
 Guided Code Generation [104]                                             ✓                              ✓
 AgentCoder [104]                                     ✓                   ✓                              ✓
 AppAgent [382]                                                                              ✓
 Cursor IDE [383]                    ✓        ✓       ✓        ✓          ✓         ✓        ✓           ✓
 Claude Code [384]                   ✓        ✓       ✓        ✓          ✓         ✓        ✓           ✓
 Gemini Code CLI [385]               ✓        ✓       ✓        ✓          ✓         ✓        ✓           ✓
 Qwen Coder [386]                    ✓        ✓       ✓        ✓          ✓         ✓        ✓           ✓
 Codex [387]                         ✓        ✓       ✓        ✓          ✓         ✓        ✓           ✓


managed through six fundamental procedures: consolidation, indexing, updating, forgetting, retrieval, and
compression [87, 388, 389, 88, 89, 365].
Specifically, the foundation rests on memory reading retrieving relevant information [90], memory writing
transforming observations into structured contents, and memory reflection reorganizing knowledge [91, 221,
85]. Comprehensive systems implement specialized functions including consolidation, indexing, and updating
employing locate-and-edit techniques [390, 92, 14, 389, 391, 89], with optimization extracting meta-insights and
selective management yielding 10% gains [388, 392].

5.2.3   Memory Architecture in Coding Agents
In practice, short-term memory plays critical role in hierarchical architectures, enabling immediate feedback
integration demonstrated by FALCON’s two-level structure [393, 357], while dynamic management with MemTool
achieves 90-94% efficiency [394].
In contrast, long-term memory implementations utilize external memory-based methods with physical storage
maintaining historical information. Vector databases emerged as prominent non-parametric solution achieving


                                                       18
                               A Survey of Vibe Coding with Large Language Models



long-term effects and allowing domain-specific knowledge access [395–397], though struggling with belief updating
challenges. To address these limitations, Memory Bank stores memory with temporal timestamps and implements
Ebbinghaus-inspired forgetting curves [89, 398, 396, 85]. These implementations categorize into three architectural
patterns: Long-Context Agents with First-In-First-Out (FIFO) eviction, RAG Agents using external pools, and
Agentic Memory Agents employing iterative reasoning [399, 365]. Furthermore, contemporary architectures adopt
dual-component systems mirroring human cognition through frameworks like RAISE [400] and InfiniteICL [401],
transforming temporary knowledge into permanent updates. Additionally, specialized mechanisms demonstrate
distinct optimization strategies. Think-in-Memory eliminates redundant reasoning by caching intermediate results
[402], whereas MemGPT leverages virtual context management to extend effective context windows through
intelligent memory paging [357], thus addressing belief updating challenges inherent in static vector database
approaches.

5.3     Action Execution
5.3.1    Tool Invocation
Tool integration with LLMs fundamentally transformed AI-powered development [93, 74], with Tool-Augmented
Models extending functionalities by integrating external tools [94, 95, 74], producing AI agentic programming
where LLM-based agents autonomously plan, execute, and interact with compilers, debuggers, and version
control reshaping development practices. Early task-specific systems suffered limited scalability [97], while ReAct
established observation-action-thought pattern becoming foundation for LangChain and AutoGen [97, 74], with
modern frameworks adopting standardized paradigms decomposing capabilities into specialized components
[403] and enabling automatic transformation of documentation into callable functions [96, 98].
Tool invocation evolved beyond traditional JSON-based approaches [74, 404], with executable code-based frame-
works [256, 127] consolidating actions into unified Python space enabling dynamic revision and composition,
demonstrating substantial improvements over predefined constraints. Systems like ToolCoder reduced hallucina-
tion errors [243, 93, 252], while agents integrating specialized tools [99] demonstrated significant improvements
outperforming commercial products like GitHub Copilot [243]. Protocol standardization through Model Context
Protocol established schema-driven interfaces, with advanced discovery mechanisms [97, 101] enabling dynamic
selection through iterative invocation and document-weighted averaging addressing scalability across large-scale
repositories. Enterprise-focused frameworks [405, 406, 102, 73] automated pipelines transforming API specifica-
tions into executable Python functions, substantially enhancing accuracy while eliminating scaffolding efforts,
with reinforcement learning integration [407, 116] unifying tool usage with reasoning through policy optimization.

5.3.2    Code-based Action Implementation
Contemporary systems implemented structured workflows through five-stage processes: planning, selection,
parameter extraction, invocation, and result integration [100, 419, 74], following systematic patterns integrating
generation with continuous mechanisms creating closed-loop systems where outcomes influence planning. Ad-
vanced workflows implement sophisticated error recovery creating robust pipelines, with environment interaction
relying on multi-turn patterns following ReAct iteratively gathering information and taking actions [103, 74, 348].
Code generation emerged as unified action paradigm consolidating diverse agent behaviors [243, 194, 420]. Exe-
cutable code-based approaches [256] integrated Python interpreters enabling dynamic revision of prior actions
upon observations through multi-turn interactions, achieving substantial improvements across API benchmarking
compared to JSON-based alternatives. Repository-level systems [99, 243] extended capabilities from isolated
snippets to complex projects with intricate dependencies, leveraging external tools for information retrieval,
navigation, and implementation assistance. Multi-agent architectures [104] decomposed programming tasks
through specialized coordination with programmer, test designer, and executor agents achieving superior per-
formance while reducing computational overhead, while repository-scale evolution systems [421] demonstrated
autonomous improvement through iterative planning across hundreds of files and thousands of lines, with
evolved implementations outperforming human-designed solutions. Reinforcement learning approaches [165]
enabled learning optimal strategies through policy optimization producing implementations mirroring human
preferences and achieving state-of-the-art results while surpassing reference solutions, with agent frameworks
[15] establishing comprehensive platforms enabling code writing, command-line operations, and multi-agent
coordination supporting diverse implementations across multiple benchmarks. Beyond conventional synthesis
tasks, code generation demonstrated versatility for structured knowledge applications, with KnowCoder pio-


                                                        19
                                    A Survey of Vibe Coding with Large Language Models


Table 3 Overview of Commercial AI-Assisted Development Softwares.

 Type            Product               Core Functionality                 Technical Features                        Target Scenarios

                 Cursor [383]          AI-native code editor with         VS Code fork with deep AI inte-           Complex projects requiring in-
                                       multi-file editing, intelligent    gration, composer agent mode, sup-        telligent refactoring, full-stack
                                       refactoring, and conversational    ports Claude/GPT-4/Gemini mod-            development, professional de-
                                       AI                                 els, codebase-wide context aware-         velopers
                                                                          ness

                 Copilot [408]         Real-time code completion, gen-    Trained on GitHub repositories, sup-      Daily   coding     assistance,
                                       eration, and explanation across    ports VS Code/JetBrains/Neovim,           autocomplete-focused    work-
                                       multiple IDEs                      inline suggestions, chat interface        flows,     GitHub-integrated
                                                                                                                    development
   Embedded      Windsurf [409]        Agentic IDE with autonomous        Cascade Flow system, auto-executes        Large codebases, multi-file rea-
                                       coding capabilities and deep       terminal commands, supports mul-          soning, team collaboration with
                                       contextual understanding           tiple AI models, built on VS Code         advanced workflow automation

                 Tabnine [410]         Enterprise-grade AI code com-      Local/on-premise deployment op-           Enterprise environments, regu-
                                       pletion with privacy-first ap-     tions, trained only on permissive         lated industries (finance, health-
                                       proach                             licenses, custom model training on        care), privacy-sensitive projects
                                                                          proprietary code

                 CodeWhisperer [411]   AWS-optimized code genera-         Integrated with AWS services, refer-      AWS      cloud    development,
                                       tion and security scanning         ence tracking for license compliance,     serverless applications, cloud-
                                                                          security vulnerability scanning           native architecture

                 v0 [412]              Natural language to Reac-          Generates production-ready React +        Frontend prototyping, UI/UX
                                       t/Next.js UI generation with       Tailwind code, integrated security        design-to-code, rapid MVP de-
                                       deployment                         checks, one-click Vercel deployment       velopment

                 Replit [413]          Cloud-based autonomous app         Complete environment setup, inte-         Non-technical users, rapid pro-
   End-to-End                          builder from natural language      grated databases and authentication,      totyping, educational projects,
                                       descriptions                       multi-language support, browser-          small business tools
                                                                          based testing

                 Bolt.new [414]        Browser-native full-stack devel-   WebContainers technology, runs            Full-stack prototyping, quick
                                       opment with instant preview        Node.js in browser, supports npm          demos, cloud-native develop-
                                       and deployment                     packages, StackBlitz infrastructure       ment without local setup

                 Claude Code [384]     Terminal-based agentic coding      Powered by Claude Sonnet 4.5,             Complex terminal workflows,
                                       tool with autonomous capabili-     local-first execution, MCP integra-       autonomous code refactoring,
                                       ties                               tion, checkpoint/rewind system, VS        multi-file operations
                                                                          Code extension

                 Gemini CLI [415]      Open-source AI agent for           Gemini 2.5 Pro with 1M token con-         Terminal-first     developers,
                                       terminal-native development        text, agent mode with multi-step          Google     Cloud   workflows,
                                                                          planning, free tier (60 RPM, 1000         budget-conscious teams
                                                                          requests/day)

                 Qwen Code [416]       Research-focused CLI tool for      Powered by Qwen3-Coder models             Open-source enthusiasts, re-
                                       agentic coding tasks               (480B MoE), 256K-1M token context,        searchers, privacy-focused local
                                                                          enhanced parser                           deployments

                 Aider [417]           Open-source AI pair program-       Multi-LLM support (Claude, GPT-           Budget-conscious developers,
                                       ming in terminal                   4o, DeepSeek), codebase mapping,          multi-model workflows, Git-
                                                                          automatic Git commits, voice com-         centric development
        CLI                                                               mands

                 Codex [387]           Cloud-based software engineer-     Parallel task execution; per-task         Pro teams automating code re-
                                       ing agent that writes features,    cloud sandboxes; CLI & IDE                views, refactors, tests, and on-
                                       fixes bugs, answers codebase       extension; GitHub PR (@codex)             call maintenance across large
                                       questions, and proposes PRs in     integration;   configurable   via         repositories
                                       isolated sandboxes                 ˜/.codex/config; MCP tool access

                 Cline [418]           Open-source coding agent in        Client-side,    zero-trust architec-      Enterprise/security-sensitive
                                       IDE/CLI that understands           ture; model-agnostic (Claude/Gemi-        orgs;   large-codebase refac-
                                       whole codebases, plans com-        ni/etc.); reads/writes files, runs ter-   tors; multi-model workflows
                                       plex changes, and executes         minal commands & browser; MCP             needing transparent, auditable
                                       multi-step tasks with user ap-     integration; SOC 2/GDPR; enter-           control
                                       proval                             prise team/billing options



neering Python class-based schema representations enabling unified information extraction through two-phase
learning framework combining code pretraining and instruction tuning [422]. Building upon this foundation,
KnowCoder-X subsequently addressed cross-lingual transfer limitations by standardizing multilingual schemas
as Python classes, achieving substantial improvements over commercial systems through bilingual alignment
instruction tuning [423]. Further advancing this paradigm, KnowCoder-V2 extended capabilities from extraction to
deep analysis by bridging knowledge organization with analytical reasoning via unified code generation, thereby


                                                                    20
                                 A Survey of Vibe Coding with Large Language Models



enabling systematic processing of complex knowledge analysis tasks [424].

5.4     Reflection: Iteration, Validation, and Debugging
5.4.1    Iterative Refinement
Effective code generation requires systematic refinement beyond single attempts [35, 116]. Large Language Models
demonstrated significant potential in automated code generation [35]. However, accuracy remains limited partic-
ularly for complex tasks demanding comprehensive understanding [118]. This stems from inherent challenges
in simultaneously comprehending natural language and producing correct code without automatic refinement,
making single-attempt approaches insufficient [118, 108]. Researchers developed multi-round frameworks em-
ploying iterative refinement, significantly improving synthesis quality [105, 117, 425]. These enable LLMs to learn
from errors through reflection mechanisms incorporating failed tests and using outcomes to enhance subsequent
attempts [118]. The approaches evolved to incorporate feedback from multiple sources [109, 127]. Direct ap-
proaches integrate compiler feedback where code LLMs generate, execute, and improve code based on results
[117]. Modern frameworks employ multi-agent architectures with coder and critic agents, where coder generates
and critic analyzes providing feedback in iterative loops [272, 127, 104, 10]. Sophisticated systems implement
specialized roles such as Reflection Agents, Thinking Agents, and Execution Agents [106].

5.4.2    Code Validation
Code validation evolved into sophisticated multi-layered approaches using dedicated critic agents conducting
thorough analyses focusing on efficiency and functional correctness [426, 116, 127]. Automated testing provides
quantitative metrics, categorized into using built-in benchmark test sets or LLM-generated test sets [426]. Advanced
approaches leverage LLM-as-a-Judge frameworks, producing not only rating scores but also detailed feedback to
repair incorrect code [427].

5.4.3    Intelligent Debugging
Self-reflection represents fundamental shift from one-shot generation to iterative refinement, involving prompting
LLM to review earlier outputs identifying logical flaws [105, 116]. Research identified post-execution self-debugging,
analyzing code after execution, struggling with bias [428]. In contrast, in-execution self-debugging examines
intermediate states showing more promise [110, 429, 428]. Advanced frameworks employ search algorithms
systematically exploring multiple debugging paths, enabling comprehensive repair capabilities [275]. Testing and
debugging methodologies involve evaluating across multiple domains [430–432, 181, 425]. Industrial deployment
shows promising results, with Meta’s TestGen-LLM achieving 75% building correctly, 57% passing reliably, and
25% increasing coverage [181]. The evolution toward multi-agent collaboration represents significant advancement
mimicking real-world development practices [111]. Modern frameworks implement specialized architectures
coordinating debugging with specialized agents as bug explainers, fault locators, and patch proposers [107].
Integration of multiple debugging and reflection techniques demonstrates exceptional improvements, with some
reaching 98.2 on HumanEval employing debugging mechanisms decomposing failed code using Control Flow
Graph analysis [111].

5.5     Agent Collaboration
5.5.1    Collaboration Mechanisms
Complex software engineering tasks increasingly demand coordinated efforts beyond single-agent capabilities
[124, 252]. Multi-agent systems represent significant shift from single-agent approaches to collaborative frameworks
enabling multiple agents to collaborate by distributing responsibilities, facilitating scalable execution, improving
resilience, and allowing dynamic adaptation [125, 124, 433, 127]. Communication serves as cornerstone of
coordination, representing medium through which collective reasoning emerges [125], with LLMs enhancing
communication, coordination, and decision-making enabling agents to interpret complex instructions [434, 435,
433, 10]. In software engineering contexts, LLM Multi-Agent Systems represent emerging approach where
multiple agents are assigned specific roles to collaboratively execute complex development tasks, dividing
responsibilities among specialized agents emulating real-world roles [436]. The field has developed several
distinct communication architectures including four primary patterns: layered, decentralized, centralized, and
shared message pools [119, 436]. Complementing these communication structures, role-based collaboration


                                                           21
                               A Survey of Vibe Coding with Large Language Models




                        Development Environment of Coding Agent                                Applications

                                                                                                     Docker


                                                                                                     Github


                                                                                                     GitOps
        Isolated Environment   Interactive Environment        Distributed Platform


Figure 6 Development Environment Architecture for Coding Agents: Isolated Environment, Interactive Environment, and
Distributed Platform.


represents prominent strategy with LLM-based agents assuming specialized roles assigned sub-tasks to solve
objectives [126, 252, 437], demonstrating considerable success with agents typically assigned roles based on expert
knowledge implemented in frameworks like AutoGen and CrewAI using teams with different roles through
task decomposition and specialization [120]. This approach categorizes into pipeline approaches where agents
sequentially complete task parts, group discussion frameworks where agents communicate to reach agreements, or
hybrid combinations [435, 438, 121, 437]. Specifically, shared message pool represents sophisticated communication
approach serving as centralized hub where agents post, access, and interpret messages facilitating asynchronous
reasoning. In MetaGPT, the pool operates as structured system enabling collaboration where agents publish and
subscribe to typed messages, reducing communication overhead [436, 10].

5.5.2    Framework Implementations
Building upon these mechanisms, several frameworks demonstrate practical implementations of multi-agent
collaboration. MetaGPT enables collaborations streamlining software engineering workflow through role-specific
prompts establishing effective cooperation implementing standard operating procedures [368, 122, 252]. Similarly,
ChatDev represents chat-powered framework where specialized agents are guided via chat chain modeling
virtual software company communicating to autonomously generate software [10, 439, 122]. Additionally, CAMEL
introduces framework enabling autonomous cooperation through role-playing, providing theoretical foundations
for agent interaction. Multi-agent role-based collaboration has demonstrated consistent performance improvements
leveraging collective intelligence [434]. MapCoder employs four specialized agents showcasing exceptional
capabilities, achieving state-of-the-art results including 93.9% on HumanEval, 83.1% on MBPP, 22.0% on APPS,
28.5% on CodeContests, and 45.3% on xCodeEval [127]. MetaGPT demonstrated impressive accuracy through
Standardized Operating Procedures [252, 121]. Beyond performance metrics, role-based systems offer significant
cost advantages. ChatDev demonstrates how communicative agents facilitate seamless workflows, proving cost-
effective and capable of proactively addressing errors, simplifying processes and improving code quality by
mimicking human teamwork patterns [10]. These implementations collectively represent fundamental shift toward
collaborative intelligence in software engineering [125].

6     Development Environment of Coding Agent
6.1     Isolated Execution Runtime Environment
6.1.1    Containerization Technologies
Containerization has become a fundamental component of the modern coding agent infrastructure. By encapsu-
lating software, dependencies, and runtime configurations within portable images, containerization guarantees a
consistent execution environment across diverse hardware and operating systems [440, 128, 129]. Containers rely
on operating system–level virtualization to achieve lightweight isolation, rapid startup, and efficient resource
utilization compared with full virtual machines [440, 130]. OS-level abstraction enables superior resource efficiency
with quicker startup than virtual machines while providing agility, portability, reproducibility, modularity, and
flexibility [129, 441, 128, 442, 443, 131, 444–446]. These properties are particularly valuable for coding agents,


                                                         22
                                 A Survey of Vibe Coding with Large Language Models



which often need to execute user-generated code repeatedly and securely while maintaining reproducibility and
scalability [447, 448, 132, 133].
Docker remains the dominant technology for constructing and distributing container images. Its layered architec-
ture, based on Dockerfiles and registries, allows for incremental builds and efficient updates [134, 449].In addition
to Docker, lightweight virtualization frameworks such as Linux Containers (LXC/LXD) and specialized research
sandboxes, including SandboxFusion and MPLSandbox, are increasingly employed in experimental systems that
demand stronger isolation or multi-language support [450, 451, 135].
At the orchestration level, Kubernetes has become indispensable in managing containerized workloads. It assigns
coding agent tasks into isolated pods, allocates computational quotas, and enforces automatic timeouts to prevent
resource monopolization [136]. These mechanisms collectively ensure that agent-generated code can be executed
in a controlled, reproducible, and efficient manner.

6.1.2   Security Isolation Mechanisms
Because large language models can generate arbitrary and potentially unsafe code, strict security isolation is
essential. Sandbox-based systems provide the first line of defense by limiting the privileges of agent-executed
code [11, 137–139, 452]. Tools such as gVisor intercept system calls to enforce fine-grained safety policies, while
lightweight hypervisors and microkernels enhance separation between host and container [453]. Multi-layer
sandboxing frameworks such as SAFE-LLM and NatiSand combine container isolation with dynamic monitoring
to detect unsafe system behavior [137, 454–456].
Hardware-assisted isolation techniques further strengthen security. Intel PKRU memory protection and ARM
TrustZone restrict unauthorized memory access and system control [457]. WebAssembly-based execution engines
also provide deterministic and memory-safe environments for running untrusted agent code [458].
Contemporary coding agents typically embed execution backends that incorporate both static and dynamic
policy enforcement. These backends restrict file I/O, network connections, and environment variables, while
maintaining extensive logging to support traceability and auditability [459, 138]. Such hybrid security design
enables continuous testing of agent-generated code without exposing the host system to unverified or malicious
behaviors.

6.1.3   Cloud-based Execution Platforms
Cloud-based execution platforms extend the principles of containerization and sandboxing to distributed envi-
ronments. They enable scalable execution across clusters, support dynamic resource allocation, and facilitate
transparent workload scheduling [460–462]. Production deployments operate on 25,000 CPU core clusters orga-
nized into specialized pod configurations separating judging pods for evaluation from execution pods for code
running with exclusive core assignment ensuring isolation and consistent performance, supporting AWS, Azure,
and Google Cloud Platform with Kubernetes-based solutions enabling transparent remote execution [463].
Resource management involves containerized environments using Docker ensuring consistent execution across
infrastructure configurations with rapid system reset capabilities [464, 465]. Security isolation relies on containerized
sandbox environments creating multiple protection layers with Docker containers providing isolated file systems,
process spaces, and network spaces implementing strict CPU and memory limits through Kubernetes management
systems enforcing timeout strategies automatically terminating environments exceeding specified durations
[136, 466, 467].
Runtime environments support diverse programming language ecosystems including C, C++, Java, Python, Rust,
Go, C#, and PHP with execution pods handling specific compilation and runtime requirements enabling agents
to work across different paradigms. Platforms use reproducible cloud compute instances providing consistent
virtual hardware configurations deployed on standardized instances like Amazon EC2 with execution engines like
JUDGE0 supporting over 60 languages through sandboxed Docker environments [466]. Modern implementations
employ dedicated Google Cloud Platform servers with standardized configurations ensuring consistent execution
eliminating interference between optimization runs [465]. Distributed frameworks implement two-tier pod design
patterns separating execution from evaluation with large-scale implementations using 8,500 execution pods running
individual code instances at concurrency 1 with exclusive core assignment while 2,000 judging pods handle
complete evaluation workflows including correctness checking. Container orchestration follows microservices
patterns where each agent and execution module operates in Kubernetes-managed containers with shared volumes


                                                           23
                                A Survey of Vibe Coding with Large Language Models



and persistent volume claims facilitating data exchange while maintaining long-term storage of execution artifacts,
logs, and results implementing secure REPL sandbox patterns governed by strict execution constraints [467].

6.2     Interactive Development Interface Environment
6.2.1    AI-Native Development Interfaces
The integration of coding agents into the developer’s workspace has transformed the traditional notion of an
Integrated Development Environment (IDE). Instead of passively editing code, developers now engage in a
continuous dialogue with the system. AI-native development interfaces embed large language models directly
within the editor, combining code completion, conversational reasoning, and contextual memory [84, 45, 1, 46].
Two dominant paradigms have emerged. The first emphasizes inline suggestion, where the system predicts the
next tokens or statements directly within the editor, offering context-sensitive autocompletion and refactoring hints.
The second paradigm emphasizes conversational interaction, in which the developer communicates with the agent
using natural language to specify intent, request explanations, or perform debugging [468–470, 140, 471, 472].
Studies show that integrating both paradigms within a unified interface produces higher task efficiency and user
satisfaction. Inline completion supports rapid iteration, while conversational interaction enhances explainability and
collaboration [469, 471]. Emerging IDEs such as Cursor and Q Developer integrate contextual memory and multi-
turn reasoning, maintaining persistent dialogue histories to provide more coherent assistance [141, 471, 473, 144].

6.2.2    Remote Development
The growth of cloud-native development practices has led to widespread adoption of remote and containerized
development environments. Systems such as GitHub Codespaces [474] and DevContainer provide pre-configured,
reproducible workspaces accessible via browsers or local editors. This paradigm allows coding agents to operate
directly within standardized, resource-isolated environments synchronized with version control systems.
Remote development also supports computation-intensive workflows by allowing resource-demanding tasks to
run on remote servers while the developer interacts through lightweight clients. SSH-based connections and
browser-based terminals enable seamless transitions between local and cloud execution contexts. These capabilities
are essential for agent-assisted programming, as they allow distributed collaboration while maintaining strict
control over dependencies and runtime configurations [475].

6.2.3    Tool Integration Protocol Standards
Standardization efforts have become increasingly important for achieving interoperability between coding agents
and existing developer tools. The Model Context Protocol (MCP) [96, 476] defines a universal interface for
exchanging contextual information such as source code, documentation, and environment state. The Language
Server Protocol (LSP) [142, 145] provides language-agnostic features including diagnostics, completion, and code
navigation, while the Debug Adapter Protocol (DAP) [477, 478] standardizes debugging interactions.
Integrating these protocols allows coding agents to function as first-class participants within conventional de-
velopment ecosystems. Agents can request, modify, and analyze project context seamlessly, while maintaining
compatibility with existing IDEs and version control systems [479, 146, 143]. This protocol convergence promotes
an open, extensible environment for hybrid human–AI programming collaboration [480, 481].

6.3     Distributed Orchestration Platform Environment
6.3.1    CI/CD Pipeline Integration
Continuous Integration and Continuous Deployment (CI/CD) frameworks are essential for maintaining the stability
and quality of software systems. Within the context of coding agents, CI/CD processes ensure that automatically
generated code passes through rigorous validation and testing stages before integration [155, 273, 482, 156].
Pipeline-as-Code practices enable reproducibility by representing build and deployment workflows as versioned
artifacts [155, 483]. In cloud-native ecosystems, Kubernetes and Jenkins-based automation frameworks such as
KubeSphere facilitate modular CI/CD pipelines. These pipelines automatically handle code building, testing, and
deployment, while ensuring that agent-generated contributions are subject to the same review and validation
processes as human-written code.


                                                         24
                                A Survey of Vibe Coding with Large Language Models



In the emerging paradigm of Vibe Coding, CI/CD pipelines are further extended with agent participation. Agents
generate code, perform static analysis, and conduct self-testing, but human oversight remains indispensable for
critical verification stages. Designing CI/CD architectures that integrate agents safely and transparently is a key
challenge for reliable large-scale deployment [155].

6.3.2   Cloud Compute Orchestration
Distributed orchestration platforms employ frameworks dynamically provisioning computational resources with
production deployments demonstrating scale operating on 25,000 CPU core clusters organized into specialized
pod configurations [460]. The orchestration landscape has been enhanced by TOSCA (Topology and Orchestration
Specification for Cloud Applications) providing interoperable models for describing cloud applications as typed
directed topology graphs representing components as nodes and dependencies as links enabling developers
to model cloud service structures with automated lifecycle management [157, 147, 148]. TOSCA’s platform-
agnostic nature allows users to switch between cloud providers enabling applications to be migrated between
vendors with minimal modification demonstrating strong compatibility with CI/CD technologies facilitating easier
testing, re-deployment, and re-engineering [148, 149], with modern platforms like FogArm providing autonomous
adaptation capabilities responding to application specification changes from CI/CD pipelines and infrastructural
variations detected through distributed monitoring [157]. LLM-powered component integration adds complexity
and opportunity where frameworks built on large language models, retrieval-augmented generation, and deep
learning enable seamless integration with CI/CD pipelines supporting multi-format output generation and
incorporating continuous learning for optimization [158]. Modern implementations configure CI/CD pipelines
to build, test, and deploy applications within containerized environments enabling faster build times and more
frequent releases with Continuous Deployment integrating directly with LLMOps to automatically deploy model
updates based on performance monitoring enabling automated model transitioning, deployment, and monitoring
while maintaining high reliability using GitOps pipelines ensuring automatic redeployment of updated agent
code or model weights with Canary releases and A/B testing [159, 160].

6.3.3   Multi-Agent Collaboration Frameworks
As coding tasks become increasingly complex, single-agent systems struggle to manage the breadth of reasoning,
planning, and verification required for end-to-end software generation. Multi-agent collaboration frameworks
address this limitation by coordinating multiple specialized agents that share contextual memory and cooperate
through structured communication channels.
Frameworks such as AutoGen, CrewAI, MetaGPT, and LangGraph exemplify this paradigm. AutoGen organizes
heterogeneous agents that perform role-specific tasks such as requirement analysis, implementation, and unit
testing [150–152]. CrewAI conceptualizes agent collaboration as a simulation of human teams, incorporating
negotiation, task assignment, and feedback integration [153]. MetaGPT introduces a meta-planning layer, where
high-level agents design task hierarchies and delegate execution to subordinate agents, thereby achieving structured
decomposition [252, 154]. LangGraph formalizes collaboration as a graph of nodes and edges representing agents
and communication pathways, which enables systematic reasoning over dependencies and task flows [484].
These frameworks collectively redefine how coding agents can scale across complex development pipelines. They
provide fault tolerance by redistributing tasks when individual agents fail, improve modularity through role
specialization, and support iterative verification through feedback loops among agents. Recent studies suggest that
multi-agent collaboration enhances both the reliability and interpretability of large-scale code synthesis [485, 123].
Despite these advances, challenges remain regarding consistency, communication efficiency, and conflict resolution.
Overly frequent message exchanges may lead to coordination overhead, while insufficient synchronization can
cause semantic drift among agents. Ongoing research is exploring graph-structured communication protocols and
shared reasoning buffers to improve coherence across collaborative agents [161, 486].
The development of multi-agent frameworks represents an essential direction for the evolution of Vibe Coding
systems. These frameworks not only enhance scalability and adaptability but also embody a shift toward
distributed intelligence in software engineering, where human developers and autonomous agents collaborate as
peers within integrated ecosystems [487].




                                                         25
                                 A Survey of Vibe Coding with Large Language Models



Feedback Loops                 Model Layer                      Agent Layer                        Human Layer

      Internal feedback


    External feedback

        Environment


           Human            Self-Refinement                                                    Human Feedback
                                                 Compiler Feedback Execution Feedback


Figure 7 Feedback Loops Framework for Coding Agents: Internal feedback via Self-Refinement, and External feedback from
Environment via Compiler Feedback and Execution Feedback, and from Human Feedback.


7      Feedback Mechanisms
7.1     Compiler Feedback
7.1.1     Syntax and Type Error Feedback
LLM-based coding agents rely on compiler feedback to iteratively improve generated code through error detection
and repair cycles [488, 489, 1, 105, 117, 490]. Compiler feedback encompasses multiple granularities: coarse-grained
feedback provides binary compilation success, while fine-grained feedback delivers detailed error reasons and
locations [491]. Beyond basic compilation feedback, systems integrate test feedback from automated frameworks
and static analysis from tools like pylint [492].
Modern architectures integrate compiler feedback through multi-agent systems employing Code Teachers reassess-
ing bug addressing, Review Agents examining compilation logs generating structured prompts, reinforcement
learning approaches with RLCF, PPOCoder, and COMPCODER, debugging agents using retrieval-augmented
generation and Chain-of-Thought methodology, and tool-integrated approaches like CoderAgent [491, 393].
Domain-specific implementations include AutoChip incorporating compilation error messages, RTLFixer using
retrieval-augmented generation for Verilog errors, and RTLCoder introducing code quality scoring [169].
Significant limitations persist in compiler feedback. Compilers report transformation failures through coarse error
messages providing insufficient insight [493, 494, 117]. Project-specific context often cannot fit into LLM prompts,
while workflow complexity creates inconsistent approaches [117, 493].
Accordingly, compiler feedback has evolved from basic validation to sophisticated iterative refinement providing
detailed feedback including compilation success status, optimization pass information, and instruction counts
[495, 38]. Effectiveness depends heavily on context—incorporating compiler feedback improves accuracy, though
highlighting errors without resolution context shows limited improvement [117].

7.1.2     Static Analysis Feedback
LLMs demonstrate exceptional capabilities for understanding complex compiler messages and static analysis
warnings [496, 497]. Correspondingly, static analysis tools analyze code without execution, employing predefined
rules to enforce standards and detect bugs, though producing large volumes of warnings including false positives
[498–502]. LLMs achieve 69-81% accuracy in prioritizing warnings and 81.13% precision with 94.64% recall in
inspecting thousands of static warnings [503, 504].
Current systems employ comprehensive verification through multiple layers: syntactic correctness checking
through compilers like GCC and Python interpreters, specialized tools including Black for formatting and nuXmv
for formal verification, code complexity analysis utilizing OClint and srcSlice [505], and vulnerability detection
employing Frama-C and Slither for Ethereum smart contracts [506, 507]. Static analysis extends to specification
verification using Frama-C to verify AI-generated specifications [505].
Multi-agent architectures integrate static analysis into LLM-powered coding systems [124]. AutoSafeCoder
implements three-agent frameworks with Coding Agents, Static Analyzer Agents, and Fuzzing Agents [138].
Reinforcement learning frameworks like REAL use program analysis-guided feedback combining automated


                                                         26
                               A Survey of Vibe Coding with Large Language Models



signals with unit tests [508]. Applications span general programming detecting vulnerabilities in C [509], hardware
description language generation with AutoChip [510], and HDLAgent supporting multiple languages [511].

7.1.3    Runtime Compilation Feedback
LLMs produce functional code but often struggle with correctness and optimization [512, 513, 253]. LLM-
based coding agents leverage dynamic feedback from compilation and runtime processes to iteratively improve
code output, transforming traditional one-shot code generation paradigms into iterative refinement processes
[488, 514–516]. Coding agents utilize several feedback categories: binary pass/fail indicators, compilation feedback
identifying syntax errors, failed tests feedback providing expected values with tracebacks, execution feedback
providing runtime information, LDB feedback printing intermediate variable values, self-feedback determining
compilation success, verification feedback checking unit tests and formal verification, and verbal feedback
providing human-readable correction suggestions [243].
Several frameworks leverage compilation feedback: CompCoder implementing three-stage pipelines improving
compilation success from 44.18% to 89.18%, CodeRL using actor-critic reinforcement learning with unit test
signals [245, 279, 246], RLCF training pre-trained LLMs using feedback from grounding functions for code quality
assessment [162], INTERVENOR using compiler feedback for agent collaboration, CoCoGen using static analysis
to identify mismatches and iteratively fixing errors using compiler feedback and repository information [117],
self-debugging frameworks like Cycle, LDB, and ReflectionCoder leveraging runtime execution information for
iterative refinement [111, 163], CompilerGPT automating interaction between compilers, LLMs, and evaluation
systems [515], and hardware-specific frameworks like AutoChip for RTL/Verilog generation demonstrating
domain-specific effectiveness [511, 169].
Integration of compilation and runtime feedback finds applications across code translation ensuring semantic
correctness through methods like TransMap and AlphaTrans [164], iterative code refinement where execution
feedback serves as supervisory signal [165–167, 26], automatic program repair showing iterative patch creation
benefits [168], visualization [167], and performance optimization where compilers provide structured feedback
explaining optimization failures.

7.2     Execution Feedback
7.2.1    Unit Test Execution Results
Unit test execution results serve as critical feedback mechanisms allowing coding agents to verify generated
code meets requirements [528, 181, 175, 509]. Results provide varying detail levels: simple correctness feedback
indicating pass/fail through binary signals, and detailed execution results including runtime errors and specific
test failure information. Test-Driven Development (TDD) has proven its merit, requiring developers to write tests
before the functional code [529, 253, 530]. Test validation frameworks like PyTest, unittest, and JUnit serve as
primary mechanisms generating feedback revealing runtime errors [524, 531, 243].
Unit test results serve multiple applications: reinforcement learning approaches leveraging execution feedback,
search-based debugging where algorithms like BESTER use execution feedback with self-reflection for automated
repairs [275], code sample filtering using test outcomes with CodeT achieving 65.8% pass@1 on HumanEval,
performance optimization analyzing execution time data [176, 170], multi-agent systems employing execution
feedback [171, 532, 13], and test-time scaling strategies generating multiple candidates.
Integration methodologies include reinforcement learning approaches fine-tuning models using test execution
outcomes assigning rewards based on results using algorithms like REINFORCE or PPO optimizing model
behavior through iterative feedback loops [245, 246], code selection and filtering using execution feedback to
identify best solutions with AlphaCode generating millions of programs filtering incorrect solutions based
on test outcomes [269], sophisticated approaches like CodeT automatically generating test cases performing
dual execution agreement analysis considering both output consistency and cross-sample agreement [176], and
structured validation frameworks implementing unit testing as iterative refinement mechanisms where agents
continuously generate test cases, evaluate outputs against functional requirements, and refine code until all tests
pass.
Despite promising applications, significant challenges limit effectiveness: unreliability of AI-generated unit tests
where code refinement depends entirely on generated unit test correctness, with studies revealing models generate
unreliable self-tests in abundance potentially misleading self-improvement processes and exacerbating program


                                                        27
                                     A Survey of Vibe Coding with Large Language Models


Table 4 Comparison of Coding Environments and Datasets for AI-Assisted Software Engineering.

 Environment/Dataset   Year   Task Scale                     Data Source                             Task Level          Interaction & Evaluation

 SWE-Gym [299]         2024   2,438 verified instances (11   Constructs interactive execution en-    Repository-level    Agents modify files and run unit
                              repos); 64,689 raw in-         vironments from GitHub issues in        RL environment      tests within Docker; rewards are
                              stances                        11 Python repos; each environment                           given when all tests pass, support-
                                                             includes the full codebase and fail-                        ing iterative RL training
                                                             ing tests
 SWE-smith [310]       2025   50k tasks (250+ environ-       Automatically converts any GitHub       Repository-level  Environment         provides     file-
                              ments); 5,016 trajectories     repository into a SWE-gym envi-         RL environment    localization and repair tools;
                                                             ronment, corrupting unit tests to                         agents interact through code edits
                                                             generate interactive tasks                                and receive rewards when modified
                                                                                                                       code passes tests
 R2E-Gym [517]         2025   8.1k tasks (13 repos)          Procedurally generates interactive      Commit/Repository-Agents interact with full reposito-
                                                             RL environments from commit his-        level    environ- ries via Docker; hybrid execution
                                                             tory using the SWE-Gen pipeline         ment              and static verifiers produce the re-
                                                                                                                       ward signals
 DeepSWE [518]         2025   ≈4.5k problems                 Builds a code RL environment by         Repository-level  Environment defines four actions
                                                             filtering R2E-Gym tasks to avoid        RL environment    (execute, search, edit, finish); re-
                                                             overlap with evaluation benchmarks                        ward is given only when all tests
                                                                                                                       pass within a time limit
 SWE-rebench [519]     2025   21,336 tasks                   Creates interactive environments        Repository-level  Uses a unified scaffold: agents edit
                                                             from mined PRs with 1–15 file mod-      interactive envi- code and run tests; environment re-
                                                             ifications and clear descriptions       ronment           wards successful test passing, with
                                                                                                                       30% of repositories building suc-
                                                                                                                       cessfully
 Multi-turn    SWE     2025   7,249 tasks                    Filtered subset of SWE-rebench          Repository-level  Agents can execute shell com-
 RL Env. [520]                                               tasks preprocessed into a multi-turn    multi-turn envi-  mands, edit files, search and submit
                                                             RL environment                          ronment           patches; reward equals test success
                                                                                                                       minus step penalties, encouraging
                                                                                                                       efficient interactions
 SWE-RL [315]          2025   ≈1.1×107 PR instances          Offline repository of PR in-            Commit-level      Non-interactive; used for offline RL
                                                             stances curated from GitHub events      offline dataset   and reward models, where similar-
                                                             (2015–2024), including bug-fix issues                     ity between generated and ground-
                                                             and patches                                               truth patches is computed with se-
                                                                                                                       quence matching
 COFFEE-               2024   Multiple problems (5 diffi-    Builds a feedback environment from      Function-level    Agents generate feedback; the en-
 GYM [521]                    culty levels)                  human code submission histories         feedback envi-    vironment applies edits and runs
                                                             with paired wrong/correct solutions     ronment           ∼35.5 tests per problem to produce
                                                                                                                       a reward
 EvoCodeBench [522]    2024   275 samples (initial ver-      Curates repository-level generation     Repository-level  Agents must generate complete
                              sion)                          tasks across 25 repos; environment      generation envi-  repositories; evaluation uses Pass@k
                                                             updated every 6 months to avoid         ronment           and domain-specific metrics
                                                             leakage
 DA-Code [523]         2024   ≈500 data analysis tasks       Aggregates real-world data analysis     Notebook-level      Provides an executable sandbox for
                                                             tasks covering cleaning, ML, and        interactive envi-   SQL/Python; evaluation based on
                                                             exploration in interactive notebooks    ronment             correctness of analysis results
 DS-1000 [524]         2024   1,000 problems                 Collects function-level tasks from      Function-level      Agents write code to pass test_-
                                                             seven data science libraries, each      offline tasks       execution and test_string; limited
                                                             with prompt, solution, and tests                            interaction beyond code submission
                                                                                                                         and test running
 BioCoder [525]        2024   1,026 Python functions +       Extracts bioinformatics code from       Function-level      Evaluated using fuzz testing; en-
                              1,243 Java methods + 253       GitHub and Rosalind projects, em-       environment         vironment requires handling long
                              Rosalind problems              phasizing cross-file dependencies       with long con-      prompts (up to 2,600+ tokens) and
                                                                                                     texts               cross-file reasoning
 MLE-Dojo [526]        2025   200+ Kaggle tasks              Encapsulates Kaggle competitions        Competition-        Agents can request information, val-
                                                             into an RL environment with uni-        level interactive   idate and execute code; reward is
                                                             fied data, evaluators, and leader-      environment         based on relative performance via
                                                             boards                                                      HumanRank
 AgentPack [527]       2025   1.3M code edits                Collects code edits co-authored by      Commit-level        Offline supervised dataset with no
                                                             agents (Claude, Codex, Cursor) and      offline dataset     interactive environment or defined
                                                             humans from Git histories                                   RL reward




errors creating circular dependency problems [172, 173], scalability constraints as generating and executing
multiple test cases for each code candidate requires significant computational resources particularly when systems
generate thousands of code samples, and limited test coverage as automatically generated tests may not capture
all edge cases or complex scenarios potentially allowing buggy code to pass initial validation while failing in
real-world deployment scenarios.

7.2.2   Integration Test Feedback
Integration test feedback involves executing automated tests against LLM-generated code and using resulting
feedback to guide subsequent iterations, building upon traditional software testing but adapting for unique
challenges of AI-generated code [492]. The fundamental premise relies on creating closed-loop systems where



                                                                         28
                                A Survey of Vibe Coding with Large Language Models



coding agents learn from execution feedback rather than relying solely on static analysis or human review.
Development of integration testing frameworks has evolved to address unique challenges of testing LLM-powered
systems [26], with OpenHands framework representing notable advancement pioneering end-to-end agent test
frameworks combining traditional integration testing with foundation model mocking techniques [183, 179, 533].
Practical implementation relies on sophisticated multi-agent architectures where test executor agents serve as central
coordinators managing interaction between code generation and test validation activities. Effectiveness varies
significantly based on type and structure of feedback, with research demonstrating structured feedback formats
achieving superior results, with test feedback leading to highest repair success rates [492]. The iterative nature
plays crucial roles with multiple rounds enhancing repair performance, though research indicates diminishing
returns after two or three iterations [492].
Filtering and selection of generated code samples involves several established approaches. Key methods include
test-based filtering using unit test outcomes [269], dual execution agreement evaluating code based on output
consistency [176], verification-based reranking training specialized verifiers [534, 535], semantic execution analysis
using execution results to capture semantic features [167], and probabilistic marginalization combining programs
with identical execution results [176].

7.2.3    Runtime Error and Exception Handling
Research frameworks have systematically categorized runtime errors when LLMs generate code identifying five
primary error types: syntax errors, parameter and attribute errors, output type errors, logical answer errors, and
timeout and runtime errors [516]. Beyond execution-level errors, comprehensive taxonomies identify 36 exception
types across 12 agent artifacts distinguishing failures across reasoning, planning, and execution phases [74, 74].
Research has developed several approaches for detecting and analyzing runtime errors: simplest approaches using
binary feedback providing only pass/fail indicators [428], sophisticated systems offering failed tests feedback
including expected versus actual values with runtime error tracebacks [429], advanced frameworks providing
failed and passed tests feedback with comprehensive input/output information [167], sophisticated debugging
approaches using control flow analysis and variable tracking with systems like LDB [429], and emerging print
debugging and reflection-based methods [111, 428].
Several specialized frameworks provide comprehensive exception management: knowledge-driven approaches
where Knowledge-driven Prompt Chaining decomposes code generation into AI chains with iterative check-
rewrite steps [178], multi-agent frameworks like Seeker using specialized agents [180], PyCapsule employing
programmer agents and debugging alongside executor agents enhanced by error handlers [174], runtime error
recovery systems like Healer with GPT-4 successfully handling 88.1% of AttributeErrors [182], and iterative
self-correction mechanisms using structured feedback loops [177].
Self-reflection represents critical capability for LLM-based coding agents defined as processes where models review
earlier outputs and attempt to identify logical flaws. When given buggy programs with execution traces, errors, or
test results as input, LLMs produce debugging instructions through self-reflection [118]. Dynamic self-correction
through execution feedback represents sophisticated approaches where systems append diagnostic information to
original prompts [177]. Modern frameworks have developed increasingly sophisticated debugging methodologies
including print debugging methods, reflection-based approaches, hierarchical debugging tools, and advanced
systems like CYCLE [111, 163].

7.3     Human Feedback
7.3.1    Interactive Requirement Clarification
Large Language Models have demonstrated remarkable capabilities in automatically generating code from natural
language requirements [35], though critical gaps exist between current LLM behavior and human problem-solving
approaches when dealing with ambiguous requirements [188, 536, 497]. While human developers typically seek
additional information through interactive clarification, current LLM-based code generation approaches lack
mechanisms for clarifying unclear requirements, with empirical studies revealing state-of-the-art Code LLMs
generate code outputs in over 63% of ambiguous scenarios without seeking necessary clarifications [188]. This
limitation has significant implications compounded by the fact that 72% of software defects in production
environments originate from misunderstood requirements [536, 184, 471].


                                                         29
                               A Survey of Vibe Coding with Large Language Models



Detection of ambiguous requirements has emerged as critical first steps with the most widely adopted approach
being code consistency checking pioneered by ClarifyGPT which determines whether given requirements are
ambiguous by generating multiple code solutions [188]. Despite methodological advances, empirical findings
reveal significant limitations with systematic evaluations showing state-of-the-art models struggle to distinguish
between well-specified and underspecified instructions [243, 112].
Generation of effective clarification questions represents core technical challenges with foundational approaches
established by ClarifyGPT using prompt-based question generation, demonstrating significant improvements
elevating GPT-4’s performance from 70.96% to 80.80% on MBPP-sanitized benchmarks [188]. To address limitations,
fine-tuning approaches have emerged with ClarifyCoder representing notable advances using synthetic data
generation and instruction-tuning [185, 536, 188, 113].
Evaluation of interactive requirement clarification systems has evolved toward systematic assessment frameworks.
Empirical findings reveal significant performance gaps—while models struggle to distinguish between well-
specified and underspecified instructions, when they do interact for underspecified inputs they effectively obtain
vital information from users leading to significant improvements with evaluations showing average absolute
improvement of 45.97% in pass@1 code generation accuracy within 5 user interactions [243, 112].

7.3.2   Code Review Feedback
Development of large language models has created urgent needs to align these powerful systems with human
intentions and preferences, with the challenge lying in effectively utilizing qualitative human feedback [223].
Foundations of this field can be traced to preference-based reinforcement learning (PbRL), with major breakthroughs
coming with Christiano et al.’s introduction of RLHF [537].
RLHF framework follows structured approaches beginning with SFT on high-quality demonstration data, with
core innovation lying in training reward models to approximate human preferences from preference data where
humans indicate preferred responses between pairs of options serving as foundations for subsequent reinforcement
learning optimization [189]. The field gained significant momentum when scaled to large language models [538]
with InstructGPT demonstrating potential of applying RLHF to large-scale models like GPT-3 enabling alignment
with user instructions across wide ranges of tasks [8], while DPO has emerged as notable simplification allowing
language models to be trained directly on preference data without explicit reward modeling or reinforcement
learning optimization stages [2, 70, 186, 68, 227].
Core RLHF methodology consists of three distinct stages: processes begin with supervised fine-tuning on high-
quality demonstration data, second stages focus on reward modeling training reward models to approximate
human preferences based on Bradley-Terry models, and final stages involve reinforcement learning optimization
where models are refined using RL algorithms like PPO [539, 2, 190, 68]. Despite effectiveness, traditional RLHF
pipelines are notably complex and computationally expensive [68].
Traditional RLHF pipelines suffer from inherent complexity and instability creating practical barriers [68]. Major
practical constraints include substantial costs and efforts required for human annotation often requiring thousands
of human comparisons to train reliable reward models [191, 540]. Scalability challenges become even more
pronounced with complex tasks as dialogues become longer spanning multiple turns greatly increasing annotation
difficulty [191].
Given these limitations, complexity and instability of traditional RLHF has motivated development of more
direct approaches with most significant breakthrough coming with DPO eliminating explicit reward modeling
stages and directly optimizing policies using preference data leveraging mathematical relationships between
optimal policies and reward functions under Bradley-Terry preference models enabling preference optimization
through simple classification objectives that are stable, performant, and computationally lightweight [68]. Beyond
DPO, researchers have explored alternative frameworks. Preference Ranking Optimization (PRO) addresses
limitations of RLHF by extending pairwise preference comparisons to accommodate human preference rankings
of any length directly fine-tuning language models through iterative contrast learning [541]. Nash Learning
from Human Feedback (NLHF) offers novel approaches learning preference models conditioned on two inputs
pursuing strategies consistently generating responses more preferred than competing policies [542]. Diffusion-DPO
demonstrates effectiveness in text-to-image generation [543, 544].
Substantial costs required for human annotation in traditional RLHF have motivated researchers to explore
AI-generated feedback as scalable alternatives with RLAIF introducing frameworks where AI-generated feedback


                                                        30
                                A Survey of Vibe Coding with Large Language Models



replaces human annotations with off-the-shelf LLMs serving as feedback models to evaluate responses based
on predefined principles demonstrating performance comparable to traditional RLHF methods across tasks like
summarization and dialogue generation [190, 2, 538, 187]. AutoPM represents another approach employing LLMs
to automatically generate preference data by eliciting pairwise comparisons based on helpfulness, honesty, and
harmlessness criteria enabling training of preference models without extensive human supervision [190, 539].

7.4     Self-Refinement Feedback
7.4.1    Self-Evaluation and Critique
Foundational architecture of self-refinement in LLMs centers around iterative feedback loops mirroring human
revision processes with most notable framework Self-Refine enabling LLMs to improve outputs through structured
three-step processes: generating initial responses, prompting models to critique own outputs, and refining responses
based on feedback [210, 105, 545]. Processes follow key steps: initial generation, self-critique, refinement, and
iteration, with notably Self-Refine requiring no additional training data or fine-tuning [105, 72]. Multiple variants
have emerged including Recursively Criticizes and Improves (RCI), CRITIC, and Self-Correct [192, 210].
Executable nature of code provides unique advantages for self-refinement in programming tasks as execution
results offer immediate and objective feedback [286, 105, 201]: Self-Debugging equipping models with ability
to autonomously detect and repair errors, Self-Edit incorporating dedicated fault detection phases, CodeChain
introducing self-revision mechanisms, Self-Collaboration using simulated internal dialogue, LeTI redefining code
generation as interactive dialogue-driven processes, and OpenCodeInterpreter unifying generation, execution, and
refinement.
Self-evaluation represents critical components encompassing models’ ability to assess quality of own generated
outputs including reasoning steps and confidence scores with multiple techniques having emerged including
self-consistency, self-correction, self-evolution, and self-feedback [193]. Self-critique and feedback generation
processes involve models acting as critics analyzing own outputs [105, 114]. However, critical analysis reveals
important limitations with research indicating self-correction works well primarily in tasks that can use reliable
external feedback, and large-scale fine-tuning appears necessary to enable effective self-correction [193, 546].
Critique generation processes involve models analyzing own outputs and providing structured suggestions for
improvement [105]. Advanced critique frameworks implement multi-dimensional evaluation systems with carefully
designed prompts instructing models to assess outputs based on specific criteria [114, 105, 201]. Performance
gains from self-refinement methods have been substantial including GPT-4 achieving gains of 8.7 points in code
optimization and 13.9 points in code readability when using Self-Refine prompting [210].

7.4.2    Multi-Agent Collaborative Feedback
Multi-agent systems employ several distinct feedback mechanisms enabling collaborative code improvement
[194, 111] with most fundamental distinctions lying between inter-agent feedback and self-feedback mechanisms,
with inter-agent feedback involving agents providing constructive criticism to each other based on interactions
and collaborations helping agents identify improvement areas and adapt strategies for continuous learning
within systems [195, 10, 127]. In multi-core agent systems, intra-agent feedback emerges as agents exchange
information and share observations including shared observations, alternative perspectives on problems, and
evaluations of proposed plans promoting collaborative problem-solving and cross-validation enhancing overall
system robustness through collective intelligence [196]. Self-feedback mechanisms allow agents to assess own
performance and identify improvement areas through self-assessment based on predefined criteria or goals, while
external feedback-based optimization leverages evaluative signals from external models or agents to refine agent
behavior integrating external reflections and corrections to enhance robustness and adaptability [195].
Core collaborative feedback mechanisms center on peer-reflection involving information exchange through role
specialization and structured communication. Self-feedback loops represent another key collaborative mechanism
where agents iteratively refine strategies based on both quantitative numerical evaluations and qualitative
natural language assessments [197]. Feedback-refine cycles enable agents to store language-level memories and
collaboratively iterate on solutions with parallel agents exchanging critiques [115]. Mutual assessment and pruning
mechanisms facilitate collaborative optimization where agents produce multiple candidates and evaluate outputs
from other agents [243].



                                                         31
                                    A Survey of Vibe Coding with Large Language Models




                          Structured
             Waterfall        &                   TDM                                    Fast & Rigid
           Constrains        Safe

                            Agile                          PDM

                                       RAD                            ICCM
                                                                                            Fast
                        Slow & Flexible                                         UAM          &
                                                                                            Risky
                                                  Development Speed
Figure 8 Comparison of Vibe Coding Development Models Framework With Software Development Models [551–553].


Self-refinement mechanisms in multi-agent coding systems operate through iterative feedback-refine cycles
demonstrating that when run in parallel with agents exchanging critiques feedback-refine cycles significantly
boost code generation quality [115]. Hybrid value functions represent key advancements incorporating both
quantitative and qualitative assessment mechanisms [197]. Circular optimization mechanisms create continuous
improvement loops through self-reflection scoring systems with notable frameworks like CodeCoR introducing
reflection agents between code generation, testing, and repair stages [243, 127].

7.4.3   Reflection and Memory-Based Feedback
Several foundational frameworks have emerged as core approaches for implementing self-refinement in large
language models with most notable being Self-Refine which introduced comprehensive end-to-end self-correction
approaches [198, 105, 547, 199]. Reflexion represents another foundational framework using verbal reinforcement
to help agents learn from prior failures incorporating three key LLM-based modules: Actors that generate actions,
Evaluators that assess results, and Self-Reflection models that analyze failure cases [201, 199, 548].
Memory architecture represents critical components in self-reflection systems with most frameworks adopting
dual-memory approaches separating short-term and long-term memory components, with trajectory history
serving as short-term memory while outputs from Self-Reflection models are stored in long-term memory
[201, 79, 272, 200, 90, 549]. Transformation of environmental feedback into memory representations is key
innovation with Self-Reflection models taking sparse reward signals along with current trajectory and persistent
memory then generating nuanced and specific feedback, effectively converting scalar rewards into natural language
feedback [201, 547, 105].
Coding domain has emerged as particularly fertile ground for self-refinement applications with numerous
frameworks specifically designed to leverage unique feedback mechanisms with program execution feedback
representing most common approaches where frameworks like Self-Edit and Self-Evolve execute initial programs
on test cases and provide execution results back as feedback [550]. Multi-agent debugging architectures have
also gained prominence with frameworks like Refinement and Guidance Debugging (RGD) system introducing
multi-LLM-based agent debuggers [118].
Performance evaluation of self-refinement frameworks reveals significant advances with Reflexion achieving
particularly notable results demonstrating 91% pass@1 accuracy on HumanEval coding benchmark surpassing
previous GPT-4 performance of 80% representing 11 percentage point improvements achieved through verbal
reinforcement [201]. Self-Refine framework has demonstrated consistent performance gains achieving approx-
imately 20% absolute improvement in task performance across diverse applications while requiring minimal
computational resources [548].




                                                           32
                                A Survey of Vibe Coding with Large Language Models



8     Vibe Coding Development Models
8.1   Framework Principles
We propose a three-dimensional classification framework for categorizing Vibe Coding development paradigms
based on: (1) human quality control level, (2) structured constraint mechanisms, and (3) context management
capability. The human quality control dimension reflects the extent to which developers review AI-generated
code, comprehend the underlying logic, and perform manual corrections and optimizations. The structured
constraint mechanism dimension captures whether the development process incorporates pre-planning and design
phases, automated testing verification, and rule-based constraints. The context management capability dimension
assesses the utilization of codebase indexing, project documentation context, and retrieval-augmented generation
techniques. Through different combinations of these three dimensions, as shown in Figure 8, we identify five
core Vibe Coding development models: Unconstrained Automation Model (UAM), Iterative Conversational
Collaboration Model (ICCM), Planning-Driven Model (PDM), Test-Driven Model (TDM), and Context-Enhanced
Model (CEM), where the first four represent distinct workflows, while the fifth serves as a horizontal enhancement
capability that can be flexibly integrated with any of the preceding four models.
These models are not mutually exclusive categories but rather composable development strategies: PDM can be
combined with TDM to achieve high-quality development of complex projects, while ICCM can be integrated with
CEM to support maintenance of large codebases. The essential distinction across all models lies in the boundary
of human-AI collaboration—specifically, the role humans assume in the AI-assisted programming process: in
UAM, AI dominates while humans merely provide requirements; in ICCM, humans review while AI executes; in
PDM, humans design while AI implements; and in TDM, machines verify while humans define standards.

8.2   Unconstrained Automation Model (UAM)
This model represents the development approach most closely aligned with the original definition of Vibe
Coding, characterized by complete trust in AI output, minimal code scrutiny, and correctness validation through
functionality testing rather than code comprehension. Whether developers issue short instructions through
high-frequency dialogues or allow AI agents to autonomously decompose tasks and iterate multiple rounds, any
workflow that accepts output without deep code inspection falls within this paradigm. This model emphasizes
high development velocity and low technical barriers, enabling non-programmers to rapidly construct application
prototypes, with development timelines compressed to several times or even dozens of times faster than traditional
approaches. This paradigm bears conceptual similarity to Rapid Application Development (RAD) methodologies
in traditional software engineering, which similarly emphasize rapid prototyping and shortened development
cycles over extensive upfront planning [554, 553]. Both approaches prioritize speed and iterative refinement,
though UAM relies on AI automation whereas RAD depends on specialized development tools and frameworks
[273].
However, this model entails significant risks and costs. The absence of human code review allows AI-generated
code to potentially harbor security vulnerabilities, accumulate technical debt, and produce code structures that
are difficult to maintain. As code scales beyond the developer’s comprehension capacity, debugging becomes
extremely challenging, and unpredictable AI behavior may lead projects into critical impasses. Consequently,
UAM is suitable only for low-risk scenarios such as disposable prototypes, proof-of-concepts, and personal utilities,
while it is not recommended for production systems, safety-critical applications, or codebases requiring long-term
maintenance.

8.3   Iterative Conversational Collaboration Model (ICCM)
ICCM positions AI as a programming partner rather than a fully autonomous agent, constructing software through
continuous dialogue and iterative cycles while humans maintain comprehensive oversight, understanding, and
control over code quality. This model requires developers to review and comprehend each AI output before
deciding whether to accept it, forming an iterative workflow of “AI generates → human reviews and understands
→ testing validates → acceptance decision.” This approach parallels pair programming in agile development
[555, 156], where AI assumes the Driver role by rapidly producing code while humans serve as the Navigator,
guiding direction and reviewing quality [556]. Empirical studies on pair programming have demonstrated
improvements in code quality and knowledge transfer [557, 558], benefits that similarly manifest in ICCM through



                                                         33
                                A Survey of Vibe Coding with Large Language Models



the continuous human-AI collaboration loop. The iterative nature manifests in continuous improvement and
incremental refinement across multiple dialogue rounds.
This model maintains high development velocity while ensuring code quality, allowing developers to benefit
from AI productivity gains through full participation while guaranteeing that code conforms to project standards
and team conventions. Compared to UAM, ICCM significantly reduces the accumulation of technical debt and
security vulnerabilities, yielding code with superior maintainability and team readability. However, this model
demands substantial developer experience and discernment capability; novices may erroneously trust AI output
due to insufficient judgment, while frequent reviews and testing increase cognitive load and time costs. This
model is appropriate for professional development environments, medium-to-large projects requiring long-term
maintenance, and team collaboration scenarios.

8.4   Planning-Driven Model (PDM)
PDM emphasizes establishing clear development plans and design specifications by humans before AI coding
commences, then guiding AI to implement progressively according to the plan, applying the “architecture-first”
philosophy of traditional software engineering to Vibe Coding. Developers invest time in organizing module
decomposition, data structures, and feature lists, typically producing a three-document system comprising technical
specification documents, coding rule files, and implementation plans, which serve as the “blueprint” for AI
coding. This model conceptually aligns with the waterfall model in traditional software development [551, 273],
where sequential phases—requirements analysis, design, implementation, and testing—proceed in a structured,
linear fashion. However, PDM retains greater flexibility than traditional waterfall approaches, as AI can rapidly
iterate on implementations while adhering to the established architectural framework [482]. This model parallels
the traditional development division where architects design while teams implement, except here the “team” is
undertaken by AI, with humans playing the roles of architect and project manager.
The core value of this model lies in ensuring directional correctness through upfront planning, avoiding directional
drift and repetitive trial-and-error during development. AI working within explicit frameworks produces more
structured and consistent code, with final outputs exhibiting superior modularity and architectural coherence,
particularly suitable for complex full-stack applications and projects requiring clear module boundaries. A crucial
implementation strategy is adopting vertical slice architecture—organizing code by business functionality rather
than technical layers, with each feature implemented end-to-end from database to UI, providing clear working
boundaries for AI. Although upfront investment in creating planning documents is required, this investment
effectively reduces subsequent maintenance costs and refactoring needs, making projects more comprehensible
and amenable to team collaboration.

8.5   Test-Driven Model (TDM)
TDM applies the TDD philosophy from traditional software engineering to Vibe Coding, with the core idea
of first defining tests and acceptance criteria, having AI generate code satisfying the tests, and ensuring code
quality through automated testing rather than manual review. Unlike other models that constrain AI behavior
through natural language descriptions or documentation, TDM employs test cases as precise constraints on AI,
where tests serve as specifications, explicitly defining objective success criteria. This model directly inherits from
TDD practices established in software engineering [529, 156], following the classic red-green-refactor cycle: write
failing tests, implement code to pass tests, then refactor for quality [274]. Humans write test cases, AI writes
implementation code, iterating development through the classic TDD cycle.
The advantage of this model lies in replacing human judgment with machine verification, providing an objective
quality assurance mechanism. When test coverage is comprehensive, code passing tests can be confidently assumed
to meet behavioral requirements, reducing developers’ burden of line-by-line auditing and communication costs.
When tests fail, failure messages precisely pinpoint issues, enabling efficient AI modifications. Additionally, this
model typically integrates with automation tools such as pre-commit hooks, enforcing quality gates including
testing, code formatting, and type checking before code submission. Although writing comprehensive test suites
requires upfront investment, this investment yields continuous quality assurance and refactoring confidence,
particularly suitable for core algorithm implementation, production-grade applications, critical business logic, and
codebases requiring long-term maintenance.




                                                         34
                                       A Survey of Vibe Coding with Large Language Models


Table 5 Comparative Analysis of Vibe Coding Development Models. Note: SE Counterpart refers to the corresponding software
engineering development model. CEM is a cross-cutting enhancement capability that can be combined with other models. The “+1 Level”
indicates improvement of one level when combined with base models, while “-1 Level” indicates risk reduction.

                Upfront    Human      Structured    Development    Code                                   Technical        SE
    Model                                                                    Maintainability   Security
              Investment   Control    Constraints      Speed      Quality                                 Debt Risk     Counterpart

    UAM        None         None        None           Strict       Low           Low            Low         High            RAD
    ICCM       Low          Strict     Moderate        High         High          High         Moderate      Low      Pair Programming
    PDM        High         Strict      Strict       Moderate       High          Strict         High        Low           Waterfall
    TDM        High        Moderate     Strict       Moderate       Strict        High           Strict      None            TDD
    CEM       Moderate        -           -          +1 Level     +1 Level      +1 Level       +1 Level    -1 Level           -



8.6     Context-Enhanced Model (CEM)
CEM is not an independent workflow model but rather a horizontal enhancement capability that can be layered
onto any other model, enabling AI to thoroughly understand existing codebases, technology stacks, and coding
conventions through technical means, thereby generating code better aligned with project environments. Core
technologies of this model include retrieval-augmented generation, codebase vector indexing, documentation
loading, and rule constraints. When users submit requirements, the system automatically retrieves relevant code
snippets, documentation, and rules from the project through semantic search engines, appending this context
to prompts provided to the LLM, enabling generated code to correctly invoke existing project code, adhere to
established coding styles, and conform to architectural conventions.
CEM significantly improves the accuracy and consistency of AI code generation, particularly demonstrating
efficacy in scenarios involving large codebase maintenance, cross-file modifications and refactoring, and global
operations. This model can be arbitrarily combined with the preceding four models: UAM combined with
CEM enables rapid yet moderately controlled prototype development; ICCM combined with CEM suits large
codebase maintenance; PDM combined with CEM ensures generated code complies with project specifications;
and TDM combined with CEM achieves superior code quality. CEM implementation typically adopts either
automatic retrieval or manual reference strategies, where tools create vector indices during project initialization
and intelligently retrieve relevant context during each dialogue.

9     Future Impact and Open Challenges
9.1     Reengineering of Development Process in Vibe Coding
The central premise of Vibe Coding—validating implementation through outcome observation rather than line-
by-line comprehension—introduces notable shifts in software development practices. Traditional Software De-
velopment Life Cycle (SDLC) models, from Waterfall to Scrum [139], were designed around assumptions of
human-authored code and predictable progression through discrete phases. Vibe Coding extends these models by
introducing AI-mediated development cycles that operate at accelerated timescales, prompting adaptations in
process design, expanding developer responsibilities, and surfacing new considerations in project management and
quality assurance. While empirical research on these impacts remains nascent and lacks longitudinal validation
[559], we can synthesize characteristics of this emergent paradigm [560, 20] to project its evolutionary trajectory
within existing development frameworks.

9.1.1       From Phased Lifecycles to Continuous Micro-Iterations
Building upon the traditional "edit-compile-debug" loop, Vibe Coding introduces a complementary "prompt-
generate-validate" cycle that operates at compressed timescales—from the weeks typical of Agile sprints to seconds
or minutes—thereby enabling more rapid iteration within the existing development framework. This accelerated
cycle is organized around "iterative goal satisfaction cycles" [560], where the developer’s workflow becomes a
continuous conversation with the coding agent, and each exchange generates a testable artifact [561, 562]. This
blurs the traditional boundaries between SDLC phases [562].

Requirements and Design. Instead of creating comprehensive design documents upfront, a developer can
engage in exploratory Vibe Coding [563]. The initial "vibe" might be a high-level user story, which the developer


                                                                   35
                               A Survey of Vibe Coding with Large Language Models



translates into a series of prompts to generate a functional prototype. The act of interacting with this AI-generated
prototype refines the requirements in real-time [561]. The design emerges organically from this iterative dialogue,
transforming the design phase from a distinct, pre-implementation step into a continuous, integrated activity.

Implementation. In this paradigm, the traditional implementation phase undergoes significant transformation,
with coding agents handling much of the syntactic construction while developers focus on higher-level orchestration.
The developer’s role evolves to encompass both traditional code authorship and emergent responsibilities as
system director and prompt engineer, with the balance tilting toward orchestration as agent capabilities advance
[564, 243]. While syntactic mastery remains foundational, the skill portfolio increasingly emphasizes the ability
to articulate intent, manage context, and evaluate agent output [565]—representing an expansion rather than
replacement of traditional programming competencies [560].

Testing and Validation. The developer’s primary "vibe check" is a form of continuous, informal acceptance
testing. However, this shift introduces ambiguity. While this immediate feedback is powerful for rapid iteration,
it lacks the rigor of formal Quality Assurance [566, 567]. The challenge lies in integrating structured testing
methodologies, such as the Test-Driven model [529] mentioned in our taxonomy, where the developer first defines
formal tests that the AI agent must then generate code to pass. This provides a concrete, verifiable "vibe" for the
agent to target.

9.1.2   Redefinition of Developer Roles and Skillsets
Effective adoption of Vibe Coding techniques requires developers to augment their existing skill sets with
capabilities in several emerging areas. Developer evaluation metrics are expanding beyond traditional code
production speed to incorporate competencies in prompt engineering, context curation, and system-level reasoning.

Intent Articulation and Prompt Engineering. Among these emergent capabilities, the ability to translate complex
requirements into effective prompts has proven particularly valuable in practice [20]. This is a creative and
analytical skill, requiring an understanding of how the model "thinks" without needing to understand its internal
architecture.

System-Level Debugging. When AI-generated systems fail, traditional line-by-line debugging becomes less
effective, as the generated logic can be opaque or non-intuitive [568]. Debugging evolves toward a process of
hypothesizing system-level failures, isolating problematic components through targeted tests, and then using
prompts to guide the AI to regenerate or patch the faulty section [569]. The focus shifts from algorithmic
debugging to behavioral debugging.

Context Curation and Management. As identified in our analysis, successful Vibe Coding depends heavily on
context engineering. Successful practitioners develop expertise in context curation, learning to feed agents the
right information—APIs, data schemas, existing codebase snippets, design patterns—to constrain generation space
effectively. The current ecosystem lacks mature open-source or commercial platforms specifically designed for this
dynamic context management in coding workflows [560, 570], making it a largely manual and ad-hoc process.

Architectural Oversight. With the AI handling implementation details, the human developer is elevated to the
role of an architect, making high-level decisions about system structure, component interaction, and technology
stacks. Their responsibility is to maintain the conceptual integrity of the project, a task that becomes more
challenging when the underlying code is not a direct product of their own mind.

9.1.3   New Challenges in Project Management and Collaboration
The Vibe Coding paradigm introduces significant hurdles for traditional project management. Estimating effort
for a task becomes difficult; a complex feature might be generated in minutes with the right prompt, while a
seemingly simple one could take hours of iterative refinement [571]. Code reviews, a cornerstone of traditional
quality control [572, 573], face new challenges in this context. When reviewing AI-generated code that the original
prompter does not fully understand, the review focus naturally expands beyond line-level correctness to also
include validation of prompt history, generated tests, and observed behavior against requirements [574–576].



                                                         36
                               A Survey of Vibe Coding with Large Language Models



Team collaboration also changes, with "pair programming" [577] potentially evolving into "mob prompting," [578]
where multiple developers collaborate on crafting the prompts and context for a shared AI agent. However, the
lack of documented case studies of Vibe Coding in large-scale enterprise projects means these process changes
remain largely theoretical and "under-explored" [579, 580, 560, 581–583] representing a critical area for future
empirical research.

9.2     Code Reliability and Security in Vibe Coding
The core trade-off of Vibe Coding is speed versus certainty. By abstracting away line-by-line code authoring, it
introduces a fundamental challenge to ensuring code reliability and security. When a developer validates code
based on its "vibe" or observed outcome, they may inadvertently approve implementations containing subtle but
critical flaws, from resource leaks and race conditions to severe security vulnerabilities. This risk is amplified
because LLMs are trained on vast corpora of public code, which inevitably includes buggy and insecure examples
[584–586]. The model may therefore reproduce these vulnerabilities in novel contexts. Consequently, for Vibe
Coding to be a viable methodology for production-grade software, it must be augmented by a new generation of
automated guardrails that operate continuously and intelligently within the development loop.

9.2.1    The Inadequacy of Manual Review
Traditional security assurance relies heavily on manual expert code review [587]. This practice is fundamentally
incompatible with the philosophy of Vibe Coding. It is paradoxical to gain development speed by having an
AI generate code, only to lose that speed by requiring a human to manually inspect every line of the output.
Furthermore, the developer prompting the AI may lack the specific security expertise to spot vulnerabilities in
the generated code, especially if it uses an unfamiliar library or a complex algorithm. The very premise of Vibe
Coding—trusting the agent to handle implementation details—necessitates a shift from human-centric inspection
to automated, real-time validation.

9.2.2    Architecting an Integrated Security and Reliability Feedback Loop
A robust Vibe Coding ecosystem must integrate automated analysis directly into the "prompt-generate-validate"
cycle. This goes beyond traditional CI/CD pipeline scans and requires real-time feedback embedded within the
developer’s interactive workflow. The architectural framework for this involves a tight coupling of the coding
agent with Static Application Security Testing (SAST), Dynamic Application Security Testing (DAST), and other
quality analysis tools.

Pre-Generation Contextual Analysis. The feedback loop should begin even before code is generated. An
intelligent agent, aware of the project’s security requirements, can analyze the developer’s prompt for security-
sensitive keywords (e.g., "authentication," "file upload," "SQL query"). This can trigger the agent to inject a
security-specific context, such as secure coding guidelines or templates, to steer the LLM towards generating
more robust code from the outset [588].

In-flight SAST Scanning. As the LLM streams its generated code into the developer’s IDE, a real-time SAST
engine should analyze it on the fly. This is a significant evolution from traditional SAST tools, which often require
complete, compilable code [589]. New, AI-enhanced SAST tools are emerging that can parse incomplete code
snippets and use machine learning to identify potential vulnerabilities with fewer false positives [590]. Platforms
like Amazon CodeWhisperer, with its integrated security scan feature [591] represent an early step in this direction.
A mature system would not just flag an issue but could feed the vulnerability information back to the LLM in a
closed loop, prompting it to self-correct its own output before the developer even sees the flawed version.

Sandboxed Dynamic Analysis. The "validate" step of the Vibe Coding loop is a critical intercept point. When
the developer executes the generated code to check its "vibe," the execution should occur within an instrumented
sandbox. This environment can perform just-in-time DAST, monitoring for runtime errors like memory leaks,
uncaught exceptions, and insecure network communications. It could also perform automated fuzzing on newly
generated API endpoints or data processing functions to test for edge-case vulnerabilities, providing immediate
feedback on the code’s dynamic behavior. The integration of static and dynamic analysis offers a complementary
approach to cover a wider range of potential issues [592, 593].



                                                         37
                               A Survey of Vibe Coding with Large Language Models



AI-Driven Threat Modeling. Beyond direct code analysis, an advanced Vibe Coding system could maintain a
dynamic threat model of the application. As a developer prompts the AI to add a new feature, a specialized
model could analyze the change in the context of the entire system, identifying potential new attack surfaces or
violations of existing security policies.

9.2.3    The Human-in-the-Loop as a Final Arbiter
Even with this sophisticated automation, the human developer remains the crucial arbiter. The role of the
developer is not eliminated but elevated. They are responsible for interpreting the outputs of these automated
security tools, resolving ambiguities, and making the final risk-based decision. The goal of the tooling is to
empower the developer with immediate, actionable intelligence, transforming the security process from a separate,
delayed phase into an intrinsic property of the code generation act itself. However, the technical specifications and
architectural blueprints for these deeply integrated, real-time security frameworks in Vibe Coding workflows are
not yet standardized [590, 20] and building them remains a major challenge for the research and tool-development
communities. Without solving this, Vibe Coding risks being confined to prototyping and non-critical applications,
unable to deliver on its promise for reliable, secure, and production-ready software systems.

9.3     Scalable Oversight of Vibe Coding Agents
As coding agents evolve toward autonomous code generation and deployment [243, 244], the scope of oversight
must expand from localized code verification to system-level governance. While Section 9.2 examined reliability
and security at the level of generated code, the next frontier concerns the supervision of agents that operate
continuously across repositories, pipelines, and environments. The central challenge lies in scaling assurance
mechanisms to match the increasing autonomy, speed, and operational complexity of these agents. Traditional
safeguards designed for human-authored code, for example, peer review [572, 594, 595], and post-deployment
auditing [596, 597], cannot feasibly monitor the millions of tokens or decisions that modern agents can generate
per hour. This growing disparity between agent capability and human supervision capacity has become a critical
obstacle to safe and accountable Vibe Coding workflows.

9.3.1    Emerging Risks of Vide Coding Workflow
Recent empirical analyses show that the introduction of autonomous agents into production pipelines correlates
with a tenfold increase in security warnings and technical debt accumulation within six months of adoption
[184, 584]. These findings reveal that human-centric verification processes fail to scale in environments where
agents autonomously generate, refactor, and redeploy code. The challenge is not simply one of quality assurance
but of maintaining interpretability and control in increasingly opaque decision pathways. Over-reliance on
autonomous coding agents introduces new classes of risks:

Cascading Errors Cascading errors occur when autonomous agents propagate flawed outputs through in-
terconnected software pipelines, transforming local inaccuracies into systemic failures. In multi-agent coding
environments, a single agent’s erroneous completion, such as generating insecure logic or malformed interfaces,
can trigger downstream faults as subsequent agents consume and redeploy its outputs. [598] demonstrate that
even minor perturbations from “faulty” agents can destabilize collaborative workflows, revealing the fragility
of LLM-based coordination without strong fault isolation. Similarly, [122] observe that emergent interactions
in AgentMesh amplify defects across code generation stages, while [599] characterize “butterfly effects” in LLM
toolchains, where trivial parameter-filling mistakes escalate into broad execution failures. Extending this view,
[600] find that scientific discovery agents exhibit correlated errors due to shared model assumptions and data
dependencies. Collectively, these studies underscore that LLM-mediated ecosystems lack the containment and
traceability necessary to prevent error propagation—rendering traditional debugging and peer review inadequate
in fully autonomous settings.

Dependency Proliferation Dependency proliferation denotes the uncontrolled expansion of software and library
linkages arising from agent-driven code generation and refactoring. Autonomous coding agents frequently
introduce or hallucinate dependencies beyond human oversight, compounding security and maintainability
challenges. [601] reveal that nearly one-fifth of packages suggested by code-generation models are nonexistent or
untrusted, creating opportunities for dependency-confusion attacks. [602] identify similar propagation patterns
in automated import suggestions, where vulnerable or deprecated modules reappear across independent tasks.


                                                         38
                                A Survey of Vibe Coding with Large Language Models



Furthermore, [603] show that fuzz-testing agents inadvertently inject unverified binaries during test synthesis, and
[604] demonstrate that build-automation agents routinely bypass provenance enforcement to optimize throughput.
These behaviors collectively inflate the software’s attack surface and contravene emerging SBOM (Software Bill of
Materials) and supply-chain transparency requirements. Dependency proliferation thus represents a structural form
of technical debt—an accreting web of opaque linkages that undermines the long-term security and interpretability
of autonomous development environments.

Alignment Failures Alignment failures emerge when an autonomous coding agent’s behavior diverges from the
developer’s intent or the organization’s governance norms [605]. Unlike deterministic compilers, agentic systems
interpret underspecified objectives probabilistically, optimizing for textual success rather than normative correctness.
[606] empirically show that goal-oriented coding agents often maximize explicit task metrics while disregarding
implicit safety or maintainability constraints embedded in natural-language prompts. Complementarily, [607]
describe “agentic misalignment” as an emergent property of reinforcement-trained code agents that overfit
reward structures, leading to functionally correct yet normatively undesirable behaviors. Such divergence erodes
accountability: once decisions are embedded in opaque model reasoning, tracing responsibility between human
and agent becomes ambiguous. Alignment failures therefore epitomize the epistemic opacity of autonomous
software systems, emphasizing the necessity of interpretable reward modeling, continuous supervision, and
human-in-the-loop intervention to ensure fidelity between developer intent and agent execution.
Addressing these systemic risks therefore necessitates a layered oversight architecture that integrates automated
analysis, formal verification, and human-in-the-loop governance. Modern static and dynamic analysis pipelines
now incorporate model-aware scanners capable of parsing incomplete code fragments and predicting vulnerabilities
in real time [509, 501], extending beyond conventional SAST [608] and DAST [609] frameworks by interfacing
directly with generation streams so that feedback can be injected before completion. Complementing these,
formal verification frameworks such as K ANI [610] and ACCA [611] demonstrate that lightweight proofs of
functional correctness can be applied to AI-generated modules, though scalability remains limited. Reinforcement-
learning-based watchdog agents offer a parallel safeguard: autonomous monitors trained to detect deviations from
project constraints, perform behavioral tracing, and intervene when agents exceed operational bounds [612, 613].
Collectively, these technologies lay the groundwork for continuous, adaptive oversight that aligns autonomous
coding processes with human accountability and system safety.

9.3.2   Toward Scalable Oversight Architectures
Achieving effective oversight in autonomous coding environments requires architectures that scale alongside agent
capabilities. A central idea in recent alignment research is enabling weak-to-strong generalization, using relatively
weak supervisors (humans or smaller models) to robustly guide much more powerful coding agents [614]. In
contrast to traditional settings where humans directly review weaker AI outputs, future agents may produce
“millions of lines of novel and potentially dangerous code” beyond any one human’s full comprehension. Scalable
oversight architectures address this gap by bootstrapping supervision: leveraging layered AI assistants and
automated checks so that even limited feedback can generalize into reliable constraints on agent behavior [615].
Alignment strategies such as iterated amplification, recursive reward modeling, and AI debate all share this goal,
allowing networks of weaker reviewers, often AIs themselves, to collectively evaluate and correct stronger agents’
decisions [616, 617]. This paradigm of “weak-to-strong oversight” underpins emerging proposals for governing
advanced code-generation systems, ensuring that each increase in agent autonomy is met with a proportional
increase in oversight capacity.

Hierarchical Weak-to-Strong Supervision. One approach is to organize oversight in tiers, where an automated
or human overseer supervises the coding agent at a high level, while that overseer is itself aided by subordinate
AI tools. This nested oversight or recursive supervision strategy allows complex judgments to be decomposed
into simpler subtasks manageable by weaker supervisors [615]. Recent studies demonstrate that a weak teacher
model’s guidance can be amplified through ensemble feedback and iterative training such that a much stronger
student model aligns with the teacher’s underlying intent [618]. OpenAI’s superalignment experiments showed
that fine-tuning GPT-4 under the noisy guidance of a GPT-2-level model, augmented with confidence-based
loss functions, could recover much of GPT-4’s original performance, achieving results comparable to GPT-3.5 on
complex reasoning tasks [614]. These findings suggest that, with appropriate training and oversight scaffolds,
coding agents can generalize from weak supervision to strong, aligned behavior. However, theory also indicates
that scalability has limits: oversight success rates decline sharply when an agent’s capability surpasses its overseer


                                                          39
                                 A Survey of Vibe Coding with Large Language Models



by several hundred Elo points [615], underscoring the need for continuous co-evolution between overseers and
agents.

Multi-Agent Debate and Critique. Another branch of scalable oversight employs multi-agent debate frame-
works [434, 619, 620], where coding agents critique each other’s code contributions to expose errors or unsafe
behaviors [621, 617]. Even a weaker human or AI judge can often identify the more truthful debater if the
setup incentivizes evidence-based argumentation [617]. In the software domain, D EBATE C ODER [622] applies
this principle to code generation: two large language models alternately produce and test code while generating
adversarial unit tests against each other. Each iteration forces self-correction until both code and tests converge
to correctness. This mechanism fuses automated testing and AI critique, forming a self-correcting oversight
loop that improves code quality and reliability without human intervention. Such multi-agent oversight reduces
dependence on a single reviewer and increases the likelihood that at least one agent detects subtle flaws or
misalignments in autonomously written code.

Continuous Monitoring and Automated Safeguards. Scalable oversight also requires continuous, model-aware
monitoring embedded throughout the software pipeline. Model-integrated static analyzers and runtime scanners
can evaluate partially generated code, flagging vulnerabilities or policy violations in real time [509, 501]. Reinforce-
ment learning–based watchdog agents extend this capacity: autonomous monitors trained to detect deviations
from specification and intervene or alert humans when the coding agent exceeds its operational bounds [612, 613].
Scalable oversight architectures for Vibe Coding agents converge on the principle of amplifying limited oversight
into broad governance. Through hierarchical weak-to-strong supervision, multi-agent critique, and automated
watchdogs, researchers aim to generalize weak feedback signals into strong preventive constraints that evolve with
agent capability [618, 614, 615]. The challenge lies not only in constructing these systems but in maintaining their
reliability as agents advance beyond direct human comprehension. By incrementally upgrading oversight tools
alongside the agents themselves, the field moves toward an adaptive architecture, one where even superhuman
coding systems remain answerable to human-aligned constraints.

9.4     Human Factors in Vibe Coding
In contrast to traditional programming where developers directly manipulate code logic, Vibe Coding emphasizes
context engineering and human-AI collaboration [28, 623]. We examine three key aspects of this transformation:
the shift in developers’ mental models, the evolution of required skill sets, and the reconfiguration of team
collaboration and responsibility [624].

9.4.1    Mental Model Shift: From Code Logic to Context Engineering
Software engineering has historically been conceptualized as the process of translating requirements into algorithms
and data structures expressed through code [625]. In Vibe Coding, however, developers increasingly act as context
engineers, where the central task involves curating and structuring prompts, providing background information,
and defining system constraints that guide AI-generated output [31, 626, 28]. Recent studies describe this shift as
the emergence of prompt engineering [627, 628]. Rather than solving low-level implementation details directly,
developers are expected to design high-level problem frames, construct testing scaffolds, and supply contextual
cues, followed by iterative refinement of AI outputs [629].
Empirical studies on GitHub Copilot and similar tools indicate that developers often adopt a “specify–verify–revise”
workflow, where prompting substitutes for manual implementation, and verification becomes the central locus
of human activity [630–632]. This transformation aligns software engineering more closely with socio-technical
practices such as product design and requirements engineering, where the clarity of intent expression is as
important as technical implementation skills [633].

9.4.2    Evolving Developer Skill Sets
The skill profile required of software developers is undergoing reconfiguration. Beyond conventional programming
expertise, Vibe Coding requires several new competencies:
      • Prompting and context design. Developers must acquire the ability to formulate prompts that encode
        both intent and constraints [31, 627, 28]. This includes modular prompt construction, retrieval-augmented


                                                          40
                                 A Survey of Vibe Coding with Large Language Models



        prompting, and the maintenance of prompt libraries as formal engineering artifacts [628].
     • Task decomposition. Research demonstrates that LLM-based agents perform more effectively when complex
       problems are decomposed into smaller, explicitly defined subtasks [634, 629]. This approach resonates with
       TDD but shifts the emphasis from manual implementation to steering AI behavior [530].
     • Quality supervision and verification. Studies highlight persistent issues in AI-generated code, including
       subtle bugs, security vulnerabilities, and hallucinated APIs [584, 635, 585, 636]. Developers must develop
       skills in automated testing, static analysis, and formal verification techniques as mechanisms of oversight
       [637, 632].
     • Agent governance and security. In addition to technical supervision, developers are increasingly responsible
       for managing access control, execution privileges, and provenance tracking of AI-generated outputs [624].
       Literature on AI safety emphasizes the importance of least-privilege principles and verifiable provenance
       [638].
These emerging skill demands reposition developers from code producers to supervisors and orchestrators of
AI-driven workflows, aligning with calls for human-in-the-loop governance in software engineering [639, 640].

9.4.3    Team Collaboration and AI Integration
The growing autonomy of coding agents introduces new challenges to team dynamics and responsibility allocation
[640, 641]. Several empirical studies suggest that AI tools are increasingly capable of assuming roles traditionally
associated with junior developers, such as generating boilerplate code, producing documentation, or proposing
test cases [642, 643, 633]. In this sense, AI systems can be regarded as quasi-team members that reshape patterns
of collaboration.
However, this reconfiguration also raises concerns regarding accountability and trust [624]. While developers
benefit from efficiency gains, they also report risks of over-reliance and automation bias [628, 35, 641]. Effective
trust calibration, characterized by neither blind acceptance nor excessive skepticism, is therefore critical [644,
624]. Beyond trust, questions of responsibility remain pressing: if an AI-generated code fragment introduces
vulnerabilities, responsibility could lie with the developer, the reviewer, or the AI provider, underscoring the
need for clearer accountability frameworks [638].
Collaborative workflows also require adaptation [641]. Existing review processes designed for human-written code
have been shown to be inadequate for the scale and pace of AI-generated code [638]. To address this limitation,
researchers propose new mechanisms including automated verification pipelines, provenance watermarks, and
the integration of formal verification methods [632]. These innovations aim to balance the benefits of automation
with the cognitive limits of human oversight [632, 640].

9.4.4    Broader Implications
The implications of Vibe Coding extend beyond team-level practices to education and organizational structures
[641]. Scholars have argued that computing curricula should integrate training in prompting, AI governance, and
human-AI collaboration to ensure that graduates acquire the competencies necessary to manage AI-augmented
workflows [645, 28]. Without such curricular reform, future developers may lack the skills required for effective
oversight [624].
At the organizational level, the adoption of AI-augmented development may lead to a reconfiguration of profes-
sional hierarchies [633]. Activities such as product design, requirements engineering, and test creation may gain
in importance, while low-level code implementation becomes increasingly automated [643]. This development
echoes earlier predictions that programmers of the future may function more as designers and supervisors than
as traditional coders [646, 243, 640].

10      Conclusion
This paper advances Vibe Coding from scattered practice to a principled, research-grounded discipline. We
formalize Vibe Coding as a triadic system that couples human intent and quality control ("what/why"), project
context ("where"), and coding agents’ decision policies ("how"), providing a first constrained MDP formulation that
specifies roles, interfaces, and optimization targets for agentic software development. Building on this foundation,


                                                         41
                               A Survey of Vibe Coding with Large Language Models



we consolidate the field into five development models—Unconstrained Automation, Iterative Conversational
Collaboration, Planning-Driven, Test-Driven, and Context-Enhanced—that practitioners can compose to meet
distinct risk, speed, and governance requirements, and articulate the corresponding contributions as theoretical
grounding, actionable guidance, and a forward-looking research agenda. More broadly, our triadic formulation
positions Vibe Coding as an instance of human-cyber-physical systems [647, 648], reflecting the convergence of
human intelligence, autonomous computation, and physical software artifacts in modern development. This
paradigm resonates with the human-machine-thing universe proposed in network big data research [649] and
human-in-the-loop computing that emphasizes organic interaction among humans, machines, and data [650], fur-
ther aligning with the emerging vision of human-machine intelligence integration as a fundamental transformation
in research and development methodologies [651].
Our work systematizes the technical substrate required for reliable, scalable agentic coding. We survey model
training and post-training for code, analyze agent capabilities in planning, memory, and tool-mediated action, and
integrate these with execution infrastructure and feedback channels spanning compiler, runtime, human oversight,
and self-refinement. By organizing these components, we clarify how context management and executable feedback
loops—rather than model quality alone—determine performance and maintainability in long-horizon software
tasks.
Additionally, we contribute a unifying taxonomy that characterizes development choices along three orthogonal
axes—human quality control, structured constraints, and context management—thereby providing a common vo-
cabulary for comparing methods and a scaffold for engineering trade-offs in practice. The framework demonstrates
how these axes induce concrete workflow patterns that can be selected and composed to satisfy project-specific
requirements while maintaining system coherence.
Beyond technical contributions, our work surfaces implications for organizations and education. We document the
ongoing shift in developers’ mental models from line-by-line authorship to context engineering and verification,
identify the emerging skill profile around prompting, task decomposition, formalized quality supervision, and
agent governance, and outline how agent autonomy reframes collaboration, accountability, and trust at the team
level. These insights ground recommendations for training, process design, and governance that align with
human-in-the-loop oversight.
In sum, our contributions include: (i) a formal definition of Vibe Coding as a constrained decision process over
the human-project-agent triad; (ii) a unified taxonomy of five development models that integrates and clarifies
existing practices; (iii) a comprehensive synthesis of the ecosystem spanning LLMs for code, agent capabilities,
development infrastructure, and multi-source feedback; and (iv) an articulation of the central role of context
engineering and the key challenges across technical infrastructure, security mechanisms, and human factors that
shape practical deployment.

Acknowledgments
We would like to acknowledge the contributions of several scholars who are not included in the author list. We
thank Yingwei Ma from Moonshot AI for carefully checking the references and tables throughout the manuscript,
Yue Liu from the National University of Singapore for proofreading the introduction section and verifying the
tables, Yanhao Li from Peking University for proofreading Sections 9 and 10, and Jiaheng Liu from Nanjing
University for reviewing the manuscript. Their feedback and suggestions have significantly improved the quality
of this paper.




                                                       42
                                 A Survey of Vibe Coding with Large Language Models



References
  [1] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan,
      Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. Advances in neural
      information processing systems, 33:1877–1901, 2020.
  [2] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini
      Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback.
      Advances in neural information processing systems, 35:27730–27744, 2022.
  [3] Fengji Zhang, Bei Chen, Yue Zhang, Jacky Keung, Jin Liu, Daoguang Zan, Yi Mao, Jian-Guang Lou, and Weizhu Chen.
      Repocoder: Repository-level code completion through iterative retrieval and generation. arXiv preprint arXiv:2303.12570,
      2023.
  [4] Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou, Silvio Savarese, and Caiming Xiong.
      Codegen: An open large language model for code with multi-turn program synthesis. arXiv preprint arXiv:2203.13474,
      2023.
  [5] Ziyang Luo, Can Xu, Pu Zhao, Qingfeng Sun, Xiubo Geng, Wenxiang Hu, Chongyang Tao, Jing Ma, Qingwei Lin,
      and Daxin Jiang. Wizardcoder: Empowering code large language models with evol-instruct. International Conference
      on Learning Representations, 2023.
  [6] Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov, Chenghao Mou, Marc Marone,
      Christopher Akiki, Jia Li, Jenny Chim, et al. Starcoder: may the source be with you! arXiv preprint arXiv:2305.06161,
      2023.
  [7] Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Tan, Yossi Adi, Jingyu Liu, Tal Remez,
      J. Rapin, Artyom Kozhevnikov, I. Evtimov, Joanna Bitton, Manish P Bhatt, Cris tian Cantón Ferrer, Aaron Grattafiori,
      Wenhan Xiong, Alexandre D’efossez, Jade Copet, F. Azhar, Hugo Touvron, Louis Martin, Nicolas Usunier, Thomas
      Scialom, and Gabriel Synnaeve. Code llama: Open foundation models for code. arXiv preprint, 2023.
  [8] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida,
      Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774,
      2023.
  [9] Claude 4.5 sonnet. https://www.anthropic.com/claude, 2025.
 [10] Cheng Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su,
      Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, and Maosong Sun. Chatdev: Communicative agents for software
      development. Annual Meeting of the Association for Computational Linguistics, 2023.
 [11] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan.
      Swe-bench: Can language models resolve real-world github issues? arXiv preprint arXiv:2310.06770, 2023.
 [12] John Yang, Carlos E Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press.
      Swe-agent: Agent-computer interfaces enable automated software engineering. Advances in Neural Information Processing
      Systems, 37:50528–50652, 2024.
 [13] Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury. Autocoderover: Autonomous program
      improvement. In Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis, pages
      1592–1604, 2024.
 [14] Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang. Agentless: Demystifying llm-based software
      engineering agents. arXiv preprint arXiv:2407.01489, 2024.
 [15] Xingyao Wang, Boxuan Li, Yufan Song, Frank F Xu, Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi Song, Bowen Li,
      Jaskirat Singh, et al. Openhands: An open platform for ai software developers as generalist agents. arXiv preprint
      arXiv:2407.16741, 2024.
 [16] Maxime Robeyns, Martin Szummer, and Laurence Aitchison.             A self-improving coding agent.       arXiv preprint
      arXiv:2504.15228, 2025.
 [17] Gpt-5 pro. https://openai.com/gpt-5, 2025.
 [18] Andrej Karpathy. Andrej karpathy’s website. https://karpathy.ai/, 2025.
 [19] Partha Pratim Ray. A review on vibe coding: Fundamentals, state-of-the-art, challenges and future directions. Authorea
      Preprints, 2025.




                                                            43
                                A Survey of Vibe Coding with Large Language Models



[20] Ranjan Sapkota, Konstantinos I Roumeliotis, and Manoj Karkee. Vibe coding vs. agentic coding: Fundamentals and
     practical implications of agentic ai. arXiv preprint arXiv:2505.19443, 2025.
[21] Marko Horvat. What is vibe coding and when should you use it (or not)? Authorea Preprints, 2025.
[22] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt Wagner, Sergey
     Shirobokov, Borislav Kozlovskii, Francisco JR Ruiz, Abbas Mehrabian, et al. Alphaevolve: A coding agent for scientific
     and algorithmic discovery. arXiv preprint arXiv:2506.13131, 2025.
[23] Chia-Tung Ho, Haoxing Ren, and Brucek Khailany. Verilogcoder: Autonomous verilog coding agents with graph-based
     planning and abstract syntax tree (ast)-based waveform tracing tool. In Proceedings of the AAAI Conference on Artificial
     Intelligence, volume 39, pages 300–307, 2025.
[24] Yujie Zhao, Hejia Zhang, Hanxian Huang, Zhongming Yu, and Jishen Zhao. Mage: A multi-agent engine for automated
     rtl code generation. In 2025 62nd ACM/IEEE Design Automation Conference (DAC), pages 1–7. IEEE, 2025.
[25] Aohan Zeng, Xin Lv, Qinkai Zheng, Zhenyu Hou, Bin Chen, Chengxing Xie, Cunxiang Wang, Da Yin, Hao Zeng, Jiajie
     Zhang, et al. Glm-4.5: Agentic, reasoning, and coding (arc) foundation models. arXiv preprint arXiv:2508.06471, 2025.
[26] John Yang, Akshara Prabhakar, Karthik Narasimhan, and Shunyu Yao. Intercode: Standardizing and benchmarking
     interactive coding with execution feedback. Advances in Neural Information Processing Systems, 36:23826–23854, 2023.
[27] Joel Becker, Nate Rush, Elizabeth Barnes, and David Rein. Measuring the impact of early-2025 ai on experienced
     open-source developer productivity. arXiv preprint arXiv:2507.09089, 2025.
[28] Lingrui Mei, Jiayu Yao, Yuyao Ge, Yiwei Wang, Baolong Bi, Yujun Cai, Jiazhi Liu, Mingyu Li, Zhong-Zhi Li, Duzhen
     Zhang, et al. A survey of context engineering for large language models. arXiv preprint arXiv:2507.13334, 2025.
[29] Noor Nashid, Mifta Sintaha, and Ali Mesbah. Retrieval-based prompt selection for code-related few-shot learning. In
     2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE), pages 2450–2462. IEEE, 2023.
[30] Yongchao Zhou, Andrei Ioan Muresanu, Ziwen Han, Keiran Paster, Silviu Pitis, Harris Chan, and Jimmy Ba. Large
     language models are human-level prompt engineers. arXiv preprint arXiv:2211.01910, 2023.
[31] Jules White, Quchen Fu, Sam Hays, Michael Sandborn, Carlos Olea, Henry Gilbert, Ashraf Elnashar, Jesse Spencer-
     Smith, and Douglas C Schmidt. A prompt pattern catalog to enhance prompt engineering with chatgpt. arXiv preprint
     arXiv:2302.11382, 2023.
[32] Christoph Treude and Marco A Gerosa. How developers interact with ai: A taxonomy of human-ai collaboration
     in software engineering. In 2025 IEEE/ACM Second International Conference on AI Foundation Models and Software
     Engineering (Forge), pages 236–240. IEEE, 2025.
[33] George Fragiadakis, Christos Diou, George Kousiouris, and Mara Nikolaidou. Evaluating human-ai collaboration: A
     review and methodological framework. arXiv preprint arXiv:2407.19098, 2024.
[34] Eitan Altman. Constrained Markov decision processes. Routledge, 2021.
[35] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri
     Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large language models trained on code.
     arXiv preprint arXiv:2107.03374, 2021.
[36] Zengzhi Wang, Rui Xia, and Pengfei Liu. Mathpile: A billion-token-scale pretraining corpus for math. Neural
     Information Processing Systems, 2023.
[37] Yuxiang Wei, Hojae Han, and Rajhans Samdani. Arctic-snowcoder: Demystifying high-quality data in code pretraining.
     arXiv preprint, 2024.
[38] Siming Huang, Tianhao Cheng, Jason Klein Liu, Jiaran Hao, Liuyihan Song, Yang Xu, J. Yang, J. H. Liu, Chenchen
     Zhang, Linzheng Chai, Ruifeng Yuan, Zhaoxiang Zhang, Jie Fu, Qian Liu, Ge Zhang, Zili Wang, Y. Qi, Yinghui
     Xu, and Wei Chu. Opencoder: The open cookbook for top-tier code large language models, 2024. URL https:
     //arxiv.org/abs/2411.04905v3.
[39] Kazuki Fujii, Yukito Tajima, Sakae Mizuki, Hinari Shimada, Taihei Shiotani, Koshiro Saito, Masanari Ohi, Masaki
     Kawamura, Taishi Nakamura, Takumi Okamoto, Shigeki Ishida, Kakeru Hattori, Youmi Ma, Hiroya Takamura, Rio
     Yokota, and Naoaki Okazaki. Rewriting pre-training data boosts llm performance in math and code, 2025. URL
     https://arxiv.org/abs/2505.02881v3.
[40] Niklas Muennighoff, Qian Liu, Qi Liu, A. Zebaze, Qinkai Zheng, Binyuan Hui, Terry Yue Zhuo, Swayam Singh,
     Xiangru Tang, L. V. Werra, and S. Longpre. Octopack: Instruction tuning code large language models. International
     Conference on Learning Representations, 2023.



                                                            44
                                A Survey of Vibe Coding with Large Language Models



[41] W. Ahmad, Aleksander Ficek, Mehrzad Samadi, Jocelyn Huang, V. Noroozi, Somshubra Majumdar, and Boris Ginsburg.
     Opencodeinstruct: A large-scale instruction tuning dataset for code llms, 2025. URL https://arxiv.org/abs/2504.
     04030v2.
[42] Jian Yang, Jiaxi Yang, Ke Jin, Yibo Miao, Lei Zhang, Liqun Yang, Zeyu Cui, Yichang Zhang, Binyuan Hui, and Junyang
     Lin. Evaluating and aligning codellms on human preference, 2024. URL https://arxiv.org/abs/2412.05210v1.
[43] M. Weyssow, Aton Kamanda, Xin Zhou, and H. Sahraoui. Codeultrafeedback: An llm-as-a-judge dataset for aligning
     large language models to coding preferences. ACM Transactions on Software Engineering and Methodology, 2024.
[44] Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu, Noah A. Smith, Daniel Khashabi, and Hannaneh
     Hajishirzi. Self-instruct: Aligning language models with self-generated instructions. Annual Meeting of the Association
     for Computational Linguistics, 2022.
[45] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional
     transformers for language understanding. North American Chapter of the Association for Computational Linguistics, 2019.
[46] Colin Raffel, Noam M. Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li,
     and Peter J. Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. Journal of machine
     learning research, 2019.
[47] N. Chirkova and Sergey Troshin. Codebpe: Investigating subtokenization options for large language model pretraining
     on source code. International Conference on Learning Representations, 2023.
[48] Daya Guo, Shuo Ren, Shuai Lu, Zhangyin Feng, Duyu Tang, Shujie Liu, Long Zhou, Nan Duan, Jian Yin, Daxin Jiang,
     and M. Zhou. Graphcodebert: Pre-training code representations with data flow. International Conference on Learning
     Representations, 2020.
[49] Yue Wang, Weishi Wang, Shafiq R. Joty, and S. Hoi. Codet5: Identifier-aware unified pre-trained encoder-decoder
     models for code understanding and generation. Conference on Empirical Methods in Natural Language Processing, 2021.
[50] Sam Blouir, Jimmy Smith, Antonios Anastasopoulos, and Amarda Shehu. Birdie: Advancing state space models with
     reward-driven objectives and curricula, 2024. URL https://arxiv.org/abs/2411.01030v5.
[51] Linus Jern, Valter Uotila, Cong Yu, and Bo Zhao. Agent-q: Fine-tuning large language models for quantum circuit
     generation and optimization. arXiv preprint, 2025.
[52] Zhangyin Feng, Daya Guo, Duyu Tang, Nan Duan, Xiaocheng Feng, Ming Gong, Linjun Shou, Bing Qin, Ting Liu,
     Daxin Jiang, and Ming Zhou. Codebert: A pre-trained model for programming and natural languages. Findings, 2020.
[53] Daya Guo, Shuai Lu, Nan Duan, Yanlin Wang, Ming Zhou, and Jian Yin. Unixcoder: Unified cross-modal pre-training
     for code representation. Annual Meeting of the Association for Computational Linguistics, 2022.
[54] Yufan Huang, Mengnan Qi, Yongqiang Yao, Maoquan Wang, Bin Gu, Colin B. Clement, and Neel Sundaresan. Program
     translation via code distillation. Conference on Empirical Methods in Natural Language Processing, 2023.
[55] Saikat Chakraborty, Toufique Ahmed, Yangruibo Ding, Prem Devanbu, and Baishakhi Ray. Natgen: generative
     pre-training by “naturalizing” source code. ESEC/SIGSOFT FSE, 2022.
[56] Wasi Uddin Ahmad, Saikat Chakraborty, Baishakhi Ray, and Kai-Wei Chang. Unified pre-training for program
     understanding and generation. North American Chapter of the Association for Computational Linguistics, 2021.
[57] Yue Wang, Hung Le, Akhilesh Deepak Gotmare, Nghi D. Q. Bui, Junnan Li, and Steven C. H. Hoi. Codet5+: Open
     code large language models for code understanding and generation. Conference on Empirical Methods in Natural
     Language Processing, 2023.
[58] Anjiang Wei, Huanmi Tan, Tarun Suresh, Daniel Mendoza, Thiago S. F. X. Teixeira, Ke Wang, Caroline Trippel, and
     Alex Aiken. Vericoder: Enhancing llm-based rtl code generation through functional correctness validation, 2025. URL
     https://arxiv.org/abs/2504.15659v2.
[59] Hyung Won Chung, Le Hou, S. Longpre, Barret Zoph, Yi Tay, W. Fedus, Eric Li, Xuezhi Wang, Mostafa Dehghani,
     Siddhartha Brahma, Albert Webson, S. Gu, Zhuyun Dai, Mirac Suzgun, Xinyun Chen, A. Chowdhery, Dasha Valter,
     Sharan Narang, Gaurav Mishra, Adams Wei Yu, Vincent Zhao, Yanping Huang, Andrew M. Dai, Hongkun Yu,
     Slav Petrov, Ed H. Chi, J. Dean, Jacob Devlin, Adam Roberts, Denny Zhou, Quoc V. Le, and Jason Wei. Scaling
     instruction-finetuned language models. Journal of machine learning research, 2022.
[60] Jason Wei, Maarten Bosma, Vincent Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M. Dai, and
     Quoc V. Le. Finetuned language models are zero-shot learners. International Conference on Learning Representations,
     2021.



                                                           45
                                 A Survey of Vibe Coding with Large Language Models



[61] Dayong Wu, Jiaqi Li, Baoxin Wang, Honghong Zhao, Siyuan Xue, Yanjie Yang, Zhijun Chang, Rui Zhang, Li Qian,
     Bo Wang, Shijin Wang, Zhixiong Zhang, and Guoping Hu. Sparkra: A retrieval-augmented knowledge service system
     based on spark large language model. Conference on Empirical Methods in Natural Language Processing, 2024.
[62] Bo Shen, Jiaxin Zhang, Taihong Chen, Daoguang Zan, Bing Geng, An Fu, Muhan Zeng, Ailun Yu, Jichuan Ji, Jingyang
     Zhao, Yuenan Guo, and Qianxiang Wang. Pangu-coder2: Boosting large language models for code with ranking
     feedback. arXiv preprint, 2023.
[63] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al.
     Lora: Low-rank adaptation of large language models. ICLR, 1(2):3, 2022.
[64] N. Houlsby, A. Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin de Laroussilhe, Andrea Gesmundo, Mona
     Attariyan, and S. Gelly. Parameter-efficient transfer learning for nlp. International Conference on Machine Learning, 2019.
[65] Chunting Zhou, Pengfei Liu, Puxin Xu, Srini Iyer, Jiao Sun, Yuning Mao, Xuezhe Ma, Avia Efrat, Ping Yu, L. Yu,
     Susan Zhang, Gargi Ghosh, M. Lewis, Luke Zettlemoyer, and Omer Levy. Lima: Less is more for alignment. Neural
     Information Processing Systems, 2023.
[66] Lichang Chen, SHIYANG LI, Jun Yan, Hai Wang, Kalpa Gunaratna, Vikas Yadav, Zheng Tang, Vijay Srinivasan, Tianyi
     Zhou, Heng Huang, and Hongxia Jin. Alpagasus: Training a better alpaca with fewer data. International Conference on
     Learning Representations, 2023.
[67] Giorgos Iacovides, Wuyang Zhou, and Danilo Mandic. Findpo: Financial sentiment analysis for algorithmic trading
     through preference optimization of llms, 2025. URL https://arxiv.org/abs/2507.18417v1.
[68] Rafael Rafailov, Archit Sharma, E. Mitchell, Stefano Ermon, Christopher D. Manning, and Chelsea Finn. Direct
     preference optimization: Your language model is secretly a reward model. Neural Information Processing Systems, 2023.
[69] Guangzhi Xiong, Qiao Jin, Xiao Wang, Yin Fang, Haolin Liu, Yifan Yang, Fangyuan Chen, Zhixing Song, Dengyu
     Wang, Minjia Zhang, Zhiyong Lu, and Aidong Zhang. Rag-gym: Systematic optimization of language agents for
     retrieval-augmented generation. arXiv preprint, 2025.
[70] Nisan Stiennon, Long Ouyang, Jeff Wu, Daniel M. Ziegler, Ryan J. Lowe, Chelsea Voss, Alec Radford, Dario Amodei,
     and Paul Christiano. Learning to summarize from human feedback. Neural Information Processing Systems, 2020.
[71] Zhenting Wang, Guofeng Cui, Kun Wan, and Wentian Zhao. Dump: Automated distribution-level curriculum learning
     for rl-based llm post-training, 2025. URL https://arxiv.org/abs/2504.09710v2.
[72] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed H. Chi, F. Xia, Quoc Le, and Denny Zhou. Chain of
     thought prompting elicits reasoning in large language models. Neural Information Processing Systems, 2022.
[73] Mengkang Hu, Pu Zhao, Can Xu, Qingfeng Sun, Jian-Guang Lou, Qingwei Lin, Ping Luo, S. Rajmohan, and Dongmei
     Zhang. Agentgen: Enhancing planning abilities for large language model based agent via environment and task
     generation. Knowledge Discovery and Data Mining, 2024.
[74] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing
     reasoning and acting in language models. International Conference on Learning Representations, 2022.
[75] Zhengdong Lu, Weikai Lu, Yiling Tao, Yun Dai, ZiXuan Chen, Huiping Zhuang, Cen Chen, Hao Peng, and Ziqian
     Zeng. Decompose, plan in parallel, and merge: A novel paradigm for large language models based planning with
     multiple constraints, 2025. URL https://arxiv.org/abs/2506.02683v1.
[76] Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, and Y. Zhuang. Hugginggpt: Solving ai tasks
     with chatgpt and its friends in hugging face. Neural Information Processing Systems, 2023.
[77] Takeshi Kojima, S. Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large language models are zero-shot
     reasoners. Neural Information Processing Systems, 2022.
[78] Zhuosheng Zhang, Aston Zhang, Mu Li, and Alexander J. Smola. Automatic chain of thought prompting in large
     language models. International Conference on Learning Representations, 2022.
[79] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, T. Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts:
     Deliberate problem solving with large language models. Neural Information Processing Systems, 2023.
[80] Runquan Gui, Zhihai Wang, Jie Wang, Chi Ma, Huiling Zhen, Mingxuan Yuan, Jianye Hao, Defu Lian, Enhong
     Chen, and Feng Wu. Hypertree planning: Enhancing llm reasoning via hierarchical thinking, 2025. URL https:
     //arxiv.org/abs/2505.02322v2.
[81] Jiaxin Wen, Jian Guan, Hongning Wang, Wei Wu, and Minlie Huang. Codeplan: Unlocking reasoning potential in
     large langauge models by scaling code-form planning. International Conference on Learning Representations, 2024.



                                                             46
                                A Survey of Vibe Coding with Large Language Models



 [82] Yuan Tian, Jonathan K. Kummerfeld, Toby Jia-Jun Li, and Tianyi Zhang. Sqlucid: Grounding natural language
      database queries with interactive explanations. ACM Symposium on User Interface Software and Technology, 2024.
 [83] Pruthvi H. Patel, Swaroop Mishra, Mihir Parmar, and Chitta Baral. Is a question decomposition unit all we need?
      Conference on Empirical Methods in Natural Language Processing, 2022.
 [84] Ashish Vaswani, Noam M. Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and
      I. Polosukhin. Attention is all you need. Neural Information Processing Systems, 2017.
 [85] Gaoke Zhang, Bo Wang, Yunlong Ma, et al. Multiple memory systems for enhancing the long-term memory of agent.
      arXiv preprint arXiv:2508.15294, 2025.
 [86] Wujiang Xu, Kai Mei, Hang Gao, Juntao Tan, Zujie Liang, and Yongfeng Zhang. A-mem: Agentic memory for llm
      agents. arXiv preprint arXiv:2502.12110, 2025.
 [87] Zeyu Zhang, Quanyu Dai, Xu Chen, Rui Li, Zhongyang Li, and Zhenhua Dong. Memengine: A unified and modular
      library for developing advanced memory of llm-based agents. In Companion Proceedings of the ACM on Web Conference
      2025, pages 821–824, 2025.
 [88] Yujie Feng, Xu Chu, Yongxin Xu, Guangyuan Shi, Bo Liu, and Xiao-Ming Wu. Tasl: Continual dialog state tracking
      via task skill localization and consolidation. Annual Meeting of the Association for Computational Linguistics, 2024.
 [89] Wanjun Zhong, Lianghong Guo, Qi-Fei Gao, He Ye, and Yanlin Wang. Memorybank: Enhancing large language
      models with long-term memory. AAAI Conference on Artificial Intelligence, 2023.
 [90] J. Park, Joseph C. O’Brien, Carrie J. Cai, M. Morris, Percy Liang, and Michael S. Bernstein. Generative agents:
      Interactive simulacra of human behavior. ACM Symposium on User Interface Software and Technology, 2023.
 [91] Wenlong Huang, P. Abbeel, Deepak Pathak, and Igor Mordatch. Language models as zero-shot planners: Extracting
      actionable knowledge for embodied agents. International Conference on Machine Learning, 2022.
 [92] Ali Modarressi, Ayyoob Imani, Mohsen Fayyaz, and Hinrich Schütze. Ret-llm: Towards a general read-write memory
      for large language models. arXiv preprint arXiv:2305.14322, 2023.
 [93] Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, R. Raileanu, M. Lomeli, Luke Zettlemoyer, Nicola Cancedda, and
      Thomas Scialom. Toolformer: Language models can teach themselves to use tools. Neural Information Processing
      Systems, 2023.
 [94] Huajun Chen. Large knowledge model: Perspectives and challenges. Data Intelligence, 2023.
 [95] Weizhou Shen, Chenliang Li, Hongzhan Chen, Ming Yan, Xiaojun Quan, Hehong Chen, Ji Zhang, and Fei Huang.
      Small llms are weak tool learners: A multi-llm agent. Conference on Empirical Methods in Natural Language Processing,
      2024.
 [96] Xinyi Hou, Yanjie Zhao, Shenao Wang, and Haoyu Wang. Model context protocol (mcp): Landscape, security threats,
      and future research directions, 2025. URL https://arxiv.org/abs/2503.23278v2.
 [97] Xiang Fei, Xiawu Zheng, and Hao Feng. Mcp-zero: Active tool discovery for autonomous llm agents. arXiv preprint,
      2025.
 [98] Zhengliang Shi, Shen Gao, Xiuyi Chen, Yue Feng, Lingyong Yan, Haibo Shi, Dawei Yin, Zhumin Chen, Suzan Verberne,
      and Zhaochun Ren. Tool learning in the wild: Empowering language models as automatic tool agents. The Web
      Conference, 2024.
 [99] Kechi Zhang, Jia Li, Ge Li, Xianjie Shi, and Zhi Jin. Codeagent: Enhancing code generation with tool-integrated agent
      systems for real-world repo-level coding challenges. arXiv preprint arXiv:2401.07339, 2024.
[100] Sakhinana Sagar Srinivas, Geethan Sannidhi, and Venkataramana Runkana. Retrieval-augmented instruction tuning for
      automated process engineering calculations : A tool-chaining problem-solving framework with attributable reflection,
      2024. URL https://arxiv.org/abs/2408.15866v1.
[101] Elias Lumer, Anmol Gulati, Vamse Kumar Subbiah, Pradeep Honaganahalli Basavaraju, and James A Burke. Scalemcp:
      Dynamic and auto-synchronizing model context protocol tools for llm agents. arXiv preprint arXiv:2505.06416, 2025.
[102] Xinyi Ni, Haonan Jian, Qiuyang Wang, Vedanshi Chetan Shah, and Pengyu Hong. Doc2agent: Scalable generation of
      tool-using agents from api documentation. arXiv preprint arXiv:2506.19998, 2025.
[103] Jiaye Lin, Yifu Guo, Yuzhen Han, Sen Hu, Ziyi Ni, Licheng Wang, Mingguang Chen, Hongzhang Liu, Ronghao Chen,
      Yangfan He, Daxin Jiang, Binxing Jiao, Chen Hu, and Huacan Wang. Se-agent: Self-evolution trajectory optimization
      in multi-step reasoning with llm-based agents. arXiv preprint, 2025.



                                                           47
                                A Survey of Vibe Coding with Large Language Models



[104] Dong Huang, Jie M Zhang, Michael Luck, Qingwen Bu, Yuhao Qing, and Heming Cui. Agentcoder: Multi-agent-based
      code generation with iterative testing and optimisation. arXiv preprint arXiv:2312.13010, 2023.
[105] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri,
      Shrimai Prabhumoye, Yiming Yang, S. Welleck, Bodhisattwa Prasad Majumder, Shashank Gupta, A. Yazdanbakhsh,
      and Peter Clark. Self-refine: Iterative refinement with self-feedback. Neural Information Processing Systems, 2023.
[106] Aman Kumar, Deepak Narayan Gadde, Keerthan Kopparam Radhakrishna, and D. Lettnin. Saarthi: The first ai
      formal verification engineer, 2025. URL https://arxiv.org/abs/2502.16662v2.
[107] Nguyen Phu Vinh, Anh Chung Hoang, Chris Ngo, and Truong-Son Hy. Repeton: Structured bug repair with
      react-guided patch-and-test cycles, 2025. URL https://arxiv.org/abs/2506.08173v1.
[108] Xue Jiang, Yihong Dong, Lecheng Wang, Qiwei Shang, and Ge Li. Self-planning code generation with large language
      models. ACM Transactions on Software Engineering and Methodology, 2023.
[109] Huan Zhang, Wei Cheng, Yuhan Wu, and Wei Hu. A pair programming framework for code generation via multi-plan
      exploration and feedback-driven refinement. In Proceedings of the 39th IEEE/ACM International Conference on Automated
      Software Engineering, pages 1319–1331, 2024.
[110] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. Teaching large language models to self-debug. arXiv
      preprint arXiv:2304.05128, 2023.
[111] Nazmus Ashrafi, Salah Bouktif, and Mohammed Mediani. Enhancing llm code generation: A systematic evaluation
      of multi-agent collaboration and runtime debugging for improved accuracy, reliability, and latency, 2025. URL
      https://arxiv.org/abs/2505.02133v1.
[112] Sarah Fakhoury, Aaditya Naik, Georgios Sakkas, Saikat Chakraborty, and Shuvendu K. Lahiri. Llm-based test-driven
      interactive code generation: User study and empirical evaluation. IEEE Transactions on Software Engineering, 2024.
[113] Shuvendu K Lahiri, Sarah Fakhoury, Aaditya Naik, Georgios Sakkas, Saikat Chakraborty, Madanlal Musuvathi, Piali
      Choudhury, Curtis von Veh, Jeevana Priya Inala, Chenglong Wang, et al. Interactive code generation via test-driven
      user-intent formalization. arXiv preprint arXiv:2208.05950, 2022.
[114] Duc Hieu Ho and Chenglin Fan. Self-critique-guided curiosity refinement: Enhancing honesty and helpfulness in
      large language models via in-context learning, 2025. URL https://arxiv.org/abs/2506.16064v1.
[115] Rintaro Ando. When your own output becomes your training data: Noise-to-meaning loops and a formal rsi trigger,
      2025. URL https://arxiv.org/abs/2505.02888v1.
[116] Yiyang Jin, Kunzhao Xu, Hang Li, Xueting Han, Yanmin Zhou, Cheng Li, and Jing Bai. Reveal: Self-evolving code
      agents via iterative generation-verification, 2025. URL https://arxiv.org/abs/2506.11442v1.
[117] Zhangqian Bi, Yao Wan, Zheng Wang, Hongyu Zhang, Batu Guan, Fangxin Lu, Zili Zhang, Yulei Sui, Xuanhua Shi,
      and Hai Jin. Iterative refinement of project-level code context for precise code generation with compiler feedback.
      Annual Meeting of the Association for Computational Linguistics, 2024.
[118] Haolin Jin, Zechao Sun, and Huaming Chen. Rgd: Multi-llm based agent debugger via refinement and generation
      guidance. International Conference on Agents, 2024.
[119] Huaiyuan Yao, Longchao Da, Vishnu Nandam, J. Turnau, Zhiwei Liu, Linsey Pang, and Hua Wei. Comal: Collaborative
      multi-agent large language models for mixed-autonomy traffic. SDM, 2024.
[120] Yuwei Lou, Hao Hu, Shaocong Ma, Zongfei Zhang, Liang Wang, Jidong Ge, and Xianping Tao. Drf: Llm-agent
      dynamic reputation filtering framework, 2025. URL https://arxiv.org/abs/2509.05764v1.
[121] Pranav Mishra, Mohammad Arvan, and Mohan Zalake. Teammedagents: Enhancing medical decision-making of llms
      through structured teamwork, 2025. URL https://arxiv.org/abs/2508.08115v1.
[122] Sourena Khanzadeh. Agentmesh: A cooperative multi-agent generative ai framework for software development
      automation, 2025. URL https://arxiv.org/abs/2507.19902v1.
[123] Dean Lawrence Williams. Multi-agent communication protocol in collaborative problem solving: A design science
      approach, 2025.
[124] Junda He, Christoph Treude, and David Lo. Llm-based multi-agent systems for software engineering: Literature
      review, vision, and the road ahead. ACM Transactions on Software Engineering and Methodology, 34(5):1–30, 2025.
[125] Khanh-Tung Tran, Dung Dao, Minh-Duong Nguyen, Quoc-Viet Pham, Barry O’Sullivan, and Hoang D. Nguyen.
      Multi-agent collaboration mechanisms: A survey of llms, 2025. URL https://arxiv.org/abs/2501.06322v1.



                                                           48
                                A Survey of Vibe Coding with Large Language Models



[126] Junyou Li, Qin Zhang, Yangbin Yu, Qiang Fu, and Deheng Ye. More agents is all you need. arXiv preprint
      arXiv:2402.05120, 2024.
[127] Md. Ashraful Islam, Mohammed Eunus Ali, and Md. Rizwan Parvez. Mapcoder: Multi-agent code generation for
      competitive problem solving. Annual Meeting of the Association for Computational Linguistics, 2024.
[128] M. Santoro, P. Mazzetti, and S. Nativi. Virtual earth cloud: a multi-cloud framework for enabling geosciences digital
      ecosystems. International Journal of Digital Earth, 2023.
[129] Seungsoo Lee and Jae-Cheul Nam. Kunerva: Automated network policy discovery framework for containers. IEEE
      Access, 2023.
[130] Elyes Lounissi, Suvam Kumar Das, Ronnit Peter, Xiaozheng Zhang, Suprio Ray, and Lianyin Jia. Funda: scalable
      serverless data analytics and in situ query processing. Journal of Big Data, 2025.
[131] L. Baresi and G. Quattrocchi. Cocos: A scalable architecture for containerized heterogeneous systems. International
      Conference on Software Architecture, 2020.
[132] Eleni Adamidi, Panayiotis Deligiannis, Nikos Foutris, and Thanasis Vergoulis. A virtual laboratory for managing
      computational experiments. International Conference on Statistical and Scientific Database Management, 2025.
[133] G. M. Kurtzer, V. Sochat, and Michael W Bauer. Singularity: Scientific containers for mobility of compute. PLoS ONE,
      2017.
[134] Yu Zhou, Weilin Zhan, Zi Li, Tingting Han, Taolue Chen, and H. Gall. Drive: Dockerfile rule mining and violation
      detection. ACM Transactions on Software Engineering and Methodology, 2022.
[135] Federico Cassano, John Gouwar, Daniel Nguyen, S. Nguyen, Luna Phipps-Costin, Donald Pinckney, Ming-Ho Yee,
      Yangtian Zi, Carolyn Jane Anderson, Molly Q. Feldman, Arjun Guha, Michael Greenberg, and Abhinav Jangda.
      Multipl-e: A scalable and polyglot approach to benchmarking neural code generation. IEEE Transactions on Software
      Engineering, 2023.
[136] Aofeng Su, Aowen Wang, Chaonan Ye, Chengcheng Zhou, Ga Zhang, Gang Chen, Guangcheng Zhu, Haobo Wang,
      Haokai Xu, Hao Chen, Haoze Li, Haoxuan Lan, Jiaming Tian, Jing Yuan, Junbo Zhao, Junlin Zhou, Kaizhe Shou,
      Liangyu Zha, Lin Long, Liyao Li, Peng Wu, Qi Zhang, Qingyi Huang, Sa Yang, Tao Zhang, Wen-Yuan Ye, Wufang
      Zhu, Xiaomeng Hu, Xijun Gu, Xinjie Sun, Xiang Li, Yuhang Yang, and Zhiqing Xiao. Tablegpt2: A large multimodal
      model with tabular data integration, 2024. URL https://arxiv.org/abs/2411.02059v3.
[137] R. Rabin, Jesse Hostetler, Sean McGregor, Brett Weir, and Nicholas C. Judd. Sandboxeval: Towards securing test
      environment for untrusted code, 2025. URL https://arxiv.org/abs/2504.00018v1.
[138] Ana Nunez, Nafis Tanveer Islam, S. Jha, and Peyman Najafirad. Autosafecoder: A multi-agent framework for securing
      llm code generation through static analysis and fuzz testing, 2024. URL https://arxiv.org/abs/2409.10737v2.
[139] Bipin Gajbhiye, Shalu Jain, and Akshun Chhapola. Secure sdlc: Incorporating blockchain for enhanced security.
      Scientific Journal of Metaverse and Blockchain Technologies, 2024.
[140] Peter Robe and Sandeep Kaur Kuttal. Designing pairbuddy—a conversational agent for pair programming. ACM
      Trans. Comput. Hum. Interact., 2022.
[141] Benedetta Donato, Leonardo Mariani, D. Micucci, O. Riganelli, and Marco Somaschini. Multimind: A plug-in for the
      implementation of development tasks aided by ai assistants. SIGSOFT FSE Companion, 2025.
[142] Dominik Bork and Philip Langer. Language server protocol: An introduction to the protocol, its use, and adoption
      for web modeling tools. Enterprise Modelling and Information Systems Architectures (EMISAJ), 18:9–1, 2023.
[143] Junde Wu. Git context controller: Manage the context of llm-based agents like git. arXiv preprint arXiv:2508.00031,
      2025.
[144] Gustavo Pinto, C. D. de Souza, T. Rocha, Igor Steinmacher, Alberto de Souza, and Edward Monteiro. Developer
      experiences with a contextualized ai coding assistant: Usability, expectations, and outcomes. 2024 IEEE/ACM 3rd
      International Conference on AI Engineering – Software Engineering for AI (CAIN), 2023.
[145] Nadeeshaan Gunasinghe and Nipuna Marcus. Language server protocol and implementation. Springer, 2021.
[146] Vincent Koc, Jacques Verre, Douglas Blank, and Abigail Morgan. Mind the metrics: Patterns for telemetry-aware
      in-ide ai application development using the model context protocol (mcp). arXiv preprint arXiv:2506.11019, 2025.
[147] Antonio Brogi, Luca Rinaldi, and J. Soldani. Tosker: A synergy between tosca and docker for orchestrating
      multicomponent applications. Software, Practice & Experience, 2018.



                                                           49
                                 A Survey of Vibe Coding with Large Language Models



[148] C. Dehury, Pelle Jakovits, S. Srirama, Giorgos Giotis, and Gaurav Garg. Toscadata: Modelling data pipeline applications
      in tosca. Journal of Systems and Software, 2021.
[149] O. Tomarchio, Domenico Calcaterra, G. Modica, and Pietro Mazzaglia. Torch: a tosca-based orchestrator of multi-cloud
      containerised applications. Journal of Grid Computing, 2021.
[150] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, E. Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang,
      Jiale Liu, A. Awadallah, Ryen W. White, Doug Burger, and Chi Wang. Autogen: Enabling next-gen llm applications
      via multi-agent conversation, 2023. URL https://arxiv.org/abs/2308.08155v2.
[151] Chenxu Zhu, Bo Chen, Huifeng Guo, Hang Xu, Xiangyang Li, Xiangyu Zhao, Weinan Zhang, Yong Yu, and Ruiming
      Tang. Autogen: An automated dynamic model generation framework for recommender system. In Proceedings of the
      Sixteenth ACM International Conference on Web Search and Data Mining, pages 598–606, 2023.
[152] Sebastian Porsdam Mann, Brian D Earp, Nikolaj Møller, Suren Vynn, and Julian Savulescu. Autogen: A personalized
      large language model for academic enhancement—ethics and proof of principle. The American Journal of Bioethics, 23
      (10):28–41, 2023.
[153] Tom Taulli and Gaurav Deshmukh. Crewai. In Building Generative AI Agents: Using LangGraph, AutoGen, and CrewAI,
      pages 103–145. Springer, 2025.
[154] Yuyan Zhou, Liang Song, Bingning Wang, and Weipeng Chen. Metagpt: Merging large language models using model
      exclusive task arithmetic. arXiv preprint arXiv:2406.11385, 2024.
[155] Et. al Amarjeet Singh. Microservices container security orchestration framework within kubernetes and docker for
      business-critical applications within digital transformation. International Journal on Recent and Innovation Trends in
      Computing and Communication, 2023.
[156] Kent Beck. Extreme programming explained: embrace change. addison-wesley professional, 2000.
[157] Giuseppe Bisicchia, Stefano Forti, Ernesto Pimentel, and Antonio Brogi. Continuous qos-compliant orchestration in
      the cloud-edge continuum. Software, Practice & Experience, 2023.
[158] Twinkle Joshi. Architecting agentic ai for modern software testing: Capabilities, foundations, and a proposed scalable
      multi-agent system for automated test generation. Journal of Information Systems Engineering & Management, 2025.
[159] Yeongrak Choi, Taeyoung Kim, and Hyung Soo Han. Intelligent exercise and feedback system for social healthcare
      using llmops, 2025. URL https://arxiv.org/abs/2501.13723v1.
[160] Kevin Song, Andrew Trotter, and Jake Y. Chen. Llm agent swarm for hypothesis-driven drug discovery, 2025. URL
      https://arxiv.org/abs/2504.17967v1.
[161] Liekang Zeng, Shengyuan Ye, Xu Chen, Xiaoxi Zhang, Ju Ren, Jian Tang, Yang Yang, and Xuemin Sherman Shen.
      Edge graph intelligence: Reciprocally empowering edge networks with graph intelligence. IEEE Communications
      Surveys & Tutorials, 2025.
[162] Abhinav C. P. Jain, Chima Adiole, Swarat Chaudhuri, T. Reps, Chris Jermaine Rice University, U. Austin, and
      U. Wisconsin. Coarse-tuning models of code with reinforcement learning feedback, 2023. URL https://arxiv.org/
      abs/2305.18341v2.
[163] Yangruibo Ding, Marcus J. Min, Gail E. Kaiser, and Baishakhi Ray. Cycle: Learning to self-refine the code generation.
      Proc. ACM Program. Lang., 2024.
[164] Ali Reza Ibrahimzada, Kai-Jie Ke, Mrigank Pawagi, Muhammad Salman Abid, Rangeet Pan, Saurabh Sinha, and
      Reyhaneh Jabbarvand. Alphatrans: A neuro-symbolic compositional approach for repository-level code translation
      and validation. Proc. ACM Softw. Eng., 2024.
[165] Jonas Gehring, Kunhao Zheng, Jade Copet, Vegard Mella, Taco Cohen, and Gabriele Synnaeve. Rlef: Grounding code
      llms in execution feedback with reinforcement learning, 2024. URL https://arxiv.org/abs/2410.02089v2.
[166] Huaye Zeng, Dongfu Jiang, Haozhe Wang, Ping Nie, Xiaotong Chen, and Wenhu Chen. Acecoder: Acing coder rl via
      automated test-case synthesis. Annual Meeting of the Association for Computational Linguistics, 2025.
[167] Yuansheng Ni, Ping Nie, Kai Zou, Xiang Yue, and Wenhu Chen. Viscoder: Fine-tuning llms for executable python
      visualization code generation, 2025. URL https://arxiv.org/abs/2506.03930v2.
[168] Fernando Vallecillos Ruiz, Max Hort, and Leon Moonen. The art of repair: Optimizing iterative program repair with
      instruction-tuned models, 2025. URL https://arxiv.org/abs/2505.02931v1.
[169] Yun-Da Tsai, Mingjie Liu, and Haoxing Ren. Rtlfixer: Automatically fixing rtl syntax errors with large language
      model. Design Automation Conference, 2023.


                                                            50
                                 A Survey of Vibe Coding with Large Language Models



[170] Yun Peng, Akhilesh Deepak Gotmare, Michael R. Lyu, Caiming Xiong, Silvio Savarese, and Doyen Sahoo. Perfcodegen:
      Improving performance of llm generated code with execution feedback. 2025 IEEE/ACM Second International Conference
      on AI Foundation Models and Software Engineering (Forge), 2024.
[171] Islem Bouzenia and Michael Pradel. You name it, i run it: An llm agent to execute tests of arbitrary projects. Proc.
      ACM Softw. Eng., 2024.
[172] Runlin Liu, Zhe Zhang, Yunge Hu, Yuhang Lin, Xiang Gao, and Hailong Sun. Llm-based unit test generation for
      dynamically-typed programs. arXiv preprint arXiv:2503.14000, 2025.
[173] Yibo Wang, Congying Xia, Wenting Zhao, Jiangshu Du, Chunyu Miao, Zhongfen Deng, Philip S Yu, and Chen Xing.
      Projecttest: A project-level llm unit test generation benchmark and impact of error fixing mechanisms. arXiv preprint
      arXiv:2502.06556, 2025.
[174] Muntasir Adnan, Zhiwei Xu, and Carlos C. N. Kuhn. Large language model guided self-debugging code generation,
      2025. URL https://arxiv.org/abs/2502.02928v2.
[175] Rangeet Pan, Myeongsoo Kim, Rahul Krishna, Raju Pavuluri, and Saurabh Sinha. Aster: Natural and multi-language
      unit test generation with llms. In 2025 IEEE/ACM 47th International Conference on Software Engineering: Software
      Engineering in Practice (ICSE-SEIP), pages 413–424. IEEE, 2025.
[176] Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, and Weizhu Chen. Codet: Code
      generation with generated tests. arXiv preprint arXiv:2207.10397, 2022.
[177] Amit Rath. Structured prompting and feedback-guided reasoning with llms for data interpretation, 2025. URL
      https://arxiv.org/abs/2505.01636v1.
[178] Xiaoxue Ren, Xinyuan Ye, Dehai Zhao, Zhenchang Xing, and Xiaohu Yang. From misuse to mastery: Enhancing code
      generation with knowledge-driven ai chaining. International Conference on Automated Software Engineering, 2023.
[179] Zhe Zhang, Xingyu Liu, Yuanzhang Lin, Xiang Gao, Hailong Sun, and Yuan Yuan. Llm-based unit test generation via
      property retrieval. arXiv preprint arXiv:2410.13542, 2024.
[180] Xuanming Zhang, Yuxuan Chen, Yuan Yuan, and Minlie Huang. Seeker: Enhancing exception handling in code with
      llm-based multi-agent approach. arXiv preprint arXiv:2410.06949, 2024.
[181] N. Alshahwan, Jubin Chheda, Anastasia Finogenova, Beliz Gokkaya, Mark Harman, Inna Harper, Alexandru Marginean,
      Shubho Sengupta, and Eddy Wang. Automated unit test improvement using large language models at meta. SIGSOFT
      FSE Companion, 2024.
[182] Zhensu Sun, Haotian Zhu, Bowen Xu, Xiaoning Du, Li Li, and David Lo. Llm as runtime error handler: A promising
      pathway to adaptive self-healing of software systems. arXiv preprint arXiv:2408.01055, 2024.
[183] Jörg Schultz. On the potential of agentic workflows for animal training plan generation. Frontiers in Veterinary Science,
      2025.
[184] Shraddha Barke, Michael B James, and Nadia Polikarpova. Grounded copilot: How programmers interact with
      code-generating models. In Proceedings of the ACM on Programming Languages, volume 7, pages 85–111. ACM, 2023.
[185] Fabrizio Marozzo. Iterative resolution of prompt ambiguities using a progressive cutting-search approach. Artificial
      Intelligence Applications and Innovations, 2025.
[186] M. Zaheer, Satwik Kottur, Siamak Ravanbakhsh, B. Póczos, R. Salakhutdinov, and Alex Smola. Deep sets, 2017. URL
      https://arxiv.org/abs/1703.06114v3.
[187] Yekun Chai, Haoran Sun, Huang Fang, Shuohuan Wang, Yu Sun, and Hua Wu. Ma-rlhf: Reinforcement learning from
      human feedback with macro actions. arXiv preprint arXiv:2410.02743, 2024.
[188] Fangwen Mu, Lin Shi, Song Wang, Zhuohao Yu, Binquan Zhang, ChenXue Wang, Shichao Liu, and Qing Wang.
      Clarifygpt: A framework for enhancing llm-based code generation via requirements clarification. Proc. ACM Softw.
      Eng., 2024.
[189] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization
      algorithms. arXiv preprint arXiv:1707.06347, 2017.
[190] Carel van Niekerk, Renato Vukovic, Benjamin Matthias Ruppik, Hsien-Chin Lin, and Milica Gavsi’c. Post-training large
      language models via reinforcement learning from self-feedback, 2025. URL https://arxiv.org/abs/2507.21931v1.
[191] Andrew Kiruluta, Andreas Lemos, and Priscilla Burity. History-aware cross-attention reinforcement: Self-supervised
      multi turn and chain-of-thought fine-tuning with vllm, 2025. URL https://arxiv.org/abs/2506.11108v1.



                                                             51
                                  A Survey of Vibe Coding with Large Language Models



[192] Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen, Yujiu Yang, Nan Duan, and Weizhu Chen. Critic: Large
      language models can self-correct with tool-interactive critiquing. International Conference on Learning Representations,
      2023.
[193] Nikita Mehandru, Amanda K. Hall, Olesya Melnichenko, Yulia Dubinina, Daniel Tsirulnikov, David Bamman, Ahmed
      Alaa, Scott Saponas, and V. Malladi. Bioagents: Democratizing bioinformatics analysis with multi-agent systems, 2025.
      URL https://arxiv.org/abs/2501.06314v1.
[194] Yoichi Ishibashi and Yoshimasa Nishimura. Self-organized agents: A llm multi-agent framework toward ultra
      large-scale code generation and optimization. arXiv preprint arXiv:2404.02183, 2024.
[195] Yashar Talebirad and Amirhossein Nadiri. Multi-agent collaboration: Harnessing the power of intelligent llm agents,
      2023. URL https://arxiv.org/abs/2306.03314v1.
[196] Amine Ben Hassouna, Hana Chaari, and Ines Belhaj. Llm-agent-umf: Llm-based agent unified modeling framework
      for seamless integration of multi active/passive core-agents. arXiv preprint, 2024.
[197] Antonis Antoniades, Albert Örwall, Kexun Zhang, Yuxi Xie, Anirudh Goyal, and W. Wang. Swe-search: Enhancing
      software agents with monte carlo tree search and iterative refinement. International Conference on Learning Representations,
      2024.
[198] Sajad Mousavi, Ricardo Luna Guti’errez, Desik Rengarajan, Vineet Gundecha, Ashwin Ramesh Babu, Avisek Naug,
      Antonio Guillen-Perez, and S. Sarkar. N-critics: Self-refinement of large language models with ensemble of critics.
      arXiv preprint, 2023.
[199] Sihyun Park. Self-review framework for enhancing instruction following capability of llm, 2025. URL https:
      //arxiv.org/abs/2507.05598v1.
[200] Yubin Ge, Salvatore Romeo, Jason Cai, Monica Sunkara, and Yi Zhang. Samule: Self-learning agents enhanced by
      multi-level reflection. arXiv preprint arXiv:2509.20562, 2025.
[201] Noah Shinn, Federico Cassano, Beck Labash, A. Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: language
      agents with verbal reinforcement learning. Neural Information Processing Systems, 2023.
[202] Shervin Minaee, Tomas Mikolov, Narjes Nikzad, Meysam Chenaghlu, Richard Socher, Xavier Amatriain, and Jianfeng
      Gao. Large language models: A survey. arXiv preprint arXiv:2402.06196, 2024.
[203] Zibin Zheng, Kaiwen Ning, Yanlin Wang, Jingwen Zhang, Dewu Zheng, Mingxi Ye, and Jiachi Chen. A survey of
      large language models for code: Evolution, benchmarking, and future trends, 2023. URL https://arxiv.org/abs/
      2311.10372v2.
[204] Yi Tay, Mostafa Dehghani, Dara Bahri, and Donald Metzler. Efficient transformers: A survey, 2022. URL https:
      //arxiv.org/abs/2009.06732.
[205] Zhongwei Wan, Xin Wang, Che Liu, Samiul Alam, Yu Zheng, Jiachen Liu, Zhongnan Qu, Shen Yan, Yi Zhu, Quanlu
      Zhang, et al. Efficient large language models: A survey. arXiv preprint arXiv:2312.03863, 2023.
[206] Jiaheng Liu, Dawei Zhu, Zhiqi Bai, Yancheng He, Huanxuan Liao, Haoran Que, Zekun Wang, Chenchen Zhang,
      Ge Zhang, Jiebin Zhang, et al. A comprehensive survey on long context language modeling. arXiv preprint
      arXiv:2503.17407, 2025.
[207] Ce Zhou, Qian Li, Chen Li, Jun Yu, Yixin Liu, Guangjing Wang, Kai Zhang, Cheng Ji, Qiben Yan, Lifang He, et al.
      A comprehensive survey on pretrained foundation models: A history from bert to chatgpt. International Journal of
      Machine Learning and Cybernetics, pages 1–65, 2024.
[208] Yupeng Chang, Xu Wang, Jindong Wang, Yuan Wu, Linyi Yang, Kaijie Zhu, Hao Chen, Xiaoyuan Yi, Cunxiang Wang,
      Yidong Wang, et al. A survey on evaluation of large language models. ACM transactions on intelligent systems and
      technology, 15(3):1–45, 2024.
[209] Sander Schulhoff, Michael Ilie, Nishant Balepur, Konstantine Kahadze, Amanda Liu, Chenglei Si, Yinheng Li, Aayush
      Gupta, HyoJung Han, Sevien Schulhoff, et al. The prompt report: a systematic survey of prompt engineering
      techniques. arXiv preprint arXiv:2406.06608, 2024.
[210] Pranab Sahoo, Ayush Kumar Singh, Sriparna Saha, Vinija Jain, S. Mondal, and Aman Chadha. A systematic survey of
      prompt engineering in large language models: Techniques and applications, 2024. URL https://arxiv.org/abs/2402.
      07927v2.
[211] Shubham Vatsal and Harsh Dubey. A survey of prompt engineering methods in large language models for different
      nlp tasks. arXiv preprint arXiv:2407.12994, 2024.



                                                              52
                                A Survey of Vibe Coding with Large Language Models



[212] Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Jingyuan Ma, Rui Li, Heming Xia, Jingjing Xu, Zhiyong Wu, Tianyu
      Liu, et al. A survey on in-context learning. arXiv preprint arXiv:2301.00234, 2022.
[213] Zheng Chu, Jingchang Chen, Qianglong Chen, Weijiang Yu, Tao He, Haotian Wang, Weihua Peng, Ming Liu, Bing
      Qin, and Ting Liu. Navigate through enigmatic labyrinth a survey of chain of thought reasoning: Advances, frontiers
      and future. arXiv preprint arXiv:2309.15402, 2023.
[214] Yu Xia, Rui Wang, Xu Liu, Mingyan Li, Tong Yu, Xiang Chen, Julian McAuley, and Shuai Li. Beyond chain-of-thought:
      A survey of chain-of-x paradigms for llms. arXiv preprint arXiv:2404.15676, 2024.
[215] Yaoting Wang, Shengqiong Wu, Yuecheng Zhang, Shuicheng Yan, Ziwei Liu, Jiebo Luo, and Hao Fei. Multimodal
      chain-of-thought reasoning: A comprehensive survey. arXiv preprint arXiv:2503.12605, 2025.
[216] Shukang Yin, Chaoyou Fu, Sirui Zhao, Ke Li, Xing Sun, Tong Xu, and Enhong Chen. A survey on multimodal large
      language models. National Science Review, 11(12):nwae403, 2024.
[217] Duzhen Zhang, Yahan Yu, Jiahua Dong, Chenxing Li, Dan Su, Chenhui Chu, and Dong Yu. Mm-llms: Recent advances
      in multimodal large language models. arXiv preprint arXiv:2401.13601, 2024.
[218] Chia Xin Liang, Pu Tian, Caitlyn Heqi Yin, Yao Yua, Wei An-Hou, Li Ming, Tianyang Wang, Ziqian Bi, and Ming Liu.
      A comprehensive survey and guide to multimodal large language models in vision-language tasks. arXiv preprint
      arXiv:2411.06284, 2024.
[219] Jiayang Wu, Wensheng Gan, Zefeng Chen, Shicheng Wan, and Philip S Yu. Multimodal large language models: A
      survey. In 2023 IEEE International Conference on Big Data (BigData), pages 2247–2256. IEEE, 2023.
[220] S. Srivastava and Vaneet Aggarwal. A technical survey of reinforcement learning techniques for large language
      models, 2025. URL https://arxiv.org/abs/2507.04136v1.
[221] Zeyu Zhang, Quanyu Dai, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. A
      survey on the memory mechanism of large language model-based agents. ACM Transactions on Information Systems, 43
      (6):1–47, 2025.
[222] Yuji Cao, Huan Zhao, Yuheng Cheng, Ting Shu, Yue Chen, Guolong Liu, Gaoqi Liang, Junhua Zhao, Jinyue Yan, and
      Yun Li. Survey on large language model-enhanced reinforcement learning: Concept, taxonomy, and methods. IEEE
      Transactions on Neural Networks and Learning Systems, 2024.
[223] Timo Kaufmann, Paul Weng, Viktor Bengs, and Eyke Hüllermeier. A survey of reinforcement learning from human
      feedback. arXiv preprint arXiv:2409.14335, 2024.
[224] Yingwei Ma, Yue Liu, Yue Yu, Yuanliang Zhang, Yu Jiang, Changjian Wang, and Shanshan Li. At which training
      stage does code data help llms reasoning? arXiv preprint arXiv:2309.16298, 2023.
[225] Zhang Shengyu, Dong Linfeng, Li Xiaoya, Zhang Sen, Sun Xiaofei, Wang Shuhe, Li Jiwei, Runyi Hu, Zhang Tianwei,
      Fei Wu, et al. Instruction tuning for large language models: A survey. arXiv preprint arXiv:2308.10792, 2023.
[226] Guiyao Tie, Zeli Zhao, Dingjie Song, Fuyang Wei, Rong Zhou, Yurou Dai, Wen Yin, Zhejian Yang, Jiangyue Yan, Yao
      Su, et al. A survey on post-training of large language models. arXiv e-prints, pages arXiv–2503, 2025.
[227] Wenyi Xiao, Zechuan Wang, Leilei Gan, Shuai Zhao, Zongrui Li, Ruirui Lei, Wanggui He, Luu Anh Tuan, Long
      Chen, Hao Jiang, et al. A comprehensive survey of direct preference optimization: Datasets, theories, variants, and
      applications. arXiv preprint arXiv:2410.15595, 2024.
[228] Lingling Xu, Haoran Xie, Si-Zhao Joe Qin, Xiaohui Tao, and Fu Lee Wang. Parameter-efficient fine-tuning methods
      for pretrained language models: A critical review and assessment. arXiv preprint arXiv:2312.12148, 2023.
[229] Yu Su, Diyi Yang, Shunyu Yao, and Tao Yu. Language agents: Foundations, prospects, and risks. In Proceedings of the
      2024 Conference on Empirical Methods in Natural Language Processing: Tutorial Abstracts, pages 17–24, 2024.
[230] Pengyu Zhao, Zijian Jin, and Ning Cheng. An in-depth survey of large language model-based artificial intelligence
      agents, 2023. URL https://arxiv.org/abs/2309.14365v1.
[231] Mohamed Amine Ferrag, Norbert Tihanyi, and Merouane Debbah. From llm reasoning to autonomous ai agents: A
      comprehensive review. arXiv preprint arXiv:2504.19678, 2025.
[232] Taicheng Guo, Xiuying Chen, Yaqi Wang, Ruidi Chang, Shichao Pei, Nitesh V Chawla, Olaf Wiest, and Xiangliang
      Zhang. Large language model based multi-agents: A survey of progress and challenges. arXiv preprint arXiv:2402.01680,
      2024.
[233] Shuaihang Chen, Yuanxing Liu, Wei Han, Weinan Zhang, and Ting Liu. A survey on llm-based multi-agent system:
      Recent advances and new frontiers in application. arXiv preprint arXiv:2412.17481, 2024.


                                                           53
                                A Survey of Vibe Coding with Large Language Models



[234] Xu Huang, Weiwen Liu, Xiaolong Chen, Xingmei Wang, Hao Wang, Defu Lian, Yasheng Wang, Ruiming Tang, and
      Enhong Chen. Understanding the planning of llm agents: A survey. arXiv preprint arXiv:2402.02716, 2024.
[235] Tula Masterman, Sandi Besen, Mason Sawtell, and Alex Chao. The landscape of emerging ai agent architectures for
      reasoning, planning, and tool calling: A survey. arXiv preprint arXiv:2404.11584, 2024.
[236] Weikai Xu, Chengrui Huang, Shen Gao, and Shuo Shang. Llm-based agents for tool learning: A survey: W. xu et al.
      Data Science and Engineering, pages 1–31, 2025.
[237] Asaf Yehudai, Lilach Eden, Alan Li, Guy Uziel, Yilun Zhao, Roy Bar-Haim, Arman Cohan, and Michal Shmueli-Scheuer.
      Survey on evaluation of llm-based agents. arXiv preprint arXiv:2503.16416, 2025.
[238] Mahmoud Mohammadi, Yipeng Li, Jane Lo, and Wendy Yip. Evaluation and benchmarking of llm agents: A survey.
      In Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 2, pages 6129–6139, 2025.
[239] Liangbo Ning, Ziran Liang, Zhuohang Jiang, Haohao Qu, Yujuan Ding, Wenqi Fan, Xiao-yong Wei, Shanru Lin, Hui
      Liu, Philip S Yu, et al. A survey of webagents: Towards next-generation ai agents for web automation with large
      foundation models. In Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 2,
      pages 6140–6150, 2025.
[240] Jiaqi Wei, Yuejin Yang, Xiang Zhang, Yuhan Chen, Xiang Zhuang, Zhangyang Gao, Dongzhan Zhou, Guangshuai
      Wang, Zhiqiang Gao, Juntai Cao, et al. From ai for science to agentic science: A survey on autonomous scientific
      discovery. arXiv preprint arXiv:2508.14111, 2025.
[241] Xueyu Hu, Tao Xiong, Biao Yi, Zishu Wei, Ruixuan Xiao, Yurun Chen, Jiasheng Ye, Meiling Tao, Xiangxin Zhou, Ziyu
      Zhao, et al. Os agents: A survey on mllm-based agents for computer, phone and browser use. In Proceedings of the
      63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 7436–7465, 2025.
[242] Jinyuan Fang, Yanwen Peng, Xi Zhang, Yingxu Wang, Xinhao Yi, Guibin Zhang, Yi Xu, Bin Wu, Siwei Liu, Zihao Li,
      et al. A comprehensive survey of self-evolving ai agents: A new paradigm bridging foundation models and lifelong
      agentic systems. arXiv preprint arXiv:2508.07407, 2025.
[243] Yihong Dong, Xue Jiang, Jiaru Qian, Tian Wang, Kechi Zhang, Zhi Jin, and Ge Li. A survey on code generation with
      llm-based agents, 2025. URL https://arxiv.org/abs/2508.00083v2.
[244] Huanting Wang, Jingzhi Gong, Huawei Zhang, Jie Xu, and Zheng Wang. Ai agentic programming: A survey of
      techniques, challenges, and opportunities. arXiv preprint arXiv:2508.11126, 2025.
[245] Hung Le, Yue Wang, Akhilesh Deepak Gotmare, S. Savarese, and S. Hoi. Coderl: Mastering code generation through
      pretrained models and deep reinforcement learning. Neural Information Processing Systems, 2022.
[246] Parshin Shojaee, Aneesh Jain, Sindhu Tipirneni, and Chandan K Reddy. Execution-based code generation using deep
      reinforcement learning. arXiv preprint arXiv:2301.13816, 2023.
[247] Jiate Liu, Yiqin Zhu, Kaiwen Xiao, Qiang Fu, Xiao Han, Wei Yang, and Deheng Ye. Rltf: Reinforcement learning from
      unit test feedback. arXiv preprint arXiv:2307.04349, 2023.
[248] Shihan Dou, Yan Liu, Haoxiang Jia, Limao Xiong, Enyu Zhou, Wei Shen, Junjie Shan, Caishuang Huang, Xiao Wang,
      Xiaoran Fan, et al. Stepcoder: Improve code generation with reinforcement learning from compiler feedback. arXiv
      preprint arXiv:2402.01391, 2024.
[249] DeepSeek-AI, Qihao Zhu, Daya Guo, Zhihong Shao, Dejian Yang, Peiyi Wang, Runxin Xu, Y. Wu, Yukun Li, Huazuo
      Gao, Shirong Ma, Wangding Zeng, Xiao Bi, Zihui Gu, Hanwei Xu, Damai Dai, Kai Dong, Liyue Zhang, Yishi Piao,
      Zhibin Gou, Zhenda Xie, Zhewen Hao, Bing-Li Wang, Jun-Mei Song, Deli Chen, Xin Xie, Kang Guan, Yu mei You,
      A. Liu, Qiushi Du, Wenjun Gao, Xuan Lu, Qinyu Chen, Yaohui Wang, C. Deng, Jiashi Li, Chenggang Zhao, C. Ruan,
      Fuli Luo, and W. Liang. Deepseek-coder-v2: Breaking the barrier of closed-source models in code intelligence. arXiv
      preprint, 2024.
[250] Yingwei Ma, Qingping Yang, Rongyu Cao, Binhua Li, Fei Huang, and Yongbin Li. Alibaba lingmaagent: Improving
      automated issue resolution via comprehensive repository exploration. In Proceedings of the 33rd ACM International
      Conference on the Foundations of Software Engineering, pages 238–249, 2025.
[251] Zhiyuan Pan, Xing Hu, Xin Xia, and Xiaohu Yang. Enhancing repository-level code generation with integrated
      contextual information. arXiv preprint arXiv:2406.03283, 2024.
[252] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang,
      Steven Ka Shing Yau, Zijuan Lin, et al. Metagpt: Meta programming for a multi-agent collaborative framework. In
      International Conference on Learning Representations, 2024.




                                                           54
                                 A Survey of Vibe Coding with Large Language Models



[253] Noble Saji Mathews and Meiyappan Nagappan. Test-driven development and llm-based code generation. In Proceedings
      of the 39th IEEE/ACM International Conference on Automated Software Engineering, pages 1583–1594, 2024.
[254] Rui Yang, Lin Song, Yanwei Li, Sijie Zhao, Yixiao Ge, Xiu Li, and Ying Shan. Gpt4tools: Teaching large language
      model to use tools via self-instruction. Advances in Neural Information Processing Systems, 36:71995–72007, 2023.
[255] Ibrahim Abdelaziz, Kinjal Basu, Mayank Agarwal, Sadhana Kumaravel, Matthew Stallone, Rameswar Panda, Yara
      Rizk, GP Bhargav, Maxwell Crouse, Chulaka Gunasekara, et al. Granite-function calling model: Introducing function
      calling abilities via multi-task learning of granular tasks. arXiv preprint arXiv:2407.00121, 2024.
[256] Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu Li, Hao Peng, and Heng Ji. Executable code actions
      elicit better llm agents. In Forty-first International Conference on Machine Learning, 2024.
[257] Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, and Yu-Xiong Wang. Language agent tree search
      unifies reasoning acting and planning in language models. arXiv preprint arXiv:2310.04406, 2023.
[258] Sehoon Kim, Suhong Moon, Ryan Tabrizi, Nicholas Lee, Michael W. Mahoney, Kurt Keutzer, and Amir Gholami. An
      llm compiler for parallel function calling, 2024. URL https://arxiv.org/abs/2312.04511.
[259] Lutfi Eren Erdogan, Nicholas Lee, Siddharth Jha, Sehoon Kim, Ryan Tabrizi, Suhong Moon, Coleman Hooper,
      Gopala Anumanchipalli, Kurt Keutzer, and Amir Gholami. Tinyagent: Function calling at the edge. arXiv preprint
      arXiv:2409.00608, 2024.
[260] Zora Zhiruo Wang, Akari Asai, Xinyan Velocity Yu, Frank F Xu, Yiqing Xie, Graham Neubig, and Daniel Fried.
      Coderag-bench: Can retrieval augment code generation? arXiv preprint arXiv:2406.14497, 2024.
[261] Bing Liu, Zhou Jianxiang, Dan Meng, and Haonan Lu. An evaluation mechanism of llm-based agents on manipulating
      apis. In Findings of the Association for Computational Linguistics: EMNLP 2024, pages 4649–4662, 2024.
[262] Zhen Guo, Adriana Meza Soria, Wei Sun, Yikang Shen, and Rameswar Panda. Api pack: A massive multi-programming
      language dataset for api call generation. arXiv preprint arXiv:2402.09615, 2024.
[263] Yuxiang Wei, Federico Cassano, Jiawei Liu, Yifeng Ding, Naman Jain, Zachary Mueller, Harm de Vries, Leandro
      Von Werra, Arjun Guha, and Lingming Zhang. Selfcodealign: Self-alignment for code generation. Advances in Neural
      Information Processing Systems, 37:62787–62874, 2024.
[264] Jingxuan He, Mark Vero, Gabriela Krasnopolska, and Martin Vechev. Instruction tuning for secure code generation.
      arXiv preprint arXiv:2402.09497, 2024.
[265] Zeyuan Ma, Hongshu Guo, Jiacheng Chen, Guojun Peng, Zhiguang Cao, Yining Ma, and Yue-Jiao Gong. Llamoco:
      Instruction tuning of large language models for optimization code generation. arXiv preprint arXiv:2403.01131, 2024.
[266] Yingwei Ma, Rongyu Cao, Yongchang Cao, Yue Zhang, Jue Chen, Yibo Liu, Yuchen Liu, Binhua Li, Fei Huang,
      and Yongbin Li. Lingma swe-gpt: An open development-process-centric language model for automated software
      improvement. arXiv preprint arXiv:2411.00622, 2024.
[267] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, Yu Wu, YK Li,
      et al. Deepseek-coder: When the large language model meets programming–the rise of code intelligence. arXiv preprint
      arXiv:2401.14196, 2024.
[268] Anton Lozhkov, Raymond Li, Loubna Ben Allal, Federico Cassano, Joel Lamy-Poirier, Nouamane Tazi, Ao Tang,
      Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei, et al. Starcoder 2 and the stack v2: The next generation. arXiv preprint
      arXiv:2402.19173, 2024.
[269] Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling,
      Felix Gimeno, Agustin Dal Lago, et al. Competition-level code generation with alphacode. Science, 378(6624):1092–1097,
      2022.
[270] Jason H Moore and Nicholas Tatonetti. Vibe coding: a new paradigm for biomedical software development. BioData
      Mining, 18:46, 2025.
[271] Yubo Dong, Xukun Zhu, Zhengzhe Pan, Linchao Zhu, and Yi Yang. Villageragent: A graph-based multi-agent
      framework for coordinating complex task dependencies in minecraft. Annual Meeting of the Association for Computational
      Linguistics, 2024.
[272] Yihong Dong, Xue Jiang, Zhi Jin, and Ge Li. Self-collaboration code generation via chatgpt. ACM Transactions on
      Software Engineering and Methodology, 2023.
[273] Alina Mihaela Dima and Maria Alexandra Maassen. From waterfall to agile software: Development models in the it
      sector, 2006 to 2018. impacts on company management. Journal of International Studies (2071-8330), 11(2), 2018.



                                                            55
                                 A Survey of Vibe Coding with Large Language Models



[274] David S. Janzen and Hossein Saiedian. Test-driven development concepts, taxonomy, and future direction. Computer,
      38:43–50, 2005. URL https://api.semanticscholar.org/CorpusID:9062470.
[275] Claire Le Goues, Michael Pradel, and Abhik Roychoudhury. Automated program repair. Communications of the ACM,
      2019.
[276] Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang Hong, Ming Zhang, Junzhe Wang, Senjie Jin,
      Enyu Zhou, Rui Zheng, Xiaoran Fan, Xiao Wang, Limao Xiong, Qin Liu, Yuhao Zhou, Weiran Wang, Changhao Jiang,
      Yicheng Zou, Xiangyang Liu, Zhangyue Yin, Shihan Dou, Rongxiang Weng, Wensen Cheng, Qi Zhang, Wenjuan Qin,
      Yongyan Zheng, Xipeng Qiu, Xuanjing Huan, and Tao Gui. The rise and potential of large language model based
      agents: A survey, 2023. URL https://arxiv.org/abs/2309.07864v3.
[277] April Clyburne-Sherin, Xu Fei, and S. Green. Computational reproducibility via containers in psychology. Meta-
      Psychology, 2019.
[278] Frank F. Xu, Uri Alon, Graham Neubig, and Vincent J. Hellendoorn. A systematic evaluation of large language
      models of code. MAPS@PLDI, 2022.
[279] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. A survey on large language models for code
      generation, 2024. URL https://arxiv.org/abs/2406.00515v2.
[280] Alon Albalak, Yanai Elazar, Sang Michael Xie, Shayne Longpre, Nathan Lambert, Xinyi Wang, Niklas Muennighoff,
      Bairu Hou, Liangming Pan, Haewon Jeong, Colin Raffel, Shiyu Chang, Tatsunori Hashimoto, and W. Wang. A survey
      on data selection for language models. Trans. Mach. Learn. Res., 2024.
[281] Shayne Longpre, Le Hou, Tu Vu, Albert Webson, Hyung Won Chung, Yi Tay, Denny Zhou, Quoc V Le, Barret Zoph,
      Jason Wei, et al. The flan collection: Designing data and methods for effective instruction tuning. In International
      Conference on Machine Learning, pages 22631–22648. PMLR, 2023.
[282] Viraat Aryabumi, Yixuan Su, Raymond Ma, Adrien Morisot, Ivan Zhang, Acyr F. Locatelli, Marzieh Fadaee, A. Ustun,
      and Sara Hooker. To code, or not to code? exploring impact of code in pre-training, 2024. URL https://arxiv.org/
      abs/2408.10914v1.
[283] Meng Chen, Philip Arthur, Qianyu Feng, Cong Duy Vu Hoang, Yu-Heng Hong, Mahdi Kazemi Moghaddam, Omid
      Nezami, Thien Nguyen, Gioacchino Tangari, Duy Vu, T. Vu, Mark Johnson, K. Kenthapadi, Don Dharmasiri, Long
      Duong, and Yuan-Fang Li. Mastering the craft of data synthesis for codellms. North American Chapter of the Association
      for Computational Linguistics, 2024.
[284] Can Xu, Qingfeng Sun, Kai Zheng, Xiubo Geng, Pu Zhao, Jiazhan Feng, Chongyang Tao, and Daxin Jiang. Wizardlm:
      Empowering large pre-trained language models to follow complex instructions. International Conference on Learning
      Representations, 2023.
[285] Yuxiang Wei, Zhe Wang, Jiawei Liu, Yifeng Ding, and Lingming Zhang. Magicoder: Empowering code generation
      with oss-instruct. International Conference on Machine Learning, 2023.
[286] Tianyu Zheng, Ge Zhang, Tianhao Shen, Xueling Liu, Bill Yuchen Lin, Jie Fu, Wenhu Chen, and Xiang Yue.
      Opencodeinterpreter: Integrating code generation with execution and refinement. Annual Meeting of the Association for
      Computational Linguistics, 2024.
[287] Xipeng Qiu, Tianxiang Sun, Yige Xu, Yunfan Shao, Ning Dai, and Xuanjing Huang. Pre-trained models for natural
      language processing: A survey. Science China technological sciences, 63(10):1872–1897, 2020.
[288] Jianxin Li, Liang Qu, Taotao Cai, Zhixue Zhao, Nur Al Hasan Haldar, Aneesh Krishna, Xiangjie Kong, F. Macau,
      Tanmoy Chakraborty, Aniket Deroy, Binshan Lin, Karen Blackmore, N. Noman, Jingxian Cheng, Ningning Cui, and
      Jianliang Xu. Ai-generated content in cross-domain applications: Research trends, challenges and propositions, 2025.
      URL https://arxiv.org/abs/2509.11151v1.
[289] F. Liu, Ge Li, Yunfei Zhao, and Zhi Jin. Multi-task learning based pre-trained language model for code completion.
      International Conference on Automated Software Engineering, 2020.
[290] Kang Yang, Xinjun Mao, Shangwen Wang, Tanghaoran Zhang, Bo Lin, Yanlin Wang, Yihao Qin, Zhang Zhang, and
      Xiaoguang Mao. Enhancing code intelligence tasks with chatgpt, 2023. URL https://arxiv.org/abs/2312.15202v1.
[291] Yue Liu, C. Tantithamthavorn, Yonghui Liu, Patanamon Thongtanunam, and Li Li. Automatically recommend code
      updates: Are we there yet? ACM Transactions on Software Engineering and Methodology, 2022.
[292] M. Saad, Jos’e Antonio Hern’andez L’opez, Boqi Chen, Neil Ernst, D’aniel Varr’o, and Tushar Sharma. Senai: Towards
      software engineering native generative artificial intelligence, 2025. URL https://arxiv.org/abs/2503.15282v1.




                                                            56
                                 A Survey of Vibe Coding with Large Language Models



[293] Youpeng Li, Weiliang Qi, Xuyu Wang, Fuxun Yu, and Xinda Wang. Revisiting pre-trained language models for
      vulnerability detection, 2025. URL https://arxiv.org/abs/2507.16887v2.
[294] Michael R. Lyu, Baishakhi Ray, Abhik Roychoudhury, Shin Hwei Tan, and Patanamon Thongtanunam. Automatic
      programming: Large language models and beyond. ACM Transactions on Software Engineering and Methodology, 2024.
[295] Jiayi Lin, Hande Dong, Yutao Xie, and Lei Zhang. Scaling laws behind code understanding model, 2024. URL
      https://arxiv.org/abs/2402.12813v1.
[296] Paras Jain, Ajay Jain, Tianjun Zhang, P. Abbeel, Joseph E. Gonzalez, and Ion Stoica. Contrastive code representation
      learning. Conference on Empirical Methods in Natural Language Processing, 2020.
[297] Xin Zhou, Sicong Cao, Xiaobing Sun, and David Lo. Large language model for vulnerability detection and repair:
      Literature review and the road ahead. ACM Transactions on Software Engineering and Methodology, 2024.
[298] K. Dharma and Clayton T. Morrison. Neural machine translation for code generation, 2023. URL https://arxiv.org/
      abs/2305.13504v1.
[299] Jiayi Pan, Xingyao Wang, Graham Neubig, Navdeep Jaitly, Heng Ji, Alane Suhr, and Yizhe Zhang. Training software
      engineering agents and verifiers with swe-gym. arXiv preprint arXiv:2412.21139, 2024.
[300] Guilherme Penedo, Anton Lozhkov, Hynek Kydlíček, Loubna Ben Allal, Edward Beeching, Agustín Piqueres Lajarín,
      Quentin Gallouédec, Nathan Habib, Lewis Tunstall, and Leandro von Werra. Codeforces cots. https://huggingface.
      co/datasets/open-r1/codeforces-cots, 2025.
[301] Chengxing Xie, Bowen Li, Chang Gao, He Du, Wai Lam, Difan Zou, and Kai Chen. Swe-fixer: Training open-source
      llms for effective and efficient github issue resolution. arXiv preprint arXiv:2501.05040, 2025.
[302] Zhangchen Xu, Yang Liu, Yueqin Yin, Mingyuan Zhou, and Radha Poovendran. Kodcode: A diverse, challenging,
      and verifiable synthetic dataset for coding. arXiv preprint arXiv:2503.02951, 2025.
[303] Jiawei Liu and Lingming Zhang. Code-r1: Reproducing r1 for code with reliable rewards. https://github.com/
      ganler/code-r1, 2025.
[304] Zhaojian Yu, Yinghao Wu, Yilun Zhao, Arman Cohan, and Xiao-Ping Zhang. Z1: Efficient test-time scaling with code.
      arXiv preprint arXiv:2504.00810, 2025.
[305] Yifei Liu, Li Lyna Zhang, Yi Zhu, Bingcheng Dong, Xudong Zhou, Ning Shang, Fan Yang, and Mao Yang. rstar-coder:
      Scaling competitive code reasoning with a large-scale verified dataset. arXiv preprint arXiv:2505.21297, 2025.
[306] Yunhui Xia, Wei Shen, Yan Wang, Jason Klein Liu, Huifeng Sun, Siyue Wu, Jian Hu, and Xiaolong Xu. Leetcodedataset:
      A temporal dataset for robust evaluation and efficient training of code llms, 2025. URL https://arxiv.org/abs/2504.
      14655.
[307] Wasi Uddin Ahmad, Sean Narenthiran, Somshubra Majumdar, Aleksander Ficek, Siddhartha Jain, Jocelyn Huang,
      Vahid Noroozi, and Boris Ginsburg. Opencodereasoning: Advancing data distillation for competitive coding. arXiv
      preprint arXiv:2504.01943, 2025.
[308] Michael Luo, Sijun Tan, Roy Huang, Ameen Patel, Alpay Ariyak, Qingyang Wu, Xiaoxiang Shi,
      Rachel Xin, Colin Cai, Maurice Weber, Ce Zhang, Li Erran Li, Raluca Ada Popa, and Ion Sto-
      ica. Deepcoder: A fully open-source 14b coder at o3-mini level. https://pretty-radio-b75.notion.site/
      DeepCoder-A-Fully-Open-Source-14B-Coder-at-O3-mini-Level-1cf81902c14680b3bee5eb349a512a51, 2025. Notion
      Blog.
[309] John Yang, Carlos E Jimenez, Alex L Zhang, Kilian Lieret, Joyce Yang, Xindi Wu, Ori Press, Niklas Muennighoff,
      Gabriel Synnaeve, Karthik R Narasimhan, et al. Swe-bench multimodal: Do ai systems generalize to visual software
      domains? arXiv preprint arXiv:2410.03859, 2024.
[310] John Yang, Kilian Lieret, Carlos E. Jimenez, Alexander Wettig, Kabir Khandpur, Yanzhe Zhang, Binyuan Hui, Ofir
      Press, Ludwig Schmidt, and Diyi Yang. Swe-smith: Scaling data for software engineering agents, 2025. URL
      https://arxiv.org/abs/2504.21798.
[311] Daoguang Zan, Zhirong Huang, Wei Liu, Hanwu Chen, Linhao Zhang, Shulin Xin, Lu Chen, Qi Liu, Xiaojian Zhong,
      Aoyan Li, et al. Multi-swe-bench: A multilingual benchmark for issue resolving. arXiv preprint arXiv:2504.02605, 2025.
[312] Jun Shern Chan, Neil Chowdhury, Oliver Jaffe, James Aung, Dane Sherburn, Evan Mays, Giulio Starace, Kevin
      Liu, Leon Maksin, Tejal Patwardhan, et al. Mle-bench: Evaluating machine learning agents on machine learning
      engineering. arXiv preprint arXiv:2410.07095, 2024.




                                                            57
                                  A Survey of Vibe Coding with Large Language Models



[313] Giulio Starace, Oliver Jaffe, Dane Sherburn, James Aung, Jun Shern Chan, Leon Maksin, Rachel Dias, Evan Mays,
      Benjamin Kinsella, Wyatt Thompson, Johannes Heidecke, Amelia Glaese, and Tejal Patwardhan. Paperbench: Evaluating
      ai’s ability to replicate ai research, 2025. URL https://arxiv.org/abs/2504.01848.
[314] The Terminal-Bench Team. Terminal-bench: A benchmark for ai agents in terminal environments, Apr 2025. URL
      https://github.com/laude-institute/terminal-bench.
[315] Yuxiang Wei, Olivier Duchenne, Jade Copet, Quentin Carbonneaux, Lingming Zhang, Daniel Fried, Gabriel Synnaeve,
      Rishabh Singh, and Sida I Wang. Swe-rl: Advancing llm reasoning via reinforcement learning on open software
      evolution. arXiv preprint arXiv:2502.18449, 2025.
[316] Jiandong Gao, Xiao Zhang, Ji Wu, and Miao Li. Enhancing elusive clues in knowledge learning by contrasting
      attention of language models. AAAI Conference on Artificial Intelligence, 2024.
[317] Vaibhav Singh, Paul Janson, Paria Mehrbod, Adam Ibrahim, Irina Rish, Eugene Belilovsky, and Benjamin Th’erien.
      Beyond cosine decay: On the effectiveness of infinite learning rate schedule for continual pre-training, 2025. URL
      https://arxiv.org/abs/2503.02844v3.
[318] Adam Ibrahim, Benjamin Th’erien, Kshitij Gupta, Mats L. Richter, Quentin Anthony, Timothée Lesort, Eugene
      Belilovsky, and Irina Rish. Simple and scalable strategies to continually pre-train large language models. Trans. Mach.
      Learn. Res., 2024.
[319] James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A Rusu, Kieran
      Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, et al. Overcoming catastrophic forgetting in neural
      networks. Proceedings of the national academy of sciences, 114(13):3521–3526, 2017.
[320] Michael McCloskey and Neal J Cohen. Catastrophic interference in connectionist networks: The sequential learning
      problem. In Psychology of learning and motivation, volume 24, pages 109–165. Elsevier, 1989.
[321] Gido M van de Ven, Nicholas Soures, and Dhireesha Kudithipudi. Continual learning and catastrophic forgetting.
      arXiv preprint arXiv:2403.05175, 2024.
[322] Timothée Lesort. Continual learning: Tackling catastrophic forgetting in deep neural networks with replay processes.
      arXiv preprint arXiv:2007.00487, 2020.
[323] Yong Xie, Karan Aggarwal, and Aitzaz Ahmad. Efficient continual pre-training for building domain specific large
      language models. Annual Meeting of the Association for Computational Linguistics, 2023.
[324] Sebastian Ruder and Barbara Plank. Learning to select data for transfer learning with bayesian optimization. Conference
      on Empirical Methods in Natural Language Processing, 2017.
[325] Yulia Tsvetkov, Manaal Faruqui, Wang Ling, B. MacWhinney, and Chris Dyer. Learning the curriculum with bayesian
      optimization for task-specific word representation learning. Annual Meeting of the Association for Computational Linguistics,
      2016.
[326] Suchin Gururangan, Ana Marasović, Swabha Swayamdipta, Kyle Lo, Iz Beltagy, Doug Downey, and Noah A. Smith.
      Don’t stop pretraining: Adapt language models to domains and tasks. Annual Meeting of the Association for Computational
      Linguistics, 2020.
[327] Yiduo Guo, Jie Fu, Huishuai Zhang, Dongyan Zhao, and Yikang Shen. Efficient continual pre-training by mitigating
      the stability gap, 2024. URL https://arxiv.org/abs/2406.14833v2.
[328] Seyed Iman Mirzadeh, Arslan Chaudhry, Huiyi Hu, Razvan Pascanu, Dilan Gorur, and Mehrdad Farajtabar. Wide
      neural networks forget less catastrophically. International Conference on Machine Learning, 2021.
[329] O. Ovadia, Meni Brief, Rachel Lemberg, and Eitam Sheetrit. Knowledge-instruct: Effective continual pre-training from
      limited data using instructions. arXiv preprint, 2025.
[330] Nikhil Kandpal, H. Deng, Adam Roberts, Eric Wallace, and Colin Raffel. Large language models struggle to learn
      long-tail knowledge. International Conference on Machine Learning, 2022.
[331] Jiaheng Liu, Ken Deng, Congnan Liu, Jian Yang, Shukai Liu, He Zhu, Peng Zhao, Linzheng Chai, Yanan Wu, Ke Jin,
      et al. M2rc-eval: Massively multilingual repository-level code completion evaluation. arXiv preprint arXiv:2410.21157,
      2024.
[332] Zhiqiang Yuan, Junwei Liu, Qiancheng Zi, Mingwei Liu, Xin Peng, and Yiling Lou. Evaluating instruction-tuned large
      language models on code comprehension and generation, 2023. URL https://arxiv.org/abs/2308.01240v1.
[333] Preetum Nakkiran, Gal Kaplun, Yamini Bansal, Tristan Yang, B. Barak, and I. Sutskever. Deep double descent: where
      bigger models and more data hurt. International Conference on Learning Representations, 2019.



                                                               58
                                 A Survey of Vibe Coding with Large Language Models



[334] Ilia Shumailov, Zakhar Shumaylov, Yiren Zhao, Nicolas Papernot, Ross Anderson, and Yarin Gal. Ai models collapse
      when trained on recursively generated data. The Naturalist, 2024.
[335] Teng Xiao, Mingxiao Li, Yige Yuan, Huaisheng Zhu, Chao Cui, and V.G. Honavar. How to leverage demonstration
      data in alignment for large language model? a self-imitation learning perspective. Conference on Empirical Methods in
      Natural Language Processing, 2024.
[336] Junqiao Wang, Zeng Zhang, Yangfan He, Yuyang Song, Tianyu Shi, Yuchen Li, Hengyuan Xu, Kunyu Wu, Guangwu
      Qian, Qiuwu Chen, and Lewei He. Enhancing code llms with reinforcement learning in code generation: A survey,
      2024. URL https://arxiv.org/abs/2412.20367v5.
[337] Shihan Dou, Muling Wu, Jingwen Xu, Rui Zheng, Tao Gui, Qi Zhang, and Xuanjing Huang. Improving rl exploration
      for llm reasoning through retrospective replay, 2025. URL https://arxiv.org/abs/2504.14363v2.
[338] M. Ferrag, Norbert Tihanyi, and M. Debbah. Reasoning beyond limits: Advances and open problems for llms. ICT
      express, 2025.
[339] Zhiheng Xi, Jixuan Huang, Chenyang Liao, Baodai Huang, Honglin Guo, Jiaqi Liu, Rui Zheng, Junjie Ye, Jiazheng
      Zhang, Wenxiang Chen, Wei He, Yiwen Ding, Guanyu Li, Zehui Chen, Zhengyin Du, Xue-Liang Yao, Yufei Xu, Jiecao
      Chen, Tao Gui, Zuxuan Wu, Qi Zhang, Xuanjing Huang, and Yu-Gang Jiang. Agentgym-rl: Training llm agents for
      long-horizon decision making through multi-turn reinforcement learning. arXiv preprint, 2025.
[340] Hongling Xu, Qi Zhu, Heyuan Deng, Jinpeng Li, Lu Hou, Yasheng Wang, Lifeng Shang, Ruifeng Xu, and Fei
      Mi. Kdrl: Post-training reasoning llms via unified knowledge distillation and reinforcement learning, 2025. URL
      https://arxiv.org/abs/2506.02208v1.
[341] Juan A. Rodriguez, Haotian Zhang, Abhay Puri, Aarash Feizi, Rishav Pramanik, Pascal Wichmann, Arnab Mondal,
      Mohammad Reza Samsami, Rabiul Awal, Perouz Taslakian, Spandana Gella, Sai Rajeswar, David Vázquez, Christopher
      Pal, and Marco Pedersoli. Rendering-aware reinforcement learning for vector graphics generation, 2025. URL
      https://arxiv.org/abs/2505.20793v1.
[342] Zitian Gao, Lynx Chen, Joey Zhou, and Bryan Dai. One-shot entropy minimization, 2025. URL https://arxiv.org/
      abs/2505.20282v4.
[343] Pittawat Taveekitworachai, Potsawee Manakul, Sarana Nutanong, and Kunat Pipatanakul. Prior prompt engineering
      for reinforcement fine-tuning, 2025. URL https://arxiv.org/abs/2505.14157v2.
[344] Ning Wang, Bingkun Yao, Jie Zhou, Yuchen Hu, Xi Wang, Zhe Jiang, and Nan Guan. Large language model for
      verilog generation with code-structure-guided reinforcement learning. 2025 IEEE International Conference on LLM-Aided
      Design (ICLAD), 2024.
[345] Hung Le, Dai Do, D. Nguyen, and S. Venkatesh. Reasoning under 1 billion: Memory-augmented reinforcement
      learning for large language models, 2025. URL https://arxiv.org/abs/2504.02273v1.
[346] Zehan Qi, Xiao Liu, Iat Long Iong, Hanyu Lai, Xueqiao Sun, Xinyue Yang, Jiadai Sun, Yu Yang, Shuntian Yao, Tianjie
      Zhang, Wei Xu, Jie Tang, and Yuxiao Dong. Webrl: Training llm web agents via self-evolving online curriculum
      reinforcement learning, 2024. URL https://arxiv.org/abs/2411.02337v3.
[347] Han Xia, Songyang Gao, Qiming Ge, Zhiheng Xi, Qi Zhang, and Xuanjing Huang. Inverse-q*: Token level reinforcement
      learning for aligning large language models without preference data. Conference on Empirical Methods in Natural
      Language Processing, 2024.
[348] Yu Huang. Levels of ai agents: from rules to large language models, 2024. URL https://arxiv.org/abs/2405.06643v2.
[349] Pengfei Cao, Tianyi Men, Wencan Liu, Jingwen Zhang, Xuzhao Li, Xixun Lin, Dianbo Sui, Yanan Cao, Kang
      Liu, and Jun Zhao. Large language models for planning: A comprehensive and systematic survey, 2025. URL
      https://arxiv.org/abs/2505.19683v1.
[350] Dhanya Jayagopal, Justin P. Lubin, and Sarah E. Chasins. Exploring the learnability of program synthesizers by novice
      programmers. ACM Symposium on User Interface Software and Technology, 2022.
[351] Gianni Molinari and Fabio Ciravegna. Towards pervasive distributed agentic generative ai - a state of the art. arXiv
      preprint, 2025.
[352] M. Helmert. The fast downward planning system. Journal of Artificial Intelligence Research, 2006.
[353] Maciej Besta, Nils Blach, Aleš Kubíček, Robert Gerstenberger, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann,
      Michal Podstawski, H. Niewiadomski, P. Nyczyk, and Torsten Hoefler. Graph of thoughts: Solving elaborate problems
      with large language models. AAAI Conference on Artificial Intelligence, 2023.



                                                            59
                                 A Survey of Vibe Coding with Large Language Models



[354] Tapio Pitkäranta and Leena Pitkäranta. Hada: Human-ai agent decision alignment architecture. arXiv preprint, 2025.
[355] Junjie Chen, Haitao Li, Jingli Yang, Yiqun Liu, and Qingyao Ai. Enhancing llm-based agents via global planning and
      hierarchical execution, 2025. URL https://arxiv.org/abs/2504.16563v3.
[356] Junyu Luo, Weizhi Zhang, Ye Yuan, Yusheng Zhao, Junwei Yang, Yiyang Gu, Bohan Wu, Binqi Chen, Ziyue Qiao,
      Qingqing Long, Rongcheng Tu, Xiaoming Luo, Wei Ju, Zhiping Xiao, Yifan Wang, Mengxue Xiao, Chenwu Liu,
      Jingyang Yuan, Shichang Zhang, Yiqiao Jin, Fan Zhang, Xianhong Wu, Hanqing Zhao, Dacheng Tao, Philip S. Yu,
      and Ming Zhang. Large language model agent: A survey on methodology, applications and challenges, 2025. URL
      https://arxiv.org/abs/2503.21460v1.
[357] Charles Packer, Vivian Fang, Shishir_G Patil, Kevin Lin, Sarah Wooders, and Joseph_E Gonzalez. Memgpt: Towards
      llms as operating systems. arXiv preprint arXiv:2310.08560, 2023.
[358] Yutao Ouyang, Jinhan Li, Yunfei Li, Zhongyu Li, Chao Yu, K. Sreenath, and Yi Wu. Long-horizon locomotion and
      manipulation on a quadrupedal robot with large language models, 2024. URL https://arxiv.org/abs/2404.05291v3.
[359] Xiaopan Zhang, Hao Qin, Fuquan Wang, Yue Dong, and Jiachen Li. Lamma-p: Generalizable multi-agent long-horizon
      task allocation and planning with lm-driven pddl planner. IEEE International Conference on Robotics and Automation,
      2024.
[360] Ishika Singh, David Traum, and Jesse Thomason. Twostep: Multi-agent task planning using classical planners and
      large language models, 2024. URL https://arxiv.org/abs/2403.17246v2.
[361] Simeng Sun, Y. Liu, Shuo Wang, Chenguang Zhu, and Mohit Iyyer. Pearl: Prompting large language models to
      plan and execute actions over long documents. Conference of the European Chapter of the Association for Computational
      Linguistics, 2023.
[362] Lutfi Eren Erdogan, Nicholas Lee, Sehoon Kim, Suhong Moon, Hiroki Furuta, G. Anumanchipalli, Kurt Keutzer, and
      Amir Gholami. Plan-and-act: Improving planning of agents for long-horizon tasks. arXiv preprint, 2025.
[363] Claudius Kienle, Benjamin Alt, O. Arenz, and Jan Peters. Learning hierarchical domain models through environment-
      grounded interaction, 2025. URL https://arxiv.org/abs/2505.13497v3.
[364] R. Janik. Aspects of human memory and large language models, 2023. URL https://arxiv.org/abs/2311.03839v3.
[365] Lianlei Shan, Shixian Luo, Zezhou Zhu, Yu Yuan, and Yong Wu. Cognitive memory in large language models, 2025.
      URL https://arxiv.org/abs/2504.02441v2.
[366] Venkatesh Balavadhani Parthasarathy, Ahtsham Zafar, Aafaq Khan, and Arsalan Shahid. The ultimate guide to
      fine-tuning llms from basics to breakthroughs: An exhaustive review of technologies, research, best practices, applied
      research challenges and opportunities. arXiv preprint arXiv:2408.13296, 2024.
[367] Jing Ren and Feng Xia. Brain-inspired artificial intelligence: A comprehensive review, 2024. URL https://arxiv.org/
      abs/2408.14811v1.
[368] Qinghua Lu, Liming Zhu, Xiwei Xu, Zhenchang Xing, Stefan Harrer, and Jon Whittle. Towards responsible generative
      ai: A reference architecture for designing foundation model based agents. 2024 IEEE 21st International Conference on
      Software Architecture Companion (ICSA-C), 2023.
[369] Jian Xie, Kai Zhang, Jiangjie Chen, Tinghui Zhu, Renze Lou, Yuandong Tian, Yanghua Xiao, and Yu Su. Travelplanner:
      A benchmark for real-world planning with language agents. International Conference on Machine Learning, 2024.
[370] Zhuosheng Zhang, Yao Yao, Aston Zhang, Xiangru Tang, Xinbei Ma, Zhiwei He, Yiming Wang, Mark B. Gerstein, Rui
      Wang, Gongshen Liu, and Hai Zhao. Igniting language intelligence: The hitchhiker’s guide from chain-of-thought
      reasoning to language agents. ACM Computing Surveys, 2023.
[371] Zihong He, Weizhe Lin, Hao Zheng, Fan Zhang, Matt Jones, Laurence Aitchison, Xuhai Xu, Miao Liu, P. O.
      Kristensson, and Junxiao Shen. Human-inspired perspectives: A survey on ai long-term memory, 2024. URL
      https://arxiv.org/abs/2411.00489v2.
[372] Yaxiong Wu, Sheng Liang, Chen Zhang, Yichao Wang, Yongyue Zhang, Huifeng Guo, Ruiming Tang, and Yong
      Liu. From human memory to ai memory: A survey on memory mechanisms in the era of llms, 2025. URL
      https://arxiv.org/abs/2504.15965v2.
[373] Shanshan Han, Qifan Zhang, Yuhang Yao, Weizhao Jin, Zhaozhuo Xu, and Chaoyang He. Llm multi-agent systems:
      Challenges and open problems, 2024. URL https://arxiv.org/abs/2402.03578v2.
[374] Christian Schröder de Witt. Open challenges in multi-agent security: Towards secure systems of interacting ai agents,
      2025. URL https://arxiv.org/abs/2505.02077v1.



                                                            60
                                A Survey of Vibe Coding with Large Language Models



[375] Anna Madison, Ellen R. Novoseller, Vinicius G. Goecks, Benjamin T. Files, Nicholas R. Waytowich, Alfred Yu, Vernon J.
      Lawhern, Steven Thurman, Christopher Kelshaw, and Kaleb McDowell. Scalable interactive machine learning for
      future command and control. 2024 International Conference on Military Communication and Information Systems (ICMCIS),
      2024.
[376] Haoran Wang, Zhenyu Hou, Yao Wei, Jie Tang, and Yuxiao Dong. Swe-dev: Building software engineering agents
      with training and inference scaling. arXiv preprint arXiv:2506.07636, 2025.
[377] Zhilong Chen, Chengzong Zhao, Boyuan Chen, Dayi Lin, Yihao Chen, Arthur Leung, Gopi Krishnan Rajbahadur,
      Gustavo A Oliva, Haoxiang Zhang, Aaditya Bhatia, et al. Repoforge: Training a sota fast-thinking swe agent with an
      end-to-end data curation pipeline synergizing sft and rl at scale. arXiv preprint arXiv:2508.01550, 2025.
[378] Yuanzhe Liu, Ryan Deng, Tim Kaler, Xuhao Chen, Charles E Leiserson, Yao Ma, and Jie Chen. Lessons learned: A
      multi-agent framework for code llms to learn and improve. arXiv preprint arXiv:2505.23946, 2025.
[379] Chaoqian Ouyang, Ling Yue, Shimin Di, Libin Zheng, Linan Yue, Shaowu Pan, Jian Yin, and Min-Ling Zhang.
      Code2mcp: Transforming code repositories into mcp services, 2025. URL https://arxiv.org/abs/2509.05941v2.
[380] Yilei Jiang, Yaozhi Zheng, Yuxuan Wan, Jiaming Han, Qunzhong Wang, Michael R Lyu, and Xiangyu Yue. Screencoder:
      Advancing visual-to-code generation for front-end automation via modular multimodal agents. arXiv preprint
      arXiv:2507.22827, 2025.
[381] Xinxing Ren, Qianbo Zang, and Zekun Guo. Simugen: Multi-modal agentic framework for constructing block
      diagram-based simulation models. arXiv preprint arXiv:2506.15695, 2025.
[382] Chi Zhang, Zhao Yang, Jiaxuan Liu, Yanda Li, Yucheng Han, Xin Chen, Zebiao Huang, Bin Fu, and Gang Yu.
      Appagent: Multimodal agents as smartphone users. In Proceedings of the 2025 CHI Conference on Human Factors in
      Computing Systems, pages 1–20, 2025.
[383] Cursor. https://cursor.com, 2025.
[384] Claude Code. https://www.anthropic.com/claude-code, 2025.
[385] Gemini Code CLI. https://github.com/google-gemini/gemini-cli, 2025.
[386] Qwen Coder. https://github.com/QwenLM/Qwen-Coder, 2025.
[387] Codex. https://openai.com/codex/, 2025.
[388] Zidi Xiong, Yuping Lin, Wenya Xie, Pengfei He, Jiliang Tang, Himabindu Lakkaraju, and Zhen Xiang. How memory
      management impacts llm agents: An empirical study of experience-following behavior. arXiv preprint arXiv:2505.16067,
      2025.
[389] Yiming Du, Wenyu Huang, Danna Zheng, Zhaowei Wang, Sébastien Montella, Mirella Lapata, Kam-Fai Wong,
      and Jeff Z. Pan. Rethinking memory in ai: Taxonomy, operations, topics, and future directions, 2025. URL https:
      //arxiv.org/abs/2505.00675v2.
[390] Yuki Hou, Haruki Tamoto, and Homei Miyashita. " my agent understands me better": Integrating dynamic human-like
      memory recall and consolidation in llm-based agents. In Extended Abstracts of the CHI Conference on Human Factors in
      Computing Systems, pages 1–7, 2024.
[391] Sanghwan Bae, Donghyun Kwak, Soyoung Kang, Min Young Lee, Sungdong Kim, Yuin Jeong, Hyeri Kim, Sang-Woo
      Lee, W. Park, and Nako Sung. Keep me updated! memory management in long-term conversations. Conference on
      Empirical Methods in Natural Language Processing, 2022.
[392] Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. Mem0: Building production-ready ai
      agents with scalable long-term memory. arXiv preprint arXiv:2504.19413, 2025.
[393] Yi Zhan, Qi Liu, Weibo Gao, Zheng Zhang, Tianfu Wang, Shuanghong Shen, Junyu Lu, and Zhenya Huang. Coderagent:
      Simulating student behavior for personalized programming learning with large language models. International Joint
      Conference on Artificial Intelligence, 2025.
[394] Elias Lumer, Anmol Gulati, V. K. Subbiah, Pradeep Honaganahalli Basavaraju, and James A. Burke. Memtool:
      Optimizing short-term memory management for dynamic tool calling in llm agent multi-turn conversations, 2025.
      URL https://arxiv.org/abs/2507.21428v1.
[395] Patrick Lewis, Ethan Perez, Aleksandara Piktus, F. Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuttler,
      M. Lewis, Wen tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. Retrieval-augmented generation for
      knowledge-intensive nlp tasks. Neural Information Processing Systems, 2020.




                                                           61
                                 A Survey of Vibe Coding with Large Language Models



[396] Brandon Kynoch, Hugo Latapie, and Dwane van der Sluis. Recallm: An adaptable memory mechanism with temporal
      understanding for large language models, 2023. URL https://arxiv.org/abs/2307.02738v3.
[397] Yuhuai Wu, M. Rabe, DeLesley S. Hutchins, and Christian Szegedy. Memorizing transformers. International Conference
      on Learning Representations, 2022.
[398] Yue Xing, Tao Yang, Yijiashun Qi, Minggu Wei, Yu Cheng, and Honghui Xin. Structured memory mechanisms for
      stable context representation in large language models, 2025. URL https://arxiv.org/abs/2505.22921v1.
[399] Yuanzhe Hu, Yu Wang, and Julian McAuley. Evaluating memory in llm agents via incremental multi-turn interactions,
      2025. URL https://arxiv.org/abs/2507.05257v2.
[400] Na Liu, Liangyu Chen, Xiaoyu Tian, Wei Zou, Kaijiang Chen, and Ming Cui. From llm to conversational agent: A
      memory enhanced architecture with fine-tuning of large language models. arXiv preprint arXiv:2401.02777, 2024.
[401] Bowen Cao, Deng Cai, and Wai Lam. Infiniteicl: Breaking the limit of context window size via long short-term
      memory transformation. arXiv preprint arXiv:2504.01707, 2025.
[402] Saurav Pawar, S. Tonmoy, S. M. M. Zaman, Vinija Jain, Aman Chadha, and Amitava Das. The what, why, and how
      of context length extension techniques in large language models - a detailed survey. arXiv preprint, 2024.
[403] Zhuocheng Shen. Llm with tools: A survey, 2024. URL https://arxiv.org/abs/2409.18807v1.
[404] Yujia Qin, Shengding Hu, Yankai Lin, Weize Chen, Ning Ding, Ganqu Cui, Zheni Zeng, Yufei Huang, Chaojun Xiao,
      Chi Han, Y. Fung, Yusheng Su, Huadong Wang, Cheng Qian, Runchu Tian, Kunlun Zhu, Shi Liang, Xingyu Shen,
      Bokai Xu, Zhen Zhang, Yining Ye, Bowen Li, Ziwei Tang, Jing Yi, Yu Zhu, Zhenning Dai, Lan Yan, Xin Cong, Ya-Ting
      Lu, Weilin Zhao, Yuxiang Huang, Junxi Yan, Xu Han, Xian Sun, Dahai Li, Jason Phang, Cheng Yang, Tongshuang Wu,
      Heng Ji, Zhiyuan Liu, and Maosong Sun. Tool learning with foundation models. ACM Computing Surveys, 2023.
[405] Prerna Agarwal, Himanshu Gupta, Soujanya Soni, Rohith Vallam, Renuka Sindhgatta, and Sameep Mehta. Automated
      creation and enrichment framework for improved invocation of enterprise apis as tools. arXiv preprint arXiv:2509.11626,
      2025.
[406] Meriem Mastouri, Emna Ksontini, and Wael Kessentini. Making rest apis agent-ready: From openapi to model context
      protocol servers for tool-augmented llms. arXiv preprint arXiv:2507.16044, 2025.
[407] Joykirat Singh, Raghav Magazine, Yash Pandya, and Akshay Nambi. Agentic reasoning and tool integration for llms
      via reinforcement learning. arXiv preprint arXiv:2505.01441, 2025.
[408] Copilot. https://copilot.microsoft.com/, 2023.
[409] Windsurf. https://windsurf.com/, 2025.
[410] Tabnine. https://www.tabnine.com/, 2025.
[411] Codewhisperer. https://workshops.aws/categories/CodeWhisperer, 2025.
[412] v0 by vercel. https://v0.app/, 2025.
[413] Replit. https://replit.com/, 2025.
[414] bolt. https://bolt.new/, 2025.
[415] Gemini cli. https://github.com/google-gemini/gemini-cli, 2025.
[416] Qwen code. https://github.com/QwenLM/qwen-code, 2025.
[417] Aider. https://aider.chat/, 2025.
[418] Cline. https://cline.bot/, 2025.
[419] Ranjan Sapkota, Konstantinos I. Roumeliotis, and Manoj Karkee. Ai agents vs. agentic ai: A conceptual taxonomy,
      applications and challenges. Information Fusion, 2025.
[420] Bingxi Zhao, Lin Geng Foo, Ping Hu, Christian Theobalt, Hossein Rahmani, and Jun Liu. Llm-based agentic reasoning
      frameworks: A survey from methods to scenarios. arXiv preprint arXiv:2508.17692, 2025.
[421] Cunxi Yu, Rongjian Liang, Chia-Tung Ho, and Haoxing Ren. Autonomous code evolution meets np-completeness.
      arXiv preprint arXiv:2509.07367, 2025.
[422] Zixuan Li, Yutao Zeng, Yuxin Zuo, Weicheng Ren, Wenxuan Liu, Miao Su, Yucan Guo, Yantao Liu, Xiang Li, Zhilei
      Hu, et al. Knowcoder: Coding structured knowledge into llms for universal information extraction. arXiv preprint
      arXiv:2403.07969, 2024.


                                                            62
                                 A Survey of Vibe Coding with Large Language Models



[423] Yuxin Zuo, Wenxuan Jiang, Wenxuan Liu, Zixuan Li, Long Bai, Hanbin Wang, Yutao Zeng, Xiaolong Jin, Jiafeng Guo,
      and Xueqi Cheng. Knowcoder-x: Boosting multilingual information extraction via code. arXiv preprint arXiv:2411.04794,
      2024.
[424] Zixuan Li, Wenxuan Liu, Long Bai, Chunmao Zhang, Wei Li, Fenghui Zhang, Quanxin Jin, Ruoyun He, Zhuo Chen,
      Zhilei Hu, et al. Knowcoder-v2: Deep knowledge analysis. arXiv preprint arXiv:2506.06881, 2025.
[425] Anastasiia Grishina, Vadim Liventsev, Aki Härmä, and Leon Moonen. Fully autonomous programming using iterative
      multi-agent debugging with large language models. ACM Transactions on Evolutionary Learning and Optimization, 2025.
[426] Amr Almorsi, Mohanned Ahmed, and Walid Gomaa. Guided code generation with llms: A multi-agent framework
      for complex code tasks. 2024 12th International Japan-Africa Conference on Electronics, Communications, and Computations
      (JAC-ECC), 2024.
[427] Ngoc Phuoc An Vo, B. Paulovicks, and V. Sheinin. Llm-as-a-judge for reference-less automatic code validation and
      refinement for natural language to bash in it automation. arXiv preprint, 2025.
[428] Xiancai Chen, Zhengwei Tao, Kechi Zhang, Changzhi Zhou, Wanli Gu, Yuanpeng He, Mengdi Zhang, Xunliang
      Cai, Haiyan Zhao, and Zhi Jin. Revisit self-debugging with self-generated tests for code generation. arXiv preprint
      arXiv:2501.12793, 2025.
[429] Lily Zhong, Zilong Wang, and Jingbo Shang. Ldb: A large language model debugger via verifying runtime execution
      step-by-step. arXiv preprint arXiv:2402.16906, 2024.
[430] Sabaat Haroon, Ahmad Faraz Khan, Ahmad Humayun, Waris Gill, Abdul Haddi Amjad, A. R. Butt, Mohammad Taha
      Khan, and Muhammad Ali Gulzar. How accurately do large language models understand code?, 2025. URL
      https://arxiv.org/abs/2504.04372v2.
[431] Yacine Majdoub and Eya Ben Charrada. Debugging with open-source large language models: An evaluation.
      International Symposium on Empirical Software Engineering and Measurement, 2024.
[432] Francisco Ribeiro. Large language models for automated program repair. SPLASH Companion, 2023.
[433] Anjana Sarkar and Soumyendu Sarkar. Survey of llm agent communication with mcp: A software design pattern
      centric review, 2025. URL https://arxiv.org/abs/2506.05364v1.
[434] Yilun Du, Shuang Li, Antonio Torralba, Joshua B Tenenbaum, and Igor Mordatch. Improving factuality and reasoning
      in language models through multiagent debate. In Forty-first International Conference on Machine Learning, 2023.
[435] Tian Liang, Zhiwei He, Wenxiang Jiao, Xing Wang, Yan Wang, Rui Wang, Yujiu Yang, Shuming Shi, and Zhaopeng Tu.
      Encouraging divergent thinking in large language models through multi-agent debate. arXiv preprint arXiv:2305.19118,
      2023.
[436] D. Ha, Phu. Trac Kien, Tho Quan, and Anh Nguyen-Duc. Evaluating classical software process models as coordination
      mechanisms for llm-based software generation, 2025. URL https://arxiv.org/abs/2509.13942v1.
[437] Jack Bell, Luigi Quarantiello, Eric Nuertey Coleman, Lanpei Li, Malio Li, Mauro Madeddu, Elia Piccoli, and Vincenzo
      Lomonaco. The future of continual learning in the era of foundation models: Three key directions, 2025. URL
      https://arxiv.org/abs/2506.03320v1.
[438] Chen Gao, Xiaochong Lan, Nian Li, Yuan Yuan, Jingtao Ding, Zhilun Zhou, Fengli Xu, and Yong Li. Large language
      models empowered agent-based modeling and simulation: A survey and perspectives. Humanities and Social Sciences
      Communications, 2023.
[439] Xinyi Mou, Xuanwen Ding, Qi He, Liang Wang, Jingcong Liang, Xinnong Zhang, Libo Sun, Jiayu Lin, Jie Zhou,
      Xuanjing Huang, and Zhongyu Wei. From individual to society: A survey on social simulation driven by large
      language model-based agents, 2024. URL https://arxiv.org/abs/2412.03563v1.
[440] Manuela Vanegas Ferro, Allen Lee, C. Pritchard, C. Barton, and M. Janssen. Containerization for creating reusable
      model code. Socio-Environmental Systems Modelling, 2022.
[441] Sari Sultan, Imtiaz Ahmad, and T. Dimitriou. Container security: Issues, challenges, and the road ahead. IEEE Access,
      2019.
[442] C. Pahl, Antonio Brogi, J. Soldani, and Pooyan Jamshidi. Cloud container technologies: A state-of-the-art review. IEEE
      Transactions on Cloud Computing, 2019.
[443] Sergei Romanov, Abel Soares Siqueira, J. D. Bruin, J. Teijema, Laura Hofstee, and R. Schoot. Optimizing asreview
      simulations: A generic multiprocessing solution for ‘light-data’ and ‘heavy-data’ users. Data Intelligence, 2024.




                                                             63
                                  A Survey of Vibe Coding with Large Language Models



[444] Marcelo Amaral, Jordà Polo, David Carrera, Iqbal Mohomed, Merve Unuvar, and M. Steinder. Performance evaluation
      of microservices architectures using containers. IEEE International Symposium on Network Computing and Applications,
      2015.
[445] Roberto Morabito. Virtualization on internet of things edge devices with container technologies: A performance
      evaluation. IEEE Access, 2017.
[446] C. Pahl and Brian Lee. Containers and clusters for edge cloud architectures – a technology review. International
      Conference on Future Internet of Things and Cloud, 2015.
[447] Richard H. Moulton, Gary A. McCully, and John D. Hastings. Confronting the reproducibility crisis: A case study of
      challenges in cybersecurity ai. Computer Assisted Radiology and Surgery - International Congress and Exhibition, 2024.
[448] C. Boettiger. An introduction to docker for reproducible research. OPSR, 2014.
[449] Sarishma and Abhishek. A systematic review of the impact of containerization on software development and
      deployment practices. Computology: Journal of Applied Computer Science and Intelligent Technologies, 2021.
[450] L. Baresi, G. Quattrocchi, and N. Rasi. A qualitative and quantitative analysis of container engines. Journal of Systems
      and Software, 2023.
[451] Loïc Miller, Pascal M’erindol, A. Gallais, and C. Pelsser. Towards secure and leak-free workflows using microservice
      isolation. International Conference on High Performance Switching and Routing, 2020.
[452] Sunil Kumar Jang Bahadur and Gopala Dhar. Securing generative ai agentic workflows: Risks, mitigation, and a
      proposed firewall architecture, 2025. URL https://arxiv.org/abs/2506.17266v1.
[453] Md Omar Faruk Rokon, Risul Islam, Ahmad Darki, E. Papalexakis, and M. Faloutsos. Sourcefinder: Finding malware
      source-code from publicly available repositories. International Symposium on Recent Advances in Intrusion Detection, 2020.
[454] Jiawei Liu, Chun Xia, Yuyao Wang, and Lingming Zhang. Is your code generated by chatgpt really correct? rigorous
      evaluation of large language models for code generation. Neural Information Processing Systems, 2023.
[455] Mohammed Latif Siddiq and Joanna C. S. Santos. Sallm: Security assessment of generated code. 2024 39th IEEE/ACM
      International Conference on Automated Software Engineering Workshops (ASEW), 2023.
[456] Marco Abbadini, Dario Facchinetti, Gianluca Oldani, Matthew Rossi, and S. Paraboschi. Natisand: Native code
      sandboxing for javascript runtimes. International Symposium on Recent Advances in Intrusion Detection, 2023.
[457] Paul Kirth, Mitchel Dickerson, Stephen Crane, Per Larsen, Adrian Dabrowski, David Gens, Yeoul Na, Stijn Volckaert,
      and M. Franz. Pkru-safe: automatically locking down the heap between safe and unsafe languages. European Conference
      on Computer Systems, 2022.
[458] Konstantinos Kanellopoulos, Konstantinos Sgouras, F. N. Bostanci, A. Kakolyris, Berkin Kerim Konar, Rahul Bera,
      Mohammad Sadrosadati, Rakesh Kumar, Nandita Vijaykumar, and Onur Mutlu. Virtuoso: Enabling fast and accurate
      virtual memory research via an imitation-based operating system simulation methodology. International Conference on
      Architectural Support for Programming Languages and Operating Systems, 2024.
[459] Haoyu Wang, Christopher M. Poskitt, and Jun Sun. Agentspec: Customizable runtime enforcement for safe and
      reliable llm agents, 2025. URL https://arxiv.org/abs/2503.18666.
[460] T. Feilhauer and M. Sobotka. Def - a programming language agnostic framework and execution environment for the
      parallel execution of library routines. Journal of Cloud Computing, 2016.
[461] Saeid Abolfazli, Zohreh Sanaei, E. Ahmed, A. Gani, and R. Buyya. Cloud-based augmentation for mobile devices:
      Motivation, taxonomies, and open challenges. IEEE Communications Surveys and Tutorials, 2013.
[462] Sebastian Böhm and G. Wirtz. Cloud-edge orchestration for smart cities: A review of kubernetes-based orchestration
      architectures. EAI Endorsed Transactions on Smart Cities, 2022.
[463] Jacopo Tagliabue, Hugo Bowne-Anderson, Ville Tuulos, Savin Goyal, R. Cledat, and David Berg. Reasonable scale
      machine learning with open-source metaflow, 2023. URL https://arxiv.org/abs/2303.11761v1.
[464] Sanidhya Vijayvargiya, Aditya Bharat Soni, Xuhui Zhou, Z. Z. Wang, Nouha Dziri, Graham Neubig, and M. Sap.
      Openagentsafety: A comprehensive framework for evaluating real-world ai agent safety, 2025. URL https://arxiv.
      org/abs/2507.06134v1.
[465] Jingzhi Gong, Rafail Giavrimis, Paul Brookes, Vardan K. Voskanyan, Fan Wu, Mari Ashiga, Matthew Truscott, Mike
      Basios, Leslie Kanthan, Jie Xu, and Zheng Wang. Tuning llm-based code optimization via meta-prompting: An
      industrial perspective. arXiv preprint, 2025.



                                                             64
                                  A Survey of Vibe Coding with Large Language Models



[466] Siddhant Waghjale, Vishruth Veerendranath, Z. Z. Wang, and Daniel Fried. Ecco: Can we improve model-generated
      code efficiency without sacrificing functional correctness? Conference on Empirical Methods in Natural Language Processing,
      2024.
[467] Mohsen Seyedkazemi Ardebili and Andrea Bartolini. Kubeintellect: A modular llm-orchestrated agent framework for
      end-to-end kubernetes management, 2025. URL https://arxiv.org/abs/2509.02449v1.
[468] Agnia Sergeyuk, Ilya Zakharov, Ekaterina Koshchenko, and Maliheh Izadi. Human-ai experience in integrated
      development environments: A systematic literature review, 2025. URL https://arxiv.org/abs/2503.06195v2.
[469] Agnia Sergeyuk, Sergey Titov, and M. Izadi. In-ide human-ai experience in the era of large language models; a
      literature review. Ide, 2024.
[470] Priyan Vaithilingam, Elena L. Glassman, Peter Groenwegen, Sumit Gulwani, Austin Z. Henley, Rohan Malpani,
      David Pugh, Arjun Radhakrishna, Gustavo Soares, J. Wang, and Aaron Yim. Towards more effective ai-assisted
      programming: A systematic design exploration to improve visual studio intellicode’s user experience. 2023 IEEE/ACM
      45th International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP), 2023.
[471] Steven I Ross, Fernando Martinez, Stephanie Houde, Michael Muller, and Justin D Weisz. Programmer experiences
      with github copilot. In Proceedings of the 28th International Conference on Intelligent User Interfaces, pages 1–10, 2023.
[472] Thomas Weber, Maximilian Brandmaier, Albrecht Schmidt, and Sven Mayer. Significant productivity gains through
      programming with large language models. Proc. ACM Hum. Comput. Interact., 2024.
[473] Daye Nam, A. Macvean, Vincent J. Hellendoorn, Bogdan Vasilescu, and B. Myers. Using an llm to help with code
      understanding. International Conference on Software Engineering, 2023.
[474] GitHub. Using github codespaces. https://docs.github.com/en/codespaces, 2024. Accessed: 2025-10-05.
[475] JetBrains. Remote development in jetbrains ides now available for github codespaces users. https://blog.jetbrains.
      com/idea/2022/07/remote-development-for-github-codespaces, 2022. Accessed: 2025-10-05.
[476] Partha Pratim Ray. A survey on model context protocol: Architecture, state-of-the-art, challenges and future directions.
      Authorea Preprints, 2025.
[477] Gidon Ernst, Johannes Blau, and Toby Murray. Deductive verification via the debug adapter protocol. arXiv preprint
      arXiv:2108.02968, 2021.
[478] Antonio García-Domínguez and Dimitris Kolovos. Cross-ide remote debugging of model management programs
      through the debug adapter protocol. In Proceedings of the ACM/IEEE 27th International Conference on Model Driven
      Engineering Languages and Systems, pages 21–25, 2024.
[479] Qiaomu Li and Ying Xie. From glue-code to protocols: A critical analysis of a2a and mcp integration for scalable
      agent systems. arXiv preprint arXiv:2505.03864, 2025.
[480] GitKraken. Model context protocol for cli and ai ides. https://www.gitkraken.com/features/mcp-server?utm_source=
      chatgpt.com, 2025.
[481] Microsoft Visual Studio Blog. Agent mode is now generally available with mcp support. https://devblogs.microsoft.
      com/visualstudio/agent-mode-is-now-generally-available-with-mcp-support/?utm_source=chatgpt.com, 2025.
[482] James A Highsmith. Agile software development ecosystems, volume 13. Addison-Wesley Professional, 2002.
[483] Todor Ivanov and N. Valchanov. Extended model of code orchestration and deployment platform. TEM Journal, 2022.
[484] Haitian Chen and Ye Ding. Implementing traffic agent based on langgraph. In Fourth International Conference on
      Intelligent Traffic Systems and Smart City (ITSSC 2024), volume 13422, pages 582–587. SPIE, 2025.
[485] Waseem Nasir and Nikoletta Kallinteris. From code generation to ai collaboration: The role of multi-agent systems in
      software engineering, 2025.
[486] Haoxiang Luo, Yu Yan, Yanhui Bian, Wenjiao Feng, Ruichen Zhang, Yinqiu Liu, Jiacheng Wang, Gang Sun, Dusit
      Niyato, Hongfang Yu, et al. Ai reasoning for wireless communications and networking: A survey and perspectives.
      arXiv preprint arXiv:2509.09193, 2025.
[487] Laurie Hughes, Yogesh K Dwivedi, Tegwen Malik, Mazen Shawosh, Mousa Ahmed Albashrawi, Il Jeon, Vincent
      Dutot, Mandanna Appanderanda, Tom Crick, Rahul De’, et al. Ai agents and agentic systems: A multi-expert analysis.
      Journal of Computer Information Systems, pages 1–29, 2025.
[488] Hojae Han, Seung won Hwang, Rajhans Samdani, and Yuxiong He. Convcodeworld: Benchmarking conversational
      code generation in reproducible feedback environments. International Conference on Learning Representations, 2025.


                                                              65
                                  A Survey of Vibe Coding with Large Language Models



[489] Zhongyuan Peng, Yifan Yao, Kaijing Ma, Shuyue Guo, Yizhe Li, Yichi Zhang, Chenchen Zhang, Yifan Zhang, Zhouliang
      Yu, Luming Li, Minghao Liu, Yihang Xia, Jiawei Shen, Yuchen Wu, Yixin Cao, Zhaoxiang Zhang, Wenhao Huang,
      Jiaheng Liu, and Ge Zhang. Criticlean: Critic-guided reinforcement learning for mathematical formalization, 2025.
      URL https://arxiv.org/abs/2507.06181v1.
[490] Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. Repairagent: An autonomous, llm-based agent for program
      repair. arXiv preprint arXiv:2403.17134, 2024.
[491] Ravin Ravi, Dylan Bradshaw, Stefano Ruberto, Gunel Jahangirova, and Valerio Terragni. Llmloop: Improving
      llm-generated code and tests through automated iterative feedback loops. ICSME. IEEE, 2025.
[492] Dekun Dai, Mingwei Liu, Anji Li, Jialun Cao, Yanlin Wang, Chong Wang, Xing Peng, and Zibin Zheng. Feedbackeval:
      A benchmark for evaluating large language models in feedback-driven code repair tasks, 2025. URL https://arxiv.
      org/abs/2504.06939v1.
[493] Xinzhe Li. A review of prominent paradigms for llm-based agents: Tool use, planning (including rag), and feedback
      learning. International Conference on Computational Linguistics, 2024.
[494] Sergi Siso, W. Armour, and Jeyarajan Thiyagalingam. Evaluating auto-vectorizing compilers through objective
      withdrawal of useful information. ACM Transactions on Architecture and Code Optimization (TACO), 2019.
[495] Dejan Grubisic, Chris Cummins, Volker Seeker, and Hugh Leather. Compiler generated feedback for large language
      models, 2024. URL https://arxiv.org/abs/2403.14714v1.
[496] Seyed Moein Abtahi and Akramul Azim. Augmenting large language models with static code analysis for automated
      code quality improvements. In 2025 IEEE/ACM Second International Conference on AI Foundation Models and Software
      Engineering (Forge), pages 82–92. IEEE, 2025.
[497] Chongzhou Fang, Ning Miao, Shaurya Srivastav, Jialin Liu, Ruoyu Zhang, Ruijie Fang, Ryan Tsang, Najmeh Nazari,
      Han Wang, Houman Homayoun, et al. Large language models for code analysis: Do {LLMs} really do their job? In
      33rd USENIX Security Symposium (USENIX Security 24), pages 829–846, 2024.
[498] Guilhem Lacombe, D. Féliot, Etienne Boespflug, and Marie-Laure Potet. Combining static analysis and dynamic
      symbolic execution in a toolchain to detect fault injection vulnerabilities. Journal of Cryptographic Engineering, 2023.
[499] Ulligaddala Srinivasarao, Akhil Chaganti, Ajay Mannam, Dhanush Kotrikeline, and Hemanth Katta. Software bug
      report detection methods based on machine learning techniques. 2024 2nd International Conference on Advancement in
      Computation & Computer Technologies (InCACCT), 2024.
[500] Ziyang Li, Saikat Dutta, and Mayur Naik. Iris: Llm-assisted static analysis for detecting security vulnerabilities. arXiv
      preprint arXiv:2405.17238, 2024.
[501] Mete Keltek, Rong Hu, Mohammadreza Fani Sani, and Ziyue Li. Lsast: Enhancing cybersecurity through llm-supported
      static application security testing. In IFIP International Conference on ICT Systems Security and Privacy Protection, pages
      166–179. Springer, 2025.
[502] Nalin Wadhwa, Jui Pradhan, Atharv Sonwane, Surya Prakash Sahu, Nagarajan Natarajan, Aditya Kanade, Suresh
      Parthasarathy, and Sriram Rajamani. Core: Resolving code quality issues using llms. Proceedings of the ACM on
      Software Engineering, 1(FSE):789–811, 2024.
[503] Brett A. Becker. An effective approach to enhancing compiler error messages. Technical Symposium on Computer Science
      Education, 2016.
[504] Mohammad Mahdi Mohajer, Reem Aleithan, Nima Shiri Harzevili, Moshi Wei, Alvine Boaye Belle, Hung Viet
      Pham, and Song Wang. Skipanalyzer: A tool for static code analysis with large language models. arXiv preprint
      arXiv:2310.18532, 2023.
[505] Haoxin Tu, Zhide Zhou, He Jiang, Imam Nur Bani Yusuf, Yuxian Li, and Lingxiao Jiang. Isolating compiler bugs by
      generating effective witness programs with large language models. IEEE Transactions on Software Engineering, 2023.
[506] Josselin Feist, Gustavo Grieco, and Alex Groce. Slither: A static analysis framework for smart contracts. International
      Workshop on Emerging Trends in Software Engineering for Blockchain, 2019.
[507] Junze Hu, Xiangyu Jin, Yizhe Zeng, Yuling Liu, Yunpeng Li, Dan Du, Kaiyu Xie, and Hongsong Zhu. Qlpro:
      Automated code vulnerability discovery via llm and static code analysis integration. arXiv preprint arXiv:2506.23644,
      2025.
[508] Feng Yao, Zilong Wang, Liyuan Liu, Junxia Cui, Li Zhong, Xiaohan Fu, Haohui Mai, Vish Krishnan, Jianfeng Gao,
      and Jingbo Shang. Training language models to generate quality code with program analysis feedback, 2025. URL
      https://arxiv.org/abs/2505.22704v1.


                                                              66
                                 A Survey of Vibe Coding with Large Language Models



[509] Greta Dolcetti, Vincenzo Arceri, Eleonora Iotti, S. Maffeis, Agostino Cortesi, and E. Zaffanella. Helping llms improve
      code generation using feedback from testing and static analysis, 2024. URL https://arxiv.org/abs/2412.14841v2.
[510] Kaiyan Chang, Wenlong Zhu, Kun Wang, Xinyang He, Nan Yang, Zhirong Chen, Dantong Jin, Cangyuan Li, Yunhao
      Zhou, Hao Yan, Zhuoliang Zhao, Yuan Cheng, Mengdi Wang, Shengwen Liang, Yinhe Han, Xiaowei Li, Huawei Li,
      and Ying Wang. A data-centric chip design agent framework for verilog code generation. ACM Transactions on Design
      Automation of Electronic Systems, 2025.
[511] Farzaneh Rabiei Kashanaki, Mark Zakharov, and Jose Renau. Beyond verilog: Agents for emerging hdls. Coins, 2025.
[512] Leitian Tao, Xiang Chen, Tong Yu, Tung Mai, Ryan Rossi, Yixuan Li, and Saayan Mitra. Codelutra: Boosting llm code
      generation via preference-guided refinement. arXiv preprint arXiv:2411.05199, 2024.
[513] Hammond Pearce, Benjamin Tan, Baleegh Ahmad, Ramesh Karri, and Brendan Dolan-Gavitt. Examining zero-shot
      vulnerability repair with large language models. In 2023 IEEE Symposium on Security and Privacy (SP), pages 2339–2356.
      IEEE, 2023.
[514] Zhongchun Zheng, Kan Wu, Long Cheng, Lu Li, Rodrigo C. O. Rocha, Tianyi Liu, Wei Wei, Jianjiang Zeng, Xianwei
      Zhang, and Yaoqing Gao. Vectrans: Enhancing compiler auto-vectorization through llm-assisted code transformations,
      2025. URL https://arxiv.org/abs/2503.19449v3.
[515] Peter Pirkelbauer and Chunhua Liao. Compilergpt: Leveraging large language models for analyzing and acting on
      compiler optimization reports, 2025. URL https://arxiv.org/abs/2506.06227v2.
[516] Shou Li, Andrey Kan, Laurent Callot, Bhavana Bhasker, Muhammad Shihab Rashid, and Timothy B Esler. Redo:
      Execution-free runtime error detection for coding agents. arXiv preprint arXiv:2410.09117, 2024.
[517] Naman Jain, Jaskirat Singh, Manish Shetty, Liang Zheng, Koushik Sen, and Ion Stoica. R2e-gym: Procedural
      environments and hybrid verifiers for scaling open-weights swe agents. arXiv preprint arXiv:2504.07164, 2025.
[518] Michael Luo, Naman Jain, Jaskirat Singh, Sijun Tan, Ameen Patel, Qingyang Wu, Alpay Ariyak, Colin Cai, Shang Zhu
      Tarun Venkat, Ben Athiwaratkun, Manan Roongta, Ce Zhang, Li Erran Li, Raluca Ada Popa, Koushik Sen, and Ion Stoica.
      Deepswe: Training a state-of-the-art coding agent from scratch by scaling rl. https://pretty-radio-b75.notion.site/
      DeepSWE-Training-a-Fully-Open-sourced-State-of-the-Art-Coding-Agent-by-Scaling-RL-22281902c1468193aabbe9a8c59bbe33,
      2025. Notion Blog.
[519] Ibragim Badertdinov, Alexander Golubev, Maksim Nekrashevich, Anton Shevtsov, Simon Karasik, Andrei An-
      driushchenko, Maria Trofimova, Daria Litvintseva, and Boris Yangel. Swe-rebench: An automated pipeline for task
      collection and decontaminated evaluation of software engineering agents. arXiv preprint arXiv:2505.20411, 2025.
[520] Alexander Golubev, Maria Trofimova, Sergei Polezhaev, Ibragim Badertdinov, Maksim Nekrashevich, Anton Shevtsov,
      Simon Karasik, Sergey Abramov, Andrei Andriushchenko, Filipp Fisin, et al. Training long-context, multi-turn software
      engineering agents with reinforcement learning. arXiv preprint arXiv:2508.03501, 2025.
[521] Hyungjoo Chae, Taeyoon Kwon, Seungjun Moon, Yongho Song, Dongjin Kang, Kai Tzu-iunn Ong, Beong-woo Kwak,
      Seonghyeon Bae, Seung-won Hwang, and Jinyoung Yeo. Coffee-gym: An environment for evaluating and improving
      natural language feedback on erroneous code. arXiv preprint arXiv:2409.19715, 2024.
[522] Jia Li, Ge Li, Xuanming Zhang, Yihong Dong, and Zhi Jin. Evocodebench: An evolving code generation benchmark
      aligned with real-world code repositories. arXiv preprint arXiv:2404.00599, 2024.
[523] Yiming Huang, Jianwen Luo, Yan Yu, Yitong Zhang, Fangyu Lei, Yifan Wei, Shizhu He, Lifu Huang, Xiao Liu, Jun
      Zhao, et al. Da-code: Agent data science code generation benchmark for large language models. arXiv preprint
      arXiv:2410.07331, 2024.
[524] Yuhang Lai, Chengxi Li, Yiming Wang, Tianyi Zhang, Ruiqi Zhong, Luke Zettlemoyer, Wen-tau Yih, Daniel Fried,
      Sida Wang, and Tao Yu. Ds-1000: A natural and reliable benchmark for data science code generation. In International
      Conference on Machine Learning, pages 18319–18345. PMLR, 2023.
[525] Xiangru Tang, Bill Qian, Rick Gao, Jiakang Chen, Xinyun Chen, and Mark B Gerstein. Biocoder: a benchmark for
      bioinformatics code generation with large language models. Bioinformatics, 40(Supplement_1):i266–i276, 2024.
[526] Rushi Qiang, Yuchen Zhuang, Yinghao Li, Rongzhi Zhang, Changhao Li, Ian Shu-Hei Wong, Sherry Yang, Percy
      Liang, Chao Zhang, Bo Dai, et al. Mle-dojo: Interactive environments for empowering llm agents in machine learning
      engineering. arXiv preprint arXiv:2505.07782, 2025.
[527] Yangtian Zi, Zixuan Wu, Aleksander Boruch-Gruszecki, Jonathan Bell, and Arjun Guha. Agentpack: A dataset of
      code changes, co-authored by agents and humans. arXiv preprint arXiv:2509.21891, 2025.




                                                            67
                                  A Survey of Vibe Coding with Large Language Models



[528] Lin Yang, Chen Yang, Shutao Gao, Weijing Wang, Bo Wang, Qihao Zhu, Xiao Chu, Jianyi Zhou, Guangtai Liang,
      Qianxiang Wang, et al. On the evaluation of large language models in unit test generation. In Proceedings of the 39th
      IEEE/ACM International Conference on Automated Software Engineering, pages 1607–1619, 2024.
[529] Kent Beck. Test-driven development: by example. Addison-Wesley Professional, 2003.
[530] Yi Cui. Tests as prompt: A test-driven-development benchmark for llm code generation. arXiv preprint arXiv:2505.09027,
      2025.
[531] Siqi Gu, Quanjun Zhang, Kecheng Li, Chunrong Fang, Fangyuan Tian, Liuchuan Zhu, Jianyi Zhou, and Zhenyu Chen.
      Testart: Improving llm-based unit testing via co-evolution of automated generation and repair iteration. arXiv preprint
      arXiv:2408.03095, 2024.
[532] Akilesh S, Rajeev Sekar, Om Kumar C U, Prakalya D, and Suguna M. Multi-agent hierarchical workflow for
      autonomous code generation with large language models. 2025 IEEE International Students’ Conference on Electrical,
      Electronics and Computer Science (SCEECS), 2025.
[533] Yu Nong, Haoran Yang, Long Cheng, Hongxin Hu, and Haipeng Cai. Automated software vulnerability patching
      using large language models. arXiv e-prints, pages arXiv–2408, 2024.
[534] Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran Kazemi, Aviral Kumar, and Rishabh Agarwal. Generative
      verifiers: Reward modeling as next-token prediction. arXiv preprint arXiv:2408.15240, 2024.
[535] Tianyi Zhang, Tao Yu, Tatsunori Hashimoto, Mike Lewis, Wen-tau Yih, Daniel Fried, and Sida Wang. Coder reviewer
      reranking for code generation. In International Conference on Machine Learning, pages 41832–41846. PMLR, 2023.
[536] Harsh R. Darji and Thibaud Lutellier. Curiosity by design: An llm-based coding assistant asking clarification questions,
      2025. URL https://arxiv.org/abs/2507.21285v1.
[537] P. Christiano, Jan Leike, Tom B. Brown, Miljan Martic, S. Legg, and Dario Amodei. Deep reinforcement learning from
      human preferences. Neural Information Processing Systems, 2017.
[538] Harrison Lee, Samrat Phatale, Hassan Mansoor, Thomas Mesnard, Johan Ferret, Kellie Lu, Colton Bishop, Ethan Hall,
      Victor Carbune, Abhinav Rastogi, et al. Rlaif vs. rlhf: Scaling reinforcement learning from human feedback with ai
      feedback. arXiv preprint arXiv:2309.00267, 2023.
[539] Junhao Yin, Haolin Wang, Peng Bao, Ju Xu, and Yongliang Wang. From clicks to preference: A multi-stage alignment
      framework for generative query suggestion in conversational system, 2025. URL https://arxiv.org/abs/2508.15811v1.
[540] Andreas Kopf, Yannic Kilcher, Dimitri von Rutte, Sotiris Anagnostidis, Zhi Rui Tam, K. Stevens, Abdullah Barhoum,
      Nguyen Minh Duc, Oliver Stanley, Rich’ard Nagyfi, ES Shahul, Sameer Suri, David Glushkov, A. Dantuluri, Andrew
      Maguire, Christoph Schuhmann, Huu Nguyen, and A. Mattick. Openassistant conversations - democratizing large
      language model alignment. Neural Information Processing Systems, 2023.
[541] Feifan Song, Bowen Yu, Minghao Li, Haiyang Yu, Fei Huang, Yongbin Li, and Houfeng Wang. Preference ranking
      optimization for human alignment. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pages
      18990–18998, 2024.
[542] Rémi Munos, Michal Valko, Daniele Calandriello, Mohammad Gheshlaghi Azar, Mark Rowland, Zhaohan Daniel Guo,
      Yunhao Tang, Matthieu Geist, Thomas Mesnard, Andrea Michi, et al. Nash learning from human feedback. arXiv
      preprint arXiv:2312.00886, 18, 2023.
[543] Benjue Weng. Navigating the landscape of large language models: A comprehensive review and analysis of paradigms
      and fine-tuning strategies, 2024. URL https://arxiv.org/abs/2404.09022v1.
[544] Bram Wallace, Meihua Dang, Rafael Rafailov, Linqi Zhou, Aaron Lou, Senthil Purushwalkam, Stefano Ermon, Caiming
      Xiong, Shafiq R. Joty, and Nikhil Naik. Diffusion model alignment using direct preference optimization. Computer
      Vision and Pattern Recognition, 2023.
[545] Yancheng He, Shilong Li, Jiaheng Liu, Weixun Wang, Xingyuan Bu, Ge Zhang, Zhongyuan Peng, Zhaoxiang Zhang,
      Zhicheng Zheng, Wenbo Su, et al. Can large language models detect errors in long chain-of-thought reasoning? arXiv
      preprint arXiv:2502.19361, 2025.
[546] Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han, and Rui Zhang. When can llms actually correct their own
      mistakes? a critical survey of self-correction of llms. Transactions of the Association for Computational Linguistics, 2024.
[547] Kaiyan Chang, Songcheng Xu, Chenglong Wang, Yingfeng Luo, Tong Xiao, and Jingbo Zhu. Efficient prompting
      methods for large language models: A survey, 2024. URL https://arxiv.org/abs/2404.01077v2.




                                                               68
                                 A Survey of Vibe Coding with Large Language Models



[548] Firuz Kamalov, D. S. Calonge, Linda Smail, Dilshod Azizov, D. Thadani, Theresa Kwong, and Amara Atif. Evolution
      of ai in education: Agentic workflows, 2025. URL https://arxiv.org/abs/2504.20082v1.
[549] Jiaheng Liu, Zehao Ni, Haoran Que, Tao Sun, Zekun Wang, Jian Yang, Jiakai Wang, Hongcheng Guo, Zhongyuan
      Peng, Ge Zhang, et al. Roleagent: Building, interacting, and benchmarking high-quality role-playing agents from
      scripts. Advances in Neural Information Processing Systems, 37:49403–49428, 2024.
[550] Liangming Pan, Michael Stephen Saxon, Wenda Xu, Deepak Nathani, Xinyi Wang, and William Yang Wang. Auto-
      matically correcting large language models: Surveying the landscape of diverse self-correction strategies, 2023. URL
      https://arxiv.org/abs/2308.03188v2.
[551] Winston W Royce. Managing the development of large software systems: concepts and techniques. In Proceedings of
      the 9th international conference on Software Engineering, pages 328–338, 1987.
[552] Agile Manifesto. Manifesto for agile software development, 2001.
[553] James Martin. Rapid application development. Macmillan Publishing Co., Inc., 1991.
[554] Paul Beynon-Davies, Chris Carne, Hugh Mackay, and Douglas Tudhope. Rapid application development (rad): an
      empirical review. European Journal of Information Systems, 8(3):211–223, 1999.
[555] Laurie Williams, Robert R Kessler, Ward Cunningham, and Ron Jeffries. Strengthening the case for pair programming.
      IEEE software, 17(4):19–25, 2000.
[556] Andrew Begel and Nachiappan Nagappan. Pair programming: what’s in it for me? In Proceedings of the Second
      ACM-IEEE international symposium on Empirical software engineering and measurement, pages 120–128, 2008.
[557] Jo E Hannay, Tore Dybå, Erik Arisholm, and Dag IK Sjøberg. The effectiveness of pair programming: A meta-analysis.
      Information and software technology, 51(7):1110–1122, 2009.
[558] Tanja Bipp, Andreas Lepper, and Doris Schmedding. Pair programming in software development teams–an empirical
      study of its benefits. Information and Software Technology, 50(3):231–240, 2008.
[559] Denae Ford, Margaret-Anne Storey, Alexey Zagalsky, and Daniel M. German. A tale of two cities: Software developers
      working from home during the covid-19 pandemic. ACM Transactions on Software Engineering and Methodology (TOSEM),
      29(4):1–28, 2020.
[560] Advait Sarkar and Ian Drosos. Vibe coding: programming through conversation with artificial intelligence. Journal of
      Software Engineering Research and Development, 3(1):1–20, 2025.
[561] Cory Hymel. The ai-native software development lifecycle: A theoretical and practical new methodology. arXiv
      preprint arXiv:2408.03416, 2024.
[562] Kaixin Wang, Tianlin Li, Xiaoyu Zhang, Chong Wang, Weisong Sun, Yang Liu, and Bin Shi. Software development life
      cycle perspective: A survey of benchmarks for code large language models and agents. arXiv preprint arXiv:2505.05283,
      2025.
[563] Rasmus Ulfsnes, Nils Brede Moe, Viktoria Stray, and Marianne Skarpen. Transforming software development with
      generative ai: Empirical insights on collaboration and workflow. In Generative AI for effective software development,
      pages 219–234. Springer, 2024.
[564] Nan Chen, Luna K. Qiu, Arran Zeyu Wang, Zilong Wang, and Yuqing Yang. Screen reader programmers in the vibe
      coding era: Adaptation, empowerment, and new accessibility landscape, 2025. URL https://arxiv.org/abs/2506.
      13270.
[565] Daniel Russo. Navigating the complexity of generative ai adoption in software engineering. ACM Transactions on
      Software Engineering and Methodology, 33(5):1–50, 2024.
[566] Kasra Ferdowsi, Ruanqianqian Huang, Michael B James, Nadia Polikarpova, and Sorin Lerner. Validating ai-generated
      code with live programming. In Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems, pages
      1–8, 2024.
[567] Vahid Garousi, Nithin Joy, Zafar Jafarov, Alper Buğra Keleş, Sevde Değirmenci, Ece Özdemir, and Ryan Zarringhalami.
      Ai-powered software testing tools: A systematic review and empirical assessment of their features and limitations.
      arXiv preprint arXiv:2409.00411, 2024.
[568] Simon Torka and Sahin Albayrak. Optimizing ai-assisted code generation. arXiv preprint arXiv:2412.10953, 2024.
[569] Priyan Vaithilingam, Tianyi Zhang, and Elena L Glassman. Expectation vs. experience: Evaluating the usability of
      code generation tools powered by large language models. In Chi conference on human factors in computing systems
      extended abstracts, pages 1–7, 2022.


                                                            69
                                 A Survey of Vibe Coding with Large Language Models



[570] Yuji Dong. An Open Resource-Oriented Architecture for Decentralized Cyber Physical Systems. The University of Liverpool
      (United Kingdom), 2018.
[571] Przemyslaw Pospieszny, Beata Czarnacka-Chrobot, and Andrzej Kobylinski. An effective approach for software project
      effort and duration estimation with machine learning algorithms. Journal of Systems and Software, 137:184–196, 2018.
[572] Peter C. Rigby and Christian Bird. Convergent contemporary software peer review practices. In Proceedings of the
      2013 9th Joint Meeting on Foundations of Software Engineering, pages 712–721, 2013.
[573] A. Ackerman, Lynne S. Buchwald, and Frank H. Lewski. Software inspections: an effective verification process. IEEE
      Software, 6(3):31–36, 1989.
[574] Kexin Sun, Hongyu Kuang, Sebastian Baltes, Xin Zhou, He Zhang, Xiaoxing Ma, Guoping Rong, Dong Shao, and
      Christoph Treude. Does ai code review lead to code changes? a case study of github actions. arXiv preprint
      arXiv:2508.18771, 2025.
[575] Zeeshan Rasheed, Malik Abdul Sami, Muhammad Waseem, Kai-Kristian Kemell, Xiaofeng Wang, Anh Nguyen, Kari
      Systä, and Pekka Abrahamsson. Ai-powered code review with llms: Early results. arXiv preprint arXiv:2404.18496,
      2024.
[576] Negar Arabzadeh and Charles LA Clarke. Benchmarking llm-based relevance judgment methods. In Proceedings of the
      48th International ACM SIGIR Conference on Research and Development in Information Retrieval, pages 3194–3204, 2025.
[577] Franz Zieris. Understanding how pair programming actually works in industry: Mechanisms, patterns, and dynamics.
      In Ernst Denert Award for Software Engineering 2020: Practice Meets Foundations, pages 275–293. Springer International
      Publishing Cham, 2022.
[578] Jim Buchan and Mark Pearl. Leveraging the mob mentality: An experience report on mob programming. In Proceedings
      of the 22nd International Conference on Evaluation and Assessment in Software Engineering 2018, pages 199–204, 2018.
[579] D. Post, R. P. Kendall, and L. G. Votta. Case study of the falcon code project. In Proceedings of the 2005 ACM/IEEE
      international symposium on Empirical software engineering, pages 234–242, 2005.
[580] Akhilesh Gadde. Democratizing software engineering through generative ai and vibe coding: The evolution of no-code
      development. Journal of Computer Science and Technology Studies, 8(2):45–62, 2025.
[581] Miku Watanabe, Hao Li, Yutaro Kashiwa, Brittany Reid, Hajimu Iida, and Ahmed E Hassan. On the use of agentic
      coding: An empirical study of pull requests on github. arXiv preprint arXiv:2509.14745, 2025.
[582] Ruchika Pandey, Prabhat Singh, Raymond Wei, and Shaila Shankar. Transforming software development: Evaluating
      the efficiency and challenges of github copilot in real-world projects. arXiv preprint arXiv:2406.17910, 2024.
[583] Giorgio Amasanti and Jasmin Jahić. The impact of ai-generated solutions on software architecture and productivity:
      Results from a survey study. In European Conference on Software Architecture, pages 89–104. Springer, 2025.
[584] Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, and Ramesh Karri. Asleep at the keyboard?
      assessing the security of github copilot’s code contributions. Communications of the ACM, 68(2):96–105, 2025.
[585] Yujia Fu, Peng Liang, Amjed Tahir, Zengyang Li, Mojtaba Shahin, Jiaxin Yu, and Jinfu Chen. Security weaknesses of
      copilot generated code in github. arXiv preprint arXiv:2310.02059, 2023.
[586] Neil Perry, Megha Srivastava, Lior Grosman, Daniel Fried, Jerry Tworek, Luke Zettlemoyer, Maria Christakis, and
      Nicolas Fournier. Do users write more insecure code with ai assistants? In Proceedings of the 2023 ACM SIGSAC
      Conference on Computer and Communications Security, pages 287–301, 2022.
[587] Alya Hannah, Ahmad Kamal, Muhammad Asim Khan, and Shafiq ur Rehman. Risk assessment, threat modeling and
      security testing in sdlc. arXiv preprint arXiv:2012.07625, 2020.
[588] Jakub Res, Ivan Homoliak, Martin Perešíni, Aleš Smrčka, Kamil Malinka, and Petr Hanacek. Enhancing security
      of ai-based code synthesis with github copilot via cheap and efficient prompt-engineering, 2024. URL https:
      //arxiv.org/abs/2403.12671.
[589] N. Medeiros, N. Ivaki, Alessandro Garcia, and Eduardo Figueiredo. Vulnerable code detection using software metrics
      and machine learning. IEEE Access, 8:144639–144652, 2020.
[590] Dinesh Reddy Chittibala. Advancements in automated code scanning techniques for detecting security vulnerabilities
      in open source software. International Journal of Computing and Engineering, 12(3):210–225, 2024.
[591] Rohith Pudari and Neil A Ernst. From copilot to pilot: Towards ai supported software development. arXiv preprint
      arXiv:2303.04142, 2023.



                                                            70
                                   A Survey of Vibe Coding with Large Language Models



[592] A. Aggarwal and P. Jalote. Integrating static and dynamic analysis for detecting vulnerabilities. In 30th Annual
      International Computer Software and Applications Conference (COMPSAC’06), pages 345–350. IEEE, 2006.
[593] A. D. Keromytis, Salvatore J. Stolfo, and Wenke Lee. The minestrone architecture combining static and dynamic
      analysis techniques for software security. In 2011 First SysSec Workshop, pages 1–6. IEEE, 2011.
[594] Alberto Bacchelli and Christian Bird. Expectations, outcomes, and challenges of modern code review. In 2013 35th
      International Conference on Software Engineering (ICSE), pages 712–721. IEEE, 2013.
[595] Shane McIntosh, Yasutaka Kamei, Bram Adams, and Ahmed E Hassan. The impact of code review coverage and
      code review participation on software quality: A case study of the qt, vtk, and itk projects. In Proceedings of the 11th
      working conference on mining software repositories, pages 192–201, 2014.
[596] Nesara Dissanayake, Asangi Jayatilaka, Mansooreh Zahedi, and M Ali Babar. Software security patch management-a
      systematic literature review of challenges, approaches, tools and practices. Information and Software Technology, 144:
      106771, 2022.
[597] Zhiqiang Lin, Xuxian Jiang, Dongyan Xu, Bing Mao, and Li Xie. Autopag: towards automated software patch
      generation with source code root cause identification and repair. In Proceedings of the 2nd ACM symposium on
      Information, computer and communications security, pages 329–340, 2007.
[598] Jen-tse Huang, Jiaxu Zhou, Tailin Jin, Xuhui Zhou, Zixi Chen, Wenxuan Wang, Youliang Yuan, Michael R Lyu, and
      Maarten Sap. On the resilience of llm-based multi-agent collaboration with faulty agents. arXiv preprint arXiv:2408.00989,
      2024.
[599] Qian Xiong, Yuekai Huang, Ziyou Jiang, Zhiyuan Chang, Yujia Zheng, Tianhao Li, and Mingyang Li. Butterfly
      effects in toolchains: A comprehensive analysis of failed parameter filling in llm tool-agent systems. arXiv preprint
      arXiv:2507.15296, 2025.
[600] Haoyang Liu, Yijiang Li, and Haohan Wang. Genomas: A multi-agent framework for scientific discovery via
      code-driven gene expression analysis. arXiv preprint arXiv:2507.21035, 2025.
[601] Joseph Spracklen, Raveen Wijewickrama, AHM Nazmus Sakib, Anindya Maiti, and Bimal Viswanath. We have a
      package for you! a comprehensive analysis of package hallucinations by code generating {LLMs}. In 34th USENIX
      Security Symposium (USENIX Security 25), pages 3687–3706, 2025.
[602] Arjun Krishna, Erick Galinkin, Leon Derczynski, and Jeffrey Martin. Importing phantoms: Measuring llm package
      hallucination vulnerabilities. arXiv preprint arXiv:2501.19012, 2025.
[603] Yukai Zhao, Menghan Wu, Xing Hu, and Xin Xia. Hfuzzer: Testing large language models for package hallucinations
      via phrase-based fuzzing. arXiv preprint arXiv:2509.23835, 2025.
[604] Yage Zhang. Cutting the root of hallucination: Structural trimming for vulnerability mitigation in code llms. In Second
      Conference on Language Modeling, 2025.
[605] Shuai Shao, Qihan Ren, Chen Qian, Boyi Wei, Dadi Guo, Jingyi Yang, Xinhao Song, Linfeng Zhang, Weinan
      Zhang, Dongrui Liu, et al. Your agent may misevolve: Emergent risks in self-evolving llm agents. arXiv preprint
      arXiv:2509.26354, 2025.
[606] Akshat Naik, Patrick Quinn, Guillermo Bosch, Emma Gouné, Francisco Javier Campos Zabala, Jason Ross Brown, and
      Edward James Young. Agentmisalignment: Measuring the propensity for misaligned behaviour in llm-based agents.
      arXiv preprint arXiv:2506.04018, 2025.
[607] Aengus Lynch, Benjamin Wright, Caleb Larson, Kevin K. Troy, Stuart J. Ritchie, Sören Mindermann, Ethan Perez,
      and Evan Hubinger. Agentic misalignment: How llms could be an insider threat. Anthropic Research, 2025.
      https://www.anthropic.com/research/agentic-misalignment.
[608] OWASP Foundation. Source code analysis tools (static application security testing, sast). https://owasp.org/
      www-community/Source_Code_Analysis_Tools, 2024.
[609] OWASP Foundation. Dynamic application security testing (dast) — owasp devsecops guideline. https://owasp.org/
      www-project-devsecops-guideline/latest/02b-Dynamic-Application-Security-Testing, 2024.
[610] Alexa VanHattum, Daniel Schwartz-Narbonne, Nathan Chong, and Adrian Sampson. Verifying dynamic trait objects
      in rust. In Proceedings of the 44th International Conference on Software Engineering: Software Engineering in Practice, pages
      321–330, 2022.
[611] Domenico Cotroneo, Alessio Foggia, Cristina Improta, Pietro Liguori, and Roberto Natella. Automating the correctness
      assessment of ai-generated code for security contexts. Journal of Systems and Software, 216:112113, 2024.



                                                               71
                                 A Survey of Vibe Coding with Large Language Models



[612] Zachary Kenton, Noah Siegel, János Kramár, Jonah Brown-Cohen, Samuel Albanie, Jannis Bulian, Rishabh Agarwal,
      David Lindner, Yunhao Tang, Noah Goodman, et al. On scalable oversight with weak llms judging strong llms.
      Advances in Neural Information Processing Systems, 37:75229–75276, 2024.
[613] Houda Nait El Barj and Théophile Sautory. Reinforcement learning from llm feedback to counteract goal misgeneral-
      ization. arXiv preprint arXiv:2401.07181, 2024.
[614] Collin Burns, Pavel Izmailov, Jan Hendrik Kirchner, Bowen Baker, Leo Gao, Leopold Aschenbrenner, Yining Chen,
      Adrien Ecoffet, Manas Joglekar, Jan Leike, et al. Weak-to-strong generalization: Eliciting strong capabilities with weak
      supervision. In International Conference on Machine Learning, pages 4971–5012. PMLR, 2024.
[615] Joshua Engels, David D Baek, Subhash Kantamneni, and Max Tegmark. Scaling laws for scalable oversight. arXiv
      preprint arXiv:2504.18530, 2025.
[616] Paul Christiano, Buck Shlegeris, and Dario Amodei. Supervising strong learners by amplifying weak experts. arXiv
      preprint arXiv:1810.08575, 2018.
[617] Geoffrey Irving, Paul Christiano, and Dario Amodei. Ai safety via debate. arXiv preprint arXiv:1805.00899, 2018.
[618] Jitao Sang, Yuhang Wang, Jing Zhang, Yanxu Zhu, Chao Kong, Junhong Ye, Shuyu Wei, and Jinlin Xiao. Improving
      weak-to-strong generalization with scalable oversight and ensemble learning. arXiv preprint arXiv:2402.00667, 2024.
[619] Yexiang Liu, Jie Cao, Zekun Li, Ran He, and Tieniu Tan. Breaking mental set to improve reasoning through diverse
      multi-agent debate. In The Thirteenth International Conference on Learning Representations, 2025.
[620] Yu Cui, Hang Fu, Haibin Zhang, Licheng Wang, and Cong Zuo. Free-mad: Consensus-free multi-agent debate. arXiv
      preprint arXiv:2509.11035, 2025.
[621] Hao Lang, Fei Huang, and Yongbin Li. Debate helps weak-to-strong generalization. In Proceedings of the AAAI
      Conference on Artificial Intelligence, volume 39, pages 27410–27418, 2025.
[622] Jizheng Chen, Kounianhua Du, Xinyi Dai, Weiming Zhang, Xihuai Wang, Yasheng Wang, Ruiming Tang, Weinan
      Zhang, and Yong Yu. Debatecoder: Towards collective intelligence of llms via test case driven llm debate for code
      generation. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
      Papers), pages 12055–12065, 2025.
[623] Johannes Schneider, Arianna Casanova Flores, and Anne-Catherine Kranz. Exploring human-llm conversations: Mental
      models and the originator of toxicity. arXiv preprint arXiv:2407.05977, 2024.
[624] Sadra Sabouri, Philipp Eibl, Xinyi Zhou, Morteza Ziyadi, Nenad Medvidovic, Lars Lindemann, and Souti Chattopad-
      hyay. Trust dynamics in ai-assisted development: Definitions, factors, and implications. arXiv preprint, 2025.
[625] Frederick P Brooks Jr. The mythical man-month (anniversary ed.). Addison-Wesley Longman Publishing Co., Inc., 1995.
[626] Laria Reynolds and Kyle McDonell. Prompt programming for large language models: Beyond the few-shot paradigm.
      In Extended abstracts of the 2021 CHI conference on human factors in computing systems, pages 1–7, 2021.
[627] Pengfei Liu, Weizhe Yuan, Jinlan Fu, Zhengbao Jiang, Hiroaki Hayashi, and Graham Neubig. Pre-train, prompt, and
      predict: A systematic survey of prompting methods in natural language processing. ACM computing surveys, 55(9):
      1–35, 2023.
[628] J Diego Zamfirescu-Pereira, Richmond Y Wong, Bjoern Hartmann, and Qian Yang. Why johnny can’t prompt: how
      non-ai experts try (and fail) to design llm prompts. In Proceedings of the 2023 CHI conference on human factors in
      computing systems, pages 1–21, 2023.
[629] Yongliang Shen, Kaitao Song, Xu Tan, Wenqi Zhang, Kan Ren, Siyu Yuan, Weiming Lu, Dongsheng Li, and Y. Zhuang.
      Taskbench: Benchmarking large language models for task automation. Neural Information Processing Systems, 2023.
[630] Emanuela Guglielmi, Venera Arnoudova, Gabriele Bavota, Rocco Oliveto, and Simone Scalabrino. How do copilot
      suggestions impact developers’ frustration and productivity? arXiv preprint arXiv:2504.06808, 2025.
[631] Anja Hawlitschek, Sarah Berndt, and Sandra Schulz. Empirical research on pair programming in higher education: a
      literature review. Computer science education, 33(3):400–428, 2023.
[632] Lori Flynn and Will Klieber. Using llms to adjudicate static-analysis alerts. arXiv preprint, 2025.
[633] Qing Xiao, Xinlan Emily Hu, Mark E Whiting, Arvind Karunakaran, Hong Shen, and Hancheng Cao. Ai hasn’t
      fixed teamwork, but it shifted collaborative culture: A longitudinal study in a project-based software development
      organization (2023-2025). arXiv preprint arXiv:2509.10956, 2025.




                                                             72
                                  A Survey of Vibe Coding with Large Language Models



[634] Qianou Ma, Tongshuang Wu, and Kenneth Koedinger. Is ai the better programming partner? human-human pair
      programming vs. human-ai pair programming. arXiv preprint arXiv:2306.05153, 2023.
[635] Suzhen Zhong, Ying Zou, and Bram Adams. Developer-llm conversations: An empirical study of interactions and
      generated code quality. arXiv preprint arXiv:2509.10402, 2025.
[636] Vibhor Agarwal, Yulong Pei, Salwa Alamir, and Xiaomo Liu. Codemirage: Hallucinations in code generated by large
      language models. arXiv preprint arXiv:2408.08333, 2024.
[637] Aaron Councilman, David Fu, Aryan Gupta, Chengxiao Wang, David Grove, Yu-Xiong Wang, and Vikram Adve.
      Towards formal verification of llm-generated code from natural language prompts. arXiv preprint arXiv:2507.13290,
      2025.
[638] Sriharitha Ambati. Security and Authenticity of AI-generated code. PhD thesis, University of Saskatchewan, 2023.
[639] Alfred Santa Molison, Marcia Moraes, Glaucia Melo, Fabio Santos, and Wesley KG Assuncao. Is llm-generated code
      more maintainable\& reliable than human-written code? arXiv preprint arXiv:2508.00700, 2025.
[640] Wannita Takerngsaksiri, Jirat Pasuksmit, Patanamon Thongtanunam, Chakkrit Tantithamthavorn, Ruixiong Zhang,
      Fan Jiang, Jing Li, Evan Cook, Kun Chen, and Ming Wu. Human-in-the-loop software development agents. In 2025
      IEEE/ACM 47th International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP), pages
      342–352. IEEE, 2025.
[641] Amr Mohamed, Maram Assi, and Mariam Guizani. The impact of llm-assistants on software developer productivity:
      A systematic literature review. arXiv preprint arXiv:2507.03156, 2025.
[642] Fangchen Song, Ashish Agarwal, and Wen Wen. The impact of generative ai on collaborative open-source software
      development: Evidence from github copilot. arXiv preprint arXiv:2410.02091, 2024.
[643] Mircea-Serban Vasiliniuc and Adrian Groza. Case study: using ai-assisted code generation in mobile teams. In 2023
      IEEE 19th International Conference on Intelligent Computer Communication and Processing (ICCP), pages 339–346. IEEE,
      2023.
[644] Sattvik Sahai, Prasoon Goyal, Michael Johnston, Anna Gottardi, Yao Lu, Lucy Hu, Luke Dai, Shaohua Liu, Samyuth
      Sagi, Hangjie Shi, et al. Amazon nova ai challenge–trusted ai: Advancing secure, ai-assisted software development.
      arXiv preprint arXiv:2508.10108, 2025.
[645] Russell Beale. Computer science education in the age of generative ai. arXiv preprint arXiv:2507.02183, 2025.
[646] Ben Shneiderman. Human-centered ai: ensuring human control while increasing automation. In Proceedings of the 5th
      Workshop on Human Factors in Hypertext, pages 1–2, 2022.
[647] Jiaofeng PAN and Jing WU. Integration of digital and real economies to shape new advantages in development: New
      form of human-cyber-physical ternary fusion. Bulletin of Chinese Academy of Sciences (Chinese Version), 39(6):1012–1021,
      2024.
[648] Zhiming Liu and Ji Wang. Human-cyber-physical systems: concepts, challenges, and research opportunities. Frontiers
      of Information Technology & Electronic Engineering, 21(11):1535–1553, 2020.
[649] Yuan-Zhuo Wang, Xiao-Long Jin, and Xue-Qi Cheng. Network big data: Present and future. Chinese Journal of
      Computers, 36:1125–1138, 06 2014. doi: 10.3724/SP.J.1016.2013.01125.
[650] Xueqi CHEGN, Shenghua Liu, and Ruqing ZHANG. Thinking on new system for big data technology. Bulletin of
      Chinese Academy of Sciences (Chinese Version), 37(1):60–67, 2022.
[651] Guojie LI. Ai4r: The fifth scientific research paradigm. Bulletin of Chinese Academy of Sciences (Chinese Version), 39(1):
      1–9, 2024.
[652] Roo-code. https://roocode.com/, 2025.
[653] Zhen Xiong, Yujun Cai, Zhecheng Li, and Yiwei Wang. Mapping the minds of llms: A graph-based analysis of
      reasoning llm, 2025. URL https://arxiv.org/abs/2505.13890.
[654] Chang Liu, Hongkai Chen, Yujun Cai, Hang Wu, Qingwen Ye, Ming-Hsuan Yang, and Yiwei Wang. Structured
      attention matters to multimodal llms in document understanding. arXiv preprint arXiv:2506.21600, 2025.
[655] Yang Liu, Xiaobin Tian, Zequn Sun, and Wei Hu. Finetuning generative large language models with discrimination
      instructions for knowledge graph completion. In International Semantic Web Conference, 2024.




                                                              73
                                 A Survey of Vibe Coding with Large Language Models



[656] Xindi Luo, Zequn Sun, Jing Zhao, Zhe Zhao, and Wei Hu. Knowla: Enhancing parameter-efficient finetuning with
      knowledgeable adaptation. In Proceedings of the 2024 Conference of the North American Chapter of the Association for
      Computational Linguistics, 2024.
[657] Haonan Ge, Yiwei Wang, Kai-Wei Chang, Hang Wu, and Yujun Cai. Framemind: Frame-interleaved video reasoning
      via reinforcement learning, 2025. URL https://arxiv.org/abs/2509.24008.
[658] Guangzi Zhang, Lizhe Chen, Yu Zhang, Yan Liu, Yuyao Ge, and Xingquan Cai. Translating words to worlds: zero-shot
      synthesis of 3d terrain from textual descriptions using large language models. Applied Sciences, 14(8):3257, 2024.
[659] Honghao Fu, Yuan Ouyang, Kai-Wei Chang, Yiwei Wang, and Yujun Cai. Contextnav: Towards agentic multimodal
      in-context learning. arXiv preprint arXiv:2510.04560, 2025.
[660] Yuanning Cui, Zequn Sun, and Wei Hu. A prompt-based knowledge graph foundation model for universal in-context
      reasoning. In Advances in Neural Information Processing Systems, 2024.
[661] Lizhe Chen, Binjia Zhou, Yuyao Ge, Jiayi Chen, and Shiguang Ni. Pis: Linking importance sampling and attention
      mechanisms for efficient prompt compression. arXiv preprint arXiv:2504.16574, 2025.
[662] Yuyao Ge, Zhongguo Yang, Lizhe Chen, Yiming Wang, and Chengyang Li. Attack based on data: a novel perspective
      to attack sensitive points directly. Cybersecurity, 6(1):43, 2023.
[663] Yujia Zheng, Tianhao Li, Haotian Huang, Tianyu Zeng, Jingyu Lu, Chuangxin Chu, Yuekai Huang, Ziyou Jiang, Qian
      Xiong, Yuyao Ge, et al. Are all prompt components value-neutral? understanding the heterogeneous adversarial
      robustness of dissected prompt in large language models. arXiv preprint arXiv:2508.01554, 2025.
[664] Yuyao Ge, Shenghua Liu, Baolong Bi, Yiwei Wang, Lingrui Mei, Wenjie Feng, Lizhe Chen, and Xueqi Cheng. Can
      graph descriptive order affect solving graph problems with llms? ACL 2025, pages 6404–6420, 2025.
[665] Jianing Chen, Zehao Li, Yujun Cai, Hao Jiang, Shuqin Gao, Honglong Zhao, Tianlu Mao, and Yucheng Zhang.
      From tokens to nodes: Semantic-guided motion control for dynamic 3d gaussian splatting, 2025. URL https:
      //arxiv.org/abs/2510.02732.
[666] Jianing Chen, Zehao Li, Yujun Cai, Hao Jiang, Chengxuan Qian, Juyuan Kang, Shuqin Gao, Honglong Zhao, Tianlu
      Mao, and Yucheng Zhang. Haif-gs: Hierarchical and induced flow-guided gaussian splatting for dynamic scene. arXiv
      preprint arXiv:2506.09518, 2025.
[667] Rongzhi Zhu, Yi Liu, Zequn Sun, Yiwei Wang, and Wei Hu. When can large reasoning models save thinking?
      mechanistic analysis of behavioral divergence in reasoning. arXiv preprint arXiv:2505.15276, 2025.
[668] Yuyao Ge, Shenghua Liu, Yiwei Wang, Lingrui Mei, Baolong Bi, Xuanshan Zhou, Jiayu Yao, Jiafeng Guo, and Xueqi
      Cheng. Focusing by contrastive attention: Enhancing vlms’ visual reasoning. arXiv preprint arXiv:2509.06461, 2025.
[669] Yuyao Ge, Shenghua Liu, Yiwei Wang, Lingrui Mei, Lizhe Chen, Baolong Bi, and Xueqi Cheng. Innate reasoning is
      not enough: In-context learning enhances reasoning large language models with less overthinking. arXiv preprint
      arXiv:2503.19602, 2025.
[670] Lingrui Mei, Shenghua Liu, Yiwei Wang, Baolong Bi, Yuyao Ge, Jun Wan, Yurong Wu, and Xueqi Cheng. a1: Steep
      test-time scaling law via environment augmented generation. arXiv preprint arXiv:2504.14597, 2025.
[671] Zhecheng Li, Guoxian Song, Yiwei Wang, Zhen Xiong, Junsong Yuan, and Yujun Cai. Generalist scanner meets
      specialist locator: A synergistic coarse-to-fine framework for robust gui grounding, 2025. URL https://arxiv.org/
      abs/2509.24133.
[672] Jiayu Yao, Shenghua Liu, Yiwei Wang, Lingrui Mei, Baolong Bi, Yuyao Ge, Zhecheng Li, and Xueqi Cheng. Who is in
      the spotlight: The hidden bias undermining multimodal retrieval-augmented generation. arXiv preprint arXiv:2506.11063,
      2025.
[673] Shiyu Ni, Keping Bi, Jiafeng Guo, and Xueqi Cheng. When do llms need retrieval augmentation? mitigating llms’
      overconfidence helps retrieval augmentation. arXiv preprint arXiv:2402.11457, 2024.
[674] Shiyu Ni, Keping Bi, Jiafeng Guo, Lulu Yu, Baolong Bi, and Xueqi Cheng. Towards fully exploiting llm internal states
      to enhance knowledge boundary perception. arXiv preprint arXiv:2502.11677, 2025.
[675] Rongzhi Zhu, Xiangyu Liu, Zequn Sun, Yiwei Wang, and Wei Hu. Mitigating lost-in-retrieval problems in retrieval
      augmented multi-hop question answering. arXiv preprint arXiv:2502.14245, 2025.
[676] Honghao Fu, Junlong Ren, Qi Chai, Deheng Ye, Yujun Cai, and Hao Wang. Vistawise: Building cost-effective agent
      with cross-modal knowledge graph for minecraft. arXiv preprint arXiv:2508.18722, 2025.




                                                            74
                                 A Survey of Vibe Coding with Large Language Models



[677] Hang Wu, Hongkai Chen, Yujun Cai, Chang Liu, Qingwen Ye, Ming-Hsuan Yang, and Yiwei Wang. Dimo-gui:
      Advancing test-time scaling in gui grounding via modality-aware visual reasoning. arXiv preprint arXiv:2507.00008,
      2025.
[678] Honghao Fu, Yufei Wang, Wenhan Yang, Alex C Kot, and Bihan Wen. Dp-iqa: Utilizing diffusion prior for blind
      image quality assessment in the wild. arXiv preprint arXiv:2405.19996, 2024.
[679] Zhen Xiong, Yujun Cai, Zhecheng Li, Junsong Yuan, and Yiwei Wang. Thinking with sound: Audio chain-of-thought
      enables multimodal reasoning in large audio-language models, 2025. URL https://arxiv.org/abs/2509.21749.
[680] Zhecheng Li, Guoxian Song, Yiwei Wang, Zhen Xiong, Junsong Yuan, and Yujun Cai. a2 r2 : Advancing img2latex
      conversion via visual reasoning with attention-guided refinement, 2025. URL https://arxiv.org/abs/2507.20890.
[681] Liyang Chen, Yujun Cai, Jieqiong Dong, and Yiwei Wang. Bright+: Upgrading the bright benchmark with marcus, a
      multi-agent rag clean-up suite, 2025. URL https://arxiv.org/abs/2506.07116.
[682] Haonan Ge, Yiwei Wang, Ming-Hsuan Yang, and Yujun Cai. Mrfd: Multi-region fusion decoding with self-consistency
      for mitigating hallucinations in lvlms, 2025. URL https://arxiv.org/abs/2508.10264.
[683] Ge Yuyao, Cheng Yiting, Wang Jia, Zhou Hanlin, and Chen Lizhe. Vision transformer based on knowledge distillation
      in tcm image classification. In 2022 IEEE 5th International Conference on Computer and Communication Engineering
      Technology (CCET), pages 120–125. IEEE, 2022.
[684] Yan Hu, Lizhe Chen, Hanna Xie, Yuyao Ge, Shun Zhou, and Xingquan Cai. Real-time non-photorealistic rendering
      method for black and white comic style in games and animation. Journal of System Simulation, 36(7):1699–1712, 2024.
[685] Lizhe Chen, Yan Hu, Yu Zhang, Yuyao Ge, Haoyu Zhang, and Xingquan Cai. Frequency-importance gaussian splatting
      for real-time lightweight radiance field rendering. Multimedia Tools and Applications, 83(35):83377–83401, 2024.
[686] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang,
      Chenxu Lv, et al. Qwen3 technical report. arXiv preprint arXiv:2505.09388, 2025.
[687] Naman Jain, Manish Shetty, Tianjun Zhang, King Han, Koushik Sen, and Ion Stoica. R2e: Turning any github
      repository into a programming agent environment. In Forty-first International Conference on Machine Learning, 2024.
[688] Terry Yue Zhuo, Minh Chien Vu, Jenny Chim, Han Hu, Wenhao Yu, Ratnadira Widyasari, Imam Nur Bani Yusuf,
      Haolan Zhan, Junda He, Indraneil Paul, et al. Bigcodebench: Benchmarking code generation with diverse function
      calls and complex instructions. arXiv preprint arXiv:2406.15877, 2024.
[689] Sridhar P. Nerur, RadhaKanta Mahapatra, and Gopalakrishnan Mangalaraj. Challenges of migrating to agile method-
      ologies. Communications of the ACM, 48(11):74–80, 2005.
[690] Kieran Conboy. Agility from first principles: Reconstructing the concept of agility in information systems development.
      Information Systems Research, 20(3):329–354, 2009.
[691] Barry Boehm. Get ready for agile methods, with care. Computer, 35(1):64–69, 2002.
[692] Torgeir Dingsøyr, Sridhar P. Nerur, Venkata Krishna Balijepally, and Nils Brede Moe. A decade of agile methodologies:
      Towards explaining agile software development. Journal of Systems and Software, 85(6):1213–1221, 2012.
[693] Yuji Zhang, Jing Li, Wei Wang, and Yang Liu. Vibe: Topic-driven temporal adaptation for twitter classification. arXiv
      preprint arXiv:2305.11744, 2023.
[694] Nan Jiang, Xiaopeng Li, Shiqi Wang, Qiang Zhou, Soneya B Hossain, Baishakhi Ray, Varun Kumar, Xiaofei Ma, and
      Anoop Deoras. Ledex: Training llms to better self-debug and explain code. Advances in Neural Information Processing
      Systems, 37:35517–35543, 2024.
[695] Torgeir Dingsøyr, Nils Brede Moe, Tore Dybå, and Geir Kjetil Hanssen. Exploring software development at the very
      large-scale: a revelatory case study and research agenda for agile method adaptation. Empirical Software Engineering,
      22(2):643–676, 2017.
[696] Ángel Fiallos Ordoñez. Mejoramiento en la productividad de software por la adaptación de un marco de desarrollo ágil. PhD
      thesis, Universidad de las Fuerzas Armadas ESPE, 2015.
[697] Veselin Georgiev and Kamelia Stefanova. Software development methodologies for reducing project risks. Economic
      Alternatives, 2:104–113, 2014.
[698] Hung-Fu Chang and S. Lu. Toward the integration of traditional and agile approaches. arXiv preprint arXiv:1305.6556,
      2013.




                                                             75
                                 A Survey of Vibe Coding with Large Language Models



[699] Vebjørn Berg, Jørgen Birkeland, and Magnus Jahre. Achieving agility and quality in product development - an
      empirical study of hardware startups. Journal of Systems and Software, 165:110643, 2020.
[700] Elias Jääsaari, Ville Hyvönen, Matteo Ceccarello, Teemu Roos, and Martin Aumüller. Vibe: Vector index benchmark
      for embeddings. arXiv preprint arXiv:2505.17810, 2025.
[701] Michael E. Fagan. Design and code inspections to reduce errors in program development. IBM Systems Journal, 15(3):
      182–211, 1976.
[702] Yonghee Shin, Andrew Meneely, Laurie Williams, and Jason Osborne. Evaluating complexity, code churn, and
      developer activity metrics as indicators of software vulnerabilities. IEEE Transactions on Software Engineering, 37(6):
      772–787, 2011.
[703] G. McGraw. Software security. Datenschutz und Datensicherheit - DuD, 28(11):668–670, 2004.
[704] Stuart Millar. Vulnerability detection in open source software: An introduction, 2022. URL https://arxiv.org/abs/
      2203.16428.
[705] A. Edmundson, P. Holtkamp, Laurie Williams, and Jason Osborne. An empirical study on the effectiveness of security
      code review. In Engineering Secure Software and Systems, pages 147–161. Springer, 2013.
[706] Mini Zeng and Feng Zhu. Secure coding in five steps. Journal of Cybersecurity Education, Research and Practice, 6(1):
      1–12, 2021.
[707] Hongzhe Li, Jaesang Oh, Suntae Kim, and Sungho Kim. Detecting violations of security requirements for vulnerability
      discovery in source code. IEICE Transactions on Information and Systems, E99.D(12):3140–3148, 2016.
[708] Pankaj Lathar, Raunak Shah, and Bhavesh Patel. Stacy-static code analysis for enhanced vulnerability detection. Cogent
      Engineering, 4(1):1345678, 2017.
[709] Syafiq Al Atiiq, Christian Gehrmann, and Kevin Dahlén. Vulnerability detection in popular programming languages
      with language models. arXiv preprint arXiv:2412.15905, 2024.
[710] Michael Howard. A process for performing security code reviews. IEEE Security & Privacy, 4(3):81–85, 2006.
[711] Larissa Braz, Christian Aeberhard, Gül Çalikli, and Alberto Bacchelli. Less is more: supporting developers in
      vulnerability detection during code review. In Proceedings of the 44th International Conference on Software Engineering,
      page 1317–1329. ACM, May 2022. doi: 10.1145/3510003.3511560. URL http://dx.doi.org/10.1145/3510003.3511560.
[712] R. Radke, S. Andra, O. Al-Kofahi, and B. Roysam. Image change detection algorithms: a systematic survey. IEEE
      Transactions on Image Processing, 14(3):294–307, 2005.
[713] A. Elgammal, David Harwood, and Larry S. Davis. Non-parametric model for background subtraction. In European
      Conference on Computer Vision, pages 751–767. Springer, 2000.
[714] Shireen Y Elhabian, Khaled M El-Sayed, and Sumaya H Ahmed. Moving object detection in spatial domain using
      background removal techniques-state-of-art. Recent patents on computer science, 1(1):32–54, 2008.
[715] T. Bouwmans, F. E. Baf, and B. Vachon. Statistical Background Modeling for Foreground Detection: A Survey. PhD thesis,
      University of Toulouse, 2010.
[716] Hanzi Wang and D. Suter. A consensus-based method for tracking: Modelling background scenario and foreground
      appearance. Pattern Recognition, 40(11):3012–3024, 2007.
[717] Soojin Park, Sungyong Park, and Heung-Nam Kim. An architecture framework for orchestrating context-aware it
      ecosystems: A case study for quantitative evaluation. Sensors (Basel, Switzerland), 18(11):3789, 2018.
[718] Jingliang Chen, Ken Goldberg, Jia-Yu Yang, and Dezhen Song. Vibe: a compressed video database structured for
      active browsing and search. IEEE Transactions on Multimedia, 6(4):581–594, 2004.
[719] Didier Perroud, Leonardo Angelini, Omar Abou Khaled, and Elena Mugellini. Context-based generation of multimodal
      feedbacks for natural interaction in smart environments. 2012. URL https://api.semanticscholar.org/CorpusID:
      59637168.
[720] T. Kryjak and M. Gorgon. Real-time implementation of the vibe foreground object segmentation algorithm. In 2013
      Federated Conference on Computer Science and Information Systems, pages 117–124. IEEE, 2013.
[721] Jacob Cohen. A coefficient of agreement for nominal scales. Educational and Psychological Measurement, 20(1):37–46,
      1960.




                                                             76
                                 A Survey of Vibe Coding with Large Language Models



[722] Camilo Chacón Sartori. Architectures of error: A philosophical inquiry into ai and human code generation, 2025.
      URL https://arxiv.org/abs/2505.19353.
[723] Nabil Mohammed Ali Munassar and A Govardhan. A comparison between five models of software engineering.
      International Journal of Computer Science Issues (IJCSI), 7(5):94, 2010.
[724] Nabil M. Mohammed, Mahmood Niazi, Mohammad Alshayeb, and Sajjad Mahmood. Exploring software security
      approaches in software development lifecycle: A systematic mapping study. Computer Standards & Interfaces, 50:
      107–115, 2017. ISSN 0920-5489. doi: https://doi.org/10.1016/j.csi.2016.10.001. URL https://www.sciencedirect.com/
      science/article/pii/S0920548916301155.
[725] Yao-Wen Huang, Fang Yu, Chia-Lin Hang, Dawu Chen, and Der-Tsai Lee. Securing web application code by static
      analysis and runtime protection. In Proceedings of the 13th international conference on World Wide Web, pages 211–221,
      2004.
[726] Mahdi Farzandway and Fatemeh Ghassemi. Automated repair of c programs using large language models. arXiv
      preprint arXiv:2509.01947, 2025.
[727] Cory Knobel and Nicole Radziwill. Vibe coding: Is human nature the ghost in the machine?                  arXiv preprint
      arXiv:2508.20918, 2025.
[728] OpenAI. Chatgpt. https://chatgpt.com/, 2024.
[729] Anthropic. Claude. https://claude.ai/, 2024.
[730] Xiang Deng, Jeff Da, Edwin Pan, Yannis Yiming He, Charles Ide, Kanak Garg, Niklas Lauffer, Andrew Park, Nitin
      Pasari, Chetan Rane, et al. Swe-bench pro: Can ai agents solve long-horizon software engineering tasks? arXiv
      preprint arXiv:2509.16941, 2025.
[731] Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie
      Cai, Michael Terry, Quoc Le, et al. Program synthesis with large language models. arXiv preprint arXiv:2108.07732,
      2021.
[732] Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan Guo, Collin Burns, Samir Puranik,
      Horace He, Dawn Song, et al. Measuring coding challenge competence with apps. arXiv preprint arXiv:2105.09938,
      2021.
[733] Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama,
      Koushik Sen, and Ion Stoica. Livecodebench: Holistic and contamination free evaluation of large language models for
      code. arXiv preprint arXiv:2403.07974, 2024.
[734] Michele Tufano, Anisha Agarwal, Jinu Jang, Roshanak Zilouchian Moghaddam, and Neel Sundaresan. Autodev:
      Automated ai-driven development. arXiv preprint arXiv:2403.08299, 2024.
[735] Junwei Liu, Kaixin Wang, Yixuan Chen, Xin Peng, Zhenpeng Chen, Lingming Zhang, and Yiling Lou. Large language
      model-based agents for software engineering: A survey. arXiv preprint arXiv:2409.02977, 2024.
[736] Reem Aleithan, Haoran Xue, Mohammad Mahdi Mohajer, Elijah Nnorom, Gias Uddin, and Song Wang. Swe-bench+:
      Enhanced coding benchmark for llms. arXiv preprint arXiv:2410.06992, 2024.
[737] Linghao Zhang, Shilin He, Chaoyun Zhang, Yu Kang, Bowen Li, Chengxing Xie, Junhao Wang, Maoquan Wang,
      Yufan Huang, Shengyu Fu, et al. Swe-bench goes live! arXiv preprint arXiv:2505.23419, 2025.
[738] Shanchao Liang, Spandan Garg, and Roshanak Zilouchian Moghaddam. The swe-bench illusion: When state-of-the-art
      llms remember instead of reason. arXiv preprint arXiv:2506.12286, 2025.
[739] Leonhard Applis, Yuntong Zhang, Shanchao Liang, Nan Jiang, Lin Tan, and Abhik Roychoudhury. Unified software
      engineering agent as ai software engineer. arXiv preprint arXiv:2506.14683, 2025.
[740] Anthropic. Claude 3 model family. https://www.anthropic.com/claude, 2024.
[741] Loubna Ben Allal, Raymond Li, Denis Kocetkov, Chenghao Mou, Christopher Akiki, Carlos Munoz Ferrandis, Niklas
      Muennighoff, Mayank Mishra, Alex Gu, Manan Dey, et al. Santacoder: don’t reach for the stars! arXiv preprint
      arXiv:2301.03988, 2023.
[742] Hazim Hanif and S. Maffeis. Vulberta: Simplified source code pre-training for vulnerability detection. IEEE International
      Joint Conference on Neural Network, 2022.
[743] Xiaonan Li, Daya Guo, Yeyun Gong, Yun Lin, Yelong Shen, Xipeng Qiu, Daxin Jiang, Weizhu Chen, and Nan Duan.
      Soft-labeled contrastive pre-training for function-level code representation. Conference on Empirical Methods in Natural
      Language Processing, 2022.


                                                             77
                                A Survey of Vibe Coding with Large Language Models



[744] Kang Yang, Xinjun Mao, Shangwen Wang, Yanlin Wang, Tanghaoran Zhang, Bo Lin, Yihao Qin, Zhang Zhang, Yao
      Lu, and Kamal Al-Sabahi. Large language models are qualified benchmark builders: Rebuilding pre-training datasets
      for advancing code intelligence tasks. IEEE International Conference on Program Comprehension, 2025.
[745] Alexey Svyatkovskiy, Shao Kun Deng, Shengyu Fu, and Neel Sundaresan. Intellicode compose: code generation using
      transformer. ESEC/SIGSOFT FSE, 2020.
[746] Xue Jiang, Zhuoran Zheng, Chen Lyu, Liang Li, and Lei Lyu. Treebert: A tree-based pre-trained model for programming
      language. Conference on Uncertainty in Artificial Intelligence, 2021.
[747] Zhongxin Liu, Zhijie Tang, Junwei Zhang, Xin Xia, and Xiaohu Yang. Pre-training by predicting program dependencies
      for vulnerability analysis tasks. International Conference on Software Engineering, 2024.
[748] Yu Nong, Richard Fang, Guangbei Yi, Kunsong Zhao, Xiapu Luo, Feng Chen, and Haipeng Cai. Vgx: Large-scale
      sample generation for boosting learning-based software vulnerability analyses. International Conference on Software
      Engineering, 2023.
[749] Changan Niu, Chuanyi Li, Vincent Ng, Jidong Ge, LiGuo Huang, and B. Luo. Spt-code: Sequence-to-sequence
      pre-training for learning source code representations. International Conference on Software Engineering, 2022.
[750] Xiaonan Li, Yeyun Gong, Yelong Shen, Xipeng Qiu, Hang Zhang, Bolun Yao, Weizhen Qi, Daxin Jiang, Weizhu Chen,
      and Nan Duan. Coderetriever: A large scale contrastive pre-training method for code search. Conference on Empirical
      Methods in Natural Language Processing, 2022.
[751] Rosalia Tufano, L. Pascarella, and G. Bavota. Automating code-related tasks through transformers: The impact of
      pre-training. International Conference on Software Engineering, 2023.
[752] Zhen Yang, J. Keung, Xiao Yu, Xiaodong Gu, Zhengyuan Wei, Xiaoxue Ma, and Miao Zhang. A multi-modal
      transformer-based code summarization approach for smart contracts. IEEE International Conference on Program
      Comprehension, 2021.
[753] Jane Yen, Tam’as L’evai, Qinyuan Ye, Xiang Ren, R. Govindan, and B. Raghavan. Semi-automated protocol dis-
      ambiguation and code generation. Conference on Applications, Technologies, Architectures, and Protocols for Computer
      Communication, 2020.
[754] Shangqing Liu, Yanzhou Li, Xiaofei Xie, Wei Ma, Guozhu Meng, and Yang Liu. Automated commit intelligence by
      pre-training. ACM Transactions on Software Engineering and Methodology, 2024.
[755] Yue Tan, Xiaoqian Hu, Hao Xue, Celso De Melo, and Flora D. Salim. Bisecle: Binding and separation in continual
      learning for video language understanding, 2025. URL https://arxiv.org/abs/2507.00469v1.
[756] Alane Suhr and Yoav Artzi. Continual learning for instruction following from realtime feedback. Neural Information
      Processing Systems, 2022.
[757] Andrea Cossu, T. Tuytelaars, Antonio Carta, Lucia C. Passaro, Vincenzo Lomonaco, and D. Bacciu. Continual
      pre-training mitigates forgetting in language and vision. Neural Networks, 2022.
[758] Yu Sun, Shuohuan Wang, Yukun Li, Shikun Feng, Hao Tian, Hua Wu, and Haifeng Wang. Ernie 2.0: A continual
      pre-training framework for language understanding. AAAI Conference on Artificial Intelligence, 2019.
[759] Rujun Han, Xiang Ren, and Nanyun Peng. Econet: Effective continual pretraining of language models for event
      temporal reasoning. Conference on Empirical Methods in Natural Language Processing, 2020.
[760] Shipeng Yan, Lanqing Hong, Hang Xu, Jianhua Han, T. Tuytelaars, Zhenguo Li, and Xuming He. Generative negative
      text replay for continual vision-language pretraining. European Conference on Computer Vision, 2022.
[761] Alec Radford, Jong Wook Kim, Chris Hallacy, A. Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda
      Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and I. Sutskever. Learning transferable visual models from
      natural language supervision. International Conference on Machine Learning, 2021.
[762] Qinyu Luo, Yining Ye, Shihao Liang, Zhong Zhang, Yujia Qin, Yaxi Lu, Yesai Wu, Xin Cong, Yankai Lin, Yingli Zhang,
      et al. Repoagent: An llm-powered open-source framework for repository-level code documentation generation. arXiv
      preprint arXiv:2402.16667, 2024.
[763] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu, Keming
      Lu, et al. Qwen2. 5-coder technical report. arXiv preprint arXiv:2409.12186, 2024.
[764] Roee Aharoni and Yoav Goldberg. Unsupervised domain clusters in pretrained language models. Annual Meeting of
      the Association for Computational Linguistics, 2020.




                                                           78
                                 A Survey of Vibe Coding with Large Language Models



[765] Zixuan Ke, Yijia Shao, Haowei Lin, Tatsuya Konishi, Gyuhak Kim, and Bin Liu. Continual pre-training of language
      models. International Conference on Learning Representations, 2023.
[766] Meta FAIR CodeGen Team. Cwm: An open-weights llm for research on code generation with world models. 2025.
[767] Sang Michael Xie, Hieu Pham, Xuanyi Dong, Nan Du, Hanxiao Liu, Yifeng Lu, Percy Liang, Quoc V. Le, Tengyu Ma,
      and Adams Wei Yu. Doremi: Optimizing data mixtures speeds up language model pretraining. Neural Information
      Processing Systems, 2023.
[768] Giorgio Roffo. Exploring advanced large language models with llmsuite, 2024. URL https://arxiv.org/abs/2407.
      12036v2.
[769] Xin Wang, Yasheng Wang, Yao Wan, Fei Mi, Yitong Li, Pingyi Zhou, Jin Liu, Hao Wu, Xin Jiang, and Qun Liu.
      Compilable neural code generation with compiler feedback.(2022). URL https://arxiv. org/abs/2203.05132.
[770] M. Lewis, Yinhan Liu, Naman Goyal, Marjan Ghazvininejad, Abdel rahman Mohamed, Omer Levy, Veselin Stoyanov,
      and Luke Zettlemoyer. Bart: Denoising sequence-to-sequence pre-training for natural language generation, translation,
      and comprehension. Annual Meeting of the Association for Computational Linguistics, 2019.
[771] Baptiste Rozière, M. Lachaux, Marc Szafraniec, and Guillaume Lample. Dobf: A deobfuscation pre-training objective
      for programming languages. Neural Information Processing Systems, 2021.
[772] Zehan Li, Jianfei Zhang, Chuantao Yin, Y. Ouyang, and Wenge Rong. Procqa: A large-scale community-based
      programming question answering dataset for code search. International Conference on Language Resources and Evaluation,
      2024.
[773] Mingyang Geng, Shangwen Wang, Dezun Dong, Haotian Wang, Ge Li, Zhi Jin, Xiaoguang Mao, and Xiangke
      Liao. Large language models are few-shot summarizers: Multi-intent comment generation via in-context learning.
      International Conference on Software Engineering, 2023.
[774] Indraneil Paul, Haoyi Yang, Goran Glavas, Kristian Kersting, and Iryna Gurevych. Obscuracoder: Powering efficient
      code lm pre-training via obfuscation grounding. International Conference on Learning Representations, 2025.
[775] Denis Kocetkov, Raymond Li, Loubna Ben Allal, Jia Li, Chenghao Mou, Carlos Muñoz Ferrandis, Yacine Jernite,
      Margaret Mitchell, Sean Hughes, Thomas Wolf, Dzmitry Bahdanau, L. V. Werra, and H. D. Vries. The stack: 3 tb of
      permissively licensed source code. Trans. Mach. Learn. Res., 2022.
[776] Zhangqian Bi, Yao Wan, Zhaoyang Chu, Yufei Hu, Junyi Zhang, Hongyu Zhang, Guandong Xu, and Hai Jin. How to
      select pre-trained code models for reuse? a learning perspective. IEEE International Conference on Software Analysis,
      Evolution, and Reengineering, 2025.
[777] Hamed Jelodar, Mohammad Meymani, and R. Razavi-Far. Large language models (llms) for source code analysis:
      applications, models and datasets, 2025. URL https://arxiv.org/abs/2503.17502v1.
[778] CodeGemma Team, Heri Zhao, Jeffrey Hui, Joshua Howland, Nam Nguyen, Siqi Zuo, Andrea Hu, Christopher A
      Choquette-Choo, Jingyue Shen, Joe Kelley, et al. Codegemma: Open code models based on gemma. arXiv preprint
      arXiv:2406.11409, 2024.
[779] Zhaojian Yu, Xin Zhang, Ning Shang, Yangyu Huang, Can Xu, Yishujie Zhao, Wenxiang Hu, and Qiufeng Yin.
      Wavecoder: Widespread and versatile enhancement for code large language models by instruction tuning. Annual
      Meeting of the Association for Computational Linguistics, 2023.
[780] Zifan Song, Yudong Wang, Wenwei Zhang, Kuikun Liu, Chengqi Lyu, Demin Song, Qipeng Guo, Hang Yan, Dahua
      Lin, Kai Chen, and Cairong Zhao. Alchemistcoder: Harmonizing and eliciting code capability by hindsight tuning on
      multi-source data. Neural Information Processing Systems, 2024.
[781] Niels Mündler, Mark Niklas Müller, Jingxuan He, and Martin T. Vechev. Swt-bench: Testing and validating real-world
      bug-fixes with code agents. Neural Information Processing Systems, 2024.
[782] Yi Tay, Mostafa Dehghani, Vinh Q. Tran, Xavier García, Jason Wei, Xuezhi Wang, Hyung Won Chung, Dara Bahri,
      Tal Schuster, H. Zheng, Denny Zhou, N. Houlsby, and Donald Metzler. Ul2: Unifying language learning paradigms.
      International Conference on Learning Representations, 2022.
[783] Kaitao Song, Xu Tan, Tao Qin, Jianfeng Lu, and Tie-Yan Liu. Mass: Masked sequence to sequence pre-training for
      language generation. International Conference on Machine Learning, 2019.
[784] Mandar Joshi, Danqi Chen, Yinhan Liu, Daniel S. Weld, Luke Zettlemoyer, and Omer Levy. Spanbert: Improving
      pre-training by representing and predicting spans. Transactions of the Association for Computational Linguistics, 2019.




                                                            79
                                A Survey of Vibe Coding with Large Language Models



[785] Minsoo Kim, V. S. Bursztyn, E. Koh, Shunan Guo, and Seung won Hwang. Rada: Retrieval-augmented web agent
      planning with llms. Annual Meeting of the Association for Computational Linguistics, 2024.
[786] Weichen Li and Weimin Pan. Enhancing chain-of-thought reasoning in large language models through text style
      diversity and prompt fusion. Other Conferences, 2024.
[787] Andrei Cosmin Redis, M. Sani, Bahram Zarrin, and Andrea Burattin. Skill learning using process mining for large
      language model plan generation. ICPM Workshops, 2024.
[788] Hung Le, Hailin Chen, Amrita Saha, Akash Gokul, Doyen Sahoo, and Shafiq R. Joty. Codechain: Towards modular
      code generation through chain of self-revisions with representative sub-modules. International Conference on Learning
      Representations, 2023.
[789] Tao Huang, Zhihong Sun, Zhi Jin, Ge Li, and Chen Lyu. Knowledge-aware code generation with large language
      models. IEEE International Conference on Program Comprehension, 2024.
[790] Izzeddin Gur, Hiroki Furuta, Austin Huang, Mustafa Safdari, Yutaka Matsuo, D. Eck, and Aleksandra Faust. A
      real-world webagent with planning, long context understanding, and program synthesis. International Conference on
      Learning Representations, 2023.
[791] Nicola Dainese, Matteo Merler, Minttu Alakuijala, and Pekka Marttinen. Generating code world models with large
      language models guided by monte carlo tree search. Neural Information Processing Systems, 2024.
[792] Gabriel Maher. Llmpc: Large language model predictive control. De Computis, 2025.
[793] Cong Zhang, Derrick-Goh-Xin Deik, Dexun Li, Hao Zhang, and Yong Liu. Planning with multi-constraints via
      collaborative language agents. International Conference on Computational Linguistics, 2024.
[794] Haitao Li, Junjie Chen, Jingli Yang, Qingyao Ai, Wei Jia, Youfeng Liu, Kai Lin, Yueyue Wu, Guozhi Yuan, Yiran Hu,
      Wuyue Wang, Yiqun Liu, and Minlie Huang. Legalagentbench: Evaluating llm agents in legal domain, 2024. URL
      https://arxiv.org/abs/2412.17259v1.
[795] Manling Li, Shiyu Zhao, Qineng Wang, Kangrui Wang, Yu Zhou, S. Srivastava, Cem Gokmen, Tony Lee, Li Erran
      Li, Ruohan Zhang, Weiyu Liu, Percy Liang, Fei-Fei Li, Jiayuan Mao, and Jiajun Wu. Embodied agent interface:
      Benchmarking llms for embodied decision making. Neural Information Processing Systems, 2024.
[796] Karthik Valmeekam, Matthew Marquez, S. Sreedharan, and Subbarao Kambhampati. On the planning abilities of
      large language models - a critical investigation. Neural Information Processing Systems, 2023.
[797] Subbarao Kambhampati. Can large language models reason and plan? Annals of the New York Academy of Sciences,
      2024.
[798] Yan Ding, Xiaohan Zhang, Chris Paxton, and Shiqi Zhang. Task and motion planning with large language models for
      object rearrangement. IEEE/RJS International Conference on Intelligent RObots and Systems, 2023.
[799] Cristina Cornelio, Flavio Petruzzellis, and Pietro Lio. Hierarchical planning for complex tasks with knowledge
      graph-rag and symbolic verification, 2025. URL https://arxiv.org/abs/2504.04578v1.
[800] Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W. Cohen. Program of thoughts prompting: Disentangling
      computation from reasoning for numerical reasoning tasks. Trans. Mach. Learn. Res., 2022.
[801] Lucas Lehnert, Sainbayar Sukhbaatar, Paul Mcvay, Michael Rabbat, and Yuandong Tian. Beyond a*: Better planning
      with transformers via search dynamics bootstrapping, 2024. URL https://arxiv.org/abs/2402.14083v2.
[802] Xinran Zhao, Hanie Sedghi, Bernd Bohnet, Dale Schuurmans, and Azade Nova. Improving large language model
      planning with action sequence similarity. International Conference on Learning Representations, 2025.
[803] Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Yu Wu, Sergey Edunov, Danqi Chen, and Wen
      tau Yih. Dense passage retrieval for open-domain question answering. Conference on Empirical Methods in Natural
      Language Processing, 2020.
[804] Jiacheng Ye, Zhiyong Wu, Jiangtao Feng, Tao Yu, and Lingpeng Kong. Compositional exemplars for in-context learning.
      International Conference on Machine Learning, 2023.
[805] Tom Silver, Soham Dan, Kavitha Srinivas, J. Tenenbaum, L. Kaelbling, and Michael Katz. Generalized planning in
      pddl domains with pretrained large language models. AAAI Conference on Artificial Intelligence, 2023.
[806] Chuheng Zhang, Wei Shen, Li Zhao, Xuyun Zhang, Lianyong Qi, Wanchun Dou, and Jiang Bian. Policy filtration in
      rlhf to fine-tune llm for code generation. 2024.




                                                           80
                                 A Survey of Vibe Coding with Large Language Models



[807] M. Fox and D. Long. Pddl2.1: An extension to pddl for expressing temporal planning domains. Journal of Artificial
      Intelligence Research, 2003.
[808] Yuqian Jiang, Shiqi Zhang, Piyush Khandelwal, and P. Stone. Task planning in robotics: an empirical comparison of
      pddl- and asp-based systems. Frontiers of Information Technology & Electronic Engineering, 2018.
[809] Alejandro Suárez-Hernández, G. Alenyà, and C. Torras. Interleaving hierarchical task planning and motion constraint
      testing for dual-arm manipulation. IEEE/RJS International Conference on Intelligent RObots and Systems, 2018.
[810] Hector Muñoz-Avila, D. Aha, and Paola Rizzo. Chathtn: Interleaving approximate (llm) and symbolic htn planning.
      NeuS, 2025.
[811] R. C. Cardoso and Rafael Heitor Bordini. A multi-agent extension of a hierarchical task network planning formalism.
      International Symposium on Distributed Computing and Artificial Intelligence, 2017.
[812] Chan Hee Song, Jiaman Wu, Clay Washington, Brian M. Sadler, Wei-Lun Chao, and Yu Su. Llm-planner: Few-shot
      grounded planning for embodied agents with large language models. IEEE International Conference on Computer Vision,
      2022.
[813] Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh Mottaghi, Luke Zettlemoyer,
      and D. Fox. Alfred: A benchmark for interpreting grounded instructions for everyday tasks. Computer Vision and
      Pattern Recognition, 2019.
[814] Valts Blukis, Chris Paxton, D. Fox, Animesh Garg, and Yoav Artzi. A persistent spatial semantic representation for
      high-level natural language instruction execution. Conference on Robot Learning, 2021.
[815] Pratyusha Sharma, A. Torralba, and Jacob Andreas. Skill induction and planning with latent language. Annual Meeting
      of the Association for Computational Linguistics, 2021.
[816] So Yeon Min, Devendra Singh Chaplot, Pradeep Ravikumar, Yonatan Bisk, and R. Salakhutdinov. Film: Following
      instructions in language with modular methods. International Conference on Learning Representations, 2021.
[817] He Zhu, Tianrui Qin, King Zhu, Heyuan Huang, Yeyi Guan, Jinxiang Xia, Yi Yao, Hanhao Li, Ningning Wang, Pai
      Liu, Tianhao Peng, Xin Gui, Xiaowan Li, Yuhui Liu, Y. Jiang, Jun Wang, Changwang Zhang, Xiangru Tang, Ge Zhang,
      Jian Yang, Minghao Liu, Xitong Gao, Jiaheng Liu, and Wangchunshu Zhou. Oagents: An empirical study of building
      effective agents, 2025. URL https://arxiv.org/abs/2506.15741v2.
[818] Chuanneng Sun, Songjun Huang, Haiqiao Liu, Jie Gong, and D. Pompili. Retrieval-augmented hierarchical in-context
      reinforcement learning and hindsight modular reflections for task planning with llms. IEEE International Conference on
      Robotics and Automation, 2024.
[819] Ce Hao, Anxing Xiao, Zhiwei Xue, and Harold Soh. Chd: Coupled hierarchical diffusion for long-horizon tasks, 2025.
      URL https://arxiv.org/abs/2505.07261v2.
[820] Karl Pertsch, Oleh Rybkin, F. Ebert, Chelsea Finn, Dinesh Jayaraman, and S. Levine. Long-horizon visual planning
      with goal-conditioned hierarchical predictors. Neural Information Processing Systems, 2020.
[821] Bernardo Aceituno and Alberto Rodriguez. A hierarchical framework for long horizon planning of object-contact
      trajectories. IEEE/RJS International Conference on Intelligent RObots and Systems, 2022.
[822] Zhixuan Liang, Yao Mu, Hengbo Ma, Masayoshi Tomizuka, Mingyu Ding, and Ping Luo. Skilldiffuser: Interpretable
      hierarchical planning via skill abstractions in diffusion-based task execution. Computer Vision and Pattern Recognition,
      2023.
[823] Woo Kyung Kim, Minjong Yoo, and Honguk Woo. Robust policy learning via offline skill diffusion. AAAI Conference
      on Artificial Intelligence, 2024.
[824] Israel Puerta-Merino, Carlos N’unez-Molina, Pablo Mesejo, and Juan Fern’andez-Olivares. A roadmap to guide the
      integration of llms in hierarchical planning. arXiv preprint, 2025.
[825] L. Kaelbling and Tomas Lozano-Perez. Hierarchical task and motion planning in the now. IEEE International Conference
      on Robotics and Automation, 2011.
[826] S Gravitas. Auto-gpt: An experimental open-source attempt to make gpt-4 fully autonomous. github. retrieved april
      17, 2023.
[827] Wenying Niu, Hongru Ma, and Yue Zhai. Research on task planning methods for embodied intelligence based on
      large language models. 2025 International Symposium on Intelligent Robotics and Systems (ISoIRS), 2025.
[828] E. Zelikman, Qian Huang, Gabriel Poesia, Noah D. Goodman, and Nick Haber. Parsel: Algorithmic reasoning with
      language models by composing decompositions. Neural Information Processing Systems, 2022.


                                                             81
                                A Survey of Vibe Coding with Large Language Models



[829] S. S. Kannan, Vishnunandan L. N. Venkatesh, and Byung-Cheol Min. Smart-llm: Smart multi-agent robot task planning
      using large language models. IEEE/RJS International Conference on Intelligent RObots and Systems, 2023.
[830] Fei Tang, Haolei Xu, Hang Zhang, Siqi Chen, Xingyu Wu, Yongliang Shen, Wenqi Zhang, Guiyang Hou, Zeqi Tan,
      Yuchen Yan, Kaitao Song, Jian Shao, Weiming Lu, Jun Xiao, and Yueting Zhuang. A survey on (m)llm-based gui
      agents, 2025. URL https://arxiv.org/abs/2504.13865v2.
[831] Yuan-Qi Bei, Weizhi Zhang, Siwen Wang, Weizhi Chen, Sheng Zhou, Haoyang Chen, Yong Li, Jiajun Bu, Shirui Pan,
      Yizhou Yu, Irwin King, Fakhri Karray, and Philip S. Yu. Graphs meet ai agents: Taxonomy, progress, and future
      opportunities, 2025. URL https://arxiv.org/abs/2506.18019v3.
[832] TaekHyun Park, YoungJun Choi, SeungHoon Shin, and Kwangil Lee. La-rcs: Llm-agent-based robot control system.
      Sensors and materials, 2025.
[833] Yuntao Wang, Shaolong Guo, Yanghe Pan, Zhou Su, Fahao Chen, Tom H. Luan, Peng Li, Jiawen Kang, and Dusit Niyato.
      Internet of agents: Fundamentals, applications, and challenges, 2025. URL https://arxiv.org/abs/2505.07176v1.
[834] Nan Wang, Yafei Liu, Chen Chen, and Haonan Lu. Genx: Mastering code and test generation with execution feedback.
      arXiv preprint arXiv:2412.13464, 2024.
[835] Hao Wang, Boyi Liu, Yufeng Zhang, and Jie Chen. Seed-cts: Unleashing the power of tree search for superior
      performance in competitive coding tasks. arXiv preprint arXiv:2412.12544, 2024.
[836] Bin Xu, Yiguan Lin, Yinghao Li, and Yang Gao. Sra-mcts: Self-driven reasoning augmentation with monte carlo tree
      search for code generation. arXiv preprint arXiv:2411.11053, 2024.
[837] W. Gosrich, Saurav Agarwal, Kashish Garg, Siddharth Mayya, Matthew Malencia, Mark Yim, and Vijay Kumar. Online
      multi-robot coordination and cooperation with task precedence relationships. IEEE Transactions on robotics, 2025.
[838] Taylor W. Webb, S. S. Mondal, and Ida Momennejad. Improving planning with large language models: A modular
      agentic architecture, 2023. URL https://arxiv.org/abs/2310.00194v4.
[839] Archiki Prasad, Alexander Koller, Mareike Hartmann, Peter Clark, Ashish Sabharwal, Mohit Bansal, and Tushar Khot.
      Adapt: As-needed decomposition and planning with language models. NAACL-HLT, 2023.
[840] Minseo Kwon, Yaesol Kim, and Young J. Kim. Fast and accurate task planning using neuro-symbolic language models
      and multi-level goal decomposition. IEEE International Conference on Robotics and Automation, 2024.
[841] Yiliu Sun, Yanfang Zhang, Zicheng Zhao, Sheng Wan, Dacheng Tao, and Chen Gong. Fast-slow-thinking: Complex
      task solving with large language models. arXiv preprint, 2025.
[842] Heng Zhou, Hejia Geng, Xiangyuan Xue, Zhenfei Yin, and Lei Bai. Reso: A reward-driven self-organizing llm-based
      multi-agent system for reasoning tasks, 2025. URL https://arxiv.org/abs/2503.02390v3.
[843] Charles L Wang, Trisha Singhal, Ameya Kelkar, and Jason Tuo. Mi9–agent intelligence protocol: Runtime governance
      for agentic ai systems. arXiv preprint arXiv:2508.03858, 2025.
[844] Xiangru Tang, Yuliang Liu, Zefan Cai, Yanjun Shao, Junjie Lu, Yichi Zhang, Zexuan Deng, Helan Hu, Kaikai An, Ruijun
      Huang, et al. Ml-bench: Evaluating large language models and agents for machine learning tasks on repository-level
      code. arXiv preprint arXiv:2311.09835, 2023.
[845] Karthik Valmeekam, Alberto Olmo, S. Sreedharan, and Subbarao Kambhampati. Planbench: An extensible benchmark
      for evaluating large language models on planning and reasoning about change. Neural Information Processing Systems,
      2022.
[846] L. Guan, Karthik Valmeekam, S. Sreedharan, and Subbarao Kambhampati. Leveraging pre-trained large language
      models to construct and utilize world models for model-based task planning. Neural Information Processing Systems,
      2023.
[847] Xavier Puig, K. Ra, Marko Boben, Jiaman Li, Tingwu Wang, S. Fidler, and A. Torralba. Virtualhome: Simulating
      household activities via programs. 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2018.
[848] Ramakrishna Bairi, Atharv Sonwane, Aditya Kanade, C. VageeshD, Arun Shankar Iyer, Suresh Parthasarathy, S. Raja-
      mani, B. Ashok, and Shashank Shet. Codeplan: Repository-level coding using llms and planning. Proc. ACM Softw.
      Eng., 2023.
[849] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, K. Gopalakr-
      ishnan, Karol Hausman, Alexander Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang,
      Rosario M Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, N. Joshi, Ryan C. Julian, Dmitry Kalashnikov, Yuheng Kuang,
      Kuang-Huei Lee, S. Levine, Yao Lu, Linda Luu, Carolina Parada, P. Pastor, Jornell Quiambao, Kanishka Rao, Jarek



                                                          82
                                 A Survey of Vibe Coding with Large Language Models



      Rettinghouse, D. Reyes, P. Sermanet, Nicolas Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, F. Xia, Ted
      Xiao, Peng Xu, Sichun Xu, and Mengyuan Yan. Do as i can, not as i say: Grounding language in robotic affordances.
      Conference on Robot Learning, 2022.
[850] Ishika Singh, Valts Blukis, A. Mousavian, Ankit Goyal, Danfei Xu, Jonathan Tremblay, D. Fox, Jesse Thomason, and
      Animesh Garg. Progprompt: Generating situated robot task plans using large language models. IEEE International
      Conference on Robotics and Automation, 2022.
[851] Bill Yuchen Lin, Chengsong Huang, Qian Liu, Wenda Gu, Sam Sommerer, and Xiang Ren. On grounded planning for
      embodied tasks with language models. AAAI Conference on Artificial Intelligence, 2022.
[852] E. Hovy. Planning coherent multisentential text. Annual Meeting of the Association for Computational Linguistics, 1988.
[853] Amanda Stent, R. Prasad, and M. Walker. Trainable sentence planning for complex information presentations in
      spoken dialog systems. Annual Meeting of the Association for Computational Linguistics, 2004.
[854] Amit Moryossef, Yoav Goldberg, and Ido Dagan. Step-by-step: Separating planning from realization in neural
      data-to-text generation. North American Chapter of the Association for Computational Linguistics, 2019.
[855] Lázaro Costa, Susana Barbosa, and Jácome Cunha. A backend platform for supporting the reproducibility of
      computational experiments, 2023. URL https://arxiv.org/abs/2308.00703v1.
[856] Yuhao Qing, Boyu Zhu, Mingzhe Du, Zhijiang Guo, Terry Yue Zhuo, Qianru Zhang, Jie M. Zhang, Heming Cui,
      S. Yiu, Dong Huang, See-Kiong Ng, and Anh Tuan Luu. Effibench-x: A multi-language benchmark for measuring
      efficiency of llm-generated code. arXiv preprint, 2025.
[857] Tom Kuchler, Michael J. Giardino, Timothy Roscoe, and Ana Klimovic. Function as a function. ACM Symposium on
      Cloud Computing, 2023.
[858] Anjali, Tyler Caraza-Harter, and M. Swift. Blending containers and virtual machines: a study of firecracker and gvisor.
      International Conference on Virtual Execution Environments, 2020.
[859] M. Bauer and C. Rossow. Cali: Compiler-assisted library isolation. ACM Asia Conference on Computer and Communications
      Security, 2021.
[860] Shravan Narayan, Craig Disselkoen, Tal Garfinkel, Nathan Froyd, Eric Rahm, Sorin Lerner, H. Shacham, and D. Stefan.
      Retrofitting fine grain isolation in the firefox renderer (extended version). USENIX Security Symposium, 2020.
[861] Jämes Ménétrey, Marcelo Pasin, Pascal Felber, V. Schiavoni, Giovanni Mazzeo, Arne Hollum, and Darshan Vaydia. A
      comprehensive trusted runtime for webassembly with intel sgx. IEEE Transactions on Dependable and Secure Computing,
      2023.
[862] Elizabeth Wyss, Alexander Wittman, Drew Davidson, and Lorenzo De Carli. Wolf at the door: Preventing install-time
      attacks in npm with latch. ACM Asia Conference on Computer and Communications Security, 2022.
[863] Md Rizwan Parvez, Wasi Uddin Ahmad, Saikat Chakraborty, Baishakhi Ray, and Kai-Wei Chang. Retrieval augmented
      code generation and summarization. arXiv preprint arXiv:2108.11601, 2021.
[864] Jose Rodrigo Sanchez Vicarte, Marcin Spoczynski, and Mostafa Elsaid. Threat modeling for ai: The case for an
      asset-centric approach, 2025. URL https://arxiv.org/abs/2505.06315v2.
[865] Boyu Han, Xinyu Wang, Yifan Wang, Junyu Yan, and Yidong Tian. New interaction paradigm for complex eda
      software leveraging gpt, 2023. URL https://arxiv.org/abs/2307.14740v2.
[866] A. Mcnutt, Chenglong Wang, R. Deline, and S. Drucker. On the design of ai-powered code assistants for notebooks.
      International Conference on Human Factors in Computing Systems, 2023.
[867] Nathaniel Weinman, S. Drucker, Titus Barik, and R. Deline. Fork it: Supporting stateful alternatives in computational
      notebooks. International Conference on Human Factors in Computing Systems, 2021.
[868] Zhenchang Xing, Qing Huang, Yu Cheng, Liming Zhu, Qinghua Lu, and Xiwei Xu. Prompt sapper: Llm-empowered
      software engineering infrastructure for ai-native services, 2023. URL https://arxiv.org/abs/2306.02230v1.
[869] Hyunjn An, Yongwon Kim, Wonduk Seo, Joonil Park, Daye Kang, Changhoon Oh, Dokyun Kim, and Seunghyun Lee.
      Aiap: A no-code workflow builder for non-experts with natural language and multi-agent collaboration, 2025. URL
      https://arxiv.org/abs/2508.02470v1.
[870] Ellen Jiang, Kristen Olson, Edwin Toh, A. Molina, Aaron Donsbach, Michael Terry, and Carrie J. Cai. Promptmaker:
      Prompt-based prototyping with large language models. CHI Extended Abstracts, 2022.




                                                            83
                                 A Survey of Vibe Coding with Large Language Models



[871] Tae Soo Kim, Yoonjoo Lee, Jamin Shin, Young-Ho Kim, and Juho Kim. Evallm: Interactive evaluation of large language
      model prompts on user-defined criteria. International Conference on Human Factors in Computing Systems, 2023.
[872] Ian Arawjo, Chelse Swoopes, Priyan Vaithilingam, Martin Wattenberg, and Elena L. Glassman. Chainforge: A visual
      toolkit for prompt engineering and llm hypothesis testing. International Conference on Human Factors in Computing
      Systems, 2023.
[873] Minsuk Kahng, Ian Tenney, Mahima Pushkarna, Michael Xieyang Liu, James Wexler, Emily Reif, Krystal Kallarackal,
      Minsuk Chang, Michael Terry, and Lucas Dixon. Llm comparator: Visual analytics for side-by-side evaluation of large
      language models. CHI Extended Abstracts, 2024.
[874] Mehmet Akhoroz and Caglar Yildirim. Conversational ai as a coding assistant: Understanding programmers’
      interactions with and expectations from large language models for coding, 2025. URL https://arxiv.org/abs/2503.
      16508v1.
[875] Philipp Eibl, Sadra Sabouri, and Souti Chattopadhyay. Exploring the challenges and opportunities of ai-assisted
      codebase generation, 2025. URL https://arxiv.org/abs/2508.07966v1.
[876] Yuqi Zhu, Xiaohan Wang, Jing Chen, Shuofei Qiao, Yixin Ou, Yunzhi Yao, Shumin Deng, Huajun Chen, and Ningyu
      Zhang. Llms for knowledge graph construction and reasoning: Recent capabilities and future opportunities. World
      wide web (Bussum), 2023.
[877] Chaojia Yu, Zihan Cheng, Hanwen Cui, Yishuo Gao, Zexu Luo, Yijin Wang, Hangbin Zheng, and Yong Zhao. A
      survey on agent workflow – status and future. 2025 8th International Conference on Artificial Intelligence and Big Data
      (ICAIBD), 2025.
[878] N. Le. A classification of adaptive feedback in educational systems for programming. Syst., 2016.
[879] Autumn Clark, Daniel Igbokwe, Samantha Ross, and M. Zibran. A quantitative analysis of quality and consistency in
      ai-generated code. 2024 7th International Conference on Software and System Engineering (ICoSSE), 2024.
[880] Sara Mernissi Arifi, R. Abbou, and Azeddine Zahi. Assisted learning of c programming through automated program
      repair and feed-back generation. Indonesian Journal of Electrical Engineering and Computer Science, 2020.
[881] Shihan Dou, Jiazheng Zhang, Jianxiang Zang, Yunbo Tao, Haoxiang Jia, Shichun Liu, Yuming Yang, Shenxi Wu,
      Shaoqing Zhang, Muling Wu, Changze Lv, Limao Xiong, Wenyu Zhan, Lin Zhang, Rongxiang Weng, Jingang Wang,
      Xunliang Cai, Yuemin Wu, Ming bo Wen, Rui Zheng, Tao Ji, Yixin Cao, Tao Gui, Xipeng Qiu, Qi Zhang, and Xuanjing
      Huang. Multi-programming language sandbox for llms. Proceedings of the 63rd Annual Meeting of the Association for
      Computational Linguistics (Volume 3: System Demonstrations), 2024.
[882] Md Ashraful Islam, Mohammed Eunus Ali, and Md Rizwan Parvez. Codesim: Multi-agent code generation and
      problem solving through simulation-driven planning and debugging. arXiv preprint arXiv:2502.05664, 2025.
[883] Mistral AI. Codestral 25.01. https://mistral.ai/news/codestral/, January 2024. Accessed: 2025-10-07.
[884] Yufan Ye, Ting Zhang, Wenbin Jiang, and Hua Huang. Process-supervised reinforcement learning for code generation,
      2025. URL https://arxiv.org/abs/2502.01715v1.
[885] Nan Jiang, Xiaopeng Li, Shiqi Wang, Qiang Zhou, Soneya Binta Hossain, Baishakhi Ray, Varun Kumar, Xiaofei Ma,
      and Anoop Deoras. Training llms to better self-debug and explain code. Neural Information Processing Systems, 2024.
[886] Daniel Nichols, Pranav Polasam, Harshitha Menon, Aniruddha Marathe, Todd Gamblin, and Abhinav Bhatele.
      Performance-aligned llms for generating fast code. arXiv preprint arXiv:2404.18864, 2024.
[887] Miltiadis Allamanis and Pengcheng Yin. Disproving program equivalence with llms, 2025. URL https://arxiv.org/
      abs/2502.18473v1.
[888] Julian Aron Prenner and Romain Robbes. Throwbench: Benchmarking llms by predicting runtime exceptions, 2025.
      URL https://arxiv.org/abs/2503.04241v1.
[889] M. Lacoste and Vincent Lefebvre. Trusted execution environments for telecoms: Strengths, weaknesses, opportunities,
      and threats. IEEE Security and Privacy, 2023.
[890] Tom Silver, Rohan Chitnis, J. Tenenbaum, L. Kaelbling, and Tomas Lozano-Perez. Learning symbolic operators for
      task and motion planning. IEEE/RJS International Conference on Intelligent RObots and Systems, 2021.
[891] Jacky Liang, Wenlong Huang, F. Xia, Peng Xu, Karol Hausman, Brian Ichter, Peter R. Florence, and Andy Zeng. Code
      as policies: Language model programs for embodied control. IEEE International Conference on Robotics and Automation,
      2022.




                                                            84
                                A Survey of Vibe Coding with Large Language Models



[892] Huihui Guo, Fan Wu, Yunchuan Qin, Ruihui Li, Keqin Li, and Kenli Li. Recent trends in task and motion planning
      for robotics: A survey. ACM Computing Surveys, 2023.
[893] Anurag Ajay, Seung-Jun Han, Yilun Du, Shaung Li, Abhishek Gupta, T. Jaakkola, Josh Tenenbaum, L. Kaelbling,
      Akash Srivastava, and Pulkit Agrawal. Compositional foundation models for hierarchical planning. Neural Information
      Processing Systems, 2023.
[894] Thomas G. Dietterich. Hierarchical reinforcement learning with the maxq value function decomposition. Journal of
      Artificial Intelligence Research, 1999.
[895] Tejas D. Kulkarni, Karthik Narasimhan, A. Saeedi, and J. Tenenbaum. Hierarchical deep reinforcement learning:
      Integrating temporal abstraction and intrinsic motivation. Neural Information Processing Systems, 2016.
[896] Alexander Pashevich, Danijar Hafner, James Davidson, R. Sukthankar, and C. Schmid. Modulated policy hierarchies,
      2018. URL https://arxiv.org/abs/1812.00025v1.
[897] Christoph Gebhardt, Antti Oulasvirta, and Otmar Hilliges. Hierarchical reinforcement learning as a model of human
      task interleaving, 2020. URL https://arxiv.org/abs/2001.02122v1.
[898] Pengfei Du. Omninova:a general multimodal agent framework, 2025. URL https://arxiv.org/abs/2503.20028v1.
[899] Minghong Geng, Shubham Pateria, Budhitama Subagdja, Lin Li, Xin Zhao, and Ah-Hwee Tan. L2m2: A hierarchical
      framework integrating large language model and multi-agent reinforcement learning. International Joint Conference on
      Artificial Intelligence, 2025.
[900] A. Drigas, Eleni Mitsea, and C. Skianis. Metamemory: Metacognitive strategies for improved memory operations and
      the role of vr and mobiles. Behavioral Science, 2022.
[901] Meire Fortunato, Melissa Tan, Ryan Faulkner, S. Hansen, Adrià Puigdomènech Badia, Gavin Buttimore, Charlie Deck,
      Joel Z. Leibo, and C. Blundell. Generalization of reinforcement learners with working and episodic memory. Neural
      Information Processing Systems, 2019.
[902] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez,
      Haotong Zhang, and Ion Stoica. Efficient memory management for large language model serving with pagedattention.
      Symposium on Operating Systems Principles, 2023.
[903] Nishant Subramani, Nivedita Suresh, and Matthew E. Peters. Extracting latent steering vectors from pretrained
      language models. Findings, 2022.
[904] Jiazheng Kang, Mingming Ji, Zhe Zhao, and Ting Bai. Memory os of ai agent, 2025. URL https://arxiv.org/abs/
      2506.06326v1.
[905] K. Armeni, C. Honey, and Tal Linzen. Characterizing verbatim short-term memory in neural language models.
      Conference on Computational Natural Language Learning, 2022.
[906] K. Oberauer, S. Lewandowsky, Edward Awh, Gordon D. A. Brown, Andrew R. A. Conway, N. Cowan, C. Donkin,
      S. Farrell, G. Hitch, Mark J. Hurlstone, W. Ma, C. Morey, D. E. Nee, J. Schweppe, Evie Vergauwe, and G. Ward.
      Benchmarks for models of short-term and working memory. Psychological bulletin, 2018.
[907] Chengkai Huang, Junda Wu, Yu Xia, Zixu Yu, Ruhan Wang, Tong Yu, Ruiyi Zhang, Ryan A. Rossi, B. Kveton,
      Dongruo Zhou, Julian J. McAuley, and Lina Yao. Towards agentic recommender systems in the era of multimodal
      large language models, 2025. URL https://arxiv.org/abs/2503.16734v1.
[908] Anian Ruoss, Gr’egoire Del’etang, Tim Genewein, Jordi Grau-Moya, R. Csordás, Mehdi Abbana Bennani, S. Legg,
      and J. Veness. Randomized positional encodings boost length generalization of transformers. Annual Meeting of the
      Association for Computational Linguistics, 2023.
[909] Alexis Chevalier, Alexander Wettig, Anirudh Ajith, and Danqi Chen. Adapting language models to compress contexts.
      Conference on Empirical Methods in Natural Language Processing, 2023.
[910] Xu Pan, Ely Hahami, Zechen Zhang, and H. Sompolinsky. Memorization and knowledge injection in gated llms, 2025.
      URL https://arxiv.org/abs/2504.21239v1.
[911] Sikuan Yan, Xiufeng Yang, Zuchao Huang, Ercong Nie, Zifeng Ding, Zonggen Li, Xiaowen Ma, Hinrich Schutze,
      Volker Tresp, and Yunpu Ma. Memory-r1: Enhancing large language model agents to manage and utilize memories
      via reinforcement learning. arXiv preprint, 2025.
[912] Christopher Kiley and Colleen M. Parks. Mechanisms of memory updating: State dependency vs. reconsolidation.
      Journal of Cognition, 2021.




                                                           85
                                A Survey of Vibe Coding with Large Language Models



[913] Junyeong Park, Junmo Cho, and Sungjin Ahn. Mr.steve: Instruction-following agents in minecraft with what-where-
      when memory. International Conference on Learning Representations, 2024.
[914] Mor Geva, R. Schuster, Jonathan Berant, and Omer Levy. Transformer feed-forward layers are key-value memories.
      Conference on Empirical Methods in Natural Language Processing, 2020.
[915] Fu-Chieh Chang, Yu-Ting Lee, and Pei-Yuan Wu. Unveiling the latent directions of reflection in large language models,
      2025. URL https://arxiv.org/abs/2508.16989v1.
[916] Manasa Bharadwaj, Nikhil Verma, and Kevin Ferreira. Omnireflect: Discovering transferable constitutions for llm
      agents via neuro-symbolic reflections, 2025. URL https://arxiv.org/abs/2506.17449v1.
[917] Yangshu Yuan, Heng Chen, Xinyi Jiang, Christian Ng, and Kexin Qiu. Cimr: Contextualized iterative multimodal
      reasoning for robust instruction following in lvlms, 2025. URL https://arxiv.org/abs/2507.22074v1.
[918] Wei Tao, Yucheng Zhou, Wenqiang Zhang, and Yu-Xi Cheng. Magis: Llm-based multi-agent framework for github
      issue resolution. Neural Information Processing Systems, 2024.
[919] Yuheng Cheng, Ceyao Zhang, Zhengwen Zhang, Xiangrui Meng, Sirui Hong, Wenhao Li, Zihao Wang, Zekai Wang,
      Feng Yin, Junhua Zhao, and Xiuqiang He. Exploring large language model based intelligent agents: Definitions,
      methods, and prospects, 2024. URL https://arxiv.org/abs/2401.03428v1.
[920] Roman J. Georgio, Caelum Forder, Suman Deb, Andri Rahimov, Peter Carroll, and Onder Gurcan. Coral protocol:
      Open infrastructure connecting the internet of agents, 2025. URL https://arxiv.org/abs/2505.00749v2.
[921] Kaiwen Dong. Large language model applied in multi-agent systema survey. Applied and Computational Engineering,
      2024.
[922] Daoguang Zan, Ailun Yu, Wei Liu, Dong Chen, Bo Shen, Wei Li, Yafen Yao, Yongshun Gong, Xiaolin Chen, Bei Guan,
      Zhiguang Yang, Yongji Wang, Qianxiang Wang, and Li zhen Cui. Codes: Natural language to code repository via
      multi-layer sketch, 2024. URL https://arxiv.org/abs/2403.16443v1.
[923] Shahbaz Siddeeq, Muhammad Waseem, Zeeshan Rasheed, Mahade Hasan, Jussi Rasku, Mika Saari, Henri Terho, Kalle
      Makela, Kai-Kristian Kemell, and Pekka Abrahamsson. Llm-based multi-agent system for intelligent refactoring of
      haskell code, 2025. URL https://arxiv.org/abs/2506.19481v1.
[924] RM Aratchige and Dr. Wmks Ilmini. Llms working in harmony: A survey on the technological aspects of building
      effective llm-based multi agent systems, 2025. URL https://arxiv.org/abs/2504.01963v1.
[925] Da Yin, Faeze Brahman, Abhilasha Ravichander, Khyathi Chandu, Kai-Wei Chang, Yejin Choi, and Bill Yuchen Lin.
      Agent lumos: Unified and modular training for open-source language agents. arXiv preprint arXiv:2311.05657, 2023.
[926] Ming Shen, Raphael Shu, Anurag Pratik, James Gung, Yubin Ge, Monica Sunkara, and Yi Zhang. Optimizing
      llm-based multi-agent system with textual feedback: A case study on software development, 2025. URL https:
      //arxiv.org/abs/2505.16086v2.
[927] Zhengqing Yuan, Ruoxi Chen, Zhaoxu Li, Weixiang Sun, Haolong Jia, Lifang He, Chi Wang, and Lichao Sun. Mora:
      Enabling generalist video generation via a multi-agent framework, 2024. URL https://arxiv.org/abs/2403.13248v3.
[928] Justin Chih-Yao Chen, Swarnadeep Saha, and Mohit Bansal. Reconcile: Round-table conference improves reasoning
      via consensus among diverse llms. arXiv preprint arXiv:2309.13007, 2023.
[929] Xuechen Liang, Meiling Tao, Tianyu Shi, and Yiting Xie. Cmat: A multi-agent collaboration tuning framework for
      enhancing small language models, 2024. URL https://arxiv.org/abs/2404.01663v6.
[930] Kai Xiong, Xiao Ding, Yixin Cao, Ting Liu, and Bing Qin. Examining inter-consistency of large language models
      collaboration: An in-depth analysis via debate. Conference on Empirical Methods in Natural Language Processing, 2023.
[931] Bo Pan, Jiaying Lu, Ke Wang, Li Zheng, Zhen Wen, Yingchaojie Feng, Minfeng Zhu, and Wei Chen. Agentcoord:
      Visually exploring coordination strategy for llm-based multi-agent collaboration. Computers & graphics, 2024.
[932] Sylvain Kouemo Ngassom, Arghavan Moradi Dakhel, Florian Tambon, and Foutse Khomh. Chain of targeted
      verification questions to improve the reliability of code generated by llms. AIware, 2024.
[933] Nam Huynh and Beiyu Lin. Large language models for code generation: A comprehensive survey of challenges,
      techniques, evaluation, and applications, 2025. URL https://arxiv.org/abs/2503.01245v2.
[934] Satyam Kumar Navneet and Joydeep Chandra. Rethinking autonomy: Preventing failures in ai-driven software
      engineering, 2025. URL https://arxiv.org/abs/2508.11824v1.




                                                           86
                                  A Survey of Vibe Coding with Large Language Models



[935] Stephen C. Adams, Tyler Cody, and P. Beling. A survey of inverse reinforcement learning. Artificial Intelligence Review,
      2022.
[936] Gabriel Poesia, Oleksandr Polozov, Vu Le, A. Tiwari, Gustavo Soares, Christopher Meek, and Sumit Gulwani.
      Synchromesh: Reliable code generation from pre-trained language models. International Conference on Learning
      Representations, 2022.
[937] Shima Imani, Liang Du, and H. Shrivastava. Mathprompter: Mathematical reasoning using large language models.
      Annual Meeting of the Association for Computational Linguistics, 2023.
[938] Shibo Hao, Yi Gu, Haodi Ma, Joshua Jiahua Hong, Zhen Wang, D. Wang, and Zhiting Hu. Reasoning with language
      model is planning with world model. Conference on Empirical Methods in Natural Language Processing, 2023.
[939] Qi He, Jie Zeng, Wenhao Huang, Lina Chen, Jin Xiao, Qianxi He, Xunzhe Zhou, Lida Chen, Xintao Wang, Yuncheng
      Huang, Haoning Ye, Zihan Li, Shisong Chen, Yikai Zhang, Zhouhong Gu, Jiaqing Liang, and Yanghua Xiao. Can
      large language models understand real-world complex instructions? AAAI Conference on Artificial Intelligence, 2023.
[940] Y. Hao, Zewen Chi, Li Dong, and Furu Wei. Optimizing prompts for text-to-image generation. Neural Information
      Processing Systems, 2022.
[941] Sina Gogani-Khiabani, Ashutosh Trivedi, Diptikalyan Saha, and Saeid Tizpaz-Niari. An llm agentic approach for
      legal-critical software: A case study for tax prep software. arXiv preprint, 2025.
[942] Yihao Qin, Shangwen Wang, Yiling Lou, Jinhao Dong, Kaixin Wang, Xiaoling Li, and Xiaoguang Mao. Soapfl: A
      standard operating procedure for llm-based method-level fault localization. IEEE Transactions on Software Engineering,
      2025.
[943] Aditya Bharat Soni, Boxuan Li, Xingyao Wang, Valerie Chen, and Graham Neubig. Coding agents with multimodal
      browsing are generalist problem solvers. arXiv preprint arXiv:2506.03011, 2025.
[944] Yixin Ji, Juntao Li, Hai Ye, Kaixin Wu, Jia Xu, Linjian Mo, and Min Zhang. A survey of test-time compute: From
      intuitive inference to deliberate reasoning, 2025. URL https://arxiv.org/abs/2501.02497v3.
[945] Michihiro Yasunaga and Percy Liang. Graph-based, self-supervised program repair from diagnostic feedback. Interna-
      tional Conference on Machine Learning, 2020.
[946] Wei Yang, Jinwei Xiao, Hongming Zhang, Qingyang Zhang, Yanna Wang, and Bo Xu. Coarse-to-fine grounded
      memory for llm agent planning, 2025. URL https://arxiv.org/abs/2508.15305v1.
[947] Victor Sanh, Albert Webson, Colin Raffel, Stephen H. Bach, Lintang Sutawika, Zaid Alyafeai, Antoine Chaffin, Arnaud
      Stiegler, Teven Le Scao, Arun Raja, Manan Dey, M Saiful Bari, Canwen Xu, Urmish Thakker, S. Sharma, Eliza Szczechla,
      Taewoon Kim, Gunjan Chhablani, Nihal V. Nayak, Debajyoti Datta, Jonathan D. Chang, Mike Tian-Jian Jiang, Han
      Wang, Matteo Manica, Sheng Shen, Zheng-Xin Yong, Harshit Pandey, Rachel Bawden, Thomas Wang, Trishala Neeraj,
      Jos Rozen, Abheesht Sharma, Andrea Santilli, Thibault Févry, Jason Alan Fries, R. Teehan, Stella Biderman, Leo Gao,
      T. Bers, Thomas Wolf, and Alexander M. Rush. Multitask prompted training enables zero-shot task generalization,
      2021. URL https://arxiv.org/abs/2110.08207v3.
[948] Tong Nie, Jiangming Sun, and Wei Ma. Exploring the roles of large language models in reshaping transportation
      systems: A survey, framework, and roadmap. Artificial Intelligence for Transportation, 2025.
[949] Yu Meng, Mengzhou Xia, and Danqi Chen. Simpo: Simple preference optimization with a reference-free reward.
      Neural Information Processing Systems, 2024.
[950] Haoran Xu, Amr Sharaf, Yunmo Chen, Weiting Tan, Lingfeng Shen, Benjamin Van Durme, Kenton Murray, and
      Young Jin Kim. Contrastive preference optimization: Pushing the boundaries of llm performance in machine translation.
      International Conference on Machine Learning, 2024.
[951] Brian Lester, Rami Al-Rfou, and Noah Constant. The power of scale for parameter-efficient prompt tuning. Conference
      on Empirical Methods in Natural Language Processing, 2021.
[952] Mingjie Liu, N. Pinckney, Brucek Khailany, and Haoxing Ren. Verilogeval: Evaluating large language models for
      verilog code generation, 2023. URL https://arxiv.org/abs/2309.07544v2.
[953] Lingzhe Zhang, Yunpeng Zhai, Tong Jia, Chiming Duan, Siyu Yu, Jinyang Gao, Bolin Ding, Zhonghai Wu, and
      Ying Li. Thinkfl: Self-refining failure localization for microservice systems via reinforcement fine-tuning, 2025. URL
      https://arxiv.org/abs/2504.18776v1.
[954] Jonas Pfeiffer, Aishwarya Kamath, Andreas Rücklé, Kyunghyun Cho, and Iryna Gurevych. Adapterfusion: Non-
      destructive task composition for transfer learning. Conference of the European Chapter of the Association for Computational
      Linguistics, 2020.


                                                              87
                                 A Survey of Vibe Coding with Large Language Models



[955] Yaoming Zhu, Jiangtao Feng, Chengqi Zhao, Mingxuan Wang, and Lei Li. Counter-interference adapter for multilingual
      machine translation. Conference on Empirical Methods in Natural Language Processing, 2021.
[956] Tao Lei, Junwen Bai, Siddhartha Brahma, J. Ainslie, Kenton Lee, Yanqi Zhou, Nan Du, Vincent Zhao, Yuexin Wu,
      Bo Li, Yu Zhang, and Ming-Wei Chang. Conditional adapters: Parameter-efficient transfer learning with fast inference.
      Neural Information Processing Systems, 2023.
[957] Kai Lv, Yuqing Yang, Tengxiao Liu, Qinghui Gao, Qipeng Guo, and Xipeng Qiu. Full parameter fine-tuning for large
      language models with limited resources. Annual Meeting of the Association for Computational Linguistics, 2023.
[958] Yongkang Liu, Yiqun Zhang, Qian Li, Shi Feng, Daling Wang, Yifei Zhang, and Hinrich Schütze. Hift: A hierarchical
      full parameter fine-tuning strategy. Conference on Empirical Methods in Natural Language Processing, 2024.
[959] Qi Luo, Hengxu Yu, and Xiao Li. Badam: A memory efficient full parameter optimization method for large language
      models. Neural Information Processing Systems, 2024.
[960] Ming Li, Yong Zhang, Zhitao Li, Jiuhai Chen, Lichang Chen, Ning Cheng, Jianzong Wang, Tianyi Zhou, and Jing
      Xiao. From quantity to quality: Boosting llm performance with self-guided data selection for instruction tuning. North
      American Chapter of the Association for Computational Linguistics, 2023.
[961] Avi Singh, John D. Co-Reyes, Rishabh Agarwal, Ankesh Anand, Piyush Patil, Peter J. Liu, James Harrison, Jaehoon
      Lee, Kelvin Xu, Aaron T Parisi, Abhishek Kumar, A. Alemi, Alex Rizkowsky, Azade Nova, Ben Adlam, Bernd Bohnet,
      Hanie Sedghi, Igor Mordatch, Isabelle Simpson, Izzeddin Gur, Jasper Snoek, Jeffrey Pennington, Jiri Hron, Kathleen
      Kenealy, Kevin Swersky, Kshiteej Mahajan, Laura Culp, Lechao Xiao, Maxwell Bileschi, Noah Constant, Roman Novak,
      Rosanne Liu, Tris Warkentin, Yundi Qian, Ethan Dyer, Behnam Neyshabur, Jascha Narain Sohl-Dickstein, and Noah
      Fiedel. Beyond human data: Scaling self-training for problem-solving with language models. Trans. Mach. Learn. Res.,
      2023.
[962] Subhabrata Mukherjee, Arindam Mitra, Ganesh Jawahar, Sahaj Agarwal, Hamid Palangi, and A. Awadallah. Orca:
      Progressive learning from complex explanation traces of gpt-4. arXiv preprint, 2023.
[963] Da Yin, Xiao Liu, Fan Yin, Ming Zhong, Hritik Bansal, Jiawei Han, and Kai-Wei Chang. Dynosaur: A dynamic growth
      paradigm for instruction-tuning data curation. Conference on Empirical Methods in Natural Language Processing, 2023.
[964] Aidan Hogan, Xin Luna Dong, Denny Vrandečić, and G. Weikum. Large language models, knowledge graphs and
      search engines: A crossroads for answering users’ questions, 2025. URL https://arxiv.org/abs/2501.06699v1.
[965] Yiming Ju, Ziyi Ni, Xingrun Xing, Zhixiong Zeng, Hanyu Zhao, Siqi Fan, and Zheng Zhang. Mitigating training
      imbalance in llm fine-tuning via selective parameter merging. Conference on Empirical Methods in Natural Language
      Processing, 2024.
[966] Lishui Fan, Yu Zhang, Mouxiang Chen, and Zhongxin Liu. Posterior-grpo: Rewarding reasoning processes in code
      generation. arXiv preprint, 2025.
[967] Nikita Sorokin, Ivan Sedykh, and Valentin Malykh. Iterative self-training for code generation via reinforced re-ranking.
      European Conference on Information Retrieval, 2025.
[968] Yanzhi Zhang, Zhaoxi Zhang, Haoxiang Guan, Yilin Cheng, Yitong Duan, Chen Wang, Yue Wang, Shuxin Zheng, and
      Jiyan He. No free lunch: Rethinking internal feedback for llm reasoning, 2025. URL https://arxiv.org/abs/2506.
      17219v2.
[969] Elias Lumer, V. K. Subbiah, James A. Burke, Pradeep Honaganahalli Basavaraju, and Austin Huber. Toolshed: Scale
      tool-equipped agents with advanced rag-tool fusion and tool knowledge bases. International Conference on Agents and
      Artificial Intelligence, 2024.
[970] Shishir G. Patil, Tianjun Zhang, Xin Wang, and Joseph E. Gonzalez. Gorilla: Large language model connected with
      massive apis. Neural Information Processing Systems, 2023.
[971] Jiajun Chai, Guojun Yin, Zekun Xu, Chuhuai Yue, Yi Jia, Siyu Xia, Xiaohan Wang, Jiwen Jiang, Xiaoguang Li, Chengqi
      Dong, Hang He, and Wei Lin. Rlfactory: A plug-and-play reinforcement learning post-training framework for llm
      multi-turn tool-use, 2025. URL https://arxiv.org/abs/2509.06980v1.
[972] Zhengliang Shi, Shen Gao, Xiuyi Chen, Lingyong Yan, Haibo Shi, Dawei Yin, Zhumin Chen, Pengjie Ren, Suzan
      Verberne, and Zhaochun Ren. Learning to use tools via cooperative and interactive agents. Conference on Empirical
      Methods in Natural Language Processing, 2024.
[973] Yanfei Zhang. Agent-as-tool: A study on the hierarchical decision making with reinforcement learning. arXiv preprint,
      2025.




                                                            88
                                  A Survey of Vibe Coding with Large Language Models



[974] Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, and Graham Neubig.
      Pal: Program-aided language models. International Conference on Machine Learning, 2022.
[975] Yu Gu, Yiheng Shu, Hao Yu, Xiao Liu, Yuxiao Dong, Jie Tang, Jayanth Srinivasa, Hugo Latapie, and Yu Su. Middleware
      for llms: Tools are instrumental for language agents in complex environments. Conference on Empirical Methods in
      Natural Language Processing, 2024.
[976] Ziyu Liu, Yuhang Zang, Yushan Zou, Zijian Liang, Xiao wen Dong, Yuhang Cao, Haodong Duan, Dahua Lin, and
      Jiaqi Wang. Visual agentic reinforcement fine-tuning, 2025. URL https://arxiv.org/abs/2505.14246v1.
[977] Ziyi Ni, Yifan Li, and Daxiang Dong. Tree-of-code: A hybrid approach for robust complex task planning and execution.
      arXiv preprint, 2024.
[978] Guozhi Yuan, Youfeng Liu, Jingli Yang, Wei Jia, Kai Lin, Yansong Gao, Shan He, Zilin Ding, and Haitao Li. Poact:
      Policy and action dual-control agent for generalized applications, 2025. URL https://arxiv.org/abs/2501.07054v1.
[979] Vaibhav Aggarwal, Ojasv Kamal, Abhinav Japesh, Zhijing Jin, and Bernhard Schölkopf. Dars: Dynamic action
      re-sampling to enhance coding agent performance by adaptive tree traversal. Annual Meeting of the Association for
      Computational Linguistics, 2025.
[980] Manish Bhattarai, Miguel Cordova, Javier E. Santos, and Dan O’Malley. Arcs: Agentic retrieval-augmented code
      synthesis with iterative refinement, 2025. URL https://arxiv.org/abs/2504.20434v1.
[981] Zhao Zhuo, Rongzhen Li, Kai Liu, Huhai Zou, KaiMao Li, Jie Yu, Tianhao Sun, and Qingbo Wu. Kaos: Large model
      multi-agent operating system, 2024. URL https://arxiv.org/abs/2406.11342v3.
[982] Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Samuel Stevens, Boshi Wang, Huan Sun, and Yu Su. Mind2web:
      Towards a generalist agent for the web. Neural Information Processing Systems, 2023.
[983] Zaid Khan, Ali Farhadi, Ranjay Krishna, Luca Weihs, Mohit Bansal, and Tanmay Gupta. Mutagrep: Execution-free
      repository-grounded plan search for code-use. arXiv preprint arXiv:2502.15872, 2025.
[984] Haolin Jin and Huaming Chen. Uncovering systematic failures of llms in verifying code against natural language
      specifications, 2025. URL https://arxiv.org/abs/2508.12358v1.
[985] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, D. Su, Yan Xu, Etsuko Ishii, Yejin Bang, Delong Chen, Wenliang Dai,
      Andrea Madotto, and Pascale Fung. Survey of hallucination in natural language generation. ACM Computing Surveys,
      2022.
[986] Jamie Hayes, Ilia Shumailov, William P Porter, and Aneesh Pappu. Measuring memorization in rlhf for code completion.
      In The Thirteenth International Conference on Learning Representations, 2024.
[987] Li Zhong, Zilong Wang, and Jingbo Shang. Debug like a human: A large language model debugger via verifying
      runtime execution step by step. Annual Meeting of the Association for Computational Linguistics, 2024.
[988] Xavier Amatriain. Prompt design and engineering: Introduction and advanced methods, 2024. URL https://arxiv.
      org/abs/2401.14423v4.
[989] Hai Ye and Hwee Tou Ng. Preference-guided reflective sampling for aligning language models. Conference on Empirical
      Methods in Natural Language Processing, 2024.
[990] Yunhai Feng, Jiaming Han, Zhuoran Yang, Xiangyu Yue, Sergey Levine, and Jianlan Luo. Reflective planning: Vision-
      language models for multi-stage long-horizon robotic manipulation, 2025. URL https://arxiv.org/abs/2502.16707v1.
[991] Weiran Yao, Shelby Heinecke, Juan Carlos Niebles, Zhiwei Liu, Yihao Feng, Le Xue, Rithesh Murthy, Zeyuan Chen,
      Jianguo Zhang, Devansh Arpit, Ran Xu, P. Mùi, Haiquan Wang, Caiming Xiong, and S. Savarese. Retroformer:
      Retrospective large language agents with policy gradient optimization. International Conference on Learning Representations,
      2023.
[992] Zikang Guo, Benfeng Xu, Xiaorui Wang, and Zhendong Mao. Mirror: Multi-agent intra- and inter-reflection for
      optimized reasoning in tool learning. International Joint Conference on Artificial Intelligence, 2025.
[993] Wenlong Liang, Rui Zhou, Yang Ma, Bing Zhang, Songlin Li, Yijia Liao, and Ping Kuang. Large model empowered
      embodied ai: A survey on decision-making and embodied learning, 2025. URL https://arxiv.org/abs/2508.10399v1.
[994] Kechi Zhang, Zhuo Li, Jia Li, Ge Li, and Zhi Jin. Self-edit: Fault-aware code editor for code generation. Annual
      Meeting of the Association for Computational Linguistics, 2023.
[995] Priyanshu Gupta, Shashank Kirtania, Ananya Singha, Sumit Gulwani, Arjun Radhakrishna, Sherry Shi, and Gustavo
      Soares. Metareflection: Learning instructions for language agents using past reflections. Conference on Empirical Methods
      in Natural Language Processing, 2024.


                                                              89
                                    A Survey of Vibe Coding with Large Language Models



 [996] Gustavo Sandoval, H. Pearce, Teo Nys, R. Karri, S. Garg, and Brendan Dolan-Gavitt. Lost at c: A user study on the
       security implications of large language model code assistants. USENIX Security Symposium, 2022.
 [997] M. Izadi, J. Katzy, Tim van Dam, Marc Otten, R. Popescu, and Arie van Deursen. Language models for code
       completion: A practical evaluation. International Conference on Software Engineering, 2024.
 [998] Albert Contreras, E. Guerra, and Juan de Lara. Conversational assistants for software development: Integration,
       traceability and coordination. International Conference on Evaluation of Novel Approaches to Software Engineering, 2024.
 [999] Maxime Savary-Leblanc, Lola Burgueño, Jordi Cabot, Xavier Le Pallec, and S. Gérard. Software assistants in software
       engineering: A systematic mapping study. Software, Practice & Experience, 2022.
[1000] C. Tan, Shangxin Guo, M. Wong, and Ching Nam Hang. Copilot for xcode: Exploring ai-assisted programming by
       prompting cloud-based large language models, 2023. URL https://arxiv.org/abs/2307.14349v1.
[1001] Jesús M. González-Barahona. Software development in the age of llms and xr. Ide, 2024.
[1002] Ching Nam Hang, Pei-Duo Yu, Roberto Morabito, and Chee-Wei Tan. Large language models meet next-generation
       networking technologies: A review. Future Internet, 2024.
[1003] D. Bork, Philip Langer, and Tobias Ortmayr. A vision for flexibile glsp-based web modeling tools, 2023. URL
       https://arxiv.org/abs/2307.01352v1.
[1004] Josselin Enet, Erwan Bousse, M. Tisi, and Gerson Sunyé. Protocol-based interactive debugging for domain-specific
       languages. Journal of Object Technology, 2023.
[1005] M. Wong, Shangxin Guo, Ching Nam Hang, Siu-Wai Ho, and C. Tan. Natural language generation and understanding
       of big code for ai-assisted programming: A review. Entropy, 2023.
[1006] Zihao Wu. Autono: A react-based highly robust autonomous agent framework, 2025. URL https://arxiv.org/abs/
       2504.04650v2.
[1007] Fei Lei, Yibo Yang, Wenxiu Sun, and Dahua Lin. Mcpverse: An expansive, real-world benchmark for agentic tool use,
       2025. URL https://arxiv.org/abs/2508.16260v1.
[1008] Narendra Kumar Reddy Choppa and Mark Knipp. The future of seamless generative ai and tool integration: Exploring
       the model context protocol. World Journal of Advanced Engineering Technology and Sciences, 2025.
[1009] Abul Ehtesham, Aditi Singh, Gaurav Kumar Gupta, and Saket Kumar. A survey of agent interoperability protocols:
       Model context protocol (mcp), agent communication protocol (acp), agent-to-agent protocol (a2a), and agent network
       protocol (anp), 2025. URL https://arxiv.org/abs/2505.02279v2.
[1010] M. Ferrag, Norbert Tihanyi, Djallel Hamouda, Leandros A. Maglaras, and Mérouane Debbah. From prompt injections
       to protocol exploits: Threats in llm-powered ai agents workflows, 2025. URL https://arxiv.org/abs/2506.23260v1.
[1011] Peng Ding and Rick Stevens. Unified tool integration for llms: A protocol-agnostic approach to function calling, 2025.
       URL https://arxiv.org/abs/2508.02979v1.
[1012] Dezhang Kong, Shi Lin, Zhenhua Xu, Zhebo Wang, Minghao Li, Yufeng Li, Yilun Zhang, Hujin Peng, Zeyang Sha,
       Yuyuan Li, Changting Lin, Xun Wang, Xuan Liu, Ningyu Zhang, Chao-Jun Chen, Muhammad Khurram Khan, and
       Meng Han. A survey of llm-driven ai agent communication: Protocols, security risks, and defense countermeasures,
       2025. URL https://arxiv.org/abs/2506.19676v3.
[1013] Peng Ding. Toolregistry: A protocol-agnostic tool management library for function-calling llms, 2025. URL https:
       //arxiv.org/abs/2507.10593v1.
[1014] Balaji Rama, Kai Mei, and Yongfeng Zhang. Cerebrum (aios sdk): A platform for agent development, deployment,
       distribution, and discovery. Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for
       Computational Linguistics: Human Language Technologies (System Demonstrations), 2025.
[1015] Yao Fehlis, Charles Crain, Aidan Jensen, Michael Watson, James Juhasz, Paul Mandel, Betty Liu, Shawn Mahon, Daren
       Wilson, Nick Lynch-Jonely, Ben Leedom, and David Fuller. Technical implementation of tippy: Multi-agent architecture
       and system design for drug discovery laboratory automation, 2025. URL https://arxiv.org/abs/2507.17852v1.
[1016] Iacopo Colonnelli, B. Cantalupo, I. Merelli, and Marco Aldinucci. Streamflow: Cross-breeding cloud with hpc. IEEE
       Transactions on Emerging Topics in Computing, 2020.
[1017] Domenico Calcaterra and O. Tomarchio. Policy-based holistic application management with bpmn and tosca. SN
       Computer Science, 2023.




                                                                90
                                  A Survey of Vibe Coding with Large Language Models



[1018] Z. Adhoni and Dayanand Lal Narayan. Improving the interoperability of a function-as-a-service platform using an
       orchestration framework with a cloud-agnostic approach. ETRI Journal, 2024.
[1019] Chiranjit Mitra. Synchronization dynamics of heterogeneous, collaborative multi-agent ai systems, 2025. URL
       https://arxiv.org/abs/2508.12314v1.
[1020] Tianyi Bai, Ling Yang, Zhen Hao Wong, Fupeng Sun, Xinlin Zhuang, Jiahui Peng, Chi Zhang, Lijun Wu, Jiantao
       Qiu, Wentao Zhang, Binhang Yuan, and Conghui He. Efficient pretraining data selection for language models via
       multi-actor collaboration. Annual Meeting of the Association for Computational Linguistics, 2024.
[1021] Bo Ni and Markus J. Buehler. Mechagents: Large language model multi-agent collaborations can solve mechanics
       problems, generate new data, and integrate knowledge, 2023. URL https://arxiv.org/abs/2311.08166v1.
[1022] Diego Gosmar, Deborah A. Dahl, E. Coin, and David Attwater. Ai multi-agent interoperability extension for managing
       multiparty conversations. NL4AI@AI*IA, 2024.
[1023] Hana Derouiche, Zaki Brahmi, and Haithem Mazeni. Agentic ai frameworks: Architectures, protocols, and design
       challenges, 2025. URL https://arxiv.org/abs/2508.10146v1.
[1024] Abdullah M. Almasoud, M. Naeem, Ibrahim Ghaznavi, Muhammad Imran Taj, Imran Hashmi, and Junaid Qadir.
       Harnessing multi-agent llms for complex engineering problem-solving: A framework for senior design projects. IEEE
       Global Engineering Education Conference, 2025.
[1025] Yuyang Cheng, Yumiao Xu, Chaojia Yu, and Yong Zhao. Hawk: A hierarchical workflow framework for multi-agent
       collaboration, 2025. URL https://arxiv.org/abs/2507.04067v1.
[1026] Xinxing Ren, Caelum Forder, Qianbo Zang, Ahsen Tahir, Roman J. Georgio, Suman Deb, Peter Carroll, Ö. Gürcan,
       and Zekun Guo. Anemoi: A semi-centralized multi-agent system based on agent-to-agent communication mcp server
       from coral protocol, 2025. URL https://arxiv.org/abs/2508.17068v2.
[1027] Yexuan Shi, Mingyu Wang, Yunxiang Cao, Hongjie Lai, Junjian Lan, Xin Han, Yu Wang, Jie Geng, Zhenan Li, Zihao
       Xia, Xiang Chen, Chen Li, Jian Xu, Wenbo Duan, and Yuanshuo Zhu. Aime: Towards fully-autonomous multi-agent
       framework, 2025. URL https://arxiv.org/abs/2507.11988v2.
[1028] Yufan Dang, Cheng Qian, Xueheng Luo, Jingru Fan, Zihao Xie, Ruijie Shi, Weize Chen, Cheng Yang, Xiaoyin
       Che, Ye Tian, Xuantang Xiong, Lei Han, Zhiyuan Liu, and Maosong Sun. Multi-agent collaboration via evolving
       orchestration, 2025. URL https://arxiv.org/abs/2505.19591v1.
[1029] N. Nascimento, Paulo Alencar, and Donald D. Cowan. Self-adaptive large language model (llm)-based multiagent
       systems. 2023 IEEE International Conference on Autonomic Computing and Self-Organizing Systems Companion (ACSOS-C),
       2023.
[1030] Rafael Barbarroxa, Bruno Ribeiro, Luis Gomes, and Zita A. Vale. Benchmarking autogen with different large language
       models. Conference on Algebraic Informatics, 2024.
[1031] Chengxuan Xia, Qianye Wu, Sixuan Tian, and Yilun Hao. Parallelism meets adaptiveness: Scalable documents
       understanding in multi-agent llm systems, 2025. URL https://arxiv.org/abs/2507.17061v1.
[1032] Tianyu Xie, Yuhang Wu, Yongdong Luo, Jiayi Ji, and Xiawu Zheng. Training-free multimodal large language model
       orchestration, 2025. URL https://arxiv.org/abs/2508.10016v2.
[1033] Raphael Shu, Nilaksh Das, Michelle Yuan, Monica Sunkara, and Yi Zhang. Towards effective genai multi-agent
       collaboration: Design and evaluation for enterprise applications, 2024. URL https://arxiv.org/abs/2412.05449v1.
[1034] Praneet Sai Madhu Surabhi, Dheeraj Reddy Mudireddy, and Jian Tao. Thinktank: A framework for generalizing
       domain-specific ai agent systems into universal collaborative intelligence platforms, 2025. URL https://arxiv.org/
       abs/2506.02931v1.
[1035] Sujan Dutta, Sayantan Mahinder, Raviteja Anantha, and Bortik Bandyopadhyay. Applying rlaif for code generation
       with api-usage in lightweight llms. arXiv preprint arXiv:2406.20060, 2024.
[1036] Yanlin Wang, Yanli Wang, Daya Guo, Jiachi Chen, Ruikai Zhang, Yuchi Ma, and Zibin Zheng. Rlcoder: Reinforcement
       learning for repository-level code completion. arXiv preprint arXiv:2407.19487, 2024.
[1037] Qingyao Li, Wei Xia, Kounianhua Du, Xinyi Dai, Ruiming Tang, Yasheng Wang, Yong Yu, and Weinan Zhang.
       Rethinkmcts: Refining erroneous thoughts in monte carlo tree search for code generation. arXiv preprint arXiv:2409.09584,
       2024.




                                                              91
                                  A Survey of Vibe Coding with Large Language Models



[1038] Evan Wang, Federico Cassano, Catherine Wu, Yunfeng Bai, Will Song, Vaskar Nath, Ziwen Han, Sean Hendryx,
       Summer Yue, and Hugh Zhang. Planning in natural language improves llm search for code generation. arXiv preprint
       arXiv:2409.03733, 2024.
[1039] Zishun Yu, Yunzhe Tao, Liyu Chen, Tao Sun, and Hongxia Yang. B -coder: Value-based deep reinforcement learning
       for program synthesis. arXiv preprint arXiv:2310.03173, 2023.
[1040] Hanbin Wang, Zhenghao Liu, Shuo Wang, Ganqu Cui, Ning Ding, Zhiyuan Liu, and Ge Yu. Intervenor: Prompting
       the coding ability of large language models with the interactive chain of repair. arXiv preprint arXiv:2311.09868, 2023.
[1041] Binjia Zhou, Hengrui Lou, Lizhe Chen, Haoyuan Li, Dawei Luo, Shuai Chen, Jie Lei, Zunlei Feng, and Yijun Bei.
       Corrdetail: Visual detail enhanced self-correction for face forgery detection. arXiv preprint arXiv:2507.05302, 2025.




                                                              92
