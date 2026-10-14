                                                 Saturation-Driven Dataset Generation for LLM
                                                 Mathematical Reasoning in the TPTP Ecosystem


                                                                              Valentin Quesnel1 and Damien Sileo1
                                                 1
                                                     Univ. Lille, Inria, CNRS, Centrale Lille, UMR 9189 - CRIStAL, F-59000 Lille, France
                                                                   valentinq2001@gmail.com, damien.sileo@inria.fr
arXiv:2509.06809v1 [cs.CL] 8 Sep 2025




                                                                                           Abstract
                                                       The scarcity of high-quality, logically sound data is a critical bottleneck for ad-
                                                       vancing the mathematical reasoning of Large Language Models (LLMs). Our
                                                       work confronts this challenge by turning decades of automated theorem proving
                                                       research into a scalable data engine. Rather than relying on error-prone LLMs
                                                       or complex proof-assistant syntax like Lean/Isabelle, our framework leverages E-
                                                       prover’s saturation capabilities on the vast TPTP axiom library to derive a massive,
                                                       guaranteed-valid corpus of theorems. Our pipeline is principled and simple: satu-
                                                       rate axioms, filter for "interesting" theorems, and generate tasks. With no LLMs in
                                                       the loop, we eliminate factual errors by construction. This purely symbolic data is
                                                       then transformed into three difficulty-controlled challenges: entailment verification,
                                                       premise selection, and proof reconstruction. Our zero-shot experiments on frontier
                                                       models reveal a clear weakness: performance collapses on tasks requiring deep,
                                                       structural reasoning. Our framework provides both the diagnostic tool to measure
                                                       this gap and a scalable source of symbolic training data to address it. We make the
                                                       code and data publicly available1


                                        1        Introduction
                                        Advancing the mathematical reasoning capabilities of Large Language Models (LLMs) is a central
                                        goal in AI, yet their performance in rigorous, multi-step logical deduction remains a critical weakness
                                        [Li et al., 2024]. This deficiency is largely attributed to a foundational issue: the extreme scarcity
                                        of high-quality training data [Wang and Deng, 2020, Xin et al., 2024]. Unlike domains rich with
                                        web-scale text or images, the corpus of formalized mathematical proofs is small, expensive to create,
                                        and requires specialized human expertise, making it impractical to crowdsource at scale [Wang and
                                        Deng, 2020, Trinh et al., 2024]. This data bottleneck severely hampers the training of more capable
                                        mathematical reasoners, motivating approaches that are logically grounded, resource-aware, and
                                        reproducible.
                                        Recently, a promising line of research has focused on synthetic data generation to overcome this
                                        scarcity [Yin and Gao, 2025, Wang and Deng, 2020]. However, many of these approaches either
                                        generate problems by prompting other LLMs, which carries a significant risk of introducing factual
                                        inconsistencies that require complex external verification in Interactive Theorem Provers (ITPs) like
                                        Lean or Isabelle [Xin et al., 2024, Wu et al., 2022], or generate random logical formulas that may
                                        lack mathematical relevance [Zombori et al., 2019].
                                        In this paper, we propose a different paradigm. Our framework is built in symbiosis with the mature
                                        automated theorem proving ecosystem. We use the saturation-based theorem prover E [Schulz, 2002]
                                             1
                                               Code and data available at:
                                            : https://github.com/sileod/reasoning_core
                                            : https://hf.co/datasets/reasoning-core/rc1

                                        Preprint. Under review.
not as a solver, but as a generative engine to exhaustively derive logical consequences from the
rich TPTP axiom library [Sutcliffe, 2017]. This purely symbolic approach ensures the mathematical
validity of every generated theorem by construction. After curating these results for "interestingness"
with AGInTRater [Puzis et al., 2006], we deconstruct the process of theorem proving into three
complementary facets of logical reasoning, each embodied by a distinct task with controllable
complexity:
      1. Conjecture Entailment: A true/false task testing deductive verification.
      2. Minimal Premise Selection: A distractor-based task requiring the identification of the
         minimal sufficient set of hypotheses
      3. Proof Graph Reconstruction: A structural reasoning task that involves ordering shuffled
         proof steps.
Our contribution is not a static dataset but a generative mechanism that produces varied and complex
tasks on demand. It provides a granular method for evaluating LLM reasoning depth, isolating
the pure logical capabilities of models from the ambiguities of natural language.

2   Related Work
Our work addresses the critical need for high-quality training data in automated theorem proving. We
position our contribution with respect to two dominant paradigms: LLM-based autoformalization and
procedural generation within Interactive Theorem Provers (ITPs).

Synthetic Data via LLM-driven Pipelines. A major line of research leverages LLMs to create new
training instances, primarily through autoformalization—translating natural language problems into
formal systems like Lean [Xin et al., 2024, Wu et al., 2022]. As seen in projects like TheoremLlama
[Wang et al., 2024], this paradigm can generate large datasets. However, this "LLM-in-the-loop"
approach faces significant drawbacks. It relies on the very models it seeks to improve and, because
LLM outputs are not guaranteed to be sound, necessitates a computationally expensive "generate-
then-verify" cycle using an Interactive Theorem Prover (ITP). This dependency not only confines
the generation process to a specific and complex proof-assistant syntax (e.g., Lean/Isabelle) but also
suffers from the high cost of rejection sampling due to frequent invalid proposals. Furthermore, being
trained on human data, LLMs tend to generate problems with a generative bias, favoring familiar
structures over more "exotic" or diverse logical paths. Our framework avoids these issues entirely:
by using saturation within the standardized TPTP ecosystem, we guarantee validity by construction,
operate independently of any proof-assistant syntax, and systematically explore the deductive space
for maximal diversity.

