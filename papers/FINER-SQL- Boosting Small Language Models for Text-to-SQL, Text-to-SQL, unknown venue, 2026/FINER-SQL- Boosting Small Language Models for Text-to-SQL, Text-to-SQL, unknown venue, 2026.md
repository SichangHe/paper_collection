                                            FINER-SQL: Boosting Small Language Models for
                                                            Text-to-SQL
                                                                 Thanh Dat Hoang1 , Thanh Trung Huynh2 , Matthias Weidlich3 , Thanh Tam Nguyen1 ,
                                                                             Tong Chen4 , Hongzhi Yin4* , Quoc Viet Hung Nguyen1*
                                        1
                                            Griffith University (Australia), 2 VinUniversity (Vietnam), 3 Humboldt-Universitat zu Berlin (Germany), 4 The University of Queensland (Australia)


                                           Abstract—Large language models have driven major advances
                                        in Text-to-SQL generation. However, they suffer from high
                                        computational cost, long latency, and data privacy concerns,
arXiv:2605.03465v1 [cs.DB] 5 May 2026




                                        which make them impractical for many real-world applications.
                                        A natural alternative is to use small language models (SLMs),
                                        which enable efficient and private on-premise deployment. Yet,
                                        SLMs often struggle with weak reasoning and poor instruction
                                        following. Conventional reinforcement learning methods based on
                                        sparse binary rewards (0/1) provide little learning signal when the
                                        generated SQLs are incorrect, leading to unstable or collapsed
                                        training. To overcome these issues, we propose FINER-SQL, a
                                        scalable and reusable reinforcement learning framework that
                                        enhances SLMs through fine-grained execution feedback. Built on
                                        group relative policy optimization, FINER-SQL replaces sparse
                                        supervision with dense and interpretable rewards that offer                Fig. 1. Execution accuracy (EX%) of FINER-SQL on BIRD dev. Although
                                        continuous feedback even for incorrect SQLs. It introduces two             SLMs are often overlooked due to their perceived weakness in reasoning, our
                                        key reward functions: a memory reward, which aligns reasoning              3B model outperforms many >14B baselines and even proprietary systems.
                                        with verified traces for semantic stability, and an atomic reward,
                                        which measures operation-level overlap to grant partial credit             of inference at scale can be extremely high. For instance,
                                        for structurally correct but incomplete SQLs. This approach                CHESS-style schema linking consumes over 340K tokens per
                                        transforms discrete correctness into continuous learning, enabling         request (over $850 per 1,000 requests with GPT-4o), even
                                        stable, critic-free optimization. Experiments on the BIRD and              before generating and selecting SQL candidates, as shown in
                                        Spider benchmarks show that FINER-SQL achieves up to 67.73%
                                        and 85% execution accuracy with a 3B model – matching much                 recent analyses [10], [20]. Such expenses are unsustainable
                                        larger LLMs while reducing inference latency to 5.57 s/sample.             for many real-world deployments, motivating the adoption of
                                        These results highlight a cost-efficient and privacy-preserving            self-hosted solutions that are both cost-efficient and privacy-
                                        path toward high-performance Text-to-SQL generation. Our code              preserving [21]–[25].
                                        is available at https://github.com/thanhdath/finer-sql.
                                           Index Terms—Text-to-SQL, Small Language Models
                                                                                                                      A natural direction is to employ small language models
                                                                                                                   (SLMs, 0.5B–3B parameters), which run efficiently on a single
                                                                       I. I NTRODUCTION                            12–24GB GPU (e.g., RTX 4090). SLMs are appealing for
                                                                                                                   lightweight, on-premise deployment, but applying them to
                                           Text-to-SQL aims to translate natural language utterances
                                                                                                                   Text-to-SQL remains nontrivial. They suffer from (i) weak
                                        into executable SQL queries, enabling non-experts to interact
                                                                                                                   reasoning capability, leading to poor SQL generation, and (ii)
                                        with databases seamlessly. The task is inherently challenging
                                                                                                                   limited instruction-following and formatting, producing invalid
                                        due to the need for compositional reasoning, schema linking,
                                                                                                                   or incomplete SQL [26]–[28]. As a result, most SQL queries
                                        and handling ambiguous user intents [1]–[6]. Recent years
                                                                                                                   from SLMs are incorrect or unexecutable, leading to very low
                                        have seen remarkable progress driven by large language mod-
                                                                                                                   accuracy.
                                        els (LLMs), which achieve state-of-the-art performance on
                                        benchmarks such as Spider and BIRD [7]–[9]. Most of these                     Recent advances in reinforcement learning (RL) have im-
                                        methods rely on large open-source models or proprietary APIs               proved the reasoning abilities of LLMs, often using policy
                                        (e.g., GPT-4, Claude), achieving high accuracy through chain-              optimization methods such as PPO [29] or GRPO [30]. These
                                        of-thought reasoning and multi-stage pipelines [10]–[14].                  works typically train models of at least 7B parameters, using
                                           Despite their success, LLM-based solutions introduce sig-               execution accuracy as the primary reward—a binary signal that
                                        nificant practical constraints. First, relying on external APIs            gives 1 for a fully correct query and 0 otherwise [31]–[34].
                                        poses privacy risks, as sensitive database schemas and user                While such sparse rewards can help large models refine their
                                        queries must be transmitted to third-party servers, poten-                 reasoning, they are ineffective for SLMs, where most attempts
                                        tially violating confidentiality [15]–[19]. Second, the cost               fail and thus receive zero signal. As a result, reinforcement
                                                                                                                   learning on small models often collapses or stagnates. To be
                                             * Corresponding authors                                               effective, SLMs require fine-grained and informative rewards
that can recognize partial correctness and provide continuous        Preference Optimisation (DPO) [40] and Odds-Ratio Prefer-
feedback even when the final SQL is wrong.                           ence Optimisation (ORPO) [41]–[43] eliminate explicit reward
   In this work, we introduce FINER-SQL [35] (Fine-grained           models and directly optimise preference pairs for improved
Execution feedback for Reinforcement learning in Text-               stability and lower cost. In contrast, online methods including
to-SQL), a reinforcement learning framework tailored for             PPO and Group Relative Policy Optimisation (GRPO) [30]
small language models. Unlike prior LLM-heavy approaches             rely on real-time rollouts, with GRPO further removing the
that rely on 7B–32B parameter models or external APIs,               value model and estimating advantages via relative candidate
FINER-SQL targets the SLM regime (≤3B), where failures               scoring. Our work adapts GRPO to train SLMs for Text-to-
dominate and dense rewards are essential. The model is               SQL, improving execution accuracy through feedback-based
trained with Group Relative Policy Optimization (GRPO),              optimisation without a separate value model.
avoiding a separate value model, and augments standard               Text-to-SQL. Text-to-SQL research has evolved from early
execution and format rewards with two dense signals: (i)             neural models such as Seq2SQL [44] and SQLNet [45] to
memory rewards compare the model’s reasoning to a bank               grammar- and relation-aware systems including IRNet [46],
of verified traces, offering stability even when execution fails;    SyntaxSQLNet [47], and RAT-SQL [1], with constrained
(ii) atomic rewards score overlap between predicted and gold         decoding methods like PICARD [48]–[50] improving syn-
queries at the operation level, giving credit to partially aligned   tactic validity. The emergence of large pretrained language
SQLs. These signals turn binary correctness into continuous          models shifted the paradigm toward prompting-based and
feedback, revealing how far an incorrect query is from the           multi-stage pipelines (e.g. SQL-PaLM [51], DIN-SQL [52],
target and which components need refinement.                         CHESS [10], [53]–[55]), integrating planning, reranking, and
   As shown in Fig. 1, despite their compact size, our               execution feedback but relying heavily on proprietary LLMs.
FINER-SQL 3B variant attains 67.73% execution accuracy               More recently, reinforcement learning approaches such as
on the BIRD dataset, outperforming many open-source models           Arctic-Text-to-SQL-R1 [31], SQL-o1 [56], and Ex-CoT [32]
exceeding 14B parameters and even some proprietary systems.          have shown that execution feedback improves compositional
   We summarize our contributions as follows:                        generalization, though these methods typically target large
    • We propose FINER-SQL, a scalable and reusable rein-            (≥7B) models and depend on sparse binary rewards, limiting
      forcement learning framework designed to boost Text-to-        applicability to smaller models [57]–[59]. Our FINER-SQL
      SQL performance of small models through fine-grained           introduces dense, interpretable rewards that provide continuous
      execution feedback.                                            feedback on reasoning and SQL structure, enabling effective
    • We introduce a memory reward mechanism that effi-              reinforcement learning for small models.
      ciently evaluates the reasoning traces of SLMs against
      verified reasoning patterns, enhancing logical consistency                     III. M ODEL AND C HALLENGES
      and training stability.
                                                                     A. Problem Formulation
    • We design atomic operation rewards that compute fine-
      grained structural similarity between generated and gold          Text-to-SQL addresses the task of generating an SQL query
      SQLs, mitigating the sparse reward problem.                    Y that corresponds to a given natural language question q.
    • Comprehensive experiments on Spider and BIRD show                                       Y = f (q, S, K | θ),
      that FINER-SQL significantly improves execution accu-          where the function f (· | θ) represents a generative model
      racy and generalization of small models, matching much         (e.g., a neural network) with learnable parameters θ [60],
      larger LLMs at a fraction of the cost. Our 3B model            [61]. This query is constructed based on a database schema S
      achieves 67.73% execution accuracy on BIRD Dev with            and, optionally, an external knowledge base K. The database
      only 5.57s per sample.                                         schema S is defined by a set of tables {T1 , T2 , . . . , Tm }, a
   In the remainder, §II discusses related work. §III formulates     set of columns {C1 , C2 , . . . , Cn }, and a set of foreign key
the Text-to-SQL problem and RL challenges for SLMs. §IV              relations {R1 , R2 , . . . , Rk }. The optional external knowledge
presents the FINER-SQL framework and its two-stage design.           K provides context for the schema, aiding in generating more
§V reports experimental results and conclusions (§VI).               accurate SQL in ambiguous situations [62]–[64].
                     II. R ELATED W ORK
                                                                     B. Challenges
Reinforcement Learning for LLMs. Reinforcement learning
has been widely used to enhance the reasoning abilities of              We argue that any reinforcement learning approach applied
large language models (e.g. DeepSeek-R1 [36], OpenAI’s O-            to SLMs for Text-to-SQL must effectively address the follow-
series) in mathematics, logic, and code generation via reward-       ing fundamental challenges:
based optimisation. Building on the Reinforcement Learning             (R1) Weak Reasoning Capability. SLM-based Text-to-SQL
from Human Feedback (RLHF) paradigm [37], these methods              systems must address limited reasoning capabilities. Chain-of-
align model behaviour with human preferences using a reward          thought prompting, effective for large models, is unreliable for
model and Proximal Policy Optimisation (PPO) [29], [38],             SLMs, often yielding illogical reasoning [65] and inaccurate
[39] under a KL constraint. Offline approaches such as Direct        SQL generation on complex schemas [66].
   (R2) Low Instruction Following Capability. SLMs struggle          (e.g., DeepSeek-R1, GPT-oss-120B), the line “Follow this
with instruction following due to limited size [67] and lack         exact response format:” is omitted, since these models natively
of diverse tuning data like InFoBench [68] and IFEval [69].          generate reasoning enclosed within <think>...</think> and
Consequently, they generalize poorly to complex instructions         we just need to modify the prompt so that the final SQL
and frequently ignore structural constraints (e.g., <think>          is returned without additional instruction. The accompany-
tags), hindering reliable SQL extraction.                            ing user prompt provides the structured task inputs, namely
   (R3) Sparse Reward Issue. RL for Text-to-SQL typically            the database schema, the natural-language question, and any
