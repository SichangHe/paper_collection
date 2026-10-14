                                            TopoAlign: A Framework for Aligning Code to Math via Topological
                                                                    Decomposition
                                                                                         Yupei Li* †
                                                                                 Imperial College London, UK
                                                                                      yl7622@ic.ac.uk

                                                        Philipp Borchert†                               Gerasimos Lampouras
                                                 Huawei Noah’s Ark Lab, London, UK                  Huawei Noah’s Ark Lab, London, UK
                                                 philipp.borchert@h-partners.com                    gerasimos.lampouras@huawei.com

                                                              Abstract                              such as Lean 4. However, proficiency in these
                                                                                                    formal languages requires specialized expertise;
                                            Large Language Models (LLMs) excel at both
                                                                                                    consequently most math problems are initially ex-
arXiv:2510.11944v2 [cs.CL] 1 Sep 2026




                                            informal and formal (e.g. Lean 4) mathematical
                                            reasoning but still struggle with autoformali-          pressed in Natural Language (NL). While NL is
                                            sation, the task of transforming informal into          ideal for human communication, its inherent flexi-
                                            formal mathematical statements. Yet, the per-           bility and contextual dependence make it challeng-
                                            formance of current Math LLMs is constrained            ing to translate into a formal system. Bridging this
                                            by the scarcity of large-scale corpora, partic-         gap requires autoformalisation, the process of faith-
                                            ularly those containing pairs of informal and           fully translating informal NL math problems into
                                            formal statements. Interestingly, the formal lan-
                                                                                                    FL. This step is essential for interacting with auto-
                                            guages used in autoformalisation share struc-
                                            tural similarities with programming languages,
                                                                                                    mated verifiers for tasks such as proof generation
                                            and code data is available at scale. However,           (Wu et al., 2022a; Ahn et al., 2024).
                                            current models trained on code do not trans-               Despite recent advances, LLMs still struggle
                                            fer effectively to formal math, due to structural       with autoformalization, in part due to the lack of
                                            and syntactic differences between them. To              large-scale, high-quality parallel datasets pairing
                                            address this, we propose TopoAlign, a frame-            natural language problem descriptions with corre-
                                            work that unlocks widely available code repos-          sponding formal statements or proofs (Wu et al.,
                                            itories as training resources for Math LLMs.
                                                                                                    2022a). Synthetic datasets such as Herald State-
                                            TopoAlign decomposes code into docstrings,
                                            main functions, and dependency functions, and           ments (Gao et al., 2025), Numina v1.5 ATF (Guo
                                            reassembles these components into analogues             et al., 2025), and Goedel-Pset (Lin et al., 2025)
                                            that structurally mirror formal statements. We          partially address this gap, but their scale and diver-
                                            train three state-of-the-art models, D EEP S EEK -      sity remain limited and not annotated by human
                                            M ATH, Q WEN -3 and H ERALD, and evaluate               expert. Furthermore, these approaches rely on gen-
                                            them on the MiniF2F, Putnam, and ProofNet               erating synthetic informal-formal pairings, which
                                            benchmarks. TopoAlign provides substantial
                                                                                                    are inherently constrained by the quality and cov-
                                            gains for D EEP S EEK -M ATH, improving perfor-
                                            mance by 17.77% on BEq@10 and 68.82% on
                                                                                                    erage of the underlying generative models, and do
                                            typecheck@10, and also measurably improves              not scale naturally with the availability of existing
                                            H ERALD by 0.12% on BEq@10 and 1.09%                    large-scale resources such as code repositories. As
                                            on typecheck@10 despite introducing no new              a result, current models either fail outright or re-
                                            mathematical knowledge.                                 quire thousands of attempts and auxiliary retrieval
                                                                                                    systems to produce accurate formalisations of even
                                        1   Introduction                                            simple math problems (Li et al., 2024).
                                        Neuro-symbolic approaches that pair LLMs with                  To overcome this data bottleneck, we look to
                                        proof assistants, such as Isabelle (Nipkow et al.,          the vast resources available in software engineer-
                                        2002a) or Lean 4 (Moura and Ullrich, 2021), enable          ing. Building on the assumption that models can
                                        advanced math reasoning by enforcing rule-based             learn the structure of a task from syntactically
                                        logical consistency (Welleck and Saha, 2023).               aligned data, even if the data is semantically dis-
                                        These assistants operate on Formal Languages (FL),          tinct from the final domain. This insight unlocks
                                           * Work conducted during an internship at Huawei Noah’s
                                                                                                    widely available code repositories as large-scale
                                        Ark Lab, London.                                            data sources for training Math LLMs. Beyond
                                           †
                                             Equal contribution.                                    providing scale, code data offers structural diver-
                                                                                     Informal     Prove the ceiling of the square root of 27 minus the
            Docstring        Read data from a database based on a
                             given category, normalize the content.                 Statement           floor of the square root of 26 equals 1




                         def main(dbfile, category):
                             db = sqlite3.connect(dbfile)
                             cursor = db.cursor()
                             members = get_category_members(db, category)                       theorem mathd_algebra_151 : Int.ceil
              Main                                                                   Formal     (Real.sqrt 27) - Int.floor (Real.sqrt 26) = 1
                             for member in members:
            Function             title = member[0]
                                                                                    Statement    := sorry
                                 content.append(get_and_normalize(db,title))
                             return content




            Repository                                                               Mathlib
             Library                                                                 Library



                                                                                                def floor : α → ℤ := floor_ring.floor
                         def get_category_members(db, category)
                                                                                                                          def toSet (u : ZFSet.{u})
          Dependencies                                     def print_db(db)     Dependencies    Set ZFSet.{u} := {x | x ∈ u}
                         def get_and_normalize(db, page)
                                                                def count(db)                           def ceil : α → ℤ := floor_ring.ceil




Figure 1: Structural similarity between code (left) and formal statements in Lean 4 (right). Code samples extracted
from GitHub repositories are decomposed into: the docstring, which maps to informal statements in mathematical
problems, the main function, which corresponds to the formal statements, and the dependency functions, which
correspond to supporting lemmata and theorems, included in external libraries (e.g. Mathlib for Lean 4).

sity, requiring complex problem-solving skills that                             code with formal mathematical languages. 2) We
we posit are transferable to formal mathematics.                                propose CAF, a training task that leverages the
Leveraging these corpora requires aligning the com-                             structurally aligned code dataset to emulate auto-
positional patterns of code with those of formal                                formalisation, thereby reducing the dependence on
proofs. We propose TopoAlign, a framework that                                  annotated pairs of informal and formal mathemat-
structurally aligns programming code with formal                                ical statements. 3) We release a large-scale semi-
math. TopoAlign decomposes code into docstrings,                                synthetic pre-training dataset of 300 million tokens,
main functions, and dependency functions, then                                  consisting of high-quality, structurally aligned code
reassembles these components into sequences that                                designed for autoformalisation tasks. 4) Through
mirror the structure of Lean 4 formal statements                                detailed ablation studies, we demonstrate that a
(see Figure 1). This alignment teaches the model                                balanced ratio of our aligned code data and formal
the compositional structure of formal math and en-                              mathematical statements yields optimal autoformal-
ables the transfer of problem-solving capabilities                              isation performance.
learned from code without introducing new math-
ematical knowledge. Using this aligned corpus,                                  2      Related Work
we introduce code autoformalisation (CAF). This
task emulates autoformalisation by aligning depen-                              Previous methods for autoformalisation draw inspi-
dency functions, and main function bodies with                                  ration from machine translation literature (Wang
informal descriptions (code docstrings), supporting                             et al., 2018; Dwivedi et al., 2022), i.e. Szegedy
lemmata, and formal statements in Lean. Unlike                                  (2020) propose encoding NL and FL in a shared
regular code generation, our setting provides a syn-                            latent space and selecting translation candidates
thetic docstring that already includes the solution                             based on embedding similarity. Some approaches
intent. We train D EEP S EEK -M ATH (Shao et al.,                               focus on rule-based methods, such as GFLean,
2024), H ERALD (Gao et al., 2025), and Q WEN -3                                 which uses the Grammatical Framework for pars-
(Yang et al., 2025) with TopoAlign and the CAF                                  ing and linearization (Pathak, 2024). However,
objective. On the MiniF2F, Putnam, and ProofNet                                 these methods struggle to adapt to diverse inputs,
benchmarks, the method yields consistent gains,                                 as their rules require frequent updates. In contrast,
achieving relative BEq improvements of 36.7% for                                LLMs provide more flexibility and consequently
D EEP S EEK -M ATH and 6.2% for H ERALD.                                        show strong autoformalisation performance (Jiang
                                                                                et al., 2022; Jiang, 2024; Wu et al., 2022b).
  Contributions: 1) We introduce TopoAlign, a                                      Despite their success in narrow domains (Soroco
novel method addressing the shortage of training                                et al., 2025; Zhu et al., 2024), these methods
corpora for Math LLMs by structurally aligning                                  face a common challenge: the scarcity of paired
NL-FL math datasets. Various approaches are             3     Methodology
aimed to extend the training datasets: ATLAS (Liu
et al., 2025b) employs a student-teacher frame-         We posit that current Math LLM performance is
work to generate synthetic data, but its perfor-        constrained primarily by the scarcity of large-scale
mance is bounded by the teacher model’s math-           training corpora. Large code datasets have already
ematical knowledge. Additionally, ATLAS gener-          proven valuable for initializing these models (Shao
ates fully synthetic data from existing Lean code.      et al., 2024; Wang et al., 2025), yet code data re-
Herald Statements (Gao et al., 2025) are syn-           mains largely untapped during subsequent training
thetically generated and limit the novelty of the       on formal mathematics. Our TopoAlign framework
resulting data. Jiang et al. (2024) demonstrate         and CAF address this gap, detailed as follows.
that high-quality multilingual data yields further
                                                        3.1    Topological Decomposition of Code for