Procedural Generation and Proof Automation in ITPs. A second stream of work focuses on
procedural generation and proof automation within ITPs. Similar to our work, Aygün et al. [2021]
also generate synthetic theorems from TPTP axioms using a forward proposer. However, their
method uses a simple linear resolution strategy with random choices, which does not guarantee the
exploration of complex or diverse logical structures. Our approach is more systematic: by using a full
saturation engine (E-prover), we exhaustively explore a part of the deductive closure of the axioms,
a process limited in practice by a prover timeout. Furthermore, we curate this vast output with the
established interest metrics of AGInTRater [Puzis et al., 2006] to focus on non-trivial theorems, a
step absent in simpler random-walk generation.
This contrast is also visible when comparing to procedural generation in ITPs like Metamath or Lean
[Wang and Deng, 2020, Yin and Gao, 2025]. These methods often start from existing human-written
proofs to guide their search. Our approach is more foundational, requiring only axioms. Moreover,
while ITPs are powerful, they are fundamentally designed for human-guided, goal-directed proof,
not for exhaustive, open-ended saturation. Tools like Sledgehammer and Duper [Clune et al., 2024]
are powerful goal-directed solvers, but not inherently generative. By using a tool purpose-built for
saturation (E-prover), our framework is architecturally better suited for the large-scale, systematic
generation we propose.

Task Formulation for Evaluation. While most data generation efforts focus on creating (theorem,
proof) pairs for training provers [Lample et al., 2022, Aygün et al., 2021], a deeper evaluation of


                                                  2
reasoning requires more granular tasks. Premise selection, for instance, has been identified as a key
bottleneck [Irving et al., 2016], yet is often treated as a preliminary step rather than a standalone
evaluation. Our contribution is therefore not just a data generation method, but the formulation of a
structured suite of complementary tasks—entailment verification, minimal premise selection, and
proof graph reconstruction. By deconstructing the theorem-proving process, a concept explored in
systems like TRAIL [Crouse et al., 2021] which analyzes proof states, we provide a robust framework
for diagnosing the specific logical capabilities and failure modes of LLMs.


3        The Framework

                                                  Ô                                             ⋆
                                         Saturation Engine                            Interest Filter


                    õ
           TPTP Library                                                                                                   ? Entailment
                                                                                                                             True/False




                                                                                                                                              Controllable Difficulty
                                                                                           High interest
                                Axioms                             All theorems                                        Z Premise Selection
             30,000+ Axioms                  Derivation
               ALG, FLD, GEO                                                                                              Find minimal set
                                              Graph                                         Low interest
                SET, TOP, ...


                                                E-prover                                    AGInTRater
                                                                                                                       « Reconstruction
                                            Exhaustive inference                  Complexity & Usefulness & Surprise      Order proof steps
                 50+ domains

                                                                                                                       ¥ Vampire Validation
 100% Valid by Construction



Figure 1: From TPTP axioms to reasoning tasks through symbolic saturation. The pipeline guaran-
tees mathematical validity by construction, with E-prover generating exhaustive derivation graphs,
AGInTRater filtering for mathematical interest, and Vampire validating all outputs. Each stage is
fully deterministic and reproducible, producing unlimited tasks with controllable difficulty.

Our framework is a multi-stage, fully symbolic pipeline that transforms foundational axioms into a
rich repository of structured reasoning tasks. The process is designed to be automated and logically
sound by construction, leveraging a synergy of established automated reasoning tools.

3.1         Stage 1: Exhaustive Generation via Saturation

The core of our method is the generation of a comprehensive directed acyclic graph (DAG) of logical
derivations. We begin by selecting an axiom file from a specific domain within the TPTP library,
expressed in clausal normal form (CNF).
For this generative step, we specifically chose the E theorem prover. While many ATPs are
optimized for goal-directed search, E-prover offers exceptional flexibility and can be configured
to run in a pure saturation mode without a specific conjecture to prove. Saturation is a proof
procedure that exhaustively applies inference rules of the superposition calculus (like resolution
and paramodulation) to explore the deductive closure of the axiom set, a process that in practice is
bounded by computational limits, such as a timeout, due to the combinatorial explosion of clauses.
We configure E-prover to output a full proof graph, which meticulously records every derived clause
and its parent(s). This process yields a vast graph containing a systematic enumeration of the logical
consequences of the initial axiom set.

3.2         Stage 2: Curation with Interest Metrics

The saturation process is exhaustive by design and often produces a combinatorial explosion of
clauses, many of which are trivial, redundant, or overly complex. To focus on mathematically
meaningful theorems, we introduce a curation stage where the entire derivation graph is analyzed to
identify the most "interesting" results.
For this, we leverage AGInTRater [Puzis et al., 2006], a system that evaluates logical formulas not in
isolation, but within the context of their derivation. AGInTRater assigns a score to each non-axiom
clause based on a combination of heuristic metrics designed to emulate human judgment. These
metrics include:


                                                                        3
Complexity and Weight Measures the structural size of a formula, penalizing overly cumbersome
statements.

Surprisingness: Evaluates new relationships between concepts by measuring how infrequently
function and predicate symbols co-occur in the initial axioms.

Usefulness: Assesses a theorem’s utility as a lemma by calculating the ratio of its "interesting"
descendants to its total descendants within the derivation graph.
By providing the entire graph to AGInTRater, we obtain a contextualized score for each potential
theorem. This crucial step prunes the vast space of logical consequences, ensuring that the tasks
generated downstream are based on non-trivial and structurally relevant mathematical statements.
We emphasize that AGInTRater provides a heuristic score. We use it to prioritize non-trivial theorems
in a principled way, without claiming alignment with human judgments of mathematical interest. In
our experiments we simply retain the top-scoring items per domain and depth setting.

3.3   Stage 3: Task Formulation and Validation

The filtered graph is modeled using the NetworkX library. For each task generated, we use the
Vampire theorem prover [Kovács and Voronkov, 2013] as our ground-truth oracle. We chose
Vampire for this validation role due to its state-of-the-art performance and speed, consistently ranking
as a top prover in the CASC competitions. Its efficiency allows us to rapidly validate the thousands
of logical entailment queries needed to generate our benchmark tasks with 100% confidence up to
Vampire timeouts .