uses sparse execution rewards [44], [70], offering no credit for     optional external knowledge. This design enforces a unified
partial correctness (e.g., valid joins) and hindering fine-grained   output structure across all teacher models, ensuring that each
policy learning [30], [71]–[73]. Since SLMs often generate           completion conforms to the canonical form:
invalid initial SQLs, this results in negligible learning signals.      ⟨q, schema⟩ → ⟨< think > reasoning < /think > SQL⟩
Prior work in math and code indicates that process-level
rewards improve convergence [71], [72], [74], highlighting the          The resulting multi-source reasoning traces are aggregated
need for shaped, step-level feedback in SLMs.                        into a Reasoning Bank, providing the SLM with diverse
                                                                     reasoning styles and compositional strategies across different
   (R4) High Cost of Explicit Reward Modeling. Process               teacher architectures. We then perform supervised fine-tuning
Reward Models (PRMs) offer fine-grained feedback [40],               (SFT) on this distilled corpus to transfer structured reasoning
[71], [74] but face high costs and adaptation needs [30]. In         and SQL generation ability to the smaller model. This step
Text-to-SQL, evaluating schema linking and partial executions        also enables the SLM to quickly adapt to the required output
adds complexity. Commercial verifiers often yield unreliable         format, as it learns to generate reasoning traces followed
judgments [8], [75] and incur prohibitive costs (e.g., $2400 for     by valid SQL structures from the beginning of training.
10k queries [76]), making them impractical for iterative RL.         Importantly, we do not filter out teacher samples with failed
   IV. FINER-SQL: R EINFORCEMENT L EARNING WITH                      executions, since the purpose of this stage is not to achieve
         F INE -G RAINED E XECUTION F EEDBACK                        execution correctness but to expose the model to a wide variety
                                                                     of reasoning trajectories and compositional patterns. Although
   Motivated by the challenges identified in §III-B, we propose
                                                                     the execution accuracy of teacher models on the BIRD training
FINER-SQL, a two-stage framework that enhances Text-to-
                                                                     set is around 50–60%, these imperfect yet diverse examples
SQL performance of SLMs through (1) reasoning distillation
                                                                     still provide valuable reasoning supervision that helps the SLM
from large reasoning models and (2) reinforcement learning
                                                                     develop robust structural understanding. We generated 37.6K
with fine-grained execution feedback, as illustrated in Fig. 2.
                                                                     distillation samples (4 teachers × BIRD training set) for only
A. Distillation - Diverse Reasoning Style for SLMs                   ∼$30. This cost was minimized by employing GRAST-SQL
     a) Reasoning Bank Construction: To address weak rea-            [77], an efficient schema-linking method, to restrict inputs to
soning and limited instruction-following capabilities (R1, R2),      the top-30 columns instead of the entire large schema.
we first distill diverse reasoning knowledge from a pool of
large reasoning models, including DeepSeek-R1, GPT-oss-                    b) Supervised Fine-Tuning Process: Given a Reasoning
120B, Qwen-2.5-72B-Instruct, and OpenAI GPT-4o. Given a              Bank containing diverse reasoning-SQL pairs distilled from
question-schema pair, each teacher model is prompted with            multiple teacher models, we perform supervised fine-tuning to
a structured instruction consisting of two messages: a system        transfer their structured reasoning and compositional knowl-
prompt that defines the response rules and a user prompt that        edge to the smaller model. During fine-tuning, we optimize
provides the database schema, natural-language question, and         the SLM only on the completion tokens – i.e., the reasoning
optional external knowledge.                                         and SQL segments – while excluding prompt tokens such as
                                                                     schema descriptions or external context. This ensures that the
   System Prompt for Teacher Models                                  model learns to reproduce reasoning paths and final SQLs
   You are a meticulous SQL expert. Generate a                       without memorizing database-specific content. The supervised
   single, correct SQL query for the user question
   and the provided database schema.                                 fine-tuning loss is formulated as:
   Follow this exact response format:                                                             τ
   <think>                                                                                       X
   Briefly reason about the steps to form the SQL.
   </think>
                                                                                Lcompletion = −       log Pθ (yj | y<j , χ).    (1)
   SQL statement                                                                              j=C+1
   Rules:                                                            where C marks the end of the prompt tokens, τ is the
   - Output exactly one SQL statement.
   - The SQL must be executable on SQLite.                           total sequence length, yt is the target completion token, χ
   - Do not include any explanatory text outside the
   <think> section.                                                  denotes the prompt, and Pθ is the model’s predicted probability
   - After </think>, output one SQL statement only.
   Do not include any extra text, tags.                              distribution parameterized by θ.

   As shown in the system prompt above, the prompt ex-                  Through this process, the SLM acquires structured reason-
plicitly constrains teachers to output a concise reasoning           ing ability, format obedience, and generalization over diverse
trace enclosed within <think> tags followed by a single              reasoning patterns—forming a strong initialization for the
executable SQL statement for SQLite3. For reasoning models           subsequent reinforcement learning stage.
Fig. 2. Overall training pipeline of FINER-SQL. Step 1: Distillation - Diverse Reasoning Style for SLMs. Teacher models (e.g., GPT-4o, DeepSeek-
R1, Qwen-2.5-72B) are prompted with question-schema pairs to produce reasoning traces and SQLs, forming a Reasoning Bank with diverse plan and
SQL styles. The SLM is initialized via supervised fine-tuning on this corpus to obtain policy π1 with structured reasoning ability. Step 2: Reinforcement
Learning from Execution Feedback. The finetuned policy generates multiple rollouts per query and is optimized using GRPO with dense, interpretable
reward signals—including format, memory, execution, and atomic rewards—to improve reasoning faithfulness and SQL accuracy.

B. Reinforcement Learning from Execution Feedback                                • Memory Reward evaluates the semantic alignment of a
   To address the challenges of sparse and costly supervision                      generated reasoning trace with a set of verified reasoning
signals (R3, R4), the distilled SLM is further optimized                           prototypes, particularly when the SQL execution fails. It
through reinforcement learning using fine-grained execution                        assigns a continuous score Rmem ∈ [0, 1] based on embed-
feedback. For each training instance, the model samples a                          ding similarity between the generated reasoning and gold
group of G rollouts {r1 , . . . , rG }, where each rollout includes                reasoning traces retrieved from diverse databases. This
a reasoning trace and its corresponding SQL prediction. In-                        reward serves two purposes: (i) it estimates the likelihood
stead of relying on a binary execution signal, we design a                         that the reasoning path is logically valid, and (ii) it
dense composite reward that reflects different dimensions of                       regularizes the model to follow the diverse reasoning
SQL quality and reasoning consistency. The reward comprises                        styles distilled from teacher models rather than generating
four complementary components:                                                     noisy or unfocused reasoning. A detailed formulation is
   • Format Reward encourages the model to follow the                              provided in §IV-C.
     standardized <think>-SQL structure, where the reason-                       • Atomic Reward captures structural similarity between

     ing process and executable SQL are clearly separated                          the predicted and reference SQLs by decomposing each
     for reliable parsing and evaluation. Although the distilled                   query into a list of atomic operations—such as FROM,
     policy π1 from §IV-A often generates correctly formatted                      JOIN, and WHERE_PRED—and measuring their overlap.
     outputs, the format reward remains essential during rein-                     Each SQL is parsed into an operation set, and the reward
     forcement learning, as exploration may cause the model                        assigns a continuous score Ratomic ∈ [0, 1] proportional to
     to deviate from ( the expected structure. Formally,                           the intersection ratio between the predicted and ground-
                         1, if the output follows the format                       truth operation sets. This fine-grained feedback provides
        Rformat (s) =                                                              partial credit for structurally correct components, encour-
                         0, otherwise.                                             aging the model to progressively assemble a complete and
   • Execution Reward assesses the executable correctness of                       executable query, as detailed in §IV-D. The atomic reward
     the generated SQL. Queries that fail to run receive zero                      is activated only when the predicted SQL is incorrect.
     reward. If the SQL executes successfully but produces
                                                                                 The overall reward for each rollout is defined as the un-
     an incorrect result, a base credit of 1.0 is assigned for
                                                                              weighted sum of all components:
     syntactic and runtime validity. When the predicted and
     ground-truth outputs match exactly, the model receives                               R = Rformat + Rexec + Ratomic + Rmem ,
     the maximum reward
                             of 2.0:                                         When an SQL fails to execute, the atomic and memory rewards
                      0, if the SQL fails to execute;
                                                                             provide fallback supervision, allowing the policy to continue
      Rexec (s | q) = 1, if executable without syntax error;                  learning from structurally or semantically meaningful rollouts.
                      
                      
                        2, if results match exactly.                             For optimization, we employ GRPO [30], which estimates
                                                                              • S is the latent state space.
                                                                              • A ⊂ V L represents the action space, where each action
                                                                                is a sequence sampled from the language model’s vocab-
                                                                                ulary V , with L denoting the maximum length of the
                                                                                generated text.
                                                                              • P : S × A → S is the transition function updating the
                                                                                state based on the generated action.
                                                                                        N
                                                                              • G ⊂ V     denotes the goal space, representing the set of
Fig. 3. Reward scaling across prediction quality levels. Each stacked
bar shows how individual rewards (Format, Execution, Atomic, Memory)            executable SQL queries that satisfy the user intent.
contribute under increasing SQL correctness—from wrong format to fully        • R : S × A × G → R represents the goal-conditioned
correct execution. The scaling illustrates that FINER-SQL replaces binary
rewards with a smooth, continuous feedback space, ensuring dense and
                                                                                reward function.
interpretable credit assignment throughout training.                          • O is the set of observations o ∈ O, capturing the visible
                                                                                context (question, schema) available to the model.
relative advantages across a group of G rollouts for each
                                                                              In this framework, the objective of the policy πθ is to
instance. This approach eliminates the need for a separate
                                                                            maximize the expected return, i.e., the expected total reward
critic or reward model, enabling stable policy improvement
                                                                            accumulated over a rollout: "
with reduced computational cost.                                                                          X H
                                                                                                                            #
Reward composition and scaling. To illustrate the behav-                                  J(θ) = Eξ∼πθ        R(st , at , g) ,
ior and relative range of each reward, Fig. 3 visualizes                                                     t=1
                                                                            where ξ = (sP   1 , a1 , . . . , sH , aH ) denotes a rollout sampled
how rewards accumulate across representative prediction cate-                                  H
gories—ranging from wrong format to correct execution. The                  from πθ , and t=1 R(st , at , g) is the cumulative reward of
Format Reward (orange) is always computed first and bounded                 that rollout. A fundamental challenge in applying reinforce-
in {0, 1}, acting as a gate that ensures structural validity.               ment learning to LLMs is the vastness of the action space
Subsequent rewards, Execution (blue), Atomic (yellow), and                  A ⊂ V L . The set of valid reasoning paths Tvalid ⊂ A
Memory (gray), expand upon this baseline, demonstrating how                 leading to a goal g ∈ G is combinatorially large. A policy
partial correctness is progressively credited even before perfect           trained solely on sparse execution signals (Rexec ∈ {0, 1})
execution is achieved. This scaling visualization highlights                tends to explore this space unconstrained, developing high
the dense nature of our reward design: every stage of im-                   variance. Concretely, given an observation o ∈ O (i.e., a
provement, from valid syntax to full correctness, produces a                question–schema prompt), the policy samples a group of
measurable and interpretable reward increase.                               rollouts {ξj }Kj=1 by stochastic decoding with temperature
                                                                            T , and each rollout is scored by the composite reward. At
C. Memory Reward: Reasoning-SQL Semantic Alignment                          inference, we follow the same sampling protocol, drawing
                                                                            K candidate generations under temperature T and select the
     a) Motivation: The output of SLMs consists of a
                                                                            best SQL via majority voting; in practice, diverse reasoning
