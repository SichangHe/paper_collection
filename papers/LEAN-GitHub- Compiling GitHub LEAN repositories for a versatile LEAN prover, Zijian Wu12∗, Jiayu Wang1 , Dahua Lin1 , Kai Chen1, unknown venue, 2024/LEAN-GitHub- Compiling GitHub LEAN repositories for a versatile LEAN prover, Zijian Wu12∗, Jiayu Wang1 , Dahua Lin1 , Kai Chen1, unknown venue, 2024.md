                                         LEAN-GitHub: Compiling GitHub LEAN repositories
                                                   for a versatile LEAN prover


                                                                      Zijian Wu12∗, Jiayu Wang1 , Dahua Lin1 , Kai Chen1
                                                              1
                                                                  Shanghai AI Laboratory, 2 The Chinese University of Hong Kong
                                                                                   wuzijian@pjlab.org.cn
arXiv:2407.17227v1 [cs.AI] 24 Jul 2024




                                                                                           Abstract
                                                      Recently, large language models have presented promising results in aiding formal
                                                      mathematical reasoning. However, their performance is restricted due to the
                                                      scarcity of formal theorem-proving data, which requires additional effort to be
                                                      extracted from raw formal language corpora. Meanwhile, a significant amount
                                                      of human-written formal language corpora remains underutilized. To address
                                                      this issue, we propose LEAN-GitHub, a dataset consisting of large-scale formal
                                                      data extracted from almost all Lean 4 repositories on GitHub. After fine-tuning
                                                      InternLM-math-plus on this dataset, our model achieved accuracies of 48.8% with
                                                      a single pass and 54.5% with 64 passes on the Lean 4 miniF2F test, surpassing state-
                                                      of-the-art method at 52%. And it also achieves state-of-the-art on two other Lean 4
                                                      benchmarks (ProofNet and Putnam) targeting different fields/levels of math. These
                                                      results demonstrate that our proposed dataset is beneficial for formal reasoning
                                                      on a wide range of math topics. We open-source our model at https://GitHub.
                                                      com/InternLM/InternLM-Math and our data at https://huggingface.co/
                                                      datasets/InternLM/Lean-GitHub.


                                         1       Introduction
                                         Theorem proving stands as a fundamental objective in mathematics. To tackle the escalating intricacy
                                         of proofs and identify non-trivial flaws within them, formalized mathematical systems like Lean [6],
                                         Isabelle [19], and Coq [24] have been developed to furnish computer-verifiable proofs [2]. However,
                                         crafting formal proofs demands substantial human effort, posing challenges for further advancement
                                         and underscoring the necessity for automated theorem proving [18]. Recently, large language models
                                         (LLMs) [1, 4, 34, 21, 23, 9, 26, 36] have shown promising results in resolving high-school level
                                         math problems through interactions with formalized proof assistants. Nevertheless, their performance
                                         remains unsatisfactory, primarily due to data scarcity.
                                         Formal languages necessitate significant expertise and effort and are utilized by a relatively small
                                         number of mathematicians, leading to a shortage of formal language corpora. In addition, unlike
                                         conventional programming languages such as Python or Java, formal proof languages contain inter-
                                         mediate information not directly visible in their raw code, e.g. proof trees comprising intermediate
                                         states between proof steps, making raw language corpora unsuitable for training. This scarcity of
                                         well-crafted human-written formal language data persists while many valuable human-written corpora
                                         remain underutilized. Although auto-formalization [30, 35] enables the synthesis of more aligned
                                         data for training, the quality and diversity of their data remain constrained and thus cannot substitute
                                         for human-crafted data.
                                         To address this challenge, we propose LEAN-GitHub in this paper: a large-scale Lean dataset
                                         that leverages open-source Lean repositories on GitHub, serving as a crucial complement to the
                                             ∗
                                                 Work done during internships at Shanghai AI Laboratory.


                                         Preprint. Under review.
