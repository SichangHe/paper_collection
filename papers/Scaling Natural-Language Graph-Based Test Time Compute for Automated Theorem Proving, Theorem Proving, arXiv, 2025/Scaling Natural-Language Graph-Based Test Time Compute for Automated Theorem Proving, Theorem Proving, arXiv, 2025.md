                                           Scaling Natural-Language Graph-Based Test Time Compute for Automated
                                                                     Theorem Proving


                                                                    Vincent Li * 1 Tim Knappe * 2 Yule Fu 3 Kevin Zhu 4 Kevin Han 4


                                                                  Abstract                                      2020; Srivastava et al., 2023). Transformer-based mod-
                                                                                                                els have shown promise in mathematical problem-solving,
                                              Large language models have demonstrated re-
arXiv:2503.11657v3 [cs.CL] 23 May 2026




                                                                                                                which inherently requires multi-step logical inference and a
                                              markable capabilities in natural language process-                precise understanding of abstract concepts (Robinson and
                                              ing tasks requiring multi-step logical reasoning                  Voronkov, 2001; Guo et al., 2025). Despite these advance-
                                              capabilities, such as automated theorem prov-                     ments, significant challenges remain in automating the iden-
                                              ing. However, challenges persist within theo-                     tification of mathematical concepts, understanding their in-
                                              rem proving, such as the identification of key                    terrelations, and formalizing proofs within a mathematical
                                              mathematical concepts, understanding their in-                    framework (Hendrycks et al., 2021). Work by (Polu and
                                              terrelationships, and formalizing proofs correctly                Sutskever, 2020) introduced training language models to
                                              within natural language. We present KG-prover, a                  generate proofs in formal languages and use such models
                                              novel framework that leverages knowledge graphs                   to address the generation of original mathematical terms
                                              mined from reputable mathematical texts to aug-                   – leading to the introduction of the GPT-f proof assistant
                                              ment general-purpose LLMs to construct and for-                   for the Metamath formalization language. Systems such as
                                              malize mathematical proofs. We also study the ef-                 InternLM2.5-StepProver and DeepSeek-Prover-V2 directly
                                              fects of scaling graph-based, test-time compute us-               generate proof candidates in the Lean language, achieving
                                              ing KG-Prover, demonstrating significant perfor-                  state-of-the-art performance in a wide variety of theorem
                                              mance improvements over baselines across multi-                   proving benchmarks (Wu et al., 2024; Ren et al., 2025).
                                              ple datasets. General-purpose LLMs improve up
                                              to 21% on miniF2F-test when combined with KG-                     Recent advances in AI-driven mathematics have targeted
                                              Prover, with consistent improvements ranging                      the integration of neurosymbolic architectures with formal
                                              from 2-11% on the ProofNet, miniF2F-test, and                     verification frameworks. Systems such as DeepMath and
                                              MUSTARD datasets. Furthermore, KG-Prover                          HOList employ MCTS guided by graph neural networks to
                                              with o4-mini achieves 50% on pass miniF2F-test.                   prune combinatorial proof spaces (Bansal et al., 2019; Alemi
                                              This work provides a promising approach for aug-                  et al., 2017). These frameworks combine self-play reinforce-
                                              menting natural language proof reasoning with                     ment learning with backward-chaining, enabling exploration
                                              knowledge graphs without the need for additional                  of lemma sequences in interactive theorem provers.
                                              finetuning.                                                       A parallel line of research explores the use of natural lan-
                                                                                                                guage as an intermediate representation for guiding formal
                                                                                                                reasoning. Notably, Jiang et al. (2023) introduced a draft-
                                         1. Introduction                                                        sketch-prove pipeline, in which informal proof sketches are
                                                                                                                first generated in natural language and then incrementally
                                         The advent of Large Language Models has revolutionized                 translated into formal code. This enables the model to ex-
                                         natural language processing, enabling machines to per-                 ploit the flexibility of natural reasoning, though at the cost
                                         form complex reasoning tasks using transformer models                  of potential errors and ambiguity during the translation into
                                         (Vaswani et al., 2023; Peters et al., 2018; Brown et al.,              a formal theorem proving language such as Lean. Theorem-
                                             The second AI for MATH Workshop at the 42nd International          Llama attempts to bridge the gap between natural language
                                         Conference on Machine Learning, Vancouver, Canada * Equal con-         (NL) reasoning and formal language (FL) proofs using an
                                         tribution 1 Boston University 2 Provadis School of International       NL-FL aligned dataset for training while still integrating
                                         Management & Technology 3 Duke University 4 Algoverse AI Re-           NL text in the proof (Wang et al., 2024).
                                         search. Correspondence to: Vincent Li <vinli@bu.edu>.
                                                                                                                In this work, we introduce KG-Prover, a novel automated
                                         Proceedings of the 42 nd International Conference on Machine           theorem-proving framework allowing a general purpose
                                         Learning, Vancouver, Canada. PMLR 267, 2025. Copyright 2025
                                         by the author(s).                                                      LLM to semantically retrieve and traverse a knowledge

                                                                                                            1
                Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

graph derived from ProofWiki.                                         HyperTree Proof Search (Lample et al., 2022) demonstrated
                                                                      that structured search algorithms could enhance proof gen-
KG-Prover begins with selecting a starting node via se-
                                                                      eration in formal systems like Metamath. Furthermore, Wu
mantic embedding lookup, followed by iteratively and se-
                                                                      et al. (2022) showed that LLMs can effectively translate
lectively expanding the traversal of covered nodes by re-
                                                                      informal mathematical statements into formal logic, target-
turning the top-k most similar nodes. In the beam search
                                                                      ing Isabelle/HOL, proving that the resulting autoformalized
method, we implement LLMs as proof judges that return the
                                                                      specifications are sufficiently accurate to improve down-
most promising candidates (Zhu et al., 2025). The general-
                                                                      stream formal provers trained on them.
purpose LLM then generates an informal proof which is
then autoformalized and verified using Lean (de Moura and             Sampling and Compute Strategies Additionally, (Snell
Ullrich, 2021). We show that effective test time compute              et al., 2024) proposes a "compute-optimal" strategy that
scaling is achievable by simply modulating the graph traver-          dynamically adjusts resources based on task difficulty. This
sal depth.                                                            approach achieves efficiency gains over traditional sampling
                                                                      and allows smaller models to outperform larger counterparts
Unlike previous approaches, our framework does not rely
                                                                      in FLOPs-matched evaluations. The strategy is broadly
on large amounts of formal training data or intensive expert
                                                                      applicable in various complex reasoning domains, including
iteration. Instead, we operate with no specialized training,
                                                                      automated theorem proving.
leveraging the built-in natural language reasoning abilities
of general-purpose LLMs to synthesize graph-retrieved in-             Feedback Mechanisms and Self-Improving Agents In im-
formation before outputting an informal proof.                        proving feedback mechanisms, STP (Dong and Ma, 2025)
                                                                      uses self-play between conjecturer and prover agents, while
Our contributions are as follows:
                                                                      Formal Theorem Proving by Hierarchical Decomposition
                                                                      (Dong et al., 2024) rewards lemma decomposition via rein-
   • Develop KG-Prover, an automated theorem proving                  forcement learning. Finally, the MUSTARD project (Huang
     framework relying on natural language informal proof             et al., 2024) used an iterative approach where the LLM gen-
     generation combined with an iterative refinement-                erates a problem, constructs an informal proof, converts it
     based knowledge graph traversal and an LLM as a                  into Lean (de Moura et al., 2015) format, and verifies the
     judge.                                                           proof with a Lean interpreter. MUSTARD operates in three
                                                                      stages: sampling concepts, using generative models to cre-
   • We build a knowledge graph using ProofWiki of over
                                                                      ate problems and solutions, and employing proof assistants
     60,000 nodes and 300,000 edges that represent math-
                                                                      to validate these solutions. Jiang et al. (2023) proposed a
     ematical concepts and their interrelations, modeling
                                                                      three-phase framework that first drafts an informal proof in
     complex relationships with mathematically similar sub-
                                                                      natural language, then sketches a rough tactic script in Lean,
     jects.
                                                                      and finally invokes a formal prover to complete the remain-
   • We introduce an iterative refinement system based on a           ing subgoals. This approach illustrates how guidance can
     heuristic evaluation by a model judge and beam search            yield strong formal results, supporting our use of informal
     for further revisions, improving performance by up to            proof generation as a first-class component.
     26.4% over baseline and 21.8% over the non-scaling               Graph LMs and Retrieval Mechanisms Graph-based
     KG-Prover.                                                       retrieval-augmented generation techniques have also re-
                                                                      ceived growing attention for their ability to leverage struc-
2. Related Work                                                       tured relationships to enhance downstream tasks such as
                                                                      question answering and formal proof search. For instance,
Learning-Based Formal Provers Recent advancements                     GraphRetriever builds a passage graph whose edges are
in theorem proving have increasingly focused on integrat-             derived from an external knowledge base and uses it to
ing structured knowledge with LLMs. Notably, DeepSeek-                retrieve relevant passages for open-domain question answer-
Prover-V1.5 (Xin et al., 2024) combines reinforcement                 ing, outperforming text-only retrieval baselines (Min et al.,
learning from proof assistant feedback (RLPAF) with                   2019). Similarly, QA-GNN jointly reasons over a retrieved
Monte-Carlo tree search. The model, pre-trained on for-               question-relevant knowledge subgraph and language-model
mal mathematical languages like Lean 4, achieves state-               representations through a graph neural network, enabling
of-the-art results on miniF2F-test and ProofNet. It does              more interpretable and accurate reasoning within language
so by dynamically exploring diverse proof paths through               model generation (Yasunaga et al., 2021). Beyond ques-
intrinsic-reward-driven search. This builds on earlier work           tion answering, GRAG retrieves textual subgraphs and in-
such as LeanDojo (Yang et al., 2023), which introduced                tegrates the joint textual and topological information into
ReProver, an LLM-based prover enhanced with retrieval                 LLMs to enhance generation (Hu et al., 2024). Collectively,
capabilities to efficiently select theorem premises. Similarly,

                                                                  2
                Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

these works underscore the capabilities of knowledge graphs         3. Methodology
with LLMs for reasoning tasks, providing more effective
retrieval.                                                          Our framework automates mathematical proof generation
                                                                    by integrating LLMs with a knowledge graph constructed
Lean Provers Recent works in direct Lean proving have               from ProofWiki. We employ a multi-stage approach combin-
shown promising advances in consistently formalizing cor-           ing retrieval-augmented generation with a multi-step LLM
rect and rigorous mathematical proofs. By training and fine-        system for proof formalization. The system consists of
tuning LMs such as InternLM2.5-StepProver and DeepSeek-             four main components: 1) knowledge graph traversal, 2)
Prover-V2 to generate directly in Lean’s formal language,           informal proof generation, 3) formal proof generation, 4)
these systems demonstrate state-of-the-art performance in           verification and refinement. Figure 1 illustrates the overall
autoformalization tasks (Wu et al., 2024; Ren et al., 2025).        KG-Prover workflow.
InternLM 2.5–StepProver applies expert iteration entirely
within Lean, using curriculum learning and self-generated           3.1. Knowledge Graph Construction
proofs to continually improve a fine-tuned policy model. In
parallel, DeepSeek-Prover V2 leverages a large language             We built the underlying KG-Prover knowledge graph by
model to recursively decompose theorems into subgoals,              parsing ProofWiki, an online compendium organized into
combining this with reinforcement learning shaped by veri-          distinct namespaces such as "Definition," "Axiom," and
fier feedback. Both approaches treat the Lean environment           "Proof." By targeting these namespaces, we reliably ex-
as an interactive medium and fully disregard natural lan-           tracted the formal components: the precise definition state-
guage during inference.                                             ments, axiom listings, theorem propositions (including lem-
                                                                    mas and corollaries), and their corresponding proof details