performance gains in autoformalization, a find-
                                                               Structural Alignment with Formal Math
ing echoed by Chan et al. (2025). Several high-
quality, human-annotated datasets have been cu-         TopoAlign builds on the premise that code and
rated, including ProofNet (Azerbayev et al., 2022),     formal mathematical statements share a composi-
MiniF2F (Zheng et al., 2022), Putnam (Tsoukalas         tional structure. Functions in code solve distinct
et al., 2024), and the Mathlib library itself (Com-     subproblems and may rely on auxiliary functions,
munity, 2020). While invaluable, creating these         analogous to how formal statements resolve in-
datasets is resource-intensive, requires domain ex-     formal problem descriptions using lemmata and
perts, and is consequently limited in scale. To ad-     theorems. We therefore decompose code at the
dress this, we find code data as a scalable alterna-    function level (see Figure 1) into three transfer-
tive to mathematical data.                              able components: (i) the docstring, corresponding
                                                        to the informal problem statement, (ii) the main
                                                        function body, serving as a proxy for the formal
   This is motivated by Chen et al. (2021a), who        statement; and (iii) its dependency functions, cor-
demonstrate that pretraining on code transfers to       responding to supporting lemmata or library the-
autoformalization, with Codex achieving notable         orems (i.e., from Mathlib in Lean 4). We select
few-shot performance on such tasks. As such,            Lean as the representative mathematical formal
Math LLMs are initialised from LLMs trained on          language in this work, while other systems such
extensive code data and progressively fine-tuned        as Isabelle (Nipkow et al., 2002b) and Coq (The
on mathematical datasets. Llemma (Zhang et al.,         Coq Development Team, 2020) are discussed in
2024), Kimina (Wang et al., 2025) and D EEP S EEK -     Appendix I. Disassembling code into components
M ATH (Shao et al., 2024) follow this paradigm. Li      that mirror those in formal mathematics enables
et al. (2024) argue that the autoformalization poten-   structural transfer. Importantly, TopoAlign targets
tial of Math LLMs remains underexplored when            structural alignment and does not assume seman-
leveraging general-purpose code data during pre-        tic equivalence between programming-language
training. To address this, we propose topologically     type systems and Lean’s dependent type system.
decomposing and aligning code from repositories         The framework provides complementary pretrain-
with formal math statements, unlocking a scalable       ing data that enhances, rather than replaces, train-
new source of training data for LLMs.                   ing on formal mathematical corpora.
                                                           To extract functional dependencies, we employ
                                                        a topological dependency parser that performs a
   Finally, given data scarcity, previous work ex-      breadth-first search to build function-level depen-
plored techniques for efficient usage of available      dency graphs (see Algorithm 1 in Appendix H).
data. Related methods aim to extract the inher-         This contrasts with file-level dependency extrac-
ent relationships between NL and FL in the data,        tion (i.e., DeepSeek (Guo et al., 2024)), which cap-
proposing alignment methods based on symbolic           tures inter-file execution order but omits intra-file
equivalence and semantic consistency (Li et al.,        functional relationships. Our parser leverages ab-
2024). However, aligning NL and FL remains chal-        stract syntax trees to trace calls and parent defini-
lenging when their formats and structures differ,       tions across files, and is designed to handle stan-
making it difficult to transfer the LLMs knowledge      dalone functions, class or instance methods, re-
and reasoning capabilities between NL and FL.           cursive calls, and imports. The result is a tree-
                                                                                                                        5000
structured representation of code dependencies, as
shown in Figure 2.                                                                                                      4000




                                                                                                 Number of JSON Files
                                                                                                                        3000
                          Root Node                                  Depth 1      Depth 2


                        driveToTarget                               calcRotDeg       ...                                2000
 Navigate the robot to a specified target position by
                                                        Docstring                getPosition
 driving forward


 def driveToTarget(self, targetX, targetY):
                                                                                                                        1000
     grid_x, grid_y = getPosition()
     rotDeg = calcRotDeg()                                Code        drive
     self.drive(100, 100)
                                                                                     ...
     self.driveToTarget()
                                                                                                                           0
                                                                                     ...                                           1       2       3       4           5       6     7    8     9
                                                                                                                                                               Max Depth
Figure 2: Function-level dependency tree showing the
hierarchy of function calls, starting from the root node.                                      Figure 3: Distribution of maximum dependency tree
Each child node represents a function called by its par-                                       depths across a random sample of 200 repositories.
ent. The docstring for the root node is extracted to
                                                                                                                        4000
represent the description of the problem addressed.
                                                                                                                        3500




                                                                                                 Number of JSON Files
                                                                                                                        3000
   To obtain informal problem statements, we ex-
                                                                                                                        2500
tract natural language descriptions from docstrings                                                                     2000
and README files. To obtain informal problem                                                                            1500
statements, we extract natural language descrip-                                                                        1000
tions from docstrings and README files. How-                                                                             500
ever, as docstrings describe a function’s interface                                                                        0
                                                                                                                               0       1   2   3   4   5       6   7       8   9 10 11 12 13 14 >15
                                                                                                                                                           Max Siblings
rather than its implementation, they do not always
align with the needs of autoformalization. We there-                                           Figure 4: Distribution of the maximum number of sib-
fore use Q WEN -3 (Yang et al., 2025) to generate                                              lings in dependency trees across a random sample of
concise summaries of each function’s implemen-                                                 200 repositories.
tation logic, augmenting missing or low-quality                                                3.2                       Code Autoformalisation (CAF)
documentation. We perform 10-gram contamina-
tion analysis, following Guo et al. (2024), to ensure                                          To leverage structurally aligned code for training
no information leakage between our dataset and the                                             Math LLMs on autoformalisation, we introduce
test set, and confirm no meaningful overlap.1 We                                               CAF, which emulates the autoformalisation process
have also provided additional analyses of the gen-                                             on code data. Treating each aligned code instance
erated dataset, including its length distribution and                                          as an analogue of a formalisation scenario allows
LLM-as-a-Judge scores, in Appendix G.                                                          the model to learn structural patterns while transfer-
                                                                                               ring general problem-solving strategies acquired in
   We analyse the structural properties of function-
                                                                                               programming. Importantly, our method focuses on
level dependency trees in the collected code to se-
                                                                                               transferring structural and problem-solving capa-
lect repositories whose hierarchical patterns resem-
                                                                                               bilities, rather than introducing new mathematical
ble those found in formal mathematics. For each
                                                                                               knowledge. While we recognize that this technique
repository we compute the maximum tree depth,
                                                                                               could be adapted to emulate other formal reason-
reflecting overall complexity and the maximum
                                                                                               ing tasks like theorem proving, in this work, we
number of sibling nodes at any depth, indicating
                                                                                               focus specifically on addressing the prevalent data
the breadth of direct dependencies. We retain repos-
                                                                                               scarcity bottleneck in autoformalisation.
itories with depth between 3 and 6 and maximum
                                                                                                  We train Math LLMs using a mixture of
sibling counts between 3 and 10, thus excluding
                                                                                               TopoAlign code data and formal mathematical data.
overly complex codebases as well as simple scripts.
                                                                                               This combined approach integrates mathematical
Figures 3 and 4 show the distributions of maximum
                                                                                               knowledge and structure with problem-solving ca-
depth and maximum sibling count for a random
                                                                                               pabilities from code, while also mitigating catas-
sample of 200 repositories. After filtering, the cor-
                                                                                               trophic forgetting during fine-tuning (Chen et al.,
pus contains 156,684 functions comprising 324.5
                                                                                               2019). In our multi-task training approach, each
million tokens.2
                                                                                               training sample consists of an input x, a docstring
     1                                                                                         for code or an informal statement for math, and a
    Additional details are provided in Appendix F.
     2
    Dataset available at:       https://huggingface.co/                                        set of dependencies d, a set of dependency func-