4     Generated Reasoning Tasks
From the curated and structured derivation graph, we deconstruct the process of theorem proving
into three complementary facets of logical reasoning, each embodied by a distinct task of increasing
complexity.

4.1   Task 1: Conjecture Entailment Verification

                                                                                         C. Task Formulation

                                                                                  Context Axioms:
             A. Derivation Graph              B. Extraction (d = 2)               Acontext = {Ax1 , . . .}
                                                                                  (For understanding only)

                                                     Acontext

       Ax1        Ax2        Ax3              Ax2                Ax3
                                                                                  Premise Subset:
                                                                       Pcorrect   Pperturbed = {L2 , Ldist }
             L1         L2         L3               L2           L3

       ...                              ...                                       Question:
                                                                                  Does the premise subset entail T?
                             T                               T
                                                                                  Answer: [True/False]




Figure 2: Generation pipeline for a Conjecture Entailment Verification task. A: We start from a
curated derivation graph. B: We extract a minimal set of lemmas Pcorrect at depth d. C: We form a
perturbed set Pperturbed and ask if it entails T .


Context and Premise Extraction: We select an interesting theorem T from the curated graph. We
perform two backward traversals from T :


                                                         4
       • Context Axioms: We trace the derivation all the way back to the foundational axioms to
         identify the complete set of axioms, Acontext , required for the proof. These axioms provide
         the necessary theoretical background (e.g., definitions of operators and predicates) for a
         model to understand the problem’s domain.
       • Immediate Premises: We perform a second traversal up to a predefined proof depth d. This
         yields a set of intermediate lemmas, Pcorrect , that are sufficient to prove T in d steps.

Controlled Premise Set Perturbation: We then create a perturbed premise set Pperturbed by applying
a controlled number of transformations, k, to Pcorrect . These transformations include adding, removing,
or replacing clauses from the original derivation graph. The number of perturbations k is another
parameter to modulate the task’s difficulty.

Task Formulation and Ground Truth: The LLM is presented with the context axioms Acontext ,
the perturbed premise set Pperturbed , and the theorem T . The prompt explicitly instructs the model that
the context axioms are for background understanding only, and that the entailment question—"Does
this specific set of premises entail the theorem?"—must be answered using only the statements in
Pperturbed . The ground truth (True or False) for this specific entailment is predetermined by Vampire.
By providing this contextual background while strictly delimiting the premises allowed for the
proof, we test the model’s ability to distinguish between general domain knowledge and the specific
hypotheses relevant to a particular deductive task. Modulating both proof depth and perturbations
allows us to precisely map the limits of this core reasoning skill.

4.2   Task 2: Minimal Premise Selection

                                                                             C. Task Formulation

                                                                         Theorem:
                                                                         Theorem T is provable from a
      A. Minimal Argument           B. Add Distractors & Shuffle         minimal subset of the premises
                                                    Ppool                below.
             Pminimal
                                                                         Premise Pool:
      Premise 1      Premise 2         Distractor A       Distractor B   1. Distractor A
                                                                         2. Premise 2
                                                                         3. Distractor B
                                        Premise 1           Premise 2    4. Premise 1
            Theorem T
                                                                         Question: Identify the mini-
                                                                         mal set of indices.
                                                                         Answer: [2, 4]

Figure 3: Generation pipeline for a Minimal Premise Selection task. A: theorem with minimal
premises Pminimal . B: embed into a larger pool Ppool with distractors and shuffle. C: the LLM
receives the shuffled, numbered pool and must return the indices of Pminimal .

This task targets a more advanced skill: identifying the necessary and sufficient hypotheses for a
proof from a noisy context. The difficulty is controlled by both the logical depth of the argument and
the amount of distracting information.

Generation Process:
      1. Context and Theorem Selection: We select an interesting theorem T from the curated
         graph and extract its foundational context axioms, Acontext .
      2. Minimal Premise Identification at Depth d: We identify a minimal set of premises,
         Pminimal , required to prove T . To control the argument’s complexity, we first extract a suffi-
         cient premise set, Psufficient , by performing a backward traversal from T up to a predefined
         proof depth d. We then apply an iterative pruning algorithm on Psufficient , using Vampire to
         guarantee minimality.


                                                      5
       3. Premise Pool Creation with k Distractors: We create a larger pool of premises, Ppool , by
          embedding Pminimal within a set of k distractor clauses. The number of distractors, k, is a
          parameter we can vary to control the signal-to-noise ratio of the task. These distractors are
          carefully selected from the same domain to be plausible but irrelevant.
       4. Task Formulation: The LLM is presented with the context axioms Acontext , the theorem T ,
          and the shuffled, numbered list of premises in Ppool . The prompt explicitly states that the
          theorem is provable from a subset of the provided pool and that its task is to identify the
          precise minimal subset of premises that are both necessary and sufficient for the proof.

The LLM must return the list of indices corresponding to the premises in Pminimal . By jointly
modulating the proof depth d and the number of distractors k, we can create a fine-grained
spectrum of tasks, from identifying short, obvious arguments in a clean context to pinpointing long,
complex reasoning chains in a very noisy one.

4.3   Task 3: Proof Graph Reconstruction


                                                                       C. Task Formulation

                                                                   Shuffled Clauses:
                                                                   1. Clause C3
  A. Original Proof Graph                                          2. Clause C7 (Theorem)
                                                                   3. Clause C5
                                                                   4. Clause C1
      C1        C2        C3        C4                             5. Clause C6
                                         B. Dissociate & Shuffle
                                                                   6. Clause C4
                                                                   7. Clause C2
           C5                  C6
                                                                   Question: Reconstruct the
                                                                   proof graph.
                     C7                                            Answer Format:
                                                                   3 <- 4, 7
                                                                   5 <- 1, 6
                                                                   2 <- 3, 5

Figure 4: Generation pipeline for a Proof Graph Reconstruction task. A: select a complete, binary
proof subgraph. B: dissociate structure and shuffle all clauses. C: the LLM receives the shuffled list
and must output derivation steps that reconstruct the original DAG.