TODO: transition from working in lean space to working in           (ProofWiki, 2025). In our pipeline, each node represents a
natural language space (using theoremllama paper)                   self-contained mathematical assertion–such as the text of a
Earlier efforts, such as TheoremLlama (Wang et al., 2024),          definition, the formal proposition of a theorem or lemma, or
demonstrated that even mid-sized open models can reach              a corollary–while the textual proof that follows is stored as a
strong formal proving performance when trained on boot-             property or linked entity. Hyperlinks within pages (e.g. ref-
strapped Lean–natural language pairs.                               erences to earlier theorems or definitions) become edges in
                                                                    the graph, capturing higher level dependencies and concep-
Integrating Graphs and forming proofs in natural lan-               tual relationships. We store this graph in a Neo4j (Webber,
guage Our model extends prior work by integrating a                 2012) graph database, augmenting each node with precom-
ProofWiki-derived knowledge graph with large language               puted embedding vectors using OpenAI’s text-embedding-
models for automated proof generation. Using natural lan-           3-large model. An example entry from our nodes collection
guage as an intermediate representation allows access to a          can be found in Appendix E.1. This structure enables ef-
much broader corpus of LaTeX-based and informal proofs              ficient semantic queries: given a problem statement, we
than formal codebases like Lean. It also harnesses LLMs’            compute its embedding and retrieve the top-k most similar
emergent reasoning abilities and exposes interpretable rea-         nodes to provide as a starting point for subsequent graph
soning traces that can reveal novel strategies. The tradeoff        traversals. Explicit details on the construction of the knowl-
is added error and complexity in the informal-to-formal             edge graph can be found in Appendix F.
translation, especially in semantically precise edge cases.
We address this with a two-agent system for informal                3.2. KG-Prover
proof generation and formalization, supported by retrieval-
                                                                    Our KG-Prover framework consists of four main compo-
augmented generation over graph-structured knowledge.
                                                                    nents: 1) knowledge graph traversal, 2) informal proof gen-
This follows trends in autoformalization seen in DeepSeek-
                                                                    eration, 3) formal proof generation, 4) verification and re-
Prover-V1.5, which combines RL and tree search, and The-
                                                                    finement.
oremLlama, which shows gains from natural language in-
termediaries. Our graph-based retrieval also aligns with
                                                                    3.2.1. R ETRIEVAL
work like GraphRetriever and QA-GNN, where structure
enables targeted, interpretable context. Iterative refinement       Let G = (V, E) be a knowledge graph, where V represents
and verification loops reflect recent advances in dynamic           all nodes as mathematical theorems and E represents the
test-time compute (Snell et al., 2024). Together, these el-         edges between them. Given a proposition P that we are
ements advance scalable, interpretable, modular theorem             tasked to prove, we use the below-signified similarity func-
proving with LLMs.                                                  tion that assigns a relevance score to each node based on its
                                                                    similarity to P .
                                                                    We opt for cosine similarity by generating an embedding

                                                                3
                  Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving




Figure 1. Whereas many modern proof systems focus on training time improvements, we integrate Node retrieval based on an intercon-
nected knowledge graph into our proof system at inference time. Before generating a proof, we inject the most similar nodes into the
context, then verify the proof using Lean. If the verification is unsuccessful, we grant the model the chance to traverse the graph deeper,
where the knowledge graph allows it to explore other related concepts and theorems, on multiple attempts.


vector for P , vP , and comparing vP to the other node                  3.2.2. I NFORMAL P ROOF G ENERATION
embeddings vi ∈ V in the knowledge graph:
                                                                        Informal proof generation integrates retrieved-context into
                                    vP · v i                            the language model prompt and uses the LLM to create an
              S = sim(vP , vi ) =
                                  ∥vP ∥2 ∥vi ∥2                         informal, natural language proof based on this enhanced
                                                                        input. Initially, generating a natural language proof allows
If P is not solved in the first iteration of generation, we             KG-Prover to take advantage of the repository of known
introduce a depth parameter d that can be incremented up to             proofs outlined within the knowledge graph. If the proof
an allowed depth D. We iteratively expand the context by                fails to pass the verification stage, the framework iteratively
selecting up to k additional nodes that are related concepts            deepens the context by one level in the knowledge graph,
of previously selected nodes.                                           selecting the top-k semantically closest neighboring nodes
                                                                        to uncover missing key concepts. The updated context is
          k1 , k2 , . . . , ki = arg max S(Vd , Vd−1 )                  then used for subsequent proof generation attempts.
                                 Vd−1 ∈V