datasets/Formal-Math-Reasoning/TopoAlign_Python.                                               tions for code or supporting lemmata and theorems
                                  TopoAlign Code Data


                   Docstring                       Dependencies                                           Main Function

                                                                                                  def navigate_to(robot,
                                                                                                  target_x, target_y):
                A function to navigate           def locate(robot):                     +             while (robot.x, robot.y) !=
                    robots to the
                     destination.
                                           +         return robot.x,
                                                 robot.y
                                                                                                      (target_x, target_y):
                                                                                                          ...
                                                                                                          return locate(robot)




                                                                       LLM 🤖

               Informal Statement                  Dependencies                                         Formal Statement

                                                                                                   theorem mathd_algebra_151 :
                 Prove the ceiling of
                the square root of 27
                                                 def ceil : α → ℤ :=                    + +        Int.ceil (Real.sqrt     27) to a
                                                                                                             Navigate the robot
                                                                                                             specified target position
                minus the floor of the
                  square root of 26
                                           +         floor_ring.ceil
                                                                                                   - Int.floor
                                                                                                               by driving
                                                                                                   (Real.sqrt 26)    = 1 forward
                      equals 1.                                                                    := sorry



                                    Formal Math Data




Figure 5: Overview of the training pipeline. Input consists of a problem description (for either code or math) and its
dependencies. The training objective is to generate the corresponding solution: the root code block for code inputs,
or the formal statement for math inputs.

for math. The model is conditioned on x and d and                         (Yang et al., 2025). We evaluate three base mod-
trained to generate the target y: the main function                       els: D EEP S EEK -M ATH (7B) (Shao et al., 2024),
for code data or the formal statement for math data,                      H ERALD (7B) (Gao et al., 2025) and Q WEN -3
as illustrated in Figure 5.                                               (4B) (Yang et al., 2025) with their instruct ver-
   The proportion of code and math samples dur-                           sions. H ERALD is specialised for autoformaliza-
ing training is controlled by parameter α, where                          tion, having been trained on the synthetic Herald
α determines the fraction of math samples and                             Statements data. In contrast, D EEP S EEK -M ATH is
1 − α the fraction of code samples. The over-                             trained on a broader range of mathematical data
all objective is defined as L = α Lmath + (1 −                            from DeepSeek-Coder (Guo et al., 2024), opti-
α) LCAF , where Lmath and LCAF denote the losses                          mised for general mathematical problem-solving
for math and code tasks, respectively. For each                           rather than explicit autoformalization. We addition-
task, the loss is computed using next-token pre-                          ally evaluate Q WEN -3, a state-of-the-art general-
diction, Pformulated as the negative  log-likelihood                     purpose reasoning model pre-trained on large-scale
L = − N     i=1 log P  y
                     θ i   | y <i , x  , where x is the                   mathematical corpora to enhance its reasoning ca-
input sequence, y = (y1 , y2 , . . . , yN ) is the target                 pabilities. This setup allows us to compare a dedi-
sequence, and Pθ is the model with parameters θ.                          cated autoformalization model against models with
                                                                          broader mathematical and code understanding.4
4       Experiments                                                           We should note that TopoAlign should be under-
                                                                          stood as a continual pre-training methodology for
Training Data.         Our code data is sourced                           math autoformalisation from code repositories, in-
from Python repositories in the Stack v2 dataset                          tended for use in the pre- and mid-training phases
(Lozhkov et al., 2024). For formal mathematical                           of LLMs providing more structural information
statements, we use the Herald Statements corpus                           and problem understanding information. As such,
(Gao et al., 2025), a synthetic dataset built from                        it is orthogonal to fine-tuning-based approaches. It
Mathlib (Community, 2020). It contains Lean state-                        follows that to meaningfully compare TopoAlign
ments similar in style and structure to those found                       against fine-tuned SOTA formalizers, it would re-
in math pretraining corpora, while avoiding over-                         quire to retrain the latter with TopoAlign data under
lap with downstream evaluation benchmarks such                            identical conditions, which is beyond the scope of
as MiniF2F, ProofNet, and Putnam. Dependency                              this study. Instead, we compare against baselines
functions for the formal statements are extracted                         using different data distributions as follows, which
using the jixia library.3                                                 we argue provides a fair and interpretable evalua-
Models.      We evaluate three base models:                               tion of TopoAlign’s contribution.
D EEP S EEK -M ATH (7B) (Shao et al., 2024), H ER -                            4
                                                                               We do not benchmark StepFun-Formalizer (Wu et al.,
ALD (7B) (Gao et al., 2025) and Q WEN -3 (4B)                             2026) or Kimina-Autoformalizer (Wang et al., 2025) due to
                                                                          benchmark contamination, as MiniF2F, ProofNet, and Putnam
    3
        https://github.com/frenzymath/jixia                               are included in their training data.
Settings. For each base model, we evaluate four                 tablished LLM-as-judge evaluation paradigm (Gu
distinct variations, namely Baseline, Math, Code                et al., 2025).
and TopoAlign. The Baseline setting evaluates the
pretrained models directly on downstream tasks                  5   Results and Discussion
without any additional fine-tuning. The Math set-
ting involves fine-tuning models exclusively on for-            Table 1 presents the Typecheck and BEq results
mal mathematical data from the Herald Statements                under the pass@k metric (Chen et al., 2021b) with
corpus, which is equivalent to applying the CAF                 k = {1, 10}, where a problem is considered solved
objective with a mixing ratio of α = 1.0. This                  if at least one of the k sampled solutions is cor-
allows us to assess the impact of training on purely            rect, evaluated on the MiniF2F-valid, MiniF2F-test,
mathematical data. In the Code setting, models                  ProofNet, and Putnam datasets. We additionally
are trained only on unaligned code data extracted               report unbiased pass@1 results in Appendix A.1.
from the Stack-V2 corpus, providing a control to                   Our proposed TopoAlign method outperforms all
test the effect of training without structural align-           benchmarked methods across most of the datasets
ment via TopoAlign. Finally, the TopoAlign set-                 and model families on the BE@10 metric, with
ting trains models on a balanced combination of                 the exception of H ERALD on ProofNet. Table
formal mathematics and structurally aligned code                5 shows that TopoAlign achieves the best over-
using CAF, with a mixing ratio of α = 0.5. This                 all model performance, measured by average rank
setting uses 4,000 randomly selected samples from               across datasets, for D EEP S EEK -M ATH, Q WEN -3,
GitHub repositories and 4,000 from the Herald                   and H ERALD. For example, D EEP S EEK -M ATH
Statements dataset. For consistency, the number of              BEq@1 on MiniF2F-valid increases by 9.65% to
training samples is kept equal across all settings.5            14.47%. Some variance in BEq@1 is expected
Hyperparameter and prompt details are provided in               due to stochastic sampling, which can account
Appendix C.                                                     for occasional drops, such as the slightly lower
                                                                score for H ERALD on Putnam. In the more robust
Benchmarks. We evaluate models on several
                                                                BEq@10 evaluation, TopoAlign yields consistent
Lean 4 autoformalisation benchmarks: Putnam
                                                                improvements across D EEP S EEK -M ATH, Q WEN -
(Tsoukalas et al., 2024), the validation and test
                                                                3, and H ERALD on Putnam, MiniF2F-valid, and
sets of MiniF2F (Zheng et al., 2022), and ProofNet
                                                                MiniF2F-test. These results demonstrate that topo-
(Azerbayev et al., 2022). Each benchmark consists
                                                                logical alignment effectively transfers structural
of paired natural language and formal language
                                                                knowledge from code to formal mathematics even,
statements. Among these, Putnam is the most chal-
                                                                though it introduces no additional mathematical
lenging problems, ProofNet comprises textbook
                                                                knowledge. These gains are observed across model
theorems, and MiniF2F is considered the most in-
                                                                architectures and datasets.
distribution benchmark, as it overlaps with Mathlib.
                                                                   TopoAlign consistently surpasses code-only vari-
Evaluation Metrics. We measure model perfor-                    ants for both H ERALD and D EEP S EEK -M ATH on
mance using two primary metrics. First, we use                  BEq and Typecheck, indicating that unaligned code
Typecheck (TC) with the Lean 4 compiler (v4.21.0)               data alone does not provide structural information
to verify the syntactic correctness of generated                beneficial for autoformalization. This is further evi-
statements (Poiroux et al., 2025; Limperg, 2025;                denced by H ERALD, which already has more math
Rabe et al., 2020; Wu et al., 2022b). For a more rig-           knowledge than other base models, trained solely
orous assessment of semantic fidelity, we employ                on code data. Its BEq scores and typecheck accu-
bidirectional equivalence (BEq) (Liu et al., 2025a),            racy decreases significantly, with generated outputs
which uses an LLM to generate proof tactics es-                 frequently syntactically invalid despite occasional
tablishing logical equivalence between the model’s              semantic plausibility (see Appendix D). This sug-
output and the reference statement. This provides               gests that raw code data not only fails to benefit aut-
a stronger signal of faithful autoformalization than            oformalization but may actively degrade an already
typechecking alone, and is consistent with the es-              capable model’s formalization ability, highlighting
                                                                the necessity of structural alignment and a proper
   5
     Each instance is a complete reasoning example and there-   training paradigm. In contrast, topological align-