<think> reasoning trace followed by the generated SQL,
                                                                            traces often lead to diverse SQL structures, which fragment
where the SQL quality directly depends on the reasoning.
                                                                            candidates into more execution groups (i.e., K distinct SQLs)
When the SQL fails to execute, evaluating only the final
                                                                            and thus cause vote dilution, where no single group secures a
output discards meaningful reasoning progress and destabilizes
                                                                            decisive majority.
learning. We therefore propose the Memory Reward, which
evaluates the reasoning itself based on its semantic similarity                To mitigate this effect, we introduce the Memory Reward
to successful reasoning traces stored in memory. This reward                (Rmem ) as a regularization signal that promotes reasoning
serves two purposes: (1) it promotes reasoning consistency                  consistency: by assigning higher scores to rollouts whose
by anchoring updates around coherent and previously verified                reasoning traces align with verified memory prototypes, the
reasoning patterns, mitigating logical variance among the K                 policy shifts probability mass toward a smaller set of coherent
sampled candidates to prevent fragmented execution groups,                  reasoning patterns, causing candidates to cluster into fewer
thereby ensuring higher consensus during majority voting;                   execution groups and yielding higher consensus during infer-
and (2) it acts as a semantic regularizer that concentrates                 ence. We define a manifold of verified reasoning prototypes
the model’s probability mass on valid structural prototypes,                Tmem ⊂ Tvalid , representing the high-quality traces stored
preventing the candidate pool from being diluted by degen-                  in memory during the distillation phase. The optimization
erate traces (e.g., excessively short sequences, uninformative              objective is formulated as:                           
content, or malformed XML tags) and directly improving the                               max Eξ∼πθ Rexec (ξ) + λRmem (ξ) .
                                                                                           θ
robustness of the final aggregated prediction.                              Mathematically, Rmem reshapes the policy’s energy landscape
     b) Theoretical Formulation: We formulate the Text-to-                  by concentrating probability mass on the verified prototypes
SQL generation process as a Goal-Augmented Partially Ob-                    in Tmem , thereby constraining the vast search space Tvalid .
servable Markov Decision Process (POMDP), defined by                        This significantly reduces policy variance (Var(πmem ) ≪
the tuple M = (S, A, P, G, R, O). The components of this                    Var(πsparse )), causing sampled candidates to cluster into fewer
process are defined as follows:                                             execution groups and ensuring robust consensus for majority
voting. Notably, we assume that the reasoning patterns distilled
from our selected teacher models are already high-quality;
therefore, Rmem is designed to encourage the SLM to stay
close to these verified prototypes rather than exploring entirely
new reasoning patterns.
     c) Memory construction and management: We define
a persistent reasoning memory M implemented as a vector
database using ChromaDB [78], supporting efficient embed-
ding retrieval and incremental updates of reasoning traces.
Each memory entry stores a reasoning embedding, its associ-         Fig. 4. The flow of memory reward computation and management. During
ated metadata (sample ID, reasoning embedding, and database         rollout, the reasoning text is embedded and compared with the centroid of top-
ID), and is managed by three operators INIT, RETRIEVE, and          k similar reasoning retrieved from different databases. The memory manager
                                                                    executes three key functions—INIT, RETRIEVE, and INSERT—to maintain
INSERT, as illustrated in Fig. 4.                                   a diverse set of verified reasoning traces for GRPO optimization.
   • INIT: Memory Initialization. The memory M is initial-          ory M clean and diverse. The system only stores reasoning
     ized with high-quality reasoning traces from the teacher       traces that are both correct in execution and sufficiently dif-
     model DeepSeek-R1, which often produces diverse rea-           ferent from what already exists in memory. If a new reasoning
     soning styles for distillation in §IV-A. We first filter       is too similar to previous ones, it is skipped. This mechanism
     samples whose generated SQLs execute correctly, then           helps M grow into a well-balanced repository that contains
     extract their reasoning content from the <think> blocks.       only effective and varied reasoning paths, guiding the model
     Each reasoning trace is embedded into a shared semantic        toward better generalization.
     space using Qwen3-Embedding-0.6B [79], and stored in                 d) Reward formulation: Let ψ(·) be the fixed encoder for
     ChromaDB with its metadata. This initialization builds a       embedding reasoning paths. Given a question/sample q (with
     foundational pool of verified reasoning paths.                 associated database db(q)) and the reasoning trace t generated
   • RETRIEVE: Cross-Database Semantic Retrieval. Dur-              by the SLM, we retrieve the top-k verified reasoning paths
     ing training, for a given reasoning trace t from database d,   from other databases
     the RETRIEVE operator searches for top-k semantically                     R(t; q) = { ri | db_id(ri ) ̸= db(q) }ki=1 ,
     similar traces {ri }ki=1 from other databases (db id ̸= d).    and compute their embeddings E = {ψ(ri )}ki=1 . We then form
     By calculating the reward based on the centroid of these       the centroid embedding
     k embeddings, the system forces the model to align                                                  k
     with the average structural pattern rather than overfit-                                        1X
                                                                                          c(t; q) =        ψ(ri ),
     ting to specific schema tokens. Furthermore, this design                                        k i=1
     does not encourage generic hallucinations, because if the      and normalize the vectors â = ψ(t)/∥ψ(t)∥2 and ĉ =
     model generates hallucinated schema elements from other        c(t; q)/∥c(t; q)∥2.
     databases, this easily leads to a SQL syntax error on the                       0,
                                                                                                   if the output format is invalid;
     current database, triggering a zero execution reward and       Rmem (t | q) = cos(â, ĉ), if the SQL executes incorrectly;
     penalizing the deviation.                                                       
                                                                                       1,           if the SQL executes correctly.
                                                                                     
   • INSERT: Incremental Memory Update. When a
                                                                    This formulation treats the reward as the direct cosine similar-
     reasoning-SQL pair executes successfully, its reasoning
                                                                    ity between the current reasoning and the centroid of retrieved
     trace is embedded and conditionally inserted into M
                                                                    successful traces, providing a dense, interpretable signal of
     using INSERT. Before insertion, the system applies a
                                                                    reasoning alignment. When execution succeeds, the reward
     quality gate to filter degenerate traces based on three
                                                                    saturates at 1.0 and the reasoning trace is stored in the memory
     metrics derived from the trace text: (1) Length Heuristics
                                                                    bank M via the INSERT operator. This design preserves
     reject traces that are too short (< 30 tokens) or too long
                                                                    stable gradients, avoids redundant scaling, and ensures that
     (> 2000 tokens); (2) Informativeness ensures schema
                                                                    even partially correct reasoning receives proportional credit.
     grounding by requiring a schema density (calculated as
                                                                          e) Example: Schema (simplified): Employee(EmpID,
     the ratio of schema column mentions to total tokens)
                                                                    Name, DeptID, Salary), Department(DeptID, DeptName).
     ≥ 0.05 with at least 2 distinct column mentions; and (3)
                                                                    Question: “List employees who earn more than the average
     Lexical Diversity prevents repetitive loops by requiring
                                                                    salary of their own department.”
     that at least 60% of consecutive word pairs are unique.
     Valid traces then undergo similarity deduplication: the         <think>
     system skips addition if the cosine similarity with the top-    1) Compute the average salary per department.
                                                                     2) Compare each employee’s salary with the department average.
     1 existing entry is ≥ 0.9, thereby avoiding redundancy          3) Return those exceeding it.
     and encouraging exploration of new reasoning paths.             </think>
                                                                     SQL: (execution fails)
     Over time, M evolves dynamically, continually enriched
     by successful reasoning produced by the student model.           Even though the SQL fails, the reasoning follows a coherent
   These operators work together to keep the reasoning mem-         logical pattern—group, aggregate, align, and compare—that
aligns with verified traces retrieved from other databases (e.g.,                               TABLE I
comparing students above class average or products above             A LL DEFINED ATOMIC OPERATIONS ; EACH REPRESENTS A MEANINGFUL
                                                                               SQL CONSTRUCT FOR STRUCTURAL COMPARISON .
category mean). The high semantic similarity produces a
                                                                       Atomic op                        Meaning / Example
strong memory reward, guiding the model to refine rather than          FROM / JOIN
discard this reasoning path.                                           FROM(tbl [AS a])
                                                                       JOIN(tbl [AS a], type)
                                                                                                        Base relation; FROM(cust AS T1)
                                                                                                        Join relation; JOIN(orders, INNER)
   In contrast, when the model produces invalid reasoning              ON EQ(a.col,b.col)               Equality key; ON EQ(T2.id,T1.id)
                                                                       ON PRED(op,lhs,rhs)              Non-equi join; ON PRED(>,T2.qty,VALUE(0))
patterns, various failure cases can occur, such as empty rea-          SELECT projections
                                                                       SELECT COL(a.col)                Column; SELECT COL(name)
soning traces, hallucinated answers instead of SQL queries,            SELECT AGG(agg,a.col)            Aggregation; SELECT AGG(SUM,total)
or the generation of XLM/HTML tags without meaningful                  SELECT EXPR(expr)                Scalar expr; SELECT EXPR(LOWER(name))
                                                                       DISTINCT                         Distinct projection
information. These reasoning traces are semantically distant           WHERE / HAVING
                                                                       WHERE PRED(op,lhs,rhs)           Predicate; WHERE PRED(=,ct,VALUE(‘AU’))
from the reasoning patterns stored in memory, leading to very          HAVING PRED(op,lhs,rhs)          Post-group filter
                                                                       Literals / Group / Order / Limit
low similarity scores and thus minimal memory rewards. Such            VALUE(v)                         Literal; VALUE(DATE ‘2024-01-01’)
penalties discourage unstructured or hallucinated reasoning            GROUP BY(a.col)
                                                                       ORDER BY(expr,dir)
                                                                                                        Group key; GROUP BY(name)
                                                                                                        Ordering; ORDER BY(rev,DESC)
behaviors and steer the model back toward compositional,               LIMIT(n)                         Row cap; LIMIT(50)
                                                                       Set ops / CTEs
SQL-oriented reasoning that can yield executable queries.              UNION / INTERSECT / EXCEPT Set operation
                                                                       WITH CTE(name)                   Declare CTE; WITH CTE(top cust)
      f) Efficiency and stability: The memory module is de-            Nested subqueries
signed for efficiency and scalability. Each reasoning trace is         ENTER SUBQUERY(role)             Enter subquery;
                                                                                                        ENTER SUBQUERY(WHERE SCALAR)
embedded once and indexed in a vector database, enabling               EXIT SUBQUERY                    Exit subquery scope
                                                                       SUBQ LAST                        Refer to last subquery;
sub-millisecond approximate nearest-neighbor retrieval even at                                          WHERE PRED(=,x,SUBQ LAST)
                                                                       Window / Alias
large scale [78], [80]. The vector database not only accelerates       WINDOW(part,order,frame)         Window spec
retrieval but also ensures consistent and reliable access to           SELECT WIN(func,args)            Windowed select
                                                                       ALIAS(kind,from,to)              Rename; ALIAS(COLUMN,SUM(total),rev)
reasoning traces during training. Since the reward depends
only on embedding similarity rather than SQL execution, it          formatting. This abstraction yields comparable atomic repre-
incurs negligible overhead and can be computed in parallel          sentations for syntactically different but equivalent SQLs; for
with rollouts. This lightweight mechanism provides dense,           deeply nested subqueries, operations are flattened into a single
cost-effective feedback that stabilizes GRPO optimization and       list to ensure efficient and consistent comparison.
improves reasoning transfer across databases.                       Reward computation. Given a predicted SQL s generated
D. Atomic Reward: Operation-Level Structural Feedback               from a rollout, we parse it into a set of atomic operations A(s)
                                                                    using our Atomic Decomposition module (see the left part of
   Execution-based rewards assess only final correctness and
                                                                    Fig. 5). Each atomic unit captures one structural action such