This task moves beyond local inference to test an LLM’s capacity to understand and reconstruct the
global, hierarchical structure of a complete proof.

Generation Process:

       1. Proof Subgraph Selection: We select candidate proofs from our curated knowledge base
          that are well-suited for a structural reconstruction task. To ensure a clear and unambiguous
          dependency structure, we filter for proofs where each intermediate step is a binary inference,
          meaning every non-axiom clause is derived from exactly two parent clauses.
       2. Complexity Control: The difficulty of the task is controlled by the target proof depth d.
          We select proof subgraphs whose number of nodes (clauses) falls within a range correspond-
          ing to the typical size of a binary proof tree of depth d and with at least one path to axioms
          of the exact length of the proof depth. This allows us to generate tasks with a predictable
          structural complexity.
       3. Task Formulation: Once a suitable proof subgraph for a theorem T is selected, we provide
          the LLM with all its unique clauses as a shuffled, numbered list. The model must reconstruct
          the original derivation DAG by specifying the parent-child relationships for each non-axiom
          clause in the format CHILD_INDEX <- PARENT_1_INDEX, PARENT_2_INDEX.


                                                      6
Evaluation Metric:       The evaluation of the reconstructed graph is performed in two stages:
      1. Structural Coherence: First, we verify that the model’s output forms a valid, acyclic
         directed graph where each derived node has exactly two distinct parent nodes from the
         provided list. Outputs that fail this basic structural check receive a score of zero.
      2. Logical Soundness: For structurally coherent graphs, we then assess their logical validity.
         We perform a semantic check on each proposed inference step (CHILD <- PARENT_1,
         PARENT_2) using Vampire to verify that the child clause is a correct logical consequence of
         its proposed parents. The final score is the proportion of logically sound inference steps in
         the reconstructed graph.
This evaluation ensures that credit is awarded only for reconstructions that are both structurally well-
formed and logically correct, providing a rigorous measure of an LLM’s deep reasoning capabilities.

5     Experiments and Discussion
We conducted a series of experiments to validate the framework and probe the zero-shot reasoning
limits of state-of-the-art Large Language Models. Our evaluation systematically measures the impact
of logical complexity, task structure, and model scale on performance without any task-specific
fine-tuning.

5.1   Experimental Setup

Dataset and Tasks. We generated a benchmark of 3,000 problems, with 50 unique instances for
each configuration. The benchmark covers five diverse TPTP domains : Algebra (ALG), Fields
(FLD), Geometry (GEO), Set Theory (SET), and Topology (TOP). For Entailment Verification and
Premise Selection, we created a fine-grained difficulty matrix. We defined four difficulty levels:
Level 1 (Easy), Level 2 (Medium), Level 3 (Hard), and Level 4 (Very Hard). These levels are a
function of both the proof depth (d) and the number of distractors/perturbations (k). For Entailment,
k was sampled from {2, 3, 4, 6}, while for Selection, k was sampled from {2, 4, 6, 8}, with higher
values of d and k corresponding to higher difficulty levels. For Proof Reconstruction, we limited our
tests to proof depths of d ∈ {1, 2, 3, 4}, as deeper tasks proved intractable.

Models and Evaluation: We evaluated three models representing different scales: gpt-5-nano,
gpt-5-mini, and gpt-5 with reasoning effort parameters set to low. All evaluations were conducted
in a strict zero-shot setting, where models were given only the problem description and format
instructions, without any in-context examples. Performance was measured using the metrics defined
in Section 4 for each respective task.

5.2   Results and Discussion

Our results, summarized in Figure 5, reveal two primary findings regarding the zero-shot logical
reasoning capabilities of current LLMs.
First, performance systematically degrades with increased logical complexity. Across all tasks
and models, we observe a clear downward trend in scores as proof depth increases. This trend
confirms that our framework’s difficulty parametrization is effective and highlights that multi-step
inference is a core bottleneck for LLMs. The degradation is particularly stark for the Proof Re-
construction task, where performance for smaller models collapses even at shallow depths. This
suggests a fundamental weakness in global, structural reasoning; while models may handle local
inference, they are largely incapable of assembling a coherent, multi-step deductive argument from
scratch.
Second, model scale is a key factor, but it is not a panacea for structural reasoning. As expected,
larger models consistently outperform smaller ones, especially on tasks with higher proof_depth or
more distractors. The gpt-5 model, for instance, maintains a clear advantage on the most difficult
problem sets. However, even this state-of-the-art model struggles immensely with the Reconstruction
task. This indicates that while scaling improves performance on tasks requiring local deduction
(Entailment) and noise filtering (Selection), it is not, by itself, sufficient to unlock robust, hierarchical
planning abilities.


                                                     7
                                                               Performance by Task and Diffculty (with CI 95%)
                1.0
                                     Model: gpt-5-nano                               Model: gpt-5-mini                             Model: gpt-5
                                                          Difficulty
                                                            Easy
                                                            Medium
                                                            Hard
                0.8                                         Very_hard



                0.6
Average Score




                0.4



                0.2



                0.0
                        Entailment     Reconstruction    Selection      Entailment     Reconstruction    Selection    Entailment   Reconstruction   Selection

Figure 5: Performance comparison of three model scales on the three reasoning tasks, aggregated
across all domains. The average score (y-axis) is plotted against four levels of task difficulty. Two
key trends are apparent: (1) performance degrades for all models as difficulty increases, and (2) the
structural reasoning required for the Reconstruction task proves significantly more challenging than
other tasks, with smaller models failing almost completely.


                      Table 1: Model performance breakdown with difficulty level, reported as average score (%).

                                            Task Type          Model            Easy          Medium           Hard    Very Hard
                                                               gpt-5                 93           68             54          44
                                            All                gpt-5-mini            72           48             37          41
                                                               gpt-5-nano            65           38             29          35