fore cannot be meaningfully split to match token counts.
Matching token counts by selecting shorter examples would       ment and the CAF task enable effective transfer
instead bias the data toward simpler code or proofs.            of both problem-solving and structural knowledge
Table 1: Auto-formalisation performance in percent for MiniF2F, ProofNet, and Putnam datasets under pass@1 and
pass@10 metrics for Typecheck (TC) and BEq. Baseline setting refers to the pretrained model, Math is trained on
additional formal math data and code is trained on additional code data that is not structurally aligned. TopoAlign
mixes math and structurally aligned code data.

          Dataset         Base Model        Setting     TC@1          BEq@1        TC@10        BEq@10
                                            Baseline     0.00          0.00         0.00         0.00
                                            Math        45.18          9.65        79.82        19.74
                       D EEP S EEK -M ATH
                                            Code        42.98         10.53        88.16        23.68
                                            TopoAlign   51.75         14.47        87.28        26.32
                                            Baseline     2.63          0.00        21.93         0.00
       MiniF2F-valid                        Math        81.58         13.16        100.00       82.02
                           Q WEN -3
                                            Code        97.37          0.00        100.00        0.00
                                            TopoAlign   77.19         13.16        100.00       85.53
                                            Baseline    73.25         25.44        92.98        38.16
                                            Math        75.44         24.12        93.86        41.23
                           H ERALD
                                            Code        75.00         20.61        90.79        32.02
                                            TopoAlign   76.75         26.75        94.74        41.23
                                            Baseline     0.00          0.00         0.00         0.00
                                            Math        43.11          9.33        77.33        21.78
                       D EEP S EEK -M ATH
                                            Code        52.89          7.56        91.52        26.79
                                            TopoAlign   54.67         16.89        88.89        29.78
                                            Baseline     6.22          0.00        37.33         0.00
       MiniF2F-test                         Math        84.44         10.22        100.00       74.22
                           Q WEN -3
                                            Code        97.78          0.00        100.00        0.00
                                            TopoAlign   88.89         23.11        100.00       84.00
                                            Baseline    78.22         24.44        95.54        41.96
                                            Math        80.89         24.44        95.54        40.36
                           H ERALD
                                            Code        80.89         20.89        90.63        34.38
                                            TopoAlign   79.56         27.56        94.20        42.86
                                            Baseline     0.00          0.00         0.00         0.00
                                            Math        21.12          5.35        43.42        12.57
                       D EEP S EEK -M ATH
                                            Code        22.73          2.67        49.47         7.49
                                            TopoAlign   32.89          9.09        56.95        14.97
                                            Baseline     6.42          0.16        31.02         0.80
         ProofNet                           Math        28.34          5.88        88.77        37.70
                           Q WEN -3
                                            Code        56.15          0.00        99.47         0.00
                                            TopoAlign   31.02          4.55        95.72        41.71
                                            Baseline    46.52         10.16        74.87        20.32
                                            Math        46.79         10.43        75.40        19.77
                           H ERALD
                                            Code        38.24          4.55        63.37         9.36
                                            TopoAlign   43.85          9.63        75.67        16.84
                                            Baseline     0.00          0.00         0.00         0.00
                                            Math        10.69          0.00        27.04         0.00
                       D EEP S EEK -M ATH
                                            Code        12.58          0.00        37.42         0.00
                                            TopoAlign   17.30          0.00        42.14         0.00
                                            Baseline     1.89          0.00        16.98         0.00
          Putnam                            Math        25.79          0.63        98.11         5.35
                           Q WEN -3
                                            Code        70.44          0.00        100.00        0.00
                                            TopoAlign   19.50          1.26        97.48         9.12
                                            Baseline    37.42          2.20        73.58         4.72
                                            Math        43.71          2.52        70.44         4.09
                           H ERALD
                                            Code        35.85          0.00        69.18         0.00
                                            TopoAlign   36.16          1.57        76.73         4.72


to formal mathematics. Notably, Q WEN -3 trained                mathematical corpora by unlocking code reposi-
on raw code frequently generates degenerate out-                tories as a scalable source of structurally aligned
puts such as endless type definitions (e.g. Nat →               pretraining data. Principally, TopoAlign unlocks
Nat), which pass typechecking but are semantically              code repositories as structurally aligned pretrain-
meaningless, suggesting prior exposure to code                  ing data while leaving the underlying code content
typechecking during training.                                   unchanged, and CAF then facilitates the transfer of
                                                                this knowledge from code to mathematics.
   These findings confirm that TopoAlign and CAF
effectively leverage code data to enhance Math
LLM training, addressing the scarcity of formal
5.1   Qualitative Error Analysis                             Table 3: Ablation study on training data composition
                                                             for D EEP S EEK -M ATH. The table compares Typecheck
                                                             (TC) and BEq scores for pass@1 to identify the optimal
To better understand model behavior, we conduct a
                                                             ratio of formal math data to our aligned code data.
qualitative error analysis on 200 failure cases, com-
prising 50 randomly selected samples per dataset                     Dataset       Data ratio   TC@1    BEq@1
generated by Q WEN -3 with TopoAlign. We cate-                                     α = 0.25     44.74   11.84
gorize the errors into four distinct types as follows,             MiniF2F-valid   α = 0.50     51.75   14.47
                                                                                   α = 0.75     52.63   10.96
with representative cases detailed in Appendix E.
                                                                                   α = 0.25     42.67    7.56
   Type 1: Missing or Incorrect Conditions, i.e.                   MiniF2F-test    α = 0.50     54.67   16.89
conditions are omitted or improperly specified,                                    α = 0.75     56.44   14.67

such as missing universal quantifiers or weakened                                  α = 0.25     12.58    0.00
                                                                     Putnam        α = 0.50     17.30    0.00
constraints. Type 2: Semantically Equivalent but                                   α = 0.75     12.89    0.00
Structurally Different, i.e. generated statements                                  α = 0.25     24.60    6.15
are semantically correct but differ in structural rep-               ProofNet      α = 0.50     32.89    9.09
                                                                                   α = 0.75     26.20    8.29
resentation, such as using set membership in place
of disjunctive equality. Type 3: Variable Type
                                                             5.2   Impact of Code–Math Data Ratio
Mismatch, i.e. variables are assigned incorrect
or incompatible types, producing statements that             We further study the effect of varying the ratio of
are syntactically plausible but semantically invalid.        code to mathematical data in the CAF objective
Type 4: Representation Inconsistency, i.e. vari-             by adjusting the α parameter. We train additional
ables or expressions are inconsistently represented,         D EEP S EEK -M ATH models with α ∈ 0.25, 0.75
leading to semantic mismatches, such as conflating           and report the results in Table 3. A balanced ra-
absolute value notation with distance functions.             tio (α = 0.5) consistently achieves the highest
                                                             or near-highest performance for both TC@1 and
   The distribution of error types across datasets is
                                                             BEq@1. Reducing the proportion of mathematical
summarised in Table 2. The majority of errors fall
                                                             data (α = 0.25) leads to the weakest performance,
under Type 1, accounting for approximately 70%
                                                             likely due to the token-level loss being dominated
of all failures. The primary bottleneck is deemed
                                                             by the longer code samples, biasing the model to-
as deep problem comprehension.
                                                             ward code generation. Increasing the proportion
                                                             of mathematical data (α = 0.75) improves TC@1
Table 2: Distribution of error types across datasets (50     scores, particularly on benchmarks closer to Math-
samples per dataset) generated by Q WEN -3.                  lib, such as MiniF2F, but does not consistently im-
                                                             prove BEq@1. These findings indicate a balanced
 Dataset         Type 1   Type 2   Type 3   Type 4   Other
                                                             mix of code and mathematical data is crucial for
 MiniF2F-valid    28       14        5        2        1
 MiniF2F-test     23       15        5        4        3
                                                             optimal autoformalisation performance: math data
 ProofNet         43        2        1        1        3     enhances syntactic accuracy, while code enhances
 Putnam           47        1        2        0        0     problem-solving capabilities.

                                                             5.3   Base model performance
   This distribution also explains the uneven per-           The D EEP S EEK -M ATH base model, which lacks
formance gains across datasets. For harder bench-            pretraining on autoformalisation tasks, fails to gen-
marks such as ProofNet and Putnam, Type 1 errors             erate meaningful outputs, often producing repeated
overwhelmingly dominate, averaging over 90% of               symbols or malformed syntax that result in type-
failures, indicating that implicit natural language          check failures. In contrast, H ERALD, which is pre-
constraints are too complex for the model to parse           trained on a large mathematical corpus, provides
reliably. Since TopoAlign provides structural align-         strong BEq performance across multiple datasets.
ment rather than additional mathematical knowl-              Notably, the introduction of CAF training fur-
edge, models with stronger inherent reasoning ca-            ther improves its results: for instance, BEq@1 on
pabilities benefit more substantially, as they can           MiniF2F-valid increases from 23.07% to 25.08%,
actively leverage the aligned structure. Weaker              and on MiniF2F-test from 22.70% to 25.64%.
models, by contrast, remain bottlenecked by their            These improvements confirm that TopoAlign pro-
inability to comprehend the underlying math.                 vides significant benefits even for models that al-
ready possess strong autoformalisation capabilities.   of TopoAlign, which is to improve the structural
                                                       quality and utility of available training data rather