fail to capture structural progress for partially correct or non-
                                                                    as SELECT_COL, FROM, or WHERE_PRED, enabling direct
executable SQL. To address this, we introduce the Atomic
                                                                    comparison between queries at the operation level.
Reward, which decomposes each SQL query into atomic oper-
                                                                       For each reference SQL gi in the ground-truth SQLs set
ations (e.g., selections, joins, predicates) and measures overlap
                                                                    {g1 , . . . , gN ′ } (see the reference SQL enrichment process
with the reference SQL at this level, providing continuous,
                                                                    below), we compute a Jaccard similarity between their atomic-
interpretable feedback that reflects compositional reasoning.
                                                                    operation sets: 
Motivation. A Text-to-SQL model may generate SQLs that
are semantically close to the ground truth—using correct                                  |A(s) ∩ A(gi )| , if |A(s) ∪ A(g )| > 0,
                                                                                                                           i
                                                                        J(s, gi ) =         |A(s) ∪ A(gi )|
tables, joins, or filters—but differ in specific clauses. For
                                                                                           0,                otherwise.
                                                                                         
instance, replacing AVG(Salary) with COUNT(*) or omit-
ting a GROUP BY clause. While token-based or n-gram simi-           This metric captures the proportion of shared operations (e.g.,
larity metrics can capture surface-level overlap, they remain       same SELECT_COL(name), WHERE_PRED(=,...)), nor-
sensitive to textual styling and fail to reflect true struc-        malized by the total number of distinct operations across both
tural alignment between SQL components. Execution-based             queries. As illustrated in the Atomic Operations Comparison
rewards likewise overlook these fine-grained distinctions. By       part of Fig. 5, each operation in the predicted SQL is aligned
analyzing SQLs through atomic operations, our comparison            with its counterpart in the reference SQLs, where bold ele-
becomes invariant to formatting and reordering, interpretable       ments denote overlapping atomic operations that contribute to
in terms of compositional structure, and capable of assigning       the overall Jaccard score.
partial credit to logically aligned fragments—encouraging the          To prevent the atomic score from saturating near 1 for high
model to gradually assemble full correctness.                       but imperfect overlaps, we apply a monotone shaping function:
Atomic decomposition. Each SQL query s is parsed into               ϕ(x) = λ x + (1 − λ) β xγ , with λ=0.05, β=0.79, γ=0.20.
atomic operations following Table I by constructing an ab-          This compresses the top end of the scale (e.g., ϕ(0.95)<0.95),
stract syntax tree (AST) and extracting clause-level primitives.    so “almost-right” structures receive slightly less credit than
Each AST node represents a distinct SQL construct (e.g.,            totally matches. The goal is to avoid over-rewarding queries
projections, predicates, aggregations, joins), enabling seman-      that are structurally very similar yet not fully correct, while
tically meaningful operations independent of token order or         still providing smooth credit for partial matches. A fully
                                                                                  are unlikely to appear unless the training instance itself is
                                                                                  mislabeled, because the distilled model is trained with the
                                                                                  same prompts to reproduce the gold SQL and thus tends to
                                                                                  generate queries that remain structurally close to the ground
                                                                                  truth rather than collapsing to vacuous predicates. Empirically,
                                                                                  the risk of reinforcing spurious structures is minimal: on the
                                                                                  BIRD training set, 670/9,428 samples (7.1%) produce empty
                                                                                  gold results, yet the execution-verified candidates we retain
                                                                                  still exhibit high structural overlap with the corresponding
                                                                                  gold SQL. Additionally, in a manual audit of 100 additional
                                                                                  non-empty cases, we did not observe hack-like patterns; the
Fig. 5.      Atomic Reward computation pipeline. The predicted SQL is             main discrepancy was SELECT versus SELECT DISTINCT,
compared against a set of reference SQLs that represent equivalent but            which is consistent with known labeling noise in NL2SQL
stylistically different realizations of the same intent. Each comparison yields   training data [81]. Finally, since the atomic reward is computed
a Jaccard similarity across atomic operations, and the final reward is the
maximum among these scores.                                                       as the maximum similarity over the reference pool (which
correct SQL will still be reward 2.0 by the execution reward.                     always includes the gold SQL), enrichment primarily reduces
   We first compute the maximum Jaccard similarity over all                       false mismatches due to syntactic variations without encour-
reference SQLs:                                                                   aging semantically incorrect SQL.
                Jmax (s) = max′ J(s, gi ),                                                        V. E MPIRICAL E VALUATION
                                    i∈[1,N ]
and then apply the shaping function to normalize the reward:                        In this section, we conduct experiments with the aim of
                   Ratomic (s) = ϕ(Jmax (s)).                                     answering the following research questions:
This formulation enhances robustness to structural variations                     (RQ1) Does FINER-SQL improve execution accuracy of
by selecting the most compatible reference query among all                            small language models over existing baselines? (§V-B)
semantically equivalent candidates. As a result, the reward                       (RQ2) How efficient is FINER-SQL in memory usage and
remains stable even when the predicted SQL differs in syntax,                         inference time compared with existing methods? (§V-C)
such as through alias renaming, operator choice, or subquery                      (RQ3) How sensitive is model performance to hyperparame-
restructuring, yet conveys the same semantics.                                        ters such as temperature and candidate number? (§V-D)
Reference SQL enrichment. To increase the diversity and                           (RQ4) How does reinforcement learning with dense rewards
coverage of structurally correct SQL references, we enrich                            improve SQL accuracy over training steps? (§V-E)
the ground-truth set using our largest distilled model (3B) in                    (RQ5) How do different reward components (atomic, mem-
§IV-A. For each training question, we sample N =30 candidate                          ory) contribute to the overall model performance? (§V-F)
SQLs from the distilled model with temperature T =1.0, using                      (RQ6) How well does FINER-SQL handle SQL queries of
the exact same prompt format as in its SFT stage. This                                varying complexity levels? (§V-G)
is important: since the distilled model has been explicitly                       (RQ7) How does the reasoning evolve after reinforcement
trained to reproduce the correct SQL for these prompts, its                           learning training? (§V-H)
generations are strongly anchored to the gold logical structure
and typically remain highly similar to the ground-truth query.                    A. Experimental Setup
The observed diversity when decoding multiple candidates                          Database. We rely on two popular Text-to-SQL benchmarks:
at T =1.0 mainly stems from the distillation setup itself:                        Spider [7] and BIRD [8], [82]–[84]. Spider is a popular bench-
during distillation, a single prompt is paired with multiple                      mark for NL2SQL translation, consisting of 200 databases
teacher-produced completions (i.e., different reasoning traces                    with multiple tables that cover 138 diverse domains. Spider
and SQL) coming from diverse teachers. As a result, sampling                      contains 7000 samples in a training set, a development set
N =30 completions naturally yields multiple stylistic variants                    with 1024 samples, and a test set. BIRD contains 95 databases,
in the thinking–SQL output (e.g., aliasing, join ordering, or                     cumulatively accounting for 33.4GB across 37 professional
equivalent predicate phrasing) while preserving the underlying                    domains. BIRD contains 9428 samples in training set, a de-
semantics required to answer the question. We then execute                        velopment set with 1534 samples and a hidden test set. BIRD
each candidate on the corresponding database and retain only                      is more challenging, with each of BIRD’s databases containing
those whose denotation matches the gold query, adding them                        around 549K rows on average, compared to Spider’s limited
to the reference pool {g1 , . . . , gN ′ } together with the original             capacity of just 2k rows. Also, BIRD offers evidence for a
gold SQL.                                                                         specific sample to facilitate the generation of the right SQL
   A potential concern is spurious correctness under empty                        query.
execution result: if the gold SQL yields an empty result set,                     Evaluation Metrics. We evaluate model performance using
a degenerate “hack” query such as WHERE 1=0 could also                            Execution Accuracy (EX) and Pass@K [85]–[87]. EX mea-
return the same empty output and might be mistakenly added                        sures whether the predicted SQL produces the same execution
to the reference pool. In our setting, however, such hacks                        result as the ground truth, serving as the primary indicator of
correctness. Pass@K captures the likelihood that at least one                                  TABLE II
of the top-K generated SQL candidates executes correctly,          C OMPARISON OF T EXT- TO -SQL METHODS ON BIRD AND S PIDER D EV.
                                                                      Methods                          BIRD Dev EX%     Spider Dev EX%
which is particularly important for selection-based Text-to-                               Proprietary Models (> 70B)
SQL systems (e.g. CHASE-SQL [11], Reasoning-SQL [76]),                DIN-SQL + GPT-4                  50.72            82.8
                                                                      DAIL-SQL + GPT-4                 54.76            83.1
as a correct query among top-K candidates can potentially be          MAC-SQL + GPT-4                  59.59            86.8
identified by an effective selection or ranking algorithm.            SuperSQL + GPT-4                 58.50            87.0
                                                                      MCS-SQL + GPT-4                  63.36            86.8
Baselines. We compare FINER-SQL against a wide range                  CHESS + GPT-4                    65.00            –
of Text-to-SQL systems, including closed-source API-based             CHASE-SQL + Gemini 1.5           73.01            –
                                                                                      Open-source Models (> 5B parameters)
methods and open-source fine-tuned models. Although recent            SFT Llama2-7B                    45.37            77.8
approaches such as OmniSQL [88] and Arctic-Text-to-SQL-               SFT Llama2-13B                   53.91            81.6
                                                                      CodeS-7B                         57.17            85.4
R1 [31] leverage large-scale synthetic corpora (e.g., SynSQL-         CodeS-15B                        58.47            84.9
2.5M [88], Gretel-Synth [89]), these introduce new schemas            CHESS (open-source, 33B+70B)     59.86            –
                                                                      Alpha-SQL 7B                     66.80            84.0
and question formulations that differ substantially from Spider       Alpha-SQL 14B                    68.70            87.0
and BIRD. To ensure fair, controlled comparisons that isolate         Alpha-SQL 32B                    69.70            –
                                                                      ExCoT 70B                        68.51            –
training algorithms rather than data volume, we evaluate only         Reasoning-SQL 7B                 64.01            78.7
methods trained on Spider and BIRD databases.                         Reasoning-SQL 14B                65.31            81.4
                                                                      SQL-R1 7B                        63.10            84.5
   Closed-source API-based Methods. DIN-SQL [90] decom-               SQL-R1 14B                       67.10            86.7
poses complex questions into schema linking, query clas-                              Open-source Models (≤ 5B parameters)
                                                                      Fine-tuned T5-3B + PICARD        23.34            79.3
sification, and self-correction before SQL synthesis. DAIL-           CodeS-1B                         50.46            77.9
SQL [91] combines prompt engineering with lightweight fine-           CodeS-3B                         55.02            83.4
                                                                      Reasoning-SQL 3B                 58.67            –
tuning, selecting demonstrations by question-query similar-           SQL-R1 3B                        54.6             78.1
ity. MAC-SQL [92] adopts a multi-agent framework where                FINER-SQL 0.5B (Ours)            50.85            70.2
                                                                      FINER-SQL 1.5B (Ours)            63.17            80.0
Decomposer, Selector, and Refiner iteratively improve SQL             FINER-SQL 3B (Ours)              67.73            85.0
generation. SuperSQL [66] performs automated architecture                                      TABLE III
search across schema linking, prompting, and post-processing         I NFERENCE EFFICIENCY AND DEPLOYMENT COST COMPARISON OF
with execution-based revision. MCS-SQL [93] uses multiple                        T EXT- TO -SQL MODELS ON BIRD D EV.
                                                                                                                Min. VRAM   Compute Setup