well-utilized Mathlib [17, 34] dataset. We develop a scalable pipeline, shown in Fig. 2, to boost
the extraction efficiency and parallelness, and managed to exploit precious data from Lean corpus
that were not compiled and extracted before. We also provide a solution to the state duplication
problem common in tree proof search methods. To showcase the efficacy of our dataset, we train
InternLM2-StepProver with our dataset included. Quantitative results show that fine-tuning on our
dataset enhances formal reasoning abilities in Lean 4 across various formal benchmarks, indicating
our proposed dataset is beneficial for formal reasoning on versatile math topics.
In summary, our paper makes the following contributions:
         • We publicly release LEAN-GitHub, a dataset consisting of large-scale formal data extracted
           from open Lean 4 repositories on GitHub, including 28,597 theorems and 218,866 tactics,
           fostering further research and development in automated theorem proving. Our dataset could
           be found at https://huggingface.co/datasets/InternLM/Lean-GitHub.
         • Our model InternLM2-StepProver , a 7B model trained on this dataset, achieves state-of-the-
           art performance on benchmarks targeting different fields/levels of math. The InternLM2-
           StepProver has reported accuracies of 48.8% within a single pass and 54.5% with 64 passes
           on the Lean 4 miniF2F [38] test, surpassing Deepseek-Prover [30] at 52%; an 18.1% Pass@1
           on ProofNet [3]; and has solved 5 out of 640 Putnam [25] problems. In addition, our model
           solved 3 IMO problems in the miniF2F dataset, see Fig. 1 for an example.2

     Case: IMO 1983 P6
     Natural Language problem: Let a, b and c be the lengths of
     the sides of a triangle. Prove that
                                                                                               237
              a2 b(a − b) + b2 c(b − c) + c2 a(c − a) ≥ 0.                                 Lean 4 Repos
                                                                                              Pre-Filter

                                                                                           147 Repos
     theorem imo_1983_p6 (a b c : R) (h0 : 0 < a ∧ 0 <
         b ∧ 0 < c) (h1 : c < a + b) (h2 : b < a + c)                                Build Import Graph
         (h3 : a < b+c) : 0 ≤ a^2 * b * (a-b) + b ^ 2 *
          c * (b - c) + c ^ 2 * a * (c - a) :=                                             10K+ Files
     by
         ring_nf                                                                      Parallel Compile
         have h4 : 0 < a+b+c := by linarith
         simp only [add_assoc]                                                        8369 Compiled
         have h5 : 0 ≤ (a-b)^2 * (a+b-c) := by
         nlinarith                                                                         Extract AST
         have h6 : 0 ≤ (a-c)^2 * (a+c-b) := by
         nlinarith                                                                     6352 AST trees
         have h7 : 0 ≤ (b-c)^2 * (b+c-a) := by
                                                                                       Extract Tactics
         nlinarith
         nlinarith [h0 .1, h0 .2.1, h0 .2.2, h1 , h2 , h3 ,
         h4 , h5 , h6 , h7 ]
                                                                                      Lean-GitHub
                                                                                     28K         219K      0.131B
                                                                                   Theorems     Tactics    Tokens



    Figure 1: An IMO problem solved by InternLM2-StepProver .                  Figure 2: The pipeline
                                                                               for constructing LEAN-
                                                                               GitHub.


2       Related works
The development of modern proof assistants, including Coq [24], Isabelle [19], and Lean [6], has
expanded the expressive capabilities of formal systems beyond first-order logic, thereby stimulating
    2
     The original problem includes determining when equality occurs. It is omitted in our formalization due to
the restriction of the formal system.


                                                      2
heightened interest in automated theorem proving. The recent integration of large language models [1,
4, 22, 30, 36] has further advanced the development of tools and datasets.
Automatic Theorem Proving Earlier works in ATP use traditional methods, such as KNN [8] or
GNN [32]. Some [13, 5, 28] exploit reinforcement learning techniques to improve performance.
Recently, more are taking advantage of the deep transformer-based methods that treat theorems
as plain texts. Many learning-based theorem proving, such as GPT-f [21], PACT [9], Llemma [4],
COPRA [23], ReProver [34] and Lean-STaR [16], instructs a language model on (proof state, next-
tactic) pairs, then proves theorems by tree search. Some [32] tries generating tactics on the granularity
of abstract syntax trees. An alternative approach involves harnessing LLMs to autonomously generate
the entire proof either independently or based on human-provided proofs [30, 7, 37, 12, 31]. Some
other methods also explores the possibility of incorporating informal proofs into formal proofs [12,
29, 16, 26]. We follow the GPT-f framework and trains our model on the granularity of tactics.
Data Extraction for Lean Corpus Following human-behavior in interacting with proof assistants,
it is crucial for the automated theorem provers to see intermediate states invisible in the code but
visible to human at runtime. Therefore, data extraction tools are critical drivers of ATP: Coq has
GamePad [11] and CoqGym [33]; Isabelle has IsarStep [15], and Lean has LeanStep [9], lean-
gym [20] (not compatible with Lean 4) and LeanDojo [34]. We focus on extraction tools for Lean4.
However, prior Lean 4 tools involve significant overhead in extraction as it is designed for a single
project, therefore not directly suitable for massive extraction on multiple projects.


3     The GitHub-Lean dataset

There are numerous Lean repositories on GitHub, which contains scarce human-written theorems
and proofs. However, the raw Lean code is unsuitable for direct training, as it has crucial runtime
information that humans can access when interact with Lean environments unrevealed. Examples
include the intermediate states and targets between each proof steps, and hints provided by some
tactics. Though there has been works on extracting these information, they are restricted on Mathlib
4 [34, 17], Lean’s centralized formal math library. Meanwhile, hundreds of Lean repositories covering
diverse topics exists on GitHub without getting exploited and extracted.
We form a dataset for theorem proving in Lean 4, named LEAN-GitHub, built upon 147 Lean 4
repositories available on the web. The dataset is one of the largest theorem proving datasets in Lean
4 formal mathematics, consisting of 28,597 theorems with formal proofs and 218,866 tactics from
2133 files. The dataset has 0.138B tokens. We propose that, training on the dataset improves model
performance on theorem proving in various mathematical topics.

3.1   Dataset Construction