6   Conclusion                                         than expand the model’s underlying mathematical
                                                       knowledge.
We show that widely available code repositories
provide a valuable and largely untapped source of      Ethic consideration
training data for mathematical LLMs. We intro-
duce TopoAlign, a structural alignment framework       This research focuses exclusively on computational
that maps code to formal mathematics and yields a      methods for mathematical reasoning and the de-
324.5 million token dataset that mirrors the struc-    velopment of machine learning frameworks to im-
ture of formal mathematical statements. Training       prove autoformalisation. It does not involve human
on this dataset substantially improves performance     subjects, personal data, or any intervention in real-
across four autoformalization benchmarks on both       world populations. All experiments are conducted
Typecheck and BEq, demonstrating that structural       on publicly available datasets or synthetic data de-
and problem-solving knowledge can be transferred       rived from code repositories, and no sensitive or
from code to formal mathematics through structural     private information is used.
alignment. Our ablations further show that a bal-
anced mix of code and formal mathematical data
is important for achieving the best performance.
                                                       References
Beyond autoformalization, TopoAlign may also           Janice Ahn, Rishu Verma, Renze Lou, Di Liu, Rui
provide a useful foundation for related tasks such       Zhang, and Wenpeng Yin. 2024. Large language
                                                         models for mathematical reasoning: Progresses and
as theorem proving.                                      challenges. In Proceedings of the 18th Conference
                                                         of the European Chapter of the Association for Com-
Limitations                                              putational Linguistics: Student Research Workshop,
                                                         pages 225–237, St. Julian’s, Malta. Association for
Due to computational and resource constraints, our       Computational Linguistics.
main experiments focus on a subset of approxi-
                                                       Zhangir Azerbayev, Bartosz Piotrowski, and Jeremy
mately 4,000 code samples and 4,000 math sam-
                                                         Avigad. 2022. Proofnet: A benchmark for autofor-
ples. We would like to emphasize 324.5M tokens           malizing and formally proving undergraduate-level
are currently only considering code repositories in      mathematics problems. In Workshop on MATH-
Python (around 28% in Stack-V2). This corpus             AI: Toward Human-Level Mathematical Reasoning,
can be further extended using other programming          NeurIPS 2022. Poster presented virtually at NeurIPS
                                                         2022.
languages in Stack-V2.
   Moreover, while TopoAlign is designed to aug-       W. Chan, M. Souliman, J. Nordhagen, and 1 others.
ment and structurally enrich existing training data      2025. Lean-ing on quality: How high-quality data
                                                         beats diverse multilingual data in autoformalization.
rather than replace high-quality mathematical cor-       arXiv preprint arXiv:2502.15795.
pora, its performance on research-level benchmarks
such as FATE-H (Jiang et al., 2025) remains lim-       Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,
ited, with all models yielding less than BEq of         Henrique Ponde de Oliveira Pinto, Jared Kaplan,
                                                        Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
0.05. This reflects an inherent constraint: struc-      Brockman, Alex Ray, Raul Puri, Gretchen Krueger,
tural alignment cannot substitute for the advanced      Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela
mathematical knowledge that only high-quality for-      Mishkin, Brooke Chan, Scott Gray, and 39 others.
mal datasets can provide, and such datasets re-         2021a. Evaluating large language models trained on
                                                        code. Preprint, arXiv:2107.03374.
main scarce at the research level. Additionally,
TopoAlign cannot replace high-quality data. For        Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,
example, our additional experiments with Goedel-        Henrique Ponde de Oliveira Pinto, Jared Kaplan,
Formalizer, which was trained on Mathlib, show          Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
                                                        Brockman, Alex Ray, Raul Puri, Gretchen Krueger,
that continued pre-training with additional mathe-      Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela
matical and TopoAlign data does not improve BEq         Mishkin, Brooke Chan, Scott Gray, and 39 others.
performance (Appendix J). This further highlights       2021b. Evaluating large language models trained on
the importance of the quality and complementarity       code.
of the data used for continued pre-training. These     Xinyang Chen, Sinan Wang, Bo Fu, Mingsheng Long,
findings are consistent with the intended scope          and Jianmin Wang. 2019. Catastrophic forgetting
  meets negative transfer: Batch spectral shrinkage for     Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Xian
  safe transfer learning. Advances in neural informa-         Zhang, Fan Yang, and Xiaoxing Ma. 2024. Autofor-
  tion processing systems, 32.                                malize mathematical statements by symbolic equiva-
                                                              lence and semantic consistency. Advances in Neural
The Mathlib Community. 2020. The lean mathematical            Information Processing Systems, 37:53598–53625.
  library. In Proceedings of the 9th ACM SIGPLAN
  International Conference on Certified Programs and        Jannis Limperg. 2025. Tactic script optimisation for
  Proofs, POPL ’20, page 367–381. ACM.                        aesop. In Proceedings of the 14th ACM SIGPLAN
                                                              International Conference on Certified Programs and
Vijay Prakash Dwivedi, Anh Tuan Luu, Thomas Lau-              Proofs, pages 98–111.
  rent, Yoshua Bengio, and Xavier Bresson. 2022.
  Graph neural networks with learnable structural and       Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,
  positional representations. In Proceedings of the In-       Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
  ternational Conference on Learning Representations          Xia, Danqi Chen, Sanjeev Arora, and Chi Jin.
  (ICLR).                                                     2025. Goedel-prover: A frontier model for open-
                                                              source automated theorem proving.     Preprint,
Guoxiong Gao, Yutong Wang, Jiedong Jiang, Qi Gao,             arXiv:2502.07640.
  Zihan Qin, Tianyi Xu, and Bin Dong. 2025. Herald:
  A natural language annotated lean 4 dataset. In Pro-      Q. Liu, X. Zheng, X. Lu, and 1 others. 2025a. Re-
  ceedings of the International Conference on Learning        thinking and improving autoformalization: towards a
  Representations (ICLR). Poster presented at ICLR            faithful metric and a dependency retrieval-based ap-
  2025, Singapore EXPO; slides available online.              proach. In The Thirteenth International Conference
                                                              on Learning Representations.
Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan,
   Xuehao Zhai, Chengjin Xu, Wei Li, Yinghan Shen,          Xiaoyang Liu, Kangjie Bao, Jiashuo Zhang, Yunqi
   Shengjie Ma, Honghao Liu, Saizhuo Wang, Kun                Liu, Yuntian Liu, Yu Chen, Yang Jiao, and Tao Luo.
   Zhang, Yuanzhuo Wang, Wen Gao, Lionel Ni,                  2025b. Atlas: Autoformalizing theorems through
   and Jian Guo. 2025. A survey on llm-as-a-judge.            lifting, augmentation, and synthesis of data. Preprint,
   Preprint, arXiv:2411.15594.                                arXiv:2502.05567.

                                                            Anton Lozhkov, Raymond Li, Loubna Ben Allal, Fed-
Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai
                                                              erico Cassano, Joel Lamy-Poirier, Nouamane Tazi,
  Dong, Wentao Zhang, Guanting Chen, Xiao Bi,
                                                              Ao Tang, Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei,
  Yu Wu, YK Li, and 1 others. 2024. Deepseek-coder:
                                                              and 1 others. 2024. Starcoder 2 and the stack v2: The
  When the large language model meets programming–
                                                              next generation. arXiv preprint arXiv:2402.19173.
  the rise of code intelligence, 2024. URL https://arxiv.
  org/abs/2401.14196, 5:19.
                                                            Leonardo de Moura and Sebastian Ullrich. 2021. The
                                                              lean 4 theorem prover and programming language. In
Qi Guo, Jianing Wang, Jianfei Zhang, Deyang Kong,             Automated Deduction–CADE 28: 28th International
  Xiangzhou Huang, Xiangyu Xi, Wei Wang, Jingang              Conference on Automated Deduction, Virtual Event,
  Wang, Xunliang Cai, Shikun Zhang, and Wei Ye.               July 12–15, 2021, Proceedings 28, pages 625–635.
  2025. Autoformalizer with tool feedback. Preprint,          Springer.
  arXiv:2510.06857.
                                                            Tobias Nipkow, Markus Wenzel, and Lawrence C Paul-
A. Jiang, C. E. Staats, C. Szegedy, and 1 others.             son. 2002a. Isabelle/HOL: a proof assistant for
  2022. Autoformalization with large language models.         higher-order logic. Springer.
  2022.
                                                            Tobias Nipkow, Markus Wenzel, and Lawrence C.
A. Q. Jiang, W. Li, and M. Jamnik. 2024. Multi-               Paulson. 2002b. Isabelle/HOL: A Proof Assistant
  language diversity benefits autoformalization. Ad-          for Higher-Order Logic, volume 2283 of LNCS.
  vances in Neural Information Processing Systems,            Springer.
  37:83600–83626.
                                                            Shashank Pathak. 2024. Gflean: An autoformal-