prompt templates and a multiple-choice selector to improve            Model                Latency(s)   DType      (GB)     (GPU Memory)
validity, while CHESS [10] and CHASE-SQL [11] employ                                      Closed-Source API-Based Methods
                                                                      DIN-SQL + GPT-4         24.09        –         –      OpenAI-based
modular, multi-path reasoning pipelines with large models to          MAC-SQL + GPT-4         24.64        –         –      OpenAI-based
                                                                      CHESS(IR,SS,CG)        118.61        –         –      OpenAI-based
refine SQL candidates.                                                CHESS(IR,CG,U T )      156.50        –         –      OpenAI-based
   Open-source Fine-tuning Methods. T5-3B + PICARD [48]                                    Open-Source Fine-Tuned Models
                                                                      Alpha-SQL 7B          1650.00      bf16      ∼22      2×46 GB L40S
enforces syntactic validity via constrained decoding. CodeS [9]       Alpha-SQL 14B         1802.00      bf16      ∼38      2×46 GB L40S
                                                                      Alpha-SQL 32B         2512.00      bf16      ∼80      4×46 GB L40S
incrementally pretrains open-source models (1B–15B) on cu-            CodeS-1B                0.69       fp32       ∼3      1×24 GB A5000
                                                                      CodeS-3B                1.06       fp32       ∼8      1×24 GB A5000
rated NL2SQL data to improve structural robustness. SFT               CodeS-7B                1.87       fp32      ∼17      1×24 GB A5000
Llama2 [8] provides a supervised fine-tuning baseline without         CodeS-15B               3.52       fp32      ∼27      1×48 GB A6000
                                                                                                  Ours: FINER-SQL
reinforcement signals. Alpha-SQL [75] combines MCTS with              FINER-SQL 0.5B          2.60       bf16       ∼3      1×24 GB A5000
                                                                      FINER-SQL 1.5B          3.25       bf16       ∼6      1×24 GB A5000
LLM reasoning for zero-shot SQL generation. CHESS (open-              FINER-SQL 3B            5.57       bf16      ∼10      1×24 GB A5000
source) [10] adapts its modular framework to open-source
LLMs, while Reasoning-SQL [76] introduces SQL-specific            stage pipeline comprising schema filtering → SQL candidate
partial rewards for RL. SQL-R1 [94] uses coarse reward sig-       generation → majority voting. This setup is also adopted in
nals without fine-grained structural feedback, and ExCoT [32]     many recent systems such as CHESS, CHASE-SQL, and SQL-
applies iterative preference optimization guided by execution.    R1. For schema filtering, we employ our prior work GRAST-
Setup. We train three policy models—Qwen2.5-Coder-0.5B,           SQL 0.6B 1 , a schema ranking model that retrieves the top-
1.5B, and 3B—using GRPO on two NVIDIA A6000 GPUs                  30 most relevant columns for each query. Unless otherwise
(48 GB each). All models are trained in bfloat16 precision        specified, all main experiments for accuracy and performance
with Flash Attention [95] for efficiency. For supervised fine-    comparison generate 30 SQL candidates per question.
tuning, the model is trained for two epochs on the reasoning
bank in §IV-A, with a learning rate of 2 × 10−5 . For GRPO        B. End-to-end Comparison
training, the number of rollouts per sample is 32, the learning      Table II presents the execution accuracy (EX%) of
rate is 8 × 10−6 , and the global batch size is 32. For the       FINER-SQL compared with recent Text-to-SQL systems on
memory reward, we set the number of retrieved reasoning           the BIRD and Spider development sets. Despite its small
traces 20. With this configuration, the total training time       parameter scale, FINER-SQL consistently achieves accu-
including supervised finetuning and reinforcement learning        racy competitive with or superior to much larger mod-
takes less than 2 days for a 3B model and much faster for         els across both benchmarks. On the BIRD benchmark,
1.5B and 0.5B.
   During inference, FINER-SQL follows a lightweight three-        1 https://huggingface.co/griffith-bigdata/GRAST-SQL-0.6B-BIRD-Reranker
FINER-SQL 3B reaches 67.73% EX, surpassing CodeS-
15B (58.47%), CHESS (33B+70B, 59.86%), and Reasoning-
SQL 14B (65.31%), while remaining comparable to Alpha-
SQL 14B (68.70%) and SQL-R1 14B (67.10%), both of which
are over four times larger. The 1.5B variant of FINER-SQL
achieves 63.17% EX, outperforming CodeS-7B (57.17%) and
MAC-SQL (59.59%) even though these use larger or propri-         Fig. 6. FINER-SQL Pass@K and EX% on BIRD Dev under different
etary backbones. On the Spider benchmark, FINER-SQL 3B           numbers of candidates (left) and sampling temperatures (right).
attains 85.0% EX, comparable to CodeS-15B (84.9%), SQL-
R1 7B (84.5%), and Alpha-SQL 7B (84.0%), and approaching
the best-performing 14B-32B models (86–87%). These results
demonstrate that our fine-grained execution feedback and
dense reward optimization effectively enable small models
to close the gap with large-scale systems in both reasoning              (a) 0.5B                 (b) 1.5B                  (c) 3B
accuracy and generalization.                                     Fig. 7. Accuracy–latency trade-off of candidate selection for FINER-SQL
   Overall, FINER-SQL substantially reduces the dependency       (left-to-right: 0.5B, 1.5B, 3B). The blue curve denotes EX%, the red curve
on massive model sizes or proprietary APIs. With maximum         denotes end-to-end average latency per query, and the yellow curve denotes
                                                                 execution-only latency.
at 3B parameters, it achieves performance on par with or
beyond many 14B-70B open-source models, confirming that          Note that this analysis includes only models with public im-
fine-grained execution and structural feedback provide a cost-   plementations; methods such as CHASE-SQL [11] and SQL-
efficient path to high Text-to-SQL accuracy.                     R1 [94] lack open-source code, preventing fair measurement
                                                                 of inference time under comparable settings.
C. Performance Evaluation                                        D. Hyperparameter Sensitivity
   Table III presents the inference latency and deployment       Number of candidates. We analyze the impact of the number
cost of Text-to-SQL models evaluated on the BIRD Dev.            of sampled SQL candidates n on inference performance, as
We compare three system categories: closed-source API-based      shown in Fig. 6 (left). Increasing n from 1 to 50 consistently
methods, (ii) open-source fine-tuned models, and (iii) our       improves both Pass@K and EX% across all FINER models,
proposed FINER-SQL family. All open-source systems are           but the gain saturates beyond 30 candidates. The smallest
deployed using vLLM [96], where the minimum VRAM                 model (0.5B) benefits the most, rising from 35% to nearly 49%
required for serving LLMs can be estimated as the sum of         EX, indicating that stochastic sampling and majority voting
model parameters, KV cache, and minor ephemeral memory:          effectively compensate for limited capacity. Larger models
VRAMserve ≈ VRAMmodel + VRAMKV-cache + VRAMothers .              (1.5B and 3B) exhibit higher initial accuracy and more stable
with KV-cache scaling linearly with context length (e.g., 40K    convergence, reaching around 82% Pass@K and 68% EX at
tokens in Alpha-SQL greatly increase memory use).                n=50. These findings demonstrate that moderate candidate
   While large models such as Alpha-SQL 14B and Alpha-           sampling provides an efficient trade-off between performance
SQL 32B achieve slightly higher execution accuracy (Table II),   gains and computational cost during inference.
they incur prohibitive inference latency (1800-2500s/sample)        We show the accuracy versus latency trade-off in Fig. 7.
and memory costs (up to ∼80GB VRAM). In contrast,                As the number of candidates increases, EX% (blue) improves
FINER-SQL 3B attains comparable accuracy with much               steadily, but it comes with the increasing in end-to-end latency
lower overhead (5.57s/sample, ∼10GB VRAM). Proprietary           (red) and SQL execution latency. Across model scales, n in
pipelines such as CHESS remain competitive in accuracy but       the range of 20–30 provides the best operating point, balance
suffer from multi-stage inference latency exceeding 100s/sam-    between accuracy and latency. This analysis guides the choice
ple due to sequential API calls [10], [20], making them          of n in interactive settings, noting that absolute execution time
unsuitable for latency-sensitive or on-premise settings.         depends on database and SQL complexity.
   Importantly, the compact memory footprint of FINER-SQL        Temperature for candidate generation. We further analyze
enables deployment on cost-effective GPUs. The 3B-parameter      the impact of sampling temperature on SQL diversity and
variant can operate comfortably on widely available and af-      execution accuracy. As illustrated in Fig. 6 (right), raising the
fordable consumer GPUs, such as the NVIDIA RTX 5070              temperature from 0 to 1.0 consistently enhances both Pass@K
(12 GB), RTX 4090 or A5000 (24 GB), without requiring            and EX% across all model sizes. Higher temperatures en-
specialized server-grade hardware. This substantially lowers     courage exploration of diverse reasoning and SQL structures,
the barrier to real-world adoption compared to large-scale       which leads to more correct candidates under majority voting.
models requiring multi-GPU racks or proprietary API.             The smallest model (0.5B) shows the strongest improvement,
   Overall, these results show that FINER-SQL achieves a         with EX increasing from 35% at greedy decoding to nearly
strong balance between accuracy, latency, and cost, enabling     49% at temperature 1.0. Larger models (1.5B and 3B) also
practical Text-to-SQL deployment on commodity hardware.          benefit moderately, stabilizing around 60-68% EX. Overall,
                                                                                Fig. 10. Performance improvement of Pass@K and EX on BIRD Dev across
Fig. 8. Sensitivity of memory retrieval top-k on BIRD Dev EX% with three        GRPO training steps. Step 0 represents the supervised fine-tuning baseline.
retrieval scopes: Cross-DB (retrieving only from other databases), Same-only
(retrieval only from current database), and Mixed (query from all databases).
the best configuration is achieved at temperature 1.0 with 50
sampled candidates, showing that moderate stochastic sam-
pling effectively balances exploration and accuracy.
Memory configuration. Fig. 8 analyzes the effect of memory
configuration by varying #retrieved reasoning traces (k) and
the retrieval scope. Across all model sizes, increasing k yields                Fig. 11. Ablation of reward components. Left: ∆EX% when removing each
modest gains that saturate around k ∈ {10, 20}, while Cross-                    reward. Right: syntax error rate when removing reward components.
DB retrieval consistently achieves the highest EX% in the                       E. Performance Gains through GRPO Training Steps
high-k regime. By excluding the querying database, Cross-
DB retrieval enables access to more diverse reasoning traces                       We analyze the impact of GRPO optimization over succes-
from different databases. In contrast, in the Mixed setting,                    sive training steps, as illustrated in Fig. 10. The curves report
retrieval is often dominated by traces from the same database                   Pass@K and EX% on BIRD Dev, where step 0 corresponds
due to strong surface-level entity overlap, causing behavior                    to the supervised fine-tuned baseline and subsequent points
and performance close to the Same-only setting. These results                   reflect progressive policy updates guided by dense execution
indicate that cross-database diversity is crucial for effective                 feedback. All models exhibit consistent improvement, con-
memory-based supervision, taking its centroid embedding al-                     firming that GRPO effectively refines reasoning and SQL
lows transfer the reasoning patterns to SLMs.                                   generation through iterative interaction with the environment.
                                                                                The 0.5B model gains the most, improving from 55.9% to
                                                                                66.3% Pass@K and from 42.9% to 49.3% EX after 2000
                                                                                steps. Larger models (1.5B and 3B) also show steady im-
                                                                                provements, with the 1.5B model rising from 75.3%/59.4%
                                                                                to 80.1%/63.1% and the 3B model from 78.3%/63.4% to
                                                                                81.6%/67.7% (Pass@K/EX). These results highlight that