Exploring the Frontier: High-Effort Reasoning on Intractable Tasks. To further investigate
the limits of structural reasoning, we conducted a small-scale exploratory study on high-difficulty
Reconstruction tasks (d = 4). We queried the largest state-of-the-art models using a high-effort
"thinking" mode. The results (detailed in Appendix 8) show that despite generating extensive chains
of thought, the model consistently failed to produce globally correct proof graphs. The reasoning
often identified correct local dependencies but failed to integrate them into a valid, overarching
structure. This reinforces our conclusion that the difficulty is not merely computational but stems
from a core deficit in the architectural capabilities of current models for hierarchical, symbolic
planning.
In summary, our experiments demonstrate that this framework provides a robust and granular
benchmark for assessing zero-shot logical reasoning. The results clearly show that even state-of-the-
art LLMs have profound weaknesses in multi-step, structural deduction, a limitation that is not fully
overcome by simply increasing model scale. This highlights the critical need for training data and
methods specifically designed to teach these complex reasoning skills, for which our framework can
provide a potentially endless source of material.


6                     Conclusion and Future Work

We have presented a novel framework for generating an endless supply of mathematically sound and
structurally complex reasoning tasks. By leveraging the power of symbolic automated reasoning, our
method ensures validity, provides fine-grained control over task difficulty, and covers a wide range of
mathematical domains. Our preliminary results demonstrate that the framework can effectively probe
the limitations of current LLMs, showing a marked decline in performance as logical depth increases,
particularly in tasks requiring global structural reasoning.
This work opens several exciting avenues for future research.


                                                                                          8
Training for Generalization: From Symbolic to Natural Language. Our primary research
direction is to use the datasets generated by our framework for fine-tuning Large Language Models.
This will allow us to test a central hypothesis: are symbolic reasoning skills transferable to natural
language? We plan to evaluate models fine-tuned on our data on existing benchmarks of mathematical
word problems to determine if mastering the underlying logical structure improves general reasoning
capabilities.

Scaling Complexity with Iterative Saturation. To generate even more complex and diverse
problems, we will implement an iterative saturation loop, an approach inspired by AGInT [Puzis
et al., 2006]. In this setup, the most "interesting" theorems from one generation round would be fed
back as new axioms for the next. This would allow us to explore the deductive closure of a theory
more deeply. However, we note that our current single-pass saturation method is already more than
sufficient to generate tasks that challenge even the most powerful state-of-the-art models.

Expanding the Logical Horizon to FOL. Finally, we plan to extend the framework to support full
first-order logic (FOL). Since our backend provers are already optimized for FOL, this is a natural
next step that will greatly increase the expressiveness of our tasks. We are releasing our open-source
code and generated datasets to facilitate this research, with the ultimate goal of fostering a new
generation of AI systems that can reason with mathematical rigor.

7   Limitations
Limitations and Design Choices. Our framework makes deliberate design choices that trade generality
for rigor. First, we work exclusively in CNF to ensure complete control over logical validity—while
this abstracts away natural language complexity, it allows us to isolate pure reasoning capabilities
without confounding factors. This is a feature, not a bug: by establishing baseline performance
on clean logical tasks, we can better understand where reasoning fails before adding linguistic
complexity.
Second, our evaluation focuses on the GPT family as a representative sample of state-of-the-art
models. While broader evaluation would be valuable, the consistent architecture allows us to isolate
the effect of scale on reasoning depth. The framework is model-agnostic and can be applied to any
LLM.
Third, the current scale (3,000 problems) represents a proof of concept. The generative nature of our
framework means it can produce arbitrary amounts of data on demand—we deliberately kept the
initial evaluation focused to establish clear trends rather than pursue scale for its own sake.




                                                  9
References
Eser Aygün et al. Learning to prove from synthetic theorems. In ICLR Workshop on Mathematical Reasoning in
  General AI, 2021.

Joshua Clune et al. Duper: A proof-producing superposition theorem prover for dependent type theory. In 15th
   International Conference on Interactive Theorem Proving (ITP 2024), 2024.

Maxwell Crouse et al. A deep reinforcement learning approach to first-order logic theorem proving. In
 Proceedings of the AAAI Conference on Artificial Intelligence, volume 35, pages 6279–6287, 2021.

Geoffrey Irving et al. Deepmath-deep sequence models for premise selection. Advances in Neural Information
  Processing Systems, 29, 2016.

Laura Kovács and Andrei Voronkov. First-order theorem proving and vampire. Computer Aided Verification,
  pages 1–35, 2013.

Guillaume Lample et al. Hypertree proof search for neural theorem proving. Advances in Neural Information
  Processing Systems, 35:26337–26349, 2022.

Zenan Li et al. Neuro-symbolic data generation for math reasoning. arXiv preprint arXiv:2412.04857, 2024.

Yury Puzis, Yi Gao, and Geoff Sutcliffe. Automated generation of interesting theorems. Proceedings of the 21st
  National Conference on Artificial Intelligence, pages 49–54, 2006.

Stephan Schulz. E: A brainiac theorem prover. AI communications, 15(2-3):111–126, 2002.

Geoff Sutcliffe. The tptp problem library and associated infrastructure. Journal of Automated Reasoning, 59:
  483–502, 2017.

Trieu H. Trinh et al. Solving olympiad geometry without human demonstrations. Nature, 625(7995):476–482,
   2024.

Mingzhe Wang and Jia Deng. Learning to prove theorems by learning to generate theorems. Advances in Neural
  Information Processing Systems, 33:18146–18157, 2020.

Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe Diao, Renjie Pi, and Tong Zhang. TheoremLlama:
  Transforming general-purpose LLMs into Lean4 experts, 2024. URL https://arxiv.org/abs/2405.
  14343.

Yuhuai Wu et al. Autoformalization with large language models. Advances in Neural Information Processing
  Systems, 35:32353–32368, 2022.

Huajian Xin et al. Deepseek-prover: Advancing theorem proving in llms through large-scale synthetic data.
  arXiv preprint arXiv:2405.14333, 2024.