Jiedong Jiang, Wanyi He, Yuefeng Wang, Guoxiong               isation framework for lean via gf. Preprint,
   Gao, Yongle Hu, Jingting Wang, Nailin Guan, Peihao         arXiv:2404.01234.
   Wu, Chunbo Dai, Liang Xiao, and 1 others. 2025.
   Fate: A formal benchmark series for frontier al-         Auguste Poiroux, Gail Weiss, Viktor Kunčak, and An-
   gebra of multiple difficulty levels. arXiv preprint        toine Bosselut. 2025. Improving autoformalization
   arXiv:2511.02872.                                          using type checking. Preprint, arXiv:2406.07222.

Q. Jiang. 2024. Language Models for Verifiable Math-        Markus N Rabe, Dennis Lee, Kshitij Bansal, and Chris-
  ematical Automation Interaction, Integration, and          tian Szegedy. 2020. Mathematical reasoning via
  Autoformalization. Ph.D. thesis, University of Cam-        self-supervised skip-tree training. arXiv preprint
  bridge, United Kingdom.                                    arXiv:2006.04757.
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,                 fusion. In Proceedings of the AAAI Conference on Ar-
  Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan                tificial Intelligence, volume 40, pages 33980–33988.
  Zhang, YK Li, Yang Wu, and 1 others. 2024.
  Deepseekmath: Pushing the limits of mathematical          An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
  reasoning in open language models. arXiv preprint           Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao,
  arXiv:2402.03300.                                           Chengen Huang, Chenxu Lv, Chujie Zheng, Dayi-
                                                              heng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao Ge,
Mauricio Soroco, Jialin Song, Mengzhou Xia, Kye               Haoran Wei, Huan Lin, Jialong Tang, and 41 oth-
 Emond, Weiran Sun, and Wuyang Chen. 2025. Pde-               ers. 2025. Qwen3 technical report. arXiv preprint
 controller: Llms for autoformalization and reasoning         arXiv:2505.09388.
 of pdes. Preprint, arXiv:2502.00963.
                                                            Lan Zhang, Xin Quan, and Andre Freitas. 2024. Consis-
C. Szegedy. 2020. A promising path towards autofor-           tent autoformalization for constructing mathematical
   malization and general artificial intelligence. In In-     libraries. In Proceedings of the 2024 Conference
   telligent Computer Mathematics: 13th International         on Empirical Methods in Natural Language Process-
  Conference, CICM 2020, Bertinoro, Italy, July 26–31,        ing, page 4020–4033. Association for Computational
  2020, Proceedings 13, pages 3–20, Bertinoro, Italy.         Linguistics.
   Springer International Publishing.
                                                            Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
The Coq Development Team. 2020. The Coq Proof                 2022. minif2f: A cross-system benchmark for formal
  Assistant Reference Manual. INRIA. https://coq.             olympiad-level mathematics. In Proceedings of the
  inria.fr.                                                   International Conference on Learning Representa-
                                                              tions (ICLR). OpenReview.net.
George Tsoukalas, Jasper Lee, John Jennings, Jimmy
  Xin, Michelle Ding, Michael Jennings, Amitayush           N. Zhu, X. Zhang, Q. Huang, and 1 others. 2024. Fgeo-
  Thakur, and Swarat Chaudhuri. 2024. Putnambench:             parser: Autoformalization and solution of plane geo-
  Evaluating neural theorem-provers on the putnam              metric problems. Symmetry, 17(1):8.
  mathematical competition. In NeurIPS 2024 Poster
  Session. Virtual poster presented at the Thirty-eighth    A     Additional results
  Annual Conference on Neural Information Process-
  ing Systems (NeurIPS), Vancouver.                         A.1    Unbiased results
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas               We report the unbiased results in Table 4 as sup-
  Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,          plementary evidence supporting our main find-
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, and 1 oth-        ings. These results, presented alongside prior lit-
  ers. 2025. Kimina-prover preview: Towards large           erature for direct comparison, show a trend where
  formal reasoning models with reinforcement learn-
  ing. arXiv preprint arXiv:2504.11354.                     TopoAlign appears to outperform other training
                                                            frameworks in terms of BEq score and Typecheck.
Qingxiang Wang, Cezary Kaliszyk, and Josef Ur-              Due to resource constraints, we reported pass@1,
  ban. 2018. First experiments with neural transla-
                                                            but they still provide supporting evidence for our
  tion of informal to formal mathematics. Preprint,
  arXiv:1805.06502.                                         hypothesis.

Sean Welleck and Rahul Saha. 2023. llmstep: Llm             A.2    Rank
  proofstep suggestions in lean. In Proceedings of the
  3rd Workshop on Mathematical Reasoning and AI
                                                            We also provide a rank-based comparison in Ta-
  (MATH-AI), NeurIPS 2023. Poster presented virtu-          ble 5, statistically summarized via the standard
  ally at NeurIPS 2023.                                     pass@k metric, to offer a concise overview across
                                                            different training settings. This is more inter-
Y. Wu, A. Jiang, W. Li, and 1 others. 2022a. Auto-
   formalization for neural theorem proving. Artificial     pretable than the raw numbers reported in Table 4
   Intelligence and Theorem Proving (AITP).                 and Table 1. From the average-rank perspective,
                                                            TopoAlign consistently achieves an average rank
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus
  Rabe, Charles Staats, Mateja Jamnik, and Christian        between 1 and 2, outperforming all other settings,
  Szegedy. 2022b. Autoformalization with large lan-         which further corroborates the effectiveness of
  guage models. In Advances in Neural Information           TopoAlign.
  Processing Systems, volume 35, pages 32353–32368.
  Curran Associates, Inc.                                   B     Software and Data
Yutong Wu, Di Huang, Ruosi Wan, Yue Peng, Shijie            To ensure full reproducibility, all data sources,
  Shang, Chenrui Cao, Lei Qi, Rui Zhang, Xishan
  Zhang, Zidong Du, Jie Yan, and Xing Hu. 2026.
                                                            tools, and code are publicly available. All
  Stepfun-formalizer: Unlocking the autoformaliza-          three basemodels we select from hugging-
  tion potential of llms through knowledge-reasoning        face checkpoint (https://huggingface.co/
Table 4: Auto-formalisation performance in percent                    Table 5: Average rank across different settings.
for MiniF2F, ProofNet, and Putnam datasets under un-
biased pass@1 metrics for Typecheck (TC) and BEq.                     Model                 Setting        Avg.Rank ↓
Baseline setting refers to the pretrained model, Math
                                                                                            Baseline          3.63
is trained on additional formal math data and code is
                                                                                            Math              2.50
trained on additional code data that is not structurally              D EEP S EEK -M ATH
                                                                                            Code              2.00
aligned. Topoalign mixes math and structurally aligned
                                                                                            TopoAlign         1.13
code data.
                                                                                            Baseline          3.50
    Dataset         Base Model        Setting     TC@1    BEq@1                             Math              1.94
                                                                      Q WEN -3
                                      Baseline    2.19    0.00                              Code              2.13
                 D EEP S EEK -M ATH
                                      Math        38.16   10.92                             TopoAlign         1.63
                                      Code        36.44   12.41
                                      TopoAlign   44.92   15.90                             Baseline          2.25
                                      Baseline    2.19    0.00                              Math              1.81
                                      Math        78.46   13.95       H ERALD
 MiniF2F-valid       Q WEN -3
                                      Code        97.37   0.00
                                                                                            Code              3.75
                                      TopoAlign   77.68   15.31                             TopoAlign         1.69
                                      Baseline    78.34   23.07
                                      Math        75.74   24.69
                     H ERALD
                                      Code        78.59   21.49
                                      TopoAlign   78.38   25.08   FrenzyMath/Herald_statements).        Ground
                                      Baseline    0.00    0.00
                                      Math        46.40   7.91
                                                                  truth dependencies were processed using Jixia
                 D EEP S EEK -M ATH
                                      Code        48.89   7.47    (https://github.com/frenzymath/jixia), as
                                      TopoAlign   55.83   15.61
                                      Baseline    4.13    0.00
                                                                  detailed in Section 4. Our complete codebase
 MiniF2F-test        Q WEN -3
                                      Math        84.00   13.33   and the generated dataset have been released
                                      Code
                                      TopoAlign
                                                  98.67
                                                  79.60
                                                          0.00
                                                          17.33
                                                                  at        https://huggingface.co/datasets/
                                      Baseline    77.78   22.70   Formal-Math-Reasoning/TopoAlign_Python.
                                      Math        81.02   21.64
                     H ERALD
                                      Code        80.84   21.29
                                      TopoAlign   80.45   25.64   C    Training Hyperparameters
                                      Baseline    0.00    0.00
                                      Math        21.65   4.33
                 D EEP S EEK -M ATH
                                      Code        20.46   1.79
                                                                  The hyperparameters used for training the LLMs
                                      TopoAlign   33.72   8.32    are listed in Tables 6 and 7. We adhere to the de-
                                      Baseline    4.84    0.80
                                      Math        27.54   4.60
                                                                  fault settings provided in the original papers. In
   ProofNet          Q WEN -3
                                      Code        54.55   0.00    our setup, we fine-tune the base models using su-
                                      TopoAlign   30.03   4.63
                                      Baseline    46.92   10.13
                                                                  pervised fine-tuning. The implementation is based
                     H ERALD
                                      Math        47.00   9.12    on the Hugging Face Transformers library (version
                                      Code        27.77   2.55
                                      TopoAlign   46.63   9.84
                                                                  4.52).
                                      Baseline    0.00    0.00
                 D EEP S EEK -M ATH
                                      Math        8.14    0.00    D    Generated Sample from Code-Only
                                      Code        10.82   0.00
                                      TopoAlign   16.26   0.00         Trained Model
                                      Baseline    1.73    0.00
                                      Math        29.84   0.57
   Putnam            Q WEN -3
                                      Code        69.18   0.00
                                                                  These samples are generated by H ERALD trained
                                      TopoAlign   22.96   0.91    exclusively on code data. The outputs demonstrate
                                      Baseline    41.98   2.76
                                      Math        43.87   2.87
                                                                  that while the model captures the underlying logical
                     H ERALD
                                      Code        34.84   0.00    structure correctly, it lacks proficiency in Lean 4
                                      TopoAlign   36.03   1.70
                                                                  syntax. However, this suggests the presence of
                                                                  semantic similarity between programming code
deepseek-ai/deepseek-math-7b-instruct,                            and formal mathematical language.
https://huggingface.co/Qwen/Qwen3-8B,
https://huggingface.co/FrenzyMath/
                                                                   Hyperparameters    D EEP S EEK -M ATH   H ERALD
Herald_translator).The downstream eval-
                                                                   learning rate             2e-4            1e-6