where Vd−1 represents the set of all traversed nodes and Vd             3.2.3. F ORMAL P ROOF G ENERATION
represents the set of all 1-hop neighbors of Vd−1 . Math-
ematically Vd−1 is defined as the set of vj : ∃(a, b) ∈                 The autoformalization LLM ingests the code prefix, propo-
E where a ∈ Vd−1 . For each traversal, we select the top k              sition, and informal proof before generating the translated
1-hop neighbors ranked by our similarity function S.                    formal proof. The framework for both the Autoformalizer
                                                                        and the generator models can be found in Appendix E.2.1.
This expansion continues until either:                                  Finally, the autoformalizers’ output is parsed to extract well-
                                                                        specified Lean 4 code.
   • P is resolved by the language model.
   • The maximum depth D is reached and the amount of
     regenerating tries is expended.

                                                                    4
                Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

3.2.4. V ERIFICATION AND R EFINEMENT                                  4. Experiment Design
To ensure the formal correctness of the proofs generated by           4.1. Models
our framework, we adopted the Lean verification method
from DeepSeek-Prover-V1.5 to enhance the formalization                To create semantic representations in the form of embed-
step in our proof generation process, utilizing RLPAF to re-          dings, we used OpenAI’s text-embedding-3-large
fine our model’s ability to generate proofs that are verifiable       model (Neelakantan et al., 2022).
in Lean (Xin et al., 2024). By integrating proof-assistant            For informal proof generation, we utilized GPT-4o-mini, as
feedback, our models are more robust in producing proofs              well as Claude 3.5 Sonnet and a collection of LLAMA
that adhere to the strict syntactic and logical requirements          3 models (OpenAI, 2024; Anthropic, 2024; AI, 2024).
of Lean.                                                              We measure performance on the COT-reasoning models
The formal proofs were verified using Lean 4 to ensure cor-           Deepseek-R1, o1-mini, and o4-mini (Team, 2025).
rectness. The generated proof code was submitted to Lean,             As an Autoformalizer we use DeepSeek-Prover-V1.5 (Xin
and the results were analyzed. On failure, we extract error           et al., 2024), which is an open-source language model, de-
messages and feed them back into the autoformalizer along             signed for theorem proving in Lean (de Moura and Ullrich,
with adjusted prompts. This loop repeats until verification           2021). We use the model explicitly only for the translation
succeeds or we exhaust the allowed attempts r. If the max-            of the already generated informal proof into Lean format to
imum depth is not yet reached, we perform another graph               validate informal proofs.
traversal and generation loop.
                                                                      4.2. Datasets
3.3. Scaling KG-Prover
                                                                      To evaluate the effectiveness of our framework, we con-
Self-consistency has proven itself as strongly effective, on          ducted experiments on multiple benchmarks commonly
commonly used reasoning as well as mathematical tasks,                used in automated theorem proving: miniF2F1 , ProofNet,
making use of the different approaches a language model               and MUSTARDSAUCE (Zheng et al., 2022; Azerbayev
might take while sampling multiple responses (Wang et al.,            et al., 2023; Huang et al., 2024). MiniF2F is a bench-
2023). To utilize this phenomenon and improve robustness              mark dataset of formal mathematics problems sourced from
and accuracy under limited graph traversals, we incorporate           undergraduate-level mathematics competitions. ProofNet
test-time scaling, sampling, and search strategies:                   is a large-scale dataset of mathematical proofs and theorem
                                                                      statements, ranging in difficulty and domain. MUSTARD-
3.3.1. B EST- OF -N                                                   SAUCE is the dataset MUSTARD generated itself using
                                                                      GPT-4.
For each proof task, we generate n independent informal
proofs, autoformalize, and verify them. A dedicated model             Our exact dataset configuration can be found in Appendix
then acts as a judge, evaluating each candidate’s proof across        G.
dimensions of mathematical correctness, clarity, and reason-
ing completeness. The judge assigns scores from 0-10 and              4.3. Introduced Scaling Parameters
provides justification for each evaluation. Candidates are
then sorted by their scores, with the highest-scoring proof           For our evaluations, we introduce multiple parameters that
selected as the "optimal" solution to convert into Lean.              can be varied. In our evaluations:

3.3.2. B EAM S EARCH                                                     • k signifies the number of selected nodes from the cur-
                                                                           rent depth descending based on semantic similarity.
We organize proof candidates into a beam of width w and
search depth s. At each step, the top-w candidates are ex-               • r signifies the provided number of attempts on one
panded by generating refinements based on verifier feedback                individual proof.
(Sun et al., 2023). These refinements are then scored and                • d defines the depth the retriever is allowed to traverse
ranked, with the top-k candidates retained for subsequent                  in the knowledge graph.
iterations. The process repeats s times, ultimately return-
ing the "best" proof that is both high-quality in terms of               • n defines the number of candidates generated by best
interpretability and formally verifiable. This balances the                of N
exploration of diverse proof paths with verification-driven              • w or beam defines the width of the beam for the beam
refinement.                                                                search implementation
                                                                         1
                                                                           Unless stated otherwise, references to miniF2F denote the
                                                                      average performance across only the test split.

                                                                  5
                 Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

   • search_depth defines the depth during beam search                                                minif2f                         ProofNet
                                                                                        35
                                                                                                                          8




                                                                         Accuracy (%)
5. Results
                                                                                        30
                                                                                                                          6
5.1. Knowledge Graph Performance
                                                                                        25
As visualized in Table 1, using graphs consistently out-                                                                  4
performs baseline proof systems and over Retrieval Aug-
mented Generation. Performance gains of the KG-Prover                                   20
                                                                                             1    2   3   4   5   6   7       1   2   3   4   5   6   7
ranged from 2-11% across different models2 . Llama 3.1 8B
achieved a 31.97% success rate on miniF2F, compared to a                                40

20.49% baseline.
                                                                                                                                        LLAMA
ProofNet represents the most challenging dataset with the                               30
                                                                                                                                        o1-mini
lowest overall performance (2-7% success rates), attributed                                                                           LLAMA Base
to the difficulty of the problems. They require higher ab-                              20                                            o1-mini Base
stract mathematical reasoning and more intricate proof struc-
tures. The miniF2F dataset showed moderate performance                                       1    2   3   4   5   6   7
(20-31% success) because it includes more structured math-
                                                                                                 MUSTARDSAUCE
ematical problems, intermediate complexity of proofs, and
more predictable reasoning patterns.
MUSTARDSAUCE demonstrated moderate performance as                       Figure 2. Accuracy increases with greater traversal depth r in the
well (24-34% success).                                                  knowledge graph

5.2. Finetuned foundation models
                                                                        predominant in smaller parameter models, such as Llama
                                                                        3.1 8b. This behavior is captured in Figure 2. We can see
         Model                               minif2f
                                                                        that with more nodes injected, the performance rises.
         TheoremLlama (pass@128)             35.04%
         TheoremLlama + KG-Prover            36.89%                     5.4. Combined Scaling with Beam Search

Table 2. Using finetuned models with knowledge graph traversal          As visualized in Figure 3, combining the knowledge graph
depth = 6, witnesses improved performance over 128 rounds of            with approaches that can sample responses from the context
generation                                                              of the KG-Prover has a positive effect on accuracy across all
                                                                        benchmarks. Achieving up to 10.75% on ProofNet, 41.34%
                                                                        on miniF2F and 50.40% on MUSTARDSAUCE, which
As visualized in Table 2, using structured Knowledge of                 equates to improvements of 26.40% in the highest scaling
our KG-Prover with a depth of 6, performs 1.85 percent-                 configuration. Across all three dataset we find the first
age points better than a finetuned model outperforming the              three depth increases to be the most effective in scaling the
pass@1283 on finetuned Lean provers.                                    accuracy. While the leaps in accuracy flatten towards deeper
                                                                        depths, on harder datasets, we see the higher depths actually
5.3. Scaling Traversal Depth                                            still bring a consistent improvement.
To allow the model for failure correction and improvement,              Additionally, we see that even on depth one the performance
the graph system has multiple consecutive attempts defined              consistently beats the baseline and on average performs on
as r. Each attempt allows the model to traverse further in              par4 better than the KG-Prover without multiple candidate
the graph and explore more nodes.                                       proofs.
As more proofs get injected into the context and the model
gets more tries to correct initial mistakes, the accuracy scales        5.5. Performance Tradeoffs
higher per iterative refinement step. This effect is most               We isolate the cost that dominates monetary expenditure
   2
      Although top − k = 5 is a fixed parameter, the actual value       in practice: the number of language-model API calls and