David S. Yin and Jing Gao. Generating millions of lean theorems with proofs by exploring state transition
  graphs. arXiv preprint arXiv:2503.04772, 2025.

Zsolt Zombori et al. Towards finding longer proofs. arXiv preprint arXiv:1905.13100, 2019.


8     Appendix
8.1     Prompt Examples for Generated Tasks

8.1.1    Task 1: Conjecture Entailment Verification
The theorem used in this example demonstrates a fundamental property of set theory.

Formal Clause: (disjoint(X1,complement(X2))|~subset(X1,X2))
Summary: A set fully contained within another has no elements outside of it.

Below is a full example of the prompt provided to the LLM for the entailment task.


                                                     10
                                 Listing 1: Prompt for the Entailment Task.
You will be given a logical entailment problem in three parts .

PART 1: CONTEXT
The following are general axioms from the domain of ** Algebra **.
They provide definitions and background theory .
** Do NOT use them directly in the proof .**

-   cnf ( disjoint2 , axiom ,( disjoint ( X1 , X2 ) | member ( f23 ( X1 , X2 ) , X1 ) ) )
-   cnf ( complement1 , axiom ,(~ member ( X1 , complement ( X2 ) ) |~ member ( X1 , X2 ) ) )
-   cnf ( disjoint3 , axiom ,( disjoint ( X1 , X2 ) | member ( f23 ( X1 , X2 ) , X2 ) ) )
-   cnf ( subset1 , axiom ,( member ( X3 , X2 ) |~ subset ( X1 , X2 ) |~ member ( X3 , X1 ) ) )


PART 2: THE SPECIFIC PROBLEM
Your task is to evaluate the following specific entailment claim .

** Premises to use :**
- ( disjoint ( X1 , complement ( X2 ) ) |~ member ( f23 ( X1 , complement ( X2 ) ) , X2 ) )
- ( subset ( image ( X1 , domain_of ( X2 ) ) , X3 ) |~ disjoint ( X2 , universal_set ) )
- ( associative ( X1 , X2 ) |~ disjoint ( X1 , X3 ) |~ member ( f35 ( X1 , X2 ) , X3 ) )
- ( disjoint ( X1 , X2 ) | member ( f23 ( X1 , X2 ) , X3 ) |~ subset ( X1 , X3 ) )


** Conclusion to prove :**
( disjoint ( X1 , complement ( X2 ) ) |~ subset ( X1 , X2 ) )


PART 3: YOUR TASK
Based ** only ** on the ’ Premises to use ’ , does the ’ Conclusion to prove
    ,→ ’ logically follow ?
Answer with a single word : ‘ True ‘ or ‘ False ‘.

--- EXPECTED OUTPUT --- ’ True ’


8.1.2   Task 2: Minimal Premise Selection
This task uses a non-trivial theorem related to the Axiom of Infinity, linking infinite-like sets to the structure of
the universe.

Formal Clause: (~inductive(X1)|~subclass(X1,complement(X2))|~subclass(universal_class,X2))
Summary: If an infinite-like set exists outside of another set, then that latter set cannot be the entire universe.

Below is a full example of the prompt provided to the LLM for the selection task.
                             Listing 2: Prompt for the Premise Selection Task.
You are a mathematical logic assistant .
Your task is to identify a minimal set of premises sufficient for a
    ,→ proof .

## General Context
The problem is set in the domain of : ** Set Theory **.
The following are the fundamental axioms of this domain .
They provide general context . ** Do not use them in the proof itself .**
Fundamental Axioms :
- cnf ( equal_implies_subclass2 , axiom ,( subclass ( X2 , X1 ) | X1 != X2 ) )
- cnf ( complement1 , axiom ,(~ member ( X1 , complement ( X2 ) ) |~ member ( X1 , X2 ) ) )
- cnf ( inductive1 , axiom ,( member ( null_class , X1 ) |~ inductive ( X1 ) ) )
- cnf ( omega_is_inductive2 , axiom ,( subclass ( omega , X1 ) |~ inductive ( X1 ) ) )
- cnf ( omega_is_inductive1 , axiom ,( inductive ( omega ) ) )
- cnf ( not_subclass_members1 , axiom ,( member ( not_subclass_element ( X1 , X2 ) ,
    ,→ X1 ) | subclass ( X1 , X2 ) ) )


                                                         11
- cnf ( regularity1 , axiom ,( X1 = null_class | member ( regular ( X1 ) , X1 ) ) )
- cnf ( subclass_implies_equal , axiom ,( X1 = X2 |~ subclass ( X1 , X2 ) |~ subclass (
   ,→ X2 , X1 ) ) )
- cnf ( subclass_members , axiom ,( member ( X3 , X2 ) |~ subclass ( X1 , X2 ) |~ member (
   ,→ X3 , X1 ) ) )
- cnf ( not_subclass_members2 , axiom ,( subclass ( X1 , X2 ) |~ member (
   ,→ not_subclass_element ( X1 , X2 ) , X2 ) ) )
- cnf ( class_elements_are_sets , axiom ,( subclass ( X1 , universal_class ) ) )

## Task
Your goal is to prove the following theorem :
** Theorem :**
‘(~ inductive ( X1 ) |~ subclass ( X1 , complement ( X2 ) ) |~ subclass (
    ,→ universal_class , X2 ) ) ‘

Below is a numbered pool of potential premises .
Your task is to identify the ** minimal subset ** of numbers from this
    ,→ pool
whose corresponding statements are ** sufficient on their own ** to
    ,→ prove the theorem .

** Pool of Premises :**
1. ( subclass ( complement ( X1 ) , X2 ) |~ subclass ( universal_class , X1 ) )
2. ( null_class = X1 | null_class = X2 |~ inductive ( unordered_pair ( X2 , X1 ) ) )
3. (~ inductive ( X1 ) |~ subclass ( X2 , null_class ) |~ subclass ( X1 , X2 ) )
4. ( member ( omega , X1 ) | intersection ( X2 , X1 ) != universal_class )