uation benchmarks were sourced directly from
                                                                   weight decay               0.1             0.1
their official repositories: MiniF2F (https://                     epochs                      1               1
github.com/openai/miniF2F), Putnam (https:                         batch size                 32              32
//github.com/trishullab/PutnamBench), and
Herald (https://huggingface.co/datasets/                                Table 6: Training hyperparameter settings.
    Hyperparameters   D EEP S EEK -M ATH   H ERALD
                                                            Reference:
    Temperature             0.70            0.70
    Top-p                   0.95            0.95
                                                            (x, y) = (1, 1) ∨ (x, y) = (16, 2)
    Max tokens              1024            1024            ∨ (x, y) = (27, 3)
                                                            Generated:
Table 7: Inference hyperparameter settings used for
autoformalisation in the pass@10 setting.                   (x, y) ∈ { (1, 1), (16, 2), (27, 3)
                                                            }

                                                         Type 3: Variable Type Mismatch. The gener-
 from math import sqrt, ceil, floor                      ated output assigns an integer type Z to a variable
                                                         that should be typed as a natural number N. Al-
 def evaluate_sqrt_expressions_1():
     assert(int(ceil(sqrt(27))) -
                                                         though syntactically plausible, this type mismatch
     int(floor(sqrt(26))) == 1)                          renders the statement semantically invalid within
                                                         the formal type system.
 def is_increasing_function(a, b):
     '''                                                    Reference:
     The function checks if the function f(x) =             n : N
      4bx + (a+1)x^2 is increasing for x >= 0.
     '''                                                    Generated:
     return 4*b <= 4*b**2 + (a+1)**2
                                                            n : Z

 def is_3_(girls: list[int]) -> int:                     Type 4: Representation Inconsistency. The ref-
     """
     >>> is_3_([1,2,3,4,5,6,7])                          erence uses abs for absolute value and Real.sqrt
     3                                                   with explicit coordinate arithmetic for Euclidean
     """
     return 3
                                                         distance. The generated output instead applies the
                                                         dist function inconsistently: once as a unary dis-
                                                         tance from zero (conflating absolute value), and
                                                         once as a binary point distance, mixing two distinct
E   Error Analysis Examples                              representations within the same statement.

                                                            Reference:
Type 1: Missing or Incorrect Conditions. The                abs y = 6
generated output losses the universal quantification        Real.sqrt ((x - 8)ˆ2 + (y - 3)ˆ2)
over all positive k and all integer multiples m. The
hypothesis h1 : 0 < n is also entirely omitted.             Generated:
                                                            dist x 0 = 6
                                                            dist (x, y) (8, 3)
    Reference:
    h0 : ∀ k : N, 0 < k → ∀ m : Z, x
    ̸= m * π / (2ˆk)
     h1 : 0 < n
    Generated:
    hx : x ̸= π / (2ˆ(n+1))



Type 2: Semantically Equivalent but Struc-
turally Different. The generated output uses set
membership notation ∈ {· · · } in place of explicit
disjunctive equality. While the two expressions
are semantically equivalent, they differ structurally,
which may cause mismatches during formal verifi-
cation or proof search.
F    Training Instructions and Inference              Generated Docstring
     Prompts
                                                      This function synchronizes local and remote
                                                      keywords for a filter by comparing provided
                                                      keywords with existing ones. It identifies
To generate docstrings describing the main            keywords to add and remove, logs changes,
functions in the code repositories, we employ         constructs API parameters, and updates the
Qwen3-14B model (https://huggingface.co/              filter via a PUT request. The response in-
Qwen/Qwen3-14B) using the following prompt for-       cludes added/deleted keywords to confirm
mat:                                                  synchronization.



                                                    def attention_mlp_stack(inputs, out_channel,
    Prompt                                              num_heads, depth, key_dim, attn_ratio,
                                                        mlp_ratio, strides, stack_drop=0,
    Provide a concise description of the prob-          activation="hard_swish", name=""):
    lem solved in the code snippet below. For-          nn = inputs
    mat the response as a docstring.                    embed_dim = nn.shape[-1]
                                                        stack_drop_s, stack_drop_e = stack_drop
    {code}                                              if isinstance(stack_drop, (list, tuple))
                                                        else [stack_drop, stack_drop]
                                                        for ii in range(depth):
                                                            block_name = name +
                                                        "block{}_".format(ii + 1)
   We manually verified 50 randomly sampled doc-            drop_rate = stack_drop_s +
                                                        (stack_drop_e - stack_drop_s) * ii /
strings from our dataset, and all of them exhibit       depth
accurate and complete descriptions of the corre-            nn =
sponding code. Selected samples are provided be-        res_mhsa_with_multi_head_position(nn,
                                                        embed_dim, num_heads, key_dim,
low:                                                    attn_ratio, drop_rate,
                                                        activation=activation, name=block_name)

                                                        if mlp_ratio > 0:
                                                        [. . .]
                                                        if mlp_ratio > 0:
 def sync(self, title: str, keywords:
                                                               nn = res_mlp_block(nn, mlp_ratio,
     Union[str, list[str]]) -> dict:
                                                        drop_rate, activation=activation,
                                                        name=block_name + "mlp_")
      title = validate_title(title)
      keywords = validate_keywords(keywords)
                                                        return keras.layers.Activation("linear",
      filter_item = self.filter(title)
                                                        name=name + "output")(nn)
      remote_keywords = filter_item["keywords"]
      [. . .]
      params = OrderedDict(
             {
               "title": title,
                                                      Generated Docstring
               "context[]":
      filter_item["context"],                         This function constructs a neural
               "filter_action":                       network stack with multi-head at-
      filter_item["filter_action"],                   tention and MLP blocks.          It applies
             }
      )                                               a series of attention mechanisms
                                                      (res_mhsa_with_multi_head_position)
      params.update(self._keyword_params(add_key
      + delete_key))
                                                      and optional MLPs (res_mlp_block)
      response = self._call_api(                      across ‘depth’ layers, adjusting dropout
          "put",                                      rates progressively. The stack supports
      f"/api/v2/filters/{filter_item['id']}",
      params=params                                   configurable heads, key dimensions, ratios,
      )                                               and activation functions, returning a linear
      response["added"] = add_keywords                output layer.
      response["deleted"] = delete_keywords
      return response
                                                     These examples demonstrate that generated doc-
strings faithfully capture the code: the first en-      Table 8: Length statistics of the generated docstrings in
hances a minimal existing docstring with con-           TopoAlign.
cise descriptions of keyword synchronization logic,
                                                          Dimension               Mean        Std.       Median      Max
while the second provides a detailed description of
the multi-layer attention–MLP architecture for a          Token number           356.74     87.14           353     4,391
                                                          Word number             52.97     12.48            52       870
function that originally lacked a docstring.
                                                          Sentence number          2.54      1.04             2        19
   For math-related tasks, we use the following
prompt format:

    Prompt

    Use the following pre-defined Lean 4                Table 9: Repetition statistics of the generated docstrings
    dependencies:                                       in TopoAlign.
    {dependencies}
                                                             Metric                                           Value
    Based on the context and the problem
                                                             Unique lines                                  250,734
    description, generate a single, syntactically
    correct Lean 4 formal statement that
                                                             Unique ratio                                  99.99%
    accurately captures the problem’s meaning.               Exact-match repeated lines                     0.02%

    Problem Description:
    {problem description}

  For code-related tasks, we employ a parallel          erated docstrings, we randomly sample 10,000 ex-
prompt structure:                                       amples and evaluate them using three independent
                                                        LLM judges, DeepSeek-V4-Pro, Qwen3.7-Max,
    Prompt
                                                        and Gemini-3.5-Flash. As reported in Table 10,
    Use the following pre-defined functions:            all three judges consistently assign high scores
    {pre-defined functions}                             for correctness, completeness, and hallucination-
                                                        free generation. The strongest scores are achieved
    Based on the context and the prob-                  by Gemini-3.5-Flash, with average scores of 4.91,
    lem description, generate a syntactically           4.81, and 4.94 out of 5 for correctness, complete-
    correct function implementation that                ness, and hallucination-free generation, respec-
    accurately captures the problem’s meaning.          tively, while the other two judges show the same
    Problem Description:                                overall trend.
    {problem description}


G    Quality of generated dataset
                                                        Table 10: LLM-as-a-Judge evaluation of 10,000 ran-
We provide an extended quality analysis of              domly selected generated docstrings from TopoAlign.
TopoAlign along three dimensions: length, repeti-       Scores range from 1 to 5, with higher scores indicating
tion, and semantic quality. As shown in Table 8, the    better quality.
generated docstrings contain an average of 356.74
                                                         Model              Correctness   Completeness    Hallucination-free
tokens, 52.97 words, and 2.54 sentences, with rela-
                                                         Gemini-3.5-Flash   4.91 ± 0.35    4.81 ± 0.40       4.94 ± 0.28
tively small variance in the median statistics. The      Qwen3.7-Max        4.73 ± 0.60    4.39 ± 0.63       4.83 ± 0.52
maximum values are higher due to a small number          DeepSeek-V4-Pro    4.41 ± 0.96    3.68 ± 0.87       4.45 ± 1.04

of substantially longer docstrings. As shown in
Table 9, the dataset exhibits negligible repetition,
with 250,734 unique lines and a unique ratio of
99.99%; only 0.02% of docstrings have an exact-
match duplicate.                                          The prompts are shown below for the LLM-as-a-
   To further assess the semantic quality of the gen-   judge.
    Prompt                                               call patterns, we construct a directed dependency
                                                         graph where each function call establishes a parent-
    [SYSTEM] You are a rigorous code-                    child relationship. The calling function serves as
    summary evaluator. You will be given a               the parent node, while the called function becomes
    Python function (with its surrounding de-            the child node.
    pendency code) and a natural-language doc-
    string that claims to describe what the func-        I   Extending TopoAlign to other Formal
    tion does.                                               Languages
    Rate the docstring on three axes on an IN-
    TEGER scale of 1–5:                                  Formal statements in other proof assistants (e.g.,
    1. Correctness — Do the statements in the            Coq and Isabelle) share structural similarities with
    docstring accurately reflect the function’s          Lean. Below we show Isabelle and Coq versions
    actual behavior? Penalize wrong claims               of the informal statement: Prove the ceiling of the
    about control flow, return values, side ef-          square root of 27 minus the floor of the square root
    fects, or algorithm. (1 = mostly wrong, 5 =          of 26 equals 1.
    fully accurate)
    2. Completeness — Does the docstring                     Isabelle:
    cover the function’s key behavior: inputs,               theorem ceil_sqrt27_minus_floor_sqrt26:
    outputs, main control flow / algorithmic                 “ceiling (sqrt 27) - floor (sqrt 26) = (1::int)"
    steps, side effects, and error handling? Pe-
    nalize missing pieces. (1 = large gaps, 5 =
    covers all salient behavior)                             Coq:
    3. Hallucination — Does the docstring                    Theorem ceil_sqrt27_minus_floor_sqrt26 :
    introduce facts NOT supported by the code                (up (sqrt 27) - Z.floor (sqrt 26))%Z = 1%Z.
    (invented behavior, non-existent parameters,
    wrong algorithm)? HIGHER score = LESS                   While these formal languages show similar struc-
    hallucination. (1 = many invented claims, 5          tural characteristics to the decomposed code data in
    = no unsupported claims)                             TopoAlign, supporting multiple formal languages
    Return ONLY a JSON object, no                        would require either training dedicated models for
    prose, no markdown: {"correctness":                  each target language or constructing a mixed pre-
    <int 1-5>, "completeness": <int                      training corpus that incorporates multiple formal
    1-5>, "hallucination": <int 1-5>,                    languages. Although this direction offers promis-
    "reason":        "<one sentence, <=40                ing practical applications, it lies beyond the scope
    words>"}                                             of the present work.

    [USER]                                               J   Additional Ablation:
    ### Dependency code (context, may                        Goedel-Formalizer
    be empty)
                                                         We additionally evaluate Goedel-Formalizer-V2-
    \{DEPENDENCY\}
                                                         8B (Lin et al., 2025) under the same experimental
    \{MAIN\}
                                                         settings as our main experiments, and report the
    \{DOCSTRING\}
                                                         results separately in Table 11. Across all continued
                                                         pre-training settings, BEq performance decreases
H    Dependency Tree Extraction                          relative to the baseline, although Typecheck per-
     Algorithm                                           formance occasionally improves. This suggests
                                                         that additional mathematical or code data does not
The dependency tree extraction process is formally       necessarily improve downstream autoformalization
described in Algorithm 1. The algorithm iterates         quality and can instead reduce semantic correctness
through all files within a given directory, systemati-   as measured by BEq. Among the continued pre-
cally identifying user-defined functions, including      training settings, TopoAlign achieves the highest
both class methods and standalone functions. We          BEq@10 performance on MiniF2F-test, ProofNet,
then analyse inter-file and inter-class dependency       and Putnam, although it remains below the base-
relationships. Through static analysis of function       line. These results also highlight the importance of
Algorithm 1 Function Call Dependency Analysis
 1: Input: Python project directory
 2: Output: Dependency graph of function calls
 3: Data Structures:
 4: function_definitions ← {}                                                   ▷ Record defined functions
 5: imports ← {} object_types ← {}         ▷ Imported names → full paths; Object names → class names;
    Save these two to track their parent function definitions or the file where they’re defined
 6: A NALYZE F ILE(f ) for all Python files f in directory (recursively)
 7: procedure A NALYZE F ILE(file_path)
 8:    Parse AST from f ile_path
 9:    Initialize function_calls ← {}, object_types ← {}
10:    for all nodes n in AST do
11:        if n is ClassDef then
12:             Track current class context                                        ▷ Class defined function
13:        else if n is Import/ImportFrom then
14:             Record imports[alias] ← full module path                        ▷ Function from other files
15:        else if n is FunctionDef then
16:             Register function with current_class.name if applicable
17:             Initialize function_calls[name] ← []                                 ▷ Save its dependency
18:        else if n is Assign with constructor call then
19:             Map object_types[var] ← class name          ▷ Record the codes that initialise this function
20:        else if n is Call then                                ▷ Record the codes that call this function
21:             Resolve full function name (direct call(obj()), method call(obj.method()), or imports
    imports[name]
22:             Append to function_calls[current_func]▷ The list to record the dependency information
23:        end if
24:    end for
25: end procedure
26: procedure B UILD D EPENDENCY G RAPH
27:    Filter to keep only project-internal calls
28:    Detect recursive calls (f → f )                                                 ▷ Self-recursive call
29:    Topological Sort:                                                                      ▷ BFS search
30:    Construct nested call tree from sorted order
31:    Insert recursion markers at tree root if needed
32: end procedure



carefully selecting the mathematical data used for
continued pre-training: the Math setting yields the
lowest BEq@10 performance on MiniF2F-valid,
MiniF2F-test, and Putnam, suggesting that addi-
tional formal mathematical data can reduce for-
malization performance when it is not sufficiently
complementary to the model’s existing training dis-
tribution.
Table 11: Autoformalization performance (%) of
Goedel-Formalizer-V2-8B (Lin et al., 2025) on
MiniF2F, ProofNet, and Putnam, reporting pass@1 and
pass@10 for Typecheck (TC) and BEq.

   Dataset      Setting     TC@1    BEq@1   TC@10   BEq@10
                Baseline    80.70   23.87   80.70   24.32
                Code        65.79   20.74   65.79   20.74
MiniF2F-valid
                Math        83.77   17.98   83.77   18.42
                TopoAlign   80.70   19.74   81.14   20.61
                Baseline    84.38   22.97   84.38   23.87
                Code        70.09   18.72   70.54   19.25
 MiniF2F-test
                Math        83.93   17.41   83.93   17.86
                TopoAlign   81.25   19.20   81.70   20.54
                Baseline    51.07   7.40    51.07   7.67
                Code        50.00   3.48    50.00   3.49
  ProofNet
                Math        53.21   5.88    53.21   5.88
                TopoAlign   52.14   6.43    52.41   6.43
                Baseline    53.14   3.41    53.14   3.75
                Code        41.82   1.36    45.28   1.36
   Putnam
                Math        60.38   0.63    60.38   0.94
                TopoAlign   58.81   1.26    59.43   1.57