In this section, we will detailedly describe how we construct the LEAN-GitHub dataset.
Selection of the repositories. After conducting an exhaustive search on GitHub, we identified a
total of 237 Lean 4 repositories (GitHub does not differentiate between Lean 3 and Lean 4) which
may contain compilable theorems. By filtering for keywords such as "theorem" and "lemma", we
estimated that there are approximately 48,091 theorems across these repositories. However, it is
important to note that the presence of a keyword does not guarantee the existence of a theorem with a
proof written in the form of tactics. The main obstacles include: a) some repositories cannot compile,
either due to improper construction of the project or incorrect Lean files included; b) dependencies
on other repositories that are not available online; c) repositories written in older versions of Lean
with deprecated features that cannot be migrated to newer versions; and d) proofs of theorems not
constructed using tactics. We discarded 90 repositories written in deprecated Lean 4 versions.
Among the remaining repositories, only 61 out of 147 could be compiled as valid Lean 4 projects with-
out requiring modifications. The remaining repositories required extra efforts to compile successfully.
A small fraction of projects relies on non-official releases of Lean 4, others contains a significant
number of isolated files. We develop automated scripts to try heuristically finding the closest official
releases for the former case. Solution to the latter case is described in the next paragraph.
Source Code Compilation. We opted not to use the Lake [6] tool provided by the Lean 4 standard
library, but instead called the underlying leanc compiler directly to compile the source code. This


                                                   3
Figure 3: Word Cloud for the theorem names                              Figure 4: Top 30 repositories with most theorems
in LEAN-GitHub.                                                         extracted.

approach offers two advantages. First, many of the Lean repositories collected are not compliant
Lean projects and cannot be compiled. This is because Lean 4 can function as both a compiled
language and a script language. Mathematicians often tend to write isolated files within an empty
Lean project, which cannot be compiled by Lake. Second, Lake would fail to build the project if
any of its building targets failed, causing the content of the whole project to be discarded. We also
observed a performance bottleneck in Lake’s concurrent primitives. To address this issue, we first
extended Lake’s import graph on file dependencies. We modified Lake to expose this information.
Then we augmented it with information of isolated files and rebuild our global import graph. With
this dependency information, we could replace Lake with a custom compiling script that directly
calls the underlying leanc compiler with increased parallelness.
Extraction Details. We develop our extraction utilities based on LeanDojo [34]. Tools such as
LeanDojo [34] and LeanStep [9] typically require the entire project to be compiled before data
extraction. We argue that this restriction is unnecessary and implemented data extraction for isolated
files. Observing some bottlenecks introduced by LeanDojo’s reliance on network connection and
its design choice that putting data extraction and interaction with Lean together, which brings many
computational redundancies, we restructured the implementation with an increased parallelism. Out
of 8639 Lean source files, 6352 files and 42K theorems were successfully extracted, with 2133 files
and 28K theorems containing valid tactic information.

3.2   Dataset Statistics

Fig. 3 shows the word cloud of the set of theorem names of our dataset. The word cloud highlights
the most frequently occurring keywords in the theorem names, with "Logic", "FirstOrder", "Matroid",
and "Arith(mezation)" being the most prominent, indicating that the dataset contains mathematics
from various fields. Fig. 4 displays the top 30 repositories with the most theorems extracted.
The distribution further shows the diverse mathematical topics in the data, including cutting-edge
mathematical fields, data structures, as well as Olympiad-level problems.

 Dataset               Lean-Workbook [35]   Deepseek-Prover [30]   miniF2F-curriculum [20]   LeanDojo-Mathlib [34]   LEAN-GitHub (ours)
 Open-sourced                   ✓                    ✕                       ✓                        ✓                      ✓
 Source                     Synthetic            Synthetic              Human-written            Human-written          Human-written
 Intermediate States            ✕                    ✕                       ✕                        ✓                      ✓
 Theorems                     57K                  870K                     327                     60K                    28K
 Tokens                      0.029B               3.108B                    1.5K                   0.138B                 0.131B
 Level                    Undergraduate        Undergraduate             High-school               Diverse                Diverse
Table 1: Comparison of dataset statistics among Lean 4 formal reasoning datasets: Lean-Workbook,
Deepseek-Prover, miniF2F-curriculum, LeanDojo-Mathlib, and LEAN-GitHub (ours).


To estimate the quality our dataset, we provide several quantitative measures and compare them with
recent and similar existing datasets, namely Lean-Workbook, Deepseek-Prover, miniF2F-curriculum
and LeanDojo-Mathlib (see Tab. 1).
Lean-Workbook and Deepseek-Prover are synthetic datasets whose topics are largely restricted to
high-school level (some in the undergraduate level), and crucial intermediate steps are not available.
Besides, since they rely on present methods to generate solutions, their solution length and quality
are also restricted. MiniF2F-curriculum, designed for expert iteration [20] has a small size of 327


                                                                    4
### Input
DECL MyNat.mul_pow
GOAL a b n : N
⊢ (a * b) ^ n = a ^ n * b ^ n
### Output
PROOFSTEP induction n with t Ht

                 Figure 5: Examples of (input, output) pairs of our training prompt.


examples, limiting its versatility and robustness. LeanDojo-Mathlib is one of the largest datasets
at the granularity of tactics, extracted from Mathlib 4, the standard mathematics library for Lean
4. It focuses mainly on describing specific mathematical theories rather than the topic of problem-
solving. In contrast, our dataset, which contains versatile fields, levels, and tastes of math proofs,
is comparably large and covers a broad spectrum of complexities. Overall, our dataset pushes the
boundaries of utilizing precious human-written corpora and is comparable to prior efforts.