### Question
Which is the smallest set of numbered premises from the pool that is
    ,→ sufficient to prove the theorem ,
without using the fundamental axioms from the context ?

### Response Format
Your answer must be ** only ** a list of numbers , sorted in increasing
    ,→ order . For example : ‘[2 , 5 , 8] ‘.

--- EXPECTED OUTPUT - - -[1 , 3 , 7]


8.1.3   Task 3: Proof Graph Reconstruction
This example features a complex theorem from topology, illustrating a consistency constraint within the formal
system.

Formal Clause: (subset_sets(X1,X2) |
               ~element_of_collection(union_of_members(top_of_basis
               (top_of_basis(subspace_topology(X2,X3,X1))))),X4) |
               ~element_of_set(X5,intersection_of_members(X4)))
Summary: To logically define a ’subspace’ structure, the object must first be a ’subset’.

Below is a full example of the prompt provided to the LLM for the reconstruction task.

                      Listing 3: Prompt for the Proof Graph Reconstruction Task.

Your task is to reconstruct the dependency graph of a mathematical
    ,→ proof from the domain of ** Topology **.

The proof graph concludes with the theorem :
‘( subset_sets ( X1 , X2 ) |~ el ement_ of_co llecti on ( union_of_members (
    ,→ top_of_basis ( top_of_basis ( subspace_topology ( X2 , X3 , X1 ) ) ) ) , X4 ) |~
    ,→ element_of_set ( X5 , i nt e rs ec ti o n_ of _ me mb er s ( X4 ) ) ) ‘

## Proof Context & Rules
This proof was generated by using the ** Superposition Calculus ** (
    ,→ which includes rules like Resolution and Paramodulation ) .


                                                      12
Therefore , the proof has the following properties :
- ** Starting Points :** Some clauses in the list are starting points (
    ,→ axioms ) and are not derived from other clauses .
- ** Derived Clauses :** Every other clause is derived from exactly **
    ,→ two ** parent clauses from the list .
- ** Clause Reuse :** A single clause can be used as a parent in
    ,→ multiple derivation steps .

## Your Task
Given the rules above , reconstruct the proof from the following
   ,→ shuffled list of clauses .
Identify the derivation for every clause that is not a starting point .

** Shuffled Clauses :**
1. ( element_of_set ( X3 , f10 ( X2 , X1 , X3 ) ) |~ el ement_ of_co llecti on ( X1 ,
    ,→ top_of_basis ( X2 ) ) |~ element_of_set ( X3 , X1 ) )
2. ( subset_sets ( X1 , X2 ) |~ element_of_set ( X3 , union_of_members (
    ,→ top_of_basis ( subspace_topology ( X2 , X4 , X1 ) ) ) ) )
3. ( element_of_set ( X1 , f1 ( X2 , X1 ) ) |~ element_of_set ( X1 , union_of_members (
    ,→ X2 ) ) )
4. ( elem ent_of _coll ection ( f1 ( X2 , X1 ) , X2 ) |~ element_of_set ( X1 ,
    ,→ union_of_members ( X2 ) ) )
5. ( element_of_set ( X1 , union_of_members ( X2 ) ) |~ element_of_set ( X1 , X3 ) |~
    ,→ eleme nt_of _colle ction ( X3 , X2 ) )
6. ( subset_sets ( X4 , X2 ) |~ elem ent_o f_coll ection ( X1 , subspace_topology ( X2 ,
    ,→ X3 , X4 ) ) )
7. ( element_of_set ( X1 , union_of_members ( X2 ) ) |~ element_of_set ( X1 ,
    ,→ union_of_members ( top_of_basis ( X2 ) ) ) )
8. ( elem ent_of _coll ection ( f10 ( X2 , X1 , X3 ) , X2 ) |~ elem ent_o f_coll ection ( X1 ,
    ,→ top_of_basis ( X2 ) ) |~ element_of_set ( X3 , X1 ) )
9. ( subset_sets ( X1 , X2 ) |~ elem ent_o f_coll ection ( f1 ( X3 , X4 ) , top_of_basis (
    ,→ subspace_topology ( X2 , X5 , X1 ) ) ) |~ element_of_set ( X4 ,
    ,→ union_of_members ( X3 ) ) )
10. ( element_of_set ( X1 , X3 ) |~ element_of_set ( X1 , in te rs e ct io n_ o f_ me m be rs (
    ,→ X2 ) ) |~ e lemen t_of_c ollec tion ( X3 , X2 ) )
11. ( subset_sets ( X1 , X2 ) |~ el ement_ of_col lecti on ( union_of_members (
    ,→ top_of_basis ( top_of_basis ( subspace_topology ( X2 , X3 , X1 ) ) ) ) , X4 ) |~
    ,→ element_of_set ( X5 , i nt e rs ec ti o n_ of _ me mb er s ( X4 ) ) )
12. ( element_of_set ( X1 , union_of_members ( X2 ) ) |~ el ement_ of_col lecti on (
    ,→ f10 ( X3 , X4 , X1 ) , X2 ) |~ elem ent_of _coll ection ( X4 , top_of_basis ( X3 ) ) |~
    ,→ element_of_set ( X1 , X4 ) )
13. ( element_of_set ( X1 , union_of_members ( X2 ) ) |~ el ement_ of_col lecti on ( f1
    ,→ ( X3 , X1 ) , top_of_basis ( X2 ) ) |~ element_of_set ( X1 , union_of_members (
    ,→ X3 ) ) )
14. ( element_of_set ( X1 , union_of_members ( X2 ) ) |~ el ement_ of_col lecti on ( X3
    ,→ , top_of_basis ( X2 ) ) |~ element_of_set ( X1 , X3 ) )
15. ( subset_sets ( X1 , X2 ) |~ el ement_ of_col lecti on ( X3 , top_of_basis (
    ,→ subspace_topology ( X2 , X4 , X1 ) ) ) |~ element_of_set ( X5 , X3 ) )