can be smaller depending on the number of related nodes available       the prompt/response tokens for those calls consume. Auto-
at the current depth.                                                   formalization and Lean verification are performed on local
    3
      We follow the definition of pass@k defined by Chen et al.
                                                                                    4
(2021)                                                                                  considering slight deviations of ± 1%

                                                                    6
                              Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

                                                   Claude 3.5           Deepseek         Llama 3.1     Llama 3.3                        o1
         Dataset (↑)                  Method                                                                         GPT 4o
                                                    Sonnet                 R1               8B            70B                          -mini
                                      Base             2.69%             2.69%            3.76%         2.15%            3.23%         3.76%
         ProofNet                     RAG              3.76%             3.76%            3.76%         3.76%            5.38%         5.91%
                                      KG-Prover        4.84%             5.38%            4.30%         4.30%            6.45%         6.99%
                                      Base             22.95%           20.08%            20.49%        25.00%           23.36%       23.77%
         miniF2F                      RAG              28.69%           22.54%            24.59%        24.59%           28.69%       28.28%
                                      KG-Prover        31.15%           28.28%            31.97%        30.74%           30.74%       30.74%
                                      Base             28.00%           20.00%            24.00%        25.60%           28.00%       24.80%
         MUSTARD                      RAG              28.40%           25.00%            28.00%         28.8%           28.00%       26.80%
                                      KG-Prover        30.00%           27.00%            27.60%         32.5%           30.00%       34.00%

Table 1. Comparison of models across ProofNet, miniF2F, and MUSTARDSAUCE datasets. Accuracy scores reflect the performance of a
single run with a maximum of three attempts per proof, measured as a percentage of successful proof generations. The bolded numbers
show the largest performance gain from baseline to our KG-Prover for each dataset, achieving more than 11% gain.

                                       miniF2F                               ProofNet                            MUSTARDSAUCE

                                                               14                                       60
                         50
          Accuracy (%)




                                                               12
                                                                                                        50
                                                               10
                         40                                                                             40
                                                                8

                                                                6                                       30
                         30
                              1   2   3   4    5   6    7           1    2   3       4    5   6    7         1   2   3     4      5    6   7
                                  Traversal Depth r                      Traversal Depth r                       Traversal Depth r

                                                                                                                 LLaMA 8B             o4-mini

Figure 3. Comparing different depths for the beam search method on a set of parameters that are n = 5, beam width 3, search depth 2.


hardware and are therefore ignored in this section.                                  6. Conclusion & Discussion
                                                                                     We present a framework that automates mathematical proof
Notation Let Tp be the average prompt length (in tokens)                             generation by integrating LLMs with a knowledge graph to
for a single informal-proof request and Tr the average length                        utilize inter-dependencies across mathematical proofs. Our
of the LLM’s response. Our methods differ only in how                                approach demonstrates the potential of combining multiple
many times that request–response pair is issued.                                     mathematical concepts in an intertwined graph. By doing so,
                                                                                     language models can be effectively guided toward correct
                                                                                     proof generation, resulting in improved accuracy and en-
Implications
                                                                                     hanced abilities in both reasoning through and formalizing
                                                                                     proofs in natural language, whilst adding lean verification
   • Retries scale linearly. Each additional attempt multi-                          in a separate translation step.
     plies total spend by r but yields diminishing accuracy                          We establish that existing foundation models can achieve
     gains beyond r=3 (Figure 2).                                                    similar or higher performing results as fine-tuned models,
                                                                                     by simple context injections of related concepts during in-
   • Beam search is the price driver. The geometric factor                           ference time, without requiring any additional pre-training,
     n + w(ws − 1)/(w − 1) explodes quickly: doubling                                expert iteration, or training system of any kind. By doing
     the beam width from 3 to 6 would more than triple                               this we witness performance increases across datasets of up
     token usage while delivering ≤1 pp extra accuracy on                            to 11% by just using the KG-Prover and up to 26% when
     P ROOF N ET.

                                                                                 7
                 Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

                 Setting                    # completions               Token budget               Cost multiplier
                 BASE                              1                   Tp + T r                      1×
                 KG-P ROVER                        r                 r (Tp + Tr )                    r×
                                                s−1
                                                 P i                ws − 1                        ws − 1 
                 KG-P ROVER + B EAM        r n+w     w          r n+w           (Tp + Tr )      r n+w         ×
                                                    i=0                w−1                            w−1

Table 3. Language-model usage per problem instance (r traversal attempts, initial beam of n candidates, beam width w, tree depth s).


combined with proper scaling techniques.                               https://neo4j.com and could potentially be replaced
                                                                       with alternative graph databases as desired.
7. Limitations
                                                                       9. Ethical Considerations & Risks
Despite the advancements in capturing semantic relation-
ships in text via vectorized embeddings, embeddings can                Our knowledge base is derived from ProofWiki, an open
potentially suffer from issues such as loss of fine-grained            database for formal proofs. While the page is moderated,
logical structure and difficulties in preserving contextual            adversaries could attempt to incorporate harmful content
dependencies across larger passages. This can lead to chal-            or incorrect factual information into the extracted pages.
lenges in accurately retrieving relevant mathematical state-           However, we consider this risk to be unlikely.
ments, especially in formalized settings where precise defi-
                                                                       Although alignment work continues to progress Large Lan-
nitions and logical consistency are crucial. While we filter
                                                                       guage Models can introduce biases towards certain marginal-
and discard irrelevant details, signs, and other minutiae,
                                                                       ized groups or other minorities. All of our introduced mod-
XML dumps can introduce noise that might disrupt of affect
                                                                       els are moderated and have content filters that should pre-
the semantic search and embeddings.
                                                                       vent models from generating harmful content. However
While our approach successfully formalizes proofs from                 said filters aren’t perfect, models can still be exploited via
structured datasets, its performance on entirely novel or              sophisticated prompting and other adversarial techniques.
highly abstract mathematical problems remains uncertain.               Given our contribution to the framework, we expect no in-
Models trained on existing proofs may struggle with cre-               creased risk in any of the given safety evaluation measures
ative problem-solving or unconventional mathematical ap-               proposed.
proaches.
Large Language Models have finite context windows, mean-               9.1. GPU usage
ing lengthy or complex proofs may exceed the model’s
                                                                              GPU model            Watts     approx. usage Time
processing capacity. This might result in incomplete rea-
soning, loss of critical details, or forgetting earlier steps in             Nvidia A40           300 W           700 hours
multi-stage proofs.                                                       Nvidia RTX A5000        300 W            50 hours
Future work may enhance the knowledge graph and improve                       Table 4. Estimated GPU usage for all Evaluations.
the autoformalization process to handle more complex math-
ematical concepts.                                                     The shown GPU usage may only partially reflect an accu-
                                                                       rate measure of the computational resources required, as
8. Reproducibility Statement                                           major models are only available through API endpoints. We
                                                                       estimate the inference time on said APIs to be roughly 170
Our experiments were conducted using publicly avail-                   hours.
able Datasets and Models. GPT-4o, 4o-mini, o1-mini
and text-embedding-3-large can be accessed via https:
//openai.com/api/. Both Deepseek-R1 and the
                                                                       References
LLAMA 3 collection are open-sourced models. Claude                     Meta AI. The llama 3 herd of models, 2024. URL https:
models can be accessed via their respective API endpoints,              //arxiv.org/abs/2407.21783.
under https://www.anthropic.com/api.
                                                                       Alex A. Alemi, Francois Chollet, Niklas Een, Geoffrey