4     Experiments
We develop the InternLM2-StepProver model that utilizes the LEAN-GitHub. InternLM2-StepProver
is built upon InternLM-math-plus-7B [36] model, which is a decoder-only transformer that is
continued pre-trained on a corpus comprising 200B informal and formal math-related tokens. We
then conduct extensive experiments on various Lean 4 datasets to test the effectiveness of InternLM2-
StepProver on formal reasoning. We also conduct ablation studies and case studies to further validate
the effectiveness of LEAN-GitHub.

4.1     Experiment settings

4.1.1    Model and Training
Our training set mainly consists of three parts: the LEAN-GitHub, Lean’s Mathlib (via the LeanDojo
dataset), which is the common practive in training formal reasoning models in Lean, and other
private synthetic theorem, which mainly comes from the autoformoalization effort of Lean Workbook.
Several other models were trained with different training set settings for ablation. We follow the
proofstep objective used by GPT-f [21], which generating a PROOFSTEP (a Lean tactic) given a GOAL
(current Lean tactic state) and the current DECLARATION (the Lean theorem name to be proved): DECL
<DECLARATION> \nGOAL <GOAL> \nPROOFSTEP <PROOFSTEP>\n, as depicted in Fig. 5.
We used a global batch size of 512 and a learning rate of 10−5 . We fine-tuned for 2 epoch to obtain
the SFT model. For the learning rate, we used a warm-up in the first 3% steps, followed by a cosine
schedule decaying to zero. The whole fine-tuning process took around 6 hours on 32 A100 GPUs.

4.1.2    Evaluation settings
We utilized a standard methodology that iteratively performs a best-first search to generate tactics and
validate intermediate proof steps within a formal proof until the proof is either finalized or resources
are exhausted. During each generation step, a state Si is expanded by generating S tactic candidates
for it, with a maximum of K expansions allowed in a single iteration. In this context, we select
S = 32 and K = 100.
State De-duplication One of the most prevalent issues in the best-first search process is the highly
duplicated states. This arises from the foundational nature of the Lean language, which is rooted in
dependent type theory. In Lean, every proposition can be viewed as a valid type, and demonstrating
that proposition is akin to discovering or constructing an element of that type, essentially proving that
the proposition is inhabited. Moreover, Lean considers two proofs of a proposition to be definitionally
equivalent. Consequently, there is no inherent mechanism to distinguish if two (potentially partial)
proofs lead to the same intermediate states. Given that numerous Lean tactics, such as intro
and have, involve introducing new hypotheses with customized names, it is common for multiple
intermediate states with essentially identical hypotheses but distinct names to emerge during the
search process, as depicted in Fig. 6. This issue becomes more pronounced in extensive proof


                                                   5
searches, where we have observed that over 50% of intermediate states are duplicates. Failure to
address this issue could result in significant computational inefficiencies.
To minimize computational wastage on dupli-
cated intermediate states and improve the ef-
ficiency of the proof search process, we ex-
                                                           Possible                                            Local context
ploited Lean’s runtime meta-programming fa-                proof tree(s)                                       ⊢Goal
cilities to provide additional information for de-
duplication. We modified Lean so that for each                            ⊢ ∀ (a b c : ℕ), a = b → a = c → c = b
intermediate state (internally stored as meta-
                                                                                          Tactic
variables and local declarations), their hypothe-                     intro a b c                          intro x y z
ses are renamed based on their internal storage
                                                           abc:ℕ                                   xyz :ℕ
order. So that states with same hypotheses and             ⊢a = b → a = c → c = b
                                                                                            ≠
                                                                                                   ⊢x=y→x=z→z=y
goals could be identified, as shown in Fig. 6.                Rename free variables                   Rename free variables

                                                           f1 f2 f3 : ℕ                            f 1 f 2 f3 : ℕ
                                                                                            =
                                                           ⊢f1 = f2 → f1 = f3 → f3 = f2            ⊢f1 = f2 → f1 = f3 → f3 = f2
4.2   Main Results