Fig. 9. Sensitivity of the shaping function in Atomic Reward under four         GRPO enables stable and monotonic performance gains across
settings. The legend reports EX on BIRD Dev for 0.5B/3B as EX0.5B /EX3B .
                                                                                different model scales, with smaller models benefiting the most
Atomic Shaping Function Sensitivity. We analyze the sen-                        from fine-grained execution feedback.
sitivity of the atomic-op shaping function φ(x) = λ x +
(1 − λ)βxγ as introduced in §IV-D. Our design objective                         F. Ablation Study
is to allocate relatively higher reward to low-overlap can-                           a) Impact of Reward Components: We evaluate the con-
didates (larger φ(x) when x ≈ 0) while preventing re-                           tribution of the memory and atomic rewards by removing them
ward saturation for near-perfect matches by controlling the                     individually or jointly during GRPO training. As shown in
endpoint φ(1) (smaller φ(x) when x ≈ 1). To keep the                            Fig. 11, excluding either reward leads to a clear drop in EX%
sweep compact, we select four representative settings by                        and a rise in syntax error rates across all model sizes. For the
inspecting the geometry of φ(x) and covering both end-                          0.5B model, removing the memory reward decreases EX by
point caps and concavity: S1 (λ=0.15, β=1.0, γ=0.35), S2                        1.79% and raises syntax errors from 19.6% to 31.5%, while
(λ=0.30, β=0.85, γ=0.55), S3 (λ=0.05, β=0.79, γ=0.20),                          removing the atomic reward causes a similar 1.92% EX drop.
and S4 (λ=0.60, β=0.50, γ=0.98) which is near linear. Fig. 9                    For the 3B model, removing the memory or atomic reward
visualizes the resulting shaping curves, and the legend reports                 reduces EX by 2.22% and 3.26%, respectively, with syntax
the corresponding execution accuracy on BIRD Dev for 0.5B                       errors increasing from 6.0% to about 10%. When both rewards
and 3B (EX0.5B /EX3B ). S3 and S4 achieve the best EX                           are removed, degradation becomes most severe (-2.97%, -
across both 0.5B and 3B models, and both share a capped                         2.16%, and -4.44% EX for 0.5B, 1.5B, and 3B), confirming
endpoint φ(1) ≈ 0.8, which suppresses the reward for near-                      their complementary effects.
perfect atomic overlap when execution is not fully correct.                        Removing the memory reward causes higher syntax error
Notably, S3 assigns much higher reward near Jaccard score                       rates, as the model explores unstable reasoning paths that lead
near 0 and yields the strongest gains on the 0.5B model,                        to invalid or unexecutable SQLs. Eliminating both rewards
reinforcing our design choice to boost low-overlap candidates                   further lowers EX due to the sparse reward problem—when
while suppressing Jaccard score near 1.                                         failures yield zero feedback, the model stops improving over
                            TABLE IV
 R EASONING S TABILITY A NALYSIS : N O M EMORY VS . W ITH M EMORY.
                      FINER-SQL 0.5B    FINER-SQL 1.5B     FINER-SQL 3B
 Metrics
                     w/o Mem  w/ Mem   w/o Mem w/ Mem    w/o Mem w/ Mem
 EX (%)                46.28   50.85     61.21   63.17     65.38    67.73
 Self-BLEU             0.674   0.724     0.607   0.631     0.584    0.615
 Mean Exec. Groups     8.07     5.59      7.16    6.25     6.21     5.27




                                                                            Fig. 13. The reasoning-length distributions before and after RL across query
                                                                            difficulties. Our RL framework leads to more concise reasoning traces.

                                                                            positional SQL generation effectively, and can rival or exceed
                                                                            much larger or GPT-4-assisted baselines.
Fig. 12. EX% by SQL complexity on BIRD Dev, showing FINER-SQL                Example of reasoning before RL: 7.8K characters & incorrect
(1.5B-3B) stay competitive on challenging queries.                           First, the user wants: ”list the lowest three eligible free rates for students aged 5-17 in continuation schools.”
                                                                             From the schema, the eligible free rate is in frpm.‘Percent (%) Eligible Free (Ages 5-17)‘. The condition ”continuation
                                                                             schools” refers to School Type = ’Continuation High Schools’. External knowledge says: eligible free rate = Free
time. Overall, the memory reward stabilizes reasoning and                    Meal Count (Ages 5-17) / Enrollment (Ages 5-17). I should check which column represents that ratio... it may already
                                                                             exist as a computed field.
reduces invalid SQLs, while the atomic reward enforces                       ...
                                                                             Maybe I need to join with schools to confirm the school type or use frpm.School Type.
operation-level structural correctness. Together, they provide               To be accurate, I should select from frpm where School Type = ’Continuation High Schools’, order by the eligible
                                                                             free rate ascending, and limit to 3 results.
fine-grained signals that guide learning and enable the model
to improve even when the generated SQL is incorrect.
                                                                             Example of reasoning after RL: concise & correct SQL
      b) Analysis of Reasoning Stability: Given each prompt,                 We need the three lowest eligible free rates for students under 18, defined by frpm.‘Free Meal Count (Ages 5-17)‘ /
                                                                             frpm.‘Enrollment (Ages 5-17)‘ for schools where frpm.‘School Type‘ is ”Continuation High Schools”. Return rates.
we sample K=30 candidate reasoning traces and their cor-                     Note we must compute the rate even if there are nulls: SQL will ignore them. Order by rate ascending, limit 3. Use
                                                                             explicit CTE or subquery for clarity. Return only the rate.
responding SQL queries. We quantify the diversity of the
reasoning texts using Self-BLEU [97], where each trace is
treated as the hypothesis and the remaining K−1 traces                      H. Reasoning Evolves under RL
serve as references; thus, a higher Self-BLEU indicates lower
diversity. Table IV shows that enabling memory consistently                    To assess how FINER-SQL shapes reasoning behavior, we
increases Self-BLEU, meaning the model produces less di-                    compare the 3B model before and after RL training. Fig. 13
verse reasoning across candidates. This reduced reasoning                   shows reasoning-length distributions across query difficulties.
variance propagates to the generated SQL, yielding fewer dis-               Before RL, the model produces long, inconsistent chains
tinct execution results (lower mean execution groups), which                (Simple: 2.38K, Moderate: 2.93K, Challenging: 3.49K on
is beneficial for majority voting: when candidates concentrate              average, many exceeding 8K), reflecting redundant exploration
into fewer execution clusters, votes are less fragmented and                and schema confusion that often fails to converge. After RL,
the correct execution is more likely to win. For instance, at               reasoning is substantially shorter and more stable (Simple:
0.5B, memory raises Self-BLEU from 0.674 to 0.724 while                     0.57K, Moderate: 0.74K, Challenging: 0.85K), indicating a
reducing mean execution groups from 8.07 to 5.59, improving                 shift toward concise, goal-oriented reasoning that yields cor-
execution accuracy from 46.28% to 50.85%.                                   rect SQL. A representative case from the california schools
                                                                            database highlights this shift. Before RL (7.8K characters),
G. Evaluation on SQL Complexity                                             the model redundantly restates schema elements, explores
   To examine how model scale and our reward design in-                     irrelevant joins, and fails to produce a correct query. After
fluence reasoning robustness, we analyze performance across                 RL (0.7K characters), it quickly identifies relevant tables and
three SQL complexity levels – simple, moderate, and chal-                   fields, applies the correct expression and filter, and completes
lenging on the BIRD Dev. Fig. 12 presents results for all                   the SQL concisely.
competing systems. Despite relying on SLMs, FINER-SQL
maintains strong and consistent performance as query com-                                                            VI. C ONCLUSION
plexity increases. The 3B variant reaches 67.7% EX, closely
approaching Alpha-SQL 32B and surpassing Alpha-SQL 7B.                         We presented FINER-SQL, a reinforcement learning frame-
Meanwhile, the 1.5B model achieves 56.0% EX on moderate                     work that boosts small language models for Text-to-SQL
and 49.0% EX on challenging queries—outperforming DAIL-                     through fine-grained execution feedback and cost-efficient
SQL and SuperSQL with GPT-4. We further observe that RL                     rewards. With dense and interpretable signals (memory and
is a key driver of this robustness. Comparing FINER-SQL                     atomic rewards), FINER-SQL turns sparse supervision into
3B against its No RL counterpart, RL consistently improves                  continuous guidance, enabling stable GRPO optimization even
execution accuracy across all complexity levels: 74.16 vs.                  when SQL fails. Experiments on Spider and BIRD show that
70.49 on simple, 58.41 vs. 53.66 on moderate, and 54.48                     1.5B-3B models trained with our method achieve competitive
vs. 49.66 on challenging. These results also suggest that                   execution accuracy with 14B-70B models at a fraction of
methodology can outweigh raw model scale: even when using                   the cost, offering a practical path for efficient and privacy-
SLMs, FINER-SQL can handle complex reasoning and com-                       preserving Text-to-SQL deployment.
                              R EFERENCES                                              “Llama: Open and efficient foundation language models,” arXiv preprint
                                                                                       arXiv:2302.13971, 2023.
 [1] B. Wang, R. Shin, X. Liu, O. Polozov, and M. Richardson, “Rat-sql:           [22] A. Q. Jiang, A. Sablayrolles, A. Mensch et al., “Mistral 7b,” arXiv
     Relation-aware schema encoding and linking for text-to-sql parsers,” in           preprint arXiv:2310.06825, 2023.
     ACL, 2020, pp. 7567–7578.                                                    [23] T. T. Huynh, M. H. Nguyen, T. T. Nguyen, P. L. Nguyen, M. Weidlich,
 [2] S. Chang, J. Wang, M. Dong, L. Pan, H. Zhu et al., “Dr.spider: A                  Q. V. H. Nguyen, and K. Aberer, “Efficient integration of multi-order
     diagnostic evaluation benchmark towards text-to-SQL robustness,” in               dynamics and internal dynamics in stock movement prediction,” in
     ICLR, 2023.                                                                       Proceedings of the Sixteenth ACM International Conference on Web
 [3] Y. Gan, X. Chen, and M. Purver, “Exploring underexplored limitations of           Search and Data Mining, 2023, pp. 850–858.
     cross-domain text-to-SQL generalization,” in EMNLP, 2021, pp. 8926–          [24] C. T. Duong, T. T. Nguyen, H. Yin, M. Weidlich, T. S. Mai, K. Aberer,
     8931.                                                                             and Q. V. H. Nguyen, “Efficient and effective multi-modal queries
 [4] N. Q. V. Hung, M. Weidlich, N. T. Tam, Z. Miklós, K. Aberer, A. Gal,             through heterogeneous network embedding,” IEEE Transactions on
     and B. Stantic, “Handling probabilistic integrity constraints in pay-as-          Knowledge and Data Engineering, vol. 34, no. 11, pp. 5307–5320, 2022.
     you-go reconciliation of data models,” Information Systems, vol. 83, pp.     [25] T. T. Nguyen, Z. Ren, T. T. Nguyen, J. Jo, Q. V. H. Nguyen, and
     166–180, 2019.                                                                    H. Yin, “Portable graph-based rumour detection against multi-modal
 [5] M. H. Nguyen, T. T. Nguyen, J. Jo, D. A. Nguyen, H. Yin, and                      heterophily,” Knowledge-Based Systems, vol. 284, p. 111310, 2024.
     Q. V. H. Nguyen, “Handling data sparsity and model poisoning attacks in      [26] T. T. Nguyen, N. Quoc Viet Hung, T. T. Nguyen, T. T. Huynh, T. T.
     federated sequential recommender systems,” Knowledge-Based Systems,               Nguyen, M. Weidlich, and H. Yin, “Manipulating recommender systems:
     p. 115545, 2026.                                                                  A survey of poisoning attacks and countermeasures,” ACM Computing
 [6] T. T. Nguyen, T. T. Nguyen, M. Weidlich, J. Jo, Q. V. H. Nguyen, H. Yin,          Surveys, vol. 57, no. 1, pp. 1–39, 2024.
     and A. W.-C. Liew, “Handling low homophily in recommender systems            [27] Q. V. H. Nguyen, T. T. Nguyen, V. T. Chau, T. K. Wijaya, Z. Miklós,
     with partitioned graph transformer,” IEEE Transactions on Knowledge               K. Aberer, A. Gal, and M. Weidlich, “Smart: A tool for analyzing and
     and Data Engineering, 2024.                                                       reconciling schema matching networks,” in ICDE, 2015, pp. 1488–1491.
                                                                                  [28] Q. V. H. Nguyen, S. T. Do, T. T. Nguyen, and K. Aberer, “Tag-based
 [7] T. Yu, R. Zhang, K. Yang, M. Yasunaga, D. Wang, Z. Li, J. Ma, I. Li,
                                                                                       paper retrieval: minimizing user effort with diversity awareness,” in In-
     Q. Yao, S. Roman, Z. Zhang, and D. Radev, “Spider: A large-scale
                                                                                       ternational Conference on Database Systems for Advanced Applications,
     human-labeled dataset for complex and cross-domain semantic parsing
                                                                                       2015, pp. 510–528.
     and text-to-SQL task,” in EMNLP, 2018, pp. 3911–3921.
                                                                                  [29] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Prox-
 [8] J. Li, B. Hui, G. Qu, J. Yang, B. Li, B. Li, B. Wang, B. Qin, R. Geng,
                                                                                       imal policy optimization algorithms,” arXiv preprint arXiv:1707.06347,
     N. Huo et al., “Can llm already serve as a database interface? a big
                                                                                       2017.
     bench for large-scale database grounded text-to-sqls,” NeurIPS, vol. 36,
                                                                                  [30] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang,
     2024.
                                                                                       Y. Li, Y. Wu et al., “Deepseekmath: Pushing the limits of mathematical
 [9] H. Li, J. Zhang, H. Liu, J. Fan, X. Zhang, J. Zhu, R. Wei, H. Pan, C. Li,
                                                                                       reasoning in open language models,” arXiv preprint arXiv:2402.03300,
     and H. Chen, “Codes: Towards building open-source language models
                                                                                       2024.
     for text-to-sql,” SIGMOD, vol. 2, no. 3, pp. 1–28, 2024.
                                                                                  [31] Z. Yao, G. Sun, L. Borchmann, Z. Shen, M. Deng, B. Zhai, H. Zhang,