ProofNet and miniF2F, and MUSTARDSAUCE are pub-                          Irving, Christian Szegedy, and Josef Urban. Deepmath -
licly available datasets. Our Code is publicly available on              deep sequence models for premise selection, 2017. URL
GitHub; we encourage anyone to validate and extend our                   https://arxiv.org/abs/1606.04442.
findings. The Neo4j-based graph database can be used under
                                                                       Anthropic.      Claude 3.5 sonnet model card adden-

                                                                   8
               Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

  dum, 2024. URL https://www.anthropic.com/                       Kefan Dong and Tengyu Ma. STP: Self-play LLM theorem
  news/claude-3-5-sonnet.                                           provers with iterative conjecturing and proving. arXiv
                                                                    preprint arXiv:2502.00212, 2025.
Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers,
  D. Radev, and J. Avigad. Proofnet: Autoformalizing and          Kefan Dong, Arvind Mahankali, and Tengyu Ma. For-
  formally proving undergraduate-level mathematics. arXiv           mal theorem proving by rewarding LLMs to decompose
  preprint arXiv:2302.12433, 2023.                                  proofs hierarchically. arXiv preprint arXiv:2411.01829,
                                                                    2024.
K. Bansal, S. Loos, M. Rabe, C. Szegedy, and S. Wilcox.
                                                                  Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,
  Holist: An environment for machine learning of higher-
                                                                    Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi
  order theorem proving. In International Conference on
                                                                   Wang, and et al. Xiao Bi. Deepseek-r1: Incentivizing
  Machine Learning (ICML), 2019.
                                                                    reasoning capability in llms via reinforcement learning.
Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie                    arXiv preprint arXiv:2501.12948, 2025.
  Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Nee-           Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
  lakantan, Pranav Shyam, Girish Sastry, Amanda Askell,             Arora, Steven Basart, Eric Tang, Dawn Song, and Ja-
  Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger,           cob Steinhardt. Measuring mathematical problem solving
  Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M.               with the math dataset, 2021. URL https://arxiv.
  Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse,           org/abs/2103.03874.
  Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray,
  Benjamin Chess, Jack Clark, Christopher Berner, Sam             Yuntong Hu, Zhihan Lei, Zheng Zhang, Bo Pan, Chen Ling,
  McCandlish, Alec Radford, Ilya Sutskever, and Dario               and Liang Zhao. GRAG: Graph retrieval-augmented
  Amodei. Language models are few-shot learners, 2020.              generation. arXiv preprint arXiv:2405.16506, 2024.
  URL https://arxiv.org/abs/2005.14165.
                                                                  Yinya Huang, Xiaohan Lin, Zhengying Liu, Qingxing
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Hen-              Cao, Huajian Xin, Haiming Wang, Zhenguo Li, Linqi
 rique Ponde de Oliveira Pinto, Jared Kaplan, Harri Ed-             Song, and Xiaodan Liang. Mustard: Mastering uni-
 wards, Yuri Burda, Nicholas Joseph, Greg Brockman,                 form synthesis of theorem and proof data, 2024. URL
 Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov,             https://arxiv.org/abs/2402.08957.
 Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke              Albert Q. Jiang, Sean Welleck, Jin Peng Zhou, Wenda
 Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea              Li, Jiacheng Liu, Mateja Jamnik, Timothée Lacroix,
 Power, Lukasz Kaiser, Mohammad Bavarian, Clemens                   Yuhuai Wu, and Guillaume Lample. Draft, sketch,
 Winter, Philippe Tillet, Felipe Petroski Such, Dave                and prove: Guiding formal theorem provers with infor-
 Cummings, Matthias Plappert, Fotios Chantzis, Eliza-               mal proofs, 2023. URL https://arxiv.org/abs/
 beth Barnes, Ariel Herbert-Voss, William Hebgen Guss,              2210.12283.
 Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor
 Babuschkin, Suchir Balaji, Shantanu Jain, William Saun-          Guillaume Lample, Marie-Anne Lachaux, Thibaut Lavril,
 ders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh          Xavier Martinet, Amaury Hayat, Gabriel Ebner, Au-
 Achiam, Vedant Misra, Evan Morikawa, Alec Radford,                 rélien Rodriguez, and Timothée Lacroix. HyperTree
 Matthew Knight, Miles Brundage, Mira Murati, Katie                 proof search for neural theorem proving. In Advances in
 Mayer, Peter Welinder, Bob McGrew, Dario Amodei,                  Neural Information Processing Systems (NeurIPS), 2022.
 Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba.              arXiv:2205.11491.
 Evaluating large language models trained on code, 2021.
                                                                  Sewon Min, Danqi Chen, Luke Zettlemoyer, and Hannaneh
 URL https://arxiv.org/abs/2107.03374.
                                                                    Hajishirzi. Knowledge guided text retrieval and reading
L. de Moura and S. Ullrich. The lean 4 theorem prover               for open domain question answering. arXiv preprint
  and programming language. In Proceedings of the In                arXiv:1911.03868, 2019.
  Automated Deduction – CADE 28: 28th International               A. Neelakantan, T. Xu, R. Puri, A. Radford, J. M. Han, et al.
  Conference on Automated Deduction, 2021.                          Text and code embeddings by contrastive pre-training.
                                                                    arXiv preprint arXiv:2201.10005, 2022.
L. de Moura, S. Kong, J. Avigad, F. van Doorn, and J. von
   Raumer. The lean theorem prover (system description). In       OpenAI.        Gpt-4o mini: Advancing cost-efficient
  A. Felty and A. Middeldorp, editors, Automated Deduc-             intelligence. OpenAI Blog, July 18 2024. Avail-
   tion – CADE-25, volume 9195 of Lecture Notes in Com-             able     at:       https://openai.com/index/
   puter Science, pages 378–388. Springer, Cham, 2015.              gpt-4o-mini-advancing-cost-efficient-intelligence

                                                              9
               Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

Matthew E. Peters, Mark Neumann, Mohit Iyyer, Matt               Stein, Berk Ekmekci, Bill Yuchen Lin, Blake Howald,
 Gardner, Christopher Clark, Kenton Lee, and Luke                Bryan Orinion, Cameron Diao, Cameron Dour, Catherine
 Zettlemoyer. Deep contextualized word representa-               Stinson, Cedrick Argueta, César Ferri Ramírez, Chandan
 tions. In Marilyn Walker, Heng Ji, and Amanda Stent,            Singh, Charles Rathkopf, Chenlin Meng, Chitta Baral,
 editors, Proceedings of the 2018 Conference of the              Chiyu Wu, Chris Callison-Burch, Chris Waites, Christian
 North American Chapter of the Association for Com-              Voigt, Christopher D. Manning, Christopher Potts, Cindy
 putational Linguistics: Human Language Technologies,            Ramirez, Clara E. Rivera, Clemencia Siro, Colin Raffel,
 Volume 1 (Long Papers), pages 2227–2237, New Or-                Courtney Ashcraft, Cristina Garbacea, Damien Sileo, Dan
 leans, Louisiana, June 2018. Association for Computa-           Garrette, Dan Hendrycks, Dan Kilman, Dan Roth, Daniel
 tional Linguistics. doi: 10.18653/v1/N18-1202. URL              Freeman, Daniel Khashabi, Daniel Levy, Daniel Moseguí
 https://aclanthology.org/N18-1202/.                             González, Danielle Perszyk, Danny Hernandez, Danqi
                                                                 Chen, Daphne Ippolito, Dar Gilboa, David Dohan, David
S. Polu and I. Sutskever. Generative language model-             Drakard, David Jurgens, Debajyoti Datta, Deep Gan-
  ing for automated theorem proving. arXiv preprint              guli, Denis Emelin, Denis Kleyko, Deniz Yuret, Derek
  arXiv:2009.03393, 2020.                                        Chen, Derek Tam, Dieuwke Hupkes, Diganta Misra, Dil-
                                                                 yar Buzan, Dimitri Coelho Mollo, Diyi Yang, Dong-Ho