After testing with Lean 4 benchmarks aiming
at different levels (high-school or undergradu-
ate), difficulties (ordinary exercises or Olympiad   Figure 6: De-duplication of intermediate proof
problems), and taste (problem-solving vs. con-       states in tree search. Different tactics may result in
structing a math system like in textbooks), we       states that are essentially the same. Renaming free
conclude that InternLM2-StepProver exhibits          variables and hypotheses based on their internal
versatile formal reasoning abilities compared to     storage order in Lean’s kernel provides a unified
prior works by achieving state-of-the-art perfor-    representation, helping identifying these states.
mance, proving the effectiveness of the diversity
of LEAN-GitHub.
Results on miniF2F. We first test the Lean 4
formal reasoning ability on miniF2F-Test and
Validation dataset. MiniF2F [38] is a standard testing dataset for evaluating the performance of
formal provers, containing 244 validation and 244 test problems, all stated in Lean. The range of
problems varies from high-school competition questions to undergraduate-level theorem proofs, e.g.
problems sampled from the MATH dataset [10], high-school mathematical competitions (including
AMC, AIME, and IMO) and some other manually crafted problems at the same difficulty. We use the
version of miniF2F in Lean 4 released by the LeanDojo [34] project, with adaptations to Lean 4.7.0.
We present the main experimental results in Tab. 2. From the table, we can observe that InternLM2-
StepProver achieves a cumulative accuracy rate of 63.9% on miniF2F-Valid and 54.5% on miniF2F-
Test, suppressing all the baselines, including DeepSeek-Prover [30] which scores 60.2% and 52.0%,
respectively. Specifically, InternLM2-StepProver significantly outperforms all prior tree-search
methods, including Hypertree Proof Search, which achieves only 58.6% on miniF2F-valid and 41.0%
on miniF2F-test, demonstrating that the potential of tree search methods still remains to be fully
explored and such method is comparable to generating whole proofs.
Results on ProofNet. ProofNet [3] is a benchmark for testing the formal reasoning ability on
undergraduate-level mathematics. It comprises 371 formal problems which are sourced from popular
undergraduate pure mathematics textbooks and cover topics such as real and complex analysis, linear
algebra, abstract algebra, and topology. We list results in Table 3. Outperforming the benchmark’s
prior leader, ReProver [34], which had a Pass@1 rate of 13.8%, our model, InternLM2-StepProver ,
achieves a significantly higher Pass@1 rate of 18.1%(Fig. 3). We have also discovered 24 proofs in
ProofNet that currently do not have Lean proofs.
Results on PutnamBench. PutnamBench [25] is a benchmark comprising 640 theorems sourced
from the Putnam Mathematical Competition, a renowned math competition in North America. These
theorems are formalized in Lean 4, Isabelle, and partially in Coq. The benchmark is designed to
test models’ formal reasoning abilities in solving problems at a premier undergraduate mathematics
level and is meticulously curated to prevent test-set leakage. We list results in Table 3. Restricted
to Lean 4 formalization, GPT-4, and COPRA [23] each solved one of the 640 problems, while
ReProver failed to solve any. To our knowledge, the most effective method has been DSP [12], which
operates in Isabelle and solved 4 problems with pass@10. As shown in Fig. 3, InternLM2-StepProver


                                                     6
outperformed these results by solving 5 problems in a single pass without informal sketches and
identified a solution for Putnam 1988 B2, a problem not yet reported to be solved by any ITP. The
generated proof is included in Tab. A.

                 Table 2: Comparing with state-of-the-arts on the miniF2F dataset.

        Method                           Model size         Pass         miniF2F-valid   miniF2F-test
        Whole-Proof Generation Methods
        GPT-4-turbo 0409[1]                  -                 64             25.4%        23.0%
                                                                1                -         30.0%
                                                               64                -         46.3%
                                                              128                -         46.3%
        DeepSeek-Prover [30]                7B
                                                             8192                -         48.8%
                                                            65536                -         50.0%
                                                          cumulative          60.2%        52.0%
        TheoremLlama [26]                    -            cumulative          36.5%        33.6%
        Tree Search Methods
        COPRA (GPT-3.5) [23]                 -                 1                 -          9.0%
        COPRA (GPT-4) [23]                   -                 1                 -         26.6%
        DSP(Isabelle) [12]                 540B              100              42.6%        38.9%
                                                               1              23.9%        24.6%
        Proof Artifact Co-Training [9]     837M
                                                               8              29.3%        29.2%
        ReProver [34]                      229M                1                 -         25.0%
        Llemma [4]                          7B                 1              26.2%        26.2%
        Llemma [4]                          34B                1              27.9%        25.8%
                                                               1              33.6%        29.6%
        Curriculum Learning [20]           837M                8              41.2%        34.5%
                                                              64              47.3%        36.6%
                                                          cumulative          58.6%           -
        Hypertree Proof Search [14]        600M
                                                              64                 -         41.0%
        Lean-STaR [16]                      7B                64                 -         46.3%
        InternLM2-Math [36]                 7B                 1              29.9%        30.3%
        InternLM2-Math-Plus [36]            7B                 1                 -         43.4%
                                                              1               59.8%        48.8%
        InternLM2-StepProver                7B
                                                             64               63.9%        54.5%



      Table 3: Comparing with state-of-the-arts on the ProofNet [3] and Putnam [25] dataset.

                          Method                      Model size       Pass    result
                          ProofNet [3] benchmark
                          ReProver [34]                   229M          1     13.8%
                          InternLM2-StepProver             7B           1     18.1%
                          Putnam [25] benchmark
                          GPT-4 [1]                         -          10      1/640
                          COPRA (GPT-4) [23]                -          10      1/640
                          DSP(Isabelle) [12]              540B         10      4/640
                          ReProver [34]                   229M          1      0/640
                          InternLM2-StepProver             7B           1      5/640



4.3   Ablation Studies