[10] S. Talaei, M. Pourreza, Y.-C. Chang, A. Mirhoseini, and A. Saberi,                A. Li, and Y. He, “Arctic-text2sql-r1: Simple rewards, strong reasoning
     “Chess: Contextual harnessing for efficient sql synthesis,” arXiv preprint        in text-to-sql,” arXiv preprint arXiv:2505.20315, 2025.
     arXiv:2405.16755, 2024.                                                      [32] B. Zhai, C. Xu, Y. He, and Z. Yao, “Excot: Optimizing reasoning for
[11] M. Pourreza, H. Li, R. Sun, Y. Chung, S. Talaei, G. T. Kakkar,                    text-to-sql with execution feedback,” arXiv preprint arXiv:2503.19988,
     Y. Gan, A. Saberi, F. Ozcan, and S. O. Arik, “Chase-sql: Multi-path               2025.
     reasoning and preference optimized candidate selection in text-to-sql,”      [33] T. T. Nguyen, T. C. Phan, M. H. Nguyen, M. Weidlich, H. Yin,
     arXiv preprint arXiv:2410.01943, 2025.                                            J. Jo, and Q. V. H. Nguyen, “Model-agnostic and diverse explanations
[12] K. T. Pham, T. T. Nguyen, V. Huynh, H. Yin, and Q. V. H. Nguyen,                  for streaming rumour graphs,” Knowledge-Based Systems, vol. 253, p.
     “An efficient and effective evaluator for text2sql models on unseen and           109438, 2022.
     unlabeled data,” in 2026 IEEE 42nd International Conference on Data          [34] C. T. Duong, T. T. Nguyen, T.-D. Hoang, H. Yin, M. Weidlich, and
     Engineering (ICDE). IEEE, 2026.                                                   Q. V. H. Nguyen, “Deep mincut: Learning node embeddings from
[13] Z. Ren, T. T. Nguyen, and W. Nejdl, “Prototype learning for interpretable         detecting communities,” Pattern Recognition, p. 109126, 2022.
     respiratory sound analysis,” in Proc. ICASSP, 2022, pp. 9087–9091.           [35] T. D. Hoang, T. T. Huynh, M. Weidlich, T. T. Nguyen, T. Chen, H. Yin,
[14] M. T. Pham, T. T. Huynh, T. T. Nguyen, T. T. Nguyen, T. T. Nguyen,                and Q. V. H. Nguyen, “Boosting small language models for text-to-
     J. Jo, H. Yin, and Q. V. Hung Nguyen, “A dual benchmarking study of               sql with fine-grained execution feedback and cost-efficient rewards,” in
     facial forgery and facial forensics,” CAAI Transactions on Intelligence           ICDE. IEEE, 2026.
     Technology, vol. 9, no. 6, pp. 1377–1397, 2024.                              [36] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma,
[15] S. Abedini, S. Mohapatra, D. Emerson, M. Shafieinejad, J. C. Cresswell,           P. Wang, X. Bi et al., “Deepseek-r1: Incentivizing reasoning capability
     and X. He, “Masksql: Safeguarding privacy for llm-based text-to-sql via           in llms via reinforcement learning,” arXiv preprint arXiv:2501.12948,
     abstraction,” arXiv preprint arXiv:2509.23459, 2025.                              2025.
[16] Z. Hui, Y. R. Dong, S. Sivapiromrat, E. Shareghi, and N. Collier,            [37] Y. Bai, A. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma,
     “Privacypad: A reinforcement learning framework for dynamic privacy-              D. Drain, S. Fort, D. Ganguli, T. Henighan et al., “Training a helpful and
     aware delegation,” arXiv preprint arXiv:2510.16054, 2025.                         harmless assistant with reinforcement learning from human feedback,”
[17] T. T. Nguyen, T. T. Huynh, Z. Ren, T. T. Nguyen, P. L. Nguyen, H. Yin,            arXiv preprint arXiv:2204.05862, 2022.
     and Q. V. H. Nguyen, “Privacy-preserving explainable ai: a survey,”          [38] Q. V. H. Nguyen, T. Nguyen Thanh, Z. Miklós, and K. Aberer,
     Science China Information Sciences, vol. 68, no. 1, p. 111101, 2025.              “Reconciling schema matching networks through crowdsourcing,” EAI
[18] T. Nguyen Thanh, N. D. K. Quach, T. T. Nguyen, T. T. Huynh, V. H.                 Endorsed Transactions on Collaborative Computing, vol. 1, no. 2, p. e2,
     Vu, P. L. Nguyen, J. Jo, and Q. V. H. Nguyen, “Poisoning gnn-based                2014.
     recommender systems with generative surrogate-based attacks,” ACM            [39] T. T. Nguyen, T. T. Nguyen, T. H. Nguyen, H. Yin, T. T. Nguyen, J. Jo,
     Transactions on Information Systems, vol. 41, no. 3, pp. 1–24, 2023.              and Q. V. H. Nguyen, “Isomorphic graph embedding for progressive
[19] T. T. Nguyen, T. T. Huynh, H. Yin, M. Weidlich, T. T. Nguyen, T. S.               maximal frequent subgraph mining,” ACM Transactions on Intelligent
     Mai, and Q. V. H. Nguyen, “Detecting rumours with latency guarantees              Systems and Technology, vol. 15, no. 1, pp. 1–26, 2023.
     using massive streaming data,” The VLDB Journal, vol. 32, no. 2, pp.         [40] R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and
     369–387, 2023.                                                                    C. Finn, “Direct preference optimization: Your language model is
[20] Y. Chung, G. T. Kakkar, Y. Gan, B. Milne, and F. Ozcan, “Is long                  secretly a reward model,” NeurIPS, vol. 36, pp. 53 728–53 741, 2023.
     context all you need? leveraging llm’s extended context for NL2SQL,”         [41] J. Hong, N. Lee, and J. Thorne, “Orpo: Monolithic preference optimiza-
     PVLDB, vol. 18, no. 8, pp. 2735–2747, 2025.                                       tion without reference model,” in EMNLP, 2024, pp. 11 170–11 189.
[21] H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux,               [42] T. T. Huynh, T. B. Nguyen, P. L. Nguyen, T. T. Nguyen, M. Weidlich,
     T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar et al.,                    Q. V. H. Nguyen, and K. Aberer, “Fast-fedul: A training-free federated
     unlearning with provable skew resilience,” in Joint European Confer-         [63] Q. V. H. Nguyen, C. T. Duong, T. T. Nguyen, M. Weidlich, K. Aberer,
     ence on Machine Learning and Knowledge Discovery in Databases.                    H. Yin, and X. Zhou, “Argument discovery via crowdsourcing,” The
     Springer, 2024, pp. 55–72.                                                        VLDB Journal, vol. 26, no. 4, pp. 511–535, 2017.
[43] B. Zhao, H. van der Aa, T. T. Nguyen, Q. V. H. Nguyen, and                   [64] T. T. Nguyen, T. C. Phan, H. T. Pham, T. T. Nguyen, J. Jo, and Q. V. H.
     M. Weidlich, “Eires: Efficient integration of remote data in event stream         Nguyen, “Example-based explanations for streaming fraud detection on
     processing,” in Proceedings of the 2021 International Conference on               graphs,” Information Sciences, vol. 621, pp. 319–340, 2023.
     Management of Data, 2021, pp. 2128–2141.                                     [65] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,
[44] V. Zhong, C. Xiong, and R. Socher, “Seq2sql: Generating structured                D. Zhou et al., “Chain-of-thought prompting elicits reasoning in large
     queries from natural language using reinforcement learning,” arXiv                language models,” NeurIPS, vol. 35, pp. 24 824–24 837, 2022.
     preprint arXiv:1709.00103, 2017.                                             [66] B. Li, Y. Luo, C. Chai, G. Li, and N. Tang, “The dawn of natural
[45] X. Xu, C. Liu, and D. Song, “Sqlnet: Generating structured queries                language to sql: Are we fully ready?” PVLDB, vol. 17, no. 11, pp.
     from natural language without reinforcement learning,” arXiv preprint             3318–3331, 2024.
     arXiv:1711.04436, 2017.                                                      [67] R. Murthy, P. Kumar, P. Venkateswaran, and D. Contractor, “Evaluating
[46] J. Guo, Z. Zhan, Y. Gao, Y. Xiao, J.-G. Lou, T. Liu, and D. Zhang,                the instruction-following abilities of language models using knowledge
     “Towards complex text-to-sql in cross-domain database with intermedi-             tasks,” arXiv preprint arXiv:2410.12972, 2024.
     ate representation,” in Proceedings of the 57th Annual Meeting of the        [68] Y. Qin, K. Song, Y. Hu, W. Yao, S. Cho, X. Wang, X. Wu, F. Liu,
     Association for Computational Linguistics, 2019, pp. 4524–4535.                   P. Liu, and D. Yu, “InFoBench: Evaluating instruction following ability
[47] T. Yu, M. Yasunaga, K. Yang, R. Zhang, D. Wang, Z. Li, and D. Radev,              in large language models,” in ACL, 2024, pp. 13 025–13 048.
     “SyntaxSQLNet: Syntax tree networks for complex and cross-domain             [69] J. Zhou, T. Lu, S. Mishra, S. Brahma, S. Basu, Y. Luan, D. Zhou, and
     text-to-SQL task,” in EMNLP, 2018, pp. 1653–1663.                                 L. Hou, “Instruction-following evaluation for large language models,”