ProofWiki. Proofwiki: An online compendium of mathemat-
                                                                 Lee, Dylan Schrader, Ekaterina Shutova, Ekin Dogus
  ical proofs, 2025. URL https://proofwiki.org.
                                                                 Cubuk, Elad Segal, Eleanor Hagerman, Elizabeth Barnes,
  Accessed: 2025-01-31.
                                                                 Elizabeth Donoway, Ellie Pavlick, Emanuele Rodola,
Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin,              Emma Lam, Eric Chu, Eric Tang, Erkut Erdem, Ernie
  Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu,               Chang, Ethan A. Chi, Ethan Dyer, Ethan Jerzak, Ethan
  Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shi-             Kim, Eunice Engefu Manyasi, Evgenii Zheltonozhskii,
  rong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao,                Fanyue Xia, Fatemeh Siar, Fernando Martínez-Plumed,
  Daya Guo, and Chong Ruan. Deepseek-prover-v2: Ad-              Francesca Happé, Francois Chollet, Frieda Rong, Gaurav
  vancing formal mathematical reasoning via reinforce-           Mishra, Genta Indra Winata, Gerard de Melo, Germán
  ment learning for subgoal decomposition, 2025. URL             Kruszewski, Giambattista Parascandolo, Giorgio Mariani,
  https://arxiv.org/abs/2504.21801.                              Gloria Wang, Gonzalo Jaimovitch-López, Gregor Betz,
                                                                 Guy Gur-Ari, Hana Galijasevic, Hannah Kim, Hannah
Alan J. A. Robinson and Andrei Voronkov. Handbook of             Rashkin, Hannaneh Hajishirzi, Harsh Mehta, Hayden
  Automated Reasoning, Volume 1. 2001.                           Bogar, Henry Shevlin, Hinrich Schütze, Hiromu Yakura,
                                                                 Hongming Zhang, Hugh Mee Wong, Ian Ng, Isaac Noble,
Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar.         Jaap Jumelet, Jack Geissinger, Jackson Kernion, Jacob
  Scaling LLM test-time compute optimally can be more            Hilton, Jaehoon Lee, Jaime Fernández Fisac, James B.
  effective than scaling model parameters. arXiv preprint        Simon, James Koppel, James Zheng, James Zou, Jan Ko-
  arXiv:2408.03314, 2024.                                        coń, Jana Thompson, Janelle Wingfield, Jared Kaplan,
Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, Abu            Jarema Radom, Jascha Sohl-Dickstein, Jason Phang, Ja-
  Awal Md Shoeb, Abubakar Abid, Adam Fisch, Adam R.              son Wei, Jason Yosinski, Jekaterina Novikova, Jelle Boss-
  Brown, Adam Santoro, Aditya Gupta, Adrià Garriga-              cher, Jennifer Marsh, Jeremy Kim, Jeroen Taal, Jesse En-
  Alonso, Agnieszka Kluska, Aitor Lewkowycz, Akshat              gel, Jesujoba Alabi, Jiacheng Xu, Jiaming Song, Jillian
  Agarwal, Alethea Power, Alex Ray, Alex Warstadt,               Tang, Joan Waweru, John Burden, John Miller, John U.
  Alexander W. Kocurek, Ali Safaya, Ali Tazarv, Alice Xi-        Balis, Jonathan Batchelder, Jonathan Berant, Jörg Fro-
  ang, Alicia Parrish, Allen Nie, Aman Hussain, Amanda           hberg, Jos Rozen, Jose Hernandez-Orallo, Joseph Boude-
  Askell, Amanda Dsouza, Ambrose Slone, Ameet Ra-                man, Joseph Guerr, Joseph Jones, Joshua B. Tenenbaum,
  hane, Anantharaman S. Iyer, Anders Andreassen, An-             Joshua S. Rule, Joyce Chua, Kamil Kanclerz, Karen
  drea Madotto, Andrea Santilli, Andreas Stuhlmüller, An-        Livescu, Karl Krauth, Karthik Gopalakrishnan, Katerina
  drew Dai, Andrew La, Andrew Lampinen, Andy Zou,                Ignatyeva, Katja Markert, Kaustubh D. Dhole, Kevin
  Angela Jiang, Angelica Chen, Anh Vuong, Animesh                Gimpel, Kevin Omondi, Kory Mathewson, Kristen Chia-
  Gupta, Anna Gottardi, Antonio Norelli, Anu Venkatesh,          fullo, Ksenia Shkaruta, Kumar Shridhar, Kyle McDonell,
  Arash Gholamidavoodi, Arfa Tabassum, Arul Menezes,             Kyle Richardson, Laria Reynolds, Leo Gao, Li Zhang,
  Arun Kirubarajan, Asher Mullokandov, Ashish Sabhar-            Liam Dugan, Lianhui Qin, Lidia Contreras-Ochando,
  wal, Austin Herrick, Avia Efrat, Aykut Erdem, Ayla             Louis-Philippe Morency, Luca Moschella, Lucas Lam,
  Karakaş, B. Ryan Roberts, Bao Sheng Loe, Barret Zoph,         Lucy Noble, Ludwig Schmidt, Luheng He, Luis Oliv-
  Bartłomiej Bojanowski, Batuhan Özyurt, Behnam He-              eros Colón, Luke Metz, Lütfi Kerem Şenel, Maarten
  dayatnia, Behnam Neyshabur, Benjamin Inden, Benno              Bosma, Maarten Sap, Maartje ter Hoeve, Maheen Fa-

                                                            10
             Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

rooqi, Manaal Faruqui, Mantas Mazeika, Marco Batu-                Vishakh Padmakumar, Vivek Srikumar, William Fedus,
ran, Marco Marelli, Marco Maru, Maria Jose Ramírez                William Saunders, William Zhang, Wout Vossen, Xiang
Quintana, Marie Tolkiehn, Mario Giulianelli, Martha               Ren, Xiaoyu Tong, Xinran Zhao, Xinyi Wu, Xudong
Lewis, Martin Potthast, Matthew L. Leavitt, Matthias              Shen, Yadollah Yaghoobzadeh, Yair Lakretz, Yangqiu
Hagen, Mátyás Schubert, Medina Orduna Baitemirova,                Song, Yasaman Bahri, Yejin Choi, Yichi Yang, Yiding
Melody Arnaud, Melvin McElrath, Michael A. Yee,                   Hao, Yifu Chen, Yonatan Belinkov, Yu Hou, Yufang
Michael Cohen, Michael Gu, Michael Ivanitskiy, Michael            Hou, Yuntao Bai, Zachary Seid, Zhuoye Zhao, Zijian
Starritt, Michael Strube, Michał Sw˛edrowski, Michele             Wang, Zijie J. Wang, Zirui Wang, and Ziyi Wu. Be-
Bevilacqua, Michihiro Yasunaga, Mihir Kale, Mike Cain,            yond the imitation game: Quantifying and extrapolat-
Mimee Xu, Mirac Suzgun, Mitch Walker, Mo Tiwari,                  ing the capabilities of language models, 2023. URL
Mohit Bansal, Moin Aminnaseri, Mor Geva, Mozhdeh                  https://arxiv.org/abs/2206.04615.
Gheini, Mukund Varma T, Nanyun Peng, Nathan A.
                                                                Hao Sun, Xiao Liu, Yeyun Gong, Yan Zhang, Daxin
Chi, Nayeon Lee, Neta Gur-Ari Krakover, Nicholas
                                                                  Jiang, Linjun Yang, and Nan Duan. Allies: Prompt-
Cameron, Nicholas Roberts, Nick Doiron, Nicole Mar-
                                                                  ing large language model with beam search.       In
tinez, Nikita Nangia, Niklas Deckers, Niklas Muen-
                                                                  Houda Bouamor, Juan Pino, and Kalika Bali, edi-
nighoff, Nitish Shirish Keskar, Niveditha S. Iyer, Noah
                                                                  tors, Findings of the Association for Computational
Constant, Noah Fiedel, Nuan Wen, Oliver Zhang, Omar
                                                                  Linguistics: EMNLP 2023, pages 3794–3805, Singa-
Agha, Omar Elbaghdadi, Omer Levy, Owain Evans,
                                                                  pore, December 2023. Association for Computational
Pablo Antonio Moreno Casares, Parth Doshi, Pascale
                                                                  Linguistics. doi: 10.18653/v1/2023.findings-emnlp.
Fung, Paul Pu Liang, Paul Vicol, Pegah Alipoormo-
                                                                  247. URL https://aclanthology.org/2023.
labashi, Peiyuan Liao, Percy Liang, Peter Chang, Peter
                                                                  findings-emnlp.247/.