Data source ablation As described in Sec. 4.1.1, InternLM2-StepProver is trained on LEAN-
GitHub, along with synthetic data including rule-based generated equations and inequalities and Lean-
Workbook [35], and human-written data extracted from Mathlib. To demonstrate the effectiveness
of the LEAN-GitHub dataset, we conducted a comparative analysis among various combinations of


                                                      7
                                     Accuracy Rates Over Pass                                         65
                                                                                                                    Accuracy Rates Over Pass
                       55
                       50                                                                             60

  Accuracy Rates (%)




                                                                                 Accuracy Rates (%)
                       45                                                                             55

                       40                                                                             50
                                                          Mathlib+SYN+LG                                                                 Mathlib+SYN+LG
                       35                                 Mathlib+SYN                                 45                                 Mathlib+SYN
                                                          Mathlib+LG                                                                     Mathlib+LG
                       30                                 Mathlib                                     40                                 Mathlib
                                                          DeepSeek-Prover                                                                DeepSeek-Prover
                                                                                                      35
                            0   10     20     30    40      50      60                                     0   10     20      30    40     50      60
                                               Pass                                                                            Pass

Figure 7: Improvement in pass rates for miniF2F-                                Figure 8: Improvement in pass rates for miniF2F-
test at pass@64 in models trained with differ-                                  valid at pass@64 in models trained with different
ent data sources, where LG stands for LEAN-                                     data sources.
GitHub and SYN stands for synthetic data.

training data, as shown in Tab. 4 and 5. The results indicate that models trained with data extracted
from GitHub significantly outperform those trained solely with Mathlib data and/or synthetic data.

Table 4: Improvement in pass rates for miniF2F at pass@1 in models trained on formal proofs, with
different data sources.
                            Model                                                   #Tokens                    miniF2F-valid      miniF2F-test
                            Mathlib                                                   0.131B                        44.3%              37.3%
                            Mathlib + LEAN-GitHub                                     0.269B                        44.3%              41.0%
                            Mathlib + synthetic theorems                              1.286B                        58.2%              46.7%
                            Mathlib + LEAN-GitHub + synthetic theorems                1.424B                        59.8%              48.8%




Table 5: Improvement in pass rates for ProofNet at pass@1 in models trained on formal proofs, with
different data sources.
                                      Model                                                                    #Tokens      ProofNet
                                      Mathlib                                                                  0.131B        15.1%
                                      Mathlib + LEAN-GitHub                                                    0.269B        16.2%
                                      Mathlib + synthetic theorems                                             1.286B        17.0%
                                      Mathlib + LEAN-GitHub + synthetic theorems                               1.424B        18.1%


The effectiveness of multiple inferences. We then focused on how LEAN-GitHub affects formal
reasoning performance when scaling evaluation (i.e. with more pass time). Since the formalization
system will tell us whether a problem is solved, there is no reason to restrict the model to a single pass
when pursuing maximum performance. By extending the evaluation budget until the performance
improvement is marginal, as shown in Fig. 7 and 8, we observe that LEAN-GitHub improves the
models’ maximum performance.
We proceeded with the evaluation of each model using temperatures 0.7 and 1.0, each with 32
independent inferences, instead of beam search which we had chosen for the Pass@1 evaluation.
Therefore, the initial accuracy rates of the first round may be lower than in the Pass@1 evaluation.
InternLM2-StepProver achieved an accumulated pass rate of 54.5% for miniF2F-test and 63.9% for
miniF2F-valid, surpassing the baseline trained without LEAN-GitHub, which had pass rates of 53.2%
and 62.3%, respectively. The same trend was observed for models trained solely on Mathlib and
on Mathlib+LEAN-GitHub. We have also discovered a proof for IMO 1983 P6, which, to our best
knowledge, has not been proved in Lean 4 before (also not be solved in compfiles3 ). Examples of
proved theorems can be found in Sec. A.

           3
                  https://github.com/dwrensha/compfiles/blob/main/Compfiles/Imo1983P6.lean


                                                                            8
5   Conclusion
In this paper, we introduce LEAN-GitHub—a dataset comprising a large-scale collection of formal
data extracted from open Lean 4 repositories on GitHub, which includes 28,597 theorems and 218,866
tactics. We then train InternLM2-StepProver using this dataset, which is the state-of-the-art model
performance on Lean 4 formal reasoning. We also train various models with LEAN-GitHub to
evaluate the formal reasoning performance that can be achieved by training on our dataset. Notably,
we find that models trained on LEAN-GitHub exhibit performance improvements in formal reasoning
across various fields and difficulty levels, demonstrating that a well-extracted, diverse dataset can
enhance model performance on a range of reasoning tasks. We hope that by opening LEAN-GitHub,
we can assist the community in better exploiting the under-utilized information in raw corpora and in
improving mathematical reasoning capabilities.