[48] T. Scholak, N. Schucher, and D. Bahdanau, “Picard: Parsing incremen-              arXiv preprint arXiv:2311.07911, 2023.
     tally for constrained auto-regressive decoding from language models,”        [70] X.-B. Nguyen, X.-H. Phan, and M. Piccardi, “Fine-tuning text-to-
     in EMNLP, 2021, pp. 9895–9901.                                                    sql models with reinforcement-learning training objectives,” Natural
[49] D. C. Thang, N. T. Tam, N. Q. V. Hung, and K. Aberer, “An evaluation              Language Processing Journal, vol. 10, p. 100135, 2025.
     of diversification techniques,” in International Conference on Database      [71] H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee,
     and Expert Systems Applications, 2015, pp. 215–231.                               J. Leike, J. Schulman, I. Sutskever, and K. Cobbe, “Let’s verify step by
                                                                                       step,” in ICLR, 2024.
[50] T. T. Nguyen, M. Weidlich, H. Yin, B. Zheng, Q. H. Nguyen, and
     Q. V. H. Nguyen, “Factcatch: Incremental pay-as-you-go fact checking         [72] W. Yuan, R. Y. Pang, K. Cho, X. Li, S. Sukhbaatar, J. Xu, and J. E.
     with minimal user effort,” in Proceedings of the 43rd International               Weston, “Self-rewarding language models,” in ICML, 2024.
     ACM SIGIR Conference on Research and Development in Information              [73] J. Lu, Z. Dou, H. Wang, Z. Cao, J. Dai, Y. Feng, and Z. Guo, “Autopsv:
     Retrieval, 2020, pp. 2165–2168.                                                   Automated process-supervised verifier,” NeurIPS, vol. 37, pp. 79 935–
                                                                                       79 962, 2024.
[51] R. Sun, S. Ö. Arik, H. Nakhost, H. Dai, R. Sinha, P. Yin, and T. Pfister,
     “Sql-palm: Improved large language model adaptation for text-to-sql,”        [74] P. Wang, L. Li, Z. Shao, R. Xu, D. Dai, Y. Li, D. Chen, Y. Wu, and
     CoRR, 2023.                                                                       Z. Sui, “Math-shepherd: Verify and reinforce llms step-by-step without
                                                                                       human annotations,” in ACL, 2024, pp. 9426–9439.
[52] M. Pourreza and D. Rafiei, “Din-sql: Decomposed in-context learning
                                                                                  [75] B. Li, J. Zhang, J. Fan, Y. Xu, C. Chen, N. Tang, and Y. Luo, “Alpha-sql:
     of text-to-sql with self-correction,” 2023.
                                                                                       Zero-shot text-to-sql using monte carlo tree search,” in ICML, 2025.
[53] M. H. Nguyen, T. T. Huynh, T. T. Nguyen, P. L. Nguyen, H. T.
                                                                                  [76] M. Pourreza, S. Talaei, R. Sun, X. Wan, H. Li, A. Mirhoseini, A. Saberi,
     Pham, J. Jo, and T. T. Nguyen, “On-device diagnostic recommendation
                                                                                       S. Arik et al., “Reasoning-sql: Reinforcement learning with sql tai-
     with heterogeneous federated blocknets,” Science China Information
                                                                                       lored partial rewards for reasoning-enhanced text-to-sql,” arXiv preprint
     Sciences, vol. 68, no. 4, p. 140102, 2025.
                                                                                       arXiv:2503.23157, 2025.
[54] K. T. Pham, T. H. Nguyen, J. Jo, Q. V. H. Nguyen, and T. T.                  [77] T. D. Hoang, T. T. Nguyen, T. T. Huynh, H. Yin, and Q. V. H. Nguyen,
     Nguyen, “Multilingual text-to-sql: Benchmarking the limits of language            “Scaling text2sql via llm-efficient schema filtering with functional
     models with collaborative language agents,” in Australasian Database              dependency graph rerankers,” arXiv preprint arXiv:2512.16083, 2025.
     Conference. Springer, 2025, pp. 108–123.
                                                                                  [78] Y. Han, C. Liu, and P. Wang, “A comprehensive survey on vector
[55] D. D. A. Nguyen, M. H. Nguyen, P. L. Nguyen, J. Jo, H. Yin,                       database: Storage and retrieval technique, challenge,” arXiv preprint
     and T. T. Nguyen, “Multi-task learning of heterogeneous hypergraph                arXiv:2310.11703, 2023.
     representations in lbsns,” in International Conference on Advanced Data      [79] Y. Zhang, M. Li, D. Long, X. Zhang, H. Lin, B. Yang, P. Xie, A. Yang,
     Mining and Applications. Springer, 2024, pp. 161–177.                             D. Liu, J. Lin et al., “Qwen3 embedding: Advancing text embedding and
[56] S. Lyu, H. Luo, R. Li, Z. Ou, J. Sun, Y. Qin, X. Shang, M. Song, and              reranking through foundation models,” arXiv preprint arXiv:2506.05176,
     Y. Zhu, “Sql-o1: A self-reward heuristic dynamic search method for                2025.
     text-to-sql,” arXiv preprint arXiv:2502.11741, 2025.                         [80] J. Johnson, M. Douze, and H. Jégou, “Billion-scale similarity search
[57] D. C. Thang, H. T. Dat, N. T. Tam, J. Jo, N. Q. V. Hung, and K. Aberer,           with gpus,” T-BD, vol. 7, no. 3, pp. 535–547, 2019.
     “Nature vs. nurture: Feature vs. structure for graph neural networks,”       [81] X. Liu, S. Shen, B. Li, N. Tang, and Y. Luo, “Nl2sql-bugs: A benchmark
     PRL, vol. 159, pp. 46–53, 2022.                                                   for detecting semantic errors in nl2sql translation,” in Proceedings of
[58] H. T. Trung, T. Van Vinh, N. T. Tam, J. Jo, H. Yin, and N. Q. V.                  the 31st ACM SIGKDD Conference on Knowledge Discovery and Data
     Hung, “Learning holistic interactions in lbsns with high-order, dynamic,          Mining V. 2, 2025, pp. 5662–5673.
     and multi-role contexts,” IEEE Transactions on Knowledge and Data            [82] Z. Ren, Y. Chang, T. T. Nguyen, Y. Tan, K. Qian, and B. W. Schuller, “A
     Engineering, vol. 35, no. 5, pp. 5002–5016, 2022.                                 comprehensive survey on heart sound analysis in the deep learning era,”
[59] T. T. Huynh, C. T. Duong, T. T. Nguyen, V. T. Van, A. Sattar, H. Yin,             IEEE Computational Intelligence Magazine, vol. 19, no. 3, pp. 42–57,
     and Q. V. H. Nguyen, “Network alignment with holistic embeddings,”                2024.
     TKDE, vol. 35, no. 2, pp. 1881–1894, 2021.                                   [83] T. T. Nguyen, Z. Ren, T. Pham, P. L. Nguyen, Q. V. H. Nguyen, and
[60] Q. V. H. Nguyen, K. Zheng, M. Weidlich, B. Zheng, H. Yin, T. T.                   H. Yin, “A review of instruction-guided image editing,” EAAI, 2026.
     Nguyen, and B. Stantic, “What-if analysis with conflicting goals: Rec-       [84] M. T. Pham, Q. V. H. Nguyen, J. Jo, and T. T. Nguyen, “An extensible
     ommending data ranges for exploration,” in 2018 IEEE 34th Interna-                benchmark for value ambiguity resolution in text-to-sql,” in Australasian
     tional Conference on Data Engineering (ICDE). IEEE, 2018, pp. 89–                 Database Conference. Springer, 2025, pp. 124–138.
     100.                                                                         [85] T. T. Huynh, T. B. Nguyen, T. T. Nguyen, P. L. Nguyen, H. Yin,
[61] N. T. Toan, P. T. Cong, N. T. Tam, N. Q. V. Hung, and B. Stantic,                 Q. V. H. Nguyen, and T. T. Nguyen, “Certified unlearning for federated
     “Diversifying group recommendation,” IEEE Access, vol. 6, pp. 17 776–             recommendation,” ACM Transactions on Information Systems, 2025.
     17 786, 2018.                                                                [86] C. Yang, W. Yuan, L. Qu, and T. T. Nguyen, “Pdc-frs: Privacy-preserving
[62] N. Q. V. Hung, D. C. Thang, N. T. Tam, M. Weidlich, K. Aberer, H. Yin,            data contribution for federated recommender system,” in International
     and X. Zhou, “Answer validation for generic crowdsourcing tasks with              Conference on Advanced Data Mining and Applications. Springer,
     minimal efforts,” The VLDB Journal, vol. 26, pp. 855–880, 2017.                   2024, pp. 65–79.
[87] D. Sakong, V. H. Vu, T. T. Huynh, P. Le Nguyen, H. Yin, Q. V. H.
     Nguyen, and T. T. Nguyen, “Higher-order knowledge-enhanced recom-
     mendation with heterogeneous hypergraph multi-attention,” Information
     Sciences, vol. 680, p. 121165, 2024.
[88] H. Li, S. Wu, X. Zhang, X. Huang, J. Zhang, F. Jiang, S. Wang, T. Zhang,
     J. Chen, R. Shi et al., “Omnisql: Synthesizing high-quality text-to-sql
     data at scale,” arXiv preprint arXiv:2503.02240, 2025.
[89] Y. Meyer, M. Emadi, D. Nathawani, L. Ramaswamy, K. Boyd,
     M. Van Segbroeck, M. Grossman, P. Mlocek, and D. Newberry,
     “Synthetic-Text-To-SQL: A synthetic dataset for training language
     models to generate sql queries from natural language prompts,”
     April 2024. [Online]. Available: https://huggingface.co/datasets/gretelai/
     synthetic-text-to-sql
[90] M. Pourreza and D. Rafiei, “Din-sql: Decomposed in-context learning
     of text-to-sql with self-correction,” NeurIPS, vol. 36, pp. 36 339–36 348,
     2023.
[91] D. Gao, H. Wang, Y. Li, X. Sun, Y. Qian, B. Ding, and J. Zhou, “Text-
     to-sql empowered by large language models: A benchmark evaluation,”
     arXiv preprint arXiv:2308.15363, 2023.
[92] B. Wang, C. Ren, J. Yang, X. Liang, J. Bai, Q.-W. Zhang, Z. Yan,
     and Z. Li, “Mac-sql: Multi-agent collaboration for text-to-sql,” arXiv
     preprint arXiv:2312.11242, 2023.
[93] D. Lee, C. Park, J. Kim, and H. Park, “Mcs-sql: Leveraging multiple
     prompts and multiple-choice selection for text-to-sql generation,” in
     COLING, 2025, pp. 337–353.
[94] P. Ma, X. Zhuang, C. Xu, X. Jiang, R. Chen, and J. Guo, “Sql-r1:
     Training natural language to sql reasoning model by reinforcement
     learning,” arXiv preprint arXiv:2504.08600, 2025.
[95] T. Dao, D. Fu, S. Ermon, A. Rudra, and C. Ré, “Flashattention: Fast and
     memory-efficient exact attention with io-awareness,” NeurIPS, vol. 35,
     pp. 16 344–16 359, 2022.
[96] W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E.
     Gonzalez, H. Zhang, and I. Stoica, “Efficient memory management for
     large language model serving with pagedattention,” in SIGOPS, 2023.
[97] Y. Zhu, S. Lu, L. Zheng, J. Guo, W. Zhang, J. Wang, and Y. Yu,
     “Texygen: A benchmarking platform for text generation models,” in The
     41st international ACM SIGIR conference on research & development
     in information retrieval, 2018, pp. 1097–1100.