Eckersley, Phu Mon Htut, Pinyu Hwang, Piotr Miłkowski,
Piyush Patil, Pouya Pezeshkpour, Priti Oli, Qiaozhu Mei,        DeepSeek-AI Team. Deepseek-r1: Incentivizing reasoning
Qing Lyu, Qinlang Chen, Rabin Banjade, Rachel Etta                capability in llms via reinforcement learning, 2025. URL
Rudolph, Raefer Gabriel, Rahel Habacker, Ramon Risco,             https://arxiv.org/abs/2501.12948.
Raphaël Millière, Rhythm Garg, Richard Barnes, Rif A.
Saurous, Riku Arakawa, Robbe Raymaekers, Robert                 Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszko-
Frank, Rohan Sikand, Roman Novak, Roman Sitelew,                  reit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and
Ronan LeBras, Rosanne Liu, Rowan Jacobs, Rui Zhang,               Illia Polosukhin. Attention is all you need, 2023. URL
Ruslan Salakhutdinov, Ryan Chi, Ryan Lee, Ryan Sto-               https://arxiv.org/abs/1706.03762.
vall, Ryan Teehan, Rylan Yang, Sahib Singh, Saif M.             Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe
Mohammad, Sajant Anand, Sam Dillavou, Sam Shleifer,               Diao, Renjie Pi, and Tong Zhang. Theoremllama: Trans-
Sam Wiseman, Samuel Gruetter, Samuel R. Bowman,                   forming general-purpose llms into lean4 experts, 2024.
Samuel S. Schoenholz, Sanghyun Han, Sanjeev Kwa-                  URL https://arxiv.org/abs/2407.03203.
tra, Sarah A. Rous, Sarik Ghazarian, Sayan Ghosh, Sean
Casey, Sebastian Bischoff, Sebastian Gehrmann, Sebas-           Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le,
tian Schuster, Sepideh Sadeghi, Shadi Hamdan, Sharon              Ed Chi, Sharan Narang, Aakanksha Chowdhery, and
Zhou, Shashank Srivastava, Sherry Shi, Shikhar Singh,             Denny Zhou. Self-consistency improves chain of thought
Shima Asaadi, Shixiang Shane Gu, Shubh Pachchigar,                reasoning in language models, 2023. URL https:
Shubham Toshniwal, Shyam Upadhyay, Shyamolima,                   //arxiv.org/abs/2203.11171.
Debnath, Siamak Shakeri, Simon Thormeyer, Simone                J. Webber. A programmatic introduction to neo4j. In
Melzi, Siva Reddy, Sneha Priscilla Makini, Soo-Hwan                Proceedings of the 3rd annual conference on Systems,
Lee, Spencer Torene, Sriharsha Hatwar, Stanislas De-               programming, and applications: software for humanity
haene, Stefan Divic, Stefano Ermon, Stella Biderman,               (SPLASH ’12), 2012.
Stephanie Lin, Stephen Prasad, Steven T. Piantadosi,
Stuart M. Shieber, Summer Misherghi, Svetlana Kir-              Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N. Rabe,
itchenko, Swaroop Mishra, Tal Linzen, Tal Schuster, Tao           Charles Staats, Mateja Jamnik, and Christian Szegedy.
Li, Tao Yu, Tariq Ali, Tatsu Hashimoto, Te-Lin Wu,                Autoformalization with large language models, 2022.
Théo Desbordes, Theodore Rothschild, Thomas Phan,                 URL https://arxiv.org/abs/2205.12615.
Tianle Wang, Tiberius Nkinyili, Timo Schick, Timo-              Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan Ying,
fei Kornev, Titus Tunduny, Tobias Gerstenberg, Trenton            Jiayu Wang, Dahua Lin, and Kai Chen. Internlm2.5-
Chang, Trishala Neeraj, Tushar Khot, Tyler Shultz, Uri            stepprover: Advancing automated theorem proving via
Shaham, Vedant Misra, Vera Demberg, Victoria Nyamai,              expert iteration on large-scale lean problems, 2024. URL
Vikas Raunak, Vinay Ramasesh, Vinay Uday Prabhu,                  https://arxiv.org/abs/2410.15700.

                                                           11
               Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao,
 Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
 Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, Dejian
 Yang, Zhibin Gou, Z. F. Wu, Fuli Luo, and Chong Ruan.
  Deepseek-prover-v1.5: Harnessing proof assistant feed-
  back for reinforcement learning and monte-carlo tree
  search. arXiv preprint arXiv:2408.08152, 2024.

Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala,
  Peiyang Song, Shixing Yu, Saad Godil, Ryan Prenger,
  and Anima Anandkumar. Leandojo: Theorem proving
  with retrieval-augmented language models. NeurIPS,
  2023.

Michihiro Yasunaga, Hongyu Ren, Antoine Bosselut, Percy
 Liang, and Jure Leskovec. QA-GNN: Reasoning with
 language models and knowledge graphs for question an-
 swering. In Proceedings of the 2021 Conference of the
 North American Chapter of the Association for Com-
 putational Linguistics: Human Language Technologies
 (NAACL-HLT), 2021. arXiv:2104.06378.
K. Zheng, J. M. Han, and S. Polu. Minif2f: a cross-system
  benchmark for formal olympiad-level mathematics. arXiv
  preprint arXiv:2109.00110, 2022.

Lianghui Zhu, Xinggang Wang, and Xinlong Wang.
  Judgelm: Fine-tuned large language models are scalable
  judges, 2025. URL https://arxiv.org/abs/
  2310.17631.




                                                            12
                 Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

A. Using Lean provers for informal proof                                                                         Best of N
                                                                            Dataset      Model
   generation                                                                                           N=2         N=6       N=10
As discussed, our approach utilizes a two step process that                 ProofNet     Llama 8B      6.45%      5.38%       8.60%
generates an informal proof in natural language that is then
translated and validated in Lean. As visualized in Table 5,                 miniF2F      Llama 8B     30.33%      30.74%     31.97%
even Lean provers can be enhanced using the KG-Prover                       Mustard      Llama 8B     30.00%      32.80%      33.6%
that utilizes natural language.
                                                                          Table 6. Results by dataset with the graph approach, comparing
                                                                          “Best of N ” values between 2 and 10.
                              Theorem        DeepSeek
     Method
                               Llama        Prover-V1.5
     minif2f Base               32.38            35.75                    Graph knowledge base will yield identical outputs, given
     minif2f RAG                34.84            36.48                    that the input doesn’t change between different runs.
     minif2f KG-Prover          36.89            37.71
                                                                          While this behavior can be favorable in some situations,
Table 5. Lean-based provers show increased performance using              other evaluations may benefit from slight variations in dif-
the KG-Prover (traversal depth = 6) even when the Node data is in         ferent seeds. To introduce a slight stochasticity, other evalu-
natural language.                                                         ations may vary the temperature parameter of the employed
                                                                          models, and use the introduced method in Appendix D.1 to
This phenomenon demonstrates that even Lean-optimized                     introduce randomness into our knowledge graph.
and fine-tuned systems benefit from structured natural lan-
guage knowledge encompassing related proofs.                              D.1. Knowledge Graph Stochasticity
                                                                          To mitigate fully repetitive outputs Nodes from the knowl-
B. Structural Improvement                                                 edge graph, we propose top-k shuffling, where we retrieve
                                                                          the k-highest ranked nodes, shuffle them, and select a sub-
Few-shot learning, even with briefly related examples, has
                                                                          set. This method ensures diversity in individual generations.
been shown to improve performance across a variety of
                                                                          We favor this implementation over random sampling over
tasks and domains.
                                                                          a broader set of candidate nodes, selecting from a pool be-
Therefore we hypothesize that even only partly related proof              yond the strict top-k. Due to the potentially less relevant
nodes will improve not only the proof understanding but                   knowledge, trading off precision for increased coverage.
will also benefit the structured formalization that is required
                                                                          The level of stochasticity can be tuned dynamically based
for the correct interpretation and conversion of informal
                                                                          on confidence scores or response variance metrics
natural language into Lean4.

C. Judging the Best of N Tries                                            E. Examples
                                                                          E.1. Node example
Interestingly, the results in Table 6 reveal a non-linear rela-
tionship in more challenging datasets like ProofNet, where                   • from_id: The ID of the current node.
an intermediate value (e.g., N = 6) did not always out-
perform a lower or higher N . This suggests that simply
increasing the number of candidates is not universally bene-                 • to_id: The ID of the linked node (found using the
ficial; the quality of each candidate and the effectiveness of                 title-name-to-ID mapping).
the judging mechanism play critical roles. As such, finding
the right balance in model temperatures is crucial because an
optimal setting enhances the judging process by providing a                  • type: There are 6 different relationship categories:
diverse pool of high-quality candidates5 .
                                                                                USES_DEFINITION,
