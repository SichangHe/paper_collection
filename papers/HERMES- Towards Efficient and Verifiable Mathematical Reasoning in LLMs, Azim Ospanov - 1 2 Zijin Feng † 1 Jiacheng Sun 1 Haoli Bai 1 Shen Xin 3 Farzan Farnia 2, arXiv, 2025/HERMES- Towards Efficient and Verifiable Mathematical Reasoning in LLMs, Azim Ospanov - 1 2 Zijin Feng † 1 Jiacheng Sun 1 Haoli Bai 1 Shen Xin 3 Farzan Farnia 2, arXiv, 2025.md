                                         HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs


                                                      Azim Ospanov * 1 2 Zijin Feng † 1 Jiacheng Sun 1 Haoli Bai 1 Shen Xin 3 Farzan Farnia 2


                                                                 Abstract                                    1. Introduction
                                              Informal mathematics has been central to modern                In recent years, Large Language Models (LLMs) have
                                              large language model (LLM) reasoning, offering                 achieved remarkable proficiency in mathematical reason-
arXiv:2511.18760v2 [cs.AI] 29 May 2026




                                              flexibility and efficient construction of arguments.           ing (Wei et al., 2022; Kojima et al., 2022; Yu et al., 2023;
                                              However, purely informal reasoning is prone to                 Xu et al., 2024), with some systems even demonstrating the
                                              logical gaps and subtle errors that are difficult              potential to solve Olympiad-level problems (Huang & Yang,
                                              to detect and correct. In contrast, formal theo-               2025). A key advancement driving this progress is the Chain-
                                              rem proving provides rigorous, verifiable mathe-               of-Thought (CoT) approach, which enables LLMs to plan
                                              matical reasoning, where each inference step is                step-by-step reasoning, decompose complex problems into
                                              checked by a trusted compiler, but lacks the ex-               sub-goals, generate intermediate reasoning steps, and itera-
                                              ploratory freedom of informal problem-solving.                 tively assess and correct them. However, long CoTs remain
                                              This mismatch leaves current LLM-based math                    susceptible to logical leaps, subtle errors, and hallucinations,
                                              agents without a principled way to combine the                 stemming from incomplete domain knowledge, imprecise
                                              strengths of both paradigms. In this work, we                  reasoning, or the accumulation of small mistakes over mul-
                                              introduce Hermes, the first tool-assisted agent                tiple steps (Huang et al., 2025; Lu et al., 2025; Akbar et al.,
                                              that explicitly interleaves informal reasoning with            2024). These issues could lead to unstable reasoning and
                                              formally verified proofs in Lean. The frame-                   degraded performance, and when uncertain, LLMs may pro-
                                              work performs intermediate formal checking to                  duce overly long or repetitive reasoning traces, increasing
                                              prevent reasoning drift and a memory module                    token usage without necessarily improving correctness.
                                              for proof continuity across multi-step reasoning               To address these limitations, researchers have proposed Pro-
                                              chains, enabling both exploration and verifica-                cess Reward Models (PRMs) and Outcome Reward Models
                                              tion. We evaluate Hermes on four challenging                   (ORMs)(Lightman et al., 2024; Wang et al., 2024b), which
                                              mathematical reasoning benchmarks using LLMs                   aim to guide LLM reasoning toward correctness by scoring
                                              of varying parameter scales, from small models                 intermediate reasoning steps or final solutions. Specifically,
                                              to state-of-the-art systems. Across all settings,              PRMs assign a score at each reasoning step, rewarding local
                                              Hermes reliably improves the reasoning accu-                   correctness, while an ORMs provide a single scalar reflect-
                                              racy of base models while substantially reduc-                 ing overall solution quality. While these models can improve
                                              ing reasoning token usage and computational cost               reasoning performance, they function largely as black-box
                                              compared to reward-based approaches. On dif-                   evaluators that assign numerical scores without explaining
                                              ficult datasets such as AIME and HARDMath2,                    why a reasoning trajectory is valid or flawed, offering lim-
                                              Hermes@1 achieves up to a 40% accuracy im-                     ited interpretability and no explicit verification of mathemat-
                                              provement while using 80% fewer total inference                ical correctness (She et al., 2025). Moreover, their training
                                              FLOPs. When scaled at test time, Hermes@5                      requires substantial human curation (Huang et al., 2025),
                                              boosts accuracy further by 20%. The implementa-                and automated supervision methods introduce noise by in-
                                              tion and codebase are publicly available at https:             ferring step correctness labels from final answers (Zhang
                                              //github.com/aziksh-ospanov/HERMES.                            et al., 2025b), leading to misalignment with true stepwise
                                                                                                             correctness. Ultimately, because both PRMs and ORMs rely
                                             1
                                               Huawei Foundation Model Department 2 Department of Com-       on LLMs as evaluative backbone, their reward signals in-
                                         puter Science & Engineering, The Chinese University of Hong         herit the stochasticity, biases, and instability of LLM-based
                                         Kong 3 Celia Team. * First Author, aospanov9@cse.cuhk.edu.hk.       judgment (Shao et al., 2024).
                                         †
                                           Corresponding Author, fengzijinn@gmail.com.
                                                                                                             In parallel to these, another line of work has focused on
                                         Proceedings of the 43 rd International Conference on Machine        formal theorem proving, which relies on proof assistants
                                         Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026        with trusted kernels such as Lean4 (Moura & Ullrich, 2021),
                                         by the author(s).

                                                                                                         1
                         HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

                                                   Lean-Driven Tool Agent Framework: Hermes
 Problem

                   Reasoning LLM        Candidate         Formalization Module         Prover Module            Feedback Module
                                          step

                                         context




 Answer                                 Candidate
                                          step

                                         context

                                          verified




Figure 1. Overview of Hermes framework. Hermes is a Lean4-driven, multi-modular reasoning agent integrating LLM reasoning with
formal verification for reliable mathematical problem solving. It comprises four modules: an LLM that generates reasoning steps, a
formalizer that formalizes these steps into Lean code, a prover that symbolically verifies their correctness, and a feedback module that
returns verification signals for subsequent reasoning. This design enables iterative reasoning with improved correctness and efficiency.

Coq (Bertot & Castéran, 2013), and Isabelle (Nipkow et al.,                 • We develop the first tool-based Lean4 reasoning agent
2002). These systems enforce rigorous formal, machine-                        that verifies feasible intermediate proof steps during
checkable reasoning, in contrast to the informal reasoning of                 inference, providing LLMs with kernel-based correct-
traditional mathematics expressed in natural language. Re-                    ness signals for mathematical reasoning.
cently, formal language-based systems such as AlphaProof
and AlphaGeometry (Yang et al., 2025; Google DeepMind,                      • We introduce a Lean4-powered memory block that
2024; Trinh et al., 2024) have achieved remarkable success                    accumulates and validates intermediate claims in con-
on International Mathematical Olympiad (IMO) problems,                        text, ensuring cross-step consistency and reducing the
rivaling top human performers. Their principal strength                       propagation of errors in long reasoning chains.
lies in verifiability and immunity to hallucinations, as for-
                                                                            • Hermes improves average accuracy by 23% across four
mal verification is embedded directly into the proof search
                                                                              benchmarks, notably achieving 40% higher accuracy
process, ensuring that inference is rigorously justified.
                                                                              on AIME’25 with 80% less compute. We demonstrate
Inspired by the strengths of both paradigms, in this work,                    scalability by showing additional performance gains
we bridge the gap between formal and informal mathemat-                       when integrating Hermes with Best-of-N sampling.
ics by combining the verifiability of formal reasoning with
the flexibility and expressiveness of LLM-based informal                 2. Related Works
reasoning. We introduce Hermes, a multi-modular scalable
tool-augmented agent (abbreviated from "Hybrid AgEnt for                 Automatic Theorem Proving. Recent LLM-based
Reasoning in Mathematics with NEuro-Symbolic Lean4                       provers have achieved remarkable advances in formal
verification"), designed to integrate formal verification into           reasoning within Lean4. Goedel-Prover-V2 (Lin et al.,
the LLM reasoning process. Hermes leverages modern                       2025b) introduces large-scale, verifier-guided training with
LLMs’ tool-calling capability to verify individual reason-               scaffolded data synthesis to achieve state-of-the-art accu-
ing steps during inference and builds a memory block that                racy on MiniF2F and PutnamBench. Kimina-Prover (Wang
ensures continuity of proof claims. For each critical proof              et al., 2025b;a) emphasizes structured reasoning patterns
step, the agent formalizes the natural-language statement                and reinforcement learning to improve sample efficiency.
into Lean goal, verifies formalization consistency through               DeepSeek-Prover-V2 (Xin et al., 2025) focuses on subgoal
back-formalization, and invokes a prover module to attempt               decomposition, using hierarchical reasoning to bridge
a proof or counter-proof. The resulting formal signal is then            informal and formal proofs. Seed-Prover (Chen et al.,
fed back into the LLM to inform its next reasoning step. The             2025) advances lemma-style reasoning and multi-tier
overview of our agentic framework is illustrated in Figure 1.            inference, achieving competition-level results on IMO and
We show that incorporating Hermes significantly enhances                 Putnam benchmarks. Collectively, these systems highlight
LLM accuracy across mathematical reasoning benchmarks                    a substantial body of work on automated theorem proving.
of varying difficulty. It reduces token usage compared to
                                                                         Autoformalization. Recent work in autoformalization,
traditional score-based methods and provides interpretable,
                                                                         translating informal mathematical statements into for-
step-level correctness feedback, offering transparency into
                                                                         mal statements, has made rapid advancements. For
how reasoning paths evolve and why certain trajectories lead
                                                                         example, Goedel-Autoformalizer (Lin et al., 2025b)
to valid conclusions while others result in hallucinations.
                                                                         built a dataset of 1.64 million formal statements from
Our contributions are as follows:
                                                                         natural-language problems in Lean4 and used this to
                                                                         train a high-performing autoformalizer model. Mean-

                                                                     2
                        HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

while, Mathesis-Autoformalizer (Yu et al., 2025) in-                 Neurosymbolic Solvers and LLMs. Recent work has
troduces a reinforcement-learning framework with a                   advanced neuro-symbolic reasoning by integrating LLMs
novel "LeanScorer" for assessment, and shows accu-                   with formal logic and theorem proving. LogicLM (Pan
racy gains on the Gaokao-Formal benchmark. The                       et al., 2023) and LogicLM++ (Kirtania et al., 2024) trans-
Kimina-Autoformalizer (Wang et al., 2025b;a) similarly               late natural-language problems into symbolic form and iter-
converts natural-language problems into Lean4 statements             atively refine them for solver-based verification. DSP (Jiang
via a fine-tuned LLM and expert iteration. Finally,                  et al., 2023) and DSP+ (Cao et al., 2025) bridge informal
HERALD-Translator (Gao et al., 2025a) provides a large               reasoning and formal proofs through a draft–sketch–prove
annotated Lean4 corpus (≈580K statements) by back-                   pipeline. Lean-STaR (Lin et al., 2025a) enhances formal
translating parts of Mathlib and demonstrates high accuracy          reasoning by interleaving natural-language rationales with
in miniF2F (Zheng et al., 2022) benchmark. According to              Lean tactics, while DTV (Zhou et al., 2023) explores deter-
previous research efforts, the current generation of formal-         ministic verifier-guided reasoning. Collectively, these meth-
ization models are capable of translating informal statements        ods demonstrate the effectiveness of hybrid LLM–symbolic
to formal goals with syntactic and semantic correctness.             approaches for logical and mathematical reasoning.

LLM collaboration with external experts. Another                     3. Problem Formulation
prominent line of research focuses on using external feed-
back to guide LLMs toward producing correct responses.               We consider verifiable mathematical problem solving in
Specifically, APOLLO (Ospanov et al., 2025) proposed                 natural language. Given a problem p, a language model
a model-agnostic proof-repair framework that enhances                produces a sequence of T intermediate reasoning steps
sample efficiency and reliability without increasing model           S = (s0 , s1 , · · · , sT ), where each step st is a natural-
size. (Ringer, 2021) introduced a Coq compiler-based repair          language mathematical claim. Reasoning proceeds autore-
agent that adapts to changes in the underlying definitions.          gressively, with each step conditioned on the previous con-
Moreover, (Jiang et al., 2022) show that combining the               text. A subset of steps, informally termed critical proof
strengths of built-in solvers (e.g., Sledgehammer in Isabelle,       steps, are those whose correctness is essential for the va-
built-in tactics in Lean) with LLMs leads to performance             lidity of the final solution. We assume access to a formal
gains. (First et al., 2023; Wang et al., 2025a; Lin et al.,          verification mechanism that can be applied to a selected
2025b; Yousefzadeh et al., 2025) report that incorporating           subset of such steps, denoted by S̃ ⊆ S, with typically
compiler feedback encourages LLMs to adapt and correct               |S̃| ≤ T .
previously generated proofs. This behavior is observed in            The objective is to design an inference-time reasoning
general-purpose models but can be further amplified by ap-           method that leverages formal theorem proving to improve
pending compiler feedback during the fine-tuning stage for           step-level correctness and overall reasoning efficiency, while
dedicated theorem proving LLMs.                                      preserving the exploratory flexibility of language-based rea-
                                                                     soning, ultimately producing a correct answer to p.
Enhanced Reasoning Techniques. To further advance
LLM reasoning, score-based models have emerged that eval-
uate the chain of thought produced by reasoning models.
                                                                     4. Our Approach
The goal is to identify and prioritize the most effective            In this section, we describe Hermes, our framework for a
reasoning traces. Two main approaches exist: Outcome Re-             verifiable and interpretable tool-based agent for mathemati-
ward Models (ORMs), which assess only the final answer,              cal reasoning. Hermes is designed to be split into multiple
and Process Reward Models (PRMs), which score reason-                swappable modules that analyze intermediate proof steps
ing steps sequentially. (Lightman et al., 2024; Wang et al.,         and produce proper verification for each mathematical step.
2024b) Furthermore, Safe (Liu et al., 2025) proposed train-          Figure 2 illustrates the complete agent pipeline, including
ing a small LSTM reward model based on Lean4 verified                intermediate proof transformations after each module. At
reasoning traces. Another line of work focuses on tool-based         the core of our agent lies the tool-calling capability of mod-
agents that equip LLMs with more complex functionality               ern LLMs, which allows the model to pause generation and
and the ability to query and verify their own outputs. Numer-        query external agents to verify reasoning steps or retrieve
ous studies have shown that teaching LLMs to use specific            additional context. In our design, the LLM is instructed to
tools enhances their performance on given tasks (Qu et al.,          verify every critical math step contributing to the final proof.
2025; Qin et al., 2023), including reasoning. (Gao et al.,
2025b) introduced Chain-of-Abstraction to better leverage            Our Lean backend of choice is the Lean4 REPL (Lean FRO,
tools in multi-step reasoning, while (Ning et al., 2024) ex-         2023), which provides compatibility with Python-based
amined the importance of using tools in the right scenarios          tool integration. We also employ the verification scheduler,
to improve reasoning in LLMs.                                        which parallelizes Lean code verification for faster inference.

                                                                 3
                                   HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

   Hermes Agent                                      #1                                Formalization Module                                                                  #2
                                   Complete the                                                                                                       import Mathlib
                                                                                              repeat up to Kf times
                                   square: x² + y² - 80x -
                                   100y + 4100 = (x - 40)²                                                  Lean4 compiler                            theorem test (x y :
                                                                            autoformalizer model                                backtranslator
                                   + (y - 50)²                                                                                                        ℝ) : x^2+y^2-
                                                                                                                                                      80*x100*y+4100 =
                invoke the agent                                 +                                                                                    (x-40)^2+(y-50)^2
                                                                                                                                                      := by sorry
Reasoning LLM




                                    Informal proof step                                                                                                 Formal Lean4 proof step


                                                          Feedback Module                                                       #3                    Prover Module
                                                                                                           import Mathlib
                                                                                                                                                     repeat up to Kp times
                                                                                        no
                                                                                                           theorem test (x y :                   Lean4 compiler
                             ?                                                      Verified by            ℝ) : x^2+y^2-
                                                                                                                                                                     prover model
                                       self-verify the step    unverified           Compiler?              80*x100*y+4100 =                                        goal           ¬goal
                                                                                        yes                (x-40)^2+(y-50)^2
                                     revise your reasoning    ¬goal ↦ True
                                                                                                           := by linarith
                                    proceed with generation goal ↦ True
                                                                                                             Formal Lean4 proof code


                                                    Figure 2. Full Hermes framework with illustrative examples.

The REPL validates proofs generated by the prover mod-                                             selection theorem provers, is compatible with our agent.
ule, returning a simple True/False signal that indicates                                           This module attempts two proofs in parallel: the original
the correctness of the intermediate proof step. Additionally,                                      goal and its negation, ¬goal. The objective is to either
our memory block uses embedding-based top-k retrieval of                                           prove the original statement or derive a counter-proof (e.g.,
the most relevant contextual information. The following                                            a counterexample) to demonstrate the invalidity of the step.
subsections describe each Hermes module in detail.                                                 Similar to the formalization module, the prover operates
                                                                                                   under a sampling budget controlled by the parameter Kp .
4.1. Formalization Module                                                                          We observe that increasing Kp improves performance but
The formalization module is responsible for accurately for-                                        incurs additional inference cost, as the prover must explore
malizing each proof step expressed in natural language into                                        more proof attempts before reaching a conclusion. Once the
its equivalent Lean4 statement. At this stage, we employ a                                         prover finds a proof or counter-proof, it returns this verifica-
dedicated Lean autoformalizer model that generates a Lean                                          tion signal to the LLM to guide the subsequent reasoning
statement corresponding to the informal proof step, insert-                                        chain. This module is highlighted in blue in Figure 2.
ing a sorry placeholder. To ensure the correctness and
                                                                                                   4.3. Memory Block
semantic relevance of the formalization, we apply two-step
verification. First, the formalized statement must success-                                        Memory block is responsible for collecting all validated
fully compile in Lean. This verification guarantees that the                                       proof steps in a structured database. Each proof step is
prover module is provided with valid code, and well-defined                                        stored alongside its vector representation to enable fast,
premises and goals. Second, the validated Lean code is back-                                       similarity-based retrieval. Because some problems in-
formalized into informal language, and the LLM evaluates                                           volve long chains of thought (CoT) with branching, non-
the equivalence between the original and back-formalized                                           overlapping reasoning paths, we implement a top-k retrieval
proof steps. If the two are deemed equivalent, the formal-                                         mechanism to select the most relevant memories for the cur-
ization module forwards the Lean statement to the prover                                           rently evaluated proof step. Furthermore, to maintain proof
module. The number of attempts to obtain a valid formal-                                           continuity and prevent the model from pursuing irrelevant or
ization is controlled by the parameter Kf , which defines                                          disjoint reasoning paths, the retrieved memories are passed
the formalization budget. A higherKf typically yields more                                         as additional context to the formalization module. These are
accurate formalizations but may increase the agent’s run-                                          incorporated into the formalized Lean statement as prelimi-
time. This hyperparameter is user-controlled. This module                                          nary hypotheses, ensuring logical consistency across proof
is highlighted in orange in Figure 2.                                                              steps. The memory block corresponds to the "database"
                                                                                                   icon in Figure 2.
4.2. Prover Module
                                                                                                   4.4. Lean4 REPL Feedback
The prover module receives a valid Lean statement and
attempts to find a corresponding proof within Lean. At                                             Our agent returns one of three states: (1) proof succeeded,
this stage, we incorporate a whole-proof generation model                                          (2) counter-proof found, or (3) verification failed. The first
together with built-in Lean solvers; however, any proof-                                           two states drive the next-generation strategy: the LLM ei-
generation method, such as tree-based provers or premise-                                          ther revises its reasoning when hallucination is detected or


                                                                                              4
                        HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

continues exploring already-verified steps. The third state           Each verification executes K attempts, with K is compa-
arises when the autoformalizer fails to produce a valid for-          rable to that used in ORM and PRM. Consequently, the
malization, or the prover cannot prove/disprove the goal.             complexity of Hermes is O(T̃ KN 2 ), yielding the ordering
The design is compatible with any autoformalizer–prover
pairing, so as research progresses, stronger components can           OORM (KN 2 ) ≤ OHermes (T̃ KN 2 ) ≤ OP RM (T KN 2 )
be swapped in seamlessly. This flexibility ensures the de-            This analysis shows that Hermes is theoretically no more
sign remains relevant for non-mathematical applications and           expensive than PRM. Empirically, Hermes achieves much
verification environments beyond Lean4. Given feedback,               higher accuracy, indicating superior overall effectiveness
the LLM then chooses to (1) continue exploring the current            and token-efficiency.
line of reasoning, (2) attempt an alternative approach, or (3)
proceed cautiously and self-verify reasoning, since the step
did not pass the Lean4 compiler.                                      5. Experiments

4.5. Complexity Analysis                                              5.1. Experimental Setup

In this section, we analyze the token-level inference com-            Hermes setup. For Hermes evaluation, we set both Kp
plexity of Hermes and compare it with standard CoT and                and Kf to 4, which strikes a good balance between in-
reward-model–based baselines (ORM and PRM). We show                   ference speed and downstream Lean verification accuracy.
that Hermes is theoretically no more expensive than PRM               Lean timeout is set to 60 seconds. The memory module se-
and lies between ORM and PRM in complexity.                           lects the top three recorded steps as context. The prover of
                                                                      choice is Goedel-Prover-V2-8B (Lin et al., 2025b) and the
Theorem 4.1. Consider a reasoning process that gener-                 autoformalizer model is Goedel-Autoformalizer-8B (Lin
ates a total of N reasoning tokens. Suppose verification              et al., 2025b), unless stated otherwise. Chosen embed-
is performed at T reasoning steps, and that each verifi-              ding model for the memory block is Qwen3-Embedding-
cation invocation executes K independent attempts. Let                0.6B (Zhang et al., 2025a). To ensure consistency with the
nf , np denote the average number of tokens generate per              Goedel-Autoformalizer and Goedel-Prover training data, we
attempt by the formalizer and prover, respectively. Then              utilize Lean version v4.9.0.
the overall token-level inference complexity of the reason-
ing–verification process is O(N 2 + KT N 2 ).                         Baseline methods. We compare our approach against
                                                                      several strong baselines, with Safe (Liu et al., 2025) serv-
Proof. The total token complexity consists of a reasoning
                                                                      ing as the previous state-of-the-art method. We further
cost and a verification cost. For reasoning, under standard
                                                                      introduce Safe*, an improved variant that replaces the
autoregressive decoding for a Transformer, generating the
                                                                      prover and autoformalizer in Safe with more advanced
i-th token incurs an incremental cost O(i) proportional to
                                                                      model Goedel-Prover-V2 (Lin et al., 2025b) and Goedel-
                          PN over all N tokens yields a
the context length. Summing
                                                                      Autoformalizer (Lin et al., 2025b) to match our Hermes
total reasoning cost of i=1 O(i) = O(N 2 ). For veri-
                                                                      setup. In addition, we include CoT, a zero-shot chain-
fication, at each of the T steps, the formalizer generates
                                                                      of-thought baseline, and Majority vote, which selects the
candidate formalized statements and the prover attempts
                                                                      most frequent answer from five sampled reasoning traces.
corresponding proofs. Each action takes K formaliza-
                                                                      We also include a range of outcome and process reward
tion–proving attempts. The per-step verification cost is
                                                                      models. The outcome reward models include Skywork-
thus O(K(n2f + n2p )). Summing over T steps yields a total
                                                                      Reward-Llama-3.1-8Bv0.2 (Liu et al., 2024) and ArmoRM-
verification cost of O(KT (n2f + n2p )) = O(KT N 2 ). Thus,           Llama3-8Bv0.1 (Wang et al., 2024a), while the process re-
the total complexity of the process is O(N 2 + KT N 2 ).              ward models include math-shepherd-mistral-7b-prm (Wang
                                                                      et al., 2024b) and RLHFlow/Llama3.1-8B-PRMDeepseek-
Theorem 4.1 provides a unified characterization of token              Data (Dong et al., 2024). The experiments are conducted
complxity across different methods. For CoT reasoning,                on numerous base models: Qwen3-8B (Team, 2025) and
no verification is performed and the complexity reduces               OpenAI o3-mini (OpenAI, 2025) in "thinking mode" and
to O(N 2 ). For ORM- and PRM-based methods, K candi-                  DeepSeek-V3.1 (et al., 2025) and V3.2 (DeepSeek-AI et al.,
date reasoning traces are first generated before verification.        2025) in "non-thinking" mode. We selected strong models
ORM-based methods apply outcome-level verification once               from both generation styles to assess our agent’s compati-
per trace (T = 1), leading to O(KN 2 ) complexity. PRM-               bility with mainstream LLMs.
based methods perform verification at every step, leading
to O(T KN 2 ). In contrast, Hermes differs by generating a            Datasets and evaluation. We conduct experiments on
single reasoning trace and interleaving verification during in-       four widely used math benchmarks: MATH-500 (Lightman
ference. In practice, verification is applied at a small subset       et al., 2023), AIME’25 (Competitions & of Problem Solv-
of critical steps, whose number is denoted by T̃ and T̃ ≪ T .         ing, 2025), CollegeMath (Tang et al., 2024), and HARD-

                                                                  5
                         HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

Table 1. Accuracy (%) of different reasoning models under four inference strategies: zero-shot CoT (@1), majority vote (@5), reward-
model selection (Best-of-5), and Hermes (@1). Results are reported on four benchmarks: MATH500 (MATH), AIME’25 (AIME),
CollegeMath (CM), and HARDMath2 (HM2). The best and second-best results are bolded and underlined, respectively.

                                    Qwen3-8B                          OpenAI o3-mini                     DeepSeek-V3.2
                          MATH      AIME      CM     HM2     MATH       AIME     CM     HM2      MATH      AIME     CM      HM2
 CoT@1                     84.8      20.0    69.1     4.3     95.8       63.3    75.2    23.2     95.8      50.0    79.8    25.6
 CoT@5+Majority            87.0      16.7    70.3     4.7     96.8       70.0    76.0    22.7     97.6      60.0    80.8    26.1
 CoT@5+Skywork             91.0      30.0    72.0     5.7     96.8       83.3    76.1    29.4     97.4      53.3    80.4    30.8
 CoT@5+ArmoRM              88.6      30.0    72.4     5.2     96.2       76.7    76.1    28.4     97.2      53.3    80.3    28.4
 CoT@5+Shepherd            87.8      23.3    70.2     5.7     96.4       80.0    75.7    25.6     97.0      60.0    80.4    27.8
 CoT@5+RLHFlow             84.0      20.0    69.4     5.7     95.8       70.0    75.9    28.4     97.2      60.0    80.3    24.6
 Lean-based methods
 CoT@5+Safe                89.4      23.3    72.4     5.7     96.0       83.3    75.7    26.1     96.2      56.7    80.0    28.9
 CoT@5+Safe*               89.4      23.3    72.5     6.2     96.8       83.3    75.8    25.6     96.6      60.0    80.1    30.3
 Hermes@1                  91.2      30.0    73.0     6.6     97.2       86.7    78.9    31.3     98.4      70.0    83.3    33.6
 Hermes@5+Majority         93.0      33.3    75.8    7.6      97.0       86.7    79.4    31.8     98.6      76.7    85.2    35.1
 Hermes@5+Skywork          94.6      43.3    77.4    10.0     97.0       86.7    79.2    31.3     98.2      80.0    84.0    36.5


Math2 (Roggeveen et al., 2025). For brevity, we refer                more effective integration of neural reasoning and sym-
to them as MATH, AIME, CM, and HM2, respectively,                    bolic verification. We also observe that on more challeng-
throughout the experiments. Each problem has a 15-minute             ing datasets, Hermes achieves the largest relative improve-
time limit and an 8,192-token budget (prompt + generation).          ments. For instance, on the harder dataset HM2, Deepseek-
All Hermes accuracy reports are @1, i.e., the reasoning              V3.2+Hermes improves performance by 31.5%, whereas
models were given only one attempt per problem. For score-           on the easier MATH dataset, the gain is only 2.7% com-
based methods, we evaluate each problem with N generated             pared to CoT. This suggests that Hermes is particularly
candidates (CoTs) and report Best-of-N (BoN). BoN accu-              effective at correcting errors in settings that require more
racy is computed based on the reasoning trace selected by            advanced mathematical reasoning. Moreover, we experi-
the reward model from the N candidates. Unless stated                mented with combining Hermes with a reward model. Sim-
otherwise, N is set to 5 reasoning traces, consistent with the       ilar to CoT@5+Skywork, we sampled 5 reasoning traces
configuration adopted in Safe (Liu et al., 2025).                    produced by Hermes and applied BoN selection using Sky-
                                                                     work. The results are shown in the last row of Table 1.
5.2. Performance of Hermes against base LLMs and                     When combined with a reward model, the final accuracy
     reward-based generation                                         increased by 10.8% on average compared to Hermes@1.
                                                                     Since Hermes produces a standard chain-of-thought, it re-
Table 1 reports the accuracy of eight baseline inference
                                                                     mains compatible with previously developed reasoning trace
methods and our proposed Hermes across three reasoning
                                                                     methods.
models and four benchmark datasets, with each method
evaluated on every combination of model and dataset. We
                                                                     5.3. Token budgets and generation efficiency
selected representative reasoning models from three distinct
parameter scales: a sub-10B model (Qwen3-8B), a medium-              As shown in Figure 3, our evaluation indicates that the
sized model (o3-mini), and a large model (DeepSeek-V3.2),            reasoning token budget of Hermes is comparable to that of
each from a distinct provider. Compared with non–Lean-               zero-shot chain-of-thought, while being 4–6 times lower
based methods, Hermes consistently outperforms all base-             than score-based methods such as Safe, ORMs, and PRMs.
lines across models and benchmarks, except on the AIME               These results demonstrate that incorporating intermediate,
benchmark with Qwen3-8B, where Skywork and ArmoRM                    verifiable feedback not only improves accuracy across a
achieve comparable performance. Specifically, averaged               range of benchmarks but also significantly reduces token
across all reasoning models and benchmarks, Hermes sur-              budgets compared to BoN reasoning trace selection.
passes zero-shot CoT, Majority vote, ORM-based Skywork
                                                                     To further investigate the performance of score-based meth-
and ArmoRM, and PRM-based Shepherd and RLHFlow
                                                                     ods, we conducted an additional experiment in which we
methods by 23.4%, 23.9%, 5.7%, 8%, 12.2%, and 14.9%,
                                                                     increased the number of sampled reasoning traces from 1
respectively. Compared with the Lean-based baselines Safe
                                                                     (zero-shot chain-of-thought) to 60. Figure 4 reports BoN
and Safe*, Hermes achieves consistently higher accuracy
                                                                     accuracy across four inference methods: Safe, Safe*, math-
across all benchmarks, exceeding them by an average of
                                                                     shepherd-mistral-7b-prm, and ArmoRM-Llama3-8Bv0.1.
10.3% and 8.5%, respectively. This demonstrates Hermes’s

                                                                 6
                                                 HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

                             [@1] ZS-CoT
                             [@1] Hermes                                                                  that reward-based BoN is more effective when the quality




                                                                                              K
                                                                                            .5K
                                                      .4K
                                                    38 K




                                                                                            40
                  40000




                                                     .8
                             [@5] ORM/PRM/Safe




                                                                                          38
                                                   37
                             [@5] Hermes                                                                  of reasoning traces exhibits higher variance, as is the case
                                                                                                          for smaller models such as Qwen3-8B.
   Token Budget


                  30000


                                 .2K                                                                      5.4. Computational Efficiency Analysis




                                                                       .8K
                  20000
                               18




                                                                     17
                                     .5K




                                                                           .7K
                                   12

                                                                                                          Following the methodology of (Kaplan et al., 2020), we




                                                                         10
                  10000




                                                                                    K
                                               K
                                              K




                                                                                 7.7
                                           7.7




                                                                                 8K
                                           7.5
                                                                                                          further examine the computational efficiency of Hermes in
                               K




                                                                     K
                            3.6




                                                                  3.6
                             K




                                                                   K
                          2.5




                                                                2.1
                     0
                              MATH               AIME'25          CollegeMath          HardMath2          comparison to CoT and reward-based approaches. Because
                                                           Dataset
                                                                                                          our agent requires communication among the reasoning,
                                             (a) Qwen3-8B                                                 formalization, and prover models, we estimate the total
                                                                                                          computational cost in terms of FLOPs for two represen-
                  35000      [@1] ZS-CoT                                                                  tative models: Qwen3-8B and DeepSeek-V3.1. OpenAI
                             [@1] Hermes
                                                          .1K
                                                       32




                  30000      [@5] ORM/PRM/Safe                                                            o3-mini is excluded from this analysis, as its architecture


                                                                                                .6K
                             [@5] Hermes
                                                     .8K




                                                                                              27
                                                                                                          and parameter count are not publicly available. We ap-
                                                   26




                                                                                            .2K
                  25000
   Token Budget




                                                                                         23               proximate the FLOP budget using the formula Cf orward =
                  20000
                                                                                                          2N + 2nlayer nctx dattn , where N denotes the number of
                  15000
                                                                                                          model parameters, nlayer the number of layers, nctx the
                  10000
                                       K




                                                                                                          input context length (set to the maximum of 8,192 tokens
                                                 K
                                   7.1




                                                                             K
                                             6.9




                                                                                        K
                                               K




                                                                          6.3



                                                                                   5.9
                                           5.9
                                   K




                                                                           K



                                                                                     K
                               5.1




                                                                       4.7



                                                                                 4.7




                  5000
                                                                                                          in our experiments), and dattn the dimensionality of the
                             K




                                                                     K
                           1.5




                                                                 1.3
                                                                   2
                          1K




                                                                94




                     0
                              MATH               AIME'25          CollegeMath          HardMath2          attention output. Values for N , nlayer , and dattn were de-
                                                           Dataset
                                                                                                          rived from each model’s configuration files. As shown in
                                           (b) OpenAI o3-mini                                             Figure 5, even after accounting for the additional compu-
                                                                                                          tation required by the Hermes agent, its total cost remains
                 30000       [@1] ZS-CoT                                                                  comparable to zero-shot CoT and substantially lower than
                             [@1] Hermes
                                                        .4K
                                                      27




                 25000
                             [@5] ORM/PRM/Safe                                                            that of reward-based models. These results demonstrate
                             [@5] Hermes
                                                                                              .4K




                                                                                                          that, despite involving external formalization and theorem-
                                                                                             21
  Token Budget




                 20000
                                                                                                          proving modules, Hermes maintains strong computational
                                                    .6K
                                                  15




                                                                                          .6K




                 15000
                                                                                                          efficiency and effective resource utilization.
                                                                                         13




                 10000
                                                 K
                                             6.9




                                                                                                          5.5. Ablation studies on different Hermes modules
                                     K




                                                                           K



                                                                                        K
                                 5.5




                                                                         5.3



                                                                                   4.9
                                  K




                  5000
                              4.1



                                            K




                                                                                  K
                                           3.3




                                                                      3K


                                                                                 2.7
                              K




                                                                     K
                             3
                          1.1




                                                                 1.1
                                                                   3
                          82




                                                                60




                     0
                              MATH               AIME'25         CollegeMath       HardMath2
                                                                                                          Recalling Section 4, Hermes is designed as a multi-modular
                                                           Dataset                                        agent. In this section, we conduct an ablation study to eval-
                                           (c) DeepSeek-V3.2                                              uate the contribution of its two key modules: the memory
                                                                                                          buffer and the prover module. The formalization and feed-
Figure 3. Average reasoning token usage per problem on                                                    back modules are not ablated, as they serve as essential
MATH500, AIME’25, CollegeMath, and HardMath2 under Zero-                                                  intermediaries bridging informal and formal mathematical
Shot Chain-of-Thought, Hermes, and Reward-based Best-of-5
settings.                                                                                                 reasoning. When ablating the memory buffer, Hermes no
                                                                                                          longer stores intermediate proof steps, preventing both the
                                                                                                          formalization module and prover module from accessing
Hermes is fixed at @1 and is shown as a dashed green line.
                                                                                                          previously validated information necessary for maintaining
Using DeepSeek-V3.1 as the base reasoning model, we
                                                                                                          coherent reasoning across steps. When ablating the prover
observe that scaling N does not yield significant gains in
                                                                                                          module, the agent omits a query to the dedicated prover
accuracy. All reward-based methods underperform com-
                                                                                                          model and instead relies solely on the built-in Lean solvers,
pared to Hermes, while consuming a linearly increasing
                                                                                                          similar to the AutoSolver module in (Ospanov et al., 2025).
number of tokens. This suggests that, rather than repeatedly
regenerating reasoning traces, it is more effective to incor-                                             Table 2 presents ablation results on MATH and AIME using
porate higher-quality intermediate verification and guidance                                              DeepSeek-V3.1. Removing the prover causes the largest
mechanisms that enhance reasoning quality without incur-                                                  performance drop (e.g., 66.7% → 50.0% on AIME) due to
ring additional token costs. On the other hand, the same                                                  less capable proof search engine, while emoving the mem-
experiment on Qwen3-8B shows that reward-based models                                                     ory buffer disrupts reasoning continuity. Notably, the harder
can outperform Hermes when given a sufficiently large to-                                                 AIME benchmark is far more sensitive to these ablations
ken budget. We observe that for n ≥ 20, both Safe* and                                                    than MATH (25.0% vs. 4.5% relative drop), as its longer
ArmoRM exceed 92% accuracy; however, they consume                                                         reasoning chains amplify error propagation. These results
roughly 28 times more tokens than Hermes. We hypothesize                                                  indicate that the advantages of Hermes’s modular design be-

                                                                                                      7
                                                                    HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs


                               97.5
                                                                          DeepSeek-V3.1                                                                                                                      Qwen3-8B
                                                                                                                                                           94
    MATH500 Accuracy (%)




                                                                                                                                    MATH500 Accuracy (%)
                               97.0
                                                                                                                                                           92
                               96.5               Safe                                                                                                                              Safe
                                                  Safe*                                                                                                    90                       Safe*
                               96.0               ArmoRM                                                                                                                            ArmoRM
                               95.5
                                                  Shepherd                                                                                                 88                       Shepherd
                                                  Majority@N                                                                                               86
                                                                                                                                                                                    Majority@N
                               95.0               Hermes                                                                                                                            Hermes
                                            1     5     10     15    20    25       30   35   40       45    50    55     60                                                   1    5   10     15    20     25    30     35     40    45    50     55    60
                                                             Number of sampled reasoning traces (N)                                                                                          Number of sampled reasoning traces (N)

                                      695       3.9K   7.1K 10.3K 13.5K 16.7K 19.9K 23.1K 26.3K 29.6K 32.8K             36K 39.1K                                          3.6K 18.2K 36.3K 54.6K 72.7K 90.9K 109.2K 127.4K 145.5K 163.5K 181.8K 200K 218K
                                                Corresponding Token Count for Reward-based BoN methods                                                                             Corresponding Token Count for Reward-based BoN methods
                                                                    (a) DeepSeek-V3.1                                                                                                                 (b) Qwen3-8B

Figure 4. Scaling behavior of BoN across ORM, PRM, Safe and Majority vote. The green dashed line indicates Hermes performance at
@1. The corresponding token consumption for each BoN is shown below as a one-dimensional heatmap.

                                                                    Qwen3-8B FLOP Budget                                                                                                            DeepSeek-V3.2 FLOP Budget
                               800               ZS-CoT                                                                                                                                 ZS-CoT




                                                                                                                                                                                                                  .2K
                                                                                                                                                                           40000
                                                                                                                      7

                                                 Hermes                                                                                                                                 Hermes

                                                                                                                                              FLOP Budget (in TeraFLOPs)
  FLOP Budget (in TeraFLOPs)




                                                                                                                      7
                                                                                4




                                                                                                                                                                                                                 37
                                                                                                                   73
                                                                                                                   72
                                                                           72
                                                                             6
                                                                          69




                               700                                                                                                                                         35000
                                                 ORM/PRM/Safe                                                                                                                           ORM/PRM/Safe




                                                                                                                                                                                                                                                          .9K
                               600               Hermes@5                                                                                                                  30000        Hermes@5




                                                                                                                                                                                                                                                         28
                               500                                                                                                                                         25000




                                                                                                                                                                                                                .1K
                                                                                                                                                                                                            21




                                                                                                                                                                                                                                                        .4K
                               400                                                                                                                                         20000




                                                                                                                                                                                                                                                    18
                                                       4




                                                                                              8
                                                  33




                                                                                              32




                               300                                                                                                                                         15000
                                                           8
                                                       24




                                                                                                   4




                                                                                                                                                                                                           K
                                                                                                21




                                                                                                                                                                                                          9.3
                               200                                                                                                                                         10000


                                                                                                                                                                                               K
                                                                                                                0




                                                                                                                                                                                                                                       K
                                                                     9




                                                                                                                                                                                                                                                   K
                                                                                                               7




                                                                                                                                                                                          7.5
                                                                                                             16




                                                                                                                                                                                                                                      7.3
                                                                15
                                                                  8




                                                                                                                                                                                                                                                 6.7
                                                                                                                                                                                            K
                                                                                                            14
                                                               13




                                                                                                                                                                                        5.6



                                                                                                                                                                                                      K




                                                                                                                                                                                                                                     K


                                                                                                                                                                                                                                                 K
                                                                                                                                                                                                    4.4




                                                                                                                                                                                                                              4.1
                               100                                                                                                                                         5000




                                                                                                                                                                                                                                            3.7
                                                                                                                                                                                       K




                                                                                                                                                                                                                              K
                                      66




                                                                                         65
                                      64




                                                                                                                                                                                       K
                                                                                         58




                                                                                                                                                                                   1.6




                                                                                                                                                                                                                          1.6
                                                                                                                                                                                                                            4
                                                                                                                                                                                   1.1




                                                                                                                                                                                                                         81
                                0                                                                                                                                             0
                                                 MATH                AIME'25             CollegeMath          HardMath2                                                                 MATH               AIME'25            CollegeMath         HardMath2
                                                                                Dataset                                                                                                                               Dataset
                                                                      (a) Qwen3-8B                                                                                                                   (b) DeepSeek-V3.2

Figure 5. Average TeraFLOPs per problem on MATH500, AIME’25, CollegeMath, and HardMath2 under Zero-Shot Chain-of-Thought,
Hermes@1, Reward-Based Best-of-5 and Hermes@5 settings. Energy usage was recorded for each of the participating models.

Table 2. Ablation study of different sub-modules of Hermes . ✓                                                                                                 Table 3. Accuracy (%) of DeepSeek-V3.1 with Hermes on HM2
indicates inclusion of a module; ✗ indicates exclusion.                                                                                                        with a combination of various autoformalizer sampling budget
                                                                                                                                                               (Kf ) and prover sampling budget (Kp ).
               Memory                                  Prover        Accuracy (%)                  Accuracy (%)
               Buffer                                  Model           MATH                           AIME                                                                                                                       Prover (@Kp )
                                     ✗                     ✗                93.0                            50.0                                                                                                        @1        @4     @8 @16
                                     ✗                     ✓                97.0                            60.0                                                                                           @1          15.6          16.6        15.2     16.6
                                                                                                                                                                               Autoformalizer
                                     ✓                     ✗                93.0                            50.0                                                                                           @4          23.7          30.3        30.8     31.8
                                                                                                                                                                                  (@Kf )
                                     ✓                     ✓                97.4                            66.7                                                                                           @8          23.2          30.8        31.8     33.7


                                                                                                                                                               ble 3 shows that increasing Kf from 1 to 4 yields a massive
come more pronounced as reasoning complexity increases.
                                                                                                                                                               82.2% accuracy boost by mitigating formalization errors,
5.6. Sensitivity analysis on various values of Kp and Kf                                                                                                       with diminishing returns beyond that. Similarly, raising Kp
                                                                                                                                                               to 4 improves accuracy by 22.3% through better proof explo-
Table 3 illustrates the sensitivity of Hermes to sampling hy-                                                                                                  ration, also saturating at higher values. We therefore select
perparameters. We vary the autoformalizer sampling budget                                                                                                      Kf =4 and Kp =4 to balance reliability with computational
(Kf ) from 1 to 8 and prover sampling budget (Kp ) from 1                                                                                                      cost. Additional ablations are in Appendix B.
to 16, which is the number of formalization and proof veri-
fication attempts, respectively. In this experiment, we use
                                                                                                                                                                5.7. Translation accuracy and verification coverage
DeepSeek-V3.1 as the reasoning model and conduct evalu-
ations on the HARDMath2. Overall, increasing either Kf                                                                                                         To evaluate the reliability of Hermes, we performed a
or Kp , or both jointly, leads to improved performance. Ta-                                                                                                    human-led audit of the formalized reasoning steps. In Ta-

                                                                                                                                       8
                          HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

ble 4, we report two primary metrics: CoT Coverage, rep-                 neither a valid proof nor a counter-proof (Table 6). These re-
resenting the proportion of formalized steps for which the               sults underscore the agent’s dependency on the current state
Prover Module successfully identified a proof, and Trans-                of the formal mathematical library. However, because Her-
lation Accuracy, defined as the proportion of steps where                mes is designed with modularity in mind, its performance
human experts verified the formalization as semantically                 will improve with the ATP community as better prover and
faithful to the original statement. Adopting the annotation              autoformalization models emerge.
protocols by (Gao et al., 2025a), we manually labeled 100
steps: 50 randomly selected successful attempts (Table 5)                Table 6. Topic distribution of formalized steps with no found proof
and 50 steps where the prover failed to find a proof (Table 6).          based on the DeepSeek-V3.2 outputs.
We also measured the density of tool calls to understand
how Hermes is utilized across different difficulty levels.                        Topic                        MATH        AIME
We found that DeepSeek-V3.2 calls the module 5.5 times                            geometry                        16         14
on MATH and 10.4 times on AIME, respectively. Viewed                              trigonometry                    6          5
alongside our 75% coverage rate, this trend suggests that                         functions                       7          3
for more challenging tasks, the model more explicitly relies                      number theory                   0           8
on Hermes to break down the reasoning chain into a more                           sets/sequences                  4          9
extensive series of sub-steps. Furthermore, qualitative in-                       equations/polynomials           7          6
spection of the Formalizer Module’s output confirms that                          others                          10          5
over 80% of these steps are faithfully translated into Lean.

Table 4. CoT coverage and translation accuracy of Hermes based
on the DeepSeek-V3.2 outputs.                                            6. Conclusion
          Metric                     MATH       AIME                     In this work, we introduced Hermes, a Lean4-powered, tool-
                                                                         augmented agent for advanced mathematical reasoning. The
          CoT Coverage                87%        76%
                                                                         framework combines the flexibility of informal problem
          Translation Accuracy        86%        80%
                                                                         solving with the rigor of formal verification by validating
                                                                         intermediate steps that would otherwise be prone to hallu-
To further refine this analysis, we categorized the manually             cinations or logical errors. Built on state-of-the-art Lean4
annotated steps by mathematical domain, as shown in Ta-                  theorem-proving and autoformalization models, Hermes in-
ble 5. We observe that the agent’s performance is strongest              corporates a dedicated memory mechanism that preserves
in equations, polynomials, and algebra. This high perfor-                proof continuity across long reasoning chains and guides the
mance correlates directly with the density of existing decla-            reasoning LLM towards a correct solution. Experimental
rations in Mathlib. According to the Lean Community (The                 results show that Hermes achieves higher accuracy on four
Lean Community, 2026), algebra alone contains 56, 000+                   challenging mathematical benchmarks while consuming
declarations, whereas Geometry (∼ 5800), Number Theory                   substantially fewer inference resources than reward-based
(∼ 6500), and Combinatorics (∼ 7500) are significantly                   approaches. On average, Hermes improves accuracy by 14%
less saturated.                                                          while using at least 4× fewer reasoning tokens. This im-
Table 5. Topic distribution of correctly formalized steps based on
                                                                         provement stems from the synergistic interaction between
the DeepSeek-V3.2 outputs.                                               its memory module, back-translator, and Lean4’s native
                                                                         solvers. Overall, Hermes represents a step toward unify-
        Topic                         MATH        AIME                   ing informal and formal mathematical reasoning within a
                                                                         scalable, verifiable, interpretable, and modular framework.
        equations/polynomials            21         16
        arithmetic                       12          6
        inequality                       5          3                    Acknowledgments
        geometry                         1          6
                                                                         The work of Farzan Farnia is partially supported by a grant
        sets/sequences                    3          4
                                                                         from the Research Grants Council of the Hong Kong Spe-
        trigonometric equations           2          3
                                                                         cial Administrative Region, China, Project 14210725, and
        functions                        3          2
                                                                         is partially supported by CUHK Direct Research Grants
        combinatorics                     0          9
                                                                         with CUHK Project No. 4055164. The work is also sup-
        others                           3          1
                                                                         ported by a grant under 1+1+1 CUHK-CUHK(SZ)-GDSTC
                                                                         Joint Collaboration Fund. The authors also thank the anony-
Finally, to diagnose failure modes within Hermes, we classi-             mous reviewers for their helpful feedback and constructive
fied a subset of steps for which the Prover Module could find            suggestions.

                                                                     9
                        HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

Impact Statement                                                      References
This paper introduces a hybrid agent designed to bridge               Akbar, S. A., Hossain, M. M., Wood, T., Chin, S.-C., Sali-
the gap between informal and formal mathematics. The                    nas, E. M., Alvarez, V., and Cornejo, E. HalluMeasure:
research relies exclusively on publicly available mathemat-             Fine-grained hallucination measurement using chain-of-
ical data and does not involve human subjects or sensitive              thought reasoning. In Al-Onaizan, Y., Bansal, M., and
personal information; as such, it poses no privacy or fairness          Chen, Y.-N. (eds.), Proceedings of the 2024 Conference
concerns. By integrating Lean into informal mathematics                 on Empirical Methods in Natural Language Process-
via tool-based agent, this work aims to enhance automated               ing, pp. 15020–15037, Miami, Florida, USA, Novem-
theorem proving. We confirm that this research adheres                  ber 2024. Association for Computational Linguistics.
strictly to the ICML Code of Ethics and presents no foresee-            doi: 10.18653/v1/2024.emnlp-main.837. URL https:
able harmful applications.                                             //aclanthology.org/2024.emnlp-main.837/.

                                                                      Bertot, Y. and Castéran, P. Interactive theorem proving and
                                                                        program development: Coq’Art: the calculus of inductive
                                                                        constructions. Springer Science & Business Media, 2013.

                                                                      Cao, C., Song, L., Li, Z., Le, X., Zhang, X., Xue, H., and
                                                                        Yang, F. Reviving dsp for advanced theorem proving in
                                                                        the era of reasoning models. In The Thirty-ninth Annual
                                                                        Conference on Neural Information Processing Systems,
                                                                        2025.

                                                                      Chen, L., Gu, J., Huang, L., Huang, W., Jiang, Z., Jie,
                                                                        A., Jin, X., Jin, X., Li, C., Ma, K., Ren, C., Shen, J.,
                                                                        Shi, W., Sun, T., Sun, H., Wang, J., Wang, S., Wang,
                                                                        Z., Wei, C., Wei, S., Wu, Y., Wu, Y., Xia, Y., Xin, H.,
                                                                        Yang, F., Ying, H., Yuan, H., Yuan, Z., Zhan, T., Zhang,
                                                                        C., Zhang, Y., Zhang, G., Zhao, T., Zhao, J., Zhou, Y.,
                                                                        and Zhu, T. H. Seed-prover: Deep and broad reasoning
                                                                        for automated theorem proving. CoRR, abs/2507.23726,
                                                                        2025. doi: 10.48550/ARXIV.2507.23726. URL https:
                                                                        //doi.org/10.48550/arXiv.2507.23726.

                                                                      Competitions, A. M. and of Problem Solving,
                                                                        A.      Aime problems and solutions — 2025.
                                                                        https://artofproblemsolving.com/wiki/index.
                                                                        php/AIME_Problems_and_Solutions, 2025.

                                                                      DeepSeek-AI, Liu, A., Mei, A., Lin, B., Xue, B., Wang,
                                                                        B., Xu, B., Wu, B., Zhang, B., Lin, C., Dong, C., Lu, C.,
                                                                        Zhao, C., Deng, C., Xu, C., Ruan, C., Dai, D., Guo, D.,
                                                                       Yang, D., Chen, D., Li, E., Zhou, F., Lin, F., Dai, F., Hao,
                                                                        G., Chen, G., Li, G., Zhang, H., Xu, H., Li, H., Liang,
                                                                        H., Wei, H., Zhang, H., Luo, H., Ji, H., Ding, H., Tang,
                                                                        H., Cao, H., Gao, H., Qu, H., Zeng, H., Huang, J., Li,
                                                                        J., Xu, J., Hu, J., Chen, J., Xiang, J., Yuan, J., Cheng, J.,
                                                                        Zhu, J., Ran, J., Jiang, J., Qiu, J., Li, J., Song, J., Dong,
                                                                        K., Gao, K., Guan, K., Huang, K., Zhou, K., Huang, K.,
                                                                       Yu, K., Wang, L., Zhang, L., Wang, L., Zhao, L., Yin,
                                                                        L., Guo, L., Luo, L., Ma, L., Wang, L., Zhang, L., Di,
                                                                        M. S., Xu, M. Y., Zhang, M., Zhang, M., Tang, M., Zhou,
                                                                        M., Huang, P., Cong, P., Wang, P., Wang, Q., Zhu, Q.,
                                                                        Li, Q., Chen, Q., Du, Q., Xu, R., Ge, R., Zhang, R., Pan,
                                                                        R., Wang, R., Yin, R., Xu, R., Shen, R., Zhang, R., Liu,
                                                                        S. H., Lu, S., Zhou, S., Chen, S., Cai, S., Chen, S., Hu,

                                                                 10
                        HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

  S., Liu, S., Hu, S., Ma, S., Wang, S., Yu, S., Zhou, S.,             Google DeepMind. AI achieves silver-medal standard solv-
  Pan, S., Zhou, S., Ni, T., Yun, T., Pei, T., Ye, T., Yue, T.,          ing international mathematical olympiad problems, 2024.
  Zeng, W., Liu, W., Liang, W., Pang, W., Luo, W., Gao,                  Accessed: 2025-05-08.
  W., Zhang, W., Gao, X., Wang, X., Bi, X., Liu, X., Wang,
  X., Chen, X., Zhang, X., Nie, X., Cheng, X., Liu, X., Xie,           Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H.,
  X., Liu, X., Yu, X., Li, X., Yang, X., Li, X., Chen, X.,               Chen, Q., Peng, W., Feng, X., Qin, B., and Liu, T. A sur-
  Su, X., Pan, X., Lin, X., Fu, X., Wang, Y. Q., Zhang, Y.,              vey on hallucination in large language models: Principles,
  Xu, Y., Ma, Y., Li, Y., Li, Y., Zhao, Y., Sun, Y., Wang, Y.,           taxonomy, challenges, and open questions. ACM Trans.
  Qian, Y., Yu, Y., Zhang, Y., Ding, Y., Shi, Y., Xiong, Y.,             Inf. Syst., 43(2), January 2025. ISSN 1046-8188. doi:
  He, Y., Zhou, Y., Zhong, Y., Piao, Y., Wang, Y., Chen, Y.,            10.1145/3703155. URL https://doi.org/10.1145/
  Tan, Y., Wei, Y., Ma, Y., Liu, Y., Yang, Y., Guo, Y., Wu,              3703155.
  Y., Wu, Y., Cheng, Y., Ou, Y., Xu, Y., Wang, Y., Gong,               Huang, Y. and Yang, L. F. Winning gold at imo 2025 with
  Y., Wu, Y., Zou, Y., Li, Y., Xiong, Y., Luo, Y., You, Y.,              a model-agnostic verification-and-refinement pipeline,
  Liu, Y., Zhou, Y., Wu, Z. F., Ren, Z. Z., Zhao, Z., Ren,               2025. URL https://arxiv.org/abs/2507.15855.
  Z., Sha, Z., Fu, Z., Xu, Z., Xie, Z., Zhang, Z., Hao, Z.,
  Gou, Z., Ma, Z., Yan, Z., Shao, Z., Huang, Z., Wu, Z.,               Jiang, A. Q., Li, W., Tworkowski, S., Czechowski, K.,
  Li, Z., Zhang, Z., Xu, Z., Wang, Z., Gu, Z., Zhu, Z., Li,               Odrzygóźdź, T., Miłoś, P., Wu, Y., and Jamnik, M.
  Z., Zhang, Z., Xie, Z., Gao, Z., Pan, Z., Yao, Z., Feng,                Thor: Wielding hammers to integrate language models
  B., Li, H., Cai, J. L., Ni, J., Xu, L., Li, M., Tian, N.,               and automated theorem provers. In Advances in Neu-
  Chen, R. J., Jin, R. L., Li, S. S., Zhou, S., Sun, T., Li,              ral Information Processing Systems, 2022. URL https:
  X. Q., Jin, X., Shen, X., Chen, X., Song, X., Zhou, X.,                 //openreview.net/forum?id=fUeOyt-2EOp.
  Zhu, Y. X., Huang, Y., Li, Y., Zheng, Y., Zhu, Y., Ma, Y.,
  Huang, Z., Xu, Z., Zhang, Z., Ji, D., Liang, J., Guo, J.,            Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J., Jamnik,
  Chen, J., Xia, L., Wang, M., Li, M., Zhang, P., Chen, R.,               M., Lacroix, T., Wu, Y., and Lample, G. Draft, Sketch,
  Sun, S., Wu, S., Ye, S., Wang, T., Xiao, W. L., An, W.,                 and Prove: Guiding formal theorem provers with informal
  Wang, X., Sun, X., Wang, X., Tang, Y., Zha, Y., Zhang,                  proofs. In International Conference on Learning Repre-
  Z., Ju, Z., Zhang, Z., and Qu, Z. Deepseek-v3.2: Pushing                sentations, 2023. URL https://doi.org/10.48550/
  the frontier of open large language models, 2025. URL                   arXiv.2210.12283.
  https://arxiv.org/abs/2512.02556.
                                                                       Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B.,
Dong, H., Xiong, W., Pang, B., Wang, H., Zhao, H., Zhou,                 Chess, B., Child, R., Gray, S., Radford, A., Wu, J., and
 Y., Jiang, N., Sahoo, D., Xiong, C., and Zhang, T. Rlhf                 Amodei, D. Scaling laws for neural language models,
 workflow: From reward modeling to online rlhf. arXiv                    2020. URL https://arxiv.org/abs/2001.08361.
  preprint arXiv:2405.07863, 2024.                                     Kirtania, S., Gupta, P., and Radhakrishna, A. LOGIC-
                                                                         LM++: Multi-step refinement for symbolic formulations.
et al., D.-A. Deepseek-v3 technical report, 2025. URL
                                                                         In Dalvi Mishra, B., Durrett, G., Jansen, P., Lipkin,
   https://arxiv.org/abs/2412.19437.
                                                                         B., Neves Ribeiro, D., Wong, L., Ye, X., and Zhao,
First, E., Rabe, M. N., Ringer, T., and Brun, Y. Baldur:                 W. (eds.), Proceedings of the 2nd Workshop on Natu-
  Whole-proof generation and repair with large language                  ral Language Reasoning and Structured Explanations
  models, 2023. URL https://arxiv.org/abs/2303.                          (@ACL 2024), pp. 56–63, Bangkok, Thailand, August
  04910.                                                                 2024. Association for Computational Linguistics. URL
                                                                         https://aclanthology.org/2024.nlrse-1.6/.
Gao, G., Wang, Y., Jiang, J., Gao, Q., Qin, Z., Xu, T., and
                                                                       Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., and Iwasawa,
  Dong, B. Herald: A natural language annotated lean 4
                                                                        Y. Large language models are zero-shot reasoners. In
  dataset. In The Thirteenth International Conference on
                                                                         Koyejo, S., Mohamed, S., Agarwal, A., Belgrave, D.,
  Learning Representations, ICLR 2025, Singapore, April
                                                                         Cho, K., and Oh, A. (eds.), Advances in Neural Informa-
  24-28, 2025. OpenReview.net, 2025a. URL https://
                                                                         tion Processing Systems, volume 35, pp. 22199–22213.
  openreview.net/forum?id=Se6MgCtRhz.
                                                                         Curran Associates, Inc., 2022.
Gao, S., Dwivedi-Yu, J., Yu, P., Tan, X. E., Pasunuru,                 Lean FRO. A read-eval-print-loop for Lean 4. https://
  R., Golovneva, O., Sinha, K., Celikyilmaz, A., Bosse-                  github.com/leanprover-community/repl, 2023.
  lut, A., and Wang, T. Efficient tool use with chain-of-
  abstraction reasoning, 2025b. URL https://arxiv.                     Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,
  org/abs/2401.17464.                                                    B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and

                                                                  11
                        HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

  Cobbe, K. Let’s verify step by step, 2023. URL https:               Ning, K., Su, Y., Lv, X., Zhang, Y., Liu, J., Liu, K., and
  //arxiv.org/abs/2305.20050.                                           Xu, J. Wtu-eval: A whether-or-not tool usage evaluation
                                                                        benchmark for large language models, 2024. URL https:
Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,              //arxiv.org/abs/2407.12823.
  B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and
  Cobbe, K. Let’s verify step by step. In The Twelfth                 Nipkow, T., Paulson, L. C., and Wenzel, M. Isabelle/HOL:
  International Conference on Learning Representations,                 a proof assistant for higher-order logic, volume 2283.
  2024. URL https://openreview.net/forum?id=                            Springer Science & Business Media, 2002.
  v8L0pN6EOi.
                                                                      OpenAI. Openai o3-mini. https://openai.com/index/
Lin, H., Sun, Z., Yang, Y., and Welleck, S. Lean-star:                  openai-o3-mini/, January 2025.
  Learning to interleave thinking and proving. In The
                                                                      Ospanov, A., Farnia, F., and Yousefzadeh, R. Apollo: Au-
  Thirteenth International Conference on Learning Rep-
                                                                        tomated llm and lean collaboration for advanced formal
  resentations, ICLR 2025, Singapore, April 24-28, 2025.
                                                                        reasoning. In The Thirty-ninth Annual Conference on
  OpenReview.net, 2025a.
                                                                        Neural Information Processing Systems, 2025.
Lin, Y., Tang, S., Lyu, B., Yang, Z., Chung, J., Zhao,                Pan, L., Albalak, A., Wang, X., and Wang, W. Y. Logic-LM:
  H., Jiang, L., Geng, Y., Ge, J., Sun, J., Wu, J., Gesi,               empowering large language models with symbolic solvers
  J., Lu, X., Acuna, D., Yang, K., Lin, H., Choi, Y.,                   for faithful logical reasoning. In Findings of the 2023
  Chen, D., Arora, S., and Jin, C. Goedel-prover-v2:                    Conference on Empirical Methods in Natural Language
  Scaling formal theorem proving with scaffolded data                   Processing (Findings of EMNLP), Singapore, Dec 2023.
  synthesis and self-correction. CoRR, abs/2508.03613,                  URL https://arxiv.org/abs/2305.12295.
  2025b. doi: 10.48550/ARXIV.2508.03613. URL https:
  //doi.org/10.48550/arXiv.2508.03613.                                Qin, Y., Liang, S., Ye, Y., Zhu, K., Yan, L., Lu, Y., Lin,
                                                                        Y., Cong, X., Tang, X., Qian, B., Zhao, S., Hong, L.,
Liu, C., Yuan, Y., Yin, Y., Xu, Y., Xu, X., Chen, Z., Wang,             Tian, R., Xie, R., Zhou, J., Gerstein, M., Li, D., Liu,
  Y., Shang, L., Liu, Q., and Zhang, M. Safe: Enhancing                 Z., and Sun, M. Toolllm: Facilitating large language
  mathematical reasoning in large language models via ret-              models to master 16000+ real-world apis, 2023. URL
  rospective step-aware formal verification. In Che, W.,                https://arxiv.org/abs/2307.16789.
  Nabende, J., Shutova, E., and Pilehvar, M. T. (eds.), Pro-
  ceedings of the 63rd Annual Meeting of the Association              Qu, C., Dai, S., Wei, X., Cai, H., Wang, S., Yin, D.,
  for Computational Linguistics (Volume 1: Long Papers),               Xu, J., and Wen, J.-r. Tool learning with large lan-
  pp. 12171–12186, Vienna, Austria, July 2025. Associa-                 guage models: a survey. Frontiers of Computer Sci-
  tion for Computational Linguistics. ISBN 979-8-89176-                 ence, 19(8), January 2025. ISSN 2095-2236. doi:
  251-0. doi: 10.18653/v1/2025.acl-long.594. URL https:                10.1007/s11704-024-40678-2. URL http://dx.doi.
  //aclanthology.org/2025.acl-long.594/.                                org/10.1007/s11704-024-40678-2.

Liu, C. Y., Zeng, L., Liu, J., Yan, R., He, J., Wang, C., Yan,        Ringer, T. Proof Repair. PhD thesis, University of Wash-
  S., Liu, Y., and Zhou, Y. Skywork-reward: Bag of tricks               ington, 2021. URL https://homes.cs.washington.
  for reward modeling in llms. CoRR, abs/2410.18451,                    edu/~djg/theses/ringer_dissertation.pdf.
  2024. doi: 10.48550/ARXIV.2410.18451. URL https:                      Ph.D. dissertation.
  //doi.org/10.48550/arXiv.2410.18451.
                                                                      Roggeveen, J. V., Wang, E. Y., Flintoft, W., Donets, P.,
Lu, H., Liu, Y., Xu, J., Nan, G., Yu, Y., Chen, Z., and Wang,           Nathwani, L. S., Gutierrez, N., Ettel, D., Graf, A. M.,
  K. Auditing meta-cognitive hallucinations in reasoning                Dandavate, S., Nageswaran, A., Ward, R., Williamson,
  large language models. In The Thirty-ninth Annual Con-                A., Mykland, A., Migacz, K. K., Wang, Y., Bostan, E.,
  ference on Neural Information Processing Systems, 2025.               Nguyen, D. T., He, Z., Descoteaux, M. L., Yeung, F.,
                                                                        Liu, S., Ponce, J. G., Zhu, L., Chen, Y., Ivshina, E. S.,
Moura, L. d. and Ullrich, S. The lean 4 theorem prover                  Fernandez, M., Kim, M., Gumbs, K., Tan, M. S., Yang,
 and programming language. In Automated Deduction                       R., Hoang, M., Brown, D., Silveira, I. A., Sykes, L.,
 – CADE 28: 28th International Conference on Au-                        Roman, A., Fredenberg, W., Chen, Y., Martin, L., Tang,
 tomated Deduction, Virtual Event, July 12–15, 2021,                    Y., Smith, K. W., Liao, H., Wilson, L. G., Cai, A. D.,
 Proceedings, pp. 625–635, Berlin, Heidelberg, 2021.                    Biju, A. E., and Brenner, M. P. Hardmath2: A benchmark
 Springer-Verlag. ISBN 978-3-030-79875-8. doi: 10.                      for applied mathematics built by students as part of a
 1007/978-3-030-79876-5_37. URL https://doi.org/                        graduate class. In The Thirty-ninth Annual Conference
 10.1007/978-3-030-79876-5_37.                                          on Neural Information Processing Systems, 2025.

                                                                 12
                       HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Zhang, M.,            Z., Wang, Z., Yang, Z., Liu, Z., and Li, J. Kimina-
  Li, Y. K., Wu, Y., and Guo, D. Deepseekmath: Push-                 prover preview: Towards large formal reasoning mod-
  ing the limits of mathematical reasoning in open lan-              els with reinforcement learning. ArXiv, 2025b. URL
  guage models. CoRR, abs/2402.03300, 2024. doi: 10.                 http://arxiv.org/abs/2504.11354.
  48550/ARXIV.2402.03300. URL https://doi.org/
  10.48550/arXiv.2402.03300.                                       Wang, P., Li, L., Shao, Z., Xu, R., Dai, D., Li, Y., Chen, D.,
                                                                    Wu, Y., and Sui, Z. Math-shepherd: Verify and reinforce
She, S., Liu, J., Liu, Y., Chen, J., Huang, X., and                 llms step-by-step without human annotations. In Proceed-
  Huang, S. R-PRM: reasoning-driven process reward                  ings of the 62nd Annual Meeting of the Association for
  modeling. CoRR, abs/2503.21295, 2025. doi: 10.                    Computational Linguistics (Volume 1: Long Papers), ACL
  48550/ARXIV.2503.21295. URL https://doi.org/                      2024, Bangkok, Thailand, August 11-16, 2024, pp. 9426–
  10.48550/arXiv.2503.21295.                                        9439. Association for Computational Linguistics, 2024b.
                                                                    doi: 10.18653/V1/2024.ACL-LONG.510. URL https:
Tang, Z., Zhang, X., Wang, B., and Wei, F. Mathscale:               //doi.org/10.18653/v1/2024.acl-long.510.
  Scaling instruction tuning for mathematical reasoning. In
  Forty-first International Conference on Machine Learn-           Wei, J., Wang, X., Schuurmans, D., Bosma, M., brian ichter,
  ing, ICML 2024, Vienna, Austria, July 21-27, 2024. Open-          Xia, F., Chi, E. H., Le, Q. V., and Zhou, D. Chain of
  Review.net, 2024. URL https://openreview.net/                     thought prompting elicits reasoning in large language
  forum?id=Kjww7ZN47M.                                              models. In Oh, A. H., Agarwal, A., Belgrave, D., and
                                                                    Cho, K. (eds.), Advances in Neural Information Process-
Team, Q. Qwen3 technical report, 2025. URL https:                   ing Systems, 2022. URL https://openreview.net/
  //arxiv.org/abs/2505.09388.                                       forum?id=_VjQlMeSB_J.
The Lean Community.      Import graph for math-                    Xin, H., Ren, Z., Song, J., Shao, Z., Zhao, W., Wang, H.,
  lib. https://leanprover-community.github.io/                       Liu, B., Zhang, L., Lu, X., Du, Q., Gao, W., Zhang,
  mathlib4_docs/, 2026.                                              H., Zhu, Q., Yang, D., Gou, Z., Wu, Z., Luo, F., and
Trinh, T., Wu, Y., Le, Q., He, H., and Luong, T. Solv-               Ruan, C. Deepseek-prover-v1.5: Harnessing proof as-
  ing olympiad geometry without human demonstrations.                sistant feedback for reinforcement learning and monte-
  Nature, 2024. doi: 10.1038/s41586-023-06747-5.                     carlo tree search. In The Thirteenth International Confer-
                                                                     ence on Learning Representations, 2025. URL https:
Wang, H., Xiong, W., Xie, T., Zhao, H., and Zhang, T. Inter-         //openreview.net/forum?id=I4YAIwrsXa.
 pretable preferences via multi-objective reward modeling
 and mixture-of-experts. In Al-Onaizan, Y., Bansal, M.,            Xu, X., Xiao, T., Chao, Z., Huang, Z., Yang, C., and Wang,
 and Chen, Y. (eds.), Findings of the Association for Com-          Y. Can llms solve longer math word problems better?
 putational Linguistics: EMNLP 2024, Miami, Florida,                 arXiv preprint arXiv:2405.14804, 2024.
 USA, November 12-16, 2024, pp. 10582–10592. Associa-              Yang, K., Poesia, G., He, J., Li, W., Lauter, K., Chaudhuri,
 tion for Computational Linguistics, 2024a. doi: 10.18653/           S., and Song, D. Formal mathematical reasoning: A
 V1/2024.FINDINGS-EMNLP.620. URL https://doi.                        new frontier in AI. In Proceedings of the International
 org/10.18653/v1/2024.findings-emnlp.620.                            Conference on Machine Learning, 2025.
Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Dos San-        Yousefzadeh, R., Cao, X., and Ospanov, A. A Lean
 tos, M., Sung, F., Zhang, Y., Zekai, Z., Qiao, L. J.,               dataset for International Math Olympiad: Small steps
 de Saxcéand, H., Barroyer, T., Zhang, E., Bailey, B.,               towards writing math proofs for hard problems. Trans-
 Pu, F., Bayer, J., Vinyes, M., Liu, Z., Jia, L., and the AI-        actions on Machine Learning Research, 2025. ISSN
 MO team. Kimina-prover: Applying test-time rl search on             2835-8856. URL https://openreview.net/forum?
 large formal reasoning models. https://huggingface.                 id=CrKMqRAhBo.
 co/blog/AI-MO/kimina-prover, July 2025a. Pub-
 lished July 10, 2025.                                             Yu, L., Jiang, W., Shi, H., Yu, J., Liu, Z., Zhang, Y., Kwok,
                                                                     J. T., Li, Z., Weller, A., and Liu, W. Metamath: Boot-
Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Santos,           strap your own mathematical questions for large language
 M. D., Sung, F., Vinyes, M., Ying, Z., Zhu, Z., Lu, J.,             models. ArXiv preprint, abs/2309.12284, 2023. URL
 Saxcé, H. d., Bailey, B., Song, C., Xiao, C., Zhang, D.,            https://arxiv.org/abs/2309.12284.
 Zhang, E., Pu, F., Zhu, H., Liu, J., Bayer, J., Michel,
 J., Yu, L., Dreyfus-Schmidt, L., Tunstall, L., Pagani, L.,        Yu, X., Zhong, J., Feng, Z., Zhai, P., Yousefzadeh, R., Ng,
 Machado, M., Bourigault, P., Wang, R., Polu, S., Bar-               W. C., Liu, H., Shou, Z., Xiong, J., Zhou, Y., Ong,
 royer, T., Li, W.-D., Niu, Y., Fleureau, Y., Hu, Y., Yu,            C., Sugiarto, A. J., Zhang, Y., Tai, W. M., Cao, H.,

                                                              13
                       HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

  Lu, D., Sun, J., Xu, Q., Xin, S., and Li, Z. Math-
  esis: Towards formal theorem proving from natural
  languages. CoRR, abs/2506.07047, 2025. doi: 10.
  48550/ARXIV.2506.07047. URL https://doi.org/
  10.48550/arXiv.2506.07047.
Zhang, Y., Li, M., Long, D., Zhang, X., Lin, H., Yang, B.,
  Xie, P., Yang, A., Liu, D., Lin, J., Huang, F., and Zhou,
  J. Qwen3 embedding: Advancing text embedding and
  reranking through foundation models. arXiv preprint
  arXiv:2506.05176, 2025a.
Zhang, Z., Zheng, C., Wu, Y., Zhang, B., Lin, R., Yu, B.,
  Liu, D., Zhou, J., and Lin, J. The lessons of developing
  process reward models in mathematical reasoning. In
  Che, W., Nabende, J., Shutova, E., and Pilehvar, M. T.
  (eds.), Findings of the Association for Computational
  Linguistics: ACL 2025, pp. 10495–10516, Vienna, Aus-
  tria, July 2025b. Association for Computational Linguis-
  tics. ISBN 979-8-89176-256-5. doi: 10.18653/v1/2025.
  findings-acl.547. URL https://aclanthology.org/
  2025.findings-acl.547/.
Zheng, K., Han, J. M., and Polu, S. miniF2F: a cross-system
  benchmark for formal Olympiad-level mathematics, 2022.
  URL https://arxiv.org/abs/2109.00110.

Zhou, J. P., Staats, C. E., Li, W., Szegedy, C., Weinberger,
  K. Q., and Wu, Y. Don’t trust: Verify–grounding llm
  quantitative reasoning with autoformalization. In The
  Twelfth International Conference on Learning Represen-
  tations, 2023.




                                                               14
                 HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

A. Prompt and instruction templates
# Hermes Tool Instruction
Formally validates a **single** reasoning step using a formal Lean4 verifier. Invoke this
    function when facing a step that potentially involves a hallucination. Make sure to
    verify EVERY critical mathematical proof step.

Args:
    proof_step (str): A proof step that includes both the goal to be proven and the
    relevant context (e.g., variables, assumptions, and previously proven statements).
    Always explicitly specify the relevant context, such as domains, data types, and any
    other necessary details. Make sure to state the proof step in English.

Returns:
    str: A status string indicating the verification result:
         - **CORRECT**: Step verified by the theorem prover.
         - **INCORRECT**: Step rejected by the theorem prover (e.g., the prover proved a
    contradiction or the opposite statement).
         - **VERIFICATION FAILURE**: Step could not be verified by Lean 4 (e.g., the prover
    was unable to prove the statement or find contradictory arguments)

Notes:
    - Treat **CORRECT** steps as reliable within the given formalization.
    - Treat **INCORRECT** steps as requiring revision; a suggested correction is returned
    with this label.
    - Use **VERIFICATION FAILURE** to indicate inconclusive or ill-formed steps that Lean 4
    was unable to prove or disprove.

# Answer verification prompt
Given a question, an answer to that question, and the ground truth for that question’s
    answer, you need to check if the given answer matches the ground truth.
* If the answer is complete and correct, simply reply with True.
* If the given answer does not match the ground truth or is incomplete, reply with False.
* Do **NOT** respond with any other characters.

Question:
<question>

Answer:
<answer>

Ground Truth:
<ground_truth>

Does the answer match the ground truth? (True or False):




                                                   15
                       HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs


# NL->FL translation prompt for Goedel-Formalizer-V2-8B
Please autoformalize the following natural language problem statement in Lean 4.
Use the following theorem name: test
The natural language statement is:
<question>
Think before you provide the lean statement.

# Theorem proving prompt for Goedel-Prover-V2-8B
Complete the following Lean 4 code:

‘‘‘lean4
<header>

<body>‘‘‘

Before producing the Lean 4 code to formally prove the given theorem, provide a detailed
    proof plan outlining the main proof steps and strategies.
The plan should highlight key ideas, intermediate lemmas, and proof structures that will
    guide the construction of the final formal proof.

# NL->FL translation prompt for Kimina-Autoformalizer-7B
Please autoformalize the following problem in Lean 4 with a header. Use the following
    theorem names: my_favorite_theorem.

<question>

# Theorem proving prompt for Kimina-Prover-RL-1.7B
Think about and solve the following problem step by step in Lean 4.
# Formal statement:
‘‘‘lean4
<header>

<body>
‘‘‘

The prompt instructions and templates are shown above. For the Hermes prompt, we follow the LangChain community
guidelines. The tool is named verify_one_mathematical_step to encourage the model to verify only a single step
rather than an entire proof. The tool description is flexible and can be modified; in particular, adjusting the description
can change how frequently the tool is invoked. The answer-verification prompt is adapted from (Liu et al., 2025). For the
autoformalizer and prover prompts, we use the officially released versions provided by the original developers.




                                                            16
                                                                                   HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

                                               Autoformalizer sampling is fixed at @1                                                                                               Autoformalizer sampling is fixed at @4                                                                                                            Autoformalizer sampling is fixed at @8
                                           Autoformalizer failed to translate                                                                                                    Autoformalizer failed to translate                                                                                                                Autoformalizer failed to translate
                                           Prover failed to prove/disprove                                                                                                       Prover failed to prove/disprove                                                                                                                   Prover failed to prove/disprove

                         100%                                                                                                                                        100%                                                                                                                                              100%
    Lean4 Feedback (%)




                                                                                                                                                Lean4 Feedback (%)




                                                                                                                                                                                                                                                                                                  Lean4 Feedback (%)
                         80%                                                                                                                                         80%                                                                                                                                               80%

                         60%                                                                                                                                         60%                                                                                                                                               60%

                         40%                                                                                                                                         40%                                                                                                                                               40%

                         20%                                                                                                                                         20%                                                                                                                                               20%

                             0%                                                                                                                                       0%                                                                                                                                                0%
                                             @1                             @4         @8                                  @16                                                     @1                        @4                                   @8                                   @16                                           @1                                     @4                               @8          @16
                                                                       Prover sampling (@K)                                                                                                               Prover sampling (@K)                                                                                                                                          Prover sampling (@K)

                                                           (a) Translator @1                                                                                                                 (b) Translator @4                                                                                                                                             (c) Translator @8

                                                                                     Figure 6. Distribution of Hermes failures with a fixed translation budget (Kf ).

                                              Prover sampling is fixed at @1                                                             Prover sampling is fixed at @4                                                                                       Prover sampling is fixed at @8                                                                                      Prover sampling is fixed at @16
                                  Autoformalizer failed to translate                                                         Autoformalizer failed to translate                                                                                   Autoformalizer failed to translate                                                                                    Autoformalizer failed to translate
                                  Prover failed to prove/disprove                                                            Prover failed to prove/disprove                                                                                      Prover failed to prove/disprove                                                                                       Prover failed to prove/disprove

                      100%                                                                                          100%                                                                                                                   100%                                                                                                                  100%
 Lean4 Feedback (%)




                                                                                               Lean4 Feedback (%)




                                                                                                                                                                                                                      Lean4 Feedback (%)




                                                                                                                                                                                                                                                                                                                                            Lean4 Feedback (%)
                      80%                                                                                           80%                                                                                                                    80%                                                                                                                   80%

                      60%                                                                                           60%                                                                                                                    60%                                                                                                                   60%

                      40%                                                                                           40%                                                                                                                    40%                                                                                                                   40%

                      20%                                                                                           20%                                                                                                                    20%                                                                                                                   20%

                       0%                                                                                            0%                                                                                                                     0%                                                                                                                    0%
                                      @1                               @4             @8                                         @1                                         @4                          @8                                            @1                                     @4                               @8                                            @1                               @4            @8
                                                        Translator sampling (@K)                                                                       Translator sampling (@K)                                                                                         Translator sampling (@K)                                                                                              Translator sampling (@K)

                                             (a) Prover @1                                                                              (b) Prover @4                                                                                                        (c) Prover @8                                                                                                       (d) Prover @16

                                                                                           Figure 7. Distribution of Hermes failures with a fixed prover budget (Kp ).


B. Additional ablation on different combinations of autoformalizers and provers
Following the ablation studies presented in Table 3 of the main text, we provide additional insights into the selection of Kf
and Kp . Figures 6 and 7 illustrate the proportion of translator and prover errors, respectively, each with either the translation
or prover budget held fixed. We observe that at @1, translation failures are overwhelmingly frequent, exceeding 60%. As
the translation budget Kf increases, such failures become rare, contributing to 10% or less of all Lean verification errors.
Conversely, when Kp = 1, the prover becomes highly unreliable, with unresolved proof steps accounting for up to 95% of
all verification failures. Increasing Kp to 16 yields diminishing returns, as theorem proving is inherently more complex than
autoformalization, requiring a substantially larger budget for high-quality proof generation. However, given that Hermes
was evaluated under moderate computational constraints, our focus remained on efficient inference and agent interaction.
Our results align with prior work, where whole-proof generation models typically employ very large sampling budgets,
ranging from 1,024 to 25,600 samples. We hypothesize that in large-scale settings, increasing Kp beyond 16 may further
reduce prover failure rates.




                                                                                                                                                                                                                  17
                                          HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

                                                                                [MATH500] Precalculus - 768




...                                                                                                          ...
#### Case 1: \(x > 0\)
If \(x > 0\), then \(y = \frac{1}{x} > 0\). Therefore, the identity holds:                                   First, I notice that $\tan^{-1}(x)$ and $\cot^{-1}\left(\frac{1}{x}\right)$ are related. Let me verify
\[ \cot^{-1}\left( \frac{1}{x} \right) = \tan^{-1}(x) \]                                                     if there's a relationship between these two inverse trigonometric functions.
...                                                                                                          Lean agent verified proof steps:
                                                                                                               1.For x > 0, θ = tan⁻¹(x) implies tan(θ) = x, so cot(θ) = 1/x, which means θ = cot⁻¹(1/x).
Thus, both solutions are valid.                                                                                  Therefore, tan⁻¹(x) = cot⁻¹(1/x) for x > 0.
                                                                                                               2.For x = 0, tan⁻¹(0) = 0 and cot⁻¹(1/0) is undefined since division by zero is not allowed.
#### Case 2: \(x < 0\)                                                                                           Therefore, x = 0 is not in the domain.
If \(x < 0\), then \(y = \frac{1}{x} < 0\). The identity \(\cot^{-1}(y) = \tan^{-1}\left( \frac{1}{y}
\right)\) doesn't hold directly.                                                                             Let me continue the analysis:
I recall that for \(y < 0\), the following identity is true:                                                 From the verification, I can see that for x ≠ 0, tan⁻¹(x) = cot⁻¹(1/x). This means the expression
\[ \cot^{-1}(y) = \pi + \tan^{-1}\left( \frac{1}{y} \right) \]                                               simplifies to:
But, I'm not sure if this is accurate. Let me verify.                                                        sin(2tan⁻¹(x)) = 1/3
Looking at the range of \(\cot^{-1}(y)\):                                                                    Let me continue the mathematical reasoning:
- The range of \(\cot^{-1}(y)\) is \((0, \pi)\).
- For \(y > 0\), \(\cot^{-1}(y) = \tan^{-1}(1/y)\).                                                          Let θ = tan⁻¹(x), so x = tan(θ). Then we have:
- For \(y < 0\), \(\cot^{-1}(y) = \pi + \tan^{-1}(1/y)\).                                                    sin(2θ) = 1/3
But, \(\tan^{-1}(1/y)\) for \(y < 0\) will give a value between \(-\pi/2\) and \(0\). Adding \               Using the identity sin(2θ) = 2tan(θ)/(1 + tan²(θ)) = 2x/(1 + x²)
(\pi\) to it gives a value between \(\pi/2\) and \(\pi\), which is within the range of \
(\cot^{-1}(y)\).                                                                                             So the equation becomes:
                                                                                                             2x/(1 + x²) = 1/3
Thus, for \(x < 0\):
\[ \cot^{-1}\left( \frac{1}{x} \right) = \pi + \tan^{-1}(x) \]                                               Solving this:
                                                                                                             6x = 1 + x²
Now, the expression inside the sine becomes:                                                                 x² - 6x + 1 = 0
\[ \tan^{-1}(x) + \cot^{-1}\left( \frac{1}{x} \right) = \tan^{-1}(x) + \pi + \tan^{-1}(x) = \pi + 2
\tan^{-1}(x) \]                                                                                              Using the quadratic formula:
                                                                                                             x = [6 ± √(36 - 4)]/2 = [6 ± √32]/2 = [6 ± 4√2]/2 = 3 ± 2√2
Thus, the equation is:
\[ \sin(\pi + 2 \tan^{-1}(x)) = \frac{1}{3} \]                                                               Now I need to check if both solutions are valid. Let me verify if they satisfy the original equation:
I know that \(\sin(\pi + \theta) = -\sin(\theta)\). Therefore:                                               Lean verified proof steps:
\[ \sin(\pi + 2 \tan^{-1}(x)) = -\sin(2 \tan^{-1}(x)) = \frac{1}{3} \]                                         1.For x = 3 + 2√2, tan⁻¹(x) is defined since x > 0, and cot⁻¹(1/x) is also defined since 1/x > 0. The
                                                                                                                 sum tan⁻¹(x) + cot⁻¹(1/x) = 2tan⁻¹(x) is valid, and sin(2tan⁻¹(x)) = 2x/(1+x²) = 1/3, so this is a
But from the previous case, \(\sin(2 \tan^{-1}(x)) = \frac{2x}{1 + x^2}\). Therefore:                            valid solution.
\[ -\frac{2x}{1 + x^2} = \frac{1}{3} \]                                                                        2.For x = 3 - 2√2, since 3 - 2√2 ≈ 3 - 2.828 = 0.172 > 0, tan⁻¹(x) is defined and cot⁻¹(1/x) is also
                                                                                                                 defined. The sum tan⁻¹(x) + cot⁻¹(1/x) = 2tan⁻¹(x) is valid, and sin(2tan⁻¹(x)) = 2x/(1+x²) = 1/3,
Simplify:                                                                                                        so this is also a valid solution.
\[ \frac{-2x}{1 + x^2} = \frac{1}{3} \]
\[ -6x = 1 + x^2 \]                                                                                          Therefore, both solutions are valid.
\[ x^2 + 6x + 1 = 0 \]
                                                                                                             **Final Answer:** 3 + 2√2, 3 - 2√2
The solutions are:
\[ x = \frac{-6 \pm \sqrt{36 - 4}}{2} = \frac{-6 \pm \sqrt{32}}{2} = \frac{-6 \pm 4 \sqrt{2}}{2} =
-3 \pm 2 \sqrt{2} \]
Now, since \(x < 0\) in this case, we need to check both solutions:
1. \(x = -3 + 2 \sqrt{2} \approx -3 + 2.828 = -0.172 < 0\)
2. \(x = -3 - 2 \sqrt{2} \approx -3 - 2.828 = -5.828 < 0\)
Both solutions are negative, so both are valid.
...
### Summary of Solutions
From both cases, we have four potential solutions:
1. \(x = 3 + 2 \sqrt{2}\)
2. \(x = 3 - 2 \sqrt{2}\)
3. \(x = -3 + 2 \sqrt{2}\)
4. \(x = -3 - 2 \sqrt{2}\)
All of them satisfy the original equation, as verified.
### Final Answer
The solutions are \(\boxed{3 + 2 \sqrt{2}}\), \(\boxed{3 - 2 \sqrt{2}}\), \(\boxed{-3 + 2
\sqrt{2}}\), and \(\boxed{-3 - 2 \sqrt{2}}\).


Figure 8. Illustration of Hermes’s effect on chain-of-thought generation: the model attempts to solve the precalculus-768 problem from
the MATH500 dataset, and Hermes detects and corrects a hallucinated reasoning step.


C. Example of a Hermes corrected problem
Figure 8 shows a case where Hermes helps the LLM avoid pursuing an incorrect reasoning path, in this example, attempting
to prove that tan−1 (x) = cot−1 (1/x) for x < 0. The Lean-validated steps guide the model away from invalid proof
directions. We observe that LLMs often generate answers with unwarranted confidence and without verifying intermediate
steps. Our agent mitigates this behavior by enforcing step-by-step validation and stricter reasoning discipline.

D. Additional formalization examples across MATH and AIME datasets
Figures 9–11 and 12-14 show qualitative examples of formalized reasoning steps from the MATH500 and AIME datasets,
respectively. Each example pairs an informal natural-language step with its corresponding formal statement in Lean,
illustrating the kinds of arithmetic, combinatorial, and number-theoretic reasoning steps covered by our benchmark.




                                                                                                        18
                        HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs




Informal Step: Given that: −f (f (1)) = 4. − f (1) = 2 when f (x) = 2x . Prove that: f (f (f (1))) = f (4) = 24 =
16.
/-Formal Statement-/
theorem test (f : N → N) (h1 : f (f 1) = 4) (h2 : ∀ x, f x = 2^x) : f (f (f 1)) = 16
    ∧ f 4 = 16 := by
  sorry


                                    Figure 9. Example #1 of a MATH500 formalized step




Informal Step: Given 5 shirts, 6 pairs of pants, and 8 hats, the total number of outfits (one of each) is 5 × 6 × 8 =
240.
/-Formal Statement-/
theorem test : let shirts := Finset.range 5 let pants := Finset.range 6 let hats :=
    Finset.range 8 (shirts × pants × hats).card = 240 := by
  sorry


                                    Figure 10. Example #2 of a MATH500 formalized step




Informal Step: Given that 24( 242 4) is even, and the pattern shows that 24n ≡ 6 mod 10 when n is even, therefore
     (2424 )
24(24          )
                   ≡ 6 mod 10.
/-Formal Statement-/
theorem test : (Even (24^(24^24))) → (∀ n : N, Even n → 24^n ≡ 6 [MOD 10]) →
    (24^(24^(24^24)) ≡ 6 [MOD 10]) := by
  sorry


                                    Figure 11. Example #3 of a MATH500 formalized step




                                                           19
                   HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs




Informal Step: Given a positive integer N = 34 × 52 , the set A of positive integer divisors of N consists of all
numbers of the form 3a × 5b where 0 ≤ a ≤ 4 and 0 ≤ b ≤ 2. The number of such divisors is (4 + 1) × (2 + 1) = 15.
/-Formal Statement-/
theorem test : let N := 3^4 * 5^2 let A := {d : N | ∃ a b, a \leq 4 ∧ b \leq 2 ∧ d =
    3^a * 5^b} (∀ x, x ∈ Nat.divisors N ↔ x ∈ A) ∧ ((Nat.divisors N).card = (4 + 1) *
     (2 + 1)) ∧ ((4 + 1) * (2 + 1) = 15) := by
  sorry


                                  Figure 12. Example #1 of an AIME formalized step




Informal Step: Given that: If d divides 3(d + 1)(d2 − 4d + 13) and d is coprime to d + 1, then d divides
3(d2 − 4d + 13). Prove that: The positive integers n such that n + 2 divides 3(n + 3)(n2 + 9) are n = 1, 11, and
37. Their sum is 1 + 11 + 37 = 49.
/-Formal Statement-/
theorem test : (∀ d : Z, d | 3 * (d + 1) * (d^2 - 4*d + 13) → Int.gcd d (d + 1) = 1 →
     d | 3 * (d^2 - 4*d + 13)) → {n : N | n > 0 ∧ (n + 2 : Z) | 3 * (n + 3) * (n^2 +
    9)} = {1, 11, 37} ∧ 1 + 11 + 37 = 49 := by
  sorry


                                  Figure 13. Example #2 of an AIME formalized step




Informal Step: Prove that: Given that the total number of ways is 9!×56×(3!)6 , we compute the prime factorization:
9! = 27 × 34 × 5 × 7; 56 = 23 × 7; (3!)6 = 26 × 36 . Multiplying yields 2( 7 + 3 + 6) × 3( 4 + 6) × 51 × 7( 1 + 1) =
21 6 × 31 0 × 51 × 72 .
/-Formal Statement-/
theorem test : 9! = 2^7 * 3^4 * 5 * 7 ∧ 56 = 2^3 * 7 ∧ (3!)^6 = 2^6 * 3^6 ∧ 9! * 56 *
    (3!)^6 = 2^16 * 3^10 * 5 * 7^2 := by
  sorry


                                  Figure 14. Example #3 of an AIME formalized step




                                                        20
                        HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

Table 7. Mean accuracy (%) ± standard deviation of various models under four inference strategies: zero-shot CoT (@1), majority
vote (@5), reward-model selection (Best-of-5), and Hermes (@1). Results are averaged over five independent runs on two benchmarks:
MATH500 and AIME’25

                              Qwen3-8B                OpenAI o3-mini              DeepSeek-V3.1               DeepSeek-V3.2
                       MATH500       AIME’25       MATH500       AIME’25      MATH500       AIME’25      MATH500        AIME’25
 CoT@1                 85.7 ± 0.7    18.7 ± 2.7   96.2 ± 0.3    71.3 ± 5.0    95.6 ± 0.7    48.0 ± 3.4   96.6 ± 0.6    49.3 ± 3.9
 CoT@5+Majority        86.8 ± 0.3    20.0 ± 2.1   96.5 ± 0.3    64.7 ± 3.4    96.9 ± 0.2    48.0 ± 3.4   97.2 ± 0.5    58.7 ± 5.8
 CoT@5+Skywork         90.9 ± 0.2    30.7 ± 2.5   96.4 ± 0.4    72.0 ± 5.8    96.7 ± 0.1    52.0 ± 2.7   97.3 ± 0.1    60.0 ± 4.7
 CoT@5+ArmoRM          89.2 ± 0.5    30.7 ± 2.5   96.1 ± 0.5    72.0 ± 5.8    96.4 ± 0.5    55.3 ± 1.6   97.0 ± 0.2    55.3 ± 1.6
 CoT@5+Shepherd        86.9 ± 0.7    25.3 ± 3.4   96.1 ± 0.2    70.0 ± 7.0    96.4 ± 0.4    57.3 ± 5.7   96.7 ± 0.3    57.3 ± 5.7
 CoT@5+RLHFlow         83.6 ± 0.3    24.0 ± 3.9   95.8 ± 0.4    65.3 ± 4.0    96.0 ± 0.7    50.0 ± 2.1   95.5 ± 0.2    53.3 ± 3.7
 Lean-based methods
 CoT@5+Safe            89.1 ± 0.3    22.0 ± 1.6   95.5 ± 0.3    80.0 ± 3.0    96.0 ± 0.3    45.3 ± 2.7   97.1 ± 0.2    46.7 ± 2.1
 CoT@5+Safe*           89.2 ± 0.4    21.3 ± 3.4   96.4 ± 0.4    80.7 ± 2.5    96.4 ± 0.5    50.0 ± 3.7   97.3 ± 0.2    52.7 ± 2.5
 Hermes@1              91.3 ± 1.1    28.0 ± 1.6   97.0 ± 0.7    84.0 ± 2.5    97.2 ± 0.5    66.7 ± 3.0   98.2 ± 0.4    74.7 ± 5.4



E. Additional results on benchmark results
Complementing Table 1, we report the mean and standard deviation for all inference methods on the MATH500 and
AIME’25 datasets, based on five independent runs. We observe that the performance of Hermes is stable, with variance
comparable to that of CoT and RM-augmented baselines.




                                                               21
                        HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

F. Hermes Algorithm

Algorithm 1 Hermes Pseudocode
  Input: Step st , Memory Database D, Hyperparameters Kf , Kp , k
  Output: Tuple (st , status, D)

  C ← R ETRIEVE T OP K(D, st , k)                                         ▷ Retrieve top-k relevant correct steps from database
  S ← st ∪ C                                                                                   ▷ Augment context with retrieval
  status ← V ERIFICATION FAILURE

  for i = 1 to Kf do
     ft ← πf (S)                                                                                             ▷ Translate to Lean
     if REPL(ft ) is True then
        s̃t ← BackTranslation(ft )
        if st ≈ s̃t then
            break                        ▷ Exit Formalization Module only when both REPL and Backtranslation are passed
        end if
     end if
  end for
  if ft = ∅ then
     Return (st , status, D)             ▷ Verification failure is returned if no translation passed REPL and backtranslation
  end if

  for j = 1 to Kp do
    p+t ← πp (·|ft )                                                                                            ▷ Proof for goal
    p−t ← πp (·|¬ft )                                                                                   ▷ Proof for counter-goal
    if REPL(p+  t ) is True then
       status ← C ORRECT S TEP
       D ← D ∪ {st }                                                                                          ▷ Update database
       break
    else if REPL(p−   t ) is True then
       status ← R EVISE S TEP
       break
    end if
  end for
  Return (st , status, D)

The Hermes algorithm (Algorithm 1) takes a natural language reasoning step st , a memory database D, hyperparameters
Kf , Kp for sampling formalizations and proofs, and retrieval parameter k. It begins by retrieving the top-k relevant, verified
steps from D using cosine similarity of vectors that represent embedded proof steps to augment the context S. The algorithm
then attempts to formalize the step into Lean code (ft ) using a formalizer policy πf , repeating up to Kf times until a
candidate passes both REPL verification and semantic consistency checks via back-translation. If formalization fails, the
step is marked as a verification failure. Otherwise, the algorithm proceeds to the prover module, which attempts to generate
                                                                         −
a valid Lean4 proof for either the initial goal (p+t ) or its negation (pt ) up to Kp times. If a proof for the statement is found,
the step is marked as correct and added to the database D; if a counter-example/proof is found, the step is flagged and LLM
is instructed to explore other proof steps; if neither goal was proved, the agent returns verification failure signal back to the
reasoning LLM.




                                                                22
                       HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

G. Distribution of successfully proved problems by math topic under different inference strategies
To better understand the impact of our agent on the underlying reasoning models, we analyze the distribution of solved
problems across different mathematical topics from MATH500 (Tables 8, 9, 10, 11) and HardMath2 (Tables 12, 13, 14,
15). Our results indicate that most mathematical domains benefit from the inclusion of Lean-based verification, although
a few topics experience slight performance drops. Geometry, for instance, shows lower gains, which we attribute to the
limited availability of geometry-related theorems in Mathlib, the primary mathematical library for Lean. Furthermore, we
observe that certain reward models exhibit domain-specific strengths: for example, Skywork consistently performs better
in geometry-related tasks. Overall, we expect that as Lean and Mathlib continue to evolve, these performance gaps will
diminish, and the verification capabilities of our agent will further improve with future updates to theorem provers and
supporting libraries.

           Table 8. Distribution of correct answers by topic on MATH500 for the DeepSeek-V3.1 base reasoning model.

                                     Counting &                    Intermediate    Number        Pre-       Pre-
                         Algebra                     Geometry
                                     Probability                     Algebra       Theory      algebra    calculus
            ZS-CoT         123            33             35             91            62          78         52
            Hermes         124            36             36             93            62          80         56
            Skywork        123            35             39             92            62          77         55
            ArmoRM         123            35             39             89            62          76         54
            Shepherd       123            36             38             92            62          77         53
            RLHFlow        123            34             35             91            62          79         53


           Table 9. Distribution of correct answers by topic on MATH500 for the DeepSeek-V3.2 base reasoning model.

                                     Counting &                    Intermediate    Number        Pre-       Pre-
                         Algebra                     Geometry
                                     Probability                     Algebra       Theory      algebra    calculus
            ZS-CoT         124            36             34             93            61          81         53
            Hermes         123            36             39             96            61          81         55
            Skywork        124            36             35             96            61          80         55
            ArmoRM         124            36             36             94            61          80         55
            Shepherd       124            36             35             95            62          78         55
            RLHFlow        124            36             36             95            62          80         53


              Table 10. Distribution of correct answers by topic on MATH500 for the o3-mini base reasoning model.

                                     Counting &                    Intermediate    Number        Pre-       Pre-
                         Algebra                     Geometry
                                     Probability                     Algebra       Theory      algebra    calculus
            ZS-CoT         124            38             35             89            62          77         54
            Hermes         124            37             37             93            61          79         55
            Skywork        123            37             36             94            62          77         55
            ArmoRM         124            37             35             93            61          76         55
            Shepherd       124            38             35             91            62          78         54
            RLHFlow        123            37             36             91            61          78         53




                                                              23
              HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs

   Table 11. Distribution of correct answers by topic on MATH500 for the Qwen3-8B base reasoning model.

                              Counting &                    Intermediate   Number        Pre-      Pre-
                Algebra                       Geometry
                              Probability                     Algebra      Theory      algebra   calculus
  ZS-CoT          120             28              27            70           60          75           44
  Hermes          123             33              31            84           61          77           47
  Skywork         120             32              32            82           62          77           50
  ArmoRM          118             31              31            80           62          75           46
  Shepherd        121             31              29            72           61          77           48
  RLHFlow         118             28              23            72           58          73           48


Table 12. Distribution of correct answers by topic on HARDMath2 for the DeepSeek-V3.1 base reasoning model.

                    asympytotic        boundary                nonlinear   nonlinear
                                                   integrals                             other   wkb
                       series           layers                   ode         pde
      ZS-CoT              0              22             9            2         8          3       4
      Hermes              0              28            10            3        14          3       6
      Skywork             0              23             8            3        16          3       7
      ArmoRM              0              21            10            3        12          3       7
      Shepherd            0              21             9            2        17          2       8
      RLHFlow             0              20             8            1        17          1       7


Table 13. Distribution of correct answers by topic on HARDMath2 for the DeepSeek-V3.2 base reasoning model.

                    asympytotic        boundary                nonlinear   nonlinear
                                                   integrals                             other   wkb
                       series           layers                   ode         pde
      ZS-CoT              0              23             8            2        13          3       9
      Hermes              0              28            10            3        14          3       6
      Skywork             0              25            10            1        17          3       9
      ArmoRM              0              23             8            2        15          3       9
      Shepherd            0              23             7            2        15          3       9
      RLHFlow             0              21             6            3        14          2       6




                                                       24
           HERMES: Towards Efficient and Verifiable Mathematical Reasoning in LLMs




 Table 14. Distribution of correct answers by topic on HARDMath2 for the o3-mini base reasoning model.

                  asympytotic     boundary                 nonlinear    nonlinear
                                               integrals                             other    wkb
                     series        layers                    ode          pde
    ZS-CoT             0             14           10           3            13         1        8
    Hermes             1             25           10           3            16         1       10
    Skywork            1             22           10           1            19         1        8
    ArmoRM             1             21           11           3            16         1        7
    Shepherd           0             12           12           3            17         1        9
    RLHFlow            2             21           10           2            16         1        8




Table 15. Distribution of correct answers by topic on HARDMath2 for the Qwen3-8B base reasoning model.

                  asympytotic     boundary                 nonlinear    nonlinear
                                               integrals                             other    wkb
                     series        layers                    ode          pde
    ZS-CoT             0              0            6           3             0         0        0
    Hermes             0              2            8           2             0         0        2
    Skywork            0              0            7           3             0         0        2
    ArmoRM             0              0            6           3             0         0        2
    Shepherd           0              0            7           3             0         0        2
    RLHFlow            0              0            7           3             0         0        2




                                                  25