References
 [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni
     Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4
     technical report. arXiv preprint arXiv:2303.08774, 2023.

 [2] Jeremy Avigad. Mathematics and the formal turn, 2023.

 [3] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir Radev,
     and Jeremy Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level
     mathematics, 2023.

 [4] Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen McAleer,
     Albert Q Jiang, Jia Deng, Stella Biderman, and Sean Welleck. Llemma: An open language
     model for mathematics. arXiv preprint arXiv:2310.10631, 2023.

 [5] Maxwell Crouse, Ibrahim Abdelaziz, Bassem Makni, Spencer Whitehead, Cristina Cornelio,
     Pavan Kapanipathi, Kavitha Srinivas, Veronika Thost, Michael Witbrock, and Achille Fokoue.
     A deep reinforcement learning approach to first-order logic theorem proving. In Proceedings of
     the AAAI Conference on Artificial Intelligence, volume 35, pages 6279–6287, 2021.

 [6] Leonardo De Moura, Soonho Kong, Jeremy Avigad, Floris Van Doorn, and Jakob von Raumer.
     The lean theorem prover (system description). In Automated Deduction-CADE-25: 25th Inter-
     national Conference on Automated Deduction, Berlin, Germany, August 1-7, 2015, Proceedings
     25, pages 378–388. Springer, 2015.

 [7] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. Baldur: Whole-proof generation
     and repair with large language models, 2023.

 [8] Thibault Gauthier, C. Kaliszyk, Josef Urban, Ramana Kumar, and Michael Norrish. Tactictoe:
     Learning to prove with tactics. Journal of Automated Reasoning, 65:257 – 286, 2018.

 [9] Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W Ayers, and Stanislas Polu. Proof artifact
     co-training for theorem proving with language models. arXiv preprint arXiv:2102.06203, 2021.

[10] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn
     Song, and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset,
     2021.

[11] Daniel Huang, Prafulla Dhariwal, Dawn Song, and Ilya Sutskever. Gamepad: A learning
     environment for theorem proving, 2018.

[12] Albert Q Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée
     Lacroix, Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding formal theorem
     provers with informal proofs. arXiv preprint arXiv:2210.12283, 2022.

[13] Cezary Kaliszyk, Josef Urban, Henryk Michalewski, and Miroslav Olšák. Reinforcement
     learning of theorem proving. Advances in Neural Information Processing Systems, 31, 2018.


                                                 9
[14] Guillaume Lample, Timothee Lacroix, Marie-Anne Lachaux, Aurelien Rodriguez, Amaury
     Hayat, Thibaut Lavril, Gabriel Ebner, and Xavier Martinet. Hypertree proof search for neural
     theorem proving. Advances in neural information processing systems, 35:26337–26349, 2022.
[15] Wenda Li, Lei Yu, Yuhuai Wu, and Lawrence C. Paulson. Isarstep: a benchmark for high-level
     mathematical reasoning, 2021.
[16] Haohan Lin, Zhiqing Sun, Yiming Yang, and Sean Welleck. Lean-star: Learning to interleave
     thinking and proving, 2024.
[17] The mathlib Community. The lean mathematical library. In Proceedings of the 9th ACM
     SIGPLAN International Conference on Certified Programs and Proofs, CPP 2020, page 367–381,
     New York, NY, USA, 2020. Association for Computing Machinery.
[18] A. Newell and H. Simon. The logic theory machine–a complex information processing system.
     IRE Transactions on Information Theory, 2(3):61–79, 1956.
[19] Lawrence C. Paulson. Isabelle a Generic Theorem Prover. Springer Verlag, 1994.
[20] Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya
     Sutskever. Formal mathematics statement curriculum learning. arXiv preprint arXiv:2202.01344,
     2022.
[21] Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving.
     arXiv preprint arXiv:2009.03393, 2020.
[22] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Mingchuan Zhang, YK Li,
     Y Wu, and Daya Guo. Deepseekmath: Pushing the limits of mathematical reasoning in open
     language models. arXiv preprint arXiv:2402.03300, 2024.
[23] Amitayush Thakur, Yeming Wen, and Swarat Chaudhuri. A language-agent approach to formal
     theorem-proving. arXiv preprint arXiv:2310.04353, 2023.
[24] The Coq Development Team. Coq, 2017.
[25] George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings,
     Amitayush Thakur, and Swarat Chaudhuri. Putnambench: Evaluating neural theorem-provers
     on the putnam mathematical competition, 2024.
[26] Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe Diao, Renjie Pi, and Tong Zhang.
     Theoremllama: Transforming general-purpose llms into lean4 experts, 2024.
[27] Jason Wei, Maarten Bosma, Vincent Y. Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan
     Du, Andrew M. Dai, and Quoc V. Le. Finetuned language models are zero-shot learners, 2022.
[28] Minchao Wu, Michael Norrish, Christian Walder, and Amir Dezfouli. Tacticzero: Learning to
     prove theorems from scratch with deep reinforcement learning. Advances in Neural Information
     Processing Systems, 34:9330–9342, 2021.
[29] Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus Rabe, Charles Staats, Mateja Jamnik,
     and Christian Szegedy. Autoformalization with large language models. Advances in Neural
     Information Processing Systems, 35:32353–32368, 2022.
[30] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan,
     Wenda Li, and Xiaodan Liang. Deepseek-prover: Advancing theorem proving in llms through
     large-scale synthetic data, 2024.
[31] Huajian Xin, Haiming Wang, Chuanyang Zheng, Lin Li, Zhengying Liu, Qingxing Cao, Yinya
     Huang, Jing Xiong, Han Shi, Enze Xie, et al. Lego-prover: Neural theorem proving with
     growing libraries. arXiv preprint arXiv:2310.00656, 2023.
[32] Kaiyu Yang and Jia Deng. Learning to prove theorems via interacting with proof assistants.
     ArXiv, abs/1905.09381, 2019.


                                                10
[33] Kaiyu Yang and Jia Deng. Learning to prove theorems via interacting with proof assistants,
     2019.
[34] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
     Godil, Ryan J Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with
     retrieval-augmented language models. Advances in Neural Information Processing Systems, 36,
     2024.
[35] Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang, Dahua Lin, and Kai Chen. Lean workbook:
     A large-scale lean problem set formalized from natural language math problems, 2024.
[36] Huaiyuan Ying, Shuo Zhang, Linyang Li, Zhejian Zhou, Yunfan Shao, Zhaoye Fei, Yichuan
     Ma, Jiawei Hong, Kuikun Liu, Ziyi Wang, Yudong Wang, Zijian Wu, Shuaibin Li, Fengzhe
     Zhou, Hongwei Liu, Songyang Zhang, Wenwei Zhang, Hang Yan, Xipeng Qiu, Jiayu Wang,
     Kai Chen, and Dahua Lin. Internlm-math: Open math large language models toward verifiable
     reasoning, 2024.
[37] Xueliang Zhao, Wenda Li, and Lingpeng Kong. Decomposing the enigma: Subgoal-based
     demonstration learning for formal theorem proving. arXiv preprint arXiv:2305.16366, 2023.
[38] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for
     formal olympiad-level mathematics. arXiv preprint arXiv:2109.00110, 2021.




                                              11
A    Case study

This section presents case studies to demonstrate the performance of our methods.

    Case 1: Binomial Coefficients
    Natural Language problem: Show that for positive integers n and k with k ≤ n, we have
     n      n−1    n−1
                     
     k   =   k   + k−1   .

    theorem numbertheory_nckeqnm1ckpnm1ckm1 (n k : N) (h0 : 0 < n ∧ 0 < k) (h1 :
        k ≤ n) : Nat.choose n k = Nat.choose (n - 1) k + Nat.choose (n - 1) (k
        - 1) :=
    by
        induction n
        all_goals cases’ k
        all_goals simp [choose, h0 .1.ne’, tsub_eq_zero_of_le (Nat.succ_le_of_lt
        h0 .2), add_zero] at *
        rw [add_comm]


In this case, InternLM2-StepProver exhibits its ability to do simple inductions. In addition, it is
capable to solving high-school level number theory problems as well as the algebra problems.

    Case 2: Putnam 1988 B2
    Natural Language problem: Prove or disprovea : If x and y are real numbers with y ≥ 0 and
    y(y + 1) ≤ (x + 1)2 , then y(y − 1) ≤ x2 .

    theorem putnam_1988_b2:
    (∀ x y : R, (y ≥ 0 ∧ y * (y + 1) ≤ (x + 1) ^ 2) → (y * (y - 1) ≤ x ^ 2))
        ↔ True :=
    by
        refine ⟨fun _ 7→ trivial, fun _ x y hy 7→?_⟩
        ring_nf at hy ⊢
        nlinarith [sq_nonneg (x - y)]

       a
           We search for two directions (prove/disprove) and only present the correct case in our formalization.


The generated proof first breaks up the conjunction into two implications, each becoming a subgoal.
The latter goal is trivial and automatically closed. InternLM2-StepProver then uses automated tactics
such as ring_nf and nlinarith to close the other subgoal. The key step in this proof is to provide
appropriate hints (i.e. sq_nonneq) to the underlying automated tactics.

    Case 3: IMO 1964 P1(2)

    Natural Language problem: Prove that there is no positive integer n for which 2n + 1 is
    divisible by 7.

    theorem imo_1964_p1_2 (n : N) : ¬7 | 2 ^ n + 1 :=
    by
        intro h
        rw [← Nat.mod_add_div n 3] at h
        rw [Nat.dvd_iff_mod_eq_zero] at h
        have h1 : n % 3 < 3 := Nat.mod_lt n three_pos
        interval_cases n % 3
        all_goals simp [pow_add, pow_mul, Nat.add_mod, Nat.pow_mod, Nat.mul_mod]
        at h ⊢




                                                         12
IMO 1964 P1 is a composite problem, consisting of a relatively simple first part and a more complex
second part, with the conclusion of the first part being used in the second. In the formalized version,
we omitted the lemma from the first part, which actually increases the difficulty of the problem.
The key to solving the problem lies in finding the cycle of 2n mod 7, which is (1,2,4). The prover
identified that the length of this cycle is 3 and conducted a case analysis based on 3 (having previously
proved some necessary premises), successfully solving the problem.
    Case 4 : Pough 3.2.8

    Natural Language problem: Prove that if H and K are finite subgroups of G whose orders
    are relatively prime then H ∩ K = 1.

    theorem exercise_Dummit_3_2_8 {G : Type*} [Group G] (H K : Subgroup G)
      [Fintype H] [Fintype K]
      (hHK : Nat.Coprime (card H) (card K)) :
      H ⊓ K = ⊥ :=
    by
        rw [eq_bot_iff_forall]
        rintro x ⟨hx : x ∈ H, hx’ : x ∈ K⟩
        have : x ∈ H ⊓ K := ⟨hx, hx’⟩
        rw [inf_eq_bot_of_coprime hHK] at this
        exact Subgroup.mem_bot.mp this


InternLM2-StepProver is also capable of solving undergraduate problems that needs to reason over a
larger repository of premises, in this case the knowledge of group and co-prime. The case exhibits
LEAN-GitHub’s effectiveness on versatile mathematic reasoning tasks.




                                                   13