D. Deterministic Evaluations                                                    RELATED_DEFINITION,
                                                                                USES_AXIOM,
Unless specified otherwise, we use greedy decoding for all
                                                                                SIMILAR_PROOF,
of our experiments. Additionally, the semantic search in our
                                                                                PROOF_DEPENDENCY,
   5
     Both best of N and best of N + tree search method evaluations              PROOF_TECHNIQUE.
had LLama 3.1 8B set on a temperature of 0.7

                                                                     13
               Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

E.2. Prompt Examples                                               Informal Proof:
                                                                   [Your proof here]
E.2.1. P ROMPT E XAMPLE 1
The model was provided with the informal proof and a code          F. Graph Dataset
template, and it generated the corresponding formal proof
in Lean 4. Each element was processed to extract the title,        We parsed an XML dump of ProofWiki, where each
namespace, and content.                                            <page> element was processed. Irrelevant sections were
                                                                   filtered, and the wikitext was cleaned to obtain structured
                                                                   content.
You are a Lean 4 code generator.
We have:                                                           F.1. Node structure
HEADER:
{header}                                                           We represented each mathematical concept as a node in the
                                                                   knowledge graph, storing attributes such as:
INFORMAL PROOF:
{informal_proof}                                                      • id: Unique identifier.

PREFIX:                                                               • type: Content type (e.g., definition, theorem).
{informal_prefix}
                                                                      • title: Page title.
STATEMENT:                                                            • name: Extracted from the title.
{formal_statement}
                                                                      • content: Theorems in algebraic notation.
GOAL (optional):
{goal}
                                                                   G. Benchmarks
INSTRUCTIONS:                              All datasets present their samples with natural language and
1. Output exactly one triple-backtick code a formal statement in Lean, which we use as ground truth to
block containing valid Lean 4 code.        compare against.
2. Do not include any text or explanations
outside the code block.                    By utilizing miniF2F, ProofNet, and MUSTARDSAUCE,
3. Make sure it compiles in Lean 4.        we  assess our framework’s ability to generate and formalize
                                           proofs across diverse mathematical problems. The datasets
Required Format:                           provided a standardized evaluation setting, allowing us to
# Start                                    compare our results uniformly with existing approaches
‘‘‘lean4                                   and to analyze the strengths and limitations of our Method.
<Lean code here>                           However, it is possible that our setup deviates from the ones
‘‘‘                                        introduced in the respective papers of the dataset, which
# End                                      explains the varied performance across tasks, which is es-
                                           pecially apparent on MUSTARDSAUCE. To set up a com-
E.2.2. P ROMPT E XAMPLE 2                  parable evaluation, we compute the baseline of our setup as
                                           well, rather than taking the previous State-of-the-Art.
You are a mathematics expert focused on
generating clear informal proofs.          G.1. Used splits

Given the following mathematical problem We ran 186 problems from the test split of ProofNet, 244
and context, generate a clear and detailed problems from the test split of miniF2F, and randomly se-
informal proof in natural language.        lected 250 theorem-proving problems from MUSTARD-
                                           SAUCE.
Context: [Retrieved context]
                                                                   H. Search Strategies within the Knowledge
Problem: [Problem statement]                                          Graph
                                          To optimize the process of automated proof generation, we
Provide your proof in the following format:
                                          explored different methods for navigating the constructed

                                                              14
                Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

knowledge graph. Specifically, we implemented two pri-                 is associated with a high-dimensional embedding vector,
mary search strategies: Breadth-First Search (BFS) and                 enabling similarity computations.
semantic search using vector embeddings. This section elab-
                                                                       Hierarchical Prompting: Similar to the BFS approach, we
orates on these methodologies, their implementation in our
                                                                       begin with a zero-shot prompt. If unsuccessful, we incre-
framework, and analyzes their respective advantages and
                                                                       mentally include the most similar nodes into the context
disadvantages in our scenario.
                                                                       when re-prompting the GPT model, effectively performing
                                                                       one-shot, two-shot prompting, and so on.
H.1. Breadth-First Search (BFS)
                                                                       Semantic search is computationally less intensive than BFS,
Breadth-First Search is a classic graph traversal algorithm            as it avoids exhaustive traversal and focuses only on nodes
that systematically explores the vertices of a graph in layers,        with high semantic relevance. By prioritizing nodes that are
starting from a given root node and expanding outward to               semantically similar to the problem statement, we provide
neighboring nodes at increasing depths. In our framework,              the GPT model with highly pertinent information, poten-
BFS was utilized as follows:                                           tially improving proof generation quality. The disadvan-
                                                                       tages are that the effectiveness of semantic search is con-
 1. Zero-Shot Prompting: We initially present the prob-                tingent upon the embedding model’s ability to accurately
    lem statement directly to the GPT model without any                capture mathematical semantics, which may be challenging
    additional context, requesting a proof in a zero-shot              for complex or abstract concepts. Important nodes that are
    setting.                                                           not semantically similar based on the embedding (e.g., foun-
 2. First-Level Traversal: If the zero-shot attempt is un-             dational axioms or lemmas) may be overlooked, potentially
    successful, we perform a BFS to explore the immedi-                omitting crucial information required for the proof.
    ate neighboring nodes of the problem statement node.               Regardless of the search method used, we adopted an itera-
    Specifically, we retrieve up to the nearest 50 nodes               tive prompting strategy with the GPT model. This approach
    connected directly to the root node.                               allows us to manage the amount of information provided to
 3. Contextual Prompting: We then prompt the GPT                       the GPT model, aiming to strike a balance between context
    model again, providing the problem statement along                 richness and the model’s capacity to process and utilize the
    with the content from the retrieved neighboring nodes              information effectively.
    to supply additional context for proof generation.
 4. Iterative Expansion: If the proof remains incomplete               I. Failure Scenarios
    or incorrect, we extend the BFS to the next level by               Although we see strong performance across multiple proof
    including nodes that are two edges away from the root,             benchmarks, there are certain scenarios in which models &
    effectively expanding the context window before re-                techniques fail to function optimally. Across multiple runs,
    prompting the GPT model.                                           we found the following possible errors:

The advantage of BFS is that it allows for a systematic ex-               • The informal proof is correct, but the conversion into a
ploration of the knowledge graph, ensuring that all nodes                   formal proof fails.
within a certain depth are considered, which may uncover
relevant but non-obvious connections. By incrementally                    • The required knowledge is not in the graph, and other
increasing the depth of traversal, we can control the amount                topics are too briefly related to be extrapolated.
of additional information provided to the GPT model, po-
tentially improving the quality of the generated proof.                In our manual analysis, we found that approximately 35% of
                                                                       the failures occur when the formal proof is incorrect despite
However, BFS can be computationally expensive, especially              the informal proof being largely valid. This suggests that
in densely connected graphs, as the number of nodes grows              the challenge often lies not in the mathematical reasoning
exponentially with each additional level of depth. Including           itself, but in bridging the gap between informal and formal
a broad set of neighboring nodes may introduce irrelevant              representations. Informal proofs frequently rely on high-
or redundant information, which could overwhelm the GPT                level abstractions, implicit assumptions, or natural language
model and hinder its ability to generate a coherent proof.             shortcuts (e.g., “it follows that,” “by symmetry”) that do not
                                                                       always translate cleanly into Lean 4, which demands preci-
H.2. Semantic Search Using Embeddings                                  sion and fully explicit logic. Typical issues include omitted
                                                                       hypotheses, ambiguous theorem references, or imperfect
Semantic search leverages vector embeddings to identify
                                                                       formalization of induction and algebraic steps.
nodes that are semantically similar to a given query (Nee-
lakantan et al., 2022). Each node in our knowledge graph               It is rare that traversal doesn’t gather relevant information

                                                                  15
                Scaling Natural-Language Graph-Based Test Time Compute for Automated Theorem Proving

or that the knowledge is not available and only apparent on
particularly hard questions. However, for difficult questions,
such as those proposed by the International Math Olympiad,
the graph cannot find the most relevant nodes.




                                                                 16