16. ( element_of_set ( X1 , union_of_members ( X2 ) ) |~ el ement_ of_col lecti on (
    ,→ union_of_members ( top_of_basis ( X2 ) ) , X3 ) |~ element_of_set ( X1 ,
    ,→ i nt er s ec ti o n_ of _m e mb er s ( X3 ) ) )

## Required Output Format
- List ** only ** the derivation steps .
- Each step must be on a new line .
- Use the exact format ‘ CHILD <- PARENT_1 , PARENT_2 ‘. Example : ‘5 <-
    ,→ 2 , 4 ‘.
- All clauses from the list must be used in the final structure .
- No explanations , comments , or extra text .

--- EXPECTED OUTPUT ---
11 <- 2 , 16
12 <- 1 , 5
13 <- 3 , 14


                                              13
    14 <- 8 , 12
    15 <- 6 , 8
    16 <- 7 , 10
    2 <- 4 , 9
    7 <- 4 , 13
    9 <- 3 , 15



    8.2     Visual Comparison of Proof Graph Reconstructions
    This section provides a detailed comparison of the proof graph reconstruction capabilities of various state-of-the-
    art models. The task is to reconstruct the dependency graph for the topology theorem on the logical consistency
    of subspace definitions, as detailed in Section 8. Each model was prompted with the full context and allowed a
    reasoning time of approximately 15 minutes to generate its solution.
    For each model, we present a single, structured visualization that overlays the model’s reconstruction onto the
    ground truth graph. The edges are color-coded for immediate analysis:

             • Green edges are correct dependencies, present in both the ground truth and the model’s output (True
               Positives).
             • Dashed gray edges are correct dependencies that the model failed to identify (False Negatives).
             • Red edges are incorrect dependencies that were hallucinated by the model (False Positives).

    8.2.1    Model: Gemini 2.5 pro(max thinking)

                                Proof Reconstruction Analysis: Gemini 2.5 pro(max thinking)
                                                                                         Correct Edge (True Positive)
                                                                                         Missing Edge (False Negative)
                                                                                         Incorrect Edge (False Positive)
                        1                            5




                                      12                            8                                     6




                                      14                            3                                    15




                                      13                            4                                     9




                                      7                             10                                    2




                                                                    16




                                                                               11




                      Figure 6: Proof graph reconstruction analysis for Gemini 2.5 pro.

    Qualitative Analysis: This model demonstrates strong performance, reconstructing most of the dependen-
    cies correctly. It makes a few specific errors, including hallucinating several dependencies for clause 12 and
    using an incorrect parent for clause 15. It also fails to reconstruct the derivation for clause 2.

    Model Output:
1   12 <- 4 , 9
2   7 <- 4 , 13
3   9 <- 3 , 15
4   11 <- 2 , 16



                                                            14
5   12   <-   1,   5
6   13   <-   3,   14
7   14   <-   8,   12
8   15   <-   6,   14
9   16   <-   7,   10



    8.2.2     Model: Claude-4.1-Opus(thinking)

                                  Proof Reconstruction Analysis: Claude-4.1-Opus(thinking)
                                                                                             Correct Edge (True Positive)
                                                                                             Missing Edge (False Negative)
                                                                                             Incorrect Edge (False Positive)
                          1                           5




                                      12                             8                                        6




                                      14                             3                                       15




                                      13                             4                                        9




                                       7                            10                                        2




                                                                    16




                                                                               11




                        Figure 7: Proof graph reconstruction analysis for Claude-4.1-Opus.

    Qualitative Analysis: The model correctly identifies a significant portion of the proof structure, particularly
    the main path leading to the conclusion. However, it hallucinates two incorrect dependencies for clause 15 and
    fails to derive several key intermediate clauses, notably clauses 14 and 2.
    Model Output:
1   7 <- 13 , 4
2   9 <- 15 , 3
3   11 <- 2 , 16
4   12 <- 5 , 1
5   13 <- 14 , 3
6   15 <- 2 , 5
7   16 <- 10 , 7




                                                            15
    8.2.3    Model: Deepseek V3.1

                                         Proof Reconstruction Analysis: Deepseek V3.1
                                                                                             Correct Edge (True Positive)
                                                                                             Missing Edge (False Negative)
                                                                                             Incorrect Edge (False Positive)
                         1                              5




                                        12                             8                                      6




                                        14                             3                                     15




                                        13                             4                                      9




                                        7                              10                                     2




                                                                       16




                                                                                   11




                       Figure 8: Proof graph reconstruction analysis for Deepseek V3.1.

    Qualitative Analysis: This model produces a highly precise but incomplete graph. Every dependency it
    identifies is correct (high precision), but it fails to reconstruct a large portion of the proof, leaving several clauses
    (9, 13, 14, 15) without inferred parents, indicating a significant failure in recall.
    Model Output:
1   2 <- 9 ,4
2   7 <- 13 ,4
3   11 <- 16 ,2
4   12 <- 5 ,1
5   16 <- 10 ,7




                                                               16
    8.2.4   Model: Gpt-5(high)

                                         Proof Reconstruction Analysis: Gpt-5(high)
                                                                                      Correct Edge (True Positive)
                                                                                      Missing Edge (False Negative)
                                                                                      Incorrect Edge (False Positive)
                       1                              5




                                    12                               8                                 6




                                    14                               3                                15




                                    13                               4                                 9




                                     7                              10                                 2




                                                                    16




                                                                                11




                       Figure 9: Proof graph reconstruction analysis for Gpt-5(high).

    Qualitative Analysis: The model provides a perfect reconstruction of the proof graph, identifying all 18
    dependencies correctly without any missing or hallucinated edges. The generated structure is identical to the
    ground truth, demonstrating a complete and accurate understanding of the proof’s logical flow.
    Model Output:
1   12 <- 5 , 1
2   15 <- 6 , 8
3   14 <- 12 , 8
4   9 <- 15 , 3
5   13 <- 14 , 3
6   2 <- 9 , 4
7   7 <- 13 , 4
8   16 <- 10 , 7
9   11 <- 2 , 16




                                                            17
